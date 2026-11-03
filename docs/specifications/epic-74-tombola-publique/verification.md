# E74 — Preuves attendues et recette

Version du 3 novembre 2026. [Périmètre](README.md), [contrats et invariants](architecture-contrats.md), [critères canoniques](../../roadmap/en-cours/epic-74-tombola-publique-backlog.md).

## Bilan d'implémentation locale

Les tests ci-dessous ont été exécutés sur les changements locaux, sans activation du TEST partagé et sans envoi d'e-mail réel. Bases Git : projet `e6bddec`, backend `3437cfc`, Animation `e275bd5`, marketplace/Live `4dbc897`, Pro `054feab`. L'epic reste **En cours** : les scénarios complémentaires indiqués ci-dessous ne sont pas réputés validés par un build ou par une recette navigateur à API simulée.

Les preuves PostgreSQL utilisent une instance locale jetable, port 55474, une base de recette et des schémas uniques par fixture. Les e-mails sont capturés dans l'outbox. Le backend est toujours exécuté par `scripts/validation/test_isolated.py`.

## Matrice des 16 critères

U = unitaire ; I = intégration application/API/PostgreSQL ; F = navigateur. Les parcours F actuels simulent les réponses API ; ils ne constituent pas à eux seuls le scénario intégral avec backend et transport e-mail réels.

| Critère | Preuves exécutées | Compléments de recette à distinguer |
| --- | --- | --- |
| E74-CA-01 | U registre à quatre moteurs, modèle public et capacité standard ; F sélection du modèle dans Animation. | Catalogue activé uniquement dans les fixtures ; aucune activation distante. |
| E74-CA-02 | I publication PostgreSQL sans commerce, rejeu d'une publication, un seul appel quota ; suites existantes des droits/quota. | La recette du générateur complète ce test par un vrai abonnement, les droits acquis et le contrôle d’un débit unique après rejeu. |
| E74-CA-03 | U compilation/règles sans commerce ; I publication normale, snapshot marchand vide, refus sans lots et sans débit. | Recette PostgreSQL sur migrations complètes : création, modification, publication, flyer et quota réel réussis pour une commune sans commerce (lots externes). |
| E74-CA-04 | U assistant et sections non applicables ; I pages/compteurs hors commune refusés ; F assistant et navigation. | Pas de preuve nouvelle de toutes les combinaisons de rôles E73. |
| E74-CA-05 | F accès direct au formulaire, aucun secret personnel dans le lien public ; ouverture du lien de confirmation sans POST. | Scan d'un QR imprimé avec caméra physique non exécuté ; pas requis pour prouver le traitement de l'URL. |
| E74-CA-06 | U flyer public contextualisé et quantités ; F flyer sans étapes commerçantes. | Rendu PDF final des trois modes non rejoué dans cette campagne. |
| E74-CA-07 | U preuve/identité minimale ; I attente puis confirmation, outbox atomique, ancien endpoint refusé ; F confirmation explicite et entrée dans Live. | Chaîne de services réels e-mail → gel → tirage externe → accès → remise réussie ; le navigateur est vérifié séparément. |
| E74-CA-08 | I demandes/confirmations concurrentes, rejeu, secret étranger, clé réutilisée, accès révoqué, renvoi/remplacement, récupération ; F reprise. | Les succès rejoués ne prolongent ni preuve ni accès. |
| E74-CA-09 | U fenêtre/date/règlement ; I expiration, fermeture, confirmation bloquée par clôture, gel revalidant les preuves. | Trois courses supplémentaires passent : expiration à 31 min, fermeture à 61 min, demande retardée de 2 h ; aucun accès ni preuve tardifs. |
| E74-CA-10 | F participation et suivi de commune séparés ; inscription ne crée aucun consentement de communication. | Aucun canal de communication inter-animations ajouté. |
| E74-CA-11 | F suivi facultatif, réutilisation de Mes communes et stockage local ; régressions Live. | Pas de nouveau compte habitant ni de synchronisation inventée entre appareils. |
| E74-CA-12 | I pages bornées, portée du curseur, totaux/compteurs, attentes non comptées publiquement, export minimal ; gel de 10 000 preuves réelles. | Mémoire globale du processus non profilée ; provenance minimale du gel encore O(N). |
| E74-CA-13 | I trois modes après gel avec identité minimale, zéro/insuffisance/exact/suppléants ; U stratégies existantes réutilisées. | 22 tests PostgreSQL couvrent les trois modes, populations 0/1/2/5, insuffisance Coffrets, suppléants et rejeu. |
| E74-CA-14 | I notification, accès et projection Live du bon numérique ; confirmation externe distincte de la remise ; régressions Pro. | Remise externe, consommation du bon et reprises testées ; financement/activation Coffrets simulés à la frontière de distribution, tirage et stockage réels. |
| E74-CA-15 | I secret/rejeu/révocation, limitation durable et 429, isolation des pages ; F mobile/clavier ; capacité N/10N au débit nominal. | Rafale simultanée de 50 : p95 ~2 s, dépasse le budget nominal ; voir mesures et limites. |
| E74-CA-16 | I migration complète/rejeu/restauration, états attente/preuve/outbox rejouables ; U/I négociation anciens lecteurs ; F régressions trois moteurs. | Générateur : entrée locale explicite complète vérifiée, séparée du build historique ; dotation externe.  Huit échecs de régression reproduits sur la base inchangée. |

