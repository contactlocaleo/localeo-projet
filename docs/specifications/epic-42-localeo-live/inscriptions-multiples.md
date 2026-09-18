# Localeo Live — plusieurs inscriptions à une animation

Ajouter une animation au carnet demande désormais l’e-mail d’inscription, même si l’installation est déjà associée à un participant. Le statut « Déjà inscrit » ne sélectionne pas une identité et ne bloque pas l’ajout d’une autre inscription.

- « Recevoir mon lien d’inscription » appelle `POST /public/animation-locale/animations/{animation_id}/inscriptions/renvoyer-lien` avec `{ email }`.
- Le backend répond toujours 202 avec le même message pour une adresse connue ou inconnue. Il envoie le lien à l’adresse enregistrée si la participation reste accessible, avec un délai minimal de cinq minutes entre envois. Aucun token ne revient dans cette réponse.
- Ouvrir le lien personnel affiche l’e-mail associé à la participation, lu avec `inclure_contact=true`. Confirmer conserve le token, la participation et son e-mail dans le carnet local.
- La clé reste `participation:{participant_id}` : deux adresses inscrites à la même animation produisent deux entrées indépendantes. Un nouvel ajout de la même participation actualise l’entrée existante.
- « M’inscrire avec cette adresse » ouvre le formulaire complet prérempli, sans inscrire automatiquement l’utilisateur. L’e-mail passe dans l’état de navigation, pas dans l’URL.
- Les anciennes fiches génériques proposent « Retrouver mon inscription ». Leurs marqueurs d’inscription ne valent pas accès personnel.
- Le retrait d’une participation ne supprime pas l’autre et ne désinscrit personne.

Cette évolution nécessite les changements de `localeo-marketplace` et `localeo-backend`. Les autres frontends ne changent pas ; le contrat d’inscription existant continue de refuser les doublons pour une même adresse.
