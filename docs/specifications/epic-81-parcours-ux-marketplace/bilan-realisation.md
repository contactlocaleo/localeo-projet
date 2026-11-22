# EPIC 81 — Bilan de réalisation locale

18 novembre 2026. **État produit : En cours.** Ce bilan concerne la réalisation locale des orientations de présentation O-01/O-02/O-03/O-06/O-07. Il ne vaut ni recette de lancement, ni validation juridique, ni clôture de l'epic. L'[epic](../../roadmap/en-cours/epic-81-parcours-ux-marketplace-20261118-backlog.md) et la [spécification](README.md) restent les sources de périmètre.

## Comportements réalisés

- **O-01 :** l'accueil explicite sur mobile et ordinateur le parcours d'expériences locales auprès de plusieurs commerçants, sans supprimer recherche, coffrets ni animations.
- **O-02 :** la fiche distingue la promesse garantie des exemples indicatifs et rassemble validité, adresses et précaution de réservation dans le bloc de décision. Les données de garantie et d'exemples restent celles de l'API ; aucun droit supplémentaire n'est calculé par le frontend.
- **O-03 :** le formulaire dit que le coffret consommateur est activé après confirmation du paiement, que la durée commence alors, que la confirmation arrive à l'acheteur et que la carte peut ensuite être préparée et partagée par lui, sans envoi automatique au proche. Cette rédaction suit le comportement vérifié du backend et du composant de carte cadeau.
- **O-07 :** prix total, validité, rappel de réservation et liens CGV/confidentialité précèdent le bouton final. La soumission et la redirection conservent leur code existant.
- **O-06 :** les actions des cartes nomment Localeo Live et distinguent consulter du fait de s'inscrire ; une animation clôturée n'annonce pas une inscription même si le booléen source est incohérent. Le retour depuis une fiche Live utilise l'origine Marketplace publique configurée et la commune validée de la projection ; un paramètre de retour arbitraire ne choisit jamais la destination. En l'absence d'origine valide, le faux retour n'est pas affiché. La navigation same-origin vers Live convertit l'URL canonique en chemin React local, évitant une page introuvable tout en conservant l'état de retour. La recette déployée doit vérifier les deux domaines réellement configurés.

## Critères et preuves

| Critère | État au 18 novembre | Preuve ou limite |
| --- | --- | --- |
| E81-CA-01 | Réalisé localement ; qualification humaine ouverte | Quatre largeurs 320/390/430/1440 px dans `epic81-home.spec.cjs`, comprises dans la suite finale de 41 tests Playwright réussis. |
| E81-CA-02 | Présentation réalisée ; validation contractuelle du catalogue ouvert | `purchase-promise.test.cjs`, `purchase-premium.spec.cjs`, tests de fiche à 200 % et plusieurs largeurs ; les textes de chaque offre publiée restent à confronter aux CGV et aux partenaires. |
| E81-CA-03 | Présentation réalisée ; recette du message réel ouverte | Code backend de validation de paiement et carte cadeau relus ; test navigateur de la fiche et du cadeau après achat simulé. Aucun envoi réel effectué. |
| E81-CA-04 | Réalisé localement ; recette juridique publiée ouverte | Test navigateur vérifiant l'ordre DOM des liens et du bouton, le prix et la lisibilité mobile/200 %. Aucun POST d'achat. |
| E81-CA-05 | Réalisé localement ; recette déployée du changement de domaine ouverte | Tests de deux origines distinctes, contexte communal, rejet d'un retour forgé et d'une origine invalide, animation clôturée, retour depuis recherche et focus. Les domaines réellement servis et la configuration publique restent à vérifier sur TEST déployé. |
| E81-CA-06 | Non vérifié | L'environnement de lancement et l'inventaire du catalogue ne sont pas identifiés ici. Les placeholders de TEST ne prouvent pas leur présence en production. |
| E81-CA-07 | Non vérifié | Aucune relecture de fiches ou droits visuels par des commerçants réels n'a eu lieu. |
| E81-CA-08 | Protocole préparé, porte non levée | [Protocole TEST](recette-stripe-test.md) : isolation et innocuité des effets métier doivent être établies avant tout appel. |
| E81-CA-09 | Non exécuté | Ni session Stripe ni paiement, retour, webhook ou état d'achat issus d'une recette EPIC 81 ; aucun succès n'est déduit des mocks. |
| E81-CA-10 | Non exécuté | Les six scénarios avec de [vrais utilisateurs](../../../ateliers/ux-workshops/marketplace/2026-11-18/synthese/plan-tests-utilisateurs.md) restent à organiser. Les votes de l'atelier étaient simulés. |

