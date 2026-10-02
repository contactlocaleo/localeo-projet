# E69 — Permissions et surfaces

Matrice cible **V1.4 du 2 octobre 2026**, liée au [cadrage](README.md).
E69-SCOPES-GLOBAUX-20261002 conserve les droits fonctionnels V1.3 et rend tous les
scopes accordés globaux. Implémentation et preuves propres à cette évolution en cours.
Les preuves ciblées et limites figurent dans le [bilan de vérification](verification-livraison.md) ;
aucune recette déployée ni couverture exhaustive de tous les routeurs n’est annoncée.

## Scopes fonctionnels des profils prédéfinis

Identifiants portés par le domaine identité et le registre explicite des routes. A = admin historique, L = Lecteur, B = Backoffice, F = Finance.
`Oui` signifie sur toutes les communes, avec les règles métier et masquages
applicables. Les chaînes de la matrice sont les scopes exacts, sans renommage ni
conversion vers les scopes techniques des batchs. B+F est leur union ; les refus techniques/argent priment.

| Scope fonctionnel | L | B | F | A | Limites |
| --- | --- | --- | --- | --- | --- |
| `metier.consulter` | Oui | Oui | Non | Oui | Listes/détails nécessaires ; pas de payload technique |
| `catalogue.gerer` | Non | Oui | Non | Oui | Créer/modifier/publier par les services, pas édition ORM |
| `onboarding.consulter` | Oui | Oui | Non | Oui | Convention et pièces du parcours autorisé ; aucun élargissement implicite aux pièces KYC |
| `onboarding.gerer` | Non | Oui | Non | Oui | Dossiers, pièces, préparation, transitions conformes au domaine |
| `support.consulter` | Oui | Oui | Non | Oui | Consultation métier du support ; aucun accès général par Finance |
| `support.gerer` | Non | Oui | Non | Oui | Traitement métier du support |
| `finance.support.consulter` | Non | Non | Oui | Oui | Projection de demandes financières autorisées uniquement, jamais alias de `support.consulter` |
| `atelier.consulter` | Oui | Oui | Non | Oui | Préparation existante et médias autorisés, pas de génération implicite |
| `atelier.gerer` | Non | Oui | Non | Oui | Génération IA, préparation et création de coffret ; coûts IA ne sont pas des commandes de mouvement de fonds PSP |
| `animation.gerer` | Non | Oui | Non | Oui | Offres catalogue, génération et préparation Animation, consultation du suivi ; hors droits internes et commandes financières réservées |
| `catalogue.qualifier_bum` | Non | Oui | Non | Oui | VALIDER/SUSPENDRE sur le coffret autorisé ; aucune modification de politique fiscale globale |
| `animation.activer_gratuitement` | Non | Oui | Non | Oui | Montant déjà nul et éligibilité vérifiée ; ne permet pas de remise à zéro |
| `animation.annuler_impayee` | Non | Oui | Non | Oui | Commande impayée non active uniquement ; pas d'annulation de facture, paiement ou remboursement |
| `acces_externes.consulter` | Limité | Oui | Non | Oui | L : seul état d'accès utile au dossier ; pas de tentatives, sessions ou détails de sécurité |
| `acces_externes.gerer` | Non | Oui | Non | Oui | Comptes commerçants et gestionnaires partenaires, jamais comptes ERP ; toutes communes du compte externe ; délégation fonctionnelle bornée |
| `finance.consulter` | Oui | Oui | Oui | Oui | Projections E65 filtrées et masquées, pas la console Stripe |
| `finance.exporter_metier` | Oui | Oui | Oui | Oui | Export de la projection métier déjà lisible ; colonnes explicitement listées, aucune génération de pièce |
| `finance.exporter` | Non | Non | Oui | Oui | Export spécialisé Finance distinct, toujours filtré et sans données techniques ; retrait F retire cette capacité |
| `finance.suivre` | Non | Non | Oui | Oui | Tickets/notes financiers du Support existant, après adaptation du rattachement ; aucune mutation de l'état bancaire/comptable |
| `documents.lire` | Selon dossier | Selon dossier | Justificatifs financiers | Oui | Contrôle de la ressource propriétaire, pas du seul UUID du fichier |
| `documents.generer` | Non | Selon métier | Non | Oui | Émission d'un avoir ou document modifiant une dette reste `finance.executer` |
| `finance.executer` | Non | Non | Non | Oui | Remboursement, transfert, avoir, correction de dette, reprise de flux financier |
| `audit.global`, `technique`, `comptes.administrer`, `sqladmin` | Non | Non | Non | Oui | Type principal historique exigé, pas seulement chaîne rôle ADMIN |

