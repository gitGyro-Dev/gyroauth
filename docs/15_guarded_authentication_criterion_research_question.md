# Guarded Authentication Criterion — Research Question and Contribution

## 1. Purpose

This document begins Priority A of the GyroAuth formalization and paper-preparation work.

The purpose is to fix the research problem, proposed contribution, novelty boundary, evaluation direction, and relation to the existing GyroAuth publications before constructing the terminology, threat model, formal security model, state machine, and simulation.

This document is a research-position document. It does not yet claim a completed security proof or empirical validation.

---

## 2. Existing GyroAuth Foundation

The existing GyroAuth foundation remains unchanged:

```text
Authentication
=
Stability-based Selection over State Convergence
```

GyroAuth interprets GyroOS execution results for authentication decisions.

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Application
```

This study does not redefine the Gyro Logic Core:

```text
Structure
↓
Slice
↓
Stability
```

It also does not redefine the GyroOS runtime or canonical Operator Response.

The present study is limited to the GyroAuth application layer.

---

## 3. Problem Statement

Adaptive and continuous authentication systems must respond to legitimate change.

A user may:

```text
change devices
change networks
travel
change roles
perform emergency operations
change long-term behavior
```

Therefore, an authentication criterion cannot always remain a fixed profile or a fixed threshold.

However, adaptation creates a second attack surface.

If observations are incorporated into the authentication criterion without sufficient constraints, an attacker may gradually move, broaden, or contaminate the criterion until malicious behavior is treated as normal.

```text
dynamic criterion
!=
unconstrained self-update
```

The problem is not only whether the current Access Subject remains admissibly related to the expected Identity.

The system must also ask whether the criterion used to evaluate that relation remains appropriate.

```text
Subject Question:

Is the current Access Subject still admissibly related
to the expected Identity?
```

```text
Criterion Question:

Is the current authentication criterion still admissible
as a basis for evaluating that relation?
```

---

## 4. Research Question

### 4.1 Primary Research Question

> How can an adaptive authentication system update a context-relative authentication criterion while preventing observed behavior from being incorporated as a new normal without sufficient evidence, traceability, and stability?

### 4.2 GyroAuth-specific Research Question

> How can GyroAuth represent authentication-criterion change as a guarded trajectory whose admissibility, traceability, and stability are continuously evaluated separately from the current authentication decision?

### 4.3 Operational Research Question

> Under what conditions should a proposed criterion update be accepted, deferred, frozen, reviewed, or rolled back while the current authentication relation is evaluated independently?

---

## 5. Central Hypothesis

The central hypothesis is:

> Authentication-criterion change should not be treated as an automatic profile update. It should be treated as a trajectory of criterion states whose transitions must themselves remain admissible, traceable, and stable.

Provisional expression:

```text
Observed Access Trajectory
        ↓
Criterion Update Candidate
        ↓
Criterion Integrity Evaluation
        ↓
ACCEPT / DEFER / FREEZE / REVIEW / ROLLBACK
```

The update candidate is not automatically the next criterion.

```text
Update Candidate
!=
Accepted Criterion
```

---

## 6. Proposed Contribution

The proposed contribution is a criterion-aware extension of GyroAuth consisting of the following elements.

### 6.1 Dual Continuous Evaluation

GyroAuth evaluates two related but distinct objects:

```text
1. Subject Evaluation
2. Criterion Integrity Evaluation
```

Subject Evaluation concerns whether the current authentication relation may continue.

Criterion Integrity Evaluation concerns whether the criterion and its update process remain usable as the basis for that decision.

```text
Subject Evaluation Loop
        ↕
