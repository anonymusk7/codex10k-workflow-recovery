import * as vscode from "vscode";
import { analyzeFile, analyzePosition, TypeAnalysis } from "./analyzer";
import { runTypeScriptTrace } from "./trace";

const supportedLanguages = new Set(["typescript", "typescriptreact"]);

export function activate(context: vscode.ExtensionContext) {
  const output = vscode.window.createOutputChannel("TSPerf Type Lens");
  const provider = new TypePerfCodeLensProvider();

  context.subscriptions.push(output);
  context.subscriptions.push(
    vscode.languages.registerCodeLensProvider(
      [{ language: "typescript" }, { language: "typescriptreact" }],
      provider,
    ),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("tsperf.refreshTypeLens", () => {
      provider.refresh();
    }),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("tsperf.analyzeTypeAtCursor", async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor || !supportedLanguages.has(editor.document.languageId)) {
        vscode.window.showWarningMessage("Open a TypeScript file before running TSPerf.");
        return;
      }
      const analysis = analyzePosition(
        editor.document.fileName,
        editor.selection.active.line,
        editor.selection.active.character,
        editor.document.getText(),
        readOptions(),
      );
      if (!analysis) {
        vscode.window.showInformationMessage("TSPerf did not find a type near the cursor.");
        return;
      }
      output.clear();
      writeAnalysis(output, analysis);
      output.show(true);
    }),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("tsperf.runTrace", async () => {
      const editor = vscode.window.activeTextEditor;
      const startPath = editor?.document.fileName ?? vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
      if (!startPath) {
        vscode.window.showWarningMessage("Open a TypeScript workspace or file before running TSPerf trace.");
        return;
      }
      await vscode.window.withProgress(
        {
          location: vscode.ProgressLocation.Notification,
          title: "TSPerf running TypeScript trace",
          cancellable: false,
        },
        async () => {
          const result = runTypeScriptTrace(startPath);
          output.clear();
          output.appendLine(`Trace dir: ${result.traceDir}`);
          output.appendLine(`tsconfig: ${result.tsconfigPath}`);
          output.appendLine(`Total command time: ${result.elapsedMs.toFixed(1)}ms`);
          output.appendLine(`Trace events: ${result.rawEventCount}`);
          output.appendLine("");
          output.appendLine("Top trace hotspots:");
          const threshold = vscode.workspace.getConfiguration("tsperf").get<number>("traceHotspotThresholdMs", 5);
          for (const hotspot of result.hotspots.filter((item) => item.elapsedMs >= threshold).slice(0, 25)) {
            const location = hotspot.file ? `${hotspot.file}${hotspot.line !== undefined ? `:${hotspot.line + 1}:${(hotspot.character ?? 0) + 1}` : ""}` : "unknown";
            output.appendLine(`- ${hotspot.elapsedMs.toFixed(2)}ms ${hotspot.name} ${location} ${hotspot.detail ?? ""}`.trim());
          }
          if (result.diagnostics.length) {
            output.appendLine("");
            output.appendLine("Compiler output:");
            for (const line of result.diagnostics.slice(0, 80)) output.appendLine(line);
          }
          output.show(true);
        },
      );
    }),
  );
}

export function deactivate() {
  // VS Code disposes registered subscriptions.
}

class TypePerfCodeLensProvider implements vscode.CodeLensProvider {
  private readonly onDidChangeEmitter = new vscode.EventEmitter<void>();
  readonly onDidChangeCodeLenses = this.onDidChangeEmitter.event;

  refresh() {
    this.onDidChangeEmitter.fire();
  }

  provideCodeLenses(document: vscode.TextDocument): vscode.CodeLens[] {
    if (!supportedLanguages.has(document.languageId)) {
      return [];
    }
    try {
      const analyses = analyzeFile(document.fileName, document.getText(), readOptions());
      return analyses.map((analysis) => toCodeLens(document, analysis));
    } catch (error) {
      return [
        new vscode.CodeLens(new vscode.Range(0, 0, 0, 0), {
          title: `TSPerf unavailable: ${error instanceof Error ? error.message : "analysis failed"}`,
          command: "tsperf.refreshTypeLens",
        }),
      ];
    }
  }
}

function readOptions() {
  const config = vscode.workspace.getConfiguration("tsperf");
  return {
    maxDepth: config.get<number>("maxDepth", 5),
    maxProperties: config.get<number>("maxProperties", 60),
  };
}

function toCodeLens(document: vscode.TextDocument, analysis: TypeAnalysis): vscode.CodeLens {
  const range = new vscode.Range(analysis.line, analysis.character, analysis.line, analysis.character);
  const title = `TSPerf: ${analysis.rating} C${analysis.complexity} / ${analysis.elapsedMs.toFixed(1)}ms`;
  return new vscode.CodeLens(range, {
    title,
    command: "tsperf.analyzeTypeAtCursor",
    arguments: [document.uri, analysis.line, analysis.character],
    tooltip: `${analysis.name}: ${analysis.typePreview}`,
  });
}

function writeAnalysis(output: vscode.OutputChannel, analysis: TypeAnalysis) {
  output.appendLine(`Name: ${analysis.name}`);
  output.appendLine(`Rating: ${analysis.rating}`);
  output.appendLine(`Complexity: ${analysis.complexity}`);
  output.appendLine(`Checker load time: ${analysis.elapsedMs.toFixed(2)}ms`);
  output.appendLine(`Location: ${analysis.fileName}:${analysis.line + 1}:${analysis.character + 1}`);
  output.appendLine("");
  output.appendLine("Type preview:");
  output.appendLine(analysis.typePreview);
  output.appendLine("");
  output.appendLine("Drivers:");
  for (const driver of analysis.drivers) {
    output.appendLine(`- ${driver}`);
  }
}
