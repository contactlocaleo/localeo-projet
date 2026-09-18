# Backlog Epic 28 - Calcul reversement coffret backoffice

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : faciliter le calcul du montant de reversement lors de la construction d'un coffret, en tenant compte du prix du coffret, du taux de marge configure et des reversements deja affectes aux prestations existantes.
- Decision produit : l'aide au calcul est une fonctionnalite back-office rattachee a la creation ou modification d'une prestation de coffret.
- Decision produit : l'operateur ne doit pas pouvoir saisir un montant de reversement superieur au montant disponible sur le coffret.
- Decision produit : l'operateur peut explicitement degrader la marge du coffret en saisissant un reversement superieur au montant disponible, mais jamais au-dela du montant restant avant d'atteindre le prix total du coffret.
- Decision produit : le total des reversements configures sur un coffret ne doit jamais etre superieur au prix du coffret.
- Decision produit : une vue 360 coffret doit completer le dispositif pour piloter la performance de chaque coffret, sa marge et ses reversements rattaches.
- Decision technique : la source de verite du plafond est calculee a partir du coffret et des prestations rattachees, pas saisie manuellement.
- Decision technique : le taux de marge applicable est celui configure sur le `type_coffret.marge_minimum_pourcent`.
- Decision produit : le calcul prend en compte toutes les prestations rattachees au coffret, sauf les prestations suspendues ou archivees.
- Decision produit : le montant de reversement d'une prestation suspendue ou archivee ne reserve pas de disponible.
- Decision UX : la confirmation de degradation de marge se fait par checkbox explicite.
- Decision audit : toute degradation de marge doit etre historisee dans l'audit avec l'ancien et le nouveau niveau de marge theorique.
- Decision produit : la page d'aide peut proposer des suggestions simples de repartition du reversement disponible.
- Decision produit : un avertissement specifique doit etre affiche quand des prestations suspendues ou archivees existent mais sont exclues du calcul.
- Decision planning : la vue 360 coffret est livree dans le meme lot MVP que l'assistant de calcul.
- Decision UX : depuis la page de creation de prestation, un lien proche du champ `montant_reversement` ouvre la page de calcul si un coffret est deja selectionne.

## Probleme

Lorsqu'un operateur construit un coffret, il doit definir le montant reverse a chaque commercant pour chaque prestation. Aujourd'hui, ce montant est saisi manuellement, alors qu'il depend :

- du prix du coffret ;
- du taux de marge minimum attendu sur le type de coffret ou la configuration de marge du coffret ;
- des montants de reversement deja affectes aux autres prestations du coffret ;
- de la capacite restante avant de degrader la marge attendue.

Sans aide explicite, l'operateur peut sous-utiliser le budget disponible ou saisir un reversement trop eleve, ce qui degrade la marge du coffret et cree des corrections manuelles.

## Risque business

- Marge Localeo degradee par erreur de saisie.
- Construction de coffrets plus lente et dependante de calculs manuels.
- Incoherence entre prix public, taux de marge attendu et sommes reversees aux commercants.
- Difficultes a piloter la rentabilite d'un coffret une fois plusieurs prestations rattachees.

## Risque technique

- Duplication des regles de calcul entre validation de formulaire, page d'aide et dashboard.
- Ambiguite sur la source du taux de marge applicable.
- Risque de course si deux prestations du meme coffret sont modifiees simultanement.
- Incoherence si une prestation en edition est incluse deux fois dans le calcul du disponible.

## Perimetre MVP

- Ajouter une page back-office d'aide au calcul du reversement pour un coffret donne.
- Depuis la creation ou modification d'une prestation coffret, afficher un lien a cote du champ `montant_reversement` quand un coffret est selectionne.
- La page de calcul affiche :
  - prix du coffret ;
  - taux de marge applicable ;
  - montant maximum reversement total autorise ;
  - total des reversements deja configures sur les prestations du coffret ;
  - montant de reversement encore disponible ;
  - liste des prestations deja presentes avec montant de reversement, statut et commercant.
