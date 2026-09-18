# Contrats corrigés avant production

## ANIM-001 — Facturation communale

Les listes et téléchargements de facturation sont limités au partenaire et à la
commune active côté backend. Les factures historiques sans commune sont réservées
au support; aucune commune n'est déduite du navigateur pour les régulariser.

## ANIM-002 et ANIM-006 — Paiement et reprise

Les clés de rejeu sont des UUID stables par intention, compatibles avec la limite
API de 128 caractères. Un paiement intégral en crédit n'exige pas d'URL Stripe,
mais sa confirmation exige la capture serveur de la réservation.

## ANIM-003 — Clôture cohérente

Scans, annulations, inscriptions, suppressions et éditions prennent le même verrou
animation que la clôture et relisent l'état après attente.

## ANIM-004 — Qualification

Le formulaire envoie `nombre_validations_requises` et
`validation_unique_par_commercant=true`. Le serveur compte les commerçants
distincts et refuse un seuil inatteignable avant publication. Les règles historiques
canoniques restent prioritaires; les tirages existants ne sont pas recalculés.

## ANIM-005 — Dates

Les jours représentent Europe/Paris. Début : minuit du premier jour; fin exclusive :
minuit suivant le dernier jour. Les API reçoivent des ISO UTC explicites. Le flyer
et le formulaire affichent les journées locales incluses. Les échéances commerçants
restent valides pendant toute la journée choisie à Paris.

## ANIM-007 — Export CSV

Les cellules textuelles pouvant être interprétées comme formules, y compris les
variantes Unicode pleine largeur, sont préfixées par `Texte: `. Les nombres typés
et les données sources sont préservés.

## ANIM-008 — Création rejouable

Une nouvelle tentative après timeout réutilise la même clé tant que le formulaire
ne change pas. Le brouillon, ses invitations et la réponse de rejeu sont atomiques.
Deux appels simultanés avec la même clé produisent un seul brouillon.

## ANIM-009 — Changement de commune

Le sélecteur présente les communes habilitées renvoyées par le serveur. Les actions
sont suspendues pendant le changement. Les réponses tardives sont rejetées.
Même après perte de confirmation, le contexte serveur est relu.

## ANIM-010 — Live, listes et exports

Le live se recharge toutes les 15 secondes lorsque l’onglet est visible, sans requêtes périodiques simultanées. Les erreurs restent visibles avec la dernière donnée reçue. Les listes parcourent les pages serveur de 100 éléments; une pagination incomplète produit une erreur explicite. Les boutons d’export validations et bilans téléchargent désormais les données réelles, avec neutralisation des formules CSV.

## ANIM-012 — Session

Une réponse de connexion sans token ou expiration valide est refusée. Le token reste en mémoire. Une minuterie et le retour sur l’onglet ferment la session expirée sans attendre un HTTP 401. La déconnexion efface immédiatement la session locale; si le serveur ne confirme pas sa révocation, un message le précise. Après reconnexion, la route interne demandée est conservée, notamment pour consulter un retour de paiement.

## ANIM-013 — Données navigateur et erreurs

Les tentatives financières ne stockent que UUID et empreinte SHA-256; aucune adresse, email, téléphone ou motif en clair. Une mémoire de secours permet le rejeu si sessionStorage est désactivé; elle est purgée au changement de commune et à la déconnexion. Les logs HTTP ne contiennent que le statut et le reporting optionnel uniquement des catégories d’erreur, sans message, URL ou pile brute. Un échec de lecture des documents ou de marquage d’une notification reste visible.

## ANIM-014 — Opérations et recette

Une opération est suivie via son identifiant sur l'API de la même origine. Le client
n'utilise pas une URL de suivi arbitraire reçue dans une réponse. Seul SUCCEEDED
est un succès; un échec, un statut inconnu ou une attente dépassée est signalé.
La [formation](../../produit/formation/animation/guide-animation-preproduction.md) et le
[suivi](../../audits/animation/remediation-2026-09-06.md) décrivent la recette de production.
