# GyroAuth Normal and Poisoned Update Scenarios

## 1. Purpose

This document completes **Priority F: Normal and Poisoned Update Scenarios** for the GyroAuth formalization and paper-preparation work.

It builds on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
docs/18_formal_security_model.md
docs/19_criterion_update_state_machine.md
```

Its purpose is to define concrete, reproducible scenarios that distinguish:

```text
legitimate criterion adaptation
from
gradual criterion poisoning
```

The scenarios are designed to prepare:

```text
Priority G: Minimal Simulation Design
Priority H: PoC Implementation and Results
Priority I: Security Claims and Limitations
```

This document does not yet provide empirical results. It specifies the inputs, transitions, expected decisions, expected criterion responses, and failure conditions that the simulation must reproduce.

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

The scenario model is limited to the GyroAuth application layer.

```text
Core change: none
GyroOS contract change: none
GyroAuth scenario model: added
```

---

## 3. Central Scenario Position

The central comparison is:

```text
dynamic criterion
!=
unconstrained self-update
```

A legitimate Context change may require the Authentication Criterion to adapt.

However, observed behavior must not become the next effective criterion merely because it was observed repeatedly.

```text
Observation
→ Candidate Update
→ Guard
→ Criterion Update Response
→ Effective Criterion Transition
```

The scenarios therefore separate:

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

## 4. Scenario Model

Each scenario is described by the tuple:

```text
Scenario = (
  Initial State,
  Context Sequence,
  Evidence Sequence,
  Observed Access Trajectory,
  Candidate Updates,
  Guard Results,
  Auth Decisions,
  Criterion Responses,
  Final State,
  Expected Security Interpretation
)
```

For stage `t`, let:

```text
A_t        = effective Authentication Criterion
A*_(t+1)   = Criterion Update Candidate
Q_t        = Criterion State
D_auth_t   = Auth Decision
D_crit_t   = Criterion Update Response
G_t        = Guard result
T_t^obs    = Observed Access Trajectory
C_t        = Context
E_t        = Evidence bundle
```

The effective criterion transition remains:

```text
A_(t+1) = A*_(t+1)   when D_crit_t = ACCEPT
A_(t+1) = A_t        when D_crit_t = DEFER / FREEZE / REVIEW
A_(t+1) = A_tau      when D_crit_t = ROLLBACK, tau < t
```

---

## 5. Shared Scenario Dimensions

The minimum simulation should represent the following dimensions.

### 5.1 Subject-side dimensions

```text
deviation magnitude
deviation direction
deviation rate
deviation spread
deviation persistence
recovery tendency
trajectory continuity
stability
authentication relation continuity
```

### 5.2 Criterion-side dimensions

```text
criterion center or reference position
criterion region width
criterion update magnitude
criterion update direction
criterion update rate
evidence provenance quality
cross-evidence consistency
challenge confirmation
discrimination preservation
rollback availability
criterion integrity
```

### 5.3 Decision dimensions

```text
Auth Decision:
  AUTH_STABLE
  RECONVERGING
  REAUTH_REQUIRED
  AUTH_FAIL

Criterion Update Response:
  ACCEPT
  DEFER
  FREEZE
  REVIEW
  ROLLBACK
```

---

## 6. Scenario N1 — Legitimate New Device Transition

### 6.1 Objective

Demonstrate that GyroAuth can permit criterion adaptation when a legitimate user changes device and sufficient supporting evidence is available.

### 6.2 Initial State

```text
Criterion State       = STABLE
Auth Decision         = AUTH_STABLE
Effective Criterion   = A_0
Rollback Point        = A_0
Known Context         = known device / known network / normal behavior
```

The current criterion includes:

```text
known device relation
known network relation
normal behavior range
normal operation order
normal response pattern
```

### 6.3 Context Change

```text
known device
→ new device
```

The new device is initially outside the current admissible device relation.

### 6.4 Evidence Sequence

```text
Stage 1:
new device observed
network remains plausible
credential succeeds
behavior remains partially consistent

Stage 2:
explicit re-authentication requested
challenge succeeds

Stage 3:
continued behavior remains consistent
network and time relations remain plausible
no privilege anomaly appears

