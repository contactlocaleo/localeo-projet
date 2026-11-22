# Configuration et ressources

Date locale : 2026-11-19, Europe/Paris ; instant initial dans [baseline](../validation/baseline.json). Poste partagé Windows 11 Famille 10.0.26200, Intel Core i7-10510U, 4 cœurs/8 processeurs logiques, RAM physique 17 007 263 744 octets. Mémoire disponible ponctuelle avant campagne : environ 2,5 Gio, variable. Fréquence et charge externe non stabilisées.

Défauts source app/infrastructure/persistence/db.py:33 : pool_size=5, max_overflow=5, pool_timeout=30 s, recycle=1800 s, pre_ping=true. Ces valeurs sont configurables et par processus ; elles ne prouvent ni dix connexions allouées ni leur consommation actuelle. app/config.py:151 : scheduler max_workers par défaut 4 ; coordinator.py:112–133 : coalesce=true et max_instances=1 par job. Cela n'impose pas un plafond global métier entre réplicas.

Aucun dotenv privé lu ; valeurs runtime opérateur, URL de base, quotas fournisseurs, proxy, limites CPU/RAM et topologie déployée INCONNUS. Aucun serveur, port ou base attribué à un agent. Seul l'orchestrateur possède le processus de mesure ; SQLite en mémoire uniquement pour simulation, pas une cible SQL intégrée.

Observabilité source : app/observability.py, observability_http.py et observability_instrumentation.py ; journaux corrélés BatchRunner. Les compteurs disponibles dans le code ne sont pas des séries de production observées. p95 API, attente pool, âge outbox et saturation ne sont pas mesurés.
