# E75 — Mots croisés assistés par l’IA

Spécification du **4 novembre 2026**. État produit : **À faire**, selon la
[roadmap commune](../../roadmap/README.md). Les 8 US et 18 critères
`E75-CA-01` à `E75-CA-18` du
[backlog canonique](../../roadmap/a-faire/epic-75-mots-croises-assistes-ia-backlog.md)
sont conservés. Ce dossier décrit une cible ; il ne constate aucune implémentation,
recette ni activation du modèle.

## Résultat attendu

L’organisateur demande une animation de mots croisés. Localeo prépare une grille
avec l’aide de l’IA, la contrôle et la soumet à l’organisateur. Après validation
de la version et des préparatifs, l’organisateur publie. L’habitant rejoint le jeu
dans Live, retrouve les indices chez les commerçants, remplit sa grille et fait
valider ses passages. **Grille entièrement correcte ET tous les passages requis
validés par les commerçants** sont nécessaires pour accéder au tirage.

L’IA n’évalue jamais les réponses des joueurs. Aucun achat chez un commerçant
n’est exigé par ce jeu. Les règles d’attestation d’achat de la tombola commerçante
E53 et l’inscription sans passage de la tombola publique E74 restent distinctes.

## Lire la spécification

| Document | Contenu |
| --- | --- |
| [Parcours et règles](parcours-regles.md) | Préparation guidée, jeu mobile, refus et règles validées |
| [Architecture et contrats](architecture-contrats.md) | Existant vérifié, domaine, transactions, DTO, compatibilité et données |
| [Vérification et livraison](verification-livraison.md) | Matrice des 18 critères, bornes et budgets, migrations, exploitation et preuves à produire |

Socles réutilisés : [E55](../moteur-animation/README.md),
[E73](../epic-73-animation-et-ou-coffrets/README.md),
[Live E42](../epic-42-localeo-live/README.md),
[PIN E70](../epic-70-validation-pin/README.md),
[salariés E72](../epic-72-acces-salaries/README.md).

## Décisions et préparation de l’implémentation

Les décisions **E75-DEC-01 à 07** restent acquises : nouveau jeu payant, assistance
IA, indices chez les commerçants, préparation par Localeo puis validation de
l’organisateur, réussite complète et attestations obligatoires. Aucune option
ne permet de désactiver ces attestations.

Les réponses du porteur produit du **4 novembre 2026**, dont « Je valide les trois
recommandations », arrêtent les choix suivants. Le tableau conserve les neuf
identifiants d’arbitrage du backlog ; ils sont désormais résolus pour la V1.

| Arbitrage | Décision V1 | Partie concernée |
| --- | --- | --- |
| E75-ARB-01, résolu | Fiches imprimables par commerce, plusieurs définitions possibles ; tous les commerces retenus sont requis. Une attestation par commerce, indépendamment du nombre de mots. Pas de diffusion générale des définitions dans le catalogue public | Affectation des indices, supports, ensemble des passages requis |
| E75-ARB-02, résolu | Circuit manuel assisté : prompt exporté, import JSON contrôlé, revue humaine ; pas de fournisseur IA intégré en V1. Préparation sous 5 jours ouvrés comme la chasse, avec suspension pendant l’attente d’un complément | Préparation, calendrier de service, coûts et offre |
| E75-ARB-03, résolu | Grille entièrement correcte et passages requis attestés | Aucun arbitrage sur cette règle ; dépend des modalités ARB-01/09 |
| E75-ARB-04, résolu | Français, une grille commune, 15 × 15 cases maximum, 5 à 25 mots, grille connectée ; thème/public/difficulté et mots souhaités dans le brief | Géométrie, bornes produit, supports et difficulté |
| E75-ARB-05, résolu | Accents, espaces et traits d’union ignorés ; contrôle global à la demande, sans dévoiler les lettres correctes. Une fois correcte, grille validée et non modifiable | Normalisation et feedback ; détails dans les parcours |
| E75-ARB-06, résolu | Essais sans quota métier mais limités techniquement ; pas d’aide révélant une réponse, pas de corrigé public en V1, même après clôture ; aucun bonus de vitesse | Aides, feedback, révélation |
| E75-ARB-07, résolu | Version publiée immuable ; retrait temporaire pour diagnostic, reprise identique ou annulation motivée puis nouvelle édition corrigée, sans transfert automatique des chances. Localeo peut offrir explicitement un crédit de remplacement | Support après publication ; aucun remboursement ou crédit automatique |
| E75-ARB-08, résolu | « Comme sur la chasse au trésor » : module payé par l’organisateur, public gratuit, 190 € HT pour 12 mois, 5 publications et quota indépendant ; mêmes mécanismes E73 de prorata, essai/cadeau et conditions acquises | Achat, droits et conditions commerciales |
| E75-ARB-09, résolu | Même parcours d’identité que la chasse, règlement et déclaration d’un adulte, accès personnel Live ; une chance par participant qualifié ; coffrets, lots libres externes et bons numériques | Inscription, déduplication, tirage et remise |

Ces confirmations constituent **E75-DEC-08 à 13**, consignées dans le backlog.
Les seuils techniques, noms de commandes et structures détaillées sont des choix
de conception de ce dossier. Aucun autre arbitrage produit n’est ouvert pour
cette V1. La disponibilité dépend encore de l’implémentation, des preuves des
18 critères et de la livraison coordonnée décrites ci-après.

## Périmètre et limites

Backend/ERP : règles, préparation, import, droits, publication, qualification,
supports, bilans, tirage et notifications existants. Animation : assistant et
validation organisateur. Marketplace : code de **Live**, sur son domaine dédié ;
aucune réouverture de `surface=animations`. Pro : validation des passages et
droits salariés. OnBoard conserve la préparation du commerce Animation, sans
introduire un contrat Coffrets, Stripe ou un rendez-vous obligatoire.

Pas de nouveau moteur de tirage, compte habitant obligatoire, canal de campagne,
application native, classement de vitesse, achat de billet, ni conversion de
chasse. Les fonctionnalités Coffrets ne changent pas.

Les tests métier listés sont **à produire**, pas exécutés dans cette phase.
Les contrôles documentaires et la revue de contrats sont consignés dans le
[document de vérification](verification-livraison.md).
