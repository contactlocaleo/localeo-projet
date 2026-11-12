# E71-EVOL-08 — Agenda partagé et rendez-vous commerciaux

Demande du 12 novembre 2026. Extension du [CRM E71](README.md), dont le statut
reste **En cours**. Cette conception et sa réalisation locale ne constituent
ni une migration TEST, ni un déploiement. Les preuves sont renseignées dans
le [bilan de livraison](verification-livraison.md).

## Résultat attendu

Chaque collaborateur publie ses disponibilités commerciales. Depuis un prospect,
un gestionnaire repère la prochaine disponibilité des membres de l’équipe,
réserve un rendez-vous, ajoute une note et suit sa réalisation. Le rendez-vous
reste une action du prospect, identifiable par une icône calendrier et son
statut. Le collaborateur concerné reçoit une notification d’affectation et le
rappel prévu, selon ses préférences CRM existantes.

L’existant comporte des tâches de type `RENDEZ_VOUS`, mais aucune durée,
réservation de créneau ou disponibilité d’équipe. Ces tâches historiques restent
consultables ; elles ne sont pas transformées automatiquement en réservations.

## Choix de réalisation et extensions proposées

- **Choix confirmé le 12 novembre : agenda intégré au CRM**, partagé entre les
  utilisateurs internes habilités. Synchronisation Google/Microsoft hors périmètre.
- Un responsable par rendez-vous. Tous les gestionnaires CRM peuvent planifier
  un rendez-vous pour un membre habilité ; chacun configure son propre agenda.
- `PLANIFIE` signifie réservé, `VALIDE` signifie prise en charge confirmée par
  le responsable désigné, `REALISE` signifie entretien terminé avec compte rendu.
  **Validation par le collaborateur concerné confirmée le 12 novembre.**
- Heure de Paris, durées de 15 à 240 minutes, créneaux hebdomadaires et absences
  ponctuelles. Aucun horaire de travail n’est inventé pour un agenda non configuré.
- Report et annulation motivés, réaffectation avec nouvelle confirmation,
  prévention du double rendez-vous : compléments nécessaires à un agenda utilisable.
- Invitations au prospect, visioconférence, récurrence des rendez-vous,
  synchronisation externe et délai de déplacement automatique restent des
  propositions ultérieures. Aucun message commercial n’est envoyé au prospect.

## Parcours

**Agenda de l’équipe** : vue bornée par période, filtre par collaborateur et
navigation entre périodes. Chaque rendez-vous expose heure/durée, responsable,
prospect et état ; son détail ouvre la fiche ou les commandes autorisées.
Une liste chronologique utilisable sur mobile accompagne la lecture calendaire.
L’état vide distingue une période sans rendez-vous d’un échec de chargement.

**Mes disponibilités** : saisir plusieurs plages par jour de semaine, les retirer
et déclarer une absence datée. Afficher le fuseau. Une modification des horaires
ne déplace ni n’annule silencieusement une réservation existante. Une absence
ne peut pas recouvrir un rendez-vous actif sans résolution explicite du conflit.

**Fiche prospect → Nouveau rendez-vous** : nom du prospect conservé, recherche
de la prochaine disponibilité par membre pour une durée donnée. Choisir une
suggestion remplit le responsable et les dates ; la saisie manuelle reste
possible, avec la même validation serveur. Titre, note facultative et rappel
avant ou à l’heure de début. Une suggestion est indicative jusqu’à confirmation.
Le serveur refuse un créneau pris entre l’affichage et l’enregistrement sans
perdre la saisie. La confirmation identifie le responsable et la date réservée.

**Détail** : prospect, responsable, horaire/durée, statut, note et rappel visibles.
Le responsable confirme sa prise en charge. Un gestionnaire peut reporter,
annuler, réaffecter ou enregistrer la réalisation avec compte rendu. Un report
ou transfert remet le rendez-vous à `PLANIFIE`. Les rendez-vous terminés ou
annulés ne proposent plus les commandes d’un rendez-vous actif.

**Après entretien** : le compte rendu rejoint l’historique du prospect. Le bouton
« Planifier la prochaine action » réutilise la création d’action existante avec
le prospect déjà renseigné ; aucune action de suivi n’est créée implicitement.

**Notifications** : notification interne persistante et possibilité de la marquer
lue. Affectation et rappel constituent deux événements distincts. Les canaux
email/WebPush suivent les préférences, droits et appareils actuels du responsable.
Les contenus externes restent neutres ; le détail privé exige une session CRM.

## Domaine, invariants et transactions

Propriétaire : domaine `prospection`. Les règles pures de disponibilité,
chevauchement, dates et transitions sont dans `rendez_vous.py`. L’application
charge les faits, orchestre les transactions et utilise les ports de persistance
et de notification. API et PWA ne réimplémentent pas ces décisions.

- Intervalle réservé `[début, fin)` : deux rendez-vous adjacents sont possibles,
  un chevauchement pour le même responsable est refusé. Le créneau doit être
  futur et intégralement compris dans une disponibilité, hors absences.
- Instants avec fuseau obligatoires ; conversion depuis Paris contrôlée,
  heures inexistantes ou ambiguës refusées explicitement. Aucun décalage silencieux.
- Une réservation référence exactement un prospect et un utilisateur interne
  actif habilité à gérer le CRM. Un contact ou dossier éventuel appartient au
  même prospect. La politique centrale d’opposition et d’archivage reste applicable.
- Relation un pour un avec `crm_taches` ; même identifiant. Le rendez-vous porte
  ses états et sa durée ; la tâche conserve échéance, responsable et révision
  de rappel. Toute commande dédiée les synchronise atomiquement. Une commande
  générique d’action refuse une tâche portant une réservation.
