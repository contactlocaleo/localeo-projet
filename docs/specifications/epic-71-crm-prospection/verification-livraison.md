# E71 — Vérification et livraison

[Spécification V1](README.md), [backlog canonique](../../roadmap/a-faire/epic-71-crm-prospection-animation-coffrets-pro-backlog.md). **Tests produit prévus, non exécutés**. Aucun code CRM, import réel ou envoi réalisé pendant la spécification. La carte reste en V1 sur confirmation utilisateur ; CSV standard seul et report de CA-24 (import spécifique Gironde) sont également confirmés.

## Matrice de traçabilité

D = domaine pur ; A = application/UoW ; SQL = PostgreSQL jetable ; API = droits/contrats ; UI = navigateur. Chemins de suites à créer dans le backend, pas fichiers annoncés existants. Chaque famille couvre succès et refus ; les résultats demeurent **à produire**.

| Critères | Propriétaire et scénario de preuve | Documentation / contrat | Fixtures et exploitation |
| --- | --- | --- | --- |
| CA-01/02 | Organisation/dossier : D/A/API minimum, deux contacts/deux périmètres, deux campagnes, zéro conversion/envoi | Parcours fiche et contrat prospects/dossiers | Structure synthétique multi-périmètre, migration additive |
| CA-03 | Opportunité : D matrice des six étapes, pause/réexamen, perte/réouverture, preuve absente/invalide/valide pour chaque objectif ; deux dossiers/une preuve en SQL concurrent, annulation métier concurrente, rejeu et réouverture sans double comptage | Transitions, règles de gain et ARB-04b | OnBoard accepté, souscription active/gratuite, commande payée ; aucun paiement créé |
| CA-04 | Événement : D/A note/correction, dates distinctes, double clic et ajouts concurrents, XSS texte échappé | Chronologie, erreurs de formulaire | Notes synthétiques, logs sans contenu et purge selon politique |
| CA-05/06 | Tâche/rappel : D/A/API cycle, échéance Paris/UTC/DST, projection prochaine action ; terminer/report/réaffecter avant envoi | Aujourd'hui, Rappels et commandes | Tâches retard/jour/futur, horloge contrôlée, aucun fournisseur réel |
| CA-07/22 | Projections : API/UI filtres communs liste/suivi/carte, comptages distincts et datés, pagination SQL, zéro résultat/erreur | Recherche, indicateurs et carte | N/10N, mêmes filtres, une structure plusieurs dossiers |
| CA-08/09 | Lot : parser/A CSV UTF-8 BOM/sans BOM, guillemets/retours ligne, colonnes manquantes/dupliquées/inconnues, rejet XLSX, limites, groupe contradictoire atomique | Dictionnaire CSV et aperçu | Fixtures synthétiques ; formule non évaluée, exports neutralisés, zéro écrit avant confirmation |
| CA-10/11 | Identité/import : SQL mêmes clés, réordre, nom changé, homonymes, contact répété, lot concurrent et source différente, namespace avec espaces/casse normalisé et création de source explicite ; panne après commit/reprise ; deux créations sources A/B ou manuel/import avec barrières SQL, candidat apparu après décision de distinction, erreur de sérialisation sans création automatique | Clés stables et plan immuable | Aucune duplication, bail expiré et jeton ancien refusé, marqueur d'effacement manuel protégé |
| CA-12 | Lot : API sources/décisions/confirmation versionnée/arrêt/reprise, rapport interdit après révocation ; acteur de reprise, exclusions, INIT sans effet, états terminaux et bilan par groupe fidèle | Imports et runbook | Stockage privé, fichier abandonné/purge, enrichissement post-import préservé |
| CA-13/14/15 | Localisation/carte : résolution INSEE/homonyme, absence de commune, hors catalogue, points agrégés, dépassement de 500 sans curseur, clic groupe et pagination 25/100 ; mobile/clavier/panne fournisseur | Carte interactive et fallback liste | France métropole/Outre-mer ; aucun contact/note transmis au fournisseur, aucune ville commerciale créée |
| CA-16/17/18 | Rattachement : A/API droits métier, cible de mauvais prospect, répétition, reprise après création externe ; gain conforme | Liens OnBoard/Animation/Achats | Aucun accès/checkout/paiement provoqué par import ou statut |
| CA-19/29 | Identité : D/API/UI toutes combinaisons de rôles/droits, absence de grant implicite, lecture liste/fiche/dossier autorisée et mutations refusées au lecteur, cardinalité des rôles éligibles sans élargissement historique, DTO/menus/registre fermés, CSRF, accès direct, session expirée ; révocation pendant commande/lot/rejeu | ERP profils, contrat droits et PWA | Comptes synthétiques sans droit/lecture/gestion/import/admin, pas d'élargissement SQLAdmin |
| CA-20/21 | Opposition/version : D/SQL course planification-opposition, fermeture pendant batch, réimport/réactivation, contact ciblé vs autre contact, coordonnée opposée réutilisée comme structure, tâche structure sans contact ciblé, correction concurrente et idempotence corps divergent | Politique commune et 409/422 | Aucun rappel sollicitant après opposition avant remise transport, versions et histoire conservées |
| CA-23 | UI parcours documenté : installation → import → fiche/carte → note → rappel → rattachement | Guide CRM, modèle CSV et aide contextuelle | Scénarios automatisés synthétiques ; aucun compte rendu de pilote requis pour clôture |
| CA-24 | **Reporté** : ancien import Gironde/sections communales | Historique E71-EVOL-02, hors V1 actuelle | Pas de fixture Gironde obligatoire pour valider le nouveau CSV |
| CA-25 | PWA/UI manifest/scope/start_url, navigation profonde, retour après auth, offline, mise à jour réelle seulement ; inspection caches et changement de compte | Installation, confidentialité et cycle PWA commun | 360/390/1280 px, clavier, ServiceWorker sans données privées |
| CA-26 | Push : A/API/UI opt-in/refus/unsupported, ownership abonnement, 404/410, panne/réessai/issue incertaine, clic hors session ; report et droits retirés | Préférences, intention/délivrance et états transport | Transport simulé, multi-appareils, aucune fuite de contact sur écran verrouillé |
| CA-27 | Email : D/A outbox éligible, préférence off/on, responsable différent, tâche annulée après enqueue, révocation avant revendication ; aucune régression des autres emails | Charte, garde d'expédition, runbook | Fournisseur simulé, destinataire interne vérifié uniquement, adresse absente/non vérifiée refusée ; preuve E69 liée à email_version, reprise depuis invitation consommée seulement, changement d’adresse entre opt-in/enqueue/envoi, réactivation volontaire et non-régression E69 ; pas de rattrapage massif |
| CA-28 | Import : INIT sur existant ignore tout ; UPSERT complète vide non protégé/ajoute contact/dossier ; notes/statut/rappels/opposition inchangés, absents conservés | Mode et règles par champ | Exemple P0001/P0002, téléphone A→B puis source C garde B ; contexte initial unique |

