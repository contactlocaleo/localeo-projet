# Correctifs de l'audit et qualification avant production

Date : 5 septembre 2026. Reference initiale : bee7d1a.
Les constats du rapport initial sont historiques ; ce document suit leur traitement.

## Correctifs applicatifs

| Point | Traitement | Verification principale |
|---|---|---|
| F01 | Host strict, autorisation sur scope.path, session sur donnees PWA | Host malforme et acces sans session refuses |
| F02 | Lien commercant-instance obligatoire, projection restreinte | Achat tiers refuse, email beneficiaire masque |
| F03 | HTTPS/autorites explicites, IP publique epinglee, TLS, aucune redirection | DNS prive refuse, transport borne |
| F04 | Starlette 1.3.1 compatible avec FastAPI 0.136.0, corps borne avant parsing | Petits depassements et corps sans longueur |
| F05 | Adresse ASGI, verrou transactionnel du quota | 32 tentatives concurrentes : exactement 5 autorisees |
| F06 | Achat et demande commits avant Stripe, reprise avec UUID stable | Interruption reelle de l'orchestration et reprise sur PostgreSQL |
| F07 | Prise sous verrou et reprise des envois interrompus | Ancien worker refuse apres nouvelle prise |
| F08 | SQL et fournisseurs hors boucle asynchrone | Execution effective dans un autre thread |
| F09 | Mot de passe par defaut refuse independamment du login | Garde de configuration |
| F10 | Quotas paiement/support avant effets externes | Refus 429 avant use case |
| F11 | Chargement groupe des prestations | Une seule lecture pour 30 prestations |
| F12 | Horodatage au plus une fois par 5 minutes, controle de cle maintenu | Revocation immediate et une seule ecriture |
| F13 | Graphe avec hashes, actions/images figees, CI pytest et PostgreSQL | Installation verrouillee, pip check, pip-audit |
| F14 | Token de gestion requis pour la resolution Checkout, logs masques | Refus sans token, expiration/revocation/achat tiers |
| F15 | Acteur issu du principal valide | X-Actor-ID et credentials non verifies ignores |

Deux complements sont corriges : echappement des resumes back-office identifies
par Bandit, et runner de migrations serialise avec dry-run sans ecriture.
Les specifications sont indexees dans [securisation-production.md](../../specifications/securisation-production/README.md).

## Resultats executes localement

- Installation de requirements.txt avec `--require-hashes` : reussie.
- `pip check` : aucune incompatibilite.
- Suite isolee Python 3.12 : **2 220 reussites**, 3 tests PostgreSQL exclus de ce
  passage car ils exigent une base explicitement autorisee ; 4 avertissements de deprecation.
- Passage PostgreSQL separe : **3 reussites** (quota concurrent, reprise Checkout,
  dry-run et runners concurrents), sur une instance locale jetable distincte.
- pip-audit 2.10.1 : **67 distributions, aucune vulnerabilite connue** a cette date.
- Bandit 1.9.4, seuil moyen/eleve : **aucun resultat restant apres corrections et
  qualification locale des faux positifs documentes**.
- Gitleaks sur l'historique complet : **65 occurrences potentielles historiques**.
  Ce controle reste bloquant ; aucune revocation n'est deduite du scan.

Les valeurs de secrets ne sont pas reproduites. Le releve limite aux regles,
fichiers, lignes et commits est dans
[secrets-historiques-expurges.json](2026-09-05-secrets-historiques-expurges.json).
Plusieurs occurrences peuvent designer le meme secret, ou une donnee synthetique.
Verifier les services Stripe/Brevo et les cles internes concernees, revoquer les
secrets exposes et tracer leur remplacement. Toute exception historique exige
une preuve de revocation ou de faux positif ; aucun ignore global n'est ajoute.

## Conditions de mise en production encore a satisfaire

1. Appliquer **v217_initialisation_checkout_durable.sql avant le nouveau code**.
   Aucun acces a la base de production n'a ete effectue.
2. Adapter le front au contrat F14 : le session_id Stripe seul ne donne plus le
   detail de l'achat. Utiliser le lien de gestion recu par email. Le depot front
   n'a pas ete fourni. Conserver l'Idempotency-Key client lors des reprises.
3. Qualifier et traiter les secrets historiques, puis obtenir un controle CI vert.
4. Verifier le proxy cible : Host, limite des corps et des connexions lentes,
   liste explicite des proxies autorises, masquage des URLs sensibles, sortie WebPush.
5. Executer la recette sur la version PostgreSQL cible, une restauration de
   sauvegarde et les controles de retention, supervision et reprise des batches.

L'environnement de preproduction autorise, le proxy et la preuve de rotation
n'ont pas ete fournis. Les corrections du backend ne constituent donc pas une
declaration d'aptitude a la production. Les modifications de roadmap deja presentes
dans le workspace ont ete preservees et exclues des commits.
