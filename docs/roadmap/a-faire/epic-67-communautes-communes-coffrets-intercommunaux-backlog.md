# EPIC 67 — Communautés de communes et coffrets intercommunaux

## Références

- Date de cadrage : **28 septembre 2026**.
- Identifiant : **EPIC-67**, disponible après recherche dans la roadmap commune,
  ses namespaces applicatifs et les documents des applications voisines.
- État produit : **À faire**, selon la [roadmap commune](../README.md).
- Demande : gérer les communautés de communes pour commercialiser des coffrets
  réunissant des commerçants de plusieurs communes appartenant à la même communauté.
- Phase réalisée : **cadrage uniquement**. Priorité et date de livraison non fixées.

### Rattachement et dépendances

Ce besoin fait évoluer le périmètre territorial de l'offre ; il dépasse une
retouche des filtres ou du libellé d'un coffret. Il constitue une epic distincte
de l'[EPIC 60 — ERP et commercialisation](../terminees/epic-60-vision-360-commercialisation-backlog.md)
et de l'[EPIC 52 — Accueil contextualisé](../terminees/epic-52-accueil-marketplace-geolocalise-backlog.md),
dont les états restent inchangés. Réutiliser leurs parcours, règles et projections.

L'[EPIC 66 — Localeo Atelier](../en-cours/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md)
cadre une première composition communale avec prompt IA externe. **L'EPIC 67 porte
son extension intercommunale** : choix d'une communauté, sélection de ses
prestations, contexte du prompt et validation du retour. L'initialisation du
référentiel et la composition ERP ordinaire peuvent être livrées indépendamment
de l'assistant IA ; la livraison de cette extension exige l'EPIC 66 disponible.

Autres dépendances : [gouvernance du référencement](../terminees/epic-1-gouvernance-du-referencement-commercant-et-prestation-backlog.md),
[conformité BUM](../terminees/epic-50-conformite-fiscale-bum-backlog.md),
[pagination des catalogues](../terminees/epic-57-bornage-pagination-api-marketplace-backlog.md)
et contrats publics existants. Aucun état de ces epics n'est rouvert implicitement.

## Problème et résultat attendu

**Besoin exprimé :** une offre locale doit pouvoir associer les savoir-faire de
plusieurs communes d'une même communauté, sans créer plusieurs coffrets séparés.
Exemple fictif : une dégustation dans la commune A et un atelier dans la commune B
deviennent deux prestations d'un seul coffret de leur communauté C.

