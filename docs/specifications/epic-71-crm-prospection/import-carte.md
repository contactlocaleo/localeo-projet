# E71 — Import CSV : INIT et UPSERT

Contrat **formats 1 et 2**, actualisé le 4 novembre 2026 pour E71-EVOL-04.
[Périmètre](README.md), [modèle format 1](modele-import.csv),
[modèle format 2](modele-import-qualification-v2.csv),
[dictionnaire de qualification](qualification-structuree.md).
Le format 1 reste le choix par défaut, avec ses 21 colonnes inchangées. Le format 2
est sélectionné explicitement à l’envoi ; le serveur ne le déduit pas des en-têtes.
Le chemin historique `import-carte.md` est conservé pour les liens. L’import reste
un CSV standard ; le parseur du classeur XLSX Gironde n’est pas réactivé.

## Préparer depuis Excel

1. Choisir le format et copier les en-têtes de son modèle dans une feuille dédiée. **Une ligne = un prospect, avec éventuellement un contact, un dossier commercial ou une observation.** Un import de prospection ne crée aucun dossier par défaut. Répéter les mêmes références pour compléter une même structure. Les blocs de qualification du format 2 restent facultatifs.
2. Attribuer des références stables : `P0001` pour le prospect, `C0001` pour le contact, `O0001` pour le dossier. Garder ces références lors des prochains exports, même si les noms ou l'ordre des lignes changent. Ne pas utiliser le numéro de ligne Excel ou le nom de la structure comme identifiant.
3. Formater les références, codes postaux, INSEE et téléphones en **Texte** dans Excel pour conserver zéros initiaux et signes `+`. Exporter des valeurs, pas des formules.
4. Enregistrer en **CSV UTF-8**, séparateur **point-virgule**. Vérifier la première ligne : certains réglages Excel produisent des virgules ; le CRM refuse ce format avec une explication, sans réinterprétation silencieuse. Les champs contenant point-virgule, guillemet ou saut de ligne sont entre guillemets CSV, un guillemet interne est doublé.
5. Dans le CRM, choisir le **Format du fichier**, la source stable, par exemple `prospection-excel`, et le mode **INIT/UPSERT**. Télécharger le modèle correspondant au format sélectionné. Format et mode sont indépendants ; fichier et plan conservent le format choisi. La source est choisie dans une liste de sources existantes ; « Nouvelle source » est une action explicite. Le serveur retire les espaces de bord et passe le nom en minuscules avant validation/unicité : 1–64 caractères `[a-z0-9._-]`. Une création normalisée vers un nom existant propose cette source, sans en créer une autre. Le nom canonique stable est affiché explicitement avant confirmation. Réutiliser exactement cette source aux imports suivants. La source de rapprochement est distincte de la colonne descriptive `source`.
6. Lire l'aperçu, corriger le fichier ou exclure explicitement les groupes en erreur, puis confirmer. Un bilan indique ce qui a réellement changé.

Deux colonnes sont toujours renseignées : **prospect_ref, nom_prospect**. **`code_insee` est obligatoire pour créer un prospect ou enrichir effectivement sa localisation**, en INIT comme en UPSERT. Il peut rester absent pour enrichir seulement les contacts ou le suivi d'une fiche existante. `contact_ref` est requis si des données de contact sont fournies.

**Dossier commercial facultatif, dans les deux formats :** laisser `opportunite_ref`, `perimetre`, `objectif_coffrets`, `titre_opportunite` et les attributs de projet du format 2 vides, ou omettre ces colonnes. Aucune référence ni aucun dossier « Qualification » n’est généré automatiquement. Pour demander un dossier, renseigner explicitement `opportunite_ref` et `perimetre` ; `objectif_coffrets` est alors obligatoire uniquement pour COFFRETS. Des champs de dossier/projet renseignés sans sa référence produisent `DOSSIER_REFERENCE_REQUISE`, sans ignorer silencieusement les données. Les contacts, notes, comptages, observations et appartenances EPCI restent importables seuls.

