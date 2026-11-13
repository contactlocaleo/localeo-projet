# Localeo ERP — audit des pages et de l’ergonomie de gestion

Date : **13 novembre 2026**. Statut : **rapport d’audit et recommandations, sans implémentation**.

## 1. Conclusion

Localeo ERP dispose déjà d’une navigation commune et de plusieurs écrans bien structurés. Le principal défaut est **l’inégalité de construction des pages à l’intérieur de cette navigation** : certaines présentent un dossier, son état et la prochaine action ; d’autres exposent une succession de liens, de données et de formulaires dont le gestionnaire doit reconstruire le sens.

L’amélioration prioritaire consiste à rendre chaque page capable de répondre immédiatement à quatre questions : **quel dossier ou périmètre suis-je en train de consulter ? Quel est son état ? Que dois-je examiner ou traiter ? Quel sera l’effet de mon action ?**

L’inspection de TEST confirme directement le besoin exprimé :

- **Préparation accompagnée** : le nom de l’animation reste un sous-titre dans une page générique ; les informations, le lien vers la checklist, les actions repliées et l’historique se succèdent sans véritable synthèse de dossier. Le bouton « Actualiser le suivi » domine visuellement les décisions métier.
- **Visions 360** : dix destinations sont présentées sur deux colonnes, sans explication propre à chaque destination ni regroupement par tâche. La page est alignée graphiquement, mais aide peu à choisir le bon parcours.
- **Achats 360** : références techniques longues, états anglais, formulaire de recherche minimal et absence de pagination visible réduisent l’efficacité de recherche.
- **Accueil** : la file de dossiers et les prochaines actions constituent un progrès réel. Avec 25 lignes affichées, les autres blocs se retrouvent toutefois loin dans la page ; sur la fenêtre observée, le lien « Reprendre » se coupe sur deux lignes.
- **Hub Animation** : les catégories et les descriptions apportent déjà du contexte. Il faut conserver ce travail ; sa transformation en point de travail quotidien est une amélioration ultérieure.

Le rapport distingue **30 points à traiter**, regroupés ci-dessous par parcours. Les priorités P1 concernent la compréhension de la tâche, les erreurs de cible ou de portée, les saisies et l’accès aux dossiers. Les P2 améliorent la continuité et la productivité. Les P3 portent sur la consolidation. Ces priorités ne constituent pas une cotation de vulnérabilités.

## 2. Périmètre et niveau de preuve

### Méthode

L’audit combine trois revues indépendantes du code — gestion/catalogue, Animation, finance/exploitation — et une inspection visuelle ciblée de TEST. Les versions locales de référence sont : backend **`40d3cfd07235d1881109046c237c91a0e6c170c6`**, documentation **`259231658841acec27011b137b5816be2b1b00ac`**. Le commit effectivement déployé sur TEST n’a pas été vérifié ; les observations de TEST et celles du code local sont donc distinguées.

Les sources principales sont les interfaces ERP du backend, leurs routes, les capacités d’accès et les spécifications E60, E65 et E73. Le [guide de prise en main ERP](../../produit/formation/backend/guide-prise-en-main-erp.md) sert de référence aux tâches quotidiennes des profils Lecteur, Backoffice, Finance et Administrateur.

L’[audit du 12 novembre](localeo-erp-ux-productivite-2026-11-12.md) est une photographie antérieure. Les améliorations documentées dans [E60 — UX et productivité](../../specifications/epic-60-vision-360-commercialisation/ux-productivite.md) sont prises en compte : accueil orienté dossiers, continuité de certaines listes, reprise de session, retours d’enregistrement et navigation au clavier. Elles ne sont pas présentées ici comme absentes.

### Preuves utilisées

| Marque | Signification | Portée |
| --- | --- | --- |
| **V** | Interface TEST observée visuellement et par sa structure accessible | Préparation accompagnée en détail, accueil, Visions 360, recherche Achats 360, hub Animation ; session Administrateur, quatre communes accessibles. Navigation en lecture seule. |
| **S** | Rendu local sur réponses API simulées | Six routes, 24 scénarios du gabarit commun ; largeur 1280, 1920 et 320 px, plus texte doublé à 320 px. Trois captures examinées visuellement : Finance à 1280, Animation à 1280, création commerçant à 320 avec texte doublé. |
| **C** | Constat dans le code actuel | Structure, liens, champs, conditions d’affichage, appels API, retours et protections. Une conséquence visuelle ou un scénario non exécuté reste à confirmer en recette. |
| **R** | Recommandation | Proposition de conception ; ni comportement existant ni résultat mesuré. |

Le contrôle automatique du navigateur a interrompu la navigation suivante, faute de pouvoir vérifier l’URL courante avec certitude. L’inspection s’arrête donc aux cinq écrans cités. Aucun dossier, droit, paiement, message ou paramètre n’a été modifié. Les captures TEST ne sont pas versées au dépôt et les identifiants des dossiers observés ne sont pas reproduits.

Il ne s’agit pas d’une certification d’accessibilité, d’un audit de sécurité complet ou d’une mesure de performance en production. Aucun gain de temps n’est chiffré sans test utilisateur. Les contenus internes de CRM, OnBoard, Ops, Control et Atelier ne sont pas audités ici ; leurs points de passage depuis ERP sont pris en compte. Le Support organisations est examiné comme parcours voisin de traitement.

## 3. Inventaire des pages examinées

Les routes abrégées commencent par `/internal/erp/`, sauf mention contraire. Une ligne peut couvrir une liste, sa fiche et ses états ; elle ne signifie pas que toutes leurs variantes ont été visitées sur TEST.

