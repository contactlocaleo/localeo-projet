# Backlog Epic 17 - Feedback client post-prestation

> État produit commun : **Terminée**. Backlog consolidé le 18 septembre 2026 ; les contributions applicatives sont réunies dans ce fichier. Les anciens états de cadrage ou de stories restent historiques et ne rouvrent pas l’EPIC.

## Perimetre

Epic source : `Epic 17. Feedback client post-prestation`

Objectif : collecter un retour simple des clients apres chaque consommation de prestation afin d'ameliorer la qualite operationnelle, detecter les irritants et alimenter la marketplace avec des signaux qualitatifs moderes et anonymises.

## Statut global

- Epic 17 : `Termine`
- Avancement : stockage, tokenisation, integration email, API publique, agregats et moderation backoffice disponibles cote backend.

## Vision produit

Le feedback post-prestation doit capter le ressenti client au meilleur moment : juste apres l'utilisation d'une prestation. Il doit rester tres simple pour maximiser le taux de reponse et eviter de transformer le parcours en enquete lourde.

Principes :
- demander un retour apres chaque prestation consommee ;
- rendre la reponse possible en un clic depuis l'email ;
- proposer une note de 1 a 4 etoiles ;
- permettre un commentaire optionnel ;
- ne jamais publier automatiquement un commentaire brut ;
- permettre la moderation backoffice avant toute exposition publique ;
- exploiter les notes sous forme d'agregats marketplace.

## Decisions initiales

- La collecte V1 est declenchee apres chaque `PRESTATION_VALIDEE`.
- Le formulaire n'est pas integre directement dans l'email.
- La V1 ne cree pas de nouvel email : le feedback est integre au template existant `prestation_utilisee`.
- L'email de prestation utilisee contient un bloc conditionnel avec des liens de notation de 1 a 4 etoiles.
- Chaque lien ouvre une page publique securisee par token opaque.
- Le token est a usage unique, expire et stocke uniquement sous forme de hash.
- La note est obligatoire.
- Le commentaire est optionnel.
- Le client peut autoriser explicitement l'utilisation publique anonymisee de son commentaire.
- Les commentaires ne sont jamais publics sans moderation.
- Un feedback global de fin de coffret pourra etre ajoute en V2.
- La duree d'expiration du token de feedback est fixee a 30 jours en V1.
- Aucune relance automatique n'est envoyee en V1 si le client ne repond pas.
- Les agregats publics ne sont pas masques lorsque le volume d'avis est faible ; le nombre d'avis doit etre affiche pour contextualiser la note.

## Modele de donnees recommande

Creer une table `feedbacks_prestation`.

Champs recommandes :
- `id`
- `validation_prestation_id` unique
- `coffret_instance_id`
- `prestation_coffret_id`
- `commercant_id`
- `coffret_id`
- `note` entier de 1 a 4
- `commentaire` nullable
- `autorisation_publication` boolean
- `statut_moderation` : `A_MODERER`, `APPROUVE`, `REFUSE`, `MASQUE`
- `token_hash`
- `token_created_at`
- `token_expires_at`
- `token_used_at`
- `date_envoi_demande`
- `date_reponse`
- `source` : `EMAIL_PRESTATION_VALIDEE`
- `date_creation`

Index recommandes :
- `validation_prestation_id`
- `commercant_id`
- `prestation_coffret_id`
- `coffret_id`
- `statut_moderation`
- `date_reponse`
- `token_hash`

Contraintes :
- une validation de prestation ne peut produire qu'un feedback client ;
- une note doit etre comprise entre 1 et 4 ;
- le token brut ne doit jamais etre stocke ;
- `token_expires_at` est initialise a `token_created_at + 30 jours` ;
- le commentaire doit etre limite en taille, par exemple 1000 caracteres.

## Parcours cible V1

