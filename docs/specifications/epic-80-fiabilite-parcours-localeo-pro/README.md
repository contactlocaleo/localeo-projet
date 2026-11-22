# EPIC 80 — Fiabilité des parcours Animation dans Localeo Pro

## Statut et décisions

Spécification du 18 novembre 2026 liée au [backlog E80](../../roadmap/en-cours/epic-80-fiabilite-parcours-localeo-pro-backlog.md) et au [workshop Pro](../../../ateliers/ux-workshops/localeo-pro/2026-11-18/README.md). L'utilisateur a validé les cinq orientations B1/C1/D1/E1/F1 pour l'implémentation le même jour ; le [registre des décisions UX](../../../ateliers/ux-workshops/localeo-pro/2026-11-18/validation/decisions.md) distingue cette réponse des votes fictifs du workshop. Les règles métier et preuves restent celles des critères de l'epic.

L'état produit relève uniquement de la [roadmap](../../roadmap/README.md). B1/C1/D1/E1/F1 sont le périmètre P1 ; A1/G1 P2 et les alternatives rejetées ne sont pas intégrées.

## Existant vérifié et cible

| Orientation | Existant lu dans les producteurs/consommateurs | Cible et refus significatif |
| --- | --- | --- |
| B1 | `ActionWorkspaces.jsx` distingue reconnaissance, confirmation, commande et reçu. Une valeur non reconnue remonte un texte « pack » du validateur Coffret. | Message de scanner commun orientant vers le QR participant Live en contexte Animation ; aucune commande après rejet local. Confirmation, verrou, idempotence et relecture du reçu préservés ; silence réseau jamais traduit en succès. |
| C1 | `NotificationsPage.jsx` affiche PIN avant Animation. `AnimationNotificationsPage.jsx` sait marquer lu, supprimer et suivre un lien ; la notification normalisée n'expose pas un état de tâche fiable. Accueil Pro lit séparément les demandes/états de préparation. | Animation avant PIN vide ; section « Actions attendues » dérivée des demandes et autorisations actuelles, indépendante des messages lus. Aucun état de tâche déduit du texte ou du non-lu. |
| D1 | Accueil charge toutes les animations, liste charge une page ; tous deux utilisent `animationCategory`, qui tient compte de la fin effective même si le statut reste EN_COURS. L'écart TEST 2/3 a une cause non établie. | Accueil et liste utilisent le même chargement complet et le même classement, puis la liste pagine localement chaque catégorie. Le domaine backend reste propriétaire de la période et des transitions ; l'UI ne crée aucun statut ni échéance. |
| E1 | L'API kit renvoie `modeOperatoire`, `supports`, version et indicateur QR de lieu. Le téléchargement peut préparer le QR de lieu avant l'archive ; la déclaration « Je suis prêt » est séparée. Le producteur du texte du guide concatène actuellement les horodatages ISO de la configuration. | Rendre les bornes locales et exactes en heure de Paris dans le guide JSON et l'archive HTML ; présenter les consignes immédiatement près du téléchargement et distinguer les rôles des QR. Ne pas inférer qu'un téléchargement atteste installation ou prêt. |
| F1 | Session et caches sont séparés par compte ; validation Animation relit le reçu après une réponse incertaine ; pages et accueil actualisent au retour visible. | Après expiration, garder le chemin de la page protégée sans paramètres ni saisie, puis recontrôler la session et les droits après connexion. Aucun rejeu de mutation. Le résultat de transaction reste porté par B1. Une absence de plusieurs semaines reste à éprouver en recette. |

## Invariants et propriétaires

1. **Passage Animation :** une reconnaissance de QR ne valide rien ; une commande confirmée a un effet unique, et un reçu relu ne déclenche aucune mutation. Les entités et services de `app/domaine/animation_locale`, puis `ServiceValidationsAnimation`, portent la règle ; les routes API et Pro exposent le résultat. Succès, doublon, refus et incertitude doivent garder des sorties différentes (`E80-CA-01..04`).
2. **Participation et préparation :** invitation acceptée, approbation organisatrice, installation, déclaration prêt et contrôle restent distincts. Les domaines Animation/E78 décident des transitions ; Pro ne calcule que la présentation d'une action explicitement autorisée (`E80-CA-05..09`). Lire ou supprimer une notification ne change pas ces états.
3. **Kit :** seul le commerce de la demande acceptée et courante accède aux supports autorisés. Le domaine vérifie cet accès et la diffusion du flyer ; le service applicatif assemble les consignes et le rendu. Le téléchargement ne confirme pas prêt (`E80-CA-10..11`).
4. **Session :** après changement de compte ou expiration, aucun état privé d'un autre compte, QR ou jeton ne survit dans la navigation. L'API contrôle droits et périmètre ; Pro invalide ses caches et présente la reprise (`E80-CA-12`).

