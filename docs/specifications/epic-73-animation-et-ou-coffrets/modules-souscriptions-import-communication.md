# EPIC 73 — Modules, souscriptions, imports et communication

## Statut, périmètre et références

Spécification cible du 17 octobre 2026, **à implémenter**. Elle détaille US03, US14 à 22, US27/28 et US34 du [backlog canonique](../../roadmap/a-faire/epic-73-animation-et-ou-coffrets-backlog.md), notamment CA-12 à 14, CA-37 à 49, CA-54/55 et CA-61. Les décisions DEC-20 à 32, DEC-60 à 108, DEC-120 à 124 et DEC-135 à 137 s'appliquent intégralement. Les descriptions de stockage et les nouvelles routes ci-dessous sont des contrats proposés pour l'implémentation ; leur présence ici ne prouve ni une API déployée ni un paiement possible.

Lire avec [architecture et contrats](architecture-contrats.md), [périmètres et parcours SaaS](perimetres-parcours-saas.md), [dotations et lots](dotation-lots.md) et [preuves et livraison](verification-livraison.md). Les comptes, délégations et rattachements de commune sont définis dans le document de parcours ; ce document en consomme les décisions sans créer un deuxième modèle d'identité.

## 1. Existant vérifié et écarts à traiter

| Source réelle lue | Comportement observé | Conséquence E73 |
| --- | --- | --- |
| [Entités Abonnements](../../../../localeo-backend/app/domaine/abonnements_plateforme/entities.py), [politique de souscription](../../../../localeo-backend/app/domaine/abonnements_plateforme/politique_souscription.py) | Offre avec prix HT, durée, droits, limites ; abonnement par partenaire/commune ; états ACTIF/EN_GRACE/EXPIRE/SUSPENDU ; calcul TVA au centime avec arrondi HALF_UP | Étendre ce domaine aux versions de catalogue, droits de modules et périodes, sans déplacer les règles dans le portail |
| [Service de souscription E47](../../../../localeo-backend/app/application/abonnements_plateforme/service_souscriptions.py) et [API E47](../../../../localeo-backend/app/api/abonnements_plateforme_api.py) | Commande, paiement Checkout, activation payée/gratuite, instantanés de prix/facturation, emails, événements Stripe ; consommation de quota sous verrou abonnement et unicité par animation | Réutiliser paiement, audit, email et journal. Les commandes client ne peuvent pas reprendre les paramètres administrateur de prix/TVA/motif libre |
| [Vérification du droit plateforme](../../../../localeo-backend/app/application/abonnements_plateforme/services/verification_droit_plateforme.py), [consultation abonnement](../../../../localeo-backend/app/application/abonnements_plateforme/use_cases/consulter_abonnement_plateforme.py) | Continuité après expiration pour clôture/tirage/envoi/bilan/export ; offre et quota relus depuis l'offre courante mutable | Faire décider le domaine sur les conditions acquises figées ; désactiver une offre au catalogue ne retire pas les droits déjà acquis. Ajouter preuve d'engagement pour la continuité, plutôt qu'autoriser toute action d'une famille |
| [Publication](../../../../localeo-backend/app/application/animation_locale/services/publication_animation.py), [gestion des animations](../../../../localeo-backend/app/application/animation_locale/services/gestion_animations.py) | Quota consommé lors de la publication ; libération existante lors d'une annulation | Distinguer journal CHASSE et journal ANIMATION_STANDARD, conserver les consommations historiques, rendre le débit atomique avec la publication et préserver les conditions existantes de libération |
| [Référencer un commerce](../../../../localeo-backend/app/application/referencement/use_cases/referencer_commercant.py) | Point d'entrée dans une UoW, brouillon, ouverture du dossier OnBoard, option `initialiser_acces=False` ; catégorie requise, doublons nom/commune ou email refusés | Réutiliser le métier de référencement et l'option sans accès ; adapter le brouillon de préparation pour la catégorie facultative, sans catégorie fictive ni invitation. Ne pas appeler le comportement par défaut qui initialise l'accès |
| [Modification du contact](../../../../localeo-backend/app/application/referencement/use_cases/mettre_a_jour_contact_commercant.py) | Modification nom/prénom/téléphone, pas de changement d'email par cette commande | Concevoir une commande de mise à jour autorisée de la fiche ; ne pas modifier le login ou transférer le compte en modifiant un email d'import |
| [Notifications Animation Live](../../../../localeo-backend/app/application/animation_locale/services/notifications_localeo_live.py), [API et traitement Live](../../../../localeo-backend/app/api/localeo_live_api.py) | Installations, suivis de participation, inbox, préférences, notifications de clôture/tirage ; diffusion d'actualités pouvant réunir commune suivie et participants ; traitements avec claims/reprises | Réutiliser stockage et transport, mais isoler le ciblage organisateur et son autorisation. Une personne qui suit la commune sans participer n'est pas destinataire |
| [Modèles SQL](../../../../localeo-backend/app/infrastructure/persistence/models.py) | Participant unique par animation/email normalisé ; consentement notifications ; abonnement Live distinct de l'installation ; source de notification permettant la déduplication | Fréquence interanimations portée par identité participant dans la commune, jamais par installation. Distinguer préférence organisateur et permission navigateur |
| [Factures Localeo](../../../../localeo-backend/app/api/factures_localeo_api.py), [service documentaire financier](../../../../localeo-backend/app/application/conformite_fiscale_bum/service_factures_localeo.py) | Consultation et téléchargement de factures Animation existants | Réutiliser émission, numérotation, pièces et autorisations ; ne pas créer de PDF de facture dans le module commercial |
| [Client Animation](../../../../localeo-animation/src/app/api.ts), [client Marketplace](../../../../localeo-marketplace/src/services/api.js), [Live](../../../../localeo-marketplace/src/live/LiveApp.jsx) | Lecture abonnement/factures, appels centralisés ; Live public existant | Étendre les contrats embarqués et consommateurs après implémentation ; conserver sessions, CSRF, invalidation des réponses au changement de contexte |

L'[import CRM E71](../epic-71-crm-prospection/import-carte.md) est une référence de conception pour les deltas, pas un import opérationnel de commerçants livré à réutiliser comme s'il activait des comptes. Les règles de rapprochement E73 sont celles explicitement retenues ici : **email en premier**, pas le modèle d'identification CRM.

Les services E47 et Live cités comportent actuellement de l'orchestration SQL ou des règles dans des adaptateurs. L'évolution extrait les règles modifiées vers leur domaine, avec ports et UoW ; elle ne propage pas ces couplages dans de nouvelles routes. Aucune refonte des domaines non touchés n'est demandée.

## 2. Responsabilités et invariants

| Propriétaire cible | Objet ou politique | Règle commune API / ERP / batch |
| --- | --- | --- |
| `abonnements_plateforme` | VersionCatalogue, ConditionsAcquises, DroitModule, PériodeSouscription, CompteurUsage | Autorisation d'usage = souscription/base valide + droit applicable + habilitation + périmètre + quota, ou continuité précisément justifiée. Le paiement attendu ne suffit jamais |
| `abonnements_plateforme` | CommandeCommerciale, DécisionRemboursement | Prix, périodes, taxes et quotas calculés côté serveur ; confirmation de paiement/activation unique ; aucune double activation ou restitution de quota par rejeu |
| `referencement` | LotImport, LigneImport, ProvenanceChamp, DemandeCorrectionIdentité | Deltas protégés, droits par commune, fiche à vérifier sans compte ni périmètre actif, pas de fusion silencieuse |
| `animation_locale` | CampagneOrganisateur, AudienceFigée, PolitiqueSollicitation | Participants de l'animation uniquement, consentements applicables, fenêtre autorisée et fréquence par commune, campagne décomptée une fois |
| `exploitation` | MesureUsage, ValorisationCoût, BudgetSuivi | Coût et quota distincts ; fiabilité et couverture visibles ; alerte de budget sans mutation commerciale |
| Identité / Accès | Habilitations effectives | Le retrait de rôle ou de commune s'applique à la requête suivante et aux travaux non commencés. Une action financière, d'import ou de communication ne découle pas de la seule possession du module |
| Conformité/finances et ports de paiement existants | Pièce émise, confirmation fournisseur | Les factures émises restent immuables ; un remboursement confirmé ne se simule pas par changement du statut payé |

Les propriétaires échangent des faits/identifiants par ports. Une campagne reçoit une décision de droit/quota ; elle ne lit pas directement les ORM d'abonnement dans le domaine. Le traitement d'import orchestre les commandes Référencement/OnBoard et consigne leur résultat dans la même transaction de ligne. Un worker ne rejoue jamais les privilèges d'un utilisateur révoqué : il exécute une opération engagée, bornée et contrôlée avec identité technique tracée.

### Habilitations

