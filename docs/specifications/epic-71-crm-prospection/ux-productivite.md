# E71-EVOL-10 — UX quotidienne et productivité

**12 novembre 2026 · spécification V1.6 · six lots implémentés, recette locale.**
[Audit et preuves](../../audits/backend/localeo-crm-ux-productivite-2026-11-12.md),
[backlog canonique](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md),
[architecture](architecture-contrats.md), [bilan](verification-livraison.md).

Après l’audit et la spécification, l’utilisateur a demandé l’implémentation des
six lots, leurs commits/push et une migration TEST si nécessaire. Les preuves
exécutées et les limites figurent dans le [bilan](verification-livraison.md).
Aucune migration supplémentaire ni modification de droits n’est nécessaire.
Aucun import réel ni envoi n’a servi à la recette. L’epic reste **En cours**.
CA-01 à 77 gardent leurs identifiants et règles ; CA-24 reste reporté.
**Sept critères ajoutés, CA-78 à 84 : 84 identifiants, 83 actifs.**

## Besoin et décisions de conception

Réduire les manipulations nécessaires pour trouver le bon interlocuteur,
consigner un échange, préparer la suite et reprendre le travail. Acteurs :
lecteur CRM, gestionnaire commercial nominatif, responsable consultant l’équipe,
importateur et administrateur des droits. Ces usages ne créent pas de nouveaux
profils ni de restriction implicite du portefeuille partagé.

Les retours conservés, la file personnelle, les compteurs cohérents, la proposition
de prochaine action et l’accessibilité mobile figurent déjà dans
[Parcours et règles](parcours-regles.md). Les lots corrigent ces écarts et ajoutent
des présentations/assistances ciblées. Aucun pipeline, barème, règle de gain,
consentement ou statut métier n’est remplacé.

Propositions retenues pour la conception, à évaluer pendant la recette : cinq
entrées mobiles fixes, contact/action en tête de fiche, détails de qualification
secondaires, indicateurs collectifs après les actions. Une recette peut ajuster
la composition sans changer les règles de domaine. Pas de refonte de framework,
de synchronisation d’agenda externe, de campagne prospect, d’automatisation de
gain ou de saisie hors ligne. Les favoris partagés, actions de masse et mesures
d’activité persistantes ne sont pas ajoutés sans besoin distinct.

## Lots, dépendances et traçabilité

Ordre conseillé : **L1 → L2**, puis L3 et L4 ; L5 peut avancer après L1 ; L6
réutilise les contextes de L1 et les explications de L5. Les travaux indépendants
ne nécessitent pas la fin de tous les lots pour être spécifiés.

| Lot / effort relatif | Résultat et constats | Critères existants à renforcer | Critères ajoutés / preuve prévue |
| --- | --- | --- | --- |
| L1 — Continuité, listes, navigation · M | UX-01/04/08 : retour contextualisé, lignes identifiables, recherche Suivi, filtres mobiles, icônes cohérentes | CA-07/15/19/22, retours agenda de CA-62 à 73 | Test recherche page 3 → fiche → deux retours ; trois dossiers homonymes ; clavier/320/390/1280 px et texte 200 % |
| L2 — Fiche et journée de travail · M | UX-02/03/05 : file personnelle/équipe, contact et prochaine action avant détails, suite facultative | CA-04/05/06/15/21/22/60/61 | CA-78 ; sections en panne indépendantes, succès/409/réponse perdue, deux responsables avec compteurs distincts |
| L3 — Agenda exploitable · M | UX-09/10 : contexte, report assisté, semaine partielle explicite | CA-62 à 73 et CA-15/21 | CA-80 ; 60 RDV, changement de jour, report concurrent et ancien rappel invalidé |
| L4 — Cibles et preuves lisibles · M | UX-06/07/15 : références sans UUID, tous les contacts sélectionnables, diagnostic d’accès | CA-03/16/17/18/19/20/21/34 | CA-79 ; contact n°26, référence interdite, preuve concurrente, session expirée/droit retiré |
| L5 — Imports et qualification guidés · L | UX-11/12/13 : progression, revue par page et suite contextualisée | CA-08 à 12, CA-41 à 59 | CA-81/82/83 ; 60 propositions, job en attente/partiel, sélection IDS=1, refus et reprise sans doublon |
| L6 — Carte homogène et recette complète · M | UX-14 ; cohérence transversale et mesure de départ/après | CA-13/15/23/50/54/55/74 à 77 | CA-84 ; mêmes filtres et répartitions, mixte/non localisé, fournisseur indisponible, scénario quotidien de bout en bout |

