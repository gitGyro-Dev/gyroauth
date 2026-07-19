# GyroAuth Threat Model

## 1. Purpose

This document completes **Priority C: Threat Model** for the GyroAuth formalization and paper-preparation work.

Its purpose is to define:

```text
what is protected
what the attacker wants
what the attacker can observe or manipulate
what remains trusted
which attacks are in scope
which attacks are out of scope
what effects GyroAuth is expected to observe
which response families are available
```

This document builds on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
```

It prepares:

```text
Priority D: Formal Security Model
Priority E: Criterion Update State Machine
Priority F: Normal and Poisoned Update Scenarios
Priority G: Minimal Simulation Design
```

This Threat Model does not claim complete attack prevention, complete identity proof, or production-grade assurance.

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

The Threat Model is limited to the GyroAuth application layer.

---

## 3. Security Objective

GyroAuth evaluates two related but distinct objects.

```text
1. Subject Evaluation
2. Criterion Integrity Evaluation
```

The first asks:

```text
Is the current Access Subject still admissibly related
to the Expected Identity?
```

The second asks:

```text
Is the current Authentication Criterion still admissible
as a basis for evaluating that relation?
```

The protected security objective is therefore not only:

```text
prevent an attacker from being accepted as the Expected Identity
```

It also includes:

```text
prevent an attacker from moving, broadening, weakening,
or contaminating the criterion until malicious behavior
is incorporated as normal
```

Central position:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 4. Protected Objects

The Threat Model protects the following objects and relations.

### 4.1 Authentication Relation

```text
current Access Subject
↔
Expected Identity
```

The protected property is whether this relation remains admissible and continuable under the current Session and Context.

### 4.2 Authentication Criterion

The currently effective Context-relative basis used to evaluate:

```text
Observed Evidence
Deviation
Stability
Observed Access Trajectory
History
response conditions
```

### 4.3 Criterion Update Process

The process by which a proposed criterion state is generated, evaluated, accepted, deferred, frozen, reviewed, or rolled back.

### 4.4 Criterion Trajectory

The traceable relational configuration of criterion changes, including:

```text
update cause
evidence origin
update magnitude
update direction
update rate
discrimination effect
response history
rollback linkage
```

### 4.5 Trusted History and Rollback Points

The minimum retained history required to distinguish:

```text
legitimate adaptation
from
gradual criterion poisoning
```

and to restore a prior trusted criterion when necessary.

### 4.6 Response Separation

The distinction between:

```text
Auth Decision
!=
Criterion Update Response
```

must be preserved.

An attacker must not be able to collapse:

```text
current access continuation
```

and:

```text
criterion adaptation approval
```

into one uncontrolled decision.

---

## 5. Security Properties of Interest

The initial formalization studies the following properties.

### 5.1 Subject Continuity Discernibility

The model should retain enough relational information to distinguish:

```text
valid Session continuity
```

from:

```text
Authentication Relation Continuity
```

### 5.2 Guarded Adaptation

A Criterion Update Candidate must not become the next effective criterion without a separate update decision.

```text
Criterion Update Candidate
!=
Accepted Criterion
```

### 5.3 Criterion Traceability

A criterion change should remain linked to:

```text
supporting Evidence
Context
History
update cause
selected response
trusted anchor or rollback point
```

### 5.4 Discrimination Preservation

Criterion adaptation should not silently destroy the ability to distinguish admissible and malicious trajectories.

### 5.5 Recovery Support

When contamination is suspected or confirmed, the model should support:

```text
DEFER
FREEZE
REVIEW
ROLLBACK
```

without automatically declaring the Expected Identity invalid.

### 5.6 Decision Independence

The model should allow combinations such as:

```text
AUTH_STABLE + FREEZE
REAUTH_REQUIRED + DEFER
AUTH_STABLE + REVIEW
```

---

## 6. System Model

At evaluation stage `t`, the model provisionally includes:

```text
I            = Expected Identity
S_t          = current Session
C_t          = current Context
X_t          = interpreted authentication state
E_t          = Observed Evidence
T_t^obs      = Observed Access Trajectory
A_t          = effective Authentication Criterion
A*_(t+1)     = Criterion Update Candidate
H_t^auth     = subject-evaluation History
H_t^crit     = criterion-update History
R_t^auth     = Auth Decision
R_t^crit     = Criterion Update Response
```

A candidate update may be generated as:

```text
A*_(t+1) = U(A_t, T_t^obs, C_(t+1), E_t, H_t^crit)
```

but:

```text
A*_(t+1)
!=
A_(t+1)
```

The accepted next criterion depends on a guarded response.

---

## 7. Trust Boundaries

The model distinguishes five trust regions.

### 7.1 External Observation Sources

Examples:

```text
device telemetry
network telemetry
location or proximity source
behavioral signal
motion signal
credential result
challenge response
privilege transition
operation sequence
```

These sources may be:

```text
trusted
partially trusted
compromised
unavailable
inconsistent
```

No single source is universally trusted by definition.

### 7.2 GyroOS Execution Boundary

GyroAuth receives or interprets GyroOS-shaped results such as:

```text
slice-done
Deviation
Stability
Operator Response
History
```

This Threat Model does not redefine GyroOS execution semantics.

### 7.3 GyroAuth Evaluation Boundary

GyroAuth maps available execution results and Evidence into:

```text
Auth Decision
Criterion Integrity Evaluation
Criterion Update Response
```

### 7.4 Protected Anchor Boundary

Examples of protected anchors include:

```text
signed policy
high-assurance credential result
administrator-approved rule
protected rollback checkpoint
independent evidence source
append-only audit linkage
```

The initial model assumes at least one anchor or independent source remains trustworthy for guarded recovery claims.

### 7.5 Review Boundary

`REVIEW` transfers the criterion-update question to an external policy, administrator, or independent validation process.

The Threat Model does not assume that automated GyroAuth evaluation can resolve every uncertainty internally.

---

## 8. Adversary Goals

An adversary may pursue one or more of the following goals.

### G1. Unauthorized Continuation

Continue an Authentication Relation after the legitimate subject is no longer the effective operator.

### G2. Unauthorized Initial Acceptance

Cause an illegitimate Access Subject to be accepted as related to the Expected Identity.

### G3. Criterion Expansion

Broaden the admissible region until malicious behavior becomes accepted.

### G4. Criterion Translation

Gradually move the criterion toward attacker-controlled behavior.

### G5. Criterion Contraction

Narrow the criterion to cause denial, lockout, or excessive re-authentication for the legitimate user.

### G6. Evidence Manipulation

Alter one or more Evidence sources so that malicious behavior appears admissible.

### G7. History Manipulation

Remove, reorder, suppress, or fabricate history so that criterion drift becomes unreadable.

### G8. Rollback Suppression

Prevent restoration of a prior trusted criterion.

### G9. Review Avoidance

Keep malicious updates below the conditions that trigger `REVIEW`, `FREEZE`, or `ROLLBACK`.

### G10. Discrimination Collapse

Reduce the difference between legitimate and malicious trajectories until the criterion can no longer distinguish them reliably.

---

## 9. Adversary Capabilities

The Threat Model considers bounded adversaries with one or more of the following capabilities.

### C1. Credential Possession

The attacker may possess a valid password, token, API key, or credential artifact.

### C2. Valid Session Access

The attacker may gain control of an already authenticated Session.

### C3. Partial Behavioral Mimicry

The attacker may imitate some observed behavior patterns.

### C4. Partial Evidence Control

The attacker may manipulate one or more Evidence sources.

Examples:

```text
location spoofing
network tunneling
device attribute manipulation
synthetic behavioral input
relay-mediated challenge response
```

### C5. Gradual Sub-threshold Drift

The attacker may repeatedly introduce small changes that individually remain below a simple threshold.

### C6. Context Manipulation

The attacker may attempt to make a malicious transition appear as a legitimate new Context.

### C7. Update-Timing Manipulation

The attacker may choose when to generate drift so that updates occur during low-observation or low-confidence periods.

### C8. Replay or Reuse

The attacker may replay previously valid Evidence or response patterns.

### C9. Partial History Influence

The attacker may influence the history used by the update process, but not necessarily the protected audit or rollback anchor.

### C10. Multi-stage Operation

The attacker may combine credential theft, Session hijacking, Evidence manipulation, and gradual criterion poisoning.

---

## 10. Trusted Assumptions

The initial Formal Security Model may rely on the following explicit assumptions.

These assumptions must be narrowed or tested in later phases.

### A1. At Least One Independent Trust Anchor

At least one policy, credential result, evidence source, or administrative anchor used for guarded recovery remains uncompromised.

### A2. Protected Rollback Point

At least one prior criterion state can be retained and restored without attacker modification.

### A3. Distinguishable Evidence Provenance

The system can distinguish at least some Evidence by source, time, or trust class.

### A4. Bounded History Integrity

The history required for the minimum simulation is ordered and sufficiently intact to evaluate update direction and rate.

### A5. Bounded Attacker Observation

The attacker does not know or perfectly reproduce every internal criterion component and independent Evidence relation.

### A6. Non-universal Evidence Compromise

Not all independent Evidence sources are simultaneously and perfectly controlled by the attacker.

### A7. Response Enforcement

When `FREEZE`, `REVIEW`, or `ROLLBACK` is selected, the corresponding implementation mechanism can enforce the response.

### A8. Criterion Separation

The effective criterion, update candidate, and rollback criterion are distinguishable system states.

### A9. Decision Separation

Auth Decision and Criterion Update Response are separately represented and enforceable.

### A10. Bounded Runtime

The implementation uses finite history, bounded loops, and explicit update checkpoints rather than unbounded recursive self-evaluation.

---

## 11. Threat Classes

## 11.1 T1 — Credential Theft

### Goal

Use a valid credential to obtain or continue unauthorized access.

### Capability

```text
valid credential artifact
possible knowledge of account context
possible access from a new device or network
```

### Observable Effects

Potential effects include:

```text
new device relation
new network relation
unusual operation order
unexpected privilege transition
behavioral drift
challenge-response inconsistency
```

### Expected GyroAuth Handling

Credential validity is Evidence, not Identity itself.

```text
valid credential
!=
stable authentication relation
```

GyroAuth may select:

```text
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

