#!/usr/bin/env python3
"""Build Jxiv-oriented English and Japanese PDFs for the guarded criterion paper."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
BUILD = ROOT / "build" / "guarded_criterion_trajectories"
DIST = ROOT / "dist"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def strip_working_header(text: str) -> str:
    """Remove the draft-only title and status lines from a manuscript."""
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
        ):
            continue
        if skipping and not line.strip():
            continue
        skipping = False
        out.append(line)
    return "\n".join(out).strip() + "\n"


def normalize_submission_headings(text: str, lang: str) -> str:
    """Convert draft headings into clean Pandoc section headings.

    The manuscript sources retain explicit section numbers for readability on
    GitHub. Publication PDFs use Pandoc's --number-sections instead, so those
    manual prefixes are removed during the build. Heading levels are also
    shifted up because the document title is supplied through metadata rather
    than represented as a numbered H1 section.
    """
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


def title_block(meta: dict[str, str], lang: str) -> str:
    """Create Pandoc metadata and visible author/contact information."""
    email = os.getenv("AUTHOR_EMAIL", meta["corresponding_email"])
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
    body = normalize_submission_headings(body, lang)
    merged = title_block(meta, lang) + "\n" + body

    BUILD.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    md = BUILD / f"guarded_criterion_trajectories_{lang}.md"
    md.write_text(merged, encoding="utf-8")

    out = DIST / f"guarded_criterion_trajectories_{lang}.pdf"
    common = [
        "pandoc", str(md), "-o", str(out),
        "--from", "gfm+tex_math_dollars",
        "--pdf-engine=lualatex",
        "--toc",
        "--number-sections",
        "-V", "geometry:margin=24mm",
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
    print(f"preflight ok: {pdf.name} ({pdf.stat().st_size} bytes, {len(extracted)} extracted chars)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Fail when corresponding email is still a placeholder")
    args = parser.parse_args()

    meta = yaml.safe_load((PAPER / "jxiv_publication_metadata.yaml").read_text(encoding="utf-8"))
    email = os.getenv("AUTHOR_EMAIL", meta["corresponding_email"])
    if args.strict and ("REPLACE" in email or "@" not in email):
        raise SystemExit("AUTHOR_EMAIL must be supplied for a submission-ready PDF")
    if shutil.which("pandoc") is None or shutil.which("lualatex") is None:
        raise SystemExit("pandoc and lualatex are required")

    outputs = [build_one(meta, "en"), build_one(meta, "jp")]
    for output in outputs:
        preflight(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
