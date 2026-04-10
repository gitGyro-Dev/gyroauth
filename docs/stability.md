# Stability Model

## Stability Function

Stability measures whether a trajectory behaves like a soliton:

\[
\mathrm{Stab}(\gamma) =
w_I I
+ w_P P
+ w_R R
+ w_T T
- w_D D
- w_V V
\]

---

## Invariance

Robustness across observation slices:

\[
I = 1 - \frac{1}{N}\sum_k d(O_k(\gamma), O_k(\hat{\gamma}))
\]

---

## Phase Alignment

\[
P = \left|\frac{1}{N}\sum_{j=1}^N e^{i\Delta\phi_j}\right|
\]

---

## Re-Convergence

\[
R = e^{-\tau_{rec}/\tau_0}
\]

---

## Temporal Consistency

\[
T = 1 - \mathrm{Var}(S_t)
\]

---

## Drift

\[
D = \frac{1}{T}\int_0^T
\left\|\frac{d}{dt}(\gamma - \hat{\gamma})\right\|dt
\]

---

## Void Exposure

\[
V = \frac{1}{T}\int_0^T \mathbf{1}_{void}(t)dt
\]

---

## Adaptive Threshold

\[
\theta(t) = \theta_0
+ \beta_R R_{risk}
+ \beta_V V
+ \beta_A A
- \beta_H H
\]