Stage 4:
new device relation becomes supported by repeated trusted evidence
```

### 6.5 Expected Subject Trajectory

```text
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
→ AUTH_STABLE
```

Interpretation:

```text
initial deviation increase
→ explicit verification
→ cross-evidence confirmation
→ re-convergence
```

### 6.6 Candidate Update

A candidate is generated to incorporate the new device relation.

```text
A*_1 = U(A_0, T_obs, C_new_device, E_reauth)
```

The candidate may modify:

```text
admissible device relation
Context mapping
expected transition relation
recovery expectation
```

It must not automatically broaden unrelated behavior, privilege, network, or data-transfer allowances.

### 6.7 Guard Expectations

```text
Evidence provenance          = sufficient
Cross-evidence consistency   = sufficient
Challenge confirmation       = successful
Update magnitude             = bounded
Update direction             = Context-explainable
Discrimination preservation  = preserved
Rollback availability        = available
```

### 6.8 Expected Criterion Responses

```text
DEFER
→ ACCEPT
```

The first response may be `DEFER` while re-authentication and additional observations are collected.

After sufficient confirmation:

```text
D_crit = ACCEPT
```

### 6.9 Expected Criterion State Path

```text
STABLE
→ ADAPTING
→ STABLE
```

### 6.10 Final State

```text
Auth Decision       = AUTH_STABLE
Criterion State     = STABLE
Effective Criterion = A_1
Rollback Point      = A_0 retained
```

### 6.11 Expected Security Interpretation

This is legitimate adaptation because:

```text
the Context change is explicit
the update is supported by trusted evidence
challenge confirmation exists
the update remains bounded
discrimination is preserved
rollback remains possible
```

---

## 7. Scenario N2 — Legitimate Travel and Network Change

### 7.1 Objective

Demonstrate that a large spatial or network deviation does not automatically imply attack or criterion failure.

### 7.2 Initial State

```text
Criterion State       = STABLE
Auth Decision         = AUTH_STABLE
Effective Criterion   = A_0
Known Context         = home region / known network
```

### 7.3 Context Change

```text
home region
→ travel region

known network
→ hotel or mobile network
```

### 7.4 Evidence Sequence

```text
travel-related time relation is plausible
credential succeeds
new network appears
location relation changes
behavior remains mostly consistent
re-authentication succeeds
operation order remains consistent
no abrupt privilege escalation occurs
```

### 7.5 Expected Subject Trajectory

```text
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
→ AUTH_STABLE
```

### 7.6 Guard Expectations

```text
large raw deviation may exist
but
Context explanation exists
challenge succeeds
cross-evidence consistency remains sufficient
trajectory direction indicates re-convergence
```

### 7.7 Expected Criterion Responses

```text
DEFER
→ ACCEPT
```

The criterion may temporarily admit a travel-specific Context without permanently treating all future remote networks as normal.

### 7.8 Required Constraint

```text
Context-specific acceptance
!=
global criterion broadening
```

### 7.9 Final State

```text
Auth Decision       = AUTH_STABLE
Criterion State     = STABLE
Effective Criterion = A_travel_context
```

The model should preserve the distinction between:

```text
travel Context admissibility
and
general unrestricted network admissibility
```

---

## 8. Scenario N3 — Legitimate Long-term Behavioral Change

### 8.1 Objective

Demonstrate that gradual change is not automatically poisoning.

A legitimate user may alter behavior over time because of:

```text
new work role
new accessibility requirement
new schedule
new application workflow
long-term physical or behavioral change
```

### 8.2 Evidence Sequence

```text
small behavioral deviation
→ persistent change
→ independent Context confirmation
→ repeated successful challenge or trusted activity
→ stable new behavior
```

### 8.3 Expected Distinguishing Features

Legitimate long-term change should have:

```text
traceable cause
consistent direction
cross-evidence support
stable post-change behavior
preserved discrimination
no hidden weakening of privilege or challenge rules
```

### 8.4 Expected Criterion Responses

```text
DEFER
→ ACCEPT
```

or, when automated confidence is insufficient:

```text
DEFER
→ REVIEW
→ ACCEPT
```

### 8.5 Final State

The updated criterion may move, but only after the change becomes traceable as a legitimate Context-relative trajectory.

---

## 9. Scenario P1 — Gradual Region Expansion Poisoning

### 9.1 Objective

Demonstrate how repeated sub-threshold deviations can gradually broaden the admissible criterion until malicious behavior is incorporated.

### 9.2 Initial State

```text
Criterion State       = STABLE
Auth Decision         = AUTH_STABLE
Effective Criterion   = A_0
Admissible Region     = narrow enough to discriminate normal and malicious behavior
Rollback Point        = A_0
```

### 9.3 Attacker Strategy

The attacker produces small deviations that remain below immediate failure thresholds.

Example:

```text
Stage 1:
slightly larger data access

Stage 2:
slightly more external transfer

Stage 3:
slightly broader operation order

Stage 4:
repeated expansion of transfer and access behavior

