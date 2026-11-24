# Sessions support Pro et Animation — réalisation du 23 novembre 2026

## Périmètre et activation

Les quatre dépôts concernés sont le backend, qui sert aussi l’ERP et Localeo Support, Animation, Pro et la documentation transverse. Marketplace et Live ne consomment aucune commande de délégation.

1. Appliquer dans cet ordre les migrations additives `v332_sessions_support.sql` et `v333_imports_delegues.sql`. La première crée les sessions et leur journal, la seconde la provenance des imports. Les lots ordinaires existants conservent une provenance support nulle.
2. Livrer le backend et les deux consommateurs compatibles. Configurer les origines HTTPS d’ERP, d’Animation et de Pro pour le même environnement. Le backend résout ces origines avec `LOCALEO_ERP_URL`, `LOCALEO_ANIMATION_PORTAIL_URL` et `LOCALEO_FRONT_COMMERCANT_ANIMATION_INVITATION_URL_TEMPLATE`. Les cookies dédiés sont sécurisés et SameSite Strict. Prévoir des origines du même site pour les déploiements utilisant ces cookies.
3. Pour la recette, définir `LOCALEO_SESSIONS_SUPPORT_ENABLED=true` dans les trois TARGET. Le backend lit la valeur au démarrage. Animation et Pro la lisent pendant leur compilation pour afficher **Interventions de Localeo**. L’import conserve son activation E73 et son worker habituel. Les valeurs par défaut désactivent le parcours.
4. Pour arrêter une intervention ou un import délégué en cours, révoquer la session dans le journal ERP. Pour désactiver l’ensemble du parcours, retirer les activations et relivrer les services concernés. Conserver les migrations et les traces pendant leur durée réglementaire.

## Preuves locales

Pour E76-CA-18, les trois builds Animation vérifient que le module d’historique est inclus avec `LOCALEO_SESSIONS_SUPPORT_ENABLED=true` et exclu avec `false` ou lorsque la clé est absente. La recette Chromium avec une API simulée vérifie **Interventions de Localeo** et **Voir le lot** à 390 et 1 024 px.

| Critères | Contrôles et résultats |
| --- | --- |
| CA-01, 02, 03, 04, 09, 12, 13 | Le test navigateur ERP exerce le choix explicite entre deux comptes et la confirmation à 390 et 1 280 px. Les tests de domaine, de transport et PostgreSQL couvrent la réauthentification, le code à usage unique, la consultation initiale, l’expiration et la perte du rôle Backoffice. |
| CA-05, 06, 08, 10 | Les essais PostgreSQL couvrent la consultation d’une page Pro sans création, son brouillon puis sa modération avec attribution, la création/modification d’un brouillon d’actualité et le refus de programmation. Le test de révocation couvre le refus hors commune. |
| CA-07, 10, 11 | Recette Chromium sur les builds locaux, API simulées. Animation traite 20 puis 100 lignes et récupère le reçu après interruption réseau. Pro conserve le brouillon après échec de soumission. Rechargement, mode, clavier et retour ERP sont exercés. |
| CA-10, 14, 16 | Essais séparés avec le moteur E73 et PostgreSQL 18 isolé. Fichiers de 20 et 100 lignes intégralement traités. Un lot poursuit son traitement après sortie puis suspend les lignes restantes après révocation. Sa reprise porte l’attribution de la nouvelle commande. |
| CA-14, 15, 17 | Tests de journalisation après annulation, filtrage de la projection client et suppression en cascade après purge des événements internes. L’historique lit les compteurs actuels du lot depuis Référencement. |
| CA-18 | Contrats, générateur, restauration et charge sont suivis ci-dessous. L’activation sur un environnement partagé relève de la livraison. |

Les preuves navigateur utilisent des réponses simulées, les preuves du worker et des transitions éditoriales une base locale jetable. La recette connectée sur TEST doit vérifier ensemble les origines réelles, les cookies, la session ERP, les deux onglets et le worker du déploiement.

### Contrats, guides et non-régression

Les trois exports OpenAPI contiennent les mêmes 33 routes E76, sur 1 267 routes par contrat. Le sélecteur `X-Support-Onglet` est obligatoire après l’échange. Les 1 234 routes du contrat antérieur et leurs schémas existants conservent leur description fonctionnelle.

Les guides Animation et Commerçant comportent les captures de l’historique, avec leur source, leurs PDF et leurs copies embarquées. Les 31 pages ont été rendues et relues. Les liens vers les PDF ont été exercés dans les deux interfaces. Le test PWA Animation couvre cinq largeurs de 320 à 1 280 px et l’absence des assets support du précache ordinaire.

Les 142 contrôles ciblés d’édition, de domaine, d’API, de transport et de plafonds HTTP ont réussi. La campagne générale backend domaine/architecture a produit 3 610 succès, sept tests ignorés et un échec sur l’accent de « Passeport commerçant ». Le même échec a été reproduit sur la révision de référence `282a9dbe`. La première suite générale Pro a produit 737 succès sur 740. Les deux suites concernées ont donné 30 succès sur 30 après correction et relance ciblée.

La campagne import compte 49 succès (7 scénarios délégués PostgreSQL, 21 contrôles API et 21 de domaine), suivis de 16 succès sur le moteur natif PostgreSQL. Les plafonds à 101 lignes et 2 000 001 octets, les demandes sensibles soumises à l’ERP, les dépôts interrompus et le gel d’une purge ont été exercés. Les migrations et leur rejeu suivis d’une restauration des équipes ont réussi dans une base locale initialement vide.

