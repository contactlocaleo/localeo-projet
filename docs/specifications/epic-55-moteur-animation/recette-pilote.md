# Moteur d’animation — recette et préparation du pilote

Ce document donne les critères de recette de l’EPIC et le relevé à compléter pour un pilote. Les règles restent celles de la [spécification](localeo_animation_engine_spec.md) et de la [conception technique](conception-technique.md). Le [compte rendu d’implémentation](suivi-implementation.md) porte les résultats des commandes, les limites et les commits.

## 1. Ce que prouvent les différents contrôles

| Contrôle | Preuve attendue | Limite |
| --- | --- | --- |
| Domaine et contrats | Trois moteurs, cinq activités, états, réponses fermées, seuils et dépendances. | N’établit pas le fonctionnement d’un appareil ni d’un environnement déployé. |
| PostgreSQL réel jetable | Transactions, concurrence, reçus, activation QR, attestations, retrait, correction, gel et conservation. | Les référentiels externes et les fournisseurs sont isolés ; aucun paiement ou envoi réel. |
| Recette transversale | Résultat préparé → accords → publication → inscription → jeu → attestation → retrait → régularisation → gel → tirage → conservation. | Part d’un résultat éditorial accepté ; génération et acquisition du lot sont couvertes séparément. |
| Navigateur à API simulée | Écrans à 390/1280 px, clavier, cinq activités, droits, perte de réponse, réconciliation et continuité. | Ne remplace pas les preuves HTTP/PostgreSQL ni un scan caméra réel. |
| Pilote humain | Parcours, durée, repérage des lieux, caméra, réseau, accessibilité et compréhension sur place. | **Non exécuté dans l’implémentation.** À renseigner sur la cible retenue. |

La recette transversale exécutable est [test_parcours_moteur_epic_postgres.py](../../../../localeo-backend/tests/security/test_parcours_moteur_epic_postgres.py). Les suites dédiées couvrent les variantes, erreurs, courses et frontières que ce parcours nominal ne peut toutes regrouper.

## 2. Critères techniques avant ouverture

- [ ] Les migrations additives sont appliquées par le lanceur officiel à la cible explicitement choisie ; leurs contrôles passent.
- [ ] La simulation de conversion est examinée ; aucun objet publié incompatible n’est présent. Les démonstrations sont identifiées explicitement. L’application de la simulation puis son rejeu ne déclenchent ni génération, ni publication, ni invitation, ni débit de quota.
- [ ] Les trois frontends embarquent les mêmes contrats générés que le backend ; leurs contrôles de contrats et builds passent.
- [ ] Le résultat de génération passe le parseur strict, les contrôles des médias WebP et les budgets de projection. Les secrets, bonnes réponses, lieux futurs et missions non choisies restent privés.
- [ ] Les mutations portent les versions et une clé stable. Après une réponse perdue, la lecture du reçu précède tout renvoi explicite ; le rejeu exact ne double aucun effet.
- [ ] Les permissions de publication, neutralisation, correction et clôture sont explicitement attribuées aux acteurs habilités. Les refus de scope et CSRF sont vérifiés.
- [ ] Les simulations de conservation sont terminées pour les catégories à traiter. Les tâches de purge, le curseur, les reprises et l’ordonnanceur sont vérifiés sur la cible retenue.
- [ ] La purge des réponses détaillées après échéance conserve les compteurs, reçus utiles, preuves, provenance du gel, population et gains.
- [ ] Les opérations en attente humaine restent distinctes des échecs techniques. Les opérateurs disposent du suivi, des identifiants de corrélation et des procédures de reprise.

Ces cases ne déclarent pas un déploiement effectué. Les succès locaux sont recensés dans le compte rendu ; chaque case d’ouverture doit être confirmée sur la cible retenue.

## 3. Fiche de préparation du pilote — à renseigner

