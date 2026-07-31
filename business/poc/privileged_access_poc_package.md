# GyroAuth Privileged Access PoC Package

## Status

Initial commercialization package for external discussion and PoC design.

This document defines the first concrete GyroAuth PoC package. It is intended for customer interviews, collaborative research discussions, security SIers, PAM vendors, IAM teams, SOC teams, and enterprise research or innovation divisions.

The package is deliberately limited to offline evaluation and optional Shadow Mode. It does not control production authentication or terminate sessions.

## 1. Executive Summary

The first GyroAuth PoC targets privileged access.

The central problem is:

```text
A privileged credential was authenticated successfully.

Does the privileged session continue to behave as the same viable authentication relation?

Independently,
should the observed behavior be allowed to update the future accepted criterion?
```

GyroAuth separates:

```text
Current privileged-session assessment
!=
Future criterion-update assessment
```

This makes the following state explicitly representable:

```text
AUTH_STABLE + FREEZE
```

Meaning:

```text
The current session is not immediately rejected,
but the observed behavior must not silently expand the future accepted baseline.
```

The initial PoC evaluates existing privileged-access logs and produces reviewable findings without changing the production access path.

## 2. Customer Problem

Privileged access creates high-impact risk after initial authentication.

A valid credential, MFA result, PAM checkout, or approved connection does not prove that the entire session remains legitimate.

Typical concerns include:

- a legitimate administrator account being used after compromise;
- a contractor or maintenance account operating outside its usual scope;
- gradual expansion of commands, systems, locations, or access times;
- suspicious behavior being incorporated into an adaptive baseline;
- a compromised or unreliable evidence source influencing future decisions;
- abrupt hard blocking being operationally unacceptable;
- SOC or IAM staff being unable to explain why an adaptive model changed.

Existing PAM, IAM, SIEM, UEBA, EDR, and access-control products remain the system of record. GyroAuth is evaluated as a complementary trajectory and criterion-update control layer.

## 3. PoC Objective

The PoC determines whether GyroAuth can reconstruct and evaluate privileged-access trajectories from existing logs and generate useful, explainable review candidates.

The primary objectives are:

1. reconstruct privileged-session trajectories from available events;
2. evaluate session continuity using GyroAuth Auth Decision states;
3. independently evaluate whether observed behavior may update the future criterion;
4. identify `FREEZE`, `REVIEW`, or `REAUTH_REQUIRED` candidates;
5. compare GyroAuth findings with existing alerts, rules, tickets, or analyst judgments;
6. document limitations, missing evidence, and operational implications.

The PoC does not attempt to prove general attack prevention effectiveness.

## 4. Target Customer

Primary customer profiles:

- enterprise IAM or PAM team;
- SOC or CSIRT;
- cloud security team;
- privileged-access management vendor;
- security SIer or managed security provider;
- enterprise research and innovation division;
- organization managing contractor or remote maintenance access.

Preferred first participant:

```text
A team that already retains privileged-access logs
and can compare findings with existing operational judgments.
```

## 5. Initial Scope

Recommended minimum scope:

| Item | Recommended range |
|---|---|
| Privileged users | 5 to 10 |
| Target environment | 1 bounded system or service |
| Observation period | 2 to 4 weeks |
| Log sources | 2 to 4 |
| PoC mode | Offline evaluation |
| Optional mode | Shadow Mode |
| Production enforcement | None |

Candidate bounded environments:

- one cloud administration environment;
- one server-management group;
- one database-administration environment;
- one PAM-controlled remote-access path;
- one maintenance-vendor access flow;
- one high-impact internal operations team.

The first PoC should avoid combining multiple unrelated privileged environments.

## 6. PoC Modes

### 6.1 Offline Evaluation

Historical or periodically exported logs are analyzed outside the production decision path.

```text
Existing privileged-access logs
→ normalization
→ trajectory reconstruction
→ GyroAuth evaluation
→ findings and report
```

Advantages:

