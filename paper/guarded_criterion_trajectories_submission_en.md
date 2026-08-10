# Guarded Criterion Trajectories for Adaptive Authentication: Separating Current Access Decisions from Future Criterion Updates

**Author:** Shuntaro Kawakami  
**Project:** GyroAuth  
**Manuscript status:** Submission candidate

## Abstract

Adaptive authentication must accommodate legitimate changes in devices, networks, locations, roles, and behavior. A criterion that never changes becomes brittle, while a criterion that incorporates observations without independent control creates an additional attack surface: malicious behavior may gradually be absorbed as a new normal. This paper proposes a GyroAuth extension in which authentication-criterion change is represented as a guarded trajectory rather than as an automatic profile update. The model separates the current authentication decision from the decision to modify the criterion used for future authentication. A Criterion Update Candidate is generated from the current criterion, observed access trajectory, Context, Evidence, and History, but it becomes effective only after a Guard selects `ACCEPT`, `DEFER`, `FREEZE`, `REVIEW`, or `ROLLBACK`. We formalize Subject Evaluation and Criterion Integrity Evaluation as separate but related decision processes, define a bounded criterion-update state machine, and implement a deterministic proof of concept comparing direct candidate adoption with guarded adoption. In a legitimate new-device scenario, the guarded model deferred adaptation until challenge confirmation and then accepted a bounded update. Under gradual region-expansion poisoning, the direct-update baseline expanded until an attack reference became admissible, whereas the guarded model froze adaptation before admission. Under single-source Evidence compromise, the guarded model prevented automatic adoption. These results demonstrate the executable structure of the proposal under synthetic assumptions. They do not establish production-grade security, universal attack detection, or empirical false-accept and false-reject rates.

**Keywords:** adaptive authentication, continuous authentication, criterion poisoning, guarded adaptation, criterion integrity, trajectory, GyroAuth

---

## 1. Introduction

Authentication increasingly operates under changing device, network, location, behavioral, and operational conditions. Digital-authentication guidance defines authenticator and assurance requirements, but application-layer systems still need to decide how observations collected across time influence future authentication decisions [1], [2]. A fixed criterion may reject legitimate change; an unconstrained adaptive criterion may normalize attacker-controlled behavior.

The central proposition of this study is:

```text
dynamic criterion
!=
unconstrained self-update
```

The problem is therefore dual. GyroAuth must evaluate whether the current Access Subject remains admissibly related to the Expected Identity, and it must separately evaluate whether the Authentication Criterion remains admissible as the basis for that judgment.

```text
Subject Evaluation
!=
Criterion Integrity Evaluation
```

The resulting decisions are also separate:

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

This separation permits the executable combination:

```text
AUTH_STABLE + FREEZE
```

The current authentication relation may remain temporarily continuable while adaptation of the future criterion is suspended.

The contributions are:

1. a dual evaluation model separating Subject Evaluation from Criterion Integrity Evaluation;
2. a Criterion Trajectory representation for traceable criterion change;
3. a Guarded Criterion Update process with `ACCEPT`, `DEFER`, `FREEZE`, `REVIEW`, and `ROLLBACK`;
4. a bounded Criterion Update State Machine;
5. a deterministic comparison between direct and guarded candidate adoption; and
6. explicit security assumptions, supported claims, limitations, and non-guarantees.

---

## 2. Background and Related Work

### 2.1 GyroAuth foundation

GyroAuth defines authentication as:

```text
Authentication
=
Stability-based Selection over State Convergence
```

