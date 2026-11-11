# EPIC 73 — Localeo Animation et/ou Coffrets

Évolution du **11 novembre 2026 — E73-EVO-DYNAMISME-COMMUNE** : profil visuel
de l'activité de l'organisation dans la commune active, quatre indicateurs
et tendances sur douze mois, **sans note globale**. Les
[critères DY-01 à DY-06](perimetres-parcours-saas.md#évolution-du-11-novembre-2026--dynamisme-de-la-commune)
portent le choix utilisateur et ses limites ; preuves propres au bilan de
livraison. La clôture historique de l'epic est conservée.

Évolution du **11 novembre 2026 — E73-EVO-FIN-ARCHIVES** : fin explicite après
traitement des lots, gel de la gestion puis archivage consultable dans
**Animations → Mes archives**. La [spécification](fin-animation-archives.md)
porte les arbitrages utilisateur et les critères FA-01 à FA-09 ; implémentation
et vérifications locales réalisées, avec preuves et limites dans son suivi. La clôture historique de l'epic reste inchangée.

Correctif du **11 novembre 2026 — lots annoncés dans Live** : résumé visible
dans le carnet et la participation, détail volontaire **Les lots à gagner**,
en remplacement du bilan de parcours redondant. Les
[critères LDOT](localeo-live-entree-unique.md#correctif-du-11-novembre-2026--lots-annoncés-dans-le-carnet)
distinguent dotation prévue, gains personnels et données indisponibles.

Évolution du **11 novembre 2026 — E73-EVO-LIVE-DOMAINE** : un service et un
build Marketplace communs aux domaines Coffrets et Live. Le Static Site est
conservé : le navigateur reconnaît l'origine du template public et ouvre
`/live/carnet` depuis `/`. La redirection serveur Node reste facultative. Les
[critères LD-01 à LD-08](localeo-live-entree-unique.md#évolution-du-11-novembre-2026--entrée-live-par-domaine-e73-evo-live-domaine)
remplacent l'obligation antérieure de deux services publics ; aucune migration
ou rétrocompatibilité historique exigée, conformément à la précision utilisateur.
Clôture historique E73 inchangée ; preuves propres au bilan.

Correctif du **11 novembre 2026 — création, envoi et suivi des messages** :
Localeo Animation distingue le brouillon, la confirmation de mise en file et
la publication dans Live. Les deux traitements existants sont raccordés à
l'ordonnanceur et à la supervision des batchs ; le transport Push reste suivi
séparément. Parcours dans la [spécification de communication](modules-souscriptions-import-communication.md),
configuration dans le [guide d'exploitation](../../exploitation/exploitation/communiquer-participants-animation.md)
et preuves dans le [bilan de livraison](verification-livraison.md).

Correctif du **11 novembre 2026 — avancement homogène** : les détails de
passeport, chasse et tombola utilisent le même suivi visuel de l'inscription
au résultat. La [précision de LS-02](localeo-live-entree-unique.md#correctif-du-11-novembre-2026--avancement-homogène-des-animations)
remplace le bloc textuel de qualification ; visites tamponnées, défis et
états backend conservés. Preuves dans le [bilan de livraison](verification-livraison.md).

Correctif du **11 novembre 2026 — E73-COR-MESSAGES-ANIMATION** : le choix
**Animations** des réglages Live autorise les messages des organisateurs pour
les participations personnellement liées. Aucun accord par animation ; le Push
requiert en plus les alertes de cet appareil. Les critères MA-01 à MA-06 sont
décrits dans la [spécification des modules et de la communication](modules-souscriptions-import-communication.md).
Migration et preuves dans le [bilan de livraison](verification-livraison.md).

Évolution du **11 novembre 2026 — E73-EVO-HABILITATIONS-ERP** : consultation
et modification motivée des habilitations Animation, par utilisateur et
organisation, depuis l’ERP. Les [critères HA-01 à HA-07](perimetres-parcours-saas.md#évolution-du-11-novembre-2026--e73-evo-habilitations-erp)
préservent droits historiques, dernier responsable et séparation des modules
commerciaux. Spécification et implémentation vérifiées localement ; preuves et
limites dans le [bilan de livraison](verification-livraison.md).

Évolution du **11 novembre 2026 — E73-EVO-MODULES-ERP-UX** : simplification de
la gestion des modules d’une souscription dans l’ERP, avec accès depuis
Supervision technique. Les [critères MU-01 à MU-06](modules-souscriptions-import-communication.md#évolution-du-11-novembre-2026--e73-evo-modules-erp-ux)
conservent les conditions acquises et commandes commerciales existantes.
Spécification et implémentation vérifiées localement ; preuves et limites dans
le [bilan](verification-livraison.md#évolution--e73-evo-modules-erp-ux-11-novembre-2026).

Évolution du **10 novembre 2026 — E73-EVO-LIVE-PARTICIPATION** : les huit lots
acceptés après l'audit des parcours sont spécifiés dans les
[critères PA](localeo-live-entree-unique.md#évolution-du-10-novembre-2026--participation-e73-evo-live-participation)
et la [conception §15](localeo-live-adhesion-conception.md#15-participation--e73-evo-live-participation).
Les huit lots sont spécifiés, implémentés, vérifiés localement et commités les
10–11 novembre ; versions, preuves et procédure de livraison dans le
[bilan](verification-livraison.md#évolution--e73-evo-live-participation-10-novembre-2026).
PM-R06 est corrigé localement au lot 5. Clôture historique conservée ; recette
humaine et hébergée préparées, réserves LA-16/LP suivies, aucun push/déploiement.


Évolution du **10 novembre 2026 — E73-EVO-LIVE-ICONOGRAPHIE** : dix
[critères IA](localeo-live-entree-unique.md#évolution-du-10-novembre-2026--iconographie-et-respiration-e73-evo-live-iconographie)
et [conception §14](localeo-live-adhesion-conception.md#14-iconographie-et-respiration--e73-evo-live-iconographie)
pour appliquer l'audit d'iconographie et d'espacement. Spécification et réalisation
locale effectuées ; principes UX complétés, résultats et limites propres au
[bilan IA](verification-livraison.md#évolution--e73-evo-live-iconographie-10-novembre-2026).
L'epic garde sa clôture historique et ses autres réserves.

Évolution du **10 novembre 2026 — E73-EVO-LIVE-PARCOURS-MOBILE** : les neuf
constats du dernier audit sont reliés aux [critères PM-01 à PM-09](localeo-live-entree-unique.md#évolution-du-10-novembre-2026--parcours-mobiles-e73-evo-live-parcours-mobile),
à la [conception §13](localeo-live-adhesion-conception.md#13-parcours-mobiles--e73-evo-live-parcours-mobile)
et au [bilan PM](verification-livraison.md#évolution--e73-evo-live-parcours-mobile-10-novembre-2026).
Corrections déjà poussées dans Marketplace `b9fb30d` ; présente phase documentaire.
Le bilan historique relevait un correctif P1 sur la revalidation des
participations, corrigé et vérifié depuis par le lot 5 PA ci-dessus. Il distingue
toujours preuves locales et recettes restantes. Clôture historique conservée,
évolution non déclarée terminée et déploiement non attesté.

Évolution du **9 novembre 2026 — E73-EVO-LIVE-CARNET** : les cinq sections du
PDF sur le carnet unifié sont traduites en **17 critères CN-01 à 17**, avec
trois priorités et deux décisions produit résolues : téléphone obligatoire
classique conservé, récupération vérifiée des participations et lots associés. La
[spécification Live](localeo-live-entree-unique.md#évolution-du-9-novembre-2026--carnet-personnel-unifié-e73-evo-live-carnet)
et la [conception §10](localeo-live-adhesion-conception.md#10-carnet-personnel-unifié--e73-evo-live-carnet)
décrivent navigation, droits, état des objets, téléphone et récupération.
Spécification puis implémentation demandées ; résultats propres au
[bilan](verification-livraison.md). Clôture historique et réserves conservées.

Évolution du **9 novembre 2026 — E73-EVO-LIVE-FICHE** : les douze axes de
l’audit visuel sont spécifiés en **12 critères E73-FD-01 à 12** dans la
[spécification Live](localeo-live-entree-unique.md#évolution-du-9-novembre-2026--fiche-animation-immersive-e73-evo-live-fiche).
La [conception §9](localeo-live-adhesion-conception.md#9-fiche-animation-immersive--e73-evo-live-fiche)
décrit la fiche de défi, les conditions visibles avant inscription, les accès
ciblés, les états et la recette mobile/bureau. **Réalisation locale Marketplace/Live**, sans
nouvelle règle, API ou migration ; résultats et limites consignés au
[bilan](verification-livraison.md). La réserve LA-16 et les évolutions précédentes
restent distinctes.

Évolution du **8 novembre 2026 — E73-EVO-LIVE-HIERARCHIE** : les huit points
de l’audit après déploiement sont spécifiés en **12 critères LH-01 à LH-12**.
La [spécification fonctionnelle](localeo-live-entree-unique.md#évolution-du-8-novembre-2026--hiérarchie-et-fluidité-e73-evo-live-hierarchie)
et la [conception §7](localeo-live-adhesion-conception.md#7-hiérarchie-et-fluidité--e73-evo-live-hierarchie)
couvrent sections, chargement, commerçants, cartes, identité graphique, états
vides et transitions. **Implémentation locale dans Marketplace/Live**, sans
migration identifiée ; les [preuves et limites](verification-livraison.md)
distinguent les nouveaux résultats des preuves historiques. La réserve de
charge LA-16 reste ouverte et aucun déploiement de ce complément n’est attesté.

Évolution du **7 novembre 2026 — E73-EVO-LIVE-ADHESION** : les 13 recommandations
de l’audit habitant sont intégrées en trois lots et **17 critères E73-LA-01 à 17**.
La [spécification Live](localeo-live-entree-unique.md#évolution-du-7-novembre-2026--adhésion-habitant-e73-evo-live-adhesion)
décrit parcours, invariants conservés, impacts et tests à produire. La
[conception détaillée](localeo-live-adhesion-conception.md) fixe les contrats,
permissions, migrations, budgets et scénarios de recette des 13 recommandations.
Les trois lots sont implémentés localement ; résultats et qualification de
performance LA-16 encore partielle sont consignés dans le
[bilan](verification-livraison.md#réalisation-locale-de-lévolution).
Cette évolution n’est pas déclarée terminée ni déployée. La clôture
historique ci-dessous est conservée.

Décision du **1er novembre 2026 — E73-DEC-CLOTURE-TESTS** : la clôture de
développement repose sur les tests exécutés. Pilote, validation humaine,
bascule des domaines et exercice hébergé restent suivis comme prérequis
d’activation, sans bloquer cette clôture. Le [bilan](verification-livraison.md)
distingue les preuves techniques de ces actions non exécutées ; les anciens
résultats de recette ne sont pas requalifiés.

Évolution du **1er novembre 2026 — E73-EVO-ONBOARDING-ANIMATION-SIMPLE** :
choix Animation/Coffrets dès le référencement et parcours Animation court,
sans contrat, Stripe ni rendez-vous imposés. Les
[critères OA-01 à OA-04](perimetres-parcours-saas.md) précisent CA-16/17/18 ;
les preuves et limites sont consignées dans le [suivi](suivi-implementation.md).

Évolution du **30 octobre 2026 — E73-EVO-LIVE-UNIQUE** : Localeo Live devient
l'entrée publique unique à `animations.localeo.city`, avec découverte multi-communes,
mes participations et mes communes, en priorité mobile. L'ancienne surface
marketplace Animation est remplacée avec reprise volontaire du carnet et maintien
des anciens accès. Aucun nouveau compte habitant. Les
[douze critères et impacts](localeo-live-entree-unique.md) remplacent les attentes
d'interface publique des évolutions ci-dessous, sans changer leurs preuves historiques.

Retours UX du **30 octobre 2026 — E73-EVO-UX-PUBLIC** : géolocalisation
volontaire, identité commune aux Coffrets et carnet Live adapté à la surface
Animation. L’[analyse des parcours](perimetres-parcours-saas.md) distingue les
corrections locales des propositions d’immersion et de simplification à suivre.

Évolution acceptée du **30 octobre 2026 — E73-EVO-DOMAINES** : site public
`animations.localeo.city`, gestion organisateur `gestion-animations.localeo.city`,
marketplace Coffrets sur un service distinct. Les équivalents TEST, critères,
compatibilité et déploiements sont précisés dans
[les origines des parcours](perimetres-parcours-saas.md#54-origines-et-continuité-des-parcours)
et le [guide de configuration](../../exploitation/technique/configurer-epic-73.md).

Spécification détaillée **V1 du 17 octobre 2026**, fondée sur les **147 décisions**, **38 user stories** et **63 critères** du [backlog canonique](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md). Les 18 groupes d’arbitrages produit recensés sont résolus. L’état produit est **Terminée le 1er novembre 2026** selon la [roadmap](../../roadmap/README.md), après vérification technique des critères et extensions conformément à E73-DEC-CLOTURE-TESTS. Le [bilan](verification-livraison.md) distingue tests exécutés, preuves réutilisées et actions d’activation ; aucun déploiement n’est attesté par cette clôture.

## Résultat attendu

Vendre et utiliser Animation et Coffrets séparément ou ensemble. Une animation choisit explicitement des coffrets, des lots libres remis hors Localeo ou des bons numériques de lots libres, indivisibles et validables par QR/PIN. Un commerçant reçoit uniquement les fonctions des produits activés et préparés, sans perte des engagements déjà pris. L’organisation cliente dispose d’une équipe, d’une souscription et de modules optionnels, ainsi que des parcours d’assistance, de pilotage et de sortie nécessaires au service.

La conception garde les cinq dépôts indépendants. Les règles sont dans le domaine backend ; ERP, OnBoard, Pro, Animation, Marketplace/Live, Support, Atelier et Ops sont des producteurs ou consommateurs des mêmes décisions. Aucun nouveau dépôt ni nouveau moteur de jeu n’est imposé.

## Lire et réaliser le périmètre

L’[évolution performance des lectures Live](localeo-live-entree-unique.md#évolution-du-8-novembre-2026--performance-des-lectures-live-e73-evo-live-performance)
du 8 novembre spécifie les constats de l’audit API en **18 critères LP**.
La [conception §8](localeo-live-adhesion-conception.md#8-performance-des-lectures--e73-evo-live-performance)
fixe les contrats de lecture allégée compatibles, l’orchestration du carnet,
les bornes SQL/HTTP et la campagne isolée. Cette phase ne les implémente pas et
ne ferme pas la réserve LA-16 ; les mesures et preuves restent au bilan.

L'[évolution des flyers du 22 octobre 2026](flyers-contextualises.md) ajoute la
contextualisation selon la dotation, les nombres de lots et de commerçants
confirmés, ainsi qu'une illustration personnalisable propre au flyer
(E73-CA-FLYER-01 à 05).

Le [suivi d’implémentation locale](suivi-implementation.md) consigne le plan en dix lots, les preuves, les commits par dépôt et les limites ; aucun push ni déploiement n’est autorisé par la réalisation lancée le 18 octobre.

La [prise en main par lot](prise-en-main-par-lot.md) présente les fonctionnalités,
leurs accès dans les applications et des scénarios pour la future recette.

Le [plan de recette métier par fonctionnalité](recette-metier.md) propose 25 fiches
avec objectif, accès, prérequis, actions et résultats attendus, ainsi qu’une
traçabilité des 38 US et 63 critères. Les tests restent à exécuter et à consigner.

Le [guide d’exploitation SaaS](../../exploitation/exploitation/exploiter-saas-animation.md)
décrit le pilotage économique, les exports et fermetures, les traitements de
conservation et le contrôle de réouverture après restauration du lot 10.

Le [guide de configuration E73 par application](../../exploitation/technique/configurer-epic-73.md)
détaille les nouvelles clés, les réglages existants à réutiliser, les exemples de
valeurs, les traitements à programmer et les vérifications avant ouverture.

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
| [Adhésion habitant Live — conception](localeo-live-adhesion-conception.md) | 13 recommandations, contrats cibles, permissions, migration contact public, performance et tests des 17 critères LA |
| [Performance des lectures Live — conception §8](localeo-live-adhesion-conception.md#8-performance-des-lectures--e73-evo-live-performance) | Audit API-01 à 08 et LIVE-01 à 03, 18 critères LP, variantes de contrat, SQL/chargement bornés, médias, diagnostics et preuves de capacité à produire |
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
