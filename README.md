# GyroAuth v2

**Authentication by Stability-based Selection under Deviation**

---

![Live Stability](outputs/live_stability_timeline.png)

---

## Position in the Stack

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Application (this repository)
```

* Gyro Logic defines **Structure / Slice / Deviation / Stability**
* GyroOS computes **Deviation -> Stability -> Selection**
* GyroAuth uses those outputs for **authentication decisions**

Upper layers do NOT depend on lower layers.  
Lower layers implement upper layers.  
Mixing layers is strictly prohibited.

---

## What is GyroAuth?

GyroAuth is an authentication system where:

> Authentication is not exact matching.  
> It is **stability-based selection under intrinsic deviation**.

Traditional authentication asks:

```text
Does this input match the stored value?
```

GyroAuth asks:

```text
Is this session still operationally acceptable as the same identity?
```

---

## Why it matters

Traditional authentication assumes:

* Exact reproducibility
* Static identity
* Binary decision (match / fail)

But real-world identity is:

* Noisy
* Dynamic
* Context-dependent

GyroAuth is designed for:

* Identity under deviation
* Authentication as a continuous process
* Selection instead of matching

---

## Core Definition

```text
Authentication = Stability-based Selection
```

More precisely:

```text
Auth <=> Selected(Representation | Stability under Delta)
```

Where:

* Delta = Deviation between observations
* Stability = tolerance to deviation
* Selection = operational choice

---

## Core Flow

```text
Structure
↓
Slice (multi-perspective observation)
↓
Observation Set
↓
Delta (Deviation)
↓
Stability Evaluation
↓
Selection
↓
Auth Decision
```

---

## Multi-Slice Model

GyroAuth operates on multiple observational slices:

* Space (location / IP)
* Time (temporal patterns)
* Motion (device dynamics)
* Device (hardware identity)
* Behavior (interaction patterns)
* Network (communication characteristics)

Identity is not a point.  
It is a **stable trajectory across slices**.

---

## Auth Decision States

```text
AUTH_STABLE
RECONVERGING
AUTH_FAIL
```

### AUTH_STABLE
* Session is stable

### RECONVERGING
* Deviation increased
* Additional observation required

### AUTH_FAIL
* Stability collapsed
* Re-authentication required

---

## Continuous Authentication

Authentication is not a one-time event.

GyroAuth continuously evaluates:

* Stability drift
* Slice inconsistency
* Re-convergence capability

Identity must remain stable over time.

---

## Security Model

GyroAuth is designed against:

* Replay attacks
* Credential theft
* Device spoofing
* Behavior imitation
* Emulator-based attacks

Why it works:

* No single static credential
* Multi-slice dependency
* Time-dependent trajectory
* Non-reproducible state evolution

Identity cannot be copied. It must continuously emerge.

---

## API (Conceptual)

```text
POST /observe
POST /authenticate
POST /reconverge
GET  /session/{id}
```

---

## Relation to GyroOS

GyroAuth does NOT compute:

* Deviation
* Stability
* Selection

These are provided by GyroOS.

GyroAuth only handles:

* Policy
* Risk control
* Auth decision

---

## Live PoC (FastAPI)

Run:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Demo flow:

```text
/observe -> /authenticate -> AUTH_STABLE
/observe -> /authenticate -> RECONVERGING
/observe -> /authenticate -> AUTH_STABLE
/observe -> /authenticate -> AUTH_FAIL
```

The graph above reflects this exact flow.

---

## Use Cases

* Passwordless authentication
* Continuous session verification
* Device trust modeling
* Anomaly detection
* Next-generation Zero Trust systems

---

## Documentation

Start here:

* docs/00_positioning.md
* docs/01_auth_model.md
* docs/03_decision_policy.md
* docs/08_poc_design.md
* docs/13_fastapi_poc.md

---

## Repository Structure

```text
docs/        -> Specifications
app/         -> Implementation
scripts/     -> Demo
examples/    -> Sample data
archive_v1/  -> Previous version
```

---

## One-line Definition

GyroAuth is:

> An authentication system that determines identity by stability-based selection under deviation.

---

## Final Statement

Authentication is not about perfect reproduction.

It is about whether identity **still holds under change**.
