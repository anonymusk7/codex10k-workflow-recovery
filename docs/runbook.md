# Codex10k Runbook

## Daily Operating Loop

1. Review `data/prospects.csv` for follow-ups due today.
2. Search buyer-intent channels for new posts:
   - Upwork: Zapier, Make, n8n, Airtable, dashboard, data cleanup, OpenAI, internal tool.
   - n8n/Make/Zapier/Airtable communities: hiring and help threads.
   - HN/YC/Wellfound: contract wedge for ops/data/automation roles.
   - Gmail: only messages labeled `Codex10k/*` or new direct replies to this run.
3. Reject employment-style roles unless they can be converted into a fixed-scope client deliverable that Codex can build and hand off.
4. For each qualified lead, add a row before outreach.
5. Send only relevant, truthful, non-spam messages.
6. Apply the appropriate `Codex10k/*` Gmail label.
7. Move replies to `Codex10k/Replied`, opt-outs to `Codex10k/OptOut`, and paid evidence to `Codex10k/Paid`.
8. Update `data/ledger.csv` only when revenue is settled and fees/costs are known.

## Email Cadence

User-approved outreach throttle as of 2026-05-09:

- Default daily cap: 10 outbound emails per calendar day.
- Absolute daily cap: 20 outbound emails only when the user explicitly says to use the higher cap for that day.
- Minimum spacing: 15 minutes between outbound emails.
- Before sending any outbound email, run `node scripts/check-email-cadence.mjs --cap 10`.
- Log every future outbound email with an exact timestamp in `data/email-send-log.csv`.
- If legacy sends are known for a day but exact timestamps are unavailable, treat the day as blocked once the known count reaches the cap.
- On 2026-05-09, the tracker already shows 41 Codex10k prospect rows with Gmail evidence and `last_touch=2026-05-09`; send no more outbound prospect emails that day.

## Qualification Checklist

- Is there a visible business pain?
- Is the workflow narrow enough to scope in one sprint?
- Is there a likely owner or buyer?
- Can a demo or short diagnosis be created without private/stolen data?
- Is the channel lawful and allowed by platform rules?
- Can payment evidence be captured?
- Can Codex execute most or all of the delivery without the user doing the work?
