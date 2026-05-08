# Payment Flow Draft

Stripe connector tools were not exposed in this environment during inspection, so this file defines the payment-flow setup to create manually or through Stripe Dashboard access if it becomes available.

Use Stripe Payment Links or hosted Checkout for simple one-time milestone payments. Do not collect card details directly, do not use legacy Charges/Sources/Card Element flows, and do not charge a buyer until they have approved the scope and authorized payment.

## Products

| Product | Price | Collection Timing |
| --- | ---: | --- |
| Workflow Triage | USD 750 | 100% upfront |
| 10-Day Workflow Sprint | USD 4,800 | 50% upfront, 50% on acceptance |
| Advanced 10-Day Workflow Sprint | USD 7,500 | 50% upfront, 50% on acceptance |
| Optimization Retainer | USD 1,000/mo | Monthly, cancel anytime |

## Payment Terms

- Work starts after upfront payment settles or a signed agreement is accepted.
- Direct third-party costs are separate and must be approved before use.
- Refunds, disputes, platform fees, payment fees, and purchased assets are subtracted in the verified profit ledger.
- For Stripe U.S. domestic card assumptions, budget 2.9% + USD 0.30 per successful transaction unless actual fee evidence differs.
- Payment links should expire or be replaced if scope changes.
- If the client needs ACH/wire/manual invoice, record settlement evidence before counting profit.

## Invoice Notes

Description:

> Fixed-scope workflow automation sprint covering discovery, implementation, testing, documentation, one revision pass, and handoff for one agreed workflow.

Evidence to store in `evidence/`:

- invoice PDF or Stripe invoice URL,
- payment/charge ID,
- payout/settlement proof,
- fee receipt,
- any refund/dispute evidence,
- signed scope or acceptance email.

## Buyer Authorization Checklist

Before sending a payment request:

- exact buyer/counterparty name,
- fixed deliverables and exclusions,
- milestone price and currency,
- who approves acceptance,
- direct costs, if any,
- refund/cancellation terms,
- data-access boundaries,
- buyer's written approval to proceed.

After payment:

- transaction ID,
- settled payout evidence,
- actual payment fee,
- final net profit calculation,
- link or screenshot evidence path in `data/ledger.csv`.