| Élément | Valeur à consigner |
| --- | --- |
| Cible et version | Environnement, versions/commits backend et trois interfaces, opérateur. |
| Territoire | Commune et périmètre ; Latresne reste l’exemple documentaire, pas un pilote confirmé. |
| Période | Date/heure de début et fin, fuseau, échéance des réponses commerçantes. |
| Participants | Public, nombre prévu, capacité éventuelle ; référent organisateur et contact support. |
| Parcours | Thème, difficulté, durée cible, fourchette d’étapes, liste vérifiée des commerces/POI. |
| Conditions de participation | Règlement présenté et sa version, déclaration adulte, absence d’achat obligatoire. |
| Commerçants | Deux propositions lorsqu’elles existent, mission sélectionnée, exigences confirmées, disponibilité et support. |
| Préparation des lieux | QR commerce automatique à l’acceptation, remis dans le kit ; seul le QR des POI est préparé par le gestionnaire. Le bloc Supports des lieux publics disparaît sans POI (E55-UX-12). Aucune fiche de visite ni checklist imposée. Les horaires, trajet, accès et consignes restent dans le guide facultatif. |
| Continuité | Source et consommateurs des objets/informations ; réponse prévue en cas de retrait global d’une étape. |
| Visuels | Thème déclaré, polices autorisées, médias de l’animation ; poids/résolution/texte alternatif. Aucun ajout décoratif spécifique dans le lecteur. |
| Appareils | Au moins un Android et un iPhone réels, navigateurs/versions, ordinateur et parcours clavier. |
| Exploitation | Acteurs habilités, traitement d’un commerce fermé, correction d’attestation, clôture et preuve de gel. |

## 4. Scénarios humains et résultats à consigner

| Scénario | Résultat attendu | Statut initial |
| --- | --- | --- |
| Inscription et reprise | Déclaration adulte/règlement explicites, lien personnel récupérable, capacité respectée. | Non exécuté sur cible réelle |
| Départ avant puis pendant la période | Défi masqué avant ouverture ; lieu courant uniquement ; départ activé au bon instant. | Non exécuté sur cible réelle |
| QR de lieu et QR personnel | Le QR de lieu ouvre le défi ; seul le scan commerçant habilité apporte l’attestation. | Caméra réelle non exécutée |
| Kit commerçant | `flyer-animation.pdf` est identique octet pour octet au PDF officiel courant, s’il est publié et diffusable dans `APPLICATION_COMMERCANT`. Aucun repli vers un ancien PDF si le document courant n’est pas diffusable. `support-mission.pdf` est présent seulement pour un support public autorisé. `qr-lieu.pdf` contient le QR opaque `LQL1` scannable dans Localeo Live. Le guide privé reste privé. | Impression et caméra réelles non exécutées |
| Kit avant publication et renouvellement | Sans flyer officiel, le ZIP reste téléchargeable avec une explication dans le guide et aucun aperçu privé. Après publication ou régénération du flyer officiel, un nouveau ZIP contient sa version courante ; l’ancien ZIP reste inchangé. | Non exécuté sur cible réelle |
| Accord historique et reprise | Télécharger prépare le support manquant avant lecture du ZIP, sans étape supplémentaire ni double écriture. Une erreur reste visible ; consulter le kit seul ne crée aucun QR. Je suis prêt reste indépendant. | Non exécuté sur cible réelle |
| Terrain mixte ou sans POI | Le gestionnaire voit uniquement les lieux publics dans le sélecteur. Sans POI, le bloc disparaît et le suivi des commerces reste visible ; une erreur de lecture n’est pas traitée comme une absence de POI. | Non exécuté sur cible réelle |
| Cinq activités | Information, choix unique, association, ordre, texte/code utilisables au toucher et au clavier. Erreur, indice, aide et succès compréhensibles. | Validation terrain non exécutée |
| Réseau interrompu | Commande bloquée/reçue clairement distinguée ; réconciliation et renvoi explicite sans double tentative. | Réseau mobile réel non exécuté |
| Commerce indisponible | Aperçu organisateur, motif et confirmation ; avis de parcours adapté, continuité disponible au bon moment. | Non exécuté sur cible réelle |
| Changement de période ou de capacité | Horaires Europe/Paris, champs autorisés et contrôles affectés relus ; versions vérifiées, réouverture explicitement confirmée si nécessaire, supports à rééditer. | Non exécuté sur cible réelle |
| Attestation erronée | Annulation autorisée, parcours conservé, qualification retirée ; nouvelle attestation reliée à la précédente. | Non exécuté sur cible réelle |
| Clôture et tirage | Population gelée depuis les faits ; replay sans second tirage ; anomalie ultérieure sans modification du gain. | Non exécuté sur cible réelle |
| Lisibilité et accessibilité | Contrastes, taille du texte, noms accessibles, focus visible, absence de débordement ; texte alternatif des images. | Recette humaine complète non exécutée |
| Parcours local | Durée mesurée, transitions compréhensibles, lieu suivant trouvable, accueil et missions réalisables. | Non exécuté sur le terrain |

