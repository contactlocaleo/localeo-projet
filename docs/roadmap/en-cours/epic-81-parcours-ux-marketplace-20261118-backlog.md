# EPIC 81 — Clarté des parcours publics Marketplace (workshop du 18 novembre 2026)

## Références

[Spécification canonique](../../specifications/epic-81-parcours-ux-marketplace/README.md) · [Bilan de réalisation locale](../../specifications/epic-81-parcours-ux-marketplace/bilan-realisation.md) · [Protocole de recette Stripe TEST](../../specifications/epic-81-parcours-ux-marketplace/recette-stripe-test.md).

- **État produit : En cours.** Cadrage issu du [workshop Marketplace](../../ux-workshops/marketplace/2026-11-18/README.md), de son [backlog UX](../../ux-workshops/marketplace/2026-11-18/workshop/backlog-ux.md), de ses [observations factuelles](../../ux-workshops/marketplace/2026-11-18/observations/observations-factuelles.md) et des [sept décisions VALIDÉE du propriétaire](../../ux-workshops/marketplace/2026-11-18/validation/decisions.md). Les votes de douze rôles sont simulés ; ils ne constituent ni tests utilisateurs ni décision de livraison.
- **Identifiant :** `EPIC 81`, recherché le 18 novembre 2026 dans la roadmap et les spécifications, y compris les namespaces applicatifs, sans occurrence antérieure.
- **Priorités d'origine :** O-08 P0 comme porte de recette, sans défaut Stripe démontré ; O-01/O-02/O-03/O-06/O-07 P1 ; O-05 P1 seulement si des contenus provisoires figurent dans l'environnement d'ouverture, sinon entretien éditorial P2.
- **Epics voisines :** [EPIC-MARKETPLACE-54](../a-faire/epic-marketplace-54-harmonisation-identite-visuelle-marketplace-backlog.md) traite la continuité de marque et sa recette, sans porter ces sept décisions de parcours ; [EPIC 18](../terminees/epic-18-page-commercant-immersive-backlog.md) et [EPIC 49](../terminees/epic-49-animations-marketplace-backlog.md) conservent leur clôture. EPIC 81 cadre les corrections et preuves issues du nouvel audit, sans rouvrir leurs périmètres historiques. [EPIC 42/Live](../terminees/epic-42-localeo-live-grand-public-backlog.md) est une dépendance de navigation.

## Problème et résultat attendu

