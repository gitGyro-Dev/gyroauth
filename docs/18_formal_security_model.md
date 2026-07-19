# GyroAuth Formal Security Model

## 1. Purpose

This document completes **Priority D: Formal Security Model** for the GyroAuth formalization and paper-preparation work.

It builds on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
```

Its purpose is to define a minimal formal model for:

```text
Subject Evaluation
Criterion Integrity Evaluation
Guarded Criterion Update
separated decisions
trusted rollback
normal adaptation
criterion poisoning
```

The model is intentionally discrete, bounded, and implementation-oriented.

It is not yet:

```text
a completed security proof
a production implementation contract
a universal identity model
a complete statistical learning model
a claim of attack prevention under unrestricted compromise
```

The formalization is designed to prepare:

```text
Priority E: Criterion Update State Machine
Priority F: Normal and Poisoned Update Scenarios
Priority G: Minimal Simulation Design
Priority H: PoC Implementation and Results
```

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

This document does not redefine:

```text
Structure
Slice
Stability
Gyro Process
GyroOS /loop/step
canonical GyroOS Operator Response
```

The model introduced here is a GyroAuth application-layer formalization.

```text
Core change: none
GyroOS contract change: none
GyroAuth formal model: expanded
```

---

## 3. Central Security Position

GyroAuth evaluates two related but distinct questions.

### 3.1 Subject Question

```text
Is the current Access Subject still admissibly related
to the Expected Identity?
```

### 3.2 Criterion Question

```text
Is the current Authentication Criterion still admissible
as a basis for evaluating that relation?
```

The resulting decisions are separate:

```text
Auth Decision
!=
Criterion Update Response
```

The central security position is:

```text
dynamic criterion
!=
unconstrained self-update
```

An observed change may produce a Criterion Update Candidate.
It does not automatically become the next effective criterion.

```text
Criterion Update Candidate
!=
Accepted Criterion
```

---

## 4. Time and Evaluation Stages

Let evaluation proceed in discrete stages:

```text
t = 0, 1, 2, ...
```

Each stage represents one bounded GyroAuth evaluation step.

A stage may correspond to:

```text
one /auth/step call
one bounded observation interval
one relevant security event
one challenge or re-authentication result
one criterion-update evaluation
```

The model does not require every stage to have equal physical duration.

```text
evaluation order
!=
fixed-rate sampling requirement
```

---

## 5. Sets and Domains

Let:

```text
S      = set of Access Subjects
I      = set of Expected Identities
C      = set of Contexts
E      = set of Evidence items or Evidence bundles
X      = set of interpreted authentication states
D      = Deviation space
K      = Stability result space
O      = GyroOS or mapped response-evidence space
A      = set of Authentication Criteria
Q      = set of Criterion States
H      = set of retained Histories
B      = set of Trusted Anchors
P      = set of Rollback Points
```

Let the Auth Decision set be:

```text
D_auth = {
  AUTH_STABLE,
  RECONVERGING,
  REAUTH_REQUIRED,
  AUTH_FAIL
}
```

Let the Criterion Update Response set be:

```text
D_crit = {
  ACCEPT,
  DEFER,
  FREEZE,
  REVIEW,
  ROLLBACK
}
```

These two decision spaces are not interchangeable.

---

## 6. Stage Inputs

At stage `t`, GyroAuth receives or derives:

```text
s_t       ∈ S     current Access Subject reference
i_t       ∈ I     Expected Identity reference
c_t       ∈ C     current Context
e_t       ∈ E     current Evidence bundle
x_t       ∈ X     interpreted authentication state
delta_t   ∈ D     local Deviation representation
k_t       ∈ K     Stability result
o_t       ∈ O     Operator Response or mapped response evidence
h_t       ∈ H     relevant retained History
a_t       ∈ A     currently effective Authentication Criterion
q_t       ∈ Q     current Criterion State
```

The model does not assume that all Evidence is equally trusted.

Each Evidence item may carry provenance metadata:

```text
prov(e) = (
  source,
  collection time,
  integrity status,
  trust class,
  Context,
  Slice reference
)
```

---

## 7. Local Authentication Realization

A Local Authentication Realization is provisionally represented as:

```text
l_t = (
  x_t,
  delta_t,
  k_t,
  o_t,
  c_t,
  h_t
)
```

where:

```text
x_t       = interpreted authentication state
delta_t   = local Deviation
k_t       = Stability result
o_t       = Operator Response or mapped response evidence
c_t       = current Context
h_t       = relevant History
```

This tuple is a GyroAuth-readable local result.

```text
{l_t}
!=
Observed Access Trajectory automatically
```

A collection of local results becomes a Trajectory only when admissible relations among them are traceable and readable under the current authentication conditions.

---

## 8. Observed Access Trajectory

Let:

```text
L_(0:t) = {l_0, l_1, ..., l_t}
```

be retained Local Authentication Realizations.

Let:

```text
R_(0:t)
```

be retained candidate relations among those realizations, such as:

```text
temporal relation
operational succession
causal relation
spatial relation
context-transition relation
challenge-response relation
privilege-transition relation
identity-reference relation
recovery relation
```

Let the authentication tracing conditions be:

```text
C_A,t = (Orientation_A, c_t, Slice_A,t)
```

Then the Observed Access Trajectory is provisionally represented as:

```text
T_t^obs
=
Read_A(
  Trace_(C_A,t)(L_(0:t), R_(0:t))
)
```

This is a structural schema rather than a conventional numerical equation.

The model preserves:

```text
History
!=
Trajectory
```

and:

```text
chronology
!=
continuity
```

---

## 9. Authentication Relation

Let the current Authentication Relation be:

```text
rho_t
=
Rel(s_t, i_t, Session_t, c_t)
```

The relation is the object selected for continuation.

```text
rho_t
!=
Access Subject
!=
Expected Identity
!=
Session
!=
Credential
```

GyroAuth does not claim to prove a complete metaphysical identity relation.

It evaluates whether the operational authentication relation remains continuable under current evidence, trajectory, criterion, and history.

---

## 10. Authentication Relation Continuity

Let:

```text
ARC(T_t^obs, i_t ; a_t, c_t)
```

be the predicate that the observed trajectory remains readable as a continuable authentication relation to the Expected Identity under the current criterion and Context.

A candidate schema is:

```text
ARC(T_t^obs, i_t ; a_t, c_t)
iff
Readable(T_t^obs ; c_t)
and
IdentityReferable(T_t^obs, i_t ; c_t)
and
Admissible(T_t^obs ; a_t, i_t, c_t)
```

This predicate does not require:

```text
no change
identical feature values
uninterrupted logging
one fixed path
all events individually valid
```

Therefore:

```text
valid events
!=
stable trajectory
```

and:

```text
valid Session
!=
continuable authentication relation
```

---

## 11. Deviation and Deviation Dynamics

Let the local multi-dimensional Deviation be:

```text
delta_t = (
  delta_t^device,
  delta_t^behavior,
  delta_t^time,
  delta_t^space,
  delta_t^network,
  delta_t^motion,
  delta_t^order,
  delta_t^privilege,
  delta_t^response
)
```

The exact dimensions are implementation-dependent.

The model does not reduce Deviation to one scalar too early.

Let the first difference be:

```text
v_t = delta_t - delta_(t-1)
```

Let the second difference be:

```text
u_t = v_t - v_(t-1)
```

Let an observation window be:

```text
W_t = {delta_(t-w+1), ..., delta_t}
```

Derived Deviation Dynamics may include:

```text
magnitude
change direction
change rate
acceleration
spread
persistence
recovery tendency
cross-evidence inconsistency
```

Provisionally:

```text
Dyn_t
=
Dyn(delta_t, v_t, u_t, W_t, h_t)
```

The intuitive term `unease` must be mapped to one or more components of `Dyn_t`.

```text
unease
!=
undefined intuition in the formal model
```

---

## 12. Authentication Criterion

Let the currently effective Authentication Criterion be:

```text
a_t ∈ A
```

A criterion may contain or reference:

```text
admissible state relations
admissible trajectory relations
Evidence priority
Context rules
Deviation tolerance
Trajectory envelope
recovery expectation
challenge requirements
update policy
protected anchors
rollback linkage
```

A criterion is not a fixed user profile.

```text
Authentication Criterion
!=
Fixed Identity Profile
```

A criterion may adapt, but its adaptation is guarded.

---

## 13. Criterion State

The current Criterion State is provisionally represented as:

```text
q_t = (
  a_t,
  c_t,
  p_t,
  z_t,
  b_t,
  pi_t,
  m_t
)
```

where:

```text
a_t  = currently effective criterion content
c_t  = current Context
p_t  = provenance state supporting the criterion
z_t  = criterion-integrity or criterion-stability state
b_t  = protected anchor linkage
pi_t = rollback-point linkage
m_t  = update-enabled mode
```

The update-enabled mode may later be represented as:

```text
ENABLED
DEFERRED
FROZEN
EXTERNAL_REVIEW
```

The exact state enumeration is reserved for Priority E.

---

## 14. Criterion Update Candidate

Let the update proposal function be:

```text
U : A × T × C × E × H → A
```

A Criterion Update Candidate is:

```text
a*_(t+1)
=
U(a_t, T_t^obs, c_(t+1), e_t^upd, h_t)
```

where:

```text
e_t^upd
```

is the Evidence selected as support for a possible criterion update.

The candidate is not yet effective.

```text
a*_(t+1)
!=
a_(t+1)
```

This separation is mandatory.

---

## 15. Criterion Update Delta

Let criterion change be represented by:

```text
Delta_t^crit
=
Diff_A(a_t, a*_(t+1))
```

`Delta_t^crit` may include:

```text
region expansion
region contraction
region translation
Evidence-priority change
Context-rule change
recovery-expectation change
challenge-requirement change
history-window change
response-policy change
rollback-link change
```

Derived criterion-update dynamics may include:

```text
update magnitude
update direction
update rate
cumulative drift
repeated sub-threshold movement
discrimination change
```

Provisionally:

```text
Dyn_t^crit
=
DynCrit(
  Delta_t^crit,
  h_t^crit
)
```

---

## 16. Trusted Anchors and Rollback Points

Let:

```text
b_t ∈ B
```

be a Trusted Anchor reference.

A Trusted Anchor may represent:

```text
protected policy
verified re-authentication result
independent trusted Evidence
signed configuration
protected update rule
external approval
```

Let:

```text
pi_tau ∈ P, tau <= t
```

be a Rollback Point linked to a prior criterion state:

```text
pi_tau ↦ q_tau
```

A valid rollback point should retain or reference:

```text
criterion state
supporting Evidence provenance
Context
integrity status
response history
creation cause
protection status
```

The model does not claim recovery when all anchors and rollback points are compromised.

---

## 17. Guard

The Guard evaluates whether a Criterion Update Candidate may proceed toward adoption.

Let:

```text
g_t
=
Guard(
  q_t,
  a*_(t+1),
  T_t^obs,
  e_t^upd,
  c_(t+1),
  h_t,
  b_t,
  pi_t
)
```

The Guard result is not required to be a single scalar.

Provisionally:

```text
g_t = (
  provenance_ok,
  cross_evidence_ok,
  context_transition_ok,
  update_magnitude_ok,
  update_direction_ok,
  update_rate_ok,
  challenge_support_ok,
  discrimination_preserved,
  history_consistent,
  rollback_available,
  residual_uncertainty
)
```

A candidate Guard admissibility predicate is:

```text
GuardAdmissible(g_t)
```

The predicate may require policy-dependent combinations rather than universal conjunction of every component.

The formal requirement is not that all systems use one identical Guard.

The requirement is that update adoption is mediated by an explicit Guard and Criterion Update Response.

---

## 18. Criterion Integrity

Let:

```text
CI_t
=
CriterionIntegrity(
  q_t,
  T_t^crit,
  g_t,
  h_t^crit,
  b_t,
  pi_t
)
```

where:

```text
T_t^crit
```

is the currently readable Criterion Trajectory.

Criterion Integrity means that the effective criterion and its update process remain sufficiently admissible and traceable to continue serving as an evaluation basis.

A candidate predicate is:

```text
CI_OK(t)
iff
CriterionReadable(T_t^crit)
and
CriterionTraceable(T_t^crit)
and
AnchorConsistent(q_t, b_t)
and
RollbackLinkValid(q_t, pi_t)
and
not ConfirmedCompromise(q_t)
```

This is a provisional logical schema.

Criterion Integrity does not mean:

```text
perfect criterion
zero uncertainty
zero false acceptance
zero false rejection
self-proven trustworthiness
```

---

## 19. Criterion Trajectory

Let retained criterion states be:

```text
Q_(0:t) = {q_0, q_1, ..., q_t}
```

Let retained criterion-update relations be:

```text
R^crit_(0:t)
```

including:

```text
proposal relation
support relation
acceptance relation
deferral relation
freeze relation
review relation
rollback relation
anchor relation
provenance relation
```

Then the Criterion Trajectory is provisionally:

```text
T_t^crit
=
Read_crit(
  Trace_crit(Q_(0:t), R^crit_(0:t))
)
```

Therefore:

```text
Criterion History
!=
Criterion Trajectory
```

The trajectory must preserve why and how a criterion changed, not merely the sequence of resulting parameter values.

---

## 20. Subject Evaluation Function

Let the Subject Evaluation function be:

```text
Eval_auth(
  rho_t,
  T_t^obs,
  delta_t,
  Dyn_t,
  k_t,
  o_t,
  a_t,
  h_t
)
```

It produces an Auth Decision:

```text
d_t^auth
=
Pi_auth(
  rho_t,
  ARC_t,
  delta_t,
  Dyn_t,
  k_t,
  o_t,
  a_t,
  h_t
)
```

where:

```text
d_t^auth ∈ D_auth
```

The model does not require `Pi_auth` to be one weighted scalar score.

A scalar score may be used by a PoC, but semantic priority and state relations may override a raw threshold.

---

## 21. Criterion Evaluation Function

Let the Criterion Evaluation function be:

```text
Eval_crit(
  q_t,
  a*_(t+1),
  Delta_t^crit,
  Dyn_t^crit,
  g_t,
  CI_t,
  h_t^crit,
  b_t,
  pi_t
)
```

It produces a Criterion Update Response:

```text
d_t^crit
=
Pi_crit(
  q_t,
  a*_(t+1),
  Delta_t^crit,
  Dyn_t^crit,
  g_t,
  CI_t,
  h_t^crit
)
```

where:

```text
d_t^crit ∈ D_crit
```

The two decisions may coexist independently.

Examples:

```text
AUTH_STABLE + FREEZE
RECONVERGING + DEFER
REAUTH_REQUIRED + REVIEW
AUTH_FAIL + ROLLBACK
```

The exact allowed combinations and precedence rules are reserved for Priority E.

---

## 22. Guarded Criterion Transition

The next effective criterion is selected by the Criterion Update Response.

```text
a_(t+1)
=
Transition_A(
  a_t,
  a*_(t+1),
  d_t^crit,
  pi_t
)
```

Minimal transition semantics:

```text
a_(t+1) = a*_(t+1)
when d_t^crit = ACCEPT
```

```text
a_(t+1) = a_t
when d_t^crit ∈ {DEFER, FREEZE, REVIEW}
```

```text
a_(t+1) = a_tau
when d_t^crit = ROLLBACK
and pi_tau is a valid trusted rollback point
```

This directly establishes:

```text
dynamic criterion
!=
unconstrained self-update
```

because:

```text
U produces a candidate
but
Transition_A selects the effective criterion
```

---

## 23. Criterion Update Safety Invariants

The initial formal model proposes the following invariants.

### 23.1 Candidate Separation

```text
INV-1:
a*_(t+1) does not become a_(t+1)
without d_t^crit = ACCEPT
```

### 23.2 Decision Separation

```text
INV-2:
d_t^auth does not implicitly determine d_t^crit
```

and:

```text
d_t^crit does not implicitly prove the Access Subject legitimate
```

### 23.3 Freeze Preservation

```text
INV-3:
if d_t^crit = FREEZE,
then a_(t+1) = a_t
and automatic adaptation is disabled
until an explicit unfreeze condition is satisfied
```

### 23.4 Review Preservation

```text
INV-4:
if d_t^crit = REVIEW,
then the candidate is not adopted before the required external or policy review completes
```

### 23.5 Rollback Authenticity

```text
INV-5:
if d_t^crit = ROLLBACK,
then the target criterion must be linked to a valid protected rollback point
```

### 23.6 Provenance Retention

```text
INV-6:
every accepted criterion transition retains traceable linkage to its supporting Evidence, Context, and decision
```

### 23.7 No Silent Discrimination Collapse

```text
INV-7:
a candidate that is known to destroy required discrimination must not be ACCEPTed
```

These invariants are design requirements.
They are not yet mechanically verified properties.

---

## 24. Normal Adaptation Condition

A normal adaptation candidate should be supportable when, under the applicable policy:

```text
Context transition is explainable
Evidence provenance is acceptable
cross-Evidence relations are sufficiently consistent
challenge or re-authentication support is available when required
update magnitude and rate are admissible
discrimination is preserved
rollback remains available
```

A provisional normal-update condition is:

```text
NormalUpdate_t
iff
GuardAdmissible(g_t)
and
CI_OK(t)
and
LegitimateContextTransition(c_t, c_(t+1))
and
DiscriminationPreserved(a_t, a*_(t+1))
```

Then:

```text
NormalUpdate_t
may permit
ACCEPT
```

It does not force ACCEPT under every policy.

---

## 25. Criterion Poisoning Condition

Let poisoning success at stage `t` be represented provisionally as:

```text
PoisonSuccess_t
iff
MaliciousInfluence(T_t^obs, e_t^upd)
and
Adopted(a*_(t+1))
and
AdmissibleMaliciousRegion(a_(t+1))
and
not AuthorizedPolicyChange
```

A broader cumulative condition is:

```text
CumulativePoisonSuccess_(0:t)
iff
CriterionDrift(a_0, a_t) exceeds an allowed bound
and
that drift is materially caused by malicious observations
and
malicious trajectories become more admissible
and
no authorized policy transition explains the change
```

This model covers, among others:

```text
region expansion
region translation
Evidence-priority poisoning
challenge weakening
history-window poisoning
response-policy poisoning
rollback-link poisoning
```

---

## 26. Detection and Containment Conditions

A poisoning attempt is not required to be fully attributed before containment.

A provisional detection indication is:

```text
PoisonIndication_t
iff
one or more of:

  repeated sub-threshold criterion drift
  unsupported update direction
  cross-Evidence inconsistency
  provenance failure
  discrimination decline
  challenge mismatch
  Context-transition mismatch
  rollback-link anomaly
  suspicious history-window change
