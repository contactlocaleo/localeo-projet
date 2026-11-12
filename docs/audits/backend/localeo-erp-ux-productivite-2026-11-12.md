# Localeo ERP — audit UX et productivité — 12 novembre 2026

Audit demandé avec les workflows d'évolution et de spécification. Le périmètre
est le poste de travail **Localeo ERP**, principalement accueil, navigation,
commerçants, coffrets, diagnostic, consultations financières, instances et accès
internes. La cible est rattachée à
[E60-EVOL-UX-20261112](../../specifications/epic-60-vision-360-commercialisation/ux-productivite.md).
L'EPIC 60 conserve sa clôture historique. Ce document est la photographie avant
changement ; la réalisation demandée ensuite, ses preuves locales et ses réserves
sont suivies dans la spécification liée ci-dessus. Les constats ci-dessous ne
sont pas réécrits rétroactivement après les corrections.

## Conclusion

Le gain attendu vient d'abord de la continuité : **retrouver un dossier → agir →
comprendre le résultat → reprendre exactement son travail**. Le code contient
déjà de bons composants, mais leurs garanties diffèrent selon les écrans.

1. **Éviter le travail perdu ou répété** : conserver l'origine d'une fiche,
   traiter distinctement panne réseau, refus et expiration, fiabiliser la reprise
   d'un enregistrement dont la réponse a été perdue.
2. **Mettre le travail à traiter avant les explications générales** : dossiers
   et alertes dès l'accueil, progression contextualisée dans les coffrets,
   recherche courante courte et filtres techniques repliés.
3. **Étendre les bonnes pratiques existantes** : retours Finance, erreurs et
   recherche Commerçants, confirmations contextualisées des commandes Animation.

Aucun pourcentage de productivité, temps économisé ni score global d'utilisabilité
n'est mesuré. Les priorités sont une appréciation experte de la gravité potentielle,
de la transversalité et de la répétition probable, à confronter aux usages réels.

## Méthode et limites

- Backend examiné : `9b2b41a340b79322450aabafa767307afbbc6096`, arbre propre au
  démarrage. Projet : base `b6675672a986171ad2ef0c9f9cef763702ab403a`, avec des
  modifications E73/roadmap/spécifications antérieures conservées.
- Revue du code, des exigences E60 et des extensions E65/E69 ; références de
  lignes correspondant à cette base. Les états historiques d'E60 ne remplacent
  pas les scopes globaux et profils courants d'E69.
- **C** : fait établi par lecture du code. **H** : conséquence ou opportunité à
  confirmer en usage. Un scénario déduit du code n'est pas un test exécuté.
- **Aucune observation visuelle ERP réalisée.** Le navigateur connecté n'était
  pas disponible ; la tentative via la fenêtre Chrome a été arrêtée par l'outil,
  incapable de vérifier l'URL courante. Aucun autre accès UI n'a été utilisé.
- Une revue indépendante a examiné un extrait transmis de `erp.js` (sessions,
  formulaires, onglets, accueil). Les sous-agents ne disposaient pas de lecture
  filesystem ; cette revue n'est donc pas un second audit complet du dépôt.
- Aucun serveur lancé, aucune base consultée/modifiée, aucun envoi ni commande
  financière exécuté. Tests applicatifs et tests utilisateurs non exécutés.

Cet audit est exploitable pour prioriser et préparer les corrections. Il ne
certifie ni le rendu déployé, ni l'accessibilité, ni la performance de TEST.
Contrastes, densité réellement perçue, zoom, cibles tactiles, lecteurs d'écran,
appareils physiques et représentativité des données restent à vérifier.

## Parcours et couverture

| Parcours / acteur | Couverture réelle | Limite |
| --- | --- | --- |
| Arrivée et reprise de dossier / Backoffice | Accueil, API activité, navigation, contrôles d'accès lus | Pas de session nominative observée ; fréquence et volume non mesurés |
| Recherche commerce → fiche → prestation | Liste et fiche, filtrage, retours, formulaires lus | Pas de création/enregistrement exécuté |
| Indisponibilité → coffret → correction → diagnostic | Filtres, composition, fiscalité et commandes lus | Aucune publication, qualification ou réévaluation |
| Paiement/reversement → détail → résultats / Finance | Module de consultation lu comme référence de continuité | Pas de rapprochement ni recette comptable ; consoles spécialisées non auditées intégralement |
| Recherche instance → client → support | Recherche, résumé, objets associés, notes et onglets lus | Actions sensibles et SQLAdmin seulement repérés, pas audités écran par écran |
| Utilisateurs → fiche → retour / Admin | Liste, pagination, détail, invitations et reconnexion lus | Aucun compte ni invitation créé |
| Interruptions et clavier | Gestion réseau/session, DOM et sémantique des onglets lus | Pannes, délais inversés, focus et lecteur d'écran à reproduire |
| Satellites | Points de passage ERP repérés | CRM, OnBoard, Atelier, Ops, Control et portail Animation ne sont pas intégralement réaudités |

