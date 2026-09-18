# Compte rendu — Analyse des écarts MVP

**Projet :** Localeo Animation — Backoffice gestionnaire  
**Date :** 16 août 2026  
**Base :** Prototype Sprint 1 + Sprint 2 (référence design)

---

## Ce qui est complet et référençable tel quel

Toutes les screens principales sont présentes et câblées à l'API mock :

- Auth (login, session expirée, logout)
- Dashboard avec KPIs dynamiques + alertes API
- Liste des animations + vue détail (10 onglets)
  - WorkflowTab, LiveTab, ConfigurationTab (mode édition), ParticipantsTab, ValidationsAnimTab, TirageTab, GainsAnimTab, FlyerTab, BilanTab, AuditTab
- 5 vues globales : Participants, Validations, Tirages, Flyers, Bilans, Coffrets
- Wizard de création câblé (modèles, commerçants, coffrets, create + publier)
- Abonnement, Support, Modèles

---

## Écarts identifiés pour le MVP production

### 🔴 Bloquant

#### 1. Persistance de session
La session n'est qu'en mémoire React. Un rechargement de page déconnecte l'utilisateur.  
**Attendu :** stocker le token JWT en `localStorage` (ou cookie `httpOnly` côté backend) et le relire au démarrage de l'application.

#### 2. Routing URL
Pas de `react-router`. Le bouton "retour" du navigateur ne fonctionne pas, aucun lien direct vers une animation ou un onglet spécifique n'est possible.  
**Attendu :** routes `/animations/:id` et `/animations/:id/:tab` au minimum.

---

### 🟠 Important MVP

#### 3. QR code absent
Quand une animation est publiée, le QR d'inscription n'est pas affiché — seulement un message informatif "sera généré à la publication".  
**Attendu :** afficher le QR code dans le LiveTab ou la ConfigurationTab une fois l'animation publiée. C'est la fonctionnalité centrale du produit côté participant.

#### 4. Exports et téléchargements en stub
Tous les boutons "Exporter CSV", "Télécharger PDF", "Télécharger flyer" déclenchent uniquement un toast de confirmation sans action réelle.  
**Attendu :** URL de téléchargement retournée par l'API, ou génération côté client selon le cas.

#### 5. Filtres et recherche non fonctionnels
Les inputs de recherche et de filtre sont présents dans toutes les vues listes, mais n'appliquent aucun filtre réel sur les données.  
**Attendu :** filtrage côté client pour les listes courtes, paramètre de requête API pour les grandes listes (participants, validations).

#### 6. Pagination absente
Les vues globales (812 participants, 634 validations…) affichent uniquement la première page retournée par le mock. Aucun contrôle de pagination n'est rendu.  
**Attendu :** contrôles précédent / suivant + indicateur "page X sur Y" sur toutes les vues listes.

#### 7. Preview du flyer
`preview_url` retourne `null` dans le mock — le FlyerTab affiche un placeholder générique.  
**Attendu :** affichage de l'image générée par le backend ; état intermédiaire "génération en cours" si le flyer n'est pas encore prêt.

---

### 🟡 Attendu MVP

#### 8. Actions workflow incomplètes
- **Annuler** (`api.animations.annuler`) : l'action n'est pas accessible depuis l'interface.
- **Archiver** : après le bilan, aucun bouton n'appelle d'action d'archivage.

Les deux statuts `annulee` et `archivee` apparaissent dans la configuration des statuts mais ne sont jamais déclenchables par l'utilisateur.

#### 9. Sélecteur de commune absent
L'API expose un concept de `communes_habilitees` (support multi-communes), mais l'interface affiche toujours "Ville de Valmont" de façon statique.  
**Attendu :** sélecteur de commune active dans la sidebar ou le TopBar, avec rechargement du contexte via `api.contexte.get()`.

#### 10. Polling temps réel absent sur le LiveTab
Le LiveTab affiche un horodatage `generated_at` mais ne re-fetche pas automatiquement les données.  
**Attendu :** polling toutes les 30 à 60 secondes pour les animations au statut `en_cours`, avec indicateur visuel de fraîcheur.

---

### 🟢 Post-MVP

#### 11. Formulaire support sans envoi réel
Le formulaire de support soumet uniquement un toast de confirmation. L'appel API (ticketing ou email) n'est pas câblé.

#### 12. Gestion d'erreurs incomplète
`ApiError` + bouton "Réessayer" est absent de certaines vues (`AnimationsView`, `ConfigurationTab`, vues globales). Un `ErrorBoundary` React global manque pour les erreurs non catchées.

#### 13. Accessibilité (ARIA)
Les modales, onglets et menus déroulants n'ont pas d'attributs ARIA (`role`, `aria-label`, `aria-expanded`). À traiter avant mise en production publique.

---

## Tableau récapitulatif

| Priorité | # | Item |
|---|---|---|
| 🔴 Bloquant | 1 | Persistance de session (localStorage / cookie) |
| 🔴 Bloquant | 2 | Routing URL (react-router, deep links) |
| 🟠 Important MVP | 3 | QR code d'inscription pour animation publiée |
| 🟠 Important MVP | 4 | Exports réels (CSV, PDF, flyer) |
| 🟠 Important MVP | 5 | Filtres et recherche fonctionnels |
| 🟠 Important MVP | 6 | Pagination sur les vues listes |
| 🟠 Important MVP | 7 | Preview du flyer généré |
| 🟡 Attendu MVP | 8 | Actions Annuler et Archiver |
| 🟡 Attendu MVP | 9 | Sélecteur de commune active |
| 🟡 Attendu MVP | 10 | Polling temps réel sur le LiveTab |
| 🟢 Post-MVP | 11 | Envoi réel du formulaire support |
| 🟢 Post-MVP | 12 | Gestion d'erreurs exhaustive + ErrorBoundary |
| 🟢 Post-MVP | 13 | Accessibilité ARIA |

---

*Document généré à partir de l'analyse du prototype — à compléter avec les retours product et les contraintes backend.*
