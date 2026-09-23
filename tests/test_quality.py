"""Evidence must retain failures and reject stale, partial and dirty release claims."""

import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SPEC = importlib.util.spec_from_file_location("quality", SCRIPTS / "quality.py")
quality = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quality)


class QualityEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "project with spaces"
        self.root.mkdir()
        self.git("init")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Test")
        (self.root / ".gitignore").write_text(".artifacts/\n", encoding="utf-8")
        self.registry = {
            "repositories": [{"name": "project", "path": "."}],
            "quality": {"release_profile": "all", "profiles": {"all": ["test"]},
                "checks": {"test": {"repository": "project", "argv": ["python", "-c", "pass"]}}}}
        self.save_registry()
        self.commit()

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def save_registry(self):
        (self.root / "repositories.json").write_text(json.dumps(self.registry), encoding="utf-8")

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-m", "fixture")

    def run_report(self):
        return quality.run_checks(self.root, self.registry, "all", execute=True)

    def blockers(self, report):
        return quality.evidence_blockers(self.root, self.registry, report,
                                        quality.snapshot(self.root, self.registry))

    def test_successful_real_command_in_spaced_path_has_fresh_evidence(self):
        report = self.run_report()
        self.assertEqual(report["status"], "passed")
        self.assertEqual(self.blockers(report), [])

    def test_plan_does_not_execute_and_cannot_supply_release_evidence(self):
        with patch.object(quality, "executable", side_effect=AssertionError("must not run")):
            report = quality.run_checks(self.root, self.registry, "all")
        self.assertEqual(report["checks"][0]["status"], "not_run")
        self.assertIn("Missing or unsuccessful check: test", self.blockers(report))

    def test_nonzero_command_is_failed_with_exit_code(self):
        self.registry["quality"]["checks"]["test"]["argv"] = ["python", "-c", "raise SystemExit(7)"]
        report = self.run_report()
        self.assertEqual(report["checks"][0]["status"], "failed")
        self.assertEqual(report["checks"][0]["exit_code"], 7)

    def test_absent_executable_is_not_run(self):
        self.registry["quality"]["checks"]["test"]["argv"] = ["localeo-command-that-does-not-exist"]
        report = self.run_report()
        self.assertEqual(report["checks"][0]["status"], "not_run")
        self.assertIsNone(report["checks"][0]["exit_code"])

    def test_timeout_is_failed_and_no_false_success(self):
        self.registry["quality"]["checks"]["test"]["argv"] = ["python", "-c", "import time; time.sleep(30)"]
        report = quality.run_checks(self.root, self.registry, "all", execute=True, timeout=0.05)
        self.assertEqual(report["checks"][0]["reason"], "timeout")
        self.assertEqual(report["checks"][0]["status"], "failed")

    def test_dirty_worktree_blocks_release_even_with_passed_checks(self):
        (self.root / "uncommitted.txt").write_text("work")
        report = self.run_report()
        self.assertEqual(report["status"], "passed")
        self.assertIn("Uncommitted work invalidates release evidence: project", self.blockers(report))

    def test_new_commit_makes_previous_evidence_stale(self):
        report = self.run_report()
        (self.root / "next.txt").write_text("revision")
        self.commit()
        self.assertIn("Repository revision changed: project", self.blockers(report))

    def test_commit_changed_during_checks_is_rejected(self):
        report = self.run_report()
        report["repositories_before"]["project"]["sha"] = "0" * 40
        self.assertIn("Repository revision changed: project", self.blockers(report))

    def test_missing_sibling_prevents_dependent_check_execution(self):
        self.registry["repositories"].append({"name": "missing", "path": "../absent"})
        self.registry["quality"]["checks"]["test"]["requires"] = ["project", "missing"]
        report = self.run_report()
        self.assertEqual(report["checks"][0]["status"], "not_run")
        self.assertIn("Repository unavailable: missing", self.blockers(report))

    def test_partial_profile_cannot_claim_full_release_coverage(self):
        report = self.run_report()
        self.registry["quality"]["checks"]["second"] = copy.deepcopy(self.registry["quality"]["checks"]["test"])
        self.registry["quality"]["profiles"]["all"].append("second")
        self.assertIn("Missing or unsuccessful check: second", self.blockers(report))

    def test_expired_or_future_report_is_rejected(self):
        for offset in (-48, 48):
            with self.subTest(offset=offset):
                report = self.run_report()
                timestamp = (datetime.now(timezone.utc) + timedelta(hours=offset)).isoformat()
                report.update(started_at=timestamp, finished_at=timestamp)
                self.assertIn("Quality evidence expired or invalid timestamps", self.blockers(report))

    def test_registry_edit_invalidates_report(self):
        report = self.run_report()
        self.registry["schema_version"] = 2
        self.save_registry()
        self.assertIn("Quality registry changed since checks", self.blockers(report))

    def test_changed_command_or_duplicate_proof_is_rejected(self):
        report = self.run_report()
        report["checks"][0]["argv"] = ["python", "-c", "print('something else')"]
        report["checks"].append(copy.deepcopy(report["checks"][0]))
        self.assertIn("Duplicate check evidence", self.blockers(report))
        self.assertIn("Missing or unsuccessful check: test", self.blockers(report))

    def test_release_manifest_hashes_without_claiming_dataset_restored(self):
        report = self.run_report()
        evidence = self.root / ".artifacts/quality/run.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_text(json.dumps(report))
        dataset = evidence.parent / "dataset.json"
        dataset.write_text('{"example": true}')
        result = quality.prepare_release(self.root, self.registry, evidence, dataset=dataset)
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["deployed"])
        self.assertEqual(result["proofs"]["dataset"]["status"], "hashed_only")
        self.assertEqual(len(result["proofs"]["dataset"]["sha256"]), 64)
        self.assertTrue(result["manual_requirements"])

    def test_cli_failure_still_writes_report_and_exits_nonzero(self):
        self.registry["quality"]["checks"]["test"]["argv"] = ["python", "-c", "raise SystemExit(3)"]
        self.save_registry()
        result = quality.main(["run", "--root", str(self.root), "--profile", "all"])
        self.assertEqual(result, 1)
        report = json.loads((self.root / ".artifacts/quality/run.json").read_text())
        self.assertEqual(report["checks"][0]["exit_code"], 3)

    def test_unknown_profile_is_refused(self):
        with self.assertRaises(ValueError):
            quality.selection(self.registry, "typo")

    def test_release_bundle_is_verified_against_sources_without_modification(self):
        spec = importlib.util.spec_from_file_location("quality_test_sync", SCRIPTS / "sync_documentation.py")
        sync = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sync)
        guide = self.root / "docs/exploitation/guide.md"
        guide.parent.mkdir(parents=True)
        guide.write_text("# Guide\n", encoding="utf-8")
        (self.root / "documentation.exports.json").write_text(json.dumps({
            "schema_version": 1, "entries": [{"source_path": "docs/exploitation/guide.md", "path": "docs/ops/guide.md"}]}))
        bundle = self.root / ".artifacts/bundle"
        sync.build_bundle(self.root, bundle)
        previous = {str(path): path.read_bytes() for path in bundle.rglob("*") if path.is_file()}
        result = quality.prepare_release(self.root, self.registry, bundle=bundle)
        self.assertEqual(result["proofs"]["documentation"]["status"], "verified")
        self.assertEqual(previous, {str(path): path.read_bytes() for path in bundle.rglob("*") if path.is_file()})
        guide.write_text("# Changed source\n", encoding="utf-8")
        result = quality.prepare_release(self.root, self.registry, bundle=bundle)
        self.assertEqual(result["proofs"]["documentation"]["status"], "failed")
        self.assertEqual(previous, {str(path): path.read_bytes() for path in bundle.rglob("*") if path.is_file()})

    def test_malformed_report_is_not_accepted(self):
        self.assertEqual(self.blockers([]), ["Unsupported quality evidence"])
        report = self.run_report()
        report["checks"] = "passed"
        self.assertEqual(self.blockers(report), ["Malformed check evidence"])

    def test_demo_without_explicit_client_path_is_not_run(self):
        self.registry["quality"]["checks"]["test"]["argv"] = ["python", "{pg_bin_dir}"]
        report = self.run_report()
        self.assertEqual(report["checks"][0]["status"], "not_run")
        self.assertIn("--pg-bin-dir is required", report["checks"][0]["reason"])

    def test_demo_parameter_preserves_spaces_as_single_argument(self):
        self.registry["quality"]["checks"]["test"]["argv"] = [
            "python", "-c", "import sys; assert sys.argv[1] == 'directory with spaces'", "{pg_bin_dir}"]
        report = quality.run_checks(self.root, self.registry, "all", execute=True, pg_bin_dir="directory with spaces")
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["checks"][0]["executed_argv"][-1], "directory with spaces")

    def test_absent_demo_evidence_is_explicitly_blocking(self):
        result = quality.prepare_release(self.root, self.registry, demonstration_required=True)
        self.assertIn("Disposable PostgreSQL demonstration compatibility not verified", result["automatic_blockers"])

    def test_registry_changed_during_checks_is_rejected(self):
        report = self.run_report()
        report["registry_sha256_before"] = "0" * 64
        self.assertIn("Quality registry changed during checks", self.blockers(report))

    def test_ready_to_review_does_not_claim_operator_checks_or_production_ready(self):
        report = self.run_report()
        evidence = self.root / ".artifacts/quality/run.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_text(json.dumps(report))
        # Bundle integrity has separate behavior coverage above; only emulate that result here.
        with patch.object(quality.importlib.util, "module_from_spec") as loaded:
            loaded.return_value.build_bundle.return_value = 1
            with patch.object(quality.importlib.util, "spec_from_file_location"):
                bundle = evidence.parent / "bundle"
                bundle.mkdir()
                (bundle / "documentation.snapshot.json").write_text("{}")
                result = quality.prepare_release(self.root, self.registry, evidence, bundle=bundle)
        self.assertEqual(result["status"], "prepared_for_review")
        self.assertEqual(result["automatic_blockers"], [])
        self.assertTrue(all(item["status"] == "not_verified" for item in result["manual_requirements"]))
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["deployed"])

    def test_git_timeout_marks_repository_unverifiable(self):
        with patch.object(quality.subprocess, "run", side_effect=subprocess.TimeoutExpired(["git"], 15)):
            state = quality.snapshot(self.root, self.registry)
        self.assertEqual(state["project"]["status"], "unverifiable")

    def test_child_receives_public_env_overrides_without_recording_inherited_secrets(self):
        self.registry["quality"]["checks"]["test"].update(
            argv=["python", "-c", "import os; assert os.environ['LOCALEO_PUBLIC_SETTING'] == 'test with spaces'; assert os.environ.get('LOCALEO_INHERITED_CREDENTIAL')"],
            env={"LOCALEO_PUBLIC_SETTING": "test with spaces"})
        private_value = "private-inherited-value-that-must-not-be-reported"
        with patch.dict(os.environ, {"LOCALEO_PUBLIC_SETTING": "original", "LOCALEO_INHERITED_CREDENTIAL": private_value}):
            report = self.run_report()
            self.assertEqual(os.environ["LOCALEO_PUBLIC_SETTING"], "original")
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["checks"][0]["env"], {"LOCALEO_PUBLIC_SETTING": "test with spaces"})
        self.assertNotIn(private_value, json.dumps(report))

    def test_environment_changes_invalidate_previously_passed_check(self):
        self.registry["quality"]["checks"]["test"]["env"] = {"LOCALEO_PUBLIC_SETTING": "old"}
        report = self.run_report()
        self.registry["quality"]["checks"]["test"]["env"] = {"LOCALEO_PUBLIC_SETTING": "new"}
        self.assertIn("Missing or unsuccessful check: test", self.blockers(report))

    def test_registry_rejects_nonstring_and_invalid_environment_settings(self):
        for invalid in (None, [], {"VALUE": False}, {"VALUE": 1}, {"": "value"},
                        {"BAD=NAME": "value"}, {"BAD\x00NAME": "value"}, {"VALUE": "bad\x00value"}):
            with self.subTest(environment=invalid):
                self.registry["quality"]["checks"]["test"]["env"] = invalid
                self.save_registry()
                with self.assertRaisesRegex(ValueError, "env must map"):
                    quality.load_registry(self.root)


if __name__ == "__main__":
    unittest.main()
