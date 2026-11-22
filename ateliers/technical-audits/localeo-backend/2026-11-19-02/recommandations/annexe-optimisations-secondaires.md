# Observations secondaires et remèdes hors backlog principal

Les dix fiches principales ne constituent pas un inventaire exhaustif. Aucun problème ci-dessous n'est déclaré corrigé faute de ticket. Les six causes candidates annexées de la consolidation restent documentées ; les réserves historiques et observations mineures s'y ajoutent sans être comptées comme de nouvelles causes majeures.

| Cause / origine | Preuve et portée | Traitement proposé / limite |
| --- | --- | --- |
| RC-03 — CONC-02, rendu email inscription | participants_animation.py:137/282–308 ; ServicePreparationEmail:175–268 : QR/template dans la coordination exclusive non-tombola. Pas d'envoi réseau direct dans cette transaction | B/C à concevoir séparément : préparation pure hors section avec revalidation de version, ou intention durable reprise. Ne pas déplacer le commit avant outbox. Capacité, reçu, token et email atomiques ; mesurer temps sous verrou avant priorité. R02 réduit le comptage seulement |
| RC-08 — MEM-02, diffusion actualités | localeo_live_api.py:825–1023 : transitions/actualités/installations globales, boucles de ciblage | C / L possible : pages stables avec progression et barrière de statut, convergence et dry_run équivalents. Ajouter LIMIT seul peut affamer des destinataires ; pas de refonte recommandée sans exposition/mesure |
| RC-09 — MEM-04, retrait classique | demandes_participation_commercants.py:613–616 appelle faits_participations complet alors que seul participant.id sert avant relecture verrouillée | B / M : parcours des IDs puis réconciliation actuelle. Préserver atomisme et flush/identity map ; chasse publiée suit neutralisation dédiée. Fréquence et coût inconnus |
| RC-11 — API-01, revalidation média | jeu_animation.py:459–463 ; contenu_generation.py:368–395 : recharge/base64/décodage des médias sélectionnés | Cache interne borné par octets/SHA immuable après autorisation courante, option distincte B/M ; aucune nécessité démontrée. Ne garantit pas deadline RC-10, ne cache pas un droit révoqué |
| RC-15 — SRE-02, réseau sous SQL | emails_batch.py:76–92, sms_batch.py:60–67 : remise sous UoW/verrou d'autorisation | C possible / L pour protocole propriétaire en trois temps. Ne pas sortir simplement HTTP de transaction : révocation/conservation/remise incertaine changeraient. Pas de saturation du pool démontrée ; R10 ne règle pas cette cause |
| RC-16 — SRE-03, scheduler | coordinator.py:110–136 et défaut4 threads ; tâches de transport et temporelles partagent executor | HYPOTHÈSE À VÉRIFIER, pas P1. Observer attente/missed/occupation avant séparer executors ou décaler cron. Augmenter threads/pool sans budget global non retenu |

## Réserves historiques persistantes, hors priorité de cette relance

Backend identique à la référence : anciennes OPT-03/05, expiration_coffrets.py:82/118/239, ont encore la sélection avant exclusion et les lectures répétées sous verrou ; aucun SQL rejoué. OPT-06, export_financier.py:13–27, est reproduite par M06 : pic Python 5 494 404 octets à 10k, sans OOM ni fuite ; spool B/M différable, pas une correction Live prioritaire. OPT-08, consulter_retour_paiement.py et paiement_gateway.py:226 : helper Stripe enrichi avec X-Checkout-Session reste ; absence d'en-tête évite cet appel. Mesures intégrées NON EXÉCUTÉES, gains NON MESURÉS.

Ancien catalogue public : comptage global et paramètres effectifs par animation persistent (catalogue_animations_publiques.py:340/368/634), malgré groupements déjà livrés. Ne pas assimiler à la recherche moderne. API/frontend Mes lots et carnet historiques du 8 novembre ne sont pas repris comme verdict courant sans graphe d'appels actualisé.

## Observations conditionnelles des annexes

Les imports modernes ont limites de fichier/lignes/cellules et worker par lots ; leur complexité imbriquée n'est pas automatiquement majeure. Un lancement multiworker peut néanmoins converger sur un même lot sans claim d'opération (S-CONC-05), avec suspension sur timeout de verrou ; scénario non exécuté. Un claim durable pourrait exiger migration additive, non proposée ici.

Les lectures historiques de participants et détails d'email peuvent conserver des N+1 ; les principaux workspaces modernes utilisent des projections bornées. La définition passeport est différente des jeux plafonnés à100 commerces. Les bornes médias/JSON, quota image, idempotence et protections email existent : aucune suppression suggérée.

WebPush : DNS avant deadline et état de reprise par notification plutôt que par abonnement peuvent allonger/rejouer le transport (annexes concurrence/SRE). Tags, claims et baux individuels limitent déjà certains effets. Aucun double effet métier démontré. Le singleton SQL du limiteur peut créer une contention conditionnelle ; nombre de requêtes ne prouve pas saturation.

Les alternatives de sélection en réservoir, nouveaux jobs/brokers, hausse générale de workers/pool, suppressions de routes ou réponses202 remplaçant des réponses synchrones ne sont pas adoptées. Catégorie C/D exige périmètre et preuves spécifiques ; aucun choix n'est prérempli au nom de l'utilisateur.

## R05 / RC-06 après mesures : copie différable, population toujours à qualifier

La seule suppression de list(tuple_ids) avant sample est P3 différable, hors des neuf corrections principales. Conserver le contrôle des doublons du domaine et vérifier toutes sources aléatoires injectées. Aucun avant/après : gain NON MESURÉ. M-LIVE-01 ne comprend ni UUID/tuple déjà construits, ni SQL, verrou ou notifications ; le faible pic transitoire à10k ne prouve pas un faible coût du tirage complet. Le chargement intégral O(N) sous coordination exclusive reste une cause distincte à mesurer avant grande jauge. Le réservoir uniforme/reprise est un lot B/C séparé, pas inclus dans ce petit correctif.