- Une opposition ou un archivage bloque la sollicitation et ses rappels. Le
  rendez-vous reste visible et réserve son créneau jusqu’à son annulation ou
  traitement explicite ; le blocage est affiché séparément de l’état du rendez-vous.
- `expected_version` et clé d’idempotence protègent les commandes. Autorité
  transactionnelle relue avant tout reçu. Révision d’agenda modifiée sous verrou
  pour sérialiser réservation, report, transfert et absence ; verrous des agendas
  concernés dans un ordre stable, sans réseau dans une transaction.
- Toute mutation conserve la trace et le reçu dans la même transaction. Une
  création rejouée retourne la réservation existante et ne renotifie pas.
- Report/transfert/annulation/réalisation invalident les intentions de l’ancienne
  révision. Une remise déjà en transport conserve le traitement d’incertitude
  existant ; aucun rejeu aveugle d’un envoi dont le résultat est inconnu.

## Contrats et stockage

Producteur et consommateur : backend et PWA CRM servie par ce backend. Routes
privées sous `/internal/prospection`, lecture `crm.consulter`, mutations
`crm.gerer`, CSRF et contrôle de session actuels. La configuration d’agenda et
les notifications personnelles nécessitent un compte nominatif. Le compte
administratif peut consulter et gérer les rendez-vous sans devenir attribuable.

La migration additive v311 porte agendas, absences et réservations ; v312
distingue affectation et rappel dans les intentions de notification. Les tables
historiques et leurs migrations restent inchangées. Aucun rendez-vous historique
n’est notifié rétroactivement. Le contrat OpenAPI E71 V1.4 est régénéré depuis
les routes et modèles de réponse ; aucun contrat embarqué Animation, Pro ou
Marketplace n’est consommateur.

Les rappels externes réutilisent les flags et le worker existants, sans nouveau
fournisseur ni secret. Les préférences email exigent toujours une adresse interne
vérifiée et le WebPush un appareil volontairement abonné. Ne pas confondre
notification préparée, envoyée et reçue sur un appareil.

## Bornes et preuves de capacité

Recherche de disponibilité sur 31 jours au maximum, équipe paginée par 25
membres (maximum 100), agenda filtré par période et page bornée. Aucun chargement
automatique de toutes les pages. Index par responsable/date, plages et états
actifs ; enrichissement des noms/prospects par jointures ou lectures groupées.
Les résultats obsolètes d’une recherche UI sont ignorés.

Budgets locaux avant activation : lecture d’une page ou des prochaines
disponibilités p95 < 1 s ; réservation p95 < 1 s hors attente de conflit ; au
plus 10 requêtes SQL pour une page indépendamment du volume total. Mesurer N/10N
sur PostgreSQL jetable (100/1 000 réservations, puis historique hors période),
avec lectures et écritures concurrentes. Deux réservations du même créneau
doivent produire un seul succès ; deux créneaux adjacents sont autorisés, y
compris après réessai explicite du conflit transactionnel éventuel, avec la
même clé de commande et sans doublon.
Ces budgets sont des cibles, pas des résultats annoncés.

## Critères et traçabilité

| Critère | Résultat observable | Preuves reliées au bilan |
| --- | --- | --- |
| E71-CA-62 | Chaque membre configure ses plages et absences ; absence de configuration explicitée | Domaine plages/DST, autorisation propriétaire, persistance et parcours UI |
| E71-CA-63 | Agenda partagé filtrable et borné, détail relié au prospect | API pagination, états vide/erreur, mobile/ordinateur |
| E71-CA-64 | Prochaine disponibilité réelle de chaque membre pour la durée choisie | Domaine créneaux, calendrier occupé, absences, pagination équipe |
| E71-CA-65 | Création depuis le prospect, dates/heure/note et responsable enregistrés | Service/API, appartenance contact/dossier, rejeu et rollback |
| E71-CA-66 | Planifié → Validé → Réalisé ; annulation distincte, confirmations autorisées | Transitions domaine, refus auteur/état, concurrence et UI |
| E71-CA-67 | Report/transfert sans double réservation et sans ancien rappel | PostgreSQL concurrent, version obsolète, invalidation et conflit conservant la saisie |
| E71-CA-68 | Rendez-vous visible parmi les actions avec calendrier et état propre | Projections tâche, dashboard/fiche/liste/détail ; anciennes tâches préservées |
| E71-CA-69 | Nouvelle affectation notifiée au membre concerné une seule fois | Intention atomique, préférences/droits, lecture personnelle et marquage lu |
| E71-CA-70 | Rappel distinct selon les canaux choisis, annulé si devenu caduc | Domaine, workers, révision/compte/appareil révoqués, incertitude transport |
| E71-CA-71 | Compte rendu conservé et accès direct à la prochaine action | Domaine résultat obligatoire, historique et parcours prospect prérempli |
| E71-CA-72 | Droits, opposition, archivage et idempotence conservés partout | API/SQL, commandes génériques refusées, absence de mutation partielle |
| E71-CA-73 | Parcours accessible et coût borné malgré l’historique | Mobile/ordinateur/clavier, contrats, requêtes/plans N/10N et charge mixte |

Documentation fonctionnelle : présente conception et guide utilisateur E71.
Exploitation : ordre v311 puis v312 avant backend, readiness, worker et rollback
applicatif sans suppression des réservations. Démonstration : tables nouvelles
classées dans le périmètre de sauvegarde/restauration, fixtures synthétiques
d’agenda et rendez-vous via les services ordinaires ; aucune génération sur une
base partagée autorisée ici.
Les trois autres applications sont sans impact : elles ne consomment pas ces
routes privées ni les données des collaborateurs commerciaux.
