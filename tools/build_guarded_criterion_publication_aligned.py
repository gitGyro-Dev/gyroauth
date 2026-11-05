#!/usr/bin/env python3
"""Build publication PDFs with canonical figure numbering aligned to placement order."""
from __future__ import annotations

import re
import sys
import shutil
import subprocess

import fitz

import build_guarded_criterion_publication as base


base.JP_CAPTIONS = {
    1: "GyroAuthは、現在のAuthentication Relationと、将来の評価に用いるCriterionのIntegrityを、関連しつつも別のProcessとして評価する。",
    2: "本提案は、Adaptive Authentication、Continuous Authentication、Drift対応、およびPoisoning-aware adaptationの交点に位置づけられる。",
    3: "Candidate生成とCandidate採用を分離する。Candidateを有効化するのはACCEPTのみである。",
    4: "Criterion StateとCriterion Update Responseは異なる。FREEZEはSubject Evaluationを必ずしも終了させず、適応経路を停止する。",
    5: "実装したP1 Scenarioでは、直接採用は攻撃参照値が許容されるまでCriterionを拡張した一方、Guard付き採用は許容前に適応を凍結した。",
    6: "AUTH_STABLE + FREEZEは、現在のAuthentication Relationを一時的に継続しながら、Criterion適応を禁止する状態を表す。AUTH_FAIL + ACCEPTは無効な組合せである。",
}

base.FIGURE_INSERTION_TARGETS = {
    1: r"^##\s+2\.",
    2: r"^##\s+3\.",
    3: r"^##\s+6\.",
    4: r"^##\s+7\.",
    5: r"^###\s+8\.3\b",
    6: r"^##\s+10\.",
}


FIGURE_WIDTHS = {
    1: 1.00,
    2: 0.88,
    3: 1.00,
    4: 0.82,
    5: 0.82,
    6: 0.78,
}


def parse_figure_source() -> list[base.FigureSpec]:
    """Parse each caption only through the next level-two section heading.

    The source contains publication-order documentation after Figure 6.  The
    base parser stopped only at ``## Rendering Notes``, which allowed that
    documentation to become part of the English Figure 6 caption.  A generic
    level-two-heading boundary keeps captions and documentation separate.
    """
    text = base.FIGURE_SOURCE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^## Figure\s+(\d+)\.\s+(.+?)\n\n"
        r"```mermaid\n(.*?)\n```\n\n"
        r"\*\*Caption:\*\*\s+(.+?)"
        r"(?=\n\n##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    specs = [
        base.FigureSpec(
            int(number),
            title.strip(),
            mermaid.strip() + "\n",
            caption.strip(),
        )
        for number, title, mermaid, caption in pattern.findall(text)
    ]
    if [spec.number for spec in specs] != [1, 2, 3, 4, 5, 6]:
        raise SystemExit("Expected Figure 1 through Figure 6 in Mermaid source")
    return specs


def latex_escape(text: str) -> str:
    """Escape caption text for raw LaTeX while preserving Unicode."""
    text = text.replace("`", "")
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def figure_markdown(number: int, lang: str) -> str:
    """Create a non-floating publication figure with explicit canonical numbering.

    Pandoc's implicit figure environment can defer a late figure differently
    between the English and Japanese documents. A centered, non-floating raw
    LaTeX block guarantees that every rendered PNG is included exactly where
    inserted and that source, artifact, caption, and PDF numbering remain equal.
    """
    specs = {spec.number: spec for spec in base.parse_figure_source()}
    caption = specs[number].caption_en if lang == "en" else base.JP_CAPTIONS[number]
    caption = latex_escape(caption)
    image = (base.BUILD_FIGURES / f"figure_{number}_tight.pdf").resolve().as_posix()
    width = FIGURE_WIDTHS[number]
    label = f"fig:guarded-criterion-{number}"
    figure_word = "Figure" if lang == "en" else "図"

    if number == 3:
        # Give the original left-to-right Figure 3 a dedicated landscape page.
        # pdflscape rotates the PDF page for on-screen reading and printing.
        return rf"""

```{{=latex}}
\clearpage
\begin{{landscape}}
\thispagestyle{{plain}}
\begin{{center}}
\hypertarget{{{label}}}{{}}
\includegraphics[width=0.96\linewidth,height=0.76\textheight,keepaspectratio]{{{image}}}

\vspace{{0.8em}}
{{\small\textbf{{{figure_word} {number}.}} {caption}}}
\end{{center}}
\end{{landscape}}
\clearpage
```

"""

    begin_container = r"\begin{minipage}{\linewidth}"
    end_container = r"\end{minipage}"
    return rf"""

```{{=latex}}
{begin_container}
\begin{{center}}
\hypertarget{{{label}}}{{}}
\includegraphics[width={width:.2f}\linewidth]{{{image}}}

\vspace{{0.4em}}
{{\small\textbf{{{figure_word} {number}.}} {caption}}}
\end{{center}}
{end_container}
```

"""


