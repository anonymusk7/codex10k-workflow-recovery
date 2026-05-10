#!/usr/bin/env python3
"""Generate the RRC STISS Salesforce QA support-slice proposal PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "rrc_salesforce_qa_support_slice_proposal.pdf"
VISUAL = ROOT / "assets" / "rrc-salesforce-qa-visual.png"


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
        title="RRC STISS Salesforce QA Support Proposal",
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
    story.append(p("RFO 455-26-1018 / SALESFORCE AND TOOLS IMPLEMENTATION SERVICES", kicker))
    story.append(p("Limited Salesforce QA, Migration Validation, UAT, and Handoff Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor. This is a narrow subcontractor/support packet for Railroad Commission of Texas RFO 455-26-1018: requirements traceability, Salesforce QA, data-migration checks, UAT evidence, release documentation, accessibility checks, and training handoff. It is not a full prime response, Texas authorization claim, HUB/VetHUB ownership claim, insurance representation, or long-term managed-services contract.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Railroad Commission of Texas", white)],
            [p("RFP", white), p("RFO 455-26-1018 STISS; responses due May 19, 2026 at 2:00 PM Central by email per RFO", white)],
            [p("Package", white), p("USD 22,500 fixed Salesforce QA/UAT, migration-validation, release-traceability, and handoff support slice", white)],
            [p("Inputs", white), p("Approved workorder requirements, non-confidential mappings, lower-environment access after approval, Jira/Copado workflow, and tracker format", white)],
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

    story.append(p("RFO-Specific Fit", h2))
    story.append(
        p(
            "Public RFO materials describe Salesforce and tools support across requirements, architecture, configuration/development, data migration, integrations, testing, UAT, accessibility, training, documentation, and release support. Workorder 1 centers on replacing the Texas Damage Reporting Form process in Salesforce. This slice strengthens delivery evidence beside a qualified prime, without claiming prime capacity.",
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Traceability matrix", "Requirements mapped to design, build, test, release, owner, status, evidence, and risk notes."],
        ["UAT script pack", "Scripts for external submissions, authenticated users, internal incident/docket processing, payments, letters, dashboards, and role access."],
        ["Migration QA pack", "Object/field mapping checks, data classification notes, reconciliation rules, duplicate handling, attachment checks, and exception log."],
        ["Release support", "Jira/Copado defect-retest register, dependency/risk log, release-readiness notes, and production-support transition checklist."],
        ["Training handoff kit", "Quick references, admin support notes, runbook gaps, known issues, and knowledge-transfer checklist."],
    ]
    story.append(make_table(rows, [1.45 * inch, 5.45 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        p(
            "This should move through a qualified prime, subcontract, or formally approved procurement path. It should not be sent as a casual procurement-content question because the written inquiry deadline has passed. No regulatory records, payment data, credentials, or confidential RRC files are requested by email. Texas business authorization, HUB/VetHUB HSP ownership, insurance representation, prime references, full delivery staffing, and long-term managed services are outside this fixed support package unless separately verified.",
            body,
        )
    )

    note = Table(
        [[p("Fixed price: USD 22,500", white), p("Next step: use this as a selected-prime/subcontract support packet or formally approved response attachment, then confirm Texas authorization, HSP/insurance responsibilities, subcontract acceptance, and whether lower-environment/sample artifacts can be reviewed without confidential records.", white)]],
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
