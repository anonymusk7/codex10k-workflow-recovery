# Codex10k Draft Payment Close Pack

Updated: 2026-05-11T01:51:03Z

Use this only after a buyer positively replies or asks for payment. No invoice, Stripe link, Checkout Session, or charge should be created until the buyer approves the exact scope, price, data boundary, and payment path.

Stripe best-practice note: use Payment Links, hosted Checkout, or Stripe Invoicing for one-time payments. Do not collect card details directly and do not use legacy Charges/Sources/Card Element flows.

## Ledger Rule

Nothing in this pack is revenue evidence. Add revenue to `data/ledger.csv` only after settlement evidence exists with transaction ID, actual processor/platform fees, direct costs, refunds/disputes, and net-profit math.

## Fast Use

1. Buyer replies yes or asks how to pay.
2. Confirm billing name/email, exact scope, exclusions, timeline, data boundary, and approval owner.
3. Use the row below to choose Stripe Payment Link/Checkout, Stripe Invoice, manual invoice, PO, or selected-vendor path.
4. Send only the approved payment URL or invoice.
5. Update `data/ledger.csv` only after settlement evidence is complete.

## Close Matrix

| Lead | Buyer | Amount | Card Fee Est. | Net Before Costs | Collection | Payment Path |
| --- | --- | ---: | ---: | ---: | --- | --- |
| C10K-090 | Society of St. Vincent de Paul Cincinnati | USD 6,800 | USD 197.50 | USD 6,602.50 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice or Stripe link after SVDP confirms local/support-sidecar eligibility. |
| C10K-093 | THRIVE Victoria | USD 7,500 | USD 217.80 | USD 7,282.20 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice or Stripe link after THRIVE confirms USD/CAD billing preference. |
| C10K-092 | Institute of International Education | USD 12,500 | USD 362.80 | USD 12,137.20 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice/PO after IIE confirms support slice can be considered. |
| C10K-088 | Friends of Springfield Art Museum | USD 7,500 | USD 217.80 | USD 7,282.20 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice/PO after Springfield confirms CRM QA support path. |
| C10K-085 | Connecticut Auditors of Public Accounts | USD 12,500 | USD 362.80 | USD 12,137.20 | 50% kickoff / 50% acceptance or buyer PO terms | No payment link until Connecticut APA confirms procedure and recipient. |
| C10K-086 | Maine Community College System | USD 10,500 | USD 304.80 | USD 10,195.20 | 50% kickoff / 50% acceptance or buyer PO terms | No payment link until MCCS confirms support-component eligibility. |
| C10K-089 | Town of Hillsborough | USD 6,500 | USD 188.80 | USD 6,311.20 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice/PO only after Hillsborough confirms data/GIS support path. |
| C10K-087 | American Battle Monuments Commission | USD 12,500 | USD 362.80 | USD 12,137.20 | 50% kickoff / 50% acceptance or buyer PO terms | Federal procurement/subcontract path first; no casual payment link. |
| C10K-084 | BakerRipley | USD 19,500 | USD 565.80 | USD 18,934.20 | 50% kickoff / 50% acceptance or buyer PO terms | Eligibility first because vendor conference may control participation. |
| C10K-091 | Northumberland Humane Society | USD 4,800 | USD 139.50 | USD 4,660.50 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice or Stripe link only after NHS confirms non-local support role is acceptable. |
| C10K-096 | Revenue Authority of Prince George's County | USD 14,500 | USD 420.80 | USD 14,079.20 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice/PO or selected-prime path after PGC confirms support route. |
| C10K-099 | Ely Area Tourism Bureau | USD 12,500 | USD 362.80 | USD 12,137.20 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice or buyer-approved payment link if Ely still wants migration QA support. |
| C10K-100 | Hiawatha Academies | USD 12,000 | USD 348.30 | USD 11,651.70 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice/PO after Hiawatha confirms website QA support path. |
| C10K-095 | Harford County Public Schools | USD 9,500 | USD 275.80 | USD 9,224.20 | 50% kickoff / 50% acceptance or buyer PO terms | Formal path or selected-vendor path after Harford responds. |
| C10K-094 | Baxter State Park Authority | USD 8,500 | USD 246.80 | USD 8,253.20 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice/PO only after Baxter confirms addenda/procurement path. |
| C10K-098 | Town of Duck | USD 6,800 | USD 197.50 | USD 6,602.50 | 50% kickoff / 50% acceptance or buyer PO terms | Invoice/PO after Duck confirms support-sidecar path. |
| C10K-097 | Napa Valley Transportation Authority | USD 4,800 | USD 139.50 | USD 4,660.50 | 50% kickoff / 50% acceptance or buyer PO terms | Formal RFQ/payment path only; avoid legal certification framing. |
| C10K-101 | 3D Walkabout | USD 1,800 | USD 52.50 | USD 1,747.50 | 100% upfront | Stripe Payment Link/Checkout is acceptable after one workflow is confirmed. |
| C10K-103 | Chek Creative | USD 1,200 | USD 35.10 | USD 1,164.90 | 100% upfront | Stripe Payment Link/Checkout after Chek sends one client-safe brief. |
| C10K-102 | SnipeAgent | USD 400 | USD 11.90 | USD 388.10 | 100% upfront | Stripe Payment Link/Checkout after architecture pass approval. |

