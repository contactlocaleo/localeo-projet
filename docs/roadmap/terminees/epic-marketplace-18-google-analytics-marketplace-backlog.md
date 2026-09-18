# Backlog EPIC-MARKETPLACE-18 - Google Analytics marketplace

> État de classement : **Terminée**. Identifiant distinct : `EPIC-MARKETPLACE-18` (ancien numéro local 18). La V1 est livrée ; la collecte reste suspendue par MARKET-001, comme indiqué ci-dessous.

## Perimetre

Epic source : `Epic 18. Google Analytics marketplace`

Objectif : integrer Google Analytics 4 dans la marketplace afin de mesurer le comportement utilisateur, comprendre les parcours de decouverte et de conversion, et identifier les points de friction sans exposer de donnees personnelles.

## Statut global

- Epic 18 : `V1 frontend implementee`
- Avancement : configuration runtime, consentement marketplace, chargement conditionnel GA4, pageviews SPA et evenements prioritaires V1 disponibles cote frontend.

## Vision produit

La marketplace doit pouvoir mesurer les usages reels pour piloter les decisions UX, produit et acquisition :

- quelles villes sont recherchees ;
- quels coffrets sont consultes ;
- quels commerces ou prestations contribuent a la conversion ;
- ou les utilisateurs quittent le tunnel ;
- quels parcours generent un achat, une commande pro ou une activation ;
- quels liens post-achat sont effectivement utilises.

Le suivi doit rester sobre, explicite et compatible avec les exigences de consentement. L'absence de consentement ou de configuration Analytics ne doit jamais bloquer l'application.

## Decisions initiales

- Utiliser Google Analytics 4, pas Universal Analytics.
- Utiliser deux proprietes GA4 separees : une pour la production, une pour l'environnement de test.
- Ne pas activer le suivi Analytics sur l'environnement de test public en V1.
- Charger le script Google Analytics uniquement si un identifiant de mesure est configure.
- Piloter l'activation via la configuration runtime `window.__APP_CONFIG__`.
- Ajouter un mecanisme de consentement marketplace dedie avant tout tracking Analytics.
- Bloquer totalement GA4 avant consentement en V1, sans Google Consent Mode.
- Ne pas envoyer d'evenement tant que le consentement requis n'est pas acquis.
- Ne jamais transmettre d'email, telephone, nom client, token brut, identifiant de paiement externe ou information personnelle.
- Utiliser des libelles publics normalises dans les parametres Analytics plutot que des identifiants techniques.
- Centraliser le tracking dans un service frontend dedie.
- Suivre les changements de route React Router comme des vues de page SPA.
- Conserver une nomenclature d'evenements stable et documentee.
- Prioriser les KPIs V1 suivants : recherche ville, conversion achat, commande pro, activation.
- Permettre un mode debug limite aux environnements non production.

## Configuration runtime recommandee

Ajouter les cles suivantes :

- `LOCALEO_GA_MEASUREMENT_ID` : identifiant GA4, par exemple `G-XXXXXXXXXX`.
- `LOCALEO_FEATURE_ANALYTICS_ENABLED` : active ou desactive le tracking.
- `LOCALEO_ANALYTICS_DEBUG_ENABLED` : active les logs de debug en environnement local ou test.

Points d'integration :

- `scripts/write-app-config.cjs` pour le build statique ;
- `server.cjs` pour le mode web service ;
- `.env.example` pour documenter les variables ;
- `src/services/runtimeConfig.js` pour lire les valeurs ;
- `src/services/featureFlags.js` ou un service dedie pour exposer l'etat Analytics.

Comportement attendu :

- production et test doivent utiliser des `LOCALEO_GA_MEASUREMENT_ID` distincts ;
- l'environnement de test public doit avoir `LOCALEO_FEATURE_ANALYTICS_ENABLED=false` par defaut ;
- si `LOCALEO_GA_MEASUREMENT_ID` est absent, Analytics est inactif ;
- si `LOCALEO_FEATURE_ANALYTICS_ENABLED=false`, Analytics est inactif ;
- si l'utilisateur n'a pas encore accepte le consentement Analytics, Analytics est inactif ;
- si l'utilisateur refuse le consentement Analytics, Analytics reste inactif ;
- avant acceptation, aucun script Google Analytics n'est charge et aucun signal n'est envoye a Google ;
- si Google Analytics ne charge pas, l'application continue normalement.

## Consentement et confidentialite

La V1 doit ajouter une gestion de consentement marketplace avant tout envoi d'evenement Analytics.

