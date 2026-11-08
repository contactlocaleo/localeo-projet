# EPIC 77 — Le Juste Prix Local

## Références et état

- **État produit : À faire**, cadrage du **6 novembre 2026**, selon la
  [roadmap commune](../README.md).
- Identifiant `77` vérifié dans les documents communs et les noms de fichiers
  des quatre dépôts applicatifs ; aucun cadrage ou moteur de Juste Prix trouvé.
- Demande : faire deviner aux habitants le prix d'un produit chez chaque
  commerçant participant, avec un seuil configurable d'éligibilité au gain.
- Socles : [moteur E55](../../specifications/moteur-animation/README.md),
  [participation commerçante E56](../../specifications/epic-56-validation-participation-commercants-animation/README.md),
  [Live E42](../../specifications/epic-42-localeo-live/README.md),
  [Animation E73](../../specifications/epic-73-animation-et-ou-coffrets/README.md),
  [validation PIN E70](../../specifications/epic-70-validation-pin/README.md) et
  [salariés Pro E72](../../specifications/epic-72-acces-salaries/README.md).
- Périmètre distinct : une estimation monétaire par commerce, un prix de
  référence, une tolérance et une réponse définitive constituent une mécanique
  différente de la chasse, des [mots croisés E75](epic-75-mots-croises-assistes-ia-backlog.md)
  et de la [tombola publique E74](../en-cours/epic-74-tombola-publique-backlog.md).
  Leurs règles et états produit sont conservés.
- Ce backlog est le cadrage canonique. Aucun dossier de spécification détaillée,
  code de modèle enregistré, migration, test métier ou livraison E77 à ce stade.

## Problème, acteurs et résultat attendu

Une commune ou une organisation souhaite faire découvrir les produits de ses
commerçants par un défi simple : **« À ton avis, combien coûte ce produit ? »**
L'habitant retrouve le jeu dans Localeo Live, découvre un produit par commerce,
propose un prix et suit sa progression vers le seuil donnant accès au tirage.
Il peut participer en ligne ou avec des passages commerçants validés, selon le
mode annoncé par le gestionnaire de l'animation.

**Acteurs :** gestionnaire organisateur dans Localeo Animation ; commerçant
principal dans Localeo Pro ; salarié habilité pour les seules validations déjà
autorisées ; habitant dans Live ; opérateur Localeo dans l'ERP pour le support
et la supervision selon ses droits actuels.

**Exemple illustratif, pas une configuration par défaut :** cinq commerces,
un produit chacun, seuil de trois prix trouvés. Pour un prix de référence de
12,50 € et une tolérance de 0,50 €, une estimation de 12,00 € à 13,00 € est
correcte, bornes comprises. Trois commerces distincts réussis rendent éligible
au tirage. Si le gestionnaire a activé les passages, les trois réussites doivent
aussi disposer de leurs validations commerçantes. Les deux autres commerces
ne deviennent pas obligatoires du seul fait de participer à l'animation.

## Décisions acquises et propositions

| Référence | Nature | Règle |
| --- | --- | --- |
| E77-DEC-01 | Demande du 6 novembre | Nouveau jeu « Le Juste Prix Local » ; exactement un produit et un juste prix par commerçant retenu pour une édition |
| E77-DEC-02 | Confirmation utilisateur | Le seuil est un nombre minimal de commerçants distincts dont le prix a été trouvé ; pas un score de proximité au prix ni un classement du plus proche |
| E77-DEC-03 | Confirmation utilisateur | Tolérance en euros configurable ; 0 € impose le prix exact, au centime. La portée de la tolérance reste à préciser en ARB-01 |
| E77-DEC-04 | Confirmation utilisateur | Atteindre le seuil donne accès au tirage au sort existant ; aucun gain automatique à cet instant |
| E77-DEC-05 | Confirmation utilisateur | Une seule réponse après confirmation par participant et commerçant ; modification libre avant confirmation définitive |
| E77-DEC-06 | Réponse explicite de l'utilisateur | Le gestionnaire choisit si un passage validé par le commerçant est requis pour comptabiliser une bonne réponse. Ce choix est propre à cette animation et annoncé avant participation |
| E77-DEC-07 | Confirmation utilisateur | Le commerçant propose le produit et son prix de référence dans Pro ; l'organisateur valide avant publication |
| E77-PROP-01 | Proposition à spécifier | Prix TTC en euros, unité/format précis et représentation monétaire exacte au centime ; pas de comparaison monétaire flottante |
| E77-PROP-02 | Proposition à arbitrer, ARB-02 | Retour immédiat « trouvé / non trouvé », sans révéler le prix exact ni un indice plus/moins avant la clôture |
| E77-PROP-03 | Proposition de réutilisation | Inscription, règlement, accès personnel Live, tirage, trois modes de lots et remise sur le socle existant ; aucune billetterie payante habitant ajoutée |