| Pages ou famille | Preuve | État et traitement attendu |
| --- | --- | --- |
| Accueil, `activite` | V, C | File d’équipe déjà utile ; réduire la longueur d’aperçu et mieux équilibrer les tâches, UX-29. |
| `visions-360` | V, C | Annuaire de liens à contextualiser, UX-01. |
| `operations`, `finance`, `supervision` | S sur Opérations/Finance, C | Hubs génériques ; séparer consultation, traitement et fonctions exceptionnelles, UX-01. |
| `administration` | C | Recherche par objet utile ; rendre explicite la destination technique, UX-01/12. |
| `commercants` | S, C | Bonne référence de liste : identité, filtres, états vides, reprise et pagination. |
| `commercants/nouveau` | S, C | Parcours structuré ; vérifier la place occupée par l’en-tête avec texte agrandi, UX-28. |
| Fiche commerçant : synthèse, référencement, activité | C | Synthèse à conserver ; adapter l’ajout de note aux droits, UX-04. |
| Fiche commerçant : offre, modèles et prestations | C | Informations répétées et éditeur peu annoncé, UX-15. |
| `coffrets`, `commercialisation` | S sur Coffrets, C | Deux intentions partagent le même tableau de diagnostic, UX-13. |
| Nouveau coffret, informations et composition | C | Aide longue, consultation/édition et composition à restructurer, UX-04/16. |
| Fiche coffret : commercialisation et cycle de vie | C | Commandes de contrôle, publication et retrait à hiérarchiser, UX-05. |
| `alertes`, `territoires` | C | Causes, états, lien d’arrivée et reprise locale, UX-11/14/24. |
| `instances`, fiche instance | C | Recherche utile ; regrouper les interventions par intention, UX-05/24. |
| `animation` | V, S, C | Catégories et descriptions déjà présentes ; travail en attente à envisager, UX-29. |
| `suivi-animations`, fiche et lots | C | Contexte et bandeau de conduite à conserver ; continuité à étendre, UX-12. |
| `animations/generations` | C | Bonne référence de file/dossier/prochaine action ; filtres techniques à reléguer aux critères avancés. |
| `animations/preparation` | C | Identité, saisies et chargement des bibliothèques, UX-03/09/24. |
| `preparations-animation`, fiche | V sur la fiche, C | Dossier de service à reconstruire visuellement, UX-02/09/12. |
| `animations/exploitation` et actions de jeu | C | Impact et confirmation existent ; contexte métier et sélection des cibles à renforcer, UX-03. |
| `animations/conservation` | C | Cibles techniques à contextualiser ; rapports, exclusions et gels à conserver, UX-03. |
| `acces-animation`, création et fiche | C | Habilitations effectives et permissions bien distinguées ; conserver ce socle. |
| `acces-animation/organisations` | C | Transformer les demandes repliées en file de traitement, UX-17. |
| Partenaires 360 et anciennes habilitations `/admin/...` | C | Rebrancher les parcours de gestion actuels, UX-18. |
| Nouvelle souscription `/admin/referencement-partenaire-animation` | C | Étapes et revue déjà présentes ; vérifier les sélecteurs de communes à volume représentatif. |
| Souscriptions et commandes d’abonnement | C | Informations commerciales présentes ; renforcer l’accès à l’action utile, UX-19. |
| Offres `/admin/offres-animation`, nouvelle offre | C | Assistant de création utile ; rendre les conditions lisibles en consultation, UX-20. |
| `catalogue-animation`, `modules-animation` | C | Droits et usages à préserver ; portée globale et pagination à clarifier, UX-06/20. |
| `remboursements-animation` | C | Dossier financier identifiable et saisie monétaire, UX-07. |
| `sollicitations-animation` | C | Réglages et reprises existants ; harmoniser contexte, filtres et action de section, UX-12/28. |
| Support organisations `/internal/support/organisations` | C | Réponse principale, échanges et notes internes déjà bien séparés ; référence à conserver. |
| `pilotage-economique`, organisation, mesures | C | Lecture mobile et séparation consultation/correction, UX-22/23. |
| `reversibilite`, fiche de fermeture | C | Engagements et décisions à séquencer, UX-19. |
| Vérifications d’import dans la fiche commerce | C, sous-composant | Motif et absence d’activation implicite expliqués ; ajouter un résumé avant/après lors d’une future amélioration. |
| `paiements`, `reversements`, fiches ERP | C | Consultations déjà structurées ; préserver inconnus, devises, filtres et reprise. |
| Campagnes `/internal/reversements/vue-360` | C | Distinguer filtres de consultation et périmètre d’exécution, UX-08. |
| Factures, demandes et rapprochements SQLAdmin | C | Exposer les dossiers et destinataires métier, UX-21. |
| Achats 360 `/admin/vision-360-achats` | V, C | Pagination, noms, états, recherche et retour, UX-10/12. |
| Clients 360 `/admin/vision-360-client` | C, couverture ciblée | Alignement du contexte de retour ; détail moins approfondi qu’Achats, UX-12. |
| `audit`, `webpush` | C | Écrans déjà structurés ; entrées contextuelles et diagnostics ciblés, UX-26. |
| Batchs, santé et configuration `/admin/...` | C | Distinguer diagnostic et exécution ; détail approfondi des batchs, UX-25. |
| `utilisateurs` | C | Faire précéder l’édition par l’état du compte et de l’invitation, UX-27. |
| Confirmations d’actions SQLAdmin | C | Remplacer l’URL technique par une confirmation métier, UX-08. |

Les bons et QR sont abordés au travers des achats et des instances ; aucune page ERP autonome « Bons » n’a été identifiée dans les entrées examinées. Le contact public d’aide est repéré comme destination, sans audit de son contenu.

## 4. Modèles de pages recommandés

