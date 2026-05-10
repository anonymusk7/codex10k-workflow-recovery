#!/usr/bin/env python3
"""Generate the Prince George's County parking data QA support PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "pgc_parking_data_qa_support_slice.pdf"
VISUAL = ROOT / "assets" / "pgc-parking-data-qa-visual.png"

INK = colors.HexColor("#142129")
MUTED = colors.HexColor("#5c6870")
BLUE = colors.HexColor("#235f91")
GREEN = colors.HexColor("#18704f")
GOLD = colors.HexColor("#c99a2f")
SOFT = colors.HexColor("#eef5f2")
LINE = colors.HexColor("#dfe5e2")


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
        title="Prince George's County Parking Data QA Support Slice",
        author="Nakul",
    )

    styles = getSampleStyleSheet()
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.45, leading=9.1, textColor=MUTED, spaceAfter=3.4)
    h1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=15.8, leading=18.2, textColor=INK, spaceAfter=3)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=9.6, leading=11, textColor=INK, spaceBefore=5, spaceAfter=3)
    kicker = ParagraphStyle("Kicker", parent=body, fontName="Helvetica-Bold", fontSize=7.2, leading=8.5, textColor=GOLD, spaceAfter=2.5)
    white = ParagraphStyle("White", parent=body, fontName="Helvetica-Bold", fontSize=7.25, leading=8.7, textColor=colors.white)
    table_body = ParagraphStyle("TableBody", parent=body, fontSize=6.65, leading=7.9, textColor=INK)

    story = []
    story.append(p("RVA-PMS-04-2026 SUPPORT SLICE", kicker))
    story.append(p("Limited Parking Data Migration and Integration Acceptance QA Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor. This is a narrow support proposal for data migration QA, integration acceptance, reporting QA, UAT evidence, and go-live readiness around the cloud-based parking management system RFP. It is not the full cloud PMS, hardware, LPR, enforcement platform, legal compliance, cyber insurance package, or ongoing maintenance contract.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Revenue Authority of Prince George's County", white)],
            [p("RFP", white), p("RVA-PMS-04-2026 Cloud-Based Parking Management System; electronic proposals due June 1, 2026", white)],
            [p("Package", white), p("USD 14,500 fixed parking data migration, integration acceptance, reporting QA, UAT, and go-live evidence support", white)],
            [p("Positioning", white), p("Support for the Revenue Authority, selected prime, or selected PMS vendor; not a full system or hardware bid", white)],
        ],
        colWidths=[0.72 * inch, 2.72 * inch],
        hAlign="LEFT",
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BLUE),
                ("GRID", (0, 0), (-1, -1), 0.5, GREEN),
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

    story.append(p("Fit", h2))
    story.append(
        p(
            "The support slice focuses on RFP risk areas that are data-heavy and evidence-heavy: migration reconciliation, LPR/payment/ERP/court/CRM/collections/DMV integration acceptance, payment and citation lifecycle edge cases, BI dashboards, revenue analysis, forecasting, spatial mapping, UAT scripts, training handoff, and launch readiness.",
            body,
        )
    )

    rows = [
        ["Area", "Support deliverable"],
        ["Migration reconciliation", "Checklist for citation, payment, permit, account, collections, location, status, and owner mappings; duplicate/under/over-payment cases; and sample reconciliation evidence."],
        ["Integration acceptance", "Matrix for LPR, payment, ERP/financial, court/Tyler, CRM/311, collections, DMV lookup, and reporting paths with expected behavior and retest status."],
        ["UAT and reporting QA", "Test scenarios for citation lifecycle, permits, payments, refunds, reporting, dashboards, forecasting, spatial views, data dictionary gaps, and operational handoff."],
        ["Issue register", "Severity, evidence, likely owner, remediation status, retest result, launch-risk note, and go-live readiness summary."],
        ["Data boundary", "No live citation records, license plates, payment data, DMV records, credentials, or enforcement exports requested by email; use sample or anonymized records first."],
    ]
    story.append(make_table(rows, [1.45 * inch, 5.45 * inch], table_body))

    note = Table(
        [[p("Fixed price: USD 14,500", white), p("Next step: if this support slice can be considered, register it as a narrow proposal beside the primary PMS vendor or route it to the selected prime/vendor after award. The package avoids production data over email.", white)]],
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
