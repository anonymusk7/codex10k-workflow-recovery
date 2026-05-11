#!/usr/bin/env python3
"""Build Codex10k May 11 prep-only proposal packets."""

from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

BUNDLED_PYTHON = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "bin" / "python3"
if BUNDLED_PYTHON.exists() and Path(sys.executable).resolve() != BUNDLED_PYTHON.resolve():
    os.execv(str(BUNDLED_PYTHON), [str(BUNDLED_PYTHON), *sys.argv])

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "codex10k" / "may11-prep-batch"
MANIFEST = OUT_DIR / "manifest.json"
OUTBOX = ROOT / "docs" / "may11-prep-batch.md"
PROSPECTS = ROOT / "data" / "prospects.csv"
BUILDER_PATH = ROOT / "scripts" / "build-draft-batch.py"
BOUNTY_MD = ROOT / "docs" / "authorized-bounty-pr-lane.md"

spec = importlib.util.spec_from_file_location("draft_builder", BUILDER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {BUILDER_PATH}")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def make_visuals() -> None:
    from PIL import Image, ImageDraw, ImageFont

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(exist_ok=True)
    font_regular = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19)
    font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 25)
    font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
    font_node = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)

    specs = {
        "boston-iam-uat-visual.png": ("IAM support evidence pack", "#255f85", ["Requirements", "Controls", "UAT"], ["Matrix", "Plan", "Proof"], ["Scope", "Controls", "Tests", "Risks", "Handoff"]),
        "stcloud-erp-data-visual.png": ("ERP conversion readiness", "#2f6f94", ["Finance", "HR", "Interfaces"], ["UAT", "Cutover", "Appendix"], ["Inventory", "Risks", "Scripts", "Cutover", "Memo"]),
        "sanantonio-library-digital-visual.png": ("Digital library launch QA", "#7a5a32", ["Patrons", "Search", "Accounts"], ["Accessibility", "Admin UAT", "Evidence"], ["Journeys", "WCAG", "Search", "Admin", "Report"]),
        "wssc-gis-ecm-visual.png": ("GIS and records task-order starter", "#2b7a5e", ["GIS", "ECM", "BIM"], ["Use cases", "Risks", "Staffing"], ["Use cases", "Data", "Records", "Risks", "Appendix"]),
        "stpete-pension-fitgap-visual.png": ("Pension workflow fit-gap", "#6d5b8e", ["Members", "Documents", "Reports"], ["Fit gap", "Demo", "Risks"], ["Functions", "Data", "Workflow", "Demo", "Plan"]),
        "gssm-cms-security-visual.png": ("CMS security response pack", "#316b9f", ["CMS", "Hosting", "Support"], ["Security", "WCAG", "KPIs"], ["Inventory", "Security", "WCAG", "Support", "Copy"]),
        "nisd-web-compliance-visual.png": ("District web compliance sidecar", "#2f6f94", ["SOW", "SFTP", "Auth"], ["Matrices", "FERPA", "QA"], ["SOW", "Security", "FERPA", "Pricing", "Portal"]),
        "njtransit-od-qa-visual.png": ("Rail O-D survey data QA", "#255f85", ["Survey", "Counts", "Stations"], ["Schema", "Dashboard", "Handoff"], ["Schema", "Clean", "Weights", "Dash", "Memo"]),
        "make-salesforce-activecampaign-visual.png": ("Salesforce and ActiveCampaign repair", "#2b7a70", ["Salesforce", "Make", "ActiveCampaign"], ["Dedupe", "Alerts", "Runbook"], ["Audit", "Map", "Fix", "Alerts", "Tests"]),
        "notion-adalo-sync-visual.png": ("Notion to Adalo sync v1", "#7a5aa6", ["Notion", "Make", "Adalo"], ["Upserts", "Logs", "Docs"], ["Schema", "Direction", "Upsert", "Errors", "Docs"]),
        "typebot-airtable-ai-visual.png": ("Typebot Airtable AI rescue", "#8a5d32", ["Typebot", "OpenAI", "Airtable"], ["403 fix", "Flow", "Scopes"], ["Tokens", "Flow", "Write", "Errors", "Guide"]),
    }

    for filename, (title, accent, left, right, nodes) in specs.items():
        img = Image.new("RGB", (1200, 675), "#f8f6ee")
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((56, 48, 1144, 627), radius=26, fill="#ffffff", outline="#dfe5e2", width=2)
        draw.rounded_rectangle((92, 88, 1108, 150), radius=18, fill="#eef5f2")
        draw.ellipse((124, 112, 138, 126), fill="#e86f55")
        draw.ellipse((151, 112, 165, 126), fill="#e8b94d")
        draw.ellipse((178, 112, 192, 126), fill="#4b9f72")
        draw.text((224, 106), title, fill="#142129", font=font_bold)
        for x, label, items in [(96, "Inputs", left), (806, "Outputs", right)]:
            draw.rounded_rectangle((x, 196, x + 298, 520), radius=20, fill="#fbfaf5", outline="#dfe5e2", width=2)
            draw.text((x + 28, 224), label, fill=accent, font=font_bold)
            for idx, item in enumerate(items):
                y = 286 + idx * 66
                draw.rounded_rectangle((x + 28, y, x + 270, y + 42), radius=12, fill="#ffffff", outline="#dfe5e2", width=2)
                draw.rectangle((x + 28, y, x + 36, y + 42), fill=accent)
                draw.text((x + 52, y + 11), item, fill="#142129", font=font_regular)
        xs = [430, 512, 594, 676, 758]
        y = 342
        for idx, (x, node) in enumerate(zip(xs, nodes)):
            if idx:
                draw.line((xs[idx - 1] + 54, y + 34, x, y + 34), fill=accent, width=5)
                draw.polygon([(x - 3, y + 34), (x - 16, y + 26), (x - 16, y + 42)], fill=accent)
            draw.rounded_rectangle((x, y, x + 74, y + 68), radius=17, fill="#ffffff", outline=accent, width=3)
            draw.text((x + 37, y + 22), node, fill="#142129", font=font_node, anchor="ma")
        draw.rounded_rectangle((426, 450, 774, 526), radius=18, fill="#142129")
        draw.text((600, 471), "bounded support before full commitment", fill="#ffffff", font=font_small, anchor="ma")
        img.save(assets_dir / filename)


