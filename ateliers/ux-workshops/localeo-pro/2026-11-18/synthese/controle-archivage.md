# Contrôle final d’archivage

**Trace historique :** ce contrôle décrit l'état à 11:10, avant la réponse utilisateur du 18 novembre. Les cinq orientations ont ensuite été [validées](../validation/decisions.md) pour E80. Le manifeste courant a été régénéré ; sa version initiale est conservée séparément.

18 novembre 2026. **Archivage documentaire terminé ; workshop global PARTIEL.** La décision utilisateur reste absente sur les cinq P1 et les tests terrain ne sont pas exécutés. Aucun succès métier supplémentaire n’est revendiqué.

## Inventaire des livrables demandés

| Élément | État à l’archivage | Référence |
| --- | --- | --- |
| Observations factuelles | Présentes, O01–O09 et C01–C06 qualifiés, preuves reliées | [Observations](../observations/observations-factuelles.md) |
| Cartographie et écrans | Présents ; parcours atteints et limites distingués | [Parcours](../observations/cartographie-parcours.md), [écrans](../observations/inventaire-ecrans.md) |
| Captures réelles | 22 PNG AVANT, décodables, conservés | [Index](../visuels/captures-avant/README.md) |
| Rapports | Rapport exécutif et compte rendu présents | [Rapport](../workshop/rapport-executif.md), [séance simulée](../workshop/compte-rendu.md) |
| Votes nominatifs | 14 orientations × 12 votants uniques = 168 votes, arguments présents ; 7 adoptions et 7 rejets | [Votes](../workshop/votes-et-arbitrages.md) |
| Backlog | Sept orientations adoptées, critères et références de conception présents | [Backlog UX](../workshop/backlog-ux.md) |
| Orientations rejetées | Sept fiches présentes ; les rejets ne valent pas refus utilisateur | [Rejets simulés](../workshop/orientations-rejetees.md) |
| Quick wins | Quatre lots proposés, non réalisés | [Quick wins](../workshop/quick-wins.md) |
| Maquettes | 18 états × 2 formats = 36 PNG, sources isolées et index présents | [Index APRÈS](../visuels/maquettes-apres/README.md) |
| Galerie HTML | Présente, commandes contrôlées ; aucune requête distante pendant le contrôle | [Galerie](../visuels/comparatif-avant-apres.html) |
| Revue et arbitrages | Présents ; réactions simulées et limites des revues sur transcription explicites | [Revue](../visuels/revue-contradictoire.md), [arbitrages](../visuels/arbitrages-maquettes.md) |
| Décisions utilisateur | Registre présent, **cinq décisions manquantes / EN ATTENTE** | [Décisions](../validation/decisions.md), [synthèse](decisions-ux.md) |
| Roadmap UX | Absente au début de l’étape 5, créée ; horizon P0/P1 validées vide | [Roadmap conditionnelle](roadmap-ux.md) |
| Plan commerçants | Absent au début de l’étape 5, créé ; huit scénarios, cinq à sept personnes à recruter dont au moins deux peu familières du numérique | [Plan non exécuté](plan-tests-commercants.md) |
| Comparaison historique | Non applicable : aucun précédent Pro ; situation et baseline documentées | [Comparaison](comparaison-precedent.md) |
| Prompts 00–05 | Présents et complets pour les instructions utilisateur connues ; particularité du 01 explicitée | [Provenance](../prompts/provenance-et-versions.md) |
| Relance autonome | Présente, version 1.0, non exécutée | [Prompt de relance](../prompts/RELANCER-WORKSHOP.md) |

## Contrôles d’intégrité

