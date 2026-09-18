# Compte rendu de réorganisation — 18 septembre 2026

> Complément du même jour : les derniers exports runtime et contrats backend ont depuis été centralisés. Consulter la [consolidation finale du backend](consolidation-documentation-backend-2026-09-18.md) ; les décisions de conservation locale ci-dessous décrivent la première étape.

La connaissance Localeo est centralisée dans `localeo-projet`, à côté des quatre applications, avec cinq dépôts Git indépendants. Aucun dépôt parent, sous-module ou changement de déploiement n’a été ajouté.

## Périmètre et analyse de départ

| Projet | Structure et responsabilité | Documentation avant réorganisation |
|---|---|---|
| Backend | FastAPI ; domaine, application, API, infrastructure ; SQLAdmin, scripts, SQL, tests | 486 fichiers inventoriés : architecture, spécifications, exploitation, juridique, roadmap, audits et 104 notes de release |
| Marketplace | React, Vite, React Query ; `src/pages`, composants, services ; serveur Node ; Localeo Live | 63 fichiers de documentation et scripts d’audit, dont quatre spécifications non suivies par Git ; prompts, images et comparateurs sous `output` |
| Commerçant | React/Vite/PWA ; API et composants ; tests unitaires et e2e | 49 fichiers documentaires et scripts ; cinq versions de guide PDF ; absence de README racine et de guide agent |
| Animation | React/TypeScript/Vite ; pnpm ; interfaces partenaires | 68 documents et artefacts inventoriés, plus DEPLOY, brief UX et gabarit Figma ; redondances avec le backend |

Le périmètre comprend les documents présents sur disque, y compris les quatre nouvelles spécifications Marketplace et la modification préalable de `DEPLOY.md` Animation. Les changements applicatifs préexistants de Marketplace ont été préservés. Les fichiers d’environnement et données d’exploitation n’ont pas été intégrés au dépôt documentaire.

## Organisation mise en place

- `docs/produit` : vision fonctionnelle, parcours, identité visuelle et formations.
- `docs/architecture` : transverse, backend, frontends, décisions et modèles.
- `docs/specifications` : dossiers fonctionnels partagés et détails propres aux applications ; la spécification du moteur est dans `moteur-animation`.
- `docs/roadmap` : pilotage commun, contributions par application et anomalies.
- `docs/exploitation` : procédures, déploiements, démonstrations et recette.
- `docs/juridique` : textes, publication et licences.
- `docs/audits` : constats datés, conservés par application.
- `livrables` : formations PDF et travaux visuels Marketplace.
- `releases` : historique des releases backend et manifeste de coordination initial.
- `docs/archives` : anciens index et gabarit Figma sans règle active.

Les identifiants EPIC historiques sont conservés. Ils ne sont pas uniques entre les projets : EPIC 53 Marketplace désigne la pagination, alors qu’EPIC 53 Animation désigne la tombola. Aucune fusion n’a été fondée sur le seul numéro.

La [consolidation ultérieure des backlogs par état](consolidation-roadmap-2026-09-18.md)
réunit désormais les contributions applicatives dans leur EPIC commune, rattache
la pagination à l'EPIC 57 et distingue les anciens numéros Marketplace 18 et 54
par des identifiants préfixés. Les sources historiques ci-dessous restent la
trace de la première réorganisation ; les destinations du manifeste sont actualisées.

## Déplacements, dédoublonnage et fusions

| Action | Fichiers sources concernés |
|---|---:|
| contrat-genere-conserve | 2 |
| deplace | 558 |
| doublon-supprime | 27 |
| fusion-version-complete | 1 |
| fusionne | 41 |
| guide-technique-local | 1 |
| outil-technique-deplace | 5 |
| renvoi-local | 1 |
| snapshot-runtime | 109 |

Total : **745 fichiers sources**, dont 27 doublons supprimés et 41 sources réunies dans 19 documents fusionnés. Les exports techniques ne sont pas des copies éditoriales concurrentes.

Les copies ont été comparées par contenu, en neutralisant seulement BOM UTF-8 et fins de ligne CRLF. Les audits homonymes, différentes versions de formation et releases datées ont été conservés : ce sont des contenus distincts.

Les fusions sémantiques couvrent notamment :

