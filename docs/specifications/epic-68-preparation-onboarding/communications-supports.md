# E68 — Communications du processus d'onboarding en sept étapes

Spécification **V1.2 — 3 octobre 2026**. Textes cibles à intégrer et approuver
avant diffusion ; aucun modèle déployé ni envoi attesté. Les règles de figement,
d'autorisation et de reprise sont dans l'[architecture](architecture-contrats.md).

## Communications par étape

| Étape | Message ou support et action attendue |
| --- | --- |
| 1. Référencer et ouvrir le dossier | Aucun message E68 implicite ; l'invitation d'identité existante reste un parcours distinct |
| 2. Planifier le rendez-vous | Email léger et ICS, aperçu puis confirmation explicite par le gestionnaire |
| 3. Préparer et confirmer les communications | Pack J−7 : mail avec deux supports, prestations et accès préparation ; SMS nominal autorisé avec le pack, remis après acceptation certaine du mail |
| 4. Accompagner la préparation | Questions/réponses et confirmations dans le même compte ; contrat PDF téléchargeable pour lecture/impression, sans upload marchand |
| 5. Faire le point avant J | Rappel J−1 à confirmer distinctement ; report/annulation/secours avec leur propre confirmation |
| 6. Conduire le rendez-vous | Support du déroulé 10/15/10/25 ; signature du contrat jour J et pratique |
| 7. Enregistrer et finaliser | Bilan partagé sans notes internes ; actions restantes datées, sans nouveau message automatique J+2 |

**Confirmation explicite avant envoi.** Les modèles de
ce document sont préparés à leur échéance mais restent « À confirmer » jusqu'à
validation explicite par un gestionnaire Localeo habilité, après aperçu exact
des destinataires, contenus, PJ et fenêtre d'envoi. Une validation couvre le
pack mail et son SMS nominal ; les confirmations de rendez-vous, rappels,
secours et avis correctifs ont chacun leur validation. Les conditions fournisseur
du SMS restent nécessaires après cette autorisation. La planification, l'aperçu
et le silence ne déclenchent aucun envoi. Toute modification pertinente exige
un nouvel aperçu et une nouvelle confirmation avant remise.

## Enveloppe et données

Réutiliser `render_email` et la charte email Localeo : version HTML et texte,
variables échappées, bouton principal unique, lecture mobile et sans images.
L'action principale ouvre l'espace de préparation ; email et téléphone restent
des moyens d'aide sans remplacer les confirmations authentifiées du commerçant.
Expéditeur et réponse utilisent la configuration autorisée de l'environnement.
Afficher le nom du référent et un contact Localeo validé ; aucun téléphone privé
de collaborateur déduit automatiquement. Les valeurs ci-dessous sont des variables
de rendu, jamais du texte à envoyer littéralement.

Avant figement, valider : nom commerçant, date/heure/fuseau, référent, modalité
et lien ou lieu, contacts destinataires et réponse, URL de préparation HTTPS de
l'environnement, liste des pièces à préparer, contrat accessible ou réserve explicite,
prestations existantes et deux supports approuvés. Une adresse/ligne SMS manquante
produit une action de correction ; elle n'est pas inventée. L'absence de SMS
n'empêche pas le mail valide, mais reste un incident visible.

Rendu des prestations : nom, description, valeur/prix renseigné, durée ou quantité,
conditions/réservation/restrictions connues, état de préparation et champs à
compléter. Chaque ligne est rattachée à sa version. Ne pas joindre notes internes,
analyse de marge interne, pièces d'identité, coordonnées bancaires, identifiants
de connexion ou secret d'initialisation. Les données manquantes affichent
« à compléter » ; zéro prestation remplace le tableau par une phrase explicite.

## Étape 2 — Confirmation légère après planification

**Objet :** Votre rendez-vous Localeo du {{date}} à {{heure}}

> Bonjour {{prenom_ou_nom}},
>
> Votre rendez-vous pour finaliser votre inscription Localeo est prévu le
> {{date}} à {{heure}} ({{fuseau_affiche}}), pour une durée d'une heure, avec
> {{referent_localeo}}.
>
> {{bloc_teams_ou_adresse}}
>
> Vous recevrez avant le rendez-vous les explications et éléments à préparer.
> Vous pouvez déjà accéder à votre espace de préparation et nous poser vos questions.
>
> **Accéder à ma préparation** — {{url_preparation}}
>
> Le fichier calendrier joint permet d'ajouter ce rendez-vous à votre agenda.
> Pour un changement ou une difficulté d'accès : {{contact_localeo}}.
>
> L'équipe Localeo

PJ : calendrier uniquement. Si le pack est dû au même créneau selon la politique
de regroupement, envoyer le pack seul avec le calendrier, sans confirmation en doublon.

