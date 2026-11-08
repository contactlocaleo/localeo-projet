# Localeo Live — performance des API de recherche et de consultation

Audit du **8 novembre 2026**, à la demande de l’utilisateur, sur les lectures qui alimentent Localeo Live. Rapport de diagnostic et propositions ; aucune correction applicative ni opération sur les données TEST n’est effectuée dans cet audit.

## 1. Conclusion et ordre de traitement

**Oui, plusieurs chemins présentent des problèmes de performance ou de passage à l’échelle.** La lenteur ressentie ne vient pas d’une seule API : le coût des lectures serveur s’ajoute à des appels en chaîne et à l’attente dans la file du navigateur.

| Ordre | Constat | Niveau de preuve | Action recommandée |
| --- | --- | --- | --- |
| 1 — P1 | L’ancien catalogue augmente son nombre de requêtes avec la taille de page : **20 SELECT pour 12 cartes, 58 pour 50**, contre 7 constants pour la recherche moderne dans le même jeu. | Mesuré sur PostgreSQL isolé ; mécanisme confirmé dans le code. | Grouper les configurations effectives, supprimer le comptage obligatoire du catalogue ou le séparer ; faire converger les consommateurs vers la lecture moderne. |
| 2 — P1 | « Mes participations » attend la résolution de tout le carnet : jusqu’à **2N GET**, auxquels s’ajoute le dashboard. L’ouverture d’une participation provoque encore des relectures. | Graphe d’appels vérifié dans le frontend ; durée privée TEST non mesurée. | Charger en priorité les cartes visibles et la participation demandée, supprimer les doublons, borner les producteurs et annuler les lectures obsolètes. |
| 3 — P1 | « Mes lots » peut attendre **jusqu’à 50 POST de liaison**, deux à la fois, avant de consulter récompenses et tirages. | Code vérifié ; aucune liaison déclenchée sur TEST pendant l’audit. | Dissocier consultation des lots et synchronisation des accès manquants. |
| 4 — P1 | La recherche moderne dépasse son objectif local p95 de 500 ms dans **3 scénarios sur 8**, tous à dix lecteurs : **653 à 677 ms**. | Benchmark existant rejoué ; service local, pas HTTP TEST ni matériel de référence qualifié. | Profiler concurrence, temps Python/SQL, attente de pool ; réduire les lectures accessoires puis rejouer la qualification de capacité. |
| 5 — P1, diagnostic à compléter | Une fiche animation publique prend **928 à 963 ms** sur trois consultations TEST, pour seulement 3,8 ko de JSON. | Lenteur HTTP observée ; attribution SQL/infrastructure non isolée. | Instrumenter cette route avec des données représentatives avant de choisir index, regroupement ou réduction de projection. |
| 6 — P2 | Écritures d’activité dans plusieurs GET privés, N+1 des preuves de tombolas publiques, comptages des messages et double lecture des lots. | Chemins de code vérifiés ; impact chiffré privé restant à mesurer. | Traiter les coûts évitables décrits en §5, avec budgets SQL par page. |

Le premier chantier recommandé associe **ancien catalogue + orchestration du carnet** : il réduit directement le nombre d’allers-retours. Augmenter les tailles de pool, les délais ou les capacités d’hébergement sans ces mesures ne résoudrait pas les appels redondants.

## 2. Périmètre et méthode

Sources examinées : backend `1b3e27c4755a441ddd9b99cd0ddf83887879e136`, marketplace `c40ee5ab02f463dd159874a7e96f5748200b0403`, documentation `e04248e0ea4cb3f08e5f68081f751822f27bb350`, branche `main`. Les retouches locales préexistantes du header Live et de leur documentation sont conservées. Les SHA ci-dessus décrivent les références locales ; **le SHA réellement déployé sur TEST n’a pas été attesté**.

Trois sources de preuves complémentaires :

1. Lecture des routes, services, adaptateurs SQL et appels frontend, avec deux explorations indépendantes backend/frontend.
2. **27 GET publics mesurés**, séquentiels et espacés d’une seconde, sur `https://test-api.localeo.city`, API annoncée par la configuration publique de `https://test-animations.localeo.city`. Neuf lectures, trois essais chacune. Trois GET préliminaires supplémentaires ont identifié la configuration et les données publiques ; ils sont exclus du tableau comparatif.
3. Deux contrôles sur une **nouvelle base PostgreSQL 18.3 jetable locale**, sans configuration opérateur : benchmark N/10N existant puis comptage SQL ciblé. Python 3.14.3, lanceur isolé bloquant les connexions externes et le chargement des `.env`. Aucune charge n’a été appliquée au TEST partagé.