def lead(
    lead_id: str,
    buyer: str,
    channel: str,
    source_url: str,
    subject: str,
    segment: str,
    opportunity: str,
    problem: str,
    offer_title: str,
    hero_title: str,
    eyebrow: str,
    lede: str,
    fit: str,
    positioning: str,
    boundary: str,
    exclusions: str,
    price: int,
    visual: str,
    steps: list[str],
    deliverables: list[str],
    cards: list[list[str]],
    next_step: str,
    quote_note: str,
    price_label: str,
    greeting: str,
    opening: str,
    email_next_step: str,
    send_caution: str,
    response_path: str,
    email: str = "",
) -> dict:
    return {
        "lead_id": lead_id,
        "buyer": buyer,
        "email": email,
        "channel": channel,
        "source_url": source_url,
        "subject": subject,
        "segment": segment,
        "opportunity": opportunity,
        "problem_hypothesis": problem,
        "offer_title": offer_title,
        "hero_title": hero_title,
        "eyebrow": eyebrow,
        "meta_description": f"Prepared support packet for {buyer}: {offer_title}.",
        "lede": lede,
        "fit": fit,
        "positioning": positioning,
        "boundary": boundary,
        "exclusions": exclusions,
        "price_usd": price,
        "pills": [price_label.split(";")[0], "support slice", "no private data by email"],
        "visual_asset": f"assets/{visual}",
        "visual_alt": f"Workflow visual for {offer_title}.",
        "workflow_steps": steps,
        "deliverables": deliverables,
        "fit_cards": cards,
        "next_step": next_step,
        "quote_note": quote_note,
        "price_label": price_label,
        "greeting": greeting,
        "opening": opening,
        "email_next_step": email_next_step,
        "send_caution": send_caution,
        "response_path": response_path,
        "packet_path": response_path,
    }


