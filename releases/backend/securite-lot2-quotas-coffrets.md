# Quotas et alertes coffrets

Les scans et validations sont limites par commercant (120) et IP (300) sur
la fenetre LOCALEO_AUTH_RATE_LIMIT_WINDOW_SECONDS (900 secondes par defaut).
Les scans d'un meme coffret signe sont limites a 30, tous commercants et IP
confondus. Les echecs de scan ont un budget distinct de 20 par commercant et IP.
Les variables LOCALEO_COFFRET_SCAN_MAX_* permettent l'ajustement en exploitation.
Les valeurs nulles ou negatives ne desactivent pas les quotas.

Chaque dimension est independante. Les compteurs PostgreSQL sont verifies et
incrementes sous verrou transactionnel, y compris la premiere insertion.
Leur commit precede l'operation metier : un echec ou rollback du scan n'efface
pas la tentative. Aucun mode performance ne desactive ces protections.
Une limite atteinte renvoie 429 et Retry-After egal au maximum de la fenetre.
L'adresse IP est celle normalisee par ASGI, jamais un X-Forwarded-For non fiable.

Un evenement durable security.coffret.quota_reached, phase alert, et un warning
structure sont emis une fois au seuil par dimension/fenetre. Surveiller cette
action dans l'audit/collecteur de logs ; metadata.operation distingue scans,
validations et echecs. Les empreintes IP sont hachees, aucun QR ni bearer n'est
journalise. Un seuil d'instance peut signaler des presentations repetitives
chez plusieurs commercants : investiguer avant regeneration du QR.
Le branchement de ce signal aux notifications du collecteur de production
reste une operation de deploiement, pas un envoi automatique configure ici.

Tests : limites independantes, changement d'IP/commercant, echecs, HTTP 429
avant traitement QR et cinq workers PostgreSQL pour deux places disponibles.
