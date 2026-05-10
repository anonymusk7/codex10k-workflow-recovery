#!/usr/bin/env python3
"""Generate the Town of Duck website RFP support proposal PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "town_of_duck_launch_qa_sidecar_proposal.pdf"


INK = colors.HexColor("#13201f")
MUTED = colors.HexColor("#5e6e6a")
GREEN = colors.HexColor("#0a755d")
TEAL = colors.HexColor("#2299a8")
CORAL = colors.HexColor("#d86149")
SOFT = colors.HexColor("#eaf5f3")
MIST = colors.HexColor("#f2f7fb")
LINE = colors.HexColor("#d7e0dd")


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
        topMargin=0.42 * inch,
        bottomMargin=0.4 * inch,
        title="Town of Duck Website RFP Support Proposal",
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
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18.2,
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
    story.append(p("WEBSITE REDESIGN RFP SUBMISSION - TOWN OF DUCK", kicker))
    story.append(p("Limited Launch-QA, Accessibility, and CMS Handoff Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor for the Town of Duck website redesign and CMS implementation RFP. This is a narrow support proposal for QA evidence, migration spot checks, retest notes, and staff publishing guardrails. It is not a full redesign bid, legal certification, hosting proposal, CMS license, or long-term maintenance contract.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Town of Duck, North Carolina", white)],
            [p("RFP", white), p("Website Redesign and Content Management System Implementation", white)],
            [p("Package", white), p("USD 6,800 fixed launch-QA/accessibility/CMS handoff sidecar", white)],
            [p("Inputs", white), p("Priority pages, representative PDFs/forms/events, staging access after approval, and preferred tracker format", white)],
        ],
        colWidths=[1.25 * inch, 5.55 * inch],
        hAlign="LEFT",
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), GREEN),
                ("GRID", (0, 0), (-1, -1), 0.5, TEAL),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(Spacer(1, 8))
    story.append(summary)

    story.append(p("RFP-Specific Fit", h2))
    story.append(
        bullets(
            [
                "WCAG-oriented QA around templates, mobile views, keyboard path, focus, headings, labels, alt text, contrast, forms, and link purpose.",
                "Content migration spot checks for redirects, page titles, metadata, broken links, public documents, search results, and high-use resident/visitor paths.",
                "Issue register that separates found issues, remediated items, open risk, retest result, and likely owner.",
                "Staff publishing checklist for maintaining accessible pages, links, images, forms, calendar/event entries, and PDFs after launch.",
            ],
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Scope sample", "Agreed representative URLs, mobile views, public documents, forms, calendar/event views, and service paths."],
        ["Accessibility QA", "Automated scan triage plus manual verification for core WCAG-oriented risks and staff-created content patterns."],
        ["Migration readiness", "Spot checks for redirects, titles, metadata, document labels, search results, linked files, and broken-link risks."],
        ["Retest tracker", "Issue register with severity, evidence note, likely owner, status, retest result, and launch-readiness note."],
        ["Staff handoff", "Concise publishing checklist and support notes for non-technical staff maintaining accessible content."],
    ]
    story.append(make_table(rows, [1.55 * inch, 5.25 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        bullets(
            [
                "This is a QA, retest, and staff-handoff support package, not legal certification of ADA compliance.",
                "This does not include full redesign, CMS development, hosting, licensing, custom remediation, or long-term maintenance unless scoped separately.",
                "The work can support the Town directly or support the selected website/CMS vendor as an independent sidecar.",
                "No resident records, credentials, analytics exports, or internal Town files are needed by email.",
            ],
            body,
        )
    )

    note = Table(
        [[p("Fixed price: USD 6,800", white), p("Next step: confirm whether this limited sidecar is responsive, then share the issue-register template and staff checklist format before award discussions.", white)]],
        colWidths=[2.1 * inch, 4.7 * inch],
        hAlign="LEFT",
    )
    note.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), INK),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(Spacer(1, 7))
    story.append(KeepTogether(note))

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
