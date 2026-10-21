"""Bounded callable-policy bridge and real, network-free MCP path experiments."""
from __future__ import annotations

import argparse
import asyncio
from contextlib import redirect_stdout, redirect_stderr
import copy
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
from importlib import import_module
from importlib.metadata import distributions, version
import io
import json
from pathlib import Path
import platform
import statistics
import sys
import time

from .cases import build_cases
from .model import Call, Case, MockWorld, Oracle
from .native import APC, ROOT, block_network, load_native, provenance

PATHS = ("callable_wrapped", "callable_raw", "callable_mcp", "callable_mcp_canonicalized")


class CallableBridge:
    """Custom trusted bridge for v1 obligations, using native Progent predicates.

    This is not a native Progent delegation protocol. The envelope and runtime
    state arrive through trusted local infrastructure; caller context is supplied
    by a trusted dispatcher. Predicates never mutate admission state.
    """

    def __init__(self, apc: APC):
        load_native()
        if not apc.envelope.verify(apc.key):
            raise ValueError("Cannot translate an invalid native authorization envelope")
        self.envelope = copy.deepcopy(apc.envelope)
        self.key = apc.key
        self.revocations = apc.revocations
        self.transferred_budget = copy.deepcopy(apc.budget.snapshot())
        self.spent = self.transferred_budget["cumulative_cost"]
        self.history = list(apc.composition.action_history)
        self.scope = self.envelope.effective_scope
        # APC's signed envelope does not contain the separate parameter policy.
        rules = apc.validator._policy.get_rules("send_external", "recipient")
        from apc.parameters import AllowlistRule
        if len(rules) != 1 or not isinstance(rules[0], AllowlistRule):
            raise ValueError("This bridge supports one finite recipient allowlist")
        self.recipients = frozenset(rules[0].allowed_patterns)
        if any("*" in p for p in self.recipients):
            raise ValueError("Wildcard recipient translation is outside this experiment")
        self.current: Call | None = None
        self.evaluations: list[dict] = []
        self.commits = 0
        self.module = import_module("secagent.tool")
        self.policy = {}
        for tool in apc.world.functions:
            if tool not in self.scope.actions:
                continue
            if tool == "send_external":
                if "mail:external" not in self.scope.resources:
                    continue
                names = ("body", "recipient")
            elif tool == "save_internal":
                names = ("resource", "body")
            else:
                names = ("resource",)
            self.policy[tool] = [(100, 0, {name: self.predicate(tool, name) for name in names}, 0)]
        with redirect_stderr(io.StringIO()):
            self.module.update_security_policy(self.policy)
        if self.module.security_policy is None:
            raise RuntimeError("Native policy was not initialized")

    def shared_reasons(self, tool: str) -> list[str]:
        call = self.current
        if call is None or call.tool != tool:
            return ["missing_trusted_dispatch_context"]
        reasons = []
        if not self.envelope.verify(self.key):
            reasons.append("invalid_signature")
        if call.actor != self.envelope.chain[-1].principal_id:
            reasons.append("principal")
        if call.session != self.envelope.task_session_id or call.policy_version != self.envelope.policy_version:
            reasons.append("task_or_policy_version")
        if time.time() >= self.envelope.expires_at:
            reasons.append("expired")
        if self.revocations.is_revoked(self.envelope.envelope_id):
            reasons.append("revoked")
        if tool not in self.scope.actions:
            reasons.append("action_scope")
        if self.spent + call.cost > self.envelope.budget_spec.max_cost + 1e-9:
            reasons.append("compute_budget")
        for earlier in self.history:
            pairs = ((earlier, tool), (tool, earlier))
            if any(pair in self.scope.composition_restrictions for pair in pairs):
                reasons.append("composition")
                break
        return reasons

    def predicate(self, tool: str, parameter: str):
        # A real closure has inspectable source, as the native checker requires.
        def allow(value):
            reasons = self.shared_reasons(tool)
            if parameter == "resource" and value not in self.scope.resources:
                reasons.append("resource")
            if parameter == "recipient" and value not in self.recipients:
                reasons.append("recipient")
            self.evaluations.append({"tool": tool, "parameter": parameter, "value": value,
                                     "allowed": not reasons, "reasons": reasons})
            return not reasons
        return allow

    def commit(self, call: Call, effects: list[dict]) -> None:
        if not effects or self.current != call:
            raise RuntimeError("State commit requires the dispatched observable effect")
        self.spent += call.cost
        self.history.append(call.tool)
        self.commits += 1

    def state(self):
        return {"spent": self.spent, "history": list(self.history), "commits": self.commits,
                "envelope_id": self.envelope.envelope_id}

    def handoff_record(self):
        return {"envelope_verified": self.envelope.verify(self.key),
                "chain": [p.principal_id for p in self.envelope.chain],
                "resources": sorted(self.scope.resources), "actions": sorted(self.scope.actions),
                "composition_restrictions": sorted(self.scope.composition_restrictions),
                "budget_snapshot": self.transferred_budget, "history": list(self.history),
                "recipient_allowlist": sorted(self.recipients),
                "recipient_policy_is_in_signed_envelope": False,
                "transport": "trusted in-process transfer; no cross-machine authentication claim"}


