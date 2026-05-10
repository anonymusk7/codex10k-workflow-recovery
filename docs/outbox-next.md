# Proposal Queue

Prepared on 2026-05-09 and updated on 2026-05-10 after the user allowed outbound email under a strict cadence. Before any email send, run `node scripts/check-email-cadence.mjs --cap 10`; send only if it returns `allowed: true`, then log the exact timestamp and message ID in `data/email-send-log.csv`.

## C10K-079 Hiawatha Academies

Source checked May 10, 2026: official Hiawatha Academies RFQ page and PDF request modernization and redesign of the school website, with WCAG 2.1 A/AA, English/Spanish/Somali support, mobile responsiveness, content migration, recruitment/family engagement, and communications requirements. Proposals are due May 15, 2026 at 11:59 PM, and the point of contact/submission email is Kyle Groves at `kgroves@hiawathaacademies.org`.

To: kgroves@hiawathaacademies.org

Subject: Modernization and Redesign of School Website RFQ - Nakul

Status: sent May 10, 2026 as Gmail message `19e104c1b35de655` with `outputs/codex10k/hiawatha_school_website_qa_sidecar_proposal.pdf` attached. This was the 10th outbound email today under the default cap, so do not send more email on May 10 unless the user explicitly raises the cap. Next action is to watch for RFQ response/confirmation; if positive, request staging/vendor timeline, representative URLs/templates, language sample paths, preferred tracker format, and procurement/payment path.

Body:

Hello Kyle,

I saw Hiawatha Academies' open RFQ for Modernization and Redesign of School Website, including the May 15, 2026 deadline, WCAG 2.1 A/AA accessibility expectations, English/Spanish/Somali language support, content migration, mobile responsiveness, recruitment/family engagement goals, and staff communication needs.

I am Nakul, an independent freelancer/sole proprietor. Please register this sender for addenda if this limited support submission can be considered.

I am not submitting this as a full redesign-prime agency response, hosting proposal, CMS license, or legal accessibility certification. I am submitting a limited support slice that could help Hiawatha directly or sit beside the selected website/CMS vendor around multilingual QA, accessibility acceptance testing, content migration checks, and launch readiness.

Reference page:

https://anonymusk7.github.io/codex10k-workflow-recovery/hiawatha-school-website-qa-sidecar.html?v=hiawatha1

Attached proposal: USD 12,000 fixed.

Scope summary:

- RFQ-aligned acceptance checklist for mobile, accessibility, multilingual navigation, migration, forms, search, analytics, and CMS handoff
- English, Spanish, and Somali sample coverage review across representative pages, navigation, calls to action, forms, and family pathways
- WCAG-oriented checks for headings, keyboard path, labels, alt text, contrast, documents, forms, and key public pages
- content migration, redirects, metadata, broken links, search, analytics, and staff publishing workflow spot checks
- issue register, retest notes, launch-readiness summary, and staff publishing guardrails

Boundaries: this is QA, acceptance testing, retest, and staff handoff support only. It does not include the full website rebuild, hosting, CMS licensing, legal accessibility certification, or long-term maintenance unless separately scoped. No student records, family records, credentials, payment data, analytics exports, or private Hiawatha files are needed by email.

If this limited support slice is useful, I can provide the acceptance checklist and issue-register format before vendor selection discussions.

Best,
Nakul

## C10K-083 Revenue Authority of Prince George's County

Source checked May 10, 2026: official Revenue Authority solicitation page for `RVA-PMS-04-2026` says electronic proposals are due by email to `RVA-PMS.RFP@co.pg.md.us` by June 1, 2026 at 2:00 PM EST.

To: RVA-PMS.RFP@co.pg.md.us

Subject: RVA-PMS-04-2026 - limited parking data QA support slice

Status: sent May 10, 2026 as Gmail message `19e10e01ea3147ae` with `outputs/codex10k/pgc_parking_data_qa_support_slice.pdf` attached. This was the third and final user-approved extra May 10 email; do not send more email on May 10 unless the user explicitly raises the cap again.

Body:

Hello,

Please find attached a limited independent support proposal for RVA-PMS-04-2026, Cloud-Based Parking Management System.

