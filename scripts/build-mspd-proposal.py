#!/usr/bin/env python3
"""Generate the MSPD case-management migration QA support-slice proposal PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "mspd_case_migration_qa_support_slice_proposal.pdf"
VISUAL = ROOT / "assets" / "mspd-case-migration-qa-visual.png"


INK = colors.HexColor("#16221f")
MUTED = colors.HexColor("#5e6d69")
GREEN = colors.HexColor("#0e7057")
NAVY = colors.HexColor("#153650")
BLUE = colors.HexColor("#27669f")
RED = colors.HexColor("#c96055")
SOFT = colors.HexColor("#eff7f2")
LINE = colors.HexColor("#d7e1dd")


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
        title="MSPD Case Management Migration QA Support Proposal",
        author="Nakul",
    )

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.35,
        leading=9,
        textColor=MUTED,
        spaceAfter=3.2,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=15.5,
        leading=17.8,
        textColor=INK,
        spaceAfter=3,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
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
        textColor=RED,
        spaceAfter=2.5,
    )
    white = ParagraphStyle(
        "White",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=7.15,
        leading=8.7,
        textColor=colors.white,
    )
    table_body = ParagraphStyle(
        "TableBody",
        parent=body,
        fontSize=6.55,
        leading=7.8,
        textColor=INK,
    )

    story = []
    story.append(p("RFP MSPD 0000000003SL / INTEGRATED PUBLIC DEFENSE MANAGEMENT SYSTEM", kicker))
    story.append(p("Migration QA, UAT Evidence, Reporting Readiness, and Stabilization Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor. This is a narrow support packet for the Missouri State Public Defender case-management modernization: legacy migration validation, requirements traceability, UAT scripts, defect retest, reporting readiness, cutover evidence, and stabilization handoff. It is not a full prime response, core platform offer, hosting commitment, security-certification claim, insurance representation, or legal/compliance certification.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Missouri State Public Defender", white)],
            [p("RFP", white), p("MSPD 0000000003SL; public summary says responses due June 30, 2026 at 5:00 PM Central through MissouriBUYS/MOVERS", white)],
            [p("Package", white), p("USD 28,500 fixed migration QA, UAT, reporting-readiness, cutover-evidence, and stabilization support slice", white)],
            [p("Inputs", white), p("Approved requirements, non-confidential mappings, sanitized samples, lower-environment evidence after approval, defect tracker, and reporting format", white)],
        ],
        colWidths=[0.72 * inch, 2.72 * inch],
        hAlign="LEFT",
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), GREEN),
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
            "Public summaries describe a statewide platform with case management, portals, document intelligence, analytics, integrations, workflow automation, HCL Notes/Domino migration, UAT, training, and stabilization. This slice strengthens the implementation evidence beside a compliant prime, without claiming to provide the core system, hosting, security certifications, court integrations, or statewide SaaS operations.",
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Migration QA workbook", "Source inventory, target mapping, field risk notes, sample reconciliation, exception categories, owner/status columns, and cutover blockers."],
        ["Traceability matrix", "Functional requirements mapped to build, migration, integration, reporting, test, training, evidence, and signoff status."],
        ["UAT script pack", "Scripts for intake, case assignment, attorney/client portals, documents, events, financials, reports, permissions, and notifications."],
        ["Defect retest register", "Severity, reproduction path, evidence, retest result, release risk, owner, and stabilization follow-up format."],
        ["Stabilization handoff", "Readiness register, launch checklist, known issues, training notes, support rhythm, and post-launch reporting checks."],
    ]
    story.append(make_table(rows, [1.45 * inch, 5.45 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        p(
            "This should move through MissouriBUYS/MOVERS, a qualified prime, subcontract, or formally approved procurement path. It should not be sent as casual outreach. No privileged case data, client records, credentials, production exports, or confidential MSPD files are requested by email. Core platform delivery, hosting, SOC 2/ISO certification, CJIS/HIPAA legal certification, insurance representation, Missouri supplier compliance, and full prime obligations are outside this fixed support package unless separately verified.",
            body,
        )
    )

    note = Table(
        [[p("Fixed price: USD 28,500", white), p("Next step: use this as a selected-prime/subcontract support packet or formally approved MOVERS response attachment, then confirm supplier registration, mandatory exhibits, insurance/security responsibilities, subcontract acceptance, and whether only sanitized or lower-environment evidence can be reviewed.", white)]],
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
