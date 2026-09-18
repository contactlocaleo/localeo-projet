# Charte des emails Localeo

Les emails transactionnels et les notifications système reprennent la marque
de la marketplace : encre bleue, papier clair et orange pour l'action principale.
Le contenu métier, les liens, les codes QR, les références et les pièces jointes
restent produits par leurs services habituels.

## Référence graphique

La référence est le code actuel de `../localeo-marketplace`, particulièrement
`src/styles/tokens.css`, `src/styles/marketplace-brand.css` (chargé après les
styles historiques), `src/styles/fonts.css` et le header/footer de `src/App.jsx`.
Les anciennes valeurs présentes dans `site-base.css` ne définissent pas la
charte actuelle.

| Usage | Valeur |
| --- | --- |
| Encre, titres, header | `#082840` |
| Fond papier | `#f6f5f1` |
| Surface du message | `#ffffff` |
| Action principale | `#f28a2e`, texte `#082840` |
| Texte secondaire | `#65747f` |
| Séparateurs | `#d7d9d8` |
| Texte courant | `DM Sans`, Arial, sans-serif |
| Titres courts | `Oswald`, Arial Narrow, Arial, sans-serif |

La marketplace auto-héberge DM Sans et Oswald dans son bundle Vite. Les emails
ne nécessitent aucun chargement de police externe : les familles de marque
s'appliquent lorsqu'elles sont disponibles, avec les replis indiqués. Les
titres, les boutons et les informations restent du texte HTML sélectionnable.

Le logo email est une copie exacte du pictogramme actuellement utilisé par la
marketplace : `public/icons/localeo-coffret-icon.png`. Le fichier backend
`app/infrastructure/email/templates/localeo.png` est un PNG transparent de
256 × 256 pixels, de rapport 1:1, affiché sans étirement. Il remplace l'ancien
écusson 32 × 32. SHA-256 des deux fichiers copiés :
`f3ad28e2b4266aa1d61acba4a11455cac26afd8494facad8010464711ecacb94`.

L'URL publique existante reste
`{LOCALEO_EMAIL_ASSET_BASE_URL}/email-assets/localeo.png` ; aucun déploiement du
frontend n'est requis pour servir le nouveau fichier. Le mot Localeo reste
présent en texte lorsque les images sont bloquées. La signature de marque
« Expériences locales à offrir » provient du header/footer de la marketplace.

## Composition commune

Le document est une colonne de 640 pixels maximum, fluide sur mobile, avec
un fond papier, un header bleu encre et une surface blanche. Le contenu dispose
de marges internes de 32 pixels sur ordinateur et de 20 pixels sur mobile.
Les angles restent discrets (4 à 6 pixels) et la hiérarchie repose sur les
espaces, les titres courts et les séparateurs.

L'ordre de lecture est : marque, contexte du message, titre principal,
information ou action attendue, détails utiles, aide/signature. L'action
principale est orange avec un texte bleu encre ; les actions secondaires sont
sobres. Les références et URLs longues peuvent revenir à la ligne. Les listes
de prestations, informations de facturation et rappels conservent une lecture
verticale claire.

Le bloc Localeo Live reste associé aux types de messages déjà prévus par
`ServicePreparationEmail`. Il conserve ses liens avec token dans le fragment
et s'insère à l'intérieur du document commun. Les QR restent embarqués en
tables HTML ; aucune dépendance à une image QR distante n'est introduite.

## Implémentation et limites

`app/infrastructure/email/branding.py` expose `render_email` et `action_link`.
Le document commun est `templates/_layout.html` ; les 15 autres modèles sont
des fragments de contenu. `render_email` échappe le titre, la catégorie, le
préheader et l'URL du logo. `action_link` échappe le libellé et l'URL. Les
fragments HTML restent du contenu de confiance produit par les services,
qui doivent échapper leurs valeurs dynamiques avant insertion.

Le marqueur `data-localeo-email="marketplace-v1"` évite un double enveloppement.
Les nouveaux emails système passent par ce rendu commun, y compris les
producteurs directs. Les communications libres et les messages déjà stockés
ne sont pas réécrits. Les objets métier, le texte brut, les destinataires et
les pièces jointes gardent leur contrat habituel.

La structure utilise des tables de présentation et des styles intégrés au
HTML, sans JavaScript, framework CSS, flex, grid ou dégradé. Les media queries
améliorent le rendu mobile ; la colonne reste fluide sans elles. Le rendu exact
des polices et des angles dépend du client mail. Une vérification navigateur
permet de contrôler la composition et les débordements ; elle ne remplace pas
une recette dans les clients Gmail, Apple Mail et Outlook utilisés en production.

## Aperçus locaux et recette

### Identifiant du QR et copie depuis les confirmations

