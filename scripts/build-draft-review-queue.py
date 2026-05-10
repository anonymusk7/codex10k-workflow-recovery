#!/usr/bin/env python3
"""Build a Codex10k draft review and close queue from the Gmail draft log."""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import UTC, datetime
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
MANIFEST = ROOT / "outputs" / "codex10k" / "draft-batch" / "manifest.json"
DRAFT_LOG = ROOT / "data" / "draft-email-log.csv"
OUT_MD = ROOT / "docs" / "draft-batch-review-queue.md"
OUT_PDF = ROOT / "outputs" / "codex10k" / "draft_batch_review_queue.pdf"

NEW_ORDER = ["C10K-090", "C10K-093", "C10K-092", "C10K-088", "C10K-085", "C10K-086", "C10K-089", "C10K-087", "C10K-084", "C10K-091"]
FOLLOW_ORDER = ["C10K-096", "C10K-099", "C10K-100", "C10K-095", "C10K-094", "C10K-098", "C10K-097", "C10K-101", "C10K-103", "C10K-102"]

RISK = {
    "C10K-090": "Strong direct-email nonprofit web RFP; local-firm preference means support-sidecar is cleaner than prime bid.",
    "C10K-093": "Strong direct-email nonprofit website RFP; buyer budget is CAD, while tracker records USD.",
    "C10K-092": "Good IIE fit, but full-service provider framing matters.",
    "C10K-088": "Good CRM migration QA lane; avoid platform-prime claims.",
    "C10K-085": "Procurement question to the inquiry contact; not a proposal.",
    "C10K-086": "Email path exists; questions deadline passed, so keep it as support component.",
    "C10K-089": "No licensed engineering claim; data/GIS support only.",
    "C10K-087": "Federal HRIS; slower, formal, no employee PII.",
    "C10K-084": "Mandatory vendor conference risk; eligibility question only.",
    "C10K-091": "Ontario/local vendor preference; support-sidecar only.",
    "C10K-096": "Highest follow-up value; procurement path likely controls.",
    "C10K-099": "High value but RFP deadline was tight; send only as courteous close/follow-up.",
    "C10K-100": "School website support; no student/family data by email.",
    "C10K-095": "K-12 routing data; formal path or selected-vendor path likely.",
    "C10K-094": "State park website support; ask for procurement path/addenda registration.",
    "C10K-098": "Municipal website RFP deadline tight; support-sidecar only.",
    "C10K-097": "Formal RFQ; avoid legal accessibility certification claims.",
    "C10K-101": "Commercial automation follow-up; quickest small close.",
    "C10K-103": "Agency pilot follow-up; quick close if they send a client-safe brief.",
    "C10K-102": "Small architecture pass; quick but low-dollar.",
}


def money(value: int | float) -> str:
    return f"USD {int(value):,}"


def status_label(log: dict) -> str:
    return "sent" if log.get("status") == "sent_from_draft" else "draft"


def load() -> tuple[list[dict], dict[str, dict]]:
    manifest = json.loads(MANIFEST.read_text())
    with DRAFT_LOG.open(newline="") as handle:
        logs = {row["lead_id"]: row for row in csv.DictReader(handle)}
    return manifest, logs


def table_rows(order: list[str], by_id: dict[str, dict], logs: dict[str, dict]) -> list[list[str]]:
    rows = [["Rank", "Lead", "Status", "Draft", "Price", "Recommendation"]]
    for index, lead_id in enumerate(order, 1):
        item = by_id[lead_id]
        log = logs[lead_id]
        rows.append(
            [
                str(index),
                f"{lead_id} - {item['buyer']}",
                status_label(log),
                log["draft_id"],
                money(item["price_usd"]),
                RISK[lead_id],
            ]
        )
    return rows


