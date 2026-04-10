# GyroAuth PoC Design

---

## 1. Objective

Demonstrate that authentication can be based on state convergence rather than credential matching.

---

## 2. Use Case

High-value transaction authentication:

* User initiates transaction on PC
* Mobile device verifies identity

---

## 3. System Architecture

* Client (PC)
* Server
* Mobile device (sensor source)

---

## 4. Data Collection

* location (GPS / Wi-Fi)
* time
* motion (accelerometer / gyro)
* device identity

---

## 5. Feature Extraction

* spatial distance
* time difference
* motion similarity
* device consistency

---

## 6. Scoring Model

[
score = w_s S + w_t T + w_m M + w_d D
]

---

## 7. Decision

* score ≥ 0.9 → accept
* 0.6 ≤ score < 0.9 → step-up
* score < 0.6 → reject

---

## 8. Evaluation Metrics

* acceptance rate (legitimate)
* rejection rate (attack)
* latency
* usability

---

## 9. Expected Outcome

* reduced replay attacks
* improved contextual authentication
* better alignment with zero-trust models

---

## 10. Conclusion

GyroAuth enables authentication as a dynamic evaluation of state, not static verification of credentials.