Les capacités sont explicitement affectées aux routes/actions, pas déduites du
verbe HTTP ou du préfixe de route. Les modifications CSRF/session et l'audit de
consultation sont permis au Lecteur ; les mutations métier, synchronisations,
générations et envois restent interdits, même derrière un GET.

Les deux exports correspondent à deux projections et contrôles distincts. Un endpoint
commun éventuel doit choisir explicitement la projection autorisée, jamais ajouter
des colonnes Finance à un export Lecteur/Backoffice à partir d'un paramètre libre.
La liste des colonnes doit être arrêtée par export avant son ouverture ; un export
non classifié reste fermé. De même, Finance ne reçoit pas `support.gerer` pour rendre
son suivi possible : la commande financière ciblée a sa propre capacité et ressource.

### Scopes globaux et contexte de navigation

Chaque profil prédéfini attribue les scopes de la matrice sur toutes les communes.
B+F est leur union fonctionnelle. Par exemple, `catalogue.gerer` provient de B
et `finance.exporter` de F ; les deux sont globaux. Le retrait de F retire
l'export spécialisé sans supprimer les fonctions Backoffice.

Le contexte expose `scopes: list[str]`, avec les identifiants exacts de cette
matrice. L'alias de compatibilité `capabilities` utilise exclusivement
`scope: {type:"GLOBAL",communeIds:[]}`. Il n'existe aucun territoire actif ni
sélecteur de communes d'habilitation. Les champs de commune d'un coffret, d'un
commerce ou d'une souscription restent des données métier ordinaires.

Finance seul n'obtient toujours pas tout le référentiel catalogue en ouvrant
`/internal/erp/api/contexte` : seules les références utiles à sa fonction sont
exposées. Une ressource multi-communes n'est plus refusée pour raison territoriale,
mais conserve les contrôles de nature, propriétaire, état et cohérence. Pièces,
liens, totaux et exports appliquent les mêmes masquages fonctionnels que l'écran.

La ressemblance avec les habilitations des batchs concerne le contrôle de chaînes
de scopes. Une clé API de batch n'est pas une session humaine, et un profil Finance
ne reçoit pas les scopes techniques ni l'accès aux routes d'exécution de batch.

## Inventaire de départ et adaptations locales

La colonne centrale conserve le constat avant E69 ; les adaptations V1.3 ont été intégrées localement. Leur filtrage territorial
est remplacé par les scopes globaux V1.4 ; les masquages et restrictions de
fonction restent à préserver dans la nouvelle preuve. Les tests référencés dans le bilan vérifient les surfaces ciblées,
sans transformer cet inventaire en garantie exhaustive de toute route historique.

