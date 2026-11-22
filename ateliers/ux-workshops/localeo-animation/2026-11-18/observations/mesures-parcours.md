# Mesures de parcours

## Méthode et limites

Les décomptes ci-dessous viennent des interactions réellement exécutées, pas d’une estimation de performance humaine. Pour les segments détaillés, un clic sur bouton, choix de modèle, radio ou case compte une action ; une saisie, un choix de valeur dans un select, une attente, un défilement ou une capture n’est pas compté comme clic. Les appels de sélecteurs échoués sont exclus : ils n’ont pas actionné le produit. Aucun chronomètre de tâche humaine n’a été lancé. **Temps de réalisation : non mesuré pour chacun des 18 parcours.**

Les séquences interrompues par lecture du code et inspection d’autres écrans ne donnent pas un total de navigation global fiable : « NR » signifie non relevé exhaustivement. Les étapes affichées par l’application sont distinguées des écrans réellement visités. Les nombres ne sont pas des objectifs UX ni des minimums théoriques.

## Tableau des 18 parcours

| # | Parcours | Étapes / clics réellement dénombrables | Champs, friction, erreur, retour ou information manquante |
| --- | --- | --- | --- |
| 1 | Connexion | 1 formulaire ; 1 clic de soumission par connexion réussie | Deux champs : email et mot de passe. Reconnexion technique après perte du contexte d’automatisation, pas un échec de compte. |
| 2 | Accueil | 1 écran principal ; navigation libre, total NR | Période et statut filtrent les indicateurs. Beaucoup de sections ; effet sur compréhension non mesuré. |
| 3 | Tombola | 7 étapes affichées + confirmation ; 14 actions depuis la liste jusqu’à la création, hors saisies | Sept valeurs saisies explicitement dans notre variante ; mission préremplie et quantité 1 conservées. Une erreur volontaire de dates puis correction ; zéro retour Précédent dans la séquence de création. |
| 4 | Passeport | 7 étapes + confirmation ; 15 actions selon le même chemin avec deux commerces, plus un choix de seuil dans le select | Minimum deux commerces ; seuil initial quatre ramené à deux. Sept valeurs saisies comme pour la tombola. Zéro retour Précédent. |
| 5 | Dotation | Segment : 3 clics (Lots libres → Gestion hors Localeo → Ajouter un lot), puis 3 saisies | Libellé, responsable et consignes ; quantité 1 préremplie. Nature et mode doivent être choisis. Coffrets et bons numériques non exécutés. |
| 6 | Reprise brouillon | Depuis le détail tombola : Animations → nom du brouillon, soit 2 clics, puis choix Configuration | Valeurs conservées. Nouvelle lecture directe de l’URL également faite. Aucun enregistrement intermédiaire de l’assistant observé. |
| 7 | Aperçu/publication | 1 étape Flyer, puis récapitulatif ; publication : 0 clic de commande | QR provisoire expliqué ; bouton Publier désactivé. Attente d’accord externe au parcours de saisie. Aucun temps de publication mesurable. |
| 8 | Ajout individuel | 1 ouverture de fiche existante ; création individuelle non atteinte | Entrée de création non trouvée. Champs d’un formulaire individuel : non accessibles. |
| 9 | Import | Flux → dépôt → mapping → aperçu → comparaison ; 10 associations de colonnes effectuées | Cinq associations marquées obligatoires ; 14 cibles affichées, dix colonnes source. Deux lignes prêtes, zéro conflit/erreur, confirmation non exécutée. Identités fortes absentes. Total de clics NR. |
| 10 | Invitations/activation | Nouvelle demande et accord préexistant consultés ; envoi : 0 | Une demande pour tombola, deux pour passeport ; échéance 30 novembre pour les créations. Activation de compte non testée. |
| 11 | Animation en cours | Depuis le bilan : 1 clic « Ouvrir le suivi de l’animation » | Libellé amont « Consulter le suivi » conduit au bilan dans le cas testé. Total depuis connexion NR. |
| 12 | Participations | 2 choix de rubrique : Participants puis Validations | Une inscription non qualifiée, zéro validation ; référence exacte de participation ou début de nom selon la liste. Aucune correction exécutée. |
| 13 | Communication/notifications | Échec de lecture puis 1 actualisation ciblée ; 2 réponses 500 enregistrées ; 1 ouverture de cloche | Pas de formulaire de campagne utilisable dans ce contexte ; cause de panne non fournie. Neuf notifications existantes. Réception nouvelle non mesurée. |
| 14 | Clôture | Depuis l’action de clôture : 1 clic ouvre la préparation ; 1 clic retourne au suivi | Case de confirmation définitive non cochée ; commande finale non envoyée. Conséquences affichées. |
| 15 | Gagnants/lots | 3 rubriques : Fin, Tirage, Gains & remise | Un gagnant, un lot, une remise non renseignée. Pas d’envoi, tirage ou attestation nouvelle. Clics globaux NR. |
| 16 | Bilan | 1 rubrique, sur une animation en cours puis une clôturée | Dates de lecture et couverture distinctes ; exports proposés, non exécutés. |
| 17 | Duplication | Depuis la ligne source : 7 actions, 3 champs saisis ; résultat Brouillon | Deux choix de contenus, nature et remise, confirmation puis création. Lots à recréer ; aucune reprise d’accords. L’action « Ajouter un lot » n’existe pas dans ce formulaire de clonage. |
| 18 | Pilotage multiple | 1 saisie de recherche, retour de détail, 1 réinitialisation | Deux résultats avant clonage ; filtre conservé au retour. Le jeu initial comporte sept animations visibles dans la liste non filtrée. |

## Séquences de création comptées

**Tombola, 14 actions :** Créer une animation → Tombola locale → Continuer → Continuer après informations → sélectionner le commerce → Continuer → Continuer après mission/échéance → Lots libres → Gestion hors Localeo → Ajouter un lot → Continuer → Continuer après flyer → Créer le brouillon → confirmer Créer le brouillon.

**Passeport, 15 actions :** même séquence avec sélection de deux commerces. Le changement du seuil dans un select est compté séparément. Les saisies de la variante testée sont : nom, début, fin, échéance de réponse, libellé du lot, responsable de remise, consignes. La mission préremplie contient deux valeurs obligatoires conservées. La correction volontaire de la date tombola constitue une saisie supplémentaire, pas un clic.

**Clone, 7 actions :** Cloner l’animation → Textes de présentation → Scénario et paramètres → Lots libres → Gestion hors Localeo → case de confirmation → Créer le brouillon cloné. Nom et deux dates saisis. Aucune sélection de commerçant ou lot reprise.

## Contraintes de formulaire confirmées par le code local

**DÉDUIT — C02 :** nom, début, fin cohérente ; minimum de commerces ; titre et description de mission ; échéance située entre aujourd’hui et le début ; seuil de passeport atteignable ; dotation explicitement choisie. Pour le lot externe de notre variante : libellé, responsable, consignes non vides et quantité entière positive. Ces contrôles front ne remplacent pas les règles serveur.

## Mesures de largeur

**OBSERVÉ :** viewport et largeur du document = 390 px pour tableau de bord, liste, informations de création, configuration, invitations, import, fin et bilan. Bureau : 1440/1440 px sur le tableau de bord final. [Relevés bruts expurgés](releves-techniques.json). Pas de mesure de vitesse humaine, taux de réussite autonome ou satisfaction.

Pour vérifier la promesse produit, chronométrer ultérieurement des sessions réelles, en séparant : préparation des informations, brouillon enregistré, attente des commerçants et publication effective. Aucun résultat de ce futur test n’est présumé.
