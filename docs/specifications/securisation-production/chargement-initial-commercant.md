# F13 — Chargement différé du scanner

Le scanner Coffret et Animation est chargé dans un module JavaScript distinct, uniquement à l'ouverture de la rubrique Scanner. L'accueil et la connexion ne téléchargent pas ce module. Un état de chargement accompagne la navigation ; les règles de validation et d'annulation restent inchangées et leurs fonctions partagées sont isolées dans `features/validation/workspaceModel.jsx`.

Le profil, la page publique, les prestations et le contact suivent la même règle de chargement à l'ouverture. Leurs fonctions de préparation des données sont séparées des composants dans `features/workspaces`. Le test navigateur parcourt ces quatre rubriques avec des réponses synthétiques.

Le logo d'en-tête et les polices principales du texte et des titres sont préchargés dès le HTML afin d'éviter leur découverte tardive après exécution de l'application. Le build réécrit les URLs des polices vers les fichiers fingerprintés ; aucune ressource distante n'est introduite.

Le mot « Pro » utilise un sous-ensemble local des mêmes glyphes Caveat, généré par `scripts/subset-wordmark.py`. La licence OFL et le copyright sont conservés avec le fichier. La police complète reste utilisée pour les signatures et textes libres ; le sous-ensemble ne doit jamais leur être appliqué.

Validation : le parcours navigateur mobile vérifie l'absence de téléchargement du scanner sur l'accueil, puis son chargement unique et son affichage après navigation. Les budgets Lighthouse existants sont rejoués sur trois mesures du build compressé.