## Étape 3 — Pack préparatoire

Le pack est prévu à J−7, selon le délai global configurable. Le rappel J−1 est
conservé ; les horaires précis et règles de regroupement suivent les arbitrages
de calendrier documentés dans l'architecture.

**Objet :** Préparons votre rendez-vous Localeo du {{date}}

> Bonjour {{prenom_ou_nom}},
>
> Nous vous retrouvons le **{{date}} à {{heure}} ({{fuseau_affiche}})** pendant
> **une heure**, avec **{{referent_localeo}}**, pour finaliser votre inscription.
>
> {{bloc_teams_ou_adresse}}
>
> **Avant notre rendez-vous**
>
> 1. Confirmez dans votre espace que vous avez reçu ces informations et indiquez
>    vos questions, même si votre dossier n'est pas encore complet.
> 2. Vérifiez les informations de votre établissement et préparez les pièces
>    demandées ci-dessous. Votre référent précise comment les présenter au
>    rendez-vous ou les faire vérifier par un canal sécurisé existant adapté.
> 3. Téléchargez votre contrat en PDF dans votre espace. Vous pouvez l'imprimer
>    pour le lire avant le rendez-vous et préparer vos questions. Vérifiez les prestations récapitulées
>    ci-dessous ; vous pouvez préparer vos propositions et confirmer les conditions
>    examinées avec votre référent dans votre espace.
>
> **Accéder à ma préparation** — {{url_preparation}}
>
> **Ce que vous devez préparer**
>
> {{liste_personnalisee_pieces_avec_etat_et_consigne}}
>
> {{bloc_contrat_courant_ou_indisponibilite_et_action_localeo}}
>
> Nous prévoyons de signer le contrat ensemble le jour du rendez-vous, après vos
> questions. Localeo enregistrera ensuite la copie signée ; aucun dépôt de fichier
> n'est demandé dans votre espace. Si vous ne pouvez pas imprimer ou si une
> autre personne doit signer pour votre établissement, signalez-le à votre référent.
> Ne nous envoyez pas de mot de passe, de coordonnées bancaires ou de justificatifs
> d'identité par réponse à cet email. Les informations demandées par Stripe se
> renseignent chez Stripe, depuis l'accès existant dans votre profil Localeo.
>
> **Vos prestations à vérifier**
>
> {{recapitulatif_prestations_ou_absence}}
>
> Ce rappel reprend les informations connues lors de cet envoi. Les points
> « à compléter » restent à examiner avec vous ; cet email ne publie pas vos offres.
>
> **Comment se déroule l'heure ensemble ?**
>
> - 10 minutes pour répondre à vos questions et préciser vos attentes.
> - 15 minutes pour vérifier votre dossier, le contrat et l'avancement Stripe.
> - 10 minutes pour confirmer les prestations examinées en amont, s'il y en a.
> - 25 minutes pour pratiquer sur la plateforme et faire le bilan des prochaines étapes.
>
> Si une vérification reste nécessaire, nous noterons ensemble l'action et son
> responsable. Une réunion terminée ne signifie pas que tous les contrôles sont terminés.
>
> **Comprendre Localeo et Stripe**
>
> Localeo vous permet de proposer vos prestations dans des coffrets et de suivre
> leur utilisation. Stripe intervient dans le traitement des paiements et des
> reversements. Dans le parcours Localeo prévu par votre convention, les frais
> Stripe sont pris en charge par Localeo ; ils sont à distinguer de la commission
> Localeo convenue avec vous. Le support joint précise ce rôle et les points à vérifier.
>
> **Documents joints** : le déroulé du rendez-vous, la présentation Localeo/Stripe
> et le fichier calendrier. Les points essentiels sont aussi dans cet email.
>
> Une question ? Ajoutez-la dans votre espace. Pour une aide ou un imprévu,
> répondez à ce mail ou appelez {{contact_localeo}}.
> Vous pouvez nous poser une question à tout moment, même après avoir confirmé la réception.
>
> L'équipe Localeo

Variante zéro prestation : « Aucune prestation n'est encore saisie. Vous pouvez
préparer vos propositions dans votre espace ; cela ne bloque pas la préparation de votre
inscription. Nous définirons avec vous la suite adaptée. »

Variante contrat indisponible : « Votre contrat n'est pas encore disponible.
Votre référent doit organiser sa consultation avant le rendez-vous ; aucune lecture ni signature ne
vous est demandée tant que vous ne pouvez pas consulter la bonne version. »
Ce cas crée une tâche et peut empêcher la préparation complète ; il ne fabrique
pas un contrat ni un lien vers une ancienne version.

