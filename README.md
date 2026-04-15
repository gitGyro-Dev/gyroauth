# GyroAuth
Authentication as State Convergence

---

## Concept

Authentication is not identity verification.

It is convergence of dynamic state.

---

## Core Idea

Auth = trajectory convergence

---

## Pipeline

Input → Slice → Stability → Trajectory → Convergence → Auth

---

## Mapping to Gyro Logic

| Theory | Implementation |
|------|------|
| Structure | Input |
| Slice | Feature extraction |
| Stability | scoring |
| Identity | trajectory |
| Limit | convergence |

---

## API

- POST /observe
- GET /stability
- POST /authenticate
- POST /reconverge

---

## Status

PoC in progress