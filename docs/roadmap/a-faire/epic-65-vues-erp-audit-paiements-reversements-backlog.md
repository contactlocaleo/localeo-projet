# EPIC 65 — Vues ERP audit, paiements et reversements

## Références

- Date de cadrage : **26 septembre 2026**.
- Identifiant : **EPIC-65**, disponible après recherche dans la roadmap commune,
  ses identifiants applicatifs et les documents des dépôts voisins.
- État produit : **À faire**, selon la [roadmap commune](../README.md).
- Demande : disposer dans Localeo ERP d’une vue des événements d’audit et de
  deux vues de suivi, « Paiements » et « Reversements », sous « Paiements et facturation ».
- Phase réalisée : **cadrage et spécification V1** ; voir le
  [dossier canonique](../../specifications/epic-65-vues-erp/README.md).
  Aucune implémentation livrée. Priorité et date de livraison non fixées.

### Rattachement et dépendances

L’[EPIC 60](../terminees/epic-60-vision-360-commercialisation-backlog.md) fournit
le socle ERP, sa navigation et les ateliers de référencement/commercialisation.
Cette nouvelle epic porte trois vues opérationnelles identifiables, au-delà des
raccourcis existants. Elle réutilise ce socle sans rouvrir sa clôture, ni l’EPIC 61
fusionnée. Les règles et écrans métier déjà livrés restent leurs dépendances :

- [EPIC 30](../terminees/epic-30-vue-360-reversements-paiements-backlog.md) : suivi
  360 des reversements et campagnes, à intégrer sans le reconstruire.
- [EPIC 39](../terminees/epic-39-stripe-connect-psp-backlog.md) et
  [EPIC 43](../terminees/epic-43-suivi-payouts-bancaires-stripe-connect-backlog.md) :
  états financiers, transferts et suivi bancaire.
- [EPIC 51](../terminees/epic-51-vision-360-achats-backoffice-backlog.md) et
  [EPIC 14](../terminees/epic-14-documents-achat-et-facturation-coffret-backlog.md) :
  achats, pièces et facturation liées aux paiements.
- [EPIC 44](../terminees/epic-44-observabilite-logs-use-cases-backlog.md) :
  corrélation et observabilité ; les événements d’audit persistés restent distincts
  des logs techniques d’exécution.

Les états de ces epics et l’abandon du paiement manuel de l’EPIC 12 sont conservés.
Le [dossier ERP existant](../../specifications/epic-60-vision-360-commercialisation/README.md)
et les spécifications de ces dépendances sont les points d’entrée pour la conception.

## Problème et résultat attendu

**Constat vérifié sur le code local**, backend `7049de7`, projet `631fd10` :
les trois entrées de [la navigation ERP](../../../../localeo-backend/app/infrastructure/erp/erp.js)
renvoient actuellement vers des listes SQLAdmin (`paiement-orm`, `reversement-orm`,
`evenement-audit-orm`). La consultation existe donc déjà, mais elle quitte le
parcours ERP. Une console métier de reversements existe aussi dans
[le backend](../../../../localeo-backend/app/infrastructure/admin/admin.py), sous
`/internal/reversements/vue-360` ; elle couvre déjà suivi, filtres et actions financières.
Les listes Audit, Paiements et Reversements sont déjà en lecture seule. La vue
paiements porte `PaiementOrm`, relié aux achats et commandes ; une projection
de paiements par achat existe dans la Vision 360 Achats. Aucun moteur financier
nouveau n’est nécessaire. Ce constat ne constitue pas une recette de l’environnement déployé.

**Acteurs :** exploitation et support habilités pour l’audit, finance et support
habilités pour les paiements et reversements. **Accès initial conservé : ADMIN.**
Les [droits historiques](../../../../localeo-backend/app/security/backoffice.py)
sont plus restrictifs que ceux du [socle ERP](../../../../localeo-backend/app/security/erp.py),
qui accepte aussi EXPLOITATION avec un périmètre communal. L’intégration ne doit
donc pas ouvrir automatiquement ces trois vues au rôle EXPLOITATION.

**Résultat attendu :** rechercher une opération, comprendre son état et accéder
à son dossier depuis une vue ERP lisible, sans devoir parcourir des tables
techniques. Exemple : partir d’un paiement, retrouver l’achat et ses pièces,
puis consulter les événements associés ; partir d’un reversement pour distinguer
le transfert vers le compte Stripe du commerce du virement vers sa banque.

## Périmètre proposé pour la première livraison

### Événements d’audit

- Vue intégrée à la rubrique de supervision ERP, avec liste et détail en lecture seule.
- Recherche par référence métier ou identifiant de corrélation et filtres par
  période, action/type, acteur, ressource et résultat, selon les données disponibles.
- Présentation des dates avec fuseau explicite, libellés compréhensibles, acteur,
  opération, issue, objet concerné et liens vers les fiches accessibles.
