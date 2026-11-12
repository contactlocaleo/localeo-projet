# Localeo CRM — audit UX et productivité — 12 novembre 2026

Audit demandé avec évolution et spécification de l’epic 71. Application en lecture
seule ; aucune donnée créée, aucun import lancé, aucun message envoyé. La cible
est décrite dans [E71-EVOL-10](../../specifications/epic-71-crm-prospection/ux-productivite.md).
Les recommandations ci-dessous ne sont pas des fonctionnalités livrées.

## Conclusion et trois priorités

Le CRM dispose des fonctions nécessaires, mais la continuité entre elles demande
trop d’effort. Le principal gain attendu vient d’une boucle courte : **trouver
qui contacter → contacter → consigner → préparer la suite → reprendre sa liste**.

1. **Conserver le contexte de travail.** Une recherche filtrée disparaît au retour
   d’une fiche ; les retours de rappels ne suivent pas l’origine. Corriger cela
   avant d’ajouter des raccourcis ou des tableaux de bord.
2. **Mettre le contact et la prochaine action en tête de fiche.** La qualification
   et les historiques repoussent les coordonnées ; les lignes « rappel » et
   « DEVIS » ne disent pas quel prospect elles concernent.
3. **Faire d’Aujourd’hui une file de travail.** Afficher d’abord les actions à
   traiter, avec un périmètre personnel/équipe explicite ; conserver les indicateurs
   de portefeuille dans une zone secondaire.

Les bénéfices de temps sont des hypothèses à mesurer. Aucun pourcentage de gain
de productivité n’a été mesuré lors de cet audit.

## Méthode et couverture

- TEST : `https://test-crm.localeo.city/internal/crm/`, Chrome, session interne
  existante de type administrateur ; ordinateur puis émulation mobile 320 et
  390 × 568. Le jeu présent comporte 1 558 prospects, un dossier et une tâche ;
  sa représentativité commerciale n’est pas établie. Aucune modification de ce jeu.
- Code backend examiné : base Git `25224e0`. Documentation : base `f8923a7`,
  avec modifications locales antérieures conservées, notamment migrations TEST
  v311/v312 et évolution de clôture automatique E73.
- Deux explorations indépendantes en lecture seule : quotidien/contacts/suivi,
  puis agenda/qualification/import/carte. Références de fichiers ci-dessous.
- **V** : reproduit visuellement sur TEST ; **C** : relevé dans le code ;
  **H** : effet ou scénario à confirmer avec des utilisateurs/données adaptées.
  Les captures sont celles de la session d’audit dans la conversation ; aucun
  fichier PNG contenant des données du portefeuille n’est ajouté au dépôt.

| Parcours | Observation et limite |
| --- | --- |
| Arrivée → Aujourd’hui → rappel → prospect | V : cinq indicateurs avant la liste ; rappel sans prospect ; retour « Rappels » depuis Aujourd’hui. Pas de réalisation/report d’action exécuté. |
| Prospects → recherche → fiche → retour | V : recherche « Léognan », deux résultats ; ouverture de la commune puis « ← Prospects » : champ vidé, retour à 1 558 résultats. Pagination avancée et retour navigateur : C. |
| Fiche → contact → noter un échange | V : contacts après qualification/dossiers/actions/historique ; formulaire ouvert sans saisir/enregistrer. C : dépendance des chargements et absence de proposition de suite après succès. |
| Suivi → dossier → rattachement/gain | V : ligne « DEVIS » sans nom de prospect. Détail interrompu par « Accès à vérifier ». Rattachement/gain : C uniquement, aucune transition tentée. |
| Agenda → choix de créneau → report/compte rendu | V : agenda vide sur la semaine du 9 au 15 novembre, bureau/mobile. Création, validation, report, concurrence et compte rendu : C ; aucune réservation créée. |
| Import → examen → progression → bilan | C uniquement ; aucun fichier déposé ni lot confirmé. |
| Actualisation → adoption → calcul de priorité | C uniquement ; aucun fournisseur interrogé, aucune donnée adoptée ni priorité recalculée. |
| Cartes générale et de qualification | C uniquement : deux rendus et transfert partiel des filtres. Pas de mesure visuelle des marqueurs sur TEST. |
| Navigation mobile et réglages | V : rail inférieur à défilement horizontal ; filtre Prospects occupe le premier écran ; menu d’en-tête = applications, pas destinations CRM. Préférences/Imports accessibles indirectement depuis Aujourd’hui. |
| Accès et réseau | V : interruption d’accès sur détail du dossier. C : gestion 401/403, erreurs et idempotence. Pas d’injection de panne, révocation, notification réelle ni test hors ligne sur TEST. |

