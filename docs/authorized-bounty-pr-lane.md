# Authorized Bounty / PR-First Lane

Updated: 2026-05-11T00:00:00Z

This lane is for lawful, in-scope security and bounty work only. It is not revenue until a program pays out and `data/ledger.csv` has transaction evidence, fees/costs, and net-profit math.

## Rules

- Work only inside explicit public scope: HackerOne, program security pages, Devpost challenges, GitHub issues with posted bounties, or maintainer-approved repositories.
- No credential misuse, persistence, lateral movement, real user data access, destructive testing, rate-limit abuse, or post-disclosure exploitation.
- Prefer patchable findings: dependency confusion in test projects, authz logic in open-source repos with local repro, unsafe defaults, injection/XSS in local dev fixtures, or CI/workflow security bugs.
- Submit a clear report first when required. Send a PR only when the program or maintainer rules allow it, or after the maintainer confirms they want a fix.
- Keep proof local and synthetic: mocked tokens, seeded fixtures, local containers, and redacted logs.

## Current Targets To Investigate

| Target | Source | Why It Fits | Next Action | Revenue Rule |
| --- | --- | --- | --- | --- |
| HackerOne public programs | https://www.hackerone.com/bug-bounty-programs | Public list of programs that can offer bounties and rules of engagement. | Filter for open-source/web programs with explicit safe-harbor and no invite gate. | Count only paid HackerOne bounty after payout evidence. |
| DevNetwork AI + ML Hackathon / TrueFoundry resilient agents | https://devnetwork-ai-ml-hack-2026.devpost.com/ | Prize path for a buildable resilient-agent artifact; not a vulnerability exploit. | Build an agent failure lab with simulated MCP/provider outages and clear logs. | Count only awarded and paid prize net of costs. |
| Algora/GitHub bounty issues | https://algora.io/projectdiscovery/bounties | PR-first payment model on GitHub issues. | Find issues with clear acceptance criteria, no account/private-data access, and tests. | Count only paid bounty after PR acceptance and payment evidence. |

## Current Artifact

`bounties/tsperf-type-lens/` contains a local MIT-licensed VS Code extension prototype for the TSPerf challenge. It has inline CodeLens, heuristic type-complexity scoring, checker materialization timing, and a trace-backed command that runs TypeScript with `--generateTrace` and summarizes hotspots. It is not submitted or published.

Local proof commands:

```bash
cd bounties/tsperf-type-lens
npm test
npm run package
```

Gate before any public action: verify the bounty is still open and payable, create/select a public repo, add repository metadata, record a demo, and get explicit user approval to submit or PR.

## Report Template

1. Scope confirmation: program URL, asset, and rule allowing the test.
2. Local reproduction: exact version, fixture data, commands, and expected/actual behavior.
3. Impact: concrete but bounded. No claims beyond the demonstrated issue.
4. Safety: no real user data, no persistence, no production disruption.
5. Fix path: patch summary, tests, and whether a PR is attached or available on request.
6. Evidence: screenshots, logs, commit links, report ID, bounty ID, payout ID.
