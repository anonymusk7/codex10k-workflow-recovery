#!/usr/bin/env python3
"""Generate the client-facing SoIN Tourism launch-QA support proposal PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "soin_launch_qa_support_proposal.pdf"
VISUAL = ROOT / "assets" / "synergy-automation-workflow-visual.png"


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
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
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
        bottomMargin=0.42 * inch,
        title="SoIN Tourism Launch QA Support Proposal",
        author="Nakul",
    )

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=11.7,
        textColor=MUTED,
        spaceAfter=5,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8,
        leading=10.5,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19.5,
        leading=22,
        textColor=INK,
        spaceAfter=5,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.4,
        leading=13.7,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
    )
    kicker = ParagraphStyle(
        "Kicker",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=8.1,
        leading=10.5,
        textColor=CORAL,
        spaceAfter=3,
    )
    white = ParagraphStyle(
        "White",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=8.3,
        leading=10.8,
        textColor=colors.white,
    )
    table_body = ParagraphStyle(
        "TableBody",
        parent=body,
        fontSize=7.8,
        leading=9.8,
        textColor=INK,
    )

    story = []
    hero = Image(str(VISUAL), width=7.05 * inch, height=1.58 * inch)
    hero.hAlign = "CENTER"
    story.append(hero)
    story.append(Spacer(1, 6))
    story.append(p("BOUNDED SUPPORT OPTION", kicker))
    story.append(p("SoIN Tourism CMS, CRM, and Partner Portal Launch QA", h1))
    story.append(
        p(
            "Prepared as a focused support slice for SoIN Tourism's public Website Services RFP. This is not a request for an individual pre-submission meeting and is not a full prime website redesign proposal.",
            body,
        )
    )

    summary = Table(
        [
            [p("Counterparty", white), p("SoIN Tourism / Clark-Floyd Counties Convention-Tourism Bureau", white)],
            [p("RFP fit", white), p("Website services, CMS, CRM system of record, and Partner Portal/Extranet launch risk", white)],
            [p("Package", white), p("USD 8,500 fixed launch-QA support package", white)],
            [p("Inputs", white), p("Staging site, priority journeys, dummy/test records, and selected vendor timeline", white)],
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
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(Spacer(1, 5))
    story.append(summary)

    story.append(p("RFP-Specific Risk Areas", h2))
    story.append(
        bullets(
            [
                "Partner Portal/Extranet flows where partners update listings, events, assets, and profile information while SoIN staff retain approval controls.",
                "CMS and CRM handoffs, including Simpleview transition assumptions and the new system-of-record workflow.",
                "AI readiness around structured content, metadata, schema, search visibility, and generative-search discoverability.",
                "High-use visitor, partner, staff-editor, form, mobile, redirect, analytics, and accessibility paths before launch.",
            ],
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Acceptance map", "Turn the RFP, FAQ, staging site, and priority journeys into a practical launch checklist."],
        ["Partner portal QA", "Test representative partner listing, event, asset, profile, approval, and staff-oversight flows."],
        ["Website QA", "Smoke test forms, redirects, metadata, schema, analytics, mobile, browser, and high-use visitor paths."],
        ["Accessibility pass", "Review representative templates and public journeys for practical WCAG-oriented issues."],
        ["Handoff", "Prioritized punch-list tracker, retest pass, editor guardrails, and 30-day regression checklist."],
    ]
    story.append(make_table(rows, [1.55 * inch, 5.25 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        bullets(
            [
                "No visitor, partner, or CRM production data is needed by email.",
                "Use public/staging pages and dummy/test records where possible.",
                "This support slice can serve SoIN directly or the selected vendor after award.",
                "This does not replace the full RFP response, website build, CRM selection, hosting, or ongoing maintenance scope.",
            ],
            body,
        )
    )

    story.append(
        KeepTogether(
            [
                p("Next Step", h2),
                p(
                    "If useful, reply with the expected staging or vendor-selection window. I will convert this support slice into a concise one-page scope with final acceptance criteria and payment terms.",
                    body,
                ),
                Spacer(1, 4),
                p("Reference: https://www.gosoin.com/request-for-proposals/", small),
            ]
        )
    )

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
