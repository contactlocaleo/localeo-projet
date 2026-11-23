# Relancer un workshop UX Localeo Live

Tu démarres une nouvelle conversation Codex, sans accès supposé aux échanges précédents. L’application publique à explorer est [Localeo Live TEST](https://test-live.localeo.city/). Prends Bouliac comme commune de référence, sauf consigne utilisateur plus récente. Traite trois missions en priorité. Participer aux animations et les retrouver, consulter et utiliser ses lots, puis consulter les animations en cours et à venir avec leurs dates et détails. Les coffrets restent secondaires. Le présent texte est un nouveau prompt autonome.

## Préparer le dossier

1. Lis le README et AGENTS.md de `localeo-projet`, les instructions locales de `localeo-marketplace` et les conventions pertinentes. Garde les cinq dépôts Git indépendants. Travaille dans le dépôt documentaire pour le workshop.
2. Recherche dans `ateliers/ux-workshops/`, y compris le sous-dossier `localeo-live/`, les README des workshops de Localeo Live. Prends le plus récent dont le statut est explicitement **TERMINÉ**. À défaut, annonce le recours au dossier le plus avancé comme référence provisoire. Au 23 novembre 2026, l’exécution archivée sous `ateliers/ux-workshops/2026-11-23/` est **PARTIELLE** et contient six maquettes P1 validées. Lis les preuves, analyses, votes, maquettes, décisions et prompts du dossier retenu. Une ancienne mention « PROMPT À FOURNIR » signifie que le texte source manque.
3. Détermine la date Europe/Paris. Crée `ateliers/ux-workshops/YYYY-MM-DD/`, avec suffixe `-02`, `-03`, etc. si nécessaire. Préserve les anciens dossiers. Prépare `prompts/`, `observations/`, `workshop/`, `visuels/captures-avant/`, `visuels/maquettes-apres/`, `validation/` et `synthese/`. Inscris dès l’ouverture date, heure, site, commune, branches, SHAs consultés, objectif, état et chemin dans le README. Archive mot pour mot la demande et chaque consigne utilisateur. Identifie les protocoles réellement suivis, les références disponibles et les textes manquants.

## Étape 1 · Explorer le site réel

Utilise Playwright ou un navigateur automatisé, à 320, 390 et 430 px. Inspecte accueil, choix de la commune, animations, entrée QR, inscription et récupération, participation et reprise, lots, programme et retour. Couvre états vides, chargements, erreurs et redirections. Demande les données autorisées pour les scénarios positifs. Si la visite reste publique, documente ce qui manque. Prends uniquement des captures AVANT du site réel. Les images fournies à part restent identifiées par leur provenance et leurs limites.

Lis les routes, composants, états et accès côté Marketplace en lecture seule. Distingue **OBSERVÉ**, **DÉDUIT** et **HYPOTHÈSE** dans `cartographie-parcours.md`, `inventaire-ecrans.md`, `observations-factuelles.md` et `limitations.md`. Relie chaque constat à sa preuve et compare aux observations historiques réévaluées. **Arrête-toi et attends l’autorisation explicite de simuler le workshop.**

## Étape 2 · Simuler le workshop

Simule six experts (UX senior, accessibilité, PM B2C, onboarding, recherche UX, facilitation) et six habitants aux usages distincts, dont plusieurs peu à l’aise avec le numérique. Donne à chacun une voix et une perspective indépendante. Marque tous les propos et votes comme simulés. Conduis six débats, sur la première impression, l’inscription et le QR, les lots, le calendrier, la maniabilité et l’accessibilité, puis la simplification et la reprise.

Pour chaque débat, présente preuves, répliques individuelles, points forts, problèmes, alternatives et votes nominatifs. Sur 12 voix, 7 à 12 pour donne **ADOPTÉE**, 6 donne **NON ADOPTÉE**, 0 à 5 donne **REJETÉE**. Les abstentions laissent le seuil fixe à sept. Garde les options rejetées et les risques critiques. Pour chaque orientation adoptée, renseigne priorité P0/P1/P2/P3, preuve ou hypothèse, bénéfice, critères d’acceptation, effort S/M/L/XL et confiance.

Livre rapport exécutif, compte rendu, registre, backlog, rejets et actions à faible effort. Donne six notes heuristiques justifiées, la matrice habitants × parcours et une décision **GO**, **GO SOUS CONDITIONS** ou **NO GO**. Compare les orientations, votes, priorités et notes avec la référence. Pour l’hypothèse d’ouverture à 10 000 habitants, présente jusqu’à cinq améliorations indispensables parmi les orientations adoptées. **Arrête-toi et attends l’autorisation de faire les maquettes.**

## Étape 3 · Maquetter les P0/P1 adoptées

Limite les planches aux P0/P1 qui ont obtenu au moins sept voix. Utilise l’AVANT authentique et précise quand l’équivalent manque ou quand une capture sert uniquement de contexte. Isole les maquettes du code applicatif et garde composants, identité et navigation de Live. Identifie les états illustratifs.

Crée `visuels/comparatif-avant-apres.html` avec deux colonnes sur ordinateur, une bascule mobile, une navigation par orientation et état, les identifiants, votes, priorités, bénéfices et efforts. Fais une revue contradictoire par les douze rôles simulés. Demande explicitement aux habitants peu familiers ce qu’ils comprennent, où ils appuient, si c’est plus simple, ce qu’ils préfèrent et ce qui reste incompris. Revote au seuil de sept si une proposition change substantiellement. Mets à jour le backlog, les preuves et le README. **Arrête-toi et attends la validation explicite de l’utilisateur.**

## Étape 4 · Enregistrer les décisions

Présente chaque P0/P1 avec mission, problème, priorité, vote, AVANT, APRÈS, bénéfice, effort et risque. Mentionne les problèmes critiques ouverts, quels qu’aient été les votes. Dans `validation/decisions.md`, laisse **EN ATTENTE** tant que la décision manque. Propose **VALIDÉE**, **REFUSÉE**, **À RÉVISER** ou **REPORTÉE**. Enregistre les décisions explicites avec date, commentaire, conditions et version des planches. Prépare les travaux applicatifs possibles selon ces catégories. **Arrête-toi après l’enregistrement des décisions. Attends une instruction distincte pour l’archivage final et une autorisation explicite pour tout développement.**

## Étape 5 · Archiver

Vérifie les prompts réellement utilisés, observations, captures, compte rendu, votes, backlog, maquettes, galerie, décisions, références de roadmap et plan de tests utilisateurs. Documente les manques, le périmètre effectivement testé et les réserves. Vérifie les fichiers, leurs liens, les versions validées et le rendu de la galerie. Contrôle l’état des dépôts applicatifs. Le README indique les métadonnées, les chiffres, les décisions et le statut réel. Un workshop incomplet reste **PARTIEL** même après archivage.

Complète `synthese/comparaison-precedent.md` avec les écarts vérifiés, problèmes persistants ou non réévalués, nouveaux constats, votes, priorités, orientations et notes. Identifie le prompt autonome de relance dans le nouveau dossier. Préserve l’historique et laisse l’implémentation à une demande ultérieure.
