# E73 — Automatiser la recette métier sur TEST

Mise à jour du **22 octobre 2026**. Cible retenue : **environnement de test avec un nouveau jeu dédié**. Le lanceur et la préparation additive existent dans `localeo-backend/scripts/recette_e73`. La couverture des 130 scénarios du [plan métier](recette-metier.md) reste partielle : un scénario référencé au catalogue n’est pas nécessairement automatisé, et un parcours codé n’est pas encore une preuve de réussite distante.

## État concret et commandes

Le lanceur lit les 130 identifiants et leurs étapes depuis la recette canonique, filtre par RM ou fonctionnalité, puis écrit un rapport HTML/JSON privé. Les origines des cinq applications sont limitées aux hôtes TEST explicites. Les contextes navigateur sont séparés par acteur ; les réponses métier ne sont pas remplacées. Les fichiers, mots de passe, cookies et liens restent sous `localeo-backend/demonstrations/prive/recette-e73/`, ignoré par Git. Aucun déploiement ni migration n’est effectué.

Depuis la racine de `localeo-backend`, avec Node et Playwright disponibles dans ce dépôt ou le dépôt Marketplace voisin, puis Python pour la préparation :

```powershell
# Une nouvelle campagne, hors ligne ; conserver ensuite son chemin affiché.
node scripts/recette_e73/cli.mjs init --mailbox <boite-controlee>
$recetteConfig = 'demonstrations/prive/recette-e73/<campagne>/config.json'
$recetteManifest = 'demonstrations/prive/recette-e73/<campagne>/manifest.json'

# Vérifier les hôtes, puis authentifier l’opérateur et lire les références.
node scripts/recette_e73/cli.mjs preflight --config $recetteConfig
node scripts/recette_e73/prepare-access.mjs $recetteConfig

# Plan sans effet distant, puis création/reprise additive explicitement demandée.
python scripts/recette_e73/seed.py --config $recetteConfig --output $recetteManifest
python scripts/recette_e73/seed.py --config $recetteConfig --output $recetteManifest --apply
node scripts/recette_e73/fixtures.mjs $recetteConfig

# Exécuter seulement les scénarios dont les données ont été préparées.
node scripts/recette_e73/cli.mjs list --select F02
node scripts/recette_e73/cli.mjs run --config $recetteConfig --select RM-02-02 --execute
```

`prepare-access.mjs` lit uniquement les accès ERP dans le fichier privé `.env.test`, se connecte et enregistre sa session privée ; il ne crée pas de données métier. Il faut le relancer lorsque cette session expire. Les communes sont sélectionnées explicitement par `seed.commune_names` et doivent exister. Le seed journalise les commandes avant leur émission et conserve leurs clés de reprise ; ne pas supprimer ce journal pour contourner un refus. Une reprise du seed n’est pas un reset de la base. Les scénarios navigateur, eux, peuvent consommer ou modifier leurs objets : utiliser les références dédiées à chaque scénario et lire son dernier résultat avant de le relancer.

Le manifeste conserve les prérequis encore absents. Les comptes non activés sont bloqués avant connexion. Les lignes CSV/XLSX locales générées ne sont pas des commerces créés ; leurs identités sont synthétiques et ne constituent pas une vérification externe de SIRET. Le seed ne fabrique pas de dates, d’encaissements, d’acceptations ni de statuts d’onboarding.

### Invitations et lecture Gmail

L’opérateur a choisi une connexion Gmail autorisée pour lire les emails des alias de recette. L’installation et l’autorisation Google restent nécessaires avant toute lecture réelle. La présence d’une adresse dans la configuration ne suffit pas. La connexion de l’assistant ne fournit pas automatiquement des identifiants OAuth à un processus Node autonome : cette première intégration reste pilotée par l’assistant connecté, sans configuration CI permanente.

Les messages effectivement reçus sont exportés dans un fichier privé de la campagne, au format `{id, recipient, receivedAt, text, html}` (message, tableau ou enveloppe `messages`). L’import local valide le destinataire exact, la date, l’origine Animation TEST, l’unicité du lien et les doublons, puis produit les fichiers attendus par les tests :

```powershell
node scripts/recette_e73/inbox.mjs --config $recetteConfig --input 'demonstrations/prive/recette-e73/<campagne>/gmail-recus.json' --seed-invitations
python scripts/recette_e73/seed.py --config $recetteConfig --output $recetteManifest --apply
```

L’option `--seed-invitations` prépare les tokens réellement reçus pour les acteurs du seed ; elle ne les consomme pas et n’active aucun compte. Les invitations supplémentaires d’un même compte dans une autre organisation doivent être rattachées explicitement à la bonne opération. Ne jamais récupérer les tokens depuis les tables pour remplacer la réception Gmail. Ne pas transmettre les fichiers privés dans un rapport partageable.

