# Contre expertise UX du parcours organisateur Localeo Animation

17 novembre 2026. Synthèse du [rapport initial](localeo-animation-utilisabilite-pilotage-2026-11-17.md), après quatre inspections indépendantes puis confrontation.

**Conserver la cible de continuité du parcours, en commençant par cinq changements circonscrits : rendre les refus de publication compréhensibles, rétablir la lecture à 400 %, protéger la saisie des paramètres, donner accès aux chiffres depuis le suivi, puis raccorder préparation, publication et reprise.** Les outils principaux existent : prochaine action, création guidée, Assistant, guide Chasse, bilan, fin et clonage. Les observations justifient leur raccordement et quelques correctifs ; elles ne démontrent pas le besoin d’une refonte générale.

La promesse **créer et publier en 5 à 10 minutes**, la facilité pour un véritable novice et l’économie procurée par le réemploi restent à mesurer. Aucune publication, nouvelle édition, remise ou synchronisation avec Live/Pro n’a été exécutée. Les critères de création commune **CU-01 à CU-06 restent une décision utilisateur acquise**, avec réalisation et recette à démontrer.

## Méthode indépendante et portée

Quatre agents : UX métier, organisateur novice simulé, interface/accessibilité, produit/technique. Chacun a remis une **phase A figée avant lecture du rapport contesté ou des autres conclusions**. La phase B confronte cette observation au même rapport figé ; trois expertises ajoutent une lecture statique. Certains avaient lu README/AGENTS et spécification d’entrée. L’agent de synthèse a travaillé après les quatre remises, à partir des preuves consignées.

L’« organisateur novice » est une **simulation cognitive par agent**, pas un test avec un membre d’association. Les conséquences de compréhension et les gains attendus sont donc des hypothèses, même lorsqu’un chemin d’écran est certain.

Inspection par Chrome natif/CUA, captures et arbre accessible, contrôle DOM indisponible. Les experts ont utilisé **successivement la même fenêtre et session**, compte TEST, Bouliac. L’indépendance porte sur l’analyse ; défilement et historique étaient partagés. Le parent a utilisé la connexion pour établir l’accès ; les experts n’ont pas évalué ce parcours, un premier accueil vide ou d’autres rôles.

Les experts ont observé des captures de fenêtre d’environ 1 500 × 952 et 502 × 952, parfois une largeur intermédiaire : **ces dimensions incluent le navigateur et ne mesurent pas le viewport CSS**. Après les expertises, le parent a corroboré le défaut à 400 %, puis consulté le guide Chasse en mode Responsive DevTools **390 × 844 et 844 × 390**, dimensions définies dans l’interface, zoom navigateur 100 %. Ce complément n’appartient à aucune phase aveugle et ne couvre que lecture, défilement et rotation du guide. Aucun appareil physique, toucher, clavier virtuel, Safari/iOS, Android ou lecteur d’écran n’a été éprouvé.

Les recettes locales/synthétiques initiales sont **rapportées, non rejouées**. Aucun build/test applicatif supplémentaire. Le HEAD Animation `74a45f27bd66caa219b56b5d86e191ee513351d4` concorde avec le rapport ; il **n’atteste pas la version déployée**. Même réserve pour le backend `20ec49c92690d5078ec697c527f1a20054c9a4d1`. `https://test-animations.localeo.city/` présentait le portail organisateur [TEST], malgré la répartition des origines différente du README ; aucune généralisation.

## Preuves réutilisables

Routes paramétrées : remplacer `{id}` par une animation autorisée dans l’état indiqué. Les noms permettent de retrouver l’échantillon TEST, susceptible d’évoluer. Les preuves sont explicitées sans dépendre des notes temporaires.

