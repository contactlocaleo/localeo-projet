# Roadmap UX Marketplace Localeo — issue du workshop du 18 novembre 2026

Cette roadmap est une **séquence candidate**, pas un calendrier de développement ni une décision de mise en production. Les sept orientations P0/P1 ont été validées par [réponse globale du propriétaire](../validation/decisions.md). Les votes du workshop étaient simulés. Les dépendances du [dossier de décision](../validation/dossier-decision.md) restent à lever ; aucune interface n'a été implémentée.

## Avant lancement — P0/P1 validées

| Ordre de préparation | ID | Priorité | Résultat attendu et critère de sortie | Dépendances |
| --- | --- | --- | --- | --- |
| 1 | O-08 | P0, porte de validation | Recette sûre de l'initialisation, de la redirection Stripe et du retour ; preuves succès/échec et état de commande consignées. **Aucune panne n'est actuellement démontrée.** | Innocuité des effets métier confirmée avant toute requête ; environnement et données TEST autorisés ; aucun paiement réel. |
| 2 | O-02 | P1 | Sur la fiche, la promesse garantie, les exemples, la validité et la réservation sont identifiables avant achat. | Vérification de la promesse canonique, des CGV et des prestations avec les commerçants. |
| 3 | O-03 et O-07 | P1 | Un seul parcours de lecture explique le cadeau et place les conditions décisives avant le bouton, sans répétition contradictoire. | Vérifier l'envoi réel, l'activation, l'usage du téléphone et les textes juridiques ; coordonner avec O-02. |
| 4 | O-01 | P1 | Le premier écran mobile nomme le parcours d'expériences locales et conserve recherche, coffrets et animations. | Test de reformulation à 320/390/430 px ; validation éditoriale. |
| 5 | O-05 | P1 conditionnel | Aucun contenu provisoire n'est publié dans l'environnement réellement ouvert ; un échantillon de fiches est relu par les partenaires. | Inventaire de l'environnement de lancement. Si les placeholders n'y figurent pas, l'entretien éditorial devient P2. |
| 6 | O-06 | P1 | La destination Localeo Live et la différence entre consulter et participer sont explicites, avec commune transmise et retour vérifié. | Vérification des liens Marketplace–Live et test d'inscription dans un cadre distinct. |

La validation UX des orientations n'autorise pas automatiquement une implémentation. Le [plan de tests](plan-tests-utilisateurs.md) prévoit de confronter les hypothèses aux vrais visiteurs et commerçants ; les contrôles d'accessibilité et les erreurs du parcours réel restent à inclure dans la recette.

## Après les premiers retours — P2

| ID | Statut actuel | Condition de réexamen | Suite possible |
| --- | --- | --- | --- |
| O-04 — entrée « Choisir une commune » dans la recherche | Adoptée par **vote simulé 8/12**, classée P2 ; **non soumise à la validation propriétaire de l'étape 4**. | Tests réels montrant que les catégories mêlées ralentissent la découverte, ou retour observable sur la perte des filtres. | Décider explicitement si une évolution ciblée de l'entrée commune et du retour avec filtres mérite un lot. |
| O-05 — entretien éditorial si aucun placeholder n'est publié | Orientation validée, mais son urgence P1 est conditionnelle. | Inventaire de l'environnement de lancement ne révélant aucun contenu provisoire. | Poursuivre la vérification périodique des fiches comme tâche P2, sans double compter une nouvelle orientation. |

## Évolutions futures — P3

**Aucune orientation P3 n'est validée ni planifiée.** O-09 (refonte graphique totale) a été rejetée 3/12 et O-10 (intégration complète de Live dans Marketplace) n'a pas été adoptée à 6/12 lors du workshop simulé. Elles ne deviennent pas automatiquement une roadmap future. Elles ne pourraient être rouvertes qu'avec des preuves nouvelles, un cadrage métier/technique et une nouvelle décision du propriétaire.

## Points de contrôle avant toute annonce de lancement

- Le statut **GO SOUS CONDITIONS** du [rapport exécutif](../workshop/rapport-executif.md) est une recommandation heuristique, non une autorisation de lancement.
- Les textes de prix, garantie, réservation, carte cadeau et CGV doivent rester cohérents entre écrans et contrat.
- La qualité des contenus réellement publiés, le parcours complet de paiement et l'accessibilité de l'application restent à vérifier ; les maquettes statiques ne sont pas des preuves de ces comportements.
