# Epic 41 - Plateforme d'animation locale MVP

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : concevoir et developper un MVP exploitable du `Passeport commercant`, tout en posant un socle generique minimal pour creer, configurer, publier, piloter, cloturer et analyser des animations territoriales.
- Domaine fonctionnel cible : `animation_locale`
- Animation de reference MVP : `Passeport commercant`
- Decision produit : le MVP ne doit pas developper une collection de jeux, mais poser les fondations d'un moteur d'animation reutilisable.
- Decision architecture : la plateforme d'animation est un domaine metier distinct de la marketplace, mais elle consomme les donnees et services du core Localeo sans les dupliquer.
- Decision de cadrage : le MVP inclut une plateforme partenaire dediee en self-service pour creer et gerer les animations.
- Decision de cadrage : la plateforme partenaire dediee est la surface produit principale des organisateurs et partenaires ; Localeo n'est pas en charge de creer les animations, mais conserve une supervision et des droits d'administration exceptionnels.
- Decision de cadrage : l'organisateur dispose dans la plateforme partenaire d'une vision live de ses animations pour suivre l'etat, les inscriptions, les validations, la progression, les qualifications, les alertes et les actions disponibles.
- Decision de cadrage : le gestionnaire doit voir rapidement ou se situe chaque animation dans le workflow global : creation, configuration, publication, animation en cours, cloture, tirage, envoi des gains, bilan et archivage.
- Decision de cadrage : le gestionnaire dispose d'un dashboard de performance pour mesurer et comparer ses animations sur ses tenants communes habilites.
- Decision de cadrage : Localeo dispose d'une vision live des animations de la plateforme pour superviser l'activite, detecter les blocages et intervenir en support, sans animer ni creer les animations.
- Decision de cadrage : le gestionnaire d'animation, organisateur ou partenaire habilite, est dans le coeur MVP ; les partenaires contributeurs/sponsors et les groupes de participants restent des extensions sauf besoin client signe.
- Decision de cadrage : le participant MVP ne cree pas de compte ; il s'inscrit avec son email depuis une page contextualisee par QR d'inscription et recoit un QR participant personnel par email.
- Decision de cadrage : le MVP inclut une application mobile participant pour consulter les animations en cours de sa commune, ses inscriptions actives, son historique, le detail d'une animation et son QR participant.
- Decision de cadrage : le tenant fonctionnel MVP est la commune ; il reference une commune du referentiel et porte le perimetre des animations, des droits gestionnaire et des vues participant.
- Decision de cadrage : une animation MVP appartient a un seul tenant commune ; les animations multi-communes ou territoires composes sont reportes hors MVP.
- Decision de cadrage : un gestionnaire peut etre habilite sur plusieurs communes des le MVP, avec selection explicite du tenant commune actif.
- Decision de cadrage : le role MVP `GESTIONNAIRE_ANIMATION` couvre le cycle nominal par tenant commune : creation, configuration, modification avant publication, publication, suivi live, cloture, tirage, envoi des gains, bilan et export.
- Decision de cadrage : les droits Localeo restent separes du role gestionnaire : supervision globale, correction support, administration exceptionnelle et gestion des abonnements ne sont pas accessibles au gestionnaire d'animation.
- Decision de cadrage : l'acces a la plateforme partenaire est payant et conditionne par un abonnement Stripe Billing actif, par formule, pour un partenaire donne et une commune donnee.
- Decision de cadrage : si un abonnement expire alors qu'une animation est publiee ou en cours, l'animation va a son terme avant cloture des acces ; les nouvelles actions payantes peuvent etre bloquees selon les droits.
- Decision de cadrage : lorsque l'animation est terminee ou cloturee, le gestionnaire peut lancer un tirage au sort depuis la plateforme partenaire, sur une population eligible figee.
- Decision de cadrage amendee par l'Epic 56 : les lots a gagner sont obligatoirement des coffrets Localeo actifs de la commune de l'animation ; ils font partie de son budget et sont achetes par le partenaire, apres acceptation des commercants et avant publication.
- Decision de cadrage : l'envoi d'un gain au vainqueur cree et active automatiquement la `CoffretInstance` du coffret gagne, rattachee au gain d'animation.
- Decision de cadrage : l'organisateur peut suivre la consommation des coffrets envoyes aux vainqueurs depuis la plateforme partenaire, sans dupliquer les regles `gestion_achats`.
- Decision de cadrage : la validation MVP utilise le QR participant scanne depuis l'application mobile commercant, qui devra evoluer pour gerer les animations ; ce QR reste distinct du QR coffret.
- Decision de cadrage : l'inscription participant collecte email, nom, prenom et telephone ; l'email de confirmation reprend les informations de l'animation et contient le QR participant directement dans le message.
- Decision de cadrage amendee par l'Epic 56 : le flyer PDF de communication est genere lors de la publication, une fois les commercants participants figes ; aucun flyer n'est disponible avant publication.
- Decision de cadrage : les gagnants sont notifies par email et push ; le push impose une application Localeo participant avec opt-in et abonnement push.
- Decision de cadrage : les donnees nominatives participant sont conservees jusqu'a fin d'animation + 12 mois, les QR/tokens jusqu'a fin + 3 mois, les validations detaillees 24 mois, les tirages/gains 5 ans sous forme pseudonymisee, les exports 90 jours maximum et les traces de notification 12 mois.
- Decision evolution : le modele doit rester extensible pour accueillir plus tard Escape Game, Rallye decouverte, Chasse au tresor, Roue des commercants, Quiz, Calendrier de l'Avent ou des animations generees par IA.

## Documents d'architecture

- [Architecture applicative EPIC 41 - Domaine animation locale](../../architecture/backend/epics/epic-41-animation-locale-architecture.md)
- [Analyse API de la maquette V2](../../specifications/epic-41-api/analyse-api-maquette.md)
- [Specifications techniques API EPIC 41](../../specifications/epic-41-api/README.md)
- [Actualites rattachees aux animations](../../specifications/epic-41-api/actualites.md)
- [Actualites - Specification Localeo Animation](../../specifications/epic-41-api/actualites-interface-animation.md)
- [Actualites - Specification Localeo Live](../../specifications/epic-41-api/actualites-localeo-live.md)
- Maquette UX de reference : `livrables/design/animation/localeo-animation-maquette-v2.zip` (la V1 est conservee comme historique).

## Arbitrages API

Source de verite : [registre des arbitrages API](../../specifications/epic-41-api/registre-arbitrages.md). Les decisions `ARB-01` a `ARB-69` sont validees et integrees.

### Identite, tenant et abonnement

- Le portail partenaire reutilise le mecanisme Localeo de token/session, adapte a un profil Animation distinct ; aucun fournisseur OIDC externe n'est introduit au MVP.
- Le contexte authentifie porte acteur, partenaire, roles et communes habilitees. La commune active est conservee en session et modifiable par une commande dediee ; toute ressource reste reverifiee cote serveur.
- `GESTIONNAIRE_ANIMATION` dispose de permissions fines. Une ressource hors tenant retourne `404`, une permission insuffisante dans le tenant retourne `403`.
- `abonnements_plateforme` devient un domaine transverse dedie. Un abonnement porte sur `partenaire + commune + formule` ; le multi-communes commercial est reporte.
- L'expiration bloque creation, publication et options payantes, mais une animation publiee ou en cours peut aller jusqu'a cloture, tirage, envoi des gains, bilan et export reglementaire.

### Participant et validation terrain

- Le participant MVP n'a pas de compte. Son acces web et mobile utilise un token opaque, revocable et expire ; l'unicite d'inscription est `animation_id + email_normalise`.
- L'email est verifie par l'utilisation du lien/QR personnel ; aucune verification SMS n'est requise au MVP.
- QR coffret et QR participant, ainsi que leurs routes de validation, restent distincts.
- Une seule validation effective est autorisee par participant et etape/commercant, sauf repetition declaree par le modele. Les soumissions identiques sont idempotentes.
- Le hors connexion commercant est exclu du MVP. Une validation erronee est annulee avec motif, jamais supprimee ; apres cloture, la correction est reservee a Localeo.

### Cloture, tirage et publication

- La cloture est automatique a la date de fin ou manuelle anticipee ; les deux chemins utilisent le meme use case atomique et idempotent.
- La population eligible est figee dans la transaction de cloture. Une validation concurrente posterieure au verrouillage est rejetee.
- Le gestionnaire ne peut pas rouvrir une animation. Localeo peut exceptionnellement la corriger avant tirage, avec motif, audit et regeneration des eligibles.
- Le tirage utilise un generateur cryptographiquement sur une population versionnee. Un participant ne gagne qu'un lot par tirage ; les lots suivent un ordre fige et des suppleants sont tires des l'origine.
- La publication rend atomiques l'etat et le QR d'inscription. Flyer et notifications sont asynchrones ; leur echec n'annule pas la publication.
- Une commande asynchrone retourne `202`, `operation_id`, `resource_id`, `status_url` et un etat initial. Son suivi utilise `GET /protected/animation-locale/operations/{operation_id}`.

### Live, documents, notifications et exploitation

- Le live MVP utilise un polling HTTP toutes les 15 secondes et un flux recent pagine par curseur.
- Les exports CSV UTF-8 sont synchrones jusqu'a 10 000 lignes, puis asynchrones. Ils sont telechargeables 7 jours, traces et supprimes automatiquement, sans jamais depasser 90 jours de conservation.
- Flyers, bilans et exports sont exposes par `animation_locale`, tandis que leur stockage et versionnement restent dans `documentaire`. Le portail ne voit que le flyer courant ; sa regeneration conserve le QR.
- Les assets passent par une route DAM protegee et sont seulement references par l'animation.
- Le portail dispose d'une inbox persistante ; les alertes de workflow restent derivees. Email obligatoire pour inscription, QR et gain, push optionnel avec opt-in, SMS hors MVP.
- Le support partenaire appartient a `support`, avec fil et rattachement facultatif a une animation, sans piece jointe au MVP.
- L'audit partenaire expose les evenements metier publiables et masque securite, corrections internes et donnees personnelles inutiles.
- Les listes stables utilisent `page/page_size` (25 par defaut, 100 maximum) ; live et audit utilisent un curseur.
- Les vues globales Participants, Validations, Tirages/Gains, Flyers et Bilans font partie du MVP.
- Localeo dispose d'une supervision live et d'un audit complet. SQLAdmin sert aux consultations simples ; toute correction metier passe par un use case/API interne audite.
- Les durees RGPD proposees restent soumises a validation juridique bloquante avant production.
- Les actualites d'animation reutilisent `activites_locales`, sont gerees depuis la fiche Animation, apparaissent sous `En direct > Animations` et utilisent la preference Live `ANIMATION` pour leur notification (`ARB-64`, valide).

### Arbitrages valides pour les actualites Animation

| ID | Decision integree | Consequence d'implementation |
| --- | --- | --- |
| `ARB-65` | Cibler les installations qui suivent la commune de l'animation ou une participation a cette animation, sous reserve de la preference `ANIMATION`. | La requete de ciblage realise l'union des deux audiences sans diffusion globale. |
| `ARB-66` | Si `ANIMATION` est active, creer l'inbox idempotente et tenter le Push uniquement avec un abonnement actif ; sinon ne creer ni inbox ni Push. | L'absence ou l'echec du Push ne supprime pas l'entree inbox autorisee. |
| `ARB-67` | Introduire `LOCALEO_FRONT_LIVE_ANIMATION_URL_TEMPLATE` avec `{animation_id}`, distinct du lien d'ajout d'une participation. | Le backend remplace le placeholder sans construire le chemin frontend. |
| `ARB-68` | Introduire `animation:gerer_actualites` et ne la reprendre sur une habilitation existante que si `animation:modifier` et `animation:publier` sont deja accordees. | Les gestionnaires complets recoivent le droit ; les profils en lecture ou personnalises restent inchanges hors condition. |
| `ARB-69` | Brouillon sur toute animation non archivee ; publication ou execution programmee seulement en `PUBLIEE`, `EN_COURS` ou `CLOTUREE`, avec rejet `409` apres archivage. | Les transitions et erreurs API suivent cette matrice de statuts. |

Toute evolution ulterieure doit etre ajoutee au registre sous un nouvel identifiant ou une nouvelle version de decision.

### Decisions techniques d'implementation

- Une session Animation distincte reutilise les composants techniques de la session commercant. Son token opaque reference une session serveur, expire apres 8 heures et ne porte aucune permission faisant autorite.
- `identite_acces` expose des routes propres au profil Animation pour connexion, consultation de session et deconnexion. Ces routes ne sont pas rattachees a `animation_locale`.
- Les partenaires, gestionnaires et habilitations sont persistants. Une habilitation relie gestionnaire, partenaire, commune, permissions, statut et periode de validite ; la session n'est pas la source de verite des droits.
- Le domaine Animation utilise des tables relationnelles dediees. JSON reste limite aux parametres variables des modeles, snapshots et audits.
- La cloture verrouille la ligne Animation et cree le snapshot eligible dans une transaction unique ; toute validation posterieure au verrouillage est rejetee.
- Le domaine `abonnements_plateforme` porte Offre, Abonnement, DroitAccesPlateforme et les evenements Stripe idempotents. Une activation administrative auditee est disponible avant le self-service.
- Les tokens publics et QR participant sont aleatoires, opaques, d'au moins 256 bits, encodes en Base64URL et stockes uniquement sous forme de hash. Le QR ne contient aucune donnee personnelle.
- Par amendement de `ARB-46`, email, telephone, nom et prenom ne sont pas chiffres au niveau applicatif au MVP. La securite repose sur les controles d'acces, la protection de l'infrastructure, le masquage, l'audit et les politiques de conservation. Ce choix doit etre reevalue avant production avec l'analyse de risques/RGPD.
- Les QR coffret et participant utilisent des chemins distincts. L'identite du commercant provient exclusivement de sa session.
- Les flyers sont generes avec ReportLab depuis un gabarit versionne et des polices embarquees. PDF et apercu PNG sont produits de facon asynchrone et stockes par `documentaire`.
- Les operations asynchrones utilisent `animation_operations`, BatchRunner/outbox, un backoff exponentiel borne, cinq tentatives maximum et une conservation de 30 jours.
- Les evenements Animation sont transformes en email ou push par `exploitation`. Chaque canal a son statut et ses relances ; un echec de notification n'annule pas la transaction metier.
- DAM expose un upload protege Animation pour PNG, JPEG et WebP, limite a 5 Mo, avec verification du contenu, quotas partenaire et rattachement a l'animation.
- Le support MVP est un fil texte, rattache facultativement a une animation. Les pieces jointes sont reportees.
- Le socle abonnement demarre avec une activation administrative auditee. Stripe est raccorde en environnement de test lorsque ses cles et son secret de webhook sont disponibles ; leur absence ne bloque pas le developpement du coeur Animation.
- Les emails d'inscription, de QR et de gain utilisent des gabarits versionnes. Leur contenu peut etre provisoire pendant le developpement ; expediteur, adresse de reponse et mentions de pied de page sont configurables et valides avant recette metier.
- Le flyer ReportLab utilise initialement des assets Localeo temporaires. Logos, polices, couleurs et mentions sont configurables par partenaire, puis le rendu de reference est fige avant recette visuelle.
- Les liens publics et QR utilisent deux templates complets configurables : `LOCALEO_ANIMATION_PUBLIC_URL_TEMPLATE` et `LOCALEO_ANIMATION_PARTICIPANT_URL_TEMPLATE`. Le backend injecte uniquement l'identifiant ou le token.
- L'application commercant forme un lot coordonne distinct du backend. Sa premiere version reconnait directement les chemins QR coffret et participant et gere les erreurs contractuelles, sans retrocompatibilite.
- Les durees RGPD validees pour le developpement sont configurables et couvertes par des tests de purge. Une validation juridique tracee demeure obligatoire avant production.
- `documentaire` fournit l'abstraction de stockage : backend local en developpement, stockage objet prive dans les environnements heberges, avec route protegee ou URL signee de courte duree. Fournisseur et retention sont figes avant recette d'infrastructure.

### Retours de branchement API de la maquette Figma

Le rapport [docs/specifications/epic-41-api/rapport-apis-manquantes.md](../../specifications/epic-41-api/rapport-apis-manquantes.md) est integre avec les decisions suivantes :

- Ajouter une `reference` pseudonymisee stable par animation aux projections participant ; ne plus utiliser `nom_affiche` comme identifiant principal des tableaux agreges.
- Ajouter l'export CSV des participants d'une animation, soumis aux droits, au masquage, a l'audit et a la purge documentaire.
- Ajouter `accroche` et `url_inscription` au flyer et documenter le telechargement securise par redirection temporaire ou streaming controle.
- Conserver les routes canoniques existantes du dashboard et de l'audit ; la maquette doit utiliser les prefixes `/protected/animation-locale`.
- Ajouter le remplacement motive d'un gagnant par son prochain suppleant et la relance idempotente de sa notification.
- Confirmer pagination serveur des participants, curseur de l'audit et filtres serveur des validations deja prevus.
- Accepter `q` comme alias de recherche sur les animations et `periode=7j|30j|12m` comme raccourci du dashboard, en plus des dates explicites.
- Le `PATCH /animations/{animation_id}` est partiel et couvre la configuration modifiable ; aucune operation PUT complete n'est imposee.
- Maintenir le polling live MVP ; SSE/WebSocket reste une evolution post-MVP.
- Ajouter en P2 l'export PDF du bilan, la lecture groupee des notifications et l'archivage groupe d'animations.

## Probleme

Localeo dispose deja d'une marketplace, de commercants references, de coffrets, de validations, de notifications et de surfaces back-office. Ces briques peuvent servir des animations territoriales, mais le backend ne porte pas encore un domaine dedie pour organiser une animation locale de bout en bout.

Sans moteur d'animation, chaque animation risque d'etre implementee comme un cas particulier, avec des regles, ecrans et objets difficiles a reutiliser. Le risque est de construire un `Passeport commercant` trop specifique, puis de devoir tout reprendre pour le prochain format d'animation.

## Vision

La plateforme d'animation locale doit devenir le moteur permettant a Localeo de proposer aux collectivites, associations de commercants, offices de tourisme et autres acteurs locaux des animations configurables autour des commercants et territoires.

Le `Passeport commercant` sert de premiere animation de reference pour valider :
- les concepts metier ;
- l'architecture technique ;
- les parcours gestionnaire d'animation, operateur Localeo, participant et commercant ;
- les regles de validation ;
- les lots, tirages et bilans.

## Principes d'architecture

- Le domaine `animation_locale` est independant du domaine marketplace.
- Le moteur d'animation ne duplique pas les donnees core.
- Les commercants, communes, coffrets, utilisateurs, notifications et mecanismes d'authentification restent fournis par les domaines existants.
- Le domaine animation conserve ses propres objets : animation, modele, participant, etape, validation, lot, tirage, bilan.
- Le tenant commune d'animation reference la commune du domaine `referencement` ; il ne la duplique pas.
- La gestion commerciale des abonnements plateforme ne doit pas etre enfouie dans `animation_locale` ; le domaine animation consomme un droit d'acces actif expose par un domaine ou service d'abonnement.
- Les integrations au core passent par des services applicatifs ou ports explicites.
- Le moteur doit rester compatible avec l'Epic 40 : package domaine/application dedie, paths API avec domaine et tag OpenAPI `Animation locale`.
- Les regles propres au `Passeport commercant` doivent etre configurees comme un modele d'animation, pas codees comme le seul fonctionnement possible.
- Le moteur doit separer le socle generique, la definition de modele et les strategies metier propres a chaque modele.
- Le `Passeport commercant` est implemente comme premiere strategie de modele, pas comme une logique enfouie dans tous les use cases du domaine.
- L'ajout d'un nouveau modele d'animation doit necessiter une nouvelle definition de modele et une strategie dediee, sans modifier les invariants communs du moteur.
- L'assistant IA de generation d'animations est un cas d'usage futur, pas un prerequis du MVP.

## Moteur generique d'animation

Le moteur d'animation doit etre concu comme un socle generique de cycle de vie, de configuration, de participation, de validation, de qualification, de tirage, de gains, de workflow et d'indicateurs. Les particularites d'un modele, comme le `Passeport commercant`, sont portees par une definition de modele et une strategie metier branchee sur ce socle.

### Socle generique

Le socle generique porte les invariants communs :
- creation d'une animation depuis un modele ;
- rattachement a un tenant commune ;
- cycle de vie et transitions ;
- droits gestionnaire et droits reserves Localeo ;
- abonnement et droit d'acces plateforme ;
- inscription participant ;
- QR d'inscription et QR participant ;
- validations d'etapes ;
- progression ;
- qualification ;
- tirage ;
- gains ;
- flyer ;
- bilan ;
- workflow ;
- live ;
- dashboard de performance ;
- audit ;
- conservation et anonymisation.