| ID | Écran, manipulation et résultat établi | Provenance et limite |
| --- | --- | --- |
| E01 | `/`, `/animations`, `/animations/nouvelle` : prochaines actions nommées, six modèles décrits, étapes adaptées ; Tombola publique à cinq étapes, Tombola locale à sept ; garde de sortie visible. | TEST : UX A01–03, novice N01–02, technique PT-A01–07. Création arrêtée avant commande finale. |
| E02 | « Test jeu des vitrines », `/animations/{id}?onglet=configuration` : « Préparer la publication » arrive dans Configuration ; publication bloquée par `VITRINES_NON_PREPAREES` et `AUCUN_ASSET_PERSONNALISE`, sans correction ciblée adjacente. Assistant trouvé séparément, avec 7/9 contrôles prêts. | TEST : UX A04, novice N03–05 ; codes vus visuellement par UX et dans l’arbre natif par le novice. [PublicationReadiness](../../../../localeo-animation/src/app/components/LotPaymentPanel.tsx) traduit peu de motifs puis affiche le code brut. |
| E03 | Chasse « La lanterne des veillées », même route Configuration : entrée sur Parcours déjà validé ; Commerces/Terrain restent à compléter. Acteur externe et travail parallélisable explicités. Préparation accompagnée : objectif annoncé de cinq jours ouvrés après demande complète, hors compléments. | TEST : technique PT-A08–11 ; complément parent VP04. Ce délai ne mesure pas le temps actif de saisie. |
| E04 | « Test juste prix Local », `?onglet=live` : statut et commandes Suspendre/Clôturer/Annuler, sans compteur de participation. Résultats ouvre Fin et archivage ; `?onglet=bilan` affiche chiffres, fraîcheur, définitions, satisfaction non collectée et exports. | TEST : quatre inspections, notamment UX A05, novice N06–08, accessibilité A08–10, technique PT-A12–14. Ni calculs ni exports vérifiés. |
| E05 | Même Juste Prix, `/animations/{id}/cloner` : nouveau brouillon annoncé ; textes sélectionnables, scénario/paramètres non reprenables fidèlement, visuels indisponibles sur cette source ; revalidations explicites. | TEST : UX A06, novice N09. Formulaire consulté, création annulée. Ni panne du clonage ni portée de tous les modèles démontrées. |
| E06 | Guide Chasse à **400 % affichés dans Chrome**, fenêtre maximisée : en-tête et navigation basse occupent presque toute la hauteur ; défiler ne rend pas le guide utilement lisible. À 100 %, contenu lisible. | TEST : accessibilité A07, corroboration parent VP01. Défaut visuel circonscrit ; parcours clavier complet et viewport normatif non mesurés. |
| E07 | Fenêtres étroites : listes et formulaires s’empilent sans débordement global observé, contexte persistant volumineux. Parent à **390 × 844 / 844 × 390** : guide lisible en défilant, même rubrique conservée après rotation, sans reproduire l’impossibilité de E06. | TEST : quatre experts ; VP05 seul pour dimensions téléphone définies. Aucune saisie modifiée pendant la rotation. |
| E08 | [ExploitationParameters](../../../../localeo-animation/src/app/components/ExploitationParameters.tsx) : Actualiser ouvre le formulaire ; `dirty` reste local, sans garde de sortie. [PreparationNavigation](../../../../localeo-animation/src/app/components/PreparationNavigation.tsx) protège séparément la commande. | Code local, confirmé par trois lecteurs. Perte de saisie déduite du démontage, non reproduite en TEST ; concerne le suivi générique. |
| E09 | [App](../../../../localeo-animation/src/app/App.tsx), [assistantNavigation](../../../../localeo-animation/src/app/lib/assistantNavigation.ts), [HuntPreparationWorkspace](../../../../localeo-animation/src/app/components/HuntPreparationWorkspace.tsx) : défaut `workflow`, certaines corrections manuelles vers Configuration sans section, sous-étape Chasse locale ; messages après publication sans bouton de suite. | Code local. Panneaux internes Chasse conservés pendant leur montage ; sortie puis remontage et publication non joués. |
| E10 | App : motif d’action désactivée dans `title` ; repli de clôture sur actions vides/statut ; « Télécharger le flyer » ouvre une rubrique. | Code local indépendant. Garde finale des droits conservée : aucune faille d’autorisation établie. |
| E11 | [ExploitationView](../../../../localeo-animation/src/app/components/ExploitationView.tsx) contient indicateurs et détails repliés ; [JustePrixExploitation](../../../../localeo-animation/src/app/components/JustePrixExploitation.tsx) est un autre composant. [FinAnimationWorkspace](../../../../localeo-animation/src/app/components/FinAnimationWorkspace.tsx) possède déjà dossiers, filtres et bilan. | Code local et E04. Les métriques du suivi générique ne décrivent pas tous les moteurs ; aucun incident caché reproduit. |
| E12 | [AnimationCreationLayout](../../../../localeo-animation/src/app/components/AnimationCreationLayout.tsx) existe ; création manuelle, préparation Chasse et réemploi utilisent des protocoles différents. [PreparationCommand](../../../../localeo-animation/src/app/components/PreparationCommand.tsx) distingue commande et résultat incertain. | Lecture technique ciblée. Différence de réconciliation à qualifier par famille ; aucun doublon de création constaté. |
| E13 | Ligne activable de confirmation : rapport initial, 358 × 44 en portrait 390 ; hauteur 20 en paysage/tablette. [mobile.css](../../../../localeo-animation/src/styles/mobile.css) limite l’agrandissement des labels de cases à 767 px, sans équivalent dans `pointer: coarse`. | **Mesures locales seulement rapportées**, cause CSS corroborée statiquement. Clôture et retrait global à remesurer séparément. |

