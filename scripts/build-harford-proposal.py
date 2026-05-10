#!/usr/bin/env python3
"""Generate the HCPS routing data readiness and QA support PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "harford_routing_data_qa_support_question.pdf"
VISUAL = ROOT / "assets" / "harford-routing-qa-visual.png"

INK = colors.HexColor("#17232a")
MUTED = colors.HexColor("#5c6870")
BLUE = colors.HexColor("#245f91")
GREEN = colors.HexColor("#18704f")
GOLD = colors.HexColor("#d5a52f")
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
        title="HCPS Routing Data QA Support Question",
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
    story.append(p("HCPS RFP 26-SR-014 SUPPORT QUESTION", kicker))
    story.append(p("Limited Routing Data Readiness and Acceptance QA Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor. This is a narrow support question for routing data readiness, acceptance testing, GPS validation samples, issue tracking, and cutover evidence. It is not a bus routing software bid, GPS/fleet platform bid, implementation-prime proposal, legal/privacy advice, or ongoing system maintenance contract.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Harford County Public Schools", white)],
            [p("RFP", white), p("RFP 26-SR-014 Bus Routing, Fleet Management, GPS, and School Planning Solutions", white)],
            [p("Package", white), p("USD 9,500 fixed routing data readiness, acceptance QA, validation tracker, and cutover evidence support", white)],
            [p("Question", white), p("Can this limited support slice be considered directly, or should it be routed only through the selected routing/fleet/GPS vendor?", white)],
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
            "The support slice sits beside the core routing/fleet/GPS solution and focuses on acceptance evidence: route data quality, required-field ownership, GPS-to-route validation samples, exception scenarios, issue register discipline, training/cutover readiness, and executive-readable unresolved-risk notes.",
            body,
        )
    )

    rows = [
        ["Area", "Support deliverable"],
        ["Data readiness", "Checklist for route, stop, vehicle, school, schedule, eligibility, and export/import fields; duplicate/missing/invalid-value checks; and ownership rules."],
        ["Acceptance tests", "Scenarios for bell schedules, route exceptions, service changes, parent-facing outputs, reporting, and selected-vendor handoff criteria."],
        ["GPS validation", "Sample plan for device-to-route matching, stale signals, vehicle identifiers, timing variance, and route-completion evidence."],
        ["Issue register", "Severity, evidence, likely owner, remediation status, retest result, launch-risk note, and cutover readiness summary."],
        ["Privacy boundary", "No student names, home addresses, live route assignments, GPS logs, credentials, or internal exports requested by email; use sample or anonymized data first."],
    ]
    story.append(make_table(rows, [1.45 * inch, 5.45 * inch], table_body))

    note = Table(
        [[p("Fixed price: USD 9,500", white), p("Next step: confirm whether HCPS can consider this limited support slice directly, or whether it should be routed only through the selected routing/fleet/GPS vendor and the RFP's formal submission path.", white)]],
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
