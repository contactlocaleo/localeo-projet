# Illustrations du guide quotidien commerçant

## 22 novembre 2026 - iconographie de gestion

Douze captures ont été reprises sur un build synthétique de Pro, base
`643a90a` avec la nouvelle iconographie. Les vues d'accueil et de préparation
illustrent les parcours décrits dans cette édition. La recette utilise
`scripts/build-browser-tests.mjs` et `scripts/capture-merchant-guide.mjs`,
avec un dossier de sortie isolé et des données fictives.

## Ajout du 22 novembre 2026 - étapes invalides de Vitrines et Juste Prix

Le chapitre 4 explique qu'une étape invalide après épuisement des essais ne
peut pas être rattrapée par scan ou PIN. Les captures existantes montrent les
lots, la préparation et les validations habituelles, dont les écrans et gestes
restent identiques : aucune de ces captures n'est affectée. Leur provenance
ci-dessous est conservée. Le texte de la page 4 est resserré pour garder des
caractères lisibles et les **douze pages**, sans modifier les autres procédures.

Depuis `localeo-commercant` :

```powershell
py -3.14 scripts/generate-merchant-guide.py --preview-dir tmp/attempts-guides-merchant-pdf
npm run guide:sync
npm run guide:check
$env:LOCALEO_TEST_DIST = 'tmp/attempts-guides-build-merchant'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/attempts-guides-build-merchant --check-guide --verify-only
```

Les douze pages ont été rendues et relues, avec inspection détaillée de la
page 4. La copie embarquée est identique au PDF canonique. La recette sur le
port 4181 a réussi à 390 et 1440 px : navigation, focus clavier, HTTP 200,
contenu du PDF, guide disponible malgré l'assistance en erreur et aucune
violation Axe. Le manifeste de vérification est
`localeo-commercant/tmp/guide-refresh-merchant-capture/verification.json`.
Il s'agit d'une preuve locale sur build synthétique, base `036aea6`, sans
déploiement distant ni compte réel. Les points d'accès aux guides sont inchangés.

## Édition du 22 novembre 2026

Le [guide source](../../guide-quotidien-commercant.md) conserve **12 chapitres**.
Cette édition actualise le suivi de préparation : liste des animations actives
ou historiques, état et acteur de la prochaine tâche, frise et distinction entre
étape consultée et préparation confirmée. Les captures concernées sont produites
depuis le frontend React, base Git `294393f` avec les modifications locales de
ce correctif. La version synthétique affiche `v1.0.0+browser-` : il s’agit d’une
recette locale, sans déploiement.

Les écrans ont été ouverts dans Chromium avec des API simulées et le commerce fictif **La Maison des Saveurs**. Le navigateur utilise l’heure de Paris et une horloge fixée au 22 novembre 2026. Les requêtes externes sont bloquées ; aucun compte réel, secret, QR personnel réel ou jeu de données installé n’est utilisé. Les invitations, montants, salariés et réponses de jeu sont des exemples fabriqués pour la formation. Aucune action métier réelle n’est exécutée.

Les captures sont réalisées directement dans l’application, sans redessiner ses écrans ni modifier ses libellés. Le script recadre la zone utile ou capture un composant entier afin de garder le texte lisible dans le PDF. Le viewport principal est de 1100 × 900 pixels, avec un facteur de pixels de 1,5.

| Fichier actuel | Vue illustrée dans le guide |
| --- | --- |
| `01-accueil.png` | Préparations de l’accueil : actions à terminer et attentes de l’organisateur |
| `02-validation.png` | Prestation de coffret à valider et action de confirmation |
| `05-horaires.png` | Page publique chargée : statut du brouillon, complétion et accroche |
| `08-activite.png` | Indicateurs d’activité : achats, réalisations et montants |
| `11-facturation.png` | Demande de facture : brut TTC, commission, net et état |
| `12-invitations.png` | Invitation en attente avec organisateur, dates et échéance de réponse |
| `13-guide-aide.png` | Guide PDF accessible dans Aide et contact |
| `14-lot.png` | Lot entier, commerce de remise, validité et confirmation de remise |
| `16-preparation.png` | Animation en cours, préparation confirmée datée et finalisation terminée |
| `17-vitrines.png` | Relecture Vitrines : contenu public et réponse privée fictive |
| `18-reglages.png` | État des notifications sur cet appareil et actualisation |
| `19-equipe.png` | Accès salarié : compte, accès effectif, invitation et révocation |

Les options Stripe, facturation, Chorus Pro, assistant d’émission, salariés et PIN sont présentées dans le texte comme dépendantes des droits et services disponibles. Une capture d’exemple ne prouve pas leur activation sur un environnement réel. La capture de réglages montre le cas où les notifications sont bloquées ; le guide explique aussi les autres états.

## Régénération et vérifications

