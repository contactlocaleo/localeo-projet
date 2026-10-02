# EPIC 69 — Accès ERP et applications internes

Version **V1.4 — évolution du 2 octobre 2026 : scopes fonctionnels globaux**. État produit : **Terminée le 2 octobre 2026**,
selon le [backlog canonique](../../roadmap/terminees/epic-69-profils-acces-erp-satellites-backlog.md).
La V1.4 backend est désormais committée et poussée sur `main` : **`4635820`**,
scopes globaux, formulaire sans périmètre territorial et correctif de migration
v252 inclus. La base de test est en v253 ; le déploiement applicatif de ce commit
n'est pas attesté. Le [bilan](verification-livraison.md) conserve les preuves et
les constats antérieurs à cette publication. **CA-18 est corrigé et testé localement
le 2 octobre**, après le correctif Backoffice `72f690c` : trace des succès/refus
avec identité vérifiée, scopes et corrélation, sans secret. Cette correction
reste à publier/livrer. La revue finale accepte les 27 critères après 37 scénarios
de trace réussis, réutilisation des preuves inchangées et contrôle du guide ERP.
La clôture n'atteste pas le déploiement ni la recette de l'environnement cible.

Ce dossier conserve les 27 critères E69-CA-01 à 27, sans renumérotation. Le socle
V1.3 est commité et poussé sur `main` (`localeo-backend` : `86199b1` ; documentation
de référence : `4613ac2`). Ces SHAs et leurs tests ne prouvent pas la V1.4,
dont l'implémentation locale, la migration v253 et les preuves propres sont
consignées dans le bilan. La revue de clôture du 2 octobre conserve l'état
**En cours** : **CA-18 était partiel**, faute de trace attribuée aux utilisateurs
internes pour les refus d'accès. L'intervention suivante, sur demande explicite,
a migré la **base de test jusqu'à v253** avec sauvegarde et contrôles ; elle n'a
ni déployé le code applicatif, ni créé de compte réel, ni recetté les parcours.

La reprise V1.1 précise les DTO et versions, la portée des capacités pour le cumul,
le contexte ERP et le monitor, les exports et les finalités d'invitation/reset.
La V1.2 conserve les 27 critères et intègre les trois arbitrages utilisateur :
invitation/récupération validées, suivi Finance via Support existant, et ouverture
au Backoffice de BUM, activation à zéro et annulation impayée non active.

## Documents

- [Architecture et contrats](architecture-contrats.md) : domaine, comptes,
  invitations, sessions, API, concurrence et transition.
- [Permissions et surfaces](permissions-surfaces.md) : capacités par rôle,
  interfaces existantes, protections et limites à lever.
- [Vérification et livraison](verification-livraison.md) : traçabilité des 27
  critères, jeux isolés, migrations et recette.
- [Guide backoffice](guide-backoffice.md) : parcours opérateur et libellés vérifiés
  dans l'interface ; export ERP configuré, publication en cible à vérifier.
