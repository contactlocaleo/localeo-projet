# Epic 62 — Validation des modifications de prestations dans Localeo Support

- Date : 10 septembre 2026.
- Statut : **À développer — cadrage initial**.
- Priorité : **Critique**, continuité de commercialisation des coffrets.
- Demande : soumettre les modifications commerçant à Localeo avant application,
  afficher « En cours de validation », notifier le support par WebPush et
  accepter avec revalidation BUM intégrée.
- Dépendances : Epic 3 (intention historique), Epic 34 (WebPush exploitation),
  Epic 50 (BUM), Epic 60 (modèles, copies et ERP), nouvelle application
  [Localeo Support](../../exploitation/exploitation/localeo-support.md).

## Problème et résultat attendu

Aujourd'hui, modifier le libellé ou la description d'une prestation depuis
l'espace commerçant change immédiatement la prestation du coffret et rend sa
qualification BUM à revalider. Le coffret peut ainsi disparaître de la marketplace.

Demain, une modification crée une proposition distincte. La version applicable,
les offres publiques et la qualification BUM restent inchangées pendant l'examen.
Localeo accepte ou refuse depuis Localeo Support. L'acceptation applique la
nouvelle version et revalide la qualification BUM des coffrets concernés dans
une même transaction, après vérification explicite par l'opérateur habilité.

Exemple : la version 4 reste vendue ; la proposition issue de cette version est
« En cours de validation ». Après acceptation, la version 5 devient applicable
aux futures ventes. Un coffret acheté avec la version 4 conserve cette version.

## Constats vérifiés dans l'existant

| Élément | Fonctionnement observé et impact |
| --- | --- |
| `app/api/commercants_api.py`, PATCH `/profils/commercants/me/prestations/{prestation_id}` | Appelle directement `MettreAJourContenuPrestationCommercant`, avec contrôle de propriété et session commerçant. Le contrat de réponse doit distinguer proposition et contenu applicable. |
| `app/application/profils/use_cases/mettre_a_jour_contenu_prestation_commercant.py` | Écrit libellé et description sur `PrestationCoffretOrm`, incrémente `version_courante`, crée un snapshot, publie via `ServiceActivitesLocales`, puis appelle `marquer_requalification_requise` si la fonctionnalité BUM est activée. Ces effets doivent être déplacés à l'acceptation. |
| `app/application/commercialisation/services/atelier_erp.py` | Modèles, versions de modèles et copies rattachées sont distincts. Une proposition sur une copie ne doit pas être propagée silencieusement à toutes les copies du même modèle. |
| `app/application/conformite_fiscale_bum/service_conformite_bum.py` | La qualification contient un snapshot de la composition, des versions de prestations et de la politique active. `decider_validation_bum` exige une vérification, un commentaire et le contrôle de version. Réutiliser ce parcours métier. |
| `app/application/conformite_fiscale_bum/service_onboarding_commercant.py` | Contenu et médias peuvent aussi déclencher une requalification. Inventorier ces écritures pour éviter un contournement ; distinguer les modifications internes autorisées du parcours commerçant. |
| `app/application/profils/services/service_profils_commercants.py` et routes `/me/page/*` | Un mécanisme de proposition existe pour la page du commerçant. Il ne constitue pas un sas pour les prestations du coffret. Réutiliser les conventions utiles, pas l'objet métier. |
| `app/application/exploitation/use_cases/pwa_exploitation.py` | WebPush exploitation possède abonnements, préférences, outbox, déduplication par type/acteur/ressource et batch. L'événement support actuel concerne un message et cible l'ancienne timeline : ajouter un événement et une destination dédiés. |
| `app/api/support_ui.py`, `app/infrastructure/erp/instances.js`, `app/api/instances_support_api.py` | Localeo Support traite les instances et leurs dossiers internes. Une modification catalogue peut exister sans instance achetée : elle nécessite une file autonome, reliée aux dossiers, et non une fausse instance. |
| `../../localeo-commercant/src/app/routes.js` | L'application propose déjà « Animer / modifier le contenu de mes prestations ». Adapter ce parcours et ses appels API, son message de succès et ses tests. |

L'Epic 3 est marquée terminée dans le suivi historique mais son intention de sas
n'est pas assurée par le PATCH actuel. Cette nouvelle demande est suivie sous
Epic 62, sans modifier rétroactivement le statut de l'Epic 3.

Dans cette epic, « WePush » désigne le **WebPush** déjà intégré à Localeo.
Il ne s'agit pas d'ajouter un prestataire de notification distinct.

## Règles métier cibles

1. Une soumission n'écrit jamais dans la version applicable, ne publie pas
   d'activité publique et ne change ni statut catalogue ni qualification BUM.
2. Le statut de demande est indépendant du statut métier de la prestation :
   une prestation peut rester **Active** avec une modification **En cours de validation**.
