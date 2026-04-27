"""
GyroAuth v2 — Live Stability Graph

Reads:
    outputs/auth_history.csv

Writes:
    outputs/live_stability_timeline.png

Run:
    python scripts/live_stability_graph.py

Usage:
    1. Start FastAPI:
        uvicorn app.main:app --reload

    2. Send /observe and /authenticate requests.

    3. Run this script repeatedly to update the graph:
        python scripts/live_stability_graph.py

This is a minimal file-based realtime bridge:
    FastAPI → outputs/auth_history.csv → graph image
"""

from __future__ import annotations

from pathlib import Path
import csv

import matplotlib.pyplot as plt


HISTORY_CSV = Path("outputs/auth_history.csv")
OUTPUT_IMAGE = Path("outputs/live_stability_timeline.png")


def read_history():
    if not HISTORY_CSV.exists():
        raise FileNotFoundError(
            "outputs/auth_history.csv not found. Run FastAPI and call /authenticate first."
        )

    rows = []

    with HISTORY_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rows.append(
                {
                    "session_id": row["session_id"],
                    "timestamp": float(row["timestamp"]),
                    "stability": float(row["stability"]),
                    "auth_state": row["auth_state"],
                    "event": row["event"],
                }
            )

    return rows


def plot(rows):
    OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)

    rows = sorted(rows, key=lambda x: x["timestamp"])

    timestamps = [r["timestamp"] for r in rows]
    stability = [r["stability"] for r in rows]
    states = [r["auth_state"] for r in rows]
    events = [r["event"] for r in rows]

    # Normalize x-axis to step number for readability
    x = list(range(len(rows)))

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(x, stability, marker="o", linewidth=2)

    ax.axhline(0.85, linestyle="--", linewidth=1)
    ax.axhline(0.70, linestyle="--", linewidth=1)

    ax.text(0, 0.865, "AUTH_STABLE threshold", fontsize=9)
    ax.text(0, 0.715, "RECONVERGING threshold", fontsize=9)

    for i, (score, state, event) in enumerate(zip(stability, states, events)):
        label = state

        if "critical_deviation_detected" in event:
            label = "AUTH_FAIL\\ncritical deviation"
        elif state == "RECONVERGING":
            label = "RECONVERGING"

        ax.annotate(
            label,
            xy=(i, score),
            xytext=(i, min(score + 0.12, 1.0)),
            arrowprops={"arrowstyle": "->"},
            fontsize=8,
            ha="center",
        )

    ax.set_title("GyroAuth v2 — Live Stability Timeline")
    ax.set_xlabel("Authentication Step")
    ax.set_ylabel("Stability")
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(x)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUTPUT_IMAGE, dpi=160)
    plt.close(fig)


def main():
    rows = read_history()
    plot(rows)

    print(f"Generated: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