- [Configuration d'environnement](../../exploitation/technique/reference-configuration-environnement.md#comptes-internes-erp--epic-69) :
  valeur de `LOCALEO_ERP_URL` et limites des invitations.

## Évolution E69-SCOPES-GLOBAUX-20261002

Décision utilisateur du **2 octobre 2026** : les habilitations internes utilisent
des scopes fonctionnels nommés, comme les autorisations de batch, **sans contexte
de commune**. Lecteur, Backoffice, Finance et Backoffice + Finance gardent les
mêmes droits fonctionnels ; chaque droit accordé s'applique à **toutes les communes**.

Cette décision remplace E69-D06 et les anciennes restrictions territoriales des
critères existants. L'élargissement est explicite, décidé et migré ; il ne crée
aucun nouveau droit financier, technique, SQLAdmin ou d'administration interne.
Les clés API des batchs restent une authentification distincte des sessions humaines.

Le domaine déduit `scopes: list[str]` des profils prédéfinis, avec les noms exacts
de la [matrice](permissions-surfaces.md), par exemple `metier.consulter`.
Une nouvelle attribution est `{role}`. L'ancienne forme `scope: {type: "GLOBAL",
communeIds: []}` est acceptée en compatibilité ; `COMMUNES` est refusé.
`capabilities` reste un alias de lecture avec portée `GLOBAL`, sans autorité
territoriale. Aucun rôle sur mesure ni scope arbitraire n'est attribuable.

## Résultat attendu

L'admin historique crée un compte nominatif, choisit ses profils prédéfinis,
puis l'invite par email. L'utilisateur définit son mot de passe et accède aux
seuls parcours autorisés de l'ERP et des satellites. Modifier son rôle ou le
désactiver retire les droits dès la prochaine requête protégée, y compris depuis
une PWA ou un ancien lien.

| Attribution | Fonction |
| --- | --- |
| Lecteur | Consultation métier sans génération, envoi ni mutation |
| Backoffice | Gestion quotidienne, onboarding, catalogue, animations, Support et Atelier |
| Finance | Consultation, exports et suivi financier spécialisé sans commande d'argent |
| Backoffice + Finance | Union explicite des scopes fonctionnels précédents, sur toutes les communes |
| Admin historique | Accès configuré conservé ; seul accès SQLAdmin, technique, administration et commandes financières sensibles |

Finance ne reçoit ni la lecture de tout le catalogue ni les pièces d'identité
des commerçants. Les références nécessaires à un paiement apparaissent dans une
projection financière limitée. Le cumul n'accorde jamais un rôle admin.

## Décisions et hypothèses

Les décisions utilisateur du backlog font autorité. Les choix techniques de
conception ci-dessous les mettent en œuvre ; les propositions encore ouvertes
ne sont pas présentées comme validées.

| Référence | Décision / état | Portée |
| --- | --- | --- |
| E69-D01 | Acquis : trois rôles métier, seul cumul Backoffice + Finance | Pas d'éditeur de rôles ni de cumul caché ; Lecteur seul signifie lecture seule |
| E69-D02 | Acquis : préserver l'admin historique | Identité de sécurité distincte des comptes nominatifs ; SQLAdmin et outils techniques restent fermés à tous les rôles métier |
| E69-D03 | Acquis : commandes engageant de l'argent réservées à l'admin en V1 | Inclut remboursement, avoir, modification de montant dû, transfert et reprise financière lorsqu'ils existent ; aucune modification des règles financières elles-mêmes |
| E69-D04 | Acquis : invitation après référencement par l'admin | Lien à usage unique, pas de mot de passe transmis ; réutilisation des mécanismes adaptés d'Animation sans mélanger les populations |
| E69-D05 | Conception : autorisations résolues côté serveur à chaque requête | Cookie sans autorité sur rôles/scopes ; même politique pour pages, commandes, pièces, exports et reprise différée |
| E69-D06 | **Remplacée le 2 octobre par E69-SCOPES-GLOBAUX-20261002** | V1.1–V1.3 : portée territoriale par attribution. V1.4 : profils prédéfinis, scopes fonctionnels globaux ; aucune commune d'habilitation |
| E69-D07 | Conception : pas de nouvelle commande financière ou de workflow comptable | Réutiliser les fonctions existantes ; signaler les fonctions absentes avant de déclarer CA-19 couvert |
| E69-H01 | **Validé par l'utilisateur :** invitation 24 h, récupération déclenchée par l'admin, matrice fixe sans restriction supplémentaire par module | Référence conservée pour traçabilité ; plus d'arbitrage ouvert sur ces trois choix |
| E69-D08 | Conception : conserver la politique de session existante, 15 min d'inactivité et 8 h absolues | Les vérifications automatiques n'entretiennent pas l'activité ; évolution éventuelle hors cette V1 |
| E69-H02 | MFA non ajoutée au périmètre acquis | Ne pas transformer une question de cadrage en fonctionnalité réputée livrée |
| E69-ARB-05 | **Résolu : option A**, consultation/export et demandes via Support existant | Tickets/notes financiers bornés ; aucun workflow financier dédié ni mutation comptable |
| E69-ARB-06 | **Résolu : ouvrir les trois actions au Backoffice**, Admin conservé | Qualification/suspension BUM du coffret, activation de souscription déjà à zéro, annulation impayée non active ; conditions métier conservées ; scopes Backoffice globaux, Finance seul refusé |

## Parcours et interfaces cibles

### Admin : créer et inviter

Dans ERP → Utilisateurs internes, l'admin consulte une liste paginée : identité,
email, profils et état du compte. La recherche **Nom ou email** est envoyée au
paramètre API `recherche` ; le filtre **État** complète cette recherche. Invitation,
envoi et dernière connexion se consultent dans la
fiche ; le filtre dédié « Invitations à reprendre » de la conception n'est pas
implémenté. Les données financières et mots de passe sont absents de cette vue.

« Ajouter un utilisateur », puis « Créer et préparer l’invitation », demande nom,
prénom, email et profils. L'admin choisit Lecteur, Backoffice, Finance ou le cumul
Backoffice + Finance ; aucun sélecteur de communes n'est proposé.
Un doublon produit un conflit : revenir à la liste pour rechercher l'email ;
l'interface ne fournit pas encore de lien direct vers le compte existant.
Un compte désactivé n'est pas réactivé par une nouvelle création.

La création réussie affiche « Compte créé — email préparé », puis le suivi réel
du canal. « Email envoyé » n'implique ni livraison ni initialisation. La fiche
propose modifier, renvoyer/annuler l'invitation, désactiver et révoquer les sessions.
Le choix des rôles est explicite et les droits effectifs sont consultables avant
confirmation. Le compte admin historique n'est pas éditable dans cet écran.

### Destinataire : initialiser puis se connecter

L'email indique Localeo ERP, l'invitant, la validité du lien et un contact de
reprise. Il contient « Définir mon mot de passe », jamais un mot de passe. Le
formulaire d'initialisation ne nécessite aucune session admin. Il reçoit un
jeton dans le fragment URL, l'efface de l'historique courant et le conserve
uniquement en mémoire le temps de soumettre mot de passe + confirmation.
L'ouverture/aperçu du mail ne consomme pas le lien.

Après succès : « Mot de passe défini — vous pouvez vous connecter ». Pas de
connexion automatique. Un lien indisponible affiche le même message pour les
cas expiré, annulé, utilisé ou invalide, avec contact de l'admin. Les destinations
de retour sont des chemins internes autorisés, jamais une URL fournie librement.

La connexion nominative utilise l'email et conduit à `/internal/erp`, dont les
liens et données dépendent des capacités. Finance dispose d'un accueil sans
référentiel catalogue. Le retour automatique à un satellite demandé avant
connexion reste un objectif de conception : le formulaire actuel renvoie à
l'accueil ERP. L'utilisateur y choisit son application autorisée.

### Vie du compte

Un retrait de rôle supprime les liens/actions correspondants au prochain échange
serveur et empêche immédiatement les nouvelles lectures/commandes interdites.
Un résultat ancien encore affiché est effacé au refus/changement de version ;
aucun système ne peut effacer une donnée déjà copiée hors de l'application.
Les caches applicatifs ne doivent pas conserver de données métier sensibles.

Un renvoi d'invitation invalide l'ancien lien ; une reprise fournisseur de la même
livraison ne crée pas un nouveau lien. Pour un compte initialisé, utiliser une
réinitialisation distincte : l'ancien mot de passe n'est remplacé qu'après
validation du formulaire ; à ce moment toutes les sessions sont révoquées.
La récupération est déclenchée par l'admin, conformément à E69-H01 validé ;
aucun libre-service « mot de passe oublié » n'est ajouté à cette V1.

## Périmètre, dépendances et préparation

Backend, ERP et PWA internes sont concernés. Animation fournit une référence
d'invitation ; ses gestionnaires, ses sessions et ses contrats ne sont pas
convertis. Marketplace, Commerçant et portail partenaire ne reçoivent pas de
nouveau rôle ; leurs appels partagés doivent rester couverts par les non-régressions.

Les projections E65 sont adaptées aux capacités métier et Finance ; Audit reste
réservé à l'admin. Atelier et OnBoard séparent consultation et gestion. E68
consommera les capacités d'onboarding sans pouvoir administrer des accès internes.
L'évolution V1.4 touche les profils, DTO/scopes, gardes, menus, fixtures et le
générateur interne du backend. Les trois frontends publics ne changent pas de
contrat : aucune transformation des gestionnaires Animation, comptes commerçants
ou clients Marketplace. Aucun déploiement n'est implicite.

La conception du socle et de l'invitation peut avancer indépendamment des écrans
encore à classifier. L'ouverture générale d'un rôle dépend du recensement complet
des entrées, des droits et des tests de refus listés dans la matrice. Les paramètres
et écarts non résolus sont recensés dans les autres documents de ce dossier.

Le tableau suivant conserve le **bilan historique V1.3**, pas une validation de
l'évolution globale V1.4. Ses anciens contrôles territoriaux sont à remplacer par
les scénarios V1.4 du bilan de vérification.

| Partie | État local V1.3 |
| --- | --- |
| Politique de rôles, principal typé, scopes par capacité, sessions et protections SQLAdmin | Implémentés ; refus HTTP, concurrence PostgreSQL et reprise historique testés |
| Création/invitation et récupération | Invitation 24 h et récupération administrée implémentées ; usage unique, versions, révocation et transport testés |
| Consultations/export Finance | Projections distinctes, filtrage avant totaux/pagination, export et pièces autorisées contrôlés |
| Suivi humain Finance | Tickets et notes Support avec rattachement financier, attribution et façades selon rôle |
| Ouverture des actions sensibles Backoffice | Trois capacités séparées, conditions métier conservées ; permissions partenaires délégables en liste fermée |

Les trois arbitrages soumis à l'utilisateur sont résolus en V1.2. Les inventaires
techniques et preuves sont suivis dans le bilan de vérification ; la recette déployée
et la politique de purge périodique des anciennes invitations restent explicites.
