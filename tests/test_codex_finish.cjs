'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { finishOutput } = require('../scripts/codex_finish.cjs');
const fs = require('node:fs');
const os = require('node:os');
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
  const project = path.resolve(__dirname, '..');
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'localeo-native-hook-'));
  const root = path.join(base, 'workspace with spaces', 'localeo-projet');
  try {
    fs.mkdirSync(path.join(root, 'scripts'), { recursive: true });
    fs.mkdirSync(path.join(root, 'docs'));
    for (const script of ['codex_context.cjs', 'codex_finish.cjs']) {
      fs.copyFileSync(path.join(project, 'scripts', script), path.join(root, 'scripts', script));
    }
    execFileSync('git', ['init', '-q', root], { windowsHide: true });
    const definition = JSON.parse(fs.readFileSync(path.join(project, '.codex/hooks.json'), 'utf8'));
    for (const [event, sources] of [['SessionStart', ['startup', 'resume', 'clear', 'compact', 'fork']], ['Stop', [undefined]]]) {
      for (const source of sources) {
        const groups = definition.hooks[event].filter(group => !group.matcher || new RegExp(group.matcher).test(source));
        assert.ok(groups.length, `No configured handler for ${event}/${source}`);
        for (const handler of groups.flatMap(group => group.hooks)) {
          const shells = process.platform === 'win32'
            ? [['powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', handler.commandWindows]], ['cmd.exe', ['/d', '/s', '/c', handler.commandWindows]]]
            : [['sh', ['-c', handler.command]]];
          for (const [shell, args] of shells) {
            const result = JSON.parse(execFileSync(shell, args, { cwd: path.join(root, 'docs'), input: JSON.stringify({ hook_event_name: event, source, cwd: root }), encoding: 'utf8', timeout: 15000, windowsHide: true, windowsVerbatimArguments: shell === 'cmd.exe' }));
            if (event === 'SessionStart') assert.equal(result.hookSpecificOutput.hookEventName, event);
            else assert.ok(result.systemMessage);
            assert.equal(result.decision, undefined);
            assert.equal(result.continue, undefined);
          }
        }
      }
    }
  } finally { fs.rmSync(base, { recursive: true, force: true }); }
});
