# Specifications Epic 42 - Localeo Live

Évolution du **9 novembre 2026 — carnet personnel unifié** portée par
[E73-EVO-LIVE-CARNET](../epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-9-novembre-2026--carnet-personnel-unifié-e73-evo-live-carnet).
**Mon carnet** réunit les animations, coffrets et lots dont l’appareil possède
les accès ; **Découvrir** ouvre le programme et les commerces, **Communes**
gère les territoires. Les filtres du carnet distinguent les types, les favoris
restent de simples enregistrements publics et chaque objet ouvre son accès précis.

Sur un nouvel appareil, **Retrouver mon carnet** propose une vérification par
e-mail pour retrouver les participations encore autorisées et leurs lots
associés, sans nouveau compte. Les coffrets utilisent leur récupération propre ;
la sauvegarde reste restaurable depuis Réglages. Un état ancien de carte ne
confirme ni progression ni disponibilité : les parcours personnels revalident
les droits. Téléphone classique obligatoire conservé, tombola sans téléphone.
La réalisation et les tests propres à cette évolution figurent au
[bilan E73](../epic-73-animation-et-ou-coffrets/verification-livraison.md) ; les
anciens bilans d’E42 ne constituent pas une preuve de ce nouveau parcours.

La fiche publique d’animation évolue le **9 novembre 2026** dans
[E73-EVO-LIVE-FICHE](../epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-9-novembre-2026--fiche-animation-immersive-e73-evo-live-fiche) :
défi et conditions avant inscription, reprise de la participation exacte ou
choix explicite entre plusieurs accès, lots et partenaires en aperçu puis
consultation volontaire. Conditions ouvre directement la section ; actualiser
conserve la lecture du même contexte sans réutiliser une ancienne autorisation.
Un favori reste distinct d’une inscription. Le
[bilan E73](../epic-73-animation-et-ou-coffrets/verification-livraison.md)
porte les résultats locaux, distincts de la clôture historique d’E42.

Complément porté par E73 le **30 octobre 2026 — E73-EVO-LIVE-ACCUEIL-RAPPELS** :
accueil personnel mobile, parcours presque terminés, échéances à 72 heures et
deux rappels facultatifs indépendants. Le détail, les contrats et les critères
de cette évolution restent dans la
[spécification canonique E73](../epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-30-octobre-2026--e73-evo-live-accueil-rappels),
sans rouvrir la clôture historique du socle E42.

Évolution portée par l'epic 73 le **30 octobre 2026 — E73-EVO-LIVE-UNIQUE** :
[découverte et participations depuis Live](../epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md)
à `animations.localeo.city`, navigation mobile et communes multiples. Aucun
nouveau compte habitant ; reprise volontaire des carnets entre origines.
Le statut terminé et les bilans historiques d'E42 ne valident pas cette évolution.

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-42-localeo-live-grand-public-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

> Consolidation des exemplaires backend et Marketplace : un dossier commun,
> deux responsabilités applicatives. Les états historiques restent datés ; les
> décisions `LIVE-ARB-41` à `LIVE-ARB-51` restent à valider. Aucune décision métier
> supplémentaire n'est prise lors de cette réorganisation.

## Evolution Actualites Animation

La specification applicative de l'affichage, de l'inbox et du WebPush des actualites rattachees aux animations est centralisee dans [Epic 41 - Specification Localeo Live](../epic-41-api/actualites-localeo-live.md).

## Objet

Ce dossier cadre `Localeo Live`, la PWA grand public destinee aux clients finaux Localeo. L'application est distincte de `Localeo Control`, du portail partenaire Animation et de l'application commercant.

## Documents

- [Évolution installation et mise à jour PWA du 29 septembre 2026](../installation-mise-a-jour-pwa.md)

- [Specification backend et API](backend-api.md)
- [Specification frontend PWA](frontend-pwa.md)
- [Carnet partage - specification backend](carnet-partage-backend.md)
- [Carnet partage - specification frontend](carnet-partage-frontend.md)
- [Registre des arbitrages](registre-arbitrages.md)
- [Backlog Epic 42](../../roadmap/terminees/epic-42-localeo-live-grand-public-backlog.md)

## Objectif MVP

Le client peut installer facilement Localeo Live depuis la marketplace et retrouver en priorité ses coffrets et participations dans `Mon carnet`. `Découvrir` donne accès aux animations locales et aux actualités, dont celles rattachées aux animations. Il peut s'inscrire, suivre ses participations et gérer ses notifications WebPush. La refonte Marketplace de septembre remplace l'ancienne navigation `En direct`, `Passeports`, `Animations`, `Réglages` ; les filtres métier restent décrits dans la spécification frontend.

