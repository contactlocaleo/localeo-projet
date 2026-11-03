# E71 — Import CSV : INIT et UPSERT

Contrat **format 1**, spécification V1.1 du 3 novembre 2026. [Périmètre V1](README.md), [modèle vide](modele-import.csv). Le chemin historique `import-carte.md` est conservé pour les liens ; la carte interactive est maintenue en V1 ; seuls le mapping Gironde et les sections communales sont reportés en V1 sur confirmation utilisateur. Ce document remplace leur contrat courant, sans prétendre avoir migré un import existant.

## Préparer depuis Excel

1. Copier les en-têtes du modèle dans une feuille dédiée. **Une ligne = un prospect + un dossier commercial + éventuellement un contact.** Répéter les mêmes références pour ajouter un contact ou un dossier à une même structure.
2. Attribuer des références stables : `P0001` pour le prospect, `C0001` pour le contact, `O0001` pour le dossier. Garder ces références lors des prochains exports, même si les noms ou l'ordre des lignes changent. Ne pas utiliser le numéro de ligne Excel ou le nom de la structure comme identifiant.
3. Formater les références, codes postaux, INSEE et téléphones en **Texte** dans Excel pour conserver zéros initiaux et signes `+`. Exporter des valeurs, pas des formules.
4. Enregistrer en **CSV UTF-8**, séparateur **point-virgule**. Vérifier la première ligne : certains réglages Excel produisent des virgules ; le CRM refuse ce format avec une explication, sans réinterprétation silencieuse. Les champs contenant point-virgule, guillemet ou saut de ligne sont entre guillemets CSV, un guillemet interne est doublé.
5. Dans le CRM, choisir la source stable, par exemple `prospection-excel`, et le mode. La source est choisie dans une liste de sources existantes ; « Nouvelle source » est une action explicite. Le serveur retire les espaces de bord et passe le nom en minuscules avant validation/unicité : 1–64 caractères `[a-z0-9._-]`. Une création normalisée vers un nom existant propose cette source, sans en créer une autre. Le nom canonique stable est affiché explicitement avant confirmation. Réutiliser exactement cette source aux imports suivants. La source de rapprochement est distincte de la colonne descriptive `source`.
6. Lire l'aperçu, corriger le fichier ou exclure explicitement les groupes en erreur, puis confirmer. Un bilan indique ce qui a réellement changé.

Quatre colonnes sont toujours renseignées : **prospect_ref, nom_prospect, opportunite_ref, perimetre**. `objectif_coffrets` est obligatoire uniquement pour COFFRETS ; `contact_ref` uniquement si des données de contact sont fournies. Les autres colonnes peuvent rester vides. Le modèle complet fournit tous les en-têtes ; le parseur accepte leur réordre et l'absence des colonnes facultatives, mais refuse les noms inconnus ou dupliqués. Le rapport distingue ligne CSV logique et groupe prospect.

## Dictionnaire des colonnes

Toutes les cellules sont des chaînes ; pas de valeur magique `NULL`, de booléen implicite ou de commande d'effacement. Limites applicables après décodage UTF-8.

| Colonne | Règle / exemple | Usage à la création et lors de l'upsert |
| --- | --- | --- |
| `prospect_ref` | Requis, 1–64 caractères `[A-Za-z0-9._-]`, sensible à la casse ; `P0001` | Identifie le prospect dans la source ; ne change jamais |
| `nom_prospect` | Requis, 200 caractères max ; `Association Exemple` | Création ; différent sur une clé existante = divergence d'identité à examiner, pas renommage |
| `type_prospect` | Vide ou `COLLECTIVITE`, `ASSOCIATION`, `COMMERCE`, `ENTREPRISE_CSE`, `AUTRE` | Coordonnée descriptive, complément si jamais renseignée |
| `commune` | Nom déclaré, 150 caractères max | Texte sans création de ville ; ne certifie pas une localisation |
| `code_insee` | Chaîne de 5 caractères, référence communale à valider si utilisée ; zéro initial conservé | Groupe localisation cohérent ; ambiguïté/incohérence signalée |
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
| `opportunite_ref` | Requis, référence stable 1–64 | Identifie le dossier sous ce prospect, pas la ligne CSV |
| `perimetre` | Requis : `ANIMATION` ou `COFFRETS` | Immutable par import sur un dossier existant |
| `objectif_coffrets` | COFFRETS : `PARTENARIAT_COMMERCANT` ou `ACHAT_ENTREPRISE_CSE` ; vide pour ANIMATION | Immutable par import sur un dossier existant |
| `titre_opportunite` | 200 caractères max ; vide = libellé du périmètre/objectif | Initialisation d'un nouveau dossier seulement |
| `source` | Provenance descriptive, 300 caractères max | Valeur initiale puis provenance du lot ; ne remplace pas la source déjà renseignée |
| `contexte_initial` | Texte 10 000 caractères max, facultatif | Une note « Contexte initial importé » uniquement pour un prospect nouvellement créé ; ignorée pour tout prospect existant |