**Constats locaux à prendre en compte**, backend `9b9cba3` : les
[règles d'Atelier](../../../../localeo-backend/app/domaine/commercialisation/services/regles_atelier.py)
et le [service ERP](../../../../localeo-backend/app/application/commercialisation/services/atelier_erp.py)
rapprochent aujourd'hui les prestations et leur coffret par commune. La
[fiche coffret Marketplace](../../../../localeo-marketplace/src/pages/CoffretPage.jsx)
utilise une commune résolue pour sa navigation et les liens commerçants.
La sélection multi-communes exige donc une évolution du domaine et de ses
consommateurs ; modifier uniquement la liste de sélection ne suffit pas.
Ce constat est une lecture du code, pas une recette de production.

La recherche ciblée dans les modèles et migrations n'a pas identifié de
référentiel de communautés existant. Les
[modèles persistés](../../../../localeo-backend/app/infrastructure/persistence/models.py)
imposent actuellement une ville au coffret comme au commerçant. Le
[diagnostic de vendabilité](../../../../localeo-backend/app/infrastructure/persistence/repositories/vendabilite_repository.py)
ne recharge pas aujourd'hui la commune de chaque commerçant : le contrôle
territorial à la publication est donc une exigence cible, pas une garde déjà
démontrée. Les [documents d'achat](../../../../localeo-backend/app/application/gestion_achats/services/service_documents_achat.py)
figent aussi une commune de coffret ; leurs snapshots historiques doivent rester
inchangés. Enfin, le [suivi ERP](../../../../localeo-backend/app/application/commercialisation/services/suivi_vendabilite.py)
filtre les coffrets selon une liste de communes autorisées.

**Acteurs :** opérateur habilité du référentiel territorial, gestionnaire de
catalogue habilité, commerçant pour ses propres prestations, acheteur et
bénéficiaire pour la découverte puis l'utilisation du coffret.

**Résultat attendu :** créer, qualifier, publier, acheter et utiliser un seul
coffret intercommunal, en identifiant sans ambiguïté la communauté porteuse de
l'offre, les communes effectivement représentées et le lieu de chaque prestation.
Les coffrets communaux existants continuent de fonctionner.

## Parcours et règles proposés

### Gérer le territoire

Dans le backoffice, créer une fiche **Communauté de communes** avec une identité
stable, un nom, une référence administrative lorsqu'elle est disponible et les
communes membres. Les communes existantes sont réutilisées par leur identifiant,
sans duplication ni création d'une commune artificielle portant le nom du groupement.
Une communauté ne remplace ni l'adresse ni la commune réelle d'un commerçant.

Proposition V1 : gestion explicite dans le backoffice, avec recherche, consultation
des membres et modification contrôlée. La source et la date de vérification des
rattachements sont identifiables. Pas d'import automatique national supposé.
La représentation des adhésions, leurs dates d'effet et la prévention des
appartenances contradictoires seront définies en spécification.

### Composer le coffret

Au démarrage de la composition, choisir **Commune** ou **Communauté de communes**,
puis le territoire. En mode communauté, la sélection regroupe les prestations
éligibles des commerçants de ses communes membres, avec un filtre par commune et
par commerçant. Chaque prestation montre son lieu réel ; le récapitulatif indique
les communes représentées. Aucun commerçant extérieur n'est admis du seul fait
qu'il est géographiquement proche.

**Invariant cible :** pour un coffret communal, chaque prestation appartient à
sa commune ; pour un coffret intercommunal, la commune de chaque commerçant
appartient à la communauté retenue, selon les rattachements applicables. Cette
règle appartient au domaine backend et doit être partagée par toutes les entrées
de composition, d'import, de diagnostic et de publication.

Un coffret conserve un périmètre de référence explicite ; son rattachement
intercommunal ne doit pas être simulé avec le `ville_id` de la commune siège.
Les modèles de prestations, leurs copies versionnées et les liens commerçants
restent ceux du parcours existant. La préparation produit un brouillon ; les
contrôles de prix, reversement, éligibilité, paiement et qualification BUM restent
applicables. L'appartenance au groupement ne vaut pas activation d'un commerçant,
publication d'une commune ou autorisation de vendre une prestation.

### Découvrir, acheter et utiliser

La Marketplace permet de rechercher/filtrer les coffrets par communauté et de
consulter sa présentation et ses communes membres. La carte et la fiche coffret
affichent le nom de la communauté et les communes réellement représentées. Les
prestations indiquent la commune et l'adresse du commerce ; le visiteur doit
pouvoir comprendre les déplacements nécessaires avant d'acheter.

Proposition de découverte V1 : un coffret intercommunal apparaît dans le catalogue
de sa communauté et dans celui de chaque commune où il propose effectivement
une prestation. Il n'est pas présenté comme réalisé dans toutes les communes
membres. Les résultats multi-communes sont dédupliqués par coffret, y compris les
compteurs et la pagination. La proximité se fonde sur les lieux réels des
prestations, pas sur un centre artificiel attribué au groupement ; le calcul
précis et l'ordre des résultats restent à spécifier.

L'achat porte sur **un coffret et une composition**, avec le prix global et la
validité habituels. Le bénéficiaire retrouve les lieux corrects sur le détail,
le résumé/QR et ses accès Live. Chaque commerçant valide uniquement les
prestations qui le concernent. Il n'existe pas de reversement à la communauté
créé implicitement par cette epic.

### Maîtriser les droits et l'évolution des rattachements

La création d'un groupement n'élargit aucun droit automatiquement. Un opérateur
limité à une commune ne reçoit pas les droits sur ses voisines. La spécification
définira une habilitation territoriale explicite ou une couverture de toutes
les communes nécessaires pour composer et gérer le coffret ; les contrôles
s'appliquent aux appels directs autant qu'à l'interface.

Un départ/arrivée de commune, un déménagement de commerçant ou l'archivage d'une
communauté présente les coffrets affectés avant validation. Les sélections en
préparation sont recontrôlées et la vendabilité des offres en vente est réévaluée
selon une politique explicite. Aucune prestation n'est retirée silencieusement
d'un coffret ; aucun achat n'est annulé ou remboursé par ce seul changement.
Les compositions, droits et preuves des achats existants restent préservés ;
un éventuel problème de réalisation passe par le traitement métier habituel.

## Périmètre

**Inclus :** référentiel des communautés et communes membres, gestion backoffice,
périmètre intercommunal du coffret, sélection et contrôles territoriaux communs,
commercialisation et découverte Marketplace, affichage des lieux dans les
parcours d'achat/utilisation, compatibilité des consommateurs et extension Atelier.

**Exclusions V1 :** coffrets entre communautés différentes, groupements commerciaux
arbitraires, regroupements régionaux/départementaux, fusion de communes, gestion
administrative complète des collectivités, vente ou facturation au nom d'une
communauté, nouvelle répartition des commissions, calcul d'itinéraire, migration
automatique des coffrets communaux vers un groupement, nouvelles animations
intercommunales. Les autres formes d'intercommunalité restent à arbitrer.

**Découpage proposé :** référentiel et domaine ; composition ERP et contrats ;
découverte/achat/utilisation ; extension de Localeo Atelier. L'offre intercommunale
n'est ouverte à la vente qu'une fois ses lecteurs, achats et validations compatibles.
La première livraison peut préparer le référentiel sans modifier les ventes existantes.

## Critères d'acceptation

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E67-CA-01 | Opérateur habilité, communes existantes | Créer une communauté et ses rattachements | Fiche identifiable, membres consultables, origine vérifiable ; doublons et rattachements incohérents refusés, aucune commune dupliquée. |
| E67-CA-02 | Gestionnaire autorisé sur le territoire | Choisir le mode communauté et des prestations | Liste filtrable par commune/commerçant, version et lieu visibles ; seuls les candidats autorisés du périmètre peuvent être retenus. |
| E67-CA-03 | Communes A et B membres de C | Créer un coffret avec une prestation de chaque commune | Un brouillon de périmètre C est créé ; les prestations conservent leur commune/commerçant réels et la fiche ERP reste canonique. |
| E67-CA-04 | Prestation extérieure à C, import ou appel API direct | Tenter un rattachement ou une publication | Refus métier motivé et absence de modification partielle ; même règle sur toutes les entrées, dont Atelier IA. |
| E67-CA-05 | Coffret intercommunal préparé | Diagnostiquer puis publier | Rattachements actuels, habilitations et contrôles de commercialisation vérifiés ; aucune dispense BUM, économique ou de statut. |
| E67-CA-06 | Acheteur sur la Marketplace | Rechercher une communauté ou une commune participante | Résultats territoriaux cohérents avec les prestations réelles ; un seul résultat par coffret, compteurs et pagination cohérents. |
| E67-CA-07 | Coffret publié dans plusieurs communes | Ouvrir sa fiche puis une fiche commerçant | Communauté et communes représentées visibles ; chaque lien conduit au commerce dans sa vraie commune, sans commune siège substituée. |
| E67-CA-08 | Achat du coffret intercommunal | Payer, consulter le justificatif et utiliser les accès de bénéficiaire | Un achat de coffret selon les règles actuelles ; identité, prestations et lieux corrects dans les documents, résumé/QR et Live. |
| E67-CA-09 | Commerçant participant ou commerce tiers | Valider une prestation du coffret | Seul un commerçant habilité peut valider ses propres prestations ; consommation unique et reversement habituel, aucun accès élargi à la communauté. |
| E67-CA-10 | Opérateur limité à la commune A | Appeler des opérations sur C contenant B | Aucun élargissement implicite de droits ; opération refusée si la couverture territoriale requise manque, y compris via API directe. |
| E67-CA-11 | Rattachement modifié après sélection ou vente | Enregistrer le changement puis reprendre/publier l'offre | Impacts présentés, préparation périmée détectée, offres réévaluées ; aucun retrait silencieux ni altération des achats existants. |
| E67-CA-12 | Coffrets communaux déjà présents et anciens liens | Migrer puis parcourir, acheter et utiliser | Les périmètres communaux, prix, compositions et liens historiques sont conservés ; aucun groupement inventé ou rattachement automatique des coffrets. |
| E67-CA-13 | Localeo Atelier disponible, communauté autorisée | Copier le prompt, coller une réponse puis créer | Territoire, membres applicables, prestations/version et communes réelles inclus dans le contexte ; réponse étrangère ou périmée refusée ; un seul brouillon créé même après répétition. |
| E67-CA-14 | Groupement, candidats ou résultats nombreux | Rechercher et parcourir les listes sur écran étroit/ordinateur | Pagination bornée, filtres compréhensibles, états vides/erreurs et accès clavier ; aucun chargement non borné de tous les commerces. |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Applications et domaine propriétaire | **Concerné : backend**, référencement territorial pour les communautés/rattachements ; commercialisation pour le périmètre et l'éligibilité ; application pour l'orchestration ; ERP pour la gestion. Les routes et écrans ne dupliquent pas le prédicat territorial. |
| Marketplace | **Concernée :** recherche, listes et compteurs, proximité, fiches territoire/coffret, fil d'Ariane et liens commerçants, panier/commande et consultation. Réutiliser les parcours existants plutôt que cloner un coffret par commune. |
| Commerçant, Animation et Live | **À examiner :** écrans, permissions et contrats supposant une commune unique par coffret ; validation chez le commerçant, carnet et résumés Live, sélection de coffrets comme lots Animation. Pas de création d'animation intercommunale dans cette epic. |
| API et consommateurs | **Concerné :** expression explicite du type/identifiant de périmètre, membres, lieux, filtres et contexte IA ; schémas documentaires canoniques et contrats embarqués. Prévoir la compatibilité et l'ordre de mise à jour, sans fournir un faux `ville_id` aux anciens lecteurs. |
| Persistance, migrations et données existantes | **Concerné :** référentiel, adhésions/version ou dates d'effet, périmètre coffret, index/recherche, droits et conservation historique. Stratégie de migration des coffrets communaux et achats à spécifier ; aucun SQL exécuté au cadrage. |
| Générateur de démonstration et fixtures | **Concerné :** deux communes membres et une extérieure, prestations éligibles/bloquées, habilitations partielles, changement d'adhésion, achat antérieur ; adaptation export/import/restauration au nouveau schéma sans modifier les règles pour le générateur. |
| Documentation fonctionnelle | **Concernée :** gestion du référentiel et de la composition, guide Marketplace et commerçant, extension de l'EPIC 66. Clarifier appartenance administrative, lieux représentés, autorisation et vendabilité. |
| Exploitation et déploiement | **Concerné :** provenance/actualisation du référentiel, contrôle des migrations, readiness, audit des changements, réévaluation des offres et diagnostic. Prévoir activation progressive et reprise ; ne pas annoncer une restauration de données non vérifiée. |

## Questions ouvertes

Propositions à arbitrer en spécification, sans supposer une validation utilisateur :

1. **Types de groupements :** limiter la V1 aux communautés de communes, comme
   demandé, ou prévoir aussi les communautés d'agglomération et métropoles ?
   Cela conditionne le référentiel, ses identifiants et les libellés publics.
2. **Source des rattachements :** saisie contrôlée dans l'ERP proposée en V1 ;
   référentiel externe officiel et synchronisation automatique éventuelle à
   examiner séparément. Fixer responsabilité, fréquence et dates d'effet.
3. **Découverte :** confirmer la présence dans les communes effectivement
   représentées, et définir le classement de proximité ainsi que l'éventuelle
   page publique dédiée au groupement. Un filtre communauté et l'identification
   des lieux sont dans le résultat attendu.
4. **Changements de périmètre :** préciser le devenir des nouvelles ventes si une
   commune sort du groupement et les permissions de gestion intercommunale.
   Préserver dans tous les cas les droits acquis et l'historique des achats.

## Passage à la spécification

Appliquer le [cycle d'epic](../../organisation/cycle-epic.md) pour préciser le
référentiel, l'invariant territorial partagé, le modèle de permissions, les
contrats et la migration, puis relier E67-CA-01 à E67-CA-14 aux preuves attendues.
La règle de vente après changement d'adhésion et la compatibilité des lecteurs
doivent être arbitrées avant ouverture de la commercialisation intercommunale.
Ce cadrage ne constitue ni une spécification détaillée, ni une implémentation,
ni une modification du référentiel ou des offres de production.