- Fichiers textuels UTF-8 lisibles et aucun fichier vide ; chemins relatifs contrôlés sur les liens Markdown, références HTML et ressources CSS.
- **62 PNG décodés intégralement avec Pillow** : 22 captures réelles, 36 maquettes et 4 captures de contrôle de la galerie. Vérification de structure puis chargement des pixels ; aucune image endommagée détectée. Cela ne prouve pas l’exactitude fonctionnelle d’un écran.
- Galerie contrôlée à nouveau avec Chromium/Playwright : bascules mobile, activation clavier, côte à côte ordinateur, chargement des 36 variantes APRÈS, accordéon du prototype et bouton de démonstration. Aucun appel réseau HTTP(S), aucune erreur JavaScript.
- Quatorze groupes de douze votes uniques avec argument, seuil fixe de sept ; contrôles structurés dans le rapport JSON. Les décomptes n’ajoutent aucune validation utilisateur.
- Six instructions 00–05 contrôlées : sections numérotées complètes ; 02 identique octet par octet à la pièce jointe fournie. 01 enrichi avec l’instruction globale connue et sa version initiale préservée. Aucun prompt interne indisponible n’est inventé.
- Recherche de motifs d’identifiants de connexion et de jetons dans les textes : aucun motif détecté. Les captures de connexion avaient été prises avec champs vides ; aucun nouvel accès authentifié ni capture d’identifiants à l’étape 5. Ce contrôle ne prétend pas être un audit exhaustif de sécurité.
- Préservation par SHA-256 des **100 fichiers des autres workshops présents** avant et après cette étape. Un seul dossier Pro recensé. Aucun workshop antérieur ou voisin édité.
- Les quatre dépôts applicatifs gardent leur commit et leur statut propre entre début et fin d’archivage. Aucun code applicatif modifié. Le dépôt documentaire reste sur `main`, au commit `7164846f266cc0c073dc0c4642c569d9b8c6676c` ; aucun commit, push ou déploiement effectué.
- `py -3 scripts/check_guidance.py` : succès, 105 guides, 1 471 liens locaux, aucune erreur ni avertissement. `py -3 scripts/sync_documentation.py --check-sources` : succès, 151 documents. Ces contrôles concernent la documentation, pas le métier ni les utilisateurs.

Résultats détaillés : [intégrité des fichiers, votes et dépôts](controle-integrite.json), [galerie à l’archivage](controle-galerie-archivage.json), [empreintes à l'archivage initial](manifest-sha256-archivage-initial.json) et [manifeste courant](manifest-sha256.json). Les horodatages exacts et nombres de liens contrôlés figurent dans les rapports. Les scripts temporaires de contrôle ne sont pas intégrés au dépôt applicatif ou documentaire.

## Empreintes et rejeu du contrôle

Le manifeste couvre les octets de tous les fichiers de cette exécution **sauf le manifeste lui-même**, pour éviter une auto-référence. Chaque entrée contient un chemin relatif, une taille et une empreinte SHA-256. Il ne constitue pas une signature externe ni une preuve de contenu métier. Après toute décision ou modification ultérieure, le manifeste devra être régénéré en traçant la mise à jour, sans effacer la version soumise précédemment.

Pour vérifier une copie de l’archive, lire le JSON, calculer SHA-256 des octets de chaque chemin relatif depuis la racine du dossier, comparer taille et empreinte, puis comparer l’ensemble des chemins pour détecter aussi les fichiers ajoutés ou supprimés. Refuser tout chemin sortant du dossier. Les tests du produit et la comparaison des états métier restent séparés.

## Anomalies et limites finales

1. **Validation non reçue** : B1/C1/D1/E1/F1 restent EN ATTENTE. Aucune catégorie VALIDÉE/REFUSÉE/À RÉVISER/REPORTÉE ne contient de décision utilisateur.
2. **Recette incomplète** : QR valide, reçu/doublon/incertitude, caméra physique, expiration et retour différé, PDF/impression, accessibilité réelle et compréhension terrain non vérifiés. Le plan de tests est futur.
3. **Provenance du prompt 01** : il contenait initialement un résumé opérationnel. L’instruction utilisateur réellement appliquée est disponible et a été ajoutée ; aucun second prompt utilisateur distinct n’est connu. Les commandes et prompts internes ne sont pas tous disponibles verbatim.
4. **Métadonnées modèle limitées** : Codex et la famille GPT-6 sont indiqués par le contexte ; révision exacte et niveaux de raisonnement non exposés. Aucun modèle précis ni réglage n’est inventé pour les agents.
5. **Historique absent** : pas de comparaison quantitative avec une exécution Pro antérieure ; aucune correction prouvée ni évolution de note annoncée.

Les mentions « aucune maquette » des livrables de l’étape 2 décrivent leur état lors de cette étape. Les sections plus récentes du README et les liens de conception portent l’état final ; les traces historiques ne sont pas réécrites comme si les maquettes avaient existé dès l’origine.
