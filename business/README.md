# GyroAuth Business / PoC

This directory is the working area for the practical application, commercialization, collaborative research, and proof-of-concept development of GyroAuth.

このディレクトリは、GyroAuthの実用化、事業化、共同研究、PoC獲得を検討・管理するための作業領域です。

## Purpose

The objective is to move GyroAuth beyond a research result and determine whether it can become:

- a company PoC or collaborative research project;
- an evaluation component for authentication and access logs;
- a guarded update layer for adaptive authentication or UEBA;
- an integration or licensing opportunity for security vendors;
- a consulting, implementation-support, or technical evaluation service.

The central commercialization sequence is:

```text
Can a third party understand it?
→ Would they want to try it?
→ Can the adoption value be explained?
→ Can it be executed as a PoC or joint research project?
→ Can it lead to continued use, a contract, or a business?
```

## Repository Policy

For the initial phase, business materials remain in this repository under `business/`.

Keeping the research implementation and business workspace together has practical advantages:

- technical claims can be traced directly to executable artifacts;
- PoC documents can reference current scenarios and releases;
- duplicate maintenance across repositories is avoided;
- the boundary between demonstrated capability and commercial hypothesis remains reviewable.

A separate repository should be considered only when one or more of the following become true:

- customer-confidential materials must be isolated;
- commercial code has a different license or access policy;
- the business artifacts develop an independent release cycle;
- external collaborators require restricted access;
- product operations become materially separate from the research repository.

## Layer Boundary

The following project boundary must not be changed for business convenience:

```text
Gyro Logic          = Theory
GyroOS              = Execution System
GyroAuth            = Authentication Application
Gyro Project Cycle  = Management / Integration / Visualization
Gyro Developer Toolkit = Automation / Validation / Operation Support
```

Immutable Gyro Logic core:

```text
Structure → Slice → Stability
```

Business documents must not:

- redefine Gyro Logic;
- change the GyroOS runtime contract independently;
- present a PoC result as a general security guarantee;
- describe the current demo as a production authentication service;
- merge `Auth Decision` with `Criterion Update Response`;
- treat a `Criterion Update Candidate` as an automatically accepted criterion.

## Current Commercialization Position

GyroAuth currently has:

- a defined stability-based authentication model;
- four Auth Decision states;
- guarded criterion-update states;
- deterministic scenarios for legitimate change, gradual poisoning, and evidence-source compromise;
- a public GitHub Pages research demo;
- reproducible research artifacts and publications.

GyroAuth does not yet have validated production performance, real-environment error rates, enterprise integrations, a production API, SLA, commercial support, or regulatory assurance.

Therefore, the initial offer should not be a production authentication service. The preferred entry point is an offline evaluation or Shadow Mode PoC using authentication and access logs.

## Directory Structure

```text
business/
├── README.md
├── strategy/
│   ├── positioning.md
│   ├── roadmap.md
│   └── repository_split_criteria.md
├── poc/
│   ├── README.md
│   ├── offline_log_evaluation.md
│   └── evaluation_framework.md
├── deliverables/
│   └── README.md
└── logs/
    └── README.md
```

## Initial Priorities

1. Define one-sentence positioning for each target audience.
2. Rank the first three market and use-case candidates.
3. Select one primary PoC.
4. Prepare a one-page company-facing technical overview.
5. Improve the public demo so it connects research understanding to a PoC inquiry.

## Source of Truth

Technical definitions and executable behavior remain in the existing GyroAuth research and implementation files. Business materials describe customer value, validation plans, constraints, and delivery models; they do not replace technical specifications.