Un groupe peut mélanger des lignes sans dossier et des lignes demandant un dossier identifié. Les modèles gardent leurs 21/85 en-têtes ; le parseur accepte leur réordre et l'absence des colonnes facultatives, mais refuse les noms inconnus ou dupliqués. Les anciens fichiers avec références de dossier conservent leur comportement. Le rapport distingue ligne CSV logique et groupe prospect.

### Territoire ouvert à la prospection

Depuis le correctif du 4 novembre 2026, les créations et changements effectifs
de localisation sont limités à la **Nouvelle-Aquitaine**. Le code INSEE doit
comporter cinq chiffres et commencer par **16, 17, 19, 23, 24, 33, 40, 47, 64,
79, 86 ou 87**. Une absence produit `COMMUNE_REQUISE`, un format incorrect
`INSEE_INVALIDE`, un autre département `PROSPECT_HORS_NOUVELLE_AQUITAINE`.

L'import contrôle le territoire déclaré par le code, sans appel réseau au
référentiel communal : il ne certifie pas l'existence du code ni sa concordance
avec le nom fourni. La saisie manuelle et **Localiser la commune** vérifient en
complément le référentiel serveur. Les données historiques sont conservées.
Un UPSERT peut ajouter un contact à une ancienne fiche hors région lorsque sa
localisation reste inchangée. Le contrôle intervient après les protections et
la décision d'enrichissement, pas sur les seules cellules brutes du fichier.
INIT déjà connu, groupe protégé ou exclu restent ignorés selon les règles existantes.

Les plans préparés avant cette restriction sont recalculés au traitement : un
groupe devenu incompatible passe en conflit `IMPORT_PLAN_OBSOLETE`, sans aucune
écriture CRM pour ce groupe. Préparer un nouvel aperçu après correction du fichier.

## Dictionnaire des 21 colonnes communes aux deux formats

Toutes les cellules sont des chaînes ; pas de valeur magique `NULL`, de booléen implicite ou de commande d'effacement. Limites applicables après décodage UTF-8.

| Colonne | Règle / exemple | Usage à la création et lors de l'upsert |
| --- | --- | --- |
| `prospect_ref` | Requis, 1–64 caractères `[A-Za-z0-9._-]`, sensible à la casse ; `P0001` | Identifie le prospect dans la source ; ne change jamais |
| `nom_prospect` | Requis, 200 caractères max ; `Association Exemple` | Création ; différent sur une clé existante = divergence d'identité à examiner, pas renommage |
| `type_prospect` | Vide ou `COLLECTIVITE`, `ASSOCIATION`, `COMMERCE`, `ENTREPRISE_CSE`, `AUTRE` | Coordonnée descriptive, complément si jamais renseignée |
| `commune` | Nom déclaré, 150 caractères max | Texte sans création de ville ; ne certifie pas une localisation |
| `code_insee` | Cinq chiffres, département de Nouvelle-Aquitaine ; requis pour une création ou un enrichissement effectif de localisation | Contrôle territorial hors réseau ; existence de la commune non certifiée par l'import |
| `code_postal` | Chaîne de 5 chiffres ou vide | Aucun calcul de commune depuis ce seul champ |
| `adresse` | 300 caractères max | Groupe localisation ; aucune adresse inventée |
| `site_web` | URL HTTP(S), 2 048 caractères max | Jamais visitée pendant l'import |
| `email_structure` | Adresse professionnelle valide, 254 caractères max | Pas de consentement ni clé unique d'organisation |
| `telephone_structure` | Chaîne, 32 caractères max, espaces/ponctuation usuels admis | Pas de numéro fabriqué, pas de déduction de pays silencieuse |
| `contact_ref` | Référence stable 1–64, requise si un champ `contact_*` est fourni | Clé du contact sous ce prospect ; pas d'identification par e-mail seul |
| `contact_nom` | 200 caractères max | Nom connu ; au moins un nom ou une coordonnée valide pour créer un contact |
| `contact_fonction` | 150 caractères max | Fonction professionnelle facultative |
| `contact_email` | Adresse valide, 254 caractères max | Complément seulement ; aucun e-mail envoyé |
| `contact_telephone` | Chaîne, 32 caractères max | Complément seulement |
| `opportunite_ref` | Facultatif ; si un dossier est demandé, référence stable 1–64 | Vide/absent = aucun dossier ; sinon identifie le dossier sous ce prospect, pas la ligne CSV |
| `perimetre` | Requis avec `opportunite_ref` : `ANIMATION` ou `COFFRETS` ; sinon vide | Qualifie le dossier, pas l’intérêt général du prospect ; immutable sur un dossier existant |
| `objectif_coffrets` | COFFRETS : `PARTENARIAT_COMMERCANT` ou `ACHAT_ENTREPRISE_CSE` ; vide pour ANIMATION | Immutable par import sur un dossier existant |
| `titre_opportunite` | 200 caractères max ; vide = libellé du périmètre/objectif | Initialisation d'un nouveau dossier seulement |
| `source` | Provenance descriptive, 300 caractères max | Valeur initiale puis provenance du lot ; ne remplace pas la source déjà renseignée |
| `contexte_initial` | Texte 10 000 caractères max, facultatif | Une note « Contexte initial importé » uniquement pour un prospect nouvellement créé ; ignorée pour tout prospect existant |

