# Liens de consultation a usage unique

Les nouveaux liens email portent un code signe dans le fragment #code=...
(24 heures). Le code contient l'identifiant du coffret et l'empreinte de sa
version de consultation, jamais le bearer durable. Le navigateur retire le
fragment puis echange le code par POST contre une session de 8 heures.
PostgreSQL conserve uniquement les empreintes du code consomme et du bearer.
Deux echanges simultanes ne peuvent pas produire deux sessions. La revocation
ou regeneration du lien invalide aussi les sessions liees a cette version.
Les codes uses restent marques au moins jusqu'a leur expiration ; aucune
suppression automatique ne doit supprimer un marqueur encore rejouable.

Un lien expire ou deja utilise propose un renvoi vers l'adresse beneficiaire
existante (ou l'acheteur), avec reponse generique et quotas par IP et instance.
Le renvoi ne modifie ni l'adresse ni la version QR. Le bon papier et le QR
inline de l'email restent utilisables selon leurs regles metier.

Deployer la migration v233 puis backend et marketplace ensemble. Les anciens
bearers restent acceptes dans Authorization pour les parcours existants ;
les liens historiques peuvent encore etre lus pendant cette migration.
Ils doivent etre regeneres en cas de fuite : le fragment n'efface pas des
journaux historiques. Une session expiree de la bibliotheque Live demande un
nouveau lien ; elle n'est pas rafraichie a partir du code deja consomme.

Brevo : contactPixelTrackingConsent=false est envoye pour les destinataires
des emails sensibles. Activer la gestion du consentement de suivi par contact
dans le compte Brevo avant mise en production et verifier que les liens recus
ne sont pas reecrits. Ce reglage distant n'est pas modifie par les commits.
Reference : https://help.brevo.com/hc/en-us/articles/37113920427922-About-email-tracking-pixels-and-the-CNIL-recommendation-in-Brevo

Recette : usage unique/rejeu/concurrence, expiration, mauvais coffret,
revocation de generation, renvoi non enumerant, retrait du fragment avant
reseau, absence de secret durable dans les liens produits et erreurs/logs.
