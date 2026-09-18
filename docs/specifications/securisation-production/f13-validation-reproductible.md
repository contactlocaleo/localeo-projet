# F13 - Validation reproductible

`requirements.in` contient les dependances directes. `requirements.txt` est le
graphe resolu avec versions exactes et hashes, produit avec pip-tools 7.6.1 :

```bash
python -m piptools compile --generate-hashes --allow-unsafe --strip-extras --resolver=backtracking --output-file=requirements.txt requirements.in
python -m pip install --require-hashes -r requirements.txt
python -m pip check
python scripts/validation/test_isolated.py -q
```

La CI execute la suite sous Python 3.12 et 3.14, sans fichiers .env, base externe
ni reseau sortant. Les donnees de configuration sont synthetiques. Les tests
de contrats HTTP injectent leurs dependances SQL ; les quotas ont leurs propres
tests. Les actions GitHub sont referencees par SHA. Les jobs de detection de
secrets, pip-audit et Bandit restent obligatoires avant promotion.

Un job PostgreSQL 16 jetable verifie la concurrence du quota, la reprise Checkout
et la serialisation des migrations. Les images PostgreSQL et Gitleaks sont figees
par digest. Localement ces trois tests passent sur l'instance PostgreSQL 11
jetable disponible ; cette version n'est pas recommandee pour la production.

Les tests locaux ne remplacent pas une recette derriere le proxy, la validation
sur la version PostgreSQL cible ni un test de restauration de sauvegarde.
Le graphe installe (67 distributions) ne presente aucune vulnerabilite connue
selon pip-audit 2.10.1 au 5 septembre 2026, apres correction de pytest,
python-dotenv et pip. Ce resultat est date et doit etre reconfirme en CI.