Les valeurs répétées pour une même référence doivent être identiques après normalisation documentaire (espaces de bord, fins de ligne) ou vides. Deux valeurs non vides contradictoires bloquent le **groupe prospect entier**. Il ne faut pas répéter des contextes différents selon le contact : le contexte est propre au prospect. Les contacts et dossiers partagent le prospect ; une ligne ne signifie pas « ce contact est l'unique contact de ce dossier ».

### Exemple réduit (données fictives)

Ces colonnes suffisent pour deux périmètres et deux contacts, sans dupliquer la structure :

```csv
prospect_ref;nom_prospect;contact_ref;contact_nom;contact_email;opportunite_ref;perimetre;objectif_coffrets;titre_opportunite;contexte_initial
P0001;Association Exemple;C0001;Camille Exemple;camille@example.invalid;O0001;ANIMATION;;Animation de printemps;Premier contact à préparer
P0001;Association Exemple;C0002;Alex Exemple;alex@example.invalid;O0001;ANIMATION;;Animation de printemps;
P0001;Association Exemple;C0001;Camille Exemple;camille@example.invalid;O0002;COFFRETS;ACHAT_ENTREPRISE_CSE;Coffrets pour les bénévoles;
P0002;Commerce Exemple;;;;O0001;COFFRETS;PARTENARIAT_COMMERCANT;Recrutement partenaire;
```

Résultat initial attendu : **2 prospects, 2 contacts et 3 dossiers**, une seule note initiale sur P0001. Exemple de format, pas preuve d'import exécuté. Les identifiants de dossier sont propres au prospect ; `O0001` de P0002 n'est pas celui de P0001.

## INIT : créer les absents, sans réinitialiser la base

INIT **ne vide jamais la base**. Pour chaque groupe dont `(source_namespace, prospect_ref)` est absent, l'aperçu propose la création du prospect, de ses contacts et dossiers. Si ce prospect est déjà connu par sa clé, tout le groupe est **ignoré**, même si de nouveaux contacts/dossiers figurent dans ce fichier. Une correspondance possible avec une fiche manuelle ou une autre source bloque le groupe jusqu'à rapprochement explicite ou confirmation de structure distincte.

Les nouveaux dossiers démarrent **À contacter**, priorité normale, responsable du lot choisi explicitement (opérateur par défaut). La source de ces valeurs est le choix du lot, jamais une colonne cachée. Aucune tâche, date de contact ou preuve de gain n'est inventée. Le contexte initial devient une note de provenance une seule fois. Le fichier ne crée aucun rappel ni notification.

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

Liste des compléments autorisés : type, site web, coordonnées de structure, coordonnées/fonction d'un contact actif et localisation. **Localisation = groupe adresse/commune/INSEE/code postal** : compléter seulement si les champs déjà présents sont compatibles ; aucune insertion d'INSEE différent sous une ancienne commune. Les champs protégés à la saisie restent protégés même s'ils redeviennent vides.

**Toujours préservés** sur l'existant : notes/contexte, historique d'échanges, étapes, priorité, responsable, tâches/rappels, oppositions, archivage, contacts obsolètes, preuves/liens métier, choix de notifications, titres/identités et source initiale déjà renseignés. `contexte_initial` d'un prospect existant est signalé comme ignoré ; il n'ajoute pas une nouvelle note à chaque réimport. Un import ne fait pas « avancer » le pipeline.

Exemple : téléphone A importé puis corrigé en B dans le CRM ; fichier suivant C → **B reste conservé**, différence B/C signalée. Un site web jamais renseigné peut être ajouté. Une cellule vide n'efface ni B ni le site. Un nouveau contact avec une nouvelle référence est ajouté après vérification de doublon. Cette V1 ne propose pas de résolution automatique à trois versions ni d'option de remplacement forcé ; mise à jour d'une coordonnée existante dans sa fiche, avec droits/version/audit.

## Identité, aperçu, atomicité et reprise

