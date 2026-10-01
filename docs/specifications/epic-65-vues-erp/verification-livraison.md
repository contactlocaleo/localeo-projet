# EPIC 65 — Vérification et livraison prévues

Référence : [parcours](README.md), [architecture et contrats](architecture-contrats.md),
[critères du backlog](../../roadmap/a-faire/epic-65-vues-erp-audit-paiements-reversements-backlog.md).
État au 30 septembre 2026 (V1.2) : **spécification seulement**. Les tests et scénarios
ci-dessous sont prévus, pas exécutés ni déclarés réussis.

## Matrice de traçabilité

Les noms `test_epic65_*` désignent des fichiers à créer dans le backend ; les
tests existants cités ensuite sont à conserver. Cette matrice est le suivi
unique des critères, à enrichir avec commandes, résultats et limites réels.

| Critère | Comportement et propriétaire | Preuves prévues | Documentation / contrat | Démonstration | Exploitation |
| --- | --- | --- | --- | --- | --- |
| E65-CA-01 | Navigation ERP, adaptateur IHM et contrôle d’accès | Tests HTML/URL directe et navigateur des trois listes/détails, absence de redirection SQLAdmin pour consulter ; liens d’actions inchangés | README E65, `erp_ui.py`, guide back-office | ADMIN et EXPLOITATION | Livraison commune assets/API, anciennes URL conservées |
| E65-CA-02 | Projection audit, domaine exploitation | Plus de 500 événements hors filtre devant un événement pertinent ; filtres combinés en SQL, ordre à dates égales, métadonnées et chemins historiques contenant secrets/HTML/URL hostile, acteur absent/unknown/anonymous | Contrat Audit, guide support/audit | Succès/échec/phase inconnue, ressources manquantes | Index et volumétrie, aucun log de corps sensible |
| E65-CA-03 | Projection paiements et politique d’état gestion achats | Tous états bruts/normalisés, dates source, origines, racine achat/commande, deux succès ambigus, frais inconnus/connus et aucun appel Stripe | Contrat Paiements, guide finance | Paiement simple, commande multi-achats, tentatives échouées puis succès | Dépendance aux projections existantes, disponibilité visible |
| E65-CA-04 | Projection de rattachement et domaine documentaire | Achats enfants paginés, trace seule/fichier disponible/absence/lecture indisponible, demande liée ; espion sur générateur pour prouver aucun appel ; aucun faux téléchargement du reçu dans E65 ou la page de traces liée | Contrat section achats, guide finance/documents | Commande avec plusieurs achats et disponibilité documentaire différente | Droits des liens documentaires vérifiés séparément |
| E65-CA-05 | Domaine reversement et port de lecture commun | ERP/360 sur même jeu ; mouvements sans reversement, dossiers fermés hors fenêtre, état annulé, requirements_due non vide, référence manquante ; aucun double comptage | Politique de pipeline, contrat périmètre, guide finance | À préparer, en cours, transféré, échec | Corriger les écarts de lecture identifiés sans changer les commandes |
| E65-CA-06 | Payout et associations du domaine | Transfer sans association ; paid/pending/failed, rapprochement inconnu, un payout pour deux reversements, multiples tentatives et échec tardif ; montant inclus distinct du global ; associations A_ENRICHIR/legacy, devise incohérente et rattachements ambigus exclus de preuve complète | DTO virements et guide financier | Couverture bancaire complète/partielle/inconnue | Aucun nouveau Transfer/Payout ni rapprochement en GET |
| E65-CA-07 | Ports SQL et projections cohérentes | Plus de 100 objets, jointures multiples, pages extrêmes, totaux avant pagination, deux devises/devise absente, null vs zéro, lecture cohérente, changement concurrent visible | Enveloppes et sémantique des dates | Plusieurs pages, dates égales, anciennes références | `EXPLAIN` représentatif, migration d’index si justifiée |
| E65-CA-08 | Identité et accès + adaptateurs | ADMIN accepté ; anonyme, session incomplète, EXPLOITATION refusés avant repository ; contrôle HTML/JSON/documents/section directe ; aucune clé batch substituée à session | Matrice ADMIN conservée, OpenAPI futur | Profils locaux synthétiques | Pas d’élargissement implicite des préfixes middleware |
| E65-CA-09 | Orchestration et UI | Échec count/synthèse/section, session expirée, réponse tardive après filtre ou compte ; aucun zéro/état payé fabriqué ; GET répété sans mutation | Contrat d’erreur et guide de reprise | Doubles de ports en erreur, réseau simulé | Corrélation visible, consultation disponible sans Stripe |
| E65-CA-10 | Présentation ERP | Navigateur 1440/1920/390 px, clavier, focus retour, libellés, tableaux longs, chargement et détail replié | Parcours E65 et captures de recette | Libellés longs et références multiples | Validation visuelle des vues finales, pas d’acceptation par build seul |

