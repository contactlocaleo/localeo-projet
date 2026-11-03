# Audit typographique — applications de gestion Localeo

Date : **3 novembre 2026**. Périmètre : Localeo Pro, Animation, ERP, Support,
Atelier, Ops et OnBoard, sur PC et mobile. Cet examen prolonge l'allègement de
Live, en tenant compte de la densité et des tâches propres aux applications
de gestion. Il ne constitue pas un nouvel audit fonctionnel complet.

Bases locales : Pro `8fbf742`, Animation `324d024`, Backend `cde1d3e` et
Projet `61be360`. Les dépôts applicatifs étaient propres avant intervention.
Le fichier `debug.log` déjà indexé dans Projet reste hors périmètre.

## Constats et priorités

| Priorité | Application | Constat dans les sources |
| --- | --- | --- |
| Haute | Pro | Les workspaces récents utilisent DM Sans et des titres compacts, mais les pages historiques conservent Oswald et de grands titres. Les différences sont particulièrement sensibles entre connexion, scan, validation et gestion. |
| Moyenne | Support | Les titres de page peuvent atteindre 40 px et héritent du gras standard du navigateur, trop présent pour une console de traitement. |
| Moyenne | OnBoard | Les nombreux titres et libellés gras donnent une emphase semblable à des informations de niveaux différents. La règle historique Oswald est masquée par la feuille partagée : la police réellement affichée est déjà la police système. |
| Modérée | Animation | La famille DM Sans et la densité sont déjà adaptées. Les tailles et graisses des titres partagés et de certaines sections divergent. |
| Modérée | ERP | La police système et les tableaux sont déjà adaptés à la gestion ; les titres méritent une graisse plus régulière. |
| Modérée | Atelier | L'interface est déjà compacte ; harmoniser la hiérarchie des titres sans agrandir toutes les données. |
| Modérée | Ops | La densité est utile au suivi opérationnel ; alléger les titres sans atténuer les alertes et indicateurs. |

## Principes retenus