L’administrateur n’est pas un substitut à la recette avec un commercial nominatif.
Les observations ne valident ni l’accessibilité complète, ni les appareils physiques,
ni les performances sous charge. Une attente de chargement a été perçue, sans
mesure permettant de conclure à un problème réseau/serveur.

## Constats exploitables

Priorités : **P1** gêne directe d’une opération quotidienne ou risque de mauvaise
cible ; **P2** amélioration de fluidité. Effort relatif : **S** localisé, **M**
plusieurs écrans/lectures, **L** transverse. Il ne s’agit pas d’un chiffrage engagé.
Confiance = solidité du constat ; la fréquence et le gain restent à mesurer.

| ID / classement | Écran, rôle, reproduction et preuve | Effet possible et correction | Acceptation observable |
| --- | --- | --- | --- |
| UX-01 · P1 · élevée · M | Commercial, recherche → fiche → retour : perte reproduite V ci-dessus. C : `crm.js:277–346,486,547,571`, curseur local et retours fixes. | Refaire sa sélection à chaque appel. Conserver filtres, page, élément, position, vue et origine ; nommer le retour selon l’entrée. | Recherche de trois pages : retour de fiche **et** navigateur restaurent le contexte ; depuis Aujourd’hui, retour à Aujourd’hui. Contexte invalide expliqué, accès toujours recontrôlé. |
| UX-02 · P1 · élevée · M | Commercial au téléphone, fiche prospect. V : coordonnées trop bas ; C : `crm.js:494–510`, lectures dossiers/tâches/événements successives avant contacts. | Retard pour trouver l’interlocuteur, une panne de section peut bloquer le reste. Synthèse contact/dernier échange/prochaine action en tête ; sections indépendantes, chargement stable et réessai local. | Sans parcourir l’historique, on trouve le contact et l’action suivante. Échec dossiers simulé : contacts consultables ; aucun déplacement du bouton en cours d’utilisation. |
| UX-03 · P1 · élevée sur code · M | Commercial/responsable, Aujourd’hui. V : indicateurs collectifs en premier dans la session ADMIN. C : `crm.js:446`, liste personnelle pour utilisateur nominatif mais lien du compteur retard collectif. | Périmètre ambigu, priorité du jour peu visible. « Mes actions / Équipe », retard/jour/à venir ; compteurs et destinations de même portée ; indicateurs secondaires. | Avec deux collaborateurs et des retards distincts, chaque compteur correspond à sa liste. L’ADMIN sans identité nominative voit « Équipe », pas une fausse vue personnelle. |
| UX-04 · P1 · élevée · M | Commercial/responsable, Rappels/Suivi. V : « rappel » et « DEVIS » sans prospect. C : `crm.js:455–459,355`, API `prospection_api.py:203` supporte `q` absent de Suivi. | Ouvrir plusieurs fiches pour retrouver la bonne. Afficher prospect/commune, action ou dossier, responsable et échéance ; recherche Suivi côté serveur ; noms lisibles dans l’historique au lieu des UUID vus sur TEST. | Trois dossiers homonymes sont distinguables sans ouverture ; recherche sur tout le résultat paginé ; auteur supprimé rendu « Compte indisponible », sans identité inventée. |
| UX-05 · P2 · élevée sur code · S/M | Commercial, enregistrer échange/terminer action. Formulaire vu V ; succès C seulement : `crm.js:235–238,524,574–585`. | Retour sans prochaine étape. Confirmation contextualisée et proposition facultative « Planifier la prochaine action », prospect/dossier préremplis. | Appel enregistré une fois ; la proposition ouvre la bonne cible ; fermer ne crée rien ; résultat réseau incertain ne propose pas une suite comme si l’appel était confirmé. |
| UX-06 · P1 · élevée sur code · M | Gestionnaire, rattachement puis gain. C : `crm.js:559–570`, saisie d’identifiants ; API de recherche et liens déjà présentes `prospection_api.py:281–296`. Parcours visuel arrêté avant ce point. | Copier des UUID entre ERP et CRM, erreur de preuve possible. Recherche lisible de référence autorisée, affichage des liens, choix d’une preuve rattachée éligible. | Rattacher puis constater un gain sans copier d’UUID ; preuve expirée/non éligible/déjà attribuée refusée sans transition partielle. |
| UX-07 · P1 conditionnel · élevée sur code · M | Commercial, planification ou opposition sur contact n°26. C : `crm.js:538,545`, seule première page consommée ; API contacts limitée à 25 par défaut. | Mauvaise cible ou impossibilité de traiter un contact. Sélecteur paginé, chargement suivant explicite et sélection conservée ; recherche seulement si exécutée sur l’ensemble côté serveur. | Contact de seconde page sélectionnable dans les deux formulaires ; aucune bascule implicite vers la structure ; refus si cible devenue interdite. |
| UX-08 · P2 · élevée · M | Tous rôles, Prospects/navigation mobile. V : filtres avant tout résultat, rail horizontal, menu Applications ne remplace pas un menu CRM. C : `crm.js:106`, `crm.css:1,17`. | Beaucoup de défilement pour des actions répétées. Recherche visible, bouton « Filtres (n) », résumé des filtres actifs, cinq entrées fixes dont « Plus ». | À 320/390 px, accès direct aux destinations quotidiennes sans défilement horizontal ; Imports/Préférences retrouvables dans Plus ; filtres appliqués restent lisibles. Texte 200 %, clavier et focus à vérifier. |
| UX-09 · P1 · élevée sur code · M | Commercial, semaine/collaborateur → RDV → retour puis report. C : `crm-agenda.js:31,39–40,105–107,244,270–272` ; disponibilités assistées à la création seulement. | Perte de planning et ressaisie de trois dates. Conserver le contexte, raccourci « Aujourd’hui », sélecteur de créneaux tenant compte du RDV déplacé, raccourcis de date du rappel. | Revenir à la semaine/au collaborateur ; reporter avec durée et ancien créneau visibles ; conflit conserve le brouillon ; validation réservée au collaborateur et défaut du rappel inchangé. |
| UX-10 · P1 sur agenda chargé · élevée sur code · M | Équipe, 60 RDV sur une semaine. C : `crm-agenda.js:79,89–96`, sept jours construits depuis une page globale de 25 ; vide d’une journée déjà qualifié « sur cette page », vide global qualifié « sur cette période ». TEST semaine vide seulement. | Prendre une vue partielle pour une disponibilité. Annoncer le résultat partiel, accès à chaque journée ; distinguer page vide et période réellement vide. | Aucun jour déclaré libre depuis une page partielle ; 60 RDV accessibles avec pagination serveur, sans télécharger toute l’année. |
| UX-11 · P1 · élevée sur code · M | Importateur, après confirmation. C : `crm.js:737,764–769`, états traduits mais progression détaillée sur lecture unique ; UUID/version de plan en tête. | « 0 / N » peut ressembler à un blocage ; rechargements répétés. Étapes explicites, compteurs, progression lue automatiquement, dernier état et réessai conservés. | Sans recharge manuelle : analyse → examen → confirmation → attente/import → bilan. « En attente de traitement » distingué d’« En cours » ; une erreur de lecture ne relance pas l’import. |
| UX-12 · P2 · élevée sur code · M | Gestionnaire, 60 propositions d’actualisation. C : `crm-actualisations.js:56,66,93–95` : choix par page, avertissement d’abandon présent, peu d’aide à la suite ; `crm.js:864–865` : confirmation ailleurs. | Relectures et arrêt avant adoption complète. « X choix sur cette page », appliquer puis continuer, précédente, liens vers les brouillons précis à confirmer. | Aucune perte silencieuse de choix ; retour à la page précédente ; confirmation de preuve, choix de référence et calcul restent séparés. |
| UX-13 · P1 · élevée sur code · M/L | Gestionnaire, preuve ajoutée → priorité à recalculer. C : `crm-priorite.js:76–101,124,169,183–184`, absence de suite ciblée et identifiants/faits techniques. | Calcul trop large par facilité et difficulté à corriger les refus. « Recalculer ce prospect », préparation limitée à son ID, noms/motifs métier dans le bilan. | Périmètre « 1 prospect » confirmé avant lancement ; seul cet ID traité ; priorité manuelle du dossier inchangée ; preuve importée jamais assimilée à une preuve vérifiée. |
| UX-14 · P2 · élevée sur code · M | Commercial/qualificateur, Carte ↔ Qualification. C : `crm.js:600–697` vs `crm-priorite.js:203–229` ; deux rendus, marqueurs 44 vs 28 px ; passage général→qualification conserve seulement le département. | Deux apprentissages et filtres perdus. Réutiliser comportement/composant accessible de carte, adapter les données et annoncer les filtres non transférables. | Même sélection compatible = même répartition ; profil Commune/EPCI et axe conservés ; liste de secours et accès tactile/clavier partout. |

