"""Behavioral tests for immutable, offline release source inspection."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import render_release_sources as sources


LEGACY = "a" * 64
RUNNER = f'''BASELINE_VERSION = 147
EMPTY_BASELINE_NAME = "baseline_v147.sql"
DANGEROUS_MIGRATIONS = {{"v148_purge_commune_test.sql", "v149_seed_commune_test.sql"}}
LEGACY_MIGRATION_CHECKSUMS = {{"v252_support_financier.sql": {{"{LEGACY}"}}}}
raise RuntimeError("THIS MUST NEVER EXECUTE")
'''.encode()


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.git("config", "core.autocrlf", "false")

    def git(self, *args, input=None):
        return subprocess.run(["git", "-C", str(self.root), *args], input=input,
                              check=True, capture_output=True, timeout=15).stdout

    def put(self, path, content):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(content)

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-qm", "Fixture")
        return self.git("rev-parse", "HEAD").decode().strip()

    def source(self):
        return sources.GitSource(self.root, self.commit())

    def migration_source(self):
        self.put(sources.RUNNER_PATH, RUNNER)
        self.put("sql/baseline_v147.sql", b"SELECT 147;\n")
        self.put("sql/v147_production_schema_catchup.sql", b"SELECT 147;\n")
        self.put("sql/v148_purge_commune_test.sql", b"DELETE FROM fixture;\n")
        self.put("sql/v149_seed_commune_test.sql", b"INSERT INTO fixture VALUES (1);\n")
        self.put("sql/v150_first.sql", b"SELECT 150;\n")
        self.put("sql/v252_support_financier.sql", b"SELECT 252;\n")
        self.put("sql/v300_last.sql", b"SELECT 300;\n")
        return self.source()

    def reviewed(self):
        return patch.object(sources, "REVIEWED_RUNNER_SHA256", {hashlib.sha256(RUNNER).hexdigest()})

    def row(self, source, filename, checksum=None):
        return {"filename": filename, "checksum_sha256": checksum or
                hashlib.sha256(source.read("sql/" + filename)).hexdigest()}

    def test_exact_commit_ignores_changed_and_untracked_worktree(self):
        self.put(".env.example", b"PUBLIC_KEY=old\n")
        source = self.source()
        self.put(".env.example", b"NEW_KEY=changed\n")
        self.put("deploy/new.env.example", b"UNTRACKED_KEY=value\n")
        self.assertEqual(source.read(".env.example"), b"PUBLIC_KEY=old\n")
        self.assertEqual(source.paths(), [".env.example"])
        self.assertEqual([k["name"] for k in sources.config_catalog(source, "backend")["keys"]], ["PUBLIC_KEY"])

    def test_git_invocation_disables_transports_and_injected_configuration(self):
        self.put("one.txt", b"1")
        sha = self.commit()
        real_run = subprocess.run
        with patch.dict("os.environ", {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "alias.evil"}), \
                patch.object(sources.subprocess, "run", wraps=real_run) as run:
            source = sources.GitSource(self.root, sha)
            source.read("one.txt")
        for call in run.call_args_list:
            self.assertFalse(call.kwargs["shell"])
            self.assertEqual(call.kwargs["env"]["GIT_ALLOW_PROTOCOL"], "")
            self.assertNotIn("GIT_CONFIG_COUNT", call.kwargs["env"])
            self.assertIn("--no-replace-objects", call.args[0])

    def test_sha_and_repository_root_are_strict(self):
        self.put("one.txt", b"1")
        source = self.source()
        for sha in ("HEAD", source.sha[:8], source.sha + ":one.txt", "-h"):
            with self.subTest(sha=sha), self.assertRaises(ValueError):
                sources.GitSource(self.root, sha)
        child = self.root / "child"
        child.mkdir()
        with self.assertRaises(ValueError):
            sources.GitSource(child, source.sha)
        blob = self.git("rev-parse", source.sha + ":one.txt").decode().strip()
        with self.assertRaises(ValueError):
            sources.GitSource(self.root, blob)

    def test_private_env_never_read_and_values_never_returned(self):
        self.put(".env.example", b"# public template\nexport TOKEN=public-placeholder-not-output\n")
        self.put("deploy/test.env.example", b"VITE_API_URL=https://private-value.invalid\nTOKEN=another-value\n")
        self.put(".env", b"PASSWORD=secret-not-read\n")
        self.put(".env.demo", b"PASSWORD=another-secret\n")
        source = self.source()
        original = source.read
        calls = []
        def read(path):
            calls.append(path)
            return original(path)
        with patch.object(source, "read", side_effect=read):
            result = sources.config_catalog(source, "marketplace")
        self.assertEqual(calls, [".env.example", "deploy/test.env.example"])
        self.assertEqual([row["name"] for row in result["keys"]], ["TOKEN", "VITE_API_URL"])
        self.assertEqual(result["keys"][1]["phase"], "build")
        for value in ("public-placeholder-not-output", "private-value.invalid", "secret-not-read", "another-value"):
            self.assertNotIn(value, json.dumps(result))
        for path in (".env", ".env.demo", ".ENV.PROD", "../.env.example", "/.env.example", "foo\\bar", "deploy/foo.env"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                source.read(path)

    def test_backend_code_only_keys_and_helpers_are_found_without_values(self):
        self.put(".env.example", b"EXAMPLE_KEY=placeholder\n")
        self.put("app/config.py", b'''import os
DIRECT = os.getenv("CODE_ONLY_KEY", "SECRET_LITERAL_SHOULD_NOT_ESCAPE")
LOOKUP = os.environ.get("LOOKUP_KEY", "NOT_AN_ENV_KEY")
INDEX = os.environ["INDEX_KEY"]
HELPER = _get_str("HELPER_KEY", "DEFAULT_MUST_STAY_PRIVATE")
ALIAS = _env_name_with_deprecated_fallback("CANONICAL_KEY", "DEPRECATED_KEY")
RENDER = any(os.getenv(name) for name in ("RENDER", "RENDER_SERVICE_ID"))
raise RuntimeError("CONFIG MUST NOT EXECUTE")
''')
        result = sources.config_catalog(self.source(), "backend")
        self.assertEqual(result["status"], "catalogued")
        names = {item["name"] for item in result["keys"]}
        self.assertEqual(names, {"EXAMPLE_KEY", "CODE_ONLY_KEY", "LOOKUP_KEY", "INDEX_KEY", "HELPER_KEY",
                                 "CANONICAL_KEY", "DEPRECATED_KEY", "RENDER", "RENDER_SERVICE_ID"})
        item = next(item for item in result["keys"] if item["name"] == "CODE_ONLY_KEY")
        self.assertEqual(item["phase"], "runtime")
        self.assertEqual(item["sources"], ["app/config.py"])
        for value in ("SECRET_LITERAL_SHOULD_NOT_ESCAPE", "NOT_AN_ENV_KEY", "DEFAULT_MUST_STAY_PRIVATE"):
            self.assertNotIn(value, json.dumps(result))

    def test_frontend_known_lists_and_build_accesses_add_names_only(self):
        self.put("scripts/public-config.cjs", b'''const CONFIG_KEYS = {
  LOCALEO_CODE_ONLY: 'SENSITIVE_DEFAULT',
};
throw new Error('DO NOT RUN');
''')
        self.put("config/publicEnvironment.js", b'''export const PUBLIC_ENV_KEYS = Object.freeze([
"LOCALEO_BROWSER_KEY", "LOCALEO_SECOND_KEY"
]);
throw new Error('DO NOT RUN');
''')
        self.put("buildEnvironment.ts", b'''const target = env.LOCALEO_DEPLOY_TARGET;
const api = origin('VITE_API_URL');
origin('LOCALEO_EXPECTED_API_ORIGIN');
const value = env['ANOTHER_BUILD_KEY'];
const defaultValue = 'SENSITIVE_DEFAULT';
throw new Error('DO NOT RUN');
''')
        self.put("pwaBuild.ts", b"throw new Error('DO NOT RUN');\n")
        source = self.source()
        expected = {
            "marketplace": {"LOCALEO_CODE_ONLY"},
            "commercant": {"LOCALEO_BROWSER_KEY", "LOCALEO_SECOND_KEY"},
            "animation": {"LOCALEO_DEPLOY_TARGET", "VITE_API_URL", "LOCALEO_EXPECTED_API_ORIGIN", "ANOTHER_BUILD_KEY"},
        }
        for app, names in expected.items():
            with self.subTest(app=app):
                result = sources.config_catalog(source, app)
                self.assertEqual({item["name"] for item in result["keys"]}, names)
                self.assertTrue(all(item["phase"] == "build" for item in result["keys"]))
                self.assertNotIn("SENSITIVE_DEFAULT", json.dumps(result))
                self.assertEqual(result["status"], "catalogued")

    def test_symlink_and_submodule_are_rejected_as_git_objects(self):
        self.put("ordinary.txt", b"initial")
        sha = self.commit()
        blob = self.git("hash-object", "-w", "--stdin", input=b".env").decode().strip()
        self.git("update-index", "--add", "--cacheinfo", f"120000,{blob},.env.example")
        self.git("update-index", "--add", "--cacheinfo", f"160000,{sha},submodule")
        self.git("commit", "-qm", "Unsafe object fixtures")
        head = self.git("rev-parse", "HEAD").decode().strip()
        source = sources.GitSource(self.root, head)
        for path in (".env.example", "submodule"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                source.read(path)
        self.assertEqual(sources.config_catalog(source, "backend")["status"], "blocked")

    def test_missing_empty_and_legacy_registry_require_investigation(self):
        source = self.migration_source()
        for registry in (None, {"tracking_exists": False, "rows": []}, {"tracking_exists": True, "rows": []}):
            with self.subTest(registry=registry), self.reviewed():
                result = sources.migration_plan(source, registry)
                self.assertEqual(result["status"], "blocked")
                self.assertIsNone(result["pending"])

    def test_registry_holes_are_pending_in_numeric_order_not_max_version(self):
        source = self.migration_source()
        registry = {"tracking_exists": True, "rows": [self.row(source, "v300_last.sql")]}
        with self.reviewed():
            result = sources.migration_plan(source, registry)
        self.assertEqual(result["status"], "planned")
        self.assertEqual(result["pending"], ["v147_production_schema_catchup.sql", "v150_first.sql", "v252_support_financier.sql"])
        self.assertNotIn("v148_purge_commune_test.sql", result["pending"])
        self.assertNotIn("v149_seed_commune_test.sql", result["pending"])

    def test_lf_crlf_and_explicit_legacy_checksums_are_accepted(self):
        source = self.migration_source()
        crlf = hashlib.sha256(b"SELECT 150;\r\n").hexdigest()
        registry = {"tracking_exists": True, "rows": [self.row(source, "v150_first.sql", crlf),
                    self.row(source, "v252_support_financier.sql", LEGACY)]}
        with self.reviewed():
            result = sources.migration_plan(source, registry)
        self.assertEqual(result["status"], "planned")
        self.assertNotIn("v150_first.sql", result["pending"])
        self.assertNotIn("v252_support_financier.sql", result["pending"])

    def test_changed_checksum_unknown_duplicate_and_invalid_registry_block(self):
        source = self.migration_source()
        good = self.row(source, "v150_first.sql")
        registries = [
            {"tracking_exists": True, "rows": [self.row(source, "v150_first.sql", "b" * 64)]},
            {"tracking_exists": True, "rows": [{"filename": "v999_unknown.sql", "checksum_sha256": "b" * 64}]},
            {"tracking_exists": True, "rows": [good, good]},
            {"tracking_exists": True, "rows": [dict(good, secret="NEVER-ECHO")]},
            {"tracking_exists": 1, "rows": [good]},
        ]
        for registry in registries:
            with self.subTest(registry=registry), self.reviewed():
                result = sources.migration_plan(source, registry)
                self.assertEqual(result["status"], "blocked")
                self.assertIsNone(result["pending"])
                self.assertNotIn("NEVER-ECHO", json.dumps(result))

    def test_dangerous_applied_file_is_flagged_without_checksum_revalidation(self):
        source = self.migration_source()
        registry = {"tracking_exists": True, "rows": [self.row(source, "v148_purge_commune_test.sql", "b" * 64)]}
        with self.reviewed():
            result = sources.migration_plan(source, registry)
        self.assertEqual(result["excluded_registry_entries"], ["v148_purge_commune_test.sql"])
        self.assertNotIn("v148_purge_commune_test.sql", result["pending"])

    def test_unknown_runner_does_not_infer_pending_or_evaluate_python(self):
        source = self.migration_source()
        result = sources.migration_plan(source, {"tracking_exists": True, "rows": []})
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["files"], [])
        self.assertIsNone(result["pending"])
        self.assertIn("not reviewed", result["blockers"][0])

    def test_runner_line_endings_do_not_change_review_identity(self):
        self.migration_source()
        self.put(sources.RUNNER_PATH, RUNNER.replace(b"\n", b"\r\n"))
        source = self.source()
        with self.reviewed():
            result = sources.migration_plan(source, None)
        self.assertTrue(result["files"])
        self.assertEqual(result["runner_sha256"], hashlib.sha256(RUNNER).hexdigest())


if __name__ == "__main__":
    unittest.main()