3. La proposition conserve auteur, date, version de départ, contenu avant/après,
   cible et périmètre des copies/coffrets examinés. Son contenu soumis est immuable.
4. V1 proposée : une seule demande ouverte par cible ; pour la corriger, retirer
   la demande puis en soumettre une nouvelle, en conservant les deux historiques.
5. États : `EN_ATTENTE_VALIDATION`, `ACCEPTEE`, `REFUSEE`, `RETIREE`.
   Un conflit d'édition bloque la décision ; il n'équivaut pas à un refus métier.
6. Refus motivé ou retrait : aucun effet sur la publication ou la BUM ; le
   commerçant voit la décision, sa date et le motif destiné à lui être communiqué.
7. Acceptation : contrôle de concurrence sur la demande, les prestations, les
   coffrets et la politique BUM ; nouvelle version applicable, diagnostics requis,
   nouvelles qualifications et audit sont enregistrés atomiquement.
8. « Accepter et revalider la BUM » explique la portée de la décision et comporte
   la confirmation explicite de vérification BUM et un commentaire. Aucun second
   passage dans chaque fiche Fiscalité n'est nécessaire. L'acceptation n'est pas
   une certification automatique sans examen.
9. Revalider la BUM signifie créer une **qualification du coffret** sur la
   politique active et les nouvelles sources ; ne pas modifier la politique
   globale ni les justificatifs des achats passés.
10. Un coffret commercialisable avant la demande le reste pendant le sas puis
    après acceptation si les autres conditions sont toujours réunies. Une
    suspension manuelle, un archivage, un brouillon ou un autre blocage ne sont
    jamais levés automatiquement. Afficher les blocages restants.
11. Si un diagnostic obligatoire échoue, si la politique a changé depuis
    l'examen ou si une source a été modifiée, aucune application partielle :
    conserver la demande ouverte et demander une nouvelle lecture du comparatif.
12. Ne jamais modifier les versions référencées par les instances déjà vendues,
    leurs droits, prix, reversements ou preuves d'achat.

## Périmètre des versions et des champs

Le parcours actuel modifie une **prestation de coffret**, pas directement son
modèle. La V1 doit couvrir au minimum libellé et description de ce parcours.
Le diff et la liste des coffrets touchés sont calculés côté serveur.

Proposition de cadrage : cibler la copie sélectionnée en V1. Pour une demande
portant ultérieurement sur le modèle et plusieurs copies, conserver explicitement
les identifiants et versions des copies incluses ; faire valider ce périmètre
par Localeo et appliquer le lot atomiquement. Ne pas sélectionner les copies
par simple égalité de libellé, ni écraser une copie personnalisée.

Inventorier les autres écritures commerçant, notamment médias, avant livraison.
Tout champ commercial éditable par le commerçant doit passer par le sas ; sinon
son édition doit être indisponible dans ce parcours. Montants, commissions,
statuts de vente et règles fiscales ne deviennent pas éditables par ce projet.
Les modifications internes ERP/Localeo OnBoard restent sous leurs règles
actuelles ; elles provoquent un conflit si elles changent une source en examen.

## Parcours Localeo Support et notifications

- Accueil : accès distincts **Instances de coffrets** et **Modifications à valider**,
  compteur, recherche commerçant/coffret, filtre de statut, ancienneté, affectation.
- Fiche mobile : résumé, version applicable face à la proposition, champs modifiés,
  liste des coffrets affectés, diagnostics BUM, historique et décision.
- Liens vers commerçant, modèle/version d'origine s'il existe, copies, coffrets
  catalogue et instances associées. Les instances montrent une information
  contextuelle sans remplacer leur contenu historique par la proposition.
- Le support de niveau 1 consulte, affecte et prépare le dossier. L'acceptation
  avec BUM et le refus métier sont réservés à ADMIN en V1 ; une délégation exige
  une habilitation explicite. Respecter les communes autorisées sur chaque API.
- À la soumission, créer l'événement `PRESTATION_MODIFICATION_SOUMISE` et son
  outbox dans la même transaction. Reprendre les mécanismes d'envoi et de retry
  WebPush exploitation. Ne pas envoyer vers les abonnements commerçants/publics.
- Destinataires : agents support habilités au périmètre, abonnés et ayant activé
  la catégorie. Le filtrage territorial est à ajouter explicitement : le helper
  actuel accepte un filtre d'acteur, sans résoudre ce périmètre métier à lui seul.
- Notification sobre, lien authentifié vers la demande dans Localeo Support ;
  pas de données client, de contenu confidentiel ou de jeton de session dans le push.
- Ajouter dans Localeo Support l'abonnement/désabonnement, les préférences et le
  service worker nécessaires. Vérifier la portée du service worker existant de
  Localeo Control avant mutualisation. Aucune mise en cache hors ligne des dossiers.
