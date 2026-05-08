import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = new URL("../outputs/codex10k/", import.meta.url);

const prospects = [
  [
    "Lead ID",
    "Company",
    "Channel",
    "Segment",
    "Problem Hypothesis",
    "Offer",
    "Status",
    "Next Action",
    "Follow-up Date",
    "Evidence",
  ],
  [
    "C10K-000",
    "Internal",
    "Workspace",
    "Run setup",
    "Independent Codex10k pipeline initialized",
    "10-Day Workflow Revenue Recovery Sprint",
    "Initialized",
    "Begin fresh lead sourcing",
    "",
    "docs/research.md",
  ],
];

const ledger = [
  [
    "Date",
    "Event ID",
    "Counterparty",
    "Channel",
    "Description",
    "Gross Revenue",
    "Payment Fees",
    "Platform Fees",
    "Direct Costs",
    "Refunds",
    "Net Profit",
    "Status",
    "Transaction ID",
    "Evidence URI",
  ],
  [
    "2026-05-08",
    "LEDGER-000",
    "Internal",
    "Workspace",
    "Codex10k ledger initialized",
    0,
    0,
    0,
    0,
    0,
    0,
    "Initialized",
    "",
    "docs/research.md",
  ],
];

const workbook = Workbook.create();
const dashboard = workbook.worksheets.add("Dashboard");
const ledgerSheet = workbook.worksheets.add("Ledger");
const prospectsSheet = workbook.worksheets.add("Prospects");
const assumptions = workbook.worksheets.add("Assumptions");

dashboard.getRange("A1:F1").values = [["Codex10k Verified Profit Dashboard", "", "", "", "", ""]];
dashboard.getRange("A3:B9").values = [
  ["Goal", 10000],
  ["Verified Net Profit", 0],
  ["Remaining", null],
  ["Gross Settled Revenue", 0],
  ["Fees + Costs + Refunds", 0],
  ["Qualified Prospects", 0],
  ["Interested Prospects", 0],
];
dashboard.getRange("B5").formulas = [["=B3-B4"]];
dashboard.getRange("B8").formulas = [["=COUNTA(Prospects!A2:A200)"]];
dashboard.getRange("B9").formulas = [["=COUNTIF(Prospects!G2:G200,\"Interested\")"]];
dashboard.getRange("D3:F7").values = [
  ["Run Label", "Codex10k", ""],
  ["Primary Offer", "10-Day Workflow Revenue Recovery Sprint", ""],
  ["Target Close Pattern", "2 sprint clients at $6k+ or 3 at $4.8k", ""],
  ["Payment Evidence", "Invoice, transaction ID, payout proof, fee receipt", ""],
  ["Rule", "Count settled revenue only", ""],
];

ledgerSheet.getRange(`A1:N${ledger.length}`).values = ledger;
ledgerSheet.getRange("K2").formulas = [["=F2-G2-H2-I2-J2"]];

prospectsSheet.getRange(`A1:J${prospects.length}`).values = prospects;

assumptions.getRange("A1:D9").values = [
  ["Assumption", "Value", "Source", "Notes"],
  ["Stripe U.S. domestic card fee", "2.9% + $0.30", "https://stripe.com/us/pricing", "Use actual fee evidence when available"],
  ["Upwork freelancer service fee", "0%-15%", "https://support.upwork.com/hc/en-us/articles/211062538-Freelancer-Service-Fee", "Varies by contract"],
  ["Upwork Connects", "$0.15 each", "https://support.upwork.com/hc/en-us/articles/34955398999699-Connects", "Treat as direct cost if used"],
  ["Cold commercial email", "Requires CAN-SPAM compliance", "https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business", "Avoid cold email until postal address is available"],
  ["Primary channel", "Public hiring posts + communities", "docs/research.md", "Buyer-intent first"],
  ["Primary price", "$4,800-$7,500", "docs/offer.md", "Fixed-scope sprint"],
  ["Retainer", "$750-$1,500/mo", "docs/offer.md", "Optional after launch"],
  ["Direct costs policy", "Approved before use", "docs/payment-flow.md", "Subtract all costs from net profit"],
];

await fs.mkdir(outputDir, { recursive: true });

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(new URL("codex10k_revenue_tracker.xlsx", outputDir));

const dashInspect = await workbook.inspect({
  kind: "table",
  range: "Dashboard!A1:F9",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 8,
});
console.log(dashInspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

await workbook.render({ sheetName: "Dashboard", range: "A1:F9", scale: 2 });
