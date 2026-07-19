# GyroAuth Guarded Criterion Update PoC — Implementation and Results

## 1. Purpose

This document completes **Priority H: PoC Implementation and Results** for the GyroAuth formalization and paper-preparation work.

It builds on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
docs/18_formal_security_model.md
docs/19_criterion_update_state_machine.md
docs/20_normal_and_poisoned_update_scenarios.md
docs/21_minimal_simulation_design.md
```

The PoC implements and executes the minimum deterministic comparison between:

```text
Model U: Unconstrained Criterion Update
Model G: Guarded Criterion Update
```

The central proposition tested is:

```text
dynamic criterion
!=
unconstrained self-update
```

The PoC does not claim production-grade security, empirical generality, or a completed security proof.

---

## 2. Invariant Foundation

The existing GyroAuth foundation remains unchanged:

```text
Authentication
=
Stability-based Selection over State Convergence
```

The layer relationship remains:

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Authentication Application
```

The Gyro Logic Core remains:

```text
Structure
↓
Slice
↓
Stability
```

This PoC does not redefine Gyro Logic or GyroOS.

```text
Core change: none
GyroOS contract change: none
GyroAuth PoC: added
```

---

## 3. Implemented Artifacts

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
docs/22_poc_implementation_and_results.md
```

The implementation uses only the Python standard library.

It is deterministic and requires no external telemetry, model training, or network connection.

---

## 4. Execution

Command:

```bash
python scripts/simulate_guarded_criterion_update.py \
  --scenarios examples/criterion_update/scenarios.json \
  --output results/criterion_update_results.json
