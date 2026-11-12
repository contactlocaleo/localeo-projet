# Localeo Animation — audit UX quotidien et productivité

Audit du **12 novembre 2026**. Périmètre : application de gestion organisateur,
sur ordinateur et mobile. Il complète l’audit ergonomique du 1er novembre ; il
ne concerne pas le carnet habitant de Localeo Live.

## Conclusion et trois priorités

La structure actuelle est exploitable : commune explicite, quatre espaces de
fiche, accès aux archives, messages accompagnés et séparation des décisions de
fin. La priorité est de fiabiliser le travail quotidien dans cette structure.

1. **Une prochaine action fiable partout.** Le tableau de bord recommande
   « Cloturer » alors que la même animation propose « Consulter le live » dans
   la liste et la fiche. La file de travail doit distinguer une action à traiter
   d’une animation simplement en cours de suivi.
2. **Conserver le travail et le point de reprise.** Recherche perdue après une
   fiche, filtres de campagne devenant invisibles, retours en première page
   après traitement et gardes de saisie incomplètes se cumulent dans une session.
3. **Rendre les listes immédiatement utilisables.** Pagination réelle,
   recherche de participant homogène, ouverture clavier et action visible sur
   la carte mobile apporteront davantage qu’une nouvelle refonte graphique.

Les recommandations sont reprises par
[E73-EVO-ANIMATION-PRODUCTIVITE](../../specifications/epic-73-animation-et-ou-coffrets/ux-productivite-organisateur.md),
en sept lots et 22 critères. **Spécifiés, pas implémentés.**

## Méthode et niveau de preuve

- **Interface (I)** : session TEST existante de l’organisation de démonstration
  Association Test Thibaut, commune Bouliac ; navigateur Chrome sur Windows,
  fenêtre bureau de 1 500 px et émulation responsive **390 × 568 pixels CSS**.
  Navigation et recherche uniquement ; formulaire de message ouvert puis quitté
  vide. Aucun envoi, création, clôture, tirage, import ou modification de données.
- **Code (C)** : frontend Animation `89579eb`, backend `fab8850`, documentation
  Projet `1476885` plus modifications locales de clôture automatique préservées.
  Trois explorations indépendantes : navigation, opérations, contrats.
- **Hypothèse (H)** : effet sur le temps de tâche, fréquence des pertes de
  contexte, compréhension utilisateur ; à mesurer, aucun gain chiffré acquis.
- L’adresse observée est `https://test-animations.localeo.city`, qui présente ici
  l’application **de gestion**. Le README local indique aussi
  `test-gestion-animations.localeo.city` pour cette surface : l’identité de
  déploiement et son SHA restent à vérifier. Les observations UI ne certifient
  donc pas le déploiement des commits locaux.
- Captures affichées dans la conversation, sans export contenant des données
  de compte. Les références de composants ci-dessous rendent l’analyse
  reproductible. Aucun scénario d’écriture ni test de charge exécuté.

## Parcours couverts et limites

| Parcours / public | Vérifié | Limite explicite |
| --- | --- | --- |
| Responsable ou gestionnaire : décider quoi faire à l’arrivée | I+C : dashboard, liste et prochaine action sur animation publiée et clôturée | Pas de comparaison de sessions avec permissions différentes |
| Retrouver une animation, ouvrir sa fiche, revenir | I+C : recherche exacte « Test animation Thibaut », un résultat, ouverture puis retour à quatre résultats et champ vide | Page profonde et archives : code seulement |
| Créer une animation depuis un modèle | C : sélection initiale, huit étapes manuelles, dates, confirmation, sorties | Aucun brouillon créé ; variantes Chasse/Léo à recetter séparément |
| Inviter les commerçants, assister un participant, corriger une validation | C : sélection, listes locales/globales, tombola publique, aperçu de correction | Aucun envoi, accès à des coordonnées réelles ou correction effectués |
| Communiquer et diffuser | I+C : Liens/QR vide, historique des messages vide, création de brouillon non enregistrée ; étapes et quotas lisibles | Aperçu d’audience, envoi immédiat/différé, erreur fournisseur et retour filtré : code seulement |
| Traiter les gains et finir une animation | I+C : Fin et archivage d’une animation clôturée, dossier remis et unités sans gagnant justifiées | Commandes de remise/fin/archivage non exécutées ; continuité page 3 : code seulement |
| Comparer les résultats | C : choix d’édition et pagination du bilan | Pas de PDF produit ni de comparaison distante exécutée |
| Usage mobile et accessibilité | I : liste, carte, fiche, menu de rubrique et formulaire de message à 390 × 568 ; C : sémantique clavier/dialogues | Téléphone physique, 320 px, zoom 200 %, lecteur d’écran et mesure de contraste à recetter |
| Gestion organisation / abonnement / finance / import | Cartographie et points d’entrée identifiés dans le code | Parcours secondaires non recettés ; aucun achat ni import ; pas de conclusion de conformité globale |

