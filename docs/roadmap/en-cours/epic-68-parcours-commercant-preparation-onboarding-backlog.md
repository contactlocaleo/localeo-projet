# EPIC 68 — Mettre en place le processus d'onboarding commerçant

**État courant : En cours — implémentation V1.2 engagée le 3 octobre 2026.**
Les paramètres ARB-01/04/06/08/10 sont approuvés par l'utilisateur : Europe/Paris,
10 h dans la fenêtre 9–18 h, revue J−2, contact humain après 48 h, rappel SMS J−1,
reprise des anciens dossiers sur décision explicite et grille de revue Backoffice.
Les [preuves et actions de configuration](../../specifications/epic-68-preparation-onboarding/verification-livraison.md)
distinguent validation locale, approbation éditoriale des supports et recette déployée.
Les états antérieurs conservés plus bas décrivent l'historique de conception.

## Périmètre de référence — processus de bout en bout

**E68-PROCESSUS-20261003 — 3 octobre 2026, conception V1.2.** L'epic se limite
à mettre en place le processus décrit ci-dessous, du référencement à la
finalisation du dossier. Elle relie et complète les outils existants pour que
le gestionnaire sache quoi faire et que le commerçant arrive préparé à son
rendez-vous d'une heure. Les détails techniques et les 31 critères conservés
servent ce parcours ; ils ne constituent pas des produits supplémentaires.

| Étape | Actions à rendre possibles | Critères du parcours |
| --- | --- | --- |
| 1. Référencer et ouvrir le dossier | Créer le commerçant, rattacher son dossier unique, vérifier les coordonnées, affecter le référent ; afficher checklist et prochaine action dans l'ERP | CA-18/20/21/22 |
| 2. Planifier le rendez-vous | Saisir date/heure, durée d'une heure, Teams ou adresse ; préparer l'email avec calendrier et confirmer explicitement son envoi | CA-01/19/29 |
| 3. Préparer et confirmer les communications | À J−7 configurable, présenter le pack et ses destinataires au gestionnaire ; confirmer ensemble mail/SMS nominal, suivre chaque canal ; deux supports et rappel des prestations connues dans le mail | CA-03/09/23/24/25/26 |
| 4. Accompagner la préparation | Même compte commerçant : initialisation/récupération d'accès existante, vue limitée de préparation, réception/questions ; contrat téléchargeable et imprimable, prestations examinées, consignes de pièces, orientation vers Stripe | CA-02/04/05/06/07/08/10/27/28 |
| 5. Faire le point avant J | Traiter les points ouverts, maintenir/adapter/reporter ; préparer le rappel J−1 et faire confirmer son envoi ; préserver les preuves encore valides | CA-11/12/13/30 |
| 6. Conduire le rendez-vous | Quatre phases 10/15/10/25 minutes : questions, dossier/contrat/Stripe avec signature jour J, prestations, pratique sans opération financière réelle et bilan | CA-14/15 |
| 7. Enregistrer et finaliser | Gestionnaire Localeo : dépôt interne et contrôle de la copie signée après rendez-vous, bilan partagé, actions restantes attribuées ; finalisation explicite sur preuves actuelles | CA-16 |

Les deux exigences transverses restent rattachées au processus : **CA-31**, guide
opérationnel publié et accessible dans l'ERP ; **CA-17**, vérification de son
efficacité sur un pilote à partir des durées, relances et résultats observés.
Il n'est pas demandé de produit analytique ou de tableau de bord décisionnel autonome.

**Périmètre à réaliser :** dossier/checklist et file de suivi, rendez-vous,
préparation et confirmation des envois, espace commerçant guidé, suivi des
questions et des prestations initiales, déroulé et bilan, rattachement des
preuves et finalisation, supports et guide ERP. Les cas d'erreur, reports,
reprises et contrôles d'accès sont les garanties de ce même processus.

**Socles à réutiliser :** identité et accès commerçant, Stripe hébergé, documents
internes et contrat, référentiel des prestations, transports email/SMS,
ordonnanceur, habilitations et règles OnBoard de finalisation. Adapter seulement
leurs points d'intégration nécessaires ; ne pas reconstruire ces fonctions.

**Hors de cette epic :** CRM de prospection (EPIC 71), moteur générique de workflows,
espace temporaire avec une seconde identité, dépôt de pièces par le commerçant,
nouvelle signature électronique, création automatique Teams, refonte de Stripe,
de la BUM, de la finance ou des habilitations, publication commerciale automatique
et sas de modification des prestations déjà applicables (EPIC 62).

**Résultat de livraison attendu :** un gestionnaire peut conduire le parcours
complet dans l'ERP, le commerçant sait préparer puis utiliser son compte, et le
dossier se finalise seulement après contrôle des éléments requis. La signature
jour J est conservée, puis la copie signée est déposée par Localeo. Aucun envoi
E68 ne part sans autorisation explicite : le calendrier prépare, l'opérateur confirme.
Les paramètres encore ouverts restent listés dans le dossier de spécification.
État maintenu **À faire** : ce recadrage ne vaut ni implémentation ni livraison.

## Références

Les références datées retracent les décisions successives. Le périmètre V1.2
ci-dessus et les décisions du 3 octobre priment sur les anciens envois automatiques
ou propositions de signature avant J ; les autres exigences du parcours sont conservées.

- **E68-SIMPLIFICATION-20261002** : l'utilisateur retire **uniquement le dépôt de
  pièces commerçant en V1** et demande un parcours simple qui assiste et guide.
  L'espace de préparation est conservé pour réception, questions, contrat et
  prestations. Cette précision remplace la composante dépôt de la conception V1.0.

- Date de cadrage : **30 septembre 2026**.
- Recadrage du **1er octobre 2026**, `E68-PILOTAGE-20261001` : démarrage au
  référencement d'un nouveau commerçant, dossier unique, rendez-vous final
  d'une heure (Teams ou physique) et checklist de préparation pilotable au backoffice.
- Complément du **1er octobre 2026**, `E68-COMMUNICATIONS-20261001` : envoi
  automatique d'un mail et d'un SMS à **J−7, délai configurable**, suivi par canal
  dans le dossier, avec les supports préparatoires joints au mail.
- Validation du **1er octobre 2026**, `E68-ACCOMPAGNEMENT-20261001` : confirmation
  de réception et questions depuis le mail, pièces personnalisées et contrat
  disponibles en amont, fichier calendrier `.ics`, rappel J−1 et contact humain
  en cas de non-confirmation. Un guide backoffice expliquant le processus et
  chaque étape devra être produit avec les spécifications et accessible dans l'ERP.
- Identifiant : **EPIC-68**, disponible après recherche dans la roadmap commune,
  ses namespaces applicatifs et les sources ciblées des applications voisines.
- État produit : **À faire**, selon la [roadmap commune](../README.md).
- Demande : associer le commerçant à la préparation avant le rendez-vous pour
  finaliser son onboarding en **une heure**, avec des prestations examinées,
  les informations nécessaires à Localeo et un commerçant rassuré et autonome.
- Phase réalisée : **spécification V1.2 du 3 octobre 2026, sans implémentation**,
  après cadrage et revue critique du 1er octobre. Les recommandations E68-REV-01
  à 09 sont retenues ; les paramètres non arbitrés restent explicitement ouverts.
  Priorité et date de livraison ne sont pas fixées.
- [Dossier de spécification](../../specifications/epic-68-preparation-onboarding/README.md) :
  parcours, architecture et contrats, communications, guide backoffice et sources
  des deux supports commerçant ; [matrice des 31 critères et livraison](../../specifications/epic-68-preparation-onboarding/verification-livraison.md).

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
- [EPIC 62 — Validation des modifications de prestations](../a-faire/epic-62-validation-modifications-prestations-backlog.md),
  **à faire**, pour son futur sas sur les prestations déjà applicables. La
  préparation initiale d'une offre relève de l'EPIC 68 ; elle ne livre pas
  implicitement ce sas et ne doit pas permettre d'en contourner les règles ;
- [EPIC 38 — Documents](../terminees/epic-38-gestion-documentaire-backlog.md),
  [EPIC 10 — Accès commerçant](../terminees/epic-10-authentification-commercant-login-password-backlog.md),
  [EPIC 8 — Questions et support](../terminees/epic-8-gestion-contacts-messages-support-backlog.md),
  [EPIC 26 — Communications](../terminees/epic-26-communication-libre-backoffice-backlog.md)
  et [EPIC 48 — Ordonnancement](../terminees/epic-48-apscheduler-ordonnancement-batchs-backlog.md).

## Problème et résultat attendu

**Complément utilisateur du 1er octobre :** le processus doit aussi être plus
simple à gérer côté backoffice. L'opérateur doit retrouver un dossier dès qu'il
référence un nouveau commerçant, y renseigner le rendez-vous final et savoir
immédiatement quelles actions préparer et suivre. Le rendez-vous est un jalon
du dossier ; il n'est plus le déclencheur de son ouverture.

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

**Lecture ciblée du backend au 1er octobre, `d1a16e8` :** la
[création ERP](../../../../localeo-backend/app/application/commercialisation/services/atelier_erp.py)
et le [parcours OnBoard](../../../../localeo-backend/app/api/onboarding_commercant_api.py)
ouvrent déjà le dossier avec le commerçant. Le
[service OnBoard](../../../../localeo-backend/app/application/conformite_fiscale_bum/service_onboarding_commercant.py)
retrouve un dossier existant et le modèle impose son unicité par commerçant.
Date/heure, affectation, checklist métier et prochaine action existent ; durée,
modalité Teams/physique, lien/lieu et suivi individuel des actions préparatoires
restent à compléter. L'automatisme d'ouverture n'est pas démontré pour tous les
producteurs : le use case de référencement seul ne crée pas de dossier. La
spécification devra cartographier les API et imports concernés. Ce constat en
lecture ne constitue pas un test ni une recette de l'environnement déployé.

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

### Priorité à la simplicité — V1.2

Présenter les sept étapes du processus de référence : référencer, planifier,
préparer/confirmer les communications, accompagner la préparation, faire le point
avant J, conduire le rendez-vous, enregistrer/finaliser.
Chaque écran met en avant la prochaine action utile et l'aide du référent, sans
exiger que l'utilisateur connaisse les états techniques. Les contrôles automatiques
ne sont pas ressaisis. Le commerçant utilise l'espace léger pour confirmer la
réception, poser ses questions, consulter le contrat et préparer les prestations ;
**aucun bouton, formulaire ou API de téléversement de pièces E68 n'est livré**.
Il prépare ses documents pour le rendez-vous, ou utilise un canal sécurisé déjà
existant et vérifié. La liste des pièces reste informative ; « à apporter » ne
signifie ni reçu ni vérifié. Les pièces sensibles ne sont pas demandées par email,
et les justificatifs Stripe restent dans le parcours hébergé Stripe.