| Surface / producteur | Entrées et constat avant E69 | Adaptation et preuves à consulter dans le bilan |
| --- | --- | --- |
| [ERP API](../../../../localeo-backend/app/api/erp_api.py) / erp.js | `/internal/erp/api/*`, contexte ADMIN/EXPLOITATION ; navigation ADMIN issue des vues SQLAdmin | Répertoire explicite des capacités ; contrôles avant callback **et avant rejeu** ; menu filtré sans lien SQLAdmin |
| [Support](../../../../localeo-backend/app/api/instances_support_api.py) | `/internal/erp/api/instances/*`, recherche/détail/chronologie/connexes, ticket/note et mise à jour ticket | L lit, B traite ; F seulement projection financière dédiée ; filtrer documents et connexes par famille |
| [Support UI](../../../../localeo-backend/app/api/support_ui.py) | `/internal/support` et `/internal/support/instances/{id}` | Connexion nominative, 403 explicite, même portée entre recherche et détail |
| [Atelier](../../../../localeo-backend/app/api/atelier_assiste_api.py) | `/internal/commercialisation/atelier/preparations/*` ; shell `/internal/atelier` avec feature flag et garde territoriale | Séparer GET sans création de préparation et toutes mutations/générations ; F refusé ; feature flag reste une condition supplémentaire |
| [OnBoard](../../../../localeo-backend/app/api/onboarding_commercant_api.py) | `/internal/onboard/api/*` : contexte ERP puis alias `require_admin_session` ADMIN | Remplacer sélectivement les doubles gardes pour les actions métier classifiées ; garder administration et commandes financières admin |
| [Paiements E65](../../../../localeo-backend/app/api/consultation_paiements_api.py) | `/internal/gestion-achats/paiements` et détails/achats ; garde ADMIN ; pas de portée territoriale injectée | Filtrage serveur avant total/listes/détails, DTO métier et capacité financière ; aucun simple élargissement du garde |
| [Reversements E65](../../../../localeo-backend/app/api/consultation_reversements_api.py) | `/internal/gestion-reversement/suivi/...` ; ADMIN, sections mouvements/paiements/sources/virements | Scopes fonctionnels globaux et masquage ; le `communeId` affiché est une donnée métier |
| [UI E65](../../../../localeo-backend/app/api/erp_ui.py) / finance-consultation.js | `/internal/erp/paiements`, `/reversements`, `/audit` ; gardes serveur et JS ADMIN | Remplacer vérifications nominales par capacités ; Audit reste historique, finance par principal courant |
| [Factures](../../../../localeo-backend/app/api/factures_localeo_api.py) | `/conformite-fiscale/factures-localeo` ; GET téléchargement appelle `rendre` et commit | Une lecture F/L ne doit pas générer ; servir fichier existant via service de lecture. En son absence signaler « document à préparer », ne pas masquer la génération en GET |
| [GED](../../../../localeo-backend/app/api/documents_api.py) | `/documents/admin*` strict ADMIN, filtres de métadonnées et mutations | Garder ces routes administratives fermées ; exposer une projection/read endpoint métier ciblée avec politique documentaire et propriétaire vérifiés |
| [Routes historiques](../../../../localeo-backend/app/infrastructure/admin/admin.py) | `/internal/achats/{id}/documents`, POST reçu PDF ; pack ZIP retiré 410 | Ne pas annoncer le pack comme export disponible ; isoler lecture document déjà produit et génération autorisée séparément |
| Même source | `/internal/reversements/vue-360/export.csv` ; export audité dans interface historique | Extraction/projection de données partagée possible ; endpoint métier export à protéger avant ouverture F, pas ouverture de toute la vue historique |
| [Vision achats](../../../../localeo-backend/app/application/gestion_achats/services/vision_360_achats.py) | Racine autorisée par intersection territoriale puis ensemble d'achats ; données personnelles ADMIN optionnelles | Commande multi-communes accessible avec le scope requis ; politique explicite des agrégats/sections et masquage personnel conservés |
| [Ops](../../../../localeo-backend/app/api/ops_ui.py) | `/internal/ops` réutilise dashboard admin ; `admin_ville_id` filtre de présentation | Satellite technique : rester admin tant qu'une projection métier explicitement autorisée n'est pas conçue ; filtre UI n'est pas un périmètre |
| [Control](../../../../localeo-backend/app/api/pwa_exploitation_api.py) | `/internal/exploitation/pwa/api/*` ADMIN | Maintien admin, y compris push, préférences, liens profonds ; scopes batch séparés |
| [Flux financiers](../../../../localeo-backend/app/api/reversements_api.py) | Campagnes Stripe / rattrapage payouts par clé `internal:finance` ; équivalents historiques admin | Ce scope technique ne devient jamais le rôle humain Finance ; pas de clé de service distribuée aux opérateurs |
| [Accès Animation](../../../../localeo-backend/app/api/acces_animation_erp_api.py) | `/internal/erp/api/acces-animation` ADMIN, invitations partenaire | Référence fonctionnelle E69 ; administration des comptes partenaire ne donne aucun droit de gérer les comptes internes |