La logique de gestion demande plusieurs modèles complémentaires. SAP Fiori distingue notamment les vues d’ensemble, listes, files de travail, pages d’objet et assistants selon la tâche. Cette distinction fournit une base pertinente pour Localeo, sans imposer l’adoption de sa bibliothèque graphique. [Référence SAP Fiori](https://www.sap.com/design-system/fiori-design-web/v1-145/page-types/floorplans/when-to-use-which-floorplan).

| Modèle | Structure recommandée | Usage Localeo |
| --- | --- | --- |
| **Accueil de travail** | Périmètre et date → dossiers à examiner → accès aux listes → fonctions par domaine | Accueil, Animation, Finance, Opérations. Un hub sans projection de travail fiable reste un répertoire de tâches décrit. |
| **Liste de gestion** | Titre et objectif → recherche/filtres → résumé des résultats → tableau comparable → pagination | Coffrets, préparations, demandes d’organisation, achats, remboursements. |
| **Fiche dossier** | Identité et état → prochaine étape → sections métier → historique et outils secondaires | Animation, préparation, commerçant, instance, souscription, utilisateur. |
| **Formulaire de décision** | Cible et portée → données nécessaires → conséquences → revue → confirmation spécifique → résultat | Publication, remboursement, fermeture, changement d’accès, campagne. |
| **Console de diagnostic** | Objet concerné → symptôme et état → faits utiles → procédure → détails techniques → intervention autorisée | Exploitation, Audit, Web Push, batchs, conservation. |

### Exemple : fiche de préparation accompagnée

Schéma de proposition, à adapter aux données et actions réellement fournies par le serveur :

```text
Animations > Préparations accompagnées > Nom de l’animation
← Retour aux demandes filtrées

NOM DE L’ANIMATION                      État : À compléter
Organisation · Commune                 Actualisé le …

PROCHAINE ÉTAPE
Vérifier les éléments nécessaires avant de confirmer la demande complète.
[ Examiner les éléments ]  [ Confirmer la demande complète* ]

Demande et calendrier                 Parcours à préparer
Complétude : à confirmer              Accès au parcours et à la checklist
Date cible : non disponible           État de préparation connu
Cause et suite possible               Validation terrain : organisateur

Suivi du service | Historique
Décisions, compléments, dates et messages publics

Autres actions : réviser l’estimation · annuler le service
```

`*` L’action reste soumise aux droits, prérequis, confirmation et transitions actuels. « Examiner les éléments » peut être un lien vers la section pertinente. Une date indisponible reste indisponible ; le rendu ne doit pas calculer une promesse de délai.

### Règles de mise en page et d’action

1. **L’identité prime sur le type d’écran.** Une fiche affiche le nom du dossier comme titre ; la rubrique apparaît dans le fil d’Ariane. Organisation, commune, référence utile et état se trouvent près de ce titre.
2. **L’action principale correspond à la tâche et à l’état.** Une action dominante quand cela a du sens ; quelques actions secondaires visibles ; les opérations rares ou sensibles dans un groupe distinct. « Actualiser » reste un utilitaire.
3. **La densité sert la comparaison.** Tableaux pour comparer des dossiers, sections pour comprendre un dossier, formulaires pour le modifier. Les cartes ne doivent pas remplacer systématiquement les listes ni augmenter les défilements.
4. **Les contrôles sont placés au niveau de leur portée.** Recherche, filtres et export près de la table ; action de dossier dans son en-tête ; action de ligne au niveau de la ligne ; traitement collectif seulement après sélection explicite et si le métier le permet. [Référence Carbon — Data table](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines).
5. **Les libellés indiquent le résultat.** « Examiner le blocage », « Ouvrir la commande », « Confirmer la préparation prête » sont plus informatifs qu’un ensemble de « Voir », « Traiter » et « Valider ». Un lien continue de naviguer ; un bouton déclenche une commande.
6. **Consultation et édition se distinguent.** Une fiche lisible précède l’édition explicite. Les décisions nécessitant de nombreux champs s’ouvrent dans une section ou un écran dédié avec Annuler/Enregistrer.
7. **Le résultat est visible au bon endroit.** Succès, refus, conflit, résultat incertain et erreur de lecture ne doivent pas se confondre. L’écran indique l’état confirmé et la suite possible, sans rejouer automatiquement une commande.

Ces principes prolongent la visibilité de l’état, le langage utilisateur, la reconnaissance des options et la prévention des erreurs décrits par Nielsen Norman Group. [Référence — heuristiques d’utilisabilité](https://www.nngroup.com/articles/ten-usability-heuristics/).

## 5. Points prioritaires

### UX-01 — P1 — Contextualiser les hubs de fonctions

**Constat V/S/C.** Visions 360, Opérations, Finance et Supervision reposent sur des couples libellé/URL et un sous-titre générique. Finance place même la reprise historique des commissions avant les consultations courantes. La recherche d’Administration aide à trouver un objet, mais n’explique pas le travail à accomplir. Sources : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 540–545, 596 et 600.

**À traiter.** Regrouper les destinations par intention : consulter un dossier, traiter une demande, contrôler, paramétrer. Ajouter une phrase d’usage à chaque entrée et identifier les outils techniques. Finance doit d’abord présenter encaissements, reversements et facturation ; les reprises exceptionnelles viennent ensuite. Réutiliser la structure descriptive déjà présente dans le hub Animation.

**Recette.** Un gestionnaire sait où vérifier un paiement ou rechercher l’achat d’un client avant d’ouvrir une destination. Aucun compteur non fourni par une projection fiable n’est inventé.

### UX-02 — P1 — Transformer la préparation accompagnée en fiche de service

**Constat V/C.** Sur TEST, titre et fil d’Ariane restent génériques, avec un retour et un lien supplémentaire vers toutes les préparations. La fiche expose ensuite nom de l’animation, état, dates, notice, lien de checklist, actualisation, décisions repliées et historique. Les informations existent mais ne construisent pas une lecture « dossier → attente → action ». Source : [preparations-service.js](../../../../localeo-backend/app/infrastructure/erp/preparations-service.js), lignes 98–128.

**À traiter.** Adopter le modèle proposé en section 4 : identité complète, état expliqué, prochaine étape visible, calendrier distinct, parcours et historique organisés. Présenter la décision courante au premier niveau et reléguer l’actualisation au rang d’utilitaire. La liste doit aider à distinguer complément attendu, demande à qualifier et retard réel.

**Recette.** Sur chaque état du service, l’opérateur identifie ce qui manque, qui doit agir et quelle décision est disponible sans déplier toutes les actions. Une annulation reste séparée de l’avancement normal.

### UX-03 — P1 — Maintenir l’identité métier dans les consoles Animation

**Constat C.** Exploitation et préparation proposent une entrée par UUID. L’aperçu d’exploitation présente statut, version et seize métriques sans nom d’animation, organisation ni commune. La correction d’une preuve et les cibles de conservation demandent également des identifiants. Sources : [exploitation_animation.html](../../../../localeo-backend/app/infrastructure/admin/exploitation_animation.html), lignes 22–28 et 60 ; [preparation_chasse.html](../../../../localeo-backend/app/infrastructure/admin/preparation_chasse.html), ligne 22 ; [conservation_animation.html](../../../../localeo-backend/app/infrastructure/admin/conservation_animation.html), ligne 28.

**À traiter.** Conserver le dossier nommé lors des transitions depuis le suivi. Depuis le menu, proposer une recherche autorisée par nom et commune. Choisir une preuve dans ses éléments de contexte utiles ; conserver les UUID dans les détails techniques.

**Recette.** Le gestionnaire vérifie la cible métier avant une intervention et revient à sa fiche. Aucun parcours courant ne dépend d’un copier-coller d’UUID. Les aperçus d’impact et confirmations existants sont conservés.

### UX-04 — P1 — Ne pas proposer une saisie impossible au profil Lecteur

**Constat C.** Le formulaire Informations du coffret et l’ajout de note interne du commerçant sont rendus sans le garde de capacité attendu, alors que leur écriture requiert `catalogue.gerer`. Sources : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 131–159, 404 et 494 ; [capacites_routes.py](../../../../localeo-backend/app/security/capacites_routes.py), lignes 41 et 98. Le serveur reste protégé : ce constat ne démontre aucun contournement d’autorisation.

**À traiter.** Présenter les valeurs et notes en consultation, puis une action Modifier ou Ajouter une note uniquement pour l’utilisateur habilité. Le référencement commerçant fournit déjà un exemple de rendu différencié.

**Recette.** Le Lecteur ne peut pas commencer une saisie vouée à un refus. Un gestionnaire peut éditer. Une perte de droit en cours de saisie conserve le refus serveur et produit un message explicite.

### UX-05 — P1 — Hiérarchiser les actions du coffret et de l’instance

**Constat C.** Commercialisation juxtapose réévaluation, vérification, mise en vente, retrait et archivage ; plusieurs actions ont le même poids. La fiche Instance accumule renvois, QR/lien, révocation, secours, documents, annulation, prolongation et remboursement. Sources : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), ligne 497 ; [instances.js](../../../../localeo-backend/app/infrastructure/erp/instances.js), lignes 50–68.

**À traiter.** Coffret : état commercial, diagnostic et blocages, action autorisée, résultat ; cycle de vie dans une section distincte. Instance : synthèse client/validité/usage, puis « Aider le client à accéder », « Traiter la demande », « Cycle de vie et remboursement », « Historique et outils avancés ».

**Recette.** Les scénarios « publier un coffret prêt », « client sans accès » et « demande de remboursement » ont chacun une entrée claire. Les confirmations et exigences de motif existantes sont conservées. Les états et autorisations viennent du serveur.

### UX-06 — P1 — Expliquer la portée globale des conditions du catalogue

**Constat C.** Le catalogue commercial demande une commune pour consulter, mais la nouvelle version d’offre porte globalement sur les futurs achats. L’avertissement « toutes les communes » est conditionné à la présence d’`offre_id`, alors que le formulaire reste disponible sans ce paramètre. Source : [modules-commerce.js](../../../../localeo-backend/app/infrastructure/erp/modules-commerce.js), lignes 151–169 ; règle décrite dans [la spécification des modules](../../specifications/epic-73-animation-et-ou-coffrets/modules-souscriptions-import-communication.md).

**À traiter.** Distinguer le filtre de disponibilité des conditions globales. Afficher systématiquement portée, ancienne/nouvelle version, prix, droits et quotas modifiés, ainsi que l’effet sur les futurs achats et les conditions déjà acquises.

**Recette.** Les deux entrées, directe et depuis une offre, fournissent la même information avant confirmation. La commune sélectionnée ne laisse jamais croire à une modification locale de tarif.

### UX-07 — P1 — Construire un véritable dossier de remboursement

**Constat C.** La liste Animation répète « Ouvrir la demande » avec peu de repères de commande/organisation. Le détail affiche un identifiant brut et demande un montant en centimes, alors que le récapitulatif est en euros. Source : [modules-commerce.js](../../../../localeo-backend/app/infrastructure/erp/modules-commerce.js), lignes 174–191.

**À traiter.** Ajouter les repères autorisés : référence, organisation, commune, commande source, état, montant et date. Présenter la décision à côté de son contexte financier. Saisir le montant dans l’unité affichée, avec conversion exacte vers le contrat en centimes. Distinguer décision, exécution, rapprochement et retrait éventuel du droit.

**Recette.** Le gestionnaire identifie le destinataire et la commande avant de décider ; `12,50 €` produit exactement `1250` centimes. Confirmation obligatoire et reprise du résultat incertain sont préservées. Aucune transaction réelle n’est nécessaire à cette recette d’interface simulée.

### UX-08 — P1 — Rendre les confirmations compréhensibles avant engagement

**Constat C.** La campagne Stripe peut être lancée depuis un formulaire direct ; les filtres visibles ne définissent pas son périmètre. Une notice l’explique, mais ne remplace pas une revue préalable. Les confirmations SQLAdmin génériques exposent surtout le chemin HTTP et « Confirmer et exécuter ». Sources : [admin.py](../../../../localeo-backend/app/infrastructure/admin/admin.py), lignes 3070–3078 et 13287–13297 ; [commandes_post.py](../../../../localeo-backend/app/infrastructure/admin/commandes_post.py), lignes 10–23.

**À traiter.** Séparer consultation et lancement. Présenter cible, portée réellement calculée, effets et blocages disponibles avant confirmation, avec un verbe métier spécifique. Annuler doit revenir au dossier ou à la liste d’origine.

**Recette.** Changer la période de consultation ne change pas implicitement la promesse d’exécution. La revue annonce le véritable périmètre. Annuler ne déclenche aucun POST métier. Les protections POST, CSRF, droits et règles financières sont conservées.

### UX-09 — P1 — Protéger les saisies de préparation avant une actualisation

**Constat C.** « Actualiser le suivi » reconstruit les formulaires de préparation accompagnée sans préserver leur saisie. La checklist terrain est reconstruite au chargement ; sa garde de sortie couvre une commande en attente, pas les champs simplement modifiés. Sources : [preparations-service.js](../../../../localeo-backend/app/infrastructure/erp/preparations-service.js), lignes 74–120 ; [preparation_chasse.html](../../../../localeo-backend/app/infrastructure/admin/preparation_chasse.html), lignes 52–73. Le scénario de perte n’a pas été exécuté sur TEST.

**À traiter.** Étendre la protection de brouillon aux modules concernés : état modifié visible, brouillon privé en mémoire d’onglet, choix explicite avant abandon, actualisation séparée de l’édition, traitement d’une version devenue différente.

**Recette.** Saisir un motif ou une observation, actualiser puis tenter de quitter : aucune perte silencieuse. Expiration ou changement de session purge le privé. Aucun stockage durable de formulaire n’est ajouté.

### UX-10 — P1 — Rendre tous les achats recherchés accessibles

**Constat V/C.** Achats 360 demande des pages de 25 résultats au service, mais le rendu n’expose pas de pagination ni de total. Le retour de détail perd recherche et page. Le champ possède un placeholder sans label associé dans ce rendu. Sur TEST, des références longues et statuts `PAYMENT_PENDING` ou `INSTANCES_RESERVEES` dominent la lecture. Source : [admin.py](../../../../localeo-backend/app/infrastructure/admin/admin.py), lignes 8128–8161.

**À traiter.** Liste ERP avec recherche nommée, résumé des résultats, précédent/suivant, référence commerciale dominante, état en français, origine expliquée et retour conservé. Les références techniques restent recherchables et copiables en détail.

**Recette.** Avec au moins 26 résultats, atteindre le dernier, ouvrir sa fiche et revenir au même filtre, à la même page et au même élément. Aucune disparition apparente de dossiers au-delà de la première page.

### UX-11 — P1 — Corriger le lien « Voir les coffrets » des territoires

**Constat C.** Le lien ouvre `/commercialisation?villeId=…`, dont le filtre par défaut est `NON_VENDABLE`. Une commune ne possédant que des coffrets vendables peut donc aboutir à une liste vide malgré un compteur positif. Sources : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), ligne 537 ; [catalogue-ux.js](../../../../localeo-backend/app/infrastructure/erp/catalogue-ux.js), ligne 4.