Responsable, gestionnaire et lecteur sont ceux des
[périmètres SaaS](../../specifications/epic-73-animation-et-ou-coffrets/perimetres-parcours-saas.md).
L’interface auditée ne permet pas d’attester tous leurs refus. Les commerçants
et habitants sont des destinataires de certaines actions, pas les opérateurs
de cette application.

## Constats et corrections proposées

Priorité P1 : fiabilité/efficacité quotidienne ou accès essentiel ; P2 : réduction
des gestes et lisibilité. Effort S : localisé, M : plusieurs composants,
L : producteur/consommateur et preuves de volume. Ce sont des estimations relatives.

### A01 — Prochaine action contradictoire et file de travail non sélective

**P1 · I+C · confiance forte · effort M/L.** Responsable/gestionnaire, dashboard,
liste et fiche. Ouvrir le dashboard Bouliac puis la liste : « Tombolat des
commercants de Noel », publiée du 14 au 15 novembre, propose « Cloturer » au
premier endroit et « Consulter le live » aux autres. Le dashboard et la liste
présentent les mêmes quatre animations ; ce petit échantillon ne prouve pas seul
le défaut de sélection. Le code le confirme :
[pilotage_animation.py](../../../../localeo-backend/app/application/animation_locale/services/pilotage_animation.py),
lignes 111–129 et 161–176, remplit `animations_a_action` avec toutes les retenues
et propose CLOTURER pour PUBLIEE/EN_COURS.
[App.tsx](../../../../localeo-animation/src/app/App.tsx), lignes 611, 1225 et 2045,
emploie deux transformations différentes.

**Effet possible :** hésitation, ouverture du mauvais espace, incitation à
clôturer prématurément. **Cible :** projection serveur commune, motif et cible
cohérents ; bloc « À traiter » séparé du suivi. La clôture anticipée reste une
action autorisée selon les règles existantes, pas une recommandation automatique.
**Acceptation :** même libellé/cible dans les trois vues à faits égaux ; aucun
clic de navigation ne clôture ; une animation à suivre sans tâche n’est pas
présentée comme un travail en attente. AP-01/02.

### A02 — Une sortie peut perdre une saisie

**P1 · C · confiance forte · effort M.** Gestionnaire, création/configuration et
changement de commune. Saisir puis utiliser menu, Retour navigateur ou commune.
`App.tsx:1063, 2886, 4004, 4754, 4809, 4815` : le menu appelle une garde, le retour
navigateur et le changement de commune suivent d’autres chemins ; certains
formulaires ne déclarent pas leur état modifié. Le changement de tenant remonte
la vue et détruit son état local.

**Effet :** ressaisie ou erreur de contexte. **Cible :** même garde sur toutes les
sorties, « Continuer la saisie » / « Quitter sans enregistrer ». **Acceptation :**
refuser conserve URL, commune, formulaire et focus ; accepter abandonne
explicitement sans transférer la saisie dans une autre commune. Les réponses de
l’ancien tenant restent invalidées. Pas de sauvegarde implicite. AP-03/04.

### A03 — Les retours perdent ou dissimulent les filtres

**P1 · I+C · confiance forte · effort M.** Gestionnaire/lecteur. Recherche exacte
dans Animations → fiche → bouton Animations : retour reproduit avec champ vide
et quatre résultats. `App.tsx:1380, 1390, 4705, 4874` ;
[AnimationArchives.tsx](../../../../localeo-animation/src/app/components/AnimationArchives.tsx):11.
Dans [OrganizerCampaignsWorkspace.tsx](../../../../localeo-animation/src/app/components/OrganizerCampaignsWorkspace.tsx):30–59,
filtrer → campagne → retour réinitialise les champs du formulaire alors que la
requête garde ses filtres. Ce second cas est établi par le code, non reproduit
avec l’historique vide observé.

**Effet :** travail répété, liste filtrée prise pour la liste complète.
**Cible :** contexte de consultation restauré, filtres appliqués toujours visibles,
retour nommé « Retour aux animations » ou « Retour aux messages ».
**Acceptation :** filtre/page/repère/focus concordent après retour ; changement
de commune ou de droits purge ce contexte. AP-05/06.

### A04 — Chargement, panne et absence de données se confondent

