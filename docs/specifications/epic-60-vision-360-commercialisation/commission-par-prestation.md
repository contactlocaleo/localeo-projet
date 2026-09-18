# Commission par prestation et saisie en euros

Decision utilisateur du 7 septembre 2026, prioritaire sur la marge cible par
type de coffret de l'Epic 60 et les anciens scenarios de recette.

- La saisie porte sur la valeur TTC en euros et le taux de commission Localeo
  propre a chaque prestation, de 0 a 100 %, avec deux decimales au maximum.
- Reversement = valeur TTC x (100 - taux) / 100, arrondi au centime le plus
  proche (demi-centime vers le haut). Marge de prestation = valeur - reversement.
- Exemple : 100,00 EUR et 20 % donnent 80,00 EUR reverses et 20,00 EUR de marge.
- Le serveur calcule le montant ; le navigateur presente une estimation en
  direct. Les API ERP continuent a transporter des montants entiers en centimes.
- Le taux est conserve sur le modele, la prestation et sa nouvelle version.
  Les anciens montants et versions restent inchanges ; un taux historique absent
  reste inconnu, sans reconstitution approximative. L'edition dans la nouvelle
  interface exige une saisie explicite du taux pour les nouvelles conditions.
- Les anciens clients envoyant seulement le reversement restent compatibles ;
  ils ne beneficient pas d'un taux invente. Un montant fourni avec un taux doit
  correspondre exactement au calcul serveur, sinon la commande est refusee.
- Aucun taux de marge n'est configure au niveau du coffret ou de son type.
  Les anciens champs techniques de marge cible sont deprecies et sans effet.
- Le coffret affiche la somme des valeurs, reversements et marges de prestations.
  Son prix client reste explicite, saisi en euros. Si ce prix differe de la somme
  des valeurs, l'ecart commercial et le solde prix moins reversements sont
  affiches distinctement ; les marges ne s'additionnent pas a ce solde.
- Le prix doit toujours couvrir les reversements engages. Cette protection de
  budget reste independante de la commission de chaque prestation.
- Une modification de modele ne propage pas les conditions aux rattachements.
  Les instantanes des achats et droits vendus ne sont jamais recalcules.

Les montants s'affichent et se saisissent en euros sur ERP et OnBoard. Le taux
est obligatoire dans les nouveaux formulaires ; aucun taux commercial par defaut
n'est impose. Les champs calcules sont en lecture seule, avec erreurs explicites
sur taux hors borne, montant negatif, precision excessive ou depassement budget.

Deploiement : appliquer la nouvelle migration additive avant le backend et ses
assets. Aucune migration deja appliquee ni aucun historique financier ne doit
etre modifie. La recette doit verifier 0 %, 100 %, un taux decimal, l'arrondi,
les anciens enregistrements sans taux et la conservation des conditions vendues.