Les valeurs répétées pour une même référence doivent être identiques après normalisation documentaire (espaces de bord, fins de ligne) ou vides. Deux valeurs non vides contradictoires bloquent le **groupe prospect entier**. Il ne faut pas répéter des contextes différents selon le contact : le contexte est propre au prospect. Les contacts et dossiers partagent le prospect ; une ligne ne signifie pas « ce contact est l'unique contact de ce dossier ».

### Exemple réduit (données fictives)

Prospect avec un contact, **sans dossier commercial**, dans les deux formats :

```csv
prospect_ref;nom_prospect;code_insee;contact_ref;contact_nom;contexte_initial
P0001;Association fictive;33234;C0001;Camille Exemple;Repères de qualification documentaire
```

Résultat : une fiche, un contact, une note initiale et **zéro dossier**. Un vrai projet
peut ensuite être ajouté depuis la fiche avec **Ajouter un dossier**, ou dans un
import UPSERT avec une référence de dossier explicite. Un réimport sans dossier
ne supprime ni ne modifie les dossiers déjà présents.

Ces colonnes suffisent pour deux périmètres et deux contacts, sans dupliquer la structure :

```csv
prospect_ref;nom_prospect;commune;code_insee;contact_ref;contact_nom;contact_email;opportunite_ref;perimetre;objectif_coffrets;titre_opportunite;contexte_initial
P0001;Association Exemple;Latresne;33234;C0001;Camille Exemple;camille@example.invalid;O0001;ANIMATION;;Animation de printemps;Premier contact à préparer
P0001;Association Exemple;Latresne;33234;C0002;Alex Exemple;alex@example.invalid;O0001;ANIMATION;;Animation de printemps;
P0001;Association Exemple;Latresne;33234;C0001;Camille Exemple;camille@example.invalid;O0002;COFFRETS;ACHAT_ENTREPRISE_CSE;Coffrets pour les bénévoles;
P0002;Commerce Exemple;Latresne;33234;;;;O0001;COFFRETS;PARTENARIAT_COMMERCANT;Recrutement partenaire;
```

Résultat initial attendu : **2 prospects, 2 contacts et 3 dossiers**, une seule note initiale sur P0001. Exemple de format, pas preuve d'import exécuté. Les identifiants de dossier sont propres au prospect ; `O0001` de P0002 n'est pas celui de P0001.

## Format 2 : compléter la qualification sans tout renseigner

Le [modèle format 2](modele-import-qualification-v2.csv) comporte **85 colonnes :
les 21 précédentes et 64 nouvelles**. Les colonnes facultatives peuvent être omises.
Les deux colonnes générales et l’INSEE à la création restent les seuls prérequis
communs ; utiliser un bloc impose ses dépendances et ses preuves. Le format 1
continue de refuser ces nouvelles colonnes : sélectionner le format 2 avant l’envoi.