Clés uniques : prospect `(source_namespace, prospect_ref)` ; contact `(source_namespace, prospect_ref, contact_ref)` ; dossier `(source_namespace, prospect_ref, opportunite_ref)`. Les liens pointent vers des UUID CRM immuables. Une fiche manuelle peut recevoir une clé source après rapprochement explicite ; ce lien ne modifie pas sa fiche. Déplacer une référence vers un autre prospect n'est pas une correction ordinaire d'import.

La confirmation fige fichier, empreinte, source, mode, format, sélection des groupes et versions observées. L'empreinte n'est pas une identité métier. Même plan confirmé + autre clé HTTP = même opération ; un nouveau lot du même contenu reste sans doublon grâce aux clés métier. Un réordre de lignes ne change pas les identités. Les compléments connus sont recalculés lors de la transaction ; une modification des champs, protections ou candidats comparés après aperçu produit un conflit à réexaminer ; une note ajoutée indépendamment est conservée sans invalider ces comparaisons.

Un **groupe prospect** est l'unité atomique : prospect, contacts, dossiers, éventuelle note initiale, provenances et résultat de groupe sont validés ensemble ou pas du tout. Maximum **100 lignes, 50 contacts et 50 dossiers par groupe** ; au-delà, rejeter et proposer de fractionner les enrichissements en plusieurs imports UPSERT. Pas d'état « réussi » avec un contact créé mais un dossier manquant. Les groupes indépendants peuvent réussir malgré un conflit tardif ailleurs : bilan `TERMINE_AVEC_REJETS`, pas de succès global trompeur.

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

Format CSV UTF-8 avec ou sans BOM, CRLF ou LF, séparateur `;`, guillemets `"`. **10 Mio**, **10 000 lignes logiques**, **21 colonnes maximum**, en-têtes fermés. Pas de ZIP, XLSX, macro, formule évaluée, HTML rendu ou URL visitée. Dépassement, UTF-8 invalide, en-tête requis absent, guillemet non fermé ou colonne supplémentaire : refus avant mutation. Lecture en flux vers staging privé borné ; ne pas conserver tout le fichier dans la session ORM.

Toute cellule est du texte : un contenu commençant par `=`, `+`, `-`, `@`, tabulation ou retour chariot n'est jamais exécuté. Appliquer les validateurs de champ (le `+` d'un téléphone valide reste permis). À la génération d'un rapport CSV destiné à Excel, neutraliser séparément l'injection de formule et documenter l'échappement ; ne pas modifier la valeur métier stockée pour cela. Les erreurs ne recopient pas les cellules sensibles dans les logs.

Conservation des fichiers/aperçus/rapports et références de rapprochement : politique CRM à fixer avant données réelles, voir [livraison](verification-livraison.md). Le modèle vide est un **gabarit documentaire**, pas un jeu importé ; fichiers réels, parseurs et fixtures exécutables restent hors de ce dépôt documentaire.

## Localisation et carte maintenue en V1

L'import conserve la commune déclarée et un éventuel code INSEE. Après validation de la fiche, la résolution géographique est une opération distincte, bornée et reprenable, sans modifier l'identité de source. Un code INSEE reconnu permet le centre communal ; un libellé/homonyme exige confirmation. Une indisponibilité géographique n'annule pas un import métier réussi et ne crée pas de fausse position.

Le cache de communes CRM conserve INSEE, nom, département/zone, latitude/longitude, source et date de référence. Il est indépendant de la publication des villes marchandes. Une fusion/changement de commune est signalé pour résolution explicite, sans déplacer arbitrairement le prospect. Les coordonnées d'un centre ne sont jamais présentées comme celles de l'établissement.

La carte applique le même filtre que la liste ; emprise et zoom bornés, **500 groupes maximum** par réponse, agrégation serveur au-delà. Réponse propre à la carte : `groups`, `truncated`, `bbox`, `zoom`, `generated_at`, totaux distincts de prospects/dossiers/non-localisés. Il n’y a pas de `next_cursor` sur cette projection ; ouvrir un groupe utilise la liste ordinaire, 25 par page et 100 maximum. `truncated` et total daté signalent si zoom/filtre est requis ; la liste paginée reste exhaustive. Les non-localisés restent visibles dans les compteurs et leur liste. Les points CRM sont dessinés dans le navigateur sans envoyer les attributs prospect au fournisseur de fond. Licence, attribution, couverture, quotas et configuration du fournisseur sont à documenter avant activation ; aucune dépendance cartographique existante n'a été identifiée dans les applications examinées.
