# EPIC 76 — Accès support par impersonification à Localeo Pro et Animation

## Références

- Identifiant **EPIC-76**, disponible après recherche dans la roadmap commune et les namespaces applicatifs le **1er novembre 2026**.
- État produit : **En cours**, selon la [roadmap commune](../README.md).
- Besoin utilisateur : depuis Localeo ERP, accéder à Localeo Pro ou Localeo Animation dans le contexte d'un utilisateur pour faciliter son assistance.
- Implémentation locale. Le [bilan de vérification](../../specifications/epic-76-impersonification-support-pro-animation/verification-livraison.md) suit la recette et les conditions d’activation.
- Dépendances : [E69 — accès internes](../../specifications/epic-69-acces-internes/README.md), [E72 — accès salariés Pro](../../specifications/epic-72-acces-salaries/README.md), [E73 — Animation et/ou Coffrets](../../specifications/epic-73-animation-et-ou-coffrets/README.md) et [E70 — validation par PIN](../../specifications/epic-70-validation-pin/README.md).
- Ces epics définissent les identités, droits et parcours à préserver. E76 ajoute une délégation temporaire entre applications pour le support ; elle ne rouvre pas leurs clôtures et ne remplace pas les actions d'administration ERP existantes.
- Frontières vérifiées : E69 sépare les sessions internes et clientes dans son [architecture](../../specifications/epic-69-acces-internes/architecture-contrats.md) ; E73 distingue opérateur ERP, équipe organisatrice et notes internes dans les [parcours SaaS](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md) ; E72 distingue commerce et acteur principal/salarié dans son [architecture](../../specifications/epic-72-acces-salaries/architecture-contrats.md).
- [Spécification E76](../../specifications/epic-76-impersonification-support-pro-animation/README.md) : parcours, actions autorisées, architecture, garde-fous de charge et matrice de recette. Ce backlog reste la source canonique du besoin et des arbitrages.

## Problème et résultat attendu

Un gestionnaire de support doit comprendre ce qu'un commerçant ou un membre
d'équipe organisatrice voit dans son application, ses menus et ses blocages.
Le besoin exprimé est de pouvoir ouvrir ce contexte depuis l'ERP, sans demander
le mot de passe de la personne ni modifier son compte pour se connecter.
L'existence et les limites d'un éventuel mécanisme technique réutilisable restent
à examiner dans le code lors de la spécification ; la recherche documentaire
n'a trouvé aucun cadrage de ce parcours transverse.

**Exemple cible :** depuis la fiche ERP d'un commerçant Animation uniquement,
l'opérateur ouvre « Accéder à Localeo Pro pour le support ». Il voit les mêmes
menus autorisés que ce compte, sans fonctions Coffrets supplémentaires. Depuis
une organisation ou une souscription Animation, il choisit un membre existant
et ouvre son espace avec ses droits réels. Il peut quitter cette session à tout
moment et retrouver le dossier ERP d'origine.

L'« impersonification » désigne ici une **session de support temporaire** :
l'utilisateur représenté et l'opérateur réel restent deux identités distinctes.
Une action de support ne doit jamais être attribuée au seul utilisateur représenté.

### Acteurs

- Opérateur interne habilité : diagnostic et, si retenu, intervention explicite.
- Commerçant principal ou salarié Pro : compte dont on reproduit le périmètre autorisé.
- Membre d'une organisation Animation : compte et rattachement dont on reproduit les droits.
- Administrateur interne : habilitations, interruption et consultation des traces selon ses capacités.

## Périmètre

### Inclus

- Entrées ERP visibles depuis le commerçant et l'organisation/souscription Animation, et entrée **Accès client** dans Localeo Support. Sélection explicite du compte lorsqu'il y en a plusieurs.
- Identification de l'application, de l'environnement, du compte, du commerce ou de l'organisation et du motif d'assistance avant ouverture.
- Consultation des écrans Pro et Animation retenus pour le support, avec droits, modules, souscriptions et état de préparation de la cible.
- Session distincte, limitée dans le temps, révocable ; bandeau permanent et sortie simple sur PC et mobile.
- Audit des ouvertures, refus, changements de mode, interventions et fins de session, avec opérateur et cible.
- Preuves unitaires, d'intégration et fonctionnelles pour les deux applications, y compris appels API directs et sessions concurrentes.