class PathRunner:
    def __init__(self, world: MockWorld, bridge: CallableBridge, path: str):
        if path not in PATHS:
            raise ValueError(path)
        self.world, self.bridge, self.path = world, bridge, path
        self.client = None
        if path == "callable_wrapped":
            self.functions = {name: bridge.module.secure_tool_wrapper(fn) for name, fn in world.functions.items()}

    async def __aenter__(self):
        if self.path.startswith("callable_mcp"):
            from fastmcp import Client, FastMCP
            from fastmcp.server.proxy import ProxyClient
            # Import the unmodified author middleware. Its module's remote proxy
            # remains inert; only the newly constructed in-memory proxy is used.
            with redirect_stderr(io.StringIO()):
                native_proxy = import_module("secagent.mcp_proxy")
                self.bridge.module.update_security_policy(self.bridge.policy)
            backend = FastMCP("pilot mock backend")
            for name, fn in self.world.functions.items():
                backend.tool(name=name)(fn)
            proxy = FastMCP.as_proxy(ProxyClient(backend), name="pilot local proxy")
            proxy.add_middleware(native_proxy.ToolCallFilterMiddleware())
            self.client = Client(proxy)
            await self.client.__aenter__()
            listed = await self.client.list_tools()
            self.tool_schemas = {tool.name: tool.inputSchema for tool in listed}
        return self

    async def __aexit__(self, *exc):
        if self.client is not None:
            await self.client.__aexit__(*exc)

    async def invoke(self, call: Call, canonical: dict) -> dict:
        raw = {k: self.world.last_result if v == "$last" else v for k, v in call.args.items()}
        wire = canonical if self.path == "callable_mcp_canonicalized" else raw
        before_effects = len(self.world.effects)
        before_evaluations = len(self.bridge.evaluations)
        before_state = self.bridge.state()
        self.bridge.current = call
        error = None
        start = time.perf_counter_ns()
        try:
            if self.client is not None:
                # Native middleware prints context; retain it in the trace rather
                # than polluting worker JSON or discarding diagnostic evidence.
                captured = io.StringIO()
                with redirect_stdout(captured), redirect_stderr(io.StringIO()):
                    result = await self.client.call_tool(call.tool, wire, raise_on_error=False)
                error = " | ".join(getattr(c, "text", "") for c in result.content) if result.is_error else None
                middleware_output = captured.getvalue()
            else:
                middleware_output = ""
                try:
                    if self.path == "callable_wrapped":
                        self.functions[call.tool](**raw)
                    else:
                        self.bridge.module.check_tool_call(call.tool, raw)
                        self.world.functions[call.tool](**raw)
                except self.bridge.module.ValidationError as rejected:
                    error = str(rejected)
            elapsed = time.perf_counter_ns() - start
            effects = self.world.effects[before_effects:]
            evaluations = self.bridge.evaluations[before_evaluations:]
            if error:
                if effects or not any(not e["allowed"] for e in evaluations):
                    raise RuntimeError(f"Unexpected framework error, not a policy denial: {error}")
            elif not effects:
                raise RuntimeError("Successful tool call created no observable effect")
            if effects:
                self.bridge.commit(call, effects)
            return {"raw_args": raw, "wire_args": wire, "canonical_args": canonical,
                    "allowed": not error, "error": error, "effects": effects,
                    "predicate_evaluations": evaluations, "state_before": before_state,
                    "state_after": self.bridge.state(), "path_ns": elapsed,
                    "middleware_output": middleware_output}
        finally:
            self.bridge.current = None


