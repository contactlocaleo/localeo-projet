# Architecture CSS de la marketplace

Ce document fixe la cible de la refonte progressive de `marketplace.css`. La migration doit rester incrémentale : chaque extraction conserve le rendu, passe le build et couvre les parcours concernés avant la suppression des règles historiques.

## Ordre de la cascade

Les feuilles globales sont chargées dans cet ordre par `src/main.jsx` :

1. `tokens.css` : variables partagées, sans sélecteur de composant ;
2. `components/*.css` : primitives réellement partagées ;
3. `site-base.css` : reset léger, typographie, structure globale et adaptations responsive historiques ;
4. `marketplace.css` : règles historiques en attente de migration ;
5. `marketplace-digital.css` : expérience numérique spécialisée ;
6. `marketplace-system.css` : composition publique actuelle ;
7. `performance.css` : ajustements de chargement et de rendu.

Les styles propres à une page devront ensuite être importés par la page ou le composant racine concerné afin de suivre le découpage JavaScript des routes.

L'ordre temporaire `components` puis `site-base` préserve les surcharges responsive déjà présentes dans la feuille historique. Il pourra devenir `base` puis `components` une fois ces adaptations rapprochées de leurs propriétaires.

## Responsabilités

- `tokens.css` est l'unique source des couleurs, espacements, rayons, ombres et largeurs réutilisés.
- `site-base.css` ne contient aucun style métier.
- `components/` accueille seulement les primitives utilisées par plusieurs familles de pages.
- `domains/` regroupe les styles d'une famille fonctionnelle partagée par plusieurs routes et est importé par son composant racine.
- `pages/` accueillera les styles spécifiques à une route ou à une famille fonctionnelle.
- `marketplace.css` est une couche de compatibilité temporaire. Aucun nouveau style ne doit y être ajouté.

## Règles de contribution

- Concevoir mobile-first et regrouper les adaptations d'un composant avec son style principal.
- Réutiliser les variables existantes avant d'ajouter une valeur brute répétée.
- Éviter les sélecteurs dépendant d'une profondeur DOM et limiter la spécificité.
- Ne pas ajouter de `!important` ; traiter la cause dans la cascade.
- Garder les états `hover`, `focus-visible`, `disabled`, chargement et erreur près du composant.
- Respecter `prefers-reduced-motion` pour toute animation non essentielle.
- Supprimer la règle d'origine dans `marketplace.css` dès qu'une extraction est validée.

## Stratégie de migration

Chaque lot porte sur une famille cohérente : primitives, accueil, catalogue, coffrets, animations, commerçants, compte. Pour chaque lot :

1. identifier les sélecteurs utilisés et leurs surcharges responsive ;
2. déplacer les règles dans leur propriétaire cible ;
3. supprimer les doublons et déclarations mortes ;
4. vérifier le build et les tests Playwright représentatifs ;
5. comparer le poids CSS produit et le nombre de `!important` restant.

L'introduction de `@layer` est différée jusqu'à la migration complète des grandes sections : mélanger des règles historiques non stratifiées avec des règles stratifiées modifierait leur priorité dans la cascade.

## Lots migrés