- Permettre a l'operateur de saisir ou reprendre le montant disponible propose.
- Bloquer toute validation si le montant saisi est superieur au plafond absolu restant avant depassement du prix du coffret.
- Permettre une validation explicite si le montant saisi depasse le disponible de marge mais reste inferieur ou egal au plafond absolu.
- Afficher clairement l'impact de degradation de marge quand le montant depasse le disponible cible.
- Au clic sur `Valider le montant du reversement`, revenir sur le formulaire prestation avec `montant_reversement` pre-rempli.
- Exclure du total la prestation en cours d'edition quand un `prestation_coffret_id` est transmis.
- Ajouter une vue 360 coffret back-office en lecture seule.
- La vue 360 coffret affiche :
  - prix public ;
  - taux de marge applicable ;
  - marge attendue ;
  - total reversements configures ;
  - reversement disponible ;
  - marge theorique restante ;
  - prestations rattachees ;
  - achats, validations et indicateurs de performance si disponibles.

## Hors perimetre MVP

- Optimisation automatique de la repartition entre commercants.
- Validation juridique ou comptable avancee du modele de marge.
- Gestion de plusieurs scenarios de prix pour un meme coffret.
- Simulation multi-coffrets.
- Export financier detaille.
- Modification en masse des reversements depuis la vue 360 coffret.
- Workflow d'approbation d'un coffret non rentable.

## Regles de calcul MVP

- `budget_reversement_total = prix_coffret * (1 - taux_marge_applicable / 100)`.
- `reversements_deja_configures = somme(montant_reversement des prestations du coffret hors prestations suspendues ou archivees)`.
- Si une prestation est en cours d'edition, son montant existant est exclu du total pour calculer le disponible modifiable.
- `reversement_disponible = budget_reversement_total - reversements_deja_configures`.
- `plafond_absolu_restant = prix_coffret - reversements_deja_configures`.
- Le montant saisi pour la prestation courante peut depasser `reversement_disponible` uniquement si l'operateur confirme explicitement la degradation de marge.
- Le montant saisi pour la prestation courante doit toujours etre inferieur ou egal a `plafond_absolu_restant`.
- Le total des reversements configures sur un coffret ne doit jamais depasser `prix_coffret`.
- Si `reversement_disponible` est negatif, toute nouvelle saisie degrade deja la marge et doit etre confirmee explicitement.
- Le taux de marge applicable doit etre lu depuis `type_coffret.marge_minimum_pourcent`.
- Une degradation de marge est confirmee via une checkbox explicite.
- Une degradation de marge doit creer un evenement d'audit contenant le taux de marge cible, la marge theorique avant saisie, la marge theorique apres saisie et l'ecart.
- Les montants doivent etre affiches en EUR, avec deux decimales.

## User Stories

1. `PRD-186` En tant qu'operateur back-office, je veux acceder a un assistant de calcul depuis le champ de reversement d'une prestation afin de ne pas calculer manuellement le montant disponible.
   - Statut : `Termine`
   - Resultat attendu : un lien est visible a cote du champ `montant_reversement` quand un coffret est selectionne.
   - Resultat attendu : si aucun coffret n'est selectionne, le lien est absent ou desactive avec un message clair.

2. `PRD-187` En tant qu'operateur back-office, je veux voir le reversement disponible d'un coffret afin de choisir un montant compatible avec la marge attendue.
   - Statut : `Termine`
   - Resultat attendu : la page affiche prix du coffret, taux de marge, budget total de reversement, total deja affecte et disponible restant.
   - Resultat attendu : les prestations deja rattachees au coffret sont listees avec leur montant de reversement.

3. `PRD-188` En tant qu'operateur back-office, je veux que la prestation en cours d'edition soit exclue du total deja affecte afin de pouvoir modifier son montant sans double comptage.
   - Statut : `Termine`
   - Resultat attendu : la page accepte un identifiant de prestation courante optionnel.
   - Resultat attendu : le calcul du disponible exclut cette prestation du total existant.

4. `PRD-189` En tant que responsable financier, je veux interdire un total de reversements superieur au prix du coffret afin d'eviter une incoherence economique impossible.
   - Statut : `Termine`
   - Resultat attendu : la validation de la prestation refuse tout montant qui ferait depasser le prix total du coffret par la somme des reversements.
   - Resultat attendu : le message d'erreur affiche le plafond absolu autorise.

