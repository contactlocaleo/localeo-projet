# F05 - Identite reseau et concurrence du limiteur

L'application utilise exclusivement l'adresse client du scope ASGI. Les en-tetes
X-Forwarded-For et X-Real-IP ne constituent pas une preuve d'identite. Le serveur
doit etre lance avec une liste explicite des adresses de proxies autorises
(`--forwarded-allow-ips`), jamais `*` sur une entree accessible directement.

Sur PostgreSQL, une cle (operation, login normalise, hash IP) est protegee par
un verrou consultatif transactionnel avant toute lecture, y compris si la
fenetre n'existe pas. Le verrou couvre verification, creation et increment et
est libere au commit/rollback. Cela serialise les tentatives d'une meme cle
entre processus. Toutes ces operations doivent utiliser le meme Unit of Work.
SQLite reste reserve aux doubles de test et n'offre pas cette garantie.
