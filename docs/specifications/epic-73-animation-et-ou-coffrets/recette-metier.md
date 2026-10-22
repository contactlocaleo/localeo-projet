# E73 — Plan de recette métier par fonctionnalité

Plan préparé le **22 octobre 2026**. **Tous les scénarios ci-dessous sont à exécuter** : ce document ne constitue ni un procès-verbal de recette, ni une autorisation de déploiement. Il couvre les **38 US et 63 critères d’acceptation** de l’epic, en **25 fiches fonctionnelles**.

Le résultat recherché est de vendre et exploiter **Animation et/ou Coffrets**, avec une expérience compréhensible pour l’organisateur, le commerçant, le salarié et le participant. Pour chaque fonctionnalité : lire l’objet, vérifier tous les prérequis, suivre les actions et comparer le résultat obtenu au résultat attendu.

Références : [spécification](README.md), [backlog et arbitrages](../../roadmap/en-cours/epic-73-animation-et-ou-coffrets-backlog.md), [matrice technique des 63 CA](verification-livraison.md), [accès par lot](prise-en-main-par-lot.md), [preuves d’implémentation et limites](suivi-implementation.md). Les CA mentionnés dans les fiches sont les identifiants `E73-CA-*` existants ; les identifiants `RM-*` servent au suivi de cette recette.

## Préparer la campagne de recette

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

## F01 — Connexion et récupération du compte organisateur

**Objet.** Permettre au membre de l’équipe de retrouver son accès sans créer de doublon ni maintenir une ancienne session après changement de mot de passe.

**Accès.** Connexion du portail Animation → mot de passe oublié ; compte connecté → gestion du mot de passe. **US25 ; CA50–51.**

**Prérequis à vérifier**

- [ ] Un compte organisateur actif, sa boîte email et deux sessions ouvertes sur des navigateurs distincts.
- [ ] Un autre compte indépendant et des liens de réinitialisation valides/expirés préparés sans exposer leurs secrets.
- [ ] L’envoi des emails et l’URL de retour vers le portail fonctionnent.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-01-01 | Demander une récupération avec l’email connu puis une adresse inconnue. | Même réponse publique, sans révéler les comptes existants. Le compte connu reçoit un lien utilisable ; aucun nouveau compte n’est créé. |
| RM-01-02 | Utiliser un lien valide, définir le nouveau mot de passe, puis réutiliser le lien et tenter l’ancien mot de passe. | Première utilisation réussie, suivantes refusées ; reconnexion avec le nouveau mot de passe. Anciennes sessions du compte invalidées, autre compte inchangé. |
| RM-01-03 | **Accompagné :** tester le lien avant puis à/après son échéance d’une heure. | Lien utilisable seulement avant expiration ; nouveau lien demandé par le parcours normal, sans perte de l’appartenance. |
| RM-01-04 | Changer le mot de passe connecté : d’abord avec une preuve d’identité erronée, puis correcte. | Aucun changement sur refus ; succès explicite ensuite et reconnexion requise sur les anciennes sessions du seul compte concerné. |

## F02 — Organisation, équipe et délégations

**Objet.** Donner à chaque collaborateur les seules communes et actions qui lui sont confiées, avec un responsable identifiable et une récupération assistée.

**Accès.** Animation → **Compte et équipe** ; ERP → **Accès Animation**. **US26 ; CA52–53.**

**Prérequis à vérifier**

- [ ] Organisations A/B, communes A1/A2/B1 et comptes responsable, gestionnaire, lecteur et multi-organisations disponibles.
- [ ] Un opérateur ERP habilité peut examiner une demande de rattachement ; emails d’invitation opérationnels.
- [ ] Une tâche programmée non commencée est affectée à un collaborateur révocable.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-02-01 | Déposer une demande d’organisation/communes, tenter d’utiliser A1 avant décision, puis faire valider le rattachement par Localeo. | La demande seule n’ouvre aucun droit ; seuls les rattachements validés deviennent accessibles. |
| RM-02-02 | Inviter un nouveau collaborateur Gestionnaire sur A1 ; accepter ; comparer à un Lecteur et à un Gestionnaire sans Achat/Import/Communication. | Rôle et commune exacts, lecteur sans écriture ; les permissions complémentaires ne viennent pas automatiquement avec le rôle ou l’achat d’un module. |
| RM-02-03 | Inviter un email déjà associé à un compte, accepter avec ce compte ; renvoyer une autre invitation et essayer l’ancien lien ; essayer un lien expiré de 7 jours. | Compte existant réutilisé après acceptation ; autres appartenances préservées ; ancien lien remplacé et lien expiré refusés. |
| RM-02-04 | Retirer une autorisation avec la session du collaborateur ouverte ; ajouter A2 à l’organisation sans l’ajouter au collaborateur ; tenter un lien direct hors droit. | Refus dès la prochaine requête ; A2 non accordée implicitement ; tâches non commencées nécessitant le droit suspendues. Les traitements déjà engagés suivent leur continuité contrôlée, sans redonner la main au compte révoqué. |
| RM-02-05 | Proposer un transfert de responsabilité ; tenter le départ du dernier responsable avant acceptation ; faire accepter le successeur actif. | Ancien responsable maintenu avant acceptation, départ bloqué ; transfert tracé après acceptation, aucune organisation sans responsable. |
| RM-02-06 | **Accompagné :** simuler la perte des accès responsables et demander une récupération ; changer ensuite d’organisation avec le compte multi-organisations. | Localeo vérifie l’autorité du demandeur et trace la réattribution ; aucune organisation doublonnée, aucun objet de l’ancien contexte affiché comme appartenant au nouveau. |

## F03 — Activation des périmètres commerçants depuis l’ERP

**Objet.** Choisir Animation, Coffrets ou les deux pour chaque commerce, sans lui ouvrir des fonctions dont les prérequis ne sont pas satisfaits.

**Accès.** ERP → fiche commerçant → périmètres. **US11 ; CA15, 17, 22 ; reprise historique en F25.**

**Prérequis à vérifier**

- [ ] Commerces distincts sans périmètre prêt, Animation seul et mixte ; leurs prérequis sont identifiés.
- [ ] Administrateur, Backoffice habilité et Backoffice non habilité disponibles ; compte commerçant ouvert en parallèle.
- [ ] Motifs et historique des changements consultables dans l’ERP.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-03-01 | Faire demander/activer Animation par l’administrateur puis par le Backoffice habilité ; refaire sans habilitation et depuis Pro. | Seuls les opérateurs ERP autorisés peuvent décider ; auteur et motif visibles. Le commerce ne s’active pas lui-même. |
| RM-03-02 | Ajouter Coffrets à un commerce Animation dont les compléments Coffrets sont incomplets ; terminer les prérequis puis activer. | Coffrets reste en préparation jusqu’à validation ; Animation continue de fonctionner ; le diagnostic indique les compléments attendus. |
| RM-03-03 | **Accompagné :** deux opérateurs modifient la même fiche depuis des versions ouvertes avant la première modification. | Le second ne remplace pas silencieusement la première décision ; conflit/relecture explicite, historique cohérent. |

## F04 — Onboarding adapté au produit

**Objet.** Accueillir un commerce Animation sans lui imposer les prestations et pièces propres aux Coffrets, puis demander les compléments utiles s’il ajoute ce produit.

**Accès.** OnBoard → dossier commerçant ; Pro → préparation du dossier lorsque proposée. **US12 ; CA16–18.**

