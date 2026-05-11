import * as fs from "node:fs";
import * as path from "node:path";
import { performance } from "node:perf_hooks";
import ts from "typescript";

export type Rating = "low" | "medium" | "high" | "extreme";

export interface AnalysisOptions {
  maxDepth?: number;
  maxProperties?: number;
}

export interface TypeAnalysis {
  name: string;
  fileName: string;
  line: number;
  character: number;
  elapsedMs: number;
  complexity: number;
  rating: Rating;
  typePreview: string;
  drivers: string[];
}

interface ProgramContext {
  program: ts.Program;
  sourceFile: ts.SourceFile;
  checker: ts.TypeChecker;
}

const DEFAULT_OPTIONS: Required<AnalysisOptions> = {
  maxDepth: 5,
  maxProperties: 60,
};

export function analyzeFile(fileName: string, sourceText?: string, options: AnalysisOptions = {}): TypeAnalysis[] {
  const config = { ...DEFAULT_OPTIONS, ...options };
  const context = createProgramContext(fileName, sourceText);
  const nodes = collectInterestingNodes(context.sourceFile);
  return nodes.map((node) => analyzeNode(context, node, config));
}

export function analyzePosition(fileName: string, line: number, character: number, sourceText?: string, options: AnalysisOptions = {}): TypeAnalysis | undefined {
  const config = { ...DEFAULT_OPTIONS, ...options };
  const context = createProgramContext(fileName, sourceText);
  const offset = context.sourceFile.getPositionOfLineAndCharacter(line, character);
  const node = findBestNodeAtPosition(context.sourceFile, offset) ?? collectInterestingNodes(context.sourceFile)[0];
  return node ? analyzeNode(context, node, config) : undefined;
}

function createProgramContext(fileName: string, sourceText?: string): ProgramContext {
  const normalized = path.resolve(fileName);
  const options = loadCompilerOptions(normalized);
  const host = ts.createCompilerHost(options, true);
  const originalReadFile = host.readFile.bind(host);
  const originalGetSourceFile = host.getSourceFile.bind(host);

  host.readFile = (requestedFile) => {
    if (path.resolve(requestedFile) === normalized && sourceText !== undefined) {
      return sourceText;
    }
    return originalReadFile(requestedFile);
  };
  host.getSourceFile = (requestedFile, languageVersion, onError, shouldCreateNewSourceFile) => {
    if (path.resolve(requestedFile) === normalized && sourceText !== undefined) {
      return ts.createSourceFile(requestedFile, sourceText, languageVersion, true);
    }
    return originalGetSourceFile(requestedFile, languageVersion, onError, shouldCreateNewSourceFile);
  };

  const program = ts.createProgram([normalized], options, host);
  const sourceFile = program.getSourceFile(normalized);
  if (!sourceFile) {
    throw new Error(`Could not load TypeScript file: ${normalized}`);
  }
  return { program, sourceFile, checker: program.getTypeChecker() };
}

function loadCompilerOptions(fileName: string): ts.CompilerOptions {
  const configPath = ts.findConfigFile(path.dirname(fileName), ts.sys.fileExists, "tsconfig.json");
  if (!configPath) {
    return {
      allowJs: false,
      noEmit: true,
      skipLibCheck: true,
      strict: false,
      target: ts.ScriptTarget.ES2022,
      module: ts.ModuleKind.Node16,
      moduleResolution: ts.ModuleResolutionKind.Node16,
    };
  }
  const configFile = ts.readConfigFile(configPath, ts.sys.readFile);
  if (configFile.error) {
    return { noEmit: true, skipLibCheck: true };
  }
  const parsed = ts.parseJsonConfigFileContent(configFile.config, ts.sys, path.dirname(configPath));
  return { ...parsed.options, noEmit: true, skipLibCheck: true };
}

