# Localeo V25 - Objets de valeur

Cette version ajoute `app/domaine/value_objects.py`.

## Objets de valeur introduits
- `Email`
- `NumeroTelephone`
- `CodePostal`
- `MontantEuroCentimes`
- `QrToken`
- `VersionCarteCommercant`

## Intégration
Les entités du domaine dans `app/domaine/modeles.py` utilisent désormais ces objets de valeur.
Les mappers ORM <-> domaine gèrent la conversion.
L'API publique reste inchangée.