**À traiter.** Faire correspondre libellé et destination : tous les coffrets de la commune pour « Voir les coffrets », accès distinct pour les offres indisponibles.

**Recette.** Vérifier communes avec offres toutes vendables, toutes bloquées, mixtes et sans offre. Le filtre d’arrivée et le résultat correspondent au lien choisi, sans changer le calcul métier de couverture.

## 6. Optimisations par parcours

### UX-12 — P2 — Étendre la continuité aux listes Animation et consoles historiques

**Constat C.** Le mécanisme commun couvre plusieurs listes du catalogue, mais pas les listes Animation. Certains curseurs ne vivent que dans le module courant ; des retours reviennent à la liste générique. Les consoles HTML historiques possèdent déjà la coque ERP, mais leur fil et retour sont souvent « Accueil ERP → titre ». Sources : [continuite.js](../../../../localeo-backend/app/infrastructure/erp/continuite.js), lignes 3–35 ; `suivi-animations.js` 41–46, `preparations-service.js` 18–33, `reversibilite-organisations.js` 16–25 ; [admin.py](../../../../localeo-backend/app/infrastructure/admin/admin.py), lignes 350–427.

**À traiter et vérifier.** Restaurer filtres, page/curseur, onglet, ligne et focus, avec parent structurel en arrivée directe. Tester retour explicite, navigateur et page devenue vide. Valider les destinations et conserver les données privées hors des stockages persistants.

