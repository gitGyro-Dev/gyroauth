# GyroAuth Formal Terminology and Scope

## 1. Purpose

This document completes **Priority B: Formal Terminology and Scope** for the GyroAuth formalization and paper-preparation work.

Its purpose is to:

```text
fix the working meanings of the main terms
separate core terms from explanatory terms
separate subject evaluation from criterion evaluation
define the scope of the formal security model
prevent cross-layer terminology drift
prepare Priority C: Threat Model
```

This document is a terminology and responsibility-boundary document.

It does not yet provide:

```text
a completed threat model
a completed formal security proof
a finalized state machine
an empirical security guarantee
a production implementation contract
```

The terminology remains subject to refinement through the Threat Model, Formal Security Model, and Simulation phases. However, later documents should not silently change these meanings.

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

The present scope is the GyroAuth application-layer interpretation of authentication relations, observed trajectories, adaptive criteria, criterion integrity, and guarded criterion updates.

---

## 3. Terminology Policy

The formalization uses three classes of terms.

### 3.1 Primary formal terms

These terms are intended to appear in definitions, equations, state transitions, the Threat Model, the PoC, and the paper.

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

### 3.2 Secondary formal terms

These terms support the model but may be represented as components rather than independent top-level objects.

```text
Context
Local Authentication Realization
State Convergence
Deviation
Deviation Dynamics
Admissible Trajectory
Authentication Viability Region
Trusted Anchor
Rollback Point
Guard
History
```

### 3.3 Explanatory terms

These terms may be used to explain intuition but should not independently determine a formal result unless mapped to formal variables.

```text
unease
wobble
thickness
usual movement
feels different
relational discomfort
```

For example:

```text
"unease"
```

must be expanded into one or more observable or derived properties such as:

```text
deviation direction
deviation rate
deviation spread
deviation persistence
recovery tendency
cross-evidence inconsistency
```

---

## 4. Primary Formal Definitions

## 4.1 Access Subject

> **Access Subject** is the currently evaluated source of access and operations within an authentication context.

An Access Subject may be:

```text
a legitimate user
a credential thief
a session hijacker
a relay-mediated operator
a bot
a remote controller
a mixed or changing source of operations
```

An Access Subject is not assumed to be the legitimate person.

```text
Access Subject
!=
Verified Identity
```

The term denotes the operational subject currently under evaluation.

---

## 4.2 Expected Identity

> **Expected Identity** is the persistent reference relation against which the current Access Subject is evaluated as the same authenticated identity across changing sessions and contexts.

Expected Identity is not reducible to:

```text
user ID
password
credential
device
location
behavioral profile
session token
one biometric feature
```

These may be Evidence associated with an Expected Identity, but none is identical to the Expected Identity.

```text
Evidence
!=
Identity
```

The term `Expected Identity` is used instead of simply `Identity` in formal evaluation expressions to make clear that the model evaluates a current Access Subject against an authentication reference rather than proving a complete metaphysical identity claim.

---

## 4.3 Session

> **Session** is a bounded operational context within which the relation between an Access Subject and an Expected Identity is observed and evaluated.

A Session may correspond to:

```text
a web login period
an API token lifetime
a device-use interval
a privileged operation interval
a sequence spanning re-authentication
a bounded cross-session evaluation window
```

The boundaries are distinct:

```text
Session continuity
!=
Identity continuity
!=
Trajectory continuity
```

A Session may remain technically valid while the authentication relation becomes non-continuable.

---

## 4.4 Observed Evidence

> **Observed Evidence** is information made available to GyroAuth through one or more observation sources and Slices for evaluating the authentication relation or the authentication criterion.

Evidence candidates include:

```text
credential result
device state
behavioral state
time relation
space relation
network relation
motion relation
operation order
privilege transition
challenge response
Operator Response
history
criterion-update provenance
```

Evidence is always interpreted under a Context and Slice.

```text
raw input
!=
formal authentication decision
```

