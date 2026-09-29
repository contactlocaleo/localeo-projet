# EPIC 66 — Localeo Atelier : composer des coffrets avec l'aide de l'IA

## Références

Évolution complémentaire `PWA-20260929` : [installation dans le header et mise à jour explicite](../../specifications/installation-mise-a-jour-pwa.md). Ses critères et preuves sont transverses aux sept applications ; elle ne clôture pas l'EPIC 66.

- Date de cadrage : **28 septembre 2026**.
- Identifiant : **EPIC-66**, disponible après recherche dans la roadmap commune,
  les namespaces applicatifs et les index documentaires des dépôts voisins.
- État produit : **En cours**, selon la [roadmap commune](../README.md).
- Demande : une application du backoffice pour sélectionner une commune et des
  prestations, générer un prompt IA, puis coller une réponse normalisée pour créer
  le coffret avec son contenu éditorial et sa vignette.
- Phase réalisée : **cadrage et spécification V1.2 du 29 septembre 2026**, dans le
  [dossier canonique](../../specifications/epic-66-localeo-atelier/README.md).
  Socle V1.1 et extensions V1.2 implémentés et testés localement. Bilan de preuves
  et limites de recette dans le dossier canonique ; aucune clôture ni livraison déclarée.
- Extension du **29 septembre 2026**, `E66-PWA-20260929` : accès à Localeo Atelier
  comme application PWA et depuis le menu déroulant Applications de l'ERP.
  Implémentée en V1.2 ; recette d'installation sur appareils déployés restante.
- Précision du **29 septembre 2026**, `E66-PRIX-20260929` : le prix TTC proposé
  à la création est la somme des prix TTC des prestations sélectionnées ;
  l'opérateur peut le modifier. Implémentée et testée localement en V1.2.
- Précision utilisateur du **28 septembre 2026** : les visuels du coffret sont au
  format **WebP** et d'un poids **strictement inférieur à 150 Ko**.
- Choix validés par l'utilisateur le **28 septembre 2026** : nom **Localeo Atelier**,
  **contrat de réponse court**, **erreurs en français** et **reprise selon les droits ERP**.
- Précision du **29 septembre 2026** : le **même prompt produit toutes les
  informations éditoriales et l'image réelle du coffret encodée en base64 dans
  le JSON** ; un second prompt ou un fichier à ajouter séparément ne constitue
  pas le parcours attendu.
- Durée de conservation validée le **29 septembre 2026** : **30 jours après la
  dernière modification enregistrée**. Les coffrets créés et leur contenu restent
  conservés ; le nettoyage porte sur les préparations et médias de travail orphelins.
- Signature proposée : **« Composez vos coffrets,
  façonnez leur histoire. »** Le nom évoque la sélection et la composition d'une
  offre locale ; l'assistance IA est un moyen, pas un prérequis technique à comprendre.

### Rattachement et dépendances

L'[EPIC 60](../terminees/epic-60-vision-360-commercialisation-backlog.md) possède
déjà l'atelier coffret et le dossier ERP : création, composition, économie et
publication. Cette nouvelle epic ajoute un parcours de composition assistée par
une IA externe, avec prompt exportable et import contrôlé de sa réponse. Elle
réutilise le coffret canonique et ses services, sans rouvrir l'EPIC 60 ni recréer
l'EPIC 61 fusionnée. La fiche ERP existante reste la destination après création.

L'[EPIC 67 — Communautés de communes](../a-faire/epic-67-communautes-communes-coffrets-intercommunaux-backlog.md)
porte l'extension ultérieure au choix d'une communauté, à la sélection de ses
prestations et au contexte du prompt/import. Le présent cadrage conserve son
périmètre communal V1 ; la composition intercommunale n'est pas une capacité
déjà acquise d'Atelier.

Autres dépendances :

- [EPIC 1](../terminees/epic-1-gouvernance-du-referencement-commercant-et-prestation-backlog.md)
  pour les statuts et l'éligibilité des commerçants et prestations.
- [EPIC 28](../terminees/epic-28-calcul-reversement-coffret-backoffice-backlog.md)
  pour l'économie du coffret, selon les règles courantes du domaine.
- [EPIC 50](../terminees/epic-50-conformite-fiscale-bum-backlog.md) pour la qualification
  BUM et les exigences éditoriales/fiscales avant commercialisation.
- [EPIC 62](../a-faire/epic-62-validation-modifications-prestations-backlog.md), encore à faire,
  pour la future validation des modifications de prestations. Le périmètre V1
  d'Atelier n'en dépend pas pour créer un nouveau coffret à partir des versions
  autorisées ; il ne crée pas un circuit concurrent de modification des prestations.

## Problème et résultat attendu

