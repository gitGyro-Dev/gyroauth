#!/usr/bin/env python3
"""Build Jxiv-oriented English and Japanese PDFs for the guarded criterion paper."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
FIGURE_SOURCE = ROOT / "figures" / "guarded_criterion_trajectories_mermaid.md"
BUILD = ROOT / "build" / "guarded_criterion_trajectories"
BUILD_FIGURES = BUILD / "figures"
DIST = ROOT / "dist"
DIST_FIGURES = DIST / "figures"


@dataclass(frozen=True)
class FigureSpec:
    number: int
    title: str
    mermaid: str
    caption_en: str


JP_CAPTIONS = {
    1: "GyroAuthは、現在のAuthentication Relationと、将来の評価に用いるCriterionのIntegrityを、関連しつつも別のProcessとして評価する。",
    2: "Candidate生成とCandidate採用を分離する。Candidateを有効化するのはACCEPTのみである。",
    3: "Criterion StateとCriterion Update Responseは異なる。FREEZEはSubject Evaluationを必ずしも終了させず、適応経路を停止する。",
    4: "実装したP1 Scenarioでは、直接採用は攻撃参照値が許容されるまでCriterionを拡張した一方、Guard付き採用は許容前に適応を凍結した。",
    5: "AUTH_STABLE + FREEZEは、現在のAuthentication Relationを一時的に継続しながら、Criterion適応を禁止する状態を表す。",
    6: "本提案は、Adaptive Authentication、Continuous Authentication、Drift対応、およびPoisoning-aware adaptationの交点に位置づけられる。",
}

FIGURE_INSERTION_TARGETS = {
    1: r"^##\s+2\.",
    6: r"^##\s+3\.",
    2: r"^##\s+6\.",
    3: r"^##\s+7\.",
    4: r"^###\s+8\.3\b",
    5: r"^##\s+10\.",
}


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def strip_working_header(text: str) -> str:
    """Remove draft-only title and status lines from a manuscript."""
    lines = text.splitlines()
    out: list[str] = []
    skipping = True
    for line in lines:
        if skipping and line.startswith("# "):
            continue
        if skipping and (
            line.startswith("**Author:")
            or line.startswith("**Project:")
            or line.startswith("**Manuscript status:")
            or line.startswith("**著者:")
            or line.startswith("**プロジェクト:")
            or line.startswith("**原稿状態:")
        ):
            continue
        if skipping and not line.strip():
            continue
        skipping = False
        out.append(line)
    return "\n".join(out).strip() + "\n"


def normalize_submission_headings(text: str, lang: str) -> str:
    """Remove manual numbering and let Pandoc number the publication PDF."""
    normalized: list[str] = []
    heading_re = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
    number_re = re.compile(r"^\d+(?:\.\d+)*\.?\s+")
    abstract_title = "Abstract" if lang == "en" else "要旨"

    for line in text.splitlines():
        match = heading_re.match(line)
        if not match:
            normalized.append(line)
            continue
        hashes, title = match.groups()
        title = number_re.sub("", title).strip()
        new_hashes = "#" * (len(hashes) - 1)
        if title == abstract_title:
            normalized.append(f"{new_hashes} {title} {{.unnumbered}}")
        else:
            normalized.append(f"{new_hashes} {title}")
    return "\n".join(normalized).strip() + "\n"


def parse_figure_source() -> list[FigureSpec]:
    text = FIGURE_SOURCE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^## Figure\s+(\d+)\.\s+(.+?)\n\n"
        r"```mermaid\n(.*?)\n```\n\n"
        r"\*\*Caption:\*\*\s+(.+?)"
        r"(?=\n\n## Figure|\n\n## Rendering Notes|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    specs = [
        FigureSpec(int(number), title.strip(), mermaid.strip() + "\n", caption.strip())
        for number, title, mermaid, caption in pattern.findall(text)
    ]
    if [spec.number for spec in specs] != [1, 2, 3, 4, 5, 6]:
        raise SystemExit("Expected Figure 1 through Figure 6 in Mermaid source")
    return specs


def render_figures() -> None:
    """Render Mermaid diagrams to editable SVG, publication PNG, and PDF."""
    if shutil.which("mmdc") is None:
        raise SystemExit("Mermaid CLI (mmdc) is required")

    BUILD_FIGURES.mkdir(parents=True, exist_ok=True)
    DIST_FIGURES.mkdir(parents=True, exist_ok=True)
    config_path = BUILD_FIGURES / "mermaid-config.json"
    config_path.write_text(
        json.dumps(
            {
                "theme": "neutral",
                "flowchart": {"htmlLabels": False, "curve": "linear"},
                "fontFamily": "Noto Sans, DejaVu Sans, sans-serif",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    for spec in parse_figure_source():
        stem = f"figure_{spec.number}"
        mmd = BUILD_FIGURES / f"{stem}.mmd"
        mmd.write_text(spec.mermaid, encoding="utf-8")
        for suffix in ("svg", "png", "pdf"):
            output = BUILD_FIGURES / f"{stem}.{suffix}"
            cmd = [
                "mmdc",
                "-i", str(mmd),
                "-o", str(output),
                "-c", str(config_path),
                "-t", "neutral",
                "-b", "white",
                "--scale", "2",
            ]
            if suffix == "png":
                cmd += ["-w", "1800"]
            run(cmd)
            shutil.copy2(output, DIST_FIGURES / output.name)


def figure_markdown(number: int, lang: str) -> str:
    specs = {spec.number: spec for spec in parse_figure_source()}
    caption = specs[number].caption_en if lang == "en" else JP_CAPTIONS[number]
    return (
        f"\n\n![{caption}](figures/figure_{number}.png)"
        f"{{#fig:guarded-criterion-{number} width=95%}}\n\n"
    )


def insert_figures(body: str, lang: str) -> str:
    """Insert six rendered figures at stable semantic points in both manuscripts."""
    for number in (1, 6, 2, 3, 4, 5):
        target = re.compile(FIGURE_INSERTION_TARGETS[number], re.MULTILINE)
        match = target.search(body)
        if match is None:
            raise SystemExit(
                f"Could not find insertion target for Figure {number} in {lang} manuscript"
            )
        body = body[: match.start()] + figure_markdown(number, lang) + body[match.start() :]
    return body


def resolved_email(meta: dict[str, str]) -> str:
    """Use a non-empty Actions secret when present, otherwise repository metadata."""
    return os.getenv("AUTHOR_EMAIL") or meta["corresponding_email"]


def title_block(meta: dict[str, str], lang: str) -> str:
    """Create Pandoc metadata and visible author/contact information."""
    email = resolved_email(meta)
    if lang == "en":
        metadata = {
            "title": meta["title_en"],
            "author": meta["author_en"],
            "keywords": meta["keywords_en"],
            "lang": "en",
        }
        visible = f"""**Affiliation:** {meta['affiliation_en']}  