### Interruption d’accès à diagnostiquer — UX-15

**P1, symptôme certain ; cause indéterminée ; effort non chiffrable avant diagnostic.**
Depuis Suivi sur TEST, cliquer sur le dossier visible « DEVIS » affiche « Accès à
vérifier — Votre session ou vos habilitations ont changé. Se reconnecter ».
La liste était lisible juste avant. L’interface mappe des HTTP 401/403 vers ce
message (`crm.js:71–74`) ; les routes liste/détail demandent la même capacité
`crm.consulter` (`prospection_api.py:202–207`). Aucune preuve ne permet d’affirmer
qu’il s’agit d’une permission manquante, d’une expiration ou d’un défaut métier.

Reproduire avec un compte nominatif de démonstration, relever **l’appel exact**
en échec et sa référence technique, distinguer 401 reconnexion / 403 accès refusé
sans boucle. Vérifier que le retour reste utilisable et que les données privées
sont retirées après révocation. Ne pas contourner le contrôle pour fluidifier
le parcours. CA-19 existant ; cette limite empêche de valider le gain en situation.

## Deux avant/après concrets

**Retour après recherche, en haut de la fiche**

- Avant : « ← Prospects » ; repart sur toute la liste.
- Après : **« ← Résultats de recherche »** ; reprend filtres, page et fiche
  sélectionnée. Depuis une action du jour : **« ← Aujourd’hui »**. Un accès
  direct garde un retour simple « ← Prospects ».

