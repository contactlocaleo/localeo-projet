# E71 — Parcours simples de Localeo CRM

[Version V1 et arbitrages](README.md). Comportements cibles V1.1 du 3 novembre 2026, **non implémentés**.

## Navigation PC et mobile

PWA distincte **Localeo CRM**, avec entrée autorisée depuis l'ERP et lancement direct après installation. Vues principales : **Aujourd'hui**, **Prospects**, **Suivi**, **Rappels**. Imports et préférences dans le menu secondaire ; aucune entrée d'administration sans droit. L'en-tête reprend l'identité partagée, le nom de l'application et l'environnement hors production. Retour ERP seulement si destination autorisée.

Sur PC, menu latéral et listes compactes exploitant la largeur disponible. Sur mobile, navigation principale accessible au pouce, listes en cartes et filtre dans un panneau ; aucune table débordante imposée. Une action principale par écran, actions secondaires regroupées. Icônes accompagnées de libellés pour les actions métier ; actualisation compacte avec nom accessible. Zones tactiles de 44 px au minimum, focus visible, statuts exprimés par texte et icône en plus de la couleur.

Un seul défilement du contenu, titres/retours cohérents, formulaires courts et aide près du champ. Revenir à la liste conserve recherche, filtres, tri, position et mode liste/carte. Le bouton retour du navigateur reste utilisable. Recherche côté serveur, pagination à la demande, pas de téléchargement complet du portefeuille. Une note non enregistrée déclenche une confirmation avant sortie ; un échec conserve le texte dans la page, sans persistance privée hors ligne.

Le mode hors connexion affiche un écran explicite de reconnexion : ni prospect en cache ni commande différée envoyée à la reconnexion. La PWA reste utile sans notifications autorisées. Chargement, vide, erreur et succès sont distincts ; succès seulement après confirmation serveur. Le délai réseau d'une mutation impose la relecture du résultat avant répétition.

## 1. Commencer sa journée — CA-05/06/22

« Aujourd'hui » montre d'abord mes actions en retard, puis celles du jour, puis les prochaines. Un filtre explicite permet de voir l'équipe, avec le même portefeuille global autorisé. Une section secondaire signale les dossiers actifs sans responsable/contact/prochaine action ; l'incomplétude n'empêche pas d'enregistrer un prospect.

Compteurs : prospects actifs distincts, dossiers ouverts par périmètre/étape, rappels en retard, dossiers sans prochaine action, gains vérifiés sur la période. Une structure Animation et Coffrets compte une fois comme prospect et deux fois comme dossiers. Les estimations facultatives ne deviennent jamais un chiffre d'affaires ; pas de prévision financière ou score de probabilité en V1.

## 2. Ajouter un prospect — CA-01/02/10

Formulaire rapide : **nom de la structure, périmètre et objet commercial**. Le titre du dossier peut être prérempli par le libellé du périmètre/objectif, sans inventer de besoin. Les coordonnées et le contact peuvent être ajoutés ensuite. Le responsable du dossier est l'utilisateur créateur par défaut pour la saisie manuelle, modifiable vers un utilisateur actif autorisé à gérer le CRM.

Une fiche prospect porte nom, type facultatif (collectivité, association, commerce, entreprise/CSE, autre), adresse/commune/INSEE facultatifs, coordonnées de structure, source, état actif/archivé et version. Une commune hors catalogue est admissible ; résolution explicite au centre communal, sans géocodage d’adresse ni création/publication d'une ville marchande.

Chaque contact porte nom, fonction, e-mail/téléphone professionnels connus et état actif/obsolète. Au moins un nom ou une coordonnée valide est nécessaire. Plusieurs contacts sont possibles ; un départ rend le contact obsolète sans supprimer son histoire. Les coordonnées de structure ne remplacent pas automatiquement celles d'une personne.

Chaque dossier appartient à un prospect, avec périmètre **ANIMATION** ou **COFFRETS**. Coffrets exige un objectif **PARTENARIAT_COMMERCANT** ou **ACHAT_ENTREPRISE_CSE**. Plusieurs dossiers du même périmètre sont possibles pour des campagnes successives. Le responsable, l'étape, la priorité normale/haute et les tâches sont propres au dossier.

Avant création, montrer les ressemblances (nom/commune, coordonnées), sans fusion automatique. Une correspondance certaine exige un identifiant CRM ou de source déjà établi ; nom ou e-mail générique commun ne suffisent jamais. Créer un prospect ne crée ni client, commerce, accès, souscription, commande ou e-mail.

## Carte interactive — CA-07/13/14/15

Dans **Prospects**, bascule « Liste / Carte » sans changer de filtre : périmètre/objectif, étape du dossier, responsable, priorité, commune/département et état actif/archivé. Un prospect ayant plusieurs dossiers correspondants apparaît une seule fois comme structure ; le groupe indique séparément prospects et dossiers.

