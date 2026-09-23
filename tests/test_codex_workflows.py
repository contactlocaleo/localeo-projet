import json
from pathlib import Path
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


if __name__ == '__main__':
    unittest.main()