### Première campagne TEST

Deux organisations synthétiques A/B ont été créées et leurs demandes validées par les parcours ERP ordinaires ; les invitations des responsables ont été enregistrées. Leur réception et leur acceptation ne sont pas encore prouvées. Les références communales utilisées sont Latresne, Carignan-de-Bordeaux et Bouliac ; Martignas-sur-Jalle n’était pas présente dans les références TEST et aucune commune existante n’a été modifiée.

La première création de commerce a échoué avec HTTP 409 « Conflit de donnees : rechargez la ressource. ». La recherche bornée par préfixe de campagne ne retrouve aucun commerce. Le rejeu de la même commande avec la même clé conserve le refus ; corrélation `LOC-01d7f7d1-6475-4201-acf8-67f47e5b805a`. Sa cause SQL exacte reste à déterminer dans les logs serveur ; aucune contrainte n’a été contournée. Souscriptions, modules, commerces actifs, animations, participants et bons restent à préparer.

Le premier passage du catalogue complet a produit **19 Bloqués et 111 Non automatisés, aucun succès métier automatique**. Ce rapport initial précède les compléments de scénarios suivants. Il reste conservé dans le dossier privé de campagne ; les réussites manuelles déjà déclarées dans la recette ne sont pas modifiées.

### Parcours actuellement raccordés

Les handlers ci-dessous exécutent des actions et assertions réelles lorsque leurs prérequis sont disponibles. Plusieurs sont encore partiels et terminent alors explicitement en `BLOQUE`. Aucun n’est déclaré réussi sur TEST à cette étape.

| Module de la suite | Identifiants raccordés | Limites principales |
| --- | --- | --- |
| `accounts.mjs` | RM-01-01 à 04 ; RM-02-01 à 06 | Réception Gmail, identités actives, états datés et variantes accompagnées. L’autorité d’un demandeur reste une preuve humaine. |
| `features.mjs` | RM-05-01 ; RM-09-01 ; RM-10-01 ; RM-16-01/02/04/05 ; RM-21-01/03 | Périmètres Pro, dotations, imports et bilan ; certaines variantes restent partielles. Import confirmé exige un worker actif, bilan exige une référence chiffrée indépendante. |
| `commercial.mjs` | RM-06-01/02 ; RM-07-06 ; RM-08-01/02 | Catalogue, devis, essais, cadeaux et facturation. RM-06-01 et RM-07-06 restent partiels ; pas de paiement ni de modification du catalogue global. |
| `lots.mjs` | RM-10-03 ; RM-11-02/03/05 ; RM-12-01 ; RM-13-01 | Exemplaires, concurrence, versions, surplus, tirage et remise. RM-10-03 reste partiel ; RM-13-01 utilise la saisie du contenu QR et ne prouve pas la capture optique par caméra. |
| `support.mjs` | RM-19-01/02/03 | Échanges réels, échéances préparées et confidentialité ; calendrier et dossiers synthétiques doivent être préparés. L’accès direct à un dossier étranger est vérifié par son lien API lorsque le frontend ne propose pas de lien profond. |

Cela représente **33 identifiants avec un parcours complet ou partiel codé**, et **97 sans parcours intégré**. Les états et UUID nécessaires sont documentés en tête de chaque module dans les champs `manifest.resources`. Les scripts refusent d’inventer un objet manquant. Les mutations de souscriptions, lots et Support sont journalisées et leur rejeu est bloqué après démarrage : examiner le résultat avant de préparer un nouveau jeu.

Contrôles exécutés le 22 octobre : **94 tests Node de l’outillage réussis**, **664 tests Python ciblés et d’architecture réussis**, contrôle des guides sans erreur et **130 sources documentaires vérifiées**. Le passage distant actualisé conserve **33 Bloqués et 97 Non automatisés**. Les cinq hôtes TEST répondent HTTP 200 ; `/sante` annonce `release: V1`, sans SHA exploitable pour attester l’identité du code hébergé. Ces preuves locales et ces précontrôles ne constituent pas une validation métier de l’epic.

## Résultat attendu

Exécuter un scénario par son identifiant RM, une fiche fonctionnelle ou toute la campagne. Chaque variante possède ses prérequis, ses actions et ses assertions observables. Un parcours passe uniquement si toutes ses assertions réussissent. Lancer une route API avec succès ne remplace pas la vérification de l’action dans l’application.

