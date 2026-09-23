"""Run explicit workspace checks and prepare evidence; never deploy or declare production ready."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_environment(check):
    """Registry overrides are public test settings, never operator credentials."""
    environment = check.get("env", {})
    if not isinstance(environment, dict) or not all(
            isinstance(key, str) and key and "=" not in key and "\x00" not in key
            and isinstance(value, str) and "\x00" not in value
            for key, value in environment.items()):
        raise ValueError("Check env must map valid variable names to string values")
    return environment


def load_registry(root):
    registry = json.loads((root / "repositories.json").read_text(encoding="utf-8-sig"))
    names = [repo["name"] for repo in registry["repositories"]]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate repository names")
    checks = registry["quality"]["checks"]
    for key, check in checks.items():
        if check["repository"] not in names or not check.get("argv"):
            raise ValueError(f"Invalid check: {key}")
        if not all(isinstance(arg, str) and arg for arg in check["argv"]):
            raise ValueError(f"argv must be a nonempty string array: {key}")
        check_environment(check)
    return registry


def snapshot(root, registry):
    states = {}
    for repo in registry["repositories"]:
        path = (root / repo["path"]).resolve()
        state = {"path": str(path), "sha": None, "dirty": None, "status": "missing"}
        if path.is_dir():
            try:
                def git(*args):
                    return subprocess.run(["git", "-C", str(path), *args], check=True,
                                          capture_output=True, text=True, encoding="utf-8", timeout=15).stdout.strip()
                # A sibling directory inside some other Git repository is not a repository.
                if Path(git("rev-parse", "--show-toplevel")).resolve() != path:
                    raise ValueError("Expected an independent Git root")
                state.update(sha=git("rev-parse", "HEAD"), dirty=bool(git("status", "--porcelain")),
                             status="available")
            except (OSError, subprocess.SubprocessError, ValueError):
                state["status"] = "unverifiable"
        states[repo["name"]] = state
    return states


def selection(registry, profile):
    selected = registry["quality"]["profiles"].get(profile)
    if not selected or len(set(selected)) != len(selected):
        raise ValueError(f"Unknown or empty/duplicate profile: {profile}")
    return [{"id": key, **registry["quality"]["checks"][key]} for key in selected]


def executable(argv):
    """Keep argv boundaries, including on Windows: never launch a .cmd via a shell."""
    argv = list(argv)
    if argv[0] == "python":
        argv[0] = sys.executable
    elif os.name == "nt" and argv[0] == "pnpm":
        corepack = shutil.which("corepack.cmd")
        node = shutil.which("node")
        if not corepack or not node:
            raise FileNotFoundError("node and corepack.cmd must be on PATH for pnpm")
        cli = Path(corepack).parent / "node_modules/corepack/dist/pnpm.js"
        if not cli.is_file():
            raise FileNotFoundError(f"Corepack pnpm JavaScript entry point unavailable: {cli}")
        argv = [node, str(cli), *argv[1:]]
    elif os.name == "nt" and argv[0] == "npm":
        npm = shutil.which("npm.cmd")
        node = shutil.which("node")
        if not npm or not node:
            raise FileNotFoundError("node and npm.cmd must be on PATH")
        cli = Path(npm).parent / "node_modules/npm/bin/npm-cli.js"
        if not cli.is_file():
            raise FileNotFoundError(f"npm JavaScript entry point unavailable: {cli}")
        argv = [node, str(cli), *argv[1:]]
    elif os.name == "nt" and Path(shutil.which(argv[0]) or argv[0]).suffix.lower() in {".cmd", ".bat"}:
        raise ValueError("Batch entry point unsupported: provide an executable and argv")
    return argv


def run_checks(root, registry, profile, *, execute=False, timeout=1800, pg_bin_dir=None):
    started = now()
    registry_before = digest(root / "repositories.json")
    before = snapshot(root, registry)
    checks = []
    for spec in selection(registry, profile):
        check = {**spec, "status": "not_run", "started_at": None, "finished_at": None,
                 "exit_code": None}
        checks.append(check)
        if not execute:
            check["reason"] = "plan_only"
            continue
        required = spec.get("requires", [spec["repository"]])
        missing = [name for name in required if before[name]["status"] != "available"]
        if missing:
            check["reason"] = "Repositories unavailable: " + ", ".join(missing)
            continue
        check["started_at"] = now()
        try:
            arguments = list(spec["argv"])
            if "{pg_bin_dir}" in arguments:
                if pg_bin_dir is None:
                    raise ValueError("--pg-bin-dir is required for the explicitly selected disposable PostgreSQL checks")
                arguments = [str(pg_bin_dir) if arg == "{pg_bin_dir}" else arg for arg in arguments]
            argv = executable(arguments)
            check["executed_argv"] = argv
            # Record only registry-declared public overrides, never the inherited environment.
            environment = {**os.environ, **check_environment(spec)}
            # Inherit stdout/stderr so logs are visible without retaining environment or secrets.
            result = subprocess.run(argv, cwd=before[spec["repository"]]["path"],
                                    timeout=timeout, shell=False, env=environment)
            check.update(status="passed" if result.returncode == 0 else "failed",
                         exit_code=result.returncode)
        except subprocess.TimeoutExpired:
            check.update(status="failed", reason="timeout")
        except (OSError, ValueError) as exc:
            check.update(status="not_run", reason=str(exc))
        check["finished_at"] = now()
    after = snapshot(root, registry)
    return {"schema_version": 1, "kind": "quality", "profile": profile,
            "started_at": started, "finished_at": now(), "registry_sha256": digest(root / "repositories.json"),
            "registry_sha256_before": registry_before,
            "repositories_before": before, "repositories_after": after, "checks": checks,
            "status": ("planned" if not execute else
                       "passed" if all(c["status"] == "passed" for c in checks) else "incomplete_or_failed"),
            "scope": "Only the named profile; no deployment approval or unlisted checks implied."}


def evidence_blockers(root, registry, report, current, *, max_age_hours=24, profile=None):
    blockers = []
    if not isinstance(report, dict) or report.get("kind") != "quality" or report.get("schema_version") != 1:
        return ["Unsupported quality evidence"]
    if report.get("registry_sha256") != digest(root / "repositories.json"):
        blockers.append("Quality registry changed since checks")
    if report.get("registry_sha256_before") != report.get("registry_sha256"):
        blockers.append("Quality registry changed during checks")
    expected = selection(registry, profile or registry["quality"]["release_profile"])
    actual = report.get("checks", [])
    if not isinstance(actual, list) or not all(isinstance(item, dict) for item in actual):
        return ["Malformed check evidence"]
    if len({item.get("id") for item in actual}) != len(actual):
        blockers.append("Duplicate check evidence")
    indexed = {item.get("id"): item for item in actual}
    for check in expected:
        proof = indexed.get(check["id"], {})
        if (proof.get("status") != "passed" or proof.get("exit_code") != 0
                or proof.get("argv") != check["argv"] or proof.get("repository") != check["repository"]
                or proof.get("env", {}) != check.get("env", {})
                or not proof.get("started_at") or not proof.get("finished_at")):
            blockers.append("Missing or unsuccessful check: " + check["id"])
    try:
        start = datetime.fromisoformat(report["started_at"])
        finish = datetime.fromisoformat(report["finished_at"])
        age = (datetime.now(timezone.utc) - finish).total_seconds()
        if finish < start or age < 0 or age > max_age_hours * 3600:
            blockers.append("Quality evidence expired or invalid timestamps")
    except (KeyError, ValueError, TypeError):
        blockers.append("Quality evidence timestamps unavailable")
    for name, state in current.items():
        before = report.get("repositories_before", {}).get(name, {})
        after = report.get("repositories_after", {}).get(name, {})
        if state["status"] != "available":
            blockers.append("Repository unavailable: " + name)
        elif state["dirty"] or before.get("dirty") is not False or after.get("dirty") is not False:
            blockers.append("Uncommitted work invalidates release evidence: " + name)
        elif not state["sha"] or not (state["sha"] == before.get("sha") == after.get("sha")):
            blockers.append("Repository revision changed: " + name)
    return blockers


def prepare_release(root, registry, report_path=None, bundle=None, dataset=None, demo_report=None,
                    demonstration_required=False):
    current = snapshot(root, registry)
    blockers = []
    proofs = {}
    if report_path:
        report = json.loads(report_path.read_text(encoding="utf-8-sig"))
        proofs["quality"] = {"path": str(report_path.resolve()), "sha256": digest(report_path)}
        blockers.extend(evidence_blockers(root, registry, report, current))
    else:
        blockers.append("Quality report missing")
        for name, state in current.items():
            if state["status"] != "available" or state["dirty"] is not False:
                blockers.append("Repository unavailable or uncommitted: " + name)
    if demo_report:
        demo = json.loads(demo_report.read_text(encoding="utf-8-sig"))
        proofs["demonstration"] = {"path": str(demo_report.resolve()), "sha256": digest(demo_report)}
        blockers.extend(evidence_blockers(root, registry, demo, current, profile="demonstration"))
    elif demonstration_required:
        blockers.append("Disposable PostgreSQL demonstration compatibility not verified")
    if bundle:
        try:
            # Existing verifier checks every byte against current canonical sources.
            spec = importlib.util.spec_from_file_location("release_documentation_verifier", Path(__file__).with_name("sync_documentation.py"))
            verifier = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(verifier)
            count = verifier.build_bundle(root, bundle, check=True)
            proofs["documentation"] = {"status": "verified", "documents": count,
                "path": str(bundle.resolve()), "snapshot_sha256": digest(bundle / "documentation.snapshot.json")}
        except (ValueError, OSError) as exc:
            proofs["documentation"] = {"status": "failed", "reason": str(exc)}
            blockers.append("Documentation bundle failed verification")
    else:
        blockers.append("Documentation bundle not verified")
    if dataset and dataset.is_file():
        proofs["dataset"] = {"status": "hashed_only", "path": str(dataset.resolve()), "sha256": digest(dataset)}
    elif demonstration_required or dataset:
        blockers.append("Dataset artifact missing")
    manual = ["Migration ordering and compatibility for the five selected revisions",
              "Backup availability and restoration rehearsal",
              "Target configuration, rollout order and rollback limitations",
              "Acceptance of remaining risks and explicit deployment authorization"]
    if demonstration_required or dataset or demo_report:
        manual.insert(0, "Dataset restore and representative journeys on target environment")
    return {"schema_version": 1, "kind": "release_preparation", "created_at": now(),
            "repositories": current, "proofs": proofs, "automatic_blockers": blockers,
            "demonstration_required": demonstration_required,
            "status": "blocked" if blockers else "prepared_for_review", "production_ready": False, "deployed": False,
            "manual_requirements": [{"requirement": item, "status": "not_verified"} for item in manual]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["plan", "run", "release"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--profile", default="documentation-local")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path, help="Existing quality report for release preparation")
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--dataset", type=Path, help="Artifact to hash; content is never embedded")
    parser.add_argument("--demo-report", type=Path, help="Separate strict PostgreSQL demonstration quality report")
    parser.add_argument("--demonstration-required", action="store_true", help="Require dataset and strict PostgreSQL proof when demonstration is affected")
    parser.add_argument("--pg-bin-dir", type=Path, help="PostgreSQL client directory for explicitly selected demonstration profile")
    parser.add_argument("--timeout", type=int, default=1800, help="Seconds per check")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        registry = load_registry(root)
        if args.timeout <= 0:
            raise ValueError("Timeout must be positive")
        result = (prepare_release(root, registry, args.report, args.bundle, args.dataset, args.demo_report, args.demonstration_required)
                  if args.action == "release" else
                  run_checks(root, registry, args.profile, execute=args.action == "run", timeout=args.timeout, pg_bin_dir=args.pg_bin_dir))
        output = args.output or root / ".artifacts/quality" / (args.action + ".json")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{result['status']}: {output}")
        return 0 if args.action == "plan" or result["status"] in {"passed", "prepared_for_review"} else 1
    except (ValueError, OSError, KeyError) as exc:
        print(f"Quality preparation refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
