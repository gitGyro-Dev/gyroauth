# GyroAuth Market and Use-Case Assessment

## Status

Initial critical assessment for commercialization planning.

This document ranks candidate markets by the likelihood that the current GyroAuth research assets can reach a third-party PoC. It does not rank the theoretical importance or long-term market size of each field.

## Decision Principle

The central question is:

```text
With the current maturity of GyroAuth,
where can a third party understand the value,
provide usable data,
and execute a low-risk PoC?
```

The following are treated as constraints:

- current validation is based mainly on deterministic and synthetic scenarios;
- production FAR, FRR, EER, latency, throughput, and scalability are not established;
- enterprise connectors and production APIs are not yet complete;
- GyroAuth should initially complement, not replace, existing authentication infrastructure;
- the preferred starting form is offline log evaluation or Shadow Mode;
- commercial claims must remain narrower than research hypotheses.

## Evaluation Scale

Each field is scored from 1 to 5.

| Score | Meaning |
|---:|---|
| 1 | Very unfavorable at the current stage |
| 2 | Major obstacles; research or partner dependency is high |
| 3 | Feasible with a carefully limited scope |
| 4 | Strong initial PoC candidate |
| 5 | Highly suitable for immediate external validation |

Higher is better for all criteria except responsibility risk, where a higher score means the risk can be limited more easily.

## Evaluation Criteria

1. **Customer problem** — severity and clarity of the operational or security problem.
2. **Market comprehensibility** — ease of explaining the value without teaching the full Gyro theory.
3. **Competitive position** — ability to define a complementary or differentiated position among existing products.
4. **Data availability** — likelihood that useful logs and contextual evidence already exist.
5. **PoC feasibility** — ability to conduct an offline or Shadow Mode PoC without changing production decisions.
6. **Differentiation** — strength of the distinction created by trajectory evaluation and guarded criterion updates.
7. **Implementation cost** — ability to start with modest integration and engineering effort.
8. **Responsibility containment** — ability to avoid directly controlling high-impact production decisions during the first PoC.
9. **Individual-project feasibility** — realistic ability to deliver and support the initial scope from the current project structure.
10. **Paid-PoC potential** — likelihood that a customer or partner would fund validation.

## Summary Ranking

| Rank | Candidate field | Total / 50 | Current judgment |
|---:|---|---:|---|
| 1 | Privileged access | 39 | First concrete PoC target |
| 2 | VPN / ZTNA | 38 | Second validation target |
| 3 | AI Agent governance | 35 | Exploratory differentiation target |
| 4 | IoT / OT | 31 | Partner-dependent secondary target |
| 5 | General continuous authentication | 29 | Too broad for initial positioning |
| 6 | Financial transactions | 24 | Defer due to validation and liability requirements |

The scores are directional planning tools, not statistically validated market measurements.

## Score Matrix

| Criterion | VPN / ZTNA | Privileged access | IoT / OT | AI Agent | Financial transactions | General continuous authentication |
|---|---:|---:|---:|---:|---:|---:|
| Customer problem | 4 | 5 | 4 | 4 | 5 | 3 |
| Market comprehensibility | 5 | 4 | 3 | 3 | 5 | 3 |
| Competitive position | 3 | 4 | 3 | 4 | 2 | 2 |
| Data availability | 5 | 4 | 3 | 3 | 4 | 4 |
| PoC feasibility | 5 | 5 | 3 | 4 | 2 | 4 |
| Differentiation | 3 | 4 | 4 | 5 | 2 | 3 |
| Implementation cost | 4 | 4 | 2 | 4 | 2 | 4 |
| Responsibility containment | 4 | 4 | 3 | 4 | 1 | 4 |
| Individual-project feasibility | 3 | 3 | 2 | 3 | 1 | 4 |
| Paid-PoC potential | 2 | 2 | 4 | 1 | 3 | 2 |
| **Total** | **38** | **39** | **31** | **35** | **24** | **33** |

### Scoring correction

The raw total for general continuous authentication is 33. Its strategic rank remains fifth because the category is too broad and risks collapsing GyroAuth into an undifferentiated market label. The summary ranking uses an adjusted strategic score of 29 after applying a positioning penalty of four points.

AI Agent governance receives a high technical and strategic score but a low paid-PoC score because customer ownership, budget, operational standards, and required evidence are still immature. It is included in the first three as an exploratory track, not as the most reliable near-term revenue track.

# 1. Privileged Access

