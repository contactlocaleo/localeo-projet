# E73 — Vérification, migration et livraison

Version de conception du **17 octobre 2026**, réalisation locale commencée le **18 octobre 2026**. [Dossier](README.md), [architecture](architecture-contrats.md), [critères canoniques](../../roadmap/en-cours/epic-73-animation-et-ou-coffrets-backlog.md). La matrice décrit les preuves attendues ; leur exécution effective et leurs limites sont enregistrées par lot dans le [suivi de réalisation](suivi-implementation.md). Un scénario sans preuve enregistrée reste non exécuté. Un lien vérifié ou une revue documentaire ne valide pas un comportement applicatif.

## 1. Traçabilité des 63 critères

Chaque ligne associe le CA à une preuve observable ; les identifiants `E73-T-*` nomment des scénarios à réaliser, pas des fichiers déjà présents. Les tests de domaine utilisent horloge/faits et ports doubles, les tests transactionnels une base PostgreSQL jetable, les contrats les DTO réels, les parcours navigateur des comptes synthétiques. Les références de documents, fixtures et livraison sont décrites après la matrice.

| Critère | Comportement / propriétaire | Preuve prévue (résultat : non exécuté) | Contrat / guide | Fixture | Livraison |
| --- | --- | --- | --- | --- | --- |
| E73-CA-01 | Cycle Animation seul, `animation_locale` | E73-T-01 : externe et numérique jusqu’à remise sans commande Coffret | D1 | F1/F2 | L2/L4 |
| E73-CA-02 | Coffrets seul, commercialisation/achats | E73-T-02 : acheter et consommer sans souscription ou onboarding Animation | D1/D3 | F3 | L1/L4 |
| E73-CA-03 | Choix explicite, Animation | E73-T-03 : omissions refusées, trois branches affichées sans présélection | D1 | F1/F2/F4 | L2 |
| E73-CA-04 | Publication libre, Animation | E73-T-04 : blocage commun pertinent ; aucun blocage paiement Coffrets | D1 | F1/F2 | L2 |
| E73-CA-05 | Parcours Coffrets acquis | E73-T-05 : commandes/réservation/envois et gains anciens identiques après migration | D1/D4 | F4/F12 | L1/L2 |
| E73-CA-06 | Ordre de lots, Animation | E73-T-06 : quantités multiples, ordre gelé, surplus en fin sans gagnants inventés | D1 | F1/F2 | L2 |
| E73-CA-07 | Tirage et population figée | E73-T-07 : 0/moins/autant de candidats, un lot par participant, suppléants stables au rejeu | D1 | F1/F2 | L2 |
| E73-CA-08 | Gain et communication | E73-T-08 : confirmation puis outbox email, consignes adaptées, aucun objet financier fictif | D1 | F1/F2 | L2 |
| E73-CA-09 | Reprise email | E73-T-09 : échec/timeout après acceptation, gain unique et statut d’envoi distinct de remise | D1 | F2 | L2/L5 |
| E73-CA-10 | Suivi externe / remplacement | E73-T-10 : contact/remise séparés, autorisations, refus avant 14 jours sans refus explicite, retirage explicite | D1 | F1 | L2 |
| E73-CA-11 | Gel de mode, Animation | E73-T-11 : changement contre engagement/publication en deux transactions ; un état final cohérent | D1 | F2/F4 | L2 |
| E73-CA-12 | Classement et forfait | E73-T-12 : passeport/tombola inclus, chasse distincte, variantes sans supplément | D2 | F5 | L3 |
| E73-CA-13 | Inclusion / droit explicite | E73-T-13 : droit inclus valide sans paiement fictif, consommation du bon quota | D2 | F5 | L3 |
| E73-CA-14 | Version catalogue | E73-T-14 : catalogue modifié par admin seulement, période acquise inchangée, renouvellement à confirmer | D2 | F5/F12 | L3 |
| E73-CA-15 | Périmètres ERP, référencement/identité | E73-T-15 : admin/Backoffice dédié autorisés ; principal/salarié/API non habilités refusés | D3 | F3/F4 | L1 |
| E73-CA-16 | Onboarding Animation | E73-T-16 : ouverture sans pièces Coffrets, prérequis Animation manquants explicités | D3 | F1 | L1 |
| E73-CA-17 | Ajout de périmètre | E73-T-17 : champs communs réutilisés, complément requis, ancien périmètre utilisable | D3 | F4 | L1 |
| E73-CA-18 | Communications OnBoard | E73-T-18 : contrats et séquences par périmètre, confirmation d’envoi conservée | D3 | F1/F4 | L1/L5 |
| E73-CA-19 | Navigation et accès directs Pro | E73-T-19 : trois périmètres, menus, appels API et liens profonds cohérents | D3 | F1/F3/F4 | L1/L4 |
| E73-CA-20 | Commerce Animation dans jeu à coffrets | E73-T-20 : accepter/valider passage sans devenir fournisseur Coffrets | D1/D3 | F4 | L1/L2 |
| E73-CA-21 | Scan/PIN/salarié | E73-T-21 : cible par périmètre, histoire autorisée, aucune élévation salarié | D1/D3 | F2/F3/F4 | L1/L2 |
| E73-CA-22 | Retrait et continuité | E73-T-22 : session ouverte, nouvelle action refusée ; seuls engagements préexistants continuent, suspension prioritaire | D3 | F7 | L1/L4 |
| E73-CA-23 | Site Animation | E73-T-23 : découverte/fiche commerce/inscription/Live sans dépendance Coffrets | D3 | F1/F2 | L4 |
| E73-CA-24 | Anciens liens et origines | E73-T-24 : reprise carnet, mêmes identités, QR/email anciens, accepter/refuser Push sans blocage | D3 | F12 | L4 |
| E73-CA-25 | ERP/Support/CRM/Atelier | E73-T-25 : projections typées, sommes sans lots libres, sélection fournisseur filtrée et refus serveur | D3/D4 | F1/F3/F4 | L1/L4 |
| E73-CA-26 | Migration manuelle périmètres | E73-T-26 : non vérifié bloque sa bascule, contrôle concurrent, pas de suggestion/activation automatique | D4 | F12 | L1 |
| E73-CA-27 | Générateur/restauration | E73-T-27 : génération par services normaux, export/restore et refus identiques aux données créées par UI | D4 | Toutes | L5 |
| E73-CA-28 | Pilote et livraison | E73-T-28 : manifeste versions/configuration/preuves, pilote contrôlé avant extension | D4 | F12 | L1–L6 |
| E73-CA-29 | Gestion externe | E73-T-29 : aucun QR ni compte Pro imposé ; non renseigné différent de non remis | D1 | F1 | L2 |
| E73-CA-30 | Modèles/exemplaires | E73-T-30 : quantité exacte, commerçant unique/modèle, snapshots et secrets distincts, création hors commune refusée | D1 | F2 | L2 |
| E73-CA-31 | Affectation exclusive | E73-T-31 : deux animations concurrentes, libération confirmée jamais attribué seulement | D1 | F2 | L2 |
| E73-CA-32 | Attributions et remplaçants | E73-T-32 : concurrence attribution/rejeu/remplacement, ancien bon révoqué et nouvelle validité complète | D1 | F2 | L2 |
| E73-CA-33 | Accès bon et QR | E73-T-33 : durée 1/90/365 et bornes invalides, QR remplacé ancien refusé, renvoi sans nouveau gain | D1 | F2 | L2/L4 |
| E73-CA-34 | Consommation unique | E73-T-34 : course scan/PIN et réponse perdue, une consommation active, acteur PIN = commerce | D1 | F2/F7 | L2 |
| E73-CA-35 | Refus de consommation | E73-T-35 : autre commerce, QR remplacé, PIN bloqué, expiration/révocation/non-attribution, reçu déjà remis | D1 | F2/F7 | L2 |
| E73-CA-36 | Incidents bon | E73-T-36 : prolongations jusqu’au plafond, correction tracée, révocation/remplacement contre scan/PIN | D1 | F2 | L2 |
| E73-CA-37 | Catalogue modules | E73-T-37 : prix/quotas/échéances/permissions visibles, modules officiels et historiques acquis | D2 | F5 | L3 |
| E73-CA-38 | Achat module | E73-T-38 : paiement confirmé/échec/doublon/retour navigateur, droit une fois, prorata et autorisation Achat | D2 | F5 | L3 |
| E73-CA-39 | Cadeau/essai | E73-T-39 : habilitation ERP, motif, durée/quota ajustés, aucune transaction financière fictive | D2 | F5 | L3 |
| E73-CA-40 | Droits cumulés | E73-T-40 : inclus/acheté/offert/essai chevauchants, maximum sans recharge ni suppression du droit acheté | D2 | F5 | L3 |
| E73-CA-41 | Fin commerciale et retrait | E73-T-41 : module/base expiré ou retrait anticipé, opérations engagées bornées, historique conservé | D2/D3 | F7 | L3 |
| E73-CA-42 | Aperçu import | E73-T-42 : XLSX/CSV, mapping, 100/101 lignes, 2 Mo/dépassement, champs obligatoires et conflits email/SIRET | D2 | F6 | L3 |
| E73-CA-43 | Import confirmé | E73-T-43 : lignes valides seulement, droits courant/commune, fiche à vérifier sans accès/invitation, rapport | D2 | F6 | L3 |
| E73-CA-44 | Deltas | E73-T-44 : référence/source/local, cellules vides, email contact ≠ login, changement après aperçu | D2 | F6 | L3 |
| E73-CA-45 | Reprise import | E73-T-45 : crash après ligne réussie, expiration avant/après démarrage, reprise sans doublon ni nouvelle ligne | D2 | F6/F7 | L3 |
| E73-CA-46 | Quota chasse indépendant | E73-T-46 : 5/an, prorata plafond, publication concurrente dernier crédit, E55 prêt/non prêt | D2/D3 | F5/F10 | L3 |
| E73-CA-47 | Module Push et quotas | E73-T-47 : absent/actif/essai, premier mois, reset Paris/DST, dernier crédit concurrent, automatique indépendant | D2 | F8 | L3 |
| E73-CA-48 | Audience/permissions/fréquence | E73-T-48 : quatre groupes, fenêtre +30 jours, Live sans Push, plusieurs appareils/animations, révocation avant démarrage | D2 | F8 | L3/L4 |
| E73-CA-49 | Suivi/reprise Push | E73-T-49 : incertain/partiel, suspension et confirmation, fréquence 3×, alerte regroupée, aucun double dépôt Live | D2 | F8 | L3/L5 |
| E73-CA-50 | Mot de passe oublié | E73-T-50 : connu/inconnu réponse identique, 1 h/usage unique, anciennes sessions révoquées | D3 | F9 | L1 |
| E73-CA-51 | Mot de passe changé | E73-T-51 : identité revérifiée, sessions du seul compte invalidées, reconnexion explicite | D3 | F9 | L1 |
| E73-CA-52 | Organisation et invitations | E73-T-52 : rattachement ERP, 7 jours, renvoi/rejeu, compte existant réutilisé sans droits automatiques | D3 | F9 | L1 |
| E73-CA-53 | Équipe et responsabilité | E73-T-53 : retrait immédiat, tâches, transfert accepté concurrent au départ, récupération assistée | D3 | F9 | L1 |
| E73-CA-54 | Souscription autonome | E73-T-54 : renouvellement avant/après échéance, upgrade/downgrade, arrêt, remboursement concurrent plafonné | D2 | F5 | L3 |
| E73-CA-55 | Facturation | E73-T-55 : permission Achat, nouveaux documents seulement, anciennes pièces identiques, autre tenant refusé | D2 | F5/F9 | L3 |
| E73-CA-56 | Guide première animation | E73-T-56 : trois dotations, prérequis et attentes visibles sans bypass de publication | D3 | F1/F2/F4 | L4 |
| E73-CA-57 | Préparation chasse | E73-T-57 : 5 jours ouvrés, pause complément, alerte retard/relance même demande, validation terrain | D3 | F10 | L4/L5 |
| E73-CA-58 | Aide/support | E73-T-58 : guide/FAQ/échanges, réponse humaine 2 jours ouvrés, notes internes inaccessibles | D3 | F10 | L4 |
| E73-CA-59 | Prochaine édition | E73-T-59 : même commune, nouveau brouillon et sélection, aucune copie participants/gains/accords/QR | D3 | F10 | L4 |
| E73-CA-60 | Mesure de valeur | E73-T-60 : définitions et inconnues, source QR, objectifs gelés, satisfaction 1..5 sans identité affichée | D3 | F10 | L4 |
| E73-CA-61 | Coûts/budgets | E73-T-61 : constaté/estimé/absent, séparation client/interne, seuils 80/100 sans effet commercial | D2 | F11 | L5 |
| E73-CA-62 | Export/fermeture | E73-T-62 : responsable seul, CSV/médias/guide sous 5 jours ouvrés, accès 30 jours, fermeture distincte et continuité | D3 | F11 | L5 |
| E73-CA-63 | Restauration hébergée | E73-T-63 : chronométrage et cohérence, RPO 4 h/RTO 8 h, preuve manquante/échec interdit mise en service | D4 | F12 | L6 |

