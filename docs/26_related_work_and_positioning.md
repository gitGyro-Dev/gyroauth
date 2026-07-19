# Guarded Criterion Trajectories — Related Work and Positioning

## 1. Purpose

This document completes the Related Work portion of **Priority K: Cross-document Review, Related Work, Figures, and Submission Refinement**.

It positions the proposed GyroAuth model against adjacent research and standards without overstating novelty.

The review focuses on:

```text
Digital authentication guidance
Adaptive and risk-based authentication
Continuous authentication
Behavioral biometrics
Concept drift and online adaptation
Data poisoning and adversarial machine learning
Zero Trust
Anomaly detection and UEBA
```

The intended contribution is not that no prior system adapts authentication criteria. The intended contribution is the explicit separation and joint execution of:

```text
current Auth Decision
```

and:

```text
permission to change the future Authentication Criterion
```

through a traceable criterion trajectory and guarded update responses.

---

## 2. Positioning Summary

| Area | Typical primary concern | Relation to this study | Main distinction of the proposed model |
|---|---|---|---|
| Digital authentication guidance | authenticator assurance, authentication protocols, session management | establishes deployment and assurance context | does not replace authenticators or AAL requirements |
| Adaptive / risk-based authentication | change challenge or access requirements using contextual risk | closely adjacent | separately evaluates whether the criterion itself may change |
| Continuous authentication | repeatedly assess the user during a session | closely adjacent | separates current subject evaluation from criterion-update authorization |
| Behavioral biometrics | classify or verify users from behavioral signals | possible Evidence source | Evidence is not Identity, and profile adaptation is not automatically accepted |
| Concept drift | maintain predictive performance under changing distributions | supplies adaptation concepts | legitimate drift and adversarial criterion movement must be distinguished under security assumptions |
| Data poisoning / adversarial ML | manipulate training or online-learning data to alter model behavior | supplies the core attack analogy | studies poisoning of an authentication criterion and adds domain-specific response semantics |
| Zero Trust | remove implicit trust and continuously evaluate access | compatible architectural context | focuses specifically on integrity of the changing authentication criterion |
| UEBA / anomaly detection | identify anomalous entities, behavior, or events | related detection layer | a current anomaly score is distinct from authorization to redefine future normality |

---

## 3. Digital Authentication Guidance

NIST SP 800-63B-4 defines requirements for authentication and authenticator management at multiple assurance levels. Its principal concern is establishing that a claimant is the subscriber associated with an account through approved authenticators and protocols.

The proposed GyroAuth model is not an alternative to password, passkey, cryptographic authenticator, MFA, or authenticator assurance requirements.

```text
Authenticator validity
!=
Authentication Relation Continuity
```

and:

```text
successful authentication event
!=
permission to adapt the future criterion
```

The guarded-criterion model can consume authenticator results and challenge results as Evidence. It does not weaken protocol-level requirements or claim that trajectory evaluation alone proves identity.

Positioning statement:

> Digital authentication guidance defines requirements for authenticators and authentication events. This study addresses an additional application-layer question: whether observations collected during and after those events may modify the criterion used for future authentication decisions.

---

## 4. Adaptive and Risk-Based Authentication

Adaptive and risk-based authentication systems use contextual signals such as device, network, location, operation sensitivity, and behavior to change authentication requirements or access responses.

This area is closely related because GyroAuth also evaluates Context-relative Evidence and can require re-authentication or escalation.

The proposed distinction is not simply the use of more signals or a new risk score. It is the presence of a second explicit decision stream:

```text
D_auth_t
=
current authentication decision
```

```text
D_crit_t
=
criterion-update response
```

An adaptive system may correctly increase or decrease current authentication friction while still leaving unspecified how observations alter future baselines. The proposed model makes that update path explicit:

```text
Observation
→ Criterion Update Candidate
→ Guard
→ ACCEPT / DEFER / FREEZE / REVIEW / ROLLBACK
→ Effective Criterion
```

