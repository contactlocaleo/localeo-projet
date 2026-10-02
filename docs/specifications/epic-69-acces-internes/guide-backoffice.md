# Gérer les accès ERP et applications internes

**Guide E69 V1.4 — cible du 2 octobre 2026, après livraison du backend et des migrations v251/v252/v253.**
L'évolution des droits globaux est en cours. Vérifier la version déployée avant utilisation ;
la présence de ce guide ne prouve pas la mise en service sur votre environnement.

## Choisir les droits

| Attribution | Usage |
| --- | --- |
| Lecteur | Consulter les dossiers et indicateurs autorisés |
| Backoffice | Gérer les dossiers, l'onboarding, le catalogue, les animations, Support et Atelier |
| Finance | Consulter et exporter les données financières nécessaires ; suivi des demandes financières autorisées sur toutes les communes |
| Backoffice + Finance | Cumuler explicitement les deux responsabilités |

L'admin historique reste réservé à l'administration et à la reprise. Seul cet
accès ouvre SQLAdmin, les outils techniques et les commandes financières sensibles
en V1. Attribuer Finance ne permet pas de déclencher un remboursement.

Chaque profil donne ses droits fonctionnels sur **toutes les communes**.
Il n'y a aucun choix de communes lors de la création ou de la modification d'un
utilisateur interne. Finance ne donne pas les droits de gestion du catalogue.
Ne pas distribuer les identifiants de l'admin historique pour contourner un refus.

Un compte Backoffice peut gérer les accès commerçants et partenaires sur toutes
les communes, avec les seules permissions partenaires délégables. Cela ne lui
donne pas le droit d'inviter un collègue dans l'ERP. Les permissions partenaires
réservées à l'admin le restent, même pour un gestionnaire présent sur plusieurs communes.

Backoffice peut aussi valider ou suspendre la qualification
BUM d'un coffret, activer une souscription déjà à 0 € et annuler une commande impayée
non active, quelle que soit sa commune. Les confirmations et conditions métier restent
obligatoires. Finance seul ne dispose pas de ces trois actions ; les remboursements,
transferts, avoirs et annulations de factures restent réservés à l'admin.

## Créer un utilisateur

1. Se connecter avec l'admin historique, puis ouvrir **Utilisateurs internes**
   (`/internal/erp/utilisateurs`) et sélectionner **Ajouter un utilisateur**.
2. Renseigner nom, prénom et email personnel de travail. Vérifier l'adresse avec
   la personne ; elle recevra le lien pour définir son mot de passe.
3. Choisir le profil ou le cumul Backoffice + Finance. Vérifier les fonctions accordées ;
   elles sont valables pour toutes les communes, sans sélection territoriale.
4. Valider **Créer et préparer l’invitation**. Le résultat initial est « email préparé », pas
   une preuve de réception. Consulter le suivi depuis la fiche.
5. L'utilisateur choisit et confirme son mot de passe, puis se connecte à l'ERP.
   L'admin ne définit pas ce mot de passe et n'en reçoit aucune copie.

Si l'email existe déjà, revenir à la liste, saisir cet email dans **Nom ou email**,
lancer **Rechercher** puis ouvrir sa
fiche. L'erreur de conflit actuelle ne fournit pas de lien vers cette fiche.
Vérifier s'il s'agit d'un compte
en attente, actif ou désactivé ; ne pas créer un doublon avec une autre adresse
uniquement pour contourner un blocage.

## Lire le suivi et traiter une invitation

| Situation | Action |
| --- | --- |
| Email préparé | Attendre sa prise en charge ou consulter l'erreur remontée ; aucune preuve de réception à ce stade |
| Email pris en charge, livraison inconnue | Vérifier avec le destinataire et les outils d'exploitation ; ne pas multiplier les renvois |
| Erreur d'adresse ou échec confirmé | Corriger l'adresse si nécessaire, puis renvoyer explicitement l'invitation |
| Invitation expirée | Renvoyer depuis la fiche ; le nouveau lien remplace l'ancien |
| Invitation utilisée | L'initialisation est terminée ; si la personne a oublié son mot de passe, utiliser le parcours de récupération prévu |
| Compte désactivé | Une invitation ne le réactive pas ; réévaluer l'habilitation avant toute réactivation explicite |

Le mail explique la durée du lien : 24 h. Le renvoi
invalide l'ancien lien, même si le destinataire reçoit l'ancien email plus tard.
L'ouverture du mail n'initialise pas le compte ; seule la validation du mot de
passe le fait. Un compte sans mot de passe initialisé n'accède pas aux dossiers.

Pour annuler un lien, utiliser **Annuler le lien en cours** dans la fiche ;
l'interface identifie automatiquement l'invitation concernée. Un compte actif
dispose du bouton **Envoyer une récupération d’accès** pour recevoir un nouveau
lien de récupération. **Renvoyer l’invitation** concerne les comptes en attente.

## Modifier ou retirer des droits

Depuis la fiche, relire les profils et les fonctions accordées avant modification.
Les changements sont tracés. Retirer Finance d'un compte Backoffice + Finance
laisse ses tâches Backoffice accessibles, mais retire le suivi financier spécialisé.
Un écran déjà ouvert peut afficher un refus à sa prochaine action : revenir à
l'accueil et actualiser, sans réessayer via SQLAdmin.

Désactiver le compte lors d'un départ ou d'un retrait complet d'accès ; ses
sessions et invitations sont invalidées. Réactiver ne restaure pas les anciens
liens ou sessions. Le compte reste consultable dans l'historique.

La récupération du mot de passe est déclenchée par l'admin en V1. L'utilisateur reçoit
un nouveau lien, son mot de passe ne change qu'après validation et ses sessions
sont alors révoquées. Ne pas lui demander son ancien mot de passe.

## Suivre une demande financière

Finance consulte le paiement/reversement et ses justificatifs autorisés, puis ouvre
ou complète une demande dans le Support existant depuis ce dossier. Le suivi utilise
les tickets/notes et leurs états habituels ; aucun workflow financier supplémentaire.
Finance ne peut pas parcourir les autres dossiers Support ni leurs échanges privés.
Une demande de remboursement est transmise à l'admin ; résoudre le ticket n'exécute
pas le remboursement et ne change pas l'état bancaire. Un dossier sans instance de
coffret conserve sa véritable référence financière, sans créer de fausse instance.

## Refus et reprise

- « Accès non autorisé » : vérifier le profil et la fonction demandée avec l'admin ; l'accès à
  un menu ne permet pas nécessairement toutes les actions du dossier.
- Finance ne peut pas rembourser : transmettre la demande à l'admin par le
  parcours convenu ; ne jamais modifier une écriture pour contourner le refus.
- Lien invalide/expiré : contacter l'admin et utiliser uniquement le nouveau lien.
- Session expirée : se reconnecter ; une session ne reste pas ouverte indéfiniment.
- Gestion des nouveaux comptes indisponible : l'admin utilise son accès historique
  de reprise. Une panne générale du backend ou de sa base relève de l'exploitation,
  pas d'un nouveau compte improvisé.

La fiche utilisateur ne fournit ni mot de passe ni lien d'invitation à copier.
Les opérateurs suivent les états et envoient les messages par les actions prévues.
Toute anomalie est remontée avec son identifiant de corrélation, sans secret.

Ce guide est accessible depuis **Guide de gestion des utilisateurs** dans la liste
des utilisateurs internes. Il décrit les actions de l'admin historique ; la présence
du document dans un bundle ne prouve pas que les migrations ont été appliquées.
