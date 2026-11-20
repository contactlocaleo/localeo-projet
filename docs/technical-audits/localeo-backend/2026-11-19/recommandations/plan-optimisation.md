# Plan court d’optimisation soumis à choix

Préparer d’abord **OPT-01 (A/P1/S)**, puis **OPT-02 (B/P1/M)** si l’utilisateur les valide individuellement. Les six P2 restent des candidats conditionnels. Aucun P0 démontré ; aucun chantier C/D recommandé. Les [huit fiches](backlog-final.md) portent preuves, alternatives, tests et retours arrière ; le [registre](../validation/decisions.md) ne contient aucun choix utilisateur.

| Lot proposé | Périmètre minimal | Preuve attendue avant acceptation | Condition de lancement |
| --- | --- | --- | --- |
| 1 — OPT-01 | Déport des quatre batchs ERP, contexte capturé et sessions confinées au thread | Même identité/corrélation/réponse ; témoin et scan progressent pendant I/O ; erreurs et déconnexion maîtrisées, pas de rejeu aveugle | Choix explicite sur OPT-01 |
| 2 — OPT-02 | Budget des cycles email/SMS et réservations progressives ; bail propriétaire si nécessaire | Travail non commencé reprenable, révocation et incertitude préservées ; deux lanceurs PostgreSQL jetables, pertes de bail et crash | Choix explicite sur OPT-02 ; cible jetable disponible pour la preuve intégrée |
| Suite — P2 | Choisir selon coût observé : progression des relances, Live/détails, expiration, CSV, médias ou Stripe | Exposition réelle et mesure avant/après du scénario concerné, sans perte de contrat | Choix ultérieur par ID ; aucune validation en bloc déduite des P1 |

Les deux P1 ont des causes distinctes : déporter ne borne pas le cycle ; borner le cycle ne rend pas le handler async non bloquant. Ils peuvent être arbitrés séparément et doivent rester des changements séparables. Sur les mêmes fichiers, les réaliser séquentiellement pour isoler les preuves et le retour arrière. OPT-02 est limité aux communications email/SMS ; examiner les autres batchs ne les inclut pas dans ce lot.

Maîtriser le coût : utiliser les mécanismes existants, éviter nouvelle dépendance, service de file, schéma ou migration. S/M sont des estimations relatives incluant recette ; aucune promesse de jours, euros ou pourcentage de gain. Ne pas lancer plusieurs P2 sans preuve d’exposition ; pour OPT-04, mesurer Live puis détail avant le dashboard historique dont l’UI actuelle utilise le mode borne. À 10 000 lignes, le CSV n’a montré aucun épuisement : OPT-06 reste P2 différable, volumes réels inconnus.

Le banc de l’étape 4 a mesuré des mécanismes locaux et simulé le bail. Capacité HTTP/PostgreSQL, saturation réelle et gains après correction restent **NON MESURÉS**. Pour les validations intégrées futures : versions réellement utilisées, ressources et budgets fixés avant essai, base jetable explicitement désignée, données synthétiques, fournisseurs doubles, paliers et arrêts du [protocole](../benchmarks/protocole.md). Une suite ignorée ou un simple import n’accepte ni un invariant ni une capacité.

Avant/après : même jeu/configuration et contrat, mesurer M01 ou M02 puis le scénario P2 choisi ; suivre lag, latence API, erreurs, CPU, RSS, checkout/verrous, durée de cycle et âge de file selon le flux. Les critères structurels des fiches sont obligatoires, même si la latence baisse. Aucun seuil produit inventé ; fixer les objectifs avec l’utilisateur/ops avant campagne intégrée. Ne pas accepter un gain qui transfère la contention vers le pool ou le disque.

Retour arrière : chaque lot doit être réversible par code sans migration. Terminer ou gérer les opérations en cours avant bascule ; conserver journaux, paiements, remises et réservations. Une communication incertaine se rapproche, elle ne se rejoue pas pour faciliter un rollback. Les procédures des fiches décrivent un plan, aucune opération externe n’est exécutée ici.

Impacts : seul ce dossier documentaire change à l’étape 5. Backend concerné par les corrections candidates ; contrats ERP/Animation/Marketplace à préserver selon chaque fiche, aucun frontend modifié. Aucun nouveau comportement produit, critère d’acceptation, contrat OpenAPI, migration ou donnée de démonstration : pas de changement du générateur à ce stade. Après choix, vérifier les consommateurs et preuves proportionnées au lot réel ; ne pas modifier les quatre applications par principe.

**Point d’arrêt actuel : attendre le choix utilisateur pour OPT-01 et OPT-02.** Les votes simulés et la recommandation de l’orchestrateur n’autorisent rien. Aucune implémentation, charge supplémentaire, installation, migration, commit, push ou déploiement dans cette étape.
