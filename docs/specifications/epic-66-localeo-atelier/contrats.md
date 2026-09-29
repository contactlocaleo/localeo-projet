# Localeo Atelier — Contrats V1

[Vue fonctionnelle](README.md) · [Invariants et transaction](architecture.md)

## Sources, producteurs et consommateurs

Ce document et le [schéma JSON](reponse-ia.schema.json) sont les sources canoniques
du contrat, avec un [exemple fictif](reponse-ia.exemple.json). Le backend produit
le prompt et valide la réponse ; l'ERP affiche et colle ; l'IA externe est un
producteur de contenu non fiable, sans accès aux API. Aucun SDK IA n'est nécessaire.

Les nouvelles routes utilisent un parseur JSON strict dans `atelier_assiste_api.py`,
les règles pures de préparation et l'adaptateur `reponse_atelier.py` : clés dupliquées,
champs inconnus et coercitions de types ne sont pas admis. Les commandes ERP
existantes restent décrites par Pydantic et reçoivent les champs éditoriaux optionnels.
Pour contrôler la surface OpenAPI, réutiliser l'
[export hors ligne](../../../../localeo-backend/scripts/documentation/export_openapi_offline.py)
pour la documentation des routes, sans charger `.env` ni importer l'application
avec le bootstrap opérateur. La [vue OpenAPI Atelier](openapi.json) est générée
hors ligne depuis les neuf chemins implémentés par
[`generate_epic66_openapi.py`](../../../../localeo-backend/scripts/documentation/generate_epic66_openapi.py).
Les commandes JSON possèdent un schéma fermé dans cette vue ; le parseur borné
et le domaine restent les contrôles d'exécution.
Si une copie du schéma est embarquée dans l'ERP, documenter la synchronisation et
tester son empreinte ; ne pas maintenir deux définitions indépendantes.

## Réponse IA courte

Version V1 : objet JSON unique avec tous les champs suivants, sans champ supplémentaire :

| Champ | Type et limite | Règle |
| --- | --- | --- |
| `schema_version` | chaîne constante `"1"` | Refuser une autre version. |
| `preparation_id`, `contexte_id`, `ville_id` | UUID | Recopier les valeurs du prompt, confronter au contexte serveur. |
| `nom` | texte 1..200 | Nom proposé, éditable. |
| `accroche` | texte 1..160 | Une phrase courte. |
| `description` | texte 1..4 000 | Texte éditorial en français, plain text, paragraphes permis. |
| `prestations` | tableau de 1..20 objets `{modele_id, version}` | Ordre de présentation. Tous les modèles sélectionnés exactement une fois ; version entière >= 1, stricte, sans coercition. |
| `visuel` | objet fermé | `mime_type: "image/webp"`, `contenu_base64` et `texte_alternatif` 1..180 décrivant l'image réelle. Ni second prompt, ni URL, ni référence DAM reçue de l'IA. |

La **réponse complète** de l'IA est ce **JSON unique avec les octets du WebP en
base64** : aucun transfert séparé demandé à l'opérateur. `contenu_base64` est
une chaîne base64 standard canonique (alphabet ASCII, padding si nécessaire,
sans espaces/sauts de ligne ni préfixe `data:`), longueur 4..200 000 caractères.
Décoder strictement, vérifier que le réencodage canonique est identique, puis
contrôler le nombre réel d'octets : **1..149 999**, jamais le poids de la chaîne.
Une chaîne de 200 000 caractères peut représenter un fichier trop lourd : la
borne de schéma seule ne suffit pas. Vérifier WebP réel et décodage d'image sous
limites de ressources avant tout stockage. La V1.1 remplace le champ de second prompt de la V1
documentaire non implémentée ; `schema_version: "1"` reste la première version à livrer.

Le JSON Schema contrôle structure et bornes. Le domaine contrôle les UUID exacts,
la fraîcheur, les versions, doublons et l'ensemble de sélection. Rejeter également
les clés JSON dupliquées, racines multiples, valeurs non finies et chaînes vides
après trim. Textes interprétés comme texte simple, rendus échappés ; ne jamais
exécuter ou injecter du HTML/Markdown fourni. Les erreurs visibles sont en français.
Les références ne doivent pas être considérées comme secrètes ni comme une preuve
d'autorisation. Un JSON syntaxiquement valide n'est pas forcément recevable.

