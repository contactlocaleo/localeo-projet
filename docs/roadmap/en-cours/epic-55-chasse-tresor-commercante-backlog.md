# Backlog Epic 55 - Moteur commun et chasse au tresor commercante

## Suivi

- Criticite : `Moyenne`.
- Statut : `En cours - lots T1–T4 implémentés et vérifiés localement, lots T5–T6 et recette à mener`.
- Catalogue V1 : `PASSEPORT_COMMERCANT`, `TOMBOLA_LOCALE`, `CHASSE_TRESOR_COMMERCANTE`.
- Dependances : Epics 41, 42, 46, 47 et 49.

La [specification detaillee unique](../../specifications/moteur-animation/localeo_animation_engine_spec.md) porte les regles, les decisions, les contrats proposes et la recette. Cette fiche conserve uniquement le suivi de livraison.

## Lot de conception technique

- [x] Dossier de conception couvrant contrats, persistance, concurrence, API/droits, médias et exploitation, établi à partir du code et relu le 19 septembre 2026 : [référence technique V1](../../specifications/moteur-animation/conception-technique.md).
- [ ] Réaliser les lots T1–T6 et vérifier leurs critères de sortie ; le dossier et ses revues statiques ne constituent pas une recette du moteur.

Compte rendu par lot, décisions et preuves : [suivi d’implémentation](../../specifications/moteur-animation/suivi-implementation.md). Les cases ci-dessous portent la livraison complète et ne sont pas cochées sur la seule présence du socle.

## Livraison proposee

Organisation retenue : socle minimal puis développement par parcours complets associant domaine, API et interfaces ; les trois moteurs restent dans la livraison. Recette progressive pendant la réalisation, puis complète avant ouverture (TRE-ARB-81/TRE-ARB-82).