**Préparer un appel, dans le premier bloc de la fiche**

- Avant : affectation, grandes sections de qualification puis dossiers/actions/
  historique ; coordonnées plus loin.
- Après : nom du prospect, commune et responsable ; **« Prochaine action »**
  avec date et libellé ; contact nommé et téléphone ; actions **« Appeler »**,
  **« Noter un échange »**, **« Planifier »**. Après succès : **« Appel enregistré »**
  puis **« Planifier la prochaine action »**. En l’absence de contact :
  **« Aucun contact renseigné » / « Ajouter un contact »** selon les droits.

## Navigation, iconographie et états

Réutiliser les SVG et composants du CRM ; une icône ne remplace pas le libellé
d’une opération importante. La priorité est le sens et la constance, pas le décor.

| Usage | Problème / preuve | Proposition |
| --- | --- | --- |
| Suivi / Qualification | Icône de graphique identique observée sur bureau/mobile | Suivi : étapes/colonnes ; Qualification : cible ou liste de vérification. Labels conservés. |
| Reporter / Réaffecter / Annuler | Icône générique proche du réglage visible dans le détail du rappel ; vérifier mapping `paths`/`icon` | Horloge/flèche, personne/flèche, croix respectivement ; ne pas réutiliser une coche de succès comme secours. |
| Tâche / rendez-vous | L’objet doit être identifiable dans une file partagée | Téléphone pour appel, calendrier pour RDV, avec type et date textuels ; ne pas montrer un ancien rappel RDV comme une réservation. |
| Actualisation / calcul | Vocabulaire technique et liens UUID C | Loupe pour vérifier, coche pour confirmer, actualisation pour recalculer, avec verbes distincts et périmètre explicite. |
| Carte et légende | Deux comportements C ; cible de 28 px dans une vue | Composant accessible commun, cible interactive ≥44 px ; légende textuelle et liste alternative, couleur jamais seule. |
| Navigation mobile | Rail débordant V | Aujourd’hui, Prospects, Agenda, Rappels, Plus ; Suivi/Qualification/Carte/Imports/Préférences dans Plus selon droits, accès direct conservé depuis les contenus. |

À contrôler en recette : focus visible et restauré après dialogue, nom accessible
des icônes seules, texte agrandi à 200 %, contraste réel, labels non tronqués,
zones tactiles, réduction des animations. Le code contient déjà labels, lien
d’évitement, focus et réduction du mouvement : ne pas les supprimer.