Ce socle ne connait pas les regles fines d'un modele particulier. Il orchestre les use cases et delegue les decisions variables a la definition de modele et a la strategie associee.

### Definition de modele

Une definition de modele decrit les capacites et contraintes configurables :
- code du modele ;
- libelle et description ;
- prerequis de creation ;
- types d'etapes supportes ;
- parametres configurables ;
- contraintes de publication ;
- regles de progression ;
- regles de qualification ;
- regles anti-fraude ;
- besoin ou non de commercants participants ;
- besoin ou non de QR participant ;
- compatibilite avec tirage, gains, flyer, live, bilan et dashboard ;
- type de lots autorises.

Exemple indicatif pour le `Passeport commercant` :

```json
{
  "code": "PASSEPORT_COMMERCANT",
  "requires_merchants": true,
  "requires_participant_qr": true,
  "qualification": {
    "type": "MIN_VALIDATIONS",
    "threshold": 5,
    "unique_merchant": true
  },
  "rewards": {
    "type": "COMMUNE_COFFRETS_ONLY"
  }
}
```

### Strategie de modele

Chaque modele actif dispose d'une strategie metier qui implemente les points de variation :
- verifier la configuration avant publication ;
- construire ou valider les etapes ;
- valider une action terrain ;
- calculer la progression ;
- qualifier un participant ;
- verifier les contraintes anti-fraude propres au modele ;
- calculer les indicateurs specifiques utiles au bilan et au dashboard.

Le moteur appelle la strategie via un registre de strategies par code modele. Au MVP, une seule strategie est necessaire : `PASSEPORT_COMMERCANT`.

### Frontiere MVP `Passeport commercant`

Doit rester dans le generique :
- cycle de vie ;
- droits ;
- abonnement ;
- inscription ;
- QR ;
- validation d'etape ;
- qualification ;
- tirage ;
- gain ;
- workflow ;
- live ;
- dashboard ;
- audit.

Doit rester specifique au `Passeport commercant` :
- une etape correspond a une visite ou validation chez un commercant ;
- les commercants doivent appartenir a la commune de l'animation ;
- la progression est calculee a partir des validations chez les commercants ;
- la qualification depend d'un seuil de validations ;
- les lots sont des coffrets actifs de la commune.

### Regle d'evolution

Le deuxieme modele d'animation doit pouvoir etre ajoute en declarant une nouvelle definition de modele et une nouvelle strategie, sans reecrire les use cases generiques de creation, publication, inscription, workflow, tirage, gains, bilan et dashboard. Si un nouveau modele impose de modifier massivement le socle, le moteur n'est pas assez generique.

## Cadrage MVP recommande

Le MVP doit prouver qu'un organisateur ou partenaire habilite peut lancer une animation territoriale simple depuis une plateforme partenaire dediee, la faire vivre sur le terrain et produire un resultat exploitable, avec une supervision possible par Localeo.

### Perimetre MVP coeur

- Creer un catalogue de modeles d'animations.
- Consulter et previsualiser les modeles disponibles.
- Creer une animation a partir d'un modele depuis la plateforme partenaire dediee.
- Definir l'organisateur sous forme de metadonnees, le tenant commune, les dates et le statut de publication.
- Verifier l'abonnement Stripe Billing actif pour le partenaire, la commune et la formule avant l'acces aux fonctions de gestion payantes.
- Configurer les regles du `Passeport commercant` : seuil de validation, fenetre d'ouverture, unicite par etape et qualification.
- Selectionner les commercants participants.
- Gerer une animation par le gestionnaire d'animation : modifier le brouillon, suivre les inscriptions, piloter les validations, cloturer et consulter le bilan.
- Afficher l'etat d'une animation dans le workflow global, avec etape courante, prochaines actions et blocages.
- Suivre en live l'etat d'une animation depuis la plateforme partenaire.
- Consulter un dashboard de performance des animations.
- Inscrire des participants.
- Generer un QR d'inscription public par animation, menant vers une page d'inscription contextualisee.
- Generer un flyer PDF de communication contenant le QR d'inscription, les informations de l'animation, la charte et le logo Localeo.
- Envoyer au participant un email de confirmation reprenant les informations de l'animation et contenant son QR participant personnel.
- Suivre la progression des participants.
- Fournir une application mobile participant listant les animations en cours de la commune, les animations auxquelles il est inscrit, son historique, le detail et le QR de participation.
- Valider des etapes chez les commercants via QR participant scanne depuis l'application mobile commercant.
- Appliquer des controles anti-fraude MVP.
- Qualifier automatiquement les participants selon les regles.
- Configurer les dotations et lots, obligatoirement sous forme de coffrets Localeo actifs de la commune de l'animation.
- Cloturer manuellement ou automatiquement une animation.
- Preparer et lancer un tirage simple apres fin ou cloture de l'animation, sur population eligible figee.
- Envoyer les gains aux vainqueurs et activer automatiquement les `CoffretInstances` lorsque le gain est un coffret.
- Suivre la consommation des coffrets envoyes aux vainqueurs : statut, activation, expiration, prestations consommees, prestations restantes et validations.
- Notifier les gagnants par email et notification push participant.
- Historiser les resultats.
- Produire un bilan d'animation.
- Exporter le bilan en CSV.
- Appliquer les regles de conservation, purge et anonymisation des donnees d'animation.

### Extensions post-MVP ou options a confirmer

- Generation d'animations par IA.
- Creation de modeles d'animations personnalises par les utilisateurs.
- Gestion avancee multi-utilisateurs de la plateforme partenaire dediee.
- Gestion avancee des partenaires contributeurs d'une animation.
- Gestion avancee des groupes de participants.
- Escape Game.
- Rallye decouverte.
- Chasse au tresor.
- Quiz.
- Calendrier de l'Avent.
- Marketplace d'animations.
- Personnalisation graphique avancee.
- Animations multi-scenarios complexes.
- Regles de scoring complexes ou temps reel avance.
- Relances et preferences de notifications multicanales avancees.
- Declinaisons image PNG/JPEG ou formats reseaux sociaux avances du flyer.
- Exports PDF ou bilans documentaires enrichis.
- Paiement de participation par les participants ou monetisation dediee d'une animation.
- Recouvrement et relances avancees des abonnements.

## Criteres de succes MVP

- Un organisateur ou partenaire habilite peut creer, configurer, publier, piloter et cloturer une animation `Passeport commercant` depuis la plateforme partenaire dediee, sans intervention developpeur ni creation par Localeo.
- Un gestionnaire peut identifier en quelques secondes l'etape courante d'une animation dans le workflow global, les etapes deja realisees, les etapes restantes, les blocages et les actions disponibles.
- Un gestionnaire peut mesurer la performance de ses animations depuis un dashboard agrege et filtrable.
- Un organisateur peut suivre en live l'etat de ses animations : statut, inscriptions, validations, progression, qualifies, tirages, alertes et incidents.
- Un gestionnaire d'animation ne peut voir, creer ou piloter que les animations des tenants communes auxquels il est habilite.
- Un gestionnaire d'animation dispose des droits nominaux de creation, configuration, publication, cloture, tirage, envoi de gains, bilan et export sur ses tenants communes, sans droits de supervision globale ni d'administration exceptionnelle Localeo.
- Un gestionnaire d'animation ne peut acceder aux fonctions payantes de la plateforme partenaire que si le partenaire dispose d'un abonnement actif pour la commune et la formule concernees.
- Un operateur Localeo peut superviser, corriger ou administrer exceptionnellement les animations creees en self-service.
- Un operateur Localeo peut consulter une vision live des animations de la plateforme, agregee et filtrable par commune : animations publiees, inscriptions, validations, qualifications, tirages, alertes et incidents.
- Un participant peut s'inscrire, retrouver sa progression et obtenir son statut de qualification sans compte client.
- Un participant peut scanner un QR d'inscription, saisir son email, valider son inscription et recevoir son QR participant par email.
- Un gestionnaire peut telecharger un flyer PDF pret a partager, contenant le QR d'inscription et les informations de l'animation dans la charte Localeo.
- Un participant peut utiliser l'application mobile pour voir les animations en cours de sa commune, ses animations actives, son historique, le detail d'une animation et son QR participant.
- Un commercant participant peut valider une etape de maniere controlee.
- Le systeme refuse les validations hors periode, hors commercant eligible, en doublon ou trop rapprochees selon les regles MVP.
- Un gestionnaire d'animation peut lancer un tirage simple apres fin ou cloture de l'animation, sur une population eligible figee.
- Le systeme bloque le tirage si l'animation n'est pas terminee ou cloturee, si la population eligible n'est pas figee ou si les lots ne sont pas configures.
- Un coffret gagne est automatiquement active lorsqu'il est envoye au vainqueur, sans attendre une activation manuelle.
- Un organisateur peut suivre la consommation des coffrets envoyes aux vainqueurs pour mesurer l'usage reel des gains.
- Les donnees personnelles d'animation sont conservees, purgees ou anonymisees selon une politique explicite et auditable.
- La plateforme partenaire dediee et le back-office Localeo peuvent consulter le bilan et exporter les donnees utiles.
- Les APIs respectent l'Epic 40 : paths `/public/animation-locale`, `/protected/animation-locale`, `/internal/animation-locale` et tag OpenAPI principal `Animation locale`.

## Concepts metier cibles

### `ModeleAnimation`

Definition reutilisable d'une animation. Il decrit les capacites du modele, les parametres configurables, les types de regles disponibles, les prerequis de publication et la strategie metier a utiliser.

Premier modele MVP :
- `PASSEPORT_COMMERCANT`

### `DefinitionModeleAnimation`

Contrat de configuration d'un modele. Il expose les capacites, prerequis, types d'etapes, regles de progression, regles de qualification, contraintes anti-fraude, besoins QR, compatibilite tirage/gains/flyer/dashboard et types de lots autorises. Cette definition doit etre versionnable fonctionnellement sans modifier les donnees historiques des animations deja creees.

### `StrategieModeleAnimation`

Point d'extension metier associe a un `ModeleAnimation`. La strategie verifie la configuration, construit ou controle les etapes, valide les actions terrain, calcule la progression, qualifie les participants et expose les indicateurs specifiques du modele. Au MVP, la seule strategie active est celle du `PASSEPORT_COMMERCANT`.

### `RegistreModelesAnimation`

Registre applicatif permettant de retrouver la definition et la strategie d'un modele a partir de son code. Il evite de disperser des conditions `if modele == ...` dans les use cases generiques.

### `TenantCommuneAnimation`

Perimetre fonctionnel d'une commune pour l'animation locale. Il reference une commune du domaine `referencement` et porte les droits, les filtres de navigation, les listes publiques et la supervision par commune. Au MVP, une animation appartient a un seul tenant commune.

### `DroitAccesPlateformeAnimation`

Droit consomme par `animation_locale` pour savoir si un gestionnaire peut acceder aux fonctions payantes de la plateforme partenaire. Il est derive d'un abonnement plateforme Stripe Billing actif, rattache a une formule, un partenaire donne et une commune donnee. Ce droit ne remplace pas les roles `identite_acces` : l'acces effectif combine authentification, habilitation tenant commune et abonnement actif.

### `AbonnementPlateforme`

Concept du domaine transverse dedie `abonnements_plateforme`, hors du coeur `animation_locale`. Il porte la formule souscrite, le partenaire, la commune, le statut, les dates de debut/fin, les informations Stripe Billing et le perimetre facture. Il doit etre consultable et modifiable par Localeo avec audit des changements.

### `Animation`

Instance concrete creee a partir d'un modele. Elle porte tenant commune, organisateur, dates, statut, configuration et cycle de vie.

Statuts indicatifs :
- `BROUILLON`
- `CONFIGUREE`
- `PUBLIEE`
- `EN_COURS`
- `CLOTUREE`
- `ARCHIVEE`
- `ANNULEE`

### `OrganisateurAnimation`

Acteur responsable de l'animation : collectivite, association de commercants, office de tourisme, structure Localeo ou partenaire. Au MVP, il doit pouvoir consulter le suivi live de ses animations depuis la plateforme partenaire.

### `GestionnaireAnimation`

Acteur habilite a creer, configurer, publier, piloter, cloturer et consulter le bilan de ses animations depuis la plateforme partenaire dediee. Il peut etre un organisateur ou un partenaire et il est rattache a un ou plusieurs tenants communes.

### `PartenaireGestionnaireAnimation`

Specialisation de `GestionnaireAnimation` pour le partenaire qui opere une animation dans le MVP.

### `PartenaireContributeurAnimation`

Acteur contribuant a une animation : financement de coffrets, animation d'un groupe de participants, consultation de statistiques ou relai local. Concept cible post-MVP sauf besoin client confirme.

### `CommercantParticipantAnimation`

Commercant rattache a l'animation. Il peut etre une etape, un point de validation, un sponsor ou un point de contact selon le modele. Au MVP, il doit etre eligible dans le tenant commune de l'animation, sauf exception explicitement administree.

### `ParticipantAnimation`

Personne inscrite a une animation. Elle porte son identite minimale, ses consentements, sa progression et son statut de qualification. Le rattachement a un groupe est optionnel et post-MVP par defaut.

### `InscriptionAnimation`

Inscription d'un participant a une animation. Au MVP, elle est creee depuis une page contextualisee par l'animation, avec saisie email et consentements minimaux.

### `QrInscriptionAnimation`

QR public rattache a une animation. Il renvoie vers la page d'inscription contextualisee de l'animation et peut etre imprime ou diffuse par le gestionnaire d'animation.

### `QrParticipantAnimation`

QR personnel rattache a l'inscription d'un participant. Il est envoye par email apres inscription, visible dans l'application mobile participant et utilise pour participer aux validations terrain. Il est distinct du QR coffret et de ses invariants `gestion_achats`.

### `FlyerCommunicationAnimation`

Support PDF genere pour aider le gestionnaire a promouvoir l'animation. Il reprend le logo et la charte Localeo, les informations publiques de l'animation, le QR d'inscription et l'URL d'inscription. Il est telechargeable depuis la plateforme partenaire et peut etre partage par le partenaire sur ses canaux de communication. Au MVP, le format cible est un PDF standard ; les declinaisons image pour reseaux sociaux sont post-MVP.

### `GroupeParticipantsAnimation`

Regroupement optionnel de participants : classe, equipe, entreprise, association, territoire, partenaire ou segment. Concept cible post-MVP sauf besoin client confirme.

### `EtapeAnimation`

Etape ou action a realiser dans l'animation. Pour le Passeport commercant, une etape correspond typiquement a une visite ou validation chez un commercant.

### `ValidationEtapeAnimation`

Preuve qu'un participant a valide une etape. Elle porte la source, le commercant, la date, le participant et les informations anti-fraude utiles.

### `DotationAnimation`

Ensemble de coffrets Localeo disponibles comme lots pour une animation.

### `LotAnimation`

Recompense individuelle ou groupee attribuable a un gagnant. Au MVP, un lot reference obligatoirement un coffret Localeo actif de la commune de l'animation depuis `commercialisation`. L'envoi du lot au vainqueur declenche la creation et l'activation automatique de la `CoffretInstance`.

### `TirageAnimation`

Operation de selection de gagnants parmi une population eligible. Au MVP, elle est lancee par le gestionnaire apres fin ou cloture de l'animation, avec parametres, population source et resultats historises.

### `GainAnimation`

Attribution concrete d'un lot a un gagnant apres tirage. Elle porte le participant gagnant, le coffret gagne, le statut d'envoi, les notifications et la reference `CoffretInstance`.

### `SuiviConsommationGainCoffret`

Vue de suivi d'un coffret gagne. Elle expose la `CoffretInstance` rattachee au gain, son statut, sa date d'activation, sa date d'expiration, les prestations consommees, les prestations restantes, les validations associees et les alertes utiles. Les statuts et validations restent portes par `gestion_achats`.

### `NotificationAnimation`

Trace des notifications liees a l'animation : inscription, progression, qualification, gagnant, cloture. Pour les gagnants, le MVP doit supporter email et notification push si le participant dispose d'un canal push actif.

### `VueLiveAnimation`

Vue operationnelle temps quasi reel d'une animation. Elle expose statut, periode, inscriptions, participants total, participants ayant termine l'animation, validations recentes, progression, participants qualifies, alertes, incidents et actions disponibles. Cote organisateur, elle est filtree sur ses animations et ses tenants communes ; cote Localeo, elle peut etre agregee sur toute la plateforme.

### `VueWorkflowAnimation`

Vue synthetique du cycle de vie global d'une animation. Elle indique l'etape courante, les etapes deja realisees, les etapes restantes, les blocages, les prerequis manquants et les actions disponibles selon le statut, les droits, l'abonnement et les regles metier. Elle est derivee des statuts et invariants du domaine ; elle ne remplace pas la machine d'etats.

### `PolitiqueConservationAnimation`

Politique de conservation, purge et anonymisation des donnees d'animation. Elle fixe les durees par type de donnee, les actions automatiques de fin de retention, les regles de pseudonymisation et les contraintes d'audit. Elle doit etre appliquee aux participants, inscriptions, QR/tokens, validations, tirages, gains, notifications, exports et vues de suivi.

### `BilanAnimation`

Synthese exploitable de l'animation : participants total, participants ayant termine l'animation, validations, completions, lots, statistiques par commercant et commune tenant. Les statistiques partenaire contributeur sont ajoutees si l'extension partenaire est activee.

### `DashboardPerformanceAnimation`

Vue analytique agregee permettant a un gestionnaire de mesurer la performance de ses animations. Elle consolide les indicateurs par periode, tenant commune, modele, statut et animation : animations creees, publiees, terminees, participants inscrits, participants ayant termine, taux de completion, validations, participants qualifies, tirages, gains envoyes, coffrets consommes et alertes de sous-performance. Elle respecte les droits par tenant commune et ne remplace pas le bilan detaille d'une animation.

## Parcours MVP

### 1. Catalogue de modeles

1. Le gestionnaire d'animation consulte les modeles disponibles.
2. Il previsualise le fonctionnement d'un modele.
3. Il selectionne un modele pour creer une animation.

### 2. Creation et configuration

1. Le gestionnaire d'animation cree une animation depuis la plateforme partenaire dediee.
2. Il definit l'organisateur.
3. Il selectionne le tenant commune parmi ses communes habilitees.
4. Il definit les dates.
5. Il selectionne les commercants participants.
6. Il configure les regles de progression et qualification.
7. Il configure les lots.
8. Il regle chaque ligne de lots au prix catalogue avec le checkout professionnel Stripe.
9. Le webhook de confirmation reserve les coffrets ; la publication reste bloquee tant que la couverture n'est pas complete.
10. Il genere ou previsualise le flyer PDF de communication avec le QR d'inscription.
11. Il publie l'animation.
12. L'operateur Localeo peut superviser, corriger ou administrer exceptionnellement l'animation si necessaire.

### 3. Gestion des partenaires contributeurs

Parcours sorti du coeur MVP sauf besoin client confirme.

1. Le gestionnaire d'animation invite un partenaire contributeur.
2. Le partenaire contributeur accepte l'invitation.
3. Le partenaire contributeur peut etre rattache a un groupe de participants.
4. Le partenaire contributeur peut contribuer au financement des coffrets.
5. Le partenaire contributeur consulte ses statistiques si l'extension le permet.

### 4. Participation

1. Le participant scanne un QR d'inscription diffuse pour une animation.
2. Il arrive sur une page d'inscription deja contextualisee avec l'animation.
3. Il saisit son email et accepte les consentements requis.
4. Le systeme cree l'inscription et rattache le participant a l'animation.
5. Le systeme envoie un email contenant le QR participant personnel.
6. Le participant peut ouvrir l'application mobile pour consulter les animations en cours de sa commune.
7. Il consulte les animations auxquelles il est inscrit, son historique de participation, le detail de chaque animation et son QR participant.
8. Il est rattache a un groupe uniquement si cette extension est activee.

### 5. Validation

1. Le participant realise une etape chez un commercant et presente son QR participant.
2. Le systeme verifie l'eligibilite de l'animation, du participant et du commercant.
3. Le systeme applique les controles anti-fraude MVP.
4. Le systeme cree la validation.
5. Le systeme met a jour la progression.
6. Le systeme qualifie automatiquement le participant si les regles sont atteintes.

### 6. Cloture

1. L'animation est cloturee automatiquement a la date prevue ou manuellement par un gestionnaire ou operateur Localeo habilite.
2. Les nouvelles participations sont bloquees.
3. Les participants qualifies sont figes.
4. La population eligible est figee.
5. L'action de lancement du tirage devient disponible pour le gestionnaire habilite.

