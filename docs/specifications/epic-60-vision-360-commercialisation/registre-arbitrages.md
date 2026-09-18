# Registre des arbitrages - Epic 60 - BackOffice ERP, referencement et commercialisation 360

## Consolidation pour implementation V1 - 2026-09-06

Decision complementaire utilisateur `ERP-NAV-01` (6 septembre 2026) : acces
Dashboard operationnel, Localeo Onboard et Localeo Control directement depuis
l'accueil ; regroupement des visions 360 ; section distincte Exploitation
courante ; referencement et administration organises par objet. Statut :
valide explicitement et implemente. Les habilitations et fiches canoniques
existantes sont conservees. Le detail figure dans la specification fonctionnelle.

Les 22 decisions explicites de l'utilisateur sont conservees. Sur sa delegation
de choisir les hypotheses sans attendre de confirmation, COM360-ARB-05/06 et
ERP-ARB-03 sont retenus sous H01/H02/H03. Cela ne constitue pas une nouvelle
validation utilisateur. Les hypotheses H01-H08 de la specification detaillee
et le rapport de developpement consignent leurs consequences.

Les precisions CON-01 a CON-09 sont retenues selon les contrats implementes.
CON-10 est qualifie sur la campagne PostgreSQL de reference ; les mesures et
leurs limites sont dans le rapport. Aucun arbitrage ne bloque l'implementation.

## Registre unique apres fusion

Ce document rassemble COM360-ARB-*, COM360-CON-* et les quinze ERP-ARB-* dont sept issus
de l'Epic 61. Les identifiants et validations sont conserves. La fusion est
decidee ; elle ne valide pas les propositions encore ouvertes.

La lecture seule proposee par COM360-ARB-05 concerne la file de diagnostic,
pas les ateliers de creation et modification inclus dans le perimetre global.
Son etat de confirmation reste ouvert.

## Arbitrages du volet diagnostic

| ID | Sujet | Proposition | Priorité | État |
| --- | --- | --- | --- | --- |
| `COM360-ARB-01` | Source du verdict | Utiliser exclusivement le diagnostic canonique de commercialisation partagé avec la Marketplace et le paiement. | P0 | Valide |
| `COM360-ARB-02` | Projection persistée | Conserver une projection minimale du verdict et de l'empreinte des causes pour accélérer les listes et détecter les transitions, sans copier les données métier. | P0 | Valide |
| `COM360-ARB-03` | États | Retenir `VENDABLE`, `NON_VENDABLE` et `INDETERMINE`; interdire qu'une erreur de diagnostic soit assimilée à vendable. | P0 | Valide |
| `COM360-ARB-04` | Priorité UX | Ouvrir la vue sur les coffrets non vendables, triés par sévérité puis ancienneté. | P0 | Valide |
| `COM360-ARB-05` | Actions | Rester en lecture seule au MVP et fournir des liens profonds vers les écrans propriétaires des données. | P0 | Retenu sous delegation H01 |
| `COM360-ARB-06` | Alertes | Alerter sur les transitions et l'empreinte des causes, puis résoudre automatiquement au retour à vendable. | P0 | Retenu sous delegation H02 |
| `COM360-ARB-07` | Canaux | Alertes BackOffice et Localeo Control obligatoires ; WebPush et email activables par configuration. | P1 | Valide |
| `COM360-ARB-08` | Réévaluation | Déclenchement événementiel complété par un batch de réconciliation et une action manuelle idempotente. | P0 | Valide |
| `COM360-ARB-09` | Données réussies | Afficher le détail des contrôles réussis dans la fiche, replié par défaut, afin d'expliquer le verdict sans surcharger la file. | P1 | Valide |
| `COM360-ARB-10` | Cohérence publique | Bloquer la livraison de toute nouvelle règle sans test de parité entre la Vision 360, la Marketplace et le paiement. | P0 | Valide |

## Historique des confirmations avant delegation

Les réponses positives utilisateur sont normalisees en `Valide`, y compris
celle de `COM360-ARB-02` initialement placée après la dernière colonne.
`COM360-ARB-05` est resté vide et `COM360-ARB-06` présente une saisie ambiguë :
leur confirmation a été demandée pendant la conception. La conception retient
les propositions du backlog comme hypothèses, sans enregistrer d'approbation
implicite. Les canaux optionnels et les contrôles réussis sont déjà approuvés
dans les lignes 07 et 09 ; ne pas les remettre à valider.

## Précisions de conception proposées

Les choix suivants rendent le MVP implementable ; ils ne constituent pas de
nouvelles validations produit déjà obtenues. Voir la
[conception technique](conception-technique.md) et les
[contrats API](contrats-api.md) pour leur sémantique complète.