### Démarrer au référencement et piloter depuis un dossier unique

**Décisions acquises au 1er octobre :**

1. L'enregistrement d'un **nouveau commerçant dans le référentiel Localeo**
   démarre son onboarding et ouvre ou rattache son dossier de préparation.
   Ce référencement initial ne signifie ni activation ni mise en vente. Il ne
   dépend pas de la date du rendez-vous et ne demande pas une seconde création
   manuelle du même commerçant. Une reprise ou une requête répétée retrouve le
   même dossier ; une mise à jour du profil ne lance pas un nouvel onboarding.
2. Le dossier est consultable depuis la fiche commerçant et rassemble son
   interlocuteur, son référent Localeo, le rendez-vous, les actions à préparer,
   les éléments déjà reçus, les questions et les blocages. Réutiliser le dossier
   OnBoard existant et les objets canoniques, sans introduire un CRM parallèle.
3. Le référent peut renseigner la **date et l'heure du rendez-vous final**, sur
   un **créneau d'une heure**, et choisir **Teams** ou **physique**. Le dossier
   présente le lien Teams ou le lieu/adresse correspondant. Le rendez-vous peut
   rester « À planifier » pendant que les premières actions avancent.
4. Une **checklist des actions à préparer en amont** permet de suivre le dossier
   sans reconstituer son état depuis plusieurs écrans. La planification rend
   visibles les échéances liées au rendez-vous ; les éléments déjà préparés
   restent acquis selon leurs règles de validité.

**Fonctionnement retenu, à détailler en spécification :** checklist de
base disponible dès l'ouverture, complétée selon le commerce. Avant planification,
les tâches liées à J indiquent « Échéance à fixer » ; aucune date n'est inventée.
L'opérateur voit pour chaque action ce qui est attendu, qui doit agir (Localeo
ou commerçant), son état, son échéance lorsqu'elle est connue et le lien vers
l'élément utile. Les libellés d'état proposés sont « À faire », « En cours »,
« En attente du commerçant », « Bloquée », « Terminée » et « Non applicable »
avec motif ; leur modèle précis reste à concevoir.

La checklist distingue une action humaine attestée d'un résultat contrôlé par
le système : consigner un appel ou l'envoi d'un support ne valide ni le contrat,
ni les documents, ni les capacités Stripe. Pour une action humaine, conserver
l'auteur, la date et le résultat ; pour un contrôle existant, afficher son état
réel et sa source. Un changement de pièce, de contrat ou de prestation rend
visible la vérification à reprendre. Une liste entièrement cochée ne déclenche
aucune activation commerciale.

Les envois, pièces reçues, signatures et états Stripe alimentent automatiquement
la vue depuis leurs sources canoniques. Le référent ne recoche pas ces résultats
et ne les recopie pas dans un commentaire obligatoire. Ses actions manuelles
portent sur les échanges, examens, décisions et blocages humains ; la prochaine
action utile est mise en avant. Une preuve périmée ou modifiée rend visible la
revue à reprendre, même si un palier de progression avait déjà été acquis.

Le suivi distingue **la préparation du rendez-vous**, **son issue** (tenu,
reporté, annulé ou commerçant absent) et **la finalisation de l'inscription**.
« Rendez-vous réalisé » ne clôture pas le dossier : des conditions métier,
notamment Stripe, peuvent rester à satisfaire. Une absence ou un commerçant
injoignable donne lieu à une action attribuée, pas à un abandon automatique.

### Checklist initiale proposée côté backoffice

Cette liste reprend les irritants du cadrage initial. Confirmation immédiate,
pack mail/SMS à J−7 configurable et rappel J−1 sont acquis ; les échéances
de revue et les responsables restent à préciser selon E68-ARB-04.

| Action à préparer | Responsable proposé | Résultat à suivre |
| --- | --- | --- |
| Confirmer l'interlocuteur et le contact | Référent Localeo | Coordonnées vérifiées, personne à joindre et référent identifiés |
| Planifier le rendez-vous final | Référent Localeo | Date, heure, créneau d'une heure, Teams avec lien facultatif ou physique avec lieu |
| Transmettre l'invitation et le parcours préparatoire | Envoi automatique, supervisé par le référent | Confirmation immédiate avec calendrier, pack mail avec deux supports joints et SMS à J−7 configurable, rappel J−1 ; programmation, envoi et réception suivis par canal, secours distinct en cas d'échec confirmé du mail |
| Vérifier la réception et recueillir les questions | Référent et commerçant | Confirmation explicite, questions suivies ou déclaration « aucune question à ce stade » ; silence signalé |
| Présenter Stripe et accompagner la préparation | Référent et commerçant | Explication des coûts et protections, questions traitées, exigences/capacités Stripe réelles visibles |
| Préparer et contrôler les pièces | Commerçant puis opérateur habilité | Pièces applicables reçues et vérifiées, manquants ou corrections identifiés |
| Mettre le contrat à disposition et suivre sa lecture | Référent et signataire | Version transmise, lecture déclarée et questions ; signature suivie séparément selon le parcours retenu |
| Préparer et examiner les prestations | Commerçant puis opérateur habilité | Propositions et versions examinées, corrections et réserves visibles, sans publication implicite |
| Préparer la prise en main de la plateforme | Référent et commerçant | Présentation et accès préparés ; exercice d'autonomie prévu pour le rendez-vous |
| Faire la revue avant rendez-vous | Référent Localeo | Synthèse des prêts/manquants, questions et décisions ; maintien adapté ou report explicite |

**Vue de suivi retenue :** une liste des dossiers avec commerçant, référent,
prochain rendez-vous ou « À planifier », prochaine action et blocages. Pouvoir
retrouver rapidement les rendez-vous proches, les dossiers sans date, les
actions en retard et ceux en attente du commerçant. Un indicateur d'avancement
peut aider, mais il ne remplace pas les actions restantes ni leurs motifs.
Les commentaires internes et pièces privées ne deviennent pas automatiquement
visibles dans le récapitulatif partagé au commerçant.

### Avant le rendez-vous : préparer ensemble

1. Depuis le dossier ouvert au référencement, Localeo planifie le rendez-vous :
   interlocuteur, coordonnées confirmées, référent, date et heure, créneau d'une
   heure, Teams avec lien facultatif ou présence physique avec lieu, moyen de poser une
   question et de demander un report. Un rendez-vous encore incomplet reste
   visible comme tel, sans être présenté comme une invitation prête à envoyer.
2. Dès la planification complète, le commerçant reçoit une confirmation légère
   du rendez-vous par mail avec son calendrier `.ics`. À J−7 configurable, il
   reçoit le pack préparatoire complet (mail et SMS), puis un rappel bref à J−1.
   Les envois rapprochés doivent être coordonnés pour éviter deux messages
   équivalents ; la règle de regroupement sera précisée en spécification.
   Son accès personnel lui permet de retrouver et reprendre sa préparation
   sur mobile, avec récupération d'accès si nécessaire.
3. La préparation présente une checklist adaptée au commerce : informations
   de référencement, documents nécessaires avec leur motif, contrat à lire,
   propositions de prestations, informations Stripe et prochaines actions.
   Distinguer ce qui est demandé maintenant, ce qui pourra être traité pendant
   le rendez-vous et ce qui conditionne uniquement une capacité ultérieure.
4. Le commerçant peut soumettre ses éléments progressivement, poser des
   questions et suivre les demandes de correction de ses informations ou prestations,
   sans dépôt de pièces dans l'espace E68. Localeo prépare une réponse,
   désigne un responsable et vérifie avec lui que la question est résolue.
5. Avant le rendez-vous, Localeo examine la préparation et partage un récapitulatif
   des éléments prêts, des décisions attendues et des manquants. Un dossier
   incomplet entraîne un contact et un choix explicite : maintien adapté ou
   report, jamais une annulation ni une validation silencieuse.

**Accès retenu :** un espace de préparation limité, utilisable avant activation,
pour confirmer la réception, poser des questions, voir les pièces à préparer, lire le
contrat et préparer/corriger les prestations. Concevoir ces droits et la reprise
de session avant les messages qui y renvoient. Réutiliser les mécanismes d'accès
existants et distinguer leur email d'initialisation des communications de
rendez-vous : le pack J−7 ne présume pas qu'un ancien lien est encore valide.
Le bouton principal du pack ouvre la demande de création du mot de passe ; le
gestionnaire n'a pas à envoyer une invitation séparée. La confirmation du pack
prépare l'identifiant manquant sans modifier un compte existant. Le commerçant
demande ensuite son lien personnel en saisissant son email ; après création et
connexion, il revient à sa préparation. Un lien secondaire conserve l'accès des
comptes déjà configurés. Aucun secret personnel n'est placé dans l'aperçu du pack.
Le contact opérationnel n'est pas réputé habilité à signer ; l'identité et les
droits du signataire restent contrôlés. L'intégration précise de cet espace et
son contrat devront être définis avec l'application Commerçant.

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

Présenter une liste conditionnelle des pièces à préparer, leur motif et la
consigne (présentation au rendez-vous ou canal sécurisé existant vérifié).
Réutiliser les documents valides déjà présents. **Pas de dépôt de pièces par le
commerçant dans la V1 E68**, ni nouveau stockage préparatoire associé. Localeo
contrôle et enregistre les preuves par ses outils internes autorisés. Distinguer
à préparer, reçu, vérifié et accepté ; ne pas assimiler une déclaration de préparation
à une pièce reçue. Une pièce attendue le jour J reste une réserve avant J et
permet un maintien adapté, sans afficher artificiellement le dossier prêt.

Le contrat complet, sa version et un résumé pédagogique sont accessibles avant
le rendez-vous. Le contrat courant est téléchargeable en PDF pour impression
et lecture en amont. Les clauses financières, engagements et modalités opérationnelles
peuvent faire l'objet de questions en amont. Distinguer mise à disposition,
consultation, déclaration de lecture et signature. Aucun délai écoulé ni clic
d'ouverture ne vaut consentement. Si le contrat change, signaler la nouvelle
version et rouvrir les confirmations concernées. **Décision du 3 octobre 2026 :
signature le jour J après les questions**, en vérifiant la version imprimée et
l'habilitation du signataire. Après le rendez-vous, le gestionnaire Localeo dépose
la copie signée dans le dossier interne et contrôle version, signataires, date
réelle de signature et lisibilité selon les règles documentaires existantes.
Le commerçant n'effectue aucun upload. Pour Teams, organiser la remise de la copie
signée par un moyen existant adapté ; tant qu'elle manque ou n'est pas vérifiée,
le dossier reste à compléter. La signature ne remplace pas les autres contrôles
de finalisation. Aucun nouveau prestataire de signature n'est décidé ici.