Références : [convention de performance](../../architecture/transverse/performance-volumetrie.md), [budgets Live LA-16](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md), [dispositif E59](../../specifications/epic-59-tests-performance-api/README.md). La présente analyse ne ferme pas la réserve de capacité LA-16.

**Limites :** pas de chronométrage des données personnelles réelles, pas d’accès DB TEST, pas de mesures CPU/pool/verrous du déploiement, pas de campagne HTTP soutenue ni mixte. Les temps HTTP incluent DNS/TCP/TLS et réseau ; les mesures locales de service les excluent. Les trois essais par route ne permettent ni p95 ni certification de SLO. Le premier essai n’est pas une preuve de démarrage à froid du serveur.

## 3. Mesures publiques sur TEST

Mesures du soir du 8 novembre, heure de Paris. Catalogue et recherche filtrés sur Latresne, page demandée de 12 ; fiche passeport publique `36446b97-6a27-54d2-af68-d815596af410`. Les capacités des quatre moteurs pris en charge par Live sont transmises aux routes concernées. Chaque appel utilise un nouveau processus `curl`, sans réutilisation de connexion entre essais et sans compression demandée.

| GET, préfixe omis quand indiqué | Résultat de la lecture | Total essai 1 / 2 / 3 | Médiane | Corps reçu |
| --- | --- | --- | --- | --- |
| `/public/localeo-live/configuration` | Capacités publiques | 716 / 264 / 345 ms | 345 ms | 302 octets |
| `/public/animation-locale/animations/recherche`, `EN_COURS` | 3 cartes | 284 / 433 / 265 ms | 284 ms | 7 161 octets |
| Même recherche, `A_VENIR` | Aucun résultat | 233 / 273 / 174 ms | 233 ms | 134 octets |
| `/public/animation-locale/animations` | 3 cartes | 715 / 444 / 1 251 ms | 715 ms | 7 108 octets |
| `/public/animation-locale/animations/{id}` | Fiche publique passeport | 928 / 963 / 952 ms | 952 ms | 3 770 octets |
| `/public/animation-locale/commercants` | 8 commerces | 546 / 274 / 303 ms | 303 ms | 3 055 octets |
| Même annuaire, `q=escale` | 1 commerce | 278 / 173 / 148 ms | 173 ms | 454 octets |
| `/public/animation-locale/commercants/{id}` | Fiche d’un commerce | 243 / 174 / 210 ms | 210 ms | 649 octets |
| `/public/animation-locale/animations/{id}/contact-public` | Pas de contact retourné | 176 / 224 / 333 ms | 224 ms | 16 octets |

**27 réponses 200, aucun échec dans cet échantillon.** Le transfert du corps est très court : sur la fiche animation, les TTFB sont 927 / 962 / 951 ms, presque égaux aux temps totaux. Sa lenteur observée précède donc essentiellement la réception du JSON. Ce constat ne sépare pas calcul serveur, accès DB, file d’exécution et transit réseau. Le test de contact vide ne qualifie pas un cas avec contact complet.

La recherche moderne est plus rapide dans ce relevé que l’ancien catalogue, mais les appels sont successifs, sans contrôle de cocharge serveur : le rapport ne présente pas leur rapport de durée comme un gain causal garanti. Aucun démarrage à froid Render, défaut réseau ou manque de ressources de TEST n’a été démontré.

## 4. Mesures isolées reproductibles

### 4.1. Recherche moderne : concurrence et volumétrie

Commande réellement exécutée depuis le backend, avec une base locale neuve :

```powershell
& 'C:/Users/casta/AppData/Local/Python/bin/python.exe' scripts/validation/test_isolated.py --postgres-test-url 'postgresql+psycopg://audit_test@127.0.0.1:55473/localeo_audit_test' tests/security/test_adhesion_live_read_performance.py -q
```

**Résultat : 1 test réussi en 73,91 s.** Le test vérifie les bornes SQL/mémoire et les résultats ; il consigne le respect du p95 mais ne l’asserte pas. Son résultat vert n’annule donc pas les trois dépassements suivants.

