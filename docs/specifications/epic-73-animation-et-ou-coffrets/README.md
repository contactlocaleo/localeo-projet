# EPIC 73 — Localeo Animation et/ou Coffrets

Spécification détaillée **V1 du 17 octobre 2026**, fondée sur les **147 décisions**, **38 user stories** et **63 critères** du [backlog canonique](../../roadmap/en-cours/epic-73-animation-et-ou-coffrets-backlog.md). Les 18 groupes d’arbitrages produit recensés sont résolus. L’état produit est **En cours** depuis le 18 octobre 2026 selon la [roadmap](../../roadmap/README.md) : ce dossier décrit la cible et le suivi local en précise les preuves, sans annoncer de déploiement.

## Résultat attendu

Vendre et utiliser Animation et Coffrets séparément ou ensemble. Une animation choisit explicitement des coffrets, des lots libres remis hors Localeo ou des bons numériques de lots libres, indivisibles et validables par QR/PIN. Un commerçant reçoit uniquement les fonctions des produits activés et préparés, sans perte des engagements déjà pris. L’organisation cliente dispose d’une équipe, d’une souscription et de modules optionnels, ainsi que des parcours d’assistance, de pilotage et de sortie nécessaires au service.

La conception garde les cinq dépôts indépendants. Les règles sont dans le domaine backend ; ERP, OnBoard, Pro, Animation, Marketplace/Live, Support, Atelier et Ops sont des producteurs ou consommateurs des mêmes décisions. Aucun nouveau dépôt ni nouveau moteur de jeu n’est imposé.

## Lire et réaliser le périmètre

Le [suivi d’implémentation locale](suivi-implementation.md) consigne le plan en dix lots, les preuves, les commits par dépôt et les limites ; aucun push ni déploiement n’est autorisé par la réalisation lancée le 18 octobre.

La [prise en main par lot](prise-en-main-par-lot.md) présente les fonctionnalités,
leurs accès dans les applications et des scénarios pour la future recette.

Le [guide d’exploitation SaaS](../../exploitation/exploitation/exploiter-saas-animation.md)
décrit le pilotage économique, les exports et fermetures, les traitements de
conservation et le contrôle de réouverture après restauration du lot 10.

La [procédure des bons numériques](../../exploitation/exploitation/gerer-bons-numeriques-animation.md)
décrit les configurations préparées, les workers, les reprises et les contrôles
de conservation restant nécessaires avant ouverture.

La [procédure d’import des commerçants](../../exploitation/exploitation/importer-commercants-animation.md)
décrit le parcours livré localement au lot 06, les décisions ERP, le worker et
la conservation des fichiers. Les résultats sont consignés dans le suivi ;
aucun environnement n’a été activé.

La [procédure de préparation accompagnée](../../exploitation/exploitation/preparer-chasse-accompagnee.md)
décrit le suivi ERP/portail, le calendrier, la validation terrain et les alertes
du lot 07. Ses preuves figurent dans le suivi de réalisation.

La [procédure de communication participants](../../exploitation/exploitation/communiquer-participants-animation.md)
décrit les préférences Live, les campagnes, leurs quotas et les alertes du lot 08,
ainsi que les réglages et traitements préparés pour une ouverture ultérieure.

Le [guide des parcours, bilans et support](../../exploitation/exploitation/parcours-plateforme-animation.md)
décrit l'assistant, le site public, les nouvelles éditions, les mesures et les
échanges privés du lot 09, ainsi que leurs reprises historiques bornées.

| Document | Contenu |
| --- | --- |
| [Architecture et contrats](architecture-contrats.md) | Propriétaires, invariants, transactions, producteurs/consommateurs, compatibilité, migrations, conservation et impacts ERP/CRM/Atelier |
| [Dotation et lots](dotation-lots.md) | Trois parcours, modèles/exemplaires, tirages/suppléants, bons, QR/PIN, corrections, emails et refus |
| [Modules, souscriptions, import et communication](modules-souscriptions-import-communication.md) | Catalogue et droits, prix/quotas/prorata, paiement/renouvellement, import avec deltas, campagnes Live/Web Push, coûts/budgets |
| [Périmètres et parcours SaaS](perimetres-parcours-saas.md) | OnBoard/Pro, équipe multi-organisations, site dédié, préparation/support, nouvelle édition, résultats et réversibilité |
| [Vérification et livraison](verification-livraison.md) | Matrice de 63 critères, 12 familles de fixtures, dépendances, migration/pilote, restauration et preuves à produire |

