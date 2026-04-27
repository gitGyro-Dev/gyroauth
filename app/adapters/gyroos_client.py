from __future__ import annotations

from typing import Any, Dict, List


class GyroOSClient:
    """
    Minimal GyroOS adapter.

    This class intentionally acts as a boundary.

    In v2 architecture:
        - GyroOS computes Deviation / Stability / Selection
        - GyroAuth applies policy and returns Auth Decision

    This mock implementation makes the PoC runnable now.
    Later, replace evaluate() with a real GyroOS API call.
    """

    def evaluate(self, observations: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not observations:
            return {
                "stability": 0.0,
                "slice_scores": [],
                "selection": {"selected": False},
                "events": ["no_observation"],
            }

        latest = observations[-1]
        slices = latest.get("slices", {})

        slice_scores = []
        events = []

        for name in ["device", "behavior", "time", "space", "network", "motion"]:
            raw = slices.get(name, {})

            # Demo convention:
            # each slice may optionally provide stability directly.
            # If omitted, default is stable.
            score = float(raw.get("stability", 0.90))

            # Clamp score to 0.0 - 1.0
            score = max(0.0, min(1.0, score))

            if score >= 0.85:
                status = "ok"
            elif score >= 0.70:
                status = "drift"
                events.append(f"{name}_drift")
            else:
                status = "warning"
                events.append(f"{name}_warning")

            slice_scores.append(
                {
                    "name": name,
                    "stability": score,
                    "status": status,
                }
            )

        # Session stability = average slice stability.
        # Production version should be replaced by GyroOS Stability Engine output.
        stability = sum(s["stability"] for s in slice_scores) / len(slice_scores)

        critical = [s for s in slice_scores if s["stability"] < 0.45]
        if critical:
            events.append("critical_deviation_detected")
            stability = min(stability, 0.40)

        return {
            "stability": round(stability, 4),
            "slice_scores": slice_scores,
            "selection": {"selected": stability >= 0.70},
            "events": events,
        }