| Animations synthétiques | Page | Lecteurs simultanés | p50 | p95 | p99 | Objectif p95 ≤ 500 ms |
| --- | --- | --- | --- | --- | --- | --- |
| 1 000 | 12 | 1 | 41 ms | 55 ms | 60 ms | Respecté localement |
| 1 000 | 12 | 10 | 308 ms | **677 ms** | 738 ms | **Dépassé** |
| 1 000 | 50 | 1 | 54 ms | 80 ms | 168 ms | Respecté localement |
| 1 000 | 50 | 10 | 427 ms | **660 ms** | 770 ms | **Dépassé** |
| 10 000 | 12 | 1 | 47 ms | 81 ms | 117 ms | Respecté localement |
| 10 000 | 12 | 10 | 237 ms | 295 ms | 337 ms | Respecté localement |
| 10 000 | 50 | 1 | 44 ms | 65 ms | 78 ms | Respecté localement |
| 10 000 | 50 | 10 | 312 ms | **653 ms** | 852 ms | **Dépassé** |

Pour chaque scénario : 100 lectures mesurées après 30 de chauffe, recherche textuelle fréquente `Rencontre`, garde BUM activée, pool de lecture 10 sans débordement. **8 SELECT/WITH par page**, pic Python mesuré d’environ **0,36 à 0,56 Mio**, sous la borne de 10 Mio. Les premiers appels par couple volume/page prennent 49 à 181 ms ; ni le cache PostgreSQL ni l’ensemble de la machine ne sont remis à froid entre scénarios.

Les plans `EXPLAIN (ANALYZE, BUFFERS)` ont été enregistrés sur le jeu jetable après `ANALYZE`. À 10 000 animations/page 50, les huit requêtes prises séparément totalisent environ 9,5 ms d’exécution et 7,7 ms de planification dans cette capture sans concurrence. Cela ne mesure ni le coût Python/ORM ni les attentes sous dix lecteurs : **aucune requête SQL unique n’est identifiée ici comme cause des 653 ms**. Les résultats non monotones entre N et 10N interdisent aussi de conclure à une croissance linéaire de la latence du catalogue moderne.

La référence exigée de 2 vCPU/4 Gio par composant n’est pas reproduite sur ce poste ; les scénarios de cinq minutes, recherches rares/vides, écritures simultanées, saturation 20/40 lecteurs, notifications, lots et médias ne sont pas couverts. Ce benchmark démontre une réserve locale sous concurrence, pas la capacité du déploiement TEST.

### 4.2. Ancien catalogue contre recherche moderne : nombre de requêtes

Contrôle temporaire exécuté via le même lanceur isolé : `tmp/live-api-audit-20261108/test_query_budget_audit.py`, **1 test réussi en 20,37 s**. Jeu de 64 animations, session neuve à chaque lecture, sans filtre texte ni participants, lots ou médias. La fixture historique ne contient pas de définition moteur classique : les lectures de retraits supplémentaires de cette branche ne sont pas incluses dans les chiffres.

| Lecture, garde BUM active | Page 1 | Page 12 | Page 50 |
| --- | --- | --- | --- |
| Ancien catalogue : SELECT | 9 | **20** | **58** |
| Dont lecture directe des paramètres d’exploitation | 2 | 13 | 51 |
| Recherche moderne : SELECT | **7** | **7** | **7** |
| Dont lecture groupée des configurations | 1 | 1 | 1 |

La fiche détail de ce jeu minimal exécute 7 SELECT. Désactiver la garde BUM retire un SELECT à chaque lecture ; ce n’est pas une proposition de correction. Les sept lectures modernes deviennent huit avec le filtre texte du benchmark précédent.

Sur cinq lectures chauffées par cas, les médianes de service local sont 53/84/138 ms pour l’ancien catalogue et 35/62/49 ms pour le moderne ; détail 40 ms. Ces petits échantillons décrivent le protocole, pas un p95. La fiche sans partenaires de la fixture ne représente pas celle de TEST : ses 40 ms ne contredisent pas les 952 ms HTTP observés avec d’autres données et une autre infrastructure.

## 5. Problèmes serveur et corrections proposées

Les références suivantes visent les sources locales auditées. Les durées non mesurées sont signalées comme risques structurels, pas comme ralentissements TEST établis.

### API-01 — P1 : ancien catalogue, comptage global et requêtes par carte