I am Nakul, an independent freelancer/sole proprietor. I am not submitting this as the full parking management system, hardware, LPR, enforcement, cyber insurance, or long-term maintenance bid. This is a narrow support slice that could sit beside the Revenue Authority, selected prime, or selected PMS vendor for data migration QA, integration acceptance, reporting QA, UAT evidence, and go-live readiness.

Reference page:

https://anonymusk7.github.io/codex10k-workflow-recovery/pgc-parking-data-qa-sidecar.html?v=pgc1

Attached package: USD 14,500 fixed.

The support slice would produce:

- migration reconciliation checklist for citations, payments, permits, accounts, collections, locations, statuses, and owner mappings
- integration acceptance matrix for LPR, payment, ERP/financial, court/Tyler, CRM/311, collections, DMV lookup, and reporting paths
- duplicate, underpayment, overpayment, refund, permit, citation lifecycle, and exception-case test scenarios
- BI/reporting QA notes for revenue analysis, forecasting, spatial views, operational dashboards, and data dictionary gaps
- UAT issue register with severity, evidence, likely owner, remediation status, retest result, and go-live risk notes
- launch evidence memo summarizing clean decisions, unresolved risks, and what should be proven before award or cutover

Boundary: no live citation records, license plates, payment data, DMV records, credentials, or enforcement exports should be sent by email. Sample or anonymized records are enough to build the initial checklist.

If this limited support slice can be considered, please register it as a narrow proposal beside the primary PMS vendor or route it to the appropriate selected-prime/subcontract path.

Best,
Nakul

## C10K-081 Harford County Public Schools

Source checked May 10, 2026: RFP 26-SR-014 public procurement materials/subagent research identify a Bus Routing, Fleet Management, GPS, and School Planning Solutions procurement with questions due May 19, 2026 and proposals due June 10, 2026. Use this only as a procurement clarification/support question unless HCPS instructs a formal path.

To: sara.rowe@hcps.org

Subject: RFP 26-SR-014 - limited routing data QA support question

Status: sent May 10, 2026 as Gmail message `19e10c2baf1299e8` with `outputs/codex10k/harford_routing_data_qa_support_question.pdf` attached. This was the second of the three user-approved extra May 10 emails; next outbound requires `node scripts/check-email-cadence.mjs --cap=13` and at least 30 minutes after `2026-05-10T07:21:14Z`.

Body:

Hello Sara,

I saw HCPS RFP 26-SR-014 for Bus Routing, Fleet Management, GPS, and School Planning Solutions. I am writing this as a procurement clarification question, not as a full routing/fleet/GPS software proposal.

I am Nakul, an independent freelancer/sole proprietor. Could HCPS consider a limited support slice that sits beside the primary solution vendor and focuses on routing data readiness, GPS validation samples, acceptance tests, issue tracking, and cutover evidence?

Reference page:

https://anonymusk7.github.io/codex10k-workflow-recovery/harford-routing-data-qa-sidecar.html?v=harford1

Attached support question: USD 9,500 fixed.

The support slice would produce:

- route/stop/vehicle/school/schedule data readiness checklist
- duplicate, missing-value, invalid-coordinate, and field-ownership checks
- acceptance test scenarios for bell schedules, route exceptions, service changes, parent-facing outputs, reporting, and handoff criteria
- GPS validation sample plan for device-to-route matching, stale signals, vehicle IDs, timing variance, and route-completion evidence
- issue register with severity, evidence, likely owner, remediation status, retest result, and launch-risk notes

Boundary: no student names, home addresses, live route assignments, GPS logs, credentials, or internal exports should be sent by email. A sample or anonymized data path is enough to shape the checklist.

If this type of limited support is eligible, should it be submitted directly through the formal RFP path, routed through the selected vendor, or treated only as an informational procurement question?

Best,
Nakul

## C10K-080 Baxter State Park Authority

Source checked May 10, 2026: official BSP RFP PDF says electronic proposals are due May 20, 2026 to `nava.tabak@baxterstatepark.org`.

To: nava.tabak@baxterstatepark.org

Subject: Baxter State Park website RFP - limited launch QA support

