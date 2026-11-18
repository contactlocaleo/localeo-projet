# Référence des maquettes — étape 3

## Statut et périmètre

Propositions de conception du 18 novembre 2026 pour Bouliac, à valider. B1, C1, D1 et E1 sont les seules orientations représentées : P1, effort M, adoptées respectivement par 12, 12, 11 et 12 voix sur 12. Aucun P0 établi. A1/F1 (P2) et les alternatives rejetées restent hors périmètre.

Les [votes](../workshop/votes-et-arbitrages.md) et le [backlog](../workshop/backlog-ux.md) font foi. B1/C1/E1 sont conditionnelles à une recette établissant les écarts. Une planche différente de l’existant ne constitue pas une décision d’implémenter cette différence.

## Intention et composition

Conserver le carnet Live : fond clair, encre bleu foncé, action verte, symbole de marque, icônes en trait, panneaux arrondis. En-tête Localeo Live / Messages / Menu ; contexte ; information utile ; action ; détails secondaires ; trois onglets Mon carnet / Mes lots / Découvrir. Aucun quatrième onglet.

La galerie porte les annotations hors des images. Elle change instantanément d’orientation et d’état ; sur mobile elle bascule entre les versions. Aucun mouvement décoratif. Le focus reste sur la commande de sélection.

Le symbole est copié sans modification depuis `localeo-marketplace/public/img/header-mark.svg`. Les couleurs et proportions s’appuient sur les captures réelles et les composants existants ; ce dossier ne remplace pas les [principes UX canoniques](../../../../produit/live/principes-ux.md).

## Mode d’emploi

Ouvrir [la galerie](comparatif-avant-apres.html). Ordinateur : deux colonnes. Mobile : boutons AVANT/APRÈS. Choisir une orientation puis un état APRÈS. Les cadres se font défiler. Chaque état dispose d’un HTML isolé, d’un PNG de fenêtre et d’un PNG complet.

Les planches portent « MAQUETTE » et « Actions illustratives · Aucun envoi ». Boutons métier inertes, aucune API, aucun compte, aucun envoi de formulaire. Les sélecteurs de galerie, les détails natifs et les ancres de période sont interactifs. La continuité métier est **représentée**, pas exécutée. Les PNG complets déroulent le contenu et placent la navigation après celui-ci ; ils ne simulent pas une capture d’écran fixe.

## Correspondance des preuves

| Orientation | AVANT réel | Localisation / limite | APRÈS |
| --- | --- | --- | --- |
| B1 | [Formulaire](captures-avant/04-inscription-juste-prix-390x844.png) ; [fiche](captures-avant/03-detail-juste-prix-390x844.png) | O5/O6 : formulaire et contexte ; résultat positif non soumis. Aucune perte de contexte démontrée. | Inscription, confirmation hypothétique, résultat inconnu. |
| C1 | [Lots vides](captures-avant/08-lots-vides-390x844.png) ; [récupération](captures-avant/09-retrouver-carnet-390x844.png) | O7/O8 : contexte de rubrique seulement. **Avant attribué absent, comparaison non équivalente.** | Six états avec lot fictif. |
| D1 | [Programme Bouliac](captures-avant/02-decouvrir-bouliac-390x844.png) ; variantes 320/430 conservées | O4 : longues descriptions avant la rubrique future. Le bénéfice de compacité reste une hypothèse. | Programme, vide et erreur. |
| E1 | [Accès invalide](captures-avant/10-qr-invalide-390x844.png) ; [récupération](captures-avant/09-retrouver-carnet-390x844.png) | O9 : bouton à texte sombre sur vert ; erreur détaillée de saisie proposée, non capturée avant. | Récupération et erreur e-mail. |

Les 15 captures AVANT de Bouliac restent intactes. Aucun écran personnel n’est fabriqué comme preuve. Les accès personnels/QR autorisés n’étant pas disponibles, aucun nouvel avant personnel n’a pu être obtenu. Les confirmations B1, les données C1 et les états exceptionnels D1/E1 sont illustratifs.

## B1 — Inscription et continuité

| Planche | Condition d’affichage attendue | Lecture et action |
| --- | --- | --- |
| [Inscription](maquettes-apres/B1-inscription.html) | Animation publique reconnue | Commune, nom public, dates, conditions clés, quatre coordonnées, consentements, validation. |
| [Confirmation](maquettes-apres/B1-confirmation.html) | Réponse métier confirmant l’inscription | « Inscription confirmée », accès à la participation, absence de promesse de fin de jeu ou de gain. |
| [Incertain](maquettes-apres/B1-incertain.html) | Résultat non vérifiable | Impossibilité de confirmer ; vérification sans nouvelle inscription ; récupération. |

Enchaînement représenté : QR connu → fiche existante → inscription → réponse confirmée ou résultat inconnu → participation autorisée ou récupération existante → retour à la destination connue. Le QR inconnu rejoint le cas E1, sans déduire l’animation.

Le formulaire conserve nom, prénom, e-mail, téléphone, majorité, règlement ; les nouvelles restent facultatives. Le panneau de règlement est un emplacement éditorial : le contenu complet réel reste obligatoire avant implémentation ; la maquette ne fournit pas un nouveau règlement.

Retour formulaire/confirmation : fiche de l’animation connue. Retour d’une récupération : destination autorisée correspondant à la demande. Le nom public peut être conservé ; aucune identité personnelle n’est déduite d’un code inconnu.

« Vérifier mon inscription » exprime une intention de lecture, pas une nouvelle recherche d’identité. Vérifier sa réalisation avec les capacités existantes. Si aucun accès personnel n’est disponible, utiliser la récupération existante ; ne créer ni endpoint, ni nouvelle confirmation locale. Les cas de rejet et leurs messages dépendent de la réponse réelle ; ils ne sont pas inventés ici.