Réponse collée limitée à **262 144 octets UTF-8** (256 Kio), mesurés avant parsing ; profondeur
maximale 8 après retrait éventuel d'une unique clôture Markdown. Le contrat court
ne peut contenir de champs prix/reversement/commission, statut, promesse garantie,
contenu indicatif, qualification, droits ou destinataires. Un champ inconnu est
refusé, même si le reste de la réponse est utilisable.

### Construction du prompt

Template V1.1 implémenté `atelier-coffret-v1` ; cible V1.2
`atelier-coffret-v2`, assemblée côté serveur. Le JSON de réponse conserve
`schema_version: "1"` : seuls les instructions et le numéro du template évoluent.
Les anciens prompts sauvegardés restent lisibles ; une réémission explicite crée
un nouveau contexte V2 et invalide l'ancienne proposition. Ne pas remplacer le
texte d'un contexte déjà émis dans un GET. L'absence de version de template dans
un ancien contexte désigne V1 ; les nouvelles émissions stockent `template_version`.

L'interface identifie un prompt historique V1 et propose **Actualiser le prompt**
avant de le copier dans le nouveau parcours. Cette action avertit de l'invalidation
de l'aperçu puis émet explicitement V2. La simple consultation de l'historique ne
réécrit rien ; une réponse V1 déjà attendue reste importable si son contexte et
ses sources sont valides, avec le rappel de relecture expérience dans l'aperçu.

Contenu du template :

1. Mission en français : proposer un coffret cohérent à partir des seules
   prestations sélectionnées, sans inventer bénéfice, certification ou engagement.
2. Identifiants de préparation/contexte/commune et nom public de la commune.
3. Liste des références/version, nom public du commerce, libellé et description
   publique de la prestation. Ne jamais copier des champs de contact, notes
   internes, achats, coordonnées personnelles, URLs privées ou paramètres financiers.
4. Intention facultative saisie par l'opérateur, distincte des instructions système.
5. Contraintes de texte, sélection exacte et **génération effective** d'une vignette
   WebP < 150 Ko, cohérente avec les prestations ; ne pas répondre par un autre prompt.
6. Gabarit JSON avec IDs déjà remplis et `visuel.contenu_base64`, demandé comme
   unique résultat à coller. Aucune pièce jointe séparée ni prose supplémentaire.

Instruction explicite du template : « Produis maintenant le nom, l'accroche,
la description et l'ordre des prestations du coffret, ainsi que son image réelle.
Encode les octets réels du WebP de moins de 150 000 octets en base64 et place-les
dans `visuel.contenu_base64`, avec `mime_type: image/webp` et son texte alternatif.
Rends uniquement le JSON conforme, sans URL, pièce jointe séparée ou prompt pour
générer l'image ultérieurement. N'invente pas la chaîne base64. »
Cette instruction n'est pas une garantie des capacités de tous les fournisseurs ;
un retour incomplet n'est jamais considéré comme une génération complète.

Projection de champs explicitement autorisés, jamais sérialisation ORM générique.
Les valeurs financières et montants du prix ne sont pas exportés. Les textes
libres doivent être relus dans l'aperçu « Données transmises à votre IA » : la liste
blanche de champs ne garantit pas qu'un texte saisi ne contienne pas de donnée
personnelle. Bloquer les URLs et chaînes de contact manifestes (email/téléphone)
d'après un contrôle dédié à cette projection, puis permettre de corriger les données ou retirer
l'intention ; ne jamais exporter silencieusement un texte détecté. Cette détection
ne prétend pas identifier tout secret arbitraire. Ne pas altérer les prestations
sources à partir du prompt pour résoudre ce refus.

