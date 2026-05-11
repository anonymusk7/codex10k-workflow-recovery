import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { spawnSync } from "node:child_process";
import ts from "typescript";

export interface TraceHotspot {
  name: string;
  category: string;
  elapsedMs: number;
  file?: string;
  line?: number;
  character?: number;
  detail?: string;
}

export interface TraceResult {
  traceDir: string;
  tsconfigPath: string;
  elapsedMs: number;
  hotspots: TraceHotspot[];
  rawEventCount: number;
  diagnostics: string[];
}

interface TraceEvent {
  name?: string;
  cat?: string;
  ph?: string;
  dur?: number;
  ts?: number;
  args?: Record<string, unknown>;
}

const HOT_EVENT_NAMES = new Set([
  "checkSourceFile",
  "checkExpression",
  "checkVariableDeclaration",
  "checkDeferredNode",
  "structuredTypeRelatedTo",
  "getVariancesWorker",
  "createProgram",
  "bindSourceFile",
]);

export function runTypeScriptTrace(startPath: string, outDir?: string): TraceResult {
  const tsconfigPath = findTsconfig(startPath);
  const traceDir = outDir ?? fs.mkdtempSync(path.join(os.tmpdir(), "tsperf-trace-"));
  const start = performance.now();
  const tscBin = resolveTscBin(tsconfigPath);
  const proc = spawnSync(
    process.execPath,
    [tscBin, "-p", tsconfigPath, "--generateTrace", traceDir, "--incremental", "false", "--pretty", "false"],
    { encoding: "utf8", cwd: path.dirname(tsconfigPath), maxBuffer: 1024 * 1024 * 20 },
  );
  const elapsedMs = performance.now() - start;
  const diagnostics = [proc.stdout, proc.stderr].filter(Boolean).join("\n").split(/\r?\n/).filter(Boolean);
  const tracePath = path.join(traceDir, "trace.json");
  const raw = fs.existsSync(tracePath) ? JSON.parse(fs.readFileSync(tracePath, "utf8")) as TraceEvent[] : [];
  const sourceFile = resolvePrimarySource(startPath);
  const sourceText = sourceFile && fs.existsSync(sourceFile) ? fs.readFileSync(sourceFile, "utf8") : undefined;
  const lineMap = sourceText ? buildLineMap(sourceText) : undefined;

  const hotspots = raw
    .filter((event) => event.ph === "X" && typeof event.dur === "number")
    .filter((event) => (event.name && HOT_EVENT_NAMES.has(event.name)) || (event.dur ?? 0) >= 5000)
    .map((event) => toHotspot(event, sourceFile, lineMap))
    .sort((a, b) => b.elapsedMs - a.elapsedMs)
    .slice(0, 40);

  return {
    traceDir,
    tsconfigPath,
    elapsedMs,
    hotspots,
    rawEventCount: raw.length,
    diagnostics,
  };
}

export function findTsconfig(startPath: string): string {
  const base = fs.statSync(startPath).isDirectory() ? startPath : path.dirname(startPath);
  const configPath = ts.findConfigFile(base, ts.sys.fileExists, "tsconfig.json");
  if (!configPath) {
    throw new Error(`No tsconfig.json found above ${base}`);
  }
  return configPath;
}

function resolveTscBin(tsconfigPath: string): string {
  const local = path.join(path.dirname(tsconfigPath), "node_modules", "typescript", "bin", "tsc");
  if (fs.existsSync(local)) {
    return local;
  }
  return require.resolve("typescript/bin/tsc");
}

function resolvePrimarySource(startPath: string): string | undefined {
  if (!fs.existsSync(startPath)) {
    return undefined;
  }
  const stat = fs.statSync(startPath);
  return stat.isDirectory() ? undefined : path.resolve(startPath);
}

function toHotspot(event: TraceEvent, sourceFile: string | undefined, lineMap: number[] | undefined): TraceHotspot {
  const args = event.args ?? {};
  const pos = typeof args.pos === "number" ? args.pos : undefined;
  const location = pos !== undefined && lineMap ? positionFor(lineMap, pos) : undefined;
  const pathArg = typeof args.path === "string" ? args.path : undefined;
  return {
    name: event.name ?? "trace event",
    category: event.cat ?? "trace",
    elapsedMs: (event.dur ?? 0) / 1000,
    file: pathArg ?? sourceFile,
    line: location?.line,
    character: location?.character,
    detail: formatDetail(args),
  };
}

function buildLineMap(text: string): number[] {
  const starts = [0];
  for (let index = 0; index < text.length; index += 1) {
    if (text.charCodeAt(index) === 10) {
      starts.push(index + 1);
    }
  }
  return starts;
}

function positionFor(lineStarts: number[], offset: number): { line: number; character: number } {
  let low = 0;
  let high = lineStarts.length - 1;
  while (low <= high) {
    const mid = Math.floor((low + high) / 2);
    if (lineStarts[mid] <= offset) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  const line = Math.max(0, high);
  return { line, character: Math.max(0, offset - lineStarts[line]) };
}

function formatDetail(args: Record<string, unknown>): string {
  const interesting = ["path", "pos", "end", "kind", "typeId", "sourceId", "targetId"];
  return interesting
    .filter((key) => args[key] !== undefined)
    .map((key) => `${key}=${String(args[key])}`)
    .join(" ");
}
