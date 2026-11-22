# Backlog final — neuf corrections compatibles proposées

Deux P1 conditionnels, sept P2 ; aucun P0. Trois classes A conditionnelles (R01/R03/R07), six B ; aucun C/D retenu. R05 est sortie du backlog principal et conservée P3 en annexe : la copie seule n'a pas de gain démontré, et ne corrige pas la population complète. Neuf fiches, aucun remplissage pour revenir à dix.

La [contre-expertise](../contradiction/contre-expertise.md) est intégrée aux minima, tests et limites ci-dessous. Les réserves bloquent l'implémentation tant que ses preuves de compatibilité ne sont pas acquises ; elles ne bloquent pas ce diagnostic. Critères, contrats, migrations et générateur sont inchangés par cet audit. Tous les gains après correction : **NON MESURÉS**, aucune variante optimisée exécutée. Décisions dans [le registre](../validation/decisions.md), champs vides.

| ID | Proposition | Classe | Priorité | Effort |
| --- | --- | --- | --- | --- |
| R01 | Déporter les unités synchrones des handlers async concernés | A conditionnelle | P1 | S |
| R02 | Réutiliser le compteur exact des inscrits dans l'inscription | B | P2 | M |
| R03 | Borner les deux lectures auxiliaires QR/PIN | A conditionnelle | P2 | S |
| R04 | Cibler et paginer les producteurs de notifications | B | P2 | M |
| R06 | Aligner le budget média avec les opérations du stockage | B | P2 | M |
| R07 | Grouper les résumés commerces du passeport | A conditionnelle | P2 | S |
| R08 | Rendre l'onglet gains Coffrets par pages et agrégats | B | P2 | M |
| R09 | Calculer les statistiques Animation depuis des projections ciblées | B | P2 | M |
| R10 | Lier les cycles email/SMS à leur budget et au bail | B | P1 | M |

Efforts relatifs S/M incluant preuves ; aucune estimation jours/euros. A = petit correctif local sous garanties citées ; B = évolution ciblée ; C = refactoring important ; D = incompatible. Les effets d'une correction ne s'additionnent pas arithmétiquement.

## R01 — Déporter les unités synchrones des handlers async concernés

- **Cause / domaines :** RC-01. Domaine et interfaces : PUT /protected/animation-locale/commercants/me/animations/{id}/juste-prix/produit/image ; quatre POST /internal/{emails,sms}/batch/{envoyer,synchroniser-statuts}. Commerçant utilise l'image ; remises ERP partagées avec Live.
- **Source / fonctions :** `app/api/juste_prix_api.py:123–133, illustrer_produit ; app/application/animation_locale/services/juste_prix.py:57–91 ; app/infrastructure/admin/admin.py:12523–12600, quatre handlers ERP`.
- **Mécanisme et conséquence :** SQL/UoW/fournisseur synchrones appelés directement sur le thread de boucle après une lecture async. Une attente de verrou ou fournisseur peut immobiliser les autres requêtes du même event loop.
- **Déclencheur / justification :** Un dépôt image attend une coordination ou un pool occupé ; ou un batch ERP non vide attend son fournisseur pendant une lecture/scan sur le même processus. Pas besoin de supposer une saturation globale.
- **Preuve / mesure :** CONFIRMÉ PAR MESURE locale du mécanisme ERP : p50 témoin 10,657 /53,184 /106,051 ms à1/5/10 coroutines, avec 10 ms injectées, contrôles0,037 /0,141 /0,278 ms. Image fortement étayée, NON MESURÉE.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel élevé sous scénario décrit, probabilité conditionnelle/inconnue en exploitation, criticité P1. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Pour les quatre endpoints ERP sans await, passer à def si routage et contexte sont confirmés ; pour l'image, garder lecture async du corps puis run_in_threadpool de l'unité synchrone complète. Sessions créées/fermées dans leur thread, identité et corrélation conservées.
- **Alternative :** Handler def si le routage/lecture du corps le permet ; conserver réponse, identité et corrélation.
- **Classe / effort :** A conditionnelle / S.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Faible à moyen : contexte de requête, annulation client, sessions. Déconnexion ne signifie pas annulation d'un effet.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** Témoin qui progresse avec adaptateur bloqué ; image valide/invalide, reçu/idempotence, droits et rollback ; quatre 303 et erreurs ERP, corrélation nettoyée, pas de session entre threads. Mesurer aussi attente threadpool/pool.
- **Rollback proposé :** Attendre les unités engagées, revenir au seul déport ; conserver journaux et effets. Aucun renvoi pour compenser une réponse perdue. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R02 — Réutiliser le compteur exact des inscrits dans l'inscription