depending on the broader trajectory.

### Residual Risk

If the attacker reproduces the legitimate trajectory and controls required Evidence, GyroAuth may not distinguish the attacker.

---

## 11.2 T2 — Session Hijacking

### Goal

Continue operations through a valid Session after the effective operator changes.

### Capability

```text
valid Session token or channel control
possibly no original credential
```

### Observable Effects

```text
Session continuity without trajectory continuity
operation-order change
rate change
privilege-use change
network or device transition
post-login behavioral drift
```

### Expected GyroAuth Handling

```text
valid Session
!=
stable authentication relation
```

The model evaluates whether Authentication Relation Continuity remains readable.

### Residual Risk

A hijacker who perfectly preserves relevant relations may remain difficult to detect.

---

## 11.3 T3 — Relay Attack

### Goal

Use a legitimate endpoint or subject to relay authentication Evidence or challenge responses while the attacker controls the effective operation.

### Capability

```text
relay communication
possible credential-response forwarding
possible proximity or location illusion
```

### Observable Effects

```text
response timing inconsistency
network relation inconsistency
device-operation mismatch
motion or space inconsistency
post-authentication trajectory divergence
```

### Expected GyroAuth Handling

Location or proximity is one Evidence source only.

```text
location match
!=
authentication success
```

The model may increase detectability when the relay introduces cross-evidence or trajectory inconsistency.

