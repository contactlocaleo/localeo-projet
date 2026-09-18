# SpÃ©cification fonctionnelle - Marketplace Localeo

## 1. Objet

Ce document dÃ©crit le comportement fonctionnel attendu de la version actuelle de la marketplace Localeo.

Il couvre :

- le parcours de dÃ©couverte par ville
- le parcours de consultation et d'achat d'un coffret
- le parcours post-paiement
- le parcours de consultation consommateur d'une instance de coffret
- le parcours professionnel d'achat multiple et d'activation

## 2. FinalitÃ© produit

La marketplace Localeo permet de vendre des coffrets digitaux liÃ©s Ã  une ville et Ã  des commerÃ§ants partenaires.

Le produit vendu n'est pas un bien physique. AprÃ¨s paiement, l'utilisateur reÃ§oit un accÃ¨s ou un lien digital permettant d'utiliser le coffret.

## 3. Acteurs

### 3.1 Visiteur

Utilisateur qui dÃ©couvre l'offre sans authentification.

### 3.2 Acheteur particulier

Utilisateur qui achÃ¨te un coffret pour lui-mÃªme ou pour l'offrir.

### 3.3 Acheteur professionnel

Utilisateur qui commande plusieurs exemplaires d'un mÃªme coffret pour une entreprise.

### 3.4 BÃ©nÃ©ficiaire

Personne qui reÃ§oit un lien d'activation ou un coffret activÃ© dans le cadre d'un achat professionnel.

### 3.5 Backend mÃ©tier

SystÃ¨me externe exposant les villes, coffrets, commerÃ§ants, achats, paiements, activations et QR codes.

## 4. Concepts mÃ©tier

### 4.1 Ville

Point d'entrÃ©e principal du catalogue.

Attributs utiles :

- identifiant
- nom
- code postal
- description Ã©ventuelle

### 4.2 CommerÃ§ant

Partenaire local associÃ© Ã  une ou plusieurs prestations.

Attributs utiles :

- identifiant
- nom
- description
- ville de rattachement
- contact email et tÃ©lÃ©phone
- image Ã©ventuelle

### 4.3 Prestation

ExpÃ©rience incluse dans un coffret.

Attributs utiles :

- identifiant
- libellÃ©
- description, dÃ©tails ou rÃ©sumÃ©
- commerÃ§ant associÃ©

### 4.4 Coffret

Produit commercial vendu sur la marketplace.

Attributs utiles :

- identifiant
- nom
- type de coffret
- prix
- durÃ©e de validitÃ©
- image
- liste de prestations
- ville associÃ©e

### 4.5 Achat

RÃ©sultat d'une transaction de paiement.

Attributs utiles :

- identifiant d'achat
- statut
- date de paiement
- type de client
- quantitÃ©
- rÃ©fÃ©rence transaction
- coffret achetÃ©

### 4.6 Coffret instance

Instance unitaire crÃ©Ã©e dans le cadre d'un achat professionnel.

Chaque coffret instance possÃ¨de son propre statut mÃ©tier.

## 5. Objectifs fonctionnels

La marketplace doit permettre :

1. d'entrer dans l'offre par la ville
2. d'explorer les coffrets disponibles localement
3. de comprendre clairement la valeur d'un coffret
4. de dÃ©clencher un paiement particulier ou professionnel
5. de restituer un statut post-paiement comprÃ©hensible
6. de gÃ©rer un achat pro coffret par coffret aprÃ¨s paiement

## 6. PÃ©rimÃ¨tre de cette version

### 6.1 Dans le pÃ©rimÃ¨tre

- recherche de ville avec suggestions
- consultation du catalogue d'une ville
- consultation du dÃ©tail d'un coffret
- consultation consommateur du dÃ©tail d'une instance de coffret
- consultation d'une page commerÃ§ant
- paiement particulier
- retour de paiement et confirmations
- commande professionnelle multi-coffrets
- gestion de coffrets pro aprÃ¨s achat
- activation d'un coffret par token
- consultation / impression d'un QR code

### 6.2 Hors pÃ©rimÃ¨tre

