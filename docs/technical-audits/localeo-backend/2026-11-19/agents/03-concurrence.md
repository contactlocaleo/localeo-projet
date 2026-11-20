# Audit indépendant — concurrence

Première analyse finalisée le 19 novembre 2026, sans lecture des autres rapports d’agents. Inspection statique directe du backend ; aucune modification applicative, exécution de test, mesure, import applicatif, connexion base/réseau ou lecture de configuration privée. Le prévol a réellement lu `app/main.py` via shell : `application_lifespan`, ligne 169, et son déport de l’arrêt via `asyncio.to_thread`, ligne 188.

Révision backend contrôlée par l’orchestrateur : `7049e7fafc76f9119924f1082a5ee7457a175d85`, branche `main`, arbre applicatif propre.

Le rapport retient **trois anomalies ou risques majeurs**, sans remplir artificiellement cinq places. Les autres chemins et protections sont consignés dans [l’annexe](03-concurrence-annexe.md). Les valeurs de configuration citées sont les défauts du code, pas celles d’un déploiement observé. Le nombre de processus ASGI, la limite effective du pool de threads et la charge réelle restent inconnus.

## Classement

L’ordre applique successivement l’impact potentiel, la probabilité, la criticité métier, la preuve puis la facilité de correction. Une probabilité qualifiée ici décrit la condition de code ; aucune fréquence d’incident n’a été mesurée.

| Rang | ID | Impact potentiel | Probabilité conditionnelle | Criticité métier | Preuve | Correction |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ASY-01 | Arrêt de progression des requêtes du même processus ASGI pendant un batch ERP | Forte dès qu’un opérateur lance un batch avec travail effectif ; fréquence inconnue | Envois email/SMS critiques et disponibilité des autres parcours du processus | FORTEMENT ÉTAYÉ PAR LE CODE | S |
| 2 | ASY-02 | Connexions et verrous métier retenus pendant les attentes fournisseur | Forte pour chaque envoi effectif ; saturation dépend du parallélisme | Remise d’accès, confirmations et SMS ; concurrence avec révocation/conservation | FORTEMENT ÉTAYÉ PAR LE CODE | M pour borner ; L pour découpler |
| 3 | ASY-03 | Chevauchement possible d’un batch toujours actif après expiration de son verrou | Moyenne, sous lenteur cumulée ou gros lot | Exclusivité des traitements email/SMS et capacité partagée | FORTEMENT ÉTAYÉ PAR LE CODE | M |

## ASY-01 — Les batchs manuels ERP exécutent SQL et HTTP dans l’event loop

**Domaine :** concurrence ASGI / exploitation ERP. **Statut : FORTEMENT ÉTAYÉ PAR LE CODE.**