Les confirmations de participation et de coffret affichent sous leur QR un bloc
« Identifiant du QR code », également présent dans la version texte du mail.
Il reprend la valeur acceptée par la saisie manuelle de Localeo Pro :

- Coffret : le `qr_token` complet, identique au QR actif enregistré ; aucune
  nouvelle signature n'est produite pour préparer l'email. Le code court de
  vérification reste libellé comme un code destiné au support.
- Animation : le `participant_token` complet, avec sa casse d'origine. Le QR
  conserve l'URL de participation et l'identifiant affiché correspond au token
  de cette participation, pas à son UUID ou à sa référence.

Le bouton « Copier l’identifiant » est un lien HTML vers la page du QR ; un
second appui sur « Copier » dans le navigateur réalise la copie. Le texte du
mail explique ces deux étapes et permet aussi une sélection manuelle. Aucun
JavaScript n'est ajouté aux emails. La copie navigateur existante utilise
[Clipboard.writeText](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText)
en contexte sécurisé avec un repli par sélection manuelle.

Le coffret ouvre `/qr-impression#token=…` sur l'origine configurée par
`LOCALEO_FRONT_CONSULTER_COFFRET_INSTANCE_QR_URL`. Le QR est encodé dans le
fragment, sans query paramètre, puis retiré de l'URL par la Marketplace. Ce
parcours permet d'afficher/copier le QR sans échanger un lien de consultation.
Les boutons de consultation, d'impression du résumé et Localeo Live conservent
leur contrat d'accès distinct ; la copie ne consomme pas leur code `cl1.`.
La validation de la prestation reste effectuée par Localeo Pro et le backend.
Pour l'animation, le bouton reprend l'URL participant avec `#qr`, qui ouvre
directement le dialogue QR et son bouton Copier.

Les régénérations de QR ou de lien de consultation coffret bénéficient du même
modèle. Les mails déjà stockés dans l'outbox gardent leur contenu : une relance
technique d'un ancien email ne le recrée pas. Déployer les adaptations
Marketplace (`#token` et `#qr`) avant le backend pour activer ces nouveaux liens.

### Générer les aperçus

Depuis la racine du backend, dans l'environnement Python du projet :

```bash
python scripts/emails/preview_emails.py --output tmp/email-previews
python -m pytest tests/infrastructure/email/test_email_branding.py tests/application/services/test_service_preparation_email.py
```

La galerie `tmp/email-previews/index.html` couvre les 15 modèles et des appels
réels aux méthodes de préparation : confirmation avec QR et token long,
remboursement, réponse et notification support, accès/réinitialisation Animation,
paiement et facture. Toutes les données sont fictives. Le script n'envoie aucun
email et n'appelle ni base de données ni API ; le logo est copié localement et
les URLs exportées utilisent le domaine réservé `localeo.example.test`.
Une politique de contenu interdit les ressources réseau dans chaque aperçu.

Vérifier à 320, 375 et 800 pixels : absence de défilement horizontal, titre
lisible, CTA accessible, logo non déformé, QR complet, références longues
contenues et bloc Localeo Live présent une seule fois lorsqu'il s'applique.
Contrôler également les messages longs et les images bloquées. Les tests
couvrent l'idempotence, l'échappement, les marqueurs des modèles, la conservation
du QR et l'absence de styles incompatibles ou de l'ancienne palette.

Recette locale du 12 septembre 2026 : la suite cumulative de 111 tests passe
(préparation et envoi simulé, producteurs directs, factures, Chorus, reversements,
souscriptions, accès et contrat de renvoi), dont les 8 tests de
`test_email_branding.py`. Les 24 aperçus ont été contrôlés sous Chromium
aux largeurs 320, 375 et 800 pixels, soit 72 contrôles sans débordement horizontal,
avec une seule enveloppe par message et les logos chargés. Les QR mesurés restent
carrés aux trois largeurs : 212 × 212 pixels pour le parcours avec token long,
132 × 132 pixels pour les exemples courts. Les captures dans
`tmp/email-previews/captures/` incluent aussi un rendu avec image indisponible.
Cette vérification navigateur ne constitue pas une certification du rendu dans
les clients de messagerie et n'a envoyé aucun email.

Recette locale du 15 septembre 2026 pour les identifiants : 50 tests de
préparation, de présentation et d'envoi simulé passent. Les 25 aperçus,
dont les confirmations réelles de préparation coffret et participation, passent
75 contrôles Chromium à 320, 375 et 800 pixels, sans débordement horizontal.
Les deux confirmations ont aussi été relues sur les captures mobiles. Aucun
email n'a été envoyé ; les captures sont dans `tmp/email-identifiers-previews/`.
Dans la Marketplace, 9 cas Chromium ciblés passent : copie, anciens liens,
nettoyage de l'URL, réouverture du même lien, changement de QR et dialogue
Animation accessible. Le build de production et ESLint passent également.
