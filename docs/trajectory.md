# Trajectory Authentication

---

## 1. Core Idea

Authentication is not a point.

It is a trajectory.

---

## 2. From State to Sequence

Traditional:

[
Auth = X_t \in \Omega
]

Trajectory-based:

[
\Gamma = {X_{t_1}, X_{t_2}, ..., X_{t_n}}
]

[
Auth = \Gamma \in \Omega_{\Gamma}
]

---

## 3. What is a Trajectory?

A trajectory is a time-ordered sequence of states.

Each state includes:

* location
* time
* motion
* device context

---

## 4. Why Trajectory Matters

A single state can be imitated.

A trajectory requires:

* temporal consistency
* physical plausibility
* behavioral continuity

---

## 5. Reproducibility

Reproducing a point is possible.

Reproducing a trajectory is extremely difficult.

---

[
P(\Gamma' = \Gamma) \rightarrow 0
]

---

## 6. Consistency Constraints

Authentication requires:

* spatial consistency
* temporal consistency
* motion consistency

---

## 7. Security Implication

Security is strengthened by:

* increasing sequence length
* increasing constraint density

---

## 8. Connection to GyroAuth

GyroAuth evaluates:

* state → admissibility
* trajectory → consistency

---

## 9. Key Statement

Authentication is not a state.

It is a **sequence of valid transformations over time**.

---

## 10. Conclusion

Trajectory authentication transforms identity from a static condition into a dynamic process.

It is not about where you are.

It is about how you arrive there.
