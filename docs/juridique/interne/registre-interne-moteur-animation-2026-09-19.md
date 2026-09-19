# Registre interne — complément technique du moteur d’animation

Date : **19 septembre 2026**. Politique technique : `moteur-animation-conservation-v1`.

**Statut : code vérifié localement, non déployé.** Ce complément reporte les catégories et contrôles du moteur dans le registre interne. Il reprend les décisions validées ; il ne modifie ni les PDF juridiques, ni les finalités, fondements ou durées des autres traitements.

## 1. Références et périmètre

- [Annexe A — registre simplifié et tableau de conservation, V1 du 13 septembre 2026](<Annexe A - Registre simplifié des traitements et tableau de conservation des données - V1.pdf>), pages 4–6 : fichiers temporaires, participants Animation, notifications, preuves, archives, gels et sauvegardes.
- [Spécification du moteur, §11.3](../../specifications/moteur-animation/localeo_animation_engine_spec.md#113-conservation--règles-documentaires-existantes-et-compléments) : catégories propres au moteur et à la génération.
- [Conception technique, §8.2 et précisions T6-R01 à T6-R11](../../specifications/moteur-animation/conception-technique.md#82-conservation-et-purge) : calcul des échéances, protections et reprise.
- [Procédure d’exploitation du moteur, §4–5](../../specifications/moteur-animation/exploitation-moteur.md#4-conservation-quotidienne) : activation, ordonnanceur, rapports et gels.

Le périmètre couvre Passeport, Tombola et Chasse : génération éditoriale, fichiers préparés, essais joueurs, accès personnels, participants, notifications Animation et reçus de participation. Les notifications Live, le carnet local, les pièces comptables et les preuves de tirage/gain gardent leurs catégories propres de l’Annexe A. La suppression locale du carnet ne supprime pas les participations serveur.

## 2. Catégories, échéances et éléments conservés

Les jours techniques représentent **24 heures** depuis l’instant UTC persisté. Les **12 mois sont calendaires**, en UTC, avec rabattement au dernier jour du mois si nécessaire. La fin de référence est la **fin effective serveur**, intégrant une prolongation autorisée ; cette prolongation recalcule aussi l’échéance des essais, des accès personnels et des reçus concernés sans réactiver un accès révoqué. Une consultation ne décale aucune échéance (T6-R02 et T6-QA02).

| Catégorie du traitement | Échéance et déclencheur | Sortie et protections |
| --- | --- | --- |
| `GENERATION` — prompts, réponses, artefacts devenus inutiles | 30 jours après `terminated_at`, uniquement pour une demande effectivement `TERMINEE` ou `ANNULEE`. | Retirer le brut et les copies gérées devenus inutiles ; conserver seulement les métadonnées nécessaires et le statut de purge. Toute référence utile ou gel protège le contenu. Une version rejetée/remplacée n’est pas supprimable tant qu’elle reste utile. |
| Demandes en attente, en correction ou en reprise de finalisation | Aucune expiration automatique par ancienneté ou changement de mois. | Le délai de génération ne démarre pas avant une terminaison/annulation effective. Aucun quota n’est libéré ou consommé par la purge. |
| Versions acceptées, templates et provenance utiles | Conservation tant qu’ils servent une animation, un historique nécessaire ou une bibliothèque réutilisable. | La fin de la demande ou le retrait de la bibliothèque ne suffit pas si une autre dépendance demeure. |
| `FICHIERS_PREPARES` — écritures de génération/flyer sans rattachement | 30 jours depuis la préparation **et** bail expiré. | Recontrôler références et gels ; supprimer uniquement les fichiers inventoriés. Aucun balayage global du stockage ne supprime un fichier inconnu. |
| `ESSAIS` — détail des réponses et tentatives de défi | 90 jours après la fin effective de l’animation. | Supprimer les détails ; préserver compteurs, progression, preuves de passage, qualification figée, reçus encore nécessaires, population, tirages et gains. |
| `TOKENS` — jetons personnels de participation | Validité jusqu’à la fin effective +90 jours, puis suppression selon les contrôles de conservation. | Un gel de conservation ne réactive pas un accès expiré ou révoqué. |
| `PARTICIPANTS` — coordonnées d’usage courant | 12 mois calendaires après la fin effective. | Retirer les coordonnées des listes opérationnelles, conserver les identifiants stables et liens probatoires. Une identité encore nécessaire est isolée dans l’archive restreinte ci-dessous. |
| `NOTIFICATIONS` — notifications Animation et commerçantes | 12 mois calendaires après création. | Supprimer sauf référence/protection utile, notamment preuve d’envoi liée à un lot ou une réclamation ; les notifications Live restent dans leur politique distincte. |
| `RECUS_PARTICIPATION` — reçus de jeu et d’attestation | Fin effective +90 jours, expiration du reçu atteinte, après suppression de ses éventuels essais. | Ne pas assimiler les reçus de correction, neutralisation et gel à cette catégorie ; ils restent dans leur circuit probatoire. |
| `ARCHIVES_IDENTITE` — coordonnées séparées de l’usage courant | Réexamen quotidien de la nécessité ; suppression possible dès disparition du besoin et des gels. | Aucun délai autonome de cinq ans appliqué aux coordonnées. Les besoins autorisés sont décrits en §3. |

Les durées documentaires existantes des **preuves nécessaires de tirage, attribution et remise sont de cinq ans** ; les **pièces comptables suivent dix ans à compter de la clôture de l’exercice concerné**. Elles restent séparées de ces catégories de purge. Le complément ne crée pas de purge automatique de ces preuves ou pièces au sein du traitement du moteur.

## 3. Archives nominatives, preuves et gels

Le retrait nominatif courant conserve les références stables ; le statut technique `ANONYMISE` ne signifie pas que les données restantes sont anonymes. Une participation encore rattachable à une personne est pseudonymisée et reste soumise au registre (Annexe A page 5, T6-R05 et T6-R08).

L’archive nominative contient uniquement les coordonnées encore nécessaires au traitement d’un gain/lot, d’une population figée ou d’un gel ciblé. Le besoin comprend un membre éligible d’une population figée sans tirage réalisé, un gain à envoyer ou en échec, et un suppléant mobilisable tant qu’un gain du même tirage reste à traiter. Le motif, les références et la date de réexamen sont conservés ; le gel possède son périmètre, auteur, justification et dates (T6-R05, R08–R09).

Une attribution ou substitution tardive conserve le statut `ANONYMISE` et ne crée pas d’éligibilité. Seule une copie destinée à l’envoi reçoit les coordonnées archivées ; la participation courante n’est pas réécrite. Une archive absente bloque explicitement le traitement ou la relance. Aucune API générale n’expose ces identités. L’archive n’est utilisée ni pour prospecter, ni pour alimenter le catalogue, ni pour réactiver des accès.

Les gels visent les seuls éléments nécessaires. Leur pose et leur levée sont tracées ; la levée remet la cible dans le contrôle ordinaire et ne déclenche pas de suppression immédiate. Une exclusion est réévaluée lors des exécutions suivantes. Les gels d’identité protègent l’archive séparée et ne prolongent pas l’exposition nominative courante.

## 4. Contrôles avant suppression et reprise

Les règles T6-R01 à R11 sont appliquées par le même service de conservation :

| Règle | Contrôle technique repris |
| --- | --- |
| R01 | Service unique pour simulation, exécution, reprise, gels et rapports. Accès ERP avec session `ADMIN` explicite ; contexte système distinct pour le batch. Aucun droit déduit d’une permission de modification ou de quota. L’ancienne entrée de purge délègue au même service. |
| R02 | Échéances du §2, vérifiées côté serveur ; reçus expirés traités après les essais, sans confondre reçus joueur et preuves d’exploitation. |
| R03 | Intention persistée avant toute écriture de fichier de génération/flyer, avec périmètre, clé contrôlée et bail. Rattachement sous le même verrou, refus de `PURGE_EN_COURS`/`PURGE`. Artefacts antérieurs déjà inventoriés contrôlés selon leurs dépendances. |
| R04 | Relecture sous verrou de l’échéance, de l’état, des références utiles et des gels. Marquage transactionnel et intention avant suppression externe hors transaction ; « déjà absent » vaut succès. Une erreur conserve marqueur et tâche reprenable. Toute nouvelle référence ou pose de gel après marquage est refusée. |
| R05 | Identifiants stables et liens probatoires conservés ; identité utile séparée. Aucune suppression en cascade des populations, tirages, gains, preuves liées ou pièces comptables. |
| R06 | Lot identifié par politique, date UTC, catégorie et mode. Bail renouvelable avec un seul propriétaire ; reprise des éléments déjà marqués avant le curseur ordonné d’échéance/identité. Rapport paginé sans donnée brute. |
| R07 | Une exécution réelle exige une simulation terminée de la même politique/catégorie. Un run inachevé reprend avant tout nouveau run, même après changement de date ; les candidats sont recontrôlés sous verrou. |
| R08 | Retrait nominatif courant à 12 mois ; archive limitée au besoin réexaminé quotidiennement, indépendante de la durée de cinq ans des preuves. Lecture interne limitée au traitement du gain. |
| R09 | Population figée, gain et suppléance tardifs traités selon §3 ; coordonnées absentes bloquantes, sans réécriture du participant ni création d’éligibilité. |
| R10 | Flyer d’un retrait Passeport/Tombola préparé hors transaction avant la commande idempotente ; version de demande et empreinte recontrôlées avant rattachement. Reçu confirmé rejoué sans nouveau fichier. Une préparation abandonnée reste inventoriée et purgeable. Droits et reçus historiques inchangés. |
| R11 | Réimport des mêmes octets possible dans un nouvel artefact, sans réactiver la clé supprimée. La déduplication ne pointe vers le nouveau qu’après purge de l’ancien et disparition des références utiles. Une écriture tardive déjà marquée est refusée au rattachement et conserve son intention de suppression reprenable. Reçus de jeu/attestation traités après leurs essais ; reçus probatoires distincts conservés dans leur circuit. |

Les copies actives et exports temporaires gérés du même périmètre sont retirés ; les métadonnées éditoriales inutiles ne deviennent pas une copie cachée du contenu purgé. Les journaux et rapports conservent les seules références, dates, statuts, motifs et résultats nécessaires, jamais le texte privé, les réponses brutes, tokens ou clés de stockage.

## 5. Simulation, rapports et sauvegardes

L’ordonnancement prévu est quotidien à **03:30 UTC**, par lots initiaux de **100**, configurables. `LOCALEO_ANIMATION_CONSERVATION_APPLY=false` maintient la simulation par défaut ; l’activation sur une cible reste une opération distincte. La purge automatique ne demande pas une validation manuelle de chaque exécution. La console ERP permet consultation et gels, sans bouton de purge réelle (procédure §4–5).

Le rapport persiste identifiant, politique, catégorie, mode, dates, état, compteurs examinés/supprimés/éligibles en simulation/exclus/erreurs, raisons, codes d’erreur sûrs et curseur de reprise. Les exclusions peuvent notamment signaler une échéance non atteinte, une préparation en cours, un gel ou une référence conservée. Une suppression partielle reste visible et reprenable ; le rapport n’annonce pas un succès du stockage en cas d’erreur. La supervision signale les échecs ainsi que l’absence d’exécution ou un retard de plus de 26 heures.

Les sauvegardes restent réservées à la continuité du service et suivent leur cycle de remplacement existant. Une restauration réapplique les suppressions dues et ne réactive pas les accès révoqués. Aucun nouveau délai de sauvegarde n’est fixé ici ; la vérification de restauration sur la cible relève de la procédure d’exploitation.

## 6. État de vérification

Les preuves locales de domaine, PostgreSQL jetable et interface ERP sont recensées dans le [suivi d’implémentation](../../specifications/moteur-animation/suivi-implementation.md). Elles couvrent notamment courses de gel/réutilisation/purge, reprises de stockage, archives nécessaires et protection des preuves. La [recette transversale](../../specifications/moteur-animation/recette-pilote.md) vérifie aussi une prolongation réelle suivie du gel/tirage : aucune purge à l’ancienne échéance, puis suppression des essais à la nouvelle fin +90 jours sans altération des preuves, population ou gains.

Ces vérifications ne déclarent ni migrations appliquées en exploitation, ni ordonnanceur activé, ni purge ou restauration réalisée sur un environnement déployé. Les contrôles de cible restent à consigner avant ouverture.

[Retour à l’index juridique](../INDEX.md).
