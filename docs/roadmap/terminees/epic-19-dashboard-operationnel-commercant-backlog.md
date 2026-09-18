# Backlog Epic 19 - Dashboard operationnel commercant

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Perimetre

Epic source : `Epic 19. Dashboard operationnel commercant`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif : fournir dans l'application commercant une vue de pilotage simple permettant a un commercant de mesurer l'activite generee par Localeo, le montant reverse associe, l'encours de prestations achetees non consommees et la repartition par version de prestation.

## Statut global

- Epic 19 : `Termine`
- Avancement : cadrage produit finalise et API backend V1 implementee. L'integration UX application commercant reste a realiser hors backend.

## Vision produit

Le dashboard commercant doit etre une page de suivi operationnel et de confiance. Il doit montrer concretement la valeur apportee par Localeo sans devenir un outil comptable complexe.

Questions auxquelles le dashboard doit repondre :
- combien de trafic Localeo arrive chez le commercant ;
- combien de reversement Localeo est genere ;
- combien de prestations achetees restent a consommer ;
- quelles prestations fonctionnent le mieux ;
- quelle version d'une prestation est concernee quand plusieurs versions ont existe ;
- comment ces indicateurs evoluent sur une periode choisie.

## Surface ciblee

### Application commercant

Objectif : donner au commercant une lecture claire de son activite Localeo.

Contenus attendus :
- periode filtree ;
- synthese des indicateurs clefs ;
- trafic et passages generes par Localeo ;
- montant reverse associe ;
- encours de prestations achetees mais non consommees ;
- prestations consommees ;
- repartition par prestation et par version de prestation ;
- tendances simples sur la periode.

## Donnees disponibles

Sources existantes utiles :
- `statuts_prestation_coffret_instance` pour les prestations a valider, validees et expirees ;
- `validations_prestation` pour les consommations effectives ;
- `prestations_coffret.version_courante` et `prestations_coffret_versions.numero_version` pour la lecture versionnee ;
- `mouvements_reversement` pour les montants a reverser ou reverses ;
- `reversements` et `paiements_reversement` pour le suivi financier execute ;
- `achats_coffret` et `coffrets_instances` pour relier achat, activation et periode ;
- `activites_locales` pour certains signaux de trafic public ou feed local ;
- `feedbacks_prestation` pour enrichir plus tard les signaux qualitatifs.

## Definitions metier

### Trafic genere par Localeo

En V1, le trafic Localeo est mesure par des signaux backend observables :
- nombre de prestations achetees rattachees au commercant ;
- nombre de prestations consommees chez le commercant ;
- nombre de coffrets instances contenant au moins une prestation du commercant ;
- nombre d'activites locales publiques rattachees au commercant ou a ses prestations.

Les visites web anonymes ou impressions front ne sont pas incluses en V1, sauf ajout ulterieur d'un tracking dedie.

### Montant reverse genere

En V1, la valeur economique affichee au commercant correspond au montant reverse au commercant, pas au montant client du coffret prorate.

Le dashboard doit distinguer clairement :
- montant potentiel lie aux prestations achetees mais non consommees ;
- montant valide apres consommation ;
- montant a reverser ;
- montant deja reverse ou paye.

En V1, la source de verite financiere recommandee est le mouvement de reversement quand il existe. A defaut, le montant de reversement snapshotable de la prestation peut etre utilise comme estimation.

### Encours

L'encours correspond aux prestations rattachees au commercant qui ont ete achetees dans un coffret mais ne sont pas encore consommees.

Regle V1 :
- `A_VALIDER` = encours consommable ;
- `VALIDEE` = prestation consommee ;
- `EXPIREE` = encours perdu ou non consommable ;
- les statuts annules doivent etre exclus ou isoles si disponibles.

### Version de prestation

Si plusieurs versions d'une meme prestation existent, le dashboard doit permettre de lire la repartition par version.

Regle V1 :
- chaque ligne de consommation ou d'encours doit exposer `prestation_coffret_id` et `prestation_version` ;
- `prestation_version` doit etre snapshottee sur les statuts de prestation afin de garantir une repartition exacte par version ;
- pour les donnees historiques sans snapshot, le backend expose explicitement la methode d'approximation ou retourne `version_inconnue`.