**Prérequis à vérifier**

- [ ] Un dossier Animation seul et un dossier mixte, avec pièces synthétiques et conventions appropriées.
- [ ] Accès opérateur OnBoard et responsable du commerce ; boîtes de réception de test.
- [ ] Les modèles de communications/conventions correspondant aux périmètres sont disponibles.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-04-01 | Compléter identité, responsable, coordonnées et engagements Animation, sans prestations ni pièces bancaires Coffrets. | Dossier Animation recevable lorsque ses propres prérequis sont remplis ; aucun blocage bancaire/Coffrets artificiel. |
| RM-04-02 | Omettre un prérequis Animation puis tenter l’activation ; le compléter et faire vérifier le dossier. | Manque compréhensible et action de correction accessible ; validation effective requise avant ouverture. |
| RM-04-03 | Demander ensuite Coffrets, y compris sur un dossier déjà clos ; vérifier les données et compléter les pièces propres au nouveau produit. | Données communes réutilisées, compléments ciblés ; pas de remise à zéro du dossier ni d’interruption d’Animation. |
| RM-04-04 | Préparer/envoyer les communications et conventions d’un dossier Animation seul puis mixte ; consulter leur suivi. | Contenu adapté aux produits, couverture des conventions explicite ; un échec d’envoi n’apparaît pas comme un succès et le suivi reste conservé. |

## F05 — Localeo Pro : fonctions utiles et continuité des engagements

**Objet.** Présenter au commerçant et au salarié uniquement les actions autorisées, tout en permettant d’honorer les engagements antérieurs à un retrait commercial.

**Accès.** Pro → compte commerçant/salarié, scan et historique ; ERP pour retrait/suspension. **US11, US13 ; CA19–22.**

**Prérequis à vérifier**

- [ ] Comptes Animation seul, Coffrets seul, mixte et salarié actif ; invitations salariés déjà initialisées.
- [ ] Animation publiée avec participation acceptée, bon déjà attribué et coffret vendu avec prestation engagée.
- [ ] Jeux distincts pour retrait de périmètre et suspension administrative ; sessions Pro ouvertes avant les changements.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-05-01 | Ouvrir Pro avec chacun des trois périmètres ; parcourir menus et liens directs vers les fonctions absentes. | Navigation adaptée, sans fonctions étrangères ; liens directs également refusés. Compte, aide, préparation et historique autorisés restent accessibles. |
| RM-05-02 | Connecter le salarié et scanner ; tenter administration, finances, gestion de droits et action d’un autre commerce. | Accès direct au scan, historique selon ses droits, aucune élévation de privilèges. Le salarié reste limité à son commerce. |
| RM-05-03 | Faire participer un commerce Animation seul à une animation dotée en coffrets et valider un passage. | Passage autorisé par sa participation ; le commerce ne devient pas fournisseur de prestations Coffrets. |
| RM-05-04 | Retirer Animation pendant une session ouverte ; tenter un nouvel engagement, un passage d’une participation déjà acceptée à une animation publiée et une remise de bon déjà attribué. | Nouvel engagement refusé immédiatement côté serveur ; seules les continuités prévues fonctionnent jusqu’à leurs limites. Aucun droit nouveau déduit de la session. |
| RM-05-05 | Retirer Coffrets avec une prestation déjà engagée dans un coffret vendu ; consulter règlement et historique, puis tenter un nouvel engagement. | Prestation antérieure et consultation autorisée préservées selon validité et habilitations ; nouvel engagement refusé. |
| RM-05-06 | Suspendre administrativement le commerce d’un jeu de continuité puis retenter QR/PIN. | La suspension prime sur les droits résiduels ; aucune remise ou validation n’est autorisée grâce à l’exception commerciale. |

## F06 — Catalogue : forfaits, modules et conditions acquises

**Objet.** Rendre lisible ce qui est inclus, optionnel ou déjà acquis, sans changer rétroactivement les droits d’un client.

**Accès.** Animation → **Abonnement** ; ERP → catalogue/modules. **US03, US14 ; CA12–14, 37.**

**Prérequis à vérifier**

- [ ] Catalogue initial chargé et souscriptions antérieure/nouvelle disponibles.
- [ ] Une organisation avec deux communes et un module accordé à A1 seulement.
- [ ] Administrateur catalogue et opérateur non administrateur.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-06-01 | Consulter forfait et modules d’une nouvelle souscription ; ouvrir les variantes de scénarios. | Passeport/tombola inclus dans le quota du forfait ; chasse, import et communication optionnels. Variantes couvertes par le droit de leur type, pas d’achat supplémentaire par scénario. |
| RM-06-02 | Vérifier les offres initiales et leur récapitulatif. | Chasse : 190 € HT/an, 5 chasses, quota distinct ; import : 49 € HT/an, sans quota commercial ; messages : 49 € HT/an, 5 campagnes/mois. Commune, dates, prérequis, HT/TVA/TTC et capacités sont explicites. |
| RM-06-03 | Avec le module acquis sur A1, tenter l’usage sur A2 ; consulter un droit inclus sans achat. | Aucun droit automatiquement étendu à A2 ; le droit inclus valide fonctionne sans paiement fictif. Seuls les modules officiels Localeo sont proposés. |
| RM-06-04 | Modifier un prix/quota par l’administrateur ; consulter l’ancienne souscription puis préparer son renouvellement ; tenter la modification sans rôle administrateur. | Conditions acquises préservées jusqu’à échéance ; nouvelles conditions présentées au renouvellement pour confirmation ; modification non administrateur refusée. |

## F07 — Achat, renouvellement et facturation

**Objet.** Acheter et faire évoluer son offre avec un prix compréhensible, des droits accordés une seule fois et des remboursements contrôlés.

**Accès.** Animation → **Abonnement**, **Finance** ; ERP → souscriptions/remboursements. **US15, US27–28 ; CA38, 54–55.**

**Prérequis à vérifier**

- [ ] Paiement de test et traitement de confirmation opérationnels, autorisation Achat et profil sans Achat.
- [ ] Souscription avec six mois exacts restants, autre proche d’échéance et autre expirée ; commandes de test remboursables.
- [ ] Opérateurs administrateur/Finance avec autorisation de remboursement et pièces de facturation existantes.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-07-01 | Préparer l’achat à six mois restants puis confirmer en mode test. | Devis chasse : 95 € HT et 3 chasses ; import/communication : 24,50 € HT chacun, capacités correspondantes conservées. Fin alignée sur la base ; droits ouverts après confirmation effective du paiement. |
| RM-07-02 | Annuler/faire échouer un paiement ; revenir plusieurs fois sur le succès d’une autre commande ; **accompagné**, rejouer sa confirmation et tester un paiement tardif devenu incompatible. | Échec sans droit ; succès unique sans recharge au rejeu. Paiement tardif à rapprocher, pas d’ouverture ou prolongation silencieuse. Le retour navigateur seul ne prouve pas le paiement. |
| RM-07-03 | Renouveler avant puis après échéance ; examiner les modules repris au récapitulatif et en retirer un. | Avant : nouvelle période après l’actuelle, sans chevauchement. Après : départ à la réactivation, sans rétrofacturation. Modules achetés proposés à confirmer ; essais/cadeaux jamais transformés automatiquement en achat. |
| RM-07-04 | Demander une montée en gamme en cours de période puis une baisse ; comparer échéance et usages déjà consommés. | Montée après paiement du différentiel proratisé, échéance conservée, usages non remis à zéro ; baisse au prochain renouvellement confirmé. |
| RM-07-05 | Demander l’arrêt puis un remboursement de base ou module ; faire décider un montant partiel/total, et tenter un montant supérieur au solde remboursable. | Arrêt à échéance sans remboursement automatique. Décision manuelle motivée par administrateur/Finance habilité ; plafond encaissé restant respecté, y compris décisions simultanées accompagnées. |
| RM-07-06 | Modifier les coordonnées de facturation avec Achat puis sans ; comparer ancienne facture et nouveau document ; ouvrir un document de B depuis A. | Autorisation requise ; nouvelles coordonnées sur les futurs documents uniquement ; anciennes pièces inchangées, document étranger inaccessible. |

