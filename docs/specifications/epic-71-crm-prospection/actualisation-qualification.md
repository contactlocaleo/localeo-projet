# E71-EVOL-05 — Vérifier et actualiser la qualification d’un prospect

Cadrage et proposition fonctionnelle du **5 novembre 2026**, à la demande
« rafraîchir à la demande les informations de qualification ». Cette évolution
de l’[epic 71](../../roadmap/en-cours/epic-71-crm-prospection-animation-coffrets-pro-backlog.md)
complète la [qualification structurée](qualification-structuree.md).
**Non implémentée** : cette demande porte sur la manière de procéder. Les choix
recommandés ci-dessous ne constituent pas des arbitrages utilisateur acquis.

## 1. Existant et résultat recherché

Le bouton d’actualisation actuel relit le CRM ; il ne consulte pas les sources
externes. Les qualifications sont renseignées manuellement ou par CSV. Le
connecteur géographique ne fournit que nom/INSEE/centre ; son rattrapage des
communes manquantes ne rafraîchit ni la population ni les contacts ou évaluations.
Aucun connecteur produit Sirene, BANATIC ou annuaire administratif n’est présent
dans l’implémentation examinée, basée sur backend `86b7fa0`.

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
Le mapping exact des champs administratifs nouveaux est à finaliser avant code ;
aucun attribut n’est caché dans une note pour éviter ce travail de modélisation.

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

## 6. Fraîcheur, historique et contrats à préparer

L’[évolution E71-EVOL-06](niveau-qualification.md) utilise les faits adoptés pour
calculer un niveau de priorité commerciale (potentiel, maturité et fiabilité).
Une simple tentative d’actualisation, ou une proposition non adoptée, ne lui
fournit pas de nouvelle preuve ; après adoption d’un fait pertinent, l’ancien
résultat de qualification doit être signalé à recalculer.

Par bloc/champ proposé, conserver : identifiant du fournisseur et de son objet,
valeur courante et version de départ, valeur trouvée, date de consultation,
date/millésime de la source lorsqu’il est connu, couverture, méthode/version,
résultat de comparaison et décision d’adoption ou de refus. La source d’import
et l’**Origine du prospect** restent inchangées ; elles ne servent pas à stocker
cette nouvelle provenance. Les faits de vérification humaine restent séparés.

États de traitement recommandés : `EN_ATTENTE`, `EN_COURS`, `TERMINE`,
`TERMINE_PARTIELLEMENT`, `ECHEC`. Un traitement terminé peut conclure « aucune
différence ». Les résultats indisponibles sont visibles par fournisseur ; les
propositions obtenues restent consultables sans promettre une vérification complète.

Contrats cibles **non existants**, à détailler puis exporter depuis le code lors
de leur implémentation : demande d’actualisation (202, blocs et version attendue),
lecture de progression/propositions paginées, application/rejet des propositions
sélectionnées avec idempotence et versions attendues. Un aperçu périmé est refusé
sans écraser une modification concurrente ; le gestionnaire peut relancer.
Le JSON OpenAPI actuel reste celui des API réellement implémentées.

Le domaine Prospection porte l’adoption, les conflits et les invariants ;
l’application orchestre les ports de référentiel et transactions ; les adaptateurs
normalisent les sources ; la PWA présente l’aperçu. Réseau hors transaction SQL,
reprise durable et absence de nouvel appel externe lors du rejeu d’une application.

## 7. Bornes et livraison à spécifier avant activation

Un prospect par demande, six blocs au maximum. Pas de lancement global du
portefeuille ni de rafraîchissement à chaque ouverture de fiche en première version.
Dédupliquer les demandes actives pour un même prospect/périmètre ; propositions
et historique paginés 25/100. Les appels ponctuels et calculs territoriaux ont des
files et budgets séparés : acquisition/API interactives courtes, préparation des
référentiels volumineux par traitements bornés. Les quotas seront centralisés
entre workers, avec timeouts, reprises limitées, attente fournisseur respectée et
échecs partiels explicites. Aucune transaction ni verrou métier pendant le réseau.

Avant implémentation : fixer par adaptateur les limites de requêtes/octets/pages,
le débit partagé, les index et volumes du référentiel NA, le budget de réponse 202,
la durée maximale des jobs et la conservation des propositions. Ces chiffres
restent **à spécifier**, pas des performances acquises. La conservation relève
aussi de l’arbitrage ARB-07 existant ; cette proposition ne le tranche pas.

Prévoir migration additive des demandes/propositions/provenances et conservation
des anciennes fiches ; aucune réécriture des observations existantes. Réutiliser
ordonnancement et supervision communs, avec identité de batch propre à ce travail
si nécessaire. Le batch des imports ne doit pas devenir un collecteur multi-source.
Le CSV 1/2 reste compatible et n’exige pas une nouvelle colonne.

## 8. Choix proposés et points encore ouverts

| Sujet | Recommandation, à valider avant la partie d’implémentation concernée |
| --- | --- |
| Adoption des données | Aperçu et sélection explicite, y compris pour les champs vides ; aucun remplacement automatique en première version |
| Potentiel commercial | Réutiliser la méthode du fichier après formalisation de la sélection et de la répartition en familles, versionner les règles et compter des établissements uniques ; méthode non approuvée = pas de nouveau total annoncé |
| Territoire courant sans date juridique | Présenter un constat daté et demander la date d’effet pour remplacer la relation historique ; ne jamais utiliser automatiquement le jour du clic comme date d’adhésion |
| Sources de contacts | Démarrer par les coordonnées institutionnelles des collectivités ; compléter les contacts de commerces manuellement faute de source fiable identifiée ; pas de service payant ou collecte sur des sites arbitraires ajoutés implicitement |
| Déploiement progressif | Identité/territoire/structure/contacts publics d’abord ; comptages et compétences après qualification des référentiels. Un bloc non équipé reste explicitement non disponible, jamais déclaré couvert |

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

Contrôles documentaires exécutés : guides et 146 sources exportées validés,
bundle local généré puis vérifié par empreintes (147 documents distribués, dont
le manifeste). Tests des lecteurs et outils documentaires : **38 réussis**,
**2 non exécutés**, création de liens symboliques non autorisée sur cette plateforme.
La revue indépendante a fait préciser la propriété de la population, le niveau
du NAF, le périmètre applicable et la priorité terrain. Ces contrôles ne prouvent
aucun des nouveaux comportements de rafraîchissement, qui restent à développer.
