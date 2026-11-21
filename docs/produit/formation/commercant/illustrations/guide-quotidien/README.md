# Illustrations du guide quotidien commerçant

## Édition du 21 novembre 2026

Le [guide source](../../guide-quotidien-commercant.md) et son PDF comportent **12 pages et 12 captures actuelles**. Elles proviennent du frontend React de Localeo Commerçant, base Git `74000ad` avec les modifications locales de maintenance du guide. La version synthétique affiche `v1.0.0+browser-` : il s’agit d’une recette locale, sans déploiement.

Les écrans ont été ouverts dans Chromium avec des API simulées et le commerce fictif **La Maison des Saveurs**. Le navigateur utilise l’heure de Paris et une horloge fixée au 21 novembre 2026. Les requêtes externes sont bloquées ; aucun compte réel, secret, QR personnel réel ou jeu de données installé n’est utilisé. Les invitations, montants, salariés et réponses de jeu sont des exemples fabriqués pour la formation. Aucune action métier réelle n’est exécutée.

Les captures sont réalisées directement dans l’application, sans redessiner ses écrans ni modifier ses libellés. Le script recadre la zone utile ou capture un composant entier afin de garder le texte lisible dans le PDF. Le viewport principal est de 1100 × 900 pixels, avec un facteur de pixels de 1,5.

| Fichier actuel | Vue illustrée dans le guide |
| --- | --- |
| `01-accueil.png` | Scanner principal et accès aux réglages des notifications |
| `02-validation.png` | Prestation de coffret à valider et action de confirmation |
| `05-horaires.png` | Page publique chargée : statut du brouillon, complétion et accroche |
| `08-activite.png` | Indicateurs d’activité : achats, réalisations et montants |
| `11-facturation.png` | Demande de facture : brut TTC, commission, net et état |
| `12-invitations.png` | Invitation en attente avec organisateur, dates et échéance de réponse |
| `13-guide-aide.png` | Guide PDF accessible dans Aide et contact |
| `14-lot.png` | Lot entier, commerce de remise, validité et confirmation de remise |
| `16-preparation.png` | Les trois repères du parcours de préparation |
| `17-vitrines.png` | Relecture Vitrines : contenu public et réponse privée fictive |
| `18-reglages.png` | État des notifications sur cet appareil et actualisation |
| `19-equipe.png` | Accès salarié : compte, accès effectif, invitation et révocation |

Les options Stripe, facturation, Chorus Pro, assistant d’émission, salariés et PIN sont présentées dans le texte comme dépendantes des droits et services disponibles. Une capture d’exemple ne prouve pas leur activation sur un environnement réel. La capture de réglages montre le cas où les notifications sont bloquées ; le guide explique aussi les autres états.

## Régénération et vérifications

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

Résultats de cette édition : build synthétique réussi, **12 pages et 12 signets**, pages rendues relues visuellement, copie embarquée identique au PDF canonique (`guide:check`). Les parcours de navigation et clavier, le PDF livré, l’absence de débordement et l’accessibilité Axe ont été vérifiés à **390 et 1440 pixels**, avec **zéro violation**. Le support répondait volontairement **HTTP 503** pendant cette recette : le guide restait accessible. Ces preuves locales ne constituent ni une recette sur appareil physique ni une vérification de déploiement.

Le nombre de pages et de signets dérive des sections de niveau 2 du Markdown : une section ouvre une page. Le générateur refuse un débordement sur une page supplémentaire au lieu de compresser le contenu. Après une évolution, recapturer les zones concernées, mettre à jour les légendes, régénérer, relire toutes les pages puis synchroniser le PDF. Voir la [procédure Commerçant](../../../../../exploitation/deploiement/commercant/mise-en-production.md#guide-commerçant-embarqué).

## Illustrations historiques conservées

Les fichiers `03-animation.png`, `04-reversements.png`, `06-publication.png` et `10-alertes.png` proviennent des captures historiques du 26 septembre 2026 sur TEST, version `v1.0.0+d09fca1f`, avec le commerce fictif **Le Fournil des Tilleuls**. Ils restent disponibles comme archives et ne sont pas utilisés dans le PDF actuel. Ils ne représentent pas l’interface de novembre.

L’ancienne édition du 29 septembre comptait huit pages et neuf illustrations utilisées. L’édition de novembre remplace les captures encore utilisées et ajoute cinq vues ; les références anciennes à un profil sans invitation ni facture en attente ne décrivent donc pas les exemples actuels.
