# E74 — Preuves attendues et recette

Version du 3 novembre 2026. [Périmètre](README.md), [contrats et invariants](architecture-contrats.md), [critères canoniques](../../roadmap/a-faire/epic-74-tombola-publique-backlog.md).

**Tous les tests métier ci-dessous sont prévus, non exécutés.** L'exploration du code et la validation des liens ne prouvent pas E74. Les noms `test_*tombola_publique*` et scénarios `e74-*` désignent des fichiers à créer lors de l'implémentation. Conserver les résultats réels, commandes, SHAs de base et artefacts dans ce document au fil de la réalisation.

## Matrice des 16 critères

Chaque ligne doit disposer de preuves comportementales avant clôture. U = domaine unitaire ; I = intégration application/API/PostgreSQL ; F = parcours fonctionnel navigateur avec transport e-mail de test.

| Critère | Comportement et propriétaire | Preuves prévues — résultat actuel | Documentation / contrat | Démonstration / fixtures | Exploitation / livraison |
| --- | --- | --- | --- | --- | --- |
| E74-CA-01 | Catalogue et droits : standard inclus, modèle identifié | U/I catalogue sur souscription nouvelle et déjà active, sans module payant ; F choisir modèle. **Non exécuté** | Catalogue, capacités, guide Animation | Souscription standard avec/sans crédit | Modèle inactif avant consommateurs compatibles |
| E74-CA-02 | Abonnements : quota consommé une fois | U/I publication répétée, concurrente, quota épuisé, droit expiré, rollback et conditions acquises ; **non exécuté** | Publication et quota E73 | Crédits dernier/disponible/épuisé | Audit consommation, aucun changement tarifaire |
| E74-CA-03 | Publication autonome, dotation externe | U/I création et publication sans commerce, refus dates/règlement/lots invalides ; F sans mission ni paiement Coffrets. **Non exécuté** | Modèle compilé et politiques de publication | Organisation avec zéro commerce | Snapshot vide distinct d'absent |
| E74-CA-04 | Assistant et périmètres | U/I capacité non applicable, refus autre organisation/commune via ERP et API ; F étapes lisibles. **Non exécuté** | Assistant et accès | Deux organisations et communes | Refus 403 auditables, pas de données étrangères |
| E74-CA-05 | QR public sans secret personnel | I contenu URL/support, GET sans mutation ; F scan et lien sur mobile/autre appareil. **Non exécuté** | QR, route Live, source de diffusion | QR d'une animation publiée | Domaine existant, fallback et cache PWA |
| E74-CA-06 | Flyer adapté | U/I données et quantités par mode ; F/PDF rendu sans commerce/achat, image fournie ou absente. **Non exécuté** | Flyer contextualisé E73, guide stand | Trois dotations, deux états d'image | Reprise génération sans document incohérent |
| E74-CA-07 | Domaine : preuve d'e-mail avant une chance | U/I attente puis confirmation, ancien endpoint refusé, aucun PIN/scan qualificatif ; F prénom/e-mail seulement et retour Live. **Non exécuté** | Identité minimale, challenge, inscription | Attente, confirmé, transport e-mail local | Outbox atomique, taux de confirmation |
| E74-CA-08 | Identité et idempotence | I doubleclic, deux clés même e-mail, clés incompatibles, réponse perdue, secret consommé, récupération ; F reprise sans doublon. **Non exécuté** | Reçus et récupération | Variantes casse/espaces, mêmes e-mails entre tombolas | Pas de fuite ni chance supplémentaire |
| E74-CA-09 | Temps et cycle de vie | U horloge avant/début/fin/après ; I confirmation/clôture concurrentes, annulation, lien expiré/remplacé ; F refus clair. **Non exécuté** | Fenêtre et codes de refus | Animations futures, ouvertes, fermées, annulées | Horloge serveur et gel traçable |
| E74-CA-10 | Participation indépendante du suivi | U/I aucune préférence positive déduite ; F refuser suivi et notifications puis participer. **Non exécuté** | Séparation des préférences | Participant sans aucun opt-in | Aucun message inter-animations ajouté |
| E74-CA-11 | Suivi commune existant, facultatif | F ajouter/retirer, limite dix, stockage absent, autre appareil ; I préférences d'installation si présentes. **Non exécuté** | Mes communes, portée navigateur | Communes suivies et non suivies | Aucune nouvelle campagne/clé d'envoi ; participation conservée |
| E74-CA-12 | Exploitation : liste bornée et gel prouvé | I filtres/curseurs/totaux exacts N/10N, non-inflation par attentes, audit/provenance et gel concurrent. **Non exécuté** | Pagination et compteurs | Attentes, qualifiés, anonymisés, données inter-tenant | Index/plans/volumétrie ; pas de collecte `All` |
| E74-CA-13 | Tirages existants selon mode | U/I zéro, moins/égal/plus de candidats, suppléants, résultat rejoué, opération relancée ; F confirmation explicite et refus Coffrets. **Non exécuté** | Protocole tirage et dotation gelée | Trois dotations × tailles de population | Aucun double gain ; reprise durable et diagnostic |
| E74-CA-14 | Gains, notifications, remises | I/F Coffret, bon consommé, libre remis, envoi échoué/repris ; Live lots à retirer avant historique. **Non exécuté** | Contrats E73 gains/remise et Live récompenses | Gagnants, suppléants, trois états de remise | Envoi ≠ livraison ≠ remise ; externes sans commerce |
| E74-CA-15 | Droits, secret, abus et capacité | I autre participant/animation/tenant, ancienne récupération, secrets absents des logs, 429 et rafale réseau partagé ; F clavier/mobile. **Non exécuté** | Erreurs, capacités, bornes, notice données | Transport faux, limiter/horloge déterministes | Budgets p95/p99, contention, purges et audit |
| E74-CA-16 | Compatibilité et démonstration | U/I/F anciens trois moteurs, migrations sans conversion, anciens clients et PWA, démonstration rejouée ; **non exécuté** | Manifestes, schémas et exports empreintés | Données historiques et E74 séparées | Montée de schéma, restauration isolée, activation distincte |

