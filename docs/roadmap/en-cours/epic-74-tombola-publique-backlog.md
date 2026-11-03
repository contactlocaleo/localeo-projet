# EPIC 74 — Tombola publique sans commerçant

## Références et état

- **État produit : En cours**, cadrage initial du **22 octobre 2026**.
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
- [Spécification détaillée V1](../../specifications/epic-74-tombola-publique/README.md)
  du **3 novembre 2026** : six arbitrages résolus, architecture et preuves prévues.
  Implémentation locale engagée le 3 novembre : backend, Animation et Live ; migration v288 désactivée par défaut. Le [bilan des tests](../../specifications/epic-74-tombola-publique/verification.md) distingue les preuves exécutées et les contrôles restants.

## Évolution E74-EVOL-INSCRIPTION-DIRECTE — 3 novembre 2026

Demande explicite : QR ou bouton Live → e-mail et règlement → inscription immédiate → un seul mail de confirmation, avec suite du jeu et accès personnel au carnet/install Live. Elle remplace l’exigence initiale de prénom et vérification intermédiaire (ARB-01/03). Les critères conservent leurs identifiants ; historique, anciens liens et une chance par adresse sont préservés. Aucun ancien inscrit en attente n’est qualifié automatiquement. L’adresse déclarée n’est pas réputée vérifiée. Voir la [spécification actualisée](../../specifications/epic-74-tombola-publique/README.md).

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

## Décisions acquises

| Référence | Nature | Contenu |
| --- | --- | --- |
| E74-DEC-01 | Demande acquise | Ajouter une « Tombola publique » au forfait standard, sans achat d'un module supplémentaire pour accéder à ce type d'animation |
| E74-DEC-02 | Demande acquise | Aucun commerçant requis pour créer, publier et participer ; qualification depuis le parcours ouvert par le QR public |
| E74-DEC-03 | Demande acquise | QR utilisable sur un support physique, notamment un stand sur un marché |
| E74-DEC-04 | Décision du 3 novembre | Développer le public par le suivi facultatif de la commune dans Live, sans nouveau canal d'envoi ni campagne inter-animations |
| E74-PROP-01 | Retenue et précisée le 3 novembre | Une participation et une chance par e-mail normalisé et par tombola dès l’inscription explicite ; rescans sans chance supplémentaire (évolution INSCRIPTION-DIRECTE) |
| E74-PROP-02 | Retenue le 3 novembre | Quota standard consommé à la publication, y compris pour les souscriptions déjà actives ; aucune hausse ni quota illimité implicite |
| E74-PROP-03 | Précisée le 3 novembre | E-mail seul, règlement accepté, qualification immédiate et un mail de confirmation ; ancien choix prénom + vérification remplacé par INSCRIPTION-DIRECTE |
| E74-PROP-04 | Remplacée par ARB-06 le 3 novembre | Suivi local facultatif de la commune ; refus/retrait sans perte de chance. Aucun consentement marketing déduit de l'inscription |

Les références de propositions initiales sont conservées pour la traçabilité.
Les réponses explicites du porteur produit du 3 novembre résolvent les six
groupes d'arbitrages consignés plus bas.

## Périmètre

### Inclus

- Nouveau type d'animation clairement distinct de « Tombola locale des
  commerçants » dans le catalogue standard. Code `TOMBOLA_PUBLIQUE`, version `1.0`.
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
- Suivi facultatif de la commune dans Live, mémorisé sur l'appareil et modifiable
  dans « Mes communes » ; aucun envoi ni inscription automatique aux futurs jeux.
- Statistiques pertinentes : inscriptions confirmées, participations éligibles,
  source de diffusion si connue, gagnants et lots remis ; ne pas inventer des
  passages ou achats chez des commerçants.

### Dotation : indépendance à préserver

Une tombola à **lots libres gérés en externe** doit pouvoir fonctionner de bout
en bout sans aucun commerce : l'organisateur assure la remise. La compatibilité
avec Coffrets et bons numériques E73 est retenue (ARB-04). Un commerce chargé
de remettre un bon, s'il est utilisé, ne devient pas une étape de qualification
du participant. Les exigences existantes de remise d'un bon numérique ne sont
pas supprimées silencieusement pour rendre cette variante autonome.

### Hors périmètre

- Billets payants, achat obligatoire, chances proportionnelles à une dépense,
  gains instantanés ou second moteur de tirage.
- Modification de la qualification de la tombola commerçante, du passeport ou
  de la chasse au trésor ; migration automatique des anciennes animations.
- Nouveau CRM de prospection B2B : E71 concerne organisations et contacts
  commerciaux, pas la création implicite de prospects à partir des joueurs.
- Nouvelle plateforme d'envoi marketing. Le recueil de préférences ne donne
  pas de droits gratuits au module Communication E73 et n'étend pas implicitement
  ses campagnes, limitées aux participants d'une animation et à leur fenêtre
  d'envoi. Aucun nouveau canal ni campagne inter-animations retenu en ARB-06.