| Action | Organisation cliente | Localeo |
| --- | --- | --- |
| Lire les modules/usages/quotas de la commune autorisée | Responsable, Gestionnaire, Lecteur selon habilitation de lecture | Profils internes autorisés au dossier |
| Acheter module, renouveler, changer de forfait, modifier facturation future | Responsable ou collaborateur avec **Achat** | Parcours commercial ERP existant, autorisation interne correspondante |
| Accorder/modifier cadeau ou essai | Jamais | Administrateur ou Backoffice avec autorisation d'octroi dédiée ; motif obligatoire |
| Modifier prix, contenu et quotas du catalogue | Jamais | Administrateur uniquement |
| Confirmer import et reprise | Responsable ou collaborateur **Import commerçants**, commune autorisée | Habilitation de référencement/import ; pas par simple accès Finance |
| Programmer/envoyer/reconfirmer campagne | Gestionnaire habilité à l'animation avec **Communication** ; Responsable doit également disposer de l'action effective prévue dans la matrice d'identité | Autorisation de communication explicite et périmètre de l'animation |
| Régler fréquence et seuil d'alerte | Jamais | Administrateur ou Backoffice avec autorisation dédiée, motif |
| Approuver/refuser remboursement et fixer montant | Demande seulement | Administrateur ou Finance avec autorisation dédiée, motif |
| Coûts/marges et budgets internes | Aucun accès | Équipes internes habilitées ; administration du budget réservée à l'habilitation de pilotage économique |

L'acteur, l'organisation et les communes sont dérivés de la session et contrôlés ; aucun `acteur` envoyé par le navigateur ne donne une autorisation. Une ressource d'un autre tenant renvoie un refus sans divulguer son contenu.

## 3. Catalogue et droits acquis

### Catalogue initial et unités

| Élément | Prix initial HT | Période / capacité | Consommation |
| --- | --- | --- | --- |
| Forfaits Animation | Conserver prix et volumes du catalogue existant confirmé ; instantané à l'achat | Passeport et tombola inclus, limite propre au forfait | Première publication réussie, journal standard |
| `CHASSE_TRESOR` | 19 000 centimes / an | 5 chasses annuelles ; quota **indépendant et supplémentaire** | Première publication réussie, journal chasse uniquement |
| `IMPORT_COMMERCANTS` | 4 900 centimes / an | Imports et mises à jour sans quota commercial | Pas de débit commercial ; limites techniques par fichier |
| `COMMUNICATION_PARTICIPANTS` | 4 900 centimes / an | 5 campagnes par mois civil Europe/Paris | Début effectif de campagne, une fois |

Le code du module est stable ; son libellé commercial peut être « Messages aux participants — Live et Web Push ». Il ne masque pas le fait qu'un message reste dans Live sans permission Push. La tombola/passeport et leurs variantes restent inclus dans leur droit de type ; les variantes de chasse n'exigent pas un achat par scénario. Les trois modules sont optionnels pour les nouvelles souscriptions. Les droits anciens sont repris factuellement et préservés jusqu'à échéance, sans attribution rétroactive d'un supplément payant.

`VersionCatalogue` est immuable après publication : code, version, libellé, prix HT/devise, durée de référence, liste de droits, limites typées (`unite`, `periode`, `quantite` nullable pour illimité), prérequis, modèle de service. Une édition crée une nouvelle version ; les commandes et droits existants référencent l'ancienne. Une offre retirée du catalogue ne retire pas les droits acquis. Il n'y a pas de chargement de code tiers : les modules officiels activent des fonctionnalités déployées du socle.

Le panier présente commune, forfait, modules, mode acquis, dates, prix catalogue, prorata, HT/TVA/TTC, volumes et engagements du service. L'essai/gift n'est ni une remise fictive sur une commande ni une facture à zéro créée pour gonfler le chiffre d'affaires.

### Origine et cycle d'un droit

`DroitModule` contient `id`, `partenaire_id`, `commune_id`, `periode_souscription_id`, `module_code`, `origine` (`INCLUS`, `ACHETE`, `OFFERT`, `ESSAI`), référence/version de conditions, `debut_at`, `fin_at`, limites acquises, preuve d'origine, acteur/motif pour octroi et `version`. Un droit acheté ne référence qu'une ligne commercialement confirmée. Une source donnée ne peut créer qu'un droit pour la même période/module/commune.

États persistés : `PREVU`, `ACTIF`, `RETIRE`, `SUSPENDU`. `EXPIRE` est aussi calculé à chaque décision d'accès par comparaison à `fin_at` ; le batch de projection n'est pas la barrière d'expiration. Activation future seulement lorsque sa période commence ; fin exclusive. Le statut effectif de la base et la suspension administrative restent prioritaires. Un droit conservé en base après expiration explique les usages passés, sans ouvrir un nouvel usage.

| Origine | Date de fin et quota par défaut |
| --- | --- |
| Acheté | Fin de la souscription en cours ; prix proratisé ; chasse proratisée arrondie au supérieur ; Push 5 dans le premier mois incomplet |
| Inclus | Conditions et dates acquises de la période de base |
| Essai | 14 jours par défaut, ajustables par Localeo, toujours subordonnés à la base ; chasse 1, Push 1 **au total** sans reset de mois, import sans quota |
| Offert | Fin de base ou date plus courte choisie ; chasse 5 par année offerte au prorata arrondi au supérieur ; Push 5/mois y compris premier incomplet ; import sans quota |

L'opérateur peut ajuster les quotas d'essai/cadeau à l'octroi et les modifier avec motif ; la version précédente et les usages restent conservés. Aucun renouvellement automatique d'essai, aucune conversion silencieuse en achat. Le cadeau/essai ne réactive pas la base ; les dates qui dépasseraient la couverture autorisée sont bornées ou refusées avec valeur corrigée proposée avant confirmation, pas rectifiées invisiblement après validation.

### Prorata, dates et montants

La précision suivante est un choix de conception pour concrétiser le prorata accepté : calendrier civil Europe/Paris, périodes annuelles en mois calendaires, conversion en UTC pour stockage des instants. Les dates d'échéance historiques E47 sont inclusives ; leur conversion cible conserve leur dernier jour autorisé et produit `fin_exclusive` à minuit Paris le lendemain. Aucune migration ne retire une journée existante. Les nouvelles périodes sont `[debut, fin_exclusive)` et n'ont pas de jour de chevauchement au renouvellement.

Pour une période annuelle, définir douze segments mensuels anniversaires avec bornes obtenues par le calcul calendaire existant (jour borné à la fin du mois). Chaque segment vaut 1/12. Le temps restant est la somme des mois entiers restants plus la fraction de jours civils du segment courant, divisée par 12. À une frontière mensuelle, 6 mois restants valent exactement 1/2 et 3 mois 1/4, conformément aux exemples retenus ; les années bissextiles et fins de mois sont testées. Le devis affiche date d'effet retenue, fin exclusive et fraction exacte rationnelle ; activation et expiration utilisent les mêmes bornes.

`prix_module_ht = HALF_UP(prix_annuel_ht_centimes × fraction_restante)` ; `quota_chasse = CEIL(quota_annuel × fraction_restante)` pour une fraction positive, zéro à échéance. Calcul rationnel/Decimal, jamais float. Calcul TVA réutilise la politique financière existante ; le taux vient de la configuration fiscale applicable au devis et est figé, jamais d'un champ libre côté client. Arrondir le prix HT une fois, puis TVA selon la convention existante. Exemple à six mois : 9 500 centimes HT et 3 chasses ; import 2 450 HT et aucun compteur ; Push 2 450 HT et 5 campagnes disponibles pour le mois courant.

Un devis est immuable et daté. Un changement de jour/date d'effet, d'échéance, de version ou de droit rend nécessaire un nouveau devis **avant** la création d'un Checkout. Une commande payée conserve son prix et son quota acceptés : ne pas les recalculer au retour du fournisseur. Si le paiement arrive trop tard pour activer les conditions acceptées (base expirée, commande remplacée ou annulée), classer `A_RAPPROCHER`, ne pas prolonger la base et ne pas ouvrir un nouveau droit ; Localeo traite rapprochement ou remboursement selon le circuit manuel. La durée de réservation du devis/Checkout est un paramètre technique, rendue par `expires_at`, et non un nouveau délai commercial garanti.

Pour un cadeau couvrant moins d'un an, appliquer la même mesure calendaire à la durée offerte, plafonnée à la couverture de base, puis arrondir le quota de chasse au supérieur. Pour une montée en gamme, le complément est le différentiel HT entre conditions de l'offre cible et conditions courantes acquises, sur le temps restant ; devis non négatif. Une offre dont les droits/quotas ne forment pas une montée en gamme ne bénéficie pas de cette action immédiate : présenter le changement au renouvellement. Les consommations du même terme restent déduites.