La [convention typographique de gestion](../architecture/transverse/conventions-backoffice.md#typographie-des-applications-de-gestion)
porte les repères communs : titres de page 24–28 px et graisse 600, sections
20–22 px, sous-sections plus compactes selon leur rôle. Les listes et tableaux
gardent une densité adaptée ; les champs mobiles et actions principales restent
lisibles. Les polices déjà embarquées sont réutilisées. La signature Localeo,
les chiffres clés, les codes opérationnels et les zones tactiles ne sont pas
diminués pour rendre l'interface plus légère.

Les corrections portent sur les sources des styles et leurs consommateurs.
Les routes, permissions, règles métier, confirmations, API, migrations,
données et générateurs de démonstration restent hors périmètre : aucun de ces
contrats n'est modifié par l'ajustement de la typographie. La roadmap conserve
ses états. Le résultat décrit un code testé localement, pas un déploiement.

## Corrections réalisées

| Application | Résultat |
| --- | --- |
| Pro | DM Sans pour l'ensemble des titres, échelle partagée 24–28 / 20–22 / 18 px et graisse 600. Suppression des variantes historiques surdimensionnées. Les groupes de formulaires déjà denses gardent leurs titres de 16–18 px ; les actions sont moins grasses. |
| Animation | DM Sans conservée, titres de page 24–28 px/600, sections 20 px et sous-titres 18 px. Les titres de l'Assistant et des guides Chasse utilisent les mêmes tokens ; les groupes compacts restent à 16 px. |
| ERP | Titres à 24 px sur petit écran et 28 px sur bureau, graisse 600 ; données et gabarit de gestion conservés. |
| Support | Titre de page ramené de 27/40 px à 24/28 px sur les formats 320/1280 contrôlés, avec une graisse de 600. |
| Atelier | Même rythme de titres que l'ERP via les styles partagés, sans agrandir les tableaux. |
| Ops | Titres semi-gras cohérents, avec conservation de la place et de l'emphase des alertes et métriques. |
| OnBoard | Police système effective conservée, ancienne règle condensée retirée, titres et commandes allégés. Le compteur de 34 px/700 et les champs mobiles de 16 px sont conservés dans les mesures réalisées. |

Les styles sont locaux à chaque dépôt ; aucune dépendance entre applications
n'est ajoutée. La signature des en-têtes reste en graisse 800 selon sa charte.

## Vérifications

| Dépôt | Preuves locales |
| --- | --- |
| Pro | Build isolé réussi ; **34 scénarios Playwright distincts** réussis dans `management-ergonomics`, `operational-ux`, `employee-invitation-ux` et `coffret-states`. Les 4 scénarios coffret ont été rejoués après l'ultime correction de l'interligne des titres de prestations. Le scénario supplémentaire `security-headers` passe après retrait des préchargements inutiles : DM Sans chargé et calculé sur le titre, aucune requête Oswald, protections CSP/cache/compression conservées. Formats 320–1440 px, texte à 200 %, clavier, erreurs, cibles tactiles et contrôles Axe des états prévus. |
| Animation | Build isolé, TypeScript et ESLint réussis ; **40 parcours** du banc `animation-workspace-ux`, **10 formats** du cadre et **3 parcours** `hunt-guided-workflow` réussis. Les 87 contrôles du guide sont inclus dans ces 3 parcours ; `workspace-primitives` ajoute **188 contrôles** sur les composants, le clavier, les gardes et les petits formats. |
| Backend — ERP et OnBoard | `erp-page-template.cjs` : **24 scénarios** ; `onboard-dossier-ux.cjs` : **24 scénarios**, avec dernier replay après l'ajustement final des interlignes. `admin-shell.cjs` : **6 scénarios et 2 instances contextualisées**. Les vues SQLAdmin portant déjà `erp-app` bénéficient des titres allégés, sans modification des contrôles ni de leur gabarit technique. |
| Backend — Ops | `ops-alert-priorities.cjs` : **12 scénarios** ; `test_ops_alert_priorities.py` : **7 tests réussis**, sortie 0. Sévérités, compteurs et actions contrôlés. |
| Backend — Support et Atelier | `epic73-support-organisations-ux.cjs` : 1280/320 px et texte à 200 %. `atelier-assiste-erp.cjs` et `atelier-pwa.cjs` : 1280/390 px, parcours, sessions et hors connexion. |
| Backend — cadre et connexion | `header-mobile.cjs` : **5 applications sur 8 largeurs**, agrandissement et cibles tactiles. `connexion-interne.cjs` : 320/390/1280 px, texte à 200 %, clavier, connexion et initialisation. |

Les mesures backend avant/après figurent dans
`tmp/type-backoffice/computed-before-after.json` : fragments représentatifs
avec les vraies feuilles CSS, complétés par les parcours ci-dessus. La comparaison
des déclarations CSS ne relève aucune modification de géométrie ou couleur.
`git diff --check` passe dans les trois dépôts applicatifs.

Le banc Animation appelait déjà `GET .../tirage-annonce` sans réponse simulée
avant correction. Sa fixture a été complétée selon le contrat existant, en
conservant le contrôle des requêtes inattendues. Ce rattrapage de test est distinct
des modifications typographiques.

Pro préchargeait encore deux fois Oswald et DM Sans dans `index.html`. Le
préchargement Oswald devenu inutile et le doublon DM Sans sont retirés. Le
test de police conserve une preuve du chargement réel, adaptée à la famille
désormais utilisée, et vérifie l'absence de requête Oswald.

Les captures sont conservées dans les sorties locales ignorées : Pro
`tmp/typography-audit/`, Animation `tmp/animation-workspace-ux/` et
`tmp/generation-browser-captures/`. Les captures Connexion Pro mobile/bureau,
tableau de bord Animation et Assistant mobile ont été examinées. La connexion
Pro affiche DM Sans600, 24,7 px à 390 px et 28 px à 1440 px, sans débordement.
Les captures ERP, Support, OnBoard, Atelier et Ops ont également été examinées
dans `.artifacts/` et `tmp/` du backend. Certains bancs fonctionnels emploient
un en-tête simplifié ou servent le symbole avec un type incorrect ; le contrôle
dédié des en-têtes vérifie séparément le vrai symbole. Les captures de ces
bancs fonctionnels ne prouvent donc pas à elles seules le rendu de la marque.

Ces bancs utilisent des données synthétiques et des services simulés ; aucune
commande métier n'est exécutée sur TEST ou production. Ils ne remplacent pas
une recette sur appareils physiques, lecteurs d'écran ou toutes les combinaisons
de données et de droits. Aucun audit exhaustif RGAA n'est revendiqué.

Contrôles documentaires : 6 documents modifiés ou ajoutés, 56 liens locaux et
134 sources exportées vérifiés sans erreur. Commits applicatifs : Pro `054feab`,
Animation `4116e0e`, Backend `aadb55f`. Les dépôts restent indépendants ; la
demande autorise les commits et push, sans recette de déploiement associée.
