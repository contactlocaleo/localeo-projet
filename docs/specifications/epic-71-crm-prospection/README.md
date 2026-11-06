# EPIC 71 — Localeo CRM, prospection Animation et Coffrets

Spécification **V1.3 — 6 novembre 2026**, détaillant **E71-EVOL-05/06/07** sur le
socle V1.2/E71-EVOL-04. [Backlog et critères](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md).
État produit : **En cours** dans la [roadmap](../../roadmap/README.md). V1.3 désigne
la version de conception, pas une release applicative : les fonctions d’actualisation et de calcul sont maintenant implémentées localement,
avec migrations v295–v298, API privées, workers et PWA. Leur activation sur un
environnement et les preuves de capacité restantes sont décrites dans le bilan. [Prise en main actuelle](guide-utilisateur.md),
[exploitation](exploitation.md) et [preuves](verification-livraison.md).

**Évolution demandée le 5 novembre 2026 — E71-EVOL-05 :**
[vérifier et actualiser la qualification à la demande](actualisation-qualification.md).
Parcours, adoption, sources, jobs et contrats cibles détaillés ; neuf critères,
implémentation locale des six blocs, comparaison et adoption explicite ; sources réelles à préparer avant activation. **Choix confirmé le 6 novembre : les six
blocs dès la première livraison**, y compris potentiel/comptages et compétences.
Les méthodes et adaptateurs correspondants doivent être prêts pour cette livraison.

**E71-EVOL-06, 5 novembre 2026 :** [niveau de qualification commerciale](niveau-qualification.md).
Entrée Qualification, calcul sur tous les résultats d’une recherche et carte
colorée/filtrable. Choix utilisateur confirmé : combinaison **potentiel, maturité
du projet et fiabilité**, avec **priorité au fort potentiel, même sans projet
engagé**, confirmée le 6 novembre. Révision du barème et contrats de
capture/calcul/carte implémentés et testés localement ; dix critères dont la couverture complète reste à lire dans le bilan.