- **Cause / domaines :** RC-02. Domaine et interfaces : POST /public/animation-locale/animations/{id}/inscriptions hors TOMBOLA_PUBLIQUE ; frontend Marketplace.
- **Source / fonctions :** `app/application/animation_locale/services/participants_animation.py:70/104/127, inscrire ; app/infrastructure/persistence/repositories/animation_locale_repositories.py:1331 ; sql/v283_e73_compteurs_lectures.sql:11–47`.
- **Mécanisme et conséquence :** Comptage exhaustif des inscrits, éventuellement deux fois, pendant la coordination exclusive qui protège identité/capacité. Le verrou est nécessaire ; le recomptage peut être remplacé par un fait exact déjà projeté.
- **Déclencheur / justification :** Arrivées simultanées dans une animation déjà fréquentée ; coût à qualifier N/10N, sans débit plafond annoncé.
- **Preuve / mesure :** NON MESURÉ : SQL, contention, gain et taux d'inscription.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel moyen à élevé selon volume, probabilité conditionnelle/inconnue en exploitation, criticité P2. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Lire le compteur transactionnel exact existant avant insertion et réutiliser ce nombre pour capacité et premier inscrit, après preuve d'équivalence et présence de v283 ; garder la coordination. Absence de groupe=0 seulement si schéma intègre ; N est lu avant insertion : premier inscrit si N==0, et non N==1 après flush. Ne pas utiliser une projection de qualification à sa place.
- **Alternative :** Réutiliser au moins le premier COUNT dans la même transaction ; conserver COUNT si le compteur n'est pas prouvé intègre.
- **Classe / effort :** B / M.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Moyen : une projection de lecture ne devient une entrée de décision qu'après preuve d'exactitude transactionnelle. Le rendu QR RC-03 reste coûteux.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** Insertion/suppression/mise à jour/anonymisation et compteur, zéro/dernier crédit/plafond, deux inscriptions et scan/clôture concurrents, même email/rejeu et premier inscrit. Déploiement de v283 à vérifier, pas appliquer ici. Ajouter transfert d'animation, rollback, cascade/TRUNCATE pertinents et égalité COUNT/compteur ; pas de mutation concurrente hors coordination.
- **Rollback proposé :** Revenir aux COUNT après fin des transactions ; conserver participants/tokens/outbox. Aucun recalcul ou purge imposé. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R03 — Borner les deux lectures auxiliaires QR/PIN