Comportement attendu :

- afficher une banniere ou un panneau de consentement lors de la premiere visite eligible ;
- permettre d'accepter ou refuser le suivi Analytics ;
- conserver le choix de l'utilisateur localement ;
- permettre de modifier ce choix ulterieurement depuis un point d'acces simple ;
- ne charger `gtag.js` qu'apres acceptation du suivi Analytics ;
- ne pas utiliser Google Consent Mode en V1 ;
- ne pas envoyer d'evenement retrospectif pour les pages vues avant consentement ;
- ne jamais bloquer la navigation si l'utilisateur ignore, refuse ou ferme le panneau.

Regles obligatoires :

- ne pas deposer de cookie Analytics avant consentement si le regime applicable l'exige ;
- ne pas suivre les parcours admin ou backoffice depuis la marketplace publique ;
- ne pas envoyer de PII dans les noms d'evenements, parametres ou URLs ;
- ne pas envoyer d'identifiants techniques internes dans les parametres Analytics ;
- ne pas transmettre les tokens de feedback, activation, consultation ou QR en clair ;
- anonymiser ou supprimer les query params sensibles avant pageview ;
- documenter les evenements collectes dans la politique de confidentialite si necessaire.

Donnees a exclure explicitement :

- email client ;
- telephone client ;
- nom complet ;
- adresse postale precise ;
- token de feedback ;
- token d'activation ;
- consultation token ;
- session checkout ;
- identifiant Stripe ou paiement externe ;
- commentaire client brut.

## Surfaces marketplace ciblees

### Page d'accueil

Objectif : mesurer l'orientation initiale et la recherche de ville.

Evenements possibles :
- `view_home`
- `search_city_started`
- `search_city_selected`
- `home_cta_clicked`

### Page ville

Objectif : comprendre l'interet local et la navigation vers les coffrets.

Evenements possibles :
- `view_city`
- `city_coffret_clicked`
- `city_commercant_clicked`
- `city_filter_used`

### Liste coffrets

Objectif : mesurer la comparaison et les sorties vers le detail.

Evenements possibles :
- `view_coffret_list`
- `coffret_card_clicked`
- `coffret_filter_used`
- `coffret_list_empty`

### Detail coffret

Objectif : mesurer la conviction et le demarrage de conversion.

Evenements possibles :
- `view_coffret`
- `coffret_purchase_started`
- `coffret_pro_order_started`
- `coffret_prestation_clicked`
- `coffret_commercant_clicked`

### Page commercant

Objectif : mesurer le role de reassurance du commercant.

Evenements possibles :
- `view_commercant`
- `commercant_coffret_clicked`
- `commercant_external_link_clicked`

### Tunnel paiement

Objectif : identifier les abandons et les erreurs de conversion.

Evenements possibles :
- `checkout_started`
- `checkout_redirected`
- `payment_return_viewed`
- `purchase_confirmed`
- `purchase_failed`
- `pro_order_confirmed`

### Parcours consommateur et post-achat

Objectif : mesurer l'usage effectif des liens envoyes apres achat.

Evenements possibles :
- `coffret_instance_viewed`
- `coffret_activation_started`
- `coffret_activation_confirmed`
- `qr_print_viewed`
- `feedback_page_viewed`
- `feedback_submitted`

## Plan de marquage V1

Evenements prioritaires :

- `page_view` pour chaque changement de route SPA ;
- `search_city_selected` ;
- `view_city` ;
- `view_coffret_list` ;
- `view_coffret` ;
- `coffret_purchase_started` ;
- `checkout_redirected` ;
- `purchase_confirmed` ;
- `purchase_failed` ;
- `pro_order_confirmed` ;
- `coffret_instance_viewed` ;
- `coffret_activation_confirmed` ;
- `feedback_submitted`.

Parametres autorises :

- `app_environment`
- `page_path` sans query param sensible
- `page_title`
- `ville_label` : libelle public normalise de la ville
- `coffret_label` : libelle public normalise du coffret
- `coffret_type`
- `commercant_label` : libelle public normalise du commercant
- `prestation_label` : libelle public normalise de la prestation si disponible
- `source_page`
- `payment_type` : `particulier` ou `pro`
- `result` : `success`, `failed`, `cancelled`, `pending`

Parametres interdits :

- toute donnee personnelle ;
- tout identifiant technique interne ;
- tout token ;
- tout commentaire ;
- tout identifiant de session de paiement externe ;
- toute valeur libre saisie par l'utilisateur.

Regle de nommage :

