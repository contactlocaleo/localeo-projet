'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { inspectWorkspace, hookOutput } = require('../scripts/codex_context.cjs');
test('missing, modified, clean and unavailable Git remain distinct without leaking filenames', () => {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'localeo-context-'));
  try {
    for (const name of ['localeo-projet', 'localeo-backend', 'localeo-commercant', 'localeo-marketplace']) {
      fs.mkdirSync(path.join(base, name), { recursive: true });
      fs.writeFileSync(path.join(base, name, '.git'), 'gitdir: fixture');
    }
    const states = inspectWorkspace(path.join(base, 'localeo-projet'), (repo) => {
      if (repo.endsWith('backend')) return '?? secret-value-never-output.env\n';
      if (repo.endsWith('commercant')) throw new Error('unavailable');
      return '';
    });
    assert.equal(states.find(r => r.name === 'localeo-animation').state, 'absent');
    assert.equal(states.find(r => r.name === 'localeo-backend').state, 'modifie');
    assert.equal(states.find(r => r.name === 'localeo-commercant').state, 'non-verifie');
    assert.equal(states.find(r => r.name === 'localeo-projet').state, 'propre');
    const output = hookOutput(states);
    assert.equal(output.hookSpecificOutput.hookEventName, 'SessionStart');
    assert.ok(!JSON.stringify(output).includes('secret-value'));
    assert.ok(output.hookSpecificOutput.additionalContext.length < 1800);
    assert.equal(output.decision, undefined);
    assert.equal(output.continue, undefined);
  } finally { fs.rmSync(base, { recursive: true, force: true }); }
});
