# Audit indépendant — mémoire

Date : 19 novembre 2026. Périmètre : matérialisations, médias, fichiers, CSV, agrégations et bornes, avec priorité Localeo Live et Animation. Lecture du code courant uniquement ; HEAD backend observé : `7049e7fafc76f9119924f1082a5ee7457a175d85` (des modifications de travail peuvent s'y ajouter). Modèle exact : INCONNU ; effort de raisonnement : INCONNU. Aucun ancien audit ni rapport d'un autre agent lu avant finalisation.

Quatre constats majeurs retenus. « FORTEMENT ÉTAYÉ PAR LE CODE » qualifie la présence du mécanisme, pas une saturation observée. Aucun chiffre de consommation, seuil de panne ni fréquence réelle ne peut être conclu sans mesure. Les chemins ci-dessous sont relatifs à `localeo-backend`.

## MEM-01 — Notifications de publication et de résultat : populations entièrement résidentes

**Statut : FORTEMENT ÉTAYÉ PAR LE CODE. Domaine : Animation / Live.**

**Sources et fonctions.** `app/application/animation_locale/services/notifications_localeo_live.py:43-94`, `creer_publication_dans_uow` ; `:97-120`, `_participations_par_installation` ; `:160-203`, `creer_resultat_tirage_dans_uow`. Producteurs : `publication_animation.py:345` et `tirages_animation.py:280`, dans le même dossier.

**Mécanisme et preuve.** La publication appelle `select(InstallationLocaleoLiveOrm).where(actif.is_(True)).scalars().all()` pour toutes les installations actives de la plateforme, puis filtre la commune en Python. Elle conserve les objets retenus, une liste d'identifiants, un ensemble des notifications existantes et ajoute les notifications ORM avant le commit de publication (`publication_animation.py:372`). Une petite commune paie donc déjà le chargement global des installations. Le résultat du tirage charge toutes les paires installation/participant de l'animation via `.all()`, produit une deuxième liste, puis un dictionnaire par installation avant d'émettre les notifications.

**Flux, conséquence et déclencheur.** Publication d'une animation par le portail/ERP et résultat du tirage de coffrets via `POST /animations/{animation_id}/tirages`. Le pic mémoire croît avec les installations globales pour la publication, avec les suivis de participation pour le résultat ; plusieurs publications simultanées reproduisent ces matérialisations dans chaque requête. Risque de ralentissement et d'échec du processus sous budget mémoire contraint ; aucun OOM observé ici. Le résultat peut dédupliquer tardivement plusieurs participations d'une même installation.

**Confiance / priorité.** Confiance élevée dans le mécanisme ; volumétrie inconnue. Impact potentiel élevé ; probabilité moyenne, croissante avec l'adoption Live ; criticité élevée à l'échelle plateforme.

**Correction locale minimale.** Déplacer le ciblage commune/catégorie en SQL et parcourir les installations distinctes par clé, par lots bornés ; insérer les notifications par lot avec conflit idempotent. Pour le résultat, agréger `est_gagnant` par installation en SQL ou dans un lot stable d'installations, puis émettre le même titre/payload. Le voisin `_notifier_participations_par_lots` (`:15-33`) fournit déjà un précédent de pages de 500 et d'insertion groupée, sans justifier une réutilisation aveugle : il ne calcule pas le statut gagnant.

**Effort : M.** Risque moyen : conserver ciblage, déduplication par installation, préférence catégorie, `source_key`, atomicité et gestion des publications concurrentes. Pas de breaking change HTTP nécessaire. Domaines transverses : idempotence, transaction publication/tirage, notifications et préférences Live. Preuves attendues après correction : cas multi-participations dont un gagnant, reprise sans doublon et nombre maximal d'objets chargés par lot sur une grande population synthétique.

## MEM-02 — Diffusion des actualités Live : chargements globaux à chaque cycle

**Statut : FORTEMENT ÉTAYÉ PAR LE CODE. Domaine : diffusion Live / batch.**

**Sources et fonction.** `app/api/localeo_live_api.py:825-1023`, `diffuser_actualites_localeo_live` ; appel par le handler interne `:1430`.

**Mécanisme et preuve.** Le cycle conserve simultanément `statuts_animations`, `a_publier`, `a_bloquer`, `a_expirer` (`:842-874`), puis toutes les actualités publiables courantes (`:910-937`) et toutes les installations actives (`:938-942`), sans `LIMIT`. Pour chaque actualité Animation il construit aussi l'ensemble de toutes les installations participantes (`:948-962`). Les actualités déjà publiées restent candidates à la recherche des notifications manquantes. La boucle parcourt ensuite toutes les installations pour chaque actualité (`:979` et suite).

**Flux, conséquence et déclencheur.** Exécution de la diffusion des actualités éditoriales et Animation, y compris en simulation pour les lectures globales. Le besoin mémoire croît au minimum avec le nombre d'installations et d'actualités actives/échues ; un retard accumulé augmente également les trois listes de transitions. Le travail de ciblage est répété par actualité. Cela peut faire coïncider un pic du batch avec le trafic QR/participation sur le même service, sans que l'audit puisse affirmer sa fréquence ou son impact réel. Ne pas confondre cette absence de pagination avec un défaut de l'inbox utilisateur, qui possède une limite.

**Confiance / priorité.** Élevée sur le code ; exploitation réelle inconnue. Impact potentiel élevé ; probabilité moyenne avec croissance/adoption et accumulation ; criticité élevée.

**Correction locale minimale.** Traiter les actualités par pages stables et les destinataires ciblés par pages SQL, sans liste globale d'installations. Borner également les transitions à un lot de travail et permettre les cycles suivants. Conserver la barrière de statut Animation et l'ordre des verrous, explicitement documentés dans la fonction ; ne pas simplement ajouter un `LIMIT` sans curseur/reprise, qui affamerait des destinataires.

**Effort : L.** Risque moyen à élevé : transactions, publication/expiration, concurrence avec « Terminer », idempotence et équivalence du `dry_run`. Pas de rupture du format de notification nécessaire ; toute modification des compteurs d'un cycle doit être explicitée pour les consommateurs internes/ops. Preuves attendues : convergence de plusieurs cycles, absence de doublon, arrêt d'animation concurrent et borne des pages réellement résidentes.

## MEM-03 — Le tirage de coffrets rematérialise la population gelée

**Statut : FORTEMENT ÉTAYÉ PAR LE CODE. Domaine : tirage historique de coffrets Animation.**

**Sources et fonctions.** `app/infrastructure/persistence/repositories/animation_locale_repositories.py:1718-1725`, `_population`, et `:1751-1756`, `obtenir_population_courante` ; `app/domaine/animation_locale/entities/tirage_animation.py:88-110`, `PopulationEligibleAnimation` ; `app/application/animation_locale/services/tirages_animation.py:247-259`, `lancer` ; route `app/api/animation_locale_api.py:2740-2744`.

**Mécanisme et preuve.** Le repository lit tous les UUID des membres gelés par `.scalars().all()`, construit un tuple ; l'entité crée un ensemble de toute la population pour détecter les doublons ; `selectionner` fait ensuite `random_source.sample(list(self.participant_ids), nombre_total)`. La liste passée au tirage est donc proportionnelle au nombre d'éligibles même pour quelques lots. Le service ne pose pas de plafond de population sur ce chemin.

**Flux, conséquence et déclencheur.** `POST /animations/{animation_id}/tirages`, dotation de coffrets autorisée par `ServiceDotationAnimation.courante(...).autoriser_financement_coffrets()`. Pic mémoire O(N) en identifiants et collections transitoires lors du tirage d'une grande population gelée, dans la transaction qui verrouille l'animation. Concurrence de tirages sur des animations différentes : pics cumulables.

**Frontière essentielle.** La clôture possède un en-tête et des insertions par lots de 500 (`animation_locale_repositories.py:1682-1715`). Le constat vise le consommateur de la population lors du tirage, pas une prétendue clôture entièrement non bornée. Il ne s'étend pas au tirage des lots libres : `services/tirages_libres.py:240-281` traite des phases reprenables et `traitement_tirages_libres.py:5-18` borne un cycle en nombre d'opérations et durée.

**Confiance / priorité.** Élevée pour le mécanisme et la route exposée ; usage et taille maximale de ces dotations inconnus. Impact élevé sur grande population ; probabilité faible à moyenne, limitée aux dotations de coffrets ; criticité moyenne.

**Correction locale minimale.** À court terme, éviter la copie `list` inutile pour `sample` et ne pas reconstruire un ensemble si l'unicité est déjà garantie par un contrat de persistance prouvé ; cela réduit le pic sans supprimer O(N). Pour une vraie borne, sélectionner via un parcours par lots avec réservoir de taille gagnants + suppléants, en conservant une sélection uniforme sans remise, la population/version gelée et la source aléatoire injectée. Ce dernier changement demande une preuve algorithmique et des tests dédiés ; copier le fonctionnement des lots libres sans analyser ses contrats ne suffit pas.

**Effort : S pour suppression de copie seule ; M pour sélection bornée.** Risque moyen à élevé pour l'algorithme de sélection et la reproductibilité de la preuve ; aucun changement HTTP nécessaire. Transverse : équité du tirage, audit, population gelée, suppléants. Aucune migration proposée sans inspection complémentaire des contraintes.

## MEM-04 — Retrait accepté d'un commerçant : tous les faits de participation chargés

**Statut : FORTEMENT ÉTAYÉ PAR LE CODE. Domaine : gestion Animation / retrait classique.**

**Sources et fonctions.** `app/application/animation_locale/services/demandes_participation_commercants.py:560-639`, `traiter_retrait`, en particulier `:613-616` ; `app/infrastructure/persistence/repositories/exploitation_animation_repository.py:20-29`, `faits_participations`.

**Mécanisme et preuve.** Accepter le retrait classique appelle `faits_participations(animation.id)` pour itérer sur les participants à réconcilier. Le repository charge tous les ORM participants, toutes les exécutions dans un dictionnaire, toutes les validations valides dans des listes par participant, éventuellement les preuves email, puis retourne une liste complète de dictionnaires d'entités. L'appelant utilise seulement `ligne['participant'].id` avant de recharger chaque participant sous verrou et de réconcilier. Le chargement complet d'exécutions et de validations à cet endroit est donc évitable indépendamment de l'optimisation de la réconciliation.

**Flux, conséquence et déclencheur.** Acceptation d'une demande de retrait côté gestion partenaire sur une animation déjà fréquentée, dans une transaction qui verrouille l'animation. Le pic dépend de la totalité participants + exécutions + preuves, même lorsque l'action porte sur un seul commerce ; des snapshots d'exécution volumineux aggravent le poids. Chasse publiée exclue explicitement à `:584-585` : ne pas étendre le constat à sa neutralisation dédiée.

**Confiance / priorité.** Élevée dans le chargement superflu ; volumétrie et fréquence des retraits inconnues. Impact potentiel élevé, probabilité faible à moyenne ; criticité moyenne.

**Correction locale minimale.** Remplacer cette lecture par un parcours des seuls identifiants de participants par clé et lots, puis conserver `obtenir_pour_mise_a_jour` et `reconcilier_dans_uow` pour chaque participant. Une réduction supplémentaire de la mémoire ORM doit préserver le flush des modifications avant expulsion ; ne pas changer l'atomicité du retrait simplement pour découper les transactions. Le helper `faits_participations_par_lots` (`exploitation_animation_repository.py:31-63`) reste plus riche que le besoin de ce consommateur.

**Effort : M.** Risque moyen : couverture de tous les participants, ordre stable, anonymisation, cohérence configuration/flyer et concurrence avec les scans. Pas de breaking change externe attendu ; domaine propriétaire des transitions inchangé. Preuves attendues : équivalence des progressions après retrait, absence d'effet sur participants anonymisés, borne du parcours des identifiants et rollback intégral sur échec.

## Limites et validation

Revue statique en lecture seule du backend ; seuls ce rapport et son annexe ont été créés dans le dépôt documentaire. Aucun import de `app.main`, dotenv privé, réseau, base, serveur, test ou benchmark exécuté. Les commandes employées lisent les sources et le SHA Git. Aucun ancien audit ni rapport d'agent consulté. Les contrôles documentaires n'ont pas été exécutés, conformément à la restriction de cette mission ; aucune validation verte n'est revendiquée.

Pas de correction, migration, changement de contrat, générateur ou consommateur frontend dans cette mission ; leurs impacts figurent dans chaque piste de correction. Les constats ne constituent pas une mesure de fuite mémoire : ils identifient des populations matérialisées, leurs propriétaires et les déclencheurs visibles. Le dashboard complet, le comportement du driver SQL, le nombre de workers et les enveloppes mémoire de déploiement ne sont pas établis. Les observations secondaires et protections déjà présentes sont dans [l'annexe](02-memoire-annexe.md).
