# E73 — Plan de recette métier par fonctionnalité

Complément du 22 octobre : les [cinq scénarios de recette des flyers](flyers-contextualises.md#accès-et-recette-métier)
RM-FLYER-01 à 05 couvrent l'évolution E73-EVO-FLYER et restent à exécuter.
Ils s'ajoutent aux scénarios initiaux sans changer leurs résultats enregistrés.

Plan préparé le **22 octobre 2026**. **Les scénarios restent à exécuter sauf ceux explicitement barrés et marqués Réussi** : ce document ne constitue ni un procès-verbal complet de recette, ni une autorisation de déploiement. Il couvre les **38 US et 63 critères d’acceptation** de l’epic, en **25 fiches fonctionnelles**.

Le résultat recherché est de vendre et exploiter **Animation et/ou Coffrets**, avec une expérience compréhensible pour l’organisateur, le commerçant, le salarié et le participant. Pour chaque fonctionnalité : lire l’objet, vérifier tous les prérequis, suivre les actions et comparer le résultat obtenu au résultat attendu.

La [préparation de l’automatisation sur TEST](automatisation-recette.md) classe les 130 scénarios par mode d’exécution et décrit le nouveau jeu dédié. Ce plan ne vaut pas exécution automatique et conserve les résultats de recette humaine séparés.

Références : [spécification](README.md), [backlog et arbitrages](../../roadmap/en-cours/epic-73-animation-et-ou-coffrets-backlog.md), [matrice technique des 63 CA](verification-livraison.md), [accès par lot](prise-en-main-par-lot.md), [preuves d’implémentation et limites](suivi-implementation.md). Les CA mentionnés dans les fiches sont les identifiants `E73-CA-*` existants ; les identifiants `RM-*` servent au suivi de cette recette.

## Préparer la campagne de recette

Décision du 30 octobre, `E73-EVO-DOMAINES` : site public `animations.localeo.city`,
gestion `gestion-animations.localeo.city`, marketplace Coffrets indépendante.
En TEST : `test-animations`, `test-gestion-animations` et `test-marketplace`.
Configurer les services distincts avant leur recette hébergée ; les preuves
historiques conservent leurs URL et ne valident pas cette bascule.

### Conditions communes de démarrage

Cocher ces conditions avant le premier test. Un contrôle manquant place les scénarios dépendants en **Bloqué**, pas en Échec ni en Validé.

- [ ] Un environnement de recette est désigné, avec ses URL ERP, OnBoard, Pro, Animation, site public, Live, Support et Ops. Les accès internes sont réservés aux profils prévus.
- [ ] Les versions réellement servies par les applications et le backend sont relevées et compatibles E73. Vérifier aussi le cache/PWA des appareils. Une migration de base, même jusqu’à `v283_e73_compteurs_lectures.sql`, ne prouve pas que le code E73 est déployé.
- [ ] Les migrations nécessaires jusqu’à v283 sont confirmées et les contrôles de schéma sont satisfaisants. Les compteurs de participation/progression/validation sont cohérents avec les données de recette.
- [ ] Les capacités nécessaires à chaque fiche sont ouvertes dans cet environnement : configuration, clés de protection, URL publiques, stockage privé, traitements de fond et fournisseurs de test. Un indicateur activé sans worker opérationnel ne suffit pas.
- [ ] Les boîtes email et appareils de test sont contrôlés par les recetteurs ; les paiements utilisent exclusivement le mode test. Aucun scénario ne cible de vrais clients ou participants.
- [ ] Les comptes, communes, souscriptions et objets ci-dessous sont préparés avec des données synthétiques identifiables. Les mots de passe, PIN, QR utilisables et fichiers d’accès restent hors de ce document et des rapports partagés.
- [ ] Le calendrier de service est défini : jours ouvrés, horaires, fermetures, fuseau Europe/Paris. Il permet de vérifier les délais de préparation, support et export.
- [ ] Un référent Localeo peut préparer les états datés, droits expirés et incidents contrôlés nécessaires aux tests accompagnés. Ne pas avancer l’horloge d’un environnement partagé ni modifier directement ses tables pour gagner du temps.
- [ ] La validation UX est organisée **d’abord par Localeo**, puis avec **Martignas-sur-Jalle**, commune pilote. Le passage d’une étape à l’autre requiert ses résultats, pas seulement la présence des écrans.

Configuration et procédures à faire vérifier par l’équipe technique : [SaaS/exploitation](../../exploitation/exploitation/exploiter-saas-animation.md), [bons numériques](../../exploitation/exploitation/gerer-bons-numeriques-animation.md), [tirages libres](../../exploitation/exploitation/gerer-tirages-libres-animation.md), [imports](../../exploitation/exploitation/importer-commercants-animation.md), [chasse accompagnée](../../exploitation/exploitation/preparer-chasse-accompagnee.md), [communications](../../exploitation/exploitation/communiquer-participants-animation.md), [parcours et bilans](../../exploitation/exploitation/parcours-plateforme-animation.md). Ces guides portent les réglages techniques ; la recette ne doit pas contourner un refus de disponibilité.

### Comptes et données à préparer

| Jeu | Contenu à vérifier avant utilisation |
| --- | --- |
| Organisations A et B | A possède deux communes autorisées, A1 et A2 ; B possède B1. A1 représente le pilote avec des données synthétiques. Les objets de B ne doivent jamais être accessibles depuis A. Prévoir un compte appartenant explicitement aux deux organisations pour tester le changement de contexte. |
| Équipe cliente | Responsable A ; gestionnaire A1 ; lecteur A1 ; collaborateurs distincts avec Achat, Import commerçants et Communication. Un gestionnaire sans ces délégations sert aux refus. |
| Équipe Localeo | Administrateur ; Backoffice avec puis sans habilitations dédiées (périmètres, cadeaux/essais, communication) ; Finance avec puis sans autorisation de remboursement ; Support limité à son périmètre. |
| Commerçants | Un commerce Animation seul, un Coffrets seul, un mixte, un en préparation, un avec périmètre retiré et engagements ouverts, un suspendu administrativement ; un salarié du commerce Animation et un autre commerce de remise. |
| Souscriptions/modules | Base active, future et expirée ; modules absent, acheté, offert, en essai et expiré ; dernier crédit disponible et quota épuisé ; période annuelle complète et exactement six mois restants au devis. |
| Animations | Un brouillon de chaque dotation ; une publiée puis clôturable par mode ; des populations de 0, 2, 3 et 5 éligibles ; une animation historique Coffrets ; des animations publiées avant retrait de droits. |
| Participants | Parcours non terminé, terminé, gagnant, suppléant ; messages autorisés/refusés ; Push accepté/refusé ; même personne sur plusieurs animations de A1 et plusieurs appareils. Préparer des liens anciens et des accès Live existants. |
| Lots/bons | Trois lots ordonnés dont deux exemplaires du même modèle ; bons valide, expiré, révoqué, consommé et QR remplacé ; anciennes attributions et suppléants disponibles/épuisés. |
| Imports | Deux versions d’un fichier synthétique de 5 lignes, CSV et XLSX ; collisions email/SIRET ; données corrigées localement ; fichiers de 100/101 lignes, de 2 000 000 octets et dépassant cette taille ; un classeur à plusieurs feuilles. |
| Dates/incidents | Invitations de plus de 7 jours, reset de plus d’une heure, premier email gagnant réussi depuis 14 jours, bornes de mois et changement d’heure Paris, campagnes suspendues, traitements interrompus et exports de plus de 30 jours. Préparation accompagnée et traçable. |

Chaque scénario peut modifier son jeu. Préparer une copie distincte avant les tests de révocation, consommation, fermeture et expiration ; ne pas réutiliser un bon consommé pour le cas « bon valide » suivant.

### Ordre recommandé et façon de consigner les résultats

1. Vérifier l’environnement et préparer les profils ; exécuter F01–F08 pour les accès, périmètres et droits commerciaux.
2. Réaliser les parcours complets F09–F14 : externe, numérique puis régression Coffrets.
3. Tester les modules F15–F17, puis les parcours publics et le pilotage F18–F23.
4. Utiliser des jeux dédiés pour F24 et les retraits/fermetures. Terminer par F25, les contrôles transverses et la validation du pilote.

Les lignes marquées **accompagné** nécessitent le référent technique ou un opérateur Localeo. Elles restent de la recette métier pour leur résultat observable ; elles ne remplacent pas les tests automatisés de concurrence, de sécurité, de pagination ou de conservation.

Pour chaque `RM-*`, enregistrer : date, recetteur, versions, compte/rôle, organisation/commune, références d’objets, résultat observé, statut **À exécuter / Validé / Échec / Bloqué**, preuve et anomalie éventuelle. Lorsqu’une ligne contient plusieurs variantes, consigner chaque variante séparément ; la ligne n’est validée que lorsque toutes le sont.

### Utiliser les marches à suivre

Chaque test dispose ci-dessous d’une marche numérotée. Lire d’abord les prérequis de sa fiche, puis exécuter les étapes dans l’ordre. Le **scénario** rappelle la couverture d’origine ; le **résultat attendu** reste la référence pour décider du succès. Les étapes ajoutées aux tests déjà réussis documentent le parcours sans annuler leur validation ni annoncer une nouvelle exécution.

- Ouvrir les URL de l’environnement désigné au début de la campagne. Les noms Animation, ERP, Pro, Live, OnBoard, Support et Ops désignent ces applications ; ne pas mélanger leurs versions test, démo et production.
- Utiliser des profils ou fenêtres privées distincts pour changer de rôle. Quand le test exige une session déjà ouverte, conserver cette fenêtre et effectuer le changement de droit depuis une autre session.
- Relever la référence des objets avant de les modifier. Pour des variantes incompatibles (bon valide/consommé/révoqué, droit actif/expiré), préparer des exemplaires ou jeux séparés.
- Si un écran, une action ou un jeu indispensable manque, noter **Bloqué**, la raison et le référent chargé de la préparation. Une vérification API accompagnée peut établir le comportement serveur ; elle ne valide pas un parcours utilisateur absent.
- Après chaque test, consigner les observations et une preuve sans mot de passe, PIN, QR utilisable, token ou donnée personnelle réelle. Un résultat attendu écrit dans ce document n’est pas une preuve d’exécution.

## F01 — Connexion et récupération du compte organisateur

**Objet.** Permettre au membre de l’équipe de retrouver son accès sans créer de doublon ni maintenir une ancienne session après changement de mot de passe.

**Accès.** Connexion du portail Animation → mot de passe oublié ; compte connecté → gestion du mot de passe. **US25 ; CA50–51.**

**Prérequis à vérifier**

- [ ] Un compte organisateur actif, sa boîte email et deux sessions ouvertes sur des navigateurs distincts.
- [ ] Un autre compte indépendant et des liens de réinitialisation valides/expirés préparés sans exposer leurs secrets.
- [ ] L’envoi des emails et l’URL de retour vers le portail fonctionnent.

### ~~RM-01-01~~ — **Réussi**

**Scénario.** ~~Demander une récupération avec l’email connu puis une adresse inconnue.~~

**Marche à suivre**

Ce parcours documente le test déjà déclaré **Réussi** le 22 octobre 2026. Une nouvelle exécution automatisée sur TEST a également réussi le **23 octobre 2026** ; voir le [bilan d’automatisation](automatisation-recette.md).

1. Prendre l’adresse du compte organisateur A et une adresse synthétique inconnue de Localeo, toutes deux sous le contrôle de l’équipe de recette.
2. Ouvrir la connexion du portail Animation sans session active, choisir **Mot de passe oublié**, saisir l’adresse connue puis **Demander un lien**.
3. Relever le message public sans copier le lien reçu ; revenir à la connexion et refaire exactement la demande avec l’adresse inconnue.
4. Comparer les deux réponses : elles doivent avoir le même contenu public et ne pas indiquer si un compte existe.
5. Dans la boîte du compte connu, ouvrir le message et vérifier que le lien mène au formulaire de réinitialisation ; utiliser RM-01-02 pour sa consommation.
6. Faire vérifier par l’opérateur habilité que l’identité connue reste unique et qu’aucun compte n’a été créé pour l’adresse inconnue ; conserver les preuves sans secret.

**Résultat attendu.** ~~Même réponse publique, sans révéler les comptes existants. Le compte connu reçoit un lien utilisable ; aucun nouveau compte n’est créé.~~

### ~~RM-01-02~~ — **Réussi**

**Scénario.** ~~Utiliser un lien valide, définir le nouveau mot de passe, puis réutiliser le lien et tenter l’ancien mot de passe.~~

**Marche à suivre**

Ce parcours documente le test déjà déclaré **Réussi** le 22 octobre 2026. Une nouvelle exécution automatisée sur TEST a également réussi le **23 octobre 2026** ; voir le [bilan d’automatisation](automatisation-recette.md).

1. Prendre le compte organisateur A, ses deux sessions déjà ouvertes dans deux navigateurs et un troisième navigateur connecté avec l’autre compte indépendant.
2. Ouvrir un lien de récupération valide du compte A ; saisir deux fois un nouveau mot de passe conforme dans le formulaire, puis **Enregistrer mon mot de passe**.
3. Vérifier la confirmation, revenir à la connexion et ouvrir une nouvelle session avec ce nouveau mot de passe.
4. Réouvrir le même lien et tenter une seconde réinitialisation : elle doit être refusée et le nouveau mot de passe doit rester inchangé.
5. Dans une fenêtre déconnectée, tenter l’ancien mot de passe : connexion refusée ; revenir ensuite au nouveau pour confirmer l’accès.
6. Dans chacune des deux anciennes sessions A, demander une page privée : une reconnexion doit être requise. Dans la session de l’autre compte, vérifier que la même lecture reste possible.

**Résultat attendu.** ~~Première utilisation réussie, suivantes refusées ; reconnexion avec le nouveau mot de passe. Anciennes sessions du compte invalidées, autre compte inchangé.~~

### RM-01-03

**Scénario.** **Accompagné :** tester le lien avant puis à/après son échéance d’une heure.

**Marche à suivre**

1. Faire préparer par le référent des liens de récupération distincts, non consommés, avec échéances connues : juste avant une heure, exactement à l’échéance et après. Utiliser des comptes ou essais séparés pour ne pas confondre expiration et usage unique.
2. Depuis la connexion Animation, ouvrir le lien encore valable, renseigner un nouveau mot de passe et confirmer avant l’échéance ; vérifier le succès et la reconnexion.
3. Pour chaque lien arrivé à échéance, tenter la même confirmation : relever le refus et vérifier que le mot de passe n’a pas changé.
4. Faire attester par le référent les instants de demande et de tentative ; ne pas modifier l’horloge partagée ni les tables pour fabriquer ces états.
5. Avec le compte du cas expiré, revenir à **Mot de passe oublié**, demander un nouveau lien et utiliser celui reçu normalement.
6. Se reconnecter avec le nouveau mot de passe et consulter **Compte et équipe** : l’organisation, le rôle et les communes doivent être conservés.

**Résultat attendu.** Lien utilisable seulement avant expiration ; nouveau lien demandé par le parcours normal, sans perte de l’appartenance.

### ~~RM-01-04~~ — **Réussi**

**Scénario.** ~~Changer le mot de passe connecté : d’abord avec une preuve d’identité erronée, puis correcte.~~

**Marche à suivre**

1. Connecter le compte organisateur A dans deux navigateurs et l’autre compte dans un troisième ; ouvrir **Compte et équipe** → **Sécurité du compte** dans le premier.
2. Saisir un mot de passe actuel volontairement faux, puis un nouveau mot de passe conforme et sa confirmation ; choisir **Enregistrer mon mot de passe**.
3. Vérifier le refus ; dans une fenêtre distincte, contrôler que l’ancien mot de passe permet toujours la connexion et que le nouveau ne la permet pas.
4. Revenir au formulaire, saisir le véritable mot de passe actuel et confirmer le nouveau ; vérifier le succès et la demande de reconnexion.
5. Solliciter une page privée dans les anciennes sessions du compte A : chacune doit demander une reconnexion ; se reconnecter avec le nouveau mot de passe.
6. Vérifier que l’autre compte conserve sa session et ses droits ; consigner les résultats sans enregistrer les mots de passe.

**Résultat attendu.** ~~Aucun changement sur refus ; succès explicite ensuite et reconnexion requise sur les anciennes sessions du seul compte concerné.~~


Succès de RM-01-01 et RM-01-02 confirmé par l’utilisateur le 22 octobre 2026.

Succès automatisé sur TEST de **RM-01-01, RM-01-02 et RM-01-04** le
**23 octobre 2026**, pour la campagne `e73-20261022-e856fb` ; preuves et limites
dans le [bilan d’automatisation](automatisation-recette.md). RM-02-06 reste
partiel et n’est pas barré.

## F02 — Organisation, équipe et délégations

**Objet.** Donner à chaque collaborateur les seules communes et actions qui lui sont confiées, avec un responsable identifiable et une récupération assistée.

**Accès.** Animation → **Compte et équipe** ; ERP → **Accès Animation**. **US26 ; CA52–53.**

**Prérequis à vérifier**

- [ ] Organisations A/B, communes A1/A2/B1 et comptes responsable, gestionnaire, lecteur et multi-organisations disponibles.
- [ ] Un opérateur ERP habilité peut examiner une demande de rattachement ; emails d’invitation opérationnels.
- [ ] Une tâche programmée non commencée est affectée à un collaborateur révocable.

### RM-02-01

**Scénario.** Déposer une demande d’organisation/communes, tenter d’utiliser A1 avant décision, puis faire valider le rattachement par Localeo.

**Marche à suivre**

1. Préparer avec le référent une organisation synthétique A et son responsable, avec A1 demandée mais non validée ; noter leurs références avant toute décision ERP.
2. Déposer la demande d’organisation et de commune depuis l’entrée de recette effectivement disponible, en renseignant l’organisation, le responsable et A1 ; conserver la référence et l’état d’attente.
3. Si aucun formulaire n’est disponible, marquer le parcours autonome **Bloqué**. Le référent peut déposer la demande par l’API prévue pour vérifier le rattachement, mais ce contrôle accompagné ne valide ni le formulaire ni son UX.
4. Avec le compte demandeur, tenter d’ouvrir A1 puis un lien direct vers sa gestion : aucun droit ne doit provenir de la seule demande.
5. Avec l’opérateur habilité, ouvrir ERP → **Accès Animation**, examiner l’autorité du demandeur et faire valider explicitement le rattachement à A1 ; garder la preuve de décision.
6. Recharger le contexte du responsable dans Animation : seule A1 validée doit être accessible. Vérifier que A2 et B1 restent interdites tant qu’elles ne sont pas accordées.

**Résultat attendu.** La demande seule n’ouvre aucun droit ; seuls les rattachements validés deviennent accessibles.

### RM-02-02

**Scénario.** Inviter un nouveau collaborateur Gestionnaire sur A1 ; accepter ; comparer à un Lecteur et à un Gestionnaire sans Achat/Import/Communication.

**Marche à suivre**

1. Connecter le responsable A dans Animation → **Compte et équipe**, sélectionner A et choisir **Inviter un collaborateur**.
2. Saisir un nouvel email de test, choisir le profil **Gestionnaire**, cocher uniquement A1 et laisser les autorisations complémentaires non cochées ; confirmer l’invitation.
3. Ouvrir l’email dans un navigateur distinct ou une fenêtre privée, choisir **Créer mon premier accès**, définir le mot de passe puis **Créer mon accès et accepter**. Se connecter ensuite avec l’email invité ; vérifier dans **Compte et équipe** le profil, A1 et l’absence d’autorisations complémentaires. Si le lien est ouvert dans une session existante, lire le bloc **Compte connecté** : lorsque c’est celui du responsable qui a envoyé l’invitation, choisir **Changer de compte**, attendre la déconnexion puis créer le premier accès. Ne pas utiliser **Accepter avec mon compte connecté** avec le compte de l’invitant. Une déconnexion échouée doit proposer **Réessayer** et empêcher la création tant qu’elle n’est pas confirmée ; l’invitation reste disponible dans cet onglet après la reprise.
4. Avec ce gestionnaire, modifier un brouillon autorisé de A1 ; tenter ensuite les parcours Achat, Import commerçants et Communication : ils doivent rester refusés sans leurs délégations.
5. Avec le lecteur A1 sans délégation, consulter le même brouillon puis tenter une modification : consultation autorisée, écriture refusée, y compris depuis un lien direct.
6. Faire accorder un module à A1 sans modifier l’équipe puis reconnecter le gestionnaire : l’achat du module ne doit ajouter aucune permission personnelle. Comparer avec les collaborateurs explicitement délégués.

**Résultat attendu.** Rôle et commune exacts, lecteur sans écriture ; les permissions complémentaires ne viennent pas automatiquement avec le rôle ou l’achat d’un module.

### RM-02-03

**Scénario.** Inviter un email déjà associé à un compte, accepter avec ce compte ; renvoyer une autre invitation et essayer l’ancien lien ; essayer un lien expiré de 7 jours.

**Marche à suivre**

1. Prendre un compte déjà membre de B, un nouveau destinataire pour le renvoi et une invitation d’organisation de plus de sept jours préparée par le référent ; conserver les liens hors du rapport.
2. Avec le responsable A, ouvrir **Compte et équipe**, inviter l’email déjà connu sur A1, puis ouvrir son invitation dans un navigateur déconnecté.
3. Choisir **J’ai déjà un compte : me connecter**, utiliser le compte correspondant puis vérifier l’email dans **Compte connecté** avant **Accepter avec mon compte connecté** ; vérifier que A et B restent accessibles avec cette même identité. Rejouer avec le lien ouvert sous le compte de l’invitant : **Changer de compte**, attendre la déconnexion puis se connecter avec le destinataire doit ramener à la même invitation, sans la recopier ni la renvoyer.
4. Inviter le second destinataire, conserver son premier email puis renvoyer cette invitation depuis le suivi d’équipe ; ouvrir le premier lien et vérifier son refus.
5. Ouvrir le nouveau lien de ce second destinataire et vérifier qu’il permet l’acceptation normale, avec uniquement les droits proposés.
6. Tenter l’invitation d’organisation de plus de sept jours : elle doit être refusée sans créer d’appartenance ; demander un nouveau lien par le parcours normal si la suite du jeu en nécessite un.

**Résultat attendu.** Compte existant réutilisé après acceptation ; autres appartenances préservées ; ancien lien remplacé et lien expiré refusés.

### RM-02-04

**Scénario.** Retirer une autorisation avec la session du collaborateur ouverte ; ajouter A2 à l’organisation sans l’ajouter au collaborateur ; tenter un lien direct hors droit.

**Marche à suivre**

1. Préparer un collaborateur A1 doté de Communication, une campagne programmée non commencée et une campagne déjà commencée à audience figée ; garder sa session Animation ouverte.
2. Avec le responsable A dans **Compte et équipe**, modifier l’accès du collaborateur, retirer Communication puis confirmer.
3. Sans reconnecter le collaborateur, tenter une nouvelle action de communication dans son onglet ouvert puis un lien direct mémorisé : le refus doit intervenir dès la prochaine requête.
4. Faire valider A2 pour l’organisation sans l’ajouter au collaborateur ; actualiser sa session et tenter A2 : la commune doit rester hors de ses droits.
5. Avec un acteur toujours habilité, lire le suivi des campagnes : la campagne non commencée doit être suspendue ; le référent vérifie la poursuite contrôlée des seuls destinataires déjà engagés dans l’autre.
6. Retenter le pilotage ou l’extension de cette campagne avec le compte privé de Communication : la continuité technique ne doit pas lui rendre son autorisation.

**Résultat attendu.** Refus dès la prochaine requête ; A2 non accordée implicitement ; tâches non commencées nécessitant le droit suspendues. Les traitements déjà engagés suivent leur continuité contrôlée, sans redonner la main au compte révoqué.

### ~~RM-02-05~~ — **Réussi**

**Scénario.** ~~Proposer un transfert de responsabilité ; tenter le départ du dernier responsable avant acceptation ; faire accepter le successeur actif.~~

**Marche à suivre**

1. Préparer A avec un seul responsable et un collaborateur actif pouvant lui succéder ; connecter chacun dans un navigateur distinct.
2. Avec le responsable, ouvrir **Compte et équipe** et proposer la responsabilité au collaborateur choisi ; confirmer la proposition.
3. Avant acceptation, actualiser l’équipe : l’ancien responsable doit encore porter ce rôle et la proposition doit rester en attente.
4. Tenter le retrait ou la rétrogradation du dernier responsable. Si l’action n’est pas exposée, faire vérifier le refus de la commande prévue par le référent ; aucune organisation sans responsable ne doit en résulter.
5. Avec le successeur connecté, ouvrir la proposition dans **Compte et équipe**, choisir **Accepter la responsabilité** et confirmer.
6. Actualiser les deux sessions et faire relire l’historique : la responsabilité doit avoir basculé après acceptation, avec auteur et date, et A doit conserver un responsable actif.

**Résultat attendu.** ~~Ancien responsable maintenu avant acceptation, départ bloqué ; transfert tracé après acceptation, aucune organisation sans responsable.~~

**Exécution automatique réussie du 23 octobre 2026.** Après correction de l’attente du frontend, un parcours inverse distinct sur l’organisation dédiée T de la campagne `e73-20261022-e856fb` a vérifié proposition en attente, refus du départ du dernier responsable, acceptation, droits des deux sessions et responsable unique. Les traces ERP de proposition et d’acceptation ont été rapprochées par auteur, date et version. Le premier rapport en échec reste conservé. Voir le [suivi d’automatisation](automatisation-recette.md#reprise-du-23-octobre).

### RM-02-06

**Scénario.** **Accompagné :** simuler la perte des accès responsables et demander une récupération ; changer ensuite d’organisation avec le compte multi-organisations.

**Marche à suivre**

1. Faire préparer par le référent une organisation de recette dont les responsables ont perdu l’accès, ainsi qu’un demandeur légitime et un compte explicitement membre de A et B ; conserver une voie opérateur de récupération.
2. Déposer la demande de récupération auprès de Localeo avec la référence de l’organisation existante et les éléments d’autorité prévus ; ne pas créer une deuxième organisation.
3. Avec l’opérateur habilité dans ERP → **Accès Animation**, faire vérifier ces éléments puis réattribuer la responsabilité par le parcours de récupération prévu.
4. Reconnecter le responsable rétabli, contrôler l’identifiant de l’organisation et ses communes ; faire vérifier la trace de réattribution et l’absence de doublon.
5. Avec le compte multi-organisations, ouvrir **Compte et équipe** → **Mes organisations**, choisir A, puis ouvrir une animation de A1 et relever sa référence.
6. Revenir à **Mes organisations**, choisir B et consulter B1 ; vérifier le nouveau contexte, l’absence d’objets A affichés comme objets B et le refus d’un ancien lien A dans ce contexte.

**Résultat attendu.** Localeo vérifie l’autorité du demandeur et trace la réattribution ; aucune organisation doublonnée, aucun objet de l’ancien contexte affiché comme appartenant au nouveau.


## F03 — Activation des périmètres commerçants depuis l’ERP

**Objet.** Choisir Animation, Coffrets ou les deux pour chaque commerce, sans lui ouvrir des fonctions dont les prérequis ne sont pas satisfaits.

**Accès.** ERP → fiche commerçant → périmètres. **US11 ; CA15, 17, 22 ; reprise historique en F25.**

**Prérequis à vérifier**

- [ ] Commerces distincts sans périmètre prêt, Animation seul et mixte ; leurs prérequis sont identifiés.
- [ ] Administrateur, Backoffice habilité et Backoffice non habilité disponibles ; compte commerçant ouvert en parallèle.
- [ ] Motifs et historique des changements consultables dans l’ERP.

### RM-03-01

**Scénario.** Faire demander/activer Animation par l’administrateur puis par le Backoffice habilité ; refaire sans habilitation et depuis Pro.

**Marche à suivre**

1. Préparer deux commerces synthétiques dont les prérequis Animation sont validés, ainsi qu’un troisième réservé au refus ; conserver une session Pro du principal.
2. Avec l’administrateur, ouvrir ERP → fiche du premier commerçant → périmètres, demander Animation puis activer en renseignant un motif de recette.
3. Avec le Backoffice habilité à gérer les périmètres, effectuer la même demande puis activation sur le deuxième commerce ; vérifier l’état obtenu dans chaque fiche.
4. Avec le Backoffice sans habilitation, ouvrir la fiche du troisième commerce et tenter l’action, y compris par l’entrée directe prévue avec le référent : aucun changement ne doit être accepté.
5. Depuis Pro avec le principal du troisième commerce, tenter de décider l’activation : l’accès commerçant ne doit pas permettre cette décision ERP.
6. Relire l’historique des deux succès et du commerce refusé : auteurs et motifs des décisions doivent être visibles, sans activation issue des tentatives non autorisées.

**Résultat attendu.** Seuls les opérateurs ERP autorisés peuvent décider ; auteur et motif visibles. Le commerce ne s’active pas lui-même.

Complément essentiel du 30 octobre 2026, **partiel sur le clone isolé** :
vingt-six contrôles réussis. Un commerce existant, dont la connexion propriétaire
Pro est réellement vérifiée, reçoit une convention explicitement fictive ; scan
ClamAV réel (PDF accepté, témoin EICAR détecté) et statut serveur CLEAN constatés.
Le Backoffice déjà habilité revoit, demande puis active Animation : version
1 → 4, auteurs et motifs rapprochés avec l’historique. Le mode HISTORIQUE est
conservé : ce commerce ne constitue pas un nouveau profil moderne mixte.
État et ouverture Coffrets, prestations, modèles, engagements, six reversements
et capacités Pro restent identiques ; le menu Pro est relu après chargement.
Sur une nouvelle fixture dédiée, la demande Admin est acceptée, puis
l’activation refusée 409 sans effet faute de convention et d’accès propriétaire
qualifiés. Aucun prérequis n’est attesté sans preuve. Activation Admin, refus
Backoffice sans habilitation et décision depuis Pro restent non exécutés :
scénario non barré. La base de signatures antivirus préexistante est signalée
ancienne de plus de sept jours ; aucune actualisation revendiquée. Preuves
`essentiels-rm0301-preuves-finales/index.json`, dix-huit pièces figées et revue
indépendante sans écart bloquant pour ce statut partiel.

### RM-03-02

**Scénario.** Ajouter Coffrets à un commerce Animation dont les compléments Coffrets sont incomplets ; terminer les prérequis puis activer.

**Marche à suivre**

1. Prendre un commerce Animation actif, avec une participation utilisable, et des compléments Coffrets manquants identifiés dans OnBoard.
2. Avec l’opérateur ERP habilité, ouvrir sa fiche → périmètres et demander Coffrets avec un motif ; vérifier que le produit passe en préparation.
3. Tenter l’activation Coffrets avant correction : relever le refus et le diagnostic des compléments attendus.
4. Avec le commerçant dans Pro, poursuivre une action Animation autorisée sur le jeu préparé ; le chantier Coffrets ne doit pas interrompre ce périmètre.
5. Compléter dans OnBoard les seules exigences Coffrets applicables et les faire valider par l’acteur compétent, puis revenir à la fiche ERP.
6. Activer Coffrets, actualiser Pro et contrôler l’accès aux fonctions du produit nouvellement validé, tout en conservant Animation et l’historique du commerce.

**Résultat attendu.** Coffrets reste en préparation jusqu’à validation ; Animation continue de fonctionner ; le diagnostic indique les compléments attendus.

### ~~RM-03-03~~ — **Réussi sur le clone isolé**

**Scénario.** ~~**Accompagné :** deux opérateurs modifient la même fiche depuis des versions ouvertes avant la première modification.~~

**Marche à suivre**

1. Avec le référent, choisir un commerce de recette et deux opérateurs ERP habilités ; faire ouvrir sa fiche de périmètres dans deux navigateurs avant toute modification.
2. Relever l’état initial commun, puis faire enregistrer par le premier opérateur une demande ou décision avec son motif.
3. Dans le second navigateur, conserver la fiche non actualisée et soumettre une décision différente avec un autre motif.
4. Vérifier que cette seconde décision ne remplace pas silencieusement la première : un conflit ou une relecture doit être demandé.
5. Actualiser la seconde fiche, contrôler la première décision et, si nécessaire au jeu, soumettre à nouveau une décision devenue explicite après cette relecture.
6. Relire l’historique avec le référent : états, ordre, auteurs et motifs doivent correspondre aux seules décisions effectivement acceptées.

**Résultat attendu.** ~~Le second ne remplace pas silencieusement la première décision ; conflit/relecture explicite, historique cohérent.~~

Preuve du 30 octobre 2026 : deux opérateurs internes distincts et habilités,
connectés normalement, ouvrent le même commerce synthétique à la version 2.
La demande Animation du premier réussit vers la version 3 ; la demande
Coffrets du second, envoyée avec la version 2, reçoit **409 CONFLIT_VERSION**.
L’état et l’historique restent identiques après ce refus, avec la seule demande
acceptée ajoutée et son auteur/motif exacts. La relecture réelle de l’écran B
confirme Animation « À préparer », Coffrets « Non demandé » et l’historique.
Mode PERIMETRES déjà présent, commune déjà basculée : aucune bascule exécutée.

Le navigateur initial a été fermé après un délai d’attente du harnais.
Le même opérateur B s’est reconnecté ; les mêmes objets, états et historiques
ont été vérifiés inchangés avant de reconstituer une saisie sans la soumettre,
puis d’accepter la confirmation native d’actualisation. Aucune commande métier
rejouée pendant cette récupération ; les initialisations techniques de session
bloquées sont distinguées des écritures métier. Les incidents restent conservés.
**48 contrôles réussis**, six étapes revues indépendamment ; dix pièces avec
empreintes vérifiées dans les index privés
`essentiels-rm0303-20261030b-reprise2-index.json` et
`essentiels-rm0303-20261030b-relecture2-index.json`.
Aucune modification du TEST partagé ; cette preuve porte sur le clone figé.


## F04 — Onboarding adapté au produit

**Objet.** Accueillir un commerce Animation sans lui imposer les prestations et pièces propres aux Coffrets, puis demander les compléments utiles s’il ajoute ce produit.

Évolution du **1er novembre 2026 — OA-01 à OA-04** : les scénarios ci-dessous
appliquent le parcours Animation sans contrat, Stripe ni rendez-vous imposés.
Les preuves antérieures restent historiques ; elles ne valident pas à elles
seules cette évolution. Les nouvelles preuves locales figurent dans le
[suivi d’implémentation](suivi-implementation.md).

**Accès.** OnBoard → dossier commerçant ; Pro → préparation du dossier lorsque proposée. **US12 ; CA16–18.**

**Prérequis à vérifier**

- [ ] Un dossier Animation seul sans contrat et un dossier mixte avec convention Coffrets synthétique appropriée.
- [ ] Accès opérateur OnBoard et responsable du commerce ; boîtes de réception de test.
- [ ] Les supports Animation et Coffrets sont disponibles ; les envois facultatifs disposent de destinataires de test contrôlés et d’un aperçu approuvé.

### RM-04-01

**Scénario.** Compléter identité, responsable, coordonnées et engagements Animation, sans prestations ni pièces bancaires Coffrets.

**Marche à suivre**

1. Avec l’opérateur OnBoard, ouvrir le dossier synthétique du commerce demandant uniquement Animation ; confirmer le produit visé avant de remplir la checklist.
2. Renseigner l’identité, la commune, le responsable, les coordonnées et les informations utiles à sa participation ; utiliser exclusivement des données de recette.
3. Avec le responsable du commerce, initialiser puis tester l’accès Pro. Ne fournir aucun contrat ni convention Animation.
4. Faire vérifier les coordonnées et prérequis d’accès par les acteurs compétents ; laisser contrat, Stripe, prestations Coffrets, rendez-vous, pack et bilan non renseignés.
5. Examiner le diagnostic et finaliser le dossier : ces éléments non applicables ne doivent pas bloquer. Vérifier que la finalisation ne décide pas elle-même l’ouverture du produit.
6. Faire contrôler l’ouverture Animation par l’opérateur ERP habilité, puis vérifier dans Pro les fonctions Animation ; conserver la checklist démontrant l’absence de blocage artificiel.

**Résultat attendu.** Dossier Animation recevable lorsque ses propres prérequis sont remplis ; aucun blocage bancaire/Coffrets artificiel.

Complément de référencement : créer un nouveau commerce en choisissant Animation,
Coffrets puis les deux avec un opérateur habilité. Vérifier demande en préparation,
dossier unique et audit, sans activation ni invitation supplémentaire. Sans droit
de gestion des périmètres, la sélection n’est pas proposée et une requête directe
avec produit est refusée ; la création historique reste disponible. Reprendre un
commerce existant ne doit pas modifier son périmètre par le seul choix du formulaire.

### RM-04-02

**Scénario.** Omettre un prérequis Animation puis tenter l’activation ; le compléter et faire vérifier le dossier.

**Marche à suivre**

1. Préparer un dossier Animation distinct, avec un prérequis obligatoire précis encore manquant, par exemple l’accès Pro non testé ou une adresse incomplète ; noter ce manque avec le référent.
2. Avec l’opérateur OnBoard, ouvrir le dossier puis consulter sa préparation ; vérifier que le manque et l’acteur attendu pour le corriger sont compréhensibles.
3. Avec l’opérateur ERP habilité, tenter d’activer Animation depuis les périmètres du commerce : l’activation doit être refusée.
4. Revenir au dossier OnBoard, utiliser l’action de correction disponible et fournir l’élément manquant ; une simple saisie ne doit pas être assimilée à sa validation.
5. Faire effectuer le contrôle effectif de cet élément par l’acteur compétent puis relire la checklist et les prérequis courants.
6. Retenter l’activation ERP et vérifier dans Pro qu’Animation s’ouvre uniquement après la validation ; noter les états avant et après.

**Résultat attendu.** Manque compréhensible et action de correction accessible ; validation effective requise avant ouverture.

### RM-04-03

**Scénario.** Demander ensuite Coffrets, y compris sur un dossier déjà clos ; vérifier les données et compléter les pièces propres au nouveau produit.

**Marche à suivre**

1. Préparer deux commerces Animation actifs : un dossier OnBoard encore ouvert et un dossier déjà clos, avec leurs données communes et preuves initiales relevées.
2. Pour chacun, faire demander Coffrets par l’opérateur ERP habilité puis ouvrir le dossier OnBoard et la préparation Pro proposée au commerçant.
3. Vérifier que l’identité, les coordonnées et les pièces communes sont réutilisées ; identifier les compléments propres aux fonctions Coffrets effectivement visées.
4. Sur le dossier clos, compléter uniquement les rubriques de complément autorisées : son statut clos et ses preuves antérieures doivent rester conservés.
5. Fournir et faire vérifier les compléments requis pour les deux dossiers, puis faire décider l’activation Coffrets dans l’ERP.
6. Avec les deux comptes Pro, vérifier qu’Animation a continué de fonctionner et que l’historique reste présent ; comparer les données initiales pour exclure toute remise à zéro.

**Résultat attendu.** Données communes réutilisées, compléments ciblés ; pas de remise à zéro du dossier ni d’interruption d’Animation.

### RM-04-04

**Scénario.** Préparer une communication facultative Animation, puis les communications et la convention Coffrets d’un dossier mixte ; consulter leur suivi.

**Marche à suivre**

1. Prendre les dossiers synthétiques Animation seul sans rendez-vous et mixte, avec leurs destinataires de test et les supports disponibles ; ouvrir chacun dans OnBoard.
2. Préparer l’aperçu de la communication Animation facultative : informations du commerce, accès Pro et participation, sans contrat ni signature ni Stripe. Vérifier le destinataire avant envoi ; une simple lecture ne doit rien envoyer.
3. Confirmer l’envoi vers la boîte contrôlée, puis comparer le message reçu, les documents et leur suivi dans OnBoard : le contenu doit couvrir Animation sans exigences Coffrets étrangères.
4. Refaire la préparation et l’envoi pour le dossier mixte ; vérifier que les exigences Coffrets et la convention Coffrets sont explicites, sans seconde convention Animation. L’ajout Coffrets après un aperçu Animation rend cet aperçu inutilisable jusqu’à une nouvelle préparation appropriée.
5. Sur un envoi distinct, faire préparer par le référent un échec contrôlé du transport de test, puis soumettre l’envoi normalement ; ne pas toucher aux destinataires réels ni à la configuration partagée.
6. Relire le suivi : l’échec doit être visible et distinct d’un succès, avec historique conservé ; joindre les références des envois sans recopier de données d’accès.

**Résultat attendu.** Contenu adapté aux produits et communication Animation facultative ; convention Coffrets seule pour le mixte. Un échec d’envoi n’apparaît pas comme un succès et le suivi reste conservé.


## F05 — Localeo Pro : fonctions utiles et continuité des engagements

**Objet.** Présenter au commerçant et au salarié uniquement les actions autorisées, tout en permettant d’honorer les engagements antérieurs à un retrait commercial.

**Accès.** Pro → compte commerçant/salarié, scan et historique ; ERP pour retrait/suspension. **US11, US13 ; CA19–22.**

**Prérequis à vérifier**

- [ ] Comptes Animation seul, Coffrets seul, mixte et salarié actif ; invitations salariés déjà initialisées.
- [ ] Animation publiée avec participation acceptée, bon déjà attribué et coffret vendu avec prestation engagée.
- [ ] Jeux distincts pour retrait de périmètre et suspension administrative ; sessions Pro ouvertes avant les changements.

### RM-05-01

**Scénario.** Ouvrir Pro avec chacun des trois périmètres ; parcourir menus et liens directs vers les fonctions absentes.

**Marche à suivre**

1. Préparer trois sessions Pro distinctes pour les principaux des commerces Animation seul, Coffrets seul et mixte ; noter les produits actifs de chacun dans l’ERP.
2. Avec Animation seul, parcourir l’accueil, le scan et les fonctions Animation ; vérifier que prestations et reversements Coffrets ne sont pas proposés hors droit.
3. Avec Coffrets seul, parcourir les fonctions Coffrets et vérifier qu’aucune fonction Animation n’est accordée implicitement ; avec le commerce mixte, contrôler la présence des deux familles autorisées.
4. Depuis les comptes non habilités, ouvrir les liens directs de fonctions disponibles au commerce mixte : le refus doit être effectif et ne pas dépendre seulement du menu masqué.
5. Pour chaque compte, ouvrir les fonctions autorisées de compte, aide et historique, ainsi que la préparation lorsqu’un complément est demandé.
6. Comparer les menus et résultats avec les périmètres ERP, en consignant séparément les trois profils et chaque accès refusé.

**Résultat attendu.** Navigation adaptée, sans fonctions étrangères ; liens directs également refusés. Compte, aide, préparation et historique autorisés restent accessibles.

### RM-05-02

**Scénario.** Connecter le salarié et scanner ; tenter administration, finances, gestion de droits et action d’un autre commerce.

**Marche à suivre**

1. Prendre le salarié actif du commerce Animation, son invitation déjà initialisée, un passage ou bon valide de son commerce et un objet réservé à un autre commerce.
2. Se connecter à Pro avec le salarié ; vérifier l’arrivée sur **Scanner** et l’accès à **Historique** uniquement selon ses droits.
3. Scanner l’objet valide du commerce, vérifier sa nature et l’action proposée puis effectuer la validation autorisée ; relire le résultat dans l’historique accessible.
4. Tenter d’ouvrir l’administration du commerce, les finances et les réglages de droits ou de PIN, notamment avec les liens directs fournis pour le jeu : ces actions doivent être refusées.
5. Scanner l’objet de l’autre commerce et tenter sa validation : le salarié doit rester limité au commerce auquel il appartient.
6. Relire l’état des deux objets avec un acteur habilité : seule l’action autorisée doit avoir produit un effet, sans privilège ajouté au salarié.

**Résultat attendu.** Accès direct au scan, historique selon ses droits, aucune élévation de privilèges. Le salarié reste limité à son commerce.

### RM-05-03

**Scénario.** Faire participer un commerce Animation seul à une animation dotée en coffrets et valider un passage.

**Marche à suivre**

1. Prendre un commerce Animation seul actif et une animation dotée en coffrets dans A1 ; préparer un participant de test pouvant effectuer un passage.
2. Avec le gestionnaire autorisé, ouvrir Animation → **Animations**, sélectionner l’animation et préparer la participation de ce commerce suivant le parcours prévu.
3. Avec le commerçant dans Pro, accepter sa participation si l’accord est demandé ; vérifier que la participation est acceptée avant le passage.
4. Avec le participant, ouvrir son parcours et présenter le QR prévu ; dans Pro, scanner et confirmer le passage autorisé.
5. Contrôler la progression du participant et l’historique Pro : le passage doit être enregistré malgré la dotation Coffrets de l’animation.
6. Relire les périmètres ERP du commerce et tenter une fonction de fournisseur Coffrets : le commerce doit rester Animation seul, sans nouvelle capacité de prestation Coffrets.

**Résultat attendu.** Passage autorisé par sa participation ; le commerce ne devient pas fournisseur de prestations Coffrets.

### RM-05-04

**Scénario.** Retirer Animation pendant une session ouverte ; tenter un nouvel engagement, un passage d’une participation déjà acceptée à une animation publiée et une remise de bon déjà attribué.

**Marche à suivre**

1. Préparer un commerce Animation actif avec participation déjà acceptée à une animation publiée, un bon déjà attribué encore valide et un nouvel engagement à tenter ; garder sa session Pro ouverte.
2. Avec l’opérateur ERP habilité, retirer le périmètre Animation avec un motif et relever l’heure ainsi que les références des engagements antérieurs.
3. Dans la session Pro toujours ouverte, tenter une nouvelle participation ou affectation : le serveur doit la refuser immédiatement.
4. Sur la participation antérieure, présenter un nouveau passage valide puis le confirmer : il doit rester possible tant que l’animation n’est pas clôturée.
5. Sur le bon antérieur, réaliser la remise par le parcours QR/PIN prévu et contrôler son reçu ; la continuité reste limitée à ce bon, à sa validité et aux habilitations personnelles.
6. Avec le référent, contrôler aussi une participation clôturée ou un bon hors validité sur des objets distincts : aucun accès général ne doit être rétabli. Relire l’historique et les refus.

**Résultat attendu.** Nouvel engagement refusé immédiatement côté serveur ; seules les continuités prévues fonctionnent jusqu’à leurs limites. Aucun droit nouveau déduit de la session.

### RM-05-05

**Scénario.** Retirer Coffrets avec une prestation déjà engagée dans un coffret vendu ; consulter règlement et historique, puis tenter un nouvel engagement.

**Marche à suivre**

1. Prendre le commerce Coffrets actif avec une prestation déjà engagée dans un coffret vendu et encore valide, ainsi qu’un principal habilité à consulter les règlements.
2. Garder Pro ouvert puis faire retirer Coffrets dans la fiche ERP par un opérateur habilité, avec motif et références de l’engagement protégé.
3. Depuis la session existante, ouvrir la prestation antérieure et effectuer l’action d’exécution encore autorisée selon le parcours Coffrets ; vérifier la confirmation.
4. Consulter le règlement et l’historique de cet engagement : les lectures autorisées doivent rester accessibles selon le rôle.
5. Tenter un nouvel engagement ou référencement de prestation Coffrets : le retrait doit l’interdire, y compris depuis un lien déjà ouvert.
6. Relire les états avec l’opérateur : le nouvel engagement ne doit pas exister et la continuité ne doit pas étendre la validité ni les habilitations de l’ancien.

**Résultat attendu.** Prestation antérieure et consultation autorisée préservées selon validité et habilitations ; nouvel engagement refusé.

### RM-05-06

**Scénario.** Suspendre administrativement le commerce d’un jeu de continuité puis retenter QR/PIN.

**Marche à suivre**

1. Préparer un commerce dont le périmètre a été retiré mais qui conserve une participation ou remise antérieure admissible ; réserver des objets distincts non consommés pour les essais QR et PIN.
2. Avec le principal ou salarié habilité dans Pro, vérifier que le jeu présente bien une continuité commerciale avant suspension, sans consommer les objets réservés.
3. Faire suspendre administrativement ce commerce par l’opérateur ERP compétent ; conserver la session Pro ouverte.
4. Présenter le QR de l’objet réservé et tenter validation ou remise : la suspension doit interdire l’opération malgré l’engagement antérieur.
5. Refaire le contrôle par le parcours PIN sur l’autre objet, avec le participant de test : le PIN ne doit pas contourner la suspension.
6. Faire relire les objets et l’historique par l’acteur habilité : aucune validation ou remise nouvelle ne doit avoir été enregistrée après la suspension.

**Résultat attendu.** La suspension prime sur les droits résiduels ; aucune remise ou validation n’est autorisée grâce à l’exception commerciale.


## F06 — Catalogue : forfaits, modules et conditions acquises

**Objet.** Rendre lisible ce qui est inclus, optionnel ou déjà acquis, sans changer rétroactivement les droits d’un client.

**Accès.** Animation → **Abonnement** ; ERP → catalogue/modules. **US03, US14 ; CA12–14, 37.**

**Prérequis à vérifier**

- [ ] Catalogue initial chargé et souscriptions antérieure/nouvelle disponibles.
- [ ] Une organisation avec deux communes et un module accordé à A1 seulement.
- [ ] Administrateur catalogue et opérateur non administrateur.

### RM-06-01

**Scénario.** Consulter forfait et modules d’une nouvelle souscription ; ouvrir les variantes de scénarios.

**Marche à suivre**

1. Connecter le responsable A sur une nouvelle souscription de A1, puis ouvrir Animation → **Abonnement** ; relever forfait, période et quota standard.
2. Consulter les droits inclus : passeport et tombola doivent relever du quota du forfait, sans ligne d’achat supplémentaire pour ces types.
3. Ouvrir **Modèles** ou la création d’animation et comparer les variantes de passeport et tombola proposées ; leur droit doit rester celui du type correspondant.
4. Revenir à **Abonnement** et lire chasse, import et communication : pour cette nouvelle souscription, ces trois modules doivent être présentés comme optionnels.
5. Sur un jeu où Chasse est acquis, ouvrir plusieurs variantes de chasse : elles ne doivent pas demander un achat distinct par scénario et doivent utiliser le droit Chasse.
6. Comparer les récapitulatifs et capacités avec les droits de chaque jeu ; noter les éventuels refus dus à un module absent sans les confondre avec un supplément par variante.

**Résultat attendu.** Passeport/tombola inclus dans le quota du forfait ; chasse, import et communication optionnels. Variantes couvertes par le droit de leur type, pas d’achat supplémentaire par scénario.

Passage principal du 30 octobre 2026, **partiel sur le clone isolé** : dix
contrôles réussis. La nouvelle base B1 inclut Animation sans module optionnel
actif ; Passeport et Tombola s’ouvrent sans achat. Sur A2, Chasse s’ouvre avec
le droit acquis. Droits, versions, échéances et usages restent inchangés après
les ouvertures. Le catalogue ne propose qu’un modèle par type : la comparaison
de plusieurs variantes distinctes reste non exécutée, scénario non barré.
Preuve `catalogue-variantes-principal-relecture-20261030.json`.

### ~~RM-06-02~~ — **Réussi**

**Scénario.** ~~Vérifier les offres initiales et leur récapitulatif.~~

**Marche à suivre**

1. Avec le responsable ou le collaborateur Achat de A1, ouvrir **Abonnement** sur une période annuelle complète et consulter les trois modules du catalogue initial.
2. Ouvrir le détail Chasse : contrôler 190 € HT par an, cinq chasses et un quota indépendant de celui du forfait standard.
3. Ouvrir Import commerçants : contrôler 49 € HT par an et l’absence de quota commercial, sans assimiler cela à une absence de limites techniques de fichier.
4. Ouvrir le module de messages aux participants : contrôler 49 € HT par an et cinq campagnes par mois.
5. Préparer les récapitulatifs sans payer ; pour chacun, lire la commune, les dates, les prérequis, les capacités et les montants HT, TVA et TTC.
6. Comparer les trois récapitulatifs au catalogue initial et consigner toute valeur manquante ou ambiguë ; aucun droit ne doit résulter de la seule consultation.

**Résultat attendu.** ~~Chasse : 190 € HT/an, 5 chasses, quota distinct ; import : 49 € HT/an, sans quota commercial ; messages : 49 € HT/an, 5 campagnes/mois. Commune, dates, prérequis, HT/TVA/TTC et capacités sont explicites.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Le collaborateur Achat A1 de la campagne `e73-20261022-e856fb` a consulté les trois modules et leurs devis sur une base annuelle complète. Prix, capacités, commune, échéance et HT/TVA/TTC sont vérifiés ; les droits et la liste des commandes restent inchangés. Rapport privé `run-1792768742029-444b`, détaillé dans le [suivi d'automatisation](automatisation-recette.md#contrôles-des-brouillons-après-déblocage-des-créations).

### ~~RM-06-03~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Avec le module acquis sur A1, tenter l’usage sur A2 ; consulter un droit inclus sans achat.~~

**Marche à suivre**

1. Prendre un gestionnaire autorisé sur A1 et A2, avec les mêmes délégations personnelles sur les deux communes, mais un module Import acquis seulement pour A1.
2. Dans Animation, sélectionner A1, ouvrir **Abonnement** puis **Import commerçants** ; vérifier que le droit de A1 permet d’accéder au parcours.
3. Changer pour A2, ouvrir le même parcours et son lien direct mémorisé : le module de A1 ne doit pas permettre un nouvel import dans A2.
4. Revenir sur un jeu possédant un droit inclus valide, identifié dans **Abonnement**, et ouvrir la fonction correspondante avec le profil habilité.
5. Effectuer une action autorisée par ce droit inclus : elle doit fonctionner sans demander ni créer un paiement fictif pour l’acquérir de nouveau.
6. Parcourir les modules proposés et comparer les origines des droits : seuls les modules officiels Localeo doivent apparaître, sans extension automatique à l’autre commune.

**Résultat attendu.** ~~Aucun droit automatiquement étendu à A2 ; le droit inclus valide fonctionne sans paiement fictif. Seuls les modules officiels Localeo sont proposés.~~


Complément vérifié le 24 octobre 2026 : `droit-inclus-principal-clone-sceau-completude.json`. Les six étapes sont couvertes : même compte et mêmes délégations sur A1/A2, Import accessible uniquement sur A1, refus de création sur A2 sans objet ajouté, trois modules officiels. Droit Animation INCLUS identifié dans Abonnement et fonction ouverte en UI, puis publication réelle du brouillon dédié avec accord Pro normal. Une consommation DEBIT relie la publication au droit inclus et à sa période ; usage 0 à 1. Droits et versions inchangés, aucune nouvelle acquisition ni commande ou paiement pour cette action. Les premières preuves partielles sont conservées. Clone isolé uniquement.

### RM-06-04

**Scénario.** Modifier un prix/quota par l’administrateur ; consulter l’ancienne souscription puis préparer son renouvellement ; tenter la modification sans rôle administrateur.

**Marche à suivre**

1. Relever dans **Abonnement** le prix, le quota, les dates et la version des conditions d’une souscription A1 déjà acquise ; garder une preuve de référence.
2. Avec l’administrateur dans ERP → **Catalogue commercial**, sélectionner la commune et publier une nouvelle version du prix ou quota avec un motif de recette.
3. Recharger l’ancienne souscription dans Animation : ses conditions et usages doivent rester ceux acquis jusqu’à son échéance.
4. Préparer son renouvellement et lire le récapitulatif : les nouvelles conditions doivent être présentées avant toute confirmation ou paiement.
5. Avec un opérateur non administrateur, tenter la modification du catalogue, y compris par l’entrée directe accompagnée si nécessaire : elle doit être refusée.
6. Relire catalogue et historique avec l’administrateur : seule la nouvelle version autorisée doit exister et aucun renouvellement ne doit avoir été accepté implicitement.

**Résultat attendu.** Conditions acquises préservées jusqu’à échéance ; nouvelles conditions présentées au renouvellement pour confirmation ; modification non administrateur refusée.


## F07 — Achat, renouvellement et facturation

**Objet.** Acheter et faire évoluer son offre avec un prix compréhensible, des droits accordés une seule fois et des remboursements contrôlés.

**Accès.** Animation → **Abonnement**, **Finance** ; ERP → souscriptions/remboursements. **US15, US27–28 ; CA38, 54–55.**

**Prérequis à vérifier**

- [ ] Paiement de test et traitement de confirmation opérationnels, autorisation Achat et profil sans Achat.
- [ ] Souscription avec six mois exacts restants, autre proche d’échéance et autre expirée ; commandes de test remboursables.
- [ ] Opérateurs administrateur/Finance avec autorisation de remboursement et pièces de facturation existantes.

### RM-07-01

**Scénario.** Préparer l’achat à six mois restants puis confirmer en mode test.

**Marche à suivre**

1. Faire préparer une base A1 avec exactement six mois calendaires restants au devis ; connecter un responsable ou collaborateur Achat et vérifier le mode de paiement de test.
2. Dans **Abonnement**, demander les devis Chasse, Import et Communication pour cette base ; relever date d’effet et fin de période avant confirmation.
3. Vérifier Chasse à 95 € HT avec trois chasses, puis Import et Communication à 24,50 € HT chacun ; Import reste sans quota commercial et Communication conserve cinq campagnes pour le mois courant.
4. Contrôler HT/TVA/TTC, commune et fin alignée sur la base, puis confirmer les achats prévus avec le fournisseur de test.
5. Au retour, relire l’état des commandes : attendre la confirmation effective serveur avant de considérer les droits ouverts ; le retour navigateur seul ne suffit pas.
6. Consulter **Abonnement** et **Finance** : droits, quotas, échéances et pièces doivent correspondre aux conditions acceptées, avec une seule acquisition par commande.

**Résultat attendu.** Devis chasse : 95 € HT et 3 chasses ; import/communication : 24,50 € HT chacun, capacités correspondantes conservées. Fin alignée sur la base ; droits ouverts après confirmation effective du paiement.

### RM-07-02

**Scénario.** Annuler/faire échouer un paiement ; revenir plusieurs fois sur le succès d’une autre commande ; **accompagné**, rejouer sa confirmation et tester un paiement tardif devenu incompatible.

**Marche à suivre**

1. Avec le profil Achat dans **Abonnement**, préparer des commandes distinctes pour paiement annulé, paiement refusé, paiement réussi et paiement tardif ; faire isoler ces cas par le référent.
2. Annuler la première au fournisseur de test puis faire refuser la seconde avec son scénario de test ; relire les commandes et vérifier l’absence de droit accordé.
3. Payer la troisième, attendre sa confirmation serveur et relever les droits et quotas ; revenir plusieurs fois sur son retour de succès puis recharger **Abonnement**.
4. Faire rejouer par le référent la confirmation fournisseur de cette même commande via le dispositif de test prévu : aucun deuxième droit, paiement ou rechargement ne doit apparaître.
5. Pour la dernière commande, faire préparer une confirmation retardée devenue incompatible, par exemple après expiration de la base, sans changer l’horloge partagée ; laisser le référent délivrer cet événement.
6. Lire la commande et les droits : le paiement tardif doit être à rapprocher, sans ouverture ni prolongation silencieuse. Conserver les références d’événements et les états, sans données de paiement sensibles.

**Résultat attendu.** Échec sans droit ; succès unique sans recharge au rejeu. Paiement tardif à rapprocher, pas d’ouverture ou prolongation silencieuse. Le retour navigateur seul ne prouve pas le paiement.

### RM-07-03

**Scénario.** Renouveler avant puis après échéance ; examiner les modules repris au récapitulatif et en retirer un.

**Marche à suivre**

1. Préparer deux bases A1 distinctes : l’une encore active, l’autre expirée, avec modules achetés, essai et cadeau identifiés ; connecter le profil Achat.
2. Pour la base active, ouvrir **Abonnement**, préparer le renouvellement et vérifier que seuls les modules précédemment achetés sont proposés à confirmer.
3. Retirer un module acheté du récapitulatif, contrôler que l’essai et le cadeau ne deviennent pas des achats, puis confirmer et payer en mode test.
4. Lire les dates des deux périodes : la nouvelle doit commencer après l’actuelle, sans chevauchement ; les droits courants doivent rester valables jusqu’à leur échéance.
5. Pour la base expirée, refaire le renouvellement en confirmant explicitement forfait et modules ; payer puis relever l’instant de réactivation.
6. Contrôler que cette période commence à la réactivation, sans facturer l’interruption, et que les pièces et modules correspondent exactement au choix confirmé pour chaque variante.

**Résultat attendu.** Avant : nouvelle période après l’actuelle, sans chevauchement. Après : départ à la réactivation, sans rétrofacturation. Modules achetés proposés à confirmer ; essais/cadeaux jamais transformés automatiquement en achat.

### RM-07-04

**Scénario.** Demander une montée en gamme en cours de période puis une baisse ; comparer échéance et usages déjà consommés.

**Marche à suivre**

1. Avec le profil Achat, ouvrir **Abonnement** sur une base active ayant déjà consommé des usages ; relever offre, échéance, quota et consommation.
2. Demander une montée en gamme et lire le devis du différentiel proratisé pour le temps restant ; vérifier que la date de fin reste celle de la base.
3. Confirmer et payer en mode test, attendre la confirmation serveur puis relire les droits : l’augmentation doit prendre effet après paiement.
4. Comparer les compteurs avant et après : les usages déjà consommés doivent rester déduits et ne pas être remis à zéro.
5. Demander ensuite une baisse de gamme ; vérifier qu’elle est présentée pour le prochain renouvellement et ne réduit pas immédiatement la période en cours.
6. Préparer ce renouvellement, vérifier les nouvelles conditions puis confirmer selon le jeu prévu ; relire les périodes et les pièces pour distinguer la montée immédiate de la baisse future.

**Résultat attendu.** Montée après paiement du différentiel proratisé, échéance conservée, usages non remis à zéro ; baisse au prochain renouvellement confirmé.

### RM-07-05

**Scénario.** Vérifier l’échéance sans renouvellement automatique puis demander un remboursement de base ou module ; faire décider un montant partiel/total, et tenter un montant supérieur au solde remboursable.

**Marche à suivre**

1. Préparer des commandes de base et de module payées en test avec soldes remboursables connus ; connecter le profil Achat et les opérateurs administrateur/Finance habilités.
2. Dans **Abonnement**, relever l’échéance et la mention « Sans renouvellement automatique » : aucune démarche d’arrêt n’est nécessaire et aucun bouton d’arrêt à échéance n’est proposé. L’accès de la période court jusqu’à sa fin exclusive ; aucun renouvellement ni remboursement ne part automatiquement. Si une demande d’arrêt historique existe, elle reste indiquée sans modifier ces droits.
3. Déposer séparément les demandes de remboursement des commandes retenues, avec leurs motifs ; les retrouver dans ERP → **Remboursements**.
4. Faire décider un remboursement partiel sur une commande et total sur une autre, par les opérateurs habilités, en saisissant montant et motif ; distinguer décision enregistrée et remboursement effectivement rapproché.
5. Tenter une décision avec un Finance sans autorisation de remboursement, puis un montant supérieur au solde encore remboursable : aucun des deux ne doit être accepté.
6. Avec le référent, faire soumettre deux décisions concurrentes sur le même solde depuis deux dossiers ouverts ; relire les montants réservés et remboursés : leur total ne doit jamais dépasser l’encaissé restant.
7. Contrôler historique, auteur, motif et pièces financières ; vérifier qu’un éventuel retrait commercial demeure une décision distincte avec sa continuité propre.

**Résultat attendu.** Expiration à échéance sans renouvellement ni remboursement automatique. Décision manuelle motivée par administrateur/Finance habilité ; plafond encaissé restant respecté, y compris décisions simultanées accompagnées. Clarification du portail le 31 octobre 2026 ; les preuves historiques d’arrêt et le contrat serveur sont conservés, sans valoir rejeu de la nouvelle présentation.

### RM-07-06

**Scénario.** Modifier les coordonnées de facturation avec Achat puis sans ; comparer ancienne facture et nouveau document ; ouvrir un document de B depuis A.

**Marche à suivre**

1. Préparer une ancienne facture de A, un futur document de test et une facture de B ; connecter deux collaborateurs A, l’un avec Achat et l’autre sans cette autorisation.
2. Avec Achat, ouvrir **Finance** et le parcours des coordonnées de facturation ; remplacer les coordonnées par de nouvelles données synthétiques puis confirmer.
3. Réouvrir l’ancienne facture : ses coordonnées et montants doivent rester inchangés ; conserver sa référence de comparaison.
4. Faire produire le nouveau document par le parcours commercial de test prévu : il doit reprendre les nouvelles coordonnées.
5. Avec le collaborateur sans Achat, tenter la modification via l’entrée disponible ou son lien direct : vérifier le refus et l’absence de changement enregistré.
6. Depuis A, ouvrir le lien de la facture B : aucune pièce ni donnée de facturation de B ne doit être accessible. Consigner les trois contrôles séparément.

**Résultat attendu.** Autorisation requise ; nouvelles coordonnées sur les futurs documents uniquement ; anciennes pièces inchangées, document étranger inaccessible.


## F08 — Cadeaux, essais, cumuls et expiration des droits

**Objet.** Offrir ou faire tester les modules sans facturation cachée ni recharge artificielle, et terminer proprement les opérations déjà engagées.

**Accès.** ERP → octroi de modules ; Animation → **Abonnement** et usages correspondants. **US16–17 ; CA39–41.**

**Prérequis à vérifier**

- [ ] Base active ; opérateurs avec/sans autorisation d’octroi ; droits achetés, cadeaux et essais qui se chevauchent.
- [ ] Animation publiée, import confirmé commencé, campagne commencée et campagne seulement programmée.
- [ ] États d’expiration préparés avec le référent, sans modifier l’horloge commune.

### ~~RM-08-01~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Accorder un essai de chaque module, puis ajuster durée/quota avec motif ; refaire sans habilitation.~~

**Marche à suivre**

1. Préparer une base active couvrant au moins quatorze jours, avec profils ERP autorisé et non autorisé à l’octroi ; ouvrir la souscription puis **Gérer les modules**.
2. Avec l’opérateur habilité, accorder successivement un **Essai** de Chasse, Import et Communication en laissant durée/quota par défaut et en renseignant un motif.
3. Lire les droits dans ERP et Animation → **Abonnement** : durée de quatorze jours, une chasse, une campagne sur tout l’essai et aucun quota commercial d’import.
4. Utiliser **Modifier cet octroi** pour ajuster durée et quota avec motif ; vérifier la conservation des versions et usages dans l’historique.
5. Tenter une fin au-delà de la base : le dépassement doit être refusé ou présenter une borne corrigée avant confirmation, sans prolonger la base.
6. Refaire un octroi ou ajustement avec l’opérateur non habilité : refus ; vérifier dans **Finance** qu’aucune facture ni conversion en achat n’est créée par ces essais.

**Résultat attendu.** ~~14 jours par défaut ; chasse 1 et communication 1 au total, import sans quota commercial. Ajustements tracés, bornés par la base ; aucune facture ou conversion en achat implicite ; refus sans habilitation.~~

**Exécution réussie du 24 octobre 2026 sur le clone isolé.** Les trois essais
accordés normalement ont été ajustés dans les formulaires ERP : durée réduite,
quotas Chasse et Communication portés à deux, Import sans quota commercial.
Identifiants conservés, versions incrémentées, auteur et motif dans l’historique,
usages conservés et lectures client concordantes. Fin au-delà de la base refusée
422 dans le formulaire et par l’API ; ajustement refusé 403 à un opérateur
nominatif existant sans habilitation, sans formulaire accessible. Commandes et
factures inchangées. Six étapes reliées aux dix artefacts privés de
`rm0801-principal-preuves-figees-20261024/index.json` ; revue indépendante effectuée.

### RM-08-02

**Scénario.** Offrir les modules jusqu’à fin de base puis sur une durée plus courte.

**Marche à suivre**

1. Préparer des bases actives distinctes pour les cadeaux jusqu’à fin de base et ceux de durée plus courte, dont une période commençant en cours de mois ; noter les dates prévues.
2. Avec l’opérateur ERP habilité, ouvrir chaque souscription → **Gérer les modules** et accorder Chasse, Import et Communication en choisissant **Cadeau**, avec motif.
3. Pour la première série, laisser la fin sur celle de la base ; pour la seconde, saisir une date de fin plus courte et vérifier les dates proposées avant confirmation.
4. Dans **Abonnement**, contrôler le quota Chasse : cinq par année offerte, proratisés et arrondis au supérieur ; faire vérifier le calcul à partir des dates retenues.
5. Contrôler Communication à cinq campagnes par mois, premier mois incomplet compris, et Import sans quota commercial ; vérifier qu’aucune fin de module ne prolonge la base.
6. Ajuster un quota de cadeau avec motif via l’opérateur habilité ; relire historique, dates et capacités explicites, sans création de facture ni achat automatique.

**Résultat attendu.** Chasse : 5/an au prorata arrondi au supérieur ; communication : 5/mois par défaut, premier mois incomplet compris ; import sans quota. Quotas ajustables et dates explicites, sans prolonger la base.

### RM-08-03

**Scénario.** Consommer sous un droit, ajouter un droit comparable puis laisser finir l’essai.

**Marche à suivre**

1. Préparer trois jeux Chasse sur un même terme : essai 1 puis achat 5 ; cadeau 3 puis achat 5 ; essai ajusté à 8 avec achat actif 5. Utiliser des bases et références distinctes.
2. Sur le premier, publier une chasse autorisée pendant l’essai, puis acquérir le droit acheté ; dans **Abonnement**, vérifier une consommation conservée et quatre disponibles, pas cinq supplémentaires.
3. Sur le deuxième, ajouter le droit acheté au cadeau : le plafond doit être cinq, jamais huit ; effectuer une publication et vérifier qu’elle n’est débitée qu’une fois.
4. Sur le troisième, faire préparer ou publier six chasses sous l’essai à huit ; relever les six usages et l’achat à cinq toujours actif.
5. Faire constater par le référent la fin d’essai sur des états datés préparés, sans avancer l’horloge partagée ; relire le troisième jeu : achat conservé, six usages conservés, disponible zéro.
6. Contrôler aussi, sur un jeu Communication accompagné, qu’un essai d’une campagne n’ajoute pas une sixième campagne à cinq déjà consommées sous droit acheté dans le mois, ni un nouveau crédit total au changement de mois.
7. Vérifier que les animations déjà publiées restent terminables et que changer de source de droit n’a remis aucun compteur à zéro.

**Résultat attendu.** Plafond le plus élevé, jamais addition des quotas ; usages conservés, aucun rechargement par changement de source. Droit acheté préservé après l’essai ; disponible zéro si usages supérieurs au plafond restant.

### RM-08-04

**Scénario.** **Accompagné :** répéter la fin des droits par expiration de module, retrait commercial anticipé, puis expiration de base. Tenter nouveaux usages et continuités.

**Marche à suivre**

1. Faire préparer par le référent trois jeux isolés correspondant à expiration de module, retrait commercial anticipé et expiration de base, avec les mêmes engagements repérés avant la fin des droits.
2. Pour chaque jeu, garder une animation publiée, un import confirmé et effectivement lancé, une campagne commencée à audience figée, ainsi que des brouillons pour de nouveaux usages.
3. Après l’événement prévu, connecter le gestionnaire habilité dans Animation et tenter une création ou publication dépendante du droit terminé, un nouvel import et une nouvelle campagne : ils doivent être bloqués.
4. Ouvrir l’animation antérieure puis poursuivre les opérations encore admissibles jusqu’à clôture, tirage ou remise selon son état et la validité des lots.
5. Faire reprendre l’import engagé et la campagne commencée par leurs parcours prévus ; contrôler que seules les lignes et l’audience déjà figées sont traitées, sans ajout de fichier, ligne ou destinataire.
6. Consulter l’historique et faire comparer les références traitées au jeu initial ; consigner séparément les trois causes de fin de droit et leurs continuités, sans modifier l’horloge commune ni les tables.

**Résultat attendu.** Nouvelles créations/publications dépendantes bloquées ; animations publiées terminables, imports lancés reprenables, campagnes commencées terminables sans audience ajoutée. Historique consultable.

### RM-08-05

**Scénario.** À expiration, ouvrir une campagne programmée non commencée puis renouveler le droit.

**Marche à suivre**

1. Préparer avec le référent une campagne Communication programmée mais non commencée, un droit arrivant à échéance avant son départ et un gestionnaire disposant de Communication.
2. À l’expiration préparée, ouvrir la campagne dans Animation et vérifier sa suspension ainsi que l’absence de début d’envoi et de message reçu dans Live.
3. Avec le profil Achat, renouveler le droit par **Abonnement**, payer en mode test si requis puis attendre la confirmation effective du droit.
4. Revenir à la campagne et faire observer par le référent le traitement de son échéance : le renouvellement seul ne doit provoquer aucune émission automatique.
5. Avec le gestionnaire habilité, reprendre le parcours d’aperçu et de confirmation ; revérifier audience, consentements, fréquence et quota avant de confirmer explicitement l’envoi.
6. Sur une copie dédiée de la variante, faire suspendre administrativement l’organisation avant la reprise : malgré le droit renouvelé, la confirmation et l’envoi doivent rester refusés. Vérifier le suivi et les boîtes Live de test.

**Résultat attendu.** Campagne suspendue ; aucune émission automatique au renouvellement. Nouvelle confirmation et contrôles courants avant envoi ; la suspension administrative reste prioritaire.


## F09 — Créer et publier avec le bon choix de dotation

**Objet.** Préparer une animation avec Coffrets, lots externes ou bons numériques, en sachant précisément ce qu’il reste à faire avant publication.

**Accès.** Animation → **Animations** → création/configuration et assistant. **US01–02, US29 ; CA01–05, 11, 56.**

**Prérequis à vérifier**

- [ ] Organisateur habilité et crédits de publication ; commerçants participants prêts selon le jeu choisi.
- [ ] Un brouillon distinct pour chaque branche ; dotation externe F10 et numérique F11 préparées.
- [ ] Un parcours Coffrets seul sans abonnement Animation, et une animation Coffrets historique pour comparaison.

### ~~RM-09-01~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Créer sans choisir la dotation, puis choisir Libre sans mode ; revenir en arrière dans le formulaire.~~

**Marche à suivre**

1. Se connecter à Animation comme gestionnaire A1 autorisé à créer ; ouvrir **Animations** et commencer un brouillon dédié `RM-09-01`, sans réservation ni affectation.
2. Renseigner les informations générales requises en laissant la dotation vide ; tenter de poursuivre et relever le choix manquant, sans Coffrets sélectionné automatiquement.
3. Choisir explicitement une dotation libre, laisser son mode vide puis tenter de poursuivre ; vérifier que le mode externe/numérique est demandé.
4. Choisir le mode externe, renseigner ses informations, avancer au récapitulatif puis revenir à l’étape précédente.
5. Vérifier que le choix explicite externe reste affiché dans le formulaire et le récapitulatif ; enregistrer le brouillon et sa référence, sans le publier.

**Résultat attendu.** ~~Aucune présélection silencieuse ; choix manquants signalés. Récapitulatif et navigation conservent le choix explicite.~~

Preuve du 23 octobre 2026 : rapport navigateur `run-1792787584279-47ba`, deux étapes réussies sur le clone isolé, depuis les informations et la mission jusqu'au brouillon enregistré puis relu. Aucun engagement ni publication ; aucun déploiement sur TEST partagé.

### RM-09-02

**Scénario.** Choisir successivement les trois branches sur des brouillons sans engagement ; regarder l’assistant puis omettre un prérequis pertinent.

**Marche à suivre**

1. Comme gestionnaire A1, préparer dans **Animations** trois brouillons indépendants `RM-09-02-C`, `-E` et `-N`, sans engagement, avec les droits de chaque branche.
2. Sur le premier, choisir Coffrets et ouvrir l’assistant ; sur le deuxième choisir Libre/externe ; sur le troisième Libre/numérique. Vérifier qu’une seule branche est retenue sur chaque fiche.
3. Revenir sur chaque brouillon sans engagement, changer explicitement de branche puis relire l’assistant ; contrôler que ses tâches correspondent à la branche désormais choisie et qu’aucune ancienne dotation ne reste active.
4. Rétablir les branches C/E/N et laisser volontairement un prérequis de leur assistant incomplet : préparation/réservation Coffrets requise, description de dotation externe ou affectation de stock numérique.
5. Tenter la publication de chaque brouillon ; relever le refus, le prérequis précis, l’acteur qui doit intervenir et l’action attendue. Vérifier que chaque animation reste non publiée.
6. Corriger chaque prérequis par le parcours indiqué puis actualiser l’assistant ; vérifier la disparition du blocage correspondant sans publier ces jeux destinés aux vérifications de formulaire.

**Résultat attendu.** Un mode unique par animation ; assistant adapté, blocage précis avec acteur/action attendue ; aucune publication contournant les prérequis.

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** : douze
contrôles réussis sur trois brouillons distincts, six changements de branche
persistés, assistants et acteur/action attendus relus. Publication désactivée
dans l’interface pour les trois prérequis manquants, aucun POST de publication.
Description externe complétée et une unité numérique créée puis affectée par
les parcours normaux : blocages correspondants levés, stock sans doublon.
Le choix d’un Coffret lève l’absence de lot mais laisse le financement requis ;
cette correction reste incomplète. Les trois animations restent en brouillon.
Preuve `branches-assistant-principal-preuves-figees.json`, scénario non barré.

### RM-09-03

**Scénario.** Publier une Libre/externe et une Libre/numérique correctement préparées sans commande Coffrets.

**Marche à suivre**

1. Se connecter comme gestionnaire A1 avec deux crédits Animation disponibles et préparer deux animations dédiées, l’une externe et l’autre numérique, sans commande Coffrets ; relever crédits et commandes avant action.
2. Dans **Animations**, compléter la dotation externe avec un responsable et ses consignes, puis la dotation numérique avec des exemplaires distincts d’un commerce Animation habilité ; vérifier accords, règlement et assistant.
3. Publier chacune ; contrôler le succès sous les seuls droits Animation et l’absence de demande de paiement Coffrets.
4. Ouvrir leurs dotations et, avec Localeo habilité, leurs traces commerciales : vérifier qu’aucune commande, commission ou prestation Coffrets n’a été créée.
5. Avec le référent, préparer la clôture et un participant éligible synthétique par animation ; confirmer leurs tirages puis vérifier les emails dans les boîtes de test.
6. Déclarer la remise externe depuis le suivi des gains et faire remettre le bon numérique par QR dans Pro ; contrôler les deux historiques selon F10–F14 et l’absence persistante d’effet Coffrets.

**Résultat attendu.** Publication possible sous les droits Animation ; aucun paiement Coffrets demandé ni commande, commission ou prestation Coffrets créée. Poursuivre jusqu’à remise avec F10–F14.

### RM-09-04

**Scénario.** Engager une réservation/affectation puis essayer de changer de mode ; refaire après publication.

**Marche à suivre**

1. Comme gestionnaire A1, préparer des brouillons distincts permettant une réservation Coffrets et une affectation numérique ; disposer aussi de copies publiées dédiées, dont une externe, avec dotation documentée.
2. Ouvrir chaque brouillon dans deux onglets avant engagement ; dans le premier effectuer la réservation ou l’affectation prévue et noter mode, ordre, quantités et durée éventuelle.
3. Dans ce premier onglet, tenter de changer de mode ; vérifier le refus et la conservation de l’engagement.
4. Dans le second onglet resté sur l’ancien état, tenter le même changement puis actualiser ; vérifier le refus ou conflit explicite, sans contournement du gel.
5. Sur chacune des copies publiées, tenter de changer mode, ordre, quantités engagées et durée applicable ; vérifier leur conservation après rechargement.
6. Comparer les références d’engagement et la dotation finale au relevé initial ; joindre les refus et conflits sans capturer de QR utilisable.

**Résultat attendu.** Changement refusé ; mode, ordre, quantités engagées et durée publiés conservés. Deux onglets concurrents ne permettent pas de contourner ce gel.

### RM-09-05

**Scénario.** Acheter/consommer un coffret avec le commerce Coffrets seul ; exécuter publication, réservation/activation et envoi d’un gain d’animation Coffrets historique.

**Marche à suivre**

1. Préparer un commerce Coffrets seul, ses accès Pro, un acheteur synthétique et une animation Coffrets historique dédiée avec organisateur habilité ; confirmer l’absence d’abonnement/onboarding Animation sur le parcours Coffrets seul.
2. Depuis la marketplace, acheter un coffret en paiement de test, relever sa référence puis ouvrir son parcours de consommation auprès du commerce Coffrets seul.
3. Dans Pro, avec le responsable de ce commerce, effectuer la consommation prévue par le parcours Coffrets ; vérifier qu’aucun abonnement ou dossier Animation n’est exigé.
4. Comme organisateur, ouvrir l’animation historique dans **Animations**, accomplir ses prérequis Coffrets puis publier selon son parcours existant.
5. Effectuer sa réservation/activation puis l’envoi d’un gain Coffrets à la boîte de test ; contrôler l’état du gain et le message reçu.
6. Comparer droits, commandes et états avec la référence Coffrets historique préparée ; vérifier qu’aucune durée, remise indivisible ou règle de remplacement propre aux lots libres n’a été imposée implicitement.

**Résultat attendu.** Aucun abonnement ni onboarding Animation imposé au parcours Coffrets seul ; les règles et droits Coffrets historiques sont préservés, sans application implicite des nouvelles règles des lots libres.


## F10 — Lots libres gérés hors Localeo

**Objet.** Décrire la dotation et suivre le contact/remise sans obliger l’organisateur à digitaliser la remise physique.

**Accès.** Animation → fiche → dotation/lots puis suivi des gains. **US04 ; CA06, 08–10, 29.**

**Prérequis à vérifier**

- [ ] Animation Libre/externe en brouillon et gestionnaire habilité.
- [ ] Responsable de remise externe, sans compte Pro, consignes et quantités connues.
- [ ] Pour le suivi, tirage confirmé de F12 et boîte email gagnant de test.

### ~~RM-10-01~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Créer « Lot A » quantité 2 puis « Lot B » quantité 1 ; saisir responsable/consignes et réordonner avant publication ; essayer quantité nulle.~~

**Marche à suivre**

1. Comme gestionnaire A1, ouvrir un nouveau brouillon Libre/externe `RM-10-01` dans **Animations**, puis sa configuration de dotation.
2. Ajouter `Lot A` en quantité 2 et `Lot B` en quantité 1 ; renseigner pour chacun un responsable externe sans compte Pro et des consignes synthétiques précises.
3. Réordonner avant publication, par exemple B avant A ; enregistrer puis relire les trois positions attendues : B, A, A.
4. Tenter de saisir une quantité 0 sur une ligne ; vérifier le refus, puis rétablir sa quantité initiale sans modifier l’ordre.
5. Relire le brouillon et l’assistant : vérifier les trois unités et l’absence de QR, de création de compte Pro ou d’achat Coffrets imposé.

**Résultat attendu.** ~~Trois positions explicites dans l’ordre choisi ; quantité invalide refusée. Aucun QR, compte Pro ou achat Coffrets imposé.~~

Preuve du 23 octobre 2026 : rapport navigateur `run-1792787672542-dd44`, trois étapes réussies sur le clone isolé : A×2/B×1, quantité zéro refusée, ordre B/A/A, récapitulatif et brouillon persistants sans QR ni achat imposé. Le premier essai attendait mal le second champ de consignes ; il s'est arrêté avant toute création serveur, puis le sélecteur a été corrigé et le cas rejoué. Aucun déploiement sur TEST partagé.

### RM-10-02

**Scénario.** Après attribution, lire l’email et le suivi avant toute réponse du gagnant.

**Marche à suivre**

1. Faire préparer une animation externe dédiée clôturée, avec un gain confirmé et son email envoyé à une boîte de test ; ne saisir encore ni contact, ni réponse, ni remise.
2. Comme gestionnaire A1, ouvrir **Animations**, la fiche puis le suivi du gain ; noter séparément état d’envoi, contact et remise.
3. Ouvrir l’email du gagnant et son lien privé dans la session de test ; comparer lot, responsable et consignes à la dotation publiée.
4. Revenir au suivi avant toute réponse du gagnant ; vérifier que l’envoi réussi n’a enregistré ni contact réussi ni remise.
5. Comparer avec un second gain externe dédié dont la non-remise a été explicitement déclarée : distinguer « Non renseigné » et « Non remis », et consigner les références sans les liens privés.

**Résultat attendu.** Lot, responsable et consignes adaptés ; email envoyé ne signifie ni contact réussi ni remise. « Non renseigné » se distingue de « Non remis ».

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** : suivi
vierge puis suivi corrigé relus séparément de l’état d’envoi. La réception
effective de l’email et son lien n’ont pas été exécutés. Le refus explicite
incorrectement affiché « non renseigné » a ensuite été corrigé : `NON_REMIS`
est relu sur le même refus à 1280/320 px, sans nouvel événement ni changement
de version. Une correction seule reste « non renseigné ». Voir les
[anomalies backend](../../roadmap/anomalies/backend.md). Preuves privées :
`externe-remise-clone-couverture.json`. Aucun succès intégral revendiqué.

### RM-10-03

**Scénario.** Enregistrer contact, réponse puis remise déclarée ; corriger la déclaration avec motif ; essayer avec un simple commerçant/salarié.

**Marche à suivre**

1. Comme gestionnaire A1 habilité, ouvrir le suivi d’un gain externe dédié confirmé et non remis ; préparer un compte Localeo habilité ainsi que des sessions commerçant et salarié sans droit de gestion.
2. Enregistrer un contact avec le gagnant puis sa réponse synthétique ; relire les deux événements et leurs auteur/date.
3. Déclarer la remise du lot, puis corriger cette déclaration avec le motif `Erreur de déclaration — recette RM-10-03`.
4. Relire l’historique : conserver la déclaration initiale, la correction et son motif ; vérifier l’état courant qui en résulte.
5. Avec Localeo habilité, ouvrir un second gain externe dédié et effectuer une déclaration contrôlée ; vérifier que cette intervention est autorisée et attribuée au bon acteur.
6. Avec le simple commerçant puis le salarié, tenter d’accéder à l’action de suivi par l’entrée ou le lien connu ; vérifier le refus effectif et l’absence d’événement ajouté.

**Résultat attendu.** Événements et correction tracés, historique conservé ; seuls gestionnaires habilités et Localeo peuvent effectuer ces opérations.

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** : contact,
réponse, remise déclarée puis correction avec le motif prescrit, quatre
événements conservés ; vrais comptes commerçant et salarié refusés sans ajout.
L’auteur absent à l’écran a été corrigé puis relu avec les dates sur les mêmes
événements à 1280/320 px, dix contrôles réussis. L’intervention Localeo en
écriture reste à traiter ; voir les [anomalies backend](../../roadmap/anomalies/backend.md)
et [Animation](../../roadmap/anomalies/animation.md). Index privé
`externe-remise-clone-couverture.json`, scénario non barré.


## F11 — Modèles, exemplaires et affectation des lots numériques

**Objet.** Constituer un stock de lots indivisibles remis par un commerce précis et éviter qu’un même exemplaire soit promis à deux animations.

**Accès.** Animation → fiche Libre/numérique → **Lots**. **US05–06 ; CA30–31, 33.**

**Prérequis à vérifier**

- [ ] Commerce de remise habilité Animation, deux animations de A1 et une de B1.
- [ ] Génération d’exemplaires opérationnelle, clés QR configurées et traitement de fond prêt ; aucun secret copié dans les preuves.
- [ ] Gestionnaire habilité aux lots ; stock vierge réservé à ce test.

### ~~RM-11-01~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Créer un modèle avec un seul commerce de remise, générer 3 exemplaires ; répéter la demande après une réponse incertaine accompagnée.~~

**Marche à suivre**

1. Comme gestionnaire A1 habilité aux lots, ouvrir la fiche numérique dédiée puis **Lots** ; avec le référent, confirmer le fonctionnement du worker et préparer une perte de réponse contrôlée sur cette opération.
2. Créer un modèle `RM-11-01` rattaché à un seul commerce Animation de remise, avec description et consignes ; relever sa référence.
3. Demander 3 exemplaires ; relever la référence de génération et distinguer opération en cours et stock disponible.
4. Après la réponse incertaine préparée, consulter puis reprendre la même demande, sans créer une seconde génération ; attendre sa fin.
5. Vérifier exactement 3 exemplaires distincts liés au modèle, sans exemplaire supplémentaire ; contrôler qu’aucun n’offre un bon utilisable avant attribution.
6. Examiner les informations de lot : aucune réserve monétaire ou consommation fractionnée ne doit être proposée ; conserver uniquement les références sans QR ni secret.

**Résultat attendu.** ~~Exactement 3 exemplaires distincts, sans création supplémentaire au rejeu ; pas de bon utilisable avant attribution, pas de solde fractionnable.~~

Preuve du 23 octobre 2026 : `parcours-libre-clone-index-completude.json` relie les six étapes à leurs preuves et empreintes. Vrais formulaires, génération de trois exemplaires, réponse coupée après acceptation serveur, vérification puis reprise de la même demande ; une génération, trois références distinctes et aucun bon avant attribution. Clone isolé uniquement, sans déploiement sur TEST partagé.

### ~~RM-11-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Affecter un exemplaire à une animation ; tenter de l’affecter à la seconde, y compris depuis deux sessions simultanées.~~

**Marche à suivre**

1. Préparer deux animations numériques brouillon A1 et deux exemplaires disponibles dédiés ; ouvrir **Lots** avec deux sessions de gestionnaires habilités.
2. Dans la première animation, affecter le premier exemplaire ; tenter ensuite de sélectionner le même dans la seconde.
3. Vérifier l’indisponibilité explicite et relire l’affectation initiale, qui doit rester unique.
4. Sur le second exemplaire encore libre, préparer son affectation à une animation différente dans chaque session puis confirmer presque simultanément avec le référent.
5. Actualiser les deux fiches et le stock : une seule affectation active pour cet exemplaire, un refus/conflit intelligible pour l’autre session et aucun stock négatif.

**Résultat attendu.** ~~Une seule affectation active ; indisponibilité claire pour l’autre, aucun stock négatif.~~

Preuves vérifiées le 24 octobre 2026 : `cas-complets-libre-clone-index-20261024.json`. Deux sessions A1, affectation puis indisponibilité, course réelle sur positions libres avec succès/refus LOT_INDISPONIBLE et une affectation active par unité. La première course à position occupée est conservée comme contrôle distinct et exclue de la preuve de collision. Clone isolé uniquement ; aucune livraison email fournisseur ni lecture optique physique revendiquée.

### ~~RM-11-03~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Modifier la description du modèle après engagement ; essayer de changer le commerce de remise et d’utiliser un exemplaire de B1.~~

**Marche à suivre**

1. Comme gestionnaire A1, préparer un modèle numérique dédié, un exemplaire engagé dans une animation A1 et un exemplaire distinct appartenant à B1 ; noter description et commerce de la version engagée.
2. Dans **Lots**, modifier la description courante du modèle puis enregistrer.
3. Rouvrir l’exemplaire engagé et sa dotation ; vérifier qu’ils gardent leur description initiale tandis que le modèle présente la nouvelle description.
4. Tenter de changer le commerce de remise du modèle engagé ; vérifier le refus et la conservation du commerce initial.
5. Depuis le contexte A1, tenter l’accès ou l’affectation de la référence B1 préparée pour ce contrôle ; vérifier le refus sans divulgation des données de B1.

**Résultat attendu.** ~~Nouvelle description sans altérer les descriptions déjà engagées ; changement de commerce engagé et accès hors commune autorisée refusés.~~

Preuves vérifiées le 24 octobre 2026 : `cas-complets-libre-clone-index-20261024.json`. Modification du modèle, snapshots initiaux préservés dans les données et visibles dans la dotation et le stock après correctif des deux composants Animation ; commerce engagé non modifiable, véritable référence B1 refusée sans effet. Rejeu sur les mêmes objets, sans migration ni changement de règle métier. Clone isolé uniquement ; aucune livraison email fournisseur ni lecture optique physique revendiquée.

### ~~RM-11-04~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Choisir la durée 1, 90 puis 365 jours sur des brouillons ; essayer 0 et 366 ; publier et retenter l’édition.~~

**Marche à suivre**

1. Comme gestionnaire A1, ouvrir un nouveau brouillon numérique `RM-11-04` avec stock dédié et crédit de publication ; relever la durée initiale attendue de 90 jours.
2. Saisir successivement 1, 90 puis 365 jours, enregistrer et relire après chaque valeur ; vérifier leur acceptation.
3. Essayer 0 puis 366 jours ; vérifier les erreurs et l’absence d’enregistrement d’une valeur hors bornes.
4. Rétablir 90 jours, compléter les prérequis et publier ; tenter ensuite de modifier la durée et vérifier qu’elle reste figée.
5. Avec un participant éligible et la clôture préparés pour ce jeu, confirmer le tirage ; comparer l’échéance du bon à sa date d’attribution, augmentée de 90 jours, et non à sa date de publication.

**Résultat attendu.** ~~90 par défaut, bornes 1–365 ; erreurs sur valeurs hors limites ; durée figée à publication, échéance calculée à l’attribution.~~

Preuve du 23 octobre 2026 : `duree-decouverte-clone-preuves-completes.json` relie neuf contrôles navigateur réussis au tirage confirmé du même brouillon. Durées 1/90/365, refus 0/366, gel après publication et refus API sans effet ; le bon unique expire 90 jours après son attribution. Clone isolé uniquement, sans déploiement sur TEST partagé.

### ~~RM-11-05~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Après attributions, libérer le surplus jamais attribué sur confirmation ; tenter la même chose avec un exemplaire attribué puis révoqué.~~

**Marche à suivre**

1. Préparer une animation numérique dédiée avec 3 exemplaires affectés et 2 participants éligibles ; comme gestionnaire A1, confirmer son tirage après clôture.
2. Dans **Lots**, relever les deux exemplaires attribués et le surplus jamais attribué en fin de dotation.
3. Demander la libération du seul surplus, lire puis confirmer l’action ; vérifier qu’il redevient disponible.
4. Sur l’un des exemplaires attribués non consommés, révoquer le bon avec un motif de recette puis tenter de libérer cet exemplaire.
5. Vérifier le refus, l’absence de retour au stock et la conservation du gain initial ainsi que du bon révoqué dans l’historique.

**Résultat attendu.** ~~Seul le surplus jamais attribué redevient disponible ; bon révoqué et ancien gain restent dans l’historique, sans retour automatique au stock.~~

Preuve du 23 octobre 2026 : `parcours-libre-clone-index-completude.json` relie les cinq étapes aux preuves vérifiées. Même animation numérique avec trois exemplaires et deux participants éligibles : seul surplus jamais attribué libéré par confirmation UI ; bon actuellement non consommé révoqué par formulaire, libération de son exemplaire refusée 409 et historique conservé. Le bon révoqué avait une ancienne remise corrigée, sans consommation active au test. Clone isolé uniquement.

## F12 — Tirage, emails, suppléants et remplacement du gagnant

**Objet.** Attribuer les lots équitablement selon l’ordre publié, informer les gagnants et gérer les refus/injoignables sans effacer le tirage initial.

**Accès.** Animation → fiche clôturée → tirage/gains ; email et Live côté gagnant. **US07–08 ; CA06–10, 32–33.**

**Prérequis à vérifier**

- [ ] Animations Libre/externe et Libre/numérique clôturées, populations éligibles figées : 0, 2, 3 et 5 participants pour 3 lots.
- [ ] Tirage libre et envois opérationnels ; deux boîtes gagnants et une liste de suppléants de test.
- [ ] Cas datés « premier email réussi depuis moins de 14 jours / au moins 14 jours », refus explicite et réserve épuisée.


### ~~RM-12-01~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Préparer puis confirmer le tirage pour chacune des quatre populations (0, 2, 3 et 5 éligibles pour 3 lots).~~

**Marche à suivre**

1. Faire préparer huit animations dédiées clôturées : externe et numérique, chacune avec 3 lots ordonnés et respectivement 0, 2, 3 ou 5 éligibles figés ; noter les populations et l’ordre publié.
2. Comme gestionnaire A1 autorisé au tirage, ouvrir chaque fiche puis lancer la préparation de son tirage ; avec le référent, observer l’étape non confirmée.
3. Avant confirmation, vérifier l’absence de gain officiel, d’email gagnant et de bon numérique utilisable ; ne pas confondre les attributions privées préparées avec des gains.
4. Confirmer chaque opération et attendre son résultat ; relever respectivement 0, 2, 3 et 3 gagnants distincts pour chaque mode, au plus un lot par personne.
5. Comparer les attributions à l’ordre des lots publié ; vérifier que les lots non attribués restent en fin et qu’aucun gagnant n’est inventé.
6. Ouvrir la réserve : aucun suppléant pour 0, 2 ou 3 éligibles ; les éligibles non gagnants restent disponibles dans leur ordre pour le jeu à 5. Consigner chaque variante séparément.

**Résultat attendu.** ~~Avant confirmation, aucun gain officiel/email/bon utilisable. Après : respectivement 0, 2, 3 et 3 gagnants distincts, au plus un lot chacun ; ordre des lots publié respecté, surplus en fin ; aucun gagnant inventé. Réserve de suppléants seulement s'il reste des éligibles non gagnants.~~

Preuves vérifiées le 24 octobre 2026 : `cas-complets-libre-clone-index-20261024.json`. Huit nouvelles animations : externe et numérique, populations0/2/3/5. Préparation non confirmée observée, aucun gain officiel/email gagnant/bon avant confirmation ; gagnants0/2/3/3, ordre publié et réserves0/0/0/2 vérifiés par UI et lectures ciblées. Clone isolé uniquement ; aucune livraison email fournisseur ni lecture optique physique revendiquée.

### ~~RM-12-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Recharger, rejouer la confirmation ou reprendre après réponse perdue avec le référent.~~

**Marche à suivre**

1. Préparer une animation externe et une numérique dédiées, chacune clôturée avec 3 lots et 5 éligibles ; connecter le gestionnaire A1 et convenir avec le référent d’une réponse de confirmation perdue sur le jeu numérique.
2. Confirmer le tirage externe puis relever attributions, ordre des suppléants et référence d’opération ; recharger la fiche.
3. Reprendre ou rejouer la confirmation de cette même opération par le parcours disponible ; vérifier le résultat inchangé, sans nouvelle population ni nouveau tirage.
4. Confirmer le tirage numérique avec l’incident prévu ; après la perte de réponse, consulter l’état de cette même opération avant toute nouvelle action.
5. Si une reprise est nécessaire, reprendre la référence existante ; comparer gagnants, suppléants et bons avant/après, avec un seul bon courant par exemplaire et aucun résultat aléatoire renouvelé.

**Résultat attendu.** ~~Mêmes attributions et suppléants, aucun nouveau tirage pour changer le résultat ; un seul bon courant par exemplaire.~~

Preuves vérifiées le 24 octobre 2026 : `cas-complets-libre-clone-index-20261024.json`. Externe et numérique à cinq éligibles : rechargement et rejeu de la même confirmation ; réponse numérique coupée après202, état relu avant reprise. Mêmes opérations, attributions, réserves et bons, sans renouveler le hasard. Clone isolé uniquement ; aucune livraison email fournisseur ni lecture optique physique revendiquée.

### RM-12-03

**Scénario.** Lire l’email du gagnant et le bon numérique ; provoquer puis reprendre un échec d’envoi contrôlé.

**Marche à suivre**

1. Préparer deux tirages dédiés, externe et numérique, avec boîtes gagnants de test ; le référent organise un échec d’envoi contrôlé sur un gain, sans empêcher l’attribution.
2. Comme gestionnaire A1, confirmer les tirages puis consulter séparément les états du gain et de son email.
3. Ouvrir l’email réussi : comparer lot, commerce ou responsable, consignes et validité applicable à la dotation ; pour le numérique, ouvrir le bon et vérifier ces mêmes informations.
4. Sur le gain dont l’email a échoué, vérifier que l’attribution existe toujours ; faire reprendre la préparation du même gain ou le transport outbox selon l’échec diagnostiqué par le référent.
5. Vérifier la réception après reprise et la stabilité du gain et du bon ; contrôler que l’envoi réussi ne marque pas le lot comme remis.
6. Avec Localeo habilité, vérifier qu’aucune commande Coffrets n’est apparue et consigner les états distincts préparation, envoi et remise.

**Résultat attendu.** Email automatique après confirmation, lot/commerce/consignes/validité exacts ; gain conservé malgré l’échec. Reprise sans nouveau gain, état d’envoi distinct de remise, aucune commande Coffrets fictive.

### RM-12-04

**Scénario.** Retirer les droits du commerce numérique après publication mais avant tirage ; tenter la confirmation.

**Marche à suivre**

1. Préparer une animation numérique dédiée publiée avec plusieurs lots, dont un commerce réservé à ce scénario, et des participants éligibles ; noter toute la dotation publiée.
2. Avec Localeo habilité dans l’ERP, retirer le droit Animation du commerce concerné avant tirage, par le parcours normal et avec motif.
3. Comme gestionnaire A1, ouvrir la fiche clôturée et tenter de confirmer le tirage.
4. Vérifier le refus global explicite : aucun gain officiel, bon ou email partiel ; comparer ordre, lots et quantités à la dotation publiée, sans retrait silencieux.
5. Faire résoudre le blocage par Localeo via les habilitations normales ; actualiser la fiche puis reprendre la confirmation prévue.
6. Contrôler que la confirmation devient possible avec la dotation publiée complète et consigner le refus puis la résolution.

**Résultat attendu.** Refus global explicite, aucun gain/bon/email partiel ; pas de lot retiré silencieusement ni de changement de dotation publiée. Nouvelle confirmation possible après résolution habilitée.

### RM-12-05

**Scénario.** Tenter de remplacer un injoignable avant 14 jours sans refus ; enregistrer un refus explicite sur un autre gain ; remplacer après délai sur le premier.

**Marche à suivre**

1. Faire préparer trois gains non remis dédiés avec suppléants ordonnés : injoignable à moins de 14 jours du premier email réussi, refus explicite à moins de 14 jours, injoignable à au moins 14 jours ; relever ces dates avec le référent, sans avancer l’horloge partagée.
2. Comme gestionnaire A1 habilité au suivi, ouvrir le premier gain et demander son remplacement motivé sans refus enregistré ; vérifier le blocage avant délai.
3. Ouvrir le deuxième gain, enregistrer le refus explicite du gagnant puis demander son remplacement avec motif.
4. Vérifier que le premier suppléant encore éligible est retenu selon l’ordre, avec conservation du refus et de l’ancienne attribution.
5. Sur le troisième gain daté, demander le remplacement pour injoignable ; vérifier son acceptation et le même respect de la réserve.
6. Comparer le seuil à la date du premier succès réel de transport, pas à la préparation de l’email ni à un renvoi ultérieur ; consigner les trois variantes séparément.

**Résultat attendu.** Avant délai : refus sauf refus explicite. Délai compté depuis le premier email envoyé avec succès ; remplacement manuel motivé selon l’ordre des suppléants éligibles.

### ~~RM-12-06~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Remplacer un gagnant numérique non servi ; tester son ancien QR et ouvrir le nouveau bon du suppléant ; refaire avec un lot déjà consommé.~~

**Marche à suivre**

1. Préparer deux gains numériques dédiés avec remplacement autorisé et suppléants disponibles : un bon non servi et un autre déjà consommé ; conserver le premier ancien QR uniquement sur l’appareil de test.
2. Comme gestionnaire A1, remplacer le gagnant non servi avec motif depuis le suivi du tirage.
3. Ouvrir le nouveau bon reçu par le suppléant ; vérifier le même lot, un nouveau bénéficiaire et une durée complète calculée depuis cette nouvelle attribution.
4. Dans Pro avec le commerce de remise autorisé, tenter l’ancien QR ; vérifier sa révocation définitive et l’absence de remise.
5. Relire l’historique des deux attributions, puis demander le remplacement du gain déjà consommé ; vérifier le refus et la conservation de sa consommation.

**Résultat attendu.** ~~Ancien bon définitivement révoqué ; nouveau bon pour le même lot, durée complète depuis nouvelle attribution, historique préservé. Lot déjà consommé non réattribuable.~~

Preuves vérifiées le 24 octobre 2026 : `cas-complets-libre-clone-index-20261024.json`. Remplacement motivé par formulaire, nouveau bon ouvert depuis le message produit préparé en outbox, même lot et durée complète ; ancien QR refusé dans Pro. Historiques relus et gain déjà consommé non réattribuable, consommation conservée. Clone isolé uniquement ; aucune livraison email fournisseur ni lecture optique physique revendiquée.

### RM-12-07

**Scénario.** Épuiser la réserve puis demander explicitement un nouveau tirage de remplacement, avec puis sans candidat éligible non gagnant.

**Marche à suivre**

1. Faire préparer avec le référent deux tirages dédiés dont les remplacements sont autorisés et la réserve épuisée : l’un avec candidat de la population gelée redevenu éligible et jamais gagnant, l’autre sans aucun candidat admissible ; ne pas ajouter de nouvel inscrit à la population.
2. Comme gestionnaire A1 habilité, ouvrir chaque gain à remplacer et vérifier l’épuisement réel de la réserve ainsi que l’historique des anciens gagnants.
3. Sur le premier jeu, demander explicitement un nouveau tirage de remplacement et renseigner son motif ; relever l’opération distincte liée à l’attribution initiale.
4. Après traitement, vérifier que seul un candidat autorisé de la population gelée peut être retenu et qu’aucun ancien gagnant remplacé ne réapparaît.
5. Exécuter la même demande sur le second jeu ; constater le résultat vide, sans bénéficiaire inventé ni suppression des droits existants.
6. Recharger les deux historiques : les tirages initiaux, remplacements, motifs et retirages restent consultables. Si la préparation du premier état n’est pas possible, marquer cette variante Bloquée avec le référent.

**Résultat attendu.** Retirage possible uniquement sur action tracée et population autorisée ; anciens gagnants remplacés non réintroduits. Aucun nouveau bénéficiaire inventé s’il n’en existe pas, historique conservé.


## F13 — Remise d’un bon numérique par QR ou PIN

**Objet.** Permettre une remise simple, indivisible et sans ambiguïté, une seule fois, depuis Pro ou le téléphone du gagnant.

**Accès.** Pro → scan ; gagnant → bon reçu/Live → validation par PIN. **US09 ; CA21, 34–35.**

**Prérequis à vérifier**

- [ ] Deux bons valides non consommés pour le commerce, un salarié actif et un autre commerce.
- [ ] Caméra autorisée ; PIN du commerce actif ; configuration QR/PIN et notification de validation opérationnelles.
- [ ] Bons expiré/révoqué, ancien QR remplacé et PIN bloqué préparés ; deuxième téléphone pour la concurrence.

### RM-13-01

**Scénario.** Scanner puis confirmer une remise avec le responsable ; répéter sur un autre bon avec le salarié.

**Marche à suivre**

1. Préparer deux bons numériques valides jamais consommés, dédiés au même commerce Animation, et ses comptes responsable et salarié actif ; autoriser la caméra sur les appareils Pro.
2. Dans Pro, comme responsable, ouvrir le scan et lire le premier QR présenté par le gagnant ; vérifier lot et commerce avant confirmation.
3. Confirmer la remise, attendre le résultat explicite puis ouvrir son reçu ; vérifier la consommation totale, sans choix d’autre prestation.
4. Dans une session Pro du salarié, scanner le second bon, vérifier son résumé puis confirmer sa remise.
5. Relire les deux historiques : chacun comporte une seule consommation, sa date, le canal QR et le bon acteur ; conserver des preuves sans QR actif.

**Résultat attendu.** Lot et commerce identifiables avant confirmation ; succès explicite après prise en compte, consommation totale avec date, canal et acteur dans l’historique ; aucune autre prestation à choisir.

### RM-13-02

**Scénario.** Depuis le téléphone du gagnant, lancer la validation PIN et faire saisir le PIN par le commerce.

**Marche à suivre**

1. Préparer un bon numérique valide non consommé dédié et un commerce avec PIN actif ; ouvrir le lien du gagnant sur son téléphone de test.
2. Vérifier lot, commerce et échéance puis ouvrir la validation par PIN depuis le bon.
3. Faire saisir personnellement au commerçant son PIN, sans le communiquer au recetteur ni l’enregistrer ; confirmer la validation prévue.
4. Attendre le résultat puis rouvrir le bon et son reçu ; vérifier la remise indivisible et son état relisible.
5. Consulter l’historique avec le gestionnaire habilité : canal PIN, commerce identifié, aucun salarié fictivement attribué ; vérifier l’absence du PIN dans le reçu et les preuves partagées.

**Résultat attendu.** Même effet métier que le scan ; résultat relisible. Trace identifiant le commerce pour le canal PIN, sans inventer un salarié ; PIN absent du reçu et des preuves partagées.

### ~~RM-13-03~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Rescanner/représenter un bon consommé puis consulter son historique.~~

**Marche à suivre**

1. Préparer un bon dédié déjà consommé, avec reçu et notification initiale identifiables ; connecter le commerce autorisé dans Pro et ouvrir le bon sur le téléphone gagnant.
2. Relever date, canal, acteur et référence de consommation initiale ainsi que le nombre de notifications logiques constaté avec le référent.
3. Rescanner le QR dans Pro puis représenter le bon dans le parcours gagnant ; vérifier que le résultat signale clairement la remise déjà effectuée.
4. Ouvrir le reçu proposé et vérifier qu’il correspond à la consommation initiale, sans nouvelle confirmation de remise possible.
5. Relire l’historique et le suivi des notifications : toujours une seule consommation et aucune nouvelle notification logique due au rejeu.

**Résultat attendu.** ~~État « déjà remis » et reçu existant compréhensibles ; aucune seconde consommation ni nouvelle notification de validation logique au rejeu.~~

Preuves vérifiées le 24 octobre 2026 : `rm1303-clone-preuves-completes.json`. Même bon déjà consommé représenté dans le scanner Pro par saisie de son vrai contenu QR, puis rouvert dans Live ; reçu initial identique, aucune nouvelle confirmation. Les audits avant/après confirment une seule consommation et une seule notification logique. Clone isolé uniquement ; cette vérification du rejeu ne qualifie pas la lecture optique par caméra.

### RM-13-04

**Scénario.** Tester les variantes : autre commerce, bon expiré, révoqué, ancien QR, référence sans attribution et PIN bloqué.

**Marche à suivre**

1. Faire préparer six cas dédiés et identifiés : bon valide d’un autre commerce, expiré, révoqué, ancien QR remplacé, référence d’exemplaire sans attribution et bon valide avec PIN du commerce bloqué ; ne pas altérer leurs états par des essais préparatoires.
2. Dans Pro, avec le commerce autorisé du jeu principal, scanner successivement les quatre premiers cas ; relever le motif de refus propre à chacun.
3. Avec le référent, présenter la référence sans attribution via le parcours de contrôle prévu ; vérifier qu’elle ne devient pas un bon consommable et qu’aucune attribution n’est créée.
4. Sur le téléphone gagnant du sixième cas, essayer la validation avec le PIN bloqué ; vérifier le refus sans déblocage implicite.
5. Rouvrir chaque bon ou état consultable avec l’acteur autorisé ; vérifier l’absence de consommation ajoutée et de message ambigu de réussite. Consigner les six variantes séparément.

**Résultat attendu.** Refus explicite sans remise enregistrée ; aucun message de succès ambigu ni déblocage implicite.

### RM-13-05

**Scénario.** **Accompagné :** confirmer presque simultanément QR et PIN sur le même bon ; simuler une réponse réseau perdue après prise en compte puis rouvrir.

**Marche à suivre**

1. Avec le référent, préparer deux bons dédiés valides non consommés, deux appareils et un commerce autorisé QR/PIN ; réserver le second à la perte de réponse.
2. Pour le premier bon, préparer le scan dans Pro et la validation PIN sur le téléphone gagnant ; déclencher les confirmations presque simultanément.
3. Relire les résultats et l’historique ; vérifier une seule consommation active, avec reçu unique et état cohérent dans les deux parcours.
4. Sur le second bon, confirmer la remise pendant que le référent interrompt seulement la réponse réseau après prise en compte ; vérifier que l’interface n’annonce pas un succès certain sans résultat reçu.
5. Rétablir la connexion et rouvrir la même demande/son résultat avant nouvelle action ; vérifier l’état réellement enregistré et une seule consommation, sans nouvelle validation à l’aveugle.

**Résultat attendu.** Une seule consommation active ; le résultat est relu avant nouvelle action. Une incertitude réseau ne s’affiche jamais comme un succès certain ; historique et état final concordent.


## F14 — Incidents et cycle de vie d’un bon

**Objet.** Corriger une erreur ou aider un gagnant sans perdre la preuve de ce qui a été fait et sans rouvrir un bon interdit.

**Accès.** Animation → fiche → lots/bons ; Localeo habilité pour assistance. **US10 ; CA33, 36.**

**Prérequis à vérifier**

- [ ] Bons non consommé, expiré, consommé, révoqué, proche du plafond de 365 jours.
- [ ] Gestionnaire habilité et compte non habilité ; historique et boîte email de test.
- [ ] Jeu séparé pour une course entre remise et révocation/correction, avec référent technique.

### RM-14-01

**Scénario.** Renvoyer un bon puis remplacer son QR ; comparer bénéficiaire, lot, échéance et tester l’ancien QR.

**Marche à suivre**

1. Comme gestionnaire A1 habilité, ouvrir un bon numérique dédié valide non consommé ; noter bénéficiaire, lot, attribution, échéance et conserver l’ancien QR sur l’appareil privé de recette.
2. Depuis les actions du bon, demander son renvoi à la boîte de test et attendre le message.
3. Ouvrir le message reçu ; vérifier qu’il donne accès au même gain, au même bénéficiaire et à la même échéance.
4. Remplacer le QR par l’action métier prévue, en renseignant le motif demandé ; ouvrir le bon actualisé.
5. Dans Pro avec le commerce autorisé, tester l’ancien QR et vérifier son refus ; scanner ensuite le nouveau et vérifier le résumé valide sans confirmer de remise inutile.
6. Relire l’historique : remplacement tracé, aucun nouveau gain, lot ou échéance modifié.

**Résultat attendu.** Aucun nouveau gain ni changement d’échéance ; ancien QR immédiatement inutilisable, nouveau QR fonctionnel selon l’état du bon.

### RM-14-02

**Scénario.** Prolonger avec motif un bon non consommé, même expiré ; tenter une échéance au-delà de 365 jours depuis attribution initiale.

**Marche à suivre**

1. Faire préparer cinq bons dédiés : valide non consommé, expiré non consommé, proche du plafond de 365 jours, consommé et révoqué ; relever pour chacun la date d’attribution initiale et l’échéance.
2. Comme gestionnaire A1 habilité, ouvrir **Lots** puis prolonger le premier avec un motif et une échéance inférieure au plafond ; vérifier que les autres bons n’ont pas changé.
3. Prolonger de même le bon expiré vers une échéance future autorisée ; vérifier qu’il redevient utilisable selon son état courant.
4. Sur le bon proche du plafond, essayer une échéance supérieure à attribution initiale +365 jours ; vérifier le refus, puis effectuer des prolongations admissibles successives jusqu’au plafond.
5. Tenter une prolongation supplémentaire au-delà du plafond puis une prolongation sur les bons consommé et révoqué ; vérifier les trois refus.
6. Relire les échéances et motifs dans chaque historique : le plafond reste lié à l’attribution initiale, sans cumul permettant de le repousser.

**Résultat attendu.** Seul le bon ciblé change ; plafond absolu respecté, extensions successives non cumulables au-delà ; consommé/révoqué refusé.

Passage principal du 24 octobre et relecture du 29 octobre 2026, **partiel
sur le clone isolé** : dix-sept contrôles, trois prolongations distinctes
acceptées jusqu’à attribution initiale +365 jours, quatre refus attendus et
quatre autres bons inchangés. Trois motifs et versions recoupés avec l’audit
durable. Le correctif d’auteur est rejoué le 29 : les mêmes prolongations
affichent Gestionnaire, les consommations restent attribuées au commerçant.
Aucune commande acceptée rejouée. Bon expiré et lecture Live non vérifiés ;
scénario non barré. Preuves `prolongations-principales-clone-completude-scellee.json`
et `prolongations-principales-clone-auteur-apres-correctif-prive.json`.

Complément du 30 octobre : le lien participant conservé dans un reçu réel
d’inscription HTTP 201 donne la projection du même bon à 320/1280 px, valide,
version 4 et échéance au 23 octobre 2027. Quatre contrôles passent sans
prolongation ni remise supplémentaire. Cela ne prouve ni la réception du lien
personnel du bon par email, ni sa lecture détaillée ou son QR ; ces limites et
le bon expiré restent ouverts. Preuve `prolongation-projection-live-20261030-prive.json`.

### ~~RM-14-03~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Révoquer avec motif un bon non consommé ; tester ensuite QR/PIN et consultation de l’historique.~~

**Marche à suivre**

1. Comme gestionnaire A1 habilité, ouvrir un bon dédié non consommé ; relever attribution, exemplaire, stock et état initial, avec ses accès QR/PIN réservés au test.
2. Demander la révocation et saisir le motif `Révocation de recette RM-14-03` ; confirmer l’action.
3. Avec le commerce autorisé dans Pro, présenter le QR ; vérifier le refus immédiat sans consommation.
4. Depuis le téléphone gagnant, tenter le parcours PIN ; vérifier le même blocage, sans remise possible.
5. Revenir à **Lots**, consulter attribution et historique ; vérifier motif et auteur conservés, bon révoqué et exemplaire non revenu automatiquement au stock.

**Résultat attendu.** ~~Remise bloquée immédiatement, attribution et motif conservés ; pas de retour automatique au stock.~~

Preuves vérifiées le 24 octobre 2026 : `rm1403-clone-preuves-completes.json`. Bon neuf révoqué depuis le formulaire avec le motif exact ; Pro présente le QR comme révoqué, sans remise possible. La demande PIN préparée avant révocation est refusée après celle-ci avec CONFLIT_VERSION ; une relecture fraîche de Live montre le bon annulé sans QR ni action PIN. Audit, auteur et motif conservés, zéro consommation, attribution active et exemplaire non libéré. Le QR a été présenté par saisie manuelle ; aucune lecture optique physique revendiquée. Clone isolé uniquement.

### RM-14-04

**Scénario.** Annuler avec motif une consommation enregistrée par erreur ; répéter sur un bon désormais expiré ou révoqué.

**Marche à suivre**

1. Faire préparer trois consommations erronées dédiées : bon encore valide, bon désormais expiré et bon dont l’état courant est révoqué ; le référent confirme des historiques cohérents sans écriture directe de statut.
2. Comme gestionnaire habilité, ouvrir chaque bon et corriger la consommation ciblée avec un motif explicite.
3. Vérifier dans chaque historique la validation initiale puis la correction, leurs dates/auteurs et l’absence d’effacement de l’ancienne action.
4. Dans Pro avec le commerce autorisé, présenter le premier bon ; vérifier qu’il est à nouveau utilisable, puis effectuer une nouvelle remise contrôlée si prévue pour ce jeu.
5. Présenter les deux autres bons par QR/PIN ; vérifier qu’expiration ou révocation empêche toujours la remise malgré l’annulation de consommation.
6. Rouvrir les anciens reçus et l’état courant : la preuve historique reste visible et n’est pas présentée comme une nouvelle consommation valide.

**Résultat attendu.** Validation initiale et correction visibles. Bon à nouveau utilisable seulement si encore valide et non révoqué ; pas d’effacement de l’ancienne action.

### RM-14-05

**Scénario.** **Accompagné :** lancer remise et révocation/remplacement en concurrence ; refaire sans permission de correction.

**Marche à suivre**

1. Avec le référent, préparer un bon valide non consommé pour chaque course remise/révocation et remise/remplacement de QR, plus des bons distincts pour les essais sans permission ; ouvrir les sessions commerce et gestionnaire.
2. Pour le premier bon, préparer la confirmation de remise dans Pro et la révocation motivée dans Animation ; déclencher presque simultanément.
3. Actualiser les deux vues et consulter l’historique : vérifier un état final cohérent, un conflit/refus compréhensible et aucune remise exécutée sur un état interdit.
4. Répéter avec le second bon et le remplacement de QR ; vérifier que jamais deux QR/bons ne permettent deux consommations actives.
5. Avec le compte sans habilitation de correction, tenter les mêmes actions de révocation/remplacement sur les jeux dédiés puis une correction de remise préparée ; vérifier les refus effectifs.
6. Comparer les historiques et reçus de chaque variante ; consigner l’ordre réel des opérations sans considérer une incertitude réseau comme un succès.

**Résultat attendu.** Un état final cohérent, jamais deux bons utilisables ni remise autorisée sur état interdit ; refus sans habilitation et conflit compréhensible.


## F15 — Chasse au trésor et préparation accompagnée

**Objet.** Acheter une capacité de chasses indépendante du forfait et suivre leur préparation par Localeo jusqu’à la validation terrain.

**Accès.** Animation → **Modèles** → chasse puis fiche ; ERP → **Préparations Animation**. **US18, US30 ; CA46, 57.**

**Prérequis à vérifier**

- [ ] Module absent/actif/épuisé et forfait standard doté d’un crédit ; chasse prête et autre incomplète.
- [ ] Calendrier de service, préparation accompagnée et alertes opérationnels ; opérateur et email demandeur.
- [ ] Dossiers en attente de complément, prêts et en retard préparés.
- [ ] Pour le test de disponibilité, le référent dispose d'une cible isolée où le service de préparation E55 peut être déclaré non prêt, puis rétabli, sans affecter les autres recetteurs.

### RM-15-01

**Scénario.** Publier une chasse avec droit actif puis une tombola/passeport ; tenter sans module et avec dernier crédit déjà consommé.

**Marche à suivre**

1. Comme gestionnaire A1, préparer une chasse prête et validée sur le terrain, une tombola et un passeport prêts, avec deux crédits standard et un quota chasse actif ; réserver des contextes dédiés sans module et à quota chasse épuisé.
2. Dans **Abonnement**, relever quota chasse acquis, consommé et restant : 5 sur une année complète, ou le quota proratisé effectivement acquis ; relever aussi le compteur standard.
3. Publier la chasse depuis sa fiche puis recharger ; vérifier un seul crédit chasse consommé et aucun crédit standard débité.
4. Publier la tombola et le passeport, chacun avec sa dotation propre ; vérifier un débit standard par publication sans effet sur le quota chasse.
5. Dans les deux contextes de refus, tenter une chasse complète sans module puis avec dernier crédit déjà consommé ; vérifier le blocage sans débit d’un autre quota.
6. Avec le référent, consulter un droit chasse dédié arrivé à échéance et son successeur ; vérifier l’absence de report des crédits anciens. Consigner séparément quota annuel et proratisé.

**Résultat attendu.** Chasse consomme uniquement son quota dédié, une fois à publication réussie ; standard consomme le forfait. 5 chasses annuelles ou quota proratisé acquis ; aucun report à échéance.

### ~~RM-15-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Déposer une demande complète de préparation puis consulter échéance et état.~~

**Marche à suivre**

1. Comme organisateur A1 avec module chasse, ouvrir **Modèles**, choisir une chasse puis sa fiche dédiée `RM-15-02` ; préparer lieux, étapes, commerces, contenus et contraintes nécessaires.
2. Saisir et transmettre la demande de préparation à distance ; relever sa référence sans la dupliquer.
3. Avec Localeo habilité, ouvrir `/internal/erp/preparations-animation` et vérifier la complétude ; déclarer la demande complète lorsqu’elle contient tous les éléments requis.
4. Dans le portail, relire état, date de complétude et échéance ; comparer au calendrier de service versionné, en Europe/Paris, pour une cible de cinq jours ouvrés.
5. Vérifier que le suivi annonce une préparation à distance et réserve la validation sur place à l’organisateur, sans promesse d’intervention terrain de Localeo.

**Résultat attendu.** ~~Préparation à distance, cible de 5 jours ouvrés depuis demande complète ; pas de promesse d’intervention terrain Localeo.~~

Preuves vérifiées le 24 octobre 2026 : `chasse-principal-clone-completude-scellee.json` et `rm1502-canonical-step-index.json`. Quatorze contrôles pour les cinq étapes : formulaire et brief complet, demande unique, qualification ERP normale, même état et échéance au portail/ERP. Complétude le 24 octobre, cible le 30 octobre à 17 h Paris selon les cinq jours ouvrés du calendrier versionné `e73-clone-calendrier-20261023`. Préparation à distance et contrôle sur place par l’organisateur explicités. Dossier EN_PREPARATION, aucune déclaration PRETE ni validation terrain simulée. Seule la capacité de préparation a été ouverte dans le clone, ordonnanceur et alertes globales toujours fermés. Clone isolé uniquement.

### RM-15-03

**Scénario.** Demander un complément côté Localeo, répondre côté client puis marquer prêt.

**Marche à suivre**

1. Préparer une demande de chasse dédiée en préparation, un organisateur A1 sans module Communication et un opérateur Localeo habilité ; noter échéance et référence initiales.
2. Dans `/internal/erp/preparations-animation`, demander un complément indispensable en décrivant précisément l’information manquante.
3. Côté organisateur, ouvrir le suivi et la boîte de test ; vérifier motif visible, état d’attente et email, distinct de son seul état de mise en file.
4. Répondre au complément dans le même dossier ; faire reprendre la préparation par Localeo et vérifier avec le référent la suspension du délai pendant l’attente puis sa reprise avec le temps restant.
5. Côté Localeo, déclarer la préparation prête ; côté portail et boîte email, vérifier le nouvel état et le message au demandeur.
6. Comparer les références et crédits avant/après : un seul dossier, aucune campagne Communication nécessaire et aucun crédit supplémentaire consommé par le complément.

**Résultat attendu.** Attente clairement affichée, délai suspendu pendant l’information indispensable ; reprise sur le même dossier ; email au demandeur et suivi dans le portail, indépendants du module Communication.

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** : douze
contrôles réussis sur une demande distincte d’A2 sans module Communication.
Complément demandé dans l’ERP, attente et motif visibles au portail, réponse
client puis reprise sur le même dossier ; historique et quotas conservés.
L’intention email contient le motif, sans tentative de transport ni réception
revendiquée. Attente réelle un samedi, budget de quarante heures ouvrées
conservé ; ce passage ne prouve pas une attente sur des heures ouvrées.
Variante A1, réception email et état « prête » restent à vérifier. Preuves
`chasse-complement-principal-completude-scellee.json`, scénario non barré.

### RM-15-04

**Scénario.** Ouvrir un dossier dépassant son délai, relancer puis faire communiquer une estimation révisée.

**Marche à suivre**

1. Faire préparer par le référent une demande dédiée dépassant son échéance calculée, avec historique de complétude/calendrier et surveillance Ops opérationnelle ; ne pas modifier l’horloge partagée.
2. Comme organisateur A1, ouvrir le suivi de cette chasse ; relever la référence, l’échéance cible et l’indication de retard.
3. Avec l’opérateur habilité, ouvrir Ops et retrouver l’alerte correspondante, puis le dossier ERP lié.
4. Côté organisateur, relancer la demande existante ; côté Localeo, répondre avec une estimation révisée.
5. Relire le suivi : estimation visible, échéance initiale et dépassement conservés, même référence de demande et aucun débit supplémentaire de crédit.

**Résultat attendu.** État de retard et alerte Ops ; relance sur la demande existante sans demande ni crédit supplémentaire.

### RM-15-05

**Scénario.** Tenter de publier une chasse non prête ou non validée sur le terrain ; terminer les validations puis publier ; **accompagné**, deux publications sur le dernier crédit.

**Marche à suivre**

1. Préparer une chasse dédiée non prête avec un crédit chasse réservé ; prévoir, dans un autre contexte isolé, deux chasses complètes et validées avec un seul crédit restant pour la concurrence.
2. Comme gestionnaire A1, tenter de publier la première depuis sa fiche ; vérifier le blocage de préparation et l’absence de débit.
3. Faire terminer la préparation par Localeo, sans validation terrain ; retenter et vérifier le refus lié au contrôle sur place.
4. Faire contrôler le parcours sur place par l’organisateur, enregistrer sa validation pour la révision courante puis publier ; vérifier le succès et un seul crédit chasse consommé.
5. Avec le référent, ouvrir les deux autres chasses dans deux sessions autorisées et confirmer leurs publications presque simultanément sur le dernier crédit.
6. Actualiser les deux fiches et compteurs : une seule publication autorisée, l’autre refusée clairement, quota chasse non négatif et compteur standard inchangé.

**Résultat attendu.** Prérequis de préparation/terrain respectés ; l’organisateur valide le parcours sur place ; une seule publication autorisée avec le dernier crédit, compteur standard inchangé.

### RM-15-06

**Scénario.** **Accompagné :** rendre le service de préparation technique E55 non prêt ; tenter l'achat du module ; examiner aussi une commande déjà confirmée avant l'indisponibilité.

**Marche à suivre**

1. Avec le référent, réserver une cible isolée et un compte responsable/délégation Achat ; préparer une commande chasse déjà confirmée et une tentative d’achat distincte, exclusivement en paiement de test.
2. Faire déclarer le service technique de préparation E55 non prêt par le dispositif de recette convenu ; noter le diagnostic sans modifier les données ni l’horloge d’un environnement partagé.
3. Dans Animation, ouvrir **Abonnement**, sélectionner le module chasse puis tenter l’achat ; vérifier son refus ou report avec diagnostic de disponibilité.
4. Ouvrir la commande déjà confirmée et son dossier d’assistance ; faire examiner la réconciliation par Support/Localeo habilité.
5. Vérifier qu’aucun nouveau paiement implicite n’est créé et que le suivi ne promet pas un service disponible pendant l’incident ; distinguer ce refus d’une validation terrain manquante sur une chasse précise.
6. Faire rétablir le service sur la cible isolée par le référent puis relire commande et dossier ; consigner l’état réconcilié sans racheter automatiquement le module.

**Résultat attendu.** Achat refusé ou différé avec diagnostic lorsque le service ne peut pas être fourni. Une commande déjà confirmée passe par une réconciliation support ; aucun nouveau paiement implicite ni promesse de préparation disponible. Distinguer cet incident de la validation terrain d'une chasse particulière.


## F16 — Import de commerçants et gestion des deltas

**Objet.** Charger un fichier puis ses mises à jour sans doublonner les établissements ni écraser les corrections faites dans Localeo.

**Accès.** Animation → **Import commerçants** ; ERP pour arbitrages SIRET/commune. **US19–20 ; CA42–45.**

**Prérequis à vérifier**

- [ ] Module actif sur A1 et permission Import commerçants ; compte sans permission et commune hors droit.
- [ ] Stockage privé et worker d’import disponibles ; fichiers synthétiques décrits dans le jeu commun.
- [ ] Fiches existantes avec référence du dernier import ; aucun fichier de prospection réel nécessaire. Cet import opérationnel est distinct de l’import CRM de l’epic 71.

### ~~RM-16-01~~ — **Réussi**

**Scénario.** ~~Télécharger le modèle ; charger CSV puis XLSX ; choisir une feuille et associer les colonnes avant aperçu.~~

**Marche à suivre**

1. Comme collaborateur A1 avec module et autorisation Import commerçants, ouvrir **Import commerçants** et télécharger le modèle ; réserver deux dépôts distincts CSV et XLSX de 5 lignes synthétiques.
2. Renseigner les cinq obligatoires : nom commercial, adresse, commune, SIRET et email de contact ; ajouter sur certaines lignes nom du contact, téléphone, catégorie, description et site web.
3. Charger le CSV dans un flux source identifié, associer ses colonnes puis ouvrir l’aperçu ; vérifier valeurs et statut des cinq lignes sans confirmer.
4. Charger le XLSX à plusieurs feuilles dans l’autre dépôt, choisir explicitement une feuille puis associer ses colonnes ; comparer l’aperçu aux seules lignes de cette feuille.
5. Consulter la liste des commerces avant toute confirmation : aucune fiche créée ou modifiée par ces aperçus ; consigner le choix de feuille et les champs obligatoires/facultatifs reconnus.

**Résultat attendu.** ~~Import limité à la feuille choisie ; aperçu sans écriture. Obligatoires : nom commercial, adresse, commune, SIRET, email de contact. Facultatifs : nom du contact, téléphone, catégorie, description, site web.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Le rapport privé `run-1792770510590-ff8a` de la campagne `e73-20261022-e856fb` porte le verdict `REUSSI_AUTOMATIQUE` : modèle téléchargé, CSV et XLSX déposés, feuille et colonnes choisies, aperçus comparés et absence de création ou modification des commerces vérifiée. Ce résultat porte uniquement sur RM-16-01 ; voir le [suivi d'automatisation](automatisation-recette.md#nouveaux-passages-ciblés-du-23-octobre).

### ~~RM-16-02~~ — **Réussi**

**Scénario.** ~~Tester 100 puis 101 lignes ; fichier de 2 000 000 octets puis plus grand ; lignes invalides et formule dans un champ importable.~~

**Marche à suivre**

1. Comme importateur A1 habilité, préparer avec le référent des fichiers distincts de 100 et 101 lignes non vides hors en-tête, de 2 000 000 octets et de taille supérieure ; prévoir aussi lignes vides, ligne invalide et formule dans un champ importable.
2. Dans **Import commerçants**, charger le fichier à 100 lignes puis celui à 101 dans deux dépôts ; vérifier l’acceptation de la borne et le refus du dépassement sans troncature.
3. Charger séparément les deux fichiers de taille frontière ; vérifier acceptation à 2 000 000 octets et refus au-delà avant toute création.
4. Charger le jeu comportant en-tête et lignes entièrement vides ; vérifier qu’ils ne gonflent pas le nombre de lignes de données.
5. Ouvrir l’aperçu des lignes invalides et de la formule ; vérifier anomalies explicites et absence d’exécution de la formule, sans confirmer ces lignes.
6. Contrôler que les dépôts refusés et simples aperçus n’ont créé aucune fiche ; enregistrer taille et compte de lignes réellement préparés pour chaque variante.

**Résultat attendu.** ~~Limites appliquées avant création, sans troncature silencieuse. En-tête exclu, lignes entièrement vides ignorées ; formules non exécutées et anomalies signalées.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Le rapport privé `run-1792772585337-3eed` porte le verdict `REUSSI_AUTOMATIQUE` pour les six étapes : bornes 2 000 000/2 000 001 octets et 100/101 lignes, lignes vides ignorées, anomalies et formule XLSX refusées, inventaire ERP inchangé. Aucun import de lignes n'a été confirmé ; voir le [suivi d'automatisation](automatisation-recette.md#nouveaux-passages-ciblés-du-23-octobre).

### RM-16-03

**Scénario.** Charger email unique connu, email partagé, même email/SIRET différent, autre email/SIRET connu et deux lignes visant la même fiche.

**Marche à suivre**

1. Préparer des fiches synthétiques connues et des fichiers dédiés couvrant email unique connu, email partagé par deux commerces, email connu avec SIRET différent, autre email avec SIRET connu et deux lignes visant une même fiche ; ajouter une collision avec B1 sans exposer ses coordonnées.
2. Comme importateur A1 habilité, charger chaque fichier dans **Import commerçants**, associer les colonnes et ouvrir son aperçu.
3. Sur le cas email unique cohérent, vérifier le rapprochement avec la fiche attendue, principalement par email et avec contrôle du SIRET.
4. Pour les quatre variantes ambiguës, lire les conflits ; vérifier qu’aucune fusion ni règle « dernière ligne gagnante » ne sélectionne silencieusement une issue.
5. Sur la collision hors organisation, vérifier le refus/conflit sans donnée de B1 dans la réponse ; ne confirmer aucune résolution ambiguë.
6. Relire les fiches initiales et relever les références d’aperçu : elles n’ont pas été fusionnées ni écrasées ; consigner chaque variante séparément.

**Résultat attendu.** Email principal pour rapprochement ; cas ambigus en conflit explicite, aucune fusion ni « dernière ligne gagnante ». Données d’une autre organisation non révélées.

### ~~RM-16-04~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Confirmer uniquement les lignes valides d’un fichier mixte ; télécharger le rapport ; tenter sans module ou permission.~~

**Marche à suivre**

1. Comme importateur A1 habilité, préparer un fichier mixte dédié avec deux créations valides, une mise à jour valide et deux lignes invalides ; réserver aussi comptes/contextes sans permission, sans module et hors commune autorisée.
2. Dans **Import commerçants**, charger le fichier, ouvrir l’aperçu et sélectionner seulement les trois lignes prêtes ; confirmer explicitement l’import partiel.
3. Suivre la même opération jusqu’à sa fin puis télécharger son rapport ; comparer les trois succès et les deux lignes écartées à l’aperçu.
4. Ouvrir les fiches créées : statut à vérifier, dossier OnBoard et demande Animation soumis à Localeo ; vérifier absence de compte activé, invitation envoyée ou accord de participation automatique.
5. Recharger l’import et les fiches : une seule création/mise à jour par ligne confirmée, sans doublon.
6. Dans chaque contexte non autorisé, tenter un nouvel import dédié ; vérifier le refus effectif pour absence de module, de permission et de droit communal, sans création.

**Résultat attendu.** ~~Lignes sélectionnées créées/mises à jour une fois ; rejetées identifiables. Nouveau commerce à vérifier, demande Animation soumise à Localeo ; aucun compte activé, invitation envoyée ou participation acceptée automatiquement. Refus hors droit.~~

Preuve du 23 octobre 2026 : `rm1604-clone-preuves-completes.json` relie par empreintes le parcours navigateur, son worker ciblé, les effets de ses deux créations et le rejeu des refus. Aperçu 2 créations/1 mise à jour/2 erreurs, accord partiel explicite, trois succès uniques et rapport téléchargé. Les fiches restent BROUILLON avec OnBoard et demande Animation DEMANDEE ; aucun compte, token d'invitation, email ou accord de participation n'est créé. Les contextes sans permission, sans module et hors commune sont refusés. Une assertion initiale du vérificateur attendait un autre libellé de refus : seuls ces contrôles ont été rejoués, sans refaire l'import terminé. Correctif de compteur appliqué au clone uniquement ; aucun déploiement sur TEST partagé.

### ~~RM-16-05~~ — **Réussi**

**Scénario.** ~~Importer V1, modifier localement le téléphone ; dans V2 modifier ce téléphone différemment, changer un site non retouché localement, laisser une cellule vide et conserver un autre champ inchangé.~~

**Marche à suivre**

1. Comme importateur A1, créer un flux source dédié et importer V1 avec téléphone `01 00 00 00 01`, site `https://v1.example.test`, description et nom de contact synthétiques ; noter les valeurs initiales.
2. Par le parcours de fiche autorisé, modifier localement le téléphone en `01 00 00 00 02` et le nom du contact ; conserver le site inchangé dans Localeo.
3. Préparer V2 dans le même flux : téléphone `01 00 00 00 03`, site `https://v2.example.test`, description vide et nom du contact identique à V1.
4. Charger V2 et lire le détail champ par champ : téléphone en conflit, site proposé à la mise à jour, cellule vide sans suppression et correction locale du contact conservée puisque le fichier n’a pas changé ce champ.
5. Résoudre le téléphone avec **Conserver Localeo**, accepter le nouveau site puis confirmer les lignes prêtes.
6. Relire la fiche et le rapport : téléphone local conservé, site V2 appliqué, description intacte et contact local préservé ; conserver la référence du flux et des deux imports.

**Résultat attendu.** ~~Téléphone en conflit à arbitrer ; site modifiable après confirmation ; cellule vide sans effacement ; modifications locales préservées si le fichier n’a pas changé le champ. Différences présentées champ par champ.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Le rapport privé `run-1792774394870-77f5` porte le verdict `REUSSI_AUTOMATIQUE`. La reprise relie par empreinte les trois étapes antérieures réussies aux valeurs V2 persistées, vérifiées dans l'interface et par un aperçu de relecture non confirmé. Téléphone local, site V2, description intacte, contact local et unicité du commerce sont vérifiés, sans rejouer l'import déjà terminé. Voir le [suivi d'automatisation](automatisation-recette.md#nouveaux-passages-ciblés-du-23-octobre).

### RM-16-06

**Scénario.** Après aperçu, faire modifier une fiche par un autre opérateur, puis confirmer ; changer email de contact, SIRET et commune dans des variantes distinctes.

**Marche à suivre**

1. Préparer quatre variantes indépendantes sur des fiches importées dédiées : concurrence après aperçu, changement d’email de contact, changement de SIRET et changement de commune ; ouvrir les sessions importateur A1 et opérateur autorisé.
2. Pour la première, ouvrir l’aperçu d’une modification puis faire modifier la fiche par l’autre opérateur avant confirmation ; confirmer et vérifier le conflit de version, sans écrasement.
3. Actualiser l’aperçu, relire les écarts et ne confirmer qu’après arbitrage explicite sur les valeurs courantes.
4. Sur la variante email, confirmer le changement autorisé du contact ; vérifier la nouvelle adresse de contact et, avec le commerçant de test, le maintien de son identifiant de connexion initial.
5. Pour SIRET puis commune, tenter la modification depuis leur aperçu ; demander la vérification motivée Localeo et vérifier qu’un simple rapprochement ne modifie pas ces identités.
6. Dans l’ERP, faire examiner chaque demande par Localeo habilité puis actualiser l’aperçu avant confirmation éventuelle ; vérifier décision et historique, sans réécriture des documents financiers anciens.

**Résultat attendu.** Écart intervenu après aperçu détecté, pas d’écrasement silencieux. Email de contact ne change pas le login ; SIRET/commune exigent validation Localeo ERP, pas seulement résolution du rapprochement.

### RM-16-07

**Scénario.** **Accompagné :** interrompre après une ligne réussie, reprendre ; expirer le module avant démarrage puis pendant un autre import déjà commencé.

**Marche à suivre**

1. Avec le référent, préparer deux imports distincts de trois lignes valides : l’un confirmé mais pas encore démarré, l’autre interruptible après un premier succès ; prévoir leurs échéances commerciales dédiées sans changer l’horloge partagée.
2. Comme importateur A1, confirmer le premier puis faire constater l’expiration du module avant son démarrage effectif ; vérifier la suspension/refus sans création de ligne.
3. Dans le second contexte encore actif, confirmer l’autre import, laisser réussir exactement une ligne puis faire interrompre son traitement par le référent.
4. Relever plan, référence d’import et résultat de la première ligne ; faire constater l’expiration commerciale de ce second contexte avant reprise.
5. Avec l’acteur toujours habilité, reprendre la même opération commencée ; vérifier que seules les lignes restantes du plan confirmé sont traitées.
6. Contrôler trois résultats uniques, aucune nouvelle ligne ajoutée au plan et aucun doublon ; distinguer cette continuité commerciale d’un retrait d’habilitation ou d’une suspension administrative.

**Résultat attendu.** Avant démarrage : refus ; déjà lancé : reprise du même import autorisée selon continuité, sans retraiter les succès ni ajouter de nouvelles lignes, aucun doublon.

### RM-16-08

**Scénario.** **Accompagné :** consulter un import terminé/abandonné depuis plus de 30 jours, puis ses fiches et un réimport.

**Marche à suivre**

1. Faire préparer par le référent deux imports dédiés, l’un terminé et l’autre abandonné depuis plus de 30 jours, avec échéances de conservation atteintes et traitement de purge normal vérifié ; conserver les références de leurs fiches et flux sources.
2. Comme importateur A1 habilité, ouvrir chaque historique dans **Import commerçants** et tenter le téléchargement du fichier source puis du rapport.
3. Vérifier l’indisponibilité explicite des quatre artefacts, sans lien public ni téléchargement encore possible après conservation.
4. Ouvrir les fiches issues de l’import terminé ; vérifier qu’elles existent toujours et que leur provenance utile aux deltas reste identifiable.
5. Charger une nouvelle version synthétique dans le même flux source actif ; vérifier les comparaisons avec l’état précédemment importé malgré la purge du fichier ancien.
6. Avec Localeo habilité, consulter l’audit conservé selon sa politique propre ; consigner séparément purge des artefacts et conservation des données métier, sans restaurer les fichiers purgés.

**Résultat attendu.** Fichier source/rapport ne restent pas téléchargeables au-delà de leur conservation ; fiches, provenance nécessaire aux deltas et audits selon leur propre politique préservés.


## F17 — Messages organisateur dans Live et en Web Push

**Objet.** Communiquer avec les participants autorisés au bon moment, avec des quotas compréhensibles et sans sollicitations excessives.

**Accès.** Animation → fiche → communication participants ; Live → messagerie/préférences ; Ops → alertes. **US21–22 ; CA47–49.**

**Prérequis à vérifier**

- [ ] Module et autorisation Communication ; participants répartis dans les quatre audiences et préférences variées, dont un sans accord explicite aux messages organisateur ; un simple abonné à la commune sans participation.
- [ ] Traitement de campagnes, dépôt Live, transport Push/VAPID, protection d’identité de fréquence et destinataires des alertes internes configurés ; appareils de test uniquement.
- [ ] Deux animations de A1, un participant commun multi-appareils ; campagnes à dernier crédit, en échec, programmées et commencées préparées.

### RM-17-01

**Scénario.** Préparer un message pour chacune des audiences : tous, parcours non terminé, parcours terminé, gagnants ; essayer avant publication et après clôture +30 jours.

**Marche à suivre**

1. Comme gestionnaire A1 doté du module et de l’autorisation Communication, préparer une animation publiée dédiée contenant participants non terminés, terminés et gagnants, avec références connues ; réserver des copies avant publication et à plus de 30 jours de clôture.
2. Ouvrir la fiche puis **Communication** ; créer quatre brouillons distincts avec titre/texte synthétiques et choisir successivement tous, parcours non terminé, parcours terminé et gagnants.
3. Prévisualiser chaque audience et comparer ses membres à la seule animation courante ; vérifier l’absence de participants d’une autre animation ou commune.
4. Tenter une campagne sur les copies hors fenêtre préparées avec le référent ; vérifier le refus avant publication effective et après clôture effective +30 jours.
5. Répéter l’accès/la préparation avec un compte sans permission puis un contexte sans module ; vérifier les refus sans consommer de crédit de campagne.
6. Sur un jeu distinct de notification automatique, vérifier avec le référent qu’une notification de service reste possible sans le module Communication ; ne pas déduire son succès du simple refus des campagnes.

**Résultat attendu.** Audience de la seule animation et droits courants ; fenêtre publication à clôture +30 jours respectée. Absence du module ou de permission interdit la campagne, sans bloquer les notifications automatiques d’animation.

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** : quatre
brouillons et leurs aperçus créés par les formulaires pour une animation
dédiée de trois participants terminés et gagnants. Comptages concordants :
tous 3, parcours non terminé 0, terminé 3, gagnants 3 ; quota identique avant et
après, aucune diffusion. Avec les préférences conservées, aucun destinataire
n'est autorisé à recevoir ces messages ; les compteurs ci-dessus désignent
les populations ciblées avant exclusion. Accès Pro responsable et salarié
refusés, soit sept contrôles réussis au total.
Les aperçus sont agrégés : ils ne prouvent pas les
identités de futurs destinataires effectivement servis. Jeux aux populations
variées, ensemble des refus, fenêtres temporelles et notification automatique
restent à compléter. Reçus privés :
`communication-principal-clone-couverture.json`, scénario non barré.

### RM-17-02

**Scénario.** Envoyer immédiatement aux comptes autorisant les messages, l’un avec Push et l’autre sans ; vérifier l'exclusion d'un participant opposé, d'un participant sans accord explicite et d'un simple abonné à la commune sans participation, même s'ils acceptent le Push ou les notifications automatiques.

**Marche à suivre**

1. Préparer une animation publiée dédiée, un crédit et cinq profils : consentant avec Push, consentant sans Push navigateur, opposé, sans accord explicite, simple abonné communal non participant ; donner aux trois exclus des préférences Push/service favorables pour distinguer les accords.
2. Comme gestionnaire A1 habilité, ouvrir **Communication**, rédiger un message identifiable `RM-17-02` et prévisualiser l’audience ; vérifier les deux destinataires et les motifs des exclusions.
3. Confirmer l’envoi immédiat puis suivre dépôt Live et transport Push jusqu’aux résultats disponibles.
4. Ouvrir Live sur les appareils des deux consentants : chacun retrouve le message ; vérifier le Push seulement sur l’appareil autorisé, sans assimiler envoi fournisseur et lecture.
5. Contrôler Live, notifications et boîtes de test des trois exclus : aucun message organisateur, aucun repli email/SMS, même avec permission navigateur ou notifications automatiques.
6. Relire le rapport : dépôt Live, envoi Push et erreurs sont distingués ; aucune ligne ne prouve à elle seule une lecture du participant.

**Résultat attendu.** Message consultable dans Live même sans permission navigateur ; Push uniquement autorisé ; les trois profils exclus ne reçoivent rien, aucun repli email/SMS. La permission navigateur ne vaut pas accord aux messages organisateur. Dépôt Live, envoi Push et erreurs distingués ; aucun de ces résultats ne prouve une lecture.

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** : nouvelle
animation publiée et cinq profils préparés par les formulaires et réglages
normaux, sans modification d'anciens participants. Deux consentants sans Push
reçoivent chacun un seul message Live et le marquent lu ; opposé après retrait
d'accord, participant sans accord explicite et simple abonné communal ne
reçoivent aucun message de cette campagne. Le worker normal ciblé capture les
quatre participants exacts, crée deux messages et exclut les deux autres pour
préférence. Les cinq carnets sont relus, un seul crédit consommé. Aucun Push
tenté ; réception Push et contrôles de non-repli email/SMS restent non exécutés.
Index privé `communication-live-principal-clone-couverture.json`, scénario non barré.

### RM-17-03

**Scénario.** Programmer en heure de Paris ; changer une préférence ou retirer la permission du gestionnaire avant démarrage.

**Marche à suivre**

1. Préparer deux campagnes dédiées sur animations publiées A1, avec crédits disponibles et destinataires consentants distincts sans historique de fréquence ; ouvrir deux sessions gestionnaire et responsable d’organisation.
2. Comme gestionnaire habilité, programmer chaque campagne à une heure future précise Europe/Paris ; relever horaire et référence sans les démarrer.
3. Avant le départ de la première, faire retirer l’accord organisateur d’un destinataire dans ses préférences Live ; garder un autre destinataire consentant pour observer le traitement.
4. Avant le départ de la seconde, faire retirer la permission Communication de son gestionnaire par le responsable, tout en gardant sa session ouverte.
5. Au démarrage prévu, suivre les deux campagnes : exclusion effective du destinataire désinscrit dans la première, suspension/refus lié aux droits dans la seconde.
6. Vérifier rapports et appareils : aucun envoi fondé uniquement sur les anciennes permissions de programmation ; conserver les heures de changement et de contrôle.

**Résultat attendu.** Droits/destinataires revérifiés au départ ; tâches concernées suspendues ou destinataires exclus, pas d’envoi fondé sur les seules permissions de programmation.

### RM-17-04

**Scénario.** Préparer/annuler des brouillons puis démarrer des campagnes jusqu’au quota, reprendre une campagne déjà commencée.

**Marche à suivre**

1. Réserver une commune/souscription dédiée avec quota mensuel acheté de 5 intact, deux animations et au moins huit destinataires consentants distincts ; attribuer des personnes différentes à chaque audience pour éviter un refus de fréquence.
2. Comme gestionnaire habilité, préparer puis annuler un brouillon, créer une programmation et sa préparation sans dépôt Live ; vérifier que le quota reste à 5 disponibles puis annuler cette programmation avant son démarrage.
3. Démarrer une première campagne vers deux destinataires frais et observer le premier message Live accepté ; vérifier qu’un seul crédit est débité à cet instant et que le second destinataire n’ajoute aucun débit.
4. Démarrer quatre autres campagnes réparties entre les deux animations, chacune vers un destinataire frais distinct ; vérifier un crédit par campagne, indépendamment de la taille de l’audience.
5. Tenter une sixième campagne avec un autre destinataire réservé et non sollicité ; vérifier le refus/suspension pour quota commun épuisé, sans message.
6. Avec le référent, reprendre une campagne déjà commencée du même jeu ; vérifier aucun second débit et un compteur partagé commune/souscription, sans réinitialisation par changement d’animation.

**Résultat attendu.** Une unité au premier message Live accepté, qui constitue le démarrage effectif, jamais au brouillon/à la programmation/préparation ; 5/mois partagés par commune/souscription, indépendants du nombre de destinataires ; reprises sans second débit.

### RM-17-05

**Scénario.** **Accompagné :** activer en fin de mois, passer le premier du mois Paris et une borne de changement d’heure ; comparer essai et achat.

**Marche à suivre**

1. Avec le référent, préparer trois contextes isolés dédiés, achat, essai et cadeau, activés en fin de mois Paris, ainsi que des observations avant/après le premier du mois et un changement d’heure ; utiliser des états datés maîtrisés sans toucher l’horloge partagée.
2. Comme gestionnaire habilité, ouvrir **Abonnement** puis **Communication** dans le contexte acheté ; vérifier 5 campagnes sur le premier mois incomplet.
3. Faire démarrer une campagne avec destinataire frais puis consulter le mois civil suivant préparé : vérifier 5 nouveaux crédits, sans ajout des anciens inutilisés, et la borne Europe/Paris.
4. Dans le contexte essai, démarrer sa seule campagne avec un autre destinataire ; au mois suivant du même essai, vérifier qu’aucun second crédit n’est accordé par le changement de mois.
5. Dans le contexte cadeau, examiner les conditions d’octroi puis le quota : 5 par mois par défaut, selon les conditions réellement accordées.
6. Comparer les dates et fenêtres au changement d’heure Paris ; vérifier qu’un décalage d’appareil ou UTC ne change pas le mois métier ni ne crée un report. Consigner les trois droits séparément.

**Résultat attendu.** Premier mois incomplet : 5 campagnes ; mois civil Paris sans report. Essai par défaut : 1 campagne au total, même s’il chevauche deux mois ; cadeau : 5/mois par défaut, sous conditions d’octroi.

### RM-17-06

**Scénario.** Laisser une programmation arriver avec quota épuisé ou droit expiré ; rétablir le droit/quota.

**Marche à suivre**

1. Préparer deux programmations dédiées avec destinataires consentants jamais sollicités : l’une dont le quota sera épuisé au départ, l’autre dont le droit aura expiré ; faire établir ces états par le référent.
2. Comme gestionnaire A1 habilité, ouvrir leur suivi au moment prévu ; vérifier suspension et information adressée au gestionnaire, sans dépôt Live.
3. Faire régulariser le quota ou le droit par le parcours normal sur les jeux dédiés ; relever le changement de période/renouvellement.
4. Rouvrir Live des destinataires et les campagnes avant toute confirmation ; vérifier qu’aucun envoi n’a repris automatiquement.
5. Examiner de nouveau contenu, date, audience et droits puis confirmer explicitement la reprise de chaque campagne.
6. Suivre leur résultat : contrôles courants appliqués, dépôt seulement après confirmation et débit conforme au premier démarrage effectif.

**Résultat attendu.** Campagne suspendue et gestionnaire informé ; aucun envoi automatique au nouveau mois/renouvellement ; confirmation explicite et vérifications avant reprise.

### RM-17-07

**Scénario.** Cibler la même personne dans deux campagnes/animations de A1 sur 24 h, avec plusieurs appareils ; attendre/préparer la fin de fenêtre.

**Marche à suivre**

1. Préparer une personne synthétique participant à deux animations A1, consentante et liée à deux appareils, ainsi que des crédits suffisants ; le référent établit un jeu dédié sans sollicitation dans les 24 heures précédentes.
2. Comme gestionnaire habilité, envoyer une première campagne depuis l’une des animations ; noter l’instant du premier dépôt et contrôler Live sur les appareils liés.
3. Dans les 24 heures glissantes, tenter une deuxième campagne depuis l’autre animation vers la même personne ; vérifier l’exclusion de fréquence quel que soit l’appareil.
4. Relire le rapport et les compteurs : plusieurs appareils n’accordent pas plusieurs droits et la deuxième campagne n’est pas mise en attente d’un envoi automatique.
5. À l’issue réelle de la fenêtre, ou sur le cas daté distinct préparé par le référent, vérifier qu’aucun ancien message exclu n’a été envoyé automatiquement ; lancer explicitement une nouvelle campagne et constater sa nouvelle éligibilité.
6. Sur ce jeu, vérifier séparément une notification automatique de service prévue ; elle reste indépendante de la limite des messages organisateur.

**Résultat attendu.** Limite initiale 1 message par personne/commune/24 h glissantes ; deuxième exclusion sans envoi différé automatique ; plusieurs appareils ne multiplient pas les droits ; notifications automatiques indépendantes.

### RM-17-08

**Scénario.** Cibler cette personne avec une troisième campagne distincte ; rejouer une reprise puis répéter sur plusieurs participants ; ajuster limite/multiplicateur côté ERP habilité.

**Marche à suivre**

1. Préparer un jeu isolé A1 avec plusieurs participants consentants, trois campagnes distinctes vers chacun dans une même fenêtre de 24 heures, limite initiale 1 et multiplicateur 3 ; disposer d’un opérateur ERP habilité et d’un lecteur sans autorisation.
2. Comme gestionnaire Communication, démarrer la première campagne puis tenter la deuxième et la troisième ; vérifier que les tentatives bloquées par fréquence figurent au suivi malgré l’absence de message.
3. Avec le référent, reprendre une de ces mêmes campagnes sans en créer une nouvelle ; vérifier que la reprise ne compte pas comme quatrième tentative.
4. Dans Ops et la boîte interne de test, contrôler une alerte au seuil de trois fois la limite, puis répéter les dépassements pour les autres participants ; vérifier leur regroupement sans email par personne.
5. Dans **ERP → Animation → Sollicitations**, comme opérateur habilité, modifier limite et multiplicateur avec motif sur ce seul jeu ; vérifier la trace et les nouvelles valeurs.
6. Comme lecteur non habilité, tenter le même réglage ; vérifier le refus, puis faire remettre les valeurs initiales par l’opérateur habilité et consigner le réglage final.

**Résultat attendu.** Alerte initiale à 3 fois la limite, tentatives bloquées incluses, reprises non recomptées ; alerte Ops et email interne regroupé, pas un email par personne ; réglage tracé et refusé sans autorisation.

### RM-17-09

**Scénario.** **Accompagné :** interrompre une campagne partiellement commencée, expirer le module puis reprendre, avec consentement retiré d’un destinataire restant.

**Marche à suivre**

1. Avec le référent, préparer une campagne dédiée à trois destinataires consentants distincts, module actif et quota disponible ; prévoir l’interruption après un premier dépôt Live, avant les suivants.
2. Comme gestionnaire A1 habilité, lancer la campagne puis faire interrompre le traitement ; relever référence, audience figée, destinataire servi et crédit unique débité.
3. Faire constater l’expiration commerciale du module sur ce jeu ; retirer l’accord organisateur d’un destinataire restant et inscrire un nouveau participant après le démarrage.
4. Reprendre la même campagne avec l’acteur toujours habilité ; vérifier que le destinataire restant consentant peut être servi et que celui ayant retiré son accord est exclu.
5. Vérifier que le nouveau participant ne rejoint pas l’audience figée, que le premier ne reçoit pas un second message Live et qu’aucun nouveau crédit n’est débité.
6. Lire les états de dépôt et de transport : échecs/incertitudes visibles, sans annonce de livraison certaine au navigateur sans preuve ni nouveau dépôt pour réparer seulement le Push.

**Résultat attendu.** Campagne terminable avec audience figée, droits des destinataires restants revérifiés ; pas de double message Live ni double débit. Échecs/incertitudes visibles ; aucune livraison navigateur certaine annoncée sans preuve.

### RM-17-10

**Scénario.** Préparer une campagne dont tous les destinataires sont exclus par préférence ou fréquence, puis lancer son traitement.

**Marche à suivre**

1. Préparer deux audiences dédiées entièrement exclues, l’une par refus/absence d’accord organisateur, l’autre par fréquence déjà atteinte ; réserver quota disponible, module actif et gestionnaire habilité.
2. Dans chaque fiche **Communication**, rédiger un message propre à la variante puis ouvrir l’aperçu ; relever les motifs d’exclusion et le quota avant action.
3. Confirmer le traitement de chaque campagne et attendre le rapport final.
4. Vérifier le résultat sans destinataire, avec motifs consultables, et l’absence de message dans Live ou Push ainsi que de repli email/SMS.
5. Comparer les quotas avant/après : aucun crédit consommé faute de premier dépôt Live ; avec le référent, vérifier que les tentatives de fréquence pertinentes pour les alertes restent tracées.

**Résultat attendu.** Résultat « sans destinataire », motifs d'exclusion consultables ; aucun message et aucun crédit de campagne consommé. Les tentatives éligibles à l'alerte de fréquence restent tracées.

### RM-17-11

**Scénario.** **Accompagné :** avec un seul crédit disponible, lancer deux campagnes ayant chacune un destinataire autorisé distinct.

**Marche à suivre**

1. Avec le référent, préparer un contexte commune/souscription dédié ayant exactement un crédit disponible et deux campagnes prêtes, chacune avec un destinataire consentant distinct sans fréquence bloquante.
2. Ouvrir les deux campagnes dans deux sessions Communication habilitées ; contrôler module, fenêtre, audience et absence de dépôt préalable.
3. Déclencher leurs démarrages presque simultanément selon le dispositif contrôlé par le référent.
4. Actualiser les rapports et les deux carnets Live : une seule campagne démarre et dépose son message ; l’autre reste suspendue sans message.
5. Contrôler le compteur à zéro, jamais négatif, et un seul débit ; recharger/reprendre les mêmes références pour vérifier l’absence de double ouverture ou de second dépôt.

**Résultat attendu.** Une seule campagne peut démarrer et débiter le dernier crédit ; l'autre reste suspendue sans message. Aucun quota négatif ni double ouverture.


## F18 — Site public Animation, inscription et continuité de Live

**Objet.** Présenter Animation comme un produit autonome, avec un site de découverte lisible et un accès continu aux participations et gains existants.

**Accès.** Site public configuré en surface Animation, cible `animations.localeo.city` ; Live ; anciens liens emails/QR. **US23 ; CA23–24.**

**Prérequis à vérifier**

- [ ] URL de recette de la surface Animation et origine publique configurées ; liens vers portail et Live résolus.
- [ ] Animation publiée, commerce Animation seul, participant neuf et participant avec ancien carnet incluant des coffrets.
- [ ] Anciens emails/QR de test ; navigateur ayant accepté puis autre ayant refusé Push.

### ~~RM-18-01~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Découvrir une animation, sa fiche, les commerçants et les modalités ; s’inscrire puis participer.~~

**Marche à suivre**

1. Ouvrir l’URL de recette du site public Animation dans un navigateur de participant neuf ; vérifier avec le référent qu’elle sert bien la surface Animation.
2. Rechercher l’animation publiée du jeu, ouvrir sa fiche et lire dates, modalités, règlement et commerces participants.
3. Revenir à la découverte puis retrouver la fiche ; vérifier que les contenus expliquent la participation et que les menus de gestion du client ne sont pas exposés.
4. Suivre le parcours d’inscription avec les coordonnées synthétiques prévues et les choix proposés ; relever la référence de participation sans copier de lien privé.
5. Ouvrir Live par le parcours proposé et commencer une action de participation autorisée pour cette animation.
6. Vérifier que la participation existe une seule fois, qu’aucun achat de coffret n’a été imposé et que la suite du jeu est compréhensible ; consigner les écrans parcourus et le résultat.

**Résultat attendu.** ~~Parcours autonome sans achat de coffret imposé ; contenus de communication compréhensibles, sans menus d’administration client.~~

Preuve du 23 octobre 2026 : `public-discovery-clone-rm18-01-completude-scellee.json` relie les six étapes à leurs rapports et empreintes. Surface publique Animation dédiée, découverte, inscription unique, ajout au carnet, Live et présentation du QR personnel réussis ; les liens générés ont été contrôlés après correction de la configuration locale. Clone isolé uniquement ; aucun achat imposé ni déploiement sur TEST partagé.

### ~~RM-18-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Ouvrir la fiche d’un commerce Animation seul et ses animations liées.~~

**Marche à suivre**

1. Faire identifier par le référent un commerce dont seul le périmètre Animation est actif et une animation publiée à laquelle il participe.
2. Sur le site public Animation de recette, ouvrir cette animation puis la fiche du commerce participant.
3. Lire la présentation du commerce, ses informations publiques et les animations qui lui sont liées ; comparer les références au jeu préparé.
4. Ouvrir une animation liée puis revenir à la fiche pour vérifier que le parcours reste utilisable.
5. Vérifier que la fiche ne présente aucune prestation Coffrets ni qualité de fournisseur Coffrets non acquise ; relever tout contenu contradictoire, sans déduire un droit d’une simple présence publique.

**Résultat attendu.** ~~Présence publique Animation ; aucune présentation comme fournisseur de prestations Coffrets sans ce périmètre.~~

Preuve du 23 octobre 2026 : `public-discovery-clone-rm18-02-completude-scellee.json` relie les cinq étapes aux rapports et empreintes. Commerce fictif activé Animation seul par les commandes normales dans une nouvelle commune dédiée, convention scannée par antivirus réel, Coffrets non demandé. Fiche publique, description, animation liée et retour réussis ; aucune prestation ni qualité de fournisseur Coffrets présentée. Clone isolé uniquement ; les communes existantes restent hors de cette bascule.

### RM-18-03

**Scénario.** Ouvrir anciens QR/emails/carnets puis accéder au nouveau site ; suivre la reprise explicite si proposée.

**Marche à suivre**

1. Préparer avec le participant de test son ancien carnet Live contenant participations, gains et coffrets ; relever leurs références dans une preuve sans secret.
2. Depuis le navigateur qui conserve ce carnet, ouvrir successivement un ancien email, un ancien QR puis l’accès habituel à Live ; vérifier l’objet retrouvé à chaque fois.
3. Ouvrir la nouvelle surface Animation et accéder à Live depuis cette surface.
4. Si une reprise de carnet est proposée entre origines, suivre explicitement l’export puis l’import prévus, avec un fichier privé conservé dans l’espace de recette ; ne pas le joindre au compte rendu.
5. Comparer comptes, participations, gains et coffrets avant/après ; vérifier que le carnet d’origine existe encore et qu’aucun doublon n’est apparu.
6. Ouvrir séparément les anciens liens préparés comme inactifs ou expirés ; vérifier qu’un message explique leur situation et permet de comprendre la suite, sans page vide ; consigner chaque variante.

**Résultat attendu.** Mêmes comptes, participations et gains ; aucun doublon ni perte de coffrets déjà présents dans Live. Liens inactifs/expirés expliqués plutôt qu’une page vide.

Complément essentiel du 30 octobre 2026, **partiel sur le clone isolé** : dix
contrôles réussis. Une participation est ajoutée volontairement au carnet depuis
le lien conservé dans son reçu réel d’inscription 201, puis transférée par les
boutons de sauvegarde/import entre la marketplace et le site public Animation
local distinct. Sept exports contrôlés : second carnet initialement vide,
identité et empreinte de capacité conservées, réimport sans doublon et carnet
d’origine intact. La participation importée est rouverte ; la même projection
du gain est relue, sans transfert d’un bon autonome. Les initialisations Live
facultatives sont bloquées avant transmission par le garde réseau : la reprise
locale reste utilisable dans cette indisponibilité. Ancien carnet prérestauration,
coffret, anciens QR/emails reçus et accès propre au bon non prouvés ; scénario
non barré. Preuve `essentiels-rm1803-carnet-20261030-reprise2-prive.json`.

### RM-18-04

**Scénario.** Refuser la réactivation des notifications sur la nouvelle origine, puis participer et lire la messagerie ; refaire en acceptant.

**Marche à suivre**

1. Préparer deux profils de navigateur pour le participant : l’un ayant autorisé Push sur l’ancienne origine, l’autre permettant de tester le refus sur la nouvelle ; prévoir un message de test déjà disponible dans Live.
2. Ouvrir la nouvelle surface Animation avec le premier profil et observer la demande éventuelle d’autorisation propre à cette origine.
3. Refuser les notifications lorsqu’elles sont proposées ; vérifier que l’ancienne permission n’est pas annoncée comme automatiquement transférée.
4. S’inscrire ou poursuivre la participation prévue, puis ouvrir la messagerie Live et lire le message de test ; vérifier que le refus Push ne bloque aucune de ces actions.
5. Avec le second profil, refaire le parcours en acceptant les notifications lorsque le navigateur le permet ; ouvrir la participation et le même type de message Live.
6. Comparer les deux résultats : les parcours métier restent accessibles dans les deux cas ; relever séparément la permission et, si testé avec le référent, la réception Push, sans assimiler permission accordée et livraison prouvée.

**Résultat attendu.** Push facultatif ; ni participation ni lecture Live bloquée. Une ancienne permission navigateur n’est pas présentée comme transférée automatiquement entre origines.


## F19 — Aide et support de l’organisateur

**Objet.** Trouver une aide utile et suivre une demande privée, avec un délai de première réponse humaine identifiable.

**Accès.** Animation → **Support**/aide ; Localeo Support côté opérateur. **US31 ; CA58.**

**Prérequis à vérifier**

- [ ] Guides/FAQ accessibles, compte client A et agent Support autorisé.
- [ ] Calendrier de service actif ; demande ancienne sans réponse humaine et autre avec note interne.

### ~~RM-19-01~~ — **Réussi**

**Scénario.** ~~Consulter l’aide puis créer une demande liée à une animation ; répondre côté Support puis client.~~

**Marche à suivre**

1. Se connecter au portail Animation avec un membre habilité de A, choisir A1 et ouvrir **Support** ; consulter l’aide et la FAQ proposées.
2. Créer une demande synthétique liée à l’animation du jeu, en décrivant un problème identifiable ; noter sa référence et son état.
3. Recharger la page puis rouvrir la demande ; vérifier que le texte et le rattachement sont conservés et qu’un seul dossier existe.
4. Dans une session distincte, connecter l’agent habilité à Localeo Support, ouvrir **Organisations Animation**, retrouver la référence et envoyer une réponse destinée au client.
5. Revenir au compte client, relire le dossier et répondre dans le même échange ; distinguer la réponse enregistrée d’un éventuel email encore en cours d’envoi.
6. Recharger les deux vues et comparer référence, messages et état ; vérifier l’ordre des échanges et l’absence de duplication, puis consigner le résultat sans note interne ni donnée personnelle réelle.

**Résultat attendu.** ~~Échange persistant dans un même dossier, état et référence lisibles ; pas de duplication après rechargement/reprise.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Après constat du backend `1.0.0+3720a08` sur API et BackOffice, le rapport privé `run-1792772538662-5ec2` porte le verdict `REUSSI_AUTOMATIQUE` : aide/FAQ, demande liée au brouillon A1, réponses Support puis client, rechargements et unicité vérifiés. Le suivi distingue le message enregistré du statut email ; aucune réception email n'est déduite d'une mise en file. Voir le [suivi d'automatisation](automatisation-recette.md#nouveaux-passages-ciblés-du-23-octobre).

### ~~RM-19-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Comparer accusé automatique, cible de 2 jours ouvrés et première réponse humaine.~~

**Marche à suivre**

1. Faire préparer par le référent une demande récente et une demande ancienne sans réponse humaine, avec leur calendrier de service et leurs dates d’ouverture ; ne pas modifier l’horloge de l’environnement.
2. Comme membre habilité de A, ouvrir **Support**, retrouver la demande récente et lire l’accusé automatique, la date d’ouverture et l’échéance annoncée.
3. Calculer avec le calendrier préparé la cible de deux jours ouvrés ; vérifier qu’elle concerne la première réponse humaine et ne promet pas une résolution en deux jours.
4. Ouvrir la demande ancienne ; vérifier que l’accusé automatique et une éventuelle note interne n’ont pas effacé l’attente de réponse humaine ou son retard.
5. Faire répondre l’agent dans **Support → Organisations Animation**, puis relire côté client la première réponse humaine et son horodatage.
6. Comparer l’attente avant/après la réponse à l’échéance initiale et consigner séparément les deux dossiers ; un calendrier absent ou un état daté non préparé empêche de valider la variante concernée.

**Résultat attendu.** ~~Accusé ne vaut pas prise en charge humaine ; délai et éventuel retard ne sont pas masqués par l’automatisme. Aucune promesse de résolution en 2 jours n’est déduite.~~

Preuve complète du 30 octobre 2026 : les onze contrôles du dossier récent A
créé le 24 sont complétés par dix contrôles sur un dossier B ouvert le 23 et
resté sans réponse. Chaque dossier est lu par le client habilité de son
organisation. Les calendriers de création persistés sont lus sans écriture :
deux jours ouvrés de 9 h à 17 h pour A, de 9 h à 18 h pour B. Week-end et
changement d’heure compris, cibles respectives au 27 octobre à 17 h et 18 h
Paris. Le retard de B est constaté naturellement le 30, sans modifier l’horloge.
Une note interne normale conserve l’absence de première réponse et le retard,
et reste invisible au client. La réponse Support unique est ensuite horodatée
après l’échéance, visible côté B ; attente levée, échéance et calendrier
initiaux conservés. Le dossier récent A est relu inchangé.
Les six étapes et quinze pièces figées sont reliées dans
`rm1902-clone-preuves-completes-20261030.json` ; revue indépendante sans écart
bloquant. Réponse de recette automatisée via session opérateur autorisée,
de type LOCALEO dans le contrat ; aucune réception email réelle revendiquée.
Les deux incidents de harnais antérieurs sont conservés, sans commande engagée.

### ~~RM-19-03~~ — **Réussi**

**Scénario.** ~~Consulter avec A une demande de B et chercher les notes internes depuis le compte client.~~

**Marche à suivre**

1. Faire préparer une demande de A avec réponse publique et note interne, ainsi qu’une demande de B ; récupérer seulement les liens nécessaires dans l’espace privé de recette.
2. Avec le compte client A, ouvrir **Support** dans A1 et consulter sa demande.
3. Vérifier que les échanges destinés au client sont lisibles et que le texte de la note interne fourni comme repère par l’agent n’apparaît pas.
4. Ouvrir directement le lien de la demande de B dans cette même session A ; vérifier le refus sans affichage du sujet, des messages ou des coordonnées de B.
5. Revenir à la liste et à la demande de A, puis recharger ; vérifier que ni la demande de B ni la note interne n’apparaissent après ce changement de navigation et consigner les deux refus.

**Résultat attendu.** ~~Données étrangères et notes internes inaccessibles ; seuls échanges destinés au client visibles.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Le rapport privé `run-1792773007754-8aca` porte le verdict `REUSSI_AUTOMATIQUE` : échanges publics de A visibles, demande de B et notes internes refusées, absence de divulgation des repères synthétiques vérifiée après retour et rechargement. Voir le [suivi d'automatisation](automatisation-recette.md#nouveaux-passages-ciblés-du-23-octobre).


## F20 — Préparer une nouvelle édition

**Objet.** Réutiliser les contenus d’une animation en conservant les validations indispensables à chaque nouvelle édition.

**Accès.** Animation → fiche → nouvelle édition. **US32 ; CA59.**

**Prérequis à vérifier**

- [ ] Animation source avec dates, contenus, commerçants, participants, gains et accords ; gestionnaire autorisé.
- [ ] Commune A2 également accessible au gestionnaire pour tester le refus intercommune.

### ~~RM-20-01~~ — **Réussi**

**Scénario.** ~~Choisir les sections à réutiliser et de nouvelles dates ; créer l’édition dans A1 puis tenter A2.~~

**Marche à suivre**

1. Se connecter comme gestionnaire autorisé sur A1 et A2 ; dans **Animations**, ouvrir l’animation source de A1 et relever sa référence, ses dates et ses contenus.
2. Depuis sa fiche, ouvrir la préparation d’une nouvelle édition ; sélectionner les sections à réutiliser et saisir de nouvelles dates cohérentes.
3. Confirmer la création pour A1, puis ouvrir le résultat ; vérifier qu’il s’agit d’un nouveau brouillon, avec une référence distincte et une provenance identifiable.
4. Revenir à l’animation source et vérifier qu’elle conserve ses dates, contenus et état.
5. Reprendre la préparation depuis la même source et tenter une destination A2 par le parcours disponible ; si l’interface ne permet pas cette destination, faire vérifier le refus de la commande correspondante par le référent.
6. Vérifier qu’aucun brouillon issu de cette source n’a été créé dans A2, même avec les droits du gestionnaire sur A2 ; consigner séparément création A1 et refus A2.

**Résultat attendu.** ~~Nouveau brouillon dans la même commune seulement ; source conservée, provenance identifiable ; A2 refusée même si accessible au gestionnaire.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Rapport privé `run-1792774003896-55cb`, verdict `REUSSI_AUTOMATIQUE` : nouvelle édition créée dans A1, source conservée, refus A2 HTTP 422 `COMMUNE_EDITION_DIFFERENTE` et inventaires des deux communes comparés sans création indue. Voir le [suivi d'automatisation](automatisation-recette.md#nouveaux-passages-ciblés-du-23-octobre).

### ~~RM-20-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Examiner participants, gains, QR, paiements, accords et consentements du brouillon ; tenter sa publication.~~

**Marche à suivre**

1. Avec le gestionnaire A1, relever sur la source les références des participants, gains, QR, paiements, accords et consentements ; garder les secrets hors des preuves.
2. Créer une nouvelle édition avec les sections de contenu prévues, puis ouvrir le nouveau brouillon dans **Animations**.
3. Examiner ses participants, lots/gains et éléments financiers accessibles ; faire compléter par le référent la vérification des objets non visibles à l’écran.
4. Vérifier qu’aucun participant, gain, QR utilisable, paiement, accord ou consentement de la source n’a été recopié.
5. Ouvrir l’assistant de publication du brouillon et contrôler les points à revalider : commerçants, droits actuels, dotation, règlement, accords et préparation selon le type.
6. Tenter de publier alors qu’un prérequis obligatoire identifié manque ; vérifier le blocage expliqué et le maintien du brouillon, puis consigner le prérequis et l’absence de publication.

**Résultat attendu.** ~~Aucun de ces objets recopié ; commerçants, droits, dotation, règlement et accords à revalider ; publication bloquée tant que nécessaire.~~

Preuves vérifiées le 24 octobre 2026 : `edition-objets-clone-sceau-completude.json`. Nouvelle édition créée par le formulaire normal ; les six familles présentes sur la source ne sont pas copiées : participants, gains, QR, paiements, accords et consentements. Contrôle UI/API complété par une relecture SQL strictement en lecture seule. Source inchangée ; prérequis manquants affichés, publication refusée avec HTTP 422 et brouillon conservé. Clone isolé uniquement.

### ~~RM-20-03~~ — **Réussi**

**Scénario.** ~~**Accompagné :** modifier la source après ouverture du formulaire ou reprendre une création après réponse perdue.~~

**Marche à suivre**

1. Avec le référent, préparer deux essais distincts et une animation source de A1 ; ouvrir le formulaire de nouvelle édition comme gestionnaire, en laissant la saisie ouverte.
2. Dans une seconde session autorisée, modifier un contenu de la source et enregistrer ; revenir au premier formulaire sans l’actualiser.
3. Confirmer la nouvelle édition depuis cette version ancienne ; vérifier un conflit explicite et l’absence de brouillon assemblé à partir de versions incohérentes.
4. Relire la source et reprendre la saisie selon les indications affichées ; conserver les références pour distinguer cette reprise du second essai.
5. Pour le second essai, faire préparer au référent une perte contrôlée de réponse lors de la création, sans modifier les données ; utiliser ensuite le parcours de consultation du résultat ou de reprise de la même opération.
6. Ouvrir **Animations**, retrouver le résultat et vérifier qu’une seule nouvelle édition correspond à cette création reprise ; relever référence et message de reprise, sans lancer volontairement une seconde création indépendante.

**Résultat attendu.** ~~Conflit de version explicite, pas de copie incohérente ; un seul nouveau brouillon pour une même création reprise.~~

**Exécution automatique réussie du 23 octobre 2026 sur TEST.** Rapport privé `run-1792774003896-55cb`, verdict `REUSSI_AUTOMATIQUE` : modification concurrente réelle, conflit explicite et saisie actualisée ; réponse coupée après création serveur puis même reçu consulté, un seul brouillon et aucune seconde commande. Voir le [suivi d'automatisation](automatisation-recette.md#nouveaux-passages-ciblés-du-23-octobre).


## F21 — Objectifs, sources de diffusion, bilans et satisfaction

**Objet.** Montrer les résultats réellement mesurés et leur provenance, sans assimiler des passages à du chiffre d’affaires.

**Accès.** Animation → fiche/bilan, **Bilans** ; Live après clôture. **US33 ; CA60.**

**Prérequis à vérifier**

- [ ] Objectifs avant publication ; liens/QR « mairie » et « commerçant » ; inscriptions avec et sans source.
- [ ] Jeu chiffré connu : inscriptions, démarrages, parcours terminés, validations QR/PIN, gains et remises ; une correction de remise et un remplacement de gagnant.
- [ ] Animation clôturée et au moins deux répondants de test ; compte organisateur sans accès à leur identité via l’enquête.

### ~~RM-21-01~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Fixer les objectifs puis publier ; tenter de changer les objectifs ; comparer résultats et édition comparable.~~

**Marche à suivre**

1. Comme gestionnaire A1, ouvrir un brouillon prêt à publier, un second sans objectif et une édition comparable préparée avec le référent ; identifier aussi un indicateur sans collecte et un indicateur mesuré à zéro.
2. Dans le premier brouillon, renseigner les objectifs proposés et enregistrer ; relever leurs valeurs avant publication.
3. Publier les deux brouillons après satisfaction de leurs prérequis ; vérifier que l’absence d’objectif n’empêche pas à elle seule la publication du second.
4. Revenir aux objectifs du premier et tenter une modification après publication ; vérifier qu’ils restent figés aux valeurs relevées.
5. Ouvrir le bilan de la fiche ou **Bilans**, lire les résultats et la comparaison à l’édition préparée ; vérifier que définitions et conditions de comparaison sont compréhensibles.
6. Comparer les exemples « zéro mesuré » et « absence de données » ; vérifier qu’ils ne sont pas présentés comme équivalents et consigner les objectifs et résultats observés.

**Résultat attendu.** ~~Objectifs facultatifs mais figés à publication ; définitions et comparabilité lisibles ; absence de données distincte de zéro.~~

**Exécution réussie du 24 octobre 2026 sur le clone isolé.** Le même brouillon
publié conserve ses objectifs 7/5/3 figés : modification refusée 409 et champs
désactivés ; zéro mesuré distinct de la satisfaction non collectée. L’autre
édition publiée n’a aucun objectif. Les deux clôtures ont été réalisées par le
parcours normal, sans dates forcées : mêmes commune, moteur et définitions,
fenêtres complètes et couverture complète. Comparaison visible de 0 et 4
inscrits, écart +4 ; les taux sans base de calcul restent absents.
Vingt-trois contrôles finaux, six étapes et empreintes dans
`sources-diffusion-clone-objectifs-comparer-sceau-completude.json` ; ancien
index partiel conservé, aucune publication rejouée.

### ~~RM-21-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Inscrire via les deux sources et sans source ; contrôler le bilan.~~

**Marche à suivre**

1. Faire préparer une animation publiée, deux liens ou QR de diffusion associés aux sources mairie et commerçant, et un accès direct sans source ; relever le nombre initial d’inscriptions.
2. Avec un premier participant synthétique neuf, ouvrir le lien mairie et terminer l’inscription ; relever sa référence sans secret.
3. Avec un deuxième participant distinct, refaire l’inscription depuis le QR ou lien commerçant.
4. Avec un troisième participant distinct, s’inscrire depuis l’accès direct sans source ; éviter de réutiliser le contexte de navigation des deux essais précédents.
5. Comme gestionnaire A1, ouvrir le bilan et consulter les sources ; comparer les variations des deux sources connues et de la catégorie inconnue aux trois inscriptions.
6. Vérifier que le total correspond aux inscriptions retenues ; faire joindre par le référent la preuve ciblée d’absence de suivi publicitaire entre sites, que les seuls chiffres du bilan ne démontrent pas.

**Résultat attendu.** ~~Attribution à la source connue et catégorie « inconnue », aucun suivi publicitaire entre sites ; total cohérent avec les inscriptions retenues.~~

Preuves vérifiées le 24 octobre 2026 : `sources-diffusion-clone-completude-scellee.json`. Deux sources créées depuis le formulaire organisateur et trois inscriptions réelles avec des participants et contextes distincts : mairie, commerce, accès direct. Bilan UI/API concordant : total 1 à 4, chaque catégorie augmente de un. Les trois traces réseau complètes ne montrent aucune tentative externe ni suivi publicitaire ; configuration et sources servies contrôlées. Les service workers sont bloqués pendant les inscriptions et leur portée Live a été auditée séparément. Les deux tentatives de police externe du portail gestionnaire sont signalées dans la preuve et exclues du constat relatif aux participants. Branche lien exercée, sans lecture optique revendiquée. Clone isolé uniquement.

### RM-21-03

**Scénario.** Vérifier les totaux avant/après remise, rescan, correction et remplacement à partir des références du jeu.

**Marche à suivre**

1. Avec le référent, dresser un tableau du jeu A1 : inscrits, parcours commencés/terminés, validations QR/PIN, gagnants et lots remis ; relever les références et totaux initiaux.
2. Comme gestionnaire A1, ouvrir le bilan de l’animation et comparer chaque indicateur à ce tableau, sans additionner des catégories différentes comme si elles représentaient des personnes distinctes.
3. Avec le commerçant et le participant prévus, réaliser une validation QR puis une variante PIN sur des objets distincts ; refaire la même validation sur chacun et relire le bilan.
4. Effectuer la remise prévue par le mode de dotation et la relire ; vérifier qu’un rescan ou une reprise n’ajoute pas une deuxième remise ni un deuxième passage.
5. Avec l’opérateur habilité, réaliser la correction de remise puis le remplacement de gagnant préparés ; après chaque action, actualiser le tableau attendu et comparer le bilan.
6. Vérifier que les indicateurs restent distincts et qu’aucun chiffre d’affaires n’est calculé à partir des passages ; consigner les écarts et références de chaque variante.

**Résultat attendu.** Aucun double comptage QR/PIN/rejeu ; indicateurs distincts inscrits, commencés/terminés, passages, gagnants et lots remis. Aucun chiffre d’affaires inventé à partir des passages.

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** :
quarante-deux valeurs du bilan relues dans l’interface et recoupées avec des
comptages indépendants en lecture seule. Remise puis correction du seul gain
externe dédié : lots remis 0 → 1 → 0, autres indicateurs et deux autres gains
inchangés. Les historiques distinguent attributions anciennes et gagnants
courants, ainsi que consommations QR/PIN et validations de parcours.
Les bilans avant/après une nouvelle validation QR/PIN et un remplacement
restent à vérifier ; scénario non barré. Preuve
`bilans-remises-principal-preuves-figees.json`.

Complément essentiel du 30 octobre 2026 : les QR des deux bons déjà consommés
sont saisis à nouveau dans Pro par le responsable puis le salarié. Les deux
rescans retrouvent les mêmes consommation et version, sans proposer une nouvelle
remise. Les sept indicateurs sont rapprochés des participants, attributions et
consommations, puis relus à l'identique dans le bilan avant/après ; aucun revenu
déduit. Les seules différences des réponses sont les dates techniques de génération
et d'observation du bilan. Une nouvelle relecture confirme tous les autres faits
strictement inchangés, sans rejouer de scan. Preuve privée
`essentiels-rm2103-20261030c-rescan-qualification.json` ; les incidents du harnais
restent conservés, dont une police externe demandée par le portail et bloquée.
Ce contrôle de bons ne constitue pas une nouvelle validation de parcours QR/PIN,
ni une lecture optique ; RM-21-03 reste partiel et non barré.

Sur une autre cohorte externe dédiée avec réserve disponible, un refus
synthétique est enregistré normalement puis un unique remplacement est accepté.
Douze contrôles groupés rapprochent les états et 21 valeurs du bilan à trois
stades : avant, après refus, après remplacement. Les 5 inscrits, 5 parcours
commencés et terminés, 5 passages, 3 gagnants courants et 0 lot remis restent
identiques. L'ancien gain REMPLACE est conservé : quatre attributions historiques
ne deviennent pas quatre gagnants. Le suppléant de rang 4 est utilisé ; celui de
rang 5, les deux autres gains et leurs événements restent inchangés. Auteur du
refus, motif, versions et reçu de remplacement sont rapprochés. Aucun rejeu.
Preuve privée `essentiels-rm2103-20261030c-remplacement-preuves-figees.json`,
quinze pièces scellées ; incident d'encodage initial conservé avant toute commande.
Les nouvelles validations de parcours QR/PIN et leurs rescans avec bilans
contemporains restent à exécuter ; scénario toujours non barré.

### ~~RM-21-04~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Après clôture, répondre dans Live avec note 1 puis 5 et commentaire facultatif ; tester 0/6, absence de réponse et accès avant clôture.~~

**Marche à suivre**

1. Préparer une animation avant clôture et une clôturée, deux participants répondants et un troisième qui ne répondra pas ; relever le nombre et la somme des notes déjà présentes.
2. Avec un participant, ouvrir Live avant la clôture et tenter l’accès à la satisfaction ; vérifier qu’aucune réponse anticipée ne peut être enregistrée.
3. Sur l’animation clôturée, répondre avec le premier participant en donnant la note 1 sans commentaire, puis avec le second en donnant 5 avec un commentaire synthétique identifiable.
4. Avec le référent si le contrôle de saisie ne les permet pas, tenter les notes 0 et 6 et vérifier leur refus sans ajout de réponse ; laisser le troisième participant poursuivre Live sans répondre.
5. Comme gestionnaire, ouvrir le bilan : avec deux seules réponses nouvelles, vérifier un ajout de deux réponses et de six points à la somme des notes, soit une moyenne de 3 si aucune autre note n’existait.
6. Lire les commentaires et vérifier l’absence d’identité ou d’identifiant participant ; contrôler avec les boîtes de test et le référent qu’aucune notification supplémentaire automatique n’a été produite par cette enquête.

**Résultat attendu.** ~~Enquête facultative accessible après clôture ; bornes respectées ; moyenne et nombre de réponses cohérents, commentaires sans identité affichée à l’organisateur ; aucune notification supplémentaire automatique.~~

Preuve du 23 octobre 2026 : `rm2104-live-complet-clone-rapport.json` dans le dossier privé de campagne. Dix contrôles réussis dans Live et Animation sur la cible restaurée isolée : refus avant clôture, deux répondants distincts (1 sans commentaire et 5 avec commentaire), bornes 0/6, troisième participant sans réponse, deux réponses et somme six, moyenne trois, commentaire anonyme et cinq canaux de notifications/outbox inchangés. Les erreurs initiales de sélecteur et de transport cookie du vérificateur sont conservées ; le contrôle final reprend en lecture seule, sans rejouer les réponses. Aucun transport fournisseur réel ni déploiement sur TEST partagé n'est revendiqué.


## F22 — Cohérence ERP, Support et Atelier

**Objet.** Retrouver les mêmes informations de produit et de lot dans les outils internes sans traiter un lot libre comme un coffret vendu.

**Accès.** ERP/Support → **Animations et lots** ; Atelier → sélection des fournisseurs. **US24 ; CA25.**

**Prérequis à vérifier**

- [ ] Une animation et un gain de chacune des trois dotations, un commerce Animation seul et un fournisseur Coffrets.
- [ ] Opérateurs habilités et lectures/export internes ; assez d’objets pour plusieurs pages.

### RM-22-01

**Scénario.** Retrouver chaque gain dans ERP/Support, filtrer par nature/commune, paginer et exporter la page affichée.

**Marche à suivre**

1. Préparer les références d’un gain Coffrets, d’un lot externe et d’un bon numérique, leurs états dans Animation/Pro/Live, ainsi qu’assez d’objets autorisés pour plusieurs pages.
2. Comme opérateur ERP habilité, ouvrir **Animations et lots**, rechercher les objets et comparer nature, état et chaîne lot/attribution/bon/remise aux références préparées.
3. Appliquer les filtres de nature et de commune, parcourir au moins deux pages et vérifier que les objets affichés respectent toujours filtres et droits.
4. Sur une page identifiée, utiliser **Exporter cette page (CSV)** ; comparer ses lignes aux seuls objets de cette page et vérifier que le fichier n’est pas annoncé comme l’ensemble des pages.
5. Dans une session Support habilitée, ouvrir **Animations et lots** et répéter recherche, filtres, pagination et export dans le périmètre de cet agent.
6. Comparer les informations communes entre ERP, Support et les applications métier ; vérifier l’absence de confusion entre remise externe, consommation numérique et prestations Coffrets, ainsi que l’absence d’objet étranger.

**Résultat attendu.** Libellés et états cohérents avec Animation/Pro/Live ; pas de confusion bon/coffret/externe, pas d’objet étranger ; CSV limité à la page affichée, conforme au filtre et aux droits. Il n'est pas présenté comme un export de toutes les pages.

Complément essentiel du 30 octobre 2026, **partiel sur le clone isolé** : sept
contrôles complètent les quatorze contrôles ERP/Support antérieurs. Les mêmes
trois gains sont rapprochés dans Animation : Coffret envoyé distinct de ses
prestations consommées, lot externe sans remise renseignée distinct d’une
remise déclarée, bon numérique consommé. Pro retrouve exactement la validation
active du même bon, état VALIDEE et canal QR_PRINCIPAL ; l’interface indique
« Lot remis ». Dans Live, l’échantillon externe est relu depuis son vrai reçu
d’inscription 201 avec les mêmes références. Aucune écriture métier transmise.
L’accès légitime Live aux deux autres échantillons n’est pas établi ; scénario
non barré. Preuve `essentiels-rm2201-preuves-20261030.json`.

Nouveau complément du 30 octobre 2026 : **onze contrôles réussis** retrouvent
dans Live le même gain numérique consommé à 320 et 1280 px, avec les mêmes
participant, animation, bon et libellé que les projections déjà rapprochées.
Le lien provient du reçu normal d'inscription 201 conservé (`inscrire-v4`),
sans extraction depuis la base ou une outbox. Aucune écriture métier ;
l'enregistrement technique Live est bloqué. Preuve privée
`essentiels-rm2201-20261030c-live-numerique-reprise1-prive.json`.
L'accès Live légitime au gain Coffrets reste à préparer ; scénario toujours partiel.

### ~~RM-22-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Vérifier les sommes financières des trois dotations ; tenter de sélectionner le commerce Animation seul comme fournisseur de prestation Coffrets dans Atelier.~~

**Marche à suivre**

1. Faire préparer un gain de chacune des trois dotations, un commerce Animation seul et un fournisseur Coffrets habilité ; relever les montants Coffrets attendus.
2. Comme opérateur interne habilité, consulter les lectures financières liées aux achats, commissions et reversements des objets préparés.
3. Comparer les sommes aux seules opérations Coffrets ; vérifier que lots externes et bons numériques n’ajoutent pas de montants Coffrets.
4. Dans Atelier, ouvrir le parcours de sélection des fournisseurs d’une prestation Coffrets et rechercher le commerce Animation seul.
5. Vérifier qu’il ne peut pas être retenu pour commander cette prestation ; faire contrôler par le référent le refus serveur d’une commande visant ce fournisseur, même si l’interface le masque.
6. Vérifier que le fournisseur Coffrets habilité reste sélectionnable selon ses prérequis habituels, sans commander réellement hors du jeu de recette ; consigner refus et comparaison financière.

**Résultat attendu.** ~~Lots libres exclus des achats/commissions/reversements Coffrets ; sélection et commande interdite côté serveur pour le fournisseur non habilité.~~

Preuve complète du 30 octobre 2026 : treize contrôles financiers complètent
les huit contrôles fournisseur rejoués après correction le 29 octobre.
Les quatre achats Coffrets du jeu totalisent 179,60 € ; les trois mouvements
uniques représentent 33,84 € dus aux commerçants et 5,96 € de commissions
constatées. Montants, références et états sont rapprochés dans les vues ERP
avec les faits indépendants en lecture seule, identiques avant/après.
Les deux animations libres n’ajoutent aucun achat Coffret, instance,
reversement ou commission. Le fournisseur Animation seul reste bloqué dans
l’interface et refusé 403 sans effet côté serveur ; le fournisseur historique
ouvert Coffrets reste sélectionnable à 320/1280 px. Leur état ACTIF et leur
commune accessible sont relus le 30 octobre. Aucun nouvel achat, paiement,
transfert ou correctif financier appliqué ; la lecture des commissions porte
sur les valeurs existantes, colonne Avant. Les six étapes sont reliées aux
preuves dans `rm2202-clone-preuves-completes-20261030.json`, avec 29 pièces
figées pour le passage principal. Anomalie et validation dans le
[registre backend](../../roadmap/anomalies/backend.md).

### ~~RM-22-03~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Ouvrir une projection commerciale/CRM disponible et ses liens vers les parcours métier.~~

**Marche à suivre**

1. Avec le référent, identifier une projection commerciale/CRM réellement disponible et les objets synthétiques qu’elle présente ; si aucun parcours n’est disponible, consigner la limite au lieu de considérer le CRM complet comme livré.
2. Comme opérateur habilité, relever dans les parcours métier les ventes, paiements, activations et périmètres actuels de ces objets.
3. Ouvrir la projection disponible et consulter ses informations commerciales sans confirmer d’action métier.
4. Suivre ses liens vers les fiches ou parcours autorisés, puis revenir et recharger la projection.
5. Comparer les états aux références initiales : la consultation n’a créé aucune vente, paiement, activation ou extension de périmètre ; consigner exactement la projection testée, sans inclure le CRM complet ni l’import E71 dans cette validation.

**Résultat attendu.** ~~Consultation ne crée ni vente, paiement, activation ou périmètre. Le CRM complet et son import E71 ne sont pas considérés comme livrés par E73.~~

Preuve du 23 octobre 2026 : `rm2203-clone-preuves-completes.json` relie cinq contrôles navigateur aux instantanés SQL en lecture seule avant/après. Projection testée : disponibilité du catalogue et diagnostic commercial 360 ; liens métier, retour et rechargement réels. Ventes, paiements, instances, statuts et périmètres des objets concernés restent identiques. Aucun CRM complet ni import E71 déclaré livré ; clone isolé uniquement.

## F23 — Usages, coûts internes et alertes de budget

**Objet.** Permettre au client de comprendre ses usages et à Localeo de suivre ses coûts sans exposer ses informations internes ni déclencher une facturation automatique.

**Accès.** Client → usages/quotas/factures ; ERP → pilotage économique ; Ops → alertes. **US34 ; CA61.**

**Prérequis à vérifier**

- [ ] Mesures d’emails, SMS, préparation de chasse, stockage, Push et support : valeurs constatées, estimées et indisponibles.
- [ ] Traitement de pilotage et alertes configurés ; budget synthétique de 100 € pour A et aucun budget pour B.
- [ ] Profils client et Localeo habilité ; deux périodes mensuelles identifiées.


### RM-23-01

**Scénario.** Consulter coûts par organisation puis commune/souscription/module selon données ; comparer au compte client.

**Marche à suivre**

1. Faire préparer les mesures d’emails, SMS, chasse, stockage, Push et support de A sur deux mois, avec exemples constatés, estimés et non valorisés ; identifier leurs rattachements disponibles.
2. Comme administrateur ou Finance habilité, ouvrir **ERP → Pilotage économique** et sélectionner l’organisation A et le premier mois.
3. Consulter la répartition par commune, souscription et module lorsque la source le permet ; comparer postes, période, rattachements et fiabilité aux mesures préparées.
4. Passer au second mois et vérifier que les valeurs restent associées à la bonne période et que les estimations ou absences ne sont pas présentées comme des dépenses certaines.
5. Dans une session client A, ouvrir les vues d’usages, quotas et **Finance**, puis consulter les factures accessibles.
6. Vérifier que le client retrouve ses usages, quotas et factures sans coûts ni marges internes ; tenter avec l’aide du référent l’accès direct à une lecture interne et vérifier le refus.

**Résultat attendu.** Interne : postes, période et fiabilité explicites. Client : usages, quotas, factures seulement ; pas de coûts/marges internes. Donnée absente ou estimation jamais présentée comme dépense certaine.

Passage principal du 24 octobre 2026, **partiel sur le clone isolé** : huit
contrôles réussis sur les deux mois affichés, les six postes, leur ventilation,
les vues Abonnement/Finance du client et le refus 403 d’une lecture interne
directe. Les familles de mesures constatées, estimées et non valorisées ne sont
pas toutes préparées sur deux mois ; le scénario reste non barré. Preuve privée
`couts-principal-clone-rapport.json`, aucune commande métier exécutée.

### ~~RM-23-02~~ — **Réussi sur le clone isolé**

**Scénario.** ~~**Accompagné :** faire passer le coût suivi de 79 à 80 puis 100 € ; rejouer les événements ; consulter l’organisation sans budget.~~

**Marche à suivre**

1. Faire préparer au référent un mois de recette avec budget de 100 € pour A, aucun budget pour B et des événements économiques synthétiques rejouables ; identifier les destinataires internes de test.
2. Comme opérateur habilité, ouvrir **Pilotage économique** et Ops ; faire établir le coût suivi de A à 79 € par le traitement prévu et vérifier l’absence d’alerte de seuil.
3. Faire traiter l’événement portant le total à 80 € ; relire le coût et vérifier l’alerte interne à 80 %, avec sa référence et sa période.
4. Faire traiter l’événement portant le total à 100 € ; vérifier l’alerte à 100 % dans les lectures internes et le canal de test prévu.
5. Faire rejouer exactement les mêmes événements par le mécanisme de reprise, puis relire valeurs et alertes ; vérifier l’absence de double mesure et de doublon logique d’alerte.
6. Consulter B après traitement de ses mesures : le suivi doit rester disponible sans alerte de budget ; consigner les quatre variantes sans modifier directement les tables.

**Résultat attendu.** ~~Alertes internes aux seuils 80 %/100 %, pas de doublon logique au rejeu ; sans budget, suivi disponible sans alerte de budget.~~

Preuve du 23 octobre 2026 : `rm2302-clone-preuves-completes.json` relie les commandes économiques normales, leurs rejeux HTTP réels, les lectures ERP/Ops et le canal de test outbox local. Budget 100 €, coûts synthétiques explicitement estimés 79/80/100 €, alerte logique unique aux seuils 80/100, deux intentions de notification et organisation B suivie sans budget ni alerte. Aucune écriture SQL métier, facture ni livraison fournisseur ; clone isolé uniquement.

### ~~RM-23-03~~ — **Réussi sur le clone isolé**

**Scénario.** ~~Après dépassement, consulter abonnement, quotas et parcours de l’organisateur.~~

**Marche à suivre**

1. Avant le dépassement, comme responsable A, relever dans **Abonnement** et **Finance** les droits, quotas, factures et échéances ; conserver les références d’un parcours organisateur autorisé.
2. Faire confirmer par le référent un dépassement du budget interne sur ce même jeu, sans autre changement de souscription, usage ou statut.
3. Recharger **Abonnement**, les usages et **Finance** avec le compte client A.
4. Comparer aux relevés : aucun supplément facturé, aucune suspension et aucun changement de quota ne doivent provenir de cette seule alerte.
5. Reprendre le parcours organisateur choisi et vérifier qu’il reste autorisé dans ses droits initiaux ; consigner l’alerte interne et les états client comparés, en distinguant toute consommation normale liée à l’action de test.

**Résultat attendu.** ~~Aucun supplément facturé, suspension ou quota changé par la seule alerte économique.~~

Preuve du 23 octobre 2026 : `rm2303-clone-preuves-completes.json` conserve les relevés immuables du responsable A1 avant/après. Budget interne synthétique 200 €, estimation portée à 201 € par commande normale et alerte constatée. Abonnement, quotas, crédit, demandes/factures et permissions du parcours organisateur sont identiques par API et navigateur ; aucun achat ni supplément facturé. Clone isolé uniquement, sans déploiement sur TEST partagé.

## F24 — Export complet et fermeture accompagnée

**Objet.** Récupérer les données transmissibles et quitter le service sans abandonner les engagements en cours ni fermer les accès à d’autres organisations.

**Accès.** Animation → **Compte et équipe** → export/fermeture ; ERP → réversibilité. **US35 ; CA62.**

**Prérequis à vérifier**

- [ ] Organisation de test dédiée, responsable et collaborateur ; ce responsable possède aussi un accès à B.
- [ ] Worker d’export, stockage privé, calendrier et notification opérationnels ; médias transmissibles et archive expirée préparés.
- [ ] Engagements ouverts connus : animation publiée, bon non consommé y compris expiré, dossier de préparation ; procédure opérateur pour leur résolution.

### RM-24-01

**Scénario.** Demander un export avec collaborateur puis responsable ; suivre sa préparation et sa disponibilité.

**Marche à suivre**

1. Préparer une organisation A dédiée à la sortie, son responsable et un collaborateur, avec calendrier, stockage privé, worker et notifications de test confirmés par le référent.
2. Comme collaborateur, ouvrir **Compte et équipe** et tenter la demande d’export ; si l’action est masquée, faire contrôler son refus direct par le référent.
3. Se connecter comme responsable A, ouvrir **Compte et équipe → Réversibilité** et demander l’export ; noter référence, date et état de préparation.
4. Lire les conditions : export inclus sans frais et cible de cinq jours ouvrés selon le calendrier ; vérifier qu’aucune demande de fermeture n’est créée.
5. Revenir au dossier après les traitements de préparation prévus, suivre son état puis vérifier la notification de disponibilité dans la boîte de test.
6. Ouvrir l’accès de téléchargement connecté et vérifier qu’il est privé ; consigner les dates réellement observées et la comparaison à la cible, sans déclarer le délai tenu avant disponibilité.

**Résultat attendu.** Responsable seul ; inclus sans frais, cible 5 jours ouvrés ; demande identifiée, notification de disponibilité sans archive publique ni fermeture automatique.

### RM-24-02

**Scénario.** Télécharger l’archive connecté ; ouvrir CSV, médias et guide ; comparer des références connues et les engagements en cours.

**Marche à suivre**

1. Avec le responsable de l’organisation dédiée, relever les références d’animations, commerçants, médias transmissibles et engagements ouverts à comparer, ainsi que la date de capture de l’export prêt.
2. Dans **Compte et équipe → Réversibilité**, télécharger l’archive en restant connecté ; la conserver dans l’espace privé de recette.
3. Ouvrir le guide et le manifeste, puis repérer les CSV et médias annoncés ; vérifier les explications des omissions et des liens entre identifiants.
4. Comparer les objets et engagements préparés à la date de capture, en distinguant les changements survenus après celle-ci ; vérifier que les médias transmissibles annoncés s’ouvrent.
5. Avec le référent, vérifier l’exclusion des données de B, notes et coûts internes, mots de passe, sessions et QR actifs, sans recopier de secrets dans le compte rendu.
6. Ouvrir le CSV contenant les cellules synthétiques à risque préparées pour la recette ; vérifier qu’elles restent du texte et qu’aucune formule ne s’exécute ; consigner les comparaisons sans joindre l’archive privée au rapport partagé.

**Résultat attendu.** Archive cohérente avec la date de capture, IDs/liens explicables, omissions motivées ; aucune donnée de B, note/coût interne, mot de passe, session ou QR actif. CSV sans formule exécutée à l’ouverture.

### RM-24-03

**Scénario.** **Accompagné :** interrompre/reprendre la génération, tenter téléchargement sans rôle puis après 30 jours de disponibilité ; consulter les données sources.

**Marche à suivre**

1. Faire préparer au référent un export reprenable et un export dont les trente jours de disponibilité sont écoulés, avec données sources identifiées ; ne pas changer l’horloge partagée.
2. Comme responsable A, demander ou suivre le premier export ; faire interrompre de manière contrôlée son worker pendant la génération sur le dispositif de recette autorisé.
3. Recharger **Réversibilité** : vérifier qu’aucune archive partielle n’est annoncée complète, puis faire reprendre le même traitement et attendre sa disponibilité réelle.
4. Tenter le téléchargement avec un collaborateur et avec un ancien responsable dont le rôle a été retiré sur ce jeu ; vérifier que chaque accès est refusé, y compris depuis un lien déjà obtenu.
5. Comme responsable courant, tenter le téléchargement de l’archive arrivée à échéance ; vérifier le refus même si le lien a été conservé.
6. Faire confirmer par le référent l’état de purge des fichiers privés, puis consulter les données métier sources dans les écrans autorisés ; vérifier que la purge de l’archive ne les a pas supprimées hors de leurs règles propres.

**Résultat attendu.** Pas d’archive partielle annoncée ; accès contrôlé à chaque téléchargement et refus après échéance ; purge de l’archive sans suppression des données métier selon leurs règles propres.

### RM-24-04

**Scénario.** Demander séparément la fermeture comme responsable avec engagements ouverts ; tenter nouvel usage et fin des engagements existants.

**Marche à suivre**

1. Faire préparer une organisation dédiée avec animation publiée, bon non consommé, bon expiré encore prolongeable, préparation en cours et éventuel export disponible ; relever l’inventaire initial avec le référent.
2. Comme responsable A, ouvrir **Compte et équipe → Réversibilité** et demander explicitement la fermeture, séparément de toute demande d’export.
3. Tenter un nouvel usage dans le portail, par exemple une nouvelle publication préparée pour ce test ; vérifier son blocage lié à la fermeture demandée.
4. Consulter l’historique et effectuer une action strictement nécessaire à un engagement existant sur le jeu prévu ; vérifier que la continuité autorisée reste possible.
5. Avec l’opérateur habilité, ouvrir **ERP → Fermeture des organisations** et comparer l’inventaire à la liste préparée, y compris bon expiré et export disponible.
6. Tenter la confirmation tant qu’un engagement reste non résolu ; vérifier le refus et sa raison, sans disparition artificielle de l’engagement ni fermeture anticipée des accès.

**Résultat attendu.** Nouveaux usages bloqués ; historique et actions strictement nécessaires préservés ; inventaire complet, fermeture effective bloquée tant que des obligations restent non résolues.

### RM-24-05

**Scénario.** Résoudre les engagements ou effectuer une reprise explicitement supportée et acceptée ; faire confirmer la fermeture par Localeo.

**Marche à suivre**

1. Comme opérateur habilité, ouvrir le dossier de l’organisation dédiée dans **ERP → Fermeture des organisations** et relire tous les engagements, exports compris.
2. Avec le responsable, déterminer pour chaque ligne la résolution effective par son parcours métier ; ne retenir une reprise que si elle dispose d’une commande réellement supportée.
3. Pour une préparation reprenable, faire accepter personnellement la reprise par l’intervenant nominatif habilité ; vérifier le résultat dans le dossier, sans appliquer ce mécanisme à un gain, bon ou paiement non transférable.
4. Terminer ou annuler les autres engagements selon leurs règles ; s’ils ne sont pas résolus, maintenir la continuité nécessaire et constater que la fermeture reste bloquée.
5. Une fois l’inventaire résolu, faire confirmer la fermeture par l’opérateur Localeo et lire la date effective ainsi que les informations de conservation communiquées au responsable.
6. Avec ce même responsable, tenter l’accès à A puis sélectionner B : vérifier les accès A fermés, y compris depuis une session ancienne, et les accès B conservés ; consigner les références de résolution et de fermeture.

**Résultat attendu.** Pas de transfert fictif : seules les reprises réellement exécutables sont proposées ; sinon continuité jusqu’à résolution. Date et conservation communiquées, accès A fermés, accès B conservés.


La reprise interne disponible pour une préparation ne prouve pas qu’un gain, un bon ou une obligation financière puisse être transféré. Un bon expiré mais encore prolongeable ne doit pas disparaître artificiellement de l’inventaire. Vérifier également les exports encore disponibles avant confirmation de la fermeture, selon les contrôles du dossier.

## F25 — Reprise de l’existant, démonstration et ouverture du pilote

**Objet.** Passer à la nouvelle offre sans perte d’engagements et prouver que le service peut être exploité et restauré avant son ouverture.

**Accès.** ERP → revue des périmètres communaux ; parcours des applications ; outils d’exploitation avec l’équipe technique. **US36–38 ; CA26–28, 63.**

**Prérequis à vérifier**

- [ ] Inventaire de commerces historiques et engagements, dont un commerce non revu ; compte opérateur autorisé.
- [ ] Manifestes de versions/configuration, jeux de démonstration et preuves locales consultables ; cible isolée pour restauration.
- [ ] Plan pilote Martignas-sur-Jalle et responsables de validation Localeo/commune ; accord spécifique avant toute opération réelle d’environnement.

### RM-25-01

**Scénario.** Examiner les commerces existants, saisir manuellement leurs périmètres puis tenter la bascule avec un commerce non revu ; terminer la revue.

**Marche à suivre**

1. Avec un opérateur ERP habilité, ouvrir la revue des périmètres communaux du jeu dédié ; comparer les commerces historiques et leurs engagements à l’inventaire préparé.
2. Examiner les faits de chaque commerce et saisir manuellement la décision Animation, Coffrets ou les deux selon le dossier ; laisser volontairement un commerce non revu.
3. Vérifier qu’aucune suggestion ou activation automatique des deux périmètres n’a remplacé la décision humaine et que les décisions saisies conservent leur auteur.
4. Sur le dispositif de recette prévu, tenter la bascule de la commune avec ce commerce non revu ; vérifier le refus et l’identification de la revue manquante.
5. Avant la bascule, reprendre un parcours historique sur le commerce non revu et consulter ses engagements ; vérifier qu’aucun droit antérieur n’a été retiré silencieusement.
6. Terminer sa revue manuelle et relire l’éligibilité de la commune ; consigner la décision et les engagements conservés, sans déduire de ce contrôle une autorisation de basculer un environnement réel.

**Résultat attendu.** Pas de proposition/activation automatique Animation+Coffrets ; commerce non revu bloque la bascule concernée. Avant bascule, fonctionnement historique préservé sans retrait silencieux.

### RM-25-02

**Scénario.** **Accompagné :** pendant la vérification de bascule, créer/déplacer un commerce puis relire l’éligibilité.

**Marche à suivre**

1. Faire préparer par le référent une commune de recette dont les commerces ont été revus, un opérateur de revue et un second acteur autorisé à créer ou déplacer un commerce.
2. Avec le premier opérateur, ouvrir la vérification de bascule et relever les commerces considérés éligibles, en laissant cette vue ouverte.
3. Dans la seconde session, créer un nouveau commerce dans cette commune ; revenir à la vérification initiale et tenter sa confirmation sur le dispositif de recette.
4. Vérifier que le contrôle courant détecte le nouvel objet ou impose une relecture, et qu’il n’autorise pas la bascule en ignorant ce commerce.
5. Refaire sur un jeu distinct avec le déplacement d’un commerce vers la commune ; vérifier le même contrôle et terminer la revue nécessaire.
6. Relire les décisions et engagements antérieurs dans l’ERP ; vérifier leur traçabilité et leur conservation, puis consigner séparément création et déplacement, sans bascule réelle implicite.

**Résultat attendu.** Impossible de basculer en oubliant le nouvel objet ; contrôle courant et décision tracée. Engagements antérieurs toujours identifiables.

### RM-25-03

**Scénario.** **Accompagné :** générer un jeu synthétique puis le sauvegarder/restaurer sur cible isolée ; reprendre des parcours QR/PIN, import et permissions.

**Marche à suivre**

1. Faire vérifier par le référent l’accord spécifique d’exercice, la cible isolée, le profil de génération synthétique et le stockage privé des fichiers ; à défaut, classer l’exercice Bloqué sans génération ni restauration.
2. Faire générer le jeu par l’outil prévu sur cette cible et noter son manifeste ; comparer ses périmètres, modules et rôles à des objets équivalents créés par interface.
3. Avec les comptes commerçant, salarié, organisateur et participant du jeu, relever les résultats initiaux d’une validation QR, d’une validation PIN, d’un import et de refus de permissions.
4. Faire sauvegarder puis restaurer ce jeu sur la cible isolée selon la procédure d’exploitation, avec ses fichiers et configuration ; conserver les preuves techniques privées et les références non secrètes du rapport.
5. Après les contrôles de reprise, se reconnecter et reprendre les mêmes parcours sur les objets prévus, avec les accès réémis par les parcours normaux lorsque requis.
6. Comparer données, fichiers, résultats et refus : le générateur n’a accordé aucun privilège ni activation forcée, et la restauration conserve les règles ; distinguer cet exercice synthétique d’une preuve de capacité hébergée.

**Résultat attendu.** Mêmes règles et refus que pour les données créées par interface ; pas de privilèges ou activation forcée par le générateur ; parcours et fichiers cohérents après restauration.

### RM-25-04

**Scénario.** Faire examiner le manifeste, les résultats des recettes et les anomalies ; faire valider l’UX par Localeo puis Martignas-sur-Jalle.

**Marche à suivre**

1. Rassembler le manifeste des versions réellement visées, les résultats de chaque recette et variante, les anomalies ouvertes et les limites de performance/restauration.
2. Avec les responsables Localeo, examiner les parcours, les éléments Bloqués ou non exécutés et les preuves liées aux critères d’acceptation ; noter le périmètre évalué.
3. Faire réaliser la validation UX interne Localeo sur les parcours prévus, notamment mobile, inscription, Live et gestion ; consigner son avis et les réserves.
4. Après cette étape, présenter les parcours et réserves à Martignas-sur-Jalle pour la validation de la commune pilote ; enregistrer son avis distinct.
5. Faire consigner une décision pilote explicite avec responsables, périmètre et conditions restantes ; ne pas transformer un build réussi en accord d’ouverture.
6. Inscrire l’extension progressive comme décision ultérieure dépendant du bilan du pilote ; conserver la séparation entre cette recette, l’autorisation de livraison et toute exécution de déploiement.

**Résultat attendu.** Décision pilote explicite ; aucun déploiement ni généralisation déduit d’un simple build vert. Extension progressive uniquement après bilan du pilote.

### RM-25-05

**Scénario.** **Accompagné technique, sur cible isolée représentative :** restaurer base/fichiers/configuration et reprendre accès, participation, validation et remise ; chronométrer jusqu’aux contrôles terminés.

**Marche à suivre**

1. Faire confirmer par le référent l’accord spécifique d’exercice, la cible isolée représentative, les sauvegardes base/fichiers/configuration et le journal indépendant des suppressions/révocations ; sinon maintenir le test Bloqué.
2. Relever avant exercice le dernier point métier durable, les objets à retrouver, les accès révoqués et les suppressions dues ; préparer les parcours accès, participation, validation et remise et leurs comptes de test.
3. Faire isoler les écritures HTTP, ordonnanceur et workers, maintenir la réouverture bloquée et démarrer le chronométrage selon le protocole d’exercice.
4. Faire restaurer base, fichiers et configuration puis appliquer la procédure de reprise : journal indépendant, suppressions, révocations, fermeture des anciennes capacités et contrôles avant réouverture.
5. Après autorisation technique de poursuivre les contrôles, se reconnecter par les parcours normaux et tester participation, validation et remise ; vérifier les données, droits et traitements ainsi que le refus des accès révoqués et des anciens QR/PIN concernés.
6. Arrêter le chronométrage seulement après les contrôles terminés ; calculer la perte réellement mesurée et le temps total de reprise, puis comparer aux maxima de 4 h et 8 h.
7. Faire établir une preuve datée précisant cible, volumes, sauvegardes, résultats et limites ; vérifier sa disponibilité avant mise en service, puis la planification trimestrielle et après changement majeur, sans présenter une simulation locale comme preuve hébergée.

**Résultat attendu.** Perte maximale mesurée **4 h**, reprise **8 h**, contrôles compris ; données, droits et traitements cohérents, suppressions dues réappliquées, accès révoqués non réactivés. Preuve datée requise avant mise en service, chaque trimestre et après changement majeur.

### RM-25-06

**Scénario.** Examiner un dossier sans preuve de restauration ou dont un objectif échoue.

**Marche à suivre**

1. Préparer avec le responsable d’exploitation deux dossiers d’exercice : l’un sans preuve de restauration et l’autre avec perte supérieure à 4 h ou reprise supérieure à 8 h ; les identifier comme dossiers de recette.
2. Examiner pour chacun les dates, cible, périmètre, sauvegardes et résultats disponibles ; distinguer preuve manquante et objectif effectivement échoué.
3. Soumettre chaque dossier à la revue de mise en service prévue et relever la décision pour le périmètre concerné.
4. Vérifier que l’ouverture reste bloquée, même si builds, tests locaux ou simulation de restauration sont réussis.
5. Consigner la correction attendue, son responsable et la preuve hébergée à produire avant réexamen ; ne pas déclarer la réserve levée sur la seule promesse d’un exercice futur.

**Résultat attendu.** Mise en service concernée bloquée jusqu’à correction/preuve ; une simulation locale seule ne vaut pas démonstration hébergée.


## Contrôles métier transverses à répéter dans les parcours

### RM-X-01 — Navigation

**Scénario.** Sur téléphone étroit puis ordinateur, parcourir les fonctions autorisées du portail ; côté interne, vérifier menus et retour accueil ERP ; côté public, découverte et participation.

**Marche à suivre**

1. Préparer un téléphone à écran étroit et un ordinateur, les mêmes versions de recette, un compte organisateur A1, un opérateur ERP et un participant synthétique.
2. Sur téléphone, connecter l’organisateur et parcourir les fonctions autorisées : listes, fiche d’animation, compte et retour ; vérifier que l’organisation et la commune actives restent identifiables.
3. Dans chaque écran, trouver l’action principale et le retour sans devoir deviner une zone masquée ; relever tout débordement qui empêche de lire ou d’agir.
4. Avec l’opérateur interne, parcourir les menus concernés et revenir à l’accueil ERP ; vérifier la cohérence des accès et du contexte.
5. Comme participant, parcourir découverte, fiche et inscription sur le site public ; vérifier que les contenus de communication se distinguent clairement de la gestion organisateur.
6. Refaire les mêmes parcours sur ordinateur et comparer ; consigner appareil, dimensions utiles et écran de toute action rendue inaccessible.

**Résultat attendu.** Portail avec codes d’application de gestion, site public avec codes de communication ; contexte organisation/commune visible, retour et action principale identifiables ; aucune fonction importante rendue inaccessible par débordement.

### RM-X-02 — Accessibilité

**Scénario.** Tester clavier seul, focus, zoom 200 %, erreurs de formulaire et états des lots sans s’appuyer uniquement sur leur couleur.

**Marche à suivre**

1. Préparer les comptes et écrans représentatifs : connexion, formulaire d’animation, support, lecture de lot et validation d’un bon ; disposer d’états succès, refus et déjà traité.
2. Sans souris, parcourir les éléments avec Tab et Maj+Tab, puis activer les commandes au clavier ; vérifier un ordre compréhensible et un focus toujours repérable.
3. Soumettre un formulaire avec un champ obligatoire manquant ou une valeur invalide ; vérifier que le champ et le message sont identifiables et que la correction est possible au clavier.
4. Régler le zoom à 200 % et refaire les actions principales ; vérifier que textes, champs, messages et boutons restent accessibles et non masqués.
5. Comparer les états du lot ou bon sans s’appuyer sur leur couleur : vérifier la présence de textes ou indications compréhensibles pour succès, refus et déjà traité.
6. Consigner les écrans, actions et obstacles observés ; qualifier ce résultat de recette UX ciblée, sans le présenter comme une certification complète d’accessibilité.

**Résultat attendu.** Libellés, ordre de lecture et messages compréhensibles ; focus utilisable, texte non masqué ; succès/refus/déjà traité distinguables. Recette UX ciblée, pas certification d’accessibilité complète.

### RM-X-03 — Dates

**Scénario.** Depuis un appareil configuré hors France, lire échéances de bons, campagnes, factures et délais de service ; inclure un changement d’heure.

**Marche à suivre**

1. Faire préparer par le référent des échéances de bons, campagnes, factures et délais de service autour d’un changement d’heure Paris, avec leurs valeurs attendues et le calendrier ouvré.
2. Régler uniquement le fuseau de l’appareil de recette hors France, sans changer l’horloge de l’environnement ; relever ce fuseau dans le compte rendu.
3. Comme participant puis organisateur, lire les bons dans Live et les campagnes dans Animation ; comparer les dates/heures affichées aux références Europe/Paris.
4. Avec le compte habilité, lire factures et échéances de support/export ; vérifier que les dates civiles restent le jour prévu sans décalage accidentel.
5. Comparer les cas avant/après changement d’heure et recalculer les jours ouvrés avec les horaires et fermetures préparés ; vérifier que le changement de fuseau de l’appareil n’a pas modifié l’échéance métier.
6. Refaire une lecture depuis un appareil en Europe/Paris, comparer et consigner chaque famille de dates et toute ambiguïté d’affichage.

**Résultat attendu.** Dates/horaires métier affichés en Europe/Paris, échéances compréhensibles ; dates civiles sans décalage accidentel. Le calcul des jours ouvrés suit le calendrier de service.

### RM-X-04 — Reprise et historique

**Scénario.** Dans chaque action à effet, recharger après confirmation ; sur les jeux accompagnés, couper la réponse puis relire l’état ; ouvrir l’historique.

**Marche à suivre**

1. Préparer une opération de chaque famille à effet dans son application : paiement de test, attribution de gain, message et consommation de bon ; noter acteurs et références initiales.
2. Avec le compte autorisé pour chaque opération, effectuer l’action une fois et attendre sa confirmation ; relever sa référence sans secret.
3. Recharger puis rouvrir l’objet depuis la liste ou l’historique ; vérifier l’état réel et l’unicité du paiement, gain, message ou consommation.
4. Pour chaque variante accompagnée, faire préparer au référent une perte de réponse contrôlée sur un jeu distinct, puis consulter le résultat ou reprendre la même opération par le mécanisme prévu.
5. Vérifier après reprise qu’un seul effet existe et qu’un état en cours n’a pas été présenté à tort comme un succès définitif.
6. Ouvrir l’historique autorisé et contrôler auteur, date, motif et référence d’opération selon l’action ; consigner chaque famille séparément, en retirant QR utilisables, PIN et autres secrets des preuves.

**Résultat attendu.** Pas de double paiement/gain/message/consommation ; état réel consultable, auteur/date/motif et référence d’opération présents selon l’action. Aucun secret dans les captures ou exports de preuve.

### RM-X-05 — Isolation

**Scénario.** Avec un lecteur puis un compte A, ouvrir un lien mémorisé vers écriture ou objet B ; retirer un droit pendant une session.

**Marche à suivre**

1. Préparer un lecteur A1, un gestionnaire A1, un objet de B et des liens privés de recette vers écriture et objet étranger ; relever les droits initiaux avec le responsable.
2. Comme lecteur A1, vérifier les actions proposées puis ouvrir directement le lien d’écriture ; vérifier que le refus est effectif et qu’aucune modification n’est enregistrée.
3. Comme compte A sans appartenance B, ouvrir le lien de l’objet B ; vérifier le refus sans divulgation de données étrangères dans la page ou l’erreur.
4. Avec le gestionnaire autorisé, laisser ouverte une page d’action ; dans une autre session, faire retirer par le responsable le droit nécessaire à cette action.
5. Depuis la session restée ouverte, tenter l’action puis recharger et reprendre le lien mémorisé ; vérifier le refus malgré l’ancien contexte affiché.
6. Relire les objets avec un acteur encore autorisé pour confirmer l’absence d’effet et consigner séparément lecture seule, isolation B et retrait de droit en session.

**Résultat attendu.** Masquage cohérent avec refus effectif ; pas d’accès par lien direct, ancien contexte ou session ouverte, ni divulgation de données étrangères dans l’erreur.

### RM-X-06 — Volumétrie

**Scénario.** **Accompagné :** jeu de 10 communes et 10 000 participants au total ; 10 utilisateurs actifs simultanés. Paginer, filtrer, changer de commune, consulter bilan et poursuivre validation pendant import/campagne. Comparer au jeu réduit, mêmes actions.

**Marche à suivre**

1. Faire préparer par le référent un jeu stabilisé de 10 communes et 10 000 participants au total, un jeu réduit comparable et dix comptes actifs simultanément ; noter environnement, versions et budgets de mesure issus de l’architecture.
2. Sur le jeu réduit, effectuer le parcours de référence : paginer une liste, filtrer, changer de commune, ouvrir un bilan et valider un objet ; relever durées, erreurs et références retournées.
3. Répartir les dix utilisateurs sur les mêmes actions du grand jeu, avec une cadence convenue et notée ; ne pas assimiler dix utilisateurs à dix requêtes par seconde.
4. Sur une liste stabilisée, parcourir les pages puis appliquer les filtres et changer de commune ; comparer les références aux attendus pour détecter doublons, omissions et perte de contexte.
5. Pendant qu’un opérateur lance l’import ou la campagne synthétique prévu, poursuivre bilans et validations ; relever durées et erreurs ainsi que la progression du traitement long.
6. Faire tester sa reprise contrôlée par le référent et vérifier que progression, résultats et parcours interactifs restent cohérents, sans duplication d’effet.
7. Comparer au jeu réduit et aux budgets retenus ; joindre les preuves techniques de pagination, requêtes et charge de la matrice de performance, et conserver les limites historiques dans le bilan sans conclure à une garantie générale de charge.

**Résultat attendu.** Pages navigables sans doublons/omissions sur un jeu stabilisé ; filtres/contexte conservés ; traitements longs avec progression et reprise, sans blocage du parcours interactif. Relever durées et erreurs, comparer aux budgets de l’architecture. Aucune garantie de charge déduite d’un ressenti ou d’une seule exécution.


La recette métier ne démontre pas à elle seule l’usage d’index ou l’absence de chargement d’une table complète. Joindre pour RM-X-06 les preuves de pagination, requêtes et charge de la [matrice de performance](architecture-contrats.md). Les lectures historiques non migrées et limites enregistrées dans le suivi doivent rester visibles dans le bilan, sans généraliser la validation de quelques écrans à toute la plateforme.

## Complément du 30 octobre — accueil et rappels Live

Ces six parcours couvrent **E73-EVO-LIVE-ACCUEIL-RAPPELS** et ses
[critères complémentaires](localeo-live-entree-unique.md). Ils s'ajoutent aux
130 scénarios initiaux, sans changer leurs numéros ni leurs résultats.
**Statut : recette hébergée à exécuter.** Les tests automatisés locaux et leurs
limites sont dans le [suivi d'implémentation](suivi-implementation.md).

Prérequis propres au complément : migration v284, backend et Live compatibles,
deux participations distinctes à une même animation dans un carnet de recette,
un parcours presque terminé, un autre incomplet finissant dans les 72 heures et
un parcours terminé. Préparer ces états par les services ordinaires. Pour les
rappels, utiliser uniquement un appareil du recetteur, HTTPS et le fournisseur
de test prévu par le [guide d'exploitation](../../exploitation/exploitation/parcours-plateforme-animation.md).
Une préférence activée ne prouve ni la permission navigateur ni la réception.

| Test | Actions de recette | Résultat attendu / critères |
| --- | --- | --- |
| RM-LIVE-HOME-01 | Ouvrir Live sans carnet puis avec les participations préparées ; consulter la priorité principale, les suivantes et la découverte. Comparer progression et échéance aux participations. | Découverte conservée ; indicateurs réels, parcours terminé sans urgence ni gain inventé. E73-HOME-01/02. |
| RM-LIVE-HOME-02 | Ouvrir deux accès de la même animation depuis l'accueil ; retirer seulement l'un des accès locaux puis rouvrir son lien. Actualiser les anciens suivis avec leurs tokens existants. | Bonne participation à chaque ouverture ; accès absent sans substitution, refus visible et carnet conservé. E73-HOME-04/05. |
| RM-LIVE-HOME-03 | Sur mobile 320/390 px, utiliser texte agrandi et clavier ; avec plus de 50 suivis, changer de page puis actualiser pendant un chargement. | Actions utilisables, page remplacée et vue partielle annoncée, ancienne réponse ignorée. E73-HOME-03/06. |
| RM-LIVE-RAPPEL-01 | Ouvrir Réglages sur installation nouvelle puis existante ; activer une seule préférence, recharger, changer l'autre puis retirer les deux. | Deux choix initialement désactivés, indépendants et mémorisés ; autres catégories/communes conservées, aucun blocage si Push refusé. E73-ALERTE-01. |
| RM-LIVE-RAPPEL-02 | Avec consentement et abonnement du recetteur, préparer un parcours à une étape restante et une échéance proche ; simuler puis effectuer le traitement autorisé pendant 09–20 h Paris. Ouvrir le rappel. | Simulation sans rappel créé ; motifs regroupés, échéance lisible, bonne participation ouverte. Plusieurs participations ouvrent Mes participations. E73-ALERTE-02/05. |
| RM-LIVE-RAPPEL-03 | Avec le référent, retirer le consentement ou achever le parcours avant transport ; rejouer les traitements et purger l'inbox. Vérifier séparément hors créneau et après échéance sur une cible isolée. | Aucun envoi devenu interdit ; pas de réarmement après purge, un rappel logique par jour et chaque type une fois par participation. Ne pas avancer l'horloge du TEST partagé. E73-ALERTE-03/04. |

Enregistrer version, appareil, heure de Paris, identifiants sans secrets,
préparation, tentative fournisseur et réception comme résultats distincts.
L'absence d'un prérequis n'est pas une validation du parcours.

## Traçabilité et décision de recette

| Fiche | US E73 | CA E73 principalement exercés |
| --- | --- | --- |
| F01 | 25 | 50–51 |
| F02 | 26 | 52–53 |
| F03 | 11 | 15, 17, 22 |
| F04 | 12 | 16–18 |
| F05 | 11, 13 | 19–22 |
| F06 | 03, 14 | 12–14, 37 |
| F07 | 15, 27–28 | 38, 54–55 |
| F08 | 16–17 | 39–41 |
| F09 | 01–02, 29 | 01–05, 11, 56 |
| F10 | 04 | 06, 08–10, 29 |
| F11 | 05–06 | 30–31, 33 |
| F12 | 07–08 | 06–10, 32–33 |
| F13 | 09 | 21, 34–35 |
| F14 | 10 | 33, 36 |
| F15 | 18, 30 | 46, 57 |
| F16 | 19–20 | 42–45 |
| F17 | 21–22 | 47–49 |
| F18 | 23 | 23–24 |
| F19 | 31 | 58 |
| F20 | 32 | 59 |
| F21 | 33 | 60 |
| F22 | 24 | 25 |
| F23 | 34 | 61 |
| F24 | 35 | 62 |
| F25 | 36–38 | 26–28, 63 |

Une fiche est validée lorsque ses prérequis sont établis, ses scénarios applicables et leurs variantes sont réussis, et ses preuves sont enregistrées. Un cas non testable faute de configuration ou de jeu reste **Bloqué** avec un responsable et une action de préparation. Un menu absent est à qualifier : version, droit, périmètre et module d’abord ; ne pas déclarer la fonction validée ou hors périmètre par défaut.

Sont bloquants pour la fonctionnalité concernée : accès à une autre organisation/commune, perte ou écrasement de données, double remise/attribution/paiement, droit non acquis accordé, contournement d’une suspension, notification à un destinataire non autorisé, publication sans prérequis ou absence de résultat fiable après reprise. Les autres anomalies sont qualifiées par Localeo avec impact, priorité et décision explicite ; elles ne disparaissent pas du compte rendu parce qu’un autre parcours réussit.

L’acceptation d’un CA combine cette recette et les preuves techniques de la matrice existante. **CA28 et CA63 restent conditionnés aux validations de pilote et d’exploitation** ; ce plan ne change pas le statut de l’epic en « terminée ».

### Modèle de compte rendu à remplir après exécution

| Test / variante | Date / recetteur | Versions / environnement | Compte, commune et objets | Observé | Statut | Preuve / anomalie |
| --- | --- | --- | --- | --- | --- | --- |
| RM-… | À renseigner | À renseigner | Références sans secrets | À renseigner | À exécuter | À renseigner |

Pour la décision finale, joindre le nombre de tests validés/échoués/bloqués/non exécutés, la liste des anomalies restantes, les limites de charge/restauration, l’avis Localeo, l’avis de Martignas-sur-Jalle et le périmètre exact accepté. **La recette n’exécute ni n’autorise, à elle seule, un commit, un push ou une livraison.**