The project layers remain:

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Authentication Application
```

This study does not redefine the Gyro Logic Core (`Structure → Slice → Stability`) or the GyroOS runtime contract. It extends the GyroAuth application-layer evaluation scope.

The foundational GyroAuth papers define the base authentication model [14], [15]. The Trajectory-Based Vulnerability Response papers apply trajectory evaluation to post-login operations and security response [16], [17]. The present study targets the integrity of the Authentication Criterion and its update process.

### 2.2 Digital authentication and Zero Trust

NIST SP 800-63-4 and SP 800-63B-4 define digital-identity and authenticator-management requirements [1], [2]. The proposed model does not replace passwords, passkeys, MFA, authenticators, or assurance levels. Authenticator and challenge results may be consumed as Evidence.

NIST Zero Trust Architecture removes implicit trust based on network location and emphasizes repeated policy-based evaluation [3], [4]. GyroAuth is compatible with that architecture but addresses a narrower problem: whether an adaptive authentication component may safely change its future decision criterion.

### 2.3 Continuous authentication and behavioral biometrics

Continuous-authentication research repeatedly evaluates a user during a session using behavioral, biometric, sensor, and contextual signals [5], [6]. GyroAuth shares the premise that authentication should not be reduced to a single login event. Its additional distinction is:

```text
continuous subject evaluation
!=
permission to update the future criterion
```

Behavioral biometrics may supply Evidence, but a behavioral feature is not identical to Identity, and an observed behavioral-profile change is not automatically an accepted criterion update.

### 2.4 Concept drift and poisoning

Concept-drift research studies adaptation under changing data distributions [8]. Such methods may generate candidate adaptations, but a security-sensitive application cannot assume that all observed drift is legitimate.

Poisoning research demonstrates that attacker-controlled training or adaptation data can change future model behavior [10], [13]. This study treats that risk as an authentication-specific state-transition problem: the current subject decision, future criterion adoption, criterion state, update response, and rollback linkage are explicitly separated.

The novelty claim is therefore limited:

> This study does not claim novelty in adaptive or continuous authentication alone. Its contribution is an explicit criterion-integrity model in which proposed authentication-criterion changes form a guarded, traceable trajectory and are authorized independently from current access decisions.

---

## 3. Terminology and Scope

### 3.1 Access Subject

An **Access Subject** is the currently evaluated source of access and operations. It may be a legitimate user, credential thief, session hijacker, relay-mediated operator, bot, remote controller, or mixed source.

```text
Access Subject
!=
Verified Identity
```

### 3.2 Expected Identity

An **Expected Identity** is the persistent reference relation against which the Access Subject is evaluated across changing Sessions and Contexts. Credentials, devices, locations, and behaviors may be Evidence but are not identical to Identity.

### 3.3 Observed Access Trajectory

An **Observed Access Trajectory** is the readable relational configuration obtained by tracing admissible relations among Local Authentication Realizations under the current Orientation, Context, and Slice.

```text
History
!=
Trajectory
```

### 3.4 Authentication Criterion

An **Authentication Criterion** is the Context-relative basis used to interpret Evidence, Deviation, Stability, Trajectory, History, and response conditions.

```text
Authentication Criterion
!=
Fixed Identity Profile
```

### 3.5 Criterion Trajectory and Criterion Integrity

A **Criterion Trajectory** is the traceable relational configuration of criterion changes, including update causes, Evidence provenance, transition magnitude, direction, rate, discrimination effects, responses, and rollback linkage.

**Criterion Integrity** is the condition in which the Authentication Criterion and its update process remain admissible and traceable as a basis for evaluating the authentication relation. It does not imply self-certification; it depends on protected anchors, independent Evidence, retained History, and valid rollback points.

---

## 4. Threat Model

The model protects:

```text
Authentication Relation
Authentication Criterion
Criterion Update Process
Criterion Trajectory
Trusted History
Rollback Points
Decision separation
```

Threat classes include credential theft, session hijacking, relay attacks, gradual behavioral mimicry, criterion poisoning, Evidence-source compromise, and coordinated multi-source compromise.

**Criterion poisoning** is an attack in which an adversary influences Evidence or an observed access trajectory so that malicious states or operations are gradually incorporated into the effective Authentication Criterion.

The main executable attack is gradual region-expansion poisoning. Additional modeled categories include criterion translation, Evidence-priority poisoning, challenge weakening, Context-rule poisoning, history-window poisoning, rollback-link poisoning, slow contraction, and response-policy poisoning.

The minimum trust assumption is that at least one independent Evidence source, protected policy anchor, intact audit linkage, or verified rollback point remains outside simultaneous attacker control. No reliable discrimination or recovery is claimed when all Evidence, anchors, History, and rollback points are compromised.

---

## 5. Formal Security Model

Evaluation proceeds through bounded stages:

```text
t = 0, 1, 2, ...
```

Let the effective criterion be `A_t`. A candidate criterion is generated by:

```text
A*_(t+1)
=
U(A_t, T_t^obs, C_(t+1), E_t, H_t)
```

Candidate generation is not adoption:

```text
A*_(t+1)
!=
A_(t+1)
```

The candidate is evaluated through:

```text
G_t
=
Guard(A_t, A*_(t+1), T_t^obs, C_(t+1), E_t, H_t, P_t)
```

The minimum Guard vector evaluates:

```text
provenance
cross-evidence consistency
challenge confirmation
update magnitude
update rate
update direction
discrimination preservation
rollback linkage
Evidence-source integrity
```

Critical failures are non-compensable:

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

The response is selected by:

```text
D_crit_t = Pi_crit(G_t, Q_t, H_t)
```

The effective transition is:

```text
A_(t+1) = A*_(t+1)   when ACCEPT
A_(t+1) = A_t        when DEFER / FREEZE / REVIEW
A_(t+1) = A_tau      when ROLLBACK, tau < t
```

Subject Evaluation remains separate and selects from:

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

Criterion Update Response selects from:

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

---

## 6. Criterion Update State Machine

Criterion States are:

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

Response semantics are:

- `ACCEPT`: adopt the candidate as the next effective criterion.
- `DEFER`: retain the current criterion while awaiting additional Evidence or challenge results.
- `FREEZE`: suspend adaptive adoption because the update path itself is unsafe; Subject Evaluation may continue.
- `REVIEW`: transfer the decision to an external policy, administrator, stronger verification path, or independent validator.
- `ROLLBACK`: restore a verified prior criterion without deleting the audit trail.

```text
DEFER != FREEZE
REVIEW != DEFER
```

Figures 1-6 in this manuscript are rendered from the canonical specifications in `figures/guarded_criterion_trajectories_mermaid.md`. The source file is provided for reproducibility; the rendered figures are embedded directly in the publication PDF.

---

## 7. Proof-of-Concept Design

The PoC compares two models using the same candidate generator.

### 7.1 Model U: direct adoption

```text
Observation
→ Candidate
→ Direct Adoption
```

### 7.2 Model G: guarded adoption

```text
Observation
→ Candidate
→ Guard
→ Criterion Update Response
→ Effective Criterion Transition
```

The minimum criterion is:

```text
A_t = (
  mu_t,
  width_t,
  provenance_requirement_t,
  challenge_requirement_t,
  rollback_integrity_t
)
```

The implementation uses deterministic synthetic inputs and the Python standard library. Artifacts are:

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

The scenarios are:

```text
N1: Legitimate New Device Transition
P1: Gradual Region Expansion Poisoning
C1: Single Evidence Source Compromise
```

---

## 8. Results

### 8.1 N1: legitimate new-device transition

The guarded model produced:

```text
Auth Decision:
REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_STABLE

