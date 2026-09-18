# Registre des anomalies

## ALL
| Identifiant | Périmètre | Description | Suivi |
| --- | --- | --- | --- |
| ANO-ANI-01 | inscription | Erreur « Failed to fetch » après « Tout envoyer » dans l’onglet Invitations, alors que les invitations sont bien envoyées et visibles après actualisation. | Corrigé côté interface : vérification de l’état serveur après une perte de réponse, sans nouvel envoi automatique. Validation en environnement réel à effectuer. |
| ANO-ANI-02 | facturation | La demande facturation porte sur un identifiant de commande qui n'est pas disponible (uuid), une demande de facturation doit porté sur une animations (ces lots). Chaque demande doit être consultable pour voir si l'ensemble des factures relatibes aux lots d'animation sont disponible ou sinon il doit être possible de consulter l'état des demandes et de les relancers. Un état général sur le dossier doit permettre de savoir si il est complet (toutes les factures sont recues) ou non | Interface corrigée et testée. Complément backend de relance et de complétude préparé et testé ; autorisation explicite requise pour son application après refus du contrôle automatique. Voir docs/specifications/ano-ani-02-facturation-animation.md. |
| ANO-ANI-03 | Origine API HTTPS explicite obligatoire. lors du build pour déploiement dans Re,der | A corriger |