Dans [catalogue_animations_publiques.py](../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py), `rechercher` recalcule un `COUNT` du résultat complet avant curseur (lignes 331–335), puis `_projections` charge les paramètres effectifs par animation (617–619). La clé du curseur les recharge encore (361). [parametres_exploitation_repository.py](../../../../localeo-backend/app/infrastructure/persistence/repositories/parametres_exploitation_repository.py), lignes 45–47 et 82–92, ajoute selon le modèle une recherche de retraits commerçants à la lecture des paramètres.

**Conséquence :** nombre d’allers-retours croissant avec la page, en plus du travail global du total. Le chemin reste utilisé pour les animations d’une fiche commerçant et comme repli de compatibilité. La recherche moderne de l’accueil n’utilise pas ce chemin lorsque la capacité serveur est annoncée.

**Correction :** réutiliser la lecture groupée `configurations_effectives_page`, y compris pour le curseur ; ne pas recalculer un total exhaustif à chaque page ; migrer les consommateurs compatibles vers le service moderne. Préserver filtres publics, compatibilité des curseurs, retraits et dates effectives. **Preuve attendue :** budget SQL constant pour pages 1/12/50 et N/10N, avec vrais modèles classiques et retraits ; comparer aussi les résultats métier.

### API-02 — P1 : fiche publique lente, cause à isoler

`GET /animations/{id}` présente une latence répétée proche d’une seconde dans l’échantillon TEST. Le [service de catalogue](../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py) projette configuration, dynamique, partenaires, dotation, modèle, règlement et visuel. Le cas synthétique minimal ne suffit pas à reproduire le coût d’une fiche réelle.

**Correction proposée en premier :** traces corrélées temps HTTP/SQL/stockage, nombre de requêtes et objets chargés, temps de pool et de sérialisation, sur une fiche avec partenaires et lots. Puis regrouper uniquement les enrichissements coûteux prouvés et dissocier les sous-listes non indispensables au premier affichage. **Preuve attendue :** fiche à 1/10/50 partenaires et lots, p50/p95/p99 HTTP chaud et premier accès, comparaison à la recherche avec le même environnement. Aucun index précis ni gain chiffré ne peut être promis à ce stade.

### API-03 — P2 : écritures et doubles transactions dans des GET privés

[localeo_live_api.py](../../../../localeo-backend/app/api/localeo_live_api.py), lignes 204–210, 494–525 : le contrôle d’installation met à jour `date_derniere_activite`, commit, puis dashboard/récompenses/tirages ouvrent leur propre UoW et relisent l’installation.

**Risque :** trois lectures lancées ensemble ajoutent des écritures synchrones sur la même installation, des transactions et des allers-retours ; contention possible mais non mesurée. **Correction :** une seule UoW de contrôle et lecture, activité actualisée conditionnellement à intervalle raisonnable. Maintenir le contrôle courant du secret, de l’état et des révocations. **Preuve :** SQL/COMMIT et attente de verrous pour une rafale de lectures de la même installation, puis plusieurs installations distinctes.

### API-04 — P2, pouvant devenir P1 : preuves de tombola publique par participant

[tableau_de_bord_live.py](../../../../localeo-backend/app/application/animation_locale/services/tableau_de_bord_live.py), lignes 108–119, et [jeu_animation.py](../../../../localeo-backend/app/application/animation_locale/services/jeu_animation.py), lignes 102–104 : malgré les préchargements groupés, la preuve email est encore obtenue par participant. Le repository effectue un `session.get`. Le calcul des prochains tirages passe aussi par ces faits.

**Risque :** jusqu’à 50 lectures supplémentaires pour une page de 50 tombolas publiques. **Correction :** port de lecture groupée des preuves pour les IDs de la page et injection dans les faits du moteur. Conserver les règles email/règlement et l’autorisation actuelle. **Preuve :** nombre SQL stable à 1/10/50 participants, incluant tombolas publiques, preuves absentes et révoquées.

### API-05 — P2 : messages, totaux recalculés sur chaque page

[messagerie_organisateur_repository.py](../../../../localeo-backend/app/infrastructure/persistence/repositories/messagerie_organisateur_repository.py), lignes 88–94 et 143 : la page de messages est bornée, mais deux `COUNT` des non-lus sont recalculés sur chaque page, avec jointures de droits pour les messages personnels. La route d’indicateur utilise déjà des `EXISTS` (96–111).

