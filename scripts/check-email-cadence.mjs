import fs from "node:fs";

const DEFAULT_CAP = 10;
const ABSOLUTE_CAP = 20;
const MIN_SPACING_MINUTES = 15;

const args = new Map(process.argv.slice(2).map((arg) => {
  const [key, value = "true"] = arg.replace(/^--/, "").split("=");
  return [key, value];
}));

const cap = Math.min(Number(args.get("cap") || DEFAULT_CAP), ABSOLUTE_CAP);
const proposedAt = args.has("proposed-at") ? new Date(args.get("proposed-at")) : new Date();
if (!Number.isFinite(cap) || cap <= 0) {
  throw new Error("--cap must be a positive number");
}
if (Number.isNaN(proposedAt.getTime())) {
  throw new Error("--proposed-at must be a valid date or ISO timestamp");
}

function localDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (char === "\"" && quoted && next === "\"") {
      cell += "\"";
      index += 1;
    } else if (char === "\"") {
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

  return rows;
}

function rowsByHeader(path) {
  if (!fs.existsSync(path)) {
    return [];
  }
  const rows = parseCsv(fs.readFileSync(path, "utf8"));
  if (rows.length < 2) {
    return [];
  }
  const header = rows[0];
  return rows.slice(1).map((row) => Object.fromEntries(header.map((key, index) => [key, row[index] || ""])));
}

const day = args.get("date") || localDate(proposedAt);
const prospects = rowsByHeader("data/prospects.csv");
const sendLog = rowsByHeader("data/email-send-log.csv");

const legacyProspectSends = prospects.filter((row) => (
  row.last_touch === day
  && /gmail:19e/.test(row.evidence_uri || "")
));

const exactSends = sendLog
  .filter((row) => row.status === "sent" && row.sent_at_iso)
  .map((row) => ({ ...row, sentAt: new Date(row.sent_at_iso) }))
  .filter((row) => !Number.isNaN(row.sentAt.getTime()) && localDate(row.sentAt) === day)
  .sort((a, b) => a.sentAt - b.sentAt);

const knownCount = Math.max(legacyProspectSends.length, exactSends.length);
const lastExactSend = exactSends.at(-1);
const minutesSinceLast = lastExactSend
  ? (proposedAt - lastExactSend.sentAt) / 60000
  : null;

const blockers = [];
if (knownCount >= cap) {
  blockers.push(`daily cap reached: ${knownCount}/${cap}`);
}
if (minutesSinceLast !== null && minutesSinceLast < MIN_SPACING_MINUTES) {
  blockers.push(`minimum spacing not met: ${minutesSinceLast.toFixed(1)} minutes since last send`);
}

const result = {
  allowed: blockers.length === 0,
  day,
  cap,
  absoluteCap: ABSOLUTE_CAP,
  minSpacingMinutes: MIN_SPACING_MINUTES,
  knownOutboundCount: knownCount,
  legacyProspectCount: legacyProspectSends.length,
  exactLoggedCount: exactSends.length,
  lastExactSendAt: lastExactSend?.sent_at_iso || null,
  minutesSinceLastExactSend: minutesSinceLast === null ? null : Number(minutesSinceLast.toFixed(1)),
  blockers,
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.allowed ? 0 : 2);