Location and proximity are Evidence candidates. They are not authentication itself.

---

## 4.5 Local Authentication Realization

> **Local Authentication Realization** is one bounded GyroAuth-readable result produced from currently available Evidence and GyroOS execution results for a local evaluation step.

A provisional representation is:

```text
a_t^auth = (
  X_t,
  Delta_t,
  K_t,
  O_t,
  C_t,
  H_t
)
```

where:

```text
X_t     = observed or interpreted authentication state
Delta_t = local Deviation
K_t     = Stability result
O_t     = GyroOS Operator Response or mapped response evidence
C_t     = current Context
H_t     = relevant History
```

This tuple is provisional and does not redefine the Gyro Logic Core or the GyroOS contract.

A set or sequence of Local Authentication Realizations is not automatically a Trajectory.

```text
{a_t^auth}
!=
Observed Access Trajectory automatically
```

---

## 4.6 Observed Access Trajectory

> **Observed Access Trajectory** is the readable relational configuration obtained by tracing admissible relations among Local Authentication Realizations associated with the current Access Subject under the current Orientation, Context, and Slice.

It is not merely:

```text
a chronological event log
a sequence of feature vectors
all stored history
one predetermined path
all available relations
```

The Observed Access Trajectory may include:

```text
order
branching
merging
gaps
re-authentication
recovery
Jump
Defer
context transition
retrospective reinterpretation
```

Provisional notation:

```text
T_t^obs
```

or, when the tracing conditions must be explicit:

```text
T_A^(t) = Read_A(Trace_CA(G_A^(0:t), E_A^(0:t)))
```

This is a structural schema, not yet a numerical equation.

---

## 4.7 Admissible Trajectory

> **Admissible Trajectory** is a trajectory whose states, transitions, relations, and update direction remain allowable for an Expected Identity under the current Context and authentication policy.

One Expected Identity may admit multiple trajectories.

```text
One Expected Identity
→
Multiple admissible trajectories
```

Therefore:

```text
Expected Identity Trajectory
!=
One fixed line
```

The formal model should use an admissible set or region where necessary rather than assuming one exact expected path.

Provisional notation:

```text
T_I^adm
```

for an admissible trajectory, or:

```text
mathcal{T}_I^adm(C_t)
```

for a Context-relative admissible trajectory family.

---

## 4.8 Authentication Relation

> **Authentication Relation** is the currently evaluated relation between an Access Subject and an Expected Identity within a Session and Context.

Provisional notation:

```text
R_t^auth = Rel(A_t^subject, I, S_t, C_t)
```

where `A_t^subject` denotes the current Access Subject and must not be confused with the authentication criterion notation introduced later.

The Authentication Relation is not the person, account, credential, or Session itself.

```text
Authentication Relation
!=
Identity
!=
Session
!=
Credential
```

GyroAuth selects whether this relation may continue.

---

## 4.9 Authentication Relation Continuity

> **Authentication Relation Continuity** is the condition under which admissible relations among changing Local Authentication Realizations can still be traced such that the relation between the current Access Subject and the Expected Identity remains readable as one continuable authentication relation.

It does not mean:

```text
no change
identical state
uninterrupted logging
valid Session token
all events individually valid
```

Therefore:

```text
continuous observation
!=
Authentication Relation Continuity
```

and:

```text
valid events
!=
stable trajectory
```

Provisional predicate:

```text
ARC(T_t^obs, I ; C_t)
```

A candidate schema is:

```text
ARC(T_t^obs, I ; C_t)
iff
Readable(T_t^obs ; C_t)
and
IdentityReferable(T_t^obs, I ; C_t)
and
Admissible(T_t^obs ; I, C_t)
```

This remains provisional until Priority D: Formal Security Model.

---

## 4.10 Authentication Criterion

> **Authentication Criterion** is the Context-relative evaluation basis used by GyroAuth to interpret Evidence, Deviation, Stability, Trajectory, History, and response conditions when selecting whether an Authentication Relation may continue.