### Residual Risk

A low-latency relay that preserves all relevant Evidence relations may not be detected.

---

## 11.4 T4 — Gradual Behavioral Mimicry

### Goal

Progressively imitate the legitimate user's behavior closely enough to avoid abrupt anomaly detection.

### Capability

```text
observation of behavior
repeated access opportunities
sub-threshold adaptation
```

### Observable Effects

```text
small repeated deviation
change in deviation direction
unusual persistence
recovery pattern mismatch
cross-context inconsistency
```

### Expected GyroAuth Handling

The model should evaluate Deviation Dynamics rather than only current magnitude.

```text
same deviation magnitude
!=
same trajectory meaning
```

### Residual Risk

Perfect or sufficiently complete mimicry may remain indistinguishable under available Evidence.

---

## 11.5 T5 — Criterion Poisoning

### Goal

Cause attacker-controlled behavior to be incorporated into the Authentication Criterion as a new normal.

### Capability

The attacker may:

```text
produce repeated sub-threshold deviations
influence update Evidence
manipulate Context labels
exploit automatic adaptation
avoid abrupt policy violations
```

### Attack Pattern

```text
small malicious deviation
→ repeated admissible-looking observations
→ candidate-region expansion or translation
→ discrimination decline
→ malicious behavior treated as normal
```

