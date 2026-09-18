# Backlog Epic 29 - Jeu de donnees de test pour recette

## Synthese

- Criticite : `Moyenne`
- Statut : `Termine`
- Objectif : disposer d'une commune de test, d'un commercant de test et de coffrets de test afin de pouvoir verifier les parcours principaux sans melanger ces donnees avec le catalogue reel.
- Decision produit : ne pas creer de mode test production complexe. Le besoin est couvert par un petit jeu de donnees explicitement identifie comme test.
- Decision technique : ajouter un marqueur simple sur les entites racines utiles a la recette, puis exclure ces donnees des surfaces publiques et indicateurs reels par defaut.
- Decision operationnelle : les donnees de test peuvent rester en base tant qu'elles sont clairement visibles comme test et non exposees au public.

## Probleme

Les tests automatises couvrent le domaine et l'application, mais il reste utile de pouvoir verifier manuellement certains parcours avec des donnees stables : consultation catalogue, achat, activation, validation prestation, contact support et back-office.

Le dispositif initial de tests controles en production etait trop complexe. Une approche plus simple consiste a maintenir un referentiel de test limite et identifiable : une commune de test, un commercant de test, des prestations de test et quelques coffrets de test.

## Perimetre MVP

- Ajouter un marqueur `is_test` ou equivalent sur les entites racines ciblees.
- Creer une commune de test.
- Creer un commercant de test rattache a cette commune.
- Creer un ou plusieurs coffrets de test rattaches a cette commune.
- Creer des prestations de test rattachees au commercant de test.
- Afficher clairement le statut test en back-office.
- Exclure les donnees de test du catalogue public par defaut.
- Exclure les donnees de test des KPIs et reversements reels par defaut.
- Documenter comment utiliser ce jeu de donnees pour une recette manuelle.

## Hors perimetre MVP

- Creer un mode test global en production.
- Automatiser tous les parcours de recette.
- Ajouter une notion de campagne de recette.
- Construire une supervision dediee des tests production.
- Simuler tous les providers externes.
- Nettoyer automatiquement des graphes complexes de donnees.
- Autoriser les tests sur des donnees client ou commercant reelles.

## User Stories

1. `PRD-197` En tant qu'operateur Localeo, je veux identifier une commune comme donnee de test afin de l'utiliser pour la recette sans la confondre avec une commune reelle.
   - Statut : `Termine`
   - Resultat attendu : une commune peut etre marquee test.
   - Resultat attendu : le marquage test est visible en back-office.

2. `PRD-198` En tant qu'operateur Localeo, je veux identifier un commercant comme commercant de test afin de rejouer les parcours sans impacter un partenaire reel.
   - Statut : `Termine`
   - Resultat attendu : un commercant peut etre marque test.
   - Resultat attendu : un commercant de test est rattache a une commune de test.

3. `PRD-199` En tant qu'operateur Localeo, je veux identifier un coffret comme coffret de test afin de pouvoir tester le parcours achat et activation.
   - Statut : `Termine`
   - Resultat attendu : un coffret peut etre marque test.
   - Resultat attendu : un coffret de test est rattache a une commune de test.

4. `PRD-200` En tant qu'operateur Localeo, je veux rattacher uniquement des prestations de test aux coffrets de test afin d'eviter tout melange avec le catalogue reel.
   - Statut : `Termine`
   - Resultat attendu : une prestation utilisee dans un coffret de test appartient a un commercant de test.
   - Resultat attendu : le back-office signale ou refuse les associations mixtes test/reel.

5. `PRD-201` En tant que responsable produit, je veux exclure les donnees de test du catalogue public afin de ne pas les exposer aux visiteurs.
   - Statut : `Termine`
   - Resultat attendu : communes, commercants, coffrets et prestations de test ne sont pas retournes par les endpoints publics par defaut.
   - Resultat attendu : une preview protegee peut les afficher si necessaire.

6. `PRD-202` En tant qu'exploitant, je veux exclure les donnees de test des KPIs reels afin de ne pas fausser les tableaux de bord.
   - Statut : `Termine`
   - Resultat attendu : achats, validations, activites, feedbacks et reversements lies aux donnees test sont exclus des indicateurs business par defaut.

7. `PRD-203` En tant que finance, je veux que les validations issues d'un coffret de test ne produisent pas de reversement payable afin de proteger les exports financiers.
   - Statut : `Termine`
   - Resultat attendu : les mouvements issus de donnees test sont marques test ou exclus des lots de paiement.

8. `PRD-204` En tant qu'operateur back-office, je veux generer ou retrouver rapidement le jeu de donnees de test afin de ne pas le reconstruire manuellement.
   - Statut : `Termine`
   - Resultat attendu : un script seed ou une action back-office cree les donnees manquantes de facon idempotente.

