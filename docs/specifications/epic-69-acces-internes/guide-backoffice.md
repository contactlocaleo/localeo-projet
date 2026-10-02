# Gérer les accès ERP et applications internes

**Guide E69 V1.3 — à utiliser après livraison du backend et des migrations v251/v252.**
Les parcours sont implémentés localement. Vérifier la version déployée avant utilisation ;
la présence de ce guide ne prouve pas la mise en service sur votre environnement.

## Choisir les droits

| Attribution | Usage |
| --- | --- |
| Lecteur | Consulter les dossiers et indicateurs autorisés |
| Backoffice | Gérer les dossiers, l'onboarding, le catalogue, les animations, Support et Atelier |
| Finance | Consulter et exporter les données financières nécessaires ; suivi des demandes selon le périmètre retenu |
| Backoffice + Finance | Cumuler explicitement les deux responsabilités |

L'admin historique reste réservé à l'administration et à la reprise. Seul cet
accès ouvre SQLAdmin, les outils techniques et les commandes financières sensibles
en V1. Attribuer Finance ne permet pas de déclencher un remboursement.

Choisir aussi le périmètre de communes de chaque rôle, ou Global explicitement.
La portée Finance ne donne pas à Backoffice le droit de gérer ces mêmes communes.
Ne pas distribuer les identifiants de l'admin historique pour contourner un refus.

Un compte Backoffice peut gérer les accès commerçants et partenaires autorisés
par son périmètre ; cela ne lui donne pas le droit d'inviter un collègue dans l'ERP.
Si un gestionnaire partenaire intervient sur plusieurs communes, une modification
globale de son accès peut nécessiter l'intervention de l'admin.

Backoffice peut aussi valider ou suspendre la qualification
BUM d'un coffret, activer une souscription déjà à 0 € et annuler une commande impayée
non active, dans son périmètre. Les confirmations et conditions métier restent
obligatoires. Finance seul ne dispose pas de ces trois actions ; les remboursements,
transferts, avoirs et annulations de factures restent réservés à l'admin.

## Créer un utilisateur

1. Se connecter avec l'admin historique, puis ouvrir **Administration → Utilisateurs
   internes → Créer et inviter**.
2. Renseigner nom, prénom et email personnel de travail. Vérifier l'adresse avec
   la personne ; elle recevra le lien pour définir son mot de passe.
3. Choisir l'attribution et le périmètre. Relire le récapitulatif des droits.
4. Valider **Créer et inviter**. Le résultat initial est « email préparé », pas
   une preuve de réception. Consulter le suivi depuis la fiche.
5. L'utilisateur choisit et confirme son mot de passe, puis se connecte à l'ERP.
   L'admin ne définit pas ce mot de passe et n'en reçoit aucune copie.

Si l'email existe déjà, ouvrir la fiche indiquée. Vérifier s'il s'agit d'un compte
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

Pour annuler un lien, sélectionner l'invitation affichée avec son type (premier
accès ou réinitialisation). Un compte déjà initialisé utilise « Réinitialiser
le mot de passe » pour recevoir un nouveau lien de récupération, pas « Inviter ».

## Modifier ou retirer des droits

Depuis la fiche, relire les rôles et communes effectifs avant modification.
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

- « Accès non autorisé » : vérifier rôle et périmètre avec l'admin ; l'accès à
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

Référence de conception : [EPIC 69](README.md).
