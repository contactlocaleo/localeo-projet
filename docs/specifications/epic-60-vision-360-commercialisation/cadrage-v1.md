# Epic 60 - Cadrage V1 pour lancement des specifications

> Historique de conception. Etat realise et decisions deleguees : [rapport V1](rapport-developpement-v1.md), [specification detaillee](specifications-fonctionnelles.md), [contrats implementes](contrats-api.md).

> Version : 1.0, consolidee le 2026-09-05.
> Statut : cadrage finalise pour demarrer les specifications fonctionnelles et
> techniques ; implementation non demarree, autorisation de production non acquise.
> Reference des decisions : [registre des arbitrages](registre-arbitrages.md).

## 1. Finalite et resultat attendu

Transformer le back-office Localeo en poste de travail de referencement,
commercialisation et suivi d'activite. L'operateur doit pouvoir referencer
un commercant, preparer son offre, composer un coffret, controler son economie
et sa vendabilite, le mettre en vente puis traiter les incidents et engagements.

Parcours directeur :

`Referencer -> Preparer l'offre -> Composer -> Verifier -> Publier -> Honorer -> Suivre`.

Une seule Epic 60, 22 stories PRD-561 a PRD-582. L'Epic 61 est fusionnee et ses
documents sont supprimes ; aucun travail n'est suivi separement sous ce numero.

## 2. Decisions produit consolidees

| Sujet | Regle de cadrage retenue | Reference |
| --- | --- | --- |
| Perimetre | ERP d'activite Localeo, sans comptabilite generale ni CRM complet | ERP-ARB-01 |
| Offre commercant | Modele de saisie autonome puis prestation propre a chaque coffret, provenance/version et conditions propres ; aucune propagation automatique | ERP-ARB-02 |
| Aptitude | Capacites et prerequis distingues du statut commercant, de la completion du dossier et du verdict coffret | ERP-ARB-04, 08 |
| Dossier de referencement | Reutiliser Onboard, son cycle, sa prochaine action, son responsable et son echeance ; pas de second workflow | ERP-ARB-05, 08 |
| Navigation | Six rubriques : Mon activite ; Commercants et catalogue ; Operations ; Finance ; Supervision ; Referentiels et administration | ERP-ARB-06 |
| Migration des interfaces | Bascule directe sur les nouveaux parcours ; aucun maintien des anciennes interfaces, le back-office n'etant pas encore utilise selon l'utilisateur | ERP-ARB-07, decision ajustee |
| Publication | Simulation explicite de l'etat cible puis verification et commande atomique sur donnees courantes ; aucune activation implicite de ressources liees | ERP-ARB-09 |
| File de travail | Defaut NON_VENDABLE, pertes d'offres prioritaires, preparation et incidents distingues, brouillons accessibles | COM360-ARB-04, ERP-ARB-10 |
| Causes communes | Regroupement visuel par source sans perdre les impacts et transitions de chaque coffret | ERP-ARB-11 |
| Engagements existants | Analyser separement ventes futures et achats engages avant modification/retrait | ERP-ARB-12 |
| Economie | Marge sur prix, commission theorique, marge cible et flux reels distingues ; frais non integres explicites | ERP-ARB-13 |
| Construction | Developper et recetter le parcours vertical complet en premier, puis harmoniser les autres destinations du perimetre avant bascule globale | ERP-ARB-14, 07 |
| Archivage | Distinguer cloture/abandon du dossier, retrait de l'offre et archivage commercant ; conserver engagements et preuves | ERP-ARB-15 |
| Diagnostic | Source canonique partagee avec Marketplace/paiement, projection minimale, trois verdicts et controles reussis visibles | COM360-ARB-01, 02, 03, 09 |
| Reevaluation | Evenements, reconciliation et action manuelle idempotente | COM360-ARB-08 |
| Canaux | Alertes BackOffice/Control ; email et WebPush configurables | COM360-ARB-07 |
| Coherence | Test de parite obligatoire entre diagnostic, Marketplace et paiement | COM360-ARB-10 |

Le principe du modele d'offre est valide ; son schema, son versionnement et
la migration des donnees restent des travaux de specification. De meme,
les six rubriques sont decidees, tandis que les libelles secondaires et
l'affordance des actions sont a concevoir et recetter.

## 3. Perimetre V1 par bloc fonctionnel

| Bloc | Livrables fonctionnels attendus | Stories |
| --- | --- | --- |
| Pilotage catalogue | Synthese, file, filtres, diagnostic complet, regroupement des causes et couverture territoriale | PRD-561 a 564, 568 |
| Alertes et historique | Transitions, deduplication, resolution, chronologie, Control et reevaluation | PRD-565 a 567 |
| Accueil et navigation | Actions frequentes, files par perimetre, six rubriques, aide contextuelle | PRD-571, 572, 581 |
| Dossier commercant | Creation/edition, reprise Onboard, offre et diagnostic d'aptitude, prochaine action | PRD-573 a 576 |
| Dossier coffret | Creation/edition, composition, economie, simulation cible et publication | PRD-577 a 580 |
| Securite et qualite | Autorisations, audit, parite, concurrence, accessibilite et mesure | PRD-569, 570, 582 |

Les brouillons sont sauvegardables sans publication. Les regles de domaine
restent appliquees sur les commandes, y compris dans les nouvelles interfaces.
La rentabilite positive, un dossier valide ou un compte Stripe pret ne
remplacent jamais le diagnostic canonique final du coffret.

