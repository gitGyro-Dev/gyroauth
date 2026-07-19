# GyroAuth Criterion Update State Machine

## 1. Purpose

This document completes **Priority E: Criterion Update State Machine** for the GyroAuth formalization and paper-preparation work.

It builds on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
docs/18_formal_security_model.md
```

Its purpose is to define the bounded state-transition semantics through which a Criterion Update Candidate is:

```text
accepted
deferred
frozen
reviewed
or rolled back
```

The state machine preserves the central security position:

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

This document prepares:

```text
Priority F: Normal and Poisoned Update Scenarios
Priority G: Minimal Simulation Design
Priority H: PoC Implementation and Results
```

It is not yet a production workflow, a complete security proof, or a replacement for GyroOS Operator Response.

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

The state machine introduced here is a GyroAuth application-layer model for Criterion Integrity and guarded criterion adaptation.

```text
Core change: none
GyroOS contract change: none
GyroAuth criterion-state model: added
```

---

## 3. Decision Separation

GyroAuth produces two different classes of decisions.

### 3.1 Auth Decision

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

This answers:

```text
May the current Authentication Relation continue?
```

### 3.2 Criterion Update Response

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

This answers:

```text
What should happen to the current criterion
or the proposed Criterion Update Candidate?
```

The two spaces must not be collapsed.

```text
Auth Decision
!=
Criterion Update Response
```

Examples:

```text
AUTH_STABLE + FREEZE
```

means that the current Authentication Relation may continue while criterion adaptation is suspended.

```text
REAUTH_REQUIRED + DEFER
```

means that explicit verification is required and the criterion update remains unaccepted.

```text
AUTH_STABLE + REVIEW
```

means that access may continue provisionally while criterion adaptation requires external or policy-level review.

A Criterion Update Response does not directly assert that the Expected Identity is valid or invalid.

---

## 4. State and Response Must Be Separated

A **Criterion State** describes the current condition of the effective criterion.

A **Criterion Update Response** describes the operation selected for the current update candidate or effective criterion.

```text
Criterion State
!=
Criterion Update Response
```

For example:

```text
State: UNCERTAIN
Response: DEFER
```

```text
State: SUSPECTED_COMPROMISE
Response: FREEZE
```

```text
State: COMPROMISED
Response: ROLLBACK
```

The same response may be selected from more than one state when different guard conditions produce the same bounded action.

---

## 5. Criterion State Set

Let the Criterion State set be:

```text
Q_crit = {
  STABLE,
  ADAPTING,
  UNCERTAIN,
  FROZEN,
  UNDER_REVIEW,
  COMPROMISED,
  ROLLED_BACK
}
```

### 5.1 STABLE

> The currently effective Authentication Criterion is sufficiently supported, traceable, and usable as the basis for Subject Evaluation.

A STABLE state does not mean:

```text
perfect criterion
zero risk
zero false acceptance
zero false rejection
permanent immutability
```

It means that no current condition requires adaptation suspension, review, or rollback.

### 5.2 ADAPTING

> A Criterion Update Candidate is being evaluated as a potentially legitimate Context-relative adaptation, but has not yet been fully incorporated as the effective criterion.

ADAPTING preserves:

```text
candidate separation
provenance linkage
bounded update magnitude
rollback linkage
```

The effective criterion remains identifiable throughout the transition.

### 5.3 UNCERTAIN

> Available Evidence is insufficient, inconsistent, or incomplete for accepting or rejecting the Criterion Update Candidate.

UNCERTAIN is not equivalent to compromise.

It means:

```text
insufficient evidence
ambiguous context transition
cross-evidence inconsistency
incomplete challenge result
unstable update direction
```

The default response is normally DEFER, but REVIEW or FREEZE may be selected when risk is elevated.

### 5.4 FROZEN

> Adaptive criterion updates are suspended while the last accepted effective criterion is preserved.

FROZEN does not necessarily stop current authentication processing.

```text
Criterion update frozen
!=
Authentication Relation automatically failed
```

The system may continue Subject Evaluation using the preserved effective criterion, protected anchors, or a restricted policy.

### 5.5 UNDER_REVIEW

> Automated criterion-update selection is insufficient, and an external policy, independent validation path, or authorized reviewer must determine the next action.

UNDER_REVIEW changes the decision authority or validation path.

It is not merely waiting for more of the same Evidence.

```text
REVIEW
!=
DEFER
```

### 5.6 COMPROMISED

> The currently effective criterion or its update trajectory is judged sufficiently contaminated, untraceable, or integrity-violating that it must no longer be treated as a reliable evaluation basis.

Examples include:

```text
confirmed criterion poisoning
untrusted provenance incorporated into the criterion
silent discrimination collapse
protected update rule tampering
rollback linkage corruption
```

COMPROMISED does not itself identify who performed the attack.

### 5.7 ROLLED_BACK

> The effective criterion has been restored to a verified prior Rollback Point.

ROLLED_BACK is a recovery state, not automatically a final stable state.

The restored criterion must still be revalidated under the current Context.

```text
ROLLED_BACK
→ validation
→ STABLE or ADAPTING or UNDER_REVIEW
```

---

## 6. Criterion Update Response Semantics

Let:

```text
a_t
```

be the current effective Authentication Criterion, and:

```text
a*_(t+1)
```

be the Criterion Update Candidate.

### 6.1 ACCEPT

> Adopt the Criterion Update Candidate as the next effective Authentication Criterion.

```text
a_(t+1) = a*_(t+1)
```

ACCEPT requires all mandatory guards for the applicable policy to pass.

At minimum, ACCEPT should preserve:

```text
provenance traceability
anchor compatibility
update-bound compliance
discrimination preservation
rollback linkage
```

ACCEPT does not mean that the candidate becomes permanently trusted.

The accepted criterion remains subject to later Criterion Integrity Evaluation.

### 6.2 DEFER

> Do not adopt the candidate yet; preserve the current effective criterion and continue bounded observation or evidence collection.

```text
a_(t+1) = a_t
```

DEFER is appropriate when:

```text
evidence is insufficient
context transition is incomplete
challenge result is pending
candidate direction is not yet readable
short-term deviation may still reconverge
```

DEFER does not authorize silent background adoption.

### 6.3 FREEZE

> Suspend adaptive criterion updates and preserve the last accepted effective criterion.

```text
a_(t+1) = a_t
UpdateEnabled_(t+1) = false
```

FREEZE is stronger than DEFER.

DEFER waits for additional support for one candidate.

FREEZE suspends the update mechanism or update class because the update path itself may be unsafe.

Typical triggers:

```text
poisoning indication
repeated sub-threshold drift
abnormal region expansion
provenance conflict
challenge weakening
rollback-link anomaly
```

### 6.4 REVIEW

> Suspend automated adoption and transfer the candidate or criterion state to an independent validation path.

```text
a_(t+1) = a_t
AutomatedUpdate_(t+1) = suspended
ExternalValidation_(t+1) = required
```

REVIEW may involve:

```text
administrator decision
protected policy engine
independent evidence source
manual security investigation
higher-assurance re-authentication
```

REVIEW is selected when the system cannot safely resolve the update using the available automated model.

### 6.5 ROLLBACK

> Replace the current effective criterion with a verified prior criterion state.

Let:

```text
p_tau = (a_tau, meta_tau)
```

be a trusted Rollback Point where `tau < t`.

Then:

```text
a_(t+1) = a_tau
```

ROLLBACK requires verification of:

```text
rollback authenticity
rollback integrity
rollback compatibility
rollback chronology
```

ROLLBACK must not select an arbitrary prior state.

```text
old criterion
!=
trusted rollback point automatically
```

---

## 7. Guard Inputs

Let the guard evaluation at stage `t` be:

```text
g_t = Guard(
  a_t,
  a*_(t+1),
  T_t^obs,
  c_(t+1),
  e_t^upd,
  h_t,
  b_t,
  p_t
)
```

where:

```text
a_t         = current effective criterion
a*_(t+1)    = update candidate
T_t^obs     = Observed Access Trajectory
c_(t+1)     = candidate Context
e_t^upd     = update Evidence
h_t         = retained History
b_t         = Trusted Anchor state
p_t         = Rollback Point state
```

The guard result is not required to be one scalar.

A provisional guard vector is:

```text
g_t = (
  g_prov,
  g_anchor,
  g_magnitude,
  g_direction,
  g_rate,
  g_cross,
  g_challenge,
  g_discrimination,
  g_rollback,
  g_history
)
```

with:

```text
g_prov            = Evidence provenance validity
g_anchor          = protected-anchor compatibility
g_magnitude       = update magnitude admissibility
g_direction       = update direction admissibility
g_rate            = update rate admissibility
g_cross           = cross-evidence consistency
g_challenge       = challenge or re-auth support
g_discrimination  = discrimination preservation
g_rollback        = rollback availability and integrity
g_history         = history-window integrity
```

A policy may classify each component as:

```text
PASS
WEAK_PASS
UNKNOWN
FAIL
CRITICAL_FAIL
```

The state machine should not reduce a CRITICAL_FAIL to an average scalar that can be cancelled by unrelated positive Evidence.

---

## 8. Mandatory and Non-compensable Guards

Some guard conditions may be weighted or Context-relative.

Others must be non-compensable.

Candidate non-compensable guards include:

```text
protected-anchor integrity
rollback authenticity
provenance integrity for mandatory Evidence
response-policy integrity
no confirmed discrimination collapse
```

Therefore:

```text
high aggregate score
+
critical anchor failure
!=
ACCEPT
```

A candidate cannot be accepted merely because unrelated Evidence raises an average score.

This prevents important integrity failures from being hidden inside a composite metric.

---

## 9. Transition Function

Let:

```text
q_t ∈ Q_crit
```

be the current Criterion State.

Let:

```text
r_t^crit ∈ {
  ACCEPT,
  DEFER,
  FREEZE,
  REVIEW,
  ROLLBACK
}
```

be the selected Criterion Update Response.

The state transition is:

```text
q_(t+1) = Transition_crit(q_t, g_t, r_t^crit, h_t)
```

The effective criterion transition is:

```text
a_(t+1) = Transition_A(
  a_t,
  a*_(t+1),
  r_t^crit,
  p_t
)
```

The state transition and criterion-content transition are related but distinct.

---

## 10. High-level Transition Table

| Current State | Guard / Condition | Response | Next State | Effective Criterion |
|---|---|---|---|---|
| STABLE | no candidate | DEFER or no-op | STABLE | preserve `a_t` |
| STABLE | supported bounded candidate | ACCEPT | STABLE | adopt `a*_(t+1)` |
| STABLE | candidate needs more Evidence | DEFER | UNCERTAIN | preserve `a_t` |
| STABLE | suspicious update trajectory | FREEZE | FROZEN | preserve `a_t` |
| STABLE | automated resolution insufficient | REVIEW | UNDER_REVIEW | preserve `a_t` |
| ADAPTING | all mandatory guards pass | ACCEPT | STABLE | adopt candidate |
| ADAPTING | support remains incomplete | DEFER | UNCERTAIN | preserve `a_t` |
| ADAPTING | poisoning indication emerges | FREEZE | FROZEN | preserve `a_t` |
| ADAPTING | policy escalation required | REVIEW | UNDER_REVIEW | preserve `a_t` |
| UNCERTAIN | stronger Evidence validates candidate | ACCEPT | STABLE | adopt candidate |
| UNCERTAIN | insufficient Evidence remains | DEFER | UNCERTAIN | preserve `a_t` |
| UNCERTAIN | risk increases | FREEZE | FROZEN | preserve `a_t` |
| UNCERTAIN | ambiguity cannot be resolved automatically | REVIEW | UNDER_REVIEW | preserve `a_t` |
| FROZEN | candidate invalidated; current criterion remains valid | DEFER | STABLE | preserve `a_t` |
| FROZEN | protected validation supports new candidate | ACCEPT | STABLE | adopt candidate |
| FROZEN | compromise suspected but unresolved | REVIEW | UNDER_REVIEW | preserve `a_t` |
| FROZEN | contamination confirmed | ROLLBACK | ROLLED_BACK | restore `a_tau` |
| UNDER_REVIEW | reviewer approves candidate | ACCEPT | STABLE | adopt candidate |
| UNDER_REVIEW | reviewer rejects candidate but current criterion valid | DEFER | STABLE | preserve `a_t` |
| UNDER_REVIEW | reviewer requires continued suspension | FREEZE | FROZEN | preserve `a_t` |
| UNDER_REVIEW | compromise confirmed | ROLLBACK | ROLLED_BACK | restore `a_tau` |
| COMPROMISED | trusted rollback available | ROLLBACK | ROLLED_BACK | restore `a_tau` |
| COMPROMISED | rollback unavailable or invalid | REVIEW | UNDER_REVIEW | criterion not silently reused |
| ROLLED_BACK | restored criterion validates in current Context | DEFER or no-op | STABLE | preserve restored criterion |
| ROLLED_BACK | legitimate adaptation still required | DEFER | ADAPTING | preserve restored criterion while generating candidate |
| ROLLED_BACK | rollback incompatible with current Context | REVIEW | UNDER_REVIEW | preserve restricted fallback |

`no-op` may be represented internally without adding a sixth Criterion Update Response if no update candidate exists.

---

## 11. State-specific Entry Conditions

### 11.1 Enter STABLE

Enter or remain in STABLE when:

```text
all mandatory integrity guards pass
criterion provenance remains traceable
no unresolved poisoning indication exists
discrimination remains above the required bound
rollback linkage remains valid
```

### 11.2 Enter ADAPTING

Enter ADAPTING when:

```text
a legitimate Context change is readable
an update candidate is generated
candidate support is non-trivial
no critical guard has failed
candidate adoption is not yet complete
```

### 11.3 Enter UNCERTAIN

Enter UNCERTAIN when:

```text
supporting Evidence is incomplete
cross-evidence results conflict
challenge result is pending
update direction is temporarily unreadable
candidate may be legitimate but is not yet admissible
```

### 11.4 Enter FROZEN

Enter FROZEN when:

```text
criterion poisoning is indicated
candidate updates repeatedly widen or move the region
mandatory provenance is missing or inconsistent
update policy integrity is uncertain
history-window manipulation is suspected
```

### 11.5 Enter UNDER_REVIEW

Enter UNDER_REVIEW when:

```text
automated guard evaluation is insufficient
policy requires human authorization
multiple trusted sources conflict
rollback selection requires external validation
high-impact criterion change is requested
```

### 11.6 Enter COMPROMISED

Enter COMPROMISED when:

```text
criterion poisoning is confirmed
protected anchors were violated
silent discrimination collapse is established
an untrusted candidate was adopted
criterion-update policy was modified without authorization
```

### 11.7 Enter ROLLED_BACK

Enter ROLLED_BACK only when:

```text
a trusted Rollback Point is selected
rollback integrity is verified
rollback application succeeds
rollback event is appended to protected History
```

---

## 12. Response Selection Rules

A provisional response selection function is:

```text
r_t^crit = Pi_crit(
  q_t,
  g_t,
  delta_t^crit,
  k_t^crit,
  h_t^crit,
  policy_t
)
```

where:

```text
delta_t^crit = Criterion Deviation
k_t^crit     = Criterion Stability or integrity-related result
h_t^crit     = Criterion update History
policy_t     = current protected policy
```

The response selection must satisfy the following ordering constraints.

### 12.1 Critical integrity failure dominates ACCEPT

```text
CriticalGuardFail(g_t)
→
r_t^crit != ACCEPT
```

### 12.2 Confirmed compromise requires containment or recovery

```text
ConfirmedCompromise(q_t, g_t)
→
r_t^crit ∈ {FREEZE, REVIEW, ROLLBACK}
```

### 12.3 Insufficient Evidence cannot silently become acceptance

```text
EvidenceInsufficient(g_t)
→
r_t^crit ∈ {DEFER, REVIEW, FREEZE}
```

### 12.4 Rollback requires a verified point

```text
r_t^crit = ROLLBACK
→
ExistsVerifiedRollbackPoint(p_tau)
```

### 12.5 ACCEPT requires bounded candidate change

```text
r_t^crit = ACCEPT
→
BoundedUpdate(a_t, a*_(t+1))
```

unless an explicitly authorized high-assurance migration policy is invoked.

---

## 13. Formal Transition Schema

The next effective criterion is:

```text
a_(t+1) =

  a*_(t+1)
    if r_t^crit = ACCEPT

  a_t
    if r_t^crit ∈ {DEFER, FREEZE, REVIEW}

  a_tau
    if r_t^crit = ROLLBACK
    and VerifiedRollbackPoint(a_tau)
