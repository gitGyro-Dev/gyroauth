from __future__ import annotations

from typing import List
from .models import RawState


def stable_demo_sequence(user_id: str, session_id: str, device_id: str, start_t: float = 0.0) -> List[RawState]:
    points = [
        (10.0, 10.0, 0.9, 0.55, 0.40, 0.60),
        (10.2, 10.1, 0.92, 0.57, 0.42, 0.62),
        (10.1, 10.0, 0.88, 0.54, 0.39, 0.59),
        (10.3, 10.2, 0.91, 0.56, 0.41, 0.61),
        (10.2, 10.1, 0.90, 0.55, 0.40, 0.60),
        (10.1, 10.2, 0.89, 0.56, 0.40, 0.61),
    ]
    seq = []
    for i, (x, y, v, interaction, pressure, rhythm) in enumerate(points):
        seq.append(
            RawState(
                timestamp=start_t + i,
                user_id=user_id,
                session_id=session_id,
                device_id=device_id,
                x=x,
                y=y,
                velocity=v,
                interaction=interaction,
                touch_pressure=pressure,
                typing_rhythm=rhythm,
            )
        )
    return seq


def shifted_demo_sequence(user_id: str, session_id: str, device_id: str, start_t: float = 100.0) -> List[RawState]:
    points = [
        (20.0, 5.0, 1.5, 0.20, 0.10, 0.20),
        (20.5, 5.4, 1.6, 0.18, 0.12, 0.18),
        (21.0, 5.9, 1.55, 0.22, 0.11, 0.19),
        (21.5, 6.3, 1.7, 0.21, 0.13, 0.21),
        (22.0, 6.8, 1.65, 0.19, 0.12, 0.20),
    ]
    seq = []
    for i, (x, y, v, interaction, pressure, rhythm) in enumerate(points):
        seq.append(
            RawState(
                timestamp=start_t + i,
                user_id=user_id,
                session_id=session_id,
                device_id=device_id,
                x=x,
                y=y,
                velocity=v,
                interaction=interaction,
                touch_pressure=pressure,
                typing_rhythm=rhythm,
            )
        )
    return seq
