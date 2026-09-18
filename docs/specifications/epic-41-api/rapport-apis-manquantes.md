# Rapport — APIs manquantes · Backoffice Localeo

**Date :** 15 août 2026  
**Périmètre :** Maquette backoffice animation (branchement mock API)  
**Référence analysée à cette date :** ancien instantané OpenAPI de 231 chemins. Le [contrat actuel](openapi.json) a été régénéré depuis le code local le 18 septembre 2026.

---

> Rapport historique du 15 août 2026. Les constats initiaux ci-dessous se lisent avec la [réconciliation Localeo](#reconciliation-localeo) en fin de document ; ils ne constituent pas une nouvelle liste de blocages ni un changement du statut terminé de l’EPIC.

## Résumé du constat initial

Le branchement mock de la maquette a révélé **7 endpoints critiques absents** de la spec OpenAPI et **8 améliorations importantes** pour une mise en production viable. Les points critiques bloquent des fonctionnalités visibles utilisateur et devront être planifiés en priorité.

---

## 🔴 Critique — Bloquant pour une fonctionnalité visible

### 1. Champ `reference` anonymisé sur `Participant`

| | |
|---|---|
| **Vue concernée** | ParticipantsTab |
| **Fonctionnalité** | Affichage d'une référence anonymisée dans le tableau (ex. `PART-0247`) |
| **API attendue** | `GET /animations/{id}/participants` → champ `reference: string` sur l'objet `Participant` |
| **Situation actuelle** | Le schéma actuel expose uniquement `nom_affiche` (ex. "J. M****") — pas anonymisé, non conforme RGPD pour un affichage agrégé |
| **Impact** | Non-conformité RGPD potentielle + incohérence UX avec le reste de l'interface |

---

### 2. Export CSV des participants d'une animation

| | |
|---|---|
| **Vue concernée** | ParticipantsTab |
| **Fonctionnalité** | Bouton "Exporter en CSV" affiché dans la maquette |
| **API attendue** | `GET /animations/{id}/participants/export` (Content-Type: text/csv) |
| **Situation actuelle** | Absent de la spec |
| **Impact** | Fonctionnalité bloquée — l'export CSV est attendu par les gestionnaires d'animation |

---

### 3. Champs `accroche` et `url_inscription` sur `Flyer`

| | |
|---|---|
| **Vue concernée** | FlyerTab |
| **Fonctionnalité** | Affichage du texte marketing et du lien QR code sur l'aperçu flyer |
| **API attendue** | `GET /animations/{id}/flyer` → champs `accroche: string`, `url_inscription: string` sur l'objet `Flyer` |
| **Situation actuelle** | Le schéma `Flyer` ne contient pas ces champs — la maquette affiche un texte statique en fallback |
| **Impact** | Le flyer généré ne reflète pas le contenu réel personnalisé par animation |

---

### 4. Endpoint de téléchargement PDF du flyer

| | |
|---|---|
| **Vue concernée** | FlyerTab |
| **Fonctionnalité** | Bouton "Télécharger PDF" |
| **API attendue** | `GET /animations/{id}/flyer/download` → redirect 302 vers URL PDF signée |
| **Situation actuelle** | Le champ `download_url` existe dans le schéma `Flyer` mais est systématiquement `null` dans la spec — aucun endpoint de download défini |
| **Impact** | Fonctionnalité bloquée — le téléchargement n'est pas possible |

---

### 5. Endpoint Dashboard (absent en totalité)

| | |
|---|---|
| **Vue concernée** | DashboardView |
| **Fonctionnalité** | KPIs globaux, graphique d'évolution, top commerçants, animations nécessitant une action |
| **API attendue** | `GET /partenaire/dashboard` → `DashboardPerformance { kpis, series, top_commercants, alertes, animations_action }` |
| **Situation actuelle** | Aucune opération dashboard dans la spec OpenAPI — l'endpoint n'existe pas |
| **Impact** | La vue principale du backoffice repose entièrement sur des données fictives |

---

### 6. Annulation / remplacement d'un gain après tirage

| | |
|---|---|
| **Vue concernée** | TirageTab |
| **Fonctionnalité** | Remplacer un gagnant (ex. gagnant injoignable) par son suppléant |
| **API attendue** | `POST /animations/{id}/gains/{gain_id}/remplacer` ou `DELETE /animations/{id}/gains/{gain_id}` |
| **Situation actuelle** | Absent de la spec — seul l'envoi d'un gain existant est prévu (`PUT /animations/{id}/gains/{gain_id}/envoyer`) |
| **Impact** | Cas métier fréquent non couvert — bloque la gestion des gagnants non répondants |

---

### 7. Endpoint Journal d'audit

| | |
|---|---|
| **Vue concernée** | AuditTab |
| **Fonctionnalité** | Affichage de l'historique des actions sur une animation |
| **API attendue** | `GET /animations/{id}/audit` → `{ items: AuditEntry[], next_cursor: string \| null }` |
| **Situation actuelle** | Absent de la spec OpenAPI — aucun endpoint d'audit par animation n'est défini |
| **Impact** | L'onglet Audit est non fonctionnel en production |

---

## 🟡 Important — Amélioration UX / Scalabilité

### 8. Pagination des participants côté serveur

| | |
|---|---|
| **Vue concernée** | ParticipantsTab |
| **Attendu** | `GET /animations/{id}/participants?page=&limit=` avec `next_cursor` en réponse |
| **Situation** | La réponse actuelle retourne tous les participants sans pagination — non scalable au-delà de ~500 participants |

---

### 9. Filtres côté serveur sur les validations

| | |
|---|---|
| **Vue concernée** | ValidationsAnimTab |
| **Attendu** | `GET /animations/{id}/validations?commercant_id=&statut=&date_debut=&date_fin=` |
| **Situation** | Aucun paramètre de filtre défini — le filtrage se ferait côté client uniquement |

---

### 10. Pagination du journal d'audit (cursor-based)

| | |
|---|---|
| **Vue concernée** | AuditTab |
| **Attendu** | `GET /animations/{id}/audit?after_cursor=` → `next_cursor` dans la réponse pour le chargement progressif |
| **Situation** | Dépend du point #7 — à intégrer dès la conception de l'endpoint |

---

### 11. Relance email d'un gagnant non répondant

| | |
|---|---|
| **Vue concernée** | GainsAnimTab |
| **Attendu** | `POST /animations/{id}/gains/{gain_id}/relancer` → déclenche un re-send de notification |
| **Situation** | Absent — la maquette affiche un indicateur "Non consommé" mais sans action possible |

---

### 12. Flux temps réel (Live Tab)

| | |
|---|---|
| **Vue concernée** | LiveTab |
| **Attendu** | SSE `GET /animations/{id}/live/stream` ou WebSocket pour un rafraîchissement push |
| **Situation** | Seul un polling GET est dans la spec — acceptable pour un MVP mais dégradé en UX pour une animation active |

---

### 13. PATCH partiel de la configuration

| | |
|---|---|
| **Vue concernée** | ConfigurationTab |
| **Attendu** | `PATCH /animations/{id}/configuration` avec body partiel `{ commercants?, coffrets?, seuil_validations? }` |
| **Situation** | Seul un PUT complet semble prévu — un PATCH partiel évite les conflits de concurrence lors d'éditions simultanées |

---

### 14. Recherche textuelle sur la liste des animations

| | |
|---|---|
| **Vue concernée** | AnimationsView |
| **Attendu** | `GET /animations?q=recherche` |
| **Situation** | Le paramètre `q` est absent — la recherche serait limitée aux données déjà chargées côté client |

---

### 15. Sélecteur de période pour le dashboard

| | |
|---|---|
| **Vue concernée** | DashboardView |
| **Attendu** | `GET /partenaire/dashboard?periode=7j|30j|12m` |
| **Situation** | Dépend du point #5 — à intégrer dès la conception de l'endpoint dashboard |

---

## 🟢 Nice-to-have

| # | Vue | Fonctionnalité | API attendue |
|---|---|---|---|
| 16 | BilanTab | Export PDF du bilan complet | `GET /animations/{id}/bilan/export` |
| 17 | Notifications | Marquer toutes les notifications comme lues | `POST /partenaire/notifications/lire-tout` |
| 18 | AnimationsView | Archivage groupé de plusieurs animations | `POST /animations/archiver-lot` avec `{ ids: string[] }` |

---

## Synthèse priorisée

```
Priorité 1 (Sprint)   → #1 Référence anonymisée, #5 Dashboard, #7 Audit
Priorité 2 (Sprint+1) → #2 Export CSV, #3 Flyer fields, #4 Flyer download, #6 Remplacement gain
Priorité 3 (Backlog)  → #8 Pagination, #9 Filtres validations, #11 Relance email, #13 PATCH config
Priorité 4 (Futur)    → #12 SSE live, #14 Recherche, #15 Période dashboard, #16–18 Nice-to-have
```

---

*Rapport généré automatiquement depuis l'analyse du branchement mock — maquette backoffice Localeo v1.*

---

## Reconciliation Localeo

| Point | Decision |
| --- | --- |
| #1 | Accepte : ajout de `reference` pseudonymisee a `ParticipantAnimation`. |
| #2 | Accepte : ajout de `/participants/export.csv`. |
| #3 | Accepte : ajout de `accroche` et `url_inscription` au flyer. |
| #4 | Deja present : `/flyer/download`; contrat enrichi avec redirection temporaire possible. |
| #5 | Deja present : `/protected/animation-locale/dashboard-performance`. Aucun doublon `/partenaire/dashboard`. |
| #6 | Accepte : commande `remplacer` motivee utilisant le prochain suppleant. |
| #7 | Deja present : `/animations/{animation_id}/audit`. |
| #8 a #10 | Deja couverts par pagination serveur, filtres et curseur ; noms canoniques Localeo conserves. |
| #11 | Accepte : commande idempotente `relancer`. |
| #12 | Reporte : polling 15 secondes confirme au MVP par `ARB-24`. |
| #13 | Couvert : `PATCH /animations/{animation_id}` est partiel et porte la configuration modifiable. |
| #14 | Accepte comme alias : `q` complete le parametre canonique `recherche`. |
| #15 | Accepte : `periode=7j|30j|12m` complete `date_debut/date_fin`. |
| #16 a #18 | Ajoutes au backlog P2. |