def insert_figures_in_publication_order(body: str, lang: str) -> str:
    """Insert Figure 1 through Figure 6 in canonical manuscript order."""
    for number in range(1, 7):
        target = re.compile(base.FIGURE_INSERTION_TARGETS[number], re.MULTILINE)
        match = target.search(body)
        if match is None:
            raise SystemExit(
                f"Could not find insertion target for Figure {number} in {lang} manuscript"
            )
        body = (
            body[: match.start()]
            + figure_markdown(number, lang)
            + body[match.start() :]
        )
    return body


_original_title_block = base.title_block


def title_block_with_graphics(meta: dict[str, str], lang: str) -> str:
    """Ensure raw LaTeX figure blocks have the graphicx command definitions."""
    if lang == "jp":
        meta = dict(meta)
        # Markdown hard break in Pandoc YAML title; avoid raw LaTeX in metadata.
        meta["title_jp"] = meta["title_jp"].replace("：", "：  \n", 1)
    block = _original_title_block(meta, lang)
    closing_front_matter = "\n---\n\n"
    header = "\nheader-includes:\n  - |\n      \\usepackage{graphicx}"
    header += "\n      " + r"\emergencystretch=2em"
    header += "\n      " + r"\usepackage{pdflscape}"
    if closing_front_matter not in block:
        raise SystemExit("Could not locate Pandoc metadata front matter terminator")
    if lang == "jp":
        header += (
            "\n      " + r"\newfontfamily\refnamelatin{DejaVu Serif}"
            + "\n      " + r"\newcommand{\referenceauthor}[1]{{\refnamelatin #1}}"
            + "\n      " + r"\makeatletter"
            + "\n      " + r"\renewcommand{\thesection}{\texttt{\number\c@section}}"
            + "\n      " + r"\renewcommand{\thesubsection}{\thesection.\texttt{\number\c@subsection}}"
            + "\n      " + r"\renewcommand{\thepage}{\texttt{\number\c@page}}"
            + "\n      " + r"\makeatother"
            + "\n      " + r"\let\gyroOriginalTOC\tableofcontents"
            + "\n      " + r"\renewcommand{\tableofcontents}{\begingroup\fontsize{9}{10}\selectfont\gyroOriginalTOC\endgroup}"
        )
    return block.replace(closing_front_matter, header + closing_front_matter, 1)



_original_normalize = base.normalize_submission_headings


def normalize_with_ascii_scenario_labels(text: str, lang: str) -> str:
    """Keep scenario identifiers N1/P1/C1 in Latin digits in Japanese headings/TOC."""
    normalized = _original_normalize(text, lang)
    if lang == "jp":
        normalized = re.sub(
            r"^(##)\s+(N1|P1|C1):",
            lambda m: f"{m.group(1)} " + r"\texttt{" + m.group(2) + "}:",
            normalized,
            flags=re.MULTILINE,
        )
    return normalized