## F08 — Cadeaux, essais, cumuls et expiration des droits

**Objet.** Offrir ou faire tester les modules sans facturation cachée ni recharge artificielle, et terminer proprement les opérations déjà engagées.

**Accès.** ERP → octroi de modules ; Animation → **Abonnement** et usages correspondants. **US16–17 ; CA39–41.**

**Prérequis à vérifier**

- [ ] Base active ; opérateurs avec/sans autorisation d’octroi ; droits achetés, cadeaux et essais qui se chevauchent.
- [ ] Animation publiée, import confirmé commencé, campagne commencée et campagne seulement programmée.
- [ ] États d’expiration préparés avec le référent, sans modifier l’horloge commune.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-08-01 | Accorder un essai de chaque module, puis ajuster durée/quota avec motif ; refaire sans habilitation. | 14 jours par défaut ; chasse 1 et communication 1 au total, import sans quota commercial. Ajustements tracés, bornés par la base ; aucune facture ou conversion en achat implicite ; refus sans habilitation. |
| RM-08-02 | Offrir les modules jusqu’à fin de base puis sur une durée plus courte. | Chasse : 5/an au prorata arrondi au supérieur ; communication : 5/mois par défaut, premier mois incomplet compris ; import sans quota. Quotas ajustables et dates explicites, sans prolonger la base. |
| RM-08-03 | Consommer sous un droit, ajouter un droit comparable puis laisser finir l’essai. | Plafond le plus élevé, jamais addition des quotas ; usages conservés, aucun rechargement par changement de source. Droit acheté préservé après l’essai ; disponible zéro si usages supérieurs au plafond restant. |
| RM-08-04 | **Accompagné :** répéter la fin des droits par expiration de module, retrait commercial anticipé, puis expiration de base. Tenter nouveaux usages et continuités. | Nouvelles créations/publications dépendantes bloquées ; animations publiées terminables, imports lancés reprenables, campagnes commencées terminables sans audience ajoutée. Historique consultable. |
| RM-08-05 | À expiration, ouvrir une campagne programmée non commencée puis renouveler le droit. | Campagne suspendue ; aucune émission automatique au renouvellement. Nouvelle confirmation et contrôles courants avant envoi ; la suspension administrative reste prioritaire. |

## F09 — Créer et publier avec le bon choix de dotation

**Objet.** Préparer une animation avec Coffrets, lots externes ou bons numériques, en sachant précisément ce qu’il reste à faire avant publication.

**Accès.** Animation → **Animations** → création/configuration et assistant. **US01–02, US29 ; CA01–05, 11, 56.**

**Prérequis à vérifier**

- [ ] Organisateur habilité et crédits de publication ; commerçants participants prêts selon le jeu choisi.
- [ ] Un brouillon distinct pour chaque branche ; dotation externe F10 et numérique F11 préparées.
- [ ] Un parcours Coffrets seul sans abonnement Animation, et une animation Coffrets historique pour comparaison.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-09-01 | Créer sans choisir la dotation, puis choisir Libre sans mode ; revenir en arrière dans le formulaire. | Aucune présélection silencieuse ; choix manquants signalés. Récapitulatif et navigation conservent le choix explicite. |
| RM-09-02 | Choisir successivement les trois branches sur des brouillons sans engagement ; regarder l’assistant puis omettre un prérequis pertinent. | Un mode unique par animation ; assistant adapté, blocage précis avec acteur/action attendue ; aucune publication contournant les prérequis. |
| RM-09-03 | Publier une Libre/externe et une Libre/numérique correctement préparées sans commande Coffrets. | Publication possible sous les droits Animation ; aucun paiement Coffrets demandé ni commande, commission ou prestation Coffrets créée. Poursuivre jusqu’à remise avec F10–F14. |
| RM-09-04 | Engager une réservation/affectation puis essayer de changer de mode ; refaire après publication. | Changement refusé ; mode, ordre, quantités engagées et durée publiés conservés. Deux onglets concurrents ne permettent pas de contourner ce gel. |
| RM-09-05 | Acheter/consommer un coffret avec le commerce Coffrets seul ; exécuter publication, réservation/activation et envoi d’un gain d’animation Coffrets historique. | Aucun abonnement ni onboarding Animation imposé au parcours Coffrets seul ; les règles et droits Coffrets historiques sont préservés, sans application implicite des nouvelles règles des lots libres. |

## F10 — Lots libres gérés hors Localeo

**Objet.** Décrire la dotation et suivre le contact/remise sans obliger l’organisateur à digitaliser la remise physique.

**Accès.** Animation → fiche → dotation/lots puis suivi des gains. **US04 ; CA06, 08–10, 29.**

**Prérequis à vérifier**

- [ ] Animation Libre/externe en brouillon et gestionnaire habilité.
- [ ] Responsable de remise externe, sans compte Pro, consignes et quantités connues.
- [ ] Pour le suivi, tirage confirmé de F12 et boîte email gagnant de test.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-10-01 | Créer « Lot A » quantité 2 puis « Lot B » quantité 1 ; saisir responsable/consignes et réordonner avant publication ; essayer quantité nulle. | Trois positions explicites dans l’ordre choisi ; quantité invalide refusée. Aucun QR, compte Pro ou achat Coffrets imposé. |
| RM-10-02 | Après attribution, lire l’email et le suivi avant toute réponse du gagnant. | Lot, responsable et consignes adaptés ; email envoyé ne signifie ni contact réussi ni remise. « Non renseigné » se distingue de « Non remis ». |
| RM-10-03 | Enregistrer contact, réponse puis remise déclarée ; corriger la déclaration avec motif ; essayer avec un simple commerçant/salarié. | Événements et correction tracés, historique conservé ; seuls gestionnaires habilités et Localeo peuvent effectuer ces opérations. |

## F11 — Modèles, exemplaires et affectation des lots numériques

**Objet.** Constituer un stock de lots indivisibles remis par un commerce précis et éviter qu’un même exemplaire soit promis à deux animations.

**Accès.** Animation → fiche Libre/numérique → **Lots**. **US05–06 ; CA30–31, 33.**

**Prérequis à vérifier**

