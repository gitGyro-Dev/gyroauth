#!/usr/bin/env python3
"""Build publication PDFs with canonical figure numbering aligned to placement order."""
from __future__ import annotations

import re
import sys

import build_guarded_criterion_publication as base


base.JP_CAPTIONS = {
    1: "GyroAuthは、現在のAuthentication Relationと、将来の評価に用いるCriterionのIntegrityを、関連しつつも別のProcessとして評価する。",
    2: "本提案は、Adaptive Authentication、Continuous Authentication、Drift対応、およびPoisoning-aware adaptationの交点に位置づけられる。",
    3: "Candidate生成とCandidate採用を分離する。Candidateを有効化するのはACCEPTのみである。",
    4: "Criterion StateとCriterion Update Responseは異なる。FREEZEはSubject Evaluationを必ずしも終了させず、適応経路を停止する。",
    5: "実装したP1 Scenarioでは、直接採用は攻撃参照値が許容されるまでCriterionを拡張した一方、Guard付き採用は許容前に適応を凍結した。",
    6: "AUTH_STABLE + FREEZEは、現在のAuthentication Relationを一時的に継続しながら、Criterion適応を禁止する状態を表す。",
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
    1: 0.95,
    2: 0.88,
    3: 0.95,
    4: 0.88,
    5: 0.82,
    6: 0.72,
}


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
    image = (base.BUILD_FIGURES / f"figure_{number}.png").resolve().as_posix()
    width = FIGURE_WIDTHS[number]
    label = f"fig:guarded-criterion-{number}"
    figure_word = "Figure" if lang == "en" else "図"

    return rf"""

```{{=latex}}
\begin{{center}}
\hypertarget{{{label}}}{{}}
\includegraphics[width={width:.2f}\linewidth]{{{image}}}

\vspace{{0.4em}}
{{\small\textbf{{{figure_word} {number}.}} {caption}}}
\end{{center}}
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
    block = _original_title_block(meta, lang)
    closing_front_matter = "\n---\n\n"
    header = "\nheader-includes:\n  - |\n      \\usepackage{graphicx}"
    if closing_front_matter not in block:
        raise SystemExit("Could not locate Pandoc metadata front matter terminator")
    return block.replace(closing_front_matter, header + closing_front_matter, 1)


base.figure_markdown = figure_markdown
base.insert_figures = insert_figures_in_publication_order
base.title_block = title_block_with_graphics


if __name__ == "__main__":
    sys.exit(base.main())