- les libelles envoyes doivent provenir des donnees publiques deja affichees a l'utilisateur ;
- les libelles doivent etre normalises avant envoi, par exemple trim, taille bornee, accents conserves ou slugifies selon convention retenue ;
- les champs libres saisis par l'utilisateur, notamment recherche de ville brute ou commentaire, ne doivent pas etre envoyes ;
- les query params trackes doivent utiliser ces libelles publics, jamais les IDs internes.

## KPIs prioritaires V1

### Recherche ville

Objectif : mesurer la capacite de la marketplace a orienter un visiteur vers une ville exploitable.

Indicateurs :
- nombre de selections de ville ;
- taux de selection apres arrivee sur la home ;
- villes les plus selectionnees via `ville_label` ;
- sorties sans selection de ville.

Evenements principaux :
- `view_home`
- `search_city_started`
- `search_city_selected`

### Conversion achat

Objectif : mesurer le passage de la consultation d'un coffret a l'achat particulier confirme.

Indicateurs :
- taux de demarrage achat depuis une page coffret ;
- taux de redirection checkout ;
- taux de confirmation achat ;
- taux d'echec ou abandon post-redirection.

Evenements principaux :
- `view_coffret`
- `coffret_purchase_started`
- `checkout_redirected`
- `purchase_confirmed`
- `purchase_failed`

### Commande pro

Objectif : mesurer l'interet et la conversion du parcours professionnel.

Indicateurs :
- taux de demarrage commande pro depuis un coffret ;
- taux de confirmation commande pro ;
- repartition des commandes pro par type de coffret ;
- echecs ou abandons identifies dans le tunnel pro.

Evenements principaux :
- `coffret_pro_order_started`
- `checkout_redirected`
- `pro_order_confirmed`
- `purchase_failed`

### Activation

Objectif : mesurer l'usage post-achat et la transformation des coffrets achetes en coffrets actives.

Indicateurs :
- nombre d'activations demarrees ;
- nombre d'activations confirmees ;
- taux d'activation par parcours ;
- delai approximatif entre achat et activation si disponible sans donnee personnelle.

Evenements principaux :
- `coffret_activation_started`
- `coffret_activation_confirmed`
- `coffret_instance_viewed`

## Architecture technique recommandee

Ajouter un service frontend dedie, par exemple `src/services/analytics.js`.

Responsabilites :

- lire la configuration runtime ;
- charger `gtag.js` uniquement si autorise ;
- initialiser GA4 ;
- appliquer l'etat de consentement ;
- exposer des fonctions de tracking stables ;
- normaliser les routes avant envoi ;
- ignorer les evenements si Analytics est inactif ;
- logger en debug uniquement si autorise.

Ajouter un hook de suivi de route, par exemple `AnalyticsRouteTracker`, branche dans `App.jsx` ou autour des `Routes`.

Contraintes :

- aucune dependance directe a GA dans les pages metier ;
- les pages appellent des helpers metier comme `trackCoffretViewed` ou `trackCheckoutStarted` ;
- un test unitaire ou une verification manuelle doit couvrir le mode desactive ;
- l'implementation doit etre compatible avec le fallback SPA du serveur Node.

## User Stories detaillees

### `PRD-093` Configuration Analytics par environnement

En tant qu'operateur Localeo, je veux configurer Google Analytics differemment entre local, test et production afin de separer les donnees et controler l'activation.

Resultats attendus :
- les variables Analytics sont exposees dans `app-config.js` ;
- l'environnement de production utilise la propriete GA4 production ;
- l'environnement de test utilise une propriete GA4 test separee ;
- l'environnement de test public reste desactive par defaut pour ne pas collecter de donnees ;
- l'absence d'identifiant GA ne provoque aucune erreur ;
- `.env.example` documente les variables.

### `PRD-094` Chargement conditionnel de GA4

En tant que systeme, je veux charger GA4 uniquement lorsque la configuration et le consentement le permettent afin de respecter la confidentialite utilisateur.

Resultats attendus :
- `gtag.js` n'est pas charge sans identifiant de mesure ;
- aucun evenement n'est envoye si Analytics est desactive ;
- aucun script GA4 ni signal limite n'est envoye avant acceptation du consentement ;
- le chargement tardif apres consentement est supporte ;
- l'application reste fonctionnelle si le script externe echoue.

### `PRD-095` Consentement Analytics marketplace

En tant que visiteur marketplace, je veux pouvoir accepter ou refuser le suivi Analytics afin de garder le controle sur les donnees de navigation collectees.