### Confirmation à la planification, puis pack préparatoire à J−7

**E68-CONFIRMATION-ENVOIS-20261003 — décision du 3 octobre.** Chaque séquence de
communication E68 requiert une confirmation explicite du gestionnaire habilité,
précédée d'un aperçu des destinataires, contenus, pièces jointes et échéance/fenêtre.
À J−7, le mail et le SMS nominal sont autorisés ensemble par une seule validation.
La confirmation de rendez-vous, le rappel J−1, le secours SMS et les avis de
report/annulation ou correctifs ont chacun leur propre validation. Sans accord,
les messages restent « À confirmer », avec action attribuée et retard visible ;
aucune émission à la seule échéance. Une modification pertinente invalide la
validation non encore exécutée. La confirmation est contrôlée côté serveur,
tracée et idempotente ; fermer l'aperçu ou cliquer deux fois ne provoque aucun
envoi implicite ou doublon. Les reprises techniques certaines conservent cette
autorisation uniquement pour le même message inchangé et toujours pertinent.
Ce choix remplace l'automatisme d'envoi décrit dans les décisions historiques :
le calendrier prépare les communications, le gestionnaire autorise leur envoi.

**Confirmation immédiate retenue :** dès que date, heure, interlocuteur Localeo
et modalité sont renseignés (adresse obligatoire en physique, lien Teams facultatif), préparer puis faire confirmer l'envoi d'un mail bref confirmant
le rendez-vous, avec un fichier `.ics`. Il annonce que les informations de
préparation suivront. Ce message ne confirme pas à la place du commerçant sa
présence. Il ne répète pas l'email d'initialisation de compte et ne contient
pas nécessairement les deux supports du pack J−7.

**Demande acquise :** une fois le rendez-vous planifié, programmer la préparation d'un mail et
un SMS au commerçant **sept jours avant le jour J par défaut**. Le délai doit
être configurable **globalement en V1, en jours calendaires**, sans dérogation
par dossier. Afficher le délai retenu et la date/heure calculée ; définir un
fuseau explicite et un créneau d'envoi en journée, dont les valeurs restent à
préciser. La saisie d'un rendez-vous ne doit pas conduire à un SMS nocturne.
Les dossiers sans date conservent une action de planification attribuée.

Avant l'envoi, vérifier la présence du rendez-vous, de son interlocuteur Localeo,
des coordonnées de contact utilisables et des deux supports. Si un élément
indispensable manque, afficher l'action à corriger et le canal bloqué dans le
dossier ; ne pas inventer de destinataire ni annoncer un envoi réussi.
La création du commerçant seule n'envoie pas ces messages : le rendez-vous et
son échéance pilotent la préparation, suivie de la confirmation explicite d'envoi.

**SMS attendu :**

- rappeler la date et l'heure du rendez-vous ;
- nommer la personne de Localeo que le commerçant rencontrera ;
- indiquer qu'un mail a été envoyé à **son adresse email**, pour expliquer les
  étapes de l'onboarding et ce qu'il doit préparer pour le jour J.

Exemple de rédaction, à adapter à la longueur du SMS :

> Localeo : votre rendez-vous avec [Prénom Nom] est prévu le [date] à [heure].
> Un mail a été envoyé à [adresse email] avec les étapes de votre onboarding
> et les éléments à préparer. À bientôt !

Le SMS reprenant « un mail a été envoyé » n'est émis qu'après confirmation
technique de prise en charge de l'envoi du mail, pas dès sa simple programmation.
Cette prise en charge ne prouve pas la livraison dans la boîte du destinataire.
Un résultat d'envoi incertain du mail garde le SMS nominal en attente et
déclenche une vérification avant toute reprise. **Après échec confirmé du mail,
un SMS de secours distinct est prévu**, rappelant le rendez-vous et demandant
de vérifier l'adresse email ou de contacter Localeo ; il ne prétend pas qu'un
mail a été envoyé. Il utilise un numéro utilisable et ne s'ajoute pas à un SMS
nominal déjà parti pour la même séquence. Un rejet tardif de livraison reste
visible et crée une action humaine si le SMS nominal est déjà envoyé. Les
tentatives de secours restent bornées et ne forment pas une boucle automatique.

**Mail attendu :** contexte et bénéfice du rendez-vous, date/heure et durée,
personne rencontrée, lien Teams ou lieu physique, étapes de l'onboarding et
liste concrète des éléments à préparer. Le commerçant doit pouvoir retrouver
ces informations et contacter son référent pour une question ou un report.
Les informations essentielles sont lisibles dans le corps du mail, sans devoir
ouvrir les pièces jointes.

**Hiérarchie retenue :** en tête, « Votre rendez-vous » et les actions à réaliser,
puis le détail des prestations et les supports. Une entrée principale vers la
préparation permet de confirmer la réception, poser une question et préparer
ses prestations ; les pièces suivent les consignes sans dépôt E68. Les deux
supports demandés restent joints. Le backoffice permet
de prévisualiser le mail et ses PJ avant envoi, sans modifier les données ou
preuves canoniques depuis cet aperçu. Un aperçu reste indicatif tant que les
versions destinées à l'envoi n'ont pas été figées.

**Expliquer le rendez-vous de finalisation de l'inscription :** le corps du
mail doit présenter son objectif et son déroulement en termes simples, en
cohérence avec le support joint et le guide backoffice. Préciser que l'heure
avec le référent sert à examiner les éléments préparés, répondre aux questions,
finaliser les points du dossier qui peuvent l'être et prendre en main l'espace
commerçant. Le commerçant doit savoir ce qu'il fera lui-même et ce que Localeo
vérifiera avec lui.

Trame de présentation proposée, correspondant aux quatre phases ci-dessous :

> Pendant ce rendez-vous d'une heure, nous répondrons à vos dernières questions,
> puis nous ferons ensemble le point sur votre dossier, vos documents, votre
> contrat et votre parcours Stripe. Nous relirons les prestations déjà préparées
> et leurs conditions, ou préciserons avec vous les prochaines étapes de votre
> offre. Vous vous connecterez ensuite à votre espace commerçant et réaliserez
> quelques gestes pratiques avec notre accompagnement. Nous terminerons par un
> bilan clair de ce qui est finalisé et des éventuelles actions restantes.

Expliquer les modalités pratiques : en visio, rejoindre le lien Teams indiqué ;
en présentiel, se rendre à l'adresse indiquée. Prévoir un téléphone ou un
ordinateur permettant d'accéder à son email et à son espace commerçant, les
éléments encore demandés dans la checklist et ses questions. Le commerçant
saisit lui-même ses accès ; aucun mot de passe n'est à communiquer au référent.
Si une pièce ou une validation Stripe manque, annoncer les étapes de suivi
plutôt que promettre une activation ou une mise en vente immédiate à l'issue.

**Rappel des prestations déjà saisies :** lorsque le dossier comporte des
prestations en préparation, inclure dans le corps du mail leur récapitulatif
détaillé pour relecture avant le rendez-vous. Pour chacune, reprendre les
informations déjà renseignées et destinées au commerçant : intitulé, description
du contenu, conditions d'utilisation, durée ou validité, disponibilités/restrictions
et éléments tarifaires partagés lorsqu'ils existent. Indiquer les informations
restant à compléter, sans les inventer, ainsi que l'état de préparation ou
d'examen ; une prestation saisie n'est pas présentée comme validée ou publiée.

Le commerçant est invité à vérifier ce rappel et à signaler une correction ou
une question via le parcours de préparation. Aucune prestation saisie : ne pas
afficher de tableau vide et ne pas bloquer le mail ; conserver les consignes
pour préparer ses propositions. Le récapitulatif reflète les versions figées
pour la prise en charge de cet envoi, et sa trace reste rattachée au dossier,
même si les prestations sont modifiées ensuite. Ne pas inclure de notes internes ni de données d'un autre
commerçant. Vérifier les cas zéro, une et plusieurs prestations, y compris une
prestation incomplète ou modifiée après envoi.

**Deux supports doivent être joints au mail** (format PDF proposé) :

1. **Le déroulé du jour J** : objectif du rendez-vous d'une heure, séquences,
   préparation attendue et résultat à l'issue. Reprendre les quatre phases et
   la répartition 10/15/10/25 minutes validées dans E68-ARB-02.
2. **La boucle Localeo, vue par le commerçant, et le rôle de Stripe** : comment
   son offre entre dans un coffret, comment le bénéficiaire vient utiliser sa
   prestation, comment il la valide et comment il suit son reversement ; qui
   fait quoi, protections et aide. Expliquer que, **dans le parcours Localeo,
   les frais Stripe sont pris en charge par Localeo**, en distinguant la commission
   Localeo. « Stripe est gratuit » ne doit pas devenir une promesse générale
   sur tous les produits ou usages Stripe.

**Programmation et contenu distincts :** programmer une intention liée au
rendez-vous, puis figer ensemble destinataire, rendez-vous, prestations et
supports avant remise au fournisseur. La spécification précisera ce point de
figement et la protection contre une modification concurrente. Avant prise en
charge, une programmation obsolète peut être annulée/recalculée ; après envoi,
conserver le message exact et traiter une correction comme une nouvelle
communication explicite. Ne pas annoncer qu'un email déjà parti a été mis à jour.

Conserver la version des supports effectivement envoyés dans la trace du dossier,
avec les destinataires et informations de rendez-vous de cet envoi. Une nouvelle
version ne réécrit pas l'historique. Une pièce jointe manquante ou impossible à
préparer empêche l'envoi du mail incomplet et fait apparaître un blocage.
Les supports ne contiennent ni pièces d'identité, ni coordonnées bancaires, ni
secrets d'accès du commerçant.

**Suivi dans le dossier :** une ligne par canal, avec date prévue, tentative,
destinataire, état d'envoi, livraison connue ou inconnue, motif d'échec exploitable
et prochaine action. États de présentation proposés : « Programmé », « En
attente », « Pris en charge », « Livré », « Échec » et « Annulé » ; ils doivent
refléter les informations réellement disponibles chez le fournisseur. L'acceptation
technique, la livraison et la confirmation humaine restent distinctes.