Revue indépendante : le défaut d’horloge capturée avant verrou a été corrigé et sa correction relue ; le coût mémoire de la provenance du gel reste explicitement O(N). Les objets ORM de provenance sont désormais évités lors de l’insertion par lots.

## Résultats et commandes reproductibles

Les logs mentionnés sont des sorties locales ignorées par Git dans `localeo-backend/tmp/`. Ils ne contiennent aucun accès de production. Les tests constituent la preuve versionnable ; les chiffres sont ceux de cette exécution, sans extrapolation à Render.

| Contrôle | Résultat | Preuve locale |
| --- | --- | --- |
| Intégration E74 : e-mail, publication, gains, transport, démonstration | **113 réussites** | `e74-integration-final.log` ; fichiers `tests/security/test_tombola_publique_*.py`, `tests/api/test_tombola_publique_email.py`, suites démonstration ciblées |
| Contrat HTTP de pagination sur PostgreSQL | **1 réussite** | `e74-http-pages.log` : borne 100, curseur invalide, `next_cursor: null`, aucun total implicite, autre commune refusée |
| Adaptateurs conservation/capacités et compteurs historiques après correction du filtre vide | **28 réussites** | `e74-adaptateurs-corriges.log` ; `test_conservation_moteur_api_t6.py`, `test_capacites_lecture_live_e74.py`, `test_compteurs_lectures_v283.py` |
| Chaîne SQL complète jusqu'à v288, rejeu et restauration pg_dump/pg_restore | **1 réussite** | `e74-migration-finale.log`, `test_tombola_publique_migration_complete.py` ; modèle installé inactif |
| Régression large backend | **1 560 réussites, 8 échecs, 7 ignorés** | `e74-regression-finale.log` ; les ignorés ne sont pas des réussites |
| Reproduction des huit échecs sur backend inchangé `3437cfc` | **8 mêmes échecs, 28 réussites** | `e74-baseline-failures.log`, worktree détaché local |
| Courses d’horloge, exports et e-mail E74 | **26 réussites** | `e74-course-horloge.log` ; tests des verrous, instantané export et compteurs sans hydratation |
| Refus abonnement et paramètres publics | **5 réussites**, vrai contrat de droit | `e74-refus-droits.log` ; absence d’abonnement ne provoque plus de 500, fermeture publique sans commerce |
| Démonstration locale complète | **11 tests unitaires et 1 test PostgreSQL réussis** | `test_demo_tombola_publique_locale_postgres.py`, migrations complètes, PDF local, droits et quota réels |
| Conservation et borne e-mail finale | **28 réussites** | `e74-purge-borne-finale.log` : maintenance limitée à 500 même lorsque le batch principal reçoit 1 000 |
| Validation finale groupée gains/e-mail/droits | **53 réussites** | `e74-validation-finale.log`, après optimisation des insertions du gel |
| Contrôles finaux architecture/application | **642 réussites** | `e74-derniers-controles.log` ; inclut refus de validation commerçante d’une participation publique |
| Architecture + intégration e-mail/export | **656 réussites** | `e74-exports-architecture.log` |
| Gains, trois modes et tailles de population | **22 réussites** | `.artifacts/e74-gains-complement.log`, `test_tombola_publique_gains.py` |
| Parcours réel après publication jusqu’à remise | **1 réussite** | `.artifacts/e74-parcours-complet.log`, `test_tombola_publique_parcours_postgres.py` |
| Capacités lecteurs catalogue/Live/global/jeu | **74 réussites** | `.artifacts/e74-live-readers-tests.log` |
| Animation | **299 tests Node réussis**, typage/lint/build réussis ; navigateur 320/390/1280 px réussi | `localeo-animation/tmp/e74-tests-final.log`, `tests/browser/public-tombola.mjs` ; avertissement de taille de bundle conservé |
| Live | **154 tests sécurité réussis**, **12 tests navigateur E74** et **19 régressions navigateur** réussis ; lint ciblé/build réussis | `localeo-marketplace/tmp/e74-security-final.log`, `tests/visual/e74-tombola-email.spec.cjs` |
| ERP/Support | Scénario participants réussi aux largeurs 320/1280, clavier/zoom ; régression suivi produits réussie | `tests/browser/epic74-participants-erp.cjs` |
| Pro | **36 tests ciblés réussis** | Réutilisation du bon numérique, sans nouveau flux d'inscription commerçante |

