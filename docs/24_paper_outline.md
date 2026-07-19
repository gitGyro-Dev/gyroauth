# Guarded Criterion Trajectories for Adaptive Authentication — Paper Outline

## 1. Purpose

This document completes the outline portion of **Priority J: Paper Outline and Manuscript** for the GyroAuth formalization and paper-preparation work.

It integrates the results of:

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
```

The paper is intended as a new GyroAuth study rather than a revision of the foundational GyroAuth paper.

---

## 2. Working Title

### Primary title

> **Guarded Criterion Trajectories for Adaptive Authentication: Separating Current Access Decisions from Future Criterion Updates**

### Short title

> **Guarded Criterion Trajectories for Adaptive Authentication**

### Japanese working title

> **適応型認証におけるGuard付きCriterion Trajectory：現在のアクセス判断と将来の認証基準更新の分離**

---

## 3. Central Research Position

The paper is organized around the following proposition:

```text
dynamic criterion
!=
unconstrained self-update
```

Adaptive authentication requires criteria to change under legitimate Context transitions. However, observations must not be incorporated automatically as a new normal merely because they are repeatedly observed.

The proposed model therefore separates:

```text
Current authentication decision
```

from:

```text
Permission to change future authentication criteria
```

This separation is formalized as:

```text
Auth Decision
!=
Criterion Update Response
```

and:

```text
Criterion Update Candidate
!=
Accepted Criterion
```

---

## 4. Research Question

### Primary question

> How can an adaptive authentication system update a Context-relative criterion while preventing repeatedly observed or compromised behavior from being incorporated as a new normal without sufficient evidence, traceability, and stability?

### GyroAuth-specific question

> How can GyroAuth represent authentication-criterion change as a guarded trajectory whose admissibility, traceability, and stability are evaluated separately from the current authentication decision?

### Operational question

> Under what conditions should a proposed criterion update be accepted, deferred, frozen, reviewed, or rolled back?

---

## 5. Proposed Contributions

The manuscript should present the following contributions.

### C1. Dual continuous evaluation

GyroAuth evaluates two related but distinct objects:

```text
Subject Evaluation
Criterion Integrity Evaluation
```

### C2. Candidate-adoption separation

A proposed criterion is not automatically the next effective criterion.

```text
A*_(t+1)
!=
A_(t+1)
```

### C3. Guarded criterion trajectory

Criterion changes are represented as a traceable trajectory of criterion states, update causes, evidence provenance, transition magnitude, transition direction, discrimination effects, responses, and rollback links.

### C4. Independent decision streams

The model defines:

```text
Auth Decision:
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

and separately:

```text
Criterion Update Response:
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

### C5. Executable minimum comparison

A deterministic PoC compares:

```text
Model U: direct candidate adoption
Model G: guarded candidate adoption
```

under legitimate adaptation, gradual criterion poisoning, and single-source Evidence compromise.

### C6. Explicit claim boundary

The study distinguishes structural demonstration from production security validation and states its assumptions and non-guarantees.

---

## 6. Paper Structure

## 6.1 Abstract

The abstract should contain five elements:

1. Adaptive authentication requires criteria to change.
2. Criterion adaptation creates a poisoning surface.
3. The paper proposes guarded criterion trajectories and separated decision streams.
4. A deterministic PoC compares unconstrained and guarded updates.
5. The result is a structural demonstration, not a production security guarantee.

Target length:

```text
180–250 words
```

---

## 6.2 Introduction

### Problem

A fixed criterion cannot accommodate all legitimate device, network, role, location, and behavioral changes.

### Risk

Directly incorporating observations into the criterion allows gradual movement, expansion, weakening, or contamination of the future acceptance basis.

### Gap

The authentication decision and criterion-update authorization are often operationally coupled or insufficiently distinguished.

### Proposal

Treat criterion change as a guarded trajectory and evaluate its integrity independently.

### Contributions

List C1–C6.

---

## 6.3 Background and Positioning

### GyroAuth foundation

```text
Authentication
=
Stability-based Selection over State Convergence
```

### Layer relationship

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Authentication Application
```

