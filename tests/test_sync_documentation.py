"""Tests autonomes du distributeur de documentation (bibliotheque standard)."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_documentation.py"
SPEC = importlib.util.spec_from_file_location("sync_documentation", SCRIPT)
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class DocumentationSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.source = self.workspace / "localeo-projet"
        self.backend = self.workspace / "localeo-backend"
        self.source.mkdir()
        self.backend.mkdir()
        self.guide = self.source / "docs/exploitation/guide.md"
        self.legal = self.source / "docs/juridique/legal.pdf"
        self.guide.parent.mkdir(parents=True)
        self.legal.parent.mkdir(parents=True)
        self.guide.write_bytes(b"# Guide\n")
        self.legal.write_bytes(b"%PDF-1.7\n\x00\xff\n")
        self.entries = [
            {"source_path": "docs/exploitation/guide.md", "path": "docs/ops/guide.md"},
            {"source_path": "docs/juridique/legal.pdf", "path": "docs/juridique/legal.pdf"},
        ]
        self.bundle = self.backend / ".runtime/documentation"
        self.manifest = self.bundle / "documentation.snapshot.json"
        self.export_path = self.source / "documentation.exports.json"
        self.write_exports()

    def write_exports(self, **overrides):
        payload = {"schema_version": 1, "entries": self.entries, **overrides}
        self.export_path.write_text(json.dumps(payload), encoding="utf-8")

    def run_sync(self, **options):
        return sync.sync_documentation(self.source, self.backend, **options)

    def test_bootstrap_only_creates_missing_targets_and_is_idempotent(self):
        self.assertEqual(2, self.run_sync())
        target = self.bundle / "docs/exploitation/guide.md"
        original = {path: (path.read_bytes(), path.stat().st_mtime_ns)
                    for path in [target, self.manifest, self.bundle / "docs/juridique/legal.pdf"]}
        self.assertEqual(2, self.run_sync())
        self.assertEqual(2, self.run_sync(check=True))
        for path, state in original.items():
            self.assertEqual(state, (path.read_bytes(), path.stat().st_mtime_ns))
        self.assertEqual(self.legal.read_bytes(), (self.bundle / "docs/juridique/legal.pdf").read_bytes())

    def test_missing_manifest_refuses_existing_copy_even_with_identical_bytes(self):
        target = self.bundle / "docs/exploitation/guide.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(self.guide.read_bytes())
        with self.assertRaisesRegex(sync.SyncError, "sans entree"):
            self.run_sync()
        self.assertFalse(self.manifest.exists())
        self.assertFalse((self.bundle / "docs/juridique").exists())

    def test_check_never_bootstraps_or_writes(self):
        with self.assertRaisesRegex(sync.SyncError, "Manifeste absent"):
            self.run_sync(check=True)
        self.assertEqual([], list(self.backend.iterdir()))

    def test_validates_all_entries_before_touching_any_target(self):
        self.run_sync()
        guide_target = self.bundle / "docs/exploitation/guide.md"
        old_guide = guide_target.read_bytes()
        old_manifest = self.manifest.read_bytes()
        self.guide.write_bytes(b"New canonical guide")
        local_pdf = self.bundle / "docs/juridique/legal.pdf"
        local_pdf.write_bytes(b"Local uncommitted edit")
        with self.assertRaisesRegex(sync.SyncError, "modifiee localement"):
            self.run_sync()
        self.assertEqual(old_guide, guide_target.read_bytes())
        self.assertEqual(old_manifest, self.manifest.read_bytes())
        self.assertEqual(b"Local uncommitted edit", local_pdf.read_bytes())

    def test_check_reports_source_change_without_writing_then_sync_updates_it(self):
        self.run_sync()
        target = self.bundle / "docs/exploitation/guide.md"
        before = target.read_bytes()
        self.guide.write_bytes(b"# New source\n")
        with self.assertRaisesRegex(sync.SyncError, "Sources ou rendus modifies"):
            self.run_sync(check=True)
        self.assertEqual(before, target.read_bytes())
        self.run_sync()
        self.assertEqual(self.guide.read_bytes(), target.read_bytes())
        self.assertEqual(2, self.run_sync(check=True))

    def test_removed_entry_is_refused_and_no_copy_is_deleted(self):
        self.run_sync()
        self.entries.pop()
        self.write_exports()
        previous = self.manifest.read_bytes()
        with self.assertRaisesRegex(sync.SyncError, "Retrait d'export interdit"):
            self.run_sync()
        self.assertTrue((self.bundle / "docs/juridique/legal.pdf").exists())
        self.assertEqual(previous, self.manifest.read_bytes())

    def test_missing_managed_target_is_treated_as_a_local_change(self):
        self.run_sync()
        target = self.bundle / "docs/exploitation/guide.md"
        target.unlink()
        with self.assertRaisesRegex(sync.SyncError, "modifiee localement ou absente"):
            self.run_sync()
        self.assertFalse(target.exists())

    def test_relative_paths_and_scopes_are_validated_before_writing(self):
        for field, value in [
            ("path", "../escape.md"),
            ("path", "/absolute.md"),
            ("path", "C:/absolute.md"),
            ("path", "docs/ops/../escape.md"),
            ("path", "docs\\ops\\guide.md"),
            ("path", "output/private/guide.pdf"),
            ("path", "docs/architecture/guide.md"),
            ("source_path", "../escape.md"),
        ]:
            with self.subTest(field=field, value=value):
                entries = [dict(entry) for entry in self.entries]
                entries[-1][field] = value
                self.write_exports(entries=entries)
                with self.assertRaises(sync.SyncError):
                    self.run_sync()
                self.assertEqual([], list(self.backend.iterdir()))

    def test_rejects_duplicate_destination_or_source(self):
        for field in ("path", "source_path"):
            with self.subTest(field=field):
                entries = [dict(entry) for entry in self.entries]
                entries[-1][field] = entries[0][field]
                self.write_exports(entries=entries)
                with self.assertRaisesRegex(sync.SyncError, "Doublon"):
                    self.run_sync()
                self.assertEqual([], list(self.backend.iterdir()))

    def test_rejects_bad_schema_before_writing(self):
        for version in (None, True, "1", 2):
            with self.subTest(version=version):
                self.write_exports(schema_version=version)
                with self.assertRaisesRegex(sync.SyncError, "schema_version"):
                    self.run_sync()
        self.assertEqual([], list(self.backend.iterdir()))

    def test_bundle_preserves_canonical_paths_links_and_bytes(self):
        content = b'# Guide\n[PDF](../juridique/legal.pdf?download=1#page=2)\n'
        self.guide.write_bytes(content)
        self.run_sync()
        self.assertEqual(content, (self.bundle / "docs/exploitation/guide.md").read_bytes())
        self.assertEqual(self.export_path.read_bytes(), (self.bundle / sync.EXPORTS_NAME).read_bytes())
        entries = json.loads(self.manifest.read_bytes())["entries"]
        self.assertEqual(3, len(entries))
        for entry in entries:
            self.assertEqual(entry["path"], entry["source_path"])
            self.assertEqual(entry["sha256"], entry["source_sha256"])
        self.assertFalse((self.backend / "docs").exists())

    def test_manifest_tampering_refused_before_any_write(self):
        self.run_sync()
        (self.bundle / sync.EXPORTS_NAME).write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(sync.SyncError, "modifiee localement"):
            self.run_sync()

    def test_check_sources_and_explicit_output_do_not_need_backend(self):
        standalone = self.workspace / "deployment/documentation"
        with mock.patch.object(sync, "PROJECT_ROOT", self.source):
            self.assertEqual(0, sync.main(["--check-sources"]))
            self.assertEqual([], list(self.backend.iterdir()))
            self.assertEqual(0, sync.main(["--output", str(standalone)]))
            self.assertEqual(0, sync.main(["--output", str(standalone), "--check"]))
        self.assertTrue((standalone / "docs/exploitation/guide.md").is_file())

    def test_symlink_source_refused_if_platform_allows_its_creation(self):
        external = self.workspace / "outside.md"
        external.write_bytes(self.guide.read_bytes())
        self.guide.unlink()
        try:
            self.guide.symlink_to(external)
        except (OSError, NotImplementedError):
            self.skipTest("Creation de symlinks interdite sur cette plateforme")
        with self.assertRaisesRegex(sync.SyncError, "Lien symbolique"):
            self.run_sync()
        self.assertEqual([], list(self.backend.iterdir()))

    def test_junction_or_symlink_in_destination_parent_is_refused(self):
        original = sync._is_link
        blocked = self.backend / ".runtime"
        with mock.patch.object(sync, "_is_link", side_effect=lambda path: path == blocked or original(path)):
            with self.assertRaisesRegex(sync.SyncError, "Lien symbolique ou jonction"):
                self.run_sync()
        self.assertEqual([], list(self.backend.iterdir()))

    def test_cli_has_check_and_backend_options_and_failure_status(self):
        with mock.patch.object(sync, "PROJECT_ROOT", self.source):
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(1, sync.main(["--backend", str(self.backend), "--check"]))
            self.assertIn("Manifeste absent", stderr.getvalue())
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(0, sync.main(["--backend", str(self.backend)]))
                self.assertEqual(0, sync.main(["--backend", str(self.backend), "--check"]))
            self.assertIn("2 documents verifies", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