**Correction :** distinguer indicateur de présence, total exact et pagination ; calculer le total seulement lorsque le parcours en a besoin, garder un `EXISTS` pour le badge et réévaluer les accès courants. Le shell charge actuellement 25 messages plutôt que le seul indicateur. **Preuve :** pages initiales/profondes sur 5 000/50 000 messages, historique et accès révoqués, budget indicateur ≤4 requêtes et p95 cible ≤200 ms sur le banc de référence.

Précision issue de la revue de spécification du 8 novembre : la liste conserve
les notifications historiques de l’installation selon sa politique actuelle,
même sans preuve personnelle courante. L’indicateur par animation est plus
restrictif et exige cette preuve pour ses deux branches. Optimiser le total
ne doit ni retirer cet historique ni transformer une notification conservée
en droit d’accès à sa destination privée.

### API-06 — P2 : lots, projection détail avant une nouvelle lecture

[animation_locale_api.py](../../../../localeo-backend/app/api/animation_locale_api.py), lignes 3606–3610 : la route de pagination appelle `obtenir` pour vérifier la visibilité, puis charge les lignes de lots. La projection détail a déjà lu la première page pour une dotation libre (`catalogue_animations_publiques.py`, 644–646).

**Correction :** contrôle de visibilité public minimal et autorisé, puis une seule lecture de la page demandée. **Preuve :** nombre SQL, page profonde, dotation libre, non-publication et retrait ; aucune fuite de lots d’une animation inaccessible.

### API-07 — P2 à mesurer : compte des inscrits et recherche commerçants

Deux risques de volumétrie distincts :

- `inscription_ouverte_sql`, dans [parametres_exploitation_repository.py](../../../../localeo-backend/app/infrastructure/persistence/repositories/parametres_exploitation_repository.py), lignes 35–39, contient un `COUNT` corrélé des participants pour le plafond `maxParticipants`. La requête est groupée pour la page, mais un comptage exécuté reste proportionnel aux inscrits. PostgreSQL peut éviter ce sous-plan quand le plafond est absent. **Mesurer sur 0/1 000/10 000 inscrits avec plafond** ; si nécessaire maintenir un compteur transactionnel de même sémantique, sans remplacer par le nombre de participants qualifiés.
- [commercants_live.py](../../../../localeo-backend/app/application/animation_locale/services/commercants_live.py), lignes 51 et 77–90, recherche en sous-chaîne `ILIKE '%terme%'` et trie sur `lower(nom) COLLATE C,id`. Les index trouvés ne couvrent pas nécessairement cette expression et tous les périmètres ; aucun index trigram de cette recherche n’a été trouvé. **Pas de scan lent démontré sur les huit commerces TEST.** Examiner les plans avec/sans recherche et filtres commune/animation ; ajouter un index normalisé/trigram seulement si les mesures le justifient. Ne pas exclure les partenaires établis hors commune organisatrice.

### API-08 — P3 : coût accessoire, payload et illustrations

- La recherche vérifie à chaque requête toute la readiness de la projection : procédures, colonnes, index, contraintes et triggers, dans [planning_catalogue_live_repository.py](../../../../localeo-backend/app/infrastructure/persistence/repositories/planning_catalogue_live_repository.py), lignes 5–35. La capture locale à 10 000/page 50 mesure environ 0,5 ms d’exécution pour cette requête : **ce n’est pas le goulot principal démontré**. Un contrôle au démarrage et un résultat positif à durée courte/invalidable peuvent supprimer un aller-retour, en conservant le refus explicite si la projection est indisponible.
- Les cartes contiennent description, description courte, règles et règlement complet même avec `detail=False` (`catalogue_animations_publiques.py`, 665–710). Les trois cartes TEST représentent environ 7,2 ko. Préférer une projection de carte légère, distincte du détail, après vérification des consommateurs et mesure des octets compressés/rendu.
- [visuel_animation_publique.py](../../../../localeo-backend/app/application/animation_locale/services/visuel_animation_publique.py), lignes 14–26, relit le stockage et contrôle le hash ; la route flyer renvoie `no-store` et accepte jusqu’à 5 Mo. **Médias non chronométrés ici.** Préparer une miniature au dépôt de l’image, puis mesurer octets et temps de stockage. Un éventuel cache interne par hash doit toujours vérifier le droit public actuel et le retrait immédiat ; un cache public long ne convient pas à cette exigence.

