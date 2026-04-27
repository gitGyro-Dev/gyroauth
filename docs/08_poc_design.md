# GyroAuth v2 — Proof of Concept (PoC)

---

## 🧭 Purpose

The PoC demonstrates:

* Authentication under deviation
* Continuous identity validation
* Non-reproducibility
* Real-world feasibility

---

## ■ System Architecture

```text
[Client / UI]
    ↓
[GyroAuth API]
    ↓
[Policy Engine]
    ↓
[GyroOS Adapter]
    ↓
[GyroOS]
```

---

## ■ Core Scenarios

### 1. Normal Login

* Stable device
* Expected behavior
* Known network

👉 Result: AUTH_STABLE

---

### 2. Continuous Session

* Minor behavior drift
* Normal variation

👉 Result: AUTH_STABLE

---

### 3. Drift / Instability

* Slight anomaly
* Location change

👉 Result: RECONVERGING

---

### 4. Attack Scenario

* Device mismatch
* Behavior anomaly

👉 Result: AUTH_FAIL

---

## ■ Input Data

```json
{
  "device": {...},
  "behavior": {...},
  "time": {...},
  "space": {...},
  "network": {...}
}
```

---

## ■ Processing Flow

```text
Observe
↓
Slice
↓
Deviation
↓
Stability
↓
Selection
↓
Policy
↓
Auth Decision
```

---

## ■ Evaluation Metrics

* False Accept Rate (FAR)
* False Reject Rate (FRR)
* Re-convergence time
* Stability variance

---

## ■ Demonstration Output

* Stability graph
* Auth state transitions
* Slice-level breakdown

---

## ■ Success Criteria

* Authentication holds under small deviation
* Attack fails even with partial mimicry
* Recovery is possible without reset

---

## ■ Tech Stack

* FastAPI (backend)
* JSON (data)
* GyroOS (local or API)
* Simple UI (optional)

---

## 🔴 Final Statement

```text
PoC is not about proving theory.

It is about proving that authentication holds under deviation.
```
