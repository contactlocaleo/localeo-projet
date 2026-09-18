# Backlog Epic 55 - Moteur commun et chasse au tresor commercante

## Suivi

- Criticite : `Moyenne`.
- Statut : `En cours - arbitrages et conception technique à finaliser`.
- Catalogue V1 : `PASSEPORT_COMMERCANT`, `TOMBOLA_LOCALE`, `CHASSE_TRESOR_COMMERCANTE`.
- Dependances : Epics 41, 42, 46, 47 et 49.

La [specification detaillee unique](../../specifications/moteur-animation/localeo_animation_engine_spec.md) porte les regles, les decisions, les contrats proposes et la recette. Cette fiche conserve uniquement le suivi de livraison.

## Livraison proposee

- [ ] Modele Animation generique : inscription, periode, territoire, publication et participation.
- [ ] Nouvelles animations : inscriptions dès publication, fermeture à la fin ou anticipée, capacité facultative atomique ; reprise des inscrits conservée et règles historiques préservées à la migration.
- [ ] DSL JSON avec enveloppe `common` et bloc `engineConfig` valide par le moteur du type.
- [ ] Registres et trois moteurs specialises avec trois renderers : Passeport, Tombola, Chasse.
- [ ] Migration des animations existantes : inventaire, conversion deterministe, simulation sans ecriture, comparaison et bascule coordonnee ; preservation des donnees et historiques.
- [ ] Bascule des brouillons et nouvelles animations ; événements historiques publiés/en cours conservés jusqu’à clôture puis migration, routage unique par animation pendant la transition.
- [ ] Cinematique complete de generation, prompt final persiste/exportable et dernier appel IA bouche.
- [ ] Provider de template Passeport : prompt genere, execution externe manuelle, depot et publication du resultat.
- [ ] File ERP des demandes de creation de chasse : statuts, export du prompt, controles, publication manuelle du resultat, reprise et lien vers instance.
- [ ] Finalisation idempotente de creation, distincte de publication publique de l’animation.
- [ ] Quota de génération partagé par partenaire : 10/mois configurables dans l’ERP, réservation à la demande, consommation au résultat accepté, libération sur annulation préalable et corrections sans double décompte.
- [ ] Parcours de chasse linéaire à ordre imposé ; cible de 5 à 8 étapes avec avertissement non bloquant ; défis QCM et information uniquement.
- [ ] Lieux/défis futurs masqués ; commerce nommé et localisé au déblocage, défi sur place ; une seule étape par commerçant.
- [ ] Runtime de chasse : scan avant/apres resolution, indice et aide de resolution distincts disponibles apres une premiere mauvaise reponse, POI et qualification.
- [ ] Information confirmée par « Continuer » sous réserve des autres conditions ; orientation par adresse et lien cartographique externe sans suivi de position Localeo.
- [ ] Retrait d’etape uniquement global en V1, conservation des autres acquis et recalcul equitable ; aucune dispense individuelle.
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
- [ ] Récupération par lien email existant sans nouvelle participation ; génération décomptée sur le mois réservé, demandes sans expiration automatique et ancienneté ERP visible.
- [ ] Conservation : prompts/réponses inutilisés 30 jours après terminaison/annulation, essais détaillés 90 jours après fin ; purge automatique avec exclusions, reprise et rapport ERP, registre interne à aligner.
- [ ] Recette de bout en bout et pilote terrain.

Le fournisseur IA reel sera branche ensuite sur le meme contrat. Aucun appel IA reel n'est requis pour la premiere livraison.

## References de suivi

- [Registre TRE-ARB-01 a TRE-ARB-53](../../specifications/moteur-animation/localeo_animation_engine_spec.md#arbitrages).
- [Besoins PRD-520 a PRD-532 et lots proposes](../../specifications/moteur-animation/localeo_animation_engine_spec.md#livraison).
- [Compléments de conception](../../specifications/moteur-animation/localeo_animation_engine_spec.md#questions-ouvertes).
- [Recette et criteres de livraison](../../specifications/moteur-animation/localeo_animation_engine_spec.md#recette).
