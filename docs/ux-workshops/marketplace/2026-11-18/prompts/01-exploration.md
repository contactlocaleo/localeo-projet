# ÉTAPE 1 — INITIALISATION ET EXPLORATION UX MARKETPLACE LOCALEO

Tu es chargé de préparer un workshop UX complet consacré à la marketplace publique Localeo.

## 1. Accès

URL : https://coffret.localeo.city

Explore l'application publique sans authentification dans un premier temps.

Si certains parcours nécessitent une connexion, demande un compte de test autorisé.

N'utilise aucune donnée bancaire réelle.

## 2. Contexte produit

La marketplace Localeo est la vitrine publique de l'écosystème Localeo.

Elle présente :
- Les communes présentes dans l'écosystème.
- Les coffrets d'expériences locales.
- Les commerçants et leurs savoir-faire.
- Les animations et leur calendrier.
- Les possibilités d'achat de coffrets.

Un coffret Localeo est un **parcours d'expériences locales**, associant plusieurs prestations proposées par des commerçants d'une commune.

Il ne s'agit pas d'un colis de produits matériels ni d'une simple carte cadeau générique.

La plateforme doit donner envie de découvrir une commune, ses commerces et ses expériences.

## 3. Objectifs de l'audit

Analyser six parcours :

### A — Première impression
Compréhension de l'offre, attractivité, lisibilité et navigation.

### B — Découverte des coffrets
Recherche, exploration, comparaison, détails, prestations, prix et conditions.

### C — Pages communes et commerçants
Présentation des territoires, visibilité des commerces, découverte des offres et cohérence des liens.

### D — Animations
Calendrier communal, découverte des événements, informations et accès à la participation.

### E — Achat
Sélection d'un coffret, compréhension de la commande, éventuelle identification, informations demandées et transition vers Stripe.

### F — Confiance et envie d'offrir
Compréhension du produit, conditions d'utilisation, parcours du bénéficiaire, réassurance et crédibilité.

## 4. Initialisation

Détermine la date locale au format YYYY-MM-DD.

Crée :

`docs/ux-workshops/marketplace/YYYY-MM-DD/`

Si un workshop distinct existe déjà ce jour-là, utilise un suffixe -02, -03, etc.

Crée :
- `prompts/`
- `observations/`
- `workshop/`
- `visuels/captures-avant/`
- `visuels/maquettes-apres/`
- `validation/`
- `synthese/`

Initialise `README.md` avec la date, l'URL, la branche Git, le commit, l'objectif et le statut.

## 5. Archivage des prompts

Prépare :
- `prompts/00-protocole-global.md`
- `prompts/01-exploration.md`
- `prompts/02-workshop.md`
- `prompts/03-maquettes.md`
- `prompts/04-validation.md`
- `prompts/05-archivage.md`

Enregistre cette instruction complète dans `01-exploration.md`.

Ne prétends pas disposer des autres prompts avant qu'ils soient effectivement fournis.

## 6. Exploration navigateur

Utilise Playwright ou un navigateur automatisé.

Explore en priorité :
- Smartphone compact.
- Smartphone standard.
- Grand smartphone.
- Ordinateur.

Inspecte les parcours suivants :

1. Arrivée sur la page d'accueil.
2. Compréhension de la proposition de valeur.
3. Recherche ou sélection d'une commune.
4. Consultation de la page d'une commune.
5. Découverte des coffrets.
6. Consultation du détail d'un coffret.
7. Compréhension des prestations incluses.
8. Consultation de la page d'un commerçant.
9. Navigation entre commerçant, commune et coffrets.
10. Consultation des animations.
11. Consultation du calendrier communal.
12. Accès au détail d'une animation.
13. Passage vers Localeo Live si proposé.
14. Sélection d'un coffret à acheter.
15. Consultation du récapitulatif de commande.
16. Passage vers Stripe, dans les limites de sécurité définies ci-dessous.

Examine également :
- Les menus.
- Les filtres.
- Les états vides.
- Les messages d'erreur.
- Les temps de chargement observables.
- Les retours arrière.
- La cohérence des liens.
- La lisibilité des prix et des conditions.
- L'affichage mobile.

## 7. Frontière de sécurité du parcours Stripe

Le parcours d'achat doit être analysé sans effectuer de paiement.

Tu peux :
- Parcourir les fiches coffrets.
- Sélectionner une offre.
- Examiner les étapes de commande.
- Vérifier les informations présentées avant paiement.
- Inspecter le code de création de session Stripe si accessible.

Tu ne dois pas :
- Effectuer un paiement.
- Saisir des coordonnées bancaires réelles.
- Confirmer une commande.
- Déclencher une facturation.
- Générer un achat réel.

Si la redirection vers Stripe crée une commande, une réservation ou une session de paiement ayant des effets métier, n'exécute pas cette action sans confirmation préalable de son innocuité.

Dans le cas contraire, arrête-toi juste avant la redirection et analyse le mécanisme par le code.

L'objectif est de vérifier la qualité du parcours jusqu'à Stripe, pas de tester le paiement.

## 8. Analyse complémentaire du code

Si le dépôt est accessible, examine :
- Les routes.
- La navigation.
- Les pages communes.
- Les fiches commerçants.
- Les fiches coffrets.
- Le calendrier.
- Les composants de commande.
- La préparation de la session Stripe.
- Les mécanismes de redirection.

Distingue l'implémentation du comportement réellement observé.

## 9. Livrables

Dans `observations/`, crée :
- `cartographie-parcours.md`
- `inventaire-ecrans.md`
- `observations-factuelles.md`
- `parcours-achat-stripe.md`
- `limitations.md`

Enregistre les captures dans `visuels/captures-avant/`.

Classe chaque constat :
- OBSERVÉ.
- DÉDUIT.
- HYPOTHÈSE.

## 10. Contraintes

Aucune modification applicative.

Aucun achat réel.

Aucune simulation d'utilisateurs à cette étape.

Aucune maquette.

Mets à jour le README, présente les résultats et attends mon autorisation avant l'étape 2.