# Codex10k Outreach

All outreach originated in this run must use the `Codex10k/` Gmail label namespace.

## Compliance Guardrails

- Use truthful sender identity, subject line, and offer.
- Do not imply credentials, case studies, clients, results, availability, or ownership that are not verified.
- Honor opt-outs immediately.
- Do not use cold SMS, robocalls, WhatsApp blasts, LinkedIn bots, scraped personal data, fake reviews, or review gating.
- For U.S. commercial cold email, CAN-SPAM requires a valid physical postal address and clear opt-out mechanism. Until a valid postal address is available, prioritize explicit hiring posts, warm replies, marketplace proposals, contact forms, and communities where the recipient has requested help.
- Outreach cadence: send at most 10 outbound emails/day by default, never more than 20/day without explicit same-day user approval, and keep at least 15 minutes between outbound emails.
- Run `node scripts/check-email-cadence.mjs --cap 10` immediately before sending and record successful sends in `data/email-send-log.csv`.

## Template: Public Hiring Post

Use this only when the post can be served as a done-for-you client project, not an employment application.

Subject: Fixed-scope workflow build for {{company}}

Hi {{name/team}},

I saw your public post looking for help with {{workflow/tooling}}.

I’m not looking for an employee role. I can take one tightly scoped workflow as a done-for-you build: map the current process, build or fix the automation, add logging/error handling, and hand over docs so your team can run it without me.

Best first step: send one blocked workflow with sample inputs and the target output. I’ll reply with either a fixed-price milestone scope or a clear no-fit.

Best,
Nakul

## Template: Agency Overflow

Subject: White-label workflow sprint capacity

Hi {{team}},

I’m reaching out because your work around {{specific service}} overlaps with the workflow systems I build: lead intake, CRM cleanup, quote flows, dashboards, and AI-assisted ops.

If you ever have a client workflow that is too small, too urgent, or too awkward for your core team, I can take a fixed-scope white-label sprint and hand back a documented build.

Useful test project: one broken or manual workflow, shipped in 10 business days.

Best,
Nakul

## Template: Warm Reply After Interest

Subject: Re: {{original subject}}

Hi {{name}},

Thanks for the interest.

The simplest next step is a short paid pilot around one workflow. I’d need:

- the current request/input source,
- where the result should land,
- who owns follow-up,
- and 5-10 sample records or examples.

From there I can send a fixed scope, price, timeline, and handoff plan.

Best,
Nakul

## Template: Employment Clarification

Subject: Re: {{original subject}}

Hi {{name}},

Small clarification: I’m not seeking an employee role or a long interview process.

I’m offering a done-for-you fixed-scope build. If you still need this workflow, the practical path is: send anonymized sample inputs and the target output, I scope a paid milestone, then I build/test/document the workflow and hand it over.

If you’re only collecting employment-style applications, no problem; feel free to ignore this.

Best,
Nakul

## Template: No-Pressure Follow-Up

Subject: Re: {{original subject}}

Hi {{name}},

Quick follow-up on this. If the workflow is still worth fixing, send me one example of the current input and where it should land. I’ll turn that into a concrete pilot scope.

If this is not relevant, reply "unsubscribe" and I will not contact you again.

Best,
Nakul

## Template: RFP Support Slice

Use this only for a public RFP or RFQ where the buyer has listed an official contact path. Do not send it to nondesignated staff during restricted procurement.

Subject: {{project}}: bounded QA/accessibility support option

Hi {{name/team}},

I saw {{organization}}'s public {{RFP/RFQ}} for {{project}}. I am not sending this as a full prime proposal or trying to bypass the procurement process.

If useful to {{organization}} or the selected vendor, I can provide a fixed-scope launch QA/support package focused on {{risk areas}}.

Fixed support package: USD {{price}}

Includes:

- {{path_or_integration}} QA
- accessibility checks on key templates and high-use pages
- mobile, browser, link, redirect, and form checks
- CMS editor workflow checks
- launch acceptance checklist and prioritized punch-list tracker

No sensitive data should be sent by email; public/staging pages and dummy/test records are enough.

If this support option is relevant, reply with the expected staging window or forward it to the selected vendor after award, and I will send a one-page scope with acceptance criteria.

Best,
Nakul