## Suites à produire et suites existantes à étendre

Dans le backend, suivre le runner isolé décrit par son `AGENTS.md`. La recette ne dépend d'aucun compte réel, base TEST partagée, fournisseur e-mail ou validation de pilote.

| Dépôt | Fichiers/scénarios ciblés |
| --- | --- |
| Backend — nouveaux | `tests/domain/animation_locale/test_tombola_publique.py` : compilation, identité, qualification et refus ; `tests/application/services/test_tombola_publique_email.py` : transactions/outbox/reçus ; `tests/api/test_tombola_publique_email.py` : contrats et anti-contournement ; `tests/security/test_tombola_publique_postgres.py` : contraintes, gel et concurrence. |
| Backend — existants | `tests/domain/animation_locale/test_tombola_locale.py`, `test_politique_participation_publication.py` ; `tests/application/services/test_participants_animation.py` ; `tests/api/test_localeo_live_animations_inscription.py` ; `tests/security/test_publication_classique_t4.py`, `test_exploitation_moteur_postgres.py`, `test_tirages_libres_postgres.py`, `test_tirages_numeriques_postgres.py`. |
| Animation | Tests existants `animation-engine-registry.test.mjs`, `assistant-presentation.test.mjs`, `assistant-navigation.test.mjs`, `publication-http-contracts.test.mjs`, `flyer-http-contracts.test.mjs` ; nouveau scénario navigateur `e74-tombola-publique` couvrant création → publication → QR → participants → tirage/remise. |
| Marketplace/Live | Tests registre, installation, jeu, communes ; scénarios existants `live-registration-clarity.spec.cjs`, `live-game.spec.cjs`, `live-lots-unified.spec.cjs`, `live-habitant-communes.spec.cjs`, `organizer-messages.spec.cjs` ; nouveau `e74-tombola-email.spec.cjs`. |
| Commerçant/Pro | Remise de bon numérique E74, refus d'une qualification par scan/PIN et non-régression des validations commerçantes des autres modèles. Pas de nouveau flux d'inscription Pro à tester. |
| Projet / contrats | Liens de documentation, exports depuis producteurs, empreintes schémas et contrats embarqués ; ces contrôles accompagnent les tests consommateurs et ne les remplacent pas. |

## Parcours fonctionnels complets

