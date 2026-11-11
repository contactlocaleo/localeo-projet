import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_codex_workflows import validate


class WorkflowValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'AGENTS.md').write_text('Useful small guidance', encoding='utf-8')
        self.skill = self.root / '.agents/skills/example/SKILL.md'
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text('---\nname: example\ndescription: A focused task\n---\nWorkflow.', encoding='utf-8')
        (self.root / '.codex').mkdir()
        self.hooks = self.root / '.codex/hooks.json'
        self.hooks.write_text(json.dumps({'hooks': {'Stop': [{'hooks': [{'type': 'command', 'command': 'node stop.cjs', 'timeout': 10}]}], 'SessionStart': [{'hooks': [
            {'type': 'command', 'command': 'node hook.cjs', 'timeout': 10, 'additionalContextLimit': 1800}
        ]}]}}))
        self.profile = self.root / '.codex/agents/localeo-ux-reviewer.toml'
        self.profile.parent.mkdir()
        self.profile.write_text('name = "localeo-ux-reviewer"\ndescription = "Review the interface"\nsandbox_mode = "read-only"\ndeveloper_instructions = "Read the assigned files and report evidence."\n', encoding='utf-8')

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def stage(self):
        self.git('init', '-q')
        self.git('add', '--all')

    def commit_fixture(self):
        self.stage()
        for key, value in [('user.name', 'Workflow CLI test'), ('user.email', 'workflow-cli@example.invalid'), ('commit.gpgsign', 'false'), ('core.hooksPath', str(self.root / 'no-hooks'))]:
            self.git('config', '--local', key, value)
        self.git('commit', '-qm', 'Fixture baseline')

    def cli(self, *args):
        command = [sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/check_codex_workflows.py'), '--repo', str(self.root), *args]
        return subprocess.run(command, capture_output=True, text=True)

    def test_accepts_discoverable_bounded_configuration(self):
        self.assertEqual(validate(self.root), [])

    def test_rejects_empty_hooks_and_non_scalar_metadata(self):
        self.hooks.write_text('{"hooks": {}}')
        self.skill.write_text('---\nname: example\ndescription: [not, a, string]\n---\nWorkflow.')
        self.assertEqual(len(validate(self.root)), 2)

    def test_rejects_duplicate_discovery_fields_and_empty_handler_group(self):
        self.skill.write_text('---\nname: example\nname: example\ndescription: task\n---\nWorkflow.')
        data = json.loads(self.hooks.read_text())
        data['hooks']['Stop'][0]['hooks'] = []
        self.hooks.write_text(json.dumps(data))
        self.assertEqual(len(validate(self.root)), 2)

    def test_rejects_missing_name_and_unbounded_context(self):
        self.skill.write_text('---\ndescription: task\n---\nWorkflow.')
        data = json.loads(self.hooks.read_text())
        data['hooks']['SessionStart'][0]['hooks'][0]['additionalContextLimit'] = 0
        self.hooks.write_text(json.dumps(data))
        errors = validate(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any('nom' in error for error in errors))
        self.assertTrue(any('contexte' in error for error in errors))

    def test_rejects_oversized_automatic_guide_and_malformed_hooks(self):
        (self.root / 'AGENTS.md').write_text('x' * 8001)
        self.hooks.write_text('{')
        self.assertEqual(len(validate(self.root)), 2)

    def test_rejects_missing_session_source_and_invalid_matcher(self):
        for matcher in ('^(startup|resume|clear|compact)$', '[', 123):
            with self.subTest(matcher=matcher):
                data = json.loads(self.hooks.read_text())
                data['hooks']['SessionStart'][0]['matcher'] = matcher
                self.hooks.write_text(json.dumps(data))
                self.assertTrue(any('SessionStart' in error for error in validate(self.root)))

    def test_accepts_arbitrary_profile_count_and_a_worker_with_write_access(self):
        for name in ('one-reviewer', 'two-reviewer', 'three-reviewer', 'example-worker'):
            (self.profile.parent / f'{name}.toml').write_text(f'name = "{name}"\ndescription = "Scoped task"\ndeveloper_instructions = "Handle the assigned files."\nsandbox_mode = "workspace-write"\n')
        self.assertEqual(validate(self.root), [])

    def test_rejects_malformed_and_incomplete_profiles(self):
        for content in ('[', 'name = "other"', 'name = "localeo-ux-reviewer"\ndescription = 42\ndeveloper_instructions = " "'):
            with self.subTest(content=content):
                self.profile.write_text(content)
                self.assertTrue(any('localeo-ux-reviewer' in error for error in validate(self.root)))

    def test_local_reviewers_keep_read_only_and_inherited_model(self):
        original = self.profile.read_text()
        for content in (original.replace('read-only', 'workspace-write'), original + 'model = "override"\n', original + 'model_reasoning_effort = "high"\n'):
            with self.subTest(content=content):
                self.profile.write_text(content)
                self.assertEqual(len(validate(self.root)), 1)

    def test_malformed_hook_shapes_and_boolean_limits_fail_without_crashing(self):
        original = self.hooks.read_text()
        for value in (None, [], {'SessionStart': [None]}, {'SessionStart': [{'hooks': [None]}]}):
            with self.subTest(value=value):
                self.hooks.write_text(json.dumps({'hooks': value}))
                self.assertTrue(validate(self.root))
        for field in ('timeout', 'additionalContextLimit'):
            with self.subTest(field=field):
                data = json.loads(original)
                data['hooks']['SessionStart'][0]['hooks'][0][field] = True
                self.hooks.write_text(json.dumps(data))
                self.assertTrue(validate(self.root))

    def test_staged_valid_configuration_ignores_invalid_working_files(self):
        self.stage()
        self.skill.write_text('broken frontmatter')
        self.hooks.write_text('{"hooks": {}}')
        self.profile.write_text('invalid = [')
        (self.root / 'AGENTS.md').write_text('x' * 8001)
        self.assertEqual(validate(self.root, staged=True), [])
        self.assertTrue(validate(self.root))

    def test_staged_invalid_configuration_is_not_repaired_by_working_files(self):
        paths = (self.skill, self.hooks, self.profile, self.root / 'AGENTS.md')
        originals = [path.read_bytes() for path in paths]
        self.skill.write_text('broken frontmatter')
        self.hooks.write_text('{"hooks": {}}')
        self.profile.write_text('invalid = [')
        (self.root / 'AGENTS.md').write_text('x' * 8001)
        self.stage()
        for path, content in zip(paths, originals):
            path.write_bytes(content)
        self.assertEqual(validate(self.root), [])
        self.assertEqual(len(validate(self.root, staged=True)), 4)

    def test_staged_deletions_use_index_even_when_files_remain_on_disk(self):
        self.stage()
        self.git('rm', '--cached', 'AGENTS.md', '.codex/hooks.json', '.agents/skills/example/SKILL.md')
        self.assertEqual(validate(self.root), [])
        errors = validate(self.root, staged=True)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any('Aucun skill' in error for error in errors))

    def test_untracked_configuration_is_not_in_staged_snapshot(self):
        self.stage()
        untracked = self.root / '.agents/skills/untracked/SKILL.md'
        untracked.parent.mkdir()
        untracked.write_text('invalid')
        self.assertEqual(validate(self.root, staged=True), [])
        self.assertTrue(validate(self.root))

    def test_cli_accepts_repo_alias_and_reports_index_failures(self):
        self.stage()
        command = [sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/check_codex_workflows.py'), '--repo', str(self.root), '--staged']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        command[-2] = str(self.root / 'missing')
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Index Git', result.stdout)

    def test_cli_changed_skips_document_only_change_despite_old_invalid_configuration(self):
        self.hooks.write_text('{"hooks": {}}')
        self.commit_fixture()
        (self.root / 'notes.md').write_text('An unrelated documentation change.\n')
        self.git('add', 'notes.md')
        result = self.cli('--staged', '--changed')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('controle non execute', result.stdout)
        self.assertNotIn('0 erreur', result.stdout)

    def test_cli_changed_rejects_indexed_invalid_configuration_despite_working_repair(self):
        self.commit_fixture()
        original = self.hooks.read_text()
        self.hooks.write_text('{"hooks": {}}')
        self.git('add', '.codex/hooks.json')
        self.hooks.write_text(original)
        result = self.cli('--staged', '--changed')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('SessionStart et Stop requis', result.stdout)

    def test_cli_changed_detects_deleted_hooks_even_when_working_file_remains(self):
        self.commit_fixture()
        self.git('rm', '--cached', '.codex/hooks.json')
        self.assertTrue(self.hooks.is_file())
        result = self.cli('--staged', '--changed')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('Definition des hooks absente ou invalide', result.stdout)

    def test_cli_changed_detects_renamed_configuration(self):
        self.commit_fixture()
        self.git('mv', '.codex/hooks.json', 'former-hooks.json')
        result = self.cli('--staged', '--changed')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('Definition des hooks absente ou invalide', result.stdout)

    def test_cli_changed_includes_pre_commit_manager_configuration(self):
        self.hooks.write_text('{"hooks": {}}')
        self.commit_fixture()
        (self.root / '.pre-commit-config.yaml').write_text('repos: []\n')
        self.git('add', '.pre-commit-config.yaml')
        result = self.cli('--staged', '--changed')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('SessionStart et Stop requis', result.stdout)

    def test_cli_changed_requires_staged(self):
        result = self.cli('--changed')
        self.assertEqual(result.returncode, 2)
        self.assertIn('--changed requiert --staged', result.stderr)


if __name__ == '__main__':
    unittest.main()
