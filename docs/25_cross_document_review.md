# Guarded Criterion Trajectories — Cross-document Review

## 1. Purpose

This document completes the cross-document review portion of **Priority K: Cross-document Review, Related Work, Figures, and Submission Refinement**.

Reviewed artifacts:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
docs/18_formal_security_model.md
docs/19_criterion_update_state_machine.md
docs/20_normal_and_poisoned_update_scenarios.md
docs/21_minimal_simulation_design.md
docs/22_poc_implementation_and_results.md
docs/23_security_claims_and_limitations.md
docs/24_paper_outline.md
paper/guarded_criterion_trajectories_full_en.md
paper/guarded_criterion_trajectories_full_jp.md
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

The review checks terminology, notation, layer ownership, threat assumptions, state semantics, PoC-result consistency, claim boundaries, English/Japanese alignment, and submission readiness.

---

## 2. Review Result

Overall result:

```text
Conceptual consistency:        PASS
Layer consistency:             PASS
Decision separation:           PASS
Threat-to-model traceability:  PASS
PoC-to-claim traceability:     PASS WITH LIMITATIONS
English/Japanese alignment:    PASS WITH EDITORIAL REFINEMENT
Related-work completeness:     PARTIAL
Figure readiness:              PARTIAL
Submission readiness:          NOT YET FINAL
```

The central research position remains coherent across the artifacts:

```text
dynamic criterion
!=
unconstrained self-update
```

and:

```text
Criterion Update Candidate
!=
Accepted Criterion
```

and:

```text
Auth Decision
!=
Criterion Update Response
```

No contradiction was found that requires changing the Gyro Logic Core or the GyroOS execution contract.

---

## 3. Invariant and Layer Review

### 3.1 Gyro Logic Core

The reviewed documents consistently preserve:

```text
Structure
→ Slice
→ Stability
```

The new terms are GyroAuth application-layer terms. They do not redefine `Structure`, `Slice`, `Stability`, Trajectory in Gyro Logic, or the canonical GyroOS Operator Response.

### 3.2 Layer ownership

```text
Gyro Logic = theory
GyroOS     = execution system
GyroAuth   = authentication application
```

The following remain GyroAuth-owned:

```text
Authentication Criterion
Criterion State
Criterion Update Candidate
Criterion Integrity
Criterion Update Response
Auth Decision
```

### 3.3 Required wording

The manuscript should continue to state:

```text
Core change: none
GyroOS contract change: none
GyroAuth application model: expanded
```

---

## 4. Terminology Review

### 4.1 Terms confirmed as stable

The following terms are consistently used and are ready for manuscript use:

```text
Access Subject
Expected Identity
Observed Evidence
Observed Access Trajectory
Authentication Relation
Authentication Relation Continuity
Authentication Criterion
Criterion State
Criterion Update Candidate
Criterion Trajectory
Criterion Integrity
Auth Decision
Criterion Update Response
Trusted Anchor
Rollback Point
Guard
```

### 4.2 Terms requiring disciplined use

#### Identity

Use `Expected Identity` in formal evaluation passages. Use `Identity` alone only when discussing the broader GyroAuth concept.

#### Trajectory

Do not reduce Trajectory to an event list, chronological history, or feature-vector sequence.

```text
History
!=
Trajectory
```

#### Criterion

Do not describe the Authentication Criterion as a conventional fixed behavioral profile. The minimum PoC uses a center and width only as an executable abstraction.

#### Integrity

`Criterion Integrity` must not be written as self-certification. It depends on external or protected anchors, provenance, retained history, and rollback linkage.

### 4.3 Explanatory language

The following may appear only as intuition and must be mapped to formal values:

```text
unease
wobble
thickness
feels different
```

Formal replacements include:

```text
deviation direction
deviation rate
deviation spread
deviation persistence
recovery tendency
cross-evidence inconsistency
```

---

## 5. Notation Review

### 5.1 Effective and candidate criteria

Use consistently:

```text
A_t         = effective Authentication Criterion at stage t
A*_(t+1)    = Criterion Update Candidate
Q_t         = Criterion State
D_auth_t    = Auth Decision
D_crit_t    = Criterion Update Response
G_t         = Guard result
T_t^obs     = Observed Access Trajectory
```

### 5.2 Access Subject symbol collision

Earlier working expressions occasionally used `A` for an Access Subject while `A_t` is also used for the Authentication Criterion.

Submission rule:

```text
s_t = Access Subject reference
A_t = Authentication Criterion
```

Do not use `A_t^subject` in the final manuscript.

### 5.3 Candidate transition

The canonical submission expression should be:

```text
A*_(t+1) = U(A_t, T_t^obs, C_(t+1), E_t, H_t)
```

```text
G_t = Guard(A_t, A*_(t+1), T_t^obs, C_(t+1), E_t, H_t, P_t)
```

```text
D_crit_t = Pi_crit(G_t, Q_t, H_t)
```

```text
A_(t+1) = A*_(t+1)  if D_crit_t = ACCEPT
A_(t+1) = A_t       if D_crit_t ∈ {DEFER, FREEZE, REVIEW}
A_(t+1) = A_tau     if D_crit_t = ROLLBACK and tau < t
```

### 5.4 Scalar summary warning

A scalar Criterion Integrity score is permitted only for visualization.

```text
scalar integrity summary
!=
complete Guard semantics
```

Critical Guard failures must remain non-compensable.

---

## 6. Threat Model Review

### 6.1 Primary evaluated threat

The implemented PoC primarily evaluates:

```text
P1: gradual region-expansion criterion poisoning
```

### 6.2 Additional modeled but unimplemented threats

