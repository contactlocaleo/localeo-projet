# Lots 1 et 2 : implementation et validation

Recette locale du 13 septembre 2026. Perimetre : lots 1 et 2 du
[rapport initial](../../docs/audits/backend/security_best_practices_report.md).
Aucun deploiement, envoi d'email reel ni acces a une base de production.
Les modifications utilisateur presentes dans les depots ont ete conservees.

## Corrections livrees

| Correction | Commit backend | Commit marketplace |
| --- | --- | --- |
| Ecriture des types de coffrets reservee a ADMIN, CSRF, ancien POST public refuse | `bfdb1a8` | Sans changement |
| Catalogue public sans contacts operationnels, routes privees autorisees explicitement | `0e781ca` | `53577ca` |
| Emission QR aleatoire, controle du QR actif, revocation des transactions anterieures sous verrou | `090814d` | Sans changement |
| Scan par JSON et image QR par header, refus du transport query | `3041ba9` | Client commercant deja compatible |
| Cache interdit sur les vraies routes sensibles | `1bd89ad` | Sans changement |
| Quotas PostgreSQL independants par commercant, IP et instance, alertes durables | `4c5249a` | Sans changement |
| Liens email a usage unique, session courte, renvoi borne, retrait des secrets des liens/logs | `fcab084` | `5f30c27` |
| QR malformes refuses proprement | `5bef80f` | Sans changement |
| Fixtures de permissions admin utilisant le registre de sessions reel | `395fc40` | Sans changement |

Chaque correction comprend ses tests et sa note. Les deux changements de
contrat applicatif ont un commit dans chaque depot concerne. L'application
commercant conserve son contrat de scan JSON ; sa compatibilite est testee.

Les liens email expirent apres 24 heures et s'echangent une fois contre une
session de 8 heures maximum. Les empreintes seules sont persistees. Le code
est retire du fragment avant l'appel reseau ; il n'est pas inscrit dans le
carnet Live. Un nouveau lien permet d'actualiser la session du coffret deja
present dans le carnet. La regeneration/revocation invalide aussi les sessions
et les QR de la generation precedente.

## Resultats

| Campagne | Resultat |
| --- | --- |
| Suite backend : securite, achats, exploitation, identite/acces, emails, schema et API QR | 468 reussis, 3 ignores |
| Integration PostgreSQL : revocation QR, migration v232, concurrence de consommation et integrite | 17 reussis |
| Integration PostgreSQL : usage unique concurrent, migration v233, revocation de session, quotas concurrents et alerte durable | 2 reussis |
| Marketplace : contrats catalogue/echange/renvoi, nettoyage des URL | 8 reussis |
| Marketplace : navigateur, QR mobile, transfert Live, lien expire, renouvellement du carnet depuis Live/detail/QR | 9 reussis |
| Commercant : ouverture, validation, statuts et contrats API | 42 reussis |
| Build de production isole et lint des fichiers marketplace modifies | Reussis |
| Lanceur remplacant le diagnostic historique | 71 reussis, inclus dans la couverture backend ci-dessus |

Les trois tests ignores sont ceux de `tests/security/test_market_postgres_regressions.py` :
leur garde impose un cluster historique au port 25432. Ils concernent
l'inscription Animation et des contraintes d'achat preexistantes. Les tests
PostgreSQL des corrections livrees ont tous ete executes, sur un cluster
jetable distinct au port 55492. Les avertissements de depreciation
Starlette/SQLite et le cycle de cles etrangeres preexistant des profils
commercants ne sont pas des echecs de la recette.

Commande de recette rapide, depuis un environnement avec `requirements.txt` :

```powershell
python output/security/reproduce_coffret_auth.py
```

La recette elargie utilise `scripts/validation/test_isolated.py` avec `tests/security`,
les tests application achat/exploitation/identite-acces, preparation/envoi
email, rate limit, schema readiness et `tests/api/test_qr_api.py`.
Le runner bloque les fichiers .env, le bootstrap, les schedulers, les appels
reseau et les connexions DB externes. Pour les tests PostgreSQL, fournir
explicitement `--postgres-test-url` vers la base jetable autorisee
`postgresql+psycopg://audit_test@127.0.0.1:55492/localeo_audit_test`.
Les anciens tests de concurrence Animation utilisent aussi la variable
`ANIMATION_TEST_DATABASE_URL` vers cette meme base jetable.

Les tests navigateur utilisent la configuration
`playwright.desktop.config.cjs` de la marketplace et les scenarios
`securite coffret`, `transfert vers Localeo Live` et
`consultation et l'impression du QR`. Les appels externes y sont interdits
et les reponses applicatives simulees. Les verifications transactionnelles
reelles sont celles du backend PostgreSQL.

## Mise en production

1. Preparer un deploiement coordonne backend/marketplace. Appliquer les nouvelles
   migrations v232 et v233 via `scripts/database/apply_migrations.py`, en verifiant d'abord
   le `--dry-run` sur l'environnement vise. Ne pas lancer les tests sur cette base.
2. Basculer tous les workers vers le backend corrige et la marketplace associee
   avant reprise normale des parcours. Les anciens workers ne doivent plus
   accepter des QR selon les anciennes regles. Les transactions OPEN sans
   empreinte sont expirees par v232 : rescanner suffit.
3. Verifier les URLs frontend configurees et les quotas `LOCALEO_COFFRET_SCAN_MAX_*`.
   Le client commercant utilise deja le corps JSON ; les integrations personnelles
   du PNG doivent passer `X-QR-Token`.
4. Activer dans Brevo la gestion du consentement de suivi par contact pour que
   `contactPixelTrackingConsent=false` des emails sensibles soit respecte.
   Verifier sur un email de recette que le lien n'est pas reecrit. Voir
   [la note des liens](securite-lot2-liens-consultation.md) et sa reference Brevo.
5. Raccorder l'action durable `security.coffret.quota_reached` aux notifications
   du collecteur d'exploitation. Verifier la redaction des journaux du proxy,
   de l'hebergeur et des outils de suivi. Les anciens secrets deja journalises
   ne sont pas effaces par ces commits : revoquer/regenerer les acces compromis.

Les anciens liens de consultation restent acceptes pendant la migration.
Les bons papier existants restent utilisables tant que leur QR correspond
exactement a l'emission active. Une regeneration/revocation rend leurs anciennes
copies inutilisables. Conserver les marqueurs de code utilise jusqu'a expiration
du code ET de la session ; aucune purge automatique n'a ete ajoutee.

La confirmation independante du beneficiaire et le MFA administrateur
appartiennent au lot 3. Les autres renforcements complementaires du rapport
(robustesse des cles au demarrage, cycle de vie des cles API, passerelle reseau,
procedure de secours) ne sont pas declares implementes par cette recette.
Un bon papier reste un titre au porteur : ces lots reduisent les surfaces de
vol et rendent la revocation effective, sans prouver l'identite du beneficiaire.