Chaque lot adapte guide, contrats et preuves touchés avant sa livraison. Les
efforts sont relatifs, pas des engagements de délai. Ce tableau conserve les
preuves demandées à la conception ; le bilan indique leurs exécutions effectives.

## L1 — Reprendre exactement son travail

Un contexte interne borné décrit route source, filtres autorisés, tri, curseur,
vue, date/collaborateur pour l’agenda, élément sélectionné et position. Les
filtres partageables restent dans l’URL ; la position et la pile bornée de
curseurs restent dans l’historique de navigation de l’onglet. Ne pas placer
notes, coordonnées ou résultats privés en stockage persistant. Un curseur
périmé peut conduire à la première page **avec explication**, sans effacer les
filtres valides. Changer de filtre remet la pagination à zéro explicitement.

En haut du détail : « ← Résultats de recherche », « ← Aujourd’hui »,
« ← Rappels » ou « ← Agenda de l’équipe » selon la provenance. Accès direct :
retour de repli simple vers la collection. Même effet pour le retour navigateur.
Valider les destinations internes dans la liste fermée des routes CRM : aucun
`return_to` externe, ni contournement de connexion/habilitation. Au retrait des
droits ou à la déconnexion, effacer les résultats et contextes privés.

Chaque ligne expose le nom du prospect et sa commune avant le titre du dossier
ou de l’action ; responsable nommé, date/type et prochaine action si pertinente.
Responsables prospect/dossier/tâche restent explicitement distincts. Historique :
résoudre les noms via projection bornée, nom de repli « Compte indisponible » ;
identifiant technique replié dans les détails de diagnostic uniquement.
La recherche Suivi utilise `q` côté serveur sur toute l’audience, jamais uniquement
sur les 25 lignes visibles. Zéro résultat ≠ erreur ; filtres conservés au réessai.

Mobile : Aujourd’hui, Prospects, Agenda, Rappels, Plus. Plus contient Suivi,
Qualification, Carte, Imports et Préférences selon autorisation. Son état actif
annonce la sous-destination ; le menu Applications conserve son rôle distinct.
Recherche immédiate, « Filtres (n) » ouvrant un panneau accessible avec Appliquer/
Réinitialiser ; récapitulatif des critères actifs. Pas de défilement horizontal
pour la navigation principale ; cibles ≥44 px, focus visible, texte 200 %,
labels visibles pour toutes les actions ambiguës. Les icônes existantes sont
harmonisées par sens, taille/trait et alignement ; pas de secours « succès »
pour une action non représentée. Le tableau de l’audit porte les remplacements.

## L2 — Voir qui contacter et préparer la suite

Aujourd’hui ouvre « Mes actions » pour un compte nominatif. Vue « Équipe »
explicite, disponible selon les droits CRM actuels ; un ADMIN système sans
identité personnelle ouvre Équipe. Regrouper En retard / Aujourd’hui / À venir,
sans présenter une réservation terminée ou une tâche fermée comme à faire.
Chaque groupe est paginé côté serveur ; compteurs, contenu et liens utilisent
exactement la même portée, date de référence Paris et règle de retard.
« Mes actions » désigne le responsable de la tâche ou du RDV, jamais le créateur
ni le responsable du prospect. À un instant de référence commun fourni par le
serveur : En retard = `due_at < instant_reference` ; Aujourd’hui = éléments
restants prévus le jour courant à Paris ; À venir = éléments des jours suivants.
Les groupes sont disjoints. Une tâche prévue demain avec un rappel disponible
aujourd’hui reste À venir, avec indication du rappel, sans seconde comptabilisation.
La prochaine action d’un rendez-vous ouvre son détail, avec le libellé et l’icône
RDV ; ne pas ajouter une seconde ligne pour la tâche liée au même rendez-vous.
Conserver la distinction des anciennes tâches de type RENDEZ_VOUS, qui ne sont
pas des réservations. Pas d’addition de compteurs hétérogènes dans le navigateur.

