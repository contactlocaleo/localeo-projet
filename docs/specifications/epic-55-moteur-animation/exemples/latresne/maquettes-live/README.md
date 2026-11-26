# Maquettes Localeo Live — La lanterne de Gaspard

## Ouvrir la démonstration

Ouvrir [index.html](index.html) dans un navigateur, puis **Commencer la démonstration**. Aucun serveur, compte, build, CDN ou appel API n’est nécessaire. Les illustrations sont embarquées en base64 dans le JSON de l’animation et sa fixture ; aucun fichier image externe ni manifeste n’est nécessaire au déroulement.

Le parcours est : [Découvrir](decouvrir.html) → [Inscription](inscription.html) → [Mon carnet](carnet.html) → [Chasse](chasse.html) → [Bilan](bilan.html). Les liens directs respectent l’état courant ; le guide permet d’initialiser un scénario précis. L’adresse `camille@example.test` est fictive.

Le bandeau **Simuler** est un outil de recette hors parcours joueur. Il permet de changer d’étape, confirmer un passage en jouant le rôle du commerçant, consulter le support supposé présent en boutique, couper le réseau ou perdre une réponse serveur. Les raccourcis remplacent la progression de démonstration. Une réinitialisation ne touche que les données de cette maquette.

## Animation utilisée

La [proposition de préparation](../animation-generee.json) reste le document éditorial de référence. La maquette suppose fictivement que les trois commerces ont accepté leur **mission A**. Elle assemble les six positions dans [parcours-demo.json](parcours-demo.json), sans publier d’événement ni solliciter de commerçant. Le scénario « Saisir un code » substitue uniquement la mission B de Mode de Biche, comme une autre édition préparée ; le joueur ne choisit jamais une alternative pendant la chasse.

| Position | Lieu | Composant |
| --- | --- | --- |
| 1 | Ancienne gare | Scan du QR du lieu, récit, `INFORMATION`, confirmation explicite. |
| 2 | Lisons sous la pluie | `ORDERING` : fragments déplaçables avec boutons haut/bas, utilisables au clavier. |
| 3 | Mirga | `ASSOCIATION` : un choix pour chaque repère, bijection complète. |
| 4 | Mode de Biche | `SINGLE_CHOICE` : une seule réponse ; variante `TEXT_INPUT / CODE`. |
| 5 | Château de la Salargue | QR du lieu puis `TEXT_INPUT / TEXTE`. |
| 6 | Finale virtuelle | `INFORMATION`, aucun nouveau déplacement, bilan. |

Pour aller vite : la librairie se résout dans l’ordre boîte → clé → citrouille → confettis ; Mirga associe LUNE à chèvre et SOLEIL à vache ; Mode de Biche attend Coton (variante : `MOD-031`) ; Salargue attend `lune`. Ces solutions appartiennent uniquement au support de recette.

## Thème et médias pilotés par les données

- `themeVisuel` dans l’animation déclare les couleurs, polices enregistrées et l’illustration de couverture.
- `presentation` sur chaque position ou mission déclare son illustration et ses surcharges. Mirga illustre un fond bleu clair hérité avec les autres tokens inchangés.
- Le parcours assemblé conserve ces déclarations. Le faux serveur filtre la présentation de l’étape courante ; l’UI ne contient aucun visuel d’Halloween codé en dur.
- Les identifiants sont résolus dans `medias[]` du [JSON de l’animation](../animation-generee.json). Les images WebP sont stockées en base64, une seule fois par identifiant ; chacune tient dans un objet JSON compact de moins de 60 000 octets. La maquette construit des sources `data:image/webp;base64,…`, avec dimensions explicites et largeur adaptative. La projection du faux serveur ne renvoie que la couverture et le média de l’étape autorisée.
- Aucune image d’étape future n’est chargée dans le rendu joueur. Une étape POI ne montre son illustration qu’après son scan. Une image absente ou `null` ne reçoit aucun décor de remplacement ; son échec de chargement laisse le texte et le jeu utilisables.
- Le shell de marque, les pictogrammes de navigation et les contrôles QR sont des composants fonctionnels Localeo Live. Les seuls **visuels narratifs** sont ceux déclarés dans l’animation.