| Bloc facultatif | Préparation et effets à examiner |
| --- | --- |
| Identité et activité | Sous-type commune/EPCI, niveau d’identité, SIREN/SIRET, NAF et sa version, famille Animation, accueil du public. Les identifiants restent du texte ; un identifiant légal exige son niveau d’identité. Une ressemblance demande un examen, jamais une fusion automatique. |
| Contact | Nature, rôle commercial et fiabilité, sous une `contact_ref` stable. `VERIFIE` exige date et source propres à la vérification ; un libellé Excel ou la date d’un annuaire ne les remplace pas. |
| Projet Animation | Besoin, porteur, opération, calendrier et budget du dossier. `porteur_contact_ref` désigne un contact de ce même prospect ; portage et budget confirmés exigent leurs preuves et dates. Un budget est exprimé en centimes, devise EUR et base HT/TTC explicite. |
| Observation du potentiel | `evaluation_ref` stable requise dès qu’une donnée d’évaluation est fournie ; observation datée, source et périmètre `COMMUNE` ou `MEMBRES_NOUVELLE_AQUITAINE`. `BROUILLON` permet une observation partielle ; `CONFIRMEE` exige des blocs valides et documentés. La couverture personnalisée d’un projet se renseigne dans le CRM, pas dans ce CSV. |
| Comptages, population, compétences | Laisser vide ce qui est inconnu ; zéro reste une mesure explicite. Comptages terrain, population/millésime et compétences EPCI conservent leurs sources, dates et preuves propres. Les cas à vérifier ne s’ajoutent pas au nombre retenu. Aucun classement n’est importé : il est calculé à partir de la référence retenue. |
| Appartenance EPCI | Commune avec INSEE connu : `epci_siren`, `appartenance_debut`, `appartenance_source_ref`, `appartenance_source_date`. Une appartenance différente déjà présente reste conservée. Un SIREN de territoire ne crée pas une fiche commerciale EPCI. |