Criterion Integrity Loop
```

The structural recurrence is fractal-like, while runtime execution must remain bounded.

### 6.2 Separation of Decisions

The authentication decision and criterion-update response are distinct.

```text
Auth Decision
!=
Criterion Update Response
```

Auth Decision candidates:

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

Criterion Update Response candidates:

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

This separation permits states such as:

```text
AUTH_STABLE + FREEZE
```

The current access relation may continue while criterion adaptation is suspended.

### 6.3 Guarded Criterion Update

Let the current criterion be:

```text
A_t
```

Let an update process produce a candidate:

```text
A*_(t+1) = U(A_t, T_obs_t, C_(t+1), E_t)
```

The candidate is evaluated before adoption:

```text
G_t = Guard(A_t, A*_(t+1), T_obs_t, C_(t+1), E_t, H_t)
```

The next criterion is selected through a Criterion Update Response rather than direct assignment.

```text
A_(t+1) =

A*_(t+1)   when response = ACCEPT
A_t        when response = DEFER / FREEZE / REVIEW
A_tau      when response = ROLLBACK, tau < t
```

This is a provisional schema, not yet a final equation.

### 6.4 Criterion Trajectory

A criterion is not treated as one fixed profile.

Its change history must preserve information about:

```text
why the update occurred
which evidence supported it
how far and how fast it moved
which direction it moved
whether discrimination was preserved
whether rollback remains possible
```

Therefore:

```text
Criterion History
!=
Criterion Trajectory
```

A Criterion Trajectory is the readable relational configuration through which criterion changes can be traced as admissible or inadmissible updates.

### 6.5 Criterion Integrity

Provisional definition:

> Criterion Integrity is the condition in which the authentication criterion and its update process remain admissible and traceable as a basis for evaluating the authentication relation to the expected Identity.

Criterion Integrity does not mean that GyroAuth proves its own trustworthiness without assumptions.

It means that the criterion and update process are included in the evaluation scope and are checked against protected anchors, evidence provenance, update history, and response rules.

---

## 7. Expected Novelty

The expected novelty is not merely continuous authentication or adaptive risk scoring.

The intended distinction is:

```text
Conventional adaptive model:
observations
→ profile or threshold update
→ future evaluation
```

```text
Proposed GyroAuth model:
observations
→ update candidate
→ criterion-trajectory evaluation
→ guarded update response
→ accepted / deferred / frozen / reviewed / rolled-back criterion
```

The proposed model treats criterion adaptation itself as an authentication-relevant trajectory and attack surface.

The novelty claim remains provisional until related-work review is completed against:

```text
Adaptive Authentication
Continuous Authentication
Risk-Based Authentication
Behavioral Biometrics
Online Learning
Concept Drift
Data Poisoning
Model Poisoning
Zero Trust
UEBA
Anomaly Detection
```

---

## 8. Relation to Previous GyroAuth Work

### 8.1 Primary GyroAuth Paper

The primary paper defines the foundational authentication model:

```text
Authentication
=
Stability-based Selection over State Convergence
```

The present study does not replace that model.

It specifies how the criterion used by Stability-based Selection may adapt without becoming an unconstrained profile update.

### 8.2 Trajectory-Based Vulnerability Response

The vulnerability-response paper applies trajectory evaluation to post-login operations and security response.

```text
Primary GyroAuth Model
        ↓
Continuous Evaluation
        ↓
Trajectory-Based Vulnerability Response
```

The present study has a different primary target:

```text
Authentication Criterion
and
Criterion Update Process
```

It studies whether the measurement and selection basis remains trustworthy enough to continue being used.

### 8.3 Intended Dependency

```text
Primary GyroAuth Paper
        ↓
Criterion Integrity and Guarded Adaptation Study
        ↓
Trajectory-Based Detection and Response Applications
```

This dependency is conceptual. It does not alter repository or layer ownership.

---

## 9. Evaluation Direction

The initial evaluation should compare at least two models.

### 9.1 Unconstrained Update Model

```text
A_(t+1) = U(A_t, X_t)
```

Observed behavior is incorporated without an independent criterion-integrity decision.

### 9.2 Guarded Update Model

```text
A*_(t+1) = U(A_t, X_t)

