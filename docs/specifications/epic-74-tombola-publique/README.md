# E74 — Tombola publique sans commerçant

Spécification V1 du **3 novembre 2026**, fondée sur les choix explicites du porteur produit et l'examen des producteurs et consommateurs. L'état produit est **En cours** dans la [roadmap](../../roadmap/README.md). L’implémentation locale et les preuves sont suivies dans le bilan ; le modèle reste désactivé avant mise en service.

- [Backlog canonique : 8 US et 16 critères](../../roadmap/en-cours/epic-74-tombola-publique-backlog.md).
- [Architecture, contrats et livraison](architecture-contrats.md).
- [Matrice des preuves et recette](verification.md).

## Harmonisation des inscriptions — 11 novembre 2026

La demande produit harmonise toutes les animations sur la tombola commerçante :
**nom, prénom, e-mail et téléphone obligatoires**, dans cet ordre et avec les mêmes
libellés, claviers et règles de saisie. Elle remplace la collecte « e-mail seul »
de l’évolution du 3 novembre et l’exception sans téléphone de CN-ARB-02.
L’inscription publique reste immédiate, gratuite et limitée à une chance par
adresse normalisée ; aucune vérification intermédiaire ni identité civile vérifiée
n’est introduite. La politique `EMAIL_DECLARE` conserve ce sens.

Les nouvelles coordonnées sont enregistrées à la création ou lors de la première
confirmation explicite d’une ancienne attente non confirmée. Une nouvelle saisie
publique pour une adresse déjà inscrite ne remplace pas l’identité existante.
Les anciennes participations restent lisibles et récupérables sans inventer les
coordonnées absentes. La collecte ne vaut ni accord marketing ni activation Push.
Les règles propres à la chasse (majorité/équipe), au règlement et à la qualification
restent conservées. Aucune migration de données n’est nécessaire.

## Évolution E74-EVOL-INSCRIPTION-DIRECTE — 3 novembre 2026

La demande produit supprime l’e-mail intermédiaire : depuis le QR ou **S’inscrire** dans Live, l’habitant saisit uniquement son adresse, accepte le règlement et valide. La commande enregistre immédiatement une participation qualifiée et prépare un seul e-mail de confirmation. Ce mail explique le tirage, donne l’accès personnel au carnet et invite à installer Live ; le consulter n’est plus nécessaire pour obtenir une chance.

Cette décision remplace les anciens arbitrages ARB-01/03 qui imposaient prénom et adresse vérifiée. Une adresse déclarée n’est pas marquée vérifiée. Les participations déjà qualifiées, anciens liens et historiques sont conservés ; les anciennes demandes abandonnées ne sont pas qualifiées automatiquement. Les critères CA07/08/09/12/15/16 gardent leurs identifiants. L’état de l’epic reste **En cours**.

## Décisions et périmètre

La tombola publique est une nouvelle mécanique `TOMBOLA_PUBLIQUE`, version initiale `1.0`. Elle rejoint la catégorie standard et utilise le quota standard existant, également pour les souscriptions déjà actives. Elle n'accorde ni quota supplémentaire ni module payant gratuit. La tombola commerçante E53 conserve sa qualification par achat validé.

| Arbitrage du backlog | Décision confirmée le 3 novembre 2026 |
| --- | --- |
| E74-ARB-01 | Nom, prénom, e-mail, téléphone, acceptation explicite du règlement et validation immédiate. Un seul e-mail de confirmation après inscription ; une consultation ne crée aucune participation. |
| E74-ARB-02 | QR et lien partageables, sans preuve de présence au stand ni géolocalisation obligatoire. |
| E74-ARB-03 | Précision du 11 novembre : nom, prénom, e-mail et téléphone obligatoires, sans nouveau compte. Une seule chance par e-mail normalisé et par tombola dès l’inscription ; coordonnées déclarées, sans prétendre les avoir vérifiées. |
| E74-ARB-04 | Trois modes existants : Coffrets, bons numériques Localeo et lots libres gérés en externe. Les lots externes fonctionnent sans commerce. |
| E74-ARB-05 | Quota standard et conditions acquises conservés, y compris pour les souscriptions déjà actives. Consommation idempotente à la publication. |
| E74-ARB-06 | Suivi facultatif de la commune dans Live, sans nouveau canal d'envoi ni campagne inter-animations. |

« Une adresse » n'est pas une preuve d'unicité d'une personne physique : deux personnes partageant une boîte disposent d'une chance commune ; plusieurs adresses ne sont pas fusionnées. La normalisation conserve la règle existante `strip().lower()` ; aucune suppression des points ou suffixes `+` propres à un fournisseur.

Sont exclus : achat ou billet payant, preuve Pro/PIN pour qualifier, chances multiples, présence physique contrôlée, fonctionnement hors connexion, nouveau compte habitant, nouveau référentiel de joueurs, second moteur de tirage, prospection CRM ou campagne future déduite de l'inscription. Les lots n'introduisent aucun mélange de modes au-delà des configurations déjà autorisées par E73.

