#!/usr/bin/env python3
"""Generate the client-facing NVTA ADA website QA sidecar quote PDF."""

from __future__ import annotations

import os
import sys
from pathlib import Path

BUNDLED_PYTHON = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "bin" / "python3"
if BUNDLED_PYTHON.exists() and Path(sys.executable).resolve() != BUNDLED_PYTHON.resolve():
    os.execv(str(BUNDLED_PYTHON), [str(BUNDLED_PYTHON), *sys.argv])

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "codex10k" / "nvta_ada_qa_sidecar_quote.pdf"
VISUAL = ROOT / "assets" / "nvta-ada-qa-visual.png"


INK = colors.HexColor("#13211d")
MUTED = colors.HexColor("#5d6f68")
FOREST = colors.HexColor("#0e684f")
CORAL = colors.HexColor("#d86443")
SOFT = colors.HexColor("#e8f3ef")
LINE = colors.HexColor("#d8dfdc")


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def bullets(items: list[str], style: ParagraphStyle) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        bulletFontName="Helvetica",
        bulletFontSize=7,
        leftIndent=16,
        bulletIndent=5,
    )


def make_table(rows: list[list[str]], widths: list[float], style: ParagraphStyle) -> Table:
    wrapped = [[Paragraph(cell, style) for cell in row] for row in rows]
    table = Table(wrapped, colWidths=widths, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.58 * inch,
        leftMargin=0.58 * inch,
        topMargin=0.36 * inch,
        bottomMargin=0.36 * inch,
        title="NVTA ADA Website QA Sidecar Quote",
        author="Nakul",
    )

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.1,
        leading=10.6,
        textColor=MUTED,
        spaceAfter=5,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=7.6,
        leading=9.6,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18.5,
        leading=21,
        textColor=INK,
        spaceAfter=5,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.8,
        leading=12.5,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
    )
    kicker = ParagraphStyle(
        "Kicker",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=9.5,
        textColor=CORAL,
        spaceAfter=3,
    )
    white = ParagraphStyle(
        "White",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=7.9,
        leading=9.7,
        textColor=colors.white,
    )
    table_body = ParagraphStyle(
        "TableBody",
        parent=body,
        fontSize=7.1,
        leading=8.6,
        textColor=INK,
    )

    story = []
    hero = Image(str(VISUAL), width=5.7 * inch, height=3.21 * inch)
    hero.hAlign = "CENTER"
    story.append(hero)
    story.append(Spacer(1, 6))
    story.append(p("LIMITED QUOTE / RFQ 26-R08", kicker))
    story.append(p("NVTA ADA Website QA Sidecar", h1))
    story.append(
        p(
            "Prepared as a limited independent quote for NVTA's public RFQ 26-R08, ADA Website Compliance. This package focuses on WCAG-oriented QA triage, manual spot checks, retest evidence, and a staff publishing checklist. It does not replace legal review or a full remediation/maintenance prime contractor.",
            body,
        )
    )

    summary = Table(
        [
            [p("Counterparty", white), p("Napa Valley Transportation Authority", white)],
            [p("RFQ", white), p("26-R08 / ADA Website Compliance for NVTA.ca.gov and VineTransit.com", white)],
            [p("Package", white), p("USD 4,800 fixed QA, retest, and staff checklist sidecar", white)],
            [p("Inputs", white), p("Priority URLs, representative PDFs/documents, preferred tracker format, and remediation owner", white)],
        ],
        colWidths=[1.25 * inch, 5.55 * inch],
        hAlign="LEFT",
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), FOREST),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2a7a69")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(Spacer(1, 5))
    story.append(summary)

    story.append(p("RFQ-Specific Fit", h2))
    story.append(
        bullets(
            [
                "Representative public pages and mobile views from NVTA.ca.gov and VineTransit.com.",
                "Manual checks around keyboard path, headings, labels, focus indicators, alt text, contrast, forms, and link purpose.",
                "Document/PDF sample review so staff can see recurring accessible-publishing risks.",
                "Retest notes that separate found issues, remediated issues, open risk, and staff-created content guardrails.",
            ],
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Scope sample", "Agreed representative URLs, mobile views, forms, and PDFs/documents for a fixed QA pass."],
        ["Automated triage", "Run automated checks, group likely issues, and remove obvious false positives from the action list."],
        ["Manual QA", "Keyboard, focus, labels, headings, alt text, contrast, link purpose, form, and PDF/document checks."],
        ["Retest tracker", "Issue register with severity, evidence note, owner/status field, retest result, and open-risk note."],
        ["Staff checklist", "Short publishing checklist for headings, links, images, PDF uploads, contrast, and pre-publish review."],
    ]
    story.append(make_table(rows, [1.55 * inch, 5.25 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        bullets(
            [
                "This is a QA and retest support quote, not legal certification of ADA compliance.",
                "This does not include full code remediation, CMS development, hosting, or long-term maintenance unless scoped separately.",
                "Public pages and representative documents are enough; no rider, HR, analytics, credential, or internal system data is needed by email.",
                "The package can support NVTA directly or a selected remediation vendor as an independent sidecar.",
            ],
            body,
        )
    )

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
