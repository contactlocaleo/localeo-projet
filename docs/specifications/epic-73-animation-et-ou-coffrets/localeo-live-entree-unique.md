# E73 — Localeo Live, entrée unique des animations

Évolution **E73-EVO-LIVE-UNIQUE**, demandée le **30 octobre 2026**.
L'epic 73 reste **En cours**. Les 63 critères initiaux et leurs résultats de
recette restent conservés ; les critères ci-dessous sont complémentaires.

## Décision et comportement attendu

En tant qu'habitant, découvrir les animations des communes choisies, s'inscrire
et retrouver ses participations dans un seul espace, Localeo Live, à
`https://animations.localeo.city`. En TEST : `https://test-animations.localeo.city`.
Le portail organisateur reste `gestion-animations.localeo.city`.

Cette décision remplace la surface publique marketplace Animation mise en place
par E73-EVO-DOMAINES et E73-EVO-UX-PUBLIC. Elle conserve le domaine décidé, les
données et les règles métier. Le même dépôt `localeo-marketplace` fournit Live
et Coffrets, sur leurs services respectifs ; aucun nouveau référentiel ni dépôt.
`LOCALEO_PUBLIC_SURFACE=ANIMATION` désigne désormais l'entrée Live. L'ancien
paramètre `surface=animations` ouvre aussi la transition vers Live.

**Arbitrage confirmé par l'utilisateur le 30 octobre : aucun nouveau compte
habitant.** Les communes sont mémorisées sur l'appareil ; leur association à un
compte ne s'applique que si un mécanisme existant la permet. L'installation
anonyme Live n'est pas un compte. Aucune synchronisation de compte n'est ajoutée.
Les contrôles existants des liens personnels, QR, PIN et WebAuthn restent en place.

Hors périmètre : refonte Coffrets, changement des règles d'animation, catalogue
ou base de participations distincts, nouvelles notifications et recommandations
personnalisées. Les notifications existantes restent facultatives.

## Parcours et priorité mobile

Navigation basse : **Découvrir**, **Mes participations**, **Mes communes**.
Découvrir présente les animations publiques **En ce moment** et **Prochainement**.
Une fiche montre titre, commune, dates, description, conditions et action autorisée.
L'inscription réutilise le formulaire existant sous `/live/animations/:id/inscription`.
Les participations et lots personnels conservent leurs accès dans le carnet.

Conception mobile d'abord : écran de référence 320–390 px, pas de débordement
horizontal, champs à 16 px, actions tactiles d'au moins 44 px, navigation à portée
du pouce et marge de sécurité PWA. Pas d'accueil marketing avant les tâches.
États de chargement, vide, erreur, stockage refusé et réseau indisponible explicites.
Le clavier, le focus, le texte agrandi à 200 % et la réduction des animations
restent utilisables. Les libellés de navigation peuvent revenir à la ligne.

La recherche ajoute ou retire des communes sans changer les inscriptions. Une
commune partagée par URL constitue un contexte de consultation : son ouverture
ne modifie pas silencieusement les communes suivies. Le suivi exige une action.

## Critères ajoutés et preuves

Les numéros 01 à 12 reprennent les CA1 à CA12 fournis par l'utilisateur.

| Critère | Résultat observable et preuve attendue |
| --- | --- |
| E73-EVO-LIVE-01 | Catalogue et détail consultables sans compte, y compris sans carnet local ; aucune permission personnelle déduite de la consultation. |
| E73-EVO-LIVE-02 | Recherche et sélection de plusieurs communes, persistance locale, modification et stockage refusé ; aucun compte nouveau selon l'arbitrage confirmé. |
| E73-EVO-LIVE-03 | Deux périodes, seuls résultats publics retournés par le producteur, pagination et état vide permettant de modifier les communes. |
| E73-EVO-LIVE-04 | Fiche vers inscription ou participation, même contexte d'animation et code de diffusion ; conservation des mécanismes d'accès existants, aucun nouvel écran de connexion fictif. |
| E73-EVO-LIVE-05 | Même participation et historique après reprise volontaire du carnet, sans création de compte, doublon métier ou effacement de l'origine. |
| E73-EVO-LIVE-06 | `/live/decouvrir?commune=<UUID>` partageable ; `/live/animations/:id` et anciens liens personnels fonctionnels. |
| E73-EVO-LIVE-07 | Domaine HTTPS dédié, même backend, accès directs et actualisation ; vérification DNS/TLS et hébergée distincte des tests locaux. |
| E73-EVO-LIVE-08 | Anciens liens personnels et QR conservés ; aucune redirection globale des capacités ni utilisation du secret d'installation d'une autre origine. |
| E73-EVO-LIVE-09 | Ancien catalogue et `surface=animations` quittent l'interface marketplace, contexte commune/animation conservé ; reprise du carnet proposée avant sortie d'origine. |
| E73-EVO-LIVE-10 | Navigation Animation de la marketplace vers Live ; parcours Coffrets et anciens `/live/*` conservés. |
| E73-EVO-LIVE-11 | Découverte, communes, inscription et carnet utilisables à 320/390 px et en PWA ; safe-area et accès au clavier. |
| E73-EVO-LIVE-12 | Recette de bascule : domaine, lecture anonyme, inscription, reprise des accès, historique, redirections et non-régression Coffrets. Aucune mise en service déclarée sur la seule base d'un build. |