Le prompt est borné à **131 072 octets UTF-8**. En cas de dépassement, afficher
« La sélection contient trop de texte pour ce prompt » ; ne pas tronquer une
condition importante d'une prestation ni supprimer silencieusement un élément.
Les textes fournis sont délimités comme données et ne peuvent modifier le schéma.

**Instruction normative V2**, présente avant les données et rappelée après leur
bloc, à chaque génération (E66-CA-22) :

> Le coffret Localeo n'est pas un objet physique : c'est une expérience composée
> de plusieurs prestations à vivre sur place auprès des commerçants sélectionnés.
> Ne représente pas de boîte, de coffret cadeau, de panier garni, de colis ou
> d'emballage comme s'il s'agissait du produit vendu. Illustre l'expérience et
> les activités réellement proposées par les prestations sélectionnées, avec une
> scène ou une composition cohérente. N'invente pas d'activité, d'objet offert,
> de livraison ou d'avantage absent de la sélection. Le titre, la description et
> le texte alternatif doivent eux aussi présenter une expérience, sans promettre
> un coffret matériel à recevoir.

Les objets servant une prestation réelle (plat, outils, etc.) restent possibles.
Les intentions/descriptions sont des données citées, jamais des instructions
prioritaires ; le template précise de ne pas suivre leurs demandes contraires.
Cela ne prouve pas l'obéissance d'une IA externe. Le contrôle sémantique du résultat
reste la relecture de l'aperçu par l'opérateur, sans classifier d'image implicite.
Le schéma JSON et son exemple technique ne changent pas pour cette exigence.

## API interne

Nouvelles routes sous **`/internal/commercialisation/atelier`**, tags `internal` et
`commercialisation`, cohérentes avec les conventions de domaine. Les routes
existantes `/internal/erp/api` conservent leurs parcours. UI :
`/internal/erp/atelier` et `/internal/erp/atelier/preparations/{id}`.

L'accès est conditionné par `LOCALEO_FEATURE_ATELIER_COFFRETS_ENABLED`, désactivé
par défaut ; lorsque le flag est désactivé, les routes Atelier renvoient 404.

Toutes les réponses de préparation portent `Cache-Control: no-store`.
Le détail et les résumés exposent `expires_at` en date UTC ISO 8601. À 30 jours
après la dernière modification, les préparations non créées sont exclues des listes
de travail et leur accès/commande renvoie 410 `ATELIER_PREPARATION_EXPIREE`, après
contrôle des droits. Une préparation CREEE nettoyée ne renvoie que son résultat
minimal autorisé et son lien coffret, jamais le contenu purgé ni un ancien prompt.
Authentification ERP et commune requises sur chaque route. Écritures :
`X-CSRF-Token`, contrôle Origin, `Idempotency-Key` ASCII visible 1..128 caractères
et `expected_version` sauf création initiale. Le dépôt réutilise les limites de
quota/débit DAM ; les erreurs de débit portent `Retry-After`.