## Candidate scope

- cloud administrators;
- server and database administrators;
- privileged remote maintenance;
- high-impact internal operations;
- contractor or vendor access;
- sensitive administrative sessions.

## Why it ranks first

Privileged access has a clear security problem after initial authentication: a valid credential does not prove that the entire session remains legitimate. It also creates a natural distinction between:

```text
May the current session continue?
```

and:

```text
Should this behavior update the future baseline?
```

This is the strongest current match for `AUTH_STABLE + FREEZE`. A session can remain operational while suspicious baseline expansion, evidence-source degradation, or unusual privilege use is held for review.

## Why it is selected as the first concrete PoC

Privileged access is narrower and more controllable than VPN / ZTNA for the first external package.

The first PoC can be limited to:

- a small number of privileged identities;
- a defined administrative system or resource group;
- selected session and operation logs;
- a fixed observation period;
- offline reconstruction or Shadow Mode;
- no production blocking and no direct baseline modification.

This bounded scope reduces the number of environmental variables that must be modeled at the outset. It avoids making the first PoC depend heavily on physical location, mobile networks, endpoint posture, network routing, proxy behavior, and other remote-access context.

The value proposition is also easier to state:

```text
A privileged credential was accepted.
Did the authenticated administrative session continue as the same expected relation?
And should the observed behavior be allowed to alter the future baseline?
```

## Strong points

- consequences of account misuse are easy to explain;
- authentication, access, and operation logs often exist;
- Shadow Mode avoids immediate interference with production access;
- review and audit outputs have direct operational meaning;
- guarded criterion updates can be positioned as an additional control rather than a replacement for PAM, IAM, or SIEM;
- a limited user group can be selected for PoC;
- scope can be restricted to one system, one role group, or one maintenance process;
- customer-side review can validate findings without delegating blocking authority to GyroAuth.

## Critical weaknesses

- established PAM, UEBA, SIEM, and identity-threat products already cover adjacent functions;
- customers may view GyroAuth as another behavioral risk score unless the update-control distinction is demonstrated clearly;
- operation events are application-specific and require normalization;
- privileged-access buyers expect high reliability, traceability, and responsibility boundaries;
- a single developer should not initially provide real-time blocking or fail-close enforcement;
- expected administrative behavior may vary significantly by role, incident, maintenance window, and emergency procedure.

## Initial PoC position

```text
Privileged-session log evaluation
+ trajectory reconstruction
+ criterion-update guard
→ offline findings and Shadow Mode review candidates
```

The first PoC should not terminate sessions, change permissions, or modify production authentication criteria.

## Paid-PoC likelihood

Moderate. The problem is serious, but an unknown research project will usually need an SIer, PAM vendor, security company, or internal research division as an intermediary.

# 2. VPN / ZTNA

## Candidate scope

- enterprise VPN sessions;
- ZTNA access;
- remote desktop connections;
- remote administration;
- cloud management access;
- changes in device, location, network, and session context.

## Why it remains second

VPN and ZTNA provide a recognizable explanation of trajectory-based authentication. Normal users change devices, networks, and locations, while attackers may gradually imitate observed behavior or expand an accepted region. The available telemetry may be comparatively standardized, and an offline PoC can be conducted without changing the authentication path.

However, the initial scope becomes wider more quickly than privileged access. A meaningful evaluation may involve several interacting layers:

- identity and authentication events;
- endpoint and device posture;
- source network and routing context;
- location and geolocation quality;
- VPN or ZTNA session lifecycle;
- application and resource access;
- step-up authentication;
- proxies, mobile networks, roaming, and legitimate travel;
- privacy-sensitive contextual information.

This makes VPN / ZTNA suitable as the second validation package after the minimum GyroAuth PoC workflow, log-normalization process, review output, and evaluation report have been established with privileged access.

## Strong points

- customer problem is familiar;
- logs commonly contain timestamps, user IDs, devices, source networks, locations, challenge results, and session events;
- legitimate change and suspicious drift can be demonstrated using existing GyroAuth scenarios;
- `REAUTH_REQUIRED` can connect conceptually to an existing MFA or step-up flow;
- Shadow Mode can compare GyroAuth decisions with current VPN or ZTNA outcomes.

## Critical weaknesses

