# Localeo Atelier — Vérification et livraison

[Spécification V1](README.md) · [Architecture](architecture.md) · [Contrats](contrats.md)

## État des preuves

L'implémentation locale du **29 septembre 2026** couvre le parcours ERP, le contrat
JSON/WebP, la création en brouillon, les lecteurs Marketplace et la conservation.
Les preuves réellement exécutées sont récapitulées dans le bilan ci-dessous ;
la matrice décrit les scénarios de référence et ne transforme pas un scénario
non exécuté en succès. Aucune IA, paiement, base de production, de test ou de démo
n'a été sollicité. Les tests PostgreSQL utilisent une instance locale jetable.
L'epic reste **En cours**, sans clôture de recette ni déploiement implicite.

## Matrice de traçabilité

| Critère | Propriétaire et comportement | Scénarios de référence ; résultats ci-dessous | Documentation / contrat | Démonstration et fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| E66-CA-01 | Identité/accès + application : commune et commandes autorisées | Tests API de liste/détail/ID direct, session absente, commune hors portée, rejeu après retrait de droits ; future lecture seule EPIC 35 | Contrats d'accès et guide opérateur | ADMIN, EXPLOITATION A, compte B sans accès | Vérifier rôle et périmètre en recette ; aucune élévation pour ouvrir Atelier |
| E66-CA-02 | Commercialisation : modèles éligibles et sélection exacte | Domaine : statuts, doublon, commune, Stripe bloqué, modèle/version absent, libellés identiques et budget ; adaptateur pagination filtrée | Contrat candidats et aide sélection | Deux commerces A, commerce B exclu, modèles actifs/inactifs | Index et bornage des listes ; aucune réutilisation d'un candidat non autorisé |
| E66-CA-03 | Application de prompt + domaine contexte | Liste blanche réelle exportée, absence contacts/finance/secrets, dépassement sans troncature, même clé/même contexte, gabarit compatible avec JSON Schema | Template versionné, schéma et guide copier/coller | Textes fictifs avec URLs/contact, intention et 20 références | Pas de clé fournisseur, pas de logs de prompt |
| E66-CA-04 | Proposition éditoriale et projection ERP | Import valide, aperçu complet, zéro coffret avant confirmation, texte simple échappé ; schéma/exemple validés | Contrat court et mapping éditorial | Réponse fictive nominale | Distinguer aperçu et publication dans la recette |
| E66-CA-05 | Domaine de réponse + parseur | JSON malformé, clés dupliquées, champ interdit, autre contexte/commune, version inconnue, omission/ajout/doublon modèle, borne UTF-8/profondeur ; préparation inchangée | Catalogue d'erreurs françaises | Réponses négatives dérivées de l'exemple | Diagnostic par code et corrélation, jamais body brut |
| E66-CA-06 | Politique média + adaptateur DAM | WebP valide 149 999 octets accepté, 150 000/150 001 refusés ; PNG renommé, faux RIFF, image illisible/animée/hors bornes ; mêmes contrôles upload/DAM/création ; quota et retry sans doublon | Contrat média, aperçu/alt et guide WebP | Petits assets synthétiques conformes et invalides | Limites locales Atelier, quota global conservé ; pas de conversion implicite |
| E66-CA-07 | Préparation + coffret + copies | UoW intégration PostgreSQL : un coffret, N copies BROUILLON, N snapshots v1, liens modèle/version exacts, ordre et version finale ; aucun envoi/publication | Transition et transaction, champs canoniques | Composition nominale 2 modèles, économie distincte | Migration additive puis backend ; ouverture seulement avec lecteurs prêts |
| E66-CA-08 | Résultat durable + registre idempotent | Deux threads/deux acteurs/deux clés, après 24 h, perte réseau, même clé body différent ; erreur forcée au Nᵉ rattachement, commit échoué, source concurrente ; rollback total ou même résultat | Protocole de reprise et erreurs 409 | Préparation déjà créée, coffret supprimé après succès | Trace terminale conservée malgré purge ; aucune recréation sur retry |
| E66-CA-09 | Domaine contexte/source | Modifier modèle/texte/statut/commune/prix/éligibilité entre prompt, import et création ; refuser ou sérialiser correctement, aucune course validation/écriture | Empreinte, verrous et régénération | Version obsolète et commerce devenu bloqué | Un conflit invite à régénérer, pas à forcer une ancienne version |
| E66-CA-10 | Règles ERP/BUM existantes | Diagnostic et refus de publication identiques ; images et description ne valent pas qualification ; parcours normal d'activation/publication après création | Guide finalisation et séparation textes éditoriaux/contractuels | Brouillon incomplet BUM, puis coffret finalisé dans fixture | Aucun contournement financier, fiscal ou d'activation ; pas de paiement réel |
| E66-CA-11 | Préparation persistée + droits actuels + expiration | Rechargement autorisé, refus après retrait de droits, concurrence de retouche, échéance de 30 jours ; résultat durable après nettoyage | Contrat versions/reprise/expiration, documentation conservation | Préparations avant/à/après échéance, créée et non créée, médias partagés | Nettoyage borné/idempotent ; sauvegarde/restauration conserve unicité et échéance |
| E66-CA-12 | ERP et Marketplace | Navigateur desktop/mobile/clavier, focus erreurs, messages français, loading/double clic, presse-papiers indisponible ; après publication accroche/description/alt/ordre visibles, repli des anciens coffrets | Guides et contrats consommateurs | Image absente, longue description, données anciennes | Recette de chaque application touchée ; résultat local distinct du déployé |