| ID | Sujet | Choix proposé | État |
| --- | --- | --- | --- |
| `COM360-CON-01` | Exhaustivité et applicabilité | UNKNOWN obligatoire prime sur FAILED ; un contrôle inapplicable est explicitement non requis, jamais présenté comme réussi. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-02` | Prestations contrôlées | Conserver les contrôles des commerçants sur toutes les prestations comme le code actuel ; ajouter la garde au moins une prestation ACTIVE. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-03` | Contenu et flags | Promesse bloquante avec BUM actif sous son code historique ; promesse hors garde et contenu indicatif manquant en avertissements MVP. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-04` | Nouvelles exclusions | Prix positif, présence de prestation active et commune publiée contrôlés simultanément sur liste, détail et nouvel achat ; qualification des écarts avant bascule. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-05` | Référence coffret | UUID comme référence MVP, aucun champ distinct dans l'entité actuelle. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-06` | Tri | Sévérité décroissante puis début d'épisode le plus récent ; option les plus anciens d'abord. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-07` | Fraîcheur | File chaque minute, tour complet toutes les 15 minutes, expiration à 20 minutes ; invalidation immédiate sur mutation connue. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-08` | Alertes initiales et rechutes | Pas de fausse perte de vente au backfill ; incident initial alerté ; épisode renouvelé après résolution même à empreinte identique. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-09` | Rétention | Idempotence 24 h ; historique et alertes fermées 12 mois ; aucune purge d'alerte ouverte. | Retenu V1 ; voir contrat implemente et rapport |
| `COM360-CON-10` | Volumes et SLO | Référence proposée 10 000 coffrets / 100 000 prestations / 1 million de changements ; objectifs p95 du backlog mesurés selon le plan de tests. | Retenu V1 ; voir contrat implemente et rapport |


## Arbitrages du volet ERP

| ID | Sujet | Proposition | Priorite | Etat |
| --- | --- | --- | --- | --- |
| `ERP-ARB-01` | Perimetre ERP | Retenir une gestion integree de l'activite Localeo et un suivi leger des dossiers, sans comptabilite generale ni CRM complet au MVP. | P0 | Valide |
| `ERP-ARB-02` | Prestation avant choix du coffret | Permettre un modele de saisie commercant autonome, puis creer une prestation propre a chaque coffret avec provenance/version et conditions propres ; aucune propagation automatique des modifications. Inventorier les concepts existants avant creation du modele. | P0 | Valide |
| `ERP-ARB-03` | Droits de modification et d'activation | Definir une matrice de permissions par action : consulter, creer, modifier, activer/publier, intervenir sur la finance et administrer. Reutiliser les roles et perimetres territoriaux existants, avec controles serveur. | P0 | Retenu sous delegation H03 ; qualification fiscale ADMIN |
| `ERP-ARB-04` | Aptitude du commercant | Distinguer les controles obligatoires des recommandations de preparation. Chaque controle expose etat, motif, source, date et traitement ; dossier complet, statut ACTIF et aptitude financiere restent distincts. | P0 | Valide |
| `ERP-ARB-05` | Suivi des dossiers de referencement | Integrer le dossier Onboard, sa prochaine action, son responsable et son echeance deja persistes. Preciser l'affectation nominative avant une file Mes dossiers ; pas de nouveau moteur de taches ni de relances automatiques. | P1 | Valide |
| `ERP-ARB-06` | Organisation des menus | Retenir six rubriques : Mon activite ; Commercants et catalogue ; Operations ; Finance ; Supervision ; Referentiels et administration. Tester les libelles et destinations sur les taches frequentes. | P0 | Valide |
| `ERP-ARB-07` | Deploiement des nouveaux parcours | Basculer directement sur les nouveaux parcours sans maintenir les anciennes interfaces : le back-office n'est pas encore utilise. Reutiliser les services metier et la stack ; inventorier les fonctions a reintegrer avant retrait. | P0 | Valide avec ajustements - decision utilisateur |

## Nouveaux arbitrages - iteration 2

Ces propositions proviennent de la [revue produit](revue-produit-iteration-2.md).
Elles ne modifient pas les validations COM360 deja acquises. Les precisions
CON-02/04/06 doivent etre confirmees avec les arbitrages ci-dessous avant
d'activer de nouvelles exclusions. Le principe de priorite aux pertes est
desormais valide par ERP-ARB-10 ; le departage technique reste a preciser.

