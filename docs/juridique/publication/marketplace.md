# Publication juridique centralisee

Les PDF de reference du depot backend sont l'unique source editoriale. Le backend
prepare les blocs de lecture et l'HTML depuis ces PDF, puis publie une edition
coherente. La Marketplace et Localeo Live consultent ce catalogue a l'execution :
une nouvelle edition ne demande plus de reconstruire leur bundle.

## Contrat public

Les appels sont centralises dans src/services/api.js et utilisent uniquement la
base LOCALEO_API_BASE_URL configuree pour l'environnement. Ils n'envoient ni
Authorization ni identifiant d'installation Live.

- GET /public/documentaire/juridique/catalogue?surface=marketplace|live :
  schema_version, environment, release_id, published_at et items.
- Chaque item fournit id, title, language, version, render_revision,
  document_date, effective_date, kind, surfaces, empreintes HTML/PDF et URL
  immuables detail_url, pdf_url, html_url, ainsi que history_url et related_ids.
- detail_url : metadata de la meme edition et sections de blocs structures.
- GET /public/documentaire/juridique/documents/:id/versions?surface=... :
  items et current (version, render_revision).

Le lecteur React echappe les textes. Il n'injecte pas l'HTML renvoye par une API.
Les paragraphes, titres, listes, tableaux et liens libelles sont derives du PDF.
Les tableaux acceptent header_rows (0 ou 1), cell_links (indices row/column) ;
marker_in_text evite d'ajouter une puce a une liste deja numerotee dans le PDF.
Les plages de liens utilisent des offsets UTF-16 [start, end).

## Routes et navigation

- /juridique : index Marketplace.
- /juridique/:documentId : edition courante.
- /juridique/:documentId/versions : historique.
- /juridique/:documentId/versions/:version/:renderRevision : lecture immuable.
- Les memes routes sous /live/juridique conservent le retour vers Live.
- /mentions-legales, /confidentialite, /cookies, /accessibilite, /cgv,
  /retractation, /conditions-utilisation et /confidentialite-live restent des
  alias vers l'edition courante.

Les routes juridiques Live sont montees dans App.jsx, hors du composant LiveApp :
elles ne creent pas d'installation ni de carnet. Les reglages et la politique de
confidentialite Live proposent des liens vers ce lecteur public.

Le lien /retractation reste la lecture du document. Le depot d'une declaration
de retractation releve du parcours metier distinct de l'epic 64.

## Versions, erreurs et archives

Le catalogue est revalide a l'ouverture. Une fois choisie, l'edition de lecture
est fixee ; son detail est charge par son URL immuable et les identifiants,
revisions, empreintes et URL PDF sont compares avant affichage. Une publication
concurrente ne doit pas modifier le PDF associe au texte en cours de lecture.

Une indisponibilite du catalogue, un document absent ou un detail incoherent
produit un etat explicite. Aucun ancien JSON local n'est presente en secours
comme edition courante. Le service worker Live ne met pas les API documentaires
dans son cache public.

Les huit PDF historiques public/legal/v1 et les deux public/legal/v1.1 restent
inchanges. server.cjs conserve un vrai 404 pour un fichier /legal absent.
Le JSON historique src/content/legalDocuments.v1.json n'est plus importe par le
lecteur ; il sert uniquement aux fixtures de regression. L'ancien importeur
DOCX scripts/import-legal-documents.ps1 est desactive pour proteger les archives.

Le telechargement pointe vers pdf_url : le backend sert le PDF original avec
Content-Type application/pdf et Content-Disposition attachment, y compris
lorsque son origine differe de celle de l'application.

## Verification

Tests navigateur cibles :

    npx playwright test --config=playwright.desktop.config.cjs tests/visual/legal-central.spec.cjs tests/visual/premium-trust.spec.cjs

Le harnais isole intercepte explicitement le service documentaire et ne contacte
aucun backend reel. Les cas couvrent index, alias, archives, erreurs, version de
lecture, URLs de l'environnement, tableaux/liens et acces Live sans installation.

Completer par ESLint sur les fichiers modifies, npm run build et le test serveur
des PDF publics. La recette distante apres deploiement doit controler l'edition
et l'empreinte du PDF reellement servi sur chaque surface ; un push ou le SHA de
l'application ne suffit pas a prouver une publication documentaire.

Le service Render exact et son lien branche/environnement se verifient dans la
configuration de deploiement. Le depot documente le Web Service, npm ci puis
npm run build et npm start, mais ne fournit pas de workflow prouvant le mapping
automatique de main vers le site de test.

La qualification sur un lot PDF reel est facultative dans la suite quotidienne :
definir LOCALEO_LEGAL_TEST_LOT avec le chemin du lot.json prepare par le backend,
puis executer tests/visual/legal-pdf-derived.spec.cjs avec la meme configuration.
Ce test lit le lot externe sans copier ses textes dans ce depot. Il compare
tous les blocs et cellules, les liens libelles et le SHA du PDF telecharge ;
il produit aussi des captures desktop et mobile.

La recette automatique dispose d'attributs stables : l'index porte
data-legal-surface, l'article data-legal-document-id, data-legal-version et
data-legal-render-revision, et le lien PDF du lecteur data-legal-pdf.