```

A containment success condition is:

```text
ContainmentSuccess_t
iff
d_t^crit ∈ {DEFER, FREEZE, REVIEW, ROLLBACK}
and
malicious candidate is not adopted at stage t
```

A recovery success condition is:

```text
RecoverySuccess_t
iff
criterion is restored to or rebuilt from a trusted admissible state
and
traceability is preserved
and
required discrimination is restored
```

The model distinguishes:

```text
detection
containment
recovery
```

They are not identical guarantees.

---

## 27. Security Properties

The initial model targets the following properties.

### 27.1 Guarded Adoption

No Criterion Update Candidate is adopted without a separate Criterion Update Response.

### 27.2 Traceable Adaptation

Every accepted update remains linked to its supporting Evidence, Context, and decision history.

### 27.3 Bounded Adaptation

Update magnitude, direction, rate, and cumulative drift may be constrained by policy and Guard conditions.

### 27.4 Decision Independence

Current access continuation and criterion adaptation approval remain separately selectable.

### 27.5 Poisoning Containment

Suspicious updates may be prevented from adoption without necessarily collapsing the current Authentication Relation.

### 27.6 Recoverability

A protected rollback point may restore a prior trusted criterion after contamination is detected.

### 27.7 Explicit Uncertainty

Evidence insufficiency may produce DEFER or REVIEW rather than forced ACCEPT or forced rejection.

---

## 28. Non-Guarantees

The model does not guarantee:

```text
complete prevention of criterion poisoning
detection of every credential theft
 detection of every relay attack
