#!/usr/bin/env python3
"""Generate the Placer Court Power BI QA/UAT sidecar proposal PDF."""

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
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "codex10k" / "placer_powerbi_qa_uat_sidecar_proposal.pdf"
VISUAL = ROOT / "assets" / "placer-powerbi-qa-visual.png"


INK = colors.HexColor("#13211f")
MUTED = colors.HexColor("#5c6a67")
PINE = colors.HexColor("#0f7057")
BLUE = colors.HexColor("#245f9f")
CORAL = colors.HexColor("#c86555")
SOFT = colors.HexColor("#eef6f1")
LINE = colors.HexColor("#d9e2df")


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


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
        rightMargin=0.54 * inch,
        leftMargin=0.54 * inch,
        topMargin=0.32 * inch,
        bottomMargin=0.32 * inch,
        title="Placer Court Power BI QA/UAT Sidecar Proposal",
        author="Nakul",
    )

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.45,
        leading=9.1,
        textColor=MUTED,
        spaceAfter=3.4,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=15.8,
        leading=18.2,
        textColor=INK,
        spaceAfter=3,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=9.6,
        leading=11,
        textColor=INK,
        spaceBefore=5,
        spaceAfter=3,
    )
    kicker = ParagraphStyle(
        "Kicker",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=8.5,
        textColor=CORAL,
        spaceAfter=2.5,
    )
    white = ParagraphStyle(
        "White",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=7.25,
        leading=8.7,
        textColor=colors.white,
    )
    table_body = ParagraphStyle(
        "TableBody",
        parent=body,
        fontSize=6.65,
        leading=7.9,
        textColor=INK,
    )

    story = []
    story.append(p("SP-2026-0010 / POWER BI DEVELOPMENT SERVICES FOR PLACER COURT", kicker))
    story.append(p("Limited Power BI QA/UAT, Data Validation, and Handoff Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor. This is a narrow support packet for the Bonfire procurement path or a selected implementation vendor: dashboard acceptance testing, data-validation evidence, defect/retest tracking, documentation, and training handoff. It is not a full implementation-prime bid, vendor-of-record insurance package, Court licensing proposal, or long-term managed-services contract.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Superior Court of California, County of Placer", white)],
            [p("RFP", white), p("SP-2026-0010 Power BI Development Services; Bonfire close May 13, 2026 at 5:00 PM Pacific", white)],
            [p("Package", white), p("USD 18,500 fixed Power BI QA/UAT, data-validation, documentation, and handoff sidecar", white)],
            [p("Inputs", white), p("Dashboard inventory, approved definitions, sample/non-confidential extracts, staging workspace access after approval, and tracker format", white)],
        ],
        colWidths=[0.72 * inch, 2.72 * inch],
        hAlign="LEFT",
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PINE),
                ("GRID", (0, 0), (-1, -1), 0.5, BLUE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    if VISUAL.exists():
        visual = Image(str(VISUAL), width=3.36 * inch, height=1.9 * inch)
        top_grid = Table([[visual, summary]], colWidths=[3.46 * inch, 3.44 * inch], hAlign="LEFT")
        top_grid.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        story.append(Spacer(1, 5))
        story.append(top_grid)
    else:
        story.append(Spacer(1, 5))
        story.append(summary)

    story.append(p("RFP-Specific Fit", h2))
    story.append(
        p(
            "Public summaries describe roughly 20 existing Power BI dashboards, data consistency and reporting-efficiency goals, accessibility/readability improvements, and source consolidation from eCourt, Tyler jury, and other internal systems. This support slice focuses on the acceptance evidence that keeps dashboard modernization from becoming a subjective go-live decision.",
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Acceptance checklist", "Representative checks for totals, measures, slicers, date ranges, drilldowns, tooltips, refresh timing, layout, accessibility, and export behavior."],
        ["UAT script pack", "Role-based scripts with expected result, actual result, evidence, owner, status, and retest fields for each dashboard group."],
        ["Defect register", "Severity, source, screenshot/evidence note, likely owner, status, retest result, and release-readiness impact."],
        ["Data dictionary review", "Definitions, measure logic, source fields, transformation notes, owner assignments, and unresolved definition risks."],
        ["Handoff kit", "Dashboard owner checklist, support queue rules, training quick reference, governance notes, and final readiness summary."],
    ]
    story.append(make_table(rows, [1.45 * inch, 5.45 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        p(
            "This should move through Bonfire or a selected-vendor/subcontract path, not casual email outreach. No case records, jury records, personnel data, credentials, or confidential Court files are requested by email. Production data extraction, Court licensing, insurance/vendor-of-record requirements, full implementation staffing, and long-term managed services are outside this fixed support package unless separately approved.",
            body,
        )
    )

    note = Table(
        [[p("Fixed price: USD 18,500", white), p("Next step: use this as a portal-ready attachment or selected-vendor support packet, then confirm required Bonfire forms, insurance/vendor requirements, accepted subcontract structure, and whether sample dashboards can be reviewed without confidential records.", white)]],
        colWidths=[2.0 * inch, 4.9 * inch],
        hAlign="LEFT",
    )
    note.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), INK),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(Spacer(1, 6))
    story.append(KeepTogether(note))

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