Resultats attendus :
- une interface de consentement est affichee avant tout tracking Analytics ;
- le refus est aussi simple que l'acceptation ;
- le choix est conserve localement ;
- l'utilisateur peut modifier son choix ulterieurement ;
- aucun script GA4 ni evenement Analytics n'est declenche avant acceptation.

### `PRD-096` Suivi des pages SPA

En tant que responsable produit, je veux suivre les vues de page dans la SPA afin de comprendre les parcours reels entre les ecrans.

Resultats attendus :
- chaque changement de route envoie une pageview si le tracking est actif ;
- les query params sensibles sont retires ;
- les query params trackes utilisent des libelles publics plutot que des IDs internes ;
- les routes 404 peuvent etre identifiees ;
- les titres ou categories de page sont coherents.

### `PRD-097` Suivi du parcours de decouverte

En tant que responsable produit, je veux mesurer la recherche de ville et la consultation des coffrets afin d'identifier les zones et offres les plus attractives.

Resultats attendus :
- la selection d'une ville est trackee ;
- les consultations de page ville et liste coffrets sont trackees ;
- les clics vers detail coffret et commercant sont trackes ;
- les evenements utilisent les libelles publics de ville, coffret et commercant ;
- les evenements ne contiennent pas de valeur libre saisie par l'utilisateur.

### `PRD-098` Suivi du tunnel de conversion

En tant que responsable business, je veux mesurer le tunnel d'achat afin d'identifier les abandons et erreurs de conversion.

Resultats attendus :
- le demarrage d'achat est tracke ;
- la redirection checkout est trackee ;
- le retour de paiement est tracke ;
- les confirmations et echecs sont distingues ;
- aucun identifiant de paiement externe n'est envoye.

### `PRD-099` Suivi des parcours pro et post-achat

En tant qu'operateur Localeo, je veux suivre les usages apres achat afin de savoir si les coffrets sont actives, consultes et utilises.

Resultats attendus :
- la consultation d'une instance de coffret est trackee ;
- l'activation confirmee est trackee ;
- la consultation du QR print est trackee ;
- la soumission de feedback est trackee ;
- les tokens sont exclus des URLs et parametres envoyes.

### `PRD-100` Documentation du plan de marquage

En tant qu'equipe produit et technique, je veux une documentation stable des evenements Analytics afin de maintenir une lecture fiable dans le temps.

Resultats attendus :
- la liste des evenements V1 est documentee ;
- les parametres autorises et interdits sont explicites ;
- les conventions de nommage sont stables ;
- toute nouvelle page ou fonctionnalite ajoute son suivi au plan de marquage.

## Criteres d'acceptation globaux

- GA4 est configurable par environnement.
- L'environnement de test public n'envoie pas de donnees Analytics en V1.
- Analytics est inactif par defaut si aucun identifiant de mesure n'est fourni.
- Une interface de consentement Analytics est disponible sur la marketplace.
- Aucun evenement n'est envoye avant le consentement requis.
- Le tracking n'expose aucune donnee personnelle ni token.
- Le tracking n'expose pas d'identifiant technique interne et privilegie les libelles publics.
- Les KPIs recherche ville, conversion achat, commande pro et activation sont mesurables en V1.
- Les pageviews SPA sont envoyees sur les changements de route.
- Les evenements prioritaires du parcours decouverte, conversion et post-achat sont couverts.
- L'application fonctionne normalement si Google Analytics est bloque ou indisponible.
- Le plan de marquage V1 est documente et relisible par le produit.

## Hors perimetre V1

- Google Tag Manager, sauf decision explicite ulterieure.
- Google Consent Mode.
- Server-side tracking.
- Attribution marketing avancee multi-canal.
- A/B testing.
- Heatmaps ou enregistrement de session.
- Export BigQuery.
- Tableaux de bord Looker Studio.
- Suivi backoffice admin.
- Envoi de donnees metier nominatives ou transactionnelles fines.

## Questions ouvertes

- Aucune question ouverte a ce stade pour la V1.

## MARKET-001 ? Jetons dans Analytics (2026-09-06)

Collecte suspendue dans le code et script tiers retire de la CSP. La reactivation exige une recette reseau et une revue du transport ; le flag seul est sans effet. Voir [contrat et exploitation](../../specifications/securisation-production/corrections-marketplace-2026-09-06.md).

## MARKET-005 - Retrait Analytics

Retrait et remise a zero synchronises entre onglets, signal fournisseur et suppression des cookies GA accessibles. Maintenir la suspension MARKET-001.