5. `PRD-190` En tant qu'operateur back-office, je veux valider le montant calcule afin de revenir au formulaire prestation avec le champ pre-rempli.
   - Statut : `Termine`
   - Resultat attendu : le bouton `Valider le montant du reversement` redirige vers le formulaire de creation ou edition de prestation.
   - Resultat attendu : le champ `montant_reversement` est pre-rempli avec le montant choisi.

6. `PRD-191` En tant qu'operateur back-office, je veux modifier le montant propose avant validation afin de choisir un reversement inferieur au disponible.
   - Statut : `Termine`
   - Resultat attendu : la page propose par defaut le montant disponible.
   - Resultat attendu : un montant inferieur ou egal au disponible est accepte.

7. `PRD-196` En tant que responsable produit, je veux pouvoir degrader explicitement la marge d'un coffret afin d'accepter ponctuellement un reversement superieur au disponible cible.
   - Statut : `Termine`
   - Resultat attendu : un montant superieur au reversement disponible cible est accepte uniquement apres confirmation explicite.
   - Resultat attendu : la confirmation se fait via une checkbox explicite.
   - Resultat attendu : l'ecran affiche la marge cible, la marge degradee et l'ecart genere par la saisie.
   - Resultat attendu : l'audit conserve l'ancien et le nouveau niveau de marge theorique.

8. `PRD-192` En tant que responsable produit, je veux une vue 360 coffret afin de piloter la performance et la rentabilite de chaque coffret.
   - Statut : `Termine`
   - Resultat attendu : une entree back-office `Vision 360 coffret` permet de rechercher et ouvrir un coffret.
   - Resultat attendu : la vue affiche prix, taux de marge, total reversements, disponible restant et marge theorique.
   - Resultat attendu : la vue 360 coffret est livree dans le meme lot MVP que l'assistant de calcul.

9. `PRD-193` En tant qu'operateur back-office, je veux voir les prestations et commercants rattaches dans la vue 360 coffret afin de comprendre la composition du coffret.
   - Statut : `Termine`
   - Resultat attendu : chaque prestation affiche statut, commercant, montant de reversement et lien vers sa fiche.
   - Resultat attendu : les prestations sont limitees et ordonnees de facon lisible.

10. `PRD-194` En tant que responsable exploitation, je veux voir les achats et validations du coffret afin de mesurer sa performance commerciale et terrain.
   - Statut : `Termine`
   - Resultat attendu : la vue 360 coffret affiche les achats recents, validations recentes, taux d'utilisation si calculable et liens vers les objets back-office.

11. `PRD-195` En tant que responsable financier, je veux identifier les coffrets a risque de marge afin de prioriser les corrections.
    - Statut : `Termine`
    - Resultat attendu : la vue signale les coffrets dont le reversement configure depasse le budget autorise.
    - Resultat attendu : la vue signale les coffrets avec disponible negatif ou marge theorique insuffisante.

## Points a arbitrer

- Aucun point en suspens identifie a ce stade.

## Criteres de recette MVP

- Pour un coffret a 100 EUR avec marge 30 %, le budget total de reversement affiche est 70 EUR.
- Si deux prestations existantes ont 20 EUR et 15 EUR de reversement, le disponible affiche est 35 EUR.
- Si l'operateur saisit 40 EUR dans ce contexte, la validation est acceptee uniquement avec confirmation explicite de degradation de marge.
- Si l'operateur valide 35 EUR depuis l'assistant, le formulaire prestation se rouvre avec `montant_reversement = 35.00`.
- Si une prestation existante a deja 15 EUR et est editee, ces 15 EUR sont exclus du total pour calculer son nouveau disponible.
- Si le prix du coffret est 100 EUR et que 80 EUR sont deja configures, le plafond absolu restant est 20 EUR.
- Si l'operateur saisit 25 EUR avec deja 80 EUR configures sur un coffret a 100 EUR, la validation est refusee meme avec confirmation de degradation de marge.
- La vue 360 coffret permet d'identifier rapidement un coffret dont le disponible est negatif.