## Éléments à préserver

- Téléphone cliquable avec nom accessible ; dates d’action/rappel distinctes et
  heure de Paris explicite ; notes sans envoi implicite au prospect.
- Pagination serveur, total daté, précédent résultat gardé en cas d’erreur de page.
- Erreurs près des champs, confirmation d’abandon d’un brouillon, conservation
  de la clé de commande en cas de résultat incertain.
- Contrôles d’opposition, éligibilité et unicité des preuves de gain ; responsable
  prospect, dossier et tâche distincts ; import sans affectation forcée.
- Carte générale : groupes mixtes, noms accessibles, liste de secours, couleurs
  cohérentes pour les responsables et état URL ; ne pas régresser E71-EVOL-09.
- Disponibilités réelles, validation par le collaborateur, protection des conflits
  et des rappels obsolètes. Aucune invitation externe ajoutée.

## Mesurer l’effet sans inventer un gain

**Unité de travail primaire :** après un échange commercial fictif, l’utilisateur
consigne le résultat sur le bon prospect et prépare la suite lorsqu’elle est
nécessaire. Une note seule n’est pas automatiquement un succès commercial.

Mesure de départ sur le même jeu synthétique, avant modification : temps médian
et dispersion pour retrouver le prospect/contact, enregistrer l’échange, planifier
la suite puis reprendre la liste ; nombre de fiches ouvertes par erreur, pertes
de contexte et interventions de l’animateur. Taux de réussite sans aide = nombre
de scénarios terminés sur la bonne cible sans intervention / nombre de scénarios
commencés. Les abandons restent au dénominateur ; panne technique et refus métier
sont distingués, pas supprimés du compte rendu.

Pour un usage réel ultérieur : taux de suite explicitement décidée = échanges
éligibles suivis d’une action liée ou d’une décision « aucune suite nécessaire »
/ échanges éligibles enregistrés sur la période. **Cette décision et son lien
ne sont pas instrumentés actuellement** : ne pas déduire ce taux des tâches
simplement présentes sur le prospect. Préférer d’abord l’observation assistée ;
une instrumentation durable nécessiterait son propre contrat et examen de données.

Scénario de 15–20 minutes, cinq utilisateurs internes si disponibles (commerciaux
et responsable), même ordinateur/mobile selon leur usage :

1. Depuis Aujourd’hui, identifier le bon rappel parmi trois homonymes.
2. Retrouver l’interlocuteur, consigner un appel fictif et programmer sa suite.
3. Reprendre la recherche filtrée à la fiche suivante.
4. Trouver un créneau et reporter le RDV, sur agenda de démonstration rempli.
5. Pour le responsable habilité, rattacher une preuve et constater un gain sans aide.

Tests séparés : contact n°26, 60 RDV, 60 propositions, import asynchrone simulé,
réseau lent/échec d’une section, 409, réponse de mutation perdue, accès retiré,
clavier/texte 200 %. Aucun appel, envoi ou changement de données réelles requis.
Les journaux métier existants peuvent prouver création et transition ; ils ne
mesurent ni le temps actif, ni l’hésitation, ni les clics perdus.

## Sources et suite

Racine des références de lignes :
[crm.js](../../../../localeo-backend/app/infrastructure/pwa/crm/crm.js),
[crm.css](../../../../localeo-backend/app/infrastructure/pwa/crm/crm.css),
[crm-agenda.js](../../../../localeo-backend/app/infrastructure/pwa/crm/crm-agenda.js),
[crm-actualisations.js](../../../../localeo-backend/app/infrastructure/pwa/crm/crm-actualisations.js),
[crm-priorite.js](../../../../localeo-backend/app/infrastructure/pwa/crm/crm-priorite.js),
[API](../../../../localeo-backend/app/api/prospection_api.py).

Les retours, la file quotidienne, la proposition de prochaine action et le mobile
sont déjà attendus dans [Parcours et règles](../../specifications/epic-71-crm-prospection/parcours-regles.md).
Leur absence est une correction, pas une nouvelle décision métier. Les extensions
et les critères inchangés à renforcer sont séparés dans
[la spécification des six lots](../../specifications/epic-71-crm-prospection/ux-productivite.md).
L’epic reste **En cours** ; audit et spécification seuls réalisés ici.