Les routes historiques, alias `/admin/internal/...`, exports et liens générés
doivent être recensés avec leur méthode, garde, producteur, consommateur, capacité,
portée et test. La liste ci-dessus est un inventaire initial des surfaces touchées,
pas une prétention d’exhaustivité de tous les routeurs backend. Le registre
[capacites_routes.py](../../../../localeo-backend/app/security/capacites_routes.py)
refuse les entrées non classifiées aux comptes nominatifs ; ce refus par défaut
ne remplace pas l’ajout d’un scénario métier pour chaque nouvelle ouverture.

## Actions et données multi-communes

### Actions métier derrière des gardes ADMIN actuelles

Inventaire complété lors de l’implémentation locale du 1er octobre ; les droits
ci-dessous ne sont pas présentés comme déjà déployés. Les commandes conservent leurs
confirmations, contrôle de version, idempotence et audit existants.

| Entrée / action observée | Effet et cible E69 |
| --- | --- |
| GET `/internal/erp/api/commercants/{mid}/acces` | B/admin : état du login et sécurité ; L : projection d'état dans le dossier seulement ; F : aucun accès à cette console |
| POST même route : `initialiser`, `reinitialiser`, `verrouiller`, `deverrouiller` | B/admin selon commerce. L'initialisation peut réaligner le login sur l'email de contact ; afficher cet effet avant confirmation. Le déverrouillage n'efface pas toutes les limites de demandes de mots de passe |
| `/internal/erp/api/acces-animation` et `/{id}/habilitations`, `/{id}/emails` | B/admin pour création/édition des gestionnaires externes, invitations et habilitations délégables ; L : état métier seulement, F refusé |
| GET `/internal/erp/api/coffrets/{cid}/fiscalite` | L/B : diagnostic métier du coffret ; F seulement données utiles dans la projection du dossier financier |
| POST `/coffrets/{cid}/qualifier` : VALIDER/SUSPENDRE | Décision BUM versionnée affectant la vendabilité, sans appel PSP. B/admin sur toutes les communes ; confirmations et règles BUM conservées, F seul refusé |
| GET `/internal/erp/api/animation-commercial/commandes` ou `/souscriptions`, détails | L/B : projection métier ; F : projection financière. Le DTO actuel contient lien Checkout, facturation et identifiants PSP : il ne peut pas être partagé intégralement avec tous les rôles |
| POST commande Animation : `checkout` | Appel PSP et modification du statut de paiement : admin selon la frontière des commandes financières ; pas de délégation par simple accès en lecture à la commande |
| Même route : `email-paiement` | Envoi du lien déjà actif sans modification du montant ni appel PSP : B/admin ; F non accordé par défaut, éventuelle extension à classifier |
| Même route : `activer-gratuitement` | Active des droits pour une commande déjà à zéro ; ne ramène pas un prix positif à zéro. B/admin sur toutes les communes ; F seul refusé |
| Même route : `annuler` | Annule commande impayée/non active, sans remboursement ; décision potentiellement engageante. B/admin sur toutes les communes ; F seul refusé |
| GET `/internal/erp/operations` | Hub métier accessible avec `metier.consulter` ; aucun accès implicite aux outils techniques liés |
| `/internal/erp/nouvelle-offre-animation`, GET configuration et POST `/internal/erp/api/offres-animation` | B/admin via `animation.gerer` ; création d'une définition au catalogue, aucun paiement ni activation de droits partenaire |
| Consoles ERP `animations/generations`, `preparation`, `exploitation` et API moteur explicitement classifiées | B/admin : génération, dépôt/vérification/acceptation d'une réponse, reprise/révision/annulation/affectation, préparation, POI et modèles ; suivi d'exploitation en lecture. Identité interne réelle, CSRF nominatif et droits courants contrôlés dans les transactions métier |