Le pack joint obligatoirement les deux supports PDF approuvés et l'ICS de la
version du rendez-vous. Le contrat se consulte et se télécharge en PDF pour
impression dans l'espace de préparation ; signature prévue le jour J et dépôt
interne de la copie signée par Localeo après le rendez-vous ;
les pièces sensibles ne sont pas jointes aux emails. La V1.2 exclut le dépôt et
la gestion des pièces dans ce portail. Contrôler la taille totale selon la limite réelle de
l'adaptateur email ; une PJ trop volumineuse bloque avec diagnostic, pas de lien
public en substitution silencieuse.

## Étapes 3 et 5 — SMS

**Nominal, uniquement après acceptation certaine du pack mail :**

> Localeo : RDV le {{date_courte}} à {{heure}} avec {{referent_court}}.
> Un mail a été envoyé à {{email}} avec les étapes et les éléments à préparer.
> Question : {{contact_court}}.

**Secours, échec mail définitif confirmé et aucun nominal engagé :**

> Localeo : RDV le {{date_courte}} à {{heure}} avec {{referent_court}}.
> Nous n'avons pas pu vous transmettre le mail de préparation.
> Merci de vérifier votre adresse avec nous : {{contact_court}}.

**Rappel J−1, canal SMS retenu en ARB-08 :**

> Localeo : rappel de votre RDV demain {{date_courte}} à {{heure}} avec
> {{referent_court}}, {{modalite_courte}}. Un imprévu ? {{contact_court}}.

Ne pas tronquer l'adresse email ou le nom en données trompeuses pour tenir dans
un SMS. Prévisualiser le nombre de segments et la limite réelle du fournisseur,
avec cas accents, email long et longs noms ; refus de rendu excessif avec action
humaine. Aucun nouveau raccourcisseur de lien ou jeton d'accès dans les SMS V1.2.
Un numéro absent/invalide ou un SMS en issue inconnue reste visible dans le dossier.

## Étape 5 — Report et annulation

Report : « Votre rendez-vous Localeo est déplacé au {{nouvelle_date}} à
{{nouvelle_heure}} avec {{referent}}. {{modalite}}. Le calendrier joint remplace
le précédent. Vos échanges et contributions sont conservés ; consultez votre
préparation pour les éléments à actualiser. Votre référent suit les pièces déjà reçues. »

Annulation : « Le rendez-vous Localeo du {{ancienne_date}} à {{ancienne_heure}}
est annulé. Votre dossier reste suivi par {{referent}}. {{prochaine_action_partagee}}.
Le calendrier joint indique cette annulation ; vérifiez sa prise en compte dans
votre agenda. »

Ces avis sont des emails correctifs tracés. Si un pack courant les remplace par
regroupement, son en-tête mentionne explicitement le changement. L'absence ou
l'échec du canal email déclenche une action humaine ; pas de SMS supplémentaire
automatique en dehors des intentions définies.

## Étape 4 — Suivre les réponses

La réception du pack, la déclaration de lecture du contrat et l'accord sur les
conditions d'une prestation sont des actions authentifiées du commerçant,
rattachées à leur version. Ouvrir un lien ou recevoir un retour technique email
ne réalise aucune de ces actions. Le commerçant pose ses questions dans le fil
partagé, confirme leur résolution ou les rouvre ; une réponse du référent ne les
ferme pas automatiquement. « Aucune question pour le moment » autorise un nouvel échange.

Si le référent recueille un retour par email ou téléphone, il consigne la date,
le canal et la source dans le dossier. Cette note reste un compte rendu attribué
à son auteur ; elle ne remplace ni l'action authentifiée du commerçant ni sa
signature et ne fabrique aucune preuve de compréhension.

## Sources des pièces jointes et approbation

Les deux sources publiques sont séparées du présent document interne :

- [Votre rendez-vous de finalisation](../../produit/formation/commercant/preparation-rendez-vous-localeo.md).
- [Comprendre la boucle Localeo et Stripe](../../produit/formation/commercant/comprendre-localeo-stripe.md).

Le backend devra générer leurs PDF depuis ces sources canoniques exportées,
avec une version/empreinte et statut d'approbation. Aucun moteur de génération
n'est ajouté au dépôt documentaire. L'approbation concerne le contenu destiné
au commerçant ; ne jamais envoyer ce document de spécification à sa place.
Le marquage « projet » des sources ne sera retiré qu'après validation éditoriale.
Avant activation : vérifier rendu mobile/impression, texte extractible, absence
de débordement et de note interne, cohérence avec les conditions réellement applicables.

La prise en charge des frais n'est pas une promesse de gratuité universelle de
Stripe. Ni le mail ni la PJ ne garantissent absence de contestation, paiement
irrévocable, disponibilité immédiate des fonds ou validation immédiate du compte.