- no effect on production availability;
- low initial integration risk;
- easier data minimization;
- repeatable comparison;
- suitable for early external validation.

### 6.2 Shadow Mode

GyroAuth evaluates near-real-time or periodically transferred events while existing systems remain authoritative.

```text
Existing PAM / IAM / SIEM decision
+
GyroAuth Shadow Evaluation
→ comparison and review
```

Shadow Mode is optional and should begin only after offline data mapping succeeds.

## 7. Required Data

### 7.1 Minimum Required Fields

The minimum normalized event schema should include:

| Field | Description |
|---|---|
| `timestamp` | Event time |
| `subject_id` | Privileged user or service identity |
| `session_id` | Privileged session identifier |
| `target_id` | Target system, service, host, or resource |
| `action` | Login, command, API operation, configuration change, or administrative action |
| `result` | Success, failure, denied, challenged, or unknown |
| `source_system` | PAM, IdP, SIEM, cloud audit, OS audit, database audit, etc. |

### 7.2 Strongly Recommended Fields

| Field | Description |
|---|---|
| `device_id` | Administrative device or endpoint |
| `source_network` | Source network, address class, or connection path |
| `privilege` | Role, privilege level, or elevated permission |
| `resource` | Accessed resource or object |
| `command_category` | Normalized command or action category |
| `authentication_method` | Password, MFA, certificate, PAM checkout, etc. |
| `challenge_result` | Step-up or re-authentication result |
| `approval_id` | Ticket, change request, or approval reference |
| `source_integrity` | Confidence in the evidence source |
| `cross_evidence` | Consistency across multiple sources |
| `context` | Maintenance window, incident response, emergency operation, or other business context |

### 7.3 Optional Enrichment

- user role and team;
- approved maintenance window;
- change-management ticket;
- target criticality;
- endpoint security posture;
- geographical or organizational location;
- incident or alert references;
- peer-group baseline;
- known administrative runbook step;
- command sequence or API-call sequence.

## 8. Data Handling Principles

The first PoC should minimize personal and confidential data.

Recommended controls:

- pseudonymize subject identifiers where possible;
- exclude command parameters or payload contents unless necessary;
- transfer only the fields required for agreed evaluation;
- define retention and deletion periods before data transfer;
- separate customer-confidential artifacts from the public repository;
- record source provenance and transformation rules;
- avoid using customer data to update public examples without explicit agreement;
- document whether analysis occurs on customer premises, in a restricted environment, or through exported files.

This public package does not define a final legal, privacy, or security contract.

## 9. Reference Architecture

```text
PAM / IAM / Cloud Audit / OS Audit / Database Audit
                       │
                       ▼
              Log Export or Feed
                       │
                       ▼
             Normalization Adapter
                       │
                       ▼
       Privileged Access Event Schema
                       │
                       ▼
             Trajectory Builder
                       │
                       ▼
               GyroAuth Evaluation
        ┌──────────────┴──────────────┐
        ▼                             ▼
Subject Evaluation          Criterion Integrity Evaluation
        │                             │
        ▼                             ▼
Auth Decision               Criterion Update Response
        └──────────────┬──────────────┘
                       ▼
            Audit Trace and Findings
                       │
                       ▼
             Analyst Review / Report
```

GyroAuth remains outside the production enforcement path during the initial PoC.

## 10. GyroAuth Outputs

### 10.1 Auth Decision

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

Interpretation in the PoC:

- `AUTH_STABLE` — the privileged session remains consistent with the expected trajectory;
- `RECONVERGING` — deviation exists, but continuity may be restored or explained;
- `REAUTH_REQUIRED` — additional verification or operational confirmation is recommended;
- `AUTH_FAIL` — trajectory continuity appears to have collapsed under the configured PoC model.

`AUTH_FAIL` in the PoC is an analytical finding, not an automatic production block.

### 10.2 Criterion Update Response

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

Interpretation:

- `ACCEPT` — the observed behavior may be incorporated into the accepted criterion;
- `DEFER` — more evidence or time is required;
- `FREEZE` — do not update the future baseline from this observation;
- `REVIEW` — human or external-system review is required;
- `ROLLBACK` — a previously accepted criterion state may require reconsideration.

The initial PoC may simulate `ROLLBACK` recommendations but must not alter a production criterion store.

## 11. Core PoC Scenarios

The first package should evaluate at least the following scenarios.

### Scenario A: Expected Administrative Session

Expected outcome:

```text
AUTH_STABLE + ACCEPT
```

Purpose:

- confirm normal trajectory reconstruction;
- verify that ordinary privileged work is not automatically escalated;
- establish an explainable reference case.

### Scenario B: Legitimate but Unusual Maintenance

Examples:

- emergency maintenance;
- new target system;
- approved out-of-hours work;
- unusual command sequence supported by a ticket.

Candidate outcome:

```text
RECONVERGING or REAUTH_REQUIRED
+
DEFER or REVIEW
```

Purpose:

- distinguish legitimate change from immediate failure;
- test use of approval and business context;
- assess analyst interpretability.

### Scenario C: Gradual Privilege or Scope Expansion

Examples:

- increasing number of targets;
- expanding command categories;
- repeated new administrative patterns;
- progressive extension of access time or resource scope.

Candidate outcome:

```text
AUTH_STABLE or RECONVERGING
+
FREEZE
```

Purpose:

- demonstrate that current continuity and future baseline acceptance are separate;
- identify potential gradual poisoning or silent normalization.

### Scenario D: Evidence-Source Degradation

Examples:

- missing endpoint evidence;
- inconsistent PAM and cloud-audit records;
- unreliable source timestamping;
- a single source reporting apparently normal behavior while other evidence is absent.

Candidate outcome:

```text
AUTH_STABLE or RECONVERGING
+
FREEZE or REVIEW
```

Purpose:

- test source-integrity handling;
- prevent apparently strong but insufficient evidence from updating the criterion.

### Scenario E: Session Continuity Collapse

Examples:

- impossible or unexplained target transition;
- high-impact actions inconsistent with role and session history;
- severe multi-source inconsistency;
- abrupt privilege-use pattern incompatible with the expected trajectory.

Candidate outcome:

```text
REAUTH_REQUIRED or AUTH_FAIL
+
FREEZE or REVIEW
```

Purpose:

- identify high-priority analytical findings;
- compare with existing alerts or incident records.

## 12. Evaluation Baseline

GyroAuth findings should be compared against one or more existing references:

- existing PAM policy results;
- SIEM correlation rules;
- UEBA or risk scores;
- IAM conditional-access outcomes;
- SOC alert disposition;
- incident or ticket history;
- administrator or system-owner review;
- approved change or maintenance records.

The purpose is not to assume the existing system is always correct. It is to identify agreement, disagreement, and cases that require explanation.

## 13. Evaluation Metrics

### 13.1 Feasibility Metrics

- percentage of events successfully normalized;
- percentage of sessions reconstructed;
- number of missing critical fields;
- processing time per event or session;
- manual mapping effort;
- number of log-source-specific adapters required.

### 13.2 Analytical Metrics

- distribution of Auth Decision states;
- distribution of Criterion Update Responses;
- number and proportion of `AUTH_STABLE + FREEZE` cases;
- number of `REAUTH_REQUIRED` candidates;
- number of `REVIEW` candidates;
- agreement and disagreement with existing controls;
- analyst-confirmed useful findings;
- analyst-rejected or unexplained findings;
- cases where missing evidence materially changes the result.

### 13.3 Operational Metrics

- analyst review time per finding;
- number of duplicate or low-value findings;
- number of findings linked to an approval, ticket, or incident;
- ability to explain each result from the audit trace;
- estimated effort required for Shadow Mode integration;
- estimated data-retention and storage requirements.

### 13.4 Security Metrics

Where labelled ground truth exists, the PoC may calculate candidate detection metrics. However, FAR, FRR, EER, precision, recall, and false-negative claims must not be generalized beyond the evaluated dataset.