- continuous access evaluation and risk-based conditional access are already established concepts;
- vendors may already provide proprietary behavioral and device-risk models;
- location and network data can be noisy, privacy-sensitive, or distorted by proxies and mobile networks;
- without real error-rate evidence, GyroAuth cannot claim superior detection;
- customers may ask why existing IdP or ZTNA rules cannot reproduce the same behavior;
- combining multiple physical, network, endpoint, and identity signals increases normalization and interpretation cost.

## Initial PoC position

```text
Existing VPN / ZTNA logs
→ offline trajectory evaluation
→ re-authentication and FREEZE candidates
→ comparison with current rules
```

The differentiator must be the explicit separation of current access continuity and future baseline acceptance, not merely continuous risk scoring.

## Paid-PoC likelihood

Moderate. It is easy to understand at a high level, but the actual evaluation scope can expand rapidly. Partner-led validation is preferable.

# 3. AI Agent Governance

## Candidate scope

- enterprise AI agents;
- autonomous workflow agents;
- API-executing agents;
- agents accessing internal data;
- multi-agent environments;
- continuously adapted agent behavior profiles.

## Why it is included in the first three

AI Agents provide the clearest conceptual differentiation for GyroAuth. Agent identity cannot be reduced to credentials alone when tools, goals, access patterns, delegated authority, and behavior change over time. The separation between current execution permission and future behavioral-baseline updates directly addresses agent drift and poisoning concerns.

## Strong points

- high conceptual fit with trajectory continuity;
- strong need to distinguish identity, authorization, behavior, and adaptation;
- guarded criterion updates are easier to present as a model-governance control;
- synthetic and sandboxed PoCs can be built without customer production access;
- the field may allow GyroAuth to define a category rather than enter a mature feature comparison.

## Critical weaknesses

- the market, terminology, standards, ownership, and budgets remain unsettled;
- many organizations do not yet retain sufficiently structured agent-operation logs;
- it is unclear whether IAM, AI governance, application security, platform engineering, or SOC owns the problem;
- customers may be interested intellectually but unwilling to fund a PoC;
- general agent-safety claims would be unjustified;
- the relationship between agent authentication, authorization, runtime policy, and behavioral governance must be kept precise.

## Initial PoC position

```text
Sandboxed agent execution trace
+ tool-use and resource-access events
+ expected task trajectory
→ current execution assessment
+ future behavior-baseline update response
```

The PoC should focus narrowly on whether observed actions may influence the accepted agent baseline. It should not claim general AI safety or autonomous-agent control.

## Paid-PoC likelihood

Low to moderate in the immediate term. This is a strategic exploration track and a possible differentiator for joint research, innovation programs, or platform-vendor collaboration.

# 4. IoT / OT

## Candidate scope

- industrial equipment;
- gateways and sensor groups;
- remote maintenance terminals;
- machine-to-machine access;
- device replacement and firmware changes;
- gradual communication or operating-pattern changes.

## Positive fit

IoT and OT identities are naturally relational and behavioral. Fixed credentials may remain valid while device communication, timing, peer relationships, or operational sequences drift. GyroAuth could distinguish legitimate maintenance and replacement from gradual compromise, while freezing baseline updates during uncertain periods.

## Why it is not in the first three

- access to meaningful OT data is difficult;
- domain expertise and site-specific interpretation are essential;
- safety and availability consequences are high;
- integration environments are heterogeneous and often legacy-dependent;
- cybersecurity validation commonly requires trusted industrial partners;
- an individual project cannot responsibly support production control environments alone.

## Recommended role

Pursue only with an OT security provider, equipment vendor, university laboratory, manufacturing partner, or funded demonstration program. Start with offline network and maintenance logs, never direct control.

# 5. General Continuous Authentication

## Positive fit

The category is immediately related to GyroAuth. It provides natural use of state convergence, trajectory evaluation, step-up authentication, and differentiated failure states.

## Why it is strategically weak as the first market label

`Continuous Authentication` is too broad and crowded. Using it as the main market position creates several problems:

- GyroAuth can be mistaken for another behavioral scoring engine;
- the criterion-update guard becomes a secondary feature rather than the central distinction;
- competitors span biometrics, device intelligence, UEBA, risk-based authentication, fraud detection, and conditional access;
- customers will immediately request benchmark comparisons that GyroAuth cannot yet provide;
- target buyer, data source, implementation form, and business owner remain vague.

## Recommended role

Use continuous authentication as the technical category, not the initial commercial market. Enter through a bounded problem such as privileged access or VPN / ZTNA.

# 6. Financial Transactions

## Positive fit

