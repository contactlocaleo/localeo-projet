# E71 — Préparer les sources de qualification

Cette procédure concerne l’exploitant. Le gestionnaire utilise **Vérifier les
données**, puis choisit les propositions dans le CRM. Le clic ne télécharge pas
un stock national et ne transforme pas une ancienne photographie en donnée récente.

## Sources et méthode

Les consultations ponctuelles utilisent des hôtes fixes : découpage administratif
`geo.api.gouv.fr`, Recherche d’entreprises et annuaire administratif DILA. Les
réponses sont bornées, normalisées puis comparées à l’identité exacte. Les
réponses brutes, noms d’agents et informations personnelles non nécessaires ne
sont pas conservés. Aucun site fourni dans une fiche prospect n’est interrogé.

Le potentiel utilise une photographie régionale préparée à partir des sources
officielles. La méthode **PROXIMITE_NAF_REV2_1** retient les établissements actifs
de proximité, une seule fois par SIRET. Les familles sont exclusives ; les cas
incertains sont distincts et le contrôle terrain n’est jamais déduit du NAF.
Cette base a été confirmée le 6 novembre 2026.

| Famille | Règle de première version |
| --- | --- |
| Alimentaire | Artisanat alimentaire sélectionné, commerces alimentaires spécialisés et petites surfaces alimentaires |
| Boutiques | Commerces de détail en magasin, équipements et biens personnels |
| Restauration | Restauration traditionnelle/rapide et débits de boissons |
| Beauté / coiffure | NAF 96.02A et 96.02B |
| Services de proximité | Réparations de biens personnels/équipements et blanchisserie de détail sélectionnées |
| Grandes surfaces | NAF 47.11D, 47.11F et 47.19A |

La liste exhaustive versionnée est dans le [domaine de comptage](../../../../localeo-backend/app/domaine/prospection/comptage_proximite.py).
Vente ambulante, à distance et activités ambiguës restent à vérifier. Un NAF
inconnu ou une nomenclature non prise en charge ne vaut pas zéro. Le NAF 2025
n’est pas substitué silencieusement à la révision 2. L’Insee précise que le code
APE est statistique ; il ne prouve pas l’accueil réel du public. Voir la
[nomenclature officielle](https://www.insee.fr/fr/statistiques/fichier/2120875/Nomenclatures_NAF_Reedition_2020.pdf)
et le [répertoire Sirene](https://www.insee.fr/fr/information/3591226).

## Fichiers préparés par l’exploitant

Le préparateur lit des fichiers locaux configurés côté serveur. Il ne propose
pas d’upload ni d’URL arbitraire dans l’API. Les exports population et BANATIC
doivent être normalisés selon les colonnes ci-dessous ; cette conversion n’est
pas un import direct de leur classeur d’origine.

- **Sirene** : CSV UTF-8 avec en-têtes natifs `siret`,
  `etatAdministratifEtablissement`, `activitePrincipaleEtablissement`,
  `nomenclatureActivitePrincipaleEtablissement`, `codeCommuneEtablissement`,
  `statutDiffusionEtablissement` ; séparateur virgule. Conserver la couverture
  complète annoncée par le manifeste, et les codes comme du texte.
- **Communes** : CSV UTF-8, séparateur `;` : `insee;nom;population;population_annee;population_source_date;population_source_ref`.
  Population municipale et millésime explicites ; la date du téléchargement ne
  remplace pas l’année statistique. Couvrir toutes les communes du stock régional.
- **EPCI** : CSV UTF-8, séparateur `;` :
  `siren;nom;membres_insee;competence_commerce;competence_tourisme;competence_marches;source_date;source_reference`.
  Membres de Nouvelle-Aquitaine séparés par `|`, sans doublons. Compétences :
  `OUI`, `NON`, `INTERET_COMMUNAUTAIRE`, `INCONNUE`. Une compétence non publiée
  reste inconnue. La source et la date sont obligatoires ; ne pas déduire une
  compétence de la seule nature de l’EPCI.

Sources : [populations Insee](https://www.insee.fr/fr/statistiques/8681011),
[BANATIC](https://www.banatic.interieur.gouv.fr/),
[schéma DILA](https://api-lannuaire.service-public.gouv.fr/explore/dataset/api-lannuaire-administration/).
Les tests utilisent uniquement des exemples synthétiques de ces contrats.

## Manifeste et publication

Créer un manifeste JSON privé, puis renseigner `CRM_REFERENTIEL_MANIFEST` avec
son chemin absolu sur le serveur. Exemple de structure à compléter :

```json
{
  "format": 1,
  "methode_version": "PROXIMITE_NAF_REV2_1",
  "source_date": "2026-11-01",
  "millesime": "2026-11",
  "reference": "Sources officielles et géographie de novembre 2026",
  "complet": true,
  "etablissements_actifs_na_attendus": 123456,
  "sirene_csv": "/stockage-prive/crm/sirene.csv",
  "communes_csv": "/stockage-prive/crm/communes.csv",
  "epcis_csv": "/stockage-prive/crm/epcis.csv",
  "empreintes_sha256": {
    "sirene_csv": "REMPLACER_PAR_SHA256",
    "communes_csv": "REMPLACER_PAR_SHA256",
    "epcis_csv": "REMPLACER_PAR_SHA256"
  }
}
```

Le total illustré est fictif : renseigner le nombre contrôlé d’établissements
actifs uniques de Nouvelle-Aquitaine. Les empreintes sont celles des fichiers
examinés. Une contradiction SIRET, un dépassement ou une source incomplète
rejette la nouvelle publication ; le référentiel précédent reste disponible.
Le préparateur travaille en flux, déduplique sur disque et écrit par lots.

Appliquer les migrations **v295 à v298**, préparer la conservation ARB-07, puis
activer explicitement `LOCALEO_FEATURE_CRM_REFERENTIELS_ENABLED` et déclencher
**Préparer les référentiels de qualification CRM** dans la supervision. Vérifier
les volumes, dates et empreintes avant l’activation de l’actualisation. Les
traitements de référentiel, d’import et de calcul partagent une capacité bornée.

Une demande d’actualisation fige les versions utilisées. Une nouvelle publication
ne remplace pas les données d’un aperçu déjà commencé. L’adoption reste explicite,
les nouvelles évaluations sont des brouillons, et les références de comptage,
population et compétences restent des choix du gestionnaire.

La première publication régionale crée la première photographie d'attribution
territoriale : les comptages précédemment retenus pour les communes/EPCI présents
doivent être revérifiés puis explicitement choisis de nouveau. Ce comportement
conservateur ne signifie pas qu'un changement de territoire a été démontré.
Ensuite, seules les modifications d'existence communale ou de composition d'EPCI
invalident cette attribution ; une nouvelle population ou un nouveau comptage
documentaire ne remplace pas une référence adoptée.

## Limites de mise en service

Les adaptateurs et fichiers normalisés sont testés localement ; aucune collecte
réelle ni publication sur TEST n’a été réalisée par cette implémentation. Les
sources officielles peuvent être indisponibles ou ne pas publier tous les blocs.
Un résultat partiel reste identifié comme tel. La préparation d’une vraie source,
la politique de conservation et les budgets de capacité sont des prérequis
d’activation, distincts des preuves fonctionnelles de l’epic.