### Raccordement des preuves locales du lot 04

Ces résultats portent sur la branche **Libre / Externe**. Les branches numériques
des critères partagés restent ouvertes jusqu’au lot 05. Les commandes, mesures,
limites et commits sont consignés dans le [suivi de réalisation](suivi-implementation.md).

| Critères | Preuves exécutées et portée |
| --- | --- |
| CA-01, 03, 04, 11 — branche externe | Domaine `test_configuration_dotation_dedicated.py`, PostgreSQL/HTTP `test_dotation_animation_postgres.py`, parcours navigateur Animation `tests/browser/dotation.mjs` : choix explicite, gel, publication sans paiement Coffrets, droits/tenant et reprise |
| CA-05 | Régressions financement/publication/tirage Coffrets et `test_valider_paiement_commande_lots.py` : paiement tardif après passage Libre à rapprocher, sans émission d’instances Coffrets |
| CA-06 à 10, 29 — branche externe | Domaine `test_attribution_lot_libre_dedicated.py`, PostgreSQL/HTTP `test_tirages_libres_postgres.py`, navigateur organisateur et `external-animation-gain.spec.cjs` : ordre, manque de candidats, un lot par participant, confirmation privée, email distinct de remise, réserve/remplacement/retirage, erreur et reçu |
| CA-07, 32 — limites externes | Mêmes tests PostgreSQL : confirmations concurrentes, remplacement contre remise et correction, reprise stable ; aucune preuve de révocation d’un bon numérique annoncée avant lot 05 |
| CA-08, 09 | Live `test_gains_live_projection_postgres.py`, jeu PostgreSQL, stockage réel IndexedDB et lien gagnant dans le navigateur : gain confirmé seulement, accès privé distinct du jeu, absence de faux QR/Coffret et versions inconnues refusées |
| Conservation / CA-27 partiel | `test_conservation_postgres_t6.py`, `test_demo_dotations_animation.py`, registre de démonstration et migrations locales : besoin d’identité externe et réserve, purge après remise, dotation synthétique par le domaine. La démonstration transverse de tous les lots et sa restauration restent au lot 10 |

