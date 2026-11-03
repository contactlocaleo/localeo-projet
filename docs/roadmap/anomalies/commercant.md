# Registre des anomalies

## Diagnostic du 3 novembre 2026 — récupération sans accès Pro initialisé sur TEST

- **Signalement** : une demande de mot de passe oublié ne produit aucun e-mail
  visible dans l’ERP. Lecture seule sur TEST : le commerce est actif et possède
  une adresse de contact, mais aucune ligne d’identifiant commerçant. Les demandes
  de récupération sont bien enregistrées, sans blocage de débit ni e-mail de reset.
- **Cause** : une adresse de contact n’est pas automatiquement un login Pro.
  Le parcours public répond volontairement de façon générique pour un login
  inconnu, sans créer de compte, token ou e-mail. Le `+` de l’adresse est conservé
  par le formulaire JSON déployé ; l’origine API TEST est correcte.
- **Traitement** : ERP → fiche du commerce → Accès → Envoyer le lien
  d’initialisation. Cette commande crée le premier identifiant et place l’e-mail
  d’initialisation dans la file. L’utilisateur a choisi de l’effectuer lui-même :
  aucune initialisation, modification de mot de passe ou émission d’e-mail exécutée.
- **Preuves** : 27 tests backend isolés réussis dans
  `test_identite_acces_use_cases.py` et `test_acces_preparation_password_api.py` ;
  7 tests Pro réussis dans `api.test.js` et `passwordResetReturn.test.js`.
  Ces tests ne prouvent pas une livraison d’e-mail réel après initialisation.
- **Impacts** : diagnostic de configuration d’accès ; aucun correctif applicatif,
  contrat, migration, générateur ou déploiement nécessaire pour ce cas. Conserver
  la réponse publique neutre afin de ne pas révéler l’existence d’un compte.

## Correction du 1er novembre 2026 — invitation salarié et aide au mot de passe

Signalement : revoir `/salaries/invitation` et reprendre la politique commune
d'initialisation du mot de passe. Version distante non précisée ; reproduction
locale sur la base Commerçant `a946ee2`. La page ne présentait aucune règle et
envoyait une saisie de moins de 12 caractères au serveur. La jauge commune
présentait à tort des classes de caractères obligatoires et validait l'absence
du login même lorsqu'il était inconnu. La politique serveur était déjà partagée.

Correction locale : cadre Localeo Pro, étapes Invitation / Mot de passe /
Connexion, commerce et destinataire masqué, expiration explicite, affichage ou
masquage de la saisie, aide commune à la longueur et messages de refus utiles.
La jauge ne certifie plus une robustesse globale. La longueur minimale affichée
reste la valeur commune de 12 caractères ; les exigences configurées et les
refus de mots courants ou de fragments du login restent vérifiés par le serveur.
Les erreurs 409 de politique reconnues permettent une correction. La résolution
temporairement indisponible se réessaie ; une mutation incertaine ne se rejoue
pas. Lien invalide sans formulaire, succès distinct et connexion explicite.
Le jeton reste dans le corps JSON, l'URL et la session sont nettoyées.

Preuves : reproduction Vitest rouge avant correction pour la saisie trop courte,
puis **27 tests Vitest réussis** (`PublicEmployeeAccess`, `EmployeeAccess`) et
**13 scénarios Playwright réussis** (`employee-invitation-ux`, `employees`).
Rendus inspectés à 320, 390 et 1280 px, texte à 200 %, sans débordement horizontal.
Audit axe sans violation sur l'invitation, son succès, le lien expiré et l'aide
commune de l'initialisation principale. Le contrôle a révélé un contraste
insuffisant dans cette aide ; il passe après correction. Build isolé réussi,
API simulées, aucun email réel. Captures dans
`localeo-commercant/tmp/employee-invitation-ux/`.