Pour chaque exécution, relever date, acteur, appareil/version, animation/participation de test, résultat attendu/observé et référence d’incident. Ne pas joindre de token personnel, base64, bonne réponse ou donnée privée aux traces partagées.

## 5. Décision de passage

Le passage au pilote repose sur les contrôles techniques et la fiche logistique complétée. L’ouverture publique reste une opération distincte de l’implémentation et des commits. Un défaut empêchant une participation, révélant une réponse privée, doublant un effet ou altérant une preuve/qualification doit être corrigé puis revérifié avant ouverture. Les écarts de durée, compréhension ou présentation sont consignés avec leur décision et leur nouvelle vérification.

<a id="e55-audit-20261113"></a>
## 6. Complément de recette après audit du 13 novembre 2026

Les scénarios ci-dessous constituent le protocole après correction. Les
résultats réellement obtenus sont dans le
[bilan d'implémentation](suivi-implementation.md#e55-audit-20261113-implementation),
séparés de l'audit initial. Une preuve locale ne coche pas les conditions
d'ouverture sur cible de la [conception](conception-technique.md#e55-audit-20261113).

| Critères | Scénario discriminant et résultat attendu |
| --- | --- |
| A01 | IndexedDB refusé avant inscription puis écriture refusée après succès : inscription serveur unique et accès temporaire au jeu possibles, état du carnet exact. Réponse perdue/deux onglets/doublon/lien expiré : même intention ou récupération, aucune deuxième place. Non-régression des autres moteurs et du protocole E74. |
| A02 | Décision ERP traitée, réponse perdue, reçu confirmé, nouvelle estimation : deuxième décision envoyée et confirmée une seule fois. Reçu absent/étranger/refusé, session changée : aucune libération incorrecte ni renvoi automatique. |
| A03 | Modifier thème dans Animation et brief de révision ERP ; actualiser, changer de demande, paginer, quitter : conservation ou abandon explicite. Conflit/version et réponse tardive d'un autre contexte ne remplacent pas la saisie. |
| A04 | Même IP et UUID renouvelés, puis origines multiples et NAT partagé : cardinalité bornée, seuils atomiques, accès légitimes possibles, aucune fuite d'existence. Purge, saturation et retour à la normale vérifiés avec budgets préalables. |
| A05 | N = 1 000 puis 10N = 10 000 participations : mêmes pages, filtres, métriques et retrait ; nombre de requêtes/hydratations, mémoire, p95/p99, débit, pool et verrous relevés. Gel exact sous scans/corrections concurrents ; pas de mémoire proportionnelle à une liste complète ni gel partiel visible. |
| A06/A08/OPT-01 | Quota en erreur avec préparation disponible ; invitations en erreur puis succès/vide ; droits retirés : seules les actions dépendantes bloquent, pas de faux zéro ni erreur persistante. Acteur attendu, délai conditionnel et prochaine action compréhensibles. |
| A07/OPT-03 | Demande recherchée hors première page et hors périmètre ; q absent, invalide, ancien/nouveau curseur, filtre modifié et réponses inversées. Seuls les résultats autorisés sont accessibles ; première page d'invitations sans collecte complète, sélection/destinataires exacts. |
| A09 | À 320×844, 390×844 et 1280×900, état initial avec tirage indisponible puis lecture retardée : action principale visible, focusable et réellement touchable/cliquable. Hit-test ou clic réel prouve l'absence de recouvrement par la barre basse. |
| A10 | Ancienne chasse sans métadonnées, chasse enrichie, brief modifié non publié, étapes neutralisées et autre moteur : informations publiques exactes, valeurs absentes non inventées, référence publiée distincte de la progression personnelle, aucun lieu futur divulgué. |
| A11/A13/A14 | Association avec doublon expliquée sans tentative serveur ; déplacement au premier/dernier rang conservant focus et annonce ; réponses/statuts à texte 200 %, clavier/toucher et contraste. Ne pas confondre zoom global et agrandissement de texte. |
| A12 | Réaligner UoW/ports, fixtures contact public et attentes UI puis rejouer préparer → accords → publier → inscrire → cinq activités → attester → neutraliser/corriger → geler/tirer → conserver. Garder les refus, idempotence et confidentialité ; pas d'assertion supprimée pour obtenir du vert. |
| OPT-02/04/05/06 | Décision sur aperçu des accords ; mesures médias/bundle et première action à froid/chaud, temps ERP/allers-retours avant-après. Le résultat de l'étude, même sans optimisation de code retenue, doit être motivé et traçable. |

La capacité vise la Chasse et ses lectures effectives ; le banc E74 Tombola
ne la remplace pas. La conception fixe les budgets initiaux p95/p99/RSS et
la charge de référence ; renseigner avant campagne matériel, versions, volumes,
concurrence réelle, politique du limiteur et point de saturation selon E59 ;
enregistrer résultats et échecs, sans augmenter les seuils après observation
pour masquer une régression.

Cas supplémentaires requis par la spécification détaillée ; leur couverture
effective et les non-exécutions sont distinguées dans le bilan :

- **A01/A02 :** jeu temporaire réellement ouvert après échec d'écriture, refus
  serveur retirant l'accès ; confirmation de reçu suivie d'un GET métier en
  erreur, réponse 2xx mal formée, 408/429/conflit d'idempotence et validation
  locale avant envoi. Vérifier ensemble les deux états de commande ERP.
- **A04 :** transactions concurrentes sur huit processus, comptage global
  conservé lors d'un refus d'origine, aucun double décompte global après
  autorisation ; capacités pleines, réutilisation après expiration, purge
  concurrente et baisse de capacité refusée. Panne PostgreSQL/timeout → 503,
  origine inconnue unique, IPv6 /64, proxy fiable et NAT de 50 familles.
- **A05 — lecteurs :** page mixte Chasse exacte et mesures inconnues d'autres
  moteurs ; filtres Oui/Non avant limite, refus 503 avant exclusion des Chasses
  non reconstruites. Appels anciens avec synthèse, nouveaux sans synthèse ni
  COUNT ; masquage des coordonnées, commune unique et refus de curseur périmé.
  Aucune collecte complète dans Tirage ; Tombola publique et famille validations
  inchangées. Faire croître aussi le nombre d'animations, pas seulement leurs
  participants ; contrôler la disparition du LATERAL par animation.
- **A05 — transitions :** inscription, jeu, attestation, régularisation,
  correction, retrait, paramètres, gel, gain/remplacement et anonymisation.
  Comparer domaine/projection/compteurs après commit, y compris refus et rejeu.
  Reprendre une reconstruction interrompue pendant jeu/retrait, refuser une
  ancienne version, préserver la provenance gelée et ne recréer aucune identité.
  Arrêt pendant retrait/gel → rollback complet ; mesurer aussi notifications,
  en-tête de population et appelants batch, sans liste complète cachée.
- **A07/A10/OPT-03 :** accents et caractères `%`/`_`/`\`, projection de recherche
  manquante, plans GIN existants ; scalaires publics de la configuration publiée,
  types absents/invalides sans valeurs inventées. Page d'invitations isolée,
  sélection limitée, reçu d'envoi sans parcours exhaustif de l'historique.

Les parcours visuels utilisent une API simulée pour isoler les états, puis
une recette avec backend réel sur cible explicitement choisie vérifie leurs
contrats. Un pilote humain Android/iPhone, clavier et familles mesure durée,
compréhension, QR imprimés/caméra, réseau interrompu, commerce fermé et charge
d'accueil. La fiche de la section 3 reste obligatoire pour identifier cette
cible ; aucun ancien constat « non déployé » n'atteste l'état actuel.

- [ ] L1 : continuité vérifiée localement ; protection mesurée en isolation,
  qualification proxy/NAT et calibrage cible restant à produire.
- [ ] L2 : parcours vérifiés localement ; résultat des contrats au bilan,
  vérification du backend et des interfaces déployés restant à produire.
- [ ] L3 : études consignées, suites et mesures au bilan ; qualification de
  capacité complète restant à produire.
- [ ] L4 : critères T6 de cible, pilote, bilan et retests satisfaits.

[Retour au dossier moteur](README.md).
