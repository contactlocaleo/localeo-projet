# Execution des migrations

Un verrou consultatif PostgreSQL de session serialise les runners sur la meme
base avant lecture des checksums. Une seule connexion conserve ce verrou entre
les transactions de migrations, y compris les scripts contenant COMMIT.
Le verrou est libere a la sortie ; la connexion est fermee en cas d'echec.

Le mode `--dry-run` ne cree plus la table de suivi et n'ecrit aucune donnee de
migration. Il lit le catalogue et les checksums disponibles. Une base jetable
verifie l'absence de ces effets et deux runners concurrents appliquant une
migration exactement une fois. Aucune migration historique n'est modifiee.