Les six illustrations ont été produites avec l’outil intégré `imagegen`, puis optimisées en WebP et intégrées en base64 dans le JSON. Dans l’exemple révisé, les images existantes ont été recompressées ; la cible moteur génère désormais récit et images dans la même demande, avant les choix de missions. Les [prompts exacts de production](../medias/prompts-generation.json) sont conservés pour la traçabilité ; ils détaillent les intentions de `animation-generee.json`. Ce sont des scènes fictives, pas des photographies documentaires des commerces de Latresne. Les textes et les supports de mission restent la source du défi.

Le preset reprend les tokens actuels de Localeo Live : bleu `#0b3d63`, encre `#082840`, orange `#f28a2e`, papier `#f6f5f1`, DM Sans et Oswald. Les fontes locales sont accompagnées de leurs licences dans `assets/`. Contrôles rectilignes, cibles tactiles d’au moins 44 px, focus visible, dialogues natifs, annonces de statut et réduction des animations sont inclus.

## États à implémenter

| Situation | Comportement observable dans la maquette |
| --- | --- |
| Inscription | Majorité et règlement requis ; ajout dans Mon carnet. Authentification supposée acquise. |
| QR de lieu incorrect | Message d’erreur, aucune progression ni tentative consommée. |
| Défi avant passage | Bonne réponse conservée, suite bloquée tant que le commerce n’a pas attesté le passage. |
| Passage avant défi | Attestation conservée, défi restant à résoudre. |
| QR du joueur | Action volontaire, vérification de l’appareil simulée, QR non scannable, attente d’une attestation distincte. |
| Réponse incorrecte | Message, nouvelle tentative, accès à l’indice et à l’aide complète. |
| Réponse invalide | Compléter/corriger la saisie, aucun essai et aucune aide débloquée. |
| Indice | Révélé après une erreur valide, sans résoudre le défi. |
| Solution demandée | Confirmation explicite, défi terminé sans pénalité ; preuve toujours requise. |
| Chargement | Latence de 500 ms, double action bloquée, statut annoncé. |
| Hors connexion | Actions serveur bloquées, saisie conservée dans l’onglet, reprise volontaire. |
| Réponse serveur perdue | Dernière vue confirmée conservée ; vérification du résultat avant toute nouvelle action, sans renvoi. |
| Neutralisation | Dispense globale simulée, distincte de la preuve ; poursuite explicite. |
| Régularisation | Histoire terminée mais participation incomplète ; nouvelle preuve pour le commerce concerné, sans rejouer le défi. |
| Avant le début / clôture | Accès au carnet, jeu bloqué. |
| Fin | Participation qualifiée uniquement après tous les défis et passages requis. Aucun gain fictif promis. |

## Structure et limites

`donnees-demo.js` est la copie de travail du parcours assemblé et de ses médias base64 ; elle permet l’ouverture locale sans `fetch`. `simulateur.js` joue le rôle du serveur : état, correction, preuves et projections. `app.js` rend les pages et leurs composants. `styles.css` contient la présentation commune, complétée par les tokens des données.

La progression se conserve dans le stockage local du navigateur ; les brouillons de réponse sont limités à l’onglet et à l’étape/version. Si le navigateur interdit tout stockage local, le repli mémoire ne survit pas à une navigation entre pages : ouvrir le dossier via un serveur statique local dans ce cas. Chromium a été vérifié en ouverture directe des fichiers.

La fixture et les médias complets sont inspectables dans cette **maquette statique**, y compris les solutions : ils ne doivent jamais être distribués ainsi en production. Le vrai serveur devra appliquer les projections, contrôles d’accès aux médias, idempotence, transactions, versions et règles métier de la [spécification](../../../localeo_animation_engine_spec.md#812-thème-visuel-et-illustrations-de-lanimation). Aucun véritable scan, WebAuthn, email, stockage serveur, contrôle terrain ou appel fournisseur n’est exécuté par la maquette. Les temps de marche, horaires et conditions d’accès ne sont pas validés par ce support.

## Vérifications réalisées

Le simulateur fait l’objet de contrôles de correction, preuves, aides, reprise et projections. Le parcours est également joué avec Chromium sur les cinq composants, les profils TEXTE/CODE, les états réseau et la régularisation. Le rendu est contrôlé aux largeurs 320, 390 et 1280 px ; les [captures](captures/00-guide-desktop.png) fournissent quelques états de référence. Les base64 sont décodées en vrais WebP, leurs dimensions, poids binaire/JSON et empreintes vérifiés ; le schéma, sa copie dans la requête et l’empreinte de cette dernière sont contrôlés séparément.

Ces vérifications portent sur le support UX. Elles ne valent pas recette du backend de production ni audit d’accessibilité complet.