- **Cause / domaines :** RC-04 + RC-05. Domaine et interfaces : POST /protected/animation-locale/validations et canal PIN partageant valider_dans_uow.
- **Source / fonctions :** `app/application/animation_locale/services/validations_animation.py:133–141 ; app/infrastructure/persistence/repositories/animation_locale_repositories.py:1510–1518 ; app/domaine/animation_locale/entities/validation_animation.py:29–31`.
- **Mécanisme et conséquence :** Toutes les preuves de la minute sont hydratées pour len, alors que le domaine décide à 60 ; toutes les annulations du participant sont chargées pour une seule antériorité.
- **Déclencheur / justification :** Nouvelles preuves distinctes d'un commerce en pointe ou historique de corrections croissant ; pas les simples rejeux d'une preuve effective.
- **Preuve / mesure :** FORTEMENT ÉTAYÉ PAR LE CODE ; durée SQL et CPU NON MESURÉES.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel moyen à élevé selon volume, probabilité conditionnelle/inconnue en exploitation, criticité P2. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Port de nombre récent plafonné à 60 sans hydratation/tri ; requête séparée pour l'antériorité participant+commerce+étape annulée, même clé max(coalesce(annulee_at,validated_at),id), LIMIT 1. Deux remèdes explicitement requis. Cadence : commerce toutes animations/tous statuts, validated_at>=now-1min, sans ajouter de borne <=now absente du code. Antériorité : ordre actuel (annulee_at ou validated_at, str(id)) et régularisation seulement si nouvelle preuve VALIDEE.
- **Alternative :** COUNT SQL simple pour cadence, moins d'allocations mais parcourt toutes les entrées ; conserver les index déjà présents avant toute proposition de migration.
- **Classe / effort :** A conditionnelle / S.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Faible à moyen : filtres, seuil et ordre des égalités ; le domaine garde la règle, aucun plafond commercial nouveau.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** 0/59/60/61 et anomalies incluses, bornes temporelles exactes, QR/PIN, annulations multiples/dates égales et référence regularise_validation_id. Plans/SQL sur cible jetable future. Le domaine reste propriétaire du seuil ; ne pas arrêter d'enregistrer les anomalies après60.
- **Rollback proposé :** Revenir aux deux lectures historiques après transactions en cours ; conserver les validations et leurs liens de régularisation. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R04 — Cibler et paginer les producteurs de notifications

- **Cause / domaines :** RC-07. Domaine et interfaces : Publication Animation et résultat tirage Coffrets → notifications privées Live ; ne concerne pas la seule lecture inbox.
- **Source / fonctions :** `app/application/animation_locale/services/notifications_localeo_live.py:43–83/86–109/160–194 ; publication_animation.py:345/372 ; tirages_animation.py:280`.
- **Mécanisme et conséquence :** Installations globales actives puis filtre commune en Python ; résultats chargés puis regroupés par installation et existence vérifiée par destinataire.
- **Déclencheur / justification :** Croissance des installations étrangères avec commune cible fixe ; plusieurs participations d'une installation pour un tirage.
- **Preuve / mesure :** FORTEMENT ÉTAYÉ PAR LE CODE ; charge SQL/mémoire intégrée NON MESURÉE.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel moyen à élevé selon volume, probabilité conditionnelle/inconnue en exploitation, criticité P2. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Ciblage SQL et pages stables d'installations distinctes ; insertion groupée idempotente, agrégation gagnant par installation. Préserver le commit métier et source_key. Préserver les préférences absentes/nulles et OR gagnant entre toutes participations d'une installation ; éviter accumulation ORM pending malgré les pages.
- **Alternative :** Optimiser d'abord la sélection publication ; garder la méthode résultat tant que sa fusion gagnant/déduplication n'est pas prouvée. La pagination peut borner mémoire, pas durée totale de transaction.
- **Classe / effort :** B / M.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Moyen : ciblage, résultat personnel, atomicité et objets ORM accumulés ; ne pas committer partiellement une publication.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** Commune/catégories, installation inactive, deux participations dont un gain, source_key/rejeu/concurrence, rollback de publication/tirage ; N/10N tenants étrangers, mémoire réelle driver+ORM et inserts.
- **Rollback proposé :** Revenir aux producteurs antérieurs après transactions ; conserver notifications déjà committées et leurs clés, aucun renvoi massif. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R06 — Aligner le budget média avec les opérations du stockage

