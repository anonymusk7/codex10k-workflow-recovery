#!/usr/bin/env python3
"""Build a close/payment readiness pack for the Codex10k Gmail draft batch."""

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
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "codex10k" / "draft-batch" / "manifest.json"
PROSPECTS = ROOT / "data" / "prospects.csv"
OUT_MD = ROOT / "docs" / "draft-payment-close-pack.md"
OUT_PDF = ROOT / "outputs" / "codex10k" / "draft_payment_close_pack.pdf"

ORDER = [
    "C10K-090",
    "C10K-093",
    "C10K-092",
    "C10K-088",
    "C10K-085",
    "C10K-086",
    "C10K-089",
    "C10K-087",
    "C10K-084",
    "C10K-091",
    "C10K-096",
    "C10K-099",
    "C10K-100",
    "C10K-095",
    "C10K-094",
    "C10K-098",
    "C10K-097",
    "C10K-101",
    "C10K-103",
    "C10K-102",
]

PAYMENT_PATH = {
    "C10K-090": "Invoice or Stripe link after SVDP confirms local/support-sidecar eligibility.",
    "C10K-093": "Invoice or Stripe link after THRIVE confirms USD/CAD billing preference.",
    "C10K-092": "Invoice/PO after IIE confirms support slice can be considered.",
    "C10K-088": "Invoice/PO after Springfield confirms CRM QA support path.",
    "C10K-085": "No payment link until Connecticut APA confirms procedure and recipient.",
    "C10K-086": "No payment link until MCCS confirms support-component eligibility.",
    "C10K-089": "Invoice/PO only after Hillsborough confirms data/GIS support path.",
    "C10K-087": "Federal procurement/subcontract path first; no casual payment link.",
    "C10K-084": "Eligibility first because vendor conference may control participation.",
    "C10K-091": "Invoice or Stripe link only after NHS confirms non-local support role is acceptable.",
    "C10K-096": "Invoice/PO or selected-prime path after PGC confirms support route.",
    "C10K-099": "Invoice or buyer-approved payment link if Ely still wants migration QA support.",
    "C10K-100": "Invoice/PO after Hiawatha confirms website QA support path.",
    "C10K-095": "Formal path or selected-vendor path after Harford responds.",
    "C10K-094": "Invoice/PO only after Baxter confirms addenda/procurement path.",
    "C10K-098": "Invoice/PO after Duck confirms support-sidecar path.",
    "C10K-097": "Formal RFQ/payment path only; avoid legal certification framing.",
    "C10K-101": "Stripe Payment Link/Checkout is acceptable after one workflow is confirmed.",
    "C10K-103": "Stripe Payment Link/Checkout after Chek sends one client-safe brief.",
    "C10K-102": "Stripe Payment Link/Checkout after architecture pass approval.",
}


def money(value: int | float) -> str:
    return f"USD {value:,.2f}".replace(".00", "")


def fee_estimate(gross: int | float) -> tuple[float, float]:
    fee = round(gross * 0.029 + 0.30, 2)
    return fee, round(gross - fee, 2)


def collection_terms(price: int) -> str:
    if price < 4800:
        return "100% upfront"
    return "50% kickoff / 50% acceptance or buyer PO terms"


def load() -> tuple[list[dict], dict[str, dict]]:
    manifest = json.loads(MANIFEST.read_text())
    with PROSPECTS.open(newline="") as handle:
        prospects = {row["lead_id"]: row for row in csv.DictReader(handle)}
    by_id = {item["lead_id"]: item for item in manifest}
    ordered = [by_id[lead_id] for lead_id in ORDER]
    return ordered, prospects