def trim_figure_pdf_margins() -> None:
    for number in range(1, 7):
        src = base.BUILD_FIGURES / f"figure_{number}.pdf"
        dst = base.BUILD_FIGURES / f"figure_{number}_tight.pdf"
        doc = fitz.open(src)
        page = doc[0]
        shapes = [fitz.Rect(item['rect']) for item in page.get_drawings()]
        shapes = [r for r in shapes if not (r.width > page.rect.width * .95 and r.height > page.rect.height * .95)]
        shapes += [fitz.Rect(b[:4]) for b in page.get_text('blocks') if b[6] == 0]
        if not shapes:
            raise RuntimeError(f"Figure {number}: no visible content for trimming")
        bounds = shapes[0]
        for rect in shapes[1:]:
            bounds |= rect
        bounds = fitz.Rect(bounds.x0 - 10, bounds.y0 - 10, bounds.x1 + 10, bounds.y1 + 10) & page.rect
        page.set_cropbox(bounds)
        doc.save(dst, garbage=4, deflate=True)
        doc.close()

_original_render = base.render_figures

# Figure 4 uses a controlled Graphviz layout. All 7 states and 15 original
# transitions are preserved; long return edges do not constrain node ranks.
FIGURE_4_DOT = r"""
digraph CriterionUpdate {
  graph [rankdir=TB, bgcolor="white", nodesep=1.0, ranksep=1.25,
         splines=polyline, pad=0.25, outputorder=edgesfirst];
  node [shape=box, style="filled", fillcolor="#F3F3F3",
        color="#888888", fontname="DejaVu Sans", fontsize=15,
        margin="0.24,0.17"];
  edge [color="#777777", fontcolor="#222222",
        fontname="DejaVu Sans", fontsize=11, arrowsize=0.65];
  STABLE; ADAPTING; UNCERTAIN; FROZEN; UNDER_REVIEW;
  COMPROMISED; ROLLED_BACK;
  {rank=same; FROZEN; UNCERTAIN;}
  STABLE -> ADAPTING [label="ACCEPT"];
  STABLE -> UNCERTAIN [label="DEFER"];
  STABLE -> FROZEN [label="FREEZE"];
  STABLE -> UNDER_REVIEW [label="REVIEW", constraint=false];
  ADAPTING -> STABLE [label="validated ACCEPT", constraint=false];
  ADAPTING -> UNCERTAIN [label="DEFER"];
  ADAPTING -> FROZEN [label="FREEZE"];
  UNCERTAIN -> ADAPTING [label="supported candidate", constraint=false];
  UNCERTAIN -> UNDER_REVIEW [label="REVIEW-U", tailport=s, headport=ne];
  FROZEN -> UNDER_REVIEW [label="REVIEW-F", tailport=s, headport=nw];
  FROZEN -> ROLLED_BACK [label="ROLLBACK", constraint=false];
  COMPROMISED -> ROLLED_BACK [label="ROLLBACK"];
  UNDER_REVIEW -> STABLE [label="externally validated", constraint=false];
  UNDER_REVIEW -> COMPROMISED [label="contamination confirmed"];
  ROLLED_BACK -> STABLE [label="validated operation", constraint=false];
}
"""

def render_tight_figures() -> None:
    if shutil.which("dot") is None:
        raise SystemExit("Graphviz dot is required to render Figure 4")
    original_parser = base.parse_figure_source
    try:
        # Other five figures retain the established Mermaid renderer.
        base.parse_figure_source = lambda: [
            spec for spec in original_parser() if spec.number != 4
        ]
        _original_render()
    finally:
        base.parse_figure_source = original_parser

    dot_source = base.BUILD_FIGURES / "figure_4.dot"
    dot_source.write_text(FIGURE_4_DOT, encoding="utf-8")
    for suffix in ("svg", "png", "pdf"):
        output = base.BUILD_FIGURES / f"figure_4.{suffix}"
        command = ["dot", f"-T{suffix}", str(dot_source), "-o", str(output)]
        if suffix == "png":
            command.insert(1, "-Gdpi=220")
        subprocess.run(command, check=True)
        shutil.copy2(output, base.DIST_FIGURES / output.name)
    trim_figure_pdf_margins()

base.render_figures = render_tight_figures

base.parse_figure_source = parse_figure_source
base.figure_markdown = figure_markdown
base.insert_figures = insert_figures_in_publication_order
base.title_block = title_block_with_graphics
base.normalize_submission_headings = normalize_with_ascii_scenario_labels


if __name__ == "__main__":
    sys.exit(base.main())
