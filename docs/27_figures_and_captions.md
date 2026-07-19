# Guarded Criterion Trajectories — Figures and Captions

## 1. Purpose

This document defines the canonical figure sequence for the English and Japanese submission manuscripts.

The following elements must use the same number:

- figure heading in `figures/guarded_criterion_trajectories_mermaid.md`;
- rendered filenames `figure_N.svg`, `figure_N.png`, and `figure_N.pdf`;
- caption and identifier inserted into the manuscript;
- figure number assigned in the generated publication PDF;
- figure references in review and publication documents.

The canonical order is the order of appearance in the manuscript.

---

## 2. Canonical Publication Order

| Figure | Title | Manuscript placement |
|---:|---|---|
| 1 | Dual Evaluation Architecture | End of Introduction |
| 2 | Research Positioning | End of Background and Related Work |
| 3 | Guarded Criterion Update Pipeline | End of Formal Security Model |
| 4 | Criterion Update State Machine | End of Criterion Update State Machine section |
| 5 | P1 Direct versus Guarded Update | Results, after the P1 comparison |
| 6 | Decision-space Separation | End of Discussion |

This order is authoritative for source numbering, generated artifact filenames, captions, and PDF numbering.

---

## Figure 1. Dual Evaluation Architecture

```mermaid
flowchart LR
    E[Observed Evidence] --> T[Observed Access Trajectory]
    T --> S[Subject Evaluation]
    T --> C[Criterion Integrity Evaluation]
    A[Effective Authentication Criterion] --> S
    A --> C
    S --> D1[Auth Decision]
    C --> D2[Criterion Update Response]
    D1 --> O1[AUTH_STABLE / RECONVERGING / REAUTH_REQUIRED / AUTH_FAIL]
    D2 --> O2[ACCEPT / DEFER / FREEZE / REVIEW / ROLLBACK]
```

**Caption:** GyroAuth evaluates the current Authentication Relation and the integrity of the criterion used for future evaluation as separate but related processes.

**Required textual reference:** Figure 1 shows that the current authentication relation and permission to modify the future criterion are evaluated through separate decision streams.

---

## Figure 2. Research Positioning

```mermaid
flowchart LR
    AA[Adaptive / Risk-Based Authentication] --> P[Guarded Criterion Trajectories]
    CA[Continuous Authentication] --> P
    CD[Concept Drift] --> P
    DP[Data Poisoning / Adversarial ML] --> P
    ZT[Zero Trust Context] --> P
    P --> X[Independent Authorization of Future Criterion Change]
```

**Caption:** The proposal is positioned at the intersection of adaptive authentication, continuous authentication, drift handling, and poisoning-aware adaptation.

---

## Figure 3. Guarded Criterion Update Pipeline

```mermaid
flowchart LR
    O[Observation / Context / History] --> U[Candidate Generator U]
    U --> C[Criterion Update Candidate]
    C --> G[Guard Vector]
    G --> R{Criterion Update Response}
    R -->|ACCEPT| N[Adopt Candidate]
    R -->|DEFER| K[Keep Current Criterion]
    R -->|FREEZE| F[Suspend Adaptive Adoption]
    R -->|REVIEW| V[External or Stronger Review]
    R -->|ROLLBACK| B[Restore Verified Prior Criterion]
```

**Caption:** Candidate generation and candidate adoption are separated. Only `ACCEPT` makes the candidate effective.

---

## Figure 4. Criterion Update State Machine

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
    UNCERTAIN --> ADAPTING: supported candidate
    UNCERTAIN --> UNDER_REVIEW: REVIEW
    FROZEN --> UNDER_REVIEW: REVIEW
    FROZEN --> ROLLED_BACK: ROLLBACK
    COMPROMISED --> ROLLED_BACK: ROLLBACK
    UNDER_REVIEW --> STABLE: externally validated
    UNDER_REVIEW --> COMPROMISED: contamination confirmed
    ROLLED_BACK --> STABLE: validated operation