## API commercant recommandee

Endpoint :
- `GET /protected/commercants/me/dashboard-operationnel`

Parametres :
- `date_debut` optionnel, format `YYYY-MM-DD` ;
- `date_fin` optionnel, format `YYYY-MM-DD` ;
- `group_by` optionnel : `jour`, `semaine`, `mois` ;
- `prestation_id` optionnel ;
- `inclure_versions` optionnel, defaut `true`.

Periode par defaut :
- si aucun filtre de dates n'est fourni, `date_debut` est positionne au premier jour du mois courant et `date_fin` au dernier jour du mois courant.

Contraintes :
- authentification commercant obligatoire ;
- le commercant ne peut consulter que ses propres donnees ;
- les dates doivent etre bornees cote backend pour eviter les requetes trop lourdes ;
- les donnees client personnelles ne sont jamais exposees ;
- les montants doivent etre exprimes en euros avec une precision stable.

Contrat de reponse recommande :

```json
{
  "commercant_id": "uuid",
  "periode": {
    "date_debut": "2026-05-01",
    "date_fin": "2026-05-31"
  },
  "kpis": {
    "prestations_achetees": 42,
    "prestations_en_encours": 18,
    "prestations_consommees": 24,
    "prestations_expirees": 0,
    "montant_potentiel_encours": 360.0,
    "montant_valide": 480.0,
    "montant_a_reverser": 240.0,
    "montant_reverse": 240.0
  },
  "par_prestation": [
    {
      "prestation_id": "uuid",
      "libelle": "Massage 30 min",
      "version_courante": 3,
      "prestations_achetees": 12,
      "prestations_en_encours": 5,
      "prestations_consommees": 7,
      "montant_valide": 140.0,
      "versions": [
        {
          "numero_version": 2,
          "prestations_achetees": 4,
          "prestations_en_encours": 1,
          "prestations_consommees": 3,
          "montant_valide": 60.0
        },
        {
          "numero_version": 3,
          "prestations_achetees": 8,
          "prestations_en_encours": 4,
          "prestations_consommees": 4,
          "montant_valide": 80.0
        }
      ]
    }
  ],
  "series": [
    {
      "periode": "2026-05-01",
      "prestations_achetees": 3,
      "prestations_consommees": 1,
      "montant_valide": 20.0
    }
  ]
}
```

## User Stories detaillees

### `PRD-099` Dashboard operationnel commercant


Statut : `Termine`

En tant que commercant authentifie, je veux consulter un dashboard operationnel afin de mesurer l'activite apportee par Localeo.

Resultats attendus :
- le dashboard est accessible depuis l'application commercant ;
- les indicateurs affiches concernent uniquement le commercant authentifie ;
- les KPIs principaux sont lisibles sans expertise comptable.

### `PRD-100` Mesure du trafic Localeo


Statut : `Termine`

En tant que commercant, je veux mesurer le trafic genere par Localeo afin de comprendre le volume d'opportunites apporte.

Resultats attendus :
- le dashboard affiche le nombre de prestations achetees ;
- le dashboard affiche le nombre de prestations consommees ;
- le dashboard affiche les coffrets ou instances contenant mes prestations lorsque c'est utile ;
- aucun detail client personnel n'est expose.

### `PRD-101` Montant reverse et reversements


Statut : `Termine`

En tant que commercant, je veux connaitre le montant de reversement genere par Localeo afin de suivre la valeur economique de ma participation.

Resultats attendus :
- le dashboard distingue montant potentiel, montant valide, montant a reverser et montant reverse ;
- les montants sont filtres sur la periode choisie ;
- les montants affiches sont coherents avec les mouvements de reversement.

### `PRD-102` Encours de prestations non consommees


Statut : `Termine`

En tant que commercant, je veux voir l'encours des prestations achetees mais non consommees afin d'anticiper les passages clients a venir.

