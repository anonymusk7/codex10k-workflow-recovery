# Proposal Queue

Prepared on 2026-05-09 and updated on 2026-05-10 after the user allowed outbound email under a strict cadence. Before any email send, run `node scripts/check-email-cadence.mjs --cap 10`; send only if it returns `allowed: true`, then log the exact timestamp and message ID in `data/email-send-log.csv`.

## C10K-047 SoIN Tourism

To: Janelle@GoSoIN.com

Subject: Bounded CMS/CRM/Partner Portal QA support for SoIN RFP

Status: sent May 10, 2026 as Gmail message `19e0fd37e18291d8` with `outputs/codex10k/soin_launch_qa_support_proposal.pdf` attached. Do not resend. Next action is to watch for a reply; if positive, request staging/vendor-selection window and convert into final scope plus payment link/invoice.

Body:

Hi Janelle,

I saw SoIN Tourism's Website Services RFP for the website, CMS, CRM system of record, and Partner Portal/Extranet work due July 1. I also saw the public FAQ note that the partner portal needs bidirectional partner updates with SoIN administrative oversight, and that AI readiness is focused on structured content, metadata, schema, and discoverability.

I am not asking for an individual pre-submission meeting. I can provide a bounded launch-QA support package for SoIN Tourism or the selected vendor once staging is available.

Fixed support package: USD 8,500.

I attached a concise support packet with the launch-QA scope and boundaries.

Includes:

- CMS, CRM, and partner portal acceptance checklist from the RFP
- partner listing/event/profile update flow QA with admin approval checks
- accessibility review on representative templates and high-use visitor/partner journeys
- redirect, metadata, schema, analytics, mobile, browser, and form smoke tests
- staff-editor guardrails and a prioritized launch punch-list tracker
- retest pass after fixes

Reference page: https://anonymusk7.github.io/codex10k-workflow-recovery/#launchqa

No visitor, partner, or CRM production data is needed by email; staging pages and dummy/test records are enough.

If this support slice is useful, reply with the expected staging or vendor-selection window and I will send a concise one-page scope with acceptance criteria.

Best,
Nakul

Generated artifact:

- `outputs/codex10k/soin_launch_qa_support_proposal.pdf`

## C10K-059 Synergy Effect / Tomas Maciulskas

To: info@s-e.lt

Subject: Project-based n8n + AI automation delivery

Status: sent May 10, 2026 as Gmail message `19e0fb48b5c32d18`. Do not resend. Next action is to watch for a reply; if positive, request one real process, systems involved, target output, and sample records.

Cadence: do not send on 2026-05-09. Before sending, run `node scripts/check-email-cadence.mjs --cap 10`; send only if it returns `allowed: true`, then log the timestamp in `data/email-send-log.csv`.

Body:

Hi Tomas,

I saw your n8n Community post for project-based AI automation / n8n delivery. I am not looking for an employee role or a long recruiting loop, but the project-based cooperation model is a good fit.

The way I would be useful is taking one messy business process and shipping a fixed-scope first milestone: map the current input, build the n8n/AI workflow, add validation and human-review gates, test with dummy or sanitized records, and hand over the workflow, docs, and operating checklist.

I prepared a short technical packet here:

https://anonymusk7.github.io/codex10k-workflow-recovery/synergy-effect-ai-automation.html

Relevant sample links:

- live workflow-recovery demo: https://anonymusk7.github.io/codex10k-workflow-recovery/
- sample n8n blueprint JSON: https://anonymusk7.github.io/codex10k-workflow-recovery/outputs/codex10k/goodiex-n8n-sales-lifecycle-blueprint.json

Preferred cooperation model: fixed-scope project milestone first, then repeat project work if delivery is useful.

Availability: project-based, async-friendly, with a narrow kickoff around one workflow and acceptance checks.

Compensation expectation: depends on scope, but a practical first milestone is usually USD 1,800-4,500 for one bounded workflow or feasibility build.

If this is useful, send one real business process you want automated, the systems involved, and the target output. I will reply with a concise milestone scope and acceptance checklist.

Best,
Nakul

## C10K-046 Visualfestation / Peter Adams

Source checked May 10, 2026: Make Community post explicitly asks to contact `visualfestation@gmail.com` for Skool, Zendo, Airtable, Rewardful, and Stripe integration.

To: visualfestation@gmail.com

Subject: Skool + Zendo + Airtable + Stripe integration

Status: sent May 10, 2026 as Gmail message `19e0fc30bdc1e43f`. Do not resend. Next action is to watch for a reply; if positive, request the first flow to prioritize, dummy/test records, and rules for refunds, failed payments, duplicates, and manual review.

Cadence: before sending, run `node scripts/check-email-cadence.mjs --cap 10`; send only if it returns `allowed: true`, then log the timestamp in `data/email-send-log.csv`.

Body:

Hi Pete,

I saw your Make Community post asking for help integrating Skool, Zendo, Airtable, Rewardful, and Stripe.

I can take this as a fixed-scope build rather than an open-ended hourly engagement. I put the v1 shape here:

https://anonymusk7.github.io/codex10k-workflow-recovery/visualfestation-integration.html?v=visual1

A practical first version would be:

- Stripe payment or subscription event becomes the trigger
- Rewardful attribution is captured and stored
- Airtable becomes the source of truth for customer, purchase, affiliate, and access status
- Skool/Zendo access or project setup gets created or flagged for manual review
- failed payment, refund, duplicate contact, and missing attribution cases are logged instead of silently breaking
- handoff notes show how to run, test, and maintain the scenario

