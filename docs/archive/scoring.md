# Continuous Authentication (Scoring Model)

---

## 1. Core Idea

Authentication is not binary.

It is continuous.

---

## 2. From Boolean to Score

Traditional:

[
Auth = True / False
]

GyroAuth:

[
Auth = score \in [0,1]
]

---

## 3. Definition

[
score = sim(\Gamma, \hat{\Gamma})
]

Where:

* (\Gamma): observed trajectory
* (\hat{\Gamma}): expected trajectory

---

## 4. Decomposition

[
score = w_s S + w_t T + w_m M + w_d D
]

Where:

* (S): spatial similarity
* (T): temporal similarity
* (M): motion similarity
* (D): device consistency

---

## 5. Interpretation

Authentication is:

> how close a state is to a valid region

---

## 6. Threshold Model

* score ≥ 0.9 → accept
* 0.6 ≤ score < 0.9 → step-up
* score < 0.6 → reject

---

## 7. Advantages

* tolerant to noise
* adaptive to context
* enables continuous authentication

---

## 8. Security Implication

Attackers must:

* reproduce trajectory
* maintain consistency
* achieve high score

---

## 9. Connection to GyroLogic

GyroLogic defines:

> truth as stability

GyroAuth defines:

> authentication as convergence score

---

## 10. Key Statement

Authentication is not a decision.

It is a **continuous evaluation of convergence**.

---

## 11. Conclusion

Scoring transforms authentication from a rigid gate into a dynamic evaluation process.

It reflects real-world uncertainty while maintaining security.
