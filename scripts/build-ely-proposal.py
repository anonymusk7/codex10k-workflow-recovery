#!/usr/bin/env python3
"""Generate the Ely website migration QA support proposal PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "ely_migration_qa_launch_readiness_proposal.pdf"


INK = colors.HexColor("#13201d")
MUTED = colors.HexColor("#5d6d68")
PINE = colors.HexColor("#12674f")
LAKE = colors.HexColor("#267c9e")
BERRY = colors.HexColor("#cf664b")
SOFT = colors.HexColor("#edf6ef")
LINE = colors.HexColor("#d9e1db")


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
        title="Ely Website Migration QA Support Proposal",
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
        textColor=BERRY,
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
    story.append(p("WEBSITE DEVELOPMENT RFP - ELY AREA TOURISM BUREAU / ELY CHAMBER", kicker))
    story.append(p("Limited Migration QA, Directory Readiness, and Launch Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor. This is a narrow support proposal for the published Website Development & Content Migration RFP: Simpleview migration, business/member directory validation, SEO preservation, analytics checks, accessibility QA, staff publishing guardrails, and launch readiness. It is not a full redesign-prime proposal, hosting proposal, CMS license, legal accessibility certification, or ongoing maintenance contract.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Ely Area Tourism Bureau / Ely Chamber of Commerce", white)],
            [p("RFP", white), p("Website Development & Content Migration; proposal due May 11, 2026", white)],
            [p("Package", white), p("USD 12,500 fixed migration QA, directory readiness, and launch support slice", white)],
            [p("Inputs", white), p("Content inventory/crawl, representative listing export, staging access after approval, and preferred tracker format", white)],
        ],
        colWidths=[1.25 * inch, 5.55 * inch],
        hAlign="LEFT",
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PINE),
                ("GRID", (0, 0), (-1, -1), 0.5, LAKE),
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
                "Content inventory, redirect/SEO spot checks, metadata checks, media/link validation, and post-migration issue register.",
                "Business/member listing field review, template acceptance checks, tier/reporting validation, dashboard/admin-flow notes.",
                "Accessibility and mobile/browser QA across representative templates, forms, search, listings, navigation, and landing pages.",
                "Analytics verification, go-live checklist, staff publishing guardrails, retest notes, and short post-launch support.",
            ],
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Migration map", "Representative page/content inventory, redirect/SEO spot checks, metadata checks, internal-link checks, and broken-link risk notes."],
        ["Directory readiness", "Business listing field review, tier/template acceptance notes, reporting/export checks, and admin workflow observations."],
        ["QA pass", "WCAG-oriented, mobile, browser, search, form, analytics, CMS publishing, and launch-readiness checks."],
        ["Issue register", "Severity, evidence, likely owner, status, retest result, and launch-readiness note for each surfaced risk."],
        ["Staff handoff", "Concise publishing guardrails for pages, images, links, listings, forms, events, and post-launch content hygiene."],
    ]
    story.append(make_table(rows, [1.55 * inch, 5.25 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        bullets(
            [
                "This is a QA, directory-readiness, and launch-support package, not a complete prime agency website rebuild.",
                "This does not include hosting, CMS licensing, full custom development, legal accessibility certification, or long-term maintenance unless scoped separately.",
                "The work can support Ely directly or support the selected website/CMS vendor as an independent sidecar.",
                "No credentials, analytics exports, private member data, payment data, or internal Ely files are needed by email.",
            ],
            body,
        )
    )

    note = Table(
        [[p("Fixed price: USD 12,500", white), p("Next step: confirm whether this limited support slice is useful, then share the migration QA checklist and issue-register format before vendor selection discussions.", white)]],
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
