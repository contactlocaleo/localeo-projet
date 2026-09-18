"""Controle hors reseau du workspace et des destinations de la migration."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote


def inspect(root):
    failures=[]
    registry=json.loads((root/'repositories.json').read_text(encoding='utf-8'))
    roots=[]
    for repo in registry['repositories']:
        path=(root/repo['path']).resolve()
        if not path.is_dir():
            failures.append('Depot absent: '+repo['name'])
            continue
        result=subprocess.run(['git','-C',str(path),'rev-parse','--show-toplevel'],capture_output=True,text=True)
        if result.returncode or Path(result.stdout.strip()).resolve()!=path:
            failures.append('Racine Git incorrecte: '+repo['name'])
        roots.append(path)
    if len(set(roots))!=5:
        failures.append('Cinq racines distinctes attendues')
    manifest=json.loads((root/'docs/organisation/migration-2026-09-18.json').read_text(encoding='utf-8'))
    for entry in manifest['files']:
        target=root.parent/entry['target_repo']/entry['target']
        if not target.is_file():
            failures.append('Destination absente: '+entry['target_repo']+'/'+entry['target'])
        if entry['action'] not in {'snapshot-runtime','contrat-genere-conserve','renvoi-local'}:
            old=root.parent/entry['repo']/entry['path']
            if old!=target and old.is_file() and entry['path']!='docs/README.md':
                failures.append('Copie originale restante: '+entry['repo']+'/'+entry['path'])
    for file in root.rglob('*.md'):
        if '.git' in file.parts or 'tmp' in file.relative_to(root).parts:
            continue
        content=file.read_text(encoding='utf-8')
        if re.search(r'\]\(@localeo-',content):
            failures.append('Marqueur de fusion non resolu: '+file.relative_to(root).as_posix())
    return failures


def links(root):
    """Inventaire des chemins manquants, sans confondre URLs/API et fichiers."""
    broken=[]
    for file in root.rglob('*.md'):
        if '.git' in file.parts or 'tmp' in file.relative_to(root).parts:
            continue
        fenced=False
        for number,line in enumerate(file.read_text(encoding='utf-8').splitlines(),1):
            if line.lstrip().startswith(('```','~~~')):
                fenced=not fenced
            if fenced:
                continue
            for value in re.findall(r'\]\((<[^>]+>|[^\s)]+)',line):
                value=value.strip('<>')
                if not value or value.startswith(('#','/')) or re.match(r'^[\w+.-]+:',value):
                    continue
                name=re.split('[?#]',value,1)[0]
                if not name or '${' in name or '<' in name:
                    continue
                if not (file.parent/unquote(name)).exists():
                    broken.append({'file':file.relative_to(root).as_posix(),'line':number,'target':value})
    return broken


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--links-report',type=Path,help='Rapport JSON des liens manquants (inclut la dette historique).')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    failures=inspect(root)
    if args.links_report:
        report=links(root)
        args.links_report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'{len(report)} references documentaires a examiner dans {args.links_report}')
    for failure in failures:
        print(failure)
    if failures:
        return 1
    print('5 depots Git distincts ; toutes les destinations presentes ; copies retirees et marqueurs controles.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