Les noms, énumérations et dépendances exacts sont dans le
[dictionnaire canonique](qualification-structuree.md#8-import--format-2-et-compatibilité-du-format-1).
Dates ISO `YYYY-MM-DD`, entiers sans séparateur ni symbole monétaire, aucune valeur
magique `NULL`. Nettoyer les cellules contenant plusieurs e-mails ou téléphones
avant l’export. Les preuves sont des références ; elles ne sont pas téléchargées.

### Observations, références et décisions dans l’aperçu

Une `evaluation_ref` inchangée avec le même contenu ne crée pas de doublon ;
un contenu différent sous cette référence produit un conflit. Utiliser une nouvelle
référence pour une nouvelle observation, sans réécrire l’historique confirmé.

L’aperçu distingue les créations, compléments, valeurs conservées, nouvelles
observations et propositions d’appartenance/référence. Si aucun choix de référence
n’existe pour un bloc territorial, la première observation confirmée admissible
peut être proposée. S’il y a plusieurs candidates, **Choisir la référence** permet
de retenir une observation séparément pour **Comptages**, **Population** et
**Compétences**. Le groupe reste à corriger jusqu’à cette décision. Une référence
existante n’est jamais remplacée par un import ultérieur : comparer les nouvelles
observations dans la fiche, puis choisir explicitement la référence à utiliser.

INIT ignore tout le groupe d’un prospect déjà connu par sa clé source, qualifications
incluses. En UPSERT, les champs vides non protégés peuvent être complétés ; un statut
et sa preuve, une identité légale, un budget ou un lien de porteur forment des blocs
cohérents. Une différence ou une protection conserve le bloc courant et signale la
divergence. Une cellule vide n’efface rien. Les nouvelles observations restent à
examiner et ne remplacent ni une correction manuelle ni une référence retenue.

La limite est de **20 évaluations et une nouvelle appartenance proposée par groupe**,
en plus des limites communes ci-dessous. Tous les effets du groupe sont atomiques.
Une modification des versions, protections, candidats ou relations examinés depuis
l’aperçu impose un nouveau plan (`IMPORT_PLAN_OBSOLETE`), sans écriture partielle.

## INIT : créer les absents, sans réinitialiser la base

INIT **ne vide jamais la base**. Pour chaque groupe dont `(source_namespace, prospect_ref)` est absent, l'aperçu propose la création du prospect, de ses contacts et dossiers. Si ce prospect est déjà connu par sa clé, tout le groupe est **ignoré**, même si de nouveaux contacts/dossiers figurent dans ce fichier. Une correspondance possible avec une fiche manuelle ou une autre source bloque le groupe jusqu'à rapprochement explicite ou confirmation de structure distincte.

Les nouveaux dossiers démarrent **À contacter**, priorité normale, responsable du lot choisi explicitement. La source de ces valeurs est le choix du lot, jamais une colonne cachée. Aucune tâche, date de contact ou preuve de gain n'est inventée. Le contexte initial devient une note de provenance une seule fois. Le fichier ne crée aucun rappel ni notification.

INIT peut être rejoué sans créer de doublons. Pour compléter les fiches déjà présentes, utiliser UPSERT ; aucun bouton « écraser tout » n'est prévu.

## UPSERT : enrichir sans remplacer le contexte

| Situation | Traitement |
| --- | --- |
| Clé prospect absente, aucune ambiguïté | Création comme INIT |
| Clé existante, champ descriptif réellement vide et jamais corrigé/effacé manuellement | Complément possible après aperçu, uniquement dans la liste autorisée ci-dessous |
| Valeur CRM identique | Inchangée ; pas de nouvel événement métier |
| Valeur CRM déjà renseignée et différente | Conservée ; différence visible dans le bilan, correction éventuelle depuis la fiche |
| Cellule vide ou colonne facultative absente | Aucun effacement et aucune remise à zéro |
| Champ vidé manuellement ou protégé | Conservé vide ; l'import ne réintroduit pas une donnée volontairement retirée |
| Nouvelle `contact_ref` ou `opportunite_ref` sur un prospect existant | Ajout explicite dans l'aperçu, sans modifier les objets existants ; doublon possible à résoudre |
| Contact obsolète, prospect archivé ou opposé | Aucun enrichissement réactivant la relation ; groupe protégé, ignoré et signalé |
| Ligne/prospect absent du nouveau fichier | Aucune suppression, clôture, annulation ou désaffectation |
| Périmètre/objectif différents pour une opportunité connue, identité incohérente | Conflit bloquant pour le groupe ; pas de déplacement/requalification automatique |
| Nouvelle source ou nouvelles références pour des données ressemblantes | Candidat au rapprochement ; aucun nouveau lien ou fusion implicite |

Liste des compléments du format 1 : type, site web, coordonnées de structure, coordonnées/fonction d'un contact actif et localisation ; le format 2 ajoute les blocs facultatifs décrits ci-dessus. **Localisation = groupe adresse/commune/INSEE/code postal** : compléter seulement si les champs déjà présents sont compatibles ; aucune insertion d'INSEE différent sous une ancienne commune. Les champs protégés à la saisie restent protégés même s'ils redeviennent vides.

**Toujours préservés** sur l'existant : notes/contexte, historique d'échanges, étapes, priorité, responsable, tâches/rappels, oppositions, archivage, contacts obsolètes, preuves/liens métier, choix de notifications, titres/identités et source initiale déjà renseignés. `contexte_initial` d'un prospect existant est signalé comme ignoré ; il n'ajoute pas une nouvelle note à chaque réimport. Un import ne fait pas « avancer » le pipeline.

Exemple : téléphone A importé puis corrigé en B dans le CRM ; fichier suivant C → **B reste conservé**, différence B/C signalée. Un site web jamais renseigné peut être ajouté. Une cellule vide n'efface ni B ni le site. Un nouveau contact avec une nouvelle référence est ajouté après vérification de doublon. Cette V1 ne propose pas de résolution automatique à trois versions ni d'option de remplacement forcé ; mise à jour d'une coordonnée existante dans sa fiche, avec droits/version/audit.

## Identité, aperçu, atomicité et reprise

Clés uniques : prospect `(source_namespace, prospect_ref)` ; contact `(source_namespace, prospect_ref, contact_ref)` ; dossier `(source_namespace, prospect_ref, opportunite_ref)`. Les liens pointent vers des UUID CRM immuables. Une fiche manuelle peut recevoir une clé source après rapprochement explicite ; ce lien ne modifie pas sa fiche. Déplacer une référence vers un autre prospect n'est pas une correction ordinaire d'import.

La confirmation fige fichier, empreinte, source, mode, format, sélection des groupes et versions observées. L'empreinte n'est pas une identité métier. Même plan confirmé + autre clé HTTP = même opération ; un nouveau lot du même contenu reste sans doublon grâce aux clés métier. Un réordre de lignes ne change pas les identités. Les compléments connus sont recalculés lors de la transaction ; une modification des champs, protections ou candidats comparés après aperçu produit un conflit à réexaminer ; une note ajoutée indépendamment est conservée sans invalider ces comparaisons.

Un **groupe prospect** est l'unité atomique : prospect, contacts, dossiers, éventuelle note initiale, qualifications, observations, références, appartenance, provenances et résultat de groupe sont validés ensemble ou pas du tout. Maximum **100 lignes, 50 contacts et 50 dossiers par groupe** ; au-delà, rejeter et proposer de fractionner les enrichissements en plusieurs imports UPSERT. Pas d'état « réussi » avec un contact créé mais un dossier manquant. Les groupes indépendants peuvent réussir malgré un conflit tardif ailleurs : bilan `TERMINE_AVEC_REJETS`, pas de succès global trompeur.

États de lot : DEPOSE → A_CORRIGER/PRET → EN_COURS → TERMINE/TERMINE_AVEC_REJETS ; INTERROMPU, ANNULE et EXPIRE explicites. Avant confirmation, annuler ne crée aucun objet CRM. Après début, arrêter suspend les groupes non appliqués ; pas de rollback global effaçant un enrichissement ultérieur. Reprise du même plan, bail et jeton de clôture, groupe validé jamais réappliqué. Une correction du fichier ouvre un nouveau lot lié.

Recontrôler les droits de l'opérateur avant chaque groupe ; retrait de droit suspend le reste. Deux imports concurrents d'une même source sont sérialisés par bail de source avec jeton de clôture, sans transaction longue ; contraintes uniques et contrôle de version protègent les clés/objets existants. Les ressemblances concurrentes entre sources différentes ou avec une saisie manuelle suivent en plus le protocole ci-dessous. Bilan privé : auteur/date/source/mode/empreinte, créés/complétés/inchangés/protégés/conflits/rejetés, références et numéros de lignes. Les téléchargements exigent le droit d'import courant ; aucun lien public.

### Concurrence entre sources et saisies manuelles

Les clés `(source, référence)` ne suffisent pas à détecter deux créations
simultanées de sources différentes. Toutes les entrées créant une organisation,
un contact ou un dossier candidat au rapprochement, ou modifiant leur identité,
utilisent la même politique de ressemblance. La recherche SQL de candidats et
l’insertion/modification se déroulent dans **une même transaction PostgreSQL
SERIALIZABLE courte**, y compris l’application d’un groupe importé. Aucun appel
réseau ni géocodage n’a lieu dans cette transaction.

La décision « structure distincte » mémorise l’ensemble/version des candidats
examinés. Un candidat apparu depuis l’aperçu invalide cette décision. Une erreur de
sérialisation ou de version produit un groupe en `CONFLIT` et impose un nouvel
aperçu/décision ; aucun réessai aveugle ne transforme une création concurrente en
confirmation de distinction. La saisie manuelle garde ses champs et affiche le
candidat ; l’import conserve les groupes déjà appliqués et signale le groupe refusé.
Tester deux connexions/barrières concurrentes, sources A/B et manuel/import.

Nom, commune ou e-mail générique ne deviennent pas des contraintes d’unicité
métier : deux structures réellement distinctes peuvent être confirmées après
examen. La garantie porte sur les clés et sur le passage obligatoire par le contrôle
de ressemblance défini, pas sur la reconnaissance parfaite de toute identité réelle.
La politique compare les valeurs normalisées exactes nom+commune et coordonnées
connues ; les absences ne constituent pas une égalité, les homonymes restent des
candidats, jamais une preuve de fusion. Pas de rapprochement flou/IA en V1.

### États et bilan sans ambiguïté

- `DEPOSE` : analyse de staging en cours ; `A_CORRIGER` : au moins un groupe retenu
  exige une correction/décision ; `PRET` : les groupes retenus sont applicables
  ou explicitement sans effet. Exclure tous les groupes est refusé ; un INIT ne
  contenant que des clés déjà connues est autorisé avec bilan « aucun changement ».
- La confirmation passe de `PRET` à `EN_COURS` ; nouvel envoi du même plan = même
  lot. Un conflit tardif ne modifie jamais ce plan et produit `TERMINE_AVEC_REJETS`.
  Les autres groupes indépendants peuvent aboutir.
- Arrêt/panne/retrait de droit : `INTERROMPU`, puis reprise avec même plan et droits
  du confirmateur. Les conflits demandent un nouveau plan lié ; pas de réapplication
  des groupes réussis. `ANNULE` exprime l’abandon explicite du reste et est terminal ;
  `EXPIRE` concerne un aperçu non confirmé selon la politique de conservation.
- Un groupe a exactement un résultat terminal : `CREE`, `COMPLETE`, `INCHANGE`,
  `IGNORE_INIT`, `PROTEGE`, `EXCLU`, `CONFLIT` ou `REJETE`. Les nombres de contacts
  et dossiers créés sont des effets séparés, jamais additionnés au nombre de prospects.
  Un champ conservé pour protection n’empêche pas `COMPLETE` pour un autre champ
  admissible du groupe ; le détail liste les deux effets. Un groupe globalement
  opposé/archivé est `PROTEGE`, sans création d’enfant.

Une note n’est créée qu’une fois pour une nouvelle organisation. Une correction
concurrente d’un champ ou de sa protection depuis l’aperçu invalide les versions
observées ; elle ne peut pas être écrasée par le plan. L’ajout indépendant d’une
note est conservé : le plan ne réécrit jamais la chronologie.

## Fichiers et limites

Format CSV UTF-8 avec ou sans BOM, CRLF ou LF, séparateur `;`, guillemets `"`. **10 Mio**, **10 000 lignes logiques**, **21 colonnes maximum pour le format 1, 85 pour le format 2**, en-têtes fermés propres au format sélectionné. Pas de ZIP, XLSX, macro, formule évaluée, HTML rendu ou URL visitée. Dépassement, UTF-8 invalide, en-tête requis absent, guillemet non fermé ou colonne supplémentaire : refus avant mutation. Lecture en flux vers staging privé borné ; ne pas conserver tout le fichier dans la session ORM.

Toute cellule est du texte : un contenu commençant par `=`, `+`, `-`, `@`, tabulation ou retour chariot n'est jamais exécuté. Appliquer les validateurs de champ (le `+` d'un téléphone valide reste permis). À la génération d'un rapport CSV destiné à Excel, neutraliser séparément l'injection de formule et documenter l'échappement ; ne pas modifier la valeur métier stockée pour cela. Les erreurs ne recopient pas les cellules sensibles dans les logs.

