# Limites et état des preuves

- Inspection directe statique du checkout backend ; aucune application importée ni lancée, aucun dotenv privé chargé, aucune base contactée.
- Les versions de requirements sont verrouillées ; versions installées, version PostgreSQL, commande réelle, workers, réplicas, CPU/RAM et limites proxy restent inconnus.
- Aucun profil CPU, mesure mémoire, charge, EXPLAIN ou chronométrage métier exécuté. Les mécanismes cartographiés ne constituent pas des anomalies démontrées ni une promesse de capacité.
- Le catalogue suit le graphe statique monté depuis main ; il ne remplace pas un relevé runtime isolé, notamment SQLAdmin, routes conditionnelles ou assemblées dynamiquement. Les chaînes F10–F12 nécessitent une exploration complémentaire lors des missions.
- Les fréquences d’appel frontend et la configuration du déploiement ne sont pas vérifiées. Les quatre consommateurs ne sont pas modifiés ni audités dans cette phase backend.
- Deux sous-agents d’exploration initiale ont été sollicités, puis ont signalé l’absence d’outils de lecture dans leur contexte. Ils n’ont lu ni écrit de source et n’ont produit aucun diagnostic. L’agent principal a repris leur inspection directement. L’accès aux outils devra être vérifié avant les six missions futures ; ne pas présenter un agent sans source lue comme un auditeur.
- `python` pointe initialement vers un alias Windows indisponible ; `py -3.14` fonctionne et sert aux contrôles documentaires. Aucun environnement applicatif n’a été installé ou modifié.
- Les dossiers de preuves ne contiennent pas de sorties réelles de benchmark : ces sorties restent dans le backend ou un stockage privé selon ses instructions ; les documents présents préparent seulement leur indexation.
- Pas de changement de règle, contrat, migration, génération de démonstration, configuration d’exploitation, commit, push ou déploiement. Les impacts de compatibilité devront être repris pour chaque recommandation future.

Prochain geste : autorisation utilisateur pour lancer les six missions en lecture, puis vérification de leur accès aux sources. Toute campagne exécutable ultérieure devra spécifier cible jetable, données synthétiques, volumes, commandes, limites et ressources isolées avant lancement. Production exclue.