Le rapport conserve, par variante : identifiant de campagne, versions déployées connues, surface, rôle synthétique, objets du jeu, prérequis contrôlés, étape atteinte, observations, durée et verdict. Les résultats automatiques sont séparés des validations humaines ; RM-01-01 et RM-01-02 conservent leur réussite manuelle déjà déclarée.

## Nouveau jeu et séparation des données

- Une campagne reçoit un identifiant unique et un préfixe de noms `RECETTE-E73-<campagne>`.
- Préparer deux organisations A/B et trois rattachements communaux A1/A2/B1, les profils Responsable/Gestionnaire/Lecteur et les délégations Achat/Import/Communication distinctes.
- Préparer les commerces Animation, Coffrets, mixtes, salariés et cas de retrait/suspension, les trois dotations, souscriptions/modules, participants, bons et fichiers décrits dans la recette.
- Décliner les états incompatibles sur des objets différents ; conserver les identifiants créés dans un manifeste privé, afin de reprendre sans créer de doublons.
- L’utilisateur a désigné la boîte de recette. Sa valeur et les alias par campagne sont placés dans la configuration privée, jamais dans les sources de tests ou rapports versionnés.
- Préparer les ajouts par les interfaces et services métier existants. Ne pas modifier directement les statuts des tables de TEST pour fabriquer un succès.
- Le générateur de démonstration actuel est un outil de remplacement de jeu : son installation/reset ne doit pas être utilisée pour cette préparation additive. Aucun remplacement du jeu actuellement installé n’est demandé.
- Ne pas modifier les paramètres globaux, tarifs actifs ou permissions de comptes existants pour faire passer un test. Les variantes qui ne peuvent pas être isolées par leurs données restent bloquées sur la cible partagée.

## Socle d’exécution et compléments attendus

1. **Précontrôle** : vérifier les URL TEST, accès, versions, rôles, rattachements, modules, fournisseurs de test, stockage et workers utiles. Une permission absente n’est pas contournée.
2. **Préparation** : créer/retrouver le jeu de la campagne, vérifier chaque état attendu, puis produire son manifeste privé. Les secrets restent hors Git et hors rapport.
3. **Navigation réelle** : Playwright avec un contexte navigateur par acteur, mobile et ordinateur pour les parcours concernés. Utiliser les frontends et le backend réellement déployés, sans intercepter leurs réponses métier pour les remplacer par des succès simulés.
4. **Effets différés** : suivre les états réels avec délais bornés ; un email en file d’attente ne prouve pas sa réception et un paiement retourné dans le navigateur ne prouve pas son encaissement confirmé.
5. **Verdicts** : Réussi automatique, Échec, Bloqué (prérequis précis), Non exécuté ou À valider humainement. Un scénario dont une variante reste non exécutée n’est pas validé globalement.
6. **Rapports privés** : HTML et JSON, captures utiles après masquage, références de corrélation expurgées. Les traces navigateur brutes contenant cookies, mots de passe, PIN, QR ou liens d’invitation ne sont pas des pièces partageables.
7. **Reprise** : rejouer uniquement les scénarios sélectionnés sur leurs objets dédiés. Ne pas réinitialiser automatiquement toute la base.

L’outillage exécutable transversal et les configurations privées appartiennent à `localeo-backend` ; les helpers et sélecteurs propres à une application peuvent rester auprès de ses tests. Les cinq dépôts restent indépendants, sans mode de recette ajouté au produit. Le suivi exhaustif des versions hébergées, les captures masquées et le raccordement de tous les scénarios restent à compléter ; le rapport actuel fournit les étapes réellement vérifiées et leurs motifs de blocage.

## Contrôles particuliers

**Emails.** Les invitations et réinitialisations doivent être envoyées aux alias contrôlés du jeu. Automatiser la récupération des liens exige un accès autorisé à la boîte ou un dispositif de réception de test. Une adresse email seule ne donne pas cet accès. En l’absence de lecture automatique, la récupération du lien reste assistée et le test est signalé comme tel. Ne pas extraire les secrets de la base pour remplacer la preuve de réception.

**Paiements et Push.** Utiliser uniquement les intégrations et destinataires de test. Distinguer état fournisseur, état applicatif, réception navigateur et lecture Live. La permission Push et la qualité sur appareil réel peuvent demander une vérification complémentaire.

**Temps.** Ne pas avancer l’horloge d’un environnement partagé. Utiliser des objets synthétiques préparés légalement dans leur cycle de vie, attendre la borne réelle ou exécuter la variante sur cible isolée avec horloge contrôlée. Le fuseau du navigateur peut être changé sans modifier l’horloge serveur.