9. `PRD-205` En tant que testeur, je veux une fiche de recette indiquant quels parcours tester avec le commercant et les coffrets de test.
   - Statut : `Termine`
   - Resultat attendu : la documentation liste les parcours achat, activation, validation prestation, support et back-office.

10. `PRD-206` En tant que responsable securite, je veux eviter que les donnees de test envoient des communications a de vrais clients.
    - Statut : `Termine`
    - Resultat attendu : les emails et SMS generes depuis les parcours de test utilisent des destinataires explicitement controles.

## Regles de gestion

- Une commune de test est marquee explicitement.
- Un commercant de test est marque explicitement.
- Un coffret de test est marque explicitement.
- Une prestation de test appartient a un commercant de test.
- Un coffret de test ne doit pas contenir une prestation d'un commercant reel.
- Un coffret reel ne doit pas contenir une prestation de test.
- Les donnees de test ne sont pas exposees publiquement par defaut.
- Les donnees de test ne sont pas incluses dans les KPIs reels par defaut.
- Les donnees de test ne sont pas incluses dans les reversements payables.
- Les communications sortantes liees aux donnees de test doivent utiliser des destinataires controles.

## Modele de donnees cible

Option recommandee MVP :

- Ajouter `is_test BOOLEAN NOT NULL DEFAULT FALSE` sur `villes`.
- Ajouter `is_test BOOLEAN NOT NULL DEFAULT FALSE` sur `commercants`.
- Ajouter `is_test BOOLEAN NOT NULL DEFAULT FALSE` sur `coffrets`.
- Ajouter `is_test BOOLEAN NOT NULL DEFAULT FALSE` sur `prestations_coffret` si le filtrage par prestation devient necessaire.

Propagation fonctionnelle :

- Un achat d'un coffret test est considere comme achat test.
- Une coffret instance issue d'un achat test est consideree comme instance test.
- Une validation issue d'une instance test est consideree comme validation test.
- Un mouvement de reversement issu d'une validation test est considere comme mouvement test ou non payable.

## Parcours de recette cibles

| Parcours | Donnees utilisees | Controle attendu |
|---|---|---|
| Catalogue back-office | Commune, commercant, coffret test | Marquage visible |
| Achat test | Coffret test | Achat identifiable comme test |
| Activation test | Instance issue du coffret test | Token et consultation fonctionnels |
| Validation prestation test | Commercant et prestation test | Pas de reversement payable |
| Contact support test | Achat ou instance test | Timeline identifiable |
| Documents test | Achat test | Document non comptabilise comme reel |

## Lots de realisation

### Lot 1 - Marquage minimal

- Ajouter les champs `is_test`.
- Les afficher en back-office.
- Ajouter les filtres publics d'exclusion.

### Lot 2 - Seed du jeu de test

- Creer un script ou une action idempotente.
- Generer commune, commercant, prestations et coffrets de test.
- Documenter les identifiants ou labels de reference.

### Lot 3 - Exclusions metier

- Exclure test des KPIs publics et operationnels reels.
- Exclure test des reversements payables.
- Marquer les achats et validations derives comme test.

### Lot 4 - Documentation recette

- Ajouter une fiche de recette manuelle.
- Lister les parcours a verifier.
- Preciser les precautions email, SMS et paiement.

## Tests attendus

- Une commune test n'apparait pas dans les endpoints publics par defaut.
- Un commercant test n'apparait pas dans les endpoints publics par defaut.
- Un coffret test n'apparait pas dans les endpoints publics par defaut.
- Un coffret test ne peut pas contenir une prestation de commercant reel.
- Un coffret reel ne peut pas contenir une prestation de test.
- Un achat de coffret test est identifiable comme test.
- Une validation de prestation test ne genere pas de reversement payable.
- Le seed du jeu de test est idempotent.

## Criteres d'acceptation MVP

- Une commune de test existe ou peut etre creee par seed.
- Un commercant de test existe ou peut etre cree par seed.
- Au moins un coffret de test existe ou peut etre cree par seed.
- Le back-office permet d'identifier clairement ces donnees comme test.
- Les endpoints publics excluent les donnees de test par defaut.
- Les KPIs et reversements reels excluent les donnees de test.
- Une documentation de recette indique comment utiliser ces donnees.

## Decisions a prendre avant implementation

- Nom exact du marqueur : `is_test`, `usage`, `mode_recette`.
- Tables exactes qui portent le marqueur en dur.
- Strategie pour les donnees derivees : champ persiste ou inference depuis le coffret/achat.
- Comportement des emails/SMS sur les parcours de test.
- Possibilite ou non d'utiliser Stripe test en environnement de production.