- **Cause / domaines :** RC-10. Domaine et interfaces : GET /public/localeo-live/participations/{id}, avec média sélectionné seulement ; Marketplace LiveAnimationGame.jsx.
- **Source / fonctions :** `app/application/animation_locale/services/contenu_generation.py:368–395 ; app/infrastructure/storage/document_storage.py:83–109 ; jeu_animation.py:459–463`.
- **Mécanisme et conséquence :** Budget monotone testé autour de get/read synchrones sans transmission de budget restant. SDK possède ses propres défauts, pas une absence totale de timeout.
- **Déclencheur / justification :** Stockage S3 lent/trickle/retries ; client Live expire à 15 s pendant que le backend peut encore travailler. Stockage réel déployé inconnu.
- **Preuve / mesure :** FORTEMENT ÉTAYÉ PAR LE CODE ; p95 stockage/HTTP et gain NON MESURÉS.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel moyen à élevé selon volume, probabilité conditionnelle/inconnue en exploitation, criticité P2. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Politique connect/read/retries explicite adaptée au budget restant, fermeture Body et lecture bornée aux octets autorisés. Préserver SHA, provenance et erreurs maîtrisées. Lire au plus taille autorisée+sentinelle et fermer Body en erreur/succès ; budget uniquement dans lecteurs compatibles, adaptateur commun à recetter.
- **Alternative :** Mesurer d'abord local versus S3 ; cache privé borné d'octets validés est un mécanisme RC-11 séparé, ne résout pas la deadline.
- **Classe / effort :** B / M.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Moyen : adaptateur partagé, faux timeouts, retries et dépassement non interruptible ; pas de cache de droit. Une deadline dure demande une conception distincte, aucun abandon de thread présenté comme annulation d'I/O.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** Sans média/local/S3 double rapide/lent/trickle/corrompu, limite octets, fermeture/erreurs, autorisation révoquée et même projection. Read timeout seul n'est pas une échéance dure.
- **Rollback proposé :** Restaurer la politique antérieure pour les lectures suivantes ; conserver stockage/intégrité, ne supprimer aucun objet. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R07 — Grouper les résumés commerces du passeport

- **Cause / domaines :** RC-12. Domaine et interfaces : GET /public/localeo-live/participations/{id}, moteur PASSEPORT_COMMERCANT uniquement.
- **Source / fonctions :** `app/application/animation_locale/services/jeu_animation.py:403–408 ; app/infrastructure/persistence/repositories/repositories_sqlalchemy.py:143–170/184`.
- **Mécanisme et conséquence :** session.get par merchantId pour nom/adresse ; lectures SQL distinctes si identity map froide. Le nombre réel n'est pas compté ici.
- **Déclencheur / justification :** Passeport avec nombreux commerces et actualisations de progression ; dépend de la latence DB et identity map.
- **Preuve / mesure :** FORTEMENT ÉTAYÉ PAR LE CODE ; N+1 potentiel source, nombre SELECT effectif NON MESURÉ.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel moyen à élevé selon volume, probabilité conditionnelle/inconnue en exploitation, criticité P2. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Projection groupée des seules colonnes utiles pour les IDs autorisés, indexer par ID puis reconstruire exactement l'ordre DSL et l'erreur de commerce absent. Traiter les clés par lots si cardinalité importante ; aucun filtre de statut implicite ni énorme IN proclamé borné.
- **Alternative :** Réutiliser lister_resumes(ids=...) existant en vérifiant ses colonnes/adresse et visibilité ; pas de pagination publique ajoutée.
- **Classe / effort :** A conditionnelle / S.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Faible à moyen : ordre, mapping adresse et périmètre. Aucune règle de qualification déplacée.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** 1/N commerces, ordre DSL différent du nom, adresse complète et absence d'un commerce, JSON identique ; compte SQL réel froid/chaud sur cible future.
- **Rollback proposé :** Revenir aux lectures par identifiant après requêtes en cours ; aucune donnée à restaurer. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R08 — Rendre l'onglet gains Coffrets par pages et agrégats

