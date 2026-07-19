# Guarded Criterion Trajectories — Submission Metadata

## English

**Title**  
Guarded Criterion Trajectories for Adaptive Authentication: Separating Current Access Decisions from Future Criterion Updates

**Short title**  
Guarded Criterion Trajectories for Adaptive Authentication

**Author**  
Shuntaro Kawakami

**Affiliation**  
Individual

**ORCID**  
0009-0004-0091-1303

**Corresponding author email**  
dev.jxiv@gyro-wedge.com

**Keywords**  
adaptive authentication; continuous authentication; criterion poisoning; guarded adaptation; criterion integrity; trajectory; GyroAuth

**Article type**  
Research article / technical study

**Language**  
English

## Japanese

**題名**  
適応型認証におけるGuard付きCriterion Trajectory：現在の認証判断と将来の認証基準更新の分離

**短縮題名**  
適応型認証におけるGuard付きCriterion Trajectory

**著者**  
川上俊太郎

**所属**  
個人

**ORCID**  
0009-0004-0091-1303

**責任著者連絡先**  
dev.jxiv@gyro-wedge.com

**キーワード**  
適応型認証；継続認証；Criterion poisoning；Guard付き適応；Criterion Integrity；Trajectory；GyroAuth

**原稿種別**  
研究論文／技術研究

**言語**  
日本語

## Central Contribution Statement

> The study introduces an explicit criterion-integrity model in which proposed authentication-criterion changes form a guarded, traceable trajectory and are authorized independently from current access decisions.

## Repository Artifacts

```text
paper/guarded_criterion_trajectories_submission_en.md
paper/guarded_criterion_trajectories_submission_jp.md
figures/guarded_criterion_trajectories_mermaid.md
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

## Reproducibility Command

```bash
python scripts/simulate_guarded_criterion_update.py \
  --scenarios examples/criterion_update/scenarios.json \
  --output results/criterion_update_results.json
```

## Required Statements

### Code and Data Availability

The source code, deterministic scenario inputs, and result summary used in this study are available in the public GyroAuth repository. The study uses synthetic inputs and does not include personal authentication telemetry.

### Conflict of Interest

The author declares no conflict of interest unless a different statement becomes necessary before submission.

### Funding

No external funding is declared unless a different statement becomes necessary before submission.

### Ethics and Personal Data

The proof of concept uses synthetic deterministic inputs and does not use human-subject data or personal authentication records.

### AI-Assisted Tools

AI-assisted tools were used for structural organization, drafting support, expression refinement, and consistency checking. The author reviewed and edited the content, claims, references, and final manuscript and assumes full responsibility for them.

## Final Submission Checklist

- [x] Research question and contribution fixed
- [x] Formal terminology and scope fixed
- [x] Threat Model documented
- [x] Formal Security Model documented
- [x] Criterion Update State Machine documented
- [x] Normal and poisoned scenarios documented
- [x] Minimal deterministic PoC implemented
- [x] Result summary recorded
- [x] Security claims and limitations documented
- [x] Related Work integrated into submission manuscripts
- [x] Verified reference subset integrated
- [x] English submission candidate created
- [x] Japanese submission candidate created
- [x] Editable figure sources created
- [ ] Render figures to SVG/PDF
- [ ] Insert rendered figures into final PDF source
- [ ] Verify reference metadata against final publisher records
- [x] Confirm author affiliation and contact metadata
- [ ] Apply final jxiv template and page formatting
- [ ] Generate English PDF
- [ ] Generate Japanese PDF
- [ ] Perform visual PDF inspection
- [ ] Run final English/Japanese paragraph-alignment review
- [ ] Confirm filenames and upload metadata
- [ ] Submit or replace files on jxiv