Hors V1 : comptabilite generale, stocks/paie, CRM complet, relances automatiques
massives, propagation automatique d'offres, correction fiscale automatique,
modification en masse et refonte des applications publiques. Les applications
publiques conservent leurs contrats ; leurs controles de vendabilite restent
alignes sur le moteur partage.

## 4. Bascule directe : portee exacte

La decision ERP-ARB-07 remplace la proposition initiale de coexistence
progressive. L'implementation peut etre decoupee en lots de travail et testee
en environnement de recette, mais la bascule utilisateur est unique.

Inventorier toutes les anciennes destinations et les classer : remplacee par
un parcours, reintegree comme fonction avancee dans la nouvelle console,
ou retiree car obsolete. Aucun besoin utile ne doit disparaitre par oubli.
Les composants internes reutilises ne constituent pas une ancienne interface
a maintenir. Pas d'obligation de redirection de compatibilite pour les anciens
liens internes ; mettre a jour tous les liens, aides et notifications produits.

Retirer les anciennes pages et commandes d'interface devenues inutiles apres
verification des consommateurs. Ne pas supprimer une API publique, une commande
metier partagee, une integration ou les donnees historiques au pretexte de
retirer une interface. Un retour arriere de deploiement reste un mecanisme
technique prepare ; ce n'est pas une seconde interface maintenue en parallele.

## 5. Points ouverts et traitement pendant les specifications

22 arbitrages sur 25 sont decides : 21 reponses positives et une decision
ajustee de bascule directe. Les trois restants sont listes ci-dessous ; les
dix precisions COM360-CON-* sont des choix de conception, pas dix approbations
produit supplementaires.

| Point | Ce qui reste a trancher | Travail autorise des maintenant | Condition avant implementation concernee |
| --- | --- | --- | --- |
| COM360-ARB-05 | Confirmation historique de la file en lecture avec liens de traitement | Specifier les ateliers d'ecriture decides et les liens de traitement ; garder la separation comme hypothese explicite | Confirmer les actions permises dans la file |
| COM360-ARB-06 | Confirmation historique du cycle d'alerte | Detailler transitions, rechutes, regroupements et canaux selon le backlog ; ne pas qualifier le cycle d'approuve | Valider la table de transitions et resolution |
| ERP-ARB-03 | Matrice de permissions par action et territoire | Proposer la matrice a partir des roles et identites reellement disponibles | Validation de la matrice avant exposition des nouvelles commandes |

COM360-CON-02/04 : qualifier les nouvelles exclusions (prestations, prix,
communes) sans ajouter silencieusement des obligations fiscales. CON-06 :
aligner le tri sur ERP-ARB-10 valide, departage exact a preciser. CON-07/10 :
mesurer frequence, fraicheur et volume. CON-09 : confirmer la retention avec
l'exploitation. Les autres precisions doivent etre formulees et testees dans
les specifications ; leur presence dans un document technique ne vaut pas
approbation utilisateur.

Ces points n'empechent pas de commencer les specifications. Ils empechent de
presenter les volets correspondants comme integralement approuves ou prets
pour une implementation sans condition.

## 6. Dossier de specification a produire

| Document cible | Contenu obligatoire | Critere de completion |
| --- | --- | --- |
| Specification fonctionnelle unifiee | Acteurs, 22 stories tracees, parcours nominaux/alternatifs, champs, validations, statuts, diagnostic courant/cible, impacts, archivage, permissions, messages et maquettes | Chaque commande explique entree, droits, effets, refus et reprise ; aucune nouvelle regle sans origine |
| Specification technique unifiee | Agregats/valeurs/services de domaine, integration Onboard, modele d'offre, migrations, repositories/UoW, transactions, concurrence, snapshots, projection, batches et audit | Separation des responsabilites et strategie de migration/bascule verifiables |
| Contrats API et commandes | Sept API existantes completees par schemas des commandes commercant/offre/coffret/publication ; erreurs, version attendue, idempotence, CSRF, OpenAPI | Aucune mutation sous GET ni dependance a un verdict obsolete ; contrats publics preserves |
| Plan de recette unifie | Cas fonctionnels, domaine, PostgreSQL, droits, parite, parcours UX, performance et bascule | Couverture explicite PRD-561 a 582, y compris refus/concurrence et absence d'effets partiels |
| Plan de bascule | Inventaire ancienne/nouvelle destination, liens, migrations, controles et retour arriere technique | Aucun ancien parcours maintenu en parallele ; aucune fonction ou donnee perdue par inadvertance |

Les documents diagnostic deja presents sont des materiaux de specification
a consolider, pas une specification complete des ateliers. Commencer par le
modele d'offre, les commandes de publication et les droits, puis detailler
les ecrans et les traitements transverses. Pas de changement de stack requis.

## 7. Criteres de sortie de l'epic

- Parcours commercant -> offre -> coffret -> verification -> publication
  -> suivi execute sans connaissance des tables techniques.
- Meme dossier Onboard et memes donnees depuis toutes les entrees.
- Aucun calcul de vendabilite ni rentabilite duplique dans les ecrans.
- Impacts sur les achats engages controles avant chaque changement concerne.
- Authentification, droits, version et prerequis recontroles a la commande.
- Alertes, couverture, historique et traitements coherents dans BackOffice/Control.
- Recette des 22 stories, regressions publiques et paiement, performance et
  bascule directe documentees ; aide et liens alignes sur la nouvelle console.

Cette V1 finalise le cadrage de l'epic pour lancer les specifications. Elle
ne declare ni ces specifications terminees, ni les tests applicatifs executes.
