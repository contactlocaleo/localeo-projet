# Design system et UI

Palette utilisée dans `src/styles.css` :
- primaire `#0078d4`
- accent `#00a3e0`
- fond `#f5f9ff`
- surface `#ffffff`

## Composants à créer

- `Header`
- `Card`
- `Button`
- `Forms`

## Consignes visuelles

- Bord arrondi (`border-radius: 14px`)
- Ombres portées
- Typographie simple et efficace

### PRO-011 — Contraste du pied de page et noms accessibles
Couleur du pied de page assombrie (#5d6872 sur #f6f5f1). La vérification Lighthouse a aussi révélé le nom absent du bouton Installer en affichage mobile et le décalage entre libellé visible et nom accessible du lien d'accueil : ces deux écarts sont corrigés dans ce même retour accessibilité. Validation : 4 tests de composants réussis et 2 scénarios axe sans violation (liste Animation et connexion mobile avec installation).