```

The next Criterion State is:

```text
q_(t+1) =

  STABLE
    if ACCEPT and all post-adoption checks pass

  UNCERTAIN
    if DEFER and additional Evidence is required

  FROZEN
    if FREEZE

  UNDER_REVIEW
    if REVIEW

  ROLLED_BACK
    if ROLLBACK succeeds

  COMPROMISED
    if compromise is confirmed and recovery is not yet completed
```

Post-adoption checks are necessary because ACCEPT is a transition decision, not permanent proof.

---

## 14. Freeze Semantics

FREEZE must be explicit about what is frozen.

Possible freeze scopes include:

```text
one update candidate
one Evidence class
one Context-transition rule
one criterion component
all adaptive updates for one Session
all adaptive updates for one Expected Identity
system-wide adaptive updates
```

The formal model records:

```text
FreezeScope_t
FreezeReason_t
FreezeStart_t
FreezeReleaseCondition_t
```

A freeze without scope or release conditions risks becoming either ineffective or permanent.

FREEZE should preserve:

```text
last accepted criterion
protected history
rollback points
current guard evidence
candidate rejection status
```

---

## 15. Review Semantics

REVIEW must record:

```text
ReviewReason
ReviewAuthority
RequiredEvidence
Deadline or bounded review window
Allowed interim Auth Decisions
Allowed interim update operations
```

Possible interim rules include:

```text
continue low-risk access
require re-authentication
limit privileges
isolate sensitive operations
preserve current criterion
forbid candidate adoption
```

These are GyroAuth application-level policy choices and do not redefine GyroOS Operator Response.

---

## 16. Rollback Semantics

A Rollback Point must contain or reference:

```text
criterion content
creation stage
supporting Evidence
provenance summary
anchor state
policy version
integrity proof or verification record
parent criterion reference
```

A rollback operation records:

```text
source criterion
restored criterion
rollback reason
rollback authority
invalidated candidates
affected Contexts
post-rollback validation result
```

Rollback does not erase history.

```text
rollback
!=
history deletion
```

The Criterion Trajectory must retain that a rollback occurred and why.

---

## 17. Criterion Trajectory Events

Each criterion transition should append an event such as:

```text
CriterionEvent_t = {
  stage,
  previous_state,
  candidate_id,
  guard_result,
  selected_response,
  next_state,
  previous_criterion_ref,
  next_criterion_ref,
  provenance_ref,
  rollback_ref,
  reason
}
```

The event log alone is not the Criterion Trajectory.

```text
Criterion event history
!=
Criterion Trajectory
```

The Trajectory is the readable relational configuration through which these transitions, Evidence, causes, and responses are traced.

---

## 18. Invariants

The state machine must preserve the following invariants.

### INV-E1 Candidate Separation

```text
a*_(t+1) != a_(t+1)
unless ACCEPT is selected
```

### INV-E2 Decision Separation

```text
Auth Decision
!=
Criterion Update Response
```

### INV-E3 Freeze Preservation

```text
FREEZE
→
a_(t+1) = a_t
```

unless a separately authorized ROLLBACK occurs.

### INV-E4 Review Preservation

```text
REVIEW
→
a_(t+1) = a_t
```

until an authorized review result selects another response.

### INV-E5 Rollback Authenticity

```text
ROLLBACK
→
VerifiedRollbackPoint(a_tau)
```

### INV-E6 Provenance Retention

Every ACCEPT, FREEZE, REVIEW, and ROLLBACK transition must remain linked to its supporting Evidence and reason.

### INV-E7 No Silent Discrimination Collapse

A candidate must not be accepted when the system has evidence that its adoption destroys the required distinction between admissible and malicious trajectories.

### INV-E8 No Critical-failure Averaging

A CRITICAL_FAIL on a non-compensable guard cannot be cancelled by unrelated positive guard values.

### INV-E9 Bounded Execution

Each state-machine step must terminate with one bounded response or explicit no-candidate result.

### INV-E10 Recovery Traceability

Rollback and post-rollback adaptation must remain visible in Criterion History and Criterion Trajectory.

---

## 19. Normal Adaptation Path

A normal Context transition may follow:

```text
STABLE
→ candidate generated
→ ADAPTING
→ provenance verified
→ challenge succeeds
→ cross-evidence consistency confirmed
→ ACCEPT
→ STABLE
```

Example:

```text
known device
→ new device
→ REAUTH_REQUIRED
→ successful re-authentication
→ bounded candidate update
→ ACCEPT
→ AUTH_STABLE
```

The Auth Decision and Criterion Update Response remain independent throughout the path.

---

## 20. Poisoning Containment Path

A gradual poisoning attempt may follow:

```text
STABLE
→ repeated small candidate changes
→ ADAPTING
→ abnormal update direction detected
→ UNCERTAIN
→ repeated sub-threshold expansion
→ FREEZE
→ FROZEN
→ review confirms contamination
→ ROLLBACK
→ ROLLED_BACK
→ post-rollback validation
→ STABLE
```

Without the guard and state machine, the same sequence may become:

```text
candidate
→ automatic adoption
→ candidate
→ automatic adoption
→ poisoned criterion
```

The guarded model makes the difference explicit.

---

## 21. Failure and Degraded Modes

### 21.1 No valid Rollback Point

If compromise is confirmed but no trusted Rollback Point exists:

```text
COMPROMISED
→ REVIEW
```

The system must not silently reuse the compromised criterion.

### 21.2 All mandatory Evidence unavailable

```text
UNCERTAIN
→ DEFER or FREEZE or REVIEW
```

not ACCEPT.

### 21.3 Protected Anchor failure

```text
Critical anchor failure
→ FREEZE or REVIEW
```

and possibly COMPROMISED depending on policy.

### 21.4 Review timeout

A review timeout must have an explicit policy outcome such as:

```text
continue restricted mode
require re-authentication
remain frozen
rollback to trusted criterion
terminate high-risk access
```

No silent acceptance is allowed.

### 21.5 State-machine implementation failure

If the Criterion Update State Machine cannot determine a valid transition:

```text
fail closed for criterion adaptation
```

This means preserve the current criterion or enter REVIEW/FROZEN according to policy.

It does not automatically imply AUTH_FAIL.

---

## 22. Minimal Simulation Reduction

For the first simulation, the full state set may be reduced to:

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
ROLLED_BACK
```

