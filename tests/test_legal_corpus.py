"""Verifie l'inventaire juridique canonique sans dependance applicative."""

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "docs" / "juridique"


class LegalCorpusTests(unittest.TestCase):
    def test_manifeste_reel_sources_sha_versions_et_exclusions(self):
        catalogue = json.loads((ROOT / "publication" / "catalogue.json").read_bytes())
        self.assertEqual(len(catalogue["documents"]), 12)
        self.assertEqual(len(catalogue["excluded_documents"]), 4)
        for entry in catalogue["documents"] + catalogue["excluded_documents"]:
            with self.subTest(document=entry["source"]):
                content = (ROOT / entry["source"]).read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), entry["pdf_sha256"])
        self.assertEqual(
            {entry["id"] for entry in catalogue["documents"] if entry["version"] == "1.1"},
            {"confidentialite", "cgv-marketplace", "conditions-animation"},
        )
        self.assertTrue(all(
            entry["source"].startswith("interne/") and entry["reason"] == "internal"
            for entry in catalogue["excluded_documents"]
        ))


if __name__ == "__main__":
    unittest.main()
