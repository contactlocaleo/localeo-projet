"""Release preparation contracts, using disposable Git repos and no providers."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import prepare_render_release as release


NOW = datetime(2026, 11, 20, 12, tzinfo=timezone.utc)
COMMIT = "a" * 40
HASH = "b" * 64


def request(app="marketplace", environment="test"):
    return {"schema_version": 1, "environment": environment,
            "applications": {app: COMMIT}, "documentation_sha": "c" * 40}


def ci_receipt(app="backend"):
    return {"observed_at": NOW.isoformat(), "repository": "contactlocaleo/localeo-" + app,
            "checks": [{"workflow": workflow, "job": job, "sha": COMMIT,
                        "run_id": index + 1, "event": "push", "status": "completed",
                        "conclusion": "success"}
                       for index, (workflow, job) in enumerate(release.expected_ci(app))]}


class InputTests(unittest.TestCase):
    def test_explicit_environment_scope_and_full_commit_required(self):
        release.validate_request(request())
        variants = []
        for key in ("environment", "applications", "documentation_sha"):
            value = request()
            del value[key]
            variants.append(value)
        for env in (None, "", "dev", "production"):
            value = request()
            value["environment"] = env
            variants.append(value)
        for apps in ({}, {"unknown": COMMIT}, {"backend": "main"}, {"backend": "abc123"}):
            value = request()
            value["applications"] = apps
            variants.append(value)
        for value in variants:
            with self.subTest(value=value), self.assertRaises(ValueError):
                release.validate_request(value)

    def test_unknown_commands_and_secret_fields_rejected(self):
        for key in ("command", "commands", "env", "token", "secrets"):
            value = request()
            value[key] = "MUST_NOT_BE_ACCEPTED"
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.validate_request(value)
            evidence = {"schema_version": 1, "environment": "test", "request_sha256": HASH,
                        key: "MUST_NOT_BE_ACCEPTED"}
            with self.assertRaises(ValueError):
                release.validate_evidence(evidence, request())

    def test_duplicate_json_members_rejected_in_nested_objects(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "request.json"
            path.write_text('{"applications":{"backend":"a","backend":"b"}}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate JSON"):
                release.read_json(path)

    def test_evidence_cannot_change_environment_or_application_scope(self):
        base = {"schema_version": 1, "environment": "test", "request_sha256": HASH}
        for change in ({"environment": "prod"}, {"ci": {"backend": {}}},
                       {"reviews": {"production_isolation": {}}}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_evidence({**base, **change}, request())

    def test_ci_requires_every_matrix_job_at_exact_sha(self):
        valid = ci_receipt()
        checks = []
        self.assertEqual("passed", release.validate_ci("backend", COMMIT, valid, checks, NOW)["status"])
        matrix = [x for x in valid["checks"] if x["workflow"] == "tests.yml"]
        self.assertGreaterEqual(len(matrix), 4)
        for index in range(len(valid["checks"])):
            receipt = deepcopy(valid)
            receipt["checks"].pop(index)
            with self.subTest(missing=index):
                result = release.validate_ci("backend", COMMIT, receipt, [], NOW)
                self.assertEqual("failed", result["status"])
        receipt = deepcopy(valid)
        receipt["checks"][0]["sha"] = "d" * 40
        self.assertEqual("failed", release.validate_ci("backend", COMMIT, receipt, [], NOW)["status"])

    def test_ci_skipped_neutral_pending_stale_and_failed_are_not_success(self):
        for conclusion in (None, "skipped", "neutral", "failure", "cancelled", "timed_out"):
            receipt = ci_receipt()
            receipt["checks"][0]["conclusion"] = conclusion
            with self.subTest(conclusion=conclusion):
                self.assertEqual("failed", release.validate_ci("backend", COMMIT, receipt, [], NOW)["status"])
        for status in ("queued", "in_progress"):
            receipt = ci_receipt()
            receipt["checks"][0]["status"] = status
            self.assertEqual("failed", release.validate_ci("backend", COMMIT, receipt, [], NOW)["status"])
        for time in (NOW - timedelta(hours=25), NOW + timedelta(seconds=1)):
            receipt = ci_receipt()
            receipt["observed_at"] = time.isoformat()
            self.assertEqual("failed", release.validate_ci("backend", COMMIT, receipt, [], NOW)["status"])

    def test_ci_duplicate_unknown_or_short_sha_jobs_refused(self):
        for kind in ("duplicate", "unknown", "short_sha"):
            receipt = ci_receipt()
            if kind == "duplicate":
                receipt["checks"].append(deepcopy(receipt["checks"][0]))
            elif kind == "unknown":
                receipt["checks"][0]["job"] = "unapproved-job"
            else:
                receipt["checks"][0]["sha"] = "abc123"
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                release.validate_ci("backend", COMMIT, receipt, [], NOW)

    def test_invalid_ci_timestamp_is_blocked_and_never_echoed(self):
        for value in ("PRIVATE_SENTINEL", {"token": "PRIVATE_SENTINEL"}):
            receipt = ci_receipt()
            receipt["observed_at"] = value
            result = release.validate_ci("backend", COMMIT, receipt, [], NOW)
            self.assertEqual("failed", result["status"])
            self.assertIsNone(result["observed_at"])
            self.assertNotIn("PRIVATE_SENTINEL", json.dumps(result))

    def test_target_receipt_binds_service_workspace_branch_domains_and_freshness(self):
        expected = {"render_service_id_verified": "srv-fixture",
                    "expected_endpoints": ["https://test-coffrets.localeo.city"]}
        valid = {"observed_at": NOW.isoformat(), "service_id": "srv-fixture",
                 "workspace_id": "tea-fixture", "branch": "main", "auto_deploy": "no",
                 "domains": [{"hostname": "test-coffrets.localeo.city", "dns": "passed",
                              "attachment": "passed", "tls": "passed", "http": "passed"}]}
        changes = [{}, {"service_id": "srv-other"}, {"workspace_id": "tea-other"},
                   {"branch": "prod"}, {"auto_deploy": "yes"}, {"domains": []},
                   {"observed_at": (NOW - timedelta(days=2)).isoformat()}]
        bad_tls = deepcopy(valid["domains"])
        bad_tls[0]["tls"] = "failed"
        changes.append({"domains": bad_tls})
        for change in changes:
            checks = []
            release.validate_target("marketplace", expected, "tea-fixture", "test", {**valid, **change}, checks, NOW)
            with self.subTest(change=change):
                self.assertEqual("failed" if change else "passed", checks[0]["status"])

    def test_configuration_compares_names_without_values_and_retains_remote_only(self):
        catalog = {"keys": [{"name": key} for key in ("PRESENT", "PREPARED", "EXCLUDED", "MISSING")], "blockers": []}
        source = SimpleNamespace(sha=COMMIT)
        target = {"render_service_id_verified": "srv-fixture"}
        receipt = {"observed_at": NOW.isoformat(), "service_id": "srv-fixture", "sha": COMMIT,
                   "present_keys": ["PRESENT", "REMOTE_ONLY"], "prepared_keys": ["PREPARED"],
                   "not_applicable_keys": ["EXCLUDED"], "reviewed": True,
                   "configuration_revision_sha256": HASH}
        with patch.object(release, "config_catalog", return_value=catalog):
            result = release.configuration("marketplace", source, target, receipt, [], NOW)
            self.assertEqual(["MISSING"], result["missing"])
            self.assertEqual(["REMOTE_ONLY"], result["remote_only"])
            self.assertEqual("failed", result["comparison"])
            receipt["prepared_keys"].append("MISSING")
            self.assertEqual("passed", release.configuration("marketplace", source, target, receipt, [], NOW)["comparison"])
            for changed in ({"sha": "d" * 40}, {"service_id": "srv-other"}, {"reviewed": False},
                            {"observed_at": (NOW - timedelta(days=2)).isoformat()}):
                with self.subTest(changed=changed):
                    result = release.configuration("marketplace", source, target, {**receipt, **changed}, [], NOW)
                    self.assertEqual("failed", result["comparison"])
            for changed in ({"values": {"PRESENT": "sensitive"}}, {"present_keys": ["PRESENT=value"]},
                            {"prepared_keys": ["EXCLUDED"]}, {"not_applicable_keys": ["UNKNOWN"]},
                            {"configuration_revision_sha256": None}, {"configuration_revision_sha256": "short"}):
                with self.subTest(changed=changed), self.assertRaises(ValueError):
                    release.configuration("marketplace", source, target, {**receipt, **changed}, [], NOW)


class DossierTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "localeo-projet"
        self.apps = {}
        for name in ("localeo-projet", "localeo-marketplace", "localeo-backend"):
            path = self.base / name
            path.mkdir()
            self.git(path, "init", "-q")
            self.git(path, "config", "user.email", "fixture@example.invalid")
            self.git(path, "config", "user.name", "Fixture")
            self.git(path, "config", "core.autocrlf", "false")
            (path / ".gitignore").write_text(".artifacts/\n.env\n", encoding="utf-8")
            (path / ".env.example").write_text("PUBLIC_KEY=VALUE_MUST_NOT_ESCAPE\n", encoding="utf-8")
            (path / "app.py").write_text('raise RuntimeError("APPLICATION MUST NOT EXECUTE")\n', encoding="utf-8")
            self.apps[name] = path
        self.registry = {"repositories": [{"name": name, "path": "." if name == "localeo-projet" else "../" + name}
                                           for name in self.apps], "quality": {"checks": {}, "profiles": {}}}
        (self.root / "repositories.json").write_text(json.dumps(self.registry), encoding="utf-8")
        services = {app: {"repository": "localeo-" + app, "render_service_id_verified": "srv-" + app,
                          "expected_endpoints": ["https://test-" + app + ".localeo.city"]}
                    for app in ("marketplace", "backend")}
        self.inventory = {"environments": {"test": {"render_workspace_id_verified": "tea-fixture", "services": services,
                                                   "databases": {"backend": {"render_database_id_verified": "dpg-fixture-a"}}}}}
        inventory_path = self.root / release.INVENTORY
        inventory_path.parent.mkdir(parents=True)
        inventory_path.write_text(json.dumps(self.inventory), encoding="utf-8")
        self.commits = {}
        for name, path in self.apps.items():
            self.git(path, "add", "-A")
            self.git(path, "commit", "-qm", "Fixture")
            self.commits[name] = self.git(path, "rev-parse", "HEAD").strip()
            (path / ".env").write_text("PRIVATE_TOKEN=PRIVATE_MUST_NOT_ESCAPE\n", encoding="utf-8")
        self.request = {"schema_version": 1, "environment": "test",
                        "applications": {"marketplace": self.commits["localeo-marketplace"]},
                        "documentation_sha": self.commits["localeo-projet"]}

    def git(self, root, *args):
        return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                              text=True, timeout=15).stdout

    def call(self, *args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return release.main(["--root", str(self.root), *map(str, args)])

    def local_report(self, blocked=False):
        return {"repositories": release.quality.snapshot(self.root, self.registry),
                "automatic_blockers": ["SENSITIVE_INTERNAL_MESSAGE"] if blocked else [],
                "status": "blocked" if blocked else "prepared_for_review"}

    def test_init_plan_verify_offline_integration_produces_unapproved_dossier(self):
        candidate = self.root / ".artifacts/deploiement/candidate"
        dossier = self.root / ".artifacts/deploiement/result"
        with patch.object(release.quality, "run_checks", side_effect=AssertionError("Tests must not execute")), \
                patch.object(release, "migration_plan", side_effect=AssertionError("No backend in scope")):
            self.assertEqual(0, self.call("init", "--environment", "test", "--applications", "marketplace", "--output", candidate))
            self.assertEqual(self.request, release.read_json(candidate / "request.json"))
            template = release.read_json(candidate / "evidence.template.json")
            self.assertEqual(release.quality.digest(candidate / "request.json"), template["request_sha256"])
            self.assertTrue(all(value["status"] == "not_run" for value in template["reviews"].values()))
            self.assertEqual(0, self.call("plan", "--request", candidate / "request.json",
                                          "--evidence", candidate / "evidence.template.json", "--output", dossier))
            manifest_path = dossier / "manifest.json"
            manifest = release.read_json(manifest_path)
            self.assertEqual("prepared_for_review", manifest["status"])
            self.assertEqual([], manifest["blockers"])
            self.assertIn("ci.marketplace", (dossier / "plan.md").read_text(encoding="utf-8"))
            self.assertIsNone(manifest["database"])
            self.assertEqual(2, manifest["schema_version"])
            self.assertEqual({"repository", "sha", "service_id", "branch", "endpoints"},
                             set(manifest["applications"]["marketplace"]))
            self.assertFalse({"execution_available", "deployment_executed", "authorized", "production_ready",
                              "checks", "quality", "profile", "mode"} & set(manifest))
            self.assertNotIn("MUST_NOT_ESCAPE", manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(0, self.call("verify", "--manifest", manifest_path,
                                          "--sha256", release.quality.digest(manifest_path)))
            old = manifest_path.read_bytes()
            self.assertEqual(2, self.call("plan", "--request", candidate / "request.json", "--output", dossier))
            self.assertEqual(old, manifest_path.read_bytes())

    def test_request_digest_mismatch_is_refused_before_quality(self):
        evidence = {"schema_version": 1, "environment": "test", "request_sha256": "d" * 64}
        with patch.object(release.quality, "prepare_release") as local:
            with self.assertRaisesRegex(ValueError, "different request"):
                release.prepare(self.root, self.request, request_hash=HASH, evidence=evidence, now=NOW)
            local.assert_not_called()

    def test_preparation_reuses_quality_gate_without_copying_arbitrary_messages(self):
        with patch.object(release.quality, "prepare_release", return_value=self.local_report(blocked=True)) as local:
            manifest = release.prepare(self.root, self.request, request_hash=HASH, now=NOW)
        self.assertEqual("prepared_for_review", manifest["status"])
        self.assertEqual([], manifest["blockers"])
        self.assertNotIn("SENSITIVE_INTERNAL_MESSAGE", json.dumps(manifest))
        self.assertFalse(local.call_args.kwargs["demonstration_required"])

    def test_simple_profile_keeps_source_integrity_but_not_manual_receipts_as_blockers(self):
        with patch.object(release.quality, "prepare_release", return_value=self.local_report(blocked=True)):
            manifest = release.prepare(self.root, self.request, request_hash=HASH, now=NOW)
        self.assertEqual("simple", manifest["profile"])
        self.assertEqual([], manifest["blockers"])
        self.assertEqual("prepared_for_review", manifest["status"])
        self.assertIn("ci.marketplace", [x["id"] for x in manifest["checks"] if x["status"] != "passed"])
        folder = release.output_directory(self.root)
        fingerprint = release.write_dossier(folder, manifest)
        release.verify(folder / "manifest.json", fingerprint, now=NOW)

    def test_source_and_input_mutations_during_preparation_block_the_dossier(self):
        initial = self.local_report()
        app_example = self.apps["localeo-marketplace"] / ".env.example"

        def change_source(*args, **kwargs):
            app_example.write_text("CHANGED=hidden\n", encoding="utf-8")
            return initial

        with patch.object(release.quality, "prepare_release", side_effect=change_source):
            manifest = release.prepare(self.root, self.request, request_hash=HASH, now=NOW)
        self.assertIn("sources.unchanged", manifest["blockers"])
        report = self.root / ".artifacts/quality.json"
        report.parent.mkdir(exist_ok=True)
        report.write_text("{}", encoding="utf-8")
        current = self.local_report()

        def change_report(*args, **kwargs):
            report.write_text('{"changed":true}', encoding="utf-8")
            return current

        with patch.object(release.quality, "prepare_release", side_effect=change_report):
            manifest = release.prepare(self.root, self.request, request_hash=HASH, quality_report=report, now=NOW)
        self.assertIn("inputs.unchanged", manifest["blockers"])

    def test_database_registry_only_reaches_migration_planner_when_target_matches(self):
        candidate = {**self.request, "applications": {"backend": self.commits["localeo-backend"]}}
        base = {"schema_version": 1, "environment": "test", "request_sha256": HASH}
        database = {"observed_at": NOW.isoformat(), "database_id": "dpg-fixture-a", "service_id": "srv-backend",
                    "binding_verified": True, "registry": [{"filename": "v1_fixture.sql", "checksum_sha256": HASH}]}
        for changed in ({}, {"database_id": "dpg-other-a"}, {"service_id": "srv-other"},
                        {"binding_verified": False}, {"observed_at": (NOW - timedelta(days=2)).isoformat()}):
            with self.subTest(changed=changed), \
                    patch.object(release.quality, "prepare_release", return_value=self.local_report()) as local, \
                    patch.object(release, "migration_plan", return_value={"blockers": []}) as migrations:
                manifest = release.prepare(self.root, candidate, request_hash=HASH,
                                           evidence={**base, "database": {**database, **changed}}, now=NOW)
                self.assertTrue(local.call_args.kwargs["demonstration_required"])
                self.assertEqual(None if changed else database["registry"], migrations.call_args.args[1])
                self.assertEqual(bool(changed), "database.identity" in manifest["blockers"])

    def test_database_evidence_refused_for_frontend_only(self):
        evidence = {"schema_version": 1, "environment": "test", "request_sha256": HASH, "database": {}}
        with self.assertRaisesRegex(ValueError, "outside requested scope"):
            release.prepare(self.root, self.request, request_hash=HASH, evidence=evidence, now=NOW)

    def test_test_backend_uses_actions_migrations_and_other_environments_preserve_predeploy(self):
        inventory = deepcopy(self.inventory)
        for environment in ("demo", "prod"):
            inventory["environments"][environment] = deepcopy(inventory["environments"]["test"])
        (self.root / release.INVENTORY).write_text(json.dumps(inventory), encoding="utf-8")
        for environment, owner in (("test", "github_actions"), ("demo", "github_actions"),
                                   ("prod", "github_actions")):
            candidate = {**self.request, "environment": environment,
                         "applications": {"backend": self.commits["localeo-backend"]}}
            with self.subTest(environment=environment), \
                    patch.object(release.quality, "prepare_release", return_value=self.local_report()), \
                    patch.object(release, "migration_plan", return_value={"blockers": []}):
                manifest = release.prepare(self.root, candidate, request_hash=HASH, now=NOW)
                self.assertEqual(owner, manifest["database"]["migration_owner"])
                self.assertFalse(manifest["authorized"])

    def test_all_documentary_gates_pass_still_never_authorizes_execution(self):
        commit = self.request["applications"]["marketplace"]
        receipt = ci_receipt("marketplace")
        for item in receipt["checks"]:
            item["sha"] = commit
        evidence = {"schema_version": 1, "environment": "test", "request_sha256": HASH,
                    "ci": {"marketplace": receipt},
                    "targets": {"marketplace": {"observed_at": NOW.isoformat(), "service_id": "srv-marketplace",
                        "workspace_id": "tea-fixture", "branch": "main", "auto_deploy": "no",
                        "domains": [{"hostname": "test-marketplace.localeo.city", "dns": "passed",
                                     "attachment": "passed", "tls": "passed", "http": "passed"}]}},
                    "configuration": {"marketplace": {"observed_at": NOW.isoformat(), "service_id": "srv-marketplace",
                        "sha": commit, "present_keys": ["PUBLIC_KEY"], "prepared_keys": [],
                        "not_applicable_keys": [], "reviewed": True, "configuration_revision_sha256": HASH}},
                    "reviews": {key: {"status": "passed", "observed_at": NOW.isoformat(), "evidence_sha256": HASH}
                                for key in release.requirements(["marketplace"], "test")}}
        with patch.object(release.quality, "prepare_release", return_value=self.local_report()):
            manifest = release.prepare(self.root, self.request, request_hash=HASH, evidence=evidence, now=NOW)
        self.assertEqual([], manifest["blockers"])
        self.assertEqual("prepared_for_review", manifest["status"])
        for key in ("execution_available", "deployment_executed", "authorized", "production_ready"):
            self.assertIs(False, manifest[key])
        self.assertIn("production_isolation", release.requirements(["marketplace"], "prod"))

    def test_output_must_be_ignored_new_child_directory(self):
        for path in (self.root, self.root / ".artifacts/deploiement", self.base / "outside"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.output_directory(self.root, path)
        with patch.object(release.subprocess, "run", return_value=SimpleNamespace(returncode=1)):
            with self.assertRaisesRegex(ValueError, "not ignored"):
                release.output_directory(self.root, self.root / ".artifacts/deploiement/unignored")

    def test_digest_tampering_expiry_and_authorization_changes_are_rejected(self):
        manifest = release.prepare(self.root, self.request, request_hash=HASH, now=NOW)
        folder = release.output_directory(self.root)
        fingerprint = release.write_dossier(folder, manifest)
        path = folder / "manifest.json"
        compact = release.verify(path, fingerprint, now=NOW)
        self.assertEqual(manifest["created_at"], compact["created_at"])
        self.assertEqual(2, compact["schema_version"])
        for when in (NOW - timedelta(seconds=1), NOW + timedelta(hours=24)):
            with self.subTest(when=when), self.assertRaises(ValueError):
                release.verify(path, fingerprint, now=when)
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            release.verify(path, fingerprint, now=NOW)
        for change in ({"authorized": True}, {"status": "blocked"},
                       {"expires_at": (NOW + timedelta(hours=25)).isoformat()}):
            path.write_text(json.dumps({**compact, **change}), encoding="utf-8")
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.verify(path, release.quality.digest(path), now=NOW)


if __name__ == "__main__":
    unittest.main()