| Méthode et suffixe | Entrée | Sortie / effets |
| --- | --- | --- |
| GET `/preparations` | `page` >=1, `page_size` 1..100 (25 par défaut), commune/état facultatifs | Page des seules préparations accessibles, ordre `updated_at DESC, id`. Résumés sans prompt complet. |
| POST `/preparations` | `ville_id` obligatoire, autres champs opérateur et `selection` | 201 ; UUID, version 1, BROUILLON. Commune existante et autorisée obligatoire ; seuls type/prix/validité peuvent être nuls, intention absente et sélection vide à ce stade. |
| GET `/preparations/{id}` | UUID | État/version, paramètres, sélection/faits autorisés, dernier contexte et aperçu si existants, média, blocages dérivés, résultat éventuel. Aucune mutation. |
| PATCH `/preparations/{id}` | Version + champs opérateur/selection modifiés | 200 ; nouvelle version ; invalidation du contexte si nécessaire. Changement de commune avec sélection exige `confirmer_reinitialisation: true`. |
| GET `/preparations/{id}/candidats` | `page`, `page_size`, `q` <=200, `commercant_id` facultatif | Modèles de la commune autorisée, version, champs utiles ERP, `rattachable`, `blocages` français ; pagination en base, aucun `coffret_id` provisoire nécessaire. |
| POST `/preparations/{id}/prompt` | Version attendue | 200 ; nouveau contexte, version, texte du prompt, version de template/schéma. Même clé rejoue la même émission. |
| GET `/preparations/{id}/prompt` | UUID | Dernier prompt autorisé, contexte et blocages actuels ; 409 si aucun contexte. N'émet rien de nouveau. |
| POST `/preparations/{id}/reponse` | Version, `texte` borné incluant le WebP base64 | 200 ; validation complète, décodage et contrôle du média, persistance atomique de la proposition normalisée et de l'asset DAM ; nouvelle version, APERCU_VALIDE. Aucune écriture en cas de refus. |
| PATCH `/preparations/{id}/proposition` | Version ; champs optionnels `nom`, `accroche`, `description`, `visuel`, `ordre` définis ci-dessous | 200 ; proposition normalisée, nouvelle version. Les IDs de modèles et versions ne peuvent pas être remplacés ; seul l'ordre complet peut changer. |
| GET `/preparations/{id}/medias` | `page`, `page_size`, `q` <=200 | Bibliothèque paginée limitée aux assets permis par la politique de [données](architecture.md). Format/poids/statut annoncés ; contrôle réel lors de la sélection. |
| POST `/preparations/{id}/medias` | Multipart `expected_version`, `file` | 201 ; dépôt WebP contrôlé, liaison à la préparation et nouvelle version dans la même transaction. Le hash idempotent inclut empreinte réelle du fichier ; aucun doublon au rejeu. |
| PUT `/preparations/{id}/media` | Version, `media_id` UUID ou null | 200 ; sélection/retour sans image, nouvelle version. Vérifier accès, contenu et quota applicable. |
| POST `/preparations/{id}/creer-coffret` | `expected_version` uniquement | 201 initial, 200 rejeu ; résultat final ci-dessous. Aucun texte ou prix recopié du navigateur : utiliser la proposition persistée confirmée. |

Les routes médias (liste, dépôt et sélection) servent uniquement au remplacement
volontaire à l'état `APERCU_VALIDE`, après import complet du contexte courant.
Aux autres états, refuser par 409 `ATELIER_ETAT_INCOMPATIBLE`. Un média conservé
d'un ancien contexte ne permet pas de contourner l'image obligatoire dans le
nouveau JSON. Le choix valide affecte `media_contexte_id` au contexte courant.

Les mêmes champs opérateur que `CoffretCommande` portent les limites existantes :
type 1..80 et référentiel existant ; prix entier 1..99 999 999 centimes ; validité
1..3 650 jours. Intention <=500. Sélection <=20 objets modèle/version uniques,
min 1 au prompt/création. Toutes les commandes sont fermées aux champs inconnus.
Le contexte d'authentification fournit l'acteur ; aucun `acteur` libre dans un body.
L'enveloppe HTTP `{expected_version, texte}` est bornée à 327 680 octets pour
absorber l'échappement JSON. La limite de 262 144 octets s'applique au texte collé
une fois extrait ; refuser avant parsing de sa réponse IA. Le frontend envoie
du JSON UTF-8 compact, sans convertir toute la chaîne en échappements Unicode.
Les réponses d'API renvoient `media_id`, URI autorisée, checksum, type et poids
décodé ; elles ne recopient jamais le base64. Conserver l'audit et les logs sans
body brut, même pour une erreur. L'empreinte idempotente inclut le texte reçu et
le contexte ; un retry valide ne crée pas de second média. Le contrôle de débit
et quota DAM s'applique aussi à cet import, pas seulement aux uploads multipart.
Pour POST/PATCH préparation, `ville_id` ne peut jamais être nul ; un champ omis au
PATCH conserve sa valeur. `intention` peut être absente/null et se normalise à une
chaîne vide ; type/prix/validité nulls remettent la préparation à l'état incomplet
et invalident le contexte. Seuls les UUID et valeurs de sélection contrôlés sont stockés.