- [ ] Commerce de remise habilité Animation, deux animations de A1 et une de B1.
- [ ] Génération d’exemplaires opérationnelle, clés QR configurées et traitement de fond prêt ; aucun secret copié dans les preuves.
- [ ] Gestionnaire habilité aux lots ; stock vierge réservé à ce test.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-11-01 | Créer un modèle avec un seul commerce de remise, générer 3 exemplaires ; répéter la demande après une réponse incertaine accompagnée. | Exactement 3 exemplaires distincts, sans création supplémentaire au rejeu ; pas de bon utilisable avant attribution, pas de solde fractionnable. |
| RM-11-02 | Affecter un exemplaire à une animation ; tenter de l’affecter à la seconde, y compris depuis deux sessions simultanées. | Une seule affectation active ; indisponibilité claire pour l’autre, aucun stock négatif. |
| RM-11-03 | Modifier la description du modèle après engagement ; essayer de changer le commerce de remise et d’utiliser un exemplaire de B1. | Nouvelle description sans altérer les descriptions déjà engagées ; changement de commerce engagé et accès hors commune autorisée refusés. |
| RM-11-04 | Choisir la durée 1, 90 puis 365 jours sur des brouillons ; essayer 0 et 366 ; publier et retenter l’édition. | 90 par défaut, bornes 1–365 ; erreurs sur valeurs hors limites ; durée figée à publication, échéance calculée à l’attribution. |
| RM-11-05 | Après attributions, libérer le surplus jamais attribué sur confirmation ; tenter la même chose avec un exemplaire attribué puis révoqué. | Seul le surplus jamais attribué redevient disponible ; bon révoqué et ancien gain restent dans l’historique, sans retour automatique au stock. |

## F12 — Tirage, emails, suppléants et remplacement du gagnant

**Objet.** Attribuer les lots équitablement selon l’ordre publié, informer les gagnants et gérer les refus/injoignables sans effacer le tirage initial.

**Accès.** Animation → fiche clôturée → tirage/gains ; email et Live côté gagnant. **US07–08 ; CA06–10, 32–33.**

**Prérequis à vérifier**

- [ ] Animations Libre/externe et Libre/numérique clôturées, populations éligibles figées : 0, 2, 3 et 5 participants pour 3 lots.
- [ ] Tirage libre et envois opérationnels ; deux boîtes gagnants et une liste de suppléants de test.
- [ ] Cas datés « premier email réussi depuis moins de 14 jours / au moins 14 jours », refus explicite et réserve épuisée.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-12-01 | Préparer puis confirmer le tirage pour chacune des quatre populations (0, 2, 3 et 5 éligibles pour 3 lots). | Avant confirmation, aucun gain officiel/email/bon utilisable. Après : respectivement 0, 2, 3 et 3 gagnants distincts, au plus un lot chacun ; ordre des lots publié respecté, surplus en fin ; aucun gagnant inventé. Réserve de suppléants seulement s'il reste des éligibles non gagnants. |
| RM-12-02 | Recharger, rejouer la confirmation ou reprendre après réponse perdue avec le référent. | Mêmes attributions et suppléants, aucun nouveau tirage pour changer le résultat ; un seul bon courant par exemplaire. |
| RM-12-03 | Lire l’email du gagnant et le bon numérique ; provoquer puis reprendre un échec d’envoi contrôlé. | Email automatique après confirmation, lot/commerce/consignes/validité exacts ; gain conservé malgré l’échec. Reprise sans nouveau gain, état d’envoi distinct de remise, aucune commande Coffrets fictive. |
| RM-12-04 | Retirer les droits du commerce numérique après publication mais avant tirage ; tenter la confirmation. | Refus global explicite, aucun gain/bon/email partiel ; pas de lot retiré silencieusement ni de changement de dotation publiée. Nouvelle confirmation possible après résolution habilitée. |
| RM-12-05 | Tenter de remplacer un injoignable avant 14 jours sans refus ; enregistrer un refus explicite sur un autre gain ; remplacer après délai sur le premier. | Avant délai : refus sauf refus explicite. Délai compté depuis le premier email envoyé avec succès ; remplacement manuel motivé selon l’ordre des suppléants éligibles. |
| RM-12-06 | Remplacer un gagnant numérique non servi ; tester son ancien QR et ouvrir le nouveau bon du suppléant ; refaire avec un lot déjà consommé. | Ancien bon définitivement révoqué ; nouveau bon pour le même lot, durée complète depuis nouvelle attribution, historique préservé. Lot déjà consommé non réattribuable. |
| RM-12-07 | Épuiser la réserve puis demander explicitement un nouveau tirage de remplacement, avec puis sans candidat éligible non gagnant. | Retirage possible uniquement sur action tracée et population autorisée ; anciens gagnants remplacés non réintroduits. Aucun nouveau bénéficiaire inventé s’il n’en existe pas, historique conservé. |

## F13 — Remise d’un bon numérique par QR ou PIN

**Objet.** Permettre une remise simple, indivisible et sans ambiguïté, une seule fois, depuis Pro ou le téléphone du gagnant.

**Accès.** Pro → scan ; gagnant → bon reçu/Live → validation par PIN. **US09 ; CA21, 34–35.**

**Prérequis à vérifier**

- [ ] Deux bons valides non consommés pour le commerce, un salarié actif et un autre commerce.
- [ ] Caméra autorisée ; PIN du commerce actif ; configuration QR/PIN et notification de validation opérationnelles.
- [ ] Bons expiré/révoqué, ancien QR remplacé et PIN bloqué préparés ; deuxième téléphone pour la concurrence.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-13-01 | Scanner puis confirmer une remise avec le responsable ; répéter sur un autre bon avec le salarié. | Lot et commerce identifiables avant confirmation ; succès explicite après prise en compte, consommation totale avec date, canal et acteur dans l’historique ; aucune autre prestation à choisir. |
| RM-13-02 | Depuis le téléphone du gagnant, lancer la validation PIN et faire saisir le PIN par le commerce. | Même effet métier que le scan ; résultat relisible. Trace identifiant le commerce pour le canal PIN, sans inventer un salarié ; PIN absent du reçu et des preuves partagées. |
| RM-13-03 | Rescanner/représenter un bon consommé puis consulter son historique. | État « déjà remis » et reçu existant compréhensibles ; aucune seconde consommation ni nouvelle notification de validation logique au rejeu. |
| RM-13-04 | Tester les variantes : autre commerce, bon expiré, révoqué, ancien QR, référence sans attribution et PIN bloqué. | Refus explicite sans remise enregistrée ; aucun message de succès ambigu ni déblocage implicite. |
| RM-13-05 | **Accompagné :** confirmer presque simultanément QR et PIN sur le même bon ; simuler une réponse réseau perdue après prise en compte puis rouvrir. | Une seule consommation active ; le résultat est relu avant nouvelle action. Une incertitude réseau ne s’affiche jamais comme un succès certain ; historique et état final concordent. |

## F14 — Incidents et cycle de vie d’un bon

**Objet.** Corriger une erreur ou aider un gagnant sans perdre la preuve de ce qui a été fait et sans rouvrir un bon interdit.

**Accès.** Animation → fiche → lots/bons ; Localeo habilité pour assistance. **US10 ; CA33, 36.**

**Prérequis à vérifier**

