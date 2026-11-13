# E60-EVOL-UX-20261112 — UX quotidienne et productivité de Localeo ERP

Conception et implémentation locale du **12 novembre 2026**, issues de
[l'audit ERP](../../audits/backend/localeo-erp-ux-productivite-2026-11-12.md).
L'audit et la spécification ont été suivis de la demande d'implémentation. L'
[EPIC 60](../../roadmap/terminees/epic-60-vision-360-commercialisation-backlog.md)
reste **Terminée** pour son périmètre historique. Les six lots de cette évolution
sont implémentés dans le backend ; le [bilan local](#bilan-dacceptation-local)
distingue leurs preuves des réserves. **CA-20 reste ouvert** : aucun gain humain
mesuré, aucune recette TEST ni validation de capacité. Aucun déploiement effectué.

## Objectif et décisions de conception

Rendre la boucle trouver → consulter/agir → comprendre → reprendre plus courte et
fiable. Le périmètre appartient à E60 (shell ERP, référencement, coffrets et
activité), avec dépendances E65 pour les consultations et E69 pour les accès.
La [roadmap commune](../../roadmap/README.md) conserve ses états ; aucun nouvel
arbitrage de droits, fiscalité, paiement ou publication n'est introduit.

| Référence | Choix et portée |
| --- | --- |
| E60-UX-D01 | Réutiliser les composants et contrats existants, et étendre les garanties Finance/Commerçants aux parcours moins homogènes. Pas de nouvelle stack. |
| E60-UX-D02 | Traiter les écarts aux exigences existantes comme correctifs à reproduire ; l'audit ne vaut pas reproduction navigateur. Les autres critères sont des évolutions d'interaction. |
| E60-UX-D03 | Préserver une saisie seulement en mémoire de l'onglet pendant une panne transitoire, masquée et non soumissible jusqu'à revalidation. Expiration, changement d'identité et retrait de droits restent autoritaires. Aucune récupération persistante après déconnexion. |
| E60-UX-D04 | Améliorer les accès par rôle sans élargir les capacités. Le menu reste rattaché aux domaines ; SQLAdmin et les commandes d'argent restent réservés selon E69. |
| E60-UX-D05 | L'accueil présente le travail autorisé et les alertes avant les compteurs. Les accès directs aux applications restent visibles, conformément à l'organisation acquise d'E60. |
| E60-UX-D06 | Ne pas créer « Mes dossiers » à partir des noms libres de responsable. L'API activité actuelle n'a ni identité d'assignation fiable ni filtre personnel. La proposition conserve une file d'équipe explicitement nommée. |
| E60-UX-D07 | Les gains humains sont à mesurer. Les budgets techniques existants ne sont pas une preuve de productivité. Les priorités et efforts de l'audit restent des estimations. |

## Parcours avant / après et lots

Les critères canoniques sont dans le
[backlog](../../roadmap/terminees/epic-60-vision-360-commercialisation-backlog.md#évolution-du-12-novembre-2026--ux-quotidienne-et-productivité).
Les comportements ci-dessous définissent la cible. Les tests exécutés et les
limites de leur couverture figurent dans la matrice et le bilan local.

### L01 — Continuité des dossiers — CA-01, 02, 03, 19

**Avant :** l'origine Disponibilité n'est pas le parent structurel d'une fiche
coffret ; la pagination Utilisateurs est locale ; la connexion ne restaure pas
la destination ERP. **Après :** chaque entrée conserve un contexte de retour validé.

- Sur liste, mémoriser destination, filtres, tri, page, ligne et position avant
  d'ouvrir une fiche. Revenir par le bouton explicite et par l'historique restaure
  la même recherche ; ne pas refaire une recherche globale au retour.
- En nouvel onglet ou arrivée directe, un parent structurel autorisé reste
  disponible. Une origine absente, mal formée ou interdite utilise ce repli.
  Une liste devenue vide propose la première page en conservant ses filtres.
- Utilisateurs utilise une URL UI sous `/internal/erp/utilisateurs` avec
  `utilisateur=<UUID>` et `page` pour la fiche et son origine ; lecture du détail
  via l'API existante. Ancienne URL sans paramètre conservée. Aucun email dans ce
  paramètre ; entrée invalide ou refusée affiche un état utile, pas un autre compte.
- Pour la reconnexion, construire une destination relative ERP dans une liste
  fermée de routes et paramètres autorisés. Ne pas transporter formulaire,
  email/téléphone de recherche, token ou URL externe. Préserver seulement le
  chemin, les UUID de ressources autorisées et l'onglet reconnu ; après connexion,
  recontrôler les droits avant lecture. Une identité différente ne récupère pas
  le contexte privé de l'utilisateur précédent.
- Le focus revient à l'action ayant ouvert la fiche si la ligne existe, sinon
  au résumé des résultats. Une restauration de défilement ne masque pas le focus.

La recherche libre Finance reste en mémoire, selon son contrat actuel ; aucune
copie dans une URL partagée pour faciliter la continuité. Pour les autres écrans,
séparer paramètres publics validés et état éphémère. Pas de cache de données métier
dans `localStorage` ni de persistance d'un formulaire.

Implémentation : origine validée dans `history.state`, recherche déjà présente
dans l'URL de la liste ; `sessionStorage` ne contient que douze positions au
maximum (clé hachée de destination, UUID de ligne, défilement et empreinte du
principal/version). Aucune copie des recherches libres, formulaires ou dossiers
dans ce stockage. L'expiration purge les métadonnées et un autre principal ne
peut les restaurer. Finance conserve sa recherche en mémoire, sans changement.

### L02 — Reprise et chargements fiables — CA-04 à 07

**Avant :** une erreur réseau du contexte vide le shell ; 401 et 403 ont la même
conséquence ; un rendu d'onglet périmé peut écrire dans le panneau actif ; un bloc
d'accueil peut faire échouer la page. **Après :** états de reprise explicites.

| Événement | Résultat cible | Refus / effet interdit |
| --- | --- | --- |
| Retour dans l'onglet, réseau indisponible | Contenu privé masqué et actions bloquées ; « Vérification de l'accès indisponible — Réessayer ». Saisie conservée uniquement en mémoire tant que le délai de session connu n'est pas dépassé. | Pas de lecture/commande depuis un contexte non revalidé ; aucune prolongation locale de session. |
| Vérification réussie, même identité et version d'autorisation | Restauration de la saisie et de son état modifié, sans soumission automatique. | Pas de relecture écrasant un formulaire modifié sans traitement explicite. |
| 401, révocation, autre identité ou droits retirés | Invalidation, effacement conforme au contexte, reconnexion/retour vers une destination permise. | Aucune restauration de données interdites et aucun maintien artificiel des délais. |
| 403 de permission ou CSRF | Refus explicite ; relecture du contexte. Si contexte encore valide, les autres fonctions autorisées restent accessibles ; le cas CSRF exige renouvellement sûr avant une nouvelle tentative. | Aucun POST rejoué automatiquement ; un retrait de capacité invalide les données/actions concernées. |
| Changement d'onglet avant réponse | Seul le panneau choisi reste interactif. Réponse ancienne ignorée ou conteneur détaché ; requête annulée si possible. | Aucun mélange d'actions/champs de panneaux ; aucune erreur ancienne masquant le nouveau. |
| Échec synthèse, activité ou alertes | État et bouton de reprise dans le seul bloc concerné ; autres blocs utilisables. | Aucun faux zéro et aucune disparition globale des données disponibles. |

Le shell reste propriétaire des états UI ; la politique d'accès du domaine et le
serveur restent propriétaires de l'autorisation. Ne pas faire dépendre cette
protection d'un simple masquage CSS.

L'identité et la version d'autorisation proviennent de la réponse serveur, jamais
d'une valeur locale choisie par l'interface. Toute purge invalide également les
requêtes, callbacks et rendus en cours : une réponse tardive ne restaure rien.
La distinction permission/CSRF utilise un code serveur stable lorsqu'il existe ;
à défaut, afficher un refus générique et revérifier le contexte, sans inventer
la cause. Une panne réseau n'ouvre aucun délai de grâce d'accès.

### L03 — Enregistrement compréhensible et rejouable — CA-08 à 10

**Avant :** message global et clé générique renouvelée à chaque appel sans clé.
**Après :** une intention d'enregistrement conserve sa clé, son payload et son
état jusqu'à un résultat certain.

- 422 : conserver les valeurs, afficher un résumé descriptif et des liens vers
  les champs nommés ; focus vers le résumé ou premier champ invalide. Les erreurs
  métier sans champ restent dans un bloc local, sans inventer de correspondance.
- 409 de version : expliquer que le dossier a changé ; permettre de consulter
  l'état courant puis d'appliquer à nouveau les changements choisis. Aucun
  écrasement, fusion automatique ou nouvelle version fabriquée côté UI.
- Réponse perdue après POST/PUT : résultat « À vérifier », clé et payload figés ;
  reprise explicite de la même intention via le reçu d'idempotence existant.
  Empêcher d'autres commandes contradictoires jusqu'à résolution. Après résultat
  certain seulement, une modification du payload produit une nouvelle intention.
- La résolution utilise la répétition du même appel avec la même clé dans la
  fenêtre existante de **24 heures**, qui restitue le résultat initial sans nouvel
  effet. Une même clé avec un autre payload reste refusée en 409. Si la clé est
  perdue (fermeture/rechargement) ou le reçu expiré, ne pas présenter une nouvelle
  soumission comme une reprise garantie : proposer une vérification du dossier
  et de la corrélation par les lectures/outils autorisés. Ce lot n'introduit pas
  de conservation persistante de payload ni une garantie au-delà du contrat.
- La préparation d'image fait partie du suivi : conserver la référence d'un
  téléversement confirmé pendant la reprise de la commande, sans téléverser à
  nouveau à chaque clic. Un téléversement lui-même incertain exige une résolution
  explicite ; ne pas le déclarer réussi ni promettre une transaction distribuée.
- Succès : annoncer ressource et résultat, puis proposer « Continuer la préparation »
  ou « Revenir aux résultats » selon le parcours. Enregistrer ne publie pas,
  ne valide pas la BUM et n'envoie aucun message supplémentaire.

Conserver les confirmations utiles à une transition engageante. Un libellé
« Enregistrer » ne remplace jamais une confirmation de publication ou d'envoi.

### L04 — Accueil orienté travail et mesure — CA-11, 12, 20

**Avant :** applications et compteurs précèdent les dossiers ; lectures en chaîne.
**Après :** titre et accès directs compacts, dossiers/alertes visibles en premier,
indicateurs datés ensuite. Un profil Finance conserve sa consultation financière
sans données de catalogue ajoutées.

La file reste « Dossiers de l'équipe à reprendre » avec responsable, échéance
formatée et prochaine action existants. « À affecter » et « À planifier » restent
explicites. Le tri serveur actuel par échéance, mise à jour et ID est préservé.
Un éventuel filtre « Mes dossiers » ou agrégat « Toutes mes tâches » demanderait
un propriétaire d'affectation et un contrat supplémentaires : hors ce lot.

Les métriques d'usage sont obtenues par la recette formative de l'audit et les
événements minimisés existants. Aucun enregistrement de saisies, contacts, UUID
comme dimensions métriques ou nouvelle télémétrie externe. Publier dans le futur
bilan valeurs avant/après et conditions d'observation ; un gain non mesuré reste H.

### L05 — Catalogue plus lisible — CA-14 à 17

- Recherche, commune et disponibilité visibles ; huit autres filtres sous
  « Filtres avancés », avec nombre de critères actifs. Un résumé décrit tous les
  critères appliqués ; effacement individuel et réinitialisation remettent page 1.
  Les mêmes contraintes API s'appliquent, y compris à une URL ancienne.
- Le filtre commerce présente une recherche nom/login et commune de distinction,
  puis stocke l'UUID sélectionné. Reprendre `/api/commercants` avec page de 25,
  sans télécharger toutes les pages ; annuler/ignorer une réponse périmée.
  Le champ UUID reste facultativement dans l'accès avancé destiné au diagnostic.
- Les valeurs techniques restent inchangées dans les API ; l'interface traduit
  états et familles. Couleur et icône complètent le texte, sans déclarer un état
  inconnu comme réussi. Conserver distincts statut du coffret, vendabilité et BUM.
- Le coffret présente son nom, statut, prix, état de préparation et accès direct
  aux onglets ; le guide long est dépliable. L'étape proposée vient des contrôles
  serveur déjà disponibles ; en cas de diagnostic inconnu, proposer de vérifier
  plutôt que d'inventer une éligibilité. Les conséquences BUM restent annoncées
  au moment de modifier/rattacher, et avant la publication.

### L06 — Navigation et clavier — CA-13, 18

« Aller à une fonction » filtre uniquement les destinations déjà autorisées du
menu ERP. L'absence de résultat permet de retrouver les rubriques ; pas de
recherche sur données métier, de nouvelle capacité ni de parcours automatique.
Activation par bouton/clavier standard ; un éventuel raccourci additionnel ne doit
pas intercepter la saisie et reste à valider avec les utilisateurs.

Le composant d'onglets partage les IDs, associations panneau/libellé et un seul
onglet tabulable. Les flèches déplacent le focus ; Entrée/Espace active une vue
dont le chargement n'est pas instantané. Le focus et l'onglet sélectionné restent
cohérents après refus d'abandon de saisie. Les panneaux exposent chargement, vide,
erreur/reprise et résultat. Recette à 1280, 390 et 320 px et texte à 200 %, sans
défilement horizontal global ; un tableau large peut défiler dans sa propre zone.

## Responsabilités, invariants et contrats

| Règle à conserver | Propriétaire et entrées | Preuve à produire |
| --- | --- | --- |
| Droits courants, révocation et durée de session | Domaine [accès internes](../../../../localeo-backend/app/domaine/identite_acces/acces_interne.py), [politique de session](../../../../localeo-backend/app/domaine/identite_acces/services/politique_session_admin.py) ; adaptateurs `security/erp.py`, monitor et connexion ; E69 fait autorité | Lecteur/Backoffice/Finance/cumul/Admin, 401/403/CSRF, retrait de droit pendant attente et identité différente après reconnexion |
| Enregistrer/rattacher n'accorde pas le droit de publier ; engagements et versions conservés | Domaine [règles atelier](../../../../localeo-backend/app/domaine/commercialisation/services/regles_atelier.py), [vendabilité](../../../../localeo-backend/app/domaine/commercialisation/services/evaluer_vendabilite.py), conditions vendues ; orchestration `ServiceAtelierErp`, API ERP et parcours Atelier | Succès/refus de publication, version obsolète, répétition et état des achats existants ; aucun calcul d'éligibilité dans l'UI |
| BUM et périmètres produits restent distincts du statut commercial | Domaines conformité BUM et onboarding ; services existants sollicités par ERP/OnBoard | Modification invalidante, contrôle absent, droit insuffisant, succès sans publication implicite |
| Consultation financière sans commande d'argent | [E65](../epic-65-vues-erp/README.md) et [E69](../epic-69-acces-internes/README.md) ; projections et gardes actuelles | Retour/filtres/exports inchangés, aucune mutation financière sur GET/actualisation |
| Une intention rejouée n'a pas deux effets | Orchestration ERP, registre `CommandeErpOrm` et [contrat E60](contrats-api.md) ; domaine garde versions et transitions | Commit puis réponse perdue, reprise même clé/payload, refus clé réutilisée autrement et aucun effet externe répété |

Les endpoints métier et leurs schémas ne sont pas remplacés. Producteurs :
`erp_api.py`, contexte/session et API utilisateurs ; consommateurs : shell ERP et
modules de consultation. Extension prévue du paramètre de retour de connexion
aux routes ERP validées ; compatibilité des retours CRM/Atelier à recetter
séparément, sans annoncer que leurs limitations actuelles sont corrigées ici.
Le backend sert les assets et le validateur de retour dans la même livraison.
Les URL existantes restent valides ; un retour mal formé est ignoré.

Le module public `retour-erp.js` ne contient que la validation des destinations.
Le garde HTML et les consultations utilisent aussi `security/navigation_erp.py`
pour transmettre un chemin autorisé et, pour Utilisateurs, son UUID. Les appels
API non authentifiés conservent leur refus HTTP ; seule la navigation HTML est
redirigée. Le fragment d'onglet est conservé par le monitor, car le serveur ne
reçoit pas les fragments d'URL. Aucun formulaire ni contexte d'autorisation ne
transite dans ce retour ; chaque destination reste protégée côté serveur.

Pas de contrat public Marketplace/Pro/Animation modifié par cette conception,
ni de contrat embarqué à régénérer. Le monitor et certains composants servent
plusieurs surfaces backend : toute modification de code devra inclure leurs
tests de non-régression, notamment Support/instances et SQLAdmin/session.

## Données, performance et livraison future

Aucune entité, colonne ni migration requise par la cible retenue. L'état UI est
éphémère, aucune persistance de brouillon ou de préférence. Aucun nouveau statut
de roadmap ou métier. Les fixtures doivent couvrir page 2, filtres actifs,
références supprimées, échec réseau, résultat incertain et droits distincts.
Le générateur de démonstration n'a pas de schéma à changer ; la représentativité
de ses données devra être vérifiée avant recette, sans génération implicite.

| Chemin | Bornes et stratégie | Budget / preuve future |
| --- | --- | --- |
| Accueil | 3 blocs indépendants au maximum après contexte ; activité 25 lignes par défaut/100 maximum, alertes 5 ; aucun polling nouveau | Cibles E60 existantes : p95 liste ≤ 500 ms, détail ≤ 800 ms côté service, environnement documenté. Vérifier affichage indépendant sous latence, p95/p99 et nombre de requêtes ; aucune mesure actuelle. |
| Recherche commerce du filtre | Page de 25, recherche serveur, pas de parcours automatique de pages, une réponse active | Plans PostgreSQL et absence de N+1 sur fixtures N/10N ; conserver les plafonds existants et examiner les offsets profonds avant d'élargir un usage. |
| Retour et onglets | Un panneau interactif ; état d'origine borné à la navigation de l'onglet, aucune collection métier stockée | Réponses inversées, mémoire/DOM après 50 changements, purge à l'expiration ; charge mixte de lecture/écriture sur base jetable. |
| Enregistrement et reprise | Une intention préparée par formulaire ; le shell bloque toute intention contradictoire dans la page tant qu'une commande est incertaine. Pas de retry en boucle ; délais serveur conservés | Reprise après commit, doublon réseau, 409 et 429 ; pas de nouvelle transaction ou concurrence financière. |

Appliquer la [convention performance](../../architecture/transverse/performance-volumetrie.md).
Les budgets de capacité/concurrence et mesures E59 sont à renseigner avant
activation ; ils ne sont pas déduits de la lecture du code ni remplacés par les
contrôles de liens. Une évolution ultérieure des files ou agrégats exigerait
requêtes, index, pagination et contrat propres.

## Matrice de traçabilité et preuves

Tous les chemins de code et de tests ci-dessous sont relatifs au dépôt backend.
Le [guide Backoffice](../epic-69-acces-internes/guide-backoffice.md#travail-quotidien-dans-lerp--évolution-e60-du-12-novembre-2026)
décrit les nouveaux parcours après livraison. Les contrats métier, OpenAPI, rôles,
migrations et trois frontends restent inchangés. Les fixtures sont synthétiques ;
aucune donnée de démonstration, donnée personnelle ou télémétrie nouvelle.

| Critères | Réalisation / propriétaire | Preuves locales | Limites restantes |
| --- | --- | --- | --- |
| 01, 02, 03, 19 — L01 | `continuite.js`, `utilisateurs-internes.js`, `retour-erp.js`, connexion et gardes HTML ; droits serveur inchangés | `erp-productivite.cjs` : origine Disponibilité/page 2, historique, actualisation, focus, arrivée directe, fiche utilisateur, retour sûr et autre profil ; `erp-page-template.cjs`, `commercants-erp-ux.cjs`, `erp-session-dialog.cjs` ; `test_erp_ux_navigation.py` | Recette TEST, nouvel onglet réel et changement de compte sur environnement déployé à compléter ; aucun formulaire restauré après reconnexion |
| 04–07 — L02 | `travail.js`, shell et panneaux détachés dans `instances.js` ; monitor conserve le délai serveur | `erp-productivite.cjs` : coupure/reprise, 401 même sans JSON, 403 sans rejeu, révocation, expiration locale pendant panne, réponse tardive et onglets inversés, bloc accueil indépendant ; tests API/session ; `support-loading.cjs` | Essais réseau et lecteur d'écran sur poste réel ; endurance de 50 changements et mesures mémoire non réalisées |
| 08–10 — L03 | Erreurs locales, payload préparé, intention incertaine et photo confirmée réutilisée ; reçus du domaine inchangés | `erp-productivite.cjs` : 422/409, perte réseau/JSON invalide, 408/429, conflit de clé, fenêtre de 24 h dépassée, photo confirmée/incertaine ; `test_epic60_erp.py` sur PostgreSQL jetable : rejeu, versions, publication, notifications et concurrence | Intention uniquement en mémoire : fermer/recharger perd la garantie de reprise. Photo incertaine : vérification manuelle par l'administrateur, pas de rapprochement automatique des médias |
| 11, 12, 20 — L04 | Travail d'équipe et alertes avant compteurs ; blocs indépendants, dates formatées | `erp-productivite.cjs`, `erp-home-applications.cjs`, profils Finance et accès E69 | **CA-20 non validé** : étude avant/après non réalisée, aucun gain chiffré. Charge et capacité TEST ouvertes |
| 14–17 — L05 | `catalogue-ux.js`, badges et fiche coffret ; filtres usuels/avancés, recherche commerce page 25, aide dépliable | `erp-productivite.cjs` : équivalence des paramètres, page remise à 1, sélection UUID, libellés ; recette historique `test_erp_anomalies.py` adaptée aux interactions ; contrôles BUM/versions côté serveur inchangés | Représentativité des homonymes et volumes de données TEST à vérifier ; plans PostgreSQL N/10N non mesurés |
| 13, 18 — L06 | Recherche des destinations permises, onglets à activation manuelle, associations accessibles, contraste footer | `erp-productivite.cjs` : clavier, refus d'abandon, axe et rendu 320/390/1280, texte 200 % ; `erp-menu-ux.cjs`, `erp-page-template.cjs` | Aucun test avec lecteur d'écran humain ni validation de préférence utilisateur ; l'axe automatisé ne vaut pas audit d'accessibilité complet |

Documentation fonctionnelle et exploitation : le guide E69 exporté a été
actualisé avec les reprises réseau, conflits, résultat incertain et recours
administrateur pour les médias. Aucun schéma, rôle, événement ou contrat de
données nouveau ne justifie une migration ou une modification du générateur.
Les données de recette restent à vérifier avant un déploiement.

## Bilan d'acceptation local

Contexte : Windows, Python 3.14, Chromium via Playwright Node 1.62.1 ; API avec le
lanceur isolé, aucun chargement des `.env` ni accès aux bases d'exploitation.
Backend basé sur `9b2b41a340b79322450aabafa767307afbbc6096`, avec les modifications
locales de cette évolution. Projet basé sur
`b6675672a986171ad2ef0c9f9cef763702ab403a`, avec les travaux documentaires E73
préexistants conservés. Les deux dépôts restent indépendants.

### Réalisation et décisions confirmées

- Six lots implémentés. CA-01 à 19 disposent de preuves techniques ciblées avec
  les limites de la matrice ; ils ne valent pas recette déployée complète.
- La panne de revalidation ne supprime plus la saisie ; le contenu reste masqué
  et `inert` jusqu'au contrôle serveur. Toute purge invalide les callbacks.
- Un 403 sans code stable affiche un refus générique et revalide le contexte,
  sans attribuer arbitrairement la cause à CSRF et sans rejouer la commande.
- Une réponse 408/429, un résultat illisible ou un conflit
  `ERP_IDEMPOTENCY_CONFLICT` ne libère pas l'intention pour une nouvelle clé.
  La limite de 24 heures bloque le rejeu au-delà de la rétention existante.
- La revue indépendante a porté sur le contrat transmis : l'agent n'avait pas
  d'outils de lecture. Ses remarques sur les 4xx, les réponses tardives et la
  fenêtre de reprise ont donné lieu à des corrections et tests ; elle ne vaut
  pas revue indépendante complète du diff ni observation visuelle.

### Résultats et tentatives

Les rapports navigateur E60 sont conservés, sans écrasement, sous
`localeo-backend/.artifacts/erp-productivite/<horodatage>/results.json` avec leurs
captures. Les tests emploient des API interceptées et n'envoient aucun message.

- Reproduction initiale `2026-11-12T19-49-34-049Z` : échecs attendus CA-04,
  CA-06 et CA-07. CA-09 non concluant à ce stade (sélecteur du prix à corriger),
  puis reprise avec une assertion sur le champ effectif.
- La recette élargie a révélé un contraste de pied de page insuffisant et la
  nécessité d'atteindre les gardes HTTP en plus du routeur UI pour le retour de
  connexion. Ces défauts ont été corrigés ; aucune assertion supprimée.
- `tests/browser/erp-productivite.cjs` : 29 scénarios ciblés, rapport final
  `2026-11-12T20-15-32-952Z`, tous réussis après harmonisation des libellés.
  Les captures des passages précédents (320/390/1280, panneau Économie) ont été
  inspectées ; aucune observation de l'application TEST réelle.
- Non-régression : `commercants-erp-ux.cjs` **16**, `erp-home-applications.cjs`
  **30**, `erp-menu-ux.cjs` **35**, `erp-page-template.cjs` **24**,
  `erp-session-dialog.cjs` **11** scénarios réussis. `epic69-acces-internes.cjs`,
  `epic65-finance-erp.cjs` et `support-loading.cjs` réussis pour leurs profils,
  largeurs et parcours annoncés. Ce sont des commandes distinctes, pas un passage
  unique de toute la suite du dépôt.
- Lanceur Python, groupe HTTP : `test_erp_ux_navigation.py`,
  `test_acces_internes_surfaces.py`, `test_admin_session_lifecycle.py`,
  `test_admin_session_cookie.py`, `test_epic65_consultations.py`,
  `test_erp_recherche_commercants.py` : **154 réussites**, 69 avertissements de
  dépréciation de l'adaptateur datetime SQLite.
- Lanceur Python, architecture et compatibilité : `tests/architecture`,
  `test_domain_dedicated_classes.py`, `test_use_case_business_test_coverage.py`,
  `test_atelier_pwa.py`, `test_crm_pwa.py`, `test_documentation.py` : **757 réussites**,
  69 avertissements datetime SQLite. Les 705 contrôles d'architecture avaient
  également réussi avant l'intégration du retour HTTP ; le résultat de 757 est
  la vérification ultérieure qui inclut ces changements.
- `tests/integration/test_epic60_erp.py` : **13 réussites** sur PostgreSQL 18.3,
  cluster local jetable au port 55819, puis arrêté. Treize avertissements de
  tri des clés étrangères cycliques `profils_commercants`/versions. Le premier
  démarrage a été repris après une attente PowerShell sur le processus enfant ;
  aucun test de cette suite n'a été déclaré réussi avant le passage complet.

La recette Python navigateur historique a nécessité l'installation de Playwright
dans un répertoire ignoré et isolé, sans modifier les dépendances du produit.
Le premier lancement ignoré faute de paquet n'est pas une réussite. Les
assertions de libellés/onglets ont ensuite été alignées sur les parcours réels :
statuts français (CA-16), aide dépliable (CA-17), conflit local (CA-08), et onglet
Offre/menu Rubriques déjà présents au SHA de base. Les fixtures de création
doivent expliciter `coffretsOuvert: true`, et les succès de modification de
coffret/prestation annoncent l'invalidation BUM déjà présente au SHA de base.
La sélection obligatoire du périmètre à la création, les cartes mobiles
Commerçants et le libellé « Localeo OnBoard » étaient également présents à cette
base. Ces attentes ont été corrigées précisément, sans rendre facultatifs les
contrôles de droits ou de formulaire. Après les reprises, la commande finale
`test_erp_anomalies.py -k 'not onboard and not ano_ob'` donne **17 réussites,
9 tests non sélectionnés** en 15,68 s (répertoire
`.artifacts/erp-productivite/pytest-navigateur-erp-final-2`). Les neuf scénarios
OnBoard hors changement n'ont pas été validés dans ce passage ; aucune réussite
de la suite complète n'est revendiquée.

Contrôles documentaires : **103 guides, 1 413 liens locaux, 0 erreur et
0 avertissement** ; `sync_documentation.py --check-sources` : **150 documents**.
`git diff --check` et vérification syntaxique des modules JavaScript modifiés :
succès. Ces contrôles ne remplacent pas les scénarios applicatifs ci-dessus.

### Réserves et livraison

- CA-20 : réaliser les mêmes tâches avant/après avec des utilisateurs, mesurer
  réussite sans aide, durée, retours et ressaisies. Aucun gain inventé.
- Recette TEST réelle, lecteur d'écran, capacité p95/p99, plans N/10N et endurance
  restent à produire avant déclaration de validation complète/activation.
- Les usages de médias incertains nécessitent le diagnostic manuel décrit dans
  le guide. Les brouillons ne survivent pas à une expiration ou fermeture.
- Livrer ensemble les assets backend, leur garde HTTP et le guide exporté ;
  aucune migration, variable de configuration ou génération nouvelle.
- Commit et push demandés après la validation locale ; aucun déploiement
  demandé. La clôture historique d'E60 n'est ni rouverte ni réutilisée comme
  validation de cette évolution.

## Évolution du 13 novembre — E60-EVOL-GESTION-20261113

La demande d’implémentation reprend le [rapport des pages ERP](../../audits/backend/localeo-erp-ux-pages-gestion-2026-11-13.md). Les trente constats sont intégrés au périmètre ; le rapport reste une photographie avant changement. Les règles et confirmations métier existantes sont conservées. La clôture historique E60 et le bilan du 12 novembre restent distincts de cette réalisation.

### Conception retenue

Cinq modèles de présentation partagent la coque existante : accueil de travail, liste de gestion, fiche dossier, formulaire de décision, console de diagnostic. Identité, état et action utile précèdent historique et données techniques. Les champs restent en lecture quand le profil ne peut pas modifier. Une seule action est mise en avant lorsqu’une prochaine étape est déterminable à partir des faits serveur ; l’interface ne calcule pas une nouvelle éligibilité.

Les retours conservent filtres, pagination, sélection et focus sans stocker de dossier ou de brouillon durablement. Les saisies privées restent en mémoire de l’onglet et sont purgées à expiration. Le filtre de consultation ne définit jamais implicitement la portée d’une commande globale. Les montants saisis en euros sont convertis exactement en centimes, sans changer les contrats financiers. Les commandes sensibles gardent contrôles serveur, CSRF, version, audit, confirmations et idempotence.

### Critères et preuves prévues

Les critères G01 à G30 correspondent respectivement aux constats UX-01 à UX-30 du rapport ; ils complètent CA-01 à CA-20 sans les renuméroter.

| Critère | Comportement attendu | Preuve prévue |
| --- | --- | --- |
| G01 | Hubs groupés par tâche, description par destination, fonctions exceptionnelles séparées | Navigateur : destinations, droits, bureau/mobile |
| G02 | Préparation accompagnée nommée, état/calendrier/parcours distincts, décision visible | Navigateur : états du service, historique et reprise |
| G03 | Consoles avec cible nommée et recherche/sélection autorisée ; référence technique secondaire | Navigateur et lectures HTTP ciblées |
| G04 | Coffret et note commerçant consultables sans formulaire d’écriture pour Lecteur | Navigateur Lecteur/gestionnaire, refus serveur conservé |
| G05 | Publication et support instance organisés par intention et portée | Navigateur : brouillon, actif, accès client, cycle de vie |
| G06 | Portée globale du catalogue annoncée quelle que soit l’entrée | Navigateur : commune filtrée et offre directe |
| G07 | Remboursement identifié, euros saisis et décision/exécution distinctes | Navigateur : montant exact, refus, résultat incertain |
| G08 | Revue métier des commandes financières/administratives avant engagement | Rendu et navigateur : cible, portée, annulation sans POST |
| G09 | Actualiser/quitter ne détruit pas silencieusement une saisie de préparation | Navigateur : saisie, reprise, conflit, expiration |
| G10 | Achats : recherche nommée, pagination et états lisibles | Rendu : plus de 25 résultats et retour filtré |
| G11 | Territoires « Voir les coffrets » ouvre tous les coffrets de la commune | Navigateur : filtre d’arrivée explicite |
| G12 | Continuité étendue aux listes Animation et parents des consoles | Navigateur : page suivante, détail, retour et focus |
| G13 | Catalogue coffrets distinct de la file des blocages | Navigateur : identité, statut, intention et retour |
| G14 | Causes/états des alertes et couverture territoriale compréhensibles | Navigateur : états, inconnus et diagnostic lié |
| G15 | Modèles réutilisables et prestations liées séparés, éditeur identifié/focalisé | Navigateur : modifier et annuler un modèle |
| G16 | Création/composition avec aide progressive et tâche visible | Navigateur : création, édition, avertissement BUM |
| G17 | Demandes d’organisation comparables avant ouverture, pagination bidirectionnelle | Navigateur : demandes et invitations |
| G18 | Partenaire 360 lié aux accès actuels, résultats navigables | Rendu : liste, détail, accès et retour |
| G19 | Souscription/commande/fermeture : contexte et actions de section hiérarchisés | Navigateur : actions autorisées et blocages |
| G20 | Catalogue/modules : navigation bidirectionnelle et offre ciblée accessible | Navigateur : plusieurs pages, accès direct |
| G21 | Factures/demandes : destinataire et source lisibles dans les droits existants | Rendu : consultation sans commande implicite |
| G22 | Pilotage mobile : valeurs associées à leurs légendes | Navigateur 320/390 px et texte agrandi |
| G23 | Mesures économiques consultables avant édition ciblée | Navigateur : 25 mesures, ouverture d’un éditeur |
| G24 | Préparation : lectures utiles bornées ; erreurs locales dans les autres listes | Navigateur : nombre d’appels, panne partielle et reprise |
| G25 | Batchs : diagnostic avant configuration/exécution, historique accessible | Rendu/navigateur : recherche et sélection sans mutation |
| G26 | Audit/Web Push : contexte et traitement ciblé sans assimilation de livraison/lecture | Navigateur : liens et filtres autorisés |
| G27 | Utilisateur : état d’accès avant édition des habilitations | Navigateur : récupération et édition explicite |
| G28 | Composants de contenu cohérents, actions lisibles et focus préservé | Captures bureau/mobile/texte agrandi, clavier |
| G29 | Accueil compact, tâches connues et accès aux listes complètes | Navigateur : aperçu borné et absence de faux compteurs |
| G30 | Aide et menus livrés alignés | Liens documentaires et comparaison des libellés |

### Responsabilités, impacts et bornes

- Le backend héberge les vues ERP, consoles et projections ; les domaines Catalogue, Animation, Identité et Finance restent propriétaires des décisions. Aucun changement de règle métier n’est nécessaire pour la présentation.
- Les projections enrichies, si nécessaires, restent des lectures autorisées et bornées : 25 éléments par défaut, au plus 100 ; pas de boucle de collecte exhaustive au montage, pas de requête de nom par ligne. Tests à 25/100 éléments ou N/10N selon le chemin réellement modifié.
- Les contrats internes modifiés doivent être testés avec leurs consommateurs ; aucune modification des interfaces publiques Live/Pro/Animation n’est présumée. Un besoin de contrat sera consigné avec producteur et consommateurs avant son édition.
- Aucune migration ni configuration nouvelle n’est prévue. Une découverte nécessitant des données supplémentaires doit être explicitée ; ne pas inventer des noms, compteurs, affectations ou délais absents.
- Les fixtures navigateur couvrent homonymes, droits restreints, plusieurs pages, erreurs et montants. Le générateur n’a pas à modifier ses données pour un changement de présentation ; réexaminer ce point si un schéma ou contrat évolue.
- Actualiser le guide ERP et le menu Animation. La spécification et le bilan restent ici, sans documentation concurrente par application.
- Les tests isolés prouvent les comportements locaux. Recette humaine, lecteur d’écran et capacité déployée restent distincts ; CA-20 n’est pas rendu vert par des captures. Aucun commit, push, migration TEST ou déploiement n’est demandé dans cette phase.

### Réalisation et bilan

Les trente constats ont un traitement dans cette évolution. Le tableau ci-dessous
décrit le résultat local ; il ne constitue pas une validation de l’environnement
TEST ni une mesure de gain de productivité auprès des gestionnaires.

| Critères | Réalisation | Preuves locales |
| --- | --- | --- |
| G01, G28 | Hubs par tâches avec descriptions ; blocs identité/décision/édition partagés dans `page-layout.css`, également chargés par les consoles ; repères mobiles moins répétitifs | `erp-gestion.cjs`, `erp-page-template.cjs`, `erp-menu-ux.cjs` |
| G02, G09 | Préparation nommée, attente et décision avant historique ; calendrier/parcours séparés ; brouillons en mémoire, actualisation et version contrôlées | `epic73-preparations-service.cjs` |
| G03 | Sélection bornée par nom/commune/moteur, identité et organisation rappelées ; preuves nommées dans le périmètre de régularisation ; référence technique séparée | `erp-gestion-preparations.cjs`, `test_gestion_preparation_erp.py`, `test_gestion_preparation_lecture.py`, `test_gestion_preparation_surfaces.py` |
| G04 | Informations du coffret et notes du commerce sans formulaire d’écriture pour Lecteur | `erp-gestion.cjs`, non-régressions `erp-productivite.cjs` |
| G05 | Vérification/publication séparées du retrait/archivage ; accès client, assistance et annulation/remboursement regroupés dans l’instance | `erp-gestion.cjs`, `erp-template-modules.cjs` |
| G06, G20 | Catalogue global explicite, revue ancienne/nouvelle version, filtre d’offre avant pagination ; curseurs bidirectionnels, résultat annoncé et pagination verrouillée pendant lecture | `erp-gestion-animation.cjs`, `epic73-modules-ux.cjs`, `test_erp_gestion_animation_projections.py` |
| G07 | Organisation, commune, date/montant de commande, décision/exécution distinctes et saisie exacte en euros | `epic73-modules-erp.cjs`, projections PostgreSQL et contrats HTTP |
| G08 | Revue des commandes historiques avec intitulé, conséquences et portée ; campagne Stripe globale annoncée indépendamment des filtres | `test_erp_gestion_admin.py`, `erp-gestion-admin.cjs`, `test_reversements_360_finance_runtime.py` |
| G10 | Achats recherchables, états français, pagination et retour avec recherche/page/focus | `test_erp_gestion_admin.py`, `erp-gestion-admin.cjs` |
| G11, G13, G14 | Tous les coffrets de la commune accessibles ; catalogue distinct des blocages ; cause/état visibles dans les alertes, couverture traduite | `erp-gestion.cjs` |
| G12 | Contexte étendu aux listes Animation et parents des consoles ; historique utilisé quand l’entrée antérieure est connue ; repli par curseur opaque, sans faux numéro de page | `epic73-suivi-produits.cjs`, `erp-gestion-animation.cjs`, `erp-gestion-preparations.cjs`, `erp-productivite.cjs` |
| G15, G16 | Modèles et prestations distincts ; éditeur nommé/focalisé et annulation avec retour du focus ; coffret organisé par identification, conditions, promesse et image, aide repliée | `erp-gestion.cjs`, `erp-productivite.cjs` |
| G17 | Demandes comparables en tableau, examen ciblé, pagination dans les deux sens, saisies protégées avant filtre/rechargement/navigation | `equipes-animation-erp.cjs` |
| G18 | Partenaires paginés, liens exacts vers gestionnaires actuels, recherche du partenaire annoncée comme recherche | `test_erp_gestion_admin.py` |
| G19 | Actions des modules et décisions de commande remontées ; fermeture présentée avec ses engagements et blocages | `souscriptions-responsable-erp.cjs`, `epic73-modules-ux.cjs`, `epic73-reversibilite.cjs` |
| G21 | Destinataires et sources de facture lisibles ; enrichissement groupé en une lecture à 25/100 lignes, sans génération de document | `test_erp_gestion_admin.py` |
| G22, G23 | Cellules économiques légendées sur mobile ; mesures consultables avant ouverture d’un éditeur ciblé | `epic73-pilotage-economique.cjs` |
| G24 | Seulement les POI utilisés chargés au montage, accords par pages de 25 ; erreurs locales et nouvelle tentative pour alertes, territoires et instances | `preparation-erp.cjs`, `erp-gestion.cjs`, `erp-template-modules.cjs` |
| G25 | Filtres et diagnostic des batchs avant configuration/intervention ; historique par clé date/identifiant, sans modifier le contrat maintenance par défaut | `test_erp_gestion_admin.py`, `test_batchs_manuels.py`, `batchs-manuels.cjs` |
| G26 | Entrées Audit/Web Push depuis commerce et instance ; codes connus expliqués, codes sources conservés ; traitement du canal ciblé, destinataire privé en mémoire | `erp-gestion.cjs`, `epic65-audit-erp.cjs`, `epic65-webpush-erp.cjs` |
| G27 | État d’accès et envois avant édition explicite ; modification protégée contre actualisation/retour, purge à expiration | `erp-gestion.cjs`, `erp-productivite.cjs` |
| G29 | Aperçu de cinq dossiers d’équipe, lien vers la file complète de 25 ; pas de nouveau compteur Animation non disponible | `erp-gestion.cjs`, `erp-home-applications.cjs` |
| G30 | Guide de prise en main et menu Animation alignés sur les groupes, ancres et parcours livrés | Contrôles documentaires et comparaison au menu du code |

Les tests navigateur sont dans `localeo-backend/tests/browser`, les tests Python
dans leurs dossiers API/application/infrastructure/security. Les lectures et
commandes navigateur sont simulées ; aucune commande utilisateur réelle n’est
effectuée. Les rapports de chaque tentative restent sous `.artifacts` du backend,
hors versionnement ; seules les dernières exécutions pertinentes fondent le bilan.

#### Vérifications exécutées le 13 novembre 2026

| Contrôle | Résultat et preuve |
| --- | --- |
| Architecture, classes de domaine, couverture des cas d’usage, navigation serveur et génération OpenAPI | **757 tests réussis**, aucun échec ni test ignoré ; `.artifacts/erp-gestion/integration-final.xml` |
| Préparation et consoles : API, application et middleware réel | **16 tests réussis**, dont portée autorisée avec `animation.gerer`, refus sans capacité et absence de route de preuves sous `/protected` |
| Administration, factures, batchs et revues financières | **32 tests réussis** ; `.artifacts/erp-gestion-admin/pytest.xml` |
| Lectures Animation | **23 tests PostgreSQL/API** et **16 contrôles de sécurité** réussis ; **8 tests ciblés rejoués** après séparation du schéma de remboursement interne, sans les additionner aux premiers passages |
| Nouveaux parcours de gestion communs | **16 scénarios réussis** ; `.artifacts/erp-gestion/2026-11-13T18-27-11-463Z/results.json` |
| Productivité, droits, erreurs, reçus, saisies et continuité | **29 scénarios réussis** après le dernier correctif de retour ; `.artifacts/erp-productivite/2026-11-13T18-34-55-531Z` |
| Navigation Animation | **28 contrôles réussis**, y compris annulation puis nouvelle tentative de sortie avec saisie en cours, en 320 et 1280 px |
| Tests Node du menu et du chargement différé des instances | **6 tests réussis** sur les modules réellement rendus ; les deux anciennes fixtures obsolètes sont actualisées après reproduction de leurs échecs sur HEAD |
| Gabarit, instances, menu et accueil | Respectivement **24, 78, 35 et 30 contrôles réussis** ; captures et vérifications clavier/mobile/texte agrandi selon chaque parcours |
| Préparations et consoles dans le navigateur | **28 scénarios réussis** répartis dans six recettes ; le service est rejoué après l’ajustement final des cases de confirmation |
| Autres parcours Animation | **Neuf recettes navigateur réussies** : catalogue, modules, remboursements, équipes, suivi, souscriptions, réversibilité, pilotage et sollicitations ; continuité/pagination rejouées après intégration |
| Audit, Web Push, administration et batchs | Recettes navigateur réussies avec commandes interceptées, droits et confirmations vérifiés |
| Documentation | `check_guidance.py` et `sync_documentation.py --check-sources` réussis ; contrat E41 généré hors ligne avec trois nouvelles lectures internes et aucune nouvelle route `/protected` |

Les revues indépendantes des parcours et des projections ont été intégrées.
Elles ont notamment conduit à protéger les saisies d’organisation, verrouiller la
pagination pendant une lecture, rétablir le focus après annulation d’un modèle
et invalider l’identité affichée lorsque la cible de conservation change.
La conservation vérifie l’absence de POST avant nouvelle sélection d’une animation.
Une recette de navigation a également reproduit puis vérifié la correction du
retour après annulation du dialogue de sortie. Les premières tentatives en échec
restent dans les artefacts ; les résultats ci-dessus correspondent aux reprises
validées, sans cumul artificiel des répétitions.

#### Contrats, données et autres dépôts

Les [contrats de gestion E73](../epic-73-animation-et-ou-coffrets/architecture-contrats.md#lectures-de-gestion-erp--13-novembre-2026)
décrivent les lectures sélection/preuves, le filtre d’offre et l’enrichissement des
remboursements. Le contrat OpenAPI complet E41 est régénéré hors ligne. Les réponses
publiques et les réponses de commande de remboursement gardent leur schéma
historique ; l’enrichissement est limité aux GET internes.

Deux dépôts sont modifiés : `localeo-backend` (ERP, consoles, lectures et tests),
`localeo-projet` (spécification, contrats, guides et traçabilité). Les applications
marketplace, commerçant et Animation ne changent pas. Aucun schéma persistant,
migration, secret, configuration ou jeu de démonstration nouveau n’est nécessaire.
Les droits, décisions financières et transitions restent portés par leurs domaines.

#### Limites explicites

- Le gain de temps quotidien n’est pas mesuré : CA-20 requiert toujours une recette
  avec les opérateurs. Les tests clavier, Axe et captures ne remplacent pas un
  essai avec lecteur d’écran ou appareil physique.
- La campagne Stripe globale ne dispose pas d’un aperçu chiffré de simulation.
  La revue explique sa portée ; le domaine recalcule les dossiers à l’exécution.
  Aucun total présumé n’est affiché.
- Les cibles de conservation qui ne sont pas des animations restent techniques.
  Les identités absentes sont signalées, sans nom reconstitué.
- Les codes d’audit inconnus gardent leur valeur source. Une installation Live
  ne devient pas une identité d’habitant, et une acceptation Web Push ne prouve
  ni affichage ni lecture.
- Les preuves PostgreSQL portent sur les projections modifiées, pas sur la
  capacité de l’environnement déployé. La pagination historique des batchs est
  vérifiée sur une base SQLite isolée.
- Aucun déploiement, migration TEST, commit ou push n’est inclus. Le statut
  historique de l’epic n’est pas réécrit ; le rapport d’audit reste la photographie
  avant cette évolution.

### Correctif du 13 novembre 2026 — Chargement des modules ERP

Signalement sur TEST : `Failed to fetch dynamically imported module` pour
`/internal/erp/assets/suivi-animations.js`. Sur la baseline locale backend
`76d5dee9`, ce module importe `gestion-pagination.js`, présent sur disque mais
absent de la liste explicite des fichiers servis par `app/api/erp_ui.py`.
La requête HTTP de cette dépendance reçoit 404 et bloque le chargement du module
parent. Le même oubli concerne `gestion-pages.js`,
`gestion-preparation-console.js` et `gestion-preparation-brouillons.js`.

Le correctif expose ces quatre fichiers par la route existante, en conservant
la session obligatoire, `Cache-Control: no-store` et le refus des fichiers non
autorisés. Il ne modifie ni les règles métier ni les habilitations. Les recettes
navigateur précédentes lisaient les fichiers par interception : elles ne
vérifiaient pas que le serveur les distribuait réellement.

Le nouveau `tests/api/test_erp_assets_dependencies.py` parcourt les imports
statiques et dynamiques littéraux de l’ERP, du suivi, du Support et des quatre
consoles via la vraie route FastAPI. Avant correction, **10 échecs et 5 succès**
confirment les ressources manquantes. Après correction, ce fichier et les
recettes HTTP navigation/consoles/équipes/sélection obtiennent **40 succès**.
Les **720 contrôles d’architecture, classes de domaine et couverture des cas
d’usage** réussissent également sur la baseline avec ce correctif local.

Commandes backend exécutées avec `python scripts/validation/test_isolated.py` :

- `tests/api/test_erp_assets_dependencies.py tests/api/test_navigation_consoles_animation_erp.py tests/api/test_erp_animation_equipe_shell.py tests/api/test_gestion_preparation_erp.py -q` ;
- `tests/architecture tests/domain/test_domain_dedicated_classes.py tests/application/use_cases/test_use_case_business_test_coverage.py -q`.

Impacts : backend pour route/tests, projet pour ce suivi ; les trois frontends
utilisent les mêmes contrats. Aucun changement d’API métier, de schéma, de
migration, de configuration ou de générateur de démonstration n’est nécessaire.
La cause est démontrée localement ; la révision déployée et la session TEST
n’ont pas été inspectées. Le contrôle après livraison consiste à ouvrir
**Animations et lots** avec une session autorisée et vérifier le chargement des
dépendances, puis les consoles de préparation. Aucun déploiement n’a été effectué.
