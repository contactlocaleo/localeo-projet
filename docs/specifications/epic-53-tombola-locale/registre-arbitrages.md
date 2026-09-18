# Epic 53 - Registre des arbitrages

Les arbitrages fonctionnels du MVP sont valides. La validation juridique du
reglement reste une condition de mise en production et non un choix fonctionnel
encore ouvert.

| ID | Point a arbitrer | Explication detaillee | Priorite | Proposition simple | Validation ou amendement |
| --- | --- | --- | --- | --- | --- |
| TOM-ARB-01 | Condition de qualification | La qualification peut reposer sur une visite, un achat ou un montant minimum. | P0 | Un achat confirme par le commercant, sans montant minimum. | Valide. |
| TOM-ARB-02 | Nombre de chances | Des chances multiples complexifient le tirage, la lisibilite et l'anti-fraude. | P0 | Une chance unique par participant. | Valide. |
| TOM-ARB-03 | Preuve d'achat | Collecter un ticket ajoute des donnees et un traitement de controle. | P0 | Le scan par le commercant constitue la confirmation suffisante. | Valide. Aucun ticket ni montant collecte. |
| TOM-ARB-04 | Validations supplementaires | Elles peuvent mesurer la frequentation sans influencer le tirage. | P1 | Les conserver pour les statistiques, sans chance supplementaire. | Valide. |
| TOM-ARB-05 | Lots | Un lot libre imposerait une nouvelle logistique d'attribution. | P0 | Uniquement des coffrets Localeo reserves. | Valide. |
| TOM-ARB-06 | Canal participant principal | Dupliquer le parcours entre Marketplace et Live cree des divergences. | P0 | Marketplace pour la decouverte, Localeo Live pour le suivi ; conserver le lien public de repli. | Valide. Reprendre la mecanique deja presente pour le Passeport commercant. |
| TOM-ARB-07 | Tirage | Plusieurs tirages rapprochent le modele d'un instant gagnant. | P0 | Un tirage final apres cloture. | Valide. |
| TOM-ARB-08 | Perimetre territorial | Une tombola multi-communes complexifie droits, contenus et bilan. | P1 | Une commune par animation dans le MVP. | Valide. |
| TOM-ARB-09 | Validation juridique du reglement | La participation est conditionnee a un achat et les gagnants sont determines par tirage. Le reglement et les communications doivent etre valides avant commercialisation. | P0 | Produire un reglement type puis le faire valider juridiquement avant la premiere publication. | Valide pour la mecanique produit. La validation juridique effective reste obligatoire avant la premiere publication. |
| TOM-ARB-10 | Stockage des specificites du modele | Les attributs propres a chaque type d'animation doivent etre configurables sans multiplier les colonnes et les migrations specifiques. | P0 | Conserver la configuration versionnee comme source de verite en base ; ne denormaliser que les attributs requis pour la recherche, les contraintes ou les projections mesurees. | Valide. Reutiliser la mecanique du Passeport et documenter les attributs de `TOMBOLA_LOCALE` dans la conception technique. |
| TOM-ARB-11 | Validations repetees | Des scans illimites chez un meme commercant gonfleraient les statistiques et augmenteraient le risque de fraude sans ajouter de chance. | P0 | Une validation effective maximum par participant et par commercant ; les validations chez d'autres commercants restent statistiques. | Valide comme hypothese de conception. L'index effectif existant porte deja cette regle. |
| TOM-ARB-12 | Annulation et eligibilite | Une validation peut etre annulee avant cloture pour corriger une erreur ou une fraude. Il faut alors definir si la chance subsiste. | P0 | Recalculer l'eligibilite avant cloture ; la perte de la derniere validation retire la chance. La population gelee devient immuable a la cloture. | Valide comme hypothese de conception. |
| TOM-ARB-13 | Notification de qualification | Les validations supplementaires ne doivent pas produire des confirmations repetitives. | P1 | Notifier uniquement la premiere transition vers l'eligibilite dans Localeo Live, avec WebPush eventuelle et sans email au MVP. | Valide comme hypothese de conception. |

## Application dans Localeo Animation

Ces impacts declinent les decisions existantes ; ils ne creent pas de nouveaux
identifiants d'arbitrage.

| Arbitrages | Impact dans le portail partenaire |
| --- | --- |
| TOM-ARB-01, TOM-ARB-02, TOM-ARB-04 | Afficher la condition et la chance unique en lecture seule, sans multiplicateur ni chances additionnelles. |
| TOM-ARB-03 | Presenter une mission explicite de confirmation d'achat par scan, sans ticket ni montant. |
| TOM-ARB-05 | Reutiliser le parcours de financement et reservation des coffrets de l'Epic 46. |
| TOM-ARB-06, TOM-ARB-07 | Garder la console partenaire pour le pilotage du tirage final ; Marketplace decouvre et Localeo Live porte la participation. |
| TOM-ARB-08 | Configurer une seule commune, sans federation multi-communes. |
| TOM-ARB-09, TOM-ARB-10 | Consommer la version backend du reglement et le catalogue par API uniquement, sans lecture du JSONB brut. |
| TOM-ARB-11, TOM-ARB-12 | Afficher les projections backend d'unicite, d'eligibilite et de population gelee sans calcul local. |
| TOM-ARB-13 | Afficher la premiere qualification sans produire de notification repetitive. |

## Gouvernance du catalogue

L'administration appartient au Backoffice backend. La suppression physique
est interdite ; le code et la strategie sont immuables. La desactivation
retire un modele des nouvelles creations sans retirer les lectures
historiques. Une recette integree est obligatoire et toute nouvelle strategie
doit etre deployee dans le backend avant activation du modele. Les regles de
persistance et de version sont detaillees dans la [conception technique](conception-technique.md#7-persistance-et-migration).