| ID | Sujet | Proposition | Priorite | Etat |
| --- | --- | --- | --- | --- |
| `ERP-ARB-08` | Un seul onboarding | Reutiliser DossierOnboardingCommercant, son cycle et ses capacites dans la fiche 360 ; aucun second statut de preparation persistant ni moteur de checklist. | P0 | Valide |
| `ERP-ARB-09` | Verification avant publication | Simuler explicitement l'etat cible ACTIVE via le moteur canonique, puis recontroler et appliquer atomiquement la commande ; ne pas exiger un verdict courant VENDABLE sur un BROUILLON. | P0 | Valide |
| `ERP-ARB-10` | Brouillons et pertes de vente | Conserver le defaut NON_VENDABLE mais distinguer preparation, perte observee, incident et retrait volontaire ; proposer les pertes d'offres en tete, sans cacher les brouillons. Le tri detaille CON-06 reste a ajuster apres decision. | P0 | Valide |
| `ERP-ARB-11` | Causes partagees | Conserver les impacts et alertes par coffret, les regrouper visuellement par ressource source et faciliter une action unique de traitement ; aucun effacement des transitions individuelles. | P1 | Valide |
| `ERP-ARB-12` | Ventes futures et engagements existants | Afficher deux analyses d'impact avant retrait/modification ; appliquer les regles existantes de versions, fermeture et traitement des achats, sans propagation silencieuse. | P0 | Valide |
| `ERP-ARB-13` | Lecture de la rentabilite | Distinguer marge sur prix, commission theorique, marge cible et flux reels ; expliciter frais non integres ; conserver la degradation autorisee Epic 28. | P0 | Valide |
| `ERP-ARB-14` | Premiere livraison utile | Prioriser un parcours vertical Onboard -> offre -> coffret -> controles -> publication -> suivi ; harmoniser ensuite le reste des menus sans retirer le perimetre demande. | P0 | Valide |
| `ERP-ARB-15` | Cloture et archivage | Distinguer cloture/abandon du dossier, retrait de l'offre et archivage commercant ; motifs et dependances verifies, engagements et preuves conserves ; pas de suppression metier generique. | P0 | Valide |

## Historique des propositions

| Iteration | Evolution | Effet sur les decisions |
| --- | --- | --- |
| Fusion 60/61 | Regroupement du diagnostic et des ateliers ERP | Fusion decidee ; validations individuelles conservees |
| Iteration 2 | Onboard existant verifie ; ERP-ARB-02 et 05 affines ; ajout ERP-ARB-08 a 15 | Propositions ouvertes lors de la revue initiale |
| Cadrage V1 | Prise en compte des reponses utilisateur au registre | 22 decisions acquises ; 3 arbitrages ouverts ; ERP-ARB-07 remplace la coexistence progressive par une bascule directe |

La precedente proposition d'un cycle de preparation A_COMPLETER/BLOQUE/
PRET_A_ACTIVER/INDETERMINE est retiree de la recommandation au profit du
cycle Onboard existant (ERP-ARB-08). Sa finalite d'explication des blocages
reste conservee dans les capacites et la qualite des donnees.

## Travaux a lancer pendant les specifications

Le perimetre, le principe du modele d'offre, la reutilisation Onboard, les six
rubriques et la bascule directe sont decides. Ne pas les remettre en arbitrage.
Il reste a detailler le schema d'offre, les preuves d'aptitude, les commandes,
la migration et la matrice de droits ERP-ARB-03. La confirmation des actions
de file COM360-ARB-05 et du cycle d'alertes COM360-ARB-06 reste ouverte.

La decision ERP-ARB-07 prime sur les anciennes propositions de coexistence.
Texte utilisateur conserve : « On migre directemet sur les nouveaux parcours
sans maitenir les existants car personne n'utilise encore le backofffice ».
ERP-ARB-14 organise le developpement et la recette du parcours vertical ; il
n'impose pas des interfaces anciennes et nouvelles ouvertes en parallele.

## Saisie des decisions

Renseigner l'etat de chaque ligne : `Valide`, `Valide avec ajustements`,
`Refuse` ou `A preciser`. En cas d'ajustement, consigner la decision retenue
ci-dessous pour distinguer la proposition initiale de la regle acceptee.
Une priorite indique l'ordre des decisions, pas leur approbation.

| ID | Decision retenue / ajustements | Date | Decideur |
| --- | --- | --- | --- |
| `ERP-ARB-01` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-02` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-03` | | | |
| `ERP-ARB-04` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-05` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-06` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-07` | Bascule directe sur les nouveaux parcours, sans maintien des anciens | Date non renseignee | Utilisateur |
| `ERP-ARB-08` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-09` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-10` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-11` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-12` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-13` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-14` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
| `ERP-ARB-15` | Proposition validee dans le registre utilisateur | Date non renseignee | Utilisateur |
