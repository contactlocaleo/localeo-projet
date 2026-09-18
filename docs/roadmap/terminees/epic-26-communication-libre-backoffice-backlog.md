# Backlog Epic 26 - Communication libre backoffice

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : permettre a un operateur back-office d'envoyer une communication libre a un commercant, a un client ou a un destinataire libre, par email ou SMS, en reutilisant les services d'envoi existants et leur historique.
- Decision produit : la communication libre est un outil d'exploitation et de support, pas un outil de campagne marketing de masse.
- Decision technique : les envois doivent passer par les outbox existantes `emails_sortants` et `sms_sortants`, sans appel direct aux providers depuis le back-office.
- Decision operationnelle : chaque communication doit etre rattachee a un acteur back-office, un destinataire identifie ou saisi librement, un canal, un contenu et un statut d'envoi historise.
- Decision MVP : la communication libre n'est pas rattachee a une demande support, un achat ou une `CoffretInstance`.
- Decision MVP : la signature Localeo est unique et non configurable par ville ou equipe.
- Decision MVP : aucun niveau de droits distinct n'est introduit entre lecture de l'historique et creation de communication.
- Decision MVP : aucune politique de retention specifique n'est ajoutee pour le contenu libre email/SMS.

## Probleme

Le back-office permet deja de diagnostiquer les achats, les coffrets, les emails, les SMS et les demandes support. En revanche, lorsqu'un operateur doit contacter ponctuellement un commercant ou un client avec un message libre, il doit sortir du systeme Localeo ou detourner un flux existant.

Cette situation fragilise la tracabilite : le contenu envoye, le destinataire, l'operateur, le canal, le statut d'envoi et les erreurs provider ne sont pas toujours rattaches au dossier Localeo. Elle empeche aussi de capitaliser sur les mecanismes deja presents : outbox email/SMS, batchs d'envoi, synchronisation de statuts et timeline support.

## Risque business

- Reponses support non tracees dans Localeo.
- Messages envoyes depuis des outils externes sans historique centralise.
- Risque d'envoyer une information au mauvais destinataire faute de recherche fiable dans le referentiel ou de validation stricte du destinataire libre.
- Difficultes a prouver qu'une communication a ete preparee, envoyee, delivree ou mise en echec.
- Perte de coherence de marque si les emails libres ne peuvent pas embarquer la signature Localeo.

## Risque technique

- Contournement de l'outbox email/SMS et appels directs aux providers.
- Duplication de logique de preparation de messages.
- Historique incomplet si la communication libre n'alimente pas les tables d'envoi actuelles.
- Exposition de donnees personnelles dans les logs ou les vues back-office.
- Risque XSS si le texte riche email n'est pas encadre et assaini.

## Perimetre MVP

- Ajouter une entree back-office `Communication libre`.
- Permettre de choisir le type de destinataire : `Client`, `Commercant` ou `Libre`.
- Permettre de rechercher un destinataire dans les referentiels existants par nom, prenom, nom de commerce, email ou telephone.
- Permettre de saisir un destinataire libre non rattache a un client ou commercant existant.
- Afficher les coordonnees disponibles du destinataire de facon lisible et masquee quand necessaire.
- Permettre de choisir le canal : `Email` ou `SMS`.
- Pour un email :
  - saisir un objet ;
  - saisir un contenu en texte riche ;
  - ajouter optionnellement une signature Localeo standardisee ;
  - generer une version texte de secours.
- Pour un SMS :
  - saisir un message texte ;
  - afficher un compteur de caracteres ;
  - appliquer les limites de longueur definies pour le provider SMS.
- Creer un `EmailSortant` ou un `SmsSortant` via les services applicatifs existants.
- Historiser la communication comme les autres envois actuels.
- Rattacher l'envoi a l'operateur back-office et au destinataire, qu'il soit resolu depuis un referentiel ou saisi librement.
- Afficher les communications libres dans les vues d'historique email/SMS et dans la timeline support quand le contexte le permet.

## Hors perimetre MVP

- Envoi de masse ou segmentation marketing.
- Programmation d'envoi differe.
- Gestion de templates marketing reutilisables.
- Pieces jointes libres.
- Rattachement obligatoire a une demande support, un achat ou une `CoffretInstance`.
- Tracking d'ouverture/clic dedie au marketing.
- Conversations bidirectionnelles SMS.
- Editeur email avance type builder drag-and-drop.
- Envoi de masse vers une liste de destinataires libres.

## User Stories

1. `PRD-159` En tant qu'operateur back-office, je veux acceder a une page de communication libre afin de contacter ponctuellement un client, un commercant ou un destinataire libre depuis Localeo.
   - Statut : `Termine`
   - Resultat attendu : une entree back-office dediee est disponible pour les profils autorises.
   - Resultat attendu : la page permet de choisir un destinataire, un canal et un contenu.