Positioning statement:

> The model is adjacent to adaptive and risk-based authentication but focuses on the integrity and authorization of criterion change itself rather than only on risk-conditioned current authentication responses.

---

## 5. Continuous Authentication

Continuous authentication repeatedly or continuously evaluates whether an ongoing user or subject remains legitimate during a session. Surveys of continuous authentication describe behavioral, biometric, sensor, and contextual signals, as well as security, privacy, usability, replay, and matching challenges.

The GyroAuth proposal shares the premise that authentication should not be reduced to a single login event.

However:

```text
continuous observation
!=
Authentication Relation Continuity
```

and:

```text
continuous subject scoring
!=
continuous permission to update the scoring criterion
```

The proposed model distinguishes:

```text
Subject Evaluation Loop
```

from:

```text
Criterion Integrity Loop
```

The result `AUTH_STABLE + FREEZE` is the minimum executable demonstration of this separation.

Positioning statement:

> Continuous authentication evaluates whether the current subject should remain accepted. Guarded criterion trajectories add a separate evaluation of whether the evidence produced during that process may redefine the future acceptance basis.

---

## 6. Behavioral Biometrics

Behavioral biometrics uses interaction patterns, motion, gait, keystroke dynamics, touch behavior, voice, and related signals to verify or identify users. These approaches can provide Evidence for continuous or implicit authentication.

GyroAuth does not define Identity as a behavioral profile.

```text
behavioral feature
!=
Identity
```

and:

```text
behavioral profile update
!=
accepted Authentication Criterion update
```

Behavioral change can be legitimate. It can also be attacker mimicry, sensor compromise, replay, or gradual poisoning. Therefore, behavior is treated as one Evidence family interpreted with provenance, cross-evidence consistency, Context, challenge results, history, and rollback linkage.

Positioning statement:

> Behavioral biometrics can supply Evidence to GyroAuth, but the proposed model does not equate behavioral similarity with identity and does not permit observed behavior to redefine the criterion without an independent update decision.

---

## 7. Concept Drift and Online Adaptation

Concept drift research studies changes in the relationship between input data and target concepts over time and develops methods for drift detection, adaptation, evaluation, and historical model reuse.

This literature is directly relevant to legitimate long-term change in authentication behavior.

However, a security-sensitive criterion cannot assume that all drift is naturally generated.

```text
observed drift
!=
legitimate drift automatically
```

The proposed model distinguishes:

```text
legitimate Context-relative adaptation
```

from:

```text
adversarial criterion movement
```

by evaluating provenance, cross-evidence consistency, challenge confirmation, update direction, cumulative rate, discrimination preservation, and rollback integrity.

The model is not presented as a general concept-drift algorithm. Its update function `U` may later use such algorithms, but adoption remains subject to GyroAuth Guard semantics.

Positioning statement:

> Concept-drift methods can generate or support candidate adaptations. This study adds a security decision layer that determines whether a candidate adaptation is admissible as an authentication criterion update.

---

## 8. Data Poisoning and Adversarial Machine Learning

Data poisoning attacks manipulate training or adaptation data so that a learned model behaves according to an attacker objective. Research covers offline poisoning, online poisoning, attacker knowledge, lifecycle stages, and mitigations.

The threat studied here is analogous but domain-specific:

> Criterion poisoning is an attack in which an adversary influences Evidence or an observed access trajectory so that malicious states or operations are gradually incorporated into the effective authentication criterion.

The PoC does not implement a machine-learning classifier. It uses a deterministic criterion to isolate the state-transition problem.

The contribution relative to generic poisoning literature is the authentication-specific separation among:

```text
current subject admissibility
future criterion adoption
criterion state
update response
rollback linkage
```

and the response set:

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

Positioning statement:

