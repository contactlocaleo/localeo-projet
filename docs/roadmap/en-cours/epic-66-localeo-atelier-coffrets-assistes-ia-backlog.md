# EPIC 66 — Localeo Atelier : composer des coffrets avec l'aide de l'IA

## Références

- Date de cadrage : **28 septembre 2026**.
- Identifiant : **EPIC-66**, disponible après recherche dans la roadmap commune,
  les namespaces applicatifs et les index documentaires des dépôts voisins.
- État produit : **En cours**, selon la [roadmap commune](../README.md).
- Demande : une application du backoffice pour sélectionner une commune et des
  prestations, générer un prompt IA, puis coller une réponse normalisée pour créer
  le coffret avec son contenu éditorial et sa vignette.
- Phase réalisée : **cadrage et spécification V1.1 du 29 septembre 2026**, dans le
  [dossier canonique](../../specifications/epic-66-localeo-atelier/README.md).
  Implémentation locale réalisée, validation en cours ; aucune clôture ni livraison déclarée.
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

**Inclus V1 :** entrée backoffice, sélection communale et versionnée, préparation
reprenable, prompt copiable, import normalisé avec prévisualisation, édition des
textes, ajout/choix de vignette et création d'un coffret brouillon avec sa composition.

**Exclusions :** appel automatique à un fournisseur IA, gestion de clés/facturation
IA, sélection intercommunale, génération en masse, modification d'un coffret déjà
vendu, écriture des prestations sources, calcul de prix/commission ou décision
fiscale par l'IA, activation automatique, nouvelle application à déployer séparément.

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
