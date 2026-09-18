# Epic 48 — Registre des arbitrages APScheduler

## Utilisation

La colonne **Validation ou amendement** doit être complétée avant le lot qui
dépend de la décision. Une proposition non validée ne constitue pas une règle
de production.

## État d'intégration au 22 août 2026

- `APS-ARB-01` à `APS-ARB-13` sont validés, car cochés par le responsable
  produit.
- `APS-ARB-01` acte l'hébergement dans le service FastAPI actuellement déployé
  sur Render, avec `BackgroundScheduler` et un leader garanti par lease
  PostgreSQL.
- L'amendement de `APS-ARB-04` remplace le registre Python comme source unique
  des fréquences : chaque cron possède un défaut applicatif surchargeable par
  variable d'environnement.
- L'amendement de `APS-ARB-05` remplace l'appel direct : APScheduler appelle les
  endpoints HTTP protégés avec une clé API `internal:batch`.
- Aucun arbitrage produit ou technique ne reste ouvert dans ce registre.

| ID | Arbitrage | Détail et impact | Priorité | Proposition de réponse | Validation ou amendement |
|---|---|---|---|---|---|
| APS-ARB-01 | Topologie de déploiement | Démarrer APScheduler dans FastAPI permet de réutiliser le service Render actuel, mais chaque worker web peut alors enregistrer et déclencher les mêmes jobs. | P0 | Intégrer `BackgroundScheduler` au lifespan FastAPI et réserver l'exécution à un leader élu par lease PostgreSQL. | [X] Validé avec amendement<br>Amendement : l'ordonnanceur doit fonctionner dans le service FastAPI actuellement déployé sur Render.<br>Date : 22/08/2026 |
| APS-ARB-02 | Version APScheduler | La branche 4 reste en préversion alors que la branche 3.11 est stable et compatible Python 3.14. Le choix affecte toute l'API d'intégration. | P0 | Utiliser `APScheduler>=3.11.3,<4.0` et prévoir une epic séparée pour une future migration majeure. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-03 | Persistance APScheduler | Un job store SQL persiste les échéances, mais sérialise les jobs et crée une seconde source de vérité. Le job store mémoire exige une stratégie de reprise après arrêt. | P0 | Recréer les jobs versionnés au démarrage avec le job store mémoire ; conserver `executions_batch` comme preuve et appliquer une reprise Localeo explicite. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-04 | Source des fréquences | Les horaires peuvent être définis dans le code, en variables d'environnement ou modifiables en base depuis le back-office. | P0 | Définir un cron par défaut dans le registre et permettre sa surcharge par une variable d'environnement dédiée ; réserver l'édition depuis le back-office à une évolution. | [X] Validé avec amendement<br>Amendement : les fréquences doivent être configurables par variables d'environnement.<br>Date : 22/08/2026 |
| APS-ARB-05 | Mode d'appel des batchs | Le scheduler peut appeler les endpoints HTTP ou invoquer directement les use cases. L'HTTP ajoute authentification et latence ; l'appel direct exige un dispatcher partagé. | P0 | Appeler les endpoints HTTP protégés depuis APScheduler avec une clé API `internal:batch`, une URL de base configurable et une corrélation propagée. | [X] Validé avec amendement<br>Amendement : on appelle les endpoints HTTP.<br>Date : 22/08/2026 |
| APS-ARB-06 | Politique des échéances manquées | Rejouer toutes les échéances après un arrêt peut provoquer une rafale ; ne rien rejouer peut laisser des expirations ou rapprochements en retard. | P0 | Coalescer les échéances ; reprendre au prochain tick les batchs fréquents et lancer au plus une reprise de démarrage pour les traitements quotidiens critiques. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-07 | Retry technique | APScheduler peut relancer rapidement un job, tandis que les outbox et batchs possèdent déjà leurs règles d'éligibilité et de reprise. | P0 | Ne pas ajouter de retry aveugle dans APScheduler ; historiser l'échec et laisser le prochain tick ou une reprise bornée le traiter. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-08 | Fuseau horaire | Les horaires métier sont exploités en France, mais les infrastructures et cron Render utilisent UTC. Les changements heure été/hiver peuvent produire des ambiguïtés. | P0 | Planifier tous les jobs en UTC et documenter l'heure locale correspondante dans le back-office. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-09 | Haute disponibilité | Plusieurs workers FastAPI peuvent coexister lors du scaling ou d'un déploiement Render. APScheduler 3.x ne doit pas partager son job store entre eux. | P0 | Démarrer un coordinateur par worker, mais un seul `BackgroundScheduler` leader grâce au lease PostgreSQL ; permettre la reprise après expiration du lease, sans actif/actif. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-10 | Pause depuis le back-office | Une pause dynamique est pratique en incident, mais doit être persistante et cohérente avec une configuration versionnée. | P1 | Au MVP, autoriser l'arrêt global par configuration et conserver les lancements manuels ; reporter la pause persistante par job. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-11 | Supervision persistante | Les workers FastAPI ne partagent pas leur mémoire et l'API doit identifier le leader et ses prochaines échéances. | P0 | Ajouter un lease et des projections SQL de heartbeat et de planification, sans en faire un job store ni une source de code exécutable. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-12 | Stratégie de bascule | Activer APScheduler avant de supprimer les cron externes crée des doublons ; faire l'inverse sans contrôle crée une interruption. | P0 | Déployer FastAPI scheduler désactivé, vérifier le lease, arrêter les déclencheurs externes batch par batch, puis activer APScheduler et contrôler le health. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
| APS-ARB-13 | Disponibilité du service Render | Un scheduler embarqué ne fonctionne que tant que le service web est actif. Les instances gratuites Render peuvent s'endormir en l'absence de trafic. | P0 | Exiger pour la production une instance Render toujours active, avec au moins une instance web en permanence ; refuser de considérer l'ordonnancement comme opérationnel sur une instance susceptible de s'endormir. | [X] Validé<br>Amendement :<br>Date : 22/08/2026 |
