#!/usr/bin/env python3
"""Generate a compact PDF close desk for the Codex10k revenue run."""

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
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "codex10k" / "codex10k_revenue_close_desk.pdf"

INK = colors.HexColor("#142129")
MUTED = colors.HexColor("#5b6870")
BLUE = colors.HexColor("#235f91")
GREEN = colors.HexColor("#18704f")
SOFT = colors.HexColor("#eef5f2")
LINE = colors.HexColor("#dfe5e2")


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def table(rows: list[list[str]], widths: list[float], style: ParagraphStyle) -> Table:
    wrapped = [[Paragraph(cell, style) for cell in row] for row in rows]
    result = Table(wrapped, colWidths=widths, hAlign="LEFT")
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return result


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.46 * inch,
        leftMargin=0.46 * inch,
        topMargin=0.32 * inch,
        bottomMargin=0.32 * inch,
        title="Codex10k Revenue Close Desk",
        author="Nakul",
    )

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=16.8, leading=19, textColor=INK, spaceAfter=4)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=12, textColor=INK, spaceBefore=7, spaceAfter=3)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.45, leading=9.2, textColor=MUTED, spaceAfter=3)
    small = ParagraphStyle("Small", parent=body, fontSize=6.55, leading=7.7, textColor=INK)
    white = ParagraphStyle("White", parent=body, fontName="Helvetica-Bold", fontSize=7.4, leading=8.8, textColor=colors.white)

    story = [
        p("Codex10k Revenue Close Desk", h1),
        p("Updated 2026-05-10T08:00:00Z. This is a conversion-control artifact, not revenue evidence. Verified net profit remains USD 0 until transaction and settlement evidence exists.", body),
    ]

    gate = Table(
        [[p("May 10 send gate", white), p("13 of 13 Gmail sends used. Do not send more email today unless the user explicitly raises the cap again. Future sends require the cadence script plus any stricter user-stated gap.", white)]],
        colWidths=[1.35 * inch, 5.75 * inch],
        hAlign="LEFT",
    )
    gate.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), INK),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(gate)

    story.append(p("Short-Cycle Close Priority", h2))
    story.append(
        table(
            [
                ["Lead", "Buyer", "Trigger", "Ask", "Asset"],
                ["C10K-007", "Bluestork / BygAI", "Phase 0 approval or payment-link request", "$1,200", "docs/bluestork-phase0-payment-request.md"],
                ["C10K-033", "GoodieX", "Selects first sales-lifecycle bottleneck", "$1,800", "docs/goodiex-v1-scope.md"],
                ["C10K-070", "SnipeAgent", "Confirms architecture pass", "$400", "snipeagent-sms-automation.html"],
                ["C10K-072", "Chek Creative", "Sends client-safe workflow brief", "$1,200", "chek-automation-partner-pilot.html"],
                ["C10K-069", "3D Walkabout", "Confirms HubSpot/ClickUp workflow open", "$1,800", "3dwalkabout-hubspot-clickup.html"],
                ["C10K-046", "Visualfestation", "Confirms integration v1", "$1,200", "visualfestation-integration.html"],
            ],
            [0.63 * inch, 1.25 * inch, 2.1 * inch, 0.62 * inch, 2.5 * inch],
            small,
        )
    )

    story.append(p("Procurement Close Priority", h2))
    story.append(
        table(
            [
                ["Lead", "Buyer", "Ask", "Reply Handling"],
                ["C10K-083", "Prince George's County Revenue Authority", "$14,500", "Clarify direct, prime, or post-award selected-vendor route."],
                ["C10K-075", "Ely Area Tourism Bureau", "$12,500", "Request payment/procurement path, export/crawl, staging timeline, tracker format."],
                ["C10K-079", "Hiawatha Academies", "$12,000", "Request staging/vendor timeline, language paths, payment path."],
                ["C10K-081", "Harford County Public Schools", "$9,500", "Follow HCPS instruction: formal path, vendor path, or informational only."],
                ["C10K-080", "Baxter State Park", "$8,500", "Register for addenda and confirm support-slice eligibility."],
                ["C10K-047", "SoIN Tourism", "$8,500", "Ask for CMS/CRM/portal priorities and proposal/payment path."],
                ["C10K-074", "Town of Duck", "$6,800", "Ask for priority pages, PDFs/forms/events, staging, tracker, payment path."],
                ["C10K-073", "NVTA", "$4,800", "Ask for priority URLs, PDF/document samples, tracker, remediation owner."],
            ],
            [0.63 * inch, 2.0 * inch, 0.68 * inch, 3.79 * inch],
            small,
        )
    )

    story.append(p("Payment Request Rule", h2))
    story.append(
        p(
            "Use Stripe Payment Links, hosted Checkout, or Stripe Invoice only after buyer approval of exact deliverables, exclusions, price, timeline, and data boundary. Do not collect card details directly, do not create a charge without buyer authorization, and do not count revenue until settlement and fee evidence exist.",
            body,
        )
    )

    story.append(p("Ledger Gate", h2))
    story.append(
        table(
            [
                ["Evidence Required Before Profit Credit"],
                ["Buyer approval message ID or signed acceptance; invoice/payment link URL or invoice PDF; transaction ID or charge/session/invoice ID; settlement or payout evidence; actual payment fee; direct costs/platform fees/refunds/disputes; final net-profit math in data/ledger.csv."],
            ],
            [7.1 * inch],
            small,
        )
    )

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
