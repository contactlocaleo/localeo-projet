# Illustrations du guide quotidien commerçant

## Captures de l’édition du 25 novembre 2026

`23-valider-passage.png` montre le passage d’un joueur avant confirmation, à
720 px. `24-mot-de-passe-oublie.png` montre le formulaire **Recevoir un lien**,
à 640 px. Les deux captures proviennent du frontend Pro sur la base Git
`6e92f40` avec les changements locaux, sous Chromium et avec des exemples
fictifs. Les requêtes externes sont bloquées.

Depuis `localeo-commercant` :

```powershell
$env:LOCALEO_TEST_DIST = 'tmp/guide-edition-20261125/capture-dist'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/guide-edition-20261125/capture-dist --report-dir tmp/guide-edition-20261125/capture-report --port 45181 --only 23-valider-passage,24-mot-de-passe-oublie
```

## Invitation du 24 novembre 2026

La capture `12-invitations.png` du 24 novembre 2026 illustre l’invitation d’une association voisine avec des données fictives. Depuis le dépôt Commerçant, utiliser le build local documenté puis `node scripts/capture-merchant-guide.mjs --dist tmp/e84-guide-pro --only 12-invitations`.

## Scan depuis l’appareil photo — E82, 24 novembre 2026

La capture **02-validation.png** montre une prestation prête à confirmer
après arrivée par le lien du QR. Chromium utilise un commerce et un QR
fictifs, des API simulées et l’accès réseau local uniquement.

Depuis `localeo-commercant` :

```powershell
$env:LOCALEO_TEST_DIST = 'tmp/e82-guide-dist'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/e82-guide-dist --report-dir tmp/e82-guide-capture --port 4220 --only 02-validation
py -3.14 scripts/generate-merchant-guide.py --preview-dir tmp/e82-guide-final
npm run guide:sync
npm run guide:check
```

## Clés d’accès du 24 novembre 2026

Les captures **21-connexion-cle.png** et **22-creation-cle.png** montrent le bouton de connexion par clé d’accès et la création depuis **Mes clés d’accès**. Elles proviennent du frontend Pro sur la base Git `2ccb8da` et les modifications locales WebAuthn, en Chromium à 640 px. Le service de disponibilité, la session et la liste de clés utilisent des réponses synthétiques. Les requêtes externes sont bloquées.

Depuis `localeo-commercant` :

```powershell
$env:LOCALEO_TEST_DIST = 'tmp/pro-passkeys-guide-capture-dist'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/pro-passkeys-guide-capture-dist --report-dir tmp/pro-passkeys-guide-capture --port 5191 --only 21-connexion-cle,22-creation-cle
py -3.14 scripts/generate-merchant-guide.py --preview-dir tmp/pro-passkeys-guide-pdf-final
npm run guide:sync
npm run guide:check
$env:LOCALEO_TEST_DIST = 'tmp/pro-passkeys-guide-check-dist'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/pro-passkeys-guide-check-dist --check-guide --verify-only --report-dir tmp/pro-passkeys-guide-capture --port 5191
```

Les quatorze pages ont été rendues et relues. Le contrôle à 390 et 1440 px a vérifié le lien applicatif, le focus clavier et les octets du PDF servi malgré l’assistance indisponible. Axe n’a signalé aucune violation sur la page d’aide. Les rapports locaux `provenance.json` et `verification.json` sont dans `tmp/pro-passkeys-guide-capture`.

## Historique des interventions du 23 novembre 2026

Captures Chromium de la rubrique **Interventions de Localeo** avec des données fictives sur la base Git `2dc3397` et les modifications E76. La capture `20-interventions.png` présente la soumission du brouillon par Localeo.

```powershell
$env:LOCALEO_TEST_SUPPORT='true'
$env:LOCALEO_TEST_DIST='tmp/e76-guide/dist'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/e76-guide/dist --report-dir tmp/e76-guide/recette --port 4376 --only 20-interventions
```

## E56-EVO-ETATS-PREPARATION — 22 novembre 2026

Les captures **01-accueil.png** et **16-preparation.png** ont été recapturées
depuis Localeo Pro, base Git `e27ffec` avec l’évolution locale. L’accueil montre
l’alerte, la vue **Mes actions** et les deux états ; l’étape 2 présente **Préparation : Terminée** et
**Déclaration à l’organisateur : À faire**. Les autres illustrations conservent
la provenance de leur dernière capture ci-dessous.

