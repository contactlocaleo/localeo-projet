"""Prepare an offline Render release dossier. No provider calls or deployment capability."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid

import quality
from render_release_sources import GitSource, config_catalog, migration_plan

ROOT = Path(__file__).resolve().parents[1]
APPS = ("backend", "marketplace", "commercant", "animation")
BRANCHES = {"test": "main", "demo": "demo", "prod": "prod"}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
KEY = re.compile(r"[A-Z][A-Z0-9_]*\Z")
INVENTORY = Path("docs/exploitation/deploiement/inventaire-render.json")
MAX_AGE = timedelta(hours=24)
# Expected names from versioned workflows, not a claim of successful remote runs.
CI = {
    "backend": {
        "tests.yml": ["tests (3.12)", "tests (3.14)",
                      "Architecture contracts and test ownership (3.12)",
                      "Architecture contracts and test ownership (3.14)",
                      "Legal publication CLI and public readers", "postgres"],
        "security.yml": ["secrets", "dependencies", "sast"],
        "browser-erp.yml": ["erp"], "animation-audit.yml": ["animation-audit"],
        "demo-compatibility.yml": ["Generated dataset, migrations and verified restore"],
    },
    "marketplace": {"quality.yml": ["Lint", "Security contracts", "Server and isolated build",
                                      "Chromium fixture journeys", "Marketplace quality gate"]},
    "commercant": {"frontend-quality.yml": ["quality"]},
    "animation": {"quality.yml": ["quality"]},
}
GATES = ("configuration_review", "migration_compatibility", "backup_policy",
         "restore_rehearsal", "rollout_and_recovery", "post_deploy_checks")


def require(ok, message="Invalid input shape or value (content withheld)"):
    if not ok:
        raise ValueError(message)


def shape(value, required, optional=()):
    require(isinstance(value, dict) and set(required) <= value.keys()
            and value.keys() <= set(required) | set(optional))


def duplicate_safe(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON member")
        result[key] = value
    return result


def read_json(path):
    require(path.is_file() and path.stat().st_size <= 8_000_000, "Missing or oversized JSON input")
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=duplicate_safe)


def digest_bytes(content):
    return hashlib.sha256(content).hexdigest()


def date(value):
    require(isinstance(value, str))
    instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(instant.tzinfo is not None, "Timezone required")
    return instant


def fresh(value, now):
    try:
        return timedelta(0) <= now - date(value) <= MAX_AGE
    except (ValueError, TypeError):
        return False


def public_timestamp(value):
    try:
        return date(value).isoformat()
    except (ValueError, TypeError):
        return None


def sha(value, length=40):
    require(isinstance(value, str) and (HEX40 if length == 40 else HEX64).fullmatch(value),
            "Full lowercase commit SHA or SHA256 required")
    return value


def names(value):
    require(isinstance(value, list) and all(isinstance(x, str) and KEY.fullmatch(x) for x in value))
    require(len(set(value)) == len(value), "Duplicate configuration key")
    return set(value)


def validate_request(request):
    shape(request, ("schema_version", "environment", "applications", "documentation_sha"))
    require(type(request["schema_version"]) is int and request["schema_version"] == 1)
    require(isinstance(request["environment"], str) and request["environment"] in BRANCHES,
            "Explicit environment must be test, demo or prod")
    applications = request["applications"]
    require(isinstance(applications, dict) and applications and applications.keys() <= set(APPS),
            "Explicit application scope required")
    for value in applications.values():
        sha(value)
    sha(request["documentation_sha"])


def check_row(checks, key, passed, present=True):
    checks.append({"id": key, "status": "passed" if passed else "failed" if present else "not_run"})


def essential_checks(applications):
    result = {"documentation.sha", "sources.unchanged", "inputs.unchanged"}
    result.update(f"source.{app}" for app in applications)
    if "backend" in applications:
        result.update(("database.identity", "database.migrations"))
    return result


def expected_ci(app):
    return [(workflow, job) for workflow, jobs in CI[app].items() for job in jobs]


def validate_ci(app, commit, receipt, checks, now):
    expected = expected_ci(app)
    if receipt is None:
        check_row(checks, f"ci.{app}", False, False)
        return {"status": "not_run", "required": [{"workflow": w, "job": j} for w, j in expected]}
    shape(receipt, ("observed_at", "repository", "checks"))
    require(receipt["repository"] == "contactlocaleo/localeo-" + app)
    require(isinstance(receipt["checks"], list))
    seen = set()
    summaries = []
    for item in receipt["checks"]:
        shape(item, ("workflow", "job", "sha", "run_id", "event", "status", "conclusion"))
        pair = (item["workflow"], item["job"])
        require(all(isinstance(x, str) for x in pair) and pair in expected and pair not in seen,
                "Unexpected or duplicate CI job")
        seen.add(pair)
        sha(item["sha"])
        require(type(item["run_id"]) is int and item["run_id"] > 0)
        require(item["event"] in ("push", "workflow_dispatch", "pull_request"))
        require(item["status"] in ("queued", "in_progress", "completed"))
        require(item["conclusion"] in (None, "success", "failure", "cancelled", "skipped", "neutral", "timed_out", "action_required", "stale"))
        passed = item["sha"] == commit and item["status"] == "completed" and item["conclusion"] == "success"
        summaries.append({**item, "matched": passed})
    passed = fresh(receipt["observed_at"], now) and seen == set(expected) and all(x["matched"] for x in summaries)
    present = receipt["observed_at"] is not None or bool(summaries)
    check_row(checks, f"ci.{app}", passed, present)
    return {"status": "passed" if passed else "failed" if present else "not_run", "observed_at": public_timestamp(receipt["observed_at"]),
            "repository": receipt["repository"], "checks": summaries,
            "provenance": "supplied_receipt_not_authenticated; executor_must_requery_github"}


def validate_target(app, expected, workspace, env, receipt, checks, now):
    if receipt is None:
        check_row(checks, f"target.{app}", False, False)
        return
    shape(receipt, ("observed_at", "service_id", "workspace_id", "branch", "auto_deploy", "domains"))
    require(receipt["auto_deploy"] in ("yes", "no", None))
    require(isinstance(receipt["domains"], list))
    domains = {}
    wanted = {x.removeprefix("https://") for x in expected["expected_endpoints"]}
    for domain in receipt["domains"]:
        shape(domain, ("hostname", "dns", "attachment", "tls", "http"))
        require(isinstance(domain["hostname"], str) and domain["hostname"] in wanted
                and domain["hostname"] not in domains)
        require(all(domain[x] in ("passed", "failed", "not_run") for x in ("dns", "attachment", "tls", "http")))
        domains[domain["hostname"]] = all(domain[x] == "passed" for x in ("dns", "attachment", "tls", "http"))
    passed = (fresh(receipt["observed_at"], now) and receipt["service_id"] == expected["render_service_id_verified"]
              and receipt["workspace_id"] == workspace and receipt["branch"] == BRANCHES[env]
              and receipt["auto_deploy"] == "no" and set(domains) == wanted and all(domains.values()))
    check_row(checks, f"target.{app}", passed, receipt["observed_at"] is not None)


def configuration(app, source, target, receipt, checks, now):
    catalog = config_catalog(source, app)
    known = {item["name"] for item in catalog["keys"]}
    check_row(checks, f"configuration_sources.{app}", not catalog["blockers"] and bool(known))
    result = {"catalog": catalog, "comparison": "unknown", "missing": None, "remote_only": None}
    if receipt is None:
        check_row(checks, f"configuration.{app}", False, False)
        return result
    shape(receipt, ("observed_at", "service_id", "sha", "present_keys", "prepared_keys", "not_applicable_keys", "reviewed", "configuration_revision_sha256"))
    require(type(receipt["reviewed"]) is bool)
    if receipt["reviewed"] or receipt["configuration_revision_sha256"] is not None:
        sha(receipt["configuration_revision_sha256"], 64)
    sha(receipt["sha"])
    present, prepared, excluded = (names(receipt[key]) for key in ("present_keys", "prepared_keys", "not_applicable_keys"))
    require(excluded <= known and prepared <= known and not (excluded & prepared)
            and not (present & prepared))
    missing = sorted(known - present - prepared - excluded)
    passed = (fresh(receipt["observed_at"], now) and receipt["service_id"] == target["render_service_id_verified"]
              and receipt["sha"] == source.sha and receipt["reviewed"] and not missing)
    check_row(checks, f"configuration.{app}", passed, receipt["observed_at"] is not None)
    result.update(comparison="passed" if passed else "failed", missing=missing,
                  remote_only=sorted(present - known), prepared_keys=sorted(prepared),
                  not_applicable_keys=sorted(excluded), configuration_revision_sha256=receipt["configuration_revision_sha256"])
    return result


def requirements(scope, env):
    result = list(GATES)
    if "backend" not in scope:
        result = [x for x in result if x not in ("migration_compatibility", "backup_policy", "restore_rehearsal")]
    if env == "prod":
        result.append("production_isolation")
    return result


def validate_evidence(evidence, request):
    shape(evidence, ("schema_version", "environment", "request_sha256"),
          ("ci", "targets", "configuration", "database", "reviews"))
    require(type(evidence["schema_version"]) is int and evidence["schema_version"] == 1)
    require(evidence["environment"] == request["environment"], "Evidence environment mismatch")
    sha(evidence["request_sha256"], 64)
    for section in ("ci", "targets", "configuration"):
        value = evidence.get(section, {})
        require(isinstance(value, dict) and value.keys() <= request["applications"].keys())
    reviews = evidence.get("reviews", {})
    require(isinstance(reviews, dict) and reviews.keys() <= set(requirements(request["applications"], request["environment"])))
    for value in reviews.values():
        shape(value, ("status", "observed_at", "evidence_sha256"))
        require(value["status"] in ("passed", "failed", "not_run"))
        if value["status"] != "not_run" or value["evidence_sha256"] is not None:
            sha(value["evidence_sha256"], 64)


def evidence_template(root, request, request_hash):
    """Names and expected identities only; never turn inventory into fresh observations."""
    validate_request(request)
    env = read_json(root / INVENTORY)["environments"][request["environment"]]
    result = {"schema_version": 1, "environment": request["environment"], "request_sha256": request_hash,
              "ci": {}, "targets": {}, "configuration": {},
              "reviews": {key: {"status": "not_run", "observed_at": None, "evidence_sha256": None}
                          for key in requirements(request["applications"], request["environment"])}}
    for app, commit in request["applications"].items():
        service = env["services"][app]
        result["ci"][app] = {"observed_at": None, "repository": "contactlocaleo/localeo-" + app, "checks": []}
        result["targets"][app] = {"observed_at": None, "service_id": service["render_service_id_verified"],
                                  "workspace_id": env["render_workspace_id_verified"], "branch": None, "auto_deploy": None,
                                  "domains": [{"hostname": url.removeprefix("https://"), "dns": "not_run",
                                               "attachment": "not_run", "tls": "not_run", "http": "not_run"}
                                              for url in service["expected_endpoints"]]}
        result["configuration"][app] = {"observed_at": None, "service_id": service["render_service_id_verified"],
                                        "sha": commit, "present_keys": [], "prepared_keys": [],
                                        "not_applicable_keys": [], "reviewed": False, "configuration_revision_sha256": None}
    if "backend" in request["applications"]:
        result["database"] = {"observed_at": None, "database_id": env["databases"]["backend"]["render_database_id_verified"],
                              "service_id": env["services"]["backend"]["render_service_id_verified"], "binding_verified": False,
                              "registry": {"tracking_exists": False, "rows": []}}
    return result


def prepare(root, request, *, request_hash, evidence=None, evidence_hash=None,
            quality_report=None, bundle=None, demo_report=None, dataset=None, now=None,
            simple=False):
    """Recompute all local evidence; supplied receipts never confer authorization."""
    now = now or datetime.now(timezone.utc)
    validate_request(request)
    evidence = evidence or {"schema_version": 1, "environment": request["environment"], "request_sha256": request_hash}
    validate_evidence(evidence, request)
    require(evidence["request_sha256"] == request_hash, "Receipts refer to a different request")
    input_paths = {"registry": root / "repositories.json", "inventory": root / INVENTORY,
                   "preparer": Path(__file__), "source_analyzer": Path(__file__).with_name("render_release_sources.py"),
                   "quality_verifier": Path(quality.__file__)}
    for key, path in (("quality_report", quality_report), ("demo_report", demo_report), ("dataset", dataset),
                      ("bundle_snapshot", bundle / "documentation.snapshot.json" if bundle else None)):
        if path is not None and path.is_file():
            input_paths[key] = path
    input_hashes = {key: quality.digest(path) for key, path in input_paths.items()}
    registry = quality.load_registry(root)
    local = quality.prepare_release(root, registry, quality_report, bundle, dataset, demo_report,
                                    demonstration_required="backend" in request["applications"])
    checks = []
    check_row(checks, "quality.workspace", not local["automatic_blockers"], quality_report is not None)
    # Do not copy arbitrary report messages, paths, commands, env or exception contents.
    local_summary = {"status": local["status"], "blocker_count": len(local["automatic_blockers"]),
                     "quality_report_sha256": quality.digest(quality_report) if quality_report else None,
                     "bundle_snapshot_sha256": quality.digest(bundle / "documentation.snapshot.json")
                     if bundle and (bundle / "documentation.snapshot.json").is_file() else None,
                     "demo_report_sha256": quality.digest(demo_report) if demo_report else None,
                     "dataset_sha256": quality.digest(dataset) if dataset and dataset.is_file() else None}
    inventory = read_json(root / INVENTORY)
    env = request["environment"]
    target_env = inventory["environments"][env]
    workspace = target_env["render_workspace_id_verified"]
    require(isinstance(workspace, str) and re.fullmatch(r"tea-[a-z0-9]+", workspace))
    docs = local["repositories"].get("localeo-projet", {})
    check_row(checks, "documentation.sha", docs.get("sha") == request["documentation_sha"] and docs.get("dirty") is False)
    sources = {r["name"]: (root / r["path"]).resolve() for r in registry["repositories"]}
    applications = {}
    for app, commit in request["applications"].items():
        target = target_env["services"][app]
        require(target["repository"] == "localeo-" + app)
        require(isinstance(target["render_service_id_verified"], str)
                and re.fullmatch(r"srv-[a-z0-9]+", target["render_service_id_verified"]))
        require(isinstance(target["expected_endpoints"], list) and target["expected_endpoints"]
                and all(isinstance(x, str) and re.fullmatch(r"https://[a-z-]+\.localeo\.city", x) for x in target["expected_endpoints"]))
        state = local["repositories"].get("localeo-" + app, {})
        check_row(checks, f"source.{app}", state.get("sha") == commit and state.get("dirty") is False)
        source = GitSource(sources["localeo-" + app], commit)
        validate_target(app, target, workspace, env, evidence.get("targets", {}).get(app), checks, now)
        applications[app] = {"repository": "contactlocaleo/localeo-" + app, "sha": commit,
                             "service_id": target["render_service_id_verified"], "branch": BRANCHES[env],
                             "endpoints": target["expected_endpoints"],
                             "ci": validate_ci(app, commit, evidence.get("ci", {}).get(app), checks, now),
                             "configuration": configuration(app, source, target, evidence.get("configuration", {}).get(app), checks, now)}
    database = None
    if "backend" in applications:
        expected_db = target_env["databases"]["backend"]["render_database_id_verified"]
        require(isinstance(expected_db, str) and re.fullmatch(r"dpg-[a-z0-9-]+", expected_db))
        receipt = evidence.get("database")
        registry_rows = None
        if receipt is not None:
            shape(receipt, ("observed_at", "database_id", "service_id", "binding_verified", "registry"))
            require(type(receipt["binding_verified"]) is bool)
            matched = (receipt["database_id"] == expected_db and receipt["service_id"] == applications["backend"]["service_id"]
                       and receipt["binding_verified"] and fresh(receipt["observed_at"], now))
            if matched:
                registry_rows = receipt["registry"]
            check_row(checks, "database.identity", matched, receipt["observed_at"] is not None)
        else:
            check_row(checks, "database.identity", False, False)
        source = GitSource(sources["localeo-backend"], request["applications"]["backend"])
        migration = migration_plan(source, registry_rows)
        check_row(checks, "database.migrations", not migration["blockers"], registry_rows is not None)
        database = {"database_id": expected_db, "migrations": migration, "backup": "required_before_execution",
                    "migration_owner": "github_actions"}
    else:
        require("database" not in evidence, "Database evidence outside requested scope")
    for key in requirements(applications, env):
        receipt = evidence.get("reviews", {}).get(key)
        check_row(checks, "review." + key, receipt is not None and receipt["status"] == "passed"
                  and fresh(receipt["observed_at"], now), receipt is not None and receipt["status"] != "not_run")
    check_row(checks, "sources.unchanged", quality.snapshot(root, registry) == local["repositories"])
    check_row(checks, "inputs.unchanged", all(path.is_file() and quality.digest(path) == input_hashes[key]
                                            for key, path in input_paths.items()))
    essential = essential_checks(applications)
    blockers = [x["id"] for x in checks if x["status"] != "passed" and (not simple or x["id"] in essential)]
    return {"schema_version": 1, "kind": "render_release_plan", "mode": "plan",
            "profile": "simple" if simple else "strict",
            "id": str(uuid.uuid4()), "created_at": now.isoformat(), "expires_at": (now + MAX_AGE).isoformat(),
            "environment": env, "workspace_id": workspace, "documentation_sha": request["documentation_sha"],
            "request_sha256": request_hash, "evidence_sha256": evidence_hash,
            "input_hashes": input_hashes,
            "inventory_sha256": quality.digest(root / INVENTORY),
            "preparer_sha256": digest_bytes(Path(__file__).read_bytes()),
            "source_analyzer_sha256": digest_bytes(Path(__file__).with_name("render_release_sources.py").read_bytes()),
            "applications": applications, "database": database, "quality": local_summary,
            "checks": checks, "blockers": blockers, "status": "blocked" if blockers else "prepared_for_review",
            "execution_available": False, "deployment_executed": False, "authorized": False,
            "production_ready": False, "executor_revision": None,
            "limitations": ["Offline preparation; imported receipts are not authenticated provider evidence.",
                            "Executor must revalidate trusted policy, SHA, target and evidence before any write.",
                            "Configuration catalogue is static and non-exhaustive; no secret values are read or stored.",
                            "No workflow, backup, approval, migration or deployment was executed."]}


def output_directory(root, requested=None):
    base = (root / ".artifacts/deploiement").resolve()
    folder = requested or base / ("plan-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:12])
    folder = folder.resolve()
    require(folder.is_relative_to(base) and folder != base, "Output must be a new .artifacts/deploiement subdirectory")
    # Check both directory and representative files against Git exclusions.
    for candidate in (folder, folder / "manifest.json", folder / "request.json"):
        proc = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "--", str(candidate)], capture_output=True, timeout=15)
        require(proc.returncode == 0, "Output is not ignored by Git")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def write_dossier(folder, manifest):
    path = folder / "manifest.json"
    quality.AtomicReportWriter(path)(manifest)
    fingerprint = quality.digest(path)
    with (folder / "manifest.sha256").open("x", encoding="ascii") as stream:
        stream.write(fingerprint + "  manifest.json\n")
    lines = ["# Plan Render", "", f"Cible : `{manifest['environment']}` — verdict : **{manifest['status']}**.",
             "", "Préparation locale ; aucune autorisation ni exécution de déploiement.",
             "Les reçus importés restent déclaratifs. L'exécuteur devra les revérifier.", "",
             f"Empreinte SHA256 : `{fingerprint}`", ""]
    shown = (essential_checks(manifest["applications"]) if manifest.get("profile") == "simple"
             else {x["id"] for x in manifest["checks"]})
    lines.extend(("| Contrôle bloquant | Résultat |", "| --- | --- |"))
    lines.extend(f"| {x['id']} | {x['status']} |" for x in manifest["checks"] if x["id"] in shown)
    if manifest.get("profile") == "simple":
        optional = [x for x in manifest["checks"] if x["id"] not in shown and x["status"] != "passed"]
        lines.extend(("", f"Observations facultatives non validées : {len(optional)} ; détails dans manifest.json."))
    with (folder / "plan.md").open("x", encoding="utf-8") as stream:
        stream.write("\n".join(lines) + "\n")
    return fingerprint


def verify(path, expected, now=None):
    sha(expected, 64)
    require(quality.digest(path) == expected, "Manifest digest mismatch")
    manifest = read_json(path)
    require(manifest.get("schema_version") == 1 and manifest.get("kind") == "render_release_plan")
    require(manifest.get("mode") == "plan" and manifest.get("environment") in BRANCHES)
    require(all(manifest.get(key) is False for key in ("execution_available", "deployment_executed", "authorized", "production_ready")),
            "Not an offline, unauthorized plan")
    require(manifest.get("status") in ("blocked", "prepared_for_review"))
    instant = now or datetime.now(timezone.utc)
    start, end = date(manifest["created_at"]), date(manifest["expires_at"])
    require(start <= instant < end and timedelta(0) < end - start <= MAX_AGE, "Manifest expired or invalid dates")
    require(isinstance(manifest.get("checks"), list) and manifest["checks"])
    require(all(isinstance(x, dict) and x.get("status") in ("passed", "failed", "not_run") for x in manifest["checks"]))
    profile = manifest.get("profile", "strict")
    require(profile in ("simple", "strict"))
    essential = essential_checks(manifest.get("applications", {}))
    failed = [x["id"] for x in manifest["checks"] if x["status"] != "passed"
              and (profile == "strict" or x["id"] in essential)]
    require(failed == manifest.get("blockers") and bool(failed) == (manifest["status"] == "blocked"))
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="action", required=True)
    init = sub.add_parser("init", help="Write an explicit scope request with current HEAD candidates only")
    init.add_argument("--environment", choices=tuple(BRANCHES), required=True)
    init.add_argument("--applications", choices=APPS, nargs="+", required=True)
    init.add_argument("--output", type=Path)
    template = sub.add_parser("template", help="Write unknown receipts template bound to an explicit request")
    template.add_argument("--request", type=Path, required=True)
    template.add_argument("--output", type=Path)
    plan = sub.add_parser("plan", help="Prepare an offline manifest; never execute quality tests or deployment")
    plan.add_argument("--request", type=Path, required=True)
    plan.add_argument("--evidence", type=Path)
    plan.add_argument("--quality-report", type=Path)
    plan.add_argument("--bundle", type=Path)
    plan.add_argument("--demo-report", type=Path)
    plan.add_argument("--dataset", type=Path)
    plan.add_argument("--simple", action="store_true", help="Use the streamlined TEST/DEMO/PROD delivery profile")
    plan.add_argument("--output", type=Path)
    check = sub.add_parser("verify", help="Check supplied fingerprint and expiry only; no authorization or remote validation")
    check.add_argument("--manifest", type=Path, required=True)
    check.add_argument("--sha256", required=True)
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        if args.action == "verify":
            manifest = verify(args.manifest, args.sha256)
            print(f"Integrity verified; dossier {manifest['status']}; authorization remains false")
            return 0
        if args.action == "init":
            require(len(set(args.applications)) == len(args.applications), "Duplicate application")
            states = quality.snapshot(root, quality.load_registry(root))
            request = {"schema_version": 1, "environment": args.environment,
                       "applications": {app: states["localeo-" + app]["sha"] for app in args.applications},
                       "documentation_sha": states["localeo-projet"]["sha"]}
            validate_request(request)
            folder = output_directory(root, args.output)
            quality.AtomicReportWriter(folder / "request.json")(request)
            quality.AtomicReportWriter(folder / "evidence.template.json")(
                evidence_template(root, request, quality.digest(folder / "request.json")))
            print(f"Candidate request only (HEAD is not approval): {folder / 'request.json'}")
            return 0
        request = read_json(args.request)
        if args.action == "template":
            template = evidence_template(root, request, quality.digest(args.request))
            folder = output_directory(root, args.output)
            quality.AtomicReportWriter(folder / "evidence.template.json")(template)
            print(f"Unknown receipts template: {folder / 'evidence.template.json'}")
            return 0
        evidence = read_json(args.evidence) if args.evidence else None
        manifest = prepare(root, request, request_hash=quality.digest(args.request), evidence=evidence,
                           evidence_hash=quality.digest(args.evidence) if args.evidence else None,
                           quality_report=args.quality_report, bundle=args.bundle, demo_report=args.demo_report,
                           dataset=args.dataset, simple=args.simple)
        folder = output_directory(root, args.output)
        fingerprint = write_dossier(folder, manifest)
        print(f"{manifest['status']}: {folder / 'manifest.json'}\nsha256: {fingerprint}")
        return 1 if manifest["blockers"] else 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, subprocess.SubprocessError):
        # Raw provider or report contents must not be echoed in error messages.
        print("Preparation refused: invalid, missing, changed or unsupported input/output. No deployment executed.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
