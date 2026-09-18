# Documents juridiques publics — lecteurs Commerçant et Animation

> Consolidation documentaire du 18 septembre 2026 : les deux guides identiques hors paramètre `surface` sont réunis ; chaque surface reste explicitement définie.

Les PDF de reference sont publies par le backend commun. Les applications Commerçant et Animation lisent leur representation structuree et telecharge le PDF original ; aucun texte juridique n'est maintenu dans le frontend.

## Routes et catalogue

- `/juridique` : documents distribues a cette plateforme.
- `/juridique/:id` : edition courante, resolue une fois par consultation.
- `/juridique/:id/versions` : historique public.
- `/juridique/:id/versions/:version/:revision` : edition immuable et son PDF associe.

Le lecteur est selectionne avant le montage des hooks de session. Une session expiree, une verification de session indisponible ou un compte en preparation ne doivent pas bloquer ces routes. Il n'existe aucune acceptation juridique globale ajoutee a la connexion.

L’API est `GET /public/documentaire/juridique/catalogue` avec le paramètre de surface correspondant :

| Application | Paramètre |
| --- | --- |
| Localeo Commerçant | `surface=commercant` |
| Localeo Animation | `surface=animation` |

Les URL immuables du détail et du PDF sont fournies par le catalogue. Les lectures publiques omettent cookies et Authorization. Le catalogue et l'historique sont relus sans cache ; les editions et PDF suivent les directives de cache du serveur. Une panne produit une erreur explicite avec reessai, sans remplacer silencieusement le document par une ancienne copie.

Le PDF est telecharge par fetch puis Blob afin de fonctionner entre origines. Le type application/pdf et la signature %PDF- sont controles. Le serveur doit autoriser l'origine frontend dans sa politique CORS. La verification operateur centrale compare aussi le SHA-256 du PDF servi avec le PDF source.

## Contenu

Le lecteur rend les titres, paragraphes, listes, tableaux et liens issus du PDF. Les textes passent par React et ne sont jamais injectes en HTML brut. Les liens acceptent uniquement http, https et mailto ; les offsets des annotations sont des indices UTF-16. Les tableaux acceptent header_rows:0|1 et cell_links. Une liste portant marker_in_text conserve ses marqueurs sources sans seconde puce.

Les modeles sont signales comme vierges a completer. Les contrats signes, dossiers propres au commercant/partenaire et reglements particuliers des animations restent dans leurs parcours existants. Les annexes internes ne font pas partie de ce catalogue public.

## Configuration et recette

Utiliser la configuration d'URL backend habituelle de la plateforme ; aucun nouveau secret n'est necessaire. Le premier deploiement doit rendre ces lecteurs disponibles et le lot documentaire test doit etre publie avant la recette distante. Une publication de texte ulterieure ne requiert pas de redeploiement frontend.

Verifier sans session, avec une session expiree, sur mobile et au clavier : index, edition, sommaire, tableaux, liens, mention modele, archives et PDF. Rendre l'API de session indisponible pendant la consultation ne doit provoquer aucun appel a cette API. Verifier aussi le cas d'une API documentaire en panne et d'un document404, ainsi que la correspondance version/empreinte HTML-PDF lors d'une publication concurrente.

Les URL PDF sont celles du backend ; aucun fichier PDF juridique n'est ajoute sous une route statique susceptible de renvoyer le HTML de l'application a la place d'un fichier absent.

Le controle de publication utilise data-legal-surface sur le conteneur, data-legal-document-id / data-legal-version / data-legal-render-revision sur le lecteur charge, et le href exact du lien a[data-legal-pdf]. Il doit aussi constater les sections du document, et ne doit jamais se limiter a un HTTP200 du serveur SPA.
