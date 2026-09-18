# Audit fonctionnel, opérationnel et UX du BackOffice Localeo

Date de l'audit : 21 août 2026  
Périmètre : backoffice présent dans `app/infrastructure/admin`, services métier associés, modèles persistés et tests automatisés.

## Limites de l'audit

L'URL et les identifiants de test fournis dans la demande sont des placeholders. L'audit est donc fondé sur une exploration exhaustive du code du backoffice, de ses routes, vues, actions, règles métier et tests ; il ne constitue pas une recette visuelle sur une instance déployée avec des données représentatives.

Les constats UX qui dépendent du volume réel, des temps de réponse, du rendu mobile ou de la qualité des données doivent être confirmés par une recette de préproduction. Aucune donnée et aucune opération financière n'ont été modifiées.

## Synthèse et notation

| Domaine | Note |
| --- | ---: |
| Pilotage activité | 6/10 |
| Gestion quotidienne | 7/10 |
| Gestion clients | 8/10 |
| Gestion commerçants | 8/10 |
| Gestion commandes/coffrets | 8/10 |
| Gestion financière | 7/10 |
| Gestion incidents | 7/10 |
| Recherche / navigation | 7/10 |
| Traçabilité / audit | 6/10 |
| Multi-territoires | 4/10 |
| UX BackOffice | 7/10 |
| Préparation globale à la PROD | 6/10 |

## Verdict : NO GO PROD en l'état

Le backoffice permet déjà de traiter une grande partie de l'activité réelle : visions 360 client, commerçant, coffret et reversements, recherche par références, réconciliation des paiements, renvoi des communications, remboursement encadré, contrôle Stripe Connect, expiration, support et alertes opérationnelles.

Le NO GO ne vient donc pas d'un manque général de fonctionnalités. Il vient de trois contrôles de production à corriger :

1. plusieurs objets transactionnels ou financiers sont encore modifiables, voire supprimables, par le CRUD SQLAdmin générique ;
2. l'audit générique enregistre l'acteur et l'opération, mais pas systématiquement l'avant, l'après et le motif ;
3. la conformité du schéma de base n'est pas garantie au démarrage, comme l'ont montré les colonnes Localeo Live absentes sur une base historique.

Une fois ces trois points sécurisés et une recette de préproduction menée, le verdict peut devenir **GO PROD AVEC CORRECTIONS** sans refonte du backoffice.

### Hypothèse d'exploitation retenue

Au lancement, le backoffice sera utilisé par un seul opérateur : le fondateur de Localeo, avec le rôle administrateur. Il n'est donc pas nécessaire de mettre en place avant le lancement une gestion multi-utilisateurs, une matrice RBAC Admin/Finance/Support/Exploitation ou un fournisseur OIDC. Le compte configuré doit toutefois rester strictement personnel, protégé par un secret fort et renouvelable, et ne jamais être partagé avec un prestataire ou un second opérateur.

## Forces constatées

- Un dashboard opérationnel distingue les alertes des statistiques et fournit des accès directs aux listes concernées.
- La Vision 360 client relie achats, coffrets, prestations, remboursements, communications, support et documents.
- La Vision 360 commerçant relie catalogue, validations, activité financière, reversements, anomalies et audit.
- La Vision 360 reversements expose les montants dus, transférés, restants, les commissions, les frais PSP et les incohérences de source.
- Les achats non confirmés disposent d'une action métier de réconciliation Stripe.
- Les remboursements sont encadrés par les contraintes pré/post-transfert.
- Les coffrets achetés disposent d'actions de renvoi d'email, régénération du QR et gestion du lien de consultation.
- Le référencement commerçant contrôle les dépendances actives et l'état Stripe Connect.
- Les prestations sont versionnées, ce qui protège mieux les coffrets déjà vendus lors d'une évolution du catalogue.
- Les flux email, SMS et WebPush disposent d'écrans d'exploitation distincts.

## Audit par rôle

### Administrateur Localeo

