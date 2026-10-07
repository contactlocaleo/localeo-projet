# Roadmap par etat

Implémentations locales E70 et E72 vérifiées les 7–8 octobre 2026 : [E70 — PIN](../specifications/epic-70-validation-pin/README.md) et [E72 — salariés](../specifications/epic-72-acces-salaries/README.md). E70 est publiée avant le lot E72 ; les deux epics restent en cours jusqu’à leur recette de mise en service. Aucun déploiement effectué.

Classement consolidé le 18 septembre 2026, complété le 5 octobre par l’EPIC 72. Les backlogs des applications sont
réunis dans les dossiers d'état, avec un seul fichier par EPIC. Le suivi inclut
les 71 identifiants du tronc commun et trois identifiants applicatifs distincts.

| Etat | Epics | Dossier |
| --- | ---: | --- |
| Terminees | 61 | [terminees/](terminees/README.md) |
| A faire | 6 | [a-faire/](a-faire/README.md) |
| En cours | 4 | [en-cours/](en-cours/README.md) |
| Abandonnees | 2 | [abandonnees/](abandonnees/README.md) |
| Fusionnee | 1 | Epic 61 reprise dans l'[Epic 60](terminees/epic-60-vision-360-commercialisation-backlog.md) |

Les 64 identifiants historiques et leurs états sont conservés ; l’EPIC 65 ajoute
les vues ERP d’audit, paiements et reversements, et l’EPIC 66 ajoute Localeo Atelier
pour composer des coffrets avec l’aide de l’IA. L’EPIC 67 ajoute les communautés
de communes et les coffrets intercommunaux. L'EPIC 68 ajoute le parcours commerçant
de préparation et finalisation de l'onboarding. L'EPIC 67 est à faire et l'EPIC 68 est en cours ; l'EPIC 65 est terminée depuis le 2 octobre après validation locale des dix critères ;
l'EPIC 66 est terminée depuis le 1er octobre, après confirmation de recette par l'utilisateur.
Le cadrage de l'[EPIC 68](en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md)
intègre les neuf recommandations acceptées le 1er octobre : suivi sans double saisie,
confirmation immédiate, pack J−7 et secours SMS, préparation commerçant accessible
avant activation, rendez-vous en quatre phases et guide ERP. La
[spécification V1.2 du 3 octobre](../specifications/epic-68-preparation-onboarding/README.md)
trace ses 31 critères, les contrats et les tests attendus ; guide et supports sont
rédigés. Seul le dépôt de pièces commerçant est différé ; l'espace de préparation
est conservé, avec sept étapes et une prochaine action visible. Les paramètres ont été validés le 3 octobre et l'implémentation V1.2 est en cours. L'approbation éditoriale des supports et la recette déployée restent distinctes.
Le 3 octobre, le parcours précise le contrat téléchargeable avant J, signé le
jour J puis déposé par Localeo, ainsi qu'une confirmation explicite du gestionnaire
avant chaque séquence d'envoi : pack mail/SMS validé ensemble, rappel et correctifs
validés séparément. Les échéances seules ne provoquent plus d'envoi.
La spécification V1.2 couvre ses extensions `E66-PWA-20260929` (PWA/menu ERP),
`E66-PRIX-20260929` (prix proposé modifiable) et `E66-EXPERIENCE-20260929`
(expérience multi-prestations, sans coffret matériel). Elles sont implémentées et
testées localement ; la recette du parcours et de la PWA est confirmée par l'utilisateur.
Les réserves techniques de préparation de livraison restent explicites dans le bilan.
La nouvelle [EPIC 69](terminees/epic-69-profils-acces-erp-satellites-backlog.md)
porte les accès ERP et satellites, terminée le 2 octobre 2026 :
trois rôles métier retenus, Lecteur, Backoffice et Finance, avec cumul explicite
Backoffice + Finance ; admin historique conservé, SQLAdmin et commandes d'argent
réservés à celui-ci, protection des satellites Support/Atelier.
Ses 27 critères incluent la création d'un utilisateur par l'admin et l'invitation
email pour initialiser le mot de passe. La [V1.4 — scopes globaux](../specifications/epic-69-acces-internes/README.md)
du 2 octobre applique les profils à toutes les communes, sans contexte territorial.
Elle conserve les décisions : invitation 24 h, récupération admin, matrice fixe, Finance via Support,
BUM/activation à zéro/annulation impayée non active ouvertes à Backoffice. L'audit
documentaire du 2 octobre distingue les commits V1.3 backend/projet poussés du
déploiement ; écarts UI, révision du bundle et recette cible restent dans le
[bilan](../specifications/epic-69-acces-internes/verification-livraison.md). L'EPIC 35 conserve sa clôture
historique ; son ancien cadrage complémentaire est transféré à E69 sur demande utilisateur.
La revue finale du 2 octobre clôture E69 après correction de **CA-18** :
37 scénarios de traçabilité réussis, preuves inchangées réutilisées, guide et
bundle ERP vérifiés. Lots de commit et prérequis de livraison consignés dans le
bilan ; la clôture n'atteste ni publication du correctif ni déploiement.
La nouvelle [EPIC 70](en-cours/epic-70-validation-prestation-telephone-client-backlog.md)
cadre une validation entièrement sur téléphone client, sans matériel dédié imposé.
Le PIN dédié est retenu avec un compromis de droits limités : contexte transactionnel,
gestion du PIN depuis l'accès commerçant et parcours client. Ses 34 critères couvrent
validité, révocation, concurrence, incidents et absence d'accès professionnel.