Provisional notation:

```text
A_t
```

An Authentication Criterion may contain or reference:

```text
admissible state relations
admissible trajectory relations
evidence priority
trajectory envelope
deviation tolerance
recovery expectation
challenge requirement
update policy
protected anchors
```

The Authentication Criterion is not a fixed user profile.

```text
Authentication Criterion
!=
Fixed Identity Profile
```

It may adapt, but adaptation is constrained.

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 4.11 Criterion State

> **Criterion State** is the currently effective configuration and integrity condition of the Authentication Criterion at a given evaluation stage.

Provisional representation:

```text
Q_t = (
  A_t,
  C_t,
  P_t,
  Z_t,
  L_t
)
```

where:

```text
A_t = effective criterion content
C_t = Context
P_t = provenance and supporting evidence state
Z_t = integrity or stability-related state
L_t = linkage to protected history and rollback points
```

The exact tuple will be fixed in the Formal Security Model.

The term `Criterion State` separates the currently effective criterion from its candidate updates and from the response selected for those updates.

---

## 4.12 Criterion Update Candidate

> **Criterion Update Candidate** is a proposed next criterion produced from the current criterion, newly observed Evidence, Context, and History, but not yet accepted as the effective Authentication Criterion.

Provisional notation:

```text
A*_(t+1)
```

Candidate generation:

```text
A*_(t+1)
=
U(A_t, T_t^obs, C_(t+1), E_t, H_t)
```

The critical distinction is:

```text
Criterion Update Candidate
!=
Accepted Criterion
```

A candidate must pass an independent criterion-integrity evaluation and Criterion Update Response.

---

## 4.13 Criterion Trajectory

> **Criterion Trajectory** is the readable relational configuration through which changes among Criterion States can be traced as admissible, deferred, frozen, externally reviewed, rolled back, or compromised updates.

Criterion Trajectory is not merely a version history.

```text
Criterion History
!=
Criterion Trajectory
```

It must preserve or reference relations such as:

```text
update cause
evidence provenance
update magnitude
update direction
update rate
Context transition
challenge confirmation
discrimination preservation
response decision
rollback linkage
```

Provisional notation:

```text
T_t^crit
```

Criterion Trajectory is a GyroAuth application concept. It does not redefine Trajectory in Gyro Logic.

---

## 4.14 Criterion Integrity

> **Criterion Integrity** is the condition in which the Authentication Criterion and its update process remain admissible, traceable, and sufficiently stable as a basis for evaluating the Authentication Relation to the Expected Identity.

Criterion Integrity concerns both:

```text
the effective criterion
and
the trajectory through which it changes
```

Criterion Integrity does not mean that GyroAuth proves its own trustworthiness without assumptions.

It may depend on:

```text
protected policy anchors
trusted or partially trusted Evidence sources
signed update records
challenge or re-authentication results
cross-evidence consistency
trusted rollback points
human or external policy review
```

Provisional notation:

```text
CI_t
```

or predicate:

```text
CriterionIntegrity(A_t, T_t^crit, Anchors_t, H_t)
```

---

## 4.15 Auth Decision

> **Auth Decision** is the GyroAuth application-layer selection describing whether and how the current Authentication Relation may continue.

Current candidates:

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

Working meanings:

### AUTH_STABLE

The current Authentication Relation remains sufficiently stable and continuable under the current criterion.

### RECONVERGING

Deviation has increased or the relation has moved outside an ordinary region, but re-convergence remains readable and continuation is conditionally possible.

### REAUTH_REQUIRED

Implicit Evidence is insufficient and explicit verification is required. The Expected Identity has not necessarily collapsed.

```text
REAUTH_REQUIRED
!=
AUTH_FAIL
```

### AUTH_FAIL

The current Authentication Relation can no longer be continued under the current evidence, trajectory, criterion, and response conditions.

