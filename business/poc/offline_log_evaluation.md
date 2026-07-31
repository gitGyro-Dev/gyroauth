# PoC Candidate 1 — Offline Authentication Log Evaluation

## Status

Initial preferred PoC candidate. Detailed market and use-case selection remains open.

## Objective

Evaluate whether GyroAuth can produce useful trajectory-based authentication and criterion-update decisions from existing authentication and access logs without affecting the production authentication path.

## Target Participants

Initial candidates:

- organizations operating VPN, ZTNA, remote access, or privileged access;
- authentication, IAM, UEBA, or security vendors;
- security SIers conducting access-log analysis;
- research organizations with suitable anonymized datasets.

## Customer Problem Hypothesis

Existing systems may decide whether an event is acceptable but may not clearly separate:

```text
Can current access continue?
```

from:

```text
Should this event update the future authentication criterion?
```

GyroAuth tests whether this separation creates actionable value.

## Candidate Inputs

Preferred normalized input is JSON or CSV containing available subsets of:

- `timestamp`
- `subject_id`
- `device_id`
- `location`
- `network`
- `action`
- `resource`
- `privilege`
- `challenge_result`
- `source_integrity`
- `cross_evidence`
- `context`
- existing authentication or risk decision

Exact required and optional fields must be defined after the first data-discovery session.

## Processing

```text
Normalized events
→ trajectory construction
→ deviation and stability evaluation
→ Auth Decision
→ Criterion Update Candidate
→ guard evaluation
→ Criterion Update Response
→ audit trace and comparison report
```

## Outputs

Auth Decision:

- `AUTH_STABLE`
- `RECONVERGING`
- `REAUTH_REQUIRED`
- `AUTH_FAIL`

Criterion Update Response:

- `ACCEPT`
- `DEFER`
- `FREEZE`
- `REVIEW`
- `ROLLBACK`

Supporting evidence:

- trajectory transitions;
- reason for FREEZE or REVIEW;
- candidate re-authentication events;
- criterion state changes;
- comparison with existing decisions;
- cases requiring operator review.

## Initial Evaluation Questions

- Does GyroAuth identify meaningful cases not visible in the existing decision?
- Can legitimate changes be distinguished from gradual criterion expansion?
- Does the separation of access and update decisions improve explainability?
- How many events require human review?
- Are required log fields available and sufficiently reliable?
- Can results be reproduced from the same input?
- Is processing time acceptable for offline analysis?

## Candidate Metrics

Metrics must be selected according to available ground truth. Candidates include:

- agreement and disagreement with existing decisions;
- true/false positive candidates after operator review;
- re-authentication candidate precision;
- number and ratio of FREEZE/REVIEW events;
- criterion-expansion cases prevented or deferred;
- processing time per event or session;
- memory and trajectory-storage use;
- percentage of events with insufficient evidence;
- analyst review time.

FAR, FRR, EER, or detection metrics must not be claimed unless the dataset and ground truth support them.

## Non-Targets

The first PoC does not:

- replace the production IdP, IAM, VPN, or MFA;
- block user access;
- provide a production SLA;
- prove general resistance to account takeover or poisoning;
- establish legal or regulatory compliance;
- create a fully autonomous criterion-update system.

## Risks

- logs may be incomplete, inconsistent, or unavailable;
- source-integrity fields may need to be inferred or omitted;
- ground truth may be weak;
- review burden may be too high;
- existing controls may already provide sufficient value;
- GyroAuth terminology may require translation into standard security operations language;
- privacy and employee-monitoring concerns may limit usable data.

## Deliverables

- normalized input schema and mapping notes;
- reproducible evaluation configuration;
- execution output and audit trace;
- comparison report;
- limitation and data-quality report;
- recommendation for no further action, extended offline analysis, Shadow Mode, or integration study.

## Transition Criteria

Proceed toward Shadow Mode or a paid continuation only when:

- data quality is sufficient;
- at least one useful decision distinction is demonstrated;
- operational review remains manageable;
- the participant identifies a concrete business or security value;
- the next integration step and responsibility boundary are clear.