Status: sent May 10, 2026 as Gmail message `19e10a5e7c318c9b` with `outputs/codex10k/baxter_website_launch_qa_sidecar_proposal.pdf` attached. This was the first of the three user-approved extra May 10 emails; next outbound requires `node scripts/check-email-cadence.mjs --cap=13` and at least 30 minutes after `2026-05-10T06:49:39Z`.

Body:

Hello Nava,

I saw Baxter State Park's April 6 RFP for a new website, hosting, and technical maintenance services, with electronic proposals due May 20, 2026.

I am Nakul, an independent freelancer/sole proprietor. I am not submitting this as a full design-prime, hosting, or long-term maintenance bid. I prepared a limited support slice that could help BSP or the selected website vendor with launch-readiness evidence around the RFP's risk areas: ADA Title II web/mobile accessibility checks, content transition, mobile QA, search/forms/ecommerce paths, performance review, and staff handoff notes.

Reference page:

https://anonymusk7.github.io/codex10k-workflow-recovery/baxter-website-launch-qa-sidecar.html?v=baxter1

Attached package: USD 8,500 fixed.

The package would produce:

- RFP-aligned acceptance checklist
- issue register with severity, evidence, likely owner, fix status, and retest result
- ADA-oriented manual checks for headings, keyboard path, focus, labels, alt text, contrast, links, forms, documents, and mobile paths
- content-transition spot checks for priority pages, redirects, metadata, downloads, maps, news/posts, search, and high-use visitor flows
- launch-readiness and staff publishing handoff notes

Boundary: no visitor records, ecommerce exports, credentials, analytics exports, or private BSP files should be sent by email. Public pages, approved staging access after procurement approval, and representative test cases are enough to start the checklist.

If this limited support slice can be considered, please register this sender for any addenda and let me know the preferred procurement path.

Best,
Nakul

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

## C10K-075 Ely Area Tourism Bureau / Ely Chamber of Commerce

Source checked May 10, 2026: official Ely RFP page and RFP PDF request website development and content migration from Simpleview, with proposals due May 11, 2026. The RFP says submissions go to Jess Edberg at `jess@rootbeerlady.com` as a PDF with subject `Website Development RFP - [Your Company Name]`.

To: jess@rootbeerlady.com

Subject: Website Development RFP - Nakul

Status: sent May 10, 2026 as Gmail message `19e1037e9f166d0a` with `outputs/codex10k/ely_migration_qa_launch_readiness_proposal.pdf` attached. Do not resend. Next action is to watch for RFP response; if positive, request current crawl/export, representative listing export, staging/vendor timeline, preferred tracker format, and procurement/payment path.

Body:

Hello Jess,

I saw the Ely Area Tourism Bureau / Ely Chamber of Commerce Website Development & Content Migration RFP, including the Simpleview migration, 50-70 page content move, business/member directory functions, SEO preservation, analytics, WCAG 2.1 AA, CMS training, QA, launch support, and 90-day post-launch support requirements.

I am Nakul, an independent freelancer/sole proprietor. I am not submitting this as a complete redesign-prime agency response, hosting proposal, CMS license, or legal accessibility certification. I am submitting a limited support slice that could help Ely directly or sit beside the selected website/CMS vendor around migration QA, directory readiness, and launch support.

Reference page:

https://anonymusk7.github.io/codex10k-workflow-recovery/ely-migration-qa-sidecar.html?v=ely1

Attached proposal: USD 12,500 fixed.

Scope summary:

- content inventory, redirect/SEO spot checks, metadata checks, media/link validation, and post-migration issue register
- business/member listing field review, template acceptance checks, tier/reporting validation, and dashboard/admin-flow notes
- WCAG-oriented, mobile, browser, search, form, analytics, CMS publishing, and launch-readiness QA checks
- go-live checklist, retest notes, staff publishing guardrails, and short post-launch support

Boundaries: this is QA, directory-readiness, and launch-support only. It does not include the full website rebuild, hosting, CMS licensing, legal accessibility certification, or long-term maintenance unless separately scoped. No credentials, analytics exports, private member data, payment data, or internal Ely files are needed by email.

If this limited support slice is useful, I can provide the migration QA checklist and issue-register format before vendor selection discussions.

Best,
Nakul

## C10K-074 Town of Duck, NC