Fixed v1 price: USD 1,200.

No live payment credentials by email; I would start with Stripe test mode, dummy records, and least-privilege access under your accounts.

If this is still open, reply with the first flow you want working, for example purchase -> grant access -> affiliate tracking, and I will send the exact acceptance checklist.

Best,
Nakul

## C10K-069 3D Walkabout / Tim Brickle

Source checked May 10, 2026: Make Community post asks for HubSpot to ClickUp automation help; official/public company sources identify Tim Brickle and `tim@3dwalkabout.com.au`.

To: tim@3dwalkabout.com.au

Subject: HubSpot to ClickUp Make reliability sprint

Status: sent May 10, 2026 as Gmail message `19e0feb8882b174a`. Do not resend. Next action is to watch for a reply; if positive, request current scenario shape, trigger stages, target ClickUp list, representative sample deals, and turn the USD 1,800 reliability sprint into an acceptance checklist.

Body:

Hi Tim,

I saw your Make Community post about stabilizing HubSpot to ClickUp automations in Make: deal-stage triggers, ClickUp task creation, writebacks to HubSpot, duplicate prevention, correct filtering, and simplifying messy scenarios.

I can take the first slice as a fixed-scope reliability sprint rather than an open-ended hourly cleanup.

I prepared the shape here:

https://anonymusk7.github.io/codex10k-workflow-recovery/3dwalkabout-hubspot-clickup.html?v=3dw1

The first sprint would focus on one dependable HubSpot-to-ClickUp path:

- confirm which HubSpot deal stages should create tasks vs update existing tasks
- define the cross-system key so one deal maps to one ClickUp task
- separate create/update logic in Make
- write ClickUp task ID/status/owner back to HubSpot
- add duplicate guards, missing-field handling, and a clear failure log
- leave a field map, test checklist, and handoff notes

Fixed sprint price: USD 1,800.

No production customer export is needed by email. A sandbox, sample records, or least-privilege access is enough to start safely.

If this is still open, send the current scenario shape, trigger stages, and target ClickUp list, and I will reply with the exact sprint acceptance checklist.

Best,
Nakul

## C10K-070 SnipeAgent / Alex T

Source checked May 10, 2026: Make Community post explicitly lists `contact@snipeagent.ai` for a fixed-price AI-powered SMS/MMS Make build.

To: contact@snipeagent.ai

Subject: SnipeAgent Make SMS automation architecture pass

Status: sent May 10, 2026 as Gmail message `19e0ffab0e946f49`. Do not resend. Next action is to watch for a reply; if positive, request NDA/full scope, test number/webhook path, API access rules, reply format, milestone demo expectations, and convert the USD 400 architecture pass into a payment request.

Body:

Hi Alex,

I saw your Make Community post for the AI-powered SMS/MMS automation system: Sinch, Claude Haiku, Rainforest API, SerpApi, Carrd webhooks, parallel API calls, MMS image handling, E.164 normalization, per-user locks, data stores, and re-engagement flows.

I can help, but I would de-risk the 6-scenario / ~41-module build before wiring everything at once.

I prepared the build path here:

https://anonymusk7.github.io/codex10k-workflow-recovery/snipeagent-sms-automation.html?v=snipe1

Recommended first step: a USD 400 architecture pass, credited toward a USD 2,400 fixed build if the checklist matches what you need.

The architecture pass would produce:

- scenario map for the 6 Make scenarios
- data-store schema for users, analytics, savings, redirects, and locks
- Sinch SMS/MMS handling plan, including E.164 normalization
- parallel Rainforest + SerpApi branch plan with timeout/error handling
- Claude Haiku structured-output and fallback plan
- milestone-demo acceptance checklist for the 30/30/40 payment structure

Boundary: I will only build consent-based SMS flows under your accounts. No unsolicited messaging system, no production phone/customer data by email, and no credential sharing outside approved access.

If the project is still open, send the NDA and scope document, and I will reply with the architecture-pass checklist.

Best,
Nakul

## C10K-072 Chek Creative / Josh

Source checked May 10, 2026: Make Community post asks for senior Make.com automation partners; official contact page lists `hello@chekcreative.com`.

To: hello@chekcreative.com

Subject: Paid Make automation partner pilot

Status: sent May 10, 2026 as Gmail message `19e10093fb4ce954`. Do not resend. Next action is to watch for a reply; if positive, request one client-safe workflow brief, tools involved, source-of-truth app, sample payloads, documentation preference, and convert the USD 1,200 pilot into a payment request.

Body:

Hi Josh,

I saw your Make Community post about building Chek Creative's senior Make.com automation bench for CRM, marketing ops, lead attribution, APIs, webhooks, reliable documentation, and async-first client work.

I am not applying for a role. A cleaner way to test fit is a paid fixed-scope pilot on one client-safe workflow.

I prepared the pilot shape here:

https://anonymusk7.github.io/codex10k-workflow-recovery/chek-automation-partner-pilot.html?v=chek1

Proposed pilot: USD 1,200.

The pilot would cover one bounded workflow or reusable Make pattern:

- source-of-truth and field ownership map
- create/update/dedupe behavior
- API/webhook logic and validation
- error handling, retries, run log, and manual-review cases
- QA checklist and short SOP your team can reuse

No client secrets or private workflows need to be sent by email. A sanitized brief, dummy payloads, or client-safe sample records are enough for the first checklist.

If useful, send one client-safe workflow brief and I will reply with the exact pilot acceptance checklist.

Best,
Nakul