def permitted_default(world: MockWorld):
    def send_external(body: str = "public-note", recipient: str = world.case.recipient) -> str:
        """Record a mock send with an explicitly permitted backend default."""
        return world.send_external(body, recipient)
    world.functions["send_external"] = send_external


async def run_case(case: Case, path: str, allow_default: bool = False) -> dict:
    world = MockWorld(case)
    if allow_default:
        permitted_default(world)
    apc = APC(case, world)
    oracle = Oracle(case)
    events = []
    for call in case.prelude:
        canonical = world.canonical(call)
        reasons = oracle.decide(call, canonical, "prelude")
        decision = apc.authorize(call, canonical)
        if reasons or not decision.allowed:
            raise RuntimeError("Invalid authorized prefix in the integration experiment")
        effects = world.execute(call, canonical)
        oracle.observe(call, effects)
        events.append({"phase": "prelude", "proposed": asdict(call), "canonical_args": canonical,
                       "oracle_reasons": reasons, "allowed": decision.allowed, "effects": effects,
                       "native_evidence": decision.evidence, "unauthorized_effect": False, "false_denial": False})
    apc.handoff()
    bridge = CallableBridge(apc)
    handoff = bridge.handoff_record()
    async with PathRunner(world, bridge, path) as runner:
        schemas = getattr(runner, "tool_schemas", {})
        for call in case.attempts:
            canonical = world.canonical(call)
            reasons = oracle.decide(call, canonical, "downstream")
            event = await runner.invoke(call, canonical)
            if event["effects"]:
                oracle.observe(call, event["effects"])
            event.update(phase="downstream", proposed=asdict(call), oracle_reasons=reasons,
                         unauthorized_effect=bool(reasons and event["effects"]),
                         false_denial=not reasons and not event["allowed"])
            events.append(event)
    return {"case": case.to_dict(), "path": path, "allow_default": allow_default,
            "handoff": handoff, "tool_schemas": schemas, "events": events, "final_state": bridge.state()}


def signature(run):
    return (any(e["unauthorized_effect"] for e in run["events"]),
            any(e["false_denial"] for e in run["events"]),
            any(f.get("contains_confidential_marker", False) for e in run["events"] for f in e["effects"]))


def semantic(runs):
    return [{"path": r["path"], "id": r["case"]["id"], "allow_default": r["allow_default"],
             "events": [[e["allowed"], e["oracle_reasons"], e["effects"]] for e in r["events"]]} for r in runs]


def summarize(runs):
    result = {}
    for path in PATHS:
        rows = [r for r in runs if r["path"] == path]
        attacks = [r for r in rows if r["case"]["kind"] == "attack"]
        benign = [r for r in rows if r["case"]["kind"] == "benign"]
        result[path] = {"runs": len(rows), "attack_cases": len(attacks), "benign_cases": len(benign),
                        "unauthorized_attack_cases": sum(signature(r)[0] for r in attacks),
                        "benign_false_denial_cases": sum(signature(r)[1] for r in benign),
                        "marker_sends": sum(f.get("contains_confidential_marker", False)
                                            for r in rows for e in r["events"] for f in e["effects"]),
                        "unsafe_templates": sorted({r["case"]["template"] for r in rows if signature(r)[0]})}
    return result


async def reduce_failure(run):
    case = Case.from_dict(run["case"])
    original = case.id
    wanted = signature(run)
    def violations(row):
        return [e["oracle_reasons"] for e in row["events"] if e["unauthorized_effect"]]
    checks = 0
    for call in tuple(case.prelude):
        candidate = replace(case, prelude=tuple(c for c in case.prelude if c != call))
        trial = await run_case(candidate, run["path"], run["allow_default"])
        checks += 1
        if signature(trial) == wanted and violations(trial) == violations(run):
            case, run = candidate, trial
    # Reduce arguments, retaining exactly the observed recipient violation or leak.
    for index in range(len(case.attempts)):
        for key in tuple(case.attempts[index].args):
            calls = list(case.attempts)
            args = dict(calls[index].args)
            args.pop(key)
            calls[index] = replace(calls[index], args=args)
            candidate = replace(case, attempts=tuple(calls))
            try:
                trial = await run_case(candidate, run["path"], run["allow_default"])
            except TypeError:
                continue  # A required backend argument cannot be removed.
            checks += 1
            if signature(trial) == wanted and violations(trial) == violations(run):
                case, run = candidate, trial
    replay = await run_case(case, run["path"], run["allow_default"])
    if semantic([run]) != semantic([replay]):
        raise RuntimeError("Reduced counterexample did not reproduce")
    return {"original_case": original, "path": run["path"], "signature": wanted, "checks": checks,
            "classification": "native_raw_argument_default_gap_pending_homogeneous_control",
            "reduced_run": replay}