## Acquis à conserver

- Menu ERP commun filtré par droits, rubrique active et fermeture mobile par Échap :
  [erp-navigation.js](../../../../localeo-backend/app/infrastructure/erp/erp-navigation.js),
  lignes 76–119. Le gabarit comporte un lien d'évitement, un titre et un retour.
- Commerçants : filtres explicites, résumé des critères, pagination, vide contextualisé,
  reprise d'erreur et conteneur propre à chaque onglet :
  [erp.js](../../../../localeo-backend/app/infrastructure/erp/erp.js), lignes 139–159 et 185–223.
- Finance : historique et retour aux résultats, restauration du focus, annulation
  des lectures périmées, filtres avancés repliés, recherche libre conservée en
  mémoire de l'onglet plutôt que dans le lien partagé :
  [finance-consultation.js](../../../../localeo-backend/app/infrastructure/erp/finance-consultation.js),
  lignes 30–110 et 184–201.
- Prévention de sortie non enregistrée, boutons bloqués pendant les enregistrements,
  saisie monétaire en euros et explications avant publication : `erp.js`, lignes
  73–76, 124–159, 472 et 531–532. Il ne manque donc pas une protection générale
  contre toute perte de saisie ; les défauts concernent certains chemins de reprise.
- Commandes Animation : prochaine étape, effets expliqués, actions selon capacités
  et confirmation explicite :
  [animation-commercial.js](../../../../localeo-backend/app/infrastructure/erp/animation-commercial.js),
  lignes 55–87. Instances : objets associés chargés à la demande et paginés :
  [instances.js](../../../../localeo-backend/app/infrastructure/erp/instances.js), lignes 73–94.

## Constats prioritaires

**P1** : risque de perte, de répétition ou d'information erronée dans une tâche.
**P2** : effort de recherche, de compréhension ou de navigation. Effort **S** =
localisé, **M** = plusieurs écrans/états ; estimation relative, pas un devis.
Les fichiers référencés ci-dessous sont ceux liés dans les acquis ou les preuves.

