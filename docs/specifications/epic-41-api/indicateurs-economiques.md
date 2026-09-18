# Epic 41 - Indicateurs economiques et d'usage des gains

> Consolidation documentaire du 18 septembre 2026 : contributions Backend et Animation réunies ; les définitions communes et le complément ANIM-007 sur les exports CSV sont conservés.

## Objectif

Completer le dashboard, le bilan et la Vision 360 Animation avec cinq indicateurs permettant de suivre la valeur encore mobilisable, l'urgence de consommation, le delai d'usage et la contribution des commercants.

Ces indicateurs sont des projections en lecture. Ils reutilisent les gains `animation_locale`, les coffrets instances et les statuts de prestations de `gestion_achats`; ils ne creent pas de source de verite ni de mouvement financier.

## Population et conventions communes

- Un gain entre dans les calculs lorsqu'il n'est pas suppleant, qu'il est `ENVOYE` et qu'il possede un `coffret_instance_id`.
- Une prestation est consommee uniquement lorsque son statut courant est `VALIDEE` et que sa `date_validation` est renseignee. Une validation annulee ne compte plus.
- Les montants reposent sur le `montant_reversement` snapshotte sur la prestation du coffret au moment de l'attribution. Ils sont exposes en centimes entiers avec `devise: "EUR"`; aucun calcul n'est effectue a partir d'un prix catalogue courant.
- Le montant dit reinjecte mesure la valeur des prestations effectivement consommees chez les commercants. Il ne prouve ni le calcul ni l'execution bancaire d'un reversement.
- Les dates sont exposees en ISO 8601 UTC. Les durees sont calculees en secondes puis exposees en heures, arrondies a deux decimales.
- Pour le bilan et la Vision 360 d'une animation, les calculs portent sur tous les gains de cette animation jusqu'a `generated_at`, y compris les consommations posterieures a sa cloture. Le filtre de periode du dashboard selectionne les animations, mais ne tronque pas le cycle de consommation de leurs gains.
- Les gains remplaces, annules, sans instance ou encore `A_ENVOYER` sont exclus. Leur nombre doit rester visible dans les alertes de coherence.

## Definitions opposables

### 1. Montant potentiel restant a reinjecter

Champ : `montant_potentiel_restant_a_reinjecter_centimes`.

Somme des `montant_reversement` des prestations non `VALIDEE` appartenant aux gains retenus dont le coffret est encore utilisable a `generated_at` : instance non annulee, non expiree et sans blocage d'usage.

- Une prestation deja consommee est exclue.
- Une prestation restante d'un coffret partiellement consomme est incluse.
- Un coffret expire est exclu du potentiel mobilisable et remonte dans les indicateurs d'expiration.
- Une valeur manquante ou negative constitue une anomalie et n'est pas assimilee a zero silencieusement.

### 2. Coffrets non consommes arrivant bientot a expiration

Champ : `coffrets_non_consommes_expirant_bientot`.

Nombre de coffrets issus des gains retenus qui ne possedent aucune prestation `VALIDEE` et dont la date d'expiration est strictement posterieure a `generated_at` et inferieure ou egale a `generated_at + horizon_expiration_jours`.

L'horizon est un entier compris entre 1 et 365, vaut 30 jours par defaut et est retourne dans la reponse. Un coffret partiellement consomme n'entre pas dans ce compteur; il reste visible dans le compteur distinct des coffrets partiellement consommes.

### 3. Delai moyen entre l'envoi du gain et sa premiere consommation

Champ : `delai_moyen_envoi_gain_premiere_consommation_heures`.

Moyenne de `premiere_date_validation - gain.envoye_at` pour les gains retenus ayant au moins une prestation actuellement `VALIDEE`. La premiere date est le minimum des `date_validation` du coffret.

- Les gains jamais consommes sont exclus de la moyenne.
- Une date de validation anterieure a `envoye_at` est exclue et genere une anomalie de donnees.
- `null` est retourne lorsque l'echantillon est vide; la valeur `0` est reservee a un delai reel nul.
- `nombre_coffrets_avec_premiere_consommation` est retourne avec la moyenne pour rendre l'echantillon explicite.

### 4. Nombre de commercants sans aucune validation

Champ : `nombre_commercants_sans_aucune_validation`.

