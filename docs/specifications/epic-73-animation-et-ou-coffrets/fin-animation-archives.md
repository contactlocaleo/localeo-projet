# Fin d’animation et archives — E73-EVO-FIN-ARCHIVES

Évolution du 11 novembre 2026. E73 conserve sa clôture historique ; les critères
ci-dessous portent le nouveau comportement demandé et ses preuves propres.
La demande remplace les étapes terminales de présentation « Tirage terminé »,
« Bilan disponible », « Archivée » par une fin explicite, puis un archivage.

## Décisions et parcours

- **Clôturer** ferme inscriptions et validations, fige la population et permet
  le traitement des tirages et des lots. Ce comportement reste conservé.
- **Terminer l’animation** est une commande explicite : chaque lot attribué est
  remis ou son dossier est explicitement clôturé ; les unités sans gagnant sont
  justifiées. Elle passe `CLOTUREE → TERMINEE`, fige la gestion en lecture seule
  et donne accès au bilan. Une animation terminée reste visible dans Live pour
  les personnes inscrites jusqu’à son archivage.
- **Archiver l’animation** passe `TERMINEE → ARCHIVEE`. L’animation disparaît des
  vues de découverte et de Mon carnet. Elle reste consultable, avec son bilan,
  depuis **Animations → Mes archives** dans Localeo Animation. Aucun accès,
  gain acquis, justificatif ni historique n’est supprimé par cet archivage.

L’animation ne se termine ni sur une date, ni sur l’envoi des e-mails, ni sur la
seule confirmation du tirage. Les actions disponibles viennent du backend.
Les opérations de tirage et de remise restent visibles dans leur suivi dédié ;
elles ne sont plus des étapes terminales concurrentes de la timeline du cycle.
Le cycle présente Préparation, Publication, Déroulement, Clôture, Terminée,
Archivée. Une animation `CLOTUREE` reste à l’étape Clôture jusqu’à sa fin explicite.

## Résolution des lots

Le domaine possède la politique de fin et de résolution des dossiers. Les
interfaces présentent ses faits et ses refus ; les routes ne recalculent pas
une seconde éligibilité à la fin.

| Nature | Preuve de traitement | Refus significatif |
| --- | --- | --- |
| Lot externe | Remise déclarée encore effective, ou décision explicite de clôture motivée (refus, abandon, autre motif documenté) | Contact, email envoyé ou simple refus enregistré sans décision de clôture ne suffisent pas |
| Bon numérique | Consommation effective, ou clôture motivée avec révocation du bon par la commande existante dans la même transaction | Expiration seule, email envoyé, révocation sans décision de dossier ne suffisent pas |
| Coffret | Remise/réception explicitement attestée, ou dossier explicitement clôturé avec motif | `ENVOYE` et instance créée ne valent pas attestation de remise |
| Lot sans gagnant | Justification explicite couvrant le nombre exact d’unités publiées non attribuées, à leur version courante | Une absence de ligne sur une page ne prouve pas l’absence de gain |

Les décisions sont datées et attribuées à l’acteur habilité, avec identité du
gain et de l’animation, nature, version et motif. Les gains remplacés restent
historiques ; seule leur attribution courante doit être résolue. Un tirage
initial ou supplémentaire non confirmé bloque la fin. La justification des
unités sans gagnant est agrégée et bornée : aucune matérialisation de milliards
d’unités ni chargement de toutes les lignes en mémoire.

La clôture d’un dossier numérique annonce clairement sa révocation avant la
confirmation ; elle réutilise la règle et l’autorisation de révocation existantes.
La fin ne révoque aucun droit implicitement. La consommation d’un coffret acquis
dans le domaine Coffrets reste indépendante de la gestion de son animation.

La décision explicite de clôturer un dossier arrête, dans la même transaction,
ses intentions d'e-mail de gain encore à préparer ou en échec de préparation.
Les e-mails déjà déposés ne sont ni effacés ni retirés. Le motif du dossier
conserve la décision ; **Terminer** n'annule aucune intention silencieusement.

## Lecture seule, accès et concurrence

Après `TERMINEE` ou `ARCHIVEE`, les commandes de gestion de cette animation
échouent côté serveur : configuration, dotation, tirage/remplacement, suivi et
correction de remise, gestion des bons, messages/actualités, supports et autres
modifications d’exploitation. Les lectures, reçus idempotents et bilan restent
accessibles avec leurs contrôles habituels. La commande distincte d’archivage
reste permise depuis `TERMINEE`. Créer une nouvelle édition produit une nouvelle
animation ; cela ne modifie pas celle qui est figée.