Le correctif du 2 octobre aligne ces liens métier déjà affichés avec leurs gardes
serveur. Le catalogue fermé reste la référence : il ne rend pas tout
`/internal/animation-locale` accessible aux comptes internes. Augmenter le quota,
neutraliser une étape, régulariser une preuve, modifier les paramètres
d'exploitation, clôturer le moteur et exécuter la conservation restent hors de
cette ouverture. La publication continue par le parcours Animation habilité.
Les formulaires de création commerçant/coffret exigent `catalogue.gerer`, comme
leurs commandes ; le Lecteur consulte les fiches existantes.

Sources complémentaires :
[gestion des accès commerçants](../../../../localeo-backend/app/application/identite_acces/services/gestion_acces_commercant_erp.py),
[gestion des accès Animation](../../../../localeo-backend/app/application/identite_acces/services/gestion_acces_animation.py),
[routes souscriptions Animation](../../../../localeo-backend/app/api/souscriptions_animation_erp_api.py).

**Délégation Animation :** la liste retournée par `/configuration` n'est pas une
preuve que toutes ses permissions sont délégables par B. Politique V1 implémentée : autoriser
le sous-ensemble des opérations partenaires ordinaires classifiées ; maintenir
`animation:quota_generation_modifier`, `animation:neutraliser_etape`,
`animation:regulariser_preuve`, `animation:generation_deposer` et
`animation:generation_accepter` admin tant que leurs effets et destinataires ne
sont pas classifiés. Toute nouvelle permission inconnue reste non délégable par B.
Les quotas payants et les droits acquis ne sont pas augmentés par la seule attribution.

Une modification globale d'un gestionnaire partenaire (email, statut, reset ou
invitation) peut affecter plusieurs communes. En V1.4, B peut exercer ses fonctions
déléguées sur toutes ces communes ; aucune couverture territoriale supplémentaire
n'est demandée. Modifier une habilitation conserve les autres habilitations selon
les règles Animation. Les permissions non délégables restent réservées à l'admin.

Les tests de délégation conservent les refus fonctionnels et les invariants de
source/destination. Les anciennes attentes de refus fondées uniquement sur la
commune sont remplacées par des succès multi-communes. La gestion des comptes
internes reste exclusivement `comptes.administrer` par principal historique,
même pour un B gérant des comptes externes.

### Ressources et documents

Les communes restent des données métier d'ERP, Atelier, Support et OnBoard.
Aucun de ces rattachements ne limite territorialement un utilisateur interne
V1.4. Les listes, compteurs, détails, commandes et documents autorisés couvrent
toutes les communes. Les contrôles de cohérence des sources et propriétaires
demeurent ; la suppression du filtre territorial ne doit pas supprimer ces contrôles.

Les projections financières et documentaires restent propres à leur fonction.
Un scope global n'autorise ni les colonnes administratives, ni les secrets ou les
pièces d'une famille interdite. Les états et snapshots historiques OnBoard sont
projetés dans le DTO métier autorisé, jamais repris comme accès à des données techniques.

Un document de facture doit conserver un propriétaire cohérent avec son achat/
reversement et la famille autorisée, pas seulement porter une étiquette « financier ». Les pièces KYC, payloads PSP,
clés, liens porteurs de droits et dumps sont interdits aux rôles métier. Le dépôt
OnBoard observé accepte `CONVENTION_COMMERCANT` ; son ouverture ne crée pas un
nouveau parcours de collecte/validation de pièces KYC. Un besoin ultérieur de
ces pièces exigerait une capacité et une décision spécifiques. Aucune
URL permanente signée permettant de continuer à lire après retrait de rôle ne
doit être exposée : téléchargement via contrôle de session courant, no-store.