- Métadonnées utiles en détail à la demande, assainies selon les habilitations ;
  une information absente reste « non renseignée », sans acteur ou succès supposé.

### Paiements — rubrique « Paiements et facturation »

- Liste et détail des paiements enregistrés, avec référence, objet payé, date,
  payeur autorisé, montant/devise, état et références utiles au diagnostic.
- Recherche et filtres période, état, contexte/origine disponible et référence ;
  accès aux achats/commandes et pièces ou demandes de facture réellement liées.
- Indicateurs sur le même périmètre que la liste, sans confondre montant payé,
  remboursé, commission et net ; aucun total additionnant plusieurs devises.
- États de paiement et disponibilité/statut des pièces affichés séparément :
  facture présente ne signifie pas paiement encaissé, pièce absente ne signifie
  pas paiement échoué. La vue ne déclenche aucune génération documentaire.

Le libellé « Paiements et facturation » désigne ici la rubrique d’accueil des
deux vues financières ; la demande ne crée pas un nouvel atelier de facturation.
Le cadrage part de `PaiementOrm`, actuellement exposé par cette entrée ERP ; une
couverture exhaustive des abonnements et des autres modèles d’encaissement reste
à inventorier avant de promettre une vue financière universelle.

### Reversements — même rubrique

- Intégrer dans le parcours ERP les lectures et informations utiles de la vue
  360 existante : période/campagne, commerçant, mouvements, reversement,
  paiements associés, montants, état et blocages.
- Détail de la composition du reversement et liens vers le commerce et les
  opérations sources, avec chronologie disponible et anomalies compréhensibles.
- Distinguer explicitement « fonds transférés au compte Stripe » et « virement
  bancaire » ; un payout groupé n’est pas présenté comme un virement individuel
  de chaque reversement. Une association inconnue reste signalée comme telle.
- Conserver l’accès aux actions déjà autorisées dans leurs parcours existants.
  Aucun nouvel ordre financier n’est lancé par une consultation ou actualisation.

### Contraintes communes et exclusions

- Utiliser l’enveloppe ERP et la largeur disponible sur ordinateur : filtres,
  tableaux et détail cohérents, sans multiplier les textes et écrans intermédiaires.
- Pagination complète, tris stables, filtres conservés lors du retour à la liste,
  distinction chargement/absence de résultat/erreur, clavier et petits écrans utilisables.
- Une ressource conserve sa source et sa fiche canoniques ; les règles restent
  dans le domaine backend, les vues consomment leurs projections.
- Pas de modification/suppression d’événements d’audit, de nouveau collecteur
  de logs, de nouveaux calculs financiers ou de changement de rétention.
- Pas de nouvelle commande de paiement, remboursement, transfert, virement,
  rapprochement ou émission de facture ; pas de réactivation du paiement manuel.
- Pas de refonte des portails publics/partenaires, de stack ERP supplémentaire,
  d’export de masse nouveau ni de suppression globale de SQLAdmin dans ce cadrage.

Découpage possible : navigation et composants communs, vue audit, vue paiements,
puis intégration du suivi reversements. Chaque vue doit être utilisable de bout
en bout avant d’être annoncée disponible ; cet ordre reste une proposition.

