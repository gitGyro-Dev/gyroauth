from __future__ import annotations

from typing import List, Optional, Tuple
import numpy as np

from .stability import distance, consistency


def align_trajectories(
    current: List[List[float]],
    reference: List[List[float]],
    max_points: int,
) -> Tuple[List[List[float]], List[List[float]]]:
    if not current or not reference:
        return [], []

    current_cut = current[-max_points:]
    reference_cut = reference[-max_points:]

    n = min(len(current_cut), len(reference_cut))
    return current_cut[-n:], reference_cut[-n:]


def trajectory_similarity(
    current: List[List[float]],
    reference: List[List[float]],
    max_points: int = 20,
) -> Optional[float]:
    c, r = align_trajectories(current, reference, max_points=max_points)
    if not c or not r:
        return None

    dists = [distance(a, b) for a, b in zip(c, r)]
    mean_dist = float(np.mean(dists))
    return float(1.0 / (1.0 + mean_dist))


def auth_score(
    stability_score: Optional[float],
    trajectory_similarity_score: Optional[float],
    trajectory: List[List[float]],
    w_stability: float = 0.4,
    w_similarity: float = 0.4,
    w_consistency: float = 0.2,
) -> Optional[float]:
    if stability_score is None or trajectory_similarity_score is None:
        return None

    c = consistency(trajectory)
    consistency_score = 0.0 if c is None else c
    score = (
        w_stability * stability_score
        + w_similarity * trajectory_similarity_score
        + w_consistency * consistency_score
    )
    return float(score)


def decide_auth(
    stability_score: Optional[float],
    similarity_score: Optional[float],
    combined_score: Optional[float],
    min_stability: float,
    min_similarity: float,
):
    if stability_score is None:
        return False, "Not enough history to evaluate stability."
    if similarity_score is None:
        return False, "Reference trajectory missing or too short."
    if stability_score < min_stability:
        return False, "Stability below threshold."
    if similarity_score < min_similarity:
        return False, "Trajectory similarity below threshold."
    if combined_score is None:
        return False, "Could not compute combined score."
    return True, "Authenticated by state convergence."
