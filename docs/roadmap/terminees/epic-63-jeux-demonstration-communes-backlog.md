# Epic 63 — Contextualiser un environnement par un jeu de données vivant

- Statut : outillage recentré ; recette connectée à effectuer avant la première séance.
- Cadrage corrigé le 12 septembre 2026 à la demande explicite de l'utilisateur.
- [Spécification](../../specifications/epic-63-demonstrations-communes/README.md).
- [Guide opérateur](../../exploitation/demonstration/exploitation.md).

## Principe directeur absolu

**La génération du jeu de données ne doit jamais impacter le code applicatif.**
Les données s'adaptent au schéma, aux contrats et aux règles existants.
Aucun changement de frontend, middleware, endpoint, marquage PDF, filtre
fournisseur, mode de démonstration ou migration de contrôle n'est requis.

Les modèles et services existants peuvent être réutilisés avec leurs interfaces
normales. Aucun monkeypatch ou changement de variable globale n'est livré.
Le journal, les sauvegardes et les accès du conducteur sont des fichiers privés
de l'outillage autonome, jamais des dépendances des applications.

Cette instruction remplace les exigences de la conception antérieure prévoyant
des adaptations applicatives. Les éventuels défauts du produit découverts
pendant la préparation sont traités séparément, notamment l'Epic 62.

## Objectif

Présenter une plateforme vivante pour une commune réelle, avec des commerces et
personnes fictifs crédibles, un historique cohérent et des parcours utilisables.
Les noms « test 1 », « commerçant 1 » et équivalents sont exclus.

Le script sauvegarde la base de test, construit le jeu dans une base jetable,
l'injecte temporairement et restaure ensuite la recette originale. BUM, TVA,
offres et autres références sélectionnées sont conservées logiquement ; elles
font également partie de la sauvegarde complète.

## Décisions produit conservées

| Sujet | Décision |
| --- | --- |
| Environnement | Remplacement temporaire de la base de test partagée. |
| Commune | Nom fourni pour chaque démonstration ; précision en cas d'homonymie. |
| Voisinage | Trois communes réelles voisines, également peuplées. |
| Identités | Commerces et personnes fictifs, descriptions réalistes. |
| Catalogue principal | Dix commerçants, quinze coffrets de deux à trois prestations. |
| Voisines | Deux commerçants, un coffret et une actualité par commune. |
| Animation | Dix animations dans des états variés, dont deux clôturées. |
| Historique | Trois mois, trente clients, soixante achats et cent inscriptions. |
| Marketplace | Coffrets, commerces et actualités de la commune consultables. |
| Parcours vivant | Création d'une animation supplémentaire pendant la séance. |
| Modèle | Passeport commerçant, cycle complet jusqu'au tirage et aux gains. |
| Fournisseurs | Stripe test, Brevo et Scaleway connectés ; aucun simulateur. |
| Destinations | Contacts et appareils internes ; adresses internes dans les données. |
| Évolution | Actions des présentateurs uniquement ; aucune activité périodique fictive. |
| Pilotage | Script hors ERP, configuration privée et conducteur par séance. |
| Restauration | Retour manuel, archive vérifiée conservée au moins trente jours. |

Objectifs : génération inférieure à dix minutes hors sauvegarde/fournisseurs,
et cycle Passeport présenté en trente minutes, à mesurer sur la cible.

## Cinq parcours

1. Animation en cours : partenaires, participants et progressions.
2. Animation clôturée : gagnants, lots envoyés ou à envoyer, consommation
   absente, partielle ou complète.
3. Marketplace communale : coffrets, commerces, actualités et Checkout Stripe test.
4. Commerçant et Support : accès, lecture des prestations, validation par QR
   ordinaire, consultation de l'instance et de ses objets connexes.
5. Nouveau Passeport : créer, configurer, accepter les participations commerçantes,
   financer les lots, publier, inscrire, valider, clôturer, tirer et attribuer.
   Cette animation est absente du jeu initial.

## Stories recentrées

| Story | Objet et critères |
| --- | --- |
| E63-01 | Registre exhaustif du schéma existant, références mixtes et documents ; table inconnue bloquante. Aucune migration ajoutée. |
| E63-02 | Cible non productive, services arrêtés, contrôle des connexions, verrou et journal hors base. |
| E63-03 | Commune et voisines résolues, paramètres bornés, textes/médias éditables, plan avec empreinte et prévisualisation. |
| E63-04 | Commerçants, onboarding, modèles versionnés, copies et coffrets ; BUM et budgets contrôlés par les règles existantes. |
| E63-05 | Achats, instances, droits, validations, finance et documents cohérents ; historique sans faux identifiant Stripe, contreparties test réelles si préparées. |
| E63-06 | Animations, participations, progressions, gagnants et consommations ; abonnements, accès et capacité pour une nouvelle animation. |
| E63-07 | Dump complet restauré en essai, fichiers contrôlés, import atomique et restauration exacte des lignes et séquences. |
| E63-08 | CLI, simulations, confirmations, journal, statut, reprise prouvée, reset avec nouveaux identifiants et rétention. |
| E63-09 | Conducteur privé, liens, comptes et QR au format ordinaire ; aucune adaptation des applications. |
| E63-10 | Acteurs, offre et quotas disponibles pour le cycle Passeport en direct, sans intervention SQL pendant la séance. |
| E63-11 | Cohérence historique et relationnelle, lectures métier et actions possibles ; aucune génération d'activité en arrière-plan. |

## Exploitation et validation

Le profil privé précise les cibles, références, contacts, clés ordinaires du
processus CLI et emplacements documentaires. Tous les opérateurs de la cible
partagent son répertoire de journal. Le script n'administre ni les services
ni les navigateurs ; les présentateurs utilisent une session propre après
chaque remplacement.

Terminer les opérations fournisseur et contrôler les webhooks avant l'installation
et avant la restauration. Une restauration SQL n'annule pas les effets externes.
Aucune quarantaine ni aucun rejeu spécifique n'est ajouté au backend.

Chaque reconstruction renouvelle identifiants et accès en conservant les
scénarios. La restauration retrouve exactement les données et séquences
originales, sans neutraliser implicitement les sessions ou files d'envoi.

Les tests utilisent PostgreSQL et les migrations existantes. Ils vérifient
transferts, fichiers, rollback et absence de modification des fichiers
applicatifs pendant la génération. Le [bilan](../../specifications/epic-63-demonstrations-communes/livraison-recette.md)
sépare les preuves locales des cinq parcours connectés restant à jouer.
Aucune base partagée n'est remplacée par la seule livraison du code.
