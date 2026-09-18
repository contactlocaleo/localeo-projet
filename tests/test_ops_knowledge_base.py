"""Verifie les sources canoniques des procedures, formations et recettes."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OPS_DIR = ROOT / "docs" / "exploitation"
PROCEDURE_DIRS = (OPS_DIR / "technique", OPS_DIR / "exploitation")
FORMATION_DIR = ROOT / "docs" / "produit" / "formation" / "backend"
REQUIRED_SECTIONS = (
    "## Fiche réflexe",
    "## Problèmes traités",
    "## Résultat attendu",
    "## Procédure",
    "## Contrôles après action",
    "## Échec, arrêt et escalade",
)


def _procedure_files(directory: Path) -> list[Path]:
    # Preserve the former backend test scope: only documents exposed in its ERP.
    exports = json.loads((ROOT / "documentation.exports.json").read_text(encoding="utf-8"))
    prefix = Path("docs/ops") / directory.name
    return sorted(
        ROOT / entry["source_path"]
        for entry in exports["entries"]
        if Path(entry["path"]).parent == prefix
        and Path(entry["path"]).suffix == ".md"
        and Path(entry["path"]).name != "README.md"
        and not Path(entry["path"]).name.startswith("reference-")
    )


class TestBaseConnaissanceOperationnelle(unittest.TestCase):
    def test_chaque_procedure_respecte_le_plan_type(self):
        for directory in PROCEDURE_DIRS:
            self.assertTrue(directory.is_dir(), f"Repertoire absent : {directory}")
            procedures = _procedure_files(directory)
            self.assertTrue(procedures, f"Aucune procedure : {directory}")
            for procedure_path in procedures:
                with self.subTest(procedure=procedure_path.relative_to(ROOT)):
                    content = procedure_path.read_text(encoding="utf-8")
                    self.assertTrue(content.startswith("# "))
                    self.assertIn("> Statut :", content[:800])
                    for section in REQUIRED_SECTIONS:
                        self.assertIn(section, content, f"Section manquante : {section}")

    def test_catalogue_reference_toutes_les_procedures(self):
        for directory in PROCEDURE_DIRS:
            catalogue = (directory / "README.md").read_text(encoding="utf-8")
            for procedure_path in _procedure_files(directory):
                with self.subTest(procedure=procedure_path.relative_to(ROOT)):
                    self.assertIn(procedure_path.name, catalogue)

    def test_les_cahiers_de_recette_sont_isoles(self):
        recette_dir = OPS_DIR / "recette"
        for name in (
            "README.md", "cahier-recette-generale-avant-mep.md",
            "cahier-tests-backoffice.md", "recette-backoffice-preproduction.md",
        ):
            with self.subTest(document=name):
                self.assertTrue((recette_dir / name).is_file())

    def test_les_supports_de_formation_sont_isoles(self):
        for name in ("README.md", "guide-backoffice-localeo.md"):
            with self.subTest(document=name):
                self.assertTrue((FORMATION_DIR / name).is_file())

    def test_les_anciens_documents_monolithiques_ne_sont_plus_a_la_racine(self):
        obsolete = {
            "exploitation.md",
            "procedures-operationnelles.md",
            "backoffice-aide-operationnelle.md",
            "ordonnancement-batchs.md",
            "mode-secours-telephonique.md",
            "reconciliation-commandes-lots-animation.md",
        }
        self.assertFalse(obsolete.intersection(path.name for path in OPS_DIR.iterdir()))


if __name__ == "__main__":
    unittest.main()
