# GyroAuth PoC Workspace

This directory defines PoC candidates, scope, evidence, metrics, constraints, and transition conditions.

## Initial PoC Priority

The preferred first PoC is an **offline log evaluation**.

Reasons:

- it does not change the production authentication path;
- customer risk is comparatively low;
- existing decisions can be compared with GyroAuth outputs;
- required data can be clarified before integration;
- the result can expose both technical value and operational burden;
- it can progress later to Shadow Mode.

## Candidate Sequence

1. Offline log evaluation
2. Customer-specific synthetic scenario
3. Shadow Mode evaluation
4. Limited step-up authentication integration
5. Criterion Update Guard integration

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