Chaque chapitre distingue l’existant lu dans le code et les nouveaux contrats à implémenter. Les OpenAPI générés existants ne sont pas modifiés pour leur faire annoncer des routes encore absentes. À l’implémentation, mettre à jour producteur, schémas générés et lecteurs ensemble.

## Couverture des user stories

Les CA gardent les identifiants du backlog ; leur matrice de preuve est dans [vérification et livraison](verification-livraison.md). Les lots ci-dessous sont un découpage documentaire, pas un changement de priorité ou de périmètre.

| US | Comportement | Chapitre principal | CA |
| --- | --- | --- | --- |
| E73-US-01 | Produits séparés/combinés | Dotation / architecture | 01, 02, 04, 05 |
| E73-US-02 | Choix et gel de dotation | Dotation | 03, 11 |
| E73-US-03 | Standard et à la carte | Modules | 12–14 |
| E73-US-04 | Lots externes et suivi | Dotation | 06, 08–10, 29 |
| E73-US-05 | Modèles et exemplaires | Dotation | 30 |
| E73-US-06 | Affectation de stock | Dotation | 31 |
| E73-US-07 | Tirage et attribution | Dotation | 07, 32 |
| E73-US-08 | Gain, email et bon | Dotation | 08, 09, 33 |
| E73-US-09 | Remise par QR/PIN | Dotation | 34, 35 |
| E73-US-10 | Cycle et incidents du bon | Dotation | 36 |
| E73-US-11 | Activation/retrait ERP | Périmètres/SaaS | 15, 22 |
| E73-US-12 | Onboarding adapté | Périmètres/SaaS | 16–18 |
| E73-US-13 | Fonctions Pro et salariés | Périmètres/SaaS | 19–21 |
| E73-US-14 | Catalogue et mes modules | Modules | 37 |
| E73-US-15 | Achat de module | Modules | 38 |
| E73-US-16 | Cadeau et essai | Modules | 39 |
| E73-US-17 | Cumul et continuité des droits | Modules | 40, 41 |
| E73-US-18 | Module chasse | Modules / parcours SaaS | 46 |
| E73-US-19 | Aperçu import | Modules | 42 |
| E73-US-20 | Import/deltas/reprise | Modules | 43–45 |
| E73-US-21 | Communication organisateur | Modules | 47, 48 |
| E73-US-22 | Résultats et reprises campagne | Modules | 49 |
| E73-US-23 | Site Animation et liens existants | Périmètres/SaaS | 23, 24 |
| E73-US-24 | ERP/CRM/Support | Architecture / périmètres | 25 |
| E73-US-25 | Récupération et sécurité du compte | Périmètres/SaaS | 50, 51 |
| E73-US-26 | Équipe et organisation | Périmètres/SaaS | 52, 53 |
| E73-US-27 | Souscription autonome | Modules | 54 |
| E73-US-28 | Facturation | Modules | 55 |
| E73-US-29 | Première animation | Périmètres/SaaS | 56 |
| E73-US-30 | Préparation accompagnée | Périmètres/SaaS | 57 |
| E73-US-31 | Aide et support | Périmètres/SaaS | 58 |
| E73-US-32 | Nouvelle édition | Périmètres/SaaS | 59 |
| E73-US-33 | Objectifs et résultats | Périmètres/SaaS | 60 |
| E73-US-34 | Coûts et usages | Modules | 61 |
| E73-US-35 | Export et fermeture | Périmètres/SaaS | 62 |
| E73-US-36 | Reprise des données existantes | Architecture / livraison | 26 |
| E73-US-37 | Démonstration transverse | Vérification/livraison | 27 |
| E73-US-38 | Mise en service et restauration | Vérification/livraison | 28, 63 |

