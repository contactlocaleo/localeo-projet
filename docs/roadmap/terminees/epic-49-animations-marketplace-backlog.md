# Backlog Epic 49 - Visibilite des animations dans la marketplace

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : rendre les animations Localeo publiques visibles dans la marketplace, sans exposer une animation rattachee a une commune dont l'abonnement Animation n'est plus actif.
- Epic source : `Epic 49. Visibilite des animations dans la marketplace`
- Dependances : Epic 41 `Animation locale`, Epic 42 `Localeo Live`, Epic 16 `Feed d'activite locale` et Epic 33 `Recherche multi-scope`.
- Surfaces ciblees : accueil marketplace, page commune, page commercant, page coffret, catalogue public des animations et fiche publique existante.

## Vision produit recommandee

La page commune doit etre le point d'entree principal : une animation est d'abord un rendez-vous local. L'accueil doit donner une preuve de vitalite a l'echelle du territoire et conduire vers un catalogue filtrable par commune. Les pages commercant et coffret ne doivent afficher une animation que lorsqu'un lien metier reel existe avec l'objet consulte.

La marketplace ne doit donc pas dupliquer partout un catalogue generique :

- `Commune` : decouverte des animations publiques de cette commune ;
- `Accueil` : synthese territoriale, nombre d'animations et communes concernees ;
- `Commercant` : animations auxquelles ce commercant participe effectivement ;
- `Coffret` : animations dans lesquelles ce coffret intervient reellement, par exemple comme lot ou gain ;
- `Catalogue /animations` : vue exhaustive et partageable, avec filtre par commune ;
- `Fiche /animations/{animation_id}` : detail public et inscription, deja amorces par les contrats existants.

Cette hierarchie preserve la fonction premiere de la marketplace, la decouverte et l'achat de coffrets, tout en rendant la vie locale nettement plus visible.

## Regle de visibilite structurante

L'eligibilite doit etre calculee par le backend et reutilisee par toutes les surfaces. Le frontend ne doit jamais tenter de reconstruire le statut de l'abonnement communal.

Une animation peut etre exposee publiquement uniquement si toutes les conditions suivantes sont remplies :

1. la commune, portee par l'unique referentiel historique `villes`, est publiee dans le referentiel public ;
2. l'abonnement Animation du couple `(partenaire_id, commune_id)` est dans sa periode de validite et de statut strictement `ACTIF` ;
3. l'animation est publiee dans un statut public autorise ;
4. sa periode de visibilite n'est pas terminee ;
5. elle n'est ni annulee, ni archivee, ni masquee ;
6. les rattachements commercant et coffret exposes sont des liens metier reels, pas une simple eligibilite potentielle.

La desactivation de l'abonnement communal doit retirer les animations de toutes les projections publiques apres expiration du cache, meme si une animation etait encore marquee comme publiee.

## Strategie de contenu par surface

| Surface | Information affichee | Forme recommandee | Condition supplementaire | Position recommandee |
| --- | --- | --- | --- | --- |
| Accueil | Total a decouvrir, total en cours, nombre de communes concernees et premiers territoires actifs | Bande editoriale territoriale, un chiffre dominant et une liste courte de communes, sans mosaique de cartes | Au moins une animation publique eligible sur le territoire | Apres l'exploration des communes et avant le feed d'activite locale |
| Commune | Une animation mise en avant puis une liste chronologique compacte | Visuel officiel si disponible, date, statut, titre, resume et CTA | Au moins une animation publique eligible dans la commune | Apres le coffret recommande et avant le catalogue complet des coffrets |
| Commercant | Animation(s) auxquelles le commercant participe | Bloc contextuel compact `Ce commerce participe` | `commercant_id` present dans la configuration publiee de l'animation | Apres l'histoire du commercant et avant ses coffrets |
| Coffret | Animation(s) utilisant reellement le coffret | Bloc contextuel `Ce coffret est a gagner dans...` ou libelle adapte au lien | Coffret rattache comme lot, gain ou ressource effective de l'animation | Apres les experiences et adresses, avant l'activite locale |
| Catalogue | Toutes les animations eligibles, regroupables par commune | En-tete sobre, filtres commune/statut et liste datee | Route publique disponible meme sans commune preselectionnee | Nouvelle route `/animations` |
| Detail | Informations, dates, regles, partenaires et inscription | Vue publique existante mutualisee avec Localeo Live lorsque possible | Animation publique eligible | Route `/animations/{animation_id}` |

