# Epic 9. Mode secours telephonique pour l'honorisation d'une prestation

## Statut

`Termine`

## Objectif

Permettre a un commercant d'honorer exceptionnellement une prestation en cas d'indisponibilite cote commercant, d'incident sur le parcours QR client ou de probleme de reseau local, grace a une procedure de secours telephonee, exploitable par le support Localeo et tracee de bout en bout.

Le but est de couvrir :
- l'identification raisonnable du commercant appelant ;
- l'identification simple d'une `CoffretInstance` a distance sans scan ;
- la verification par un operateur Localeo de la validite du coffret ;
- l'autorisation ou le refus de l'honorisation ;
- la tracabilite complete de la decision et de son contexte.

## Problemes a resoudre

- Un commercant peut se retrouver incapable d'acceder a son espace ou au parcours de validation au moment d'honorer une prestation.
- Le QR code du client n'est pas exploitable facilement dans un contexte d'appel telephonique.
- Le support ne dispose pas encore d'un identifiant simple, lisible et dicte a l'oral pour retrouver une `CoffretInstance`.
- Les validations manuelles informelles exposent a des risques de fraude, d'erreur et d'absence de tracabilite.
- L'absence de procedure outillee peut conduire a refuser une prestation legitime ou a autoriser une prestation sans preuve suffisante.

## Perimetre V1

- Ajout d'un `verification_code` court, unique et lisible a l'oral sur chaque `CoffretInstance`.
- Recherche back-office d'une `CoffretInstance` par `verification_code`.
- Procedure de verification minimale de l'identite commercant lors d'un appel.
- Workflow support permettant d'autoriser ou refuser une validation en `mode secours`.
- Journalisation et audit des usages du mode secours.
- Documentation operateur et procedure commercant.

## Hors perimetre V1

- Mode offline autonome cote commercant.
- Validation automatique sans intervention support.
- Synchronisation offline locale.
- Verification cryptographique locale du support client.
- Application mobile ou interface dediee au support telephonique.
- Authentification forte du commercant par second facteur temps reel.
- Traitement d'une indisponibilite totale du backend, de la base de donnees ou du back-office Localeo.

## Modele cible

### `CoffretInstance.verification_code`

Champs recommandes :
- `verification_code`
- `verification_code_created_at`

Contraintes :
- code unique ;
- code court ;
- code lisible et dictable a l'oral ;
- caracteres non ambigus ;
- recherche rapide en back-office ;
- affichage sur les supports utiles en complement du QR code client.

Format retenu :
- type `AB34-KT92` ;
- 8 caracteres utiles groupes par 4 ;
- sans caracteres ambigus de type `O/0`, `I/1`, `S/5`.

Notes :
- le `verification_code` sert a identifier une `CoffretInstance` ;
- le `verification_code` n'est pas un secret ;
- la decision support repose sur le code plus les controles metier effectues au back-office.
- `verification_code_created_at` est persiste pour tracer la generation du code et faciliter les controles d'exploitation.

### `ValidationSecours`

Champs recommandes :
- `id`
- `secours_request_id`
- `coffret_instance_id`
- `statut_prestation_coffret_instance_id`
- `prestation_coffret_id`
- `commercant_id`
- `operateur_admin_identifiant`
- `canal` : `TELEPHONE`
- `decision` : `AUTORISE`, `REFUSE`, `A_CONTROLER`
- `statut_execution` : `EN_COURS`, `SUCCES`, `ECHEC`
- `motif_incident`
- `verification_commercant_resume`
- `validation_metier_id` nullable
- `erreur_execution` nullable
- `commentaire`
- `date_creation`
- `date_execution` nullable