Dans la fiche, ordre cible :

1. Nom/commune, statut/opposition, responsable du prospect et retour.
2. Contact immédiatement utilisable, dernière interaction et prochaine action.
   Sans contact : « Aucun contact renseigné », Ajouter selon droits. S’il y en a
   plusieurs sans principal métier défini, montrer les choix sans inventer un
   « principal » ; conserver la dernière sélection seulement pendant la session.
3. Actions « Appeler », « Noter un échange », « Planifier », « Nouveau rendez-vous ».
   Téléphone absent ou sollicitation interdite : état explicite ; la note factuelle
   reste possible selon les règles existantes.
4. Dossiers, autres contacts, historique et qualification détaillée en sections.

Lire le prospect/son accès avant de charger les sous-sections ; ensuite, lectures
indépendantes avec gabarits stables, résultats bornés, état vide et réessai local.
Une panne d’historique ne masque pas les coordonnées. Un refus d’accès global
efface toute la surface privée ; une panne réseau d’une section conserve les
autres sections autorisées. Ne jamais recharger automatiquement une mutation.

Après succès confirmé d’une note/appel ou réalisation d’action : « Appel enregistré »
ou « Action terminée », puis « Planifier la prochaine action » et « Revenir à la
fiche ». Prospect/dossier connus préremplis, cible visible/modifiable selon droits.
Cette proposition est facultative. Pas de tâche créée à la fermeture ; une réponse
incertaine conserve commande/clé et procédure de réconciliation existantes avant
d’afficher un succès. Préserver les règles CA-60/61 des rappels : pas de nouveau
comportement par défaut introduit par un raccourci visuel.

## L3 — Agenda et report

URL et retour conservent date, semaine/jour, collaborateur et page ; raccourci
« Aujourd’hui ». La semaine reste une vue paginée : indiquer « 25 rendez-vous
affichés — suivants disponibles » si `has_more`, jamais « jour libre » sur une
page incomplète. Si une page suivante vide résulte d’une modification concurrente,
afficher « Aucun rendez-vous sur cette page » et proposer Précédente/Première.
« Aucun rendez-vous sur cette période » seulement quand la lecture de la première
page complète établit ce résultat. Une journée reste sélectionnable sur mobile,
même si elle n’a aucun élément dans la page actuelle.

Reporter réutilise le sélecteur de disponibilités de création : ancien créneau, collaborateur,
durée et note conservés à l’ouverture ; choix d’un nouveau début remplit la fin.
Le collaborateur est non modifiable dans Reporter ; un changement de responsable
passe par l’action Réaffecter existante, avec ses règles propres. Les suggestions
ne doivent pas laisser croire à un transfert implicite depuis un créneau d’autrui.
Le motif reste requis. Ne jamais promettre un créneau avant la réservation
transactionnelle. Sur conflit, conserver les choix/motif et proposer de relire
les disponibilités. Date du rappel : conserver le défaut existant à l’heure du
rendez-vous ; proposer « À l’heure », « 15 min avant », « 1 h avant »,
« Personnalisé », avec résultat en heure de Paris. Ne pas ajouter une désactivation
de la date : les canaux externes restent régis par les préférences CRM. Validation
personnelle et rappels obsolètes suivent [Rendez-vous](rendez-vous.md).

