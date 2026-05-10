#!/usr/bin/env python3
"""Build Codex10k draft-batch pages, PDFs, and local email bodies from JSON."""

from __future__ import annotations

import csv
import html
import json
import os
import re
import sys
import textwrap
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
DATA = ROOT / "data" / "draft-batch-leads.json"
OUT_DIR = ROOT / "outputs" / "codex10k" / "draft-batch"
MANIFEST = OUT_DIR / "manifest.json"
OUTBOX_MD = ROOT / "docs" / "draft-batch-outbox.md"

INK = colors.HexColor("#142129")
MUTED = colors.HexColor("#5c6870")
BLUE = colors.HexColor("#235f91")
GREEN = colors.HexColor("#18704f")
GOLD = colors.HexColor("#c99a2f")
SOFT = colors.HexColor("#eef5f2")
LINE = colors.HexColor("#dfe5e2")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return value.strip("-")


def money(amount: int | float | str) -> str:
    number = int(float(amount))
    return f"USD {number:,}"


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def pdf_table(rows: list[list[str]], widths: list[float], style: ParagraphStyle) -> Table:
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


def html_page(lead: dict) -> str:
    visual = lead.get("visual_asset", "assets/baxter-website-qa-visual.png")
    steps = lead.get("workflow_steps") or [
        "Intake map",
        "Data check",
        "QA matrix",
        "Retest notes",
        "Handoff pack",
    ]
    deliverables = lead["deliverables"]
    fit_cards = lead.get("fit_cards") or [
        ["Narrow support", lead["fit"]],
        ["Works beside the primary team", lead["positioning"]],
        ["Data boundary", lead["boundary"]],
    ]
    pills = lead.get("pills") or [money(lead["price_usd"]) + " fixed", "sample data first", "no private data by email"]
    step_html = "\n".join(
        f'<span class="step"><small>{index:02d}</small><strong>{esc(step)}</strong></span>'
        for index, step in enumerate(steps[:5], 1)
    )
    deliverable_html = "\n".join(f"<li>{esc(item)}</li>" for item in deliverables)
    card_html = "\n".join(
        f"<article class=\"card\"><h3>{esc(title)}</h3><p>{esc(text)}</p></article>"
        for title, text in fit_cards
    )
    pill_html = "\n".join(f"<span class=\"pill {'primary' if index == 0 else ''}\">{esc(pill)}</span>" for index, pill in enumerate(pills))
    brand_initial = esc((lead["buyer"] or "C")[0].upper())
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{esc(lead['buyer'])} {esc(lead['offer_title'])}</title>
    <meta name="description" content="{esc(lead['meta_description'])}" />
    <style>
      :root {{
        color-scheme: light;
        --ink: #142129;
        --muted: #5c6870;
        --paper: #fbfaf5;
        --panel: #ffffff;
        --line: #dfe5e2;
        --blue: #235f91;
        --green: #18704f;
        --gold: #c99a2f;
        --soft: #eef5f2;
        --shadow: 0 22px 60px rgba(20, 33, 41, 0.15);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; background: var(--paper); color: var(--ink); }}
      a {{ color: inherit; }}
      .topbar {{
        position: sticky; top: 0; z-index: 20; display: flex; align-items: center; justify-content: space-between; gap: 18px;
        padding: 14px clamp(18px, 4vw, 56px); border-bottom: 1px solid var(--line);
        background: rgba(251, 250, 245, 0.94); backdrop-filter: blur(14px);
      }}
      .brand {{ display: flex; align-items: center; gap: 12px; text-decoration: none; }}
      .brand-mark {{ display: grid; place-items: center; width: 42px; height: 42px; border-radius: 8px; background: var(--ink); color: #fff; font-weight: 950; }}
      .brand strong, .brand span {{ display: block; }}
      .brand span {{ color: var(--muted); font-size: 0.86rem; }}
      nav {{ display: flex; flex-wrap: wrap; gap: 18px; color: var(--muted); font-weight: 720; }}
      nav a {{ text-decoration: none; }}
      .hero, .section {{ padding: clamp(34px, 6vw, 76px) clamp(18px, 5vw, 72px); }}
      .hero {{ display: grid; grid-template-columns: minmax(0, 0.94fr) minmax(340px, 1.06fr); gap: clamp(26px, 5vw, 64px); align-items: center; min-height: calc(100vh - 72px); }}
      .eyebrow {{ margin: 0 0 12px; color: var(--gold); font-size: 0.78rem; font-weight: 900; letter-spacing: 0.08em; text-transform: uppercase; }}
      h1 {{ max-width: 820px; margin: 0; font-size: 4.9rem; line-height: 0.96; letter-spacing: 0; }}
      .lede {{ max-width: 720px; margin: 24px 0 0; color: var(--muted); font-size: 1.18rem; line-height: 1.62; }}
      .price-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 26px; }}
      .pill {{ display: inline-flex; align-items: center; min-height: 42px; padding: 10px 14px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); color: var(--ink); font-weight: 850; }}
      .primary {{ background: var(--blue); color: #fff; }}
      .visual {{ position: relative; overflow: hidden; border: 1px solid rgba(20, 33, 41, 0.14); border-radius: 8px; background: #dfe9dc; box-shadow: var(--shadow); }}
      .visual img {{ display: block; width: 100%; height: auto; }}
      .workflow-strip {{ position: absolute; left: clamp(14px, 3vw, 30px); right: clamp(14px, 3vw, 30px); bottom: clamp(14px, 3vw, 28px); display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 7px; }}
      .step {{ position: relative; min-height: 78px; padding: 10px; border: 1px solid rgba(255, 255, 255, 0.42); border-radius: 8px; background: rgba(255, 255, 255, 0.86); box-shadow: 0 14px 34px rgba(20, 33, 41, 0.14); backdrop-filter: blur(12px); }}
      .step::before {{ content: ""; position: absolute; inset: -1px; border: 2px solid transparent; border-radius: inherit; animation: focusStep 10s linear infinite; pointer-events: none; }}
      .step:nth-child(2)::before {{ animation-delay: 2s; }}
      .step:nth-child(3)::before {{ animation-delay: 4s; }}
      .step:nth-child(4)::before {{ animation-delay: 6s; }}
      .step:nth-child(5)::before {{ animation-delay: 8s; }}
      .step small {{ display: block; color: var(--blue); font-size: 0.68rem; font-weight: 950; text-transform: uppercase; }}
      .step strong {{ display: block; margin-top: 6px; color: var(--ink); font-size: 0.72rem; line-height: 1.18; overflow-wrap: anywhere; }}
      .section {{ border-top: 1px solid var(--line); }}
      .section h2 {{ margin: 0 0 18px; font-size: 2.85rem; line-height: 1; letter-spacing: 0; }}
      .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
      .card {{ min-height: 168px; padding: 22px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); }}
      .card h3 {{ margin: 0 0 12px; font-size: 1.02rem; }}
      .card p, .scope-list li, .fineprint {{ color: var(--muted); line-height: 1.56; }}
      .scope-list {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px 28px; max-width: 960px; margin: 0; padding-left: 20px; }}
      .closing {{ display: grid; grid-template-columns: minmax(0, 0.72fr) minmax(280px, 0.28fr); gap: 26px; align-items: start; }}
      .quote {{ padding: 24px; border-radius: 8px; background: var(--ink); color: #fff; }}
      .quote strong {{ display: block; font-size: 2.4rem; line-height: 1; }}
      .quote span {{ display: block; margin-top: 12px; color: rgba(255, 255, 255, 0.78); line-height: 1.5; }}
      @keyframes focusStep {{ 0%, 16% {{ border-color: rgba(35, 95, 145, 0.95); box-shadow: 0 0 0 4px rgba(35, 95, 145, 0.13); }} 17%, 100% {{ border-color: transparent; box-shadow: none; }} }}
      @media (max-width: 940px) {{
        .hero, .closing {{ grid-template-columns: 1fr; }}
        .hero {{ min-height: auto; }}
        .grid, .scope-list {{ grid-template-columns: 1fr; }}
        .workflow-strip {{ position: static; grid-template-columns: 1fr; padding: 12px; background: #fff; }}
        .step {{ min-height: 70px; }}
        h1 {{ font-size: 3.85rem; }}
        .section h2 {{ font-size: 2.35rem; }}
      }}
      @media (max-width: 640px) {{
        nav {{ display: none; }}
        .brand span {{ display: none; }}
        h1 {{ font-size: 2.55rem; }}
        .section h2 {{ font-size: 2.1rem; }}
      }}
    </style>
  </head>
  <body>
    <header class="topbar">
      <a class="brand" href="#top" aria-label="{esc(lead['buyer'])} support packet">
        <span class="brand-mark">{brand_initial}</span>
        <span>
          <strong>{esc(lead['buyer'])}</strong>
          <span>{esc(lead['offer_title'])} from Nakul</span>
        </span>
      </a>
      <nav aria-label="Packet sections"><a href="#fit">Fit</a><a href="#workflow">Workflow</a><a href="#deliverables">Deliverables</a><a href="#next">Next step</a></nav>
    </header>
    <main id="top">
      <section class="hero" aria-labelledby="hero-title">
        <div>
          <p class="eyebrow">{esc(lead['eyebrow'])}</p>
          <h1 id="hero-title">{esc(lead['hero_title'])}</h1>
          <p class="lede">{esc(lead['lede'])}</p>
          <div class="price-row" aria-label="Proposal summary">{pill_html}</div>
        </div>
        <figure class="visual" aria-label="{esc(lead['offer_title'])} workflow preview">
          <img src="{esc(visual)}" alt="{esc(lead['visual_alt'])}" />
          <figcaption class="workflow-strip" id="workflow">{step_html}</figcaption>
        </figure>
      </section>
      <section class="section" id="fit"><h2>Fit</h2><div class="grid">{card_html}</div></section>
      <section class="section" id="deliverables"><h2>Deliverables</h2><ul class="scope-list">{deliverable_html}</ul></section>
      <section class="section" id="next">
        <div class="closing">
          <div>
            <h2>Next step</h2>
            <p class="fineprint">{esc(lead['next_step'])}</p>
            <p class="fineprint">Prepared by Nakul as an independent freelancer/sole proprietor. {esc(lead['exclusions'])}</p>
          </div>
          <aside class="quote" aria-label="Fixed price"><strong>${int(float(lead['price_usd'])):,}</strong><span>{esc(lead['quote_note'])}</span></aside>
        </div>
      </section>
    </main>
  </body>
</html>
"""


def build_pdf(lead: dict, pdf_path: Path) -> None:
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.32 * inch,
        bottomMargin=0.32 * inch,
        title=f"{lead['buyer']} {lead['offer_title']}",
        author="Nakul",
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=15.4, leading=17.7, textColor=INK, spaceAfter=3)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=9.6, leading=11, textColor=INK, spaceBefore=5, spaceAfter=3)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.25, leading=8.9, textColor=MUTED, spaceAfter=3.4)
    small = ParagraphStyle("Small", parent=body, fontSize=6.45, leading=7.7, textColor=INK)
    kicker = ParagraphStyle("Kicker", parent=body, fontName="Helvetica-Bold", fontSize=7.1, leading=8.3, textColor=GOLD, spaceAfter=2.5)
    white = ParagraphStyle("White", parent=body, fontName="Helvetica-Bold", fontSize=7.2, leading=8.6, textColor=colors.white)

    story = [
        paragraph(lead["eyebrow"].upper(), kicker),
        paragraph(lead["offer_title"], h1),
        paragraph(
            f"Prepared by Nakul as an independent freelancer/sole proprietor for {lead['buyer']}. {lead['positioning']} {lead['exclusions']}",
            body,
        ),
    ]

    summary = Table(
        [
            [paragraph("Buyer", white), paragraph(lead["buyer"], white)],
            [paragraph("Opportunity", white), paragraph(lead["opportunity"], white)],
            [paragraph("Package", white), paragraph(f"{money(lead['price_usd'])} fixed - {lead['offer_title']}", white)],
            [paragraph("Path", white), paragraph(lead.get("packet_path", lead["send_caution"]), white)],
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
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    visual_path = ROOT / lead.get("visual_asset", "")
    if visual_path.exists():
        visual = Image(str(visual_path), width=3.36 * inch, height=1.9 * inch)
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

    story.append(paragraph("Fit", h2))
    story.append(paragraph(lead["fit"], body))
    rows = [["Area", "Support deliverable"]]
    for index, item in enumerate(lead["deliverables"][:6], 1):
        rows.append([f"{index}", item])
    story.append(pdf_table(rows, [0.45 * inch, 6.45 * inch], small))
    story.append(paragraph("Boundary", h2))
    story.append(paragraph(lead["boundary"], body))
    note = Table(
        [[paragraph(f"Fixed price: {money(lead['price_usd'])}", white), paragraph(lead["next_step"], white)]],
        colWidths=[2.0 * inch, 4.9 * inch],
        hAlign="LEFT",
    )
    note.setStyle(
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
    story.append(Spacer(1, 6))
    story.append(KeepTogether(note))
    doc.build(story)


def email_body(lead: dict, public_url: str) -> str:
    deliverables = "\n".join(f"- {item}" for item in lead["deliverables"][:6])
    return "\n\n".join(
        [
            lead["greeting"],
            lead["opening"],
            f"I am Nakul, an independent freelancer/sole proprietor. {lead['positioning']}",
            f"Reference page:\n{public_url}",
            f"Attached package: {money(lead['price_usd'])} fixed.",
            f"The support slice would produce:\n\n{deliverables}",
            f"Boundary: {lead['boundary']}",
            lead["email_next_step"],
            "Best,\nNakul",
        ]
    ).strip()


def main() -> None:
    leads = json.loads(DATA.read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    outbox_lines = [
        "# Codex10k Draft Batch Outbox",
        "",
        "Prepared local packets for Gmail draft review. These are drafts only; do not send without explicit user approval.",
        "",
    ]

    for lead in leads:
        lead.setdefault("slug", slugify(f"{lead['lead_id']} {lead['buyer']}"))
        html_path = ROOT / f"{lead['slug']}.html"
        pdf_path = OUT_DIR / f"{lead['slug']}.pdf"
        email_path = OUT_DIR / f"{lead['slug']}.email.txt"
        page = html_page(lead)
        html_path.write_text(page)
        build_pdf(lead, pdf_path)
        public_url = f"https://anonymusk7.github.io/codex10k-workflow-recovery/{lead['slug']}.html?v=draft1"
        body = email_body(lead, public_url)
        email_path.write_text(body)
        entry = {
            "lead_id": lead["lead_id"],
            "buyer": lead["buyer"],
            "to": lead["email"],
            "cc": lead.get("cc", ""),
            "subject": lead["subject"],
            "slug": lead["slug"],
            "html_path": str(html_path.relative_to(ROOT)),
            "pdf_path": str(pdf_path.relative_to(ROOT)),
            "email_path": str(email_path.relative_to(ROOT)),
            "public_url": public_url,
            "source_url": lead["source_url"],
            "price_usd": lead["price_usd"],
            "send_caution": lead["send_caution"],
            "reply_message_id": lead.get("reply_message_id", ""),
            "draft_id": lead.get("draft_id", ""),
        }
        manifest.append(entry)
        outbox_lines.extend(
            [
                f"## {lead['lead_id']} {lead['buyer']}",
                "",
                f"- To: `{lead['email']}`",
                f"- Subject: {lead['subject']}",
                f"- Source: {lead['source_url']}",
                f"- Page: {public_url}",
                f"- PDF: `{entry['pdf_path']}`",
                f"- Price: {money(lead['price_usd'])}",
                f"- Caution: {lead['send_caution']}",
                "",
                "Body:",
                "",
                "```text",
                body,
                "```",
                "",
            ]
        )

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    OUTBOX_MD.write_text("\n".join(outbox_lines))
    print(MANIFEST)
    print(OUTBOX_MD)


if __name__ == "__main__":
    main()