Ces suites se recouvrent : ne pas additionner leurs totaux comme un nombre de tests uniques. Le lint global marketplace rencontre une erreur de permission dans des sorties locales préexistantes (`output`/`tmp`) ; le lint des sources modifiées passe.

Les huit échecs backend de base concernent un libellé accentué du catalogue et des fixtures historiques incomplètes (réversibilité, mise à jour versionnée, verrou de commande lots). Ils ont été reproduits sur le commit initial, sans modification ni skip pour les rendre verts.

### Capacité mesurée

`tests/performance/test_e74_capacite_locale.py` : **2 tests réussis**, N=1 000 puis 10 000, 50 clients, arrivées limitées au débit spécifié de 20 commandes/s. À 10 000 : page p95 11,94 ms, total 14,92 ms, demande p95 39,51 ms / p99 54,02 ms, confirmation p95 35,70 ms / p99 37,46 ms. Plan `Index Only Scan`, 26 lignes et deux requêtes par page. Log `e74-capacite-nominale.log`.

`tests/performance/test_e74_gel_local.py` : **1 réussite**, gel de 10 000 participants en **5,88 s**, 141 requêtes, lecture et insertion par lots de 500, aucun objet ORM de membre/provenance accumulé ; log `e74-gel-membres-bornes.log`. La même exécution compte **17 tests réussis** avec les régressions de clôture, publication et le parcours e-mail → remise.

La réduction mémoire a d’abord fait dépasser le budget du gel (10,06 à 16,96 s selon le mode d’insertion). Le profilage a conduit à des insertions SQL groupées avec compilation réutilisable pour les membres et la provenance ; le dernier résultat ci-dessus passe le budget de 10 s sans modifier son assertion.

Deux essais de rafale instantanée de 50 commandes ont dépassé le budget nominal (p95 ~2,0–2,3 s ; logs `e74-capacite.log`, `e74-capacite-v2.log`). Le scénario nominal ne représente pas cette rafale. La fixture de capacité exécute v288 sur le schéma ciblé ; les mesures ne prouvent ni les ressources de l'hébergement cible ni la charge cumulée de tous les triggers historiques. Mesure RSS, endurance et charge mixte avec tirage/outbox restent à produire.

Exemple de relance locale, depuis le backend, avec une base jetable déjà préparée :

```powershell
& 'C:/Users/casta/AppData/Local/Python/bin/python.exe' scripts/validation/test_isolated.py --postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55474/localeo_audit_test tests/security/test_tombola_publique_postgres.py -q -s --tb=short
```

La migration complète utilise une seconde base vide réservée `localeo_audit_migrations_test` ; son test refuse une base contenant des données initiales.

## Plan de couverture de référence (spécification)

Dans le backend, suivre le runner isolé décrit par son `AGENTS.md`. La recette ne dépend d'aucun compte réel, base TEST partagée, fournisseur e-mail ou validation de pilote.

