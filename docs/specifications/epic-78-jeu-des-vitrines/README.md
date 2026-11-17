# E78 — Le jeu des vitrines

Spécification préparée le **15 novembre 2026** à partir du
[cadrage du 6 novembre](../../roadmap/en-cours/epic-78-jeu-des-vitrines-backlog.md).
État produit : **En cours**, selon la [roadmap commune](../../roadmap/README.md).
Les six user stories et les seize critères `E78-CA-01` à `E78-CA-16` restent
les références d'acceptation. L’implémentation locale des 16 et 17 novembre est suivie
dans le [bilan de réalisation](bilan-realisation.md) : parcours et démonstration
vérifiés, qualification de charge soutenue ouverte ; modèle encore inactif.
Les observations de spécification du 15 novembre sont conservées comme historique.

## Résultat recherché

Les habitants découvrent les commerces participants, observent leurs vitrines
réelles et identifient un intrus. Noël et Pâques sont des thèmes privilégiés,
sans limiter le jeu à ces fêtes. Live présente une consigne courte, les lieux
à découvrir, les réponses enregistrées et la progression confirmée par le serveur.
Le parcours ne reprend pas implicitement l'ordre linéaire ni les aides de la chasse.

L'objet existe dans une vitrine préparée. Une proposition de contenu, un accord
de participation commerçante et un contrôle de mise en place sont trois faits
différents. Une photo ou un QR ne les remplace pas automatiquement.

## Documents canoniques

| Document | Usage |
| --- | --- |
| [Parcours et règles](parcours-regles.md) | Préparer, approuver, publier, découvrir, répondre, qualifier et traiter les incidents |
| [Architecture et contrats](architecture-contrats.md) | Existant vérifié, domaine propriétaire, projections, transactions, persistance et compatibilité |
| [Vérification et livraison](verification-livraison.md) | Matrice des seize critères, scénarios de recette, capacité, démonstration et lots de réalisation |
| [Backlog](../../roadmap/en-cours/epic-78-jeu-des-vitrines-backlog.md) | Besoin, critères stables, décisions produit et arbitrages |

## Décisions acquises

`E78-DEC-01/02` confirment le jeu de recherche d'intrus dans de vraies vitrines
et son usage multithème. Les réponses utilisateur du **15 novembre 2026**
résolvent les sept arbitrages du cadrage ; leur trace est dans le backlog.

| Arbitrage résolu | Décision du 15 novembre | Partie concernée |
| --- | --- | --- |
| E78-ARB-01 | Un intrus par commerce, QCM, une seule réponse après confirmation explicite | Modèle de réponse, consommation d'essai, correction et formulaire Live |
| E78-ARB-02 | Mêmes conditions que le Juste Prix local : seuil de commerces réussis fixé par l'organisateur, une chance au tirage existant | Qualification, conditions publiques et population du tirage |
| E78-ARB-03 | Préparation dans Pro puis approbation et contrôle terrain par l'organisateur | Habilitations de préparation, transitions et kit |
| E78-ARB-04 | Comme le Juste Prix local : choix explicite avec ou sans passages requis ; si requis, bonne réponse et passage du même commerce, dans n'importe quel ordre pendant le jeu | Commandes Pro/PIN, droits salariés et condition de qualification |
| E78-ARB-05 | Réussite/échec immédiat, solution après clôture métier confirmée | Projections, reçus, révélation et wording Live |
| E78-ARB-06 | Suspension de l'édition ; reprise identique si le dispositif est rétabli, sinon annulation puis nouvelle édition | Reprise, retrait éventuel et équité des réponses/qualifications |
| E78-ARB-07 | Inclusion au forfait standard organisateur avec les dotations existantes, sans tarif ou quota propre à E78 | Droits commerciaux et activation du modèle |

La demande « même condition que pour le just prix local » reprend explicitement
le seuil, le choix de passages et la chance unique de la
[règle E77](../epic-77-juste-prix-local/parcours-regles.md#réussite-passages-et-qualification--ca-09-à-13).
Elle ne transfère pas le prix, la tolérance ou les modalités de réponse d'E77.

## Portée et préparation de l'implémentation

Les cinq dépôts sont concernés par une réalisation future : sources canoniques
ici, règles/API/ERP et outils dans le backend, préparation et suivi dans Animation,
préparation commerçante et passages dans Pro, expérience habitant dans Live au
sein de Marketplace. Coffrets conserve ses parcours ; l'accès au jeu pointe vers Live.

Les décisions produit sont résolues. La spécification couvre les parcours,
invariants, contrats, permissions, migrations, preuves et dépendances des lots.
Le périmètre a été déclaré prêt à implémenter le 15 novembre. L’implémentation
locale et sa validation ont commencé le 16 novembre ; l’état produit est
**En cours**, avec résultats et réserves dans le [bilan](bilan-realisation.md).
L'inclusion dans l'offre standard ne rend pas le moteur disponible
avant la livraison coordonnée de ses producteurs et consommateurs.

Références : [moteur E55](../moteur-animation/README.md),
[participation E56](../epic-56-validation-participation-commercants-animation/README.md),
[Live E42](../epic-42-localeo-live/README.md),
[offre E73](../epic-73-animation-et-ou-coffrets/README.md),
[Juste Prix E77](../epic-77-juste-prix-local/README.md),
[PIN E70](../epic-70-validation-pin/README.md),
[salariés E72](../epic-72-acces-salaries/README.md).

Aucune génération IA de réponse, reconnaissance de photo, obligation d'achat,
classement ou preuve GPS n'est ajoutée à ce périmètre. Les prochains contrôles
métier, navigateur et PostgreSQL sont distingués entre prévus, exécutés et
limités dans le [bilan de réalisation](bilan-realisation.md).