Les lectures `/agenda/equipe` et `/agenda/creneaux` doivent accepter un contexte
optionnel `rendez_vous_id` pour le report. Après vérification de l’accès au RDV et
du droit de le reporter, exclure **sa seule occupation** du calcul ; les autres
réservations, absences et plages restent contraignantes. Lier ce contexte au
curseur de disponibilité ; refus d’un curseur utilisé avec un autre RDV ou filtre.
La mutation revalide version et disponibilité, indépendamment de la suggestion.
Cas de preuve : déplacer 10 h–11 h à 10 h 15–11 h 15 sans autre conflit est proposé
et accepté ; le même déplacement reste refusé s’il croise une autre réservation.
Un ID interdit ne permet jamais de faire disparaître une occupation d’autrui.

## L4 — Choisir la bonne cible sans identifiant technique

Planifier une action et enregistrer une opposition doivent parcourir les contacts
par pages de 25 (borne serveur maximale inchangée), avec nom/rôle/état et sélection
stable. Un champ de recherche ne doit pas filtrer seulement les éléments chargés :
la première livraison peut conserver une navigation Précédents/Suivants sans
recherche supplémentaire. Une cible retirée, devenue obsolète ou opposée suit les
refus du domaine ; aucune sélection de remplacement silencieuse.

Rattachement : choisir le type puis rechercher une référence lisible via
`GET /references-metier`, pagination existante. Présenter nom/type/état et
appartenance utiles, sans données hors des droits métier. Confirmer le lien
explicite ; afficher les références rattachées dans le dossier. Pour gagner,
choisir une référence **déjà rattachée** et éligible, puis confirmer la transition.
Un lien n’est pas une preuve de gain ; les ports métier et le domaine contrôlent
à nouveau état/appartenance/unicité dans la transaction.

Accès : diagnostiquer UX-15 avec le contexte et la requête exacte. 401 mène à la
reconnexion avec retour interne validé ; 403 indique le refus courant. Un refus
métier limité à une action ne signifie pas forcément session invalide. Ne garder
aucune donnée lorsque les droits de consultation sont effectivement retirés.
Le scénario de gain reste non validé sur TEST tant que l’interruption n’est pas
expliquée et la recette autorisée rejouée.

## L5 — Comprendre les traitements et leur prochaine étape

Import : en tête, nom du fichier/source et étapes « Analyse », « À vérifier »,
« Import », « Terminé ». Une étiquette secondaire conserve le statut serveur
exact traduit, notamment attente, arrêt, échec et résultat partiel. Ne pas mapper
un état d’erreur vers « Terminé » réussi. Compteurs traités/total et créations/
compléments/rejets seulement s’ils sont fournis par le serveur ; inconnu ≠ zéro.
UUID/empreinte/version de plan dans les détails techniques repliés.

Lecture automatique du statut seulement pour le lot visible non terminal :
intervalle initial 5 s, au plus une requête active, ralentissement jusqu’à 30 s
sur erreurs ; suspendre hors écran/onglet masqué et arrêter sur état terminal.
Dernière lecture datée et bouton Actualiser ; erreur explicite sans effacer le
résultat. Une absence de progrès ne prouve pas un batch désactivé : afficher
« En attente de traitement » selon l’état serveur et permettre de consulter le
diagnostic autorisé. La lecture ne confirme ni ne reprend l’import. Confirmation
du plan, décisions et idempotence des commandes restent inchangées.

Actualisation : afficher « X choix sur cette page ». « Appliquer les choix » et
« Appliquer et continuer » indiquent précisément la portée ; précédente et
suivante disponibles. Changement de page avec choix non appliqués : confirmation
explicite, pas de perte silencieuse. Après succès, liens vers les évaluations
créées/restant à confirmer ; accès au bon prospect/bloc et retour au lot.
La première version n’ajoute pas de filtre global « À examiner » tant que le
serveur ne le porte pas : ne pas simuler cette recherche sur la page seule.

Après attestation/adoption qui invalide la priorité : « Recalculer ce prospect »
prépare une capture avec `selection={mode:"IDS",ids:[id]}`, profil/objectif/règle
existants. Montrer **1 prospect** et confirmer avant le calcul ; ne pas réutiliser
silencieusement la recherche entière. Dans les bilans : nom du prospect, résultat,
motif traduit et action utile. Priorité commerciale calculée et priorité du dossier
NORMALE/HAUTE ont des libellés distincts. La priorité reste décidée par le domaine.