Le 5 octobre, l'[EPIC 72 — Accès salariés Localeo Pro](en-cours/epic-72-acces-salaries-validation-localeo-pro-backlog.md)
ajoute l'invitation email, le compte individuel limité au scanner Coffret/Animation,
la révocation et l'audit : 22 critères, historique complet du commerce en lecture seule, option ERP désactivée par défaut et sans plafond. L'EPIC 70 est
étendue aux passages Animation et aux pannes du mobile commerçant : 34 critères,
PIN automatique valable 7 jours par défaut, configurable jusqu’à 30 jours, notification Localeo Pro à chaque succès. E70 est en cours depuis le 7 octobre ; E72 est également en cours.

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
| 65 | Terminee | Trois vues ERP et projections partagées, dix critères vérifiés le 2 octobre ; scopes E69 intégrés, 691 tests et parcours navigateur réussis. Configuration et recette cible dans le bilan, aucun déploiement implicite. |
| 66 | Terminee | [Localeo Atelier](terminees/epic-66-localeo-atelier-coffrets-assistes-ia-backlog.md) : [V1.2](../specifications/epic-66-localeo-atelier/README.md) implémentée et testée ; clôture produit le 1er octobre après confirmation utilisateur du parcours et de la PWA, réserves de livraison conservées dans le bilan. |
| 67 | A faire | [Communautés de communes](a-faire/epic-67-communautes-communes-coffrets-intercommunaux-backlog.md) : référentiel, coffrets intercommunaux, commercialisation et extension de Localeo Atelier ; droits et achats existants préservés. |
| 68 | En cours | [Processus d'onboarding commerçant](en-cours/epic-68-parcours-commercant-preparation-onboarding-backlog.md) : V1.2 implémentée localement, sept étapes du référencement à la finalisation ; envois confirmés, espace sans dépôt, signature jour J puis dépôt interne. Paramètres validés ; livraison test, approbation des supports et recette cible suivies dans le bilan. |
| 61 | Fusionnee | Contenu repris dans l'Epic 60 ; une fusion n'est pas un abandon. |
| 35 | Terminee (historique) | Clôture conservée ; le cadrage non livré des nouveaux rôles est transféré à l'EPIC 69 sur demande explicite du 1er octobre. |
| 69 | Terminee | [Profils et accès ERP/satellites](terminees/epic-69-profils-acces-erp-satellites-backlog.md) : clôture le 2 octobre après validation CA-18, 27 critères conservés ; recette cible et configuration dans le bilan. |
| 70 | En cours | [Validation sur téléphone client](en-cours/epic-70-validation-prestation-telephone-client-backlog.md) : PIN dédié retenu, 34 critères ; contexte transactionnel, gestion commerçant du PIN et parcours client sans matériel ; risque résiduel borné par les droits, validité et révocation. |
| 72 | En cours | [Accès salariés Localeo Pro](en-cours/epic-72-acces-salaries-validation-localeo-pro-backlog.md) : implémentation locale vérifiée, 22 critères ; option ERP, invitations, scanner et historique limités, conservation. |
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