## 4. Compteurs, chevauchements et continuité

### Journal de consommation commun

L'usage est un fait unique `ConsommationUsage` : organisation, commune, période de base, unité, ressource source (`animation_id` ou `campagne_id`), instant, droit/conditions utilisés, clé d'idempotence, état et éventuelle correction liée. Un index unique sur `(unite, ressource_source_id, type_consommation)` empêche le double débit API/worker ; la période est enregistrée au moment du démarrage, pas recalculée lors d'une reprise après minuit ou renouvellement.

Les compteurs sont des projections sous verrou, reconstructibles depuis ce journal. Verrouillage ordonné : périmètre de souscription → compteur d'unité/période → ressource métier. Évaluer droit, disponibilité, effectuer débit et transition métier dans une même UoW ; échec = aucun débit et aucune publication/envoi. Deux publications avec un dernier crédit donnent exactement un succès. Deux canaux d'entrée ne disposent pas de compteurs séparés.

Ces compteurs de décision sont mis à jour synchroniquement avec le journal dans la même transaction ; ils ne sont pas les projections différées du tableau de bord. La frontière `CompteUsage` contrôle débit et correction pour l'unité/fenêtre concernée. Un écart compteur/journal bloque la commande et appelle une reconstruction contrôlée ; ne pas autoriser un usage depuis une valeur analytique potentiellement ancienne.

Les fenêtres de quota sont explicites : terme de base pour les animations/chasses, mois civil Paris pour le Push acheté/inclus/offert, fenêtre totale de l'essai en plus du mois pour le Push d'essai. **Aucun compteur n'est indexé seulement par l'identifiant du cadeau ou de la commande** : ajouter un deuxième octroi ne remet pas la consommation à zéro.

À usage et fenêtre comparables, le plafond est le maximum des limites actives, jamais leur somme. Tout usage consomme une fois le journal partagé, y compris lorsqu'un essai ou un cadeau l'a autorisé. Un changement de source, un second achat ou la fin d'un essai conserve ce journal ; si le plafond retombe sous les consommations déjà réalisées, le disponible devient zéro sans annuler les usages engagés.

Pour les périodes différentes, ne pas convertir « un essai total » en quota mensuel : chaque campagne commencée pendant l'essai apparaît dans son compteur de durée totale, et dans le compteur du mois commun. L'autorisation doit satisfaire le plafond mensuel disponible d'au moins un droit actif et, lorsqu'elle dépend de l'essai, son plafond total. Les campagnes effectuées sous un autre droit pendant la même fenêtre d'essai comptent aussi dans cette borne, pour ne pas contourner un plafond en changeant de provenance. Un essai accordé après épuisement d'un droit mensuel ne recharge pas ce mois : le journal partagé conserve les usages, et le plafond le plus élevé applicable à ce mois reste la borne. Même logique pour la chasse dans le terme. Renouveler ouvre un nouveau terme ou mois, sans report de reliquat.

| Scénario obligatoire | Résultat attendu |
| --- | --- |
| Essai chasse 1 consommée, achat chasse 5 sur le même terme | 4 disponibles, jamais 5 supplémentaires ; si achat proratisé à 3, 2 disponibles |
| Cadeau chasse 3 + achat chasse 5 | Plafond 5, pas 8 ; journal commun |
| Essai chasse porté à 8 avec 6 utilisées, achat actif plafonné à 5, puis fin d'essai | Achat toujours actif, disponible 0 ; les 6 animations publiées finissent |
| Push essai 1 commencé le 31, essai encore actif le 1er | Aucun nouveau crédit d'essai ; un droit mensuel acheté actif possède son nouveau plafond mensuel propre |
| Push acheté 5 et essai 1 simultanés, cinq campagnes du mois déjà commencées | Sixième refusée ; l'essai n'est pas un crédit additionnel |
| Campagne démarrée le 31, reprise technique le 1er | Toujours un seul débit sur le mois du démarrage |

Les libérations de quota d'annulation restent des corrections de journal liées à l'usage initial, aux conditions d'annulation de l'animation et au terme initial. Aucun crédit ne migre au nouveau terme. Une demande de préparation de chasse, un brouillon, une relance de préparation ou une duplication ne consomme pas un crédit commercial de publication ; les protections techniques de génération sont distinctes et restent visibles.

### Expiration commerciale et retrait

| Opération | Engagement qui ouvre la continuité | Après expiration/retrait commercial |
| --- | --- | --- |
| Animation/chasse | Animation déjà publiée et droits enregistrés à publication | Finir participations, clôture, tirage, contact et remise des lots selon validité ; pas de nouvelles créations/publications utilisant le droit expiré |
| Import | Plan confirmé **et traitement lancé** | Terminer les lignes figées, reprendre échecs techniques du même lot ; pas de nouveau fichier, nouveau plan ou ligne ajoutée |
| Campagne | Début effectif d'envoi enregistré et audience figée | Terminer/reprendre les destinataires déjà figés, en revérifiant autorisations ; aucune extension d'audience |
| Campagne programmée non commencée | Aucune continuité acquise | Suspendre ; après renouvellement, confirmation explicite, nouvel aperçu et nouveaux contrôles |
| Historique | Dossier autorisé | Consultation/export conservés selon droits et conservation ; aucune restauration de droit d'écriture |

La fin de base applique ces règles même si un module a une date mal alignée. Retrait commercial anticipé = même continuité. Suspension administrative de l'organisation/compte = refus prioritaire, pas de passe-droit de continuité. Retrait d'autorisation du collaborateur : tâches non commencées suspendues ; un autre acteur actuellement habilité peut les reprendre explicitement. Les opérations engagées se poursuivent sous contrôle technique borné ; le collaborateur révoqué ne peut plus les consulter ou piloter hors ses droits restants.

## 5. Achat, renouvellement, facturation et remboursement

Parcours portail : choisir commune → voir forfait/modules et prérequis → demander devis → récapituler dates/conditions → confirmer → paiement → état serveur « En attente de confirmation », « Actif » ou « À rapprocher ». Le retour Checkout ne déclenche pas une activation locale. En cas de délai réseau, le client consulte la commande avec sa clé initiale ; il ne crée pas un second achat automatiquement.

La ligne de commande porte `nature` (`SOUSCRIPTION`, `MODULE`, `COMPLEMENT_FORFAIT`), souscription/période cible, version de conditions, montant HT/TVA/TTC, fraction, quota et dates acquis. Les tables E47 peuvent être étendues par des lignes typées ; ne pas présenter un module comme un achat de lot Coffrets. Le paiement passe par le port existant, avec une clé fournisseur stable dérivée de la commande ; les événements fournisseurs reçus sont enregistrés et rapprochés une fois.

États cibles : `BROUILLON → EN_ATTENTE_PAIEMENT → PAIEMENT_EN_COURS → PAYEE → ACTIVATION_EN_COURS → ACTIVE` ; branches `ANNULEE`, `EXPIREE`, `A_RAPPROCHER`, `ECHEC_ACTIVATION_REPRENABLE`. Les états de l'ancienne commande E47 restent compatibles par mapping explicite ; une projection `ACTIVE` peut résulter de sous-lignes toutes activées plutôt qu'un remplacement immédiat de ses valeurs persistées. Facture/notification/outbox ont leur propre état : échec email n'annule pas un droit payé. `PAIEMENT_CONFIRME` et émission de droit s'appuient sur une preuve serveur, jamais sur un paramètre de retour.

Renouvellement : avant échéance, nouvelle période à la fin exclusive de l'actuelle ; après expiration, nouvelle période à la réactivation confirmée, sans rétrofacturer l'interruption. Préremplir seulement les modules précédemment achetés ; permettre de les retirer, présenter les nouvelles conditions et obtenir confirmation. Ne pas cocher un cadeau/essai en achat. Une période future payée n'est pas un abonnement ACTIF concurrent : elle devient active à son début, sous verrou tenant, en clôturant l'ancienne période effective. Préserver l'unicité SQL du courant.

Montée en gamme : devis du complément proratisé, effet après paiement, même échéance et mêmes consommations ; pas de cumul de deux plafonds de forfait. Baisse : applicable au renouvellement confirmé. Arrêt : jusqu'à fin payée, pas de prélèvement de renouvellement implicite, pas de remboursement automatique. Les factures, avoirs et échéances documentaires suivent leurs propriétaires existants. Les coordonnées de facturation courantes peuvent changer pour le prochain document ; un instantané émis ne se réécrit pas.