L'administrateur dispose d'une couverture large du référentiel, du catalogue, des achats, des instances, des reversements, du support et des communications. Le dashboard aide à identifier les problèmes du jour.

Manques principaux : aucune synthèse commerciale datée et territoriale sur la page d'accueil ; menu très dense ; absence de recherche globale transverse. La différenciation des droits n'est pas nécessaire tant que le backoffice conserve un unique administrateur.

### Opérateur quotidien

Les incidents de paiement, d'activation, d'email, de SMS, de consommation et de reversement sont généralement visibles. Plusieurs actions de reprise sont accessibles sans base ni logs.

Manques principaux : pas de file de travail unifiée avec propriétaire, priorité, ancienneté et état de résolution ; les liens des cartes du dashboard ouvrent souvent une liste non préfiltrée ; certaines corrections passent par l'édition technique d'un enregistrement plutôt que par une action métier.

### Responsable financier

La Vision 360 reversements est solide pour un démarrage : montant transférable, montant dû, transféré, restant, commissions et erreurs PSP sont exposés. Les paiements client conservent les références Stripe et les montants de commission.

Risque majeur : les mouvements et reversements restent modifiables par le formulaire générique. Une donnée financière ne devrait être modifiée que par un cas d'usage contrôlé, idempotent, motivé et audité.

### Responsable commercial

Les fiches commerçant, territoires, coffrets, prestations, profils et indicateurs de Vision 360 permettent un suivi individuel satisfaisant.

Manques principaux : portefeuille par territoire, comparaison de périodes, classement des coffrets, commerçants sans activité et tunnel de référencement consolidé hors Animation.

### Support client

La Vision 360 client constitue un bon point d'entrée : recherche par identité, historique des achats et coffrets, prestations, remboursements, communications, documents et support. Les actions utiles sont proches du contexte.

Manques principaux : chronologie unique horodatée de bout en bout et explication métier du « pourquoi » d'un statut ; la reconstruction d'un écart de consommation nécessite encore de croiser plusieurs tableaux.

## Audit du dashboard

### Disponible

- commerçants sans accès ou Stripe Connect incomplet ;
- incohérences entre coffrets, prestations et commerçants ;
- achats payés, en attente, sans référence et activations incomplètes ;
- instances actives, partielles et terminées ;
- prestations consommées et taux d'utilisation ;
- montants et mouvements transférables ;
- reversements en préparation et transferts en erreur ;
- emails et SMS en attente ou en erreur ;
- support non lu, signalements et demandes de publication ;
- actions d'expiration et de relance.

### Manquant ou insuffisant

- CA du jour, de la semaine et du mois ;
- nombre de commandes et panier moyen sur une période ;
- évolution par rapport à la période précédente ;
- répartition et filtre par territoire ;
- coffrets les plus vendus et commerçants les plus actifs ;
- nouveaux clients sur une période ;
- commissions générées par période ;
- coffrets expirant bientôt avec reliquat ;
- remboursements et WebPush en erreur dans les alertes centrales ;
- liens systématiquement préfiltrés sur l'anomalie indiquée.

Le dashboard répond correctement à « que dois-je surveiller ? », mais moins bien à « comment se porte l'activité aujourd'hui ? ».

## Flux financiers

| Question | Évaluation | Commentaire |
| --- | --- | --- |
| Montant payé par le client | Disponible | Achat et paiement sont reliés ; références PSP détaillées. |
| Valeur du coffret | Disponible | Achat et coffret accessibles depuis les vues de détail. |
| Consommation réalisée | Disponible | Validations et statuts de prestations sont reliés à l'instance. |
| Commerçant concerné | Disponible | Relations et Vision 360 commerçant. |
| Commission Localeo | Disponible | Commission brute et nette estimée dans les paiements et contrôles 360. |
| Montant dû au commerçant | Disponible | Mouvements transférables et agrégat par commerçant. |
| Montant déjà reversé | Disponible | Reversements, paiements et transferts Stripe. |
| Erreur de reversement | Disponible | Statuts, motifs, références PSP et alertes. |
| Remboursement | Disponible | Workflow dédié avec contrôles avant/après transfert. |
| Protection contre correction directe | Insuffisante | Plusieurs ModelView financiers restent éditables. |
| Justification d'une correction | Partielle | Certaines actions demandent un motif, pas les éditions génériques. |