L'exception existante de retrait des coordonnées du contact public est
conservée pour `TERMINEE` et `ARCHIVEE` : dépublication ou effacement seulement,
sans ajout ni remplacement de coordonnées. Les obligations de conservation et
d'effacement conservent leurs parcours et habilitations propres.
Le questionnaire volontaire d'un participant reste disponible après la clôture,
y compris à l'état `TERMINEE`, avec ses accès et versions ; il ne réouvre
aucune action de jeu ou de gestion. L'avis conservé continue d'alimenter le bilan.

Une programmation de communication encore à publier ou une opération asynchrone
de gestion non terminée est un blocage explicite à résoudre avant la fin.
Ni nouvelle publication tardive ni annulation silencieuse ne sont induites par
**Terminer**. Les workers relisent la garde terminale avant toute nouvelle
écriture de gestion et conservent les protections d'idempotence.

Le transport technique d'un message déjà durablement publié avant la fin reste
un effet acquis : Push, courrier et leurs traces peuvent se terminer avec les
contrôles habituels de préférences et d'accès. Un appareil indisponible ne
bloque pas la fin de l'animation. Cela ne permet ni nouveau message ni
modification de l'animation. Les envois de gains qui créent encore un droit
Coffret appartiennent au traitement des lots, à résoudre avant la fin.

Terminer, clôturer un dossier et archiver utilisent version attendue,
confirmation, clé d’idempotence et audit. Une fin concurrente à une remise,
correction, attribution ou publication est sérialisée par la coordination et
le verrou Animation existants ; la garde est relue après acquisition. Les
rejeux retournent le reçu acquis sans nouvel effet. Un refus ne produit ni
changement partiel de statut ni révocation partielle.

## Contrats et données

Le producteur est `ServiceFinAnimation` ; ses contrats Pydantic sont dans
`app/application/animation_locale/contrats_moteur/fin_animation.py`. Les chemins
suivants sont sous `/protected/animation-locale` :

| Méthode et chemin | Entrée et résultat |
| --- | --- |
| `GET /animations/{id}/etat-fin` | `limit` de 1 à 100, défaut 25, et `cursor` opaque lié à l’animation ; retourne l’état, la version Animation, les compteurs exacts, les blocages, les actions autorisées et une page de dossiers |
| `POST /animations/{id}/dossiers-fin/{ref}/decision` | `expected_version`, `version_dossier` opaque, `decision`, `motif` de 5 à 2 000 caractères, `confirmation: true` ; `nombre_unites` exact obligatoire pour la justification agrégée |
| `POST /animations/{id}/terminer` | `expected_version` et `confirmation: true` ; refuse tout dossier non résolu, dotation publiée indisponible, unité non justifiée ou opération de gestion non terminée |
| `POST /animations/{id}/archiver` | `expected_version` et `confirmation: true` ; exige `TERMINEE` |
| `GET /animations/{id}/commandes-fin/{cle}` | Reçu acquis : `200 CONFIRMEE`, `202 EN_COURS` ou `404 COMMANDE_NON_ENREGISTREE` ; aucune nouvelle écriture ni répétition implicite de commande |
| `GET /animations?archives=false` ou `archives=true` | La pagination `page` / `page_size` existante reste conservée ; défaut hors archives, `true` ne retourne que les `ARCHIVEE` |

La lecture de fin retourne `animation_id`, `statut`, `version`, `compteurs`
(`dossiers_non_resolus`, `nombre_unites_sans_gagnant`, `operations_en_cours`),
`blocages` (`code`, `libelle`, `nombre`), `actions_disponibles`, `items`,
`next_cursor` et `has_more`. Chaque dossier possède `ref`, `nature`, `libelle`,
`beneficiaire`, `quantite`, `statut_resolution`, `version_dossier`, ses actions et
la dernière décision applicable à cette version. Les références et versions ne
sont pas reconstruites par l’interface. Le bénéficiaire est une présentation
nom/prénom privée ; aucun e-mail, QR, PIN ou lien personnel n’est ajouté.

Les décisions sont `ATTESTER_REMISE`, `CLOTURER_DOSSIER` et
`JUSTIFIER_NON_ATTRIBUES`. Les capacités sont produites après vérification des
droits, dont `animation:tirer` pour une clôture de bon numérique. L’attestation
Coffret exige une instance effectivement créée et un gain `ENVOYE` ; ce fait ne
remplace pas l’attestation. Le total Coffrets vient des quantités de la
configuration publiée, le total Libre du compteur de sa dotation publiée. Les
unités non attribuées restent un seul dossier agrégé, sans matérialisation par
unité, même pour des totaux supérieurs à deux milliards.