## 6. L’orchestration frontend amplifie les délais des API

### LIVE-01 — P1 : carnet exhaustif et relectures au clic

[LiveAnimations.jsx](../../../../localeo-marketplace/src/live/LiveAnimations.jsx), lignes 196–245 : `Promise.all` résout toutes les entrées, chacune par participation puis animation contextualisée, avant de publier la liste. À N entrées résolues, cela peut représenter **2N GET + un dashboard**, hors messages globaux. Le clic refait la résolution ; [LiveAnimationGame.jsx](../../../../localeo-marketplace/src/live/LiveAnimationGame.jsx), lignes 127–149, relit encore la participation au montage.

**Correction :** résumés immédiatement visibles, pagination/revalidation progressive, fiche publique et contextualisation mutualisées par animation sous une même installation, entrée ciblée prioritaire. Chaque projection privée reste attachée à sa participation et à son token : deux participations d’une même animation peuvent avoir des droits et gains distincts. Propager `AbortSignal` jusque dans les méthodes actuellement dépourvues de signal (`api.js`, 537 et 567). Une donnée d’affichage récente ne remplace jamais la validation actuelle d’une action ou d’un QR. **Preuve :** carnets 1/10/50, requête lente parmi les entrées, retour arrière, clic direct et annulation ; nombre d’appels proportionnel aux seules cartes revalidées.

### LIVE-02 — P1 : lots bloqués derrière la liaison des accès

[useLiveRewards.js](../../../../localeo-marketplace/src/live/useLiveRewards.js), lignes 78–129 : jusqu’à 50 accès sont liés avec concurrence 2 avant les GET récompenses/tirages ; les marqueurs de liaison restent locaux au montage du hook. Ensuite `Promise.allSettled` attend les deux sources avant de les publier. L’accueil désactive déjà cette liaison (`linkAccesses:false`) ; « Mes lots » utilise le comportement par défaut.

**Correction :** afficher les suivis déjà associés, lier uniquement les manquants de manière bornée et ne pas bloquer une source réussie sur l’autre. **Preuve :** remontage sans reliaison superflue, carnet de 50, accès supprimé, une source lente ou en échec ; préserver récupération des lots existants et absence de duplication.

### LIVE-03 — P2 : dépendances d’accueil et file sans priorité

Le parcours normal combine **1 configuration → 2 recherches de périodes**, en parallèle de dashboard, récompenses, tirages et messages : **7 GET usuels**, plus éventuellement la création d’installation et la résolution d’une commune partagée. La recherche attend la configuration ([LiveDiscovery.jsx](../../../../localeo-marketplace/src/live/LiveDiscovery.jsx), 236–243). Les lecteurs du hook de capacités mutualisent déjà la configuration 60 s. Réglages (`LiveApp.jsx`, 615) et WebPush (`useLivePush.js`, 63) appellent encore directement l’API : ces parcours peuvent ajouter des lectures non mutualisées.

La file de [api.js](../../../../localeo-marketplace/src/services/api.js), lignes 294–346, accepte 3 lectures simultanées et 40 en attente, sans priorité. Le délai global de 15 s comprend l’attente avant départ. Les lectures secondaires peuvent donc retarder le catalogue ; un `Promise.all` sur 50 entrées peut dépasser cette file avant toute saturation serveur.

**Correction :** conserver les bornes, mais limiter les producteurs, privilégier la configuration/catalogue/détail actif, mutualiser les lecteurs de configuration restants, reporter les lectures personnelles sans installation ou accès connu et distinguer attente en file, HTTP et rendu dans les mesures. Ne pas augmenter arbitrairement la concurrence. Le repli historique peut lancer deux catalogues par commune, jusqu’à 20 pour dix communes : conserver la compatibilité seulement lorsque nécessaire. **Preuve :** premier visiteur, carnet dense, serveur lent et navigation pendant chargement ; aucun rejet évitable par surproduction ni lecture obsolète non annulée.

## 7. Points correctement maîtrisés

La recherche moderne possède une pagination par clé, `LIMIT page_size+1`, sans comptage global du catalogue, et groupe configurations/modèles/dotations. Dashboard, récompenses, tirages et annuaire sont paginés côté serveur ; les préchargements ORM du dashboard évitent déjà plusieurs faux N+1. Les routes auditées sont synchrones FastAPI : aucun SQL synchrone exécuté dans une route `async` n’a été identifié sur ces chemins.

