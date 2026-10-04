# EPIC 68 — Processus d'onboarding commerçant en sept étapes

Spécification **V1.2 — 3 octobre 2026**. État produit : **En cours**, selon le
[backlog canonique](../../roadmap/en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md).
Ce dossier décrit la V1.2 implémentée localement ; les preuves et limites figurent
dans la [vérification de livraison](verification-livraison.md). Aucun envoi réel
ni recette déployée n'est attesté. L'historique des décisions reste dans le backlog.
Les 31 identifiants E68-CA-01 à 31 restent stables.

## Objectif et périmètre

Mettre en place un seul processus, du référencement à la finalisation contrôlée
du dossier. Le gestionnaire est guidé dans l'ERP ; le commerçant prépare son
rendez-vous d'une heure dans son propre compte puis apprend à utiliser Localeo.
Les **sept étapes** ci-dessous restent la référence métier et de recette. Elles
ne doivent pas imposer sept formulaires principaux au gestionnaire : l'écran
OnBoard privilégie l'action utile et un suivi lisible.

Réutiliser OnBoard, l'identité commerçant, les documents internes, Stripe hébergé,
le référentiel des prestations, les transports email/SMS, l'ordonnanceur et les
habilitations existantes. Adapter leurs intégrations nécessaires au parcours.
La V1.2 ne comporte ni dépôt de pièces par le commerçant, ni compte temporaire,
ni nouveau fournisseur de signature, ni création automatique Teams. Elle ne crée
pas de CRM, de moteur générique de workflows, de produit analytique, de refonte
fiscale/financière ou de sas de modification des prestations déjà applicables.

## Correction ergonomique OnBoard du 3 octobre 2026

La vue courante se concentre sur trois gestes :

1. **Activer le commerçant** avec l'action existante lorsqu'elle est disponible.
   L'activation et ses conditions restent distinctes de la finalisation du dossier.
2. **Vérifier et confirmer le mail de préparation**. Planifier le rendez-vous si
   nécessaire, puis présenter l'aperçu et les destinataires. Le SMS associé est
   annoncé explicitement lorsqu'il fait partie de la séquence ; aucun envoi ne
   résulte de la seule activation ou sauvegarde du rendez-vous.
3. **Suivre l'état du dossier** : rendez-vous, communications et éléments restant
   à traiter sont lisibles sans ouvrir de formulaire. Les questions, prestations,
   actions, modifications du rendez-vous et fin de réunion se déplient au besoin.

Les détails de préparation sont repliés par défaut, sans masquer un blocage ni
supprimer une action métier. La section « Bilan du pilote OnBoard » est retirée
de l'interface. Les données historiques et API de mesure sont conservées.
La liste garde la recherche, le statut et le suivi de préparation visibles ; les
filtres de dates, référent, commune et blocage se regroupent dans « Plus de filtres ».
La création explique le choix entre commerçant existant et nouveau commerçant ;
le rendez-vous se renseigne ensuite dans le dossier. Les libellés, l'affichage
mobile et la navigation au clavier doivent permettre le traitement quotidien
sans vocabulaire technique de configuration.
L'onglet principal « À faire et suivi » garde les prochaines actions au premier
plan. Les rubriques de détail restent accessibles au clavier et l'enregistrement
conserve la rubrique ouverte dans le même dossier. « Vérifier le dossier »,
« Valider le dossier » et « Terminer le dossier » nomment les actions existantes
sans changer leurs conditions d'exécution.
Les confirmations par séquence, permissions et protections de concurrence restent
inchangées. Cette correction concerne le rendu ERP, sans modification de contrat,
de migration, du générateur ou des applications satellites.

## 1. Référencer et ouvrir le dossier

**Gestionnaire Localeo :** créer le commerçant par une entrée métier autorisée,
vérifier les coordonnées connues, identifier interlocuteur/signataire et affecter
un référent. La création ouvre ou rattache le dossier OnBoard unique dans la même
transaction. Un réessai retrouve ce dossier ; une modification de profil n'en crée pas un autre.

**Résultat :** dossier accessible depuis la fiche et la file ERP, checklist et
prochaine action visibles, même sans rendez-vous. Aucun pack E68, aucune activation
ou mise en vente implicite. Email et mobile sont demandés pour le parcours nominal ;
un mobile absent bloque le SMS, pas le mail valide, et appelle un autre contact.

**Critères :** CA-18/20/21/22.

## 2. Planifier le rendez-vous