Criterion Update Response:
DEFER
→ ACCEPT
→ ACCEPT
```

Final values:

```text
mu    = 0.234
width = 0.120
```

The first candidate was deferred while challenge confirmation was pending. After successful re-authentication and cross-evidence support, a bounded update was accepted without widening the admissible region.

### 8.2 P1: gradual region-expansion poisoning

For the direct-update baseline:

```text
final mu    = 0.3969728
final width = 0.277212
attack reference admissible = true
```

For the guarded model:

```text
final mu    = 0.200
final width = 0.120
freeze stage = 2
attack reference admissible = false
```

The guarded response path was:

```text
DEFER
→ FREEZE
→ FREEZE
→ FREEZE
→ FREEZE
```

At stage 2, the model produced:

```text
AUTH_STABLE + FREEZE
```

This demonstrates that current subject acceptance and permission to redefine future acceptance can be represented independently.

### 8.3 C1: single Evidence-source compromise

The guarded model produced:

```text
FREEZE
→ FREEZE
```

Final values remained:

```text
mu    = 0.200
width = 0.120
```

No candidate was accepted. Apparently strong Evidence values did not compensate for low source integrity and weak cross-evidence consistency.

All seven executable assertions passed.

---

## 9. Discussion

The main result is structural: authentication systems can separate the decision to continue the current relation from the decision to alter the criterion governing future relations. `AUTH_STABLE + FREEZE` is the minimum executable example.

The model remains adaptive. N1 shows that legitimate Context-relative change can be accepted after challenge confirmation, provenance checks, and cross-evidence consistency. The model also recognizes that repeated observation alone does not establish legitimacy:

```text
repeated observation
!=
new normal automatically
```

Criterion Integrity is not self-proof. Its value depends on external or protected references. The Guard is therefore not merely a weighted score: critical failures cannot be averaged away.

---

## 10. Security Claims and Limitations

Under the implemented deterministic assumptions, the PoC structurally demonstrates that:

1. candidate generation can be separated from adoption;
2. Auth Decision and Criterion Update Response can remain separate;
3. supported bounded adaptation can be accepted;
4. direct adoption can cause cumulative criterion expansion;
5. guarded adoption can freeze the implemented P1 attack before attack-reference admission;
6. source-integrity failure can block adoption in C1; and
7. `AUTH_STABLE + FREEZE` is executable.

The study does **not** establish complete prevention of criterion poisoning, universal detection of credential theft or relay attacks, zero false accepts, zero false rejects, perfect identity proof, security under total compromise, production performance, privacy guarantees, formal correctness, or statistical generalization.

The PoC uses synthetic deterministic inputs, a one-dimensional criterion, reduced trajectory proxies, and hand-configured thresholds. It does not measure real-world error rates or operational costs.

---

## 11. Reproducibility and Availability

Run:

```bash
python scripts/simulate_guarded_criterion_update.py \
  --scenarios examples/criterion_update/scenarios.json \
  --output results/criterion_update_results.json