Précision V1.1, **E66-CA-03 à 06 et 08** : vérifier le parcours réel à un seul
collage JSON contenant l'image, sans upload complémentaire ; fixture d'image
décodée, base64 tronqué/invalide/non canonique, mauvais MIME, PNG encodé, champs
visuels manquants, bornes du texte UTF-8 et du fichier décodé. Vérifier notamment
149 999 octets acceptés et 150 000 refusés après décodage, tous deux encodables en
200 000 caractères ; 150 001 octets donnent 200 004 caractères, refusés dès la
limite de longueur. Un refus quota/image/contexte ou une panne au commit ne laisse aucune
proposition partielle ni asset orphelin. Même clé/retry ou même checksum autorisé
dans la préparation ne duplique pas le média. GET/résultat/audit ne renvoient pas
le base64. Une image issue d'un ancien contexte ne confirme pas une nouvelle réponse.

L'exemple JSON contient désormais un **vrai WebP 2 × 2 de 66 octets** (carré ocre),
fixture de transport uniquement, pas une illustration commerciale du coffret.
Sa conformité structurelle et son décodage ne prouvent pas la génération par une IA.

Conservation validée **E66-D05 / E66-CA-11** : tester avec horloge contrôlée la
reprise juste avant 30 jours, le refus à l'échéance exacte et après ; lecture,
rejeu et mutation échouée ne prolongent pas la durée, modification réussie oui.
Tester une expiration avant le passage du batch, puis `dry_run`, nettoyage répété,
panne/reprise et concurrence sauvegarde/création/nettoyage. Préserver les coffrets,
prestations, achats, médias partagés et marqueurs d'unicité ; vérifier le retrait
des textes/contextes/images de travail orphelines et l'absence de recréation après
purge. Un snapshot restauré conserve ses échéances passées, sans redémarrer 30 jours.

## Suites et couches de vérification

- Domaine pur : préparation, proposition, transitions, sélection, contexte, budget,
  statuts initiaux et unicité logique. Aucun ORM, FastAPI ou fournisseur dans les tests.
- Application : ports réels représentés par doubles sans recopie des règles,
  droits, transaction, erreur au milieu de l'assemblage, audits et absence d'effets externes.
- Persistance PostgreSQL isolée : verrous inter-acteurs, contraintes, commit,
  rollback, migration depuis schéma courant et résultat après 24 h. SQLite ou un
  fake ne prouve pas la sérialisation nécessaire.
- API : schéma fermé, limites UTF-8, CSRF, authentification, idempotence, refus hors
  commune, accès au DAM et projection d'erreurs. Relier l'exemple et les fixtures
  à `reponse-ia.schema.json` avec contrôle des formats UUID activé.