## Parcours organisateur

1. **Choisir** « Tombola publique » dans le catalogue Animation. Afficher « Incluse dans votre forfait » et le quota réellement disponible. Les droits d'organisation, de commune et de publication restent requis.
2. **Préparer** en étapes : Commune → Présentation et dates → Lots → Règlement et support → Vérifier et publier. Le modèle est choisi auparavant. Aucune sélection, invitation, mission, réponse ou activation de commerçant n'est exigée pour qualifier les habitants.
3. **Vérifier** dans l'assistant : montrer d'abord le prochain blocage réel et son action. Distinguer acquis, manquant et non applicable à partir du serveur. Les actions secondaires restent accessibles sans encombrer le guide. Dates, règlement, droits et disponibilité de la dotation restent contrôlés ; l'absence de commerce n'est pas une alerte.
4. **Publier** avec les contrôles et la consommation de quota E73. Une organisation sans commerce peut publier une dotation externe. Coffrets conserve ses prérequis de dotation/paiement ; un bon numérique conserve ses prérequis de remise par un commerce. Ce commerce de remise ne devient pas une condition de qualification.
5. **Diffuser** le QR public et le lien équivalent. Le flyer présente commune, dates, lots, conditions et consigne « Saisissez votre e-mail pour vous inscrire ». Il annonce une seule chance après validation et ne demande aucun achat. Utiliser l'image personnalisée si présente ; ne pas inventer d'image ni afficher « 0 commerçant » comme anomalie.
6. **Suivre** les demandes en attente, participants qualifiés, gagnants et remises. Listes paginées réellement côté serveur ; compteurs exacts de catégories explicites. Les compteurs publics comprennent les inscriptions directes qualifiées et les anciennes participations confirmées, sans révéler les adresses ou les demandes en attente.
7. **Clôturer, tirer et remettre** avec les workflows E73. Les nouvelles inscriptions et les confirmations des anciens liens sont fermées à la fin des inscriptions ; la population du tirage est figée à la clôture. La confirmation des résultats et les actions irréversibles restent explicites.

Les opérations ERP, API et batch passent par les mêmes politiques métier. L’ERP ne doit pas rendre un habitant éligible en contournant la preuve d’inscription et le règlement. Une inscription directe ne prouve pas la possession de la boîte e-mail.

## Parcours habitant dans Live

| Étape | Présentation et action principale | Résultat et issue alternative |
| --- | --- | --- |
| Découvrir | Fiche publique mobile : commune, dates, vrais lots, « une chance par e-mail », bouton « S’inscrire » | Aucune connexion requise. Le QR ouvre le même formulaire ; aucune inscription par simple ouverture. |
| S’inscrire | Nom, prénom, e-mail, téléphone ; règlement consultable et acceptation non précochée ; bouton de validation unique | Une inscription qualifiée et une chance immédiatement, puis un e-mail de confirmation préparé. Une réponse 202 ne prouve pas la livraison du mail. |
| Retrouver | Ouvrir l’accès personnel reçu par e-mail et ajouter l’animation au carnet Live | « Mes participations », « Mes lots » et tirages à venir réutilisés. Ce lien donne accès au suivi ; il ne crée pas une nouvelle chance. Aucun carnet personnel n’est inventé dans le navigateur qui n’a saisi qu’une adresse. |
| Installer Live | Proposition facultative dans le mail et les parcours Live existants | Installer facilite le retour au carnet ; aucune obligation pour participer ni synchronisation automatique entre appareils promise. |
| Suivre la commune | Action secondaire « Suivre cette commune » avec portée « dans ce navigateur » | Facultatif ; aucun changement de chance, abonnement marketing ou autorisation de notifications implicite. |

Une nouvelle saisie de la même adresse ne modifie pas l’identité existante et ne retourne jamais son accès personnel au demandeur public. Elle n’ajoute aucune chance ; un accès de récupération peut être envoyé selon les limites existantes. Le rejeu avec la même clé et le même corps ne renvoie pas un deuxième mail. Une faute d’adresse se corrige avant validation ; après validation, saisir la bonne adresse ne transfère ni ne supprime une participation déjà enregistrée sous une autre adresse.

L’e-mail de confirmation précise que l’inscription est déjà enregistrée, annonce la suite (tirage et résultats, sans promesse de gain), propose le lien personnel vers Live et l’ajout au carnet, puis l’installation facultative. Une inscription ne constitue ni un compte ni un consentement marketing. Le prénom absent reste absent, y compris dans les messages, listes et résultats.

Les anciens liens de vérification restent utilisables dans leur durée de validité et nécessitent leur confirmation explicite. Une ancienne demande en attente peut être qualifiée par une nouvelle inscription explicite pendant l’ouverture ; cette transition invalide son challenge et empêche l’envoi d’un mail intermédiaire encore en attente. Aucune migration ne qualifie les attentes abandonnées.

