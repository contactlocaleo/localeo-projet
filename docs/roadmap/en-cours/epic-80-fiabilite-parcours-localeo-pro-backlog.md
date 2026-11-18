# EPIC 80 — Fiabilité des parcours Animation dans Localeo Pro

## Références

- **État produit : En cours.** Cadrage, spécification et réalisation partielle du 18 novembre 2026, demandés après l'audit du [workshop Localeo Pro](../../ux-workshops/localeo-pro/2026-11-18/README.md). L'identifiant 80 a été recherché dans la roadmap, ses namespaces et les quatre dépôts applicatifs sans occurrence.
- Les [constats de l'exploration](../../ux-workshops/localeo-pro/2026-11-18/observations/observations-factuelles.md), le [rapport](../../ux-workshops/localeo-pro/2026-11-18/workshop/rapport-executif.md), les [votes simulés](../../ux-workshops/localeo-pro/2026-11-18/workshop/votes-et-arbitrages.md), les [maquettes](../../ux-workshops/localeo-pro/2026-11-18/visuels/comparatif-avant-apres.html) et le [backlog potentiel](../../ux-workshops/localeo-pro/2026-11-18/validation/backlog-implementation-potentiel.md) fondent le périmètre.
- **Portée de l'arbitrage :** cinq orientations P1, B1/C1/D1/E1/F1, ont été adoptées par douze rôles fictifs puis **validées par l'utilisateur pour l'implémentation E80** le 18 novembre 2026, sans condition supplémentaire. Le [registre utilisateur](../../ux-workshops/localeo-pro/2026-11-18/validation/decisions.md) distingue les deux événements. Cette décision ne constitue pas une preuve de fonctionnement.
- Socles proches : [E56, validation des participations](../../specifications/epic-56-validation-participation-commercants-animation/README.md), [E72, accès salariés terminé](../terminees/epic-72-acces-salaries-validation-localeo-pro-backlog.md), [E73, Animation terminé](../terminees/epic-73-animation-et-ou-coffrets-backlog.md) et [E78, préparation Vitrines en cours](../en-cours/epic-78-jeu-des-vitrines-backlog.md). Cette epic traite la continuité du parcours Pro entre modèles ; elle ne rouvre pas ces epics ni leurs règles métier.

## Problème et résultat attendu

Sur le compte TEST observé, un QR invalide dans le parcours Animation produit un message parlant de « pack » ; l'accueil annonce deux animations en cours quand la liste en affiche trois, dont une période passée ; le guide montre des dates ISO UTC. Le contenu du kit, les résultats d'une validation réelle et les reprises après interruption n'ont pas été vérifiés. La boîte présente une section PIN vide avant les notifications Animation. Ces faits sont datés et propres au compte exploré ; la cause de l'écart des compteurs et l'ampleur des difficultés en boutique demeurent inconnues.

Le commerçant doit pouvoir reconnaître le bon QR et le résultat certain ou incertain d'un passage, retrouver une action réellement ouverte, comprendre la prochaine étape de préparation et utiliser les supports sans confondre téléchargement, installation et déclaration prêt. Après interruption, il retrouve un contexte et des droits relus, sans nouvelle validation implicite. L'amélioration de la vitesse ou de la compréhension reste une hypothèse à mesurer auprès de commerçants.

## Périmètre

- **B1, P1 — scan et résultat :** corriger le message hors contexte constaté ; éprouver sur téléphone confirmation, doublon, refus, reçu et perte de réponse avant de modifier les garanties existantes.
- **C1, P1 — messages et actions :** rendre les messages Animation accessibles avant un PIN vide, distinguer information et action actuelle, conserver historique, préférences et liens autorisés.
- **D1, P1 — préparation :** diagnostiquer le 2/3 et les périodes, puis exposer périmètre, responsable, échéance connue et prochain geste à partir des états métier existants.
- **E1, P1 — kit :** vérifier les fichiers et effets réels du téléchargement, présenter les supports selon leur usage et les dates en heure de Paris, distinguer QR d'inscription et QR participant.
- **F1, P1 — reprise :** vérifier puis compléter, si un manque est établi, la continuité après perte de réponse, expiration et retour différé. B1 porte le résultat de transaction ; F1 porte session, navigation et contexte.
- **Exclusions :** A1/G1, adoptées P2 par la simulation mais hors du lot de validation des maquettes ; tutoriel obligatoire, validation automatique, rappel push quotidien, fusion des états métier, déclaration prêt au téléchargement, succès hors connexion et remplacement du scanner, tous rejetés par la simulation. Aucun nouveau statut, borne de période, obligation métier, canal de notification, droit ou déploiement n'est décidé ici.
- **Dépendances :** diagnostic de l'existant avant changement ; QR et comptes de recette autorisés, téléphones physiques, kit réel, états incomplet/attente/prêt, réseau dégradé. D1 fournit les états fiables nécessaires à C1/F1 ; E1 dépend de l'inventaire du kit.

## Critères d'acceptation cibles

Ces critères cadrent le résultat à vérifier après la décision utilisateur. Les maquettes seules ne les satisfont pas ; voir le [bilan de réalisation](../../specifications/epic-80-fiabilite-parcours-localeo-pro/verification-livraison.md).

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E80-CA-01 · B1 | Commerçant, QR Animation invalide | Saisir ou scanner le QR | Rejet compréhensible, QR à demander et reprise indiqués ; aucun texte « pack » hors contexte, aucun succès local. |
| E80-CA-02 · B1 | Commerçant, QR de test autorisé | Reconnaître puis confirmer, y compris double clic ou doublon | Animation et étape lisibles avant confirmation ; résultat serveur certain et un seul effet métier. |
| E80-CA-03 · B1/F1 | Réponse perdue ou vérification indisponible | Vérifier l'opération existante puis revenir | Reçu relu sans mutation ; incertitude conservée si l'état reste inconnu ; aucun renvoi automatique ni succès présumé. |
| E80-CA-04 · B1 | Commerçant sur téléphone physique | Utiliser caméra autorisée/refusée et saisie manuelle | Voie de repli et résultat accessibles, focus et annonce du changement d'état compréhensibles. |
| E80-CA-05 · C1 | Message informatif ou tâche courante | Ouvrir puis marquer lu | Lecture distincte de l'achèvement ; seule une tâche établie par un état actuel reste visible après lecture. |
| E80-CA-06 · C1 | Principal ou salarié selon droits | Ouvrir notifications et lien d'action | PIN vide repliable et retrouvable ; fonctions existantes conservées ; destination autorisée après contrôle de session, sans supposer push/email reçu. |
| E80-CA-07 · D1 | Même compte, périmètre et instant | Comparer accueil et liste Animation | Compteurs cohérents ou différence de périmètre explicitée ; cause du 2/3 diagnostiquée avant correction. |
| E80-CA-08 · D1 | Période passée ou transition de date | Consulter animation et préparation | Classement conforme à la règle métier vérifiée ; aucune période active inventée par l'interface. |
| E80-CA-09 · D1 | Préparation incomplète, en attente ou prête | Consulter le prochain geste | Responsable, action autorisée et échéance connue visibles ; acceptation, approbation, installation, prêt et contrôle restent distincts. |
| E80-CA-10 · E1 | Kit de test autorisé | Télécharger, ouvrir et imprimer | Supports annoncés présents et lisibles, QR contrôlés ; téléchargement sans déclaration prêt automatique. |
| E80-CA-11 · E1 | Guide ou période de préparation | Lire dates et consignes | Instants en heure de Paris, bornes exactes et dates civiles préservées ; QR d'inscription et QR participant distingués. |
| E80-CA-12 · F1 | Interruption avant envoi, expiration ou retour après absence | Reprendre Pro | Droits et états actuels relus, contexte et actions encore valables retrouvables ; aucun rejeu, secret ou QR dans URL. |
| E80-CA-13 · transversal | Commerçants et aides techniques, tâches essentielles | Effectuer validation, préparation et reprise | Compréhension, erreurs, aide et temps consignés ; blocages d'accessibilité traités avant extension, sans gain revendiqué sans mesure. |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Applications et domaine propriétaire | **Concerné :** `localeo-commercant` pour les cinq parcours. **À examiner :** `localeo-backend` comme propriétaire des résultats, droits, états, compteurs, notifications et kit. `localeo-animation` seulement si une projection partagée ou les consignes du kit changent. Marketplace sans parcours modifié identifié à ce stade. |
| API et consommateurs | **À examiner :** contrats existants de validation/reçu, notifications/tâches, listes/compteurs et kit ; producteurs backend et consommateurs Pro, Animation éventuel. Toute modification d'OpenAPI documentaire reste dans ce dépôt. |
| Persistance, migrations et données existantes | **À examiner :** uniquement si le diagnostic impose un nouvel état, une projection ou une trace ; aucune migration déduite d'une maquette. |
| Générateur de démonstration et fixtures | **À examiner :** cas succès/doublon/incertitude, action lue encore ouverte, périodes et trois états de préparation ; ne pas générer sur un environnement réel. |
| Documentation fonctionnelle | **Concerné après choix des libellés :** aide Pro, guide de préparation, consignes QR et support de première connexion. Sources canoniques et lecteurs à identifier avant édition. |
| Exploitation et déploiement | **À examiner :** support d'accès réellement diffusé, recette sur téléphones, kit imprimé, accessibilité et reprise réseau ; ordre de livraison si le contrat backend évolue. Aucune ouverture à 500 commerçants déduite de cette epic. |

## Questions ouvertes

1. Le 2/3 observé en TEST provient-il d'un cache, d'un instant ou d'une donnée différente ? La liste et l'accueil locaux utilisent maintenant le même chargement complet, mais le constat TEST reste à revérifier.
2. Quels supports contient le kit TEST effectivement téléchargé, et quelle est leur lisibilité à l'impression ?
3. Les cas réels de doublon, perte de réponse, session expirée et retour différé respectent-ils les garanties couvertes localement ?

## Passage à la spécification

La [spécification E80](../../specifications/epic-80-fiabilite-parcours-localeo-pro/README.md) relie les critères aux invariants, contrats et preuves ; son bilan distingue les lots vérifiés des critères encore ouverts. Le [backlog potentiel du workshop](../../ux-workshops/localeo-pro/2026-11-18/validation/backlog-implementation-potentiel.md) reste une source de conception, sans devenir une seconde roadmap.