### 7. Tirages au sort

1. Le gestionnaire d'animation lance un tirage depuis l'animation terminee ou cloturee.
2. Le systeme verifie que l'animation est terminee ou cloturee, que la population eligible est figee et que les lots sont configures.
3. Le systeme cree le tirage avec ses parametres et la population eligible source.
4. Le systeme attribue les lots.
5. Les gagnants sont designes.
6. Les gains sont prepares pour envoi.
7. Pour chaque gain, le systeme cree et active automatiquement la `CoffretInstance` du coffret gagne au moment de l'envoi.
8. Les resultats, gains envoyes et references de `CoffretInstance` sont historises.
9. Les gagnants sont notifies.

### 7 bis. Suivi des coffrets envoyes aux vainqueurs

1. Le gestionnaire ouvre le suivi des coffrets gagnes depuis l'animation.
2. Le systeme liste les coffrets envoyes aux vainqueurs avec leur `CoffretInstance`.
3. Le systeme affiche pour chaque coffret le statut, la date d'activation, la date d'expiration, les prestations consommees, les prestations restantes et les dernieres validations.
4. Le systeme signale les coffrets non consommes, proches expiration, expires ou en anomalie.
5. Le gestionnaire consulte uniquement les coffrets issus des animations de ses tenants communes habilites.

### 8. Bilan

1. Le systeme calcule le bilan.
2. Le bilan expose les participants total, participants ayant termine l'animation, validations, qualifications, lots et taux de completion.
3. Le bilan presente les statistiques par commercant et commune tenant ; les statistiques partenaire contributeur sont ajoutees si l'extension partenaire est activee.
4. Le bilan est exportable.

## Passeport commercant MVP

Le `Passeport commercant` est le premier modele d'animation implemente.

Regles MVP cible :
- une animation est associee a un tenant commune ;
- plusieurs commercants peuvent participer ;
- chaque commercant peut representer une etape ou un point de validation ;
- un participant progresse en validant des etapes chez les commercants ;
- un seuil de validations peut qualifier le participant ;
- les participants qualifies deviennent eligibles aux tirages ;
- les lots peuvent etre associes a l'animation ou a un tirage ;
- les lots sont obligatoirement des coffrets actifs de la commune, envoyes sous forme de `CoffretInstance` automatiquement activee ;
- l'association a un partenaire contributeur est post-MVP par defaut.

Le Passeport commercant ne doit pas devenir une implementation rigide : ses regles doivent etre exprimees comme configuration d'un modele.

## APIs et surfaces cible

### Plateforme partenaire dediee MVP

- Catalogue des modeles.
- Selection du tenant commune actif quand le gestionnaire est habilite sur plusieurs communes.
- Consultation du statut d'abonnement, de la formule, des dates et des limitations d'acces.
- Affichage des limitations d'acces si l'abonnement n'est pas actif.
- Creation et configuration d'une animation.
- Suivi live d'une animation : statut, inscriptions, validations, progression, qualifies, alertes, incidents et actions disponibles.
- Gestion des commercants participants.
- Gestion des lots.
- Publication, pilotage, cloture.
- Lancement du tirage au sort apres fin ou cloture.
- Envoi des gains et activation automatique des coffrets gagnes.
- Suivi de consommation des coffrets envoyes aux vainqueurs.
- Suivi des participations et validations.
- Bilan et export CSV.

### Back-office Localeo

- Vision live des animations de la plateforme.
- Filtrage et supervision par tenant commune.
- Consultation et modification des abonnements plateforme : formule, statut, dates, perimetre, motif de suspension ou exception d'acces.
- Supervision des animations partenaires.
- Administration et correction exceptionnelles des animations.
- Supervision des tirages au sort.
- Audit, support et exports.
- Extensions post-MVP : gestion des partenaires et des groupes.

### Application mobile participant MVP

- Liste des animations en cours de la commune.
- Liste des animations auxquelles le participant est inscrit.
- Historique des animations auxquelles le participant a participe.
- Detail d'une animation : description, dates, commune, etapes, commercants participants, progression.
- QR participant personnel pour chaque animation active.
- Reception des notifications push liees aux animations, notamment notification de gain si le participant est gagnant et opt-in push.

### APIs publiques

Paths cibles indicatifs, coherents avec l'Epic 40 :
- `/public/animation-locale/modeles`
- `/public/animation-locale/communes/{commune_id}/animations`
- `/public/animation-locale/animations/{animation_id}`
- `/public/animation-locale/animations/{animation_id}/inscription`
- `/public/animation-locale/animations/{animation_id}/inscriptions`
- `/public/animation-locale/participants/{participant_token}/animations`
- `/public/animation-locale/participants/{participant_token}/historique`
- `/public/animation-locale/participants/{participant_token}/animations/{animation_id}`
- `/public/animation-locale/participants/{participant_token}/animations/{animation_id}/qr`
- `/public/animation-locale/participants/{participant_token}/progression`

Tag OpenAPI principal :
- `Animation locale`

### APIs protegees / internes

Paths cibles indicatifs :
- `/protected/animation-locale/tenant-communes`
- `/protected/animation-locale/droit-acces`
- `/protected/animation-locale/communes/{commune_id}/animations`
- `/protected/animation-locale/animations`
- `/protected/animation-locale/animations/{animation_id}`
- `/protected/animation-locale/animations/{animation_id}/workflow`
- `/protected/animation-locale/animations/{animation_id}/live`
- `/protected/animation-locale/animations/{animation_id}/live/evenements`
- `/protected/animation-locale/dashboard-performance`
- `/protected/animation-locale/animations/{animation_id}/publier`
- `/protected/animation-locale/animations/{animation_id}/cloturer`
- `/protected/animation-locale/animations/{animation_id}/tirages`
- `/protected/animation-locale/animations/{animation_id}/gains/{gain_id}/envoyer`
- `/protected/animation-locale/animations/{animation_id}/gains/coffrets/consommation`
- `/protected/animation-locale/animations/{animation_id}/gains/{gain_id}/coffret-consommation`
- `/protected/animation-locale/animations/{animation_id}/flyer`
- `/protected/animation-locale/animations/{animation_id}/flyer/regenerer`
- `/protected/animation-locale/animations/{animation_id}/bilan`
- `/protected/animation-locale/participants/{participant_id}/progression`
- `/internal/animation-locale/live`
- `/internal/animation-locale/communes/{commune_id}/live`
- `/internal/animation-locale/dashboard-performance`
- `/internal/animation-locale/animations/{animation_id}/workflow`
- `/internal/animation-locale/communes/{commune_id}/droit-acces`
- `/internal/animation-locale/live/evenements`
- `/internal/animation-locale/live/alertes`
- `/internal/animation-locale/animations`
- `/internal/animation-locale/animations/{animation_id}/cloturer`
- `/internal/animation-locale/animations/{animation_id}/tirages`
- `/internal/animation-locale/animations/{animation_id}/gains`
- `/internal/animation-locale/animations/{animation_id}/gains/coffrets/consommation`
- `/admin/api/animation-locale/animations`

## Relations avec le core Localeo

Le domaine animation consomme le core sans dupliquer :

- `referencement` : communes/villes, commercants, types commercants ; le tenant commune reference la commune sans la dupliquer.
- `commercialisation` : coffrets ou offres si une animation veut les mettre en avant ou les utiliser comme lots.
- `gestion_achats` : creation, activation, consultation, consommation et cycle de vie des `CoffretInstances` issues d'un gain d'animation.
- `abonnements_plateforme` : domaine transverse dedie aux offres, souscriptions, statuts, facturation Stripe Billing et droits d'acces payants au portail partenaire.
- `identite_acces` : authentification, sessions, roles gestionnaire d'animation, droits scopes par tenant commune, tokens, API keys si necessaire.
- `exploitation` : notifications, email, SMS, WebPush, audit, batchs.
- `support` : eventuelles demandes liees aux participants.
- `documentaire` : metadonnees et acces aux flyers PDF generes, exports ou documents de bilan si necessaire.
- `dam` ou assets applicatifs : logo Localeo et elements de charte utilises dans les supports generes.

## User Stories

Priorisation de cadrage :

- Coeur MVP : `PRD-334`, `PRD-335`, `PRD-336`, `PRD-337`, `PRD-338`, `PRD-341`, `PRD-342`, `PRD-343`, `PRD-344`, `PRD-345`, `PRD-346`, `PRD-347`, `PRD-348`, `PRD-349`, `PRD-350`, `PRD-351`, `PRD-352`, `PRD-353`, `PRD-354`, `PRD-355`, `PRD-356`, `PRD-357`, `PRD-358`, `PRD-359`, `PRD-360`, `PRD-361`, `PRD-362`, `PRD-363`, `PRD-364`, `PRD-365`, `PRD-415`.
- Extension a challenger avant inclusion MVP : `PRD-339` partenaires contributeurs, `PRD-340` groupes de participants.
- Transverse technique : `PRD-352` et `PRD-353` doivent etre livres des le socle pour respecter l'Epic 40.
- Transverse conformite : `PRD-362` doit etre integre des le MVP pour eviter de stocker durablement des donnees participant nominatives sans regle d'anonymisation.

1. `PRD-334` En tant que gestionnaire d'animation, je veux consulter le catalogue des modeles d'animations afin de choisir le bon format pour une animation locale.
   - Statut : `A faire`
   - Priorite : `MVP coeur`
   - Resultat attendu : le catalogue expose au moins le modele `Passeport commercant`.
   - Resultat attendu : chaque modele decrit son fonctionnement, ses prerequis et ses parametres configurables.

2. `PRD-335` En tant que gestionnaire d'animation, je veux creer une animation a partir d'un modele afin de lancer une animation territoriale sans developpement specifique.
   - Statut : `A faire`
   - Priorite : `MVP coeur`
   - Resultat attendu : une animation est creee en statut `BROUILLON`.
   - Resultat attendu : elle reference son modele, son gestionnaire, son organisateur, son tenant commune et ses dates.
   - Resultat attendu : un gestionnaire d'animation ne peut gerer que les animations rattachees a ses tenants communes.
   - Resultat attendu : Localeo n'est pas le canal nominal de creation des animations.

3. `PRD-336` En tant que gestionnaire d'animation, je veux configurer les regles du Passeport commercant afin de definir comment les participants progressent et se qualifient.
   - Statut : `A faire`
   - Priorite : `MVP coeur`
   - Resultat attendu : les regles de validation, seuil de qualification et contraintes de dates sont configurables.
   - Resultat attendu : la configuration est verifiee avant publication.

4. `PRD-337` En tant que gestionnaire d'animation, je veux selectionner les commercants participants afin de definir les lieux ou etapes de l'animation.
   - Statut : `A faire`
   - Priorite : `MVP coeur`
   - Resultat attendu : les commercants sont selectionnes depuis le referentiel core.
   - Resultat attendu : l'animation ne duplique pas les donnees commercant.

5. `PRD-338` En tant que gestionnaire d'animation, je veux publier une animation configuree afin de la rendre accessible aux participants.
   - Statut : `A faire`
   - Priorite : `MVP coeur`
   - Resultat attendu : une animation non valide ne peut pas etre publiee.
   - Resultat attendu : la publication fige les regles critiques de l'animation.

6. `PRD-339` En tant que gestionnaire d'animation, je veux gerer les partenaires contributeurs d'une animation afin de suivre leurs contributions et statistiques.
   - Statut : `A faire`
   - Priorite : `Extension a challenger`
   - Resultat attendu : un partenaire contributeur peut etre invite, accepter l'invitation et etre rattache a l'animation.

7. `PRD-340` En tant que gestionnaire d'animation, je veux gerer des groupes de participants afin d'organiser les participants par classe, equipe, partenaire ou segment.
   - Statut : `A faire`
   - Priorite : `Extension a challenger`
   - Resultat attendu : un participant peut etre rattache a un ou plusieurs groupes selon les regles de l'animation.

8. `PRD-341` En tant que participant, je veux m'inscrire a une animation afin de participer au Passeport commercant.
   - Statut : `A faire`
   - Priorite : `MVP coeur`
   - Resultat attendu : l'inscription cree un participant rattache a l'animation.
   - Resultat attendu : les consentements et informations minimales sont collectes.

9. `PRD-342` En tant que participant, je veux consulter ma progression afin de savoir quelles etapes il me reste a valider.
   - Statut : `A faire`
   - Priorite : `MVP coeur`
   - Resultat attendu : la progression affiche les etapes validees, restantes et le statut de qualification.

10. `PRD-343` En tant que commercant participant, je veux valider une etape d'un participant afin de certifier sa visite ou action dans mon commerce.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : la validation est rattachee a l'animation, au participant, au commercant et a l'etape.
    - Resultat attendu : la validation terrain se fait par scan du QR participant depuis l'application mobile commercant.
    - Resultat attendu : l'application mobile commercant evolue pour reconnaitre les QR d'animation locale et les router vers les controles `animation_locale`.
    - Resultat attendu : une validation invalide ou en double est refusee.

11. `PRD-344` En tant que systeme, je veux appliquer des controles anti-fraude MVP afin de limiter les validations abusives.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : les validations trop frequentes, hors dates ou hors commercants eligibles sont refusees ou signalees.

12. `PRD-345` En tant que systeme, je veux qualifier automatiquement les participants afin de constituer la population eligible aux tirages.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : les regles de qualification sont appliquees apres chaque validation et a la cloture.

13. `PRD-346` En tant que gestionnaire d'animation, je veux configurer les coffrets a gagner afin de preparer les recompenses de l'animation.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : chaque lot a gagner reference obligatoirement un coffret Localeo actif de la commune de l'animation.
    - Resultat attendu : les lots libres, lots externes et lots hors commune sont exclus du MVP.
    - Resultat attendu : les lots portent coffret reference, libelle d'affichage, quantite et statut.
    - Resultat attendu : les coffrets offerts en gain sont achetes par le partenaire apres acceptation des commercants, avant publication, et imputes au budget de l'animation.
    - Resultat attendu : le partenaire contributeur est gere seulement si l'extension partenaire est activee.

14. `PRD-347` En tant que systeme, je veux cloturer automatiquement une animation afin de bloquer les nouvelles participations et figer les eligibles.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : la cloture bloque inscriptions et validations nouvelles.
    - Resultat attendu : les participants qualifies sont calcules et figes.

15. `PRD-348` En tant que gestionnaire d'animation, je veux realiser un tirage au sort afin d'attribuer les lots aux participants qualifies.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : le tirage peut etre lance depuis la plateforme partenaire lorsque l'animation est terminee ou cloturee.
    - Resultat attendu : le tirage est bloque tant que la population eligible n'est pas figee.
    - Resultat attendu : le tirage utilise une population eligible tracee.
    - Resultat attendu : les gagnants, lots attribues et parametres du tirage sont historises.

16. `PRD-349` En tant que gagnant, je veux etre notifie de mon gain afin de connaitre le lot et les modalites de remise.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : les gagnants sont notifies par email et notification push lorsque les canaux sont disponibles et les preferences applicables.
    - Resultat attendu : le push gagnant s'appuie sur l'application Localeo participant avec opt-in et abonnement push actif.
    - Resultat attendu : si le participant dispose d'un abonnement push actif, une notification push est creee avec un contenu sobre et un lien vers le detail de l'animation ou du gain.
    - Resultat attendu : si le canal push n'est pas disponible, l'email collecte a l'inscription sert de canal de repli.
    - Resultat attendu : le systeme evite les doublons de notification pour un meme gain et un meme canal.
    - Resultat attendu : l'envoi est trace et rejouable en cas d'echec.

17. `PRD-350` En tant que gestionnaire d'animation, je veux consulter le bilan d'une animation afin de mesurer son impact territorial.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : le bilan expose participants total, participants ayant termine l'animation, validations, qualifies, lots distribues, taux de completion et statistiques par commercant et commune tenant.
    - Resultat attendu : les statistiques partenaire contributeur sont gerees seulement si l'extension partenaire est activee.

18. `PRD-351` En tant que gestionnaire d'animation, je veux exporter le bilan afin de partager les resultats avec les partenaires et financeurs.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : un export est disponible et audite.

19. `PRD-352` En tant que responsable technique, je veux que le domaine animation locale soit separe de la marketplace afin d'ajouter de nouveaux modeles sans casser le core commercialisation.
    - Statut : `A faire`
    - Priorite : `Transverse technique`
    - Resultat attendu : les objets `animation_locale` ne dupliquent pas communes, commercants, coffrets ou utilisateurs.
    - Resultat attendu : les dependances au core passent par des ports/services explicites.
    - Resultat attendu : le moteur separe le socle generique, la definition de modele et les strategies metier propres a chaque modele.
    - Resultat attendu : les use cases generiques de creation, publication, inscription, workflow, tirage, gains, bilan et dashboard ne contiennent pas de logique metier codee en dur pour le `PASSEPORT_COMMERCANT`.
    - Resultat attendu : une registry permet de retrouver la definition et la strategie d'un modele depuis son code.
    - Resultat attendu : l'ajout d'un nouveau modele doit passer par une nouvelle definition et une nouvelle strategie, sans modifier les invariants communs du moteur.

20. `PRD-353` En tant qu'integrateur API, je veux que les APIs Animation locale respectent les conventions de l'Epic 40 afin de garder des paths et tags OpenAPI coherents.
    - Statut : `A faire`
    - Priorite : `Transverse technique`
    - Resultat attendu : les paths canoniques portent `/animation-locale`.
    - Resultat attendu : le tag OpenAPI principal est `Animation locale`.

21. `PRD-354` En tant que participant, je veux m'inscrire simplement a une animation depuis un QR contextualise afin de participer sans creer de compte.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : le QR d'inscription ouvre une page deja contextualisee avec l'animation.
    - Resultat attendu : le participant saisit email, nom, prenom, telephone et valide les consentements requis.
    - Resultat attendu : l'inscription cree un participant rattache a l'animation.
    - Resultat attendu : le participant recoit par email une confirmation reprenant les informations de l'animation et son QR participant personnel directement dans le message.
    - Resultat attendu : le QR participant est distinct du QR coffret.

22. `PRD-355` En tant que participant, je veux une application mobile pour suivre mes animations locales afin de retrouver facilement mes participations et mon QR.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : l'application affiche les animations en cours de la commune.
    - Resultat attendu : l'application affiche les animations auxquelles je suis inscrit.
    - Resultat attendu : l'application affiche l'historique des animations auxquelles j'ai participe.
    - Resultat attendu : pour chaque animation, je peux consulter le detail, la progression et mon QR participant.

23. `PRD-356` En tant qu'operateur Localeo, je veux une vision live des animations de la plateforme afin de superviser l'activite sans etre en charge de creer ou animer les animations.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : la vision live affiche les animations publiees, en cours, cloturees ou en anomalie.
    - Resultat attendu : la vision live affiche les inscriptions, validations, qualifications et tirages recents.
    - Resultat attendu : la vision live signale les alertes operationnelles : absence de validations, QR en erreur, email non envoye, cloture en retard, tirage bloque.
    - Resultat attendu : les actions Localeo restent limitees a la supervision, au support et a l'administration exceptionnelle.

24. `PRD-357` En tant que gestionnaire d'animation, je veux travailler dans le tenant de ma commune afin de ne voir et gerer que les animations de mon perimetre.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : un tenant commune reference une commune du referentiel.
    - Resultat attendu : une animation MVP appartient a un seul tenant commune.
    - Resultat attendu : un gestionnaire peut etre habilite sur plusieurs tenants communes.
    - Resultat attendu : le portail impose une selection explicite du tenant commune actif avant creation ou gestion.
    - Resultat attendu : les droits de creation, modification, publication, cloture, tirage et export sont controles par tenant commune.
    - Resultat attendu : le role `GESTIONNAIRE_ANIMATION` autorise le cycle nominal : creer, configurer, modifier une animation non publiee, publier, suivre le live, cloturer, lancer le tirage, envoyer les gains, consulter le bilan et exporter.
    - Resultat attendu : apres publication, les modifications critiques sont bloquees ou passent par une depublication/action explicite selon le statut.
    - Resultat attendu : le gestionnaire ne peut pas modifier les abonnements, acceder a la supervision globale, corriger exceptionnellement une animation hors perimetre ou administrer tous les tenants.
    - Resultat attendu : les listes publiques et l'application mobile participant filtrent les animations par commune.
    - Resultat attendu : Localeo peut agreger la vision live et filtrer par commune.