La configuration du seuil et celle de la tolérance sont **deux paramètres
distincts**. Le choix de passages facultatifs n'est pas un droit de modifier
les règles des chasses, mots croisés ou tombolas déjà définies.

## Périmètre

### Inclus

- Modèle identifiable dans le catalogue et l'assistant de Localeo Animation,
  activé seulement lorsque son offre, ses droits et ses consommateurs sont prêts.
  Le code moteur sera arrêté lors de la spécification.
- Assistant guidé : dates, commerçants retenus, produits/prix approuvés,
  tolérance applicable, seuil, mode de passage, règlement et dotation.
- Proposition commerçante : nom du produit, description et unité/format
  nécessaires pour éviter les ambiguïtés, prix de référence, visuel fourni
  facultatif ; états « à compléter / proposé / validé / à corriger » à préciser.
- Révision de la proposition avant publication, puis validation de sa version
  par l'organisateur. Le prix actuel du magasin n'actualise pas automatiquement
  la référence de jeu déjà publiée.
- Live mobile : fiche du jeu, liste des commerçants et accès à leurs profils,
  fiche produit, saisie du prix en euros, récapitulatif et confirmation explicite,
  reprise du carnet et progression graphique vers l'éligibilité.
- Si les passages sont requis : réutilisation des validations commerçantes
  autorisées, y compris PIN/salariés lorsqu'ils sont déjà habilités. Un QR
  public facilite l'accès au jeu, mais ne prouve pas à lui seul une visite.
- Sans passage requis : une réponse correcte peut compter sans validation Pro.
- Éligibilité unique au tirage lorsque le nombre de commerces réussis atteint
  le seuil ; résultats, lots et historique dans les entrées Live existantes.
- Supports et liens directs orientés Live, sans renvoi vers une surface
  animations de la marketplace. Communication adaptée au mode de passage.
- Suivi de l'organisateur : produits à valider, participants, réponses,
  prix trouvés, passages manquants, qualifiés, tirage et lots remis ; droits
  de lecture et agrégations à définir lors de la spécification.

### Règles à préserver dans la conception

- Seuil entier entre 1 et le nombre de commerçants effectivement retenus et
  prêts à publier. Un commerçant ou plusieurs soumissions ne comptent jamais deux fois.
- Une estimation est correcte si son écart absolu au prix de référence ne
  dépasse pas la tolérance applicable, bornes comprises. Le serveur décide.
- Si le mode exige les passages, le commerce compte si **bonne réponse ET
  passage validé**. Les deux faits restent distincts ; un passage ne rend pas
  correcte une mauvaise réponse. Leur ordre, avant clôture, sera précisé.
- Produit, prix, tolérance, seuil et mode de passage appartiennent à la version
  publiée. Les erreurs après publication relèvent d'une reprise explicite,
  sans réévaluation silencieuse des réponses passées (ARB-03).
- Une réponse définitive est conservée, qu'elle soit correcte ou non ; double
  clic, réponse réseau perdue et reprises techniques ne consomment pas un
  deuxième essai et ne créent pas de deuxième chance au tirage.
- Les prix de référence/solutions restent hors des API, QR et supports publics
  tant que leur révélation n'est pas autorisée. Chaque commerçant ne prépare
  que son produit ; l'organisateur ne gère que son périmètre autorisé.
