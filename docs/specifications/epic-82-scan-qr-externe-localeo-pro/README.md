# EPIC 82 — Scanner un QR client depuis l’appareil photo avec Localeo Pro

Spécification fonctionnelle et technique du 24 novembre 2026. Le [backlog E82](../../roadmap/terminees/epic-82-scan-qr-externe-localeo-pro-backlog.md) porte les critères d’acceptation. La [roadmap commune](../../roadmap/README.md) porte l’état produit. [Clôture et preuves](#clôture-sur-test-le-24-novembre-2026)

## Périmètre et décisions

Au comptoir, le client présente son QR sur un écran ou un support imprimé. Le responsable ou le salarié habilité peut utiliser l’appareil photo du téléphone ou un lecteur de QR pour ouvrir directement l’action dans Localeo Pro. Le scanner de Localeo Pro reste utilisable avec la caméra et la saisie manuelle.

Avant E82, les QR de coffret et de bon numérique contiennent un jeton brut. Le QR du participant contient un lien vers sa participation dans Live. Le scanner Pro reconnaît ces trois formats. E82 ajoute un lien Pro aux nouveaux visuels, tout en gardant ces formats utilisables dans **Scanner**.

| Décision validée | Comportement retenu |
| --- | --- |
| Supports concernés | Coffrets, QR personnels de participants à une animation et bons numériques. Les affiches d’inscription et les QR de lieu continuent de servir aux parcours publics et aux jeux. |
| Destination | Une page de Localeo Pro dans le navigateur mobile suffit. Le téléphone peut proposer la PWA installée. L’ouverture dépend du lecteur et du choix du commerçant sur le téléphone. |
| Geste métier | L’analyse démarre automatiquement après contrôle de la session et connexion éventuelle. Le commerçant vérifie le contenu et confirme explicitement la prestation, le passage ou la remise. |
| Entrée historique | **Scanner** garde le démarrage caméra, la saisie ou le collage de l’identifiant et les actions habituelles. Il reconnaît les anciens QR et les nouveaux liens Pro. |

## Parcours fonctionnels

### Depuis l’appareil photo ou un lecteur QR

1. Le commerçant scanne le QR du client et ouvre le lien proposé par son téléphone. Pro arrive sur `/validation`, récupère la valeur et nettoie l’adresse. Pro utilise la valeur lue par le téléphone, sans solliciter sa propre caméra.
2. Pro vérifie la session et le droit au scanner. Si la session est absente ou expirée avant l’analyse, Pro affiche la connexion. Une authentification réussie reprend l’analyse sur le même écran après vérification des droits. Si la vérification de session est temporairement indisponible, l’écran propose de la relancer.
3. Pro prépare une fois la validation et présente le résultat. L’analyse d’un coffret ouvre le contexte de cette instance et présente les prestations disponibles pour le commerce. L’analyse d’un participant présente l’animation et son étape pour le commerce. L’analyse d’un bon présente le lot entier et l’état de sa remise.
4. Le commerçant confirme l’action proposée. Pour un coffret qui contient plusieurs prestations, il choisit celle qu’il vient de fournir. Une autre prestation requiert un nouveau scan selon le fonctionnement Coffret. La réussite s’affiche après confirmation du serveur.

### Depuis Scanner dans Localeo Pro

Ouvrir **Scanner** démarre la caméra selon le parcours habituel du profil. Le commerçant peut saisir ou coller l’identifiant si la caméra est refusée, indisponible ou si le QR est difficile à lire. Les formats historiques et le nouveau lien Pro aboutissent aux mêmes étapes d’analyse et de confirmation. Un QR distribué avant l’activation reste valable dans ce scanner selon les règles de validité habituelles. Pour disposer du lien direct, le client peut réafficher ou régénérer le visuel sur un support qui le permet.

### Refus, interruption et deuxième scan

| Situation | Résultat attendu |
| --- | --- |
| Format de lien invalide ou lien Pro d’une autre origine saisi dans le scanner | Pro rejette le lien localement, indique de rescanner et laisse le parcours manuel accessible. Aucune requête de préparation pour ce lien. Les formats historiques du participant suivent leur liste d’origines existante. |
| Salarié révoqué, session de préparation seule ou droit scanner absent | Seule une session habilitée peut préparer la validation. Une session invalide repasse par le contrôle de connexion. Si la session est valide et dépourvue du droit d’accès, Pro abandonne le QR en attente. |
| QR inconnu, expiré, révoqué, remplacé ou hors périmètre du commerce | Pro présente l’état ou le refus fourni par la préparation serveur et une action de reprise appropriée. Aucune confirmation ne peut être obtenue pour une ressource ou un commerce non autorisé. |
| Prestation déjà validée, passage déjà attesté ou bon déjà remis | Pro affiche l’état ou le résultat fourni par le serveur. La lecture d’un QR ou la répétition d’une confirmation ne produit pas un deuxième effet. |
| Quitter le parcours, recharger, se déconnecter ou changer de compte | Une valeur en attente dans la page est abandonnée. Une connexion après perte de ce contexte reprend la destination autorisée selon les règles habituelles. Pour réanalyser ce QR, le commerçant le présente à nouveau. |
| Perte de réponse après confirmation, ou nouvelle arrivée pendant une confirmation en cours | Pro donne la priorité à la vérification du résultat précédent. Il invite à rescanner le nouveau QR après résolution. Une lecture de reçu, un rafraîchissement ou une reconnexion ne rejoue pas la confirmation. Pour un salarié, un reçu Animation `404 COMMANDE_NON_ENREGISTREE` clôt la vérification et permet un nouveau scan explicite. Un `404` portant un autre code conserve l’incertitude. |
| Nouveau lien alors qu’un QR est affiché sans confirmation lancée | Le nouveau lien peut remplacer le contexte affiché. Une préparation déjà en cours se termine avant la suivante. |

## Invariants et responsabilités

| Invariant | Propriétaire et effet observable |
| --- | --- |
| Le QR identifie une cible et la session authentifie l’acteur. | Le backend vérifie la session, le commerce, les droits du responsable ou du salarié puis les conditions propres au QR à chaque opération qui le requiert. Les permissions de préparation et de confirmation sont contrôlées selon les capacités existantes. Pro choisit le parcours d’affichage et ne peut étendre ce périmètre. [Accès salariés](../epic-72-acces-salaries/architecture-contrats.md) |
| La préparation est distincte de la confirmation. | Exploitation ouvre une transaction temporaire pour un coffret. Animation résout l’étape du participant ou prépare le contexte temporaire du bon. Ces opérations ne valident aucune prestation, ne comptent aucun passage et ne remettent aucun lot. |
| Une confirmation s’applique à une seule cible selon ses règles métier. | Exploitation assure l’unicité de la validation active par prestation, selon les règles de transaction et d’annulation existantes. Animation conserve l’attestation, la progression et l’idempotence selon le moteur. L’agrégat `BonLot` garantit une consommation intégrale unique, y compris face à une validation PIN concurrente. L’audit et le reçu des commandes existantes font foi. [Coffrets et validation](../validation-prestations/contrats-api.md), [validations Animation](../epic-56-validation-participation-commercants-animation/README.md), [bons et remise](../epic-73-animation-et-ou-coffrets/dotation-lots.md) |
| Une réponse manquante laisse l’effet indéterminé. | Pro suspend la confirmation suivante et relit le résultat de la transaction, de l’attestation ou de la remise selon le profil et la famille. Les garde-fous transactionnels et les clés d’idempotence existants protègent le serveur contre la concurrence. [Fiabilité E80](../epic-80-fiabilite-parcours-localeo-pro/README.md) |

## Contrats et compatibilité

### Lien optique

```text
https://<origine-pro>/validation#qr=<jeton encodé>
```

- Le backend encode le jeton métier existant avec l’encodage en pourcentage. `LOCALEO_FRONT_COMMERCANT_SCAN_ORIGIN` donne l’origine HTTPS de Pro pour la cible. Une valeur vide produit les contenus historiques.
- Pro accepte le chemin exact `/validation` sur sa propre origine, avec un unique fragment `#qr=` et sans paramètres de requête ni identifiants d’URL. Pro décode le fragment une fois. La valeur décodée compte de 20 à 4 096 caractères et utilise l’alphabet des jetons pris en charge. Les services appliquent ensuite les limites de leur famille. Le HTTP sur l’interface locale sert aux tests isolés.
- À l’arrivée initiale, Pro remplace l’adresse par `/validation` avant le routage. Une arrivée dans un onglet ouvert nettoie de la même façon le lien entrant. Le QR reste en mémoire jusqu’à sa prise en charge. Le fragment optique constitue une entrée de navigation ponctuelle. Les règles de reprise E80 s’appliquent après son retrait. Le jeton reste exclu du chemin et de la requête HTTP, des journaux, de la télémétrie et des stockages navigateur. Les données de reprise existantes conservent les références de transaction ou de reçu, selon leur contrat. [PRO-005](../validation-prestations/scan-commercant.md)

### Producteurs et consommateurs

| Famille | Rendu backend consommé | Valeur historique et autres accès |
| --- | --- | --- |
| Coffret | SVG de consultation autorisée utilisé dans Marketplace et Live, carte cadeau et export, SVG d’impression, PNG de référence, QR embarqué dans les emails Coffret. Le lien E82 s’applique aux QR de validation valides. | Le champ `qr_token` et l’identifiant copié gardent leur valeur brute. La consultation, le lien d’impression et la validation PIN gardent leurs entrées distinctes. Les rendus techniques ERP gardent leur format. |
| Participant | PNG du QR personnel de la participation dans Live et de la route historique, QR embarqué dans les emails de participation. | Les liens personnels ouvrent toujours Live. Live copie le jeton de la participation qu’il détient déjà. La réponse PNG livre uniquement l’image. Le scanner traite aussi les anciens liens participant issus d’une origine autorisée. |
| Bon numérique | `qr_image_svg` du bon personnel présenté dans Live. | Le jeton versionné `bon_lot.v1.…` reste utilisé pour la préparation. La remise par PIN reste accessible via son parcours dédié. |

Le format optique change à la génération du visuel. Les images et emails déjà distribués conservent les valeurs qu’ils encodent. Le jeton est sensible, notamment pour le participant, dont le jeton protège aussi sa consultation dans Live. Le droit d’agir dans Pro vient toujours de la session professionnelle.

### Frontière API

Les deux entrées Pro s’appuient sur les mêmes routes protégées, avec le Bearer de session et le scope `commercant:validation`. Le backend produit le [contrat OpenAPI canonique](../epic-41-api/openapi.json) avec `scripts/documentation/generate_epic41_openapi.py`. Pro utilise `api/localeo-openapi.json`, généré par `scripts/export-openapi.py`. Le lien optique n’étant pas une entrée HTTP, son ajout ne change pas les schémas OpenAPI.

| Famille | Préparation, chemins sous `/protected` | Confirmation et reprise |
| --- | --- | --- |
| Coffret | `POST /exploitation/validation/ouvrir-transaction` avec `qr_coffret_instance` dans le corps JSON. | `POST /exploitation/validation/valider-prestation` avec `transaction_id` et `statut_prestation_coffret_instance_id` en paramètres. Le salarié relit `GET /exploitation/validation/transactions/{transaction_id}/resultat`. Le responsable relit le détail et les prestations de l’instance Coffret. |
| Participant | `POST /animation-locale/commercants/me/participants/resoudre` avec `qr_token` dans le corps JSON. | `POST /animation-locale/validations` avec le jeton et l’étape dans le corps, les versions attendues et `Idempotency-Key`. Relecture par `GET /animation-locale/commercants/me/participants/{participant_id}/attestations/commandes/{cle}`. |
| Bon numérique | `POST /exploitation/bons-lots/scans` avec `qr_token` dans le corps JSON. | `POST /exploitation/bons-lots/{bon_id}/consommations` avec le contexte, la version attendue et `Idempotency-Key`. Relecture par `GET /exploitation/bons-lots/operations/{operation_id}`. |

## Données, coût et mise en service

- E82 réutilise les jetons, les droits et les données existants. La configuration change l’encodage à la génération. Elle ne déclenche pas de rotation de jetons, de migration de base, de régénération des anciens supports ou d’adaptation du générateur de démonstration. Les preuves locales utilisent des QR et comptes fictifs.
- Une ouverture directe prépare au plus une fois l’action. Elle réutilise les lectures et écritures du scanner pour cette opération. Le rendu encode une valeur déjà chargée sans nouvelle requête en base. Les contrôles portent sur la préparation unique, le décodage des supports et le poids de l’email. Les volumes de trafic sur cible restent à observer lors de la recette, selon la [convention de performance](../../architecture/transverse/performance-volumetrie.md).
- Livrer le scanner Pro compatible avant l’activation du nouveau rendu. Commencer par TEST, vérifier iPhone et Android, puis décider de l’activation sur les autres cibles. Un retour à une origine vide rétablit le format historique pour les nouveaux rendus. Garder Pro compatible pour les QR au nouveau format déjà distribués. [Procédure d’activation E82](../../exploitation/deploiement/commercant/mise-en-production.md#activer-le-scan-depuis-lappareil-photo--e82)

## Traçabilité et recette

| Critère | Propriétaire et preuve locale consignée | Protocole de recette TEST et impacts |
| --- | --- | --- |
| E82-CA-01 | Pro. Playwright couvre caméra simulée et saisie pour les trois familles et les deux profils. | Employer des anciens et nouveaux QR avec caméra réelle et vérifier la saisie sans caméra. Guide Commerçant, chapitre 3. |
| E82-CA-02, CA-03 | Pro et accès backend. Playwright couvre les trois familles et les deux profils, sessions active, absente et expirée. | Ouvrir les liens depuis les lecteurs des deux téléphones et confirmer la reprise de destination après connexion. |
| E82-CA-04 | Domaines Exploitation et Animation. Playwright distingue la préparation de la confirmation et vérifie la sélection Coffret. | Contrôler l’action côté commerce et l’état client associé après confirmation explicite. |
| E82-CA-05 | Backend et reprise dans Pro. Tests locaux de refus, de retrait du droit de scanner, de priorité du reçu et du résultat Animation absent pour un salarié. | Recetter mauvais commerce, QR expiré ou remplacé, deuxième scan et perte de réponse. Vérifier le reçu avant un éventuel réessai. |
| E82-CA-06 | Pro et backend. Tests du parseur, du retrait du fragment, de l’origine et du corps HTTP. | Contrôler l’adresse dans Pro et l’absence du jeton dans les journaux de la cible de recette. |
| E82-CA-07 | Backend, Marketplace et Live. Tests de rendu et décodage synthétique. Compatibilité de certains parcours Marketplace à confirmer. | Tester écran, email et impression suivant le support disponible, outils iOS et Android, ainsi que les liens Live, identifiants copiables et PIN. Guide Commerçant, chapitres 3 et 4. |

Le [guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md) et sa copie embarquée couvrent les deux façons de scanner. Le [guide Animation](../../produit/formation/animation/guide-quotidien-animation.md) présente les gestes organisateur, la diffusion des supports publics et le suivi de remise. Le nouveau point d’entrée concerne le commerçant dans Pro et ne modifie aucune de ces consignes organisateur.

La recette navigateur de référence est [external-qr.spec.js](../../../../localeo-commercant/tests/e2e/external-qr.spec.js). Côté backend, [test_qr_api.py](../../../../localeo-backend/tests/api/test_qr_api.py), [test_presentation_qr_participant.py](../../../../localeo-backend/tests/application/animation_locale/test_presentation_qr_participant.py) et [test_service_preparation_email.py](../../../../localeo-backend/tests/application/services/test_service_preparation_email.py) couvrent les rendus et la séparation des usages. Ces preuves locales ne remplacent pas la recette d’activation.

### Bilan local du 24 novembre 2026 — historique de l’implémentation

- **Pro.** 93 tests Vitest ciblés et 54 tests Playwright réussis, dont 37 scénarios E82 et 17 scénarios existants. Le parcours direct est couvert pour les trois familles, les deux profils et les sessions active, absente ou expirée. Le scanner historique, le rejet d’une origine étrangère, le refus de droits, le nettoyage du fragment et la priorité du reçu sont vérifiés avec caméra et API simulées. Le build isolé est réussi. Deux tests de préparation ont dépassé le délai par défaut sous charge avant de réussir lors de la passe ciblée avec un délai de 15 secondes.
- **Backend.** 131 tests isolés réussis sur le rendu, les emails, les routes QR, la consultation et la confidentialité. Les trois contenus optiques synthétiques sont décodés à l’identique par ZXing. Une capture de l’email Coffret dans Chromium à 390 px décode aussi le lien exact. Le balisage des cellules a été compacté en conservant les dimensions, les couleurs et la marge du QR. L’exemple à dix prestations pèse 96 974 octets après ce changement.
- **Guide.** Capture de la prestation après arrivée par le lien, rendu et relecture des 14 pages, copie vérifiée à l’octet. Le lien Aide et contact livre le PDF à 390 et 1440 px malgré l’indisponibilité simulée de l’assistance. Contrôle Axe réussi sur ces deux vues.
- **Marketplace et Live.** La suite de compatibilité sur réponses simulées a obtenu 17 réussites sur 28. Les 11 échecs concernent des scénarios existants de copie d’identifiants, de lien participant, d’ouverture du QR ou d’affichage du bon. L’impression du QR, le lien fragment et la saisie historique de la page d’impression passent. Le dépôt Marketplace est vierge de changement E82 et la suite ne contacte pas le backend modifié. Ces échecs laissent la compatibilité de ces parcours à confirmer en recette intégrée.
- **Documentation.** Les liens ciblés E82 et les 155 sources exportées sont vérifiés. Le contrôle global des documents modifiés signale deux captures manquantes dans un chantier parallèle du guide Animation.
- **Activation.** La recette physique iPhone et Android, les clients de messagerie et l’activation par environnement restent à vérifier. Les résultats locaux ne qualifient pas le matériel ni l’hébergement cible.

### Complément d’implémentation E82-CA-05

Le scanner salarié attendait un statut `ABSENTE` dans une réponse réussie. Le serveur retourne en pratique `404 COMMANDE_NON_ENREGISTREE` lorsque la commande est absente et `202 EN_COURS` si elle est toujours en cours. Pro distingue désormais ce `404` métier d’un autre refus. Il efface les références de reprise après le constat d’absence, affiche le résultat et permet de rescanner. La reprise exige un nouveau geste. [Route de relecture](../../../../localeo-backend/app/api/merchant_animation_scan_api.py), [parcours salarié](../../../../localeo-commercant/src/features/employees/EmployeeScanner.jsx)

- **Pro.** Le test du `404` métier reproduit le blocage avant correction. Après correction, 95 tests Vitest ciblés et 57 scénarios Playwright passent, dont le nouveau scan explicite après constat de l’absence du reçu. Un `404` portant un autre code conserve le reçu en attente. Le cas de reprise a également été rejoué avec un UUID et une clé de commande de forme contractuelle.
- **Backend.** 141 tests isolés réussis pour cette passe. Les contrôles couvrent le rendu des trois familles, le mode historique par défaut et les réponses `404` et `202` de la route de relecture avec une unité de travail en mémoire.
- **Marketplace et Live.** Treize scénarios ciblés réussis sur les parcours actuels, dont l’impression, la copie, l’affichage du QR Passeport, l’ouverture d’un coffret et le PIN. La relecture des échecs historiques a identifié des attentes d’interface ou des fixtures décalées des parcours actuels. Les tests utilisent des réponses simulées.
- **Guides.** Le correctif réutilise le message de relecture et le bouton de nouveau scan déjà présents pour un résultat non confirmé. Le guide Commerçant décrit déjà ces gestes et sa copie PDF a été vérifiée. Le guide Animation concerne les gestes de l’organisateur et ne décrit pas ce traitement du reçu. Aucun impact sur les contrats HTTP, les migrations ou les données de démonstration.

### Clôture sur TEST le 24 novembre 2026

**E82-DEC-CLOTURE-TEST** · Le porteur produit confirme dans la conversation avoir validé E82 en tests et demande sa clôture. Le statut **Terminée** s’appuie sur cette validation globale sur TEST et sur les preuves locales des sept critères ci-dessus. Les scénarios détaillés, les appareils et les références des artefacts déployés sur TEST n’ont pas été communiqués dans cette confirmation.

- Les sources E82 sont poussées sur `main` dans Projet (`65bad04`), Localeo Pro (`0a0864e`) et Backend (`2c0b082`). Ces SHA identifient les versions de référence du code et de la documentation.
- Les vérifications locales portent sur les deux entrées, les trois familles de QR, les deux profils, la confirmation et la reprise du reçu. Le PDF du guide Commerçant de la révision E82 compte 13 pages et sa copie embarquée est identique. Le guide Animation conserve les gestes de l’organisateur.
- La promotion DEMO et PROD suivra une livraison distincte. Les TARGET backend locaux contiennent l’origine de Pro propre à chaque environnement. Livrer Pro compatible avant d’appliquer la valeur du backend. Contrôler ensuite le scan direct, l’ancien scanner et la reprise du reçu sur la cible. E82 réutilise les contrats, les migrations et les accès existants. Pour revenir au rendu historique, redéployer le backend de la cible avec une valeur vide. [Procédure d’activation et de retour arrière](../../exploitation/deploiement/commercant/mise-en-production.md#activer-le-scan-depuis-lappareil-photo--e82)