Un rejeu du traitement ou un événement fournisseur répété ne doit pas provoquer
de double envoi. Si le mail est parti mais le SMS a échoué, la reprise concerne
le SMS ; elle ne renvoie pas automatiquement le mail. En cas de résultat incertain,
vérifier l'état avant de proposer un nouvel envoi. Report ou annulation du
rendez-vous neutralise les messages programmés devenus obsolètes ; les messages
déjà envoyés restent dans l'historique et une action de mise à jour du commerçant
est visible. Un changement du délai de configuration ne renvoie jamais un message
déjà émis ; son effet sur les programmations en attente doit être explicite.

### Réception et questions : une boucle vérifiable

Le suivi du mail et du SMS distingue envoi demandé, envoi effectué, livraison ou échec technique
lorsque l'information est disponible, et **confirmation explicite du commerçant**
qu'il a reçu les informations et pris connaissance du rendez-vous. L'ouverture
d'un email n'est pas une preuve suffisante de lecture ou de compréhension.

Le commerçant peut déclarer « J'ai des questions » ou « Je n'ai pas de question
à ce stade » et revenir sur cette déclaration. L'absence de réponse reste
inconnue. Une réponse envoyée par Localeo ne clôt pas automatiquement la question.
En cas de non-réponse ou d'échec de livraison, le référent reçoit une action de
contact ; un échange téléphonique peut être consigné avec date, auteur et résultat.

### Calendrier et rendez-vous d'une heure

**Déclencheur validé :** le dossier démarre au référencement du nouveau commerçant,
même sans rendez-vous. Le calendrier suivant concerne les communications et
échéances autour du rendez-vous, pas l'ouverture du dossier.

**Déclenchement validé : mail et SMS à J−7 par défaut, délai configurable.**
Les jours calendaires et le réglage global sont retenus ; fuseau et créneau
d'envoi restent à préciser. **Propositions restantes :**
relance ciblée vers J−3 si nécessaire et revue interne à J−2. Le rappel bref
à J−1 est retenu ; son canal et son horaire restent à préciser.
Pour un rendez-vous pris après l'échéance théorique, proposer l'envoi dès que les
informations sont complètes, dans le créneau d'envoi autorisé ; cette règle de
rattrapage reste à valider. Ne pas envoyer un rappel pour un rendez-vous déjà
passé ni prétendre que les étapes anticipées ont eu lieu.

**Déroulé retenu en quatre phases**, totalisant 60 minutes. La revue des prestations
avant J constitue un jalon de préparation ; le rendez-vous confirme cet examen
et garde du temps pour la prise en main et le bilan.

| Phase | Durée cible retenue | Résultat attendu |
| --- | ---: | --- |
| Accueil et questions restantes | 10 min | Compréhension reformulée par le commerçant, points ouverts identifiés |
| Contrat, documents et Stripe | 15 min | Engagements compris, preuves et état Stripe vérifiés, décisions restantes explicites |
| Prestations et référencement | 10 min | Versions examinées avant J confirmées, conditions et économie comprises, publication distinguée de la préparation |
| Prise en main, autonomie et bilan | 25 min | Connexion sur l'appareil du commerçant, exercice guidé puis réalisé seul, contact support retrouvé ; capacités et actions restantes récapitulées |

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
- Pas d'intégration calendrier externe ni de signature électronique supplémentaire
  imposée en V1. Le SMS préparatoire est inclus ; réutiliser le fournisseur et
  les mécanismes d'envoi existants, sans choisir un nouveau prestataire ici.
- Choisir Teams ne présume ni création automatique d'une réunion Microsoft,
  ni accès au calendrier : un lien peut être renseigné dans le dossier. Aucun
  envoi automatique d'invitation n'est décidé par le seul référencement.

Découpage proposé : (1) ouverture du dossier, planification, checklist et suivi
backoffice ; (2) invitation, accès de préparation, contenus et contributions du
commerçant, examen et questions ; (3) conduite du rendez-vous, reprise et mesure.
Ces lots ne valent pas livraison du parcours complet isolément.

### Documentation backoffice à produire avec les spécifications

**Livrable demandé : un guide opérationnel du parcours d'onboarding, consultable
dans la documentation de l'ERP.** Le rédiger avec la spécification, puis le
mettre en cohérence avec les écrans et actions réellement livrés. Il doit
permettre à un opérateur de conduire un dossier sans avoir à lire les contrats API.

Contenu attendu :

- vue d'ensemble du parcours et répartition des tâches entre Localeo et commerçant ;
- ouverture du dossier au référencement, affectation du référent et planification ;
- lecture des états alimentés automatiquement et traitement des actions humaines,
  prochaine action utile, distinction préparation/rendez-vous tenu/inscription finalisée ;
- confirmation immédiate avec calendrier, réglage global du délai J−7 et
  compréhension de la programmation mail/SMS, des deux supports et du rappel J−1 ;
- prévisualisation du mail et des PJ, accès commerçant limité et récupération d'accès,
  distinction entre contact et signataire ;
- suivi des états : programmé, envoi pris en charge, livraison connue/inconnue,
  confirmation commerçant et questions ; action à mener selon le résultat ;
- examen des pièces, du contrat, de Stripe et des prestations avant le rendez-vous ;
- déroulé du jour J, exercice d'autonomie, bilan et suivi des actions restantes ;
- cas pratiques : coordonnées erronées, PJ indisponible, échec partiel, absence
  de réponse, rendez-vous tardif, report/annulation, changement de contrat et
  exigences Stripe encore en attente. Préciser qui intervient et comment reprendre
  sans double envoi ni fausse validation ; distinguer SMS nominal, secours après
  échec confirmé du mail et vérification d'un résultat incertain.

Conserver une source canonique dans la documentation de formation backoffice
du dépôt projet, reliée au guide général et à la spécification E68. Sa publication
doit passer par les lecteurs documentaires ERP et le bundle existants, selon la
[procédure documentaire](../../exploitation/technique/reference-documentation-centralisee.md) :
déclarer la source dans `documentation.exports.json`, fournir une entrée retrouvable
depuis la documentation ERP et un accès contextuel depuis le dossier onboarding,
contrôler les droits et tester sa lecture depuis un backend livré seul avec bundle.
Ne pas créer une copie divergente dans le backend.

Le guide de processus est distinct des deux supports adressés au commerçant.
Pendant la conception, identifier clairement les parcours cibles non disponibles ;
à la livraison, les consignes doivent correspondre au fonctionnement réel.
La présence d'un fichier Markdown ou son export ne prouve pas sa disponibilité
dans l'ERP déployé : prévoir une recette d'ouverture et de navigation du guide.