La dernière passe sessions, édition, historique et conservation compte 20 succès. Un second gestionnaire retrouve les compteurs 31 jours après la fin de session. Le retrait de son habilitation masque les opérations et la limite des 180 jours est vérifiée à la seconde. Un incident de projection est visible côté ERP et la relecture aboutit après rétablissement. Quatre tests des comptes de démonstration ont réussi, dont la génération complète sur le schéma migré et la restauration des accès. Le jeu produit contient zéro session support et zéro événement d’intervention.

### Charge et conditions d’activation

Le build initial Animation charge 13 fichiers JavaScript dans les trois cas. Leur taille gzip est de 269 672 octets sur la référence, 270 031 octets avec l’historique désactivé et 270 138 octets avec l’historique activé. L’écart maximal mesuré est de 466 octets. Le code d’intervention est chargé à l’entrée du parcours.

Le banc backend `scripts/performance/mesurer_sessions_support.py` mesure une lecture Animation authentifiée sur PostgreSQL local. Il compte 11 requêtes SQL dans le parcours ordinaire, dont zéro requête de support. Sur la version modifiée, en alternant les configurations sur la même machine, le p95 passe de 26,97 à 26,55 ms au repos et de 52,76 à 55,34 ms pendant un import. Le worker traite 4,25 lignes/s en mode ordinaire et 4,22 lignes/s en délégation sur cette passe. La première comparaison entre révisions, exécutée en concurrence avec d’autres validations, a dépassé +5 %. La campagne interversions reste nécessaire avant activation en production.

Une répétition dans le même répertoire local a dépassé le seuil en charge mixte. Sous le même import délégué, les lectures ordinaires alternées passent de 62,36 à 66,52 ms au p95 avec le support activé (**+6,67 %**). Au repos, elles passent de 28,30 à 29,22 ms (+3,25 %). Le témoin interversions sous import natif mesure 27,05 ms sur la référence et 27,18 ms sur E76. Le débit de l’import délégué est de 3,90 lignes/s sur cette passe, contre 6,85 lignes/s pour le natif, sans attente de verrou sur les 14 échantillons actifs observés. La variabilité des deux passes empêche de garantir le budget de charge. **Conserver l’activation PROD bloquée** jusqu’à la qualification en environnement représentatif.

Pour dix résultats sur 2 000 cibles, la recherche globale Animation de Localeo Support a d’abord lu 16 041 blocs PostgreSQL en 16,66 ms. Filtrer les rattachements avant les jointures ramène ce chiffre à 160 blocs et 3,73 ms. L’optimisation reste dans la recherche déléguée. Depuis une fiche, la recherche conserve son filtre sur le rattachement (1,22 ms sur ce jeu). Entre 200 et 2 000 entrées, le journal passe de 0,16 à 0,22 ms et l’historique de 0,55 à 2,30 ms selon les plans SQL locaux. Ces mesures portent sur les requêtes en base.

## Exploitation et conservation

Dans **Localeo Support → Accès client**, le journal administrateur permet de filtrer par opérateur, compte, session et période. Vérifier le mode et le dernier résultat avant de révoquer. Une révocation s’applique aussi aux lots engagés dont la session interactive est déjà terminée. Le gestionnaire autorisé peut ouvrir **Interventions de Localeo → Voir le lot**. En cas de réponse incertaine à une commande d’import, relire le reçu avant de la soumettre de nouveau.

L’historique est reconstruit à la lecture. Actualiser cette vue relit les traces et le suivi du lot. Les motifs internes restent réservés au journal d’administration. Le récapitulatif client est visible pendant 180 jours après la fin de session. Les pièces détaillées suivent les 30 jours du lot terminal. Le journal interne suit la [conservation T8](../identite-acces/conservation-validations-acces.md) et ses procédures de gel. Confirmer l’inscription de la projection client dans le registre avant PROD.

En cas d’échec de la projection, rechercher `historique.indisponible` dans le journal ERP. Si la base ne peut pas recevoir l’événement, le backend le signale dans son journal applicatif. Le bouton **Réessayer** du compte concerné reconstruit la vue à partir des faits déjà validés.

## Évolution du 24 novembre 2026 — Fiches Animation et édition des brouillons

Les vérifications locales portent sur les arbres de travail issus de Backend `57f8df5a`, Animation `77e2db2` et Projet `371cee8`.

| Critères | Preuves locales |
| --- | --- |
| E76-CA-06, 08, 09, 10, 14 | 22 tests ciblés au total avec PostgreSQL 18 jetable. Le test des fiches lit les huit statuts, vérifie le périmètre de la session et l’absence de transition lors de la lecture d’une animation publiée. Le PATCH refuse le mode Consultation, un droit absent dans le rôle ou l’habilitation communale, les autres statuts, un champ de publication, une version obsolète et le changement de corps lors d’un rejeu. La commande nominale persiste une seule nouvelle version et un seul succès dans le journal. |
| E76-CA-01, 07, 09, 10, 12, 17 | Recettes Chromium ERP et Animation à 390 et 1 280 px sur des API simulées. L’opérateur retrouve une archive, conserve sa recherche en passant en intervention, relit un conflit, enregistre la correction du brouillon puis retourne à l’ERP. Le scénario du guide vérifie la visibilité de l’intervention personnelle et l’accès au PDF à 390 et 1 024 px. |
| E76-CA-18 | 782 contrôles Backend d’architecture, de domaine et de couverture. TypeScript, lint, build et 430 tests Animation réussis. Les 27 chemins sous `/protected/sessions-support/` et leurs schémas concordent dans les exports canonique et embarqué. |

L’évolution utilise les statuts, configurations et traces E76 existants. Elle ne requiert aucune migration ni adaptation des données de démonstration. Le guide Animation, son PDF et sa copie embarquée décrivent l’historique. Le parcours Pro garde ses opérations existantes. La recette sur un environnement livré et la mesure de charge restent à faire.
