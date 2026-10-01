# Localeo Atelier — Vérification et livraison

[Spécification V1](README.md) · [Architecture](architecture.md) · [Contrats](contrats.md)

## Clôture produit et préparation de livraison — 1er octobre 2026

**EPIC 66 terminée côté produit**, à la demande de l'utilisateur, après son « oui »
à la confirmation du parcours complet Atelier (création et affichage Marketplace)
et de l'installation puis réouverture de la PWA. L'environnement, les navigateurs,
les appareils et les références des coffrets de recette n'ont pas été précisés.
Cette déclaration opérateur n'est pas une observation directe de l'agent et ne
prouve pas une recette de toutes les plateformes ni une version déployée donnée.

La clôture est enregistrée dans le [backlog canonique](../../roadmap/terminees/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md).
Les bilans du 29 septembre ci-dessous restent historiques. Les réserves techniques
de livraison demeurent ouvertes : le manifeste automatique est **`blocked`**,
et aucun déploiement, commit ou push n'est effectué dans cette préparation.

### Versions examinées

Les cinq arbres étaient propres avant les contrôles. Seule la documentation de
clôture est modifiée ensuite ; les preuves métier concernent les SHAs ci-dessous.
La référence de la précédente livraison d'environnement n'est pas connue : aucune
comparaison avec la version réellement déployée n'est déclarée.

| Dépôt | SHA complet |
| --- | --- |
| Projet | `6beb93fa5349393c603249e66411472ce117089c` |
| Backend | `d1a16e82ff5ee037a8a6bff324d9bf87cd7cdd74` |
| Marketplace | `4e948f1f52ffb86a3bf992e015ce6107daae6545` |
| Commerçant | `38ff5ad32b1a4231de432d61474b00eb71cbf9c8` |
| Animation | `cac5eb431b3d8a8a18bc1311635f4f2f9e78c27c` |

### Preuves renouvelées

- **621 tests backend réussis**, aucun ignoré, 64,01 s : commande de consolidation
  V1.2 ci-dessous exécutée sur le SHA courant. 134 avertissements de dépréciation
  de l'adaptateur datetime SQLite, conservés dans le résultat.
- **24 tests PostgreSQL réussis**, aucun ignoré, 292,61 s : assemblage (6),
  conservation (7), prix (4), HTTP (7). Les quatre fichiers sont
  `test_atelier_assiste_postgres.py`, `test_atelier_conservation_postgres.py`,
  `test_atelier_prix_postgres.py` et `test_atelier_http_postgres.py`, sous
  `tests/integration/`, via `scripts/validation/test_isolated.py` avec
  `--postgres-test-url postgresql+psycopg://audit_test@127.0.0.1:55465/localeo_audit_test`.
  PostgreSQL 18 jetable, schémas synthétiques, instance arrêtée après exécution.
  26 avertissements : 24 cycles de clés étrangères de fixture et 2 dépréciations
  de `datetime.utcnow()` ; aucun contournement ajouté.
- **Trois scripts navigateur backend réussis** : `atelier-assiste-erp.cjs`,
  `atelier-prix.cjs`, `atelier-pwa.cjs`, sous `tests/browser/`, lancés par `node`.
  Largeurs 1280/390 px, réponses métier simulées, worker loopback réel ; cela ne
  constitue pas une nouvelle installation OS ni une recette distante.
- **Trois scénarios visuels Marketplace réussis**, 24,5 s, sortie normale :
  `node node_modules/@playwright/test/cli.js test --config=playwright.desktop.config.cjs tests/visual/coffret-editorial.spec.cjs`.
  Cette exécution lève la réserve de terminaison du runner signalée le 29 septembre.
- Bundle documentaire local construit et vérifié : **118 sources exportées**,
  **119 documents distribués avec le manifeste**. Empreinte du snapshot dans le
  manifeste de préparation ; les sorties restent sous `.artifacts/quality/`,
  hors Git. Les contrôles documentaires sont renouvelés après la clôture.

