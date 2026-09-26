# Moteur d’animation — recette et préparation du pilote

Ce document donne les critères de recette de l’EPIC et le relevé à compléter pour un pilote. Les règles restent celles de la [spécification](localeo_animation_engine_spec.md) et de la [conception technique](conception-technique.md). Le [compte rendu d’implémentation](suivi-implementation.md) porte les résultats des commandes, les limites et les commits.

## 1. Ce que prouvent les différents contrôles

| Contrôle | Preuve attendue | Limite |
| --- | --- | --- |
| Domaine et contrats | Trois moteurs, cinq activités, états, réponses fermées, seuils et dépendances. | N’établit pas le fonctionnement d’un appareil ni d’un environnement déployé. |
| PostgreSQL réel jetable | Transactions, concurrence, reçus, activation QR, attestations, retrait, correction, gel et conservation. | Les référentiels externes et les fournisseurs sont isolés ; aucun paiement ou envoi réel. |
| Recette transversale | Résultat préparé → accords → publication → inscription → jeu → attestation → retrait → régularisation → gel → tirage → conservation. | Part d’un résultat éditorial accepté ; génération et acquisition du lot sont couvertes séparément. |
| Navigateur à API simulée | Écrans à 390/1280 px, clavier, cinq activités, droits, perte de réponse, réconciliation et continuité. | Ne remplace pas les preuves HTTP/PostgreSQL ni un scan caméra réel. |
| Pilote humain | Parcours, durée, repérage des lieux, caméra, réseau, accessibilité et compréhension sur place. | **Non exécuté dans l’implémentation.** À renseigner sur la cible retenue. |

La recette transversale exécutable est [test_parcours_moteur_epic_postgres.py](../../../../localeo-backend/tests/security/test_parcours_moteur_epic_postgres.py). Les suites dédiées couvrent les variantes, erreurs, courses et frontières que ce parcours nominal ne peut toutes regrouper.

## 2. Critères techniques avant ouverture

- [ ] Les migrations additives sont appliquées par le lanceur officiel à la cible explicitement choisie ; leurs contrôles passent.
- [ ] La simulation de conversion est examinée ; aucun objet publié incompatible n’est présent. Les démonstrations sont identifiées explicitement. L’application de la simulation puis son rejeu ne déclenchent ni génération, ni publication, ni invitation, ni débit de quota.
- [ ] Les trois frontends embarquent les mêmes contrats générés que le backend ; leurs contrôles de contrats et builds passent.
- [ ] Le résultat de génération passe le parseur strict, les contrôles des médias WebP et les budgets de projection. Les secrets, bonnes réponses, lieux futurs et missions non choisies restent privés.
- [ ] Les mutations portent les versions et une clé stable. Après une réponse perdue, la lecture du reçu précède tout renvoi explicite ; le rejeu exact ne double aucun effet.
- [ ] Les permissions de publication, neutralisation, correction et clôture sont explicitement attribuées aux acteurs habilités. Les refus de scope et CSRF sont vérifiés.
- [ ] Les simulations de conservation sont terminées pour les catégories à traiter. Les tâches de purge, le curseur, les reprises et l’ordonnanceur sont vérifiés sur la cible retenue.
- [ ] La purge des réponses détaillées après échéance conserve les compteurs, reçus utiles, preuves, provenance du gel, population et gains.
- [ ] Les opérations en attente humaine restent distinctes des échecs techniques. Les opérateurs disposent du suivi, des identifiants de corrélation et des procédures de reprise.

Ces cases ne déclarent pas un déploiement effectué. Les succès locaux sont recensés dans le compte rendu ; chaque case d’ouverture doit être confirmée sur la cible retenue.

## 3. Fiche de préparation du pilote — à renseigner

