#!/usr/bin/env node
// Run only central rules; never import configuration from the consumer repository.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { lint } from 'markdownlint/promise';

const tools = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repository = resolve(process.argv[2] ?? '.');
try {
  const output = execFileSync(process.env.PYTHON ?? 'python3', [
    resolve(tools, 'scripts/validate_docs.py'), '--list-markdown', repository,
  ], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  const files = JSON.parse(output).map((path) => resolve(repository, path));
  const config = JSON.parse(readFileSync(resolve(tools, '.markdownlint.json'), 'utf8'));
  const results = await lint({ files, config, noInlineConfig: true });
  const findings = Object.entries(results).flatMap(([file, issues]) =>
    issues.map((issue) => `${file}:${issue.lineNumber}: ${issue.ruleNames[0]} ${issue.ruleDescription}${issue.errorDetail ? ` (${issue.errorDetail})` : ''}`)
  ).join('\n');
  if (findings) {
    console.log(findings);
    process.exitCode = 1;
  } else {
    console.log(`Markdown formatting passed (${files.length} files).`);
  }
} catch (error) {
  console.error(error.stdout?.toString() || error.message);
  process.exitCode = 1;
}