Les recherches publiques et l’annuaire annulent les requêtes obsolètes et bornent leurs fenêtres. La configuration est mutualisée pour les lecteurs du hook de capacités ; le service worker ne met pas en cache les réponses API privées. Les coordonnées d’aide et les QR ont des conditions de chargement spécifiques. Ces protections doivent être conservées.

## 8. Plan de vérification après correction

| Lot | Modification à préparer | Critères de vérification |
| --- | --- | --- |
| A — requêtes évitables | API-01, API-06 ; traces de la fiche API-02 | Même résultat public, requêtes SQL constantes par page, aucune première page de lots lue deux fois ; profil représentatif expliquant la latence de la fiche. |
| B — parcours visible | LIVE-01/02/03 | Cartes visibles chargées en priorité ; aucune résolution exhaustive au démarrage ; pas de triple relecture au clic ni de liaison de 50 accès avant la consultation des lots ; annulation et file bornées. |
| C — personnel et messages | API-03/04/05 | Rafale de GET sans réécriture systématique d’activité ; preuves groupées ; badge par présence non lue ; révocations et secrets toujours contrôlés. |
| D — capacité | Recherche et consultations après A/B/C | Banc isolé de référence ; N=1 000 animations/10 000 participations/50 000 messages et 10N ; cinq minutes à 1 puis 10 lecteurs, recherches fréquentes/rares/vides, écritures 2/s ; saturation 20/40 et retour nominal. Mesurer erreurs, p50/p95/p99, SQL, pool/verrous, CPU/mémoire et payload. |

Conserver les budgets LA-16 : recherche p95 ≤500 ms/p99 ≤1 s et ≤10 requêtes par page ; indicateur messages ≤200/500 ms et ≤4 requêtes ; contact ≤250/600 ms et ≤6 requêtes hors moteur nécessaire ; lieu courant ≤500 ms/1 s. Pour la fiche publique et l’annuaire, fixer un budget HTTP spécifique dans la conception à partir du parcours et du banc de référence : ce rapport n’invente pas un SLO déjà acquis.

Le pool backend est borné et configurable, avec défaut de code 5 connexions + 5 en débordement par processus, attente jusqu’à 30 s. **La configuration TEST n’est pas connue.** Instrumenter attente de pool et nombre de workers avant tout redimensionnement. Corréler les temps avec l’identifiant de requête ; éviter tokens, secrets et données personnelles dans les traces de performance.

## 9. Preuves conservées, contrôles et impacts

Sorties de travail non versionnées : projet `tmp/live-audit-http-measures.json` et réponses publiques `tmp/live-audit-*.json` ; backend `tmp/live-api-audit-20261108/` contenant les deux logs réussis, mesures, plans et script de comptage. Le benchmark historique du 7 novembre a été sauvegardé puis restauré à l’identique ; le résultat du 8 est conservé séparément. Ces artefacts locaux complètent les tableaux de ce rapport, sans devenir une documentation concurrente.

| Contrôle | Résultat |
| --- | --- |
| Échantillon HTTP public TEST | 27/27 réponses 200 ; trois essais par route, sans garantie statistique. |
| Benchmark isolé existant | 1 test réussi ; 3/8 objectifs p95 dépassés, limites ci-dessus. |
| Comptage SQL isolé | 1 test réussi ; N+1 ancien catalogue mesuré. |
| Documentation | Contrôle ciblé : 99 guides, 1 199 liens locaux, aucune erreur ni avertissement ; 148 sources exportées vérifiées ; `git diff --check` réussi. |
| Charge HTTP soutenue, charge mixte, données personnelles TEST, navigateur instrumenté | Non exécutés. |

Seul le dépôt documentaire est modifié par cet audit : rapport et index. Les changements antérieurs du header restent en place. Les quatre applications ne sont pas corrigées, les statuts de roadmap ne changent pas. **Aucune migration SQL, modification de contrat, de règle métier, de générateur ou de configuration n’est nécessaire pour produire ce rapport.** Les propositions futures API-01/05/08 pourront affecter les contrats/consommateurs ; elles devront être spécifiées et vérifiées lors de leur mise en œuvre. Aucun commit, push ni déploiement n’est demandé dans cette étape.