```

**Caption:** Criterion States and Criterion Update Responses are distinct. `FREEZE` stops adaptation without necessarily terminating Subject Evaluation.

---

## Figure 5. P1 Direct versus Guarded Update

```mermaid
flowchart TB
    I[Same Initial Criterion and Same Observations]
    I --> U[Model U: Direct Adoption]
    I --> G[Model G: Guarded Adoption]
    U --> U1[Repeated Candidate Adoption]
    U1 --> U2[Center Drift and Width Expansion]
    U2 --> U3[Attack Reference Becomes Admissible]
    G --> G1[DEFER]
    G1 --> G2[FREEZE at Stage 2]
    G2 --> G3[Trusted Criterion Preserved]
    G3 --> G4[Attack Reference Remains Non-admissible]
```

**Caption:** Under the implemented P1 scenario, direct adoption expanded the criterion until the attack reference became admissible, while guarded adoption froze adaptation before admission.

**Claim boundary:** This figure represents the implemented deterministic P1 scenario. It does not establish universal poisoning prevention.

---

## Figure 6. Decision-space Separation

```mermaid
quadrantChart
    title Auth Decision and Criterion Update Response are independent
    x-axis Criterion update blocked --> Criterion update allowed
    y-axis Current relation rejected --> Current relation accepted
    quadrant-1 AUTH_STABLE + ACCEPT
    quadrant-2 AUTH_STABLE + FREEZE
    quadrant-3 AUTH_FAIL + ROLLBACK
    quadrant-4 AUTH_FAIL + ACCEPT is invalid
```

**Caption:** `AUTH_STABLE + FREEZE` represents temporary continuation of the current Authentication Relation while prohibiting criterion adaptation.

**Rendering note:** If the selected Mermaid renderer does not support `quadrantChart`, redraw Figure 6 as a conventional 2×2 matrix without changing its meaning.

---

## 3. Decision and Result Tables

### Table 1. Decision Sets

| Decision space | Values | Evaluated object |
|---|---|---|
| Auth Decision | `AUTH_STABLE`, `RECONVERGING`, `REAUTH_REQUIRED`, `AUTH_FAIL` | current Authentication Relation |
| Criterion Update Response | `ACCEPT`, `DEFER`, `FREEZE`, `REVIEW`, `ROLLBACK` | proposed change to future Authentication Criterion |

### Table 2. PoC Result Summary

| Scenario | Model | Final center | Final width | Freeze stage | Attack reference admissible | Final criterion state |
|---|---:|---:|---:|---:|---:|---|
| N1 | U | 0.24808 | 0.120000 | — | No | ADAPTING |
| N1 | G | 0.23400 | 0.120000 | — | No | STABLE |
| P1 | U | 0.3969728 | 0.277212 | — | Yes | ADAPTING |
| P1 | G | 0.20000 | 0.120000 | 2 | No | FROZEN |
| C1 | U | 0.23280 | 0.120000 | — | No | ADAPTING |
| C1 | G | 0.20000 | 0.120000 | 1 | No | FROZEN |

### Table 3. Claim Boundary

| Claim class | Examples |
|---|---|
| Structurally demonstrated | candidate/adoption separation; decision-stream separation; bounded supported adaptation; P1 freeze before configured attack-reference admission; C1 update blocking; `AUTH_STABLE + FREEZE` |
| Conditional | broader poisoning containment; rollback-supported recovery; credential-theft resistance; session-hijacking or relay detection |
| Unsupported | universal attack detection; complete poisoning prevention; zero false accepts/rejects; perfect identity proof; production performance; privacy guarantees |

---

## 4. Rendering and Publication Rules

1. Render each figure as SVG, PNG, and PDF.
2. Use filenames `figure_1` through `figure_6` according to the canonical publication order.
3. Insert figures in numeric order so that Pandoc's automatic numbering matches the source number.
4. Use the same formal labels in the English and Japanese editions; translate captions and surrounding prose only.
5. Preserve state identifiers and Criterion Update Responses exactly.
6. Verify arrows, labels, and captions in monochrome printing.
7. Do not imply quantitative performance from conceptual diagrams.
8. Regenerate or verify PoC values against the committed result artifact before submission.
9. Treat any mismatch among source heading, filename, caption, insertion order, and PDF number as a publication-blocking error.
