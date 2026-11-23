# Workshop UX Localeo Live · carnet rempli · 23 novembre 2026

**PARTIEL · exploration, atelier simulé et maquettes terminés.** La validation utilisateur des nouvelles maquettes est attendue. Le carnet rempli de TEST constitue la preuve de référence pour les parcours personnels.

| Repère | Valeur |
| --- | --- |
| Date et heure | 23 novembre 2026, Europe/Paris, exploration entre 09 h 00 et 09 h 06 |
| Site et commune | [Localeo Live TEST](https://test-live.localeo.city/) · Bouliac 33270 |
| Dépôt documentaire | `main` · `224870a826bdff3d2c0fe7af3bc62d700f0d4832` |
| Marketplace consulté | `main` · `ccd4ac72432d17a0c39d090d73b14e095d796f84` |
| Dossier | `ateliers/ux-workshops/localeo-live/2026-11-23-02/` |
| Objectif | Rejouer l’atelier à partir du carnet rempli, de ses participations, de ses lots et du programme Bouliac. |

Aucun atelier Live antérieur explicitement terminé n’a été identifié. La [première exécution du 23 novembre](../2026-11-23/README.md), archivée et partielle, sert de référence provisoire. Les décisions qui s’y rapportent concernent ses versions de maquette.

[Demande exacte](prompts/00-demande-utilisateur.txt) · [Accord pour enchaîner jusqu’aux maquettes](prompts/01-accord-enchainement.txt) · [Protocole de référence](prompts/REFERENCE-RELANCE-2026-11-23.md)

## Exploration

L’onglet Chrome déjà ouvert avait accès à 11 participations, dont neuf à Bouliac. Le Passeport de Bouliac tient compte de deux visites validées, un lot libre est à retirer et quatre tirages figurent dans Mes lots. Le lot indique une échéance non précisée et fournit une consigne de test insuffisante pour savoir où se déplacer. La lecture publique distincte a ouvert la fiche du Passeport et a reproduit les consignes d’inscription contradictoires de la tombola.

Les huit captures de session ont été prises aux dimensions CSS indiquées, avec une densité d’image de deux. Les cinq captures Playwright à 390 px proviennent d’un profil vierge. Deux captures de lot comportent un masque localisé sur le nom du responsable. [Captures AVANT](visuels/captures-avant/)

| Livrable | Objet |
| --- | --- |
| [Cartographie](observations/cartographie-parcours.md) | Parcours publics et personnels rejoués. |
| [Inventaire](observations/inventaire-ecrans.md) | Écrans, preuves et composants. |
| [Observations](observations/observations-factuelles.md) | Constats, conséquences et hypothèses. |
| [Limites](observations/limitations.md) | Accès, transitions et usages encore à éprouver. |

## Workshop simulé

Six ateliers, douze rôles fictifs, quatorze propositions et 168 votes nominatifs. Sept orientations adoptées, dont cinq P1 et deux P2. Sept rejetées. Aucun P0 établi. Le **NO GO simulé à 10 000 habitants** concerne un lancement immédiat, en l’absence de preuves positives complètes du QR et du retrait, et avec des consignes publiques à clarifier.

[Rapport exécutif](workshop/rapport-executif.md) · [Compte rendu](workshop/compte-rendu.md) · [Registre](workshop/votes-et-arbitrages.md) · [Backlog](workshop/backlog-ux.md) · [Options rejetées](workshop/orientations-rejetees.md) · [Actions à faible effort](workshop/quick-wins.md) · [Comparaison avec la première exécution](synthese/comparaison-precedent.md)

## Nouvelles maquettes

Quatorze états illustrent les cinq P1 B1, B3, C1, D1 et F1. Le comparatif distingue les AVANT réels, les preuves de contexte et les états manquants. C1 et F1 sont maintenant comparés à un lot réellement attribué et à un Passeport personnel qualifié. La revue des douze rôles a précisé les libellés, le contact et le trajet de retour depuis un tirage. Les votes restent applicables.

[Ouvrir le comparatif](visuels/comparatif-avant-apres.html) · [Référence des états](visuels/reference-maquettes.md) · [Revue simulée](visuels/revue-contradictoire.md) · [Contrôles](visuels/controle-maquettes.md)

Les changements sont documentaires et confinés à ce dossier de `localeo-projet`. Les guides Commerçant et Animation sont sans impact. L’accord reçu couvre l’enchaînement jusqu’aux maquettes. La décision sur les cinq nouvelles propositions relève de la validation suivante.