Remboursement : demande client → décision interne motivée `REFUSEE` ou `APPROUVEE` avec montant → exécution fournisseur → `CONFIRMEE` / `ECHEC_REPRENABLE` / `A_RAPPROCHER`. Plafond = encaissements confirmés de la commande moins remboursements confirmés **et montants déjà réservés par des remboursements approuvés/en cours** ; vérifier sous verrou pour que deux opérateurs ne remboursent pas deux fois. Un succès fournisseur sans réponse locale est rapproché avec la même clé ; pas de seconde émission. Le retrait du droit est une décision commerciale explicite associée, avec continuité ; ne pas déduire automatiquement d'un remboursement partiel une durée ou un quota nouveaux. La pièce rectificative n'est produite que par le parcours financier autorisé.

Le propriétaire de ce plafond est la racine `CommandeCommerciale` de `abonnements_plateforme`, avec une politique pure de disponible remboursable. Elle détient les faits d'encaissement rapprochés et les décisions/réservations de remboursement de cette commande ; elle ne calcule pas depuis un statut de facture ni un appel Stripe en cours. L'application enregistre approbation, montant réservé, version, audit et intention d'exécution dans une même UoW sous verrou commande. La confirmation fournisseur identifiée transforme une réservation en remboursement confirmé, sans la soustraire deux fois. Un résultat inconnu conserve la réservation ; seule une décision de rapprochement ou un échec définitif attesté permet sa libération. Les reprises gardent la même référence fournisseur et d'idempotence.

Le port de paiement transmet des faits typés (référence externe, commande, devise, montant, état confirmé) après vérification de provenance ; la politique du domaine décide de leur application et déduplique les confirmations. Le circuit documentaire financier reçoit la décision confirmée pour émettre l'avoir, sans posséder une seconde politique de plafond. Cette règle est une extension E73 à implémenter, pas un service de remboursement E47 déjà disponible. Le [guide des domaines](../../architecture/transverse/domaines-fonctionnels.md) distingue les commandes de souscriptions/modules des achats Coffrets de `gestion_achats`.

## 6. Import opérationnel de commerçants

### Écran et fichier

Parcours : commune/souscription → modèle ou fichier → choix de feuille XLSX → association des colonnes → aperçu → résolution → confirmation des lignes valides → progression → rapport/reprise. Présenter séparément créations, mises à jour, inchangés, conflits, erreurs et corrections sensibles en attente Localeo. Aucun bouton d'activation de commerce n'est ajouté au portail organisateur.

Formats V1 : `.xlsx` et CSV, **100 lignes de données maximum** et **2 Mo = 2 000 000 octets maximum** par fichier. En-tête exclu du décompte, toutes lignes de données sélectionnées incluses même invalides ; lignes entièrement vides ignorées. Un classeur à plusieurs feuilles demande un choix, pas d'import silencieux de toutes les feuilles. CSV UTF-8 avec détection contrôlée de séparateur et aperçu ; SIRET/commune/codes conservés comme chaînes. Fichier trop grand ou dépassant 100 lignes : refus avant écriture de fiche, sans troncature à 100. Un fichier XLSX est une archive : limites de décompression, nombre de cellules et temps de lecture techniques indépendantes, refus explicite si dépassées. Aucune macro, formule, lien externe ou contenu HTML exécuté ; une formule dans un champ importable est signalée, pas évaluée. Les CSV de rapport neutralisent les cellules interprétables comme formule par un tableur.

| Champ | Règle |
| --- | --- |
| Nom commercial | Obligatoire, texte nettoyé, pas un identifiant |
| Adresse | Obligatoire ; mapping lignes/code postal séparés possible, aperçu de la valeur complète ; pas de géocodage certifiant implicitement l'identité |
| Commune | Obligatoire, correspondance au référentiel et à la commune autorisée ; homonyme à résoudre, aucune nouvelle commune créée automatiquement |
| SIRET | Obligatoire, chaîne de 14 chiffres validée par le validateur de référence ; ne remplace pas le rapprochement primaire email |
| Email de contact | Obligatoire, syntaxe validée et normalisation commune trim/casse selon la politique Email existante ; pas de transformation Gmail ou de fusion d'alias |
| Nom du contact, téléphone, catégorie d'activité, description, site web | Facultatifs ; catégorie rapprochée au référentiel, jamais inventée ; téléphone/site validés s'ils présents ; site HTTP(S), sans visite automatique |

La catégorie facultative révèle un écart réel avec `ReferencerCommercant` actuel : E73 doit permettre une fiche BROUILLON de préparation sans catégorie validée, ou conserver une fiche d'import à vérifier jusqu'à complétion, présentée comme telle. **Cible retenue pour l'implémentation : fiche de préparation Référencement avec catégorie nullable tant qu'à vérifier**, puis exigence existante lors du référencement effectif. Adapter entité, repository, projection et tests en conséquence ; ne pas choisir une catégorie factice qui rendrait le commerce publiable. Le SIRET se rattache au champ d'identité légal du dossier, avec état non vérifié à la création.

### Rapprochement et protection du tenant

1. Réutiliser un lien de provenance validé pour le même flux source et la même fiche ; il stabilise les réimports malgré un déplacement de ligne. Revalider email/SIRET proposés et droits, ne pas traiter ce lien comme un droit de mutation.
2. Sans lien fiable, rechercher principalement l'email de contact normalisé parmi les fiches visibles et autorisées. Une correspondance unique cohérente avec le SIRET devient une proposition de mise à jour, jamais une acceptation de participation.
3. Plusieurs commerces avec cet email, email égal/SIRET différent, deux lignes visant la même fiche, email différent/SIRET déjà connu : conflit explicite. Ne pas appliquer « dernière ligne gagne ». Un résultat d'une autre organisation non autorisée affiche seulement « vérification Localeo nécessaire », sans nom ni coordonnées.
4. Aucun rapprochement certain : proposer une création à vérifier ; recontrôler unicité et doublons au commit. Les contrôles globaux existants de référencement ne sont pas contournés : un conflit global non visible devient une ligne écartée à traiter par Localeo, pas une fusion automatique.
5. Changement de SIRET ou de commune d'une fiche existante : demande de correction ERP liée à la ligne. La résolution d'identité dans l'aperçu ne donne pas le pouvoir de l'appliquer. Si cette correction conditionne le choix de fiche, la ligne reste en attente ; les autres lignes indépendantes peuvent être confirmées.

Le flux source a un identifiant stable propre à l'organisation/commune, distinct du nom du fichier. Empreinte fichier, mapping versionné, références de lignes et décisions de rapprochement composent la provenance. Les lignes absentes d'un nouvel import ne suppriment ni ne désactivent aucune fiche. Les données de suivi restent distinctes des prospects E71. Un email de contact modifié n'altère ni login commerçant, ni mot de passe, ni rattachement salarié : ces actions restent dans Identité/Accès et OnBoard.

### Comparaison à trois versions

Pour chaque champ, conserver `S` dernière valeur source reconnue, `L` valeur Localeo actuelle et `N` nouvelle valeur source, plus version fiche, version source et décision de protection locale. Normaliser les valeurs avec la même règle pour comparaison, conserver la valeur source d'affichage.

| Situation | Proposition d'aperçu |
| --- | --- |
| N vide | Conserver L, jamais effacer ; ne pas remplacer S par une suppression implicite |
| N = S | Aucun changement source ; conserver L même si L a été corrigé localement |
| L = S et N différent | Modification applicable après confirmation |
| L = N | Déjà convergé ; reconnaître N comme référence source sans réécrire le champ |
| L différent de S et N différent de S et de L | Conflit : garder Localeo ou accepter fichier, explicitement par champ |
| Première association sans S et L renseigné différent de N | Conflit initial, pas d'hypothèse « Localeo non modifié » |

Lorsqu'un opérateur conserve une correction locale contre une nouvelle source, enregistrer N comme nouvelle référence source **et** la protection/valeur locale retenue : un mois identique ne repose pas le même conflit et ne rétablit pas N. La protection locale disparaît seulement par convergence ou décision explicite ultérieure. Aucun patch `null` issu d'une cellule vide n'est émis.

L'aperçu renvoie un `plan_version`, l'empreinte du mapping/fichier et la version de chaque fiche. À confirmation puis dans chaque transaction de ligne, recontrôler versions/provenance/droits. Modification locale après aperçu → `CONFLIT_VERSION`, ligne suspendue et aperçu recalculé ; pas d'écrasement silencieux. Verrouiller flux/provenance puis fiche dans un ordre déterministe. Deux fichiers du même flux ne font pas avancer concurremment la référence S ; reprise du premier avant confirmation du second ou refus `IMPORT_SOURCE_OCCUPEE`.

### Traitement, reprise et conservation

États du lot : `DEPOSE → A_CONFIGURER → PREVISUALISE → CONFIRME → EN_COURS → TERMINE / TERMINE_PARTIEL`, avec `SUSPENDU`, `ECHEC_TECHNIQUE_REPRENABLE`, `ABANDONNE`. La confirmation ne vaut pas lancement : le worker enregistre un jeton d'engagement au premier claim après vérification du droit actif. S'il expire entre confirmation et claim, suspendre sans traiter. Une fois lancé, seules les lignes du plan confirmé sont autorisées à finir après expiration commerciale.