- crÃ©ation de compte utilisateur
- authentification front classique
- espace client personnel
- remboursement ou annulation depuis le front
- administration catalogue
- suivi dÃ©taillÃ© de consommation des prestations

## 7. Parcours utilisateurs

## 7.1 Recherche d'une ville

### DÃ©clenchement

L'utilisateur arrive sur `/search`.

### Comportement

1. L'utilisateur saisit au moins 2 caractÃ¨res.
2. Le systÃ¨me affiche les villes correspondantes.
3. L'utilisateur sÃ©lectionne une ville.
4. Le systÃ¨me navigue vers la liste des coffrets de cette ville.

### Ã‰lÃ©ments visibles

- champ de recherche
- suggestions
- message d'aide
- villes populaires si disponibles
- blocs de dÃ©couverte et mises en avant si les donnÃ©es existent

### RÃ©sultat attendu

L'utilisateur accÃ¨de Ã  un catalogue contextualisÃ© par ville.

## 7.2 Consultation du catalogue d'une ville

### DÃ©clenchement

L'utilisateur arrive sur `/coffrets` aprÃ¨s sÃ©lection d'une ville.

### Comportement

- affichage des coffrets disponibles pour la ville
- filtrage par type de coffret
- affichage d'un angle Ã©ditorial de lecture sur chaque coffret
- ouverture du dÃ©tail d'un coffret

### Cas particuliers

- si aucune ville n'est rÃ©solue, redirection vers la recherche
- si la ville n'a aucune offre, affichage d'un Ã©tat vide

### RÃ©sultat attendu

L'utilisateur peut comparer rapidement les coffrets d'une ville.

## 7.3 Consultation dÃ©taillÃ©e d'un coffret

### DÃ©clenchement

L'utilisateur arrive sur `/coffret`.

### Informations affichÃ©es

- nom du coffret
- type de coffret
- prix
- durÃ©e de validitÃ©
- nombre de prestations
- commerÃ§ants associÃ©s
- dÃ©tail des prestations
- caractÃ¨re digital du produit

### Actions possibles

- acheter le coffret en parcours particulier
- accÃ©der au parcours pro si activÃ©
- consulter une fiche commerÃ§ant

### RÃ©sultat attendu

L'utilisateur comprend ce qu'il achÃ¨te, comment il le recevra et auprÃ¨s de qui il pourra l'utiliser.

## 7.4 Consultation d'un commerÃ§ant

### DÃ©clenchement

L'utilisateur arrive sur `/commercant` depuis la home, le catalogue ou le dÃ©tail d'un coffret.

### Informations affichÃ©es

- identitÃ© du commerÃ§ant
- description
- coordonnÃ©es si disponibles
- ville
- coffrets associÃ©s Ã  ce commerÃ§ant

### RÃ©sultat attendu

L'utilisateur comprend le rÃ´le du commerÃ§ant dans l'offre Localeo et peut revenir vers les coffrets liÃ©s.

## 7.5 Achat particulier

### DÃ©clenchement

Depuis la page coffret, l'utilisateur remplit le formulaire d'achat standard.

### DonnÃ©es saisies

- email
- tÃ©lÃ©phone

### RÃ¨gles

- un email valide est requis
- un tÃ©lÃ©phone valide est requis
- le paiement standard doit Ãªtre activÃ© via feature flag

### RÃ©sultat attendu

Le frontend initialise un paiement et redirige vers le checkout retournÃ© par l'API.

## 7.6 Retour et confirmation de paiement particulier

### DÃ©clenchement

AprÃ¨s checkout, le backend renvoie vers `/retour-paiement`, puis vers :

- `/confirmation` en cas de succÃ¨s
- `/echec-paiement` en cas d'annulation, d'erreur ou d'attente

### Informations attendues

- statut
- rÃ©fÃ©rence d'achat
- type de client
- quantitÃ©
- email destinataire
- tÃ©lÃ©phone
- montant
- rÃ©fÃ©rence de paiement

### RÃ©sultat attendu

L'utilisateur comprend si son achat est confirmÃ© et quelles sont les prochaines Ã©tapes.

## 7.7 Commande professionnelle

### DÃ©clenchement

Depuis la page coffret, si l'option pro est active, l'utilisateur accÃ¨de Ã  `/commande-pro`.

