"""Thin calls into pinned author implementations; no reimplementation of their checks."""
from __future__ import annotations

import contextlib
import hashlib
import importlib
import io
import json
import logging
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
_loaded = False


def provenance() -> dict:
    pins = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
    hashes = {}
    for name, pin in pins["repositories"].items():
        repo = ROOT / pin["path"]
        actual = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
        if actual != pin["commit"]:
            raise RuntimeError(f"{name} pin mismatch: {actual}")
        for diff in ([], ["--cached"]):
            subprocess.run(["git", "-C", str(repo), "diff", "--exit-code", *diff], check=True, capture_output=True)
        extra = subprocess.check_output(["git", "-C", str(repo), "ls-files", "--others", "--exclude-standard", pin["package"]], text=True)
        if extra.strip():
            raise RuntimeError(f"untracked files in native package {name}: {extra}")
        for file in sorted((repo / pin["package"]).rglob("*.py")):
            hashes[str(file.relative_to(ROOT)).replace("\\", "/")] = hashlib.sha256(file.read_bytes()).hexdigest()
    return {"pins": pins, "source_sha256": hashes}


def block_network() -> None:
    def blocked(*args, **kwargs):
        raise RuntimeError("Network access is disabled during the pilot")
    socket.socket.connect = blocked
    socket.socket.connect_ex = blocked
    socket.create_connection = blocked


def load_native() -> None:
    global _loaded
    if _loaded:
        return
    os.environ.update(SECAGENT_GENERATE="False", SECAGENT_UPDATE="False", ENABLE_SECAGENT="True")
    pins = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
    for pin in pins["repositories"].values():
        sys.path.insert(0, str(ROOT / pin["path"]))
    with contextlib.redirect_stderr(io.StringIO()):
        importlib.import_module("apc.pdp")
        importlib.import_module("secagent.tool")
    logging.getLogger("apc.security").setLevel(logging.CRITICAL)
    _loaded = True


class APC:
    def __init__(self, case, world):
        load_native()
        from apc.approval import ApprovalStore
        from apc.budget import BudgetState
        from apc.calibrate import ImpactWeights
        from apc.compose import CompositionChecker
        from apc.core import Scope, Principal, ExecutionRole, AuthorizationEnvelope, DelegationBudgetSpec
        from apc.intent import IntentChecker, IntentSpec
        from apc.parameters import ParameterPolicy, ParameterValidator, AllowlistRule
        from apc.pdp import PolicyDecisionPoint, EvidenceSink, RevocationRegistry
        self.case = case
        self.world = world
        # Public synthetic test key, used only in this in-memory pilot.
        self.key = b"synthetic-pilot-key-not-a-production-credential"
        restrictions = frozenset({("read_confidential", "send_external")}) if case.composition_required else frozenset()
        scope = Scope(frozenset(case.resources), frozenset(world.functions), frozenset({"public", "internal", "confidential"}), restrictions)
        self.root_scope = scope
        human = Principal("human:root", ExecutionRole.AS_USER, scope)
        agent = Principal("agent:a", ExecutionRole.ON_BEHALF_OF, scope)
        spec = DelegationBudgetSpec(8, 1.0, 1000, "confidential", True, case.cost_limit)
        envelope = AuthorizationEnvelope("root-envelope", "root-task", human, scope, spec,
                                         expires_at=time.time() + (7200 if case.status == "renewed" else 3600), policy_version="pilot-v1")
        envelope.sign(self.key)
        self.envelope = envelope.narrow(agent, self.key)
        self.budget = BudgetState(spec)
        self.composition = CompositionChecker(restrictions)
        self.sink = EvidenceSink()
        self.revocations = RevocationRegistry()
        policy = ParameterPolicy()
        policy.add_rule("send_external", "recipient", AllowlistRule(frozenset({case.recipient})))
        self.validator = ParameterValidator(policy)
        self.intent = IntentChecker(IntentSpec("Execute the bounded pilot task", permitted_resource_patterns=case.resources,
                                              permitted_action_sequences=tuple(world.functions)))
        self.pdp = PolicyDecisionPoint(self.key, ImpactWeights(.3, .3, .4), 1.0, ApprovalStore(), self.sink,
                                      revocation_registry=self.revocations, parameter_validator=self.validator)

    def handoff(self, reset=False, fresh_pdp=False):
        from apc.budget import BudgetState
        from apc.calibrate import ImpactWeights
        from apc.compose import CompositionChecker
        from apc.core import Scope, Principal, ExecutionRole, AuthorizationEnvelope
        from apc.approval import ApprovalStore
        from apc.pdp import PolicyDecisionPoint
        c = self.case
        role = Scope(frozenset(c.role_resources), self.root_scope.actions, self.root_scope.data_classifications)
        self.envelope = self.envelope.narrow(Principal("agent:b", ExecutionRole.ON_BEHALF_OF, role), self.key)
        if c.status == "expired":
            # A trusted issuer constructs an already expired grant; no signed-field tampering.
            old = self.envelope
            self.envelope = AuthorizationEnvelope(old.envelope_id, old.task_session_id, old.originating_principal,
                                                 old.effective_scope, old.budget_spec, chain=list(old.chain),
                                                 created_at=1.0, expires_at=2.0, policy_version=old.policy_version)
            self.envelope.sign(self.key)
        if c.status == "revoked":
            self.revocations.revoke(self.envelope.envelope_id, "pilot revokes the actual delegated envelope")
        if reset:
            self.budget = BudgetState(self.envelope.budget_spec)
            self.composition = CompositionChecker(self.envelope.effective_scope.composition_restrictions)
        if fresh_pdp:
            self.pdp = PolicyDecisionPoint(self.key, ImpactWeights(.3, .3, .4), 1.0, ApprovalStore(), self.sink,
                                          revocation_registry=self.revocations, parameter_validator=self.validator)

    def authorize(self, call, args):
        from apc.pdp import ProposedAction
        from .model import Decision
        resource = args.get("resource", "mail:external")
        sensitivity = "confidential" if call.tool == "read_confidential" else "public"
        proposal = ProposedAction(call.tool, resource, args, call.actor, call.session, call.policy_version,
                                  sensitivity_class=sensitivity, compute_cost=call.cost)
        before = len(self.sink.packages)
        result = self.pdp.evaluate(proposal, self.envelope, self.budget, self.composition, intent_checker=self.intent)
        return Decision(result.admitted, list(result.denial_reasons), self.sink.packages[before:],
                        [p.principal_id for p in self.envelope.chain], ["APC"])


class Progent:
    """Explicitly static JSON-schema policy profile; general callable policies are not tested."""

    def __init__(self, case, resources):
        load_native()
        self.case = case
        self.resources = tuple(sorted(resources))
        self.module = importlib.import_module("secagent.tool")
        policy = {}
        for tool in ("read_confidential", "read_public", "save_internal", "send_external"):
            if tool == "send_external":
                if "mail:external" not in resources:
                    continue
                args = {"recipient": {"type": "string", "enum": [case.recipient]}}
            else:
                args = {"resource": {"type": "string", "enum": list(self.resources)}}
            policy[tool] = [(100, 0, args, 0)]
        with contextlib.redirect_stderr(io.StringIO()):
            self.module.update_security_policy(policy)
        if self.module.security_policy is None:
            raise RuntimeError("Progent policy initialization failed")

    def authorize(self, call, args):
        from .model import Decision
        try:
            self.module.check_tool_call(call.tool, args)
        except self.module.ValidationError as error:
            return Decision(False, [str(error)], checked_by=["Progent"])
        return Decision(True, checked_by=["Progent"])
