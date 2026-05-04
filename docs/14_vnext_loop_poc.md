# GyroAuth vNext — Loop-aligned PoC

## 1. Purpose

This PoC aligns GyroAuth with the GyroOS v4 `/loop/step` premise.

The goal is not to implement full GyroOS.  
The goal is to validate the GyroAuth interpretation layer:

```text
GyroOS /loop/step output
→ slice-done / Stability / Operator Response / History
→ Stability-based Selection over State Convergence
→ Auth Decision
```

---

## 2. Difference from v2.0 PoC

| Item | v2.0 PoC | vNext PoC |
|---|---|---|
| Main purpose | Feasibility demonstration | Loop-aligned interpretation |
| Core API | `/observe`, `/authenticate` | `/auth/step` |
| GyroOS premise | Simplified / mocked | `/loop/step`-shaped mock |
| Decision input | Stability-centered | Stability + Δ + Operator Response + History |
| States | AUTH_STABLE / RECONVERGING / AUTH_FAIL | AUTH_STABLE / RECONVERGING / REAUTH_REQUIRED / AUTH_FAIL |

---

## 3. Core Principle

`/loop/step` is not an authentication API.

It is the GyroOS execution unit:

```text
Gyro Processₙ
→ Operator Responseₙ
→ Gyro Processₙ₊₁
```

GyroAuth does not redefine `/loop/step`.

GyroAuth maps GyroOS execution results into authentication decisions.

---

## 4. API

### Start server

```bash
uvicorn app.vnext.main:app --reload
```

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### Endpoints

```text
POST /auth/step
GET  /auth/session/{session_id}
GET  /auth/history/{session_id}
POST /auth/reset/{session_id}
```

---

## 5. Expected Demo Flow

Use a fresh session or call:

```text
POST /auth/reset/demo-session-001
```

Then execute:

```text
POST /auth/step with stable_loop.json
POST /auth/step with mild_drift_loop.json
POST /auth/step with reauth_required_loop.json
POST /auth/step with recovery_loop.json
POST /auth/step with attack_collapse_loop.json
GET  /auth/session/demo-session-001
GET  /auth/history/demo-session-001
```

Expected states:

```text
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_FAIL
```

---

## 6. Verified Result

The vNext loop-aligned PoC was executed successfully.

Observed history:

```json
{
  "session_id": "demo-session-001",
  "stability_history": [
    0.92,
    0.78,
    0.66,
    0.89,
    0.42
  ],
  "deviation_history": [
    0.0883,
    0.18,
    0.3083,
    0.1067,
    0.585
  ],
  "response_history": [
    "Continue",
    "Adjust",
    "Re-auth",
    "Continue",
    "Fail"
  ],
  "auth_state_history": [
    "AUTH_STABLE",
    "RECONVERGING",
    "REAUTH_REQUIRED",
    "AUTH_STABLE",
    "AUTH_FAIL"
  ],
  "auth_score_history": [
    0.9262,
    0.7625,
    0.5998,
    0.8811,
    0.2336
  ]
}
```

Confirmed transition:

```text
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_FAIL
```

This confirms that `Re-auth` is not treated as failure.

```text
Re-auth ≠ AUTH_FAIL
Re-auth → REAUTH_REQUIRED
```

This is important because `REAUTH_REQUIRED` is an application-layer state meaning explicit verification is required, not that identity has already collapsed.

---

## 7. Decision Priority

The vNext decision rule is not a raw threshold rule.

Important:

```text
Operator Response = Re-auth
does not mean failure.
```

`Re-auth` means:

```text
Explicit verification is required.
```

Decision priority:

```text
1. Operator Response = Fail
   → AUTH_FAIL

2. Operator Response = Re-auth / Escalate
   → REAUTH_REQUIRED
   unless the state has actually collapsed

3. Otherwise, use AuthScore thresholds
```

---

## 8. AuthScore

```text
AuthScore =
0.40 * Stability
+ 0.25 * TrajectoryContinuity
+ 0.20 * ResponseConfidence
+ 0.15 * (1.0 - ContextRisk)
- 0.20 * DeviationRisk
```

Thresholds:

```text
AuthScore >= 0.85 → AUTH_STABLE
0.70 <= AuthScore < 0.85 → RECONVERGING
0.55 <= AuthScore < 0.70 → REAUTH_REQUIRED
AuthScore < 0.55 → AUTH_FAIL candidate
```

However, Operator Response has semantic priority.

---

## 9. Final Statement

v2.0 PoC proves feasibility.

vNext PoC proves loop-aligned interpretation.

```text
/auth/step
→ GyroOS /loop/step mock
→ slice-done / Stability / Operator Response / History
→ Stability-based Selection over State Convergence
→ Auth Decision
```