**Incidents.** Une perte de réponse limitée au navigateur doit être déclenchée après prise en compte si c’est l’objet du test. Une requête annulée avant son traitement n’en apporte pas la preuve. Les arrêts de services, pannes fournisseur, restaurations et charge exigent une cible ou un créneau réservé.

**Humain.** Un script peut vérifier les champs et transitions, mais pas attester l’autorité d’un demandeur, la vérification sur le terrain ou l’avis UX de Localeo puis Martignas-sur-Jalle. Ne pas signer ces décisions à la place de leurs responsables.

## Inventaire des 130 scénarios

Les catégories désignent le mode cible, **pas une couverture déjà acquise** :

- **Navigateur** : interactions et assertions automatisables, sous réserve du jeu et des fournisseurs.
- **Préparation technique** : le navigateur est complété par des états datés, incidents, événements ou paramètres dédiés.
- **Part humaine** : automatisation des contrôles informatiques et résultat humain distinct.
- **Cible réservée** : scénario à isoler ou à exécuter dans un créneau explicitement réservé.

Cette table décrit la **cible de couverture**. Consulter les handlers de `scripts/recette_e73/scenarios` et le dernier rapport pour la couverture réelle ; un identifiant absent des handlers reçoit `NON_AUTOMATISE`, un parcours partiel ou privé d’un prérequis reçoit `BLOQUE`. Les tests unitaires des outils utilisent des doubles locaux et ne valident pas les applications hébergées.