- **Cause / domaines :** RC-13. Domaine et interfaces : GET /protected/animation-locale/animations/{id}/gains et /gains/coffrets/consommation ; GainsAnimTab actuel.
- **Source / fonctions :** `localeo-animation/src/app/App.tsx:2939–2959 ; src/app/api.ts:838–856/1264–1280 ; backend app/api/animation_locale_api.py:2747–2753/2798–2810`.
- **Mécanisme et conséquence :** collectPages collecte toutes les pages avant résolution et le composant attend gains+consommations ; route gains renvoie liste complète. Pagination serveur seule ne borne pas l'ouverture d'écran.
- **Déclencheur / justification :** Dotation de plus d'une page ; erreurs tardives ou actualisation complète.
- **Preuve / mesure :** FORTEMENT ÉTAYÉ PAR LE CODE ; premier rendu et requêtes HTTP réelles NON MESURÉS.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel moyen à élevé selon volume, probabilité conditionnelle/inconnue en exploitation, criticité P2. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Paginer une projection de gains autorisés enrichis de leur consommation sur les mêmes gain_id ; ne pas paginer deux listes indépendamment (conso.find absent afficherait zéro). État page/cursor conservant filtres/navigation/focus ; agrégats exacts sur mêmes définitions (actifs, ENVOYE, zéro/partiel). Route additive et anciens consommateurs conservés.
- **Alternative :** Faire d'abord une projection enrichie ciblée sur les IDs de la page existante ; les totaux restent globaux exacts. Ne pas fabriquer des zéros ni des totaux de page.
- **Classe / effort :** B / M.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Moyen : évolution entre deux dépôts et contrat additif ; compatibilité à prouver, sans suppression de l'ancienne route.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Évolution additive du contrat backend, OpenAPI canonique et contrat embarqué Animation ; migration consommateur ciblée. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** Plusieurs pages, indicateurs exacts, retour/actualisation/focus, réponse obsolète/erreur page tardive, mobile/clavier ; contrat embarqué Animation et OpenAPI canonique à aligner après choix.
- **Rollback proposé :** Revenir au composant/route antérieurs en conservant la nouvelle route additive si déjà consommée ; aucun gain/remise annulé. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R09 — Calculer les statistiques Animation depuis des projections ciblées

- **Cause / domaines :** RC-17. Domaine et interfaces : GET /protected/animation-locale/animations/{id}/live, détail/statistiques et dashboard historique sans mode_lecture=borne.
- **Source / fonctions :** `app/application/animation_locale/services/pilotage_animation.py:65–80/101–126 ; app/api/animation_locale_api.py ; localeo-animation/src/app/App.tsx:1792/1987 et api.ts:1234`.
- **Mécanisme et conséquence :** participants/validations complets pour compter, notifications tenant avant filtre animation ; dashboard historique charge encore plus large. Dashboard courant borne demandé à App.tsx:1210, donc non accusé globalement.
- **Déclencheur / justification :** Animation fréquentée ouverte dans workflow/Live ; statistiques complètes répétées ; volume réel et fréquence inconnus.
- **Preuve / mesure :** FORTEMENT ÉTAYÉ PAR LE CODE, ajout orchestrateur vérifié ; SQL/allocations intégrées NON MESURÉS.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel moyen à élevé selon volume, probabilité conditionnelle/inconnue en exploitation, criticité P2. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** COUNT/GROUP BY/projections transactionnelles avec filtres tenant/animation avant lecture, alertes ciblées ; préserver calculs et toutes variantes de réponse. Agréger les mêmes statuts participants et validations ; ne pas substituer des compteurs de qualification de sens différent. Alertes ciblées mais pas paginées silencieusement. Faits de tirage/gains alimentant actions à examiner séparément.
- **Alternative :** Traiter d'abord /live réellement consommé ; laisser dashboard historique inchangé tant que ses appelants ne sont pas inventoriés.
- **Classe / effort :** B / M.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Moyen : changer le sens des compteurs ou substituer des données partielles au contrat exhaustif. Pas de breaking change requis.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** Statuts/éligibilité/validations annulées et période Paris, zéro, alerte hors animation, borné versus historique ; N/10N tenants étrangers et mêmes résultats métier.
- **Rollback proposé :** Revenir aux calculs en mémoire pour prochaines lectures ; conserver les projections déjà livrées, pas de rollback métier. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## R10 — Lier les cycles email/SMS à leur budget et au bail

