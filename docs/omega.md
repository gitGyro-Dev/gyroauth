# Authentication Region (Ω)

---

## 1. Core Definition

In GyroAuth, authentication is defined as:

[
Auth(u,t) = 1 \iff X_t \in \Omega_u
]

Where:

* (X_t): observed state
* (\Omega_u): authentication region

---

## 2. What is Ω?

Ω is not a single point.

It is a **region in a multi-dimensional space**.

---

## 3. Structure of Ω

[
\Omega = \Omega_S \cap \Omega_T \cap \Omega_M \cap \Omega_D
]

Where:

* (\Omega_S): spatial constraints
* (\Omega_T): temporal constraints
* (\Omega_M): motion constraints
* (\Omega_D): device constraints

---

## 4. Interpretation

Authentication is not:

> matching a secret

It is:

> entering a valid region

---

## 5. Security Implication

As constraints increase:

* Region becomes smaller
* Valid states become fewer
* Attack becomes harder

---

### Key Statement

> Security = Reduction of admissible region

---

## 6. Why Region (Not Point)

Real-world systems include:

* GPS noise
* human variability
* sensor uncertainty

Therefore:

> authentication must tolerate variation

---

## 7. Visual Intuition

* Outside Ω → invalid
* Inside Ω → valid

---

## 8. Connection to GyroLogic

GyroLogic defines truth as:

> convergence within a valid region

GyroAuth applies the same principle:

> authentication = convergence into Ω

---

## 9. Conclusion

Authentication is not equality.

It is **admissibility within a constrained space**.
