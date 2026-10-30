# EPIC 75 — Mots croisés assistés par l’IA

## Références et état

- **État produit : À faire**, cadrage initial du **22 octobre 2026**.
- Arbitrages de parcours confirmés le **23 octobre 2026** : indices chez les
  commerçants ; Localeo prépare puis l’organisateur valide ; grille entièrement
  correcte et passages requis validés par les commerçants obligatoires pour accéder au tirage.
- Demande : ajouter une animation payante « Le mot croisé », assistée par l’IA,
  sur le modèle de la chasse au trésor.
- Identifiant `75` vérifié dans la documentation commune et les noms de fichiers
  des dépôts applicatifs ; aucun cadrage de mots croisés existant retrouvé.
- [Roadmap commune](../README.md), [cycle d’epic](../../organisation/cycle-epic.md).
- Socles : [E55 — moteur et chasse au trésor](../../specifications/moteur-animation/README.md),
  [E73 — Animation et/ou Coffrets](../../specifications/epic-73-animation-et-ou-coffrets/README.md),
  [E42 — Live](../../specifications/epic-42-localeo-live/README.md).
- Périmètre distinct : une nouvelle mécanique de jeu et une nouvelle offre
  commerciale, avec création de grilles, réponses croisées et expérience joueur
  spécifiques. E75 ne remplace ni la chasse ni la
  [tombola publique E74](epic-74-tombola-publique-backlog.md).
- Aucun dossier de spécification détaillée ni implémentation dans ce cadrage.

## Problème et résultat attendu

Un organisateur doit pouvoir proposer une animation de mots croisés adaptée à
son thème, sans construire manuellement toute la grille et ses définitions.
L’assistance IA facilite la préparation ; elle ne suffit pas à démontrer que la
grille est cohérente, les définitions exactes ou la difficulté appropriée.

**Parcours cible proposé :** l’organisateur dispose du module, renseigne un
thème et les éléments utiles. Localeo prépare la grille avec l’assistance IA,
puis l’organisateur la valide avant publication. Le participant rejoint le jeu
depuis un lien ou un QR, trouve les indices chez les commerçants et remplit la
grille sur son téléphone. Il retrouve sa progression et doit compléter toute
la grille avec les bonnes réponses et faire valider les passages requis par les
commerçants pour accéder au tirage des lots. Ces conditions sont cumulatives.

Acteurs : responsable de l’organisation ou acheteur habilité, gestionnaire de
l’animation, opérateur Localeo, participant et gagnant ; commerçants accueillant
les indices et validant les passages, ou salariés habilités selon leurs droits
existants. Le participant ne peut pas attester lui-même son passage.

## Décisions acquises et propositions

| Référence | Nature | Contenu |
| --- | --- | --- |
| E75-DEC-01 | Demande acquise | Nouveau type d’animation de mots croisés |
| E75-DEC-02 | Demande acquise | Assistance IA à la préparation du jeu |
| E75-DEC-03 | Demande acquise | Animation payante sur le modèle de la chasse au trésor |
| E75-DEC-04 | Confirmé le 23 octobre | Les participants trouvent les indices chez les commerçants ; aucun mode entièrement en ligne retenu à ce stade |
| E75-DEC-05 | Confirmé le 23 octobre | Localeo prépare avec l’assistance IA, puis l’organisateur valide avant publication, comme pour la chasse au trésor |
| E75-DEC-06 | Confirmé le 23 octobre | Une grille entièrement complétée avec les bonnes réponses est obligatoire pour qualifier le participant au tirage au sort des lots |
| E75-DEC-07 | Confirmé le 23 octobre, remplace la demande intermédiaire d’option configurable | Validation commerçante obligatoire pour toutes les animations avec passages, y compris les mots croisés. Elle se cumule avec la grille correcte ; aucune option de désactivation à la création |
| E75-PROP-01 | Interprétation à confirmer | « Payante » désigne le module acheté par l’organisateur, avec participation gratuite du public ; aucun achat de billet participant ajouté implicitement |
| E75-PROP-02 | Proposition | Module distinct dans le catalogue E73, achetable, offert ou en essai pour une commune/souscription ; quota propre aux mots croisés |
| E75-PROP-03 | Proposition | Validation humaine du contenu et contrôle déterministe de la grille avant publication ; version publiée figée |
| E75-PROP-04 | Proposition | Réutiliser identité, participation, clôture, tirage et gestion des lots ; ne pas créer de deuxième moteur de tirage |

