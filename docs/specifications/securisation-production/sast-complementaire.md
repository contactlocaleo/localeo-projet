# Verification SAST complementaire

Le scan Bandit effectif a revele deux resumes back-office qui interpolaient sans
echappement le nom, la ville, le type ou le contact. Ces champs sont maintenant
echappes avant construction du HTML de confiance. Deux tests injectent des balises
dans tous ces champs et verifient leur affichage comme texte.

Les autres alertes B704 examinees concernent des libelles passes a `escape`,
des fragments issus des helpers HTML internes, des identifiants UUID/nombres,
ou les SVG produits exclusivement par qrcode. Les exceptions locales nomment
B704 et leur justification ; aucun test Bandit n'est desactive globalement.
Toute introduction d'une nouvelle donnee editable dans ces fragments exige un
echappement et un test de regression. Les metadonnees JSON restent echappees.

Deux alertes B608 sont des faux positifs : le document HTML/JavaScript de la PWA
n'est jamais execute comme SQL ; les clauses du compteur de moderation sont
des constantes du code choisies d'apres les colonnes presentes, sans donnees
utilisateur concatenees. Les exceptions sont limitees a ces expressions.