Source checked May 10, 2026: official Town of Duck website redesign and CMS implementation RFP was published April 23, 2026. Proposals are due May 14, 2026 at 5:00 PM EST, electronic submissions are acceptable, and the RFP contact is Kay Nickens at `knickens@ducknc.gov`.

To: knickens@ducknc.gov

Subject: Website Redesign RFP Submission - Town of Duck - limited QA sidecar

Status: sent May 10, 2026 as Gmail message `19e10294ab3b5ab5` with `outputs/codex10k/town_of_duck_launch_qa_sidecar_proposal.pdf` attached. Do not resend. Next action is to watch for procurement response; if positive, request priority pages, representative PDFs/forms/events, staging access timing, preferred tracker format, remediation owner, and procurement/payment path.

Body:

Hello Kay,

I saw the Town of Duck's Website Redesign and CMS Implementation RFP, including the ADA, Section 508, WCAG 2.2 AA, content migration, searchable document, analytics, staff workflow, and post-launch support requirements.

I am Nakul, an independent freelancer/sole proprietor. I am not submitting this as a full redesign-prime proposal, hosting proposal, CMS license, or legal compliance certification. I am submitting a limited sidecar proposal that could support the Town directly or support the selected website/CMS vendor around launch QA and staff handoff.

Reference page:

https://anonymusk7.github.io/codex10k-workflow-recovery/duck-ada-launch-qa-sidecar.html?v=duck1

Attached proposal: USD 6,800 fixed.

Scope summary:

- WCAG-oriented QA across representative templates, mobile views, forms, documents, and high-use public-service paths
- content migration spot checks for redirects, metadata, linked documents, searchability, events/calendar pages, and broken-link risks
- issue register with severity, evidence, likely owner, status, retest result, and launch-readiness note
- staff publishing checklist for accessible pages, images, links, forms, calendar/event entries, and PDFs

Boundaries: this is QA, retest, and staff-handoff support only. It does not include full redesign, CMS implementation, hosting, licensing, legal certification, or long-term maintenance unless separately scoped. No resident records, credentials, analytics exports, or internal Town files are needed by email.

If this limited support proposal is responsive, I can provide the issue-register template and staff checklist format before award discussions.

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

## C10K-073 Napa Valley Transportation Authority

Source checked May 10, 2026: official RFQ 26-R08 says quotes for ADA Website Compliance should be sent by email to `procurements@nvta.ca.gov`, copy `rcoombs@nvta.ca.gov`, with subject `Quote for RFQ No. 26-R08, ADA WEBSITE COMPLIANCE`. Quotes are due May 22, 2026 at 2:00 PM local time.

To: procurements@nvta.ca.gov
Cc: rcoombs@nvta.ca.gov

Subject: Quote for RFQ No. 26-R08, ADA WEBSITE COMPLIANCE

Status: sent May 10, 2026 as Gmail message `19e101890b095ee2` with `outputs/codex10k/nvta_ada_qa_sidecar_quote.pdf` attached. Do not resend. Next action is to watch for procurement response; if positive, request priority URLs, representative PDFs/documents, preferred tracker format, remediation owner, and procurement/payment path.

Body:

Hello Renel,

Please find attached a limited independent quote for RFQ No. 26-R08, ADA Website Compliance.

I am submitting a narrow QA/retest/staff-checklist support package rather than representing this as a full legal compliance certification or full remediation/maintenance prime contract.

Reference page:

https://anonymusk7.github.io/codex10k-workflow-recovery/nvta-ada-qa-sidecar.html?v=nvta1

Quoted package: USD 4,800 fixed.

Scope summary:

- representative NVTA.ca.gov and VineTransit.com page/mobile sample
- automated accessibility scan triage with false-positive cleanup
- manual checks for keyboard path, headings, labels, focus indicators, alt text, contrast, forms, link purpose, and representative PDF/document samples
- issue register with severity, evidence note, owner/status field, retest result, and open-risk note
- staff checklist for accessible publishing of pages, images, links, forms, and PDFs

Boundary: this is QA and retest support only. It does not include legal certification, full code remediation, CMS development, hosting, or ongoing maintenance unless scoped separately. No rider, HR, analytics, credential, or internal system data is needed by email.

If this limited quote is responsive, I can provide the issue tracker template and staff checklist format before award discussions.

Best,
Nakul