**Référent :** saisir date, heure, fuseau, durée d'une heure, interlocuteur Localeo,
modalité Teams ou présentiel. Le lien Teams est facultatif et peut être ajouté
ultérieurement ; s'il est renseigné, il doit être HTTPS. L'adresse est obligatoire
en présentiel. Un rendez-vous incomplet sur les autres informations requises reste
à compléter et ne déclenche pas de communication.

**Système :** préparer l'email léger de confirmation avec fichier calendrier,
ainsi que les échéances du pack J−7 et du rappel J−1. Le gestionnaire prévisualise
et confirme explicitement l'envoi de l'email de rendez-vous. La sauvegarde du
rendez-vous seule n'autorise rien ; cette validation n'autorise pas le pack futur.
Le calendrier conserve la même identité lors d'un report.

**Critères :** CA-01/19/29.

## 3. Préparer et confirmer les communications

**Système :** à J−7 configurable globalement, préparer un pack « À confirmer ».

**Gestionnaire :** vérifier l'email et le mobile destinataires, le rendez-vous,
les contenus, les pièces jointes et la fenêtre d'envoi ; confirmer l'envoi du
mail et du SMS nominal ensemble. Annuler, fermer ou ne pas répondre n'envoie rien.
Le dossier conserve auteur, date et version approuvée ; le double clic est sans doublon.

Le mail contient les actions de préparation, la liste personnalisée des éléments
à préparer, l'accès à l'espace, les modalités de lecture du contrat et les
prestations déjà saisies. Deux supports sont joints : déroulé du rendez-vous et
présentation Localeo/Stripe. Ils doivent être approuvés et disponibles.

Le SMS annonce le mail seulement après sa prise en charge certaine. Chaque canal
a son suivi ; une livraison technique ne prouve pas la lecture. Un échec certain
peut préparer un secours à confirmer distinctement. Une issue incertaine impose
un rapprochement avant reprise. Une modification des éléments approuvés avant
remise invalide l'autorisation et demande une nouvelle confirmation.
Les confirmations de rendez-vous, rappels, secours et correctifs n'héritent
jamais de l'autorisation du pack. Les communications d'identité existantes
restent distinctes des séquences E68, mais leur demande est accessible depuis
le bouton « Créer mon mot de passe » du pack. La confirmation du pack prépare
l'identifiant manquant, sans envoyer d'invitation séparée ; le commerçant demande
ensuite son lien personnel en saisissant son email. Un compte déjà configuré
peut rejoindre directement sa préparation par le lien secondaire.

**Critères :** CA-03/09/23/24/25/26.

## 4. Accompagner la préparation

**Commerçant :** accéder à son compte existant, l'initialiser ou le récupérer
via les parcours d'identité existants si nécessaire, puis arriver directement
sur la préparation. Aucun second compte ni droit commercial anticipé.

Il confirme la réception, pose ses questions, consulte/télécharge le contrat
courant en PDF pour lecture et impression, prépare les pièces selon les consignes
et examine ou propose ses prestations initiales. Il peut déclarer sa lecture ;
cette déclaration est facultative et ne vaut jamais signature. Aucun téléversement
de pièces n'est disponible. Le contrat reste à signer le jour J.
Les démarches d'identité et bancaires Stripe se font sur Stripe, depuis l'accès
existant du profil. Aucun justificatif sensible n'est demandé par email.

**Référent :** répondre aux questions, examiner les prestations et leurs versions,
partager les corrections attendues, suivre les contrôles documentaires/Stripe,
affecter les actions restantes. Une note interne ne remplace pas l'accord du
commerçant sur les conditions ; sa réponse seule ne résout pas une question :
le commerçant confirme la résolution ou la rouvre.

L'espace montre seulement les éléments autorisés de ce dossier, sans notes internes.
Une ouverture de lien ou un scanner d'email ne produit aucune confirmation.
Une pièce à apporter n'est pas reçue ou vérifiée ; une proposition ne publie rien.

**Critères :** CA-02/04/05/06/07/08/10/27/28.

## 5. Faire le point avant J

**Référent :** examiner réception, accès, contrat, questions, prestations et
contrôles restants ; décider de maintenir, maintenir avec objectifs adaptés
ou proposer un report. Enregistrer motif, responsable et prochaine action.

**Système et gestionnaire :** préparer le rappel J−1 puis en confirmer l'envoi
distinctement, sans les supports du pack. Sans validation, l'action reste visible.
Un report recalcule les échéances et invalide les communications périmées ;
l'avis de report ou d'annulation doit lui aussi être confirmé. Les bonnes preuves
sont conservées. Aucun rappel obsolète après le rendez-vous.
Un défaut d'accès ou une pièce prévue le jour J peut justifier un maintien adapté,
sans transformer une réserve en preuve de préparation complète.

