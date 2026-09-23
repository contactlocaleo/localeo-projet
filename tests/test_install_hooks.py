from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.install_hooks import git, install


class HookInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.githooks').mkdir()
        (self.root / '.githooks/pre-commit').write_text('#!/bin/sh\nexit 0\n')
        subprocess.run(['git', '-C', str(self.root), 'config', '--local', 'core.hooksPath', str(self.root / 'previous')], check=True)

    def test_installs_idempotently_in_local_config_for_missing_previous_path(self):
        first = install(self.root, sys.executable)
        self.assertEqual(install(self.root, sys.executable), first)
        self.assertEqual(git(self.root, 'config', '--local', '--get', 'core.hooksPath'), first)
        self.assertEqual(git(self.root, 'config', '--local', '--get', 'localeo.python'), sys.executable)

    def test_preserves_existing_hook_and_configuration(self):
        (self.root / 'previous').mkdir()
        hook = self.root / 'previous/pre-commit'
        hook.write_text('custom-hook')
        with self.assertRaisesRegex(ValueError, 'Hooks existants'):
            install(self.root, sys.executable)
        self.assertEqual(hook.read_text(), 'custom-hook')
        self.assertEqual(git(self.root, 'config', '--local', '--get', 'core.hooksPath'), str(self.root / 'previous'))
        self.assertEqual(git(self.root, 'config', '--local', '--get', 'localeo.python'), '')

    def test_invalid_python_does_not_change_configuration(self):
        with self.assertRaisesRegex(ValueError, 'Python'):
            install(self.root, str(self.root / 'missing-python'))
        self.assertEqual(git(self.root, 'config', '--local', '--get', 'core.hooksPath'), str(self.root / 'previous'))

    def test_git_actually_executes_installed_hook_and_preserves_its_refusal(self):
        (self.root / '.githooks/pre-commit').write_text('#!/bin/sh\nprintf ran > hook-ran.txt\nexit 1\n', encoding='utf-8')
        install(self.root, sys.executable)
        for key, value in [('user.name', 'Hook test'), ('user.email', 'hook@example.invalid'), ('commit.gpgsign', 'false')]:
            subprocess.run(['git', '-C', str(self.root), 'config', '--local', key, value], check=True)
        result = subprocess.run(['git', '-C', str(self.root), 'commit', '--allow-empty', '-m', 'Fixture only'], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.root / 'hook-ran.txt').read_text(), 'ran')


if __name__ == '__main__':
    unittest.main()
