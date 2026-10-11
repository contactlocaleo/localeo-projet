# E71 — Import contrôlé et carte

Références : [arbitrages](README.md), [contrats](architecture-contrats.md). Les paramètres proposés sont des bornes initiales à mesurer, non des volumes déjà testés. Aucun fichier privé n'est présent dans ce dossier.

## Assistant d'import — CA-08 à 12 et 24

1. **Déposer** : contrôler droit d'import, taille réelle, format et stockage privé. Afficher nom expurgé, empreinte SHA-256, onglets détectés et limites. Le dépôt peut créer un lot technique temporaire, jamais une organisation/contact/opportunité.
2. **Mapper** : choisir une famille de source, la zone de données de chaque onglet, les champs cibles, un axe explicite par lot/ligne, les correspondances de statuts et exceptions. Ne pas prendre une ligne de synthèse pour un prospect.
3. **Prévisualiser** : normalisation non destructive, valeur brute conservée en provenance selon conservation, champs cibles, erreurs par cellule, rapprochements candidats, comparatif avant/après. Chaque ligne est à créer, rattacher, mettre à jour, ignorer, corriger ou rejeter.
4. **Décider** : confirmer chaque ambiguïté ou exclure les lignes correspondantes avec motif. L'interface affiche le nombre de structures, contacts, opportunités et tâches, pas seulement les lignes.
5. **Confirmer** : l'opérateur confirme le plan et sa version ; le serveur relit droits, versions, oppositions et validité du plan. Un fichier ou mapping modifié invalide l'aperçu ; aucun traitement d'un plan périmé.
6. **Suivre et reprendre** : progression durable, bilan paginé et téléchargement privé autorisé. Un délai réseau n'invite pas à redéposer le fichier ; l'écran retrouve le lot par son ID.

Le rapport inclut feuille/ligne/champ/code d'erreur et IDs créés/rattachés, sans secrets. Il est visible uniquement aux rôles d'import autorisés. Les contenus dangereux sont échappés à l'affichage ; un futur export tableur neutraliserait les formules, mais n'est pas ajouté implicitement au périmètre.

## Import mensuel et deltas — E71-EVOL-01, décision du 9 octobre

Le fichier Gironde est reçu **chaque mois**. Le parcours cible est « Imports → Importer le fichier du mois → Examiner les changements → Confirmer ». Le premier import configure un profil **Prospection Gironde** ; les suivants réutilisent ses onglets, colonnes, règles de normalisation, correspondances de provenance et exceptions validées. Aucun remapping complet mensuel requis si la structure reste compatible.

Le profil est versionné. Détecter les colonnes par en-têtes et signature de structure, pas uniquement par lettre Excel. Nouvelle colonne, colonne manquante ou règle X/Y non applicable : afficher l’écart et demander seulement les décisions nécessaires. Les plages du fichier V2 décrites plus bas sont des constats du premier fichier, **pas des limites fixes de lignes** pour les mois suivants. Détecter les nouvelles lignes jusqu’à la fin des données dans les limites techniques ; exclure les synthèses. La règle X/Y sauvegardée ne s’applique qu’aux lignes satisfaisant ses conditions, jamais aveuglément au fichier entier.

### Écran de comparaison

Présenter des compteurs et filtres : **Nouveaux**, **Mises à jour proposées**, **Modifications CRM conservées**, **Conflits à résoudre**, **Inchangés**, **Absents du fichier**, **Erreurs**. Masquer les inchangés par défaut, sans les soustraire du bilan. Pour chaque champ modifié, montrer « Dernier fichier pris en compte », « Valeur actuelle du CRM », « Nouveau fichier » et l’action proposée. Une décision peut être appliquée à une sélection de champs sans conflit ; aucun bouton global ne force le remplacement des valeurs protégées.

L’opérateur traite uniquement les ambiguïtés, puis confirme le lot des créations et mises à jour sûres. Les conflits peuvent rester exclus du lot avec une raison visible. Après confirmation : résumé créé/mis à jour/conservé/non traité et lien vers le rapport. Conserver les choix « Garder la valeur CRM » pour ne pas représenter le même conflit à chaque dépôt identique ; un changement ultérieur de la source doit être signalé à nouveau.