Conservation des fichiers/aperçus/rapports et références de rapprochement : politique CRM à fixer avant données réelles, voir [livraison](verification-livraison.md). Le modèle vide est un **gabarit documentaire**, pas un jeu importé ; fichiers réels, parseurs et fixtures exécutables restent hors de ce dépôt documentaire.

## Localisation et carte maintenue en V1

### Périmètre régional — ajustement du 4 novembre 2026

La carte est limitée à la **Nouvelle-Aquitaine (région INSEE 75)**. Le filtre
« Département » propose les douze départements : Charente (16),
Charente-Maritime (17), Corrèze (19), Creuse (23), Dordogne (24), Gironde (33),
Landes (40), Lot-et-Garonne (47), Pyrénées-Atlantiques (64), Deux-Sèvres (79),
Vienne (86) et Haute-Vienne (87).
Référence : [Code officiel géographique INSEE](https://www.insee.fr/fr/metadonnees/geographie/region/75-nouvelle-aquitaine).

- L’API carte impose cette région et combine département, commune, filtres
  commerciaux et emprise avant agrégation. Un rectangle géographique ne suffit
  pas à déterminer l’appartenance régionale : le code INSEE fait foi.
- La vue initiale couvre la région ; le choix d’un département recadre sa zone,
  même sans résultat. Déplacement et dézoom sont bornés sur l’enveloppe régionale.
  « Recentrer » revient à la région ou au département sélectionné. Les raccourcis
  métropole/outre-mer sont retirés. Les enveloppes de navigation sont calculées
  autour des centres communaux du référentiel `geo.api.gouv.fr` avec une marge ;
  elles ne représentent pas les contours administratifs exacts.
- « Voir la liste avec ces filtres » conserve `region=75`, le département et les
  autres filtres ; ouvrir une commune ajoute son code INSEE. La liste générale
  des prospects reste nationale en l’absence de filtre géographique.
- Le compteur et le lien « sans commune · tous territoires » concernent les
  fiches sans code INSEE, selon les autres filtres commerciaux. Ils ne leur
  attribuent aucune région ou département supposé et ignorent l’emprise.
- Le filtre reste utilisable avec la liste des communes si le fond de carte
  n’est pas configuré. Aucun déplacement de fiche ni nouvelle migration.

L'import conserve la commune déclarée et un éventuel code INSEE. Après validation de la fiche, la résolution géographique est une opération distincte, bornée et reprenable, sans modifier l'identité de source. Un code INSEE reconnu permet le centre communal ; un libellé/homonyme exige confirmation. Une indisponibilité géographique n'annule pas un import métier réussi et ne crée pas de fausse position.

Le batch `prospection.imports.traiter` alimente automatiquement le cache des codes
INSEE de Nouvelle-Aquitaine encore absents, même sans lot restant à traiter.
Il couvre aussi les imports déjà terminés et les fiches archivées. Par passage :
au plus 12 départements, 1 000 codes distincts par département et 2 000 communes
dans chaque réponse publique. Le référentiel fournit les centres par
[département](https://geo.api.gouv.fr/decoupage-administratif/communes) ; seul ce
code public est transmis. Aucun réseau dans la transaction d’import ni pendant
une transaction SQL ; les écritures additives conservent tout centre déjà connu.
Un département indisponible ne bloque pas les autres et sera réessayé.

La projection carte expose `geolocalisation_en_attente` : nombre de prospects
sélectionnés ayant un INSEE sans centre connu, après filtres de prospection et
de territoire, avant la fenêtre géographique et le plafond de 500 communes.
Ce compteur est distinct de `sans_commune` (INSEE absent). L’interface explique
l’attente et conserve l’accès à la liste. Un code ancien/inconnu ne produit
aucune position supposée : **Localiser la commune** permet sa résolution explicite.

Le cache de communes CRM conserve INSEE, nom, département/zone, latitude/longitude, source et date de référence. Il est indépendant de la publication des villes marchandes. Une fusion/changement de commune est signalé pour résolution explicite, sans déplacer arbitrairement le prospect. Les coordonnées d'un centre ne sont jamais présentées comme celles de l'établissement.

La carte applique le même filtre que la liste ; emprise et zoom bornés, **500 groupes maximum** par réponse, agrégation serveur au-delà. Réponse propre à la carte : `groups`, `truncated`, `bbox`, `zoom`, `generated_at`, totaux distincts de prospects/dossiers/non-localisés. Il n’y a pas de `next_cursor` sur cette projection ; ouvrir un groupe utilise la liste ordinaire, 25 par page et 100 maximum. `truncated` et total daté signalent si zoom/filtre est requis ; la liste paginée reste exhaustive. Les non-localisés restent visibles dans les compteurs et leur liste. Les points CRM sont dessinés dans le navigateur sans envoyer les attributs prospect au fournisseur de fond. Licence, attribution, couverture, quotas et configuration du fournisseur sont à documenter avant activation ; aucune dépendance cartographique existante n'a été identifiée dans les applications examinées.
