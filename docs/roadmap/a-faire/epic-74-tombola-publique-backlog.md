# EPIC 74 — Tombola publique sans commerçant

## Références et état

- **État produit : À faire**, cadrage initial du **22 octobre 2026**.
- Besoin : proposer dans le forfait standard une tombola accessible par QR public,
  utilisable notamment sur un stand de marché, sans commerçant nécessaire ;
  constituer un public susceptible de participer à de futures animations.
- Identifiant `74` vérifié dans la roadmap commune et les namespaces applicatifs.
  Base documentaire lue : `localeo-projet` `6d25510`, avec travaux locaux conservés.
- [Roadmap commune](../README.md), [cycle d'epic](../../organisation/cycle-epic.md).
- Epic proche : [E53 — Tombola locale](../terminees/epic-53-tombola-locale-backlog.md),
  **terminée**, conditionne la qualification à un achat confirmé par un commerce.
  E74 ajoute une mécanique autonome ; elle ne remplace pas E53 et ne rouvre pas
  sa clôture historique.
- Socles à réutiliser : [E41 — Animation](../../specifications/epic-41-api/README.md),
  [E42 — Live](../../specifications/epic-42-localeo-live/README.md),
  [E73 — Produits, dotations et SaaS](../../specifications/epic-73-animation-et-ou-coffrets/README.md).
  Pas de deuxième moteur de tirage ni de référentiel de participants parallèle.
- Aucun dossier de spécification détaillée ni code nouveau à ce stade.

## Problème et résultat attendu

La tombola locale existante ne répond pas au besoin d'un organisateur qui tient
un stand et souhaite faire participer les visiteurs sans achat ni validation
par un commerçant. Sa règle actuelle est vérifiée dans la
[spécification E53](../../specifications/epic-53-tombola-locale/README.md).

**Exemple cible :** la commune prépare une tombola publique, choisit ses dates et
ses lots puis publie une affiche comportant un QR. Sur le marché, un visiteur le
scanne, suit le parcours de participation et obtient une confirmation claire.
L'organisateur suit les participations, clôture et tire les gagnants avec le
socle existant. Aucun commerce fictif, achat, scan Pro ou PIN commerçant n'est
nécessaire pour qualifier le visiteur.

Acteurs : organisateur et collaborateurs habilités, visiteur/participant,
gagnant, opérateur Localeo pour la supervision. La constitution d'une audience
pour des événements futurs est distincte de l'inscription à ce jeu : une
participation ne vaut pas, à elle seule, autorisation de communication future.

## Décisions acquises et propositions

| Référence | Nature | Contenu |
| --- | --- | --- |
| E74-DEC-01 | Demande acquise | Ajouter une « Tombola publique » au forfait standard, sans achat d'un module supplémentaire pour accéder à ce type d'animation |
| E74-DEC-02 | Demande acquise | Aucun commerçant requis pour créer, publier et participer ; qualification depuis le parcours ouvert par le QR public |
| E74-DEC-03 | Demande acquise | QR utilisable sur un support physique, notamment un stand sur un marché |
| E74-DEC-04 | Objectif acquis, modalités ouvertes | Développer le public des prochaines animations ; modalités de recueil et de réutilisation des préférences à arbitrer |
| E74-PROP-01 | Proposition | Une participation et une chance par identité retenue et par tombola ; rescans sans chance supplémentaire |
| E74-PROP-02 | Proposition | Consommer le quota standard d'animations du forfait à la publication, avec les mêmes règles que les autres types standard ; pas de quota illimité implicite |
| E74-PROP-03 | Proposition | Après scan : formulaire court ou réutilisation du compte existant, puis confirmation explicite ; aucun mot de passe supplémentaire pour un compte déjà reconnu |
| E74-PROP-04 | Proposition | Communications futures facultatives, choix non précoché et révocable ; refus sans perte de chance ni exclusion du jeu |

Les propositions ne sont pas des arbitrages validés. Les trois premières
questions interactives portent sur le parcours après scan, la présence sur place
et le recueil facultatif des préférences de communication.

## Périmètre

### Inclus

- Nouveau type d'animation clairement distinct de « Tombola locale des
  commerçants » dans le catalogue standard. Code technique candidat
  `TOMBOLA_PUBLIQUE`, à confirmer lors de la spécification.
- Assistant de création adapté : nom, commune, organisateur, dates, présentation,
  dotation et règlement ; aucune étape obligatoire de sélection, mission,
  invitation, acceptation ou onboarding de commerçants.
- Page publique mobile, QR d'accès et lien équivalent ; support téléchargeable
  affichable sur le stand. Flyers contextualisés : ne pas afficher « 0 commerçant
  participant » comme une anomalie ni demander un passage en commerce.
- Participation, identification minimale, dédoublonnage, confirmation, reprise
  d'une requête incertaine et fermeture des inscriptions aux dates prévues.
- Clôture, population éligible figée, tirage, suppléants, information des gagnants
  et suivi des lots via les mécanismes existants, adaptés au nouveau modèle.
- Préparation de l'audience future avec préférences distinctes et traçables,
  selon l'arbitrage de communication ; visibilité des résultats par organisation
  et commune, sans réinscription automatique aux futurs jeux.
- Statistiques pertinentes : inscriptions confirmées, participations éligibles,
  source de diffusion si connue, gagnants et lots remis ; ne pas inventer des
  passages ou achats chez des commerçants.

### Dotation : indépendance à préserver

Une tombola à **lots libres gérés en externe** doit pouvoir fonctionner de bout
en bout sans aucun commerce : l'organisateur assure la remise. La compatibilité
avec Coffrets et bons numériques E73 est à préciser (ARB-04). Un commerce chargé
de remettre un bon, s'il est utilisé, ne devient pas une étape de qualification
du participant. Les exigences existantes de remise d'un bon numérique ne sont
pas supprimées silencieusement pour rendre cette variante autonome.

### Hors périmètre proposé

- Billets payants, achat obligatoire, chances proportionnelles à une dépense,
  gains instantanés ou second moteur de tirage.
- Modification de la qualification de la tombola commerçante, du passeport ou
  de la chasse au trésor ; migration automatique des anciennes animations.
- Nouveau CRM de prospection B2B : E71 concerne organisations et contacts
  commerciaux, pas la création implicite de prospects à partir des joueurs.
- Nouvelle plateforme d'envoi marketing. Le recueil de préférences ne donne
  pas de droits gratuits au module Communication E73 et n'étend pas implicitement
  ses campagnes, limitées aux participants d'une animation et à leur fenêtre
  d'envoi. Le canal des futures invitations reste un arbitrage explicite.
- Scan hors connexion, géolocalisation obligatoire, application native ou
  contrôle physique de présence, sauf décision spécifique ARB-02.

## User stories proposées

| ID | Acteur et besoin | Critères |
| --- | --- | --- |
| E74-US-01 | Organisateur : choisir la tombola publique parmi les animations standard | 01, 02 |
| E74-US-02 | Organisateur : configurer et publier sans commerçant, avec un parcours adapté | 03, 04 |
| E74-US-03 | Organisateur : télécharger le QR et un support compréhensible pour un stand | 05, 06 |
| E74-US-04 | Visiteur : participer depuis son téléphone et savoir que sa participation est enregistrée | 07, 08, 09 |
| E74-US-05 | Participant : choisir séparément s'il souhaite être informé des prochaines animations | 10, 11 |
| E74-US-06 | Gestionnaire : suivre et clôturer la tombola puis tirer les gagnants | 12, 13 |
| E74-US-07 | Gagnant et organisateur : recevoir le résultat et suivre la remise du lot | 14 |
| E74-US-08 | Localeo : superviser, mesurer et exploiter le nouveau modèle sans régression | 15, 16 |

## Critères d'acceptation cibles

Les critères dépendant d'un arbitrage sont explicitement conditionnés ; ils ne
constituent pas une preuve d'implémentation ou d'approbation des propositions.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E74-CA-01 | Organisateur habilité, forfait standard actif | Consulter le catalogue et choisir une tombola | « Tombola publique » est identifiable et incluse ; aucune souscription de module spécifique exigée |
| E74-CA-02 | Quota et droits du forfait connus | Publier/rejouer la publication | Règle commerciale choisie en ARB-05 appliquée une seule fois ; aucune double consommation ni accès sans droit |
| E74-CA-03 | Organisation sans aucun commerce rattaché, dotation externe prête | Créer puis publier la tombola | Aucun commerce, mission, invitation, minimum de commerces ou paiement Coffrets imposé à cette configuration ; dates/règlement/dotation requis restent contrôlés |
| E74-CA-04 | Gestionnaire autorisé dans sa commune | Parcourir l'assistant et le suivi | Étapes commerçants absentes ou explicitement non applicables ; une action directe ne contourne pas les droits d'organisation/commune |
| E74-CA-05 | Tombola publiée | Télécharger le support puis scanner le QR ou ouvrir le lien | Ouverture de la bonne animation ; QR sans identité personnelle ni secret d'administration ; lien lisible proposé en alternative |
| E74-CA-06 | Flyer d'une tombola publique avec dotation connue | Lire le document | Promesse et nombre d'exemplaires cohérents ; aucune instruction d'achat/scan chez un commerçant ni compteur commerçants inadapté ; image personnalisée compatible avec le socle flyer |
| E74-CA-07 | Visiteur pendant la période autorisée | Suivre le parcours ARB-01 et confirmer selon sa règle | Participation enregistrée et éligibilité explicite sans validation Pro/PIN ; état « à confirmer » distinct si une vérification d'identité reste nécessaire |
| E74-CA-08 | Même identité selon ARB-03, double clic/rescan/réponse perdue | Répéter ou reprendre la participation | Même participation retrouvée, pas de chances ajoutées au rejeu selon la règle retenue ; une erreur réseau n'est pas annoncée comme succès |
| E74-CA-09 | Avant ouverture, après clôture, animation annulée ou règle de présence non satisfaite | Tenter de participer | Refus compréhensible sans inscription qualifiée ; contrôle serveur des dates et de la présence si cette option est retenue |
| E74-CA-10 | Visiteur qui refuse les communications futures | Participer | Accès au jeu et chances inchangés ; aucune préférence positive implicite tirée du scan ou de l'acceptation du règlement |
| E74-CA-11 | Option de communications futures retenue en ARB-06 | Accepter puis retirer cette préférence | Portée, canal, information présentée et date tracés ; retrait effectif pour les sollicitations futures, sans suppression arbitraire des faits de participation ; si l'option est différée, aucun envoi futur lancé par cette epic |
| E74-CA-12 | Gestionnaire, liste de participants et bilan | Consulter, filtrer et clôturer | Listes paginées côté serveur, totaux exacts, pas de faux passages commerçants ; population éligible figée selon le socle de clôture |
| E74-CA-13 | Tombola clôturée, tirage autorisé | Tirer, rejouer ou tirer avec zéro/peu de candidats | Résultat cohérent avec la population figée ; aucun double tirage/gain involontaire ; règles de suppléants et cas sans candidat explicites |
| E74-CA-14 | Tirage confirmé et dotation compatible | Notifier puis remettre un lot | Parcours de remise E73 conservé, état d'envoi distinct de remise ; la gestion externe reste réalisable sans commerce |
| E74-CA-15 | Utilisateur non habilité ou trafic automatisé | Appeler les routes publiques/protégées | Pas d'accès aux participants d'autrui ; protections contre abus, erreurs sans données privées, audit exploitable et performances bornées |
| E74-CA-16 | Autres modèles et données existantes | Rejouer leurs parcours et les fixtures de démonstration | Qualification commerçante inchangée ; modèle public testé isolément, aucune activation ni conversion automatique d'animations existantes |

## Impacts à instruire

| Sujet | Impact initial et sources |
| --- | --- |
| Domaine backend | **Concerné** : stratégie de qualification du nouveau modèle, validation de publication sans commerce, règles de quota, population figée et audit. Le domaine décide ; API/portail ne simulent pas une validation commerçante |
| Localeo Animation | **Concerné** : catalogue, assistant, QR/supports, page participants, clôture/tirage, bilan et préférences futures selon arbitrage |
| Site Animation / Marketplace / Live | **Concerné** : présentation publique, inscription mobile, identité et reprise, confirmation et suivi. Une simple ouverture par prévisualisation de lien ou robot ne doit pas créer une participation |
| Localeo Pro | **Non requis pour qualifier** ce modèle ; **à examiner** pour la remise optionnelle des bons numériques et la non-régression des autres modèles |
| ERP / Support / Ops | **Concerné** : modèle identifiable, supervision des refus/doublons/abus et assistance sans visibilité indue des données personnelles. CRM E71 sans transfert automatique |
| API et consommateurs | **À spécifier** : exposition du modèle et de ses capacités, commande publique de participation/reprise, statut, statistiques et préférences. Aucun faux contrat OpenAPI ajouté au cadrage |
| Persistance / migration | **À examiner** : catalogue, preuve de qualification autonome, unicité concurrente, provenance du QR, préférences et conservation ; aucune reprise automatique des anciennes tombolas |
| Performance | **Concerné** : QR commun susceptible de rafales, inscription concurrente et limites anti-abus ; pagination/index/comptages bornés selon la convention transverse ; volumétrie propre à cette mécanique à confirmer |
| Générateur / fixtures | **Concerné** : organisation sans commerce, lots externes, nouveau et ancien participant, répétition, clôture, refus communication, perte réseau et droits ; génération via parcours métier normal, sans campagne distante à ce stade |
| Documentation fonctionnelle / règlement | **Concerné** : guide stand, distinction tombolas, conditions de participation, information sur les données et préférences. Faire relire le règlement spécifique avant commercialisation ; aucune validation juridique présumée |
| Exploitation / livraison | **À examiner** : activation du modèle après livraison de tous les consommateurs, notifications, conservation, observabilité et retour arrière ; hébergement et clés existants à réutiliser si suffisants |

## Questions ouvertes

| ID | Décision attendue et proposition | Partie dépendante |
| --- | --- | --- |
| E74-ARB-01 | Formulaire puis confirmation explicite, ou participation immédiate pour un compte reconnu ? Recommandation : action explicite, confirmation claire, sans effet de bord lors d'une simple consultation | US04, CA07/08 |
| E74-ARB-02 | Participation via lien partagé autorisée ou présence au stand requise ? Un QR fixe seul ne démontre pas une présence physique. Recommandation V1 : lien partageable ; si présence exigée, cadrer la preuve et le rôle de l'animateur | US03/04, CA05/09 |
| E74-ARB-03 | Données obligatoires et preuve d'identité : proposition prénom + email, réutilisation de Live et vérification email selon les capacités existantes ; confirmer une chance par identité et la règle pour les participants sans compte | US04, anti-doublons, éligibilité et contact gagnant |
| E74-ARB-04 | Modes de dotation disponibles : externe seul en V1, ou les trois modes E73 ? Recommandation : réutiliser les modes compatibles, avec remise numérique par commerce uniquement si volontairement choisie | US02/07 et parcours sans commerce de bout en bout |
| E74-ARB-05 | Confirmer l'utilisation du quota d'animations standard existant, ainsi que l'ouverture aux souscriptions standard déjà actives ; aucune hausse tarifaire ni quota illimité déduit de la demande | US01, catalogue et conditions acquises E73 |
| E74-ARB-06 | Recueil facultatif pour les futures animations ou simple conservation du jeu ? Si retenu, préciser destinataire de l'autorisation (organisateur/commune/Localeo), canaux et parcours d'envoi autorisé. Le module E73 actuel ne couvre pas implicitement des campagnes inter-animations après sa fenêtre | US05, préférences et réutilisation d'audience |

Les trois questions interactives initiales correspondent à ARB-01, ARB-02 et
au premier choix d'ARB-06. Leurs réponses ne sont pas encore consignées dans ce
cadrage. Les autres propositions restent à traiter avant leur spécification.

## Passage à la spécification

Ce backlog comprend **8 US et 16 critères cibles**, avec **6 groupes d'arbitrages**.
Le besoin sans commerçant et l'inclusion standard sont acquis. La spécification
devra résoudre les décisions dépendantes, rapprocher le nouveau modèle du registre
existant, définir identité/participation/communication et détailler contrats,
transactions, index et preuves. Les scénarios ci-dessus sont prévus, **non exécutés**.
Ce cadrage ne réalise ni implémentation, ni migration, ni envoi, ni déploiement.