### Comparaison à trois versions, champ par champ

Noter **B** la dernière valeur source reconnue pour ce champ, **C** la valeur CRM courante et **N** la nouvelle valeur source. Conserver aussi la provenance de la dernière écriture et un marqueur de modification locale depuis l’application de la source : les dates seules, ou l’égalité de valeurs après un aller-retour manuel, ne prouvent pas l’absence de modification.

| Situation | Proposition de l’assistant |
| --- | --- |
| N = B | Aucun delta source ; conserver C, même différent de B |
| N différent de B, C = B et aucun changement local/protection | Proposer N, à appliquer seulement lors de la confirmation du lot |
| N différent de B et modification locale depuis l’import | Conserver C par défaut ; conflit si N diffère de C ; choix explicite « Garder CRM » / « Prendre le fichier » selon droits |
| N = C | Aucun changement métier ; rapprocher la provenance sans effacer un marqueur de protection locale |
| Aucune référence B fiable | Initialisation/rapprochement explicite ; ne pas assimiler un champ existant à une valeur importée remplaçable |
| N vide ou colonne absente | Aucun effacement automatique ; distinguer cellule vide, champ absent et demande explicite d’effacement |

Une correction locale reste protégée lors des mois suivants, même si l’opérateur a reconnu la nouvelle valeur source sans la retenir. La référence source reconnue peut avancer vers N lors d’un choix explicite, mais la protection locale subsiste ; un conflit non traité n’avance pas sa référence B. Conserver séparément dernière source observée, dernière source reconnue, dernière valeur effectivement appliquée et décision opérateur. Un changement de mapping invalide les comparaisons des champs concernés jusqu’à revalidation.

Les notes, tâches réalisées, affectations, étapes commerciales, oppositions, décisions de gain et liens métier ne deviennent pas des champs remplaçables depuis Excel. Le fichier peut proposer un enrichissement ou une action métier distincte autorisée ; il ne remplace pas le suivi commercial. Les identifiants de rapprochement ne se réécrivent pas par la résolution d’un simple conflit de coordonnées.

Exemple : janvier contient le téléphone A ; l’équipe le corrige en B. Février contient encore A : conserver B sans action. Mars contient C : afficher B/C avec B conservé par défaut ; ne jamais restaurer A ni imposer C. En parallèle, une adresse non modifiée dans le CRM peut être mise à jour depuis mars après confirmation.

### Identification entre mois et absences

Le nom du fichier, sa date de dépôt et le numéro de ligne ne sont pas des identifiants de prospect. Réutiliser les liens de provenance validés, les clés source stables disponibles et les identifiants fiables. Un déplacement de ligne ne crée ni nouvelle organisation ni nouvelle opportunité. Sans clé stable ou correspondance certaine, proposer un rapprochement ciblé ; ne jamais fusionner au seul nom/commune/email générique. Une même ligne déjà rattachée garde son opportunité, sauf choix explicite de créer une nouvelle affaire.

Une ligne absente du nouveau fichier est signalée, **sans suppression, archivage, clôture ni annulation automatique**. Si elle revient, retrouver le lien antérieur. Le lot porte une période source mensuelle confirmée par l’opérateur et un ordre de traitement serveur ; un mois plus ancien est signalé et ne fait pas reculer silencieusement la référence. Son import éventuel est un rattrapage explicite, avec le même contrôle de deltas. Un rejeu exact reste sans effet supplémentaire.

À la confirmation et à chaque transaction de ligne, revérifier version CRM, protection locale et révision source : une modification effectuée après l’aperçu devient un conflit à recalculer. Deux imports mensuels ne mettent pas à jour la même référence de source concurremment. Une reprise conserve le plan confirmé et ne réapplique pas les lignes réussies.

## Sélection des onglets — E71-EVOL-02, décision du 9 octobre