- [ ] Modele Animation generique : inscription, periode, territoire, publication et participation.
- [ ] Permissions par action regroupées en profils prêts à l’emploi, contrôles serveur et périmètres partenaire/animation ; mapping aux habilitations existantes (TRE-ARB-68).
- [ ] Verrou par participation et coordination des opérations globales au niveau animation ; ordre/protocole physique et scénarios de concurrence à vérifier (TRE-ARB-69).
- [ ] Préparation guidée avec sauvegarde/reprise du brouillon, rubriques manquantes et récapitulatif avant publication (TRE-ARB-70).
- [ ] Bibliothèque de fiches POI du partenaire, version et validation propres à chaque animation ; accès, QR et consignes revérifiés, éditions publiées préservées (TRE-ARB-71).
- [ ] Nouvelles animations : inscriptions dès publication, fermeture à la fin ou anticipée, capacité facultative atomique ; reprise des inscrits conservée et paramètres des brouillons convertis contrôlés avant première publication.
- [ ] DSL JSON avec enveloppe `common` et bloc `engineConfig` valide par le moteur du type.
- [ ] Registres et trois moteurs specialises avec trois renderers : Passeport, Tombola, Chasse.
- [ ] Modules internes au backend existant, interfaces communes, registre explicite et livraison coordonnée avec les frontends (TRE-ARB-64).
- [ ] Modèles de validation backend comme source des schémas ; export automatique JSON Schema et contrôle de concordance, règles métier dans le domaine (TRE-ARB-65).
- [ ] Version de contrat coordonnée par moteur pour configuration/commandes/projections ; versions de contenu et schéma commun distinctes, futures parties publiées préservées (TRE-ARB-66).
- [ ] Définitions versionnées en JSON, participations/preuves/progression en tables structurées ; mapping, contraintes et migrations de l’existant à finaliser (TRE-ARB-67).
- [ ] Contrat extensible par type : schéma, règles, commandes, projections, préparation, renderer et capacités ; provider facultatif. Ajout de futurs types sans imposer le profil linéaire Chasse V1 au socle.
- [ ] Conversion des brouillons/configurations retenus : inventaire, simulation sans écriture, lots contrôlés/tracés/reprenables et contrôle de source ; ensemble validé avant ouverture, aucune suppression implicite de données (TRE-ARB-80).
- [ ] Bascule directe : aucune animation publiée avec l’ancien moteur, donc aucune coexistence ; moteur commun seul et consommateurs alignés avant ouverture.
- [ ] Live non déployé : aucune rétrocompatibilité avec un ancien client ; conserver le versionnement des futures définitions et participations.
- [ ] Cinematique complete de generation, prompt final persiste/exportable et dernier appel IA bouche.
- [ ] Génération sur brief court : listes de commerçants et POI, fourchette d’étapes, durée approximative, public, difficulté, thème général et schéma attendu. Récit et parcours proposés dans ce cadre puis acceptés ; schéma à liste variable, écart au brief signalé, contrôles opérationnels hors prompt (TRE-ARB-87).
- [ ] Provider de template Passeport : prompt genere, execution externe manuelle, depot et publication du resultat.
- [ ] File ERP des demandes de creation de chasse : statuts, export du prompt, controles, publication manuelle du resultat, reprise et lien vers instance.
- [ ] Finalisation idempotente de creation, distincte de publication publique de l’animation.
- [ ] Aperçu des impacts avant retrait/correction, motif et confirmation explicite, recontrôle serveur et actualisation si impact obsolète (TRE-ARB-72).
- [ ] Brouillon Animation unique créé dès le début de la demande, non publiable en attente et complété par le résultat accepté ; reprise sans doublon (TRE-ARB-73).
- [ ] ERP : liste filtrable des demandes avec statuts/prochaine action/erreurs et fiche détaillée prompt/résultat/historique (TRE-ARB-74).
- [ ] Quota disponible calculé depuis réservations/consommations, sans compteur supplémentaire ; journal et coordination transactionnelle partenaire/mois (TRE-ARB-75).
- [ ] Quota de génération partagé par partenaire : 10/mois configurables dans l’ERP, réservation à la demande, consommation au résultat accepté, libération sur annulation préalable et corrections sans double décompte.
- [ ] Quota mensuel en Europe/Paris sans report ; changement de plafond sur le mois courant et les suivants, passé inchangé, engagements conservés lors d’une baisse et places supplémentaires immédiatement disponibles lors d’une hausse (TRE-ARB-59).
- [ ] Profil DSL Chasse V1 fermé : `ALL`, unique successeur `SUCCESS`, terminal sans transition ; autres combinaisons ambiguës refusées.
- [ ] Parcours de chasse linéaire à ordre imposé ; fourchette d’étapes du brief (suggestion 5 à 8 par défaut) avec avertissement non bloquant ; défis QCM, information, association, remise en ordre et saisie courte (TRE-ARB-88).
- [ ] Lieux/défis futurs masqués ; commerce nommé et localisé au déblocage, défi sur place ; une seule étape par commerçant.
- [ ] Progression narrative, résolution, preuves, effets et qualification séparés ; état de régularisation explicite dans Live.
- [ ] Protocole transactionnel et d’idempotence : courses clôture/correction/retrait/capacité, versions, résultat rejouable et effets uniques vérifiés.
- [ ] Runtime de chasse : scan avant/apres resolution, indice et aide de resolution distincts disponibles apres une premiere mauvaise reponse, POI et qualification.
- [ ] Information confirmée par « Continuer » sous réserve des autres conditions ; orientation par adresse et lien cartographique externe sans suivi de position Localeo.
- [ ] Retrait d’etape uniquement global en V1, conservation des autres acquis et recalcul equitable ; aucune dispense individuelle.
- [ ] Dépendances explicites validées avant publication ; retraits successifs résolus dans l’ordre.
- [ ] Objets/indices indispensables fournis avec provenance de dispense sans fuite des étapes futures ; retrait définitif après démarrage et dernière étape requise non retirable, contrôle atomique.
- [ ] Parcours Animation, Live et commercant, publication, duplication et tirage existant.
- [ ] Chasse sans achat obligatoire ; inscription familiale adulte avec progression/chance uniques et sans données enfant.
- [ ] Publication de chasse bloquée sans règlement et checklist confirmée (horaires, accords, trajet, accessibilité, consignes), avec auteur/date/version.
- [ ] Preuve annulée avant clôture : nouveau scan requis, autres acquis conservés ; après clôture, population figée et anomalies tracées sans recalcul.
- [ ] POI validés par l’organisateur sans seconde approbation Localeo : responsable, auteur, date, emplacement QR et observations ; photo facultative.
- [ ] Alternatives textuelles obligatoires aux éléments visuels/sonores nécessaires aux défis, disponibles avec le contenu sans contourner les preuves.
- [ ] Bibliothèque privée du partenaire/opérateurs habilités, versions acceptées uniquement ; réutilisation versionnée dans la même commune.
- [ ] Dépôt/publication ERP possibles par le même opérateur avec les deux permissions, contrôles et prévisualisation obligatoires, audit de chaque action.
- [ ] QCM de 2 à 6 propositions avec une bonne réponse ; aucun score/classement V1 ; déclaration adulte obligatoire sans date de naissance à l’inscription de chasse.
- [ ] Activités supplémentaires V1 : association un-à-un (2–6), ordre unique (3–6), mot/code et variantes normalisées ; définitions et commandes contrôlées par le domaine, aucun appel IA pour corriger (TRE-ARB-88).
- [ ] Adapter génération/import/édition/prévisualisation et trois rendus Live accessibles au clavier ; solutions privées, présentation mélangée stable, reprise et aides après erreur valide ; tests de bornes, références, normalisation, idempotence et non-divulgation.
- [ ] Récupération par lien email existant sans nouvelle participation ; génération décomptée sur le mois réservé, demandes sans expiration automatique et ancienneté ERP visible.
- [ ] Conservation : prompts/réponses inutilisés 30 jours après terminaison/annulation, essais détaillés 90 jours après fin ; purge automatique avec exclusions, reprise et rapport ERP, registre interne à aligner.
- [ ] Connexion nécessaire pour réponses/scans/validations ; conservation de la saisie en cours, reprise sur état serveur et réconciliation des commandes incertaines, sans progression locale ni synchronisation automatique.
- [ ] Saisie temporaire liée à l’onglet, participation/étape/version ; restauration après rafraîchissement, suppression après validation confirmée ou expiration et aucune soumission automatique (TRE-ARB-76).
- [ ] Modèles de réponse explicites et constructeurs dédiés par public, champs autorisés énumérés et tests de non-divulgation (TRE-ARB-77).
- [ ] Journal d’audit commun raccordé à l’existant, corrections par nouvelles traces, corrélations et vues ERP filtrées ; conservation applicable (TRE-ARB-78).
- [ ] Purge quotidienne configurable par lots reprenables, protections revérifiées, rapport et signalement des échecs (TRE-ARB-79).
- [ ] Modifications après publication selon la phase : recontrôles avant démarrage, début figé ensuite, prolongation/capacité et réouverture explicite des inscriptions avant fin ; inscrits préservés, gel respecté et audit.
- [ ] Départ et finale virtuels ou physiques au choix de l’organisateur, contrôles du lieu et preuves requises préservés (TRE-ARB-60).
- [ ] Durée estimée et difficulté renseignées, conseils/avertissements non bloquants ; références ajustées après le pilote (TRE-ARB-61).
- [ ] Passages actuellement valides en principal, annulations et historique séparés, sans doublon ni modification du gel (TRE-ARB-62).
- [ ] Tests métier/contrats à chaque évolution et scénarios entre applications par parcours terminé ; recette complète avant ouverture et contrôles obligatoires des dépôts maintenus (TRE-ARB-82).
- [ ] Recette de bout en bout et pilote sur une commune, une chasse et quelques commerces/POI : essai interne puis petit groupe de familles avant ouverture ; lieux/calendrier/participants à sélectionner (TRE-ARB-63).
- [ ] Bilan qualitatif du pilote : compréhension, faisabilité, scans, reprise et charge commerçante ; anomalies bloquantes corrigées et parcours concernés retestés avant ouverture (TRE-ARB-83).