## Contrôles exécutés

- `node --test tests/security/purchase-promise.test.cjs` : **5/5 réussis**, 0 échec/skip.
- `node scripts/run-visual-tests.cjs --port 8273 tests/visual/epic81-home.spec.cjs tests/visual/purchase-premium.spec.cjs tests/visual/discovery-premium.spec.cjs tests/visual/live-context-return.spec.cjs tests/visual/live-entry-redirects.spec.cjs --workers=2` : **41/41 réussis**, rapport `test-results/visual-runs/2026-11-18T22-47-37-868Z-15iADi` (sortie locale non versionnée).
- `node scripts/run-visual-tests.cjs --port 8273 tests/visual/desktop-layout.spec.cjs --grep "la fiche coffret reste contenue sur mobile|la fiche coffret reste lisible à 200" --workers=1` : **2/2 réussis**, rapport `test-results/visual-runs/2026-11-18T22-49-43-411Z-REb8mM`.
- Après la revue indépendante, `node scripts/run-visual-tests.cjs --port 8273 tests/visual/epic81-home.spec.cjs tests/visual/discovery-premium.spec.cjs tests/visual/live-context-return.spec.cjs --workers=2` : **26/26 réussis**, rapport `test-results/visual-runs/2026-11-18T22-52-51-685Z-z0Nqbe`. Le test mobile vérifie l'absence de doublon ; ceux de Live vérifient l'origine distincte/invalide et l'animation clôturée.
- `node --test tests/security/public-config.test.cjs tests/security/purchase-promise.test.cjs` : **7/7 réussis** après ajout de la configuration d'origine Marketplace.
- `npx eslint` sur les fichiers JS/JSX touchés : **réussi** ; `git diff --check` : **réussi**. Le `npm run lint` global a rencontré un `EPERM` en parcourant `output/bum-politique/pytest-approval-1` (signalé pendant la revue), sans résultat global exploitable.
- Contrôles documentaires `py -3 scripts/check_guidance.py` et `py -3 scripts/sync_documentation.py --check-sources` : **réussis**, sans erreur ni alerte (151 sources).

Le premier passage Playwright a exposé un lien same-origin aboutissant à une page introuvable et des assertions anciennes sur l'URL d'inscription. Le chemin a été corrigé, les assertions alignées sur la route canonique et la suite finale ci-dessus a été rejouée d'un seul tenant. Un autre scénario de retour attendait une étape intermédiaire qui n'existe plus pour une participation déjà enregistrée ; il vérifie désormais le trajet direct, l'erreur puis le retour avec focus et position conservés. Les échecs initiaux ne sont pas comptés comme des succès du passage final.

## Impacts et reste à faire

**Dépôts modifiés :** `localeo-marketplace` pour les textes, la navigation, les styles et leurs tests ; `localeo-projet` pour la spécification, le protocole et la roadmap. `localeo-backend`, `localeo-animation` et `localeo-commercant` ont été consultés ou évalués sans modification applicative. Aucun endpoint, schéma, règle de paiement, permission, migration, requête supplémentaire ou traitement périodique n'a été modifié ; les tests restent sur fixtures locales. Le générateur de démonstration n'a pas été modifié, car l'origine et la destination des contenus provisoires O-05 ne sont pas établies.

Avant une clôture ou une ouverture publique : vérifier les contenus et droits visuels de l'environnement effectivement publié, confirmer les textes juridiques et chaque promesse coffret, injecter `LOCALEO_MARKETPLACE_PUBLIC_ORIGIN` dans la configuration publique du service frontend puis tester le changement de domaine sur les deux domaines déployés, lever la porte de sécurité de la recette Stripe puis documenter son résultat, et réaliser les tests auprès de vrais utilisateurs. Aucun achat réel, commit, push ou déploiement n'a été effectué dans cette réalisation.
