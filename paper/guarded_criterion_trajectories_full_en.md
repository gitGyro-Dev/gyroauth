# Guarded Criterion Trajectories for Adaptive Authentication: Separating Current Access Decisions from Future Criterion Updates

## Abstract

Adaptive authentication must respond to legitimate changes in devices, networks, locations, roles, and behavior. A criterion that never changes becomes brittle, but a criterion that incorporates observations without independent control creates a second attack surface: malicious behavior may gradually be absorbed as a new normal. This paper proposes a GyroAuth extension in which authentication-criterion change is represented as a guarded trajectory rather than as an automatic profile update. The model separates the current authentication decision from the decision to modify the criterion used for future authentication. A Criterion Update Candidate is generated from current observations, Context, History, and the effective criterion, but it becomes effective only after a Guard and a Criterion Update Response select `ACCEPT`, `DEFER`, `FREEZE`, `REVIEW`, or `ROLLBACK`. We formalize the distinction between Subject Evaluation and Criterion Integrity Evaluation, define a bounded criterion-update state machine, and implement a deterministic proof of concept comparing direct candidate adoption with guarded adoption. Under a legitimate new-device scenario, the guarded model deferred adaptation until challenge confirmation and then accepted a bounded update. Under gradual region-expansion poisoning, the direct-update baseline expanded until an attack reference became admissible, whereas the guarded model froze adaptation before admission. Under single-source Evidence compromise, the guarded model rejected automatic adoption despite apparently valid Evidence values. These results demonstrate the executable structure of the proposal under synthetic assumptions. They do not establish production-grade security, universal attack detection, or empirical false-accept and false-reject rates.

**Keywords:** adaptive authentication, continuous authentication, criterion poisoning, guarded adaptation, trajectory, criterion integrity, GyroAuth

---

## 1. Introduction

Authentication systems increasingly operate in environments where user state, device state, network conditions, location, behavior, and operational context change over time. A fixed profile or fixed threshold may fail to accommodate legitimate change. A user may replace a device, travel, change roles, alter an established workflow, or perform an emergency operation. Therefore, an adaptive authentication system requires some mechanism by which its evaluation criterion can change.

Adaptation, however, creates an additional security problem. When observed behavior is incorporated directly into the criterion, repeated malicious behavior can gradually move, broaden, weaken, or contaminate the basis used for future decisions. The system may continue to evaluate the current access relation correctly while simultaneously corrupting the rule by which later access will be judged.

This paper studies that distinction. The central proposition is:

```text
dynamic criterion
!=
unconstrained self-update
```

The problem is not only whether the current Access Subject remains admissibly related to the Expected Identity. The system must also determine whether the Authentication Criterion remains appropriate as a basis for that judgment.

We therefore separate two questions:

```text
Subject Question:
Is the current Access Subject still admissibly related
with the Expected Identity?
```

```text
Criterion Question:
Is the current Authentication Criterion still admissible
as a basis for evaluating that relation?
```

The resulting decision spaces are intentionally different:

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

This separation allows combinations such as:

```text
AUTH_STABLE + FREEZE
```

The current access relation may remain temporarily continuable while adaptation of the future criterion is suspended.

The contributions of this paper are as follows.

1. We define a dual continuous-evaluation model that separates Subject Evaluation from Criterion Integrity Evaluation.
2. We represent criterion change as a traceable Criterion Trajectory rather than as an unexamined sequence of profile updates.
3. We define a Guarded Criterion Update process with five responses: `ACCEPT`, `DEFER`, `FREEZE`, `REVIEW`, and `ROLLBACK`.
4. We define a bounded Criterion Update State Machine that preserves the separation between current authentication and future criterion modification.
5. We implement a deterministic proof of concept comparing direct candidate adoption with guarded adoption under legitimate adaptation, gradual poisoning, and single-source Evidence compromise.
6. We state explicit assumptions, supported claims, conditional claims, and non-guarantees.

---

## 2. Background and Positioning

### 2.1 GyroAuth foundation

GyroAuth defines authentication as:

```text
Authentication
=
Stability-based Selection over State Convergence
```

