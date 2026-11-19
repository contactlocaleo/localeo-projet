# Localeo CRM — exploration et workshop UX

## Actualisation du 19 novembre 2026 — réalisation locale

UX01–UX05 validées ; seuils UX02 confirmés ensuite : **interaction 30 jours,
évolution 60 jours**, pauses justifiées et dossiers clos exclus des alertes
temporelles. La demande explicite de spécification et d’implémentation a conduit
à la [réalisation locale dans l’EPIC 71](../../../specifications/epic-71-crm-prospection/workshop-crm-20261118.md).
Les [décisions](validation/decisions.md), le cadrage et les preuves sont reliés.
Aucun déploiement ni modification des données TEST. Les risques de recette
humaine et de mise en service restent distincts des tests synthétiques locaux.

Les étapes ci-dessous conservent leur bilan à leur date de clôture : leurs
mentions « en attente » et « non implémenté » décrivent l’état antérieur aux
décisions et à la demande de réalisation. Les manifestes et rapports archivés
attestent leur version initiale, pas les documents actualisés ultérieurement.

- Début : 18 novembre 2026, heure de Paris ; exploration poursuivie après minuit le 19 novembre.
- Environnement : https://test-crm.localeo.city (TEST).
- Dépôt documentaire : `localeo-projet`, branche `main`, commit de départ `dd14e11c4522d2b6de1f9480cf30d50abaffc822`.
- Code consulté : `localeo-backend`, commit local `ef913e85db91b5ff475d0093863e13ce4e03c199`. Version effectivement déployée non établie.
- Statut : **archivage documentaire finalisé avec réserves ; workshop incomplet, cinq décisions utilisateur en attente**.

L'exploration a utilisé Playwright/Chromium sur ordinateur (1440 × 1000). La connexion, l'accueil, les listes Prospects, Suivi, Rappels, Qualification, Notifications, Imports et l'agenda ont été parcourus. Un prospect clairement fictif a été créé dans TEST pour vérifier contact, action et réservation de rendez-vous, sans modifier de fiche existante. Les captures ne contiennent pas d'identifiants de connexion ; les coordonnées des résultats Prospects sont masquées.

Le passage à 390 × 844 n'a pas abouti à une page utilisable : le chargement est resté sur « Ouverture de votre espace commercial… », puis une nouvelle navigation a expiré. Cela ne démontre pas un défaut mobile du produit. La modification du rendez-vous, le compte rendu après rendez-vous et plusieurs transitions ont été vérifiés dans le code, mais pas exécutés dans l'interface. Aucune étude avec des utilisateurs réels n'a eu lieu.

## Livrables

