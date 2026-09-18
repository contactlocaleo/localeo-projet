# Epic 57 - Registre des arbitrages

## Mode d'emploi

Ce registre contient uniquement les decisions a valider avant de figer les
contrats de pagination et de commencer leur generalisation. Les principes de
l'Epic 57 qui ne sont pas soumis a arbitrage sont rappeles en fin de document.

Etat du registre : les dix-huit arbitrages sont valides.

| ID | Point a arbitrer | Explication detaillee | Priorite | Proposition simple | Validation ou amendement |
| --- | --- | --- | --- | --- | --- |
| PAG-ARB-01 | Traitement d'une taille invalide | Les validateurs FastAPI actuels retournent `422` pour une valeur nulle, negative ou excessive, tandis que le backlog recommandait initialement un bornage silencieux. Un comportement different selon la route rendrait le contrat difficile a comprendre. | P0 | Toute route de collection impose une taille par defaut et un maximum serveur. Une valeur fournie nulle, negative, non numerique ou superieure au maximum retourne `422` ; l'absence de valeur applique le defaut et ne peut jamais declencher une lecture non bornee. | Valide avec amendement : conserver `422` et rendre le bornage serveur obligatoire. |
| PAG-ARB-02 | Nom du parametre de taille | Les routes utilisent actuellement `limit`, `page_size` ou les deux. Accepter simultanement deux valeurs contradictoires rend la priorite ambigue. | P0 | Utiliser `page_size` sur les nouveaux contrats. Pendant la compatibilite, conserver `limit` comme alias deprecie et refuser la requete si `limit` et `page_size` sont tous deux fournis avec des valeurs differentes. | Valide. |
| PAG-ARB-03 | Format public de la pagination | Le code melange `page_size`, `next_cursor`, `nextCursor` et des listes sans enveloppe. Cette decision conditionne les schemas OpenAPI et tous les clients. | P0 | Standardiser les nouvelles reponses sur `{items, pagination: {pageSize, nextCursor, hasMore}}` en camelCase. Ne retourner `total` que lorsqu'il est deja disponible sans requete supplementaire couteuse. | Valide. |
| PAG-ARB-04 | Migration des listes existantes | Remplacer directement une liste JSON par une enveloppe paginee casse les clients deployes qui attendent un tableau. Maintenir temporairement une route non paginee laisserait cependant subsister le risque que l'Epic doit supprimer. | P0 | Interdire immediatement les lectures non paginees sur les routes du perimetre. Faire evoluer chaque route vers une enveloppe paginee et adapter ses clients dans le meme lot de livraison ; ne conserver aucun ancien contrat permettant de charger toute la collection. | Valide avec amendement : aucune periode de coexistence avec une liste non bornee. |
| PAG-ARB-05 | Contenu et opacite du curseur | Un curseur limite a une date peut perdre des elements partageant le meme horodatage. Un JSON encode en Base64 est opaque pour le client mais reste falsifiable. | P0 | Encoder dans un curseur versionne toutes les valeurs du tri et l'identifiant stable. Signer le curseur avec un secret backend partage par les instances, sans y placer de donnee personnelle ni de token metier. | Valide. |
| PAG-ARB-06 | Reponse a un curseur invalide | Le backlog demande une erreur fonctionnelle `400`, alors que certaines routes transforment aujourd'hui l'erreur en `422`. Un curseur valide syntaxiquement mais incompatible avec les filtres doit aussi etre traite. | P0 | Retourner `400 CURSEUR_INVALIDE` pour un curseur malforme, falsifie, expire ou incompatible avec la route et ses filtres. Ne jamais le traiter comme une erreur serveur. | Valide. |
| PAG-ARB-07 | Duree de validite d'un curseur | Un curseur sans expiration facilite la reprise mais peut survivre a une evolution du tri, des filtres ou du schema. | P1 | Inclure une version de contrat dans le curseur, sans expiration temporelle au MVP. Invalider explicitement les versions non supportees avec `400 CURSEUR_INVALIDE`. | Valide. |
| PAG-ARB-08 | Strategie de departage stable | Chaque collection possede un tri metier different. Sans dernier critere unique, ajouts et egalites peuvent produire doublons ou omissions entre pages. | P0 | Terminer tous les tris pagines par `id` dans le meme sens que le dernier critere principal, et inclure l'ensemble du tuple dans le curseur. Documenter le tuple par route dans OpenAPI. | Valide. |
| PAG-ARB-09 | Definition d'un doublon | Une activite peut etre atteinte par plusieurs rattachements territoriaux. Deux lignes peuvent aussi representer une meme source metier sans avoir le meme identifiant technique. | P0 | Dedupliquer d'abord par identifiant public de la ressource retournee. Traiter la duplication d'une meme source metier comme une anomalie de production distincte, protegee par les contraintes d'unicite du domaine source. | Valide. |
| PAG-ARB-10 | Communes utilisees par l'accueil | Le contexte geographique peut contenir jusqu'a cinquante communes, alors que le widget `communesDisponibles` est recommande a huit. Limiter trop tot le contexte reduirait silencieusement les contenus des autres widgets. | P0 | Conserver toutes les communes eligibles et bornees pour calculer la projection territoriale, mais n'exposer que les huit premieres dans `widgets.communesDisponibles`. Le champ `contexte.communes` conserve son contrat de recherche de proximite. | Valide. |
| PAG-ARB-11 | Plafond des animations de l'accueil | L'implementation Epic 52 retourne actuellement six animations, tandis que l'Epic 57 en recommande quatre. Cette reduction modifie directement la composition de l'accueil. | P0 | Retenir quatre animations dans `widgets.animationsProches`, avec un plafond fixe et versionne cote backend. | Valide. |
| PAG-ARB-12 | Configuration des plafonds de l'accueil | Le backlog demande une configuration backend versionnee. Des variables d'environnement facilitent l'exploitation mais permettent a deux instances de retourner des contrats differents et au plafond de changer sans version de code. | P0 | Definir les plafonds `1/8/4/5/6` comme constantes versionnees dans la projection. Ne pas les exposer comme parametres client ni comme variables d'environnement. | Valide. |
| PAG-ARB-13 | Projection des coffrets | Le parametre actuel `avec_prestations` peut declencher un chargement detaille et des requetes unitaires sur toute une liste. Il faut definir si cette compatibilite reste autorisee sur la route paginee. | P0 | La collection paginee retourne uniquement la projection `summary`. Les prestations detaillees restent disponibles sur la route d'un coffret unique ; ne pas proposer `projection=detail` sur une collection au MVP. | Valide. |
| PAG-ARB-14 | Calcul du total global | Un `COUNT` exact ajoute une requete et peut devenir couteux avec les filtres d'eligibilite. Le frontend n'en a pas besoin pour un chargement progressif. | P0 | Ne pas calculer de total sur les routes publiques paginees de l'Epic 57. Utiliser `limit + 1` pour produire `hasMore` et `nextCursor`. | Valide. |
| PAG-ARB-15 | Coherence d'une pagination pendant les mutations | Une pagination par curseur stable evite les decalages d'offset, mais ne fournit pas un snapshot transactionnel entre plusieurs requetes. Des ajouts recents peuvent ne pas apparaitre dans les pages suivantes. | P1 | Accepter une coherence de lecture sans snapshot : aucune omission pour les elements situes apres le curseur, les nouveaux elements places avant lui apparaissent lors d'un rafraichissement explicite. Documenter ce comportement. | Valide. |
| PAG-ARB-16 | Resolution groupee de la bibliotheque Live | Le backlog recommande 30 references par defaut et 50 au maximum, mais ne precise pas le comportement d'un lot excessif ni l'ordre des resultats. | P1 | Refuser avec `422` un corps de plus de 50 references, traiter au plus 30 par appel frontend et retourner exactement un resultat par reference dans l'ordre de la requete, y compris pour les erreurs individuelles. | Valide. |
| PAG-ARB-17 | Mesure du poids des reponses | Mesurer chaque corps apres serialisation peut consommer memoire et CPU. Sans convention, les valeurs seront incomparables entre middleware, proxy et observabilite applicative. | P1 | Mesurer `Content-Length` lorsqu'il est disponible et completer par une metrique au reverse proxy. Ne pas reserialiser une reponse uniquement pour la mesurer dans l'application. | Valide. |
| PAG-ARB-18 | Seuils de mise en production | Les alertes proposees (`500 Ko`, P95 `500 ms`, plus de 50 lignes) n'indiquent ni fenetre, ni volume minimum, ni environnement de reference. | P1 | Valider les contrats fonctionnels avant de bloquer le deploiement sur ces seuils. Collecter une baseline en preproduction puis fixer les alertes de production dans le lot d'observabilite. | Valide. |

## Points non soumis a arbitrage

- toute collection publique ou protegee identifiee par l'Epic 57 est bornee par
  le backend ;
- le tri, l'eligibilite et la deduplication sont appliques avant la limite ;
- une limite transmise par le client ne peut jamais depasser le maximum serveur ;
- les collections soumises a des mutations frequentes utilisent un curseur et
  non un offset ;
- le frontend ne calcule pas `hasMore` a partir de la seule taille recue ;
- le chargement d'une page suivante exige une action utilisateur, sauf decision
  produit explicite en faveur d'un scroll infini ;
- une erreur de chargement d'une page suivante conserve les elements deja
  affiches ;
- les filtres relationnels, notamment `animation_id`, sont appliques dans la
  requete backend et non apres reception par le frontend ;
- les tokens, references privees et coordonnees ne sont jamais inscrits dans les
  curseurs ou les journaux techniques ;
- les exports, batchs et ecrans d'administration restent hors perimetre de
  l'Epic 57.