Focus visible, commandes clavier et sélecteurs natifs ont fonctionné dans l’échantillon. Les étapes Chasse conservent leurs noms accessibles en fenêtre étroite. L’ancien chemin annoncé pour le lien d’évitement et le focus incohérent rapporté par l’outil sont des **limites d’instrumentation à reproduire**, sans panne acquise.

## Arbitrages fondés sur les preuves

**Entrée par phase ou par intention.** Les avis divergent surtout sur l’étendue de R01. E02–04 montrent que la phase seule ne répond pas toujours à « voir les chiffres » ou « corriger ce point ». Priorité au lien de tâche et au retour explicite ; défaut par phase/modèle pour l’ouverture ordinaire seulement. Aucun déplacement automatique pendant le travail, aucun accueil supplémentaire obligatoire.

**Suivi et interventions.** E04 confirme un défaut d’orientation sur Juste Prix ; le bilan existe. Il faut d’abord un accès direct à la lecture d’activité. Cela ne prouve pas qu’une file globale manque sur tous les modèles. R04/U07 deviennent une conception conditionnée par l’inventaire des faits actionnables et des projections existantes, sans compteurs frontend tirés d’une page partielle.

**Perte de saisie et reprises.** Le novice demande un test pour U02 ; les lecteurs techniques confirment le branchement manquant. On peut retenir le correctif ciblé, avec reproduction obligatoire avant livraison. La garde observée dans le wizard ne réfute pas cet autre formulaire. R03 conserve également son objectif, sans prétendre avoir reproduit une publication ou une perte systématique à chaque étape.

**Mobile et accessibilité.** Le cas 400 % E06 est un défaut observé et corroboré ; la simple compacité d’un en-tête à 502 px reste une solution à comparer. VP05 ajoute une consultation aux formats téléphones définis, sans valider le parcours mobile complet. Les seuils tablette ne constituent pas un défaut. La cible interne **44 × 44 CSS px** est conservée ; [W3C 2.5.5](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html) est AAA avec exceptions, [2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) AA demande 24 × 24 ou ses exceptions. La hauteur de 20 px seule n’établit donc pas un échec AA ; aucun verdict WCAG global.

**Fin, navigation et premiers accès.** E11 réfute l’absence de guide de fin : raccorder l’existant. « À résoudre » initial et mémoire de rubrique restent des options à tester ; le comportement actuel de première rubrique est spécifié. La connexion et l’invitation n’ont pas été évaluées par les experts, le catalogue aide déjà au choix : U11/U12 ne deviennent pas des échecs novices acquis. Aucun verdict « écarter » n’est forcé : les objectifs utiles sont conservés ou restreints ; les solutions sans preuve restent des essais.

## Verdicts sur les 30 références

Les matrices qualifient les préconisations ; **seuls les items B du backlog constituent des travaux**, sans doublon. Nature : **O** fait TEST observé ; **C** code local ; **RI** mesure/constat seulement rapporté ; **H** hypothèse d’usage ; **P** préférence ; **D** décision acquise. Importance H/M/B : haute/moyenne/basse. Confiance F/M/f : forte/moyenne/faible, distinguant fait et bénéfice. Effort S/M/L : localisé / plusieurs composants et états / producteur serveur et consommateurs, sans estimation de durée ; à confirmer lors du cadrage.

### Parcours et supports