La carte présente des centres communaux intitulés **« Localisation à la commune — approximative »**, jamais l'adresse exacte d'un contact. Les points superposés sont regroupés ; cliquer sur un groupe ouvre une liste paginée de prospects et leurs dossiers correspondant aux filtres, puis la fiche. Sur mobile, le panneau s'ouvre sous la carte ; retour conserve filtres, zone et zoom. Les contrôles sont nommés et accessibles au clavier ; la liste offre toutes les actions sans manipuler la carte.

Compteur « Sans commune identifiée » ouvrant une liste dédiée, toujours inclus dans le total du portefeuille. L'INSEE résolu et son centre sont séparés de la commune textuelle source. Nom ambigu ou code postal partagé : choix explicite parmi les candidats, ou laisser à qualifier. Une panne du référentiel n'empêche pas la saisie/import ; une panne du fond de carte affiche un réessai et le retour à la liste.

Couverture proposée : France métropolitaine et Outre-mer couverts par le référentiel, sélecteur de zones pour ne pas rendre les points illisibles. Une commune non couverte reste dans la liste avec son état, jamais placée sur un point arbitraire. Aucun GPS personnel nécessaire pour consulter les prospects. Le fournisseur de fond reçoit seulement les requêtes nécessaires aux tuiles, aucune fiche, note ou coordonnée de contact.

## 3. Suivre et consigner un échange — CA-03/04

Six étapes : **À contacter**, **En discussion**, **Proposition envoyée**, **Gagnée**, **Perdue**, **En pause**. Sauts et retours sont autorisés entre étapes actives, avec trace ; pas de formulaire de qualification imposé avant chaque étape. Perte : motif obligatoire. Pause : motif et date de réexamen ; échéance = signal à reprendre, pas réouverture automatique. Réouverture d'un dossier terminal : action explicite et motif.

Conserver les preuves de gain décidées en octobre : partenariat commerçant accepté avec commerce et dossier OnBoard liés ; Animation avec souscription activée payée ou gratuite ; achat Coffrets avec commande payée. Le serveur lit les preuves canoniques. Un accord oral peut être noté en discussion ; il ne certifie pas le gain. Le changement d'étape n'active aucun objet métier. Les tâches ouvertes sont présentées lors de la clôture pour annulation/réalisation explicite, jamais supprimées en silence.

**Unicité du gain confirmée (ARB-04b).** Une même commande payée, souscription
activée ou acceptation commerçant ne peut faire gagner qu’un seul dossier CRM.
Plusieurs dossiers peuvent conserver un lien de consultation, clairement distinct
de l’attribution du gain. Un conflit indique que la preuve est déjà attribuée et
propose le dossier détenteur si l’utilisateur est autorisé à le consulter.

Réouvrir, perdre ou archiver le dossier ne libère pas automatiquement sa preuve.
Le même dossier peut retrouver son état gagné avec cette preuve si elle est encore
éligible ; cela ne compte pas une seconde vente. La V1 ne propose pas de transfert
silencieux d’attribution entre dossiers. Les indicateurs de gains comptent les
preuves canoniques distinctes et affichent leur période ; la chronologie conserve
chaque transition. Un gain est un constat commercial à sa date, pas une nouvelle
attestation de paiement : consulter l’état financier courant dans le domaine métier.

Dans la fiche, **Ajouter une note** est immédiatement visible. Types courts : note, appel, rendez-vous, e-mail consigné. Texte libre limité à 10 000 caractères, date réelle de l'échange, auteur et date de saisie serveur. Les corrections sont versionnées/tracées ; elles ne remplacent pas l'audit. Une note disant « e-mail envoyé » n'envoie rien et ne prouve aucune délivrance. Après enregistrement, proposer « Programmer la prochaine action » sans l'imposer.

Les échanges globaux sont rattachés au prospect, ceux d'une affaire à son dossier ; la chronologie de la fiche indique ce contexte. Ni import ni réouverture ne réécrivent les notes, décisions ou preuves historiques.

## 4. Programmer et recevoir un rappel — CA-05/06/26/27

Action depuis la fiche ou un dossier : libellé, type (appel, e-mail, rendez-vous, préparation, suivi), responsable, échéance et rappel. Une sollicitation désigne explicitement sa cible : un contact actif du prospect (`contact_id`) ou la structure (`cible=STRUCTURE`, coordonnées de structure). Canal explicite pour appel/e-mail/rendez-vous/suivi sollicitant ; une préparation interne est marquée non sollicitante. L’opposition de la structure bloque toutes ses cibles ; une opposition de contact bloque les tâches qui le ciblent. Si sa coordonnée est réutilisée comme coordonnée de structure, le blocage reste applicable à cette coordonnée normalisée : pas de contournement par changement de libellé. Une tâche peut appartenir au prospect sans dossier ; si un dossier est indiqué, il doit appartenir au même prospect. Proposition simple : rappel à l'échéance par défaut ; l'utilisateur peut fixer une date/heure antérieure. Pas de récurrence automatique en V1.