| Test | Scénario de référence | Mode cible |
| --- | --- | --- |
| RM-01-01 | Demander une récupération avec l’email connu puis une adresse inconnue. | Navigateur |
| RM-01-02 | Utiliser un lien valide, définir le nouveau mot de passe, puis réutiliser le lien et tenter l’ancien mot de passe. | Navigateur |
| RM-01-03 | **Accompagné :** tester le lien avant puis à/après son échéance d’une heure. | Préparation technique |
| RM-01-04 | Changer le mot de passe connecté : d’abord avec une preuve d’identité erronée, puis correcte. | Navigateur |
| RM-02-01 | Déposer une demande d’organisation/communes, tenter d’utiliser A1 avant décision, puis faire valider le rattachement par Localeo. | Navigateur |
| RM-02-02 | Inviter un nouveau collaborateur Gestionnaire sur A1 ; accepter ; comparer à un Lecteur et à un Gestionnaire sans Achat/Import/Communication. | Navigateur |
| RM-02-03 | Inviter un email déjà associé à un compte, accepter avec ce compte ; renvoyer une autre invitation et essayer l’ancien lien ; essayer un lien expiré de 7 jours. | Préparation technique |
| RM-02-04 | Retirer une autorisation avec la session du collaborateur ouverte ; ajouter A2 à l’organisation sans l’ajouter au collaborateur ; tenter un lien direct hors droit. | Navigateur |
| RM-02-05 | Proposer un transfert de responsabilité ; tenter le départ du dernier responsable avant acceptation ; faire accepter le successeur actif. | Navigateur |
| RM-02-06 | **Accompagné :** simuler la perte des accès responsables et demander une récupération ; changer ensuite d’organisation avec le compte multi-organisations. | Part humaine |
| RM-03-01 | Faire demander/activer Animation par l’administrateur puis par le Backoffice habilité ; refaire sans habilitation et depuis Pro. | Navigateur |
| RM-03-02 | Ajouter Coffrets à un commerce Animation dont les compléments Coffrets sont incomplets ; terminer les prérequis puis activer. | Navigateur |
| RM-03-03 | **Accompagné :** deux opérateurs modifient la même fiche depuis des versions ouvertes avant la première modification. | Navigateur |
| RM-04-01 | Compléter identité, responsable, coordonnées et engagements Animation, sans prestations ni pièces bancaires Coffrets. | Navigateur |
| RM-04-02 | Omettre un prérequis Animation puis tenter l’activation ; le compléter et faire vérifier le dossier. | Navigateur |
| RM-04-03 | Demander ensuite Coffrets, y compris sur un dossier déjà clos ; vérifier les données et compléter les pièces propres au nouveau produit. | Navigateur |
| RM-04-04 | Préparer/envoyer les communications et conventions d’un dossier Animation seul puis mixte ; consulter leur suivi. | Navigateur |
| RM-05-01 | Ouvrir Pro avec chacun des trois périmètres ; parcourir menus et liens directs vers les fonctions absentes. | Navigateur |
| RM-05-02 | Connecter le salarié et scanner ; tenter administration, finances, gestion de droits et action d’un autre commerce. | Navigateur |
| RM-05-03 | Faire participer un commerce Animation seul à une animation dotée en coffrets et valider un passage. | Navigateur |
| RM-05-04 | Retirer Animation pendant une session ouverte ; tenter un nouvel engagement, un passage d’une participation déjà acceptée à une animation publiée et une remise de bon déjà attribué. | Navigateur |
| RM-05-05 | Retirer Coffrets avec une prestation déjà engagée dans un coffret vendu ; consulter règlement et historique, puis tenter un nouvel engagement. | Navigateur |
| RM-05-06 | Suspendre administrativement le commerce d’un jeu de continuité puis retenter QR/PIN. | Navigateur |
| RM-06-01 | Consulter forfait et modules d’une nouvelle souscription ; ouvrir les variantes de scénarios. | Navigateur |
| RM-06-02 | Vérifier les offres initiales et leur récapitulatif. | Navigateur |
| RM-06-03 | Avec le module acquis sur A1, tenter l’usage sur A2 ; consulter un droit inclus sans achat. | Navigateur |
| RM-06-04 | Modifier un prix/quota par l’administrateur ; consulter l’ancienne souscription puis préparer son renouvellement ; tenter la modification sans rôle administrateur. | Préparation technique |
| RM-07-01 | Préparer l’achat à six mois restants puis confirmer en mode test. | Préparation technique |
| RM-07-02 | Annuler/faire échouer un paiement ; revenir plusieurs fois sur le succès d’une autre commande ; **accompagné**, rejouer sa confirmation et tester un paiement tardif devenu incompatible. | Préparation technique |
| RM-07-03 | Renouveler avant puis après échéance ; examiner les modules repris au récapitulatif et en retirer un. | Préparation technique |
| RM-07-04 | Demander une montée en gamme en cours de période puis une baisse ; comparer échéance et usages déjà consommés. | Navigateur |
| RM-07-05 | Demander l’arrêt puis un remboursement de base ou module ; faire décider un montant partiel/total, et tenter un montant supérieur au solde remboursable. | Navigateur |
| RM-07-06 | Modifier les coordonnées de facturation avec Achat puis sans ; comparer ancienne facture et nouveau document ; ouvrir un document de B depuis A. | Navigateur |
| RM-08-01 | Accorder un essai de chaque module, puis ajuster durée/quota avec motif ; refaire sans habilitation. | Navigateur |
| RM-08-02 | Offrir les modules jusqu’à fin de base puis sur une durée plus courte. | Navigateur |
| RM-08-03 | Consommer sous un droit, ajouter un droit comparable puis laisser finir l’essai. | Préparation technique |
| RM-08-04 | **Accompagné :** répéter la fin des droits par expiration de module, retrait commercial anticipé, puis expiration de base. Tenter nouveaux usages et continuités. | Préparation technique |
| RM-08-05 | À expiration, ouvrir une campagne programmée non commencée puis renouveler le droit. | Préparation technique |
| RM-09-01 | Créer sans choisir la dotation, puis choisir Libre sans mode ; revenir en arrière dans le formulaire. | Navigateur |
| RM-09-02 | Choisir successivement les trois branches sur des brouillons sans engagement ; regarder l’assistant puis omettre un prérequis pertinent. | Navigateur |
| RM-09-03 | Publier une Libre/externe et une Libre/numérique correctement préparées sans commande Coffrets. | Navigateur |
| RM-09-04 | Engager une réservation/affectation puis essayer de changer de mode ; refaire après publication. | Navigateur |
| RM-09-05 | Acheter/consommer un coffret avec le commerce Coffrets seul ; exécuter publication, réservation/activation et envoi d’un gain d’animation Coffrets historique. | Navigateur |
| RM-10-01 | Créer « Lot A » quantité 2 puis « Lot B » quantité 1 ; saisir responsable/consignes et réordonner avant publication ; essayer quantité nulle. | Navigateur |
| RM-10-02 | Après attribution, lire l’email et le suivi avant toute réponse du gagnant. | Navigateur |
| RM-10-03 | Enregistrer contact, réponse puis remise déclarée ; corriger la déclaration avec motif ; essayer avec un simple commerçant/salarié. | Navigateur |
| RM-11-01 | Créer un modèle avec un seul commerce de remise, générer 3 exemplaires ; répéter la demande après une réponse incertaine accompagnée. | Préparation technique |
| RM-11-02 | Affecter un exemplaire à une animation ; tenter de l’affecter à la seconde, y compris depuis deux sessions simultanées. | Navigateur |
| RM-11-03 | Modifier la description du modèle après engagement ; essayer de changer le commerce de remise et d’utiliser un exemplaire de B1. | Navigateur |
| RM-11-04 | Choisir la durée 1, 90 puis 365 jours sur des brouillons ; essayer 0 et 366 ; publier et retenter l’édition. | Navigateur |
| RM-11-05 | Après attributions, libérer le surplus jamais attribué sur confirmation ; tenter la même chose avec un exemplaire attribué puis révoqué. | Navigateur |
| RM-12-01 | Préparer puis confirmer le tirage pour chacune des quatre populations (0, 2, 3 et 5 éligibles pour 3 lots). | Navigateur |
| RM-12-02 | Recharger, rejouer la confirmation ou reprendre après réponse perdue avec le référent. | Préparation technique |
| RM-12-03 | Lire l’email du gagnant et le bon numérique ; provoquer puis reprendre un échec d’envoi contrôlé. | Préparation technique |
| RM-12-04 | Retirer les droits du commerce numérique après publication mais avant tirage ; tenter la confirmation. | Navigateur |
| RM-12-05 | Tenter de remplacer un injoignable avant 14 jours sans refus ; enregistrer un refus explicite sur un autre gain ; remplacer après délai sur le premier. | Préparation technique |
| RM-12-06 | Remplacer un gagnant numérique non servi ; tester son ancien QR et ouvrir le nouveau bon du suppléant ; refaire avec un lot déjà consommé. | Navigateur |
| RM-12-07 | Épuiser la réserve puis demander explicitement un nouveau tirage de remplacement, avec puis sans candidat éligible non gagnant. | Navigateur |
| RM-13-01 | Scanner puis confirmer une remise avec le responsable ; répéter sur un autre bon avec le salarié. | Navigateur |
| RM-13-02 | Depuis le téléphone du gagnant, lancer la validation PIN et faire saisir le PIN par le commerce. | Part humaine |
| RM-13-03 | Rescanner/représenter un bon consommé puis consulter son historique. | Navigateur |
| RM-13-04 | Tester les variantes : autre commerce, bon expiré, révoqué, ancien QR, référence sans attribution et PIN bloqué. | Préparation technique |
| RM-13-05 | **Accompagné :** confirmer presque simultanément QR et PIN sur le même bon ; simuler une réponse réseau perdue après prise en compte puis rouvrir. | Préparation technique |
| RM-14-01 | Renvoyer un bon puis remplacer son QR ; comparer bénéficiaire, lot, échéance et tester l’ancien QR. | Navigateur |
| RM-14-02 | Prolonger avec motif un bon non consommé, même expiré ; tenter une échéance au-delà de 365 jours depuis attribution initiale. | Préparation technique |
| RM-14-03 | Révoquer avec motif un bon non consommé ; tester ensuite QR/PIN et consultation de l’historique. | Navigateur |
| RM-14-04 | Annuler avec motif une consommation enregistrée par erreur ; répéter sur un bon désormais expiré ou révoqué. | Préparation technique |
| RM-14-05 | **Accompagné :** lancer remise et révocation/remplacement en concurrence ; refaire sans permission de correction. | Navigateur |
| RM-15-01 | Publier une chasse avec droit actif puis une tombola/passeport ; tenter sans module et avec dernier crédit déjà consommé. | Part humaine |
| RM-15-02 | Déposer une demande complète de préparation puis consulter échéance et état. | Navigateur |
| RM-15-03 | Demander un complément côté Localeo, répondre côté client puis marquer prêt. | Navigateur |
| RM-15-04 | Ouvrir un dossier dépassant son délai, relancer puis faire communiquer une estimation révisée. | Préparation technique |
| RM-15-05 | Tenter de publier une chasse non prête ou non validée sur le terrain ; terminer les validations puis publier ; **accompagné**, deux publications sur le dernier crédit. | Part humaine |
| RM-15-06 | **Accompagné :** rendre le service de préparation technique E55 non prêt ; tenter l'achat du module ; examiner aussi une commande déjà confirmée avant l'indisponibilité. | Cible réservée |
| RM-16-01 | Télécharger le modèle ; charger CSV puis XLSX ; choisir une feuille et associer les colonnes avant aperçu. | Navigateur |
| RM-16-02 | Tester 100 puis 101 lignes ; fichier de 2 000 000 octets puis plus grand ; lignes invalides et formule dans un champ importable. | Navigateur |
| RM-16-03 | Charger email unique connu, email partagé, même email/SIRET différent, autre email/SIRET connu et deux lignes visant la même fiche. | Navigateur |
| RM-16-04 | Confirmer uniquement les lignes valides d’un fichier mixte ; télécharger le rapport ; tenter sans module ou permission. | Navigateur |
| RM-16-05 | Importer V1, modifier localement le téléphone ; dans V2 modifier ce téléphone différemment, changer un site non retouché localement, laisser une cellule vide et conserver un autre champ inchangé. | Navigateur |
| RM-16-06 | Après aperçu, faire modifier une fiche par un autre opérateur, puis confirmer ; changer email de contact, SIRET et commune dans des variantes distinctes. | Navigateur |
| RM-16-07 | **Accompagné :** interrompre après une ligne réussie, reprendre ; expirer le module avant démarrage puis pendant un autre import déjà commencé. | Préparation technique |
| RM-16-08 | **Accompagné :** consulter un import terminé/abandonné depuis plus de 30 jours, puis ses fiches et un réimport. | Préparation technique |
| RM-17-01 | Préparer un message pour chacune des audiences : tous, parcours non terminé, parcours terminé, gagnants ; essayer avant publication et après clôture +30 jours. | Préparation technique |
| RM-17-02 | Envoyer immédiatement aux comptes autorisant les messages, l’un avec Push et l’autre sans ; vérifier l'exclusion d'un participant opposé, d'un participant sans accord explicite et d'un simple abonné à la commune sans participation, même s'ils acceptent le Push ou les notifications automatiques. | Navigateur |
| RM-17-03 | Programmer en heure de Paris ; changer une préférence ou retirer la permission du gestionnaire avant démarrage. | Navigateur |
| RM-17-04 | Préparer/annuler des brouillons puis démarrer des campagnes jusqu’au quota, reprendre une campagne déjà commencée. | Navigateur |
| RM-17-05 | **Accompagné :** activer en fin de mois, passer le premier du mois Paris et une borne de changement d’heure ; comparer essai et achat. | Préparation technique |
| RM-17-06 | Laisser une programmation arriver avec quota épuisé ou droit expiré ; rétablir le droit/quota. | Préparation technique |
| RM-17-07 | Cibler la même personne dans deux campagnes/animations de A1 sur 24 h, avec plusieurs appareils ; attendre/préparer la fin de fenêtre. | Préparation technique |
| RM-17-08 | Cibler cette personne avec une troisième campagne distincte ; rejouer une reprise puis répéter sur plusieurs participants ; ajuster limite/multiplicateur côté ERP habilité. | Préparation technique |
| RM-17-09 | **Accompagné :** interrompre une campagne partiellement commencée, expirer le module puis reprendre, avec consentement retiré d’un destinataire restant. | Préparation technique |
| RM-17-10 | Préparer une campagne dont tous les destinataires sont exclus par préférence ou fréquence, puis lancer son traitement. | Navigateur |
| RM-17-11 | **Accompagné :** avec un seul crédit disponible, lancer deux campagnes ayant chacune un destinataire autorisé distinct. | Navigateur |
| RM-18-01 | Découvrir une animation, sa fiche, les commerçants et les modalités ; s’inscrire puis participer. | Navigateur |
| RM-18-02 | Ouvrir la fiche d’un commerce Animation seul et ses animations liées. | Navigateur |
| RM-18-03 | Ouvrir anciens QR/emails/carnets puis accéder au nouveau site ; suivre la reprise explicite si proposée. | Navigateur |
| RM-18-04 | Refuser la réactivation des notifications sur la nouvelle origine, puis participer et lire la messagerie ; refaire en acceptant. | Navigateur |
| RM-19-01 | Consulter l’aide puis créer une demande liée à une animation ; répondre côté Support puis client. | Navigateur |
| RM-19-02 | Comparer accusé automatique, cible de 2 jours ouvrés et première réponse humaine. | Préparation technique + Part humaine |
| RM-19-03 | Consulter avec A une demande de B et chercher les notes internes depuis le compte client. | Navigateur |
| RM-20-01 | Choisir les sections à réutiliser et de nouvelles dates ; créer l’édition dans A1 puis tenter A2. | Navigateur |
| RM-20-02 | Examiner participants, gains, QR, paiements, accords et consentements du brouillon ; tenter sa publication. | Navigateur |
| RM-20-03 | **Accompagné :** modifier la source après ouverture du formulaire ou reprendre une création après réponse perdue. | Préparation technique |
| RM-21-01 | Fixer les objectifs puis publier ; tenter de changer les objectifs ; comparer résultats et édition comparable. | Navigateur |
| RM-21-02 | Inscrire via les deux sources et sans source ; contrôler le bilan. | Navigateur |
| RM-21-03 | Vérifier les totaux avant/après remise, rescan, correction et remplacement à partir des références du jeu. | Navigateur |
| RM-21-04 | Après clôture, répondre dans Live avec note 1 puis 5 et commentaire facultatif ; tester 0/6, absence de réponse et accès avant clôture. | Navigateur |
| RM-22-01 | Retrouver chaque gain dans ERP/Support, filtrer par nature/commune, paginer et exporter la page affichée. | Navigateur |
| RM-22-02 | Vérifier les sommes financières des trois dotations ; tenter de sélectionner le commerce Animation seul comme fournisseur de prestation Coffrets dans Atelier. | Navigateur |
| RM-22-03 | Ouvrir une projection commerciale/CRM disponible et ses liens vers les parcours métier. | Navigateur |
| RM-23-01 | Consulter coûts par organisation puis commune/souscription/module selon données ; comparer au compte client. | Navigateur |
| RM-23-02 | **Accompagné :** faire passer le coût suivi de 79 à 80 puis 100 € ; rejouer les événements ; consulter l’organisation sans budget. | Préparation technique |
| RM-23-03 | Après dépassement, consulter abonnement, quotas et parcours de l’organisateur. | Navigateur |
| RM-24-01 | Demander un export avec collaborateur puis responsable ; suivre sa préparation et sa disponibilité. | Navigateur |
| RM-24-02 | Télécharger l’archive connecté ; ouvrir CSV, médias et guide ; comparer des références connues et les engagements en cours. | Navigateur |
| RM-24-03 | **Accompagné :** interrompre/reprendre la génération, tenter téléchargement sans rôle puis après 30 jours de disponibilité ; consulter les données sources. | Préparation technique |
| RM-24-04 | Demander séparément la fermeture comme responsable avec engagements ouverts ; tenter nouvel usage et fin des engagements existants. | Navigateur |
| RM-24-05 | Résoudre les engagements ou effectuer une reprise explicitement supportée et acceptée ; faire confirmer la fermeture par Localeo. | Part humaine |
| RM-25-01 | Examiner les commerces existants, saisir manuellement leurs périmètres puis tenter la bascule avec un commerce non revu ; terminer la revue. | Part humaine |
| RM-25-02 | **Accompagné :** pendant la vérification de bascule, créer/déplacer un commerce puis relire l’éligibilité. | Navigateur |
| RM-25-03 | **Accompagné :** générer un jeu synthétique puis le sauvegarder/restaurer sur cible isolée ; reprendre des parcours QR/PIN, import et permissions. | Cible réservée |
| RM-25-04 | Faire examiner le manifeste, les résultats des recettes et les anomalies ; faire valider l’UX par Localeo puis Martignas-sur-Jalle. | Part humaine |
| RM-25-05 | **Accompagné technique, sur cible isolée représentative :** restaurer base/fichiers/configuration et reprendre accès, participation, validation et remise ; chronométrer jusqu’aux contrôles terminés. | Cible réservée |
| RM-25-06 | Examiner un dossier sans preuve de restauration ou dont un objectif échoue. | Part humaine |
| RM-X-01 | Sur téléphone étroit puis ordinateur, parcourir les fonctions autorisées du portail ; côté interne, vérifier menus et retour accueil ERP ; côté public, découverte et participation. | Part humaine |
| RM-X-02 | Tester clavier seul, focus, zoom 200 %, erreurs de formulaire et états des lots sans s’appuyer uniquement sur leur couleur. | Part humaine |
| RM-X-03 | Depuis un appareil configuré hors France, lire échéances de bons, campagnes, factures et délais de service ; inclure un changement d’heure. | Préparation technique |
| RM-X-04 | Dans chaque action à effet, recharger après confirmation ; sur les jeux accompagnés, couper la réponse puis relire l’état ; ouvrir l’historique. | Préparation technique |
| RM-X-05 | Avec un lecteur puis un compte A, ouvrir un lien mémorisé vers écriture ou objet B ; retirer un droit pendant une session. | Navigateur |
| RM-X-06 | **Accompagné :** jeu de 10 communes et 10 000 participants au total ; 10 utilisateurs actifs simultanés. Paginer, filtrer, changer de commune, consulter bilan et poursuivre validation pendant import/campagne. Comparer au jeu réduit, mêmes actions. | Cible réservée |

## Ordre de réalisation

1. Socle, manifeste du jeu, précontrôles et rapport ; F01/F02 (comptes/invitations) pour éprouver les identités, emails et changements de session.
2. F03–F08 : périmètres, onboarding et droits commerciaux.
3. F09–F14 : trois dotations, tirage, remise QR/PIN et incidents.
4. F15–F17 : chasse, import/deltas et communication.
5. F18–F24 : parcours public, support, nouvelle édition, bilans, coûts, export et fermeture.
6. F25 et contrôles transverses : validations humaines, exercice réservé, charge et consolidation.

Chaque étape complète sa couverture et ses preuves avant d’étendre la campagne. Aucun commit, push, déploiement ou migration n’est déclenché par la préparation de cette automatisation.
