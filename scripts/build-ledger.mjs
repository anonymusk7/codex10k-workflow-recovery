import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = new URL("../outputs/codex10k/", import.meta.url);
const prospectsCsv = new URL("../data/prospects.csv", import.meta.url);
const ledgerCsv = new URL("../data/ledger.csv", import.meta.url);

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (char === '"' && quoted && next === '"') {
      cell += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(cell);
      cell = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") {
        index += 1;
      }
      row.push(cell);
      if (row.some((value) => value.length > 0)) {
        rows.push(row);
      }
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }

  row.push(cell);
  if (row.some((value) => value.length > 0)) {
    rows.push(row);
  }

  return rows.map((csvRow) => csvRow.map((value) => {
    if (value === "") return null;
    const numeric = Number(value);
    return Number.isFinite(numeric) && value.trim() !== "" ? numeric : value;
  }));
}

const prospectsRaw = parseCsv(await fs.readFile(prospectsCsv, "utf8"));
const ledgerRaw = parseCsv(await fs.readFile(ledgerCsv, "utf8"));

const prospects = [
  ["Lead ID", "Created", "Label Namespace", "Company", "Contact", "Channel", "Source URL", "Segment", "Problem Hypothesis", "Offer", "Status", "Last Touch", "Next Action", "Follow-up Date", "Evidence", "Notes"],
  ...prospectsRaw.slice(1),
];

const ledger = [
  ["Date", "Event ID", "Counterparty", "Channel", "Description", "Gross Revenue", "Payment Fees", "Platform Fees", "Direct Costs", "Refunds", "Net Profit", "Status", "Transaction ID", "Evidence URI", "Notes"],
  ...ledgerRaw.slice(1),
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
dashboard.getRange("B8").formulas = [["=COUNTIFS(Prospects!K2:K200,\"<>initialized\",Prospects!K2:K200,\"<>hold_employment_style\",Prospects!K2:K200,\"<>bounced\",Prospects!K2:K200,\"<>\")"]];
dashboard.getRange("B9").formulas = [["=COUNTIF(Prospects!K2:K200,\"interested\") + COUNTIF(Prospects!K2:K200,\"proposal_sent\") + COUNTIF(Prospects!K2:K200,\"invoice_sent\") + COUNTIF(Prospects!K2:K200,\"paid\")"]];
dashboard.getRange("D3:F7").values = [
  ["Run Label", "Codex10k", ""],
  ["Primary Offer", "10-Day Workflow Revenue Recovery Sprint", ""],
  ["Target Close Pattern", "2 sprint clients at $6k+ or 3 at $4.8k", ""],
  ["Payment Evidence", "Invoice, transaction ID, payout proof, fee receipt", ""],
  ["Rule", "Count settled revenue only", ""],
];

ledgerSheet.getRange(`A1:O${ledger.length}`).values = ledger;
ledgerSheet.getRange("K2").formulas = [["=F2-G2-H2-I2-J2"]];

prospectsSheet.getRange(`A1:P${prospects.length}`).values = prospects;

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