- Fondations : tokens centralisés et primitives d'actions extraites.
- Animations publiques : fondations, responsive, catalogue, détail, règlement et inscription regroupés dans `styles/domains/animations.css` et chargés avec `PublicAnimations`.
- Accueil : finitions, responsive, fil d'activité et surcharges système regroupés dans `styles/pages/home.css`, chargé avec `AccueilPage` sans sélecteur résiduel dans `marketplace-system.css`.
- Ville : finitions, responsive et surcharges système regroupés dans `styles/pages/city.css`, chargé avec `CityPage` sans sélecteur résiduel dans `marketplace-system.css`.
- Catalogue des coffrets : finitions desktop, correctifs mobiles historiques et composition système regroupés dans `styles/pages/coffrets.css`, chargé uniquement avec `CoffretsPage`. Aucun sélecteur `marketplace-shell--coffrets` ne reste dans les deux feuilles historiques globales.
- Fiche coffret : confinement mobile, surface produit, panneau d'achat, galerie immersive, cartes éditoriales, correctifs tardifs et composition système regroupés dans `styles/pages/coffret-detail.css`, chargé uniquement avec `CoffretPage`. Aucun sélecteur `marketplace-shell--coffret-detail` ne reste dans les feuilles historiques globales ; la finition générique des champs reste partagée et les mouvements propres à la fiche respectent `prefers-reduced-motion`.
- Page Commerçant : portrait, moments du commerce, coffret vedette, récit détaillé, densité mobile, correctifs tardifs et composition système regroupés dans `styles/pages/merchant.css`, chargé uniquement avec `CommercantPage`. Aucun sélecteur `marketplace-shell--merchant` ne reste dans les feuilles historiques globales et les mouvements concernés respectent `prefers-reduced-motion`.
- Confirmation particulier, étape 1 : thème consommateur, statuts, panneaux, textes et actions regroupés dans `styles/pages/confirmation.css` au niveau de cascade historique, sans embarquer les variantes professionnelle et suivi.
- Confirmations, étape 2 : structure moderne partagée, panneaux, récapitulatifs, primitives de statut, copie et assistance regroupés dans `styles/domains/confirmation-base.css`. Le chargement reste temporairement global pour conserver la cascade tant que les thèmes professionnelle et suivi ne sont pas entièrement extraits.
- Confirmation professionnelle, étape 3 : thème, actions, états, composition mobile et correctifs de page regroupés dans `styles/pages/confirmation-pro.css`, chargé uniquement avec `ConfirmationProPage`. Les anciens styles `confirmation-pro-nextsteps` et `grid--pro-summary`, sans consommateur JSX, ont été supprimés.
- Suivi de coffret, étape 4 : thème de parcours, progression, prochaine découverte, code de secours, timeline, prestations et adaptations mobiles regroupés dans `styles/pages/coffret-instance.css`, chargé uniquement avec `CoffretInstancePage`. Le bouton Localeo Live reste partagé avec la vue QR et l'ancien composant `marketplace-journey-list`, sans consommateur JSX, a été supprimé.
- Confirmations, étape 5 : `styles/domains/confirmation-base.css` est importé uniquement par les trois routes qui le consomment ; le thème particulier `styles/pages/confirmation.css` quitte également le point d'entrée global. Chaque page charge d'abord le socle puis son thème pour préserver la cascade.
- Commande professionnelle : hero, coffret sélectionné, formulaire, quantités rapides, synthèse et CTA mobile regroupés dans `styles/pages/commande-pro.css`, chargé uniquement avec `CommandeProPage`. Les anciens styles `pro-order-reference`, sans consommateur JSX, et une règle de breadcrumb impossible ont été supprimés ; les élévations respectent désormais `prefers-reduced-motion`.
- Gestion professionnelle : récapitulatif, KPIs, progression d'activation, liste des coffrets et workflow d'affectation regroupés dans `styles/pages/mes-coffrets-pro.css`, chargé uniquement avec `MesCoffretsProPage`. L'ancien hero, les métadonnées de détail non rendues et les sous-composants avancés sans consommateur JSX ont été supprimés.
- Activation professionnelle : carte d'activation, confirmation, actions responsive et impression ciblée regroupées dans `styles/domains/activation-pro.css`, partagé uniquement par `ActiverCoffretPage` et `ActivationConfirmeePage`. Les anciens parcours et callouts sans consommateur JSX ont été supprimés, et la confirmation ne dépend plus implicitement du thème complet de confirmation pro.
- Retours et statuts de paiement : le socle léger de confirmation (conteneur, erreur, grille, cartes et actions) est regroupé dans `styles/domains/confirmation-shell.css`, chargé uniquement par les cinq routes de confirmation, statut et suivi qui le consomment. `RetourPaiementPage` conserve le loader global partagé et redirige vers le statut ou la confirmation appropriée.
- QR et consultation : l'impression est isolée dans `styles/pages/qr-print.css` et la vue 360 du coffret dans `styles/pages/coffret-qr.css`. Chaque route ne charge que sa propre feuille ; les règles d'impression génériques des confirmations restent globales. L'impression QR dispose désormais d'une composition mobile sur une colonne et d'un libellé orienté utilisateur.
- Pages utilitaires : le formulaire consommateur est regroupé dans `styles/pages/contact.css` avec des classes `contact-page__*` indépendantes de l'accueil. Les documents juridiques, leur sommaire fixe et leur lecture mobile sont isolés dans `styles/pages/legal.css`. Les liens juridiques partagés du pied de page et du tunnel d'achat restent globaux.
- États techniques et avis : les états vides, erreurs récupérables et pages introuvables partagent désormais `styles/components/empty-state.css`. Le formulaire d'avis prestation et ses états sont différés dans `styles/pages/feedback.css`, avec une notation mobile 2×2 et le respect de `prefers-reduced-motion`. La résolution des liens courts réutilise la structure standard de la marketplace.
- Assainissement transversal : une analyse statique conservatrice des classes littérales, templates et concaténations a retiré 534 règles et 661 sélecteurs sans consommateur de `marketplace.css`, soit 72,8 kB de source. Un second passage ne détecte plus de règle entièrement orpheline. Les animations restantes sont toutes référencées ; les styles actifs de compatibilité restent volontairement en place et devront être migrés par propriétaire plutôt que supprimés automatiquement.

## Bilan du chantier

- CSS initiale de production avant migration : 498,24 kB, 74,82 kB compressés.
- CSS initiale après migration et assainissement : 254,06 kB, 40,67 kB compressés.
- Réduction du chargement initial : 244,18 kB, soit 49,0 % ; 34,15 kB compressés, soit 45,6 %.
- Les feuilles de route extraites sont chargées à la demande avec leurs chunks JavaScript respectifs.
- `marketplace.css` reste une couche de compatibilité active : l'absence de sélecteur mort ne signifie pas que toutes ses règles sont déjà rangées dans leur propriétaire final.