| ID | Priorité / effort | Fait et preuve C | Conséquence H et optimisation proposée |
| --- | --- | --- | --- |
| ERP-UX-01 | P1 / M | `erp.js:32–47,225–230` : la liste Disponibilité ouvre `/coffrets/{id}` ; le retour est déduit du parent `/coffrets`. Le referrer n'est repris que si son chemin égale ce parent. | Le retour explicite depuis une indisponibilité mène à la liste Coffrets et perd les filtres de diagnostic. Porter une origine validée et conserver page, tri, filtres, ligne et position. Le retour immédiat depuis la liste Commerçants peut déjà reprendre ses paramètres : ne pas généraliser le défaut. |
| ERP-UX-02 | P1 / M | `erp.js:6–10` : au retour dans un onglet, toute erreur du GET contexte appelle `clearPrivate()`, qui vide contenu et indicateur de saisie modifiée. | Une panne transitoire peut effacer une saisie. Maintenir le contenu masqué et les commandes bloquées pendant une vérification relançable ; restaurer uniquement après confirmation de la même identité et des mêmes droits. Révocation et expiration gardent leurs protections. |
| ERP-UX-03 | P1 / M | `erp.js:24` traite ensemble 401 et 403 comme « Session expirée ». Le contrat E60 distingue session, permission et CSRF. | Un refus sur une action peut entraîner reconnexion et perte de contexte inutiles. Séparer les états et revalider le contexte ; n'exposer aucune donnée devenue interdite. Un 403 ne prouve pas à lui seul une expiration. |
| ERP-UX-04 | P2 / M | `erp.js:522–546` : applications, puis synthèse, puis dossiers, puis alertes ; trois lectures séquentielles. Une erreur non traitée localement atteint le catch global qui remplace tout le contenu. L'exigence E60 place les actions avant les compteurs. | L'utilisateur attend et cherche son travail plus bas ; un bloc défaillant masque les autres. Présenter d'abord les dossiers/alertes, charger les blocs indépendamment et permettre une reprise locale. Le délai réel et la place au premier écran restent à mesurer. |
| ERP-UX-05 | P2 / M | `erp.js:225–230` : onze champs de filtrage au même niveau, dont « Code du blocage » et « UUID commerçant ». | Charge de lecture et copier-coller d'identifiants. Garder recherche, commune et disponibilité directement accessibles ; replier les autres critères avec compteur actif. Sélectionner un commerce par nom/commune via une recherche bornée. Finance fournit déjà un modèle de filtres avancés. |
| ERP-UX-06 | P2 / M | `erp.js:80–89,466–470` : chaque fiche coffret place quatre indicateurs, l'avertissement BUM et le guide complet de cinq étapes avant les onglets. | L'aide générale repousse la tâche d'un utilisateur régulier. Afficher une progression compacte et le prochain contrôle pertinent ; garder l'aide détaillée à la demande et rappeler les conséquences BUM près de la commande concernée. Aucun problème de hauteur mesuré. |
| ERP-UX-07 | P2 / S | `erp.js:30,225–228,504,511` affiche des codes `NON_VENDABLE`, `REFERENCE`, `OPEN`, `PUBLISHED`. Le badge générique classe tout état hors listes connues en `fail`. | Décodage mental et signaux négatifs ambigus. Traduire par vocabulaire métier et attribuer une tonalité par objet ; un brouillon, une nature technique ou une archive n'est pas automatiquement un échec. La liste Commerçants possède déjà ses libellés et tons explicites. |
| ERP-UX-08 | P1 / M | `erp.js:24,124–137,253–263,469` : l'appel générique génère une clé d'idempotence quand aucune n'est fournie ; le formulaire générique ne conserve pas de clé stable entre deux soumissions identiques. | Après écriture réussie et réponse perdue, « Réessayer » peut être traité comme une nouvelle commande : doublon ou conflit selon l'opération. Conserver clé et payload jusqu'à résolution ; distinguer échec certain et résultat inconnu. Ce risque n'est pas une preuve de doublon observé. Instances et Utilisateurs offrent déjà des patterns de clé stable. |
| ERP-UX-09 | P2 / M | `erp.js:23–24,124–137` : les erreurs serveur sont concaténées, notamment via les chemins `loc`, puis affichées dans le statut global précédant le contenu. | L'utilisateur doit retrouver le champ et peut manquer visuellement le retour après défilement. Rattacher les erreurs aux champs, fournir un résumé focalisable et une reprise explicite des conflits. L'annonce `role=alert/status` existe déjà ; ne pas déclarer les erreurs silencieuses pour tout lecteur d'écran. |
| ERP-UX-10 | P1 / M | `erp.js:139–159,473–477` : les onglets Coffrets partagent le même `body`. Le compteur de révision protège catch/finally, mais pas l'ajout tardif après `await` de Fiscalité. `instances.js:110–117` réutilise aussi un corps de page. | Des réponses inversées peuvent mélanger le contenu d'un ancien onglet à l'onglet actif. Utiliser un conteneur par rendu ou invalider toutes les écritures périmées ; ne conserver interactif que le dernier choix. Les onglets Commerçants utilisent déjà un conteneur détachable. |
| ERP-UX-11 | P2 / S | `erp.js:147,151,155–158` : tabIndex, IDs, `aria-controls` et association du panneau sont conditionnés par `options.className`, fourni pour Commerçants mais pas pour Coffrets. Les flèches activent automatiquement l'onglet et sa lecture réseau. | Navigation clavier inégale et relations onglet/panneau incomplètes dans les Coffrets. Harmoniser le composant, un seul onglet dans l'ordre de tabulation, liens sémantiques complets ; activation explicite si contenu non instantané. Validation au lecteur d'écran nécessaire. |
| ERP-UX-12 | P2 / M | `admin_session.js:26–27,54,97`, `admin_session.py:75` et `identite-interne.js:51–53` : le monitor fournit une connexion sans destination ERP ; le formulaire n'accepte comme retour que certaines routes CRM, sinon accueil ERP. | Après reconnexion, retrouver manuellement la fiche. Préparer une destination ERP locale autorisée, sans donnée saisie ni secret ; recontrôler les droits avant retour. La durée de session ne change pas. Aucune récupération de brouillon après expiration n'est promise. |
| ERP-UX-13 | P2 / S | `utilisateurs-internes.js:85–96,106–109` : pagination et détail en callbacks sans URL de fiche ; « Revenir à la liste » appelle `liste()` donc page 1. | L'administration répétée de comptes perd sa position ; une fiche ne se rouvre pas par un lien dédié. Conserver la page et le focus, fournir une destination stable sous contrôle d'accès. Les filtres de recherche restent dans l'URL : ne pas affirmer leur disparition générale. |
| ERP-UX-14 | P2 / S | `erp-navigation.js:49–59,94–107`, `erp.js:515–529,544` : navigation par rubriques, pages de raccourcis et applications ; recherche des destinations limitée à l'administration par objet. | Opportunité, sans preuve de difficulté réelle : un accès clavier « Aller à… » sur les seules destinations autorisées pourrait raccourcir les gestes fréquents. Valider l'utilité avec utilisateurs réguliers avant favoris, récents ou recherche fédérée. |

