# TSPerf Submission Notes

Status: local proof built; do not submit or publish without explicit approval.

## What Works

- MIT-licensed VS Code extension scaffold.
- Inline CodeLens for TypeScript and TSX declarations.
- Heuristic complexity scoring from the TypeScript checker graph.
- Checker materialization timing for selected declarations.
- `TSPerf: Analyze Type at Cursor` output report.
- `TSPerf: Run TypeScript Trace` command that runs `tsc --generateTrace`, parses `trace.json`, and summarizes hotspots.
- Local tests cover analyzer output, positional analysis, `tsconfig` discovery, and trace parsing.
- Local VSIX package was generated successfully at `tsperf-type-lens-0.1.0.vsix`; it is ignored from git until submission is approved.

## Evidence

```bash
npm install
npm test
npm run package
```

Latest local result:

- `npm test`: passed.
- `npm run package`: passed; warning only for missing public repository metadata.

## Before Submission

1. Verify the Algora TSPerf challenge is still open and payable.
2. Create or select a public repository approved by the user.
3. Add repository metadata to `package.json`.
4. Record a short demo video in VS Code showing CodeLens and trace mode on a slow conditional/generic type.
5. Compare trace hotspots against `npx analyze-trace` on one fixture.
6. Submit only through the challenge's allowed path.