Le backoffice sait répondre à « combien doit-on à chaque commerçant ? » grâce à la Vision 360 reversements. Il sait aussi distinguer les montants transférés et restants. Le risque principal n'est pas la visibilité mais l'intégrité opérationnelle : l'édition générique peut contourner les invariants des cas d'usage.

## Simulation des incidents

| Incident | Verdict | Informations et actions disponibles | Manques / intervention technique |
| --- | --- | --- | --- |
| Client payé, coffret non reçu | FACILE | Recherche client/achat, paiement PSP, instances, outbox email, renvoi de confirmation et réconciliation. | Prévoir une chronologie unique et une cause lisible de non-création/non-envoi. |
| Solde incorrect après consommation | POSSIBLE MAIS COMPLEXE | Instance, prestations, validations, transaction et audit accessibles. | Pas de journal de solde unifié avant/après ; croisement manuel de plusieurs vues. |
| Validation commerçant non payée | FACILE | Vision commerçant, validation, mouvement, reversement, transfert et erreur PSP. | Ajouter un accès direct depuis la validation vers le mouvement attendu et son diagnostic. |
| Fermeture temporaire/définitive d'un commerçant | POSSIBLE MAIS COMPLEXE | Suspension/archivage et contrôles empêchant certaines incohérences. | Pas de parcours assisté présentant impacts, coffrets actifs, bénéficiaires concernés et plan de sortie. |
| Erreur de coffret/prestation après vente | FACILE | Versionnement des prestations et règles de dépendance. | Vérifier en recette que l'interface distingue clairement version publiée et version future. |
| Transaction/opération en échec | FACILE | Dashboard, listes de paiements, transferts et communications en erreur. | WebPush et certaines erreurs batch ne remontent pas au dashboard principal. |
| Expiration avec reliquat | POSSIBLE MAIS COMPLEXE | Date d'expiration, état des prestations, batch de relance et expiration. | Pas d'alerte agrégée « expire bientôt avec reliquat » ni d'explication visible du traitement du reliquat. |

## Recherche et navigation

### Points satisfaisants

- recherches dédiées client, commerçant et coffret ;
- recherche achat par référence, email, téléphone, entreprise ou contact ;
- recherche paiement par identifiants PSP ;
- recherche reversement par statut et références Stripe ;
- relations cliquables entre objets ;
- pagination et tri natifs SQLAdmin ;
- accès contextuels depuis les visions 360.

### Points à corriger

- absence de recherche globale unique acceptant email, téléphone, référence achat, identifiant instance ou identifiant PSP ;
- filtres date/statut/territoire inégaux selon les listes ;
- cartes du dashboard qui ne transportent pas toujours le filtre correspondant ;
- navigation multi-territoires essentiellement portée par les relations `ville`, sans sélecteur global persistant ;
- duplication de l'enregistrement de plusieurs BaseView Animation dans la fonction d'initialisation du backoffice ;
- catégories nombreuses et menu Exploitation dense malgré le regroupement récent des WebPush.

## CRUD et protection métier