1. **Sans commerce, bout en bout** : organisation de test sans commerce → standard → lots externes → assistant → publication → flyer/QR → prénom/e-mail/règlement → attente sans chance → e-mail capturé localement → ouverture sans mutation → confirmation explicite → une chance → clôture → tirage confirmé → lot visible dans Live → remise par organisateur. Vérifier toutes les identités et versions entre écrans et base.
2. **Reprise et autre appareil** : demander sur A, ouvrir sur B sans installation connue, confirmer, perdre la réponse puis rejouer même commande ; un participant/une preuve/une chance et un accès valable. Reprendre ensuite sur A par e-mail. Aucun état local n'accorde l'éligibilité.
3. **Secret et prévisualisation** : GET, robot de messagerie et préchargement n'écrivent rien ; secret étranger, expiré, révoqué ou remplacé refusés ; nouvelle clé sur secret consommé sans nouvelle mutation. L'ancien endpoint et la récupération ne donnent pas d'accès en attente. Révocation bloque le reçu de succès.
4. **Clôture en course** : deux transactions réelles PostgreSQL, barrière synchronisée ; inclure une confirmation commise avant gel ou refuser celle passée après. Aucun qualifié absent de la population par course ; aucun lien tardif ne l'étend. Rejouer après arrêt worker.
5. **Trois modes, population insuffisante** : lots externes et numériques avec zéro/un/plusieurs candidats ; Coffrets refuse si exemplaires supérieurs aux candidats, sans émission partielle ni modification de dotation. Nombre exact et cas suffisant vérifiés également.
6. **Mobile et préférences** : 320/390 px et PC, clavier/zoom, commandes accessibles, liens retour et rafraîchissement cohérents ; suivi commune refusé puis ajouté/retiré, notifications refusées, stockage indisponible, limite dix. Participation et lots restent utilisables dans chaque cas.
7. **Compatibilité** : anciennes tombolas/passeports/chasses avant et après migration, ancienne PWA face au catalogue/direct E74, cache et mise à jour ; aucun type inconnu envoyé à un lecteur qui ne le comprend pas sans réponse explicite de mise à jour.
8. **Volumétrie et exploitation** : N/10N selon budgets d'architecture, charge mixte lectures/confirmations/gel, plusieurs habitants sur même IP ; total exact, plans/index, bornes mémoire, délais, saturation explicite. Restaurer une sauvegarde isolée contenant attentes, preuves, outbox et gains, puis reprendre sans doublon.

## Documentation et données à livrer avec le code

- Compléter les guides Animation/ERP avec le parcours sans commerce et l'avertissement Coffrets ; le guide Live avec vérification, récupération et suivi local ; le support stand avec QR/lien et confirmation d'adresse.
- Actualiser les sources de règlement/notice selon les finalités et durées réellement appliquées, sans affirmer une validation juridique obtenue. Leur revue de mise en service reste distincte des tests de clôture.
- Régénérer les contrats depuis le backend, puis mettre à jour les manifestes/schémas embarqués et vérifier empreintes et tests de chaque lecteur.
- Adapter le générateur backend et ses assertions aux états de preuve ; aucun accès réel ou donnée privée dans les fixtures. Vérifier suppression/anonymisation/restauration, pas seulement création des tables.
- Documenter activation, fermeture d'urgence, limitation de débit, échecs d'e-mail, reprise outbox, purge et retour vers l'avant. Décrire les variables effectivement introduites lors du développement avec exemples sans secret ; aucune variable hypothétique à configurer aujourd'hui.

## Bilan de préparation

Les choix produit sont fixés et les responsabilités, contrats cibles, limites existantes et preuves sont identifiés. Les travaux peuvent être implémentés par lots : domaine/données et contrats → consommateurs et UX → intégration/recette/capacité → activation. Le nouveau parcours d'e-mail et la pagination réellement bornée sont du développement requis.

La clôture technique nécessite les preuves pertinentes réussies pour les 16 critères. Une vérification locale ne vaut pas déploiement ; une action pilote ou une preuve externe n'est pas une condition ajoutée à la clôture. À ce stade, **aucune preuve d'exécution métier E74, migration ou activation n'est acquise**.

## Contrôles de spécification du 3 novembre 2026

- Exploration en lecture des producteurs backend et des consommateurs Animation/Live, puis revue indépendante `localeo-contract-reviewer` des trois documents. Les trois écarts relevés (négociation des clients historiques, contrat de pagination, affichage des dates) ont été corrigés et leur résolution confirmée en seconde lecture. Aucun reste concret dans ces points ; cela ne vaut pas test d'implémentation.
- Dépôt documentaire, base `7b3d5e5` et modifications locales E74 : `python scripts/check_guidance.py` avec `--document` pour les trois fichiers de ce dossier, le backlog E74, la roadmap et l'index. Résultat : **99 guides, 1 158 liens locaux, zéro erreur, zéro avertissement**.
- Aucun contrat généré ni entrée de `documentation.exports.json` modifié dans cette phase ; pas de lecteur applicatif à exécuter pour un changement d'export. Les tests domaine/intégration/navigateur, migrations, charge et génération de démonstration restent **non exécutés**.