- Scan hors connexion, géolocalisation obligatoire, application native ou
  contrôle physique de présence : le lien est partageable selon ARB-02.

## User stories

| ID | Acteur et besoin | Critères |
| --- | --- | --- |
| E74-US-01 | Organisateur : choisir la tombola publique parmi les animations standard | 01, 02 |
| E74-US-02 | Organisateur : configurer et publier sans commerçant, avec un parcours adapté | 03, 04 |
| E74-US-03 | Organisateur : télécharger le QR et un support compréhensible pour un stand | 05, 06 |
| E74-US-04 | Visiteur : participer depuis son téléphone et savoir que sa participation est enregistrée | 07, 08, 09 |
| E74-US-05 | Participant : choisir séparément de suivre la commune dans Live pour retrouver ses animations | 10, 11 |
| E74-US-06 | Gestionnaire : suivre et clôturer la tombola puis tirer les gagnants | 12, 13 |
| E74-US-07 | Gagnant et organisateur : recevoir le résultat et suivre la remise du lot | 14 |
| E74-US-08 | Localeo : superviser, mesurer et exploiter le nouveau modèle sans régression | 15, 16 |

## Critères d'acceptation cibles

Les identifiants restent stables. Les formulations ont été précisées selon les
arbitrages du 3 novembre ; les critères ne constituent pas une preuve d'implémentation.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E74-CA-01 | Organisateur habilité, forfait standard actif | Consulter le catalogue et choisir une tombola | « Tombola publique » est identifiable et incluse ; aucune souscription de module spécifique exigée |
| E74-CA-02 | Quota et droits du forfait connus, souscription nouvelle ou déjà active | Publier/rejouer la publication | Quota standard existant consommé une seule fois, conditions acquises inchangées ; aucune double consommation ni accès sans droit |
| E74-CA-03 | Organisation sans aucun commerce rattaché, dotation externe prête | Créer puis publier la tombola | Aucun commerce, mission, invitation, minimum de commerces ou paiement Coffrets imposé à cette configuration ; dates/règlement/dotation requis restent contrôlés |
| E74-CA-04 | Gestionnaire autorisé dans sa commune | Parcourir l'assistant et le suivi | Étapes commerçants absentes ou explicitement non applicables ; une action directe ne contourne pas les droits d'organisation/commune |
| E74-CA-05 | Tombola publiée | Télécharger le support puis scanner le QR ou ouvrir le lien | Ouverture de la bonne animation ; QR sans identité personnelle ni secret d'administration ; lien lisible proposé en alternative |
| E74-CA-06 | Flyer d'une tombola publique avec dotation connue | Lire le document | Promesse et nombre d'exemplaires cohérents ; aucune instruction d'achat/scan chez un commerçant ni compteur commerçants inadapté ; image personnalisée compatible avec le socle flyer |
| E74-CA-07 | Visiteur pendant la période autorisée | Saisir l’e-mail et accepter le règlement depuis le QR ou S’inscrire dans Live | Inscription immédiatement qualifiée, une chance, confirmation claire et un seul mail expliquant la suite et invitant au carnet/install Live. Pas de prénom ni vérification intermédiaire ; aucune mutation sur simple ouverture |
| E74-CA-08 | Même e-mail normalisé, double clic/rescan/réponse perdue | Répéter ou reprendre la participation | Une participation et une chance par tombola ; même clé et corps rejoués sans second mail. Aucune restitution publique d’accès personnel ; récupération par mail bornée. Une erreur réseau n’est pas annoncée comme succès |
| E74-CA-09 | Avant ouverture, à/après la fin, animation clôturée ou annulée | Tenter une première inscription directe ou confirmer un ancien lien | Refus compréhensible sans qualification ; contrôle serveur des dates et statuts, y compris lien reçu avant fermeture. Aucune preuve de présence exigée |
| E74-CA-10 | Visiteur qui refuse suivi commune ou notifications facultatives | Participer | Accès au jeu et chances inchangés ; aucune préférence positive implicite tirée du scan ou de l'acceptation du règlement |
| E74-CA-11 | Participant souhaitant suivre la commune dans Live | Ajouter puis retirer le suivi | Choix explicite, portée navigateur annoncée, limite et stockage indisponible gérés ; retrait sans suppression de participation. Aucun nouveau canal d'envoi, opt-in marketing ou campagne inter-animations |
| E74-CA-12 | Gestionnaire, liste de participants et bilan | Consulter, filtrer et clôturer | Listes paginées côté serveur, totaux exacts, pas de faux passages commerçants ; inscriptions directes comptées et figées avec les anciennes qualifications, sans assimiler adresse déclarée et vérifiée ; population figée selon le socle de clôture |
| E74-CA-13 | Tombola clôturée, tirage autorisé | Tirer, rejouer ou tirer avec zéro/peu de candidats | Résultat cohérent avec la population figée ; aucun double tirage/gain involontaire ; règles de suppléants et cas sans candidat explicites |
| E74-CA-14 | Tirage confirmé et dotation compatible | Notifier puis remettre un lot | Parcours de remise E73 conservé, état d'envoi distinct de remise ; la gestion externe reste réalisable sans commerce |
| E74-CA-15 | Utilisateur non habilité ou trafic automatisé | Appeler les routes publiques/protégées | Pas d'accès aux participants d'autrui ; protections contre abus, erreurs sans données privées, audit exploitable et performances bornées |
| E74-CA-16 | Autres modèles et données existantes | Rejouer leurs parcours et les fixtures de démonstration | Qualification commerçante inchangée ; modèle public testé isolément, aucune activation ni conversion automatique d'animations existantes |