Les historiques utiles d'un dossier restent lisibles sans ouvrir Audit global.
Une note interne de support doit être classifiée avant restitution à F/L ; une
projection peut supprimer le champ ou la famille, jamais transmettre la donnée
puis la cacher en CSS.

## Suivi financier et limites de la livraison

**Suivi financier humain :** E69 ajoute aux états techniques existants des tickets
et notes du Support pour le traitement humain, sans commande bancaire nouvelle.

**E69-ARB-05 résolu : option A retenue.** Finance consulte et exporte les données
autorisées, puis ouvre/complète des tickets et notes du Support existant. Les
états de traitement restent ceux du Support : aucun workflow financier autonome,
aucune résolution de ticket ne modifie une écriture ou l'état PSP.

L'accès Finance part d'un dossier financier autorisé, avec un rattachement serveur
et une classification financière explicite. Ni un mot « paiement » dans le titre,
ni un paramètre client ne rend un ticket accessible. Les anciens tickets/notes
non classifiés restent fermés à Finance ; aucune ouverture générale des connexes.

**Adaptation implémentée localement :** la migration
[v252](../../../../localeo-backend/sql/v252_support_financier.sql) préserve les tickets
d’instance et ajoute les rattachements financiers typés avec un propriétaire unique.
Les façades Finance et Backoffice ont leurs scopes fonctionnels propres ; le
sélecteur des responsables ne présente que des comptes actifs dotés du scope
adapté au dossier, sans condition territoriale.
Les preuves PostgreSQL incluent un paiement sans instance, les notes cloisonnées
et le refus d’un ticket général ou d’un propriétaire incohérent.

**E69-ARB-06 résolu : les trois actions sont ouvertes à Backoffice**, Admin
conservé et Finance seul refusé. Les capacités précises ci-dessus sont appliquées
aux écrans, API, alias et commandes différées, globalement pour l'attribution B.
Remboursements, avoirs, annulations de facture, transferts, modification brute
de montant et Checkout PSP restent admin ; l'annulation métier d'une commande
impayée non active est l'exception explicite, pas une permission financière globale.

**Classification locale :** délégation Animation bornée, projections financières
masquées, exports métier/Finance distincts et lecture de factures déjà produites.
Les accès GED contrôlent famille et propriétaire ; KYC et propriétaire incohérent
restent refusés. Les contrôles documentaires et tests ciblés ne valent pas recette
déployée. Toute action inconnue reste fermée aux rôles métier.

**Exposition technique :** conserver Ops et Control admin ; ne pas appeler
« gestion quotidienne » toute action d'une rubrique « Exploitation ». L'administration
de fournisseur, relance de webhook, recalcul persisté et édition brute ne sont
pas une permission Finance ou Backoffice.

## Présentation ERP et satellites

Le contexte V2 expose un principal et `scopes: list[str]`, sans commune
d'habilitation ; `capabilities` demeure l'alias GLOBAL de compatibilité.
ERP, Support, Atelier et OnBoard utilisent ces scopes pour la navigation et
les commandes ; ils ne fabriquent pas un rôle ADMIN nominatif. OnBoard conserve
les dossiers et récapitulatifs en lecture pour Lecteur, retire ses commandes et
revalide la session avant mutation. Finance peut ouvrir l’accueil ERP neutre sans
charger le référentiel catalogue, puis ses pages financières.

Monitor, retour au premier plan et réponses asynchrones contrôlent les changements
de principal et de droits. Les contenus privés sont purgés à l’expiration ; une
ancienne réponse ne doit pas repeupler un écran fermé. Les preuves navigateur
locales figurent dans le bilan, distinctes des essais PWA réels restant en cible.
