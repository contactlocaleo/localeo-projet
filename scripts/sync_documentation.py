"""Prepare un bundle de deploiement, sans copies documentaires versionnees dans le backend."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORTS_NAME = "documentation.exports.json"
SNAPSHOT_NAME = "documentation.snapshot.json"


class SyncError(ValueError):
    """La synchronisation risquerait de perdre des modifications ou de sortir du perimetre."""


def _is_link(path: Path) -> bool:
    return path.is_symlink() or getattr(path, "is_junction", lambda: False)()


def _root(path: Path) -> Path:
    path = Path(path)
    if _is_link(path) or not path.is_dir():
        raise SyncError(f"Racine absente ou lien interdit: {path}")
    return path.resolve()


def _parts(value: object, *, destination: bool = False) -> list[str]:
    if not isinstance(value, str) or not value or any(c in value for c in ("\\", ":", "\x00")):
        raise SyncError(f"Chemin relatif POSIX requis: {value!r}")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise SyncError(f"Chemin relatif sans traversee requis: {value!r}")
    if destination and (len(parts) < 3 or parts[:2] not in [["docs", "ops"], ["docs", "juridique"], ["output", "pdf"]]):
        raise SyncError(f"Identifiant hors de docs/ops, docs/juridique ou output/pdf: {value}")
    return parts


def _path(root: Path, relative: str, *, destination: bool = False, required: bool = False) -> Path:
    candidate = root
    for part in _parts(relative, destination=destination):
        candidate = candidate / part
        if _is_link(candidate):
            raise SyncError(f"Lien symbolique ou jonction interdit: {candidate}")
    if not candidate.resolve().is_relative_to(root):
        raise SyncError(f"Chemin hors de sa racine: {candidate}")
    if candidate.exists() and not candidate.is_file():
        raise SyncError(f"Fichier regulier attendu: {candidate}")
    if required and not candidate.is_file():
        raise SyncError(f"Fichier absent: {candidate}")
    return candidate


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hash(value: object) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise SyncError("Empreinte SHA-256 invalide dans le manifeste existant")
    return value


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise SyncError(f"schema_version doit etre l'entier 1: {path}")
    entries = value.get("entries")
    if not isinstance(entries, list) or not entries:
        raise SyncError(f"entries doit contenir au moins un document: {path}")
    return value


def _entries(manifest: dict, *, snapshot: bool = False) -> list[dict]:
    if snapshot and manifest.get("source_repository") != "localeo-projet":
        raise SyncError("source_repository doit etre localeo-projet")
    seen_paths, seen_sources = set(), set()
    for entry in manifest["entries"]:
        if not isinstance(entry, dict):
            raise SyncError("Chaque entree doit etre un objet")
        _parts(entry.get("path"), destination=not snapshot)
        _parts(entry.get("source_path"))
        for value, seen, label in (
            (entry["path"], seen_paths, "destination"),
            (entry["source_path"], seen_sources, "source"),
        ):
            identity = value.casefold()
            if identity in seen:
                raise SyncError(f"Doublon de {label}: {value}")
            seen.add(identity)
        if snapshot:
            _hash(entry.get("sha256"))
            _hash(entry.get("source_sha256"))
    return manifest["entries"]


def _atomic_write(path: Path, content: bytes) -> None:
    if path.is_file() and path.read_bytes() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix="." + path.name + ".", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _bundle_root(path: Path) -> Path:
    """Accepte une destination nouvelle, mais jamais un lien dans ses parents."""
    path = Path(os.path.abspath(path))
    for parent in [path, *path.parents]:
        if _is_link(parent):
            raise SyncError(f"Lien symbolique ou jonction interdit: {parent}")
    if path.exists() and not path.is_dir():
        raise SyncError(f"Repertoire attendu: {path}")
    return path.resolve()


def source_entries(source_root: Path) -> list[dict]:
    """Valide les sources autorisees avant une livraison ou en CI documentaire."""
    source_root = _root(source_root)
    exports = _entries(_load(_path(source_root, EXPORTS_NAME, required=True)))
    for entry in exports:
        parts = _parts(entry["source_path"])
        if parts[0] not in {"docs", "livrables"} or len(parts) < 2:
            raise SyncError(f"Source hors documentation: {entry['source_path']}")
        _path(source_root, entry["source_path"], required=True)
    return exports


def build_bundle(source_root: Path, bundle_root: Path, *, check: bool = False) -> int:
    """Copie les sources sans les transformer, avec manifeste et empreintes."""
    source_root, bundle_root = _root(source_root), _bundle_root(bundle_root)
    if bundle_root == source_root or source_root.is_relative_to(bundle_root):
        raise SyncError("Le bundle doit etre distinct du depot source et de ses parents")
    exports = source_entries(source_root)
    paths = [entry["source_path"] for entry in exports] + [EXPORTS_NAME]
    manifest_path = _path(bundle_root, SNAPSHOT_NAME)
    previous = _entries(_load(manifest_path), snapshot=True) if manifest_path.exists() else []
    old_by_path = {entry["path"].casefold(): entry for entry in previous}
    removed = set(old_by_path) - {path.casefold() for path in paths}
    if removed:
        raise SyncError("Retrait d'export interdit; preparer un nouveau bundle: " + ", ".join(sorted(removed)))
    if check and not manifest_path.exists():
        raise SyncError("Manifeste absent; verification impossible avant initialisation")
    writes, entries = [], []
    # Valider tout le plan avant la premiere ecriture ; conserver les edits locaux.
    for relative in paths:
        source = _path(source_root, relative, required=True)
        destination = _path(bundle_root, relative)
        previous_entry = old_by_path.get(relative.casefold())
        if previous_entry is not None:
            if not destination.is_file() or _sha(destination.read_bytes()) != previous_entry["sha256"]:
                raise SyncError(f"Copie modifiee localement ou absente; aucune ecriture: {relative}")
        elif destination.exists():
            raise SyncError(f"Copie existante sans entree dans le manifeste; aucune ecriture: {relative}")
        content = source.read_bytes()
        digest = _sha(content)
        entries.append({"path": relative, "source_path": relative,
                        "sha256": digest, "source_sha256": digest})
        writes.append((destination, content))
    snapshot = {"schema_version": 1, "source_repository": "localeo-projet", "entries": entries}
    if check:
        normalized = [{key: entry[key] for key in ("path", "source_path", "sha256", "source_sha256")} for entry in previous]
        if normalized != entries:
            raise SyncError("Sources ou rendus modifies; preparer le bundle avant livraison")
        return len(exports)
    for destination, content in writes:
        _atomic_write(destination, content)
    _atomic_write(manifest_path, (json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return len(exports)


def sync_documentation(source_root: Path, backend_root: Path, *, check: bool = False) -> int:
    """Compatibilite CLI : bundle genere et ignore sous .runtime/documentation."""
    return build_bundle(source_root, _root(backend_root) / ".runtime/documentation", check=check)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Verifie un bundle deja prepare, sans ecriture")
    mode.add_argument("--check-sources", action="store_true", help="Verifie seulement les sources et l'allowlist")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--backend", type=Path, default=PROJECT_ROOT.parent / "localeo-backend")
    destination.add_argument("--output", type=Path, help="Destination explicite du bundle de deploiement")
    args = parser.parse_args(argv)
    try:
        if args.check_sources:
            count = len(source_entries(PROJECT_ROOT))
        elif args.output is not None:
            count = build_bundle(PROJECT_ROOT, args.output, check=args.check)
        else:
            count = sync_documentation(PROJECT_ROOT, args.backend, check=args.check)
    except (SyncError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Synchronisation refusee: {exc}", file=sys.stderr)
        return 1
    verified = args.check or args.check_sources
    print(f"{count} documents {'verifies' if verified else 'prepares dans le bundle'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