async def homogeneous_controls():
    """No APC import/use in enforcement: same native MCP and finite recipient policy."""
    from fastmcp import Client, FastMCP
    from fastmcp.server.proxy import ProxyClient
    load_native()
    with redirect_stderr(io.StringIO()):
        module = import_module("secagent.mcp_proxy")
    secagent = import_module("secagent.tool")
    rows = []
    for mode in ("mcp", "mcp_canonicalized", "wrapped"):
        for name, args in (("permitted", {"recipient": "reviewer0@example.test"}),
                           ("forbidden", {"recipient": "attacker@example.test"}), ("omitted", {})):
            case = build_cases()[0]
            world = MockWorld(case)
            policy = {"send_external": [(100, 0, {"recipient": {"enum": [case.recipient]}}, 0)]}
            with redirect_stderr(io.StringIO()):
                secagent.update_security_policy(policy)
            canonical = world.canonical(Call("send_external", args))
            error = None
            if mode == "wrapped":
                wrapped = secagent.secure_tool_wrapper(world.send_external)
                try:
                    wrapped(**args)
                except Exception as rejected:
                    from jsonschema.exceptions import ValidationError as SchemaError
                    if not isinstance(rejected, (secagent.ValidationError, SchemaError)):
                        raise
                    error = str(rejected)
            else:
                backend = FastMCP("homogeneous mock backend")
                backend.tool(name="send_external")(world.send_external)
                proxy = FastMCP.as_proxy(ProxyClient(backend), name="homogeneous local proxy")
                proxy.add_middleware(module.ToolCallFilterMiddleware())
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    async with Client(proxy) as client:
                        result = await client.call_tool("send_external", canonical if mode.endswith("canonicalized") else args,
                                                        raise_on_error=False)
                if result.is_error:
                    error = " | ".join(getattr(c, "text", "") for c in result.content)
            if bool(world.effects) == bool(error):
                raise RuntimeError("Homogeneous control execution/error accounting mismatch")
            rows.append({"mode": mode, "case": name, "raw_args": args, "canonical_args": canonical,
                         "allowed": not error, "error": error, "effects": world.effects,
                         "unauthorized_effect": any(f["recipient"] != case.recipient for f in world.effects),
                         "enforcement": "native Progent only; no APC"})
    return rows


def focused_cases():
    cases = {c.template: c for c in build_cases() if c.variant == 0}
    rows = []
    # Permit the backend recipient default to isolate omitted dynamic predicates.
    for template in ("expired_grant", "revoked_grant", "history_loss", "budget_reset", "current_grant"):
        case = cases[template]
        cost = 30 if template == "budget_reset" else 1
        attempts = (Call("send_external", {}, cost=cost),)
        rows.append(replace(case, id=f"optional-empty-{template}", template=f"optional-empty-{template}",
                            attempts=attempts))
    return rows


def percentiles(samples):
    ordered = sorted(samples)
    return {"samples": len(samples), "mean_us": statistics.mean(samples) / 1000,
            **{f"p{p}_us": ordered[min(len(ordered)-1, int((len(ordered)-1)*p/100))] / 1000 for p in (50, 95, 99)}}