### Expected GyroAuth Handling

The update candidate must be separately evaluated.

```text
Observed Access Trajectory
→ Criterion Update Candidate
→ Criterion Integrity Evaluation
→ ACCEPT / DEFER / FREEZE / REVIEW / ROLLBACK
```

### Residual Risk

Criterion poisoning may succeed when:

```text
all relevant Evidence is compromised
history is unavailable
anchors are compromised
rollback points are unavailable
attacker drift is indistinguishable from legitimate adaptation
```

---

## 11.6 T6 — Evidence Source Compromise

### Goal

Manipulate an Evidence source so that malicious activity appears admissible.

### Capability

Control or spoof one or more sources.

### Observable Effects

```text
single-source confidence increase
cross-source contradiction
provenance discontinuity
sudden Evidence priority change
```

### Expected GyroAuth Handling

No single Evidence source should automatically authorize criterion adaptation.

The Guard should consider:

```text
source provenance
source independence
cross-evidence consistency
historical reliability
```

### Residual Risk

If all relevant Evidence sources are compromised consistently, the model does not claim reliable detection.

---

## 11.7 T7 — History Suppression or Reordering

### Goal

Remove the relational pattern that makes gradual drift or poisoning readable.

### Capability

```text
drop events
reorder events
truncate windows
suppress failed challenges
```

### Observable Effects

```text
gaps
unexpected window reset
broken provenance
rollback linkage failure
```

### Expected GyroAuth Handling

History gaps must not automatically become neutral.

Possible responses include:

```text
DEFER
FREEZE
REVIEW
```

### Residual Risk

Without trusted history or an external audit anchor, retrospective reconstruction may be impossible.

---

## 11.8 T8 — Rollback Point Corruption

### Goal

Prevent recovery by corrupting or replacing the last trusted criterion state.

### Capability

Access to rollback storage or checkpoint metadata.

### Expected GyroAuth Handling

Rollback points require protected provenance and integrity verification.

### Residual Risk

If both the current criterion and all rollback points are compromised, rollback-based recovery is not guaranteed.

---

## 11.9 T9 — Criterion Contraction Attack

### Goal

Narrow the criterion to reject legitimate behavior, force repeated challenges, or deny service.

### Capability

Influence update Evidence or policy weighting.

### Observable Effects

```text
increasing false rejection
shrinking admissible region
challenge frequency growth
legitimate recovery failure
```

### Expected GyroAuth Handling

Criterion Integrity must evaluate both over-expansion and over-contraction.

```text
adaptive
!=
permissive
```

and:

```text
strict
!=
correct
```

### Residual Risk

A denial-oriented attacker may still cause availability loss even when unauthorized acceptance is prevented.

---

## 11.10 T10 — Response Manipulation

### Goal

Alter or suppress the selected Criterion Update Response.

Examples:

```text
convert FREEZE to ACCEPT
suppress REVIEW
ignore ROLLBACK
```

### Expected GyroAuth Handling

Response selection and response enforcement should be auditable and separately represented.

### Residual Risk

If enforcement is compromised, model-level correctness does not imply operational security.

---

## 11.11 T11 — Context Laundering

### Goal

Present malicious drift as a legitimate Context change.

Example:

```text
attacker-controlled operation
→ labeled as travel, emergency, or role change
→ criterion adaptation requested
```

### Expected GyroAuth Handling

Context change should require supporting relational Evidence and should not alone authorize adaptation.

### Residual Risk

A fully compromised Context authority may defeat this distinction.

---

## 11.12 T12 — Multi-source Coordinated Compromise

### Goal

Coordinate several compromised Evidence sources to create a mutually consistent but false trajectory.

