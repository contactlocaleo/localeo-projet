"""Install this repository's Git hook without changing global or existing hooks."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import stat
import subprocess
import sys


def git(root: Path, *args: str) -> str:
    result = subprocess.run(['git', '-C', str(root), *args], text=True, capture_output=True, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError('Git inaccessible pour la configuration des hooks')
    return result.stdout.strip()


def install(root: Path, python: str) -> str:
    root = root.resolve()
    target = root / '.githooks'
    if not (target / 'pre-commit').is_file():
        raise ValueError('Hook versionne manquant')
    previous = git(root, 'config', '--get', 'core.hooksPath')
    old = Path(previous).expanduser() if previous else root / git(root, 'rev-parse', '--git-path', 'hooks')
    if not old.is_absolute():
        old = root / old
    if old.resolve() != target.resolve() and old.exists():
        active = [p for p in old.iterdir() if p.is_file() and not p.name.endswith('.sample')]
        if active:
            raise ValueError('Hooks existants conserves ; integrer le controle Localeo au gestionnaire existant avant activation')
    if not Path(python).is_file():
        raise ValueError('Executable Python introuvable')
    if os.name != 'nt':
        hook = target / 'pre-commit'
        hook.chmod(hook.stat().st_mode | stat.S_IXUSR)
    # All preconditions are checked before either local setting is changed.
    subprocess.run(['git', '-C', str(root), 'config', '--local', 'localeo.python', python], check=True)
    subprocess.run(['git', '-C', str(root), 'config', '--local', 'core.hooksPath', str(target)], check=True)
    return str(target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true', help='Activer le hook Git uniquement dans ce depot')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        if args.install:
            print('Hook Git actif : ' + install(root, sys.executable))
        else:
            print('core.hooksPath : ' + (git(root, 'config', '--get', 'core.hooksPath') or '(Git par defaut)'))
            print('Python configure : ' + (git(root, 'config', '--local', '--get', 'localeo.python') or '(absent)'))
        return 0
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