**E71-EVOL-07, 5 novembre 2026 :** [dates des actions plus explicites](parcours-regles.md#e71-evol-07--dates-des-actions-plus-explicites).
Libellés « Action prévue le » et « Me rappeler le », aides et cohérence des écrans,
sans changement des règles. **Implémentation locale du 6 novembre vérifiée**,
CA-60/61 ; aucun déploiement effectué.
L’ensemble compte désormais **61 IDs, 60 actifs et CA-24 reporté**.

## Préparation des nouvelles évolutions — 6 novembre 2026

| Périmètre | Existant vérifié | Cible et préparation |
| --- | --- | --- |
| Actualisation E71-EVOL-05, CA-41–49 | API et worker de vérification, six blocs normalisés, aperçu paginé et adoption atomique | Implémentation locale ; [sources régionales](referentiels-qualification.md), conservation et capacité à préparer avant activation réelle |
| Niveau E71-EVOL-06, CA-50–59 | Menu Qualification, recherche et capture, calcul durable, axes invalidables et carte colorée | Seuils confirmés commune 5/10, EPCI 20/50 ; activation indépendante et capacité à vérifier |
| Dates E71-EVOL-07, CA-60–61 | Champs et calendrier fonctionnels ; anciens libellés encore présents dans `d928b9a` | « Action prévue le » / « Me rappeler le », aides et erreurs cohérentes ; implémentation locale et tests réussis le 6 novembre, déploiement restant |
| Recherche, CA-07/13/35 | Département, qualification, contacts, projets et responsable déjà filtrables | [Catalogue partagé](parcours-regles.md#recherche-partagée--ca-0713355054), puis ajouts niveau/état/profil dans E71-EVOL-06 ; pas de seconde sémantique de recherche |
| Correctifs du 6 novembre | Sept corrections backend jusqu’à `d928b9a`, dont responsable propre au prospect et filtre des rappels par type | Conservés dans les parcours cibles ; migration v294 appliquée sur TEST après sauvegarde le 6 novembre. Ce constat ne valide pas E71-EVOL-05/06/07 |

Réponses utilisateur du 6 novembre :

- **Actualisation complète dès la première livraison** : identité, territoire,
  potentiel, activité, structure et contacts. Le découpage progressif proposé
  n’est pas retenu ; un bloc sans adaptateur ne vaut pas livraison complète.
- **Barème 40/35/25 à revoir, non retenu en l’état**. Priorité confirmée aux
  prospects à fort potentiel, même sans projet engagé. L’absence de dossier,
  de budget ou d’interlocuteur ne doit donc pas empêcher ce classement ; elle
  reste visible pour préparer la prise de contact. Le potentiel inconnu n’est
  pas assimilé à un potentiel nul.

Les seuils commune 5/10 et EPCI 20/50 et la base de comptage sont confirmés le
6 novembre : établissements actifs de proximité des six familles CRM, dédupliqués
par SIRET ; cas incertains et contrôle terrain distincts. Le mapping technique
versionné et la conservation ARB-07 restent à documenter. Le choix ne valide ni l’ancien seuil de 70/100 ni la
couverture globale de 80 %. Aucun nouveau coefficient n’est présenté comme validé.

Les textes de rappel sont implémentés localement. La suite peut avancer sur les composants
indépendants (droits, jobs, capture, comparaison et mocks fournisseurs). Aucun
profil de scoring non validé ni source non qualifiée ne doit être activé sur le
portefeuille réel. Les preuves prévues sont des tests unitaires, d’intégration,
fonctionnels et de capacité ; aucun pilote commercial ou compte rendu externe
n’est ajouté comme condition de clôture.

## Objectif

Une PWA **Localeo CRM** simple pour savoir qui contacter, retrouver les échanges et préparer la prochaine action. Elle couvre **Animation** et **Coffrets**, avec une même fiche prospect et plusieurs contacts/dossiers commerciaux si nécessaire. Les comptes sont ceux de l'ERP ; les droits CRM sont attribués distinctement dans l'ERP.

L'utilisateur voit des **Prospects**, des **Dossiers commerciaux** et des **Rappels**. Le terme technique « opportunité » désigne un dossier commercial, pas une deuxième fiche prospect à remplir. Coffrets distingue le recrutement d'un commerçant partenaire de l'achat de coffrets par une entreprise/CSE ; « Pro » ne désigne ici ni l'application commerçant ni un accès salarié.

## Périmètre V1 retenu

- **Aujourd'hui** : mes rappels en retard, du jour et à venir ; dossiers actifs sans prochaine action ; raccourcis « Nouveau prospect » et « Ajouter une note ».
- **Prospects** : recherche, filtres, fiche contacts, chronologie, notes et dossiers Animation/Coffrets ; suivi conservé après rattachement à un client existant.
- **Carte interactive** : prospects de Nouvelle-Aquitaine regroupés par commune, filtre par département partagé avec la liste et accès aux fiches ; localisation communale indicative, y compris hors catalogue Localeo.
- **Territoire de saisie temporaire** (4 novembre 2026) : création et modification effective de localisation limitées à une commune de Nouvelle-Aquitaine, identifiée par son code INSEE. Même règle métier pour la saisie manuelle, la localisation et les imports INIT/UPSERT. Les fiches historiques hors région ou sans commune restent consultables et modifiables pour leur suivi et contacts ; aucune suppression ni migration. Les conditions et limites du contrôle des imports sont détaillées dans [Import CSV](import-carte.md#territoire-ouvert-à-la-prospection).
- **Suivi commercial** : liste et vue par étapes, responsable, priorité simple, prochaine action et résultat gagné/perdu ; aucun devis ou paiement recréé dans le CRM.
- **Rappels** : tâches datées, report/annulation/réalisation, notification interne persistante, WebPush volontaire et e-mail facultatif au responsable interne.
- **Imports** : CSV standard produit depuis Excel, aperçu puis confirmation, modes INIT et UPSERT sans écrasement du suivi commercial.
- **Application installable** : identité visuelle des applications de gestion Localeo, navigation PC/mobile, mêmes comptes internes, accès CRM distinct.

Compléments recommandés inclus dans la conception : responsable et prochaine action visibles, détection des doublons avant création, « Ne plus contacter », archivage réversible, filtres mémorisés dans l'URL et indicateurs simples. Le socle n’inclut pas de scoring automatique ; E71-EVOL-06 ouvre séparément un calcul déterministe de priorité commerciale, sans paramétrage de pipeline complexe ni scoring IA.

## Lire et préparer le fichier

| Document | Utilité |
| --- | --- |
| [Parcours et règles](parcours-regles.md) | Écrans, saisie rapide, étapes, notes, rappels, passage aux parcours métier |
| [Import INIT / UPSERT](import-carte.md) | Colonnes, clés stables, exemples et protection des données existantes |
| [Modèle CSV vide](modele-import.csv) | En-têtes exacts à remplir depuis Excel ; aucune donnée réelle |
| [Qualification structurée — E71-EVOL-04](qualification-structuree.md) | Attributs de potentiel/terrain, identité légale, territoire, fiabilité des contacts et qualification des projets ; règles et contrats cibles |
| [Actualisation à la demande — E71-EVOL-05](actualisation-qualification.md) | Sources, comparaison et adoption, contrats, reprise et tests locaux ; préparation des référentiels requise avant activation |
| [Niveau de qualification — E71-EVOL-06](niveau-qualification.md) | Seuils validés, capture, calcul, invalidation par axe, carte et tests locaux ; réserves de capacité dans le bilan |
| [Modèle CSV format 2](modele-import-qualification-v2.csv) | 21 colonnes conservées et 64 facultatives/conditionnelles ; format 1 conservé par défaut, format 2 choisi explicitement |
| [Architecture et contrats](architecture-contrats.md) | PWA, profils ERP, domaine, API, notifications, concurrence et capacité |
| [Vérification et livraison](verification-livraison.md) | Tests exécutés et réserves, traçabilité, migrations et activation |

## Ce qui change par rapport à octobre

| Décision antérieure | Cible E71-EVOL-03 |
| --- | --- |
| Module Prospection dans l'ERP, sans nouvelle PWA | **Remplacé par la demande** : PWA Localeo CRM autonome en navigation ; identité et attribution des droits restent dans l'ERP |
| Droits CRM automatiquement portés par Lecteur/Backoffice | **Remplacé par la demande** : autorisations CRM explicites ; aucun droit CRM automatique pour les comptes non administrateurs existants |
| Rappels uniquement dans l'ERP | **Étendu par la demande** : file CRM + WebPush opt-in + e-mail facultatif, destinés à l'équipe interne |
| Import propre au classeur Gironde, profils mensuels et comparaison à trois versions | **Choix utilisateur confirmé le 3 novembre** : CSV normalisé, identifiants stables et enrichissement des champs vides uniquement ; les divergences restent à traiter dans la fiche |
| Carte interactive | **Maintien confirmé par l’utilisateur le 3 novembre** : carte communale, filtres, groupes et accès aux fiches ; CA-13 actif |
| Sections communales « Coffrets & élus 2026 » | Report confirmé avec l’ancien import Gironde ; CA-24 conservé comme reporté, jamais présenté comme validé |
| Preuves de gain et rattachement explicite aux parcours métier | **Conservés** : règles décidées le 9 octobre ; l'import ou un statut ne crée ni accès, ni abonnement, ni commande |

E71-EVOL-01 (import mensuel) et E71-EVOL-02 (deux destinations du classeur) restent des décisions historiques ; leur réalisation spécifique est reportée sur choix utilisateur confirmé le 3 novembre. Un réimport régulier reste possible avec le CSV standard. L'analyse historique du classeur reste dans l'historique Git ; elle n'est plus le contrat d'import courant. Aucun ancien fichier n'a été relu, modifié ou importé ici.

La carte est explicitement maintenue en V1. Le CSV standard seul et le report du traitement spécifique Gironde sont confirmés par l’utilisateur. Les choix techniques ci-dessous décrivent la conception ; le bilan de vérification distingue l’implémentation locale, les preuves acquises et les limites.

## Arbitrages et préparation

### E71-EVOL-04 — qualification structurée, 4 novembre 2026

La demande porte sur la spécification des concepts utiles du classeur comme
attributs et relations : potentiel et évaluations datées, contrôle terrain,
identité/nature des structures, appartenance EPCI, profil d’activité, fiabilité
des contacts et projet Animation (porteur, besoin, calendrier et budget).
Les attributs sont facultatifs, avec preuves conditionnelles pour déclarer un
fait vérifié. Les inconnus ne deviennent pas zéro ou « non ». Le classement est
calculé depuis l’évaluation de référence ; priorité et étape restent des décisions
commerciales distinctes. Les évaluations successives ne remplacent pas les
corrections humaines et le format 1 continue de fonctionner.

Le [dictionnaire et les contrats](qualification-structuree.md) définissent la
cible. **CA-30 à CA-40 sont ajoutés**, soit 40 identifiants dont 39 actifs et
CA-24 toujours reporté. Les 28 critères actifs précédents et leurs preuves sont
conservés ; les onze nouveaux critères sont implémentés localement et leurs preuves fonctionnelles/capacité sont consignées dans le bilan. La demande
ne réalise ni migration ni import réel. La politique de conservation ARB-07
reste une condition d’activation avec données réelles.

### Arbitrages du socle conservés

| Identifiant conservé | Décision ou proposition actuelle | Conséquence |
| --- | --- | --- |
| E71-ARB-01 | CSV standard seul en V1 confirmé ; format technique retenu : UTF-8 point-virgule, version 1, INIT/UPSERT, 10 Mio / 10 000 lignes | Modèle fourni ; aucun import XLSX direct ni parseur Gironde en V1 |
| E71-ARB-02 | Acquis : Coffrets comprend partenaires commerçants et achats entreprises/CSE | Deux objectifs sous un périmètre Coffrets |
| E71-ARB-03 | WebPush demandé ; e-mail facultatif proposé, désactivé initialement | Un rappel à l'échéance choisie, pas de campagne vers les prospects |
| E71-ARB-04 | Preuves de gain du 9 octobre conservées ; six étapes recommandées | « Gagnée » ne signifie pas accord verbal sans preuve métier |
| E71-ARB-04b | Confirmé : une même preuve canonique ne fait gagner qu’un seul dossier ; liens de consultation multiples possibles | Attribution unique transactionnelle et refus concurrent ; réouverture sans libération implicite de la preuve |
| E71-ARB-05 | Droits distincts demandés ; consultation, gestion, import et administration proposés | Comptes ERP conservés ; les anciens droits ERP ne sont pas retirés par cette évolution |
| E71-ARB-06 | Carte interactive maintenue sur décision utilisateur ; centres communaux et liste de secours | Couverture métropole/Outre-mer proposée ; fournisseur/licence/quotas à fixer avant activation, aucune ville commerciale créée |
| E71-ARB-07 | Blocage de sollicitation et protection d'opposition conservés ; durées de conservation CRM non établies | Politique par catégorie à valider avant données réelles ; développement et tests synthétiques possibles |
| E71-ARB-08 | Acquis : ouvrir le parcours métier autorisé, puis rattacher son résultat | Aucune conversion automatique à l'import |
| E71-ARB-09 | Actualisé le 4 novembre 2026 : adresse CRM dédiée demandée | `crm.localeo.city` / `test-crm.localeo.city`, même backend et chemins `/internal/crm/`. Même compte et mêmes droits ERP, connexion distincte par domaine ; anciens accès conservés. Activation DNS/HTTPS et `CRM_PUBLIC_ORIGIN` selon le [guide d'exploitation](exploitation.md#domaine-dédié) |

Le périmètre V1 est implémenté et testé localement sur données synthétiques, avec les réserves détaillées dans le bilan. ARB-01 et ARB-04b sont confirmés ; la conservation ARB-07 conditionne l’activation avec données réelles. La configuration du fournisseur cartographique et des référentiels reste nécessaire avant activation ; toutes les cibles de performance ne sont pas validées. Les preuves historiques portent sur 39 critères actifs : 28 du socle et 11 de l’extension. E71-EVOL-05/06/07 ajoutent 21 critères : 60 actifs au total, CA-24 reste reporté. Tests unitaires, intégration et fonctionnels requis, sans pilote commercial ni compte rendu externe obligatoire.

## Décisions confirmées et revue de finalisation

Le 3 novembre, l’utilisateur confirme explicitement : **une preuve de gain pour
un seul dossier** et **CSV standard uniquement en V1**. La carte interactive,
confirmée auparavant, reste active (CA-13). CA-24 est reporté sur ce périmètre
confirmé, sans être coché comme testé.

La revue V1.1 complète les contrats d’import (sources, décisions, plan immuable,
états/bilan), la détection de doublons concurrente entre sources et la preuve de
vérification d’adresse interne nécessaire aux rappels e-mail. Les responsabilités
restent respectivement Prospection et Identité interne. La matrice a été définie lors de cette spécification. Les parcours désormais
implémentés, leurs tests exécutés et les réserves figurent dans le
[bilan de vérification](verification-livraison.md).
