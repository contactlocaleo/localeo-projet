# E71-EVOL-05 — Vérifier et actualiser la qualification d’un prospect

Spécification cible **V1 du 6 novembre 2026**, issue du cadrage du 5 novembre, à la demande
« rafraîchir à la demande les informations de qualification ». Cette évolution
de l’[epic 71](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md)
complète la [qualification structurée](qualification-structuree.md).
**Implémentation locale du 6 novembre** : domaine, stockage v295/v298, commandes
atomiques, API, worker supervisé, baux partagés v297 et comparaison PWA.
Le [bilan](verification-livraison.md) distingue preuves et réserves ; la
[préparation des référentiels](referentiels-qualification.md) décrit les entrées
réelles attendues. Aucun déploiement ni collecte sur TEST réalisé.
**Décision utilisateur : les six blocs dès la première livraison.**
Le comptage retenu couvre les établissements actifs de proximité des six familles,
dédupliqués par SIRET ; cas incertains et terrain distincts. L’aperçu et
l’adoption explicite protègent les valeurs existantes ; aucune application automatique.
Les sections de conception ci-dessous restent l’oracle de vérification, pas une
preuve automatique d’exécution des tests de capacité.

## 1. Existant et résultat recherché

Le bouton d’actualisation actuel relit le CRM ; il ne consulte pas les sources
externes. Les qualifications sont renseignées manuellement ou par CSV. Le
connecteur géographique ne fournit que nom/INSEE/centre ; son rattrapage des
communes manquantes ne rafraîchit ni la population ni les contacts ou évaluations.
Aucun connecteur produit Sirene, BANATIC ou annuaire administratif n’est présent
dans l’implémentation examinée le 6 novembre, backend `d928b9a`. Les sources
vérifiées sont `app/domaine/prospection/qualification.py` et `regles.py`,
`app/application/prospection/qualification.py`, les schémas
`app/api/prospection_qualification_schemas.py` / `prospection_api.py` et la
persistance `app/infrastructure/persistence/crm_qualification.py`.

La cible est une vérification **d’un prospect à la demande**, sur ses six blocs,
sans refaire un import. Le gestionnaire voit les changements trouvés, leur
provenance et leurs limites avant de décider ce qui doit être retenu.
Une source consultée aujourd’hui peut décrire une situation plus ancienne :
« vérifié auprès de la source » ne signifie pas « vérifié sur le terrain ».

## 2. Parcours recommandé

1. Dans la fiche, choisir **Vérifier les données**, distinct de **Actualiser la
   page**. Tous les blocs disponibles sont présélectionnés ; possibilité de ne
   vérifier que les contacts, par exemple. Les identifiants manquants sont indiqués.
2. Le travail s’exécute en arrière-plan. La fiche reste utilisable. Un second clic
   retrouve le traitement en cours au lieu de lancer des recherches identiques.
3. Un bilan affiche **Inchangé**, **Nouveauté**, **Différence à examiner**,
   **Non disponible** ou **Vérification manuelle nécessaire**, par bloc.
4. Comparer **Valeur actuelle / Valeur trouvée / Source et date**. Les modifications
   protégées et identités contradictoires sont signalées. Rien n’est appliqué
   automatiquement, y compris dans un champ vide ou volontairement vidé.
5. Appliquer les propositions choisies par blocs cohérents, ou **Conserver ma
   valeur**. Une évaluation reste une nouvelle observation ; son éventuelle
   confirmation et sa sélection comme référence sont des choix explicites.
6. La fiche présente la date de consultation et les différences restant à
   examiner. L’historique d’actualisation explique les choix sans remplir
   l’**Historique des échanges** de réponses techniques ou de longs textes.

La présentation reste la même sur PC/mobile : une action principale, un résumé
court, puis les différences dépliables et paginées. Pas de six formulaires à
remplir successivement lorsque certaines données n’ont pas changé.

### Couverture de la première livraison — décision du 6 novembre

Les six blocs doivent avoir un parcours fonctionnel et un adaptateur ou
référentiel qualifié pour leur périmètre applicable. Cela inclut comptages,
familles d’activité et compétences, sans les repousser à une livraison suivante.
Les développements internes peuvent être séquencés, mais la livraison annoncée
couvre l’ensemble. Un simple bouton ou un bloc toujours NON_PRIS_EN_CHARGE ne
constitue pas une couverture fonctionnelle.

La recette doit démontrer un résultat exploitable par bloc sur fixtures
représentatives, ainsi qu’une vérification simultanée des six blocs, puis une
panne fournisseur partielle sans perte de données. Une donnée non publiée ou
un bloc légitimement non applicable reste signalé comme tel : couvrir tous les
blocs ne garantit pas que toutes les informations existent pour chaque prospect.
La méthode de comptage et la qualification technique des sources deviennent des
prérequis de cette livraison complète, sans imposer de pilote externe à la clôture.

## 3. Ce qui peut être vérifié selon le bloc