### Relation to previous work

```text
Foundational GyroAuth paper
→ base authentication model

Trajectory-Based Vulnerability Response
→ post-login operation and response application

Present study
→ integrity of the adaptive authentication criterion itself
```

### Related-work categories requiring literature review

```text
Adaptive Authentication
Continuous Authentication
Risk-Based Authentication
Behavioral Biometrics
Concept Drift
Online Learning Security
Data Poisoning
Model Poisoning
Zero Trust
UEBA
Anomaly Detection
```

No novelty claim should be finalized until the related-work review is completed.

---

## 6.4 Terminology and Model Scope

Define at minimum:

```text
Access Subject
Expected Identity
Session
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
```

Important distinctions:

```text
Access Subject != Verified Identity
Evidence != Identity
History != Trajectory
Session continuity != Authentication Relation Continuity
Criterion Update Candidate != Accepted Criterion
Auth Decision != Criterion Update Response
```

---

## 6.5 Threat Model

### Protected objects

```text
Authentication Relation
Authentication Criterion
Criterion Update Process
Criterion Trajectory
Trusted History
Rollback Points
Decision separation
```

### Main threats

```text
Credential theft
Session hijacking
Relay attack
Gradual behavioral mimicry
Criterion poisoning
Evidence-source compromise
Multi-source coordinated compromise
```

### Criterion poisoning subtypes

```text
Region expansion
Criterion translation
Evidence-priority poisoning
Recovery-expectation poisoning
Challenge weakening
Context-rule poisoning
History-window poisoning
Rollback-link poisoning
Slow contraction
Response-policy poisoning
```

### Trust assumption

At least one independent Evidence source, protected anchor, audit linkage, or verified rollback point remains outside simultaneous attacker control.

---

## 6.6 Formal Security Model

### Discrete stages

```text
t = 0, 1, 2, ...
```

### Effective criterion

```text
A_t
```

### Candidate criterion

```text
A*_(t+1)
=
U(A_t, T_t^obs, C_(t+1), E_t, H_t)
```

### Guard

```text
G_t
=
Guard(A_t, A*_(t+1), T_t^obs, C_(t+1), E_t, H_t, P_t)
```

### Criterion response

```text
D_crit_t
=
Pi_crit(G_t, Q_t, H_t)
```

### Effective transition

```text
A_(t+1) = A*_(t+1)   when ACCEPT
A_(t+1) = A_t        when DEFER / FREEZE / REVIEW
A_(t+1) = A_tau      when ROLLBACK, tau < t
```

### Non-compensation rule

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

---

## 6.7 Criterion Update State Machine

Criterion States:

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

Criterion Update Responses:

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

Clarify:

```text
DEFER
= insufficient evidence for one candidate

FREEZE
= suspension of the adaptive update path

REVIEW
= transfer to an external or stronger decision path

ROLLBACK
= restoration of a verified prior criterion
```

---

## 6.8 Scenarios

### N1. Legitimate new-device transition

Expected:

```text
REAUTH_REQUIRED
→ AUTH_STABLE

DEFER
→ ACCEPT
```

### P1. Gradual region-expansion poisoning

Model U:

```text
direct adoption
→ cumulative expansion
→ attack reference becomes admissible
```

Model G:

```text
DEFER
→ FREEZE
→ trusted criterion preserved
```

### C1. Single Evidence-source compromise

Expected:

```text
single Evidence match
!=
criterion update acceptance
```

---

## 6.9 PoC Implementation

Artifacts:

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

Implementation characteristics:

```text
Python standard library only
deterministic
synthetic inputs
discrete stages
one-dimensional criterion abstraction
explicit coefficients
seven executable assertions
```

---

## 6.10 Results

### N1

Guarded adaptation accepted after challenge confirmation and cross-evidence support.