```text
AUTH_FAIL
!=
Identity deletion
```

The decision concerns continuation of the current relation.

---

## 4.16 Criterion Update Response

> **Criterion Update Response** is the GyroAuth application-layer response selected for a Criterion Update Candidate after criterion-integrity evaluation.

Candidates:

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

Working meanings:

### ACCEPT

Adopt the candidate as the effective next Authentication Criterion.

```text
A_(t+1) = A*_(t+1)
```

### DEFER

Do not adopt the candidate yet. Preserve the current criterion while collecting additional Evidence or waiting for a clearer Context.

```text
A_(t+1) = A_t
```

### FREEZE

Suspend adaptive criterion updates because poisoning, instability, or insufficient criterion integrity is suspected. Subject evaluation may continue separately if policy allows.

```text
A_(t+1) = A_t
AdaptiveUpdateEnabled_(t+1) = false
```

### REVIEW

Preserve the current criterion and transfer the update decision to an external policy, administrator, independent verification path, or higher-trust process.

`REVIEW` differs from `DEFER` because the deciding authority or validation path changes.

### ROLLBACK

Replace the current criterion with a previously trusted criterion state.

```text
A_(t+1) = A_tau,
where tau < t
```

A trusted Rollback Point is required.

These are GyroAuth Criterion Update Responses. They do not modify the canonical GyroOS Operator Response vocabulary.

---

## 5. Secondary Formal Definitions

## 5.1 Context

> **Context** is the set of currently relevant environmental, operational, policy, temporal, and relational conditions under which Evidence and trajectories are interpreted.

Provisional notation:

```text
C_t
```

Context may affect:

```text
which Evidence is relevant
which relations are admissible
which Deviation is expected
which trajectory region is viable
which response is required
whether a criterion update may be accepted
```

Context is not an unconstrained explanation that can justify any result.

```text
Context-relative
!=
arbitrary
```

---

## 5.2 State Convergence

> **State Convergence** is the observed tendency of the authentication state and its relations to maintain or recover admissibility with respect to the Expected Identity under the current Authentication Criterion and Context.

It is not exact matching.

```text
State Convergence
!=
Exact State Equality
```

State Convergence is observed and interpreted. The final Auth Decision is selected through Stability-based Selection.

---

## 5.3 Deviation

> **Deviation** is the Slice-relative difference between an observed authentication realization or relation and the currently relevant criterion, admissible relation, or trajectory expectation.

Provisional notation:

```text
Delta_t
```

Deviation is not automatically risk, attack, or failure.

```text
Deviation exists
!=
Attack confirmed
```

---

## 5.4 Deviation Dynamics

> **Deviation Dynamics** is the multi-dimensional development of Deviation across time and relations, including its direction, rate, acceleration, spread, persistence, and recovery tendency.

Provisional representation:

```text
D_t = (
  Delta_t,
  v_t,
  a_t,
  W_t,
  P_t,
  R_t
)
```

where:

```text
Delta_t = current multi-dimensional Deviation
v_t     = change direction and rate
a_t     = change in rate or direction
W_t     = spread or width over an interval
P_t     = persistence
R_t     = recovery or re-convergence tendency
```

Deviation Dynamics prevents the model from collapsing all trajectory meaning into one current scalar.

---

## 5.5 Authentication Viability Region

> **Authentication Viability Region** is the Context-relative region of states, transitions, and trajectories within which the Authentication Relation remains readable as continuable.

Provisional notation:

```text
V_I(C_t, A_t)
```

The region may change with Context and trusted trajectory evidence.

```text
V_I(C_t, A_t)
!=
V_I(C_(t+1), A_(t+1))
```

The region is not a permanently fixed profile and must not expand automatically merely because behavior was observed.

---

## 5.6 Guard

> **Guard** is the criterion-integrity evaluation that constrains whether and how a Criterion Update Candidate may affect the effective Authentication Criterion.

Provisional notation:

```text
G_t
=
Guard(
  A_t,
  A*_(t+1),
  T_t^obs,
  T_t^crit,
  C_(t+1),
  E_t,
  H_t,
  Anchors_t
)
```

Candidate Guard components include:

```text
Evidence provenance
cross-evidence consistency
update magnitude
update direction
update rate
challenge confirmation
discrimination preservation
rollback availability
policy constraints
```

The Guard does not necessarily produce only a Boolean result. It may support the five Criterion Update Responses.

---

## 5.7 Trusted Anchor

> **Trusted Anchor** is a policy, credential result, signed state, protected reference, external verification, or other input that the Threat Model assumes is sufficiently protected for constraining criterion updates.

A Trusted Anchor is not automatically infallible. Its protection and assumed attacker limitations must be stated in the Threat Model.

---

## 5.8 Rollback Point

> **Rollback Point** is a prior Criterion State retained as sufficiently trusted and recoverable for use after suspected or confirmed criterion contamination.

A Rollback Point must include or reference:

```text
criterion content
provenance
acceptance reason
time or stage
integrity evidence
linkage to later updates
```

Rollback without a protected and traceable point is not a security guarantee.

---

## 5.9 History

> **History** is retained information from previous subject evaluations, criterion evaluations, decisions, responses, and transitions that is made available to a current evaluation.

History is input material.

```text
History
!=
Trajectory automatically
```

Trajectory requires relation selection, tracing, and readability under the current conditions.

---

## 6. Decision Separation

GyroAuth has two distinct decision dimensions.

### 6.1 Subject evaluation dimension

Question:

```text
May the current Authentication Relation continue?
```

Output:

```text
Auth Decision
```

### 6.2 Criterion evaluation dimension

Question:

```text
May the proposed criterion change become the next effective criterion?
```

Output:

```text
Criterion Update Response
```

Therefore:

```text
Auth Decision
!=
Criterion Update Response
```

Valid combinations may include:

```text
AUTH_STABLE + ACCEPT
AUTH_STABLE + FREEZE
AUTH_STABLE + REVIEW
RECONVERGING + DEFER
REAUTH_REQUIRED + DEFER
REAUTH_REQUIRED + FREEZE
AUTH_FAIL + ROLLBACK
```

The exact permitted combination matrix will be fixed in Priority D and Priority E.

A criterion problem must not automatically be interpreted as proof that the Access Subject is malicious.

```text
Criterion uncertainty
!=
Subject compromise confirmed
```

Likewise, a currently stable subject result does not automatically justify updating the criterion.

```text
AUTH_STABLE
!=
Criterion update automatically ACCEPTed
```

---

## 7. Notation and Symbol Table

The following notation is provisional but should be used consistently in subsequent documents unless explicitly revised.

| Symbol | Meaning |
|---|---|
| `t` | discrete evaluation stage or time index |
| `I` | Expected Identity |
| `S_t` | Session or Session state, where context makes the meaning clear |
| `C_t` | Context at stage `t` |
| `E_t` | currently available Evidence or update-supporting Evidence |
| `X_t` | observed or interpreted authentication state |
| `Delta_t` | authentication Deviation |
| `D_t` | Deviation Dynamics |
| `K_t^auth` | subject-side Stability-related result |
| `T_t^obs` | Observed Access Trajectory |
| `T_t^crit` | Criterion Trajectory |
| `A_t` | effective Authentication Criterion |
| `A*_(t+1)` | Criterion Update Candidate |
| `Q_t` | Criterion State |
| `G_t` | Guard evaluation |
| `CI_t` | Criterion Integrity state or result |
| `H_t` | retained History |
| `Anchor_t` | trusted anchor set or state |
| `A_tau` | prior trusted criterion used for rollback |
| `R_t^auth` | Auth Decision |
| `R_t^crit` | Criterion Update Response |

### 7.1 Reserved distinctions

The following symbols or terms must not be silently collapsed:

```text
T_t^obs
!=
T_t^crit
```

```text
R_t^auth
!=
R_t^crit
```

```text
A_t
!=
A*_(t+1)
```

```text
Identity
!=
Observed Access Trajectory
```

```text
History
!=
Trajectory
```

```text
Criterion State
!=
Criterion Update Response
```

---

## 8. Formal Study Scope

The formal security study includes:

```text
subject-side authentication relation evaluation
observed access trajectory
context-relative criterion adaptation
criterion update candidates
criterion trajectory
criterion integrity
guarded criterion updates
separated subject and criterion decisions
normal adaptation versus criterion poisoning
trusted anchors and rollback points
minimum synthetic simulation
conditional security claims and limitations
```

The intended primary security problem is:

```text
How can a dynamic authentication criterion adapt
without treating every observed behavior as the new normal?
```

The central design constraint remains:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 9. Explicit Non-Scope

The current formalization does not attempt to provide:

```text
perfect human identification
complete prevention of credential theft
complete prevention of relay attacks
complete detection of session hijacking
security when all Evidence sources are compromised
security when all Trusted Anchors are compromised
zero false acceptance
zero false rejection
universal biometric modeling
production-grade distributed architecture
privacy-preserving learning design
hardware resource optimization
full GyroOS implementation
formal proof of Gyro Logic itself
```

The current PoC may use synthetic discrete-time data.

Real-world deployment claims require later work on:

```text
datasets
sensor trust
resource consumption
privacy
calibration
latency
long-term drift
multi-tenant isolation
operational policy
```

---

## 10. Layer and Repository Responsibility Boundaries

## 10.1 Gyro Logic

Gyro Logic owns the theory-level concepts and Core.

GyroAuth may reference Gyro Logic studies concerning:

```text
Continuity Readability
Trajectory
Difference
Boundary
Stability
```

GyroAuth does not rewrite those definitions.

```text
Core change: none
```

## 10.2 GyroOS

GyroOS owns runtime execution concepts and canonical execution contracts.

GyroAuth consumes or interprets outputs such as:

```text
slice-done
Stability
Operator Response
History
```

GyroAuth does not redefine `/loop/step` or canonical GyroOS Operator Response.

```text
GyroOS contract change: none
```

## 10.3 GyroAuth

GyroAuth owns the application-layer meanings introduced here:

```text
Access Subject
Expected Identity
Authentication Relation
Observed Access Trajectory for authentication
Authentication Relation Continuity
Authentication Criterion
Criterion State
Criterion Update Candidate
Criterion Trajectory
Criterion Integrity
Auth Decision
Criterion Update Response
```

## 10.4 Project Cycle and Developer Toolkit

Project Cycle may track and publish the status of these definitions but does not alter them.

Developer Toolkit may validate schemas, terminology consistency, update histories, or generated documents but does not decide the theory.

---

## 11. Terms Not Adopted as Primary Terms

The following expressions are useful intuitively but are not adopted as primary formal terms at this stage.

### 11.1 Identity Profile

Not adopted because it suggests a fixed collection of user features.

Preferred terms:

```text
Expected Identity
Authentication Criterion
Admissible Trajectory
```

### 11.2 Baseline

Not adopted as the sole model because it often suggests one statistical center or threshold.

It may still be used for a specific implementation component, provided it is not equated with the full Authentication Criterion.

### 11.3 Identity Trajectory as one exact path

Not adopted because one Expected Identity may admit multiple valid trajectories.

Preferred expression:

```text
Context-relative admissible trajectory family
```

### 11.4 Self-verifying authentication

Not adopted because GyroAuth cannot establish its own trustworthiness without external assumptions and protected anchors.

Preferred expression:

```text
criterion-aware continuous evaluation
```

### 11.5 Absolute attack resistance

Not adopted.

All security claims must remain conditional on:

```text
Threat Model
Trusted Assumptions
Evidence Availability
Implementation
Simulation or empirical results
```