## Direction UX/UI

### These visuelle

Traiter les animations comme un agenda local vivant : rythme editorial, dates tres lisibles, typographie forte et visuels officiels, avec la couleur Localeo comme signal d'action.

### Plan de contenu

1. orientation : `Animations Localeo` et periode concernee ;
2. preuve : compteurs exacts et communes actives ;
3. decouverte : animation mise en avant puis liste chronologique ;
4. action : consulter le detail, s'inscrire ou explorer une commune.

### These d'interaction

- apparition sobre de la ligne temporelle et des animations au chargement ;
- changement de commune avec mise a jour en place de la liste et annonce accessible du nombre de resultats ;
- transition legere entre catalogue et fiche detaillee, sans carrousel automatique.

### Regles de presentation

- ne jamais utiliser une vignette generique de coffret ou de commercant pour illustrer une animation ;
- utiliser le visuel ou flyer officiel lorsqu'il existe ;
- sans visuel officiel, afficher un bloc typographique fonde sur la date et le nom, pas une image sans rapport ;
- privilegier une animation mise en avant et une liste, plutot qu'une grille de cartes identiques ;
- afficher clairement `Inscriptions ouvertes`, `En cours` ou `Bientot` ;
- ne pas afficher de bloc vide sur les pages d'accueil, commune, commercant ou coffret ;
- reserver l'etat vide explicatif a la route dediee `/animations` ;
- conserver des cibles tactiles d'au moins 44 px et un ordre de lecture clavier coherent.

## Proposition pour l'accueil

Le compteur global est pertinent s'il raconte une activite reelle et permet immediatement d'aller plus loin. La formulation doit distinguer les animations reellement en cours de celles dont les inscriptions sont ouvertes.

Exemple de contenu :

> 12 animations Localeo a decouvrir
>
> 4 en cours · 8 inscriptions ouvertes · 6 communes
>
> Saint-Loubes 3 · Libourne 2 · Bordeaux 2 · Voir toutes les communes

Le CTA `Voir les animations` ouvre `/animations`. Le detail par commune reste une vraie page filtrable et partageable, plutot qu'une modale depuis l'accueil. Une carte geographique n'est pas recommandee en V1 : une liste de communes est plus accessible, plus rapide et plus efficace tant que la densite territoriale reste moderee.

## Routes frontend ciblees

- `GET /animations` : catalogue territorial public ;
- `GET /animations?commune_id={commune_id}` : catalogue filtre et partageable ;
- `GET /animations/{animation_id}` : detail public existant a conserver ;
- `GET /animations/participants/{token}` : QR et detail participant existants, hors indexation.

La route catalogue doit permettre de revenir simplement vers la commune d'origine ou vers l'accueil. La fiche detaillee doit conserver le contexte de navigation sans rendre Localeo Live obligatoire.

## Contrats backend a prevoir

### Extension de la liste publique

Etendre `GET /public/animation-locale/animations` sans casser les consommateurs actuels :

- filtres optionnels `commune_id`, `commercant_id` et `coffret_id` ;
- pagination ou limite bornee ;
- tri public stable par statut puis date de debut ;
- application systematique de la regle d'eligibilite communale ;
- projection publique sans donnees de participant, abonnement commercial ou configuration interne.

### Synthese territoriale

Ajouter `GET /public/animation-locale/animations/synthese`, declare avant la route dynamique `/{animation_id}` :

- `total_a_decouvrir` ;
- `total_en_cours` ;
- `total_inscriptions_ouvertes` ;
- `total_communes` ;
- `programme_actif` lorsqu'une commune est filtree ;
- `communes[]` avec `id`, `nom`, `code_postal`, `nombre_animations`, `nombre_en_cours` et `prochaine_date` ;
- filtres optionnels `commune_id`, `commercant_id` et `coffret_id` ;
- cache public court avec invalidation lors d'une publication, annulation ou desactivation d'abonnement.

Les compteurs de la synthese et les elements de la liste doivent utiliser strictement le meme predicat d'eligibilite.

