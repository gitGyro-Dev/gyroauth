# Guarded Criterion Trajectories — Figures and Captions

## 1. Purpose

This document completes the figure-design portion of **Priority K: Cross-document Review, Related Work, Figures, and Submission Refinement**.

The figures are specified as Mermaid-compatible source diagrams so that they can be rendered later into SVG or PDF without changing the model.

The final manuscript should include at least Figures 1–4. Figures 5–6 are recommended.

---

## Figure 1. Dual Evaluation Architecture

```mermaid
flowchart LR
    E[Observed Evidence] --> T[Observed Access Trajectory]
    T --> SE[Subject Evaluation]
    SE --> AD[Auth Decision]

    T --> UC[Criterion Update Candidate]
    A[Effective Authentication Criterion] --> SE
    A --> UC
    UC --> G[Guard]
    G --> CI[Criterion Integrity Evaluation]
    CI --> CR[Criterion Update Response]
    CR --> NT[Next Effective Criterion]
    NT --> A

    AD -. separate decision stream .- CR
```

**Caption:** Dual GyroAuth evaluation architecture. Subject Evaluation selects the current Auth Decision, while Criterion Integrity Evaluation independently selects whether a proposed criterion change is accepted, deferred, frozen, reviewed, or rolled back. The two decision streams are related but not interchangeable.

**Manuscript placement:** End of Introduction or beginning of Formal Security Model.

**Required textual reference:**

> Figure 1 shows that the current authentication relation and the permission to modify the future criterion are evaluated through separate decision streams.

---

## Figure 2. Guarded Criterion Update Pipeline

```mermaid
flowchart TD
    O[Observation at stage t] --> U[Candidate generator U]
    U --> C[Candidate A* t+1]
    C --> GV[Guard vector]

    GV --> P{Critical guard failure?}
    P -- Yes --> X[ACCEPT prohibited]
    X --> S1[DEFER / FREEZE / REVIEW / ROLLBACK]

    P -- No --> S{Evidence sufficient and update bounded?}
    S -- Yes --> A[ACCEPT]
    S -- No --> D[DEFER or REVIEW]

    A --> N1[A t+1 = A* t+1]
    D --> N2[A t+1 = A t]
    S1 --> N3[Preserve or restore trusted criterion]
```

**Caption:** Guarded criterion-update pipeline. Candidate generation does not imply adoption. Critical Guard failures are non-compensable and prevent `ACCEPT`, even when other evidence appears favorable.

**Manuscript placement:** Formal Security Model, immediately after the candidate, Guard, and transition equations.

---

## Figure 3. Criterion Update State Machine

```mermaid
stateDiagram-v2
    [*] --> STABLE

    STABLE --> ADAPTING: ACCEPT
    STABLE --> UNCERTAIN: DEFER
    STABLE --> FROZEN: FREEZE
    STABLE --> UNDER_REVIEW: REVIEW

    ADAPTING --> STABLE: validated ACCEPT
    ADAPTING --> UNCERTAIN: DEFER
    ADAPTING --> FROZEN: FREEZE
    ADAPTING --> UNDER_REVIEW: REVIEW

    UNCERTAIN --> ADAPTING: supported ACCEPT
    UNCERTAIN --> FROZEN: repeated unsafe drift
    UNCERTAIN --> UNDER_REVIEW: unresolved REVIEW

    FROZEN --> UNDER_REVIEW: REVIEW
    FROZEN --> ROLLED_BACK: verified ROLLBACK
    FROZEN --> STABLE: validated release

    UNDER_REVIEW --> STABLE: external validation
    UNDER_REVIEW --> ROLLED_BACK: verified ROLLBACK
    UNDER_REVIEW --> COMPROMISED: contamination confirmed

    COMPROMISED --> ROLLED_BACK: verified ROLLBACK
    ROLLED_BACK --> STABLE: validated operation
```

**Caption:** Criterion Update State Machine. Criterion States are distinct from Criterion Update Responses. `DEFER` concerns insufficient support for a candidate, `FREEZE` suspends the adaptive update path, `REVIEW` transfers the decision path, and `ROLLBACK` restores a verified prior criterion.

**Manuscript placement:** Criterion Update State Machine section.

---

## Figure 4. P1 Comparison: Direct vs Guarded Adoption

```mermaid
flowchart LR
    subgraph U[Model U: Direct Adoption]
        U1[Small deviation 1] --> U2[Direct adoption]
        U2 --> U3[Small deviation 2]
        U3 --> U4[Direct adoption]
        U4 --> U5[Cumulative center shift and width expansion]
        U5 --> U6[Attack reference becomes admissible]
    end

    subgraph G[Model G: Guarded Adoption]
        G1[Small deviation 1] --> G2[DEFER]
        G2 --> G3[Repeated unexplained drift]
        G3 --> G4[FREEZE]
        G4 --> G5[Trusted criterion preserved]
        G5 --> G6[Attack reference remains non-admissible]
    end
```

