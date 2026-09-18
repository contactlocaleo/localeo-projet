# Design system et interface

La source des tokens et des styles est [src/styles.css](../../../../../localeo-commercant/src/styles.css). Réutiliser ses variables plutôt que maintenir une palette parallèle dans les composants.

## Repères visuels actuels

| Token | Valeur | Usage |
| --- | --- | --- |
| `--blue-900` | `#0b3d63` | Bleu principal |
| `--bg`, `--paper` | `#f6f5f1` | Fond clair |
| `--surface` | `#ffffff` | Surface |
| `--accent`, `--focus` | `#f28a2e` | Accent et focus |
| `--font-body` | DM Sans | Texte courant, puis polices de repli |
| `--font-display` | Oswald | Typographie de titre, puis polices de repli |

Les fontes sont déclarées dans [src/fonts.css](../../../../../localeo-commercant/src/fonts.css) et importées par [src/main.jsx](../../../../../localeo-commercant/src/main.jsx). Le token `--market-radius` vaut `4px` ; les rayons et ombres varient selon les composants. Il n'existe pas de règle générale imposant `14px` à toutes les bordures.

Le [manifeste PWA](pwa.md#installation-et-manifeste) conserve encore ses anciennes couleurs de thème et de fond. Ne pas les prendre comme définition de la palette CSS actuelle.

## Réutiliser les composants existants

Les composants partagés sont dans [src/app](../../../../../localeo-commercant/src/app) et les parcours dans [src/features](../../../../../localeo-commercant/src/features). Chercher les contrôles et classes existants avant d'ajouter une abstraction. [MerchantSessionHeader.jsx](../../../../../localeo-commercant/src/app/MerchantSessionHeader.jsx) et [PwaInstallButton.jsx](../../../../../localeo-commercant/src/app/PwaInstallButton.jsx) portent notamment la session et l'installation ; ce document ne prescrit pas de nouveaux composants génériques.

Préserver le focus visible, les libellés et noms accessibles, la navigation au clavier ainsi que les états chargement, vide, erreur et expiration. Vérifier les changements de styles sur mobile et sur les parcours concernés.

## Retour accessibilité PRO-011

Le pied de page utilise `#5d6872` sur `#f6f5f1`. Le retour PRO-011 mentionne aussi la correction du nom du bouton Installer sur mobile et l'alignement entre le libellé visible et le nom accessible du lien d'accueil. Les quatre tests de composants et deux scénarios axe sans violation sont le résultat historique consigné pour cette remédiation ; ils n'ont pas été rejoués pour cette mise à jour documentaire. Les commandes de vérification sont dans le [README de l'application](../../../../../localeo-commercant/README.md#vérifications).