## L6 — Une lecture cartographique cohérente

Réutiliser les interactions accessibles de la carte générale pour la qualification,
avec un adaptateur de lecture qui préserve objectif/profil Commune ou EPCI, filtres
de niveau/validité, axe et viewport compatibles. Cela n’autorise pas à comparer des
profils non calibrés ni à colorer toutes les communes avec le niveau d’un siège EPCI.
La vue générale garde aussi l’axe Responsable et ses groupes mixtes.

Lors d’un changement de périmètre qui ne peut reprendre tous les filtres : afficher
ceux conservés et ceux non applicables, sans les supprimer discrètement ni
transformer le résultat vide en succès. Liste non localisée et secours sans fond
de carte conservés. Les contrôles d’accessibilité de l’audit sont transversaux.

## Propriétaires, contrats cibles et compatibilité

Le domaine `prospection` conserve opposition, transitions, preuves de gain et
qualification ; le domaine de l’agenda décrit dans `rendez-vous.md` conserve
disponibilité/validation/concurrence. Identité interne porte droits et révocation.
Application : orchestration et projections ; API/worker : adaptateurs ; UI :
présentation et navigation. **Aucune règle d’éligibilité ni calcul de priorité dans
le JavaScript.** Les mêmes refus doivent rester vrais via API directe et batch.

| Producteur → consommateur | Delta à réaliser avec le lot | Bornes, droits et compatibilité |
| --- | --- | --- |
| Lectures tâches/dossiers/événements → listes CRM et fiche | Ajouter des résumés de présentation typés : prospect `{id,nom,commune}`, responsable `{id,nom_affiche}` nullable, prochaine action `{id,type,date_action,route_interne}` nullable ; noms d’auteurs/références dans historique | Ajouter sans retirer les IDs/champs actuels ; aucune note/coordonnée dans une ligne qui n’en a pas besoin. Chargement groupé sur la page, sans requête par ligne. Ne pas déduire le responsable du prospect de celui du dossier. |
| Lecture quotidienne → Aujourd’hui | Étendre la lecture avec portée explicite `MOI|EQUIPE`, responsable courant résolu côté serveur pour MOI, date de référence Paris et groupes retard/jour/à venir avec pages et compteurs de même portée | Pagination de chaque groupe (25, maximum 100), pas de tableau exhaustif. Identité système sans utilisateur : MOI refusé explicitement, UI ouvre EQUIPE. Les droits restent ceux du CRM ; aucune audience supplémentaire. À formaliser dans l’OpenAPI avant implémentation du producteur. |
| Contacts → sélecteurs tâche/opposition | Consommer `next_cursor/has_more` existants, 25 par page ; pas de nouveau champ obligatoire ni recherche locale trompeuse | Contrôle de la cible à la mutation, sélection explicite. Aucun endpoint de recherche nouveau nécessaire à L4. |
| Références métier/rattachements → dossier | Réutiliser recherche paginée et lecture d’éligibilité ; compléter les résumés lisibles par projection autorisée si absents | Autorisation métier relue, pas de détail d’objet interdit. Gain recontrôlé atomiquement ; le libellé UI ne fait pas foi. |
| Agenda/disponibilités → création/report | Réutiliser les commandes ; ajouter aux deux lectures de disponibilités le contexte facultatif `rendez_vous_id` autorisé pour exclure la seule occupation reportée, curseur lié à ce contexte | Sans contexte : comportement de création conservé. Aucun nouveau statut ni conversion de tâche ; version/idempotence, heure Paris, collisions et anciennes intentions de rappel conservées. |
| Import/actualisation/calcul → progression et suite | Réutiliser états/compteurs/versions. Compléter la projection de résultat par liens bornés vers les évaluations produites si nécessaire ; calcul IDS=1 déjà supporté | Progression GET bornée, pas de mutation automatique, résultat partiel explicite ; reprise et droits du worker inchangés. Erreur de transport ≠ échec métier. |
| API cartes générale et qualification → composant partagé | Adapter leurs projections sans supprimer la sémantique profil/objectif et sans télécharger toutes les fiches | Conserver bornes/agrégations/pagination de leurs contrats ; non-localisés accessibles ; fonds de carte ne reçoivent aucune note/coordonnée. |