**Sources et fonctions.** Dans [admin.py:12523](../../../../../../localeo-backend/app/infrastructure/admin/admin.py#L12523), `setup_admin.admin_lancer_batch_envoi_emails` est un handler `async def`. Il appelle directement `BatchRunner().execute`, puis `creer_batch_emails(...).execute` par son `handler`, sans `await` de déport. Même structure pour `admin_synchroniser_statuts_emails` à 12543, `admin_lancer_batch_envoi_sms` à 12562 et `admin_synchroniser_statuts_sms` à 12584. [BatchRunner.execute:642](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L642) exécute `handler()` à 669, dans le thread appelant. [LancerBatchEmails.execute:21](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L21) parcourt ses candidats et appelle le fournisseur à 79. [ServiceEnvoiEmail._envoyer:49](../../../../../../localeo-backend/app/infrastructure/email/service_envoi_email.py#L49) appelle `requests.post` à 64 ; la consultation des statuts fait `requests.get` à 124. Les SMS emploient également `requests` synchrones avec `timeout=20`.

**Chaîne vérifiée.** `POST /internal/emails/batch/envoyer` → handler async ERP → `BatchRunner.execute` → `LancerBatchEmails.execute` → `ServiceEnvoiEmail.envoyer` → HTTP Brevo. Les routes `/internal/emails/batch/synchroniser-statuts`, `/internal/sms/batch/envoyer` et `/internal/sms/batch/synchroniser-statuts` présentent le même mécanisme. `setup_admin` est monté dans `main.py:525` ; il ne s’agit pas d’un helper async sans appelant établi.

**Mécanisme et conséquence.** Le corps du handler reste exécuté par la boucle ASGI. Les attentes SQL synchrones et les appels réseau ne rendent pas la main à cette boucle. Une opération pourtant administrative peut donc retarder les réponses et le traitement des autres connexions du même processus, notamment les parcours publics, de scan ou les webhooks. Un `requests` qui libère le GIL pendant son attente ne rend pas pour autant la boucle disponible : son thread continue d’attendre le retour de l’appel.

**Déclencheur et bornes.** Lancer un de ces batchs depuis l’ERP avec des messages à traiter suffit à atteindre le mécanisme. Le défaut `limit=100` et le délai réseau de 20 secondes par appel sont des bornes locales, pas un budget temporel global de batch. Le nombre d’appels dépend des candidats et des erreurs ; aucun temps total n’est annoncé. Un lot vide peut encore effectuer du SQL synchrone. Plusieurs processus ASGI réduiraient la portée à chaque processus atteint ; leur nombre n’est pas établi.

**Mesure disponible :** aucune. **Confiance :** élevée pour le blocage de la boucle sur ce chemin ; impact et fréquence en exploitation non quantifiés.

**Correction minimale compatible :** résoudre l’identité de l’opérateur puis déporter l’ensemble du travail synchrone du batch avec `run_in_threadpool`, ou transformer le handler complet en `def` si aucun accès async n’est nécessaire. Garder acquisition du verrou, UoW, envoi, journal et libération dans cette unité synchrone ; ne pas dispatcher chaque requête ORM séparément. Réutiliser le modèle déjà employé par les webhooks Stripe et l’authentification ERP. Cela protège la boucle mais occupe encore un thread pendant le batch : ASY-02 et ASY-03 restent à traiter séparément.

**Effort : S. Risque :** faible à modéré, surtout propagation d’erreurs, contexte de corrélation et accès à la session HTTP. **Breaking change : non**, pour ce déport conservant le contrat HTTP. **Autres domaines affectés :** API, SRE et persistance ; cause candidate = réutilisation d’orchestrations synchrones depuis des entrées async ERP sans frontière de déport explicite. Les uploads présentent des manifestations secondaires de cette même cause, détaillées en annexe.

## ASY-02 — Les transactions d’envoi conservent leur connexion et leurs verrous pendant HTTP

**Domaine :** concurrence transactionnelle / exploitation. **Statut : FORTEMENT ÉTAYÉ PAR LE CODE.**

**Sources et fonctions.** [emails_batch.py:73](../../../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L73) ouvre un UoW pour chaque email, appelle `obtenir_pour_envoi`, puis `provider.envoyer` avant `uow.commit()` à 87. [EmailSortantRepositorySqlAlchemy.obtenir_pour_envoi:1105](../../../../../../localeo-backend/app/infrastructure/persistence/repositories/repositories_sqlalchemy.py#L1105) verrouille les capacités associées puis sélectionne l’email avec `FOR UPDATE SKIP LOCKED`. [conservation_emails_saas.py:74](../../../../../../localeo-backend/app/infrastructure/persistence/conservation_emails_saas.py#L74) peut verrouiller le gestionnaire et la capacité ; ces protections précèdent le réseau. Pour les SMS, [sms_batch.py:60](../../../../../../localeo-backend/app/application/exploitation/use_cases/sms_batch.py#L60) conserve pareillement le UoW autour de l’envoi à 64 et du commit à 67 ; repository à 1192. La fermeture intervient à la sortie du UoW, [sqlalchemy_unit_of_work.py:216](../../../../../../localeo-backend/app/infrastructure/persistence/uow/sqlalchemy_unit_of_work.py#L216).

**Chaîne vérifiée.** Batch API protégé ou batch manuel ERP → sélection/réservation committée → nouvel UoW → verrou email/SMS et, selon son type, capacité métier → requête fournisseur → mise à jour et commit. Ce risque existe aussi via [lancer_batch_emails:26](../../../../../../localeo-backend/app/api/emails_api.py#L26), handler `def` : il concerne alors le thread et la base, sans justifier un diagnostic de blocage de l’event loop.

**Mécanisme et conséquence.** Une connexion PostgreSQL reste empruntée pendant l’aller-retour externe ; des commandes portant sur la même capacité peuvent attendre les verrous conservés. Sous plusieurs traitements concurrents, les attentes réseau se traduisent en pression sur le pool et en contention métier. [db.py:33](../../../../../../localeo-backend/app/infrastructure/persistence/db.py#L33) configure par défaut 5 connexions et 5 débordements par processus, avec 30 secondes d’attente d’acquisition. Ces défauts ne prouvent ni épuisement observé ni limite globale du déploiement.

**Déclencheur et bornes.** Fournisseur lent ou dégradé pendant un envoi effectif, avec d’autres opérations concurrentes utilisant la base ou les mêmes capacités. `SKIP LOCKED` évite d’attendre l’email lui-même pour un autre candidat ; il ne libère ni la connexion utilisée ni les autres verrous déjà pris. La réservation initiale est bien committée avant la boucle d’envoi : il serait faux d’affirmer que tout le lot reste verrouillé pendant tout le réseau. Le timeout réseau de 20 secondes existe, mais n’est pas un plafond global garanti de transaction.

**Mesure disponible :** aucune attente de verrou, occupation du pool ou durée de transaction relevée. **Confiance :** élevée sur la rétention ; moyenne sur son incidence en exploitation.

**Correction minimale compatible :** rendre les délais connexion/lecture fournisseur explicitement configurables et prudents, borner le travail d’un cycle côté serveur, et conserver les protections de révocation existantes. Ce correctif borne l’exposition sans supprimer entièrement la rétention. Un découplage complet exige un protocole de remise/claim et de rapprochement qui préserve l’autorisation jusqu’à la remise ainsi que le traitement des résultats incertains ; ce n’est pas un simple déplacement de `commit`. En particulier, ne pas relâcher les verrous de capacité avant HTTP sans preuve métier compensatoire.

**Effort : M** pour les budgets ; **L** pour supprimer la rétention réseau. **Risque :** modéré pour les délais, élevé pour un découplage naïf susceptible de remettre un lien révoqué ou de réémettre après résultat incertain. **Breaking change : non** pour les budgets sans changement de protocole. **Autres domaines affectés :** persistance, API, SRE, identité et conservation ; cause candidate = atomicité de remise garantie par une transaction couvrant un effet externe, sur le pool partagé des requêtes métier.

## ASY-03 — Le verrou de batch expire sans renouvellement ni arrêt du handler

**Domaine :** exclusivité des batchs / capacité. **Statut : FORTEMENT ÉTAYÉ PAR LE CODE.**

**Sources et fonctions.** [BatchRunner._acquire_lock:608](../../../../../../localeo-backend/app/application/exploitation/services/batchs.py#L608) supprime les verrous expirés puis fixe `expires_at = now + timeout_seconds + 60` à 622. `execute`, lignes 642–703, appelle directement son handler sans deadline serveur ni renouvellement périodique du verrou. Emails et SMS sont déclarés avec `timeout_seconds=300`, lignes 169–196 : leur verrou a donc une échéance nominale de 360 secondes. [BatchHttpClient.execute:34](../../../../../../localeo-backend/app/infrastructure/scheduler/http_client.py#L34) configure un timeout HTTP, qui n’est pas un mécanisme d’annulation du handler synchrone serveur.

**Chaîne et mécanisme.** Scheduler ou opérateur → premier `BatchRunner.execute` → traitement séquentiel des candidats → échéance du verrou atteinte pendant que le handler travaille toujours → nouvelle requête → suppression du verrou expiré et acquisition par cette deuxième exécution. La libération finale filtre heureusement par `correlation_id` : l’ancienne exécution ne supprime pas le nouveau verrou. En revanche, l’exclusivité annoncée du batch n’est plus assurée après l’échéance.

**Conséquence, déclencheur et protections.** Si la somme des attentes fournisseur et SQL dépasse le bail, un second lancement peut accroître la concurrence, l’occupation des threads et des connexions. La limite de lot règle un nombre de candidats, pas sa durée. Le scheduler utilise `max_instances=1`, mais seulement pour son job local : cette protection ne couvre pas un lancement manuel ni un handler serveur continuant après timeout du client. Les réservations par message et `SKIP LOCKED` restent présents ; **aucun double envoi ni corruption de données n’est établi** par ce constat. Le risque démontré est la possibilité de chevauchement et de pression supplémentaire.

**Mesure disponible :** aucune exécution dépassant le bail observée. **Confiance :** élevée sur la fenêtre de chevauchement, moyenne sur sa probabilité réelle. **Correction minimale compatible :** renouveler le verrou avec contrôle de propriété depuis une transaction courte indépendante et arrêter de prendre de nouveaux éléments si le bail est perdu ; ajouter un budget serveur de cycle compatible avec les appels fournisseur en cours. Éviter de présenter une simple augmentation du timeout client comme une garantie d’exclusivité.

**Effort : M. Risque :** modéré, arrêt/reprise et libération conditionnelle à vérifier. **Breaking change : non** si les réponses et compteurs restent compatibles. **Autres domaines affectés :** SRE, API et persistance ; cause candidate = utilisation d’un timeout de catalogue/client comme durée de bail, sans suivi de vie de l’exécution serveur. Ce constat n’est pas consolidé avec les autres audits.


## Vérification documentaire par l’orchestrateur

Première version indépendante finalisée avant contrôle. Chaînes des batchs ERP, envoi sous verrou et échéance du bail relues directement dans les sources citées. SHA ajouté et ligne du commit email rectifiée (87) ; constats et ordre conservés. Aucun rapprochement avec les autres rapports.
