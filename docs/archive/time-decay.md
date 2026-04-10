# docs/time-decay.md

# Dynamic Time Decay Logic

---

## 1. Purpose

This note introduces a **dynamic time-decay mechanism** for GyroAuth in order to reduce the replay window to near zero.

The goal is not merely to make replay attacks difficult, but to make them **operationally useless**.

---

## 2. Core Idea

Authentication data should not remain valid even for a short static interval.

Instead, validity should decay continuously as a function of elapsed time.

[
V_{auth}(t) = V_{base}(t) \cdot \delta(\Delta t)
]

Where:

* (V_{base}(t)): base authentication vector
* (\Delta t): elapsed time between generation and verification
* (\delta(\Delta t)): decay factor

---

## 3. Design Principle

Traditional OTP systems allow validity windows such as 30 seconds.

GyroAuth should move to a much shorter temporal validity model:

* ideal window: within 0.5 seconds
* degraded trust: 0.5 to 1.0 seconds
* invalid: beyond 1.0 seconds

This means intercepted data becomes unusable almost immediately.

---

## 4. Example Decay Model

A simple exponential model:

[
\delta(\Delta t) = e^{-\lambda \Delta t}
]

Where:

* large (\lambda) means rapid expiration

A stricter production model can be implemented as a hard gate:

[
\delta(\Delta t) =
\begin{cases}
1 & \Delta t \leq 0.5 \
\alpha & 0.5 < \Delta t \leq 1.0 \
0 & \Delta t > 1.0
\end{cases}
]

Where (0 < \alpha < 1).

---

## 5. Implementation Concept

### Client side

* generate authentication payload
* include timestamp (T_{gen})
* sign payload using device-bound key

### Server side

* receive payload at (T_{recv})
* calculate:

[
\Delta t = T_{recv} - T_{gen}
]

* apply decay
* reject stale vectors even if all other dimensions are correct

---

## 6. Why This Matters

Replay attacks depend on the assumption that captured authentication material remains valid long enough to be reused.

Dynamic time decay breaks that assumption.

Even if an attacker captures:

* device signature
* sensor payload
* state vector

the value of that payload collapses almost immediately.

---

## 7. Security Benefit

### Traditional model

* replay feasible inside validity window

### Time-decay model

* replay window shrinks toward zero
* captured data becomes disposable noise

> Authentication freshness becomes part of authentication itself.

---

## 8. Engineering Considerations

### Clock synchronization

The system needs bounded drift between client and server.

Possible mitigations:

* signed server nonce
* device-server round-trip calibration
* trusted time source

### Network latency

Hard expiry must account for realistic mobile latency.

Recommended deployment profile:

* consumer network: soft decay + hard cut around 1.0s
* enterprise/internal network: hard cut closer to 0.5s

### Jitter tolerance

A strict threshold should not punish legitimate users on unstable networks.
The decay model can reduce score before full rejection.

---

## 9. Integration with Scoring

Time freshness should not be treated as a separate add-on.
It should directly modulate the final score.

[
score_{final} = score_{state} \cdot \delta(\Delta t)
]

This preserves the GyroAuth principle:

> authentication is a continuous evaluation of valid state under time constraints

---

## 10. Development Implication

This feature should be designed early, not added later.

Why:

* timestamp must be embedded in signed payload structure
* server validation pipeline must be freshness-aware
* PoC metrics should include replay-window measurements

---

## 11. Suggested PoC Metrics

* mean generation-to-verification delay
* success rate under 0.5s / 1.0s thresholds
* replay rejection rate
* false rejection rate under mobile latency conditions

---

## 12. Key Statement

Security is not just about valid state.

It is about **fresh valid state**.

---

## 13. Conclusion

Dynamic time decay turns authentication from a reusable artifact into a rapidly expiring event.

In GyroAuth, time is not metadata.

It is part of the authentication logic itself.
