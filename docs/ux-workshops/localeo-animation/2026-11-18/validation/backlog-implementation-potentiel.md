# Backlog réalisé — recette UX à valider

Préparé le 2026-11-18T12:38:07+01:00 ; actualisé le 18 novembre 2026. **Onze orientations autorisées, implémentées et poussées ; recette UX à valider.** Le [registre](decisions.md) distingue autorisation, réalisation et recette. Le [bilan canonique WA](../../../../specifications/epic-73-animation-et-ou-coffrets/verification-livraison.md#workshop-ux-20261118) porte les preuves exécutées et leurs limites. Les neuf fiches P0/P1 ci-dessous conservent les critères initiaux ; F1/G1 P2 sont également réalisés et tracés dans le bilan.

## Validation fonctionnelle spécifique

**D2**, le 18 novembre : suivre l’atelier en cas de contradiction avec PO-13 ; ouvrir le suivi opérationnel, avec Bilan distinct. Voir le registre et E73-WA-13. La direction est validée, pas la recette.

## Orientations à réviser

Aucune décision reçue. Les réserves documentées ne sont pas transformées en choix « À RÉVISER » à la place de l’utilisateur.

## Orientations reportées

Aucune décision reçue. L’attente n’est pas un report.

## Orientations refusées

Aucune décision reçue. Les rejets du workshop simulé ne sont pas des refus utilisateur.

## Détail des neuf orientations P0/P1 réalisées

Périmètre : neuf P0/P1 de l’étape 3. F1 et G1 (P2 adoptées) restent dans le backlog historique, sans être assimilées à un report. Aucun sujet rejeté ou P3 ajouté. Ordre ci-dessous documentaire : aucune planification ni date engagée.

### D1 — Rétablir et fiabiliser Communication

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P0, effort M provisoire. [Fiche](orientations-a-decider.md#d1) · [Maquette v2](../visuels/maquettes-apres/D1.html).

**Objectif réalisé :** Préparer et suivre une communication fiable, avec une conduite claire en cas d’erreur.

**Dépendances :** Endpoint campagnes-organisateur et chaîne d’envoi ; P0 pour un lancement autonome incluant Communication, pas une panne globale démontrée.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. La cause est identifiée puis la lecture fonctionne sur le contexte ayant échoué et sur un jeu contrôlé pertinent.
2. Préparation, aperçu, résultat d’envoi et historique sont vérifiés avec des destinataires exclusivement isolés.
3. Un échec de lecture propose reprise ou support et conserve contexte ; un envoi dont le résultat est inconnu n’est pas rejoué automatiquement.
4. Un contrôle distingue réussite, refus et résultat incertain sans annoncer un envoi non confirmé.

### A1 — Donner la priorité aux actions attendues

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort M provisoire. [Fiche](orientations-a-decider.md#a1) · [Maquette v2](../visuels/maquettes-apres/A1.html).

**Objectif réalisé :** Identifier ce qui demande une intervention, puis accéder aux nouvelles.

**Dépendances :** Hiérarchie et sémantique des composants existants ; aucun nouveau calcul métier d’urgence.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. À contexte et droits identiques, les actions existantes à traiter et Créer sont accessibles avant les nouvelles sur bureau et mobile.
2. Succès, information et alerte ont un libellé et un repère distincts, sans dépendre seulement de la couleur.
3. Les nouvelles restent toutes accessibles ; la commune et les filtres ne sont pas perdus lors du retour.

### B1 — Sauvegarder avant la fin des sept étapes

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort L provisoire. [Fiche](orientations-a-decider.md#b1) · [Maquette v2](../visuels/maquettes-apres/B1.html).

**Objectif réalisé :** Préparer une animation en plusieurs sessions sans prétendre qu’elle est publiable.

**Dépendances :** Contrat de brouillon partiel à spécifier avec le backend ; droits, validation partielle et reprise. Pas une simple retouche de bouton.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. Après modèle, nom et commune, une commande explicite enregistre un brouillon incomplet et confirme seulement la sauvegarde réellement réussie.
2. Après fermeture et reconnexion, les champs enregistrés sont restitués et les éléments manquants sont listés.
3. Un échec de sauvegarde conserve la saisie et indique quoi faire ; aucune invitation ni publication n’est déclenchée.
4. Le domaine conserve les contrôles complets de publication ; un brouillon incomplet ne les contourne pas.

### B2 — Expliquer préparation, accords et publication

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort M provisoire. [Fiche](orientations-a-decider.md#b2) · [Maquette v2](../visuels/maquettes-apres/B2.html).

**Objectif réalisé :** Savoir qui doit agir, pourquoi et où, sans promettre le délai de réponse de tiers.

**Dépendances :** Réutiliser les diagnostics et statuts canoniques ; vérifier les liens et les acteurs disponibles dans le contrat.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. Avant de commencer, le parcours annonce le résultat brouillon, les prérequis d’accord et l’étape de publication.
2. Chaque blocage affiché comprend une action, un acteur connu, une raison et un lien ciblé ; aucun statut d’activation n’est inventé.
3. Les options de dotation existantes sont expliquées en langage courant, en conservant responsable et consignes.
4. L’aperçu précise quand le QR définitif devient disponible ; la distinction entre aperçu et support publié est conservée.
5. Aucun délai de 5–10 minutes n’est présenté comme acquis avant un test humain délimitant début et fin.

### B3 — Proposer un seuil de passeport cohérent

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort S provisoire. [Fiche](orientations-a-decider.md#b3) · [Maquette v2](../visuels/maquettes-apres/B3.html).

**Objectif réalisé :** Démarrer avec une règle compatible et compréhensible.

**Dépendances :** Bornes du domaine à respecter ; estimation S seulement si le contrat existant suffit. Capture 18 insuffisante pour voir le champ inférieur.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. Une nouvelle sélection de deux commerces propose un seuil compatible et explique ce qu’il signifie.
2. Une modification de sélection qui invalide un seuil déjà choisi provoque un message et un ajustement explicite, jamais une modification silencieuse.
3. Le serveur rejette toujours une configuration invalide, y compris hors interface.

### C1 — Rendre trouvable l’ajout d’un commerce absent

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort L provisoire. [Fiche](orientations-a-decider.md#c1) · [Maquette v2](../visuels/maquettes-apres/C1.html).

**Objectif réalisé :** Lui donner un chemin explicite et un suivi de demande sans créer de compte actif implicite.

**Dépendances :** Référentiel commerçants, droits de référencement et contrat backend ; périmètre à confirmer avant chiffrage ferme.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. Le sélecteur expose une action pour un commerce absent et décrit le résultat d’une demande de référencement.
2. Le parcours canonique existant est recherché et réutilisé ; son propriétaire et ses droits sont confirmés avant toute nouvelle fonction.
3. Le retour affiche un état réel et la prochaine action ; demande, éligibilité, activation et participation restent distinctes.
4. Aucune invitation ni activation automatique ne résulte de la simple demande.

### C2 — Sécuriser la compréhension de l’import

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort L provisoire. [Fiche](orientations-a-decider.md#c2) · [Maquette v2](../visuels/maquettes-apres/C2.html).

**Objectif réalisé :** Réduire le travail mécanique et permettre une décision informée avant import.

**Dépendances :** Qualité des adresses, faux positifs, contrats d’aperçu et import ; code déployé non identifié. L vaut pour l’ensemble, pas seulement les libellés.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. Les en-têtes reconnus du modèle sont préassociés, visibles, corrigeables et soumis à confirmation.
2. Colonne requise et valeur requise sont distinguées, avec exemples et erreurs de ligne compréhensibles.
3. Deux lignes de même nom/adresse sans email ni SIRET sont signalées comme similitude à examiner, sans fusion ni rejet automatique.
4. Le périmètre du rapprochement est indiqué ; les conflits email/SIRET et les contrôles serveur existants sont conservés.
5. La confirmation explicite montre les lignes et effets prévus avant création ; les essais utilisent un jeu isolé.

### D2 — Diriger le suivi vers le suivi opérationnel

**Direction fonctionnelle : VALIDÉE le 18 novembre. Réalisation : IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort S provisoire. [Fiche](orientations-a-decider.md#d2) · [Maquette v2](../visuels/maquettes-apres/D2.html).

**Objectif réalisé :** Accéder immédiatement à l’espace attendu.

**Dépendances :** Routes et états existants ; vérifier la navigation retour et les droits.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. Sur une animation en cours, Consulter le suivi ouvre l’espace opérationnel attendu.
2. Le bilan dispose d’un accès distinct et explicitement nommé.
3. Les définitions inscription, progression, qualification, validation, ainsi que dates et périmètres, restent visibles et exactes.

### E1 — Rendre explicite le chemin de fin

**Réalisation : AUTORISÉE, IMPLÉMENTÉE ET POUSSÉE. Recette UX : À VALIDER.** Priorité P1, effort M provisoire. [Fiche](orientations-a-decider.md#e1) · [Maquette v2](../visuels/maquettes-apres/E1.html).

**Objectif réalisé :** Savoir ce qui est fini, ce qui reste à faire et les effets de la prochaine action.

**Dépendances :** Transitions du domaine et dossiers existants, droits ; aucune clôture ou remise automatique.

**Critères de recette — preuves automatisées et limites dans le bilan canonique :**

1. La fin de période est expliquée sans la confondre avec clôture métier ou archivage.
2. La confirmation de clôture explique arrêt des inscriptions/validations et fixation des participants éligibles en langage courant, en conservant son caractère définitif.
3. Les dossiers restants pointent vers l’action et le responsable quand il est connu ; aucun responsable n’est inventé.
4. Information du gagnant, remise effective et enregistrement de remise restent distincts ; bilan et date de référence sont accessibles.

## Organisation initiale de la suite — historique avant réalisation

Le paragraphe suivant conserve le plan initial, remplacé pour l’exécution par le bilan canonique WA. Après décisions, conserver les catégories ci-dessus et les commentaires exacts. Pour les seules orientations validées, préparer le cadrage des contrats et critères, puis estimer les lots. D1 nécessite un diagnostic ; B1 et C1 nécessitent d’abord la clarification de leurs contrats. Les ajustements locaux D2/B3 restent candidats, sans contourner les validations serveur. Aucun ordre technique ferme n’est déduit de ce classement.

Périmètre futur possible : frontend Animation pour les présentations et parcours ; backend pour les règles, droits, brouillon partiel, référencement, import et Communication selon diagnostic. Les consommateurs commerçant, marketplace et traitements éventuels devront être identifiés si un contrat change ; aucun impact ni absence d’impact définitif n’est présumé ici.

Cette étape ne modifie ni règle métier, contrat, source applicative, migration, générateur de données, ni configuration d’exploitation. Elle n’ajoute aucune epic à la roadmap commune. Les tests proposés sont futurs ; les contrôles exécutés ici portent uniquement sur la documentation.

## Rattachement canonique ultérieur

La demande d’analyse/cadrage et l’arbitrage de primauté de l’atelier sont tracés dans l’[EPIC 73](../../../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md#workshop-ux-20261118). Son cadrage distingue corrections, évolutions et acquis AP/PO/SA, ajoute F1/G1 dans un lot P2 et remplace explicitement PO-13. Ce document conserve la présentation initiale pour la décision ; il ne crée pas de backlog d’exécution concurrent.
