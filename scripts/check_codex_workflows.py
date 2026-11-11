"""Validate local Codex discovery metadata and bounded automatic context, offline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tomllib


SESSION_SOURCES = ('startup', 'resume', 'clear', 'compact', 'fork')
READ_ONLY_REVIEWERS = {'localeo-invariant-reviewer', 'localeo-contract-reviewer', 'localeo-ux-reviewer'}
# Keep this scope aligned with scripts/git_pre_commit.cjs.
WORKFLOW_INPUTS = re.compile(
    r'(?:AGENTS\.md|\.agents/skills/.*|\.codex/agents/.*\.toml|\.codex/hooks\.json|'
    r'\.githooks/pre-commit|\.pre-commit-config\.yaml|'
    r'scripts/(?:check_codex_workflows\.py|git_pre_commit\.cjs|codex_(?:context|finish)\.cjs))'
)


class ConfigurationSource:
    """Read one consistent source: working files or Git's stage-zero index."""

    def __init__(self, root: Path, staged: bool):
        self.root = root.resolve()
        self.staged = staged
        if staged:
            top = self.git('rev-parse', '--show-toplevel').decode('utf-8').strip()
            if Path(top).resolve() != self.root:
                raise ValueError('--repo/--root doit designer la racine du depot Git')
            self.files = set(self.git('ls-files', '--cached', '-z').decode('utf-8').split('\0'))
        else:
            paths = [root / 'AGENTS.md', root / '.codex/hooks.json']
            paths.extend((root / '.agents/skills').glob('*/SKILL.md'))
            paths.extend((root / '.codex/agents').glob('*.toml'))
            self.files = {path.relative_to(root).as_posix() for path in paths if path.is_file()}

    def git(self, *args: str) -> bytes:
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, check=False)
        if result.returncode:
            raise ValueError('Index Git inaccessible ou fichier non resolu')
        return result.stdout

    def read(self, path: str) -> bytes:
        if path not in self.files:
            raise FileNotFoundError(path)
        return self.git('show', f':{path}') if self.staged else (self.root / path).read_bytes()

    def matching(self, pattern: str) -> list[str]:
        return sorted(path for path in self.files if re.fullmatch(pattern, path))


def has_workflow_changes(root: Path) -> bool:
    source = ConfigurationSource(root, staged=True)
    # Both sides of a rename matter: moving a configuration away is a deletion.
    paths = source.git('diff', '--cached', '--name-only', '--no-renames', '-z').decode('utf-8').split('\0')
    return any(WORKFLOW_INPUTS.fullmatch(path) for path in paths)