- [ ] Bons non consommé, expiré, consommé, révoqué, proche du plafond de 365 jours.
- [ ] Gestionnaire habilité et compte non habilité ; historique et boîte email de test.
- [ ] Jeu séparé pour une course entre remise et révocation/correction, avec référent technique.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-14-01 | Renvoyer un bon puis remplacer son QR ; comparer bénéficiaire, lot, échéance et tester l’ancien QR. | Aucun nouveau gain ni changement d’échéance ; ancien QR immédiatement inutilisable, nouveau QR fonctionnel selon l’état du bon. |
| RM-14-02 | Prolonger avec motif un bon non consommé, même expiré ; tenter une échéance au-delà de 365 jours depuis attribution initiale. | Seul le bon ciblé change ; plafond absolu respecté, extensions successives non cumulables au-delà ; consommé/révoqué refusé. |
| RM-14-03 | Révoquer avec motif un bon non consommé ; tester ensuite QR/PIN et consultation de l’historique. | Remise bloquée immédiatement, attribution et motif conservés ; pas de retour automatique au stock. |
| RM-14-04 | Annuler avec motif une consommation enregistrée par erreur ; répéter sur un bon désormais expiré ou révoqué. | Validation initiale et correction visibles. Bon à nouveau utilisable seulement si encore valide et non révoqué ; pas d’effacement de l’ancienne action. |
| RM-14-05 | **Accompagné :** lancer remise et révocation/remplacement en concurrence ; refaire sans permission de correction. | Un état final cohérent, jamais deux bons utilisables ni remise autorisée sur état interdit ; refus sans habilitation et conflit compréhensible. |

## F15 — Chasse au trésor et préparation accompagnée

**Objet.** Acheter une capacité de chasses indépendante du forfait et suivre leur préparation par Localeo jusqu’à la validation terrain.

**Accès.** Animation → **Modèles** → chasse puis fiche ; ERP → **Préparations Animation**. **US18, US30 ; CA46, 57.**

**Prérequis à vérifier**

- [ ] Module absent/actif/épuisé et forfait standard doté d’un crédit ; chasse prête et autre incomplète.
- [ ] Calendrier de service, préparation accompagnée et alertes opérationnels ; opérateur et email demandeur.
- [ ] Dossiers en attente de complément, prêts et en retard préparés.
- [ ] Pour le test de disponibilité, le référent dispose d'une cible isolée où le service de préparation E55 peut être déclaré non prêt, puis rétabli, sans affecter les autres recetteurs.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-15-01 | Publier une chasse avec droit actif puis une tombola/passeport ; tenter sans module et avec dernier crédit déjà consommé. | Chasse consomme uniquement son quota dédié, une fois à publication réussie ; standard consomme le forfait. 5 chasses annuelles ou quota proratisé acquis ; aucun report à échéance. |
| RM-15-02 | Déposer une demande complète de préparation puis consulter échéance et état. | Préparation à distance, cible de 5 jours ouvrés depuis demande complète ; pas de promesse d’intervention terrain Localeo. |
| RM-15-03 | Demander un complément côté Localeo, répondre côté client puis marquer prêt. | Attente clairement affichée, délai suspendu pendant l’information indispensable ; reprise sur le même dossier ; email au demandeur et suivi dans le portail, indépendants du module Communication. |
| RM-15-04 | Ouvrir un dossier dépassant son délai, relancer puis faire communiquer une estimation révisée. | État de retard et alerte Ops ; relance sur la demande existante sans demande ni crédit supplémentaire. |
| RM-15-05 | Tenter de publier une chasse non prête ou non validée sur le terrain ; terminer les validations puis publier ; **accompagné**, deux publications sur le dernier crédit. | Prérequis de préparation/terrain respectés ; l’organisateur valide le parcours sur place ; une seule publication autorisée avec le dernier crédit, compteur standard inchangé. |
| RM-15-06 | **Accompagné :** rendre le service de préparation technique E55 non prêt ; tenter l'achat du module ; examiner aussi une commande déjà confirmée avant l'indisponibilité. | Achat refusé ou différé avec diagnostic lorsque le service ne peut pas être fourni. Une commande déjà confirmée passe par une réconciliation support ; aucun nouveau paiement implicite ni promesse de préparation disponible. Distinguer cet incident de la validation terrain d'une chasse particulière. |

## F16 — Import de commerçants et gestion des deltas

**Objet.** Charger un fichier puis ses mises à jour sans doublonner les établissements ni écraser les corrections faites dans Localeo.

**Accès.** Animation → **Import commerçants** ; ERP pour arbitrages SIRET/commune. **US19–20 ; CA42–45.**

**Prérequis à vérifier**

- [ ] Module actif sur A1 et permission Import commerçants ; compte sans permission et commune hors droit.
- [ ] Stockage privé et worker d’import disponibles ; fichiers synthétiques décrits dans le jeu commun.
- [ ] Fiches existantes avec référence du dernier import ; aucun fichier de prospection réel nécessaire. Cet import opérationnel est distinct de l’import CRM de l’epic 71.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-16-01 | Télécharger le modèle ; charger CSV puis XLSX ; choisir une feuille et associer les colonnes avant aperçu. | Import limité à la feuille choisie ; aperçu sans écriture. Obligatoires : nom commercial, adresse, commune, SIRET, email de contact. Facultatifs : nom du contact, téléphone, catégorie, description, site web. |
| RM-16-02 | Tester 100 puis 101 lignes ; fichier de 2 000 000 octets puis plus grand ; lignes invalides et formule dans un champ importable. | Limites appliquées avant création, sans troncature silencieuse. En-tête exclu, lignes entièrement vides ignorées ; formules non exécutées et anomalies signalées. |
| RM-16-03 | Charger email unique connu, email partagé, même email/SIRET différent, autre email/SIRET connu et deux lignes visant la même fiche. | Email principal pour rapprochement ; cas ambigus en conflit explicite, aucune fusion ni « dernière ligne gagnante ». Données d’une autre organisation non révélées. |
| RM-16-04 | Confirmer uniquement les lignes valides d’un fichier mixte ; télécharger le rapport ; tenter sans module ou permission. | Lignes sélectionnées créées/mises à jour une fois ; rejetées identifiables. Nouveau commerce à vérifier, demande Animation soumise à Localeo ; aucun compte activé, invitation envoyée ou participation acceptée automatiquement. Refus hors droit. |
| RM-16-05 | Importer V1, modifier localement le téléphone ; dans V2 modifier ce téléphone différemment, changer un site non retouché localement, laisser une cellule vide et conserver un autre champ inchangé. | Téléphone en conflit à arbitrer ; site modifiable après confirmation ; cellule vide sans effacement ; modifications locales préservées si le fichier n’a pas changé le champ. Différences présentées champ par champ. |
| RM-16-06 | Après aperçu, faire modifier une fiche par un autre opérateur, puis confirmer ; changer email de contact, SIRET et commune dans des variantes distinctes. | Écart intervenu après aperçu détecté, pas d’écrasement silencieux. Email de contact ne change pas le login ; SIRET/commune exigent validation Localeo ERP, pas seulement résolution du rapprochement. |
| RM-16-07 | **Accompagné :** interrompre après une ligne réussie, reprendre ; expirer le module avant démarrage puis pendant un autre import déjà commencé. | Avant démarrage : refus ; déjà lancé : reprise du même import autorisée selon continuité, sans retraiter les succès ni ajouter de nouvelles lignes, aucun doublon. |
| RM-16-08 | **Accompagné :** consulter un import terminé/abandonné depuis plus de 30 jours, puis ses fiches et un réimport. | Fichier source/rapport ne restent pas téléchargeables au-delà de leur conservation ; fiches, provenance nécessaire aux deltas et audits selon leur propre politique préservés. |

## F17 — Messages organisateur dans Live et en Web Push

**Objet.** Communiquer avec les participants autorisés au bon moment, avec des quotas compréhensibles et sans sollicitations excessives.

