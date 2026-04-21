# docs/intentional-gesture.md

# Intentional Gesture as Dynamic Key Material

---

## 1. Purpose

This note proposes an authentication extension where a deliberate physical gesture contributes to the login event.

The goal is to turn password entry itself into a **multi-dimensional act**, rather than a purely symbolic one.

---

## 2. Core Idea

A password alone is a string.

GyroAuth can extend this by requiring the device to be held or moved in a specific way during input.

Example:

* user enters password
* while tilting device forward by 15 degrees
* within a tolerated gesture window

This means authentication depends on both:

* symbolic input
* embodied device state

---

## 3. Conceptual Shift

Traditional password input:

[
Auth \sim H(K)
]

Gesture-extended input:

[
Auth \sim H(K, G)
]

Where:

* (K): password or secret
* (G): gesture-derived state

---

## 4. Gesture as Dynamic Salt

A practical implementation uses sensor-derived gesture features as dynamic salt-like material.

For example:

[
G = g(a_t, \omega_t, q_t)
]

Where:

* (a_t): acceleration
* (\omega_t): angular velocity
* (q_t): orientation/quaternion

Then:

[
K' = H(K \parallel G \parallel nonce)
]

This means the final authentication material is valid only under the intended gesture condition.

---

## 5. Why This Matters

If an attacker learns the visible password:

* shoulder surfing
* screen observation
* leaked input sequence

that still does not reveal the physical dimension of the act.

The attacker must also reproduce:

* device angle
* motion pattern
* timing of the gesture

---

## 6. Security Benefit

This idea helps resist:

* visual password theft
* static secret replay
* simple credential observation attacks

It adds a physical layer without needing a separate external token.

---

## 7. Engineering Caution

This should **not** rely on raw sensor values alone.

Raw sensors are noisy and unstable.

Instead, the system should derive compact gesture features such as:

* tilt range class
* directional movement class
* stable orientation window
* gesture timing interval

This produces a robust and repeatable gesture state.

---

## 8. Practical Design Pattern

### Enrollment

* user chooses or is assigned a simple gesture
* system records tolerated feature envelope

### Verification

* user performs password entry
* system checks whether gesture features fall inside valid region

---

## 9. Example Rule

[
Auth = 1 \iff
\begin{cases}
K \text{ is correct} \
G \in \Omega_G
\end{cases}
]

Where (\Omega_G) is the valid gesture region.

This maintains consistency with the broader GyroAuth model:

> authentication = admissibility into a constrained region

---

## 10. UX Considerations

This idea is powerful but potentially fragile if overdesigned.

Recommended constraints:

* keep gesture simple
* use tolerant ranges, not exact angles
* reserve for high-risk flows, not every login

Good examples:

* slight forward tilt
* brief right-left tilt
* hold steady in a narrow orientation band

Bad examples:

* complex secret dance-like motion
* overly precise angle requirement
* long gesture sequences

---

## 11. PoC Direction

### Input

* password
* device orientation
* accelerometer / gyroscope
* timing

### Output

* gesture match score
* final authentication decision

### Metrics

* successful legitimate repetition rate
* observation attack resistance
* usability burden

---

## 12. Relationship to GyroAuth

This mechanism does not replace the password.

It transforms password entry into a **stateful event**.

The secret becomes inseparable from the physical condition of its execution.

---

## 13. Key Statement

A password should not only be known.

It should be **performed in a valid physical state**.

---

## 14. Conclusion

Intentional gesture extends authentication from symbolic input into embodied action.

This creates a practical bridge between classical credentials and multi-dimensional state authentication.