- Contrats publics/consommateurs : sérialisation des nouveaux champs optionnels,
  tolérance aux champs absents/nulls, formulaires historiques préservant les champs
  non soumis, ordre, snapshots d'achats inchangés et lecteurs stricts compatibles.
- Navigateur : parcours ERP complet puis rendu Marketplace sur données isolées,
  sans IA connectée. Vérifier les données effectivement copiées et envoyées, pas
  seulement les libellés ou boutons.

Réutiliser les tests backend existants
[ERP intégré](../../../../localeo-backend/tests/integration/test_epic60_erp.py),
[sessions ERP](../../../../localeo-backend/tests/security/test_erp_session_access.py),
[upload ERP](../../../../localeo-backend/tests/security/test_erp_image_upload.py)
et [quotas DAM](../../../../localeo-backend/tests/security/test_dam_upload_controls.py)
en ajoutant des suites dédiées aux comportements ci-dessus. Exécuter via le runner
isolé du backend ; lancer les contrôles d'architecture pour les nouvelles couches,
puis les suites ciblées, sans affaiblir les assertions existantes. Les scripts
exécutables et générateurs restent dans le dépôt applicatif.

## Démonstration, migrations et exploitation

Le générateur doit pouvoir produire une commune avec deux commerces et plusieurs
modèles, une autre commune interdite, une préparation sans image, un aperçu validé
et une création terminée. Générer des réponses fictives, sans réseau IA. Inclure les
versions de modèles, références DAM et liens d'origine dans l'export/restauration.
Un schéma générique d'export ne dispense pas d'un round-trip vérifié sur base jetable.
Ne pas régénérer les environnements test/démo à l'occasion de la seule implémentation.

Ordre proposé de livraison :

1. Ajouter migration, entités/ports et contrôles readiness des nouvelles structures.
   Aucun remplissage artificiel d'anciens textes ni changement de statuts existants.
2. Livrer les contrats backend/ERP et les contrôles serveur, tout en maintenant
   Atelier fermé aux opérateurs tant que la recette n'est pas complète. Le mécanisme
   d'ouverture existant doit contrôler routes et navigation ensemble ; s'il n'en
   existe pas, prévoir un contrôle de livraison désactivé par défaut.
3. Adapter les consommateurs Marketplace et vérifier les interfaces partagées.
   Les champs nullables permettent de livrer les lecteurs avant toute création IA.
4. Réaliser la recette isolée et déployée, relever SHAs, version de migration,
   résultats et réserves, puis ouvrir l'entrée Atelier pour le périmètre autorisé.
5. Contrôler après ouverture le diagnostic du premier brouillon, les permissions,
   les erreurs françaises, les médias et l'absence de publication automatique.

Aucune nouvelle clé IA ni tâche de génération n'est requise. Limites et état du
module doivent être consultables par l'exploitation sans exposer le contenu des
préparations. Auditer imports acceptés/refusés et créations avec identifiants/codes,
sans texte ni identifiants personnels dans le prompt. Intégrer le nettoyage
quotidien à 30 jours à l'ordonnanceur existant, avec simulation, métriques de retard
et recette des protections ; aucune exécution réelle dans cette phase. Une restauration doit préserver les
marqueurs terminaux pour ne pas autoriser une deuxième création.

Reprise : fermer l'entrée et les commandes Atelier en cas d'incident, conserver
les brouillons déjà créés et leurs données. Un rollback applicatif peut tolérer les
colonnes supplémentaires mais ne doit pas passer par un ancien formulaire qui
efface les nouveaux contenus ; vérifier cette compatibilité avant l'ouverture.
Pas de suppression automatique de colonnes, médias ou coffrets pour revenir en arrière.

## Contrôles de cette phase documentaire

Résultats du **29 septembre 2026**, dépôt Projet sur base `3ddc144` avec les
modifications documentaires locales, backend lu à `9b9cba3` et Marketplace à `0aa5e77` :

- `check_guidance.py` avec le backlog et les quatre documents du dossier :
  **91 guides, 916 liens locaux, 0 erreur, 0 avertissement**.
