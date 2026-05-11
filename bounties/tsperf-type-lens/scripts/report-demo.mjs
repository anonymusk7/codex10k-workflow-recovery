import fs from "node:fs/promises";
import path from "node:path";
import analyzer from "../dist/analyzer.js";

const { analyzeFile } = analyzer;

const demoFile = path.resolve("demo/slow-types.ts");
const analyses = analyzeFile(demoFile, await fs.readFile(demoFile, "utf8"));
const top = [...analyses].sort((a, b) => b.complexity - a.complexity).slice(0, 6);

console.log("# TSPerf Demo Report");
console.log("");
for (const item of top) {
  console.log(`- ${item.name}: ${item.rating}, C${item.complexity}, ${item.elapsedMs.toFixed(2)}ms`);
  console.log(`  drivers: ${item.drivers.join(", ")}`);
}

console.log("");
console.log("Trace mode can be exercised from VS Code with `TSPerf: Run TypeScript Trace`.");