25. `PRD-358` En tant qu'organisateur ou partenaire, je veux acceder a la plateforme d'animation via un abonnement actif afin que l'usage de la plateforme soit payant et controle.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : un abonnement plateforme Stripe Billing est rattache a une formule, un partenaire donne et une commune donnee.
    - Resultat attendu : le gestionnaire peut consulter son abonnement : formule, statut, dates, perimetre couvert et limitations d'acces.
    - Resultat attendu : le statut d'abonnement actif conditionne l'acces aux fonctions payantes du portail partenaire.
    - Resultat attendu : si l'abonnement expire alors qu'une animation est publiee ou en cours, l'animation va a son terme avant cloture des acces.
    - Resultat attendu : sans abonnement actif, les nouvelles actions payantes hors finalisation d'animation en cours sont bloquees ou degradees selon une regle produit explicite.
    - Evolution : la tarification, le prix négocié, la gratuité, le paiement
      Stripe, l'activation conditionnelle et l'intégration au suivi du CA sont
      détaillés dans l'`Epic 47 — Souscription et paiement de l'abonnement
      partenaire Animation`.
    - Resultat attendu : les parcours publics participant et les QR d'animations deja publiees ne sont pas interrompus automatiquement avant la fin de l'animation.
    - Resultat attendu : Localeo peut consulter et modifier l'abonnement pour comprendre les blocages d'acces, corriger un statut, prolonger une periode, changer une formule ou intervenir en support.
    - Resultat attendu : chaque modification d'abonnement est auditee avec acteur, date, ancienne valeur, nouvelle valeur et motif.

26. `PRD-359` En tant qu'organisateur, je veux suivre en live l'etat d'une animation afin de piloter son deroulement sans attendre le bilan final.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : la vue live est accessible depuis la fiche animation de la plateforme partenaire.
    - Resultat attendu : la vue live affiche le statut de l'animation, la periode, le nombre total de participants, le nombre de participants ayant termine l'animation, les inscriptions, les validations recentes, la progression globale et les participants qualifies.
    - Resultat attendu : la vue live affiche les alertes utiles a l'organisateur : absence de validations, QR en erreur, email non envoye, cloture proche ou cloture en retard.
    - Resultat attendu : la vue live expose les actions disponibles selon le statut et les droits : modifier le brouillon, publier, relancer, cloturer, lancer le tirage ou exporter.
    - Resultat attendu : l'organisateur ne voit que les animations de ses tenants communes habilites.
    - Resultat attendu : les donnees live sont rafraichies selon un mecanisme simple MVP, par exemple polling incremental.

27. `PRD-360` En tant que vainqueur, je veux recevoir un coffret deja active lorsque mon gain est envoye afin de pouvoir l'utiliser sans action manuelle supplementaire.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : les coffrets utilisables comme gains ont ete achetes par le partenaire apres acceptation des commercants, avant publication, et appartiennent au budget de l'animation.
    - Resultat attendu : seuls les coffrets actifs de la commune de l'animation peuvent etre configures et envoyes en gain.
    - Resultat attendu : lorsqu'un gain est envoye, le systeme cree une `CoffretInstance` rattachee au gagnant.
    - Resultat attendu : la `CoffretInstance` est automatiquement activee au moment de l'envoi du gain.
    - Resultat attendu : la `CoffretInstance` porte une origine `GAIN_ANIMATION` et reference l'animation, le tirage, le gain et le participant gagnant.
    - Resultat attendu : l'envoi du gain est idempotent et ne peut pas creer plusieurs `CoffretInstances` pour le meme gain.
    - Resultat attendu : l'activation est auditee et visible dans la supervision Localeo et le support.
    - Resultat attendu : la notification gagnant contient les informations utiles pour acceder au coffret active.

28. `PRD-361` En tant qu'organisateur, je veux suivre la consommation des coffrets envoyes aux vainqueurs afin de mesurer l'usage reel des lots distribues.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : la plateforme partenaire liste les coffrets envoyes aux vainqueurs.
    - Resultat attendu : chaque ligne affiche la `CoffretInstance`, le vainqueur, le statut du coffret, la date d'activation, la date d'expiration et le niveau de consommation.
    - Resultat attendu : le detail expose l'identite du gagnant, les commercants, les dates de validation, les prestations restantes et les donnees personnelles masquees selon les droits autorises.
    - Resultat attendu : des alertes signalent les coffrets non consommes, proches expiration, expires ou incoherents.
    - Resultat attendu : les donnees de consommation sont lues depuis `gestion_achats` sans dupliquer les statuts ni les validations.
    - Resultat attendu : l'organisateur ne voit que les coffrets issus des animations de ses tenants communes habilites.

29. `PRD-362` En tant que responsable produit et conformite, je veux appliquer une politique de conservation et d'anonymisation des donnees d'animation afin de limiter l'exposition des donnees personnelles apres l'animation.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : les donnees nominatives participant, email, nom, prenom et telephone, sont conservees jusqu'a fin d'animation + 12 mois puis anonymisees.
    - Resultat attendu : les QR participants, tokens et liens de consultation sont revoques ou supprimes au plus tard fin d'animation + 3 mois.
    - Resultat attendu : les validations detaillees sont conservees 24 mois, puis les references participant nominatives sont anonymisees.
    - Resultat attendu : les tirages et gains sont conserves 5 ans avec donnees participant pseudonymisees lorsque la donnee nominative n'est plus necessaire.
    - Resultat attendu : les exports CSV generes sont supprimes automatiquement apres 90 jours maximum.
    - Resultat attendu : les traces de notification email/push sont conservees 12 mois, puis purgees ou anonymisees techniquement.
    - Resultat attendu : les logs d'audit et de securite lies a l'animation sont conserves 24 mois.
    - Resultat attendu : l'anonymisation supprime email, telephone, nom et prenom, remplace le participant par un identifiant non reversible et conserve uniquement les indicateurs utiles : commune, animation, date approximative, statut termine/non termine, nombre de validations et gain oui/non.
    - Resultat attendu : les donnees de consommation de coffret suivent le cycle de vie `gestion_achats`; `animation_locale` applique uniquement le masquage et l'anonymisation de ses references participant.

30. `PRD-363` En tant que gestionnaire d'animation, je veux generer un flyer PDF contenant le QR et les informations de l'animation afin de disposer d'un support de communication pret a partager.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : le flyer PDF est genere lors de la publication a partir de la configuration et des commercants participants figes, puis peut etre regenere tant que l'animation reste publiee.
    - Resultat attendu : le flyer reprend la charte et le logo Localeo dans un gabarit standard.
    - Resultat attendu : le flyer contient au minimum le nom de l'animation, la commune, les dates, l'organisateur ou partenaire, un court texte de presentation, le QR d'inscription et l'URL d'inscription.
    - Resultat attendu : le QR du flyer est le QR d'inscription public de l'animation et ne contient aucun droit gestionnaire.
    - Resultat attendu : le gestionnaire peut previsualiser, telecharger et regenerer le PDF depuis la plateforme partenaire.
    - Resultat attendu : si les informations publiques ou le QR d'inscription changent avant publication, le PDF existant est marque a regenerer ou remplace lors de la regeneration.
    - Resultat attendu : le PDF partage avant ouverture de l'animation dirige vers une page publique contextualisee qui respecte le statut et la fenetre d'inscription.
    - Resultat attendu : la generation, le telechargement et le remplacement du flyer sont audites.
    - Resultat attendu : le binaire PDF et ses metadonnees sont geres via le domaine `documentaire` ou le service documentaire retenu, sans stockage direct en base `animation_locale`.

31. `PRD-364` En tant que gestionnaire d'animation, je veux visualiser rapidement l'etat d'une animation dans son workflow global afin de savoir ou elle en est et quoi faire ensuite.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : la liste des animations affiche un indicateur de workflow lisible pour chaque animation.
    - Resultat attendu : la fiche animation affiche un workflow global comprenant au minimum : brouillon, configuration, prete a publier, publiee, en cours, cloturee, tirage a lancer, gains a envoyer, bilan disponible, archivee ou annulee.
    - Resultat attendu : l'etape courante, les etapes terminees, les etapes restantes et l'etape suivante attendue sont visibles rapidement.
    - Resultat attendu : les blocages sont visibles avec une raison actionnable : configuration incomplete, abonnement inactif, periode non ouverte, QR non disponible, participants non eligibles, tirage bloque, gains non envoyes ou bilan indisponible.
    - Resultat attendu : les actions affichees dependent du statut, des droits `GESTIONNAIRE_ANIMATION`, du tenant commune actif et de l'abonnement.
    - Resultat attendu : la vue workflow est derivee des statuts, transitions et invariants du domaine ; elle ne cree pas une seconde source de verite.
    - Resultat attendu : Localeo peut voir la meme information en supervision, agregee et filtrable par commune.

32. `PRD-365` En tant que gestionnaire d'animation, je veux consulter un dashboard de performance afin de mesurer l'efficacite de mes animations et comparer leurs resultats.
    - Statut : `A faire`
    - Priorite : `MVP coeur`
    - Resultat attendu : le dashboard est accessible depuis la plateforme partenaire dediee.
    - Resultat attendu : le dashboard ne montre que les animations des tenants communes habilites du gestionnaire.
    - Resultat attendu : le dashboard est filtrable par periode, tenant commune, modele d'animation, statut et animation.
    - Resultat attendu : le dashboard affiche les indicateurs globaux : nombre d'animations creees, publiees, en cours, terminees, cloturees et archivees.
    - Resultat attendu : le dashboard affiche les indicateurs de participation : inscrits, participants ayant termine, taux de completion, progression moyenne, participants qualifies et taux de qualification.
    - Resultat attendu : le dashboard affiche les indicateurs terrain : validations totales, validations par animation, validations par commercant participant et validations recentes.
    - Resultat attendu : le dashboard affiche les indicateurs de gains : tirages realises, gagnants, coffrets envoyes, coffrets actifs, coffrets consommes, partiellement consommes, expires et taux de consommation.
    - Resultat attendu : le dashboard affiche le montant potentiel restant a reinjecter, les coffrets entierement non consommes expirant dans un horizon configurable, le delai moyen entre l'envoi d'un gain et sa premiere consommation, ainsi que la taille de l'echantillon utilise.
    - Resultat attendu : le dashboard affiche le nombre de commercants participants effectifs sans aucune validation et la repartition du montant reinjecte par commercant.
    - Resultat attendu : le dashboard permet de comparer plusieurs animations sur les principaux indicateurs MVP.
    - Resultat attendu : les donnees personnelles participant sont exclues des vues agregees ; tout acces au detail nominatif reste limite aux ecrans autorises.
    - Resultat attendu : Localeo peut consulter une vue de performance agregee et filtrable en supervision, sans devenir le gestionnaire des animations.

33. `PRD-415` En tant que gestionnaire d'animation, je veux gerer les actualites d'une animation afin d'informer les habitants et participants de son deroulement.
    - Statut : `Backend/backoffice implemente le 2026-08-23 - interfaces Localeo Animation et Localeo Live a raccorder`
    - Priorite : `P0`
    - Resultat attendu : la fiche Localeo Animation propose un onglet `Actualites` avec liste, creation, modification, programmation, publication, masquage et suppression des brouillons.
    - Resultat attendu : chaque actualite est rattachee de facon non ambigue a une animation et herite de sa commune ; ce rattachement ne peut pas etre modifie apres creation.
    - Resultat attendu valide (`ARB-64`) : une actualite publiee apparait dans Localeo Live sous `En direct`, filtre `Animations`, avec le nom de l'animation et un lien vers sa fiche.
    - Resultat attendu (`ARB-65`, `ARB-66`) : les installations eligibles recoivent une inbox idempotente lorsque `ANIMATION` est activee ; le WebPush est tente en complement lorsqu'un abonnement actif existe.
    - Resultat attendu (`ARB-67`) : le lien est produit depuis `LOCALEO_FRONT_LIVE_ANIMATION_URL_TEMPLATE` avec l'identifiant de l'animation.
    - Resultat attendu (`ARB-69`) : une actualite ne peut etre rendue publique que pour une animation `PUBLIEE`, `EN_COURS` ou `CLOTUREE` non archivee ; une publication deja diffusee est masquee et non supprimee physiquement.
    - Resultat attendu : tenant, audit, OpenAPI et non-duplication du moteur `activites_locales` sont couverts ; la permission `animation:gerer_actualites` et sa reprise suivent `ARB-68`.
    - Specification detaillee : [Actualites rattachees aux animations](../../specifications/epic-41-api/actualites.md).

## Regles de gestion

- Une animation est toujours creee depuis un modele.
- Une animation MVP est rattachee a un seul tenant commune.
- Le modele d'une animation ne peut pas etre change apres creation.
- Les use cases generiques ne doivent pas contenir de conditions metier dispersees sur le code `PASSEPORT_COMMERCANT`.
- Tout comportement specifique a un modele doit passer par une `StrategieModeleAnimation` referencee dans le `RegistreModelesAnimation`.
- Une definition de modele doit declarer ses prerequis, capacites, regles configurables, contraintes de publication et types de lots autorises.
- L'ajout d'un nouveau modele ne doit pas modifier les invariants communs du moteur, sauf besoin generique explicitement arbitre.
- La vue workflow d'une animation est derivee du statut, des transitions autorisees, des droits, de l'abonnement et des invariants metier.
- La vue workflow ne doit pas porter un etat persiste concurrent au statut de l'animation.
- Toute etape bloquee dans le workflow doit exposer une raison actionnable et, si possible, l'action corrective disponible.
- Le dashboard de performance est filtre par les tenants communes habilites du gestionnaire.
- Les indicateurs du dashboard de performance sont calcules a partir des donnees d'animation, de validation, de tirage et de consommation `gestion_achats`, sans dupliquer les statuts source.
- Les indicateurs economiques des gains utilisent le montant de reversement snapshotte sur les prestations, en centimes et en EUR ; ils mesurent une valeur consommee ou encore mobilisable et non l'execution bancaire du reversement.
- Les commercants sans validation sont comptes parmi les seuls participants effectifs ayant accepte leur invitation selon l'Epic 56 ; les invitations en attente, refusees, expirees ou annulees sont exclues.
- Les vues agregees du dashboard de performance ne doivent pas exposer de donnees personnelles participant.
- Un gestionnaire d'animation ne peut agir que sur les animations de ses tenants communes habilites.
- Le role MVP `GESTIONNAIRE_ANIMATION` est scope par tenant commune et couvre creation, configuration, modification avant publication, publication, suivi live, cloture, tirage, envoi de gains, bilan et export.
- Le gestionnaire d'animation ne peut pas modifier les abonnements, acceder a la supervision globale Localeo, corriger exceptionnellement une animation hors perimetre ou administrer tous les tenants.
- Un operateur Localeo habilite peut superviser tous les tenants communes et filtrer ses vues par commune.
- L'acces aux fonctions payantes du portail partenaire exige un abonnement plateforme actif en plus des droits `identite_acces`.
- Un abonnement suspendu, expire ou resilie bloque les nouvelles actions self-service payantes, mais une animation publiee ou en cours peut aller a son terme avant cloture des acces.
- Une animation publiee ne peut pas modifier ses regles critiques sans action explicite de depublication ou nouvelle version.
- Une animation ne peut accepter des participations que dans sa fenetre d'ouverture.
- Une inscription par email a une meme animation reste unique. La premiere soumission renvoie `201 CONFIRMEE`, un `participant_url` non nul et envoie le QR. Toute nouvelle soumission avec le meme email normalise est refusee en `409 Conflict`, sans creer de token ni renvoyer le QR.
- La suppression manuelle d'un participant exige la permission dediee `animation:supprimer_participant`. Elle supprime aussi ses tokens et validations, mais elle est refusee des que le participant appartient a une population de tirage figee ou possede un gain.
- Le QR participant peut etre renvoye par email sans creer une nouvelle inscription.
- Un QR participant revoque ou remplace ne doit plus permettre de validation.
- Le flyer PDF utilise le QR d'inscription public de l'animation, jamais le QR participant ni un token gestionnaire.
- Le flyer PDF peut etre genere en brouillon ou configuration, mais le QR doit respecter le statut public de l'animation et ne pas ouvrir les inscriptions avant publication ou hors fenetre autorisee.
- Toute modification d'information publique utilisee dans le flyer doit marquer le PDF a regenerer ou remplacer le PDF existant lors de la regeneration.
- La generation, le telechargement et le remplacement du flyer PDF sont audites.
- Une validation n'est acceptee que si l'animation est active, le participant inscrit et le commercant eligible dans le tenant commune de l'animation.
- La validation terrain est effectuee par scan du QR participant depuis l'application mobile commercant.
- Une meme etape ne peut pas etre validee deux fois par le meme participant sauf regle explicite du modele.
- La qualification d'un participant est calculee par les regles du modele et de l'animation.
- Les tirages ne peuvent etre lances qu'apres fin ou cloture de l'animation.
- Les tirages ne peuvent utiliser que des populations eligibles figees.
- Un lot attribue ne peut pas etre attribue une seconde fois sauf annulation explicite.
- Tout lot a gagner reference obligatoirement un coffret Localeo actif de la commune de l'animation.
- Les lots libres, lots externes et lots hors commune sont exclus du MVP.
- Un gain envoye au vainqueur cree une seule `CoffretInstance` activee, de maniere idempotente.
- Une `CoffretInstance` issue d'un gain d'animation doit etre tracee avec l'origine `GAIN_ANIMATION`.
- Les coffrets utilises comme lots doivent etre actifs et rattaches a la commune de l'animation.
- La consommation d'une `CoffretInstance` issue d'un gain reste geree par `gestion_achats`; `animation_locale` expose uniquement une vue de suivi rattachee au gain.
- Un organisateur ne peut consulter la consommation que des coffrets issus de ses animations et tenants communes habilites.
- La cloture bloque les nouvelles inscriptions et validations.
- Les bilans doivent etre recalculables ou historises de maniere auditable.
- Les donnees nominatives participant sont conservees jusqu'a fin d'animation + 12 mois, puis anonymisees.
- Les QR participants, tokens et liens de consultation sont revoques ou supprimes au plus tard fin d'animation + 3 mois.
- Les validations detaillees sont conservees 24 mois, puis les references participant nominatives sont anonymisees.
- Les tirages et gains sont conserves 5 ans avec participant pseudonymise lorsque l'identite nominative n'est plus necessaire.
- Les exports CSV generes sont supprimes automatiquement apres 90 jours maximum.
- Les traces de notification email/push sont conservees 12 mois, puis purgees ou anonymisees.
- Les logs d'audit et de securite lies a l'animation sont conserves 24 mois.
- L'anonymisation supprime email, telephone, nom et prenom, remplace le participant par un identifiant non reversible et conserve seulement les indicateurs utiles.
- Le suivi de consommation des coffrets gagnes suit le cycle de vie `gestion_achats`; `animation_locale` applique le masquage et l'anonymisation de ses references participant.
- Une actualite d'animation reutilise `activites_locales` et porte obligatoirement l'identifiant de son animation ; la ville cible est heritee du tenant de l'animation.
- Une actualite peut etre preparee avant publication de l'animation, mais sa publication effective exige une animation `PUBLIEE`, `EN_COURS` ou `CLOTUREE` et non archivee.
- Une actualite publiee est masquee, jamais supprimee physiquement ; seuls les brouillons peuvent etre supprimes.
- La diffusion Live est idempotente et respecte la preference `ANIMATION` de chaque installation.

## Impacts sur les epics existantes

- Epic 16 : le feed d'activite locale marketplace reste distinct ; il porte les actualites d'animation sous `ACTUALITE_ANIMATION`, sans devenir le moteur d'animation.
- Epic 42 : Localeo Live affiche ces publications sous `En direct > Animations` et applique la preference de notification `ANIMATION`.
- Epic 23 : les batchs peuvent porter la cloture automatique, notifications et exports.
- Epic 26 : la communication libre peut servir le support autour d'une animation.
- Epic 27 et 37 : les visions 360 commercant/client peuvent afficher plus tard des blocs d'animation.
- Epic 34 : Localeo Control doit afficher la vision live des animations de la plateforme pour supervision interne, sans devenir la surface d'animation.
- Epic 35 : les roles back-office devront proteger creation, publication, tirage et export.
- Epic 38 : la gestion documentaire peut porter les metadonnees, l'acces et le stockage des flyers PDF generes.
- Epic 40 : `animation_locale` devient un domaine fonctionnel supplementaire avec packages, paths et tags OpenAPI dedies.

## Lots d'implementation - decoupage de reference

Ce decoupage remplace le regroupement historique conserve plus bas. Chaque lot doit produire un increment testable, documente dans OpenAPI lorsque des contrats sont exposes, et sans regression sur les domaines Localeo reutilises.

### Lot 0 - Socle technique et conventions

Etat : code implemente le 16 aout 2026. La validation `pytest` doit etre rejouee dans un environnement Python compatible avant integration, l'interpreteur local n'etant pas disponible lors de l'implementation.

- Creer les packages `animation_locale` et `abonnements_plateforme` et leurs frontieres.
- Ajouter erreurs metier, permissions, idempotence, audit et les templates d'URL Animation/Participant.
- Creer les modeles relationnels, migrations, repositories, unite de travail et factories de test.
- Poser `animation_operations` et les conventions de traitements asynchrones.
- Critere de sortie : migrations reversibles, repositories testes et suite globale sans regression.

### Lot 1 - Identite, partenaires et habilitations

Etat : code implemente le 16 aout 2026. Validation `pytest` a executer dans l'environnement Python du projet avant integration.

- Persister partenaires, gestionnaires et habilitations par commune.
- Implementer la session Animation distincte de huit heures, connexion, consultation et revocation.
- Implementer la selection de commune active, les permissions fines et l'isolation tenant avec reponses `403`/`404`.
- Critere de sortie : un gestionnaire se connecte et n'accede qu'aux communes et actions autorisees.

### Lot 2 - Abonnement et droits d'acces

Etat : code implemente le 16 aout 2026. Validation `pytest` a executer dans l'environnement Python du projet avant integration. Le raccordement du webhook Stripe Billing reste conditionne par la configuration des secrets de test prevue par `ARB-53`.

- Implementer Offre, Abonnement, DroitAccesPlateforme et le port `verifier_droit(...)`.
- Fournir l'activation administrative auditee et les regles d'expiration en cours d'animation.
- Preparer les evenements Stripe idempotents puis raccorder Stripe test lorsque les secrets sont disponibles.
- Critere de sortie : creation et publication sont autorisees ou refusees selon le droit d'acces.

### Lot 3 - Catalogue et creation d'animation

Etat : code implemente le 16 aout 2026. Le catalogue, la strategie `PASSEPORT_COMMERCANT`, les projections d'eligibilite et le CRUD de brouillon versionne sont exposes selon les contrats OpenAPI. Validation `pytest` a executer dans l'environnement Python du projet avant integration.

- Implementer le catalogue et la strategie `PASSEPORT_COMMERCANT`.
- Exposer commercants et coffrets eligibles.
- Creer et modifier une animation, ses etapes, regles, lots et configuration versionnee.
- Exposer liste et fiche en appliquant tenant, pagination et controles de coherence.
- Critere de sortie : une animation complete peut etre creee en brouillon avec les contrats OpenAPI.

### Lot 4 - Publication et communication

Etat : code implemente le 16 aout 2026. La validation et la publication sont controlees par tenant et abonnement, l'URL et le QR publics sont stables, et les flyers PDF/PNG versionnes sont stockes via `documentaire`. Validation `pytest` a executer dans l'environnement Python du projet avant integration.

- Valider la configuration et publier atomiquement l'animation et son QR d'inscription.
- Valoriser les URLs publiques depuis les templates complets sans construire de chemin frontend.
- Generer flyer PDF et apercu PNG avec ReportLab, gabarits versionnes et assets temporaires.
- Stocker via `documentaire`, securiser le telechargement et exposer le suivi des operations.
- Critere de sortie : une animation publiee possede une page publique, un QR stable et un flyer telechargeable.

### Lot 5 - Inscription et parcours participant

Etat : code implemente le 16 aout 2026. L'inscription sans compte, l'unicite email par animation, les tokens personnels hashes, le QR, la progression publique et le renvoi anti-abus sont raccordes a l'outbox email et a l'audit. Validation `pytest` a executer dans l'environnement Python du projet avant integration.

- Exposer la page publique contextualisee et l'inscription idempotente sans compte.
- Garantir l'unicite par animation et email normalise.
- Generer token opaque et QR participant, consulter la progression et permettre le renvoi avec anti-abus.
- Versionner l'email d'inscription et appliquer consentements, masquage et audit.
- Critere de sortie : un participant s'inscrit et recoit un QR exploitable sans PII dans le token ou le QR.

### Lot 6 - Validation commercant et progression

Etat : code implemente le 16 aout 2026. Le scan participant utilise la session commercant et une etape deterministe, les doublons sont neutralises en base, la velocite anormale est isolee, et progression, qualification et annulation motivee sont transactionnelles. Validation `pytest` a executer dans l'environnement Python du projet avant integration.

- Distinguer les parcours QR participant et QR coffret.
- Enregistrer la validation depuis la session commercant avec unicite, idempotence et anti-fraude.
- Calculer progression et qualification et permettre l'annulation motivee.
- Livrer les filtres et listes de validations et coordonner la premiere version de l'application commercant.
- Critere de sortie : un scan valide fait progresser le participant et les doublons sont neutralises.

### Lot 7 - Live, workflow et vues globales

Etat : code implemente le 16 aout 2026. Workflow, live avec polling conseille a 15 secondes, flux recent, dashboard, inbox tenant, audit partenaire et vues globales sont exposes. Les vues Tirages/Gains sont contractuellement disponibles et seront alimentees par les objets du Lot 8. Validation `pytest` a executer dans l'environnement Python du projet avant integration.

- Exposer workflow, prochaine action, live par polling de 15 secondes et flux recent par curseur.
- Implementer dashboard et vues globales Participants, Validations, Tirages/Gains, Flyers et Bilans.
- Ajouter inbox, lecture groupee, alertes actionnables et audit partenaire.
- Critere de sortie : le portail pilote l'animation et couvre les vues prevues par la maquette V2.

### Lot 8 - Cloture, tirage et gains

Etat : code implemente le 16 aout 2026. La cloture manuelle et automatique gele une population eligible
versionnee sous verrou transactionnel. Le tirage cryptographique alloue les lots dans leur ordre configure,
cree les suppleants sans doublon et peut etre rejoue sans nouvelle allocation. Le remplacement motive,
l'envoi/relance idempotents et les vues de consommation des coffrets sont exposes par l'API. La distribution
du coffret est planifiee par une operation `GAIN_ANIMATION` et active une instance reservee par l'achat
professionnel Stripe du partenaire. Aucun achat a zero euro n'est cree lors de l'attribution.

- Implementer cloture automatique et manuelle avec verrouillage et gel versionne des eligibles.
- Executer le tirage cryptographique, l'affectation ordonnee des lots et la liste de suppleants.
- Remplacer un gagnant avec motif, envoyer ou relancer le gain de maniere idempotente.
- Initialiser le paiement professionnel Stripe des lots, reserver les `CoffretInstance` apres confirmation et bloquer la publication avant couverture complete.
- Activer une `CoffretInstance` prepayee et notifier par email ou push lors de l'envoi du gain.
- Critere de sortie : une animation est cloturee et ses gains distribues sans double attribution.

### Lot 9 - Bilans, exports et conservation

Etat : code implemente le 16 aout 2026. Les bilans consolident participants, validations, gains et
indicateurs commercants. Les exports CSV UTF-8 BOM et PDF sont servis en reponse privee sans stockage
public persistant. La lecture groupee des notifications et l'archivage groupe avec resultat unitaire sont
exposes. Le batch interne de conservation supporte le mode simulation, anonymise les participants apres
12 mois, supprime les tokens apres 3 mois et les notifications apres 12 mois.

- Consolider bilan et indicateurs puis produire les exports CSV synchrones ou asynchrones.
- Ajouter les fonctions P2 retenues : export PDF, archivage groupe et lecture groupee des notifications.
- Appliquer stockage prive, expiration des fichiers, purge, anonymisation et pseudonymisation.
- Couvrir les durees RGPD par des tests automatises.
- Critere de sortie : les donnees sont exportables, archivables et purgees conformement aux regles validees.

### Lot 10 - Industrialisation et mise en production

Etat : socle logiciel implemente le 16 aout 2026. La supervision interne globale, le diagnostic,
l'audit et les corrections exceptionnelles sur liste blanche sont exposes et proteges par une session
administrateur. Un diagnostic de readiness rend explicites les prerequis externes et interdit de confondre
code termine et autorisation de mise en production. Les contrats OpenAPI de l'Epic 41 sont tous implementes.

Prerequis externes restant a valider dans chaque environnement avant production : domaine public HTTPS,
stockage objet prive, secrets et webhooks Stripe, identite et contenus email, conformite du rendu implemente
a la direction artistique validee des flyers,
recette bout en bout de la premiere version de l'application commercant et validation juridique RGPD tracee.

Integration des surfaces internes : la console d'administration expose une supervision Animation avec
diagnostic, audit, correction encadree, readiness, partenaires, gestionnaires, habilitations, offres et
abonnements en lecture controlee. Localeo Control affiche les animations, compteurs et alertes avec polling
de 15 secondes et redirige toute correction vers la console d'administration.

Le backoffice porte egalement un parcours guide de referencement initial : creation du partenaire,
selection d'une ou plusieurs communes, activation administrative de l'offre sur chaque commune,
creation du premier gestionnaire avec toutes les permissions Animation et mise en file de son email
d'invitation. L'ensemble est journalise avec l'identite de l'administrateur connecte.
La gestion courante s'appuie sur trois consoles metier : catalogue des offres et de leur utilisation,
habilitations par gestionnaire et commune, et Vision 360 partenaire regroupant abonnements, territoires,
utilisateurs, animations, alertes et audit recent.

- Finaliser Stripe et ses webhooks, les contenus email et implementer la direction artistique validee des flyers.
- Configurer le domaine HTTPS et le stockage objet heberge, puis recetter la premiere version de l'application commercant.
- Tracer la validation juridique RGPD.
- Ajouter supervision, metriques, alertes et tests de charge, securite, reprise et non-regression.
- Critere de sortie : tous les prerequis de production sont traces et valides.

### Lot 11 - Actualites d'animation et diffusion Localeo Live

Etat : backend/backoffice implemente le 23 aout 2026 ; frontend Localeo Animation et diffusion/UX Localeo Live restant a raccorder. `ARB-65` a `ARB-69` valides.

- Faire evoluer `activites_locales` avec le rattachement relationnel `animation_id`, le type `ACTUALITE_ANIMATION` et les index de lecture.
- Ajouter le port inter-domaines et les use cases de gestion sous controle du tenant et de la permission issue de `ARB-68`.
- Exposer l'onglet et les APIs de gestion des actualites depuis la fiche Localeo Animation.
- Enrichir le feed public et son filtre fonctionnel `ANIMATION` avec la reference Animation et le deep link tranche par `ARB-67`.
- Etendre la diffusion Localeo Live et la deduplication inbox/WebPush selon l'audience et la semantique tranchees par `ARB-65` et `ARB-66`.
- Appliquer aux brouillons, publications et programmations les transitions tranchees par `ARB-69`.
- Mettre a jour les contrats OpenAPI Epic 41 et Epic 42, les migrations, l'audit et les recettes bout en bout.
- Critere de sortie : une actualite est geree depuis Localeo Animation, visible dans `En direct > Animations` et notifiee une seule fois aux installations eligibles.

### Dependances et jalons

Ordre nominal historique : `Lot 0 -> Lot 1 -> Lot 2 -> Lot 3 -> Lot 4 -> Lot 5 -> Lot 6 -> Lot 8 -> Lot 9 -> Lot 10`. L'evolution `Lot 11` depend des Lots 3 et 7 ainsi que des lots Backend B3-B5 de l'Epic 42.

- Le Lot 7 peut demarrer apres le Lot 3 et progresser en parallele des Lots 4 a 6.
- Premier increment demonstrable : Lots 0 a 4.
- Premier parcours metier complet : Lots 0 a 8.
- Les secrets Stripe, contenus et assets definitifs, domaine HTTPS, stockage objet et validation juridique ne bloquent pas le socle ; ils conditionnent les recettes ou la production selon `ARB-53` a `ARB-59`.

### Rattachement principal des tickets existants

| Lot | Tickets principaux |
| --- | --- |
| Lot 0 | `EP41-T01`, `EP41-T21`, `EP41-T22`, `EP41-T34`, `EP41-T38`, `EP41-T43` |
| Lot 1 | `EP41-T24`, `EP41-T29` |
| Lot 2 | `EP41-T25`, `EP41-T40` |
| Lot 3 | `EP41-T02` a `EP41-T05` |
| Lot 4 | `EP41-T31`, `EP41-T36`, `EP41-T42`, `EP41-T46` |
| Lot 5 | `EP41-T06` a `EP41-T10`, `EP41-T41` |
| Lot 6 | `EP41-T11` a `EP41-T13`, `EP41-T44` |
| Lot 7 | `EP41-T19`, `EP41-T20`, `EP41-T26`, `EP41-T32`, `EP41-T33` |
| Lot 8 | `EP41-T14` a `EP41-T17`, `EP41-T27`, `EP41-T28`, `EP41-T37` |
| Lot 9 | `EP41-T18`, `EP41-T30`, `EP41-T35`, `EP41-T39`, `EP41-T45` |
| Lot 10 | Finalisation de `EP41-T40` a `EP41-T46`, supervision et criteres de mise en production |
| Lot 11 | `EP41-T51` actualites d'animation, feed Localeo Live et notifications |

`EP41-T00` correspond au cadrage deja realise. Un ticket transverse peut etre amorce dans son lot principal puis finalise au Lot 10 lorsque sa dependance externe devient disponible.

## Regroupement historique de cadrage - remplace

La section suivante est conservee pour la tracabilite des besoins et criteres UX initiaux. Ses numeros de lots ne pilotent plus l'ordre d'implementation ; la section precedente est la reference.

### Lot 0 - Finalisation cadrage produit et UX

- Valider les arbitrages ouverts avant implementation.
- Decrire les ecrans de la plateforme partenaire dediee : liste animations, creation, configuration, pilotage, cloture, bilan.
- Decrire la vue workflow globale : etapes, etape courante, prochaines actions, blocages, affichage liste et fiche animation.
- Decrire le dashboard de performance : indicateurs, filtres, comparaisons, droits et limites d'exposition des donnees personnelles.
- Decrire la vue live organisateur : indicateurs, flux recent, alertes, et actions disponibles.
- Decrire le comportement tenant commune du portail partenaire : selection commune, droits, filtres, messages d'acces refuse.
- Decrire le parcours abonnement : offre, souscription ou activation, statut, blocage/degradation d'acces, support Localeo.
- Decrire les ecrans back-office Localeo de supervision et d'administration.
- Decrire la vision live Localeo : indicateurs, flux d'evenements, alertes et actions de support autorisees.
- Decrire les parcours publics : fiche animation, inscription, progression.
- Decrire le gabarit du flyer PDF : informations affichees, QR, logo, charte Localeo, apercu, telechargement et regeneration.
- Decrire les parcours application mobile participant : commune, inscriptions actives, historique, detail, QR participant.
- Decrire le parcours commercant de validation.
- Figer les contrats API MVP et les evenements d'audit.

#### Livrables Lot 0 a produire avant implementation

Le Lot 0 doit produire un cadrage assez precis pour permettre aux lots de developpement de demarrer sans reouvrir les arbitrages fonctionnels. Les livrables sont des maquettes fonctionnelles ou descriptions ecran, des regles UX, les contrats API cible et la liste des evenements d'audit.

##### Plateforme partenaire dediee

Ecrans MVP a cadrer :
- Accueil partenaire avec selection du tenant commune actif si le gestionnaire est habilite sur plusieurs communes.
- Dashboard de performance des animations, avec filtres periode, tenant commune, modele, statut et animation.
- Liste des animations avec recherche, filtres, indicateur de workflow, statut, periode, participants, alertes et actions rapides.
- Catalogue des modeles avec detail du modele `PASSEPORT_COMMERCANT`, prerequis, exemple de parcours et parametres configurables.
- Assistant de creation d'animation : modele, tenant commune, informations publiques, dates, commercants sollicites, acceptations, coffrets a gagner, regles et recapitulatif ; le flyer est genere a la publication.
- Fiche animation avec onglets : workflow, live, configuration, participants, validations, tirage, gains/coffrets, flyer, bilan, audit.
- Ecrans de cloture, tirage, envoi des gains et suivi de consommation des coffrets gagnes.

Regles UX :
- L'utilisateur ne doit jamais creer une animation hors tenant commune actif.
- Les actions impossibles doivent rester visibles uniquement si elles aident a comprendre le blocage, avec une raison actionnable.
- Les actions sensibles, publication, cloture, tirage et envoi des gains, demandent une confirmation explicite.
- La cloture arretera inscriptions et validations et figera atomiquement la population eligible ; le retour UI affichera le nouvel etat et la prochaine action.
- Les alertes, notifications et actions recommandees ouvrent directement la fiche dans l'onglet actionnable concerne.
- Toute commande declenchee depuis le portail affiche un retour de succes ou d'echec ; les traitements asynchrones exposent un statut consultable.
- La confirmation de publication distingue l'activation, la generation du QR d'inscription et l'etat de sa diffusion aux commercants.
- Les donnees personnelles participant sont masquees par defaut dans les vues agregees.
- Les vues doivent distinguer clairement pilotage live, bilan d'une animation et dashboard de performance multi-animations.

##### Workflow global d'une animation

Le workflow affiche au minimum les etapes :
- `BROUILLON`
- `CONFIGURATION`
- `PRETE_A_PUBLIER`
- `PUBLIEE`
- `EN_COURS`
- `CLOTUREE`
- `TIRAGE_A_LANCER`
- `GAINS_A_ENVOYER`
- `BILAN_DISPONIBLE`
- `ARCHIVEE`
- `ANNULEE`

Pour chaque etape, la vue doit afficher :
- etape courante ;
- etapes deja terminees ;
- etapes restantes ;
- prochaine action attendue ;
- actions disponibles selon droits, statut et abonnement ;
- blocages et raisons : configuration incomplete, abonnement inactif, periode non ouverte, QR non disponible, participants non eligibles, tirage bloque, gains non envoyes, bilan indisponible.

##### Dashboard de performance

Indicateurs MVP :
- animations creees, publiees, en cours, terminees, cloturees et archivees ;
- participants inscrits, participants ayant termine, taux de completion, progression moyenne ;
- participants qualifies et taux de qualification ;
- validations totales, validations par animation, validations par commercant et validations recentes ;
- tirages realises, gagnants, coffrets envoyes, coffrets actifs, coffrets consommes, coffrets partiellement consommes, coffrets expires et taux de consommation ;
- montant potentiel restant a reinjecter et repartition du montant reinjecte par commercant ;
- coffrets entierement non consommes expirant bientot, avec horizon retourne et configurable (30 jours par defaut) ;
- delai moyen entre l'envoi du gain et sa premiere consommation, accompagne du nombre de coffrets observes ;
- commercants participants effectifs sans aucune validation, accompagne du nombre total de commercants participants effectifs ;
- alertes de sous-performance : faible inscription, faible completion, absence de validation, coffrets non consommes, tirage non lance, gains non envoyes.

Les definitions, populations, cas limites et contrats de ces indicateurs sont specifies dans [Indicateurs economiques et d'usage des gains](../../specifications/epic-41-api/indicateurs-economiques.md).

Filtres MVP :
- periode ;
- tenant commune ;
- modele d'animation ;
- statut ;
- animation.

Contraintes :
- aucune donnee personnelle participant dans les vues agregees ;
- comparaison limitee aux animations visibles par le gestionnaire ;
- lecture des donnees de consommation depuis `gestion_achats`, sans duplication des statuts source.

##### Parcours abonnement et acces

Ecrans et etats a cadrer :
- consultation de la formule, du statut, des dates et du tenant commune couvert ;
- affichage d'un bandeau d'acces limite si l'abonnement n'est pas actif ;
- blocage des nouvelles actions payantes si l'abonnement est expire, suspendu ou resilie ;
- maintien des actions de finalisation autorisees pour une animation publiee ou en cours ;
- message support Localeo si le gestionnaire ne comprend pas le blocage.

Messages de blocage minimaux :
- abonnement inactif ;
- tenant commune non habilite ;
- action reservee Localeo ;
- animation non modifiable dans son statut courant ;
- coffret non eligible car hors commune ou inactif ;
- tirage impossible car population eligible non figee.

##### Back-office Localeo

Ecrans MVP a cadrer :
- supervision live globale des animations ;
- filtre par commune, partenaire, statut, modele et anomalie ;
- detail d'une animation creee par un partenaire ;
- consultation des workflows et blocages ;
- consultation du dashboard de performance agrege ;
- consultation et correction des abonnements plateforme ;
- correction exceptionnelle d'une animation avec motif obligatoire ;
- audit des actions sensibles.

Localeo ne doit pas etre le canal nominal de creation et d'animation. Les actions d'administration restent des actions de support ou correction exceptionnelle.

##### Parcours publics participant

Ecrans MVP a cadrer :
- page publique animation contextualisee ;
- formulaire d'inscription : email, nom, prenom, telephone, consentements ;
- page de confirmation apres inscription ;
- page de consultation de progression via token ;
- etat d'une animation non ouverte, terminee ou cloturee ;
- erreur QR invalide, expire ou remplace.

##### Application mobile participant

Ecrans MVP a cadrer :
- selection ou detection de commune ;
- animations en cours de la commune ;
- inscriptions actives ;
- historique des animations participees ;
- detail animation ;
- QR participant ;
- detail du gain et coffret gagne ;
- opt-in push et etat d'abonnement push.

##### Application mobile commercant

Parcours MVP a cadrer :
- scan du QR participant ;
- reconnaissance d'un QR animation distinct du QR coffret ;
- affichage du participant et de l'animation avec donnees minimales ;
- validation d'etape ;
- refus explicite : animation inactive, participant invalide, commercant non eligible, doublon, hors periode, validation trop rapprochee ;
- confirmation de validation et mise a jour de progression.

##### Flyer PDF

Gabarit MVP :
- format PDF standard ;
- logo Localeo et charte Localeo ;
- nom de l'animation ;
- commune ;
- dates ;
- organisateur ou partenaire ;
- court texte de presentation ;
- QR d'inscription public ;
- URL d'inscription ;
- mention simple de participation et d'information personnelle.

Regles :
- le QR du flyer est toujours le QR d'inscription public ;
- le flyer ne contient aucun QR participant ni token gestionnaire ;
- le PDF est marque a regenerer si les informations publiques ou le QR changent ;
- le binaire et les metadonnees sont portes par `documentaire`.

##### Contrats API MVP a figer

Les contrats doivent respecter l'Epic 40 :
- paths prefixes par `/public/animation-locale`, `/protected/animation-locale`, `/internal/animation-locale` ou `/admin/api/animation-locale` ;
- tag OpenAPI principal `Animation locale` ;
- distinction d'usage public, protege et interne par tags OpenAPI complementaires ;
- schemas d'erreur homogenes pour acces refuse, abonnement bloque, tenant non habilite, statut incompatible et validation refusee.

Endpoints a figer en Lot 0 :
- catalogue et detail modele ;
- creation, lecture, modification, publication et cloture animation ;
- workflow animation ;
- live animation ;
- dashboard de performance ;
- flyer PDF ;
- inscription participant ;
- progression participant ;
- validation commercant ;
- tirage ;
- envoi des gains ;
- suivi de consommation coffrets ;
- bilan et export CSV ;
- supervision Localeo.

##### Evenements d'audit MVP a figer

Evenements minimaux :
- `ANIMATION_CREEE`
- `ANIMATION_CONFIGUREE`
- `ANIMATION_PUBLIEE`
- `ANIMATION_DEPUBLIEE`
- `ANIMATION_CLOTUREE`
- `ANIMATION_ANNULEE`
- `ANIMATION_FLYER_GENERE`
- `ANIMATION_FLYER_TELECHARGE`
- `ANIMATION_FLYER_REMPLACE`
- `PARTICIPANT_INSCRIT`
- `QR_PARTICIPANT_RENVOYE`
- `VALIDATION_ETAPE_ACCEPTEE`
- `VALIDATION_ETAPE_REFUSEE`
- `PARTICIPANT_QUALIFIE`
- `TIRAGE_LANCE`
- `GAIN_ATTRIBUE`
- `GAIN_ENVOYE`
- `COFFRET_GAIN_ACTIVE`
- `NOTIFICATION_GAIN_ENVOYEE`
- `BILAN_CONSULTE`
- `BILAN_EXPORTE`
- `ABONNEMENT_PLATEFORME_MODIFIE`
- `CORRECTION_EXCEPTIONNELLE_LOCALEO`

Chaque evenement sensible doit porter acteur, date, tenant commune, animation, action, motif si obligatoire, ancienne valeur et nouvelle valeur quand applicable, correlation technique et source de l'action.

##### Definition de pret du Lot 0

Le Lot 0 est considere termine lorsque :
- la maquette `localeo-animation-maquette-v2.zip` est la reference UX tracee dans le backlog, le DCT et l'analyse API ;
- les ecrans MVP sont listes et decrits ;
- les transitions et blocages du workflow sont figes ;
- les indicateurs du dashboard de performance sont figes ;
- les messages d'acces refuse et d'abonnement bloque sont definis ;
- les endpoints MVP sont listes avec leur usage public/protege/interne ;
- les contrats de reponse des commandes portent nouvel etat, prochaine action, ressource produite et statut de traitement lorsque applicable ;
- les evenements d'audit sensibles sont listes ;
- les donnees personnelles visibles par ecran sont explicitement limitees ;
- les points de validation juridique RGPD sont isoles avant production.

### Lot 1 - Socle domaine animation

- Creer l'enveloppe `animation_locale` prevue par l'Epic 40 si elle n'existe pas encore dans le code cible.
- Creer les concepts `ModeleAnimation`, `TenantCommuneAnimation`, `Animation`, gestionnaire d'animation, organisateur, participants, etapes, validations, lots, tirages, flyers et bilans.
- Creer les concepts `DefinitionModeleAnimation`, `StrategieModeleAnimation` et `RegistreModelesAnimation`.
- Definir la frontiere entre socle generique et strategie `PASSEPORT_COMMERCANT`.
- Definir le contrat de strategie : verification configuration, publication, validation terrain, progression, qualification, anti-fraude et indicateurs.
- Brancher la strategie `PASSEPORT_COMMERCANT` via le registre de modeles, sans conditions dispersees dans les use cases generiques.
- Definir les statuts et transitions.
- Definir la projection `VueWorkflowAnimation` a partir des statuts, transitions, droits, abonnement et invariants metier.
- Definir la projection `DashboardPerformanceAnimation` a partir des animations, validations, tirages, gains et donnees de consommation `gestion_achats`.
- Definir les value objects : periode d'animation, statut, configuration, seuil de qualification, token de participation, QR d'inscription, QR participant, flyer PDF, code de validation.
- Definir le rattachement obligatoire d'une animation a un tenant commune.
- Definir les controles de droits gestionnaire par tenant commune.
- Definir la matrice de droits `GESTIONNAIRE_ANIMATION` et les droits reserves a Localeo.
- Definir le port applicatif de verification du `DroitAccesPlateformeAnimation`.
- Ajouter les repositories domaine.
- Ajouter les ports d'acces au core Localeo.
- Ajouter les regles d'import inter-domaines specifiques a `animation_locale`.

### Lot 2 - Catalogue, creation et publication self-service

- Lister les modeles.
- Previsualiser un modele.
- Creer une animation depuis un modele par un gestionnaire d'animation depuis la plateforme partenaire dediee.
- Configurer organisateur, tenant commune, dates et commercants.
- Implementer le modele `PASSEPORT_COMMERCANT`.
- Configurer les regles de progression et qualification.
- Gerer les etapes associees aux commercants.
- Generer, previsualiser, telecharger et regenerer le flyer PDF de communication.
- Valider la configuration avant publication.
- Publier et de-publier une animation selon les transitions autorisees.
- Exposer les endpoints `/protected/animation-locale` de gestion self-service.

### Lot 2 bis - Abonnement et droit d'acces plateforme

- Creer le domaine transverse dedie `abonnements_plateforme` et son port de verification des droits consomme par `animation_locale`.
- Integrer Stripe Billing comme mode d'encaissement MVP.
- Definir les formules d'abonnement MVP : libelle, prix, periode, conditions d'activation et droits associes.
- Definir les statuts d'abonnement MVP : actif, en essai si retenu, suspendu, expire, resilie.
- Rattacher chaque abonnement a une formule, un partenaire donne et une commune donnee.
- Exposer un droit d'acces simple consomme par `animation_locale`.
- Laisser les animations publiees ou en cours aller a leur terme en cas d'expiration d'abonnement, puis cloturer les acces.
- Bloquer ou degrader les nouvelles actions self-service payantes si l'abonnement n'est pas actif.
- Afficher au gestionnaire le statut d'abonnement, la formule, les dates, le perimetre couvert et le motif de blocage.
- Permettre a Localeo de consulter et modifier l'abonnement : statut, formule, dates, perimetre, motif de suspension et exception d'acces.
- Auditer toute modification d'abonnement.

### Lot 3 - Parcours participant public

- Generer le QR d'inscription public d'une animation.
- Inscrire les participants.
- Collecter email, nom, prenom, telephone et consentements minimaux.
- Generer le token de participation.
- Generer le QR participant personnel.
- Envoyer l'email d'inscription avec les informations de l'animation et le QR participant directement dans le message.
- Afficher la progression publique via token.
- Exposer les endpoints `/public/animation-locale`.

### Lot 3 bis - Application mobile participant

- Lister les animations en cours d'une commune.
- Lister les animations auxquelles le participant est inscrit.
- Lister l'historique des animations auxquelles le participant a participe.
- Afficher le detail d'une animation.
- Afficher le QR participant.
- Gerer l'opt-in et l'abonnement push participant si le canal push est active pour les notifications de gain.
- Exposer les endpoints publics tokenises necessaires a l'application mobile.

### Lot 4 - Validation commercant et qualification

- Faire evoluer l'application mobile commercant pour scanner les QR participants d'animation.
- Valider les etapes via QR participant scanne depuis l'application mobile commercant.
- Ajouter les controles anti-fraude MVP.
- Recalculer la progression apres validation.
- Qualifier automatiquement les participants.
- Exposer les endpoints `/protected/animation-locale`.

### Lot 5 - Cloture, lots et tirage simple

- Configurer dotations et lots.
- Configurer uniquement des lots references sur des coffrets Localeo actifs de la commune de l'animation.
- Acheter/reserver les coffrets lots apres acceptation des commercants et avant publication par le partenaire.
- Restreindre les coffrets lots aux coffrets actifs de la commune de l'animation.
- Cloturer l'animation.
- Calculer la population eligible.
- Figer la population eligible a la fin ou cloture.
- Rendre disponible l'action de tirage pour le gestionnaire habilite.
- Lancer et executer les tirages.
- Historiser les gagnants et lots attribues.
- Envoyer les gains aux vainqueurs.
- Creer et activer automatiquement les `CoffretInstances` pour tous les gains.
- Ajouter le suivi de consommation des coffrets envoyes aux vainqueurs.
- Notifier les gagnants par email et notification push participant.

### Lot 6 - Bilan et exploitation

- Produire les statistiques.
- Produire les indicateurs de consommation des coffrets gagnes : envoyes, actifs, consommes, partiellement consommes, expires, prestations restantes.
- Produire les indicateurs economiques et d'usage des gains : potentiel restant, expirations proches, delai de premiere consommation, commercants sans validation et repartition du montant reinjecte.
- Exporter le bilan en CSV.
- Ajouter les vues de la plateforme partenaire dediee.
- Ajouter le dashboard de performance des animations dans la plateforme partenaire.
- Ajouter la vue live organisateur dans la plateforme partenaire.
- Ajouter la vue workflow globale dans la liste et la fiche animation.
- Ajouter les vues back-office Localeo de supervision.
- Ajouter la vision live Localeo des animations de la plateforme, agregee et filtrable par commune.
- Ajouter le flux live des evenements d'animation.
- Ajouter les alertes operationnelles liees aux animations.
- Ajouter audit et tests.
- Ajouter les traitements de purge et d'anonymisation des donnees d'animation.
- Ajouter la suppression automatique des exports CSV apres 90 jours maximum.
- Exposer les endpoints `/internal/animation-locale` et `/admin/api/animation-locale`.

### Lot 7 - Extensions post-MVP

- Gerer les partenaires contributeurs.
- Gerer les groupes de participants.
- Ajouter un portail partenaire avance multi-utilisateurs.
- Ajouter les notifications multicanales avancees.
- Ajouter les exports PDF ou documents de bilan enrichis.
- Ajouter d'autres modeles d'animation.

## Arbitrages actes

- Tenant commune : utiliser une commune du referentiel comme tenant fonctionnel MVP ; reporter les animations multi-communes et l'entite `TerritoireAnimation` dediee.
- Moteur generique : separer socle generique, definition de modele, registre et strategie metier par modele ; `PASSEPORT_COMMERCANT` est la premiere strategie, pas le fonctionnement code en dur du moteur.
- Gestionnaire d'animation : rattacher chaque animation a un organisateur ou partenaire habilite, autoriser l'habilitation sur plusieurs communes et imposer la selection explicite du tenant commune actif.
- Workflow animation : afficher une vue synthetique globale, derivee du statut et des invariants metier, pour situer rapidement l'animation et les actions possibles.
- Dashboard performance : fournir au gestionnaire une vue agregee, filtrable et comparative de ses animations, sans exposition de donnees personnelles participant.
- Droits gestionnaire : retenir un role MVP `GESTIONNAIRE_ANIMATION`, scope par tenant commune, couvrant creation, configuration, modification avant publication, publication, suivi live, cloture, tirage, envoi des gains, bilan et export.
- Droits reserves Localeo : supervision globale, support, correction exceptionnelle, administration tous tenants et modification des abonnements plateforme.
- Abonnement plateforme : ne pas le modeliser comme un objet interne `animation_locale`; exposer un droit d'acces actif consomme par le portail partenaire.
- Abonnement plateforme : modele par formule pour un partenaire donne et une commune donnee, avec encaissement Stripe Billing.
- Abonnement expire : laisser les animations publiees ou en cours aller a leur terme avant cloture des acces ; bloquer les nouvelles actions payantes hors finalisation autorisee.
- Organisateur : stocker les informations organisateur directement sur l'animation au MVP ; creer une entite organisateur seulement si plusieurs animations doivent partager le meme organisateur.
- Participant : ne pas creer de compte participant ; utiliser une inscription simple avec token de participation.
- Participant : collecter email, nom, prenom et telephone a l'inscription.
- Inscription : privilegier un parcours QR d'inscription -> page contextualisee -> email de confirmation avec informations animation et QR participant integre.
- Flyer de communication : generer un PDF depuis la creation ou configuration de l'animation, avec logo et charte Localeo, informations publiques, QR d'inscription et URL publique.
- Flyer de communication : gerer l'apercu, le telechargement, la regeneration et le remplacement du PDF existant sans exposer de notion de version au gestionnaire.
- Flyer de communication : utiliser le domaine `documentaire` ou le service documentaire retenu pour le binaire et les metadonnees, sans stocker le PDF directement en base `animation_locale`.
- Validation : scanner le QR participant depuis l'application mobile commercant, a faire evoluer pour supporter les animations ; le QR participant reste separe du QR coffret et de ses invariants `gestion_achats`.
- Anti-fraude MVP : refuser hors periode, hors commercant eligible, doublon d'etape, validation trop rapprochee et participant invalide.
- Notification gagnant : email et push MVP ; le push impose une application Localeo participant avec opt-in et abonnement push. SMS et relances avancees restent post-MVP.
- Coffret gagne : creer et activer automatiquement la `CoffretInstance` a l'envoi du gain, avec origine `GAIN_ANIMATION` et idempotence stricte.
- Coffret gagne : les lots a gagner sont obligatoirement des coffrets Localeo actifs de la commune de l'animation, font partie de son budget et sont achetes par le partenaire apres acceptation des commercants et avant publication.
- Suivi consommation coffret gagne : lire les statuts, validations et prestations restantes depuis `gestion_achats`, sans recreer de logique de consommation dans `animation_locale`.
- Export bilan : CSV MVP ; PDF ou document enrichi post-MVP.
- Donnees participants : conserver les donnees nominatives jusqu'a fin d'animation + 12 mois, puis anonymiser.
- QR/tokens participant : revoquer ou supprimer au plus tard fin d'animation + 3 mois.
- Validations detaillees : conserver 24 mois, puis anonymiser les references participant nominatives.
- Tirages et gains : conserver 5 ans avec participant pseudonymise lorsque l'identite nominative n'est plus necessaire.
- Exports CSV : supprimer automatiquement apres 90 jours maximum.
- Notifications : conserver les traces email/push 12 mois, puis purger ou anonymiser.
- Audit et securite : conserver les logs lies a l'animation 24 mois.

## Points de vigilance avant production

- Valider juridiquement la politique de conservation, d'anonymisation et d'information participant avant mise en production.

## Proposition de tickets implementables

- `EP41-T00` Finaliser le Lot 0 produit/UX : ecrans, parcours, workflow, dashboard, abonnement, flyer, API, audit, donnees personnelles et definition de pret.
- `EP41-T01` Modeliser les concepts de base du domaine `animation_locale`.
- `EP41-T02` Creer le catalogue des modeles d'animations.
- `EP41-T03` Ajouter la creation self-service d'une animation depuis un modele par un organisateur ou partenaire.
- `EP41-T04` Ajouter la configuration self-service : organisateur, tenant commune, dates, regles et commercants.
- `EP41-T05` Implementer le modele `Passeport commercant`.
- `EP41-T06` Ajouter l'inscription des participants.
- `EP41-T07` Ajouter le QR d'inscription public et la page d'inscription contextualisee.
- `EP41-T08` Ajouter l'envoi email du QR participant personnel.
- `EP41-T09` Ajouter l'application mobile participant : animations de la commune, inscriptions actives, historique, detail et QR.
- `EP41-T10` Ajouter la progression participant via token.
- `EP41-T11` Ajouter la validation d'etape chez un commercant via scan du QR participant depuis l'application mobile commercant.
- `EP41-T12` Ajouter les controles anti-fraude MVP.
- `EP41-T13` Ajouter la qualification automatique.
- `EP41-T14` Ajouter les dotations et lots.
- `EP41-T15` Ajouter la cloture manuelle et automatique.
- `EP41-T16` Ajouter le lancement des tirages au sort simples apres fin ou cloture de l'animation.
- `EP41-T17` Ajouter les notifications gagnants par email ou push avec audit, idempotence et reprise en cas d'echec.
- `EP41-T18` Ajouter le bilan d'animation et son export CSV.
- `EP41-T19` Ajouter les vues de la plateforme partenaire dediee et back-office de supervision.
- `EP41-T20` Ajouter la vision live Localeo des animations : indicateurs, flux d'evenements et alertes.
- `EP41-T21` Ajouter les APIs avec paths et tags OpenAPI `Animation locale`.
- `EP41-T22` Documenter les integrations avec le core Localeo.
- `EP41-T23` Reporter explicitement partenaires contributeurs, groupes, portail partenaire avance, notifications avancees et exports enrichis en post-MVP.
- `EP41-T24` Ajouter le tenant fonctionnel par commune : modele, droits gestionnaire, filtres portail, filtres publics et supervision Localeo.
- `EP41-T25` Ajouter la gestion d'abonnement plateforme : droit d'acces, consultation, modification auditee, statut, blocages self-service, affichage portail et supervision Localeo.
- `EP41-T26` Ajouter la vue live organisateur : etat animation, inscriptions, validations, progression, qualifies, alertes et actions disponibles.
- `EP41-T27` Ajouter l'envoi des gains coffrets : creation et activation automatique de `CoffretInstance`, origine `GAIN_ANIMATION`, idempotence, audit et notification gagnant.
- `EP41-T28` Ajouter le suivi de consommation des coffrets envoyes aux vainqueurs : statuts, validations, prestations consommees/restantes, alertes, droits et export.
- `EP41-T29` Ajouter la matrice de permissions `GESTIONNAIRE_ANIMATION` : cycle nominal par tenant commune et droits reserves Localeo.
- `EP41-T30` Ajouter la politique de conservation, purge et anonymisation des donnees d'animation : participants, QR/tokens, validations, gains, notifications, exports et audit.
- `EP41-T31` Ajouter le flyer PDF de communication : gabarit Localeo, QR d'inscription, informations animation, apercu, telechargement, regeneration, stockage documentaire et audit.
- `EP41-T32` Ajouter la vue workflow globale d'une animation : etapes, etat courant, blocages, prochaines actions, affichage liste/fiche et supervision Localeo.
- `EP41-T33` Ajouter le dashboard de performance des animations : indicateurs, filtres, comparaisons, droits tenant commune, anonymisation et supervision Localeo.
- `EP41-T34` Ajouter le moteur generique de modeles d'animation : definition de modele, registre, strategie `PASSEPORT_COMMERCANT`, contrat de strategie et separation du socle generique.
- `EP41-T35` Ajouter la reference participant pseudonymisee et l'export CSV des participants par animation.
- `EP41-T36` Completer le flyer avec accroche, URL d'inscription et telechargement securise coherent avec le documentaire.
- `EP41-T37` Ajouter le remplacement d'un gagnant par un suppleant et la relance de notification gagnant.
- `EP41-T38` Aligner les filtres maquette/API : alias `q`, periode dashboard, pagination et curseurs.
- `EP41-T39` Ajouter en P2 l'export PDF du bilan, la lecture groupee des notifications et l'archivage groupe.
- `EP41-T40` Configurer l'activation administrative des abonnements puis le raccordement Stripe test avec webhooks idempotents.
- `EP41-T41` Creer et versionner les gabarits email Animation avec identite d'envoi configurable et validation avant recette.
- `EP41-T42` Implementer la [direction artistique validee des flyers](../../specifications/epic-41-api/flyer-direction-artistique.md) : logo officiel Localeo Animation, palette des emails, composition editoriale, visuel principal avec repli, PDF A4, apercu PNG, zone sure `4:5`, QR imprime d'au moins 35 mm, URL de secours, explication du scan du QR personnel chez les commercants participants, declinaisons sociales et presse, versionnement de charte et tests de non-regression visuelle. Direction validee le 28 aout 2026 ; implementation restante.
- `EP41-T43` Ajouter les templates complets Animation et Participant par environnement et tester le remplacement des placeholders.
- `EP41-T44` Coordonner la premiere version de l'application commercant avec les deux parcours QR et leurs erreurs contractuelles, sans retrocompatibilite.
- Spécification d’implémentation associée : [Évolutions de l’application commerçant](../../specifications/epic-41-api/application-commercant.md), découpées en lots `COM-0` à `COM-7`. Les lots `COM-5` à `COM-7` couvrent la disponibilité par commune, la vue `Mes animations` et la notification d’inclusion.
- `EP41-T45` Implementer et tester les purges RGPD configurables, puis tracer la validation juridique comme prerequis de production.
- `EP41-T46` Raccorder `documentaire` a un stockage local puis objet prive, avec telechargements proteges ou URLs signees et retention configuree.
- `EP41-T47` Ajouter la suppression manuelle d'un participant avec permission `animation:supprimer_participant`, controle tenant, cascade tokens/validations, audit sans PII et blocage apres gel de la population eligible ou attribution d'un gain. Etat : implemente le 20 aout 2026.
- `EP41-T48` Exposer le contexte commercant avec l'indicateur explicite d'activation Animation pour la commune active et masquer la rubrique lorsqu'il est faux. Etat : implemente le 20 aout 2026.
- `EP41-T49` Exposer la liste et le detail des animations auxquelles le commerce connecte participe, sans donnees nominatives participant. Etat : implemente le 20 aout 2026.
- `EP41-T50` Produire une notification idempotente `ANIMATION_COMMERCANT_INCLUS`, persistee dans l'inbox et diffusee par WebPush lorsqu'un abonnement actif existe. Etat : implemente le 20 aout 2026 ; preference email dediee hors perimetre actuel.
- `EP41-T51` Ajouter les actualites rattachees aux animations : gestion dans Localeo Animation, projection `En direct > Animations`, notification Live configurable, OpenAPI, migration et recette bout en bout. Etat : backend/backoffice et diffusion inbox/WebPush Live implementes ; frontends et recette bout en bout a terminer.
- `EP41-T52` Ajouter au dashboard, au bilan et a la Vision 360 les cinq indicateurs economiques et d'usage des gains, leur horizon d'expiration configurable, leur reconciliation au centime et leurs tests de non-regression. Etat : specification finalisee le 28 aout 2026 ; implementation a faire.


## Correctifs de préproduction ANIM — 7 septembre 2026

Le [guide Animation et sa recette](../../produit/formation/backend/guide-animation-preproduction.md)
complète les critères de clôture, qualification, calendrier, financement et suivi
asynchrone. Les corrections ANIM-001 à ANIM-014 sont suivies dans le dépôt Animation;
leur validation technique ne vaut pas activation en production. Le statut produit
de cette epic reste inchangé.


## Compléments Animation

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### Lots d'implementation - decoupage de reference / Lot 10 - Industrialisation et mise en production

Prerequis externes restant a valider dans chaque environnement avant production : domaine public HTTPS,
stockage objet prive, secrets et webhooks Stripe, identite et contenus email, charte finale des flyers,
recette bout en bout de la premiere version de l'application commercant et validation juridique RGPD tracee.

- Finaliser Stripe et ses webhooks, les contenus email et la charte des flyers.

### Proposition de tickets implementables

- `EP41-T42` Rendre la charte des flyers configurable, fournir les assets temporaires et figer un rendu de reference avant recette visuelle.

### Correctifs ANIM de préproduction — 7 septembre 2026

Les critères de qualification, clôture, calendrier et suivi sont complétés par les [contrats corrigés](../../specifications/securisation-production/contrats-animation.md) et la [formation](../../produit/formation/animation/guide-animation-preproduction.md). Le statut produit de cette epic reste inchangé. Les preuves de test et les conditions d’activation figurent dans le [suivi de remédiation](../../audits/animation/remediation-2026-09-06.md).

## Compléments Commerçant

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### 1. Objet

Cette spécification décrit les évolutions à apporter à l’application commerçant Localeo pour prendre en charge les animations locales, sans modifier le parcours historique de validation des coffrets.

Le commerçant doit pouvoir utiliser un scanner unique, reconnaître un QR de coffret ou un QR personnel de participant à une animation, confirmer l’action adaptée et obtenir un résultat immédiatement compréhensible. Il doit également pouvoir consulter les animations auxquelles son commerce participe et être informé lorsqu’il est inclus dans une nouvelle animation.

Le backend Animation correspondant est implémenté. L’évolution de l’application reste un lot coordonné distinct, conformément aux arbitrages `ARB-47` et `ARB-57`.

### 2. Résultat attendu

À partir de l’espace commerçant authentifié :

1. le commerçant ouvre l’action `Scanner un QR` ;
2. l’application lit le QR sans interpréter ni afficher son secret ;
3. elle détermine le parcours `COFFRET` ou `ANIMATION` ;
4. elle affiche un écran de confirmation adapté ;
5. elle appelle exclusivement l’API correspondant au type détecté ;
6. elle présente le succès, le rejeu ou l’erreur métier ;
7. elle permet d’enchaîner avec un nouveau scan.

### 3. Décisions déjà validées

| Décision | Conséquence pour l’application |
| --- | --- |
| QR coffret et QR participant distincts | Aucun appel de validation coffret avec un token Animation, et inversement. |
| Identité du commerçant issue de la session | Aucun `commercant_id` n’est envoyé par le frontend. |
| Scope `commercant:validation` | Le bouton de scan est indisponible si la session ne possède pas ce scope. |
| Token participant opaque et sans PII | L’application ne décode jamais le token et ne le journalise pas. |
| Validation idempotente | Un retry réseau ne doit pas produire une seconde validation effective. |
| Contrôle de l’étape côté serveur | Le backend vérifie que le commerçant authentifié participe à l’animation. |
| Première version non déployée | Les deux parcours QR sont livrés ensemble, sans mécanisme de rétrocompatibilité. |
| Déploiement par commune | La rubrique Animation est visible uniquement si Localeo Animation est activé pour la commune active du commerce. |
| Inclusion à une animation | L’ajout effectif du commerce à une animation produit une notification idempotente adressée au commerçant. |

### 4. Périmètre fonctionnel

#### 4.1 Inclus

- scanner unique depuis l’accueil ou la rubrique Validations ;
- détection du parcours QR ;
- maintien du parcours coffret existant ;
- résolution d’un QR participant Animation ;
- présentation de l’animation, du participant masqué et de l’étape du commerce ;
- confirmation de validation ;
- gestion du doublon et des retries ;
- affichage de la progression retournée lorsqu’elle est disponible ;
- erreurs actionnables ;
- télémétrie sans token ni PII ;
- activation maîtrisée par feature flag pendant la recette initiale.
- rubrique `Animations` affichée uniquement dans une commune où Localeo Animation est déployé ;
- liste des animations auxquelles le commerce connecté participe ;
- détail en lecture seule d’une animation et statut de l’étape du commerce ;
- notification lors de l’inclusion du commerce dans une animation ;
- ouverture de l’animation concernée depuis la notification.

#### 4.2 Hors périmètre

- inscription d’un participant depuis l’application commerçant ;
- modification ou suppression d’un participant ;
- annulation d’une validation Animation par le commerçant au MVP ;
- consultation de la liste complète des participants ;
- tirage, gains, bilan ou gestion de l’animation ;
- validation hors ligne ou mise en file locale d’un scan ;
- décodage local des signatures ou secrets QR.

### 5. Navigation et écrans

#### 5.0 Disponibilité de la rubrique Animation

Après authentification et à chaque changement de commune active, l’application récupère les capacités fonctionnelles du contexte commerçant. La rubrique `Animations` et ses raccourcis ne sont rendus que si `animation_locale_disponible=true`.

Cette valeur est une décision backend fondée sur l’activation du service Localeo Animation pour la commune. Elle ne doit jamais être déduite d’une liste vide : une commune équipée peut ne disposer d’aucune animation à cet instant.

Lorsque `animation_locale_disponible=false` :

- aucun onglet, bloc d’accueil, badge ou raccourci Animation n’est visible ;
- l’application ne charge ni la liste ni les notifications Animation ;
- un lien profond Animation affiche un écran fonctionnel indisponible puis revient vers l’accueil ;
- le scanner Coffret reste disponible ; si un QR Animation est néanmoins scanné, le backend refuse l’action et l’application indique que le service n’est pas disponible dans cette commune.

#### 5.1 Point d’entrée

Le bouton principal reste `Scanner un QR`. Il ne faut pas créer deux scanners concurrents. Une aide courte indique : « Coffret ou animation Localeo ».

#### 5.2 États du parcours

| État | Contenu principal | Action |
| --- | --- | --- |
| `CAMERA` | Viseur, permission caméra, saisie manuelle de secours si déjà disponible | Scanner |
| `ANALYSE` | Indicateur bref, interaction verrouillée | Aucune |
| `CONFIRMATION_COFFRET` | Parcours existant inchangé | Continuer vers la prestation |
| `CONFIRMATION_ANIMATION` | Nom de l’animation, participant masqué, étape/commerce, statut de l’étape | Confirmer la validation |
| `SUCCES_ANIMATION` | Animation, participant masqué, heure, progression si disponible | Scanner un autre QR |
| `DEJA_VALIDEE` | Information non bloquante : étape déjà enregistrée | Fermer ou scanner à nouveau |
| `ERREUR` | Message actionnable et identifiant de corrélation | Réessayer ou fermer |

#### 5.3 Écran de confirmation Animation

Afficher uniquement :

- nom de l’animation ;
- commune ;
- référence participant pseudonymisée ou nom abrégé ;
- nom du commerce connecté ;
- intitulé `Étape chez votre commerce` ;
- état `À valider` ou `Déjà validée` ;
- bouton principal `Valider cette étape`.

Ne pas afficher l’email, le téléphone, le token, l’identifiant technique ou le QR sous forme textuelle.

#### 5.4 Liste `Mes animations`

La rubrique présente uniquement les animations auxquelles le commerce de la session est effectivement rattaché. Elle ne doit pas exposer les animations simplement publiées dans la commune.

Les vues proposées sont :

- `À venir` : animation publiée dont la période n’a pas commencé ;
- `En cours` : animation publiée et dans sa période active ;
- `Terminées` : animation clôturée ou dont la date de fin est passée.

Chaque ligne affiche le nom, la commune, le type, les dates, le statut, le rôle ou l’étape du commerce et, si disponible, le nombre de validations réalisées chez ce commerce. Une liste vide affiche un état dédié sans masquer la rubrique.

Le détail est en lecture seule et présente la description, les dates, les consignes, l’étape du commerce, les validations agrégées et les contacts utiles. Il n’expose jamais la liste nominative des participants.

#### 5.5 Centre de notifications

Une notification `ANIMATION_COMMERCANT_INCLUS` contient le nom de l’animation, la commune, sa période et un lien profond vers son détail. Elle peut être marquée comme lue et contribue au badge non lu de l’application.

La notification est créée une seule fois pour le couple `(animation_id, commercant_id)`, au moment où l’inclusion devient effective. Une sauvegarde répétée de la configuration ne doit pas la dupliquer. Si le commerçant est retiré puis réintégré, une nouvelle notification n’est produite que si le backend crée une nouvelle occurrence d’inclusion auditée.

Le canal obligatoire est l’inbox persistante de l’application. Une notification WebPush est envoyée si l’appareil est abonné et si la préférence correspondante est active. L’email peut être activé comme canal de repli selon les préférences de notification du commerçant. Aucun message ne doit être envoyé tant que l’animation est encore un brouillon non destinée à être communiquée ; l’envoi intervient à la publication ou lors d’une inclusion dans une animation déjà publiée.

#### 5.6 Inventaire des nouveaux écrans

| ID écran | Intitulé | Route frontend indicative | API principale | Visibilité |
| --- | --- | --- | --- | --- |
| `COM-ANI-ACCUEIL` | Bloc Animation de l’accueil | `/` | `GET /protected/animation-locale/commercants/me/contexte` | Uniquement si `animation_locale_disponible=true` |
| `COM-ANI-LISTE` | Mes animations | `/animations` | `GET /protected/animation-locale/commercants/me/animations` | Uniquement si le module est disponible |
| `COM-ANI-DETAIL` | Détail et suivi d’une animation | `/animations/{animation_id}` | `GET /protected/animation-locale/commercants/me/animations/{animation_id}` | Commerce rattaché uniquement |
| `COM-ANI-INBOX` | Notifications Animation | `/notifications?categorie=animation` | `GET /protected/animation-locale/commercants/me/notifications` | Uniquement si le module est disponible |
| `COM-ANI-INDISPONIBLE` | Animation indisponible | Écran technique sans route permanente | Contexte ou réponse `404` | Lien profond devenu inaccessible |

#### 5.7 Bloc Animation sur l’accueil

Le bloc donne un accès rapide au suivi sans concurrencer l’action principale `Scanner un QR`.

Contenu :

- titre `Mes animations` ;
- compteur des animations en cours ;
- prochaine animation à venir, si elle existe ;
- compteur de notifications non lues ;
- action `Voir mes animations` ;
- action secondaire `Voir les notifications` uniquement en présence d’au moins une notification.

```text
┌──────────────────────────────────────┐
│ Mes animations                  (2)  │
│ 1 animation en cours                 │
│ Prochaine : Passeport gourmand       │
│ Du 25 août au 15 septembre           │
│                                      │
│ [Voir mes animations]  1 nouveauté   │
└──────────────────────────────────────┘
```

Le bloc n’est pas rendu tant que le contexte n’est pas chargé. Il ne doit pas apparaître brièvement puis disparaître dans une commune non équipée. Pendant le chargement initial, utiliser un squelette neutre de l’accueil, sans libellé Animation.

#### 5.8 Écran `Mes animations`

##### 5.8.1 En-tête et filtres

L’en-tête contient :

- bouton retour ou navigation principale ;
- titre `Mes animations` ;
- texte d’aide `Les animations auxquelles votre commerce participe` ;
- badge de notifications non lues ;
- onglets `En cours`, `À venir`, `Terminées` avec compteurs lorsqu’ils sont connus.

La catégorie d’affichage est dérivée des dates et du statut retournés :

| Catégorie UI | Règle |
| --- | --- |
| `À venir` | Statut publié et `date_debut` postérieure à maintenant |
| `En cours` | Statut `PUBLIEE` ou `EN_COURS` et instant courant compris entre les dates |
| `Terminées` | Statut `CLOTUREE`, `ARCHIVEE` ou `ANNULEE`, ou date de fin passée |

Les onglets sont des filtres de présentation. Ils ne modifient jamais l’appartenance du commerce à l’animation.

##### 5.8.2 Carte d’animation

Chaque carte affiche :

- visuel ou pictogramme du type d’animation ;
- nom de l’animation ;
- commune ;
- période au format local ;
- badge de statut utilisateur ;
- intitulé de l’étape du commerce ;
- nombre de validations effectuées chez ce commerce ;
- action `Voir le détail`.

```text
┌──────────────────────────────────────┐
│ [visuel] Passeport gourmand          │
│ Annecy · En cours                    │
│ 25 août — 15 septembre               │
│ Étape chez votre commerce            │
│ 18 validations réalisées             │
│                         [Voir détail] │
└──────────────────────────────────────┘
```

La carte entière peut être interactive, mais l’action doit conserver un libellé accessible. Aucun nom, email, téléphone ou identifiant de participant n’apparaît dans la liste.

##### 5.8.3 États de la liste

| État | Présentation | Action |
| --- | --- | --- |
| Chargement initial | 3 squelettes de cartes | Aucune |
| Rafraîchissement | Contenu conservé avec indicateur discret | Aucune |
| Liste vide globale | `Votre commerce ne participe encore à aucune animation` | Retour accueil |
| Onglet vide | `Aucune animation dans cette catégorie` | Changer d’onglet |
| Erreur récupérable | Message court et `Réessayer` | Relancer la même requête |
| Session expirée | Parcours de reconnexion existant | Reprendre la route demandée |
| Module désactivé entre deux requêtes | Purger les données locales et quitter la rubrique | Retour accueil |

La pagination se déclenche par bouton `Afficher plus` ou chargement progressif accessible. Le changement d’onglet replace le focus sur le titre de la liste et revient en première page.

#### 5.9 Écran de détail et suivi d’une animation

L’écran est strictement en lecture seule. Il aide le commerçant à comprendre l’animation et à suivre son activité, sans lui donner accès au pilotage partenaire.

##### 5.9.1 En-tête

- bouton retour vers `Mes animations` ;
- nom de l’animation ;
- badge `À venir`, `En cours`, `Terminée` ou `Annulée` ;
- commune et période ;
- type d’animation.

##### 5.9.2 Sections

| Section | Contenu |
| --- | --- |
| Présentation | Description publique de l’animation |
| Votre participation | Nom de l’étape, rôle du commerce et consignes opérationnelles |
| Suivi chez votre commerce | Nombre total de validations réalisées, dernière activité si disponible |
| Période | Dates de début et de fin, avec état temporel explicite |
| Besoin d’aide | Contact ou accès au support Localeo existant |

```text
┌──────────────────────────────────────┐
│ ← Mes animations                     │
│ Passeport gourmand       [En cours]  │
│ Annecy · 25 août — 15 septembre      │
├──────────────────────────────────────┤
│ Présentation                         │
│ Découvrez les commerces locaux…      │
├──────────────────────────────────────┤
│ Votre participation                  │
│ Étape chez votre commerce            │
│ Scannez le QR présenté par le client │
├──────────────────────────────────────┤
│ Suivi chez votre commerce            │
│ 18 validations réalisées             │
├──────────────────────────────────────┤
│ [Scanner un QR]        [Aide]         │
└──────────────────────────────────────┘
```

Le bouton `Scanner un QR` est visible uniquement pendant une période permettant les validations. Il ouvre le scanner commun et ne préremplit jamais un participant. Pour une animation à venir, terminée ou annulée, le bouton est remplacé par une information expliquant pourquoi aucune validation n’est possible.

Une réponse `404` signifie que l’animation n’est plus accessible au commerce, qu’elle appartient à une autre commune ou que le module a été désactivé. L’application supprime alors la fiche de son cache et affiche `Cette animation n’est plus disponible pour votre commerce`.

#### 5.10 Écran des notifications Animation

L’application peut réutiliser le centre de notifications existant en ajoutant une catégorie `Animations`. Il ne faut pas créer deux inbox concurrentes.

Chaque entrée affiche :

- état lu/non lu ;
- icône Animation ;
- titre ;
- message ;
- date relative, complétée par une date absolue accessible ;
- action implicite vers l’animation.

```text
┌──────────────────────────────────────┐
│ Notifications · Animations           │
├──────────────────────────────────────┤
│ ● Vous participez à une animation    │
│   Votre commerce est inclus dans     │
│   Passeport gourmand · il y a 2 h    │
├──────────────────────────────────────┤
│   Vous participez à une animation    │
│   Marché de Noël · 12 janvier        │
└──────────────────────────────────────┘
```

À l’ouverture d’une entrée, l’application marque la notification comme lue puis ouvre son `action_cible`. Si le marquage échoue mais que le détail reste autorisé, la navigation continue et le badge sera réconcilié au prochain chargement. Un lien profond WebPush suit le même parcours après restauration ou vérification de la session.

#### 5.11 Écran `Animation indisponible`

Cet écran transitoire est réservé aux liens profonds, favoris ou notifications devenus invalides. Il ne constitue pas une rubrique visible.

Contenu :

- pictogramme informatif ;
- titre `Animation indisponible` ;
- message `Localeo Animation n’est pas disponible pour votre commerce dans cette commune` ou `Cette animation n’est plus accessible` selon le contexte connu ;
- action principale `Retour à l’accueil` ;
- aucune action commerciale ou proposition d’abonnement au commerçant.

L’écran ne révèle ni l’existence d’une animation d’un autre commerce, ni le nom d’un partenaire, ni la cause administrative de la désactivation.

#### 5.12 Navigation et rafraîchissement

```text
Accueil
  └─ Mes animations
       ├─ Liste filtrée
       │    └─ Détail animation
       │          └─ Scanner un QR
       └─ Notifications Animation
             └─ Détail animation
