'use strict';
const { execFileSync, spawnSync } = require('node:child_process');
let python;
try {
  python = execFileSync('git', ['config', '--local', '--get', 'localeo.python'], { encoding: 'utf8', windowsHide: true }).trim();
} catch {
  process.stderr.write('Hook Localeo non configure : python scripts/install_hooks.py --install\n');
  process.exit(1);
}
if (!python) process.exit(1);
const result = spawnSync(python, ['scripts/check_guidance.py', '--repo', '.', '--staged', '--changed', '--all-markdown'], { stdio: 'inherit', windowsHide: true });
if (result.error) process.stderr.write('Python du hook indisponible ; relancer scripts/install_hooks.py --install avec le Python actif.\n');
if (result.status !== 0) process.exit(result.status ?? 1);

let changed;
try {
  // Disabling rename detection also exposes a removed configuration path.
  changed = execFileSync('git', ['diff', '--cached', '--name-only', '--no-renames', '-z'], { encoding: 'utf8', windowsHide: true }).split('\0');
} catch {
  process.stderr.write('Index Git indisponible pour le controle des workflows Codex.\n');
  process.exit(1);
}
const workflowInputs = /^(?:AGENTS\.md|\.agents\/skills\/.*|\.codex\/agents\/.*\.toml|\.codex\/hooks\.json|\.githooks\/pre-commit|\.pre-commit-config\.yaml|scripts\/(?:check_codex_workflows\.py|git_pre_commit\.cjs|codex_(?:context|finish)\.cjs))$/;
if (!changed.some(file => workflowInputs.test(file))) process.exit(0);

const workflows = spawnSync(python, ['scripts/check_codex_workflows.py', '--repo', '.', '--staged'], { stdio: 'inherit', windowsHide: true });
if (workflows.error) process.stderr.write('Controle des workflows Codex indisponible.\n');
process.exit(workflows.status ?? 1);