## Contrats, données et compatibilité

Producteur des lectures et commandes Animation : `localeo-backend`. Contrats canoniques et schémas OpenAPI restent dans `localeo-projet` ; l'OpenAPI embarqué consommé par Pro est `localeo-commercant/api/localeo-openapi.json`. Aucun champ, endpoint ou erreur n'est ajouté pour les corrections de texte, ordre et dates du présent lot ; aucun export de contrat n'est donc requis. Si le diagnostic de C1/D1/F1 établit un manque de projection, le producteur et tous ses consommateurs devront être spécifiés et testés ensemble avant extension. La liste paginée ne doit jamais être assimilée au total global sans un total fiable.

Les instants stockés, bornes métier et migrations restent inchangés. Le guide traite une date civile comme un jour sans heure, un timestamp naïf selon la convention UTC existante et un instant avec offset selon son instant réel ; l'affichage utilise `Europe/Paris`. Aucune nouvelle donnée personnelle ni télémétrie n'est introduite. Le générateur de démonstration n'a pas de schéma à adapter pour ce lot ; des fixtures synthétiques doivent couvrir les dates, le rejet QR et PIN vide. Les cas de reçu, préparation et retour différé réutilisent d'abord les jeux existants.

## Ordre de réalisation et preuves

| Lot / critères | Travail autorisé maintenant | Preuve prévue et état initial | Impacts fonctionnels et exploitation |
| --- | --- | --- | --- |
| L1 · CA-01, 04 | Rejet QR local et aide de reprise, annonce accessible ; préserver le scanner Coffret. | Parcours synthétique rejet local, aucune mutation ; recette sur téléphone physique encore requise pour CA-04. | Guide de scan Pro à réviser si le texte est repris ; aucun contrat ni migration. |
| L2 · CA-06 | Animation avant PIN vide, PIN accessible et fonctions conservées. | Test UI de l'état PIN vide et navigation Animation ; clavier/mobile à vérifier. | Aide notifications Pro à réviser ; aucune API modifiée. |
| L3 · CA-11 | Conversion du guide kit côté producteur, JSON et HTML généré. | Test applicatif hiver/été, changement de jour, date civile/invalide et archive ; impression réelle à vérifier séparément. | Consignes kit communes actualisées ; aucun changement de borne ni migration. |
| L4 · CA-02, 03, 05, 07..10, 12 | Diagnostiquer capacités existantes et écarts ; compléter seulement les manques établis. | Tests de commande/reçu, lecture de tâche, compteurs même périmètre, kit réel, expiration et retour. Une partie exige appareil ou environnement de recette autorisé. | Contrats, générateur, procédure et éventuelle migration à réévaluer après diagnostic, avant code dépendant. |
| L5 · CA-13 | Recette avec commerçants variés et aides techniques avant extension. | Non exécutée ; relever réussite, erreurs, aide et durée sans promettre de gain. | Condition d'ouverture à 500 commerces ; aucun déploiement implicite. |

La boîte de notifications lit désormais les demandes de participation pour afficher les actions attendues ; cette lecture réutilise la requête et son cache par session de l'accueil. La liste des animations charge toutes les pages pour aligner ses catégories sur l'accueil, selon la borne existante de `collectPages` (500 pages, détection d'incohérence). Avant extension à 500 commerces, mesurer ces lectures sur le volume cible selon la [convention de volumétrie](../../architecture/transverse/performance-volumetrie.md). Aucun index ou schéma n'est modifié.

## Points ouverts

- Le 2/3 observé en TEST n'est pas reproduit sur le même jeu local ; source, page, commune et instant sont à rapprocher avant de conclure à un défaut backend ou frontend.
- Le contenu binaire et l'impression du kit TEST n'ont pas été éprouvés ; la recette devra vérifier nom, QR et pages effectives.
- Caméra physique, mauvaise connexion réelle, expiration et retour après plusieurs semaines, lecteurs d'écran et compréhension commerçants restent non exécutés.