- Les périodes de jeu, de validation et de tirage suivent les statuts et bornes
  du domaine ; la consultation d'une animation future n'autorise pas à jouer.
- Les réponses et l'éligibilité ne sont jamais calculées exclusivement en
  JavaScript. Aucun paiement, lot supplémentaire ou notification commerciale
  implicite n'est provoqué par une estimation.
- Interface simple, immersive et accessible : montants lisibles, clavier
  numérique mobile, confirmation compréhensible, progression et états avec
  textes/pictogrammes, sans dépendre d'une couleur seule. Utiliser le visuel
  réellement fourni, sans inventer d'illustration de produit.
- Lectures et écritures bornées : filtrage/pagination serveur, aucune recherche
  de participant par chargement de toute l'animation ; bilans agrégés. Prévoir
  budgets et preuves selon la [convention de performance](../../architecture/transverse/performance-volumetrie.md).

### Hors périmètre

- Classement au plus proche, enchères, achat requis pour proposer un prix,
  bonus de chances pour les commerçants supplémentaires ou gain automatique.
- Plusieurs produits ou plusieurs énigmes de prix pour un même commerçant
  dans la même édition ; devises multiples ou paiement de l'estimation.
- Vérification automatique des prix en caisse, branchement e-commerce, IA
  décidant d'une réponse ou alimentation des prix depuis le CRM.
- Nouveau moteur de tirage, nouveau portefeuille de lots ou nouveau compte
  habitant ; migration automatique des anciennes animations vers ce modèle.
- Révélation publique automatique du prix après chaque réponse, changement
  silencieux des règles publiées ou modification des autres jeux.

## User stories

| ID | Acteur et besoin | Critères |
| --- | --- | --- |
| E77-US01 | Organisateur : créer et configurer le jeu avec une prochaine action claire | CA-01 à 03 |
| E77-US02 | Commerçant : proposer un produit précis et son prix ; organisateur : l'approuver | CA-04 à 05 |
| E77-US03 | Habitant : découvrir les commerces et confirmer une estimation sur mobile | CA-06 à 10 |
| E77-US04 | Commerçant/habitant : valider et suivre les passages lorsque le mode le demande | CA-11 à 12 |
| E77-US05 | Habitant : suivre son seuil d'éligibilité et reprendre son parcours | CA-13 à 14 |
| E77-US06 | Organisateur : clôturer, tirer les gagnants et remettre les lots via les parcours existants | CA-15 à 16 |
| E77-US07 | Organisateur/opérateur : traiter les erreurs et suivre l'animation sans altérer les règles publiées | CA-17 à 18 |
| E77-US08 | Localeo : intégrer le modèle sans régression, avec contrats et preuves proportionnées | CA-19 à 20 |

## Critères d'acceptation cibles