Cette décision remplace les propositions d’import multi-onglets précédentes. **Seul « Pipeline qualifié » alimente les organisations, contacts, opportunités et tâches structurés.** « Coffrets & élus 2026 » est un enrichissement communal séparé. Tous les autres onglets sont exclus de l’import, y compris Budgets potentiels et Budgets territoriaux : ils ne produisent ni prospects ni enrichissements automatiques.

Lecture effective du classeur privé le 9 octobre, sans modification, recalcul ni consultation des URLs : Pipeline qualifié possède 34 en-têtes en A4:AH4 ; Coffrets & élus 2026 possède 33 en-têtes en A7:AG7 et 21 lignes complètes en A8:AG28, sans formule. Ces positions décrivent ce fichier ; le profil mensuel recherche les en-têtes et toutes les lignes de données, pas une plage figée. Les valeurs de personnes et coordonnées ne sont pas copiées dans la documentation Git.

### Fiche commune et section « Coffrets & élus 2026 »

Chaque ligne du second onglet est rattachée à la fiche **commune du CRM**, identifiée par code INSEE confirmé. D contient le nom, mais cet onglet ne fournit pas de code INSEE : nom et contexte Gironde servent à rechercher des candidats, pas à certifier une identité. Réutiliser une correspondance de source déjà validée ; sinon afficher commune/département/INSEE et faire confirmer les cas incertains. Homonyme, absence de résultat ou doublon de lignes : mise en attente, sans rattachement arbitraire.

Si la commune n’a pas encore de fiche CRM, créer sa fiche territoriale après résolution confirmée, **sans créer d’organisation prospectée ni de Ville commerciale**. Ne pas la publier sur la Marketplace. Une ligne sans rattachement confirmé reste dans le rapport « Communes à identifier ». Deux lignes visant le même INSEE et la même section ne s’écrasent pas : résolution explicite des doublons.

Créer ou compléter une section intitulée exactement **Coffrets & élus 2026**, avec les libellés de colonnes et leur contenu. Présentation en groupes lisibles, en conservant chaque champ séparément pour les deltas ; pas de collage opaque en note unique. Le nom de commune reste aussi visible comme valeur source, distinct du nom canonique de la fiche.

| Groupe de présentation | Colonnes reprises intégralement |
| --- | --- |
| Classement et territoire | A Rang ; B Score ; C Priorité ; D Commune ; E Population 2023 ; F Bassin / EPCI |
| Contexte commercial | G Centre-bourg / centralité ; H Profil de consommation ; I Mix commerçant / usage coffrets ; J Flux / événements |
| Équipe et contexte 2026 | K Équipe élue 2026 ; L Tête de liste / maire ; M Signal politique 2026 ; N Engagement / signal documenté |
| Interlocuteur indiqué | O Contact prioritaire ; P Fonction ; Q Coordonnée publique ; R Statut contact |
| Approche proposée | S Angle d’attaque Localéo ; T Question d’ouverture ; U Pilote recommandé ; V Risque / validation préalable |
| Sources et date déclarée | W Source population ; X Source résultat 2026 ; Y Source programme / politique ; Z Source contact / contexte ; AA Vérifié le |
| Détail du score source | AB Population /15 ; AC Pouvoir d’achat /15 ; AD Mix /20 ; AE Centre /20 ; AF Flux /15 ; AG Politique /15 |

Conserver les valeurs textuelles sources et leur provenance, avec typage d’affichage prudent pour nombres/dates ; une cellule vide affiche « Non renseigné ». Ne pas recalculer les scores, certifier les résultats électoraux, déduire une opinion personnelle ni utiliser ces données pour un profilage politique automatique. Les champs K:N et AG restent des contenus fournis par l’utilisateur, étiquetés comme tels. Cette reprise explicite de toutes les colonnes remplace leur exclusion générale proposée auparavant, sans ajouter d’enrichissement externe.