async def latency(warmup: int, samples: int):
    rows = []
    for path in PATHS:
        case = next(c for c in build_cases() if c.template == "permitted_default" and c.variant == 0)
        world = MockWorld(case)
        apc = APC(case, world)
        apc.handoff()
        bridge = CallableBridge(apc)
        call = replace(case.attempts[0], cost=0)
        raw, canonical = call.args, world.canonical(call)
        times = []
        async with PathRunner(world, bridge, path) as runner:
            for index in range(warmup + samples):
                # Reuse a fixed empty history: no state-growth cost or per-call
                # logging in these narrow steady-state microbenchmarks.
                bridge.history.clear()
                bridge.evaluations.clear()
                world.effects.clear()
                bridge.current = call
                start = time.perf_counter_ns()
                if runner.client is not None:
                    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                        result = await runner.client.call_tool(call.tool, canonical if path.endswith("canonicalized") else raw,
                                                               raise_on_error=False)
                    if result.is_error or not world.effects:
                        raise RuntimeError("Unexpected MCP latency probe rejection")
                    bridge.commit(call, world.effects)
                else:
                    # Authorization only, using wrapper-equivalent native default
                    # binding for the wrapped path; no tool execution or commit.
                    bridge.module.check_tool_call(call.tool, canonical if path == "callable_wrapped" else raw)
                elapsed = time.perf_counter_ns() - start
                bridge.current = None
                if index >= warmup:
                    times.append(elapsed)
        rows.append({"path": path, "warmup": warmup, "measurement": "MCP round trip + mock effect + bridge commit"
                     if path.startswith("callable_mcp") else "native checker + callable predicates; prebound args; no execution",
                     **percentiles(times)})
    return rows


def write_json(path: Path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, values):
    path.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in values), encoding="utf-8")