```text
criterion translation
evidence-priority poisoning
recovery-expectation poisoning
challenge weakening
context-rule poisoning
history-window poisoning
rollback-link poisoning
slow contraction
response-policy poisoning
```

The manuscript must not imply that these threats were experimentally evaluated.

### 6.3 Trust assumption

The minimum assumption is internally consistent:

> At least one independent Evidence source, protected anchor, intact audit linkage, or verified rollback point remains outside simultaneous attacker control.

This is a disjunctive minimum assumption for the model, not a claim that any one artifact is sufficient in every deployment.

### 6.4 Total compromise

The following remains explicitly outside supported security claims:

```text
all Evidence sources compromised
all protected anchors compromised
all rollback points compromised
runtime implementation compromised
perfect attacker reproduction of all relevant relations
```

---

## 7. State Machine Review

### 7.1 Criterion states

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

### 7.2 Criterion Update Responses

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

### 7.3 Semantic distinctions

```text
DEFER
= insufficient support for the current candidate
```

```text
FREEZE
= the adaptive update path is considered unsafe
```

```text
REVIEW
= decision authority or validation path is transferred
```

```text
ROLLBACK
= a verified prior criterion is restored without deleting history
```

### 7.4 Editorial refinement

`ROLLED_BACK` is a Criterion State; `ROLLBACK` is a response. The manuscript must preserve this grammatical distinction.

### 7.5 Bounded execution

The conceptual recurrence may be described as recursive or fractal-like, but the implementation must be described as bounded. Avoid language suggesting an infinite self-verification loop.

---

## 8. PoC and Result Review

### 8.1 Artifact consistency

The manuscript, PoC report, and result summary consistently report:

#### N1 guarded model

```text
Criterion response:
DEFER → ACCEPT → ACCEPT

final mu    = 0.234
final width = 0.120
```

#### P1 direct-update baseline

```text
final mu    = 0.3969728
final width = 0.277212
attack reference admissible = true
```

#### P1 guarded model

```text
final mu    = 0.200
final width = 0.120
freeze stage = 2
attack reference admissible = false
```

#### C1 guarded model

```text
FREEZE → FREEZE
final mu    = 0.200
final width = 0.120
```

### 8.2 Required interpretation

The most important executable result remains:

```text
AUTH_STABLE + FREEZE
```

Interpretation:

```text
current access continuation
!=
permission to redefine future acceptance
```

### 8.3 Result wording

Use:

> Under the implemented deterministic P1 scenario, the guarded model froze adaptation before the configured attack reference became admissible.

Do not use:

> The model prevents criterion poisoning.

### 8.4 Baseline wording

Model U is an intentionally unsafe control baseline. It must not be presented as a complete representation of existing adaptive-authentication systems.

---

## 9. Claim Review

### 9.1 Structurally demonstrated

The following claims remain supported by the current PoC:

```text
candidate/adoption separation is executable
decision-stream separation is executable
bounded supported adaptation can be accepted
direct candidate adoption can accumulate criterion drift
P1 adaptation can be frozen before configured attack-reference admission
C1 compromised-source updates can be blocked
AUTH_STABLE + FREEZE is executable
```

### 9.2 Conditional

```text
criterion-poisoning containment beyond P1
rollback-supported recovery
credential-theft resistance
session-hijacking detection
relay-attack detection
multi-source compromise resistance
```

### 9.3 Unsupported

```text
universal attack detection
complete prevention of poisoning
zero false acceptance
zero false rejection
perfect identity proof
formal correctness proof
statistical generalization
production performance
privacy guarantee
```

---

## 10. English/Japanese Alignment Review

The English and Japanese manuscripts have equivalent section order, contribution structure, formal model, PoC results, claims, limitations, and conclusion.

Editorial rules for the submission pair:

1. Keep formal symbols identical.
2. Keep state and response identifiers in English monospace.
3. Translate prose, not identifiers.
4. Use `Criterion poisoning` consistently; avoid alternating between unrelated Japanese translations.
5. Use `Guard付き` consistently in Japanese.
6. Preserve the same conditional qualifiers in both languages.
7. Keep numerical results identical.
8. Keep reference numbering identical.

---

## 11. Issues Requiring Correction Before Submission

### Required

```text
R1 Add completed Related Work section.
R2 Replace reference placeholders with a numbered bibliography.
R3 Add figure references and captions.
R4 Add a table comparing adjacent research areas and the proposed scope.
R5 Add a table separating supported, conditional, and unsupported claims.
R6 Ensure all equations use one notation set.
R7 Remove statements saying Related Work is incomplete after it is inserted.
R8 Confirm all PoC values directly from the committed result artifact.
R9 Perform English/Japanese paragraph-level correspondence review.
R10 Format title page, author information, affiliations, and disclosure for the submission venue.
```

### Recommended

```text
E1 Add a rollback execution scenario before making recovery claims.
E2 Add sensitivity analysis before discussing threshold robustness.
E3 Add a multidimensional scenario before claiming general authentication coverage.
E4 Add a reproducibility appendix with exact command and environment.
E5 Add a machine-readable result table generated from the PoC output.
```

---

## 12. Final Review Position

The Priority A–J artifacts form a coherent research package. The central contribution is now sufficiently stable for a new paper:

> Authentication-criterion adaptation is represented as a guarded, traceable trajectory, and authorization to change future criteria is evaluated separately from the decision to continue the current authentication relation.

The current work is suitable for manuscript refinement and preprint preparation, but the submission should remain labeled as a structural, executable proof of concept rather than a production security validation.

```text
Cross-document review: complete
Conceptual contradiction requiring redesign: none
Submission refinement still required: yes
```
