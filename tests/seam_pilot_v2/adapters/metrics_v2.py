"""Metric aggregation for the v2 matrix."""
from __future__ import annotations

from typing import Any


def case_leaked(run: dict[str, Any]) -> bool:
    return any(event["unauthorized_effect"] for event in run["events"])


def case_false_denial(run: dict[str, Any]) -> bool:
    return any(event["false_denial"] for event in run["events"])


def summarize(runs: list[dict[str, Any]], arms: tuple[str, ...]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for arm in arms:
        subset = [r for r in runs if r["arm"] == arm]
        attacks = [r for r in subset if r["case"]["kind"] == "attack"]
        benign = [r for r in subset if r["case"]["kind"] == "benign"]
        events = [e for r in subset for e in r["events"]]
        per_template: dict[str, dict[str, int]] = {}
        for run in subset:
            template = run["case"]["template"]
            block = per_template.setdefault(template, {"runs": 0, "leaked": 0, "false_denials": 0,
                                                        "unauthorized_events": 0})
            block["runs"] += 1
            block["leaked"] += int(case_leaked(run))
            block["false_denials"] += int(case_false_denial(run))
            block["unauthorized_events"] += sum(e["unauthorized_effect"] for e in run["events"])
        result[arm] = {
            "runs": len(subset),
            "attack_cases": len(attacks),
            "attack_successes": sum(case_leaked(r) for r in attacks),
            "attack_success_rate": (sum(case_leaked(r) for r in attacks) / len(attacks)) if attacks else None,
            "benign_cases": len(benign),
            "benign_false_denial_cases": sum(case_false_denial(r) for r in benign),
            "benign_false_denial_rate": (sum(case_false_denial(r) for r in benign) / len(benign)) if benign else None,
            "unauthorized_effect_events": sum(e["unauthorized_effect"] for e in events),
            "false_denial_events": sum(e["false_denial"] for e in events),
            "confidential_marker_external_effects": sum(
                effect.get("contains_confidential_marker", False) for e in events for effect in e["effects"]),
            "receipt_failures": sum(1 for r in subset for e in r["events"]
                                    if e.get("receipt_ok") is False),
            "gate_mapping_rejections": sum(
                1 for r in subset for e in r["events"]
                if (e.get("gate") or {}).get("code") == "MAPPING-REJECT"),
            "gate_proof_gaps": sum(
                1 for r in subset for e in r["events"]
                if (e.get("gate") or {}).get("code") == "PROOF-GAP"),
            "gate_allow_events": sum(
                1 for r in subset for e in r["events"] if (e.get("gate") or {}).get("admitted")),
            "events": len(events),
            "per_template": per_template,
        }
    return result


def condition_confusion(runs: list[dict[str, Any]], arm: str = "apc_tracegrant_scope_only") -> dict[str, Any]:
    """2x2 of locked `predicted_safe` against observed unauthorized effects in one arm."""
    subset = [r for r in runs if r["arm"] == arm]
    tp = fp = fn = tn = 0
    rows: list[dict[str, Any]] = []
    for run in subset:
        predicted_safe = bool(run["case"]["predicted_safe"])
        leaked = case_leaked(run)
        if not predicted_safe and leaked:
            tp += 1
        elif not predicted_safe and not leaked:
            fp += 1
        elif predicted_safe and leaked:
            fn += 1
        else:
            tn += 1
        rows.append({
            "case": run["case"]["id"],
            "template": run["case"]["template"],
            "kind": run["case"]["kind"],
            "hypothesis": run["case"]["hypothesis"],
            "predicted_safe": predicted_safe,
            "observed_leak": leaked,
            "observed_receipt_failure": any(e.get("receipt_ok") is False for e in run["events"]),
            "oracle_reasons": sorted({reason for e in run["events"] for reason in e["oracle_reasons"]}),
        })
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    return {
        "arm": arm,
        "true_positive": tp, "false_positive": fp, "false_negative": fn, "true_negative": tn,
        "precision": precision, "recall": recall,
        "rows": rows,
    }