### Capability

Control multiple sources and their timing.

### Expected GyroAuth Handling

This threat tests the limit of cross-evidence consistency.

Consistency among compromised sources is not equivalent to truth.

### Residual Risk

The initial model does not claim security when all relevant independent sources and anchors are compromised.

---

## 12. Legitimate Change Classes

The Threat Model must distinguish attacks from legitimate adaptation.

These cases are not attackers, but they are necessary comparison classes.

## 12.1 N1 — New Device

```text
known identity relation
→ new device
→ deviation increase
→ stronger verification
→ controlled adaptation
```

Expected result:

```text
REAUTH_REQUIRED
+
DEFER or ACCEPT after validation
```

## 12.2 N2 — Travel or Network Change

A location or network transition may be legitimate when supported by time, device, challenge, and operation relations.

## 12.3 N3 — Role Change

A new privilege or operation pattern may be legitimate when linked to an authorized role transition.

## 12.4 N4 — Emergency Operation

An unusual operation sequence may be legitimate under an emergency Context but should require stronger Evidence or review.

## 12.5 N5 — Long-term Behavioral Change

Behavior may change gradually because of age, health, work, accessibility, or device changes.

The criterion should adapt without treating every long-term change as poisoning.

## 12.6 N6 — Temporary Degradation

Fatigue, injury, network degradation, or environmental constraints may temporarily change behavior without changing the Expected Identity relation.

## 12.7 N7 — Recovery after Re-authentication

A temporary deviation may be resolved by explicit verification and re-convergence.

```text
Re-auth
!=
AUTH_FAIL
```

---

## 13. Criterion Poisoning Subclasses

Because Criterion poisoning is the central threat, it is divided into specific subclasses.

### P1. Region Expansion

Increase the width of the admissible region until attacks fit inside it.

### P2. Region Translation

Move the criterion center toward attacker behavior.

### P3. Evidence Priority Poisoning

Increase the weight or priority of attacker-controlled Evidence.

### P4. Recovery Expectation Poisoning

Redefine prolonged deviation as acceptable recovery.

### P5. Challenge Requirement Weakening

Reduce the conditions that require explicit verification.

### P6. Context-rule Poisoning

Make suspicious Context changes automatically admissible.

### P7. History-window Poisoning

Alter the effective history window so that earlier trusted behavior is forgotten too quickly.

### P8. Rollback-link Poisoning

Change which checkpoint is considered trusted.

### P9. Slow Contraction

Narrow the criterion to cause legitimate-user denial or forced migration.

### P10. Response-policy Poisoning

Bias the update selector toward `ACCEPT` and away from `FREEZE`, `REVIEW`, or `ROLLBACK`.

---

## 14. Normal Update versus Poisoned Update

The minimum comparison is:

| Evaluation Axis | Legitimate Update | Poisoned Update |
|---|---|---|
| Context change | Explainable and supported | Unclear, fabricated, or contradictory |
| Evidence provenance | Multiple or trusted sources | Manipulated, replayed, or weakly sourced |
| Re-authentication | Successful where required | Avoided, relayed, or inconsistent |
| Update magnitude | Proportionate to Context | Disproportionate or cumulative |
| Update direction | Toward a validated new operating pattern | Toward attacker-controlled behavior |
| Update rate | Consistent with legitimate transition | Tuned to remain sub-threshold |
| Trajectory | Relationally readable | Locally plausible but globally suspicious |
| Discrimination | Preserved | Degraded |
| Rollback | Available and linked | Suppressed or corrupted |
| Expected response | ACCEPT after validation | DEFER / FREEZE / REVIEW / ROLLBACK |

This comparison is required for the later simulation.

---

## 15. Observable Security Signals

The model may use one or more of the following observable or derived signals.

### 15.1 Subject-side Signals

```text
Deviation magnitude
Deviation direction
Deviation rate
Deviation acceleration
Deviation spread
Deviation persistence
recovery tendency
cross-evidence inconsistency
operation-order inconsistency
privilege-transition inconsistency
```

### 15.2 Criterion-side Signals