Stage 5:
large malicious transfer appears normal under the contaminated criterion
```

### 9.4 Unconstrained Update Path

Without Guarded Criterion Update:

```text
A_0
→ A_1
→ A_2
→ A_3
→ A_4
→ poisoned criterion
```

Each small change is incorporated as a new normal.

```text
small malicious deviation
→ automatic acceptance
→ admissible region expansion
→ discrimination decline
```

### 9.5 Guarded Update Path

With GyroAuth guarded adaptation:

```text
Stage 1: ACCEPT or DEFER
Stage 2: DEFER
Stage 3: FREEZE
Stage 4: REVIEW or ROLLBACK
```

### 9.6 Observable Signals

```text
persistent outward update direction
repeated same-direction criterion movement
increasing region width
weak or missing Context explanation
insufficient challenge confirmation
reduced separation between normal and malicious trajectories
```

### 9.7 Expected Auth Decisions

The current access relation may remain temporarily valid.

Possible path:

```text
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
```

The simulation must preserve the possibility of:

```text
AUTH_STABLE + FREEZE
```

This means:

```text
current access may continue temporarily
while criterion adaptation is stopped
```

### 9.8 Expected Criterion Responses

```text
DEFER
→ FREEZE
→ REVIEW
or
DEFER
→ FREEZE
→ ROLLBACK
```

### 9.9 Expected Criterion State Path

```text
STABLE
→ ADAPTING
→ UNCERTAIN
→ FROZEN
→ UNDER_REVIEW
or
→ ROLLED_BACK
```

### 9.10 Success and Failure Conditions

Guarded model success:

```text
criterion expansion is halted
before malicious behavior becomes admissible
```

Guarded model failure:

```text
poisoned behavior is accepted
and discrimination collapses
before FREEZE or ROLLBACK
```

---

## 10. Scenario P2 — Criterion Translation Poisoning

### 10.1 Objective

Demonstrate poisoning that moves the center of the criterion rather than merely widening it.

### 10.2 Attacker Strategy

```text
normal behavior center = c_0
attacker gradually shifts observed behavior
c_0 → c_1 → c_2 → c_3
```

The admissible region width may remain approximately constant while the center moves toward attacker behavior.

### 10.3 Observable Signals

```text
persistent same-direction criterion movement
weak Context explanation
absence of trusted re-authentication
trajectory moves away from trusted rollback points
increasing mismatch with independent Evidence
```

### 10.4 Expected Criterion Responses

```text
DEFER
→ FREEZE
→ ROLLBACK
```

### 10.5 Expected Distinction

```text
stable width
!=
stable criterion
```

The simulation must not identify poisoning only by region expansion.

---

## 11. Scenario P3 — Evidence Priority Poisoning

### 11.1 Objective

Demonstrate an attacker attempting to alter which Evidence sources dominate the authentication decision.

### 11.2 Attacker Strategy

Example:

```text
behavioral Evidence becomes inconsistent
attacker-controlled location Evidence remains apparently valid
criterion update increases location weight
criterion update decreases challenge or behavior weight
```

### 11.3 Poisoning Effect

```text
Evidence Priority:
behavior / challenge / device
→
attacker-controlled location
```

### 11.4 Required Guard Property

A criterion update must not be accepted solely because one high-weight Evidence source supports it when that source is also the object of the proposed reweighting.

```text
self-supporting Evidence reweighting
!=
sufficient update justification
```

### 11.5 Expected Responses

```text
FREEZE
or
REVIEW
```

If a trusted earlier criterion exists and unauthorized reweighting has already occurred:

```text
ROLLBACK
```

---

## 12. Scenario P4 — Challenge Requirement Weakening

### 12.1 Objective

Demonstrate poisoning that weakens when explicit verification is required.

### 12.2 Attacker Strategy

```text
small deviations occur repeatedly
re-authentication is repeatedly avoided
criterion update gradually raises challenge threshold
future suspicious activity no longer triggers REAUTH_REQUIRED
```

### 12.3 Observable Signals

```text
challenge threshold moves in one permissive direction
no trusted evidence supports the weakening
false acceptance risk increases
protected policy anchor is contradicted
```

### 12.4 Expected Responses

```text
FREEZE
→ REVIEW
```

If protected policy requires a minimum challenge rule, the update candidate must not be accepted.

```text
Protected Anchor contradiction
→ ACCEPT forbidden
```

---

## 13. Scenario P5 — History-window Poisoning

### 13.1 Objective

Demonstrate manipulation of the retained history so that suspicious prior behavior disappears from evaluation.

### 13.2 Attacker Strategy

```text
reduce history window
increase time decay
remove prior suspicious stages
retain only recent attacker-shaped behavior
```

### 13.3 Poisoning Effect

```text
criterion appears stable
because contrary history is no longer visible
```

### 13.4 Expected Guard Checks

```text
history retention policy consistency
provenance linkage
rollback linkage
unexpected window contraction
loss of discrimination evidence
```

### 13.5 Expected Responses

```text
FREEZE
→ REVIEW
or
ROLLBACK
```

---

## 14. Scenario P6 — Rollback-link Poisoning

### 14.1 Objective

Demonstrate an attacker attempting to remove or redirect trusted rollback points.

### 14.2 Attacker Strategy

```text
replace trusted rollback pointer
mark poisoned criterion as trusted
remove linkage to A_0
```

### 14.3 Required Invariant

```text
ROLLBACK
→ VerifiedRollbackPoint
```

A rollback target must be authenticated, provenance-linked, and earlier than the suspected contamination interval.

### 14.4 Expected Responses

```text
FREEZE
→ REVIEW
```

If no verified rollback point remains:

```text
ROLLBACK unavailable
```

The system must not fabricate a trusted recovery state.

---

## 15. Scenario C1 — Single Evidence Source Compromise

### 15.1 Objective

Demonstrate that one compromised Evidence source must not automatically authorize a criterion update.

### 15.2 Example

```text
location Evidence = apparently normal
network Evidence  = inconsistent
device Evidence   = inconsistent
behavior Evidence = inconsistent
challenge result  = missing
```

### 15.3 Expected Subject Decision

```text
RECONVERGING
or
REAUTH_REQUIRED
```

### 15.4 Expected Criterion Response

```text
DEFER
or
FREEZE
```

### 15.5 Required Property

```text
single Evidence match
!=
criterion update acceptance
```

---

## 16. Scenario C2 — Multi-source Coordinated Compromise

### 16.1 Objective

Define a boundary case in which multiple Evidence sources are compromised simultaneously.

### 16.2 Example

```text
location manipulated
network manipulated
device identifiers cloned
behavior replayed
challenge channel compromised
```

### 16.3 Expected Model Position

If all relevant Evidence sources, anchors, and rollback links are compromised, GyroAuth does not claim reliable detection or recovery.

```text
all Evidence sources compromised
+
all anchors compromised
+
all rollback points compromised
→
security claim unavailable
```

### 16.4 Simulation Role

This scenario is primarily a limitation case rather than a success case.

---

## 17. Normal Update vs Poisoned Update Comparison

| Dimension | Normal Update | Poisoned Update |
|---|---|---|
| Context explanation | Present and traceable | Missing, weak, or contradictory |
| Evidence provenance | Trusted or sufficiently supported | Untrusted, manipulated, or self-referential |
| Cross-evidence consistency | Sufficient | Decreasing or strategically selective |
| Challenge confirmation | Successful when required | Avoided, weakened, or compromised |
| Update magnitude | Bounded and explainable | Cumulative or disproportionate |
| Update direction | Context-relative and stabilizing | Persistent movement toward attacker behavior |
| Update rate | Compatible with legitimate change | Sub-threshold but strategically sustained |
| Region width | Bounded | Expanding or silently contracting |
| Criterion center | Context-explainable | Shifted toward attacker behavior |
| Evidence priority | Preserved or justified | Reweighted toward attacker-controlled sources |
| Discrimination | Preserved | Declining or collapsed |
| History linkage | Retained | Reduced, truncated, or poisoned |
| Rollback linkage | Preserved | Removed, redirected, or invalidated |
| Expected response | ACCEPT, possibly after DEFER/REVIEW | DEFER, FREEZE, REVIEW, or ROLLBACK |

---

## 18. Response Semantics in Scenarios

### 18.1 ACCEPT

Use when:

```text
supporting Evidence is sufficient
critical Guard conditions pass
update remains bounded
Context explanation is coherent
discrimination is preserved
rollback linkage remains valid
```

Effect:

```text
A_(t+1) = A*_(t+1)
```

### 18.2 DEFER

Use when:

```text
Evidence may become sufficient
but current evidence is incomplete
```

Effect:

```text
A_(t+1) = A_t
```

The candidate remains pending or is regenerated later.

### 18.3 FREEZE

Use when:

```text
update path itself appears unsafe
repeated suspicious drift is present
provenance is compromised
critical Guard conditions fail
```

Effect:

```text
A_(t+1) = A_t
AdaptiveUpdateEnabled = false
```

### 18.4 REVIEW

Use when:

```text
automated evaluation cannot resolve the update safely
policy or administrator judgment is required
```

Effect:

```text
A_(t+1) = A_t
External or higher-assurance review required
```

### 18.5 ROLLBACK

Use when:

```text
criterion contamination is confirmed or strongly supported
and
a verified rollback point exists
```

Effect:

```text
A_(t+1) = A_tau
```

---

## 19. Required Simulation Assertions

The Priority G and H implementation should verify at least the following assertions.

### Assertion F-1 — Legitimate Adaptation

```text
A legitimate Context change with trusted support
can eventually produce ACCEPT.
```

### Assertion F-2 — Candidate Separation

```text
A Criterion Update Candidate never becomes effective
without an explicit Criterion Update Response.
```

### Assertion F-3 — Suspicious Drift Containment

```text
Persistent suspicious criterion movement
can produce DEFER or FREEZE before full poisoning.
```

### Assertion F-4 — Decision Separation

```text
AUTH_STABLE + FREEZE
is representable.
```

### Assertion F-5 — Rollback Authenticity

```text
ROLLBACK is impossible without a verified rollback point.
```

### Assertion F-6 — Discrimination Preservation

```text
ACCEPT is forbidden when the candidate silently collapses
normal-versus-malicious trajectory discrimination.
```

### Assertion F-7 — Context-specificity

```text
A Context-specific legitimate update
must not automatically broaden unrelated Contexts.
```

### Assertion F-8 — Evidence Diversity

```text
One compromised Evidence source
must not independently authorize criterion adoption.
```

### Assertion F-9 — Poisoning Diversity

```text
The model must detect candidate poisoning through
region expansion, center translation, evidence reweighting,
history manipulation, challenge weakening, or rollback-link attack.
```

### Assertion F-10 — Non-Guarantee Boundary

```text
The model must explicitly report that reliable detection
is not guaranteed when all Evidence, anchors, and rollback points
are simultaneously compromised.
```

---

## 20. Minimum Scenario Set for the First PoC

The first PoC does not need to implement every scenario.

The minimum required set is:

```text
Scenario N1:
Legitimate New Device Transition