def write_md(items: list[dict], prospects: dict[str, dict]) -> None:
    updated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    lines = [
        "# Codex10k Draft Payment Close Pack",
        "",
        f"Updated: {updated_at}",
        "",
        "Use this only after a buyer positively replies or asks for payment. No invoice, Stripe link, Checkout Session, or charge should be created until the buyer approves the exact scope, price, data boundary, and payment path.",
        "",
        "Stripe best-practice note: use Payment Links, hosted Checkout, or Stripe Invoicing for one-time payments. Do not collect card details directly and do not use legacy Charges/Sources/Card Element flows.",
        "",
        "## Ledger Rule",
        "",
        "Nothing in this pack is revenue evidence. Add revenue to `data/ledger.csv` only after settlement evidence exists with transaction ID, actual processor/platform fees, direct costs, refunds/disputes, and net-profit math.",
        "",
        "## Fast Use",
        "",
        "1. Buyer replies yes or asks how to pay.",
        "2. Confirm billing name/email, exact scope, exclusions, timeline, data boundary, and approval owner.",
        "3. Use the row below to choose Stripe Payment Link/Checkout, Stripe Invoice, manual invoice, PO, or selected-vendor path.",
        "4. Send only the approved payment URL or invoice.",
        "5. Update `data/ledger.csv` only after settlement evidence is complete.",
        "",
        "## Close Matrix",
        "",
        "| Lead | Buyer | Amount | Card Fee Est. | Net Before Costs | Collection | Payment Path |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for item in items:
        price = int(item["price_usd"])
        fee, net = fee_estimate(price)
        lines.append(
            f"| {item['lead_id']} | {item['buyer']} | {money(price)} | {money(fee)} | {money(net)} | {collection_terms(price)} | {PAYMENT_PATH[item['lead_id']]} |"
        )
    lines.extend(["", "## Buyer Approval Reply Skeleton", "", "```text"])
    lines.extend(
        [
            "Hi {{name}},",
            "",
            "Great, I can start once the payment path is approved and the agreed sample inputs are available.",
            "",
            "Scope: {{scope}}",
            "Price: {{amount}} fixed",
            "Collection: {{collection_terms}}",
            "Payment path: {{payment_link_or_invoice_or_po_path}}",
            "Timeline: {{timeline}} after payment/PO approval and input availability",
            "",
            "Please confirm the billing name/email, approval owner, and whether you prefer Stripe-hosted card payment, Stripe invoice, manual invoice, or procurement/PO handling.",
            "",
            "No production credentials or private records need to be sent by email for the first checklist; dummy, redacted, or buyer-approved secure workspace inputs are fine.",
            "",
            "Best,",
            "Nakul",
        ]
    )
    lines.extend(["```", ""])
    lines.extend(["## Per-Lead Close Notes", ""])
    for item in items:
        prospect = prospects.get(item["lead_id"], {})
        price = int(item["price_usd"])
        fee, net = fee_estimate(price)
        lines.extend(
            [
                f"### {item['lead_id']} {item['buyer']}",
                "",
                f"- Draft ID: `{item['draft_id']}`",
                f"- Offer: {prospect.get('offer', 'Fixed-scope support slice')}",
                f"- Status: {prospect.get('status', 'draft_created')}",
                f"- Amount: {money(price)}",
                f"- Planning-only card fee estimate: {money(fee)}; estimated net before direct costs: {money(net)}",
                f"- Collection terms: {collection_terms(price)}",
                f"- Payment path: {PAYMENT_PATH[item['lead_id']]}",
                f"- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.",
                f"- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines))


def write_pdf(items: list[dict]) -> None:
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=landscape(letter),
        leftMargin=0.35 * inch,
        rightMargin=0.35 * inch,
        topMargin=0.3 * inch,
        bottomMargin=0.3 * inch,
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=15, leading=17, textColor=colors.HexColor("#142129"))
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=6.6, leading=7.7, textColor=colors.HexColor("#43525a"))
    cell = ParagraphStyle("Cell", parent=body, fontSize=5.75, leading=6.65)
    story = [
        Paragraph("Codex10k Draft Payment Close Pack", h1),
        Paragraph("Use only after buyer approval. No payment link, invoice, Checkout Session, or charge before exact scope, price, data boundary, and payment path are approved. Ledger credit requires settled transaction evidence and actual fee math.", body),
        Spacer(1, 5),
    ]
    rows = [["Lead", "Buyer", "Amount", "Fee Est.", "Net Est.", "Collection", "Payment Path"]]
    for item in items:
        price = int(item["price_usd"])
        fee, net = fee_estimate(price)
        rows.append(
            [
                item["lead_id"],
                item["buyer"],
                money(price),
                money(fee),
                money(net),
                collection_terms(price),
                PAYMENT_PATH[item["lead_id"]],
            ]
        )
    wrapped = [[Paragraph(str(value), cell) for value in row] for row in rows]
    table = Table(wrapped, colWidths=[0.55 * inch, 1.35 * inch, 0.72 * inch, 0.65 * inch, 0.72 * inch, 1.25 * inch, 4.45 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef5f2")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dfe5e2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2.4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 5))
    story.append(Paragraph("Card-fee estimates assume 2.9% + USD 0.30 only for planning. Replace with actual evidence before ledger credit.", body))
    doc.build(story)


def main() -> None:
    items, prospects = load()
    write_md(items, prospects)
    write_pdf(items)
    print(OUT_MD)
    print(OUT_PDF)


if __name__ == "__main__":
    main()