### Parcours retenu

**E76-ARB-01, validé le 1er novembre 2026** — consultation par défaut, puis mode
intervention explicite et tracé. Les habilitations, actions et modalités retenues
le 23 novembre sont détaillées dans les arbitrages E76-ARB-02 à 04.

1. L'opérateur choisit **Ouvrir une session support** dans le dossier ERP ou passe par **Accès client** dans Localeo Support.
2. Une confirmation récapitule application, environnement, compte, rattachement,
   droits effectifs et motif ; un ticket existant peut être lié sans imposer sa création.
3. L'application s'ouvre en consultation avec un bandeau « Session support » :
   identité représentée, opérateur, mode, échéance et bouton « Quitter le support ».
4. Si le besoin le nécessite et que l'opérateur est habilité, il demande le mode
   intervention ; ses possibilités et leurs conséquences sont présentées avant confirmation.
5. Il termine la session. L'ERP permet de retrouver les actes et leur attribution.
   Le compte représenté retrouve le récapitulatif de l'intervention dans Localeo.

### Exclusions et frontières proposées

- Pas de partage, lecture ou réinitialisation de mot de passe pour ouvrir la session ; pas de compte client fictif ni de remplacement de l'identité réelle dans l'audit.
- Pas d'extension à Localeo Live, Marketplace, Ops, OnBoard, Atelier ou à des services tiers comme Stripe dans cette epic.
- Pas de modification des droits du client, de son offre ou de son périmètre pour « débloquer » artificiellement l'écran observé.
- Pas de reproduction des données purement locales à son appareil, de sa caméra, de son historique de navigation ou de ses notifications personnelles. La session reproduit le contexte serveur autorisé, pas son téléphone.
- Pas de connexion automatique d'un salarié en tant que commerçant principal, ni d'un membre organisateur en tant que propriétaire.
- Pas de session support hors ligne ni de délégation en cascade. Aucun droit ERP interne n'est transporté comme droit client.
- Les interventions sont limitées à la liste de la spécification. Les actes administratifs ERP existants gardent leurs propres autorisations.

### Contraintes existantes à préserver

Les profils E69 sont prédéfinis et leurs scopes fonctionnels sont globaux, sans
périmètre communal interne. E76 ne crée pas implicitement un rôle « Support »
ni une attribution de scopes arbitraires. Cette portée interne globale ne donne
jamais une session client couvrant plusieurs commerces ou organisations.

Le domaine backend porte les autorisations et le cycle de session ; l'application
orchestre le transfert et l'audit, les interfaces présentent les droits effectifs.
Une action reste soumise aux invariants de son domaine (Animation, validation,
commercialisation, etc.). Masquer un bouton n'est pas un contrôle d'autorisation.

## Critères d'acceptation cibles