**ORCID:** {meta['orcid']}  
**Corresponding author:** {email}

**Keywords:** {meta['keywords_en']}

---
"""
    else:
        metadata = {
            "title": meta["title_jp"],
            "author": meta["author_jp"],
            "keywords": meta["keywords_jp"],
            "lang": "ja",
        }
        visible = f"""**所属:** {meta['affiliation_jp']}  
**ORCID:** {meta['orcid']}  
**責任著者連絡先:** {email}

**キーワード:** {meta['keywords_jp']}

---
"""
    yaml_text = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{yaml_text}\n---\n\n{visible}"


def append_required_statements(body: str, meta: dict[str, str], lang: str) -> str:
    if lang == "en":
        appendix = f"""

## Declarations

**Conflict of Interest.** {meta['conflict_en']}

**Funding.** {meta['funding_en']}

**Ethics and Personal Data.** {meta['ethics_en']}

**Code and Data Availability.** The source code, deterministic scenario inputs, and result summary are available in the public GyroAuth repository. The study uses synthetic inputs and contains no personal authentication telemetry.

**AI-Assisted Tools Disclosure.** AI-assisted tools were used for structural organization, drafting support, expression refinement, and consistency checking. The author reviewed and edited the content, claims, references, and final manuscript and assumes full responsibility for them.
"""
    else:
        appendix = f"""