```

- le contexte est chargé après authentification et après toute modification du commerce ou de la commune active ;
- la liste est rafraîchie à l’ouverture, au retour au premier plan et après une validation réussie ;
- le détail peut être rafraîchi par geste ou action explicite ;
- le compteur de notifications est réconcilié après lecture et au retour au premier plan ;
- tout passage de `animation_locale_disponible=true` à `false` purge immédiatement listes, détails et notifications Animation du cache local.

#### 5.13 Responsive et accessibilité des écrans de suivi

- une colonne sur mobile ; deux colonnes maximum pour les cartes sur tablette ou écran large ;
- largeur de lecture du détail limitée pour conserver des lignes lisibles ;
- zones interactives d’au moins 44 × 44 px ;
- ordre de focus : retour, titre, statut, contenu, actions ;
- badges toujours accompagnés d’un libellé textuel ;
- compteurs annoncés avec leur sens, par exemple `18 validations réalisées` ;
- squelettes ignorés par les lecteurs d’écran et chargement annoncé une seule fois ;
- aucune actualisation ne déplace automatiquement le focus ;
- dates rendues dans le fuseau local de la commune et accompagnées de l’année lorsque nécessaire.

### 6. Reconnaissance des QR

#### 6.1 QR participant Animation

Le QR contient une URL publique issue de `ANIMATION_PUBLIC_BASE_URL` :

```text
{ANIMATION_PUBLIC_BASE_URL}/participants/{participant_token}
```

L’application accepte uniquement une origine Localeo autorisée et le chemin `/participants/{token}`. Elle extrait le token en mémoire pour les appels API, sans le persister dans les logs, analytics, crash reports ou historique de navigation.

#### 6.2 QR coffret

Le format signé historique reste pris en charge par le parcours coffret existant. L’application ne tente pas de décoder ou de vérifier sa signature localement ; elle transmet la valeur au backend Coffret.

#### 6.3 Algorithme de routage

```text
si valeur = URL HTTPS d’une origine Localeo autorisée
   et chemin = /participants/{token}
      alors type = ANIMATION