**Accès.** Animation → fiche → communication participants ; Live → messagerie/préférences ; Ops → alertes. **US21–22 ; CA47–49.**

**Prérequis à vérifier**

- [ ] Module et autorisation Communication ; participants répartis dans les quatre audiences et préférences variées, dont un sans accord explicite aux messages organisateur ; un simple abonné à la commune sans participation.
- [ ] Traitement de campagnes, dépôt Live, transport Push/VAPID, protection d’identité de fréquence et destinataires des alertes internes configurés ; appareils de test uniquement.
- [ ] Deux animations de A1, un participant commun multi-appareils ; campagnes à dernier crédit, en échec, programmées et commencées préparées.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-17-01 | Préparer un message pour chacune des audiences : tous, parcours non terminé, parcours terminé, gagnants ; essayer avant publication et après clôture +30 jours. | Audience de la seule animation et droits courants ; fenêtre publication à clôture +30 jours respectée. Absence du module ou de permission interdit la campagne, sans bloquer les notifications automatiques d’animation. |
| RM-17-02 | Envoyer immédiatement aux comptes autorisant les messages, l’un avec Push et l’autre sans ; vérifier l'exclusion d'un participant opposé, d'un participant sans accord explicite et d'un simple abonné à la commune sans participation, même s'ils acceptent le Push ou les notifications automatiques. | Message consultable dans Live même sans permission navigateur ; Push uniquement autorisé ; les trois profils exclus ne reçoivent rien, aucun repli email/SMS. La permission navigateur ne vaut pas accord aux messages organisateur. Dépôt Live, envoi Push et erreurs distingués ; aucun de ces résultats ne prouve une lecture. |
| RM-17-03 | Programmer en heure de Paris ; changer une préférence ou retirer la permission du gestionnaire avant démarrage. | Droits/destinataires revérifiés au départ ; tâches concernées suspendues ou destinataires exclus, pas d’envoi fondé sur les seules permissions de programmation. |
| RM-17-04 | Préparer/annuler des brouillons puis démarrer des campagnes jusqu’au quota, reprendre une campagne déjà commencée. | Une unité au premier message Live accepté, qui constitue le démarrage effectif, jamais au brouillon/à la programmation/préparation ; 5/mois partagés par commune/souscription, indépendants du nombre de destinataires ; reprises sans second débit. |
| RM-17-05 | **Accompagné :** activer en fin de mois, passer le premier du mois Paris et une borne de changement d’heure ; comparer essai et achat. | Premier mois incomplet : 5 campagnes ; mois civil Paris sans report. Essai par défaut : 1 campagne au total, même s’il chevauche deux mois ; cadeau : 5/mois par défaut, sous conditions d’octroi. |
| RM-17-06 | Laisser une programmation arriver avec quota épuisé ou droit expiré ; rétablir le droit/quota. | Campagne suspendue et gestionnaire informé ; aucun envoi automatique au nouveau mois/renouvellement ; confirmation explicite et vérifications avant reprise. |
| RM-17-07 | Cibler la même personne dans deux campagnes/animations de A1 sur 24 h, avec plusieurs appareils ; attendre/préparer la fin de fenêtre. | Limite initiale 1 message par personne/commune/24 h glissantes ; deuxième exclusion sans envoi différé automatique ; plusieurs appareils ne multiplient pas les droits ; notifications automatiques indépendantes. |
| RM-17-08 | Cibler cette personne avec une troisième campagne distincte ; rejouer une reprise puis répéter sur plusieurs participants ; ajuster limite/multiplicateur côté ERP habilité. | Alerte initiale à 3 fois la limite, tentatives bloquées incluses, reprises non recomptées ; alerte Ops et email interne regroupé, pas un email par personne ; réglage tracé et refusé sans autorisation. |
| RM-17-09 | **Accompagné :** interrompre une campagne partiellement commencée, expirer le module puis reprendre, avec consentement retiré d’un destinataire restant. | Campagne terminable avec audience figée, droits des destinataires restants revérifiés ; pas de double message Live ni double débit. Échecs/incertitudes visibles ; aucune livraison navigateur certaine annoncée sans preuve. |
| RM-17-10 | Préparer une campagne dont tous les destinataires sont exclus par préférence ou fréquence, puis lancer son traitement. | Résultat « sans destinataire », motifs d'exclusion consultables ; aucun message et aucun crédit de campagne consommé. Les tentatives éligibles à l'alerte de fréquence restent tracées. |
| RM-17-11 | **Accompagné :** avec un seul crédit disponible, lancer deux campagnes ayant chacune un destinataire autorisé distinct. | Une seule campagne peut démarrer et débiter le dernier crédit ; l'autre reste suspendue sans message. Aucun quota négatif ni double ouverture. |

## F18 — Site public Animation, inscription et continuité de Live

**Objet.** Présenter Animation comme un produit autonome, avec un site de découverte lisible et un accès continu aux participations et gains existants.

**Accès.** Site public configuré en surface Animation, cible `animations.localeo.city` ; Live ; anciens liens emails/QR. **US23 ; CA23–24.**

**Prérequis à vérifier**

- [ ] URL de recette de la surface Animation et origine publique configurées ; liens vers portail et Live résolus.
- [ ] Animation publiée, commerce Animation seul, participant neuf et participant avec ancien carnet incluant des coffrets.
- [ ] Anciens emails/QR de test ; navigateur ayant accepté puis autre ayant refusé Push.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-18-01 | Découvrir une animation, sa fiche, les commerçants et les modalités ; s’inscrire puis participer. | Parcours autonome sans achat de coffret imposé ; contenus de communication compréhensibles, sans menus d’administration client. |
| RM-18-02 | Ouvrir la fiche d’un commerce Animation seul et ses animations liées. | Présence publique Animation ; aucune présentation comme fournisseur de prestations Coffrets sans ce périmètre. |
| RM-18-03 | Ouvrir anciens QR/emails/carnets puis accéder au nouveau site ; suivre la reprise explicite si proposée. | Mêmes comptes, participations et gains ; aucun doublon ni perte de coffrets déjà présents dans Live. Liens inactifs/expirés expliqués plutôt qu’une page vide. |
| RM-18-04 | Refuser la réactivation des notifications sur la nouvelle origine, puis participer et lire la messagerie ; refaire en acceptant. | Push facultatif ; ni participation ni lecture Live bloquée. Une ancienne permission navigateur n’est pas présentée comme transférée automatiquement entre origines. |

## F19 — Aide et support de l’organisateur

**Objet.** Trouver une aide utile et suivre une demande privée, avec un délai de première réponse humaine identifiable.

**Accès.** Animation → **Support**/aide ; Localeo Support côté opérateur. **US31 ; CA58.**

**Prérequis à vérifier**

- [ ] Guides/FAQ accessibles, compte client A et agent Support autorisé.
- [ ] Calendrier de service actif ; demande ancienne sans réponse humaine et autre avec note interne.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-19-01 | Consulter l’aide puis créer une demande liée à une animation ; répondre côté Support puis client. | Échange persistant dans un même dossier, état et référence lisibles ; pas de duplication après rechargement/reprise. |
| RM-19-02 | Comparer accusé automatique, cible de 2 jours ouvrés et première réponse humaine. | Accusé ne vaut pas prise en charge humaine ; délai et éventuel retard ne sont pas masqués par l’automatisme. Aucune promesse de résolution en 2 jours n’est déduite. |
| RM-19-03 | Consulter avec A une demande de B et chercher les notes internes depuis le compte client. | Données étrangères et notes internes inaccessibles ; seuls échanges destinés au client visibles. |