## Buyer Approval Reply Skeleton

```text
Hi {{name}},

Great, I can start once the payment path is approved and the agreed sample inputs are available.

Scope: {{scope}}
Price: {{amount}} fixed
Collection: {{collection_terms}}
Payment path: {{payment_link_or_invoice_or_po_path}}
Timeline: {{timeline}} after payment/PO approval and input availability

Please confirm the billing name/email, approval owner, and whether you prefer Stripe-hosted card payment, Stripe invoice, manual invoice, or procurement/PO handling.

No production credentials or private records need to be sent by email for the first checklist; dummy, redacted, or buyer-approved secure workspace inputs are fine.

Best,
Nakul
```

## Per-Lead Close Notes

### C10K-090 Society of St. Vincent de Paul Cincinnati

- Draft ID: `r1477712879751866611`
- Offer: Website launch QA, accessibility, and donor-path support
- Status: sent_from_draft
- Amount: USD 6,800
- Planning-only card fee estimate: USD 197.50; estimated net before direct costs: USD 6,602.50
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice or Stripe link after SVDP confirms local/support-sidecar eligibility.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-093 THRIVE Victoria

- Draft ID: `r341758721023828887`
- Offer: Youth-services website QA and campaign-readiness support
- Status: sent_from_draft
- Amount: USD 7,500
- Planning-only card fee estimate: USD 217.80; estimated net before direct costs: USD 7,282.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice or Stripe link after THRIVE confirms USD/CAD billing preference.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-092 Institute of International Education

- Draft ID: `r-4264919839455923807`
- Offer: Fulbright Scholar website maintenance QA and accessibility support
- Status: sent_from_draft
- Amount: USD 12,500
- Planning-only card fee estimate: USD 362.80; estimated net before direct costs: USD 12,137.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice/PO after IIE confirms support slice can be considered.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-088 Friends of Springfield Art Museum

- Draft ID: `r-516733945645526600`
- Offer: Museum CRM data migration and acceptance QA support
- Status: sent_from_draft
- Amount: USD 7,500
- Planning-only card fee estimate: USD 217.80; estimated net before direct costs: USD 7,282.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice/PO after Springfield confirms CRM QA support path.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-085 Connecticut Auditors of Public Accounts

- Draft ID: `r-5424769604189818739`
- Offer: SharePoint workflow QA and maintenance support slice
- Status: sent_from_draft
- Amount: USD 12,500
- Planning-only card fee estimate: USD 362.80; estimated net before direct costs: USD 12,137.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: No payment link until Connecticut APA confirms procedure and recipient.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-086 Maine Community College System

- Draft ID: `r7792718751307555089`
- Offer: IAM role validation and rollout QA support
- Status: sent_from_draft
- Amount: USD 10,500
- Planning-only card fee estimate: USD 304.80; estimated net before direct costs: USD 10,195.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: No payment link until MCCS confirms support-component eligibility.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-089 Town of Hillsborough

- Draft ID: `r-3371871953269203560`
- Offer: GIS/data workflow QA and deliverable support slice
- Status: auto_reply_received
- Amount: USD 6,500
- Planning-only card fee estimate: USD 188.80; estimated net before direct costs: USD 6,311.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice/PO only after Hillsborough confirms data/GIS support path.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-087 American Battle Monuments Commission

- Draft ID: `r8757273967754748544`
- Offer: HRIS migration and acceptance QA support
- Status: sent_from_draft
- Amount: USD 12,500
- Planning-only card fee estimate: USD 362.80; estimated net before direct costs: USD 12,137.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Federal procurement/subcontract path first; no casual payment link.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-084 BakerRipley

