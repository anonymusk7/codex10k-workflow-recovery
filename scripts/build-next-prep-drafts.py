#!/usr/bin/env python3
"""Build the next Codex10k prep-only proposal batch."""

from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

BUNDLED_PYTHON = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "bin" / "python3"
if BUNDLED_PYTHON.exists() and Path(sys.executable).resolve() != BUNDLED_PYTHON.resolve():
    os.execv(str(BUNDLED_PYTHON), [str(BUNDLED_PYTHON), *sys.argv])

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "codex10k" / "prep-drafts"
MANIFEST = OUT_DIR / "prep_draft_manifest.json"
OUTBOX = ROOT / "docs" / "prep-drafts-next.md"
PROSPECTS = ROOT / "data" / "prospects.csv"
BUILDER_PATH = ROOT / "scripts" / "build-draft-batch.py"

spec = importlib.util.spec_from_file_location("draft_builder", BUILDER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {BUILDER_PATH}")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def ensure_visual_assets() -> None:
    """Create offer-specific PNG workflow visuals used by this prep batch."""
    from PIL import Image, ImageDraw, ImageFont

    asset_specs = {
        "research-automation-client-onboarding-visual.png": {
            "title": "Research automation control layer",
            "accent": "#2f6f94",
            "left": ["Client config", "Source list", "Cadence rules"],
            "right": ["Google Doc output", "Run state", "Error log"],
            "nodes": ["Config", "Sources", "Run", "Doc", "Log"],
        },
        "bubble-saas-blueprint-visual.png": {
            "title": "Maternity SaaS MVP blueprint",
            "accent": "#7a5aa6",
            "left": ["Roles", "Care flows", "Payments"],
            "right": ["PDFs", "Scheduling", "Milestone plan"],
            "nodes": ["Roles", "Data", "Stripe", "PDF", "Plan"],
        },
        "pace-scheduling-migration-visual.png": {
            "title": "Scheduling migration readiness",
            "accent": "#2b7a5e",
            "left": ["Legacy events", "Rooms", "Fees"],
            "right": ["Field map", "Test load", "Cutover evidence"],
            "nodes": ["Inventory", "Map", "Rules", "Test", "Cutover"],
        },
        "m365-records-governance-visual.png": {
            "title": "M365 records governance pilot",
            "accent": "#316b9f",
            "left": ["Content inventory", "Taxonomy", "Owners"],
            "right": ["Permissions", "Lifecycle", "Pilot QA"],
            "nodes": ["Inventory", "Taxonomy", "Access", "Lifecycle", "QA"],
        },
        "caregiver-sms-state-visual.png": {
            "title": "Caregiver SMS state model",
            "accent": "#2b7a70",
            "left": ["Fictional SMS", "Scenario state", "Approval rules"],
            "right": ["Reviewer queue", "Event log", "Analytics view"],
            "nodes": ["SMS", "State", "Review", "Log", "Metrics"],
        },
        "hubspot-document-export-visual.png": {
            "title": "HubSpot document export proof",
            "accent": "#315f9f",
            "left": ["Associations", "Files", "Owners"],
            "right": ["Manifest", "Export test", "Failure list"],
            "nodes": ["Inventory", "API", "Sample", "Manifest", "Plan"],
        },
        "transportation-safety-dashboard-visual.png": {
            "title": "Transportation safety dashboard workflow",
            "accent": "#2f6f94",
            "left": ["Crash data", "VRU counts", "Corridors"],
            "right": ["KPI model", "Dashboard", "Update workflow"],
            "nodes": ["Sources", "QA", "KPIs", "Map", "Refresh"],
        },
    }

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(exist_ok=True)
    font_regular = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19)
    font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
    font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
    font_node = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)

    for filename, spec in asset_specs.items():
        path = assets_dir / filename
        img = Image.new("RGB", (1200, 675), "#f7f6ef")
        draw = ImageDraw.Draw(img)
        accent = spec["accent"]

        draw.rounded_rectangle((56, 48, 1144, 627), radius=28, fill="#ffffff", outline="#dfe5e2", width=2)
        draw.rounded_rectangle((92, 88, 1108, 148), radius=20, fill="#f0f5f2")
        draw.ellipse((124, 111, 138, 125), fill="#e86f55")
        draw.ellipse((150, 111, 164, 125), fill="#e8b94d")
        draw.ellipse((176, 111, 190, 125), fill="#4b9f72")
        draw.text((224, 105), spec["title"], fill="#142129", font=font_bold)

        panel_y = 190
        for x, label, lines in [
            (94, "Input controls", spec["left"]),
            (806, "Output evidence", spec["right"]),
        ]:
            draw.rounded_rectangle((x, panel_y, x + 300, 520), radius=22, fill="#fbfaf5", outline="#dfe5e2", width=2)
            draw.text((x + 28, panel_y + 28), label, fill=accent, font=font_bold)
            for idx, item in enumerate(lines):
                y = panel_y + 88 + idx * 70
                draw.rounded_rectangle((x + 28, y, x + 272, y + 44), radius=12, fill="#ffffff", outline="#dfe5e2", width=2)
                draw.rectangle((x + 28, y, x + 36, y + 44), fill=accent)
                draw.text((x + 50, y + 12), item, fill="#142129", font=font_regular)

        node_xs = [430, 512, 594, 676, 758]
        node_y = 342
        for idx, (x, label) in enumerate(zip(node_xs, spec["nodes"])):
            if idx:
                draw.line((node_xs[idx - 1] + 54, node_y + 34, x, node_y + 34), fill=accent, width=5)
                draw.polygon([(x - 2, node_y + 34), (x - 16, node_y + 26), (x - 16, node_y + 42)], fill=accent)
            draw.rounded_rectangle((x, node_y, x + 74, node_y + 68), radius=18, fill="#ffffff", outline=accent, width=3)
            draw.text((x + 37, node_y + 22), label, fill="#142129", font=font_node, anchor="ma")

        draw.rounded_rectangle((426, 450, 774, 526), radius=18, fill="#142129")
        draw.text((600, 471), "fixed-scope proof before full build", fill="#ffffff", font=font_small, anchor="ma")
        img.save(path)