LEADS = [
    lead(
        "C10K-111",
        "City of Boston - Identity and Access Management Managed Services",
        "Boston Supplier Portal packet",
        "https://content.boston.gov/bid-listings/ev00017196",
        "IAM managed services support appendix for EV00017196",
        "IAM UAT and proposal readiness",
        "Boston DoIT is procuring Identity and Access Management Managed Services through EV00017196.",
        "A prime bidder can use a compact UAT/control-evidence appendix to strengthen implementation readiness without overclaiming prime IAM capacity.",
        "IAM proposal readiness and UAT evidence pack",
        "IAM acceptance evidence before managed-services handoff",
        "Boston IAM procurement support",
        "I can package the requirements trace, control evidence, UAT scripts, and implementation-readiness appendix a prime team can attach to the formal IAM managed services response.",
        "The official bid listing is active through May 26, 2026 and routes proposals through Boston's Supplier Portal.",
        "This is a specialist support appendix beside a qualified IAM managed-services prime or a portal response if eligibility is confirmed.",
        "No credentials, tenant exports, employee records, or security-sensitive configuration should be sent by email. Use dummy scenarios or an approved secure workspace.",
        "This is not an IAM managed-services prime bid, legal compliance certification, SOC report, or cybersecurity warranty.",
        4800,
        "boston-iam-uat-visual.png",
        ["Requirements", "Controls", "UAT scripts", "Risk matrix", "Appendix"],
        [
            "Requirements-to-acceptance matrix for core IAM managed-services obligations",
            "Implementation and test-plan outline with role, access, and break-glass scenarios",
            "UAT checklist covering provisioning, deprovisioning, MFA, role changes, and reporting",
            "Security and compliance response draft language for a prime team's review",
            "Issue/risk register with owner, severity, evidence, and closure criteria",
            "Five-day support appendix package ready for formal team review",
        ],
        [["Why this slice", "IAM projects fail in acceptance evidence, not only tool selection."], ["Buyer-safe boundary", "No live tenant details or credentials are needed for the first pack."], ["Route", "Use the Supplier Portal or prime/subcontract path only."]],
        "Use as a Boston Supplier Portal attachment or prime/subcontract support appendix after confirming eligibility and required forms.",
        "Fixed support appendix for a qualified team, subject to procurement eligibility.",
        "USD 4,800 fixed; subject to portal or prime/subcontract eligibility",
        "Hello,",
        "I saw Boston's EV00017196 IAM managed-services procurement and prepared a narrow support appendix focused on UAT and implementation-readiness evidence.",
        "If this support slice is eligible, the first input would be the prime response outline and any public/non-sensitive requirements matrix.",
        "Portal-only for buyer submission. Gmail only for procedural clarification to the named contact, not sales outreach.",
        "Boston Supplier Portal or approved prime/subcontract path",
    ),
    lead(
        "C10K-112",
        "City of St. Cloud - ERP Software and Implementation Services",
        "OpenGov portal packet",
        "https://govtribe.com/opportunity/state-local-contract-opportunity/enterprise-resource-planning-erp-software-and-implementation-services-2026027",
        "ERP data conversion and UAT readiness sidecar",
        "ERP data migration and UAT",
        "St. Cloud is procuring ERP software and implementation services for finance, HR/payroll, procurement, data conversion, interfaces, testing, and go-live support.",
        "ERP implementation risk is concentrated in conversion inventory, interface assumptions, UAT coverage, and cutover evidence.",
        "ERP data conversion and UAT readiness sidecar",
        "ERP conversion risk turned into testable evidence",
        "St. Cloud ERP readiness",
        "I can turn the ERP implementation scope into a conversion inventory, interface risk log, UAT script pack, cutover checklist, and proposal appendix for the implementation team.",
        "The posted opportunity is active through June 9, 2026 and points to electronic procurement through OpenGov.",
        "This is a support slice beside an ERP implementation prime, or a formal portal component only if eligibility and forms are confirmed.",
        "No payroll, employee, vendor, bank, or HR records should be sent by email; use schema-only exports, dummy records, or an approved workspace.",
        "This is not a full ERP software bid, accounting advice, HR compliance advice, hosting package, or managed implementation prime proposal.",
        5500,
        "stcloud-erp-data-visual.png",
        ["Inventory", "Interfaces", "UAT pack", "Cutover", "Appendix"],
        [
            "Conversion inventory worksheet for finance, HR, payroll, procurement, and assets",
            "Interface risk log for inbound/outbound systems, owners, cadence, and failure modes",
            "UAT script pack with role, data, pass/fail evidence, and retest fields",
            "Cutover checklist with freeze, validation, rollback, and first-payroll safeguards",
            "Proposal appendix language for migration, testing, and launch-readiness controls",
            "Open decisions list for the ERP prime and City project team",
        ],
        [["High-risk lane", "Data conversion and UAT are usually where ERP launches lose trust."], ["Prime-friendly", "The pack strengthens an implementation response without pretending to be the ERP platform."], ["Data-safe first", "A schema-only start avoids payroll or HR data exposure."]],
        "Use only through the St. Cloud OpenGov path or with an approved ERP prime/subcontract route.",
        "Fixed support slice, subject to buyer/prime approval and final contracting.",
        "USD 5,500 fixed; support slice only",
        "Hello,",
        "I prepared a focused ERP data-conversion and UAT readiness packet for the St. Cloud ERP procurement.",
        "If this support slice is eligible, the first input would be the public requirements list, target ERP modules, and schema-only migration inventory.",
        "Portal-only to the agency. Gmail is appropriate only for approved ERP vendor/prime teaming outreach.",
        "St. Cloud OpenGov portal or approved ERP prime/subcontract path",
    ),
    lead(
        "C10K-113",
        "City of San Antonio Public Library - Digital Experience Redesign",
        "SAePS portal packet",
        "https://webapp1.sanantonio.gov/BidContractOpps/Content.aspx?id=6163&page=Default",
        "SAPL digital library accessibility and launch acceptance test pack",
        "Digital library launch QA",
        "San Antonio Public Library seeks a library-specific Platform as a Service solution for the Digital Library through RFCSP 26-029 / RFx 6100019598.",
        "The most useful support slice is acceptance evidence across patron journeys, accessibility, search, account flows, and admin workflows.",
        "Digital library accessibility and launch acceptance test pack",
        "Digital library launch proof for patrons, staff, and accessibility",
        "SAPL digital library QA",
        "I can build the test matrix and launch evidence pack around patron search, account workflows, accessibility, and admin UAT so the new digital library can be accepted cleanly.",
        "The official city posting lists a May 18, 2026 deadline and directs vendors to the SAePS portal.",
        "This is a specialist launch-acceptance support pack beside the PaaS vendor or as a formal portal component if eligible.",
        "No patron records, library account data, staff credentials, or restricted analytics should be sent by email. Use public catalog examples or approved test accounts.",
        "This is not the PaaS platform, library ILS contract, legal accessibility certification, hosting package, or long-term managed service.",
        9500,
        "sanantonio-library-digital-visual.png",
        ["Journeys", "WCAG pass", "Search QA", "Admin UAT", "Evidence"],
        [
            "Patron journey test matrix for discovery, account, holds, renewals, digital resources, and help paths",
            "Keyboard, screen-reader, contrast, focus, and mobile checks for priority templates",
            "Search/navigation acceptance tests with expected results and failure notes",
            "Admin workflow UAT scripts for content updates, resource changes, and help escalation",
            "Launch readiness report with blocker severity, retest status, and go/no-go summary",
            "Staff handoff checklist for routine checks after launch",
        ],
        [["Public impact", "Digital-library failures hit patrons immediately, especially mobile and accessibility paths."], ["Vendor support", "The pack helps the selected PaaS/vendor team show acceptance evidence."], ["Strict route", "San Antonio procurement rules mean portal-only handling."]],
        "Use through SAePS or with the selected/prime vendor after confirming communication and submission rules.",
        "Fixed support pack, subject to SAePS or vendor eligibility.",
        "USD 9,500 fixed; portal/vendor support only",
        "Hello,",
        "I saw the SAPL Digital Experience Redesign solicitation and prepared a narrow launch-acceptance and accessibility QA support pack.",
        "If this support role is eligible, the first input would be public patron journeys and the draft implementation/launch plan.",
        "Portal-only. Do not Gmail or cold-email outside listed solicitation communication rules.",
        "SAePS portal or approved selected-vendor/prime path",
    ),
    lead(
        "C10K-114",
        "WSSC Water - GIS and Engineering Records Document Management Support",
        "OpenGov portal packet",
        "https://procurement.opengov.com/portal/wsscwater/projects/256299",
        "GIS and ECM task-order starter support pack",
        "GIS, ECM, and engineering records",
        "WSSC Water is procuring GIS and Engineering Records Document Management Support through an OpenGov opportunity.",
        "The first value is a task-order starter pack that maps likely use cases, data/workflow risks, and staffing evidence for a BOA response.",
        "GIS/ECM readiness and task-order starter pack",
        "GIS and engineering records support before BOA task orders arrive",
        "WSSC GIS/ECM support",
        "I can prepare a support appendix that maps GIS, ECM, engineering records, eBuilder, Primavera, BIM, SQL/cloud migration, and workflow risks into task-order-ready evidence.",
        "The public opportunity is active through May 29, 2026 and routes action through OpenGov.",
        "This is a support appendix beside a qualified BOA prime or formal portal component only if eligibility is confirmed.",
        "No utility engineering records, maps with sensitive infrastructure, credentials, or nonpublic project files should be sent by email.",
        "This is not a BOA prime bid, licensed engineering service, engineering judgment, utility security assessment, or records-retention legal opinion.",
        3500,
        "wssc-gis-ecm-visual.png",
        ["Use cases", "Data map", "Records risk", "Staffing", "Appendix"],
        [
            "Three likely task-order use cases with scope, data needs, acceptance evidence, and handoff notes",
            "GIS/ECM data and workflow risk register for engineering records and project systems",
            "Draft staffing/responsibility matrix for GIS, document management, and workflow support",
            "Cloud/SQL migration and integration assumptions list for prime review",
            "Ten-page technical support appendix outline for a formal BOA response",
            "Open questions checklist for OpenGov or prime-team clarification",
        ],
        [["BOA-ready", "The work turns broad support language into concrete task-order evidence."], ["Sensitive data boundary", "Infrastructure records stay out of email and public artifacts."], ["Prime-aware", "The packet supports, rather than replaces, a qualified BOA response."]],
        "Use through WSSC OpenGov or an approved prime/subcontract channel after confirming eligibility and communication rules.",
        "Fixed readiness pack, subject to formal procurement or prime approval.",
        "USD 3,500 fixed; BOA support slice only",
        "Hello,",
        "I prepared a narrow GIS/ECM task-order starter packet for the WSSC Water engineering records support opportunity.",
        "If this support slice is eligible, the first input would be the public RFP sections and any non-sensitive task-order priorities.",
        "Portal-only for buyer. Gmail only for approved teaming outreach to likely primes.",
        "WSSC OpenGov portal or approved prime/subcontract path",
    ),
    lead(
        "C10K-115",
        "City of St. Petersburg - Pension Management Software",
        "OpenGov portal packet",
        "https://procurement.opengov.com/portal/stpete",
        "Pension software data and workflow fit-gap sprint",
        "Pension SaaS fit-gap and workflow QA",
        "St. Petersburg is procuring pension management software with workflow, document management, data import/export, reporting, audit trail, and member portal needs.",
        "A fit-gap and demo-script pack can help evaluate vendor responses and surface migration/reporting risk before award.",
        "Pension data and workflow fit-gap sprint",
        "Pension workflow risk mapped before vendor demo decisions",
        "St. Pete pension fit-gap",
        "I can convert the pension software functional areas into a fit-gap matrix, migration/reporting risk log, demo-script checklist, and sample implementation schedule.",
        "The public opportunity points to OpenGov submission with a May 26, 2026 deadline.",
        "This is an evaluation/support slice for the City project team or a pension SaaS implementation team, not a software-product bid.",
        "No member records, pension calculations, bank data, beneficiary data, credentials, or personnel data should be sent by email.",
        "This is not actuarial advice, legal benefit advice, pension administration software, hosting, or a full implementation prime proposal.",
        2800,
        "stpete-pension-fitgap-visual.png",
        ["Functions", "Data risk", "Workflow", "Demo script", "Schedule"],
        [
            "Functional fit-gap matrix for activity tracking, member portal, documents, reports, and audit trail",
            "Migration risk log for import/export fields, history depth, attachments, and validation checks",
            "Workflow QA checklist for approvals, notices, document handling, and exception states",
            "Vendor demo script with must-show scenarios and pass/fail evidence fields",
            "Sample implementation schedule with discovery, build, test, parallel run, and go-live checks",
            "Open issues memo for procurement or implementation-team review",
        ],
        [["Decision aid", "Fit-gap evidence helps avoid buying software that looks good only in a demo."], ["Privacy boundary", "Pension member data stays inside approved systems."], ["Fast lane", "A five-day support sprint can finish before deeper procurement decisions."]],
        "Use through the St. Petersburg OpenGov process or with an approved pension software vendor/prime.",
        "Fixed fit-gap support sprint, subject to approval and data boundary review.",
        "USD 2,800 fixed; support/evaluation slice only",
        "Hello,",
        "I prepared a focused pension software fit-gap and workflow QA packet for the St. Petersburg RFP lane.",
        "If this support slice is eligible, the first input would be the public functional requirements and a dummy demo scenario set.",
        "Portal-only to the agency. Procedural email only if permitted by the solicitation.",
        "St. Petersburg OpenGov portal or approved vendor/prime path",
    ),
    lead(
        "C10K-116",
        "South Carolina Governor's School for Science and Mathematics",
        "South Carolina procurement packet",
        "https://apps.sceis.sc.gov/SCSolicitationWeb/solicitationAttachment.do?solicitnumber=5400028226",
        "CMS support and accessibility/security response pack",
        "School website CMS and security response",
        "SC GSSM has a live website redesign/CMS/support solicitation with accessibility, security questionnaire, support, and maintenance needs.",
        "The support lane is a response pack around CMS support, security evidence mapping, WCAG plan, integration inventory, and redacted-copy QA.",
        "CMS support and accessibility/security response pack",
        "CMS support evidence for a school website response",
        "SC GSSM web support",
        "I can prepare a security questionnaire evidence map, WCAG support plan, integration/test matrix, support KPI template, and redacted-copy QA checklist for the website/CMS response.",
        "The official SC procurement attachment page is active for solicitation 5400028226, with a June 10, 2026 due date reported in the packet research.",
        "This is a support appendix beside a qualified web/CMS prime or formal portal component if vendor registration and forms are confirmed.",
        "No student, parent, applicant, donor, staff, credential, or nonpublic security data should be sent by email.",
        "This is not a hosting contract, full redesign prime bid, legal accessibility certification, student-data compliance opinion, or cybersecurity certification.",
        5900,
        "gssm-cms-security-visual.png",
        ["Inventory", "Security map", "WCAG plan", "Support KPIs", "Redacted copy"],
        [
            "Security questionnaire evidence map for CMS, hosting, access control, backups, and incident response",
            "WCAG support plan with sample checks, cadence, exception handling, and ownership model",
            "Integration inventory and test matrix for forms, calendars, media, analytics, and authentication",
            "Monthly support KPI template for tickets, response, fixes, audits, and releases",
            "Redacted-copy QA checklist for public procurement posting",
            "Decision log for hosting, support, custom development, and maintenance assumptions",
        ],
        [["Procurement fit", "Security and accessibility response details are material, not garnish."], ["School-safe data", "No student or staff data is needed to prepare the first packet."], ["Durable support", "KPI templates help the buyer compare ongoing support promises."]],
        "Use only through the South Carolina procurement path or an approved web/CMS prime route after forms are confirmed.",
        "Fixed support pack, subject to portal eligibility and final scope.",
        "USD 5,900 fixed; response-support slice only",
        "Hello,",
        "I prepared a CMS support and accessibility/security response packet for the SC GSSM website solicitation.",
        "If this support slice is eligible, the first input would be the public RFP attachment set and the response structure.",
        "Portal-only. Email only for formal procurement questions, not sales outreach.",
        "South Carolina procurement portal or approved web/CMS prime path",
    ),
    lead(
        "C10K-117",
        "Northside Independent School District - District Web Services",
        "Bonfire/Euna portal packet",
        "https://media.governmentnavigator.com/media/bid/1776452898_4_17_2026-2026-070.pdf",
        "District web RFP compliance and portal package QA",
        "District web compliance support",
        "Northside ISD issued RFP 2026-070 for District Web Design, Development, and Implementation Services through Bonfire/Euna.",
        "A tight compliance sidecar can help a web prime complete the SOW questionnaire, accessibility/security matrix, FERPA/data-transfer checklist, and portal package QA.",
        "District web RFP compliance sidecar",
        "School web proposal evidence before the portal clock runs out",
        "NISD web RFP sidecar",
        "I can prepare the SOW response matrix, accessibility/security evidence map, data-transfer/FERPA checklist, pricing narrative skeleton, and portal package QA checklist.",
        "The public RFP copy lists a May 13, 2026 opening and requires portal upload through Bonfire/Euna.",
        "This is a support sidecar for a qualified district web prime or formal portal package if eligibility, references, and forms are already in place.",
        "No student, family, staff, SFTP, authentication, district account, or private website data should be sent by email.",
        "This is not a full district web platform bid, FERPA legal opinion, hosting proposal, school communications platform, or long-term managed services contract.",
        7500,
        "nisd-web-compliance-visual.png",
        ["SOW matrix", "Security", "FERPA", "Pricing", "Portal QA"],
        [
            "Statement-of-work response matrix aligned to required web, CMS, implementation, and support questions",
            "Accessibility/security response matrix with evidence requests and unknowns",
            "Data-transfer and FERPA-aware checklist for SFTP, authentication, exports, and role-based publishing",
            "Pricing narrative skeleton separating platform, implementation, support, and optional services",
            "Portal package QA checklist for required PDFs/XLS files, signatures, forms, and attachments",
            "Submission readiness memo with blockers, missing references, and nonresponsive-risk flags",
        ],
        [["Deadline-sensitive", "The portal deadline is close, so the value is package readiness, not broad redesign."], ["Prime support", "Useful beside a qualified school web vendor with references already in hand."], ["Strict communication", "No contact outside authorized procurement rules."]],
        "Use only with an approved district web prime or through Bonfire/Euna if all required forms and eligibility are ready.",
        "Fixed compliance-support sidecar, subject to portal eligibility and schedule reality.",
        "USD 7,500 fixed; portal/prime support only",
        "Hello,",
        "I prepared a narrow district web RFP compliance sidecar for Northside ISD RFP 2026-070.",
        "If this support slice is eligible, the first input would be the prime response draft and required-document checklist.",
        "Portal-only. No Gmail outreach during procurement evaluation.",
        "NISD Bonfire/Euna portal or approved district web prime path",
    ),
    lead(
        "C10K-118",
        "NJ TRANSIT - Rail Origin-Destination Survey",
        "Bid Express support packet",
        "https://www.njtransit.com/procurement/calendar/",
        "O-D survey data QA and dashboard prototype support",
        "Transportation survey data QA",
        "NJ TRANSIT lists RFP 0000234 for NEC/NJCL/RVL Rail Origin-Destination Survey 2025/2026 due through Bid Express.",
        "A subconsultant support slice can cover schema QA, cleaning rules, dashboard wireframes, and field-to-analysis handoff evidence.",
        "O-D survey data QA and dashboard prototype",
        "Rail survey data that survives cleaning, weighting, and handoff",
        "NJ TRANSIT survey QA",
        "I can prepare a data QA and dashboard prototype packet for a qualified survey/planning prime: schema checks, cleaning rules, weighting risks, and analysis handoff.",
        "NJ TRANSIT's procurement calendar lists the RFP due May 19, 2026 through Bid Express.",
        "This is a data QA subconsultant/support slice beside a qualified survey/planning firm, not a survey-prime proposal.",
        "No rider personal data, raw survey responses, location traces, or nonpublic operational datasets should be sent by email.",
        "This is not licensed transportation planning, statistical certification, field survey staffing, DBE/SBE certification, or a full RFP prime response.",
        3200,
        "njtransit-od-qa-visual.png",
        ["Schema", "Clean rules", "Weight risks", "Dashboard", "Handoff"],
        [
            "Survey schema QA checklist for route, station, time, trip purpose, transfers, and demographics fields",
            "Cleaning and validation rules for duplicates, impossible trips, missing values, and inconsistent station names",
            "Nonresponse and weighting risk checklist for planner/statistician review",
            "Dashboard wireframes for line, station pair, corridor, and survey-completion views",
            "Field-to-analysis handoff plan with data dictionary and QA evidence fields",
            "Prime-team memo with assumptions, exclusions, and next data decisions",
        ],
        [["Subconsultant lane", "The support is useful to a qualified survey/planning prime."], ["Data evidence", "Cleaning and handoff proof is a concrete deliverable, not a generic analytics promise."], ["Privacy boundary", "No raw personal survey records outside approved systems."]],
        "Use only as a prime/subconsultant support attachment or through Bid Express if eligibility is confirmed.",
        "Fixed support slice, subject to prime approval and procurement eligibility.",
        "USD 3,200 fixed; survey-data support only",
        "Hello,",
        "I prepared a narrow O-D survey data QA and dashboard prototype support packet for NJ TRANSIT RFP 0000234.",
        "If this support slice is eligible, the first input would be the public RFP package and a dummy survey schema.",
        "Portal-only to NJ TRANSIT. Gmail only for approved teaming outreach to survey/planning primes.",
        "Bid Express or approved survey/planning prime path",
    ),
    lead(
        "C10K-119",
        "Brittany / nonprofit Salesforce-ActiveCampaign Make scenarios",
        "Make Community forum packet",
        "https://community.make.com/t/need-help-with-integrations-on-scenarios/107903",
        "Salesforce-ActiveCampaign Make stabilization sprint",
        "CRM integration rescue",
        "A nonprofit posted for help with multiple Make scenarios where Salesforce and ActiveCampaign are not working as desired.",
        "The practical first close is stabilizing two scenarios with mapping rules, dedupe checks, error handling, and a short runbook.",
        "Salesforce-ActiveCampaign Make stabilization sprint",
        "Two nonprofit CRM scenarios stabilized with evidence",
        "Make CRM rescue",
        "I can audit up to two scenarios, define field/update rules, fix filters and dedupe behavior, add failure alerts, and leave a short test checklist.",
        "The Make Community post is a direct Hire Help request and should be handled through forum reply/DM first.",
        "This is a fixed rescue sprint using dummy records or least-privilege access after approval.",
        "No donor, constituent, member, volunteer, fundraising, or sensitive CRM records should be shared by forum DM or email.",
        "This does not include bulk outreach, list scraping, deliverability evasion, fundraising advice, or unauthorized CRM access.",
        1200,
        "make-salesforce-activecampaign-visual.png",
        ["Audit", "Field map", "Fixes", "Alerts", "Runbook"],
        [
            "Scenario audit for up to two Make workflows and the exact Salesforce/ActiveCampaign failure points",
            "Field mapping and update-rule document covering creates, updates, ownership, and duplicates",
            "Filter, dedupe, and error-path fixes in a testable copy or approved workspace",
            "Failure alerts for bad payloads, auth issues, missing fields, and repeated errors",
            "Dummy-record test checklist with pass/fail evidence and retest notes",
            "Short handoff runbook for future changes and safe credential rotation",
        ],
        [["Fast close", "Small, concrete, and directly tied to a posted broken workflow."], ["Nonprofit-safe", "Starts with dummy records and least-privilege access."], ["No spam lane", "The offer is system repair, not bulk outreach tactics."]],
        "Reply or DM in Make Community with the packet link; ask for a dummy record and the two failing scenarios.",
        "Fixed rescue sprint for up to two scenarios.",
        "USD 1,200 fixed; dummy records first",
        "Hi Brittany,",
        "I saw your Make Community post about Salesforce and ActiveCampaign scenarios not behaving correctly for your nonprofit.",
        "If useful, send one dummy record, the two scenarios causing the most trouble, and what should happen when the workflow succeeds.",
        "Forum/DM only unless Brittany provides a public email. Do not request donor/member data.",
        "Make Community reply/DM to Brittany",
    ),
    lead(
        "C10K-120",
        "Emanuel Arias - Notion and Adalo integration",
        "Make Community forum packet",
        "https://community.make.com/t/help-setting-up-a-notion-adalo-app-integration/107803",
        "Notion-Adalo Sync v1",
        "No-code app data sync",
        "Emanuel asked for help building communication between Notion databases and an Adalo app.",
        "A one-direction sync with upsert, dedupe, and error logging is the safest first version before promising two-way behavior.",
        "Notion-Adalo Sync v1",
        "A controlled Notion-Adalo sync before two-way complexity",
        "Notion + Adalo sync",
        "I can map up to two Notion databases and two Adalo collections, build one approved sync direction first, add upsert/dedupe/error logging, and hand off a compact setup doc.",
        "The Make Community post is a direct integration help request and should be handled through forum reply/DM.",
        "This is a fixed v1 integration proof using sample records and approved API access.",
        "No live API tokens, user private data, payment data, or production records should be shared by forum DM or email.",
        "This is not a promise of full two-way sync, offline support, app-store readiness, or privacy/legal compliance.",
        1500,
        "notion-adalo-sync-visual.png",
        ["Schema", "Direction", "Upsert", "Errors", "Docs"],
        [
            "Schema map for up to two Notion databases and two Adalo collections",
            "Sync-direction decision note with create/update/delete behavior and conflict rules",
            "Make scenario or equivalent integration plan for one approved direction",
            "Upsert and dedupe rules with stable IDs and retry behavior",
            "Error log for failed records, missing fields, API limits, and auth problems",
            "Handoff doc with setup steps, tokens-to-create list, and acceptance checklist",
        ],
        [["Right first step", "One direction proves the data model before two-way sync creates conflict risk."], ["Sample-data safe", "No live tokens or production records are needed in messages."], ["Clear finish line", "The deliverable is a working v1 plus docs, not indefinite troubleshooting."]],
        "Reply or DM in Make Community with the packet link; ask for sample schemas and one desired sync direction.",
        "Fixed v1 sync proof for a bounded schema.",
        "USD 1,500 fixed; one approved sync direction first",
        "Hi Emanuel,",
        "I saw your Notion-to-Adalo integration post and prepared a small v1 sync scope that keeps the first milestone clear.",
        "If useful, send sample field names from the Notion database and Adalo collection, plus whether Notion should push to Adalo or the reverse.",
        "Forum/DM only. Do not request live API tokens in messages.",
        "Make Community reply/DM to Emanuel_Arias",
    ),
    lead(
        "C10K-121",
        "Ann - Make, Typebot, OpenAI, and Airtable setup",
        "Make Community forum packet",
        "https://community.make.com/t/integration-make-typebot-open-ai-airtable/107562",
        "Typebot-Airtable-AI setup rescue",
        "AI chatbot workflow rescue",
        "Ann asked for Make, Typebot, OpenAI, and Airtable setup help, including Typebot conditions and a 403/API permissions issue.",
        "The fastest useful paid task is fixing permissions/model access and proving one working multi-step bot flow with Airtable read/write.",
        "Typebot-Airtable-AI setup rescue",
        "A working Typebot-Airtable-AI path from permissions to test flow",
        "Typebot + Airtable rescue",
        "I can fix the model/API permission path, build one working multi-step Typebot flow, connect Airtable read/write through Make, and document the required token/scopes setup.",
        "The Make Community post is a direct small-budget build request and should be handled through forum reply/DM.",
        "This is a fixed rescue sprint using a sandbox bot, dummy Airtable rows, and approved keys only in a secure workspace.",
        "No API keys, personal data, private customer records, or regulated advice content should be sent by forum DM or email.",
        "This does not include medical/legal/financial advice flows, deceptive bot behavior, scraping, or production support beyond the handoff.",
        850,
        "typebot-airtable-ai-visual.png",
        ["Permissions", "Flow", "Airtable", "Errors", "Guide"],
        [
            "OpenAI/model access and 403-permission diagnosis checklist",
            "One working multi-step Typebot flow with conditions and expected bot responses",
            "Airtable read/write connection through Make using dummy rows and clear field mapping",
            "Basic error visibility for failed API calls, missing fields, and bad model responses",
            "Token/scope setup guide without exposing secrets in messages",
            "Final acceptance checklist with one pass/fail test run",
        ],
        [["Small and concrete", "The 403 and first working flow are easy to define and accept."], ["Sandbox first", "No keys or private records need to move through forum messages."], ["Bounded AI", "The bot behavior is testable, not open-ended."]],
        "Reply or DM in Make Community with the packet link; ask for screenshots of the error and dummy Airtable fields.",
        "Fixed rescue sprint for one working setup path.",
        "USD 850 fixed; sandbox and dummy rows first",
        "Hi Ann,",
        "I saw your Make/Typebot/OpenAI/Airtable setup post and prepared a small rescue scope around the 403/API permission issue and first working flow.",
        "If useful, send a screenshot of the error, dummy Airtable field names, and the one Typebot path you want working first.",
        "Forum/DM only. Never request API keys over forum or email.",
        "Make Community reply/DM to Ann",
    ),
]