1. Une prestation est validee.
2. Le systeme cree une demande de feedback tokenisee.
3. L'email `prestation utilisee` contient quatre liens de notation.
4. Le client clique sur une note.
5. La page publique verifie le token et preselectionne la note.
6. Le client peut ajouter un commentaire optionnel.
7. Le client valide.
8. Le token devient utilise.
9. Le feedback apparait en backoffice.
10. Les agregats sont disponibles pour la marketplace.
11. Les commentaires approuves peuvent etre exposes anonymement si l'autorisation est donnee.

## Email attendu

Dans le template existant `prestation_utilisee`, ajouter un bloc court et conditionnel.

Le bloc est affiche uniquement si le use case de validation de prestation fournit les donnees de feedback, notamment les liens tokenises de notation.

- Titre : `Comment s'est passee cette experience ?`
- Texte : `Votre retour aide Localeo et ses partenaires a ameliorer les coffrets.`
- Boutons/liens :
  - `1 etoile`
  - `2 etoiles`
  - `3 etoiles`
  - `4 etoiles`

Chaque lien contient :
- le token de feedback ;
- la note choisie ;
- un lien vers une page marketplace publique dediee.

Le mail ne doit pas contenir de formulaire HTML interactif.

La creation d'un nouvel email dedie est hors perimetre V1. Elle pourra etre envisagee en V2 uniquement pour une relance si le client n'a pas repondu.

## API publique recommandee

Endpoints :
- `GET /public/feedbacks-prestation/{token}`
- `POST /public/feedbacks-prestation/{token}`

`GET` retourne :
- validite du token ;
- statut de reponse ;
- indicateur `soumission_autorisee` ;
- note preselectionnee si fournie ;
- resume public de la prestation ;
- resume public du commercant ;
- resume public du coffret.

`POST` accepte :
- `note` entre 1 et 4 ;
- `commentaire` optionnel ;
- `autorisation_publication` boolean.

Regles :
- refuser un token inconnu, expire, revoque ou deja utilise ;
- ne jamais exposer email client, telephone client, achat_id public ou details sensibles ;
- retourner un message generique en cas de token invalide.

## Backoffice attendu

Ajouter une vue `Feedbacks prestation`.

Fonctionnalites V1 :
- lister les feedbacks ;
- filtrer par note, commercant, prestation, coffret, statut de moderation ;
- consulter le commentaire ;
- approuver un commentaire ;
- refuser un commentaire ;
- masquer un commentaire approuve ;
- voir les feedbacks sans commentaire comme signaux quantitatifs ;
- pointer vers la validation de prestation source.

Actions possibles :
- `Approuver`
- `Refuser`
- `Masquer`
- `Remettre a moderer`

Implementation V1 backend :
- migration `sql/v135_feedback_client_post_prestation.sql` ;
- projection ORM `FeedbackPrestationOrm` ;
- generation d'une demande de feedback lors de `PRESTATION_VALIDEE` ;
- integration conditionnelle dans le template email `prestation_utilisee` ;
- endpoints publics `GET/POST /public/feedbacks-prestation/{token}` ;
- endpoint public `GET /public/feedbacks-prestation/metriques` ;
- endpoint public `GET /public/feedbacks-prestation/commentaires` ;
- vue backoffice `Feedbacks prestation` avec actions de moderation.

## Agregats marketplace

La V1 doit exposer des agregats publics sans commentaire brut non modere.

Agregats utiles :
- note moyenne par commercant ;
- nombre d'avis par commercant ;
- note moyenne par prestation ;
- nombre d'avis par prestation ;
- note moyenne par coffret ;
- nombre d'avis par coffret ;
- taux de satisfaction, par exemple part des notes 3 ou 4.

Endpoints possibles :
- `GET /public/feedbacks-prestation/metriques?commercant_id=...`
- `GET /public/feedbacks-prestation/metriques?coffret_id=...`
- `GET /public/feedbacks-prestation/metriques?prestation_coffret_id=...`

## Exposition publique des commentaires

