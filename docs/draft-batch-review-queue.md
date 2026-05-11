# Codex10k Draft Batch Review Queue

Updated: 2026-05-11T02:29:07Z

This is a review queue for the 20 Gmail draft-batch packets. Sent: 9. Still draft-only: 11. Do not count any value here as revenue until completed and settled payment evidence exists in `data/ledger.csv`.

Total draft pipeline: USD 172,600.

Payment close pack: `docs/draft-payment-close-pack.md` and `outputs/codex10k/draft_payment_close_pack.pdf`.

## Recommended New-Draft Order

| Rank | Lead | Status | Draft ID | Price | Why / Caution |
| ---: | --- | --- | --- | ---: | --- |
| 1 | C10K-090 Society of St. Vincent de Paul Cincinnati | sent | `r1477712879751866611` | USD 6,800 | Strong direct-email nonprofit web RFP; local-firm preference means support-sidecar is cleaner than prime bid. |
| 2 | C10K-093 THRIVE Victoria | sent | `r341758721023828887` | USD 7,500 | Strong direct-email nonprofit website RFP; buyer budget is CAD, while tracker records USD. |
| 3 | C10K-092 Institute of International Education | sent | `r-4264919839455923807` | USD 12,500 | Good IIE fit, but full-service provider framing matters. |
| 4 | C10K-088 Friends of Springfield Art Museum | sent | `r-516733945645526600` | USD 7,500 | Good CRM migration QA lane; avoid platform-prime claims. |
| 5 | C10K-085 Connecticut Auditors of Public Accounts | sent | `r-5424769604189818739` | USD 12,500 | Procurement question to the inquiry contact; not a proposal. |
| 6 | C10K-086 Maine Community College System | sent | `r7792718751307555089` | USD 10,500 | Email path exists; questions deadline passed, so keep it as support component. |
| 7 | C10K-089 Town of Hillsborough | sent | `r-3371871953269203560` | USD 6,500 | No licensed engineering claim; data/GIS support only. |
| 8 | C10K-087 American Battle Monuments Commission | sent | `r8757273967754748544` | USD 12,500 | Federal HRIS; slower, formal, no employee PII. |
| 9 | C10K-084 BakerRipley | sent | `r7718642615731016285` | USD 19,500 | Mandatory vendor conference risk; eligibility question only. |
| 10 | C10K-091 Northumberland Humane Society | draft | `r9137065922616610769` | USD 4,800 | Ontario/local vendor preference; support-sidecar only. |

## Recommended Follow-Up Order

Follow-up drafts should generally wait until the user wants a manual follow-up cadence. They remain draft-only unless marked sent below.

| Rank | Lead | Status | Draft ID | Price | Why / Caution |
| ---: | --- | --- | --- | ---: | --- |
| 1 | C10K-096 Revenue Authority of Prince George's County | draft | `r5521619101680114811` | USD 14,500 | Highest follow-up value; procurement path likely controls. |
| 2 | C10K-099 Ely Area Tourism Bureau | draft | `r-4234669480558694433` | USD 12,500 | High value but RFP deadline was tight; send only as courteous close/follow-up. |
| 3 | C10K-100 Hiawatha Academies | draft | `r3962797927973152463` | USD 12,000 | School website support; no student/family data by email. |
| 4 | C10K-095 Harford County Public Schools | draft | `r3100201977837495910` | USD 9,500 | K-12 routing data; formal path or selected-vendor path likely. |
| 5 | C10K-094 Baxter State Park Authority | draft | `r5353432031169205359` | USD 8,500 | State park website support; ask for procurement path/addenda registration. |
| 6 | C10K-098 Town of Duck | draft | `r3606409848104572723` | USD 6,800 | Municipal website RFP deadline tight; support-sidecar only. |
| 7 | C10K-097 Napa Valley Transportation Authority | draft | `r907155150484054466` | USD 4,800 | Formal RFQ; avoid legal accessibility certification claims. |
| 8 | C10K-101 3D Walkabout | draft | `r8198823679674218259` | USD 1,800 | Commercial automation follow-up; quickest small close. |
| 9 | C10K-103 Chek Creative | draft | `r-3557540405541149303` | USD 1,200 | Agency pilot follow-up; quick close if they send a client-safe brief. |
| 10 | C10K-102 SnipeAgent | draft | `r332576918970528924` | USD 400 | Small architecture pass; quick but low-dollar. |

## Close Rule

When a buyer replies positively, use `docs/revenue-close-desk.md` first. Ask for the exact billing/procurement path, then create a Stripe Payment Link, hosted Checkout Session, Stripe invoice, or manual invoice only after the buyer approves the exact scope.

Ledger credit requires transaction ID, settlement or payout proof, actual fee evidence, direct-cost/refund evidence, and net-profit math.