Notes :
- une entree `ValidationSecours` trace une demande et sa decision ;
- la trace doit identifier sans ambiguite la ligne `statuts_prestation_coffret_instance` traitee en mode secours ;
- `secours_request_id` porte l'idempotence technique de la demande de secours et doit etre unique ;
- une decision `AUTORISE` declenche la validation metier effective via un use case dedie `TraiterValidationSecours` ;
- le use case secours ne depend pas d'une transaction QR client ouverte ; il reutilise ou extrait la logique metier de validation commune au parcours nominal ;
- le use case dedie de mode secours s'execute dans le pattern `UOW` deja en place afin de garantir la coherence entre validation metier et trace `ValidationSecours` ;
- la trace `ValidationSecours` est conservee en plus de la validation metier afin d'auditer le recours au mode secours ;
- le resume de verification commercant doit expliciter les informations controlees lors de l'appel.

### Audit

Evenements d'audit retenus :
- `validation.secours.authorized`
- `validation.secours.refused`
- `validation.secours.control_requested`
- `validation.secours.failed`

Regles :
- `validation.secours.authorized` est emis lorsqu'une decision `AUTORISE` aboutit a une validation metier effective ;
- `validation.secours.refused` est emis lorsqu'une decision `REFUSE` est enregistree ;
- `validation.secours.control_requested` est emis lorsqu'une decision `A_CONTROLER` est enregistree ;
- `validation.secours.failed` est emis lorsqu'une validation secours autorisee echoue techniquement ou metierement ;
- les evenements d'audit ne remplacent pas le journal metier `ValidationSecours`.

## User Stories

### `PRD-040` Generer un code de verification par `CoffretInstance`

- En tant que systeme, je veux generer un `verification_code` unique pour chaque `CoffretInstance` afin de permettre sa recherche a distance sans scan de QR code.
- Statut : `Termine`

Criteres d'acceptation :
- chaque nouvelle `CoffretInstance` recoit un `verification_code` unique ;
- le code est court et lisible a l'oral ;
- le code est persiste avec `verification_code_created_at`, indexe et contraint en unicite ;
- le code est affiche sur les supports utiles en complement du QR code client ;
- une collision est impossible ou geree par regeneration atomique.

### `PRD-041` Retrouver une `CoffretInstance` par code de verification

- En tant qu'operateur support, je veux retrouver une `CoffretInstance` a partir d'un `verification_code` dicte au telephone afin d'instruire rapidement la demande.
- Statut : `Termine`

Criteres d'acceptation :
- le back-office permet une recherche directe par `verification_code` ;
- une recherche sur un code inexistant retourne un resultat explicite ;
- la fiche de resultat expose au minimum le statut du coffret, sa date d'expiration et l'etat de consommation ;
- la fiche de resultat expose les prestations associees, groupees par commercant ;
- la recherche est exploitable sans scanner de QR code.

### `PRD-042` Verifier l'identite du commercant appelant

- En tant qu'operateur support, je veux verifier l'identite du commercant appelant avec une procedure minimale afin de limiter les usages abusifs du mode secours.
- Statut : `Termine`

Criteres d'acceptation :
- la procedure documentee exige plusieurs informations de verification ;
- la verification s'appuie au minimum sur le nom du commerce, la commune, le contact principal et le telephone de contact reference ;
- si l'appel ne provient pas du telephone reference, l'operateur doit renforcer la verification et choisir `A_CONTROLER` en cas de doute ;
- le back-office expose a l'operateur les informations necessaires a cette verification, sans recourir a une carte ou un QR commercant ;
- le resume des controles effectues est consigne dans la trace de validation secours ;
- une verification insuffisante empeche une autorisation directe.

### `PRD-043` Autoriser ou refuser une honorisation en mode secours

- En tant qu'operateur support, je veux pouvoir autoriser ou refuser une prestation en mode secours apres verification afin de traiter l'incident en conservant un cadre operatoire.
- Statut : `Termine`