function collectInterestingNodes(sourceFile: ts.SourceFile): ts.Node[] {
  const nodes: ts.Node[] = [];
  const visit = (node: ts.Node) => {
    if (
      ts.isTypeAliasDeclaration(node) ||
      ts.isInterfaceDeclaration(node) ||
      ts.isClassDeclaration(node) ||
      ts.isEnumDeclaration(node) ||
      ts.isFunctionDeclaration(node) ||
      ts.isVariableDeclaration(node)
    ) {
      nodes.push(node);
    }
    ts.forEachChild(node, visit);
  };
  visit(sourceFile);
  return nodes;
}

function findBestNodeAtPosition(sourceFile: ts.SourceFile, offset: number): ts.Node | undefined {
  let best: ts.Node | undefined;
  const visit = (node: ts.Node) => {
    if (offset < node.getFullStart() || offset > node.getEnd()) {
      return;
    }
    if (isAnalyzable(node)) {
      best = node;
    }
    ts.forEachChild(node, visit);
  };
  visit(sourceFile);
  return best;
}

function isAnalyzable(node: ts.Node): boolean {
  return (
    ts.isTypeAliasDeclaration(node) ||
    ts.isInterfaceDeclaration(node) ||
    ts.isClassDeclaration(node) ||
    ts.isEnumDeclaration(node) ||
    ts.isFunctionDeclaration(node) ||
    ts.isVariableDeclaration(node) ||
    ts.isTypeNode(node)
  );
}

function analyzeNode(context: ProgramContext, node: ts.Node, options: Required<AnalysisOptions>): TypeAnalysis {
  const target = analysisTarget(node);
  const start = performance.now();
  const type = context.checker.getTypeAtLocation(target);
  const typePreview = context.checker.typeToString(type, target, ts.TypeFormatFlags.NoTruncation | ts.TypeFormatFlags.InTypeAlias);
  const elapsedMs = performance.now() - start;
  const drivers: string[] = [];
  const complexity = scoreType(context.checker, type, target, options, drivers, new Set(), 0);
  const position = context.sourceFile.getLineAndCharacterOfPosition(node.getStart(context.sourceFile));

  return {
    name: nodeName(node),
    fileName: context.sourceFile.fileName,
    line: position.line,
    character: position.character,
    elapsedMs,
    complexity,
    rating: ratingFor(complexity, elapsedMs),
    typePreview: trimPreview(typePreview),
    drivers: summarizeDrivers(drivers),
  };
}

function analysisTarget(node: ts.Node): ts.Node {
  if (ts.isTypeAliasDeclaration(node)) return node.type;
  if (ts.isInterfaceDeclaration(node) || ts.isEnumDeclaration(node)) return node.name;
  if (ts.isClassDeclaration(node)) return node.name ?? node;
  if (ts.isFunctionDeclaration(node)) return node.type ?? node.name ?? node;
  if (ts.isVariableDeclaration(node)) return node.type ?? node.name;
  return node;
}

function nodeName(node: ts.Node): string {
  const maybeNamed = node as ts.Node & { name?: ts.Node };
  if (maybeNamed.name && ts.isIdentifier(maybeNamed.name)) {
    return maybeNamed.name.text;
  }
  if (ts.isVariableDeclaration(node)) {
    return node.name.getText();
  }
  return node.getText().slice(0, 64);
}

