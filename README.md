## 🚀 Latest Release

GyroAuth v2.0 (PoC)  
https://github.com/gitGyro-Dev/gyroauth/releases/tag/v2.0.0

# GyroAuth v2

**Authentication by Stability-based Selection under Deviation**

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

---

## Updated Core Flow (v4 aligned)

```text
GyroOS:
Gyro Processₙ
→ Operator Responseₙ
→ Gyro Processₙ₊₁

GyroAuth:
→ Selection
→ Auth Decision
```

---

## Key Correction

GyroAuth does NOT call:

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
```

---

## Final Statement

GyroAuth is not driven by raw inputs.

It is driven by:

```text
Stability + Operator Response
→ Selection
→ Authentication
```