Le tarif de **190 € HT/an**, les **5 chasses** et le délai de préparation de
**5 jours ouvrés** sont des conditions existantes de la chasse. Ils ne sont
**pas adoptés pour les mots croisés** par ce cadrage. Prix, quotas, niveau de
service restent à décider explicitement ; le rôle humain suit désormais DEC-05.

## Périmètre

### Inclus

- Nouveau type identifiable dans le catalogue et l’assistant de création ;
  code candidat `MOTS_CROISES`, à confirmer lors de la spécification.
- Module commercial utilisant les mécanismes E73 : achat, essai/cadeau,
  habilitations, conditions acquises, droits par commune, suivi des usages,
  renouvellement et continuité des animations déjà publiées.
- Préparation : thème, public visé, difficulté et éléments locaux fournis par
  l’organisateur ; choix des paramètres effectifs et de leurs limites en ARB-04.
- Proposition IA de mots/définitions et assemblage d’une grille cohérente.
  Le choix de faire construire la géométrie par un algorithme ou de valider une
  géométrie proposée par l’IA relève de la spécification technique.
- Préparation par Localeo, prévisualisation, corrections et validation explicite
  par l’organisateur avant publication. Chaque
  régénération produit une proposition identifiable ; elle n’écrase pas
  silencieusement les corrections retenues.
- Joueur : accès mobile depuis QR/lien, définitions horizontales/verticales,
  saisie et correction, progression sauvegardée, reprise, résultat explicite.
  Les indices sont disponibles chez les commerçants, avec validation obligatoire
  des passages requis ; support et répartition restent à préciser en ARB-01.
- Grille entièrement correcte et passages requis validés obligatoires pour la qualification, clôture et tirage ; compatibilité
  avec les dotations Coffrets, lots libres externes et bons numériques à instruire.
- Supports de communication et flyers adaptés : promesse de mots croisés,
  dotation et chiffres réels, sans consigne de chasse ou compteur commerçants
  inadapté. Réutiliser l’[évolution des flyers E73](../../specifications/epic-73-animation-et-ou-coffrets/flyers-contextualises.md).
- Bilan : inscrits, grilles commencées/terminées, qualifiés, gagnants et lots
  remis ; suivi interne du coût et des échecs de préparation IA.

### Contraintes de conception proposées

- Le domaine backend décide publication, réponses acceptées, qualification,
  droits et consommation des quotas. L’IA propose des contenus, l’application
  orchestre, les interfaces présentent les décisions.
- Résolution et attestations commerçantes sont des faits distincts : une grille
  correcte seule ou des passages validés seuls ne qualifient pas le joueur.
  Un QR en libre-service ne remplace pas l’attestation commerçante. Réutiliser
  les validations autorisées existantes, sans imposer un achat pour les mots croisés.
- Contrôle avant publication : réponses de longueur compatible, croisements
  concordants, numérotation et définitions complètes, aucune case attendue sans
  réponse ; connectivité et règles d’accents/espaces à fixer en ARB-04/05.
- Solutions réservées à la préparation et au contrôle serveur, absentes des
  réponses publiques avant la révélation autorisée. Une obfuscation côté client
  ne constitue pas un contrôle d’accès.
- Aucun appel IA requis pour enregistrer une lettre ou évaluer une réponse.
  Préparation asynchrone avec état visible, délais bornés et reprise contrôlée ;
  pas d’attente indéfinie ni de régénérations sans limite.
- Interface de gestion cohérente avec Localeo Animation ; site public orienté
  découverte ; Live centré sur le jeu. Clavier, lecteurs d’écran, focus visible,
  libellés des coordonnées/directions et états compréhensibles sans couleur
  seule ; prévoir une saisie par définition accessible en complément de la grille.
- Listes et bilans paginés/agrégés côté serveur, accès indexés par animation et
  participant ; aucune table complète chargée pour compter les joueurs ou
  retrouver une progression. Taille de grille et cadence de sauvegarde bornées.
- Une modification en brouillon relance les contrôles. Après publication, une
  correction erronée ne doit pas disqualifier silencieusement les joueurs :
  procédure de correction/annulation à fixer explicitement en ARB-07.

### Hors périmètre proposé

- Mots mêlés, sudoku, jeu multijoueur en temps réel, application native ou
  validation par un modèle IA à chaque réponse.
- Billets payants pour les joueurs, classement au temps ou bonus achetables,
  sauf nouvel arbitrage explicite.