Chaque ligne = transaction indivisible fiche + provenance + demande Animation/dossier à vérifier + résultat/audit. Succès conservé en cas d'erreur d'une autre ligne. Clé unique `(import_id, ligne_id, revision_plan)` et identifiant métier créé enregistré empêchent doublon à la reprise. Une erreur métier ne boucle pas en retry : résolution et nouveau plan exigés. Une reprise technique du même plan ignore les succès. Un collaborateur révoqué ne relance pas ; un responsable/habilité peut reprendre l'opération engagée, sans ajouter de nouveaux usages.

Création : fiche **à vérifier**, demande Animation soumise à Localeo ERP, aucun identifiant actif, invitation, scope actif, contrat accepté ou participation créée automatiquement. Les effets involontaires de l'actuel `ReferencerCommercant` sont testés avec `initialiser_acces=False` et un faux transport d'email ; l'import ne génère pas d'email commerçant.

Fichiers et rapports privés, téléchargements authentifiés avec droits revérifiés, aucune URL publique persistante. Les artefacts sont supprimés 30 jours après la fin ou l'abandon ; une reprise technique qui n'est pas terminale ne déclenche pas ce délai. Les fiches/provenances/audits ne sont pas supprimés avec le fichier. Leur rattachement aux politiques existantes figure dans la matrice de conservation de livraison ; sauvegardes, gels et purge ne se traitent pas par suppression locale opportuniste. L'expiration du module ne supprime pas les fiches ni leur historique.

## 7. Messages organisateur, Live et Web Push

### Parcours et états de campagne

Écran : animation → Communication → nouveau message → titre/texte/lien interne autorisé → groupe → aperçu du nombre ciblé/autorisé/exclu → envoi immédiat ou date/heure Paris → confirmation → progression et rapport. Afficher distinctement messages disponibles dans Live, Push remis au service, erreurs et exclus ; jamais « lus » à partir d'un accusé transport. Pas de champs email/SMS de secours.

`CampagneOrganisateur` appartient à une animation/commune/organisation : titre, corps texte, deep link validé, groupe (`TOUS`, `PARCOURS_NON_TERMINE`, `PARCOURS_TERMINE`, `GAGNANTS`), instant programmé UTC + zone d'affichage Paris, créateur, version, approbateur, états, audience figée, instant de démarrage et consommation associée. Texte échappé et longueur bornée par schéma ; liens limités à des parcours internes autorisés sans token transmis au suivi public.

États : `BROUILLON → PROGRAMMEE / PRETE → EN_COURS → TERMINEE / TERMINEE_PARTIELLE`; branches `ANNULEE_AVANT_DEMARRAGE`, `SUSPENDUE_DROIT`, `SUSPENDUE_QUOTA`, `SUSPENDUE_HABILITATION`, `HORS_FENETRE`, `SANS_DESTINATAIRE`, `ECHEC_REPRENABLE`. Le contenu/groupe peut changer avant démarrage avec nouvelle version/confirmation ; aucun ajout de destinataire après démarrage. Une annulation avant départ ne consomme rien. Une suspension nécessite confirmation active après nouvel aperçu, jamais envoi tardif automatique au premier jour du mois ou au renouvellement.

Les groupes se calculent depuis les états du moteur et les attributions confirmées, non depuis des compteurs frontends. Les quatre groupes sont dans **une seule animation** ; le module n'ouvre ni prospection ni audiences publicitaires. La fenêtre est publication effective jusqu'à clôture effective + 30 jours ; instant de départ revérifié, pas seulement date de programmation. Un changement de date de clôture invalidant la programmation est visible avant départ.

### Autorisation du participant et identité de fréquence

Conditions cumulatives pour créer un message : participation réelle dans l'animation et groupe, autorisation messages organisateur applicable à cette participation, droit de lecture personnel encore valable, limites de sollicitation. La permission navigateur ne donne pas le consentement aux messages organisateur ; suivre une commune n'en donne aucun non plus. Les notifications automatiques et préférences correspondantes conservent leurs règles indépendantes.

Le champ actuel `consentement_notifications` et la catégorie Live `ANIMATION` ne doivent pas être réinterprétés silencieusement comme un nouveau consentement organisateur plus large. Ajouter une préférence explicite organisateur avec version de texte/date/source/retrait ; reprendre seulement les consentements anciens dont le périmètre couvre réellement cet usage, sur preuve de version. Sinon proposer un choix facultatif dans le parcours personnel, sans bloquer participation ni messages automatiques. Le défaut d'autorisation exclut du nouveau module.

La fréquence commune utilise un identifiant technique de destinataire stable dérivé de l'identité de participation normalisée déjà utilisée par le moteur (email normalisé), cloisonné par commune. Enregistrement pseudonymisé côté serveur, non exposé au client ni utilisé comme droit de consultation. Plusieurs participations du même email dans une commune partagent la borne ; deux personnes ayant des emails distincts sur une même installation gardent leurs propres bornes. Les installations servent au transport/lecture, pas à contourner la limite. Un email modifié avec autorisation conserve le lien d'identité pour ne pas réinitialiser le délai ; aucune fusion de comptes n'en découle.

À défaut d'installation Live actuellement liée, conserver le message personnel autorisé lié à la participation pour le rendre disponible dans son parcours Live lors d'une liaison ultérieure autorisée. Ne pas chercher un appareil au seul email et ne pas transmettre un token de participation dans un Push public. Une personne sans permission navigateur reçoit le message dans Live ; aucun fallback email/SMS. Si plusieurs installations autorisées voient le même message, il reste **un message métier** et un débit de fréquence, avec références de diffusion distinctes par installation.

### Démarrage atomique, traitement borné et transports

La racine `CampagneOrganisateur` porte son état, sa version, le contenu figé et la référence d'audience scellée ; elle ne contient pas tous les messages. La racine `SollicitationDestinataire`, identifiée par commune et identité de destinataire, protège la fréquence interanimations. Audience, opérations destinataires et messages sont persistés séparément avec unicités ; aucune transaction ne verrouille toute l'audience ni ne crée tous ses messages.

1. Acquérir un bail technique dans une transaction courte **déjà commitée** avant les verrous métier. Le jeton de bail interdit les écritures d'un worker obsolète ; il ne vaut ni début de campagne, ni droit, ni débit. Recharger les droits de l'initiateur et le contexte avant préparation et avant démarrage effectif.
2. Matérialiser une sélection cohérente des participants cibles avec une date/version de sélection, puis la sceller. Le repository fournit une capture cohérente des IDs et critères à cet instant, jamais une pagination changeante pouvant oublier ou ajouter des participants au fil du traitement. La préparation est reprenable par lots bornés, ne crée aucun message et ne consomme aucun quota. Une capture incomplète ne permet pas de démarrer ; les autorisations actuelles seront revérifiées, même si elles étaient valables lors de la capture. L'audience scellée forme la limite supérieure du traitement et n'est pas élargie à la reprise.
3. Traiter les candidats de cette audience par transactions unitaires, avec une taille de lot de lecture technique bornée. Sous les verrous dans l'ordre souscription/compteur → animation/campagne → garde destinataire, vérifier bail/version, fenêtre d'envoi, droit courant et préférences. Compter la tentative distincte pour un destinataire autorisé, y compris si la fréquence l'exclut. Évaluer `[maintenant − 24 h, maintenant)` en UTC ; à la limite, exclure sans envoi différé. Une exclusion ne débite pas le quota de campagne.
4. Au **premier message accepté**, enregistrer atomiquement début effectif, engagement limité à l'audience scellée, débit unique dans le mois de ce début, consommation de fréquence, message Live et intention de transport. Aucun effet externe avant commit. Si droit/quota indisponible, suspendre sans message ni débit, selon les règles de reconfirmation. Si tous les candidats sont exclus, terminer `SANS_DESTINATAIRE` sans débit ; les tentatives/exclusions restent disponibles dans le rapport. Une préparation interrompue n'acquiert pas la continuité commerciale réservée aux campagnes commencées.
5. Après ce début, traiter chaque destinataire restant par une transaction courte : vérifier engagement/suspension, autorisation et fréquence courantes, puis inscrire tentative/exclusion ou message + fréquence + outbox ensemble. Aucun nouveau débit de campagne, aucun destinataire ajouté. La fin commerciale du module permet cette continuation bornée ; elle ne redonne pas de pouvoir au collaborateur révoqué. Les messages déjà commités restent acquis si une transaction ultérieure échoue. Une reprise cible uniquement les opérations non terminales, sans prolonger une campagne en réessayant les exclusions de fréquence.
6. Juste avant transport, revérifier autorisation du destinataire et de l'installation ; une révocation peut encore empêcher cette diffusion. Déduplication `(campagne_id, participant_id, installation_id, canal)` ; échec Push ne supprime pas Live. Réutiliser claims, expiration de bail, retries bornés et invalidation des endpoints définitivement invalides. Absence d'accusé final = état incertain, pas seconde campagne. La fin du traitement est calculée depuis les opérations terminales, sans reprendre toute l'audience sous verrou.