La [matrice de recette](../../specifications/epic-76-impersonification-support-pro-animation/README.md#matrice-de-recette) relie les critères aux preuves prévues. Les résultats sont consignés au bilan de vérification.

| Critère | Acteur et préconditions | Action | Résultat observable et effets interdits |
| --- | --- | --- | --- |
| E76-CA-01 | Opérateur authentifié dans l'ERP | Ouvre le support depuis une fiche commerçant ou organisation/souscription, ou depuis Accès client dans Localeo Support | Application, environnement, compte et rattachement sont explicites. Le choix entre plusieurs comptes ne présélectionne pas silencieusement le plus privilégié. |
| E76-CA-02 | Opérateur autorisé ou non par la matrice retenue | Demande l'ouverture, y compris par API directe | Le serveur vérifie la capacité dédiée ; absence de droit, identité non vérifiée et origine non autorisée sont refusées sans session créée. Aucun rôle client ne reçoit cette capacité. |
| E76-CA-03 | Compte sélectionné existant | Confirme la demande avec un motif | Motif non vide et cible vérifiée sont requis ; compte désactivé, rattachement invalide ou cible d'un autre environnement sont refusés avec une explication exploitable. Aucun compte n'est réactivé implicitement. |
| E76-CA-04 | Session ERP autorisée | Transfère l'accès vers Pro ou Animation | Aucun mot de passe client n'est requis ou changé ; le transfert est limité à l'application, la cible et l'environnement prévus. Un lien rejoué, expiré ou détourné ne crée pas une nouvelle session autorisée ; aucun secret durable n'est exposé dans URL, logs ou référents. |
| E76-CA-05 | Commerçant principal ou salarié ciblé | Consulte les écrans Pro retenus pour le support | Menus et API respectent le périmètre Animation/Coffrets, la préparation et les capacités du compte réel. Un salarié ne gagne pas les droits du principal et un compte Animation seul n'accède pas aux fonctions Coffrets. |
| E76-CA-06 | Membre d'équipe Animation ciblé | Consulte les écrans Animation retenus pour le support | Les ressources restent limitées à l'organisation, au rattachement sélectionné, aux droits, modules et souscriptions applicables. Un identifiant modifié ou lien profond vers une autre organisation n'élargit pas l'accès. Les notes privées Support et les autres données internes ERP restent absentes de cette vue client. |
| E76-CA-07 | Session support active | Consulte ou recharge une page, sur PC et mobile | Le bandeau support reste visible avec cible, mode, environnement, échéance et sortie ; navigation, erreurs et retours ne masquent pas l'identité représentée. Le support est identifiable autrement que par la couleur. |
| E76-CA-08 | Session en consultation | Tente une mutation, y compris par appel direct ou traitement déclenché à l'ouverture d'écran | Aucune écriture métier, consommation, communication externe ni modification de préférence du client n'a lieu. Seules les traces et données de gestion de la session support sont autorisées. |
| E76-CA-09 | Session ouverte en consultation et opérateur habilité | Demande puis confirme l'intervention | Le changement est explicite, visible et audité ; les actions possibles sont l'intersection des droits actuels de la cible et des actions support autorisées. Le mode n'est jamais hérité d'une ancienne session. |
| E76-CA-10 | Session en intervention | Exécute une action autorisée, interdite, répétée ou dont le résultat est incertain | Les règles métier et contrôles de concurrence/idempotence existants s'appliquent ; aucune élévation de droit ni double effet. Les opérations exclues restent refusées côté serveur, même si la cible pourrait les réaliser seule. |
| E76-CA-11 | Sessions ERP, support et éventuelles sessions client normales coexistantes | Ouvre deux contextes, recharge, revient dans un onglet ancien ou utilise la PWA | Chaque action garde sa cible et son mode vérifiés ; pas de substitution silencieuse de compte, de cache partagé entre cibles, ni d'écrasement de session normale. Aucun abonnement push ou accès durable du client n'est créé sur l'appareil du support. |
| E76-CA-12 | Session support active | Quitte, atteint l'échéance ou perd sa session ERP d'origine | L'accès support est invalidé côté serveur ; les appels suivants et anciens onglets sont refusés, sans renouvellement silencieux. La sortie volontaire ramène au dossier ERP si la session interne reste valide ; les sessions normales du client sont conservées. |
| E76-CA-13 | Session active | Retrait du droit opérateur, révocation administrative, désactivation de cible ou retrait de rattachement | Les requêtes suivantes ne conservent aucun droit retiré. Un changement de rôle, module ou périmètre réduit immédiatement les possibilités selon les règles existantes. Aucun jeton déjà émis ne permet de contourner ce retrait. |
| E76-CA-14 | Opérateur et cible authentifiés par le serveur | Consulte puis agit ou rencontre un refus | La trace relie opérateur réel, identité représentée, application, rattachement, environnement, mode, motif, session, horodatage et résultat ; une action métier n'est jamais attribuée au seul client. Les secrets et contenus sensibles ne sont pas copiés dans les journaux. |
| E76-CA-15 | Opérateur habilité à l'audit | Recherche une intervention dans l'ERP | Recherche paginée et filtres par opérateur, cible, période et session permettent de reconstituer début, changement de mode, actions et fin. Les refus restent consultables après rollback ; l'accès aux traces est contrôlé. |
| E76-CA-16 | Session active, action en vol | Fait concourir expiration/révocation et commande métier | Une règle de priorité est spécifiée et testée ; aucune nouvelle action n'est autorisée après retrait effectif. Les effets déjà validés et leur double attribution sont conservés, sans rejeu implicite lors de la reprise. |
| E76-CA-17 | Opérateur intervenant à la suite d'une demande reçue | Termine une session passée en intervention | Le récapitulatif indique qui a agi, pour quel compte, quand, sur quel dossier et avec quel résultat. Pour un import Animation, les gestionnaires ayant actuellement le droit de consulter les imports de l’organisation et de la commune du lot peuvent le lire. Si le récapitulatif échoue, l'ERP le signale et permet sa reprise sans rejouer les actes. |
| E76-CA-18 | Environnement isolé, profils internes et cibles représentatives | Exécute les suites unitaires, intégration et parcours fonctionnels des deux applications | Succès, refus, frontières de droits, isolation des sessions, retraits concurrents et audit sont couverts. Les parcours client ordinaires et ERP restent opérationnels ; les simulations et contrôles externes non exécutés sont distingués. |

## Impacts à instruire

| Sujet | Impact initial et source à examiner |
| --- | --- |
| Applications et domaine propriétaire | **Concernés :** backend (domaine Identité/Accès, orchestration, ERP, contrôles des services métier), Pro et Animation (session, navigation, bandeau et erreurs). Marketplace/Live **sans modification fonctionnelle prévue**, car hors cibles ; isolation des sessions sur domaines voisins à examiner. |
| API et consommateurs | **Concernés :** ouverture/transfert/fin/révocation, contexte de session, commandes et audit. Producteur backend ; consommateurs ERP, Pro, Animation. Définir les contrats documentaires canoniques puis les contrats embarqués des consommateurs, sans accepter d'identité opérateur déclarée librement par le navigateur. |
| Persistance, migrations et données existantes | **À examiner :** représentation de la délégation, révocation, durée, motif et double attribution des actions ; migration éventuelle, compatibilité avec les historiques existants et conservation. Ne pas réécrire les anciennes attributions utilisateur. |
| Générateur de démonstration et fixtures | **Concernés :** opérateur autorisé/interdit, deux commerces, compte principal/salarié, Animation seule/Coffrets/mixte, deux organisations et droits organisateur différents. Générateur/restaurateur à examiner dans le backend ; aucune création réelle dans ce cadrage. |
| Documentation fonctionnelle | **Concernée :** guides ERP/support, Pro et Animation ; expliquer finalité, entrée, limites, mode, durée et sortie, ainsi que l'information du client. Source unique dans ce dépôt, lecteurs/bundle ERP à vérifier lors de publication. |
| Exploitation et déploiement | **Concernés :** origines HTTPS, session/cookies/PWA, activation par environnement, révocation d'urgence, traces et conservation. Migrations et ordre backend/ERP puis consommateurs à spécifier ; aucune variable, durée ou valeur de secret inventée comme configuration déjà existante. |
| Performance et volumétrie | **Concernées :** contrôle de droits à chaque requête, persistance/audit, recherche paginée et purge. Budgets, bornes, index et preuves N/10N/charge mixte à définir selon la [convention transverse](../../architecture/transverse/performance-volumetrie.md). |

## Arbitrages

| Arbitrage | Décision retenue |
| --- | --- |
| E76-ARB-01 — Consultation ou intervention | Validé le 1er novembre 2026. Consultation par défaut et intervention explicite et tracée. |
| E76-ARB-02 — Habilitations | Validé le 23 novembre 2026. Administrateur, Backoffice et Backoffice + Finance après réauthentification ERP. Lecteur et Finance seul sont exclus. |
| E76-ARB-03 — Actions d'intervention | Validé le 23 novembre 2026. Animation : parcours d'import de commerçants et enregistrement d'un brouillon d'actualité. Pro : enregistrement du brouillon de page publique et soumission à modération. La consultation couvre les écrans utiles à ces parcours. L'import complet sert de recette transverse. |
| E76-ARB-04 — Durée et information | Validé le 23 novembre 2026. 30 minutes au maximum ou 15 minutes d'inactivité. Motif obligatoire, référence facultative, demande déjà reçue suffisante. Récapitulatif client consultable pendant 180 jours après la fin de l’intervention selon les droits de lecture de CA-17. La révocation explicite suspend les lignes restantes d'un import lancé. Le journal interne suit la règle commune T8, avec un plafond de 12 mois calendaires par événement. |

## Préparation de l’implémentation

La spécification relie les critères aux règles de domaine, contrats, consommateurs,
fixtures et preuves attendues selon le [cycle d'epic](../../organisation/cycle-epic.md).
Le bilan consigne les mesures de charge locales et les vérifications restant à réaliser sur l’environnement cible.
