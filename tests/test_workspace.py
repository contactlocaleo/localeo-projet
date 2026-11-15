import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from scripts.check_workspace import inspect


class CurrentWorkspaceTests(unittest.TestCase):
    def test_current_roots_do_not_depend_on_historical_destinations(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            repos = []
            for index in range(5):
                path = parent / f'repo-{index}'
                subprocess.run(['git', 'init', '-q', str(path)], check=True)
                repos.append({'name': path.name, 'path': '../' + path.name})
            root = parent / 'repo-0'
            (root / 'repositories.json').write_text(json.dumps({'repositories': repos}))
            directory = root / 'docs/organisation'
            directory.mkdir(parents=True)
            (directory / 'migration-2026-09-18.json').write_text(json.dumps({'files': [{
                'target_repo': 'repo-0', 'target': 'retired.md', 'repo': 'repo-1',
                'path': 'old.md', 'action': 'move'}]}))
            self.assertEqual(inspect(root), [])
            self.assertIn('Destination absente: repo-0/retired.md', inspect(root, historical=True))
            repos[-1]['path'] = '../missing'
            (root / 'repositories.json').write_text(json.dumps({'repositories': repos}))
            self.assertTrue(inspect(root))