**Observé en TEST :** l'accueil mobile n'explicite pas immédiatement le parcours multi-prestations chez les commerçants ; sur la fiche coffret, garantie, exemples, validité, réservation, cadeau et conditions d'achat sont dispersés ; les liens d'animation conduisent vers Localeo Live sans annoncer systématiquement ce passage ; des contenus commerçants provisoires existent en TEST. Le [parcours d'achat](../../ux-workshops/marketplace/2026-11-18/observations/parcours-achat-stripe.md) a été arrêté avant le bouton final, car l'initialisation crée un achat et une session avant redirection. **Aucune panne de paiement et aucun contenu provisoire en production ne sont établis.**

**Hypothèses à vérifier :** un visiteur pourrait confondre le coffret avec un colis ou une carte cadeau générique, surestimer les prestations garanties, hésiter sur le destinataire du cadeau ou perdre son repère vers Live. Les effets sur la conversion et la compréhension n'ont pas été mesurés auprès de vrais utilisateurs.

**Résultat attendu :** un visiteur, notamment sur téléphone, comprend le coffret comme un parcours d'expériences locales auprès de plusieurs commerçants, distingue ce qui est garanti de ce qui est illustratif, connaît les conditions décisives et le circuit du cadeau avant l'action d'achat, puis comprend quand la consultation des animations se poursuit dans Live. La décision d'ouverture s'appuie sur une recette contrôlée de la frontière Stripe et sur le catalogue réellement publié.

## Périmètre

- **Lot 1 — Offre et décision d'achat :** O-01 sur l'accueil ; O-02 sur la promesse de la fiche coffret ; O-03 sur l'envoi et l'usage du cadeau ; O-07 sur les conditions avant le bouton. Une seule source de vérité éditoriale doit éviter les formulations contradictoires entre la fiche, le formulaire, les CGV et les messages effectivement envoyés.
- **Lot 2 — Découverte des animations :** O-06, libellés de destination vers Localeo Live, distinction consultation/participation, conservation de la commune et retour identifiable.
- **Lot 3 — Contenu et preuve de lancement :** O-05, inventaire du catalogue dans l'environnement d'ouverture et correction des seuls contenus provisoires qui y sont effectivement présents ; O-08, protocole puis recette isolée de l'initialisation, de la redirection et du retour Stripe avec effets métier maîtrisés.
- **Exclusions :** paiement réel, modification des règles de commercialisation ou de réservation, nouvelles prestations promises, refonte graphique totale, intégration de Live dans Marketplace, nouvelle recherche ou nouvelle entrée commune O-04 (P2, non validée par le propriétaire), O-09 rejetée et O-10 non adoptée.
- **Contraintes :** préserver l'identité Localeo et les composants utiles ; vérifier les libellés contre le comportement réel et les textes juridiques ; maintenir la lisibilité mobile et l'accessibilité ; traiter les résultats de recette Stripe comme preuves ou anomalies à qualifier, non comme défauts présumés.

## Critères d'acceptation

| Critère | Orientation et acteur/préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E81-CA-01 | O-01 ; visiteur sur mobile 320, 390 ou 430 px | Ouvrir l'accueil | Le premier écran décrit un **parcours d'expériences locales chez plusieurs commerçants** et donne une action vers les coffrets, avec un accès distinct aux animations ; aucun vocabulaire ne suggère un colis matériel ou une simple carte cadeau générique. |
| E81-CA-02 | O-02 ; visiteur sur une fiche coffret publiée | Lire le prix et la proposition avant achat | Le droit garanti, les exemples seulement indicatifs, la durée de validité et la nécessité éventuelle de réserver sont identifiables au point de décision et cohérents avec le contrat et les prestations actives ; un exemple n'est pas présenté comme une garantie. |
| E81-CA-03 | O-03 ; acheteur d'un coffret à offrir | Lire la fiche avant de saisir ses coordonnées | La chronologie paiement → réception → préparation éventuelle de la carte → usage par le bénéficiaire, le destinataire de chaque message et le rôle du téléphone sont expliqués conformément aux comportements vérifiés ; aucune étape ou notification fictive n'est promise. |
| E81-CA-04 | O-07 ; visiteur à 390 ou 1440 px | Atteindre l'action finale d'achat | Prix total, validité, réservation et liens CGV/confidentialité sont consultables **avant** l'action ; le résumé ne contredit ni la fiche ni les textes juridiques et ne déclare pas le paiement déjà testé. |
| E81-CA-05 | O-06 ; visiteur dans les animations d'une commune | Ouvrir une animation ou son agenda | La destination « Localeo Live » et la différence entre consulter et participer sont annoncées avant le départ ; la commune reste sélectionnée et un retour vers son contexte Marketplace est identifiable, sous réserve des actions réellement offertes par Live. |
| E81-CA-06 | O-05 ; responsable du catalogue d'ouverture | Inventorier communes, commerces et coffrets publiés | Le relevé distingue TEST et l'environnement d'ouverture ; aucun nom ou texte provisoire ne subsiste dans ce dernier. Si aucun placeholder n'y est observé, le correctif de contenu P1 est clos comme sans changement requis et l'entretien passe en suivi P2. |
| E81-CA-07 | O-05 ; commerçants partenaires échantillonnés | Relire leur fiche et les prestations liées | Les descriptions, images et prestations présentées sont confirmées ou corrigées avant publication, avec droits d'usage des visuels vérifiés ; la maquette d'audit ne vaut pas validation du contenu. |
| E81-CA-08 | O-08 ; équipe de recette sur environnement TEST autorisé | Préparer la recette du bouton final | Les effets de `POST /public/gestion-achats/paiements/initialiser`, les données, l'isolation, les nettoyages et l'innocuité sont établis **avant** tout appel ; aucune donnée bancaire, commande ou facturation réelle n'est engagée. Si l'innocuité n'est pas établie, l'appel n'est pas exécuté et la porte reste ouverte. |
| E81-CA-09 | O-08 ; recette isolée et autorisée | Initialiser puis suivre session, redirection et retours | Des preuves distinctes documentent succès, échec/annulation, reprise/idempotence et état de commande ; toute anomalie bloquante est corrigée puis revérifiée ou l'ouverture est reportée. Une absence de preuve n'est pas présentée comme succès. |
| E81-CA-10 | O-01/O-02/O-03/O-06/O-07 ; panel de vrais visiteurs dont personnes peu familières du numérique | Accomplir les six scénarios du [plan de tests](../../ux-workshops/marketplace/2026-11-18/synthese/plan-tests-utilisateurs.md) | La reformulation du produit, la distinction garantie/exemples, le cadeau et le passage Live sont observés avec consignes neutres ; les échecs et hésitations sont consignés, sans transformer les votes simulés en validation d'usage. |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Applications et domaine propriétaire | **Concerné :** `localeo-marketplace` pour accueil, fiche, formulaire et liens. **À examiner :** `localeo-backend` propriétaire des règles d'achat, garantie, données publiques et initialisation ; `localeo-animation` seulement si le retour ou l'entrée Live requiert un contrat de navigation. `localeo-commercant` seulement si O-05 impose une correction des contenus à leur source. Aucune règle métier nouvelle n'est arbitrée. |
| API et consommateurs | **À examiner :** payload public de coffret/prestations, destination et contexte commune vers Live, contrat d'initialisation et de retour Stripe ; identifier les consommateurs avant tout changement. Les libellés seuls ne justifient pas un changement d'API. |
| Persistance, migrations et données existantes | **À examiner :** O-05 peut demander correction de données éditoriales ; O-08 crée des objets d'achat en TEST lors d'une recette autorisée. Aucune migration décidée au cadrage. |
| Générateur de démonstration et fixtures | **À examiner :** les contenus provisoires vus en TEST peuvent provenir du jeu de démonstration ; conserver des données de test identifiables sans les confondre avec un catalogue de lancement. |
| Documentation fonctionnelle | **Concerné :** promesse du coffret, cadeau, réservation, validité, CGV et parcours Live à confronter aux [spécifications](../../specifications/INDEX.md) et aux textes publiés. Les maquettes sont des références d'intention, pas des contrats. |
| Exploitation et déploiement | **Concerné :** contrôle des contenus réellement ouverts et porte de recette Stripe avant décision de lancement ; définir environnement de test, jeux de données, preuves, traitement des anomalies et responsable du GO. Aucun déploiement demandé par ce cadrage. |

## Questions ouvertes

1. Quelle formulation contractuelle exacte couvre la garantie, les exemples, la réservation et la validité de chaque type de coffret ? La spécification du lot 1 et la revue juridique en dépendent ; **l'orientation UX est déjà validée**.
2. Quels e-mails et SMS sont effectivement envoyés, à qui et quand, et comment la carte cadeau et l'activation fonctionnent-elles ? Vérifier le code et les textes avant de figer O-03.
3. Quels liens de retour et quelles actions de participation Live sont réellement disponibles par type d'animation ? O-06 doit s'y adapter, sans promettre une inscription inexistante.
4. Quel environnement et quelles communes/coffrets/commerces seront ouverts au public ? Cette vérification décide si la correction O-05 reste P1 ou devient suivi P2.
5. Quel protocole TEST rend l'appel de création d'achat et de session Stripe sans effet financier ou métier indésirable ? La recette O-08 ne peut commencer avant réponse documentée.

## Passage à la spécification

Les [critères du cycle d'epic](../../organisation/cycle-epic.md#spécifier) s'appliquent au prochain lot : confirmer les comportements et propriétaires des règles, les contrats et consommateurs, la source des contenus, les états d'erreur et d'accessibilité, puis relier chaque critère E81-CA à des preuves ciblées. Ce fichier est un **cadrage** ; ni spécification détaillée, ni implémentation, ni recette Stripe n'a été réalisée par sa création.
