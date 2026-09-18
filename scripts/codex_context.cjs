'use strict';
// SessionStart: only repository presence/status, never file contents or secrets.
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const REPOS = ['localeo-projet', 'localeo-backend', 'localeo-animation', 'localeo-commercant', 'localeo-marketplace'];
function inspectWorkspace(root, runGit = (repo) => execFileSync('git', ['-C', repo, 'status', '--porcelain', '--untracked-files=normal'], { encoding: 'utf8', timeout: 1200, windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'], env: { ...process.env, GIT_OPTIONAL_LOCKS: '0' } })) {
  return REPOS.map((name) => {
    const repo = name === 'localeo-projet' ? root : path.join(path.dirname(root), name);
    if (!fs.existsSync(path.join(repo, '.git'))) return { name, state: 'absent' };
    try { return { name, state: runGit(repo).trim() ? 'modifie' : 'propre' }; }
    catch { return { name, state: 'non-verifie' }; }
  });
}
function hookOutput(states) {
  const names = (state) => states.filter((repo) => repo.state === state).map((repo) => repo.name).join(', ') || 'aucun';
  return { hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: [
    'Workspace Localeo : cinq depots Git independants. Lire AGENTS.md puis seulement les guides utiles au perimetre ; les guides voisins ne sont pas herites.',
    `Depots absents : ${names('absent')}. Travaux locaux presents : ${names('modifie')}. Statut non verifie : ${names('non-verifie')}.`,
    'Preserver les travaux locaux ; commit, push et deploiement suivent la demande en cours. La roadmap commune porte les etats ; le domaine backend porte les invariants.',
    'Routage et preuves : localeo-projet/docs/organisation/codex.md. Les profils de revue et skills de ce depot sont disponibles selon leur decouverte par le client.'
  ].join('\n') } };
}
if (require.main === module) {
  process.stdout.write(JSON.stringify(hookOutput(inspectWorkspace(path.resolve(__dirname, '..')))) + '\n');
}
module.exports = { inspectWorkspace, hookOutput };