Compléter les cas performance de l'[architecture](architecture-contrats.md) : pages 25/100 et profondes, lignes SQL réellement lues, mémoire, N/10N, trafic mixte et saturation, import et worker concurrents. Une bonne pagination UI ne prouve pas la pagination SQL.

## Tests et clôture

Suites cibles : `tests/domain/prospection/`, `tests/application/prospection/`, API, PostgreSQL jetable, parcours navigateur CRM et tests transport simulé. Utiliser le [runner isolé backend](../../../../localeo-backend/scripts/validation/test_isolated.py) et les contrôles d'architecture locaux. Aucun accès à TEST partagé, aucune notification réelle implicitement incluse dans les tests.

Pour la clôture : **tests unitaires, intégration et fonctionnels de tous les critères actifs**, avec migrations/restauration synthétique, droits, fournisseurs simulés, PWA, import/reprise et capacité. Aucun pilote commercial, contact de prospect, validation municipale ou compte rendu UX externe ne constitue un critère de clôture. Des tests prévus ou ignorés ne valent jamais réussite. Le critère reporté reste visible comme hors V1 ; l'E71 reste À faire tant que le développement et ses tests ne sont pas effectués.

Les conditions d'activation réelle restent distinctes : configuration des transports, politique de conservation, hébergement et attribution des droits. Une campagne de test locale ne prouve pas un envoi au fournisseur ou une livraison réelle sur tous les navigateurs.