**P1 · I transitoire+C · confiance forte · effort M.** Tous rôles. Au chargement du
dashboard, la phrase « Aucune animation nécessitant une action ou données
indisponibles » apparaît avant les lignes ; ne pas la confondre avec une panne
persistante. `App.tsx:983, 1085, 1302, 2796, 4025` ignore certaines erreurs et peut
présenter un catalogue vide ou un abonnement « Inactif » faute de réponse.

**Effet :** diagnostic erroné et actualisations répétées. **Cible :** emplacement
stable, états chargement/vide/refus/erreur distincts et « Réessayer » local.
**Acceptation :** panne de modèle ≠ aucun modèle ; abonnement inconnu ≠ inactif ;
reprise sans perdre les filtres ni rejouer une commande. AP-07.

### A05 — Plusieurs listes récupèrent toutes les pages avant de servir la première

**P1 · C · confiance forte sur la structure · effort L.** Listes Animations,
participants non publics et validations locales. Ouvrir une animation fortement
peuplée : `api.ts:824, 1080, 1213, 1221`, `App.tsx:1404, 2581, 2590, 2704` et
[ProofCorrections.tsx](../../../../localeo-animation/src/app/components/ProofCorrections.tsx):28–53
collectent les pages avant filtrage/rendu local. Dix lignes visibles ne prouvent
pas dix lignes chargées. Aucun ralentissement N/10N mesuré dans cet audit.

**Effet attendu :** délai et mémoire augmentent avec l’historique. **Cible :** une
page serveur, filtres indexés, retour précédent explicite, export exhaustif séparé.
**Acceptation :** une ouverture ne demande pas les pages suivantes ; même borne
à N/10N ; compteurs globaux distincts des lignes visibles. La suppression groupée
ne vise jamais silencieusement les brouillons non affichés. AP-08/09/10/22.

### A06 — Ouverture bureau inaccessible au clavier et focus des confirmations incomplet

**P1 · C + arbre accessible observé · confiance forte · effort S/M.** Liste
Animations : nom simple et `<tr onClick>` (`App.tsx:1588`), sans lien/bouton
d’ouverture sur bureau, contrairement au mobile.
[ResponsiveTable.tsx](../../../../localeo-animation/src/app/components/ResponsiveTable.tsx):34,74.
Création/annulation et suppression de participants : fenêtres en `div` sans
primitive de dialogue (`App.tsx:1928, 2754, 4247`) ; libellés du wizard non reliés
aux champs (`4370` et suivants).

**Cible :** lien de nom, champs associés et `ManagementDialog` existant.
**Acceptation :** ouverture par Tab/Entrée, nom accessible, focus contenu puis
retour au déclencheur, Échap lorsque permis, conséquences et blocages conservés.
Parcours clavier complet à exécuter avant livraison. AP-11/12.

### A07 — Création longue et erreurs de calendrier détectées tard

**P2 · C · confiance forte · effort M.** Créer depuis une carte Modèles passe encore
par le choix de modèle ; une étape entière présente la commune déjà active.
`App.tsx:4007, 4064, 4101, 4345` : huit étapes et contrôle des dates limité à leur
présence avant Continuer. Fin antérieure au début remonte tard au serveur.

**Cible :** accès aux informations depuis le modèle choisi, modèle modifiable,
commune dans le contexte et le récapitulatif ; erreur à proximité de la date.
**Acceptation :** aucun choix déjà connu à ressaisir ; période invalide signalée
avant de continuer ; saisie conservée après refus serveur. Ne pas modifier les
préconditions de publication ni imposer ce wizard à Chasse/Léo. AP-13/14.

### A08 — Recherche de participant différente selon le moteur

**P1 · C · confiance forte · effort M.** Support/gestionnaire : Participants →
recherche → sélection d’une tombola publique. Le lecteur spécialisé remplace la
recherche par état et pagination seulement :
[GlobalReadWorkspace.tsx](../../../../localeo-animation/src/app/components/GlobalReadWorkspace.tsx):21–45,
[PublicTombolaParticipants.tsx](../../../../localeo-animation/src/app/components/PublicTombolaParticipants.tsx):38–42.

**Cible :** recherche serveur par coordonnées déjà autorisées ou référence,
portée explicitement annoncée. **Acceptation :** retrouver un participant situé
au-delà de la première page sans les parcourir ; pas de filtre limité à 25 lignes
ni de nouvelle exposition de coordonnées. AP-10/15.

### A09 — L’aperçu de correction est éloigné de l’action

**P1 · C · confiance forte sur le DOM · effort S/M.** Gestionnaire : Examiner une
correction dans une longue liste. `ProofCorrections.tsx:34–55` ajoute le formulaire
après toutes les lignes, sans progression de focus.