zero false acceptance
zero false rejection
perfect human identification
security when all Evidence sources are compromised
security when all Trusted Anchors are compromised
security when all Rollback Points are compromised
security under runtime code compromise
security when the attacker perfectly reproduces all relevant trajectories
automatic correctness of every Guard policy
production performance or resource efficiency
```

The model provides a structure for conditional evaluation and guarded response.

It does not remove the need for:

```text
protected implementation
independent Evidence
policy design
secure storage
challenge mechanisms
auditability
operational review
```

---

## 29. Minimum Executable Model

For the first Simulation or PoC, the full relational model may be reduced to a bounded numerical representation.

A minimal criterion may be:

```text
a_t = (
  center_t,
  width_t,
  evidence_weights_t,
  challenge_threshold_t
)
```

A minimal observation may be:

```text
x_t = (
  behavior_t,
  network_t,
  operation_t,
  challenge_result_t
)
```

A candidate update may be:

```text
a*_(t+1)
=
U(a_t, x_t)
```

A minimal Guard may evaluate:

```text
update magnitude
update direction
repeated sub-threshold drift
cross-Evidence consistency
challenge confirmation
discrimination preservation
```

The PoC should compare:

```text
Unconstrained Update Model
versus
Guarded Update Model
```

The minimum required result is to demonstrate that:

```text
normal Context change can be accepted under supporting Evidence
while
gradual malicious drift is deferred, frozen, reviewed, or rolled back
before unrestricted criterion contamination
```

This is an executable demonstration, not a universal security proof.

---

## 30. Formal Model Summary

The complete working flow is:

```text
Observed Evidence
        ↓