## Critères d’acceptation

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E65-CA-01 | Opérateur habilité dans l’ERP | Ouvrir Audit, Paiements ou Reversements | Une vue ERP intégrée s’ouvre ; les deux dernières sont sous « Paiements et facturation ». La simple consultation ne redirige plus vers une liste SQLAdmin. |
| E65-CA-02 | Opérateur audit, événements sur plusieurs périodes/acteurs | Combiner filtres et recherche puis ouvrir un événement | Seuls les événements correspondants sont affichés, avec détail, ressource et corrélation disponibles ; aucun événement n’est modifié. |
| E65-CA-03 | Finance/support autorisé, paiements de plusieurs états | Rechercher une référence, filtrer, ouvrir le paiement | Montant/devise, état et dates proviennent de la source ; le dossier associé est accessible selon les droits ; aucune donnée manquante n’est présentée comme un succès. |
| E65-CA-04 | Paiement avec pièce ou demande liée, et autre sans pièce | Consulter la section facturation | Liens existants ou absence explicite ; paiement et facturation restent distincts, aucun document ni nouvelle demande n’est créé par consultation. |
| E65-CA-05 | Finance, reversement composé de plusieurs mouvements | Filtrer par période/commerce et ouvrir le détail | Composition, totaux, étapes et blocages concordent avec la vue métier canonique ; les accès aux actions existantes restent soumis aux mêmes droits. |
| E65-CA-06 | Reversement transféré, virement en attente/échoué/groupé | Consulter la progression bancaire | Transfert et virement apparaissent séparément ; ni faux versement bancaire confirmé, ni montant groupé attribué à chaque commerce. |
| E65-CA-07 | Liste sur plusieurs pages et, le cas échéant, plusieurs devises | Filtrer, paginer, ouvrir puis revenir | Aucun élément omis ou doublonné ; filtres conservés ; compteurs et totaux portent sur tout le périmètre filtré et gardent les devises séparées. |
| E65-CA-08 | Acteur sans rôle ADMIN, dont EXPLOITATION, ou hors périmètre autorisé | Accéder par menu, URL directe, API ou lien documentaire | Refus serveur cohérent ; l’accès au socle ERP ne suffit pas. Aucune fuite de données personnelles, bancaires, secrets ou métadonnées brutes non autorisées. |
| E65-CA-09 | Réseau indisponible ou réponse partielle | Charger/actualiser l’une des trois vues | Erreur ou incomplet visible avec reprise de lecture ; jamais « aucun paiement », « tout payé » ou total zéro fabriqué ; aucune commande financière ni appel fournisseur de mutation. |
| E65-CA-10 | Opérateur bureau, clavier ou petit écran | Filtrer, consulter le détail et revenir | Largeur desktop exploitée, actions lisibles et accessibles, détail secondaire à la demande, aucune information essentielle inaccessible. |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Applications et domaine propriétaire | **Concerné :** backend ERP, exploitation/audit, gestion achats, gestion reversement et domaines de facturation. Services de lecture existants à réutiliser. **Sans modification prévue** des trois frontends : seules des données issues de leurs parcours sont consultées. |
| API et consommateurs | **À examiner :** réutilisation des services ERP/360, éventuels contrats internes paginés manquants, permissions et liens documentaires. Aucun contrat public à changer par défaut. Si nouvelle API, source OpenAPI canonique dans ce dépôt et génération dans le backend. |
| Persistance et historique | **À examiner :** sources des dates/statuts, événements anciens incomplets, index de recherche et coûts d’agrégation. Aucun nouvel état financier ni migration imposé à ce stade ; besoin d’index à mesurer. |
| Démonstration et fixtures | **Concerné :** couvrir événements réussis/échoués, paiement sans pièce, paiement/remboursement, reversement bloqué, virement en attente/échoué/groupé et accès refusé. Examiner les données existantes de l’EPIC 63 avant d’adapter son générateur ; aucune opération bancaire réelle pour préparer ces scénarios. |
| Documentation fonctionnelle | **Concerné :** navigation ERP, guide support/audit et guide finance ; renvoyer vers les règles des EPIC 30/39/43/51 au lieu de les recopier. Les états historiques de la roadmap restent conservés. |
| Exploitation et déploiement | **À examiner :** volumétrie audit/finance, pagination, index, permissions, diagnostic d’une lecture indisponible, liens entrants et ordre API/vue. Conserver les politiques de masquage et de rétention existantes. |

## Questions ouvertes pour la spécification

La [spécification du 26 septembre](../../specifications/epic-65-vues-erp/README.md)
répond à l’inventaire des sources et formalise les hypothèses H01/H02 : paiements
d’achats/commandes existants, souscriptions hors agrégation, consultation et liens
vers actions existantes. Les questions ci-dessous conservent leur portée produit ;
aucune absence de réponse n’est assimilée à une validation d’extension.

1. **Couverture des paiements :** inventorier les sources réellement couvertes par
   l’entrée actuelle ; préciser si abonnements et financements Animation doivent
   être agrégés dès cette livraison ou accessibles via leurs dossiers existants.
   Cela conditionne les projections et indicateurs, pas la vue audit.
2. **Actions de la vue reversements :** la proposition conserve des liens vers
   les actions existantes. Déterminer lesquelles intégrer ensuite directement
   dans l’ERP, avec leurs confirmations, droits et reprises existants.
3. **Données affichées et ouverture ultérieure :** fixer les champs autorisés du
   détail audit et financier et leur masquage. L’accès initial reste ADMIN ;
   une ouverture à EXPLOITATION nécessiterait une décision et un périmètre
   territorial explicites. Elle ne bloque pas la livraison ADMIN.
4. **Recette et priorité :** convenir d’un jeu représentatif, des volumes cibles
   et de l’ordre des trois vues. Aucun délai ni objectif de performance chiffré
   n’est supposé validé.

## Passage à la spécification

Le besoin et les trois vues sont spécifiés selon le
[cycle d’epic](../../organisation/cycle-epic.md). Les
[contrats et responsabilités](../../specifications/epic-65-vues-erp/architecture-contrats.md)
et la [matrice de preuves](../../specifications/epic-65-vues-erp/verification-livraison.md)
portent la préparation de l’implémentation. Les dix critères restent inchangés.
Les extensions H01/H02 restent à confirmer si elles sont souhaitées ; le périmètre
de consultation décrit peut être préparé indépendamment. Les tests fonctionnels
et la recette sont **à réaliser** ; le contrôle de liens documentaire ne vaut
ni validation métier ni livraison des vues. L’état produit reste **À faire**.
