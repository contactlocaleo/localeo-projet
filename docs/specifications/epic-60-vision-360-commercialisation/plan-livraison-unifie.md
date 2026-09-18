# Plan de livraison unifie - Epic 60

> Historique de conception. Etat realise et decisions deleguees : [rapport V1](rapport-developpement-v1.md), [specification detaillee](specifications-fonctionnelles.md), [contrats implementes](contrats-api.md).

## Perimetre et references

L'Epic 60 absorbe l'Epic 61 sur decision utilisateur. Ce plan coordonne les
lots C0-C5 du diagnostic et E0-E5 des parcours ERP, conserves comme reperes.
Il n'ajoute pas de nouvelle epic et ne renumerote aucune story.

- [Backlog unique PRD-561 a PRD-582](../../roadmap/terminees/epic-60-vision-360-commercialisation-backlog.md).
- [Registre unique](registre-arbitrages.md).
- [Conception du diagnostic](conception-technique.md), [API de lecture et reevaluation](contrats-api.md).
- [Analyse des parcours ERP](analyse-parcours-erp.md).
- [Tests et livraison du diagnostic](plan-tests-et-livraison.md).

## Etat de preparation

| Volet | Disponible | A completer |
| --- | --- | --- |
| Diagnostic et alertes | Conception, sept contrats API, plan de tests | Arbitrages residuels, implementation et preuves de recette |
| Ateliers commercant/coffret et navigation | Analyse, 12 stories, propositions UX et arbitrages ERP | Maquettes, permissions d'ecriture, modele d'offre, contrats de commandes et tests detailles |
| Integration | Perimetre et sequencement unifies | Recette transactionnelle de bout en bout et mesures d'usage |

Les API COM360-API-001 a 007 ne couvrent pas la creation et la modification
metier. Leurs nouvelles commandes devront etre concues explicitement, sans
transformer la reevaluation en commande de correction implicite.

## Strategie de livraison retenue en V1

ERP-ARB-07 impose une bascule directe sur les nouveaux parcours, sans maintien
des anciennes interfaces. Les lots ci-dessous sont des unites de conception,
developpement et recette ; ils ne prescrivent pas une coexistence utilisateur.
Inventorier les fonctions a reintegrer, retirer les anciennes interfaces,
mettre a jour les liens et preparer un retour arriere technique du deploiement.
Voir le [cadrage V1](cadrage-v1.md) pour la portee et les points ouverts.

## Sequencement de travail

Iteration 2 : les etapes ci-dessous restent les reperes de couverture. La
premiere recette doit traverser U0-U4 sur un commercant et un coffret, avec
integration Onboard existant, avant harmonisation exhaustive de tous les
menus. Cette priorite, validee dans ERP-ARB-14, ne retire aucun lot.
La [revue produit](revue-produit-iteration-2.md) ajoute les cas critiques a
la recette commune et affine les arbitrages avant conception des commandes.

| Etape | Lots d'origine | Livrable et dependances |
| --- | --- | --- |
| U0 - Cadrage commun | E0 et preparation C0 | Arbitrer offre/prestation, droits, aptitude et menus ; inventorier commandes, consommateurs et ecrans existants |
| U1 - Socle diagnostic | C0-C1 | Domaine canonique, parite publique/paiement, projections, historique et recalcul durable |
| U2 - Pilotage et navigation | C2-C3 et E1 | API, file commercialisation, detail et navigation commune ; traitements menant aux ecrans proprietaires existants |
| U3 - Referencement commercant | E2-E3 | Creation/edition, preparation, aptitude, offre commercant et rattachements ; depend du modele et des permissions valides en U0 |
| U4 - Atelier coffret | E4 et integration C3 | Composition, edition, rentabilite Epic 28, diagnostic Epic 60, controle avant publication |
| U5 - Alertes et suivi complet | C4-C5 et E5 | Control, chronologie, couverture, harmonisation, recette et formation ; finaliser la mesure de performance et d'usage |

Les lots peuvent etre developpes et recettes separement. La recette du
parcours vertical ne clot pas l'epic ; les fonctions utiles du perimetre sont
reintegrees avant la bascule utilisateur unique. Les alertes font partie de
la recette, sans attendre une coexistence d'interfaces qui n'est pas retenue.

## Regles d'integration

- Reutiliser le dossier Onboard, ses capacites et son suivi ; aucune seconde
  source de preparation dans le dossier 360.
- Verifier un etat cible de publication sans exiger que le brouillon soit
  deja vendable ; simuler sans ecriture puis recontroler a la commande atomique.
- Distinguer cloture du dossier, retrait des nouvelles ventes et archivage
  metier ; aucune action ne supprime implicitement les engagements existants.

- Un seul moteur de vendabilite et un seul calcul canonique de rentabilite.
- La file de diagnostic est en lecture avec reevaluation ; les ateliers
  executent des commandes metier autorisees et auditees.
- Toute mutation d'atelier pouvant affecter le diagnostic invalide les
  projections et demande leur reevaluation dans la transaction metier.
- Une simulation non sauvegardee est identifiee comme telle ; le verdict
  courant reste date et lie aux donnees persistees.
- Modifier une offre ou un rattachement respecte les versions et engagements
  des achats existants ; aucune propagation silencieuse aux coffrets vendus.
- L'aptitude commercant, son statut, la vendabilite coffret et sa marge sont
  quatre informations distinctes, sans raccourci de validation entre elles.
- Les droits des liens de traitement sont verifies sur les commandes cibles,
  pas seulement sur la page de diagnostic ou dans le menu.

## Tracabilite et recette globale

| Stories | Couverture |
| --- | --- |
| PRD-561 a PRD-570 | Matrice detaillee du plan de tests diagnostic |
| PRD-571 a PRD-582 | Criteres du backlog ERP et scenarios de l'analyse ; detail technique a completer avec les commandes |
| Parcours integre | Les scenarios ci-dessous lient les deux ensembles sans nouvelle numerotation PRD |

Scenarios d'integration a livrer :

1. Creer un commercant brouillon, reprendre son dossier et son offre, traiter
   les manques puis activer par une action explicite et autorisee.
2. Creer un coffret, rattacher les prestations, ajuster le reversement,
   consulter marge et diagnostic puis publier apres recontrole serveur.
3. Modifier une prestation utilisee : afficher les impacts, respecter les
   versions, invalider les projections et verifier la parite avec le public.
4. Introduire un blocage connu sur un coffret precedemment vendable : alerte
   unique dans le BackOffice/Control, traitement par l'atelier, reevaluation
   puis resolution avec historique conserve.
5. Tester edition concurrente, refus territorial, reprise de brouillon,
   degradation de marge, erreur de source et refus de publication sans effet
   partiel ni contournement par les anciennes routes CRUD.
6. Verifier le retrait des anciennes interfaces, les nouvelles destinations, la navigation par mission et la
   preservation des droits et engagements des achats deja effectues.

La definition de termine globale exige ces scenarios, les deux matrices de
recette, les performances mesurees et l'aide operateur. Les seuils diagnostic
existants restent applicables ; les objectifs de temps de parcours ERP seront
fixes apres une mesure initiale. Aucun test applicatif de la nouvelle epic
n'est declare execute par la seule fusion de ces documents.