## Tests à produire et non-régression

### Domaine et orchestration

- Politique partagée des états de paiement : conserver la normalisation de
  Vision 360, sans valeur « succès » par défaut pour un statut inconnu.
- Parité E65 / Vision 360 : une commande avec un paiement réussi direct et un
  second sur son achat enfant conserve les deux paiements et le diagnostic
  `AMBIGUOUS` ; une tentative hors période de liste reste visible dans le dossier.
  Tester la sélection SQL commune, pas uniquement le mapping d’un DTO simulé.
- Classement pur des mouvements, éligibilité Stripe via le commerçant et suivi
  bancaire via le payout. Tester les règles sans ORM ni fournisseur.
- Nouveaux tests `tests/application/exploitation/test_epic65_audit.py`,
  `tests/application/gestion_achats/test_epic65_paiements.py` et
  `tests/application/gestion_reversement/test_epic65_suivi.py` : orchestration,
  erreurs des ports, rattachements et absence d’effets. Les doubles fournissent
  des faits, sans recopier la politique métier.
- Refus d’accès testé avant toute requête aux données ; pas seulement absence
  de bouton dans la page.

### Adaptateurs et contrats

- Tests PostgreSQL sur **base jetable** : filtrage avant LIMIT, pagination et
  jointures, agrégats par devise, lecture liste/synthèse cohérente, dates UTC
  historiques et journées Paris de 23/25 heures pour Audit/Paiements.
- Campagnes février, année bissextile, fin de mois, première/seconde moitié ;
  filtres inversés/incomplets/excessifs refusés, jamais inversés silencieusement.
- Couples `campaign`/`month` incomplets ou combinés à des dates refusés ; détails
  Audit/Paiement/Reversement refusant les filtres de période, suivi d’un commerce
  conservant ces filtres ; dates nulles triées en dernier et
  achats enfants paginés par date puis UUID, y compris une racine ACHAT isolée.
- Sources des reversements : deux paiements explicitement liés au même achat
  tous deux conservés, un paiement partagé entre mouvements affiché une seule
  fois ; référence absente, références d’achat contradictoires et plusieurs
  tentatives sans lien explicite signalées incomplètes. Une tentative récente
  échouée ne remplace pas un paiement explicitement lié plus ancien. Vérifier
  aussi la console historique après extraction, sans écriture de rapprochement.
- `tests/api/test_epic65_consultations.py` à créer : schémas fermés, statuts HTTP,
  cache no-store, aucune route de mutation et sérialisation sans données brutes.
- Confronter les requêtes réelles du navigateur au contrat Pydantic exporté ;
  une requête en erreur n’est pas transformée en résultat vide dans l’UI.
- Vérifier les liens documents sur une vraie source de test ; une réponse HTTP
  réussie sur un contrat simulé ne prouve pas la bonne association aux achats.
  Une trace sans route de lecture sûre produit `TRACE_ONLY`, aucun `documentLink` ;
  une erreur produit `UNKNOWN`, jamais `NONE`. La page de traces liée ne propose
  plus le GET reçu invalide ; aucune génération n'est déclenchée pour le remplacer.
  Plus de 20 liens/diagnostics vérifient compteurs avant limite, troncature
  explicite et accès aux détails ; aucun chemin de stockage ne devient un href.
- Audit : jeton dans un segment de `path` ou dans `resourceId`, query/fragment,
  metadata imbriquée et clé inconnue ne sont pas sérialisés. Vérifier le gabarit
  reconnu ou null, les UUID/entiers admis, les booléens refusés comme compteurs,
  `metadataRedacted` distinct de `metadataTruncated` et la recherche par ID d'événement.
- Repli d'une source sans `paiement_id` : achat enfant avec paiement direct de
  commande unique ; puis ajout d'un paiement sur un autre enfant, qui rend le
  repli incomplet. Ne pas éliminer une tentative échouée ou hors période.
- Payout : deux BalanceTransactions différentes (Transfer et compte connecté)
  mais références destination/compte cohérentes sont acceptées ; comptes ou
  destinations contradictoires sont signalés. Deux tentatives du même flux ne
  doublent pas la couverture, quel que soit leur statut bancaire.
- Paramètres répétés/inconnus, page après la dernière et jeu stable à dates
  égales ; insertion entre deux pages et reprise explicite à la première.
  `generatedAt` ne sert pas de jeton d'instantané. Tester les statuts HTML
  séparément des erreurs JSON et le refus de rôle avant recherche d'un UUID.

### Dépendance de recette E35