function scoreType(
  checker: ts.TypeChecker,
  type: ts.Type,
  anchor: ts.Node,
  options: Required<AnalysisOptions>,
  drivers: string[],
  seen: Set<number>,
  depth: number,
): number {
  if (depth > options.maxDepth) {
    drivers.push("depth cap");
    return 4;
  }
  if (isPrimitiveLike(type)) {
    return 1;
  }
  if (isCompilerLibraryType(type)) {
    drivers.push("compiler-library type");
    return 2;
  }
  const id = typeIdentity(type);
  if (seen.has(id)) {
    drivers.push("recursive reference");
    return 2;
  }
  seen.add(id);

  let score = 1;
  if (type.isUnion()) {
    score += type.types.length * 2;
    drivers.push(`union:${type.types.length}`);
    for (const child of type.types.slice(0, 20)) {
      score += scoreType(checker, child, anchor, options, drivers, seen, depth + 1);
    }
  }
  if (type.isIntersection()) {
    score += type.types.length * 3;
    drivers.push(`intersection:${type.types.length}`);
    for (const child of type.types.slice(0, 20)) {
      score += scoreType(checker, child, anchor, options, drivers, seen, depth + 1);
    }
  }

  const properties = checker.getPropertiesOfType(type);
  if (properties.length) {
    const inspected = Math.min(properties.length, options.maxProperties);
    score += inspected;
    drivers.push(`properties:${properties.length}`);
    for (const property of properties.slice(0, inspected)) {
      const declaration = property.valueDeclaration ?? property.declarations?.[0] ?? anchor;
      try {
        const propertyType = checker.getTypeOfSymbolAtLocation(property, declaration);
        score += Math.min(25, scoreType(checker, propertyType, declaration, options, drivers, seen, depth + 1));
      } catch {
        score += 1;
        drivers.push("property-error");
      }
    }
    if (properties.length > inspected) {
      score += properties.length - inspected;
      drivers.push("property cap");
    }
  }

  const callSignatures = checker.getSignaturesOfType(type, ts.SignatureKind.Call);
  if (callSignatures.length) {
    score += callSignatures.length * 4;
    drivers.push(`call-signatures:${callSignatures.length}`);
  }
  const constructSignatures = checker.getSignaturesOfType(type, ts.SignatureKind.Construct);
  if (constructSignatures.length) {
    score += constructSignatures.length * 4;
    drivers.push(`construct-signatures:${constructSignatures.length}`);
  }

  const typeArgs = checker.getTypeArguments(type as ts.TypeReference);
  if (typeArgs.length) {
    score += typeArgs.length * 2;
    drivers.push(`type-args:${typeArgs.length}`);
    for (const arg of typeArgs.slice(0, 12)) {
      score += scoreType(checker, arg, anchor, options, drivers, seen, depth + 1);
    }
  }

  seen.delete(id);
  return score;
}

function typeIdentity(type: ts.Type): number {
  return (type as ts.Type & { id?: number }).id ?? type.flags;
}

function isPrimitiveLike(type: ts.Type): boolean {
  const primitiveFlags =
    ts.TypeFlags.StringLike |
    ts.TypeFlags.NumberLike |
    ts.TypeFlags.BooleanLike |
    ts.TypeFlags.BigIntLike |
    ts.TypeFlags.ESSymbolLike |
    ts.TypeFlags.Null |
    ts.TypeFlags.Undefined |
    ts.TypeFlags.Void |
    ts.TypeFlags.Never |
    ts.TypeFlags.Any |
    ts.TypeFlags.Unknown;
  return (type.flags & primitiveFlags) !== 0;
}

function isCompilerLibraryType(type: ts.Type): boolean {
  const declarations = type.symbol?.declarations ?? type.aliasSymbol?.declarations ?? [];
  return declarations.some((declaration) => {
    const fileName = declaration.getSourceFile().fileName.replaceAll("\\", "/");
    return /\/node_modules\/typescript\/lib\/lib\..+\.d\.ts$/.test(fileName) || /\/typescript\/lib\/lib\..+\.d\.ts$/.test(fileName);
  });
}

function ratingFor(complexity: number, elapsedMs: number): Rating {
  if (complexity >= 220 || elapsedMs >= 80) return "extreme";
  if (complexity >= 100 || elapsedMs >= 35) return "high";
  if (complexity >= 35 || elapsedMs >= 10) return "medium";
  return "low";
}

function trimPreview(value: string): string {
  return value.length > 360 ? `${value.slice(0, 357)}...` : value;
}

function summarizeDrivers(drivers: string[]): string[] {
  const counts = new Map<string, number>();
  for (const driver of drivers) {
    counts.set(driver, (counts.get(driver) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([driver, count]) => (count > 1 ? `${driver} x${count}` : driver));
}