Les **20 critères E77-CA-01 à E77-CA-20** sont des cibles, pas des tests passés.
Les propositions et arbitrages encore ouverts ne sont pas présentés comme acquis.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E77-CA-01 | Organisateur habilité, modèle disponible pour sa souscription | Choisir « Le Juste Prix Local » | Brouillon de ce type avec libellés et assistant propres ; aucune conversion d'une autre animation |
| E77-CA-02 | Brouillon avec N commerces effectivement retenus | Régler seuil, tolérance et mode de passage | Seuil 1..N et tolérance monétaire non négative ; publication impossible si paramètres manquants, incohérents ou seuil inatteignable |
| E77-CA-03 | Gestionnaire préparant la publication | Consulter le récapitulatif | Commerces, produits approuvés, conditions du jeu, seuil, tolérance et passage requis/non requis explicites ; points bloquants et prochaine action visibles |
| E77-CA-04 | Commerçant autorisé pour l'animation | Proposer ou corriger son produit/prix dans Pro | Une proposition courante pour son commerce ; produit identifiable, montant valide et visuel fourni facultatif ; ni prix des autres commerces ni approbation organisatrice usurpée |
| E77-CA-05 | Organisateur, propositions commerçantes reçues | Valider puis publier | Un produit/prix approuvé par commerce publié ; aucune proposition modifiée ou incomplète approuvée implicitement ; version jouée figée |
| E77-CA-06 | Habitant avant, pendant ou après la période de jeu | Ouvrir une fiche puis tenter de répondre | Consultation selon visibilité ; soumission acceptée uniquement pendant la période ouverte et dans les statuts autorisés |
| E77-CA-07 | Habitant inscrit selon le parcours retenu | Ouvrir un lien ou QR d'animation/commerce | Arrivée dans Live sur la bonne animation et le bon produit ; accès à la liste des commerçants et à leurs profils, reprise selon les accès existants |
| E77-CA-08 | Participant sans réponse définitive pour ce commerce | Saisir, modifier puis confirmer son prix | Saisie en euros, erreurs explicites, récapitulatif avant engagement ; une seule estimation définitive pour ce couple participant/commerce |
| E77-CA-09 | Réponse soumise au serveur | Évaluer le montant | Écart absolu comparé à la tolérance ; les deux bornes sont acceptées, l'écart supérieur refusé, 0 € exige l'égalité au centime ; précision monétaire conservée |
| E77-CA-10 | Réponse déjà enregistrée, double clic ou incident réseau | Réessayer la même commande ou envoyer une autre estimation | Rejeu retrouve le résultat ; nouvelle réponse définitive refusée sans écraser la première ni ajouter d'essai ou de chance |
| E77-CA-11 | Animation avec passages requis | Trouver le prix puis faire valider le passage, ou inversement si autorisé | Le commerce compte seulement quand les deux conditions sont remplies ; mauvais prix, validation étrangère et QR libre-service seul ne donnent aucun point |
| E77-CA-12 | Animation sans passages requis | Confirmer une estimation correcte | Le commerce compte sans validation Pro ; aucune exigence de passage héritée de la chasse ou des mots croisés |
| E77-CA-13 | Participant avec X commerces réussis | Consulter sa progression puis atteindre le seuil | Compteur de commerces distincts, seuil et prochaines actions visibles ; éligible au seuil, sans gain automatique ni chances supplémentaires au-delà |
| E77-CA-14 | Participant reprenant son carnet | Revenir dans Live ou recharger la page | Réponses définitives, passages, progression et éligibilité conservés ; pas de nouveau compte ou duplication de participation |
| E77-CA-15 | Animation clôturée avec qualifiés | Préparer et exécuter le tirage | Population éligible figée selon les règles retenues ; une chance par participant qualifié, refus pour les non-éligibles ; moteur existant réutilisé |
| E77-CA-16 | Gagnant avec dotation existante compatible | Consulter puis retirer/utiliser son lot | Résultat et lot dans Live, remise/consommation et droits habituels ; prix du produit deviné et valeur du lot restent distincts |
| E77-CA-17 | Erreur de produit/prix ou commerce indisponible après publication | Demander une correction | Diagnostic et procédure explicites selon ARB-03 ; pas d'édition silencieuse du prix, de baisse du seuil ou de disqualification rétroactive ; historique conservé |
| E77-CA-18 | Organisateur/opérateur autorisé | Suivre préparation, jeu et bilan | Produits à approuver, réponses, réussites, passages manquants, qualifiés et gains lisibles, paginés/agrégés ; pas de prix privés dans une restitution publique |
| E77-CA-19 | Client Live ancien ou requête manipulée | Appeler le jeu, accéder à un autre commerce ou demander le prix de référence | Compatibilité explicite, droits et contrôles serveur ; pas de solution dans un DTO public ni de repli vers les règles d'un autre moteur ; aucune régression des jeux existants |
| E77-CA-20 | Jeux synthétiques et implémentation future | Exécuter tests domaine, intégration et parcours PC/mobile | Preuves des deux modes, limites/tolérance, seuil, réponse unique, concurrence/reprise, autorisations, confidentialité, tirage, pagination et capacité ; contrôles non exécutés distincts des réussites |

## Impacts à instruire

