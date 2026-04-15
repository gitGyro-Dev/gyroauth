from __future__ import annotations

from typing import List
from .models import RawState


def _device_hash(device_id: str) -> float:
    return (sum(ord(c) for c in device_id) % 1000) / 1000.0


def slice_state(state: RawState) -> List[float]:
    return [
        float(state.velocity),
        float(state.interaction),
        float(state.touch_pressure),
        float(state.typing_rhythm),
        float(state.x),
        float(state.y),
        _device_hash(state.device_id),
    ]
