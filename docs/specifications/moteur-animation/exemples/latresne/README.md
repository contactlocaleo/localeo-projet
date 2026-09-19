# Exemple de préparation de chasse — Latresne

- [Prompt à envoyer avec le schéma](prompt-complet.md).
- [Schéma de réponse — entrée documentaire de la spécification](../../contrats/reponse-generation-chasse.schema.json).
- [Requête exportée](requete-exemple.json).
- [Proposition avec deux missions par commerce](animation-generee.json).
- [Maquette navigable Localeo Live](maquettes-live/index.html) et [guide UX](maquettes-live/README.md).
- [Illustrations WebP en base64](animation-generee.json) : tableau `medias` du résultat de génération.
- [Spécification du workflow](../../localeo_animation_engine_spec.md#811-préparation-et-choix-des-missions-commerçantes).

## Ce que représente cet exemple

La réponse est une proposition de préparation, pas une chasse jouable ni un engagement réel. Pour Halloween, elle comporte six positions, trois commerces et deux missions candidates pour chacun. Dates illustratives : 31 octobre 2026 de 14 h à 18 h ; environ 60 minutes par groupe. Aucun commerçant n’a été sollicité par cette opération documentaire.

| Commerce | Mission A à confirmer | Mission B à confirmer |
| --- | --- | --- |
| Lisons sous la pluie | Présenter un livre et les fragments du conte fournis. | Placer un marque-page codé dans l’enveloppe du présentoir du jeu. |
| Mirga | Présenter un fromage de chèvre et un de vache avec les repères convenus. | Placer un message sous le rabat d’une carte de menu fictif. |
| Mode de Biche | Présenter un article 100 % coton, composition visible. | Placer un message derrière une fleur en carton du jeu. |

Ces ressources sont **demandées sous condition**, pas déclarées présentes en magasin. L’organisateur relit, ajuste et valide les propositions avant l’envoi. Le commerçant accepte en choisissant une mission et en confirmant chaque élément nécessaire, ou refuse. La réalisation est ensuite vérifiée avant publication. L’organisateur fixe un minimum de commerçants pour chaque chasse. Si le nombre de commerces retenus avec accord valide et mission confirmée est inférieur à ce minimum, la publication est bloquée : il choisit d’adapter ou d’annuler, sans annulation automatique. Ce seuil de préparation est conservé côté serveur, pas fixé dans la réponse IA ; atteindre le minimum ne dispense pas des autres contrôles. Les décisions et confirmations sont conservées côté serveur, hors réponse IA.

## Schéma et champs

Une étape commerçante contient `lieu`, `titre`, `missionsProposees` (une à deux alternatives, deux souhaitées). Chaque mission a son identifiant, sa `preparationCommercant`, ses textes joueur, `interactionCommercant`, `consigneCommercant` et son défi. Le champ `supportAFournir` contient le texte exact à préparer, ou null. `elementsAConfirmer` liste les engagements demandés, jamais leurs confirmations effectives. Aucun identifiant de mission retenue ou statut d’accord ne figure dans la sortie IA.

`interactionCommercant` est le dialogue facultatif proposé au joueur ; `consigneCommercant` est le texte privé adressé au commerce et peut inclure un code ou une mise en place à préserver. La conversation peut être facultative alors que la préparation est indispensable. Le commerçant ne valide pas la réponse du joueur : le moteur conserve correction, aides et preuve de passage séparées.

Les étapes POI/virtuelles gardent leur contenu unique, avec consigne commerçant nulle. Les cinq types de défi sont inchangés. Le schéma contrôle la structure ; le domaine devra contrôler unicité des missions, références, cohérence des supports/solutions, version, confirmations et publication.

## Thème et illustrations

Le contrat conserve `themeVisuel` à l’animation : titres Oswald, corps DM Sans, papier clair, bleu nuit et orange Localeo. Chaque position référence une intention d’image WebP 16:9 dans `presentation.illustration`. Les trois commerces possèdent un visuel neutre commun aux deux missions ; une mission pourrait le remplacer dans sa propre `presentation`, ou le supprimer avec `illustration: null`. Mirga surcharge seulement la couleur `fond` ; les autres propriétés héritent du thème commun. La finale réutilise explicitement l’image de couverture.

Les six identifiants de médias sont `visuel-couverture`, `visuel-gare`, `visuel-librairie`, `visuel-fromagerie`, `visuel-boutique` et `visuel-salargue`. La demande de génération livre maintenant récit et images ensemble, avant le choix des missions. Dans cet exemple, les six illustrations déjà produites avec `imagegen` ont été recompressées et intégrées à `medias[].base64` ; elles ne sont pas régénérées artistiquement. Chaque image est stockée une seule fois et reliée aux étapes par son identifiant. Aucun manifeste ni fichier WebP externe n’est nécessaire à la maquette. Les [prompts exacts de création](medias/prompts-generation.json) restent conservés pour la traçabilité. Les prompts ne comportent ni code, ni réponse, ni lieu futur. Le visuel de Salargue conserve un ciel sans astre pour préserver l’énigme.

Ces illustrations représentent une fiction : elles ne certifient pas la devanture, le stock ni la participation des commerces réels. Les informations nécessaires aux défis restent dans les textes et les supports à confirmer. La couverture ne révèle pas les lieux suivants. Voir [le contrat de présentation et son cycle de préparation](../../localeo_animation_engine_spec.md#812-thème-visuel-et-illustrations-de-lanimation).

### Poids des illustrations embarquées

Budget : **60 000 octets maximum par objet média JSON compact**, base64 et métadonnées compris ; cible d’environ 50 Ko. Le binaire WebP est limité à 44 000 octets pour tenir compte de la hausse de taille du base64.

| Image | Résolution | WebP binaire | Objet JSON avec base64 |
| --- | --- | --- | --- |
| `visuel-couverture` | 768 × 432 | 43 638 o | 58 363 o |
| `visuel-gare` | 640 × 360 | 43 794 o | 58 565 o |
| `visuel-librairie` | 768 × 432 | 43 888 o | 58 698 o |
| `visuel-fromagerie` | 768 × 432 | 43 854 o | 58 651 o |
| `visuel-boutique` | 640 × 360 | 43 518 o | 58 201 o |
| `visuel-salargue` | 768 × 432 | 42 920 o | 57 405 o |

Le JSON total est plus lourd que chaque image : les six médias sont nécessaires pour représenter toute la chasse. Le serveur de production ne transmettra que les images autorisées à l’étape du joueur.

## Du parcours proposé au parcours joué

L’ordre de `etapes` est l’ordre proposé. Deux missions pour un commerce comptent comme une seule position, pas deux étapes. Après réponses et relecture finale, l’assemblage garde seulement la mission acceptée de chaque commerce retenu. La mission B n’est jamais un repli automatique après un refus de A. Les commerces refusés sont retirés ou remplacés explicitement avec révision du récit et nouvelles invitations si nécessaire.

Le moteur crée ensuite `startStepId` et les liens `transitions[].targetStepId`, avec `location.refId` pour chaque lieu. Le lieu de l’élément suivant est la prochaine destination, révélée à son déblocage. Les alternatives, supports privés, refus et accords ne sont pas envoyés au joueur. Les contenus candidats ne doivent pas être affichés avant que leurs conditions soient confirmées et la chasse publiée.

## Envoi au LLM et traçabilité

Pour un essai manuel, envoyer [le prompt](prompt-complet.md) et [le schéma de réponse](../../contrats/reponse-generation-chasse.schema.json). L’export JSON regroupe messages, schéma et métadonnées ; seuls `messages_json` et `response_schema_json` constituent la charge utile décrite. Empreinte SHA-256 : `458eb65cdeda23f5c8b2fdd10e0335e6b64323b31a005874d7436058ee2ddecd`. Cette révision 8 conserve les missions alternatives de la révision 7 et embarque les illustrations dans le résultat JSON de génération. La réponse a été rédigée dans la conversation ; aucun appel par le moteur, aucune invitation réelle et aucune publication n’ont été exécutés.

La spécification et les schémas restent une cible documentaire ; les validations opérationnelles, projections et interfaces sont à implémenter. Les accords et contrôles réels restent dans la préparation serveur, tandis que le LLM peut proposer les exigences à confirmer. Les sources locales conservées ci-dessous identifient les lieux ; elles ne prouvent ni leur participation ni la disponibilité des produits demandés.

## Sources locales conservées hors prompt

- [Ancienne gare de Latresne — donnée Office de tourisme de l’Entre-deux-Mers diffusée sur Cirkwi](https://www.cirkwi.com/fr/point-interet/882729-ancienne-gare-de-latresne) — consulté le 19 septembre 2026.
- [Site de la librairie Lisons sous la pluie](https://lisons-sous-la-pluie.fr/) — consulté le 19 septembre 2026.
- [Annuaire municipal des commerces de Latresne](https://www.mairie-latresne.fr/commerces-entreprises-et-artisans/) — consulté le 19 septembre 2026.
- [Annuaire des entreprises — établissement Fromagerie Mirga Latresne](https://annuaire-entreprises.data.gouv.fr/entreprise/949096861) — consulté le 19 septembre 2026.
- [Site de Mode de Biche](https://modedebiche.fr/) — consulté le 19 septembre 2026.
- [Inventaire du patrimoine — Château de la Salargue, notice IA00056818](https://pop.culture.gouv.fr/notice/merimee/IA00056818) — consulté le 19 septembre 2026.