```

Recorded execution result:

```text
exit code = 0
assertions passed = 7 / 7
```

`results/criterion_update_summary.json` records the verified summary.

The script writes the complete stage-by-stage result to:

```text
results/criterion_update_results.json
```

when executed.

---

## 5. Implemented Model

## 5.1 Criterion

The effective criterion is represented by:

```text
A_t = (
  mu_t,
  width_t,
  provenance_requirement_t,
  challenge_requirement_t,
  rollback_integrity_t
)
```

This is a minimum numeric abstraction. It is not a claim that production authentication is one-dimensional.

## 5.2 Candidate generation

Both models use the same candidate generator.

```text
mu*_(t+1)
=
mu_t + eta_mu (y_t - mu_t)
```

```text
width*_(t+1)
=
width_t
+ eta_width max(0, |y_t - mu_t| - width_t)
```

The models differ only in candidate adoption.

## 5.3 Model U

```text
Observation
→ Candidate
→ Direct Adoption
```

Model U has no independent Guard, Criterion Integrity Evaluation, Freeze, Review, or Rollback selection.

## 5.4 Model G

```text
Observation
→ Candidate
→ Guard Vector
→ Criterion Update Response
→ Effective Criterion Transition
```

The effective criterion changes only through `ACCEPT`.

```text
Candidate Update
!=
Accepted Criterion
```

---

## 6. Implemented Guard Vector

The PoC evaluates:

```text
provenance
cross-evidence consistency
challenge confirmation
update magnitude
update direction
cumulative update rate
discrimination preservation
rollback linkage
evidence-source integrity
```

Each Guard result is:

```text
PASS
WARN
FAIL
```

Critical failures are not averaged away.

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

A scalar Criterion Integrity summary is generated only for visualization and reporting. It does not override the Guard vector.

---

## 7. Implemented Decisions

### Auth Decision

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

### Criterion Update Response

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

The two decision streams remain independent.

```text
Auth Decision
!=
Criterion Update Response
```

---

## 8. Scenario N1 — Legitimate New Device Transition

### 8.1 Objective

Confirm that trusted, Context-explainable change can be incorporated after explicit verification.

### 8.2 Model G result

```text
Auth Decision:
REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_STABLE
```

```text
Criterion Update Response:
DEFER
→ ACCEPT
→ ACCEPT
```

```text
Final Criterion State:
STABLE
```

Final values:

```text
mu    = 0.234
width = 0.120
```

The width did not broaden. The new Context shifted the criterion center through bounded, supported adaptation.

### 8.3 Interpretation

The first candidate was not adopted because challenge confirmation was still pending.

After successful re-authentication and cross-evidence consistency, the guarded model accepted the bounded update.

This demonstrates:

```text
adaptive
!=
permanently fixed
```

and:

```text
Guarded
!=
non-adaptive
```

---

## 9. Scenario P1 — Gradual Region Expansion Poisoning

### 9.1 Objective

Test whether repeated small, suspicious observations can broaden the criterion until the attack reference becomes admissible.

The attack reference is:

```text
y_attack = 0.62
```

### 9.2 Model U result

Final values:

```text
mu    = 0.3969728
width = 0.277212
```

Result:

```text
attack reference admissible = true
```

Model U directly adopted each candidate:

```text
DIRECT_ADOPT
→ DIRECT_ADOPT
→ DIRECT_ADOPT
→ DIRECT_ADOPT
→ DIRECT_ADOPT
```

The criterion moved and broadened until the attack reference entered the admissible region.

### 9.3 Model G result

Final values:

```text
mu    = 0.200
width = 0.120
```

Response path:

```text
DEFER
→ FREEZE
→ FREEZE
→ FREEZE
→ FREEZE
```

```text
freeze stage = 2
attack reference admissible = false
```

The effective criterion remained at the trusted initial state.

### 9.4 Decision separation result

At stage 2, the PoC produced:

```text
AUTH_STABLE + FREEZE
```

This is a required result.

It means:

```text
the current access relation may remain temporarily continuable
while
criterion adaptation is stopped
```

The criterion response was not inferred directly from the Auth Decision.

### 9.5 Interpretation

The guarded model recognized repeated, unexplained update direction and cross-evidence weakness before the attack reference became admissible.

This demonstrates the operational difference between:

```text
current subject acceptance
```

and:

```text
permission to redefine future acceptance
```

---

## 10. Scenario C1 — Single Evidence Source Compromise

### 10.1 Objective

Confirm that an apparently valid Evidence value does not authorize criterion adaptation when source integrity and cross-evidence consistency fail.

### 10.2 Model G result

Response path:

```text
FREEZE
→ FREEZE
```

Final values:

```text
mu    = 0.200
width = 0.120
```

No candidate was accepted.

### 10.3 Interpretation

The scenario contained high apparent provenance values but low source integrity and low cross-evidence consistency.

The result confirms:

```text
single Evidence match
!=
criterion update acceptance
```

and:

```text
high average evidence appearance
cannot compensate for a critical source-integrity failure
```

---

## 11. Result Summary

| Scenario | Model | Final center | Final width | Freeze stage | Attack reference admissible | Final state |
|---|---:|---:|---:|---:|---:|---|
| N1 | U | 0.24808 | 0.120000 | — | No | ADAPTING |
| N1 | G | 0.23400 | 0.120000 | — | No | STABLE |
| P1 | U | 0.3969728 | 0.277212 | — | **Yes** | ADAPTING |
| P1 | G | 0.20000 | 0.120000 | 2 | **No** | FROZEN |
| C1 | U | 0.23280 | 0.120000 | — | No | ADAPTING |
| C1 | G | 0.20000 | 0.120000 | 1 | No | FROZEN |

---

## 12. Verified Assertions

All seven executable assertions passed.

```text
PASS N1 guarded model eventually accepts supported adaptation
PASS P1 unconstrained model makes attack reference admissible
PASS P1 guarded model freezes criterion adaptation
PASS P1 guarded model keeps attack reference non-admissible
PASS C1 guarded model does not accept compromised source update
PASS C1 guarded model freezes or reviews
PASS Auth Decision and Criterion Update Response remain separate
```

---

## 13. What the PoC Demonstrates

The implemented PoC demonstrates, under its declared deterministic assumptions, that:

1. A dynamic criterion can accept legitimate Context-relative adaptation.
2. Candidate generation can remain common while adoption policy differs.
3. Direct candidate adoption can cause cumulative criterion expansion.
4. A guarded model can stop adaptation before the attack reference becomes admissible.
5. A compromised Evidence source can block criterion adaptation even when another Evidence value appears valid.
6. `AUTH_STABLE + FREEZE` is an executable state combination.
7. Subject evaluation and criterion-integrity evaluation can remain separate.

The central proposition is therefore executable in the minimum model:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 14. What the PoC Does Not Demonstrate

The PoC does not establish:

```text
complete prevention of criterion poisoning
universal detection of credential theft
universal detection of relay attacks
security when all Evidence sources are compromised
security when rollback integrity is compromised
real-world false-accept or false-reject rates
production performance
privacy guarantees
formal proof of correctness
statistical generalization
```

The scenario inputs and coefficients are synthetic and deterministic.

The PoC is evidence that the proposed state-transition structure is executable and behaviorally distinguishable. It is not evidence that the selected coefficients are optimal or production-ready.

---

## 15. Implementation Limitations

### 15.1 One-dimensional criterion

The criterion center and width are scalar. Production GyroAuth would require multidimensional state and relation representations.

### 15.2 Reduced trajectory proxy

Trajectory Continuity is represented by a deterministic proxy. It does not replace the broader relational definition.

### 15.3 Simplified discrimination reference

Discrimination preservation uses one attack reference point. Future work should include multiple attack classes or distributions.

### 15.4 Minimal rollback path

The implementation retains a rollback point and implements `ROLLBACK`, but the required scenarios primarily demonstrate `DEFER`, `ACCEPT`, and `FREEZE`.

A dedicated confirmed-contamination scenario should exercise rollback in the next extension.

### 15.5 No resource benchmark

CPU, memory, storage, energy, sampling frequency, and history compression are not measured in this PoC.

---

## 16. Reproducibility

The implementation is reproducible because:

```text
no randomness is used
all coefficients are explicit
all scenario inputs are versioned
all outputs are JSON serializable
the script returns non-zero when an assertion fails
```

Any coefficient change should be treated as a new experiment and should regenerate the result file.

---

## 17. Priority H Completion Status

Priority H is complete at the minimum PoC level.

```text
Implementation: complete
Deterministic execution: complete
Required scenarios: complete
Assertions: 7 / 7 passed
Production validation: not complete
Formal proof: not complete
```

---

## 18. Preparation for Priority I

Priority I should convert these results into a Security Claims and Limitations matrix.

It should distinguish:

```text
Demonstrated by this PoC
Conditionally supportable
Not yet demonstrated
Explicitly not guaranteed
```

Claims must remain bounded by:

```text
Threat Model
Trusted Assumptions
Synthetic Scenario Scope
Guard Configuration
Rollback Integrity
Evidence-source Integrity
```

Recommended next document:

```text
docs/23_security_claims_and_limitations.md
```

---

## 19. Layer Consistency

```text
Gyro Logic Core change: none
GyroOS contract change: none
GyroAuth simulation implementation: added
```

Only the `gyroauth` repository is updated by this Priority.
