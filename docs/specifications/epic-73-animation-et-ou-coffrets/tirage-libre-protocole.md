# E73 — Protocole du tirage libre préparé

Conception LOT04, écrite avant son implémentation. Le périmètre livré par ce lot est `LIBRE/EXTERNE`. La politique de tirage et de remplacement appartient au domaine `animation_locale` ; le SQL ci-dessous réalise ses garanties de persistance. Les futurs bons numériques ajouteront leurs gardes de commerce/exemplaire au scellement, sans réutiliser une simple déclaration externe comme preuve de consommation.

## Population et opération durables

La source est la population gelée existante, normalisée dans `animation_population_eligible_membres`, avec provenance `animation_gels_populations`. Il n'existe pas de tableau JSONB de participants à charger : l'index unique existant `(population_id, participant_id)` permet une lecture par clé.

Une opération initiale unique par animation conserve l'identifiant/version de population, le gel de configuration, la révision publiée de dotation, l'auteur et les positions des lots. Un compteur de membres est enregistré avec la population ; son initialisation historique est une migration, pas un `COUNT` à chaque consultation. Le POST vérifie l'autorité courante et les versions, enregistre l'opération et son reçu, puis retourne `202`. Une nouvelle clé HTTP ne crée pas un second tirage initial. La réponse perdue se traite par lecture du même état.

Le secret de préparation est créé une seule fois par un port cryptographique. Il n'est exposé ni dans les réponses ni dans les journaux. Il sert à produire les clés aléatoires privées des candidats de manière reproductible lors d'une reprise du même traitement.

## Préparation bornée

Chaque cycle repère une opération par une lecture `LIMIT 1`, puis verrouille identité, animation et opération dans cet ordre. Deux workers revérifient la phase et les curseurs sous ce verrou. Chaque phase traite au maximum 500 lignes dans une transaction courte ; le curseur et les lignes produites sont commités ensemble.

1. **Indexation** : `WHERE population_id = :population AND participant_id > :dernier ORDER BY participant_id LIMIT 500`. La première page omet la comparaison. Aucune participation vivante n'est triée aléatoirement. Chaque membre reçoit une clé pseudorandom de 256 bits via le port cryptographique, liée au secret privé, à son identifiant et au compteur de rejet. Les clés sont uniques dans l'opération ; une collision est résolue par un nouveau candidat de clé, jamais par un départage au nom ou à l'identifiant. La sélection par clés aléatoires distinctes n'introduit ainsi aucun biais de départage. Le compteur de rejet est conservé. Rejouer une transaction conserve les clés déjà persistées et reproduit les autres à partir de la même préparation.
2. **Classement** : `WHERE operation_id = :operation AND cle_aleatoire > :derniere ORDER BY cle_aleatoire LIMIT 500`, sur l'index unique `(operation_id, cle_aleatoire)`. Les rangs sont affectés par lots, sans `OFFSET`, sans `ORDER BY random()` et sans chargement de la permutation complète. La réserve contient tous les candidats au-delà du nombre de gagnants.
3. **Attributions privées** : les premiers `min(nombre_lots, nombre_eligibles)` rangs sont associés aux unités dans l'ordre publié. Les lignes sont parcourues par curseur `(animation_id, ordre, id)` ; l'opération conserve la ligne courante, son index d'unité, le curseur suivant et un tampon de 100 lignes au maximum. Aucun plafond commercial de lignes ou d'unités n'est imposé. Une tranche de 500 unités de lignes distinctes demande au plus cinq nouvelles pages de lignes, jamais une requête par gagnant. Attributions et intentions d'email restent privées. Le reste de la permutation demeure une réserve paginée, sans gain fictif.

Le travail total reste proportionnel à la population et aux attributions, avec une mémoire applicative bornée à 500 candidats et un tampon technique de 100 lignes de lot. La charge ne doit pas être cachée dans une requête HTTP. Une phase en erreur garde son opération et son curseur ; la reprise n'offre pas un nouveau résultat au gestionnaire.

## Visibilité atomique

L'opération porte `confirmed_at`, absent pendant toute la préparation. Les lectures de gains et de suppléants, la consultation personnelle, les remplacements et le worker d'email exigent une jointure avec une opération confirmée. Une attribution préparée ne constitue donc pas encore un gain officiel.

Le scellement verrouille l'animation puis l'opération, revérifie l'autorité actuelle, l'état clôturé, la population/provenance et la révision publiée de dotation. Il compare les compteurs de préparation aux compteurs attendus. Les contraintes d'unicité protègent participant gagnant historique et unité courante. Le marqueur est écrit dans la même transaction que l'audit de confirmation ; sa lecture constitue la preuve de résultat. Toute erreur laisse l'ensemble invisible.

Pour `EXTERNE`, le scellement lit uniquement les métadonnées de dotation et met à jour une opération : il ne réécrit ni toutes les attributions ni la réserve. Les intentions d'email ne sont pas copiées dans l'outbox à ce moment. Le coût du rendu et de leur mise à disposition est porté par un worker après confirmation. Le protocole numérique futur devra mesurer séparément les gardes liées aux commerces et exemplaires avant d'autoriser son scellement.