| Réf. / verdict | Écran, preuve observable et conséquence ; nature | Minimum suffisant → backlog | Importance ; confiance | Effort et risques |
| --- | --- | --- | --- | --- |
| **R01 — Modifier** | Entrée/reprise : E02–04/E09, destinations parfois éloignées de l’intention. O+C ; bénéfice H. | Tâche/retour prioritaires, défaut ordinaire par phase et modèle, vues existantes → B04/B05. | H ; faits F, gain M | M ; liens entrants, lecteur, phase changée pendant saisie. |
| **R02 — Conserver** | Préparer/publier : E02–03/E09, contrôles présents mais correction à rechercher. O+C ; coût H. | Blocage compréhensible → correction exacte → contrôle relu ; acteur/attente explicites → B01/B05. | H ; faits F, gain M | M, L si destination structurée nécessaire ; ne pas router un texte libre ni imposer commerces/terrain partout. |
| **R03 — Conserver** | Succès/reprise : E09/E12, suite textuelle et sous-étape locale. C, interaction non reproduite ; gain H. | Bouton de suite après résultat confirmé, étape/contexte valides en URL ou mémoire éphémère → B05. | H ; mécanisme F, gain M | M ; faux succès, URL/focus avant accord de sortie, contexte obsolète. |
| **R04 — Modifier** | Suivi : E04/E11 ; Juste Prix sans chiffres, bilan présent ; besoin d’une file générale H. | Accès aux chiffres d’abord ; inventaire avant projection d’interventions → B04/B12. | H ; cas F, généralisation M | M puis L conditionnel ; faux zéro, double compte, priorité métier locale. |
| **R05 — Modifier** | Clôture/fin/bilan : E11, guide déjà présent ; chaîne complète non jouée. O+C, efficacité H. | Raccorder clôture/tirage au guide/dossier ; tester filtre À résoudre selon intention → B09. | H en fin ; présence F, gain M | M ; étapes inapplicables, dossier masqué, fusion de décisions. |
| **R06 — Conserver** | Tous supports : E06–07, responsive partiel et défaut 400 %. O ; réussite tactile H. | Réussite mobile/clavier/zoom dans chaque lot ; corriger faible hauteur → B02/B13. | H ; constats F, couverture f | M transversal ; ne pas reconstruire viewport/dialogues existants. |
| **R06.1 — Conserver** | Confirmation : E13, label tactile variable ; usage au doigt inconnu. C+RI. | Label activable visant 44 × 44, accord distinct de l’exécution ; remesurer → B08. | H ; cause F, mesures M | S ; cascade CSS, multiline, espacements en paysage. |
| **R06.2 — Modifier** | Accès/hauteur : E04/E06–07 ; détour établi, densité variable. O ; raccourcis H. | Liens précis, menu complet ; zones fixes compactes/défilantes en faible hauteur → B02/B04/B05. | H ; faits F, disposition M | S/M ; contexte perdu ou champ/erreur recouverts. |
| **R06.3 — Vérifier par test** | Tablette/listes : seuils rapportés, aucune panne établie. RI+C ; disposition H/P. | Éprouver largeur utile, portrait/paysage/partage avant fiches ou tableaux → B13. | M ; défaut f, besoin de preuve F | M de recette ; correction à confirmer, régression bureau. |
| **R06.4 — Vérifier par test** | Saisie/clavier système : jamais ouvert ; E06 renforce le risque sans prouver ce cas. H. | Dates, motif, réponse, erreur et confirmation sur appareils → B13. | H ; défaut inconnu | M de recette ; correction à confirmer, sélecteurs natifs et hauteur visible. |
| **R06.5 — Vérifier par test** | Listes au doigt : E01/E07, responsive lisible ; panneau de sélection encombrant observé, gêne H. | Identité/état/action/retour ; essayer panneau compact, préserver sélection active → B13/B14. | M ; occupation F, gain M | S/M selon essais ; densité, mauvaise cible, décision groupée indue. |
| **R06.6 — Vérifier par test** | Réseau/reprise : E12, reçus existants ; suspension réelle non faite. C+RI ; risque H. | Arrière-plan/session/réponse tardive ; relire reçu/droits avant renvoi → B13. | H ; mécanismes F, terrain inconnu | M de recette ; doublon, succès prématuré, cache privé. |

### Constats locaux