| Sujet | Analyse initiale et sources |
| --- | --- |
| Domaine backend | **Concerné** : nouveau modèle ; validation de configuration, commande d'estimation, réponse unique et qualification. Le registre actuel et le passeport donnent des précédents ; ne pas placer le calcul dans Pro/Live |
| Backend/ERP et Animation | **Concernés** : catalogue, accès au modèle, assistant, validation organisatrice, contrôle de publication, support, bilan et correction d'incident |
| Localeo Pro | **Concerné** : proposition du produit/prix propre au commerce et, si requis, validation des passages ; préserver les droits principal/salarié et le périmètre Animation seul |
| Marketplace/Live | **Concerné pour Live** : renderer du défi, saisie/confirmation, progression et résultats. **Sans refonte de la marketplace Coffrets**, le lien vers Live est conservé |
| API et consommateurs | **Concernés** : contrats de configuration/jeu et projections publiques/privées, erreurs et compatibilité ; sources canoniques et générateurs backend, contrats embarqués auprès des consommateurs |
| Persistance et migrations | **À examiner** : stocker proposition/version approuvée, prix figé, estimation définitive, résultat et lien à la preuve de passage ; unicité et concurrence. Aucun numéro SQL réservé au cadrage |
| Démonstration et fixtures | **Concernées** : modes avec/sans passages, au seuil et sous seuil, prix exact/tolérance, mauvais prix définitif, compte commerçant limité, tirage et lots ; politique de transfert à préciser si de nouvelles tables sont ajoutées |
| Documentation fonctionnelle | **Concernée** : guides organisateur, Pro et Live, règles lisibles et supports/QR/flyer contextualisés ; pas de documentation concurrente par dépôt |
| Exploitation et déploiement | **À examiner** : activation du modèle et offre, livraison API/consommateurs, reprise d'incident, diagnostics sans solutions publiques, quotas et conservation des réponses |
| Coût, volume et trafic | **Concerné** : estimation au plus une fois par participant/commerce, sauvegarde/rejeu, listes paginées et bilan agrégé ; limites et budgets à chiffrer avant développement/activation, mesures N/10N et charge mixte prévues |

## Arbitrages à achever à la spécification

Les décisions DEC-01 à 07 sont acquises. Les sujets ci-dessous restent ouverts
et ne bloquent pas l'existence du cadrage ; ils bloquent leurs comportements
dépendants avant implémentation.

| Référence | Décision attendue et proposition | Périmètre dépendant |
| --- | --- | --- |
| E77-ARB-01 | Tolérance unique pour l'animation ou réglage par produit/commerce ? Recommandation initiale : une valeur commune explicite pour une V1 simple ; ne pas présenter cette portée comme validée | Formulaire et comparaison monétaire publiée |
| E77-ARB-02 | Quand montrer réussite/échec et révéler le vrai prix ? Recommandation : réussite/échec immédiat, aucun indice plus/moins, révélation exacte après clôture selon le règlement | Retour joueur, projections et supports |
| E77-ARB-03 | Produit/prix erroné, produit indisponible ou commerce retiré après publication : suspension/reprise identique, annulation et nouvelle édition ? Définir aussi l'ordre réponse/passage et le gel à clôture ; aucune seconde estimation implicite | Reprise, équité et support |
| E77-ARB-04 | Type standard inclus ou module organisateur distinct ? Tarif HT, durée, quota, accompagnement et compatibilité des dotations à retenir. Ne pas recopier automatiquement les 190 € HT/12 mois/5 publications d'E75 | Offre, habilitations et publication commerciale |

## Passage à la spécification

Le besoin, les acteurs et les sept décisions acquises permettent de spécifier
les parcours indépendants. Instruire les quatre arbitrages avant les branches
qui en dépendent, puis créer le dossier canonique dans l'index des spécifications
selon le [cycle d'epic](../../organisation/cycle-epic.md), sans recopier ce backlog
dans les applications.

La future spécification reliera les 20 critères aux responsabilités, contrats,
droits, migrations, fixtures et preuves attendues. La clôture reposera sur des
tests unitaires, d'intégration, fonctionnels et de capacité, sans transformer
un pilote ou une validation externe en condition implicite. Aucun de ces tests
n'est annoncé comme exécuté par ce cadrage.