| Bloc | Vérification proposée | Ce qui exige une décision ou une preuve humaine |
| --- | --- | --- |
| Identité | Dénomination officielle, forme/nature et état administratif lorsqu’ils sont publiés ; correspondance INSEE/SIREN/SIRET | Nom d’affichage du prospect, rattachement ambigu, nouvel identifiant ou fusion ; ne jamais remplacer une commune ou un établissement par un homonyme |
| Territoire | Nom/code communal, centre, département/région, appartenance EPCI et liste de membres ; population avec millésime explicite | Changement d’identité communale, date d’effet non fournie, siège hors Nouvelle-Aquitaine ; appartenance administrative et couverture commerciale d’un projet restent distinctes |
| Évaluation du potentiel | Nouvelle photographie des commerces identifiés dans les sources, familles, cas à vérifier, population et compétences documentées | Contrôle terrain, méthode de comptage non comparable, choix de la référence ; aucun potentiel « à jour » affiché sur un calcul incomplet |
| Activité | NAF/APE avec version de nomenclature et bon niveau d’identité ; proposition de famille Animation à partir d’une règle versionnée | Pour un SIRET, prendre le NAF de cet établissement exact, jamais celui du siège ou de l’unité légale ; accueil réel du public et famille corrigée demandent examen |
| Informations de la structure | Adresse administrative, téléphone/e-mail générique et site lorsqu’ils sont disponibles dans une source adaptée | Origine éditoriale du prospect, nom commercial retenu, coordonnées volontairement corrigées ; ne pas déplacer le siège vers la zone d’intervention |
| Contacts | Coordonnées publiques d’un service/accueil de collectivité et éventuelles fonctions publiées ; propositions de nouveaux contacts | Décideur ou porteur réel, preuve de vérification, contact personnel, consentement ; ne jamais deviner une adresse ou envoyer un e-mail de test |

Un même champ n’a qu’un propriétaire : les coordonnées de la structure ne sont
pas celles d’un contact, les membres d’un EPCI ne sont pas sa commune de siège.
La population affichée dans **Territoire** est une lecture de la référence du
bloc **POPULATION** ; aucun second champ de population modifiable sur la structure.
Le potentiel territorial concerne une commune, les membres NA d’un EPCI ou un
projet dont la couverture est connue. Un commerce/une association sans projet
couvert n’hérite pas du total de sa commune : le bloc est indiqué non applicable
ou demande de préciser le périmètre, sans créer un projet automatiquement.
Le mapping fermé de la section 10.1 distingue les champs adoptables des constats
administratifs consultables ; aucun attribut n’est caché dans une note.

## 4. Référentiels proposés et limites vérifiées

Sources officielles consultées le 5 novembre 2026 ; leurs capacités ne prouvent
pas encore le fonctionnement d’un adaptateur Localeo.

