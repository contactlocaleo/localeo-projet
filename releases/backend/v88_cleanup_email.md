# V88 - Nettoyage final Email

## Actions réalisées
- renommage ServiceEmail -> ServiceEnvoiEmail
- suppression notion envoi direct dans le code métier
- clarification rôle : uniquement utilisé par batch

## Résultat
Architecture clean :
- use cases -> EmailSortant
- batch -> ServiceEnvoiEmail