BOUNTY_LANE = {
    "lead_id": "C10K-122",
    "buyer": "Authorized bounty and PR-first lane",
    "source_url": "https://www.hackerone.com/bug-bounty-programs",
    "secondary_url": "https://devnetwork-ai-ml-hack-2026.devpost.com/",
    "offer": "Authorized vulnerability disclosure and PR-first bounty pipeline",
}


def csv_line(row: dict, fieldnames: list[str]) -> str:
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writerow(row)
    return buf.getvalue()


def upsert_prospect(entry: dict, lead_data: dict) -> None:
    with PROSPECTS.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
    row = {
        "lead_id": lead_data["lead_id"],
        "created_at": "2026-05-11",
        "label_namespace": "Codex10k",
        "company": lead_data["buyer"],
        "contact": lead_data["email"],
        "channel": lead_data["channel"],
        "source_url": lead_data["source_url"],
        "segment": lead_data["segment"],
        "problem_hypothesis": lead_data["problem_hypothesis"],
        "offer": lead_data["offer_title"],
        "status": "prep_packet_ready_no_send",
        "last_touch": "2026-05-11",
        "next_action": f"Review prepared packet and use only via approved path: {lead_data['response_path']}",
        "follow_up_date": "2026-05-14",
        "evidence_uri": f"{entry['html_path']}; {entry['pdf_path']}; {entry['draft_path']}; {entry['public_url']}",
        "notes": lead_data["send_caution"],
    }
    line = csv_line(row, fieldnames).encode()
    raw = PROSPECTS.read_bytes()
    lines = raw.splitlines(keepends=True)
    prefix = f"{lead_data['lead_id']},".encode()
    for index, existing in enumerate(lines):
        if existing.startswith(prefix):
            ending = b"\r\n" if existing.endswith(b"\r\n") else b"\n"
            lines[index] = line.rstrip(b"\n") + ending
            PROSPECTS.write_bytes(b"".join(lines))
            return
    if raw and not raw.endswith((b"\n", b"\r\n")):
        raw += b"\n"
    PROSPECTS.write_bytes(raw + line)