sinon
      type = COFFRET_LEGACY
```

Toute URL absolue d’une origine non autorisée est rejetée localement comme QR non reconnu. Aucun fallback Coffret ne doit transmettre une URL externe au backend.

### 7. Authentification

L’application réutilise l’authentification et la session commerçant existantes. La connexion crée la session :

```http
POST /protected/identite-acces/commercants/auth/login
```

Les appels de résolution et de validation suivants utilisent ensuite :

```http
Authorization: Bearer <session_token>
```

La session doit contenir le scope `commercant:validation`. Les réponses `401` provoquent le renouvellement ou la reconnexion. Les réponses `403` affichent un écran d’accès insuffisant et ne doivent pas déclencher de boucle de retry.

### 8. Contrats API

#### 8.0 Contexte fonctionnel du commerce

Contrat à exposer ou à intégrer au payload de session existant :

```http
GET /protected/animation-locale/commercants/me/contexte
Authorization: Bearer <session_token>
```

```json
{
  "commercant_id": "uuid",
  "commune_id": "uuid",
  "animation_locale_disponible": true,
  "permissions": ["animation:lire", "animation:valider"],
  "notifications_non_lues": 1
}
```

La réponse est recalculée côté serveur depuis la commune active, l’abonnement ou l’activation du module et les habilitations du commerce. Une commune inexistante dans la session ou un module non activé retourne `animation_locale_disponible=false`, sans révéler les données d’une autre commune.

#### 8.1 Parcours coffret existant

| Étape | API |
| --- | --- |
| Ouvrir la transaction | `POST /protected/exploitation/validation/ouvrir-transaction` |
| Valider la prestation sélectionnée | `POST /protected/exploitation/validation/valider-prestation` |

Ce parcours reste inchangé et constitue un test de non-régression obligatoire.

#### 8.2 Résoudre le QR participant — contrat immédiatement utilisable

```http
GET /public/animation-locale/participants/{participant_token}
```

La réponse fournit l’animation, le participant masqué et les étapes. L’application sélectionne l’étape dont `commercant_id` correspond au commerce de la session.

Si aucune étape ne correspond, l’application ne propose pas la validation. Le backend effectuera de nouveau ce contrôle lors de la commande.

#### 8.3 Valider une étape Animation

```http
POST /protected/animation-locale/validations
Authorization: Bearer <session_token>
Idempotency-Key: <uuid-ou-ulid-stable-pour-la-tentative>
Content-Type: application/json

