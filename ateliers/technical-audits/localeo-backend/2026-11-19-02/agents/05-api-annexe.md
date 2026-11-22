# Annexe — périmètre API et observations secondaires

Lecture indépendante du code courant le 19 novembre 2026. Modèle exact : **INCONNU** ; effort de raisonnement : **INCONNU**. Aucun ancien audit/rapport lu et aucune exécution applicative, réseau, base, serveur, test ou benchmark. Les chemins sont relatifs au dépôt indiqué ; les numéros de lignes désignent les sources lues et peuvent évoluer avec les travaux parallèles.

## Parcours effectivement examinés

| Parcours | Producteur courant | Consommateur constaté / qualification |
| --- | --- | --- |
| Lecture personnelle et commandes Live | `localeo-backend/app/api/jeu_animation_api.py:75–113`, `services/jeu_animation.py:399–463` | `localeo-marketplace/src/live/LiveAnimationGame.jsx:178`, 258–299 : commandes, reçus, puis actualisation. API-01/02 concernent ce chemin. |
| Dashboard Live | `services/tableau_de_bord_live.py:117–155` | `localeo-marketplace/src/live/useLiveDashboard.js:34–64` : demande d'une page de 50, rejet des surtailles et curseurs répétés. Pas de collecte automatique de tout le carnet. |
| Consultation publique et visuels | `app/api/animation_locale_api.py:3961–4010`, `services/visuel_animation_publique.py:18–49` | `localeo-marketplace/src/components/useAnimationFlyerImage.js:5–10` utilise le `visuel_url` explicite de l'API. Celui-ci vise l'illustration de flyer (`services/catalogue_animations_publiques.py:698`) ; ne pas confondre avec l'ancien `/visuel`. |
| QR personnel | `services/participants_animation.py:240–247`, `qr_png` | Génération PNG après résolution et contrôle courant. Le `no-store` de la route est cohérent avec la capacité personnelle ; pas de proposition de cache public. |
| Dépôt et suivi d'import commerces | `app/api/imports_commercants_api.py:257–268`, `services/imports_commercants.py:107–155` | `localeo-animation/src/app/merchantImportsApi.ts:23–47` : pages de 25, commandes avec reçus ; dépôt borné et travail synchrone déporté dans `run_in_threadpool`. L'`async def` n'exécute donc pas directement parsing/SQL sur la boucle événementielle. |
| Gains coffrets et résultats | `app/api/animation_locale_api.py:2721–2810` | `localeo-animation/src/app/App.tsx:2939–2959` : API-03. `src/app/resultsApi.ts:18–22` utilise des pages de bilan et des synthèses séparées. |
| Fin/clôture moteur | `services/fin_animation.py:consulter`, `commander` | Projection de dossiers paginée, décisions et version attendue. Lecture insuffisante pour conclure à une régression de latence ; ne pas transposer la route historique de gains aux dossiers moteur. |

## Observations secondaires, non promues en constats majeurs

1. **Deux autorisations sur la lecture moteur.** `app/api/jeu_animation_api.py:84–87` appelle `service.autoriser`, puis `service.lire` ; `_snapshot` rappelle `_autoriser` (`services/jeu_animation.py:324–325`, 363–369). Cela introduit une lecture supplémentaire, mais la première précède le garde de limitation par participation et constitue une protection ; toute fusion doit préserver cet ordre. Aucun gain chiffré ni suppression recommandée sans analyse de sécurité.

2. **ETag du visuel historique sans branche 304 dans la route.** `app/api/animation_locale_api.py:3998–4009` renvoie un ETag et un cache public court mais n'inspecte pas `If-None-Match` ; le service lit les octets avant la réponse. Cependant le consommateur public constaté affiche le `visuel_url` de l'illustration-flyer, expressément `no-store` pour permettre les retraits (3961–3981). Optimiser le seul `/visuel` ne prouve donc pas une amélioration du catalogue actuel. Toute mise en cache du flyer devrait préserver sa règle de retrait et n'est pas une retouche technique automatique.

3. **Payload Live borné mais répété.** `services/projections_jeu.py:9`, 178–200 impose un budget de 256 000 octets et évalue au plus trois images pour la chasse. `contenu_generation.py:300–316` borne un média à 44 000 octets binaires / 60 000 octets JSON. Le base64 est intégré à chaque projection plutôt qu'une URL privée indépendante ; cela ajoute du transfert, mais n'établit ni payload non borné ni fuite de toute la définition. Une séparation des ressources serait un changement de contrat et de gestion des autorisations, au-delà du correctif local API-01.

4. **Transport fournisseur distinct des commandes courantes.** `services/participants_animation.py:324` et `services/verification_email.py:_emettre` ajoutent des emails à l'outbox ; `services/notification_gain_sms.py:1–37` crée une intention SMS sans transport. `services/distribution_coffrets.py:30` distingue distribution synchrone des droits et notifications. Le timeout de 20 secondes du transport Brevo (`app/infrastructure/sms/service_envoi_sms.py:59–64`) ne suffit donc pas à conclure que l'inscription ou le clic d'envoi de gain attend directement Brevo.

5. **Budgets SQL existants, pas délai HTTP global.** `app/infrastructure/animation_locale/composition.py:12–19` fixe `lock_timeout=3s` et `statement_timeout=15s` par transaction du moteur ; une autre composition d'exploitation autorise 60 secondes. Un timeout SQL par instruction ne borne pas la somme SQL + médias + sérialisation. La présence de ces protections interdit néanmoins d'affirmer l'absence générale de budgets.

## Contrôles et limites

Les commandes utilisées sont des lectures de fichiers et recherches `rg`/`Get-Content`, puis l'écriture des deux rapports attribués. Certains chemins supposés au début de l'exploration étaient absents ; les preuves retenues renvoient aux chemins réellement trouvés. Aucun code n'a été importé et aucune configuration privée n'a été ouverte.

Les méthodes historiques de collecte globale encore définies dans `localeo-animation/src/app/api.ts:1314–1322` ne sont pas considérées comme des parcours actifs sans appelant retrouvé. Les nouveaux workspaces, le dashboard préchargé et les imports bornés ne sont pas assimilés à ces méthodes. La recherche de consommateurs est ciblée, pas une preuve d'absence exhaustive d'appels externes.

Contrôles documentaires non exécutés : le brief interdit les tests et l'exécution se limite ici à la lecture/production des rapports. Ni contrat exporté ni guide applicatif n'a été modifié. Le seul dépôt écrit est `localeo-projet`, exclusivement `agents/05-api.md` et `agents/05-api-annexe.md` ; les autres modifications concurrentes restent hors périmètre. Aucun processus d'exécution partagé n'a été lancé.