## Invariants, contrats et conservation

Le backend reste propriétaire de la visibilité publique, des dates et autorisations
d'inscription, des progressions, attributions, consommations et historiques.
L'interface groupe les projections existantes et n'accorde aucun droit supplémentaire.
Réutiliser `fetchPublicAnimations`, `fetchPublicAnimation`, `searchVilles`, le
formulaire d'inscription et les contrats de participation existants. Aucun nouveau
contrat OpenAPI n'est annoncé pour une association à un compte inexistante.

Le catalogue est borné : au plus dix communes suivies et deux lectures concurrentes,
pagination indépendante par commune et période, détection des curseurs répétés,
annulation des anciennes recherches et déduplication par animation. Une erreur
partielle ne devient pas un résultat complet vide. Ces bornes d'interface ne
constituent pas une mesure de capacité serveur ; avant activation, mesurer sur
1 puis 10 communes les requêtes, latences, volumes et erreurs en charge mixte.
Budget cible de navigation : interactions locales immédiates, état de chargement
visible sans attendre la dernière commune ; les résultats restent consultables
si une autre commune échoue. La tenue en charge hébergée reste à prouver.

Le carnet est en IndexedDB par origine. Un DNS ne peut pas migrer ce stockage.
Conserver `/live/reprise-carnet` sur l'ancien domaine : export privé puis import
volontaire sur le nouveau, validation et fusion transactionnelles existantes,
mêmes identifiants et capacités, sans nouvelle inscription. Aucun token ajouté à
une URL de transition. L'ancien carnet reste présent. Les anciens liens personnels
restent servis lorsque leur redirection ne peut préserver l'accès sans risque.

## Impacts et ordre de livraison

| Périmètre | Impact et vérification |
| --- | --- |
| Marketplace / Live | Routes, navigation, découverte multi-communes et sélection locale, inscription sous scope `/live/`, transition de l'ancien catalogue ; tests Node et navigateur mobile/bureau. |
| Backend / ERP / batchs | Aucun changement de règle, schéma ou commande métier prévu ; mêmes endpoints publics et privés. Les liens générés continuent à être acceptés par les routes de compatibilité. |
| Portail Animation / Pro | Aucun nouveau parcours métier ; liens publics et QR existants conservés. Les origines publiques dédiées déjà prévues restent applicables. |
| Données / migrations | Pas de migration SQL ni duplication de participation ; reprise locale du carnet explicite. Pas de synchronisation de compte ou de secret d'installation entre origines. |
| Démonstration | Réutiliser communes, animations et participations synthétiques existantes ; adapter les scénarios de navigation, sans régénérer des données réelles. |
| Exploitation | Deux services publics conservés, même API ; DNS/TLS du service Live, cache et PWA, maintien des anciens accès et reprise de carnet avant retrait de toute ancienne origine. |

Préparer le bundle et ses tests, déployer le même backend compatible et le frontend
Live sur TEST, configurer le domaine dédié et vérifier TLS. Contrôler ensuite les
douze parcours et la reprise du carnet avec un utilisateur de recette. Mettre à
jour les liens marketplace et générés après cette vérification. Ne pas retirer
l'ancien hébergement des accès personnels ni sa page de reprise du carnet.
Le repli conserve le même backend et les données ; rétablir le bundle précédent
et ses origines sans effacer de carnet. Un service worker précédent doit toujours
permettre l'ouverture des anciens accès. Commit, push et déploiement sont séparés.

## Suivi des preuves

Les résultats réels et limites sont consignés dans le
[suivi d'implémentation](suivi-implementation.md). Les 130 scénarios historiques
de [recette métier](recette-metier.md) conservent leurs statuts ; cette évolution
ajoute ses propres parcours de bascule et n'est pas validée par leurs anciens succès.