def report(output, metrics, controls, diagnostics, timings):
    lines = ["# Callable policies and native MCP integration: observed results", "",
             "This follow-up tests the pinned author code with stronger Progent callable policies.", "",
             "| Path | Unauthorized attack cases / 40 | Benign false denials / 40 | Marker sends |",
             "|---|---:|---:|---:|"]
    for path, values in metrics.items():
        lines.append(f"| {path} | {values['unauthorized_attack_cases']} | {values['benign_false_denial_cases']} | {values['marker_sends']} |")
    lines.extend(["", "## Interpretation", "",
                  "Callable predicates with default expansion preserve all obligations tested by this matrix if the wrapped and canonicalized rows are zero. Static-profile failures from v1 do not demonstrate an inherent Progent representation limit.", "",
                  "The bridge is custom trusted infrastructure. It copies the verified native envelope, runtime state, and separate recipient policy; native Progent evaluates its predicates. This is not a general APC policy compiler or a native cross-domain handoff protocol.", "",
                  "## Progent-only control", "", "| Path | Input | Actual unauthorized effect | Admitted |", "|---|---|---:|---:|"])
    for row in controls:
        lines.append(f"| {row['mode']} | {row['case']} | {int(row['unauthorized_effect'])} | {row['allowed']} |")
    same_engine = any(r["mode"] == "mcp" and r["case"] == "omitted" and r["unauthorized_effect"] for r in controls)
    lines.extend(["", "The native raw checker only visits constrained arguments present in the request. The native MCP middleware calls it before the backend applies optional defaults. The native function wrapper applies defaults first.", "",
                  "The omitted-recipient failure also occurs with Progent alone." if same_engine else "The homogeneous control did not establish the same failure; further triage is required.",
                  "Thus the observed raw MCP gap is an integration issue candidate, not evidence of a uniquely heterogeneous APC-to-Progent failure. It uses an initialized policy and unmodified middleware; its deployment frequency and prior reporting remain unestablished.", "",
                  "The optional parameters and defaults belong to our synthetic backend. We did not establish omission behavior in the original GitHub-target sample tools, which may require their constrained parameters. Canonicalization is a controlled mitigation using trusted actual backend signatures; remote schemas alone need not capture every backend default or transformation.", "",
                  "## Exploratory all-optional-argument controls", "",
                  "These 20 diagnostics use a permitted recipient default to isolate omitted dynamic guards; they are outside the 80-case denominator.", "",
                  "| Path | Case | Unauthorized effect | False denial |", "|---|---|---:|---:|"])
    for row in diagnostics:
        sig = signature(row)
        lines.append(f"| {row['path']} | {row['case']['template']} | {int(sig[0])} | {int(sig[1])} |")
    lines.extend(["", "## Local latency", "",
                  "Authorization and MCP round-trip measurements have different boundaries; do not compare them as interchangeable enforcement overhead. The warmed microbenchmark resets history between repetitions; it does not model growing long-lived tasks.", "",
                  "| Path | Measurement | p50 us | p99 us | Samples |", "|---|---|---:|---:|---:|"])
    for row in timings:
        lines.append(f"| {row['path']} | {row['measurement']} | {row['p50_us']:.2f} | {row['p99_us']:.2f} | {row['samples']} |")
    lines.extend(["", "## Research decision", "",
                  "The original heterogeneous-composition publication gate remains unmet. The faithful bounded bridge is feasible. The realistic MCP default gap deserves a narrow reproducibility/engineering note, but a handoff-specific failure or justified compatibility limit needs additional evidence.", "",
                  "All effects are in-memory mock records; no agent models, paid APIs, real sends, external server connections, or network authentication were exercised. Foreign caller context/freshness cases remain trusted conformance interventions. Five parameter variants per template are not independent deployment samples. See the frozen protocol and provenance in this directory.", ""])
    (output / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


async def experiment(output, warmup, samples):
    # Windows creates an internal socketpair while constructing its event loop.
    # Disable connections only after that trusted runtime setup is complete.
    block_network()
    cases = build_cases()
    traces = []
    for path in PATHS:
        print(f"Integration matrix: {path} ({len(cases)} cases)", flush=True)
        for case in cases:
            traces.append(await run_case(case, path))
    write_jsonl(output / "traces.jsonl", traces)
    metrics = summarize(traces)
    write_json(output / "metrics.json", metrics)
    reduced = []
    for run in traces:
        if any(signature(run)[:2]):
            reduced.append(await reduce_failure(run))
    controls = await homogeneous_controls()
    write_json(output / "homogeneous_controls.json", controls)
    same_engine = any(r["mode"] == "mcp" and r["case"] == "omitted" and r["unauthorized_effect"] for r in controls)
    for row in reduced:
        if same_engine:
            row["classification"] = "native_MCP_raw_argument_gap_also_present_without_APC"
    write_jsonl(output / "counterexamples.jsonl", reduced)
    diagnostics = [await run_case(case, path, allow_default=True) for path in PATHS for case in focused_cases()]
    write_jsonl(output / "optional_argument_diagnostics.jsonl", diagnostics)
    timings = await latency(warmup, samples)
    write_json(output / "latency.json", timings)
    report(output, metrics, controls, diagnostics, timings)
    return {"runs": len(traces), "disagreements_reduced": len(reduced), "homogeneous_controls": len(controls),
            "diagnostic_runs": len(diagnostics), "outcome_sha256": hashlib.sha256(json.dumps(semantic(traces), sort_keys=True).encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--warmup", type=int, default=100)
    parser.add_argument("--samples", type=int, default=1000)
    args = parser.parse_args()
    if args.warmup < 0 or args.samples < 1:
        parser.error("warmup >= 0 and samples >= 1 required")
    if version("fastmcp") != "2.13.0":
        raise RuntimeError("Use the frozen FastMCP 2.13.0 integration environment")
    source = provenance()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    snapshot = output / "harness_sources"
    snapshot.mkdir()
    hashes = {}
    files = list((ROOT / "seam_pilot").glob("*.py")) + list((ROOT / "tests").glob("*.py"))
    files += [ROOT / n for n in ("pins.json", "requirements-integration.lock", "PROTOCOL_INTEGRATION.md")]
    for file in files:
        relative = file.relative_to(ROOT)
        destination = snapshot / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(file.read_bytes())
        hashes[relative.as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
    cases = [c.to_dict() for c in build_cases()]
    write_json(output / "cases.json", cases)
    manifest = {"status": "running", "started_utc": datetime.now(timezone.utc).isoformat(),
                "python": sys.version, "platform": platform.platform(), "dependencies":
                {d.metadata["Name"]: d.version for d in distributions()}, **source, "harness_sha256": hashes,
                "dataset_sha256": hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest(),
                "paths": PATHS, "warmup": args.warmup, "samples": args.samples,
                "network": "socket connections blocked; in-memory MCP transports only"}
    write_json(output / "manifest.json", manifest)
    try:
        observations = asyncio.run(experiment(output, args.warmup, args.samples))
    except BaseException as error:
        manifest.update(status="failed", error=repr(error))
        write_json(output / "manifest.json", manifest)
        raise
    manifest.update(observations, status="complete", completed_utc=datetime.now(timezone.utc).isoformat())
    write_json(output / "manifest.json", manifest)
    print(f"Completed {observations['runs']} integration runs: {output / 'REPORT.md'}", flush=True)


if __name__ == "__main__":
    main()