## Décisions structurantes conservées

- Animation : passeport et tombola inclus selon forfait existant ; chasse à la carte avec **5 chasses/an pour 190 € HT**, quota indépendant, prix et quantité proratisés (quantité arrondie au supérieur).
- Import : **49 € HT/an**, sans quota commercial ; XLSX/CSV, **100 lignes et 2 Mo** par fichier, email comme premier rapprochement, conflits explicites et corrections locales protégées. Aucun accès ni invitation automatique.
- Communication organisateur : **49 € HT/an, 5 campagnes/mois civil Europe/Paris**, premier mois complet, sans report ; Live et Push distincts, fréquence par défaut **1 message/participant/commune/24 h**, configurable, alerte à **3 fois** la limite par défaut. Notifications automatiques indépendantes.
- Bons : **90 jours par défaut, 1 à 365 jours**, durée gelée à publication ; prolongation individuelle dans le plafond de 365 jours depuis attribution. Un lot par participant, suppléants et remplacements tracés, ancien bon révoqué.
- Périmètres commerce : ERP uniquement ; saisie/revue **manuelle**, aucune proposition automatique ; prérequis adaptés et continuité limitée des engagements lors du retrait.
- Équipe : responsable/gestionnaire/lecteur, communes et permissions complémentaires explicites ; invitation **7 jours**, récupération **1 heure**, compte existant réutilisé sans doublon.
- Service : préparation chasse accompagnée à distance **5 jours ouvrés**, première réponse humaine support **2 jours ouvrés** ; site `animations.localeo.city` sur socle partagé, reprise des anciens parcours sans imposer le Push.
- Réversibilité : responsable seul, CSV/médias/guide **sans frais sous 5 jours ouvrés**, archive disponible **30 jours**, fermeture accompagnée distincte.
- Reprise : perte maximale cible **4 heures**, rétablissement **8 heures maximum**, exercice avant mise en service puis trimestriel et après modification majeure du dispositif ; preuve manquante ou objectifs échoués bloquent la mise en service concernée.

Les durées de consommation, de validité de secret, de conservation et de disponibilité d’un export ne sont pas interchangeables. Le catalogue initial et les conditions historiques restent distincts ; les cadeaux/essais ne deviennent jamais un achat automatique.

## Préparation de l’implémentation

**Cible initiale confirmée le 18 octobre :** 10 communes, 10 000 participants au total et 10 connexions simultanées (modélisées par 10 utilisateurs actifs dans les tests). Ce sont des hypothèses de dimensionnement à vérifier, pas des quotas commerciaux. **Validation UX : Localeo puis Martignas-sur-Jalle**, première commune pilote, avant extension progressive.

**Attention UX — 18 octobre :** la plateforme organisateur adopte les codes d’une application de gestion ; le site public Animation ceux d’un site de communication et de découverte. Navigation stable, états/action sans ambiguïté, simplicité d’apprentissage et accessibilité clavier/lecteur d’écran/zoom/mobile sont détaillés dans les [parcours SaaS](perimetres-parcours-saas.md). Les six scénarios E73-UX-01 à 06 du plan de vérification doivent être réalisés, avec revue de deux parcours représentatifs avant généralisation des écrans.

Les comportements, domaines, interfaces, migrations et preuves prévues sont détaillés pour les 38 US. Aucun arbitrage produit déjà tranché n’est rouvert par la rédaction. L’implémentation devra matérialiser les contraintes SQL et ports, régénérer les contrats disponibles, compléter les preuves et rattacher les nouvelles données aux catégories de conservation existantes.

Les éléments suivants conditionnent l’activation et non la rédaction : readiness du moteur E55, commune pilote et revue manuelle de ses commerces, reconstitution des conditions historiques, calendrier de service configuré, clés/origines/canaux opérationnels, preuve de restauration hébergée. Une ambiguïté dans les données historiques est signalée et bloque sa migration, sans attribution automatique de droits ni nouvelle décision produit implicite.

## Vérifications de cette version

### Revue de performance du 18 octobre 2026