LEADS = [
    {
        "lead_id": "C10K-104",
        "buyer": "Claire Manwaring / caregiver SMS workflow",
        "email": "",
        "channel": "Make Community draft",
        "source_url": "https://community.make.com/t/looking-for-short-term-help-with-make-bubble-supabase-claude-twilio/108581",
        "subject": "Stateful SMS MVP build-readiness sprint",
        "segment": "Caregiver SMS workflow",
        "opportunity": "Bubble, Supabase, Make, Twilio, Claude, Slack approval, and analytics workflow for a short-term May build.",
        "problem_hypothesis": "The risk is not one Make scenario; it is durable conversation state, approval routing, audit logs, analytics, and safe escalation boundaries.",
        "offer_title": "Stateful SMS MVP build-readiness sprint",
        "hero_title": "Caregiver SMS state, approval, and analytics sprint",
        "eyebrow": "Make + Bubble + Supabase + Twilio",
        "meta_description": "A client-safe proposal packet for a caregiver SMS workflow sprint.",
        "lede": "I can turn the current product brief into a testable state machine, Twilio/Make flow map, Supabase event log, Slack approval loop, and two end-to-end journeys before deeper implementation.",
        "fit": "The post already names the stack and the delivery window. The strongest first milestone is an execution-ready state model and proof path, not a vague hourly contractor pitch.",
        "positioning": "This is a fixed build-readiness sprint that can be credited toward implementation if the architecture matches the product constraints.",
        "boundary": "No PHI, caregiver private data, real health details, or production phone numbers should be sent by email or forum DM. Use fully fictional conversations and buyer-approved secure workspaces.",
        "exclusions": "This is not medical, HIPAA, privacy, employment, or compliance advice; it is technical workflow architecture and implementation readiness.",
        "price_usd": 3500,
        "pills": ["USD 3,500 fixed", "credited if approved", "fictional data first"],
        "visual_asset": "assets/caregiver-sms-state-visual.png",
        "visual_alt": "Workflow diagram showing fictional SMS intake, state memory, human approval, event logging, and analytics handoff.",
        "workflow_steps": ["State schema", "SMS flow map", "Approval loop", "Event log", "Journey tests"],
        "deliverables": [
            "Conversation-state schema for caregiver, scenario, message, status, and escalation events",
            "Twilio plus Make flow map with retry, duplicate, timeout, and manual-review states",
            "Supabase event-log table plan with analytics-ready fields and privacy boundaries",
            "Slack approval loop specification with reviewer actions and rejection paths",
            "Two dummy-data journey tests with expected prompts, approvals, and final outcomes",
            "Implementation backlog with build estimate, risks, and acceptance criteria",
        ],
        "fit_cards": [
            ["Why this slice", "State and review controls decide whether the SMS MVP works reliably."],
            ["Buyer-safe first step", "Dummy conversations prove the workflow before production data or phone numbers."],
            ["Build bridge", "The sprint can inform a milestone-based implementation quote after the brief is approved."],
        ],
        "next_step": "Reply in Make Community/DM with the packet link and ask for one fully fictional conversation, desired approval states, and the current Bubble/Supabase table shape.",
        "quote_note": "Fixed architecture/readiness sprint, credited toward implementation if approved.",
        "price_label": "USD 3,500 fixed, credited toward implementation if approved",
        "greeting": "Hi Claire,",
        "opening": "I saw your Make/Bubble/Supabase/Twilio/Claude caregiver SMS build post. I prepared a narrow first milestone that gets the state model and approval loop testable before production data enters the workflow.",
        "email_next_step": "If this matches the gap, send one fully fictional caregiver conversation, desired approval states, and the current Bubble/Supabase table shape.",
        "send_caution": "Forum/DM path only unless Claire provides an email. Do not request PHI.",
        "response_path": "Make Community reply/DM to Claire_Manwaring",
    },
    {
        "lead_id": "C10K-105",
        "buyer": "Ray Roberts / HubSpot document export",
        "email": "",
        "channel": "Make Community draft",
        "source_url": "https://community.make.com/t/looking-for-help-with-export-documents-from-hubspot-to-nutshell-or-just-export/108371",
        "subject": "HubSpot document rescue sprint",
        "segment": "CRM document migration",
        "opportunity": "HubSpot document export or transfer to Nutshell with a clear one-time migration/debug need.",
        "problem_hypothesis": "The buyer needs an inventory, sample transfer/export, manifest, and failure report before committing to a full migration run.",
        "offer_title": "HubSpot document rescue sprint",
        "hero_title": "HubSpot document export with manifest and failure proof",
        "eyebrow": "HubSpot + Nutshell migration",
        "meta_description": "A fixed HubSpot document rescue proposal for Ray Roberts.",
        "lede": "I can inventory the document associations, test a 25-record export or transfer path, and leave a clean manifest that supports either Nutshell ingestion or a controlled archive.",
        "fit": "The ask is sharply bounded: documents are stuck in HubSpot and the buyer needs evidence for either transfer or reliable export.",
        "positioning": "This is a compact migration rescue, not a broad CRM rebuild.",
        "boundary": "No customer private documents should be sent by forum DM or email; use a least-privilege workspace, sample records, or redacted test files.",
        "exclusions": "This is not a Nutshell platform guarantee until attachment ingestion capabilities are confirmed.",
        "price_usd": 950,
        "pills": ["USD 950 fixed", "25-record proof", "manifest included"],
        "visual_asset": "assets/hubspot-document-export-visual.png",
        "visual_alt": "Workflow visual showing HubSpot association inventory, file export test, manifest validation, and failure-list handoff.",
        "workflow_steps": ["Inventory", "API check", "25-record proof", "Manifest", "Run plan"],
        "deliverables": [
            "HubSpot document and association inventory for a representative sample",
            "Nutshell attachment/API feasibility check with fallback export route",
            "25-record test transfer or export with success/failure evidence",
            "CSV manifest with object ID, document name, owner, association, status, and error note",
            "Failure taxonomy for permissions, duplicates, unsupported files, and missing associations",
            "Full-run quote and runbook after sample proof",
        ],
        "fit_cards": [
            ["Fast proof", "A small sample tests whether Nutshell transfer is real or export is safer."],
            ["Audit trail", "The manifest prevents a black-box migration and gives a clear retry list."],
            ["Low-risk start", "Scope stays under 1,000 docs unless inventory shows more work."],
        ],
        "next_step": "Reply in Make Community/DM with the packet link and ask for a 10-record redacted sample or screen share of document associations.",
        "quote_note": "Fixed 25-record sample proof; full run quoted after inventory.",
        "price_label": "USD 950 fixed for the 25-record sample proof; full run quoted after inventory",
        "greeting": "Hi Ray,",
        "opening": "I saw your HubSpot document export/Nutshell post. I prepared a small rescue sprint that tests transfer feasibility before anyone commits to a full migration run.",
        "email_next_step": "If helpful, send a redacted sample or a screen share of the document associations and I can confirm the first proof path.",
        "send_caution": "Forum/DM path only unless Ray provides an email. Verify Nutshell attachment support before promising transfer.",
        "response_path": "Make Community reply/DM to RayRoberts",
    },
    {
        "lead_id": "C10K-106",
        "buyer": "Eli Malone-Shkurkin / research automation",
        "email": "",
        "channel": "Make Community draft",
        "source_url": "https://community.make.com/t/looking-to-hire-pro-for-daily-industry-research-automation-40-hours-good-rates/107995",
        "subject": "Self-serve research automation upgrade",
        "segment": "AI research workflow",
        "opportunity": "Daily industry research automation needs scaling into a self-serve multi-client setup.",
        "problem_hypothesis": "The current workflow likely benefits from a client config layer, persistence cleanup, failure logging, and output provisioning before it scales.",
        "offer_title": "Self-serve research automation upgrade",
        "hero_title": "Daily research automation that can onboard clients cleanly",
        "eyebrow": "Make + AI research ops",
        "meta_description": "A fixed research automation upgrade proposal for Eli Malone-Shkurkin.",
        "lede": "I can tighten the control layer around client configuration, Google Doc provisioning, persistence cleanup, and error logging so the workflow can move beyond one-off manual setup.",
        "fit": "The buyer already has a working automation direction. The immediate value is turning it into a repeatable onboarding and delivery system.",
        "positioning": "This is a bounded first milestone inside the broader expansion.",
        "boundary": "No scraped/private data or client secrets should be shared by forum DM; use an approved source list and dummy client config first.",
        "exclusions": "This does not include spam, scraping restricted sources, bypassing site rules, or claiming unsupported data coverage.",
        "price_usd": 3800,
        "pills": ["USD 3,800 fixed", "config layer", "failure logging"],
        "visual_asset": "assets/research-automation-client-onboarding-visual.png",
        "visual_alt": "Research automation workflow from client config to source run, document output, and error logging.",
        "workflow_steps": ["Client config", "Source run", "Doc output", "Persistence", "Error log"],
        "deliverables": [
            "Client configuration schema for industry, sources, cadence, output style, and owner",
            "Onboarding form or table plan that creates a new client run without manual scenario edits",
            "Google Doc or Drive provisioning pattern with naming, folders, and permissions checklist",
            "Persistence cleanup for run state, duplicate prevention, and source-level result tracking",
            "Failure logging and alert rules for empty runs, source failures, and output errors",
            "Handoff doc with one sample client configured end to end",
        ],
        "fit_cards": [
            ["Scale lever", "A config layer turns a custom scenario into repeatable delivery."],
            ["Cleaner ops", "Failure logs and persistence make daily runs supportable."],
            ["Commercial path", "The first upgrade can lead into a build/retainer if the workflow proves useful."],
        ],
        "next_step": "Reply in Make Community/DM with the packet link and ask for one sample client config, current scenario shape, and desired output format.",
        "quote_note": "Fixed upgrade milestone for one self-serve onboarding and output path.",
        "price_label": "USD 3,800 fixed for one self-serve onboarding and output path",
        "greeting": "Hi Eli,",
        "opening": "I saw your daily industry research automation post. I prepared a bounded first milestone that focuses on the self-serve/client-onboarding layer inside the broader expansion.",
        "email_next_step": "If useful, send one sample client config, current scenario shape, and target output format.",
        "send_caution": "Forum/DM path only unless Eli provides an email. Keep data-source permissions explicit.",
        "response_path": "Make Community reply/DM to Eli_Malone-Shkurkin",
    },
    {
        "lead_id": "C10K-107",
        "buyer": "birthcoachuk / Marley",
        "email": "marley@midwifemarley.com",
        "channel": "Bubble Forum / public email draft",
        "source_url": "https://forum.bubble.io/t/experienced-bubble-developer-needed-for-saas-mvp/393713",
        "subject": "Bubble SaaS MVP blueprint for maternity-professional workflows",
        "segment": "Bubble SaaS architecture",
        "opportunity": "Bubble SaaS MVP for maternity professionals with roles, Stripe, email, PDFs, scheduling, invoicing, and localization.",
        "problem_hypothesis": "The full build is compliance-sensitive; the safest first close is a technical blueprint and milestone quote before implementation.",
        "offer_title": "Bubble SaaS technical blueprint + build plan",
        "hero_title": "A safer first step for the maternity SaaS MVP",
        "eyebrow": "Bubble SaaS discovery",
        "meta_description": "A fixed Bubble SaaS technical blueprint proposal for Marley.",
        "lede": "I can produce the data model, role/privacy map, integration plan, compliance question list, and milestone build quote before the MVP build starts.",
        "fit": "The brief is high-value but touches healthcare-adjacent workflows, payments, PDFs, localization, and user roles. A blueprint reduces build risk.",
        "positioning": "This is a paid discovery/architecture milestone that can roll into implementation if the boundaries are approved.",
        "boundary": "No client/patient private data should be shared by email; use dummy personas, workflows, and sample documents until a secure workspace is approved.",
        "exclusions": "This is not medical, legal, privacy, or regulatory advice, and not a promise of compliance certification.",
        "price_usd": 1500,
        "pills": ["USD 1,500 fixed", "build plan", "privacy map"],
        "visual_asset": "assets/bubble-saas-blueprint-visual.png",
        "visual_alt": "SaaS blueprint workflow from roles and data model to integrations, acceptance, and build plan.",
        "workflow_steps": ["Roles", "Data model", "Integrations", "Risks", "Milestones"],
        "deliverables": [
            "Bubble data model draft for users, clients, sessions, invoices, PDFs, and status records",
            "Role/privacy map for maternity professionals, admins, and customer-facing views",
            "Stripe, email, PDF, scheduling, localization, and notification integration plan",
            "Compliance and data-boundary question list to resolve before build",
            "MVP milestone plan with acceptance criteria and implementation quote range",
            "Technical risks memo covering scalability, privacy, and no-code maintainability",
        ],
        "fit_cards": [
            ["Right first milestone", "The blueprint makes the full build quotable and safer."],
            ["Healthcare-adjacent care", "Data boundaries are handled before private data or credentials."],
            ["Implementation bridge", "The blueprint can inform a milestone-based implementation quote after scope and boundary review."],
        ],
        "next_step": "Send dummy workflows, target user roles, and the must-have MVP screens; no private client or patient data needed.",
        "quote_note": "Fixed blueprint; implementation quoted after boundaries and MVP scope are approved.",
        "price_label": "USD 1,500 fixed blueprint; implementation quoted after boundaries and MVP scope are approved",
        "deliverables_intro": "The blueprint milestone would produce",
        "greeting": "Hi Marley,",
        "opening": "I saw your Bubble SaaS MVP post for maternity professionals. I prepared a practical first milestone that gets the architecture and build plan clear before anyone commits to the full MVP.",
        "email_next_step": "If useful, send dummy workflows, target user roles, and the must-have MVP screens; no private client/patient data needed.",
        "send_caution": "Public email listed in the Bubble post. Keep as discovery/blueprint before implementation.",
        "response_path": "Bubble Forum reply/DM or approved email path to marley@midwifemarley.com",
    },
    {
        "lead_id": "C10K-108",
        "buyer": "Town of Parker / PACE",
        "email": "",
        "channel": "Bonfire portal packet",
        "source_url": "https://parkeronline.bonfirehub.com/opportunities/232506",
        "subject": "PACE scheduling data migration readiness support",
        "segment": "Scheduling system data migration",
        "opportunity": "PACE event and building scheduling system replacement with migration and integrations scoring weight.",
        "problem_hypothesis": "Scheduling replacement risk is concentrated around legacy data inventory, field mapping, duplicate rules, migration tests, and cutover evidence.",
        "offer_title": "Legacy scheduling data migration readiness pack",
        "hero_title": "Scheduling migration proof before cutover risk appears",
        "eyebrow": "PACE scheduling data readiness",
        "meta_description": "A portal-ready data migration support packet for Town of Parker PACE.",
        "lede": "I can support a future or primary scheduling platform vendor with a focused migration-readiness package: source inventory, field map, duplicate rules, test migration checklist, and cutover plan.",
        "fit": "The RFP centers on a scheduling platform procurement; this packet is only a data-migration support slice if the portal or subcontract path is allowed.",
        "positioning": "This is a specialist support package beside a future or primary scheduling platform vendor, or as a portal attachment if the path is approved.",
        "boundary": "No patron, payment, staff, or facility booking records should be sent by email. Use synthetic data, redacted samples, or schema-only field lists in an approved workspace.",
        "exclusions": "This is not the scheduling platform, payment processor, hosting contract, legal retention advice, or full prime SaaS proposal.",
        "price_usd": 9500,
        "pills": ["USD 9,500 fixed", "portal-ready", "migration QA"],
        "visual_asset": "assets/pace-scheduling-migration-visual.png",
        "visual_alt": "Data migration workflow visual from source inventory to test loads, defects, and cutover evidence.",
        "workflow_steps": ["Inventory", "Field map", "Duplicate rules", "Test load", "Cutover"],
        "deliverables": [
            "Legacy scheduling source inventory and export checklist",
            "Field mapping matrix for events, rooms, staff, customers, fees, and integrations",
            "Duplicate, missing-value, inactive-record, and attachment exception rules",
            "Test migration checklist with sample-load acceptance criteria",
            "Defect and retest register for vendor/user review",
            "Cutover evidence pack with rollback notes and post-launch checks",
        ],
        "fit_cards": [
            ["Vendor support", "Works beside the future scheduling SaaS implementer rather than replacing it."],
            ["Scored risk", "Migration readiness maps to the highest-risk part of the replacement."],
            ["Portal caution", "No submission or account action without action-time approval."],
        ],
        "next_step": "Use as a Bonfire/portal-ready support attachment only after confirming the submission path, forms, and eligibility.",
        "quote_note": "Fixed support slice, subject to portal eligibility and final scope; not a standalone prime SaaS proposal.",
        "price_label": "Indicative fixed-price support slice: USD 9,500, subject to portal eligibility and final scope; not a standalone prime SaaS proposal",
        "greeting": "Hello,",
        "opening": "I prepared a narrow PACE scheduling data-migration readiness packet that can sit beside a future or primary scheduling platform vendor.",
        "email_next_step": "If this support slice is eligible, the first input would be a test export or sample field list from the legacy scheduling system.",
        "send_caution": "Portal-only. Do not send casual email or submit without action-time approval.",
        "response_path": "Bonfire/Euna portal only",
    },
    {
        "lead_id": "C10K-109",
        "buyer": "City of Raleigh Planning & Development",
        "email": "",
        "channel": "NC eVP portal packet",
        "source_url": "https://evp.nc.gov/solicitations/",
        "subject": "Raleigh records governance pilot support slice",
        "segment": "M365 / records governance",
        "opportunity": "Records and information governance consulting across selected pilot content categories and records lifecycle workflows.",
        "problem_hypothesis": "The practical first win is a pilot inventory/taxonomy/permissions workflow that proves governance before citywide rollout.",
        "offer_title": "M365 and SharePoint information governance pilot",
        "hero_title": "Records governance that starts with a provable pilot",
        "eyebrow": "M365 records workflow",
        "meta_description": "A portal-ready M365/SharePoint governance pilot support packet for Raleigh.",
        "lede": "I can support a narrow pilot around content inventory, taxonomy, permissions, retention/lifecycle model, and workflow QA before broader records-governance rollout.",
        "fit": "The solicitation is broader than tooling, but the pilot lane maps well to SharePoint/M365 governance and repeatable workflow evidence.",
        "positioning": "This is a support slice beside a records-management lead or formal portal response if the path is approved.",
        "boundary": "No confidential records content should be sent by email; use metadata inventories, redacted samples, or approved workspace exports.",
        "exclusions": "This is not legal records-retention advice, a citywide records-management prime bid, or a Microsoft licensing package.",
        "price_usd": 18000,
        "pills": ["USD 18,000 fixed", "portal-ready", "pilot first"],
        "visual_asset": "assets/m365-records-governance-visual.png",
        "visual_alt": "Governance workflow visual from inventory to taxonomy, permissions, retention, and pilot handoff.",
        "workflow_steps": ["Inventory", "Taxonomy", "Permissions", "Lifecycle", "Pilot QA"],
        "deliverables": [
            "Pilot content inventory template for selected content categories and record families",
            "Taxonomy and metadata draft with owners, retention prompts, and exception rules",
            "SharePoint/M365 permissions review checklist for pilot libraries and groups",
            "Workflow QA checklist for intake, classification, access, retention trigger, and handoff",
            "Issue/risk register covering privacy, access, duplicate stores, and unsupported content",
            "Pilot findings memo with rollout backlog and governance decision points",
        ],
        "fit_cards": [
            ["Pilot value", "A small pilot makes records governance concrete before citywide rollout."],
            ["M365 fit", "Taxonomy, permissions, and lifecycle checks map to SharePoint realities."],
            ["Procurement caution", "Portal action requires explicit approval and required forms."],
        ],
        "next_step": "Use as an NC eVP portal-ready support packet after checking forms, supplier requirements, and submission eligibility.",
        "quote_note": "Fixed pilot support slice, subject to portal eligibility and buyer approval.",
        "price_label": "Indicative fixed-price pilot support slice: USD 18,000, subject to portal eligibility and buyer approval",
        "greeting": "Hello,",
        "opening": "I prepared a narrow records-governance pilot packet for the Raleigh Planning & Development opportunity.",
        "email_next_step": "If this support slice is eligible, the first input would be a metadata-only inventory from one pilot content area.",
        "send_caution": "Portal-only. Do not send or submit without action-time approval.",
        "response_path": "NC electronic Vendor Portal",
    },
    {
        "lead_id": "C10K-110",
        "buyer": "MORPC - Central Ohio Transportation Safety and Non-Motorized Data Collection Plans",
        "email": "mschaper@morpc.org",
        "channel": "MPO RFP email draft",
        "source_url": "https://www.morpc.org/wp-content/uploads/2026/04/RFP-Central-Ohio-Transportation-Safety-Plan.pdf",
        "subject": "Central Ohio safety plan - dashboard/update workflow support slice",
        "segment": "Transportation safety data",
        "opportunity": "Transportation safety and non-motorized data collection plans with regional safety dashboard, GIS, and update workflow needs.",
        "problem_hypothesis": "A narrow dashboard/data workflow support slice can help the prime team turn counts, crash data, and VRU priorities into repeatable update evidence.",
        "offer_title": "Safety dashboard prototype + update workflow support",
        "hero_title": "Safety-plan data that can be updated after the report ships",
        "eyebrow": "Transportation safety analytics",
        "meta_description": "A support proposal for MORPC transportation safety dashboard and update workflow needs.",
        "lede": "I can provide a narrow data/dashboard support slice: KPI model, sample dashboard wireframes, data dictionary, update workflow, QA checks, and handoff notes for the plan team.",
        "fit": "The overall RFP is a large consultant scope, but a data workflow prototype is a practical support lane for a prime or internal project team.",
        "positioning": "This is an indicative specialist support slice for a prime/subconsultant attachment or formal compliant proposal path after approval.",
        "boundary": "No confidential or restricted datasets should be sent by email; use public/sample datasets or an approved secure workspace.",
        "exclusions": "This is not licensed traffic engineering, legal safety certification, or a full planning-prime proposal.",
        "price_usd": 12500,
        "pills": ["Indicative USD 12,500", "dashboard prototype", "subconsultant-ready"],
        "visual_asset": "assets/transportation-safety-dashboard-visual.png",
        "visual_alt": "Transportation data workflow visual from source data to dashboard, QA checks, and update handoff.",
        "workflow_steps": ["KPI model", "Data map", "Wireframes", "QA checks", "Handoff"],
        "deliverables": [
            "Safety KPI and data-source model for crash, VRU, bike/ped counts, and plan priorities",
            "Dashboard wireframes for executive view, corridor/location view, and update status",
            "Data dictionary with field definitions, source owner, refresh cadence, and quality checks",
            "Sample update workflow for monthly/quarterly data refresh and issue review",
            "QA checklist for missing values, stale records, duplicate locations, and map joins",
            "Handoff memo for the prime team with open decisions and implementation backlog",
        ],
        "fit_cards": [
            ["Support lane", "Useful beside a transportation planning prime without claiming the whole RFP."],
            ["Durable output", "Focuses on update workflow, not just a static final report."],
            ["Data safety", "Starts with public/sample data and explicit source permissions."],
        ],
        "next_step": "Use only as a prime/subconsultant attachment, or as a formal compliant proposal path after action-time approval.",
        "quote_note": "Indicative fixed-fee support slice: USD 12,500, subject to MORPC/prime approval and final contracting.",
        "price_label": "Indicative fixed-fee support slice: USD 12,500, subject to MORPC/prime approval and final contracting",
        "greeting": "Hello Maria,",
        "opening": "I saw the Central Ohio Transportation Safety and Non-Motorized Data Collection Plans RFP and prepared a narrow support-slice packet focused on dashboard/data workflow readiness.",
        "email_next_step": "If a focused data/dashboard support role is eligible, I can adapt this as a prime/subconsultant attachment or formal compliant proposal component.",
        "send_caution": "Use only as prime/subconsultant collateral or formal compliant proposal path after approval; do not send as a casual inquiry.",
        "response_path": "Prime/subconsultant attachment or formal compliant proposal path after approval",
    },
]


