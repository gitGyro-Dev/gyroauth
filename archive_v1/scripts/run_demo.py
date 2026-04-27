from __future__ import annotations

from archive_v1.app.auth_engine import auth_score, decide_auth, trajectory_similarity
from archive_v1.app.config import settings
from archive_v1.app.demo_data import shifted_demo_sequence, stable_demo_sequence
from archive_v1.app.slice_engine import slice_state
from archive_v1.app.stability import stability


def evaluate_sequence(seq):
    features = [slice_state(s) for s in seq]
    current = features[-1]
    hist = features[:-1]
    stab = stability(current, hist, alpha=settings.alpha)
    return features, stab


def main():
    enrolled_seq = stable_demo_sequence(user_id="alice", session_id="sess-enroll", device_id="phone-A")
    enrolled_features, enrolled_stability = evaluate_sequence(enrolled_seq)

    auth_seq_good = stable_demo_sequence(
        user_id="alice", session_id="sess-auth-good", device_id="phone-A", start_t=100.0
    )
    auth_features_good, auth_stability_good = evaluate_sequence(auth_seq_good)
    sim_good = trajectory_similarity(auth_features_good, enrolled_features)
    score_good = auth_score(auth_stability_good, sim_good, auth_features_good)
    ok_good, reason_good = decide_auth(
        auth_stability_good, sim_good, score_good,
        settings.stability_threshold, settings.similarity_threshold
    )

    auth_seq_bad = shifted_demo_sequence(
        user_id="alice", session_id="sess-auth-bad", device_id="phone-A", start_t=200.0
    )
    auth_features_bad, auth_stability_bad = evaluate_sequence(auth_seq_bad)
    sim_bad = trajectory_similarity(auth_features_bad, enrolled_features)
    score_bad = auth_score(auth_stability_bad, sim_bad, auth_features_bad)
    ok_bad, reason_bad = decide_auth(
        auth_stability_bad, sim_bad, score_bad,
        settings.stability_threshold, settings.similarity_threshold
    )

    print("=== Enrolled Reference ===")
    print(f"Reference length: {len(enrolled_features)}")
    print(f"Reference stability: {enrolled_stability:.4f}")

    print("\n=== Good Authentication Attempt ===")
    print(f"Stability:  {auth_stability_good:.4f}")
    print(f"Similarity: {sim_good:.4f}")
    print(f"Score:      {score_good:.4f}")
    print(f"Auth:       {ok_good}")
    print(f"Reason:     {reason_good}")

    print("\n=== Bad Authentication Attempt ===")
    print(f"Stability:  {auth_stability_bad:.4f}")
    print(f"Similarity: {sim_bad:.4f}")
    print(f"Score:      {score_bad:.4f}")
    print(f"Auth:       {ok_bad}")
    print(f"Reason:     {reason_bad}")


if __name__ == "__main__":
    main()