## Critères d'acceptation

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E68-CA-01 | Référent, dossier ouvert et rendez-vous planifié | Compléter les informations puis confirmer explicitement l'envoi de la séquence concernée | Confirmation légère avec `.ics` préparée dès planification complète, pack à J−7 configurable et rappel J−1 ; chaque séquence attend sa validation, aucun envoi à la seule sauvegarde ; date/heure, créneau d'une heure, lien/lieu et référent cohérents ; pas de doublon ni confirmation de présence supposée |
| E68-CA-02 | Commerçant avant activation | Ouvrir puis reprendre la préparation sur mobile | Espace limité et guidé pour réception/questions, liste des pièces à préparer, contrat et propositions ; aucune fonction de dépôt E68 ; récupération d'accès, pas de droits commerciaux ni pouvoir de signature déduit du contact |
| E68-CA-03 | Commerçant découvrant Stripe | Consulter l'explication avant de commencer | Rôle, informations demandées, protections réelles, aide et frais Stripe pris en charge par Localeo compris ; commission Localeo distinguée, aucune promesse de garantie absolue |
| E68-CA-04 | Commerçant, exigences documentaires applicables | Consulter les consignes puis préparer les pièces | Liste personnalisée, aide du référent, présentation au rendez-vous ou canal sécurisé existant vérifié ; aucun nouveau dépôt marchand ; réutilisation des preuves valides, à préparer/reçu/vérifié distincts, aucune pièce sensible demandée par email |
| E68-CA-05 | Commerçant/signataire, contrat disponible en amont | Télécharger/imprimer et lire avant J, questionner puis signer le jour J ; gestionnaire déposant la copie après rendez-vous | Accès borné au contrat du commerçant, PDF lisible/imprimable, version identifiée ; consultation/lecture/signature distinctes ; version imprimée contrôlée, copie signée vérifiée avant finalisation, aucun upload marchand ; nouvelle version signalée sans réemploi silencieux de l'accord |
| E68-CA-06 | Commerçant, offre sans coffret possible | Proposer puis corriger une prestation avant J | Brouillon reprenable et soumission identifiable ; aucune publication ni modification silencieuse d'une offre déjà applicable |
| E68-CA-07 | Opérateur habilité, proposition soumise | Examiner avant J la faisabilité et l'économie | Décision sur une version précise, motif et corrections partagés ; accord commerçant sur les conditions traçable ; changement significatif impose un nouvel examen des éléments touchés |
| E68-CA-08 | Référent, risque fiscal ou autre réserve détecté | Préparer le bilan avant rendez-vous | Réserve, responsable et action visibles ; `REVIEW_REQUIRED` n'est pas affiché comme validation favorable ; acceptation d'une prestation distincte de la qualification BUM du coffret |
| E68-CA-09 | Mail/SMS programmés ou envoyés, événements fournisseur reçus ou absents | Consulter les deux suivis dans le dossier puis recueillir la confirmation | Pour chaque canal : destinataire, échéance, tentative, état réel et éventuel échec ; livraison inconnue explicitement distinguée de livrée ; ni ouverture ni silence ne valent réception comprise, rendez-vous confirmé ou absence de question |
| E68-CA-10 | Commerçant ayant une question | La soumettre, recevoir une réponse et confirmer sa résolution | Échange lié au dossier, responsable et état visibles ; nouvelle question possible après « aucune question à ce stade » ; réponse de Localeo seule insuffisante pour conclure |
| E68-CA-11 | Non-réponse, échec email ou préparation incomplète | Appliquer relance et traitement humain | Actions bornées et traçables, échec visible au référent ; pas de relance en double lors d'un rejeu, pas de dossier déclaré prêt par défaut |
| E68-CA-12 | Report, annulation ou rendez-vous rapproché | Modifier le rendez-vous | Même dossier et checklist conservés, échéances relatives à J recalculées et changements visibles ; anciennes relances devenues inutiles neutralisées, preuves encore valides conservées, aucun faux historique de préparation |
| E68-CA-13 | Référent et commerçant, point avant J | Consulter le même récapitulatif partagé | Éléments prêts/manquants, questions et prochaines actions concordants ; maintien adapté ou report motivé ; dossier commerçant et aptitudes commerciales distingués |
| E68-CA-14 | Dossier préparé, rendez-vous tenu | Suivre le déroulé expliqué au commerçant | Quatre phases 10/15/10/25 minutes cohérentes avec mail, support joint et guide ; prestations examinées avant J puis confirmées, prise en main et bilan préservés ; cible de 60 minutes sans suppression d'une vérification obligatoire ; dépassement et cause consignés |
| E68-CA-15 | Commerçant sur son propre appareil | Se connecter et réaliser les gestes de prise en main | Autonomie observée sur scénario représentatif, aide retrouvable ; ni partage de mot de passe ni opération financière réelle de test |
| E68-CA-16 | Fin du rendez-vous ou absence du commerçant, blocages possibles | Consigner l'issue et partager le bilan puis réaliser le suivi | Préparation, issue du rendez-vous et finalisation de l'inscription distinctes ; rendez-vous tenu avec Stripe en attente laissant le dossier à compléter ; reste à faire attribué avec échéance, absence/injoignable sans abandon automatique ni capacité inventée |
| E68-CA-17 | Pilote Localeo, dossiers représentatifs | Mesurer le parcours avant/après à partir du suivi des dossiers | Durée du rendez-vous, temps de gestion backoffice, relances manuelles, préparation avant J, questions et autonomie suivis avec événements et dénominateurs définis ; chiffres inconnus non remplacés par des succès ; bilan pilote du processus, sans produit analytique autonome |
| E68-CA-18 | Opérateur habilité, nouveau commerçant à référencer | Enregistrer le commerçant puis rouvrir sa fiche | Un dossier de préparation rattaché à ce commerçant est disponible sans seconde création manuelle, même sans rendez-vous ; répétition ou modification du profil sans doublon, sans activation ni invitation implicite |
| E68-CA-19 | Référent, dossier ouvert | Planifier le rendez-vous final | Date et heure enregistrées, créneau d'une heure, choix Teams ou physique avec coordonnées correspondantes ; horaire non ambigu et même information dans le dossier et l'invitation ; lien Teams manquant signalé sans bloquer la planification, URL fournie HTTPS et adresse physique obligatoire |
| E68-CA-20 | Référent, dossier avec ou sans rendez-vous | Consulter la checklist puis planifier | Étapes lisibles et prochaine action utile en premier ; envoi, pièces déjà enregistrées, signature et Stripe alimentés depuis leurs sources, actions humaines identifiées sans double saisie ; échéances liées à J après planification, aucune pièce à apporter assimilée à reçue |
| E68-CA-21 | Opérateur habilité, action de préparation | Consigner un échange, examen, blocage ou correction | Actions manuelles réservées aux constats et décisions humains, auteur/date et résultat retrouvables ; aucun commentaire obligatoire pour recopier un résultat automatique ; changement de preuve déclenchant la revue concernée, sans validation manuelle de substitution |
| E68-CA-22 | Référent, plusieurs dossiers à préparer | Consulter et filtrer le suivi backoffice | Dossiers sans rendez-vous, rendez-vous proches, actions en retard et attentes commerçant retrouvables ; ouvrir le même dossier depuis le suivi ou la fiche ; aucune file concurrente ni donnée hors des droits de l'opérateur |
| E68-CA-23 | Rendez-vous complet à venir, délai global configuré en jours calendaires | Atteindre l'échéance puis rejouer le traitement | Pack mail/SMS préparé à J−7 par défaut et restant A_CONFIRMER jusqu'à validation du gestionnaire ; date/heure et fuseau explicites, créneau en journée ; aucun envoi sans autorisation courante, doublon, dérogation par dossier ou émission à la seule création ; retard visible, chevauchement et rattrapage selon règle spécifiée |
| E68-CA-24 | Pack explicitement autorisé, mail pris en charge, en échec confirmé ou incertain | Déterminer le SMS à émettre | Nominal couvert par l'accord du pack après prise en charge mail : date/heure, interlocuteur et adresse destinataire ; secours après échec certain préparé pour confirmation distincte si aucun nominal engagé, sans prétendre le mail envoyé ; aucun SMS sans autorisation courante, incertain sans renvoi aveugle |
| E68-CA-25 | Mail préparatoire avec ou sans prestations, gestionnaire habilité | Prévisualiser puis confirmer explicitement l'envoi du pack mail/SMS | Destinataires email/mobile, contenus, PJ et fenêtre présentés ; fermer/annuler sans envoi, accord tracé auteur/date/versions, double clic idempotent ; rendez-vous/actions prioritaires, entrée vers préparation ; objectif, étapes, rôles et modalités sans promesse d'activation automatique ; prestations connues et manquants explicites, absence sans blocage/tableau vide ; déroulé et présentation Localeo/Stripe joints, frais Stripe/commission distingués ; aucun envoi sans accord ou PJ requise, aucun aperçu ne modifie les preuves ni ne divulgue les notes internes |
| E68-CA-26 | Échec partiel, report/annulation, modification des coordonnées ou du délai | Reprendre ou reprogrammer les communications | Intention, autorisation et contenu figé distincts ; modification des éléments approuvés invalidant l'autorisation avant remise et imposant un nouvel aperçu/accord ; copie exacte conservée, correctif confirmé séparément ; réessai technique du même message sous accord valide, reprise manuelle confirmée, aucun renvoi aveugle ni réémission du mail pour reprendre le SMS |
| E68-CA-27 | Commerçant destinataire du mail préparatoire | Utiliser « J'ai reçu les informations » ou « J'ai une question » | Confirmation explicite datée ou question liée au bon dossier, visible du référent ; simple ouverture du mail ou préchargement d'un lien sans confirmation ne valide rien ; accès limité au dossier autorisé |
| E68-CA-28 | Commerçant, exigences et contrat disponibles | Consulter le mail puis préparer ses éléments | Liste de pièces adaptée et consignes sans dépôt E68 ; contrat courant lisible avant J, questions et lecture conservées dans l'espace ; aucune demande de pièce sensible par email, déclaration de préparation distincte de réception et lecture distincte de signature |
| E68-CA-29 | Commerçant, rendez-vous planifié | Ajouter le `.ics` de confirmation immédiate ou du pack J−7 | Même identité de rendez-vous, date/heure/fuseau, durée et lien/lieu cohérents ; report/annulation avec version actualisée à spécifier/tester, sans synchronisation automatique promise ni seconde identité pour le même rendez-vous |
| E68-CA-30 | Rendez-vous actif à J−1 ou préparation sans confirmation | Préparer le rappel, confirmer son envoi puis suivre les dossiers nécessitant un contact | Rappel bref à J−1 sans supports ni autorisation héritée du pack, validation explicite du gestionnaire requise ; canal/horaire à préciser ; absence de validation d'envoi ou de retour marchand visible avec action attribuée ; rendez-vous annulé ou passé sans rappel, aucune confirmation supposée |
| E68-CA-31 | Opérateur habilité, backend et documentation livrés | Ouvrir le guide depuis la documentation ERP et le dossier onboarding | Guide lisible et versionné décrivant étapes, acteurs, checklist, communications et cas de reprise ; liens fonctionnels et droits préservés, lecture vérifiée avec bundle sans dépôt projet voisin ; aucune copie divergente ni fonctionnalité future présentée comme disponible |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Backend, domaine propriétaire | **Concerné** : cycle et préparation dans le domaine onboarding existant ; identités, documents, communication, référencement/commercialisation et BUM conservent leurs règles. L'application orchestre, les interfaces ne décident pas seules qu'un dossier est prêt |
| ERP / OnBoard / Support | **Concernés** : dossier dès référencement, planification date/heure/Teams ou physique, checklist et suivi des prochaines actions ; réutiliser la fiche et le dossier OnBoard, désigner l'entrée de référence sans multiplier les dossiers ou files concurrentes |
| Application Commerçant | **Concernée** : accès avant activation, checklist, contributions et questions. Les droits actuels profil/Stripe ne suffisent pas : définir des capacités de préparation limitées et les parcours de reprise |
| Marketplace | **À examiner** : réutilisation d'une présentation publique de la plateforme ou de supports existants ; aucun changement de checkout ou de vendabilité demandé |
| Application Animation | **Sans objet pour son interface V1** : aucun parcours partenaire demandé ; non-régression des prestations partagées à vérifier si leurs contrats évoluent |
| API et consommateurs | **Concernés** : producteur backend, consommateurs internes et commerçant ; contrat canonique, états/actions, erreurs, droits, concurrence et compatibilité à spécifier, sans exposer les API internes aux commerçants |
| Persistance, migrations et existant | **À examiner** : liaison unique commerçant/dossier, déclencheur des créations ERP/API/import, rendez-vous et fuseau horaire, actions/responsables/preuves/échéances ; reprise de dossiers ouverts ou clôturés sans créer une seconde préparation ni inventer de lecture/consentement historique ; migration seulement après conception |
| Email, SMS et traitements | **Concernés** : configuration J−7, ordonnanceur, messages liés au rendez-vous, envoi mail avec deux PJ puis SMS informant de cet envoi, suivi fournisseur par canal et reprises idempotentes ; horaires/fuseau, retards, report/annulation et changement de configuration à spécifier ; respecter la [charte email](../../architecture/transverse/charte-emails-localeo.md) |
| Documents et accès | **Concernés** : deux supports pédagogiques joints, fichier `.ics`, liste de pièces personnalisée, contrat versionné et consignes de préparation sans nouveau dépôt marchand ; droits des actions de confirmation/questions, collecte minimale, contrôles et conservation ; aucun document sensible du commerçant joint aux messages |
| Générateur / fixtures | **Concernés** : [EPIC 63](../terminees/epic-63-jeux-demonstration-communes-backlog.md), nouveau commerçant sans rendez-vous, dossier réutilisé sans doublon, Teams/physique, checklist partielle ; échéance configurable, pièces jointes manquantes, mail/SMS en échec partiel ou incertain, événement fournisseur répété, report avant/après envoi, rendez-vous tardif ; questions, contrat changé et Stripe en attente ; génération isolée sans envoi réel |
| Documentation fonctionnelle et publication ERP | **Concernées** : guide opérationnel backoffice à produire avec la spécification, source canonique de formation, entrée documentaire ERP et lien depuis le dossier ; export autorisé, bundle et test du lecteur/recette sur cible ; parcours E50 et aide commerçant à aligner, sans confondre guide interne et supports envoyés |
| Exploitation / livraison | **Concernées** : supervision mail/SMS et dossiers oubliés, réglage du délai/horaires, canaux absents ou invalides, PJ indisponibles, responsable et délai de réponse, activation progressive sans envoi massif aux anciens dossiers ; ordre backend/consommateurs, recette des deux canaux et reprise à définir |