```text
criterion drift distance
criterion region expansion
criterion region contraction
update rate
update direction
Evidence provenance quality
cross-evidence agreement
challenge confirmation
rollback availability
discrimination change
response frequency
```

### 15.3 Meta-signals

```text
history gap
source reliability change
Context-label instability
unexpected update frequency
repeated sub-threshold candidate updates
```

No single signal is assumed sufficient in all cases.

---

## 16. Response Expectations

The Threat Model uses two separate response families.

## 16.1 Auth Decision

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

## 16.2 Criterion Update Response

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

### ACCEPT

The update candidate may become the next effective criterion.

### DEFER

The current criterion remains effective while more Evidence is collected.

### FREEZE

Adaptive criterion updates are suspended to prevent suspected contamination.

### REVIEW

The update question is transferred to an external policy, administrator, or independent validation process.

### ROLLBACK

The effective criterion is restored to a prior trusted state.

These meanings will be fixed more precisely in Priority E.

---

## 17. Threat-to-Response Matrix

| Threat | Primary Observable Effect | Auth Decision Candidates | Criterion Update Response Candidates |
|---|---|---|---|
| Credential theft | Cross-context and behavioral deviation | RECONVERGING / REAUTH_REQUIRED / AUTH_FAIL | DEFER / FREEZE / REVIEW |
| Session hijacking | Session continuity without relation continuity | REAUTH_REQUIRED / AUTH_FAIL | FREEZE / REVIEW |
| Relay attack | Timing and cross-evidence inconsistency | RECONVERGING / REAUTH_REQUIRED | DEFER / REVIEW |
| Behavioral mimicry | Low-magnitude persistent directional drift | RECONVERGING / REAUTH_REQUIRED | DEFER / FREEZE |
| Criterion poisoning | Criterion drift and discrimination decline | Any, depending on subject state | DEFER / FREEZE / REVIEW / ROLLBACK |
| Evidence compromise | Source contradiction or provenance failure | RECONVERGING / REAUTH_REQUIRED | DEFER / FREEZE / REVIEW |
| History suppression | Unreadable update trajectory | REAUTH_REQUIRED candidate | DEFER / FREEZE / REVIEW |
| Rollback corruption | Recovery path unavailable | No direct mapping | REVIEW / external recovery |
| Criterion contraction | Rising false rejection and shrinking region | REAUTH_REQUIRED candidate | DEFER / FREEZE / ROLLBACK |
| Context laundering | Unsupported Context shift | REAUTH_REQUIRED | DEFER / REVIEW |

The matrix is provisional and does not replace the later state machine.

---

## 18. Attack Success Conditions

For this study, an attack is considered successful when one or more of the following occur.

### S1. Unauthorized Authentication Continuation

An illegitimate Access Subject remains accepted while the Authentication Relation is no longer admissible.

### S2. Poisoned Criterion Adoption

A malicious Criterion Update Candidate becomes the effective criterion.

### S3. Discrimination Loss

The criterion becomes unable to distinguish the attack trajectory from legitimate trajectories under the modeled Evidence.

### S4. Recovery Loss

No trusted rollback or review path remains available.

### S5. Persistent False Rejection

A malicious update causes legitimate activity to remain outside the admissible region.

### S6. Response Bypass

A selected `FREEZE`, `REVIEW`, or `ROLLBACK` is not enforced.

---

## 19. Detection Success Conditions

The minimum model counts detection or containment as successful when:

```text
a suspicious update is not automatically adopted
```

and at least one of the following occurs:

```text
DEFER is selected before adoption
FREEZE stops further adaptation
REVIEW transfers the decision
ROLLBACK restores a trusted criterion
REAUTH_REQUIRED obtains stronger Evidence
AUTH_FAIL prevents relation continuation
```

Detection does not require perfect attacker attribution.

The model may identify:

```text
criterion update is not currently trustworthy
```

without proving:

```text
this specific human is the attacker
```

---

## 20. Out-of-Scope Threats

The initial model does not claim protection against:

```text
complete compromise of every Evidence source
complete compromise of all trusted anchors
complete compromise of all rollback points
arbitrary modification of GyroAuth code at runtime
arbitrary modification of GyroOS execution results
hardware root compromise
cryptographic primitive failure
perfect attacker reproduction of every relevant trajectory relation
unbounded denial-of-service
malicious administrators with unrestricted authority
fully compromised external review process
```