| Réf. / verdict | Écran, preuve observable et conséquence ; nature | Minimum suffisant → backlog | Importance ; confiance | Effort et risques |
| --- | --- | --- | --- | --- |
| **U01 — Conserver** | Paramètres génériques : E08, Actualiser ouvre le formulaire ; recherche d’édition H. C. | « Consulter les dates et inscriptions » ; édition selon droit, sans second clic imposé inutile → B11. | H pour repérage ; fait F, gain M | S ; lecture seule, chargement, erreur. |
| **U02 — Conserver** | Paramètres non envoyés : E08, `dirty` sans garde ; perte déduite, non jouée. C. | Brancher garde commune ; reproduire refus/acceptation, historique, commune → B03. | H ; statique F, reproduction restante | S/M ; doubles invites, URL/focus, reçu de commande à préserver. |
| **U03 — Modifier** | Refus : E02/E10, codes bruts ou motif seulement au survol. O+C. | Motif métier visible et associé, acteur, correction si connue ; repli sûr → B01. | H ; faits F, compréhension M | S/M ; ne pas contourner droits ni doubler le guide explicite. |
| **U04 — Conserver** | Clôture de repli : E10 ; capacité suggérée après liste vide/erreur. C ; occurrence H. | Capacité serveur explicite ou état inconnu avec relecture → B06. | H ; branche F, occurrence inconnue | S/M ; conserver clôture anticipée permise et garde finale. |
| **U05 — Modifier** | Fin répartie : E11 ; guide et dossiers existent. O+C ; effort H. | Absorber dans R05, liens/conséquences sans second guide → B09. | H près de clôture ; présence F, gain M | M ; séquence universelle et projections en doublon. |
| **U06 — Vérifier par test** | Groupes : E04/E09, première rubrique spécifiée ; mémoire H/P. | Liens de tâche d’abord, comparer ensuite dernière rubrique/règle actuelle → B14. | M ; comportement F, mémoire f | M ; arrivée surprise, retour obsolète, garde contournée. |
| **U07 — Modifier** | Interventions : E11, métriques génériques repliées ; aucun incident manqué observé. C ; urgence H. | Qualifier action possible/droit/destination, réutiliser alertes → B12. | H si incident ; besoin M | M/L conditionnel ; statistique devenue alerte, doublon ou comptage partiel. |
| **U08 — Modifier** | Fraîcheur : E04/E11, bilan déjà horodaté ; confusion de portée H. O+C. | Ajouter seulement portée/date utiles manquantes, lecture distincte du calcul → B10. | M ; existant F, gain M | S/M ; fausse fraîcheur, formulaire/focus perdus ; aucun polling requis. |
| **U09 — Modifier** | Vocabulaire : E02/E04–05 ; Live, moteur, MVP/poi et actions techniques exposés. O+C ; compréhension H. | Suivi organisateur stable, verbes exacts, termes métier et populations définies → B04/B11. | H sur refus/navigation, M ailleurs ; fait F, mots finaux M | S/M ; ne pas fusionner inscrits/terminés/éligibles/remis ni changer codes d’événements. |
| **U10 — Conserver** | Flyer : E10, navigation annoncée téléchargement. C. | Renommer cette action « Ouvrir le flyer » → B11. | M ; fait F, gain M | S ; garder vrais téléchargements et disponibilité documentaire. |
| **U11 — Vérifier par test** | Connexion/invitation non évaluées par les experts ; constat initial seulement rapporté. RI+H. | Tester invitation valide/expirée et arrivée directe ; aide/affichage mot de passe selon résultat → B15. | M si difficulté confirmée ; traitement différé, confiance f | S/M ; réponses neutres et attribution des droits inchangées. |
| **U12 — Vérifier par test** | Choix modèle : E01/E03, descriptions utiles et dépendances réelles. O ; comparaison enrichie H/P. | Comparatif compact des préparatifs à tester, exemples adaptés ; durée étayée seulement → B16. | M ; acquis F, bénéfice M | S/M d’étude ; surcharge, estimation trompeuse, étapes utiles retirées. |

### Création commune validée et réalisation à vérifier