Revue backend indépendante : **29 tests existants réussis** via
`scripts/validation/test_isolated.py` : service de politique, gestion du mot de
passe Animation, initialisation/réinitialisation commerçant et API salariés E72.
Les orchestrations emploient des doubles ; aucune recette PostgreSQL ni rejeu
sur TEST n'a été réalisé. La revue frontend indépendante n'a relevé aucun défaut
de nettoyage, de session ou de rejeu des mutations dans les fichiers concernés.

Impacts : interface Commerçant et documentation canonique d'authentification.
Aucune modification de règle serveur, contrat API, permission, schéma, migration,
générateur de démonstration ou configuration d'exploitation. La limite technique
bcrypt de 72 octets, explicitement traitée par Animation mais pas par les services
commerçant/salarié, n'est pas modifiée par cette harmonisation de l'aide.
Aucun commit, push ou déploiement dans cette intervention.

## Correction du 1er novembre 2026 — ergonomie des accès salariés

Signalement : la page **Accès salariés** de Localeo Pro manque de repères
visuels et de hiérarchie. Version distante non précisée ; reproduction locale
sur la base Commerçant `a946ee2`, route `/salaries`, compte principal autorisé.
L'ancien écran réutilisait les styles étroits du PIN, affichait les codes API
bruts et juxtaposait invitations et révocation.

Correction locale : en-tête de gestion commun, formulaire d'invitation distinct,
liste structurée sur toute la largeur, pictogrammes et badges avec libellés,
états d'invitation et d'envoi séparés, expiration lisible, actions regroupées
et pagination par flèches nommées. L'état du compte reste distinct de
`acces_effectif` fourni par le serveur. Les valeurs inconnues restent neutres.
L'option inactive désactive aussi la saisie ; les révocations restent possibles.
Les confirmations contextuelles, le retour du focus, les versions et le blocage
après réponse incertaine sont conservés.

Preuves locales : reproduction navigateur échouant avant correction sur le
libellé « Invitation expirée », puis **21 tests Vitest** réussis
(`EmployeeManagement` et `EmployeeAccess`) et **10 scénarios Playwright** réussis
(`employee-management-ux` et `employee-confirmation`). Couverture : liste longue,
email long, option inactive, état vide, compte activé mais accès indisponible,
invitation expirée, échec d'envoi, révocation, renvoi et annulation avec focus
clavier et une seule commande. Rendu inspecté à 320, 390 et 1280 px, texte
agrandi à 200 % sur 320 px, absence de débordement horizontal et audit axe sans
violation sur la page. Build navigateur isolé réussi, API simulées, aucun envoi
réel. Captures locales dans `localeo-commercant/tmp/employee-management-ux/`.

Impacts : présentation Commerçant et ce suivi uniquement ; aucun changement
de contrat API, droit, règle métier, schéma, migration, générateur de
démonstration ou configuration d'exploitation. Les styles sont isolés dans
`EmployeeManagement.module.css`, avec réutilisation de `BusinessWorkspace`
et `StatusBadge`. Aucun commit, push ou déploiement dans cette intervention ;
rejeu sur TEST après livraison non effectué.

## ANO-COM-E73-INVITATION-DECISION — Accès à la réponse commerçant

Signalement du **30 octobre 2026** sur TEST : absence du bouton de validation
pour **L'Escale Douce / Test passeport TCA**. L'écran observé dans Localeo Pro
`1.0.0+dbf6f52e` est `/animations/99527546-96eb-4a76-9a4b-b88db26ef12a`,
avec retour Notifications, dates du 1 au 9 novembre et kit indisponible.
Le contrôle visuel a été interrompu par Échap ; aucune acceptation ou autre
mutation métier n'a été effectuée sur TEST. Le détail API individuel de la
demande et son échéance n'ont pas été lus.

Trois écarts reproduits localement dans `localeo-commercant`, base `dbf6f52` :

- Le backend expose le lien de notification dans `action_cible`, ignoré par
  le frontend. Le repli ouvre la fiche animation au lieu de la demande.
