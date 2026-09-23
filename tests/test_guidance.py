"""Regression coverage for guidance parsing and real Git index semantics."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_guidance.py"
SPEC = importlib.util.spec_from_file_location("check_guidance", SCRIPT)
guidance = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = guidance
SPEC.loader.exec_module(guidance)


class MarkdownTests(unittest.TestCase):
    def test_examples_are_ignored_but_code_in_label_preserves_link(self):
        text = '''```markdown
[example](missing.md)
```
~~~
[example](also-missing.md)
~~~
`[inline](missing.md)` and ``[other](missing.md)``
<!-- [hidden](missing.md) -->
[the `README` guide](README.md)
'''
        self.assertEqual([(link.line, link.destination) for link in guidance.markdown_links(text)], [(9, "README.md")])

    def test_inline_spaces_escapes_balanced_parentheses_and_title(self):
        links = guidance.markdown_links('[space](<folder/my guide.md> "title") [escaped](file\\(old\\).md) [nested](file(new).md)')
        self.assertEqual([link.destination for link in links], ["folder/my guide.md", r"file\(old\).md", "file(new).md"])

    def test_reference_styles_case_and_multiline_definition(self):
        text = '[first][DOC] [Doc][] [doc]\n\n[doc]:\n  <my guide.md> "Guide"\n'
        self.assertEqual([link.destination for link in guidance.markdown_links(text)], ["my guide.md"] * 3)
        undefined = guidance.markdown_links('[link][unknown] ordinary [words]')
        self.assertEqual(len(undefined), 1)
        self.assertEqual(undefined[0].reference, "unknown")
        self.assertIsNone(undefined[0].destination)

    def test_external_api_and_fragment_destinations_are_not_files(self):
        source = Path.cwd() / "README.md"
        for destination in ("https://example.org/file.md", "mailto:someone@example.org", "/api/orders", "//example.org", "#section", "app://connector"):
            with self.subTest(destination=destination):
                self.assertIsNone(guidance.local_target(source, destination))
        self.assertEqual(guidance.local_target(source, "my%20guide.md?download=1#intro"), source.parent / "my guide.md")

    def test_unclosed_prose_bracket_does_not_hide_a_later_link(self):
        links = guidance.markdown_links("An unfinished [note\n\n[actual guide](guide.md)")
        self.assertEqual([link.destination for link in links], ["guide.md"])


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.new_repo("localeo-projet")

    def git(self, *args, repo=None):
        result = subprocess.run(["git", "-C", str(repo or self.repo), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def new_repo(self, name):
        repo = self.base / name
        repo.mkdir()
        self.git("init", "--quiet", repo=repo)
        self.git("config", "user.email", "guidance-test@example.invalid", repo=repo)
        self.git("config", "user.name", "Guidance tests", repo=repo)
        self.git("config", "commit.gpgsign", "false", repo=repo)
        self.git("config", "core.hooksPath", str(repo / ".git" / "no-test-hooks"), repo=repo)
        return repo

    def write(self, name, content="present\n", repo=None):
        target = (repo or self.repo) / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "--quiet", "-m", "Fixture")

    def check(self, **options):
        return guidance.check_guidance(self.repo, [self.repo], **options)

    def test_changed_functional_document_is_checked_without_loading_historical_debt(self):
        self.write('docs/old-spec.md', '[old](already-missing.md)')
        self.commit()
        self.write('docs/new-feature.md', '[broken](absent.md)')
        self.git('add', 'docs/new-feature.md')
        result = self.check(staged=True, changed=True, all_markdown=True)
        self.assertEqual(result['checked_guides'], 1)
        self.assertEqual(len(result['errors']), 1)
        self.assertEqual(result['errors'][0]['destination'], 'absent.md')

    def test_deleted_target_rechecks_unchanged_functional_document(self):
        self.write('docs/ops.md', '[procedure](procedure.md)')
        self.write('docs/procedure.md')
        self.commit()
        self.git('rm', 'docs/procedure.md')
        result = self.check(staged=True, changed=True, all_markdown=True)
        self.assertEqual(len(result['errors']), 1)
        self.assertEqual(result['errors'][0]['destination'], 'procedure.md')

    def test_staged_functional_document_is_not_repaired_by_unstaged_edit(self):
        self.write('docs/feature.md', '[broken](missing.md)')
        self.git('add', 'docs/feature.md')
        self.write('docs/feature.md', 'Working tree repaired but not staged')
        self.assertEqual(len(self.check(staged=True, changed=True, all_markdown=True)['errors']), 1)

    def test_tracked_and_untracked_guidance_exclude_ignored_and_outputs(self):
        self.write("README.md", "[target](target.md)\n")
        self.write("target.md")
        self.write(".gitignore", "ignored/\n")
        self.commit()
        self.write(".agents/skills/example/SKILL.md", "[missing](missing.md)\n")
        self.write("ignored/README.md", "[missing](missing.md)\n")
        self.write("output/README.md", "[missing](missing.md)\n")
        self.write("node_modules/package/README.md", "[missing](missing.md)\n")
        report = self.check()
        self.assertEqual(report["checked_guides"], 2)
        self.assertEqual(len(report["errors"]), 1)
        self.assertTrue(report["errors"][0]["source"].endswith("SKILL.md"))

    def test_files_directories_encoded_spaces_and_reference_links(self):
        self.write("README.md", '[space](<docs/my guide.md>) [encoded](docs/my%20guide.md#section) [dir](docs) [ref][]\n\n[ref]: docs/my%20guide.md\n')
        self.write("docs/my guide.md")
        report = self.check()
        self.assertEqual(report["checked_links"], 4)
        self.assertEqual(report["errors"], [])

    def test_staged_reads_index_guide_and_accepts_staged_target_missing_on_disk(self):
        self.write("README.md", "[target](target.md)\n")
        target = self.write("target.md")
        self.git("add", "--all")
        self.write("README.md", "[uncommitted](missing.md)\n")
        target.unlink()
        self.write("AGENTS.md", "[untracked](missing.md)\n")
        report = self.check(staged=True)
        self.assertEqual(report["checked_guides"], 1)
        self.assertEqual(report["errors"], [])

    def test_staged_deletion_is_detected_even_when_target_still_exists_on_disk(self):
        self.write("README.md", "[target](target.md)\n")
        self.write("target.md")
        self.commit()
        self.git("rm", "--cached", "target.md")
        self.assertTrue((self.repo / "target.md").exists())
        for changed in (False, True):
            with self.subTest(changed=changed):
                report = self.check(staged=True, changed=changed)
                self.assertEqual(report["checked_guides"], 1)
                self.assertEqual([issue["reason"] for issue in report["errors"]], ["missing_target"])

    def test_changed_includes_unchanged_guide_linking_to_deleted_directory(self):
        self.write("README.md", "[directory](docs)\n")
        self.write("AGENT.md", "[pre-existing](already-missing.md)\n")
        target = self.write("docs/only-file.md")
        self.commit()
        target.unlink()
        target.parent.rmdir()
        report = self.check(changed=True)
        self.assertEqual(report["checked_guides"], 1)
        self.assertEqual([issue["destination"] for issue in report["errors"]], ["docs"])

    def test_changed_selects_untracked_guides_and_index_changes_on_unborn_branch(self):
        self.write("README.md", "[broken](missing.md)\n")
        self.git("add", "README.md")
        self.write("AGENTS.md", "[also broken](missing.md)\n")
        self.assertEqual(self.check(changed=True)["checked_guides"], 2)
        self.assertEqual(self.check(changed=True, staged=True)["checked_guides"], 1)

    def test_staged_neighbour_uses_disk_and_same_repository_directory_uses_index(self):
        neighbour = self.new_repo("localeo-backend")
        self.write("notes.md", repo=neighbour)
        self.write("README.md", "[neighbour](../localeo-backend/notes.md) [directory](docs)\n")
        target = self.write("docs/notes.md")
        self.git("add", "--all")
        target.unlink()
        target.parent.rmdir()
        self.assertEqual(self.check(staged=True)["errors"], [])

    def test_explicit_document_is_checked_and_missing_neighbours_are_warnings(self):
        self.write("docs/codex.md", "[broken](missing.md)\n")
        report = guidance.check_guidance(self.repo, documents=[Path("docs/codex.md")])
        self.assertEqual(report["checked_guides"], 1)
        self.assertEqual(len(report["warnings"]), 4)
        self.assertEqual(report["errors"][0]["reason"], "missing_target")

    def test_cli_reports_json_and_returns_nonzero_for_broken_links(self):
        self.write("README.md", "[broken](missing.md)\n")
        report_file = self.base / "report.json"
        with contextlib.redirect_stdout(io.StringIO()):
            code = guidance.main(["--root", str(self.repo), "--repo", str(self.repo), "--report", str(report_file)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(report_file.read_text(encoding="utf-8"))["errors"][0]["reason"], "missing_target")


if __name__ == "__main__":
    unittest.main()