## Conservation et audit : décision restante ARB-07

Aucune durée CRM n'a été établie dans cette tâche. Ne pas importer par analogie les durées de conservation des achats/PIN. Avant données réelles, rattacher à la politique Localeo : prospects/contacts, notes/tâches, oppositions/preuves, fichiers/staging/rapports, clés de rapprochement/protections, idempotence, abonnements/intention/délivrance.

Prévoir déclencheurs et durées par catégorie, stockage SQL/objets/caches/sauvegardes, suppression/anonymisation cohérente et preuve de dry-run. Une lecture interne ne prolonge pas automatiquement la conservation. La purge des clés de source doit empêcher une réimportation silencieuse d'une personne opposée : référence minimale ou mise en quarantaine à requalifier selon la politique retenue, pas recréation aveugle.

Logs techniques : IDs, codes, versions, comptages, durée et corrélation uniquement. Aucun nom de personne, e-mail, téléphone, note, valeur de cellule, URL d'abonnement push ou lien signé. Rapports/fichiers privés à accès contrôlé, aucune copie en Git ou fixture réelle. Le modèle CSV versionné contient seulement ses en-têtes.

## Documentation, démonstration et impacts

- Backend : domaine/API/migrations/worker, CRM et droits ERP, générateur et tests. Enregistrer domaine/tags/contrats à l'implémentation ; pas de fausse route publiée ici.
- Guides canoniques à livrer : prise en main CRM, import/reprise, configuration des droits et rappels, règles de gain/opposition/carte. Ajouter leur export à `documentation.exports.json` quand consommés et tester l'accès du lecteur. La présente conception n'est pas le manuel d'un écran disponible.
- Générateur backend : prospects synthétiques deux périmètres, contacts/homonymes, commune dense/non localisée/hors catalogue/Outre-mer, opposition, tâches, gains et import interrompu. Transports neutralisés. Étendre registre de tables, nettoyage, sauvegarde/restauration pour les nouvelles dépendances.
- Pro/Animation/Marketplace : pas de mutation des données ou nouvelles API publiques ; contrôler les liens consommateurs si leurs destinations sont changées. Les comptes et parcours de vente existants restent propriétaires de leurs règles.
- Geo : fonds/attribution/couverture à configurer et à tester ; aucune donnée CRM transmise au fournisseur, cache communal indépendant des villes marchandes.

## Livraison et reprise prévues

1. Appliquer ARB-04b confirmé (une preuve/un dossier) et tester sur fixtures ; arrêter conservation et paramètres de fournisseurs avant activation réelle.
2. Livrer migration additive/readiness, catalogue/DTO des droits, preuve de vérification d’adresse E69 et backend, fonctionnalités désactivées. Aucune preuve d’adresse créée à partir du seul état ACTIF. Ne pas réserver un numéro SQL dans cette spécification.
3. Livrer PWA CRM, routes privées, manifest/SW, contrats et guides ; configurer stockage, workers bornés, carte et canaux.
4. Exécuter la matrice locale et CI, migration/restauration sur base jetable, tests E69 et non-régression email ; aucune autorisation CRM ajoutée en masse.
5. Après autorisation d'exploitation distincte : vérifier HTTPS/installation, attribution d'un profil de recette, aperçu CSV, notification interne et transports configurés. Les tests déjà effectués restent distingués des observations de cible.
6. En incident : désactiver commandes/imports et producteurs de rappels ; interrompre proprement les lots, préserver groupes validés et états de remise. Ne pas supprimer les tables ni retirer un ancien message déjà remis au fournisseur.

Runbooks à produire : fichier invalide/doublon, résultat inconnu après timeout, conflit tardif, mauvais rattachement, droits retirés pendant lot, tâche annulée pendant envoi, backlog de notifications, panne carte, purge et restauration. Mesures : durée/état des lots, groupes rejetés/protégés/conflits, âge des files, échec/expiration/issue incertaine transport, conflits de version, temps SQL/mémoire, jamais contenu personnel.

## État de cette phase