## 14. Success Criteria

The PoC is considered technically successful when all mandatory criteria are met.

### Mandatory

1. At least 90% of in-scope privileged sessions can be reconstructed from agreed data.
2. GyroAuth produces both Auth Decision and Criterion Update Response for the evaluated sessions.
3. Every reported finding includes a reproducible audit trace.
4. At least one meaningful case demonstrates the value of separating current access assessment from criterion-update assessment.
5. Analysts or system owners can review the findings without requiring changes to the Gyro Logic core.
6. The PoC operates without changing production authentication or access decisions.
7. Missing data, unsupported conclusions, and limitations are documented explicitly.

### Commercial Validation Indicators

The following are not mandatory technical success criteria, but support continuation:

- the customer identifies at least one operationally useful finding;
- the customer requests Shadow Mode, additional users, or additional systems;
- a PAM, SIEM, IAM, or security partner sees integration value;
- the required data can be supplied repeatedly;
- the customer can identify an owner and budget for the next phase.

## 15. Failure and No-Go Conditions

The first PoC should stop, narrow scope, or be judged inconclusive when:

- session identifiers cannot be reconstructed reliably;
- required timestamps or event ordering are unavailable;
- available data contains only login success or failure and no meaningful trajectory evidence;
- normalization requires uncontrolled application-specific development;
- customer expectations require certified prevention or real-time blocking;
- the customer requires production enforcement before offline value is demonstrated;
- analyst review cannot distinguish findings from ordinary rule-based alerts;
- privacy, contractual, or security constraints cannot be satisfied;
- success would require changing the fixed Gyro Logic core or merging Auth Decision with Criterion Update Response.

## 16. Non-Goals

The first PoC does not include:

- automatic session termination;
- fail-close production enforcement;
- automatic privilege revocation;
- modification of PAM, IAM, IdP, or target-system policy;
- production criterion updates;
- credential issuance or identity proofing;
- replacement of MFA, PAM, IAM, SIEM, UEBA, or EDR;
- guaranteed account-takeover detection;
- general insider-threat detection;
- certification, compliance attestation, or formal security guarantee;
- 24-hour monitoring or operational support;
- deployment across multiple unrelated environments;
- customer-confidential data in the public GitHub repository.

## 17. Deliverables

The PoC should produce:

1. PoC scope and data agreement;
2. normalized event-schema definition;
3. source-to-schema mapping document;
4. data-quality and missing-field report;
5. trajectory reconstruction summary;
6. Auth Decision and Criterion Update Response results;
7. audit-trace examples;
8. comparison with existing rules, alerts, or analyst judgments;
9. finding review table;
10. limitations and non-guarantees;
11. final PoC report;
12. recommendation for one of:

```text
STOP
REFINE OFFLINE EVALUATION
PROCEED TO SHADOW MODE
PROCEED TO LIMITED INTEGRATION DESIGN
```

Optional deliverables:

- customer-specific architecture diagram;
- demonstration dataset;
- synthetic scenario replay;
- dashboard prototype;
- REST API or batch interface proposal;
- next-phase estimate.

## 18. Proposed Schedule

Recommended duration: 4 to 6 weeks.

| Phase | Duration | Main activities |
|---|---:|---|
| 0. Qualification | 2 to 5 business days | problem confirmation, data-owner confirmation, scope selection |
| 1. Data Mapping | 1 week | sample review, schema mapping, data-quality assessment |
| 2. Offline Implementation | 1 to 2 weeks | normalization, trajectory reconstruction, evaluation setup |
| 3. Evaluation | 1 to 2 weeks | scenario analysis, comparison, analyst review |
| 4. Reporting | 1 week | findings, limitations, recommendation, next-phase design |

The schedule begins only after usable sample data and a responsible customer contact are available.

## 19. Roles and Responsibilities

### GyroAuth Side

- define the PoC schema and evaluation model;
- implement agreed normalization and analysis within scope;
- generate reproducible outputs and audit traces;
- document assumptions and limitations;
- facilitate review sessions;
- produce the final report.

