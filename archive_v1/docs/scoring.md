# Scoring

## Stability

Stability = mean(exp(-distance))

---

## Final Score

auth_score =
w1 * stability +
w2 * trajectory_similarity +
w3 * consistency

---

## Decision

auth_score > threshold