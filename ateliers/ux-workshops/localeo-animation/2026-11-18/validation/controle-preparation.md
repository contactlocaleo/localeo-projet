# Contrôle de préparation — étape 4

18 novembre 2026, Europe/Paris. **Dossier préparé ; décisions utilisateur non reçues.** Aucun choix attribué à l’utilisateur. L’étape 4 reste en attente de ces décisions.

## Vérifications

- Neuf fiches P0/P1 adoptées, reliées aux observations, votes, captures réelles et maquettes v2. Les onze éléments demandés figurent dans chaque fiche ; les conséquences et bénéfices non mesurés restent qualifiés.
- Neuf entrées du registre portent EN ATTENTE DE DÉCISION, sans date, commentaire ni condition inventés. Les quatre catégories de décision sont vides ; les neuf candidats restent séparés dans le backlog potentiel.
- Les risques R1 à R6 du rapport sont présentés séparément, avec les dépendances B1/C1/C2/D1/E1 et la limite de preuve B3. Les rejets simulés ne sont pas transformés en refus utilisateur.
- Seuls README et prompt 04 sont modifiés parmi les 252 fichiers couverts par le manifeste d’étape 3 ; tous les visuels, observations, votes et backlog historique sont préservés. Les nouvelles pièces sont dans `validation/`.
- Les quatre dépôts applicatifs sont propres ; le dépôt documentaire signale uniquement le dossier non suivi `docs/ux-workshops/`. Aucune connexion à TEST, modification applicative, implémentation, migration, commit, push ou publication à cette étape.
- `py -3 scripts/sync_documentation.py --check-sources` : 151 documents vérifiés, succès.
- Le premier contrôle de liens a signalé les deux fichiers de contrôle encore en préparation ; ils ont été ajoutés avant la relance finale.

Résultat du contrôle documentaire final : `py -3 scripts/check_guidance.py` réussit (107 guides, 1551 liens locaux, 0 erreur, 0 avertissement). Le contrôle ciblé des nouvelles pièces et du README vérifie 172 liens et leurs ancres, neuf fiches complètes et neuf décisions en attente. Un lien relatif repris du rapport a été corrigé avant ce succès.

Le [manifeste de préparation](manifest-preparation-sha256.json) couvre l’état du dossier avant les décisions. Il devra rester historique lors de l’enregistrement des réponses. Les [décisions](decisions.md) demeurent la source des choix utilisateur ; les avis et votes du workshop restent des simulations.