Revue indépendante en lecture du code et des preuves : aucun défaut bloquant
d'Atelier identifié. CA-14 s'appuie désormais sur la déclaration utilisateur,
sans matrice d'appareils. Pour CA-23, le prompt expérience et l'aide de relecture
sont testés ; les fixtures techniques ne prouvent pas le sens d'une image.
La confirmation du parcours ne constitue pas une preuve séparée de comparaison
de visuels « expérience » / « boîte ». Cette limite reste visible, et la relecture
humaine demeure nécessaire pour chaque proposition IA avant création.

### Contrôles généraux de livraison et blocages conservés

`python scripts/quality.py run --profile workspace` : **17 contrôles réussis sur
21**, quatre en échec. Le rapport conserve leurs codes de sortie :

| Contrôle | Constat |
| --- | --- |
| `backend-tests` | Collecte interrompue par trois noms de modules présents à la fois sous `tests/integration/` et `tests/security/` : `test_coffret_rate_limit`, `test_consultation_link_exchange`, `test_qr_revocation`. Trois tests ignorés lors de cette collecte ne valent pas réussite. |
| `marketplace-lint` | `EPERM` sur le dossier local `output/bum-politique/pytest-approval-1`. |
| `marketplace-security` | Empreintes des contrats moteur différentes dans l'arbre Windows. Vérification indépendante : les 198 entrées divergentes correspondent aux blobs Git HEAD et après normalisation CRLF vers LF. Aucun manifeste ni assertion modifié pour masquer l'échec. |
| `commercant-tests` | 376 tests réussis, un échec d'empreinte moteur. Même vérification des 198 entrées : blobs HEAD conformes, divergence locale CRLF/LF. |

Les builds des trois frontends passent ; Animation compte 169 tests réussis et
ses contrôles de types/lint passent. Le profil documentaire comprend un test
ignoré, conservé explicitement comme tel. Ces résultats ne rendent pas le profil
workspace globalement vert et ne remplacent pas la recette cible.

Artefacts de travail : `epic66-20261001-workspace.json`,
`epic66-20261001-release.json` et dossier `epic66-20261001-documentation`, dans
`.artifacts/quality/` du projet. Le manifeste est produit par :

```console
python scripts/quality.py release --report .artifacts/quality/epic66-20261001-workspace.json --bundle .artifacts/quality/epic66-20261001-documentation --output .artifacts/quality/epic66-20261001-release.json
```

Après la mise à jour documentaire de clôture, le projet est non committé : le
manifeste renouvelé conserve aussi cette limite de fraîcheur. Il faudra enregistrer
la documentation, résoudre les contrôles en échec et renouveler les preuves avant
de déclarer le dossier `prepared_for_review`.

### Conditions opérationnelles maintenues

- Backend et assets Atelier ensemble ; lecteurs Marketplace compatibles avant
  ouverture. Aucun changement applicatif effectué dans cette préparation.
- Migration `v250_localeo_atelier.sql` inchangée depuis `a28592d` ; checksum SHA-256
  normalisé selon le migrateur :
  `b43c591e5a57788b6179518795c1bcdb1b1b8ada086f3e004b7a1c78c78eacd2`.
  Sa présence et son checksum sur cible restent à contrôler selon la
  [procédure schéma](../../exploitation/technique/deployer-et-verifier-schema.md).
- Configurations à contrôler, sans valeurs privées :
  `LOCALEO_FEATURE_ATELIER_COFFRETS_ENABLED`, `LOCALEO_SCHEDULER_ENABLED`,
  `LOCALEO_DOCUMENTATION_ROOT`. Pas de nouveau fournisseur ni secret IA.
  Le build autonome doit utiliser la révision documentaire choisie explicitement
  (`prepare_documentation.py --revision <SHA-complet>`), ou le bundle préparé et vérifié.
- Profil `demonstration` planifié dans `epic66-20261001-demonstration-plan.json` ;
  transfert/restauration intégral du générateur non réexécuté dans cette passe.
  Aucun jeu ni environnement régénéré. Les tests PostgreSQL Atelier renouvellent
  la preuve de conservation et de roundtrip des préparations, sans valoir recette
  complète du générateur ni restauration d'exploitation.
- Avant livraison : sauvegarde et restauration adaptées à la cible, migrations
  puis readiness ; arrêter en cas de checksum différent ou de lecture indisponible.
  Contrôler ensuite droits, brouillon créé, prix, contenu Marketplace, reprise PWA
  et ordonnanceur de conservation. Leurs reçus opérateur restent à renseigner.
