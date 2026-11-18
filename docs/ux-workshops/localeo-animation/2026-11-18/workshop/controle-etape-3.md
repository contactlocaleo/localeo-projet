# Contrôle de l’étape 3

18 novembre 2026, consolidation à 12 h 22 (Europe/Paris). Horodatage exact de l’archive dans [le manifeste final](manifest-etape-3-sha256.json).

## Périmètre et statut

**Étape 3 terminée ; validation utilisateur attendue.** Neuf orientations retenues : A1, B1, B2, B3, C1, C2, D1, D2, E1. Toutes correspondent aux votes initiaux à au moins 7/12 et aux priorités P0/P1 : une P0, huit P1. Aucune proposition supplémentaire ni implémentation applicative.

Le [prompt 03](../prompts/03-maquettes.md) contient l’instruction reçue. Le backlog et le README réfèrent aux livrables. Les votes simulés ne sont pas des décisions de validation.

## Contrôles exécutés

| Contrôle | Résultat et portée |
| --- | --- |
| Correspondance votes / maquettes | 9 identifiants identiques au sous-ensemble adopté P0/P1 ; aucune orientation hors périmètre. |
| Scénarios et rendus | 30 états, 60 rendus finaux : 1440 × 1000 et 390 × 844. Aucune largeur de document supérieure au viewport sur ces 60 mesures. |
| Intégrité des PNG | 187 PNG décodables : 63 captures originales, 60 rendus v1 conservés, 60 rendus v2 et 4 captures de contrôle de galerie. |
| Galerie | 9 comparaisons, deux colonnes sur bureau, bascule avant/après sur mobile, activation au clavier, retour aux deux colonnes, filtres P0 et P1/onboarding vérifiés. Les 18 images finales de la galerie se chargent. |
| C2 mobile | Deux cases de sélection entièrement dans la largeur de 390 px ; comparaison empilée, largeur interne et visible de 318 px. |
| B1 mobile | Bouton Enregistrer placé avant les champs facultatifs, entre y=643 et y=688 dans une fenêtre haute de 844 px ; transition locale vers la confirmation vérifiée. |
| E1 | Commande grise et désactivée avant attestation, activée après coche, désactivée après décoche. Retour sans clôture vérifié. La confirmation ouvre une fin de scénario et ne déclenche ni tirage ni remise, même simulés. |
| Réseau et erreurs | Aucune requête HTTP(S) externe et aucune erreur JavaScript relevées pendant les contrôles locaux. Aucune connexion à l’application TEST pendant cette étape. |
| Revue contradictoire | 108 fiches initiales uniques, 12 profils × 9 orientations, 648 réponses aux six questions. Relecture ciblée v2 par les mêmes douze rôles. Avis et préférences explicitement fictifs. |
| Liens | 769 références locales Markdown/HTML/CSS examinées avant finalisation de cette note ; aucun fichier cible manquant. Contrôle des chemins, pas une garantie de rendu Markdown dans tous les lecteurs. |
| Archives | Archive ZIP v1 lisible sans erreur ; PNG de revue conservés et liens ajustés vers v1. Aucun avis initial réécrit pour lui faire approuver la version finale. |
| Préservation de l’étape 2 | Sur les 95 fichiers du manifeste précédent, seules les trois évolutions prévues sont présentes : README, prompt 03, backlog. Les 63 captures et les observations sont inchangées. |
| Préservation de Localeo Pro | 107 empreintes du manifeste précédent vérifiées, toutes identiques. Aucune écriture dans les autres exécutions. |
| Périmètre Git | Les quatre dépôts applicatifs Animation, backend, commerçant et marketplace sont propres. Dans le dépôt documentaire, seul le répertoire non suivi `docs/ux-workshops/` apparaît. Aucun commit, push ou déploiement. |
| Confidentialité | Aucun marqueur de compte Gmail, jeton Bearer ou champ de jeton d’authentification trouvé dans les fichiers texte du dossier. Les captures réelles restent les versions expurgées d’étape 1 ; aucune nouvelle connexion ni donnée d’authentification utilisée. |
| Documentation | `py -3 scripts/check_guidance.py` : 107 guides, 1543 liens locaux, 0 erreur, 0 avertissement. `py -3 scripts/sync_documentation.py --check-sources` : 151 documents vérifiés. |

Preuves : [interactions locales](controle-interactions-maquettes.json), [mesures des 60 rendus](../visuels/maquettes-apres/mesures-rendus.json), [correspondances des images](../visuels/preuves-comparatif.json), [revue complète](revue-maquettes.md), [arbitrages](arbitrages-maquettes.md).

Le premier relevé de galerie comptait six images non encore chargées à cause du chargement différé. Le contrôle après chargement retrouve les 18 images valides. Une tentative de décodage lors du changement de source responsive a également été répétée après stabilisation, avec succès. Ces événements d’instrumentation ne sont pas présentés comme des défauts de l’application.

## Limites maintenues

- **B3 : preuve visuelle partielle.** Le seuil est hors cadrage de la capture AVANT disponible. AN-05 et le relevé DOM documentent le problème ; aucune capture reconstruite n’est proposée comme réelle.
- **D1 : panne non réparée.** Les états proposés ne prouvent ni la disponibilité du service, ni l’envoi, la distribution ou la lecture d’un message.
- **B1 et C1 : contrats à confirmer.** Brouillon partiel, circuit de référencement, propriétaire et droits nécessitent un cadrage avant développement. C2 exige encore une vérification des faux positifs et des règles de rapprochement.
- **Tests humains non exécutés.** Pas de validation sur téléphone physique, clavier virtuel ou lecteur d’écran ; aucune conformité d’accessibilité complète revendiquée. Aucun gain de temps mesuré.
- **Revue simulée.** Les corrections de représentation restent dans les orientations adoptées ; aucun nouveau vote nécessaire selon la revue. Cela ne vaut aucune décision de l’utilisateur.

Les maquettes et leurs boutons sont des présentations locales isolées. Aucune action applicative, invitation, notification, publication, clôture, remise ou suppression n’a été exécutée à cette étape. Les dossiers `validation/` et `synthese/` restent réservés aux étapes suivantes.