### DonnÃ©es saisies

- nom de l'entreprise
- nom du contact
- email professionnel
- tÃ©lÃ©phone professionnel
- quantitÃ©
- usage prÃ©vu

### RÃ¨gles

- le parcours pro n'est disponible que si le paiement standard est actif et si le flag pro est actif
- un coffret doit dÃ©jÃ  Ãªtre sÃ©lectionnÃ©
- la quantitÃ© doit Ãªtre supÃ©rieure ou Ã©gale Ã  1
- le type client transmis au backend est `PROFESSIONNEL`

### RÃ©sultat attendu

Le checkout est initialisÃ© pour une commande multi-coffrets.

## 7.8 Consultation consommateur d'une instance de coffret

### DÃ©clenchement

L'utilisateur accÃ¨de Ã  `/coffret-instance` depuis un lien reÃ§u par email.

### ParamÃ¨tres attendus

- `achat_id`
- `coffret_instance_id`
- `consultation_token`

### Comportement

1. le frontend lit les paramÃ¨tres du lien
2. le `consultation_token` est transmis au backend en header `Authorization` au format `Bearer <token>`
3. le frontend charge le rÃ©capitulatif d'achat
4. le frontend charge le dÃ©tail du coffret instance
5. le frontend charge les prestations rattachÃ©es au coffret instance
6. le frontend enrichit l'affichage avec le dÃ©tail du coffret source quand `coffret_id` est disponible

### Informations affichÃ©es

- rÃ©fÃ©rence d'achat
- statut d'achat
- date d'achat
- montant et quantitÃ© si disponibles
- dÃ©tail du coffret source
- statut du coffret instance
- dates de crÃ©ation, activation et expiration
- email bÃ©nÃ©ficiaire si prÃ©sent
- liste des prestations du coffret instance

### RÃ©sultat attendu

Le consommateur peut consulter le contenu de son coffret Ã  partir d'un lien direct reÃ§u par email, sans espace client dÃ©diÃ©.

## 7.9 Confirmation de commande professionnelle

### DÃ©clenchement

AprÃ¨s paiement, `/retour-paiement` redirige vers `/confirmation-pro` si le type client rÃ©solu est professionnel.

### Informations affichÃ©es

- entreprise
- contact
- coffret achetÃ©
- validitÃ©
- quantitÃ©
- email destinataire
- tÃ©lÃ©phone
- rÃ©fÃ©rence commande
- rÃ©fÃ©rence paiement

### RÃ©sultat attendu

L'acheteur comprend que les coffrets sont crÃ©Ã©s et qu'ils pourront Ãªtre activÃ©s plus tard.

## 7.10 Gestion d'une commande professionnelle

### DÃ©clenchement

L'utilisateur accÃ¨de Ã  `/mes-coffrets-pro`.

### Informations affichÃ©es

- rÃ©capitulatif de commande
- progression d'activation
- liste des coffrets instances
- statut de chaque coffret instance
- date d'activation si disponible
- email bÃ©nÃ©ficiaire si disponible

### Actions possibles sur un coffret non activÃ©

- activer le coffret
- envoyer un lien d'activation

### RÃ©sultat attendu

L'acheteur professionnel gÃ¨re la distribution opÃ©rationnelle coffret par coffret.

## 7.11 Activation directe par token

### DÃ©clenchement

L'utilisateur accÃ¨de Ã  `/activer-coffret` avec ou sans token prÃ©rempli.

### Comportement

- saisie d'un code d'activation
- appel API d'activation
- redirection vers `/activation-confirmee`

### RÃ©sultat attendu

Le coffret est activÃ© et l'utilisateur obtient un retour simple sur l'opÃ©ration.

## 7.12 Consultation / impression de QR code

### DÃ©clenchement

L'utilisateur accÃ¨de Ã  `/qr-impression` avec un token de QR.

### Comportement

- chargement du dÃ©tail du QR via API
- affichage du SVG
- possibilitÃ© d'impression navigateur

### RÃ©sultat attendu

Le QR peut Ãªtre visualisÃ© et imprimÃ© dans un format exploitable.

