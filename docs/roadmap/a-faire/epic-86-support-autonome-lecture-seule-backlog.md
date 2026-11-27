# EPIC 86 — Support autonome en lecture seule dans Animation et Localeo Pro

## Références et état

- **À faire**, cadrage du **26 novembre 2026**. Identifiant `EPIC-86` vérifié dans la [roadmap commune](../README.md) et les namespaces applicatifs.
- [E76 — Sessions support](../en-cours/epic-76-impersonification-support-pro-animation-backlog.md) porte l’intervention ouverte depuis l’ERP ou Localeo Support. E86 porte le compte nominatif, la connexion autonome depuis Animation et Pro et la consultation du menu complet en lecture seule.
- La spécification s’appuiera sur les [comptes internes E69](../../specifications/epic-69-acces-internes/README.md), les [accès salariés E72](../../specifications/epic-72-acces-salaries/README.md), les [équipes et souscriptions E73](../../specifications/epic-73-animation-et-ou-coffrets/README.md) et l’[adaptateur WebAuthn E83](../../specifications/epic-83-cles-acces-localeo-pro/README.md).

## Problème et résultat attendu

Un agent doit comprendre ce qu’un gestionnaire, un commerçant titulaire ou un salarié voit dans son application pour l’aider à diagnostiquer un blocage. La consultation E76 part de l’ERP ou de Localeo Support et couvre les écrans utiles aux interventions prévues. Le besoin supplémentaire est de se connecter directement aux applications avec une identité support nominative et de parcourir toutes les rubriques autorisées à la personne représentée. [Écrans et opérations E76](../../specifications/epic-76-impersonification-support-pro-animation/README.md#écrans-et-opérations-autorisés)

Par exemple, un administrateur donne la portée Animation à une agente. Elle passe par **Accès support Localeo** depuis la connexion Animation, s’authentifie, choisit le gestionnaire, son organisation et sa commune, puis renseigne un motif. Elle retrouve les rubriques et les modules que voit le gestionnaire dans ce contexte. Le profil support ne figure pas dans l’équipe du client.

## Périmètre et découpage

- Dans l’ERP, gérer le compte nominatif et ses portées **Animation** et **Commerçant** indépendamment. Chaque portée ouvre la recherche de tous les clients éligibles du produit. L’agent sélectionne un seul contexte client à la fois et peut rattacher la consultation à une référence de dossier facultative.
- Depuis les deux applications, ouvrir une page de connexion commune à l’environnement. La connexion exige le mot de passe et une passkey liée au compte, avec vérification de l’utilisateur. La récupération passe par l’administrateur et invalide les clés remplacées et les sessions concernées.
- Afficher le menu complet selon les droits actuels de la personne, y compris les coordonnées qu’elle peut lire. Les vues à risque affichent les états utiles au diagnostic. Les secrets, les exports, la génération de documents et les commandes métier sont refusés. La consultation n’accorde aucun accès aux commandes d’intervention E76.
- Isoler l’authentification, les sessions et les API de consultation. Déclarer les lectures et les champs autorisés pour chaque rubrique. Exécuter les projections en transaction de lecture seule, avec la journalisation sur un chemin distinct. Borner le coût des contrôles de droits et des lectures à la cible et à la page demandées.
- Livrer le socle et une rubrique par produit pour la recette sur TEST, puis couvrir tout le menu. L’activation est distincte par produit et par environnement. La mise en service d’un produit exige sa couverture complète et le respect des budgets mesurés.

## Critères d’acceptation

| Critère | Situation et action | Résultat observable |
| --- | --- | --- |
| E86-CA-01 · Habilitation | Un administrateur crée un compte support, attribue les deux portées ou en retire une. | Chaque portée donne accès à la recherche des clients éligibles du produit correspondant et le serveur refuse le produit non attribué. Le compte ne figure ni dans **Compte et équipe** ni dans **Accès salariés**. |
| E86-CA-02 · Connexion | Un agent ouvre **Accès support Localeo** depuis Animation puis depuis Pro. | Son mot de passe et sa passkey avec vérification utilisateur ouvrent une session dédiée au produit demandé. La même passkey fonctionne dans les deux applications du même environnement. Le mot de passe seul, une preuve refusée ou une clé d’un autre environnement ne donnent pas accès. |
| E86-CA-03 · Cible | L’agent recherche un client, sélectionne un gestionnaire, un titulaire ou un salarié éligible et confirme le motif. | La recherche explicite par référence ou préfixe indexé est paginée par curseur à 25 résultats, sans comptage global. Le serveur vérifie le rattachement, la commune et la souscription applicables. Le bandeau affiche l’agent, la cible et l’échéance. Les identifiants hors du contexte choisi sont refusés. |
| E86-CA-04 · Menu complet | Le support parcourt le menu d’un titulaire, d’un salarié ou d’un gestionnaire avec ses droits et modules. | Chaque rubrique accessible est consultable dans son état courant. Les coordonnées que la cible peut lire sont visibles. Le statut et le montant d’une facture sont consultables. Les secrets, exports, générations de documents et commandes métier restent inaccessibles. |
| E86-CA-05 · Lecture seule | L’agent ouvre une rubrique ou tente une écriture par appel direct. | Aucune lecture ne modifie les données métier, ne consomme un quota client ni ne déclenche un envoi. Le serveur refuse la mutation. Les routes client ordinaires, ERP et d’intervention E76 n’acceptent pas le justificatif de consultation. |
| E86-CA-06 · Fin d’accès | L’agent change de cible, perd un droit ou retrouve un onglet après expiration. | Le changement invalide le contexte précédent et ses réponses tardives. Le retrait s’applique dès le prochain contrôle serveur. La session expire après 30 minutes au maximum ou 15 minutes d’inactivité. Les appels automatiques ne prolongent pas sa durée. |
| E86-CA-07 · Audit | L’agent ouvre une cible, consulte une ressource ou rencontre un refus. | Chaque lecture métier est journalisée durablement avant restitution. Le journal relie l’agent, la cible, le motif, les références, l’horodatage et le résultat. Les coordonnées en clair, les secrets et les contenus sont absents des journaux et des caches. Une panne d’audit bloque la lecture support. |
| E86-CA-08 · Coût ordinaire | Les clients utilisent les applications et installent la PWA avec la fonctionnalité activée. | Les parcours ordinaires n’ajoutent aucun appel HTTP, aucune requête SQL ni aucun chargement de module ou d’asset propre au support. |
| E86-CA-09 · Charge globale | À trafic comparable, mesurer la référence, l’activation sans agent, la charge mixte avec consultation et import E76, puis la saturation et la reprise. | Chaque parcours ordinaire respecte au maximum +5 % de p95 et +10 % de p99, les seuils absolus E59 applicables et moins de 0,5 % d’erreurs inattendues à charge nominale. Au dépassement des plafonds, les requêtes support excédentaires sont refusées. |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Applications et domaine | **Concerné.** Identité/Accès porte l’habilitation, la session et les refus. L’ERP gère le compte. Animation et Pro portent l’entrée, le choix de la cible et les vues de consultation. Live et Marketplace entrent dans la recette de charge des ressources partagées. |
| API et consommateurs | **Concerné.** API Support dédiée pour l’authentification, la recherche, le contexte et les lectures. Le backend produit le [contrat canonique](../../specifications/epic-41-api/openapi.json). L’ERP et les deux applications consomment les opérations qui les concernent. Synchroniser les contrats embarqués. |
| Persistance | **Concernée.** Migrations additives pour les portées, les clés, les sessions et leur audit. Conserver la compatibilité avec les comptes et sessions existants. Appliquer la [conservation T8](../../specifications/identite-acces/conservation-validations-acces.md) au journal et vérifier la purge. |
| Démonstration et fixtures | **Concernées.** Prévoir les portées Animation, Pro et cumulées, plusieurs organisations et communes, les titulaires, les salariés et des droits différents. Les jeux générés ne créent aucune session support active. |
| Documentation | **Concernée.** Compléter l’[aide ERP et Support](../../exploitation/exploitation/localeo-support.md). Vérifier les sections Connexion des guides [Animation](../../produit/formation/animation/guide-quotidien-animation.md) et [Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md). Si le parcours client visible évolue, actualiser les sources, captures, PDF et copies embarquées selon la [procédure](../../organisation/maintenance-guides-utilisateurs.md). |
| Exploitation | **Concernée.** Documenter les origines HTTPS, l’enrôlement, la récupération, la révocation et le suivi du journal. Vérifier sur TEST la bascule d’arrêt qui invalide les sessions de consultation. |
| Performance | **Concernée.** Charger les vues à la demande, isoler les connexions SQL de consultation et limiter l’admission avant les traitements coûteux. Vérifier les recherches, lectures et purges à N puis 10N. Le pilote part de 2 requêtes simultanées par agent, 4 par environnement et 5 requêtes support par seconde pour l’environnement. Suivre latences, erreurs, attentes SQL et coût d’audit. [Convention transverse](../../architecture/transverse/performance-volumetrie.md) · [Seuils E59](../../specifications/epic-59-tests-performance-api/conception-technique.md#7-seuils-initiaux) |

## Passage à la spécification

Inventorier les rubriques et opérations de lecture par produit et par rôle. Vérifier la parité d’affichage, les lectures qui provoquent aujourd’hui une écriture, la disponibilité de l’audit et les refus pendant un changement de cible ou de droits. Définir les origines de connexion, les contrats et le budget de connexions pour les instances de chaque environnement. [Cycle d’epic](../../organisation/cycle-epic.md#spécifier)

Un essai local E76 en charge mixte avec un import délégué a mesuré **+6,67 % au p95** pour une lecture Animation ordinaire. La recette E86 doit mesurer l’impact sur Animation, Pro, ERP, Live, Marketplace et les traitements qui partagent le backend avant activation en production. [Bilan E76](../../specifications/epic-76-impersonification-support-pro-animation/verification-livraison.md#charge-et-conditions-dactivation)