GyroAuth is positioned in the following layer relationship:

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Authentication Application
```

The present study does not redefine the Gyro Logic Core:

```text
Structure
↓
Slice
↓
Stability
```

It also does not redefine the GyroOS runtime or canonical Operator Response. The contribution is limited to the GyroAuth application layer.

### 2.2 Relation to previous GyroAuth work

The foundational GyroAuth paper defines the base authentication model. The Trajectory-Based Vulnerability Response study applies trajectory evaluation to post-login operations and security response. The present study targets a different object:

```text
Authentication Criterion
and
Criterion Update Process
```

The study asks whether the basis used for Stability-based Selection remains trustworthy enough to continue being used.

### 2.3 Related-work scope

The final publication must compare the proposed model with current work in:

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

This working manuscript does not yet finalize novelty against that literature. A formal related-work review and reference list are required before submission.

---

## 3. Terminology and Scope

### 3.1 Access Subject

An **Access Subject** is the currently evaluated source of access and operations within an authentication context. It may be a legitimate user, a credential thief, a session hijacker, a relay-mediated operator, a bot, a remote controller, or a mixed source.

```text
Access Subject
!=
Verified Identity
```

### 3.2 Expected Identity

An **Expected Identity** is the persistent reference relation against which the Access Subject is evaluated as the same authenticated identity across changing Sessions and Contexts. Credentials, devices, locations, and behaviors may be Evidence associated with that relation, but none is identical to the Expected Identity.

```text
Evidence
!=
Identity
```

### 3.3 Observed Evidence

**Observed Evidence** is information made available to GyroAuth through observation sources and Slices. Examples include credential results, device state, behavioral state, time, space, network, motion, operation order, privilege transitions, challenge results, response evidence, history, and criterion-update provenance.

### 3.4 Observed Access Trajectory

An **Observed Access Trajectory** is the readable relational configuration obtained by tracing admissible relations among Local Authentication Realizations under the current Orientation, Context, and Slice. It is not merely a chronological log or a sequence of feature vectors.

```text
History
!=
Trajectory
```

### 3.5 Authentication Relation

An **Authentication Relation** is the currently evaluated relation between an Access Subject and an Expected Identity within a Session and Context. GyroAuth selects whether that relation may continue.

### 3.6 Authentication Criterion

An **Authentication Criterion** is the Context-relative basis used by GyroAuth to interpret Evidence, Deviation, Stability, Trajectory, History, and response conditions.

```text
Authentication Criterion
!=
Fixed Identity Profile
```

### 3.7 Criterion Update Candidate

A **Criterion Update Candidate** is a proposed next criterion generated from the current criterion, new Evidence, Context, and History. It is not yet effective.

```text
Criterion Update Candidate
!=
Accepted Criterion
```

### 3.8 Criterion Trajectory

A **Criterion Trajectory** is the readable relational configuration through which criterion changes can be traced as admissible or inadmissible. It includes update causes, supporting Evidence, provenance, magnitude, direction, rate, discrimination effects, responses, and rollback linkage.

### 3.9 Criterion Integrity

**Criterion Integrity** is the condition in which the Authentication Criterion and its update process remain admissible and traceable as a basis for evaluating the authentication relation.

Criterion Integrity does not imply self-certification. It depends on protected anchors, Evidence provenance, history, rollback points, and response rules.

---

## 4. Threat Model

### 4.1 Security objectives

The model protects two related properties:

1. the ability to evaluate whether the current Authentication Relation remains continuable; and
2. the ability to prevent an attacker from moving, broadening, weakening, or contaminating the Authentication Criterion until malicious behavior is treated as normal.

### 4.2 Protected objects

The protected objects are:

```text
Authentication Relation
Authentication Criterion
Criterion Update Process
Criterion Trajectory
Trusted History
Rollback Points
Decision separation
```

### 4.3 Threat classes

The Threat Model includes:

```text
Credential theft
Session hijacking
Relay attack
Gradual behavioral mimicry
Criterion poisoning
Evidence-source compromise
Multi-source coordinated compromise
```

The main threat studied in the PoC is Criterion poisoning.

### 4.4 Criterion poisoning

Criterion poisoning is an attack in which an adversary influences Evidence or the observed trajectory so that malicious states or operations are gradually incorporated into the effective criterion.

Relevant subtypes include:

```text
Region expansion
Criterion translation
Evidence-priority poisoning
Recovery-expectation poisoning
Challenge-requirement weakening
Context-rule poisoning
History-window poisoning
Rollback-link poisoning
Slow contraction
Response-policy poisoning
```

### 4.5 Trusted assumptions

The minimum model assumes that at least one of the following remains outside simultaneous attacker control:

```text
an independent Evidence source
a protected policy anchor
an intact audit linkage
a verified rollback point
```

The model does not claim reliable discrimination or recovery if all Evidence sources, anchors, history, and rollback points are compromised.

---

## 5. Formal Security Model

### 5.1 Discrete evaluation stages

Evaluation proceeds through bounded stages:

```text
t = 0, 1, 2, ...
```

Each stage may correspond to one `/auth/step` call, one observation interval, one relevant security event, one challenge result, or one criterion-update evaluation.

### 5.2 Decision spaces

The Auth Decision set is:

```text
D_auth = {
  AUTH_STABLE,
  RECONVERGING,
  REAUTH_REQUIRED,
  AUTH_FAIL
}
```

The Criterion Update Response set is:

```text
D_crit = {
  ACCEPT,
  DEFER,
  FREEZE,
  REVIEW,
  ROLLBACK
}
```

These spaces are not interchangeable.

### 5.3 Candidate generation

Let the effective criterion at stage `t` be:

```text
A_t
```

A candidate is generated by:

```text
A*_(t+1)
=
U(A_t, T_t^obs, C_(t+1), E_t, H_t)
```

Candidate generation is not candidate adoption.

```text
A*_(t+1)
!=
A_(t+1)
```

### 5.4 Guard

The candidate is evaluated through:

```text
G_t
=
Guard(
  A_t,
  A*_(t+1),
  T_t^obs,
  C_(t+1),
  E_t,
  H_t,
  P_t
)
```

The minimum Guard vector contains:

```text
provenance
cross-evidence consistency
challenge confirmation
update magnitude
update rate
update direction
discrimination preservation
rollback linkage
evidence-source integrity
```

### 5.5 Non-compensation rule

Critical Guard failures cannot be averaged away.

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

This prevents a high average summary score from masking failure of a critical property such as source integrity or discrimination preservation.

### 5.6 Criterion Update Response

The response is selected by:

```text
D_crit_t
=
Pi_crit(G_t, Q_t, H_t)
```

The effective criterion transition is:

```text
A_(t+1) = A*_(t+1)
when D_crit_t = ACCEPT
```

```text
A_(t+1) = A_t
when D_crit_t ∈ {DEFER, FREEZE, REVIEW}
```

```text
A_(t+1) = A_tau
when D_crit_t = ROLLBACK and tau < t
```

### 5.7 Subject Evaluation

Subject Evaluation remains separate from criterion adaptation. It uses the Observed Access Trajectory, Deviation, Stability, Context, History, and response evidence to select an Auth Decision.

The criterion response must not be inferred directly from the Auth Decision.

---

## 6. Criterion Update State Machine

### 6.1 Criterion States

The model defines:

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

### 6.2 Response semantics

#### ACCEPT

The candidate becomes the next effective criterion.

#### DEFER

The current criterion remains effective while additional Evidence, challenge results, or observations are collected.

#### FREEZE

Adaptive adoption is suspended because the update path itself is considered unsafe. Subject Evaluation may continue independently.

#### REVIEW

Automated adoption is suspended and the decision is transferred to an external policy, administrator, stronger verification path, or independent validator.

#### ROLLBACK

A verified prior criterion is restored without deleting the audit trail.

### 6.3 Distinctions

```text
DEFER
!=
FREEZE
```

`DEFER` concerns insufficient support for a candidate. `FREEZE` concerns danger in the adaptive path.

```text
REVIEW
!=
DEFER
```

`REVIEW` changes the decision path or decision authority.

---

## 7. PoC Design

### 7.1 Compared models

The PoC compares two models using the same candidate generator.

#### Model U: Unconstrained Update

```text
Observation
→ Candidate
→ Direct Adoption
```

#### Model G: Guarded Update

```text
Observation
→ Candidate
→ Guard
→ Criterion Update Response
→ Effective Criterion Transition
```

Model U is an intentionally unsafe baseline. It is not claimed to represent every adaptive-authentication system.

### 7.2 Criterion representation

The effective criterion is represented as:

```text
A_t = (
  mu_t,
  width_t,
  provenance_requirement_t,
  challenge_requirement_t,
  rollback_integrity_t
)
```

where `mu_t` is the criterion center and `width_t` is the admissible region width. This scalar representation is a minimum executable abstraction, not a production identity model.

### 7.3 Candidate generator

Both models use:

```text
mu*_(t+1)
=
mu_t + eta_mu (y_t - mu_t)
```

and:

```text
width*_(t+1)
=
width_t
+ eta_width max(0, |y_t - mu_t| - width_t)
```

The models differ only in adoption.

### 7.4 Scenarios

The minimum scenarios are:

```text
N1: Legitimate New Device Transition
P1: Gradual Region Expansion Poisoning
C1: Single Evidence Source Compromise
```

### 7.5 Implementation

The implementation uses the Python standard library and deterministic synthetic inputs.

Artifacts:

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

The implementation records candidate values, Guard results, Auth Decisions, Criterion Update Responses, criterion states, effective criteria, and assertions.

---

## 8. Results

### 8.1 Scenario N1: Legitimate new-device transition

The guarded model produced:

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

Final values were:

```text
mu    = 0.234
width = 0.120
```

The first candidate was not adopted because challenge confirmation was pending. After successful re-authentication and cross-evidence consistency, the model accepted a bounded update. The admissible width did not expand.

This result demonstrates that guarded adaptation is not equivalent to non-adaptation.

```text
Guarded
!=
Non-adaptive
```

### 8.2 Scenario P1: Gradual region-expansion poisoning

The attack reference was:

```text
y_attack = 0.62
```

#### Model U

Final values:

```text
mu    = 0.3969728
width = 0.277212
```

Result:

```text
attack reference admissible = true
```

The direct-update baseline adopted every candidate until the criterion moved and broadened enough to include the attack reference.

#### Model G

Final values:

```text
mu    = 0.200
width = 0.120
freeze stage = 2
```

Result:

```text
attack reference admissible = false
```

Response path:

```text
DEFER
→ FREEZE
→ FREEZE
→ FREEZE
→ FREEZE
```

The effective criterion remained at the trusted initial state.

At stage 2, the model produced:

```text
AUTH_STABLE + FREEZE
```

This demonstrates the operational difference between:

```text
current subject acceptance
```

and:

```text
permission to redefine future acceptance
```

### 8.3 Scenario C1: Single Evidence-source compromise

The guarded model produced:

```text
FREEZE
→ FREEZE
```

Final values:

```text
mu    = 0.200
width = 0.120
```

No candidate was accepted. Apparently strong Evidence values did not compensate for low source integrity and weak cross-evidence consistency.

```text
single Evidence match
!=
criterion update acceptance
```

### 8.4 Assertions

All seven executable assertions passed:

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

## 9. Discussion

### 9.1 Main finding

The PoC demonstrates that the current authentication decision and the permission to alter future authentication criteria can be represented as separate executable decisions.

The distinction matters because a subject may remain temporarily acceptable under the current criterion while the observed update path is unsafe. `AUTH_STABLE + FREEZE` captures this case directly.

### 9.2 Guarded adaptation is still adaptive

The N1 result shows that a guarded model can accept legitimate change after challenge confirmation, provenance checks, and cross-evidence consistency. The proposal does not require criteria to remain static.

### 9.3 Repeated observation is insufficient

The P1 result shows that repetition alone does not establish legitimacy.

```text
repeated observation
!=
new normal automatically
```

Small local deviations can accumulate into large criterion drift. Therefore, the Guard considers cumulative direction, expansion, discrimination loss, and Evidence quality rather than only one-step magnitude.

### 9.4 Criterion Integrity is not self-proof

The model does not prove its own trustworthiness without assumptions. Criterion Integrity depends on protected anchors, independent Evidence, retained history, and valid rollback links.

### 9.5 Relation to GyroAuth

The proposal extends GyroAuth by including the criterion and its update process in the application-layer evaluation scope. It does not change the Gyro Logic Core or the GyroOS execution contract.

---

## 10. Security Claims

### 10.1 Structurally demonstrated claims

Under the implemented deterministic assumptions, the PoC supports the following claims:

1. A Criterion Update Candidate can be separated from the accepted criterion.
2. Auth Decision and Criterion Update Response can remain separate decision streams.
3. Legitimate bounded adaptation can be accepted after sufficient support.
4. Direct candidate adoption can produce cumulative criterion expansion.
5. A guarded response can freeze adaptation before the attack reference becomes admissible in the implemented P1 scenario.
6. A compromised Evidence source can block criterion adoption in the implemented C1 scenario.
7. `AUTH_STABLE + FREEZE` is executable.

### 10.2 Conditional claims

The following claims require additional assumptions and validation:

```text
criterion-poisoning containment beyond P1
rollback-supported recovery
credential-theft resistance
session-hijacking detection
relay-attack detection
multi-source compromise resistance
```

### 10.3 Unsupported claims

This study does not establish:

```text
complete prevention of criterion poisoning
universal attacker detection
zero false acceptance
zero false rejection
perfect identity proof
security under total Evidence and anchor compromise
production performance
privacy guarantees
formal proof of correctness
statistical generalization
```

---

## 11. Limitations

### 11.1 Synthetic deterministic inputs

The scenarios are manually specified and deterministic. They do not represent empirical population distributions.

### 11.2 One-dimensional criterion

The criterion center and width are scalar. A production system would require multidimensional state and relational representations.

### 11.3 Reduced trajectory proxy

The PoC uses reduced numerical proxies for Trajectory Continuity and Stability. These do not replace the broader relational definitions.

### 11.4 Hand-configured thresholds

Guard thresholds and coefficients are explicit but not optimized from real data.

### 11.5 No measured false-accept or false-reject rates

The study demonstrates state-transition behavior, not operational biometric or authentication accuracy.

### 11.6 Limited attacks

The executable scenarios cover one legitimate adaptation, one gradual expansion attack, and one single-source compromise. Translation poisoning, evidence-priority poisoning, challenge weakening, history-window poisoning, and rollback-link poisoning remain future work.

### 11.7 No production integration

The PoC does not include cryptographic protocol integration, hardware attestation, production GyroOS execution, privacy-preserving storage, distributed Evidence collection, or resource benchmarking.

### 11.8 Related-work review incomplete

Novelty claims must remain provisional until the proposed model is compared against current primary literature and standards.

---

## 12. Future Work

The next research steps are:

1. implement verified rollback execution;
2. add criterion translation poisoning;
3. add Evidence-priority poisoning and challenge weakening;
4. perform threshold and coefficient sensitivity analysis;
5. add legitimate-change false-positive comparisons;
6. extend the criterion to multidimensional states and relations;
7. measure computational and storage costs;
8. evaluate with real or realistically generated authentication telemetry;
9. complete related-work and standards comparison;
10. evaluate privacy and governance requirements for retained criterion history.

---

## 13. Conclusion

Adaptive authentication requires criteria that can respond to legitimate change. However, direct observation-to-criterion incorporation creates a poisoning surface in which repeated malicious behavior may gradually redefine normality.

This paper proposed a GyroAuth extension that treats criterion change as a guarded trajectory. The model separates current authentication decisions from decisions about whether future criteria may change. Candidate updates are generated but do not become effective until a Guard and a Criterion Update Response select acceptance, deferral, freezing, review, or rollback.

A deterministic PoC showed that supported new-device adaptation could be accepted, gradual criterion expansion could be frozen before attack-reference admission, and a compromised Evidence source could block adoption. The result `AUTH_STABLE + FREEZE` demonstrated that current access continuation and future criterion modification can be evaluated independently.

The study is a structural and executable demonstration, not a production security guarantee. Its central position is:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## References

The final reference list will be added after a current primary-source review covering adaptive authentication, continuous authentication, behavioral biometrics, concept drift, online learning security, poisoning attacks, Zero Trust, UEBA, and anomaly detection.

---

## AI-Assisted Tools Disclosure

AI-assisted tools were used for structural organization, drafting support, expression refinement, and consistency checking during preparation of this manuscript. The author reviewed and edited the content, claims, references, and final manuscript and assumes full responsibility for them.