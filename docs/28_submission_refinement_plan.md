# Guarded Criterion Trajectories — Submission Refinement Plan

## 1. Purpose

This document completes the submission-refinement portion of **Priority K: Cross-document Review, Related Work, Figures, and Submission Refinement**.

It converts the current English and Japanese working manuscripts into a controlled path toward a Jxiv-ready preprint.

Current manuscripts:

```text
paper/guarded_criterion_trajectories_full_en.md
paper/guarded_criterion_trajectories_full_jp.md
```

The current manuscripts are complete working drafts, but they should not yet be treated as submission-ready final versions.

---

## 2. Submission Position

The paper should be submitted as a **new study**, not as a revision of the foundational GyroAuth paper.

### Foundational paper

```text
GyroAuth:
Authentication as Stability-Based Selection over State Convergence
```

### Applied vulnerability paper

```text
Trajectory-Based Vulnerability Response
```

### Present paper

```text
integrity of the adaptive Authentication Criterion
and
authorization of Criterion updates
```

Recommended title:

> **Guarded Criterion Trajectories for Adaptive Authentication: Separating Current Access Decisions from Future Criterion Updates**

Japanese title:

> **適応型認証におけるGuard付きCriterion Trajectory：現在のアクセス判断と将来の認証基準更新の分離**

---

## 3. Required Manuscript Revision

### 3.1 Background and Related Work

Replace the current placeholder subsection with a structured comparison covering:

```text
NIST digital authentication guidance
adaptive and risk-based authentication
continuous authentication
behavioral biometrics
concept drift
online and data poisoning
Zero Trust
UEBA and anomaly detection
```

Use the positioning and references in:

```text
docs/26_related_work_and_positioning.md
```

Required conclusion of Related Work:

> The novelty claim is not adaptive or continuous authentication alone. The contribution is an explicit criterion-integrity model in which proposed criterion changes are represented as a guarded trajectory and authorized independently from current access decisions.

### 3.2 Introduction

The Introduction should contain:

1. legitimate need for criterion adaptation;
2. criterion adaptation as a second attack surface;
3. the current-decision/future-criterion distinction;
4. the central proposition;
5. six concise contributions;
6. a limitation sentence stating that the PoC is synthetic and structural.

Keep:

```text
dynamic criterion
!=
unconstrained self-update
```

### 3.3 Terminology

Reduce the formal terminology section to terms required by later equations and discussion.

Required terms:

```text
Access Subject
Expected Identity
Observed Evidence
Observed Access Trajectory
Authentication Relation
Authentication Criterion
Criterion Update Candidate
Criterion Trajectory
Criterion Integrity
Auth Decision
Criterion Update Response
```

Move extended definitions to an appendix if the venue length requires compression.

### 3.4 Threat Model

The submission must identify P1 as the implemented threat and distinguish it from modeled-but-unimplemented poisoning classes.

Required wording:

> The executable PoC evaluates gradual region-expansion poisoning and single-source Evidence compromise. Other poisoning classes remain within the formal threat taxonomy but are not experimentally evaluated in this paper.

### 3.5 Formal Model

Use one consistent notation set.

```text
s_t         Access Subject reference
A_t         effective Authentication Criterion
A*_(t+1)    Criterion Update Candidate
Q_t         Criterion State
G_t         Guard vector
D_auth_t    Auth Decision
D_crit_t    Criterion Update Response
T_t^obs     Observed Access Trajectory
```

Do not reuse `A` for Access Subject.

### 3.6 Non-compensation rule

Make the non-compensation rule prominent:

```text
CriticalGuardFail
→
D_crit_t != ACCEPT
```

Explain that a scalar Criterion Integrity summary is not authoritative.

### 3.7 PoC

State clearly that Model U is an intentionally unsafe control baseline and not a claim about every existing adaptive-authentication system.

The PoC section must include:

```text
same initial criterion
same scenario inputs
same candidate generator
different adoption policy
```

### 3.8 Results

Insert:

```text
Figure 4 P1 Direct vs Guarded Comparison
Table 2 PoC Result Summary
```

Use exact values from the committed result artifact.

The most important qualitative result is:

```text
AUTH_STABLE + FREEZE
```

### 3.9 Security Claims

Replace broad prose with a three-level table:

```text
Structurally demonstrated
Conditional
Unsupported
```

Do not use “prevents criterion poisoning” without scenario and assumption qualifiers.

### 3.10 Limitations

Retain all current limitations and add:

```text
no sensitivity analysis
no rollback execution result
no multidimensional criterion
no real telemetry
no comparative benchmark against deployed products
```

---

## 4. Recommended Final Paper Structure

```text
1. Introduction
2. Background and Related Work
3. Terminology and Scope
4. Threat Model
5. Guarded Criterion Trajectory Model
6. Criterion Update State Machine
7. PoC Design
8. Results
9. Discussion
10. Security Claims and Limitations
11. Future Work
12. Conclusion
References
AI-Assisted Tools Disclosure
Appendix A: Extended Definitions
Appendix B: Reproducibility
```

The current manuscript structure is compatible with this plan. The principal change is replacing the Related Work placeholder and adding figures, tables, references, and appendices.

---

## 5. Abstract Refinement

Recommended English abstract structure:

```text
Problem
Adaptive criteria are necessary but create a poisoning surface.

Gap
Current authentication and permission to change future criteria are insufficiently separated.

Method
Criterion Update Candidate + Guard + separate Criterion Update Response.

Evaluation
Deterministic comparison under N1, P1, and C1.

Result
Supported adaptation accepted; unsafe expansion frozen; compromised-source update blocked.

Boundary
Structural PoC, not production security validation.
```

Recommended closing sentence:

> The results demonstrate an executable separation between accepting the current authentication relation and authorizing observations to redefine future authentication criteria, under the declared synthetic assumptions.

The Japanese abstract should preserve the same six-part logic and all qualifiers.

---

## 6. Figure and Table Integration

Source specifications:

```text
docs/27_figures_and_captions.md
```

Minimum set:

```text
Figure 1 Dual Evaluation Architecture
Figure 2 Guarded Criterion Update Pipeline
Figure 3 Criterion Update State Machine
Figure 4 P1 Direct vs Guarded Comparison
Table 1 Decision Sets
Table 2 PoC Result Summary
Table 3 Claim Boundary
```

Optional:

```text
Figure 5 Decision-space Separation
Figure 6 Research Positioning
```

All diagrams should be rendered as vector graphics.

---

## 7. Reference Integration

Initial numbered references are provided in:

```text
docs/26_related_work_and_positioning.md
```

Before submission:

1. verify exact publisher metadata;
2. replace provisional arXiv references if peer-reviewed final versions exist;
3. verify page ranges and DOI capitalization;
4. use one citation style in both manuscripts;
5. keep English and Japanese reference numbering identical;
6. cite the foundational GyroAuth and vulnerability-response papers explicitly;
7. avoid citing non-primary product marketing as evidence of novelty.

---

## 8. Reproducibility Appendix

Add an appendix containing:

```text
Repository: gitGyro-Dev/gyroauth
Script: scripts/simulate_guarded_criterion_update.py
Scenario input: examples/criterion_update/scenarios.json
Recorded summary: results/criterion_update_summary.json
Runtime dependency: Python standard library
Input type: deterministic synthetic stages
```

Execution command:

```bash
python scripts/simulate_guarded_criterion_update.py \
  --scenarios examples/criterion_update/scenarios.json \
  --output results/criterion_update_results.json
```

State that the full output is generated locally and the committed summary records the verified result used in the manuscript.

---

## 9. Submission Metadata Checklist

```text
[ ] Final English title
[ ] Final Japanese title
[ ] Author name and affiliation
[ ] Corresponding email
[ ] ORCID, if used
[ ] Abstract within venue limits
[ ] Keywords
[ ] English manuscript PDF
[ ] Japanese manuscript PDF
[ ] Figure legibility
[ ] Reference verification
[ ] DOI verification
[ ] AI-assisted tools disclosure
[ ] Code and data availability statement
[ ] Conflict-of-interest statement, if required
[ ] Funding statement, if required
[ ] License selection
[ ] Jxiv category selection
[ ] English/Japanese relation stated correctly
```

---

## 10. Code and Data Availability Statement

Recommended wording:

> The deterministic proof-of-concept implementation, synthetic scenario definitions, and recorded result summary are available in the public GyroAuth repository. The study does not use personal authentication data or external production telemetry.

Japanese:

> 決定論的PoC実装、Syntheticシナリオ定義、および記録済み結果サマリーは、公開GyroAuthリポジトリで提供する。本研究は個人の認証データまたは外部の本番Telemetryを使用していない。

---

## 11. AI-Assisted Tools Disclosure

Current disclosure is suitable in principle.

Recommended English wording:

> AI-assisted tools were used for structural organization, drafting support, language refinement, and consistency checking. The author reviewed and edited the technical content, equations, claims, references, and final manuscript and assumes full responsibility for the work.

Recommended Japanese wording:

> 本稿の作成にあたり、構成整理、草稿作成補助、表現調整、言語調整、および整合性確認のためにAI支援ツールを使用した。技術内容、数式、主張、参考文献、および最終原稿は著者が確認・編集し、本稿に対する全責任を負う。

---

## 12. Final Claim Language

### Preferred

```text
under the implemented deterministic assumptions
in the evaluated P1 scenario
structurally demonstrates
supports the separation of
can freeze adaptation before the configured attack reference becomes admissible
```

### Avoid

```text
prevents all criterion poisoning
detects every attacker
guarantees identity
eliminates false acceptance
eliminates false rejection
proves production security
```

---

## 13. Remaining Work after Priority K

Priority K produces the review, literature positioning, figure source, and submission plan. The following execution work remains:

```text
Priority L1  Integrate Related Work into both manuscripts
Priority L2  Render and insert figures
Priority L3  Add numbered references and in-text citations
Priority L4  Perform English/Japanese paragraph-level synchronization
Priority L5  Generate submission PDFs
Priority L6  Conduct final consistency and formatting review
Priority L7  Prepare Jxiv metadata and submit
```

A separate Priority L is recommended because final manuscript replacement, figure rendering, PDF generation, and submission metadata are execution tasks rather than conceptual design tasks.

---

## 14. Priority K Completion Status

```text
Cross-document Review: complete
Related Work and Positioning: complete as review draft
Figure specifications: complete
Submission refinement plan: complete
Final manuscript integration: pending Priority L
PDF generation: pending Priority L
Jxiv submission: pending
```

The research package is now ready to move from manuscript development to final integration and publication preparation.