**Cible :** détail adjacent ou panneau explicitement focalisé ; retour au repère.
**Acceptation :** conséquences visibles et accessibles directement à 320 px et au
clavier, sans parcourir les autres lignes ; ouverture/annulation sans correction,
motif/confirmation/version/reçu inchangés. AP-16.

### A10 — Un détour de filtre peut élargir la portée d’une invitation

**P1 · C · confiance forte · effort S/M.** Gestionnaire : sélectionner A à envoyer →
filtrer En attente → revenir. La sélection est purgée et l’absence de sélection
fait proposer « Tout envoyer ». Le libellé change effectivement ; aucun envoi
silencieux n’est démontré. Sources :
[MerchantParticipationTab.tsx](../../../../localeo-animation/src/app/components/MerchantParticipationTab.tsx):89,134,168,219 ;
[HuntInvitations.tsx](../../../../localeo-animation/src/app/components/HuntInvitations.tsx):32–53
exige déjà une sélection explicite.

**Cible :** « Envoyer la sélection (n) », désactivé à zéro, sélection de page
explicite et annonce de son retrait. **Acceptation :** consulter un filtre ne
permet pas d’envoyer A+B sans sélection de B ; droits/relance côté domaine.
AP-17. Même règle de portée pour la suppression de brouillons (AP-09).

### A11 — Traiter une série de gains ou de dossiers impose de repartir au début

**P1 · C et vue Fin en I · confiance forte · effort M/L.** Gestionnaire : page 3 →
gain → contact/remise → retour. `onChanged` recharge la première page ; seuls
Suivants/Premiers existent dans
[ExternalPrizesWorkspace.tsx](../../../../localeo-animation/src/app/components/ExternalPrizesWorkspace.tsx):72,115,127.
Toute décision de fin réinitialise aussi les curseurs :
[FinAnimationWorkspace.tsx](../../../../localeo-animation/src/app/components/FinAnimationWorkspace.tsx):41–74.
Pas de filtre serveur « À résoudre ». En UI : zéro dossier à résoudre et quatre
unités sans gagnant déjà justifiées ; le nombre de lots sans gagnant n’est donc
pas un nombre de tâches restantes.

**Cible :** précédent, reprise après résultat confirmé, filtre de dossiers à
résoudre et accès ciblé depuis un gain lorsque applicable. **Acceptation :** traiter
le rang 63 n’impose pas de relire les pages 1/2 ; expliquer un curseur devenu
invalide ; compteurs globaux, versions et décision Terminer restent serveur ;
ne pas présenter les unités justifiées comme bloquantes. AP-18/19/20.

### A12 — Les éditions sont difficiles à distinguer dans la comparaison

**P2 · C · confiance forte · effort M.** Responsable : Bilan → Comparer → chercher
l’édition précédente. Le sélecteur présente titre/commune, sans période/moteur,
et perd la sélection quand la page change :
[AnimationResultsWorkspace.tsx](../../../../localeo-animation/src/app/components/AnimationResultsWorkspace.tsx):36–40.
Les mesures et filtres date/modèle nécessaires existent déjà.

**Cible :** titre, période et moteur dans les candidats, filtres bornés et choix
conservé. **Acceptation :** deux éditions homonymes distinguables avant sélection ;
navigation dans les candidats sans remplacement silencieux du choix ; refus de
comparabilité expliqué depuis le serveur. AP-21.

### A13 — Le mobile privilégie le cadre au détriment de l’action

**P2 · I+C · confiance forte sur 390 × 568, effet à tester · effort M.** La marque,
les commandes et la commune forment trois rangées fixes. Dans la fiche observée,
le premier écran est absorbé par ce cadre, titre/statut/action et sélecteur de
rubrique. Dans la carte, « Action suivante » se retrouve dans « Voir les détails »
et seul « Ouvrir » est immédiatement présenté. `ResponsiveTable.tsx:53–60`
choisit génériquement deux champs, sans priorité explicite pour l’action suivante.
Le guide de communication en quatre tuiles précède aussi la saisie sur petit écran.

**Cible :** cadre compact à deux rangées lorsque possible, action métier explicite
sur la carte, progression compacte et aide dépliable. Conserver les textes de
conséquence indispensables. **Acceptation :** prochaine action disponible sans
déplier la carte ; après ouverture d’un formulaire, titre/étape et premier champ
atteignables sans traverser une longue introduction ; focus non masqué par les
barres fixes, 320 px/200 % sans troncature fonctionnelle. AP-12/14.

## Deux avant/après concrets