### 11.6 Location authentication

Not adopted as a description of GyroAuth.

```text
Location
=
one possible Evidence element
```

GyroAuth evaluates multi-dimensional relations, trajectories, Deviation, Stability, History, and responses.

---

## 12. Working Model Summary

The subject-side evaluation is provisionally summarized as:

```text
Observed Evidence
↓
Local Authentication Realization
↓
Observed Access Trajectory
↓
State Convergence
+
Authentication Relation Continuity
+
Deviation Dynamics
+
Stability
+
History
↓
Stability-based Selection
↓
Auth Decision
```

The criterion-side evaluation is provisionally summarized as:

```text
Current Authentication Criterion
+
Observed Access Trajectory
+
Context Change
+
Update Evidence
↓
Criterion Update Candidate
↓
Criterion Trajectory
+
Criterion Integrity
+
Trusted Anchors
+
History
↓
Guard
↓
ACCEPT / DEFER / FREEZE / REVIEW / ROLLBACK
↓
Next Effective Criterion
```

The two evaluations remain related but distinct:

```text
Subject Evaluation Loop
        ↕
Criterion Integrity Loop
```

The structural recurrence may be fractal-like, but runtime execution must remain bounded.

---

## 13. Priority B Decisions

Priority B adopts the following working decisions for subsequent formalization.

### Decision B-1

GyroAuth selects continuation of an Authentication Relation, not proof of a complete human identity.

### Decision B-2

Expected Identity and Observed Access Trajectory are distinct.

### Decision B-3

Observed history is not automatically a Trajectory.

### Decision B-4

One Expected Identity may admit multiple Context-relative trajectories.

### Decision B-5

Authentication Relation Continuity concerns traceable relational continuity, not unchanged features or uninterrupted logging.

### Decision B-6

The Authentication Criterion is adaptive but not an unconstrained self-updating profile.

### Decision B-7

Criterion Update Candidate and Accepted Criterion are distinct.

### Decision B-8

Auth Decision and Criterion Update Response are distinct decision dimensions.

### Decision B-9

Criterion Integrity includes both the effective criterion and its update trajectory.

### Decision B-10

ACCEPT, DEFER, FREEZE, REVIEW, and ROLLBACK are GyroAuth Criterion Update Responses and do not redefine GyroOS Operator Response.

### Decision B-11

Security claims remain conditional and must be fixed only after the Threat Model and Simulation.

### Decision B-12

No change is made to Gyro Logic Core or GyroOS contracts.

---

## 14. Open Questions for Later Priorities

The following questions remain intentionally open.

```text
What exact attacker capabilities define criterion poisoning?
Which Evidence sources are trusted, partially trusted, or untrusted?
Is Guard Boolean, scored, ordered, or policy-composed?
How is Criterion Integrity represented numerically or relationally?
What combinations of Auth Decision and Criterion Update Response are allowed?
When does FREEZE affect subject evaluation?
What constitutes a trusted Rollback Point?
How is discrimination preservation measured?
How are normal long-term changes distinguished from gradual poisoning?
Which terms must appear in the public API and which remain internal?
```

These questions belong to:

```text
Priority C: Threat Model
Priority D: Formal Security Model
Priority E: Criterion Update State Machine
Priority F: Normal versus Poisoned Update Scenarios
Priority G/H: Simulation and PoC
```

---

## 15. Priority B Completion Status

```text
Priority B: Formal Terminology and Scope
Status: Working definitions established
```

The terminology is now sufficiently structured to begin **Priority C: Threat Model**.

Before final publication, the terminology must be reviewed against:

```text
the completed formal model
the implemented simulation
related work terminology
English/Japanese manuscript consistency
README consistency
API/schema naming
```

---

## 16. Core and Contract Change Status

```text
Gyro Logic Core change: none
GyroOS contract change: none
GyroAuth application terminology: expanded
GitHub repository updated: gyroauth only
```
