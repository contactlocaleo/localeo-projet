'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { finishOutput } = require('../scripts/codex_finish.cjs');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

test('clean workspaces produce no noisy reminder and no completion claim', () => {
  assert.deepEqual(finishOutput([{ name: 'repo', state: 'propre' }]), {});
});
test('unknown and dirty states remain advisory without forcing continuation or approval', () => {
  for (const state of ['absent', 'modifie', 'non-verifie']) {
    const output = finishOutput([{ name: 'private-name', state }]);
    assert.ok(output.systemMessage);
    assert.deepEqual(Object.keys(output), ['systemMessage']);
    assert.ok(!JSON.stringify(output).includes('private-name'));
  }
});

test('configured commands emit valid hook JSON from a repository subdirectory', () => {
  const root = path.resolve(__dirname, '..');
  const definition = JSON.parse(fs.readFileSync(path.join(root, '.codex/hooks.json'), 'utf8'));
  for (const event of ['SessionStart', 'Stop']) {
    const handler = definition.hooks[event][0].hooks[0];
    const shells = process.platform === 'win32'
      ? [['powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', handler.commandWindows]], ['cmd.exe', ['/d', '/s', '/c', handler.commandWindows]]]
      : [['sh', ['-c', handler.command]]];
    for (const [shell, args] of shells) {
      const result = JSON.parse(execFileSync(shell, args, { cwd: path.join(root, 'docs'), encoding: 'utf8', timeout: 15000, windowsHide: true, windowsVerbatimArguments: shell === 'cmd.exe' }));
      if (event === 'SessionStart') assert.equal(result.hookSpecificOutput.hookEventName, event);
      assert.equal(result.decision, undefined);
      assert.equal(result.continue, undefined);
    }
  }
});