## Principes

- mobile first, installable et accessible ;
- consultation publique possible sans compte lorsque le risque le permet ;
- aucun compte au MVP : acces par token et sauvegarde locale volontaire des liens ;
- aucune duplication des referentiels coffrets, commercants, communes et animations ;
- separation stricte des notifications grand public, commercants et Localeo Control ;
- donnees personnelles minimales et consentements explicites ;
- verification locale par le verrouillage securise de l'appareil avant chaque affichage d'un QR personnel de coffret ou de participation.

## Evolution carnet partage

L'evolution post-MVP du carnet permet de persister et synchroniser les passeports/coffrets et participations entre plusieurs appareils sans creer de compte client. Elle repose sur un carnet pseudonyme cote backend, une installation et un secret distincts par appareil, un appairage explicite et une recuperation par passkey lorsqu'aucun ancien appareil n'est disponible.

Les responsabilites sont separees dans deux specifications :

- le backend porte la source de verite, les autorisations carnet-ressource, l'appairage, la revocation et la verification des passkeys de recuperation ;
- le frontend porte l'activation volontaire, la migration IndexedDB, les parcours multi-appareils, les etats hors ligne et la protection locale des QR.

## Etat du cadrage

Les arbitrages `LIVE-ARB-01` a `LIVE-ARB-40` sont valides. Les propositions `LIVE-ARB-41` a `LIVE-ARB-51` cadrent le carnet partage et restent a valider avant implementation. Le MVP utilise une selection manuelle de commune, sans geolocalisation, et la gestion des publications editoriales est realisee depuis le backend/back-office. `LIVE-ARB-38` couvre l'ajout direct d'un coffret. `LIVE-ARB-39` dissocie desormais la creation de l'installation du consentement WebPush et fournit une facade Live explicite pour les participations. `LIVE-ARB-40` impose une verification locale WebAuthn avant chaque affichage d'un QR personnel, sans compte ni nouvelle authentification client cote serveur. Le bilan backend annonce les lots initiaux B0-B8 et leur contrat OpenAPI terminés ; l'évolution B9-B11 reste une conception à arbitrer. Le prototype frontend et sa refonte sont décrits ci-dessous. Leur existence ne permet pas de déclarer tous les lots frontend livrés : l'état de recette doit être contrôlé dans les backlogs de chaque application.

## Historique et refonte frontend — origine Marketplace

Le bilan du 19 août 2026 décrit un prototype navigable sous `/live/*` : shell,
feed filtrable, passeport graphique, catalogue et participation, inbox,
préférences, manifeste, icône dérivée du marqueur Localeo, service worker limité
à `/live/`, vignette d'acquisition et retour vers `/accueil`. Il cite des données
de démonstration, l'identité Nunito Sans / Caveat / bleu / orange et des premiers
contrôles responsive, tactiles, clavier et `prefers-reduced-motion`. Ces mentions
caractérisent cette livraison historique, pas une nouvelle charte ni une preuve
de fonctionnement de bout en bout.

La refonte de septembre fait du carnet l'entrée principale, conserve les
participations distinctes d'une famille et facilite l'ajout explicite sans double
confirmation. Elle n'introduit ni compte ni synchronisation multi-appareils.
Voir [le parcours frontend](frontend-pwa.md)
et [le backlog Marketplace](../../roadmap/terminees/epic-42-localeo-live-grand-public-backlog.md).

## Lots d'implementation

Le backlog distingue deux trajectoires :

- backend initial : `B0` a `B8`, du contrat OpenAPI a la readiness production ;
- backend carnet partage : `B9` a `B11`, de la persistance a la recuperation WebAuthn ;
- frontend PWA initial : `F0` a `F8`, du module `/live` a la recette PWA ;
- frontend carnet partage : `F9` a `F11`, de l'activation a la recette multi-appareils.

Les couples `B1/F4`, `B2/F5-F6`, `B3/F3` et `B4-B5/F7` portent les recettes integrees. Le detail et les dependances sont documentes dans le backlog Epic 42.

## Documents complémentaires du dossier

- [E-mail dans les détails personnels Localeo Live](email-achat-inscription.md)
- [Localeo Live — plusieurs inscriptions à une animation](inscriptions-multiples.md)
- [openapi.json](openapi.json)

[Retour à l’index des spécifications](../INDEX.md)
