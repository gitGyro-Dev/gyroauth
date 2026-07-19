# Guarded Criterion Trajectories — Publication Rendering and Jxiv Preflight

## 1. Purpose

This document records the publication-rendering workflow and the Jxiv-oriented preflight applied to the English and Japanese submission candidates.

## 2. Current Jxiv requirements reflected in the workflow

The rendering process is designed around the Jxiv guidelines revised on June 1, 2026.

The publication PDF must:

```text
be written in Japanese or English
be uploaded as one PDF per manuscript
contain the complete article, including figures and tables
include title, all author names, affiliations,
and corresponding-author identification and contact details
permit text extraction
remain below 20 MB
use a standard journal-like layout
```

Jxiv does not prescribe a dedicated manuscript template.

The submission system separately requires bibliographic metadata, references, keywords, conflict-of-interest disclosure, manuscript status, and license selection.

## 3. Added artifacts

```text
paper/jxiv_publication_metadata.yaml
tools/build_guarded_criterion_publication.py
.github/workflows/build_guarded_criterion_publication.yml
```

Expected generated artifacts:

```text
dist/guarded_criterion_trajectories_en.pdf
dist/guarded_criterion_trajectories_jp.pdf
```

## 4. Build command

Local build:

```bash
python -m pip install pyyaml
AUTHOR_EMAIL="author@example.org" \
python tools/build_guarded_criterion_publication.py --strict
```

GitHub Actions build:

```text
Build Guarded Criterion Publication PDFs
```

For a submission-ready build, configure the repository Actions secret:

```text
JXIV_CORRESPONDING_EMAIL
```

Without this secret, the workflow creates review PDFs containing the visible placeholder:

```text
REPLACE_BEFORE_SUBMISSION
```

Such PDFs must not be submitted to Jxiv.

## 5. Automated preflight

The build checks:

```text
English PDF generation
Japanese PDF generation
LuaLaTeX completion
PDF file size below 20 MB
text extraction through pdftotext
title text present in extracted content
```

The workflow uploads both PDFs as a GitHub Actions artifact for visual inspection.

## 6. Manual preflight still required

Before submission, verify:

```text
no clipped text
no missing Japanese glyphs
no broken equations
no overflow in code blocks or tables
correct title and author order
Independent Researcher affiliation
ORCID 0009-0004-0091-1303
valid corresponding-author email
complete figures and tables
reference accuracy
English/Japanese manuscript distinction
conflict-of-interest statement
license selection
```

## 7. Translation handling

If the English and Japanese manuscripts are submitted as separate original-language presentations of substantially identical work, the Jxiv translation rules must be checked at submission time.

A translated manuscript generally requires:

```text
same authors as the original
permission from the copyright owner
clear identification as a translated manuscript
the original paper's bibliographic information on the title page
```

The two PDFs generated here do not automatically add a translation cover statement because the original/translation submission order has not yet been fixed.

## 8. Current blocker

The corresponding-author email is not stored in the repository.

Therefore:

```text
rendering automation: ready
review PDF generation: ready
strict submission PDF generation: blocked until JXIV_CORRESPONDING_EMAIL is configured
Jxiv submission itself: not performed
```

## 9. Layer consistency

```text
Gyro Logic Core change: none
GyroOS contract change: none
GyroAuth publication tooling: added
```