- Localeo Live : carnet et familles, actualités, exigences backend WebAuthn, API et décisions existantes.
- Animations Marketplace : contrats backend et comportement du flag, dont le défaut `true` a été vérifié dans le code courant.
- BUM Commerçant : routes, pièces multipart, détail groupé, correction et PRO-009.
- Paiement des lots d’animation : architecture, API, Stripe, arbitrages et parcours.
- Participation des commerçants : invitations, contact de l’auteur, notifications, flyer et avertissement du 13 septembre.
- Publication juridique : procédure unique avec les surfaces Commerçant et Animation.
- Anomalies Marketplace : registre actuel et signalements historiques ; statut inconnu explicitement conservé.
- Authentification Animation : session navigateur actuelle distinguée de l’ancien modèle de jeton en mémoire.

Le rapport API racine Animation, inclus intégralement dans une version plus complète, a été supprimé au profit de cette dernière. Le brief Figma recopié dans `src/imports/pasted_text` a été regroupé avec sa source documentaire. Le patch `ano-ani-02-backend.patch` reste un artefact de travail, sans application au code.

Dix-huit livrables supplémentaires du backend (PDF, PNG et DOCX) ont été classés : exemples techniques et versions juridiques de travail. Les copies identiques ont été rattachées à leur document canonique ; les onze PDF opérationnels utilisés par l’ERP restent distribués dans le backend. Une sauvegarde complémentaire est conservée dans `localeo-marketplace/tmp/reorganization-additional-before-2026-09-18.zip`.

Les fichiers et actions exacts sont tracés dans [le manifeste de migration](migration-2026-09-18.json), avec dépôt source, chemin initial, chemin cible, empreinte avant migration, statut de suivi Git et type d’action. La sauvegarde locale `localeo-marketplace/tmp/reorganization-before-2026-09-18.zip` contient les originaux et guides locaux ; elle est exclue du dépôt transverse. Les historiques Git des applications restent accessibles.

## Autonomie des applications et fonctionnement préservé

Les README techniques et notices associées au code restent dans leurs applications. Les guides d’agent renvoient explicitement au guide transverse. Un workspace VS Code ouvre les cinq dossiers ; `repositories.json` décrit les responsabilités et commandes. Ce workspace ne change pas les autorisations de l’environnement d’exécution de l’agent.

Les outils d’audit exécutables ont été déplacés de `docs/audits` vers `scripts/audits` dans leurs applications : leur accès au serveur local et aux dépendances est conservé. Les deux contrats OpenAPI backend générés pour EPIC 41 et EPIC 42 restent avec leurs générateurs et tests.

Les copies backend d’exploitation et juridiques sont nécessaires au lecteur ERP, à la configuration affichée et au script de publication. Leurs sources sont centralisées ; les copies distribuées restent aux chemins attendus et sont contrôlées par SHA-256. Le synchroniseur traite les liens Markdown et refuse d’écraser une copie modifiée localement. Le backend peut être cloné et déployé seul ; sa CI vérifie le manifeste sans accès à `localeo-projet`.

Les PDF publics des frontends, les 11 PDF opérationnels distribués par le backend, les fixtures, données de référence et jeux de démonstration restent des ressources applicatives. Aucun texte juridique n’a été publié à distance, aucun service Render redéployé et aucune base modifiée.

## Points conservés à arbitrer

Le classement des documents inventoriés est terminé. Les variantes qui portent encore des compléments ou contradictions sont identifiées par leur application, avec renvois communs. Elles ne constituent pas des règles métier nouvellement validées. Le [registre des variantes](variantes-a-harmoniser.md) donne les renvois précis vers chaque version.

| Sujet | Écart conservé ou règle à préciser |
|---|---|
| Localeo Live | CTA de confirmation email systématique ou facultatif selon les anciens documents ; coexistence de règles de présence/WebAuthn et de parcours carnet à lire selon leur contexte |
| Paiement des lots | Clôture avant/après attribution, réponse HTTP de rejeu 201/200, métadonnées Stripe et état de matérialisation dans les versions anciennes |
| Participation commerçants | Descriptions divergentes de l’aperçu privé du flyer ; compléments conservés et identifiés |
| Synthèse Animation ancienne | Prix Essentielle 708 € HT dans la synthèse du 4 septembre, 990 € HT dans les textes juridiques ultérieurs ; ancien statut de recette EPIC 47 face à sa clôture dans la roadmap |
| Variantes EPIC 41, 47, 50, 53, 58 | Versions backend et interface non identiques conservées avec provenance ; harmonisation métier future possible, sans suppression de clauses distinctes |

### Documents ou ensembles non reclassés