Le script applicatif utilise Chromium, le commerce fictif La Maison des
Saveurs, des API synthétiques et l’heure de Paris fixée au 22 novembre 2026.
Les requêtes externes sont bloquées. Aucun compte, QR utilisable ou jeu de
données réel n’est sollicité. Le port 4283 et les builds sont isolés.

Depuis `localeo-commercant`, commandes exécutées :

```powershell
$env:LOCALEO_TEST_DIST = 'tmp/preparation-dual-guide-mes-actions-dist'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/preparation-dual-guide-mes-actions-dist --only 01-accueil,16-preparation --report-dir tmp/preparation-dual-guide-mes-actions-capture --port 4283
py -3.14 scripts/generate-merchant-guide.py --preview-dir tmp/preparation-dual-guide-mes-actions-pdf
npm run guide:sync
npm run guide:check
$env:LOCALEO_TEST_DIST = 'tmp/preparation-dual-guide-mes-actions-pdf-check-dist'
node scripts/build-browser-tests.mjs
node scripts/capture-merchant-guide.mjs --dist tmp/preparation-dual-guide-mes-actions-pdf-check-dist --check-guide --verify-only --report-dir tmp/preparation-dual-guide-mes-actions-capture --port 4283
```

Les **douze pages** ont été rendues et relues, sans débordement de texte ni
changement de taille des caractères. Une première génération à treize pages
a été refusée par le générateur avant remplacement du PDF ; le texte de la
page 1 a été resserré, puis la version à douze pages a été validée. Le générateur
conserve désormais les rendus de diagnostic lorsque `--preview-dir` est fourni,
même si le nombre de pages est refusé.

La copie embarquée est identique au PDF canonique. La recette a vérifié le lien
applicatif, le focus clavier, HTTP 200 et les octets du PDF servi à **390 et
1440 px**, avec l’assistance en erreur ; **aucune violation Axe**. Les rapports
sont `tmp/preparation-dual-guide-mes-actions-capture/provenance.json` et `verification.json`.
La même recette vérifie qu’une ancienne déclaration enregistrée sans
attestation laisse la préparation à compléter à l’étape 2, à 390 et 1440 px.
Cette passe finale inclut le style de résumé partagé dès l’accueil initial et
le libellé **Mes actions**. L’état est en tête de l’étape 2 et la commande de
confirmation suit les consignes du kit. Les sorties de la première
passe sont conservées dans les dossiers `tmp/preparation-dual-guide-*` antérieurs.
Cette preuve locale ne vaut pas recette connectée ou déploiement.

## Iconographie de gestion du 22 novembre 2026

Les douze vues du guide ont été recapturées depuis Localeo Pro sur la base
`643a90a`, avec les évolutions locales. L’accueil montre les deux files sous
**Préparation des animations**, et la page 7 conserve la déclaration datée et
le statut **Préparation : confirmée**. Les libellés, états et montants observés
proviennent de scénarios Chromium et d’API synthétiques.

Depuis `localeo-commercant`, le build de capture est produit par
`node scripts/build-browser-tests.mjs` avec `LOCALEO_TEST_DIST` défini vers
`tmp/guide-iconography-pro-dist`. La commande
`node scripts/capture-merchant-guide.mjs --dist tmp/guide-iconography-pro-dist`
a été exécutée avec une copie locale du script, un port réservé (4281) et
un dossier de sortie séparé. Son manifeste est
`tmp/iconography-pro-guide/provenance.json`. Une recapture ciblée de l’accueil
a utilisé le build `tmp/guide-iconography-pro-dist-final` et le port 4282.

Le PDF est régénéré par
`py -3.14 scripts/generate-merchant-guide.py --preview-dir tmp/iconography-pro-guide/pdf`
puis synchronisé par `npm run guide:sync` et vérifié par `npm run guide:check`.
Les douze pages ont été rendues et relues. Le build
`tmp/guide-iconography-pro-pdf-check-dist` et les options
`--check-guide --verify-only` ont vérifié les liens, le focus clavier et
le PDF effectivement servi à 390 et 1440 px, y compris avec l’assistance
indisponible. Axe n’a signalé aucune violation. Le rapport est
`tmp/iconography-pro-guide/verification.json`.

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
| `16-preparation.png` | Étape 2 terminée, déclaration à l’organisateur encore à faire |
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

