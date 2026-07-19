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
            + base.figure_markdown(number, lang)
            + body[match.start() :]
        )
    return body


base.insert_figures = insert_figures_in_publication_order


if __name__ == "__main__":
    sys.exit(base.main())
