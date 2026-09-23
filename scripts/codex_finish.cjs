'use strict';
// Advisory only: a Stop hook must not infer test success from an assistant message.
const path = require('node:path');
const { inspectWorkspace } = require('./codex_context.cjs');

function finishOutput(states) {
  if (states.every(repo => repo.state === 'propre')) return {};
  return { systemMessage: 'Localeo : des depots sont modifies, absents ou non verifies. Le compte rendu doit distinguer controles reussis, echecs et non executes, et signaler les impacts documentation/generateur/livraison. Un arbre propre ou ce rappel ne prouve aucune validation. Guide : docs/organisation/utiliser-workflows-codex.md.' };
}

function run() {
  process.stdout.write(JSON.stringify(finishOutput(inspectWorkspace(path.resolve(__dirname, '..')))) + '\n');
}
if (require.main === module) run();
module.exports = { finishOutput, run };