## Habillage bleu nuit et orange — 22 novembre 2026

Les douze captures utilisées par le PDF ont été reprises depuis le frontend Pro
construit dans `tmp/charte-pro-20261122`, sur la base `e27ffec` et les
modifications locales présentes. Elles montrent la palette bleu nuit, papier
clair et pêche, ainsi que les icônes de gestion avec un accent orange. Les
modifications de préparation et de déclaration déjà en cours sont conservées ;
les étapes et les libellés pédagogiques restent applicables.

Commande de capture :
`node scripts/capture-merchant-guide.mjs --dist tmp/charte-pro-20261122 --report-dir tmp/charte-pro-guide-capture-final-20261122`.
Le manifeste `provenance.json` de ce dossier conserve les routes, dimensions
et appels simulés. Le serveur local du guide utilise le port réservé 4181,
sans requête externe ni compte réel.

Le PDF a été régénéré avec
`py -3.14 scripts/generate-merchant-guide.py --preview-dir tmp/charte-pro-guide-pdf-20261122` :
ses **12 pages** ont été rendues et relues, avec inspection détaillée des pages
de préparation et Vitrines. `guide:sync` et `guide:check` confirment l'égalité
de la copie embarquée. La recette finale du lien, du PDF servi, du clavier et
de l'accessibilité à 390 et 1440 px est conservée dans
`tmp/charte-pro-guide-verify-final-20261122/verification.json` ; l'assistance
y répond volontairement HTTP 503 et Axe ne remonte aucune violation.

Une mise à jour parallèle des captures de préparation a ensuite régénéré le
guide. Deux tentatives ont été périmées par ces écritures concurrentes. Le
contrôle final porte sur le PDF de 1 202 199 octets, SHA-256
`37183d0e2eb3538a991b6d5ec0817c2b82e8409a2f454bb6de751a92b5adbbf3`.
Ses 12 pages ont été rendues et relues dans
`tmp/charte-pro-guide-snapshot-20261122-2`, sans écraser les captures ni
relancer la génération canonique. Seule la copie statique du PDF du build
local a été actualisée. La navigation, le clavier, l'accès HTTP au PDF et
Axe ont réussi à 390 et 1440 px avec l'assistance indisponible ; rapport :
`tmp/charte-pro-guide-verify-snapshot-20261122-2/verification.json`.
Le relevé `snapshot.json` confirme les empreintes canonique, embarquée et
servie identiques avant et après ce contrôle. Une édition remplacée après
ce contrôle exige sa propre vérification.

La recette visuelle complémentaire de l'accueil, du scanner et du formulaire
de mot de passe couvre 320, 390 et 1280 px, avec texte à 100 et 200 % :
**18 combinaisons sans violation Axe ni débordement horizontal**, captures et
résultats dans `tmp/charte-pro-visual-final-20261122`. Ces preuves locales ne
constituent pas une validation d'un déploiement.

## Illustrations historiques conservées

L’édition du 21 novembre 2026 reposait sur la base `74000ad` et comportait
**12 pages, 12 captures et 12 signets**. Son build synthétique, la relecture des
pages rendues, `guide:check` et les contrôles de navigation, clavier, HTTP et Axe
à **390 et 1440 pixels** avaient réussi, sans violation Axe. L’assistance
répondait volontairement HTTP 503 et le guide restait accessible. Ces résultats
appartiennent à cette édition, sans prouver la recette du correctif courant.

Les fichiers `03-animation.png`, `04-reversements.png`, `06-publication.png` et `10-alertes.png` proviennent des captures historiques du 26 septembre 2026 sur TEST, version `v1.0.0+d09fca1f`, avec le commerce fictif **Le Fournil des Tilleuls**. Ils restent disponibles comme archives et ne sont pas utilisés dans le PDF actuel. Ils ne représentent pas l’interface de novembre.

L’ancienne édition du 29 septembre comptait huit pages et neuf illustrations utilisées. L’édition de novembre remplace les captures encore utilisées et ajoute cinq vues ; les références anciennes à un profil sans invitation ni facture en attente ne décrivent donc pas les exemples actuels.
