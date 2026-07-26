# GyroAuth v2.1.0 — Guarded Criterion Trajectories and Research Demo

## Summary

GyroAuth v2.1.0 adds the guarded criterion-update research track, deterministic proof-of-concept scenarios, publication artifacts, and a minimal GitHub Pages research demo.

This release preserves the foundational definition:

```text
Authentication = Stability-based Selection over State Convergence
```

and makes the following distinctions explicit:

```text
Subject Evaluation
!=
Criterion Integrity Evaluation

Auth Decision
!=
Criterion Update Response

Criterion Update Candidate
!=
Accepted Criterion
```

A central executable combination is:

```text
AUTH_STABLE + FREEZE
```

The current authentication relation may continue while adaptation of the future authentication criterion is blocked.

## Highlights

### Guarded Criterion Trajectories

- Introduces Criterion Integrity Evaluation as a separate application-layer decision process.
- Represents authentication-criterion change as a guarded, traceable trajectory.
- Adds Criterion Update Responses:
  - `ACCEPT`
  - `DEFER`
  - `FREEZE`
  - `REVIEW`
  - `ROLLBACK`
- Preserves the position:

```text
dynamic criterion
!=
unconstrained self-update
```

### Deterministic PoC

The release includes three fixed scenarios:

- **N1 — Legitimate New Device Transition**
  - `REAUTH_REQUIRED → AUTH_STABLE → AUTH_STABLE`
  - `DEFER → ACCEPT → ACCEPT`

- **P1 — Gradual Region Expansion Poisoning**
  - direct adoption expands the criterion until the attack reference becomes admissible;
  - guarded adoption produces `DEFER → FREEZE → FREEZE` and preserves the trusted criterion;
  - Stage 2 demonstrates `AUTH_STABLE + FREEZE`.

- **C1 — Single Evidence Source Compromise**
  - apparently strong evidence does not override insufficient source integrity and weak cross-evidence consistency;
  - the guarded response remains `FREEZE`.

Relevant artifacts:

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

### Publication Artifacts

- English and Japanese Guarded Criterion Trajectories manuscripts.
- Canonically numbered figures 1–6.
- Automated PDF generation, A4/size/text/image checks, and repository commit workflow.
- English manuscript submitted to Jxiv and currently under review.
- Japanese manuscript prepared as a submission candidate.

Publication files:

```text
publications/guarded_criterion_trajectories/jxiv_submission/
├── guarded_criterion_trajectories_en.pdf
└── guarded_criterion_trajectories_jp.pdf
```

### GitHub Pages Research Demo

A static research demo is available at:

https://gitgyro-dev.github.io/gyroauth/

The demo provides:

- N1 / P1 / C1 scenario selection;
- stage-by-stage Auth Decision and Criterion Update Response;
- current criterion center and width;
- attack-reference admissibility;
- direct-versus-guarded comparison;
- explicit visualization of `AUTH_STABLE + FREEZE`.

The demo uses HTML, CSS, Vanilla JavaScript, and static data only. It does not use an external API, backend service, production credentials, or real authentication telemetry.

## Scope and Non-Guarantees

This release is a deterministic research implementation.

It is not:

- a production authentication service;
- a universal criterion-poisoning detector;
- a guarantee of zero false accepts or false rejects;
- a replacement for passwords, passkeys, MFA, authenticators, or assurance frameworks;
- a redefinition of Gyro Logic or the GyroOS runtime contract.

## Layer Consistency

```text
Gyro Logic = Theory
GyroOS     = Execution System
GyroAuth   = Authentication Application
```

- Gyro Logic Core remains unchanged.
- GyroOS runtime responsibilities remain unchanged.
- This release extends only the GyroAuth application layer with criterion-integrity evaluation, research artifacts, and visualization.

## Links

- Live Demo: https://gitgyro-dev.github.io/gyroauth/
- Repository: https://github.com/gitGyro-Dev/gyroauth
- Previous Release: https://github.com/gitGyro-Dev/gyroauth/releases/tag/v2.0.0
- GyroAuth English paper: https://doi.org/10.51094/jxiv.4600
- GyroAuth Japanese paper: https://doi.org/10.51094/jxiv.5341
- Trajectory-Based Vulnerability Response: https://doi.org/10.51094/jxiv.5416
- Japanese vulnerability-response paper: https://doi.org/10.51094/jxiv.5440
