# Codex10k Revenue Close Desk

Updated: 2026-05-10T08:00:00Z

Use this file when a buyer replies positively. It is a close-control sheet, not revenue evidence. Do not count any amount until the ledger gate at the bottom is satisfied.

## Current Send Gate

- May 10 Gmail cap used: 13 of 13.
- User-approved extra sends used: 3 of 3.
- Do not send more email on May 10 unless the user explicitly raises the cap again.
- Before any future outbound email, run `node scripts/check-email-cadence.mjs --cap=<approved cap>` and obey any stricter user-stated gap.

## Short-Cycle Close Priority

| Lead | Buyer | Trigger To Act | First Payment Ask | Close Asset |
| --- | --- | --- | ---: | --- |
| C10K-007 | Bluestork / BygAI | Phase 0 approval, meeting confirmation, or payment-link request | USD 1,200 | `docs/bluestork-phase0-payment-request.md` |
| C10K-033 | GoodieX Tech LLC | Chooses the first sales-lifecycle bottleneck or asks for next step | USD 1,800 | `docs/goodiex-v1-scope.md` |
| C10K-070 | SnipeAgent | Sends NDA/scope or confirms architecture pass | USD 400 | `snipeagent-sms-automation.html` |
| C10K-072 | Chek Creative | Sends one client-safe workflow brief | USD 1,200 | `chek-automation-partner-pilot.html` |
| C10K-069 | 3D Walkabout | Confirms HubSpot-to-ClickUp workflow is still open | USD 1,800 | `3dwalkabout-hubspot-clickup.html` |
| C10K-046 | Visualfestation | Confirms Skool/Zendo/Airtable/Rewardful/Stripe v1 | USD 1,200 | `visualfestation-integration.html` |

## Procurement Close Priority

These are higher-value but slower. Treat positive replies as procurement-path clarification first, not casual sales conversation.

| Lead | Buyer | First Payment Ask | Next Step If They Reply |
| --- | --- | ---: | --- |
| C10K-083 | Revenue Authority of Prince George's County | USD 14,500 | Ask whether to submit narrow support slice directly, via selected prime, or after award. |
| C10K-075 | Ely Area Tourism Bureau | USD 12,500 | Ask for procurement/payment path, current export/crawl, staging/vendor timeline, and tracker format. |
| C10K-079 | Hiawatha Academies | USD 12,000 | Ask for staging/vendor timeline, sample language paths, and procurement/payment path. |
| C10K-081 | Harford County Public Schools | USD 9,500 | Follow HCPS instruction: formal path, selected-vendor path, or informational only. |
| C10K-080 | Baxter State Park Authority | USD 8,500 | Ask to register for addenda and confirm whether support slice can be considered. |
| C10K-047 | SoIN Tourism | USD 8,500 | Ask for CMS/CRM/partner portal priorities and proposal/payment path. |
| C10K-074 | Town of Duck | USD 6,800 | Ask for priority pages, PDFs/forms/events, staging timing, tracker format, and payment path. |
| C10K-073 | NVTA | USD 4,800 | Ask for priority URLs, representative PDF/document samples, tracker format, remediation owner, and payment path. |

## Payment Request Rule

Use Stripe Payment Links, hosted Checkout, or Stripe Invoice after the buyer approves the exact scope. Do not collect card details directly and do not create a charge without buyer authorization.

Preferred one-time collection:

1. Buyer approves exact deliverables, exclusions, price, timeline, and data boundary.
2. Create Stripe Payment Link, hosted Checkout Session, or invoice.
3. Send only the approved payment URL or invoice.
4. Start work after payment settles and required inputs are available.
5. Record transaction and fee evidence before ledger credit.

If Stripe is unavailable, use a manual invoice or bank transfer. Do not count revenue until settlement evidence exists.

## Fast Reply Templates

### Buyer Says Yes

Subject: Re: approved fixed-scope milestone

Hi {{name}},

Great, I can start after payment is complete and the sample inputs are available.

Scope: {{lead_scope}}
Price: USD {{amount}} fixed.
Payment: {{insert_payment_link_or_invoice_url}}
Timeline: {{timeline}} after payment, access rules, and sample inputs are available.

Please send or confirm:

- billing name and billing email,
- preferred invoice entity, if different,
- sample or anonymized records/files,
- who approves the milestone,
- any systems or data that are off-limits.

I will not need production credentials or private records by email for the first checklist.

Best,
Nakul

### Procurement Says Formal Path Only

Subject: Re: formal submission path

Hi {{name}},

Understood. I will treat this as formal-procurement only and will not route additional material outside the required path.

If a limited support slice is eligible through the formal process, I can submit the narrow package there. If it must be handled through the selected prime/vendor instead, I can hold it for that route.

Best,
Nakul

### Buyer Asks For Proof Before Paying

Subject: Re: proof path before payment

Hi {{name}},

The safest proof path is a small sample-data checklist, not production access.

I can use {{sample_type}} to show the acceptance format:

- input assumptions,
- expected output,
- pass/fail checks,
- error and manual-review cases,
- handoff notes.

If that matches what you need, the paid milestone remains USD {{amount}} fixed.

Best,
Nakul

## Ledger Gate

Do not add revenue to `data/ledger.csv` unless all evidence exists:

- buyer approval message ID or signed acceptance,
- invoice/payment link URL or invoice PDF,
- transaction ID or charge/session/invoice ID,
- settlement or payout evidence,
- actual payment fee evidence,
- direct costs, platform fees, refunds, or disputes,
- final net-profit math.

Verified net profit remains USD 0 until this gate is complete.