```text
final mu    = 0.234
final width = 0.120
```

### P1 Model U

```text
final mu    = 0.3969728
final width = 0.277212
attack reference admissible = true
```

### P1 Model G

```text
final mu    = 0.200
final width = 0.120
freeze stage = 2
attack reference admissible = false
```

Required result:

```text
AUTH_STABLE + FREEZE
```

### C1 Model G

```text
FREEZE
→ FREEZE

final mu    = 0.200
final width = 0.120
```

All seven implemented assertions passed.

---

## 6.11 Discussion

### Main interpretation

The current access relation and permission to redefine future acceptance can be evaluated separately.

### Why AUTH_STABLE + FREEZE matters

The current relation may remain temporarily continuable while adaptive criterion adoption is suspended.

### Why the model is not non-adaptive

Legitimate, bounded, supported change can still be accepted.

### Why the model is not self-certifying

Criterion Integrity depends on protected anchors, provenance, independent Evidence, history, and rollback assumptions.

### Relation to Gyro concepts

The criterion update is handled as a GyroAuth application-layer trajectory without modifying the Gyro Logic Core or canonical GyroOS Operator Response.

---

## 6.12 Security Claims and Limitations

### Structurally demonstrated

```text
candidate-adoption separation
decision-stream separation
guarded bounded adaptation
freezing before attack-reference admission in P1
blocking adaptation under C1
AUTH_STABLE + FREEZE
```

### Conditional

```text
criterion-poisoning containment
rollback-supported recovery
credential-theft resistance
session-hijacking detection
relay-attack detection
```

### Not established

```text
complete prevention of criterion poisoning
zero false acceptance
zero false rejection
universal attacker detection
security under total Evidence and anchor compromise
production performance
privacy guarantees
formal proof of correctness
statistical generalization
```

---

## 6.13 Conclusion

The conclusion should restate:

```text
Adaptive criterion change is necessary.
Automatic adoption is unsafe.
Criterion change should be proposed, traced, guarded, and responded to independently.
```

The paper should close with the central proposition:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 7. Figures and Tables

### Figure 1

GyroAuth layer and decision separation.

```text
Observed Access Trajectory
        ├── Subject Evaluation ──> Auth Decision
        └── Criterion Evaluation ──> Criterion Update Response
```

### Figure 2

Guarded criterion-update pipeline.

```text
Observation
→ Candidate
→ Guard
→ Response
→ Effective Criterion
```

### Figure 3

Criterion Update State Machine.

### Figure 4

P1 comparison of Model U and Model G.

Recommended axes:

```text
stage
criterion center
criterion width
attack reference
freeze point
```

### Table 1

Formal terminology and distinctions.

### Table 2

Threat classes and expected responses.

### Table 3

Scenario results.

### Table 4

Security claims, assumptions, evidence level, and limitations.

---

## 8. Manuscript Policy

The first manuscript is a complete working draft, but the following sections remain explicitly provisional until external literature review and publication-format review are completed:

```text
Related Work
Novelty comparison
Reference list
Statistical claims
Production-security implications
```

The manuscript must not use unsupported claims such as:

```text
GyroAuth prevents criterion poisoning
GyroAuth detects every attacker
GyroAuth proves identity
GyroAuth guarantees zero false acceptance
GyroAuth guarantees zero false rejection
```

---

## 9. Priority J Completion Criteria

Priority J is complete when the repository contains:

```text
1. This paper outline
2. A full English working manuscript
3. A full Japanese working manuscript
4. Explicit related-work placeholders
5. Explicit claim and limitation boundaries
6. Consistency with Priority A–I documents
```

After Priority J, the next work should be a cross-document and manuscript review rather than immediate submission.

---

## 10. Layer Consistency

```text
Gyro Logic Core change: none
GyroOS contract change: none
GyroAuth paper model: added
```

The manuscript may reference Gyro Logic and GyroOS, but it must not redefine them.