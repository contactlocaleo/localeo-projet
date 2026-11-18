# Backlog UX — orientations issues du workshop simulé

**Aucun développement autorisé ni exécuté.** Adoption = majorité de rôles fictifs, pas validation de l’utilisateur. Les bénéfices sont attendus, non mesurés. Les critères ci-dessous sont des vérifications futures, pas des tests déjà réussis.

## Lecture

P0 : blocage essentiel ou risque opérationnel majeur. P1 : friction importante ou risque significatif. P2 : utile et différable. P3 : confort ou évolution future. Efforts relatifs : S = ajustement local ; M = plusieurs composants/états ; L = parcours ou contrat partagé ; XL = évolution de cycle métier. Ces tailles ne sont ni des jours ni un devis. Une inconnue backend peut modifier l’estimation.

Constats : OBSERVÉ = interface ou comportement effectivement examiné ; DÉDUIT = interprétation documentée du code/contrat ; HYPOTHÈSE = besoin ou conséquence à tester. Source principale : [registre factuel AN](../observations/observations-factuelles.md), complété par [mesures](../observations/mesures-parcours.md) et [limites](../observations/limitations.md).

## Vue d’ensemble

| ID | Orientation | Priorité | Effort | Pour /12 | Décision simulée |
| --- | --- | --- | --- | ---: | --- |
| [A1](#a1) | Donner la priorité aux actions attendues | P1 | M | 12 | ADOPTÉE |
| [A2](#a2) | Personnaliser les blocs de l’accueil | P3 | L | 0 | REJETÉE |
| [B1](#b1) | Sauvegarder avant la fin des sept étapes | P1 | L | 12 | ADOPTÉE |
| [B2](#b2) | Expliquer préparation, accords et publication | P1 | M | 12 | ADOPTÉE |
| [B3](#b3) | Proposer un seuil de passeport cohérent | P1 | S | 12 | ADOPTÉE |
| [B4](#b4) | Ajouter un formulaire unique facultatif | P2 | L | 4 | REJETÉE |
| [C1](#c1) | Rendre trouvable l’ajout d’un commerce absent | P1 | L | 9 | ADOPTÉE |
| [C2](#c2) | Sécuriser la compréhension de l’import | P1 | L | 9 | ADOPTÉE |
| [C3](#c3) | Programmer des relances facultatives | P2 | L | 6 | NON ADOPTÉE |
| [D1](#d1) | Rétablir et fiabiliser Communication | P0 | M | 12 | ADOPTÉE |
| [D2](#d2) | Diriger le suivi vers le suivi opérationnel | P1 | S | 12 | ADOPTÉE |
| [E1](#e1) | Rendre explicite le chemin de fin | P1 | M | 12 | ADOPTÉE |
| [E2](#e2) | Programmer une clôture facultative | P2 | XL | 1 | REJETÉE |
| [F1](#f1) | Enregistrer des vues filtrées | P2 | M | 7 | ADOPTÉE |
| [F2](#f2) | Regrouper les échéances dans un calendrier | P2 | L | 5 | REJETÉE |
| [G1](#g1) | Accélérer l’accès aux tâches sur mobile | P2 | M | 10 | ADOPTÉE |
| [G2](#g2) | Proposer une visite guidée facultative | P3 | M | 4 | REJETÉE |

<a id="a1"></a>
## A1 — Donner la priorité aux actions attendues

- **Mission / parcours :** E — Pilotage global ; première prise en main
- **Priorité :** P1 ; **effort :** M (provisoire).
- **Vote :** 12 pour / 0 contre / 0 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-02, AN-19 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [02](../visuels/captures-avant/02-tableau-bord-bureau.png), [32](../visuels/captures-avant/32-notifications.png), [44](../visuels/captures-avant/44-tableau-bord-mobile.png).
- **Problème :** L’accueil place de nombreuses nouvelles jaunes avant les actions ; leur apparence rapproche information positive et alerte.
- **Conséquence :** L’action urgente peut être moins facile à repérer. Effet sur les personnes : hypothèse.
- **Solution soumise :** Placer les actions à traiter et l’accès à la création avant les nouvelles ; différencier succès, information et alerte. Conserver le contexte communal, les filtres et l’accès à toutes les notifications. Aucun nouveau moteur d’alertes.
- **Bénéfice attendu :** Identifier ce qui demande une intervention, puis accéder aux nouvelles.
- **Confiance :** Élevée sur l’écran ; moyenne sur le gain supposé.
- **Risques / dépendances :** Hiérarchie et sémantique des composants existants ; aucun nouveau calcul métier d’urgence.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/A1.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#A1) · [rendu bureau](../visuels/maquettes-apres/A1-accueil-bureau.png) · [rendu mobile](../visuels/maquettes-apres/A1-accueil-mobile.png). 1 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. À contexte et droits identiques, les actions existantes à traiter et Créer sont accessibles avant les nouvelles sur bureau et mobile.
2. Succès, information et alerte ont un libellé et un repère distincts, sans dépendre seulement de la couleur.
3. Les nouvelles restent toutes accessibles ; la commune et les filtres ne sont pas perdus lors du retour.

<a id="a2"></a>
## A2 — Personnaliser les blocs de l’accueil

- **Mission / parcours :** E — Pilotage global
- **Priorité :** P3 ; **effort :** L (provisoire).
- **Vote :** 0 pour / 11 contre / 1 abstention(s) — **REJETÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** HYPOTHÈSE.
- **Sources :** AN-02 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [02](../visuels/captures-avant/02-tableau-bord-bureau.png).
- **Problème :** Les profils auraient des besoins d’affichage différents ; aucun besoin de personnalisation n’a été mesuré.
- **Conséquence :** Un écran uniforme pourrait imposer des informations peu utiles à certains rôles.
- **Solution soumise :** Permettre à chaque organisateur de choisir et déplacer les blocs de son accueil, avec restauration de la disposition standard. Personnalisation facultative.
- **Bénéfice attendu :** Adapter les informations visibles aux habitudes individuelles.
- **Confiance :** Faible : demande exploratoire, sans test réel.
- **Risques / dépendances :** Persistance des préférences, maintenance de plusieurs dispositions et accessibilité.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. La personnalisation est facultative et fonctionne au clavier sans glisser-déposer obligatoire.
2. La disposition peut être réinitialisée ; aucune information ou action critique ne devient inaccessible.
3. Les préférences respectent les droits et le contexte d’organisation.

<a id="b1"></a>
## B1 — Sauvegarder avant la fin des sept étapes

- **Mission / parcours :** A — Création et reprise
- **Priorité :** P1 ; **effort :** L (provisoire).
- **Vote :** 12 pour / 0 contre / 0 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-03 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [05](../visuels/captures-avant/05-tombola-informations.png), [12](../visuels/captures-avant/12-recapitulatif.png), [48](../visuels/captures-avant/48-sortie-saisie-mobile.png).
- **Problème :** Le premier enregistrement arrive après les sept étapes ; quitter plus tôt propose de perdre la saisie.
- **Conséquence :** Risque de ressaisie ou d’abandon lors d’une interruption, non mesuré avec des personnes.
- **Solution soumise :** Enregistrer explicitement un brouillon incomplet dès modèle, nom et commune renseignés ; reprendre les champs réellement enregistrés. Afficher état de sauvegarde et éléments manquants. Aucun envoi ni publication implicite ; les contrôles serveur de publication restent inchangés. Contrat de brouillon partiel à spécifier avant développement.
- **Bénéfice attendu :** Préparer une animation en plusieurs sessions sans prétendre qu’elle est publiable.
- **Confiance :** Élevée sur le constat ; moyenne sur la solution et son coût.
- **Risques / dépendances :** Contrat de brouillon partiel à spécifier avec le backend ; droits, validation partielle et reprise. Pas une simple retouche de bouton.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/B1.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#B1) · [rendu bureau](../visuels/maquettes-apres/B1-saisie-bureau.png) · [rendu mobile](../visuels/maquettes-apres/B1-saisie-mobile.png). 3 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. Après modèle, nom et commune, une commande explicite enregistre un brouillon incomplet et confirme seulement la sauvegarde réellement réussie.
2. Après fermeture et reconnexion, les champs enregistrés sont restitués et les éléments manquants sont listés.
3. Un échec de sauvegarde conserve la saisie et indique quoi faire ; aucune invitation ni publication n’est déclenchée.
4. Le domaine conserve les contrôles complets de publication ; un brouillon incomplet ne les contourne pas.

<a id="b2"></a>
## B2 — Expliquer préparation, accords et publication

- **Mission / parcours :** A — Publication ; B — Préparation des commerçants
- **Priorité :** P1 ; **effort :** M (provisoire).
- **Vote :** 12 pour / 0 contre / 0 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-06, AN-07, AN-08, AN-09, AN-10, AN-15 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [12](../visuels/captures-avant/12-recapitulatif.png), [14](../visuels/captures-avant/14-brouillon-cree.png), [15](../visuels/captures-avant/15-invitations-non-envoyees.png), [49](../visuels/captures-avant/49-assistant-mobile.png).
- **Problème :** Les accords conditionnent la publication ; certains diagnostics sont techniques et les étapes du résultat final restent dispersées.
- **Conséquence :** L’organisateur peut confondre création du brouillon, accord du commerce, activation d’un compte et publication.
- **Solution soumise :** Expliquer tôt le résultat de la création : brouillon préparé, puis accords, puis publication. Remplacer les diagnostics techniques par action + responsable + raison du blocage + lien ciblé ; préciser les termes de dotation sans changer ses modes. Distinguer sélection, invitation, accord, préparation et activation seulement si cette dernière est connue. Ne promettre aucun délai humain non mesuré.
- **Bénéfice attendu :** Savoir qui doit agir, pourquoi et où, sans promettre le délai de réponse de tiers.
- **Confiance :** Élevée sur les libellés et conditions observés ; moyenne sur la compréhension future.
- **Risques / dépendances :** Réutiliser les diagnostics et statuts canoniques ; vérifier les liens et les acteurs disponibles dans le contrat.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/B2.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#B2) · [rendu bureau](../visuels/maquettes-apres/B2-publication-bureau.png) · [rendu mobile](../visuels/maquettes-apres/B2-publication-mobile.png). 5 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. Avant de commencer, le parcours annonce le résultat brouillon, les prérequis d’accord et l’étape de publication.
2. Chaque blocage affiché comprend une action, un acteur connu, une raison et un lien ciblé ; aucun statut d’activation n’est inventé.
3. Les options de dotation existantes sont expliquées en langage courant, en conservant responsable et consignes.
4. L’aperçu précise quand le QR définitif devient disponible ; la distinction entre aperçu et support publié est conservée.
5. Aucun délai de 5–10 minutes n’est présenté comme acquis avant un test humain délimitant début et fin.

<a id="b3"></a>
## B3 — Proposer un seuil de passeport cohérent

- **Mission / parcours :** A — Paramétrage du passeport
- **Priorité :** P1 ; **effort :** S (provisoire).
- **Vote :** 12 pour / 0 contre / 0 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-05 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [17](../visuels/captures-avant/17-passeport-minimum-commerces.png), [19](../visuels/captures-avant/19-passeport-recapitulatif.png).
- **Problème :** Après sélection de deux commerces, le seuil proposé reste à quatre et doit être corrigé.
- **Conséquence :** Une correction évitable et une incertitude sur le fonctionnement du passeport.
- **Solution soumise :** Proposer au choix du seuil une valeur initiale compatible avec les commerces sélectionnés et expliquer la conséquence. Si la sélection change, signaler l’incompatibilité et demander un ajustement explicite, sans changer silencieusement une règle déjà choisie. Garder le contrôle serveur.
- **Bénéfice attendu :** Démarrer avec une règle compatible et compréhensible.
- **Confiance :** Élevée sur le constat DOM ; moyenne sur la règle d’initialisation à confirmer.
- **Risques / dépendances :** Bornes du domaine à respecter ; estimation S seulement si le contrat existant suffit. Capture 18 insuffisante pour voir le champ inférieur.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/B3.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#B3) · [rendu bureau](../visuels/maquettes-apres/B3-compatible-bureau.png) · [rendu mobile](../visuels/maquettes-apres/B3-compatible-mobile.png). 2 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. Une nouvelle sélection de deux commerces propose un seuil compatible et explique ce qu’il signifie.
2. Une modification de sélection qui invalide un seuil déjà choisi provoque un message et un ajustement explicite, jamais une modification silencieuse.
3. Le serveur rejette toujours une configuration invalide, y compris hors interface.

<a id="b4"></a>
## B4 — Ajouter un formulaire unique facultatif

- **Mission / parcours :** A — Création fréquente
- **Priorité :** P2 ; **effort :** L (provisoire).
- **Vote :** 4 pour / 7 contre / 1 abstention(s) — **REJETÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** HYPOTHÈSE.
- **Sources :** AN-03 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [05](../visuels/captures-avant/05-tombola-informations.png), [12](../visuels/captures-avant/12-recapitulatif.png).
- **Problème :** Les sept étapes pourraient ralentir les organisateurs fréquents ; leur coût humain n’est pas mesuré.
- **Conséquence :** Navigation répétée potentiellement coûteuse, mais le guidage peut aussi rassurer.
- **Solution soumise :** Ajouter un mode facultatif « formulaire unique » pour utilisateurs fréquents, avec les mêmes champs, validations, aperçu et confirmations que le parcours guidé, qui reste disponible.
- **Bénéfice attendu :** Accélérer la saisie experte si un besoin est démontré.
- **Confiance :** Faible : aucune comparaison humaine des formats.
- **Risques / dépendances :** Deux présentations à maintenir ; B1 et B3 peuvent déjà réduire l’effort sans nouveau mode.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. Le parcours guidé reste disponible et les deux modes utilisent les mêmes validations métier.
2. Le formulaire unique conserve aperçu, récapitulatif et confirmations.
3. Un test comparatif avec organisateurs fréquents mesure temps, erreurs et recours à l’aide avant généralisation.

<a id="c1"></a>
## C1 — Rendre trouvable l’ajout d’un commerce absent

- **Mission / parcours :** B — Ajout individuel
- **Priorité :** P1 ; **effort :** L (provisoire).
- **Vote :** 9 pour / 0 contre / 3 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-11 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [07](../visuels/captures-avant/07-selection-commercants.png), [57](../visuels/captures-avant/57-details-commerce.png).
- **Problème :** Aucun accès individuel n’a été trouvé dans les écrans explorés ; cela ne prouve pas l’absence de fonction dans tout Localeo.
- **Conséquence :** Un organisateur avec un seul commerce manquant ne sait pas poursuivre.
- **Solution soumise :** Depuis le sélecteur, proposer « Mon commerce n’est pas dans la liste » et un parcours de demande individuelle de référencement avec suivi. Réutiliser la fonction canonique disponible après vérification de sa portée ; une demande ne rend pas le commerce éligible, activé ou participant. Ne pas créer un compte actif ni envoyer d’invitation automatiquement.
- **Bénéfice attendu :** Lui donner un chemin explicite et un suivi de demande sans créer de compte actif implicite.
- **Confiance :** Moyenne : non-accessibilité locale établie, couverture de l’écosystème incomplète.
- **Risques / dépendances :** Référentiel commerçants, droits de référencement et contrat backend ; périmètre à confirmer avant chiffrage ferme.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/C1.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#C1) · [rendu bureau](../visuels/maquettes-apres/C1-selection-bureau.png) · [rendu mobile](../visuels/maquettes-apres/C1-selection-mobile.png). 3 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. Le sélecteur expose une action pour un commerce absent et décrit le résultat d’une demande de référencement.
2. Le parcours canonique existant est recherché et réutilisé ; son propriétaire et ses droits sont confirmés avant toute nouvelle fonction.
3. Le retour affiche un état réel et la prochaine action ; demande, éligibilité, activation et participation restent distinctes.
4. Aucune invitation ni activation automatique ne résulte de la simple demande.

<a id="c2"></a>
## C2 — Sécuriser la compréhension de l’import

- **Mission / parcours :** B — Import et doublons
- **Priorité :** P1 ; **effort :** L (provisoire).
- **Vote :** 9 pour / 0 contre / 3 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ / DÉDUIT.
- **Sources :** AN-12, AN-13, AN-14 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [21](../visuels/captures-avant/21-import-commercants.png), [22](../visuels/captures-avant/22-import-mapping.png), [23](../visuels/captures-avant/23-import-apercu.png), [24](../visuels/captures-avant/24-import-comparaison.png).
- **Problème :** Le modèle téléchargé exige un remappage ; les mentions obligatoire sont ambiguës ; deux lignes similaires sans identifiant fort donnent deux créations proposées et zéro conflit.
- **Conséquence :** Saisie de mapping évitable et risque de surinterpréter zéro conflit comme absence de doublon. Aucun doublon effectivement créé n’est prouvé.
- **Solution soumise :** Préassocier les colonnes reconnues du modèle fourni, laisser vérifier/corriger ; distinguer colonne requise et cellule requise ; présenter les limites de rapprochement. Signaler la similitude nom/adresse comme doute à examiner, sans fusion ni rejet automatiques, en conservant les conflits forts email/SIRET. Confirmation explicite des lignes.
- **Bénéfice attendu :** Réduire le travail mécanique et permettre une décision informée avant import.
- **Confiance :** Élevée sur l’aperçu et le code local ; moyenne sur le rapprochement proposé.
- **Risques / dépendances :** Qualité des adresses, faux positifs, contrats d’aperçu et import ; code déployé non identifié. L vaut pour l’ensemble, pas seulement les libellés.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/C2.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#C2) · [rendu bureau](../visuels/maquettes-apres/C2-apercu-bureau.png) · [rendu mobile](../visuels/maquettes-apres/C2-apercu-mobile.png). 4 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. Les en-têtes reconnus du modèle sont préassociés, visibles, corrigeables et soumis à confirmation.
2. Colonne requise et valeur requise sont distinguées, avec exemples et erreurs de ligne compréhensibles.
3. Deux lignes de même nom/adresse sans email ni SIRET sont signalées comme similitude à examiner, sans fusion ni rejet automatique.
4. Le périmètre du rapprochement est indiqué ; les conflits email/SIRET et les contrôles serveur existants sont conservés.
5. La confirmation explicite montre les lignes et effets prévus avant création ; les essais utilisent un jeu isolé.

<a id="c3"></a>
## C3 — Programmer des relances facultatives

- **Mission / parcours :** B — Invitations et préparation
- **Priorité :** P2 ; **effort :** L (provisoire).
- **Vote :** 6 pour / 5 contre / 1 abstention(s) — **NON ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** HYPOTHÈSE.
- **Sources :** AN-15 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [15](../visuels/captures-avant/15-invitations-non-envoyees.png), [58](../visuels/captures-avant/58-invitation-acceptee-existante.png).
- **Problème :** Le coût de relances répétées est anticipé par certains profils, mais aucune campagne réelle de relance n’a été observée.
- **Conséquence :** Suivi manuel potentiellement coûteux quand de nombreux commerces tardent à répondre.
- **Solution soumise :** Ajouter des relances planifiées facultatives : calendrier, aperçu des destinataires, confirmation de l’organisateur, possibilité d’annuler et contrôle des droits/plafonds à l’envoi. Aucun accord déduit d’une relance.
- **Bénéfice attendu :** Anticiper des rappels tout en gardant la maîtrise de leurs destinataires.
- **Confiance :** Faible à moyenne : besoin simulé, fréquence réelle inconnue.
- **Risques / dépendances :** Fiabilité Communication, planification backend, consentement et droits ; charge de messages à mesurer.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. Avant programmation, l’organisateur voit calendrier, destinataires et contenu et confirme explicitement.
2. Une relance peut être annulée ; droits, destinataires encore concernés et plafonds sont contrôlés à l’envoi.
3. Une relance n’est jamais assimilée à un accord ; les essais utilisent uniquement des destinataires isolés.

<a id="d1"></a>
## D1 — Rétablir et fiabiliser Communication

- **Mission / parcours :** C — Suivi et communication
- **Priorité :** P0 ; **effort :** M (provisoire).
- **Vote :** 12 pour / 0 contre / 0 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-18 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [29](../visuels/captures-avant/29-communication.png), [31](../visuels/captures-avant/31-communication-echec-confirme.png).
- **Problème :** Deux lectures Communication échouent en HTTP 500, dont une après actualisation, dans la session test.
- **Conséquence :** Le parcours de communication n’est pas utilisable dans ce contexte ; autonomie non démontrée si cette capacité est promise au lancement.
- **Solution soumise :** Diagnostiquer et rétablir la lecture Communication en erreur 500, vérifier préparation/aperçu et envoi sur destinataires isolés ; distinguer échec de lecture et envoi incertain, préserver le contexte et proposer une reprise/support. Pas de répétition automatique d’envoi.
- **Bénéfice attendu :** Préparer et suivre une communication fiable, avec une conduite claire en cas d’erreur.
- **Confiance :** Élevée sur la panne locale ; faible sur sa cause et sa portée ; effort à réestimer après diagnostic.
- **Risques / dépendances :** Endpoint campagnes-organisateur et chaîne d’envoi ; P0 pour un lancement autonome incluant Communication, pas une panne globale démontrée.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/D1.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#D1) · [rendu bureau](../visuels/maquettes-apres/D1-lecture-bureau.png) · [rendu mobile](../visuels/maquettes-apres/D1-lecture-mobile.png). 6 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. La cause est identifiée puis la lecture fonctionne sur le contexte ayant échoué et sur un jeu contrôlé pertinent.
2. Préparation, aperçu, résultat d’envoi et historique sont vérifiés avec des destinataires exclusivement isolés.
3. Un échec de lecture propose reprise ou support et conserve contexte ; un envoi dont le résultat est inconnu n’est pas rejoué automatiquement.
4. Un contrôle distingue réussite, refus et résultat incertain sans annoncer un envoi non confirmé.

<a id="d2"></a>
## D2 — Diriger le suivi vers le suivi opérationnel

- **Mission / parcours :** C — Suivi en cours
- **Priorité :** P1 ; **effort :** S (provisoire).
- **Vote :** 12 pour / 0 contre / 0 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-16, AN-17 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [25](../visuels/captures-avant/25-suivi-animation-en-cours.png), [26](../visuels/captures-avant/26-suivi-detail.png), [27](../visuels/captures-avant/27-participants-animation.png).
- **Problème :** Consulter le suivi mène au bilan de l’animation en cours ; un autre accès mène au suivi opérationnel.
- **Conséquence :** Détour et confusion entre observation en cours et bilan.
- **Solution soumise :** Faire aboutir « Consulter le suivi » au suivi opérationnel, avec accès distinct au bilan. Préserver les définitions, périmètres et dates des indicateurs ; aucun indicateur temps réel inventé.
- **Bénéfice attendu :** Accéder immédiatement à l’espace attendu.
- **Confiance :** Élevée sur le décalage ; moyenne sur le gain humain.
- **Risques / dépendances :** Routes et états existants ; vérifier la navigation retour et les droits.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/D2.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#D2) · [rendu bureau](../visuels/maquettes-apres/D2-suivi-bureau.png) · [rendu mobile](../visuels/maquettes-apres/D2-suivi-mobile.png). 2 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. Sur une animation en cours, Consulter le suivi ouvre l’espace opérationnel attendu.
2. Le bilan dispose d’un accès distinct et explicitement nommé.
3. Les définitions inscription, progression, qualification, validation, ainsi que dates et périmètres, restent visibles et exactes.

<a id="e1"></a>
## E1 — Rendre explicite le chemin de fin

- **Mission / parcours :** D — Clôture, lots et bilan
- **Priorité :** P1 ; **effort :** M (provisoire).
- **Vote :** 12 pour / 0 contre / 0 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ.
- **Sources :** AN-20, AN-21 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [35](../visuels/captures-avant/35-fin-archivage.png), [37](../visuels/captures-avant/37-gains-remises.png), [38](../visuels/captures-avant/38-bilan-cloturee.png), [62](../visuels/captures-avant/62-confirmation-cloture-detail.png), [63](../visuels/captures-avant/63-gagnant-email-masque.png).
- **Problème :** Une période terminée peut rester En cours ; clôturée, terminée et archivée sont distinctes ; un email gagnant n’équivaut pas à une remise enregistrée.
- **Conséquence :** Risque d’interpréter trop tôt le travail comme terminé ou de mal comprendre une action définitive.
- **Solution soumise :** Expliquer près de l’action les états « période finie », « clôturée », « terminée », « archivée », leurs conséquences et la prochaine tâche. Réutiliser les dossiers à résoudre existants et leur responsable connu ; remplacer le jargon de gel par une explication compréhensible. Conserver confirmation définitive, distinction informer/remettre et droits métier.
- **Bénéfice attendu :** Savoir ce qui est fini, ce qui reste à faire et les effets de la prochaine action.
- **Confiance :** Élevée sur les états consultés ; moyenne sur leur compréhension ; exécution de clôture non vérifiée.
- **Risques / dépendances :** Transitions du domaine et dossiers existants, droits ; aucune clôture ou remise automatique.
- **Maquette v2 :** [parcours interactif](../visuels/maquettes-apres/E1.html) · [comparatif AVANT/APRÈS](../visuels/comparatif-avant-apres.html#E1) · [rendu bureau](../visuels/maquettes-apres/E1-periode-bureau.png) · [rendu mobile](../visuels/maquettes-apres/E1-periode-mobile.png). 4 état(s) illustré(s). [Revue et arbitrages](arbitrages-maquettes.md).

**Critères d’acceptation futurs**

1. La fin de période est expliquée sans la confondre avec clôture métier ou archivage.
2. La confirmation de clôture explique arrêt des inscriptions/validations et fixation des participants éligibles en langage courant, en conservant son caractère définitif.
3. Les dossiers restants pointent vers l’action et le responsable quand il est connu ; aucun responsable n’est inventé.
4. Information du gagnant, remise effective et enregistrement de remise restent distincts ; bilan et date de référence sont accessibles.

<a id="e2"></a>
## E2 — Programmer une clôture facultative

- **Mission / parcours :** D — Clôture
- **Priorité :** P2 ; **effort :** XL (provisoire).
- **Vote :** 1 pour / 9 contre / 2 abstention(s) — **REJETÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** HYPOTHÈSE.
- **Sources :** AN-20 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [33](../visuels/captures-avant/33-publication-cloture.png), [62](../visuels/captures-avant/62-confirmation-cloture-detail.png).
- **Problème :** Une clôture manuelle pourrait être oubliée ; sa fréquence et son coût ne sont pas mesurés.
- **Conséquence :** Une animation pourrait rester en attente d’action après la période prévue.
- **Solution soumise :** Ajouter une clôture programmée facultative à une date confirmée, avec précontrôle, avertissement préalable et annulation possible avant exécution ; ne pas tirer au sort ni déclarer de remise automatiquement. Nouvelle règle serveur à concevoir, avec traitement d’incidents en cours.
- **Bénéfice attendu :** Éviter l’oubli dans les cas où une règle programmée est appropriée.
- **Confiance :** Faible : besoin et règle future non validés.
- **Risques / dépendances :** Nouvelle transition planifiée backend, irréversibilité et incidents ; préserver la décision humaine aux cas sensibles.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. La date et les conséquences sont confirmées explicitement, avec avertissement et possibilité d’annuler avant exécution.
2. Un précontrôle traite les incidents et prérequis ; un échec est visible sans état partiellement annoncé comme clos.
3. Aucun tirage ni remise n’est déclenché par cette programmation.
4. Les règles serveur, droits et reprise après incident sont spécifiés et testés avant activation.

<a id="f1"></a>
## F1 — Enregistrer des vues filtrées

- **Mission / parcours :** E — Pilotage multi-animation
- **Priorité :** P2 ; **effort :** M (provisoire).
- **Vote :** 7 pour / 3 contre / 2 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** HYPOTHÈSE.
- **Sources :** AN-23 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [03](../visuels/captures-avant/03-animations-bureau.png), [39](../visuels/captures-avant/39-recherche-brouillons.png).
- **Problème :** Le retour conserve déjà la recherche ; le besoin supplémentaire de vues sauvegardées et partagées reste à démontrer.
- **Conséquence :** Reconstituer les mêmes filtres pourrait coûter du temps aux équipes récurrentes.
- **Solution soumise :** Enregistrer et partager des vues de liste filtrées au sein de l’organisation, tout en gardant filtres actifs visibles, retour conservé, droits et réinitialisation.
- **Bénéfice attendu :** Retrouver un périmètre habituel tout en comprenant les filtres actifs.
- **Confiance :** Faible à moyenne : usage multi-animation simulé sur petit jeu observé.
- **Risques / dépendances :** Stockage des préférences et droits ; le comportement de retour déjà satisfaisant doit être préservé.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. Une vue enregistre des filtres explicites et dispose d’une réinitialisation simple.
2. Le partage reste limité à l’organisation et ne donne aucun droit supplémentaire.
3. Le retour conserve la recherche courante et signale une vue devenue incompatible avec les droits.

<a id="f2"></a>
## F2 — Regrouper les échéances dans un calendrier

- **Mission / parcours :** E — Pilotage multi-animation
- **Priorité :** P2 ; **effort :** L (provisoire).
- **Vote :** 5 pour / 6 contre / 1 abstention(s) — **REJETÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** HYPOTHÈSE.
- **Sources :** AN-02, AN-15, AN-20, AN-23 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [02](../visuels/captures-avant/02-tableau-bord-bureau.png), [03](../visuels/captures-avant/03-animations-bureau.png), [35](../visuels/captures-avant/35-fin-archivage.png).
- **Problème :** Dates et échéances sont réparties entre plusieurs écrans ; le besoin d’une représentation calendrier n’a pas été testé.
- **Conséquence :** Risque anticipé de perdre une échéance quand plusieurs animations sont gérées.
- **Solution soumise :** Ajouter un calendrier transversal des dates et échéances avec retour vers les actions existantes, en complément de la liste et sans remplacer les statuts métier.
- **Bénéfice attendu :** Repérer les périodes qui nécessitent une intervention.
- **Confiance :** Moyenne sur la dispersion ; faible sur la supériorité d’un calendrier.
- **Risques / dépendances :** Consolidation des échéances, fuseau horaire, filtre d’organisation, accessibilité.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. Les échéances proviennent des données canoniques et renvoient aux actions existantes avec droits vérifiés.
2. Le calendrier complète la liste, sans remplacer les statuts métier.
3. Une alternative lisible en liste et au clavier présente le même périmètre et les mêmes dates.

<a id="g1"></a>
## G1 — Accélérer l’accès aux tâches sur mobile

- **Mission / parcours :** C / D / E — Pilotage mobile
- **Priorité :** P2 ; **effort :** M (provisoire).
- **Vote :** 10 pour / 0 contre / 2 abstention(s) — **ADOPTÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** OBSERVÉ / HYPOTHÈSE.
- **Sources :** AN-24 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [45](../visuels/captures-avant/45-animations-mobile.png), [49](../visuels/captures-avant/49-assistant-mobile.png), [51](../visuels/captures-avant/51-invitations-mobile.png), [52](../visuels/captures-avant/52-navigation-mobile.png), [54](../visuels/captures-avant/54-fin-mobile.png).
- **Problème :** Le détail mobile donne accès à dix-huit rubriques par un sélecteur ; une difficulté à retrouver les tâches est supposée, pas mesurée.
- **Conséquence :** Recherche et changements de rubrique potentiellement coûteux sur le terrain.
- **Solution soumise :** Ajouter dans le détail mobile des accès aux tâches courantes de l’animation, selon droits et état, tout en gardant le sélecteur complet et un repère de rubrique. Vérifier téléphone réel, clavier et lecteur d’écran avant de conclure à un gain.
- **Bénéfice attendu :** Retrouver plus vite les tâches courantes sans perdre les fonctions secondaires.
- **Confiance :** Élevée sur la structure ; faible à moyenne sur la difficulté humaine.
- **Risques / dépendances :** Navigation responsive existante ; le panneau partiel de la capture 52 ne suffit pas à établir un défaut de rendu.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. Les raccourcis suivent état et droits de l’animation ; rubrique et contexte restent visibles.
2. Le sélecteur complet reste disponible et les retours conservent le contexte.
3. Un contrôle sur téléphone réel, au clavier et avec lecteur d’écran vérifie ordre de focus, libellés et accès ; un test humain mesure le gain.

<a id="g2"></a>
## G2 — Proposer une visite guidée facultative

- **Mission / parcours :** Transverse — Prise en main
- **Priorité :** P3 ; **effort :** M (provisoire).
- **Vote :** 4 pour / 6 contre / 2 abstention(s) — **REJETÉE**
- **Validation utilisateur :** en attente ; les votes simulés ne constituent pas votre validation.
- **Nature du constat :** HYPOTHÈSE.
- **Sources :** AN-02, AN-10, AN-24 dans le [registre factuel](../observations/observations-factuelles.md) ; captures [02](../visuels/captures-avant/02-tableau-bord-bureau.png), [49](../visuels/captures-avant/49-assistant-mobile.png).
- **Problème :** Certains nouveaux organisateurs pourraient souhaiter un aperçu guidé ; son efficacité n’est pas établie.
- **Conséquence :** Besoin anticipé d’aide à l’orientation, sans preuve qu’une visite soit le bon format.
- **Solution soumise :** Proposer une visite guidée facultative de première utilisation, quittable/rejouable, sans blocage de la navigation ni répétition imposée. Elle complète les aides contextuelles ; elle ne remplace pas la correction des obstacles.
- **Bénéfice attendu :** Fournir un repère initial aux personnes qui le souhaitent.
- **Confiance :** Faible : proposition exploratoire.
- **Risques / dépendances :** Maintenance au fil des écrans, accessibilité ; à comparer à une aide contextuelle simple.
- **Maquette :** hors périmètre de l’étape 3 (priorité ou adoption non éligible).

**Critères d’acceptation futurs**

1. La visite est facultative, quittable, rejouable et utilisable au clavier.
2. Elle ne bloque jamais une action ni ne se répète sans demande.
3. Les aides contextuelles demeurent disponibles et les obstacles connus sont corrigés indépendamment.

## Dépendances et ordre de préparation

1. Diagnostiquer D1 et confirmer le parcours canonique C1 avant de figer leurs coûts. Préparer des destinataires et objets exclusivement isolés pour les vérifications futures.
2. Traiter les propositions locales D2/B3 et les formulations B2/E1 dans les futures maquettes, en préservant les règles du domaine et les retours de navigation.
3. Spécifier le brouillon partiel B1 et le périmètre de C2 avant toute implémentation. A1 réorganise les informations existantes ; il ne crée pas de règle de priorité métier.
4. F1 et G1 sont adoptées P2 : confronter aux usages réels après les parcours essentiels. Les autres propositions restent non retenues.

Les propositions visuelles de l’étape 3 sont isolées du code applicatif dans `visuels/maquettes-apres/`. Les votes ne remplacent aucune validation explicite.