Revue indépendante de conception et lectures ciblées du backend : cinq lacunes précisées — pagination effective en stockage/index, bilans avec collections complètes, export et capture en mémoire bornée, préparation du tirage proportionnelle à sa population, portée des verrous pendant la continuation de campagne. La [matrice d’accès E73](architecture-contrats.md) indique les formes d’index et les accès attendus ; les scénarios E73-PERF-01 à 08 du plan de vérification séparent croissance des données et croissance du trafic. Les constats sur le code historique ne sont pas des mesures de capacité.

La [convention transverse de performance](../../architecture/transverse/performance-volumetrie.md) devient une règle pour les futures évolutions via le cycle d’epic, le modèle d’architecture, les conventions API et la matrice de revue. Aucun nouveau plafond commercial n’est introduit. Tirage libre et export complet utilisent un traitement durable ; leur progression ne vaut pas confirmation métier. Les plans SQL, budgets de capacité et mesures sur environnement représentatif restent à produire avant activation.

Seconde lecture indépendante après corrections : aucun écart important restant identifié sur ces cinq points. Contrôles documentaires du 18 octobre : `check_guidance.py` sur le dossier et les guides modifiés sans erreur ni alerte, `sync_documentation.py --check-sources` sur 122 documents réussi, `git -c core.safecrlf=false diff --check` réussi. Aucun benchmark, plan `EXPLAIN`, test de charge, migration d’index ou changement applicatif exécuté ; seules les exigences et preuves attendues ont été renforcées dans `localeo-projet`.

### Contrôles de la spécification

Lecture du code local des producteurs/consommateurs et revue indépendante en lecture seule par `localeo-contract-reviewer`, puis intégration des constats : continuité des attributions sur animations publiées, refus atomique d’émission/remplacement lorsque le commerce de remise a perdu son droit, pagination à curseur pour les nouvelles listes, code commun `CONFLIT_VERSION`. Aucun autre écart bloquant identifié par cette revue ; cela ne remplace pas les tests d’implémentation.

Revue DDD complémentaire du 17 octobre par `localeo-invariant-reviewer` : trois imprécisions corrigées — transaction de campagne non bornée, ordre de verrouillage du claim ambigu, propriétaire du disponible remboursable non univoque. L’architecture nomme désormais les racines et leurs limites, les valeurs/politiques pures, les contrats de faits entre domaines et les exceptions transactionnelles. Les campagnes séparent préparation, premier message/débit atomique puis traitement par destinataire ; les remboursements de souscriptions relèvent de `CommandeCommerciale`. Le guide transverse des domaines est aligné sur cette frontière. Les [preuves DDD attendues](verification-livraison.md#preuves-ddd-attendues-à-limplémentation) couvrent ces corrections ; la revue ne certifie pas une implémentation E73.

Contrôles du 17 octobre, arbre documentaire local non committé :

- `scripts/check_guidance.py` sur les six fichiers du dossier, le backlog et les index modifiés : **103 guides, 1 333 liens, aucune erreur ni alerte**.
- `scripts/sync_documentation.py --check-sources` : **122 documents vérifiés** ; aucun contrat runtime généré ni bundle de déploiement publié par cette tâche.
- Comparaison des lignes d’identifiants du backlog et des matrices : **38 US et 63 CA**, ensembles identiques, sans doublon ni omission.
- `git -c core.safecrlf=false diff --check` : réussi.

Après corrections DDD : seconde lecture indépendante sans écart restant identifié sur les trois constats ; `check_guidance.py` sur le dossier et le guide des domaines : **100 guides, 1 124 liens, aucune erreur ni alerte** ; contrôle des sources exportées : **122 documents vérifiés** ; contrôle des espaces du diff réussi. Ces contrôles portent sur la documentation, pas sur la capacité transactionnelle ou la performance des futures implémentations.

Tests applicatifs, migrations, génération/restauration de démonstration, recette navigateur, appels fournisseurs et déploiement E73 : **non exécutés** dans cette tâche de spécification. Seul `localeo-projet` est modifié par ce travail ; les modifications préexistantes du suivi moteur et de `localeo-animation` sont conservées. Le dossier ne constitue aucune preuve de livraison ou de performance hébergée.