Après fermeture, **Retrouver ma participation** reste disponible pour les participations qualifiées jusqu’à la limite existante de 90 jours après la fin. Une récupération ne qualifie jamais une ancienne attente et sa réponse reste neutre.

### États et refus lisibles

- **Ancienne demande à confirmer** : attente créée avant la simplification, zéro chance tant qu’aucune commande valide ne l’a qualifiée. Cet état n’apparaît plus après une nouvelle inscription directe réussie.
- **Inscription enregistrée** : preuve d’inscription dans la période autorisée, une chance ; aucun badge d’adresse vérifiée, de visite ou étape commerciale inventé.
- **Ancien lien expiré ou remplacé** : proposer une inscription directe si elle reste ouverte ; aucun token personnel livré par une adresse seule.
- **Fermée ou annulée** : aucune nouvelle qualification, même avec un lien émis avant fermeture. Une confirmation déjà réussie reste une réussite au rejeu de son reçu valide, sans nouvelle mutation.
- **Résultat incertain** : ne pas annoncer un succès ; reprendre la commande ou récupérer l'accès par e-mail.
- **Connexion indisponible** : expliquer que l’inscription nécessite le réseau. Ne pas mettre la commande en file hors ligne.

Les interfaces privilégient une action principale, des libellés courts, pictogrammes avec nom accessible, cibles tactiles d'au moins 44 px, focus visible, erreurs près du champ et annonces accessibles des transitions. Le parcours doit rester utilisable à 320 px, au clavier et avec réduction des animations. L'état n'est jamais communiqué uniquement par une couleur ou une animation de célébration.

## Tirage et lots : différences à conserver

| Mode E73 | Zéro ou peu de candidats | Remise |
| --- | --- | --- |
| Lots libres externes | Nombre de gagnants = minimum entre exemplaires et candidats ; zéro reste un résultat explicite sans gain. Confirmation et version de population existantes. | Déclaration de remise par l'organisateur, aucun commerce requis. |
| Bons numériques | Même protocole de tirage libre ; disponibilité et affectation des bons contrôlées par E73. | Consommation selon les accès, QR/PIN et règles de remise existants ; indépendante de la qualification initiale. |
| Coffrets | Le moteur existant refuse un tirage avec moins de candidats que de lots. Afficher ce blocage, sans supprimer silencieusement des lots ou créer des gagnants. | Parcours Coffrets existant ; aucune émission ou distribution sur un tirage refusé. |

La qualification ne promet pas un lot. Les états d'envoi, de livraison éventuelle, de retrait et de consommation sont distincts. Les reprises du tirage et des notifications ne recréent pas de gains. Les politiques de suppléants et de remplacement restent celles du mode choisi.

Pour Coffrets, tous les exemplaires publiés participent au tirage et la dotation est figée : aucune sélection réduite ni correction après publication n'est disponible dans le parcours actuel. Prévenir l'organisateur lors du choix de ce mode et expliquer le refus si le seuil n'est pas atteint. E74 ne modifie pas implicitement cette règle ; permettre un tirage Coffrets partiel demanderait une évolution distincte.

## Suivi de la commune et notifications

Réutiliser « Mes communes » et la préférence locale existante (maximum dix communes). L'ouverture du QR n'ajoute pas la commune automatiquement. Si la limite est atteinte, proposer « Gérer mes communes » ; une indisponibilité du stockage n'empêche pas de participer et n'est pas annoncée comme un suivi sauvegardé.

Le retrait dans « Mes communes » enlève le suivi de cet appareil et synchronise les préférences d'installation lorsqu'elles existent. Il conserve la participation et les lots. Il ne désabonne pas silencieusement des messages propres à une animation : ce choix dispose déjà de sa gestion distincte. Aucune synchronisation entre appareils ni association à un compte inexistant n'est promise.

L’e-mail de confirmation d’inscription, les anciennes vérifications, la récupération d’accès et les notifications transactionnelles du jeu restent dans leurs finalités. Le suivi commune n'active ni push, ni préférence organisateur, ni module Communication. Les communications facultatives existantes restent limitées à leur animation, à leurs droits et à leur fenêtre d'envoi.

## Préparation de l'implémentation

Les six arbitrages sont résolus. La conception technique et les preuves sont détaillées dans les deux documents liés en tête. L’évolution d’inscription directe porte sur l’identité déclarée, la preuve de qualification, l’e-mail, les lecteurs et la compatibilité des anciens liens. Ses résultats de tests sont distingués des preuves historiques du parcours avec vérification.

La clôture technique reposera sur les tests unitaires, d'intégration et fonctionnels de la [matrice](verification.md), y compris migrations, concurrence et volumétrie. Les démarches de mise en service et la revue du règlement ne sont pas des preuves techniques ni un pilote requis pour clôturer ; elles restent suivies séparément avant utilisation réelle.

- [Guide organisateur, habitant et support](guide-utilisation.md).
- [Migration, activation et exploitation](exploitation.md).