La matrice ci-dessus valide le socle ADMIN. Pour une livraison combinée avec
`E35-PROFILS-20260928`, compléter E65-CA-01/04/08/09 par les preuves E35-PROF-11 :
lectures financières Lecteur/Backoffice/Admin, audit Admin seul, périmètres
identiques entre listes, synthèses, détails et pièces ; aucun lien vers console
technique pour les profils métier et aucune commande pour Lecteur. Révoquer ou
réduire le profil dans un autre onglet doit produire le refus dès la requête
suivante et effacer les données devenues interdites. Ces tests dépendent de la
politique et des contrats E35 ; ils ne sont ni exécutables ni réputés réussis
sur la seule base des gardes ADMIN actuels.

### Suites existantes à préserver

- `tests/security/test_erp_session_access.py` et
  `tests/integration/test_epic60_erp.py` : sessions, droits et navigation existants.
- `tests/infrastructure/admin/test_reversements_360_finance_runtime.py` :
  finance 360 après extraction, export existant et différences de lecture tracées.
- `tests/infrastructure/admin/test_backoffice_transactional_views_readonly.py`
  et `test_backoffice_audit_snapshots.py` : lecture seule et données d’audit.
- `tests/application/use_cases/test_vision_360_achats.py` : normalisation, racines,
  frais inconnus et droits techniques.
- `tests/application/services/test_audit_animation_query.py` : filtrage avant
  pagination sans modifier la projection spécialisée Animation.
- `tests/api/test_reversements_api.py`, tests payouts et use cases reversements :
  conserver le comportement des API finance, commandes et suivis commerçants.

Commandes à exécuter lors de l’implémentation, depuis le backend, avec le runner
isolé documenté ; ne pas importer l’application avec les secrets de l’opérateur :

```console
python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q
python scripts/validation/test_isolated.py tests/security/test_erp_session_access.py tests/integration/test_epic60_erp.py tests/infrastructure/admin/test_reversements_360_finance_runtime.py tests/application/use_cases/test_vision_360_achats.py -q
```

Ajouter les nouveaux fichiers de domaine/application/API et les tests PostgreSQL
appropriés une fois créés. Un skip pour base indisponible reste **non exécuté**,
jamais preuve de pagination ou de cohérence financière. Le navigateur utilise
une configuration isolée et des comptes synthétiques ; pas l’environnement réel
ni des opérations Stripe pour vérifier une consultation.

## Données de démonstration

L’EPIC ne crée pas de nouvelle donnée obligatoire : aucun changement de schéma
fonctionnel n’est prévu. Le générateur de l’EPIC 63 et son registre de tables sont
donc des lecteurs/producteurs à **vérifier**, pas à modifier automatiquement.

Scénarios minimaux : deux commerces, plusieurs périodes et devises, mouvement
non affecté, reversement constitué avec éléments hors période, tentative échouée
puis succès, paiement aux frais inconnus, commande multi-achats, pièce manquante,
payout groupé et couverture bancaire partielle, audit historique non assaini.
Les états bancaires rares sont représentés dans des fixtures de test, sans
envoyer de fonds. Examiner les jeux existants avant d’ajouter des profils ou
événements au générateur ; s’il est modifié, appliquer le workflow démonstration
et vérifier installation/restauration sur cibles jetables. Aucun accès réel ou
fichier de profils privé n’est copié dans la documentation.

## Documentation et exploitation à actualiser à la livraison

La présente spécification est la référence de conception. À l’implémentation :

- mettre à jour le [guide de formation back-office](../../produit/formation/backend/guide-backoffice-localeo.md)
  et le [guide d’exploitation back-office](../../exploitation/exploitation/reference-guide-backoffice.md)
  avec les nouvelles destinations, sens des dates et distinction Transfer/virement ;
- compléter la [recette back-office](../../exploitation/recette/recette-backoffice-preproduction.md)
  avec les scénarios E65, sans les marquer réussis avant exécution ;
- documenter les nouveaux contrats via le générateur OpenAPI backend et vérifier
  ses consommateurs ERP ; conserver le contrat publié actuel tant que le code
  ne porte pas les nouvelles routes ;
- examiner les guides finance de la console 360 pour les corrections explicites
  de lecture, sans modifier les règles Stripe ou réintroduire des paiements manuels.

Déploiement prévu dans un même backend : migration additive d’index éventuelle,
services/API, puis assets ERP compatibles. Aucun déploiement des trois frontends
n’est requis. Si assets et API coexistent temporairement en versions différentes,
une route manquante affiche « Vue indisponible », sans repli sur des données
incomplètes. Les anciens écrans restent accessibles aux ADMIN par leurs URL.
Le retour de version restaure l’ancienne navigation ; aucun état financier ni
audit n’a été transformé par cette livraison. Un éventuel index additionnel peut
rester présent selon sa migration, sans promettre un rollback destructif.

