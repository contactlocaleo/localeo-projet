# Arbitrages des maquettes — étape 3

18 novembre 2026. **Propositions isolées, réactions simulées, aucune autorisation de développement.** [Galerie](comparatif-avant-apres.html) · [Revue contradictoire](revue-contradictoire.md) · [Backlog voté](../workshop/backlog-ux.md).

## Périmètre et parti visuel

Seules B1, C1, D1, E1 et F1 sont représentées : cinq P1 avec au moins sept voix sur douze. Aucun P0 établi ; A1 et G1 restent hors périmètre P2. Aucun tutoriel imposé, aucune validation automatique, aucune fusion des états métier, aucun succès hors connexion.

Parti visuel : conserver le cadre opérationnel calme de Pro, ses surfaces claires, son en-tête marine et son action principale verte. Hiérarchie : contexte, état, prochain geste, puis détails accessibles. Interactions de présentation : bascule Avant/Après sur mobile, sélection d’un état et d’un format, dépliage des détails ; pas de mouvement décoratif. Le skill frontend a été appliqué à ce périmètre d’application existante, avec priorité à la fidélité demandée.

**OBSERVÉ dans le code et les captures** : fond `#f5f7f9`, texte `#183243`, texte secondaire `#526575`, bordure `#d8e1e7`, accent `#09685e`, fond actif `#e1f0ec`, en-tête `#123247`, rayons de panneau 12 px et de bouton 9 px, police système. Sources : `localeo-commercant/src/styles.css`, `src/app/ApplicationFrame.module.css` et captures 03/10. Le symbole `header-mark.svg` est copié depuis l’application. Le mot-symbole et la galerie utilisent la police système comme le composant actuel. Aucun changement de charte.

## Traçabilité AVANT / APRÈS

| Orientation | Vote simulé initial | Preuve réelle et zone | Proposition et limite |
| --- | --- | --- | --- |
| B1 · P1 · M | 11 / 1 / 0 | O04/C02 : [erreur QR](captures-avant/19-scanner-erreur-locale-mobile.png), encadré « pack » ; [scanner](captures-avant/04-scanner-mobile.png). | Huit états : scan indisponible, rejet local, confirmation, succès, doublon, refus temporel, réponse perdue, vérification impossible. Les résultats serveur n’ont pas été observés sur le compte. |
| C1 · P1 · M | 12 / 0 / 0 | O05 : [boîte réelle](captures-avant/09-notifications-generales-mobile.png), PIN vide puis Animation. | Information non lue et cas fictif de tâche encore ouverte après lecture. L’action ne peut être déduite du seul texte ou du non-lu. |
| D1 · P1 · L | 9 / 0 / 3 | O02/O03/O06/O07/C04 : [accueil](captures-avant/03-accueil-pro-mobile.png), [liste 3](captures-avant/05-animations-mobile.png), [prêt](captures-avant/16-preparation-vitrines-mobile.png). | Accueil, incomplet, attente d’approbation et prêt. Compteurs illustratifs ; états incomplet/attente non reproduits sur le compte. |
| E1 · P1 · M | 12 / 0 / 0 | O08/C03 : [guide](captures-avant/21-guide-preparation-mobile.png), période ISO et consignes. | Kit et gestes regroupés, un seul flyer cité par le guide. Ni PDF ni impression vérifiés. |
| F1 · P1 · L | 12 / 0 / 0 | O09/C05 : [rechargement immédiat](captures-avant/20-retour-rechargement-mobile.png). | Retour, expiration, interruption avant confirmation. L’AVANT ne constitue pas une preuve du comportement après plusieurs semaines. |

Les captures nécessaires à chacune des cinq orientations existaient déjà : aucune nouvelle connexion ou action distante n’a été nécessaire. Les 22 fichiers AVANT sont conservés sans modification. Aucun écran synthétique n’est placé dans ce dossier. Les états complémentaires APRÈS n’ont pas d’équivalent réel disponible : la galerie l’indique explicitement, sans inventer de capture de succès ou de panne. Un QR participant de test autorisé et un protocole de recette seront nécessaires pour les comparer réellement.

## Arbitrages complémentaires après les douze avis simulés

