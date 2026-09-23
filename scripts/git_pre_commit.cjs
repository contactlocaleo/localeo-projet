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
process.exit(result.status ?? 1);