- Reprise : désactiver Atelier, conserver préparations, coffrets et sentinelles ;
  ne pas supprimer v250 ni réactiver les écritures d'un ancien backend sur des
  préparations AUTO sans compatibilité vérifiée. Voir le
  [guide d'activation et de conservation](../../exploitation/technique/localeo-atelier.md).

## État des preuves

**V1.2 du 29 septembre : implémentation locale.** PWA, prix AUTO/MANUEL et
consigne expérience (E66-CA-13 à 23) disposent des preuves spécifiques du bilan
V1.2 ci-dessous. Les résultats V1.1 ne couvrent pas seuls ces ajouts.
Les contrôles de liens/export ne sont pas une recette produit, et la vérification
locale de la PWA ne prouve pas son installation sur chaque appareil déployé.

## Bilan d'implémentation V1.2 — 29 septembre 2026

Arbre backend fondé sur `a28592d`, projet sur `0c5b0d9`, avec modifications locales
V1.2 non committées. Dépôts modifiés : backend et projet ; aucun changement des
frontends Marketplace, Commerçant ou Animation, des fichiers `.env` ou d'une base
d'exploitation. Pas de nouvelle migration : v250 est préservée. Les tests de base
ont utilisé uniquement PostgreSQL 18 local jetable, arrêté après validation.

Livré localement : shell Atelier PWA et menu Applications avec capacité serveur,
anciens liens redirigés, prix AUTO/MANUEL et compatibilité des préparations/contextes
anciens, template `atelier-coffret-v2` et relecture expérience. OpenAPI métier
régénéré hors ligne (neuf chemins, champ `mode_prix` additionnel). Les sources et
écritures atomiques partagent les règles commerciales existantes.

Preuves exécutées, sans skip sur ce périmètre :

- Runner isolé, contrôles d'architecture et recensements obligatoires, domaine et
  application Atelier, API, rattachement, parseur WebP, sécurité PWA et session :
  **611 tests réussis** en 30,21 s ; détail de la commande ci-dessous.
- PostgreSQL : `test_atelier_prix_postgres.py` + `test_atelier_http_postgres.py` :
  **11 réussis**, prix final, JSONB, concurrence, API et compatibilité. Socle
  `test_atelier_assiste_postgres.py` + `test_atelier_conservation_postgres.py` :
  **13 réussis**, création/idempotence, migration additive et conservation.
- `node tests/browser/atelier-assiste-erp.cjs` : réussi à 1280/390 px, import,
  image, erreurs, retries et confirmation avant abandon des retouches.
- `node tests/browser/atelier-prix.cjs` : réussi à 1280/390 px, AUTO/MANUEL,
  personnalisation conservée, retour au total, reprise, confirmation de tarifs,
  refus d'une notation numérique ambiguë, conflit et réponse tardive après expiration.
- `node tests/browser/atelier-pwa.cjs` : serveur HTTP loopback réel, worker enregistré
  et scope vérifié, panne réseau/API et page neutre 503, caches vides, menu et accès
  dégradé, session expirée/restaurée, logout entre onglets, retrait partiel des
  communes et montage lent concurrent à une revalidation ; réussi à 1280/390 px.
  Chromium CDP ne rapporte aucune erreur d'installabilité. Les captures desktop/mobile
  ont été inspectées dans `tmp/atelier-pwa-captures` (non versionné).

Commande de consolidation backend (Python 3.14, hors dotenv/services externes) :

```console
python scripts/validation/test_isolated.py tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py tests/domain/test_preparation_coffret_assiste_dedicated.py tests/domain/test_rattachement_modele.py tests/application/test_atelier_assiste.py tests/api/test_atelier_assiste.py tests/infrastructure/test_reponse_atelier.py tests/security/test_atelier_pwa.py tests/security/test_admin_session_cookie.py tests/security/test_admin_session_lifecycle.py tests/security/test_erp_session_access.py -q -p no:cacheprovider
```

Revue indépendante : trois défauts corrigés et couverts (prix exponentiel,
retouches perdues au rechargement, réaffichage après retrait partiel des droits),
puis correction de la course montage/revalidation. Le chargement concurrent du
menu et du shell a aussi conduit à stabiliser le jeton CSRF par session sans
affaiblir les contrôles Origin et de révocation. Deux lectures HTTP issues du même
cookie initial suivies d'un POST réel sont couvertes, ainsi que l'absence de jeton
ajouté dans les cookies retournés et les refus d'origine/session différente.

Contrôles documentaires finaux : **92 guides, 957 liens locaux, zéro erreur et
zéro avertissement**, **118 sources exportées vérifiées** ; diff sans erreur
d'espacement. Les avertissements de normalisation CRLF/LF de Git ne changent pas
le résultat de ces contrôles.

Limites : aucune installation réelle OS sur Chrome/Edge/Android/Safari iOS ni
recette HTTPS d'un environnement déployé ; cette partie de CA-14 reste à vérifier.
La présence des consignes et du rappel visuel ne garantit pas l'obéissance d'une
IA externe : aucune génération commerciale réelle n'a été soumise à recette.
Les suites complètes de tous les domaines ne sont pas déclarées vertes : seules
les suites listées ont été exécutées pour V1.2. Les avertissements observés concernent
les adaptateurs datetime SQLite et les cycles de clés étrangères des fixtures
historiques ; ils ne sont pas masqués. Ni commit, ni push, ni déploiement réalisés.

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

## Matrice V1.2 — preuves à produire

Cette table conserve le plan de preuve ; les exécutions et limites réelles sont
consignées dans le bilan V1.2 ci-dessous. Réutiliser les
tests de domaine/API/HTTP PostgreSQL et navigateur Atelier existants en les étendant,
sans remplacer leurs preuves V1.1. Les chemins désignent les suites à enrichir.

| Critère | Propriétaire / preuves attendues | Contrat et guide | Démonstration / fixtures | Livraison |
| --- | --- | --- | --- | --- |
| CA-13 | Navigation : `tests/browser/atelier-assiste-erp.cjs`, accès par menu à 390/1280 px et clavier, une entrée Atelier, autres liens conservés ; flag/droit absent masque seulement Atelier | Capacité contexte, routes et guide PWA | ADMIN, EXPLOITATION avec/sans commune, profil refusé | Backend et assets ensemble ; garder anciens liens |
| CA-14 | PWA : tests HTTP manifeste/icônes/SW publics neutres et scope ; recette réelle HTTPS installation puis lancement autonome sur Chrome/Edge desktop et Android, Safari iOS avec ajout écran d'accueil si disponible | Manifeste/installation facultative | Aucun compte fournisseur ; compte ERP de recette autorisé | Captures et navigateur/version ; indiquer les plateformes non testées, ne pas déduire installabilité du seul manifeste |
| CA-15 | Navigateur + API : deep link, reload, ancien lien 303, login puis retour sûr, même ID/version, fiche ERP après succès | Routes/retour login | Préparation existante, créée, expirée, hors commune | Pas de nouvelle base ou copie locale |
| CA-16 | `tests/integration/test_atelier_http_postgres.py` + navigateur : 401/403/404, retrait droits/flag, deux onglets et logout, retour arrière/bfcache/visibilité ; vérifier contenu masqué et aucune donnée protégée dans stockages/cache | Session/capacité et no-store | Profil révoqué après installation | Nouvelle entrée dans les gardes globaux ; aucune généralisation d'accès |
| CA-17 | Navigateur réseau : panne initiale, panne avant envoi, réponse perdue après commit, update avec saisie non enregistrée ; une création, aucune file/rejeu automatique, aucun worker des autres apps perturbé | Worker et reprise idempotente | Réponses simulées/DB jetable, pas de prod | Vérifier refus réseau et scope réel sous HTTPS |
| CA-18 | `tests/domain/test_preparation_coffret_assiste_dedicated.py` + application : somme 2500+4000+1500=8000, 10+20=30 centimes, ajout/retrait, doublon, 20 lignes dont hors pagination, zéro, null, négatif, dépassement plafond | AUTO, candidats éligibles avant budget | Prestations avec prix TTC distincts des reversements | Pas de migration SQL ; valider candidats plus chers que l'ancien prix |
| CA-19 | Application/PostgreSQL/navigateur : MANUEL 7500 conservé après ajout, égalité manuelle au total, retour AUTO, sauvegarde/reprise, requêtes en retard et conflits entre onglets | Table des commandes et mode JSONB | Préparations sans mode, null et modes nouveaux | Ancien client/prix sans mode ; nouvel UI/backend compatible |
| CA-20 | Domaine/API/HTTP : prix zéro/négatif refusé, budget insuffisant bloque prompt/import/création, total fourni en entrée refusé, rollback au commit, retry sans nouveau calcul/échéance, prix final exact | Contrat fermé et invariants I08/I09 | Budget juste/insuffisant et mode contradictoire | Rejouer CA-07/08 transaction/idempotence |
| CA-21 | PostgreSQL : source modifiée avec/sans incrément de version, mutation concurrente, GET sans réécriture, actualisation explicite, anciens contextes toujours compatibles si faits stables ; aucun achat/coffret retarifé | Versions d'empreinte, historique et droits | JSONB V1.1/V1.2, source supprimée, CREEE nettoyée | Sauvegarde/restauration mixte ; rollback avec Atelier désactivé |
| CA-22 | Domaine prompt : consigne présente avant/après données, intention « boîte cadeau » ne remplace pas les instructions, prestas seulement, pas de montants/contact ; V1 stocké inchangé, réémission V2/version empreinte2 | Template V2, JSON réponse V1 inchangé | Texte contradictoire, données libres, anciens prompts | Aucun appel IA réel obligatoire pour automatisation |
| CA-23 | Navigateur : rappel expérience, relecture sans case ajoutée, nouvel import refusé conserve ancien aperçu, remplacement valide ; revue humaine d'images expérience/boîte et textes promettant un colis | Aide relecture et limites du contrôle WebP | Illustrations fictives métier ; ne pas utiliser le carré WebP technique comme preuve sémantique | Relecture humaine distincte du test de présence de consigne ; aucune conformité universelle IA annoncée |

### Conditions de livraison V1.2

La revue indépendante de contrat a relevé trois ambiguïtés corrigées dans la
conception : invalidation limitée aux paramètres/sélection/mode, matérialisation
transactionnelle des métadonnées à la première émission V2 historique, notification
d'expiration du moniteur partagé. Ajouter explicitement aux tests CA-21 l'émission
V2 directe d'une ancienne préparation sans mutation préalable et la modification
de tarif sans incrément de version ; aux tests CA-16, un onglet visible laissé
inactif jusqu'à échéance et un 401 du moniteur sans requête métier.
Cette revue documentaire n'est pas une exécution de ces tests.

1. Implémenter backend/règles/DTO/guards/login et module UI partagé ; étendre le
   générateur OpenAPI puis régénérer son export avec les contrats réels.
2. Exécuter les contrôles d'architecture obligatoires et les suites ciblées de la
   table sur des fixtures locales, dont PostgreSQL pour concurrence/commit ;
   tester le schéma V1.1 existant sans migration et la conservation des données.
3. Livrer backend et assets de même révision avec activation Atelier maîtrisée.
   Aucun nouveau secret ou fournisseur ; migrer v250 seulement sur une cible qui
   ne l'a pas encore. Aucune intervention distante n'est autorisée par cette spec.
4. Recetter sous HTTPS menu, connexion, installation, reprise, prix et prompt V2.
   Les navigateurs non testés restent une limite explicite ; seules les preuves
   réellement exécutées peuvent lever les réserves de livraison.
5. Retour arrière : désactiver Atelier, conserver les préparations et résultats,
   revenir à la révision précédente et vérifier refus des URL/API. Le worker
   réseau ne garde pas de données ; ne pas réactiver les écritures de l'ancien
   backend sur des préparations AUTO sans correctif de compatibilité.

Impacts démo : fixtures et parcours de validation évoluent ; aucune nouvelle table
dans le registre ni génération distante nécessaire. Marketplace, Commerçant,
Animation et Live : contrats métier publics inchangés ; vérifier le prix canonique
du coffret créé et l'absence de changement dans les achats existants. Les menus et
connexions partagés ERP/Ops/Support/OnBoard/Control demandent une non-régression.

## Suites et couches de vérification V1.1

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