- `sync_documentation.py --check-sources` : **118 documents vérifiés**.
- Validateur `jsonschema` 4.26.0, Draft 2020-12 avec vérification des UUID : schéma
  valide, exemple accepté, **11 cas structurels invalides refusés** (version,
  UUID, bornes de texte, sélection vide, champ interdit, URL visuelle, version de
  modèle nulle/booléenne et doublon exact). Dépendance installée uniquement dans
  un dossier temporaire backend, sans modification des dépendances applicatives.
- `git diff --check` : réussi.
- Revue indépendante des contrats : commune obligatoire, retouches/alt et
  pagination précisés ; garde avant rejeu rendu explicite. Seconde lecture :
  aucune contradiction bloquante relevée dans ce périmètre documentaire.

Ces résultats ne sont pas une recette métier. Le schéma ne prouve pas la fraîcheur
des sources, les droits, les transactions, le décodage des médias ou les rendus.
Seuls les fichiers versionnés de `localeo-projet` sont modifiés par cette phase ;
migrations, générateurs, applications et données restent à implémenter dans leurs
dépôts respectifs. H01 est remplacée par D04 (JSON avec image base64) et H02 par
D05 (conservation de 30 jours, validée). Les résultats ci-dessus décrivent la revue initiale ;
la précision V1.1 sur le média intégré a fait l'objet des contrôles complémentaires
suivants le 29 septembre : mêmes 91 guides/916 liens sans erreur ; schéma révisé
valide, exemple accepté, WebP réellement décodé (66 octets, 2 × 2) et **16 cas
structurels invalides refusés**. La revue indépendante a fait préciser les états
autorisant le remplacement d'image et les bornes base64/décodage. Les validations
applicatives de transaction, quota et contexte restent à implémenter/exécuter.

## Bilan d'implémentation locale — 29 septembre 2026

Arbres de travail non commités : backend sur `9b9cba3`, Marketplace sur `0aa5e77`,
Projet sur `3ddc144`. Les modifications documentaires antérieures des EPIC 35, 65
et 67 sont conservées. Aucun changement dans les applications Commerçant et Animation :
leurs consommateurs tolèrent les champs éditoriaux additifs et leurs contrats moteur
ne sont pas modifiés.

| Critères | Preuves exécutées et sources |
| --- | --- |
| CA-01, CA-03, CA-05, CA-08 | [Tests HTTP](../../../../localeo-backend/tests/api/test_atelier_assiste.py) et [HTTP PostgreSQL réel](../../../../localeo-backend/tests/integration/test_atelier_http_postgres.py) : auth, CSRF/Origin, droits avant rejeu, expiration, clé réutilisée avec autre corps, même contexte/version/échéance au retry, refus après retrait de commune, activation désactivée. |
| CA-02 à CA-06, CA-09 | [Domaine](../../../../localeo-backend/tests/domain/test_preparation_coffret_assiste_dedicated.py), [admission JSON/WebP](../../../../localeo-backend/tests/infrastructure/test_reponse_atelier.py), [application](../../../../localeo-backend/tests/application/test_atelier_assiste.py) : JSON fermé, Unicode, octets réels, format/dimensions, taille, quotas, périmètre média, sélection exacte, empreinte des sources/commune/configuration et whitelist du prompt. Le test proche de la borne utilise un WebP décodable de 149 998 octets ; 150 000 sont refusés. |
| CA-07, CA-08, CA-10 | [PostgreSQL Atelier](../../../../localeo-backend/tests/integration/test_atelier_assiste_postgres.py) : migration v250 et rejeu, copies/snapshots BROUILLON, ordre, rollback de l'import et de la création, création concurrente à deux acteurs, résultat durable après 30 jours. Le test HTTP force un échec de commit : 500, aucune préparation/commande persistée, puis retry réussi. |
| CA-11 | [Conservation PostgreSQL](../../../../localeo-backend/tests/integration/test_atelier_conservation_postgres.py) et suite Atelier : expiration, simulation, effacement, résultat durable, images référencées préservées, URI alternatives et snapshots JSON, sentinelle terminale, garde de couverture des triggers, contention réelle à deux médias et trois tentatives avec rollback intégral, roundtrip de données avec échéance inchangée. |
| CA-12 | [Parcours navigateur ERP](../../../../localeo-backend/tests/browser/atelier-assiste-erp.cjs) : 390 et 1 280 px, import refusé, texte échappé, conservation du collage, image, confirmation et retry ; [présentation Marketplace](../../../../localeo-marketplace/tests/security/coffret-editorial.test.cjs), [scénarios visuels](../../../../localeo-marketplace/tests/visual/coffret-editorial.spec.cjs), [contrats backend](../../../../localeo-backend/tests/application/commercialisation/test_atelier_contenus.py) : contenu éditorial séparé des mentions BUM, ordre et fallback des anciens coffrets. |

