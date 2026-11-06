# EPIC 71 — Localeo CRM, prospection Animation et Coffrets

## Références : socle E71-EVOL-03 et extensions E71-EVOL-04/05/06/07

- État produit : **En cours**, selon la [roadmap commune](../README.md).
- Cadrage initial : 2 octobre 2026 ; décisions/imports E71-EVOL-01 et E71-EVOL-02 du 9 octobre ; **recadrage du 3 novembre 2026** à la demande utilisateur.
- [Spécification canonique V1](../../specifications/epic-71-crm-prospection/README.md), [format d'import et gabarit](../../specifications/epic-71-crm-prospection/import-carte.md).
- Socle : implémentation locale du CRM, migrations v290–v293 et vérification sur données synthétiques. Extension E71-EVOL-04 du 4 novembre : qualification structurée et import 2 implémentés localement, tests et limites dans le bilan. Aucun déploiement ou import réel dans cette phase.
- **E71-EVOL-05, 5 novembre 2026 :** demande d’actualisation de qualification à la demande ; [cadrage et proposition de parcours](../../specifications/epic-71-crm-prospection/actualisation-qualification.md). Neuf critères ajoutés, choix recommandés à valider, aucun développement de cette extension réalisé.
- **E71-EVOL-06, 5 novembre 2026 :** [niveau de qualification commerciale](../../specifications/epic-71-crm-prospection/niveau-qualification.md), entrée de menu, calcul sur recherche et carte colorée/filtrable. Choix utilisateur : combiner potentiel, maturité du projet et fiabilité. Dix critères ajoutés ; barème recommandé à valider, non implémenté.
- **E71-EVOL-07, 5 novembre 2026 :** [dates des actions plus explicites](../../specifications/epic-71-crm-prospection/parcours-regles.md#e71-evol-07--dates-des-actions-plus-explicites) : « Action prévue le » et « Me rappeler le », aides courtes et vocabulaire cohérent ; règles conservées, deux critères ajoutés, non implémenté.

**Besoin actuel :** créer une application **Localeo CRM (PWA)** simple pour gérer la prospection commerciale et le suivi de la relation client sur les périmètres Animation et Coffrets. Saisir un prospect et ses contacts, suivre les échanges et étapes, prendre des notes et programmer des rappels WebPush/e-mail facultatif. Réutiliser les profils ERP avec des droits CRM distincts. Initialiser puis enrichir depuis un fichier produit par l'utilisateur depuis Excel, sans écraser le contexte existant.

La cible n'est plus un module de prospection seulement inclus dans l'ERP. La **carte interactive est maintenue en V1 sur confirmation utilisateur**. La V1 reporte les fiches communales enrichies et le parseur spécifique Gironde sur confirmation utilisateur du 3 novembre ; le besoin de réimport est couvert par un CSV standard. Ce report est **confirmé**, sans valider ni implémenter les anciens critères. Le détail historique demeure dans Git ; aucun classeur privé repris dans ce dépôt.

## Résultat attendu

Le commercial ouvre « Aujourd'hui », sait qui rappeler, ouvre une fiche pour retrouver ses contacts et le dernier échange, consigne sa note puis programme la suite. Une association intéressée par une animation et par des coffrets garde une fiche commune, avec deux dossiers commerciaux distincts. Après gain, les échanges restent consultables et les liens vers les applications métier permettent le suivi de la relation.

Acteurs : utilisateurs internes explicitement habilités au CRM ; responsable d'un dossier ou rappel ; administrateur des comptes ERP pour attribution/retrait des droits. Aucun accès prospect ni compte CRM autonome.

## Périmètre V1 retenu

1. **PWA CRM** PC/mobile, installation et identité visuelle Localeo. Depuis la demande du 4 novembre 2026 : domaine dédié `crm.localeo.city` / `test-crm.localeo.city`, même backend et chemin `/internal/crm/`, mêmes comptes ERP avec connexion distincte par domaine ; accès historiques conservés. Voir [activation](../../specifications/epic-71-crm-prospection/exploitation.md#domaine-dédié).
2. **Fiches prospects et contacts** : coordonnées connues, commune, source, plusieurs contacts, notes et chronologie ; recherche, filtres, opposition et archivage.
3. **Dossiers commerciaux** : Animation ou Coffrets ; pour Coffrets, recrutement de partenaire commerçant ou achat entreprises/CSE. Responsable, six étapes simples, priorité normale/haute et prochaine action calculée.
4. **Carte et pilotage quotidien** : carte interactive par commune avec filtres partagés, groupes et accès aux fiches ; Aujourd'hui, suivi par étapes, mes rappels, dossiers sans action ; indicateurs simples, sans prévision de chiffre d'affaires.
5. **Rappels internes** persistants, WebPush volontaire par appareil, e-mail facultatif désactivé initialement ; destinataire = responsable interne, jamais prospect.
6. **Import CSV** : source et références stables, aperçu et bilan, INIT crée les absents ; UPSERT ajoute et complète les champs jamais renseignés, sans remplacer notes, statut, affectation ou rappels.
7. **Rattachements métier** explicites vers ERP/OnBoard, souscriptions Animation et commandes Coffrets, avec les droits de chaque domaine ; aucune conversion implicite.

Compléments recommandés : détection de doublons, responsable et prochaine action visibles, « Ne plus contacter », archivage réversible, filtres conservés et rappel accessible depuis la fiche. Ils évitent les oublis sans ajouter une administration complexe.

### Hors V1 retenue

Import XLSX Gironde et sections communales (CA-24), campagnes automatiques vers les prospects, synchronisation de boîtes mail, scraping/enrichissement, scoring IA, pipeline personnalisable, devis/facturation/paiement, fusion destructive, export massif et modification hors ligne. Le dossier continue de relier les applications métier qui possèdent ces fonctions.

## Décisions conservées et remplacées

- Coffrets comprend les achats entreprises/CSE, sens de « Pro » acquis le 2 octobre ; ne pas confondre avec Localeo Pro ou E72.
- Rattachements et preuves de gain du 9 octobre conservés : commerçant accepté et OnBoard lié, souscription Animation activée payée/gratuite, commande Coffrets payée. Accord verbal et paiement sont distincts.
- La demande du 3 novembre remplace « pas de nouvelle PWA » et ajoute WebPush/e-mail facultatif. Elle remplace l'attribution CRM implicite par des autorisations distinctes gérées dans ERP.
- Pour simplifier, recommandation de six étapes, CSV standard et upsert « compléter sans remplacer », plutôt que mapping mensuel multi-onglets et résolution à trois versions. Les IDs de critères restent stables.
- ARB-04b (une preuve canonique pour un seul dossier gagnant) et le CSV standard seul/report Gironde sont confirmés par l’utilisateur ; ARB-07 (conservation par catégorie) reste à définir avant données réelles. Les autres arbitrages et leur statut figurent dans le [README canonique](../../specifications/epic-71-crm-prospection/README.md).

## Critères d'acceptation

**Socle : implémentation locale réalisée ; preuves et réserves dans le [bilan de vérification](../../specifications/epic-71-crm-prospection/verification-livraison.md).** Les 29 identifiants ci-dessous sont conservés (28 actifs, CA-24 reporté). E71-EVOL-04 ajoute ensuite CA-30 à 40. Les évolutions E71-EVOL-05 à 07 ajoutent CA-41 à 61 : **60 critères actifs et 1 reporté**, dont vingt et un nouveaux à concevoir/implémenter ; ils ne constituent pas des tests réussis.

| Critère | Acteur / action | Résultat observable et refus attendu |
| --- | --- | --- |
| E71-CA-01 | Gestionnaire CRM crée un prospect et ses contacts | Saisie minimale possible, données inconnues visibles, plusieurs contacts ; aucun compte ou objet opérationnel/envoi implicite |
| E71-CA-02 | Ajouter un dossier Animation et un dossier Coffrets ou une nouvelle campagne | Une seule fiche prospect ; étapes, responsables et historique propres, pas d'écrasement d'un dossier passé |
| E71-CA-03 | Changer d'étape, pause/perte/gain/réouverture | Six étapes, motifs sensibles et réexamen, historique ; gain refusé sans preuve canonique ou si elle est attribuée à un autre dossier, aucune activation/paiement par changement d'étape |
| E71-CA-04 | Ajouter/corriger note, appel, rendez-vous ou e-mail consigné | Auteur, dates d'événement/saisie et correction retrouvables ; aucun envoi ou état de délivrance déduit d'une note |
| E71-CA-05 | Planifier, terminer, reporter, annuler ou réaffecter | Responsable habilité, échéance, résultat, retard et prochaine action cohérents ; aucune tâche terminée par consultation |
| E71-CA-06 | Ouvrir Aujourd'hui/Rappels et traiter l'échéance | File interne persistante, retard/jour/à venir et fuseau explicites, aucune duplication au rejeu ; tâche fermée/ancienne échéance ne renotifie pas |
| E71-CA-07 | Rechercher et filtrer les listes et le suivi par étapes | Même périmètre filtré en liste/suivi/carte, compteurs cohérents, pagination serveur, filtres conservés et vide distinct d'une erreur |
| E71-CA-08 | Déposer le CSV, choisir source/mode et prévisualiser | Aperçu sans mutation CRM, compléments/protections/doublons/rejets explicites ; fichier invalide refusé sans exécution ; dossier commercial facultatif, créé seulement avec sa référence et son périmètre explicites, contacts/notes/potentiel importables seuls |
| E71-CA-09 | Corriger/exclure des groupes incomplets ou incohérents | Rapport par ligne et groupe, valeurs non inventées ; aucune application partielle d'un groupe prospect |
| E71-CA-10 | Importer ou saisir un prospect ressemblant à un existant | Clés source stables, comparaison et rapprochement explicites ; jamais de fusion automatique au nom/commune/e-mail générique |
| E71-CA-11 | Réimporter, reprendre après panne ou traiter un lot concurrent | Aucun doublon, aucun écrasement des enrichissements/protections ; révision/candidat de rapprochement changé après aperçu = conflit explicite, y compris entre deux sources ou avec la saisie manuelle |
| E71-CA-12 | Consulter le bilan, arrêter/reprendre un lot | Source/mode/auteur/empreinte/résultats privés traçables ; arrêt conserve les groupes déjà appliqués et leurs enrichissements ultérieurs |
| E71-CA-13 | Ouvrir la carte interactive et un groupe communal | Centres identifiés comme approximatifs, regroupements bornés, mêmes filtres que la liste, accès aux prospects/dossiers sans doublons ; non-localisés toujours accessibles |
| E71-CA-14 | Territoire de saisie limité à la Nouvelle-Aquitaine (demande du 4 novembre 2026) | Création et changement effectif de localisation exigent un INSEE de la région, y compris en INIT/UPSERT ; commune hors catalogue Localeo admise dans la région. Fiches historiques hors région/sans commune conservées et suivi modifiable. Aucun objet Ville créé/publié ; [règles et limites de l'import](../../specifications/epic-71-crm-prospection/import-carte.md#territoire-ouvert-à-la-prospection) |
| E71-CA-15 | Utilisateur PC/mobile/clavier | Liste/fiche/notes/rappels exploitables, actions compréhensibles, retours cohérents, pas de scroll horizontal imposé ; liste utilisable si carte/référentiel indisponible, aucune donnée de contact/note transmise au fond de carte |
| E71-CA-16 | Rattacher un commerçant / ouvrir OnBoard puis reprendre | Droits métier propres, référence et dossier canoniques, historique CRM conservé, pas d'activation ou duplication automatique |
| E71-CA-17 | Rattacher partenaire/souscription Animation | Lien exact, droit vérifié, gain seulement sur activation canonique ; aucune invitation/commande/publication implicite |
| E71-CA-18 | Relier achat/commande Coffrets | Référence typée réelle, distinction estimé/commandé/payé, pas de paiement ni facture déclenchés par CRM |
| E71-CA-19 | Profils internes, session expirée/révoquée ou accès API direct | Contrôles serveur courants, CSRF, mêmes droits globaux, aucune fuite de contact/note et aucun accès SQLAdmin additionnel |
| E71-CA-20 | Marquer Ne plus contacter, réimporter ou rouvrir | Sollicitations bloquées, opposition conservée, levée réservée ; archivage/obsolescence jamais effacés par import |
| E71-CA-21 | Enregistrer ou envoyer des commandes concurrentes | Versions/idempotence/transaction, conflit explicite, notes indépendantes conservées ; révocation prime sur rejeu |
| E71-CA-22 | Consulter indicateurs et dossiers sans action | Prospects/dossiers distincts, gains comptés par preuves canoniques distinctes sans doubler une réouverture, filtres/période affichés, inconnus visibles ; pas de fausse conversion ou de chiffre d'affaires déduit |
| E71-CA-23 | Suivre le guide et le parcours synthétique | Installation/connexion → import → note → rappel → suivi → rattachement vérifiés par tests fonctionnels, documentation disponible selon droits ; pas de pilote externe exigé pour clôturer |
| E71-CA-24 | **Reporté : import spécifique Gironde et sections communales** | Ancien critère conservé ; contrat CSV CA-08 à 12/28 le remplace dans V1 retenue, sans prétendre traiter l'ancien XLSX |
| E71-CA-25 | Installer/ouvrir/actualiser Localeo CRM en PWA | Application nommée et scope propres, domaine dédié configurable, accès historique conservé, routes profondes et retour après connexion sur l'origine courante, mise à jour réelle, écran offline clair sans cache de données privées ; installations et push restent liés à leur origine |
| E71-CA-26 | Activer/refuser WebPush puis recevoir/ouvrir un rappel | Opt-in par appareil, compte interne courant, aucune fuite sur écran verrouillé ; refus/expiration conserve le rappel interne ; retries/report/révocation sans doublons applicatifs |
| E71-CA-27 | Activer/désactiver les rappels par e-mail | Désactivés initialement, destinataire interne seulement, envoi à l'échéance sans rattrapage massif ni fallback implicite ; tâche annulée/droit retiré/adresse modifiée empêche l'envoi encore en attente ; vérification et opt-in liés à la version courante de l'adresse |
| E71-CA-28 | Utiliser le même modèle en INIT puis UPSERT | INIT ignore le prospect déjà connu ; UPSERT complète les vides non protégés et ajoute contacts/dossiers ; notes/statuts/responsables/rappels/oppositions conservés, absents non supprimés |
| E71-CA-29 | Administrateur ERP attribue/retire les droits CRM | Cases consulter/gérer/importer/administrer distinctes et dépendances contrôlées ; aucun droit automatique sur compte non admin existant, menu et API immédiatement cohérents |

## E71-EVOL-04 — qualification structurée, 4 novembre 2026

Demande : intégrer les concepts du classeur de qualification comme attributs
filtrables du CRM. [Spécification V1.2](../../specifications/epic-71-crm-prospection/qualification-structuree.md).
Extension implémentée localement : domaine, API, SQL v293, PWA et CSV 2 ; tests synthétiques et limites dans le bilan. Aucun import réel ni déploiement.
Le statut En cours et les preuves historiques E71-EVOL-03 sont conservés.

- Attributs facultatifs sur prospect/contact/dossier ; évaluations datées et
  relations explicites pour les faits qui ne sont pas une simple valeur courante.
- Classification du potentiel calculée et sourcée, sans remplacer étape,
  priorité, tâches, preuve de gain ou budget réel par une estimation de marché.
- CSV standard format 2, avec protection des données et coexistence du
  format 1. Pas de parseur spécifique XLSX/Gironde ; CA-24 reste reporté.
- La restriction Nouvelle-Aquitaine demeure ; une appartenance territoriale ne
  permet pas de créer un prospect EPCI à siège hors région sous une fausse commune.

Les IDs 01–29 restent inchangés ; les impacts sur 07–14/15/19–23/28 concernent
filtres, import, UX, droits et concurrence. Les critères suivants s’ajoutent sans
déclarer la capacité intégralement acquise : **40 IDs, 39 actifs, 1 reporté** au total.

| Critère ajouté | Acteur / action | Résultat observable et refus attendu |
| --- | --- | --- |
| E71-CA-30 | Gestionnaire renseigne nature/activité d’un prospect | Champs conditionnels, types et nomenclature explicites ; absence conservée, accueil public confirmé seulement avec date/preuve, aucune activation métier |
| E71-CA-31 | Saisir/rechercher SIREN, SIRET ou identité communale | Unité personne morale/établissement distincte ; formats et préfixe cohérents, deux établissements d’un SIREN conservés, aucun rapprochement ou gain implicite |
| E71-CA-32 | Ajouter et choisir une évaluation documentaire | Observation datée/sourcée, comptages cohérents, inconnus distincts de zéro ; référence explicite et classement serveur reproductible, aucune addition des cas incertains ou des canaux commune/EPCI |
| E71-CA-33 | Enregistrer un contrôle terrain, corriger une observation ou ajouter une nouvelle source | Triplet nombre/date/preuve requis pour retenir le terrain ; brouillon visible mais non utilisé ; confirmé immuable, correction liée/historique, aucun remplacement automatique de la référence par un import |
| E71-CA-34 | Qualifier personne/service/accueil et ses coordonnées | Rôle et fiabilité structurés ; vérification liée à la version courante avec preuve/date ; changement rend à revalider, aucun consentement ni portage de tous les dossiers déduit |
| E71-CA-35 | Qualifier un dossier Animation | Besoin, porteur du même prospect, opération/calendrier et budget avec base HT/TTC et preuve ; inconnus non inventés, aucun passage Gagnée ou rappel automatique, champs refusés sur un dossier Coffrets |
| E71-CA-36 | Associer commune/EPCI, couverture de projet et compétences | Relations typées sourcées et datées, membres distincts du siège et de la couverture ; un rattachement courant communal, compétences nuancées, aucune fiche hors région créée implicitement |
| E71-CA-37 | Importer format 1 puis format 2, en INIT et UPSERT | Modèle/format explicites ; version 1 conservée ; blocs cohérents protégés, observations idempotentes et référence non écrasée ; groupe atomique et bilan, aucun historique/étape/tâche/opposition effacé |
| E71-CA-38 | Filtrer et consulter liste/suivi/carte/fiches sur PC/mobile | Attributs filtrables côté serveur, une organisation unique, critères enfant sur le même enfant ; mêmes résultats entre surfaces, historique paginé, inconnus visibles, aucun score transmis aux tuiles |
| E71-CA-39 | Modifier/confirmer/importer simultanément ou avec un droit retiré | Domaine commun, versions/idempotence, référence unique, plan obsolète refusé sans effet partiel ; droits et confidentialité conservés, notes indépendantes préservées |
| E71-CA-40 | Migrer/restaurer/générer un jeu et livrer l’extension | Anciennes fiches et plans format 1 inchangés, aucune confirmation extraite de notes ; fixtures synthétiques, contrats/guides synchronisés et performances mesurées, reprise sans suppression des nouvelles données |

La [matrice de vérification](../../specifications/epic-71-crm-prospection/verification-livraison.md#e71-evol-04--preuves-et-résultats)
relie ces critères aux tests, documents, données synthétiques et opérations.
Tests domaine, HTTP/PostgreSQL, navigateur, migration/restauration et charge exécutés localement ; résultats et réserves dans le bilan. L’epic reste En cours.

## E71-EVOL-05 — actualisation de qualification à la demande, 5 novembre 2026

Demande : pouvoir rechercher des données récentes pour **Identité, Territoire,
Évaluation du potentiel, Activité, Informations de la structure et Contacts**.
Le bouton d’actualisation de page existant ne consulte pas les référentiels.
[Proposition fonctionnelle et sources officielles](../../specifications/epic-71-crm-prospection/actualisation-qualification.md).

Recommandation : une action **Vérifier les données**, une comparaison par blocs,
puis une adoption explicite des propositions choisies. Préserver les données
manuelles, liens d’import, observations confirmées et références. Distinguer
date de consultation, date des données et preuve terrain. Les données publiques
ne certifient pas le rôle commercial d’un contact ni le nombre de commerces
effectivement disponibles pour une animation.

Cette extension fait évoluer l’exclusion historique de synchronisation
Sirene/BANATIC **pour ce seul parcours à la demande**. Pas de collecte automatique
du portefeuille, fusion ou campagne vers les prospects. Les modalités d’adoption,
la méthode du comptage et les adaptateurs de données restent proposés, non
arbitrés implicitement. L’epic reste **En cours** ; CA-01 à 40 et le report de
CA-24 sont conservés. **49 IDs, 48 actifs, 1 reporté** au total.

| Critère ajouté | Acteur / action | Résultat observable et refus attendu |
| --- | --- | --- |
| E71-CA-41 | Gestionnaire demande la vérification d’un prospect | Sélection des six blocs, progression durable et bilan court PC/mobile ; une seconde demande identique retrouve le travail actif, aucune application implicite |
| E71-CA-42 | Rechercher identité, activité et structure par identifiants stables | Correspondance exacte et source adaptée ; absence/ambiguïté/contradiction signalée, aucune fusion ou substitution d’INSEE/SIREN/SIRET ; pas de création ERP |
| E71-CA-43 | Examiner et adopter des propositions | Différences et provenance par groupe cohérent, protection des corrections et du vide explicite ; adoption tracée, refus d’un aperçu périmé ; valeurs absentes non effacées |
| E71-CA-44 | Recalculer potentiel et vérifier le territoire | Nouvelle observation sourcée et méthode/version/couverture connues ; historique confirmé préservé, références choisies explicitement, terrain prioritaire dans la référence retenue ; non applicable sans périmètre, incomplet ou non comparable signalé, aucune population sans millésime ni date d’effet juridique inventée |
| E71-CA-45 | Vérifier les coordonnées publiques et contacts | Contact/service proposé sans doublon implicite ; aucun rôle, consentement ou fiabilité humaine déduit ; adoption d’une coordonnée différente invalide les anciennes vérifications selon les règles existantes |
| E71-CA-46 | Consulter la fraîcheur des informations | Consultation/source/millésime/preuve humaine distincts ; bilan par bloc et données restant à examiner ; une tentative ou une source ancienne ne rend pas la fiche « à jour » |
| E71-CA-47 | Une source échoue, limite le débit ou ne couvre pas le bloc | Échec partiel et reprise explicites, valeurs préservées, aucune fausse donnée ; quotas et mémoire bornés, calcul lourd hors requête interactive et réseau hors transaction |
| E71-CA-48 | Appliquer avec modifications concurrentes ou droits retirés | Droits CRM relus, versions/idempotence contrôlées et audit ; rejet sans écrasement, aucun contact ou dossier hors prospect affecté |
| E71-CA-49 | Livrer l’actualisation et la vérifier | Migrations additives et restauration, fournisseurs fictifs, contrats/consommateurs/guides/générateur cohérents et mesures de capacité ; CSV existants compatibles, aucun test externe ou ancien bilan assimilé à une preuve de cette extension |

Les règles d’adoption recommandées, sources, points à trancher, limites techniques
à chiffrer et la matrice des preuves **prévues** sont dans la proposition canonique.
Il s’agit d’un cadrage ; aucun de ces neuf critères n’est annoncé implémenté.

## E71-EVOL-06 — niveau de qualification commerciale, 5 novembre 2026

Demande : entrée **Qualification**, recherche de prospects, calcul sur l’ensemble
du résultat et pastilles de niveau sur la carte avec filtre multi-niveaux.
[Cadrage canonique](../../specifications/epic-71-crm-prospection/niveau-qualification.md).
L’utilisateur retient explicitement une **priorité commerciale combinant
fiabilité, potentiel et maturité du projet**, plutôt qu’un simple indicateur de
complétude. Les poids/seuils et conditions de fraîcheur restent recommandés.

Le résultat est calculé par objectif et profil ; il ne remplace ni priorité
manuelle, ni étape du dossier, ni classement territorial existant. Aucun dossier
créé pour calculer la maturité d’un prospect importé. Les données absentes ne
deviennent pas un potentiel nul. La carte ne prête pas à une commune le score
d’un commerce ou d’un EPCI localisé au même endroit.

Cette évolution ouvre le scoring déterministe pour cet usage ; scoring IA,
probabilités de vente, campagnes et pipeline configurable restent exclus.
L’epic reste **En cours**. Les IDs et preuves historiques sont conservés :
**59 IDs, 58 actifs, 1 reporté** ; ces dix nouveaux critères ne sont pas implémentés.

| Critère ajouté | Acteur / action | Résultat observable et refus attendu |
| --- | --- | --- |
| E71-CA-50 | Ouvrir Qualification et rechercher des prospects | Entrée de menu dédiée, filtres serveur partagés, total et objectif explicites, navigation PC/mobile ; consultation distincte du calcul |
| E71-CA-51 | Préparer puis lancer le calcul sur la recherche | Toute l’audience autorisée figée, pas seulement la page visible ; règle et base de faits identifiées, confirmation du compte, zéro résultat refusé et double clic dédupliqué |
| E71-CA-52 | Calculer et expliquer le niveau commercial | Potentiel, maturité et fiabilité selon barème de domaine versionné ; contributions, faits/provenance, inconnus/couverture et motifs accessibles, aucun score IA ou probabilité de conversion |
| E71-CA-53 | Évaluer sans dossier ou avec plusieurs projets/types | Sans création de dossier, maturité inconnue explicite ; objectif/profil adaptés, mêmes faits du même dossier admissible, aucun potentiel communal attribué au commerce ou mélange de projets |
| E71-CA-54 | Filtrer et trier Qualification/Prospects/Carte | Objectif, modèle actif, niveaux et états cohérents côté serveur ; inconnus, non calculés et obsolètes filtrables, compteurs par prospects uniques et pagination conservée ; tri par score limité au même profil/modèle sauf calibration commune validée |
| E71-CA-55 | Lire les couleurs d’une commune ou d’un groupe mixte | Niveau du prospect commune uniquement en vue communes ; répartition si plusieurs prospects/niveaux co-localisés, aucune propagation depuis siège EPCI, légende et pictogrammes accessibles, non-localisés accessibles en liste |
| E71-CA-56 | Modifier un fait, une référence, un contact ou une règle après calcul | Résultat daté/historisé et dépendances de tous les dossiers/contacts candidats contrôlées, y compris ajout/réouverture ; ancien niveau à recalculer visible, expiration distinguée de tentative d’actualisation, aucun ancien vert présenté comme actuel |
| E71-CA-57 | Interrompre, reprendre ou lancer des travaux concurrents | Progression durable, unité atomique et idempotente, conflits de versions explicites, droits relus à chaque unité et révocation arrêtant la suite, bilan partiel conservé |
| E71-CA-58 | Consulter un niveau élevé et poursuivre la gestion CRM | Aucune modification de priorité/étape/opposition/archivage/tâche, aucun gain/dossier/envoi/compte implicite ; sollicitation interdite toujours bloquée |
| E71-CA-59 | Migrer, superviser et vérifier le nouveau calcul | Données existantes Non calculé, migration additive/restauration, CSV 1/2 compatibles, supervision du batch, contrats/guides/fixtures cohérents et capacité N/10N mesurée ; tests prévus non assimilés à des réussites |

La spécification conserve le barème 40/35/25 et les seuils comme propositions,
avec profils, preuves et fraîcheur à préciser avant développement dépendant.
La matrice des tests prévus et les impacts sont dans le cadrage canonique.

## E71-EVOL-07 — dates des actions plus explicites, 5 novembre 2026

Demande : remplacer les libellés « Échéance » et « Rappel » par **« Action prévue
le »** et **« Me rappeler le »** avec une aide courte, dans la création, le détail
et le report. [Spécification et matrice](../../specifications/epic-71-crm-prospection/parcours-regles.md#e71-evol-07--dates-des-actions-plus-explicites).
Les règles de date, rappels, notifications et droits restent inchangées.
Cette retouche ne demande ni migration, ni nouveau contrat, ni nouveau batch.
État de cette évolution : **spécifiée, non implémentée** ; epic **En cours**.
CA-01 à 59 restent stables ; total courant **61 IDs, 60 actifs, 1 reporté**.

| Critère ajouté | Acteur / action | Résultat observable et refus attendu |
| --- | --- | --- |
| E71-CA-60 | Planifier, consulter ou reporter une action sur PC/mobile | Libellés « Action prévue le » et « Me rappeler le » cohérents, dates en heure de Paris, aides visibles/accessibles et erreur près du champ ; date affichée en liste identifiée, responsable destinataire non ambigu |
| E71-CA-61 | Saisir un rappel avant/à/après la date de l’action, ou l’omettre à la création | Avant/égal acceptés, après refusé, omission initiale = date de l’action ; retard selon due_at, rappel disponible selon remind_at, report et notifications/préférences inchangés |

Les preuves sont prévues dans la spécification ; aucun test de ce nouveau rendu
n’est annoncé exécuté. Les preuves historiques ne valident pas ces nouveaux libellés.

## Impacts et limites

| Périmètre | Impact |
| --- | --- |
| Backend | Domaine prospection, API privées, persistance additive, import durable, worker/rappels et preuves de gain |
| ERP / E69 | Catalogue fermé des autorisations, API des comptes, écran de profils, menu et liens CRM ; identités actuelles conservées |
| Nouvelle surface CRM | PWA satellite dans le backend proposée ; manifest/scope, navigation, formulaires, listes et notifications |
| Email / WebPush | Transports existants, nouveaux abonnements CRM internes et outbox/déduplication ; pas de campagne prospect |
| OnBoard / Animation / Achats | Liens et lecture de preuves autorisés ; pas de création parallèle d'objets métier |
| Pro / Animation / Marketplace | Pas de nouvelle API publique ni modification directe de ces frontends ; destinataires métier existants préservés |
| Carte / géographie | Centres communaux, communes hors catalogue, regroupement et fallback liste ; composant/fournisseur à sélectionner, configuration et couverture à tester |
| Import / données | CSV documentaire vide fourni ; fichiers réels privés, pas de migration automatique des clients existants ; conservation à arrêter |
| Générateur / tests | Fixtures synthétiques dans le backend : deux périmètres, import/rejeu/conflit, opposition, rappels et profils ; aucun envoi réel |
| Documentation / exploitation | Guides CRM/import/profils, runbooks reprise/notifications, schéma/readiness/capacité et bundle à adapter à l'implémentation |

Ordre de réalisation : domaine/droits et PWA → fiches/notes/suivi/carte → tâches/rappels → import → rattachements/recette. Le [plan de vérification](../../specifications/epic-71-crm-prospection/verification-livraison.md) relie chaque critère aux tests, documents, fixtures et conditions d'activation. Le statut est **En cours** ; le bilan de vérification distingue les tests exécutés et les réserves de livraison.
