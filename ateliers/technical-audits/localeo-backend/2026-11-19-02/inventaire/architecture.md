# Architecture inspectée

Les cinq dépôts restent indépendants. Backend FastAPI : routes app/api et ERP SQLAdmin app/infrastructure/admin → services/use cases app/application → domaine app/domaine et ports → UoW SQLAlchemy synchrone et repositories app/infrastructure/persistence. Aucun import d'app.main effectué.

Live est servi par Marketplace ; le portail organisateur est localeo-animation et le scan terrain par localeo-commercant. Les commandes préservent idempotence, reçus, accès tenant et transitions du domaine. Les lectures ne sont pas toutes équivalentes : jeu moteur paginé, tableau personnel borné, dashboard Animation borné et anciennes projections exhaustives coexistent.

La persistance utilise PostgreSQL via psycopg synchrone ; les transactions s'ouvrent dans l'UoW. Les envois email/SMS passent par réservations/outbox et fournisseurs ; APScheduler coordonne des endpoints HTTP avec bail BatchRunner côté serveur. Un timeout HTTP n'interrompt pas nécessairement le handler. Les lectures médias utilisent un adaptateur local/S3.

Sources : app/main.py (lecture seulement), app/infrastructure/persistence/db.py:33, uow/sqlalchemy_unit_of_work.py, app/infrastructure/scheduler/coordinator.py:112, app/application/exploitation/services/batchs.py:608. Carte détaillée : [flux](flux-critiques.md).