**Critères :** CA-11/12/13/30.

## 6. Conduire le rendez-vous

| Durée indicative | Actions des deux parties |
| --- | --- |
| 10 minutes | Questions, attentes et difficultés restantes |
| 15 minutes | Dossier et pièces, contrat et état Stripe ; signature après questions, version applicable et habilitation du signataire contrôlées |
| 10 minutes | Confirmation des prestations examinées avant J et de leurs conditions |
| 25 minutes | Pratique sur l'appareil habituel, exercice accompagné, autonomie et bilan |

L'exercice utilise un scénario de démonstration sans achat, consommation ou
paiement réel et sans partage de mot de passe. Un dépassement est consigné ;
une vérification nécessaire n'est pas supprimée pour tenir l'heure.
En Teams, organiser la remise de la copie signée par un moyen existant adapté.

**Critères :** CA-14/15 ; la signature reste couverte par CA-05.

## 7. Enregistrer et finaliser

**Gestionnaire :** récupérer ou numériser la copie signée et la déposer dans
le dossier documentaire interne ; contrôler version, signataires, date réelle
de signature, lisibilité et contrôles documentaires requis. Le dépôt ne crée
pas la signature et ne vaut pas validation automatique du document.

Enregistrer tenue/absence, durée réelle, autonomie et actions restantes avec
responsable et échéance ; partager le bilan sans notes internes. Une absence
appelle un contact, jamais un abandon automatique.

Finaliser explicitement l'inscription uniquement sur preuves actuelles. Si une
copie signée, un contrôle obligatoire ou Stripe reste en attente selon les fonctions
visées, le dossier reste à compléter. Une preuve modifiée rouvre son contrôle.
La réunion tenue, la signature et la finalisation sont distinctes. Aucune prestation
ni aucun coffret n'est obligatoire pour l'inscription ; les capacités commerciales
gardent leurs conditions propres.

**Critères :** CA-16, avec contrôles documentaires CA-04/05.

## Exigences transverses et lecture du dossier

- **CA-17 :** mesures à partir des dossiers, durées, relances et autonomie ;
  dénominateurs explicites et données manquantes conservés dans les API existantes.
  Le tableau pilote ne fait plus partie de l'écran opérationnel OnBoard.
- **CA-31 :** [guide backoffice](../../produit/formation/backend/guide-preparation-onboarding-commercant.md)
  suivant les mêmes sept étapes, accessible depuis l'ERP et le dossier OnBoard.
- [Architecture et contrats](architecture-contrats.md) : propriétaires, règles,
  accès, API cibles, calendrier, confirmations, reprises et persistance.
- [Communications et supports](communications-supports.md) : modèles par étape
  et sources des supports à produire et approuver.
- [Vérification et livraison](verification-livraison.md) : matrice des 31 critères,
  recette en sept étapes, tests, configuration, migration et preuves de conception.

Les étapes sont un parcours utilisateur, pas sept nouveaux statuts métier.
La préparation, l'issue du rendez-vous, la finalisation et les capacités restent
distinctes. Un lot partiel ne vaut pas livraison du processus complet.

## Paramètres V1.2 et décisions du 3 octobre 2026

| Référence stable | Décision encore nécessaire | Limite actuelle |
| --- | --- | --- |
| ARB-01 | Validé : Europe/Paris, 10 h, fenêtre 9–18 h | J−7 global configurable en jours calendaires ; une échéance prépare seulement une demande de confirmation |
| ARB-04 | Validé : revue J−2 et contact humain après 48 h sans retour | Référent responsable et actions datées ; pas de relance automatique sans confirmation |
| ARB-06 | Validé : clarté, faisabilité, prix, conditions, capacité à honorer et réserves BUM | Examen Backoffice sans calcul automatique de rentabilité ; accord et versions obligatoires |
| ARB-07 | Approbation éditoriale des supports, notamment frais Stripe conformes à la convention | Sources rédigées, PDF/rendu et diffusion à valider |
| ARB-08 | Validé : rappel J−1 par SMS à 10 h | Envoi à confirmer ; contact humain après 48 h, aucun suivi J+2 automatique retenu |
| ARB-10 | Validé : reprise des anciens dossiers sur décision du gestionnaire | Pas de campagne ou réouverture massive à la migration |

ARB-02 (durées), ARB-03 (même espace sans dépôt), ARB-05 (signature jour J et dépôt
interne après rendez-vous) et ARB-09 (confirmations d'envoi) sont résolus et intégrés
aux étapes ci-dessus. Seule l'approbation éditoriale ARB-07 reste attendue avant diffusion.
