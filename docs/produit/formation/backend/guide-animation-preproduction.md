# Formation et recette Animation — corrections ANIM

Référence : audit préproduction du 6 septembre 2026 dans le dépôt
`localeo-animation/docs/audits/`. Ce guide décrit les comportements attendus après
correction. Il ne constate pas un déploiement et ne rouvre pas les epics terminées.

## Finance — ANIM-001, ANIM-002, ANIM-006, ANIM-013

- Choisir explicitement la commune active avant de consulter commandes et factures.
  Un même partenaire peut avoir plusieurs communes : leurs documents sont séparés.
- Une facture historique sans commune identifiable est réservée au support.
  Vérifier son abonnement source avant toute régularisation; ne pas lui affecter
  automatiquement la commune actuellement ouverte par le gestionnaire.
- Après une erreur réseau, reprendre la commande existante. Le retour navigateur
  de Stripe n'est pas une preuve de paiement. Attendre la confirmation serveur.
- Une commande couverte entièrement par crédit ne redirige pas vers Stripe.
  Le serveur vérifie et capture la réservation avant de confirmer le paiement.
- L'état A_RECONCILIER nécessite le traitement support documenté pour les lots;
  ne pas forcer PAYEE et ne pas relancer un achat pour masquer l'incident.
- Une erreur de chargement des documents est affichée; elle ne signifie pas que
  la commande n'a aucun document.

## Qualification, calendrier et clôture — ANIM-003 à ANIM-005

Un commerçant donne au plus une validation effective à un participant. Un seuil
manuel de quatre sur dix commerçants est atteint après quatre validations distinctes.
Le serveur refuse la publication si les acceptations ne permettent pas d'atteindre
ce seuil. Les règles historiques canoniques restent prioritaires sur un ancien
champ de formulaire; les tirages existants ne sont pas recalculés automatiquement.

Les jours saisis représentent Europe/Paris, indépendamment du fuseau du poste.
Le dernier jour choisi est inclus; la fermeture temporelle prend effet au minuit
suivant. Les journées de changement d'heure peuvent durer 23 ou 25 heures.
Les inscriptions ne sont plus acceptées à la fin et un scan à l'instant exact de
fin est refusé. La clôture fige la population éligible. Un scan, une annulation ou
une édition qui attend la clôture ne peut pas modifier ensuite cette population.

## Création, commune et live — ANIM-008 à ANIM-010

Après timeout de création, réessayer sans modifier le formulaire renvoie le même
brouillon. Modifier le formulaire constitue une nouvelle intention.
Pendant un changement de commune, attendre la relecture du contexte serveur.
Même si la confirmation réseau est perdue, le contexte est relu : ne pas supposer
que l'ancienne commune est restée active. Les réponses tardives sont rejetées.
Le live s'actualise toutes les 15 secondes lorsque l'onglet est visible; en cas
d'erreur, les dernières données restent affichées avec un avertissement.

Les listes parcourent la pagination serveur. Les exports contiennent des données
réelles. Les cellules potentiellement interprétables comme formules portent le
préfixe visible `Texte: `, notamment les téléphones commençant par +. La donnée
source n'est pas modifiée et les nombres négatifs restent numériques.

## Session et opérations — ANIM-012 à ANIM-014

La session reste uniquement en mémoire et expire même sans appel API.
À la déconnexion, les données locales sont effacées immédiatement. Un message
précise si la révocation serveur n'a pas pu être confirmée.
Une opération PENDING/RUNNING n'est pas un succès; attendre SUCCEEDED. Si elle
reste en cours, consulter son état avant de relancer l'action.

## Recette requise sur la cible

Avec deux communes du même partenaire et deux profils (lecture/gestion), vérifier
les refus intercommunaux pour listes, fichiers et mutations, puis le parcours
création → invitations → achat/crédit → publication → scan → clôture → tirage → gains.
Vérifier les quotas, les rôles révoqués, le mode Stripe, la livraison email/outbox,
les documents et la restauration de sauvegarde. Ces contrôles nécessitent des
comptes de recette et la configuration réelle de la plateforme.

## Tests automatisés isolés

La CI `animation-audit.yml` utilise un PostgreSQL 18 jetable sur le port 55439 et
installe les dépendances verrouillées avec vérification des hashes. Le lanceur
`scripts/validation/run_animation_audit_tests.py` ignore les fichiers dotenv, désactive les
jobs et providers réels et bloque les connexions hors de cette base locale.
Les tests PostgreSQL sont explicitement ignorés sans leur variable de connexion;
ils sont exécutés par le job dédié, jamais réputés validés par un skip.
