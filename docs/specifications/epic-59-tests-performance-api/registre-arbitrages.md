# Registre des arbitrages - Epic 59 Tests de performance des API

## Decisions validees

| ID | Sujet | Proposition | Etat |
| --- | --- | --- | --- |
| `PERF-ARB-01` | Outil de charge | Executer le binaire k6 directement sur le poste Windows, sans Docker, transmettre les resultats a Grafana Cloud k6 Free et conserver `pytest` pour les tests fonctionnels. | Valide |
| `PERF-ARB-02` | Perimetre des parcours | Retenir les huit parcours `PERF-JRN-01` a `PERF-JRN-08`, dont six P0 interactifs et deux P1 d'exploitation. | Valide |
| `PERF-ARB-03` | Separation parcours/profil | Rendre chaque parcours reutilisable avec les profils smoke, nominal, pointe, stress, pic et endurance. | Valide |
| `PERF-ARB-04` | Cibles de test | Autoriser un benchmark de production manuel, borne et sans effet de bord ; creer un environnement ephemere a la demande pour les ecritures et les campagnes lourdes. | Valide |
| `PERF-ARB-05` | Autorisation explicite | Exiger une allowlist d'hotes, un indicateur d'autorisation, le type de cible et des plafonds avant tout tir. | Valide |
| `PERF-ARB-06` | Source de la charge nominale | En l'absence de mesures, etablir une baseline technique par paliers depuis une charge minimale, puis remplacer cette hypothese par les mesures reelles lorsqu'elles seront disponibles. | Valide |
| `PERF-ARB-07` | Repartition mixte | Demarrer avec 55 % Marketplace, 25 % Live, 10 % Commercant, 5 % Animation, 3 % BackOffice et 2 % Achat, puis recalibrer sur les mesures. | Valide |
| `PERF-ARB-08` | Seuils | Utiliser les seuils initiaux comme hypotheses et les ratifier apres une baseline representative. | Valide |
| `PERF-ARB-09` | Jeux de donnees | Faire gerer par la campagne la sauvegarde de la base ephemere, l'import des profils `small`, `reference` ou `capacity`, la surcouche `runId` et la restauration garantie de l'etat initial. | Valide |
| `PERF-ARB-10` | Fournisseurs externes | Utiliser Stripe Test, `EMAIL_DEV_MODE=true`, `SMS_DEV_MODE=true`, un adaptateur WebPush simule et un stockage dedie sur la cible ephemere ; interdire ces effets de bord pendant un benchmark de production. | Valide |
| `PERF-ARB-11` | Ecritures concurrentes | Fournir une ressource unique par iteration, sauf scenario explicitement consacre a l'idempotence. | Valide |
| `PERF-ARB-12` | BackOffice | Mesurer separement pages HTML SQLAdmin et API internes, avec session, cookie et CSRF reels sur la cible autorisee. | Valide |
| `PERF-ARB-13` | Exploitation sous charge | Executer Localeo Control et les endpoints de diagnostic pendant une pointe publique. | Valide |
| `PERF-ARB-14` | Declenchement | Ne lancer aucune campagne automatiquement ; chaque execution est manuelle et autorisee par un administrateur. | Valide |
| `PERF-ARB-15` | Conservation des resultats | Conserver pendant une semaine dans Grafana Cloud k6 le resume, les metriques et les informations expurgees de commit, environnement et dataset. | Valide |
| `PERF-ARB-16` | Environnement representatif | Creer a la demande une cible avec PostgreSQL `0,5 CPU / 1 Go RAM` et backend Render `0,5 CPU / 512 Mo RAM` ; documenter tout ecart avec la production. | Valide |

## Reponses actees

- aucune mesure de trafic n'est disponible au demarrage : la charge de
  reference sera calibree par paliers ;
- l'environnement hors production est cree a la demande ;
- PostgreSQL dispose de `0,5 CPU` et `1 Go RAM` ;
- le serveur backend Render dispose de `0,5 CPU` et `512 Mo RAM` ;
- les resultats sont consultes dans Grafana Cloud k6 et conserves une semaine ;
- les fournisseurs sont configures selon `PERF-ARB-10` ;
- les exports sont testes au volume maximal autorise ;
- seul un administrateur autorise, surveille et arrete une campagne.

## Decisions deja imposees par le cadre de securite

- aucun secret de test n'est versionne ou imprime ;
- aucune campagne non supervisee ne vise la production ;
- les donnees de production ne sont pas recopiees sans anonymisation et
  autorisation explicites ;
- le nettoyage ne cible que des ressources dont l'appartenance au `runId` est
  verifiee ;
- un test ne produit aucun paiement ou message externe reel.