def write_md(manifest: list[dict], logs: dict[str, dict]) -> None:
    by_id = {item["lead_id"]: item for item in manifest}
    updated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    sent_count = sum(1 for log in logs.values() if log.get("status") == "sent_from_draft")
    draft_count = len(manifest) - sent_count
    lines = [
        "# Codex10k Draft Batch Review Queue",
        "",
        f"Updated: {updated_at}",
        "",
        f"This is a review queue for the 20 Gmail draft-batch packets. Sent: {sent_count}. Still draft-only: {draft_count}. Do not count any value here as revenue until completed and settled payment evidence exists in `data/ledger.csv`.",
        "",
        f"Total draft pipeline: {money(sum(item['price_usd'] for item in manifest))}.",
        "",
        "Payment close pack: `docs/draft-payment-close-pack.md` and `outputs/codex10k/draft_payment_close_pack.pdf`.",
        "",
        "## Recommended New-Draft Order",
        "",
        "| Rank | Lead | Status | Draft ID | Price | Why / Caution |",
        "| ---: | --- | --- | --- | ---: | --- |",
    ]
    for index, lead_id in enumerate(NEW_ORDER, 1):
        item = by_id[lead_id]
        log = logs[lead_id]
        lines.append(f"| {index} | {lead_id} {item['buyer']} | {status_label(log)} | `{log['draft_id']}` | {money(item['price_usd'])} | {RISK[lead_id]} |")
    lines.extend(
        [
            "",
            "## Recommended Follow-Up Order",
            "",
            "Follow-up drafts should generally wait until the user wants a manual follow-up cadence. They remain draft-only unless marked sent below.",
            "",
            "| Rank | Lead | Status | Draft ID | Price | Why / Caution |",
            "| ---: | --- | --- | --- | ---: | --- |",
        ]
    )
    for index, lead_id in enumerate(FOLLOW_ORDER, 1):
        item = by_id[lead_id]
        log = logs[lead_id]
        lines.append(f"| {index} | {lead_id} {item['buyer']} | {status_label(log)} | `{log['draft_id']}` | {money(item['price_usd'])} | {RISK[lead_id]} |")
    lines.extend(
        [
            "",
            "## Close Rule",
            "",
            "When a buyer replies positively, use `docs/revenue-close-desk.md` first. Ask for the exact billing/procurement path, then create a Stripe Payment Link, hosted Checkout Session, Stripe invoice, or manual invoice only after the buyer approves the exact scope.",
            "",
            "Ledger credit requires transaction ID, settlement or payout proof, actual fee evidence, direct-cost/refund evidence, and net-profit math.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n")


def write_pdf(manifest: list[dict], logs: dict[str, dict]) -> None:
    by_id = {item["lead_id"]: item for item in manifest}
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT_PDF), pagesize=letter, leftMargin=0.45 * inch, rightMargin=0.45 * inch, topMargin=0.35 * inch, bottomMargin=0.35 * inch)
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=16, leading=18, textColor=colors.HexColor("#142129"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=colors.HexColor("#142129"), spaceBefore=7)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=7.3, leading=8.7, textColor=colors.HexColor("#4f5f67"))
    small = ParagraphStyle("Small", parent=body, fontSize=6.35, leading=7.5)
    story = [
        Paragraph("Codex10k Draft Batch Review Queue", h1),
        Paragraph(f"20 Gmail draft-batch packets tracked. Sent: {sum(1 for log in logs.values() if log.get('status') == 'sent_from_draft')}. Verified net profit remains USD 0 until settled payment evidence exists.", body),
        Paragraph(f"Total draft pipeline: {money(sum(item['price_usd'] for item in manifest))}", body),
        Paragraph("Recommended New-Draft Order", h2),
    ]
    for title, order in [("new", NEW_ORDER), ("follow-up", FOLLOW_ORDER)]:
        if title == "follow-up":
            story.append(Paragraph("Recommended Follow-Up Order", h2))
            story.append(Paragraph("Follow-up drafts are ready, but most original messages were sent on May 10, 2026; use only when the user wants a manual follow-up cadence.", body))
        rows = table_rows(order, by_id, logs)
        wrapped = [[Paragraph(cell, small) for cell in row] for row in rows]
        table = Table(wrapped, colWidths=[0.35 * inch, 1.38 * inch, 0.38 * inch, 1.05 * inch, 0.68 * inch, 3.0 * inch], hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef5f2")),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#dfe5e2")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 4))
    story.append(Paragraph("Close Rule", h2))
    story.append(Paragraph("Use docs/revenue-close-desk.md for positive replies. Create a payment link or invoice only after buyer approval of scope, price, data boundary, and payment path. Count revenue only after settlement and actual fee evidence.", body))
    doc.build(story)


def main() -> None:
    manifest, logs = load()
    write_md(manifest, logs)
    write_pdf(manifest, logs)
    print(OUT_MD)
    print(OUT_PDF)


if __name__ == "__main__":
    main()
