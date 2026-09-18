# Epic 53 - Tombola locale des commercants

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-53-tombola-locale-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Objet

Cette Epic ajoute un deuxieme modele d'animation au socle de l'Epic 41. Une personne inscrite devient eligible au tirage apres un achat, sans montant minimum, valide chez l'un des commercants participants.

Le MVP privilegie une mecanique volontairement simple : une personne, une validation qualificative et une chance au tirage.

## Documents

- [Backlog](../../roadmap/terminees/epic-53-tombola-locale-backlog.md)
- [Registre des arbitrages](registre-arbitrages.md)
- [Conception technique](conception-technique.md)

## Ancrage dans l'existant

| Existant | Reutilisation |
| --- | --- |
| Catalogue `ModeleAnimation` | Ajouter `TOMBOLA_LOCALE` sans coder un second moteur |
| Participant et QR Animation | Inscription et identification du participant |
| Validation commercant | Preuve de l'achat confirmee par le commercant |
| Population eligible | Figee lors de la cloture |
| Tirage, suppleants et gains | Reutilises sans changement de nature |
| Commande de lots | Coffrets achetes et reserves par le partenaire |
| Notifications Animation et Live | Validation, cloture, resultat et gain |
| Epic 49 | Projection publique Marketplace |

## Regle metier structurante

La premiere validation effective chez un commercant participant rend le participant eligible. Les validations suivantes peuvent etre comptees dans les statistiques de frequentation, mais n'ajoutent aucune chance au tirage dans le MVP.

Le scan du QR vaut confirmation par le commercant qu'un achat a ete effectue. Aucun montant ni justificatif n'est collecte.

## Arbitrages integres au MVP

Les decisions detaillees et leur justification sont conservees dans le
[registre des arbitrages](registre-arbitrages.md). Le MVP repose sur les choix
actes suivants :

| Sujet | Decision |
| --- | --- |
| Inscription | Une inscription par personne et par Tombola. |
| Qualification | Un achat confirme par un commercant participant, sans montant minimum. |
| Preuve | Le scan du QR participant par le commercant suffit ; aucun ticket ni montant n'est collecte. |
| Chances | Une chance unique par participant, acquise a la premiere validation effective. |
| Validations suivantes | Elles alimentent les statistiques, sans modifier les chances de gagner. |
| Lots | Uniquement des coffrets Localeo achetes et reserves pour l'animation. |
| Parcours participant | Marketplace pour la decouverte, Localeo Live pour l'inscription et le suivi, avec le lien public de repli existant. |
| Tirage | Un tirage final apres cloture sur une population eligible figee. |
| Territoire | Une seule commune par tombola dans le MVP. |
| Reglement | Un reglement type propre a la Tombola, configurable selon la mecanique du Passeport, puis valide juridiquement avant la premiere publication. |
| Configuration | Les specificites de `TOMBOLA_LOCALE` sont conservees dans la configuration versionnee ; une denormalisation n'est introduite que pour un besoin technique explicite. |
| Validations repetees | Une validation effective maximum par participant et par commercant ; les autres commercants alimentent uniquement les statistiques. |
| Annulation | L'eligibilite est recalculee avant cloture, puis la population gelee devient immuable. |
| Notification | Une seule notification lors de la premiere qualification, dans Localeo Live avec WebPush eventuelle. |

La validation juridique finale du reglement reste une condition de
commercialisation. Elle ne bloque pas la conception ni l'implementation du
moteur.

## Frontieres de responsabilite

- le Backoffice supervise le modele et les incidents, mais ne pilote pas nominalement la tombola ;
- Localeo Animation configure et exploite la tombola pour le partenaire ;
- la Marketplace assure la decouverte publique ;
- Localeo Live porte l'inscription, le QR, la progression et les notifications participant ;
- l'application commercant produit la validation terrain.

## Integration de Localeo Animation

Le portail consomme le catalogue par `GET /protected/animation-locale/modeles`,
sans acces direct a la table backend ni a son JSONB. Il utilise `code` comme
identifiant stable, les libelles et les definitions fournis par l'API, et
propose uniquement les modeles actifs. Une desactivation bloque les nouvelles
creations mais conserve la consultation des animations existantes.

Localeo Animation construit le formulaire depuis le contrat du modele,
presente les constantes Tombola en lecture seule et configure dates,
commercants, mission, lots, contenus et visuels. Il pilote invitations et
acceptations selon l'Epic 56, puis le financement des coffrets selon l'Epic 46.
Le suivi, la cloture, le tirage, les suppleants, les gains et les exports
utilisent les projections et commandes backend sans recalcul local de
l'eligibilite.

Le [volet frontend de la conception](conception-technique.md#91-localeo-animation)
detaille les champs consommes, les constantes, les erreurs et les tests.
Le catalogue est administre uniquement dans le Backoffice backend. Une
modification de ses definitions exige une recette integree ; tout nouveau
comportement exige une strategie backend deployee avant activation.

## Hors perimetre MVP

- chances multiples ou liees au montant ;
- ticket de caisse photographie ;
- tirages instantanes ;
- lots autres que les coffrets Localeo ;
- federation de plusieurs communes ;
- administration du catalogue depuis Localeo Animation.

## Consequences pour la conception technique

- strategie de qualification `TOMBOLA_LOCALE` portee par le domaine et enregistree dans un registre extensible de modeles ;
- contrat de validation explicitant la confirmation d'achat, sans montant ni justificatif ;
- calcul idempotent d'une chance unique a partir de la premiere validation effective ;
- configuration versionnee comme source de verite des attributs propres au modele ;
- projections de statistiques par commercant ;
- reglement par defaut et mission commercant propres au modele ;
- tests de non-regression garantissant que le Passeport conserve son comportement.

[Retour à l’index des spécifications](../INDEX.md)