- Nouveau prestataire de paiement, moteur de tirage ou messagerie parallèle.
- Publication automatique d’un contenu IA non relu ; ingestion libre de pages
  externes ou transfert de données personnelles de participants à un fournisseur IA.
- Migration des anciennes chasses ou consommation de leurs crédits par défaut.

## User stories proposées

| ID | Acteur et besoin | Critères |
| --- | --- | --- |
| E75-US-01 | Acheteur et Localeo : acheter ou accorder le module et comprendre les droits disponibles | 01, 02 |
| E75-US-02 | Gestionnaire : définir le thème et demander à Localeo la préparation assistée par IA | 03, 04 |
| E75-US-03 | Localeo prépare et corrige ; l’organisateur relit et valide la grille avant publication | 05, 06, 07 |
| E75-US-04 | Gestionnaire : publier une version prête et diffuser ses supports | 07, 08 |
| E75-US-05 | Participant : trouver les indices chez les commerçants, résoudre la grille sur mobile et reprendre sa progression | 08, 09, 10, 11 |
| E75-US-06 | Participant : connaître son résultat et son éligibilité selon des règles annoncées | 12, 13 |
| E75-US-07 | Gestionnaire et gagnant : clôturer, tirer et suivre les lots avec le socle existant | 14, 15 |
| E75-US-08 | Localeo et gestionnaire : suivre usages, coûts et incidents sans régression des autres animations | 16, 17, 18 |

## Critères d’acceptation cibles

Les critères dépendant d’un arbitrage décrivent la cible à confirmer, pas une
décision acquise. Ils sont prévus et **non exécutés**.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E75-CA-01 | Acheteur habilité dans sa commune, conditions ARB-08 définies | Acheter le module ou consulter un octroi | Prix, durée, quota et commune explicites ; paiement attendu seul sans activation ; aucun crédit chasse détourné |
| E75-CA-02 | Droit absent, expiré, hors commune ou quota épuisé | Tenter un nouvel usage protégé | Refus serveur compréhensible ; essai/cadeau contrôlé et tracé ; continuité uniquement pour les opérations déjà engagées selon E73 |
| E75-CA-03 | Gestionnaire autorisé, brief conforme | Demander une proposition | Demande de préparation transmise à Localeo, état et prochaine action visibles ; proposition soumise à l’organisateur pour validation ; double clic sans deuxième traitement involontaire |
| E75-CA-04 | Préparation échouée, trop longue ou incomplète | Consulter puis reprendre | Échec ou attente explicites, reprise bornée sans publication ni effacement de la dernière proposition conservée ; coûts et crédit de publication distingués |
| E75-CA-05 | Grille candidate comportant un croisement incohérent ou une définition manquante | Valider/publier | Blocage et anomalies localisées ; une réponse IA ne peut contourner les contrôles déterministes |
| E75-CA-06 | Grille corrigée par un humain | Régénérer ou modifier un mot | Corrections conservées tant qu’un remplacement explicite n’est pas accepté ; contrôles relancés sur toute la grille concernée ; auteur/version de validation tracés |
| E75-CA-07 | Contenu préparé par Localeo, paramètres et dotation prêts, droit disponible | Publier puis rejouer la requête | Validation explicite de la version par l’organisateur exigée ; une version publiée et un seul débit du quota choisi ; aucune publication partielle ; indices chez les commerçants prêts selon les modalités ARB-01 |
| E75-CA-08 | Animation publiée | Ouvrir QR, page publique et flyer | Même animation et consignes pour trouver les indices chez les commerçants ; lots et commerces cohérents ; aucun corrigé ni secret dans le support |
| E75-CA-09 | Participant autorisé, animation ouverte | Saisir au clavier/mobile ou par définition | Cases et définitions associées, direction/focus visibles, saisie utilisable sans dépendre uniquement d’un geste tactile ou d’une couleur |
| E75-CA-10 | Progression enregistrée puis réseau interrompu | Reprendre et renvoyer la sauvegarde | Dernier état confirmé retrouvé ; état non enregistré visible ; répétition sans participation ou chance supplémentaire ; conflit entre sessions traité explicitement |
| E75-CA-11 | Visiteur ou autre participant | Consulter le jeu, ses API ou une progression tierce | Pas d’accès au corrigé avant la règle de révélation, ni aux réponses personnelles d’autrui ; droits revérifiés côté serveur |
| E75-CA-12 | Règles DEC-06/07 et ARB-01/05/06 annoncées | Soumettre une grille incomplète, erronée puis correcte, avec et sans passages requis validés | Qualification uniquement avec grille entièrement correcte ET passages requis validés par les commerçants ; grille correcte seule et passages seuls insuffisants ; états de résolution et passages manquants distincts ; aucune auto-attestation ni option de désactivation ; accents/variantes et aides suivent la même règle pour tous ; aucune décision d’éligibilité confiée à l’IA |
| E75-CA-13 | Animation clôturée, annulée ou requêtes concurrentes | Soumettre/rejouer une réussite | Pas de qualification tardive non autorisée, pas de double chance ; borne temporelle serveur et effet de la clôture explicites |
| E75-CA-14 | Animation clôturée | Tirer avec zéro, peu ou plusieurs qualifiés | Population figée contenant uniquement les participants avec grille entièrement correcte et passages requis validés ; gestion du manque de gagnants et des suppléants via le socle ; aucun moteur de tirage parallèle |
| E75-CA-15 | Gagnant attribué, mode de dotation compatible | Notifier et remettre le lot | Email et état de remise cohérents avec E73 ; bon QR/PIN uniquement lorsque choisi ; remise du lot distincte des validations de passages ayant qualifié le joueur |
| E75-CA-16 | Gestionnaire et opérateur selon droits | Consulter participants, bilan et coûts | Pagination et accès indexés ; totaux cohérents ; coûts IA internes séparés des quotas client et des données personnelles |
| E75-CA-17 | Tentatives abusives, répétition de génération ou appel IA indisponible | Lancer/sauvegarder/jouer | Limites techniques observables ; jeu publié utilisable sans dépendance synchrone à l’IA ; pas de correction ni secret dans les logs |
| E75-CA-18 | Données et types d’animation existants | Vérifier contrats, migrations et fixtures | Chasse, tombolas, passeport et conditions acquises préservés ; nouvelle animation non attribuée automatiquement aux souscriptions existantes |