O:R ne créent aucun contact structuré, aucune tâche de sollicitation ni consentement. Q peut contenir téléphone, email, URL ou texte mixte : conserver le contenu sans conversion forcée. « Vérifié 2026 » / « Vérifié le » restent déclarés par le fichier, distincts de la date d’import. Les sources sont affichées échappées ; liens HTTP(S) seulement, pas d’exécution ni de visite automatique.

### Import mensuel des sections communales

Le même dépôt produit deux bilans séparés : **Prospects du Pipeline** et **Sections communales Coffrets & élus 2026**. Afficher leurs créations, modifications, conflits, inchangés et lignes non rattachées, avec confirmation unique du plan mais résultats distincts. Une commune présente dans les deux onglets partage la fiche territoriale ; elle ne fusionne pas toutes les organisations installées sur son territoire.

Appliquer la comparaison à trois versions à chacun des 33 champs de la section : dernière valeur source reconnue / valeur locale / nouvelle valeur source. Une correction locale de la section est protégée ; une commune absente le mois suivant ne perd pas sa section. Un changement du champ D ou de rattachement INSEE exige résolution d’identité, pas une mise à jour de texte qui déplacerait toute la section. La période mensuelle de source est distincte de l’année 2026 du titre : ne pas renommer cette section en fonction de la date d’import. Un futur onglet d’une autre année demande un profil/version explicite.

Une ligne communale est atomique avec sa provenance et ses décisions de champ ; les lignes Pipeline et communales restent reprenables indépendamment. Les totaux de prospects et les indicateurs de gain excluent les fiches communales seules. La carte peut afficher leur contexte depuis une commune sélectionnée, sans les compter comme organisations prospects.

### Modèle de mapping Gironde V2

La lecture décrite dans le backlog date du 2 octobre ; ce document ne certifie ni les coordonnées ni les valeurs du fichier. L'identité du fichier est son empreinte dans le backlog. Le modèle ci-dessous doit être testé sur une **fixture synthétique**, puis approuvé sur aperçu par l'opérateur avant import réel.

| Onglet | Traitement cible |
| --- | --- |
| Pipeline qualifié (`A4:AH42`) | En-têtes ligne 4, lignes 5–42 candidates ; organisation/territoire, contact/fonction, coordonnées, provenance et opportunité séparés ; axe Animation proposé puis confirmé ; aucune tâche sans type/échéance/référent exploitables |
| Coffrets & élus 2026 (`A7:AG28`) | Section de fiche commune exclusivement, selon E71-EVOL-02 ; aucune création de prospect/contact/opportunité |
| Budgets potentiels (`A5:AJ58`) | Exclu de l’import par décision E71-EVOL-02 |
| Budgets territoriaux | Exclu de l’import par décision E71-EVOL-02 |
| Tableau de bord, Playbook commercial, Sources & méthode, Hypothèses budget, Synthèse budgets | Exclus des lignes de prospects ; la provenance documentaire utile peut être attachée au lot, sans recalcul de budget/scoring |

**Exception X/Y** : les 37 lignes où Y est une URL et X vaut « À contacter » sont marquées `MAPPING_STATUT_AMBIGU`. L'aperçu propose X → statut, Y → provenance seulement pour les lignes identifiées et après choix explicite ; la ligne où Y contient déjà le statut garde son mapping propre. Aucun décalage général de colonnes. Une URL n'est jamais acceptée comme étape ou prochaine action.

Les 33 rapprochements de libellés avec Budgets potentiels et le recoupement entre les deux listes ne prouvent pas l'identité de structures. Ils servent à proposer une commune ou une comparaison. Les dates « vérifié le » et scores sont étiquetés « déclarés dans la source », distincts d'une vérification opérateur CRM.

Colonnes retenues par défaut proposées : identité structure, identifiants officiels valides, coordonnées professionnelles, fonction, besoin/axe, origine/source, action et statut interprétables. Budgets/signaux/scoring : option d'enrichissement sourcée, avec unité, date et confiance déclarée ; aucune dérivation de prix, de prévision comptable ou de décision automatique. Écarter le profilage personnel d'opinion politique et les données sans utilité commerciale définie.

### Normalisation et rapprochement