Preuves complémentaires :
[monitor JS](../../../../localeo-backend/app/security/admin_session.js),
[session serveur](../../../../localeo-backend/app/security/admin_session.py),
[connexion](../../../../localeo-backend/app/infrastructure/erp/identite-interne.js),
[utilisateurs](../../../../localeo-backend/app/infrastructure/erp/utilisateurs-internes.js),
[API activité](../../../../localeo-backend/app/api/erp_api.py) lignes 172–181,
[exigences E60](../../specifications/epic-60-vision-360-commercialisation/specifications-fonctionnelles.md)
sections 3 et 10.

Les constats 02, 03, 08 et 10 demandent une reproduction technique ciblée avant
correction ; ils ne deviennent pas des évolutions de règles métier. Le 04 comporte
un écart à la hiérarchie déjà attendue et une amélioration de résilience. Les autres
propositions précisent ou étendent les interactions. Aucune anomalie n'est déclarée
corrigée par cet audit.

## Priorisation et mise en œuvre proposée

| Ordre | Lot de la spécification | Résultat quotidien | Dépendance |
| --- | --- | --- | --- |
| 1 | L02 — Reprise et chargements fiables | Pas de travail effacé pour une panne passagère ; panneau toujours cohérent | Reproductions 02/03/10, politique de session conservée |
| 2 | L01 — Continuité des dossiers | Retour à sa liste, sa page et sa ligne ; reconnexion au bon dossier | Destination autorisée, même identité et droits réévalués |
| 3 | L03 — Enregistrement compréhensible et rejouable | Résultat certain, erreurs actionnables, aucune répétition aveugle | Reçu d'idempotence/version existant |
| 4 | L04 — Accueil orienté travail et mesure | Dossiers et alertes prioritaires, périmètre compréhensible | Pas d'assimilation d'un responsable en texte libre à une identité |
| 5 | L05 — Catalogue plus lisible | Recherche courte, moins de codes, aide au bon endroit | Diagnostic et règles BUM serveur conservés |
| 6 | L06 — Navigation et clavier | Accès rapide aux fonctions et onglets cohérents | Recherche de destinations seulement ; utilité à valider |

Les critères et dépendances sont décrits dans l'unique
[spécification de l'évolution](../../specifications/epic-60-vision-360-commercialisation/ux-productivite.md).
Les actions financières groupées, publications automatiques, brouillons persistants,
recherche de toutes les données et personnalisation multi-applications ne sont pas
retenus par défaut : ils demanderaient un cadrage propre.

## Mesurer l'effet sur le quotidien

Prévoir une observation avant/après avec 5 à 8 utilisateurs couvrant Backoffice,
Finance, lecture seule et Admin. Ce nombre sert à une étude formative, pas à
démontrer un gain statistique. Faire exécuter les mêmes tâches sur des données
synthétiques comparables, sans enseigner d'abord le chemin attendu.

1. Retrouver un commerce, consulter une prestation, revenir au même résultat.
2. Partir d'un filtre d'indisponibilité, identifier le blocage, ouvrir le traitement
   puis retrouver la file ; vérifier le refus si l'acteur n'a pas le droit.
3. Corriger un formulaire après 422 et 409 ; distinguer un enregistrement incertain
   et un échec certain sans créer deux ressources.
4. Retrouver un paiement et sa pièce, revenir aux résultats et à la période.
5. Reprendre une fiche après interruption réseau, changement d'onglet et reconnexion.
6. Pour l'Admin, ouvrir un compte en page 2 et revenir à sa position.

Relever réussite sans aide, durée médiane et dispersion, retours arrière, filtres
ressaisis, champs ressaisis, reprises d'erreurs et appréciation de facilité de 1 à 7.
Rapporter les refus attendus séparément des échecs. Ne pas mélanger temps d'attente
serveur et temps de décision humaine. Cibles proposées : aucun contexte perdu dans
les scénarios prescrits, aucune double commande lors d'une reprise, réduction des
recherches répétées ; objectif de temps seulement après une mesure initiale.

## Repères d'accessibilité et statut des preuves

Les recommandations sur les erreurs suivent l'identification textuelle du champ
et de la nature du problème décrite par le
[W3C — Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html).
Les retours de chargement/succès doivent être perceptibles par les technologies
d'assistance selon
[W3C — Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).
Le modèle d'onglets et le choix d'activation selon la latence s'appuient sur
[W3C — Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/).
Références consultées le 12 novembre 2026 ; elles ne constituent pas une certification.

**Exécuté :** revue statique et revue indépendante limitée à l'extrait transmis.
**Non exécuté :** recette UI, tests de panne, tests applicatifs, accessibilité
instrumentée, mesure de capacité et étude utilisateurs. Les contrôles documentaires
de cette livraison sont consignés dans la spécification.