Local Authentication Realization
        ↓
Observed Access Trajectory
        ↓
Subject Evaluation
        ↓
Auth Decision
```

and separately:

```text
Observed Access Trajectory
+ Context
+ Update Evidence
+ Current Criterion
        ↓
Criterion Update Candidate
        ↓
Criterion Update Delta and Dynamics
        ↓
Guard
        ↓
Criterion Integrity Evaluation
        ↓
Criterion Update Response
        ↓
ACCEPT / DEFER / FREEZE / REVIEW / ROLLBACK
        ↓
Next Effective Criterion
```

The two flows interact but do not collapse into one decision.

```text
Subject Evaluation Loop
        ↕
Criterion Integrity Loop
```

The structural recurrence is fractal-like.
Runtime execution remains bounded and explicit.

---

## 31. Priority D Decisions

Priority D fixes the following working positions.

### 31.1 Dual Evaluation

```text
GyroAuth evaluates both:

1. the current Authentication Relation
2. the criterion used to evaluate that relation
```

### 31.2 Guarded Update

```text
Update Candidate
→ Guard
→ Criterion Integrity Evaluation
→ Criterion Update Response
→ Effective Criterion
```

### 31.3 Mandatory Separation

```text
Criterion Update Candidate
!=
Accepted Criterion
```

```text
Auth Decision
!=
Criterion Update Response
```

### 31.4 Criterion Change as Trajectory

Criterion change is not represented only as parameter history.
It is represented as a traceable relational configuration linked to Evidence, Context, decision, and rollback state.

### 31.5 Conditional Security

Claims are conditional on:

```text
Threat Model
Trusted Assumptions
Guard policy
Evidence availability
protected anchors
protected rollback points
implementation integrity
```

---

## 32. Open Questions for Priority E

Priority E must determine:

1. Which Criterion States are formally adopted?
2. Are `STABLE`, `ADAPTING`, `UNCERTAIN`, `FROZEN`, and `COMPROMISED` sufficient?
3. Which state and response combinations are valid?
4. What exact transition guards lead to ACCEPT, DEFER, FREEZE, REVIEW, and ROLLBACK?
5. Can REVIEW coexist with a still-continuable current Authentication Relation?
6. What is required to leave FROZEN state?
7. What evidence authorizes rollback?
8. What evidence authorizes recovery from rollback?
9. Which transitions require explicit re-authentication?
10. How should failure of the criterion-evaluation mechanism itself be represented?
11. What precedence applies when Auth Decision and Criterion Update Response disagree operationally?
12. Which transition rules are required for the minimum Simulation?

---

## 33. Priority D Completion Status

```text
Priority D: Formal Security Model
Status: completed as working model
```

Completed:

```text
sets and state domains
stage inputs
Local Authentication Realization
Observed Access Trajectory
Authentication Relation
Authentication Relation Continuity
Deviation Dynamics
Authentication Criterion
Criterion State
Criterion Update Candidate
Criterion Update Delta
Trusted Anchors
Rollback Points
Guard
Criterion Integrity
Criterion Trajectory
Subject Evaluation function
Criterion Evaluation function
Guarded Criterion Transition
security invariants
normal adaptation condition
criterion poisoning condition
containment and recovery conditions
security properties
non-guarantees
minimum executable model
```

Not yet completed:

```text
final Criterion State Machine
final response precedence
formal transition table
normal and poisoned scenario fixtures
simulation implementation
empirical results
mechanical verification
paper manuscript
```

Next:

```text
Priority E: Criterion Update State Machine
```
