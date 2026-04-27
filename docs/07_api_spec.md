# GyroAuth v2 — API Specification

---

## 🧭 Purpose

This document defines the API layer of GyroAuth.

GyroAuth:

* Collects observations
* Sends them to GyroOS
* Receives Stability / Selection
* Applies policy
* Returns authentication decision

---

## ■ System Role

```text
Client
↓
GyroAuth API
↓
GyroOS (Deviation / Stability / Selection)
↓
GyroAuth Policy
↓
Auth Decision
```

---

## ■ API Overview

```text
POST /observe
POST /authenticate
POST /reconverge
GET  /session/{id}
```

---

## ■ 1. POST /observe

### Purpose

Collect multi-slice observation data.

---

### Request

```json
{
  "session_id": "string",
  "timestamp": 1710000000,
  "slices": {
    "device": {...},
    "behavior": {...},
    "time": {...},
    "space": {...},
    "network": {...},
    "motion": {...}
  }
}
```

---

### Description

* Raw or preprocessed data
* Slice-based structure
* Partial slices allowed

---

### Response

```json
{
  "status": "ok"
}
```

---

## ■ 2. POST /authenticate

### Purpose

Perform authentication decision based on current state.

---

### Request

```json
{
  "session_id": "string"
}
```

---

### Internal Flow

```text
Retrieve observations
↓
Call GyroOS
↓
Get:
  - deviation profile
  - stability scores
  - selection result
↓
Apply policy
↓
Return auth decision
```

---

### Response

```json
{
  "auth_state": "AUTH_STABLE",
  "stability": 0.92,
  "risk_level": "low",
  "details": {
    "device": 0.95,
    "behavior": 0.90,
    "time": 0.93
  }
}
```

---

## ■ 3. POST /reconverge

### Purpose

Trigger re-evaluation under degraded stability.

---

### Request

```json
{
  "session_id": "string",
  "reason": "manual | automatic"
}
```

---

### Behavior

* Increase observation frequency
* Require additional slices
* Optionally trigger soft challenge

---

### Response

```json
{
  "auth_state": "RECONVERGING",
  "message": "additional observation required"
}
```

---

## ■ 4. GET /session/{id}

### Purpose

Retrieve current session status.

---

### Response

```json
{
  "session_id": "string",
  "auth_state": "AUTH_STABLE",
  "stability": 0.91,
  "history": [
    {
      "timestamp": 1710000000,
      "stability": 0.93
    },
    {
      "timestamp": 1710000100,
      "stability": 0.89
    }
  ]
}
```

---

## ■ Auth States

```text
AUTH_STABLE
RECONVERGING
AUTH_FAIL
```

---

## ■ Risk Levels

```text
low
medium
high
```

---

## ■ Error Handling

### Invalid Session

```json
{
  "error": "SESSION_NOT_FOUND"
}
```

---

### Insufficient Data

```json
{
  "error": "INSUFFICIENT_OBSERVATION"
}
```

---

## ■ GyroOS Integration

GyroAuth calls GyroOS through an adapter layer:

```text
GyroAuth → GyroOS Adapter → GyroOS API
```

Expected GyroOS response:

```json
{
  "stability": 0.92,
  "deviation": {...},
  "selection": {...}
}
```

---

## ■ Design Principles

* Stateless API layer
* Session-based evaluation
* Slice-agnostic input
* GyroOS-decoupled interface

---

## 🔴 Final Statement

```text
The API does not authenticate by itself.

It orchestrates observation, evaluation, and decision.
```