## User Stories

### `PRD-439` Eligibilite publique centralisee des animations

- Priorite : `P0`
- Statut : `A faire`
- En tant que responsable produit, je veux que seules les animations de communes disposant d'un abonnement Animation actif soient exposees afin de respecter le perimetre contractuel.
- Le predicat est applique par le backend a la liste, au detail, aux syntheses et aux rattachements contextuels.
- Une desactivation d'abonnement retire l'animation de toutes les surfaces publiques.
- Aucun detail commercial de l'abonnement n'est expose publiquement.

### `PRD-440` Catalogue public territorial des animations

- Priorite : `P0`
- Statut : `A faire`
- En tant que visiteur, je veux consulter les animations Localeo en cours ou a venir afin de choisir un rendez-vous local.
- La route `/animations` permet de filtrer par commune et statut public.
- Chaque ligne affiche date, commune, titre, statut et acces au detail.
- La route est partageable, responsive et utilisable sans charger Localeo Live.

### `PRD-441` Animations sur la page commune

- Priorite : `P0`
- Statut : `A faire`
- En tant que visiteur d'une commune, je veux voir ses animations actives afin de comprendre ce qui s'y passe actuellement.
- Le bloc est absent si aucune animation publique eligible n'est disponible.
- Une animation est mise en avant, les suivantes sont affichees sous forme de liste chronologique.
- Le CTA secondaire ouvre `/animations?commune_id={commune_id}`.

### `PRD-442` Animations liees sur la page commercant

- Priorite : `P1`
- Statut : `A faire`
- En tant que visiteur d'un commercant, je veux voir les animations auxquelles il participe afin de pouvoir le rencontrer dans ce contexte.
- Le bloc ne montre que les animations contenant effectivement ce commercant.
- Une animation de la meme commune sans ce commercant ne doit pas etre affichee sur sa fiche.
- Le CTA ouvre le detail public de l'animation.

### `PRD-443` Animations liees sur la page coffret

- Priorite : `P1`
- Statut : `A faire`
- En tant que visiteur d'un coffret, je veux savoir s'il intervient dans une animation afin de comprendre ce lien et consulter l'animation.
- Le bloc ne montre que les animations utilisant effectivement ce coffret comme lot, gain ou ressource configuree.
- Le simple fait qu'un coffret soit eligible pour une animation ne suffit pas a l'afficher.
- Le libelle precise la nature du lien lorsqu'elle est publique.

### `PRD-444` Synthese territoriale sur l'accueil

- Priorite : `P1`
- Statut : `A faire`
- En tant que visiteur, je veux connaitre le nombre d'animations Localeo actives sur le territoire afin de percevoir la dynamique du reseau.
- La synthese distingue `en cours` et `inscriptions ouvertes`.
- Elle permet d'acceder au catalogue et aux animations d'une commune.
- Elle est entierement absente lorsque le total public eligible vaut zero.

### `PRD-445` Contrats publics de liste et de synthese

- Priorite : `P0`
- Statut : `A faire`
- En tant qu'application marketplace, je veux obtenir listes, compteurs et regroupements depuis des contrats publics coherents afin d'eviter le surchargement et les divergences de calcul.
- Le backend fournit les filtres commune, commercant et coffret sans requetes N+1.
- Les resultats sont pagines et les syntheses disposent d'un cache public court.
- Le contrat OpenAPI documente les statuts inclus et les regles de tri.

### `PRD-446` Qualite, SEO et mesure du parcours animation

- Priorite : `P1`
- Statut : `A faire`
- En tant que responsable produit, je veux mesurer et referencer la decouverte des animations afin de piloter leur utilite sans collecter de donnees personnelles.
- Les pages catalogue et detail definissent titres, descriptions et URL canoniques coherents.
- Le balisage structure `Event` est ajoute sur les fiches eligibles lorsque les donnees obligatoires sont disponibles.
- Les evenements de mesure couvrent impression du bloc, filtre commune, ouverture du detail et debut d'inscription.
- Aucun token participant, email, telephone ou identifiant personnel n'est transmis aux analytics.

### `PRD-447` Animations dans la recherche marketplace