| Situation | Avant observé | Après proposé : libellé et emplacement |
| --- | --- | --- |
| Animation publiée, avant fin effective, sans tâche à traiter | Dashboard : bouton « Cloturer » ; liste/fiche : « Consulter le live » | Dans « Animations en cours et à venir », bouton **« Consulter le suivi »** sur la ligne et la carte ; même libellé en tête de fiche. Dans « À traiter », seules les recommandations nécessitant une intervention. Clôture anticipée dans les actions secondaires autorisées, avec confirmation existante. |
| Recherche puis consultation de plusieurs animations | Recherche → une ligne → fiche → « Animations » → champ vide, quatre lignes | En tête de fiche **« Retour aux animations »**. Au retour : recherche conservée, **« 1 résultat pour “Test animation Thibaut” »**, focus sur le nom ouvert. **« Effacer les filtres »** à côté du résumé ; aucun effacement lié à l’ouverture d’une fiche. |

## Iconographie et présentation à conserver ou ajuster

La base de pictogrammes avec libellés est cohérente. Remplacer les mots utiles
par des icônes seules réduirait la compréhension ; l’optimisation porte sur la
hiérarchie, le nombre de répétitions et la sémantique de l’action.

| Usage | Constat | Proposition |
| --- | --- | --- |
| Navigation Préparer/Piloter/Communiquer/Résultats | Groupes et pictogrammes déjà partagés | Conserver ; même icône dans titre et entrée, nom accessible visible |
| Flèche de fin de ligne Animations | Repère graphique sans action clavier propre sur bureau | Nom lié + flèche décorative ; CTA métier explicite sur mobile |
| Barre « 2/6 · Publication » | Indique une phase, pas un travail restant | Garder texte de phase ; ne pas la substituer au motif de la prochaine action |
| Vérification / attente / erreur | Certains états partagent un texte ambigu | Pictogramme existant + libellé distinct ; couleur jamais seule |
| Communication, quatre étapes | Explication utile mais volumineuse sur mobile | Étape courante compacte, autres étapes accessibles ; aides secondaires repliables |
| Fin d’animation | « Lots sans gagnant » peut être lu comme une anomalie malgré justification | Afficher état **« Justifiés »** ou **« À justifier »** depuis la projection serveur, à côté du compteur concerné |

## Mesure de départ et validation utilisateur

Aucune donnée de télémétrie produit n’a été consultée. Les KPI d’animations et les
rapports de messages mesurent l’activité métier, pas le temps perdu dans les
retours et recherches. Les quatre animations observées ne forment pas une
mesure de performance.

Avant puis après chaque lot, faire réaliser à 5–6 organisateurs (responsables et
gestionnaires, dont usage mobile) les mêmes tâches sur données synthétiques :
retrouver une édition ; consulter trois fiches et revenir ; créer un brouillon
avec une date erronée puis corriger ; retrouver un participant hors page 1 ;
examiner une correction ; préparer un message sans l’envoyer ; traiter trois
dossiers tardifs ; comparer deux éditions homonymes. Un lecteur teste les refus.

Mesurer par tâche : réussite sans aide / tentatives commencées, temps médian et
p90 jusqu’au résultat vérifié, nombre de retours/recherches répétés, erreurs et
abandons. Une ouverture de page ne vaut pas réussite. Pour la continuité :
**retours avec filtres/page/repère conservés / retours vers une liste précédemment
contextualisée**. Pour les commandes : séparer reçu confirmé, en cours, refusé
et inconnu ; ne pas déduire la réception Push de la publication Live.

Mesures techniques prévues : N/10N, première page/page profonde, nombre de
requêtes, racines hydratées, octets, p95/p99 et mémoire. Tests isolés, aucune
charge sur TEST partagé. Instrumentation éventuelle agrégée, sans nom de
participant, contenu de message, adresse ou recherche saisie. Les seuils de
livraison et les critères observables sont définis dans la spécification liée.

## À préserver et suite

Conserver la commune visible, les quatre espaces, les listes globales déjà
paginées, les détails de participation à la demande, les filtres repliables,
les reçus et confirmations, les quotas/droits séparés, les états Live/Push,
la copie de lien avec secours manuel, les archives en lecture seule et la
séparation Clôturer/Terminer/Archiver. La clôture automatique reste une évolution
distincte déjà spécifiée, pas une fonctionnalité réputée disponible.

Les sept lots couvrent A01–A13. L’implémentation devra produire les tests annoncés,
les contrats générés et la recette des rôles/volumes non vérifiés ici. Cet audit
ne certifie ni la délivrance des messages, ni les transitions distantes, ni
l’accessibilité complète de l’application.
