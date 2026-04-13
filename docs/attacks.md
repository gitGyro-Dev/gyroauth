# Attack Models

## 1. Pseudo-Soliton Attack

Locally stable behavior mimicking real identity:

- Appears stable short-term
- Fails long-term convergence

Mitigation:
- Require long-term stability
- Verify re-convergence

---

## 2. Phase Attack

Replay with phase shift:

\[
\Delta\phi(t) \neq 0
\]

Mitigation:
- Phase synchronization checks

---

## 3. Drift Attack

Gradual deviation:

\[
D(t) = \left\|\frac{d}{dt}(\gamma - \hat{\gamma})\right\|
\]

Mitigation:
- Drift monitoring
- Adaptive thresholds

---

## 4. Void Exploitation

Occurs in unobserved regions:

Mitigation:
- Increase slice density
- Detect observation gaps