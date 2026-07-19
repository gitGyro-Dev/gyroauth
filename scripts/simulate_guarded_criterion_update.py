#!/usr/bin/env python3
"""Deterministic PoC for guarded authentication-criterion updates.

Compares:
- Model U: unconstrained direct candidate adoption
- Model G: guarded candidate adoption with ACCEPT/DEFER/FREEZE/REVIEW/ROLLBACK

No external dependencies are required.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


@dataclass
class Criterion:
    mu: float = 0.20
    width: float = 0.12
    provenance_requirement: float = 0.70
    challenge_requirement: float = 0.70
    rollback_integrity: int = 1


@dataclass
class RuntimeState:
    criterion_state: str = "STABLE"
    frozen: bool = False
    consecutive_suspicious: int = 0
    cumulative_width_expansion: float = 0.0
    previous_deviation: float = 0.0


CONFIG: Dict[str, float] = {
    "eta_mu": 0.20,
    "eta_width": 0.50,
    "theta_cross": 0.65,
    "theta_source": 0.60,
    "max_center_shift": 0.08,
    "max_width_change": 0.05,
    "max_cumulative_width_expansion": 0.10,
    "max_discrimination_loss": 0.06,
    "suspicious_freeze_count": 2,
    "attack_reference": 0.62,
    "theta_fail": 0.28,
    "theta_cont_fail": 0.25,
    "theta_reauth": 0.55,
    "theta_reconverge": 1.10,
}


def candidate_update(criterion: Criterion, observation: Dict[str, Any]) -> Criterion:
    y = float(observation["y"])
    deviation = abs(y - criterion.mu)
    candidate = deepcopy(criterion)
    candidate.mu = clamp(
        criterion.mu + CONFIG["eta_mu"] * (y - criterion.mu)
    )
    candidate.width = clamp(
        criterion.width
        + CONFIG["eta_width"] * max(0.0, deviation - criterion.width)
    )

    # This PoC permits trusted evidence to strengthen a requirement, but never
    # weakens provenance or challenge requirements automatically.
    if float(observation.get("challenge", 0.0)) >= criterion.challenge_requirement:
        candidate.challenge_requirement = max(
            criterion.challenge_requirement,
            min(0.90, float(observation["challenge"]) * 0.90),
        )
    return candidate


def subject_values(
    criterion: Criterion,
    observation: Dict[str, Any],
    previous_deviation: float,
) -> Dict[str, float]:
    deviation = abs(float(observation["y"]) - criterion.mu)
    deviation_norm = deviation / max(criterion.width, 1e-9)
    direction = deviation - previous_deviation
    recovery = 1.0 if direction < 0 else 0.0
    cross = float(observation["cross"])
    challenge = float(observation["challenge"])
    privilege = float(observation["privilege"])

    trajectory_continuity = clamp(
        1.0
        - 0.35 * deviation_norm
        - 0.25 * privilege
        + 0.25 * cross
        + 0.10 * recovery
    )
    stability = clamp(
        0.50 * trajectory_continuity
        + 0.25 * cross
        + 0.20 * challenge
        - 0.20 * deviation_norm
    )
    return {
        "delta": round(deviation, 6),
        "delta_norm": round(deviation_norm, 6),
        "direction": round(direction, 6),
        "recovery": recovery,
        "trajectory_continuity": round(trajectory_continuity, 6),
        "stability": round(stability, 6),
    }


def auth_decision(subject: Dict[str, float], observation: Dict[str, Any]) -> str:
    if (
        subject["stability"] < CONFIG["theta_fail"]
        and subject["trajectory_continuity"] < CONFIG["theta_cont_fail"]
    ):
        return "AUTH_FAIL"
    if bool(observation.get("challenge_required", False)) and float(
        observation["challenge"]
    ) < 0.70:
        return "REAUTH_REQUIRED"
    if subject["stability"] < CONFIG["theta_reauth"]:
        return "REAUTH_REQUIRED"
    if (
        subject["delta_norm"] > CONFIG["theta_reconverge"]
        or subject["direction"] > 0.0
    ):
        return "RECONVERGING"
    return "AUTH_STABLE"


def discrimination_distance(criterion: Criterion) -> float:
    return max(
        0.0,
        abs(CONFIG["attack_reference"] - criterion.mu) - criterion.width,
    )


def guard_vector(
    current: Criterion,
    candidate: Criterion,
    observation: Dict[str, Any],
    runtime: RuntimeState,
) -> Tuple[Dict[str, str], Dict[str, float]]:
    center_shift = abs(candidate.mu - current.mu)
    width_change = candidate.width - current.width
    discrimination_before = discrimination_distance(current)
    discrimination_after = discrimination_distance(candidate)
    discrimination_loss = discrimination_before - discrimination_after

    provenance = float(observation["provenance"])
    cross = float(observation["cross"])
    challenge = float(observation["challenge"])
    source_integrity = float(observation["source_integrity"])
    context_explained = bool(observation.get("context_explained", False))
    challenge_required = bool(observation.get("challenge_required", False))

    guards = {
        "provenance": "PASS"
        if provenance >= current.provenance_requirement
        else "FAIL",
        "cross_evidence": "PASS"
        if cross >= CONFIG["theta_cross"]
        else ("WARN" if cross >= 0.45 else "FAIL"),
        "challenge": "PASS"
        if (not challenge_required or challenge >= current.challenge_requirement)
        else "FAIL",
        "magnitude": "PASS"
        if (
            center_shift <= CONFIG["max_center_shift"]
            and width_change <= CONFIG["max_width_change"]
        )
        else "FAIL",
        "direction": "PASS" if context_explained else "WARN",
        "discrimination": "PASS"
        if discrimination_loss <= CONFIG["max_discrimination_loss"]
        else "FAIL",
        "rollback": "PASS" if current.rollback_integrity == 1 else "FAIL",
        "source": "PASS"
        if source_integrity >= CONFIG["theta_source"]
        else "FAIL",
    }

    projected_cumulative_expansion = (
        runtime.cumulative_width_expansion + max(0.0, width_change)
    )
    guards["rate"] = (
        "PASS"
        if projected_cumulative_expansion
        <= CONFIG["max_cumulative_width_expansion"]
        else "FAIL"
    )

    metrics = {
        "center_shift": round(center_shift, 6),
        "width_change": round(width_change, 6),
        "discrimination_before": round(discrimination_before, 6),
        "discrimination_after": round(discrimination_after, 6),
        "discrimination_loss": round(discrimination_loss, 6),
        "projected_cumulative_width_expansion": round(
            projected_cumulative_expansion, 6
        ),
    }
    return guards, metrics


def criterion_integrity_score(guards: Dict[str, str]) -> float:
    mapping = {"PASS": 1.0, "WARN": 0.5, "FAIL": 0.0}
    return round(
        sum(mapping[value] for value in guards.values()) / len(guards),
        6,
    )


def select_criterion_response(
    guards: Dict[str, str],
    observation: Dict[str, Any],
    runtime: RuntimeState,
) -> str:
    critical = {
        "provenance",
        "challenge",
        "discrimination",
        "rollback",
        "source",
    }
    critical_fail = any(guards[name] == "FAIL" for name in critical)
    repeated_suspicious = (
        runtime.consecutive_suspicious
        >= int(CONFIG["suspicious_freeze_count"])
    )
    cumulative_excess = guards["rate"] == "FAIL"

    if observation.get("confirmed_contamination", False):
        return "ROLLBACK" if guards["rollback"] == "PASS" else "REVIEW"
    if runtime.frozen:
        return "FREEZE"
    if guards["source"] == "FAIL":
        return "FREEZE"
    if repeated_suspicious and (
        critical_fail
        or cumulative_excess
        or guards["direction"] != "PASS"
        or guards["cross_evidence"] != "PASS"
    ):
        return "FREEZE"
    if critical_fail:
        if (
            guards["challenge"] == "FAIL"
            and not observation.get("attack_suspected", False)
        ):
            return "DEFER"
        return "REVIEW"
    if guards["magnitude"] == "FAIL" or cumulative_excess:
        return "FREEZE"
    if guards["cross_evidence"] == "WARN" or guards["direction"] == "WARN":
        return "DEFER"
    return "ACCEPT"


def transition_state(
    current_state: str,
    response: str,
    observation: Dict[str, Any],
) -> str:
    transitions = {
        "ACCEPT": "STABLE"
        if observation.get("adaptation_complete", False)
        else "ADAPTING",
        "DEFER": "UNCERTAIN",
        "FREEZE": "FROZEN",
        "REVIEW": "UNDER_REVIEW",
        "ROLLBACK": "ROLLED_BACK",
    }
    return transitions.get(response, current_state)


def run_model(scenario: Dict[str, Any], guarded: bool) -> Dict[str, Any]:
    initial = Criterion(**scenario["initial_criterion"])
    criterion = deepcopy(initial)
    rollback_point = deepcopy(initial)
    runtime = RuntimeState()
    stages: List[Dict[str, Any]] = []

    for index, observation in enumerate(scenario["observations"], start=1):
        subject = subject_values(
            criterion,
            observation,
            runtime.previous_deviation,
        )
        decision = auth_decision(subject, observation)
        candidate = candidate_update(criterion, observation)
        guards, metrics = guard_vector(
            criterion,
            candidate,
            observation,
            runtime,
        )

        suspicious = (
            bool(observation.get("attack_suspected", False))
            or guards["cross_evidence"] != "PASS"
            or guards["direction"] != "PASS"
            or guards["source"] == "FAIL"
        )
        runtime.consecutive_suspicious = (
            runtime.consecutive_suspicious + 1 if suspicious else 0
        )

        if guarded:
            response = select_criterion_response(
                guards,
                observation,
                runtime,
            )
            previous_criterion = deepcopy(criterion)
            if response == "ACCEPT":
                criterion = candidate
                runtime.cumulative_width_expansion += max(
                    0.0,
                    criterion.width - previous_criterion.width,
                )
            elif response == "ROLLBACK":
                criterion = deepcopy(rollback_point)
                runtime.frozen = False
                runtime.cumulative_width_expansion = 0.0
            elif response == "FREEZE":
                runtime.frozen = True
            runtime.criterion_state = transition_state(
                runtime.criterion_state,
                response,
                observation,
            )
        else:
            response = "DIRECT_ADOPT"
            previous_criterion = deepcopy(criterion)
            criterion = candidate
            runtime.cumulative_width_expansion += max(
                0.0,
                criterion.width - previous_criterion.width,
            )
            runtime.criterion_state = "ADAPTING"

        stages.append(
            {
                "stage": index,
                "label": observation.get("label", f"stage-{index}"),
                "observation": observation,
                "subject": subject,
                "auth_decision": decision,
                "candidate": asdict(candidate),
                "guard": guards if guarded else None,
                "criterion_integrity": criterion_integrity_score(guards)
                if guarded
                else None,
                "criterion_response": response,
                "criterion_state": runtime.criterion_state,
                "effective_criterion": asdict(criterion),
                "candidate_metrics": metrics,
            }
        )
        runtime.previous_deviation = subject["delta"]

    attack_admissible = (
        abs(CONFIG["attack_reference"] - criterion.mu) <= criterion.width
    )
    return {
        "model": "G" if guarded else "U",
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "final_criterion": asdict(criterion),
        "final_criterion_state": runtime.criterion_state,
        "attack_reference": CONFIG["attack_reference"],
        "attack_reference_admissible": attack_admissible,
        "rollback_point_retained": asdict(rollback_point),
        "stages": stages,
    }


def summarize(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "model": result["model"],
        "scenario_id": result["scenario_id"],
        "final_mu": result["final_criterion"]["mu"],
        "final_width": result["final_criterion"]["width"],
        "final_state": result["final_criterion_state"],
        "attack_reference_admissible": result["attack_reference_admissible"],
        "freeze_stage": next(
            (
                stage["stage"]
                for stage in result["stages"]
                if stage["criterion_response"] == "FREEZE"
            ),
            None,
        ),
        "auth_decisions": [
            stage["auth_decision"] for stage in result["stages"]
        ],
        "criterion_responses": [
            stage["criterion_response"] for stage in result["stages"]
        ],
    }


def assertions(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {(r["scenario_id"], r["model"]): r for r in results}

    def has_response(scenario_id: str, response: str) -> bool:
        return any(
            stage["criterion_response"] == response
            for stage in by_key[(scenario_id, "G")]["stages"]
        )

    checks = [
        (
            "N1 guarded model eventually accepts supported adaptation",
            has_response("N1", "ACCEPT"),
        ),
        (
            "P1 unconstrained model makes attack reference admissible",
            by_key[("P1", "U")]["attack_reference_admissible"],
        ),
        (
            "P1 guarded model freezes criterion adaptation",
            has_response("P1", "FREEZE"),
        ),
        (
            "P1 guarded model keeps attack reference non-admissible",
            not by_key[("P1", "G")]["attack_reference_admissible"],
        ),
        (
            "C1 guarded model does not accept compromised source update",
            not has_response("C1", "ACCEPT"),
        ),
        (
            "C1 guarded model freezes or reviews",
            has_response("C1", "FREEZE") or has_response("C1", "REVIEW"),
        ),
        (
            "Auth Decision and Criterion Update Response remain separate",
            any(
                stage["auth_decision"] == "AUTH_STABLE"
                and stage["criterion_response"] == "FREEZE"
                for stage in by_key[("P1", "G")]["stages"]
            ),
        ),
    ]
    return [{"name": name, "passed": bool(passed)} for name, passed in checks]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenarios",
        default="examples/criterion_update/scenarios.json",
    )
    parser.add_argument(
        "--output",
        default="results/criterion_update_results.json",
    )
    args = parser.parse_args()

    scenario_data = json.loads(
        Path(args.scenarios).read_text(encoding="utf-8")
    )
    results: List[Dict[str, Any]] = []
    for scenario in scenario_data["scenarios"]:
        results.append(run_model(scenario, guarded=False))
        results.append(run_model(scenario, guarded=True))

    payload = {
        "config": CONFIG,
        "summaries": [summarize(result) for result in results],
        "assertions": assertions(results),
        "results": results,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(payload["summaries"], ensure_ascii=False, indent=2))
    print(json.dumps(payload["assertions"], ensure_ascii=False, indent=2))
    failed = [item for item in payload["assertions"] if not item["passed"]]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