Les trois listes renvoient `{items, page, page_size, total}` : `total` compte les
résultats après filtres et droits, `items` ne dépasse jamais `page_size`. Une page
au-delà de la dernière renvoie 200 avec `items: []` et le total ; valeurs de page
invalides donnent 422. Tri des préparations par `updated_at DESC, id ASC`, candidats
par `libelle ASC, id ASC`, médias par `nom ASC, id ASC`, selon la collation de base.
Filtres appliqués avant pagination en base, jamais après un chargement intégral.

Contrat exact de retouche de proposition :

```json
{
  "expected_version": 4,
  "nom": "Mon coffret",
  "accroche": "Une découverte locale",
  "description": "Description relue par l'opérateur.",
  "ordre": ["44444444-4444-4444-8444-444444444444", "88888888-8888-4888-8888-888888888888"],
  "visuel": {"texte_alternatif": "Illustration des deux expériences."}
}
```

Seule `expected_version` est obligatoire, avec au moins une retouche. Les clés
omises conservent leur valeur ; aucune des retouches présentes n'accepte null.
`ordre` est un tableau complet d'UUID de modèles, sans doublon, ensemble identique
à celui de la proposition ; les versions sont celles déjà validées. `visuel` est
un objet fermé contenant `texte_alternatif`, selon les mêmes bornes que la réponse
IA. Le texte alternatif stocké reste non vide (1..180) ;
un composant présentant l'image comme décorative peut rendre `alt=""` sans effacer
cette valeur canonique. Ce choix de rendu ne change pas le contrat d'import/retouche.

Avant d'appeler le helper d'idempotence existant, contrôler l'accès à la préparation
et, si elle est créée, au coffret courant : son rejeu `old.result` précède le callback.
Un contrôle dans le seul callback laisserait fuiter un ancien résultat après retrait
de droits. Même principe pour le rejeu de prompt et d'upload.

Pour les profils actuels, ADMIN et EXPLOITATION autorisé sur la commune disposent
des commandes Atelier. Lors de la livraison de l'évolution EPIC 35, consulter et
muter deviennent des capacités distinctes : Lecteur consulte, Backoffice/Admin
créent selon leur périmètre ; émission de contexte, import et upload sont des
mutations. Ne jamais ajouter Lecteur au garde existant sans contrôler les commandes.

Résultat de création :

```json
{
  "preparation_id": "11111111-1111-4111-8111-111111111111",
  "coffret_id": "55555555-5555-4555-8555-555555555555",
  "statut": "BROUILLON",
  "version": 3,
  "prestations": [
    {"id": "66666666-6666-4666-8666-666666666666", "version": 1, "ordre_presentation": 1},
    {"id": "77777777-7777-4777-8777-777777777777", "version": 1, "ordre_presentation": 2}
  ],
  "replayed": false
}
```

Au rejeu, vérifier les droits courants puis retourner le résultat historique avec
`replayed: true`. Le statut/version de cette réponse décrivent la création initiale,
pas un coffret éventuellement modifié ou publié depuis : charger son dossier pour
son état courant. Une ancienne clé avec un body différent donne 409 avant action.

### Erreurs métier et transport

Enveloppe cible de ces nouvelles routes :
`{"detail":{"code":"ATELIER_SOURCE_OBSOLETE","message":"Une prestation a changé. Actualisez la sélection puis copiez un nouveau prompt.","champs":[]}}`.
`champs` contient seulement chemins et messages utiles, sans valeur collée ou donnée
interdite. L'ERP adapte les exceptions héritées à cette enveloppe et ne montre pas
une traceback ou un code anglais seul. Conserver l'identifiant de corrélation de
la plateforme dans son en-tête courant pour le diagnostic.