Les preuves de volume couvrent 10 000 candidats, 1 000 lignes de lots, les index
réels, une préparation bornée et le coût constant du scellement externe. Elles
ne remplacent ni la charge simultanée transverse du lot 10 ni la recette humaine.

### Raccordement des preuves locales du lot 08

Les preuves ci-dessous complètent les règles commerciales du lot 03. Le
[suivi de réalisation](suivi-implementation.md#lot-08--communication-participants)
consigne les commandes exécutées, résultats, mesures et reprises de tests.

| Critères | Preuves exécutées et portée |
| --- | --- |
| CA-47 | Domaine `test_campagnes_organisateur_dedicated.py`, PostgreSQL `test_campagnes_organisateur_postgres.py` : débit unique au premier dépôt, concurrence du dernier crédit, audience sans destinataire autorisé sans débit, ouverture technique indépendante des notifications automatiques |
| CA-48 | Mêmes suites, `test_messages_organisateur_postgres.py` et navigateur Animation/Live : quatre groupes, préférence explicite, fenêtre publication/+30 jours, contrôle courant de session et autorisation, message Live sans installation Push, liaison personnelle vérifiée et retrait |
| CA-49 | `test_diffusion_messages_organisateur.py`, `test_execution_campagnes_organisateur.py`, `test_sollicitation_postgres_e73.py` et navigateur ERP : baux/reprises, absence de double dépôt, suspension et confirmation, réglage 1/24 h et seuil 3×, alerte regroupée et outbox transactionnelle |
| Performance / frontières | Suites `test_campagnes_organisateur_performance.py`, `test_messages_organisateur_performance.py` et cas volumineux de sollicitation : pages SQL bornées, index réels, audience traitée par lots, dix lecteurs locaux ; contrôles d'architecture et de contrat HTTP |

Ces preuves locales ne constituent pas un envoi fournisseur réel, une recette
humaine ni une capacité démontrée de l'hébergement. La purge transversale, les
gels et la réapplication des règles après restauration restent à vérifier au
lot 10 ; aucune durée supplémentaire n'est introduite pour ce lot.

### Raccordement des preuves locales du lot 09 — vérifié localement

| Critères | Preuves et limites |
| --- | --- |
| CA-23/24 | Site public Animation, fiche commerce, source d'inscription, continuité explicite du carnet et satisfaction Live ; navigateur mobile/bureau et texte agrandi. Origines/DNS et recette hébergée non exécutés |
| CA-56 | `test_assistant_animation_api.py` et `test_assistant_quota_postgres.py` : contrôles propriétaires sans publication, synchronisation de statut ni débit lors d'une lecture ; refus de session et de quota |
| CA-58 | `test_demande_organisation_dedicated.py`, `test_support_organisations_postgres.py`, `test_support_organisations_http_postgres.py`, `epic73-support-organisations.cjs` : deux jours ouvrés, notes privées, droits courants, concurrence, rollback, email unique, reçus et saisie préservée |
| CA-59/60 | Domaine Valorisation, `test_valorisation_animation_postgres.py`, API et navigateur : nouvelle édition sans données personnelles copiées, provenance, objectifs, sources, satisfaction et mesures agrégées ; réconciliation explicite hors GET |
| CA-27, partiel | Migration v276 depuis une base vide, rejeu, atomicité et correspondance aux modèles : trois réussites locales. Générateur/registre : 23 réussites ; démonstration complète, reprise après interruption et restauration : dix réussites, 571,16 s, aucune base partagée. La preuve hébergée et la consolidation de conservation restent au lot 10 |

Les résultats finaux, artefacts et corrections de revue sont consignés dans le
[suivi](suivi-implementation.md). Le [guide des parcours et du support](../../exploitation/exploitation/parcours-plateforme-animation.md)
décrit l'exploitation. Le lot 09 est terminé localement ; les critères du lot 10,
la recette humaine et les vérifications hébergées restent non réalisés. Le lot 10
n'est pas commencé, conformément à la consigne du 19 octobre.

### Documents et guides associés

- **D1** : [dotation et lots](dotation-lots.md) ; actualiser à l’implémentation les parcours organisateur, les supports de gain, l’aide scanner Pro, E70 et les projections Live. Contrats gagnants discriminés et consommation.
- **D2** : [modules, souscriptions, import et communication](modules-souscriptions-import-communication.md) ; guides catalogue/finance ERP, espace « Mes modules », modèles CSV/XLSX, rapports, aide communication et alertes Ops. Contrats commerciaux, imports et campagnes.
- **D3** : [périmètres et parcours SaaS](perimetres-parcours-saas.md) ; guides OnBoard/contrats commerçants, rôles et aide partenaire, support, site Animation, réversibilité. Contrats identités/périmètres/projections et anciennes URL.
- **D4** : [architecture et contrats](architecture-contrats.md), présent plan et [recette générale](../../exploitation/recette/cahier-recette-generale-avant-mep.md) ; registre de conservation et procédures incident, migrations, démonstration, manifeste de livraison.

Ces références identifient les mises à jour futures des documents d’usage. Les guides aujourd’hui utilisés en exploitation ne sont pas réécrits comme si E73 était livrée.

## 2. Données de démonstration et preuves de non-régression

| Fixture | Cas à générer / vérifier |
| --- | --- |
| F1 | Animation seule, dotation externe, plusieurs modèles/quantités, responsable de remise sans compte Pro ; lot non renseigné/remis/refusé et aucun candidat |
| F2 | Animation seule, bons numériques : plusieurs exemplaires, disponible/affecté/attribué/consommé/expiré/révoqué/remplacé, commerce et salarié, gain en échec email |
| F3 | Commerce et client Coffrets seuls ; achat, prestation et règlement existants sans droits Animation |
| F4 | Commerce mixte, jeu à coffrets avec participant commerçant Animation seul ; onboarding complémentaire incomplet |
| F5 | Deux organisations et communes, droits inclus/achetés/offerts/essai/expirés avec chevauchements, conditions catalogue ancienne/nouvelle, factures et remboursements simulés |
| F6 | XLSX/CSV 100 lignes, 101 lignes refusées, fichier trop grand, conflit email partagé/SIRET, cellules vides, correction locale, crash/reprise et delta de version |
| F7 | Périmètre retiré avec bons attribués, jeu publié et prestations vendues ; module expiré ; salarié révoqué et commerce suspendu pour vérifier la priorité des refus |
| F8 | Participants communs à deux animations d’une commune, deux appareils, accord messages sans Push, suivi commune seul exclu, campagnes suspendues/en cours/incertaines |
| F9 | Un compte organisateur dans deux organisations, responsable/gestionnaire/lecteur et permissions distinctes ; invitation remplacée et transfert en attente |
| F10 | Préparation chasse complète/en attente client/en retard/prête, support interne/externe, nouvelle édition, objectifs et données manquantes, avis facultatif |
| F11 | Budget absent/80 %/100 %, coûts estimés/constatés, export prêt/expiré, fermeture avec engagement ouvert puis transfert documenté |
| F12 | Données historiques avec périmètre à revoir manuellement, ancien lien/QR, archives/suppressions/révocations, outbox et paiement en résultat incertain au moment d’une sauvegarde |

Le générateur reste dans le backend : [instructions locales](../../../../localeo-backend/scripts/demonstration/AGENTS.md), [générateur](../../../../localeo-backend/scripts/demonstration/generator.py), [registre des tables](../../../../localeo-backend/scripts/demonstration/table_registry.json), [schéma](../../../../localeo-backend/scripts/demonstration/schema.py), [archive](../../../../localeo-backend/scripts/demonstration/archive.py). Mettre à jour création, découverte des dépendances, inventaire, export des accès et restauration ensemble. Ajouter les nouvelles tables au registre avec leurs relations/ordre ; un schéma inconnu doit être signalé plutôt qu’omis de l’archive.

Le code actuel capture un schéma et ses migrations puis vérifie des empreintes de tables/lignes/séquences à la restauration ; conserver ces contrôles et couvrir aussi objets, QR/invitations et effets externes E73. Les profils synthétiques ne doivent pas contenir de comptes réels ; artefacts, accès, secrets et fichiers d’import restent dans le répertoire privé opérateur, pas dans ce dépôt documentaire. Aucun mode démo, contournement de droit ou donnée fictive financière dans `app/` pour faciliter le scénario.

Régressions obligatoires : E46 achat lots, E47 souscriptions, E55 moteur/publication/gel, E56 participation, E68 onboarding et confirmation des communications, E70 PIN/coffrets/passages/conservation, E72 salariés/scan/historique. Étendre les tests pertinents existants au lieu de prétendre que leur ancien succès couvre les nouveaux types. Les jobs PostgreSQL doivent réellement s’exécuter : un skip ne prouve ni contrainte d’unicité ni ordre de verrouillage.

## 3. Lots de réalisation et dépendances

Les neuf regroupements du backlog restent dans l’epic ; les jalons L1 à L6 ci-dessous organisent les dépendances techniques, sans promettre une livraison partielle du pivot complet.

| Jalon | Contenu | Conditions de passage |
| --- | --- | --- |
| L1 — Accès et données de base | Identité/appartenance, périmètres/prérequis, revue manuelle, filtres métier ERP/Pro/Atelier, lecture typée | Migration additive prouvée, isolation et droits contrôlés dès la requête suivante ; accès historiques conservés |
| L2 — Dotation et remise | Choix de mode, modèles/stock, gains libres, QR/PIN, incidents, Live/email | Tous les lecteurs savent distinguer les cibles ; concurrence et régressions Coffrets démontrées |
| L3 — Droits commerciaux | Conditions figées/catalogue, commandes et modules, quotas, import, chasse, campagnes | Permissions L1, souscription et paiements réconciliés ; aucun achat proposé pour une capacité non disponible |
| L4 — Parcours SaaS et site | Équipe/portail, facturation, assistant, accompagnement, support, réemploi/bilans, origine Animation | Modules utiles prêts, contrats et liens anciens vérifiés ; DNS/TLS/SW/cookies testés sur la cible |
| L5 — Exploitabilité | Exports/fermeture, conservation, coûts, alertes, documentation et générateur | Classes de conservation mappées, rapports exploitables, démonstration restaurable, transport simulé dans les tests |
| L6 — Pilote et reprise | Sauvegarde/restauration, recette réelle pilote, extension progressive | Preuves de CA-28/63, responsable de bascule identifié ; aucun commerce non vérifié basculé |

La chasse reste dépendante de la readiness E55, indépendamment du module payé ; refuser ou différer l’achat si le service ne peut pas être fourni, expliquer le diagnostic et utiliser une réconciliation support pour une commande déjà confirmée. Cette spécification ne clôture pas E55, E68, E70 ou E72.

## 4. Séquence de migration et d’ouverture

1. Épingler les SHAs des cinq dépôts, l’empreinte des contrats et l’état des travaux locaux. Préparer le pilote **Martignas-sur-Jalle**, choisi le 18 octobre, après validation interne Localeo ; désigner le responsable technique et le responsable de vérification métier, inventorier les engagements et sources de sauvegarde.
2. Sur copie jetable, tester les migrations additives avec [l’outil standard](../../../../localeo-backend/scripts/database/apply_migrations.py) ; aucune modification d’un SQL déjà appliqué. Vérifier interruption/reprise et checksums. La [procédure schéma](../../exploitation/technique/deployer-et-verifier-schema.md) demeure l’entrée opératoire.
3. Préparer les instantanés commerciaux et appartenances à partir des faits, signaler ambiguïtés ; faire saisir les périmètres commerce manuellement dans l’ERP. Pas de proposition automatique. Capturer les engagements autorisés à continuer sans élargir les rôles.
4. Déployer backend compatible en lecture, contrôles de readiness et workers comprenant les nouveaux types. Conserver fermées les nouvelles écritures/modules non vérifiés, sans couper les parcours historiques par un flag global.
5. Livrer les lecteurs Animation, Pro, Marketplace/Live et ERP, leurs contrats embarqués et emails typés. Les versions anciennes/PWA en cache ne doivent pas pouvoir confirmer un nouveau type qu’elles ne savent pas présenter ; proposer mise à jour ou erreur explicite.
6. Vérifier les paramètres non secrets : URL publique Animation et URL Live canonique, allowlists origines/CORS/CSP, cookies/session/SW, comptes fournisseurs de test, clés QR/PIN et rotations, plafonds import, calendrier de service, destinataires Ops, cadence des jobs et échéances. Réutiliser les clés existantes lorsqu’elles ont le même objectif ; nommer les nouveaux réglages lors de l’implémentation, aucun secret dans les docs.
7. Exécuter l’exercice de restauration §5 et la recette pilote sur données contrôlées. Ouvrir seulement les capacités livrées et vérifiées de la commune validée ; publier un rapport de bascule avec refus observés et conditions de retour. Étendre commune par commune sur le même contrôle.

Retour arrière : distinguer rollback binaire avant données nouvelles et correction compatible après usage. Après émission d’un bon ou droit module, ne pas effacer tables, attributions ou paiements pour revenir à l’ancienne version. Suspendre les nouvelles commandes touchées, garder les engagements lisibles et honorables dans le service compatible, réconcilier puis corriger. Un incident sécurité peut exiger une suspension plus forte, explicite et auditée ; la continuité commerciale n’est pas un contournement.

## 5. Exercice de reprise — CA-63

**Responsable : équipe technique Localeo.** Avant mise en service, puis chaque trimestre et après modification majeure du dispositif de sauvegarde/restauration. RPO **4 heures maximum**, RTO **8 heures maximum** ; ces valeurs sont des objectifs à démontrer, pas des garanties d’exploitation déjà vérifiées.

Périmètre cohérent : base et journal nécessaire au point de reprise, objets DAM/documentaires/private imports/export encore requis, configuration/version du code, références et accès aux secrets gérés séparément, habilitations/révocations/suppressions, état des tâches/outbox, idempotence et rapprochement des fournisseurs. Une sauvegarde base seule ne suffit pas si les documents ou clés nécessaires ne sont plus accessibles. L’exercice utilise un environnement isolé représentatif, avec interdiction d’envoyer aux vrais destinataires ou de rejouer des paiements réels.

Mesures : `incident_at`, `dernier_instant_restituable_coherent`, `reouverture_parcours_essentiels_at`. La perte mesurée doit être au plus 4 h ; le temps entre l’incident simulé et la réouverture validée doit être au plus 8 h. Inclure la préparation, la restauration et les contrôles, pas seulement la durée de `pg_restore`. Documenter l’hypothèse de détection et l’écart éventuel plutôt que déplacer le départ du chronomètre après le diagnostic.

Procédure d’exercice :

1. Définir le scénario de panne, sauvegarde choisie, volume représentatif, dernière transaction témoin et état des objets ; relever heures UTC et versions.
2. Restaurer sur cible vierge isolée, contrôler empreintes, relations, schéma/migrations et droits. Réappliquer les suppressions et révocations dues avant ouverture.
3. Maintenir les envois et tâches automatiques fermés pendant le rapprochement des effets externes. Pour paiement, message ou remise dont le résultat est incertain dans la fenêtre perdue, retrouver les preuves/IDs externes ou mettre la cible en attente de traitement ; ne pas autoriser une répétition aveugle au motif du RPO accepté.
4. Jouer accès/responsable/salarié, participation, lot externe, scan/PIN, bons corrigés/révoqués, droits module expirés et imports/campagnes partiels. Vérifier qu’un ancien accès révoqué et un ancien QR remplacé restent refusés.
5. Réouvrir les parcours essentiels sur la cible d’exercice après cohérence démontrée, reprendre les jobs sans duplication, mesurer RPO/RTO et consigner résultats des [DR-001 à DR-008](../../exploitation/recette/cahier-recette-generale-avant-mep.md).
6. Archiver rapport daté : environnement/versions, sauvegardes/objets, durées, échantillons rapprochés, refus, incertitudes, opérateurs, écarts et correction. Preuve absente ou objectif manqué : **mise en service concernée bloquée**, exercice à refaire après correction.

Une restauration locale éphémère de démonstration est une preuve utile de cohérence de l’outillage, pas la preuve hébergée de ce critère. Aucun exercice distant n’est exécuté par la rédaction de ce dossier.

## 6. Contrôles et bilan de cette spécification

### Preuves UX et accessibilité attendues

Exigence transverse du 18 octobre, détaillée dans les [parcours SaaS, section 5](perimetres-parcours-saas.md), applicable à US23/29 et aux parcours de gestion des lots, imports, campagnes et souscriptions. Les critères métier restent inchangés ; ces preuves complètent leur recette.

| ID | Parcours / preuve | Résultat attendu |
| --- | --- | --- |
| E73-UX-01 | Organisateur débutant : liste → création → brouillon → contrôle de publication, trois dotations | Contexte commune visible, prochaine action compréhensible, étapes et blocages expliqués ; retour à la liste conserve filtres/page, aucune réussite anticipée |
| E73-UX-02 | Visiteur : accueil public → animation → participation → retour Live | Compréhension dates/lieu/règles et action principale ; découverte sans compte, accès participant distinct de l’accès gestionnaire ; aucun détour imposé par Coffrets |
| E73-UX-03 | Import en conflit, campagne en attente, tirage `202`, réponse perdue et refus de droit | États lisibles et annoncés, saisie conservée, reprise de la même opération, action de résolution ou aide accessible ; aucune répétition involontaire d’un effet |
| E73-UX-04 | Clavier et lecteur d’écran sur les deux parcours, menus, formulaires et fenêtres | Noms et structure compréhensibles, focus visible/ordonné/restauré, aucune impasse ; erreurs et résultats annoncés, sens indépendant des couleurs |
| E73-UX-05 | Mobile 320 pixels CSS, texte 200 %, contrastes, réduction des animations | Informations et actions conservées, absence de débordement global ; contrôles tactiles et critères de contraste de conception vérifiés |
| E73-UX-06 | Essai des deux parcours par des personnes peu familières de Localeo, plus audit automatisé | Compte rendu des réussites, erreurs et hésitations ; obstacles essentiels corrigés avant généralisation. Un audit automatisé seul ne vaut pas validation de l’accessibilité |

Conserver captures/états, scénario, appareil/navigateur et technologie d’assistance, résultats et corrections dans les preuves de réalisation. Aucun essai utilisateur, recette navigateur ou audit d’accessibilité exécuté lors de cette rédaction.

Organisation de la validation confirmée le 18 octobre : **Localeo en premier**, puis essais avec la **commune pilote de Martignas-sur-Jalle**. La première passe corrige les obstacles internes avant présentation au pilote ; la seconde vérifie la compréhension et l’usage des parcours par les personnes concernées. Consigner les retours et corrections avant extension aux autres communes. Ce choix désigne les étapes de recette, pas une validation déjà obtenue.

### Preuves de performance attendues à l’implémentation

Appliquer [P01 à P08](../../architecture/transverse/performance-volumetrie.md) et la matrice d’accès E73. Ces scénarios complètent les CA, sans changer les tarifs, quotas commerciaux ou règles de tirage. Réutiliser le [banc E59](../epic-59-tests-performance-api/conception-technique.md) et des données synthétiques sur cible jetable ; la présente revue ne lance aucune campagne de charge.

| ID / couverture | Scénario discriminant | Critère observable |
| --- | --- | --- |
| E73-PERF-01 — listes, CA-12/18/20/25/37/53 | Pages 25 et 100, première et curseur profond ; faire croître séparément tenant consulté, tenants étrangers et historique à N/10N ; filtres rares/fréquents et liste vide | Limite effective en SQL et portée d’accès avant limite, enrichissement borné, nombre de requêtes stable, pas d’hydratation proportionnelle au volume global ; plans et buffers conservés |
| E73-PERF-02 — validations, CA-08/10/35/36 | Scan/PIN sous lecture d’historique, grand stock et nombreuses autres communes | Recherche ciblée et droits courants ; aucune double remise, index utile, pas de verrou de commune ou de chargement d’historique complet |
| E73-PERF-03 — campagne et quotas, CA-38/40/47/49 | Audience N/10N, deux campagnes d’une commune, publication simultanée et autres communes, derniers crédits, bail expiré | Premier débit unique, fréquence correcte ; continuation sans mutex de quota ; mémoire bornée, attente de verrous et âge de file mesurés, progression équitable |
| E73-PERF-04 — bilans/coûts, CA-60/61 | Même nombre d’animations affichées, croissance participants/passages/gains/avis ; cache froid/chaud | Totaux par agrégation/projection, détails paginés, pas de N+1 ni lecture complète des enfants ; fraîcheur annoncée et budget interactif tenu |
| E73-PERF-05 — import/jobs, CA-44/45/46 | Import 100 lignes puis nombreuses opérations indépendantes ; ambiguïtés, fichiers compressés, échéances massives, interruption/reprise | Limites 100/2 Mo et décompression/parseur maîtrisés ; rapprochement indexé, jobs bornés, aucun accès automatique ; pas de scan de l’annuaire par ligne ni de claim global |
| E73-PERF-06 — export, CA-62 | N/10N lignes et octets de médias, modifications pendant capture, arrêt capture puis assemblage, responsable retiré | Manifeste cohérent, mémoire et espace temporaire dans leurs budgets, reprise sans mélange d’instantanés ; aucun verrou métier pendant transfert ; archive complète ou échec explicite |
| E73-PERF-07 — tirage, CA-07/32 | Faire varier séparément population, nombre de lots et commerces ; double confirmation et retrait de périmètre | Préparation sans effet publié, réserve exhaustive/unicité, confirmation atomique, mémoire/temps sous verrou mesurés ; aucune troncature pour accélérer |
| E73-PERF-08 — frontend et charge mixte, CA-18/24/53 | Navigation/polling pendant imports, campagnes, exports et tirages, annulation/changement d’organisation | Aucun préchargement de toutes les pages, cache/DOM bornés, appels obsolètes annulés ; p95/p99 interactifs et taux d’erreur dans budgets, saturation explicite puis récupération |

Deux axes distincts : volume N/10N à trafic fixé, puis trafic par paliers à jeu fixé. Les valeurs de N, distribution par tenant, ancienneté, tailles de médias, durée et débit sont inscrits au rapport **avant** chaque campagne ; inclure une commune très active et beaucoup de petites communes. Ne pas tirer une conclusion de capacité d’un jeu minuscule ou d’un cache chaud seul.

Référence de départ confirmée le 18 octobre : **10 communes et 10 000 participants au total**, avec **10 utilisateurs actifs simultanément** pour représenter les connexions annoncées. Exécuter une répartition équilibrée puis une répartition concentrée, en gardant le total fixe. Pour l’axe volumétrie, comparer notamment 10 000 à 100 000 participants synthétiques à concurrence fixe ; pour l’axe trafic, augmenter par paliers au-delà de 10 utilisateurs sur le jeu de référence. Les scénarios notent cadence, temps entre actions, rôles, durée et requêtes/seconde réellement obtenues : connexions simultanées et débit HTTP ne sont pas équivalents. Les paliers supérieurs explorent la marge et la saturation, sans promettre leur prise en charge ni créer un quota commercial.

Budgets initiaux à calibrer : reprendre E59 pour Animation listes/détail (p95 700 ms), bilans (900 ms), ERP listes (1 000 ms), Pro écritures (1 000 ms), Live listes (600 ms), erreurs inattendues inférieures à 0,5 %. Ce sont des objectifs de départ, pas des résultats ni des SLA acquis. Définir aussi p99, mémoire, pool/verrous, débit soutenu et délai des jobs avant leur recette ; le délai de réponse d’acceptation d’un export/tirage ne représente pas son délai de fin. La phase terminale atomique du tirage doit disposer de son budget spécifique.

Archiver par scénario : SHA, migrations/index réellement installés, matériel, statistiques PostgreSQL, SQL/plans, nombre de requêtes/objets hydratés, latences, erreurs, ressources, attentes, débit/âge des files et comparaison. Une page dont le coût suit linéairement le volume global ou un budget dépassé reste un écart à traiter. La croissance linéaire du travail total d’un export/permutation est attendue ; la mémoire et l’impact interactif doivent rester bornés dans l’enveloppe déclarée. Les seuils et performances hébergées ne sont pas vérifiés par les contrôles documentaires.

### Preuves DDD attendues à l’implémentation

La [revue des frontières](architecture-contrats.md) complète les CA existants ; elle n’ajoute pas d’arbitrage produit. Chaque scénario ci-dessous doit distinguer test de règle pure, test d’orchestration et preuve transactionnelle réelle.

| Contrôle | Preuve attendue |
| --- | --- |
| Domaine indépendant | Construire agrégats/valeurs/politiques sans ORM, framework, configuration opérateur, réseau ni horloge implicite ; les contrôles d’import complètent les tests de refus et transitions, sans les remplacer |
| Frontières et adaptateurs | API, ERP et worker passent par les mêmes commandes ; faits interdomaines typés et versions courantes. Un frontend, un job ou un repository ne décide pas lui-même du quota, de la remise ou du périmètre |
| Remboursement | Politique pure du disponible : réservé, confirmé, rejet définitif, résultat inconnu et confirmation rejouée. Deux approbations concurrentes sous PostgreSQL ne dépassent jamais l’encaissement disponible ; réponse fournisseur perdue ne libère pas la réservation et ne retire pas implicitement un droit |
| Campagne volumineuse | Audience cohérente scellée, arrêt/reprise pendant préparation puis après premier message et au milieu du traitement. Aucune émission avant engagement ; quota débité une seule fois, aucun destinataire ajouté, aucune duplication Live et fréquence interanimations respectée |
| Verrous et bail | Deux connexions PostgreSQL font concourir démarrage, reprise et consommation du dernier crédit ; ordre commun conservé, worker au bail périmé refusé, aucun verrou de claim conservé dans la transaction métier |
| Projections et autorité | Tableau de bord volontairement retardé sans effet sur autorisation/quota/remboursement ; compteur de décision et journal atomiques, reconstruction contrôlée, refus sur incohérence |
| Transactions interagrégats | Échec injecté entre débit/publication, attribution/bon, ligne/fiche et message/fréquence : aucun état partiel acquis. Outbox non visible avant commit, livraison après commit reprenable sans recommencer la transition |

Les bornes techniques de capture/lot et les durées de transaction des campagnes seront mesurées à volume représentatif avant activation ; aucune performance n’est prouvée par cette seule conception. Les confirmations de tirage restent soumises à leur atomicité propre et doivent également faire l’objet de mesures de capacité.

À l’implémentation, lancer le [runner isolé backend](../../../../localeo-backend/scripts/validation/test_isolated.py) sur tests domaine/application/API ciblés, puis tests PostgreSQL/concurrence et contrôles d’architecture selon le [guide backend](../../../../localeo-backend/AGENT.md). Les scénarios E73-T-* doivent être rattachés aux fichiers réels dans cette matrice avec commande, SHA/arbre, environnement et résultat. Les contrats générés et consommateurs doivent être contrôlés ensemble. La démonstration utilise le [runner de compatibilité](../../../../localeo-backend/scripts/validation/run_demo_compatibility_tests.py) et ses bases jetables.

Lors de la rédaction initiale de la spécification, seuls les contrôles documentaires et la revue indépendante du [README](README.md) avaient été réalisés ; aucun contrôle applicatif ni déploiement n'avait été exécuté. Les preuves d'implémentation ajoutées depuis sont raccordées par lot ci-dessus et détaillées dans le [suivi de réalisation](suivi-implementation.md). Les exercices hébergés, la recette humaine et les déploiements restent non exécutés. Les travaux préexistants des dépôts voisins et du suivi moteur sont préservés.