| Objet | État actuel | Recommandation production |
| --- | --- | --- |
| Territoire | CRUD | Conserver création/modification ; interdire suppression si référencé, préférer archivage. |
| Commerçant | CRUD avec invariants et actions d'accès | Conserver ; exiger motif pour suspension/archivage et afficher l'impact. |
| Utilisateur commerçant | Consultation et actions d'accès | Approche correcte ; pas d'édition directe des secrets. |
| Coffret | CRUD avec contrôles et rentabilité | Conserver ; publication/archivage via actions métier et versionnement. |
| Prestation | CRUD et versions | Conserver ; ne jamais réécrire la version consommée par une instance vendue. |
| Achat | Création interdite mais édition/suppression génériques possibles | Passer en lecture seule ; exposer uniquement réconciliation, annotation et workflows contrôlés. |
| Paiement | Création interdite mais édition/suppression génériques possibles | Passer totalement en lecture seule ; corrections via synchronisation PSP. |
| Coffret acheté | Création interdite mais édition/suppression génériques possibles | Interdire suppression et édition libre ; actions dédiées pour expiration, lien, QR et statut. |
| Consommation | Création interdite mais édition/suppression génériques possibles | Lecture seule ; annulation/correction par action motivée créant une contre-écriture. |
| Mouvement/reversement | Suppression interdite mais édition encore possible | Lecture seule ; transitions uniquement via services métier idempotents. |
| Remboursement | Workflow dédié | Conserver ; rendre les champs financiers immuables après exécution. |

## Historisation et auditabilité

Le socle d'audit persiste l'acteur, la date, l'action, la phase, l'IP, la requête et les ressources concernées. Plusieurs opérations sensibles ajoutent des métadonnées et des motifs.

Les limites sont importantes :

- le compte administrateur configuré est acceptable pour le lancement uniquement parce qu'il reste personnel et utilisé par un seul administrateur ;
- l'audit générique de CRUD est déclenché après mutation et n'enregistre pas automatiquement l'état avant/après ;
- une édition SQLAdmin ne demande pas systématiquement de motif ;
- l'échec de persistance de l'audit est journalisé mais ne bloque pas l'opération métier ;
- aucune séparation des rôles n'est prévue ; ce point devient une évolution obligatoire dès l'arrivée d'un second opérateur.

Le standard cible avant production doit être : compte personnel non partagé, action métier, confirmation, motif obligatoire pour les corrections sensibles, valeurs avant/après et identifiant de corrélation. Les comptes nominatifs multiples et les rôles différenciés pourront attendre l'arrivée d'un second opérateur.

## Multi-territoires

Le modèle rattache villes, commerçants, coffrets et animations. Les consoles Animation savent limiter le périmètre communal d'un opérateur. En revanche, la majorité du backoffice général fonctionne comme une vue globale sans sélecteur de territoire persistant ni filtrage systématique par rôle.

À 2 territoires, cela reste exploitable. À 10 ou 20, les listes globales, le dashboard sans filtre et l'absence de périmètre par opérateur augmenteront les erreurs et le temps de traitement. Une refonte n'est pas nécessaire : un filtre global de territoire, propagé aux dashboards et listes principales, avec option « Tous les territoires » réservée aux administrateurs, suffit pour les premières phases.

## Anomalies et améliorations prioritaires