Vérifications sur une cible **explicitement autorisée** : ADMIN et EXPLOITATION,
listes/détails/document existant, totaux et filtres, absence de requête fournisseur,
droits des anciennes actions, liens entrants, pages lentes et erreurs corrélées.
Les volumes de référence doivent être mesurés avant de fixer une durée cible ;
aucun SLA ni date de livraison n’est supposé accepté.

## Résultats de la spécification initiale — 26 septembre

- Lecture des sources et analyse indépendantes des paiements/audit et reversements réalisées.
- Revue indépendante de contrat réalisée puis relue après corrections : dates et
  tris explicites, racines incomplètes, sections inconnues, portée de recherche,
  liste positive de métadonnées et distinction entre statut payout et cohérence
  des associations. Aucun constat bloquant restant sur le périmètre décrit.
- Tests applicatifs, PostgreSQL, navigateur et recette physique : **non exécutés**, car aucune implémentation n’est demandée à cette phase.
- `check_guidance.py --changed --all-markdown` avec les trois documents E65
  explicitement sélectionnés : **12 guides, 244 liens locaux, aucune erreur ni avertissement**.
- `sync_documentation.py --check-sources` : **118 documents vérifiés**.
- `git diff --check` réussi. Ces contrôles documentaires ne prouvent ni le
  comportement de l’API cible ni la couverture des scénarios de recette.
- Hypothèses H01/H02 et volumes d’exploitation : voir le README. Ils ne doivent
  pas être transformés en décisions utilisateur supposées.

## Revue de spécification V1.1 — 27 septembre

- Sources locales confrontées au backend `eec63d2` et au projet `696d487` ; aucune
  vérification d’un environnement déployé.
- Revue indépendante des contrats audit/paiements/droits effectuée. Le cas des
  paiements attachés aux achats enfants est intégré à la lecture commune et aux
  preuves prévues. Les sources de reversements multiples ou ambiguës sont
  explicites ; période du suivi commerce et détails complets restent distincts.
- Périmètre conservateur H01/H02 exploitable pour l’implémentation ; abonnements
  agrégés et nouveaux formulaires financiers restent exclus. Volumes et index
  à mesurer lors de l’implémentation, sans promesse de performance chiffrée.
- Contrôles documentaires : `check_guidance.py` avec les cinq documents modifiés
  explicitement sélectionnés, **90 guides et 924 liens locaux, aucune erreur ni
  avertissement** ; `sync_documentation.py --check-sources`, **118 documents** ;
  `git diff --check` réussi.
- Aucun code applicatif modifié ; tests métier, PostgreSQL et navigateur
  **non exécutés**. L’état produit reste **À faire**.

## Revue de spécification V1.2 — 30 septembre

- Sources locales relues sur backend `3252c72` et projet `484f10d`, puis
  modifications documentaires locales E65. La modification préexistante du
  suivi des environnements de démonstration est hors périmètre et préservée.
- Revue indépendante paiements/reversements et relecture des corrections :
  traces documentaires distinctes des fichiers, candidats sources communs à
  la Vision 360, transactions Stripe plateforme/compte connecté distinguées,
  diagnostics et liens bornés. Constats intégrés au contrat et aux preuves prévues.
- Contrôles de session/droits et sources audit relus ; garde ADMIN conservé,
  dépendance E35 explicite, chemins d'audit avec jetons occultés, pagination
  et statuts HTTP précisés. Les identifiants CA-01 à CA-10 sont conservés.
- Préparation : socle ADMIN exploitable pour H01/H02. L'ouverture E35 attend sa
  politique, ses périmètres/masquages et ses preuves ; agrégation d'abonnements
  et nouveaux formulaires financiers restent hors périmètre sans complément.
  Plans SQL, index et volumes restent à mesurer à l'implémentation.
- Aucun code applicatif ni OpenAPI publié modifié ; aucun test métier,
  PostgreSQL ou navigateur exécuté. Aucun commit, push ou déploiement.
  L'état produit reste **À faire**.
- Contrôles documentaires réussis : `scripts/check_guidance.py`, avec les six
  documents E65/backlog/index/roadmap modifiés explicitement sélectionnés :
  **91 guides, 982 liens locaux, 0 erreur, 0 avertissement** ;
  `scripts/sync_documentation.py --check-sources` : **118 documents vérifiés** ;
  `git diff --check` réussi. L'interpréteur configuré par `localeo.python` a
  été utilisé après constat que `python` n'était pas accessible dans le PATH
  du bac à sable. Ces contrôles ne prouvent pas les comportements cibles.
