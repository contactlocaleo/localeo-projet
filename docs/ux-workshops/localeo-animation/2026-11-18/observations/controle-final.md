# Contrôle final — étape 1

Contrôles exécutés le 18 novembre 2026, vers 11 h 42–11 h 44, Europe/Paris. Aucun test applicatif ni build lancé pour cette exploration documentaire sans modification de code.

| Contrôle | Résultat |
| --- | --- |
| `py -3 scripts/check_guidance.py` | Succès : 106 guides, 1 483 liens locaux, zéro erreur et zéro avertissement après création du présent rapport. |
| `py -3 scripts/sync_documentation.py --check-sources` | Succès : 151 documents vérifiés. |
| Liens propres à cette exécution | 169 cibles locales vérifiées avant ajout du lien de manifeste ; aucune absente. Contrôle final de toutes les cibles effectué après finalisation. |
| PNG | 63 fichiers ouverts et vérifiés par Pillow ; aucune image corrompue. Dimensions bureau/mobile cohérentes. |
| Revue visuelle ciblée | Bureau, import mobile, assistant passeport, tirage, détail marchand masqué et confirmation de clôture inspectés visuellement ; tous les écrans ont également été lus par leur contenu DOM pendant la navigation. Pas de recette exhaustive d’accessibilité. |
| Secrets dans les documents | Lecture UTF-8 des Markdown/JSON et recherche d’adresses email, marqueurs de compte, jetons Bearer/JWT : zéro correspondance. Prompt de connexion expurgé ; aucun fichier d’authentification créé. Captures de connexion prises avant saisie ; coordonnées masquées sur les vues concernées. Pas d’OCR exhaustif des images. |
| Instructions des étapes suivantes | Emplacements 00 et 02–05 présents, absence de prompt spécifique explicitement signalée. Aucun prompt historique inventé. |
| Étapes non autorisées | Dossiers workshop, maquettes après, validation et synthèse vides. Aucune simulation, maquette ou validation anticipée. |
| Dépôts applicatifs | `git status --porcelain` vide dans Animation, backend, commerçant et marketplace au contrôle final. Aucun code applicatif modifié. |
| Dépôt documentaire | `git status --short` signale `?? docs/ux-workshops/`, déjà présent avant cette exécution. Les nouvelles écritures de ce travail sont limitées à `localeo-animation/2026-11-18/`. Aucun commit/push. |
| Archive Pro précédente | 107 empreintes du manifeste précédent comparées : zéro différence. Aucune écriture effectuée dans les archives Pro ou Live. Pas de nouvelle empreinte de référence antérieure disponible pour Live dans cette étape. |

Le premier passage de `check_guidance.py` avait signalé le lien vers ce rapport encore absent ; le fichier a été créé et le contrôle relancé avec succès. Il ne s’agissait pas d’une anomalie applicative.

## Intégrité et provenance

Le [manifeste SHA-256](manifest-sha256.json) couvre les fichiers de cette exécution sauf lui-même. Il est généré après la finalisation des documents et captures. Les captures et observations sont des preuves de cette visite, pas des tests de non-régression ni une certification de l’application.

**État final : exploration terminée avec limites ; workshop complet non réalisé.** Communication en erreur, publication et actions sensibles non exécutées, test humain de la promesse 5–10 minutes restant à faire. Attente d’autorisation pour l’étape 2.