| Élément | Valeur à consigner |
| --- | --- |
| Cible et version | Environnement, versions/commits backend et trois interfaces, opérateur. |
| Territoire | Commune et périmètre ; Latresne reste l’exemple documentaire, pas un pilote confirmé. |
| Période | Date/heure de début et fin, fuseau, échéance des réponses commerçantes. |
| Participants | Public, nombre prévu, capacité éventuelle ; référent organisateur et contact support. |
| Parcours | Thème, difficulté, durée cible, fourchette d’étapes, liste vérifiée des commerces/POI. |
| Conditions de participation | Règlement présenté et sa version, déclaration adulte, absence d’achat obligatoire. |
| Commerçants | Deux propositions lorsqu’elles existent, mission sélectionnée, exigences confirmées, disponibilité et support. |
| Préparation des lieux | Support QR associé à la bonne position, disponible puis actif à la publication ; deux blocs Terrain sans fiche de visite ni checklist imposée (E55-UX-11). Les horaires, trajet, accès et consignes peuvent être relus dans le guide facultatif. |
| Continuité | Source et consommateurs des objets/informations ; réponse prévue en cas de retrait global d’une étape. |
| Visuels | Thème déclaré, polices autorisées, médias de l’animation ; poids/résolution/texte alternatif. Aucun ajout décoratif spécifique dans le lecteur. |
| Appareils | Au moins un Android et un iPhone réels, navigateurs/versions, ordinateur et parcours clavier. |
| Exploitation | Acteurs habilités, traitement d’un commerce fermé, correction d’attestation, clôture et preuve de gel. |

## 4. Scénarios humains et résultats à consigner

| Scénario | Résultat attendu | Statut initial |
| --- | --- | --- |
| Inscription et reprise | Déclaration adulte/règlement explicites, lien personnel récupérable, capacité respectée. | Non exécuté sur cible réelle |
| Départ avant puis pendant la période | Défi masqué avant ouverture ; lieu courant uniquement ; départ activé au bon instant. | Non exécuté sur cible réelle |
| QR de lieu et QR personnel | Le QR de lieu ouvre le défi ; seul le scan commerçant habilité apporte l’attestation. | Caméra réelle non exécutée |
| Cinq activités | Information, choix unique, association, ordre, texte/code utilisables au toucher et au clavier. Erreur, indice, aide et succès compréhensibles. | Validation terrain non exécutée |
| Réseau interrompu | Commande bloquée/reçue clairement distinguée ; réconciliation et renvoi explicite sans double tentative. | Réseau mobile réel non exécuté |
| Commerce indisponible | Aperçu organisateur, motif et confirmation ; avis de parcours adapté, continuité disponible au bon moment. | Non exécuté sur cible réelle |
| Changement de période ou de capacité | Horaires Europe/Paris, champs autorisés et contrôles affectés relus ; versions vérifiées, réouverture explicitement confirmée si nécessaire, supports à rééditer. | Non exécuté sur cible réelle |
| Attestation erronée | Annulation autorisée, parcours conservé, qualification retirée ; nouvelle attestation reliée à la précédente. | Non exécuté sur cible réelle |
| Clôture et tirage | Population gelée depuis les faits ; replay sans second tirage ; anomalie ultérieure sans modification du gain. | Non exécuté sur cible réelle |
| Lisibilité et accessibilité | Contrastes, taille du texte, noms accessibles, focus visible, absence de débordement ; texte alternatif des images. | Recette humaine complète non exécutée |
| Parcours local | Durée mesurée, transitions compréhensibles, lieu suivant trouvable, accueil et missions réalisables. | Non exécuté sur le terrain |

Pour chaque exécution, relever date, acteur, appareil/version, animation/participation de test, résultat attendu/observé et référence d’incident. Ne pas joindre de token personnel, base64, bonne réponse ou donnée privée aux traces partagées.

## 5. Décision de passage

Le passage au pilote repose sur les contrôles techniques et la fiche logistique complétée. L’ouverture publique reste une opération distincte de l’implémentation et des commits. Un défaut empêchant une participation, révélant une réponse privée, doublant un effet ou altérant une preuve/qualification doit être corrigé puis revérifié avant ouverture. Les écarts de durée, compréhension ou présentation sont consignés avec leur décision et leur nouvelle vérification.

[Retour au dossier moteur](README.md).