- Permission navigateur refusée, abonnement absent ou panne push : la demande
  reste visible dans la file. Distinguer notification créée, envoyée et échouée ;
  l'envoi ne garantit pas que l'opérateur a lu la demande.

## Backlog initial et critères d'acceptation

Toutes les stories ci-dessous sont **À développer**.

| Story | Livrable | Critères de recette |
| --- | --- | --- |
| E62-01 | Demande versionnée et soumission commerçant | Version active et BUM identiques avant/après soumission ; contrôle de propriété ; doublon de requête sans seconde demande ; historique conservé. |
| E62-02 | UX commerçant | Affichage simultané « Active » et « En cours de validation », aperçu du candidat, retrait, historique et motif du refus ; aucun message prétendant que la modification est déjà publiée. |
| E62-03 | File et dossier mobile Support | Recherche, pagination, affectation, diff et coffrets impactés ; accès depuis l'ERP et les instances ; aucun accès hors périmètre. |
| E62-04 | Décision et application avec BUM | Bouton explicite, commentaire et vérification ; publication et qualifications atomiques ; conflit ou diagnostic bloquant sans effet partiel ; double clic idempotent. |
| E62-05 | Refus et retrait | Aucun changement catalogue ; décision tracée ; motif visible par le commerçant, notes internes non exposées. |
| E62-06 | WebPush support | Outbox transactionnelle, déduplication, destinataires autorisés, lien mobile après reconnexion, retries et file toujours utilisable sans push. |
| E62-07 | Protection des droits et concurrence | Achat simultané à l'acceptation cohérent avec une seule version ; anciennes instances inchangées ; édition ERP, changement de politique ou deuxième décideur détectés. |
| E62-08 | Migration, déploiement et exploitation | Schéma et readiness, contrats compatibles durant le déploiement, métriques et recette documentées ; aucun rétablissement massif implicite de coffrets bloqués. |

## Impacts techniques et livraison

- **Domaine** : transitions de demande, invariants de publication et portée de
  l'acceptation. **Application** : soumettre, retirer, consulter, affecter,
  accepter/revalider, refuser ; orchestration dans une unité de travail.
- **Persistance** : nouvelle demande avec version de départ et candidat JSON
  borné/validé, état, décision, responsable, dates et version de concurrence ;
  table de cibles si lot multi-copies retenu ; contraintes d'unicité des demandes
  ouvertes, index de file et historique. Numéro de migration à réserver à
  l'implémentation, après les migrations présentes (v229 pour Support).
- **API** : faire évoluer le PATCH actuel ou ajouter une route de soumission avec
  adaptation compatible ; ne jamais conserver un ancien chemin qui écrit encore
  directement. Réponses explicites `version_applicable` et `demande_en_cours`.
  Endpoints Support protégés par session, CSRF, idempotence et versions attendues.
- **Frontends** : dépôt `localeo-commercant`, shell Localeo Support et ERP dans
  ce dépôt ; vérifier les lecteurs publics de `localeo-marketplace` et les
  activités locales. Aucun candidat ne doit fuiter dans la recherche publique.
- **Batch/configuration** : réutiliser le canal `WEBPUSH_CONTROL_*` et vérifier
  la planification existante côté `localeo-cronjobs`, sans nouveau service supposé.
- **Reprise** : ne pas fabriquer de demandes pour les anciennes modifications.
  Lister les coffrets déjà bloqués pour requalification et proposer une revue
  explicite ; ne pas réactiver automatiquement ces dossiers historiques.
- **Déploiement** : schéma d'abord, backend compatible puis frontend commerçant
  et Support ; protéger le parcours d'écriture pendant la transition. Un rollback
  ne doit pas rouvrir la modification directe tant que des demandes sont pendantes.
- **Observabilité** : demandes ouvertes/ancienneté, conflits, décisions, blocages
  de publication après décision, échecs push ; audit corrélant demande, versions,
  acteur, commentaire et qualifications créées.

## Arbitrages à confirmer avant développement

1. Extension dès la V1 à une demande globale sur modèle et plusieurs copies,
   ou conservation du périmètre actuel par copie (proposition de cadrage ci-dessus).
2. Habilitation de certains opérateurs support à décider avec BUM, au-delà d'ADMIN.
3. Notification de décision au commerçant : affichage dans son espace obligatoire ;
   push/email additionnel à définir, sans le déduire de la notification support.
4. Objectif de délai de traitement et éventuelles relances/escalades.

La définition de terminé inclut tests métier, intégration PostgreSQL pour
atomicité/concurrence, recette mobile commerçant et Support, tests d'accès et
WebPush simulé, et non-régression des ventes pendant une demande pendante.
Cette epic est un cadrage : aucun changement de comportement n'est livré par
la création de ce document.
