# Suites de l’audit CRM du 18 novembre 2026

Conception du **19 novembre 2026**, puis réalisation locale dans la même
demande ; preuves et limites dans le bilan. [Cadrage et critères E71-AUD-01 à 09](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md#audit-crm-20261118),
[décision utilisateur UX01–UX05](../../ux-workshops/localeo-crm/2026-11-18/validation/decisions.md).
L’EPIC 71 reste **En cours** ; CA-01 à 84 et leurs preuves historiques sont
conservés. Les neuf critères AUD complètent la recette de cette évolution.

## Existant et écarts

Le vrai shell est `localeo-backend/app/infrastructure/pwa/crm/crm.js`, l’agenda
`crm-agenda.js`. Les endpoints privés sont produits par `prospection_api.py` et
`prospection_rendez_vous_api.py`, consommés directement par cette PWA. Les
projections et curseurs proviennent de `prospection_core.py`/`prospection_lectures.py`.

- Aujourd’hui expose déjà trois groupes paginés et leurs totaux issus d’un même
  instant signé ; les indicateurs collectifs sont repliés. Réutiliser ces groupes.
- Prospect, dossier et tâche ont des responsables distincts ; certains formulaires
  affichent seulement « Responsable ». La création affecte le dossier uniquement.
- Le formulaire de tâche reçoit un dossier facultatif depuis le détail dossier,
  mais la création depuis le prospect n’offre pas de choix explicite de dossier.
- L’état vide de dernière interaction passe `null` à `replaceChildren`, qui le
  convertit en texte. Retirer cet enfant sans masquer une erreur de lecture.
- La réservation RDV revient à la fiche par le cycle générique du formulaire.
  Ajouter une confirmation avec accès au détail enregistré et à son jour d’agenda.
- Report, modification, annulation, réalisation et compte rendu existent déjà.
  La prochaine action du détail RDV perd le dossier associé : transmettre celui-ci.

## Invariants, droits et frontières

Le domaine `prospection` conserve les règles d’appartenance, affectation,
sollicitation, échéances, transitions, compte rendu, idempotence et concurrence.
Les services existants orchestrent les commandes ; aucune transition ou nouvelle
politique de rappel dans le navigateur. Lecteur : consulter uniquement ;
gestionnaire : commandes existantes, droits revérifiés côté serveur, version et
clé d’idempotence conservées. Un conflit garde la saisie ; une réponse incertaine
ne confirme pas le succès et se réconcilie par la même commande/clé.

## Lots et comportement cible

### A — Correction et recette existante (AUD-01/02/08/09)

Sans échange : afficher uniquement « Aucun échange consigné ». Avec échange :
type, date Paris et contenu ; erreur : réessai de la section. Réutiliser les
preuves de recherche/retour ; vérifier droits distincts, mobile et clavier.

### B — Responsabilités et rattachement (UX03/04, AUD-04/05)

Création prospect : « Responsable du premier dossier », annonce explicite du
prospect non attribué et accès à son affectation après création. Création/édition
dossier : « Responsable du dossier ». Tâche : « Responsable de l’action ».
Les récapitulatifs indiquent ce qui change et les responsabilités conservées.

Le formulaire d’action affiche le prospect et un contexte « Prospect uniquement »
ou un dossier sélectionné. Depuis un dossier, ce contexte est fixé et annoncé.
Depuis le prospect, sélecteur de dossiers paginé via l’API existante, sans charger
le portefeuille complet. Le choix alimente uniquement `opportunite_id` ; le
serveur vérifie l’appartenance. Une action générale ne couvre pas les dossiers.
Expliquer « Sans prochaine action » et conserver action/rappel distincts.

### C — Résumé et pilotage (UX01/02, AUD-03/06)

Résumé compact des trois totaux déjà reçus d’Aujourd’hui, même portée et instant de référence
Paris ; chaque total mène au groupe correspondant sans nouvelle requête de
comptage. Zéro personnel expliqué ; accès Équipe explicite. Erreur/chargement
ne deviennent jamais zéro. Accès visible aux listes de pilotage existantes.

Ajouter des filtres de lecture booléens optionnels `sans_responsable` et
`sans_prochaine_action` et `sans_interaction_recente` sur GET `/organisations` : prospects actifs selon le
filtre `etat`, responsable du prospect nul, ou aucune tâche OUVERTE au niveau
du prospect (y compris ses dossiers). Paramètres combinables, appliqués en SQL
avant total et pagination signée. Aucun changement des requêtes sans ces
paramètres. Source canonique : `openapi.json`, générateur backend documentaire.

La vue de pilotage distingue prospects non attribués, prospects sans action et
dossiers sans action ; listes chevauchantes non additionnées. Responsables des
prospects et dossiers restent distincts ; filtres actifs visibles et retirables.
Les retards et RDV à venir ouvrent les surfaces existantes. **Décision complémentaire reçue : 30 jours sans interaction, 60 jours sans
évolution**, pauses justifiées et dossiers clos exclus des deux alertes.
`GET /organisations?sans_interaction_recente=true` sélectionne les prospects
actifs créés depuis au moins 30 jours, sans NOTE/APPEL/EMAIL/RENDEZ_VOUS/CORRECTION
sur les 30 derniers jours. Sans dossier, le prospect reste éligible ; avec des
dossiers, au moins un doit être hors PAUSE/GAGNEE/PERDUE. Les traces techniques
d’affectation, tâches et imports ne constituent pas une interaction.
`GET /opportunites?sans_evolution=true` sélectionne les dossiers actifs hors de
ces trois étapes, créés depuis au moins 60 jours, sans transition vers une étape
différente sur les 60 derniers jours. Le journal canonique de transition
« ancienne étape → nouvelle étape : motif » permet d’ignorer une reconfirmation
sans changement ; éditer le titre ne remet pas le délai à zéro. Le cutoff est
inclusif, en durées glissantes de 24 heures ; sans historique, prendre la création.
Les paramètres de politique appartiennent à `app/domaine/prospection/risques.py` ;
SQL projette ces faits sans mutation. Les autres listes sans action conservent
leur définition historique, pauses comprises et explicitement annoncées.

### D — Continuité RDV (UX05, AUD-07)

Après réservation/report confirmé : titre, date Paris, responsable, rappel
interne et liens vers détail et agenda au jour du RDV. Réalisation : compte rendu
obligatoire selon domaine, proposition facultative de prochaine action avec
contexte dossier conservé ; « Plus tard » ne crée rien. Depuis le détail, lien
direct vers la bonne date d’agenda. Modifier/report/annuler réutilisent leurs
commandes et contrôles actuels ; aucun message prospect automatique.

## Impacts et matrice de preuve

| Critères | Preuves prévues | Documentation / données / exploitation |
| --- | --- | --- |
| AUD-01/03/04/05/06 | Navigateur synthétique : vide/échange/erreur, portées, deux dossiers et propriétaires, rattachement refusé/conservé, listes et filtres | Guide CRM et contrat de lecture ; fixtures fictives, générateur déjà doté de dossiers/tâches à responsables distincts, couverture à confirmer |
| AUD-02 | Recettes `crm-productivite.cjs`, `crm-recherches-locales.cjs`, `crm-prospects-filtres.cjs` | Réutilisation de la convention de préservation du contexte |
| AUD-07 | Recettes RDV navigateur et tests application/domaine existants : transitions/refus, conflit, rappel caduc, compte rendu, suite facultative | Guide RDV ; transports isolés, aucun envoi réel |
| AUD-08/09 | Lecteur/gestionnaire, révocation, clavier, 390/1280 px, absence de débordement | Recette synthétique distincte du déploiement et des appareils physiques |
| Filtres UX02 | API : transmission/refus booléen ; PostgreSQL : positifs/négatifs, plusieurs pages, total/cursor, plans N/10N | Requêtes bornées ; index existants organisation/tâches, budgets locaux : page de 25, au plus 12 requêtes SQL et moins de 2 s ; plans et mesures N=1 000/10N=10 000 avec 10 événements et 4 tâches terminées par prospect |

Seuls `localeo-projet` et `localeo-backend` sont concernés. Aucun consommateur
public Marketplace/Pro/Animation modifié ; comptes ERP et worker existants
inchangés. Pas de nouvelle table, migration, paramètre opérateur ou tâche
planifiée pour les lots décrits. Le générateur reste dans backend ; ne pas
modifier les données TEST. Déploiement, import et nettoyage TEST hors demande.

## Réalisation et reprise

Lots A/B/C/D implémentés localement ; aucune décision de seuil restant ouverte.
La revue indépendante sur extrait a demandé de vérifier réponse tardive,
contexte dossier, date Paris, permissions et focus : le garde de génération du
formulaire, la résolution du vrai libellé du dossier et les scénarios navigateur
ont été complétés. La revue n’a pas consulté les fichiers et ne vaut pas revue
complète du diff.

Les résultats exécutés, les rapports de tentatives et limites sont dans le
[bilan E71](verification-livraison.md#workshop-crm-20261118). Aucun accès à un environnement d’exploitation, import, notification externe,
commit, push ou déploiement effectué. Les recettes
humaines et physiques restent distinctes des preuves synthétiques.