Resultats attendus :
- le dashboard affiche le nombre de prestations `A_VALIDER` ;
- l'encours est disponible globalement et par prestation ;
- les prestations expirees ou annulees ne sont pas melangees avec l'encours consommable.

### `PRD-103` Repartition par version de prestation


Statut : `Termine`

En tant que commercant, je veux voir la repartition par version de prestation afin de comprendre l'impact des evolutions de mon offre.

Resultats attendus :
- le dashboard affiche les indicateurs par `prestation_id` ;
- le dashboard affiche une sous-repartition par `numero_version` quand plusieurs versions existent ;
- les versions anciennes restent lisibles meme si la prestation courante a change ;
- si la version exacte n'est pas disponible historiquement, le backend expose explicitement la methode d'approximation ou retourne `version_inconnue`.

### `PRD-104` Filtrage par plage de dates

En tant que commercant, je veux filtrer le dashboard sur une plage de dates afin d'analyser une semaine, un mois ou une periode personnalisee.

Resultats attendus :
- `date_debut` et `date_fin` filtrent tous les indicateurs ;
- les dates invalides sont rejetees avec une erreur explicite ;
- une periode par defaut correspondant au mois courant est appliquee si aucun filtre n'est fourni ;
- une borne maximale de periode protege le backend.

## Backlog d'implementation

### Lot 1 - Modele de lecture et cadrage des versions

Objectif : clarifier la source de verite des indicateurs et la version de prestation associee.

Statut : `Termine`

Taches :
- identifier si `statuts_prestation_coffret_instance` porte ou peut retrouver la version de prestation au moment de l'achat ;
- ajouter un snapshot `prestation_version` sur les statuts de prestation ;
- documenter la strategie de fallback pour les donnees historiques ;
- definir les statuts inclus dans encours, consomme, expire ou annule.

### Lot 2 - Use case dashboard commercant

Objectif : centraliser les calculs metier.

Statut : `Termine`

Taches :
- implementer le calcul des KPIs globaux ;
- implementer le detail par prestation ;
- implementer le detail par version ;
- implementer les series temporelles ;
- appliquer les filtres de date ;
- garantir le cloisonnement par commercant.

### Lot 3 - API commercant

Objectif : exposer les donnees a l'application commercant.

Statut : `Termine`

Taches :
- implementer `GET /protected/commercants/me/dashboard-operationnel` ;
- ajouter les schemas de requete/reponse ;
- ajouter les validations de dates et bornes de periode ;
- proteger l'endpoint par session commercant ;
- ne jamais exposer de donnees client personnelles.

### Lot 4 - UX application commercant

Objectif : rendre les indicateurs actionnables et lisibles.

Statut : `Termine`

Taches :
- afficher les KPIs principaux ;
- afficher un graphique simple par periode ;
- afficher le tableau par prestation ;
- afficher le detail par version ;
- ajouter les filtres de dates ;
- gerer les etats vides.

### Lot 5 - Tests et validation

Objectif : securiser les calculs et le cloisonnement.

Statut : `Termine`

Taches :
- tester le cloisonnement par commercant ;
- tester les filtres de date ;
- tester les KPIs globaux ;
- tester l'encours `A_VALIDER` ;
- tester la repartition par version ;
- tester les montants de reversement ;
- tester l'absence de donnees client dans la reponse.

## Criteres d'acceptation globaux

- Un commercant authentifie peut consulter son dashboard operationnel.
- Les indicateurs ne concernent que le commercant authentifie.
- Le dashboard affiche prestations achetees, consommees, en encours et expirees.
- Le dashboard affiche les montants utiles : potentiel, valide, a reverser et reverse.
- Le dashboard permet de filtrer par plage de dates.
- Le dashboard expose une repartition par prestation.
- Le dashboard expose une repartition par version de prestation quand elle est disponible.
- Aucune donnee personnelle client n'est exposee.
- Les periodes trop longues sont bornees cote backend.

## Hors perimetre V1

- Tracking web d'impressions ou de clics front temps reel.
- Attribution marketing multi-canal.
- Export comptable avance.
- Comparaison avec d'autres commercants.
- Objectifs commerciaux ou previsions.
- Notifications automatiques de performance.