## Questions ouvertes

La [table d'arbitrages de la spécification](../../specifications/epic-68-preparation-onboarding/README.md)
précise les propositions soumises le 2 octobre (calendrier, signature, revue des
prestations) et les contrats désormais conçus. Aucune absence de réponse ne vaut
acceptation. Les paramètres ouverts bloquent uniquement les parties dépendantes.

| Arbitrage | Décision attendue et proposition | Effet sur la spécification |
| --- | --- | --- |
| E68-ARB-01 | **Partiellement résolu : J−7 configurable globalement, jours calendaires et créneau en journée retenus**, sans dérogation par dossier en V1. Préciser fuseau, heures, effet sur les envois en attente et règle de rattrapage/regroupement des messages proches | Programmation prévisible sans SMS nocturne ni rafale ; aucune replanification silencieuse |
| E68-ARB-02 | **Résolu : quatre phases de 10/15/10/25 minutes**, revue des prestations avant J, prise en main et bilan renforcés | Même déroulé dans mail, support, guide et recette chronométrée ; vérifications obligatoires préservées |
| E68-ARB-03 | **Conception détaillée le 2 octobre** : espace existant, scope limité `commercant:preparation`, identité du dossier dérivée de la session, renouvellement contrôlé des anciennes sessions, récupération d'accès et distinction contact/signataire ; API cibles dans la spécification | Réception/questions, consignes de pièces, contrat et propositions accessibles avant activation sans dépôt marchand ni ouverture des droits commerciaux ; reste à implémenter |
| E68-ARB-04 | Fixer qui répond et examine, sous quel délai, et les critères du maintien adapté/report ; proposition de revue à J−2 | Organisation de la file, responsabilités, alertes ; le silence ne vaut jamais confirmation |
| E68-ARB-05 | **Moment de signature décidé le 3 octobre** : PDF téléchargeable/imprimable avant J, signature le jour J, dépôt interne par Localeo après rendez-vous ; pièces conditionnelles selon exigences applicables | Version et habilitation contrôlées ; copie signée reçue/vérifiée avant finalisation, remise à organiser pour Teams ; aucun dépôt marchand ni nouveau fournisseur de signature |
| E68-ARB-06 | Définir la grille de viabilité des prestations, les approbateurs et la frontière avec E62 pour les offres existantes | Modèle/proposition/copie, droits d'édition, critères économiques et traitement des réserves BUM |
| E68-ARB-07 | Deux PJ acquises : déroulé du jour J et présentation boucle Localeo/Stripe vue commerçant ; PDF proposé. Valider rédaction, périmètre exact des frais Stripe pris en charge, protections et limites | Contenus fidèles à la convention, versionnés et lisibles ; ne pas transformer la prise en charge en gratuité universelle de Stripe |
| E68-ARB-08 | Mail + SMS initiaux, rappel J−1 et contact humain en non-confirmation acquis ; préciser canal/horaire du rappel, délai d'escalade humaine, suivi après J et mesure pilote ; point J+2 encore proposé | Éviter les sollicitations inutiles ; rappel sans supports répétés, responsabilités, accessibilité et mesure pilote |
| E68-ARB-09 | **Complété le 3 octobre :** calendrier préparatoire et confirmation explicite avant chaque séquence ; pack mail + SMS nominal validé ensemble à J−7, autres messages/rappel J−1/secours à confirmer distinctement | Accès initial distinct ; autorisation côté serveur, aperçu périmé refusé, aucun envoi par sauvegarde ou silence ; dépendance SMS/mail et absence de doublons préservées |
| E68-ARB-10 | Définir la reprise des commerçants déjà référencés et des dossiers clos ; proposition de conserver les dossiers existants et de proposer une reprise explicite selon leurs droits | Pas de création massive, de réouverture ou d'envoi aux anciens dossiers lors du déploiement ; nouveau référencement et reprise restent distingués |

## Revue critique avant spécification — 1er octobre 2026

**Trace historique :** les références au dépôt marchand dans cette revue décrivent
la conception antérieure. E68-SIMPLIFICATION-20261002 retire ce seul mécanisme en V1 ;
les autres capacités de l'espace et ses contrôles restent au périmètre.

**Conclusion :** le résultat attendu est cohérent, mais les 31 critères couvrent
à la fois le pilotage backoffice, la communication et un parcours commerçant
avant activation. Une checklist et des messages ne suffiront pas à eux seuls.
La conception doit d'abord arrêter les accès, les règles de préparation et les
reprises ; elle ne doit pas multiplier les validations manuelles. Cette revue
ne constitue ni une spécification complète ni une validation des choix ouverts.

### Recommandations retenues par l'utilisateur

Les neuf recommandations suivantes sont validées le 1er octobre 2026. Leur
intention est acquise ; les paramètres encore indiqués dans les arbitrages
et la conception des contrats restent à préciser. Le tableau conserve les
risques qui ont motivé ces décisions.

| Référence | Risque concret | Recommandation et critères concernés |
| --- | --- | --- |
| E68-REV-01 | Dix actions de préparation et une checklist métier peuvent obliger le référent à saisir deux fois le même avancement | Une seule vue de dossier. Les informations connues (envoi, pièce reçue, signature, état Stripe) alimentent la lecture ; les actions manuelles portent uniquement sur les échanges et examens humains. Mettre la prochaine action utile en premier, sans imposer un nouveau commentaire pour chaque donnée déjà prouvée. CA-20/21/22. |
| E68-REV-02 | « Rendez-vous finalisé », « prêt pour le rendez-vous » et « inscription finalisée » peuvent être confondus, surtout si Stripe reste en attente | Définir séparément la préparation du rendez-vous, son issue (tenu, reporté, annulé, absent) et les conditions métier de finalisation. Un rendez-vous tenu peut laisser le dossier à compléter ; pas de clôture de convenance. Définir aussi le traitement d'un commerçant injoignable ou absent, sans abandon automatique. CA-12/13/14/16. |
| E68-REV-03 | Dans le cadrage précédent, un rendez-vous fixé plusieurs semaines à l'avance n'était annoncé avec son calendrier qu'à J−7 | Confirmation légère dès la planification avec `.ics`, puis pack complet mail/SMS à J−7 et rappel J−1. Éviter deux messages équivalents si la planification intervient près de J−7. CA-01/23/29/30. |
| E68-REV-04 | Le SMS est bloqué précisément lorsque le mail n'arrive pas à être envoyé ; le référent hérite de tous ces cas | Conserver le SMS nominal qui annonce le mail après sa prise en charge. Prévoir un SMS de secours distinct après échec confirmé, rappelant le rendez-vous et invitant à vérifier l'adresse ou contacter Localeo, sans annoncer de mail envoyé. Un résultat incertain ne déclenche ni message trompeur ni renvoi automatique ; la reprise humaine reste possible. CA-09/11/24/26. |
| E68-REV-05 | Le commerçant reçoit une liste de choses à faire mais peut ne pas disposer des droits ou d'un accès encore utilisable pour les réaliser | Concevoir en priorité un espace de préparation limité et mobile : réception/questions, pièces, contrat et propositions, avec reprise de l'accès. Distinguer contact opérationnel et signataire ; ne pas assimiler une adresse destinataire à un pouvoir de signature. Articuler le mail d'initialisation d'accès existant avec les communications E68. CA-02/04/05/06/10/27/28. |
| E68-REV-06 | Délai configurable, report, coordonnées modifiées et dossiers sans date peuvent générer des rappels inutiles ou des dossiers oubliés | Réglage global : jours calendaires, fuseau explicite, créneau en journée ; pas de dérogation par dossier en V1. Montrer la date calculée, définir rattrapage et priorité si J−7/J−1 se chevauchent. Avant envoi, contrôler la version du rendez-vous et le destinataire ; les dossiers sans date ont une prochaine action attribuée. CA-18/19/23/26/30. |
| E68-REV-07 | Le mail cumule explication, contrat, pièces, prestations, deux PDF et calendrier ; le commerçant peut ignorer les actions essentielles | Conserver tous les contenus demandés, avec en tête « votre rendez-vous » et les actions à faire, puis les prestations et les supports. Une entrée principale vers la préparation regroupe réception/questions et dépôt. Les deux PDF restent joints ; éviter de demander de tout lire avant de trouver la première action. Prévisualiser le mail réel et ses PJ depuis le dossier, sans permettre de modifier les preuves canoniques. CA-25/27/28/29. |
| E68-REV-08 | Les 20 minutes initialement prévues pour les prestations le jour J risquaient de reporter leur examen au rendez-vous, au détriment de l'autonomie | Faire de la revue avant J un jalon réel, avec maintien adapté ou report décidé par le référent. Répartition retenue : 10 min de questions, 15 min dossier/contrat/Stripe, 10 min de confirmation des prestations et 25 min de prise en main/bilan. Elle remplace le minutage précédent ; la signature et les vérifications sensibles ne sont pas accélérées pour tenir l'heure. CA-07/13/14/15/16. |
| E68-REV-09 | Préparer le mail lors de la planification fige des prestations et coordonnées qui peuvent changer avant J−7 | Distinguer la programmation d'un envoi de son contenu définitif. Fixer le moment où sont figés rendez-vous, destinataire, prestations et supports, puis conserver ce contenu exact. Prévoir l'annulation avant prise en charge et une communication corrective si l'ancien message est déjà parti. La formule « au moment de l'envoi » ne doit pas masquer la course entre modification et fournisseur. CA-12/25/26. |

### Existant vérifié par la revue indépendante de contrats

Lecture du backend `d1a16e8` et de l'application Commerçant `38ff5ad`, sans
connexion externe ni exécution de tests métier :

- **Préparation commerçant :** les
  [droits avant activation](../../../../localeo-backend/app/domaine/identite_acces/acces_portail_commercant.py)
  se limitent à session/profil ; les routes prestations/messages existantes
  demandent d'autres capacités. Le
  [dépôt documentaire OnBoard](../../../../localeo-backend/app/api/onboarding_commercant_api.py)
  est interne et l'[application Commerçant](../../../../localeo-commercant/src/App.jsx)
  intercepte déjà la session de préparation. Une extension explicite des droits,
  du parcours et de son contrat embarqué est nécessaire ; un lien dans le mail
  ne suffit pas.
- **Accès initial :** le
  [référencement](../../../../localeo-backend/app/application/referencement/use_cases/referencer_commercant.py)
  peut préparer son propre email d'initialisation avec un jeton expirant. Le pack
  J−7 doit être articulé avec cet accès, pas le remplacer ou le répéter implicitement.
- **Communications :** les batchs mail et SMS actuels sont indépendants ; la
  dépendance « SMS seulement après mail pris en charge » n'est pas acquise par
  leur seule réutilisation. Le
  [modèle d'email sortant](../../../../localeo-backend/app/domaine/exploitation/entities/email_sortant.py)
  contient déjà le corps et les PJ matérialisés : E68 doit préciser la programmation,
  le figement des versions et le déclencheur du SMS.
- **Guide ERP :** le
  [lecteur documentaire](../../../../localeo-backend/app/infrastructure/documentation.py)
  n'autorise que les documents du manifeste. CA-31 couvre déjà le besoin ; conserver
  comme preuves distinctes rédaction, export, accès depuis l'ERP et lecture dans
  l'artefact déployé. Ce n'est pas un nouveau manque fonctionnel du cadrage.

### Frontières à préserver dans la conception

La préparation du rendez-vous doit être portée par les règles du dossier
OnBoard ; la communication orchestre les canaux et leurs retours fournisseur.
Les documents, habilitations, droits commerçant, capacités Stripe et prestations
restent dans leurs domaines respectifs. L'ERP présente leurs résultats sans
fabriquer une seconde validation ni exposer ses API internes au commerçant.

Le [domaine OnBoard actuel](../../../../localeo-backend/app/domaine/conformite_fiscale_bum/onboarding.py)
porte déjà les transitions `PRET_A_VALIDER`, `VALIDE` et `CLOTURE`, ainsi qu'une
progression acquise et des capacités détaillées. La progression acquise ne suffit
donc pas à dire « prêt pour le rendez-vous » après changement d'une preuve.
La revue des prestations reste distincte des capacités nécessaires à l'inscription :
le socle autorise un commerçant sans prestation rattachée à un coffret.

### Paramètres et contrats à préciser en premier

1. **Accès de préparation et signataire** (E68-ARB-03/05) : où le commerçant
   confirme, dépose et corrige, et comment il récupère un accès expiré.
2. **Prérequis du rendez-vous et définition de la fin** (E68-ARB-04/06) : ce
   qui doit être examiné avant J, ce qui permet un maintien adapté et ce qui
   laisse le dossier à compléter après le rendez-vous ; critères de signature.
3. **Chronologie et incidents de communication** (E68-ARB-01/08) : heure,
   rattrapage, absence de confirmation, report et coordination des messages proches.
   La confirmation immédiate, le pack J−7 configurable et le SMS de secours
   sont retenus ; préciser leurs contrats d'exécution et de reprise.

Les autres décisions (mise en page des PDF, libellés, ordre détaillé des écrans)
peuvent avancer en parallèle. Le guide backoffice et les deux supports doivent
être rédigés pendant la conception : ils serviront aussi à vérifier que le
processus peut être expliqué simplement. Conserver les trois lots proposés,
sans présenter le premier comme l'implémentation de toute l'EPIC.

### Preuves à prévoir pour les points challengés

| Scénario | Propriétaire et preuve attendue |
| --- | --- |
| Rendez-vous tenu avec validation Stripe encore en attente ; pièce modifiée après revue | Domaine OnBoard : préparation du rendez-vous distincte de finalisation ; résultat observable « actions restantes », aucune capacité inventée. |
| Commerçant avant activation, lien d'accès expiré, autre commerçant ou autre signataire | Identité/accès + application : accès limité, reprise et refus hors périmètre ; recette mobile du parcours réellement autorisé. |
| Report ou changement de contact pendant un envoi ; fournisseur accepte puis connexion perdue ; événement reçu deux fois | OnBoard + communication : version vérifiée, issue incertaine conservée, rapprochement et reprise sans envoi aveugle ; tests de concurrence et des deux canaux. |
| Création après J−7, rendez-vous le lendemain, rappel J−1 proche du pack, dossier sans date | Politique de calendrier : cas de retard, changement d'heure et priorité entre messages, aucune rafale ni échéance fictive. |
| Confirmation immédiate puis pack ; mail en échec confirmé, incertain ou rejeté après SMS nominal | Communication : invitation calendrier cohérente, pas de doublon équivalent ; secours sans fausse annonce d'envoi, nominal suspendu en cas d'incertitude et reprise humaine si déjà envoyé ; tentatives bornées. |
| Mail comportant plusieurs prestations, PJ et calendrier ; guide dans l'ERP | Recette du contenu réel sur mobile, traces des versions et cohérence date/heure/modalité ; lecture documentaire via le bundle livré. |
| Même portefeuille de dossiers avant/après | CA-17 : mesurer aussi le temps de gestion Localeo par dossier et le nombre de relances manuelles ; une heure de rendez-vous ne prouve pas à elle seule un processus plus efficace. |

Les scénarios de cette table sont **à produire**, pas exécutés dans cette revue.
Les champs, DTO, migrations, permissions précises et stratégie d'idempotence
restent à spécifier à partir des producteurs et consommateurs réels.

## Historique du cadrage

- **3 octobre 2026 — consolidation documentaire V1.2** : spécifications limitées
  au processus courant en sept étapes ; guide, communications et recette alignés.
  Anciennes décisions et preuves conservées uniquement dans ce backlog ; les
  31 critères et arbitrages métier encore ouverts restent inchangés.

- **3 octobre 2026 — E68-PROCESSUS-20261003, V1.2** : recentrage demandé sur
  la mise en place du seul processus d'onboarding convenu. Synthèse en sept
  étapes, limites et socles à réutiliser explicités ; 31 critères conservés
  et rattachés au parcours (CA-01 clarifié, CA-17 borné au bilan pilote).
  Les garanties d'envoi, l'espace sans dépôt, la signature jour J et le dépôt
  interne après rendez-vous restent acquis. Documentation seulement, état À faire.

- **3 octobre 2026 — E68-CONFIRMATION-ENVOIS-20261003** : demande utilisateur
  de confirmation explicite pour éviter les erreurs d'envoi. Échéances conservées
  mais communications en attente d'une validation humaine par séquence ; pack
  mail/SMS validé ensemble. CA-23/24/25/26/30 et preuves associées précisés ;
  guides, contrats cibles et reprise alignés. Changement documentaire, sans code
  ni migration exécutés ; les autorisations existantes ne sont jamais présumées.

- **3 octobre 2026 — E68-CONTRAT-JJ-20261003** : contrat téléchargeable et
  imprimable pour lecture avant J, signature le jour J, puis dépôt de la copie
  signée par le gestionnaire Localeo après le rendez-vous. Moment de signature
  ARB-05 décidé ; CA-05 et preuve T05 précisés, guides et mail alignés. Pas de
  nouvelle API d'upload marchand ni de finalisation sans contrôles actuels.

- **2 octobre 2026 — E68-SIMPLIFICATION-20261002, V1.1** : demande de simplicité
  et précision utilisateur « retirer uniquement le dépôt de pièces ». Espace
  réception/questions/contrat/prestations conservé ; dépôt/API/stockage marchand
  de pièces différés. CA-02/04/20/28 et supports alignés, sans clôture ou code.

- **2 octobre 2026 — E68-SPEC-20261002** : spécification V1.0, cartographie des
  producteurs et consommateurs, règles de préparation/finalisation, API cibles,
  concurrence des envois et reprise, matrice CA-01 à 31. Guide backoffice et deux
  supports rédigés/exportables ; accès ERP et PDF restent à réaliser. Paramètres
  de calendrier, signature, grille de revue, diffusion des supports et reprise
  historique distingués des décisions déjà acquises. Statut À faire conservé.

- **30 septembre 2026** : parcours partagé, préparation avant J, dix-sept critères
  et hypothèses de calendrier/déroulé.
- **1er octobre 2026 — E68-PILOTAGE-20261001** : le référencement initial devient
  le point de départ ; dossier avant planification, rendez-vous final Teams ou
  physique d'une heure, checklist et suivi backoffice. E68-CA-01/12 précisés,
  E68-CA-18 à 22 ajoutés. Les besoins de contribution du commerçant sont conservés.
  Le démarrage du dossier n'est plus un arbitrage de délai avant J ; les hypothèses
  J−7/J−10, le contenu des phases et les modalités de communication restent ouvertes.
- **1er octobre 2026 — E68-COMMUNICATIONS-20261001** : mail + SMS automatiques
  à J−7 configurable, suivi séparé dans le dossier, deux supports joints au mail.
  Remplace l'hypothèse de choix J−7/J−10 et l'envoi manuel proposé précédemment ;
  E68-ARB-01 partiellement résolu, E68-ARB-09 résolu, E68-CA-23 à 26 ajoutés.
  Aucun envoi réel ni création de supports exécutables à cette phase de cadrage.
- **1er octobre 2026 — E68-ACCOMPAGNEMENT-20261001** : les quatre compléments
  proposés dans la synthèse sont acceptés ; guide backoffice publié dans l'ERP
  ajouté aux livrables attendus de spécification/livraison. E68-CA-27 à 31 ajoutés.
  Le canal/horaire du rappel et les délais du contact humain restent à préciser.
- **1er octobre 2026 — rappel des prestations** : le mail préparatoire inclut
  le détail des prestations déjà saisies dans le dossier lorsqu'elles existent,
  pour relecture avant J. E68-CA-25 complété ; aucune prestation requise pour
  envoyer le mail et aucune validation commerciale déduite du récapitulatif.
- **1er octobre 2026 — explication du rendez-vous final** : objectif, déroulement,
  rôles, matériel utile et bilan attendu explicités dans le corps du mail, avec
  cohérence entre ce résumé, la pièce jointe et le guide backoffice. E68-CA-14/25
  précisés ; le découpage proposé en quatre phases reste à arrêter.
- **1er octobre 2026 — revue critique avant spécification** : neuf recommandations
  E68-REV-01 à 09, revue indépendante des contrats et priorisation des décisions.
  À cette étape de revue, les 31 critères et décisions acquises sont conservés ;
  les ajouts sont soumis à validation explicite, obtenue dans l'entrée suivante.
- **1er octobre 2026 — E68-DECISIONS-20261001** : l'utilisateur retient les neuf
  recommandations E68-REV-01 à 09. Parcours et critères alignés : états alimentés
  automatiquement, préparation/issue du rendez-vous/finalisation distinctes,
  confirmation immédiate avec calendrier, SMS de secours, accès limité avec reprise,
  réglage global, mail hiérarchisé et prévisualisable, figement traçable des contenus.
  Le minutage 10/15/10/25 remplace 10/15/20/15 ; temps de gestion et relances manuelles
  rejoignent la mesure pilote. Les 31 identifiants de critères restent stables.
  Horaires, contrats et arbitrages explicitement ouverts restent à spécifier.

### Compléments retenus le 1er octobre 2026

- Un bouton **« J'ai reçu les informations »**, puis **« J'ai une question »**,
  pour rendre la confirmation explicite et simple depuis le mail, selon les
  droits d'accès de préparation à définir.
- Une liste de pièces **personnalisée dans le corps du mail**, avec liens de
  dépôt sécurisé, et le contrat accessible à l'avance pour laisser du temps
  à la lecture ; éviter de multiplier les PJ ou de demander un retour de pièces
  sensibles par email.
- Un fichier **calendrier `.ics`** pour ajouter le rendez-vous, son lien Teams
  ou son adresse ; ce fichier s'ajoute aux deux supports pédagogiques et ne
  constitue pas une synchronisation Microsoft/agenda.
- Un rappel bref **à J−1**, sans renvoyer tous les supports, uniquement si le
  rendez-vous est toujours actif ; canal et horaire à préciser.
- Une action de **contact humain en cas d'échec ou d'absence de confirmation**,
  prioritaire dans la checklist, avec responsable et résultat consigné.

Le rattrapage des rendez-vous pris à moins de sept jours reste à préciser selon
E68-ARB-01 ; le point de suivi J+2 reste une proposition. Ces délais ne sont pas
fixés par la validation des recommandations. Les quatre phases de 10/15/10/25
minutes sont en revanche retenues dans E68-ARB-02.

## Passage à la spécification

Le besoin, les acteurs et les critères sont cadrés. La prochaine phase doit
décrire le parcours de bout en bout, les écrans et messages, les états et preuves,
les responsabilités et contrats, puis relier chaque critère aux scénarios de
réussite, refus, absence de réponse et reprise. Produire aussi le guide backoffice
et prévoir explicitement son accès dans l'ERP, ses exports et sa recette. Suivre le
[cycle d'epic](../../organisation/cycle-epic.md).

La spécification sera reliée à ce backlog et à l'index canonique lorsqu'elle
existera ; aucun dossier de conception vide ni contrat API hypothétique n'est
créé ici. Les arbitrages ci-dessus bloquent seulement les choix qui en dépendent.
Ce cadrage n'a déclenché aucun email, aucune modification applicative, ni aucun
déploiement.

## Archive des contrôles documentaires antérieurs à la consolidation V1.2

Ces résultats sont conservés pour traçabilité. Ils décrivent les sources au moment
indiqué et ne prouvent pas la version consolidée courante ni une implémentation.

#### Contrôles consignés avant consolidation

Les chiffres ci-dessous retracent les contrôles **V1.0**, antérieurs au recadrage.
Ils ne prouvent pas la V1.1 ni les fonctions reportées. Les nouveaux contrôles
documentaires du recadrage sont consignés séparément ci-dessous.

- Lecture des producteurs et consommateurs aux versions backend `33face6` et
  Commerçant `38ff5ad`, avec explorations indépendantes dossier et canaux.
- Rédaction de la spécification, du guide et des deux sources publiques ; aucune
  génération PDF de ces supports ni recette de leur rendu n'est encore réalisée.
- Revue indépendante `localeo-contract-reviewer` réalisée : accord marchand sur
  les conditions ajouté comme commande distincte ; idempotence des nouvelles
  mutations distinguée des anciennes entrées sans corps ; route de préparation
  ACTIF explicitée. Politique globale et qualification des questions précisées.
- `check_guidance.py` : **90 guides, 939 liens, 0 erreur, 0 avertissement**.
- `check_guidance.py --changed --all-markdown` : **12 documents, 141 liens,
  0 erreur, 0 avertissement** lors du contrôle initial des nouveaux documents.
- `sync_documentation.py --check-sources` : **122 sources vérifiées**. Bundle
  local ignoré `.artifacts/epic68-specification/documentation` préparé puis contrôlé
  par `--check` ; contrôle backend du snapshot : **123 documents distribués et
  sources canoniques vérifiés** (manifeste inclus).
- Lecteur réel `resolve_ops_document`, racine explicitement fixée à ce bundle :
  **3 alias E68 lus avec succès** (guide, déroulé, Localeo/Stripe), sans import
  de l'application ni chargement des paramètres d'exploitation. Ce test ne prouve
  ni la future route ERP ni ses droits, à vérifier lors de l'implémentation.

#### Contrôles du recadrage V1.1 — 2 octobre 2026

- Backlog, spécifications, guide ERP, sources des supports et index alignés sur
  l'arbitrage : seul le dépôt marchand de pièces est différé. Les confirmations,
  questions, lecture du contrat et préparation des prestations sont conservées.
- `check_guidance.py --document` sur le backlog : **91 guides, 972 liens,
  0 erreur, 0 avertissement** ; `--changed --all-markdown` : **16 documents,
  284 liens, 0 erreur, 0 avertissement**.
- `sync_documentation.py --check-sources` : **122 sources vérifiées** ; nouveau
  bundle local ignoré `.artifacts/epic68-simplification/documentation` généré puis
  contrôlé avec `--check` : **122 documents vérifiés**.
- Contrôleur backend du snapshot : **123 documents distribués et sources
  canoniques vérifiés** ; lecteur réel `resolve_ops_document` : **3 alias E68
  lus avec succès**, racine fixée au nouveau bundle, sans charger l'application.
- `git diff --check` : succès. Aucun code applicatif ni migration modifié pour
  ce recadrage documentaire ; aucun test métier exécuté ou déclaré réussi.

#### Décision contrat — 3 octobre 2026

`E68-CONTRAT-JJ-20261003` précise CA-05/T05 : téléchargement et impression avant J,
signature le jour J, dépôt interne après rendez-vous. Backlog, parcours,
architecture, mail et guides alignés ; aucun code ni migration modifié.
Contrôles exécutés : `check_guidance.py --document` sur le backlog, **91 guides,
972 liens, 0 erreur, 0 avertissement** ; `sync_documentation.py --check-sources`,
**122 sources vérifiées** ; `git diff --check`, succès. Le rendu du PDF contractuel
et les scénarios T05 restent à tester à l'implémentation ; les bundles contrôlés
le 2 octobre sont antérieurs à cette décision et devront être régénérés à la livraison.

#### Confirmation des envois — 3 octobre 2026

`E68-CONFIRMATION-ENVOIS-20261003` remplace l'envoi à échéance par la préparation
d'une séquence à confirmer explicitement. CA-23/24/25/26/30, contrats cibles,
guide ERP, messages et index alignés. Revue indépendante en lecture seule :
aucune contradiction bloquante repérée ; deux compléments de couverture intégrés
à T01/T12 et T26. Aucun code ni migration exécutés.
`check_guidance.py --document` : **91 guides, 972 liens, 0 erreur, 0 avertissement** ;
`sync_documentation.py --check-sources` : **122 sources vérifiées**. Les bundles
historiques doivent être régénérés à la livraison. Les scénarios d'autorisation
et de concurrence sont des preuves à produire à l'implémentation.

#### Recentrage sur le processus — 3 octobre 2026, V1.2

`E68-PROCESSUS-20261003` rattache les 31 critères au seul parcours d'onboarding.
CA-01 explicite la confirmation d'envoi déjà acquise ; CA-17 reste une mesure du
pilote sans produit analytique autonome. La recette complète ci-dessus relie
les étapes, les socles à réutiliser et les contrôles à préserver.
Backlog, spécifications, guide ERP et index alignés. Aucun code, contrat OpenAPI
exécutable, migration ou générateur modifié dans ce recadrage documentaire ;
leurs impacts de réalisation restent suivis dans la matrice et la recette.
Contrôles exécutés : backlog **91 guides, 972 liens, 0 erreur, 0 avertissement** ;
documents modifiés **16 guides, 284 liens, 0 erreur, 0 avertissement** ; exports
**122 sources vérifiées** ; `git diff --check`, succès. Les sources ont évolué
depuis les bundles historiques : les régénérer avant livraison. Ces contrôles
ne prouvent aucune fonction applicative ni disponibilité du parcours déployé.

Les tests métier de la matrice restent non exécutés. L'epic conserve son statut
**À faire** ; le dossier distingue les parties conçues des arbitrages encore ouverts.


## Évolution E68-EVOL-20261008-ADMIN — rubrique Administration OnBoard

Décision utilisateur du 8 octobre 2026 : déplacer « Réglages pour tous les
commerçants (administrateur) » dans une rubrique **Administration** dédiée de
Localeo OnBoard, et retirer cette section de toutes les vues individuelles.
Le placement précédent dans chaque dossier est remplacé ; les réglages restent
globaux et réservés à l’administrateur existant. Le statut **En cours** et les
critères E68-CA-01 à 31 sont conservés.

| Critère ajouté | Contexte et action | Résultat attendu |
| --- | --- | --- |
| E68-CA-32 | Administrateur dans OnBoard, avec ou sans dossier ; ouvrir Administration, régler puis revenir aux dossiers | Rubrique autonome accessible directement et après rechargement, aucun réglage ni chargement de politique dans les vues commerçants. Autres profils exclus, y compris accès direct. Aperçu des impacts, motif, version et confirmation explicite conservés ; saisie modifiée ou réponse tardive ne valide pas un ancien aperçu. Aucun envoi de message par simple navigation ou sauvegarde des réglages. |

Les CA-23, 25 et 26 gardent leurs règles de calendrier, autorisation et concurrence.
La [spécification](../../specifications/epic-68-preparation-onboarding/README.md)
et le [bilan dédié](../../specifications/epic-68-preparation-onboarding/verification-livraison.md)
portent l’implémentation et ses preuves. Aucun nouveau rôle, contrat API, paramètre
métier ni changement de données n’est demandé.