def write_bounty_lane() -> None:
    md = """# Authorized Bounty / PR-First Lane

Updated: 2026-05-11T00:00:00Z

This lane is for lawful, in-scope security and bounty work only. It is not revenue until a program pays out and `data/ledger.csv` has transaction evidence, fees/costs, and net-profit math.

## Rules

- Work only inside explicit public scope: HackerOne, program security pages, Devpost challenges, GitHub issues with posted bounties, or maintainer-approved repositories.
- No credential misuse, persistence, lateral movement, real user data access, destructive testing, rate-limit abuse, or post-disclosure exploitation.
- Prefer patchable findings: dependency confusion in test projects, authz logic in open-source repos with local repro, unsafe defaults, injection/XSS in local dev fixtures, or CI/workflow security bugs.
- Submit a clear report first when required. Send a PR only when the program or maintainer rules allow it, or after the maintainer confirms they want a fix.
- Keep proof local and synthetic: mocked tokens, seeded fixtures, local containers, and redacted logs.

## Current Targets To Investigate

| Target | Source | Why It Fits | Next Action | Revenue Rule |
| --- | --- | --- | --- | --- |
| HackerOne public programs | https://www.hackerone.com/bug-bounty-programs | Public list of programs that can offer bounties and rules of engagement. | Filter for open-source/web programs with explicit safe-harbor and no invite gate. | Count only paid HackerOne bounty after payout evidence. |
| DevNetwork AI + ML Hackathon / TrueFoundry resilient agents | https://devnetwork-ai-ml-hack-2026.devpost.com/ | Prize path for a buildable resilient-agent artifact; not a vulnerability exploit. | Build an agent failure lab with simulated MCP/provider outages and clear logs. | Count only awarded and paid prize net of costs. |
| Algora/GitHub bounty issues | https://algora.io/projectdiscovery/bounties | PR-first payment model on GitHub issues. | Find issues with clear acceptance criteria, no account/private-data access, and tests. | Count only paid bounty after PR acceptance and payment evidence. |

## Report Template

1. Scope confirmation: program URL, asset, and rule allowing the test.
2. Local reproduction: exact version, fixture data, commands, and expected/actual behavior.
3. Impact: concrete but bounded. No claims beyond the demonstrated issue.
4. Safety: no real user data, no persistence, no production disruption.
5. Fix path: patch summary, tests, and whether a PR is attached or available on request.
6. Evidence: screenshots, logs, commit links, report ID, bounty ID, payout ID.
"""
    BOUNTY_MD.write_text(md)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    make_visuals()
    manifest = []
    lines = [
        "# Codex10k May 11 Prep Batch",
        "",
        f"Updated: {datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}",
        "",
        "Prepared only. Do not send, submit, upload, create portal accounts, or bind Nakul without explicit action-time approval.",
        "",
    ]
    for lead_data in LEADS:
        lead_data.setdefault("slug", builder.slugify(f"{lead_data['lead_id']} {lead_data['buyer']}"))
        html_path = ROOT / f"{lead_data['slug']}.html"
        pdf_path = OUT_DIR / f"{lead_data['slug']}.pdf"
        draft_path = OUT_DIR / f"{lead_data['slug']}.draft.txt"
        html_path.write_text(builder.html_page(lead_data))
        builder.build_pdf(lead_data, pdf_path)
        public_url = f"https://anonymusk7.github.io/codex10k-workflow-recovery/{lead_data['slug']}.html?v=may11prep"
        body = builder.email_body(lead_data, public_url)
        draft_path.write_text(body + "\n")
        entry = {
            "lead_id": lead_data["lead_id"],
            "buyer": lead_data["buyer"],
            "to": lead_data["email"],
            "subject": lead_data["subject"],
            "response_path": lead_data["response_path"],
            "source_url": lead_data["source_url"],
            "slug": lead_data["slug"],
            "html_path": str(html_path.relative_to(ROOT)),
            "pdf_path": str(pdf_path.relative_to(ROOT)),
            "draft_path": str(draft_path.relative_to(ROOT)),
            "public_url": public_url,
            "price_usd": lead_data["price_usd"],
            "status": "prep_packet_ready_no_send",
        }
        manifest.append(entry)
        upsert_prospect(entry, lead_data)
        lines.extend([
            f"## {lead_data['lead_id']} {lead_data['buyer']}",
            "",
            f"- Path: {lead_data['response_path']}",
            f"- To: `{lead_data['email'] or 'not email-first'}`",
            f"- Source: {lead_data['source_url']}",
            f"- Page: {public_url}",
            f"- PDF: `{entry['pdf_path']}`",
            f"- Draft copy: `{entry['draft_path']}`",
            f"- Price: {builder.money(lead_data['price_usd'])}",
            f"- Caution: {lead_data['send_caution']}",
            "",
            "Draft:",
            "",
            "```text",
            body,
            "```",
            "",
        ])
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    OUTBOX.write_text("\n".join(lines).rstrip() + "\n")
    write_bounty_lane()
    print(MANIFEST)
    print(OUTBOX)
    print(BOUNTY_MD)


if __name__ == "__main__":
    main()