> Adversarial-learning research establishes that adaptive models can be poisoned. This study operationalizes that risk for adaptive authentication by representing criterion changes as guarded trajectory transitions with explicit containment and recovery responses.

---

## 9. Zero Trust

NIST Zero Trust Architecture removes implicit trust based on network location and focuses access decisions on identities, devices, resources, policy, and continuously evaluated conditions.

GyroAuth is compatible with this architecture because it does not treat a valid session, known network, or prior authentication event as permanent trust.

```text
known network
!=
trusted subject automatically
```

```text
valid session
!=
continuable authentication relation automatically
```

The present study does not propose a complete Zero Trust Architecture. It focuses on one narrower control problem: whether the criterion used by an adaptive authentication component remains trustworthy enough to continue changing.

Positioning statement:

> Zero Trust supplies the broader policy and architecture context for repeated access evaluation. Guarded criterion trajectories address the integrity of one adaptive decision component within such an architecture.

---

## 10. UEBA and Anomaly Detection

UEBA and anomaly-detection systems identify behavior that differs from expected patterns, peer groups, baselines, or historical behavior. These systems may provide risk signals or trigger responses.

GyroAuth can consume anomaly-related outputs as Evidence, but it does not equate anomaly with authentication failure.

```text
Deviation exists
!=
AUTH_FAIL
```

and:

```text
low anomaly score
!=
permission to update future normality
```

A major relevance of UEBA is baseline adaptation. If a baseline changes automatically from observed activity, repeated malicious operations may be normalized. The proposed model isolates this issue through candidate/adoption separation and cumulative Guard checks.

Positioning statement:

> Anomaly and UEBA systems evaluate divergence from a baseline. Guarded criterion trajectories additionally evaluate whether that baseline itself may move, expand, weaken, or be restored.

---

## 11. Novelty Boundary

The paper should not claim that it is the first work to:

```text
use adaptive authentication
use continuous authentication
use behavioral Evidence
address concept drift
study poisoning attacks
apply Zero Trust principles
use rollback in security systems
```

The defensible novelty candidate is the combined GyroAuth formulation:

1. represent authentication-criterion change as a Criterion Trajectory;
2. generate a Criterion Update Candidate without automatic adoption;
3. evaluate current authentication and criterion integrity in separate decision spaces;
4. expose `ACCEPT`, `DEFER`, `FREEZE`, `REVIEW`, and `ROLLBACK` as explicit update responses;
5. preserve critical non-compensable Guards;
6. demonstrate `AUTH_STABLE + FREEZE` as an executable state combination;
7. connect normal adaptation and criterion poisoning within one bounded state-transition model.

Recommended novelty wording:

> This study does not claim novelty in adaptive or continuous authentication alone. Its contribution is an explicit criterion-integrity model in which proposed authentication-criterion changes form a guarded, traceable trajectory and are authorized independently from current access decisions.

---

## 12. Reference Set for the Manuscript

### Digital authentication and Zero Trust

[1] D. Temoshok et al., *Digital Identity Guidelines: Authentication and Authenticator Management*, NIST SP 800-63B-4, 2025. DOI: 10.6028/NIST.SP.800-63b-4.

[2] D. Temoshok et al., *Digital Identity Guidelines*, NIST SP 800-63-4, 2025. DOI: 10.6028/NIST.SP.800-63-4.

[3] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, *Zero Trust Architecture*, NIST SP 800-207, 2020. DOI: 10.6028/NIST.SP.800-207.

[4] R. Chandramouli and Z. Butcher, *A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments*, NIST SP 800-207A, 2023. DOI: 10.6028/NIST.SP.800-207A.

### Continuous authentication and behavioral biometrics

[5] M. Abuhamad, A. Abusnaina, D. Nyang, and D. Mohaisen, “Sensor-Based Continuous Authentication of Smartphones’ Users Using Behavioral Biometrics: A Contemporary Survey,” *IEEE Internet of Things Journal*, vol. 8, no. 1, pp. 65–84, 2021. DOI: 10.1109/JIOT.2020.3020076.