- [Parcours et état de vérification](observations/cartographie-parcours.md)
- [Écrans et captures](observations/inventaire-ecrans.md)
- [Constats factuels](observations/observations-factuelles.md)
- [Couverture du pilotage commercial](observations/couverture-pilotage-commercial.md)
- [Limites et données fictives créées](observations/limitations.md)
- [Prompt complet de l'étape 1, expurgé](prompts/01-exploration.md)

## Étape 2 — workshop simulé

Le prompt de l’étape 2 a été reçu et [archivé intégralement](prompts/02-workshop.md). L’exécution conserve le dossier daté du début de l’exploration, malgré sa poursuite le 19 novembre.

Douze profils fictifs, sept ateliers, treize orientations et 156 votes individuels motivés ont été produits. Ces simulations ne sont pas des données de recherche utilisateur. La conclusion est **GO SOUS CONDITIONS pour un pilote encadré sur ordinateur** ; l’usage autonome à dix personnes n’est pas validé. Les limites de l’étape 1 restent actives : mobile, exhaustivité, cycle complet du rendez-vous et collaboration multi-compte à vérifier.

- [Rapport exécutif et cinq priorités](workshop/rapport-executif.md)
- [Compte rendu et matrice personas/parcours](workshop/compte-rendu.md)
- [Votes et arbitrages](workshop/votes-et-arbitrages.md)
- [Backlog UX](workshop/backlog-ux.md)
- [Orientations non retenues](workshop/orientations-rejetees.md)
- [Quick wins](workshop/quick-wins.md)

À la clôture de l’étape 2, les prompts `00`, `03`, `04` et `05` étaient des fichiers d’attente : leurs instructions distinctes n’ont pas été fournies. Aucune maquette, validation utilisateur ou synthèse de phase ultérieure n’avait été produite à la clôture de l’étape 2. Aucun code applicatif, contrat ou donnée de TEST n’a été modifié pendant l’étape 2. Les objets fictifs de l’étape 1 restent décrits dans les limitations.

Les votes ont été contrôlés automatiquement : 12 profils distincts, 13 bulletins par profil, un argument par vote, seuil fixe de 7 POUR. Résultat : 10 orientations adoptées et 3 rejetées ; aucune égalité à 6 POUR. Les majorités ne constituent pas une validation utilisateur.

Contrôles exécutés le 19 novembre 2026 :

- `py -3 scripts/check_guidance.py` : 112 guides, 1 652 liens locaux, aucune erreur ni avertissement.
- `py -3 scripts/sync_documentation.py --check-sources` : 151 documents vérifiés.
- Contrôle ciblé du dossier : 241 liens Markdown, aucune cible manquante ; quatre fichiers JSON valides ; 156 votes cohérents avec les décisions.
- Prompt de l’étape 2 identique à la pièce jointe ; aucune valeur des identifiants fournis retrouvée dans les fichiers Markdown/JSON archivés.
- Relecture indépendante des livrables : aucun écart factuel ou de gouvernance relevé. Quatre dépôts applicatifs sans modification Git ; seul le dossier documentaire est ajouté.

Ces vérifications portent sur les livrables, pas sur le fonctionnement du CRM. Aucun nouveau test applicatif ou utilisateur exécuté pendant l’étape 2. Aucun commit, push ni déploiement demandé ou effectué. **Étape 2 clôturée ; étape 3 autorisée ensuite par l’utilisateur.**

## Étape 3 — maquettes et revue contradictoire

Le [prompt complet](prompts/03-maquettes.md) est archivé. Les cinq orientations P1 adoptées UX01–UX05 sont représentées par **12 scènes HTML statiques et 24 PNG bureau/mobile**, isolés du code applicatif. Les quinze captures AVANT restent conservées. Aucune orientation P2 ou rejetée n’a été ajoutée.

- [Galerie comparative AVANT/APRÈS](visuels/comparatif-avant-apres.html) — deux colonnes sur bureau, bascule sur smartphone.
- [Inventaire des scènes et des preuves](visuels/inventaire-maquettes.md).
- [Revue des douze profils et arbitrages complémentaires](visuels/arbitrages-complementaires.md).
- [Parti pris et limites de périmètre](visuels/parti-pris-visuel.md).

La revue compte 72 réponses aux six questions et 60 préférences individuelles réparties sur cinq orientations, toutes simulées. UX02 reste discutée : 5 préférences APRÈS, 7 réserves. Les corrections de libellé, de portée et de présentation ont été intégrées ; aucun changement substantiel des orientations n’a nécessité de nouveau vote. Les votes initiaux du backlog sont conservés et complétés par les références visuelles.

Les contrôles locaux couvrent les rendus à 1440 et 390 px, les cinq bascules comparatives, les douze sélections de scène, le clavier et le repli sans JavaScript. Aucun débordement horizontal détecté, aucune erreur JavaScript. Ils ne valident pas les fonctionnalités du CRM, son accessibilité complète ou son usage mobile réel. Les images APRÈS utilisent des données fictives, sans connexion à TEST ni modification des objets existants.

Contrôles documentaires de l’étape 3 : `check_guidance.py` sans erreur ni avertissement ; `sync_documentation.py --check-sources` avec 151 documents vérifiés. Le [contrôle ciblé de livraison](visuels/controle-livraison.json) confirme les liens, les empreintes des captures AVANT, le périmètre P1 et l’absence des valeurs sensibles fournies dans les fichiers texte archivés. Les quatre dépôts applicatifs sont sans modification Git.

À la clôture de l’étape 3, les prompts `00`, `04` et `05` restaient en attente. Aucune implémentation applicative, aucun commit, push ou déploiement effectué. L’étape 4 a ensuite été autorisée pour préparer la décision, sans validation implicite des maquettes.


## Étape 4 — dossier de validation préparé

Le [prompt complet](prompts/04-validation.md) est archivé. Les cinq P1 adoptées UX01–UX05 sont présentées avec parcours, problèmes, conséquences possibles, votes, captures réelles, maquettes, bénéfices, efforts, risques et dépendances.

- [Dossier de décision et fiches des cinq orientations](validation/dossier-decision.md).
- [Risques critiques pour la mise en usage, encore non résolus](validation/risques-non-resolus.md).
- [Registre des décisions utilisateur](validation/decisions.md) : **cinq EN ATTENTE DE DÉCISION ; zéro validation, refus, révision ou report reçu**.
- [Backlog d’implémentation potentiel](validation/backlog-implementation-potentiel.md), distinguant les quatre catégories de décision et les candidats en attente.

UX02 conserve 7 réserves visuelles simulées sur 12 malgré son adoption à 8 voix. Aucun P0 démontré ; les conditions de recette du pilotage, des rôles, du cycle RDV, du mobile et de la collaboration restent ouvertes. Aucune nouvelle recette applicative ou utilisateur n’est réalisée pendant l’étape 4.

Les prompts `00` et `05` restent en attente. Seul le dossier documentaire est modifié ; aucune implémentation ni donnée de TEST modifiée. **Attente de vos décisions explicites pour UX01–UX05. À leur réception : enregistrement, actualisation du backlog et du README, puis arrêt sans implémentation.**

Contrôles de préparation : `py -3 scripts/check_guidance.py` — 112 guides, 1 663 liens, zéro erreur et avertissement. Contrôle ciblé — 624 liens locaux sans cible manquante, cinq fiches complètes et cinq statuts en attente, valeurs confidentielles fournies absentes des fichiers texte, empreintes des captures AVANT conservées. Le rapport `validation/controle-preparation.json` conserve aussi les empreintes des maquettes soumises. Les quatre dépôts applicatifs sont sans modification Git. Aucun contrat ni source exportée modifié ; aucun test applicatif exécuté dans cette phase.


## Étape 5 — archive et relance

- Finalisation documentaire : **2026-11-19T07:43:58+01:00**, fuseau Europe/Paris ; début d’exploration le 18 novembre, heure initiale précise non archivée.
- URL analysée : https://test-crm.localeo.city ; branche `main`, commit documentaire `dd14e11c4522d2b6de1f9480cf30d50abaffc822` (HEAD vérifié à l’archivage). Les livrables sont locaux et non commités.
- Modèle déclaré de l’agent principal : Codex basé sur GPT-6 ; identifiant exact et niveau de raisonnement non établis. Modèles et raisonnement des agents précédents non établis ; voir la provenance.
- Protocole initial : instructions séquentielles 01–05, **aucun protocole global distinct ni numéro de version fourni**. Le prompt de relance **v1.0** est créé maintenant pour une future exécution, sans réécriture historique.
- Bilan : **13 orientations proposées, 10 adoptées et 3 rejetées en simulation**. Parmi les propositions : P0 = 0, P1 = 5, P2 = 6, P3 = 2 ; parmi les adoptées : P0 = 0, P1 = 5, P2 = 5, P3 = 0.
- Validation utilisateur : **0 validée, 0 refusée, 0 à réviser, 0 reportée ; 5 P1 en attente**. Les autres orientations restent hors du registre de décision de l’étape 4.

Parcours observés sur ordinateur : connexion d’un compte existant, accueil, recherche, création fictive et premier dossier, ajout de contact, historique, action avec date/rappel, liste des retards et réservation fictive de RDV. Qualification, pilotage collectif, préparation et agenda sont partiels. Statut, affectation effective, modification/report/annulation et compte rendu ne sont pas recettés dans l’interface. Aucun AVANT mobile exploitable, aucun test avec de vraies personnes et aucune livraison de rappel vérifiée.

- [Roadmap UX conditionnelle](synthese/roadmap-ux.md).
- [Plan de tests utilisateurs réels — huit scénarios](synthese/plan-tests-utilisateurs.md).
- [Inventaire, contrôles et anomalies d’archivage](synthese/controle-archivage.md).
- [Provenance des prompts et évolution du protocole](synthese/provenance-prompts.md).
- [Prompt complet d’archivage](prompts/05-archivage.md).
- [Prompt autonome de relance v1.0](prompts/RELANCER-WORKSHOP.md).
- [Contrôle final](synthese/controle-final.json) et [manifeste d’intégrité](synthese/manifest-integrite.json).

Limites d’archivage : `00` reste un constat de protocole non fourni ; cinq décisions manquent ; les recettes du registre de risques restent ouvertes. **Des noms de collaborateurs et des libellés commerciaux demeurent dans certaines captures réelles : l’archive n’est pas intégralement anonymisée.** Les valeurs des identifiants de connexion ne sont pas archivées. Aucun workshop CRM précédent dans le répertoire dédié : comparaison historique non applicable. Les objets fictifs de l’étape 1 restent dans TEST, sans nettoyage effectué ici.

**Statut final : archive documentaire finalisée avec réserves ; workshop incomplet et orientations non validées.** Aucune modification applicative, aucun commit, push ou déploiement. Cette archive ne vaut ni recette du produit, ni autorisation de mise en œuvre ou de lancement.