Sources backend et documentation examinées en lecture ; nouvelle spécification et gabarit documentaire écrits. Revue indépendante des contrats effectuée puis corrections vérifiées : cible des tâches/oppositions, droits de lecture des dossiers, projection cartographique distincte, namespace d'import et cardinalité des droits E69. Aucune contradiction résiduelle identifiée dans ces corrections.

Contrôles documentaires exécutés le **3 novembre 2026**, dans `localeo-projet`, sur la base `7e09409` avec les modifications E71 locales :

- `python scripts/check_guidance.py` : 95 guides, 1 077 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 11 documents, 305 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 134 sources vérifiées.
- Lecture CSV standard du gabarit : 21 en-têtes uniques, concordance exacte avec le dictionnaire ; exemple documentaire : 2 prospects, 2 contacts et 3 dossiers distincts. Contrôle des identifiants : CA-01 à CA-29 sans trou ; seul CA-24 reporté, 28 actifs.
- Les quatre dépôts applicatifs restent propres et inchangés par cette phase. Les travaux locaux étrangers à E71 sont préservés ; aucun commit/push demandé pour cette spécification.

Ces contrôles valident la documentation, pas un import applicatif. **Tests CRM, migrations, import réel, envoi fournisseur et déploiement : non exécutés**, aucun code CRM implémenté par cette demande.

### Reprise et finalisation V1.1 du 3 novembre 2026

Relecture à la demande utilisateur sur base documentaire `3cdbf32` et travaux E71
locaux conservés. L’utilisateur confirme **CSV standard seul** et **une preuve de
gain pour un seul dossier**. Carte interactive maintenue ; aucune question métier
ouverte ne bloque désormais les développements sur données synthétiques.

La revue des producteurs identifie deux lacunes corrigées dans la conception :

1. `UtilisateurInterne.modifier` incrémente `email_version` sans retirer ACTIF :
   l’état actif ne prouve pas la vérification de la nouvelle adresse. Le fait
   versionné est porté par Identité interne, repris uniquement depuis une
   invitation consommée correspondante ; préférence et remise transport le vérifient.
2. Les clés par source ne protègent pas deux créations ressemblantes simultanées de
   sources différentes. Le contrôle de candidats et la création partagent désormais
   une transaction SERIALIZABLE sur toutes les entrées concernées ; décision
   devenue obsolète = réexamen explicite, jamais fusion ou retry aveugle.

Les contrats d’import explicitent aussi sources, décisions d’aperçu, confirmation
et reprise, acteurs, résultats par groupe et états terminaux. Les critères CA-03,
10/11/12/22/27/28 portent les preuves correspondantes. Les tests applicatifs restent
**à produire lors de l’implémentation** ; aucun résultat de revue ne les remplace.

La politique de conservation, le choix/configuration du fond cartographique et
les paramètres de transport restent des conditions d’activation avec données
réelles. Ils ne sont ni des pilotes obligatoires ni des preuves produit acquises.

Contrôles de finalisation exécutés sur cette V1.1 :

- Revue indépendante des contrats après correction : les deux lacunes ci-dessus
  sont levées ; aucune contradiction bloquante identifiée dans les sections relues.
- `python scripts/check_guidance.py` : 95 guides, 1 077 liens, zéro erreur/avertissement.
- `python scripts/check_guidance.py --all-markdown --changed` : 11 documents,
  305 liens, zéro erreur/avertissement.
- `python scripts/sync_documentation.py --check-sources` : 134 documents vérifiés.
- `git -c core.safecrlf=false diff --check` : réussi.
- Contrôle CSV avec la bibliothèque standard Python : 21 colonnes uniques en
  concordance avec le dictionnaire ; exemple de 2 prospects, 2 contacts et 3 dossiers.
  Les 29 identifiants sont présents sans trou ni doublon dans le backlog et la
  matrice ; 28 actifs, CA-24 reporté.
- Les quatre dépôts applicatifs sont propres et inchangés. Seul le dépôt
  documentaire est modifié pour E71 ; les autres travaux locaux sont préservés.

Ces résultats sont documentaires. Aucun test produit CRM, aucune migration,
aucun import réel ni déploiement n’ont été exécutés. Aucun commit ou push n’est
réalisé dans cette phase de spécification.