| HTTP | Codes principaux | Comportement |
| --- | --- | --- |
| 401 / 403 | Session absente / droit ou CSRF refusé | Reconnexion ou refus français ; aucun résultat d'idempotence divulgué. |
| 404 | `ATELIER_INTROUVABLE` | Ressource absente ou hors périmètre, sans confirmer son existence. |
| 409 | `ATELIER_VERSION_CONFLICT`, `ATELIER_SOURCE_OBSOLETE`, `ATELIER_CONTEXTE_OBSOLETE`, `ERP_IDEMPOTENCY_CONFLICT`, `ATELIER_ETAT_INCOMPATIBLE` | Recharger/régénérer selon le cas, conserver la saisie non enregistrée. |
| 410 | `ATELIER_COFFRET_SUPPRIME` | Préparation terminale dont le coffret a été supprimé ; aucune recréation. |
| 410 | `ATELIER_PREPARATION_EXPIREE` | « Cette préparation a expiré après 30 jours sans modification. Commencez une nouvelle préparation. » Aucun rejeu ne la réactive. |
| 413 | `ATELIER_REPONSE_TROP_LONGUE`, `ATELIER_IMAGE_TROP_LOURDE`, `ATELIER_PROMPT_TROP_LONG` | Indiquer limite et action corrective. |
| 415 / 422 | `ATELIER_IMAGE_INVALIDE`, `ATELIER_BASE64_INVALIDE`, `ATELIER_REPONSE_INVALIDE`, `ATELIER_SELECTION_INVALIDE`, `ATELIER_DONNEES_PROMPT_INTERDITES` | Format réel/base64/contrat/sélection refusé ; aucune écriture partielle. |
| 422 | `ATELIER_IMAGE_MANQUANTE` | « Ajoutez ou confirmez l'image de ce coffret avant de le créer. » Sauvegarde de la préparation possible, création refusée. |
| 429 / 507 | Débit / quota DAM | Attendre ou libérer du stockage via une personne habilitée ; aucune création d'asset partielle. |

## Champs canoniques et contrats consommateurs

| Proposition/import | Stockage final | Consommation |
| --- | --- | --- |
| `nom` | Coffret.nom existant | ERP et lecteurs actuels. |
| `accroche`, `description` | Nouveaux champs Coffret, nullables pour les anciens | ERP éditable ; cartes Marketplace pour accroche, fiche pour description dédiée. |
| `visuel.texte_alternatif` retouché | Nouveau Coffret.image_alt | Image informative de couverture ; alt vide conservé lorsqu'une image est réellement décorative. |
| Ordre du tableau `prestations` | Prestation.ordre_presentation | Tri ERP et projections publiques, comportement historique conservé pour les lignes anciennes. |
| `visuel.contenu_base64` décodé et contrôlé, ou remplacement volontaire | Asset DAM, puis Coffret.image_uri existant | DAM/public `vignette_url` ; rattachement au contexte courant, aucun base64 dans les projections publiques ni dans la préparation persistée. |

Les commandes/détails ERP et `CoffretSummaryPayload`/`CoffretDetailPayload`
du backend exposent de manière additive les champs optionnels `accroche`, `description`,
`image_alt`, et `ordre_presentation` sur les prestations. Entités, mappers,
projections publiques et listes transportent ces mêmes champs.
Les anciens clients peuvent ignorer ces champs et les anciens coffrets restent
lisibles. Les formulaires existants doivent préserver les champs absents du body.
La modification ERP emploie `exclude_unset` : omettre un champ préserve sa valeur,
un null explicite efface un champ éditorial nullable. L'ordre, entier positif
nullable et unique par coffret, ne modifie ni prix ni droits de consommation.