def update_prospects(manifest: list[dict]) -> None:
    existing_text = PROSPECTS.read_text()
    with PROSPECTS.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    today = "2026-05-10"
    entries_by_id = {entry["lead_id"]: entry for entry in manifest}
    leads_by_id = {lead["lead_id"]: lead for lead in LEADS}

    def prospect_row(entry: dict, lead: dict, status: str = "prep_draft_ready_no_send") -> dict:
        return {
            "lead_id": lead["lead_id"],
            "created_at": today,
            "label_namespace": "Codex10k",
            "company": lead["buyer"],
            "contact": lead["email"],
            "channel": lead["channel"],
            "source_url": lead["source_url"],
            "segment": lead["segment"],
            "problem_hypothesis": lead["problem_hypothesis"],
            "offer": lead["offer_title"],
            "status": status,
            "last_touch": today,
            "next_action": f"Review prepared packet and use only via approved path: {lead['response_path']}",
            "follow_up_date": "2026-05-13",
            "evidence_uri": f"{entry['html_path']}; {entry['pdf_path']}; {entry['email_path']}; {entry['public_url']}",
            "notes": lead["send_caution"],
        }

    seen_ids = set()
    updated_rows = []
    changed = False
    for row in rows:
        lead_id = row["lead_id"]
        if lead_id in entries_by_id:
            seen_ids.add(lead_id)
            updated = prospect_row(entries_by_id[lead_id], leads_by_id[lead_id], row.get("status") or "prep_draft_ready_no_send")
            if row != updated:
                changed = True
            updated_rows.append(updated)
        else:
            updated_rows.append(row)

    new_rows = []
    for entry, lead in zip(manifest, LEADS):
        if lead["lead_id"] in seen_ids:
            continue
        new_rows.append(prospect_row(entry, lead))
    if not changed and not new_rows:
        return
    with PROSPECTS.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
        writer.writerows(new_rows)
    if not existing_text.endswith("\n"):
        PROSPECTS.write_text(PROSPECTS.read_text().rstrip("\n") + "\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_visual_assets()
    manifest = []
    outbox = [
        "# Codex10k Prep Drafts - Next Batch",
        "",
        f"Updated: {datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}",
        "",
        "Prepared only. Do not send, submit, create portal accounts, upload files, or bind Nakul without explicit action-time approval.",
        "",
    ]
    for lead in LEADS:
        lead.setdefault("slug", builder.slugify(f"{lead['lead_id']} {lead['buyer']}"))
        html_path = ROOT / f"{lead['slug']}.html"
        pdf_path = OUT_DIR / f"{lead['slug']}.pdf"
        email_path = OUT_DIR / f"{lead['slug']}.draft.txt"
        html_path.write_text(builder.html_page(lead))
        builder.build_pdf(lead, pdf_path)
        public_url = f"https://anonymusk7.github.io/codex10k-workflow-recovery/{lead['slug']}.html?v=prep2"
        body = builder.email_body(lead, public_url)
        email_path.write_text(body + "\n")
        entry = {
            "lead_id": lead["lead_id"],
            "buyer": lead["buyer"],
            "to": lead["email"],
            "subject": lead["subject"],
            "response_path": lead["response_path"],
            "slug": lead["slug"],
            "html_path": str(html_path.relative_to(ROOT)),
            "pdf_path": str(pdf_path.relative_to(ROOT)),
            "email_path": str(email_path.relative_to(ROOT)),
            "public_url": public_url,
            "source_url": lead["source_url"],
            "price_usd": lead["price_usd"],
            "status": "prep_draft_ready_no_send",
        }
        manifest.append(entry)
        outbox.extend(
            [
                f"## {lead['lead_id']} {lead['buyer']}",
                "",
                f"- Path: {lead['response_path']}",
                f"- To: `{lead['email'] or 'not email-first'}`",
                f"- Subject: {lead['subject']}",
                f"- Source: {lead['source_url']}",
                f"- Page: {public_url}",
                f"- PDF: `{entry['pdf_path']}`",
                f"- Draft copy: `{entry['email_path']}`",
                f"- Price: {builder.money(lead['price_usd'])}",
                f"- Caution: {lead['send_caution']}",
                "",
                "Draft:",
                "",
                "```text",
                body,
                "```",
                "",
            ]
        )
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    OUTBOX.write_text("\n".join(outbox))
    update_prospects(manifest)
    print(MANIFEST)
    print(OUTBOX)


if __name__ == "__main__":
    main()