### UX-13 — P2 — Distinguer gestion des coffrets et traitement des indisponibilités

**Constat C.** Coffrets et Commercialisation partagent le tableau « Coffret / Vendabilité / Pourquoi ? / Depuis / Action » et le lien « Traiter ». Source : [catalogue-ux.js](../../../../localeo-backend/app/infrastructure/erp/catalogue-ux.js), lignes 4–5 et 53.

**À traiter.** Vue Catalogue : nom, commune, statut commercial, prix si disponible, disponibilité et accès au dossier. Vue Blocages : cause, ancienneté et examen du diagnostic. Partager le socle de recherche et de continuité, pas nécessairement toutes les colonnes.

**Recette.** Distinguer deux coffrets homonymes et un brouillon d’un coffret actif ; comprendre que statut commercial et vendabilité sont deux informations différentes. Tout champ manquant nécessite d’abord une projection de lecture adaptée.

### UX-14 — P2 — Donner aux alertes et territoires un vocabulaire de traitement

**Constat C.** Les alertes présentent nature et ancienneté, sans cause par dossier ni état ouvert/fermé visible dans toutes les vues. Les regroupements de causes ne conduisent pas à leur sélection. Territoires transmet directement des codes comme `NOT_PUBLISHED` ou `NO_KNOWN_SELLABLE` au badge. Source : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 30–32 et 530–537.

**À traiter.** Afficher cause principale, autres causes, état, commune, ancienneté et accès au diagnostic. Traduire distinctement commune non publiée, absence de coffret, offre disponible et diagnostic à vérifier. Conserver l’incertitude réelle.

**Recette.** Expliquer trois alertes depuis la liste, distinguer une alerte fermée, rejoindre un regroupement filtré. Aucun code technique non expliqué ne tient lieu de décision métier.

### UX-15 — P2 — Clarifier modèles et prestations du commerçant

**Constat C.** L’onglet Offre et prestations répète plusieurs informations sur les modèles, prestations et coffrets. Un clic Modifier peut remplacer un éditeur plus bas sans annoncer clairement le modèle ni déplacer le focus. Source : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 311–326 et 387–393.

**À traiter.** Deux sections : « Modèles réutilisables » et « Prestations dans des coffrets ». Chaque éditeur annonce création ou modification et le nom concerné, avec Annuler/Enregistrer et un retour à la bonne ligne.

**Recette.** Depuis une liste longue, Modifier mène immédiatement à l’éditeur identifié. Le texte explique qu’un modèle modifié ne met pas implicitement à jour les coffrets déjà composés.

### UX-16 — P2 — Raccourcir le chemin de création et composition d’un coffret

**Constat C.** Le nouveau coffret présente un guide de cinq étapes avant le formulaire. Composition cumule explications, budget, avertissement BUM, tableau, recherche, modèles et formulaire. Source : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 82–92, 283 et 410–476.

**À traiter.** Créer des sections Identification, Offre client et Visuel, avec aide brève au bon endroit. En composition, séparer contenu actuel et ajout/édition d’une prestation ; garder le guide complet accessible et l’avertissement BUM au moment pertinent.

**Recette.** Un utilisateur récurrent atteint sa tâche sans relire tout le guide. Les conséquences d’une modification sur la validation restent visibles. Tester bureau, 390 et 320 px sans supprimer de prérequis métier.

### UX-17 — P2 — Présenter les demandes d’organisation comme une file

**Constat C.** Le résumé des demandes repliées contient surtout le nom de l’organisation ; date, représentant et invitation demandent une ouverture. La pagination propose la suite sans retour symétrique. Source : [equipes-animation.js](../../../../localeo-backend/app/infrastructure/erp/equipes-animation.js), lignes 167–208.

**À traiter.** Tableau avec organisation, communes, représentant, date, état et prochaine action ; détail de vérification séparé. Ajouter recherche/filtres bornés côté serveur si le volume le nécessite.

**Recette.** Repérer demandes à vérifier et invitations expirées sans ouvrir chaque ligne ; distinguer les homonymes ; parcourir les deux sens. La sélection seule ne renvoie aucune invitation.

### UX-18 — P2 — Aligner Partenaires 360 et gestion moderne des accès

**Constat C.** La recherche partenaire est limitée à 100 sans continuation ni indication de limite. Compteurs et gestionnaires sont peu navigables. « Gérer les accès » renvoie à une ancienne console puis à SQLAdmin, alors que des fiches ERP contextualisées existent. Source : [admin.py](../../../../localeo-backend/app/infrastructure/admin/admin.py), lignes 8386–8451.

**À traiter.** Synthèse partenaire et liens nommés vers souscriptions, gestionnaires, animations et alertes. Relier les écrans actuels et garder les outils historiques dans un accès technique distinct. Expliciter et rendre navigables les résultats bornés.

