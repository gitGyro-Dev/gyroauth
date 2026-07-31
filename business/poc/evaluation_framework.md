# PoC Evaluation Framework

## Principle

A PoC is successful only when it produces evidence that supports a customer or research decision.

## Evaluation Areas

### Customer problem

- Is the problem concrete?
- Who owns it?
- What is the current cost or risk?

### Current alternative

- What tools, controls, or reviews are already used?
- Is GyroAuth complementary, competitive, or redundant?

### Data feasibility

- Are the necessary events available?
- Are subject, device, source, timestamp, and outcome fields reliable?
- Can the data be minimized or anonymized?

### Technical feasibility

- Can trajectories be constructed?
- Are results reproducible?
- What processing and storage costs are observed?

### Decision value

- Does GyroAuth produce useful distinctions?
- Are `REAUTH_REQUIRED`, `AUTH_FAIL`, and `AUTH_STABLE + FREEZE` operationally meaningful?
- Does the audit trace improve review?

### Operational burden

- How many events require `REVIEW` or `FREEZE` handling?
- Who resolves them?
- Is the review workload manageable?

### Continuation value

- Is there a justified next phase?
- Is the suitable path a paid PoC, integration study, consulting, licensing, or joint research?
- Can a small team deliver it responsibly?

## Evidence Classes

Label every result as one of:

1. deterministic research scenario;
2. synthetic-data evaluation;
3. historical real-data evaluation;
4. Shadow Mode observation;
5. limited live integration;
6. production evidence.

Do not present evidence from one class as a stronger class.

## Decision Outcomes

- `STOP`
- `REFINE`
- `EXTEND_OFFLINE`
- `SHADOW_MODE`
- `INTEGRATION_STUDY`
- `PAID_CONTINUATION`
- `JOINT_RESEARCH`

## Criticism Review Format

```text
Criticism
→ Current fact
→ Missing evidence
→ PoC that could resolve it
→ Constraint statement if unresolved
```