Nombre de commercants participants effectifs de l'animation qui ne possedent aucune validation de passage au statut courant `VALIDEE` sur toute la duree de l'animation.

La population de reference comprend uniquement les commercants ayant accepte leur invitation et integres a la configuration effective selon l'Epic 56. Les invitations en attente, refusees, expirees ou annulees ne gonflent pas cet indicateur. Une validation annulee ne suffit pas a sortir un commercant du compteur.

Le contrat retourne egalement `nombre_commercants_participants_effectifs` afin de permettre le calcul et l'affichage du taux correspondant.

### 5. Repartition du montant reinjecte par commercant

Champ : `repartition_montant_reinjecte_par_commercant`.

Regroupement des prestations `VALIDEE` des gains retenus par commercant porteur de la prestation. Chaque ligne contient :

- `commercant_id` et `nom_commercant` ;
- `montant_reinjecte_centimes` ;
- `nombre_prestations_consommees` ;
- `part_du_montant_reinjecte_pourcentage`, arrondie a deux decimales.

La liste est triee par montant decroissant puis par identifiant pour garantir un ordre stable. Sa somme doit etre egale au `montant_reinjecte_centimes` global. Une prestation sans commercant resolvable est conservee dans une ligne `commercant_id: null`, libellee `Commercant non renseigne`, et declenche une alerte de coherence.

## Contrat de reponse cible

Les champs sont ajoutes aux reponses de :

- `GET /protected/animation-locale/dashboard-performance` ;
- `GET /protected/animation-locale/animations/{animation_id}/bilan` ;
- `GET /internal/animation-locale/vision-360/animations/{animation_id}/indicateurs`.

Extrait commun :

```json
{
  "consommation_financiere": {
    "devise": "EUR",
    "montant_reinjecte_centimes": 125000,
    "montant_potentiel_restant_a_reinjecter_centimes": 48000,
    "coffrets_non_consommes_expirant_bientot": 7,
    "horizon_expiration_jours": 30,
    "delai_moyen_envoi_gain_premiere_consommation_heures": 93.5,
    "nombre_coffrets_avec_premiere_consommation": 12,
    "nombre_commercants_sans_aucune_validation": 3,
    "nombre_commercants_participants_effectifs": 18,
    "repartition_montant_reinjecte_par_commercant": [
      {
        "commercant_id": "00000000-0000-0000-0000-000000000001",
        "nom_commercant": "Exemple",
        "montant_reinjecte_centimes": 25000,
        "nombre_prestations_consommees": 5,
        "part_du_montant_reinjecte_pourcentage": 20.0
      }
    ]
  }
}
```

Le parametre optionnel `horizon_expiration_jours` est accepte par ces trois routes. Pour preserver la compatibilite, le champ historique `montant_reinjecte` en euros reste retourne pendant une version d'API et est documente comme deprecie au profit de `montant_reinjecte_centimes`.

## Criteres de recette

- Les cinq indicateurs sont identiques entre dashboard, bilan et Vision 360 pour une meme animation, un meme horizon et un meme `generated_at`.
- Les sommes monetaires sont testees avec un coffret non consomme, un coffret partiel, un coffret entierement consomme et un coffret expire.
- La moyenne est testee avec un echantillon vide, plusieurs consommations du meme coffret et une validation annulee.
- Le compteur commercant est teste avec des invitations acceptees, en attente, refusees et avec une validation annulee.
- La repartition est stable, reconcilie le total global au centime et n'expose aucune donnee personnelle de gagnant.
- Le calcul reste une projection synchrone avec le cache court de la Vision 360; si le budget de 1,5 seconde sur 365 jours n'est plus tenu, des index sont ajoutes avant d'envisager une table analytique.


## ANIM-007 - Export CSV et cellules texte

Les valeurs textuelles commencant par un operateur de formule, sa variante pleine
largeur, ou un controle de ligne sont prefixees par `Texte: ` dans le CSV.
Cela concerne aussi les telephones commencant par +. Les nombres types (y compris
negatifs) restent numeriques; les donnees sources ne sont pas modifiees. Les
separateurs, guillemets et retours ligne sont echappes par le serialiseur CSV.
Le prefixe visible est conserve lors d'un reenregistrement en tableur, contrairement
aux echappements speciaux susceptibles d'etre retires par Excel.
Reference : [OWASP CSV Injection](https://owasp.org/www-community/attacks/CSV_Injection).
