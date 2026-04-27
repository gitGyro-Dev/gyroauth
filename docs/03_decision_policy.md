# GyroAuth v2 — Decision Policy

---

## 🧠 Purpose

This document defines how GyroAuth converts:

* Deviation (Δ)
* Stability
* Selection

into:

👉 Authentication decisions

---

## ■ Core Principle

```text id="z3ey0m"
Authentication is a policy applied to stability under deviation.
```

GyroAuth does NOT decide based on:

* Exact matching
* Single observation
* Static thresholds

👉 It decides based on:

* Multi-slice stability
* Deviation patterns
* Temporal consistency

---

## ■ Input Model

GyroAuth receives from GyroOS:

* Stability score(s)
* Deviation profile (Δ)
* Selection candidates

---

## ■ Decision Pipeline

```text id="6od6rf"
Observation
↓
Multi-Slice Analysis
↓
Deviation Profile (Δ)
↓
Stability Evaluation
↓
Policy Application
↓
Auth Decision
```

---

## ■ Stability Model

### 1. Slice-level Stability

Each slice produces its own stability score:

```text id="1xk9ai"
Stab_device
Stab_behavior
Stab_time
Stab_space
Stab_network
Stab_motion
```

---

### 2. Session-level Stability

Overall stability is computed as:

```text id="y6mndh"
Stab_session = Σ (wi * Stab_i) - Penalty(critical deviation)
```

Where:

* wi = slice weight
* Penalty = penalty for abnormal deviation

---

## ■ Slice Weighting

Different slices have different importance.

### Core Slices (high weight)

* Device
* Behavior
* Time

### Contextual Slices (medium weight)

* Space
* Network
* Motion

---

## ■ Critical Deviation Detection

Certain deviations must override average stability.

Examples:

* Unknown device
* Impossible location jump
* Network anomaly
* Behavior discontinuity

```text id="kwxknh"
If critical deviation detected → force RECONVERGING or AUTH_FAIL
```

---

## ■ Decision Thresholds

Define thresholds:

```text id="px1m8b"
θ_stable
θ_recover
θ_fail
```

Where:

* θ_stable > θ_recover > θ_fail

---

## ■ Auth Decision Logic

```text id="yk3z7r"
if Stab_session ≥ θ_stable:
    AUTH_STABLE

elif Stab_session ≥ θ_recover:
    RECONVERGING

else:
    AUTH_FAIL
```

---

## ■ Interpretation

### AUTH_STABLE

* Stability is sufficient
* Identity is considered valid
* No additional action

---

### RECONVERGING

* Stability degraded
* Identity uncertain but recoverable
* Requires additional observation or soft challenge

---

### AUTH_FAIL

* Stability collapsed
* Identity invalid
* Requires re-authentication

---

## ■ Risk-based Adjustment

Thresholds are NOT fixed.

They adapt based on context:

### Low-risk context

* Lower θ_stable
* More tolerant to deviation

### High-risk context

* Higher θ_stable
* Stricter evaluation

---

## ■ Context Factors

Risk level is influenced by:

* Transaction type
* Device trust
* Network environment
* Access frequency
* User profile

---

## ■ Temporal Stability

Stability must be evaluated over time:

```text id="5m8r0u"
Stab(t) = f(Stab_t-n ... Stab_t)
```

This enables:

* Drift detection
* Sudden instability detection
* Recovery tracking

---

## ■ Re-convergence Policy

When entering RECONVERGING:

System should:

* Increase observation frequency
* Require additional slices
* Apply soft challenge (optional)

```text id="v5m2rd"
Goal: restore stability without breaking UX
```

---

## ■ Fail-safe Policy

When AUTH_FAIL:

* Terminate session OR
* Require step-up authentication

Examples:

* MFA fallback
* Full re-login

---

## ■ Anti-patterns (Prohibited)

The following MUST NOT be implemented:

❌ Single threshold decision
❌ Single-slice dependency
❌ Exact match fallback
❌ Immediate fail on minor deviation

---

## ■ Design Philosophy

GyroAuth assumes:

```text id="s9muj6"
Deviation is normal
```

Therefore:

```text id="i7h0t2"
Authentication must tolerate deviation
```

---

## ■ Key Insight

Traditional systems:

```text id="gk8x3y"
Deviation = error
```

GyroAuth:

```text id="q3u4zx"
Deviation = signal
```

---

## 🔴 Final Statement

```text id="4hb4pp"
Authentication is not about rejecting deviation.

It is about determining whether deviation is still acceptable.
```