Trim et normalisation de comparaison séparés de la valeur affichée ; ne pas retirer accents/ponctuation d'un nom stocké pour forcer une identité. Email/téléphone invalides produisent une anomalie, pas une réparation inventée. Conserver code INSEE/SIRET comme chaînes ; valider leur forme avant de proposer un rapprochement. Un email public n'est ni consentement ni preuve d'identité de structure.

Identité durable de provenance : `(source_namespace, source_record_key, type_entite, sous_cle)` liée aux UUID CRM. Le rang Excel n'est pas une clé métier. Si la source ne contient pas de clé stable, le premier import reçoit des clés internes et mémorise les positions/empreintes ; tout fichier modifié/retrié exige rapprochement explicite des lignes anciennes, nouvelles et supprimées. Le système ne prétend pas reconnaître une identité sans information suffisante.

Exactement le même fichier, mapping et sélection confirmés réutilisent le lot/résultat connu. Une autre clé HTTP ne contourne pas cette identité. Pour une version modifiée, l'aperçu propose des correspondances ; les cas ambigus restent bloqués ou exclus. Deux lots concurrents d'une même famille de source sérialisent leurs validations et vérifient les clés uniques avant toute création. L'opérateur peut déclarer une nouvelle affaire pour une structure connue, mais jamais par simple changement de ligne Excel.

Priorité aux données CRM enrichies : un champ renseigné/importé peut être mis à jour seulement selon un choix de champ explicite et une version courante. Notes, responsable, étape, oppositions et contacts obsolètes ne sont pas écrasés automatiquement. Rechercher les oppositions sur les identités fiables et contacts normalisés avant confirmation ; une correspondance possible impose résolution, elle ne justifie ni fusion ni création contournant un blocage.

### États, transactions et reprise

États du lot proposés : `DEPOSE`, `A_CORRIGER`, `PRET`, `EN_COURS`, `TERMINE`, `TERMINE_AVEC_REJETS`, `INTERROMPU`, `ANNULE`, `EXPIRE`. États de ligne : `A_TRAITER`, `APPLIQUEE`, `IGNOREE`, `REJETEE`, `CONFLIT`.

- Avant confirmation uniquement, modifier mapping/sélection/version de source remet le lot en aperçu à recalculer. Dès `EN_COURS`, le plan confirmé est immuable : reprise avec le même plan et ses clés de ligne ; toute correction de mapping ou de source crée un nouveau lot lié, avec rapprochement sur les résultats déjà appliqués.
- `PRET → EN_COURS` exige version du plan, empreinte, consentement de l'opérateur et absence d'erreur bloquante sur les lignes retenues.
- Chaque ligne est atomique : toutes ses mutations CRM, correspondances de provenance et événements sont validés ensemble, ou aucun ne l'est. Contraintes uniques sur origine et événement de ligne ; version courante contrôlée dans la transaction.
- Un worker prend un bail avec jeton de clôture ; un worker dont le bail a expiré ne peut valider après reprise par un autre. La ligne marquée appliquée n'est jamais réappliquée.
- Un conflit tardif est rapporté, pas écrasé. Les lignes indépendantes peuvent réussir ; le bilan distingue succès partiel et import terminé intégralement.
- Avant confirmation, annuler passe le lot à `ANNULE` sans objet CRM. Après début, « arrêter » passe le lot à `INTERROMPU`, suspend les lignes non appliquées et conserve les mutations réussies. **Pas de rollback global** effaçant les enrichissements ultérieurs.
- La correction admin compare versions et références avant de délier/corriger. Une suppression métier éventuelle suit sa propre politique ; elle ne résulte pas d'un bouton « annuler le fichier ».

Rejouer une confirmation après timeout renvoie le même lot ; une reprise ne multiplie ni contacts, ni tâches, ni notes. Les tâches importées satisfont la même politique d'opposition que les tâches manuelles.

### Traitement technique du fichier