L'implémentation doit fixer et éprouver une borne de lot technique et le mécanisme de capture cohérente sur un volume représentatif ; cela ne crée pas de plafond commercial de participants. L'arrêt pendant la capture, après le premier message ou au milieu de l'audience doit être récupérable. Les transactions de reprise suivent le même ordre de verrous que le premier démarrage ; aucun bail technique ne conserve un verrou de campagne avant d'acquérir celui du compteur.

Après le premier message, la continuation n'acquiert plus le verrou exclusif du compteur ou de la souscription pour un débit inexistant. Les contrôles de suspension restent courants et cohérents au commit, via faits/révisions transactionnels ; campagne/opération destinataire et garde communal portent les seules mutations nécessaires. Séparer débit de quota et fréquence, limiter la concurrence et mesurer la contention sur une campagne très volumineuse. Les workers lisent initialement au plus 100 tâches/candidats par lot, paramètre technique à calibrer avec borne validée ; chaque transaction de message reste unitaire. Les recherches d'échéances et de fréquence utilisent les accès/index de la [matrice de performance](architecture-contrats.md), sans charger toutes les installations ou tout le journal.

Le transport Web Push ne garantit pas une livraison exactement une fois à l'appareil ; l'unicité garantie porte sur commande métier, outbox, débit et message Live. Fournir un identifiant/tag stable au service worker pour remplacer une notification répétée du même message plutôt qu'en créer une nouvelle. Une reprise ne modifie pas le quota et n'ajoute pas une deuxième tentative de campagne.

### Limites et alertes Ops

Politique par commune/souscription : limite initiale `1` message par participant sur 24 h, entier strictement positif configurable ; multiplicateur de seuil initial `3`, configurable par Localeo. En cas de plusieurs souscriptions qui couvriraient une même commune/destinataire, le garde de fréquence reste communal et ne peut être doublé en changeant de gestionnaire/organisation ; une politique effective unique de commune est nécessaire et référencée par les souscriptions. Les organisations voient uniquement leur propre rapport.

Une tentative unique `(campagne_id, destinataire_communal)` est inscrite même si la fréquence bloque. Dès `nombre_campagnes_distinctes_24h >= multiplicateur × limite_effective`, ouvrir/enrichir une alerte Ops regroupée par commune/souscription ; le premier franchissement enfile un email interne aux destinataires configurés. Les autres personnes ou tentatives enrichissent la même alerte ouverte, sans email par participant. Une clôture d'alerte n'efface pas les compteurs ni ne remet le plafond à zéro. Changement de configuration tracé avec motif et version ; il ne déclenche pas l'envoi de messages précédemment exclus.

Rapport organisateur : volumes ciblés, autorisés, messages Live créés, exclus fréquence/préférences, Push sans abonnement/envoyés/échec, état technique et possibilité de reprise. Aucun email de participant ni endpoint navigateur dans l'agrégat commercial ou les alertes usuelles. Les détails personnels éventuels exigent un droit d'exploitation spécifique. Les tableaux de coûts ne déduisent pas une livraison ni une lecture de la présence dans l'outbox.

## 8. Suivi économique et budgets

Le client voit ses usages, limites, disponibilité et documents facturés ; **jamais coûts internes ou marges**, y compris dans JSON caché par l'interface, export, rapport de campagne ou message d'erreur.

| Poste | Mesure et source cible | Valorisation |
| --- | --- | --- |
| Emails | Identifiant d'email sortant, type, état/instant confirmé ; source métier rattachée | Coût constaté fournisseur si rapproché, sinon tarif unitaire versionné estimé |
| SMS | SMS sortant et preuve fournisseur/segments lorsqu'ils sont disponibles | Ne pas confondre message demandé et segments facturés ; couverture explicite |
| Préparation de chasse | Demande/génération existante et prestation humaine saisie, unités séparées | Coût externe constaté ou temps × tarif interne estimé, sans compter deux fois le même travail |
| Stockage | Mesure d'octets-jours par stockage privé/public, provenance locataire si disponible | Tarif daté estimé ou facture rapprochée ; résiduel non ventilable visible |
| Web Push | Diffusions par transport et résultat, compteur campagne séparé | Coût fournisseur constaté, tarif estimé ou « indisponible » ; gratuité supposée interdite |
| Support | Temps saisi par intervenant lié à demande, révision/correction tracée | Coût réel fourni ou estimation tarif interne ; pas de déduction du délai d'attente |

`MesureUsage` est append-only avec clé unique producteur/événement/unité et dimensions organisation, commune, période, souscription, module lorsque connues. `ValorisationCoût` référence mesure, devise, montant, nature `CONSTATE`/`ESTIME`/`INDISPONIBLE`, tarif/source et version. Une valeur indisponible n'est pas zéro. Une réconciliation remplace l'estimation active d'une même mesure par le constat sans les additionner ; garder les révisions et différences explicables. Les totaux d'organisation comprennent une rubrique « non ventilé » ; ne pas répartir arbitrairement sur les communes. Les factures de plateforme et revenus restent des sources différentes des coûts.

Mois civil Europe/Paris, événements stockés UTC. Période de service et date de réception de la preuve séparées ; correction tardive révise le mois concerné avec `calcule_a` et couverture. Une marge n'est affichée comme fiable qu'avec coûts et revenus comparables, sinon « marge estimée »/« couverture incomplète » ; le portail client ne reçoit aucune de ces valeurs.

Budget : montant mensuel positif facultatif par organisation, devise EUR, auteur/date/motif et version ; sans budget, suivi actif sans alerte. Base de suivi = coûts constatés + estimations non remplacées, avec leur part explicitement affichée, jamais les indisponibles assimilés à zéro. Franchissements 80 % puis 100 % calculés sur cette base, étiquetés « estimation incluse » si besoin. Un saut direct au-delà de 100 % produit une alerte consolidée mentionnant les deux seuils, pas deux emails identiques. Déduplication organisation/mois/seuil/version de budget ; la modification ou correction enrichit l'alerte et la traçabilité, sans répéter un email à chaque recalcul. Les données manquantes restent visibles comme couverture incomplète même sous 80 %.

Aucune branche du use case de coût n'appelle retrait de droit, débit client, suspension, modification de quota ou changement d'offre. Ces dépendances sont interdites et couvertes par tests. Les destinataires internes et canaux Ops sont configurés par l'exploitation ; une panne d'alerte ne bloque pas un paiement, import, participation ou validation.

## 9. Contrats HTTP cibles

### Conventions communes

Les routes suivantes sont **nouvelles cibles**, pas une description d'OpenAPI actuel. Producteur backend, consommateurs portail Animation/ERP et Live. Conserver le contrat existant `GET /protected/animation-locale/abonnement`, en ajoutant les projections nécessaires de façon compatible ; les actions commerciales nouvelles appartiennent à Abonnements, l'import à Référencement, la campagne à Animation. Aucun nouveau token navigateur persistant. Session Animation en cookie + CSRF existants ; session ERP et autorisations dédiées côté interne.

Commandes : en-tête `Idempotency-Key` opaque, corps JSON `expected_version` pour toute ressource existante. Clé scindée par acteur/organisation/opération ; même clé et même empreinte → même résultat autorisé, même clé autre contenu → 409 `IDEMPOTENCE_CONFLIT`. Autorisation revérifiée avant de retourner un résultat mémorisé. Les écritures métier et reçu d'idempotence sont atomiques. Ressource périmètre différente → 404 ou refus sans fuite ; acteur non habilité à sa propre ressource → 403 `ACTION_INTERDITE`.

Réponse commune de commande : `{id, version, statut, operation_id?, actions_disponibles, ...resultat}` ; `201` création, `200` transition/rejeu, `202` traitement durable asynchrone. Erreurs : `{code, detail, correlationId, request_id, current_version?}` ; `current_version` seulement si ressource visible. Dates ISO8601 UTC, montants en centimes entiers, durées/zone explicites. `409 CONFLIT_VERSION` entraîne relecture et confirmation, jamais relance automatique d'une écriture.

Nouvelles listes : paramètres `limit` (25 par défaut, maximum 100) et `cursor` opaque lié aux filtres ; réponse `items`, `next_cursor`, `has_more`, tri stable par date puis ID, filtres de période/état et scope serveur. La pagination existante reste inchangée pour ses consommateurs. Le rapport technique peut paginer les lignes, sans exposer le fichier brut. Les opérations asynchrones possèdent un GET de ressource source avec progression/dernière erreur/reprise disponible ; pas de polling d'un identifiant de job hors tenant.

