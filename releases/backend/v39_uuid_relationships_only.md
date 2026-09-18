# Localeo V39 - Modifications ciblées

Cette version part de la version fournie et applique uniquement deux modifications :

1. génération automatique des clés primaires UUID côté ORM :
   - `default=uuid.uuid4`

2. ajout des `relationship(...)` SQLAlchemy pour exploiter correctement les clés étrangères :
   - dans le code SQLAlchemy
   - dans SQLAdmin via des listes de sélection

Aucune autre refonte n'a été ajoutée.
