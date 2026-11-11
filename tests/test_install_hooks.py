import json
from pathlib import Path
import shutil
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


class WorkflowPreCommitTests(unittest.TestCase):
    """Exercise the installed hook through real commits in disposable repositories."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repository with spaces'
        self.root.mkdir()
        self.git('init', '-q')
        for key, value in [('user.name', 'Workflow test'), ('user.email', 'workflow@example.invalid'), ('commit.gpgsign', 'false'), ('core.hooksPath', str(self.root / 'no-hooks'))]:
            self.git('config', '--local', key, value)
        project = Path(__file__).resolve().parents[1]
        for name in ('.githooks/pre-commit', 'scripts/git_pre_commit.cjs', 'scripts/check_guidance.py', 'scripts/check_codex_workflows.py'):
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(project / name, destination)
        self.write('AGENTS.md', 'Read the relevant guidance.')
        self.valid_skill = '---\nname: example\ndescription: Handle a focused task\n---\nFollow the assigned task.\n'
        self.skill = self.write('.agents/skills/example/SKILL.md', self.valid_skill)
        self.hooks = self.write('.codex/hooks.json', json.dumps({'hooks': {
            'SessionStart': [{'matcher': '^(startup|resume|clear|compact|fork)$', 'hooks': [{'type': 'command', 'command': 'node context.cjs', 'timeout': 10, 'additionalContextLimit': 1800}]}],
            'Stop': [{'hooks': [{'type': 'command', 'command': 'node finish.cjs', 'timeout': 10}]}],
        }}))
        self.profile = self.write('.codex/agents/example-reviewer.toml', 'name = "example-reviewer"\ndescription = "Review a scoped change"\ndeveloper_instructions = "Read the delegated files."\nsandbox_mode = "read-only"\n')
        self.git('add', '--all')
        self.git('commit', '-qm', 'Fixture baseline')
        install(self.root, sys.executable)

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
        return target

    def commit(self):
        return subprocess.run(['git', '-C', str(self.root), 'commit', '-qm', 'Fixture change'], capture_output=True, text=True, encoding='utf-8')

    def assert_refused_without_changes(self, expected):
        index = self.git('ls-files', '--stage')
        head = self.git('rev-parse', 'HEAD')
        result = self.commit()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(expected, result.stdout + result.stderr)
        self.assertEqual(self.git('ls-files', '--stage'), index)
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)

    def test_valid_staged_skill_commits_while_unstaged_invalid_edit_is_preserved(self):
        staged = self.valid_skill + '\nA valid clarification.\n'
        self.skill.write_text(staged, encoding='utf-8')
        self.git('add', '.agents/skills/example/SKILL.md')
        self.skill.write_text('invalid unstaged edit', encoding='utf-8')
        index = self.git('ls-files', '--stage')
        result = self.commit()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Configuration Codex : 0 erreur', result.stdout + result.stderr)
        self.assertEqual(self.git('ls-files', '--stage'), index)
        self.assertEqual(self.git('show', 'HEAD:.agents/skills/example/SKILL.md'), staged)
        self.assertEqual(self.skill.read_text(), 'invalid unstaged edit')

    def test_invalid_staged_skill_refuses_despite_unstaged_repair(self):
        self.skill.write_text('invalid indexed frontmatter', encoding='utf-8')
        self.git('add', '.agents/skills/example/SKILL.md')
        self.skill.write_text(self.valid_skill, encoding='utf-8')
        self.assert_refused_without_changes('frontmatter absent')
        self.assertEqual(self.skill.read_text(), self.valid_skill)

    def test_empty_hooks_refuse_even_with_valid_working_definition(self):
        original = self.hooks.read_text()
        self.hooks.write_text('{"hooks": {}}', encoding='utf-8')
        self.git('add', '.codex/hooks.json')
        self.hooks.write_text(original, encoding='utf-8')
        self.assert_refused_without_changes('SessionStart et Stop requis')
        self.assertEqual(self.hooks.read_text(), original)

    def test_invalid_indexed_profile_refuses(self):
        self.profile.write_text('name = "example-reviewer"\ndescription = ""\ndeveloper_instructions = ""\n', encoding='utf-8')
        self.git('add', '.codex/agents/example-reviewer.toml')
        self.assert_refused_without_changes('description doit etre une chaine non vide')

    def test_deleted_hooks_refuse_even_if_definition_remains_on_disk(self):
        self.git('rm', '--cached', '.codex/hooks.json')
        self.assertTrue(self.hooks.is_file())
        self.assert_refused_without_changes('Definition des hooks absente ou invalide')

    def test_rename_away_from_configuration_path_triggers_validation(self):
        self.git('mv', '.codex/hooks.json', 'former-hooks.json')
        self.assert_refused_without_changes('Definition des hooks absente ou invalide')

    def test_unrelated_document_commit_does_not_run_additional_checker(self):
        self.write('scripts/check_codex_workflows.py', 'raise SystemExit("Unexpected workflow checker execution")\n')
        self.write('docs/change.md', 'A documentation-only change.\n')
        self.git('add', 'docs/change.md')
        result = self.commit()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('Configuration Codex', result.stdout + result.stderr)

    def test_pre_commit_manager_configuration_triggers_workflow_validation(self):
        self.write('.pre-commit-config.yaml', 'repos: []\n')
        self.git('add', '.pre-commit-config.yaml')
        result = self.commit()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Configuration Codex : 0 erreur', result.stdout + result.stderr)

    def test_unrelated_document_still_fails_on_a_broken_link(self):
        self.write('docs/change.md', '[missing](absent.md)\n')
        self.git('add', 'docs/change.md')
        self.assert_refused_without_changes('absent.md')


if __name__ == '__main__':
    unittest.main()
