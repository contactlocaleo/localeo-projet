# EPIC 66 — Localeo Atelier

Évolution complémentaire du 29 septembre 2026 : [installation et mise à jour explicite des PWA](../installation-mise-a-jour-pwa.md), commune à Atelier et six autres applications. Le header remplace les commandes d'installation/mise à jour auparavant situées dans le contenu. Les protections de session et de saisie de la V1.2 sont conservées.

## Statut et sources

Spécification V1.2 du **29 septembre 2026**, issue du
[backlog EPIC 66](../../roadmap/en-cours/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md).
État produit : **En cours**, selon la [roadmap](../../roadmap/README.md) :
implémentation locale réalisée, validation en cours.
Ce dossier décrit les comportements et leur mise en œuvre ; les preuves et limites
de livraison sont tenues dans le [document de vérification](verification-livraison.md).

**Extensions V1.2 implémentées localement, en validation :** le cadrage `E66-PWA-20260929` du
[backlog](../../roadmap/en-cours/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md)
ajoute une application PWA Localeo Atelier et son entrée dans le menu Applications
de l'ERP (E66-CA-13 à 17). Il fait évoluer la présentation intégrée décrite par
E66-C04, tout en conservant le déploiement backend. La présente V1.1 et ses preuves
ne couvrent pas cette extension ; ses preuves propres sont consignées dans le bilan V1.2. La cible est détaillée ci-dessous et dans
[l'architecture](architecture.md), les [contrats](contrats.md) et la
[matrice des preuves à produire](verification-livraison.md).

**Précision spécifiée en V1.2 :** `E66-PRIX-20260929` dans le même backlog prévoit un
prix TTC prérempli par la somme des valeurs TTC des prestations sélectionnées,
modifiable par l'opérateur (E66-CA-18 à 21). Cette cible fait évoluer la saisie
initiale du prix décrite ci-dessous ; son calcul automatique est implémenté.
Les contrôles de budget et l'absence de décision financière par l'IA
restent inchangés.

**Précision spécifiée en V1.2 :** `E66-EXPERIENCE-20260929` impose au prompt de définir
le coffret comme une expérience multi-prestations vécue sur place, sans boîte ou
emballage représentant le produit vendu (E66-CA-22 et 23 du backlog). Les textes
et le visuel doivent refléter les prestations réelles. Cette consigne explicite
est implémentée dans le générateur ; le contrôle WebP ne vérifie pas le sens
de l'image produite.

Base de conception V1.2 : backend `a28592d`, projet `0c5b0d9` avec les cadrages
locaux du 29 septembre ; lecture du code et revue de contrat, sans accès à une
base d'exploitation. Aucun arbitrage produit bloquant n'est identifié : les
extensions ont été implémentées suivant cette conception. Leur livraison
reste conditionnée aux preuves planifiées ; elles ne sont pas acquises par les
tests V1.1 ni par les contrôles documentaires.

- [Domaine, données et transaction](architecture.md).
- [Contrats, prompt et import](contrats.md).
- [Schéma normatif de réponse IA V1](reponse-ia.schema.json).
- [OpenAPI des routes Atelier implémentées](openapi.json).
- [Exemple fictif conforme](reponse-ia.exemple.json).
- [Traçabilité, tests et livraison](verification-livraison.md).
- [Guide opérateur, activation et conservation](../../exploitation/technique/localeo-atelier.md).

Applications concernées : **backend**, qui sert l'ERP et le DAM, et **Marketplace**,
qui doit afficher les nouveaux contenus après publication. Commerçant, Animation
et Live sont des consommateurs à vérifier pour les contrats partagés, sans nouveau
parcours de génération dans ces applications.

## Décisions et hypothèses

| Référence | Nature | Choix et conséquence |
| --- | --- | --- |
| E66-D01 | Validé par l'utilisateur | Nom **Localeo Atelier** ; contrat court, erreurs en français, reprise selon les droits ERP actuels. |
| E66-D02 | Validé par l'utilisateur | Visuels **WebP**, strictement inférieurs à **150 Ko** ; convention documentée : moins de 150 000 octets. Contrôle du fichier réel, y compris en bibliothèque. |
| E66-D03 | Besoin acquis | Choisir une commune et ses prestations, copier un prompt dans une IA externe, coller son retour, puis créer automatiquement le coffret après confirmation. Aucun fournisseur IA intégré. |
| E66-C01 | Choix de conception | Un coffret inclut exactement les modèles sélectionnés, une fois chacun, dans l'ordre proposé puis validé. L'IA ne décide ni des prix, ni des reversements, ni des statuts, ni de la qualification BUM. |
| E66-C02 | Choix de conception | Tous les objets créés restent **BROUILLON**, y compris les copies des prestations actives. Publication par le parcours ERP existant. |
| E66-C03 | Choix de conception | Textes éditoriaux séparés de `promesse_garantie` et `contenu_indicatif` ; aucun remplissage fiscal ou contractuel automatique depuis l'IA. |
| E66-C04 | Choix V1 remplacé pour la présentation par D06 | Entrée intégrée à l'ERP dans la V1 ; la V1.2 ouvre une PWA dédiée, toujours servie par le backend. Le dossier ERP reste canonique après création. |
| E66-D04 | Précision utilisateur du 29 septembre, remplace H01 | Le prompt unique fait produire toutes les informations éditoriales **et l'image réelle WebP encodée en base64 dans le JSON**. Un seul contenu à coller ; ni fichier séparé obligatoire, ni second prompt de génération. |
| E66-C05 | Conséquence de conception | Décoder et contrôler l'image à l'import puis enregistrer proposition et média ensemble. Création via Atelier avec image conforme au contexte courant. Sauvegarde de préparation incomplète conservée ; le DAM est un remplacement volontaire après import. |
| E66-D05 | Validé par l'utilisateur le 29 septembre, remplace H02 | Conservation du contenu des préparations : **30 jours après la dernière modification enregistrée**. Consultation et retry ne prolongent pas le délai. Expiration à l'échéance et nettoyage quotidien ; coffrets créés, médias utilisés et marqueurs d'unicité préservés. |

La signature commerciale proposée dans le backlog n'est pas validée par le seul
choix du nom. Les limites chiffrées des contrats ci-dessous sont des choix de
conception V1, pas des validations utilisateur supplémentaires.

| Référence V1.2 | Nature | Décision |
| --- | --- | --- |
| E66-D06 | Demande utilisateur | PWA Localeo Atelier installable, accessible depuis le menu Applications ERP, mêmes droits et préparations. |
| E66-D07 | Demande utilisateur | Prix TTC proposé = somme des valeurs TTC des prestations sélectionnées, modifiable. |
| E66-D08 | Demande utilisateur | Le prompt définit explicitement une expérience multi-prestations vécue sur place et exclut le coffret matériel comme représentation du produit vendu. |
| E66-C06 | Conception | PWA sous `/internal/atelier/`, usage en ligne, aucune donnée authentifiée en cache persistant ; anciens liens ERP conservés par redirection. |
| E66-C07 | Conception | Modes AUTO/MANUEL ; prix personnalisé conservé lors des changements de sélection et à la reprise, action explicite pour revenir au total. Les préparations historiques gardent leur prix. |
| E66-C08 | Conception | Pas de nouvelle migration SQL : métadonnées de calcul dans le JSONB existant avec lecture compatible des anciennes lignes. Pas de modification de v250. |

## Existant vérifié et écarts

Référence avant implémentation : lecture du backend `9b9cba3` et de la Marketplace
`0aa5e77`, sans connexion à une base. Les constats ci-dessous décrivent cet état initial :

| Source existante | Constat | Adaptation cible |
| --- | --- | --- |
| [Atelier ERP](../../../../localeo-backend/app/application/commercialisation/services/atelier_erp.py) | Création d'un coffret brouillon et copies versionnées des modèles ; transaction fournie par l'appelant. Le rattachement recopie actuellement le statut ACTIVE du modèle. | Réutiliser les règles et ports avec une commande de composition atomique dont les copies sont BROUILLON. |
| [Règles d'Atelier](../../../../localeo-backend/app/domaine/commercialisation/services/regles_atelier.py) | Commune, versions, éligibilité, absence de doublon, budget et montants. | Même service de domaine pour les nouvelles entrées ; aucun calcul financier par l'IA. |
| [Commandes ERP](../../../../localeo-backend/app/api/erp_api.py) | CSRF, idempotence par acteur et clé pendant 24 h, audit, commit en fin de requête. | Ajouter une unicité durable préparation → coffret, indépendante de la clé et de l'opérateur. |
| [Schémas ERP](../../../../localeo-backend/app/api/erp_schemas.py), [modèles persistés](../../../../localeo-backend/app/infrastructure/persistence/models.py) | Pas de description/accroche/texte alternatif dédiés au coffret, ni d'ordre de présentation explicite des prestations. | Champs additifs et mapping canonique ; préserver le sens des champs BUM. |
| [DAM](../../../../localeo-backend/app/application/dam/services/service_images.py), [contrôles raster](../../../../localeo-backend/app/security/uploads.py) | Stockage en transaction, quota et signatures raster ; plusieurs formats autorisés, pas de décodage complet démontré par le contrôle de signature. | Politique WebP Atelier et décodage contrôlé avant admission, sans restreindre les autres parcours DAM. |
| [Sécurité ERP](../../../../localeo-backend/app/security/erp.py) | ADMIN global et EXPLOITATION limité à ses communes ; pas de profil Lecteur implémenté dans ce garde. | Respecter les droits actuels ; adapter les capacités à l'évolution EPIC 35 lorsqu'elle est livrée. |
| [Fiche Marketplace](../../../../localeo-marketplace/src/pages/CoffretPage.jsx) | Visuel et contenu issus des projections actuelles ; description éditoriale dédiée et texte alternatif IA non consommés. | Afficher les nouveaux champs avec replis pour les anciens coffrets, sans toucher aux conditions d'achat. |

## Parcours et comportements

### 1. Préparer — E66-CA-01, 02, 11

Depuis Commercialisation, ouvrir une préparation ou cliquer « Nouveau coffret ».
Choisir une commune autorisée, un type de coffret existant et la durée de validité.
En V1.2, la sélection préremplit le prix TTC selon le parcours de prix ci-dessous.
L'opérateur peut le personnaliser ; aucun montant n'est reçu de l'IA.
Ajouter entre 1 et 20 modèles actifs, filtrables par commerçant et texte.
La liste indique le lieu, la valeur TTC et les informations économiques ERP ;
les reversements/marges restent dans Localeo. Un candidat indisponible affiche
son motif. Le budget global est vérifié après chaque modification et avant prompt.

Un brouillon de préparation incomplet peut être enregistré. Une intention
facultative (500 caractères) précise le thème ou le public. Les doublons de modèle
et les libellés de prestations incompatibles avec l'unicité actuelle du coffret
sont signalés avant génération ; aucun renommage automatique d'une source.
Changer de commune requiert de confirmer la remise à zéro de la sélection et
du retour IA. Aucune modification n'est perdue par simple navigation après
l'enregistrement confirmé. Une erreur réseau conserve la saisie en mémoire ;
aucun contenu personnel du prompt n'est persisté dans le stockage du navigateur.

### 2. Copier le prompt — E66-CA-03, 09

« Copier le prompt » enregistre une version du contexte puis copie le texte
préparé par le serveur. Si le presse-papiers est indisponible, afficher un champ
sélectionnable, sans imposer un téléchargement. Le prompt contient uniquement
les faits autorisés, des références opaques de préparation et le contrat court.
Les textes sources sont présentés comme des données, jamais comme des instructions.
Afficher « À coller dans votre IA » et « Coller la réponse complète ».
Le même prompt demande de produire directement les textes et l'image WebP, sans
faire rédiger à l'opérateur une seconde demande. Le JSON contient les octets de
l'image encodés en base64. Utiliser une IA avec les outils nécessaires pour générer
une image, l'exporter en WebP et encoder ses octets réels ; un modèle textuel ne
doit pas inventer cette chaîne. Un retour sans WebP conforme est refusé en français.

Toute modification de commune, sélection, version source, intention, type, prix
ou validité invalide le contexte précédent. Un changement d'image ou une retouche
éditoriale locale ne nécessite pas un nouveau prompt, mais change la version de
préparation et impose une nouvelle confirmation de création.

### 3. Coller et relire — E66-CA-04, 05, 06

Coller la réponse puis « Afficher la proposition ». Aucun JSON à corriger à la main.
Le parseur accepte l'objet JSON seul ou une unique clôture Markdown `json` entourant
exactement cet objet ; prose additionnelle et réponses multiples sont refusées.
La réponse ne déclenche ni création de coffret, ni téléchargement externe, ni outil
IA côté Localeo. L'import décode localement l'image intégrée et l'enregistre dans
le DAM uniquement si toute la réponse est valide.

Sans ajout manuel de fichier, l'aperçu affiche nom, accroche,
description, ordre et prestations exactes, image réelle et texte alternatif.
Un second prompt, une URL ou une description d'image ne remplace pas les octets intégrés.
Prix, contenu des prestations et informations métier
restent issus de Localeo. Nom, accroche, description, ordre et texte alternatif
peuvent être ajustés ; modifier le contenu d'une prestation source n'est pas proposé.
Les mentions BUM et la promesse contractuelle restent à traiter dans le dossier ERP.
L'opérateur vérifie les allégations factuelles ; les contrôles de structure ne
garantissent pas qu'une phrase IA est véridique.

L'image importée ou choisie doit être active, accessible, décodable en WebP et
mesurer de 1 à 149 999 octets. Contrôler aussi le contenu réel d'un média existant.
Image invalide : message en français, sélection et textes conservés, aucun
rattachement invalide. Absence d'image/base64 invalide : retour refusé sans écriture
partielle, préparation précédente conservée. Un nouveau contexte
invalide la confirmation du visuel précédent ; réimporter un JSON complet avec
image pour le nouveau contexte avant tout remplacement volontaire. Localeo ne peut prouver la provenance
IA d'un fichier ; il contrôle sa conformité et l'opérateur confirme sa pertinence.

### 4. Créer et poursuivre — E66-CA-07, 08, 10

« Créer le coffret » confirme la version affichée, les textes et la composition.
Désactiver l'action pendant la requête, afficher un indicateur de traitement et
une confirmation. Le serveur recontrôle droits, sources et visuel puis crée en
une transaction le coffret, les copies/version 1 des prestations, leurs liens aux
modèles et l'origine Atelier. Aucun statut ACTIVE, qualification ou publication
n'est déduit de cette confirmation.

Après succès, ouvrir la fiche ERP canonique et afficher les points restant à
compléter pour publier. Une réponse réseau perdue est résolue en relisant la
préparation : si elle est créée, « Ouvrir le coffret » remplace « Créer ».
Deux opérateurs ou deux clés différentes ne peuvent créer deux coffrets depuis
la même préparation. Revenir à une préparation créée ne relance pas l'assemblage.
Les modifications ultérieures passent par le dossier ERP, sans synchronisation
automatique avec le retour IA d'origine.

### Ergonomie et refus — E66-CA-12

Sur ordinateur, liste/sélection et aperçu occupent la largeur disponible en deux
zones ; sur mobile, elles suivent l'ordre du parcours. Une action principale par
étape, boutons avec curseur adapté, états occupés et erreurs annoncées aux aides
techniques. Le focus rejoint le premier problème sans effacer le texte collé.
Toutes les erreurs visibles sont en français et proposent une action concrète.
Un conflit d'édition invite à recharger/comparer, sans écraser la dernière sauvegarde.
Une perte de droits interdit la reprise et n'affiche plus le contenu protégé.

## Présentation PWA — E66-CA-13 à 17 (cible V1.2)

Le menu déroulant **Applications** de l'ERP propose **Localeo Atelier** lorsque
le serveur autorise l'accès et que le flag est actif. Le menu partagé, la carte
d'accueil et le raccourci Commercialisation utilisent la même destination
`/internal/atelier/`. Aucun rôle ou droit n'est inféré de l'installation.
Les autres entrées du menu sont conservées. L'application affiche son identité,
la liste des préparations, **Nouveau coffret**, **Accueil ERP** et **Se déconnecter**.
La préparation s'ouvre sous `/internal/atelier/preparations/{id}` ; un lien direct
et un rafraîchissement retrouvent la même préparation après contrôle serveur.

Sur un navigateur compatible, l'installation utilise le nom **Localeo Atelier**,
son icône et une fenêtre autonome. Le bouton d'installation apparaît seulement
si le navigateur fournit cette possibilité ; une aide indique sinon la commande
d'installation du navigateur, sans promettre sa disponibilité partout. L'usage
web complet reste possible. Aucun push ni accès métier hors ligne n'est ajouté.

Une session absente conduit à la connexion avec un retour interne contrôlé vers
l'URL demandée. Une session expirée masque les données, suspend les actions et
propose la reconnexion ; aucune sauvegarde ou création n'est rejouée automatiquement.
Après reconnexion, recharger l'état serveur et résoudre le conflit éventuel avant
nouvelle commande. La saisie non enregistrée n'est pas persistée pour traverser
la connexion ; informer l'opérateur de cette limite. Au retour d'arrière-plan,
revalider session et disponibilité avant de réafficher le contenu protégé.

Une coupure conserve seulement la saisie de l'onglet encore autorisé en mémoire,
affiche **Connexion interrompue — vos dernières modifications ne sont pas enregistrées**,
et bloque les nouvelles commandes. Une perte de réponse après création déclenche
une relecture explicite de la préparation ; résultat durable et clé d'idempotence
empêchent un second coffret. L'accès initial hors réseau présente une page neutre.
Une mise à jour disponible propose un rechargement après avertissement si la saisie
n'est pas enregistrée ; elle ne remplace pas le formulaire pendant son utilisation.

## Prix proposé et personnalisé — E66-CA-18 à 21 (cible V1.2)

Une préparation nouvelle utilise **AUTO**. À chaque sélection enregistrée, le
serveur additionne les valeurs TTC des modèles/version retenus. Afficher côte à
côte **Total des prestations** et **Prix TTC du coffret**, avec la mention
**Calculé automatiquement** ou **Personnalisé**. Exemple : 25 € + 40 € + 15 € = 80 €.
La sélection est indépendante de la pagination/recherche de candidats : toute la
sélection est comptée, y compris les lignes hors de la page visible.

Les ajouts/retraits de sélection sont enregistrés par commandes versionnées
sérialisées ; la réponse serveur actualise le prix. Pendant le calcul, signaler
**Calcul en cours** et bloquer prompt/création ; ne pas afficher l'ancien total
comme celui de la sélection non confirmée. Une erreur conserve la saisie à corriger
et distingue clairement les changements non enregistrés. Les modifications du
prix manuel suivent le même enregistrement versionné, sans requête par frappe.

Modifier le prix bascule en **MANUEL**, même si le montant est égal au total.
Un ajout ou retrait actualise le total mais conserve le prix personnalisé.
**Utiliser le total des prestations** repasse explicitement en AUTO. Sauvegarde,
reprise, second onglet et PWA ne changent pas ce mode. Un conflit de version exige
de recharger ; aucune réponse asynchrone ancienne ne remplace la dernière sélection.

Sans prestation, le total vaut 0, le prix AUTO reste vide et la création est
impossible. Un tarif absent ou invalide rend le total indisponible avec le motif ;
il ne vaut pas zéro. Un total nul ou dépassant le plafond du prix est affichable
mais ne devient pas un prix AUTO valide ; l'opérateur peut corriger la sélection
ou choisir un prix manuel conforme. Les contrôles de budget restent obligatoires
avant émission du prompt, import et création. Une préparation MANUEL sous le budget
peut être conservée en brouillon pour correction, sans pouvoir avancer.

Un prix ou une sélection modifiés invalident contexte et aperçu selon le parcours
existant. Une bascule de mode, même à montant égal, est une modification explicite
de préparation et invalide également le contexte. Une lecture ne recalcule jamais
le prix sauvegardé à partir d'un nouveau tarif source. Une source devenue obsolète
est signalée ; l'opérateur recharge les versions puis confirme l'actualisation.
En AUTO, ce changement explicite recalcule le prix ; en MANUEL, seul le total change.

## Expérience à illustrer — E66-CA-22 et 23 (cible V1.2)

Le prompt contient systématiquement la définition et les exclusions rédigées dans
les [contrats](contrats.md), indépendamment du thème saisi. Il demande de montrer
les activités/prestations réelles, pas une boîte à acheter. Les plats, outils et
autres objets nécessaires à une prestation restent représentables. Textes et
texte alternatif ne promettent aucun colis ou cadeau matériel non inclus.

Au-dessus de l'aperçu, afficher **Le visuel doit représenter les expériences
proposées, pas une boîte cadeau**. L'opérateur relit avant **Créer le coffret** ;
aucune case supplémentaire obligatoire. En cas d'image inadaptée, il peut recopier
le prompt et importer une nouvelle réponse sous le contexte courant, ou remplacer
volontairement le média après import complet selon les règles existantes. L'ancien
aperçu reste conservé tant qu'un nouvel import n'a pas réussi. Pas de classificateur
visuel ni de filtre naïf interdisant le mot « coffret » dans le nom commercial.

## Dépendances et limites de livraison

La V1 reste communale. L'[EPIC 67](../../roadmap/a-faire/epic-67-communautes-communes-coffrets-intercommunaux-backlog.md)
fera évoluer le contrat de territoire ; ne pas simuler une communauté avec un
`ville_id`. L'[évolution de l'EPIC 35](../../roadmap/terminees/epic-35-profils-backoffice-differencies-backlog.md)
imposera lecture seule au Lecteur et mutation métier au Backoffice, sans contourner
les communes autorisées. Elle n'est pas supposée déjà implémentée.

H01 est remplacée par D04 et H02 par D05 : le retour JSON avec image base64 et
la conservation de 30 jours sont validés. La fonctionnalité est désactivée par défaut,
avec migration additive v250 à appliquer avant activation. La documentation ne vaut
ni déploiement ni exécution du nettoyage sur un environnement partagé. Les preuves
et conditions de livraison figurent dans le document de vérification.