## F20 — Préparer une nouvelle édition

**Objet.** Réutiliser les contenus d’une animation en conservant les validations indispensables à chaque nouvelle édition.

**Accès.** Animation → fiche → nouvelle édition. **US32 ; CA59.**

**Prérequis à vérifier**

- [ ] Animation source avec dates, contenus, commerçants, participants, gains et accords ; gestionnaire autorisé.
- [ ] Commune A2 également accessible au gestionnaire pour tester le refus intercommune.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-20-01 | Choisir les sections à réutiliser et de nouvelles dates ; créer l’édition dans A1 puis tenter A2. | Nouveau brouillon dans la même commune seulement ; source conservée, provenance identifiable ; A2 refusée même si accessible au gestionnaire. |
| RM-20-02 | Examiner participants, gains, QR, paiements, accords et consentements du brouillon ; tenter sa publication. | Aucun de ces objets recopié ; commerçants, droits, dotation, règlement et accords à revalider ; publication bloquée tant que nécessaire. |
| RM-20-03 | **Accompagné :** modifier la source après ouverture du formulaire ou reprendre une création après réponse perdue. | Conflit de version explicite, pas de copie incohérente ; un seul nouveau brouillon pour une même création reprise. |

## F21 — Objectifs, sources de diffusion, bilans et satisfaction

**Objet.** Montrer les résultats réellement mesurés et leur provenance, sans assimiler des passages à du chiffre d’affaires.

**Accès.** Animation → fiche/bilan, **Bilans** ; Live après clôture. **US33 ; CA60.**

**Prérequis à vérifier**

- [ ] Objectifs avant publication ; liens/QR « mairie » et « commerçant » ; inscriptions avec et sans source.
- [ ] Jeu chiffré connu : inscriptions, démarrages, parcours terminés, validations QR/PIN, gains et remises ; une correction de remise et un remplacement de gagnant.
- [ ] Animation clôturée et au moins deux répondants de test ; compte organisateur sans accès à leur identité via l’enquête.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-21-01 | Fixer les objectifs puis publier ; tenter de changer les objectifs ; comparer résultats et édition comparable. | Objectifs facultatifs mais figés à publication ; définitions et comparabilité lisibles ; absence de données distincte de zéro. |
| RM-21-02 | Inscrire via les deux sources et sans source ; contrôler le bilan. | Attribution à la source connue et catégorie « inconnue », aucun suivi publicitaire entre sites ; total cohérent avec les inscriptions retenues. |
| RM-21-03 | Vérifier les totaux avant/après remise, rescan, correction et remplacement à partir des références du jeu. | Aucun double comptage QR/PIN/rejeu ; indicateurs distincts inscrits, commencés/terminés, passages, gagnants et lots remis. Aucun chiffre d’affaires inventé à partir des passages. |
| RM-21-04 | Après clôture, répondre dans Live avec note 1 puis 5 et commentaire facultatif ; tester 0/6, absence de réponse et accès avant clôture. | Enquête facultative accessible après clôture ; bornes respectées ; moyenne et nombre de réponses cohérents, commentaires sans identité affichée à l’organisateur ; aucune notification supplémentaire automatique. |

## F22 — Cohérence ERP, Support et Atelier

**Objet.** Retrouver les mêmes informations de produit et de lot dans les outils internes sans traiter un lot libre comme un coffret vendu.

**Accès.** ERP/Support → **Animations et lots** ; Atelier → sélection des fournisseurs. **US24 ; CA25.**

**Prérequis à vérifier**

- [ ] Une animation et un gain de chacune des trois dotations, un commerce Animation seul et un fournisseur Coffrets.
- [ ] Opérateurs habilités et lectures/export internes ; assez d’objets pour plusieurs pages.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-22-01 | Retrouver chaque gain dans ERP/Support, filtrer par nature/commune, paginer et exporter la page affichée. | Libellés et états cohérents avec Animation/Pro/Live ; pas de confusion bon/coffret/externe, pas d’objet étranger ; CSV limité à la page affichée, conforme au filtre et aux droits. Il n'est pas présenté comme un export de toutes les pages. |
| RM-22-02 | Vérifier les sommes financières des trois dotations ; tenter de sélectionner le commerce Animation seul comme fournisseur de prestation Coffrets dans Atelier. | Lots libres exclus des achats/commissions/reversements Coffrets ; sélection et commande interdite côté serveur pour le fournisseur non habilité. |
| RM-22-03 | Ouvrir une projection commerciale/CRM disponible et ses liens vers les parcours métier. | Consultation ne crée ni vente, paiement, activation ou périmètre. Le CRM complet et son import E71 ne sont pas considérés comme livrés par E73. |

## F23 — Usages, coûts internes et alertes de budget

**Objet.** Permettre au client de comprendre ses usages et à Localeo de suivre ses coûts sans exposer ses informations internes ni déclencher une facturation automatique.

**Accès.** Client → usages/quotas/factures ; ERP → pilotage économique ; Ops → alertes. **US34 ; CA61.**

**Prérequis à vérifier**

- [ ] Mesures d’emails, SMS, préparation de chasse, stockage, Push et support : valeurs constatées, estimées et indisponibles.
- [ ] Traitement de pilotage et alertes configurés ; budget synthétique de 100 € pour A et aucun budget pour B.
- [ ] Profils client et Localeo habilité ; deux périodes mensuelles identifiées.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-23-01 | Consulter coûts par organisation puis commune/souscription/module selon données ; comparer au compte client. | Interne : postes, période et fiabilité explicites. Client : usages, quotas, factures seulement ; pas de coûts/marges internes. Donnée absente ou estimation jamais présentée comme dépense certaine. |
| RM-23-02 | **Accompagné :** faire passer le coût suivi de 79 à 80 puis 100 € ; rejouer les événements ; consulter l’organisation sans budget. | Alertes internes aux seuils 80 %/100 %, pas de doublon logique au rejeu ; sans budget, suivi disponible sans alerte de budget. |
| RM-23-03 | Après dépassement, consulter abonnement, quotas et parcours de l’organisateur. | Aucun supplément facturé, suspension ou quota changé par la seule alerte économique. |

## F24 — Export complet et fermeture accompagnée

**Objet.** Récupérer les données transmissibles et quitter le service sans abandonner les engagements en cours ni fermer les accès à d’autres organisations.

**Accès.** Animation → **Compte et équipe** → export/fermeture ; ERP → réversibilité. **US35 ; CA62.**

**Prérequis à vérifier**

