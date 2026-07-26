# Project Cycle Reflection — GyroAuth v2.1.0 Release and GitHub Pages Demo

Date: 2026-07-26  
Repository: `gitGyro-Dev/gyroauth`  
Scope: Guarded Criterion Trajectories publication package, GitHub Pages research demo, and v2.1.0 release  
Status: v2.1.0 released; GitHub Pages demo published; English Jxiv manuscript remains under review.

## 1. Hubへ反映する内容

### 1.1 Cycle Summary

This cycle converted the Guarded Criterion Trajectories research result into a public-facing repository release and an interactive GitHub Pages research demo.

The public flow is now:

```text
GitHub Repository
→ Live Research Demo
→ Jxiv publication status
→ Reproducible PoC and source artifacts
```

The demo visualizes the central distinction:

```text
Auth Decision
!=
Criterion Update Response
```

and the executable state:

```text
AUTH_STABLE + FREEZE
```

This means that the current Authentication Relation may remain continuable while the future criterion-update path is frozen.

The invariant application definition remains:

```text
Authentication
=
Stability-based Selection over State Convergence
```

### 1.2 Dashboard Update Candidates

Record the following GyroAuth status:

```text
Project: GyroAuth
Release: v2.1.0
Release status: published / latest
Demo status: published
Demo URL: https://gitgyro-dev.github.io/gyroauth/
English Jxiv manuscript: submitted / under review
Japanese manuscript and PDF: complete / submission candidate
PoC status: deterministic scenarios complete
Public communication stage: repository + demo + release available
```

Suggested dashboard highlight:

> GyroAuth v2.1.0 has been released with a public GitHub Pages research demo that separates current authentication decisions from future criterion-update responses.

### 1.3 Weekly Record

Record as completed:

- created the minimal static GitHub Pages demo;
- published the demo from `main` / `docs`;
- verified the public Pages URL;
- added README navigation to the Live Demo;
- prepared v2.1.0 Release Notes;
- published GyroAuth v2.1.0;
- updated README Latest Release navigation to the formal Release page;
- preserved Jxiv status as `Under review` without adding an unconfirmed DOI;
- received a GitHub star, indicating initial external repository interest.

### 1.4 Roadmap Progress

```text
Guarded Criterion Trajectories formalization: complete
Deterministic PoC: complete
English/Japanese publication PDFs: complete
English Jxiv submission: complete / under review
Minimal public research demo: complete
GitHub Pages publication: complete
README public navigation: complete
v2.1.0 release: complete
Post-publication DOI synchronization: pending
Japanese Jxiv submission decision: pending
```

### 1.5 Demo Artifact

Canonical public artifact:

```text
Artifact type: Interactive Research Demo
Name: GyroAuth Research Demo
URL: https://gitgyro-dev.github.io/gyroauth/
Source directory: docs/
Technology: HTML + CSS + Vanilla JavaScript
External API: none
External JavaScript CDN: none
Data type: deterministic public PoC data
```

The demo provides:

- three selectable scenarios;
- stage-by-stage navigation;
- Auth Decision display;
- Criterion Update Response display;
- criterion center and width;
- attack-reference admissibility;
- criterion state;
- direct-update versus guarded-update comparison;
- explicit `AUTH_STABLE + FREEZE` display;
- research-demo disclaimer;
- repository and release navigation.

### 1.6 Public Links

```text
Repository:
https://github.com/gitGyro-Dev/gyroauth

Live Demo:
https://gitgyro-dev.github.io/gyroauth/

Latest Release:
https://github.com/gitGyro-Dev/gyroauth/releases/tag/v2.1.0

Release Notes source:
release_candidates/gyroauth/v2.1.0/release_notes.md
```

### 1.7 Jxiv, ResearchHub, and X Relationship

Current publication relation:

```text
GitHub Pages
= first-touch interactive explanation

GitHub Repository
= source, PoC, publication artifacts, and reproducibility

Jxiv
= formal research publication

ResearchHub
= external evaluation and discussion candidate after Jxiv publication

X
= announcement and entry-point distribution
```

Current Jxiv status must remain:

```text
English manuscript: Under review
```

No DOI or publication URL should be treated as final until Jxiv publication is confirmed.

After Jxiv publication:

- update README and demo Jxiv links;
- update the v2.1.0 Release description when appropriate;
- update Hub Publications, Links, Artifacts, Dashboard, and Weekly;
- prepare ResearchHub publication/discussion entry;
- announce the publication and demo relationship on X.

## 2. Developer Toolkitへ反映する内容

### 2.1 Demo Data Generation Candidate

Current demo data is a static extraction from the deterministic PoC.

Future Toolkit support should distinguish:

```text
simulation source
!=
generated demo data
!=
demo visualization
```

Candidate command:

```text
gyro demo generate-data \
  --scenarios examples/criterion_update/scenarios.json \
  --results results/criterion_update_results.json \
  --output docs/scenarios.js
```

Generation should include source commit and schema version in the generated file.

### 2.2 Pages Deployment Check

Candidate validation command:

```text
gyro pages check
```

Checks:

