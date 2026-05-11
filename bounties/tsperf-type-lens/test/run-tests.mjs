import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { analyzeFile, analyzePosition } from "../dist/analyzer.js";
import { findTsconfig, runTypeScriptTrace } from "../dist/trace.js";

const dir = await fs.mkdtemp(path.join(os.tmpdir(), "tsperf-type-lens-"));
const file = path.join(dir, "fixture.ts");
await fs.writeFile(
  path.join(dir, "tsconfig.json"),
  JSON.stringify({ compilerOptions: { strict: true, noEmit: true, skipLibCheck: true, target: "ES2022" }, include: ["fixture.ts"] }, null, 2),
);
await fs.writeFile(
  file,
  `
type Primitive = string | number | boolean;
type Box<T> = { value: T; meta: { createdAt: Date; tags: string[] } };
type LargeUnion =
  | { kind: "a"; payload: Box<Primitive> }
  | { kind: "b"; payload: Box<Primitive[]> }
  | { kind: "c"; payload: Box<Record<string, Primitive>> };
interface ApiResponse {
  id: string;
  result: LargeUnion;
  retry(): Promise<LargeUnion>;
}
const current: ApiResponse = {} as ApiResponse;
`,
);

const analyses = analyzeFile(file);
assert.ok(analyses.length >= 4, "expected several analyzable declarations");

const largeUnion = analyses.find((item) => item.name === "LargeUnion");
assert.ok(largeUnion, "expected LargeUnion analysis");
assert.ok(largeUnion.complexity > 10, "expected non-trivial complexity");
assert.ok(largeUnion.elapsedMs >= 0, "expected elapsed time");
assert.ok(largeUnion.drivers.length > 0, "expected complexity drivers");

const positional = analyzePosition(file, 8, 12);
assert.ok(positional, "expected positional analysis");
assert.ok(positional.complexity > 0, "expected positional complexity");
assert.ok(positional.typePreview.length > 0, "expected positional type preview");

assert.equal(findTsconfig(file), path.join(dir, "tsconfig.json"));
const trace = runTypeScriptTrace(file, path.join(dir, "trace"));
assert.ok(trace.rawEventCount > 0, "expected trace events");
assert.ok(trace.hotspots.length > 0, "expected trace hotspots");

console.log("TSPerf analyzer tests passed");
