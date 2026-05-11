# TSPerf Type Lens

Prototype VS Code extension for the Algora TSPerf challenge.

It shows a CodeLens above TypeScript type declarations with:

- checker load time in milliseconds
- structural complexity score
- low/medium/high/extreme rating
- top drivers such as union width, property count, signatures, and recursion depth

The extension also adds `TSPerf: Analyze Type at Cursor`, which prints a focused report for the selected type or nearest declaration.

For slower but more compiler-native timing, `TSPerf: Run TypeScript Trace` resolves the nearest `tsconfig.json`, runs the workspace TypeScript compiler with `--generateTrace`, and summarizes the slowest trace events in the extension output panel.

## Why this fits the bounty

The challenge asks for an MIT-licensed VS Code plugin that shows the complexity and time-to-load of a TypeScript type. This prototype measures the local TypeScript checker operation for a symbol and produces a deterministic complexity score from the materialized type graph.

## Safety and scope

This is a local developer tool. It does not call external services, upload source code, read credentials, or contact a remote API.

## Development

```bash
npm install
npm test
```

To try it in VS Code, run `npm run compile`, then launch an Extension Development Host from this folder.

## Current limits

- CodeLens time measures TypeScript checker materialization in the local extension process, not tsserver internals.
- Trace mode uses TypeScript's public `--generateTrace` output, whose event shape can change between TypeScript versions.
- Complexity is a heuristic score, not an official TypeScript compiler metric.
- Very large projects can be expensive; recursion and property inspection are capped.