- Priorite : `P2`
- Statut : `A faire`
- En tant que visiteur, je veux retrouver une animation par son nom depuis la recherche marketplace afin d'y acceder directement.
- Le scope `ANIMATION` est ajoute a l'Epic 33 uniquement apres mise en service du catalogue public.
- Seules les animations respectant l'eligibilite publique centralisee sont indexees.

## Decoupage propose

| Lot | Priorite | Etat | Contenu | Dependances | Sortie attendue |
| --- | --- | --- | --- | --- | --- |
| B0 | P0 | Termine | Predicat d'eligibilite, filtres et synthese publique | Epic 41 | OpenAPI et tests backend garantissant l'absence d'animations de communes non abonnees |
| F0 | P0 | Termine | Catalogue `/animations` et integration de la fiche existante | B0 | Parcours public partageable sans Localeo Live |
| F1 | P0 | Termine | Bloc page commune | F0 | Decouverte locale contextualisee |
| F2 | P1 | Termine | Synthese accueil et detail par commune | B0, F0 | Preuve territoriale et acces au catalogue |
| F3 | P1 | Termine | Blocs commercant et coffret | B0, F0 | Contextes metier pertinents sans duplication generique |
| F4 | P1 | Termine | Responsive, accessibilite, SEO, analytics et recette | F1-F3 | Mise en production mesuree et accessible |
| F5 | P2 | Termine | Scope animation dans la recherche | Epic 33, F0 | Acces direct par recherche multi-scope |

## Ordre de mise en oeuvre recommande

1. centraliser l'eligibilite et livrer la synthese backend ;
2. creer le catalogue `/animations` ;
3. integrer le bloc principal sur la page commune ;
4. ajouter la synthese territoriale sur l'accueil ;
5. ajouter les blocs strictement contextuels sur les pages commercant et coffret ;
6. ouvrir le scope de recherche et finaliser la recette transverse.

## Criteres d'acceptation globaux

- Une animation d'une commune sans abonnement Animation actif n'apparait nulle part dans la marketplace.
- Une animation annulee, cloturee, archivee ou masquee ne contribue pas aux compteurs publics.
- Les compteurs de l'accueil correspondent exactement au catalogue accessible.
- La page commune n'affiche son bloc que lorsqu'au moins une animation eligible existe.
- Les pages commercant et coffret n'affichent que leurs rattachements reels.
- Le catalogue et le detail sont consultables sans installer ou charger Localeo Live.
- L'absence de visuel officiel ne provoque jamais l'affichage d'une image generique sans rapport.
- Les routes directes, le retour arriere, le clavier, le mobile et les lecteurs d'ecran sont recettables.
- Aucune donnee participant ni information contractuelle d'abonnement n'est exposee.
- Une indisponibilite de l'API animation ne bloque ni la consultation ni l'achat des coffrets.

## Hors perimetre initial

- carte geographique interactive du territoire ;
- recommandations personnalisees ou geolocalisation automatique ;
- affichage public du nombre de participants ;
- commentaires, reactions ou reseau social autour des animations ;
- gestion des animations depuis la marketplace ;
- duplication des ecrans de suivi personnel de Localeo Live.

## Etat des lieux technique avant implementation (23 aout 2026)

- `GET /public/animation-locale/animations` et le detail public existent deja, mais la liste charge toutes les animations, applique le filtre en memoire puis appelle le detail pour chaque ligne : ce fonctionnement cree un risque N+1 et ne fournit pas une pagination fiable.
- le `count` actuel correspond au nombre d'elements apres application de `limit`, pas au total eligible ;
- la liste et le detail ne controlent pas encore l'abonnement du couple reel `(partenaire_id, commune_id)` ;
- le detail ne retourne ni statut public derive, ni indicateur d'inscription, ni visuel public, ni URL publique explicite ;
- `VilleOrm` ne porte actuellement aucun statut `actif` : la commune du payload public est marquee active en dur ;
- les rattachements commercants et coffrets sont stockes dans la configuration JSON versionnee (`commercant_ids` et `lots`) ; ils referencent bien les objets existants et ne doivent pas creer un second concept de commune ;
- la route Marketplace `/animations/{animation_id}` existe, mais le catalogue `/animations` n'existe pas encore ; la declaration actuelle de la route dynamique devra rester apres la nouvelle route catalogue ;
- Localeo Live consomme deja la liste et le detail publics : leur evolution doit rester additive ou etre coordonnee avec ce consommateur ;
- les pages accueil, commune, commercant et coffret ne chargent actuellement aucune projection animation ;
- le backend ne dispose pas de cache public applicatif a invalider pour ces projections.