with responses:

```text
ACCEPT
DEFER
FREEZE
ROLLBACK
```

REVIEW may be represented as an external terminal or suspended state.

Minimum transition logic:

```text
if critical_guard_fail:
    FREEZE
elif confirmed_poisoning and valid_rollback:
    ROLLBACK
elif evidence_insufficient:
    DEFER
elif all_required_guards_pass:
    ACCEPT
else:
    DEFER
```

This reduction is only for the first PoC.

It does not remove REVIEW from the formal model.

---

## 23. Properties to Test in Priority F and G

The next phases should test at least:

```text
P1 legitimate candidate can reach ACCEPT
P2 insufficient Evidence cannot reach ACCEPT
P3 critical guard failure cannot reach ACCEPT
P4 FREEZE preserves the effective criterion
P5 ROLLBACK selects only a verified point
P6 repeated sub-threshold poisoning eventually triggers containment
P7 normal Context adaptation does not remain permanently frozen
P8 Auth Decision and Criterion Update Response remain independent
P9 rollback events remain traceable
P10 no unresolved transition silently adopts a candidate
```

---

## 24. Open Questions

The following remain open for later refinement:

1. Which guards are mandatory in every deployment?
2. Which guards may be Context-relative or weighted?
3. How should Criterion Stability be numerically represented?
4. How long may UNCERTAIN or UNDER_REVIEW persist?
5. Which freeze scopes are required for the first PoC?
6. How is discrimination preservation measured without a real dataset?
7. How many trusted Rollback Points should be retained?
8. Can ACCEPT be provisional before becoming fully STABLE?
9. How should multiple concurrent Context updates be serialized or merged?
10. How should distributed GyroAuth instances coordinate criterion state?
11. Which transitions require explicit audit signatures?
12. How should privacy constraints limit retained Criterion History?