2. `PRD-160` En tant qu'operateur back-office, je veux rechercher un destinataire dans les referentiels client et commercant ou saisir un destinataire libre afin de contacter la bonne personne.
   - Statut : `Termine`
   - Resultat attendu : la recherche accepte nom, prenom, nom de commerce, email et telephone.
   - Resultat attendu : les resultats indiquent le type de destinataire, son libelle, ses coordonnees disponibles et son statut utile.
   - Resultat attendu : le mode libre permet de saisir un nom/libelle optionnel, un email ou un telephone selon le canal choisi.

3. `PRD-161` En tant qu'operateur back-office, je veux choisir entre email et SMS afin d'utiliser le canal adapte au besoin de communication.
   - Statut : `Termine`
   - Resultat attendu : le canal email est disponible seulement si une adresse email exploitable existe ou est saisie.
   - Resultat attendu : le canal SMS est disponible seulement si un telephone exploitable existe ou est saisi.

4. `PRD-162` En tant qu'operateur back-office, je veux composer un email riche afin d'envoyer une communication claire et professionnelle.
   - Statut : `Termine`
   - Resultat attendu : l'email contient un objet obligatoire et un corps riche assaini.
   - Resultat attendu : le contenu HTML autorise une mise en forme simple : paragraphes, liens, gras, italique et listes.
   - Resultat attendu : une version texte est produite automatiquement ou saisie explicitement.

5. `PRD-163` En tant qu'operateur back-office, je veux ajouter une signature Localeo afin de garantir une coherence de marque sur les emails libres.
   - Statut : `Termine`
   - Resultat attendu : une option permet d'ajouter la signature standard Localeo.
   - Resultat attendu : la signature est maintenue cote application et non recopiee manuellement par l'operateur.

6. `PRD-164` En tant qu'operateur back-office, je veux composer un SMS court afin d'envoyer une information rapide au destinataire.
   - Statut : `Termine`
   - Resultat attendu : le SMS affiche un compteur de caracteres.
   - Resultat attendu : le SMS respecte les contraintes de longueur, de caracteres et d'expediteur du provider.

7. `PRD-165` En tant que responsable exploitation, je veux que chaque communication libre soit historisee comme les autres envois afin de conserver une trace auditable.
   - Statut : `Termine`
   - Resultat attendu : les emails libres creent des lignes `emails_sortants` avec un type dedie.
   - Resultat attendu : les SMS libres creent des lignes `sms_sortants` avec un type dedie.
   - Resultat attendu : les statuts provider, erreurs, retries et synchronisations suivent les mecanismes existants.

8. `PRD-166` En tant que responsable securite, je veux encadrer les communications libres afin d'eviter les abus, les fuites de donnees et les contenus dangereux.
   - Statut : `Termine`
   - Resultat attendu : l'acces est limite aux administrateurs autorises.
   - Resultat attendu : les contenus HTML sont assainis avant enregistrement et envoi.
   - Resultat attendu : l'acteur back-office, la date, le canal et le destinataire sont audites, y compris pour un destinataire libre.

## Regles de gestion

- Une communication libre ne doit jamais appeler directement Brevo ou un autre provider.
- L'envoi doit passer par les batchs existants d'email ou de SMS.
- Le destinataire peut etre selectionne depuis un referentiel connu ou saisi en mode libre.
- Le mode libre exige au minimum un email valide pour le canal email ou un telephone valide pour le canal SMS.
- Le mode libre doit conserver le libelle saisi par l'operateur quand il existe, sans creer de fiche client ou commercant.
- Le canal email exige une adresse email valide.
- Le canal SMS exige un numero de telephone normalise et compatible avec le provider.
- Le contenu email riche doit etre assaini selon une liste blanche de balises et d'attributs.
- Les liens dans les emails doivent etre visibles et ne doivent pas masquer de destination dangereuse.
- La signature Localeo doit etre ajoutee par le systeme quand l'option est activee.
- La signature Localeo est unique pour le MVP.
- Un apercu doit etre affiche avant creation de l'envoi.
- La creation d'une communication libre doit etre auditee.
- Les listes back-office doivent masquer les coordonnees quand l'affichage complet n'est pas necessaire.
- Un operateur ne peut relancer une communication libre que via les mecanismes de relance existants.

## Modele de donnees cible

### Email libre

- Table existante : `emails_sortants`
- Type cible : `COMMUNICATION_LIBRE_BACKOFFICE`
- Champs attendus :
  - `destinataire`
  - `sujet`
  - `corps_html`
  - `corps_texte`
  - `statut`
  - `provider_message_id`
  - `erreur`
  - `date_creation`
  - `date_envoi`
  - `metadata`

### SMS libre

- Table existante : `sms_sortants`
- Type cible : `COMMUNICATION_LIBRE_BACKOFFICE`
- Champs attendus :
  - `destinataire`
  - `message`
  - `statut`
  - `provider_message_id`
  - `erreur`
  - `date_creation`
  - `date_envoi`
  - `metadata`

### Metadata minimale