**Recette.** Depuis une organisation, rejoindre le bon utilisateur et ses droits effectifs, puis revenir à la recherche. Dates et états sont lisibles ; aucun changement d’habilitation n’est induit par cette réorientation.

### UX-19 — P2 — Mettre l’action utile en tête des dossiers commerciaux et de fermeture

**Constat C.** Les dossiers contiennent déjà états, conséquences et prochaines étapes, mais des actions utiles restent loin dans la page : gestion des modules après plusieurs sections, commande par ancre, engagements et formulaires de fermeture empilés. Sources : [animation-commercial.js](../../../../localeo-backend/app/infrastructure/erp/animation-commercial.js), lignes 41–59 ; [reversibilite-organisations.js](../../../../localeo-backend/app/infrastructure/erp/reversibilite-organisations.js), ligne 104 et suivantes.

**À traiter.** En-tête du dossier, état, zone « À faire maintenant », sections de consultation, puis historique. Pour une fermeture, présenter engagements à résoudre avant décision finale.

**Recette.** Dans chaque état représentatif, le gestionnaire trouve l’action disponible sans parcourir tous les formulaires. Les blocages et conséquences existants restent affichés ; aucune urgence n’est déduite arbitrairement côté interface.

### UX-20 — P2 — Rendre le catalogue, les offres et leurs pages réellement navigables

**Constat C.** Le composant de pagination du commerce des modules ne propose que « Page suivante ». Une offre ciblée est recherchée dans la page chargée, avec invitation à parcourir les suivantes si elle manque. La liste historique des offres expose notamment des limites JSON et états bruts. Sources : [modules-commerce.js](../../../../localeo-backend/app/infrastructure/erp/modules-commerce.js), lignes 51 et 151–169 ; [admin.py](../../../../localeo-backend/app/infrastructure/admin/admin.py), ligne 8367.

**À traiter.** Précédent/suivant cohérents, accès direct à l’offre ciblée, liste de comparaison et fiche de conditions lisibles. Réutiliser la présentation monétaire et le récapitulatif de l’assistant Nouvelle offre.

**Recette.** Retrouver une offre située au-delà de 25 entrées, revenir aux résultats, comparer droits/quotas/prix sans lire du JSON. Ne jamais assimiler l’absence d’un droit sur une page à son absence réelle.

### UX-21 — P2 — Faire de la facturation une consultation de dossiers

**Constat C.** Le hub Finance mène aux listes SQLAdmin de factures et demandes, avec des colonnes d’identifiants de commerçant ou destinataire. Sources : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), ligne 543 ; [admin.py](../../../../localeo-backend/app/infrastructure/admin/admin.py), lignes 12369 et 12396.

**À traiter.** Tableau métier avec numéro, destinataire nommé, source, montant/devise, état et date. Fiche avec pièces disponibles, source et historique. Garder consultation et commande financière distinctes, sans étendre les droits du profil Finance.

**Recette.** Retrouver une facture par référence ou destinataire autorisé, ouvrir sa source et revenir. L’absence d’un document reste explicite ; un téléchargement ne déclenche pas une génération implicite.

### UX-22 — P2 — Préserver les légendes du pilotage économique sur mobile

**Constat C déterministe, rendu à confirmer.** La table du pilotage crée ses cellules sans `data-label`. À 720 px et moins, le CSS masque l’en-tête visuellement et utilise cet attribut pour légender chaque valeur. Sources : [pilotage-economique.js](../../../../localeo-backend/app/infrastructure/erp/pilotage-economique.js), ligne 40 ; [erp.css](../../../../localeo-backend/app/infrastructure/erp/erp.css), lignes 24–34.

**À traiter.** Réutiliser une table commune associant valeurs et en-têtes, ou conserver un tableau défilable accessible lorsque la comparaison bidimensionnelle le justifie.

**Recette.** À 390 et 320 px, puis texte agrandi, chaque montant et quantité garde sa légende visible et sémantique. Les états constaté, estimé, incomplet et inconnu restent distincts. Le défilement éventuel reste local au tableau.

### UX-23 — P2 — Séparer les mesures économiques de leur correction

**Constat C.** Une page peut rendre 25 mesures avec, pour chacune, des formulaires de rapprochement et de correction immédiatement ouverts. Les vues utilisent une série de boutons dont l’actif est désactivé. Source : [pilotage-economique.js](../../../../localeo-backend/app/infrastructure/erp/pilotage-economique.js), lignes 41–43 et 99–118.

**À traiter.** Tableau comparable des mesures, puis action Examiner ouvrant contexte, preuve, historique et correction. Conserver organisation, mois et vue active dans la continuité de consultation.

**Recette.** Comparer 25 mesures sans traverser 25 formulaires ; identifier sans ambiguïté la mesure modifiée. La vue active reste perceptible et accessible au clavier ; une donnée inconnue ne devient pas zéro.

### UX-24 — P2 — Borner les chargements et isoler les erreurs de lecture