En V1, un commentaire est exposable seulement si :
- `autorisation_publication = true` ;
- `statut_moderation = APPROUVE` ;
- le commentaire ne contient pas de donnee personnelle evidente ;
- l'affichage reste anonymise.

Affichage recommande :
- `Client Localeo`
- note ;
- commentaire ;
- periode floutee, par exemple `recemment` ou `ce mois-ci`.

## User Stories detaillees

### `PRD-087` Demande de feedback post-prestation


Statut : `Termine`

En tant que client, je veux pouvoir donner mon avis juste apres avoir utilise une prestation afin de partager facilement mon ressenti.

Resultats attendus :
- l'email existant `prestation_utilisee` contient un CTA de feedback ;
- le client peut choisir une note de 1 a 4 ;
- le lien ouvre une page publique securisee.

### `PRD-088` Soumission securisee du feedback


Statut : `Termine`

En tant que systeme, je veux verifier un token de feedback afin de garantir qu'un avis correspond a une prestation reellement consommee.

Resultats attendus :
- le token est opaque, expire et a usage unique ;
- le token brut n'est jamais stocke ;
- un token invalide ou expire ne permet pas de soumettre un avis.

### `PRD-089` Commentaire optionnel et consentement


Statut : `Termine`

En tant que client, je veux pouvoir ajouter un commentaire optionnel et choisir s'il peut etre reutilise publiquement de facon anonymisee.

Resultats attendus :
- le commentaire est optionnel ;
- l'autorisation de publication est explicite ;
- le commentaire est limite en taille ;
- le commentaire n'est pas publie automatiquement.

### `PRD-090` Moderation backoffice


Statut : `Termine`

En tant qu'admin, je veux moderer les commentaires client afin de maitriser ce qui peut etre affiche publiquement.

Resultats attendus :
- une vue backoffice liste les feedbacks ;
- un admin peut approuver, refuser ou masquer un commentaire ;
- les notes restent exploitables meme si le commentaire est refuse.

### `PRD-091` Agregats publics de satisfaction


Statut : `Termine`

En tant que visiteur marketplace, je veux voir des signaux de satisfaction agreges afin de mieux choisir un coffret ou un commercant.

Resultats attendus :
- les pages commercant, coffret et prestation peuvent afficher une note moyenne ;
- le nombre d'avis est affiche ;
- les agregats restent affichables meme si le volume d'avis est faible ;
- aucun detail client n'est expose.

### `PRD-092` Exploitation qualite


Statut : `Termine`

En tant qu'operateur Localeo, je veux suivre les retours faibles afin de detecter les prestations ou partenaires a surveiller.

Resultats attendus :
- le backoffice permet de filtrer les notes 1 ou 2 ;
- les retours faibles pointent vers le commercant, la prestation et la validation source ;
- le systeme conserve la trace du retour pour pilotage qualite.

## Criteres d'acceptation globaux

- Un feedback ne peut etre soumis que via un token valide.
- Un token ne peut etre utilise qu'une seule fois.
- Une validation de prestation ne produit pas plusieurs feedbacks.
- La note est obligatoire et comprise entre 1 et 4.
- Le commentaire est optionnel.
- Les commentaires publics sont anonymises, autorises par le client et moderes.
- Les agregats publics ne permettent pas d'identifier un client.
- Le backoffice permet de moderer les commentaires.
- L'absence de feedback ne bloque jamais le parcours client.

## Hors perimetre V1

- Feedback global de fin de coffret.
- Reponse publique du commercant a un avis.
- Publication automatique des commentaires sans moderation.
- Analyse semantique automatique des commentaires.
- Relance automatique des clients n'ayant pas repondu. Elle pourra etre reetudiee en V2 apres mesure du taux de reponse, avec une relance unique apres 5 a 7 jours maximum.
- Integration d'avis tiers externes.

## Questions ouvertes

- Aucune question ouverte a ce stade pour la V1.
