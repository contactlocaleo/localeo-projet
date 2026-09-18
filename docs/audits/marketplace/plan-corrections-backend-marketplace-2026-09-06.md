# Corrections pré-production — répartition backend / Marketplace

> Actualisation du 7 septembre 2026 : les dix constats MARKET sont corriges et testes localement. Voir le [registre des commits, preuves et conditions de livraison](suivi-corrections-backend-marketplace-2026-09-06.md). Le texte ci-dessous conserve l'etat historique du 6 septembre ; il ne constitue pas le statut actuel du deploiement.

Date : 6 septembre 2026. Référence : [compte rendu d'audit](audit-preproduction-2026-09-06.md), Marketplace `ecb6d56`, backend `728be26` avec modifications locales d'activation identifiées dans le rapport.

Ce document conserve le plan initial. Son execution et les decisions de contrat retenues sont suivies dans le registre actualise ci-dessus et les specifications correctives. Les controles sur la version deployee restent requis.

## Répartition synthétique

**Principalement Marketplace :** MARKET-001, MARKET-003, MARKET-005 et MARKET-006.

**Principalement backend :** MARKET-007, MARKET-008 et MARKET-010.

**Correction coordonnée backend + Marketplace :** MARKET-002, MARKET-004 et MARKET-009.

« Principalement » désigne le propriétaire du défaut. Les tests d'intégration et la recette peuvent concerner les deux dépôts. Localeo Live appartient au dépôt Marketplace.

| ID | Sujet | Backend | Marketplace / Live | Exploitation | Priorité |
| --- | --- | --- | --- | --- | --- |
| MARKET-001 | Jetons dans Analytics | Préserver la sécurité des liens ; migration des capacités si nécessaire | Bloquer les émissions sensibles et normaliser les routes | Désactivation effective du tag, configuration Google, vérification des flux | P0 |
| MARKET-002 | Retour de paiement | Concevoir un accès de retour sécurisé B2C/Pro et une projection adaptée | Acquérir/transmettre l'accès, afficher le statut serveur, gérer la reprise | Déployer un couple compatible | P0 |
| MARKET-003 | Faux succès Pro | Fournir le statut faisant autorité via MARKET-002 | Supprimer le succès par défaut et les preuves provenant seulement de l'URL/cache | Recette Pro et crédit intégral | P0 |
| MARKET-004 | Données dans URL API | Accepter JSON et headers ; publier le contrat | Migrer les appels ; aucun fallback silencieux en query | Revue des traces et durée de conservation | P1, livraison coordonnée |
| MARKET-005 | Retrait Analytics | Pas de correction métier backend identifiée | Propager le retrait, synchroniser les onglets | Configurer et vérifier le comportement du fournisseur | Avant réactivation Analytics |
| MARKET-006 | Priorité des `.env` | Pas de correction métier backend identifiée | Corriger le générateur/configuration de build | Valider la configuration finale de chaque mode de livraison | P1 ; contrôle avant livraison |
| MARKET-007 | Inscription non rejouable | Véritable idempotence et récupération sécurisée | Conserver la clé/payload lors d'une reprise incertaine ; exploiter le résultat | Aucun changement requis identifié | P1 |
| MARKET-008 | Continuité participant | Projection dédiée après validation du jeton | Présenter les états métier et la continuité attendue | Recette avec abonnement expiré | P1 |
| MARKET-009 | Pro sans crédit rejeté | Clarifier et valider les conditions d'achat | Collecter/transmettre les conditions sans dépendre d'une session crédit | Maintenir le flag désactivé jusqu'à recette | Avant activation crédit |
| MARKET-010 | Quantité non bornée | Validation API/domaine et contraintes appropriées | Refléter les mêmes bornes pour guider l'utilisateur | Vérifier les contraintes effectivement appliquées | P1 |

## 1. Corrections dans l'application Marketplace

### MARKET-001 — Empêcher l'émission des capacités d'accès

**Fichiers :** [analytics.js](../../../../localeo-marketplace/src/services/analytics.js), [AnalyticsRouteTracker.jsx](../../../../localeo-marketplace/src/components/AnalyticsRouteTracker.jsx), [App.jsx](../../../../localeo-marketplace/src/App.jsx), pages et composants qui appellent `trackEvent`.

Travail recommandé :

1. Prévoir la suspension effective d'Analytics comme solution immédiate d'ouverture.
2. Identifier toutes les routes contenant des capacités : participant, feedback, lien court, ajout Live, consultation, activation et retour de paiement.
3. Remplacer les chemins variables par des routes canoniques pour les seules mesures autorisées ; ne jamais inclure un jeton brut, même tronqué.
4. Contrôler également `page_title`, les labels libres et les émissions automatiques du tag.
5. Traiter le cas d'un tag déjà chargé avant navigation vers une page sensible. Ne pas considérer un simple montage conditionnel du tracker comme une garantie d'arrêt du fournisseur.

**Acceptation :** avec consentement préalablement accordé, navigation directe et SPA sur chaque parcours sensible ; aucune sentinelle token/email/téléphone dans les événements applicatifs ou requêtes Analytics. Un test du wrapper seul ne clôt pas le constat.

**Backend :** aucune réécriture de l'autorisation n'est nécessaire pour la suspension immédiate. Un éventuel échange de lien en accès temporaire constitue un chantier coordonné distinct.

### MARKET-003 — Confirmation Pro exclusivement fondée sur le serveur

**Fichiers :** [ConfirmationProPage.jsx](../../../../localeo-marketplace/src/pages/ConfirmationProPage.jsx), [CommandeProPage.jsx](../../../../localeo-marketplace/src/pages/CommandeProPage.jsx), [paymentStatus.js](../../../../localeo-marketplace/src/services/paymentStatus.js), [RetourPaiementPage.jsx](../../../../localeo-marketplace/src/pages/RetourPaiementPage.jsx).

Travail recommandé :

1. Utiliser un statut initial `pending` ou inconnu ; ne jamais considérer l'absence de statut comme un succès.
2. Supprimer les sources de preuve limitées à `statut=succes`, à `quantite` ou à un booléen enregistré dans le navigateur.
3. Charger l'achat identifié par le contrat de retour, y compris après crédit intégral sans session Stripe.
4. Distinguer « paiement confirmé », « en attente », « échec confirmé » et « résultat impossible à vérifier ».
5. N'afficher les coffrets disponibles et l'envoi d'email que si le contrat serveur permet réellement ces affirmations ; un email mis en file n'est pas une preuve de livraison.
6. Réexaminer les confirmations à partir d'un cache ancien et les retours arrière.

**Acceptation :** `/confirmation-pro?quantite=10` sans accès valide ne confirme rien ; 401/403/500/timeout n'affichent pas de succès ; l'achat confirmé s'affiche correctement ; un financement intégral par crédit suit un parcours authentifié.

**Dépendance :** le garde d'affichage peut être corrigé immédiatement ; la récupération complète dépend de MARKET-002.

### MARKET-005 — Rendre le retrait de consentement effectif

**Fichiers :** [analytics.js](../../../../localeo-marketplace/src/services/analytics.js), [AnalyticsConsentBanner.jsx](../../../../localeo-marketplace/src/components/AnalyticsConsentBanner.jsx), [LiveApp.jsx](../../../../localeo-marketplace/src/live/LiveApp.jsx).

Travail recommandé : propager le choix au tag chargé selon son mode de consentement ; bloquer les événements applicatifs ; gérer les changements `storage` entre onglets ; vérifier navigation et rechargement après retrait. Examiner la configuration Google, pas seulement le code du wrapper.

**Acceptation :** aucune mesure non autorisée après retrait dans l'onglet courant ou un autre onglet. Contrôler les émissions automatiques et les cookies concernés. Conserver Analytics désactivé tant que cette preuve n'est pas acquise.

### MARKET-006 — Harmoniser la configuration de production

**Fichiers :** [write-app-config.cjs](../../../../localeo-marketplace/scripts/write-app-config.cjs), [vite.config.mjs](../../../../localeo-marketplace/vite.config.mjs), [runtimeConfig.js](../../../../localeo-marketplace/src/services/runtimeConfig.js), [server.cjs](../../../../localeo-marketplace/server.cjs).

Travail recommandé :

1. Utiliser une résolution commune ou compatible avec Vite : variables du processus prioritaires, puis fichiers spécifiques au mode devant les fichiers génériques.
2. Tester les priorités avec des fixtures fictives, sans dépendre des `.env` réels d'un développeur.
3. Définir explicitement les clés destinées au navigateur ; réduire la portée de `envPrefix`.
4. Vérifier la destination API et l'environnement final pour le mode statique et le serveur Node.
5. Séparer la validation de configuration de la génération de fichiers afin de pouvoir contrôler le résultat sans mutation.

**Acceptation :** une `.env.local` générique ne remplace pas la production ; les configurations statique et Node sont cohérentes ; aucune valeur serveur fictive sensible n'est incorporée au bundle.

## 2. Corrections principalement côté backend

### MARKET-007 — Implémenter l'idempotence d'inscription

**Fichiers :** [animation_locale_api.py](../../../../localeo-backend/app/api/animation_locale_api.py), [participants_animation.py](../../../../localeo-backend/app/application/animation_locale/services/participants_animation.py), mécanisme d'idempotence et repositories du domaine animation.

Travail recommandé :

1. Distinguer la corrélation d'une requête de sa clé d'idempotence métier.
2. Associer clé, animation, empreinte du payload et résultat dans une transaction.
3. Même clé + même payload : rejouer un résultat exploitable. Même clé + payload différent : conflit explicite.
4. Préserver l'unicité métier des participants sous concurrence.
5. Concevoir une récupération du lien sans conserver arbitrairement un jeton brut non protégé ni révéler un accès par simple connaissance d'un email.
6. Garantir qu'une reprise ne multiplie pas les emails ou participants.

**Acceptation backend :** deux appels simultanés et un retry après perte de réponse produisent un participant et un résultat récupérable ; le changement de payload avec la même clé est refusé ; connaître l'email d'un inscrit ne donne pas son jeton.

**Adaptation Marketplace :** conserver clé et payload tant que le résultat est incertain ; ne pas renouveler implicitement la clé après une simple modification de champ sans clarifier la demande précédente ; afficher la reprise et exploiter le résultat serveur.

### MARKET-008 — Préserver l'accès participant après retrait public

**Fichiers :** [animation_locale_api.py](../../../../localeo-backend/app/api/animation_locale_api.py), [participants_animation.py](../../../../localeo-backend/app/application/animation_locale/services/participants_animation.py), [catalogue_animations_publiques.py](../../../../localeo-backend/app/application/animation_locale/services/catalogue_animations_publiques.py).

Travail recommandé : après validation du jeton, construire une projection participant distincte de l'éligibilité du catalogue. Préserver la règle `MKTANIM-ARB-02` : la fin de visibilité publique ne supprime pas automatiquement l'accès d'un participant existant. Définir explicitement le comportement pour expiration de l'abonnement, commune dépubliée, animation clôturée ou annulée, sans exposer la configuration interne.

**Acceptation :** participant valide encore accessible après expiration d'abonnement ; animation absente du catalogue public ; jeton expiré/révoqué refusé ; aucun accès à un autre participant.

**Adaptation Marketplace :** vérifier [AnimationParticipantPage.jsx](../../../../localeo-marketplace/src/pages/AnimationParticipantPage.jsx) et Live sur ces états ; une animation retirée de la découverte ne doit pas être confondue avec un jeton invalide.

### MARKET-010 — Valider les quantités avant tout effet métier

**Fichiers :** [paiements_api.py](../../../../localeo-backend/app/api/paiements_api.py), [initialiser_paiement.py](../../../../localeo-backend/app/application/gestion_achats/use_cases/initialiser_paiement.py), [achat_coffret.py](../../../../localeo-backend/app/domaine/gestion_achats/entities/achat_coffret.py), modèles et migrations concernés.

Travail recommandé : définir une borne minimale et un plafond métier ; les appliquer dans le schéma d'entrée et le domaine avant calcul/persistance ; garder des montants entiers en centimes et cohérents ; ajouter les contraintes de base pertinentes avec stratégie de migration des données existantes.

**Acceptation :** zéro, négatif, décimal et quantité excessive refusés avant création d'achat, réservation de crédit ou appel Stripe ; quantité maximale autorisée traitée correctement. Aucun test ne doit déclencher de paiement réel.

**Adaptation Marketplace :** mêmes limites affichées dans le formulaire Pro. Cette validation UI ne remplace jamais celle du serveur.

## 3. Corrections coordonnées entre les deux dépôts

### MARKET-002 — Nouveau contrat sécurisé de retour de paiement

**Backend propriétaire du contrat ; Marketplace propriétaire du parcours utilisateur.**

Fichiers backend : [achats_api.py](../../../../localeo-backend/app/api/achats_api.py), [consulter_achat_depuis_session_checkout.py](../../../../localeo-backend/app/application/gestion_achats/use_cases/consulter_achat_depuis_session_checkout.py), [initialiser_paiement.py](../../../../localeo-backend/app/application/gestion_achats/use_cases/initialiser_paiement.py), [paiement_gateway.py](../../../../localeo-backend/app/infrastructure/paiement/paiement_gateway.py), schémas API.

Fichiers Marketplace : [api.js](../../../../localeo-marketplace/src/services/api.js), [RetourPaiementPage.jsx](../../../../localeo-marketplace/src/pages/RetourPaiementPage.jsx), [ConfirmationPage.jsx](../../../../localeo-marketplace/src/pages/ConfirmationPage.jsx), [ConfirmationProPage.jsx](../../../../localeo-marketplace/src/pages/ConfirmationProPage.jsx), [CommandeProPage.jsx](../../../../localeo-marketplace/src/pages/CommandeProPage.jsx), [CoffretPage.jsx](../../../../localeo-marketplace/src/pages/CoffretPage.jsx).

**Orientation recommandée, à concevoir :** délivrer un accès de retour spécifique, à portée minimale et durée bornée, lié à l'achat ou à la tentative checkout. Il doit permettre de vérifier le résultat sans donner automatiquement tous les droits de gestion Pro. Le choix entre jeton dédié, échange de capacité et autre session de retour doit être documenté ; aucun de ces mécanismes n'est déclaré existant par ce document.

Backend :

1. Définir acquisition, portée, durée, rejeu autorisé et révocation de l'accès de retour.
2. Contrôler le lien entre cet accès, l'achat et la session checkout ; ne jamais croire `achat_id` fourni par le client.
3. Fournir une projection minimale du statut serveur et de la disponibilité des droits, sans données d'une autre commande.
4. Couvrir paiement particulier, Pro, crédit intégral et webhook retardé.
5. Documenter les statuts, headers, erreurs et conditions de polling dans OpenAPI.

Marketplace :

1. Acquérir et transmettre cet accès ; ne pas se contenter d'un `session_id`.
2. Retirer les valeurs sensibles de l'URL après acquisition lorsque le contrat le prévoit.
3. Gérer expiration, absence d'accès, refus, statut en attente et reprise réseau.
4. Ne pas transformer une impossibilité de vérification en échec définitif ni en succès.
5. Mettre à jour les fixtures qui simulent aujourd'hui une réponse sans vérifier les headers.

**Acceptation commune :** parcours réel en environnement de recette isolé B2C/Pro/crédit intégral ; retour avant webhook ; refresh ; mauvais jeton ; session d'un autre achat ; 401/403 ; timeout et reprise. Aucun nouvel achat automatique lors d'une incertitude.

**Ordre :** contrat → implémentation backend testée → mise à disposition compatible → client → recette du couple. Prévoir le sort des anciens liens. Ne pas désactiver l'autorisation pour rétablir la compatibilité.

### MARKET-004 — Migrer les transports sensibles

Backend : remplacer les paramètres personnels du checkout par un schéma JSON validé ; accepter le jeton QR via header dédié ou Bearer documenté ; conserver quotas et idempotence ; mettre à jour OpenAPI.

Marketplace : remplacer `postAsQuery` pour le checkout et `{ token }` pour le détail QR ; conserver les headers d'idempotence, de crédit et Live requis ; vérifier qu'aucun retry ne réintroduit les données dans l'URL.

Exploitation : examiner les traces susceptibles de contenir des URL anciennes et la durée de conservation. Une purge ou révocation ne fait pas partie d'un simple correctif de transport.

**Acceptation :** aucune sentinelle personnelle dans URL d'API ; mêmes règles métier et mêmes résultats ; absence de retour silencieux vers l'ancien contrat. Si une transition est nécessaire, ses dates et consommateurs doivent être explicites.

### MARKET-009 — Achat Pro avec et sans crédit

Backend : préciser si les conditions s'appliquent à tous les achats Pro lorsque le flag est actif ; retourner la version attendue ; vérifier consentement, organisation, session crédit et financement exclusivement côté serveur.

Marketplace : charger et présenter les conditions applicables même sans crédit existant, collecter une acceptation explicite et transmettre sa version. Ne pas déduire automatiquement une acceptation actuelle de la seule présence d'une ancienne session crédit. Couvrir absence de crédit, crédit partiel, crédit intégral et session expirée.

**Acceptation :** les quatre cas sont cohérents ; pas de débit d'une autre organisation ; refus compréhensible lorsque les conditions ne sont pas acceptées ; absence de double réservation lors des retries.

**Dépendances :** MARKET-002 et MARKET-003 pour le retour et la confirmation du financement intégral. Maintenir le flag désactivé tant que ce parcours n'est pas recetté.

## 4. Vérifications backend et exploitation distinctes des anomalies confirmées

Ces contrôles ne sont pas présentés comme des vulnérabilités démontrées. Ils restent nécessaires pour certifier l'ouverture.

| Contrôle | Responsable | Preuve attendue |
| --- | --- | --- |
| Activation concurrente | Backend | Revue/livraison des corrections locales, deux transactions concurrentes, même bénéficiaire et bénéficiaires différents |
| Unicité des droits d'instance | Backend + exploitation | Migration vérifiée, données existantes analysées, contrainte réellement installée |
| Idempotence achat et webhook | Backend | Même événement/requête en parallèle, réponse perdue, un achat logique et un ensemble de droits |
| Consommation QR | Backend | Même QR depuis deux sessions, contrôle commerçant/instance et absence de double consommation |
| Facturation | Backend + Marketplace | Droits de lecture/écriture par instance, validation exécutée, document immuable et téléchargement cloisonné |
| Révocation et caches | Backend + Marketplace | Le serveur refuse après révocation ; le frontend ne présente pas un cache comme preuve de droit actif |
| Configuration de production | Exploitation + Marketplace | Origines API/Stripe, flags, headers, versions et CORS effectivement servis |
| Reprise et rollback | Exploitation | Restauration, maintien des assets nécessaires, procédure de rollback recettée |
| Avis de dépendances | Mainteneur + autorisation d'accès externe | Contrôle actualisé autorisé ; aucune conclusion « zéro CVE » avant résultat |

## 5. Ordre de livraison recommandé

| Lot | Contenu | Dépendance | Condition de sortie |
| --- | --- | --- | --- |
| A | Suspension Analytics et garde de confirmation Pro | Aucune modification métier backend pour ces protections immédiates | Plus de fuite liée au tag désactivé ; plus de succès Pro sans preuve |
| B | Contrat retour checkout B2C/Pro | Conception commune MARKET-002 | Backend testé et contrat disponible |
| C | Client de retour + confirmations + crédit intégral | Lot B | Recette d'achat et reprise complète ; MARKET-002/003 fermés |
| D | JSON checkout et header QR | Backend compatible avant client | MARKET-004 fermé sans fallback sensible |
| E | Idempotence inscription et continuité participant | Contrats animation | MARKET-007/008 fermés |
| F | Conditions crédit et quantités | Règles métier validées ; lot C pour crédit intégral | MARKET-009/010 fermés ; activation du crédit autorisable |
| G | Consentement complet et configuration | Recette fournisseur et modes de déploiement | MARKET-005/006 fermés ; Analytics réactivable seulement après preuve |

Avant l'ouverture, fermer les P0 et vérifier les migrations et protections de concurrence. Les lots P1 peuvent être avancés lorsque leur coût ou les fonctionnalités ouvertes le justifient. La sévérité MOYENNE ne dispense pas de recette avant activation d'une fonctionnalité concernée.

## 6. Registre de suivi actualise le 7 septembre 2026

| ID | État | Preuve attendue (resultats dans le registre lie) |
| --- | --- | --- |
| MARKET-001 | Corrige et teste localement | Commit/configuration + capture des requêtes autorisées et absence de sentinelles |
| MARKET-002 | Corrige et teste localement | Contrat, commits des deux dépôts, recette B2C/Pro |
| MARKET-003 | Corrige et teste localement | Tests négatifs sans achat et tests positifs avec serveur |
| MARKET-004 | Corrige et teste localement | Tests de transport JSON/header et compatibilité |
| MARKET-005 | Corrige et teste localement | Retrait effectif, onglets et tag chargé |
| MARKET-006 | Corrige et teste localement | Matrice de priorité des environnements et artefact final |
| MARKET-007 | Corrige et teste localement | Retry/concurrence et récupération non divulguante |
| MARKET-008 | Corrige et teste localement | Participant valide après retrait public |
| MARKET-009 | Corrige et teste localement | Achat Pro avec/sans crédit et consentement versionné |
| MARKET-010 | Corrige et teste localement | Validation des bornes avant tout effet |

Les numéros de ligne cités dans le compte rendu correspondent aux sources auditées. Après correction, joindre les références de commits et les résultats de recette plutôt que de considérer les anciennes lignes comme des preuves de l'état courant.

Les commits par ID, les resultats de tests et les conditions encore requises sur la cible figurent dans le [registre de resolution](suivi-corrections-backend-marketplace-2026-09-06.md). Analytics reste suspendu ; son autorisation de reactivation ne resulte pas de cette cloture locale.