Criteres d'acceptation :
- l'operateur peut enregistrer une decision `AUTORISE`, `REFUSE` ou `A_CONTROLER` ;
- le motif d'incident est obligatoire ;
- l'operateur doit selectionner explicitement le `statut_prestation_coffret_instance_id` cible a traiter dans la `CoffretInstance` ;
- une decision `AUTORISE` n'est possible que si la `CoffretInstance` est valide selon les regles metier ;
- une instance expiree, inconnue ou dont la prestation cible est deja consommee est refusee ou remontee en controle selon la regle definie ;
- une `CoffretInstance` deja partiellement consommee reste eligible si la prestation du commercant appelant n'a pas encore ete validee ;
- un rejeu de la meme demande de secours ne doit pas produire de double validation metier ni de double trace incoherente ;
- aucune seconde validation `AUTORISE` ne peut etre executee pour le meme `statut_prestation_coffret_instance_id` ;
- la decision est attribuee a un operateur identifie.

### `PRD-044` Tracer les usages du mode secours

- En tant qu'administrateur, je veux disposer d'un historique des validations secours afin d'auditer les usages et d'identifier les abus ou incidents recurrents.
- Statut : `Termine`

Criteres d'acceptation :
- chaque demande en mode secours cree une trace exploitable ;
- la trace contient la date, l'operateur, le commercant, la `CoffretInstance`, la prestation cible, le motif et la decision ;
- les evenements `validation.secours.authorized`, `validation.secours.refused`, `validation.secours.control_requested` et `validation.secours.failed` sont emis selon l'issue du traitement ;
- l'historique est consultable en back-office ;
- les usages du mode secours sont distinguables des validations nominales.

### `PRD-045` Documenter la procedure de secours

- En tant qu'exploitant, je veux disposer d'une procedure documentee pour le commercant et le support afin d'uniformiser le traitement des incidents.
- Statut : `Termine`

Criteres d'acceptation :
- une procedure commercant explique quand et comment contacter le support ;
- une procedure operateur decrit les etapes de verification et de decision ;
- la procedure ops/support est documentee dans [docs/ops/exploitation/valider-prestation-mode-secours.md](../../exploitation/exploitation/valider-prestation-mode-secours.md) ;
- la documentation precise le caractere exceptionnel du mode secours ;
- les cas de refus, de doute et de controle manuel sont explicitement decrits.

## Back-office cible

Vue ou action `Mode secours` :
- recherche par `verification_code` ;
- affichage du statut de la `CoffretInstance` ;
- affichage des informations minimales du commercant et du coffret ;
- affichage des prestations associees, regroupees par commercant ;
- selection explicite de la prestation cible avant toute decision `AUTORISE` ;
- generation ou transport d'un `secours_request_id` unique pour chaque action de validation secours ;
- saisie du motif d'incident ;
- saisie du resume de verification commercant ;
- enregistrement d'une decision `AUTORISE`, `REFUSE` ou `A_CONTROLER`.

Informations minimales attendues sur la fiche :
- `CoffretInstance`
- statut
- date d'expiration
- etat des prestations associees
- historique recent si utile
- liste des commercants lies au coffret avec les informations utiles a la verification telephonique :
  - nom commercant
  - numero de telephone
  - commune
  - contact principal
- liste des prestations associees a la `CoffretInstance`, groupees par commercant, avec indication claire des prestations deja validees et restant a valider

Contraintes d'affichage :
- le mode secours ne suppose jamais un commercant unique sur le coffret ;
- si plusieurs commercants sont lies au coffret, ils doivent etre tous affiches ;
- si un commercant est lie a plusieurs prestations dans la `CoffretInstance`, elles doivent etre toutes affichees et distinguables ;
- l'operateur doit pouvoir identifier rapidement si le commercant appelant fait bien partie des commercants lies au coffret.

## Regles de securite