- `docs/index.html` exists;
- required CSS and JavaScript files exist;
- relative paths resolve;
- no forbidden secrets are present;
- no external JavaScript or analytics calls are present;
- the configured Pages source matches the repository structure;
- public URL responds after deployment.

### 2.3 Broken-Link Check

Candidate command:

```text
gyro links check --scope readme,docs,release
```

Required targets:

- Live Demo URL;
- repository URL;
- latest Release URL;
- internal Release Notes path;
- publication artifact paths;
- Jxiv link only after confirmed publication.

### 2.4 Scenario Schema Validation

Candidate schema fields:

```text
scenario_id
scenario_name
summary
stages
stage
label
auth_decision
criterion_response
criterion_center
criterion_width
criterion_state
attack_reference_admissible
```

Validation rules:

- every scenario has at least one stage;
- stage numbers are ordered and unique;
- Auth Decision and Criterion Update Response remain separate fields;
- criterion center and width are numeric;
- no generated state contradicts the canonical PoC output;
- P1 Stage 2 preserves `AUTH_STABLE + FREEZE`;
- final P1 guarded state keeps the attack reference non-admissible.

### 2.5 Screenshot and GIF Automation Candidates

Candidate commands:

```text
gyro demo screenshot
gyro demo gif
```

Suggested outputs:

```text
artifacts/demo/gyroauth_demo_default.png
artifacts/demo/gyroauth_p1_auth_stable_freeze.png
artifacts/demo/gyroauth_demo_walkthrough.gif
```

Automation must remain optional and must not add external tracking or runtime dependencies to the deployed demo.

### 2.6 README Demo-Link Synchronization

Candidate command:

```text
gyro release sync-links \
  --release v2.1.0 \
  --demo https://gitgyro-dev.github.io/gyroauth/
```

The command should update or validate:

- README Latest Release link;
- README Live Demo link;
- Release Notes links;
- Hub link candidates;
- no placeholder Jxiv URL remains after publication.

## 3. GitHub更新候補

### 3.1 Completed Files and Changes

Created:

```text
docs/index.html
docs/styles.css
docs/app.js
docs/scenarios.js
release_candidates/gyroauth/v2.1.0/release_notes.md
```

Updated:

```text
README.md
```

README now includes:

- formal v2.1.0 Release link;
- Release Notes source link;
- Live Demo link;
- central dual-evaluation proposition;
- `AUTH_STABLE + FREEZE`;
- Jxiv `Under review` status.

### 3.2 GitHub Pages Configuration

```text
Deployment source: Deploy from a branch
Branch: main
Folder: /docs
Custom domain: none
Public URL: https://gitgyro-dev.github.io/gyroauth/
```

The GitHub-generated Pages URL is not entered in the Custom domain field.

### 3.3 Workflow Addition

```text
Pages-specific Workflow added: no
```

The minimal deployment uses GitHub Pages branch deployment from `main` / `docs`.

Existing publication-PDF Workflow remains separate and unchanged.

### 3.4 Release

```text
Tag: v2.1.0
Title: GyroAuth v2.1.0 — Guarded Criterion Trajectories and Research Demo
Release status: published
Latest release: yes
Pre-release: no
Release URL: https://github.com/gitGyro-Dev/gyroauth/releases/tag/v2.1.0
```

### 3.5 Validation Result

Confirmed through the published page and repository state:

- the demo loads publicly;
- scenario controls are displayed;
- the dual-evaluation diagram is visible;
- the page uses repository-local static assets;
- README reaches the Live Demo;
- README reaches the formal v2.1.0 Release;
- no custom-domain configuration is required;
- no Jxiv DOI was fabricated;
- no production authentication claim was introduced.

### 3.6 Follow-up GitHub Candidates

After Jxiv publication:

- replace `Under review` with the confirmed publication and DOI;
- add the Jxiv link to the demo header;
- update Release Notes or Release description if appropriate;
- add a Japanese README or bilingual public entry page if prioritized;
- add deterministic demo-data generation validation;
- add broken-link and static-page checks to CI;
- create a compact screenshot for repository social preview and X posts.

## 4. 次回Gyro Project Cycleで扱う内容

### 4.1 Publication Tracking

- continue monitoring English Jxiv status;
- record editorial or technical revision requests;
- update DOI and publication URL after publication;
- decide Japanese Jxiv submission timing;
- decide ResearchHub publication timing after Jxiv publication;
- prepare X announcement text linking paper, demo, and repository.

### 4.2 Public Entry Optimization

Review visitor flow using:

```text
GitHub star / social link
→ README
→ Live Demo
→ Release
→ PoC and manuscript
```

Candidate improvements:

- shorten the README first-view explanation;
- add a screenshot or animated GIF;
- add a `Reproduce the PoC` link near the demo link;
- add Japanese guidance without duplicating canonical definitions;
- evaluate GitHub repository social-preview image.

### 4.3 Demo Validation Automation

Prioritize:

```text
scenario schema validation
broken-link check
static asset check
source-to-demo data consistency check
screenshot generation
```

### 4.4 Release and Artifact Tracking

Hub should register:

```text
Release artifact: GyroAuth v2.1.0
Demo artifact: GitHub Pages Research Demo
Publication artifact: Guarded Criterion Trajectories PDFs
Research status: English Jxiv under review
Repository status: public release available
External-interest signal: first GitHub star observed
```

### 4.5 Next Research and Implementation Candidates

- bounded `/auth/step` implementation based on the GyroOS `/loop/step` contract;
- multi-dimensional criterion representation;
- evidence provenance and independent-anchor representation;
- rollback integrity demonstration;
- additional poisoning scenarios;
- audit-trace visualization;
- empirical evaluation with synthetic or privacy-preserving data.

## 5. Layer Consistency Check

### 5.1 Gyro Logic

```text
Status: CONSISTENT / UNCHANGED
```

- The invariant Core remains `Structure → Slice → Stability`.
- No Gyro Logic canonical definition was changed.
- The demo does not promote authentication-specific terms into the Logic Core.
- The public visualization remains an application-layer explanation.

### 5.2 GyroOS

```text
Status: CONSISTENT / UNCHANGED
```

- No GyroOS Runtime Contract was changed.
- The static demo does not implement or emulate the full GyroOS runtime.
- Existing deterministic outputs are visualized without redefining `/loop/step`.
- Future `/auth/step` work remains downstream of the GyroOS execution contract.

### 5.3 GyroAuth

```text
Status: CONSISTENT / PUBLICATION AND VISUALIZATION EXTENDED
```

The application layer now includes a public interactive visualization of:

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

The extension preserves:

```text
Authentication
=
Stability-based Selection over State Convergence
```

The demo is explicitly a deterministic research demonstration and not a production authentication service or security guarantee.

### 5.4 Gyro Project Cycle

```text
Status: CONSISTENT / PUBLICATION TRACKING
```

- Project Cycle records confirmed outputs and public links.
- It does not rewrite theoretical definitions.
- It should integrate the release, demo, publication status, and external-interest signal into Dashboard, Weekly, Roadmap, Artifacts, and Links.

### 5.5 Gyro Developer Toolkit

```text
Status: CONSISTENT / DEPLOYMENT AND VALIDATION SUPPORT
```

- Toolkit candidates support generation, validation, deployment checking, link synchronization, and screenshots.
- Toolkit must not alter scenario results or theoretical definitions.
- Generated demo data must remain traceable to canonical simulation sources and commits.

## 6. Repository Structure

### 6.1 Current Relevant Structure

```text
gyroauth/
├── README.md
├── app/
│   └── vnext/
├── docs/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── scenarios.js
│   └── ... existing research documents
├── examples/
│   ├── criterion_update/
│   │   └── scenarios.json
│   └── vnext/
├── figures/
│   └── guarded_criterion_trajectories_mermaid.md
├── paper/
│   ├── guarded_criterion_trajectories_submission_en.md
│   ├── guarded_criterion_trajectories_submission_jp.md
│   ├── guarded_criterion_trajectories_submission_metadata.md
│   └── jxiv_publication_metadata.yaml
├── project_cycle/
│   ├── gyroauth_guarded_criterion_trajectories_jxiv_submission_reflection_20260724.md
│   └── gyroauth_v2_1_0_release_and_github_pages_reflection_20260726.md
├── publications/
│   └── guarded_criterion_trajectories/
│       └── jxiv_submission/
│           ├── guarded_criterion_trajectories_en.pdf
│           └── guarded_criterion_trajectories_jp.pdf
├── release_candidates/
│   └── gyroauth/
│       └── v2.1.0/
│           └── release_notes.md
├── results/
│   ├── criterion_update_results.json
│   └── criterion_update_summary.json
├── scripts/
│   └── simulate_guarded_criterion_update.py
└── tools/
    ├── build_guarded_criterion_publication.py
    └── build_guarded_criterion_publication_aligned.py
```

### 6.2 Artifact Dependency Relations

```text
examples/criterion_update/scenarios.json
+
scripts/simulate_guarded_criterion_update.py
→ results/criterion_update_results.json
→ results/criterion_update_summary.json
→ docs/scenarios.js
→ GitHub Pages visualization
```

```text
paper manuscripts
+
publication metadata
+
Mermaid figures
+
publication build tools
→ final English/Japanese PDFs
→ Jxiv submission artifacts
```

```text
research artifacts
+
GitHub Pages demo
+
README navigation
+
Release Notes
→ GyroAuth v2.1.0 public release
```

### 6.3 Repository Boundary

This cycle changed only:

```text
gitGyro-Dev/gyroauth
```

Referenced but unchanged:

```text
gitGyro-Dev/gyrologic
gitGyro-Dev/gyroos
gitGyro-Dev/gyro-hub
```

## 7. Cycle Conclusion

```text
Guarded Criterion Trajectories research package: complete
Minimal public interactive demo: complete
GitHub Pages deployment: complete
README public navigation: complete
GyroAuth v2.1.0 release: complete
English Jxiv publication: under review
Japanese submission decision: next cycle
Post-publication link synchronization: next cycle
```

The main outcome of this cycle is that GyroAuth now has a complete public path from first contact to reproducible research:

```text
See
→ Interact
→ Understand
→ Read
→ Reproduce
```