```

The repository contains the simulation source, scenario inputs, summary results, formalization documents, and figure sources.

---

## 12. Conclusion

Adaptive authentication requires criteria that respond to legitimate change, but direct observation-to-criterion incorporation creates a poisoning surface. This paper proposed a GyroAuth extension that represents criterion change as a guarded trajectory. Current Auth Decisions and future Criterion Update Responses are independently selected. A deterministic PoC showed bounded adaptation, poisoning containment under the implemented P1 assumptions, and rejection of compromised-source updates.

The central position is:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## References

[1] D. Temoshok et al., *Digital Identity Guidelines: Authentication and Authenticator Management*, NIST SP 800-63B-4, 2025. DOI: 10.6028/NIST.SP.800-63b-4.

[2] D. Temoshok et al., *Digital Identity Guidelines*, NIST SP 800-63-4, 2025. DOI: 10.6028/NIST.SP.800-63-4.

[3] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, *Zero Trust Architecture*, NIST SP 800-207, 2020. DOI: 10.6028/NIST.SP.800-207.

[4] R. Chandramouli and Z. Butcher, *A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments*, NIST SP 800-207A, 2023. DOI: 10.6028/NIST.SP.800-207A.

[5] M. Abuhamad, A. Abusnaina, D. Nyang, and D. Mohaisen, “Sensor-Based Continuous Authentication of Smartphones’ Users Using Behavioral Biometrics: A Contemporary Survey,” *IEEE Internet of Things Journal*, vol. 8, no. 1, pp. 65–84, 2021. DOI: 10.1109/JIOT.2020.3020076.

[6] A. Al Abdulwahid, N. Clarke, I. Stengel, S. Furnell, and C. Reich, “Security, Privacy, and Usability in Continuous Authentication: A Survey,” *Sensors*, vol. 21, no. 17, 5967, 2021. DOI: 10.3390/s21175967.

[8] J. Gama, I. Žliobaitė, A. Bifet, M. Pechenizkiy, and A. Bouchachia, “A Survey on Concept Drift Adaptation,” *ACM Computing Surveys*, vol. 46, no. 4, Article 44, 2014. DOI: 10.1145/2523813.

[10] B. Biggio, B. Nelson, and P. Laskov, “Poisoning Attacks against Support Vector Machines,” in *Proceedings of the 29th International Conference on Machine Learning*, 2012, pp. 1467–1474.

[13] A. Vassilev, A. Oprea, A. Fordyce, H. Anderson, X. Davies, and M. Hamin, *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*, NIST AI 100-2e2025, 2025. DOI: 10.6028/NIST.AI.100-2e2025.

[14] S. Kawakami, “GyroAuth: Authentication as Stability-Based Selection over State Convergence,” Jxiv, DOI: 10.51094/jxiv.4600.

[15] S. Kawakami, “GyroAuth (Japanese edition): Authentication as Stability-Based Selection over State Convergence,” Jxiv, DOI: 10.51094/jxiv.5341.

[16] S. Kawakami, “Trajectory-Based Vulnerability Response,” Jxiv, DOI: 10.51094/jxiv.5416.

[17] S. Kawakami, Japanese edition of “Trajectory-Based Vulnerability Response,” Jxiv, DOI: 10.51094/jxiv.5440.

---

## AI-Assisted Tools Disclosure

AI-assisted tools were used for structural organization, drafting support, expression refinement, and consistency checking. The author reviewed and edited the content, claims, references, and final manuscript and assumes full responsibility for them.