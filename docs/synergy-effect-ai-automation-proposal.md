# Synergy Effect AI Automation Proposal Packet

Opportunity: `C10K-059`
Contact: Tomas Maciulskas / Synergy Effect
Source: https://community.n8n.io/t/hiring-ai-automation-engineer-n8n-ai-agent-developer/294904
Status: queued for May 10 only after email cadence check passes.

## Why This Is Qualified

The post was published on May 7, 2026 and explicitly allows project-based cooperation, freelance/contractor work, and end-to-end ownership of specific automation projects. It asks for production-ready n8n, AI model, API, browser automation, OCR, CRM/ERP, finance/logistics/customer-support, RAG, and human-in-the-loop work.

This should not be treated as an employee application. The sellable wedge is a fixed-scope project delivery packet that shows how one messy process becomes a working, tested, documented workflow.

## Proposed First Milestone

Offer: fixed-scope AI automation implementation slice.

Price range to quote after process details: USD 1,800-4,500.

Best first workflows:

- document or invoice intake to structured review queue,
- CRM/ERP enrichment and routing,
- inbox triage with human approval gates,
- support request classification and escalation,
- RAG/document search pilot with logging and confidence checks.

## Delivery Standard

- Use dummy or sanitized records before production access.
- Map input, validation, routing, output, owner, and exception paths.
- Add logging, replay notes, error states, and human-review gates.
- Deliver workflow export, setup notes, acceptance checklist, and operator handoff.
- Avoid any claim of prior Synergy Effect access, partnership, credentials, or guaranteed result.

## Send Gate

Before sending:

1. Run `node scripts/check-email-cadence.mjs --cap 10`.
2. Confirm it returns `allowed: true`.
3. Send only one email.
4. Log the send in `data/email-send-log.csv` with exact timestamp and message ID.