Les trois commandes et la décision portent `Idempotency-Key`, partagent le
registre idempotent existant sous `FIN_ANIMATION:{id}` et retournent
`animation_id`, `statut`, `version`, `operation`, et éventuellement `dossier_ref`.
La même intention rejoue son reçu acquis. Une autre intention doit conserver sa
propre clé ; un conflit ou une version périmée n’est pas rejoué automatiquement.
Chaque décision augmente aussi la version Animation. La coordination exclusive,
puis le verrou Animation, précèdent les faits de résolution et la nouvelle
vérification des habilitations. La révocation numérique et la décision sont
atomiques. Une clôture explicite annule uniquement sa préparation d’e-mail non
encore déposée (`ANNULE_DOSSIER`) ; aucun message déjà déposé n’est retiré.
L’ancienne commande d’archivage en lot sans version/confirmation est refusée avec
`COMMANDE_ARCHIVAGE_VERSIONNEE_REQUISE`.

La migration additive `v309_fin_animation_archives.sql` crée les registres
`animation_decisions_fin_dossier` et `animation_transitions_fin`, avec identité
d’acteur, date, version et unicités ; elle ne convertit aucune ancienne
`CLOTUREE`. Les FK `RESTRICT` protègent les preuves contre une suppression
d’animation. Les décisions sont conservées dans leur historique et ne valent
résolution que pour la version courante du dossier. Les exports d’organisation
ajoutent deux projections explicites et ordonnées, sans JSON métier brut ni
accès personnel. Le registre de démonstration inclut les deux tables pour les
captures et restaurations. Les politiques existantes de conservation des
identités restent distinctes ; l’archivage ne purge aucun de ces registres.

## Critères et preuves

| Critère | Acceptation observable | Preuve à produire |
| --- | --- | --- |
| FA-01 | Clôturer conserve la population figée et permet encore de traiter les lots | Régressions domaine/application de clôture et tirage |
| FA-02 | Un seul dossier non résolu, un tirage en attente ou des unités non justifiées bloquent Terminer | Domaine pur, orchestration et API pour chaque nature, zéro lot et remplacements |
| FA-03 | Attestation et clôture sont explicites, motivées, auditées et refusées hors droits/tenant/version | Tests HTTP/PG, rollback clôture/révocation et rejeu |
| FA-04 | Fin confirmée : statut TERMINEE, bilan lisible et mutations refusées sur API, ERP et workers | Matrice des entrées, concurrence PostgreSQL et garde de domaine |
| FA-05 | Archiver exige TERMINEE, retire l’animation de Live et conserve les lots/droits acquis | Contrats catalogue/tableau privé, Mes lots et régressions Coffrets/Pro |
| FA-06 | Mes archives ouvre une liste paginée et les fiches/bilans en lecture seule | Recette Animation PC/mobile, erreurs, liens directs et clavier |
| FA-07 | Timeline à six étapes, prochaine action concrète et compteurs de blocage visibles | Contrat workflow et recette de chaque état, sans progression inventée |
| FA-08 | Fin/reprise/archivage sont idempotents, sans double effet et sûrs en concurrence | PG jetable : remise, correction, remplacement et workers face à la fin |
| FA-09 | Démonstration, conservation/export/restauration et documentation utilisent le nouveau modèle | Tests générateur et lecteurs ; aucune génération sur environnement réel |

Périmètres : backend/API/ERP/batchs ; Localeo Animation ; Live et Pro pour les
statuts, les refus et la préservation des droits. Les règles financières et
l’utilisation des coffrets autonomes restent dans leur domaine propriétaire.
Aucun déploiement ni réparation de données n’est autorisé par cette spécification.

## Suivi de réalisation

Spécification et implémentation locales établies à partir des deux arbitrages
utilisateur. Les cinq dépôts sont concernés ; aucun déploiement, commit ou push
au titre de cette évolution. Les suites backend, PostgreSQL et interfaces sont vérifiées localement.
La recette sur TEST et une PWA installée ne sont pas revendiquées ; la
compatibilité complète du générateur est consignée ci-dessous.

