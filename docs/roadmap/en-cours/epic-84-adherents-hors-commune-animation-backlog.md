# EPIC 84 — Inviter les adhérents hors commune à une animation

**État produit · En cours.** Cadrage du 24 novembre 2026. Cette epic reprend l’amorce `E73-EVO-ADHERENTS-HORS-COMMUNE` et ses identifiants HC. Elle suit le parcours complet, du fichier d’adhérents à l’étape jouée en magasin, avec une recette propre. [Roadmap commune](../README.md) · [Socle de gestion des commerçants E73](../../specifications/epic-73-animation-et-ou-coffrets/gestion-commercants-animation.md) · [Accords de participation E56](../../specifications/epic-56-validation-participation-commercants-animation/README.md). [Spécification E84](../../specifications/epic-84-adherents-hors-commune-animation/README.md).

## Besoin et décisions

Le CEJ de Martignas-sur-Jalle compte parmi ses adhérents des commerçants de Saint-Jean-d’Illac. Son gestionnaire doit pouvoir les référencer à leur véritable adresse et les inviter à la même animation que les commerces de Martignas. Chaque établissement décide de sa participation. Les habitants retrouvent ensuite l’événement depuis les communes participantes.

Le CEJ conserve une seule souscription, une commune de pilotage et un dossier par animation. Le rattachement individuel des adhérents extérieurs est direct et sans quota. Cette version conserve le ciblage actuel des notifications aux habitants. La facturation et les droits Coffrets gardent leur périmètre.

## Critères d’acceptation

| Critère | Action et résultat observable |
| --- | --- |
| HC-01 · Saisie | Dans **Commerçants**, la commune et le code postal de pilotage sont préremplis. **Choisir une autre commune** permet une recherche par nom ou code postal. Le gestionnaire sélectionne la commune réelle et enregistre l’établissement dans son réseau. Sa commune apparaît dans la liste et le sélecteur d’invitation. |
| HC-02 · Import mixte | Un gestionnaire habilité importe un CSV ou un fichier Excel XLSX mêlant les deux communes. Pour chaque ligne, l’aperçu indique la commune reconnue et l’action proposée (création, rattachement, complétion ou vérification Localeo). Les lignes prêtes peuvent être confirmées ensemble et les autres reprises ultérieurement. |
| HC-03 · Identité | Si commune, SIRET et email concordent avec une fiche existante, la saisie et l’import réutilisent cette fiche. Une répétition ou un réimport conserve une fiche et un seul lien au réseau. Localeo traite les ambiguïtés et corrections d’identité. La réponse au CEJ protège les données des commerces extérieurs à son périmètre. |
| HC-04 · Éligibilité | Le CEJ peut sélectionner les commerces actifs et autorisés pour Animation de sa commune ainsi que ceux explicitement rattachés à son réseau. À confirmation du lot, une fiche complète qui remplit les conditions d’activation Animation devient sélectionnable. Le rapport distingue **Sélectionnable pour une animation** et **À compléter**. Une ligne en vérification reste identifiable comme telle. |
| HC-05 · Invitation et agendas | Le CEJ choisit ses destinataires et suit les réponses dans un dossier unique. Chaque commerce accepte ou refuse pour cette animation. Une fois publiée, elle apparaît dans l’agenda de pilotage et dans celui de chaque commune publiée dans Live où au moins un établissement a une participation acceptée et valide. Un habitant qui suit les deux villes voit une seule fiche et dispose d’une seule inscription. |
| HC-06 · Première connexion | Confirmer un import ou le rejouer, même avec des emails renseignés, ne crée aucun identifiant Pro, aucun jeton de première connexion et aucun email sortant. Le gestionnaire déclenche explicitement l’invitation à initialiser l’accès Pro. Il choisit séparément les destinataires de la demande de participation depuis l’animation. |
| HC-07 · Participation en magasin | Même si sa ville n’a aucune souscription Animation, l’adhérent peut se connecter à Pro, répondre à sa propre invitation, consulter sa mission et accéder à son kit au stade prévu. Pour une chasse au trésor, le CEJ peut placer une étape dans son établissement, la publier et un joueur peut l’y réaliser. |
| HC-08 · Retrait | Avant confirmation, le gestionnaire voit quelles invitations en attente du CEJ seront annulées. Le retrait du réseau conserve les participations acceptées, la fiche partagée, le compte Pro, les Coffrets et les liens avec les autres associations. Si le dernier commerce participant d’une ville extérieure quitte ensuite l’animation, celle-ci disparaît de l’agenda de cette ville. |
| HC-09 · Renouvellement | Au renouvellement de la souscription pour le même partenaire et la même commune de pilotage, le gestionnaire retrouve ses adhérents et peut les sélectionner pour de nouvelles invitations selon leur éligibilité. |

