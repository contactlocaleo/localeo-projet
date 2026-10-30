# Registre des anomalies

## ANO-COM-E73-INVITATION-DECISION — Accès à la réponse commerçant

Signalement du **30 octobre 2026** sur TEST : absence du bouton de validation
pour **L'Escale Douce / Test passeport TCA**. L'écran observé dans Localeo Pro
`1.0.0+dbf6f52e` est `/animations/99527546-96eb-4a76-9a4b-b88db26ef12a`,
avec retour Notifications, dates du 1 au 9 novembre et kit indisponible.
Le contrôle visuel a été interrompu par Échap ; aucune acceptation ou autre
mutation métier n'a été effectuée sur TEST. Le détail API individuel de la
demande et son échéance n'ont pas été lus.

Trois écarts reproduits localement dans `localeo-commercant`, base `dbf6f52` :

- Le backend expose le lien de notification dans `action_cible`, ignoré par
  le frontend. Le repli ouvre la fiche animation au lieu de la demande.
- Une fiche animation répond déjà 200 lorsqu'une invitation est en attente,
  avec `demande_participation.id` et son statut. Le frontend n'ouvrait la
  demande que sur 404 et affichait sinon la mission et le kit sans décision.
- Une échéance ISO enregistrée à minuit était considérée comme dépassée par
  le navigateur, même si le serveur autorisait encore la réponse. Le domaine
  `DemandeParticipationCommercant` conserve la validité jusqu'à la fin du
  jour de Paris ; ses actions et son indicateur explicite font autorité.

Correction locale : lecture de `action_cible`, conversion des liens historiques
`/animations/invitations/{id}` vers le parcours existant, ouverture de la demande
sur une fiche 200 `EN_ATTENTE`, respect de l'échéance serveur et secours
calendaire Europe/Paris lorsque cet indicateur est absent. Les notifications
historiques de flyer `/animations/{id}/flyer` ouvrent la fiche animation,
qui porte le flyer ; la revue a détecté et corrigé ce cas avant livraison.
Le bouton existant **Accepter la participation** conserve l'accord explicite,
l'idempotence et les refus du serveur.

Quatre reproductions échouent avant correction pour les liens de notification,
la fiche 200 et l'échéance ISO. Le test de flyer ajouté après revue échoue aussi
avant son adaptation. Les tests couvrent les changements été/hiver, les refus
explicites, les réponses incertaines et l'absence de décision avant clic.

Validation : **187 tests Vitest réussis** (Animation, dates et contrat embarqué),
**15 scénarios Playwright réussis** (9 de parcours/invitation dont 6 à 390/1280 px,
6 de flyer dont mobile/bureau), build navigateur isolé réussi et
**22 tests backend existants réussis** pour la décision et l'espace Animation,
via le lanceur isolé. Aucun appel réel du backend dans ces recettes automatisées.
Guides et 130 sources exportées validés, `git diff --check` réussi dans les deux
dépôts touchés.

Périmètre : interface Commerçant et ce suivi canonique. Aucun changement du
backend, de contrat API, de droits, de règle métier, de schéma, migration,
participation ou générateur requis. La spécification E56 du consentement reste
applicable. Correction enregistrée dans le commit Commerçant `7e6b008`, à la
demande de l'utilisateur. **Déploiement et rejeu sur TEST restant à vérifier** ;
aucune acceptation métier effectuée sur TEST.

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