- [ ] Organisation de test dédiée, responsable et collaborateur ; ce responsable possède aussi un accès à B.
- [ ] Worker d’export, stockage privé, calendrier et notification opérationnels ; médias transmissibles et archive expirée préparés.
- [ ] Engagements ouverts connus : animation publiée, bon non consommé y compris expiré, dossier de préparation ; procédure opérateur pour leur résolution.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-24-01 | Demander un export avec collaborateur puis responsable ; suivre sa préparation et sa disponibilité. | Responsable seul ; inclus sans frais, cible 5 jours ouvrés ; demande identifiée, notification de disponibilité sans archive publique ni fermeture automatique. |
| RM-24-02 | Télécharger l’archive connecté ; ouvrir CSV, médias et guide ; comparer des références connues et les engagements en cours. | Archive cohérente avec la date de capture, IDs/liens explicables, omissions motivées ; aucune donnée de B, note/coût interne, mot de passe, session ou QR actif. CSV sans formule exécutée à l’ouverture. |
| RM-24-03 | **Accompagné :** interrompre/reprendre la génération, tenter téléchargement sans rôle puis après 30 jours de disponibilité ; consulter les données sources. | Pas d’archive partielle annoncée ; accès contrôlé à chaque téléchargement et refus après échéance ; purge de l’archive sans suppression des données métier selon leurs règles propres. |
| RM-24-04 | Demander séparément la fermeture comme responsable avec engagements ouverts ; tenter nouvel usage et fin des engagements existants. | Nouveaux usages bloqués ; historique et actions strictement nécessaires préservés ; inventaire complet, fermeture effective bloquée tant que des obligations restent non résolues. |
| RM-24-05 | Résoudre les engagements ou effectuer une reprise explicitement supportée et acceptée ; faire confirmer la fermeture par Localeo. | Pas de transfert fictif : seules les reprises réellement exécutables sont proposées ; sinon continuité jusqu’à résolution. Date et conservation communiquées, accès A fermés, accès B conservés. |

La reprise interne disponible pour une préparation ne prouve pas qu’un gain, un bon ou une obligation financière puisse être transféré. Un bon expiré mais encore prolongeable ne doit pas disparaître artificiellement de l’inventaire. Vérifier également les exports encore disponibles avant confirmation de la fermeture, selon les contrôles du dossier.

## F25 — Reprise de l’existant, démonstration et ouverture du pilote

**Objet.** Passer à la nouvelle offre sans perte d’engagements et prouver que le service peut être exploité et restauré avant son ouverture.

**Accès.** ERP → revue des périmètres communaux ; parcours des applications ; outils d’exploitation avec l’équipe technique. **US36–38 ; CA26–28, 63.**

**Prérequis à vérifier**

- [ ] Inventaire de commerces historiques et engagements, dont un commerce non revu ; compte opérateur autorisé.
- [ ] Manifestes de versions/configuration, jeux de démonstration et preuves locales consultables ; cible isolée pour restauration.
- [ ] Plan pilote Martignas-sur-Jalle et responsables de validation Localeo/commune ; accord spécifique avant toute opération réelle d’environnement.

| Test | Actions métier | Résultat attendu |
| --- | --- | --- |
| RM-25-01 | Examiner les commerces existants, saisir manuellement leurs périmètres puis tenter la bascule avec un commerce non revu ; terminer la revue. | Pas de proposition/activation automatique Animation+Coffrets ; commerce non revu bloque la bascule concernée. Avant bascule, fonctionnement historique préservé sans retrait silencieux. |
| RM-25-02 | **Accompagné :** pendant la vérification de bascule, créer/déplacer un commerce puis relire l’éligibilité. | Impossible de basculer en oubliant le nouvel objet ; contrôle courant et décision tracée. Engagements antérieurs toujours identifiables. |
| RM-25-03 | **Accompagné :** générer un jeu synthétique puis le sauvegarder/restaurer sur cible isolée ; reprendre des parcours QR/PIN, import et permissions. | Mêmes règles et refus que pour les données créées par interface ; pas de privilèges ou activation forcée par le générateur ; parcours et fichiers cohérents après restauration. |
| RM-25-04 | Faire examiner le manifeste, les résultats des recettes et les anomalies ; faire valider l’UX par Localeo puis Martignas-sur-Jalle. | Décision pilote explicite ; aucun déploiement ni généralisation déduit d’un simple build vert. Extension progressive uniquement après bilan du pilote. |
| RM-25-05 | **Accompagné technique, sur cible isolée représentative :** restaurer base/fichiers/configuration et reprendre accès, participation, validation et remise ; chronométrer jusqu’aux contrôles terminés. | Perte maximale mesurée **4 h**, reprise **8 h**, contrôles compris ; données, droits et traitements cohérents, suppressions dues réappliquées, accès révoqués non réactivés. Preuve datée requise avant mise en service, chaque trimestre et après changement majeur. |
| RM-25-06 | Examiner un dossier sans preuve de restauration ou dont un objectif échoue. | Mise en service concernée bloquée jusqu’à correction/preuve ; une simulation locale seule ne vaut pas démonstration hébergée. |

## Contrôles métier transverses à répéter dans les parcours

| Test | Préparation et actions | Résultat attendu / preuve |
| --- | --- | --- |
| RM-X-01 — Navigation | Sur téléphone étroit puis ordinateur, parcourir les fonctions autorisées du portail ; côté interne, vérifier menus et retour accueil ERP ; côté public, découverte et participation. | Portail avec codes d’application de gestion, site public avec codes de communication ; contexte organisation/commune visible, retour et action principale identifiables ; aucune fonction importante rendue inaccessible par débordement. |
| RM-X-02 — Accessibilité | Tester clavier seul, focus, zoom 200 %, erreurs de formulaire et états des lots sans s’appuyer uniquement sur leur couleur. | Libellés, ordre de lecture et messages compréhensibles ; focus utilisable, texte non masqué ; succès/refus/déjà traité distinguables. Recette UX ciblée, pas certification d’accessibilité complète. |
| RM-X-03 — Dates | Depuis un appareil configuré hors France, lire échéances de bons, campagnes, factures et délais de service ; inclure un changement d’heure. | Dates/horaires métier affichés en Europe/Paris, échéances compréhensibles ; dates civiles sans décalage accidentel. Le calcul des jours ouvrés suit le calendrier de service. |
| RM-X-04 — Reprise et historique | Dans chaque action à effet, recharger après confirmation ; sur les jeux accompagnés, couper la réponse puis relire l’état ; ouvrir l’historique. | Pas de double paiement/gain/message/consommation ; état réel consultable, auteur/date/motif et référence d’opération présents selon l’action. Aucun secret dans les captures ou exports de preuve. |
| RM-X-05 — Isolation | Avec un lecteur puis un compte A, ouvrir un lien mémorisé vers écriture ou objet B ; retirer un droit pendant une session. | Masquage cohérent avec refus effectif ; pas d’accès par lien direct, ancien contexte ou session ouverte, ni divulgation de données étrangères dans l’erreur. |
| RM-X-06 — Volumétrie | **Accompagné :** jeu de 10 communes et 10 000 participants au total ; 10 utilisateurs actifs simultanés. Paginer, filtrer, changer de commune, consulter bilan et poursuivre validation pendant import/campagne. Comparer au jeu réduit, mêmes actions. | Pages navigables sans doublons/omissions sur un jeu stabilisé ; filtres/contexte conservés ; traitements longs avec progression et reprise, sans blocage du parcours interactif. Relever durées et erreurs, comparer aux budgets de l’architecture. Aucune garantie de charge déduite d’un ressenti ou d’une seule exécution. |

La recette métier ne démontre pas à elle seule l’usage d’index ou l’absence de chargement d’une table complète. Joindre pour RM-X-06 les preuves de pagination, requêtes et charge de la [matrice de performance](architecture-contrats.md). Les lectures historiques non migrées et limites enregistrées dans le suivi doivent rester visibles dans le bilan, sans généraliser la validation de quelques écrans à toute la plateforme.

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