**25 novembre 2026 · HC-03-ERP.** Pour instruire une vérification d’identité, le support Localeo peut retrouver un établissement par son SIRET dans la liste Commerçants de l’ERP. La recherche par nom ou login et les habilitations de consultation restent applicables. [Parcours et preuves](../../specifications/epic-84-adherents-hors-commune-animation/README.md#recherche-par-siret-dans-lerp)

**25 novembre 2026 · HC-04-SÉLECTION.** À la création d’une animation, le gestionnaire parcourt directement les commerces locaux et les adhérents extérieurs de son réseau. Une case décochée à l’ouverture permet de restreindre la liste à la commune de pilotage. Le filtre préserve les choix déjà effectués et le compteur indique les adhérents sélectionnés hors commune. [Sélection à la création](../../specifications/epic-84-adherents-hors-commune-animation/README.md#sélection-à-la-création)

## Recette de référence

1. Préparer trois commerces fictifs : un commerce local à Martignas, un adhérent extérieur à Saint-Jean-d’Illac et un commerce de Saint-Jean-d’Illac extérieur au CEJ.
2. Exercer la saisie et l’import, puis réimporter le fichier. Vérifier les communes, l’unicité des fiches et rattachements, la confirmation partielle d’un lot ambigu et l’absence d’email en file.
3. Inviter les deux premiers établissements. Vérifier que le troisième est exclu du sélecteur et que le backend refuse une tentative d’invitation directe. Suivre le premier accès Pro sur invitation explicite, l’accord de l’adhérent et une étape effectivement jouée dans son magasin.
4. Vérifier l’agenda avant et après publication, la déduplication pour un habitant des deux villes, le retrait avec invitation en attente puis le retrait après acceptation. Renouveler la souscription et retrouver le réseau.

## Impacts et preuves attendues

| Sujet | Travail à prévoir pour la livraison |
| --- | --- |
| Backend et données | Référencement porte le lien organisation, commune de pilotage et établissement. Animation porte l’accord par événement. Vérifier le rattachement atomique, les reprises et la migration additive sur des commerces et animations historiques. |
| Applications et contrats | Synchroniser le backend producteur et ses consommateurs pour la saisie, l’aperçu et le résultat d’import, la sélection, le retrait, la mission Pro et l’agenda Live. Contrôler les habilitations en lecture et en écriture, y compris lors de la reprise d’un lot. |
| Démonstration et exploitation | Représenter les trois commerces de recette dans les données de démonstration. Documenter le diagnostic d’une ligne en vérification et la reprise après correction par Localeo. |
| Guides utilisateur | Actualiser le [guide Animation](../../produit/formation/animation/guide-quotidien-animation.md) pour la saisie, l’import et le retrait, et le [guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md) pour l’accès Pro et la mission hors commune. Vérifier les captures, les PDF et leurs copies embarquées lors de la livraison. |

## État des preuves

Les parcours HC-01 à HC-09 sont implémentés. Les vérifications locales couvrent le lot mixte et son réimport sans email, le retrait concurrent avec une réponse, l’étape de chasse jouée chez un adhérent extérieur, la visibilité dans les deux villes et le renouvellement réel de la souscription sur une base de test. Le générateur de démonstration a également produit les trois commerces de référence et le sélecteur a retourné les deux commerces attendus. L’epic reste en cours jusqu’à sa revue de clôture. [Spécification et preuves par critère](../../specifications/epic-84-adherents-hors-commune-animation/README.md#preuves-de-comportement)