def validate(root: Path, *, staged: bool = False) -> list[str]:
    errors = []
    try:
        source = ConfigurationSource(root, staged)
    except (OSError, ValueError, UnicodeError) as error:
        return [str(error)]
    try:
        if len(source.read('AGENTS.md')) > 8_000:
            errors.append('AGENTS.md depasse le budget local de 8000 octets ; extraire les details')
    except (OSError, ValueError):
        errors.append('AGENTS.md absent ou illisible')
    names = set()
    files = source.matching(r'\.agents/skills/[^/]+/SKILL\.md')
    if not files:
        errors.append('Aucun skill local')
    for file in files:
        label = PurePosixPath(file).parent.name
        try:
            text = source.read(file).decode('utf-8-sig')
        except (OSError, ValueError, UnicodeError):
            errors.append(f'{label}: skill illisible')
            continue
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f'{label}: frontmatter absent')
            continue
        # The repository deliberately uses simple scalar discovery fields.
        entries = re.findall(r'^(name|description):[^\S\n]*(.*)$', parts[1], re.M)
        fields = dict(entries)
        if len(entries) != len(fields):
            errors.append(f'{label}: champ de decouverte duplique')
        name = fields.get('name', '').strip().strip('\"\'')
        description = fields.get('description', '').strip().strip('\"\'')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name != label:
            errors.append(f'{label}: nom de decouverte invalide')
        if name in names:
            errors.append(f'{label}: nom duplique')
        names.add(name)
        raw_description = fields.get('description', '').strip()
        non_scalar = raw_description.startswith(('[', '{', '|', '>', '&', '*', '!')) or raw_description.casefold() in ('null', '~', 'true', 'false') or raw_description.isnumeric()
        if not description or len(description) > 500 or non_scalar:
            errors.append(f'{label}: description scalaire requise, 500 caracteres maximum')
        if len(text.encode('utf-8')) > 14_000:
            errors.append(f'{label}: corps trop volumineux ; utiliser des references ciblees')
        if not parts[2].strip():
            errors.append(f'{label}: corps vide')
    for file in source.matching(r'\.codex/agents/[^/]+\.toml'):
        label = PurePosixPath(file).stem
        try:
            profile = tomllib.loads(source.read(file).decode('utf-8-sig'))
        except (OSError, ValueError, UnicodeError):
            errors.append(f'{label}: profil TOML absent ou invalide')
            continue
        if profile.get('name') != label or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', label):
            errors.append(f'{label}: nom du profil invalide')
        for field in ('description', 'developer_instructions'):
            if not isinstance(profile.get(field), str) or not profile[field].strip():
                errors.append(f'{label}: {field} doit etre une chaine non vide')
        if 'sandbox_mode' in profile and profile['sandbox_mode'] not in ('read-only', 'workspace-write', 'danger-full-access'):
            errors.append(f'{label}: sandbox_mode invalide')
        if label in READ_ONLY_REVIEWERS:
            if profile.get('sandbox_mode') != 'read-only':
                errors.append(f'{label}: le profil de revue local doit rester en lecture seule')
            if 'model' in profile or 'model_reasoning_effort' in profile:
                errors.append(f'{label}: le profil de revue local doit heriter du modele et de son effort')
    try:
        hooks = json.loads(source.read('.codex/hooks.json').decode('utf-8-sig'))['hooks']
        if not isinstance(hooks, dict) or not {'SessionStart', 'Stop'} <= hooks.keys():
            errors.append('SessionStart et Stop requis par la configuration locale')
        matched_sources = set()
        for event, groups in hooks.items():
            if not isinstance(groups, list) or not groups:
                errors.append(f'{event}: aucun groupe de hooks')
                continue
            for group in groups:
                if event == 'SessionStart':
                    matcher = group.get('matcher', '')
                    if not isinstance(matcher, str):
                        errors.append('SessionStart: matcher invalide')
                    else:
                        try:
                            pattern = re.compile(matcher)
                            matched_sources.update(value for value in SESSION_SOURCES if pattern.search(value))
                        except re.error:
                            errors.append('SessionStart: matcher invalide')
                if not isinstance(group.get('hooks'), list) or not group['hooks']:
                    errors.append(f'{event}: aucun gestionnaire de hooks')
                    continue
                for handler in group['hooks']:
                    if handler.get('type') != 'command' or not isinstance(handler.get('command'), str) or not handler['command'].strip():
                        errors.append(f'{event}: hook command attendu')
                    if 'commandWindows' in handler and (not isinstance(handler['commandWindows'], str) or not handler['commandWindows'].strip()):
                        errors.append(f'{event}: commandWindows doit etre une commande non vide')
                    timeout = handler.get('timeout', 0)
                    if type(timeout) not in (int, float) or not 0 < timeout <= 15:
                        errors.append(f'{event}: timeout requis, maximum local 15 secondes')
                    if event == 'SessionStart':
                        limit = handler.get('additionalContextLimit', 0)
                        if type(limit) not in (int, float) or not 0 < limit <= 1800:
                            errors.append('SessionStart: contexte automatique doit etre borne a 1800 tokens')
        if 'SessionStart' in hooks and matched_sources != set(SESSION_SOURCES):
            errors.append('SessionStart: sources non couvertes : ' + ', '.join(value for value in SESSION_SOURCES if value not in matched_sources))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, UnicodeError):
        errors.append('Definition des hooks absente ou invalide')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', '--repo', dest='root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--staged', action='store_true', help="Lire uniquement la configuration presente dans l'index Git")
    parser.add_argument('--changed', action='store_true', help="Avec --staged, controler seulement si un fichier de configuration concerne change")
    args = parser.parse_args()
    if args.changed and not args.staged:
        parser.error('--changed requiert --staged')
    if args.changed:
        try:
            if not has_workflow_changes(args.root):
                print("Configuration Codex : aucun fichier concerne dans l'index, controle non execute.")
                return 0
        except (OSError, ValueError, UnicodeError) as error:
            print(str(error))
            return 1
    errors = validate(args.root, staged=args.staged)
    for error in errors:
        print(error)
    print(f'Configuration Codex : {len(errors)} erreur(s). Activation native et qualite semantique non attestees.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
