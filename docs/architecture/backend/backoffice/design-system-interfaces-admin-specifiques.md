# Design system des interfaces d'administration spécifiques

Toutes les pages HTML produites par `app.infrastructure.admin.admin` et toutes les interfaces SQLAdmin utilisent le même langage visuel Localeo. Cette règle couvre les dashboards, visions 360, consoles Animation, timeline support, procédures de correction, formulaires de secours, écrans documentaires et vues issues des modèles SQLAlchemy.

## Principes communs

- barre de navigation persistante vers la console SQLAdmin, le dashboard, le territoire, le support et les procédures ;
- bleu Localeo comme accent d'action principal, orange réservé à l'accent de marque et rouge aux opérations dangereuses ;
- largeur de travail commune, espaces et rayons homogènes ;
- tableaux défilables horizontalement, en-têtes fixes et survol lisible ;
- champs, boutons, onglets et feedbacks suivant les mêmes dimensions ;
- focus clavier visible, responsive mobile et respect de `prefers-reduced-motion` ;
- barre d'administration masquée à l'impression, notamment pour les QR codes et documents.

Le design system est injecté par la classe `HTMLResponse` locale. Une nouvelle vue spécifique qui retourne cette réponse bénéficie donc immédiatement du shell. Il ne faut plus recopier un nouveau thème complet dans un renderer ; le CSS local doit uniquement décrire une disposition propre à son métier.

Le shell ne présente qu'un seul en-tête. Le titre de la vue spécifique est affiché à côté de la marque Localeo et ses liens ou actions contextuels sont intégrés à la navigation principale. Les routes globales correspondent directement aux chemins exposés par les `BaseView` SQLAdmin ; elles ne doivent pas répéter le nom de la méthode exposée.

L'identité visuelle du backoffice utilise `assets/localeo-administration-icon.png` dans le header des vues spécifiques et la navigation SQLAdmin. Le favicon commun provient de `assets/localeo-administration-favicon-64.png`. Il est exposé sur le chemin conventionnel `/favicon.ico`, utilisé aussi par l'accueil backend et Swagger UI. Les URLs injectées sont versionnées pour invalider le cache favicon des navigateurs locaux ; les fichiers restent exposés en lecture seule et ne doivent pas être dupliqués dans les templates.

## Interfaces SQLAdmin et SQLAlchemy

Le template `templates/sqladmin/layout.html` charge `_localeo_design_system.html` pour toutes les listes, fiches détail, créations et modifications générées par SQLAdmin. Le socle uniformise également les filtres, recherches, actions groupées, tableaux, formulaires, pagination, modales et messages de retour.

Les templates métier existants héritent du même layout :

- référentiels ville, commerçant, coffret et prestation ;
- bibliothèque et téléversement de médias ;
- gestion des emails, SMS et notifications WebPush ;
- reversements et assistants métier associés.

Les extensions métier utilisent les composants communs selon leur rôle : `localeo-template-actions` pour les actions de liste, `localeo-extension-section` pour un bloc de formulaire, `localeo-helper-row` pour une aide contextuelle et `localeo-media-choice` pour la sélection d'un média. Leur JavaScript ne doit pas redéfinir les couleurs, boutons, champs ou conteneurs du design system.

## Hiérarchie d'une page

1. navigation globale commune ;
2. titre et contexte du périmètre ;
3. feedback éventuel ;
4. action ou information principale ;
5. détails secondaires et historique.

Les animations sont courtes et fonctionnelles : entrée légère, survol des lignes et retour d'affordance des boutons. Elles sont désactivées lorsque le système demande une réduction des mouvements.