Proposition : XLSX sans macro, 10 Mio de fichier, 100 Mio décompressés au total, 10 000 lignes métier, 100 colonnes par feuille sélectionnée et 1 000 000 cellules examinées au total ; délai de traitement borné et traitement par flux. Rejeter fichiers chiffrés, XLSM, ZIP incohérents, liens externes actifs et dépassements. Une formule n'est **jamais exécutée**, ni son URL visitée ; seule une valeur en cache explicitement retenue peut devenir estimation de provenance, jamais un champ d'identité/preuve de gain. Cache absent = valeur inconnue/anomalie.

Utiliser un adaptateur de parsing isolé avec limites ZIP/XML, y compris fichiers non sélectionnés et shared strings ; la borne `read_upload_limited` seule ne suffit pas. Aucun calcul Excel, macro, appel réseau ni résolution de lien externe. Rapport et fichier dans stockage privé, accès authentifié et `Cache-Control: no-store`. Les limites sont des propositions techniques à confronter au volume pilote ARB-01, pas une bibliothèque choisie sans évaluation.

## Carte et localisation — CA-07/13/14/15

Le cache `CommuneProspection` contient code INSEE, nom, département/région, centroïde, source et date de référence. Il ne crée pas de `Ville` commerciale. La recherche utilise le port géographique ; l'adaptateur actuel peut résoudre nom/code postal/INSEE, mais les autorisations CRM ne dépendent pas de la publication Marketplace.

Un code postal partagé ou un homonyme produit plusieurs candidats ; l'utilisateur choisit ou laisse non localisé. Une commune hors catalogue est autorisée. Une commune supprimée/fusionnée ne change pas arbitrairement une fiche : signalement puis choix explicite du rattachement actuel, provenance historique conservée. Une mise à jour de centroïde n'est pas un déplacement d'établissement.

Le point est intitulé **« Centre de la commune — localisation indicative »**. Un clic ouvre la liste paginée des organisations et opportunités de la commune ; plusieurs opportunités n'ajoutent pas de faux prospects. Compteurs `organisations`, `opportunites`, `localisees`, `non_localisees` distincts ; filtres identiques à ceux de la liste. Le cadrage visible de la carte n'efface pas les non-localisés du total du portefeuille.

Proposition de contrat carte : bbox/zoom bornés, réponse avec groupes communaux/clusters, compteurs, `truncated` et `generated_at`. Au-delà de 500 éléments rendus, agréger côté serveur ; si une réponse reste tronquée, l'annoncer et demander zoom/filtre. Ne pas charger tous les contacts pour dessiner la carte. La liste demeure la voie exhaustive paginée. Une vue d'étapes chargée partiellement indique les totaux et propose « Charger la suite ».

Couverture exacte et fournisseur restent à confirmer par ARB-06. Si Outre-mer retenu, sélecteur de zones avec recentrage plutôt qu'une étendue France illisible ; toute commune non couverte reste accessible et signalée dans la liste. Un fournisseur indisponible n'empêche ni l'enregistrement ni la consultation des fiches. Afficher erreur carte et réessai sans perdre les filtres.

Le fournisseur de fond de carte reçoit seulement les requêtes nécessaires au fond (emprise/tuiles), **pas les données de prospects**. Les points CRM sont rendus localement dans le navigateur à partir de l'API interne. La résolution de communes transmet des critères géographiques, pas nom de contact, email, téléphone, note ou fichier. Documenter fournisseur, licence/attribution, couverture, quotas, journalisation et configuration avant activation ; aucune clé navigateur privilégiée ou géolocalisation personnelle demandée.

## Cibles de performance à valider

Jeu proposé pour mesures : 10 000 organisations, 30 000 opportunités, 60 000 tâches et 10 utilisateurs internes simultanés ; aucun chiffre mesuré à ce stade. Cibles initiales : p95 liste ≤ 1 s côté API hors réseau, carte agrégée ≤ 2 s, interface utilisable sur mobile 390 px et clavier sans carte. Fixer le budget d'import après benchmark ; afficher progression durable et permettre reprise plutôt qu'un timeout synchrone long. Si le volume attendu diffère, actualiser les index/limites et la recette avant livraison.