{
  "qr_token": "token-opaque-extrait-du-qr",
  "etape_id": "uuid-etape-retourne-par-la-resolution"
}
```

Réponse nominale actuelle :

```json
{
  "id": "uuid-validation",
  "animation_id": "uuid-animation",
  "participant_id": "uuid-participant",
  "commercant_id": "uuid-commercant",
  "etape_id": "uuid-etape",
  "statut": "VALIDEE",
  "validated_at": "2026-08-20T10:30:00Z",
  "annulation_motif": null
}
```

La même `Idempotency-Key` doit être réutilisée pour tous les retries techniques d’une tentative. Un nouveau scan confirmé crée une nouvelle clé.

### 9. Évolutions backend recommandées pour l’application

Ces évolutions ne bloquent pas une première intégration, mais évitent au frontend de composer un contrat public et améliorent fortement le retour utilisateur.

#### 9.1 Résolution protégée du scan

Contrat recommandé :

```http
POST /protected/animation-locale/scans/resoudre
Authorization: Bearer <session_token>

{
  "valeur_qr": "https://.../participants/token"
}
```

Réponse cible :

```json
{
  "type": "ANIMATION_PARTICIPANT",
  "animation": {"id": "uuid", "nom": "Passeport gourmand", "commune": "Annecy"},
  "participant": {"reference": "PART-0247", "nom_affiche": "Alice D."},
  "etape": {"id": "uuid", "statut": "A_VALIDER"},
  "action_autorisee": true,
  "raison_blocage": null
}
```

Le backend dérive le commerçant depuis la session et ne retourne que les données utiles à la confirmation.

#### 9.2 Réponse de validation enrichie

Ajouter de manière compatible :

```json
{
  "progression": 60,
  "nombre_validations": 3,
  "nombre_validations_requises": 5,
  "participant_qualifie": false,
  "idempotent_replay": false,
  "deja_validee": false
}
```

À terme, `etape_id` pourra devenir optionnel : le backend peut le dériver du couple animation/commerçant après résolution du token.

#### 9.3 Animations du commerce

```http
GET /protected/animation-locale/commercants/me/animations?statut=EN_COURS&page=1&page_size=20
GET /protected/animation-locale/commercants/me/animations/{animation_id}
```

Le commerçant est toujours dérivé de la session. La liste est filtrée par la commune active et par l’existence d’un rattachement effectif dans `animation_commercants`. Le détail retourne `404` si le commerce n’est pas rattaché à l’animation et `403` si la commune demandée sort du tenant actif.

Le payload de liste fournit au minimum `id`, `nom`, `description_courte`, `type`, `commune`, `date_debut`, `date_fin`, `statut`, `etape_commercant`, `nombre_validations` et `detail_url`.

#### 9.4 Notifications du commerce

```http
GET  /protected/animation-locale/commercants/me/notifications?lue=false
POST /protected/animation-locale/commercants/me/notifications/{notification_id}/lire
```

La publication d’une animation crée les notifications pour les commerces déjà inclus. L’ajout ultérieur d’un commerce à une animation publiée crée immédiatement la sienne. La création s’appuie sur une clé d’idempotence métier stable et sur l’outbox existante afin d’éviter pertes et doublons entre inbox, WebPush et email.

Événement interne attendu :

```json
{
  "type": "ANIMATION_COMMERCANT_INCLUS",
  "animation_id": "uuid",
  "commercant_id": "uuid",
  "commune_id": "uuid",
  "inclusion_id": "uuid",
  "occurred_at": "2026-08-20T10:30:00Z"
}
```

### 10. Règles métier et UX

| Situation | Comportement attendu |
| --- | --- |
| Étape valide | Afficher le succès et la progression disponible. |
| Même étape déjà validée | Ne pas présenter une erreur rouge ; afficher `Étape déjà validée`. |
| QR participant expiré ou révoqué | Demander au participant de faire renvoyer son QR. |
| Animation non publiée, clôturée ou hors période | Expliquer que l’animation n’accepte plus de validation. |
| Commerce absent de l’animation | Indiquer que cette étape ne concerne pas ce commerce. |
| Module Animation non déployé dans la commune | Masquer la rubrique et refuser tout accès direct aux données Animation. |
| Module déployé mais aucune animation rattachée | Afficher l’état vide `Aucune animation pour votre commerce`. |
| Commerce inclus dans une animation publiée | Créer une seule notification et ouvrir le détail depuis son lien profond. |
| Cadence de scan anormale | Afficher `Validation en cours de contrôle` si le statut retourné est `ANOMALIE`. |
| Session expirée | Conserver l’intention en mémoire, reconnecter, puis demander une nouvelle confirmation. |
| Réseau indisponible | Ne pas valider hors ligne ; proposer de réessayer avec la même clé d’idempotence. |

### 11. Mapping des erreurs

| HTTP | Message utilisateur | Retry |
| ---: | --- | --- |
| `400` / `422` | QR ou demande non reconnu | Non, nouveau scan |
| `401` | Votre session a expiré | Après reconnexion |
| `403` | Vous n’êtes pas autorisé à valider cette étape | Non |
| `404` | Participation introuvable | Non |
| `409` | Validation impossible dans l’état actuel de l’animation | Selon le détail métier |
| `410` | Ce QR n’est plus valide | Non, renvoi du QR |
| `429` | Trop de scans rapprochés, patientez un instant | Oui, temporisé |
| `5xx` | Service momentanément indisponible | Oui, même clé d’idempotence |

L’application affiche le `correlationId` dans la zone de détail/support, jamais le token QR.

### 12. Sécurité et confidentialité

- liste blanche stricte des origines QR Localeo ;
- aucune navigation automatique vers l’URL scannée ;
- aucun token dans les logs, analytics, breadcrumbs, notifications ou stockage permanent ;
- token conservé en mémoire uniquement pendant le parcours ;
- HTTPS obligatoire hors développement ;
- validation finale exclusivement côté backend ;
- aucun `commercant_id`, `participant_id` ou statut calculé par le client ne fait autorité ;
- nettoyage de l’écran et du token à la fermeture, au logout et au passage prolongé en arrière-plan ;
- masquage des données participant dans les captures de diagnostic.

### 13. Résilience et concurrence

- une tentative possède une seule `Idempotency-Key` ;
- double tap : bouton désactivé dès le premier envoi ;
- timeout : proposer `Réessayer`, sans générer une nouvelle clé ;
- retour arrière avant succès : demander confirmation avant abandon ;
- reprise après fermeture de l’application : nouveau scan obligatoire ;
- aucune file de validations hors ligne, car le statut de l’animation et l’éligibilité doivent être vérifiés en temps réel.

### 14. Observabilité

Événements autorisés, sans PII ni secret :

- `merchant_scan_started` ;
- `merchant_scan_type_detected` avec `type=COFFRET|ANIMATION|UNKNOWN` ;
- `merchant_animation_scan_resolved` ;
- `merchant_animation_validation_confirmed` ;
- `merchant_animation_validation_succeeded` ;
- `merchant_animation_validation_replayed` ;
- `merchant_animation_validation_failed` avec code HTTP/code métier ;
- `merchant_animation_list_viewed` ;
- `merchant_animation_detail_viewed` ;
- `merchant_animation_inclusion_notification_opened` ;
- `merchant_animation_feature_hidden` avec motif non sensible ;
- `merchant_scan_abandoned`.

Mesurer taux de résolution, taux de succès, délais, erreurs par version d’application et part de QR inconnus. Ne jamais envoyer la valeur scannée.

### 15. Accessibilité et compatibilité

- bouton de validation d’au moins 44 px ;
- contraste WCAG AA ;
- retour texte et visuel, pas uniquement couleur ou vibration ;
- lecteur d’écran annonçant le type de QR et le résultat ;
- permission caméra explicable et récupérable depuis les réglages ;
- prise en charge des appareils actuellement supportés par l’application commerçant ;
- affichage portrait prioritaire, mais confirmation utilisable en paysage.

### 16. Déploiement

1. livrer derrière un feature flag `animation_validation_enabled` ;
2. publier le backend avant l’application ;
3. activer sur un groupe pilote de commerces participants ;
4. vérifier télémétrie, erreurs et non-régression Coffret ;
5. généraliser progressivement.

L’application n’étant pas encore déployée, la première version publiée embarque directement les parcours Coffret et Animation. Aucun fallback ni contrôle de version minimale n’est requis.

### 17. Découpage proposé

| Lot | Contenu | Dépendances | Critère de sortie |
| --- | --- | --- | --- |
| `COM-0` | Feature flag de recette et télémétrie sans token | Configuration | Fonction masquée et mesurable |
| `COM-1` | Scanner unique et routage QR Coffret/Animation | `ARB-47` | Aucun impact sur les coffrets |
| `COM-2` | Résolution et écran de confirmation Animation | API participant actuelle ou résolution protégée | Étape du commerce affichée |
| `COM-3` | Validation, idempotence, succès, doublon et erreurs | `POST /validations` | Parcours E2E nominal et retries |
| `COM-4` | Accessibilité, pilote, support et déploiement progressif | Backend publié et commerce pilote | Recette terrain validée |
| `COM-5` | Capacité Animation par commune et navigation conditionnelle | Activation/abonnement commune | Rubrique absente si le module n’est pas déployé |
| `COM-6` | Liste et détail en lecture seule des animations du commerce | APIs `/commercants/me/animations` | À venir, en cours et terminées couvertes |
| `COM-7` | Notification d’inclusion, inbox, badge et lien profond | Outbox et préférences de notification | Une inclusion produit une notification unique |

### 18. Critères d’acceptation

- [ ] Le scanner reconnaît un QR participant Animation sans casser un QR coffret.
- [ ] Une origine externe n’est jamais ouverte ni transmise au backend.
- [ ] Le commerce et l’étape sont dérivés et contrôlés depuis la session/backend.
- [ ] Une validation nominale n’est créée qu’une fois.
- [ ] Un retry réseau réutilise la même clé d’idempotence.
- [ ] Une étape déjà validée produit un état informatif, pas un faux échec.
- [ ] Une animation clôturée, hors période ou étrangère au commerce est refusée proprement.
- [ ] Aucun token ou PII n’apparaît dans les logs et analytics.
- [ ] Le parcours Coffret passe intégralement ses tests de non-régression.
- [ ] Les tests caméra, faible réseau, double tap, session expirée et reprise sont couverts.
- [ ] La rubrique Animation est invisible si le module n’est pas activé pour la commune active.
- [ ] Une commune équipée sans animation affiche un état vide, et non une rubrique masquée.
- [ ] Seules les animations auxquelles le commerce est rattaché sont listées et consultables.
- [ ] Le changement de commune active recalcule la disponibilité et vide les données Animation précédentes.
- [ ] Une inclusion dans une animation publiée crée exactement une notification persistante.
- [ ] Une inclusion préparée dans un brouillon est notifiée au moment de la publication, sans doublon.
- [ ] Le lien profond de la notification ouvre le détail autorisé de l’animation.
- [ ] Les préférences WebPush/email sont respectées sans empêcher la création de l’inbox.

### 19. Matrice de tests minimale

| Cas | Attendu |
| --- | --- |
| QR coffret valide | Parcours coffret historique |
| QR participant valide et étape ouverte | Confirmation puis succès Animation |
| QR participant déjà validé | État `Déjà validée`, aucun doublon |
| QR d’un autre commerce | Refus métier |
| QR expiré/révoqué | Message de renvoi du QR |
| Animation avant début/après fin/clôturée | Refus métier explicite |
| Double validation simultanée | Une seule validation effective |
| Timeout après envoi | Retry idempotent |
| QR URL externe | Rejet local |
| Session sans scope | `403`, aucune commande |
| Mode avion | Aucun stockage de validation, retry manuel |
| Commune sans Localeo Animation | Aucun élément de navigation Animation et aucun chargement API métier |
| Commune équipée, liste vide | Rubrique visible avec état vide |
| Animation publiée sans rattachement du commerce | Absente de la liste et détail inaccessible |
| Inclusion avant publication | Une notification émise à la publication |
| Inclusion après publication | Une notification émise immédiatement |
| Sauvegarde répétée de la même inclusion | Aucune notification supplémentaire |
| Changement vers une commune non équipée | Cache Animation purgé et rubrique masquée |

### 20. Définition de terminé

L’évolution est terminée lorsque les lots `COM-0` à `COM-7` sont validés, que la recette bout en bout couvre au moins un commerce pilote, une animation publiée, une commune équipée et une commune non équipée, que la notification d’inclusion est idempotente, que les journaux ont été contrôlés pour l’absence de token/PII et que le parcours Coffret ne présente aucune régression.

### Correctif PRO-002 — résultat de validation
Seul le statut backend VALIDEE confirme une étape. ANOMALIE nécessite un contrôle ; un HTTP 409 reste un refus, jamais un rejeu implicite. Le frontend conserve la date serveur disponible. Validation : 21 tests unitaires ciblés et un scénario navigateur de conflit réussis.


#### PRO-006 — Pagination complète Animation
Les listes animations, invitations et notifications parcourent les pages annoncées par `pagination.total`. Une page manquante, répétée ou invalide produit une erreur visible ; aucune liste partielle n'est mise en cache comme complète. Limite de protection : 500 pages, avec erreur explicite. Le signal d'annulation et l'époque de session restent appliqués. Contrat serveur vérifié dans `animation_locale_api.py` : `items` et `pagination` (page, page_size, total). Validation : 24 tests réussis (pagination, cache, pages Animation).


#### PRO-007 — Respecter les interdictions et échéances serveur
Les interdictions explicites et `echeance_depassee=true` ne sont jamais annulées localement. Une liste d'actions vide interdit toute action. Une date civile YYYY-MM-DD s'affiche jusqu'en fin de journée locale ; un timestamp, même à minuit, garde son instant exact. Le backend décide lors de la commande. Validation : 32 tests réussis (contrats et pages Animation), dont échéance serveur, interdiction avant échéance et timestamp à minuit.

#### PRO-005 — Retirer les QR des URLs techniques
Coffrets : POST JSON sur le contrat backend existant. Animation : nouvel endpoint authentifié `/protected/animation-locale/commercants/me/participants/resoudre`, corps `qr_token`, projection minimale limitée au commerce. Aucun fallback vers l'URL publique. Jetons de mot de passe retirés par remplacement d'historique, conservés uniquement en mémoire. Origine Marketplace de recette retirée de la production et remplacée par l'origine de production documentée. Déployer le backend avant le frontend. Tests : 6 backend ciblés réussis, build réussi, 3 E2E réussis après un premier timeout de démarrage Vite. Le runner peut utiliser `LOCALEO_E2E_EXTERNAL_SERVER=1` pour un serveur contrôlé séparément sur Windows. Le lien public bénéficiaire demeure côté backend ; la rétention des anciennes URLs dans les proxys reste un contrôle d'exploitation.

#### PRO-008 — Clé stable pour décision incertaine
Verrou synchrone dès confirmation et clé conservée en mémoire pour une même décision et un même motif après erreur réseau. Les réponses d'enrichissement antérieures ne peuvent plus remplacer la décision. Un conflit recharge la demande autoritaire et exige un nouveau choix ; aucune commande n'est rejouée automatiquement. Les changements de demande/session invalident les réponses en cours. Validation : 18 tests réussis, dont double clic, réponse perdue avec clé identique, enrichissement tardif et conflit suivi de relecture.

## Références complémentaires des interfaces

- Animation : [Architecture applicative EPIC 41 - Domaine animation locale](../../architecture/backend/epics/epic-41-animation-locale-architecture.animation.md)
- Animation : [Analyse API de la maquette V2](../../specifications/epic-41-api/analyse-api-maquette.md)
- Animation : [Specifications techniques API EPIC 41](../../specifications/epic-41-api/README.md)
- Animation : [registre des arbitrages API](../../specifications/epic-41-api/registre-arbitrages.md)
- Animation : [Indicateurs economiques et d'usage des gains](../../specifications/epic-41-api/indicateurs-economiques.md)
