#!/usr/bin/env python3
"""Generate the Baxter State Park website RFP support proposal PDF."""

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
OUT = ROOT / "outputs" / "codex10k" / "baxter_website_launch_qa_sidecar_proposal.pdf"
VISUAL = ROOT / "assets" / "baxter-website-qa-visual.png"


INK = colors.HexColor("#15231f")
MUTED = colors.HexColor("#5c6b66")
PINE = colors.HexColor("#115f49")
BLUE = colors.HexColor("#2a6f9b")
CEDAR = colors.HexColor("#a5683f")
SOFT = colors.HexColor("#eef5ef")
LINE = colors.HexColor("#dfe6df")


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
        title="Baxter State Park Website Launch QA Support Proposal",
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
        fontSize=15.9,
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
        textColor=CEDAR,
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
    story.append(p("BAXTER STATE PARK WEBSITE DESIGN AND HOSTING RFP", kicker))
    story.append(p("Limited ADA, Migration, Performance, and Launch-Readiness QA Support", h1))
    story.append(
        p(
            "Prepared by Nakul as an independent freelancer/sole proprietor. This is a narrow support proposal for acceptance testing, evidence, retest notes, and staff handoff around Baxter State Park's published website design and hosting RFP. It is not a full design-prime proposal, hosting proposal, CMS license, legal accessibility certification, or long-term maintenance contract.",
            body,
        )
    )

    summary = Table(
        [
            [p("Buyer", white), p("Baxter State Park Authority", white)],
            [p("RFP", white), p("Design of a new website plus hosting and technical maintenance; electronic proposals due May 20, 2026", white)],
            [p("Package", white), p("USD 8,500 fixed launch QA, ADA-oriented checks, transition evidence, and staff handoff notes", white)],
            [p("Inputs", white), p("Public/current pages, approved staging access, proposed structure, representative ecommerce/forms/search paths, and preferred tracker format", white)],
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
            "The support slice focuses on launch-risk areas named in the RFP: approximately 45 unique pages, ecommerce, search, semantic tags, ADA Title II web and mobile accessibility, mobile-first responsiveness, UI/UX acceptance, CMS handoff, transition support, performance testing, owner-rights handoff, and staff-ready maintenance evidence.",
            body,
        )
    )

    story.append(p("Deliverables", h2))
    rows = [
        ["Area", "Support deliverable"],
        ["Acceptance checklist", "RFP-aligned checklist for ADA, mobile, ecommerce, search, content transition, CMS handoff, analytics readiness, performance, and owner-rights acceptance."],
        ["Issue register", "Severity, evidence note, reproduction detail, likely owner, remediation status, retest result, launch-readiness note, and open-risk summary."],
        ["ADA-oriented QA", "Manual checks for headings, keyboard path, focus, labels, alt text, contrast, link purpose, forms, document samples, semantic structure, and mobile paths."],
        ["Migration and launch QA", "Spot checks for priority pages, redirects, metadata, links, images, downloads, maps, news/posts, ecommerce paths, search, and high-use visitor flows."],
        ["Staff handoff", "Concise publishing guardrails for accessible pages, images, links, forms, downloadable files, announcements, embedded media, and future content updates."],
    ]
    story.append(make_table(rows, [1.45 * inch, 5.45 * inch], table_body))

    story.append(p("Boundaries", h2))
    story.append(
        p(
            "This supports BSP directly or the selected website/design/hosting vendor; it does not replace the full website provider. No visitor records, ecommerce exports, credentials, analytics exports, or private BSP files are requested by email. Hosting, CMS licensing, full custom development, legal accessibility certification, and ongoing technical maintenance are outside this fixed package unless separately scoped.",
            body,
        )
    )

    note = Table(
        [[p("Fixed price: USD 8,500", white), p("Next step: register this sender for addenda if the limited support slice can be considered, then confirm whether BSP wants the acceptance checklist and issue-register format before vendor selection discussions.", white)]],
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
