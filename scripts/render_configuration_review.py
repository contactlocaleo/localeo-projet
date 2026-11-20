"""Compare committed configuration names with Render without persisting values.

The Render API returns secret values. This program discards them in memory and
only writes key names and review findings to an ignored local dossier.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from render_release_sources import GitSource, config_catalog
import prepare_render_release as release


ROOT = Path(__file__).resolve().parents[1]
APPS = ("backend", "marketplace", "animation", "commercant")
KEY = re.compile(r"[A-Z][A-Z0-9_]*\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")
API = "https://api.render.com/v1"
PAGE_SIZE = 100
MAX_RESPONSE = 4 * 1024 * 1024


class ReviewError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ReviewError(message)


def fetch(path: str, token: str) -> object:
    request = urllib.request.Request(
        API + path,
        headers={"Accept": "application/json", "Authorization": "Bearer " + token},
        method="GET",
    )
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=15) as response:
            raw = response.read(MAX_RESPONSE + 1)
    except urllib.error.HTTPError as error:
        raise ReviewError(f"Render API HTTP {error.code}; response withheld") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ReviewError("Render API unavailable; details withheld") from None
    require(len(raw) <= MAX_RESPONSE, "Render response too large")
    try:
        return json.loads(raw)
    except (UnicodeError, ValueError):
        raise ReviewError("Render API returned invalid JSON; content withheld") from None


def direct_keys(service_id: str, token: str, get=fetch) -> list[str]:
    result: set[str] = set()
    cursor: str | None = None
    seen_cursors: set[str] = set()
    while True:
        query = urllib.parse.urlencode({"limit": PAGE_SIZE, **({"cursor": cursor} if cursor else {})})
        page = get(f"/services/{service_id}/env-vars?{query}", token)
        require(isinstance(page, list), "Invalid Render variable page")
        require(len(page) <= PAGE_SIZE, "Oversized Render variable page")
        for row in page:
            require(isinstance(row, dict) and isinstance(row.get("envVar"), dict),
                    "Invalid Render variable row")
            variable = row["envVar"]
            name = variable.get("key")
            require(isinstance(name, str) and KEY.fullmatch(name) is not None,
                    "Invalid Render variable name")
            require(isinstance(variable.get("value"), str), "Invalid Render variable value shape")
            require(name not in result, "Duplicate Render variable name")
            result.add(name)
        if len(page) < PAGE_SIZE:
            return sorted(result)
        cursor = page[-1].get("cursor")
        require(isinstance(cursor, str) and cursor and cursor not in seen_cursors,
                "Render variable pagination incomplete")
        seen_cursors.add(cursor)


def group_links(workspace_id: str, services: set[str], token: str, get=fetch) -> dict[str, list[str]]:
    query = urllib.parse.urlencode({"ownerId": workspace_id, "limit": PAGE_SIZE})
    page = get(f"/env-groups?{query}", token)
    require(isinstance(page, list) and len(page) < PAGE_SIZE,
            "Render environment group inventory incomplete")
    links = {service_id: [] for service_id in services}
    for group in page:
        require(isinstance(group, dict) and group.get("ownerId") == workspace_id
                and isinstance(group.get("id"), str)
                and isinstance(group.get("serviceLinks"), list), "Invalid Render environment group")
        for link in group["serviceLinks"]:
            require(isinstance(link, dict), "Invalid Render environment group link")
            service_id = link.get("id")
            if service_id in links:
                links[service_id].append(group["id"])
    return {key: sorted(set(value)) for key, value in links.items()}


def build_review(app: str, plan_app: dict, deployed_sha: str, remote_keys: list[str] | None,
                 linked_groups: list[str] | None, observed_at: str | None) -> dict:
    source = GitSource(ROOT.parent / ("localeo-" + app), deployed_sha)
    deployed = config_catalog(source, app)
    candidate = plan_app["configuration"]["catalog"]
    require(not deployed["blockers"] and not candidate["blockers"],
            "Configuration source analysis blocked")
    old = {item["name"] for item in deployed["keys"]}
    new = {item["name"] for item in candidate["keys"]}
    present = set(remote_keys) if remote_keys is not None else None
    return {
        "schema_version": 1,
        "kind": "localeo_configuration_review",
        "environment": "demo",
        "application": app,
        "render_service_id": plan_app["service_id"],
        "deployed_commit": deployed_sha,
        "candidate_commit": plan_app["sha"],
        "render_observed_at": observed_at,
        "render_direct_keys": sorted(present) if present is not None else None,
        "render_linked_environment_group_ids": linked_groups,
        "analysis_scope": "static_public_examples_and_known_config_code_not_exhaustive",
        "deployed_code_key_count": len(old),
        "candidate_code_keys": candidate["keys"],
        "new_in_candidate_code": sorted(new - old),
        "no_longer_referenced_in_candidate_catalog": sorted(old - new),
        "candidate_keys_absent_from_direct_render_configuration": sorted(new - present) if present is not None else None,
        "new_candidate_keys_absent_from_direct_render_configuration": sorted((new - old) - present) if present is not None else None,
        "render_keys_outside_candidate_catalog": sorted(present - new) if present is not None else None,
        "formerly_referenced_keys_still_on_render": sorted((old - new) & present) if present is not None else None,
        "reviewed": False,
        "interpretation": "Absent keys may be optional or supplied by an environment group. Outside-catalog keys are not approved for deletion.",
    }


def prepare(plan_path: Path, baseline_path: Path, output_dir: Path, live: bool) -> list[dict]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    require(plan.get("environment") == "demo" and set(plan.get("applications", {})) == set(APPS),
            "Expected a four-application DEMO plan")
    require(isinstance(baseline, dict) and set(baseline) == set(APPS)
            and all(isinstance(value, str) and SHA.fullmatch(value) for value in baseline.values()),
            "Invalid deployed commit baseline")
    token = os.environ.get("RENDER_READ_API_KEY", "") if live else ""
    require(not live or token, "RENDER_READ_API_KEY is required for live inventory")
    service_ids = {plan["applications"][app]["service_id"] for app in APPS}
    workspace_id = plan["workspace_id"]
    links = group_links(workspace_id, service_ids, token) if live else {}
    observed_at = datetime.now(timezone.utc).isoformat() if live else None
    reports = []
    for app in APPS:
        plan_app = plan["applications"][app]
        service_id = plan_app["service_id"]
        if live:
            service = fetch(f"/services/{service_id}", token)
            require(isinstance(service, dict) and service.get("id") == service_id
                    and service.get("ownerId") == workspace_id
                    and service.get("branch") == "demo", "Render service identity mismatch")
            keys = direct_keys(service_id, token)
            group_ids = links[service_id]
        else:
            keys = None
            group_ids = None
        reports.append(build_review(app, plan_app, baseline[app], keys, group_ids, observed_at))
    output_dir.mkdir(parents=True, exist_ok=True)
    for report in reports:
        path = output_dir / f"demo-{report['application']}.configuration-review.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return reports


def collect_request(root: Path, request_path: Path, evidence_path: Path | None,
                    output_dir: Path, token: str, get=fetch, *, check_output=True) -> dict:
    """Create a names-only evidence file for the existing offline plan command."""
    request = release.read_json(request_path)
    release.validate_request(request)
    request_hash = release.quality.digest(request_path)
    evidence = release.read_json(evidence_path) if evidence_path else release.evidence_template(root, request, request_hash)
    release.validate_evidence(evidence, request)
    require(evidence["request_sha256"] == request_hash, "Evidence belongs to another request")
    environment = request["environment"]
    inventory = release.read_json(root / release.INVENTORY)["environments"][environment]
    workspace_id = inventory["render_workspace_id_verified"]
    targets = {app: inventory["services"][app]["render_service_id_verified"]
               for app in request["applications"]}
    require(len(set(targets.values())) == len(targets), "Duplicate Render service target")
    links = group_links(workspace_id, set(targets.values()), token, get)
    observed_at = datetime.now(timezone.utc).isoformat()
    report = {"schema_version": 1, "kind": "render_configuration_inventory",
              "environment": environment, "request_sha256": request_hash,
              "observed_at": observed_at, "applications": {}}
    updated = deepcopy(evidence)
    for app, service_id in targets.items():
        service = get(f"/services/{service_id}", token)
        expected_service = inventory["services"][app]
        require(isinstance(service, dict) and service.get("id") == service_id
                and service.get("ownerId") == workspace_id
                and service.get("branch") == release.BRANCHES[environment]
                and service.get("name") == expected_service["render_name_verified"]
                and service.get("environmentId") == expected_service["render_environment_id_verified"]
                and service.get("type") == expected_service["render_type_verified"],
                "Render service identity mismatch")
        direct = direct_keys(service_id, token, get)
        source = GitSource(root.parent / ("localeo-" + app), request["applications"][app])
        catalog = config_catalog(source, app)
        require(not catalog["blockers"], "Configuration source analysis blocked")
        expected = {row["name"] for row in catalog["keys"]}
        linked = links[service_id]
        report["applications"][app] = {
            "service_id": service_id, "candidate_sha": request["applications"][app],
            "direct_keys": direct, "linked_environment_group_ids": linked,
            "candidate_keys_absent_from_direct_service": sorted(expected - set(direct)),
            "render_keys_outside_candidate_catalog": sorted(set(direct) - expected),
            "analysis_scope": catalog["analysis"],
            "reviewed": False,
        }
        # Reading names cannot approve configuration, versions, or values.
        updated.setdefault("configuration", {})[app] = {
            "observed_at": observed_at, "service_id": service_id,
            "sha": request["applications"][app], "present_keys": direct,
            "prepared_keys": [], "not_applicable_keys": [],
            "reviewed": False, "configuration_revision_sha256": None,
        }
    release.validate_evidence(updated, request)
    if check_output:
        base = (root / ".artifacts/deploiement").resolve()
        destination = output_dir.resolve()
        require(destination.is_relative_to(base) and destination != base,
                "Output must be under .artifacts/deploiement")
        for candidate in (destination, destination / "render-configuration-inventory.json",
                          destination / "evidence.with-render-configuration.json"):
            proc = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "--", str(candidate)],
                                  capture_output=True, timeout=15)
            require(proc.returncode == 0, "Output is not ignored by Git")
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "render-configuration-inventory.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "evidence.with-render-configuration.json").write_text(
        json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--plan", type=Path, help="Review a DEMO plan against deployed code")
    source.add_argument("--request", type=Path, help="Collect Render key names for a release request")
    parser.add_argument("--deployed-shas", type=Path)
    parser.add_argument("--evidence", type=Path, help="Optional existing evidence to enrich")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--live", action="store_true", help="Read Render with RENDER_READ_API_KEY")
    args = parser.parse_args()
    try:
        if args.request:
            require(args.live and not args.deployed_shas, "Request collection requires --live")
            token = os.environ.get("RENDER_READ_API_KEY", "")
            require(bool(token), "RENDER_READ_API_KEY unavailable")
            report = collect_request(ROOT, args.request, args.evidence, args.output_dir, token)
            for app, details in report["applications"].items():
                print(f"{app}: {len(details['direct_keys'])} direct Render keys; "
                      f"{len(details['linked_environment_group_ids'])} linked groups")
            return 0
        require(args.deployed_shas is not None, "Deployed commit baseline required")
        reports = prepare(args.plan, args.deployed_shas, args.output_dir, args.live)
    except (ReviewError, ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError):
        print("Configuration review blocked; input or provider details withheld")
        return 2
    for report in reports:
        print(f"{report['application']}: +{len(report['new_in_candidate_code'])} "
              f"-{len(report['no_longer_referenced_in_candidate_catalog'])} "
              f"Render={'read' if args.live else 'unavailable'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
