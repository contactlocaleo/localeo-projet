# Localeo Live — audit visuel de la fiche animation

**8 novembre 2026.** Reprise de l’inspection visuelle demandée après une première
interruption du contrôle du navigateur. Objet : rapprocher la fiche publique
des codes UX/UI de l’accueil et faciliter la décision de participer sur mobile.

Suite demandée le **9 novembre** : les douze axes sont détaillés dans la
[spécification E73-EVO-LIVE-FICHE](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#évolution-du-9-novembre-2026--fiche-animation-immersive-e73-evo-live-fiche)
et sa [conception §9](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md#9-fiche-animation-immersive--e73-evo-live-fiche).
Ce lien ne transforme pas l’audit en preuve de correction ou de déploiement.

## Conclusion

**La rupture visuelle avec l’accueil est confirmée sur TEST.** La fiche assemble
retour, métadonnées, titre, raccourcis, objectif, inscription, annuaire, trois
compteurs, dates et sections de détail dans une longue colonne. L’habitant doit
reconstituer lui-même ce qu’il va faire, chez qui et sous quelles conditions.

L’impression « trop textuelle » vient surtout de cet empilement de libellés,
des espaces entre les repères et du manque de composition commune. La description
et le règlement sont déjà repliables : ce bon principe mérite d’être conservé.
La priorité est une **fiche de défi** : promesse concrète, condition essentielle,
action claire, récompense et lieux de jeu faciles à repérer.

Deux défauts de parcours sont observés directement : l’obligation d’achat reste
cachée dans les conditions, et le raccourci « Les conditions » mène à une section
encore fermée, qui demande une seconde activation.

## Méthode, preuves et limites

- Fiche demandée : [TEST — Passeport Delphine](https://test-animations.localeo.city/live/animations/6d6f2b0f-c865-4bda-9de2-4ee752c6990d),
  sans flyer. Vue publique avec inscription proposée, deux validations, un
  participant, zéro gagnant, un lot de formation et deux partenaires observés.
- Comparaison avec [l’accueil](https://test-animations.localeo.city/live/decouvrir)
  une fois chargé, dans la même session : cartes arrondies, promesse en phrase,
  dates compactes, un indicateur de lots et CTA bleu nuit. Les sections En ce
  moment/Prochainement et Animations/Commerçants y sont nettement identifiées.
- Variante avec flyer : [TEST — passeport TCA](https://test-animations.localeo.city/live/animations/99527546-96eb-4a76-9a4b-b88db26ef12a).
  Image chocolat configurée visible sur la carte et la fiche ; aucun visuel
  de substitution demandé ou créé.
- Observation de Chrome sur ordinateur, fenêtre d’environ 1 020 × 950 pixels,
  zoom navigateur préexistant **90 %** ; aperçu mobile DevTools **iPhone 16,
  393 × 852**, échelle « Fit to window », sans ralentissement réseau. Les
  premiers réglages Responsive n’étant pas fiables pour attester la largeur,
  les conclusions mobiles utilisent le preset iPhone ensuite sélectionné.
  Ce n’est ni un téléphone physique ni une mesure de pixels CSS du bureau.
- Parcours inspecté : début de fiche, défilement vers lots/partenaires,
  raccourci Conditions, ouverture de l’accordéon, accueil et variante avec flyer.
  Les rendus et arbres d’accessibilité ont été consultés. Aucun formulaire
  d’inscription soumis, accès récupéré, consentement ou suivi modifié volontairement.
- Lecture indépendante du frontend : `c40ee5ab02f463dd159874a7e96f5748200b0403`,
  modifications locales préexistantes de header conservées. Documentation de
  base `e04248e0ea4cb3f08e5f68081f751822f27bb350`. Le SHA réellement déployé
  n’est pas attesté. Les propositions du header encore locales ne servent pas
  de preuve du rendu TEST.
- Pas de tests de contraste instrumentés, zoom 200 %, clavier complet,
  lecteur d’écran, CLS ou compréhension par des habitants. Pas de chronométrage
  API pendant cette reprise. Les états connecté/inscrit, fermé, annulé, backend
  lent/erreur et transition directe entre deux fiches n’ont pas été recettés
  visuellement ; les constats correspondants ci-dessous sont explicitement code.

## Constats et recommandations

| Référence / priorité | Constat et preuve | Proposition |
| --- | --- | --- |
| **FD-01 — P1 : expliquer l’effort avant l’inscription** | **Observé** : « Votre défi — 2 validations à réaliser » sépare le nombre de son libellé et ne précise pas le geste. L’accordéon révèle ensuite « Effectuer un achat, sans montant minimum, chez un commerçant participant… ». L’accueil est plus concret : « Faites valider votre passage chez 2 commerçants ». | Une promesse en phrase, avec pictogramme et nombre intégré. Rendre l’achat obligatoire visible près de l’action, à partir des règles publiques réelles. Ajouter un guide illustré court : s’inscrire, se rendre chez les partenaires, faire valider ses passages selon les règles. Aucun passage supplémentaire imposé à une tombola publique. |
| **FD-02 — P1 : composer un premier écran cohérent avec l’accueil** | **Observé** : grand espace entre retour et statut, commune/code postal, moteur sur une autre ligne, titre puis raccourcis ; bloc d’objectif rectangulaire et CTA orange plat. Sur ordinateur, la colonne est étroite avec beaucoup d’espace latéral ; sur mobile le contexte occupe plusieurs étages. **Code** : `.live-main` 760 px contre accueil 1 080 px ; styles de challenge et CTA distincts. | Reprendre une même famille de carte/section : pictogramme de moteur, titre, commune, statut/période compacte, promesse et action. Donner un rôle constant au bleu nuit et à l’orange ; harmoniser rayons, bordures, espacement et poids typographiques dans les composants sources. Sur bureau, organiser éventuellement le complément en deux zones ; sur mobile conserver une colonne lisible. |
| **FD-03 — P1 : ouvrir la bonne participation** | **Code, non observé dans cette session** : pour un habitant reconnu inscrit, le CTA mène à toute la liste `/live/animations`, quelle que soit la fiche consultée. Un état inscrit côté installation ne garantit pas un token personnel local. | Un accès local confirmé : « Reprendre ma participation » vers cet accès précis. Plusieurs accès : choix explicite. Aucun accès personnel local : « Retrouver mon inscription ». Ne jamais emprunter le token d’une autre participation à la même animation. |
| **FD-04 — P2 : hiérarchiser les chiffres** | **Observé** : 1 participant, 0 gagnant et 1 lot sont trois grands nombres de même poids ; le zéro gagnant occupe une place importante avant le résultat. Les dates et la note de dotation sont encore séparées. | Un indicateur dominant adapté au moment de l’animation, puis les chiffres utiles en second niveau. Par exemple, mettre le lot à gagner en valeur avant tirage ; résultats publiés ensuite. Aucun compteur animé ou total de « lots restants » déduit d’une dotation totale ; aucun zéro transformé en activité fictive. |
| **FD-05 — P2 : rendre le gain désirable et compréhensible** | **Observé** : la récompense n’arrive qu’après compteurs, dates et description repliée ; bloc « Les récompenses du défi » séparé par des filets. Dans l’exemple, le lot est explicitement fictif de formation. | Un aperçu compact « À gagner » près du défi, puis une section graphique distincte avec nature du lot et modalités utiles. Garder les mentions de formation. « Participer au tirage » ou « qualifié » uniquement lorsque le moteur l’autorise ; montrer le détail complet sur demande sans confondre dotation, disponibilité et gain personnel. |
| **FD-06 — P2 : donner un sens aux commerçants** | **Observé** : une grande entrée « Les commerçants de l’animation » dans l’introduction, puis les deux cartes partenaires plus bas, après les lots. Le lien d’annuaire est déjà visible et utile. | Une section « Où jouer ? » identifiable par pictogramme et accent communs à l’accueil. Quelques partenaires dans une fenêtre bornée et une action « Tous les commerçants », avec profil, horaires et itinéraire. Associer le commerce à l’étape de jeu sans reconstruire une progression publique. Préserver les lieux secrets des chasses. |
| **FD-07 — P1 : rendre le raccourci Conditions effectif** | **Reproduit visuellement** : le lien ajoute `#animation-conditions` et déplace la page, mais l’accordéon reste fermé. Une deuxième activation révèle les conditions. | Une activation ouvre la section et place correctement le focus, ou conduit vers un détail déjà ouvert. Afficher les conditions essentielles avant inscription ; réserver au niveau dépliable les explications longues et le règlement complet. |
| **FD-08 — P2 : rapprocher la récupération du choix d’inscription** | **Observé** : « Retrouver mon inscription », son explication, favori, partage et aide sont tout en bas, après les partenaires et conditions. « M’inscrire » demeure fixé sur mobile. | « Déjà inscrit ? Retrouver mon accès » près de l’action principale, discret et explicite. Favori et partage dans une zone secondaire cohérente. Ne pas multiplier les appels à l’action de même importance ni provoquer un envoi d’email sans demande explicite. |
| **FD-09 — P2 : intégrer le flyer au défi** | **Observé** : variante sans flyer essentiellement composée de textes et de compteurs ; avec flyer, grande image rectangulaire avant le titre, qui repousse le contexte. Le visuel réel est correctement réutilisé. **Code** : son conteneur disparaît en cas d’échec, contrairement aux cartes d’accueil ; déplacement non mesuré. | Identité graphique compacte cohérente avec les cartes, titre/objectif proches du visuel. Sans flyer : pictogramme du moteur et composition graphique, sans image inventée ni grand emplacement vide. Image lente/en erreur : géométrie stable ; vérifier recadrage et CLS au rendu avant de conclure. |
| **FD-10 — P2 : harmoniser retour et actualisation** | **Observé** : retour textuel dans une ligne isolée, sans actualiser sur la fiche réussie ; l’accueil possède son bouton pictogramme au niveau du titre. | Une barre locale cohérente : retour nommé, repère de page et actualiser accessible. Préserver contexte/focus/position du programme au retour ; réactualisation discrète des mêmes données, sans retour au grand écran d’attente ni nouvelle boucle de polling. |
| **FD-11 — P2 : contextualiser états et aide** | **Code seulement** : une animation annulée peut recevoir une phrase invitant à découvrir le résultat d’un tirage, même sans résultat ; l’aide peut évoquer une étape ou un suivi personnel absent de la fiche publique. | Distinguer découverte, inscrit avec accès, inscription future autorisée, inscriptions fermées, clôture avant résultat, résultat publié et annulation. Texte d’aide propre à la découverte publique ; les indications personnelles restent dans la participation autorisée. |
| **FD-12 — P1 à reproduire : garder contenu et action synchronisés** | **Observé** : l’ouverture de TCA remplace le contenu par un grand panneau « Chargement de l’animation… ». **Code** : une transition directe A→B conservant le même composant peut garder le contenu A pendant que l’URL d’inscription utilise B ; ce mélange précis n’a pas été reproduit. | État de lecture identifié par animation, action activable seulement pour la même identité validée ; squelette adapté au premier affichage et maintien sobre au rafraîchissement du même contexte. Annuler les demandes obsolètes et réinitialiser le focus pour la nouvelle fiche. Aucun cache ne doit autoriser QR, inscription ou gain. |

## Composition recommandée

Ordre mobile proposé, à concevoir puis tester :

1. **Retour / identité / actualiser** : même logique que les autres pages Live.
2. **Le défi** : visuel configuré ou pictogramme, titre, commune, période/statut,
   promesse concrète et condition importante. Une seule action principale,
   conservée au-dessus de la navigation basse si nécessaire.
3. **Comment jouer ?** : trois étapes illustrées propres au moteur. Sur une
   fiche publique, invitation à participer ; dans la participation, progression
   personnelle seulement si elle est fournie par le serveur.
4. **À gagner** puis **Où jouer ?** : sections clairement marquées, aperçus bornés
   et approfondissement volontaire. La priorité relative peut s’adapter au jeu.
5. **Conditions complètes / règlement / aide** : accès explicite, légende courte
   et contenu détaillé dépliable. Récupération proche du CTA, partage/favori secondaires.

L’esprit jeu vient d’un objectif compréhensible, d’étapes reconnaissables et d’un
retour de réussite réel. Pas de badges de progression avant inscription, faux
compte à rebours, classement fictif, célébration sur GET ou pluie d’effets.
Un compte à rebours éventuel exige date et fuseau autoritaires, traitement de
l’échéance et mouvement réduit ; une date compacte est suffisante sans cela.

## Éléments à conserver

- **Observé sur mobile** : action d’inscription fixée au-dessus de la navigation
  basse ; elle reste accessible pendant la lecture des conditions. Aucun
  chevauchement bloquant de cette action n’a été constaté sur le preset inspecté.
- Retour contextuel, liens publics sans token, règlement repliable et profils
  de partenaires consultables. La page publique ne présente pas de QR personnel.
- Description repliée plutôt qu’un texte intégral imposé ; image réelle du flyer
  et absence d’illustration fabriquée lorsqu’il n’y en a pas.
- **Code** : affichage public avant enrichissement personnel ; récupération
  non énumérante ; aide chargée sur ouverture volontaire. Une animation future
  peut accepter des inscriptions si le serveur le permet : la fermeture du QR
  avant démarrage ne doit pas fermer implicitement ces inscriptions.

## Traçabilité du diagnostic et recette recommandée

| Attente | Source applicable / code | Preuve et état de cet audit | Suite |
| --- | --- | --- | --- |
| Cohérence des composants et lisibilité mobile | [Conception E73 §2 et §7](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md) ; `AnimationChallengeIntro.jsx`, `AnimationDetailView.jsx`, `animation-challenge.css`, `live-public-detail.css`, `live-discovery.css` | Comparaison visuelle fiche sans/avec flyer et accueil, FD-01/02/04/05/06/09/10. **Partiel** : plusieurs codes et composants diffèrent. | Maquette/composition puis Playwright 320 × 568, 393 × 852, tablette et bureau ; zoom, contraste, clavier, état sans image et titre long. |
| Compréhension avant engagement | Même conception ; `AnimationRulesAndRegulation.jsx`, raccourci `AnimationChallengeIntro.jsx:33`, accordéon `AnimationDetailView.jsx:117` | Obligation d’achat découverte dans le contenu fermé et double geste Conditions, FD-01/07. **Non satisfait** pour l’accès direct utile aux conditions. | Test d’ouverture en un geste, focus et achat lisible avant action. Ne pas recopier génériquement toute une configuration en libellés. Aucun `[object Object]` observé dans cet exemple. |
| Continuité personnelle | [Spécification Live](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md) ; `LiveAnimationDetail.jsx:57–80` | FD-03/08/11 : récupération visible en bas, branche inscrit et statuts revus dans le code. **Partiel**, états privés non recettés. | Accès unique/multiple/absent, inscrit sur installation sans token local, futur, fermé, annulé, résultat absent/présent ; aucun accès emprunté. |
| Fluidité et identité de lecture | [Performance E73 §8](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-adhesion-conception.md#8-performance-des-lectures--e73-evo-live-performance), LP-02/12/14/18 ; `LiveAnimationDetail.jsx:30–48`, `LiveApp.jsx:677` | Attente en panneau observée ; risque A→B et erreur flyer issus du code. **Non vérifiable visuellement** pour le mélange, le CLS et les percentiles. | Réponses lentes/inversées, changement direct A→B, erreurs/retours, revalidation même contexte, mesures de chargement selon le rapport API existant. |

Les propositions respectent les règles publiées, la qualification du moteur et
la distinction installation/carnet/participation. Les API et performances ne
sont pas réputées corrigées par un changement de présentation ; le
[rapport API](../backend/audit-performance-api-localeo-live-2026-11-08.md) reste
la référence de leurs mesures.

Audit seul : nouveau rapport et index documentaire ; aucun source applicatif,
contrat, statut de roadmap, migration ou générateur modifié. Les travaux locaux
antérieurs de header et de spécification performance sont préservés. Aucun test
applicatif nouveau exécuté, commit, push ou déploiement dans cette reprise.