## 申告事項

**利益相反。** {meta['conflict_jp']}

**研究資金。** {meta['funding_jp']}

**倫理および個人データ。** {meta['ethics_jp']}

**コードおよびデータの公開。** 本研究で使用したソースコード、決定論的シナリオ入力、結果概要は公開GyroAuthリポジトリで提供する。本研究は合成入力を使用し、個人の認証テレメトリを含まない。

**AI支援ツールの使用。** 構成整理、草稿作成補助、表現調整、整合性確認のためにAI支援ツールを使用した。本文、主張、参考文献および最終原稿は著者が確認・編集し、全責任を負う。
"""
    if "## Declarations" in body or "## 申告事項" in body:
        return body
    return body.rstrip() + appendix + "\n"


def build_one(meta: dict[str, str], lang: str) -> Path:
    src = PAPER / f"guarded_criterion_trajectories_submission_{lang}.md"
    body = strip_working_header(src.read_text(encoding="utf-8"))
    body = append_required_statements(body, meta, lang)
    body = insert_figures(body, lang)
    body = normalize_submission_headings(body, lang)
    merged = title_block(meta, lang) + "\n" + body

    BUILD.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    md = BUILD / f"guarded_criterion_trajectories_{lang}.md"
    md.write_text(merged, encoding="utf-8")

    out = DIST / f"guarded_criterion_trajectories_{lang}.pdf"
    common = [
        "pandoc", str(md), "-o", str(out),
        "--from", "markdown+tex_math_dollars+link_attributes+fenced_code_blocks+pipe_tables+strikeout+task_lists+autolink_bare_uris",
        "--pdf-engine=lualatex",
        "--resource-path", str(BUILD),
        "--toc",
        "--number-sections",
        "-V", "papersize=a4",
        "-V", "geometry:a4paper,margin=24mm",
        "-V", "fontsize=10.5pt",
        "-V", "colorlinks=true",
        "-V", "linkcolor=black",
        "-V", "urlcolor=blue",
    ]
    if lang == "jp":
        common += [
            "-V", "documentclass=ltjsarticle",
            "-V", "mainfont=Noto Serif CJK JP",
            "-V", "sansfont=Noto Sans CJK JP",
            "-V", "monofont=Noto Sans Mono CJK JP",
            "-V", "CJKmainfont=Noto Serif CJK JP",
        ]
    else:
        common += [
            "-V", "mainfont=Libertinus Serif",
            "-V", "sansfont=Libertinus Sans",
            "-V", "monofont=DejaVu Sans Mono",
        ]
    run(common)
    return out


def preflight(pdf: Path) -> None:
    if pdf.stat().st_size > 20 * 1024 * 1024:
        raise SystemExit(f"{pdf} exceeds Jxiv 20 MB limit")
    txt = pdf.with_suffix(".txt")
    run(["pdftotext", str(pdf), str(txt)])
    extracted = txt.read_text(encoding="utf-8", errors="replace")
    if len(extracted.strip()) < 1000:
        raise SystemExit(f"Text extraction appears insufficient: {pdf}")
    print(
        f"preflight ok: {pdf.name} "
        f"({pdf.stat().st_size} bytes, {len(extracted)} extracted chars)"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict", action="store_true",
        help="Fail when corresponding email is still a placeholder",
    )
    args = parser.parse_args()

    meta = yaml.safe_load(
        (PAPER / "jxiv_publication_metadata.yaml").read_text(encoding="utf-8")
    )
    email = resolved_email(meta)
    if args.strict and ("REPLACE" in email or "@" not in email):
        raise SystemExit(
            "A valid corresponding email must be supplied by AUTHOR_EMAIL or repository metadata"
        )
    if shutil.which("pandoc") is None or shutil.which("lualatex") is None:
        raise SystemExit("pandoc and lualatex are required")

    render_figures()
    outputs = [build_one(meta, "en"), build_one(meta, "jp")]
    for output in outputs:
        preflight(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