| Source | Usage proposé et limite |
| --- | --- |
| [API Recherche d’entreprises](https://recherche-entreprises.api.gouv.fr/docs/) | Recherche d’identité publique par SIREN/SIRET. Une recherche exacte ignore les autres filtres : le serveur Localeo doit donc vérifier lui-même identité, établissement et territoire renvoyés. Le filtre d’activité porte sur l’unité légale ; ses totaux ne constituent pas directement le nombre d’établissements compatibles Animation. Couverture publique limitée ; gérer 429 et `Retry-After`. |
| [Sirene — Insee](https://www.insee.fr/fr/information/3591226) | Identités d’entreprises/établissements et fichiers/API pour préparer un référentiel de comptage. Le calcul Localeo doit distinguer SIREN et SIRET, établissements actifs/fermés, nomenclature et couverture de diffusion ; l’accès à un registre ne définit pas la sélection commerciale. |
| [API Découpage administratif](https://geo.api.gouv.fr/decoupage-administratif/communes), [EPCI](https://geo.api.gouv.fr/decoupage-administratif/epcis) | Communes, centres et relations territoriales. Une photographie courante ne fournit pas nécessairement la date juridique d’un changement. Elle ne suffit pas à inventer un millésime statistique de population. |
| [Populations de référence — Insee](https://www.insee.fr/fr/statistiques/8681011) | Source millésimée pour la population. Distinguer année statistique, date de publication, géographie et date d’entrée en vigueur ; aucune substitution par l’année du clic. |
| [BANATIC](https://www.banatic.interieur.gouv.fr/), [présentation DGCL](https://www.collectivites-locales.gouv.fr/gerer-les-finances-publiques-locales/dematerialisation-des-comptes-locaux-et-open-data/ouverture-des-donnees-financieres-des-collectivites-locales) | Exports des intercommunalités et compétences, avec date du fichier. L’interface d’export est identifiée ; contrat de téléchargement et mapping des compétences à qualifier avant automatisation, sans supposer une API temps réel documentée. |
| [Annuaire administratif DILA](https://www.data.gouv.fr/dataservices/api-annuaire-de-ladministration-et-des-services-publics), [modèle des données](https://api-lannuaire.service-public.gouv.fr/explore/dataset/api-lannuaire-administration/) | Services publics, coordonnées institutionnelles et métadonnées publiées. Les champs disponibles varient selon la fiche ; ils ne garantissent pas les coordonnées d’un élu ou du bon interlocuteur commercial. Pas de couverture équivalente garantie pour les contacts de tous les commerces/associations. |

Pour les comptages, recommandation : préparer côté serveur un référentiel régional
Sirene/territoires **versionné et indexé**, puis calculer la commune, les membres
NA de l’EPCI ou la couverture du projet demandée. Ne pas télécharger le stock
national à chaque clic, ni multiplier les appels d’identité par commerce.
Sa date reste affichée ; si le référentiel disponible est ancien, le clic ne le
transforme pas en photographie récente. Son alimentation technique est distincte
d’une actualisation automatique de toutes les fiches prospects.

## 5. Invariants à préserver et nouvelle adoption des données

- Les droits CRM actuels restent la base : consulter voit le bilan ; gérer
  demande et applique. Les droits sont relus à l’application et au traitement.
- Les identités stables et liens CSV ne changent pas. Aucun rapprochement,
  fusion, commerce ERP, compte, dossier, abonnement ou gain créé implicitement.
- Les corrections manuelles, y compris remise à vide, restent protégées.
  Une divergence peut être présentée ; son remplacement demande un choix
  explicite, la valeur/version observée et une trace de décision. Une proposition
  fournisseur ne devient pas une correction manuelle simplement en réutilisant
  le `PATCH` actuel : distinguer les provenances dans la future commande domaine.
- Une absence de résultat, une source indisponible ou un champ non publié ne
  signifie ni zéro, ni fermeture, ni contact obsolète. Aucune suppression implicite.
- Évaluations confirmées immuables : créer une nouvelle observation. Références
  COMPTAGES/POPULATION/COMPETENCES séparées, terrain prouvé prioritaire **dans
  l’observation/référence retenue**, sans priorité automatique d’un ancien relevé,
  cas incertains exclus du comptage retenu. Aucun changement de référence sans
  choix du gestionnaire ni mélange de versions entre blocs.
- Une nouvelle population ou compétence n’oblige pas à recalculer un comptage
  absent. Un bloc incomplet reste brouillon et n’influence pas le classement.
- Les changements de périmètre ou de méthode rendent les observations non
  comparables et demandent examen. Un EPCI ne cumule pas ses totaux avec ceux de
  ses communes ; couverture de projet vérifiée par empreinte au moment du calcul.
- Les contacts restent des objets CRM distincts : pas de rapprochement par seul
  e-mail/téléphone, ni de remplacement d’une personne par l’accueil générique.
  Une coordonnée acceptée différente invalide l’ancienne vérification et peut
  rendre un porteur de dossier à revalider, selon les règles existantes.

## 6. Fraîcheur, historique et contrats cibles

L’[évolution E71-EVOL-06](niveau-qualification.md) utilise les faits adoptés pour
calculer un niveau de priorité commerciale (potentiel, maturité et fiabilité).
Une simple tentative d’actualisation, ou une proposition non adoptée, ne lui
fournit pas de nouvelle preuve ; après adoption d’un fait pertinent, les axes
dépendants sont signalés à recalculer. Une modification de contact seule ne
retire pas la priorité fondée sur un potentiel toujours courant.

Par bloc/champ proposé, conserver : identifiant du fournisseur et de son objet,
valeur courante et version de départ, valeur trouvée, date de consultation,
date/millésime de la source lorsqu’il est connu, couverture, méthode/version,
résultat de comparaison et décision d’adoption ou de refus. La source d’import
et l’**Origine du prospect** restent inchangées ; elles ne servent pas à stocker
cette nouvelle provenance. Les faits de vérification humaine restent séparés.

États de traitement : `EN_ATTENTE`, `EN_COURS`, `TERMINE`,
`TERMINE_PARTIELLEMENT`, `ECHEC`. Un traitement terminé peut conclure « aucune
différence ». Les résultats indisponibles sont visibles par fournisseur ; les
propositions obtenues restent consultables sans promettre une vérification complète.

Contrats désormais implémentés et exportés depuis le code, détaillés en section 10 : demande d’actualisation (202, blocs et version attendue),
lecture de progression/propositions paginées, application/rejet des propositions
sélectionnées avec idempotence et versions attendues. Un aperçu périmé est refusé
sans écraser une modification concurrente ; le gestionnaire peut relancer.
Le JSON OpenAPI actuel reste celui des API réellement implémentées.

Le domaine Prospection porte l’adoption, les conflits et les invariants ;
l’application orchestre les ports de référentiel et transactions ; les adaptateurs
normalisent les sources ; la PWA présente l’aperçu. Réseau hors transaction SQL,
reprise durable et absence de nouvel appel externe lors du rejeu d’une application.

## 7. Bornes et livraison à vérifier avant activation

Un prospect par demande, six blocs au maximum. Pas de lancement global du
portefeuille ni de rafraîchissement à chaque ouverture de fiche en première version.
Dédupliquer les demandes actives pour un même prospect/périmètre ; propositions
et historique paginés 25/100. Les appels ponctuels et calculs territoriaux ont des
files et budgets séparés : acquisition/API interactives courtes, préparation des
référentiels volumineux par traitements bornés. Les quotas seront centralisés
entre workers, avec timeouts, reprises limitées, attente fournisseur respectée et
échecs partiels explicites. Aucune transaction ni verrou métier pendant le réseau.

Les limites proposées de requêtes/octets/pages, débit partagé, index, volumes,
réponse 202 et durée des jobs sont détaillées en section 10.5. Elles devront être
confrontées à chaque contrat fournisseur puis vérifiées par les tests de capacité :
ce ne sont pas des performances acquises. La conservation relève de la section
10.6 et de l’arbitrage ARB-07 existant ; cette proposition ne le tranche pas.

Prévoir migration additive des demandes/propositions/provenances et conservation
des anciennes fiches ; aucune réécriture des observations existantes. Réutiliser
ordonnancement et supervision communs, avec identité de batch propre à ce travail
si nécessaire. Le batch des imports ne doit pas devenir un collecteur multi-source.
Le CSV 1/2 reste compatible et n’exige pas une nouvelle colonne.

## 8. Choix confirmés, propositions et points encore ouverts

| Sujet | Décision ou proposition explicitement identifiée |
| --- | --- |
| Adoption des données | Aperçu et sélection explicite, y compris pour les champs vides ; aucun remplacement automatique en première version |
| Potentiel commercial | Réutiliser la méthode du fichier après formalisation de la sélection et de la répartition en familles, versionner les règles et compter des établissements uniques ; méthode non approuvée = pas de nouveau total annoncé |
| Territoire courant sans date juridique | Présenter un constat daté et demander la date d’effet pour remplacer la relation historique ; ne jamais utiliser automatiquement le jour du clic comme date d’adhésion |
| Sources de contacts | Démarrer par les coordonnées institutionnelles des collectivités ; compléter les contacts de commerces manuellement faute de source fiable identifiée ; pas de service payant ou collecte sur des sites arbitraires ajoutés implicitement |
| Périmètre de première livraison — confirmé le 6 novembre | Les six blocs ensemble, y compris activité, comptages et compétences ; qualifier leurs méthodes/référentiels avant cette livraison. Un adaptateur manquant est un reste à développer, pas un report accepté |

## 9. Critères et preuves prévues

Les nouveaux critères **E71-CA-41 à 49** sont définis dans le backlog. Aucun test
de cette nouvelle fonctionnalité n’est annoncé exécuté à ce stade.

| Critères | Preuves à produire | Impacts |
| --- | --- | --- |
| 41/46 | Navigateur PC/mobile : demande ciblée, différences courtes, dates distinctes, aucun résultat complet annoncé en cas de bloc absent | PWA CRM, parcours et guide à compléter à la livraison |
| 42/43 | Domaine : identités exactes, bon NAF d’établissement, ambiguïtés/refus, protection du vide et adoption explicite ; intégration avec anciens liens CSV | Organisation/contact, commande d’adoption et migrations additives |
| 44 | Domaine/SQL : observations immuables, population sans double stockage, terrain de la référence retenue, méthode/territoire versionnés, bloc non applicable sans couverture et comptage incomplet refusé | Référentiels préparés, évaluations et références ; quotas/mesures à documenter |
| 45 | Domaine/HTTP : nouveaux services proposés sans doublon, absence non destructrice, contact et porteur à revalider après adoption | Contrats de contact, audit et fixtures |
| 47/48 | Doubles fournisseurs : indisponibilité, 429/reprise, résultat partiel, doublon de clic, droit retiré, conflit concurrent et rejeu | Jobs/ports, API privées, ordonnancement et supervision |
| 49 | Migration/restauration, démonstration à fournisseurs fictifs, contrats et capacité N/10N, absence d’appels réels en tests | Générateur et guide ops à adapter ; cinq dépôts indépendants conservés |

Les trois autres frontends et les comptes ERP ne changent pas de contrat dans
ce cadrage : la fonctionnalité reste interne au backend/PWA CRM et réutilise
les droits existants. Leur absence d’impact devra être reconfirmée au contrat
final. Aucun développement, migration, appel de qualification réelle sur TEST,
commit, push ou déploiement n’est réalisé par cette demande de conception.

Contrôles historiques du cadrage du 5 novembre : guides et 146 sources exportées validés,
bundle local généré puis vérifié par empreintes (147 documents distribués, dont
le manifeste). Tests des lecteurs et outils documentaires : **38 réussis**,
**2 non exécutés**, création de liens symboliques non autorisée sur cette plateforme.
La revue indépendante a fait préciser la propriété de la population, le niveau
du NAF, le périmètre applicable et la priorité terrain. Ces contrôles ne prouvent
aucun des nouveaux comportements de rafraîchissement, qui restent à développer.


## 10. Contrat cible détaillé — révision du 6 novembre 2026

Cette section détaille les résumés techniques des sections 6/7.
Les hypothèses métier de la section 8 restent proposées, non implicitement validées.

### 10.1. Mapping vers le modèle réel et groupes indivisibles

Le contrat fournisseur n’est pas un `PATCH` libre. Les chemins ci-dessous forment
une liste fermée. Les bornes/enums de [qualification structurée](qualification-structuree.md)
et les validateurs du domaine existant restent applicables. Un champ fournisseur
sans destination n’est pas écrit arbitrairement dans la qualification JSON.

| Groupe / cible existante | Champs adoptables | Conditions et limites |
| --- | --- | --- |
| `NOM_STRUCTURE` / organisation | `nom` (300 caractères) | Proposition du nom officiel comme affichage, choix explicite ; aucun remplacement obligatoire du nom commercial |
| `IDENTITE_LEGALE` / organisation.qualification | `niveau_identite`, `siren`, `siret`, `sous_type_collectivite`, `nature_epci` | Groupe indivisible cohérent ; compléter une identité absente n’autorise pas à modifier une identité stable contradictoire. `type` ne change pas automatiquement |
| `LOCALISATION` / organisation | `insee`, `commune`, `code_postal`, `adresse` | Groupe contrôlé par référentiel serveur ; commune identifiée immuable ; établissement relocalisé seulement après contrôle NA et ressemblances. Aucun centre fournisseur écrit directement sur le prospect |
| `ACTIVITE_NAF` / organisation.qualification | `code_naf`, `version_naf` | Paire indivisible ; SIRET exact si établissement, jamais repli sur le siège |
| `FAMILLE_ANIMATION` / organisation.qualification | `famille_animation` | Non disponible tant que mapping NAF/version vers familles non arbitré ; jamais déduit d’un intitulé libre |
| `COORDONNEES_STRUCTURE` / organisation | `telephone` (40), `email` (254), `site_web` (2048) | Une proposition par champ, validations existantes ; seulement coordonnées publiques fournies. Liens HTTP(S) sans identifiants ; aucune exploration du site pour enrichir |
| `APPARTENANCE` / relation commune–EPCI | `epci_siren`, `debut`, `source_reference`, `source_date` | Groupe indivisible ; date juridique requise. Constat actuel sans date → vérification manuelle, pas écriture d’appartenance. Membres EPCI lus des relations, non dupliqués |
| `CONTACT_PUBLIC` / contact | `nom`, `fonction`, `telephone`, `email`, `qualification.nature_contact` | Créer un service/accueil ou cibler explicitement un contact du prospect ; pas de rapprochement sur seul téléphone/e-mail |
| `EVALUATION_POPULATION` / nouvelle évaluation | `population`, `population_annee`, `population_source_ref`, `population_source_date` + contexte | Groupe indivisible millésimé, aucune population duplicative sur organisation |
| `EVALUATION_COMPTAGES` / nouvelle évaluation | `nb_commerces_documentaires`, `nb_cas_a_verifier`, `nb_actifs_tous_secteurs`, les six champs de familles + contexte | Méthode et couverture figées ; total/familles cohérents, incertains exclus ; pas d’écriture de `nb_commerces_terrain` ou de ses preuves |
| `EVALUATION_COMPETENCES` / nouvelle évaluation | `competence_commerce`, `competence_tourisme`, `competence_marches`, `competences_source_ref`, `competences_source_date` + contexte | Conserver INCONNUE ; absence dans un export ≠ NON |

Le contexte d’évaluation est `date_observation`, `source_libelle`,
`source_reference`, `source_date`, `perimetre_territorial`, `projet_id` éventuel et
`couverture_empreinte` uniquement pour `COUVERTURE_PROJET`, conformément au
validateur existant ; ce champ reste vide pour COMMUNE et
MEMBRES_NOUVELLE_AQUITAINE. L’empreinte de composition territoriale commune/EPCI
est portée par la provenance additive, pas par ce champ réservé aux projets.
Les versions de méthode/référentiels/géographie sont
portées par la provenance additive. Adoption → nouvelle évaluation **BROUILLON** ;
la confirmation et le choix de référence utilisent ensuite les commandes existantes,
comme deux actions explicites distinctes. Des blocs ne partagent une observation
que si portée, couverture et date d’observation concordent ; sinon observations
séparées dans la même transaction d’adoption.

Les six familles de comptage sont `nb_alimentaire`, `nb_boutiques`,
`nb_restauration`, `nb_beaute_coiffure`, `nb_services_proximite`,
`nb_grandes_surfaces`. Leur somme et la présence du total suivent le domaine actuel.

`source`, `responsable_id`, états commerciaux/archivage, oppositions,
`role_commercial`, `fiabilite_contact=VERIFIE`, preuves/dates d’accueil public,
qualification de projet/budget/porteur et liens ERP sont exclus des adoptions.
La catégorie juridique et l’état administratif éventuels restent des **constats
sourcés consultables**, sans conversion en `ACTIF/ARCHIVE`. Leur usage comme
attribut métier nécessiterait un contrat dédié, pas une clé JSON libre.

Une coordonnée contact changée invalide sa vérification selon le domaine actuel
et rend les portages confirmés dépendants `A_REVALIDER`. Un nouveau contact n’est
jamais désigné décideur/porteur. Les contradictions d’identité se traitent par
rapprochement explicite ; pas de fusion ajoutée à cette évolution.

### 10.2. Propriétaires, états et instantanés

Objets cibles du domaine Prospection : `DemandeActualisationProspect` et
`PropositionActualisationProspect`, portant applicabilité, adoption cohérente,
protections et conflits. L’application capture les versions, orchestre les ports
et transactions ; les adaptateurs normalisent sans écrire le prospect. L’API et
le batch ne contournent jamais ces décisions par SQL direct.

| État du job | Transition et résultat |
| --- | --- |
| `EN_ATTENTE` | Demande persistée et autorisée ; bail worker → EN_COURS |
| `EN_COURS` | Acquisition bornée, reprise par source ; bail expiré → reprise du même job, sans dupliquer résultats |
| `TERMINE` | Chaque bloc applicable demandé a un résultat exploitable, même inchangé ; non applicable explicitement justifié |
| `TERMINE_PARTIELLEMENT` | Au moins un résultat exploitable et un bloc indisponible/ambigu/non équipé ; jamais « fiche à jour » |
| `ECHEC` | Aucun résultat exploitable, droits révoqués ou deadline dépassée sans résultat ; données CRM intactes |

Les terminaux ne repartent pas en cours : une relance crée un job `relance_de`
avec nouvelles versions/dates. Elle ne réutilise pas silencieusement l’aperçu
précédent. La page peut être quittée sans annuler le job. Droits relus avant
chaque acquisition et finalisation ; révocation arrête le travail et la lecture
n’est plus accessible sans `crm.consulter`.

Par source : `DISPONIBLE`, `ABSENT`, `NON_APPLICABLE`, `INDISPONIBLE`, `AMBIGU`,
`NON_PRIS_EN_CHARGE`. Par proposition : constat `INCHANGE`, `NOUVEAUTE`,
`DIFFERENCE`, `VERIFICATION_MANUELLE`, et décision indépendante `A_EXAMINER`,
`ADOPTEE`, `CONSERVEE`, `PERIMEE`. Un constat sans cible adoptable n’est pas
sélectionnable. Aucun aperçu n’est publié avant finalisation du job ; le snapshot
finalisé est immuable, ses décisions sont tracées séparément.

Provenance par proposition : UUID/job/organisation, format `1`, groupe,
objet/version cible, chemins autorisés, valeurs avant/trouvées, protections,
fournisseur/objet, consultation UTC, date/millésime de source éventuels,
empreinte normalisée, version d’adaptateur/méthode, couverture et IDs de snapshots.
Aucune réponse brute multi-objets, clé secrète ou donnée personnelle superflue
n’est conservée dans l’audit. Origine du prospect et source CSV restent intactes.

Snapshots référentiels : ID, fournisseur, format, production, millésime/géographie,
empreinte, compteurs et intégrité, états `EN_PREPARATION/VALIDE/REJETE/RETIRE`.
Publication atomique du pointeur vers un snapshot validé ; le job fige ses IDs au
démarrage. Pas de mélange de géographies sans correspondance contrôlée, pas de
snapshot incomplet. Format inconnu → `SOURCE_INCOMPATIBLE` pour cet adaptateur,
sans approximation. Un snapshot ancien garde sa date réelle ; aucune durée
universelle de fraîcheur commerciale n’est inventée ici.

Le niveau commercial E71-EVOL-06 utilise seulement les faits adoptés/confirmés
selon son contrat. Proposition/tentative ne rajeunit rien. Une adoption pertinente
incrémente les versions des faits et invalide les axes dépendants dans la même
transaction, selon le contrat E71-EVOL-06 ; aucune notification ou relance
commerciale implicite.

### 10.3. Contrats HTTP implémentés localement

Producteur backend Prospection, consommateur unique PWA CRM embarquée. Préfixe
`/internal/prospection`. Réutiliser session ERP, CSRF, capacités, `Idempotency-Key`,
`Cache-Control: no-store`, schémas fermés et contrôles objets liés. Aucun URL de
collecte ou token fournisseur envoyé par le navigateur.

| Route cible | Corps / sortie |
| --- | --- |
| `POST /organisations/{id}/actualisations` | `expected_version` positif ; `blocs` : 1–6 uniques parmi IDENTITE/TERRITOIRE/POTENTIEL/ACTIVITE/STRUCTURE/CONTACTS ; `projet_id` facultatif du prospect ; `relance_de` facultatif. 202 : job/état/lien lecture/`reutilise`, sans appel externe synchrone |
| `GET /organisations/{id}/actualisations` | Historique 25 par défaut/100 maximum, curseur lié aux droits/filtres ; ordre created_at DESC puis id DESC ; items/has_more/next_cursor ; résumés sans coordonnées |
| `GET /organisations/{id}/actualisations/{job_id}` | État, progression sources/blocs, dates, versions capturées, bilan/motifs ; pas toutes les propositions |
| `GET /organisations/{id}/actualisations/{job_id}/propositions` | Snapshot finalisé, page 25/100, curseur stable, filtres bloc/décision en stockage ; snapshot_version et total figé |
| `POST /organisations/{id}/actualisations/{job_id}/decisions` | Version snapshot, versions cibles, 1–25 décisions distinctes sur groupes cohérents ; 200 : décisions, objets/versions changés et IDs des nouvelles évaluations brouillon |

Lecture `crm.consulter`, commande `crm.gerer`, droits relus en transaction et
au rejeu. Job/contact/projet étranger au prospect → 404 sans fuite. Prospect
archivé : historique lisible, lancement et adoption refusés. Aucun nouveau droit
implicite à un responsable de prospect.

Exemple de demande et réponse synthétiques :

```json
{"expected_version":12,"blocs":["STRUCTURE","CONTACTS"]}
```

```json
{
  "id":"11111111-1111-4111-8111-111111111111",
  "etat":"EN_ATTENTE",
  "organisation_version":12,
  "reutilise":false,
  "lecture":"/internal/prospection/organisations/22222222-2222-4222-8222-222222222222/actualisations/11111111-1111-4111-8111-111111111111"
}
```

Exemple de décision ; aucune valeur fournisseur n’est renvoyée par le client :

```json
{
  "snapshot_version":1,
  "expected_organisation_version":12,
  "versions_cibles":[],
  "decisions":[{
    "proposition_id":"33333333-3333-4333-8333-333333333333",
    "decision":"ADOPTER",
    "remplacer_proteges":["telephone"]
  }]
}
```

`versions_cibles` contient les couples fermés `type,id,expected_version` des
contacts/projets/appartenances concernés. `CONSERVER` trace la décision sans
changer la valeur ou sa protection. `ADOPTER` exige `remplacer_proteges` égal
aux chemins protégés du groupe explicitement confirmés, y compris vides. Une
protection existante continue de protéger la valeur adoptée des prochains imports ;
la provenance indique le remplacement explicite sans inventer de preuve humaine.

Appartenance sans date juridique non adoptable : la saisie prouvée par commande
existante périme l’aperçu. Contact nouveau avec ressemblances : parcours actuel
d’examen obligatoire, pas de forçage via cette route. Une proposition décidée ne
reçoit pas une décision contradictoire ; relancer une nouvelle vérification.

### 10.4. Atomicité, concurrence et refus

Clé métier de déduplication active : prospect + blocs triés + périmètre/projet +
empreinte versions initiales. Contrainte unique partielle en base. Même clé
idempotente/corps → même réponse ; corps différent → 409. Nouvelle clé mais même
job actif → ce job, `reutilise=true`. Des blocs différents ne sont pas fusionnés.

Adoption **tout ou rien** pour 25 groupes maximum : relire droits/états/versions
et empreinte de couverture ; verrouiller dans un ordre fixe organisation, projets,
contacts, relations, propositions (UUID triés dans chaque type) ; appliquer domaine ;
écrire valeurs/provenance/décisions/audit/versions/invalidation et réponse
idempotente ; commit. Un groupe invalide annule tous les groupes. Aucun réseau ni
fichier lourd dans cette transaction. Les dépendances et invalidations de porteur
utilisent les versions de contacts comme aujourd’hui, sans charger tous les dossiers.

Deux décisions concurrentes se sérialisent ; version périmée refusée même si le
champ paraît identique. Réponse perdue après commit : même clé retrouve le résultat,
sans nouvel appel externe ni contact/évaluation. Les propositions restantes sur un
objet modifié deviennent périmées : nouvelle comparaison, jamais rebase silencieux.
La création d’un service déduplique son lien de provenance stable et respecte les
ressemblances ; aucune égalité d’e-mail n’autorise une fusion.

| Statut / code cible | Condition et suite |
| --- | --- |
| 401/403, gardes existantes | Session/droits manquants ou révoqués |
| 404 `RESSOURCE_INTROUVABLE` | Cible/job/enfant absent ou étranger |
| 409 `VERSION_CONFLICT` | Objet/couverture changé ; relire et relancer |
| 409 `IDEMPOTENCY_CONFLICT` | Clé réutilisée pour autre corps |
| 409 `PROPOSITION_DEJA_DECIDEE` | Décision contradictoire ; historique préservé |
| 409 `ACTUALISATION_NON_TERMINEE` | Snapshot pas encore finalisé |
| 409 `PROSPECT_ARCHIVE` | Nouveau lancement/adoption sur fiche archivée |
| 422 `PROPOSITION_NON_ADOPTABLE` | Ambiguïté, absence, groupe incomplet, protection non confirmée ou date/identité manquante |
| 422, codes qualification existants | Contraintes NA/identité/NAF/preuves/évaluation |
| 429 `ACTUALISATION_SATUREE` | File/quota local plein, Retry-After ; aucune fausse acceptation |
| 503 `ACTUALISATION_NON_CONFIGUREE` | Fonction désactivée ou aucun adaptateur configuré pour les blocs |

Enveloppe CRM actuelle : `detail.code`, `detail.message` et corrélation
transversale, pas une deuxième convention. Les erreurs fournisseurs alimentent
le bilan asynchrone, pas un 500 interactif. Un bloc absent n’empêche pas l’adoption
d’un autre bloc complet du snapshot terminal partiel.

### 10.5. Fournisseurs, budgets et capacité

Revérifications le **6 novembre 2026** :
[contrat officiel Recherche d’entreprises](https://recherche-entreprises.api.gouv.fr/openapi.json),
[communes](https://geo.api.gouv.fr/decoupage-administratif/communes),
[EPCI](https://geo.api.gouv.fr/decoupage-administratif/epcis),
[annuaire DILA](https://www.data.gouv.fr/dataservices/api-annuaire-de-ladministration-et-des-services-publics).
Recherche directe par identifiant ignore les filtres et ne couvre pas les entités
non diffusibles ; sa limite IP documentée est 7 requêtes/s et une limite ASN
s’applique aussi. Localeo conserve un plafond inférieur sans supposer un débit
garanti. Geo fournit centre et relations actuelles, pas une date juridique
fiable ni un millésime de population implicite. DILA décrit coordonnées des
services/mairies ; schéma/routes précis restent à figer par fixtures avant
activation. Aucun export BANATIC n’est assimilé à une API temps réel.

Budgets initiaux de conception **à mesurer**, non performances acquises :

| Opération | Borne / cible |
| --- | --- |
| Lancement/lecture/adoption | p95 ≤500 ms/500 ms/1 s sur cible jetable ; délai SQL 3 s, attente verrou 500 ms ; aucun réseau au lancement |
| Acquisition ponctuelle | Connexion 2 s, réponse 10 s ; 3 tentatives maximum ; 2 Mio décompressés/réponse, 10 pages et 500 objets/source/job ; 10 Mio normalisés/job |
| Concurrence et débit | 2 unités lourdes CRM maximum partagées avec les imports ; plafonds par famille : imports 2, actualisation 1, qualification 1. Préparation de référentiels incluse dans actualisation, capture incluse dans qualification ; un appel simultané/fournisseur, plafond partagé 1 requête/s sans rafale ; réduire si limite fournisseur inférieure |
| Reprises | Backoff 2 puis 8 s avec dispersion ; respecter le plus grand délai avec Retry-After ; attente persistée libère worker ; deadline 15 min après création, bail 30 s renouvelé |
| File | 100 jobs actifs/en attente/environnement ; 5 lancements/minute/acteur hors rejeu ; 429 avant acceptation si saturation |
| Préparation référentiel | Job séparé, streaming et lots 1 000 ; 2 millions d’établissements NA/snapshot, 20 Gio temporaires et 2 h/job ; dépassement → rejet et ancien snapshot conservé |
| Calcul territorial | Agrégats préparés par commune/méthode/snapshot ; 5 000 communes maximum par portée figée ; pas N appels par commerce ni total tronqué présenté complet |
| PWA | Poll au moins 5 s, 30 s après 2 min ; stop onglet masqué/terminal ; 2 pages en mémoire ; aucune donnée privée en localStorage/service worker |
| Mémoire | Acquisition/calcul ≤256 Mio additionnels ; préparation snapshot ≤512 Mio ; jamais stock national complet en mémoire |

Le limiteur partagé et les baux sont implémentés dans `ordonnancement.py` ; les
tests PostgreSQL couvrent saturation, expiration et fencing. Aucune unité ni connexion SQL conservée pendant une
attente de quota/reprise. Pour DILA/geo, ces chiffres sont des limites internes,
pas des quotas garantis.
Dépassement → `LIMITE_SOURCE`/bilan partiel, jamais comptage partiel valide.

Indexes à prouver par plans PostgreSQL : unicité active de job,
`(etat,disponible_apres,id)` pour baux, `(organisation_id,created_at,id)` historique,
`(job_id,bloc,decision,id)` propositions, unicité de provenance par
`(fournisseur,objet_id,type_cible,cible_id)`, agrégats
`(snapshot_id,methode_version,commune_insee)`. Comptage EPCI sur membres figés et
SIRET uniques ; jamais addition de totaux déjà agrégés et communes incluses.

Réutiliser ordonnanceur/supervision avec traitements cibles distincts
`crm_actualisation_qualification` et `crm_preparer_referentiels`, sans détourner
l’import CSV. Mesures : âge file, durées/source, 429, reprises, octets/lignes,
snapshots, conflits/adoptions/partiels. Logs IDs/codes/volumes, pas coordonnées.

Recette prévue : N=10 000 puis 10N=100 000 prospects avec historiques croissants,
100 000 puis 1 000 000 établissements synthétiques ; même cible/pages,
caches froid/chaud ; 1/5/20 clients, lectures CRM + écritures + les 2 unités CRM,
saturation à 100 jobs puis retour à la normale. Mesurer p50/p95/p99, SQL,
verrous, mémoire et absence de famine des autres traitements. Aucun chiffre
mesuré n’est revendiqué ici ; dépassement du budget empêche l’activation concernée.

### 10.6. Migration, compatibilité et conservation

Migrations additives v295 (actualisation), v296 (priorité), v297 (capacité partagée)
et v298 (référentiels) : jobs, propositions,
décisions, snapshots, provenance et versions/empreintes de faits pour invalidation.
FK/unicités et champs typés d’état/dates/IDs ; charges normalisées JSON à schéma
fermé versionné. Anciennes fiches, évaluations confirmées et identités CSV conservées.
Imports 1/2 et anciens clients restent compatibles sans nouveau champ obligatoire.

Ordre : migration sur sauvegarde restaurée isolée → backend contrats désactivés →
préparation des sources/snapshots et PWA → tests des six blocs applicables avec
adaptateurs qualifiés → activation de la livraison complète. Un état permanent
`NON_PRIS_EN_CHARGE` sur un cas annoncé couvert empêche cette validation ; une
indisponibilité ponctuelle du fournisseur reste un résultat partiel géré en service.
Rollback applicatif : désactiver acquisition/adoption, conserver tables/audit ;
pas de promesse de migration destructive inverse. OpenAPI généré et testé à
l’implémentation seulement ; aucun contrat fictif ajouté à l’export actuel.

Conservation **non arbitrée**, ARB-07 : durées propositions rejetées/indécises,
coordonnées sources, journaux, provenance adoptée et suppression de prospect.
Prévoir purge par lots 100, désactivée avant politique définie ; proposition
purgée non adoptable. Pas de collecte réelle avec conservation illimitée activée
par défaut. La preuve adoptée doit rester reconstructible sans réponse brute
complète, selon la politique future. Cela bloque activation réelle concernée,
pas développement/test synthétique. Aucune durée légale n’est inventée.

### 10.7. Préparation par périmètre et preuves

- Première livraison : **six blocs confirmés par l’utilisateur le 6 novembre**.
  L’identité/territoire/structure/contacts seuls ne suffisent pas à la déclarer
  terminée. Aperçu et adoption explicite conservés, sans autorisation d’écriture
  automatique.
- Méthode de comptage/familles : **arbitrage métier bloquant** pour nouveaux
  totaux/familles, donc pour la livraison complète ; le développement indépendant
  identité/coordonnées peut avancer. Préciser activités retenues, grandes
  surfaces, cas incertains et version NAF. Le fournisseur ne décide pas à la place
  du produit.
- Date juridique absente : refus d’adoption spécifié ; saisie prouvée via parcours
  existant, jamais date du clic.
- Contrats DILA/BANATIC/population : qualification technique par fixtures avant
  livraison des six blocs, pas nouvel arbitrage métier implicitement acquis.
- Rétention : ARB-07 reste ouverte, bloque collecte réelle concernée.

Tests nouveaux **prévus, non exécutés**. Matrice détaillée complétant la section 9 :

| CA | Preuve comportementale à produire | Contrat, fixtures, guides et exploitation |
| --- | --- | --- |
| 41 | PC/mobile : blocs, progression, retour après fermeture, double clic même job, navigation clavier et focus | Routes jobs/PWA ; fixture aucune différence/progression ; guide CRM |
| 42 | Domaine/adaptateur : SIRET vs siège, homonymes, SIREN/INSEE contradictoire, non diffusible, hors NA, aucune création ERP | Mapping fermé, fixtures sources versionnées |
| 43 | Domaine/PostgreSQL : vide protégé, adoption/refus, groupes indivisibles, annulation totale si un groupe échoue, réponse perdue/rejeu | Adoption/provenance/audit atomiques, aide comparaison |
| 44 | Brouillon créé, confirmé immutable, références séparées, couverture EPCI/projet, source millésimée, incomplet/non comparable, date juridique absente | Sources synthétiques et méthode approuvée ; garde activation par bloc ; diagnostic potentiel |
| 45 | Service nouveau/candidat ressemblant, contact étranger refusé, coordonnée changée invalide vérification/porteur, absence non destructrice | Contrats contact réutilisés ; pas de rôle/consentement inventé |
| 46 | Consultation/source/millésime/preuve distincts, proposition non adoptée ne rajeunit pas le score, historique séparé des échanges | Bilan/provenance typés, source ancienne/inconnue |
| 47 | 429 et Retry-After au-delà deadline, bail expiré, JSON incompatible, plafonds pages/octets, snapshot rejeté ; N/10N et mixte | Jobs supervisés et doubles fournisseurs ; mesures/reprise sans réseau réel |
| 48 | Révocation lancement/worker/commit/rejeu, deux gestionnaires, concurrence projet/contact, même job nouvelle clé, conflit idempotence | Verrous/versions/déduplication, erreurs stables et audit |
| 49 | Migration/restauration jetable, ancien client/CSV, nouvelles routes, démonstration sans réseau, export contrat cohérent | Générateur/guide ops/contrat à adapter, rétention conditionnelle et rollback applicatif |

Fichiers cibles backend à créer :
`tests/domain/prospection/test_actualisation_dedicated.py`,
`tests/application/test_crm_actualisation.py`,
`tests/api/test_crm_actualisation_api.py`,
`tests/integration/test_crm_actualisation_postgres.py`,
`tests/browser/crm-actualisation.cjs`, tests adaptateurs et campagne de capacité.
Ce sont des destinations prévues, pas des fichiers existants ou preuves réussies.
Contrôles d’architecture requis lors de l’implémentation des objets/use cases.

Impacts : backend (domaine/application/API/persistance/PWA/jobs/générateur/tests),
projet (source présente, guides CRM/ops, contrat exporté, matrice livraison).
Les trois autres frontends ne consomment pas ces API privées, donc aucun impact
direct actuel ; à reconfirmer à la revue du contrat implémenté. Aucun test externe,
ancien bilan ou contrôle de lien ne valide ces nouveaux comportements.

### Complétude d’un bloc implémentée

Un résultat `DISPONIBLE` peut préciser `complet=false` et un `motif` lorsqu’un
sous-bloc n’est pas comparable ou manque. Le job devient alors
`TERMINE_PARTIELLEMENT`, tout en conservant les propositions complètes adoptables.
La reprise conserve ce constat et les mêmes identifiants de snapshots.
