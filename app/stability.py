from __future__ import annotations

from typing import Iterable, List, Optional
import numpy as np


def distance(a: Iterable[float], b: Iterable[float]) -> float:
    va = np.array(list(a), dtype=float)
    vb = np.array(list(b), dtype=float)
    return float(np.linalg.norm(va - vb))


def kernel_similarity(a: Iterable[float], b: Iterable[float], alpha: float = 1.0) -> float:
    d = distance(a, b)
    return float(np.exp(-alpha * d))


def stability(current: List[float], history: List[List[float]], alpha: float = 1.0) -> Optional[float]:
    if not history:
        return None
    sims = [kernel_similarity(current, h, alpha=alpha) for h in history]
    return float(np.mean(sims))


def consistency(history: List[List[float]], alpha: float = 1.0) -> Optional[float]:
    n = len(history)
    if n < 2:
        return None
    sims = []
    for i in range(n):
        for j in range(i + 1, n):
            sims.append(kernel_similarity(history[i], history[j], alpha=alpha))
    return float(np.mean(sims)) if sims else None