| Réf. | Objection ou besoin | Décision dans les maquettes finales | Portée |
| --- | --- | --- | --- |
| M01 · B1/F1 | Julien, Hugo et Opérations : que faire si la vérification reste impossible ? | Ajout de l’état « Résultat toujours inconnu » : ne pas relancer, informer le participant, rétablir la connexion, vérifier de nouveau, accès à l’aide. | Précise l’incertitude déjà adoptée ; aucune nouvelle règle ni mutation. |
| M02 · E1 | Claire et Martine : « 19–23 » peut être compris comme tout le 23. | Fin à 0 h affichée hors accordéon : « dans la nuit du 22 au 23 ». Début et détail horaire conservés. | Conversion fidèle des instants observés, sans décider d’une borne inclusive/exclusive métier. |
| M03 · C1 | Isabelle : une action lue peut disparaître parmi les anciens messages. | Repère « Actions attendues » et maquette distincte « Message lu / Action attendue ». Lire ne termine pas la préparation. | La disponibilité d’un état de tâche fiable conditionne ce repère. Pas de relance push. |
| M04 · D1 | Trois abstentions initiales, Claire et Martine : trop de statuts. | Un seul état principal et un geste ; détails de participation dans un accordéon. Le cas prêt conserve les attestations, contrôle et version. | Aucun état métier fusionné ni nouveau. |
| M05 · B1 | Patrick : la confirmation ralentit la file. | Confirmation maintenue avec contexte court et bouton explicite ; reçu et explications secondaires en détail. | Désaccord conservé. Mesure en caisse requise ; aucun gain de durée annoncé. |
| M06 · C1/D1 | Risque de supprimer des fonctions ou repères existants. | Options « Tout marquer comme lu » et suppression accessibles ; PIN replié, avertissement appareil conservé ; menu ordinateur et quatre entrées mobiles maintenus. | Aucun retrait fonctionnel décidé. Les contrôles du prototype sont illustratifs. |
| M07 · E1/D1 | PM : les consignes pourraient introduire de nouvelles obligations. | Rattachement aux preuves existantes : « Après approbation, installez… » dans la capture 16 ; impression taille réelle, test du QR, mission d’achat et déclaration prêt dans la capture 21. | Aucune nouvelle obligation : « 100 % » explicite « taille réelle ». Les règles varient par animation. |
| M08 · B1/F1 | Certitude abusive de « aucune validation ». | Réservé au rejet local, au refus certain et à l’interruption avant tout envoi. Les cas réponse perdue et vérification impossible restent incertains. | Condition à prouver par l’état réel ; jamais inférée du silence du serveur. |

Le commentaire d’accessibilité sur « l’aide illisible » provenait d’une ambiguïté de la transcription : « Le QR reste illisible ? » est le titre d’une aide, pas un défaut de rendu constaté. La revue visuelle principale a vérifié ce libellé et le dépliage. Cela ne vaut pas audit d’accessibilité.

**Aucun changement substantiel de l’orientation adoptée n’a été retenu ; aucun nouveau vote n’a donc été organisé.** Les préférences de revue ne sont pas un second scrutin. Si une suite décide une nouvelle règle de préparation, une autre borne de période, ou une procédure opérationnelle nouvelle, elle devra être instruite séparément ; les voix fictives n’autorisent aucun développement.

## Hypothèses et dépendances conservées

- **HYPOTHÈSE B1/F1 :** affichage utile des résultats et reprise fiable. Confirmation, reçu et état incertain existent dans le code (C02) ; la maquette ne prouve pas leur fonctionnement. La vérification doit lire une opération identifiable sans la rejouer. Après expiration, droits et contexte doivent être relus ; aucun QR ou jeton ne figure dans les URL du prototype.
- **HYPOTHÈSE D1 :** périmètre explicite des compteurs utile. « 2 en cours / 1 à venir » est un exemple, pas une résolution du 2/3. Ne pas faire du libellé « période ouverte » une nouvelle règle métier avant diagnostic. La prochaine action dépend du modèle et de l’état : l’attente Vitrines et l’installation Tombola sont deux cas différents.
- **DÉDUIT E1 :** les instants `2026-11-18T23:00:00Z` et `2026-11-22T23:00:00Z` donnent respectivement 19 novembre à 0 h et 23 novembre à 0 h à Paris. L’affichage de la borne exacte évite d’inventer « jusqu’au 23 inclus ». L’intention métier et la règle d’acceptation restent à contrôler.
- **OBSERVÉ E1 :** le guide cite `flyer-animation.pdf` ; **non vérifié** : le contenu effectivement téléchargé. Aucune taille, nombre de pages, archive ou autre support n’est promis. Télécharger ne déclare jamais prêt ; le lien de participation reste distinct.
- **HYPOTHÈSE C1 :** une action lue reste utile si elle est actuelle et autorisée. Aucune action n’est inventée à partir d’un message de publication. Les exemples « information » et « tâche en brouillon » sont des scénarios séparés.
- **Non exécuté :** QR valide/doublon réel, caméra physique, coupure réseau métier, session expirée réelle, retour différé réel, téléchargement/impression, tests avec commerçants, lecteur d’écran et conformité d’accessibilité.

## Isolation et mode de lecture

Les HTML/CSS/JS sont exclusivement des sources de maquette dans ce workshop. Aucun import du code applicatif, API, dépendance distante ou stockage de session. Les boutons métier affichent seulement une indication de démonstration ; les liens de navigation mènent à des scénarios locaux. Les accordéons fonctionnent. Les filtres métier dessinés ne filtrent aucune donnée réelle.

Les PNG APRÈS sont des vues dépliées : la navigation mobile est placée en bas du document au rendu pour ne masquer aucun contenu. Le prototype interactif conserve sa barre collante ; les captures AVANT, y compris leurs artefacts de capture longue, ne sont pas retouchées. Les panneaux de la galerie défilent et les images peuvent être ouvertes à taille réelle.

La galerie répond aux formats mobile et ordinateur ; chaque état possède un PNG 390 px et un PNG 1440 px. Une comparaison ordinateur peut conserver un AVANT mobile lorsque c’est la preuve disponible ; le format est indiqué, sans prétendre à une mesure quantitative entre deux mises en page équivalentes.