| Critères | Réalisation et preuves locales |
| --- | --- |
| FA-01/02/03 | Domaine de fin et commandes versionnées/idempotentes ; tests des trois natures de lot, refus, rollback révocation/décision, justifications exactes et dotation incomplète. Tests HTTP et PostgreSQL dans `tests/domain/animation_locale/test_fin_animation.py`, `tests/api/test_fin_animation_api.py`, `tests/security/test_fin_animation_postgres.py` du backend ; 839 tests réussis dans la passe finale incluant architecture, domaine, application et API ; 13 cas PostgreSQL distincts réussis, puis reprise de deux cas droits/dotation réussie. Rapports backend `tmp/fin-animation-verification-finale.txt`, `tmp/fin-animation-pg-livraison.txt` et `tmp/fin-animation-pg-droits-dotation.txt`. Les suites se recouvrent et ne s’additionnent pas. |
| FA-04/08 | Garde commune `gel_gestion_animation.py` sur les entrées existantes ; revue indépendante des verrous et revalidation des habilitations. Suites de gardes 142, 130 et 83 réussites (recouvrantes) ; concurrence PostgreSQL dans les deux ordres entre fin et correction de remise externe, plus double fin idempotente. Aucune course worker PostgreSQL séparée annoncée ; ses refus après verrou sont couverts dans les tests ciblés des services. |
| FA-05 | Live conserve `TERMINEE` et retire `ARCHIVEE` du carnet, sans supprimer les lots. Deux recettes 320/1280 réussies dans le run Marketplace `15-25-29-555Z-g8L0AL`, 23 tests Node incluant les projections du carnet. Lectures catalogue/participant/Pro et annonce figée : 94 tests ciblés, 2 tests PostgreSQL et 5 projections privées réussis après les corrections de revue. |
| FA-06/07 | Animation : `FinAnimationWorkspace`, `AnimationArchives`, statut et six étapes serveur, retour contextuel préservé ; 22 recettes Fin/Archives à 320/1280 et 26 recettes timeline réussies. Rapports `tmp/fin-animation-captures-lQ7ab9/report.json` et `tmp/workflow-timeline-95bLiq/report.json`. Types, lint complet, build isolé et 18 tests Node réussis. Les recettes utilisent une API simulée. |
| FA-09 | Deux tables classées `replace` dans le registre ; recette locale opt-in avec décisions explicites, sans modifier les dix scènes historiques. 85 tests unitaires de démonstration réussis. Recette avec le vrai `ContexteAutoriseAnimation` et commune explicite : 5 nouveaux cas PostgreSQL réussis (quatre scénarios et rollback complet), plus reprise réussie du cas historique, rapport `backend/tmp/demo-fin-recette-pg-final.txt`. Ces fixtures utilisent les métadonnées. Compatibilité avec migrations, génération et restauration : 8 cas réussis au passage complet, puis 2 variantes de changement de schéma réussies en reprise avec un chemin court ; détails et limites ci-dessous. |

Les revues ont fait corriger le total Coffrets, les intentions d'anciens gains,
les capacités des bons, les cibles de prochaine action, le retrait des contacts,
le snapshot des commerces, les lectures de lots après fin et l'annonce de date
restée modifiable depuis l'ERP. Le questionnaire volontaire habitant reste
indépendant du gel de gestion. Pro : 50 tests Vitest du modèle d'animation et des contrats API
réussis sur configuration isolée. Les contrats embarqués sont synchronisés
après les exports canoniques ; aucun résultat local ne prouve la migration TEST.

La pagination PostgreSQL est vérifiée sur 1 000 dossiers : 17 lectures SQL
constantes pour des pages de 1/10/50, sans doublons et sans matérialisation
par unité de lot. Plans et mesures dans `backend/tmp/fin-animation-pg-pagination.txt`.
Ce contrôle ne constitue pas une campagne de charge sur infrastructure hébergée.

### Compatibilité PostgreSQL du générateur

Le passage complet sur PostgreSQL 18, avec migrations jusqu'à v309, a produit
**8 réussites et 2 échecs d'écriture d'archive**, sans skip. Rapport backend
`tmp/fin-demo-detached-a44862b6e6434003af97d25bf3b5e825-proof/results.xml`.
Les deux chemins de checkpoint atteignaient 264 caractères sous Windows ; les
archives originales de 216 caractères étaient bien écrites. Sans modification
des assertions ou des sources produit, la reprise des deux variantes de
`test_demo_reset_schema.py` dans `tmp/dq4d2007ed/` réussit : **2 cas, 0 échec,
0 skip**, sortie 0. Le runner isolé et son contrôle des scénarios requis sont
conservés pour ce module ciblé. Il ne s'agit pas d'un nouveau passage global
des dix cas ; les deux rapports sont nécessaires au bilan.

Les fixtures ont été adaptées au CRM Nouvelle-Aquitaine et vérifient les
contraintes différées avant leur restauration dans une même transaction.
L'intégrité restaurée est comparée sur toutes les données, en attendant
explicitement l'incrément des quatre jetons CRM qui invalide les anciens baux ;
l'empreinte de la sauvegarde source reste identique à l'original. Aucun skip,
retrait d'assertion, mode produit spécial ou désactivation de contrainte.
Les premiers rapports rouges et un passage interrompu par une erreur de
stdout de l'outil sont conservés ; ils ne sont pas comptés comme succès.
Les trois clusters jetables 31475, 31571 et 31572 sont arrêtés ; aucune base
TEST ni aucun fournisseur réel n'ont été utilisés.