### Souscriptions et modules

Préfixe cible `P = /protected/abonnements-plateforme` ; `I = /internal/abonnements-plateforme`. Les routes internes utilisent les mêmes commandes métier que le portail et sont présentées dans l'ERP.

| Méthode et chemin | Entrée essentielle | Sortie / refus spécifique |
| --- | --- | --- |
| GET `P/catalogue?commune_id=...` | Commune autorisée | Versions commercialisables, conditions, prérequis ; aucune donnée de coûts |
| GET `P/souscriptions/{id}/modules` | Souscription autorisée | Droits acquis/sources/dates/quotas partagés et `actions_disponibles` |
| POST `P/souscriptions/{id}/devis` | `expected_version`, `nature: ACHAT_MODULES/RENOUVELLEMENT/MONTEE_GAMME`, `module_codes`, `offre_code?` | `devis_id`, version, dates, fraction, lignes figées et échéance devis ; 409 `BASE_INACTIVE`, `MODULE_DEJA_ACHETE`, `CHANGEMENT_NON_AUTORISE` |
| POST `P/devis/{id}/commander` | `expected_version`, `conditions_version`, `conditions_acceptees: true`, `facturation_version` | Commande durable, montant et état ; 409 `DEVIS_EXPIRE`/`CONDITIONS_MODIFIEES` |
| POST `P/commandes/{id}/checkout` | `expected_version` | Session de paiement ou opération en cours, jamais droit ; 409 `COMMANDE_NON_PAYABLE` |
| GET `P/commandes/{id}` | Identifiant autorisé | Paiement, activation et rapprochement, références documentaires |
| POST `P/souscriptions/{id}/arret` | `expected_version`, `motif` | Arrêt à échéance, continuité et date visibles |
| POST `P/commandes/{id}/demandes-remboursement` | `expected_version`, `motif` | Demande `A_EXAMINER`, aucun remboursement immédiat |
| PATCH `P/organisations/{id}/facturation` | `expected_version`, coordonnées courantes | Nouvelle version, `effet: FUTURS_DOCUMENTS` |
| POST `I/souscriptions/{id}/octrois-modules` | `expected_version`, module, `origine: OFFERT/ESSAI`, dates, limites, motif | Droit et plafond partagé résultant ; 422 `LIMITES_INVALIDES`, 409 `BASE_INACTIVE` |
| PATCH `I/octrois-modules/{id}` | `expected_version`, nouvelles dates/limites, motif | Nouvelle révision, usages inchangés |
| POST `I/droits-modules/{id}/retirer` | `expected_version`, motif | Retrait commercial avec liste de continuité |
| POST `I/catalogue/versions` | Version précédente, conditions, date de publication | Nouvelle version immuable ; administrateur uniquement |
| POST `I/remboursements/{id}/decider` | `expected_version`, `decision`, `montant_centimes?`, motif, `retrait_commercial_demande` | Réservation/exécution durable ; 409 `MONTANT_NON_REMBOURSABLE`, motif et décision tracés |

Exemple de devis de chasse à mi-période :

```json
{
  "devis_id": "uuid",
  "version": 1,
  "nature": "ACHAT_MODULES",
  "commune_id": "uuid",
  "fraction_restante": {"numerateur": 1, "denominateur": 2},
  "lignes": [{
    "module_code": "CHASSE_TRESOR",
    "catalogue_version": 1,
    "prix_annuel_ht_centimes": 19000,
    "montant_ht_centimes": 9500,
    "quota": {"unite": "PUBLICATION_CHASSE", "quantite": 3, "periode": "TERME_SOUSCRIPTION"}
  }],
  "devise": "EUR"
}
```

Le contrat réel inclut aussi les dates d'effet/fin, TVA/TTC, expiration et conditions acceptables ; l'exemple abrégé ne définit pas des champs optionnels.

### Imports

Préfixe `R = /protected/referencement/imports-commercants`. `POST R` multipart (`fichier`, `commune_id`, `flux_source_id?`) crée le lot et ne crée aucune fiche ; 413 `FICHIER_TROP_VOLUMINEUX`, 422 `FORMAT_NON_SUPPORTE`/`TROP_DE_LIGNES`. Retour `id, version, feuilles, colonnes, statut`.

| Route | Commande ou lecture |
| --- | --- |
| GET `R/modele?format=xlsx|csv` | Modèle sans données personnelles, cinq champs obligatoires/cinq facultatifs |
| PUT `R/{id}/mapping` | `expected_version`, feuille, ligne d'en-tête, mapping champ→colonne ; nouvelle version |
| POST `R/{id}/previsualiser` | `expected_version` ; construit plan/version et résultats paginés |
| GET `R/{id}` et `R/{id}/lignes` | État, progression, compteurs et décisions de champ ; valeurs autorisées seulement |
| POST `R/{id}/resolutions` | `expected_version`, `plan_version`, choix de rapprochement et `ligne_id/champ/choix: LOCALEO|SOURCE` ; corrections sensibles en attente Localeo |
| POST `R/{id}/confirmer` | `expected_version`, `plan_version`, `ligne_ids`, `accepter_import_partiel` ; 202, plan figé ; 409 `PLAN_OBSOLETE`, `CONFLITS_NON_RESOLUS`, `IMPORT_SOURCE_OCCUPEE` |
| POST `R/{id}/reprendre` | `expected_version` ; 202 même traitement uniquement lignes techniques restantes |
| POST `R/{id}/abandonner` | `expected_version`, motif ; terminal, conserve les succès et déclenche délai artefacts |
| GET `R/{id}/rapport` | Fichier privé après contrôle courant ; 410 `ARTEFACT_EXPIRE` après purge |

Les corrections SIRET/commune sont exposées dans l'ERP Référencement par une commande interne motivée avec `expected_version`, identifiant de demande/fiche et valeurs proposées. Leur décision est reçue comme événement du domaine ; l'import ne valide pas lui-même ces corrections. Une mutation locale pendant traitement produit un résultat de ligne `CONFLIT_VERSION` et une nouvelle résolution, pas un 500 retryable.

### Campagnes et messages

Préfixe `A = /protected/animation-locale/animations/{animation_id}/campagnes-organisateur`.

| Route | Contrat essentiel |
| --- | --- |
| GET/POST `A` | Lecture paginée / création `{titre, corps, groupe, deeplink?}`, version 1 |
| GET/PATCH `A/{id}` | Lecture / édition avant départ avec `expected_version` |
| POST `A/{id}/apercu` | `expected_version` ; volumes estimatifs, droits/quotas/fréquence, exclusions ; aucune réservation ni tentative |
| POST `A/{id}/programmer` | `expected_version`, `programmee_at` ISO8601 avec offset, `timezone: Europe/Paris`, confirmation ; valide les heures ambiguës/inexistantes explicitement |
| POST `A/{id}/envoyer` | `expected_version`, confirmation ; 202 durable, contrôles au démarrage |
| POST `A/{id}/reconfirmer` | `expected_version`, choix `IMMEDIAT` ou nouvel instant ; seulement après nouveau contrôle, sans reprendre anciennes exclusions |
| POST `A/{id}/annuler` | `expected_version` ; possible avant démarrage seulement |
| POST `A/{id}/reprendre` | `expected_version` ; reprise technique audience figée, pas un nouvel envoi |
| GET `A/{id}/rapport` | Compteurs et états par canal, incertitude transport visible |

Refus/états : `MODULE_NON_ACTIF`, `QUOTA_EPUISE`, `CAMPAGNE_HORS_FENETRE`, `CAMPAGNE_DEJA_COMMENCEE`, `HABILITATION_RETIREE`, `VERSION_AUDIENCE_OBSOLETE`. La fréquence est un motif d'exclusion de destinataire, pas un échec global de toutes les personnes. L'expiration après programmation est un état suspendu durable, pas une erreur perdue dans les logs.

Préférences/messages personnels : étendre le contrat Live/participation existant avec `messages_organisateur_autorises`, version/horodatage et messages liés à une participation prouvée. **Une installation seule ne peut modifier le consentement d'une participation qu'elle ne contrôle pas** : employer la preuve d'accès participant existante en plus de son secret d'installation lors du rattachement. Les schémas OpenAPI documentaires E41/E42, générateurs backend et imports consommateurs sont à actualiser ensemble lors de l'implémentation ; pas de copie documentaire présentée comme runtime.

Configuration interne : `PUT /internal/animation-locale/communes/{id}/politique-sollicitation` avec `expected_version`, `limite_24h`, `multiplicateur_alerte`, `motif` ; retour version effective et périmètre. Les pages Ops consomment les alertes internes existantes enrichies, sans route publique de destinataires.