## Impacts instruits par la spécification

L'[architecture canonique](../../specifications/epic-74-tombola-publique/architecture-contrats.md)
décrit les producteurs/consommateurs vérifiés, données, concurrence, bornes et
livraison ; la [matrice des preuves](../../specifications/epic-74-tombola-publique/verification.md)
relie les 16 critères aux tests, documents, fixtures et opérations.

| Sujet | Impact retenu |
| --- | --- |
| Domaine/backend | Moteur public et preuve de qualification (inscription directe ou vérification historique), identité minimale, qualification/publication sans commerce, gel depuis les faits, quota standard et liste réellement bornée |
| Animation | Catalogue, assistant, création/configuration, QR/flyer, participants, bilan et tirage contextualisés |
| Marketplace/Live | Fiche publique, inscription directe et mail de confirmation, anciens liens maintenus, reprise, renderer, découvertes/filtres et suivi local facultatif ; pas de nouveau compte |
| Pro | Aucune qualification par scan/PIN E74 ; non-régression des autres modèles et remise optionnelle de bons numériques |
| ERP/Support/Ops | Capacités du modèle, refus compréhensibles, supervision et périmètres organisation/commune ; aucun transfert CRM automatique |
| Contrats | Producteur backend, exporteurs existants et deux registres frontend fermés à étendre avant activation ; aucun faux OpenAPI généré durant la spécification |
| Données | Migration additive identité/challenge/preuve/projection/index ; pas de conversion historique ; suppression/anonymisation/restauration à vérifier |
| Performance | QR commun et IP partagée, anti-abus par adresse, pages 25/100 et traitements par lots ; budgets N/10N et charge mixte définis, à mesurer |
| Générateur | Organisation sans commerce, trois modes de lots, inscription directe et anciennes attentes/confirmations/expirations ; commandes métier et transport e-mail isolé |
| Documents | Guides organisateur/habitant/stand, contrats, notice/règlement et procédures ; revue de mise en service séparée des tests de clôture |
| Exploitation | Outbox et reprise, purge, observabilité, activation après consommateurs compatibles ; pas de nouveau DNS, tarif ou clé d'envoi prévu |

## Arbitrages résolus le 3 novembre 2026

| ID | Décision explicite | Partie concernée |
| --- | --- | --- |
| E74-ARB-01 | Remplacé par INSCRIPTION-DIRECTE : formulaire e-mail/règlement et qualification immédiate ; un seul mail après inscription, aucun effet lors d’une simple ouverture | US04, CA07/08 |
| E74-ARB-02 | QR/lien partageables, sans contrôle de présence au stand | US03/04, CA05/09 |
| E74-ARB-03 | Remplacé par INSCRIPTION-DIRECTE : e-mail déclaré seul, une chance par adresse normalisée et par tombola, sans nouveau compte ni marquage fictif « vérifié » | US04, CA07/08/15 |
| E74-ARB-04 | Trois modes E73 : Coffrets, bons numériques, lots libres externes ; les lots externes restent autonomes sans commerce | US02/07, CA03/13/14 |
| E74-ARB-05 | Quota standard existant, applicable également aux souscriptions actives, sans modification des conditions acquises | US01, CA01/02 |
| E74-ARB-06 | Suivi facultatif de la commune dans Live, sans nouveau canal d'envoi ni campagne inter-animations | US05, CA10/11 |

Les réponses produit sont regroupées dans trois questions : parcours et preuve
(ARB-01/02/03), dotation et quota (ARB-04/05), suivi de commune (ARB-06).
Aucun arbitrage produit bloquant ne reste ouvert pour cette V1.

## Passage à l'implémentation

Ce backlog conserve **8 US et 16 critères**, avec **6 groupes d'arbitrages résolus**.
La spécification V1 détaille comportements, contrats cibles, responsabilités,
transactions, index, migration, compatibilité et preuves. Les limites existantes
sont explicites, notamment le refus Coffrets si les candidats sont moins nombreux
que les lots et l'absence actuelle de vérification d'e-mail.

L’état produit demeure **En cours**, conformément à la roadmap. Le bilan distingue les preuves historiques et les tests de l’évolution INSCRIPTION-DIRECTE ; un succès local ne constitue ni une migration distante ni un déploiement.