- Draft ID: `r7718642615731016285`
- Offer: Salesforce implementation QA and UAT support sidecar
- Status: gmail_draft_created_no_send
- Amount: USD 19,500
- Planning-only card fee estimate: USD 565.80; estimated net before direct costs: USD 18,934.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Eligibility first because vendor conference may control participation.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-091 Northumberland Humane Society

- Draft ID: `r9137065922616610769`
- Offer: Donation, adoption, and campaign website QA support
- Status: gmail_draft_created_no_send
- Amount: USD 4,800
- Planning-only card fee estimate: USD 139.50; estimated net before direct costs: USD 4,660.50
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice or Stripe link only after NHS confirms non-local support role is acceptable.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-096 Revenue Authority of Prince George's County

- Draft ID: `r5521619101680114811`
- Offer: Parking PMS migration QA follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 14,500
- Planning-only card fee estimate: USD 420.80; estimated net before direct costs: USD 14,079.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice/PO or selected-prime path after PGC confirms support route.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-099 Ely Area Tourism Bureau

- Draft ID: `r-4234669480558694433`
- Offer: Ely tourism migration QA follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 12,500
- Planning-only card fee estimate: USD 362.80; estimated net before direct costs: USD 12,137.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice or buyer-approved payment link if Ely still wants migration QA support.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-100 Hiawatha Academies

- Draft ID: `r3962797927973152463`
- Offer: Hiawatha multilingual website QA follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 12,000
- Planning-only card fee estimate: USD 348.30; estimated net before direct costs: USD 11,651.70
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice/PO after Hiawatha confirms website QA support path.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-095 Harford County Public Schools

- Draft ID: `r3100201977837495910`
- Offer: Harford routing data QA follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 9,500
- Planning-only card fee estimate: USD 275.80; estimated net before direct costs: USD 9,224.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Formal path or selected-vendor path after Harford responds.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-094 Baxter State Park Authority

- Draft ID: `r5353432031169205359`
- Offer: Baxter ADA/migration launch QA follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 8,500
- Planning-only card fee estimate: USD 246.80; estimated net before direct costs: USD 8,253.20
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice/PO only after Baxter confirms addenda/procurement path.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-098 Town of Duck

- Draft ID: `r3606409848104572723`
- Offer: Town of Duck launch QA follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 6,800
- Planning-only card fee estimate: USD 197.50; estimated net before direct costs: USD 6,602.50
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Invoice/PO after Duck confirms support-sidecar path.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-097 Napa Valley Transportation Authority

- Draft ID: `r907155150484054466`
- Offer: NVTA ADA website QA follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 4,800
- Planning-only card fee estimate: USD 139.50; estimated net before direct costs: USD 4,660.50
- Collection terms: 50% kickoff / 50% acceptance or buyer PO terms
- Payment path: Formal RFQ/payment path only; avoid legal certification framing.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-101 3D Walkabout

- Draft ID: `r8198823679674218259`
- Offer: 3D Walkabout HubSpot-ClickUp sprint follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 1,800
- Planning-only card fee estimate: USD 52.50; estimated net before direct costs: USD 1,747.50
- Collection terms: 100% upfront
- Payment path: Stripe Payment Link/Checkout is acceptable after one workflow is confirmed.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-103 Chek Creative

- Draft ID: `r-3557540405541149303`
- Offer: Chek Creative automation pilot follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 1,200
- Planning-only card fee estimate: USD 35.10; estimated net before direct costs: USD 1,164.90
- Collection terms: 100% upfront
- Payment path: Stripe Payment Link/Checkout after Chek sends one client-safe brief.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.

### C10K-102 SnipeAgent

- Draft ID: `r332576918970528924`
- Offer: SnipeAgent architecture pass follow-up
- Status: gmail_draft_created_no_send
- Amount: USD 400
- Planning-only card fee estimate: USD 11.90; estimated net before direct costs: USD 388.10
- Collection terms: 100% upfront
- Payment path: Stripe Payment Link/Checkout after architecture pass approval.
- Approval needed: exact deliverables, exclusions, timeline, billing route, data boundary, and acceptance owner.
- Evidence to capture: buyer approval message, invoice/payment URL or invoice PDF, transaction/session/invoice ID, settlement/payout proof, actual fee evidence, direct costs/refunds/disputes, and ledger math.