### Coûts

`GET /internal/exploitation/couts-organisations/{id}?mois=YYYY-MM` retourne ventilation, niveau de fiabilité, couverture, date de calcul, budget et alertes. `PUT .../{id}/budget` accepte `expected_version, montant_centimes|null, devise, mois_effet, motif`. Les mesures/rapprochements passent par ports de collecte internes idempotents ; aucune route du portail client ne renvoie ces montants. Une projection publique au tenant `/protected/abonnements-plateforme/souscriptions/{id}/usages` ne contient que compteurs/quotas facturables et références de factures autorisées.

## 10. Persistance, migration et exploitation

Ajouter des migrations, ne pas modifier les SQL appliqués. Tables/ensembles cibles : versions de catalogue et instantanés, périodes de souscription, lignes commerciales modules, droits de module, consommations/compteurs, demandes/remboursements réservés, lots/lignes/provenances import, demandes de correction sensible, campagnes/audiences/messages, compteurs et tentatives de sollicitation, mesures/valorisations/budgets/alertes. Les noms physiques seront alignés au mapper existant ; les contraintes métier ci-dessus sont obligatoires.

Contraintes nécessaires : unicité droit par preuve d'origine ; unicité reçu idempotent par acteur/opération ; débit par ressource/unité ; ligne réussie par import/plan ; progression de provenance sérialisée ; message métier par campagne/participant ; diffusion par message/installation ; tentative par campagne/destinataire ; mesure par producteur/événement/unité ; réservation de remboursement sérialisée par commande. `version` entier monotone sur agrégats modifiables, FK incluant contexte tenant sur les ressources sensibles, index sur dates d'effet/expiration/claims.

Reprise E47 : capturer les conditions réellement acquises depuis les instantanés commerciaux et preuves existantes, comparer au catalogue et résoudre les cas sans preuve avec Localeo ; ne pas supposer que l'offre actuelle décrit une vente ancienne. Conserver les IDs et rattachements partenaires/communes ; pas de création d'organisations concurrentes. Les compteurs historiques sont importés dans leur unité et période, sans redébiter une chasse ancienne ni effacer sa consommation. Si les données ne distinguent pas de manière prouvée les droits chasse historiques, classer à contrôler avant bascule plutôt que facturer un supplément ou retirer l'accès.

Déploiement progressif : schéma additif → migration/dry-run des conditions et journaux → backend lecteurs compatibles → contrats/clients → activation pilote par commune après preuve. L'ancien consommateur continue ses lectures et activités acquises ; les nouvelles commandes restent fermées tant que leur producteur/permission/worker n'est pas prêt. Flags techniques ne remplacent pas les droits commerciaux. Après bascule des écritures d'un périmètre, une marche arrière bloque les nouveaux usages et conserve les journaux/effets déjà engagés ; pas de retour destructif aux compteurs anciens.

Workers : transitions d'expiration et activation future, rapprochement paiement/remboursement, traitement import, campagne due, diffusion Live/Push, purge d'artefacts et agrégation coût. Chaque worker possède claim, lease, idempotence, mode de simulation, compteur et erreur exploitable ; les retries techniques ne contournent ni une nouvelle version ni une décision métier. Les invitations d'équipe, participation, messages automatiques et emails de service sont hors quota organisateur.

Conservation : fichiers/rapports import 30 jours après terminal/abandon ; autres catégories (commerce/provenance, contrats/paiements/pièces, audits, messages Live/Push, coûts agrégés) rattachées aux politiques canoniques existantes avec mêmes gels et droits. Pour les messages organisateur, réutiliser la politique Live pour le contenu et définir dans la matrice de conservation la trace minimale de consentement/exclusion/compteur nécessaire à la preuve ; ne pas conserver les endpoints en clair dans l'audit de campagne. Aucun nouveau délai ne peut être choisi arbitrairement par un worker. La [vérification de livraison](verification-livraison.md) doit contrôler ces raccordements avant mise en service.

## 11. Preuves à produire et matrice locale de couverture

**Tests prévus, non exécutés par cette spécification.** Données synthétiques, fournisseurs simulés, bases jetables uniquement ; aucune notification, activation ou facture réelle pendant la recette automatisée.

| US / critères | Preuves de domaine, transaction et parcours attendues |
| --- | --- |
| US03 — CA-12/13/14 | Passeport/tombola inclus, chasse indépendante ; variantes sans supplément ; modification catalogue sans altération du droit historique ; catalogue masqué ne révoque pas une vente |
| US14 — CA-37 | Catalogue par commune et prérequis ; modes inclus/achat/cadeau/essai ; Admin seul modifie ; consommateurs ne déduisent pas le droit du prix affiché |
| US15 — CA-38 | Prorata à 6/3 mois exact, jours/février/année bissextile ; TVA/arrondis ; double clic/deux webhooks/retour sans webhook ; paiement tardif et activation en échec rapprochables ; aucun module avant confirmation |
| US16 — CA-39 | Octroi autorisé/motif, essais bornés, cadeaux bornés, aucun achat implicite ; collisions cadeaux/essais/achats sans addition ni remise à zéro |
| US17 — CA-40/41 | Expiration au bon instant sans attendre batch ; continuité ressource par ressource ; retrait commercial vs suspension ; retrait de collaborateur ; journal conservé après renouvellement et quotas sans report |
| US18 — CA-46 | Une chasse consomme uniquement son compteur à publication ; deux publications sur dernier crédit ; annulation/reprise ; préparation/relance pas de débit de publication ; anciennes chasses finissent après expiration |
| US19 — CA-42 | CSV/XLSX, 100/101 lignes, 2 Mo et dépassement, archive décompressée excessive, formules non exécutées ; mapping/category facultative/5 champs obligatoires ; aperçu sans écriture ; commune non autorisée refusée |
| US20 — CA-43/44/45 | Email primaire et ambiguïtés, source/Localeo/fichier trois versions, vide sans effacement, ligne partielle et reprise après crash commit ; modification concurrente depuis Pro/ERP ; SIRET/commune soumis Localeo ; aucune invitation/login/scope/participation ; expiration après vrai lancement seulement ; purge 30 jours sans fiche supprimée |
| US21 — CA-47/48 | Achat sans permission Communication refusé ; audience hors animation exclue ; consentement ancien non élargi ; quatre groupes ; message Live sans Push ; multiappareil et multi-animation même personne limités ; programmation Paris, quota au départ, fenêtre clôture+30j |
| US22 — CA-49 | Reprise campagne/midnight sans double débit ; retrait destinataire avant diffusion ; même campagne pas trois tentatives ; alerte seuil ×3, bloqués inclus, regroupement Ops/email ; quota épuisé suspend/reconfirmation ; rapport distingue Live/Push/lecture/inconnu |
| US27 — CA-54 | Renouvellement avant/après, futur droit pas actif trop tôt, upgrade prorata sans reset, baisse au terme, arrêt payé sans remboursement automatique ; double remboursement réservé concurrent et rapprochement fournisseur |
| US28 — CA-55 | Coordonnées futures seulement, fichiers existants inchangés, délégation Achat et tenant, téléchargement financier autorisé, avoir et remboursement réconciliés |
| US34 — CA-61 | Collecte rejouée unique, coût estimé remplacé non ajouté, données manquantes distinctes zéro, non ventilé conservé, coûts invisibles client, alertes 80/100 dédupliquées ; aucune mutation abonnement/quota/facture par dépassement |

Vérifier PostgreSQL : verrous de quota avec deux connexions, fréquence avec deux campagnes simultanées, dernier crédit au changement de mois Paris, événements Stripe concurrents, remboursement concurrent, import interrompu juste après commit d'une ligne. Les tests de domaine utilisent horloge/faits injectés, sans SQL ni fournisseur ; l'orchestration est couverte séparément. Les tests de contrat contrôlent tenant, version, corps d'erreur, idempotence et pagination, puis les scénarios navigateur couvrent chaque état incertain/suspendu et les retours de paiement.

Démonstration à adapter dans le backend : communes A/B, responsables et collaborateurs habilités/non habilités, modules actif/futur/offert/essai/expiré, derniers crédits, campagne sans Push mais Live autorisé, import avec delta local et doublon email, coûts partiels et alerte. Aucune donnée privée ni fichier utilisateur dans les fixtures ; le générateur appelle les règles du produit et ne crée pas de raccourci d'activation.

Documentation à mettre à jour lors de l'implémentation : catalogue/vente et conditions de prorata, écrans Mes modules et import, guide de communication/préférences, support paiement incertain et reprise, procédures ERP d'octroi/remboursement, Ops de diffusion/coût et conservation. Les règles d'onboarding/périmètre, droits d'équipe, origine Animation et remise des lots restent dans les documents liés ; leurs tests sont des dépendances de cette couverture.
