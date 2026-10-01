# EPIC 68 — Parcours commerçant de préparation et finalisation de l'onboarding

## Références

- Date de cadrage : **30 septembre 2026**.
- Identifiant : **EPIC-68**, disponible après recherche dans la roadmap commune,
  ses namespaces applicatifs et les sources ciblées des applications voisines.
- État produit : **À faire**, selon la [roadmap commune](../README.md).
- Demande : associer le commerçant à la préparation avant le rendez-vous pour
  finaliser son onboarding en **une heure**, avec des prestations examinées,
  les informations nécessaires à Localeo et un commerçant rassuré et autonome.
- Phase réalisée : **cadrage initial uniquement** ; spécification, priorité et
  date de livraison restent à établir.

### Rattachement et dépendances

L'[EPIC 50](../terminees/epic-50-conformite-fiscale-bum-backlog.md) porte le socle
OnBoard interne et le [parcours terrain](../../specifications/epic-50-conformite-fiscale-bum/onboarding-commercant-mobile.md).
L'EPIC 68 porte un résultat autonome : **un parcours partagé avec le commerçant,
commençant avant le rendez-vous**, avec contributions, questions, confirmations
et préparation vérifiée. Elle réutilise le dossier existant sans rouvrir l'EPIC 50
ni créer un second référentiel commerçant. L'exclusion historique de création
autonome n'est pas levée : Localeo initie et rattache le dossier.

Réutiliser également :

