# Design system et interface

La source des tokens et des styles est [src/styles.css](../../../../../localeo-commercant/src/styles.css). Réutiliser ses variables plutôt que maintenir une palette parallèle dans les composants.

## Repères visuels actuels

| Token | Valeur | Usage |
| --- | --- | --- |
| `--text`, `--muted` | `#183243`, `#526575` | Texte principal et secondaire |
| `--bg`, `--paper` | `#f5f7f9` | Fond de travail |
| `--surface` | `#ffffff` | Surface |
| `--accent`, `--accent-action` | `#09685e` | Action principale, texte blanc |
| `--accent-soft`, `--accent-text` | `#e1f0ec`, `#07594f` | Navigation et sélection actives |
| `--line`, `--input-line` | `#d8e1e7`, `#a5b8c4` | Contours des surfaces et des champs |
| `--focus` | `#b96913` | Focus clavier |
| `--font-body` | Police système sans empattement | Texte et titres de gestion |
| `--font-display` | `var(--font-body)` | Même famille pour les titres |
| `--radius-panel`, `--radius-button`, `--radius-field` | 12, 9, 7 px | Panneaux, actions et champs |

La [charte CRM commune](../../transverse/identite-entetes-applications.md#charte-des-espaces-de-gestion-internes--référence-crm)
est déclinée localement pour conserver l’indépendance des déploiements.
La signature du bandeau conserve son fond bleu nuit et son accent orange.
Les badges de statut et contenus personnalisables conservent leurs couleurs
propres ; leurs couleurs ne doivent pas être remplacées par celle des boutons.

Depuis le **4 novembre 2026**, les titres de page utilisent 25 px (23 px sur mobile)
et une graisse de 600, les sections 18 px et sous-sections 15 px. Le corps de travail
est à 14 px, avec des champs mobiles à 16 px. Les sections de formulaire déjà compactes
gardent leur densité ; les anciens grands titres de connexion, scan et validation
adoptent cette hiérarchie. Les compteurs et codes opérationnels gardent leurs
dimensions utiles. Voir les [repères typographiques de gestion](../../transverse/conventions-backoffice.md#typographie-des-applications-de-gestion)
et le [suivi d’ergonomie commun](../../../audits/ergonomie-gestion-pro-animation-2026-11-01.md).

Le [manifeste PWA](pwa.md#installation-et-manifeste) conserve encore ses anciennes couleurs de thème et de fond. Ne pas les prendre comme définition de la palette CSS actuelle.

## Réutiliser les composants existants

Les composants partagés sont dans [src/app](../../../../../localeo-commercant/src/app) et les parcours dans [src/features](../../../../../localeo-commercant/src/features). Chercher les contrôles et classes existants avant d'ajouter une abstraction. [MerchantSessionHeader.jsx](../../../../../localeo-commercant/src/app/MerchantSessionHeader.jsx) et [PwaInstallButton.jsx](../../../../../localeo-commercant/src/app/PwaInstallButton.jsx) portent notamment la session et l'installation ; ce document ne prescrit pas de nouveaux composants génériques.

Préserver le focus visible, les libellés et noms accessibles, la navigation au clavier ainsi que les états chargement, vide, erreur et expiration. Vérifier les changements de styles sur mobile et sur les parcours concernés.

## Retour accessibilité PRO-011

Le pied de page utilise `#5d6872` sur `#f6f5f1`. Le retour PRO-011 mentionne aussi la correction du nom du bouton Installer sur mobile et l'alignement entre le libellé visible et le nom accessible du lien d'accueil. Les quatre tests de composants et deux scénarios axe sans violation sont le résultat historique consigné pour cette remédiation ; ils n'ont pas été rejoués pour cette mise à jour documentaire. Les commandes de vérification sont dans le [README de l'application](../../../../../localeo-commercant/README.md#vérifications).