Contrôles locaux :

- **561 tests backend réussis** : architecture, domaine Atelier, parseur, application,
  API, contenu éditorial, readiness, registre de démonstration, bootstrap et scheduler.
  Après le dernier test de borne WebP et le contrôle du commit HTTP, **42 tests parseur/API**
  ont également réussi. Ces suites se recouvrent ; leurs nombres ne s'additionnent pas.
- **13 tests PostgreSQL Atelier/conservation réussis** dans la passe consolidée,
  plus **7 tests HTTP PostgreSQL réussis**. Le runner isolé interdit les connexions
  externes et ne charge pas les fichiers `.env`. Les schémas de test sont supprimés.
- **13 tests ERP PostgreSQL existants réussis**, couvrant la non-régression du rattachement.
- Marketplace : **8 tests éditoriaux et lint ciblé réussis**. Les trois scénarios
  Playwright ont affiché un succès, mais le processus est resté bloqué à la fermeture
  et a été interrompu : ne pas annoncer une sortie globale verte pour ce runner.
- OpenAPI : génération hors ligne réussie, **9 chemins Atelier**. Aucun SDK ni appel IA.
- Documentation : **90 guides et 923 liens vérifiés**, aucune erreur ni avertissement ;
  **118 sources exportées vérifiées** ; `git diff --check` réussi dans les trois dépôts.
- Revue indépendante des contrats, droits, transaction et conservation : constats
  corrigés puis preuves ajoutées (fraîcheur, déduplication d'image, Unicode, formes
  d'URI, protection des sentinelles et reprise après contention).

Limites et contrôles élargis :

- La suite backend élargie a révélé un test Animation historique attendant
  `Passeport commercant` alors que le catalogue inchangé porte `Passeport commerçant`.
  Les deux fichiers sont inchangés par cette livraison. Le deuxième échec, le nombre
  de jobs attendu, a été corrigé pour vérifier explicitement le nouveau job Atelier ;
  la suite ciblée scheduler est verte. Sept tests ignorés de la suite élargie ne sont
  pas comptés comme succès.
- Suite sécurité Marketplace : **102/103** ; le hash du contrat moteur inchangé
  diverge à cause de la conversion locale LF/CRLF, confirmée contre le blob HEAD.
  Le lint global rencontre un répertoire `output` inaccessible ; le lint ciblé passe.
- PostgreSQL signale le cycle de clés étrangères existant entre profils commerçants
  et leurs versions. Aucun contournement ni skip ajouté aux preuves Atelier.
- Aucun essai chez un fournisseur IA, génération sur un environnement réel, migration
  déployée, restauration d'exploitation, commit ou push. La recette produit déployée
  reste distincte de ces validations locales ; l'epic n'est pas déclarée terminée.

Livraison : suivre le [guide d'activation et de conservation](../../exploitation/technique/localeo-atelier.md).
Appliquer `v250_localeo_atelier.sql` avant le backend, livrer les lecteurs Marketplace,
puis activer `LOCALEO_FEATURE_ATELIER_COFFRETS_ENABLED=true` après recette. La valeur
par défaut reste `false`. Les migrations futures ajoutant des tables doivent maintenir
la couverture des triggers ; sinon la purge refuse de supprimer des octets. Le générateur
peut laisser les préparations vides, sans simuler une création IA ; le registre et le
roundtrip dédié couvrent la restauration des nouvelles données et des échéances.
