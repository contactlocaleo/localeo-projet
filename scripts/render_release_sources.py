"""Read immutable, local Git sources without checking out or executing them.

No application imports, network calls, SQL connections, or private dotenv reads.
Migration behavior is supported only for the explicitly reviewed runner below.
"""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess


RUNNER_PATH = "scripts/database/apply_migrations.py"
# Reviewed at backend 46cc89042a19ec2208fec6f54d9730693567efe9.
REVIEWED_RUNNER_SHA256 = frozenset({
    "73bc0d9a6e0a54333128357d48c31d6a00c8a6ff6cbe55930eaf201d6516e697",
    "a3e5ceba65d7a9129e27aea6b84715933e31b24491643458c9d203e5cd574acd",
})
MAX_BLOB_BYTES = 16 * 1024 * 1024
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
MIGRATION_NAME = re.compile(r"v(\d+)_.*\.sql\Z")
CONFIG_KEY = re.compile(r"[A-Z][A-Z0-9_]*\Z")
PUBLIC_CONFIG_SOURCES = {
    "backend": ("app/config.py",),
    "marketplace": ("scripts/public-config.cjs",),
    "commercant": ("config/publicEnvironment.js",),
    "animation": ("buildEnvironment.ts", "pwaBuild.ts"),
}


def _normalized(content: bytes) -> bytes:
    return content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class GitSource:
    """An independent repository root and an exact full commit identifier."""

    def __init__(self, path: Path, sha: str):
        self.path = Path(path).resolve(strict=True)
        if not self.path.is_dir() or not (self.path / ".git").exists():
            raise ValueError("Source must be an independent Git repository root")
        if not isinstance(sha, str) or not HEX40.fullmatch(sha):
            raise ValueError("Source requires a complete lowercase 40-character commit SHA")
        self.sha = sha
        root = Path(self._git("rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()
        if root != self.path:
            raise ValueError("Source must be an independent Git repository root")
        if self._git("cat-file", "-t", sha).strip() != b"commit":
            raise ValueError("Source SHA must identify a commit, not a tag or tree")
        self._entries: dict[str, tuple[str, str, str, int | None]] = {}
        self._cache: dict[str, bytes] = {}
        for entry in self._git("ls-tree", "-r", "-l", "-z", "--full-tree", sha).split(b"\0"):
            if not entry:
                continue
            metadata, name = entry.split(b"\t", 1)
            mode, kind, oid, size = metadata.decode("ascii").split()
            self._entries[name.decode("utf-8", errors="strict")] = (mode, kind, oid, None if size == "-" else int(size))

    def _git(self, *args: str) -> bytes:
        # Do not inherit alternate object directories, replacement refs, injected
        # config, or credential/transport overrides from an operator environment.
        env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_TERMINAL_PROMPT="0", GIT_NO_LAZY_FETCH="1",
                   # Older Git versions ignore NO_LAZY_FETCH. Deny every
                   # transport as well, including file and external helpers.
                   GIT_ALLOW_PROTOCOL="", GIT_PROTOCOL_FROM_USER="0")
        try:
            result = subprocess.run(
                ["git", "--no-replace-objects", "-c", "core.hooksPath=" + os.devnull,
                 "-C", str(self.path), *args],
                capture_output=True, check=True, shell=False, timeout=30, env=env,
            )
        except (OSError, subprocess.SubprocessError):
            # Git stderr can contain paths or private configuration: do not emit it.
            raise ValueError("Local Git object could not be read") from None
        return result.stdout

    def paths(self) -> list[str]:
        """Tracked paths at the SHA; callers still must use read's safety checks."""
        return sorted(self._entries)

    def read(self, path: str) -> bytes:
        if not isinstance(path, str) or not path or "\\" in path or ":" in path:
            raise ValueError("Unsafe Git source path")
        parts = path.split("/")
        if any(part in ("", ".", "..") for part in parts) or PurePosixPath(path).is_absolute():
            raise ValueError("Unsafe Git source path")
        for part in parts:
            if part.lower().startswith(".env") and part != ".env.example":
                raise ValueError("Private dotenv sources must never be read")
        # foo.env.local and deploy/foo.env are private too.
        basename = parts[-1]
        if ".env" in basename.lower() and not basename.endswith(".env.example"):
            raise ValueError("Private dotenv sources must never be read")
        entry = self._entries.get(path)
        if entry is None:
            raise ValueError("Requested source is absent at the selected commit")
        mode, kind, oid, size = entry
        if mode not in ("100644", "100755") or kind != "blob":
            raise ValueError("Only regular Git blobs may be read; links and submodules are forbidden")
        if size is None or size > MAX_BLOB_BYTES:
            raise ValueError("Source blob exceeds the allowed size")
        if path not in self._cache:
            self._cache[path] = self._git("cat-file", "blob", oid)
        return self._cache[path]


def _python_config_keys(content: str) -> set[str]:
    tree = ast.parse(content)
    names: set[str] = set()
    helpers = {"_get_str", "_get_bool", "_get_https_origin", "_get_int", "_get_list",
               "_get_secret", "_get_json_object", "_cors_headers"}
    def add(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and CONFIG_KEY.fullmatch(node.value):
            names.add(node.value)
    def is_env_call(node):
        return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and (
            (node.func.attr == "getenv" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os")
            or (node.func.attr == "get" and isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "environ" and isinstance(node.func.value.value, ast.Name)
                and node.func.value.value.id == "os"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if is_env_call(node) or (isinstance(node.func, ast.Name) and node.func.id in helpers):
                if node.args:
                    add(node.args[0])
            elif isinstance(node.func, ast.Name) and node.func.id == "_env_name_with_deprecated_fallback":
                for arg in node.args[:2]:
                    add(arg)
        elif isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute):
            if node.value.attr == "environ" and isinstance(node.value.value, ast.Name) and node.value.value.id == "os":
                add(node.slice)
        elif isinstance(node, (ast.GeneratorExp, ast.ListComp, ast.SetComp)):
            # A finite os.getenv(name) for name in (...) list is static too.
            if is_env_call(node.elt) and node.elt.args and isinstance(node.elt.args[0], ast.Name):
                for generator in node.generators:
                    if (isinstance(generator.target, ast.Name) and generator.target.id == node.elt.args[0].id
                            and isinstance(generator.iter, (ast.Tuple, ast.List, ast.Set))):
                        for value in generator.iter.elts:
                            add(value)
    return names


def _javascript_config_keys(path: str, content: str) -> set[str]:
    names = set()
    # Narrow, known contracts only. Never collect arbitrary string literals or
    # default values: an uppercase default can itself be a sensitive value.
    if path == "scripts/public-config.cjs":
        match = re.search(r"\bconst\s+CONFIG_KEYS\s*=\s*\{(.*?)^\s*\};", content, re.S | re.M)
        if not match:
            raise ValueError("Known public configuration list is not recognizable")
        names.update(re.findall(r"^\s*([A-Z][A-Z0-9_]*)\s*:", match.group(1), re.M))
    elif path == "config/publicEnvironment.js":
        match = re.search(r"\bPUBLIC_ENV_KEYS\s*=\s*Object\.freeze\(\[(.*?)\]\)", content, re.S)
        if not match:
            raise ValueError("Known public configuration list is not recognizable")
        names.update(re.findall(r"['\"]([A-Z][A-Z0-9_]*)['\"]", match.group(1)))
    elif path in ("buildEnvironment.ts", "pwaBuild.ts"):
        names.update(re.findall(r"\benv\.([A-Z][A-Z0-9_]*)\b", content))
        names.update(re.findall(r"\benv\[['\"]([A-Z][A-Z0-9_]*)['\"]\]", content))
        if path == "buildEnvironment.ts":
            names.update(re.findall(r"\borigin\(['\"]([A-Z][A-Z0-9_]*)['\"]\)", content))
    return names


def config_catalog(source: GitSource, application: str) -> dict:
    """Extract names from examples and known config code, without execution."""
    selected = [path for path in source.paths() if path == ".env.example" or
                (path.startswith("deploy/") and path.count("/") == 1 and path.endswith(".env.example"))]
    keys: dict[str, set[str]] = {}
    hashes: dict[str, str] = {}
    phases: dict[str, set[str]] = {}
    blockers: list[str] = []
    for path in selected:
        try:
            content = source.read(path)
            hashes[path] = _digest(content)
            lines = content.decode("utf-8-sig").splitlines()
        except (ValueError, UnicodeError):
            blockers.append("Public configuration example cannot be read safely: " + path)
            continue
        for line_number, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=", stripped)
            if match:
                keys.setdefault(match.group(1), set()).add(path)
            else:
                blockers.append(f"Unsupported public example syntax: {path}:{line_number}")
    app = application.removeprefix("localeo-")
    code_paths = [path for path in PUBLIC_CONFIG_SOURCES.get(app, ()) if path in source.paths()]
    for path in code_paths:
        try:
            content = source.read(path)
            hashes[path] = _digest(content)
            text = content.decode("utf-8-sig")
            found = _python_config_keys(text) if path.endswith(".py") else _javascript_config_keys(path, text)
            for name in found:
                keys.setdefault(name, set()).add(path)
                phases.setdefault(name, set()).add("runtime" if app == "backend" else "build")
        except (ValueError, UnicodeError, SyntaxError):
            blockers.append("Known configuration source cannot be analyzed safely: " + path)
    if not selected and not code_paths:
        blockers.append("No supported public configuration source exists at this commit")
    return {
        "status": "blocked" if blockers else "catalogued",
        "analysis": "static_public_examples_and_known_config_code_not_exhaustive",
        "keys": [{"name": name, "sources": sorted(paths),
                  "phase": next(iter(phases[name])) if name in phases and len(phases[name]) == 1
                  else "build" if name.startswith(("VITE_", "REACT_APP_", "NEXT_PUBLIC_")) else "unknown"}
                 for name, paths in sorted(keys.items())],
        "source_hashes": hashes, "blockers": blockers,
    }


def _runner_constants(content: bytes) -> dict:
    wanted = {"BASELINE_VERSION", "EMPTY_BASELINE_NAME", "DANGEROUS_MIGRATIONS", "LEGACY_MIGRATION_CHECKSUMS"}
    result = {}
    for node in ast.parse(content.decode("utf-8")).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    result[target.id] = ast.literal_eval(node.value)
    if result.keys() != wanted:
        raise ValueError("Reviewed migration constants are missing")
    return result


def migration_plan(source: GitSource, registry: dict | None) -> dict:
    """Compare every tracked migration with a supplied registry, without SQL.

    An absent/empty registry cannot distinguish a fresh DB from a historical DB.
    It therefore always requires an operator investigation before planning.
    """
    result = {"status": "blocked", "runner_sha256": None, "files": [],
              "pending": None, "blockers": [], "excluded_registry_entries": []}
    blockers = result["blockers"]
    try:
        runner = source.read(RUNNER_PATH)
        result["runner_sha256"] = _digest(_normalized(runner))
        if result["runner_sha256"] not in REVIEWED_RUNNER_SHA256:
            blockers.append("Migration runner revision is not reviewed; planning is forbidden")
            return result
        constants = _runner_constants(runner)
    except (ValueError, SyntaxError, UnicodeError):
        blockers.append("Migration runner is absent or cannot be read safely")
        return result
    baseline = constants["EMPTY_BASELINE_NAME"]
    dangerous = constants["DANGEROUS_MIGRATIONS"]
    legacy = constants["LEGACY_MIGRATION_CHECKSUMS"]
    names = []
    for path in source.paths():
        if path.startswith("sql/") and path.count("/") == 1:
            name = path[4:]
            match = MIGRATION_NAME.fullmatch(name)
            if match or name == baseline:
                names.append((constants["BASELINE_VERSION"] if name == baseline else int(match.group(1)), name))
    if not names:
        blockers.append("No migration SQL files exist at the selected commit")
    if baseline not in {name for _, name in names}:
        blockers.append("Baseline SQL is absent")
    for version, name in sorted(names):
        try:
            raw = source.read("sql/" + name)
        except ValueError:
            blockers.append("Migration cannot be read safely: " + name)
            continue
        normalized = _normalized(raw)
        accepted = {_digest(raw), _digest(normalized), _digest(normalized.replace(b"\n", b"\r\n"))}
        accepted.update(legacy.get(name, set()))
        result["files"].append({"filename": name, "version": version,
                                "sha256": _digest(normalized),
                                "accepted_checksums": sorted(accepted),
                                "excluded": name in dangerous})
    by_name = {item["filename"]: item for item in result["files"]}
    if registry is None:
        blockers.append("Database migration registry has not been supplied")
        return result
    if (not isinstance(registry, dict) or set(registry) != {"tracking_exists", "rows"}
            or type(registry.get("tracking_exists")) is not bool or not isinstance(registry.get("rows"), list)):
        blockers.append("Migration registry shape is invalid")
        return result
    if not registry["tracking_exists"] or not registry["rows"]:
        blockers.append("Missing or empty migration tracking requires a baseline investigation")
        return result
    applied = set()
    for row in registry["rows"]:
        if (not isinstance(row, dict) or set(row) != {"filename", "checksum_sha256"}
                or not isinstance(row.get("filename"), str)
                or not isinstance(row.get("checksum_sha256"), str)
                or not HEX64.fullmatch(row["checksum_sha256"])):
            blockers.append("Migration registry row is invalid")
            continue
        name = row["filename"]
        if name in applied:
            blockers.append("Migration registry contains a duplicate filename")
            continue
        applied.add(name)
        item = by_name.get(name)
        if item is None:
            blockers.append("Migration registry contains a file absent from the selected commit")
        elif item["excluded"]:
            # The reviewed runner skips these files before validating checksums.
            result["excluded_registry_entries"].append(name)
        elif row["checksum_sha256"] not in item["accepted_checksums"]:
            blockers.append("Applied migration checksum differs: " + name)
    if blockers:
        return result
    result["pending"] = [item["filename"] for item in result["files"]
                         if item["filename"] != baseline and not item["excluded"]
                         and item["filename"] not in applied]
    result["status"] = "planned"
    return result