## Impacts à instruire

| Sujet | Impact initial et sources |
| --- | --- |
| Domaine backend | **Concerné** : moteur Animation pour grille/version/réponses/qualification ; Abonnements pour droit/quota ; application de préparation pour orchestration IA. Fronts, API et worker ne réimplémentent pas ces invariants |
| Localeo Animation | **Concerné** : catalogue, brief, préparation/relecture/aperçu, contrôle de publication, supports, participants et bilan |
| Marketplace / site Animation / Live | **Concerné** : découverte, entrée QR/lien, grille accessible, progression, résultats et reprise. Préférences de communication existantes conservées |
| Localeo Pro / OnBoard | **Concerné** : participation, indices et validation obligatoire des passages avec les droits existants ; remise des lots selon ARB-09. Aucun nouveau droit salarié implicite |
| ERP / Support / Ops | **Concerné** : gestion de l’offre et des octrois, supervision de préparation, incidents, coûts et assistance selon habilitations |
| API et consommateurs | **À spécifier** : nouveau type/capacités, brief et propositions, grille publique sans solutions, progression, résultat et états. Contrats backend et embarqués à faire évoluer ensemble, sans inventer de routes au cadrage |
| Persistance / migration | **À examiner** : catalogue et journal d’usage, versions de grilles, solution protégée, progression et qualification ; unicité/concurrence, index et conservation ; aucune conversion silencieuse de chasses |
| IA / médias / exploitation | **Concerné** : format de sortie contrôlé, génération manuelle assistée ou fournisseur selon ARB-02, temps/reprises/coûts bornés, traçabilité sans secrets. Ne pas présumer une intégration fournisseur déjà disponible |
| Générateur / fixtures | **Concerné** : grille valide/invalide, jeu incomplet/réussi, refus droit/quota, interruption/reprise, dotations et modes retenus ; jeux déterministes sans coût IA obligatoire pour les tests |
| Documentation fonctionnelle | **Concerné** : guide organisateur, aides joueur, conditions de réussite, règles de jeu, promesse commerciale et procédure de correction ; aucune approbation éditoriale ou juridique présumée |
| Performance / preuves | **Concerné** : pagination/index, bornage de grille/génération/sauvegardes, concurrence de qualification et quota ; reprendre la cible E73 comme base à confirmer, mesurer les rafales de sauvegarde propres au jeu |
| Déploiement | **À examiner** à la spécification : activation coordonnée modèle/module/consommateurs, migrations, configuration et retour arrière. Aucun déploiement dans cette phase |

## Questions ouvertes

