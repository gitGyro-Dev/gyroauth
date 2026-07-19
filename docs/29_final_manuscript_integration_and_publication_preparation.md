# Final Manuscript Integration and Publication Preparation

## 1. Purpose

This document completes **Priority L: Final Manuscript Integration and Publication Preparation** for the Guarded Criterion Trajectories study.

It integrates the outputs of Priorities A–K into publication-oriented English and Japanese manuscript candidates and fixes the remaining work required before jxiv submission.

## 2. Integrated Artifacts

The following publication artifacts were added:

```text
paper/guarded_criterion_trajectories_submission_en.md
paper/guarded_criterion_trajectories_submission_jp.md
paper/guarded_criterion_trajectories_submission_metadata.md
figures/guarded_criterion_trajectories_mermaid.md
```

The submission candidates build on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
docs/18_formal_security_model.md
docs/19_criterion_update_state_machine.md
docs/20_normal_and_poisoned_update_scenarios.md
docs/21_minimal_simulation_design.md
docs/22_poc_implementation_and_results.md
docs/23_security_claims_and_limitations.md
docs/24_paper_outline.md
docs/25_cross_document_review.md
docs/26_related_work_and_positioning.md
docs/27_figures_and_captions.md
docs/28_submission_refinement_plan.md
```

## 3. Integration Decisions

### 3.1 New submission candidates

The existing working manuscripts were preserved.

New publication-oriented files were created rather than silently replacing the earlier working drafts:

```text
working draft
→ retained for traceability

submission candidate
→ integrated Related Work, references, reproducibility, and publication statements
```

### 3.2 Central proposition

The manuscript remains centered on:

```text
dynamic criterion
!=
unconstrained self-update
```

### 3.3 Decision separation

The final manuscript preserves:

```text
Subject Evaluation
!=
Criterion Integrity Evaluation
```

```text
Auth Decision
!=
Criterion Update Response
```

```text
Criterion Update Candidate
!=
Accepted Criterion
```

### 3.4 Executable focal result

The principal explanatory result remains:

```text
AUTH_STABLE + FREEZE
```

Interpretation:

```text
the current Authentication Relation may remain temporarily continuable
while
permission to modify the future Authentication Criterion is suspended
```

### 3.5 Notation policy

The submission candidates use:

```text
s_t = Access Subject reference
A_t = effective Authentication Criterion
A*_(t+1) = Criterion Update Candidate
D_auth_t = Auth Decision
D_crit_t = Criterion Update Response
```

This avoids using `A` for both Access Subject and Authentication Criterion.

## 4. Related Work Integration

The final manuscripts now position the proposal against:

```text
digital authentication guidance
Zero Trust
continuous authentication
behavioral biometrics
concept drift
poisoning and adversarial machine learning
previous GyroAuth publications
```

The novelty statement is intentionally bounded:

> This study does not claim novelty in adaptive or continuous authentication alone. Its contribution is an explicit criterion-integrity model in which proposed authentication-criterion changes form a guarded, traceable trajectory and are authorized independently from current access decisions.

The manuscripts use the verified first-submission reference subset from `docs/26_related_work_and_positioning.md`.

Provisional references whose metadata still requires publisher verification were excluded from the integrated submission candidates.

## 5. Figures

Editable Mermaid sources were added for:

```text
Figure 1  Dual Evaluation Architecture
Figure 2  Guarded Criterion Update Pipeline
Figure 3  Criterion Update State Machine
Figure 4  P1 Direct versus Guarded Update
Figure 5  Decision-space Separation
Figure 6  Research Positioning
```

The figure source file is:

```text
figures/guarded_criterion_trajectories_mermaid.md
```

These are source specifications, not final publication graphics.

Before submission they must be rendered and visually inspected as SVG/PDF.

## 6. Reproducibility Integration

The manuscripts include the execution command:

```bash
python scripts/simulate_guarded_criterion_update.py \
  --scenarios examples/criterion_update/scenarios.json \
  --output results/criterion_update_results.json
```

The included artifacts are:

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

The manuscripts state that the PoC is:

```text
synthetic
deterministic
one-dimensional
structural
not production validation
```

## 7. Claim Boundary

The integrated manuscripts support structural claims only within the declared model and scenarios.

Supported in the current PoC:

```text
candidate/adoption separation
decision-stream separation
bounded legitimate adaptation
direct-update cumulative expansion
guarded P1 freezing before attack-reference admission
C1 source-integrity blocking
AUTH_STABLE + FREEZE
```

Not established:

```text
complete criterion-poisoning prevention
universal credential-theft detection
universal session-hijacking detection
universal relay-attack detection
zero false acceptance
zero false rejection
perfect identity proof
security under total compromise
production performance
privacy guarantees
formal correctness
statistical generalization
```

## 8. Publication Statements

The metadata file includes working statements for:

```text
Code and Data Availability
Conflict of Interest
Funding
Ethics and Personal Data
AI-Assisted Tools
```

These statements must be confirmed by the author before submission.

## 9. Cross-language Alignment

The English and Japanese candidates share the same section structure:

```text
Abstract / 要旨
Introduction / はじめに
Background and Related Work / 背景とRelated Work
Terminology and Scope / 用語と適用範囲
Threat Model
Formal Security Model
Criterion Update State Machine
PoC Design / PoC設計
Results / 結果
Discussion / 考察
Security Claims and Limitations / Security Claimsと限界
Reproducibility and Availability / 再現性と公開物
Conclusion / 結論
References / 参考文献
AI-Assisted Tools Disclosure / AI支援ツールの使用
```

The candidates are semantically aligned, but a final paragraph-by-paragraph language review remains necessary after figure insertion and formatting.

## 10. Submission Readiness

Current status:

```text
Research model:                 READY
Threat Model:                   READY
Formal Security Model:          READY
State Machine:                  READY
PoC implementation:             READY
PoC result record:              READY
Security claim boundary:        READY
Related Work integration:       READY FOR FIRST SUBMISSION DRAFT
English manuscript content:     SUBMISSION CANDIDATE
Japanese manuscript content:    SUBMISSION CANDIDATE
Figure source:                  READY
Rendered figures:               NOT YET GENERATED
Final PDF layout:               NOT YET GENERATED
Publisher metadata verification: PARTIAL
jxiv upload package:            NOT YET GENERATED
```

The repository is ready to move from content integration to publication production.

## 11. Remaining Publication-production Work

Required before submission:

1. render Mermaid figures to SVG/PDF;
2. insert figures and tables into the final document source;
3. verify exact reference metadata against publisher records;
4. confirm author affiliation, email, and ORCID if used;
5. apply the current jxiv format and metadata requirements;
6. generate English and Japanese PDFs;
7. inspect fonts, equations, page breaks, captions, and links;
8. run final cross-language and claim-consistency review;
9. execute the PoC once more from a clean checkout;
10. record the final commit SHA used for publication;
11. prepare upload filenames and jxiv metadata;
12. submit as a new study rather than replacing the foundational GyroAuth paper.

## 12. Layer Consistency

```text
Gyro Logic Core change: none
GyroOS contract change: none
GyroAuth application-layer model: extended
```

No change was made to `gitGyro-Dev/gyrologic` or `gitGyro-Dev/gyroos`.

## 13. Priority L Result

Priority L is complete at the Markdown manuscript-integration level.

```text
Priority L content integration: complete
Publication rendering and PDF production: remaining
jxiv submission: remaining
```
