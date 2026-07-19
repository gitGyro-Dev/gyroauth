# GyroAuth Security Claims and Limitations

## 1. Purpose

This document completes **Priority I: Security Claims and Limitations** for the GyroAuth formalization and paper-preparation work.

It builds on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
docs/18_formal_security_model.md
docs/19_criterion_update_state_machine.md
docs/20_normal_and_poisoned_update_scenarios.md
docs/21_minimal_simulation_design.md
docs/22_poc_implementation_and_results.md
```

Its purpose is to define:

```text
what the current model supports
what the PoC demonstrates
which claims are conditional
which claims remain unsupported
which assumptions each claim requires
which limitations must accompany publication
```

This document is not a production security certification, a universal attack-resistance claim, or a completed formal proof.

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

The claims in this document apply only to the GyroAuth application-layer model and PoC described in the preceding documents.

```text
Core change: none
GyroOS contract change: none
GyroAuth claim boundary: clarified
```

---

## 3. Claim Policy

GyroAuth claims must follow four rules.

### 3.1 No unconditional security language

The following expressions must not be used without proof and evidence:

```text
completely prevents
fully resistant
unattackable
always detects
zero false acceptance
zero false rejection
guaranteed identity proof
```

### 3.2 Claims must be linked to assumptions

Every security claim must identify:

```text
Threat Model
Trusted Assumptions
Observable Evidence
Model or PoC Evidence
Residual Risk
```

### 3.3 Structural demonstration is not empirical validation

The current PoC demonstrates that the proposed transition structure is executable and behaviorally distinguishable under synthetic deterministic inputs.

It does not establish real-world detection performance.

```text
Executable structure
!=
Production security guarantee
```

### 3.4 Detection, containment, and prevention are distinct

A model may:

```text
detect suspicious criterion drift
contain further adaptation
preserve a trusted criterion
support rollback
```

without proving that the underlying attack was prevented from beginning.

```text
Detection
!=
Containment
!=
Prevention
!=
Recovery
```

---

## 4. Evidence Levels

Claims are classified into four levels.

### Level S — Structurally demonstrated

The formal model and executable PoC directly demonstrate the stated property under declared assumptions.

### Level C — Conditionally supportable

The model supports the property only when specified assumptions, Evidence quality, and attack observability conditions hold.

### Level H — Hypothesis requiring further validation

The model provides a plausible mechanism, but the present PoC does not provide sufficient evidence for a security claim.

### Level N — Not supported

The current model must not claim the property.

---

## 5. Core Security Claims

## 5.1 Candidate Separation

### Claim

> A Criterion Update Candidate is not automatically adopted as the next effective Authentication Criterion in the guarded model.

### Status

```text
Level S — Structurally demonstrated
```

### Basis

The model separates:

```text
Candidate generation
from
Candidate adoption
```

The next criterion is selected through:

```text
Guard
→ Criterion Update Response
→ Effective Criterion Transition
```

The PoC demonstrates that candidates may be generated while the effective criterion remains unchanged under `DEFER` or `FREEZE`.

### Assumptions

```text
Guard execution is not bypassed
Criterion Update Response is enforced
Runtime state is not directly overwritten
```

### Limitation

This claim does not hold if an attacker compromises the implementation and directly modifies the effective criterion state.

---

## 5.2 Decision Separation

### Claim

> GyroAuth can evaluate the current Authentication Relation separately from the acceptability of criterion adaptation.

### Status

```text
Level S — Structurally demonstrated
```

### Basis

The model maintains two decision spaces:

```text
Auth Decision
!=
Criterion Update Response
```

The PoC executes:

```text
AUTH_STABLE + FREEZE
```

This shows that current access may remain temporarily continuable while criterion adaptation is stopped.

### Assumptions

```text
The two decision streams remain independently represented
Criterion responses are not inferred directly from Auth Decisions
```

### Limitation

The PoC demonstrates one executable separation pattern. It does not prove that every production integration will preserve the separation correctly.

---

## 5.3 Guarded Adaptation

### Claim

> A dynamic authentication criterion can accept bounded, Evidence-supported change without treating every observation as a new normal.

### Status

```text
Level S — Structurally demonstrated
Level C — Security effectiveness remains conditional
```

### Basis

Scenario `N1` demonstrates:

```text
REAUTH_REQUIRED
→ AUTH_STABLE
```

and:

```text
DEFER
→ ACCEPT
```

The criterion center changed after successful challenge confirmation and cross-evidence consistency, while the admissible width did not broaden.

### Assumptions

```text
Challenge result is trustworthy
Evidence provenance is meaningful
Cross-evidence consistency is observable
Update magnitude remains bounded
```

### Limitation

The present model uses synthetic scalar inputs and does not establish that the selected Guard thresholds are suitable for real users or real environments.

---

## 5.4 Containment of Gradual Region Expansion in the PoC

### Claim

> Under the implemented P1 scenario and declared Guard rules, the guarded model stops criterion adaptation before the attack reference becomes admissible.

### Status

```text
Level S — Demonstrated for the implemented scenario
```

### Basis

For `P1`:

```text
Model U:
attack reference admissible = true
```

```text
Model G:
freeze stage = 2
attack reference admissible = false
```

The effective guarded criterion remained at the trusted initial state.

### Assumptions

```text
The attack produces observable cumulative drift
The configured Guards cover the manipulated dimensions
The attacker cannot bypass FREEZE
The trusted initial criterion is valid
```

### Limitation

This result applies only to the implemented deterministic region-expansion scenario. It does not establish detection of every gradual poisoning strategy.

---

## 5.5 Critical Guard Non-compensation

### Claim

> A critical Guard failure cannot be overridden by a high average Criterion Integrity summary in the current model.

### Status

```text
Level S — Structurally demonstrated
```

### Basis

The model retains a Guard vector and applies:

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

The scalar Criterion Integrity value is reporting-only.

### Assumptions

```text
Critical Guards are correctly designated
The response policy enforces non-compensation
```

### Limitation

This does not prove that the chosen critical Guard set is complete.

---

## 5.6 Single-source Evidence Does Not Authorize Adaptation Automatically

### Claim

> One apparently valid Evidence source is insufficient to authorize criterion adaptation when source integrity or cross-evidence consistency fails.

### Status

```text
Level S — Demonstrated for scenario C1
```

### Basis

Scenario `C1` produces:

```text
FREEZE
→ FREEZE
```

No candidate was accepted despite apparently favorable individual Evidence values.

### Assumptions

```text
Source integrity can be evaluated
At least one independent comparison source remains trustworthy
Cross-evidence inconsistency is observable
```

### Limitation

If all relevant Evidence sources are compromised consistently, this claim no longer applies.

---

## 5.7 Traceable Criterion Change

### Claim

> The model can retain the cause, Evidence provenance, update delta, selected response, and rollback linkage associated with criterion change.

### Status

```text
Level S — Structurally supported
```

### Basis

The formal model and state machine represent Criterion Trajectory events containing:

```text
previous criterion
candidate criterion
Guard vector
Criterion Update Response
next effective criterion
Evidence references
Context
rollback linkage
```

### Assumptions

```text
Audit history is retained
History linkage is not silently removed
```

### Limitation

The current PoC is not a tamper-evident audit system and does not cryptographically protect history.

---

## 5.8 Rollback-supported Recovery

### Claim

> The model supports restoration of a prior verified criterion when contamination is detected and a valid Rollback Point exists.

### Status

```text
Level C — Formally represented, not fully exercised by the minimum PoC
```

### Basis

The model defines:

```text
ROLLBACK
→ verified prior criterion A_tau
```

and requires retention of the audit trail.

### Required conditions

```text
A verified Rollback Point exists
Rollback linkage remains intact
The restored criterion was not already contaminated
The runtime can enforce restoration
```

### Limitation

The current minimum scenario set primarily demonstrates `DEFER` and `FREEZE`. A dedicated rollback execution scenario remains necessary before claiming empirical recovery behavior.

---

## 6. Conditional Security Claims

## 6.1 Improved Resistance to Credential Theft

### Claim boundary

GyroAuth may improve resistance to credential theft when possession of the credential does not reproduce the expected Authentication Relation Continuity and Criterion Integrity conditions.

### Status

```text
Level C
```

### Required conditions

```text
Post-theft trajectory differs observably
At least one relevant Evidence source remains trustworthy
The attacker cannot reproduce all expected relations
The criterion has not already been poisoned
```

### Not guaranteed

GyroAuth does not guarantee detection when the attacker reproduces all relevant Evidence and trajectory relations within the observed model.

---

## 6.2 Session Hijacking Detection

### Claim boundary

GyroAuth may detect or escalate a hijacked Session when the change in operational source creates observable trajectory, Context, response, or cross-evidence inconsistency.

### Status

```text
Level C
```

### Required conditions

```text
The hijack changes observable relations
The system continues evaluating after login
The affected Evidence is not fully compromised
```

### Not guaranteed

A valid Session identifier alone does not prove Authentication Relation Continuity, but GyroAuth does not guarantee detection of a hijacker who perfectly reproduces the legitimate subject's observable trajectory.

---

## 6.3 Relay Attack Detection

### Claim boundary

GyroAuth may increase detectability of some relay attacks when relay-mediated operation creates inconsistencies among time, space, device, network, motion, behavior, response, or operation order.

### Status

```text
Level H to Level C depending on implemented Evidence
```

### Required validation

```text
Concrete relay scenario
Observable cross-evidence relations
Attack and legitimate baselines
Executed detection results
```

### Not guaranteed

The current PoC does not implement a relay protocol or demonstrate universal relay-attack detection.

---

## 6.4 Post-login Anomaly Detection

### Claim boundary

GyroAuth can represent post-login deviation and trajectory changes that occur after a formally valid login event.

### Status

```text
Level C
```

### Basis

The model evaluates a continuing Authentication Relation rather than treating successful login as a permanent conclusion.

### Limitation

The current criterion-update PoC does not establish detection rates for real post-login attacks.

---

## 6.5 Recovery Support

### Claim boundary

GyroAuth supports staged responses such as:

```text
RECONVERGING
REAUTH_REQUIRED
FREEZE
REVIEW
ROLLBACK
```

rather than collapsing every deviation into immediate failure.

### Status

```text
Level S for representational support
Level C for operational security benefit
```

### Limitation

Recovery success depends on trustworthy new Evidence, correct response integration, and uncompromised rollback or policy anchors.

---

## 7. Claims Not Supported by the Current Work

The current work must not claim the following.

### 7.1 Perfect identity proof

```text
GyroAuth proves the complete real-world identity of a human
```

Not supported.

GyroAuth evaluates whether the current Access Subject remains admissibly related to an Expected Identity under observed conditions.

### 7.2 Universal attack detection

```text
GyroAuth detects every credential theft
GyroAuth detects every relay attack
GyroAuth detects every session hijack
GyroAuth detects every poisoning attempt
```

Not supported.

### 7.3 Zero-error authentication

```text
False Accept = 0
False Reject = 0
```

Not supported.

### 7.4 Security under total Evidence compromise

If all Evidence sources, protected anchors, audit history, and rollback points are compromised consistently, the model does not claim reliable distinction or recovery.

### 7.5 Self-certification

GyroAuth does not prove its own trustworthiness from itself alone.

```text
Criterion-aware evaluation
!=
complete self-verification
```

### 7.6 Production performance

The current work does not establish:

```text
CPU cost
memory cost
storage cost
energy cost
latency
throughput
scalability
```

### 7.7 Privacy guarantees

The current work does not define or prove:

```text
data minimization
privacy preservation
unlinkability
anonymity
retention compliance
```

### 7.8 Statistical generalization

The synthetic deterministic PoC does not establish population-level generalization, robustness across users, or optimal coefficients.

---

## 8. Assumption Matrix

| Assumption | Why it is needed | Failure consequence |
|---|---|---|
| At least one relevant Evidence source remains trustworthy | Enables cross-evidence validation | Coordinated compromise may appear consistent |
| Guard execution is enforced | Prevents direct candidate adoption | Model collapses into unconstrained update |
| Critical Guard failures are non-compensable | Prevents average-score masking | Unsafe update may be accepted |
| Audit and provenance linkage are retained | Supports traceability and review | Criterion changes become unexplainable |
| Rollback Point is verified | Supports safe restoration | Rollback may restore contaminated state |
| Protected anchors are not all compromised | Provides an external trust basis | Criterion integrity may become undecidable |
| Context labels are meaningful | Distinguishes legitimate change from arbitrary drift | Normal and malicious transitions may be conflated |
| Response enforcement is correct | Makes FREEZE/REVIEW/ROLLBACK operational | Selected protection may not take effect |

---

## 9. Limitation Categories

## 9.1 Model Abstraction

The criterion is represented by a scalar center and width plus a small number of integrity-related fields.

Production authentication is multidimensional and relational.

```text
Minimum scalar abstraction
!=
complete authentication state
```

## 9.2 Reduced Trajectory Representation

The PoC uses deterministic proxies for Trajectory Continuity and Stability.

It does not implement the full relational Trajectory concept.

## 9.3 Synthetic Scenarios

The scenarios are authored to expose specific structural differences.

They are not drawn from real attack datasets or user populations.

## 9.4 Hand-selected Parameters

Thresholds and coefficients are declared but not empirically optimized.

The results demonstrate model behavior under those parameters, not universal superiority.

## 9.5 Limited Attack Diversity

The executable PoC covers:

```text
legitimate new-device adaptation
gradual region-expansion poisoning
single Evidence-source compromise
```

It does not yet execute:

```text
criterion translation poisoning
challenge-policy weakening
history-window poisoning
rollback-link poisoning
coordinated multi-source compromise
perfect behavioral mimicry
```

## 9.6 No Formal Theorem Proof

The documents define Invariants and transition conditions, but no theorem prover or complete mathematical proof has been provided.

## 9.7 No Production Runtime Integration

The PoC is a standalone deterministic simulation.

It does not exercise a complete GyroOS runtime, production identity provider, real device telemetry, or distributed policy system.

---

## 10. Security Claim Matrix

| Claim | Current status | Current evidence | Required next evidence | Main limitation |
|---|---|---|---|---|
| Candidate updates are not automatically adopted | Supported | Formal transition + executable PoC | Production integration test | Runtime bypass not covered |
| Auth Decision and Criterion Update Response are separate | Supported | `AUTH_STABLE + FREEZE` | API/state contract tests | Integration may collapse streams |
| Legitimate bounded adaptation is possible | Supported in N1 | `DEFER → ACCEPT` | Realistic multi-dimensional scenarios | Synthetic scalar model |
| Gradual region expansion can be contained | Supported for P1 | Model G freezes before attack reference admission | Parameter sensitivity and attack variants | Scenario-specific result |
| One compromised source need not authorize adaptation | Supported for C1 | Critical source/cross-evidence Guards | Multi-source compromise tests | Requires independent Evidence |
| Criterion poisoning can always be prevented | Not supported | None | Broad threat evaluation and proofs | Unrestricted attacker impossible to cover |
| Criterion poisoning can be detected under observable drift | Conditional | P1 result | Additional poisoning classes | Perfectly hidden drift may evade detection |
| Rollback can restore a trusted criterion | Conditional | Formal model only | Executed rollback scenario | Trusted point may be absent or compromised |
| Credential theft resistance improves | Conditional | Structural reasoning | Credential-theft PoC or dataset | Full trajectory reproduction may evade |
| Session hijacking can be detected | Conditional | Structural reasoning | Hijacking scenarios | Requires observable transition difference |
| Relay attacks can be detected | Hypothesis / conditional | No dedicated execution | Relay attack model and results | Current PoC does not implement relay |
| False Accept and False Reject are reduced | Not established | No population metrics | Dataset evaluation | No empirical rates |
| Production efficiency is acceptable | Not established | No benchmark | CPU/memory/storage/energy tests | Deferred implementation concern |

---

## 11. Publication-safe Claim Wording

The following formulations are acceptable for the next paper.

### Recommended

> The proposed model separates criterion-update proposals from criterion adoption and subjects the update trajectory to an independent Guard and response process.

> In the minimum deterministic PoC, the guarded model accepts a supported legitimate context transition while freezing a gradual region-expansion trajectory before the attack reference becomes admissible.

> The results demonstrate an executable distinction between current subject acceptance and permission to redefine future acceptance.

> The model provides a framework for detecting and containing some forms of criterion poisoning under explicit trust and observability assumptions.

### Avoid

> GyroAuth prevents criterion poisoning.

> GyroAuth detects attackers continuously.

> GyroAuth is secure against credential theft and relay attacks.

> The model proves identity.

> The PoC validates production security.

---

## 12. Minimum Additional Validation Before Stronger Claims

Before stronger paper claims are made, the following are recommended.

### 12.1 Rollback execution

Add a scenario that reaches:

```text
FREEZE
→ REVIEW or COMPROMISED
→ ROLLBACK
→ ROLLED_BACK
→ STABLE
```

### 12.2 Additional poisoning classes

Execute at least:

```text
P2 Criterion Translation Poisoning
P3 Evidence Priority Poisoning
P4 Challenge Requirement Weakening
```

### 12.3 Sensitivity analysis

Vary:

```text
Guard thresholds
candidate learning rates
cumulative drift limits
Evidence quality
attack speed
```

### 12.4 False-positive comparison

Compare legitimate long-term change with gradual poisoning.

### 12.5 Multi-dimensional criterion

Replace the scalar center/width abstraction with at least a low-dimensional vector or relation model.

### 12.6 Resource measurement

Measure:

```text
CPU
memory
history size
stage latency
```

only after the formal model and paper-level PoC are stable.

---

## 13. Priority I Outputs

Priority I fixes the following position.

### Supported now

```text
candidate/adoption separation
decision-stream separation
guarded bounded adaptation
scenario-specific containment of P1
single-source compromise blocking in C1
traceable response structure
```

### Conditional

```text
criterion-poisoning detectability
rollback-supported recovery
credential-theft resistance improvement
session-hijacking detection
post-login anomaly detection
relay-attack detectability
```

### Not supported

```text
universal attack prevention
perfect identity proof
zero false acceptance
zero false rejection
security under total compromise
production performance guarantees
privacy guarantees
statistical generalization
```

The central publication-safe conclusion is:

> GyroAuth does not treat adaptive criterion change as automatic profile update. It represents criterion change as a guarded trajectory and separates current authentication decisions from decisions about whether future authentication criteria may change.

The current PoC supports this structural claim under synthetic deterministic assumptions.

---

## 14. Preparation for Priority J

Priority J should prepare the paper outline and manuscript around the following evidence chain:

```text
Problem:
Adaptive criteria are necessary but can become an attack surface.

Model:
Criterion Update Candidate
→ Guard
→ Criterion Update Response
→ Effective Criterion Transition

Separation:
Auth Decision
!=
Criterion Update Response

PoC result:
Legitimate adaptation accepted
Poisoning trajectory frozen
Compromised source rejected

Claim boundary:
Structural and scenario-specific support
not universal production security
```

The paper must preserve the exact distinction between:

```text
what was formally defined
what was executed
what was observed
what remains conditional
what is explicitly not guaranteed
```

---

## 15. Layer Consistency

```text
Gyro Logic Core change: none
GyroOS contract change: none
GyroAuth security claim boundary: defined
```

This document does not change any other repository or layer.
