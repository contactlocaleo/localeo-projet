# E73 — Productivité quotidienne de l’organisateur

## Statut et périmètre

**E73-EVO-ANIMATION-PRODUCTIVITE — 12 novembre 2026. Sept lots implémentés ; validation AP-22 partielle.**
Source : [audit UX](../../audits/animation/localeo-animation-ux-productivite-2026-11-12.md),
[backlog E73](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#évolution-du-12-novembre-2026--productivité-de-lorganisateur)
et [roadmap](../../roadmap/README.md). La clôture historique des 63 CA reste
inchangée. Les critères **AP-01 à AP-22** ci-dessous sont ajoutés, sans renuméroter
les critères antérieurs. Le bilan ci-dessous distingue code livré, preuves et réserves.

Applications affectées : **Animation** et **Backend** pour
les projections de lecture. Projet porte les sources canoniques. ERP, Live et
Pro ne changent pas de parcours ; vérifier leurs consommateurs des contrats
partagés avant toute suppression. Aucun nouveau service ni nouveau statut métier.

Objectif : savoir quoi faire, retrouver un dossier, le traiter puis poursuivre
sans ressaisie, détour ou doute sur le résultat. Acteurs : responsable,
gestionnaire autorisé, lecteur pour la consultation. Périmètre courant conservé :
organisation, commune active, habilitations et moteurs supportés.

Hors périmètre : envoi réel pendant l’audit, synchronisation d’agenda, refonte
des prix/modules, changement de qualification, automatisation des remises,
clôture automatique déjà suivie dans E73-EVO-CLOTURE-AUTO, changement de marque.

Bases avant implémentation : Animation `89579eb`, Backend `fab8850`, Projet
`1476885`. OpenAPI régénéré par le lanceur officiel hors ligne et copié dans
Animation. La migration TEST est vérifiée ; le déploiement applicatif après
push et la recette sur téléphone physique restent distincts des preuves locales.

## Existant, décisions et éléments préservés

Les constats A01–A13 de l’audit distinguent interface et code. Les corrections
de garde, d’accessibilité, d’état de chargement et de cohérence d’action appliquent
des attentes déjà présentes dans
[les parcours SaaS §5](perimetres-parcours-saas.md). La restauration complète des
listes, la file sélective, la simplification du wizard, la recherche spécialisée
et la reprise des dossiers constituent les évolutions explicitées ici.

Conserver : quatre espaces Préparer/Piloter/Communiquer/Résultats, menu mobile,
commune visible, référence visuelle Pro, liens directs/retours sûrs, détails de
participation à la demande, création distincte de publication, destinataires
autorisés, aperçu/confirmation, idempotence, reçu et réconciliation. Conserver
les règles de fin et d’archives ainsi que le masquage actuel des coordonnées.

Les choix de conception ci-dessous traduisent les recommandations de l’audit
et la demande d’implémentation, sans nouvel arbitrage métier implicite.
Les lots ne nécessitent pas de nouvelle décision métier pour protéger une saisie,
rendre les actions accessibles ou conserver un filtre. Aucune interdiction de
clôture anticipée et aucune nouvelle règle de consentement ne sont introduites.

## Lots, dépendances et critères d’acceptation

Les critères ci-dessous restent la cible d’acceptation. Les preuves réellement
exécutées et leurs limites sont reliées par lot dans la matrice finale ; l’audit
et une validation documentaire ne remplacent pas ces tests.

| Lot | Périmètre / critères | Dépendances | Taille indicative |
| --- | --- | --- | --- |
| L1 | Décider depuis un accueil fiable : AP-01, AP-02, AP-07 | Projection serveur avant branchement UI | M/L |
| L2 | Protéger la saisie et retrouver son contexte : AP-03 à AP-06 | Indépendant de L1 ; socle des retours suivants | M |
| L3 | Chercher et paginer sans collecte exhaustive : AP-08 à AP-10, AP-15 | Contrats Backend puis Animation ; réutilise L2 | L |
| L4 | Accès clavier et mobile : AP-11, AP-12 | Indépendant ; composants utilisés par L5/L6 | M |
| L5 | Préparer, inviter et corriger efficacement : AP-13, AP-14, AP-16, AP-17 | L2/L4 ; L3 pour la liste de corrections bornée | M |
| L6 | Enchaîner les gains et terminer une édition : AP-18 à AP-20 | L2/L4 ; extensions de lecture de fin avant UI | M/L |
| L7 | Comparer et mesurer : AP-21, AP-22 | AP-21 autonome ; référence AP-22 avant travaux, mesures après chaque lot | M |

Les sept lots sont implémentés. L7 conserve une réserve de vérification AP-22 :
les outils et mesures locales existent, mais ne constituent ni une étude
utilisateur ni un banc HTTP complet à charge mixte. La note de reprise locale
consigne les preuves et ressources ; le présent document reste canonique.

### L1 — Accueil et prochaine action

| ID | Déclencheur, résultat observable et refus |
| --- | --- |
| AP-01 | À faits et droits identiques, dashboard, liste, fiche et workflow affichent la même recommandation, le même motif et la même destination issus du serveur. Avant fin effective, une animation publiée/en cours sans tâche propose **Consulter le suivi** ; cela rejoint la rubrique Live existante. Après fin effective, la recommandation de clôture est possible selon les faits courants. La recommandation ne déclenche aucune transition. Sans projection valide, afficher **Ouvrir l’animation**, pas un calcul local de remplacement. |
| AP-02 | L’accueil distingue **À traiter** des **Animations en cours et à venir**. La première section ne contient que les animations ayant une intervention recommandée et autorisée : préparation/publication requise, clôture arrivée à échéance, tirage requis et disponible, dossier de fin à résoudre ou fin prête. Ni consultation seule, ni animation archivée, ni action interdite. Une animation terminée consultable n’est pas une urgence d’archivage. Motif visible, ordre et pagination définis au contrat. Si rien n’est à traiter, afficher **Aucune action en attente** et conserver l’accès au suivi. |
| AP-07 | Sur contexte, abonnement, modèles, dashboard et fiches, distinguer chargement, données confirmées vides, refus et erreur. Réessayer ne relit que le bloc concerné, garde filtres/saisie et n’exécute aucune commande. Abonnement non lu reste **Statut indisponible**, jamais **Inactif** par défaut. Erreur de catalogue propose une reprise, pas **Aucun modèle actif**. Pendant chargement initial, emplacement stable et annonce accessible ; pendant relecture, données explicitement en cours d’actualisation, commandes dépendantes désactivées. |

### L2 — Continuité et saisies

| ID | Déclencheur, résultat observable et refus |
| --- | --- |
| AP-03 | Une saisie modifiée dans création/configuration ou un parcours protégé déclenche la même garde lors de menu, onglet, retour interne, Retour/Avancer navigateur, changement de commune/organisation. **Continuer la saisie** conserve URL, contexte, valeurs et focus ; **Quitter sans enregistrer** réalise la navigation demandée. Une fermeture/recharge utilise la protection navigateur disponible sans promettre une récupération après crash. Un formulaire intact n’ajoute pas de confirmation. |
| AP-04 | Accepter un changement de périmètre annule/invalide les réponses anciennes et purge les listes/détails/caches du périmètre quitté ; aucun brouillon n’est transféré automatiquement. Une commande en cours ou incertaine garde les restrictions et le reçu du parcours existant. Une réponse ancienne ne rétablit ni ancien tenant ni droits révoqués. Ne pas persister messages/coordonnées/brouillons en stockage navigateur pour résoudre la continuité. |
| AP-05 | Liste Animations/Archives → fiche → **Retour aux animations/archives** restitue filtres appliqués, page, position et focus sur l’élément ouvert. Lien direct sans parent : liste sûre de la commune courante. Si l’élément disparaît ou le curseur expire, garder les filtres, revenir à une page valide et annoncer **La liste a changé, résultats actualisés**. Les retours externes fournis dans l’URL sont refusés. |
| AP-06 | Historique Communication → campagne → retour conserve champs de filtre, filtres réellement appliqués et page ; aucune liste filtrée avec champs affichés Tous/vides. **Effacer les filtres** est explicite. Un éventuel formulaire de filtres en préparation se distingue des filtres appliqués. Ouvrir, filtrer ou revenir n’envoie/programme rien. |

### L3 — Lectures et recherche

| ID | Déclencheur, résultat observable et refus |
| --- | --- |
| AP-08 | La liste Animations charge une page bornée de 25, maximum 100, avec recherche, période, modèle, statut/phase et alerte appliqués avant pagination au serveur. Aucun `listAll/collectPages` interactif. Actions **Précédent/Suivant** utilisables au clavier et sur mobile ; filtre changé = première page. Les archives restent séparées. Un total non fourni n’est pas remplacé par le nombre de lignes de la page. |
| AP-09 | Sélection et suppression de brouillons portent uniquement sur les éléments explicitement sélectionnés. **Sélectionner les brouillons de cette page** n’inclut pas les pages non lues. Confirmation indique nombre et objets concernés ; rien de publié sélectionnable comme brouillon. Changer de filtre annonce l’effacement de la sélection. Maximum 100 éléments par opération UI ; aucune collecte implicite de toutes les pages. Les contrôles serveur de suppression existants restent obligatoires. |
| AP-10 | Participants et Validations ont la même recherche/pagination depuis le menu global ou une fiche, avec animation fixée dans la fiche. Réutiliser les lectures globales bornées pour les moteurs compatibles ; la tombola publique garde son lecteur autorisé. Résumé, définition des compteurs et date d’observation visibles ; ne pas comparer comme égaux des KPI ayant des périmètres différents. Réponse tardive d’un filtre ou tenant précédent ignorée. |
| AP-15 | Dans une tombola publique, rechercher par préfixe d’e-mail déjà autorisé ou par référence complète de participation, sans télécharger les autres pages. Aide visible **E-mail (début de l’adresse) ou référence complète**. La recherche active n’est pas supprimée silencieusement en changeant de moteur : la nouvelle vue la reprend si compatible, sinon explique et demande de la reformuler. Les compteurs restent libellés **Toute l’animation** ; le total de résultats filtrés, s’il est demandé, appartient à la pagination. |

### L4 — Accessibilité et lecture mobile

| ID | Déclencheur, résultat observable et refus |
| --- | --- |
| AP-11 | Chaque animation de la table bureau possède un lien nommé ou bouton d’ouverture indépendant de la suppression ; Tab/Entrée permettent de l’ouvrir. Champs et erreurs du wizard sont associés aux libellés. Création/annulation/suppression participants utilisent la primitive `ManagementDialog` : nom, focus initial, cycle contenu, fermeture autorisée et retour au déclencheur. Aucune suppression de confirmation sensible pour réduire le nombre de clics. |
| AP-12 | À 320 et 390 px, puis texte agrandi à 200 %, l’action recommandée de la carte est visible sans ouvrir **Voir les détails** ; couleur et icône sont accompagnées de texte. Le cadre mobile privilégie deux rangées quand la largeur le permet, garde commune/compte/notifications accessibles et laisse le contenu défiler. Aucune cible principale inférieure à 44 × 44 px, aucun focus masqué par les barres fixes ni défilement horizontal de toute la page. La progression du message devient compacte, l’aide reste dépliable ; ouverture de formulaire place le focus sur son titre puis les champs. Vérifier les contrastes existants selon §5.2, pas une simple impression visuelle. |

### L5 — Préparation et opérations courantes

| ID | Déclencheur, résultat observable et refus |
| --- | --- |
| AP-13 | Depuis une carte Modèles, le modèle choisi est confirmé dans un résumé modifiable et le parcours manuel arrive aux informations à saisir. La commune active est visible avant saisie et dans la confirmation finale ; supprimer son étape purement informative. Depuis Nouvelle animation sans modèle, conserver son choix. Si le modèle devient indisponible, expliquer le refus et préserver les champs compatibles sans créer. Les parcours Chasse/Léo et capacités moteur restent distincts. |
| AP-14 | Fin antérieure au début est signalée près de la date avant Continuer. Les autres préconditions locales de saisie expliquent ce qui manque ; le serveur garde les règles métier et ses refus sont rattachés au champ/étape approprié. Après erreur, valeurs conservées. Étape courante compacte, informations secondaires repliables, aucune condition légale/conséquence indispensable cachée. Même principe de progression appliqué au formulaire Communication, sans modifier ses quatre décisions et ses confirmations. |
| AP-16 | Examiner une correction ouvre un détail adjacent ou panneau nommé/focalisé ; avec une liste longue, le titre et les conséquences sont immédiatement atteignables sans traverser les autres lignes. Annuler revient au déclencheur en gardant filtre/page. Aucun POST de décision à l’ouverture ; motif, version, gel, confirmation et reçu restent ceux du serveur. |
| AP-17 | Invitations : **Envoyer la sélection (n)** est désactivé à zéro ; **Sélectionner cette page** explicite, maximum 100. Un changement de filtre/page purge la sélection et l’annonce ; zéro ne signifie jamais Tous. Sélection A → autre filtre → retour ne peut envoyer A+B sans sélection de B. Les invitations déjà non envoyables restent refusées au serveur, y compris après une course ; aucun contournement de délai de relance ou de configuration versionnée. |

### L6 — Gains et fin d’animation

| ID | Déclencheur, résultat observable et refus |
| --- | --- |
| AP-18 | Après résultat confirmé d’un contact/remise dans un gain de page 3, le retour conserve le filtre et la page de travail avec repère stable, ou explique son repositionnement si la population a changé. **Précédent** est disponible pour les pages déjà visitées. Réconciliation de reçu inconnue ne relance pas la commande ; refus/révocation purge les coordonnées et commandes devenues interdites. |
| AP-19 | Fin et archivage propose **À résoudre / Tous les dossiers**, filtre serveur qui inclut dossiers attribués non résolus et dossier agrégé sans gagnant encore à justifier. Le résumé distingue **Dossiers attribués à résoudre**, **Unités sans gagnant à justifier**, **Opérations en cours** ; aucune somme mélangeant dossiers et unités. Le filtre ne change pas les compteurs globaux ni les conditions de Terminer. Après une décision, relecture et reprise au même point, sans réinitialisation systématique en page 1. |
| AP-20 | Un gain disposant d’un dossier de fin peut ouvrir **Traiter le dossier de fin** sans parcourir les pages : référence fournie par le serveur, lecture ciblée autorisée. Dossier absent/inaccessible expliqué, aucune référence construite côté client. Les décisions exigent toujours versions animation/dossier, confirmation, motif et idempotence ; conflit → rafraîchir puis reconfirmer. Fin/archivage séparés, animation terminale en lecture seule ; aucun effet de remise déduit d’un e-mail ou d’un coffret envoyé. |

### L7 — Comparaison et mesure

| ID | Déclencheur, résultat observable et refus |
| --- | --- |
| AP-21 | Le comparateur présente titre, période, commune et moteur de chaque édition ; réutilise filtres serveur période/modèle et page de 25. Changer de page de candidats garde le choix explicite déjà sélectionné. La réponse serveur décide de la comparabilité et explique son refus ; le client ne fabrique pas d’écarts entre moteurs incompatibles. |
| AP-22 | Les scénarios de l’audit disposent d’une référence avant changement, puis de mesures après chaque lot : réussite sans aide/tentatives, temps médian/p90, retours correctement restaurés/retours contextualisés, erreurs et résultats incertains. N/10N, 25/100 lignes, concurrence et mémoire sont mesurés sur base isolée selon les budgets ci-dessous. Aucun succès fonctionnel ou performance n’est déclaré sur la seule base d’un build ou d’une présence de composant. |

## Responsabilités et invariants

| Règle / propriétaire | Entrées concernées et preuve future |
| --- | --- |
| `Animation` et services purs du domaine `animation_locale` : état, période effective, possibilité de clôture/tirage/fin | API, ERP, batch existants continuent à utiliser les mêmes transitions. La recommandation commune reçoit faits de période/workflow/opérations et capacités déjà autorisées, sans ORM/HTTP ni nouvelle mutation. Test à horloge fixée avant/à/après fin et pour chaque état terminal. |
| `CampagneOrganisateur` : aperçu, audience, version, programmation et transitions | UI et API existantes ; confirmation unique, résultat inconnu puis reçu, zéro second envoi automatique. Une publication Live n’est ni une réception Push ni une lecture. |
| Domaine Fin : chaque gain traité et unités sans gagnant justifiées avant Terminer | Domaines/service de fin existants ; filtre ou accès ciblé n’altère jamais les compteurs de décision. Tests deux décisions concurrentes, justification périmée, remise/refus, révocation d’un bon atomique. |
| Identité/accès et application : organisation, commune, rôle, capacité et droits acquis | Contrôles avant lecture et mutation ; compteurs, références et curseurs n’accordent pas de droit. Test accès direct étranger, révocation pendant requête et changement de commune. |
| Adaptateurs de lecture : page autorisée, projection et bornes | SQL filtre droits et périmètre avant LIMIT ; enrichit une page sans N+1. Pas d’invariant métier dans la vue, le repository ou le composant. |
| Interface : contexte, saisie, sélection, focus | État éphémère borné et segmenté ; garder un filtre n’autorise pas à conserver une donnée refusée. Aucun changement de modèle ou de filtre ne constitue une commande métier. |

Les règles de recommandation jusque-là réparties entre application backend et
frontend rejoignent une politique pure du domaine ; l’application charge les
faits et applique les autorisations, puis un présentateur construit les libellés
et destinations à partir des codes. API/ERP/batch ne se mettent pas à décider
une transition à partir d’un libellé. Référence :
[ADR domaine d’abord](../../architecture/decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md).

## Contrats et compatibilité

Chaîne : producteur Backend → `scripts/documentation/generate_epic41_openapi.py`
→ [OpenAPI canonique E41](../epic-41-api/openapi.json) →
`localeo-animation/src/imports/openapi.json` et ses clients typés.
Les extensions ci-dessous sont **cibles**, pas des routes déjà livrées. Ne pas
éditer les JSON pour faire croire à leur présence avant implémentation du producteur.

### Recommandation et dashboard

Ajouter une projection commune `recommandation` aux résumés animation, au détail
et au workflow : `code`, `libelle`, `motif`, `destination` (rubrique interne parmi
les destinations autorisées), `disponible`, `a_traiter`, `observe_le`. Champ nullable
si aucune recommandation ; motif absent pour la consultation ordinaire. Les
permissions exposées dans `exploitation.allowedActions` gardent leur sémantique.

La politique applique les préconditions existantes dans cet ordre : préparation
avant publication ; action de tirage/fin fondée sur les blocages réels après
clôture ; clôture recommandée à échéance si disponible ; sinon suivi. Les faits
de tirage déjà lancé/terminé et opération active empêchent de recommander un
second lancement. Les règles spécifiques moteur restent propriétaires de leurs
préconditions. Un responsable autorisé à clôturer avant terme conserve son action
secondaire ; un lecteur n’acquiert jamais cette commande.

Étendre `dashboard-performance` avec un mode explicite `mode_lecture=borne`,
demandé par le nouveau client, `actions_limit` (25, max100) et `actions_cursor`.
Dans ce mode, la réponse **omet `animations_a_action` et ne calcule/hydrate pas
sa collection exhaustive** ; `actions_a_traiter` porte
`items/nextCursor/hasMore/observedAt`. Le schéma distingue ce mode du mode
historique par le discriminateur `mode_lecture` ajouté au mode borné. Sans
opt-in, la réponse historique reste inchangée pour les lecteurs non migrés ;
elle n’est pas incluse dans les preuves de coût du nouveau parcours.

La file applique les mêmes filtres explicites date/modèle/statut/animation que
le dashboard ; la période choisie détermine l’intervalle, avec la sémantique de
chevauchement des animations. Pour une période relative (7/30 jours…), figer les
bornes absolues lors de la première lecture et les porter dans le curseur signé
pour les pages suivantes ; seul un rafraîchissement explicite recalcule la période.
Le titre annonce cette restriction pour ne pas
présenter « Aucune action en attente » comme un constat hors des filtres actifs.
Ordre : fin effective croissante, valeurs absentes en dernier, puis ID croissant.
Curseur signé lié à l’acteur/périmètre autorisé, filtres résolus, tri, limite et
version ; expiration 30 minutes, 422 en cas de curseur invalide/expiré, 403 pour
un accès refusé. Droits relus à chaque page. Une fin effective pouvant changer,
la navigation est vivante : un report peut déplacer une ligne ; rafraîchissement
explicite réinitialise la page avec annonce, sans promettre un instantané.

`a_traiter` et les droits sont appliqués **avant LIMIT** sur une projection
interrogeable : faits persistés/versionnés du workflow et prédicats temporels
indexables, puis enrichissement de la seule page. Le repository n’invente pas
la règle : les codes de recommandation/hors date proviennent de la politique de
domaine ; les lectures utilisent directement les faits persistés par les transitions.
L’implémentation compile la politique déclarative du domaine vers les expressions
SQL ; elle n’ajoute pas de table de projection ni de reconstruction asynchrone.
L’échéance temporelle est un prédicat sur la période effective, sans nouveau job.
Si une projection additionnelle est nécessaire, prévoir sa migration et sa
reconstruction par lots avant activation ; aucun scan/hydratation de toutes les
animations dans la requête HTTP pour calculer puis filtrer `a_traiter`.
Chaque carte explique son motif, sans score opaque d’urgence. Le suivi des
animations emprunte la lecture paginée ci-dessous. Retirer l’usage historique
après inventaire ; ne pas faire deux appels par animation.
Le dashboard borné conserve les 50 dernières alertes non lues autorisées
dans le périmètre, avec une indication visible de cette limite. Le droit de
consultation seul ne crée pas de tâche. Un tirage initial bloqué propose
**Reprendre le tirage** seulement au gestionnaire autorisé, sans second lancement.
Les KPI gardent leurs définitions documentées et affichent le périmètre/période,
sans exiger leur égalité avec les lectures globales à définition différente.

### Listes Animations, participants et validations

La route historique `/protected/animation-locale/animations` a `page/page_size`,
un total et `next_cursor:null` ; son ordre est `created_at DESC,id ASC`. Elle
supporte recherche par sous-chaîne du nom, statut, modèle, moteurs, archives et
chevauchement des périodes, mais pas le filtre d’alertes. Ne pas changer
silencieusement ce contrat pour les consommateurs existants.

Pour supprimer collecte exhaustive et offsets profonds, ajouter la famille
`GET /protected/animation-locale/lectures-globales/animations`, selon le protocole
déjà utilisé pour participants/validations. Cette lecture réutilise les prédicats
existants et ajoute explicitement le filtre d’alerte/phase ; elle ne crée pas un
second domaine Animation. Paramètres : `limit`, `cursor`, `recherche` (nom,
sous-chaîne insensible à la casse, 120 caractères max), `statut`, `modele_code`,
`moteurs_supportes`, `date_debut`, `date_fin`, `archives`, `avec_alertes`,
`phase_workflow`, `suivi_actif` (uniquement PUBLIEE/EN_COURS, avant pagination).
Les dates explicites priment sur une période relative, même si une seule borne
est fournie. Dates = chevauchement de la période effective, pas date de
création. Statut/phase inconnus ou intervalle inversé : 422. Reprendre la liste
des phases du workflow existant dans le schéma généré ; pas de phase inventée
depuis la couleur UI.

Réponse : `items` de résumé autorisé avec recommandation, `nextCursor`, `hasMore`,
`observedAt`. Pas de total exhaustif obligatoire ; afficher « 25 résultats
affichés » si aucun total filtré daté n’est fourni. Curseur signé par clé
`created_at DESC,id ASC`, lié au tenant, commune, filtres, tri et version du
contrat ; durée 30 minutes, erreur 422 explicitement distinguée d’un refus 403.
Pas de snapshot inter-pages garanti. L’ancienne route reste inchangée ; le
frontend migre cette liste et ses archives, sans bascule cachée vers `listAll`.

Participants non publics et validations réutilisent
`/lectures-globales/participants` et `/lectures-globales/validations` avec
`animation_id` dans la fiche. Recherche préfixe existante, `qualifie/termine` ou
`statut`, `synthese/allowedActions/actualisation/observedAt` conservés. La lecture
globale peut inclure des archives ; le dashboard les exclut : préciser les
périmètres, ne pas modifier leur sens pour aligner artificiellement les chiffres.

Pour la tombola publique, étendre `GET /animations/{id}/participants-page` par
`recherche` (120 caractères max) : préfixe d’e-mail insensible à la casse ou
référence exacte `ParticipantAnimation.reference` (pas `participant_id` ni
`inscription_id`), sans recherche sur téléphone/nom non prévue. Ajouter au DTO
de cette page `reference_participation`, issue de ce champ existant, et la
présenter dans le détail de participation et les informations secondaires de
la ligne ; aucune référence à générer lors de la lecture. L’utilisateur peut
ainsi la copier depuis ce détail ou la retrouver si elle lui est communiquée.
Le prédicat cherche l’égalité de la référence après normalisation canonique
ou le préfixe d’e-mail en minuscules après retrait des espaces externes ; `%`
et `_` sont traités comme caractères littéraux, pas comme jokers. Filtre SQL et
curseur signé incluent la recherche normalisée ; expiration existante 30 minutes
et borne haute date/ID conservées. Limite 25/max100, états EN_ATTENTE/QUALIFIE/
GAGNANT inchangés ; gagnants toujours inclus dans qualifiés. Les compteurs de
`participants-compteurs` restent globaux et datés ; `avec_total` sur la page
détermine seulement le total filtré. L’ajout de référence ne dévoile ni coordonnée supplémentaire,
ni identifiant d’accès habitant, ni PIN/QR/token ; couvrir absence et non-fuite
par les tests de contrat.

### Fin, gains, communication et résultats

Étendre `GET /animations/{id}/etat-fin` avec `a_traiter` booléen par défaut false,
lié au curseur. Le prédicat réutilise les faits de domaine : dossiers attribués
non résolus ou dossier agrégé avec unités non justifiées. Compteurs/blocages
restent globaux. Exposer `unites_non_justifiees` déjà calculé par le domaine,
sans remplacer `nombre_unites_sans_gagnant` ; ne pas additionner dossiers et unités.

Ajouter `GET /animations/{id}/dossiers-fin/{ref}` : DTO de dossier existant et
version animation courante, même autorisation que `etat-fin`, 404 si absent du
périmètre autorisé, 403 si capacité refusée. Les lectures existantes
`/animations/{id}/gains` (Coffrets), `/animations/{id}/gains-libres` (attributions
libres externes/numériques) et `/animations/{id}/bons-lots` (vue des bons)
fournissent `dossier_fin_ref` nullable et opaque. Le serveur associe uniquement
l’attribution courante confirmée à son dossier ; un supplément/remplacement
sans dossier propre, une attribution non confirmée ou un bon non attribué porte
`null`, sans fabriquer de dossier. Une vue de bon déjà associé à une attribution
renvoie la même référence que celle du gain, pas un second dossier. Dossier
résolu ou animation terminale : consultation possible selon les droits, actions
exactement celles du serveur, aucune invitation à retraiter une remise acquise.
Ne pas reconstruire la référence ni hydrater tous les dossiers pour ce lien.
Les POST décision/terminer/archiver et reçus restent inchangés. Corriger lors de
la génération la documentation de leur 404 de reçu, déjà produit mais absent
de l’OpenAPI lu ; un reçu introuvable ne signifie pas succès ni rejeu autorisé.

Aucun endpoint supplémentaire pour Communication : liste, rapport, aperçu,
envoyer/programmer et `GET commandes/{cle}` existent. Préserver 200 confirmé,
202 en cours, reçu introuvable et distinction publication/transport. Après
opération acceptée, réutiliser le suivi existant ; pas de seconde commande
« Démarrer ». Le comparateur réutilise filtres période/modèle et mesures du
contrat de résultats ; aucune recherche plein texte nouvelle n’est promise.

### Reprise, cache et versions

L2 stocke le contexte de consultation en mémoire de session d’application, clé
organisation/commune/acteur/vue/filtres, maximum 20 vues et 20 curseurs par vue.
Ne conserver que les paramètres et repères, pas un historique de coordonnées.
Chaque retour relit la page autorisée ; rechargement complet peut réinitialiser
le repère avec filtres sûrs présents dans l’URL, sans promesse de brouillon durable.
Pour les recherches de personnes, rester en mémoire, pas dans l’URL/journal.
Maximum 100 lignes rendues par liste ; ancienne réponse annulée/ignorée, une
requête active par liste, temporisation de recherche 300 ms.

Après mutation confirmée, relire la page et les compteurs touchés ; si un filtre
« À résoudre » fait disparaître le dossier, garder le prochain repère de la page.
Si elle devient vide, revenir à la dernière page visitée encore valide. Curseur
expiré/invalide : reprise première page avec message et filtres conservés.
Navigation vivante, sans promesse d’exhaustivité ; export conserve son mécanisme
spécifique. Une commande incertaine n’entraîne ni mutation optimiste définitive
ni nouvelle clé d’idempotence automatique.

Livrer les extensions de lecture Backend et les contrats avant le frontend
consommateur. L’absence de projection nouvelle affiche un état explicite ou le
lien neutre, jamais une règle client concurrente. Retrait des lectures historiques
seulement après inventaire des consommateurs ; aucune compatibilité implicite
avec une ancienne version de la clôture automatique.

## Performance, données et migrations

Cibles de conception selon [P01–P08](../../architecture/transverse/performance-volumetrie.md),
**partiellement mesurées, limites au bilan**. Jeu isolé N=1 000 puis 10N=10 000 racines de la famille
consultée dans un tenant, croissance séparée des tenants étrangers et historiques.
Tester 25 puis 100 lignes et profondeur 1/20, cache froid/chaud ; charge mixte
de 10 opérateurs avec lectures et mutations synthétiques contrôlées.

| Famille | Accès et borne | Ressources / budget proposé et preuve |
| --- | --- | --- |
| Liste Animations et file à traiter | Tenant/commune/moteur/droits avant page ; tri par clé ; index composé aligné et index recherche adaptés après EXPLAIN | Une requête HTTP de page, au plus 100+1 racines et enrichissement groupé de cette page ; plafond initial 12 requêtes SQL avec contrôles d’accès inclus, indépendant de N et du nombre de lignes rendues. |
| Participants / validations / tombola | Lecteurs existants bornés ; recherche dans SQL, index de préfixe normalisé tenant/animation/e-mail et référence exacte | Une page, maximum 100+1 racines ; 12 SQL maximum proposés ; comparaison 25/100 détecte N+1 ; compteurs traités séparément, pas d’hydratation exhaustive. |
| Fin paginée / dossier ciblé | `a_traiter` avant LIMIT, même ordre de curseur ; lecture ciblée par animation/ref et liaison gain | 100+1 dossiers maximum ou un seul ciblé ; pas d’appel par dossier. Compteurs de décision cohérents et synchrones, leur coût d’agrégation est mesuré séparément. |
| Dashboard / agrégats | Ne plus charger tous les participants pour fabriquer une page ; agrégations SQL/projections groupées selon définition | Pas de budget constant mensonger pour les agrégats globaux : mesurer lignes scannées, EXPLAIN et temps séparés ; passer à une projection datée si le budget ne tient pas, sans dégrader les compteurs de décision. |
| Navigateur | Une page rendue, 20 contextes/20 curseurs par contexte ; pas d’enrichissement individuel des lignes | p95 API de lecture ≤ 1 s, p99 ≤ 2 s ; p95 première page utilisable ≤ 2 s dans le banc déclaré. Surcroît mémoire navigateur pour même page à 10N ≤ 20 % par rapport à N. Mesurer octets, DOM, erreurs techniques et saturation ; ne pas relever le seuil après échec. |

Ces budgets initiaux doivent être consignés avec matériel, index, versions,
trafic, p95/p99 et taux d’erreur avant activation ; une limite non mesurée reste
ouverte. Aucun stress test sur TEST partagé. L’authentification, les droits et
les invariants ne sont pas supprimés pour tenir un budget.

La migration **v313_animation_productivite.sql** ajoute `pg_trgm` si nécessaire
et quatre index : tenant/commune/date/ID des animations, nom en trigrammes,
préfixe e-mail des participants et référence exacte. Aucun statut, consentement,
contenu métier ou nouvelle table de projection. Elle a été appliquée sur TEST
le 12 novembre 2026 après sauvegarde complète ; version 313 et quatre index
vérifiés. Aucun nouveau batch, secret ni réglage fournisseur.
Les extensions Backend et leurs index précèdent le frontend consommateur.
Un retour au frontend précédent ne nécessite pas de suppression des index ;
les anciens lecteurs restent disponibles. Pas de génération de démonstration
sur TEST : jeux synthétiques isolés pour les tests.

Fixtures : deux communes/deux organisations, rôles responsable/gestionnaire/
lecteur, droits révoqués, animations de chaque état et moteur, grands historiques,
deux éditions homonymes, campagnes filtrables, gains au-delà de la page 2,
dossiers justifiés/non justifiés, curseurs expirés et réponse après changement
de tenant. Réutiliser les générateurs applicatifs ; scénarios synthétiques
isolés, aucun appel fournisseur. Pas de changement requis au schéma des données
de démonstration en première intention ; leur couverture doit être adaptée.

## Matrice de traçabilité et preuves d’implémentation

Les résultats détaillés, rapports de chaque tentative et limites figurent au
[bilan de livraison](verification-livraison.md#évolution--e73-evo-animation-productivite-12-novembre-2026).
Les scripts restent dans leurs dépôts applicatifs ; les sorties `tmp/` sont
locales et non versionnées. Les passes se recouvrent et ne sont pas additionnées.

| Lot / critères | Réalisation et preuves de comportement | Limite de preuve |
| --- | --- | --- |
| L1 — AP-01/02/07 | Politique `recommandation_animation`, compilation SQL avant LIMIT, dashboard borné et suivi distinct. Tests `test_recommandation_productivite`, `test_productivite_animation` domaine/service/API/PostgreSQL : horloge, droits, terminaux, tirage bloqué, alertes, filtres et curseurs. Navigateur App : états du contexte/abonnement et filtre de file. | Pas de certification du déploiement TEST par le push ; recette avec comptes réels à faire après livraison. |
| L2 — AP-03 à 06 | `JourneyNavigation`, protection des commandes via `PreparationNavigation`, contexte mémoire borné et historique Communication. Scripts `productivity-primitives`, `productivity-primitives-generation`, `productivity-workspace`, `productivity-operations` : menu, Retour/Avancer, saisie, page/focus, disparition de repère, commande incertaine. | Fermeture/rechargement natifs selon navigateur ; aucun brouillon durable promis. |
| L3 — AP-08/09/10/15 | Nouvelle lecture animations, recherche publique littérale, routes participants/validations réutilisées. Tests API/SQL et `pagination-contract` : une page, moteur public négocié, filtres avant LIMIT, cursors tenant/droits. Tests App : page25, retour, sélection explicite, erreur de curseur et filtres conservés. | Pas de total exhaustif inventé ; navigation vivante. Mesures de capacité séparées en AP-22. |
| L4 — AP-11/12 | Table avec action nommée, dialogues communs, focus initial/retour, champs associés et grille mobile. Primitives navigateur à 320/390/1440 et texte 200 %, contraste texte≥4,5/focus≥3 ; opérations/App à 320/1280. | Automatisation Chromium locale ; lecteur d’écran et téléphone physique non vérifiés. |
| L5 — AP-13/14/16/17 | Création sans étape commune informative, modèle conservé, dates invalides avant suite ; correction dans un dialogue focalisé ; invitations explicitement sélectionnées. Tests App/operations : refus/modèle indisponible, maintien des champs, ouverture sans POST, zéro sélection désactivé, filtre purgeant la sélection. | Fournisseurs simulés, aucun envoi réel sur TEST. |
| L6 — AP-18/19/20 | Reprise des gains, filtre fin avant LIMIT, unités sans gagnant distinctes, référence de dossier produite côté serveur et lecture ciblée. Tests domaine/API/PostgreSQL + navigateur : dossier absent/refus, version/conflit, curseur invalide distinct du conflit de mutation, retour contextualisé. | La lecture et le lien ne valent pas remise ; règles métier et réconciliation existantes conservées. |
| L7 — AP-21/22 | Comparateur avec période/commune/moteur ; choix conservé après pagination. Tests navigateur AP-21, microbanc PostgreSQL N/10N, métriques de première page et restauration. | **AP-22 partiel** : référence initiale qualitative seulement, pas de médiane/p90 humaine ni de p95 API HTTP complète avec charge mixte. Ne pas considérer les microbancs comme acceptation globale. |

Le générateur de démonstration n’a pas besoin de nouveau schéma : les champs de
lecture proviennent des données existantes. Les tests ajoutent localement les
grands historiques, organisations étrangères, rôles et dossiers nécessaires.
ERP, Marketplace/Live et Pro ne consomment pas les nouvelles routes ; anciens
contrats de mutation et lecteurs conservés, aucune adaptation de ces interfaces.

## Préparation, risques et recette après livraison

La réalisation et les tests locaux sont consignés au bilan. Les mesures de
capacité complète et la recette physique mobile/lecteur d’écran restent des
réserves explicites ; la clôture historique E73 ne les masque pas. Les index
sont appliqués, les contrats générés et les tests de rôle/concurrence exécutés.

Vérifier sur le bon service TEST et relever son SHA : prochain geste identique
sur trois vues, retour filtré, saisie protégée, absence de préchargement des autres
pages, recherche publique, aperçu de correction focalisé, invitation à zéro
désactivée, reprise de fin et comparaison identifiable. Utiliser des données
synthétiques et fournisseurs factices pour les commandes ; les tests de lecture
ne prouvent pas les écritures.

Le lot de clôture automatique peut modifier les faits temporels et le workflow :
intégrer sa projection s’il est livré avant L1, sans reproduire son ordonnanceur.
La recommandation restera fondée sur l’état courant, quelle que soit l’entrée
ayant clôturé. Aucun autre audit historique n’est réputé clôturé par ce document.