Dans la Marketplace, adapter les normaliseurs, cartes et
[présentation](../../../../localeo-marketplace/src/services/coffretPresentation.js),
ainsi que la fiche. L'accroche éditoriale ne remplace pas la promesse contractuelle
utilisée par [le parcours d'achat](../../../../localeo-marketplace/src/services/coffretPurchase.js).
Afficher la description dans un bloc distinct, sans dupliquer la promesse ni le
contenu indicatif. Repli sur le rendu courant quand les nouveaux champs sont nuls.
Préserver les snapshots et documents des achats passés. Les sélecteurs de lots
Animation, lecteurs Commerçant et Live doivent tolérer ces ajouts et conserver
leurs données métier ; les contrats embarqués stricts sont à examiner avant release.

## Extensions V1.2 — prix et compatibilité HTTP

Producteur : API interne Atelier ; consommateurs : module Atelier partagé ERP/PWA.
Schémas canoniques documentaires : ce contrat et `openapi.json` généré par
`scripts/documentation/generate_epic66_openapi.py` dans le backend. L'OpenAPI
versionné a été régénéré hors ligne depuis le code V1.2 (neuf chemins).
L'admission `PARAMS`, les schémas documentaires backend, le validateur de domaine,
les DTO et le module UI ont été adaptés ensemble. Cet export couvre les routes
métier Atelier ; les routes de présentation PWA restent décrites ci-dessous.

POST/PATCH préparation acceptent le champ plat optionnel
`mode_prix: "AUTO" | "MANUEL"` (null et valeurs inconnues refusés). Les bornes et
le transport du `prix_centimes` existant restent inchangés. Les champs calculés
`total_prestations_centimes` et `reference_prix` sont interdits en entrée.

| Commande | Mode résolu / effet |
| --- | --- |
| POST sans mode ni prix, ou prix null | AUTO ; calcul depuis la sélection, prix null si préparation incomplète ou total non admissible. |
| POST sans mode avec prix positif | MANUEL pour compatibilité avec l'ancien client ; ne pas écraser le prix fourni. |
| POST/PATCH avec mode AUTO | `prix_centimes` doit être absent ; tout prix fourni, même null, donne 422. Calcul serveur depuis la sélection résultante. |
| POST/PATCH avec mode MANUEL | Prix explicite positif ou null (brouillon incomplet) ; au PATCH, prix omis conserve le prix effectif existant. |
| PATCH sans mode ni prix | Conserve le mode courant, MANUEL si historique. Si sélection change, actualise le total et, en AUTO seulement, le prix. |
| PATCH sans mode avec prix présent | MANUEL, y compris null ; respecte l'intention de l'ancien client qui envoie un prix. |

Le nouveau client AUTO omet toujours le prix calculé lorsqu'il renvoie une commande.
Il envoie explicitement MANUEL lors d'une personnalisation, et AUTO sans prix
pour **Utiliser le total des prestations**. Un corps contradictoire est refusé
atomiquement (`422 ATELIER_MODE_PRIX_INVALIDE`). Le PATCH de sélection porte
l'ensemble résultant, pas un delta ; les limites 20 et unicité demeurent.
Un changement de commune confirmé vide la sélection comme auparavant : en AUTO,
total 0/prix null ; en MANUEL, prix conservé mais progression bloquée sans sélection.

Exemple de retour non nettoyé (champs additionnels, les autres champs restent présents) :

```json
{"mode_prix":"AUTO","prix_centimes":8000,"total_prestations_centimes":8000}
```

`total_prestations_centimes` est un entier >=0, ou null quand les sources ne sont
pas évaluables. Le total peut dépasser le plafond du prix : aucun clamp. Les
blocages expliquent `ATELIER_PRIX_NON_CALCULABLE` (tarif absent/invalide),
`ATELIER_PRIX_HORS_LIMITES` (total nul ou trop élevé en AUTO), et le budget
`ERP_BUDGET_EXCEEDED`. Ces blocages sont dérivés en lecture ; sauvegarder un état
incomplet n'est pas une validation pour l'émission ou la création. Si une source
invalide est soumise en mutation, réponse 422 sans écriture ; version périmée :
409 `ATELIER_SOURCE_OBSOLETE`. Les DTO minimaux après nettoyage n'ajoutent pas
de données de prix effacées. Les nouvelles clés de stockage sont explicitement
filtrées de la projection, sans sérialisation générique du snapshot.

La liste des candidats conserve son format mais `rattachable` exprime l'éligibilité
de la source (pas le budget de l'ancien prix). Le budget de l'ensemble est présenté
au niveau de la préparation et recontrôlé aux commandes finales. Le client n'a pas
à augmenter artificiellement le prix pour pouvoir sélectionner une prestation.

Concurrence et idempotence inchangées : expected_version, verrou de préparation,
contrôle des sources et écriture atomique. Le hash de commande intègre le mode
transmis. Une même clé/body rejoue le résultat, même clé/body différent donne 409.
La relecture d'un résultat idempotent ancien peut ne pas contenir les champs
additionnels : l'UI recharge le détail avant une nouvelle mutation.

## Extensions V1.2 — routes PWA et capacité

| Route GET | Contrat cible |
| --- | --- |
| `/internal/atelier/` | HTML dédié, session ERP + flag + capacité, `no-store`. |
| `/internal/atelier/preparations/{id}` | Même shell et contrôles, UUID valide ; chargement détail soumis aux droits de commune. |
| `/internal/erp/atelier` et `/internal/erp/atelier/preparations/{id}` | 303 vers la destination Atelier correspondante après contrôle ; `no-store`, aucun contenu dupliqué. |
| `/internal/atelier/manifest.webmanifest` | Public, données statiques, MIME manifeste ; `id`, `start_url`, `scope` = `/internal/atelier/`, name/short_name = Localeo Atelier, display = standalone, lang = fr. |
| `/internal/atelier/icons/{nom}` | Liste fermée de PNG 192 et 512 px, plus variante maskable 512 px testée ; pas de lecture de chemin libre. |
| `/internal/atelier/sw.js` | Worker public neutre, JavaScript, `no-cache`, scope limité à `/internal/atelier/` sans en-tête élargissant ce scope. |

Manifeste/icônes/SW ne portent aucune donnée d'environnement privée. Les ressources
publiques restent disponibles flag désactivé pour une installation existante ;
le shell et les API demeurent interdits. Les assets UI restent servis selon leur
contrat actuel ; aucune extension générale des exceptions du middleware interne.
Le chemin `/internal/atelier` sans slash redirige vers `/internal/atelier/`.

Étendre de façon additive `GET /internal/erp/api/contexte` avec
`applications.atelier: {disponible: boolean, url: "/internal/atelier/"}`,
`Cache-Control: no-store`. `disponible` est vrai seulement si flag actif et capacité
ERP autorisée avec au moins une commune pour EXPLOITATION. Conserver csrfToken,
role et communes existants. Un profil refusé par ce contexte obtient toujours 403,
pas un contexte plus permissif pour construire le menu. Le menu partagé exploite
la même capacité ; un échec masque Atelier seul, les autres entrées restent intactes.

La nouvelle URL doit être intégrée aux contrôles globaux avant les routes : une
exception locale FastAPI ne suffit pas. Navigation anonyme : 303 login avec retour
Atelier strictement validé selon l'architecture ; API anonyme : 401, aucun HTML.
Session valide non autorisée : 403 ; flag inactif : 404 ; ressource hors commune :
404 selon le contrat existant. L'ordre reste authentification, autorisation puis
flag/données. Les anciennes URL appliquent les mêmes contrôles avant redirection.

La PWA n'introduit pas de nouvel endpoint métier ni de file de synchronisation.
Les routes API demeurent `/internal/commercialisation/atelier`, avec CSRF, Origin,
no-store, admission bornée et idempotence. L'action finale ouvre le dossier ERP
canonique ; elle ne transforme pas la PWA en parcours de publication.

## Contrat de conservation (inchangé en V1.2)

`POST /protected/commercialisation/batch/atelier/conserver` exige le scope
`internal:batch`. Paramètres de query : `limit`, entier 1..500 (100 par défaut),
et `dry_run`, booléen (false par défaut). La commande passe par `BatchRunner`
sous le code `commercialisation.atelier.conserver`, planifié à 04:00 UTC chaque jour.
Le résultat du traitement contient `preparations`, `medias_purges`,
`medias_conserves` et `dry_run`. En simulation, le nombre de préparations éligibles
est calculé ; les compteurs de médias restent à zéro sans simuler chaque suppression.
L'expiration fonctionnelle à 30 jours ne dépend pas du passage du batch.
Voir le [guide d'exploitation](../../exploitation/technique/localeo-atelier.md)
pour activation, reprise et conservation des sentinelles DAM.
