from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Trajectory:
    user_id: Optional[str] = None
    raw_states: list = field(default_factory=list)
    features: List[List[float]] = field(default_factory=list)

    def add(self, raw_state, feature_vector: List[float], max_len: int) -> None:
        self.user_id = getattr(raw_state, "user_id", self.user_id)
        self.raw_states.append(raw_state)
        self.features.append(feature_vector)

        if len(self.raw_states) > max_len:
            self.raw_states = self.raw_states[-max_len:]
        if len(self.features) > max_len:
            self.features = self.features[-max_len:]

    def clear(self, keep_last_n: int = 0) -> int:
        if keep_last_n <= 0:
            self.raw_states.clear()
            self.features.clear()
        else:
            self.raw_states = self.raw_states[-keep_last_n:]
            self.features = self.features[-keep_last_n:]
        return len(self.features)

    def last(self):
        return self.features[-1] if self.features else None