Scenario P1:
Gradual Region Expansion Poisoning

Scenario C1:
Single Evidence Source Compromise
```

Recommended fourth scenario:

```text
Scenario P2:
Criterion Translation Poisoning
```

This set is sufficient to demonstrate:

```text
normal adaptation
versus
guarded poisoning containment
```

and:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 21. Suggested Scenario Data Shape

A later JSON representation may use:

```json
{
  "scenario_id": "N1",
  "stage": 0,
  "context": {},
  "evidence": {},
  "subject_state": {
    "deviation": {},
    "stability": 0.0,
    "trajectory_continuity": 0.0,
    "auth_decision": "AUTH_STABLE"
  },
  "criterion_state": {
    "state": "STABLE",
    "effective_criterion": {},
    "candidate": {},
    "guard": {},
    "integrity": 0.0,
    "response": "DEFER",
    "rollback_point": null
  },
  "expected": {
    "auth_decision": "AUTH_STABLE",
    "criterion_response": "DEFER",
    "next_criterion_state": "ADAPTING"
  }
}
```

This is a scenario interchange candidate, not yet a canonical API schema.

---

## 22. Security Interpretation Boundaries

Successful simulation of these scenarios may support claims that:

```text
criterion updates are separately evaluated
normal adaptation and poisoning can be represented differently
suspicious gradual drift can trigger bounded responses
criterion updates can be frozen without automatically failing authentication
verified rollback points can support recovery
```

It does not prove:

```text
complete prevention of criterion poisoning
detection of every attack
zero false acceptance
zero false rejection
security under total Evidence compromise
security under anchor compromise
security under runtime code compromise
perfect human identity proof
```

---

## 23. Priority F Outputs

Priority F fixes the following scenario position.

### Normal adaptation

```text
legitimate Context change
+
trusted supporting Evidence
+
bounded update
+
preserved discrimination
→
DEFER / REVIEW as needed
→
ACCEPT
```

### Poisoned adaptation

```text
persistent attacker-shaped movement
+
weak or manipulated provenance
+
declining discrimination
+
unsafe update direction
→
DEFER / FREEZE / REVIEW / ROLLBACK
```

### Central distinction

```text
small deviation
!=
legitimate update automatically
```

and:

```text
repeated observation
!=
new normal automatically
```

### Required PoC comparison

```text
Unconstrained Update Model
versus
Guarded Criterion Update Model
```

---

## 24. Next Step

The next step is:

```text
Priority G: Minimal Simulation Design
```

Priority G should specify:

```text
simulation variables
initial values
update equations
Guard equations
scenario input sequences
output tables
output graphs
evaluation metrics
reproducibility conditions
```

The first implementation should remain synthetic, discrete, bounded, and explicitly tied to the scenarios defined in this document.