These questions do not block the first discrete simulation.

---

## 25. Priority E Outputs

Priority E fixes the following working structure.

### Criterion States

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

### Criterion Update Responses

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

### Central Transition Principle

```text
Candidate
→ Guard
→ Criterion Update Response
→ State Transition
→ Effective Criterion
```

not:

```text
Observation
→ Automatic Criterion Adoption
```

### Recovery Principle

```text
confirmed contamination
+
verified rollback point
→
ROLLBACK
→
post-rollback validation
```

### Separation Principle

```text
current access continuation
and
criterion adaptation approval
are evaluated separately
```

---

## 26. Handoff to Priority F

Priority F should define executable scenario specifications for at least:

```text
Scenario N1: legitimate new-device adaptation
Scenario N2: legitimate long-term behavior change
Scenario P1: gradual region expansion poisoning
Scenario P2: evidence-priority poisoning
Scenario P3: rollback-link attack or invalid rollback attempt
```

Each scenario should specify:

```text
initial Criterion State
initial effective criterion
input Evidence sequence
candidate updates
guard outcomes
Auth Decisions
Criterion Update Responses
state transitions
final effective criterion
expected security interpretation
```

Priority F must demonstrate the difference between:

```text
normal adaptive change
```

and:

```text
malicious or untraceable criterion change
```

without claiming complete attack prevention.

---

## 27. Layer Consistency Check

```text
Gyro Logic Core change: none
GyroOS execution contract change: none
GyroAuth criterion-state formalization: added
```

The state-machine states and Criterion Update Responses are GyroAuth application-layer concepts.

They do not replace or rename canonical GyroOS Operator Responses.

No change is made to:

```text
Structure
↓
Slice
↓
Stability
```
