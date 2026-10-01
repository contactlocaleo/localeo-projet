# Roadmap par etat

Classement consolidé le 18 septembre 2026, complété le 30 septembre par l’EPIC 68. Les backlogs des applications sont
réunis dans les dossiers d'état, avec un seul fichier par EPIC. Le suivi inclut
les 68 identifiants du tronc commun et trois identifiants applicatifs distincts.

| Etat | Epics | Dossier |
| --- | ---: | --- |
| Terminees | 58 | [terminees/](terminees/README.md) |
| A faire | 8 | [a-faire/](a-faire/README.md) |
| En cours | 2 | [en-cours/](en-cours/README.md) |
| Abandonnees | 2 | [abandonnees/](abandonnees/README.md) |
| Fusionnee | 1 | Epic 61 reprise dans l'[Epic 60](terminees/epic-60-vision-360-commercialisation-backlog.md) |

Les 64 identifiants historiques et leurs états sont conservés ; l’EPIC 65 ajoute
les vues ERP d’audit, paiements et reversements, et l’EPIC 66 ajoute Localeo Atelier
pour composer des coffrets avec l’aide de l’IA. L’EPIC 67 ajoute les communautés
de communes et les coffrets intercommunaux. L'EPIC 68 ajoute le parcours commerçant
de préparation et finalisation de l'onboarding. Les EPIC 65, 67 et 68 sont à faire ;
l'EPIC 66 est en cours depuis le 29 septembre, avec une implémentation locale en validation.
La spécification V1.2 couvre ses extensions `E66-PWA-20260929` (PWA/menu ERP),
`E66-PRIX-20260929` (prix proposé modifiable) et `E66-EXPERIENCE-20260929`
(expérience multi-prestations, sans coffret matériel). Elles sont implémentées et
testées localement ; la recette des appareils déployés reste à faire, sans changement d'état produit.
L'[EPIC 35](terminees/epic-35-profils-backoffice-differencies-backlog.md)
porte aussi un cadrage d'évolution du 28 septembre vers les profils Lecteur,
Backoffice et Admin, à spécifier et implémenter ; sa clôture historique et les
totaux ci-dessus restent inchangés.
Les Epics 3 et 4 n'ont pas de fichier dedie :
leurs descriptions dans la roadmap produit sont referencees depuis le dossier
des epics terminees. Aucun fichier autonome de l'Epic 61 n'est recree.

## Contributions applicatives et collisions de numéros

- L'ancien numéro **Marketplace 53**, consacré à la pagination, est fusionné
  dans l'[EPIC 57](terminees/epic-57-bornage-pagination-api-marketplace-backlog.md).
  La tombola conserve le numéro 53.
- [EPIC-MARKETPLACE-18 — Google Analytics](terminees/epic-marketplace-18-google-analytics-marketplace-backlog.md)
  est distincte de la page commerçant immersive (EPIC 18). Sa V1 est livrée ;
  la collecte reste suspendue par MARKET-001.
- [EPIC-MARKETPLACE-54 — Identité visuelle](a-faire/epic-marketplace-54-harmonisation-identite-visuelle-marketplace-backlog.md)
  est distincte du calendrier de l'Avent (EPIC 54). L'implémentation locale est
  livrée selon le bilan historique ; la revue et la recette connectée restent attendues.
  Le classement courant est **à faire**.
- [EPIC-PRES-CONTENU-001 — Édition des prestations](terminees/epic-animation-edition-prestations.md)
  conserve son identifiant et rejoint les terminées : le parcours d'édition directe
  existe déjà. Le futur sas de validation reste à faire dans l'EPIC 62.

Les spécifications sont regroupées par fonctionnalité dans leur [index](../specifications/INDEX.md).
Le [compte rendu de consolidation](../organisation/consolidation-roadmap-2026-09-18.md)
précise la provenance et les divergences historiques conservées.

## Decisions de classement

| Epic | Etat retenu | Constat |
| --- | --- | --- |
| 5 | Abandonnee | Le backlog annule explicitement le QR commercant au profit de l'authentification de l'Epic 10. |
| 12 | Abandonnee | Le paiement manuel est decommissionne par l'Epic 39 ; le document reste une trace historique. |
| 47 | Terminee | Cloture produit confirmee par l'utilisateur le 15 septembre 2026 ; l'ancienne reserve de recette reste une reference d'exploitation. |
| 54, 58, 62, 64 et EPIC-MARKETPLACE-54 | A faire | Classement courant des dossiers ; voir les réserves de chaque backlog. |
| 55 | En cours | Moteur commun et chasse au trésor ; conception, arbitrages et livraison suivis dans le backlog. |
| 65 | A faire | Spécification V1.2 du 30 septembre des trois vues ERP audit, paiements et reversements ; socle ADMIN et dépendance E35 explicités, aucune implémentation livrée. |
| 66 | En cours | [Localeo Atelier](en-cours/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md) : [V1.2](../specifications/epic-66-localeo-atelier/README.md) implémentée localement, PWA, prix automatique modifiable et prompt expérience testés ; limites de recette dans le bilan, aucune clôture. |
| 67 | A faire | [Communautés de communes](a-faire/epic-67-communautes-communes-coffrets-intercommunaux-backlog.md) : référentiel, coffrets intercommunaux, commercialisation et extension de Localeo Atelier ; droits et achats existants préservés. |
| 68 | A faire | [Préparation de l'onboarding](a-faire/epic-68-parcours-commercant-preparation-onboarding-backlog.md) : parcours partagé avant un rendez-vous d'une heure, Stripe, documents, contrat, prestations et questions ; dix-sept critères cadrés, calendrier et déroulé à arbitrer. |
| 61 | Fusionnee | Contenu repris dans l'Epic 60 ; une fusion n'est pas un abandon. |
| 35 | Terminee (historique) | Évolution `E35-PROFILS-20260928` cadrée dans son backlog : trois profils et séparation métier/technique, non livrée ; aucun nouvel identifiant créé. |
| Autres identifiants du tronc commun | Terminees | Statut produit consolide conserve ; les anciennes mentions de stories a faire ne rouvrent pas ces epics. |

Les changements des Epics 5, 12 et 47 corrigent des incoherences entre les
anciens totaux globaux, les decisions explicites des backlogs et la confirmation
de cloture de l'Epic 47 par l'utilisateur. Les historiques
de stories restent conserves. Ce rangement n'est pas une nouvelle recette de
toutes les fonctionnalites : les limites de mise en service, notamment des
Epics 50 et 63, restent documentees dans leurs dossiers.

## Documents transverses

- [Roadmap produit consolidee](product-roadmap.md).
- [Suivi backlog et historique des stories](suivi-backlog.md).
- [Roadmap securite et performance](a-faire/security-performance-roadmap.md).
- [Sprint securite immediate](a-faire/sprint-1-securite-immediate.md).

Lors d'un changement d'etat, deplacer tous les documents de l'epic, actualiser
les index et les deux syntheses, puis verifier les liens entrants et sortants.
Conserver les noms de fichiers pour faciliter le suivi dans Git.