| Priorité | Domaine | Problème | Risque opérationnel | Correction actionnable | Effort |
| --- | --- | --- | --- | --- | --- |
| 🔴 | Finance / achats | Achat, paiement, instance, consommation, mouvements et reversements restent partiellement éditables via CRUD. | Altération d'une preuve financière ou contournement d'un invariant. | Mettre les vues transactionnelles en lecture seule et conserver uniquement des actions métier contrôlées. | Faible |
| 🟡 | Sécurité / audit | Le compte administrateur configuré ne permet pas d'accueillir un second opérateur de façon traçable. | Partage de compte et perte d'imputabilité lors de la croissance de l'équipe. | Conserver le compte personnel au lancement ; mettre en place OIDC et rôles avant d'ouvrir le backoffice à une autre personne. | Moyen |
| 🔴 | Audit | Pas d'avant/après ni motif systématique sur les mutations génériques. | Impossible de justifier précisément une correction. | Capturer diff avant/après et motif ; interdire l'édition générique des données sensibles. | Moyen |
| 🔴 | Déploiement | Les migrations ne garantissent pas encore automatiquement la conformité des bases historiques. | Backoffice indisponible après déploiement, intervention SQL urgente. | Exécuter les migrations en pre-deploy et ajouter un readiness de schéma bloquant. | Moyen |
| 🟠 | Dashboard | Pas de CA, commandes, panier moyen ni comparaison de périodes. | Pilotage commercial quotidien incomplet. | Ajouter Aujourd'hui/7j/30j, CA, ventes, panier et variation N-1. | Moyen |
| 🟠 | Expiration | Pas de compteur « expire bientôt avec reliquat ». | Réclamations et reliquats non anticipés. | Ajouter compteur et liste préfiltrée avec montant/prestations restantes. | Faible |
| 🟠 | Multi-territoires | Pas de filtre territorial global sur le backoffice général. | Erreurs de périmètre et analyses lentes à 10–20 territoires. | Ajouter un sélecteur persistant et le propager aux requêtes principales. | Moyen |
| 🟠 | Incidents | Pas de chronologie unifiée commande → paiement → instance → validation → reversement. | Diagnostic lent et dépendant de l'expertise de l'opérateur. | Créer une timeline support à partir des objets déjà disponibles. | Moyen |
| 🟠 | Navigation | Les cartes dashboard ouvrent souvent une liste non préfiltrée. | L'opérateur doit refaire manuellement le diagnostic. | Ajouter les paramètres de filtre dans chaque lien d'alerte. | Faible |
| 🟠 | Qualité | Des BaseView Animation sont enregistrées deux fois. | Menu dupliqué ou comportement SQLAdmin instable. | Supprimer les trois appels `add_base_view` dupliqués et ajouter un test d'unicité. | Faible |
| 🟡 | Recherche | Absence de recherche globale. | Temps de traitement support supérieur. | Champ global multi-identifiants redirigeant vers la bonne Vision 360. | Moyen |
| 🟡 | Commerçants | Suspension sans parcours d'impact consolidé. | Oubli de bénéficiaires ou coffrets concernés. | Ajouter une prévisualisation d'impact et un plan de sortie. | Moyen |
| 🟡 | Alertes | WebPush et remboursements en erreur absents du dashboard central. | Incidents silencieux jusqu'à consultation du menu dédié. | Ajouter deux cartes d'alerte préfiltrées. | Faible |
| 🟡 | UX | Libellés techniques et mélange français/anglais dans certains statuts. | Compréhension plus lente et risque d'action erronée. | Dictionnaire de libellés métier commun à toutes les vues. | Faible |
| 🟢 | Reporting | Pas d'exports analytiques avancés consolidés. | Limitation seulement lorsque les volumes croîtront. | Prévoir des exports périodiques ciblés, sans construire un BI complet. | Moyen |

## Une journée chez Localeo

| Étape du lundi matin | Évaluation | Parcours actuel |
| --- | --- | --- |
| 1. Vérifier les ventes | POSSIBLE MAIS COMPLEXE | Ouvrir achats et paiements ; le dashboard donne des volumes globaux mais pas aujourd'hui/semaine/mois ni CA. |
| 2. Vérifier les paiements | FACILE | Carte paiements non finalisés, liste détaillée PSP et action de réconciliation. |
| 3. Vérifier les consommations | FACILE | Dashboard d'utilisation, validations et instances ; Vision 360 client/commerçant pour le détail. |
| 4. Vérifier les reversements | FACILE | Vision 360 reversements, montants transférables, transferts demandés et erreurs. |
| 5. Identifier les anomalies | FACILE | Bandeau d'alertes et sections paiement, catalogue, communications, support et reversements. |
| 6. Vérifier les nouveaux commerçants | FACILE | Référencement, accès, Stripe Connect, profil et publication. |
| 7. Traiter les incidents clients | FACILE | Recherche et Vision 360 client, renvoi QR/email, remboursement et support. |
| 8. Vérifier les actions du jour | POSSIBLE MAIS COMPLEXE | Les alertes existent, mais ne forment pas une file assignable et certains liens ne sont pas préfiltrés. |

## Checklist de mise en production