- `localeo-marketplace/output/bum-politique/politique-bum-a-valider.md` : ancien brouillon de validation au milieu d’artefacts d’exploitation. À qualifier comme archive de travail ou à supprimer après vérification avec la politique approuvée ; laissé sur place.
- `localeo-marketplace/output/demo-generation` et `output/reference-import` : ensembles mêlant jeux de données, comptes, importations, preuves et sorties de tests. Ils restent dans le dépôt applicatif ; préciser quels éventuels livrables expurgés doivent rejoindre la connaissance commune. Certains répertoires temporaires de tests refusent la lecture.
- `localeo-marketplace/output/hero-v35-tests.patch` : patch de tests non appliqué, laissé avec le projet applicatif ; à qualifier comme correctif à intégrer ou historique à archiver.

Quatre références à trois anciens documents juridiques absents avant migration sont également consignées dans le [registre des sources historiques absentes](sources-historiques-absentes.md). Il ne s’agit pas de fichiers perdus pendant le déplacement.

Ces exclusions ne remettent pas en cause le classement des fichiers de `docs/`, des rapports racine et des livrables identifiés. Les caches, dépendances, builds et répertoires temporaires ne sont pas une source documentaire.

## Vérifications et limites

| Contrôle | Résultat |
|---|---|
| Intégrité et classement | 745 fichiers sources sauvegardés et vérifiés ; toutes les destinations présentes ; 27 doublons confirmés par contenu |
| Indépendance Git | Cinq racines distinctes ; quatre HEAD applicatifs inchangés ; dépôt transverse initialisé |
| Liens Markdown | Aucun chemin relatif manquant après corrections ; quatre anciennes références à des sources absentes consignées explicitement ; les ancres intra-document ne font pas l’objet d’une validation exhaustive |
| Copies distribuées | 109 exports, contrôle autonome backend et contrôle avec les sources canoniques |
| Synchroniseur | 14 tests réussis, 1 ignoré ; cas de libellé contenant du code inline ajouté pour préserver les liens ERP |
| Vérificateur backend | 23 tests réussis, 2 ignorés |
| Tests ciblés ERP, configuration, OpenAPI, juridique et base documentaire | 100 réussis, 15 échecs préexistants, 1 ignoré |
| Contrôle final après resynchronisation : ERP, configuration, OpenAPI et juridique | 68 réussis, 1 ignoré : les dépendances isolées de la CLI juridique ne sont pas installées pour `test_preparation_juridique.py` |
| Session navigateur Animation | 12 tests frontend réussis pour confirmer le comportement décrit dans la fusion |
| Outils d’audit déplacés | Vérification syntaxique Node des quatre scripts réussie ; même profondeur relative vers leurs dépendances |
| Diffs Git | `git diff --check` réussi dans les cinq dépôts ; ce contrôle ne couvre pas les fichiers encore non suivis |

Les quinze échecs préexistants concernent treize documents ne respectant pas le plan de procédure exigé et deux index incomplets. Les mêmes assertions appliquées aux originaux sauvegardés retrouvent exactement les mêmes échecs : [détail avant/après](tests-preexistants-2026-09-18.json). Aucun test n’a été désactivé ou assoupli. Les trois tests de liens symboliques ignorés dans les suites des nouveaux outils demandent un droit Windows absent dans cet environnement ; leurs autres protections de chemins sont testées.

Les sources textuelles du transverse ont été normalisées en LF, avec règles Git explicites. Le backend impose également LF pour ses copies documentaires et conserve les PDF binaires, afin que les empreintes ne changent pas selon le système du clone. L’identité des contenus bruts et des objets Git après filtrage a été vérifiée pour les 109 sources et leurs 109 exports. Les tests ciblés restent locaux, sans connexion à la démonstration ni à une base de production. Aucun build frontend n’a été nécessaire pour ce changement documentaire.


Le générateur backend `scripts/documentation/generate_ops_pdfs.js` utilise onze anciens chemins de sources déjà absents avant cette réorganisation. Les PDF existants ont été préservés ; ce générateur demande une remise à niveau distincte avant régénération. Les anciennes assertions de tests et résultats de recette inclus dans les documents ne sont pas présentés comme de nouveaux tests exécutés.

La première tentative a détecté un document Windows-1252 avant toute écriture dans le nouveau dépôt. Les 727 sources et leurs copies de sauvegarde ont été revérifiées intactes avant reprise. La conversion de ce document en UTF-8 est tracée dans le manifeste.

Les cinq dépôts restent locaux et indépendants. Le nouveau dépôt est initialisé, sans dépôt distant créé. Les modifications de cette réorganisation n’ont pas été commitées ni poussées ; le manifeste initial contient les HEAD antérieurs, pas les SHAs d’une release.