- Une fiche animation répond déjà 200 lorsqu'une invitation est en attente,
  avec `demande_participation.id` et son statut. Le frontend n'ouvrait la
  demande que sur 404 et affichait sinon la mission et le kit sans décision.
- Une échéance ISO enregistrée à minuit était considérée comme dépassée par
  le navigateur, même si le serveur autorisait encore la réponse. Le domaine
  `DemandeParticipationCommercant` conserve la validité jusqu'à la fin du
  jour de Paris ; ses actions et son indicateur explicite font autorité.

Correction locale : lecture de `action_cible`, conversion des liens historiques
`/animations/invitations/{id}` vers le parcours existant, ouverture de la demande
sur une fiche 200 `EN_ATTENTE`, respect de l'échéance serveur et secours
calendaire Europe/Paris lorsque cet indicateur est absent. Les notifications
historiques de flyer `/animations/{id}/flyer` ouvrent la fiche animation,
qui porte le flyer ; la revue a détecté et corrigé ce cas avant livraison.
Le bouton existant **Accepter la participation** conserve l'accord explicite,
l'idempotence et les refus du serveur.

Quatre reproductions échouent avant correction pour les liens de notification,
la fiche 200 et l'échéance ISO. Le test de flyer ajouté après revue échoue aussi
avant son adaptation. Les tests couvrent les changements été/hiver, les refus
explicites, les réponses incertaines et l'absence de décision avant clic.

Validation : **187 tests Vitest réussis** (Animation, dates et contrat embarqué),
**15 scénarios Playwright réussis** (9 de parcours/invitation dont 6 à 390/1280 px,
6 de flyer dont mobile/bureau), build navigateur isolé réussi et
**22 tests backend existants réussis** pour la décision et l'espace Animation,
via le lanceur isolé. Aucun appel réel du backend dans ces recettes automatisées.
Guides et 130 sources exportées validés, `git diff --check` réussi dans les deux
dépôts touchés.

Périmètre : interface Commerçant et ce suivi canonique. Aucun changement du
backend, de contrat API, de droits, de règle métier, de schéma, migration,
participation ou générateur requis. La spécification E56 du consentement reste
applicable. Correction enregistrée dans le commit Commerçant `7e6b008`, à la
demande de l'utilisateur. **Déploiement et rejeu sur TEST restant à vérifier** ;
aucune acceptation métier effectuée sur TEST.

## ALL
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-COM-01 | Invitation |sur la vue liste des demandes d'invitation, la commune et la date sont marqués "Non renseignés" alors qu'ils le sont das la backoffice| A corriger |
| ANO-COM-02 | Notification |la fonctionnalité "Marquer tout lu" ne fonctionne pas , l'état n'est pas persisté| A corriger |
| ANO-COM-03 | Notification |Le descrptif de la notification comporte des erreurs d'accent notament sur la description de la misttion | A corriger |

## Correction du 29 septembre 2026 — icônes PWA

- Attendu : utiliser le marqueur Localeo Pro de la même famille graphique que Live/OnBoard pour l'installation de Commerçant.
- Cause : les fichiers `public/icon-192.png` et `public/icon-512.png` contenaient encore l'ancien écusson, contrairement au favicon et au logo source.
- Correction locale : génération des deux icônes transparentes depuis `public/localeo-pro-icon.png` ; ajout d'une icône Apple 180 sur fond blanc et de sa référence HTML. Export reproductible via `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/export-pwa-icons.ps1`.
- Preuves : contrôle visuel de l'export Apple, dimensions et transparence des trois exports ; build isolé `node scripts/build-browser-tests.mjs` réussi. Le manifeste conserve les mêmes chemins d'icônes 192/512.
- Impact limité aux ressources statiques et à leur export : aucun contrat API, règle métier, migration ou générateur de démonstration modifié. Déploiement et vérification sur appareils iOS/Android non effectués ; le renouvellement des icônes déjà installées dépend du système.
