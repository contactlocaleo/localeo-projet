# Localeo V76 - Correctif runtime

## Correctif appliqué
- suppression de l'import invalide `MontantEuro` dans `app/application/use_cases/valider_prestation.py`
- réalignement avec le modèle actuel de reversements qui utilise `MontantEuroCentimes`

## Cause
`app.domaine.reversements` n'expose pas `MontantEuro`, seulement `MontantEuroCentimes`.

## Impact
Corrige l'erreur d'import au démarrage observée sur la V75.