## C1 — Lots

| Planche | Donnée métier / condition | Action autorisée |
| --- | --- | --- |
| [Disponible](maquettes-apres/C1-disponible.html) | VALIDE confirmé et retrait effectivement autorisé | Présenter mon bon. |
| [Incertain](maquettes-apres/C1-incertain.html) | Lecture impossible ; état actuel inconnu | Actualiser ; QR masqué ; dernier état connu explicitement ancien. |
| [Remis](maquettes-apres/C1-remis.html) | CONSOMME confirmé | Aucun retrait ; contact organisateur. |
| [Expiré](maquettes-apres/C1-expire.html) | EXPIRE confirmé | Aucun retrait ; contact. Date fictive passée au 17 novembre. |
| [Annulé](maquettes-apres/C1-revoque.html) | REVOQUE confirmé | Libellé habitant « Bon annulé » ; aucune nouvelle règle. |
| [Bon](maquettes-apres/C1-bon.html) | VALIDE fraîchement vérifié | Zone QR non scannable ici ; fermer relit l’état. Affichage et fermeture ne remettent pas le lot. |

« Panier garni », l’animation d’exemple, Commerce exemple, son adresse et les dates sont fictifs. Ils illustrent des modalités de remise, sans prétendre à leur disponibilité dans les données réelles.

Ordre : gain → état → échéance → lieu → comment → action. Pour les états non utilisables, les anciennes coordonnées sont des informations de contexte, sans instruction de retrait. En cas d’incertitude, elles ne valent pas confirmation : vérifier avant déplacement.

Données absentes : afficher « Date limite non renseignée », « Lieu de retrait non renseigné » ou « Modalités à confirmer auprès de l’organisateur », selon le champ manquant. Ne pas compléter par supposition. N’afficher une cause d’annulation, une date de remise ou une fraîcheur précise que si elle existe dans les données autorisées.

Préservés : actualisation, retour Mes lots, contact organisateur, distinction vu/remis, stockage local du carnet et validation par code lorsque la capacité existe. « Ajouter au carnet » dans l’exemple correspond à un bon non mémorisé ; pour un accès déjà mémorisé, conserver le libellé/action existant approprié. La validation PIN est secondaire et conditionnelle au bon ; aucune capacité généralisée. La récupération reste accessible dans Mes lots via le retour, comme sur l’avant réel.

Pas de nouvelle transition métier, possibilité de retrait par un tiers, exigence de pièce d’identité ou horaire de commerce inventé. Le domaine garde l’autorité sur la disponibilité et la remise.

## D1 — Programme

[Programme compact](maquettes-apres/D1-programme.html), [vide](maquettes-apres/D1-vide.html), [erreur](maquettes-apres/D1-erreur.html).

Le 18 novembre 2026 : deux animations en cours, une prochaine. L’ordre au sein des sections utilise les dates confirmées ; pas de statut recalculé pour remplacer le backend. Les périodes restent celles des captures.

- Juste Prix Local : 15–22 novembre, un commerce, bonne estimation et passage validé, chance au tirage après qualification.
- Jeu des vitrines : 18–21 novembre, une réponse définitive, sans achat.
- Tombola Locale : 19–23 novembre, achat requis sans minimum chez un partenaire, inscription obligatoire.

Le détail garde les règles complètes, dotations et restrictions. Les conditions clés ne deviennent pas une promesse de gain. Une donnée de date absente est indiquée, pas complétée.

Le raccourci Prochainement conduit à sa section. Zéro animation donne un message explicite, sans liens d’ancre morts ni faux compte. Une erreur distingue le dernier programme connu du résultat actuel inconnu ; aucun badge vert « En cours » n’est maintenu pour l’état non vérifié. Un chargement initial ne vaut pas « aucune animation » : conserver l’état de lecture existant, sans ajouter de planche de chargement non nécessaire.

Rechercher, changer de commune, consulter les commerces, partager et ouvrir la fiche restent présents. Retour fiche → programme conserve la commune, les filtres et la position pertinente (exigence non exécutée dans les planches statiques). Aucun calendrier mensuel imposé ; aucun export ICS existant supprimé par cette proposition qui ne redessine pas le détail du tirage.

## E1 — Accessibilité ciblée

[QR invalide](maquettes-apres/E1-acces-invalide.html), [erreur e-mail](maquettes-apres/E1-formulaire-erreur.html). Le premier garde une récupération existante ; le second illustre une erreur explicite associée au champ, avec valeur conservée.

Cibles essentielles de 44 px ou plus, champs à 16 px, labels visibles, focus contrasté, trois onglets textuels, état nommé sans dépendre de la couleur. Résumé d’erreur en texte et association aria-describedby/aria-invalid. La palette retenue doit être contrôlée dans chaque futur état applicatif ; la présente maquette ne valide pas l’application.

La lecture du code et le contrôle navigateur des planches sont distincts de tests au lecteur d’écran, sur clavier virtuel ou avec des habitants. Voir [contrôles](controles/controle-technique.md).

## Revue et portée

La [revue contradictoire](revue-contradictoire.md) rassemble six experts et six habitants fictifs, sur les contenus transmis. L’agent principal inspecte les rendus ; les sous-agents n’avaient pas d’accès direct aux fichiers. Aucun test terrain, clic habitant ou préférence réellement recueillie.

Les corrections de formulation et de représentation restent dans B1/C1/D1/E1. Aucun changement substantiel retenu : aucun nouveau vote. Les votes d’origine restent inchangés. Validation utilisateur attendue avant la suite.