- **Cause / domaines :** RC-14. Domaine et interfaces : POST /protected/exploitation/{emails,sms}/batch/envoyer et entrées ERP ; dépendance des liens/confirmations/résultats Live. Les autres types BatchRunner nécessitent examen distinct.
- **Source / fonctions :** `app/application/exploitation/services/batchs.py:608–700 ; app/application/exploitation/use_cases/emails_batch.py:25–92 ; sms_batch.py:17–67 ; scheduler/http_client.py:51–63`.
- **Mécanisme et conséquence :** Bail timeout+60 expirant sans deadline du handler ; timeout du client ne l'arrête pas. Une nouvelle invocation peut être admise après expiration pendant l'ancien travail.
- **Déclencheur / justification :** 100 remises séquentielles à environ 4 s chacune dépasseraient le bail de 360 s, puis déclenchement suivant ; scénario crédible explicite, aucune fréquence ni double envoi observé.
- **Preuve / mesure :** FORTEMENT ÉTAYÉ PAR LE CODE, simulation M02 achevée : refus à+359 s, admission à+361 s avec premier callback actif ; bail360 s. SQLite/horloge logique, pas durée361 s réelle ni concurrence PostgreSQL.
- **Confiance / impact / probabilité / criticité :** élevée sur mécanisme ; impact potentiel élevé sous scénario décrit, probabilité conditionnelle/inconnue en exploitation, criticité P1. Aucun incident ni saturation attribué sans mesure.
- **Minimum :** Budget monotone de cycle, réservations progressives et marge pour fournisseur ; pas de nouvelle unité après perte de propriété. Renouvellement propriétaire borné uniquement si nécessaire. Le budget restant doit couvrir aussi remise_salaries.execute(limit), appelé ensuite par email, ou cette exclusion doit être explicite. Stopper avant claim et transport, jamais abandonner un lot déjà réservé ; bornes d'unité/marge ou renouvellement pour éviter expiration pendant I/O.
- **Alternative :** Bail renouvelé avec borne serveur explicite pour une unité longue ; augmenter seul timeout/bail ne lie pas le travail au budget.
- **Classe / effort :** B / M.
- **Bénéfice :** moins de travail/attente inutile ou meilleure borne dans le périmètre ; plausible seulement. Gain chiffré après correction et capacité API : **NON MESURÉS**.
- **Risques :** Moyen : reprise et remise incertaine. Les claims individuels et libération corrélée existent ; ne pas prétendre double envoi automatique. RC-15 transaction fournisseur reste distinct. Budget coopératif entre unités, pas échéance dure du fournisseur ; compteurs de cycle partiel à définir sans rupture.
- **Compatibilité / breaking change :** aucune rupture requise dans ce minimum, à prouver. Contrat externe conservé, règles du domaine et droits inchangés. Aucune nouvelle migration imposée ; présence et intégrité des migrations existantes restent une précondition lorsque citées. Générateur sans impact si schéma et règles ne changent pas ; fixtures synthétiques adaptées aux tests requis.
- **Tests et preuve attendue :** Avant/après expiration, perte de propriétaire/ancien finally, 2 lanceurs PostgreSQL, réservations non commencées, fournisseur accepté puis crash et rapprochement ; mêmes compteurs/révocations.
- **Rollback proposé :** Suspendre nouveaux déclenchements, terminer/rapprocher les effets engagés avant retour ; garder réservations et journaux, aucun reset/renvoi aveugle. Procédure proposée, jamais exécutée ; conserver tous effets métier committés.
- **Décision utilisateur :** champ vide dans le registre ; aucune autorisation de correction.

## C/D et sujets différés

Les remèdes C possibles (population/reprise de tirage, actualités, protocole de remise hors transaction) sont séparés dans [l'annexe](annexe-optimisations-secondaires.md). Aucun nouveau broker, hausse générale de ressources, suppression de route ou changement silencieux de réponse recommandé. Toute rupture D ou migration nouvelle exigerait une nouvelle fiche justifiée ; aucun refus/accord au nom de l'utilisateur.