**Caption:** P1 gradual region-expansion comparison. The direct-update baseline repeatedly adopts candidates and expands until the configured attack reference becomes admissible. The guarded model defers and then freezes adaptation, preserving the trusted criterion under the implemented deterministic assumptions.

**Manuscript placement:** Results section before or after the P1 result table.

---

## Figure 5. Decision-space Separation

```mermaid
quadrantChart
    title Auth Decision and Criterion Update Response are independent
    x-axis Current relation less continuable --> Current relation more continuable
    y-axis Criterion update less admissible --> Criterion update more admissible
    quadrant-1 AUTH_STABLE + ACCEPT
    quadrant-2 REAUTH_REQUIRED + ACCEPT or DEFER
    quadrant-3 AUTH_FAIL + ROLLBACK
    quadrant-4 AUTH_STABLE + FREEZE
```

**Caption:** Conceptual separation of current Authentication Relation evaluation and criterion-update admissibility. `AUTH_STABLE + FREEZE` occupies the case in which the current relation may continue while observations are prohibited from redefining future acceptance.

**Manuscript placement:** Discussion section.

**Rendering note:** If the target Mermaid renderer does not support `quadrantChart`, replace this with a manually drawn 2×2 matrix.

---

## Figure 6. Research Positioning

```mermaid
flowchart TB
    AA[Adaptive / Risk-Based Authentication] --> GCT[Guarded Criterion Trajectories]
    CA[Continuous Authentication] --> GCT
    BB[Behavioral Biometrics] --> GCT
    CD[Concept Drift] --> GCT
    DP[Data Poisoning / Adversarial ML] --> GCT
    ZT[Zero Trust] --> GCT
    UEBA[UEBA / Anomaly Detection] --> GCT

    GCT --> P[Criterion change is proposed, evaluated, and authorized separately]
```

**Caption:** Research positioning. The proposed model draws from adaptive and continuous authentication, concept-drift adaptation, and poisoning-aware learning, while focusing specifically on the integrity and authorization of authentication-criterion change.

**Manuscript placement:** Background and Related Work section.

---

## Table 1. Decision Sets

| Decision space | Values | Evaluated object |
|---|---|---|
| Auth Decision | `AUTH_STABLE`, `RECONVERGING`, `REAUTH_REQUIRED`, `AUTH_FAIL` | current Authentication Relation |
| Criterion Update Response | `ACCEPT`, `DEFER`, `FREEZE`, `REVIEW`, `ROLLBACK` | proposed change to future Authentication Criterion |

**Caption:** Separate decision spaces for current authentication and criterion adaptation.

---

## Table 2. PoC Result Summary

| Scenario | Model | Final center | Final width | Freeze stage | Attack reference admissible | Final criterion state |
|---|---:|---:|---:|---:|---:|---|
| N1 | U | 0.24808 | 0.120000 | — | No | ADAPTING |
| N1 | G | 0.23400 | 0.120000 | — | No | STABLE |
| P1 | U | 0.3969728 | 0.277212 | — | Yes | ADAPTING |
| P1 | G | 0.20000 | 0.120000 | 2 | No | FROZEN |
| C1 | U | 0.23280 | 0.120000 | — | No | ADAPTING |
| C1 | G | 0.20000 | 0.120000 | 1 | No | FROZEN |

**Caption:** Deterministic PoC results. Model U directly adopts candidates. Model G applies Guard evaluation and Criterion Update Responses.

---

## Table 3. Claim Boundary

| Claim class | Examples |
|---|---|
| Structurally demonstrated | candidate/adoption separation; decision-stream separation; supported bounded adaptation; P1 freeze before configured attack-reference admission; C1 update blocking; `AUTH_STABLE + FREEZE` |
| Conditional | broader poisoning containment; rollback-supported recovery; credential-theft resistance; session-hijacking or relay detection |
| Unsupported | universal attack detection; complete poisoning prevention; zero false accepts/rejects; perfect identity proof; production performance; privacy guarantees |

**Caption:** Security claim boundary for the current structural PoC.

---

## Rendering and Publication Rules

1. Render diagrams as vector graphics, preferably SVG for repository use and PDF for submission.
2. Do not use screenshots of Mermaid source in the paper.
3. Use the same labels in English and Japanese editions; translate captions and prose only.
4. Keep state identifiers and responses unchanged.
5. Verify that arrows and line breaks remain readable in monochrome printing.
6. Do not imply quantitative performance from conceptual diagrams.
7. Figure 4 must state that the result is scenario-specific and deterministic.
8. Table 2 values must be regenerated or verified from the committed result artifact before final submission.

## Minimum Figure Set for Submission

```text
Figure 1 Dual Evaluation Architecture
Figure 2 Guarded Criterion Update Pipeline
Figure 3 Criterion Update State Machine
Figure 4 P1 Direct vs Guarded Comparison
Table 1 Decision Sets
Table 2 PoC Result Summary
Table 3 Claim Boundary
```