[6] A. Al Abdulwahid, N. Clarke, I. Stengel, S. Furnell, and C. Reich, “Security, Privacy, and Usability in Continuous Authentication: A Survey,” *Sensors*, vol. 21, no. 17, 5967, 2021. DOI: 10.3390/s21175967.

[7] A. Mahfouz, T. M. Mahmoud, and A. Sharaf Eldin, “A Survey on Behavioral Biometric Authentication on Smartphones,” *Journal of Information Security and Applications*, vol. 37, pp. 28–37, 2017. DOI should be verified against the final publisher record before submission.

### Concept drift and online adaptation

[8] J. Gama, I. Žliobaitė, A. Bifet, M. Pechenizkiy, and A. Bouchachia, “A Survey on Concept Drift Adaptation,” *ACM Computing Surveys*, vol. 46, no. 4, Article 44, 2014. DOI: 10.1145/2523813.

[9] Y. Sun, K. Tang, Z. Zhu, and X. Yao, “Concept Drift Adaptation by Exploiting Historical Knowledge,” *IEEE Transactions on Neural Networks and Learning Systems*, vol. 29, no. 10, pp. 4822–4832, 2018. DOI should be verified against the final publisher record before submission.

### Poisoning and adversarial learning

[10] B. Biggio, B. Nelson, and P. Laskov, “Poisoning Attacks against Support Vector Machines,” in *Proceedings of the 29th International Conference on Machine Learning*, 2012, pp. 1467–1474.

[11] Y. Wang and K. Chaudhuri, “Data Poisoning Attacks against Online Learning,” arXiv:1808.08994, 2018. Final publication status should be verified before submission.

[12] X. Zhang, X. Zhu, and L. Lessard, “Online Data Poisoning Attack,” arXiv:1903.01666, 2019. Final publication status should be verified before submission.

[13] A. Vassilev, A. Oprea, A. Fordyce, H. Anderson, X. Davies, and M. Hamin, *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*, NIST AI 100-2e2025, 2025. DOI: 10.6028/NIST.AI.100-2e2025.

### GyroAuth publications

[14] S. Kawakami, “GyroAuth: Authentication as Stability-Based Selection over State Convergence,” Jxiv, DOI: 10.51094/jxiv.4600.

[15] S. Kawakami, “GyroAuth：状態収束に対する安定性に基づく認証,” Jxiv, DOI: 10.51094/jxiv.5341.

[16] S. Kawakami, “Trajectory-Based Vulnerability Response,” Jxiv, DOI: 10.51094/jxiv.5416.

[17] S. Kawakami, Japanese edition of “Trajectory-Based Vulnerability Response,” Jxiv, DOI: 10.51094/jxiv.5440.

---

## 13. Verification Notes

Before final submission:

```text
verify exact author lists and page ranges
verify final publication status for arXiv references
verify DOI for the behavioral-biometric survey
choose one citation style and apply it consistently
confirm Jxiv title capitalization and Japanese titles
add access dates only where required by the venue
```

References [1]–[6], [8], [10], [13]–[17] are sufficient for the first submission draft. References [7], [9], [11], and [12] should be treated as provisional until publisher metadata is verified.

---

## 14. Related-work Conclusion

The proposed model belongs at the intersection of adaptive authentication, continuous authentication, concept drift, and poisoning-resistant online adaptation.

Its strongest defensible position is:

> Existing work motivates adaptive current authentication, continuous subject evaluation, drift handling, and poisoning awareness. GyroAuth adds an explicit application-layer distinction between accepting the current authentication relation and authorizing observations to redefine the criterion used for future decisions.

This distinction is represented formally and demonstrated by:

```text
AUTH_STABLE + FREEZE
```

which means:

```text
continue evaluating the current relation
while suspending criterion adaptation
```
