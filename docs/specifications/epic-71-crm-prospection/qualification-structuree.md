# E71-EVOL-04 — Qualification structurée des prospects

Spécification **V1.2 du 4 novembre 2026**, demandée après l’analyse du classeur de
qualification Nouvelle-Aquitaine. [Epic et décisions](README.md),
[critères stables](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md),
[matrice de preuves](verification-livraison.md#e71-evol-04--preuves-et-résultats).
État produit : **En cours** ; cette extension est **implémentée localement et vérifiée sur données synthétiques**.

## 1. Objectif et écart avec l’existant

Le commercial doit filtrer les prospects selon leur potentiel, identifier le
porteur, voir ce qui est effectivement vérifié et préparer une proposition adaptée.
Ces informations deviennent des champs et relations du CRM, pas un texte à
rechercher dans les notes. Les informations inconnues restent inconnues.

Le socle antérieur à cette évolution offre organisation, coordonnées, contacts, dossiers à six
étapes, notes, tâches, oppositions et import CSV format 1 de 21 colonnes. L’évolution ajoute les attributs de qualification ci-dessous. La carte indique la commune
de localisation du prospect, pas sa zone d’intervention. Les règles de droit,
gain, opposition, identité de source et protection des corrections sont conservées.

Le changement étend E71-EVOL-03 ; il ne réactive pas le parseur XLSX Gironde ni
le critère reporté CA-24. Aucun score IA, synchronisation Sirene/BANATIC, fond de
carte de couverture, catalogue d’offres ou prévision de ventes n’est ajouté.

## 2. Organisation des informations

| Emplacement | Informations et propriétaire |
| --- | --- |
| Prospect — Identité et activité | Nature de collectivité, identifiants légaux, activité du commerce ; `OrganisationProspect` |
| Prospect — Territoire | Commune existante, appartenance EPCI, membres et population ; identités géographiques et relations typées du domaine Prospection |
| Prospect — Potentiel | Évaluations datées, comptages, sources et preuves ; `EvaluationPotentielProspect` |
| Contact — Rôle et fiabilité | Personne/service/accueil, rôle commercial, vérification ; contact rattaché à l’organisation |
| Dossier Animation — Projet à qualifier | Besoin, porteur, prochaine opération, calendrier et budget ; `QualificationProjetAnimation` liée à `OpportuniteProspection` |

Les champs sont facultatifs et révélés selon le type de prospect/périmètre.
Ils ne deviennent pas un préalable obligatoire pour créer une fiche, ajouter une
note ou un rappel. Les règles existantes de localisation à la création demeurent.

Les entités liées, statuts et compteurs sont stockés explicitement et filtrables ;
les quelques résumés éditoriaux (besoin, intitulé, outils) sont de courts attributs
de leur objet, pas des notes de chronologie utilisées à la place du modèle.

## 3. Dictionnaire : identité, activité et territoire

Les noms techniques suivants servent aux contrats cibles. Texte en UTF-8,
espaces de bord retirés, chaîne vide normalisée en absence. Pas de zéro ou de
valeur « vérifiée » initialisé par migration. Les dates métier sont ISO `YYYY-MM-DD`,
les instants techniques UTC ; une date de vérification/observation ne peut être future.

| Attribut | Type / valeurs / contraintes | Règle et origine Excel |
| --- | --- | --- |
| `sous_type_collectivite` | `COMMUNE`, `EPCI`, `AUTRE_COLLECTIVITE`, ou absent ; seulement pour COLLECTIVITE | Distingue les deux tables du classeur, sans modifier les types généraux existants |
| `nature_epci` | `CC`, `CA`, `CU`, `METROPOLE`, `AUTRE`, ou absent ; seulement EPCI | Nature C de la table intercommunale ; « METRO » devient METROPOLE |
| `niveau_identite` | `PERSONNE_MORALE`, `ETABLISSEMENT`, ou absent | Distingue une organisation et l’un de ses points d’exploitation ; requis avec un identifiant légal |
| `siren` | Chaîne de 9 chiffres ou absente | Identité de la personne morale ; SIREN EPCI A, pas un INSEE |
| `siret` | Chaîne de 14 chiffres ou absente ; réservé au niveau établissement/COMMERCE | SIRET E commerces ; préfixe de 9 chiffres égal au SIREN si les deux sont fournis |
| `code_naf`, `version_naf` | Code texte ≤10 caractères, version de nomenclature ≤30 ; fournis ensemble | NAF F des commerces ; version explicitement déclarée, aucune conversion silencieuse de nomenclature |
| `famille_animation` | `ALIMENTAIRE`, `BOUTIQUES`, `RESTAURATION`, `BEAUTE_COIFFURE`, `SERVICES_PROXIMITE`, `GRANDE_SURFACE`, `AUTRE`, ou absent | Famille H des commerces ; ne prouve pas leur participation à une animation |
| `accueil_public` | `A_QUALIFIER`, `CONFIRME`, `NON_CONFIRME`, ou absent | CONFIRME exige `accueil_verifie_le` et `accueil_preuve_ref` ; une activité NAF compatible seule reste A_QUALIFIER |
| `accueil_verifie_le`, `accueil_preuve_ref` | Date et référence de preuve ≤500 caractères | Référence documentaire ou contrôle observé, pas de pièce jointe binaire ni de téléchargement automatique |

Un SIRET exige niveau_identite=ETABLISSEMENT ; une collectivité identifiée par
SIREN utilise PERSONNE_MORALE. Pour un établissement, le SIREN peut être dérivé
du préfixe SIRET dans l’aperçu, explicitement annoncé ; un SIREN fourni différent
reste un refus. Le format des identifiants ne certifie pas leur existence. La saisie d’un
identifiant n’active aucun commerce, compte Pro, souscription ou lien ERP.
Une commune est identifiée par son INSEE existant, sans lui inventer un SIREN.
Plusieurs établissements peuvent partager un SIREN ; ils ne sont jamais fusionnés
sur cette seule égalité. SIRET égal ou SIREN égal entre deux personnes morales
déclarées produit un candidat à examiner, pas une fusion automatique. Une identité
commune ou EPCI contradictoire bloque la mutation et demande un rapprochement.
La même politique s’applique aux saisies et imports dans la transaction de
détection de ressemblances existante.

### Relations territoriales

- **Commune → EPCI** : relation d’appartenance portant sur INSEE communal et
  SIREN EPCI, avec date d’effet, source et date de référence. Un seul rattachement
  courant par commune ; un remplacement explicite conserve l’historique.
- **Établissement → commune** : réutiliser sa localisation INSEE ; ne pas créer
  une deuxième commune de rattachement concurrente.
- **Projet → communes couvertes** : ensemble d’INSEE, maximum 100 par commande,
  pagination au-delà pour la lecture. Cette couverture n’est ni le siège du
  prospect ni une appartenance administrative. Aucun prospect n’est créé pour
  chaque commune couverte.

L’EPCI est référencé par son SIREN même si sa fiche commerciale n’a pas encore été
créée ; une référence de territoire ne crée pas un prospect ni un dossier. Une
fiche EPCI existante peut être reliée explicitement après vérification du SIREN.
Lire ses communes membres utilise les relations courantes, pas une collection
dupliquée modifiable sur la fiche EPCI. Membres et couverture restent distincts.

Le siège d’un EPCI demeure une commune de localisation explicitement renseignée.
La restriction Nouvelle-Aquitaine des nouvelles fiches/localisations reste en
vigueur : un EPCI à siège hors région n’est pas créé avec un siège fictif pour
porter ses membres régionaux. Les références territoriales peuvent mentionner
un EPCI hors région sans autoriser sa création comme prospect. Les membres hors
région ne deviennent pas des cibles commerciales implicites.

## 4. Évaluations datées du potentiel

Une évaluation est attachée à **un prospect**, un périmètre territorial et une
date d’observation. Elle possède un UUID CRM, une version, un état
`BROUILLON`/`CONFIRMEE`, un auteur et une provenance. Son identité d’import est
`(source_namespace, prospect_ref, evaluation_ref)` ; le numéro de ligne Excel
n’est pas une référence stable.

| Champs | Type et validation |
| --- | --- |
| `date_observation`, `source_libelle`, `source_reference`, `source_date` | Date d’observation requise ; libellé de source 1–200 ; référence ≤500, date de source facultative mais non future ; source_reference requise pour confirmer |
| `perimetre_territorial` | `COMMUNE`, `MEMBRES_NOUVELLE_AQUITAINE`, `COUVERTURE_PROJET` ; pour la troisième valeur, référence d’un projet du même prospect et empreinte de sa couverture au moment de l’évaluation |
| `nb_commerces_documentaires`, `nb_cas_a_verifier`, `nb_actifs_tous_secteurs` | Entiers de 0 à 2 147 483 647 ou absents ; absence ≠ zéro |
| `nb_alimentaire`, `nb_boutiques`, `nb_restauration`, `nb_beaute_coiffure`, `nb_services_proximite`, `nb_grandes_surfaces` | Même borne ; tous renseignés → somme égale à nb_commerces_documentaires, sinon détail explicitement incomplet, jamais rempli de zéros par défaut |
| `population`, `population_annee` | Entier ≥0 et millésime 1900–année d’observation ; fournis ensemble ; millésime et source conservés |
| `population_source_ref`, `population_source_date` | Référence ≤500 et date de source requises avec population ; distinctes de celles du comptage Sirene et des compétences BANATIC |
| `nb_commerces_terrain`, `controle_terrain_date`, `controle_terrain_preuve_ref` | Comptage ≥0, date et référence ≤500 ; le triplet complet est requis pour retenir un comptage terrain confirmé |

Les compteurs « à vérifier » ne s’ajoutent jamais au nombre retenu. La population
et les établissements actifs tous secteurs ne remplacent pas un nombre de
commerces compatibles. Les grandes surfaces ne sont comptées dans leur famille
que si la source les retient explicitement. Aucun contrôle terrain n’est déduit
d’une déclaration d’activité ou d’un contact public disponible.

Le gestionnaire peut enregistrer un brouillon partiel. Confirmer exige périmètre,
dates/provenance valides et au moins un bloc complet parmi comptages, population
et compétences. Chaque bloc fourni doit satisfaire ses dépendances ; une population
ou une compétence connue peut ainsi être confirmée sans nombre de commerces.
Un nombre terrain sans date/preuve maintient l’observation en brouillon et
n’influence ni le ciblage ni un indicateur « vérifié » : retirer ce bloc incomplet
ou le compléter avant de confirmer les autres données dans cette observation.
Une observation ne contenant que des compétences INCONNUE ne prouve aucun fait.
Les évaluations confirmées sont immuables : une correction explicite crée une
nouvelle révision liée à celle corrigée, sans effacer auteur, valeurs et preuve.
Un brouillon se modifie avec sa version attendue. Une confirmation n’efface pas
les évaluations antérieures, même de sources différentes.

### Valeur de référence et classement calculé

La clé territoriale est `(organisation_id, perimetre_territorial, projet_id)` :
projet_id est requis uniquement pour COUVERTURE_PROJET et absent sinon. Chaque
clé possède des références indépendantes pour les blocs COMPTAGES, POPULATION
et COMPETENCES. Chaque référence désigne une évaluation confirmée contenant le
bloc choisi, sélectionnée par un gestionnaire ou à la première importation si
aucune référence de ce bloc n’existe. Un import ultérieur ne remplace pas ce
choix : les observations nouvelles figurent dans « À examiner ». Ainsi une
compétence nouvellement documentée ne remplace pas le comptage retenu.
Une seule référence courante par clé/bloc, mise à jour atomique avec version et
audit ; le gestionnaire peut la changer après comparaison.

Dans l’évaluation du bloc COMPTAGES, la base de ciblage est le triplet terrain confirmé s’il
existe, sinon le nombre documentaire retenu. La projection expose `base= TERRAIN`
ou `DOCUMENTAIRE`, la valeur, la date et la source ; aucun mélange de versions.
Le classement déterministe versionné `SEUILS_ANIMATION_1` donne :

| Base retenue | Commune | EPCI / membres NA |
| --- | --- | --- |
| Absente | NON_EVALUE | NON_EVALUE |
| 0–4 | SOUS_SEUIL | SOUS_SEUIL |
| 5–9 | MUTUALISATION_A_ETUDIER | MUTUALISATION_A_ETUDIER |
| ≥10 | PROSPECTION_COMMUNALE | PROSPECTION_EPCI |

Les portées admissibles sont explicites :

| Prospect / contexte | Portée autorisée | Objet territorial mesuré |
| --- | --- | --- |
| Collectivité COMMUNE, INSEE connu | COMMUNE | Cette commune uniquement ; classement communal |
| Collectivité EPCI, SIREN connu | MEMBRES_NOUVELLE_AQUITAINE | Ses membres NA, pas sa commune de siège ; classement EPCI |
| Tout prospect avec son dossier Animation et une couverture déclarée | COUVERTURE_PROJET + projet_id | Ensemble figé par l’empreinte de couverture ; aucun classement de commune isolée |
| Ancien prospect sans sous-type ou commerce sans projet couvert | Aucune confirmation territoriale implicite | Compléter le contexte avant confirmation ; pas de comptage de commune attribué au commerce |

Deux dossiers d’une organisation possèdent ainsi des références de couverture
distinctes. Une modification de couverture incrémente sa version : les anciennes
observations restent lisibles, mais leurs références sont signalées OBSOLETES
si l’empreinte diffère, et ne fournissent plus les chiffres courants filtrables.
Une nouvelle observation ou un choix explicite d’une observation de même empreinte
est nécessaire ; aucune transposition automatique des comptages.

Le classement indique un potentiel, pas l’étape commerciale. Une priorité normale
ou haute demeure une décision existante du dossier. Pour une couverture de projet
personnalisée, afficher comptage/provenance mais pas une étiquette de commune
isolée. Les totaux documentaires communaux et EPCI ne s’additionnent pas pour
produire un chiffre de marché ou un nombre de prospects uniques.

Les taux de transformation, tarifs simulés et CA de scénario du classeur restent
hors de ces champs. Aucun revenu ni probabilité commerciale n’est inféré.

### Compétences de l’EPCI

Sur une observation d’EPCI, ajouter `competence_commerce`, `competence_tourisme`,
`competence_marches` : `OUI`, `NON`, `INTERET_COMMUNAUTAIRE`, `INCONNUE`.
Les valeurs inconnues ne valent pas NON. Confirmation d’une compétence exige
source/référence et date ; « avec intérêt communautaire » conserve sa nuance.
Utiliser `competences_source_ref` (≤500) et `competences_source_date`, distincts
de la source/date des comptages : la photographie BANATIC et le stock Sirene
peuvent avoir des dates différentes. La compétence ne prouve ni budget ni portage d’une opération. Une évolution des
compétences est une nouvelle observation, pas une réécriture du diagnostic précédent.

## 5. Contact : rôle et fiabilité

| Attribut | Type / règles |
| --- | --- |
| `nature_contact` | `PERSONNE`, `SERVICE`, `ACCUEIL_GENERIQUE`, `A_QUALIFIER` |
| `role_commercial` | `DECIDEUR`, `PORTEUR_OPERATIONNEL`, `RELAIS`, `A_QUALIFIER` ; un accueil générique ne peut devenir décideur sans requalification explicite en personne/service |
| `fiabilite_contact` | `A_QUALIFIER`, `A_REVALIDER`, `VERIFIE` ; absent sur historique non évalué |
| `contact_verifie_le`, `contact_source_ref` | Date et référence ≤500 ; requis pour VERIFIE, jamais déduits de la seule syntaxe d’un e-mail |

La qualité est attachée à la version courante des nom/fonction/coordonnées du
contact. Modifier l’une de ces données rend l’ancienne vérification historique
et place la nouvelle version en A_REVALIDER, sauf nouvelle preuve fournie dans
la même commande. L’email structure et le contact personnel restent distincts.

« Modifier » signifie changer la valeur normalisée, pas simplement réenregistrer
un numéro avec les mêmes espaces de bord.
VERIFIE ne signifie ni consentement commercial, ni vérification d’adresse de
compte interne, ni autorisation de lever une opposition.

Le rôle commercial est un repère général du contact dans son organisation.
Le porteur confirmé d’un projet est exclusivement le lien du dossier décrit
ci-dessous ; un contact marqué PORTEUR_OPERATIONNEL ne devient pas porteur de
tous les dossiers, et un rôle général de décideur ne prouve pas son pouvoir sur
une opération particulière.

## 6. Dossier Animation : qualification du projet

| Attribut | Type / règles |
| --- | --- |
| `besoin_statut`, `besoin_resume` | `A_QUALIFIER`, `IDENTIFIE`, `ABSENT` ; résumé ≤1000, requis pour IDENTIFIE |
| `porteur_statut`, `porteur_contact_id` | `A_RECHERCHER`, `IDENTIFIE`, `CONFIRME`, `ABSENT` ; IDENTIFIE/CONFIRME exigent contact actif du même prospect, autre qu’un simple accueil générique |
| `portage_confirme_le`, `portage_preuve_ref` | Date/référence ≤500 requises pour CONFIRME ; preuve liée à `porteur_contact_version` calculée serveur, aucun transfert automatique à un autre contact |
| `operation_intitule`, `operation_debut`, `operation_fin` | Texte ≤200 ; dates facultatives, fin ≥ début ; dates futures autorisées ici. Sans date, afficher « Calendrier à qualifier », pas un retard |
| `budget_statut`, `budget_montant_centimes`, `budget_devise` | `A_QUALIFIER`, `CONFIRME`, `ABSENT` ; entier ≥0, devise EUR. Montant absent ≠ zéro ; ABSENT interdit un montant ; CONFIRME exige montant, date et preuve |
| `budget_confirme_le`, `budget_preuve_ref`, `budget_base` | Date/référence requises pour montant confirmé ; base `HT`/`TTC` explicite. Budget rattaché au projet, jamais au nombre total de commerces |
| `outils_existants` | Texte de qualification ≤500, facultatif ; pas de connexion ou synchronisation externe |

`porteur_statut_effectif` est une projection contractuelle filtrable : reprend le
statut déclaré tant que le contact lié est actif, de nature admissible et de la
version associée ; sinon IDENTIFIE/CONFIRME deviennent A_REVALIDER. La modification,
obsolescence ou requalification du contact ne détruit pas l’ancienne déclaration
et sa preuve. Le filtre « porteur confirmé » porte sur l’état effectif, avec jointure
aux faits courants du contact ; pas de dépendance à un recalcul différé de toutes
les fiches. Reconfirmer exige de choisir/vérifier le contact courant et une nouvelle
preuve, avec version. A_REVALIDER est calculé, pas une confirmation importable.

Les références de preuve sont des attributs de provenance, pas de longues notes
substituant les valeurs typées. Le budget ne constitue ni proposition tarifaire,
ni paiement, ni preuve de gain. Aucun champ rempli ne change automatiquement une
étape du pipeline, ne crée une commande ou ne notifie un prospect.

Les dossiers Coffrets restent utilisables sans ces champs Animation. Contacts et
évaluations restent séparés entre dossiers : identifier un porteur sur un projet
ne le désigne pas automatiquement sur les autres. Opposition/archivage continuent
de bloquer les sollicitations, même si le dossier devient qualifié.

## 7. Parcours et filtres

Fiche prospect : résumé compact du potentiel (nombre, base, date, classement),
identité, puis sections repliables Territoire, Évaluations et Activité. Une action
principale « Compléter la qualification » ouvre le groupe concerné ; pas de
formulaire imposant tous les champs en permanence. Historique paginé, comparaison
de deux évaluations et action explicite « Utiliser comme référence ».

Contacts : pictogramme et libellé personne/service/accueil, rôle et fiabilité
visibles sans ouvrir une note. Dossier : résumé porteur/besoin/calendrier/budget,
avec liens vers contact et preuves. À 320 px et au clavier : labels explicites,
focus conservé, erreurs près du champ, aucune dépendance à la couleur seule.

Filtres serveur communs liste/suivi/carte, persistés dans l’URL : sous-type, nature
EPCI, famille Animation, classement, base documentaire/terrain, intervalle de
commerces, données non évaluées, EPCI SIREN, besoin, porteur, budget, fiabilité et
présence de données à examiner. Les filtres contact/dossier utilisent EXISTS :
une organisation reste unique même si plusieurs enfants correspondent. Combiner
plusieurs critères dossier exige qu’un **même dossier** les satisfasse ; même
principe pour plusieurs critères de contact. Pas de résultat composé artificiellement
d’un budget du dossier A et d’un porteur du dossier B.

La carte conserve le point du siège/commune ; les champs de couverture ne déplacent
pas le point et n’ajoutent pas de contours géographiques dans cette évolution.
Aucun nom, score détaillé ou preuve n’est transmis au fournisseur de tuiles.

## 8. Import : format 2 et compatibilité du format 1

Le format 1 et son [modèle actuel](modele-import.csv) restent inchangés et pris en
charge. Le serveur actuel refuse les nouvelles colonnes : **ne pas les ajouter
au fichier de production avant livraison du format 2**. Le modèle cible
[format 2](modele-import-qualification-v2.csv) est un gabarit de spécification,
pas une fonctionnalité déjà disponible. Le mode INIT/UPSERT reste indépendant
du numéro de format, choisi explicitement à l’upload ; pas de détection implicite
par noms de colonnes. Fichier et plan conservent le numéro de format.

Le gabarit complet comporte **85 colonnes : 21 existantes et 64 nouvelles**.
Les quatre colonnes de base requises et l’INSEE à la création restent les seuls
prérequis généraux ; les autres colonnes peuvent être omises. Dès qu’un bloc est
utilisé, ses dépendances conditionnelles deviennent obligatoires. En CSV : dates
ISO, entiers sans séparateur ni symbole monétaire, budget en centimes, énumérations
exactes et aucune valeur magique NULL. Le modèle vide n’est pas une obligation
de renseigner 85 cellules par prospect.

Le format 2 reprend les 21 colonnes et ajoute trois familles facultatives :
attributs courants (organisation/contact/dossier), observations versionnées et
appartenance EPCI. Toutes les nouvelles colonnes sont décrites par les noms de
ce document ; les adaptations de noms CSV sont dans le tableau ci-dessous.

| Groupe CSV | Mapping et règles |
| --- | --- |
| Identité/activité | Noms identiques aux attributs §3 ; compléments seulement si vides et non protégés ; conflit d’identité ou contradiction SIREN/SIRET = groupe bloqué |
| Contact | Noms du §5 ; contact_ref requis avec les nouveaux champs comme avec les anciens ; statut vérifié lié aux coordonnées de la même ligne/version |
| Projet Animation | Noms du §6 ; `porteur_contact_ref` remplace l’UUID dans le CSV et se résout sous le même prospect, dans le groupe ou parmi ses contacts déjà liés à cette source ; pas de rôle automatique à partir du nom du contact |
| Observation | `evaluation_ref` requis dès qu’une valeur d’évaluation est fournie ; `evaluation_date`, `evaluation_source`, `evaluation_source_ref`, `evaluation_source_date`, `evaluation_perimetre` correspondent aux métadonnées du §4 ; `evaluation_etat` vaut BROUILLON ou CONFIRMEE. Pas de couverture de projet personnalisée dans ce CSV, seulement COMMUNE ou MEMBRES_NOUVELLE_AQUITAINE |
| Comptages/population/terrain/compétences | Noms du §4. Confirmation exige les mêmes preuves qu’à la saisie ; une colonne de fiabilité ou un nombre ne suffisent pas |
| Appartenance | `epci_siren`, `appartenance_debut`, `appartenance_source_ref`, `appartenance_source_date` ; seulement pour un prospect Commune, INSEE connu. Date d’effet et provenance requises ; SIREN ne crée pas un prospect EPCI |

Les bornes restent 10 Mio, 10 000 lignes logiques, 100 lignes/50 contacts/50
dossiers par groupe. Le nombre de colonnes maximum devient celui du modèle
format 2, sans élargir le parseur du format 1. Au plus 20 évaluations par groupe
et une nouvelle appartenance proposée. Répéter les mêmes références ne multiplie
pas les objets. Les valeurs contradictoires d’un même attribut/référence bloquent
le groupe, indépendamment des contacts/dossiers répétés sur les lignes.

Pour le classeur actuel : communes A→INSEE, D→classement **recalculé**, E/F→comptages,
H:M→familles, O→population/2026, P→epci_siren, T→niveau documentaire à expliciter
par les preuves, U:Y→contact après nettoyage, AG/AH/AJ→triplet terrain.
EPCI C→nature, H→population des membres NA, I/J→comptages, P:R→compétences avec
leur source BANATIC. Commerces E/F/H→SIRET/NAF/famille. Ni l’adresse d’un commerce
ni un département de siège ne deviennent une adresse/INSEE de mairie ou d’EPCI.

Une fiabilité Excel « Contact vérifié » sans date de vérification propre au
contact ne produit pas VERIFIE : conserver la qualification source dans sa
provenance et proposer A_REVALIDER. La date d’annuaire ne devient pas une date
de vérification humaine. « Non confirmé » pour portage ou budget se convertit
en état à qualifier, jamais en ABSENT. Un classement importé n’est pas une colonne
acceptée : le domaine le recalcule à partir de l’observation retenue.

### UPSERT et observations successives

- INIT sur prospect déjà connu continue d’ignorer **tout le groupe**, nouveaux
  attributs/observations inclus ; utiliser UPSERT pour enrichir l’existant.
- Champs courants : compléter les vides jamais protégés ; une différence reste
  visible et conservée en CRM. Ne pas réinitialiser le pipeline, un budget confirmé,
  la fiabilité d’un contact ou un lien de porteur avec une cellule source différente.
- Les faits liés (statut et preuve de vérification, identité légale, budget et
  preuve, porteur et preuve) sont planifiés comme blocs cohérents : si une valeur
  protégée/existante empêche le complément, conserver tout le bloc et montrer la
  divergence. Jamais de statut CONFIRME importé avec le montant ou le contact
  d’une autre version. Ajouter les protections nécessaires aux qualifications de
  dossiers, qui n’ont pas aujourd’hui les champs protégés des organisations/contacts.
- Observations : même evaluation_ref et même contenu = inchangé ; même référence
  avec contenu différent = conflit, jamais remplacement. Une nouvelle référence
  ajoute une observation avec provenance ; elle ne remplace pas la référence active.
- Première observation confirmée sur une clé territoriale sans référence du bloc
  concerné : affectation explicite de ce bloc dans l’aperçu. Plusieurs candidates
  dans le groupe : l’opérateur choisit par bloc, sans choix arbitraire par ordre
  de ligne. Une observation de population ne remplace jamais la référence COMPTAGES.
- Appartenance vide : création possible dans le groupe. Une appartenance existante
  différente n’est jamais remplacée par import ; divergence à traiter manuellement.
- `contexte_initial` conserve sa règle historique : création seulement ; il ne
  reçoit pas automatiquement les valeurs structurées et ne les synchronise pas.

Prospect, champs, contacts, dossiers, observations, éventuelle référence et
appartenance du groupe sont atomiques. Les versions/protections/relations examinées
entrent dans le plan ; une correction manuelle ou un nouveau candidat depuis
l’aperçu produit IMPORT_PLAN_OBSOLETE et aucune écriture partielle. L’opérateur
voit les créations, compléments, valeurs conservées, nouvelles observations et
changements proposés de référence avant confirmation. Aucun effacement par cellule
vide ; aucune suppression d’observation absente du fichier suivant.

Le nouvel import demeure CSV standard : pas de lecture automatique des onglets,
de calcul Excel ou de collecte Web. Les cellules multi-adresses/téléphones doivent
être nettoyées avant dépôt. Les références de preuves ne sont pas visitées à l’import.

## 9. Architecture, API et concurrence

Propriétaire des règles : `app/domaine/prospection`, avec valeurs d’identité,
comptage, preuve datée et classement pures ; observations et relations comme
agrégats explicites. L’application orchestre accès, UoW, contrôle de candidats,
versions et persistance. La projection de classement n’est pas une règle locale
du template JavaScript ou du worker d’import.

Familles implémentées sous `/internal/prospection` :

- PATCH organisation/contact : attributs courants, expected_version et protocole
  idempotent existants ; aucune affectation de statut d’évaluation implicite.
- GET/POST `/organisations/{id}/evaluations`, détail et confirmation/correction
  versionnés ; GET paginé, pas d’historique complet embarqué dans la fiche.
- PUT `/organisations/{id}/evaluation-reference` avec périmètre, evaluation_id,
  bloc, projet_id si couverture et expected_version ; choix confirmé du même
  prospect/clé territoriale contenant le bloc demandé uniquement.
- Commandes d’appartenance sur la commune et de couverture sur le dossier ; dates,
  preuves et versions, pas d’écriture d’une liste inverse EPCI concurrente.
- Qualification du projet comme sous-ressource versionnée du dossier Animation ;
  refus pour un dossier Coffrets, contact tiers ou obsolète.
- Dépôt d’import : `format_version` accepte {1,2} ; valeur
  par défaut 1, contrat de staging et hash incluent le format. Un ancien client
  ne reçoit pas silencieusement un modèle 2.

Toutes mutations : droits courants crm.gerer, CSRF, Idempotency-Key et version
attendue ; importer exige crm.importer en plus. Consulter/historique/preuves :
crm.consulter, mêmes accès privés. Les corps et champs inconnus sont refusés.
Effacer volontairement un champ courant est une action explicite qui pose une
protection contre réimport. Pas de suppression physique d’une observation confirmée.
Références de preuve : texte/HTTP(S) sans identifiants intégrés, pas d’exécution,
d’URL récupérée côté serveur ni de contenu personnel dans les logs.

Nouveaux refus 422 : qualification incomplète, comptages incohérents, portée
invalide, code légal mal formé, contact incompatible ; 409 : version/conflit
d’identité, évaluation immuable, référence d’import contradictoire. Les schémas sont exportés dans l’OpenAPI et les refus portent un code et un message. Droit révoqué prime sur un
rejeu ; conservation/opposition/archivage existants ne sont pas contournés.

Un choix de référence et deux confirmations concurrents n’installent pas deux
références actives ; contrôle de version et unicité par clé territoriale/bloc.
Une appartenance concurrente vérifie la commune sous verrou et les bornes
temporelles. Ordre commun : organisation → contact/dossier → évaluation/relations.
Le worker d’import utilise le même domaine et protocole, sans accès réseau dans
la transaction. Les modifications indépendantes de notes/tâches restent conservées.

Producteur réel : `app/api/prospection_api.py`, `prospection_imports_api.py`,
application service/imports et persistance SQL directe `prospection_core.py` /
`repositories/crm_imports_repository.py` (pas de modèle ORM CRM à supposer). Consommateur : PWA CRM
backend `crm_ui.py` et ses templates/assets ; ERP ne change que si un lien de
résumé est exposé. Contrat documentaire courant : [OpenAPI E71](openapi.json),
générateur backend `scripts/documentation/generate_epic71_openapi.py`.
Les nouveaux schémas sont inclus dans l’OpenAPI V1.2 générée hors ligne depuis les routes réelles.

Les schémas de sortie explicites décrivent les lectures modifiées :
fiche organisation avec identité/activité, référence de potentiel et résumé
calculé ; contact avec nature/rôle/fiabilité et version de vérification ; dossier
avec qualification de projet et état de réexamen ; page d’évaluations avec
items/next_cursor/has_more ; mutation avec id/version/effet. Pas d’historique
complet en liste ni de nouvelles valeurs obligatoires pour les anciennes fiches.
Les anciennes projections/commandes du format 1 continuent d’être acceptées ;
les schémas de sortie et leurs tests doivent prévenir toute fuite de champs
internes, chemins de fichiers, tokens ou pièces de preuve hors des droits CRM.
Pro, Animation, Live, Support et Atelier ne consomment pas ces attributs dans
cette évolution ; aucun nouveau droit à leur attribuer.

## 10. Données, capacité et livraison

Migration additive **v293_crm_qualification.sql**, après v290/v291/v292 : colonnes/valeurs
facultatives d’identité/contact/projet, observations immuables et référence active,
appartenances datées et couverture, index/protections d’import. Pas d’extraction
automatique des anciennes notes, pas d’identité légale ou de confirmation forgée.
Fiches existantes lisibles avec valeurs absentes. La purge/restauration couvre les
preuves, versions, relations et références ; ARB-07 de conservation reste applicable,
sans inventer de durées. Aucune extension de conservation illimitée.

Index à confirmer par les requêtes PostgreSQL : observations
`(organisation_id,perimetre_territorial,date_observation DESC,id DESC)`, unicité
source/prospect/evaluation_ref ; référence active organisation/périmètre/projet/bloc ; unicités partielles distinctes
pour projet absent et projet présent (pas de doublons via NULL) ;
appartenance courante commune unique et `(epci_siren,commune_insee)` ; contacts
organisation/fiabilité et dossiers organisation/statuts de qualification. Identifiants
légaux indexés pour recherche exacte, SIREN non unique pour les établissements.
Les projections courantes pour filtres sont mises à jour dans la transaction du
choix de référence, pas recalculées par scan complet de l’historique à chaque liste.

Listes 25, maximum 100, curseurs stables liés aux filtres/droits/tri/version ;
historique 25 par page, membres et couverture idem, deux évaluations maximum en
comparaison. Fiche : ≤10 requêtes SQL et seulement résumés/enfants bornés ; liste
≤8 requêtes, carte ≤500 groupes comme le socle. Au plus 100 nouveaux membres de
couverture par mutation ; pas de téléchargement préalable de toutes les fiches.

Objectifs à mesurer sur cible jetable : N=10 000 puis 10N=100 000 prospects,
jusqu’à 20 observations par prospect, historiques/communes étrangères augmentés
séparément ; p95 lecture/filtre ≤500 ms et p99 ≤1 s, mutation ≤800 ms/2 s.
Charge mixte initiale : 20 utilisateurs, 20 lectures/s, 5 mutations/s et un import
de 10 000 lignes ; mesurer SQL, plans, mémoire, attentes et reprise après saturation.
Les mesures locales et leurs limites sont consignées dans le bilan ; ces objectifs ne constituent pas une garantie sur TEST. Le worker garde les limites
de groupe/mémoire/bail du socle et ne conserve pas le lot complet hydraté.

Livraison : migration/readiness → backend/contrats/UI format 2 → guides/export
documentaire/générateur synthétique → tests → ouverture explicite du format 2.
Le format 1, anciens plans et fiches restent lisibles. Un plan format 1 ne devient
jamais format 2 ; les anciens plans sont revalidés sans nouveaux effets.
En incident, fermer les nouvelles mutations de qualification/import 2, préserver
les données et la lecture ; pas de rollback SQL destructeur ni ancien binaire
ignorant des versions nouvelles sans validation de compatibilité.

La démonstration devra couvrir mairie, EPCI, deux établissements d’un même SIREN,
contact générique/service/décideur, comptages zéro/inconnus, contrôle terrain complet
ou incomplet, deux dates/sources, opposition et référence protégée. Données fictives,
aucun recopiage du classeur privé ni envoi externe. Les tests attendus et résultats
de cette phase figurent dans la matrice canonique, pas dans un bilan parallèle.


## 11. Repères d’implémentation locale

Le domaine pur est `app/domaine/prospection/qualification.py`. Le service CRM
orchestre les commandes via `app/application/prospection/qualification.py` ;
la persistance SQL est dans `crm_qualification.py` et `prospection_filtres.py`.
Le même domaine valide l’import 2. Aucun attribut n’est extrait des anciennes notes.

Les API supplémentaires sont définies dans `prospection_qualification_api.py` :

| Ressource | Lectures / commandes |
| --- | --- |
| Évaluations | GET/POST organisation → évaluations ; GET/PATCH détail ; POST confirmation/correction |
| Références | GET/PUT `evaluation-reference`, choix par bloc et version ; `projet_id` isole les références de couverture |
| Territoire | GET/PUT `appartenance`, GET `membres` paginé ; GET/PUT dossier → `couverture` |
| Projet | GET/PUT dossier → `qualification`, mêmes droits et idempotence CRM |

`expected_version` concerne l’organisation pour l’appartenance, le dossier pour
la qualification/couverture, l’évaluation pour sa modification/confirmation et
la référence pour son remplacement (0 à la première sélection). La couverture
accepte AJOUTER/RETIRER/REMPLACER par lots de 100 communes, avec lecture paginée.
Une référence devenue obsolète reste consultable mais ne fournit plus de potentiel courant.

Le contrôle d’identité communale s’applique aussi à l’action **Localiser**.
Effacer le sous-type territorial ou l’identifiant connu n’autorise pas un changement
d’identité en deux commandes. Un changement de siège d’EPCI reste permis.
Les coordonnées normalisées inchangées ne dégradent pas la fiabilité du contact.

Aucun déploiement, import de données réelles ou migration TEST n’est inclus.
Les limites de charge, rappels et conservation du socle demeurent dans le
[bilan](verification-livraison.md).


L’indicateur **Nouvelles données à examiner** utilise l’ordre technique des
créations/confirmations et du dernier choix de référence par bloc, sous le même
verrou d’organisation. La date déclarée de la source ne sert pas d’acquittement.
Choisir B après comparaison avec A résorbe l’alerte sans supprimer A. Confirmer
plus tard un ancien brouillon ou importer une observation réactive l’indicateur.