Ces deltas sont la **cible documentaire**, pas une description de l’API déployée.
Les DTO et l’[OpenAPI canonique](openapi.json) doivent être alignés avec les
projections retenues avant livraison de chaque lot ; le schéma exécutable actuel
n’est pas modifié dans cet audit. Déployer producteur et ressources CRM ensemble ;
champs ajoutés optionnels pendant coexistence, valeurs absentes rendues « Non
renseigné » et jamais zéro. Un refus de session ou de consultation effectivement
constaté retire les résultats privés. Une panne technique de relecture conserve
seulement le dernier état déjà autorisé en mémoire, daté comme ancien ; elle ne
simule pas une donnée fraîche et ne permet pas de poursuivre automatiquement
une mutation. Reprise toujours soumise aux contrôles serveur courants.

## Impacts, données et preuves de livraison

| Périmètre | Traitement prévu et justification |
| --- | --- |
| Backend/PWA CRM | Seul dépôt applicatif directement touché ; modules existants à faire évoluer, contrats de lecture et tests API/PWA associés. Pas de nouveau service. |
| ERP / OnBoard / souscriptions / commandes | Identités et lectures de preuves consommées ; vérifier refus/éligibilité des ports. Aucun changement de droits ni d’écran métier ERP demandé. |
| Animation / Marketplace / Pro | Sans modification directe : aucune API publique, aucun parcours de leurs utilisateurs changé. Ne pas propager une refonte CRM dans ces applications. |
| Schéma et données existantes | Pas de nouveau stockage métier requis pour navigation/assistances ; aucune migration prévue. Éventuel index de projection seulement sur plan mesuré, à tracer alors ; aucun retour arrière sur v311/v312, pas de recalcul/import automatique. |
| Batchs et notifications | Règles conservées ; la progression UI ne déclenche aucun job. Les tests de report doivent vérifier invalidation des anciennes intentions ; aucun nouvel e-mail/WebPush implicite. |
| Générateur et fixtures | Vérifier le générateur CRM existant avant changement ; enrichir au besoin ses scénarios synthétiques : titres homonymes, deux responsables, contact n°26, 60 RDV/propositions, preuves autorisées/interdites. Aucun nouveau champ obligatoire prévu ; génération réelle non demandée. |
| Guides et exploitation | Guide quotidien, retour/recherche, report, gain, suivi d’import et interprétation des priorités à réviser avec chaque lot ; diagnostic accès/attente explicite ; version PWA et bundle documentaire contrôlés. |
| Capacité | Projections groupées sans N+1, pagination 25/max100, lectures indépendantes sans hydratation complète ; mesurer N/10N et polling selon les budgets canoniques, aucune performance affirmée à partir de cet audit. |
| Mesure de productivité | Protocole avant/après dans l’audit ; pas de télémétrie persistante nouvelle ni de données personnelles copiées dans les rapports. |

Tests prévus : domaine/application pour gain, opposition, report et idempotence ;
contrat/projection pour scopes/compteurs, pagination et droits ; navigateur avec
API synthétiques pour les parcours. Réutiliser les harnesses CRM existants et
les compléter là où la nouvelle attente diffère, sans affaiblir leurs assertions.
Les contrôles d’architecture s’appliquent si les couches/ports changent ; docs et
sources exportées à contrôler à chaque lot. Aucun test métier exécuté ici.

La conception ne dépend d’aucun nouvel arbitrage métier. Restent avant déclaration
de livraison : formalisation et tests des DTO additifs, diagnostic UX-15, recette
avec compte commercial nominatif, jeux denses, clavier et appareil physique.
La mise en œuvre d’un lot indépendant peut avancer sans masquer ces réserves.
