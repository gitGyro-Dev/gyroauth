"""
GyroAuth v2 — Stability Graph Demo

Purpose:
    Demonstrate the core GyroAuth visual story:

        AUTH_STABLE
        → small drift
        → RECONVERGING
        → recovery
        → AUTH_STABLE
        → attack
        → AUTH_FAIL

This script generates:
    1. Stability timeline graph
    2. Slice stability breakdown graph
    3. CSV demo data

Suggested location:
    scripts/demo_stability_graph.py

Run:
    python scripts/demo_stability_graph.py

Output:
    outputs/stability_timeline.png
    outputs/slice_breakdown.png
    outputs/demo_stability_data.csv
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import csv
import matplotlib.pyplot as plt


@dataclass
class StabilityPoint:
    t: int
    stability: float
    auth_state: str
    event: str


def build_demo_sequence() -> List[StabilityPoint]:
    """
    Builds a deterministic demo sequence.

    This is not a production model.
    It is a visual PoC dataset for explaining GyroAuth behavior.
    """

    return [
        StabilityPoint(0, 0.94, "AUTH_STABLE", "session_start"),
        StabilityPoint(1, 0.93, "AUTH_STABLE", "normal_observation"),
        StabilityPoint(2, 0.91, "AUTH_STABLE", "normal_behavior"),
        StabilityPoint(3, 0.88, "AUTH_STABLE", "small_drift"),
        StabilityPoint(4, 0.78, "RECONVERGING", "behavior_drift_detected"),
        StabilityPoint(5, 0.73, "RECONVERGING", "additional_observation_required"),
        StabilityPoint(6, 0.81, "RECONVERGING", "reconvergence_started"),
        StabilityPoint(7, 0.89, "AUTH_STABLE", "stability_recovered"),
        StabilityPoint(8, 0.92, "AUTH_STABLE", "normal_session_restored"),
        StabilityPoint(9, 0.69, "RECONVERGING", "network_anomaly"),
        StabilityPoint(10, 0.45, "AUTH_FAIL", "device_behavior_mismatch"),
        StabilityPoint(11, 0.22, "AUTH_FAIL", "attack_detected"),
    ]


def write_csv(points: List[StabilityPoint], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "stability", "auth_state", "event"])

        for p in points:
            writer.writerow([p.t, p.stability, p.auth_state, p.event])


def plot_stability_timeline(points: List[StabilityPoint], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    times = [p.t for p in points]
    stability = [p.stability for p in points]

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(times, stability, marker="o", linewidth=2)

    # Threshold lines
    stable_threshold = 0.85
    recover_threshold = 0.70

    ax.axhline(stable_threshold, linestyle="--", linewidth=1)
    ax.axhline(recover_threshold, linestyle="--", linewidth=1)

    ax.text(times[0], stable_threshold + 0.015, "AUTH_STABLE threshold", fontsize=9)
    ax.text(times[0], recover_threshold + 0.015, "RECONVERGING threshold", fontsize=9)

    # Annotate significant events
    for p in points:
        if p.event in {
            "small_drift",
            "behavior_drift_detected",
            "stability_recovered",
            "network_anomaly",
            "attack_detected",
        }:
            ax.annotate(
                p.event,
                xy=(p.t, p.stability),
                xytext=(p.t, min(p.stability + 0.12, 1.0)),
                arrowprops={"arrowstyle": "->"},
                fontsize=8,
                ha="center",
            )

    ax.set_title("GyroAuth v2 — Stability Timeline")
    ax.set_xlabel("Time")
    ax.set_ylabel("Stability")
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(times)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_slice_breakdown(output_path: Path) -> None:
    """
    Generates a slice stability snapshot at the moment of attack.

    The purpose is to show which slice collapsed and why the session failed.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    slices = ["Device", "Behavior", "Time", "Space", "Network", "Motion"]
    values = [0.42, 0.38, 0.88, 0.72, 0.55, 0.49]

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(slices, values)
    ax.set_title("GyroAuth v2 — Slice Stability Breakdown")
    ax.set_xlabel("Stability")
    ax.set_xlim(0.0, 1.0)
    ax.grid(True, axis="x", alpha=0.3)

    for index, value in enumerate(values):
        ax.text(value + 0.02, index, f"{value:.2f}", va="center")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    output_dir = Path("outputs")

    points = build_demo_sequence()

    write_csv(points, output_dir / "demo_stability_data.csv")
    plot_stability_timeline(points, output_dir / "stability_timeline.png")
    plot_slice_breakdown(output_dir / "slice_breakdown.png")

    print("GyroAuth v2 stability demo generated:")
    print(f"- {output_dir / 'demo_stability_data.csv'}")
    print(f"- {output_dir / 'stability_timeline.png'}")
    print(f"- {output_dir / 'slice_breakdown.png'}")


if __name__ == "__main__":
    main()
