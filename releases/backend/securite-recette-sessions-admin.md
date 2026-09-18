# Recette des autorisations administrateur

Les tests DATA008 et DATA009 utilisaient un cookie signe sans session serveur,
desormais refuse par le registre de revocation. Ils ne pouvaient plus atteindre
les controles de role et de POST intentionnel qu'ils devaient verifier.

Une fixture opt-in cree une vraie session dans un registre SQLite ephemere.
Le middleware et les controles applicatifs restent actifs. Les tests couvrent
les refus 403 des roles limites, le refus des origines hostiles et les actions
ADMIN autorisees. Les tests du cycle de session conservent le refus des anciens
cookies sans registre. Aucune modification des autorisations de production.