| ID | Décision attendue / proposition | Parties dépendantes |
| --- | --- | --- |
| E75-ARB-01 | **Mode décidé : indices chez les commerçants et validation commerçante obligatoire (DEC-04/07).** Restent le support des indices, leur répartition et la définition des passages requis ; aucune option désactivant l’attestation | US02/04/05, Pro et OnBoard |
| E75-ARB-02 | **Rôles décidés : Localeo prépare puis l’organisateur valide (DEC-05).** Restent génération intégrée/manuelle assistée, délai annoncé et limites de régénération | US02/03, exploitation et coût |
| E75-ARB-03 | **Résolu : grille entièrement correcte ET passages requis validés par les commerçants (DEC-06/07).** Identité et limitation des chances en ARB-09 ; répartition des passages en ARB-01 | US06/07, règle métier de réussite |
| E75-ARB-04 | Langue(s), niveaux, taille/nombre de mots et thème local ; mots imposés par le gestionnaire ? Proposition V1 : français, une grille commune par animation, taille bornée, validation humaine des faits locaux | US02/03/05, géométrie, accessibilité |
| E75-ARB-05 | Accents, espaces, traits d’union, variantes acceptées et affichage des erreurs : contrôle à la demande, par mot ou final ? Fixer les règles avant publication pour éviter des rejets ambigus | US03/06, corrigé et saisie |
| E75-ARB-06 | Aides/indices, nombre d’essais et révélation du corrigé ; impact d’une aide sur l’éligibilité ? Proposition : pas de révélation publique avant clôture, pas de bonus de vitesse | US05/06, équité et protections contre essais automatisés |
| E75-ARB-07 | En cas de mauvaise définition publiée : qui corrige, suspend ou annule, et comment préserver/rectifier les qualifications déjà acquises ? Pas de remplacement silencieux de grille en cours | US03/04/06, support et audit |
| E75-ARB-08 | Confirmer module payé par organisateur et gratuit pour joueurs ; tarif HT annuel, quota indépendant, essais/cadeaux et prorata à fixer. Proposition : réutiliser E73 avec crédit débité une seule fois à publication ; ne pas reprendre automatiquement 190 € / 5 | US01/04, catalogue, achat et usages |
| E75-ARB-09 | Confirmer modes de lots E73 disponibles et identité minimale/limitation de chances. Proposition : réutiliser Live, une chance par participant qualifié. Les commerçants portant les indices et ceux remettant les lots ont des rôles distincts | US05/07, participation et remise |

Les trois réponses du 23 octobre sont consignées dans DEC-04 à DEC-06.
ARB-03 est résolu ; ARB-01 et ARB-02 conservent des modalités ouvertes.
Les propositions restantes ne sont pas validées implicitement par ces réponses.

### Précision du 23 octobre — validation par le commerçant

Une première demande proposait de rendre l’exigence de validation commerçante
configurable à la création et d’étendre ce choix aux autres animations.
L’utilisateur a ensuite corrigé : « je veux garder la validation par le
commerçant », en réponse à la question concernant le passeport et la tombola
commerçante. Leur validation commerçante est donc conservée ; aucun remplacement
par un QR en libre-service ou une simple inscription n’est retenu.

Confirmation finale : « Obligatoire partout, y compris les mots croisés ».
Elle remplace la demande intermédiaire d’option configurable, désormais abandonnée.
Passeport, tombola commerçante et chasse conservent leurs règles de validation
existantes, sans changement de statut ni réécriture de leur historique.
E75 exige cette attestation en plus de la grille entièrement correcte.
La tombola publique E74 sans passage commerçant conserve son périmètre distinct.
L’attestation d’achat propre à E53 n’est ni supprimée ni étendue aux autres jeux.
Aucune évolution des autres animations n’est nécessaire pour introduire cette
option finalement non retenue.

## Passage à la spécification

**8 US, 18 critères cibles et 9 groupes d’arbitrages, dont 1 résolu et 8 encore
ouverts ou partiels.** Le nouveau jeu payant, l’assistance IA, les indices chez
les commerçants, la préparation Localeo validée par l’organisateur, la grille
correcte et les passages requis validés obligatoires pour le tirage sont acquis. Résoudre les modalités restantes
et l’offre avant de figer la conception détaillée.
La spécification devra relier chaque critère aux contrats, transactions,
index, comportements observables et preuves, selon le cycle d’epic.
Cette création ne réalise ni code, ni migration, ni activation commerciale,
ni commit, push ou déploiement.