## 8. RÃ¨gles de gestion

## 8.1 Recherche de ville

- la recherche est activÃ©e Ã  partir de 2 caractÃ¨res
- sans ville rÃ©solue, les pages catalogue ou produit redirigent vers la recherche

## 8.2 Coffrets et contenu

- un coffret est toujours liÃ© Ã  une ville
- un coffret peut contenir zÃ©ro, une ou plusieurs prestations
- les prestations peuvent Ãªtre enrichies avec leur commerÃ§ant
- le coffret est toujours prÃ©sentÃ© comme un produit digital

## 8.3 Paiement

- l'initialisation du paiement dÃ©pend de la prÃ©sence d'une `checkout_url`
- sans `checkout_url`, le paiement est considÃ©rÃ© en erreur
- le front ne finalise jamais lui-mÃªme une transaction, il s'appuie sur le backend

## 8.4 Parcours pro

- le parcours pro dÃ©pend de `LOCALEO_FEATURE_PAYMENT_ENABLED` et `LOCALEO_FEATURE_PRO_ORDERS_ENABLED`
- un achat pro peut produire plusieurs coffrets instances
- un coffret activÃ© ne doit plus proposer l'action principale d'activation

## 8.5 Images

- si une image mÃ©tier est fournie, elle doit Ãªtre utilisÃ©e en prioritÃ©
- sinon un visuel de fallback est utilisÃ©

## 8.6 Post-paiement

- la page de retour de paiement est une page technique de rÃ©solution et de redirection
- la page finale de succÃ¨s ou d'Ã©chec doit Ãªtre explicite et autonome
- la page consommateur `/coffret-instance` est une page de consultation directe depuis email
- le lien d'accÃ¨s consommateur dÃ©pend de la prÃ©sence d'un `consultation_token`

## 9. Exigences d'interface

## 9.1 ClartÃ© produit

L'interface doit rappeler qu'il s'agit d'un produit digital sans livraison physique.

## 9.2 ComprÃ©hension rapide

L'utilisateur doit pouvoir comprendre :

- ce qu'est un coffret
- ce qu'il contient
- Ã  quel commerÃ§ant ou Ã  quelle ville il se rattache

## 9.3 ProgressivitÃ©

Le parcours doit rester court :

1. ville
2. coffret
3. paiement

## 9.4 RÃ©assurance

Les pages d'achat et de confirmation doivent expliciter la suite du parcours.

## 10. HypothÃ¨ses structurantes

- la ville est l'entrÃ©e primaire du catalogue
- le front fonctionne sans authentification standard
- l'API constitue la source de vÃ©ritÃ© mÃ©tier
- le parcours pro repose sur la granularitÃ© `achat -> coffrets instances`
- le parcours consommateur de consultation repose sur un lien signÃ© ou tokenisÃ© envoyÃ© par email

## 11. Risques fonctionnels

- confusion possible entre coffret, prestation et commerÃ§ant
- densitÃ© d'offre faible dans certaines villes
- dÃ©pendance forte Ã  la qualitÃ© des rÃ©ponses API
- risque d'incomprÃ©hension si les statuts backend sont trop bruts

## 12. Indicateurs mÃ©tier suggÃ©rÃ©s

- taux de transformation recherche ville -> catalogue
- taux de transformation catalogue -> dÃ©tail coffret
- taux de transformation dÃ©tail coffret -> checkout
- taux de conversion paiement particulier
- taux de conversion paiement professionnel
- taux d'activation des coffrets pro
- taux d'envoi de liens d'activation

## 13. SynthÃ¨se

La version actuelle de la marketplace Localeo repose sur un parcours principal simple :

1. choisir une ville
2. consulter les coffrets
3. acheter un coffret digital
4. consulter son instance de coffret via lien email ou gÃ©rer les activations dans le cas pro

Le parcours professionnel Ã©tend ce modÃ¨le avec une gestion unitaire des coffrets crÃ©Ã©s aprÃ¨s achat.



## Correctifs de securite du 6 septembre 2026

Voir le [contrat des correctifs MARKET](../../specifications/securisation-production/corrections-marketplace-2026-09-06.md), qui complete les parcours et les regles de livraison.