## Resultat de l'implementation

- le backend applique une requete SQL unique et bornee aux animations `PUBLIEE` ou `EN_COURS`, a la configuration courante, a la commune publiee et a l'abonnement strictement `ACTIF` du couple partenaire-commune ;
- les routes publiques de liste, synthese, detail et visuel partagent cette eligibilite, exposent un cache HTTP court et des reponses OpenAPI modelisees ;
- la pagination par curseur, les filtres commune, commercant, coffret, statut et inscription ainsi que l'horizon configurable sont disponibles ;
- la migration `v177_epic49_animations_marketplace.sql` ajoute l'indicateur de publication de la commune et les index de lecture ;
- le Marketplace expose le catalogue `/animations`, enrichit l'accueil et les pages commune, commercant et coffret, et conserve le detail direct lorsque le feature flag est coupe ;
- le detail dispose des metadonnees SEO client, du JSON-LD `Event`, d'un visuel de repli et d'un rendu explicite des regles de participation ;
- la recherche multi-scope accepte maintenant les resultats `ANIMATION` et ouvre leur detail public ;
- le build de production Marketplace est valide ; la recette fonctionnelle sur donnees deployees reste le dernier jalon avant MEP.

## Conception associee

- [Vue d'ensemble](../../specifications/epic-49-animations-marketplace/README.md)
- [Conception backend et contrats API](../../specifications/epic-49-animations-marketplace/backend-api.md)
- [Conception Marketplace](../../specifications/epic-49-animations-marketplace/frontend-marketplace.md)
- [Registre des arbitrages](../../specifications/epic-49-animations-marketplace/registre-arbitrages.md)

## Decisions issues du registre

- seule la valeur d'abonnement `ACTIF` autorise la visibilite publique ; `EN_GRACE` est exclu ;
- l'expiration retire immediatement l'animation des routes publiques de decouverte et de detail, sans couper les acces participant tokenises ni les operations de continuite ;
- `commune` est le terme metier canonique et reference l'unique table historique `villes` ; aucun second concept n'est cree ;
- l'horizon futur vaut 90 jours par defaut et reste configurable ;
- le visuel principal est explicitement reference, puis l'apercu flyer et enfin un bloc typographique servent de replis ;
- l'evolution API est additive et conserve temporairement `limit` ;
- la pagination utilise un curseur stable, une taille maximale de 50 et une projection `pagination` ;
- le cache V1 repose sur les en-tetes HTTP pendant 60 secondes, sans cache serveur ;
- l'affichage Marketplace est pilote par un feature flag runtime sans couper l'API publique ;
- les analytics reutilisent le consentement existant et excluent toute PII ;
- l'accueil utilise la commune selectionnee, sinon une synthese globale ;
- le MVP SEO fournit titre, canonique et JSON-LD cote client, sans SSR ni prerendu.
- seuls les coffrets presents dans les `lots` de la configuration publiee sont exposes, avec la nature `LOT_A_GAGNER`.

## Arbitrages restants

Aucun. Tous les arbitrages du registre sont valides au 23 aout 2026.

## MARKET-007 - Inscription non rejouable

Reprise transactionnelle et recuperation de la capacite apres perte de reponse ; aucun acces par email seul. Voir le contrat des correctifs Marketplace du 6 septembre 2026.

## MARKET-008 - Continuite participant

MKTANIM-ARB-02 applique : acces participant authentifie distinct de la disponibilite du catalogue public.


## Compléments Marketplace

Les passages communs sont intégrés au corps principal. Les précisions et jalons propres à cette interface sont conservés ci-dessous ; leurs anciens états de lots ne remplacent pas l’état produit commun.

### MARKET-007 - Inscription non rejouable

Reprise de la meme intention apres resultat incertain, en coordination avec l'idempotence backend. Test navigateur dans market-corrections.spec.cjs.
