# Registre des anomalies

## ALL
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-COM-01 | Invitation |sur la vue liste des demandes d'invitation, la commune et la date sont marqués "Non renseignés" alors qu'ils le sont das la backoffice| A corriger |
| ANO-COM-02 | Notification |la fonctionnalité "Marquer tout lu" ne fonctionne pas , l'état n'est pas persisté| A corriger |
| ANO-COM-03 | Notification |Le descrptif de la notification comporte des erreurs d'accent notament sur la description de la misttion | A corriger |

## Correction du 29 septembre 2026 — icônes PWA

- Attendu : utiliser le marqueur Localeo Pro de la même famille graphique que Live/OnBoard pour l'installation de Commerçant.
- Cause : les fichiers `public/icon-192.png` et `public/icon-512.png` contenaient encore l'ancien écusson, contrairement au favicon et au logo source.
- Correction locale : génération des deux icônes transparentes depuis `public/localeo-pro-icon.png` ; ajout d'une icône Apple 180 sur fond blanc et de sa référence HTML. Export reproductible via `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/export-pwa-icons.ps1`.
- Preuves : contrôle visuel de l'export Apple, dimensions et transparence des trois exports ; build isolé `node scripts/build-browser-tests.mjs` réussi. Le manifeste conserve les mêmes chemins d'icônes 192/512.
- Impact limité aux ressources statiques et à leur export : aucun contrat API, règle métier, migration ou générateur de démonstration modifié. Déploiement et vérification sur appareils iOS/Android non effectués ; le renouvellement des icônes déjà installées dépend du système.