Financial activity contains rich trajectories, gradual fraud patterns, device and location changes, high-value decisions, and strong demand for explainability.

## Why it ranks last for the initial phase

- mature fraud platforms and specialist vendors dominate the field;
- buyers require rigorous statistical validation and extensive historical data;
- false positives and false negatives have direct financial and customer consequences;
- regulations, model governance, data residency, privacy, and audit requirements are substantial;
- transaction behavior is not identical to authentication continuity;
- liability and support expectations are incompatible with an early individual research project;
- access to representative datasets is difficult.

## Recommended role

Defer until GyroAuth has validated metrics, broader engineering support, and a specialized financial partner. Financial transactions may later be an application field, but they should not be used as the first proof of commercial viability.

# Selected Initial Three

## 1. Privileged Access — first concrete PoC target

This is the strongest combination of problem severity, bounded scope, explainability, and direct relevance of guarded criterion updates.

### Initial hypothesis

GyroAuth can identify privileged sessions that may continue under existing controls while preventing uncertain behavior from silently expanding the accepted baseline.

### Preferred external partners

- PAM vendors;
- security SIers;
- enterprise SOC or IAM teams;
- cloud security providers;
- managed security providers;
- large-company research and innovation divisions.

## 2. VPN / ZTNA — second validation target

This remains a strong field for obtaining recognizable logs and explaining normal environmental change, suspicious drift, re-authentication, and Shadow Mode comparison. It should follow the privileged-access PoC rather than compete with it for the first package.

### Initial hypothesis

GyroAuth can improve the interpretability of remote-access evaluation by separating session-continuity decisions from future criterion updates.

### Preferred external partners

- VPN and ZTNA vendors;
- IdP and IAM integrators;
- remote-access service providers;
- enterprise information-system departments;
- security SIers.

## 3. AI Agent Governance — exploratory differentiation target

This is not the safest near-term revenue target, but it may create the strongest original positioning and joint-research opportunities.

### Initial hypothesis

GyroAuth can evaluate whether an agent's current execution remains acceptable while independently deciding whether the observed behavior may update the agent's future accepted trajectory.

### Preferred external partners

- enterprise agent-platform providers;
- AI governance teams;
- API security vendors;
- universities and research institutions;
- corporate innovation programs;
- agent observability and orchestration providers.

# Portfolio Rule

The three selected fields now have explicit priority and different roles:

```text
Privileged Access
= first concrete PoC package

VPN / ZTNA
= second validation package after the PoC method is established

AI Agent Governance
= bounded exploratory differentiation track
```

Recommended initial allocation:

| Track | Relative effort |
|---|---:|
| Privileged access | 60% |
| VPN / ZTNA | 25% |
| AI Agent governance | 15% |

# First PoC Decision

The first concrete GyroAuth PoC package is fixed as:

```text
Privileged Access
+ offline log evaluation
+ optional Shadow Mode comparison
+ no production enforcement
```

## Reasons

1. The subject population and monitored systems can be limited.
2. Administrative operations provide a clearer bounded trajectory than broad remote-access context.
3. The security consequence of session misuse is understandable without explaining the entire Gyro theory.
4. `AUTH_STABLE + FREEZE` has a concrete operational interpretation.
5. Existing PAM, IAM, SIEM, and system logs can be used without replacing those systems.
6. Findings can be reviewed by the customer before any operational action is considered.
7. The first implementation can avoid physical-location, mobile-network, endpoint-posture, and routing complexity.

## Required next artifacts

1. Privileged-access PoC purpose and problem statement.
2. Target customer and target-system boundary.
3. Minimum input-log schema.
4. Event normalization and trajectory-construction rules.
5. PoC architecture and data flow.
6. Baseline comparison method.
7. Success criteria and evaluation metrics.
8. Explicit non-goals and responsibility boundary.
9. Deliverables and report structure.
10. Indicative schedule and pricing logic.

# Go / No-Go Conditions

## Continue a field when

- a data owner confirms that suitable logs exist;
- the operational problem is recognized without extensive theory education;
- a Shadow Mode or offline comparison can be executed;
- a buyer or partner can identify a budget or research mechanism;
- the result can be measured against an existing rule, decision, or review process.

## Defer a field when

- production intervention is required before offline value is demonstrated;
- representative data cannot be obtained;
- the customer expects certified detection or prevention claims;
- the field requires 24-hour operational support;
- success depends on changing the Gyro Logic core or erasing the distinction between Auth Decision and Criterion Update Response.
