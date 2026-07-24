# Project Cycle Reflection — Guarded Criterion Trajectories Jxiv Submission

Date: 2026-07-24  
Repository: `gitGyro-Dev/gyroauth`  
Scope: Guarded Criterion Trajectories for Adaptive Authentication  
Status: English Jxiv submission completed; under review. Japanese manuscript and PDF are complete and retained as submission candidates.

## 1. Hubへ反映する内容

### 1.1 Cycle Summary

This cycle completed the formalization, proof-of-concept validation, publication packaging, and English Jxiv submission of the GyroAuth paper:

**Guarded Criterion Trajectories for Adaptive Authentication: Separating Current Access Decisions from Future Criterion Updates**

The paper addresses the integrity of adaptive authentication criteria. It treats criterion change as a guarded and traceable trajectory rather than as unconstrained profile adaptation.

The central proposition is:

```text
dynamic criterion
!=
unconstrained self-update
```

The work separates the current authentication judgment from the authorization of future criterion change:

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

The minimum executable combination demonstrating this separation is:

```text
AUTH_STABLE + FREEZE
```

The current Authentication Relation may temporarily remain continuable while the criterion-adaptation path is frozen.

### 1.2 Completed Research Artifacts

The following research components were completed:

- research question and contribution statement;
- formal terminology and application scope;
- threat model for criterion poisoning and Evidence-source compromise;
- Formal Security Model;
- Guard vector and critical-failure semantics;
- Criterion Update State Machine;
- Criterion Update Responses:
  - `ACCEPT`
  - `DEFER`
  - `FREEZE`
  - `REVIEW`
  - `ROLLBACK`;
- deterministic proof of concept;
- normal and adversarial scenarios;
- security claims, limitations, and non-guarantees;
- Related Work and verified references;
- English and Japanese submission manuscripts;
- six canonical publication figures;
- English and Japanese final PDFs;
- Jxiv submission metadata;
- AI-assisted tools disclosure;
- publication workflow and technical preflight checks.

### 1.3 PoC Results

Three deterministic scenarios were implemented.

#### N1: Legitimate New Device Transition

The guarded model deferred criterion adaptation until challenge confirmation and cross-evidence support were available, then accepted a bounded update.

```text
Auth Decision:
REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_STABLE

Criterion Update Response:
DEFER
→ ACCEPT
→ ACCEPT
```

Final values:

```text
mu    = 0.234
width = 0.120
```

#### P1: Gradual Region Expansion Poisoning

The direct-update baseline expanded the criterion until the attack reference became admissible.

```text
final mu    = 0.3969728
final width = 0.277212
attack reference admissible = true
```

The guarded model froze adaptation before admission.

```text
final mu    = 0.200
final width = 0.120
freeze stage = 2
attack reference admissible = false
```

Response path:

```text
DEFER
→ FREEZE
→ FREEZE
→ FREEZE
→ FREEZE
```

At stage 2:

```text
AUTH_STABLE + FREEZE
```

#### C1: Single Evidence Source Compromise

The guarded model rejected automatic adoption despite apparently strong Evidence values because source integrity and cross-evidence consistency were insufficient.

```text
FREEZE
→ FREEZE
```

Final values remained:

```text
mu    = 0.200
width = 0.120
```

All seven executable assertions passed.

### 1.4 Publication Status

English publication PDF:

```text
publications/guarded_criterion_trajectories/jxiv_submission/
guarded_criterion_trajectories_en.pdf
```

Japanese publication PDF:

```text
publications/guarded_criterion_trajectories/jxiv_submission/
guarded_criterion_trajectories_jp.pdf
```

Current publication state:

```text
English Jxiv submission: submitted / under review
Japanese Jxiv submission: manuscript and PDF complete / not yet submitted
```

The final publication PDFs include:

- title;
- author;
- affiliation;
- ORCID;
- corresponding-author email;
- abstract or Japanese summary;
- keywords;
- six rendered figures;
- references;
- AI-assisted tools disclosure;
- declarations.

### 1.5 Latest Gyro Logic Relationship

The paper preserves the invariant Core:

```text
Structure → Slice → Stability
```

It does not redefine the Gyro Logic canonical definitions or the GyroOS runtime contract.

The paper is consistent with the current Gyro Logic Minimal Formal Model in the following areas:

- invariant Core preservation;
- `History != Trajectory`;
- contextual tracing of admissible relations;
- Identity is not reduced to a Credential, device, location, or behavior;
- Stability is not treated as a universal terminal completion;
- application-layer decisions can remain distinct while a current relation remains locally continuable.

The following latest Logic concepts are not directly formalized in this paper:

- local articulation;
- Stability Scene;
- Incorporated Readability;
- explicit Continuity Readability;
- non-metric Difference formalization;
- Boundary as a derivative readable distinction;
- direct citation of the current Minimal Formal Model paper.

The correct project-level characterization is:

> The GyroAuth paper is consistent with the latest Gyro Logic, but it does not claim to implement the complete Minimal Formal Model.

## 2. Developer Toolkitへ反映する内容

### 2.1 Publication Automation Requirements

This cycle established a reusable publication workflow pattern for Gyro repositories.

Required functions:

- deterministic manuscript assembly;
- Mermaid extraction and rendering;
- SVG, PNG, and PDF figure generation;
- canonical figure-number validation;
- fixed, non-floating figure placement;
- English and Japanese PDF generation through Pandoc and LuaLaTeX;
- A4 validation;
- PDF size validation against the Jxiv 20 MB limit;
- text-extraction checks;
- author and corresponding-email checks;
- embedded-image count checks;
- publication artifact upload;
- final PDF commit to a repository publication directory;
- prevention of recursive workflow execution.

### 2.2 Reusable Failure Cases

The Developer Toolkit should retain checks or guidance for the following failure modes discovered in this cycle:

- an empty environment variable preventing fallback to repository metadata;
- Mermaid CLI Chromium sandbox failure on Ubuntu runners;
- unsupported Pandoc reader extensions;
- resource-path failures for generated figures;
- implicit LaTeX figure floats dropping a late figure;
- Python string escapes injecting control characters into raw LaTeX;
- missing `graphicx` when only raw LaTeX image blocks are used;
- `git diff --quiet` failing to detect untracked generated files;
- over-broad figure-caption parsing consuming later documentation sections;
- long Mermaid quadrant-chart titles being clipped;
- preflight steps that fail without identifying the exact failed assertion.

### 2.3 Candidate Toolkit Features

Future reusable commands or modules:

```text
gyro publication build
gyro publication preflight
gyro publication inspect
gyro publication commit
gyro figures render
gyro figures validate-order
gyro jxiv metadata validate
```

Candidate validation schemas:

```text
PublicationMetadata
FigureSpecification
PublicationPreflightResult
JxivSubmissionChecklist
GeneratedArtifactManifest
```

The publication workflow should distinguish:

```text
source manuscript
!=
generated publication artifact
```

and:

```text
workflow success
!=
visual publication approval
```

## 3. GitHub更新候補

### 3.1 Completed in `gitGyro-Dev/gyroauth`

Completed repository updates include:

- formal terminology and scope documents;
- threat and security-claim documents;
- deterministic simulation and scenarios;
- English and Japanese manuscripts;
- six canonical Mermaid figures;
- aligned publication builder;
- GitHub Actions publication workflow;
- robust PDF preflight diagnostics;
- final English and Japanese publication PDFs;
- publication-PDF auto-commit flow;
- submission metadata and AI disclosure.

### 3.2 Follow-up Candidates

After Jxiv review or publication:

- record English Jxiv identifier and DOI when assigned;
- update README and README_jp publication sections;
- update publication index and repository links;
- record the submission and publication state in release notes;
- create or update a release candidate for the next GyroAuth version;
- add the latest Gyro Logic Minimal Formal Model citation after its publication, if a version update is appropriate;
- decide whether the Japanese paper should be submitted immediately or after English acceptance/publication;
- update submission metadata checklist items that still represent pre-generation status;
- preserve an immutable manifest containing PDF SHA, source commit, workflow run, and build-tool versions.

### 3.3 Publication Files

Canonical final-PDF directory:

```text
publications/
└── guarded_criterion_trajectories/
    └── jxiv_submission/
        ├── guarded_criterion_trajectories_en.pdf
        └── guarded_criterion_trajectories_jp.pdf
```

Canonical figure order:

```text
Figure 1  Dual Evaluation Architecture
Figure 2  Research Positioning
Figure 3  Guarded Criterion Update Pipeline
Figure 4  Criterion Update State Machine
Figure 5  P1 Direct versus Guarded Update
Figure 6  Decision-space Separation
```

## 4. 次回Gyro Project Cycleで扱う内容

### 4.1 Publication Tracking

- monitor English Jxiv review status;
- record any editorial or technical revision request;
- assign DOI and publication URL after release;
- determine the timing of the Japanese submission;
- update Hub publications, links, artifacts, dashboard, and weekly records.

### 4.2 Logic-to-Auth Connection

After publication of the Gyro Logic Minimal Formal Model, review whether the Auth paper or its next version should explicitly connect:

```text
Accepted Criterion Update
↔
application-layer Incorporated Readability
```

This must remain a candidate correspondence, not an automatic identity.

Also examine:

- Local Authentication Realization and local articulation;
- `AUTH_STABLE` versus Logic-level Stability Scene;
- Continuity Readability versus Expected Identity;
- Auth Deviation versus Logic-level Difference;
- admissible criterion regions versus Boundary and Boundary State.

### 4.3 Next Research Candidates

Potential next papers or cycles:

- formal connection between Criterion Trajectory and the Minimal Formal Model;
- multi-dimensional criterion representation;
- evidence-provenance graph and independent-anchor formalization;
- rollback-point integrity;
- coordinated multi-source compromise;
- criterion translation and slow-contraction poisoning;
- empirical evaluation using privacy-preserving or synthetic datasets;
- bounded `/auth/step` implementation connected to the GyroOS `/loop/step` contract;
- operational UI and audit-trace visualization.

### 4.4 Project Management Updates

The Gyro Hub should record:

```text
Project: GyroAuth
Artifact: Guarded Criterion Trajectories
English submission: completed / under review
Japanese artifact: final PDF complete
Research stage: publication review
Implementation stage: deterministic PoC complete
Next decision: Japanese submission timing and post-publication integration
```

## 5. Layer Consistency Check

### 5.1 Gyro Logic

```text
Status: CONSISTENT
```

- The invariant Core remains `Structure → Slice → Stability`.
- Canonical definitions were not rewritten.
- No application-specific authentication concept was promoted into the Logic Core.
- The paper uses Logic concepts as theoretical constraints rather than redefining them.

### 5.2 GyroOS

```text
Status: CONSISTENT
```

- The GyroOS runtime contract was not changed.
- No claim was made that the current deterministic PoC is the canonical GyroOS runtime.
- Future `/auth/step` integration remains downstream of the GyroOS execution contract.

### 5.3 GyroAuth

```text
Status: CONSISTENT / EXTENDED
```

The application layer was extended with:

- Authentication Criterion;
- Criterion Trajectory;
- Criterion Integrity;
- Criterion Update Candidate;
- Guard vector;
- Criterion Update Response;
- Criterion Update State Machine;
- guarded adoption and rollback semantics.

The extension preserves:

```text
Authentication
=
Stability-based Selection over State Convergence
```

It adds an independent evaluation of whether the future criterion may change.

### 5.4 Gyro Project Cycle

```text
Status: CONSISTENT
```

The Project Cycle records progress, artifacts, publication state, dependencies, and next actions. It does not redefine theory, runtime, or authentication semantics.

### 5.5 Gyro Developer Toolkit

```text
Status: CONSISTENT
```

The Toolkit and GitHub Actions support rendering, validation, packaging, inspection, and repository updates. They do not alter theoretical definitions or research claims.

## 6. Repository Structure

Relevant repository structure after this cycle:

```text
.github/
└── workflows/
    └── build_guarded_criterion_publication.yml

docs/
├── 16_formal_terminology_and_scope.md
├── 23_security_claims_and_limitations.md
├── 27_figures_and_captions.md
└── 30_publication_rendering_and_jxiv_preflight.md

examples/
└── criterion_update/
    └── scenarios.json

figures/
└── guarded_criterion_trajectories_mermaid.md

paper/
├── guarded_criterion_trajectories_full_en.md
├── guarded_criterion_trajectories_full_jp.md
├── guarded_criterion_trajectories_submission_en.md
├── guarded_criterion_trajectories_submission_jp.md
├── guarded_criterion_trajectories_submission_metadata.md
└── jxiv_publication_metadata.yaml

publications/
└── guarded_criterion_trajectories/
    └── jxiv_submission/
        ├── guarded_criterion_trajectories_en.pdf
        └── guarded_criterion_trajectories_jp.pdf

results/
└── criterion_update_summary.json

scripts/
└── simulate_guarded_criterion_update.py

tools/
├── build_guarded_criterion_publication.py
└── build_guarded_criterion_publication_aligned.py

project_cycle/
└── gyroauth_guarded_criterion_trajectories_jxiv_submission_reflection_20260724.md
```

## Reflection Conclusion

This cycle moved the Guarded Criterion Trajectories work from conceptual separation to an executable, documented, reproducible, publication-ready GyroAuth study.

The main research result is not that adaptive authentication should stop adapting. It is that adaptation of the future authentication criterion must be evaluated independently from the current authentication decision.

```text
dynamic criterion
!=
unconstrained self-update
```

```text
AUTH_STABLE + FREEZE
```

The English paper has been submitted to Jxiv and is under review. The Japanese paper is complete and retained as the next publication candidate. The next Project Cycle should focus on publication tracking, Hub integration, Japanese submission timing, and a carefully bounded connection to the latest Gyro Logic Minimal Formal Model.