Dates affichées en **Europe/Paris**, instants stockés UTC avec fuseau ; les heures inexistantes ou ambiguës au changement d'heure demandent correction/choix explicite. Une date seule nécessite une heure confirmée. Terminer exige un résultat court, annuler un motif ; reporter conserve l'ancienne échéance et invalide l'ancien rappel. La « prochaine action » est calculée depuis la première tâche ouverte, pas un deuxième champ éditable.

Le rappel interne est toujours disponible. **WebPush** est activé volontairement par appareil depuis les préférences ; aucun prompt navigateur avant un clic explicite. Refus, navigateur non compatible ou abonnement expiré : message clair, file interne intacte. À l'ouverture, la notification mène à la tâche après authentification, puis contrôle les droits courants.

**E-mail facultatif** : préférence personnelle désactivée initialement. Un message à la même échéance, adressé à l’adresse vérifiée du compte interne du responsable, jamais au contact du prospect. La vérification est liée à la version d’adresse courante par Identité interne (consommation d’un lien valide d’initialisation/réinitialisation), pas au seul état actif du compte. Changer l’adresse suspend l’option jusqu’à vérification puis nouvel opt-in pour cette adresse. Sans adresse interne vérifiée disponible, l’option e-mail est indisponible avec explication ; la file interne et le push restent utilisables. Activer l'e-mail en plus du push peut produire un message sur chaque canal choisi ; aucun basculement e-mail implicite après refus du push. Aucun rattrapage massif lors de la première activation d'un canal : tâches déjà échues restent dans la file interne.

Un rappel n'est produit qu'une fois par tâche/révision d'échéance/destinataire/canal (et abonnement pour le push). Réaffectation, annulation, réalisation, archivage, perte de droits ou changement de préférence annulent les envois encore en attente ; recontrôle avant remise au transport. Un message déjà remis au fournisseur ne peut pas être rappelé et ne prouve pas la lecture. En cas d'issue incertaine, distinguer cet état d'un échec certain ; pas de promesse de livraison « exactement une fois » par un fournisseur externe.

Notifications discrètes : « Une action commerciale vous attend », sans nom, note, téléphone ou e-mail de prospect sur écran verrouillé. Notification interne et état de tâche restent la référence même si l'envoi échoue. Les erreurs sont observables et les retries bornés ; jamais de boucle de renvoi à chaque visite.

## 5. Importer — CA-08 à 12/28

Parcours **Fichier → Aperçu → Confirmation → Bilan**. Choisir source stable, mode INIT/UPSERT et responsable des nouveaux dossiers (opérateur par défaut). Télécharger le [modèle](modele-import.csv), puis préparer le CSV selon le [contrat d'import](import-carte.md). L'aperçu montre créations, compléments, valeurs conservées, conflits et rejets. Aucune conversion, tâche ou notification n'est déclenchée par l'import.

## 6. Passer au métier — CA-16/17/18

Depuis un dossier, rechercher puis rattacher une référence canonique existante, ou ouvrir le parcours ERP/OnBoard autorisé et revenir rattacher son résultat. Les droits CRM et métier se cumulent ; un accès CRM ne donne pas un accès Animation, Pro, Finance ou SQLAdmin. Aucun contact/note dans l'URL de retour. En cas d'interruption après création métier, chercher le résultat existant ; ne pas recréer automatiquement.

Conserver la fiche, ses contacts, notes et rappels après gain/rattachement : c'est la continuité de la relation client. Support, facturation, contrats, livraison et gestion opérationnelle restent dans leurs applications ; aucun ticket ou paiement dupliqué dans le CRM.

## Opposition et archivage — CA-20

Proposition simple : **Ne plus contacter** au niveau prospect (tous ses contacts) ou contact, pour toutes les sollicitations commerciales. Enregistrement immédiat par gestionnaire CRM, motif/source/date/acteur ; une levée requiert l'administration CRM et une justification/provenance explicites. Cette simplification remplace la proposition antérieure d'opposition configurable par axe/canal ; la levée demeure sensible.

La saisie manuelle, l'import et les tâches utilisent la même règle. Les tâches de sollicitation ouvertes deviennent bloquées et leurs rappels externes sont annulés ; notes factuelles et préparation interne restent possibles. Une tâche « préparation » ne permet pas d'y cacher une demande d'appel ; le canal/type sollicitation est explicite. Archiver interdit de nouvelles sollicitations et retire la fiche des vues actives ; réactiver ne lève pas l'opposition. Aucune cellule CSV ne réactive un contact obsolète, une fiche archivée ou une opposition.