## Remplacement, suivi et effets

Un remplacement verrouille animation, opération et attribution courante. Le domaine vérifie refus documenté ou 14 jours depuis le premier envoi réussi, absence de réponse incompatible et absence de remise déclarée active. Il consomme le premier suppléant encore éligible ; une exclusion est motivée par les faits de domaine, sans choix arbitraire du gestionnaire. L'ancien gagnant demeure dans la preuve historique et ne redevient jamais candidat.

Si la réserve est épuisée, une commande de retirage distincte réutilise la population gelée en excluant tous les anciens gagnants. Elle suit le même protocole privé, avec un lien vers l'attribution à remplacer. Un résultat vide ne retire aucun droit existant. Contact, réponse, refus, incident, remise déclarée et correction ciblée sont des événements tracés ; l'état d'envoi reste indépendant de la remise.

Le worker d'email sélectionne uniquement des intentions confirmées. Un cycle exécute 25 tranches par défaut, au maximum 100, et cesse d'en démarrer après 20 secondes. Chaque attribution possède une identité d'envoi unique. Le rendu HTML/texte passe par un adaptateur et le transport par l'outbox existante. Son échec n'annule pas l'attribution. La première date réelle de succès de l'outbox est la référence du délai de remplacement ; mise en file et reprise ne modifient pas cette origine. Aucun fournisseur réel n'est invoqué dans les preuves locales.

Une préparation email échouée est isolée et devient reprenable par une commande habilitée, avec le même gain et un reçu. La réussite du transport renseigne atomiquement `premiere_reussite_at` seulement si elle est absente. Le lien email fournit une capacité de consultation du gain externe, hashée et bornée à 90 jours techniques ; il ne crée aucun token de participation. Le secret circule dans le fragment du lien puis dans le corps de la résolution limitée en fréquence, jamais dans une URL d'API, un carnet ou une trace. Un ancien gagnant remplacé consulte son état historique sans accéder au suppléant. Une identité déjà anonymisée n'est consultée que dans l'archive restreinte existante ; son absence interdit la préparation, sans réhydratation des coordonnées courantes.

## Index, lectures et preuves

- Candidats : unicités `(operation_id, participant_id)`, `(operation_id, cle_aleatoire)` et `(operation_id, rang)` ; réserve disponible par opération/rang.
- Opérations : une initiale par animation ; file par état/date/id ; recherche d'une opération et contrôle de confirmation par clé primaire.
- Attributions : unicité historique `(animation_id, participant_id)`, unité courante unique, pages animation/rang/id, lecture personnelle participant/animation/id.
- Suivi : `(attribution_id, occurred_at, id)` ; reçus par acteur/ressource/clé ; intentions par état/date/id.
- Pages publiques de gestion : 25 éléments par défaut, 100 maximum, `LIMIT + 1`, curseur opaque lié à la ressource ; jamais de total recalculé sur le journal.

La réserve est présentée dans l'ordre des opérations confirmées `(created_at, id)`, puis des rangs, identique au choix du suppléant. Sa requête sélectionne au maximum `limit + 1` opérations et, par jointure `LATERAL`, `limit + 1` candidats par opération ; le tri final reste donc borné à 10 201 lignes au maximum, même si la réserve contient des millions de candidats. Les opérations confirmées disposent de l'index partiel `(animation_id, created_at, id)`. Les curseurs vérifient leur ressource, leur arité et les types UUID/rang/date : une valeur malformée retourne `400 CURSEUR_INVALIDE`.

La présence d'un candidat après le curseur se vérifie par une sonde scalaire corrélée `ORDER BY rang LIMIT 1`, avec borne de rang indexable. Un `EXISTS` susceptible d'être transformé en semi-jointure ne garantit pas cette borne : la preuve ajoutée a détecté un parcours des 10 000 candidats à la deuxième page avant correction. Les plans réels des pages initiale, suivante et après le rang 9 000 utilisent désormais `uq_candidat_libre_rang`, une ligne sondée et 26 lignes de page, sans filtrage de tous les rangs précédents. Le tri final borné demeure permis.

Le total des unités est stocké en `BIGINT`, comme les métadonnées de dotation. Une dotation de trois milliards d'unités et un participant ne produit qu'une attribution ; aucune unité excédentaire n'est matérialisée pour le tirage externe.

## Exécution locale et activation future

Le lanceur `python -m scripts.exploitation.traiter_tirages_libres --limit 25` simule par défaut depuis la racine du backend. L'application effective demande à la fois `--apply` et `LOCALEO_ANIMATION_TIRAGES_LIBRES_APPLY=true`. Le point d'entrée interne `POST /internal/animation-locale/tirages-libres/traiter` suit la même garde et exige une clé de portée `internal:batch` ; son corps contient `simulation` (vrai par défaut) et `limit` (1 à 100). Chaque phase peut reprendre la même opération après interruption. Ce lot n'active aucun ordonnanceur, ne modifie aucun environnement et n'exécute aucun fournisseur réel.

