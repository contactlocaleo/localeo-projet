# E74 — Tombola publique sans commerçant

Spécification V1 du **3 novembre 2026**, fondée sur les choix explicites du porteur produit et l'examen des producteurs et consommateurs. L'état produit est **En cours** dans la [roadmap](../../roadmap/README.md). L’implémentation locale et les preuves sont suivies dans le bilan ; le modèle reste désactivé avant mise en service.

- [Backlog canonique : 8 US et 16 critères](../../roadmap/en-cours/epic-74-tombola-publique-backlog.md).
- [Architecture, contrats et livraison](architecture-contrats.md).
- [Matrice des preuves et recette](verification.md).

## Décisions et périmètre

La tombola publique est une nouvelle mécanique `TOMBOLA_PUBLIQUE`, version initiale `1.0`. Elle rejoint la catégorie standard et utilise le quota standard existant, également pour les souscriptions déjà actives. Elle n'accorde ni quota supplémentaire ni module payant gratuit. La tombola commerçante E53 conserve sa qualification par achat validé.

| Arbitrage du backlog | Décision confirmée le 3 novembre 2026 |
| --- | --- |
| E74-ARB-01 | Formulaire court, acceptation explicite du règlement, puis confirmation explicite depuis l'e-mail reçu. Une consultation ne crée aucune participation. |
| E74-ARB-02 | QR et lien partageables, sans preuve de présence au stand ni géolocalisation obligatoire. |
| E74-ARB-03 | Prénom et e-mail obligatoires, sans nom, téléphone ou nouveau compte. Adresse vérifiée avant qualification. Une seule chance par e-mail normalisé et par tombola. |
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
5. **Diffuser** le QR public et le lien équivalent. Le flyer présente commune, dates, lots, conditions et consigne « Inscrivez-vous puis confirmez votre e-mail ». Il ne promet aucune chance avant cette confirmation et ne demande aucun achat. Utiliser l'image personnalisée si présente ; ne pas inventer d'image ni afficher « 0 commerçant » comme anomalie.
6. **Suivre** les demandes en attente, participants qualifiés, gagnants et remises. Listes paginées réellement côté serveur ; compteurs exacts de catégories explicites. Les compteurs publics ne comprennent que les participations confirmées, sans révéler les adresses ou les demandes en attente.
7. **Clôturer, tirer et remettre** avec les workflows E73. La confirmation d'e-mail est fermée à la fin des inscriptions ; la population du tirage est figée à la clôture. La confirmation des résultats et les actions irréversibles restent explicites.

Les opérations ERP, API et batch passent par les mêmes politiques métier. L'ERP ne doit pas rendre un habitant éligible en contournant la preuve d'adresse.

## Parcours habitant dans Live

| Étape | Présentation et action principale | Résultat et issue alternative |
| --- | --- | --- |
| Découvrir | Fiche publique mobile : commune, dates, vrais lots, règle « une chance par e-mail confirmé », bouton « Participer » | Aucune connexion requise. Avant ouverture ou après fermeture : dates et état lisibles, action indisponible. |
| S'inscrire | Prénom, e-mail, règlement consultable et acceptation non précochée ; bouton « Recevoir mon lien de confirmation » | Le serveur accepte la demande. Pas encore de chance ni de participation confirmée dans la bibliothèque Live. |
| Attendre | « Vérifiez votre boîte e-mail » ; rappeler les indésirables, permettre correction d'adresse et renvoi après délai | Une réponse 202 indique la prise en compte, pas la livraison du message. Une erreur réseau reste incertaine et se reprend avec la même clé. |
| Confirmer | Le lien ouvre la bonne tombola, y compris sur un autre appareil. Bouton « Confirmer ma participation » | L'ouverture seule ne qualifie pas. Le POST explicite vérifie secret, dates et état courant. |
| Retrouver | « Vous participez : 1 chance au tirage », état de qualification serveur et date annoncée si connue | Accès personnel vérifié ajouté au parcours Live existant ; « Mes participations », « Mes lots » et tirages à venir réutilisés. |
| Suivre la commune | Action secondaire « Suivre cette commune » avec portée « dans ce navigateur » | Facultatif ; aucun changement de chance, abonnement marketing ou autorisation de notifications implicite. |

Le prénom est modifiable lors de la confirmation par le détenteur du lien ; une demande publique non vérifiée ne modifie jamais le profil d'une participation déjà confirmée. Une erreur d'adresse se corrige en demandant un nouveau lien à la bonne adresse : elle ne transfère pas un accès existant. Les demandes abandonnées ne sont pas qualifiées.

Un participant déjà confirmé retrouve son accès par e-mail. Une nouvelle saisie de son adresse ne retourne jamais son accès personnel au demandeur public et n'ajoute aucune chance. Aucun compte, mot de passe, appareil reconnu ou accès Live existant ne dispense de la preuve d'adresse propre à cette tombola.

Après fermeture des inscriptions, conserver une action « Retrouver ma participation » vers la récupération d'accès, distincte de « Participer ». Elle reste disponible selon la durée d'accès existante (jusqu'à 90 jours après la fin) pour les participants confirmés. Une demande encore en attente ne peut plus être confirmée ni recevoir un nouveau lien de vérification. La réponse publique de récupération reste neutre dans les deux cas.

### États et refus lisibles

- **À confirmer** : demande enregistrée, e-mail non vérifié, zéro chance ; ne pas afficher « Inscription confirmée ».
- **Qualifié** : preuve confirmée dans la période autorisée, une chance ; aucun badge de visite ou étape commerciale inventée.
- **Lien expiré ou remplacé** : proposer un renvoi si la tombola accepte encore les inscriptions ; aucun token personnel livré.
- **Fermée ou annulée** : aucune nouvelle qualification, même avec un lien émis avant fermeture. Une confirmation déjà réussie reste une réussite au rejeu de son reçu valide, sans nouvelle mutation.
- **Résultat incertain** : ne pas annoncer un succès ; reprendre la commande ou récupérer l'accès par e-mail.
- **Connexion indisponible** : expliquer que la confirmation nécessite le réseau. Ne pas mettre la commande en file hors ligne.

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

L'e-mail de vérification, la récupération d'accès et les notifications transactionnelles du jeu restent dans leurs finalités. Le suivi commune n'active ni push, ni préférence organisateur, ni module Communication. Les communications facultatives existantes restent limitées à leur animation, à leurs droits et à leur fenêtre d'envoi.

## Préparation de l'implémentation

Les six arbitrages sont résolus. La conception technique et les preuves sont détaillées dans les deux documents liés en tête. Les limites observées du code actuel (identité obligatoire complète, absence de preuve d'adresse, registres fermés et pagination en mémoire) font partie du travail E74, pas d'hypothèses de compatibilité.

La clôture technique reposera sur les tests unitaires, d'intégration et fonctionnels de la [matrice](verification.md), y compris migrations, concurrence et volumétrie. Les démarches de mise en service et la revue du règlement ne sont pas des preuves techniques ni un pilote requis pour clôturer ; elles restent suivies séparément avant utilisation réelle.

- [Guide organisateur, habitant et support](guide-utilisation.md).
- [Migration, activation et exploitation](exploitation.md).