Source normative : [E73-EVO-CREATION-UX-COMMUNE](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md#règle-du-17-novembre-2026--création-homogène-des-animations). B07 porte exclusivement la création ; les raccordements après création restent dans B05.

| Réf. / verdict | Écran, preuve observable et conséquence ; nature | Minimum suffisant → backlog | Importance ; confiance | Effort et risques |
| --- | --- | --- | --- | --- |
| **CU-01 — Conserver** | Cadre : E01/E12, socle commun local et un sous-ensemble observé. D+O+C ; homogénéité complète inconnue. | Comparer liste/catalogue et chaque modèle, garder cadre/repères communs → B07. | H ; décision F, couverture partielle | S/M ; ne pas reconstruire le layout ni uniformiser les contenus métier. |
| **CU-02 — Conserver** | Actions : E01/E12, requis et garde visibles ; finale non jouée. D+O+C. | Aller/retour avec valeurs ; effets et finale nommés, créer/demander/publier distingués → B07. | H ; décision F, réalisation M | M ; effet implicite, double création, demande prise pour résultat. |
| **CU-03 — Conserver** | Adaptation/revue : cinq étapes sans commerce observées E01 ; correction finale non jouée. D+O+C. | Étapes utiles, données compatibles, Modifier ciblé puis revue, incompatibilités expliquées → B07. | H ; décision F, couverture M | M ; effacement silencieux ou reprise incompatible ; trois dotations à couvrir. |
| **CU-04 — Conserver** | États/refus : E12, protocoles de réconciliation différents. D+C ; panne/doublon non constatés. | Recetter erreurs, droit retiré, conflit et réponse perdue par famille ; suite après fait confirmé → B07. | H ; différence F, risque effectif M | M, L si manque contractuel confirmé ; clé/corps, reçu, faux succès. |
| **CU-05 — Conserver** | Reprise : E01, garde déclenchée, abandon explicite ; refus/commune non éprouvés. D+O+C. | Conserver URL/étape/valeur/focus au refus, invalider contexte, garder commande incertaine → B07. | H ; décision F, couverture partielle | M ; transfert entre communes, droit ancien, promesse après crash. |
| **CU-06 — Conserver** | Supports : E07 ne couvre pas toute la création ; E06 concerne la préparation. D+O partiels. | Comparaison tous modèles, toucher/clavier, 320 px/texte 200 %, rotation et apprentissage transférable → B07/B13. | H ; décision F, réalisation globale inconnue | M de recette, correctifs à confirmer ; champs/erreurs/actions masqués, variantes incohérentes. |

## Backlog unique proposé

**C** : correction justifiée ; **E** : évolution à spécifier ou décision déjà spécifiée à réaliser ; **T** : idée/risque à éprouver avant développement. Ce backlog ne modifie ni la roadmap ni l’adoption des propositions. Les recettes transverses sont regroupées dans B13 et alimentent les items concernés ; elles ne créent pas un second correctif pour le même défaut.

| ID / type | Travail et limite de responsabilité | Traçabilité |
| --- | --- | --- |
| **B01 · C** | Traduire les motifs de publication et expliquer les actions indisponibles à proximité ; réutiliser les contrôles existants. Les destinations de correction sont traitées dans B05. | R02, U03 |
| **B02 · C** | Rétablir une surface de lecture/interaction du guide à fort zoom/faible hauteur ; isoler les couches fixes responsables, préserver focus et contexte. | R06, R06.2 ; vigilance CU-06 |
| **B03 · C** | Raccorder la saisie non envoyée des paramètres à la garde commune, après reproduction ciblée. | U02 |
| **B04 · E** | Faire répondre les accès suivi/résultats à l’intention, d’abord Juste Prix ; accès direct au bilan/activité, défaut ordinaire selon phase/modèle, sans déplacement automatique. | R01, R04, R06.2, U09 |
| **B05 · E** | Raccorder entrée de préparation, contrôle, correction, retour, publication confirmée et suite ; conserver sous-étape/contextes valides. | R01–03, R06.2 |
| **B06 · C** | Corriger la disponibilité de clôture déduite d’une lecture vide/échouée ; conserver capacité explicite et garde finale. | U04 |
| **B07 · E acquise** | Réaliser/vérifier les six CU dans les créations, en réutilisant le socle ; qualifier notamment la réponse perdue de chaque famille. Aucun constat actuel de doublon. | CU-01–06 |
| **B08 · C** | Étendre les zones activables des labels de confirmations tactiles ; remesurer clôture et retrait, sans changer les décisions. | R06.1 |
| **B09 · E** | Raccorder clôture/tirage au guide de fin/dossier/bilan ; comparer À résoudre initial à Tous selon intention. | R05, U05 |
| **B10 · E** | Préciser portée et fraîcheur là où elles manquent, sans nouvelle fréquence d’actualisation ni date inventée. | U08 |
| **B11 · C** | Corriger les verbes d’ouverture dates/flyer et le jargon exposé ; conserver les distinctions de populations et les codes techniques internes. | U01, U09, U10 |
| **B12 · E à qualifier** | Inventorier situations actionnables, alertes existantes, droits et producteurs ; spécifier une synthèse seulement si manque démontré. | R04, U07 |
| **B13 · T/recette** | Plan commun appareils, zoom, clavier, listes, réseau/session et rotation ; analyser chaque défaut constaté dans son item propriétaire. | R06, R06.3–06.6, CU-06 ; non-régression B01–11 |
| **B14 · T** | Comparer retour ciblé et mémoire de groupe ; expérimenter panneau de sélection compact et repères d’étapes, sans changement automatique des conventions. | U06, R06.5 ; complément E01/E07 |
| **B15 · T** | Observer premier accès/invitation valide ou expirée avant d’enrichir l’aide de connexion. | U11 |
| **B16 · T** | Faire choisir un modèle et chronométrer des scénarios préparés ; comparer une aide courte aux préparatifs, segmenter la promesse 5–10 minutes. | U12 ; complément produit, CU comme base de recette |
| **B17 · T** | Cartographier réemploi par modèle/variante/section, expliquer tôt la portée effective, mesurer le travail évité sans élargir les copies autorisées. | Complément E05 ; contexte U12/R05, sans défaut de clonage présumé |

## Les cinq changements prioritaires

L’ordre combine impact sur les tâches centrales et solidité de preuve ; il ne mesure pas un gain utilisateur. B06/B08/B11 peuvent accompagner les lots comme corrections ciblées. La réalisation CU reste acquise et s’applique aux travaux de création ; sa validation n’est pas rouverte par cet ordre.

| Priorité | Bénéfice attendu, distinct du fait | Critère concret de validation |
| --- | --- | --- |
| **1 · B01 — Refus compréhensibles** | E02 prouve les codes bruts ; leur traduction devrait réduire l’hésitation avant publication. Aucun gain de temps mesuré. | Rejouer les deux motifs vus : texte métier, acteur et correction compréhensibles sans survol ; motif inconnu explicite ; aucun droit ajouté. Un organisateur peut dire s’il agit ou attend Pro. |
| **2 · B02 — Lecture à fort zoom** | E06 confirme l’absence de surface utile ; corriger le cumul doit rendre la préparation consultable. | Même guide à 400 % : chaque étape, champ, erreur et commande atteint au défilement/clavier sans recouvrement ; focus visible. Vérifier aussi viewport CSS de référence, 200 %, faible hauteur et formats VP05. |
| **3 · B03 — Protection de la saisie** | E08 prouve le branchement manquant ; éviter la perte silencieuse reste à reproduire puis démontrer. | Données jetables : changer valeur/motif, quitter par rubrique/historique/commune ; refus conserve valeur, URL, rubrique et focus, acceptation abandonne explicitement ; commande incertaine toujours réconciliée. |
| **4 · B04 — Activité et résultats trouvables** | E04 prouve le détour et les chiffres disponibles ; un accès direct devrait répondre à « combien ont participé ? ». | Depuis « Consulter le suivi » du Juste Prix et Résultats en cours, activité/bilan accessible sans recherche dans le sélecteur ; commandes sensibles toujours distinctes. Tester novice, lecteur, lien profond et retour ; ne pas modifier les métriques. |
| **5 · B05 — Préparation et reprise continues** | E02–03/E09 établissent des destinations et états locaux perfectibles ; terminer sans recherche reste une hypothèse d’usage. | Manuel + Chasse : action → manque utile → correction exacte → contrôle relu → publication confirmée → lien explicite de suivi ; reprise Terrain après interruption. Sur banc synthétique autorisé : refus de sortie et réponse perdue sans fausse réussite ni seconde commande. |

## Validation du délai et du réemploi

**B16 doit mesurer créer ET publier**, pas seulement atteindre un brouillon. Fixer départ, rôle, modèle, décisions, dotation, contenus et accords déjà prêts ; nommer l’arrivée : demande acceptée, brouillon créé, publication confirmée ou démarrage. Chronométrer séparément choix, temps actif dans l’outil, préparation hors outil et attente externe. Comparer un modèle simple préparé, un modèle dépendant des commerçants et la Chasse accompagnée. Les accords Pro, le terrain et l’objectif de cinq jours ouvrés affiché ne peuvent être absorbés dans une durée universelle de clics ; ils ne réfutent pas pour autant 5–10 minutes actives sur un cas préparé. Aucun temps réel n’est établi.

**B17 doit vérifier ce que réutiliser économise.** Le Juste Prix observé permet les textes, sans scénario ni visuels réutilisables dans cette source. C’est une limite annoncée, pas une panne prouvée. Vérifier couverture par modèle/variante, éléments évités/revalidés et temps jusqu’à nouvelle publication. Conserver la même commune, source/version, provenance et copie par liste blanche ; jamais participants, accords, gains, QR, paiements ou état exécuté. Le domaine [NouvelleEdition](../../../../localeo-backend/app/domaine/animation_locale/valorisation/regles.py) et le [service d’éditions](../../../../localeo-backend/app/application/animation_locale/services/editions_animation.py) restent propriétaires de ces règles.

**Résultats qui changeraient un arbitrage :** une protection effective retrouvée en reproduction réduirait B03 ; une projection existante complète éviterait tout développement serveur B12. Un essai novice peut départager accès explicite et changement d’arrivée B04, mémoire B14 et comparatif B16. Une incompatibilité de clonage voulue appelle une promesse plus précise, pas une copie forcée ; une variante normalement compatible refusée justifierait un correctif B17. Un dépassement des dix minutes sur cas préparé conduirait à revoir la promesse ou les frictions observées, sans supprimer les prérequis métier.

B13 complète chaque lot : vrais appareils iOS/Android et tablette, portrait/paysage, clavier ouvert/physique, texte agrandi, 320 CSS px, lecteur d’écran ; listes réalistes et retours/filtres/focus ; arrière-plan, verrouillage, session expirée et réponse tardive. Les automatismes synthétiques existants gardent leur valeur pour commandes/droits/reçus, sans valoir essai physique. Avec organisateurs réels novices et habitués, mesurer réussite sans aide, recherche de rubriques, ressaisie, erreurs, compréhension et temps depuis un départ identique ; établir la référence avant tout objectif chiffré.

## Propriétaires et impacts des changements proposés

**Backend** conserve droits, transitions, paramètres modifiables, éligibilités, gains et reçus. La [recommandation de cycle](../../../../localeo-backend/app/domaine/animation_locale/services/recommandation_animation.py) n’autorise aucune commande et n’est pas une file exhaustive d’interventions. Animation présente et orchestre ; ne pas recalculer les décisions depuis des statistiques ou une page partielle. Gardes, versions, idempotence, contexte de commune/session et distinction confirmé/incertain restent indispensables.

Les corrections minimales concernent surtout **Animation**. Motifs/destinations structurés ou agrégation complète pourraient affecter **Backend**, contrats canoniques **Projet**, types embarqués et lecteurs ERP : à établir par B05/B12, sans API nouvelle prescrite ici. **Live/Marketplace, Pro/Commerçant et Coffrets** sont des dépendances métier à préserver ; notification inscrite dans un audit ne prouve pas sa réception, chiffre affiché ne prouve ni chiffre d’affaires ni remise. Toute évolution de leurs conséquences exige une recette de contrat et de comportement dédiée.

Audit documentaire seul : **aucun code, donnée métier, contrat, migration, générateur, configuration ops ou statut de roadmap modifié**, aucun commit, push ou déploiement. L’impact schéma/exploitation sera requalifié si une projection est retenue. Adapter les aides aux comportements livrés. Futures fixtures : arrivée vide, modèles/dotations, attente externe, lecteur, refus, conflit/réponse incertaine, fin à traiter ; aucune génération réelle demandée.

## Annexe de provenance

Notes de travail non versionnées : `localeo-animation/tmp/contre-expertise-20261117/`, comprenant protocole, quatre paires phase A/confrontation, `verification-parent.md` et journal des portes. Les observations sont explicitées ci-dessus ; ces fichiers ne sont pas des dépendances documentaires canoniques.

| Source figée | SHA-256 |
| --- | --- |
| Rapport initial | `F2A3759042B7E5D9666F9F98BA7298701750F17C0AAC105832556589A1DF7E86` |
| UX métier, phase A | `D505A12B5085475677DC09744BB31A254193A3BB8414FCA9271C4A7B6989028B` |
| Organisateur, phase A | `DDA302074C7978382CF6ACB9522931C7CA31EDA8C64CBC40F41F8A5EB9489A66` |
| Accessibilité, phase A | `FB610CB2FA70745AA0836BA89F4DB77E9DC54B55641930A839D7A3950FE48911` |
| Produit/technique, phase A | `0AD1EFC06641F4E32E6D4F8D17F86947A441BE50D47813650BA20D80F3500999` |

Le parent a vérifié les quatre empreintes avant synthèse, puis contrôlé leur conservation après les confrontations. Une coquille d’UUID dans une note aveugle a été identifiée par VP02 ; les routes restent ici paramétrées. Les phases A sont conservées telles que remises.

## Vérifications du livrable

- `py scripts/check_guidance.py --document docs/audits/animation/localeo-animation-contre-expertise-ux-2026-11-17.md --document docs/audits/INDEX.md` : succès, 101 documents contrôlés, 1 407 liens locaux, zéro erreur ou avertissement. Ce contrôle ne vérifie pas les ancres ou la disponibilité des pages externes.
- `py scripts/sync_documentation.py --check-sources` : succès, 151 sources exportées vérifiées. Ce nouvel audit et son entrée d’index ne modifient pas le périmètre des exports.
- `git diff --check` : succès. Contrôle de structure : 30 références distinctes, 17 items de backlog distincts et exactement cinq priorités ; aucune adresse e-mail recopiée.
- Les sept fichiers préexistants ont été comparés à leurs empreintes initiales, en retirant uniquement notre ajout à l’index pour cette comparaison : contenu utilisateur et rapport initial préservés. Les quatre dépôts applicatifs ont gardé leur HEAD initial et ne présentent aucune modification suivie ; seules les notes temporaires ignorées d’Animation ont été ajoutées.

**Dépôt modifié par cette tâche : Projet**, avec ce rapport et son lien dans l’index des audits. Ces contrôles documentaires ne remplacent aucune recette applicative restante ; aucun test applicatif, commit, push ou déploiement n’a été effectué.