These may be studied later, but they are not part of the initial proof of concept.

---

## 21. Security Claim Boundary

The Threat Model may support conditional claims such as:

```text
criterion updates are not automatically adopted
subject evaluation and criterion evaluation are separated
sub-threshold drift can be evaluated over a trajectory
criterion poisoning can trigger guarded responses
trusted rollback points can support recovery
normal adaptation and poisoned adaptation can be represented differently
```

It does not support unconditional claims such as:

```text
all criterion poisoning is prevented
all credential theft is detected
all relay attacks are detected
all Session hijacking is detected
false acceptance is zero
false rejection is zero
GyroAuth proves its own trustworthiness
human identity is perfectly determined
```

Every claim remains conditional on:

```text
attacker capabilities
trusted assumptions
Evidence availability
history integrity
response enforcement
implementation correctness
```

---

## 22. Minimum Simulation Threat Scope

The first simulation should not attempt every threat class.

It should compare at least:

### Scenario N — Legitimate Context Change

```text
known device
→ new device
→ Deviation increase
→ successful re-authentication
→ cross-evidence consistency
→ controlled update candidate
→ ACCEPT
→ re-convergence
```

### Scenario P — Gradual Criterion Poisoning

```text
small malicious deviation
→ repeated sub-threshold deviation
→ candidate-region expansion or translation
→ discrimination decline
→ DEFER
→ FREEZE
→ REVIEW or ROLLBACK
```

### Baseline U — Unconstrained Update

```text
A_(t+1) = U(A_t, X_t)
```

### Proposed G — Guarded Update

```text
A*_(t+1) = U(A_t, X_t)

A_(t+1) = Transition(
  A_t,
  A*_(t+1),
  Guard_t,
  CriterionUpdateResponse_t
)
```

The comparison should demonstrate:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 23. Required Outputs for Priority D

Priority D: Formal Security Model must convert this Threat Model into explicit definitions for:

```text
system state
subject state
criterion state
Evidence state
Context state
attacker action
trusted anchor
guard predicate
criterion deviation
criterion stability
Auth Decision function
Criterion Update Response function
state transition
attack success predicate
detection or containment predicate
```

At minimum, the Formal Security Model must represent:

```text
normal update
poisoned update
candidate generation
guarded acceptance
deferral
freeze
review
rollback
```

---

## 24. Priority C Outputs

Priority C fixes the following working position.

### Protected Relation

```text
Access Subject
↔
Expected Identity
```

### Protected Evaluation Basis

```text
Authentication Criterion
+
Criterion Update Process
+
Criterion Trajectory
```

### Central Threat

```text
Observed malicious behavior
is gradually incorporated
as a new admissible criterion
```

### Central Defense Structure

```text
Update Candidate
→ independent Criterion Integrity Evaluation
→ guarded Criterion Update Response
```

### Main Assumption Boundary

The model requires at least one protected anchor, Evidence source, audit linkage, or rollback point that is not simultaneously controlled by the attacker.

### Main Non-guarantee

The model does not claim reliable distinction when all relevant Evidence, anchors, history, and rollback paths are compromised or perfectly simulated.

---

## 25. Layer Consistency Check

### Gyro Logic

No Core change.

```text
Structure
↓
Slice
↓
Stability
```

Trajectory and Continuity remain derivative theoretical references.

### GyroOS

No runtime contract or canonical Operator Response change.

### GyroAuth

This Threat Model defines application-layer security objectives, attacker capabilities, trusted assumptions, and response expectations.

### Project Cycle

No theory definition is delegated to Project Cycle.

### Developer Toolkit

Future tools may validate threat-model coverage, scenario files, or response traces, but they do not define the security model.

---

## 26. Core Change Status

```text
Gyro Logic Core change: none
GyroOS contract change: none
GyroAuth threat-model scope: added
```

---

## 27. Next Priority

The next task is:

```text
Priority D: Formal Security Model
```

Priority D should formalize:

```text
subject state
criterion state
dual evaluation
guarded update
attack success
response semantics interface
```

without yet overclaiming a complete security proof.
