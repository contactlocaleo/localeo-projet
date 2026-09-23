"""Validate local Codex discovery metadata and bounded automatic context, offline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


def validate(root: Path) -> list[str]:
    errors = []
    guide = root / 'AGENTS.md'
    if not guide.is_file():
        errors.append('AGENTS.md absent')
    elif guide.stat().st_size > 8_000:
        errors.append('AGENTS.md depasse le budget local de 8000 octets ; extraire les details')
    skills = root / '.agents/skills'
    names = set()
    files = sorted(skills.glob('*/SKILL.md'))
    if not files:
        errors.append('Aucun skill local')
    for file in files:
        text = file.read_text(encoding='utf-8-sig')
        parts = text.split('---', 2)
        label = file.parent.name
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
    try:
        hooks = json.loads((root / '.codex/hooks.json').read_text(encoding='utf-8-sig'))['hooks']
        if not isinstance(hooks, dict) or not {'SessionStart', 'Stop'} <= hooks.keys():
            errors.append('SessionStart et Stop requis par la configuration locale')
        for event, groups in hooks.items():
            if not isinstance(groups, list) or not groups:
                errors.append(f'{event}: aucun groupe de hooks')
                continue
            for group in groups:
                if not isinstance(group.get('hooks'), list) or not group['hooks']:
                    errors.append(f'{event}: aucun gestionnaire de hooks')
                    continue
                for handler in group['hooks']:
                    if handler.get('type') != 'command' or not handler.get('command'):
                        errors.append(f'{event}: hook command attendu')
                    timeout = handler.get('timeout', 0)
                    if not isinstance(timeout, (int, float)) or not 0 < timeout <= 15:
                        errors.append(f'{event}: timeout requis, maximum local 15 secondes')
                    if event == 'SessionStart' and not 0 < handler.get('additionalContextLimit', 0) <= 1800:
                        errors.append('SessionStart: contexte automatique doit etre borne a 1800 tokens')
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        errors.append('Definition des hooks absente ou invalide')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    for error in errors:
        print(error)
    print(f'Configuration Codex : {len(errors)} erreur(s). Activation native et qualite semantique non attestees.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
