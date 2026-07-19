# Guarded Criterion Trajectories — Figure Sources

This file contains editable Mermaid sources for the submission manuscript.

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

## Figure 2. Guarded Criterion Update Pipeline

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

## Figure 4. P1 Direct versus Guarded Update

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

## Figure 5. Decision-space Separation

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

## Figure 6. Research Positioning

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

## Rendering Notes

For publication:

1. render each figure to SVG and PDF;
2. use consistent typography with the manuscript;
3. preserve monochrome readability;
4. ensure line and label sizes remain legible at single-column width;
5. replace Mermaid-specific styling if required by the submission venue;
6. verify that Figure 5 is supported by the selected Mermaid renderer; if not, redraw it as a conventional 2×2 matrix.