| Dépôt | Fichiers/scénarios ciblés |
| --- | --- |
| Backend — nouveaux | `tests/domain/animation_locale/test_tombola_publique.py` : compilation, identité, qualification et refus ; `tests/application/services/test_tombola_publique_email.py` : transactions/outbox/reçus ; `tests/api/test_tombola_publique_email.py` : contrats et anti-contournement ; `tests/security/test_tombola_publique_postgres.py` : contraintes, gel et concurrence. |
| Backend — existants | `tests/domain/animation_locale/test_tombola_locale.py`, `test_politique_participation_publication.py` ; `tests/application/services/test_participants_animation.py` ; `tests/api/test_localeo_live_animations_inscription.py` ; `tests/security/test_publication_classique_t4.py`, `test_exploitation_moteur_postgres.py`, `test_tirages_libres_postgres.py`, `test_tirages_numeriques_postgres.py`. |
| Animation | Tests existants `animation-engine-registry.test.mjs`, `assistant-presentation.test.mjs`, `assistant-navigation.test.mjs`, `publication-http-contracts.test.mjs`, `flyer-http-contracts.test.mjs` ; nouveau scénario navigateur `e74-tombola-publique` couvrant création → publication → QR → participants → tirage/remise. |
| Marketplace/Live | Tests registre, installation, jeu, communes ; scénarios existants `live-registration-clarity.spec.cjs`, `live-game.spec.cjs`, `live-lots-unified.spec.cjs`, `live-habitant-communes.spec.cjs`, `organizer-messages.spec.cjs` ; nouveau `e74-tombola-email.spec.cjs`. |
| Commerçant/Pro | Remise de bon numérique E74, refus d'une qualification par scan/PIN et non-régression des validations commerçantes des autres modèles. Pas de nouveau flux d'inscription Pro à tester. |
| Projet / contrats | Liens de documentation, exports depuis producteurs, empreintes schémas et contrats embarqués ; ces contrôles accompagnent les tests consommateurs et ne les remplacent pas. |

## Parcours fonctionnels complets

1. **Sans commerce, bout en bout** : organisation de test sans commerce → standard → lots externes → assistant → publication → flyer/QR → prénom/e-mail/règlement → attente sans chance → e-mail capturé localement → ouverture sans mutation → confirmation explicite → une chance → clôture → tirage confirmé → lot visible dans Live → remise par organisateur. Vérifier toutes les identités et versions entre écrans et base.
2. **Reprise et autre appareil** : demander sur A, ouvrir sur B sans installation connue, confirmer, perdre la réponse puis rejouer même commande ; un participant/une preuve/une chance et un accès valable. Reprendre ensuite sur A par e-mail. Aucun état local n'accorde l'éligibilité.
3. **Secret et prévisualisation** : GET, robot de messagerie et préchargement n'écrivent rien ; secret étranger, expiré, révoqué ou remplacé refusés ; nouvelle clé sur secret consommé sans nouvelle mutation. L'ancien endpoint et la récupération ne donnent pas d'accès en attente. Révocation bloque le reçu de succès.
4. **Clôture en course** : deux transactions réelles PostgreSQL, barrière synchronisée ; inclure une confirmation commise avant gel ou refuser celle passée après. Aucun qualifié absent de la population par course ; aucun lien tardif ne l'étend. Rejouer après arrêt worker.
5. **Trois modes, population insuffisante** : lots externes et numériques avec zéro/un/plusieurs candidats ; Coffrets refuse si exemplaires supérieurs aux candidats, sans émission partielle ni modification de dotation. Nombre exact et cas suffisant vérifiés également.
6. **Mobile et préférences** : 320/390 px et PC, clavier/zoom, commandes accessibles, liens retour et rafraîchissement cohérents ; suivi commune refusé puis ajouté/retiré, notifications refusées, stockage indisponible, limite dix. Participation et lots restent utilisables dans chaque cas.
7. **Compatibilité** : anciennes tombolas/passeports/chasses avant et après migration, ancienne PWA face au catalogue/direct E74, cache et mise à jour ; aucun type inconnu envoyé à un lecteur qui ne le comprend pas sans réponse explicite de mise à jour.
8. **Volumétrie et exploitation** : N/10N selon budgets d'architecture, charge mixte lectures/confirmations/gel, plusieurs habitants sur même IP ; total exact, plans/index, bornes mémoire, délais, saturation explicite. Restaurer une sauvegarde isolée contenant attentes, preuves, outbox et gains, puis reprendre sans doublon.

### Cas limites de récupération et de rejeu (CA08/09/15)

- Après fermeture, appeler les deux routes de récupération pour une adresse absente, en attente et confirmée : même 202 public ; aucune création, preuve ni nouvelle chance ; seul le confirmé encore autorisé reçoit un accès par l'outbox. Tester également la limite `date_fin + 90 jours`, l'anonymisation et les délais de renvoi.
- Confirmer avant expiration, perdre la réponse, puis rejouer la même commande après les 30 minutes du challenge et après fermeture, avant les 24 heures du reçu : même succès autorisé, sans prolongation d'accès ni mutation de population. Une première confirmation avec un challenge expiré reste refusée.
- Rejouer avec secret incorrect, autre animation, autre corps ou clé, reçu expiré, accès révoqué ou participant anonymisé : aucun accès restitué. Vérifier que la recherche d'un reçu ne contourne pas les contrôles d'autorisation courants.

## Documentation et données à livrer avec le code

