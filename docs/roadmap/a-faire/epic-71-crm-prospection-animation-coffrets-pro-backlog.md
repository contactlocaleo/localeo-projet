# EPIC 71 — CRM de prospection Animation, commerçants partenaires et offre Pro

## Références

- Date de cadrage : **2 octobre 2026**.
- Identifiant : **EPIC-71**, disponible après recherche dans la roadmap commune,
  ses namespaces et les documents applicatifs présents. Les numéros de migration
  SQL ne constituent pas des identifiants d'epic.
- État produit : **À faire**, selon la [roadmap commune](../README.md).
- Demande : centraliser la prospection Animation (collectivités, associations),
  Coffrets (commerçants partenaires et clients de l'offre Pro), initialiser le CRM
  depuis un fichier, visualiser les prospects par ville sur une carte interactive
  de France et suivre états, historique, prochaines actions et rappels.
- Phase réalisée : **cadrage initial**, sans spécification détaillée, import réel,
  implémentation, contact de prospects ou déploiement.
- Décisions utilisateur du 2 octobre : **offre Pro = coffrets pour entreprises/CSE**,
  destinés à leurs salariés ou clients ; **tâches et rappels internes d'abord**.
- Fichier source fourni et examiné en lecture seule :
  `Localeo_Prospection_Gironde-V2.xlsx`, dans le dossier privé de prospection indiqué
  par l'utilisateur. Structure et anomalies utiles décrites ci-dessous ; aucun
  contact ni fichier copié dans Git, aucune correction du classeur effectuée.

### Dépendances et périmètre autonome

L'[EPIC 60](../terminees/epic-60-vision-360-commercialisation-backlog.md) exclut
explicitement un CRM complet ; son suivi léger de référencement ne couvre pas
la prospection. L'[EPIC 68](../en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md)
commence au référencement d'un commerçant et prépare son inscription, pas son
acquisition commerciale. E71 est donc une nouvelle epic en amont, sans rouvrir E60
ni transformer le dossier OnBoard en fichier de prospects.

Réutiliser les [accès ERP E69](../terminees/epic-69-profils-acces-erp-satellites-backlog.md),
les référentiels d'organisations/villes et les parcours métier existants :
[Animation E41](../terminees/epic-41-plateforme-animation-locale-mvp-backlog.md),
[abonnement Animation E47](../terminees/epic-47-souscription-abonnement-partenaire-animation-backlog.md),
[commandes et achats E51](../terminees/epic-51-vision-360-achats-backoffice-backlog.md).
Les liens exacts entre opportunité, partenaire, commerçant et commande seront
spécifiés après vérification de leurs producteurs.

### Existant vérifié en lecture

Exploration ciblée du backend, sans appel externe ni test métier : aucun module
CRM/prospect trouvé dans `app/` ; les notes et relances repérées concernent des
objets opérationnels existants, pas un portefeuille générique de prospection.

- [Référencement commerçant](../../../../localeo-backend/app/application/referencement/use_cases/referencer_commercant.py) :
  crée un commerçant BROUILLON et son profil, avec accès/email optionnels. Ne pas
  l'appeler automatiquement à l'import ; ses contrôles de doublons métier subsistent.
- [Référencement partenaire Animation](../../../../localeo-backend/app/application/animation_locale/use_cases/referencer_partenaire_animation.py) :
  peut orchestrer gestionnaire, habilitations, souscription et checkout/activation
  gratuite. Une « conversion » doit annoncer ces effets et utiliser une action
  explicite ; ce n'est pas une simple insertion d'organisation CRM.
- [Service crédit B2B](../../../../localeo-backend/app/application/conformite_fiscale_bum/service_credit_achat_b2b.py) :
  enregistrer une organisation Pro peut créer un compte crédit et un code.
  Cette identité de facturation/crédit n'est pas un référentiel de prospects à détourner.
- [Ville](../../../../localeo-backend/app/domaine/referencement/entities/ville.py) et
  [intégration géographique](../../../../localeo-backend/app/infrastructure/integrations/geo_api_gouv.py) :
  code INSEE, coordonnées et recherche de communes réutilisables en partie.
  La recherche de proximité actuelle filtre les villes publiées ; le CRM ne doit
  pas reprendre cette restriction pour ses prospects hors catalogue.

## Problème et résultat attendu

Le besoin exprimé est de disposer d'un outil quotidien de prospection dans
Localeo : retrouver qui contacter, pour quelle offre, où se trouve le prospect,
ce qui a déjà été échangé et la prochaine action attendue. Un fichier de départ
doit pouvoir alimenter cette base, sans ressaisie manuelle systématique.

La lecture du fichier identifie des données multi-onglets et une anomalie de
correspondance entre en-têtes et valeurs, détaillées ci-dessous. Aucun taux de
doublons métier ni temps perdu n'est présenté comme mesuré. La réussite sera évaluée
sur un jeu représentatif puis un pilote : prospects retrouvables, historique
fiable, tâches visibles et absence de doublons lors d'un réimport.

**Exemple cible :** une association est contactée pour une animation et souhaite
aussi acheter des coffrets. Une seule organisation et ses contacts sont conservés,
avec deux opportunités aux étapes et échéances indépendantes. La fiche permet
de reprendre le dernier échange, planifier un appel et ouvrir les dossiers métier
issus d'une conversion explicite.

Acteurs : équipe commerciale/Backoffice Localeo, référent d'une opportunité,
administrateur pour configuration/imports sensibles et habilitations. Aucun accès
public au CRM n'est créé pour les prospects dans cette epic.

## Périmètre proposé

Les éléments demandés sont acquis comme besoin. Les choix détaillés ci-dessous
sont des **propositions de cadrage**, à distinguer des arbitrages validés.

### 1. Organisations, contacts et opportunités séparés

Une fiche organisation représente la structure prospectée : collectivité,
association, commerce, entreprise/CSE ou autre type à préciser. Elle contient
nom, identifiants connus, commune/localisation, coordonnées professionnelles,
provenance, responsable et références métier éventuelles. Les champs inconnus
restent inconnus ; un prospect incomplet peut être conservé comme « à qualifier ».

Les contacts portent nom/fonction, coordonnées professionnelles, organisation
et rôle dans l'échange (interlocuteur, décideur, relais, etc.). Plusieurs contacts
sont possibles ; le départ d'un contact ne supprime pas l'historique de la structure.
Une adresse email générique ne constitue pas à elle seule l'identité de l'organisation.

Une opportunité représente un besoin commercial daté. Trois axes proposés :

| Axe | Cibles | Résultat métier poursuivi |
| --- | --- | --- |
| Animation | Collectivités, associations et autres organisateurs autorisés | Préparer une relation partenaire et un projet d'animation, puis orienter vers le parcours existant |
| Partenariat commerçant | Commerces proposant des prestations dans les coffrets | Décision de référencement, puis dossier OnBoard et préparation E68 |
| Offre Pro / achat de coffrets | Entreprises, CSE et autres structures acheteuses | Suivre un besoin d'achat professionnel puis le relier à une commande existante ou préparée par son parcours autorisé |

« Offre Pro » désigne les **commandes de coffrets pour entreprises/CSE**, confirmé
par l'utilisateur. La nature de l'organisation et l'axe commercial
sont indépendants : une entreprise peut acheter des coffrets et proposer des prestations.
Plusieurs opportunités successives du même axe sont possibles (campagnes/événements
distincts), avec historique séparé ; ne pas écraser une affaire gagnée l'année précédente.

Champs d'opportunité utiles proposés : axe, objet/besoin, étape, responsable,
priorité, date cible, prochaine action, échéance, raison de perte ou de pause,
montant/volume estimé facultatif, devise si montant, liens métier et origine.
Une estimation inconnue ne devient pas zéro ; elle n'est pas un chiffre d'affaires réalisé.

### 2. Étapes et historique exploitables

Proposition de parcours commercial commun, avec vocabulaire adapté par axe :

**À qualifier → À contacter → Contact engagé → Besoin qualifié → Proposition
présentée → Décision attendue → Gagnée / Perdue**.

Une opportunité peut être mise en pause avec motif et date de réexamen, ou
réouverte avec justification. Tous les prospects ne passent pas artificiellement
par chaque étape : un saut motivé conserve l'acteur, la date et le motif. Les
conditions de passage « gagnée » doivent être définies par axe avant spécification.
La création d'un compte partenaire ou d'une commande impayée ne prouve pas un gain.

L'état de joignabilité, une opposition à la prospection, l'archivage de la fiche,
l'étape de l'opportunité et les statuts opérationnels restent distincts.
« Ne plus contacter » n'est pas simplement une affaire perdue : il empêche les
nouvelles sollicitations dans le périmètre enregistré, même après import ou réouverture.

Historique : appels, rendez-vous, notes, emails enregistrés manuellement, changements
d'étape, affectations, imports, décisions et liens métier. Distinguer date de
l'événement et date de saisie ; une note disant « mail envoyé » n'est pas une preuve
de délivrance fournisseur. Corrections tracées sans réécriture silencieuse des échanges.
Pas de synchronisation automatique des boîtes mail ni d'enregistrement d'appels en V1 proposée.

### 3. Prochaines actions, rappels et pilotage

Chaque opportunité active doit avoir un responsable et une prochaine action datée,
ou une anomalie de complétude visible. Une tâche porte type (appel, mail, rendez-vous,
préparation, suivi), échéance avec fuseau, responsable, état et résultat.
Réaliser, reporter, annuler ou réaffecter une tâche conserve l'historique.

Vues proposées : portefeuille filtrable, fiche détaillée, tableau par étapes,
« mes actions », actions en retard, sans responsable, sans prochaine action et
en pause à reprendre. Décision V1 : **tâches et rappels internes**, avec proposition
de badge/file d'échéances persistante dans l'ERP. Un éventuel résumé email envoyé
à l'équipe reste à arbitrer ; les relances automatiques aux prospects sont hors V1.

Indicateurs : organisations distinctes, opportunités par axe/étape, tâches échues,
dernière interaction, délais et conversions selon une définition explicite.
Une organisation présente sur deux axes compte une fois comme organisation et deux
fois comme opportunité. Les montants estimés et commandes réellement payées ne se confondent pas.

### 4. Import initial et réimport contrôlé

Prévoir un assistant : sélection du fichier, correspondance des colonnes,
normalisation, aperçu, qualification des anomalies/doublons, validation et compte rendu.
Format **XLSX requis** pour le fichier réel ; CSV proposé comme complément à confirmer. Aucun code,
macro ou formule du classeur n'est exécuté. Séparer clairement lignes d'organisation,
contacts et opportunités si le fichier mélange ces niveaux ; préciser l'axe au
niveau du lot ou de la ligne, sans l'inférer uniquement du type d'organisation.

Champs minimaux proposés : nom de structure ou identité exploitable du prospect,
axe commercial choisi et référence de ligne source. Email/téléphone/ville non
renseignés ne provoquent pas de données inventées : fiche à qualifier, actions de
complétude, absence de point sur la carte si non localisable. Mapping des statuts
historiques explicite ; une valeur inconnue est à qualifier, pas « gagnée » par défaut.

L'aperçu distingue créations, rattachements possibles, mises à jour proposées,
doublons possibles et lignes rejetées avec cause. Ni même nom, ni même commune,
ni même domaine email ne suffisent à fusionner automatiquement deux structures.
Les identifiants officiels éventuels et références métier aident au rapprochement,
sans confondre organisation et établissements. Les contacts et oppositions connus
doivent être pris en compte avant la validation.

L'opérateur confirme le périmètre des lignes retenues ; les lignes exclues restent
dans un rapport identifiable. Un réessai après interruption ou le réimport du
même fichier ne doit pas dupliquer fiches, contacts, opportunités, événements ou
rappels déjà créés. Les changements détectés sont proposés avec comparaison avant/après,
sans écraser notes, propriétaire, opposition ou statut récents par des valeurs anciennes.

Tracer auteur, date, origine, empreinte/version du fichier, mapping, références
de lignes et bilan créé/mis à jour/ignoré/rejeté. Conserver le fichier et les
rapports dans un stockage privé selon la durée à définir, pas dans Git ou les logs.
Une annulation avant validation ne crée rien ; après import, la reprise/correction
du lot doit préserver les données ensuite enrichies et signaler ses limites.
Importer ne crée aucun compte, invitation, inscription, abonnement, commande ou envoi.

#### Lecture du fichier fourni — éléments à prendre en compte

Examen structurel du 2 octobre 2026, fichier de **88 081 octets**, empreinte SHA-256
`3b6e76522ea8ffd7296e7f1fd8f4d65e826f9ec262da98a4e9903e8b0411f17d`.
Lecture OOXML des cellules/en-têtes et valeurs enregistrées, sans recalcul de
formules, modification du fichier, validation des contacts ou consultation de leurs sources web.

| Onglet / plage examinée | Constat vérifié | Conséquence pour le cadrage |
| --- | --- | --- |
| Pipeline qualifié, `A4:AH42` | 34 en-têtes, 38 lignes classées ; territoire/type/EPCI, contact/fonction/téléphone/email, vérification, signaux, angle, offre, prochaine action/statut, sources et composantes de score | Base candidate Animation à qualifier ; dissocier organisation, contact, opportunité, provenance et tâche. Le rang n'est pas une clé métier stable |
| Coffrets & élus 2026, `A7:AG28` | 33 en-têtes, 21 lignes classées par commune ; contacts, centralité, usages, recommandations et contexte institutionnel | Liste de cibles territoriales, pas 21 commerçants ou entreprises/CSE identifiés. Axe et organisation à confirmer par ligne ; ne pas créer de faux établissements |
| Budgets potentiels, `A5:AJ58` | 53 communes, 53 codes INSEE de cinq caractères, 742 cellules de formule ; budgets estimés, sources, type de montant et confiance | Enrichissement potentiel des territoires, pas création de 53 nouveaux prospects ni import de budgets comme commandes/prix contractuels |
| Budgets territoriaux | 28 cellules de formule ; portes d'entrée territoriales et prescripteurs | Distinguer organisme prescripteur, zone couverte et client potentiel ; géographie étendue non réduite à une commune fictive |
| Tableau de bord, Playbook commercial, Sources & méthode, Hypothèses budget, Synthèse budgets | Cinq autres onglets de synthèse, conseils, sources et paramètres ; Synthèse budgets comporte 26 cellules de formule | Ne pas importer ces lignes comme prospects. Conserver la provenance utile, pas recréer un moteur de budget ou scoring automatique en V1 |

**Anomalie de mapping vérifiée :** sur 37 des 38 lignes du pipeline, `Y`
(en-tête « Statut » en Y4) contient une URL et `X` (en-tête « Prochaine action »)
contient « À contacter ». Une ligne contient « À contacter » dans Y. L'assistant
doit détecter cette hétérogénéité, bloquer le mapping aveugle et proposer une
correction/mise à l'écart explicite des lignes concernées. Ne pas décaler toutes
les lignes ni toutes les colonnes automatiquement à partir d'un seul exemple.

Les libellés territoriaux du pipeline recoupent exactement **33** des communes
de Budgets potentiels après suppression des espaces de bord et passage en
minuscules ; ceux de Coffrets & élus recoupent **une** ligne du pipeline selon
cette même méthode. Ce sont des candidats au rapprochement, **pas des doublons
d'organisation certifiés**. L'INSEE disponible doit être vérifié puis utilisé
pour la localisation lorsqu'un rattachement est établi.

Les dates « Vérifié le », sources, score et priorité importés restent des faits
de provenance déclarés par le fichier, pas des validations réalisées par le CRM.
Les valeurs calculées mises en cache ne sont pas recalculées ni certifiées ici.
Le mapping devra choisir explicitement les enrichissements à reprendre ; par
défaut, seules les informations professionnelles utiles sont retenues, sans
profilage personnel d'opinion politique depuis les colonnes de contexte électoral.
Les cases mixtes « coordonnée publique » doivent être séparées en type de contact
validé ou note à qualifier, pas traitées systématiquement comme une adresse email.

### 5. Carte interactive de France

Afficher une carte avec les villes des prospects, un regroupement des points
superposés et une sélection ouvrant les fiches/opportunités associées. Les mêmes
filtres doivent agir sur la carte et la liste : axe, étape, responsable, priorité,
commune/département/région et échéance, selon les données disponibles.

Proposition V1 : **position à la commune**, fondée sur un identifiant de commune
fiable et un centre communal ; ne pas présenter ce point comme une adresse précise.
Les homonymes, codes postaux couvrant plusieurs communes et correspondances ambiguës
sont soumis à confirmation. Les prospects non localisés restent comptés et accessibles
dans une liste dédiée. Plusieurs opportunités d'une structure au même lieu sont
consultables sans ajouter artificiellement des prospects au compteur.

Ne pas limiter le CRM aux villes déjà présentes dans le catalogue marchand.
Une localisation prospective nationale doit pouvoir être qualifiée sans activer
une nouvelle ville commerciale. La couverture métropole/Outre-mer et les structures
multi-établissements/multi-villes restent à préciser. Les rattachements géographiques
sont des filtres, **pas des restrictions d'habilitation par commune**.

La carte ne remplace pas la liste : accès clavier et usage mobile, état de chargement,
erreur de fond de carte et navigation des résultats sans carte. Regroupement et
chargement borné au volume pilote à fixer. Ne transmettre au fournisseur cartographique
aucun nom de contact, email, téléphone, note ou fichier importé ; documenter les
données de localisation strictement nécessaires si un service externe est retenu.

### 6. Passage au métier et droits

Conversion explicite d'une opportunité avec recherche d'un objet existant avant
création, aperçu des données reprises et action autorisée :

- **Commerçant** : rattacher ou référencer par le parcours canonique ; dossier
  OnBoard unique et préparation E68 lorsque disponible. Un simple prospect CRM
  ne possède pas de dossier OnBoard ni de droits de validation de prestations.
- **Animation** : rattacher ou créer le partenaire par son parcours autorisé,
  puis relier le projet. Ne pas fabriquer un abonnement accepté/payé, une animation
  publiée ou une invitation non demandée à partir d'une étape commerciale.
- **Pro** : relier le besoin à l'organisation/commande réellement gérée par
  le domaine achats. Une note « intéressé » ou « gagné » ne crée pas de paiement,
  facture ou commande fictive. La préparation d'une commande utilise ses contrôles existants.

Le CRM conserve ses échanges après conversion et affiche les références métier
sans devenir propriétaire des statuts d'activation, paiement ou onboarding.
Une conversion répétée ou concurrente ne crée pas deux objets métier. Toute
modification ultérieure de données opérationnelles suit leur parcours propriétaire.

Intégration souhaitée dans l'ERP, avec scopes E69 globaux. Proposition de matrice
à confirmer : Backoffice gère la prospection ; Lecteur consulte un périmètre
fonctionnel explicite ; Finance n'obtient pas automatiquement accès à toutes les
notes/contact prospects ; admin historique conserve configuration et administration.
Les droits d'import, export éventuel, fusion, correction et conversion seront
définis par action, vérifiés côté serveur et reflétés dans l'interface. Aucun nouveau
rôle « Commercial » ou découpage territorial n'est imposé sans arbitrage.

### Hors périmètre proposé pour la première version

- Campagnes email/SMS automatiques, séquences marketing, collecte de contacts par
  scraping, enrichissement acheté, synchronisation Outlook/Gmail/Teams et appels enregistrés.
- Scoring IA, prévision financière probabiliste, devis/signature électronique nouveaux.
- Remplacement d'OnBoard, des achats Pro, du contrat Animation ou des référentiels métier.
- ERP comptable, paiement depuis la carte, publication ou activation automatique.
- Application publique pour prospects et application mobile commerciale séparée.

Ces exclusions bornent la proposition V1 ; le suivi et les rappels internes
confirmés par l'utilisateur sont inclus.

## Critères d'acceptation

Ces critères décrivent la cible de cadrage, **pas des tests exécutés**. Les paramètres
non arbitrés sont identifiés dans les questions ouvertes ; leurs choix ne sont pas
présentés comme déjà acceptés.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E71-CA-01 | Backoffice, prospect à saisir | Créer une organisation et ses contacts | Fiche avec origine, type et coordonnées connues ; données manquantes visibles, aucun objet opérationnel/envoi créé implicitement |
| E71-CA-02 | Organisation intéressée par plusieurs offres | Créer deux opportunités d'axes différents ou successives | Une organisation partagée, responsables/étapes/historique propres ; aucune duplication forcée ni écrasement d'affaire passée |
| E71-CA-03 | Opportunité active | Changer d'étape, mettre en pause, perdre ou rouvrir | Acteur/date/motif historisés, motif de perte/pause et réexamen ; « gagnée » conforme aux preuves définies par axe, sans faux paiement/activation |
| E71-CA-04 | Utilisateur autorisé, échange intervenu | Ajouter/corriger un appel, note, rendez-vous ou mail consigné | Date d'événement distincte de saisie, auteur et corrections traçables ; aucun état de délivrance déduit d'une note |
| E71-CA-05 | Opportunité à suivre | Affecter, planifier, terminer, reporter ou annuler une tâche | Responsable/échéance/résultat, retard et absence de prochaine action visibles ; pas de tâche terminée automatiquement par simple consultation |
| E71-CA-06 | Responsable, échéance atteinte | Consulter les rappels et traiter une action | File interne fiable à aujourd'hui/en retard, fuseau explicite, report/réaffectation tracés ; réexécution ne multiplie pas les rappels |
| E71-CA-07 | Portefeuille alimenté | Filtrer/rechercher et passer liste/tableau/carte | Même périmètre et comptages cohérents, pagination/chargement borné ; absence de résultat distincte d'une erreur |
| E71-CA-08 | Opérateur et fichier au format retenu | Mapper les colonnes puis prévisualiser | Aucun écrit métier avant confirmation ; aperçu des créations/mises à jour/doublons/rejets et choix de l'axe ; fichier invalide refusé sans exécution de contenu |
| E71-CA-09 | Fichier comportant manques et erreurs | Corriger ou exclure des lignes puis confirmer | Rapport par ligne, minimum défini, valeurs historiques inconnues à qualifier ; aucun email/ville/statut inventé, lignes exclues identifiables |
| E71-CA-10 | Données déjà connues ou homonymes | Rapprocher avant import ou création | Candidats et différences présentés ; pas de fusion au seul nom/ville/email générique, ni confusion établissement/organisation |
| E71-CA-11 | Lot déjà importé, interrompu ou enrichi depuis | Réessayer/réimporter | Pas de doublons d'objets ou tâches ; mise à jour proposée et protégée contre écrasement d'historique/opposition ; résultat de reprise explicite |
| E71-CA-12 | Opérateur consultant un import réalisé | Ouvrir bilan et provenance, demander correction | Auteur/date/empreinte/mapping/lignes retrouvables, fichier privé, correction bornée sans suppression des enrichissements ultérieurs |
| E71-CA-13 | Plusieurs prospects dans une commune | Ouvrir la carte et un groupe de points | Position communale identifiée comme approximative, liste des structures/opportunités du groupe et accès à leurs fiches |
| E71-CA-14 | Prospect sans localisation ou commune ambiguë | Importer, filtrer et qualifier sa ville | Aucune localisation arbitraire ; file « non localisés », correction explicite ; commune hors catalogue qualifiable sans activation commerciale |
| E71-CA-15 | Mobile/clavier ou fournisseur cartographique indisponible | Naviguer dans le portefeuille | Liste utilisable, erreur carte visible, filtres conservés ; aucun contact/note/fichier transmis au fournisseur de carte |
| E71-CA-16 | Prospect commerçant qualifié, utilisateur habilité | Convertir ou rattacher à un commerçant existant, puis réessayer | Référence canonique et dossier OnBoard unique par parcours autorisé ; aucune activation ou inscription automatique par import/statut CRM |
| E71-CA-17 | Opportunité Animation, utilisateur habilité | Relier/créer le partenaire via son parcours | Historique CRM conservé et lien métier exact ; pas d'abonnement payé, publication, invitation ou projet en double implicitement |
| E71-CA-18 | Opportunité Pro et besoin qualifié | Relier une commande ou ouvrir son parcours de préparation | CRM relie un objet achats réel, distingue estimation/commande/paiement ; aucun paiement ou facture issu du seul statut CRM |
| E71-CA-19 | Profils internes et accès directs API | Lire, importer, modifier ou convertir | Contrôles serveur par scopes/actions, mêmes droits sur toutes communes ; refus sans fuite de contacts/notes, pas de nouvel accès SQLAdmin |
| E71-CA-20 | Opposition ou contact obsolète connu | Planifier une sollicitation, réimporter ou rouvrir une opportunité | Alerte/blocage des nouvelles sollicitations dans le périmètre défini, opposition conservée ; aucun accord de prospection déduit de l'import |
| E71-CA-21 | Deux utilisateurs modifiant la même fiche ou conversion | Enregistrer concurremment | Conflit explicite ou fusion contrôlée de données indépendantes ; aucune perte silencieuse de note/tâche ni double objet opérationnel |
| E71-CA-22 | Responsable du pilotage, données incomplètes | Consulter volumes, étapes, retards et conversions | Organisations/opportunités distinctes, règles de calcul visibles, inconnus séparés, estimation distincte de chiffre d'affaires et devises non additionnées arbitrairement |
| E71-CA-23 | Opérateur novice sur environnement de recette | Suivre le guide puis importer et traiter un prospect | Guide ERP disponible selon droits, exemple anonymisé couvrant import/doublon/carte/relance/conversion, preuves de recette documentées avant clôture |
| E71-CA-24 | Fichier Gironde V2 ou fixture anonymisée conservant sa structure | Prévisualiser les onglets, le mapping et les enrichissements | Synthèses exclues des prospects ; anomalie X/Y du pipeline détectée par ligne ; recoupements et INSEE proposés sans fusion arbitraire ; budgets/scoring restent des estimations sourcées, pas des commandes ni vérifications CRM |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Backend / domaine | **Concerné** : propriétaire métier prospection à définir, organisation/contact/opportunité/tâche/import ; domaine décide étapes et conversion, application orchestre les domaines existants, ERP présente |
| ERP et droits E69 | **Concernés** : navigation CRM, vues/filtres, scopes globaux et droits par action ; import et carte restent privés ; aucun contexte d'autorisation commune |
| Animation / Commerçant / Marketplace | **À examiner** pour liens et rattachement aux parcours existants ; aucune nouvelle interface publique demandée, contrats existants à préserver |
| API / consommateurs | **Concernés** : contrats CRM internes, import asynchrone si volume l'exige, liste/carte cohérentes, reprise/conflits ; consommateurs ERP et domaines convertis à inventorier avant schéma |
| Référentiels géographiques | **Concernés** : villes prospects au-delà du catalogue, identifiants/homonymes, géolocalisation communale et cache ; fournisseur/licence/coût/coverage à choisir en spécification |
| Persistance / migrations | **Concernées** : entités CRM, liens métier, journal/tâches/imports, concurrence et reprise ; aucune migration de toutes les organisations opérationnelles en prospects sans décision |
| Fichier de départ | **Concerné, structure examinée** : XLSX Gironde V2, neuf onglets, sources multi-axes et incohérence X/Y ; mapping métier exact et fixture anonymisée à produire, aucune validation automatique des contacts ou budgets |
| Communications / batchs | **Concernés** pour rappels internes/recalculs si nécessaires ; intégration emails/SMS externes seulement si ajout explicite au périmètre, pas par réutilisation implicite d'E68 |
| Données et conservation | **Concernées** : origine, contacts professionnels, opposition, collecte minimale, correction/archivage/purge et durée par catégorie à définir ; aucun fichier personnel dans Git/démo/logs |
| Générateur / fixtures E63 | **Concernés** : organisations multi-axes, multi-contacts, doublons/homonymes, imports interrompus, points superposés, non localisés, tâches échues, conversions réessayées ; données synthétiques sans prospection réelle |
| Documentation fonctionnelle | **Concernée** : guide commercial/backoffice canonique, import et erreurs, sens des étapes et indicateurs, carte et conversion ; export ERP et accès à tester |
| Exploitation / livraison | **Concernées** : fichiers privés, quotas/limites, traitement d'import et géolocalisation en erreur, sauvegarde/reprise, configuration carte/rappels, migrations puis activation contrôlée |

## Questions ouvertes et propositions

| Arbitrage | Proposition / information attendue | Partie dépendante |
| --- | --- | --- |
| E71-ARB-01 | **Fichier fourni et structure examinée** : XLSX requis. Reste à valider mapping par onglet/ligne, traitement de l'anomalie X/Y, colonnes d'enrichissement, CSV complémentaire et volume futur | Assistant d'import et fixture anonymisée ; aucun import réel pendant le cadrage |
| E71-ARB-02 | **Résolu : coffrets pour entreprises/CSE**, confirmé le 2 octobre | Axe Pro et rattachement au domaine achats, sans nouvelle offre inventée |
| E71-ARB-03 | **Résolu sur le périmètre : tâches et rappels internes d'abord**. File ERP proposée ; résumé email interne éventuel et cadence à préciser | Aucune relance externe automatique V1 ; échéances et suivi interne inclus |
| E71-ARB-04 | Valider les trois axes et le parcours d'étapes proposé ; définir ce qui prouve « gagnée » pour chaque axe et qui peut le constater | Transitions, métriques et conservation des anciens statuts importés |
| E71-ARB-05 | Proposition : Backoffice gestion, Lecteur consultation bornée, Finance sans accès CRM implicite, admin configuration ; décider import/fusion/export et conversion par action | Matrice scopes E69 et affichage des données de contact/notes |
| E71-ARB-06 | Carte communale France proposée ; préciser métropole/Outre-mer, sites multiples/zone de prospection, volume cible et nombre d'utilisateurs | Données géographiques, fournisseur à sélectionner, recette performance et couverture |
| E71-ARB-07 | Définir les règles d'origine des contacts, opposition, conservation et purge des fichiers/notes selon la politique Localeo | Publication des procédures et import exploitable ; pas d'accord commercial fabriqué à partir d'un fichier |
| E71-ARB-08 | Définir le degré de conversion V1 : rattachement et ouverture des parcours existants proposés, puis création orchestrée quand les contrats le permettent | Atomicité inter-domaines, invitation explicite, aucun changement des règles d'achats ou onboarding |

## Découpage et passage à la spécification

1. **Portefeuille et données initiales** : fiches/contacts/opportunités, droits,
   import avec rapprochement, provenance et historique.
2. **Pilotage quotidien** : étapes, tâches, rappels internes, filtres et indicateurs.
3. **Couverture géographique et passage au métier** : carte/listes synchronisées,
   rattachements/conversions, guide, démonstration et reprise opérationnelle.

La carte fait partie de l'epic proposée, même si elle est livrée après le socle.
Une première livraison de fiches ne vaut pas réalisation de tous les critères.
Le [cycle d'epic](../../organisation/cycle-epic.md) s'applique : arbitrages ayant un
effet métier explicites, producteurs/consommateurs examinés, conception canonique
et matrice de preuves avant implémentation. Aucun dossier de spécification vide
n'est créé à cette phase ; priorité et date de livraison restent à décider.