- [ ] Missions de préparation : idéalement deux variantes par commerce, exigences/produits/messages à confirmer, contenus et aides cohérents, une seule position par commerce (TRE-ARB-89).
- [ ] Raccorder invitations EPIC 56 : relecture organisateur, choix unique et confirmations explicites, versions, refus, échéances, relances et audit ; aucun accord dans le résultat IA.
- [ ] Stabiliser le parcours selon réponses, supports à fournir et checklist de mise en place ; assembler seulement les missions retenues. Publication impossible avec attente, engagement périmé ou préparation manquante ; minimum de commerçants fixé par chasse ; sous ce seuil, publication bloquée et adaptation/annulation explicite par l’organisateur, sans annulation automatique.
- [ ] Tester retrait avant lancement, modification après accord, duplications sans consentement, non-divulgation et courses avec réponse/publication/annulation ; adapter Animation/ERP et application Commerçant.

## Préparation et évolutions ultérieures

- [ ] Comparer les fournisseurs IA pendant le développement V1, sur les mêmes briefs ; intégrer le fournisseur retenu après le pilote, avec les mêmes contrats et contrôles (TRE-ARB-84, choix 25.B).
- [ ] Après V1, cadrer en priorité le rallye à ordre libre comme prochain type d’animation ; conserver le profil linéaire de la Chasse V1 (TRE-ARB-85, choix 26.C).
- [ ] Après V1, concevoir l’adaptation contrôlée vers un nouveau brouillon dans une autre commune : lieux remplacés, faits revus, nouvelles validations et provenance conservée (TRE-ARB-86, choix 27.A).

La comparaison fournisseur prépare la suite pendant le développement. Le traitement manuel reste celui de la V1 ; intégration IA réelle, rallye et adaptation intercommunes ne sont pas des fonctionnalités requises pour la première livraison.

## References de suivi

- [Registre TRE-ARB-01 a TRE-ARB-89](../../specifications/moteur-animation/localeo_animation_engine_spec.md#arbitrages).
- [Besoins PRD-520 a PRD-532 et lots proposes](../../specifications/moteur-animation/localeo_animation_engine_spec.md#livraison).
- [Compléments de conception](../../specifications/moteur-animation/localeo_animation_engine_spec.md#questions-ouvertes).
- [Recette et criteres de livraison](../../specifications/moteur-animation/localeo_animation_engine_spec.md#recette).