Le complément du **22 novembre 2026** sur les préparations actualise les captures
`01-accueil.png` et `16-preparation.png` depuis la base Pro `643a90a` avec les
modifications locales du correctif. La première montre les vues **À préparer ou
terminer** et **En attente de l’organisateur**, ainsi que la première tâche ; la
seconde distingue **Animation : En cours**, **Préparation : confirmée**, la date
de déclaration et la finalisation **Terminée**. Les sources Commerçant sont
actualisées dans la même livraison. Le guide Animation ne change pas : aucune
procédure ni aucun écran de son application n’est modifié par ce complément.

Pour recapturer uniquement ces deux vues, utiliser le build isolé
`tmp/guide-preparations-status-dist`, puis
`node scripts/capture-merchant-guide.mjs --dist tmp/guide-preparations-status-dist --only 01-accueil,16-preparation`.
Les paramètres de triage et de pagination sont appliqués aux réponses simulées
avant sélection des lignes, comme dans le contrat serveur.

La recette finale de ce complément réussit : **12 pages rendues et relues**,
copies canonique/embarquée/servie identiques, navigation et clavier vérifiés à
**390 et 1440 pixels**, assistance simulée indisponible (HTTP 503), **zéro
violation Axe** et aucun débordement horizontal. Les empreintes du PDF sont
restées stables avant et après la vérification finale. Les nouvelles captures
d’iconographie apportées en parallèle ont été conservées dans le PDF ; une
première vérification avait détecté sa régénération concurrente, puis le cycle
final capture, rendu, synchronisation et vérification a été rejoué.

Depuis le dépôt `localeo-commercant`, sans charger de configuration opérateur :

```powershell
$env:LOCALEO_TEST_DIST = 'tmp/guide-merchant-dist-refresh'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/guide-merchant-dist-refresh
py -3.14 scripts/generate-merchant-guide.py --preview-dir tmp/guide-refresh-merchant-pdf
npm run guide:sync
npm run guide:check
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/guide-merchant-dist-refresh --check-guide --verify-only
```

Le serveur isolé des captures utilise le port **4181** et s’arrête en fin de commande. Les générateurs et fixtures exécutables restent dans le dépôt applicatif. Le manifeste local `tmp/guide-refresh-merchant-capture/provenance.json` relève les captures et requêtes simulées ; `verification.json` contient les résultats de recette. Les aperçus du PDF sont dans `tmp/guide-refresh-merchant-pdf`.

Les résultats exécutés de l’édition du 22 novembre sont relevés dans le
[bilan du correctif](../../../../../specifications/epic-78-jeu-des-vitrines/bilan-realisation.md#correctif-du-22-novembre-2026--clarifier-la-préparation-commerçant).
Les 12 captures ont été reproduites ; quatre images changent : validation
coffret, remise de lot, frise de préparation et revue Vitrines. Les 12 pages
du PDF ont été rendues et relues, avec inspection détaillée des pages 7/8.
La copie embarquée est identique au PDF canonique. Navigation, clavier,
PDF HTTP 200 et Axe sans violation ont été vérifiés à 390/1440 px, y compris
avec l’assistance en erreur HTTP 503. Les manifests locaux de capture et de
vérification conservent les résultats ; il s’agit de preuves locales synthétiques.

Le nombre de pages et de signets dérive des sections de niveau 2 du Markdown : une section ouvre une page. Le générateur refuse un débordement sur une page supplémentaire au lieu de compresser le contenu. Après une évolution, recapturer les zones concernées, mettre à jour les légendes, régénérer, relire toutes les pages puis synchroniser le PDF. Voir la [procédure Commerçant](../../../../../exploitation/deploiement/commercant/mise-en-production.md#guide-commerçant-embarqué).

## Illustrations historiques conservées

L’édition du 21 novembre 2026 reposait sur la base `74000ad` et comportait
**12 pages, 12 captures et 12 signets**. Son build synthétique, la relecture des
pages rendues, `guide:check` et les contrôles de navigation, clavier, HTTP et Axe
à **390 et 1440 pixels** avaient réussi, sans violation Axe. L’assistance
répondait volontairement HTTP 503 et le guide restait accessible. Ces résultats
appartiennent à cette édition, sans prouver la recette du correctif courant.

Les fichiers `03-animation.png`, `04-reversements.png`, `06-publication.png` et `10-alertes.png` proviennent des captures historiques du 26 septembre 2026 sur TEST, version `v1.0.0+d09fca1f`, avec le commerce fictif **Le Fournil des Tilleuls**. Ils restent disponibles comme archives et ne sont pas utilisés dans le PDF actuel. Ils ne représentent pas l’interface de novembre.

L’ancienne édition du 29 septembre comptait huit pages et neuf illustrations utilisées. L’édition de novembre remplace les captures encore utilisées et ajoute cinq vues ; les références anciennes à un profil sans invitation ni facture en attente ne décrivent donc pas les exemples actuels.