- Le mode secours est reserve aux situations exceptionnelles d'indisponibilite ou d'incident declare.
- Le `verification_code` permet d'identifier une `CoffretInstance` mais ne constitue pas a lui seul une preuve de validite.
- Une verification commercant insuffisante bloque l'autorisation directe.
- Le mode secours ne permet de valider que la prestation rattachee au commercant appelant ; il ne permet jamais de valider globalement tout le coffret.
- Une decision `AUTORISE` exige une selection explicite de la prestation cible a valider dans la `CoffretInstance`.
- Une validation secours est idempotente : le rejeu de la meme demande ne doit jamais produire un double effet metier.
- Le traitement d'une validation secours `AUTORISE` est porte par un use case dedie execute dans le `UOW` existant.
- Toute decision en mode secours doit etre attribuee a un operateur identifie.
- Toute decision en mode secours doit comporter un motif d'incident.
- Les usages du mode secours doivent etre auditables a posteriori.
- En cas de doute, la decision par defaut est `REFUSE` ou `A_CONTROLER` selon la politique d'exploitation retenue.
- Le mode secours ne couvre pas une indisponibilite totale du backend, de la base de donnees ou du back-office Localeo ; ces cas relevent d'une procedure d'exploitation hors V1.

## Decisions produit actees

- Le mode secours retenu en V1 est un mode de secours telephonique avec intervention support, et non un mode offline autonome.
- Une `CoffretInstance` porte un `verification_code` dedie, visible et lisible a l'oral.
- Le `verification_code` sert d'identifiant de recherche, pas de secret d'authentification.
- L'identification du commercant repose sur plusieurs informations de verification et non sur un seul element.
- Aucun element issu de la carte, du QR ou du concept `qr_commercant` n'est utilise pour identifier le commercant.
- Une decision `AUTORISE` passe par un use case dedie de mode secours, idempotent, qui orchestre via le `UOW` existant la validation metier et l'ecriture de `ValidationSecours`.
- `ValidationSecours` reference explicitement le `statut_prestation_coffret_instance_id` cible afin de lever toute ambiguite dans les coffrets multi-commercants ou multi-prestations.
- Une `CoffretInstance` deja partiellement consommee peut etre traitee en mode secours si la prestation du commercant appelant reste a valider.
- Le mode secours est ouvert a toutes les prestations et a tous les commercants eligibles au parcours nominal, sans restriction de perimetre specifique en V1.
- Une decision `AUTORISE` execute la validation ; une decision `REFUSE` ou `A_CONTROLER` ne produit aucun effet de consommation.
- L'operateur support est trace par un identifiant texte stable si aucun modele admin dedie n'existe.
- Si un `admin_id` fiable est disponible dans le back-office, il est stocke ; sinon `operateur_admin_identifiant` texte est obligatoire.
- `verification_code_created_at` est ajoute en plus de `verification_code`.
- La procedure ops/support est portee par [docs/ops/exploitation/valider-prestation-mode-secours.md](../../exploitation/exploitation/valider-prestation-mode-secours.md).
- Les evenements d'audit retenus sont `validation.secours.authorized`, `validation.secours.refused`, `validation.secours.control_requested` et `validation.secours.failed`.
- La logique commune entre validation nominale et `TraiterValidationSecours` doit etre extraite ou partagee pour eviter la duplication des regles metier.
- Toute utilisation du mode secours doit laisser une trace d'audit dediee.

## Decisions a instruire

`Aucune decision bloquante identifiee pour la V1 apres alignement avec l'Epic 10.`

## Ordre d'implementation recommande

1. Ajouter `verification_code` sur `CoffretInstance` avec generation et contrainte d'unicite.
2. Afficher le `verification_code` sur les supports ou vues utiles.
3. Ajouter la recherche back-office par `verification_code`.
4. Ajouter le journal metier `ValidationSecours`.
5. Extraire ou partager la logique metier commune de validation nominale.
6. Ajouter le use case `TraiterValidationSecours`.
7. Ajouter l'action ou le workflow back-office de decision en mode secours.
8. Ajouter les audits du mode secours.
9. Rediger la procedure commercant.
10. Rediger la procedure operateur.