### 🔴 À faire impérativement avant lancement

1. Rendre les tables transactionnelles et financières non éditables/non supprimables dans SQLAdmin.
2. Garantir que le compte administrateur reste personnel, avec un secret fort stocké hors du dépôt et une procédure de rotation.
3. Capturer avant/après et motif pour toute correction sensible.
4. Exécuter automatiquement les migrations avant le démarrage applicatif.
5. Ajouter un contrôle de conformité du schéma au readiness.
6. Recetter sur préproduction les cinq parcours Vision 360 et les actions financières.
7. Tester restauration de base, reprise PSP et idempotence des batchs.
8. Supprimer les enregistrements de menu Animation dupliqués.
9. Valider explicitement la politique du reliquat à expiration et l'afficher aux opérateurs.

### 🟠 Fortement recommandé avant lancement

1. Ajouter CA, ventes, panier moyen et périodes au dashboard.
2. Ajouter l'alerte coffrets expirant avec reliquat.
3. Préfiltrer les listes ouvertes depuis les cartes d'alerte.
4. Ajouter un filtre territorial persistant.
5. Ajouter remboursements et WebPush en erreur au dashboard.
6. Construire une timeline support unifiée à partir des données existantes.
7. Ajouter une prévisualisation d'impact avant suspension d'un commerçant.
8. Harmoniser libellés et badges de statut.
9. Tester les temps de réponse avec un volume prévisionnel à 20 territoires.
10. Formaliser la procédure quotidienne et les escalades PSP.

### 🟡 À prévoir en V1.1

- recherche globale multi-identifiants ;
- tableau commercial par territoire et comparaison de périodes ;
- file de travail avec assignation et échéance ;
- exports opérationnels programmés ;
- suivi de commerçants sans activité ;
- indicateurs de récurrence et d'activation client ;
- amélioration du parcours de fermeture commerçant.
- comptes administrateurs nominatifs, OIDC et RBAC avant l'arrivée d'un second opérateur.

### 🟢 À ne pas développer maintenant

- ERP comptable complet ;
- moteur BI et constructeur de rapports libre-service ;
- workflows personnalisables par territoire ;
- gestion de 500 territoires et délégations hiérarchiques complexes ;
- moteur général de tickets remplaçant un outil support spécialisé ;
- correction manuelle arbitraire des écritures financières ;
- orchestration no-code de tous les batchs.

## Conclusion

### 1. Puis-je exploiter Localeo quotidiennement avec ce BackOffice ?

Oui fonctionnellement, après correction des trois blocants de contrôle. Les opérations quotidiennes sont largement couvertes sans accès direct à la base.

### 2. Puis-je comprendre rapidement un problème client ou commerçant ?

Oui dans la majorité des cas grâce aux visions 360. Les cas de solde/consommation restent plus lents faute de chronologie unifiée.

### 3. Ai-je une maîtrise suffisante des flux financiers ?

La visibilité est suffisante pour démarrer, mais la protection contre les éditions directes et la traçabilité avant/après des corrections ne le sont pas encore.

### 4. Le BackOffice peut-il gérer les 10 à 20 premiers territoires ?

Oui sans refonte majeure, à condition d'ajouter rapidement un filtre territorial global et des statistiques par territoire.

### 5. Quelles sont les trois fonctionnalités au meilleur rapport valeur/effort ?

1. verrouiller en lecture seule les vues transactionnelles/financières et passer par des actions métier ;
2. ajouter des liens d'alerte préfiltrés et l'alerte « expiration avec reliquat » ;
3. enrichir le dashboard avec CA, ventes et panier moyen sur Aujourd'hui/7j/30j.

Le socle n'a pas besoin de devenir un ERP. Il a surtout besoin de devenir un poste de contrôle sûr : données financières immuables, compte administrateur personnel, schéma garanti et alertes directement actionnables.

Le découpage de mise en œuvre est disponible dans le [plan d'actions BackOffice](plan-actions-backoffice-preproduction.md).