### Customer or Partner Side

- define the target privileged environment;
- provide lawful and authorized access to agreed data;
- explain log semantics and existing controls;
- identify known maintenance, incidents, alerts, and tickets where available;
- provide IAM, PAM, SOC, or system-owner reviewers;
- approve data handling, retention, and deletion procedures;
- avoid treating PoC outputs as production enforcement decisions.

## 20. Costing Approach

A final price requires confirmation of data sources, data volume, normalization complexity, environment restrictions, and review requirements.

The initial commercial model should prefer a fixed-scope paid PoC rather than usage-based SaaS pricing.

A quotation should separate:

1. qualification and scope design;
2. data mapping and normalization;
3. GyroAuth evaluation setup;
4. analysis and review sessions;
5. final reporting;
6. optional Shadow Mode or integration design;
7. travel, secure-environment work, or special compliance requirements.

Cost drivers:

- number of log sources;
- number of target systems;
- availability of session identifiers;
- normalization complexity;
- requirement for on-premises processing;
- data volume and observation period;
- number of review sessions;
- customer-specific dashboard or connector development;
- contractual, privacy, and security review effort.

The public repository should not contain customer-specific pricing or quotations.

## 21. Responsibility Boundary

During the initial PoC:

```text
Existing customer controls remain authoritative.
GyroAuth outputs are analytical findings and review recommendations.
```

The customer remains responsible for:

- production authentication decisions;
- access approval and revocation;
- incident response;
- legal and employment decisions;
- final interpretation of customer-specific context.

Any later production integration requires a separate design for fail-open, fail-close, escalation, audit, rollback, availability, and support responsibility.

## 22. Critical Risks

### Technical

- insufficient event detail;
- inconsistent session identifiers;
- application-specific command semantics;
- weak evidence-source integrity;
- high normalization cost;
- unvalidated thresholds;
- limited ground truth.

### Operational

- too many `REVIEW` or `FREEZE` findings;
- increased analyst workload;
- unclear criterion ownership;
- inadequate approval and ticket context;
- resistance to new terminology.

### Commercial

- overlap with PAM, UEBA, SIEM, or identity-threat features;
- expectation that the existing vendor should provide the capability;
- long enterprise security procurement cycles;
- difficulty funding a PoC from an individual research project;
- PoC completion without a clear production owner.

### Responsibility

- outputs being misrepresented as confirmed compromise;
- production action being taken without customer validation;
- customer data being retained beyond agreement;
- pressure to provide real-time blocking before reliability is established.

## 23. Go / No-Go for Next Phase

### Proceed to Shadow Mode when

- offline reconstruction quality is acceptable;
- at least one customer-recognized useful case is found;
- required logs can be delivered repeatedly;
- processing and storage requirements are manageable;
- the customer identifies a technical and operational owner;
- the customer accepts that existing controls remain authoritative.

### Proceed to Limited Integration Design when

- Shadow Mode results are stable over an agreed period;
- analyst workload is acceptable;
- escalation and re-authentication flows are defined;
- responsibility boundaries are agreed;
- security, privacy, and availability requirements are documented;
- integration does not require changing Gyro Logic or erasing GyroAuth decision separation.

### Stop or redirect when

- data cannot support trajectory reconstruction;
- no operationally meaningful distinction from existing controls is found;
- the customer requires unsupported production guarantees;
- continuation requires disproportionate custom integration;
- no owner, budget, or next-phase decision exists.

## 24. Customer-Facing One-Sentence Description

GyroAuth evaluates whether a privileged session remains consistent under change and independently determines whether its behavior should be allowed to reshape the future accepted baseline.

## 25. Internal Positioning Statement

```text
GyroAuth Privileged Access PoC
=
Offline or Shadow Mode evaluation of privileged-session continuity
+
independent control of future criterion updates
+
explainable analyst review output
```

It is not a production PAM replacement or an automated session-blocking service.