La préparation des emails alimente l'outbox existante ; le transport conserve son mécanisme d'exploitation habituel. La simulation ne modifie ni préparation, ni attribution, ni email.

## Mesures locales du lot

Sur PostgreSQL isolé, la preuve `test_performance_10000_candidats_1000_lignes_et_scellement_constant` traite 10 000 candidats et 1 000 lignes de lots distinctes. La tranche de 500 gagnants émet 16 lectures SQL et son pic mémoire mesuré est d'environ 2,5 Mo. Le scellement produit deux écritures — opération et audit — sans mise à jour des candidats ni des attributions. Les pages de gains restent à une requête SQL, sans lecture par ligne.

Les plans avec statistiques actualisées utilisent `uq_animation_population_membre` et `uq_candidat_libre_cle` pour lire 500 lignes ; aucune lecture séquentielle ni aucun tri de toute la population n'est accepté par cette preuve. Les temps observés localement sont inférieurs à 3 ms par lecture sur cette exécution ; ils ne constituent pas un engagement de temps de réponse en hébergement. Les statistiques PostgreSQL doivent rester entretenues pour que le plan utilise ces index. L'artefact local `.artifacts/e73-tirage-libre-performance.json` contient les plans, buffers et mesures de la dernière exécution, sans être versionné.

Les preuves exigées sont : plans `EXPLAIN (ANALYZE, BUFFERS)` avec 10 000 membres ; mémoire applicative et taille des lots de résultats ; coût de scellement indépendant de la réserve ; rejet des préparations dans tous les lecteurs ; deux confirmations concurrentes ; rollback avant marqueur ; timeout puis relecture ; reprise après interruption ; collision de clés simulée ; unicité et stabilité de la permutation ; un lot maximum par participant ; zéro candidat ; remplacement et correction concurrents ; aucun effet Coffrets ni envoi réel.

Les résultats d'exécution sont consignés dans [le suivi d'implémentation](suivi-implementation.md) et [la vérification de livraison](verification-livraison.md). Ce document décrit le protocole et ne vaut pas preuve de disponibilité en environnement.

## Extension numérique — protocole du lot 05

Les étapes d'indexation et de classement restent bornées à 500 candidats, sans
garde commerce. Les affectations numériques publiées remplacent les lignes
externes comme source des unités, par pages et dans leur ordre immuable.
Attributions, bons et intentions d'envoi initiaux sont préparés privés. Tous
leurs lecteurs, protections d'engagement et traitements exigent le marqueur
`confirmed_at` de l'opération ; un enregistrement privé ne constitue pas un bon
attribué. L'origine métier est `COALESCE(bon.attributed_at, tirage.confirmed_at)`.
L'échéance initiale dérive de cette origine et de la durée publiée, sans mettre
à jour tous les bons au scellement.

Seule la phase de scellement prend, après l'autorité organisatrice, les gardes
de commune puis de tous les commerces de la dotation dans un ordre stable,
par pages de 100. Elle prend ensuite animation/opération, puis exemplaires
gagnants triés, et revérifie configuration, droits normaux, absence de
suspension, affectations et préparations. Le marqueur de confirmation et son
audit activent atomiquement gains, bons et intentions ; aucun email ni capacité
personnelle n'est créé avant cette confirmation. Le coût final dépend des
commerces et exemplaires gagnants, pas de la réserve des suppléants. Sa mémoire,
ses requêtes, ses verrous et son délai doivent être mesurés ; dépasser un budget
technique laisse l'opération diagnostiquée et reprenable, sans tronquer le tirage.

Un remplacement direct prend la garde du commerce avant l'animation et le bon.
Il exige un droit normal à un nouvel engagement ; un droit résiduel ne suffit
pas. Révocation de l'ancien bon, nouveau bon daté de la nouvelle attribution,
suppléant utilisé et intention d'envoi sont transactionnels. Pour un retirage
préparé, ces effets n'interviennent qu'au scellement ; l'ancien bon reste intact
si aucun candidat ou un commerce indisponible empêche le remplacement.

QR et PIN appellent le même cœur de consommation sans commit interne. L'ordre
E70 place la demande/contexte avant la cible. Le reçu durable conserve son
occurrence historique et expose aussi l'état courant après une correction.
La protection lors du retrait du périmètre vise le bon exact, jamais seulement
l'animation. Une ancienne participation ne donne aucun droit sur un bon nouveau.

La capacité personnelle d'un bon est distincte de son QR et de l'accès de jeu.
Elle est hashée, limitée à ce bon et valable 400 jours techniques après émission,
ce qui couvre la durée métier maximale de 365 jours et sa consultation historique.
Cette borne ne prolonge ni le bon ni la conservation des données. Une rotation
QR invalide les anciennes présentations de scan/PIN sans supprimer le chemin de
consultation du gagnant. L'ancien bon remplacé montre seulement sa révocation,
sans information sur son successeur. Les tokens restent hors URL d'API et traces.