**Constat C.** La préparation terrain parcourt toutes les pages d’accords puis de POI avant son rendu. Alertes, Territoires et Instances peuvent remonter vers un remplacement global du contenu en cas d’erreur initiale, contrairement aux reprises locales des commerçants/coffrets. Sources : [preparation_chasse.html](../../../../localeo-backend/app/infrastructure/admin/preparation_chasse.html), lignes 50–52 ; [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 530, 537 et 600 ; [instances.js](../../../../localeo-backend/app/infrastructure/erp/instances.js), lignes 37 et 43.

**À traiter.** Charger les références utiles au parcours, rechercher les bibliothèques à la demande, rendre les sections indépendantes. Conserver titre, filtres et retour pendant une erreur locale. Ce point rejoint l’exigence de lectures bornées d’[E73](../../specifications/epic-73-animation-et-ou-coffrets/architecture-contrats.md).

**Recette.** Mesurer le nombre d’appels sur un volume représentatif ; ouvrir une chasse sans parcourir toute la bibliothèque. Simuler lenteur, erreur partielle et résultat vide ; aucune panne n’est présentée comme une absence de dossiers. Aucun POST n’est rejoué automatiquement.

### UX-25 — P2 — Faire des batchs un poste de diagnostic

**Constat C.** La console empile raccourcis, fiches de traitements, métadonnées, ordonnancement ouvert et commandes manuelles. Les dernières exécutions sont limitées à 30 sans recherche/pagination dans ce rendu. Source : [admin.py](../../../../localeo-backend/app/infrastructure/admin/admin.py), lignes 5276–5368.

**À traiter.** Tableau filtrable par traitement, famille et état ; détail du diagnostic et de la procédure ; configuration et payloads secondaires. Séparer clairement simulation, lorsqu’elle existe, et exécution.

**Recette.** Retrouver un échec parmi plusieurs familles, consulter son diagnostic puis revenir. Distinguer jamais exécuté, désactivé, erreur de lecture et échec. Une consultation ne déclenche aucune opération.

### UX-26 — P2 — Relier Audit et Web Push aux dossiers métier

**Constat C.** Audit expose des codes d’action/phase/ressource ; Web Push demande un destinataire exact et renvoie aux batchs sans cibler le traitement du canal. Sources : [audit.js](../../../../localeo-backend/app/infrastructure/erp/audit.js), lignes 104 et 138 ; [webpush.js](../../../../localeo-backend/app/infrastructure/erp/webpush.js), lignes 157 et 172.

**À traiter.** Entrées contextuelles depuis les dossiers autorisés, libellés métier avec valeur source consultable, critères techniques avancés, lien vers le diagnostic précis et retour conservé.

**Recette.** Partir d’un dossier, consulter le bon événement ou canal sans recopier son UUID et revenir au même filtre. Une installation Live ne devient pas une identité habitant ; une acceptation fournisseur ne devient pas une preuve de lecture ou de réception.

### UX-27 — P2 — Recentrer la fiche utilisateur sur son accès

**Constat C.** Le formulaire complet identité/profil/habilitations précède les informations d’invitation et les actions de récupération. Source : [utilisateurs-internes.js](../../../../localeo-backend/app/infrastructure/erp/utilisateurs-internes.js), lignes 54 et 113.

**À traiter.** Bandeau identité/état/profil, invitation et dernière connexion disponible, action contextuelle ; sections Informations, Habilitations et Sessions. L’édition devient explicite.

**Recette.** Pour une demande « je ne peux plus me connecter », l’administrateur voit l’état et le dernier envoi avant de modifier des droits. Aucun changement de profil n’ajoute ou ne retire silencieusement une autorisation ; retraits et renvois gardent leurs confirmations.

### UX-28 — P2 — Compléter le gabarit commun par des composants de contenu

**Constat V/S/C.** La coque et l’en-tête sont mutualisés. Le contenu intérieur reste largement assemblé dans chaque module. La classe générique `.panel` apporte surtout une animation, sans définir une structure de dossier ; les pages l’utilisant seules ne bénéficient donc pas d’une hiérarchie complète. Les tests du gabarit n’examinent pas la pertinence de l’action métier. Sources : [page-layout.js](../../../../localeo-backend/app/infrastructure/erp/page-layout.js), [page-layout.css](../../../../localeo-backend/app/infrastructure/erp/page-layout.css), [erp.css](../../../../localeo-backend/app/infrastructure/erp/erp.css), ligne 1.

**À traiter.** Définir des composants de présentation pour identité de dossier, état expliqué, action principale/secondaire, liste filtrée, résumé de décision, erreur locale et historique. Prévoir des espaces et séparateurs cohérents ; réserver les encadrés aux ensembles qui doivent être distingués. Sur écran intermédiaire, éviter les mots d’action coupés. Avec texte doublé, réduire les répétitions de navigation avant la tâche sans supprimer les repères.

**Recette.** Vérifier chaque famille avec données longues et réelles, droits restreints, liste pleine, erreur et vide. Évaluer au clavier, zoom et mobile. WCAG 2.2 prévoit une cible de 24 × 24 CSS px avec exceptions ; une cible de 44 px peut rester l’objectif de confort interne pour les commandes principales. Le focus doit rester visible, notamment sous les éléments fixes. [Cibles de pointage](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [focus non masqué](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).

### UX-29 — P3 — Équilibrer l’accueil et faire évoluer les hubs vers le travail quotidien

**Constat V/C.** L’accueil place déjà les dossiers d’équipe avant les compteurs, mais une page de 25 dossiers repousse alertes et autres accès. Le hub Animation possède une grille descriptive sans synthèse des demandes à traiter. Sources : [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 562–581 et 602–607.

**À traiter.** Tester un aperçu limité des dossiers, avec accès explicite à la file complète, et une visibilité équilibrée des autres tâches. Pour Animation, ajouter éventuellement demandes à vérifier et préparations à reprendre, seulement si des projections fiables sont disponibles. Afficher périmètre, date et indisponibilité.

**Recette.** Un gestionnaire repère ses catégories de travail sans traverser 25 lignes. Les indicateurs ouvrent les listes correspondantes. Ne pas créer une fausse file personnelle à partir d’un responsable en texte libre ; conserver la notion d’équipe tant que le domaine ne porte pas l’affectation.

### UX-30 — P3 — Aligner l’aide sur les menus réellement livrés

**Constat documentaire.** Le [guide de prise en main](../../produit/formation/backend/guide-prise-en-main-erp.md) décrit la navigation actuelle par sous-groupes. Le [guide du menu Animation](../../exploitation/exploitation/menu-animation-erp.md) décrit encore d’anciens groupes et ancres comme `#souscriptions` ou `#animations`.

**À traiter.** Lors de la prochaine évolution, actualiser cette source, les intitulés de formation et les captures utiles. Éviter que le support donne des noms de rubriques différents de ceux de l’interface.

**Recette.** Un nouvel utilisateur rejoint les pages citées depuis les libellés du guide, sans interpréter d’anciennes entrées. Vérifier les liens et conserver une seule description canonique par parcours.

## 7. Acquis à conserver

- **Commerçants** : identité et commune en liste, recherche, filtres, pagination, reprise locale, synthèse et actions contextuelles constituent une base interne réutilisable.
- **Demandes de création Animation** : file, détail, état, prochaine action, étapes et détails techniques repliés montrent déjà la bonne direction pour les opérateurs.
- **Accès et modules** : droits effectifs, permissions, droits commerciaux et quotas sont distingués. Une refonte visuelle doit conserver ces distinctions.
- **Paiements et reversements ERP** : états inconnus, devises, montants, transferts Stripe et réception bancaire ne sont pas confondus ; les recherches privées et retours sont déjà pris en charge.
- **Support organisations** : réponse principale, échanges, notes internes et délais sont différenciés. Les compteurs limités à la page sont annoncés comme tels.
- **Reprise des commandes** : confirmations, versionnement, idempotence et traitement du résultat incertain existent dans plusieurs modules. Leur réutilisation doit accompagner la nouvelle mise en page.

## 8. Ordre de traitement proposé

Les lots ci-dessous sont une proposition de découpage, pas une nouvelle roadmap validée. Aucun statut d’epic n’est modifié par cet audit.

| Lot | Contenu | Dépendances et sortie attendue |
| --- | --- | --- |
| **A — Références de page** | UX-01, UX-02, socle UX-28 | Maquettes et composants éprouvés sur un hub et une préparation accompagnée. Coque existante conservée ; premier bénéfice visible sur la demande initiale. |
| **B — Incohérences d’usage** | UX-04, UX-09, UX-10, UX-11, UX-22 | Correctifs ciblés des droits présentés, saisies, pagination, destination et légendes. Tests de comportement précis ; pas besoin d’attendre une refonte générale. |
| **C — Décisions et cibles** | UX-03, UX-05, UX-06, UX-07, UX-08, UX-19 | Dossiers identifiés, portées explicites, décisions relues. Dépend de projections nommées ou d’aperçus métier lorsqu’ils manquent. |
| **D — Listes et continuité** | UX-12 à UX-18, UX-20, UX-21, UX-23, UX-27 | Tableau/liste/fiche harmonisés, contexte et focus conservés, consultation séparée de l’édition. |
| **E — Exploitation et consolidation** | UX-24 à UX-26, finition UX-28, UX-29, UX-30 | Lectures bornées, diagnostics ciblés, recette complète, accueil affiné et aide alignée. UX-24 peut être avancé si des lenteurs sont constatées. |

Les lots A et B peuvent progresser séparément ; les commandes sensibles du lot C doivent être examinées tôt. Estimer l’effort après inventaire des projections disponibles : une traduction de libellé, une restauration de page et un aperçu financier calculé par le domaine ne représentent pas le même travail.

### Impacts techniques à anticiper

| Surface | Implication pour une future réalisation |
| --- | --- |
| Frontend ERP et consoles historiques du backend | Principal périmètre d’évolution. Éviter de reconstruire une bibliothèque de présentation différente pour chaque module. |
| Domaine et orchestration | Les transitions, droits, éligibilités, calculs, dates et périmètres de commande restent côté backend. L’interface consomme des faits et actions autorisées. |
| Contrats/projections de lecture | Certains besoins exigent noms, références, résultats paginés ou aperçu de portée. Vérifier producteur et consommateurs avant d’ajouter des champs ; mettre à jour les contrats canoniques dans `localeo-projet`. |
| Live, Animation et Pro | Aucune modification imposée par cet audit. Réévaluer les impacts si une projection ou un contrat partagé change. |
| Documentation fonctionnelle et ops | Adapter les parcours et procédures aux nouveaux libellés, retours et confirmations. Le rapport reste la photographie initiale. |
| Migrations | Aucune migration nécessaire pour ce rapport ni présumée pour une mise en page. Un besoin futur de données ou d’affectation métier doit être évalué explicitement. |
| Démonstration | Prévoir dossiers nommés, états variés, plus d’une page de résultats, homonymes, droits restreints, montants et versions. Le générateur peut nécessiter un ajustement si les contrats changent. |
| Mesure et confidentialité | Mesurer durée, réussite et erreurs sans enregistrer le contenu des formulaires, recherches personnelles ou données client dans une télémétrie de navigation. |

## 9. Validation et mesure de l’amélioration

### Vérification exécutée pour cet audit

La commande `node tests/browser/erp-page-template.cjs`, dans le backend, a terminé avec **24 scénarios réussis**. Elle utilise des réponses simulées locales pour `operations`, `finance`, `animation`, `commercants/nouveau`, `coffrets` et `commercants`. Elle vérifie notamment présence du titre, fil d’Ariane, retour, actions attendues, menu mobile et absence de débordement horizontal global.

Les captures sont conservées comme sorties de travail non versionnées dans `.artifacts/erp-page-template/`. Le texte doublé est une simulation d’agrandissement des polices, pas une preuve complète de fonctionnement avec le zoom du navigateur. Les listes de cette fixture sont vides : ce succès ne prouve ni la lisibilité des tableaux remplis ni la pertinence de la prochaine action. Aucun test métier ou commande réelle n’a été exécuté pour cet audit.

La vérification documentaire `python scripts/check_guidance.py --document docs/audits/backend/localeo-erp-ux-pages-gestion-2026-11-13.md --document docs/audits/INDEX.md` a réussi : **99 guides, 1 350 liens locaux, aucune erreur ni avertissement**. Les contrôles d’export ne sont pas concernés : ce rapport et son entrée d’index ne modifient aucune source exportée ni aucun contrat consommé par une application.

### Recette à prévoir lors de la réalisation

| Scénario | Résultat observable |
| --- | --- |
| Gestionnaire débutant cherche un dossier | Il choisit la destination sans connaître son nom technique et retrouve l’objet parmi des homonymes. |
| Préparation à compléter puis en attente | Il voit qui doit agir, les éléments manquants et l’action autorisée ; la validation terrain reste distincte du service Localeo. |
| Profil Lecteur puis gestionnaire | Consultation et écriture sont cohérentes ; aucune saisie inutile avant un refus prévisible. |
| Liste de plus de 25 résultats | Dernier résultat accessible ; fiche et retour conservent filtre, page et focus. |
| Formulaire modifié puis actualisation | Pas de perte silencieuse ; choix explicite avant abandon, conflit et expiration traités. |
| Décision globale depuis une vue filtrée | Portée réelle annoncée avant confirmation ; le filtre de lecture n’est pas pris pour le périmètre d’exécution. |
| Erreur API ou résultat incertain | L’écran distingue panne, vide, refus et commande non confirmée ; reprise ciblée sans double action. |
| Bureau, écran intermédiaire, mobile, texte agrandi | Identité, état et action restent lisibles ; pas de mot d’action illisible ni de valeur sans légende. |
| Parcours intégral au clavier | Focus visible et logique, onglets annoncés, retour à l’élément d’origine, confirmations compréhensibles. |
| Préparation avec bibliothèque volumineuse | Nombre d’appels borné ; le premier contenu utile ne dépend pas du parcours de toutes les pages de bibliothèque. |

Pour mesurer la productivité, comparer les mêmes tâches avant/après avec des gestionnaires débutants et réguliers : temps pour trouver le dossier, temps pour identifier l’action correcte, erreurs de cible/portée, allers-retours inutiles, pertes de saisie et demandes d’aide. Recueillir aussi la compréhension de l’état et la confiance dans le résultat. Définir les objectifs chiffrés après une première mesure, plutôt que promettre un pourcentage de gain sans référence.

Le livrable de la prochaine phase devrait réunir des écrans de référence avec données représentatives, leurs critères de recette et le rattachement de chaque point à un lot. Une validation limitée à la présence d’un en-tête ou à un build réussi ne suffira pas à démontrer l’amélioration de l’usage quotidien.
