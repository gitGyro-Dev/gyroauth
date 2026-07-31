# GyroAuth PoC Workspace

This directory defines PoC packages, scope, evidence, metrics, constraints, and transition conditions.

## First Concrete PoC

The first concrete GyroAuth PoC package is:

- [`privileged_access_poc_package.md`](privileged_access_poc_package.md)

The selected position is:

```text
Privileged Access
+ offline log evaluation
+ optional Shadow Mode
+ no production enforcement
```

The package evaluates whether privileged-session trajectories can be reconstructed from existing logs and whether GyroAuth can independently produce:

```text
Auth Decision
!=
Criterion Update Response
```

The primary demonstrable state is:

```text
AUTH_STABLE + FREEZE
```

A privileged session may remain operational while uncertain behavior is prevented from silently expanding the future accepted baseline.

## Why Privileged Access Comes First

Privileged access provides a narrower and more controllable initial boundary than VPN / ZTNA.

The first scope can be limited to:

- 5 to 10 privileged users;
- one bounded system or service;
- 2 to 4 weeks of events;
- 2 to 4 log sources;
- offline analysis only.

VPN / ZTNA remains the second validation package because it may require broader treatment of identity, endpoint posture, physical or network context, routing, proxies, location, and session conditions.

## PoC Development Sequence

1. Privileged-access offline log evaluation
2. Privileged-access Shadow Mode
3. Limited integration design for review or step-up authentication
4. VPN / ZTNA validation package
5. AI Agent governance exploratory package

No transition to production enforcement occurs automatically between these stages.

## Supporting Documents

- [`offline_log_evaluation.md`](offline_log_evaluation.md) — general offline-evaluation model
- [`evaluation_framework.md`](evaluation_framework.md) — common evaluation principles and evidence framework
- [`privileged_access_poc_package.md`](privileged_access_poc_package.md) — first customer-facing PoC package

## Required PoC Definition

Every PoC document must define:

- target customer and problem;
- current alternative or control;
- objective and hypothesis;
- required data and data constraints;
- architecture and execution method;
- GyroAuth outputs;
- evaluation metrics;
- success and stop criteria;
- non-targets;
- operational and security risks;
- deliverables;
- transition path after the PoC.

## Mandatory Claim Boundary

```text
PoC result != general security guarantee
```

The evaluation must distinguish deterministic scenario behavior, synthetic-data results, and real-environment evidence.

The initial package must also maintain:

```text
Existing customer controls remain authoritative.
GyroAuth outputs are analytical findings and review recommendations.
```
