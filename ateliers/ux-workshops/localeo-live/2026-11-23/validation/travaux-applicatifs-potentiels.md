# Travaux applicatifs potentiels après la validation des maquettes

La préparation s’appuie sur la version `2026-11-23-maquettes-v1` et les constats du workshop. L’ordre proposé commencera par les écarts publics reproduits, puis les scénarios qui demandent des données autorisées. Une instruction de développement distincte sera nécessaire. [Décisions](decisions.md) · [Backlog du workshop](../workshop/backlog-ux.md)

## Répartition des décisions

| Catégorie | Orientations |
| --- | --- |
| VALIDÉES | B1, B3, C1, D1, D3, E1 |
| À RÉVISER | 0 |
| REPORTÉES | 0 |
| REFUSÉES | 0 |

A1 et F1 restent au backlog P2. Les options rejetées par le workshop sont conservées séparément. [Options rejetées dans la simulation](../workshop/orientations-rejetees.md)

## Orientations validées

| Lot de travail potentiel | Propriétaire et dépendance | Preuves avant une livraison |
| --- | --- | --- |
| D3 · Corriger la fiche Passeport indisponible | Examiner ensemble la lecture du programme et du détail. Marketplace porte la présentation du retour. Le backend est à examiner si le diagnostic établit un écart de publication ou d’éligibilité. | Une carte éligible ouvre le bon détail. Tester une fiche disparue entre deux lectures et une erreur temporaire. Vérifier retour, commune, filtres et focus utile. |
| B1 · Aligner les conditions d’inscription | Faire confirmer la règle et le règlement utilisés pour la tombola. Marketplace présente les faits et les champs du contrat. En cas de divergence de données ou de contrat, traiter la source correspondante. | Comparer fiche et formulaire pour une visite requise, une visite dispensée et une règle inconnue. Vérifier l’annonce des champs et le retour au détail. |
| D1 · Expliquer la fin prévue dans le programme | Marketplace réutilise les dates et le statut public. L’éligibilité et la clôture relèvent du domaine. Qualifier séparément toute incohérence de données. | Scénarios en cours, fin prévue dépassée avant clôture, futur rempli, futur vide et lecture partielle. Vérifier le raccourci, les modalités et le focus. |
| B3 · Vérifier le parcours QR et sa reprise | Préparer un QR valide, un code du jour et une boîte de test autorisée. Réutiliser les composants Live et la procédure d’ajout au carnet. La confirmation dépend du résultat d’inscription. | QR valide, invalide et expiré, code erroné, réception d’e-mail, confirmation, réouverture et reprise. Tester la réponse incertaine, l’idempotence du réessai existant et la récupération. |
| C1 · Vérifier les états et les consignes de retrait | Utiliser des lots de test autorisés. Le domaine porte les droits et transitions de remise. L’interface montre l’état vérifié ou le dernier état connu. | État à retirer, remis, expiré, annulé et lecture incertaine. Ouvrir puis fermer le bon et vérifier l’absence de remise avant la confirmation attendue. Couvrir le lieu et les consignes absents. |
| E1 · Vérifier les gestes essentiels avec aides d’accès | Recette transverse avec états réels de la fiche, du formulaire, du programme et des lots. Prioriser les obstacles reproduits. | Navigation clavier, focus visible, annonce d’erreur, lecteur d’écran, texte agrandi et clavier virtuel en relevant chaque action bloquée ou terminée. |

La 429 fait l’objet d’une vérification d’exploitation distincte sur un environnement autorisé. Vérifier à quel moment le programme devient partiel et dans quelles conditions une lecture reprend. Le message de maquette sert de référence pour l’état affiché. [Risques ouverts](revue-pour-decision.md#risques-à-conserver-pour-la-suite)

Les corrections d’interface concernent d’abord `localeo-marketplace`. Le diagnostic déterminera les impacts éventuels sur le backend, le contrat partagé, les données de démonstration et les parcours visibles des guides Commerçant ou Animation. Vérifier ces impacts au périmètre réel d’une future modification. [Principes Live](../../../../../docs/produit/live/principes-ux.md) · [Spécification existante](../../../../../docs/specifications/epic-73-animation-et-ou-coffrets/workshop-live-20261118.md)