- `source` : `backoffice_communication_libre`
- `acteur_admin_id` ou identifiant operateur disponible
- `destinataire_type` : `CLIENT`, `COMMERCANT` ou `LIBRE`
- `destinataire_id`
- `destinataire_libelle`
- `destinataire_libre_email` ou `destinataire_libre_telephone` si aucun referentiel n'est rattache
- `canal`
- `signature_localeo`
- Aucun `objet_metier_id` n'est exige dans le MVP.

## Recherche destinataire

### Destinataire libre

- Saisie par :
  - libelle ou nom visible pour l'operateur ;
  - email pour le canal email ;
  - telephone pour le canal SMS.
- Validations attendues :
  - email syntaxiquement valide ;
  - telephone normalise et compatible avec le provider SMS ;
  - confirmation explicite avant creation de l'envoi ;
  - absence de creation automatique d'une fiche client ou commercant.

### Referentiel commercant

- Recherche par :
  - nom de commerce ;
  - nom/prenom du contact si disponible ;
  - email de contact ;
  - telephone de contact.
- Resultats affiches :
  - nom de commerce ;
  - ville si disponible ;
  - statut commercant ;
  - email masque ;
  - telephone masque.

### Referentiel client

- Recherche par :
  - nom ;
  - prenom ;
  - email client ;
  - telephone client ;
  - reference achat si disponible.
- Resultats affiches :
  - nom/prenom ou email si le nom est absent ;
  - references metier utiles ;
  - email masque ;
  - telephone masque.

## Back-office cible

### Page de composition

- `GET /admin/communications-libres`
- Acces reserve aux administrateurs autorises.
- Sections attendues :
  - recherche destinataire ;
  - choix canal ;
  - composition ;
  - apercu ;
  - validation.

### Action de creation

- `POST /admin/communications-libres`
- Cree un email ou SMS sortant en statut `A_ENVOYER`.
- Redirige vers la fiche de l'envoi cree ou vers l'historique des communications libres.

### Historique

- Filtrer les emails/SMS par type `COMMUNICATION_LIBRE_BACKOFFICE`.
- Afficher :
  - date creation ;
  - canal ;
  - destinataire masque ;
  - objet ou extrait ;
  - statut ;
  - acteur ;
  - lien vers email/SMS sortant.

## Lots d'implementation

### Lot 1 - Cadrage domaine et contrats

- Definir les types `COMMUNICATION_LIBRE_BACKOFFICE` email et SMS.
- Definir le contrat de recherche destinataire.
- Definir les metadata obligatoires.
- Definir la signature Localeo standard.

### Lot 2 - Recherche destinataire

- Ajouter le use case `RechercherDestinatairesCommunicationLibre`.
- Interroger les referentiels commercant et client.
- Ajouter un mode de saisie et validation de destinataire libre.
- Normaliser et masquer les coordonnees dans la reponse.
- Limiter le nombre de resultats.

### Lot 3 - Composition email

- Ajouter la preparation d'email libre dans `ServicePreparationEmail`.
- Ajouter l'assainissement du HTML.
- Ajouter l'option signature Localeo.
- Creer l'email sortant via l'outbox existante.

### Lot 4 - Composition SMS

- Ajouter la preparation de SMS libre dans le service SMS applicatif.
- Valider la longueur et le format telephone.
- Creer le SMS sortant via l'outbox existante.

### Lot 5 - Back-office et historique

- Ajouter la page SQLAdmin ou route admin dediee.
- Ajouter l'apercu avant validation.
- Ajouter les filtres d'historique.
- Ajouter les liens depuis les vues email/SMS et, si disponible, la timeline support.

### Lot 6 - Securite et tests

- Restreindre l'acces aux administrateurs autorises.
- Auditer les creations de communications libres.
- Ajouter des tests de validation canal/destinataire/contenu.
- Ajouter des tests de destinataire libre email et SMS.
- Ajouter des tests d'assainissement HTML.
- Ajouter des tests de creation outbox email et SMS.

## Definition of Done

- Un operateur autorise peut rechercher un client ou un commercant.
- Un operateur autorise peut saisir un destinataire libre.
- Un operateur autorise peut envoyer une communication libre par email si l'adresse existe ou est saisie et valide.
- Un operateur autorise peut envoyer une communication libre par SMS si le telephone existe ou est saisi et valide.
- Les emails libres supportent un contenu riche assaini et une signature Localeo optionnelle.
- La signature Localeo utilisee est unique.
- Les envois creent des lignes outbox existantes, sans appel direct provider.
- Les batchs existants prennent en charge l'envoi.
- Les statuts et erreurs sont historises comme les autres emails/SMS.
- Les communications libres sont auditables avec acteur, destinataire, canal et date.
- Les communications libres MVP ne sont pas rattachees a une demande support, un achat ou une `CoffretInstance`.
- Les donnees personnelles sont masquees dans les vues de liste quand necessaire.
- Les tests couvrent recherche, validation, creation outbox et securite HTML.

## Points arbitres

- Pas de rattachement a une demande support, un achat ou une `CoffretInstance` dans le MVP.
- Signature Localeo unique.
- Pas de distinction de droits entre lecture de l'historique et creation pour le moment.
- Pas de politique de retention specifique pour le moment.