**Besoin exprimé :** gagner du temps pour transformer une sélection de prestations
locales en une offre cohérente, attractive et prête à être finalisée. L'opérateur
veut utiliser l'IA de son choix, puis éviter de ressaisir manuellement sa proposition.

**Constat vérifié sur le code local**, backend `9b9cba3`, projet `3ddc144` :
le [service Atelier ERP](../../../../localeo-backend/app/application/commercialisation/services/atelier_erp.py)
et la [spécification ERP](../../specifications/epic-60-vision-360-commercialisation/specifications-fonctionnelles.md)
portent déjà la création et la composition des coffrets. Leur existence ne vaut
pas recette de l'environnement déployé. Ce constat décrit le point de départ avant implémentation du nouveau parcours IA.

Les [règles d'Atelier](../../../../localeo-backend/app/domaine/commercialisation/services/regles_atelier.py)
contrôlent déjà la commune, le budget disponible et le rattachement d'un modèle
actif dans sa version courante. Ce rattachement crée une copie de prestation,
liée à son modèle et sa version, sans modifier la source. Les
[API ERP](../../../../localeo-backend/app/api/erp_api.py) portent les habilitations,
la protection CSRF, l'idempotence et le dépôt d'images via le DAM.
Le [parcours de génération Animation](../../../../localeo-backend/app/application/animation_locale/services/contenu_generation.py)
fournit un précédent prompt/réponse versionné à étudier ; il est spécialisé
Animation et ne constitue pas un import de coffrets directement réutilisable.

**Acteur principal :** opérateur Localeo habilité à créer des coffrets dans le
backoffice, avec le périmètre territorial déjà autorisé. Aucun accès IA ou droit
de publication supplémentaire n'est accordé par cette nouvelle entrée.

**Exemple avant/après :** après avoir choisi trois prestations de Latresne,
l'opérateur copie un prompt contenant leurs références et descriptions. L'IA
produit le nom, l'accroche, la description, l'ordre de présentation et l'image
WebP encodée en base64 dans un seul JSON. L'opérateur colle cette réponse,
voit le coffret proposé, puis clique sur **Créer le
coffret** : le titre, la description et la composition sont renseignés sans
ressaisie dans un nouveau brouillon, accessible depuis sa fiche ERP habituelle.

## Parcours proposé

### 1. Composer

Depuis une entrée **Localeo Atelier** du backoffice, choisir une commune puis
les prestations de ses commerçants. Recherche et filtres facilitent la sélection ;
chaque ligne montre le commerçant, le contenu de la prestation et les informations
utiles à l'assemblage. Une prestation indisponible à la composition indique son
motif ; aucune promesse de vendabilité n'est déduite du seul fait de la sélectionner.
La sélection s'appuie sur les modèles actifs et leurs versions courantes autorisés
par le parcours de rattachement existant, et non sur la modification de copies
déjà incluses dans d'autres coffrets. Ce vocabulaire technique reste masqué derrière
une liste de prestations compréhensible pour l'opérateur.

Le récapitulatif affiche la sélection et les informations économiques calculées
par Localeo. Une intention facultative permet de préciser thème, public ou ton,
par exemple « une sortie gourmande à deux ». Les champs indispensables à la
création, dont le prix selon le parcours actuel, restent maîtrisés par l'opérateur.

Proposition V1 : **une sélection produit un coffret comprenant toutes les
prestations choisies**, une seule fois chacune. L'IA peut proposer leur ordre de
présentation ; elle ne peut ni en ajouter ni en retirer. Changer la sélection
demande de régénérer le prompt. La création en série reste hors périmètre.

### 2. Façonner avec l'IA

Une action **Copier le prompt** fournit un texte complet prêt à coller dans l'IA
choisie par l'opérateur. Pas de téléchargement de fichier ni de paramétrage de
modèle obligatoire. Le prompt inclut les faits utiles autorisés, les contraintes
éditoriales Localeo et le format exact de réponse attendu.

Le retour demandé est un **objet JSON versionné**, avec une référence à la
préparation, à la commune et aux prestations/version sélectionnées. Il contient :

- le nom du coffret et une accroche courte ;
- sa description, cohérente avec les prestations et la promesse réellement offerte ;
- l'ordre proposé des références sélectionnées ;
- l'image WebP encodée en base64, son type MIME et son texte alternatif.

**La réponse complète est un JSON unique contenant l'image réelle en base64**.
Le prompt demande de générer la vignette, d'encoder ses octets réels et de les
intégrer au JSON, sans fichier séparé ni instructions pour une seconde génération.

Les consignes visuelles du prompt rappellent le format **WebP** et la limite de
**moins de 150 Ko**. Cette consigne ne remplace pas le contrôle du fichier réel.

**Précision utilisateur du 29 septembre 2026 — E66-EXPERIENCE-20260929 :**
le prompt doit explicitement définir le coffret comme une **expérience réunissant
plusieurs prestations physiques, vécues sur place auprès des commerçants**, et
non comme un objet matériel. Il demande une image de l'expérience proposée,
sans boîte, coffret cadeau, panier garni ou emballage représentant le produit vendu.
Cette exigence est cadrée ci-dessous et reste à intégrer au générateur de prompt.

Le contrat de réponse reste **court**, limité aux informations utiles à l'import
et aux références nécessaires aux contrôles. Ce principe est validé ; les champs
éditoriaux canoniques, le format définitif et leurs limites seront
spécifiés avant implémentation. L'opérateur n'a pas à écrire ou corriger du JSON.
Les instructions interdisent d'inventer une prestation, une valeur financière,
une disponibilité, une certification ou un engagement absent des faits fournis.

### 3. Importer et créer

L'opérateur colle la réponse dans **Coller la réponse de l'IA**. Une prévisualisation
lisible restitue titre, description, composition et image décodée ; les
textes restent modifiables avant création. Les erreurs sont présentées **en français**,
avec une explication compréhensible et l'action corrective attendue. Une erreur de format explique ce qui
manque et permet de recoller une réponse sans perdre la sélection.

Le retour s'importe par **Coller la réponse de l'IA**, sans dépôt de fichier requis.
Localeo décode le base64, contrôle les octets WebP et enregistre le média dans le
DAM avec la proposition, en une transaction. Un refus ne laisse ni proposition
partielle ni média orphelin. La bibliothèque reste un remplacement volontaire après
import. Une description, un second prompt, une URL ou un base64 invalide ne remplace
pas une image. Une préparation incomplète peut être sauvegardée ; l'import complet
et la création exigent un visuel conforme au contexte courant.
Aucune URL fournie par l'IA ne déclenche un téléchargement arbitraire côté serveur.

**Contrainte acquise sur les visuels :** tout fichier joint ou média existant
retenu pour ce parcours doit être une image **WebP valide**, de taille strictement
inférieure à **150 Ko**. Convention de mesure du cadrage : 1 Ko = 1 000 octets,
donc **moins de 150 000 octets décodés** ; un fichier de 150 000 octets est refusé.
La chaîne base64 est plus volumineuse que l'image : le seuil porte sur le WebP,
pas sur le JSON, dont le contrat prévoit une limite de transport distincte.
Le serveur contrôle le format réel et le poids, sans se fier uniquement à
l'extension ou au type annoncé. Un autre format, un fichier illisible ou un poids
égal/supérieur à la limite produit un message compréhensible et empêche le
rattachement du visuel ; la préparation reste conservée. Le choix dans le DAM
est soumis aux mêmes contrôles que le dépôt. Aucune conversion automatique ni
migration des médias déjà utilisés par d'autres coffrets n'est supposée acquise.

**Créer le coffret** constitue la validation explicite de la proposition affichée.
Cette action crée automatiquement le brouillon et sa composition, rattache le
média disponible, puis ouvre sa fiche ERP. Elle n'active ni le coffret ni ses
prestations. Les vérifications métier et la publication restent celles du parcours
existant. Le travail de préparation peut être enregistré et repris **selon les
droits ERP en vigueur au moment de la reprise**, y compris son périmètre territorial.
L'enregistrement d'une préparation ne confère aucun droit supplémentaire à son
auteur ou à un autre opérateur.

Sur ordinateur, la largeur disponible sert à conserver la sélection et l'aperçu
côte à côte ; sur écran étroit, le même parcours s'affiche dans l'ordre de lecture.
Les contrôles et erreurs restent accessibles au clavier, sans dépendre du survol.

## Périmètre

**Inclus socle V1.1 :** entrée backoffice, sélection communale et versionnée, préparation
reprenable, prompt copiable, import normalisé avec prévisualisation, édition des
textes, ajout/choix de vignette et création d'un coffret brouillon avec sa composition.

**Exclusions :** appel automatique à un fournisseur IA, gestion de clés/facturation
IA, sélection intercommunale, génération en masse, modification d'un coffret déjà
vendu, écriture des prestations sources, calcul de prix/commission ou décision
fiscale par l'IA, activation automatique, nouvelle application à déployer séparément.

L'extension `E66-PWA-20260929` ajoute une application PWA identifiable et installable,
servie par le backend existant. L'exclusion d'un déploiement séparé demeure ; elle
n'exclut plus une présentation autonome d'Atelier.

**Contraintes :** réutiliser le socle ERP et les règles backend. Le prompt est
exporté manuellement et ne contient ni secret, jeton, coordonnées personnelles
non nécessaires, données d'achat ou paramètres financiers internes. La réponse
collée est une donnée non fiable : validation côté serveur, contenu affiché sans
exécution de HTML/script, refus des références inventées et des champs d'autorité
(statut, droits, validation BUM, montants) non prévus par le contrat.

## Critères d'acceptation

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E66-CA-01 | Opérateur authentifié et habilité | Ouvrir Atelier, choisir une commune | Seules les communes et actions autorisées sont accessibles ; un appel direct hors périmètre est refusé. |
| E66-CA-02 | Commune sélectionnée | Rechercher et sélectionner des prestations | Le commerçant, la version et le contenu sont identifiables ; les références hors commune, indisponibles ou dupliquées sont refusées avec un motif. |
| E66-CA-03 | Sélection valide non vide | Copier le prompt | Une seule demande exige nom, accroche, description, ordre, texte alternatif et génération effective d'une image WebP < 150 Ko intégrée en base64 dans un JSON unique/versionné, sans fichier séparé ni second prompt à exécuter ni donnée personnelle ou secrète inutile exportée. |
| E66-CA-04 | Préparation et réponse compatible | Coller uniquement le JSON complet | L'aperçu affiche nom, accroche, description, ordre des prestations et image réellement décodée sans ressaisie ni upload séparé ; import proposition/média atomique, aucun coffret n'est encore créé. |
| E66-CA-05 | Réponse mal formée, incomplète ou d'une autre préparation | Importer | Message compréhensible en français avec action corrective, sélection conservée et aucune écriture partielle ; version inconnue, prestation ajoutée/omise, doublon, champ interdit, base64 invalide ou image non conforme sont refusés. |
| E66-CA-06 | Aperçu valide | Modifier les textes et joindre/choisir une image | L'aperçu reflète les changements ; média autorisé, WebP valide et strictement inférieur à 150 000 octets, texte alternatif disponible. Format réel non conforme, fichier illisible ou taille égale/supérieure refusés côté serveur, y compris pour un média DAM existant ; préparation conservée. Absence d'image ou image non confirmée pour le contexte courant bloque la création complète, sans empêcher la sauvegarde de préparation. |
| E66-CA-07 | Proposition relue et champs obligatoires renseignés | Créer le coffret | Un seul coffret BROUILLON est créé avec les prestations sélectionnées et le contenu validé ; lien vers sa fiche ERP, aucune publication implicite. |
| E66-CA-08 | Création en cours ou réponse réseau incertaine | Répéter le clic ou reprendre la demande | Pas de double coffret ni de composition partielle ; résultat retrouvé ou échec explicite, création transactionnelle et reprise idempotente. |
| E66-CA-09 | Version, statut ou rattachement communal changé depuis le prompt | Importer puis créer | Recontrôle serveur des sources et permissions ; refus d'une sélection périmée, liste des éléments à revoir et régénération proposée, sans mise à jour silencieuse. |
| E66-CA-10 | Coffret créé par Atelier | Consulter son diagnostic puis demander sa publication | Mêmes règles de prix, reversement, droits, BUM et vendabilité que les autres coffrets ; l'origine IA ne valide ni n'exempte aucun contrôle. |
| E66-CA-11 | Préparation sauvegardée ou créée | Reprendre et consulter l'historique, puis atteindre l'échéance | Reprise selon les droits ERP actuels pendant 30 jours après dernière modification ; lecture/retry ne prolongent pas le délai. Préparation non créée expirée non reprenable ; contenu préparatoire nettoyé, coffrets créés, médias utilisés et résultat durable d'unicité préservés. Origine et lien coffret traçables, sans journalisation indiscriminée du texte collé. |
| E66-CA-12 | Ordinateur ou écran étroit, usage clavier | Effectuer le parcours complet | Actions principales visibles, ordre lisible, aperçu utilisable, retours de chargement et erreurs en français ; aucune édition technique du JSON obligatoire. |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Applications et domaine propriétaire | **Concerné : backend/ERP**, orchestration du parcours et interface. Le domaine commercialisation conserve la création, composition et publication ; référencement porte les sources autorisées. Réutiliser le service Atelier existant. |
| Autres applications | **Concernée : Marketplace**, affichage des nouveaux champs éditoriaux, texte alternatif et ordre des prestations ; repli conservé pour les anciens coffrets. Commerçant, Animation et Live ne reçoivent pas de parcours IA V1 ; non-régression sur leurs contrats partagés. Aucun nouveau dépôt. |
| API et consommateurs | **Concerné :** contrat interne versionné prompt/réponse/import, validation et habilitations serveur ; dépôt et sélection DAM contrôlent le format WebP réel et la taille strictement inférieure à 150 000 octets. Champs optionnels additifs dans les projections publiques, règles des autres parcours DAM conservées. [Contrats et schéma V1](../../specifications/epic-66-localeo-atelier/contrats.md) implémentés localement, en validation. |
| Persistance, migrations et données existantes | **Concerné :** préparation reprenable, contexte/version, résultat durable unique, origine, nouveaux champs éditoriaux et ordre des prestations. Migration additive v250 présente dans le dépôt et décrite dans la spécification ; aucune conversion des coffrets ou achats existants, aucune migration exécutée. |
| Générateur de démonstration et fixtures | **Concerné pour les preuves :** commune avec prestations éligibles/non éligibles, réponses IA fictives valides/invalides, source devenue obsolète, média absent et reprise. Prévoir des WebP valides sous le seuil, au seuil de 150 000 octets et au-dessus, un autre format renommé `.webp`, un fichier illisible et un média DAM non conforme. Aucun appel IA réel ; adapter le générateur seulement si les nouvelles données persistées le nécessitent. |
| Documentation fonctionnelle | **Concerné :** guide backoffice, parcours de composition, exemple copiable et aide sur les erreurs ; préciser brouillon versus publication et proposition visuelle versus fichier image. |
| Exploitation et déploiement | **Concerné :** limites de taille, expiration à 30 jours, nettoyage automatique borné, audit, diagnostic d'échec et migrations. Sans clé IA ni génération automatique côté Localeo ; pas d'intervention sur les environnements réels à cette phase. |

## Arbitrages et spécification V1

Le [dossier du 29 septembre](../../specifications/epic-66-localeo-atelier/README.md)
distingue les choix validés et les choix de conception. La précision du 29 septembre
remplace H01 par D04 : un prompt unique produit un JSON contenant l'image réelle
en base64 ; le DAM reste
un remplacement volontaire. H02 est remplacée par D05 : conservation validée à
30 jours après dernière modification ; expiration et nettoyage implémentés localement, en validation.
Le nom, le contrat court, les erreurs en français, les droits ERP et le format/poids
des visuels ainsi que la conservation de 30 jours sont acquis.

L'entrée Commercialisation, les champs et limites, les permissions par opération,
le contrat fermé, la création atomique en brouillon et les adaptations des lecteurs
sont spécifiés. La [matrice de preuves](../../specifications/epic-66-localeo-atelier/verification-livraison.md)
relie les douze critères aux preuves de validation et aux impacts de déploiement.
L'état produit est **En cours** au 29 septembre 2026 : implémentation locale
réalisée et validation en cours. Le bilan de preuves est maintenu dans le dossier
de spécification ; ce passage ne vaut ni clôture ni déploiement.

## Extension du 29 septembre 2026 — Localeo Atelier en PWA

Référence stable : **E66-PWA-20260929**. Demande utilisateur : disposer de Localeo
Atelier comme application PWA, à l'image de Localeo Control et Localeo Support,
et l'ouvrir depuis la liste déroulante des applications disponibles dans l'ERP.
L'epic reste **En cours** ; aucun nouvel identifiant ni dépôt n'est nécessaire.

### Problème et résultat attendu

**Constat vérifié dans le backend `a28592d` :** les routes
`/internal/erp/atelier` et `/internal/erp/atelier/preparations/{id}` servent la
coquille ERP via [erp_ui.py](../../../../localeo-backend/app/api/erp_ui.py).
Le [menu partagé Applications](../../../../localeo-backend/app/infrastructure/erp/app-header.js)
ne référence pas Atelier. La navigation latérale ERP comporte déjà un lien Atelier.
[Support](../../../../localeo-backend/app/api/support_ui.py) et
[Control](../../../../localeo-backend/app/api/pwa_exploitation_api.py) possèdent un
manifeste avec une ouverture autonome. Ce constat de code n'est pas une recette
de leur installation sur tous les navigateurs.

**Acteur :** opérateur habilité à utiliser Atelier, avec ses droits ERP actuels.
Depuis « Applications », il choisit **Localeo Atelier**, retrouve directement ses
préparations et peut installer l'application sur son appareil lorsque le navigateur
le permet. Une fois installée, elle s'ouvre sous son propre nom et son icône, avec
une navigation centrée sur la composition de coffrets et un retour explicite à l'ERP.
Les préparations sont les mêmes depuis l'ERP et depuis l'application installée.

### Périmètre et contraintes

- Une entrée applicative dédiée avec identité **Localeo Atelier**, icônes,
  manifeste et ouverture autonome ; présentation adaptée à l'ordinateur et au mobile.
- Un lien **Localeo Atelier** dans le menu déroulant Applications de l'ERP ;
  cohérence avec le menu partagé et les autres accès Atelier déjà présents.
- Un accès direct aux préparations enregistrées et un retour à la fiche ERP du
  coffret créé, sans dupliquer le parcours métier ni les données.
- Réutilisation de la session backoffice, des permissions et du périmètre communal.
  Le flag `LOCALEO_FEATURE_ATELIER_COFFRETS_ENABLED` reste la condition d'activation.
- Proposition de cadrage : **usage métier en ligne**. Une coupure affiche un état
  compréhensible et permet de réessayer ; aucune file de commandes métier hors
  connexion, aucun rejeu automatique de création, aucun cache persistant des
  préparations, prompts, réponses IA ou données authentifiées.
- Les douze critères initiaux restent applicables, dont idempotence, conservation
  de 30 jours, import WebP/base64 et création en brouillon sans publication implicite.

**Exclus :** application native ou publication dans un store, nouveau compte,
nouveau rôle, notifications push, fournisseur IA intégré, nouveau domaine métier,
nouveau dépôt ou déploiement autonome. L'évolution des profils reste portée par
l'EPIC 35 ; la PWA ne lui attribue pas de droits anticipés.

### Critères ajoutés

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E66-CA-13 | Opérateur habilité, Atelier activé | Ouvrir le menu déroulant Applications de l'ERP et choisir Localeo Atelier | Une entrée unique, utilisable au clavier et sur mobile, ouvre l'application dédiée. Les accès Atelier existants conduisent au même parcours et les autres applications restent accessibles. |
| E66-CA-14 | Navigateur compatible avec l'installation PWA, environnement HTTPS | Installer puis relancer Localeo Atelier | Nom et icône propres, ouverture autonome sur Atelier ; aucune installation obligatoire pour l'usage web. Si l'installation n'est pas proposée par le navigateur, le parcours web reste utilisable. |
| E66-CA-15 | Préparation enregistrée et accès autorisé | Ouvrir son lien direct, actualiser, puis la reprendre dans la PWA | Même préparation et même état serveur ; navigation adaptée à la largeur, retour ERP accessible et ouverture de la fiche canonique après création. Aucun doublon ni copie locale concurrente. |
| E66-CA-16 | Session absente, expirée ou droits retirés ; ou Atelier désactivé | Ouvrir l'application ou son lien direct, y compris depuis une installation existante | Connexion requise ou refus explicite selon le cas ; contrôle serveur inchangé et aucune donnée protégée affichée depuis un cache. Le menu ne propose pas un accès utilisable lorsque la fonctionnalité est désactivée ou les droits insuffisants. |
| E66-CA-17 | Application ouverte, coupure réseau ou nouvelle version disponible | Tenter une action puis retrouver la connexion ; reprendre après mise à jour | État explicite en français, aucune fausse confirmation ni création différée automatique. Reprise fondée sur l'état serveur et l'idempotence existante ; une mise à jour ne recharge pas silencieusement un formulaire non enregistré. Le mécanisme PWA ne contrôle ni ne met en cache les autres applications. |

### Analyse d'impact initiale

Les mentions « à examiner » ci-dessous conservent la trace du cadrage initial.
La V1.2 du dossier canonique arrête désormais les routes PWA, la politique de
session/cache et les preuves ; le tableau ne constitue pas un second contrat.

| Sujet | Impact et travail attendu |
| --- | --- |
| Applications et propriétaire | **Concerné : backend**, interface Atelier, navigation ERP partagée et distribution PWA. Commercialisation reste propriétaire des règles ; réutiliser les services existants. Aucun changement fonctionnel attendu dans Marketplace, Commerçant, Animation ou Live. |
| API et consommateurs | **Concerné :** nouvelles ressources de présentation PWA et gestion de session/liens directs. Réutiliser le contrat métier Atelier sans variante mobile. Vérifier la compatibilité des anciennes URL et les menus partagés de Support, Ops, OnBoard et ERP. |
| Persistance et migrations | **Sans nouvelle donnée métier attendue :** mêmes préparations et coffrets. Aucune migration prévue pour ce seul accès PWA ; à confirmer en conception. Ne pas modifier la migration 250 déjà appliquée en test. |
| Démonstration et fixtures | **Concerné pour les preuves :** scénario existant Atelier accessible par menu et lien direct, profils autorisé/refusé, flag désactivé, session expirée et réseau coupé. Aucun nouveau jeu métier ni génération distante nécessaire au cadrage. |
| Documentation fonctionnelle | **Concerné :** compléter la spécification et le guide Atelier avec l'ouverture, l'installation facultative, le retour ERP et la reprise ; conserver une seule source canonique. |
| Exploitation et livraison | **Concerné :** ressources HTTPS, identité/manifeste, périmètre du mécanisme PWA, politique de cache, mise à jour et non-régression entre applications. Même déploiement backend ; aucune activation d'environnement à cette phase. |

### Spécification de l'extension PWA

Le [dossier V1.2](../../specifications/epic-66-localeo-atelier/README.md) précise
l'URL `/internal/atelier/`, les redirections des anciens liens, le retour de
connexion validé, le manifeste, les contrôles d'accès et le worker sans cache
de données métier. Les preuves navigateur sont planifiées dans la matrice canonique.
Les critères E66-CA-13 à 17 sont **implémentés et vérifiés localement**, avec les
limites de recette du bilan V1.2 ; le contrôle Chromium local ne prouve pas
l'installation effective sur tous les appareils cibles.

## Extension du 29 septembre 2026 — Prix TTC proposé automatiquement

Référence stable : **E66-PRIX-20260929**. Le besoin prolonge la création de coffrets
dans Localeo Atelier, accessible depuis l'ERP et la future PWA. L'epic reste
**En cours** ; les autres parcours de modification d'un coffret existant ne sont
pas transformés implicitement.

### Besoin et règle cible

**Demande acquise :** proposer automatiquement un prix TTC égal à la somme des
prix TTC des prestations sélectionnées, avec possibilité de le modifier.
Exemple : des prestations de **25 €**, **40 €** et **15 €** proposent un coffret
à **80 € TTC** ; l'opérateur peut saisir **75 € TTC**, sous réserve des contrôles
économiques existants.

**Constat vérifié sur le backend `a28592d` :** la préparation contient un prix
en centimes saisi par l'opérateur. Les sources portent une valeur TTC
`valeur_centimes` et un reversement distinct. Les
[règles d'Atelier](../../../../localeo-backend/app/domaine/commercialisation/services/regles_atelier.py)
exigent un prix positif couvrant le total des reversements. Le prix proposé
utilise la **valeur TTC des versions de prestations sélectionnées**, une fois
par prestation ; il ne somme ni les reversements ni les commissions.

**Comportement proposé pour les changements de sélection :** tant que le prix
n'a pas été personnalisé, l'ajout ou le retrait d'une prestation actualise le
prix proposé. Après une saisie manuelle, conserver ce prix et afficher séparément
le nouveau total des prestations ; une action **Utiliser le total des prestations**
permet de revenir au calcul automatique. Sauvegarder puis reprendre une préparation
conserve ce choix. Une modification des tarifs sources suit le contrôle de version
existant : aucun changement silencieux de prix ou de sélection enregistrée.

La règle appartient au domaine commercialisation ; les interfaces présentent
le résultat et les services applicatifs orchestrent son calcul et sa sauvegarde.
L'IA ne fixe aucun montant. Le prix confirmé reste celui utilisé pour créer
le coffret ; les règles existantes d'invalidation du contexte du prompt lors d'un
changement de prix ou de sélection restent applicables.

### Critères ajoutés

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E66-CA-18 | Nouvelle préparation, prestations aux valeurs TTC connues | Sélectionner les prestations puis en ajouter ou retirer une, sans personnaliser le prix | Prix TTC prérempli et actualisé à leur somme exacte en centimes, sans cumul de doublons ni approximation flottante. Aucun tarif absent ne devient implicitement zéro ; une sélection vide ne permet pas de créer un coffret. |
| E66-CA-19 | Prix proposé automatiquement | Saisir un prix différent puis modifier la sélection, sauvegarder et reprendre | Prix personnalisé conservé et total des prestations visible séparément. « Utiliser le total des prestations » rétablit le prix calculé et ses actualisations ultérieures. |
| E66-CA-20 | Prix proposé ou personnalisé | Confirmer la création depuis l'ERP ou la PWA | Prix confirmé utilisé pour le brouillon ; mêmes contrôles serveur de droits, versions, limites monétaires et budget. Prix nul/négatif ou inférieur aux reversements refusé en français, sans écriture partielle ni prix corrigé silencieusement. |
| E66-CA-21 | Tarif source modifié depuis la préparation ou coffret déjà créé | Reprendre la préparation puis tenter de créer ; consulter un coffret existant | Sources périmées signalées et revalidation requise selon le parcours existant ; aucun recalcul rétroactif des coffrets, achats ou prix déjà enregistrés. |

### Impacts et passage à la spécification

Les impacts initialement ouverts ci-dessous sont résolus dans la V1.2 canonique :
champs HTTP additionnels, métadonnées JSONB compatibles et aucune nouvelle migration
SQL. Le détail contractuel se lit dans le dossier de spécification.

| Sujet | Impact initial |
| --- | --- |
| Applications et domaine | **Concerné : backend/ERP et future PWA Atelier**, calcul métier partagé et affichage du prix/total. Pas de modification des prix dans les lecteurs Marketplace, Commerçant, Animation ou Live : ils continuent à utiliser le prix canonique du coffret. |
| Contrats et persistance | **À spécifier :** distinguer calcul automatique et prix personnalisé, exposer le total, conserver ce choix à la reprise. Examiner la compatibilité des préparations existantes en préservant leur prix, sans déduire leur mode de la seule égalité avec le total. Migration éventuelle à déterminer ; ne pas modifier v250 déjà appliquée en test. Le JSON IA n'acquiert aucun champ financier. |
| Démonstration et preuves | **Concerné :** sommes avec centimes, ajout/retrait, personnalisation puis retour au total, reprise, budget insuffisant et tarif source périmé. Adapter les fixtures ; aucune génération réelle requise au cadrage. |
| Documentation et exploitation | **Concerné :** compléter les spécifications et l'aide Atelier, préciser le comportement des préparations existantes et l'ordre de livraison si le contrat ou le stockage évolue. Aucun fournisseur ou secret supplémentaire. |

La V1.2 retient la conservation du prix personnalisé et l'action de retour au total
comme choix de conception. Elle spécifie modes AUTO/MANUEL, compatibilité des
anciennes préparations, calcul serveur et contrats additionnels ; aucune migration
SQL nouvelle n'est nécessaire. Les critères E66-CA-18 à 21 sont **implémentés et
testés localement** ; les nouvelles preuves sont consignées dans le bilan V1.2.

## Précision du 29 septembre 2026 — Représenter une expérience, pas une boîte

Référence stable : **E66-EXPERIENCE-20260929**. Besoin utilisateur acquis : éviter
que le mot « coffret » conduise l'IA à représenter un produit physique à recevoir.
Le coffret Localeo regroupe plusieurs prestations réelles chez les commerçants ;
il n'est pas lui-même une boîte ou un colis. Le nom métier « coffret » est conservé.

**Constat vérifié sur le backend `a28592d` :** le
[générateur de prompt](../../../../localeo-backend/app/domaine/commercialisation/services/preparation_coffret_assiste.py)
demande un coffret cohérent et son image réelle, sans expliciter cette distinction.
Le cadrage renforce E66-CA-03 ; il ne constate pas qu'une image incorrecte a été
produite sur un environnement déployé.

**Consigne cible à intégrer explicitement au prompt :**

> Le coffret Localeo n'est pas un objet physique : c'est une expérience composée
> de plusieurs prestations à vivre sur place auprès des commerçants sélectionnés.
> Ne représente pas de boîte, de coffret cadeau, de panier garni, de colis ou
> d'emballage comme s'il s'agissait du produit vendu. Illustre l'expérience et
> les activités réellement proposées par les prestations sélectionnées, avec une
> scène ou une composition cohérente. N'invente pas d'activité, d'objet offert,
> de livraison ou d'avantage absent de la sélection. Le titre, la description et
> le texte alternatif doivent eux aussi présenter une expérience, sans promettre
> un coffret matériel à recevoir.

Les objets effectivement nécessaires aux prestations peuvent être représentés
(par exemple un plat pour un repas ou des outils pour un atelier). L'interdiction
porte sur la présentation du coffret lui-même comme marchandise emballée ; elle
n'interdit pas de montrer le contenu réel d'une prestation sélectionnée.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E66-CA-22 | Préparation valide, toute sélection de prestations | Copier le prompt | Le texte contient explicitement la définition d'expérience multi-prestations sur place et l'interdiction de représenter un coffret matériel ; ces consignes demeurent présentes même si une intention libre demande une boîte cadeau. Les faits de la sélection restent des données, pas des instructions remplaçant ces règles. |
| E66-CA-23 | Réponse IA importée | Examiner le visuel et les textes avant création | L'aperçu permet de vérifier leur cohérence avec l'expérience et les prestations choisies. Une représentation de boîte vendue ou une promesse de livraison n'est pas conforme au résultat attendu ; l'opérateur peut refaire générer la proposition avant confirmation. Aucun contrôle automatique de la signification d'une image n'est prétendu acquis par sa seule validation WebP. |

**Impacts :** backend, consignes du prompt et tests de leur présence/priorité ;
spécification et aide de relecture Atelier à compléter. Prévoir des fixtures
illustrant une expérience conforme et une boîte non conforme, sans appel IA réel
obligatoire. Le format JSON, le WebP < 150 Ko en base64, les droits et les règles
de création restent inchangés. Aucune migration, nouveau service d'analyse d'image
ou modification des coffrets déjà créés n'est prévu. Les autres applications
continuent à lire les contenus canoniques, sans nouveau contrat consommateur.

Pas d'arbitrage produit ouvert. Cette précision est **implémentée en V1.2** :
template `atelier-coffret-v2`, contrat JSON de réponse V1 inchangé,
relecture guidée de l'aperçu. Les preuves prévues distinguent contenu du prompt
réellement généré et relecture du résultat visuel ; aucune obéissance universelle
d'une IA externe n'est supposée.
