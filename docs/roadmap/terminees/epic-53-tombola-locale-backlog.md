# Backlog Epic 53 - Tombola locale des commercants

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Moyenne`.
- Statut : `Termine`.
- Objectif : permettre a une commune ou un partenaire d'organiser une tombola locale dans laquelle un achat valide chez un commercant participant qualifie une personne pour un tirage final.
- Modele cible : `TOMBOLA_LOCALE`.
- Dependances : Epics 41, 42, 46, 47, 48 et 49.

Voir [le cadrage fonctionnel](../../specifications/epic-53-tombola-locale/README.md), [le registre des arbitrages](../../specifications/epic-53-tombola-locale/registre-arbitrages.md) et [la conception technique](../../specifications/epic-53-tombola-locale/conception-technique.md).

### Avancement backend

- tranche 1 engagee : contrat de strategie, registre des modeles, resultat canonique de qualification ;
- strategie Passeport adaptee au contrat commun sans suppression de l'API historique ;
- strategie et catalogue `TOMBOLA_LOCALE` ajoutes avec les constantes du MVP ;
- catalogue migre vers une table normalisee administrable, avec specificites
  JSONB et version ; avertissements de modification portes uniquement par
  SQLAdmin ;
- service applicatif d'evaluation de participation ajoute ;
- prochaine tranche : brancher l'evaluation canonique sur les validations, le pilotage et le gel de la population.

## MVP acte

- une inscription par personne et par tombola ;
- un achat sans montant minimum chez n'importe quel commercant participant ;
- validation de l'achat par scan du QR participant depuis l'application commercant ;
- une seule chance au tirage, quel que soit le nombre d'achats ;
- un tirage final sur une population eligible figee ;
- lots constitues de coffrets Localeo achetes et reserves par le partenaire ;
- notification des participants et remise des gains par les processus existants.

## Responsabilites par surface

### Backoffice / backend Localeo

- enregistrer le modele `TOMBOLA_LOCALE`, ses regles et son reglement par defaut ;
- appliquer l'eligibilite `au moins une validation effective` ;
- garantir l'unicite de la chance au tirage ;
- reutiliser inscription, population figee, tirage, suppleants, gains et audit ;
- exposer la supervision, les anomalies, les validations et les resultats ;
- executer les clotures et notifications automatiques via les batchs existants.

### Localeo Animation

- proposer la Tombola dans le catalogue des modeles ;
- configurer dates, commercants, lots, regles et contenus publics ;
- acheter et reserver les coffrets constituant les lots ;
- suivre inscriptions, validations, eligibles et repartition par commercant ;
- cloturer, lancer le tirage, traiter les suppleants et envoyer les gains ;
- consulter et exporter le bilan.

### Marketplace

- rendre la tombola visible sur les surfaces territoriales et commercants eligibles ;
- afficher dates, principe, commercants, lots et reglement ;
- orienter vers le parcours d'inscription sans dupliquer le moteur d'animation ;
- retirer la tombola de la decouverte selon les regles publiques de l'Epic 49.

### Localeo Live

- permettre l'inscription ou la reprise d'une participation ;
- conserver le QR participant dans le carnet local ;
- afficher la qualification au tirage apres validation ;
- notifier ouverture, validation, cloture, resultat et mise a disposition du gain ;
- afficher l'historique de la participation sans reveler les autres participants.

### Application commercant

- afficher les tombolas auxquelles le commercant participe ;
- scanner le QR du participant et confirmer qu'un achat a ete effectue ;
- empecher les validations dupliquees ou hors periode ;
- afficher un accusé de validation et des compteurs non nominatifs ;
- permettre la consultation de l'historique utile au support.

## User Stories

### PRD-496 - Declarer le modele Tombola locale

En tant que produit Localeo, je veux disposer d'un modele distinct afin d'appliquer des regles et un reglement propres a la tombola.

### PRD-497 - Configurer une tombola

En tant que gestionnaire, je veux definir sa periode, ses commercants et ses lots afin de preparer sa publication.

### PRD-498 - Publier et rendre visible la tombola

En tant que visiteur, je veux decouvrir les tombolas de ma commune depuis la Marketplace et Localeo Live.

### PRD-499 - S'inscrire a la tombola

En tant que participant, je veux m'inscrire sans compte obligatoire et conserver mon QR.

### PRD-500 - Valider un achat

En tant que commercant, je veux scanner le QR apres un achat afin de qualifier le participant.

### PRD-501 - Calculer l'eligibilite

En tant que systeme, je veux accorder une seule chance apres la premiere validation effective.

### PRD-502 - Cloturer et tirer les gagnants

En tant que gestionnaire, je veux figer les eligibles et realiser un tirage rejouable et auditable.

### PRD-503 - Notifier les participants

En tant que participant, je veux etre informe de ma validation et du resultat du tirage.

### PRD-504 - Envoyer les gains

En tant que gestionnaire, je veux attribuer les coffrets aux gagnants et utiliser les suppleants si necessaire.

### PRD-505 - Piloter la tombola

En tant que partenaire, je veux suivre les inscriptions, validations, eligibles, gains et statistiques par commercant.

### PRD-506 - Superviser la tombola

En tant qu'operateur Localeo, je veux consulter son etat, ses anomalies et sa chronologie depuis le Backoffice.

## Hors perimetre MVP

- chances multiples proportionnelles au nombre ou au montant des achats ;
- preuve par ticket de caisse photographie ;
- tirages instantanes apres chaque achat ;
- lots autres que les coffrets Localeo ;
- federation de plusieurs communes dans une meme tombola.

## Definition de termine

- le modele peut etre configure, valide, publie et cloture de bout en bout ;
- une validation commercant qualifie une seule fois le participant ;
- la population du tirage est figee et auditable ;
- les gains sont envoyes avec les notifications attendues ;
- chaque surface n'expose que les actions relevant de sa responsabilite ;
- le bilan distingue inscriptions, validations, eligibles et activite par commercant.


## Correctifs de préproduction ANIM — 7 septembre 2026

Le [guide Animation et sa recette](../../produit/formation/backend/guide-animation-preproduction.md)
complète les critères de clôture, qualification, calendrier, financement et suivi
asynchrone. Les corrections ANIM-001 à ANIM-014 sont suivies dans le dépôt Animation;
leur validation technique ne vaut pas activation en production. Le statut produit
de cette epic reste inchangé.


## Compléments Animation

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### Synthese

- Modele : `TOMBOLA_LOCALE`.
- Dependances : Epics 41, 46, 48, 49 et 56.
- Backend : socle et catalogue persistant engages ; integration transactionnelle en cours.

Voir le [cadrage](../../specifications/epic-53-tombola-locale/README.md), la
[conception](../../specifications/epic-53-tombola-locale/conception-technique.md) et
le [registre](../../specifications/epic-53-tombola-locale/registre-arbitrages.md).

### Tranche A - Catalogue generique

- charger et indexer les modeles actifs par `code` ;
- supprimer les libelles limites au Passeport ;
- gerer indisponibilite, desactivation et fallback historique ;
- tester Passeport et Tombola.

### Tranche B - Configuration Tombola

- ajouter la carte et le detail ;
- construire le formulaire depuis la definition ;
- verrouiller les constantes MVP ;
- integrer acceptations Epic 56 et financement Epic 46 ;
- traiter `REGLE_TOMBOLA_NON_MODIFIABLE`.

### Tranche C - Pilotage et execution

- afficher inscriptions, validations, eligibles et statistiques ;
- afficher readiness et anomalies ;
- cloturer et afficher la population gelee ;
- lancer le tirage, gerer suppleants/gains et exporter le bilan.

### Criteres d'acceptation

- aucune eligibilite calculee dans le frontend ;
- aucun libelle limite a un ternaire Passeport ;
- une Tombola active est configurable de bout en bout ;
- un modele desactive reste lisible historiquement ;
- constantes MVP non editables ;
- erreurs avec `correlationId` ;
- aucune regression Passeport.

### Recette transverse

- appliquer la migration backend du catalogue ;
- verifier `TOMBOLA_LOCALE` dans `GET /modeles` ;
- tester desactivation/reactivation dans le Backoffice de recette ;
- valider juridiquement le reglement ;
- recetter avec l'application commercant, Marketplace et Localeo Live.

### Correctifs ANIM de préproduction — 7 septembre 2026

Les critères de qualification, clôture, calendrier et suivi sont complétés par les [contrats corrigés](../../specifications/securisation-production/contrats-animation.md) et la [formation](../../produit/formation/animation/guide-animation-preproduction.md). Le statut produit de cette epic reste inchangé. Les preuves de test et les conditions d’activation figurent dans le [suivi de remédiation](../../audits/animation/remediation-2026-09-06.md).