- Compléter les guides Animation/ERP avec le parcours sans commerce et l'avertissement Coffrets ; le guide Live avec vérification, récupération et suivi local ; le support stand avec QR/lien et confirmation d'adresse.
- Actualiser les sources de règlement/notice selon les finalités et durées réellement appliquées, sans affirmer une validation juridique obtenue. Leur revue de mise en service reste distincte des tests de clôture.
- Régénérer les contrats depuis le backend, puis mettre à jour les manifestes/schémas embarqués et vérifier empreintes et tests de chaque lecteur.
- Adapter le générateur backend et ses assertions aux états de preuve ; aucun accès réel ou donnée privée dans les fixtures. Vérifier suppression/anonymisation/restauration, pas seulement création des tables.
- Documenter activation, fermeture d'urgence, limitation de débit, échecs d'e-mail, reprise outbox, purge et retour vers l'avant. Décrire les variables effectivement introduites lors du développement avec exemples sans secret ; aucune variable hypothétique à configurer aujourd'hui.

## Bilan de préparation

Les choix produit sont fixés et les responsabilités, contrats cibles, limites existantes et preuves sont identifiés. Les travaux peuvent être implémentés par lots : domaine/données et contrats → consommateurs et UX → intégration/recette/capacité → activation. Le nouveau parcours d'e-mail et la pagination réellement bornée sont du développement requis.

La clôture technique nécessite les preuves pertinentes réussies pour les 16 critères. Une vérification locale ne vaut pas déploiement ; une action pilote ou une preuve externe n'est pas une condition ajoutée à la clôture. Les preuves locales acquises figurent en tête de ce document. Aucune activation distante n'a été effectuée ; les compléments de tests restent visibles dans la matrice.

## Historique — contrôles de spécification avant implémentation

- Exploration en lecture des producteurs backend et des consommateurs Animation/Live, puis revue indépendante `localeo-contract-reviewer` des trois documents. Les trois écarts relevés (négociation des clients historiques, contrat de pagination, affichage des dates) ont été corrigés et leur résolution confirmée en seconde lecture. Aucun reste concret dans ces points ; cela ne vaut pas test d'implémentation.
- Dépôt documentaire, base `7b3d5e5` et modifications locales E74 : `python scripts/check_guidance.py` avec `--document` pour les trois fichiers de ce dossier, le backlog E74, la roadmap et l'index. Résultat : **99 guides, 1 158 liens locaux, zéro erreur, zéro avertissement**.
- Aucun contrat généré ni entrée de `documentation.exports.json` modifié dans cette phase ; pas de lecteur applicatif à exécuter pour un changement d'export. Les tests domaine/intégration/navigateur, migrations, charge et génération de démonstration restent **non exécutés**.

### Reprise de spécification du 3 novembre 2026

- Base documentaire `e6bddec`, backend `3437cfc` ; les choix produit et les 16 critères restent inchangés. Précisions apportées sur la récupération après fermeture et la reprise d'un succès au-delà du délai initial du challenge, avec leurs scénarios de refus.
- Nouvelle revue en lecture seule par `localeo-contract-reviewer` des contrats, producteurs et consommateurs ; relecture des précisions : aucun écart bloquant restant identifié dans ce périmètre. La récupération historique jusqu'à `date_fin + 90 jours` a été vérifiée dans le service et l'entité participant.
- Contrôles locaux : `check_guidance.py` sur les six documents E74/index/roadmap, **99 guides, 1 158 liens, zéro erreur et avertissement** ; `sync_documentation.py --check-sources`, **134 documents vérifiés** ; `git diff --check` réussi. Python utilisé par chemin explicite, l'alias système étant indisponible.
- Seul le dépôt documentaire est modifié. Aucun code, contrat généré, migration, test métier, envoi ou déploiement réalisé. Le périmètre est prêt à implémenter ; l'état produit reste **À faire**.


## Contrôles documentaires et contrats après implémentation

- `check_guidance.py` incluant les six documents E74 : **100 guides, 1 107 liens, zéro erreur et avertissement**.
- `sync_documentation.py --check-sources` : **134 sources vérifiées**.
- Export moteur avec `--check` : **98 fichiers conformes** dans Animation et dans Live ; les OpenAPI E41/E42 proviennent du producteur local, et le contrat embarqué Animation correspond à E41.
- `git diff --check` : réussi dans les cinq dépôts. Pro reste inchangé.
- Aucun commit, push, activation de modèle, migration distante ni envoi réel effectué. Les quatre dépôts modifiés restent indépendants.