A_(t+1) = Transition(
  A_t,
  A*_(t+1),
  Guard_t,
  CriterionUpdateResponse_t
)
```

### 9.3 Minimum Comparison Scenarios

#### Normal Context Change

```text
known device
→ new device
→ deviation increase
→ successful re-authentication
→ cross-evidence consistency
→ controlled adaptation
→ ACCEPT
```

#### Gradual Criterion Poisoning

```text
small malicious deviation
→ repeated sub-threshold deviation
→ candidate-region expansion
→ discrimination decline
→ DEFER / FREEZE / REVIEW / ROLLBACK
```

### 9.4 Candidate Evaluation Measures

```text
criterion drift distance
attack incorporation rate
time to defer
time to freeze
time to rollback
false rejection during legitimate adaptation
false acceptance after poisoning
recovery time
discrimination preservation
```

The first PoC may use synthetic, discrete-time data. Real-world datasets are not required for the initial proof of concept, but later empirical validation will be necessary for stronger claims.

---

## 10. Initial Security Claim Boundary

The intended model may support conditional claims such as:

```text
criterion updates are not automatically adopted
subject evaluation and criterion evaluation are separated
suspicious gradual drift can trigger guarded responses
trusted rollback points can support recovery
normal context change and poisoning can be represented as different trajectories
```

The study does not initially claim:

```text
complete prevention of criterion poisoning
detection of every credential theft or relay attack
zero false acceptance
zero false rejection
security when all evidence sources are compromised
security when protected anchors or rollback points are compromised
perfect identification of a human individual
complete self-verification by GyroAuth
```

Claims must remain conditional on the threat model, trusted assumptions, implementation, and observed evidence.

---

## 11. Scope Boundaries

This study includes:

```text
adaptive authentication criterion
criterion update candidates
criterion trajectory
criterion integrity
guarded update responses
normal adaptation versus poisoning
minimal simulation or PoC
security claims and limitations
```

This study does not yet include:

```text
full production deployment
complete GyroOS implementation
hardware resource optimization
universal biometric modeling
proof against unrestricted attackers
real-world performance guarantees
privacy-preserving implementation details
```

CPU, memory, storage, energy use, sampling policy, and history compression are important implementation topics but are deferred until the formal model and minimum PoC are stable.

---

## 12. Priority A Outputs

Priority A fixes the following working position.

### Research Problem

Adaptive authentication criteria are necessary for legitimate change but can become an attack surface when observations are incorporated without guarded evaluation.

### Research Question

How can GyroAuth adapt its authentication criterion while separately and continuously evaluating whether the criterion and its update trajectory remain admissible, traceable, and stable?

### Proposed Method

```text
Dual Continuous Evaluation
+
Criterion Trajectory
+
Criterion Integrity
+
Guarded Criterion Update
+
Separated Auth Decision and Criterion Update Response
```

### Expected Contribution

A formal and executable model in which authentication-criterion changes are proposed, evaluated, accepted, deferred, frozen, reviewed, or rolled back rather than automatically incorporated.

### Evaluation

A minimum comparison between legitimate context adaptation and gradual criterion poisoning, with guarded and unguarded update models.

### Claim Boundary

The model aims to improve detectability, update control, and recoverability under explicit assumptions. It does not claim absolute prevention or perfect identification.

---

## 13. Next Priority

The next step is:

```text
Priority B
Formal Terminology and Scope
```

Priority B should determine:

```text
which terms are formal objects
which terms are explanatory only
symbol assignments
state variables
responsibility boundaries
terms intentionally not adopted
```

The definitions in this document remain working definitions until reviewed and fixed in Priority B.

---

## 14. Repository and Layer Constraints

This document belongs to:

```text
gitGyro-Dev/gyroauth
```

References to Gyro Logic or GyroOS may be used for consistency checks.

This work must not update the `gyrologic` or `gyroos` repositories from the GyroAuth thread.

```text
Core change: none
GyroOS contract change: none
GyroAuth research scope: expanded
```
