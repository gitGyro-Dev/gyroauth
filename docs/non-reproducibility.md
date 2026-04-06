# Non-Reproducibility

---

## 1. Core Idea

The core security property of GyroAuth is:

> Authentication cannot be reproduced.

---

## 2. Traditional Security Model

Security is based on:

* protecting secrets
* preventing access
* increasing difficulty

---

## Problem

If secrets are stolen:

→ authentication can be replayed

---

## 3. GyroAuth Model

Authentication depends on:

* space
* time
* motion
* device constraints

---

## 4. Attack Model

An attacker must reproduce:

[
X_t = (S_t, T_t, M_t, D_t)
]

---

## 5. Impossibility

Perfect reproduction requires:

* exact location
* exact time
* exact motion
* exact device state

---

[
P(X'_t = X_t) \approx 0
]

---

## 6. Security Shift

Traditional:

> Hard to break

GyroAuth:

> Impossible to satisfy

---

## 7. Key Statement

> Security is not resistance.
> It is non-reproducibility.

---

## 8. Implication

Even if credentials are leaked:

→ authentication cannot succeed

---

## 9. Conclusion

Authentication is no longer about secrets.

It is about the ability to reproduce a valid state.

And that is fundamentally non-reproducible.