- [EPIC 39 — Stripe Connect](../terminees/epic-39-stripe-connect-psp-backlog.md) et
  sa [procédure d'onboarding](../../exploitation/exploitation/onboarder-commercant-stripe-connect.md)
  pour le parcours hébergé, les capacités et les reprises ;
- [EPIC 60 — ERP et commercialisation](../terminees/epic-60-vision-360-commercialisation-backlog.md)
  pour modèles, copies, versions, aptitudes et référentiel commun ;
- [EPIC 62 — Validation des modifications de prestations](epic-62-validation-modifications-prestations-backlog.md),
  **à faire**, pour son futur sas sur les prestations déjà applicables. La
  préparation initiale d'une offre relève de l'EPIC 68 ; elle ne livre pas
  implicitement ce sas et ne doit pas permettre d'en contourner les règles ;
- [EPIC 38 — Documents](../terminees/epic-38-gestion-documentaire-backlog.md),
  [EPIC 10 — Accès commerçant](../terminees/epic-10-authentification-commercant-login-password-backlog.md),
  [EPIC 8 — Questions et support](../terminees/epic-8-gestion-contacts-messages-support-backlog.md),
  [EPIC 26 — Communications](../terminees/epic-26-communication-libre-backoffice-backlog.md)
  et [EPIC 48 — Ordonnancement](../terminees/epic-48-apscheduler-ordonnancement-batchs-backlog.md).

## Problème et résultat attendu

**Constat rapporté par l'utilisateur :** le commerçant participe trop tard au
processus. Le rendez-vous concentre découverte de la plateforme, inquiétudes
sur Stripe, examen de la viabilité des prestations, recherche des documents et
première lecture du contrat. Cela réduit le temps de compréhension et de prise
en main. Aucune mesure chiffrée de durée ou de taux de réussite n'est disponible
dans ce cadrage ; une mesure initiale est à établir.

**Socle documenté :** OnBoard permet déjà préparation et suivi internes, checklist,
documents, invitation et test d'accès. Le commerçant en préparation peut déjà
accéder à son profil et à Stripe. En revanche, les droits avant activation ne
couvrent pas actuellement l'ensemble des messages et prestations commerciales :
le futur espace de préparation exige des permissions propres, pas l'ouverture
anticipée de tous les droits commerciaux. L'existence d'un email, d'un document
ou d'un diagnostic n'établit pas sa compréhension ou son acceptation.

**Acteurs :** commerçant et signataire habilité, référent Localeo responsable du
dossier, opérateur chargé des documents et prestations, administrateur habilité
à la qualification BUM ; Stripe pour ses contrôles et les capacités de paiement.

**Avant / après attendu :** au lieu de découvrir le contrat et Stripe pendant
le rendez-vous, le commerçant reçoit un parcours lisible, prépare ses éléments,
pose ses questions et propose ses prestations. Localeo examine ces éléments
avant le jour J. Le rendez-vous sert à lever les dernières questions, confirmer
les décisions et pratiquer sur la plateforme.

Le succès comprend deux résultats distincts :

- le commerçant comprend ses engagements, sait se connecter et réaliser les
  gestes utiles sans communiquer son mot de passe ;
- Localeo dispose d'informations et de preuves contrôlées pour le référencement
  du commerçant et de ses prestations, avec chaque capacité réellement ouverte
  ou encore bloquée identifiée. La fin du rendez-vous ne vaut pas mise en vente.

## Périmètre

### Avant le rendez-vous : préparer ensemble

1. Localeo planifie le rendez-vous dans le dossier existant : interlocuteur,
   coordonnées confirmées, référent, date, heure, durée d'une heure, lieu ou mode
   à distance, moyen de poser une question et de demander un report.
2. Le commerçant reçoit une invitation expliquant Localeo, les bénéfices et le
   fonctionnement de la plateforme, le déroulé du rendez-vous et les éléments
   à préparer. Un accès personnel lui permet de retrouver et reprendre sa
   préparation sur mobile ; la modalité d'accès reste à spécifier.
3. La préparation présente une checklist adaptée au commerce : informations
   de référencement, documents nécessaires avec leur motif, contrat à lire,
   propositions de prestations, informations Stripe et prochaines actions.
   Distinguer ce qui est demandé maintenant, ce qui pourra être traité pendant
   le rendez-vous et ce qui conditionne uniquement une capacité ultérieure.
4. Le commerçant peut soumettre ses éléments progressivement, poser des
   questions et suivre les demandes de correction. Localeo prépare une réponse,
   désigne un responsable et vérifie avec lui que la question est résolue.
5. Avant le rendez-vous, Localeo examine la préparation et partage un récapitulatif
   des éléments prêts, des décisions attendues et des manquants. Un dossier
   incomplet entraîne un contact et un choix explicite : maintien adapté ou
   report, jamais une annulation ni une validation silencieuse.

### Stripe : expliquer les coûts et le rôle réel

Prévoir une présentation courte et compréhensible avant tout renvoi vers Stripe :
son rôle dans les paiements et reversements, la raison des informations demandées,
qui renseigne quoi, les étapes et l'interlocuteur en cas de difficulté. Expliquer
les protections et contrôles effectivement apportés sans promettre une absence
de risque, un paiement inconditionnel ou un délai non garanti.

**Exigence produit : les frais Stripe sont portés par Localeo, pas par le
commerçant**, conformément au modèle de l'EPIC 39. Distinguer explicitement ces
frais de la commission Localeo et du montant de reversement convenu. La
spécification doit rattacher le texte exact à la convention et au périmètre des
frais pris en charge, sans annoncer que tous les services sont gratuits.

Le commerçant peut commencer ou reprendre Stripe en amont. Les coordonnées
bancaires et preuves demandées par Stripe suivent son parcours hébergé ; ne pas
les redemander par email. Le retour de navigation ne prouve pas que Stripe est
prêt : conserver le contrôle serveur de ses exigences et capacités.

### Prestations : examiner la viabilité avant le jour J

Permettre au commerçant de préparer une proposition décrivant le contenu,
les conditions d'utilisation, la capacité à l'honorer, les disponibilités ou
restrictions et les éléments économiques nécessaires. Les champs et droits
précis seront définis en spécification ; les commissions et décisions fiscales
ne deviennent pas librement modifiables par ce parcours.

Localeo examine la faisabilité opérationnelle, la clarté de la promesse, la
cohérence économique et les informations fiscales, puis demande une correction
ou confirme la version examinée. Le commerçant connaît l'état et le motif de
la décision avant le rendez-vous. Une modification significative après examen
rend visible ce qui doit être revérifié ; elle ne réutilise pas une approbation
sur un contenu différent.

Réutiliser les modèles de prestations préparables **sans coffret**. L'acceptation
d'une proposition ne vaut ni rattachement automatique, ni publication, ni
qualification fiscale BUM d'un coffret. Le diagnostic `REVIEW_REQUIRED` exige
un traitement explicite dans la préparation ; une checklist exécutée ne doit
pas être présentée comme un avis fiscal favorable. Préserver la séparation des
décisions documentée dans le [contrôle BUM](../../exploitation/exploitation/traiter-blocage-wording-acquisition-bum.md).

### Documents et contrat : donner du temps pour lire

Présenter une liste conditionnelle des pièces avec format attendu, destination,
statut et éventuel motif de refus. Réutiliser les documents valides déjà présents,
prévoir un dépôt sécurisé et une aide pour les éléments manquants. Distinguer
pièce déposée, vérifiée et acceptée ; ne pas assimiler dépôt et conformité.

Le contrat complet, sa version et un résumé pédagogique sont accessibles avant
le rendez-vous. Les clauses financières, engagements et modalités opérationnelles
peuvent faire l'objet de questions en amont. Distinguer mise à disposition,
consultation, déclaration de lecture et signature. Aucun délai écoulé ni clic
d'ouverture ne vaut consentement. Si le contrat change, signaler la nouvelle
version et rouvrir les confirmations concernées. La signature avant le rendez-vous
ou pendant celui-ci reste à arbitrer ; aucun nouveau prestataire de signature
n'est décidé ici.

### Réception et questions : une boucle vérifiable

Le suivi distingue envoi demandé, envoi effectué, livraison ou échec technique
lorsque l'information est disponible, et **confirmation explicite du commerçant**
qu'il a reçu les informations et pris connaissance du rendez-vous. L'ouverture
d'un email n'est pas une preuve suffisante de lecture ou de compréhension.

Le commerçant peut déclarer « J'ai des questions » ou « Je n'ai pas de question
à ce stade » et revenir sur cette déclaration. L'absence de réponse reste
inconnue. Une réponse envoyée par Localeo ne clôt pas automatiquement la question.
En cas de non-réponse ou d'échec de livraison, le référent reçoit une action de
contact ; un échange téléphonique peut être consigné avec date, auteur et résultat.

### Calendrier et rendez-vous d'une heure — propositions à challenger

**Hypothèse de travail, non délai validé :** invitation dès la planification,
avec une cible à **J−7 jours calendaires**, relance ciblée vers J−3 si nécessaire,
revue interne à J−2 et récapitulatif à J−1. La spécification comparera notamment
J−7 et J−10 selon la complexité des pièces, les disponibilités et le délai réel
nécessaire à la lecture. Un rendez-vous pris tardivement suit un parcours adapté,
sans prétendre que les étapes anticipées ont eu lieu.

La demande mentionne « 43 phases » : le nombre reste à confirmer. **Proposition
en quatre phases**, totalisant 60 minutes :

| Phase | Durée proposée | Résultat attendu |
| --- | ---: | --- |
| Accueil et questions restantes | 10 min | Compréhension reformulée par le commerçant, points ouverts identifiés |
| Contrat, documents et Stripe | 15 min | Engagements compris, preuves et état Stripe vérifiés, décisions restantes explicites |
| Prestations et référencement | 20 min | Versions examinées confirmées, conditions et économie comprises, publication distinguée de la préparation |
| Prise en main et autonomie | 15 min | Connexion sur l'appareil du commerçant, exercice guidé puis réalisé seul, contact support retrouvé |

La dernière phase couvre les gestes utiles : retrouver son offre, comprendre
comment honorer une prestation, consulter ses reversements et demander de
l'aide. Les exercices utilisent un scénario de démonstration adapté aux droits
disponibles, sans achat, consommation ni mouvement financier réel involontaire.

À la fin : récapitulatif partagé, capacités ouvertes ou bloquées, actions restantes
avec responsable et échéance. Un suivi après rendez-vous confirme la prise en main
et traite les restes à faire ; proposition J+2 à valider. Une contrainte externe
Stripe ne doit pas être masquée pour annoncer un onboarding terminé en une heure.

### Exclusions et contraintes

- Pas de refonte générale d'OnBoard, de CRM complet ni d'auto-inscription publique.
- Pas de changement du modèle économique, de calcul fiscal ou des conditions
  Stripe décidé par cette epic ; leur explication doit être fidèle au référentiel.
- Pas de vente, activation, qualification BUM ou signature automatique à partir
  d'un email, d'une soumission ou de la clôture du rendez-vous.
- Pas d'obligation générale de posséder une prestation ou un coffret pour
  finaliser le référencement commerçant : les aptitudes commerciales restent
  distinctes de son dossier, conformément au socle existant.
- Pas de copie concurrente des profils, documents ou prestations ; toute collecte
  préparatoire garde sa provenance et ses règles d'intégration au référentiel.
- Pas d'intégration calendrier externe, SMS ou signature électronique supplémentaire
  imposée en V1 ; besoin et coût à arbitrer s'ils sont nécessaires.

Découpage proposé : (1) invitation, accès de préparation et contenus ;
(2) contributions, examen et boucle questions ; (3) conduite du rendez-vous,
reprise et mesure. Ces lots ne valent pas livraison du parcours complet isolément.

## Critères d'acceptation

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E68-CA-01 | Référent, rendez-vous planifié | Initier la préparation | Invitation rattachée au dossier existant, date/heure/modalité, durée, référent, déroulé et prochaines actions lisibles ; aucun doublon commerçant |
| E68-CA-02 | Commerçant avant activation | Ouvrir puis reprendre la préparation sur mobile | Accès à son seul dossier et aux actions de préparation autorisées ; lien expiré/remplacé repris sans ouvrir les droits de vente ou un dossier tiers |
| E68-CA-03 | Commerçant découvrant Stripe | Consulter l'explication avant de commencer | Rôle, informations demandées, protections réelles, aide et frais Stripe pris en charge par Localeo compris ; commission Localeo distinguée, aucune promesse de garantie absolue |
| E68-CA-04 | Commerçant, exigences documentaires applicables | Consulter la liste puis déposer une pièce | Liste adaptée avec motif et destination ; dépôt sécurisé, statut de contrôle et correction visible ; réutilisation des preuves valides, aucun document bancaire demandé par email |
| E68-CA-05 | Commerçant/signataire, contrat disponible en amont | Lire, questionner puis confirmer ou signer selon le parcours retenu | Version identifiée, temps de lecture permis ; consultation, lecture déclarée et signature distinctes ; nouvelle version signalée sans réemploi silencieux de l'accord |
| E68-CA-06 | Commerçant, offre sans coffret possible | Proposer puis corriger une prestation avant J | Brouillon reprenable et soumission identifiable ; aucune publication ni modification silencieuse d'une offre déjà applicable |
| E68-CA-07 | Opérateur habilité, proposition soumise | Examiner avant J la faisabilité et l'économie | Décision sur une version précise, motif et corrections partagés ; accord commerçant sur les conditions traçable ; changement significatif impose un nouvel examen des éléments touchés |
| E68-CA-08 | Référent, risque fiscal ou autre réserve détecté | Préparer le bilan avant rendez-vous | Réserve, responsable et action visibles ; `REVIEW_REQUIRED` n'est pas affiché comme validation favorable ; acceptation d'une prestation distincte de la qualification BUM du coffret |
| E68-CA-09 | Email envoyé, événement fournisseur reçu ou absent | Afficher le suivi puis recueillir la confirmation | Livraison technique et confirmation commerçant distinctes ; ni ouverture ni silence ne valent réception comprise, rendez-vous confirmé ou absence de question |
| E68-CA-10 | Commerçant ayant une question | La soumettre, recevoir une réponse et confirmer sa résolution | Échange lié au dossier, responsable et état visibles ; nouvelle question possible après « aucune question à ce stade » ; réponse de Localeo seule insuffisante pour conclure |
| E68-CA-11 | Non-réponse, échec email ou préparation incomplète | Appliquer relance et traitement humain | Actions bornées et traçables, échec visible au référent ; pas de relance en double lors d'un rejeu, pas de dossier déclaré prêt par défaut |
| E68-CA-12 | Report, annulation ou rendez-vous rapproché | Modifier le rendez-vous | Anciennes relances devenues inutiles neutralisées, nouvelles échéances explicites ; documents conservés selon leurs règles, aucun faux historique de préparation |
| E68-CA-13 | Référent et commerçant, point avant J | Consulter le même récapitulatif partagé | Éléments prêts/manquants, questions et prochaines actions concordants ; maintien adapté ou report motivé ; dossier commerçant et aptitudes commerciales distingués |
| E68-CA-14 | Dossier préparé, rendez-vous tenu | Suivre le déroulé retenu | Durée cible de 60 minutes vérifiable, aucune étape obligatoire supprimée pour respecter l'heure ; dépassement et cause consignés |
| E68-CA-15 | Commerçant sur son propre appareil | Se connecter et réaliser les gestes de prise en main | Autonomie observée sur scénario représentatif, aide retrouvable ; ni partage de mot de passe ni opération financière réelle de test |
| E68-CA-16 | Fin du rendez-vous, blocages possibles | Partager le bilan puis réaliser le suivi | Informations de référencement et prestations examinées retrouvables ; chaque reste à faire a un responsable et une échéance ; aucune vente ou capacité Stripe annoncée sans contrôle serveur |
| E68-CA-17 | Pilote Localeo, dossiers représentatifs | Mesurer le parcours avant/après | Durées, préparation avant J, questions non résolues, reprises et autonomie suivies avec définition des événements et dénominateurs ; chiffres inconnus non remplacés par des succès |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Backend, domaine propriétaire | **Concerné** : cycle et préparation dans le domaine onboarding existant ; identités, documents, communication, référencement/commercialisation et BUM conservent leurs règles. L'application orchestre, les interfaces ne décident pas seules qu'un dossier est prêt |
| ERP / OnBoard / Support | **Concernés** : préparation partagée, file des actions/questions, examen, déroulé et bilan ; désigner l'entrée de référence sans multiplier les dossiers ou files concurrentes |
| Application Commerçant | **Concernée** : accès avant activation, checklist, contributions et questions. Les droits actuels profil/Stripe ne suffisent pas : définir des capacités de préparation limitées et les parcours de reprise |
| Marketplace | **À examiner** : réutilisation d'une présentation publique de la plateforme ou de supports existants ; aucun changement de checkout ou de vendabilité demandé |
| Application Animation | **Sans objet pour son interface V1** : aucun parcours partenaire demandé ; non-régression des prestations partagées à vérifier si leurs contrats évoluent |
| API et consommateurs | **Concernés** : producteur backend, consommateurs internes et commerçant ; contrat canonique, états/actions, erreurs, droits, concurrence et compatibilité à spécifier, sans exposer les API internes aux commerçants |
| Persistance, migrations et existant | **À examiner** : préparation, confirmations, versions, questions et échéances ; reprise de dossiers ouverts ou clôturés sans inventer de lecture/consentement historique ; migration seulement après conception |
| Email et traitements | **Concernés** : réutiliser envoi, événements fournisseur et ordonnanceur, relances idempotentes, report/annulation, erreurs et reprise ; respecter la [charte email](../../architecture/transverse/charte-emails-localeo.md) |
| Documents et accès | **Concernés** : droits du commerçant/signataire, collecte minimale, pièces conditionnelles, contrôles existants, historique des versions et durées de conservation à préciser ; pas de copie sensible dans les emails ou liens publics |
| Générateur / fixtures | **Concernés** : [EPIC 63](../terminees/epic-63-jeux-demonstration-communes-backlog.md), scénarios avant J, sans réponse, email en échec, questions, corrections, contrat changé, Stripe en attente, report et issue partielle ; génération isolée sans envoi réel |
| Documentation fonctionnelle | **Concernée** : parcours E50, espace commerçant, pédagogie Stripe, pièces, contrat, prestations, assistance ; une source canonique par sujet, contenus exacts à relier aux contrats approuvés |
| Exploitation / livraison | **Concernées** : supervision des relances et dossiers oubliés, responsable et délai de réponse, activation progressive sans envoi massif aux anciens dossiers ; ordre backend/consommateurs, recette email et reprise à définir |

## Questions ouvertes

| Arbitrage | Décision attendue et proposition | Effet sur la spécification |
| --- | --- | --- |
| E68-ARB-01 | Délai avant J : comparer J−7 et J−10, jours calendaires/ouvrés, délai de lecture et prise de RDV tardive | Calendrier, relances et critères de préparation ; aucun délai choisi implicitement |
| E68-ARB-02 | Confirmer 3 ou 4 phases : proposition de quatre phases et 60 minutes ci-dessus | Déroulé, supports et recette chronométrée |
| E68-ARB-03 | Choisir l'accès avant activation : espace commerçant limité avec invitation, ou entrée dédiée reliée au même dossier ; préciser représentant/signataire | Authentification, droits, reprise et parcours mobile |
| E68-ARB-04 | Fixer qui répond et examine, sous quel délai, et les critères du maintien adapté/report ; proposition de revue à J−2 | Organisation de la file, responsabilités, alertes ; le silence ne vaut jamais confirmation |
| E68-ARB-05 | Arrêter les pièces conditionnelles et le moment de signature : avant J facultatif ou pendant J après questions | Contrat, habilitation du signataire, délai de lecture et preuves ; pas de fournisseur de signature imposé |
| E68-ARB-06 | Définir la grille de viabilité des prestations, les approbateurs et la frontière avec E62 pour les offres existantes | Modèle/proposition/copie, droits d'édition, critères économiques et traitement des réserves BUM |
| E68-ARB-07 | Valider les textes pédagogiques Stripe : périmètre exact des frais portés par Localeo, protections décrites et limites ; support court texte/visuel/vidéo | Contenus cohérents avec convention et fonctionnement réel ; choix média sans refonte imposée |
| E68-ARB-08 | Définir nombre/canaux de relances, suivi après J et mesure pilote : proposition email puis contact humain et point à J+2 | Coût opérationnel, accessibilité, instrumentation et objectifs chiffrés après mesure initiale |

## Passage à la spécification

Le besoin, les acteurs et les critères sont cadrés. La prochaine phase doit
décrire le parcours de bout en bout, les écrans et messages, les états et preuves,
les responsabilités et contrats, puis relier chaque critère aux scénarios de
réussite, refus, absence de réponse et reprise. Suivre le
[cycle d'epic](../../organisation/cycle-epic.md).

La spécification sera reliée à ce backlog et à l'index canonique lorsqu'elle
existera ; aucun dossier de conception vide ni contrat API hypothétique n'est
créé ici. Les arbitrages ci-dessus bloquent seulement les choix qui en dépendent.
Ce cadrage n'a déclenché aucun email, aucune modification applicative, ni aucun
déploiement.
