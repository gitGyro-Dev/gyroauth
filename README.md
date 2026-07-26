## 🚀 Latest Release

[**GyroAuth v2.1.0 — Guarded Criterion Trajectories and Research Demo**](https://github.com/gitGyro-Dev/gyroauth/releases/tag/v2.1.0)

Release notes: [`release_candidates/gyroauth/v2.1.0/release_notes.md`](release_candidates/gyroauth/v2.1.0/release_notes.md)

## ▶ Live Demo

https://gitgyro-dev.github.io/gyroauth/

The static research demo visualizes:

```text
Auth Decision
!=
Criterion Update Response
```

including the executable state:

```text
AUTH_STABLE + FREEZE
```

Jxiv status for the Guarded Criterion Trajectories English manuscript: **Under review**.

# GyroAuth vNext

**Authentication by Stability-based Selection over State Convergence**

---

## Position in the Stack

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Application (this repository)
```

* Gyro Logic defines **Structure / Slice / Deviation / Stability**
* GyroOS executes **Gyro Process + Operator Response**
* GyroAuth interprets results for **authentication decisions**

GyroAuth does not redefine Gyro Logic.  
GyroAuth does not reimplement GyroOS.  
GyroAuth is an application layer built on top of GyroOS.

---

## Core Definition

```text
Authentication = Stability-based Selection over State Convergence
```

State Convergence is what GyroAuth observes.  
Stability-based Selection is how GyroAuth makes an authentication decision.

In short:

```text
GyroAuth observes whether a multi-dimensional state converges
toward an expected Identity Trajectory,
then selects an Auth Decision based on Stability,
Deviation, Operator Response, and History.
```

---

## Updated Core Flow (v4 aligned)

```text
GyroOS:
Gyro Processₙ
→ Operator Responseₙ
→ Gyro Processₙ₊₁

GyroAuth:
Stability-based Selection
→ Auth Decision
```

---

## Key Correction

GyroAuth does NOT reduce authentication to:

```text
observe → evaluate → update
```

GyroAuth depends on:

```text
POST /loop/step
```

which returns:

```text
slice-done = X + Δ
Stability
Operator Response
History
```

GyroAuth maps these GyroOS execution results into application-level authentication decisions.

---

## vNext Loop-aligned PoC

GyroAuth vNext introduces a loop-aligned PoC based on the GyroOS v4 `/loop/step` premise.

The vNext PoC does not implement full GyroOS.  
It validates the GyroAuth interpretation layer:

```text
GyroOS /loop/step output
→ slice-done / Stability / Operator Response / History
→ Stability-based Selection over State Convergence
→ Auth Decision
```

Verified transition:

```text
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_FAIL
```

Important:

```text
Re-auth ≠ AUTH_FAIL
Re-auth → REAUTH_REQUIRED
```

See:

```text
docs/14_vnext_loop_poc.md
app/vnext/main.py
examples/vnext/
```

---

## Auth Decision States

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

* `AUTH_STABLE` — the session state converges toward the expected Identity Trajectory.
* `RECONVERGING` — deviation increased, but re-convergence is still possible.
* `REAUTH_REQUIRED` — explicit verification is required; identity has not necessarily collapsed.
* `AUTH_FAIL` — trajectory continuity collapsed and authentication cannot continue.

---

## Final Statement

GyroAuth is not driven by raw inputs.

It is driven by:

```text
State Convergence
+ Stability
+ Operator Response
+ History
→ Stability-based Selection
→ Authentication
```

Authentication is not exact matching.

It is whether identity still holds under change.
