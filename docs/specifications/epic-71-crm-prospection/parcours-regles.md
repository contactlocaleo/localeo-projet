# E71 — Parcours et règles

Référence : [README et arbitrages](README.md). Les règles marquées « proposé » dépendent des arbitrages correspondants. Toutes les preuves ci-dessous sont à construire, pas exécutées.

## Parcours et présentation ERP

Entrée proposée **Prospection** dans l'ERP, URL `/internal/erp/prospection`. Réutiliser l'en-tête partagé, le retour ERP toujours accessible, les menus autorisés et les composants de messages/formulaires. Ne pas créer une nouvelle PWA ni une nouvelle authentification.

Les vues sont Portefeuille (liste / étapes / carte), Mes actions, À qualifier et Imports. Une fiche organisation regroupe contacts, opportunités et chronologie ; chaque opportunité conserve ses propres tâches, décisions et liens métier. Retour à la liste avec recherche, filtres, tri et pagination conservés dans l'URL ; navigation clavier et historique navigateur utilisables. Une mutation non enregistrée demande confirmation avant sortie. Les dates horaires sont affichées en **Europe/Paris**, les instants stockés en UTC ; les dates civiles ne sont pas décalées.

Un seul bouton principal par opération : « Enregistrer », « Planifier », « Confirmer l'import » ou « Rattacher ». Les boutons d'activation, d'invitation ou de paiement appartiennent aux parcours métier correspondants. Désactiver un bouton pendant la requête ne remplace pas l'idempotence serveur. Après délai réseau, afficher « Résultat à vérifier » et relire l'opération avant de permettre un nouvel essai. Succès seulement après résultat serveur ; erreur, chargement et liste vide distincts.

## Objets et complétude — CA-01/02

- **Organisation prospectée** : UUID, nom obligatoire, type (`COLLECTIVITE`, `ASSOCIATION`, `COMMERCE`, `ENTREPRISE_CSE`, `AUTRE` proposés), identifiants officiels facultatifs et typés, commune principale facultative, origine, responsable facultatif, archivage et version. Le type n'impose pas un axe commercial. Nom et email générique ne sont pas des clés uniques.
- **Contact professionnel** : UUID, organisation, nom/fonction et coordonnées connues, qualité de provenance, état actif/obsolète. Au moins un nom ou une coordonnée exploitable ; ne pas inventer un interlocuteur à partir du seul nom d'une ville. Un départ rend le contact obsolète sans effacer les événements historiques.
- **Opportunité** : UUID, organisation, axe (`ANIMATION`, `PARTENARIAT_COMMERCANT`, `COFFRETS_PRO` proposés), objet, étape, responsable, priorité, dates, estimation facultative avec devise, version et liens métier. Deux opportunités du même axe peuvent coexister ; le titre n'est pas une clé d'unicité.
- **Tâche** : UUID, opportunité, type, responsable, échéance UTC et fuseau saisi, contact/canal éventuels, état, résultat, version. Une tâche de préparation interne n'est pas une sollicitation.

Une organisation minimale peut être enregistrée avec nom et provenance. Une opportunité minimale exige organisation, axe et objet. L'absence de responsable, de contact, de commune ou d'action suivante apparaît comme une anomalie de complétude ; elle ne fabrique pas de données. Les montants inconnus restent `null` ; les montants connus sont des entiers en unité monétaire mineure avec devise.

## Cycle commercial — CA-03

Étapes proposées : `A_QUALIFIER`, `A_CONTACTER`, `CONTACT_ENGAGE`, `BESOIN_QUALIFIE`, `PROPOSITION_PRESENTEE`, `DECISION_ATTENDUE`, `GAGNEE`, `PERDUE`, `EN_PAUSE`.

| Commande | Préconditions et résultat | Refus / trace |
| --- | --- | --- |
| Avancer ou revenir à une étape active | Opportunité non archivée, droit de gestion, version courante ; saut ou retour avec motif | Refuser changement direct d'une affaire terminale ; conserver ancienne/nouvelle étape, acteur et motif |
| Mettre en pause | Motif et date future de réexamen, ancienne étape mémorisée | Sans motif/date : refus ; arrivée de la date = rappel, jamais réouverture automatique |
| Reprendre | Action explicite vers étape active, motif | Opposition conservée et tâches non recréées implicitement |
| Déclarer perdue | Motif obligatoire ; historique conservé | Les tâches ouvertes sont proposées à annulation, pas supprimées ; leur traitement doit être confirmé |
| Déclarer gagnée | Preuve canonique lue par le serveur, conforme à ARB-04, droit de gestion et de consultation de la preuve | Un lien partenaire, un commerçant BROUILLON ou un checkout créé ne suffit pas ; refus `PREUVE_GAIN_INSUFFISANTE` |
| Rouvrir gagnée/perdue | Justification obligatoire ; conserver décision précédente et preuve datée | Ne modifie ni paiement, ni abonnement, ni dossier métier ; ne ressuscite aucune tâche annulée |

Un statut historique importé « gagné » reste une valeur de provenance et une anomalie à qualifier tant que la preuve métier requise n’est pas présente. Un remboursement ou une résiliation ultérieurs produisent une divergence visible entre preuve du gain historique et état courant ; ils ne réécrivent pas silencieusement l'histoire CRM. Le traitement de cette divergence appartient à un opérateur.

## Historique — CA-04

Enregistrer appel, rendez-vous, note et email consigné avec `occurred_at`, `recorded_at`, auteur et provenance. `recorded_at` est fixé par le serveur. Un email consigné n'invoque pas le fournisseur et n'affiche pas « délivré ». Une correction crée un événement référant l'événement corrigé avec motif ; pas d'édition silencieuse des traces. Les dates futures relèvent des tâches ; les corrections de date d'événement restent tracées.

La chronologie métier contient les informations nécessaires à la reprise commerciale. L'audit technique conserve IDs, codes d'action, versions et corrélation, jamais une copie intégrale du texte libre ou du fichier. La purge peut supprimer/anonymiser un contenu selon la politique retenue ; « historique » ne signifie pas conservation illimitée.

## Actions et rappels — CA-05/06

États proposés : `A_FAIRE`, `TERMINEE`, `ANNULEE`. Reporter modifie l'échéance avec motif et événement ; réaffecter vérifie un compte interne actif habilité au CRM. Terminer exige un résultat, annuler un motif. Répéter la même commande ne crée pas un deuxième événement. Les tâches d'une opportunité close restent visibles jusqu'à traitement explicite.

« Prochaine action » est la projection de la première tâche ouverte par échéance, puis UUID ; pas un champ libre divergent. « Mes actions » utilise l'identité du serveur. Aujourd'hui = journée civile Paris ; retard = échéance antérieure à l'instant serveur. À échéance précise, la tâche devient due, puis en retard. Une date sans heure importée reste à compléter, sans choix arbitraire d'horaire.

La file de rappels est une lecture des tâches, sans création périodique d'un rappel par affichage. Rechargement, double consultation ou reprise d'un worker ne multiplient rien. Proposition V1 : badge persistant et file ERP ; aucun email de rappel interne ni relance automatique externe tant qu'ARB-03 n'est pas étendu.

## Opposition et archivage — CA-20

Proposition ARB-07 : opposition portée par l'organisation ou le contact, applicable à un ou plusieurs axes/canaux, avec motif, origine, date et auteur. Une portée omise est refusée ; l'écran propose explicitement « toutes les sollicitations ».

Une organisation opposée bloque les sollicitations de ses contacts dans la portée choisie ; une opposition contact ne se propage pas silencieusement aux autres contacts. Ne pas contourner une opposition en changeant de contact après opposition globale. Planifier/reporter/réactiver une tâche de sollicitation vérifie à nouveau les oppositions actives ; une tâche de préparation ou une note factuelle reste possible. Les tâches existantes incompatibles apparaissent bloquées, sans être effacées.

Le système ne peut empêcher un appel passé hors Localeo : il refuse sa planification dans le CRM et avertit l'opérateur. Consigner après coup un échange réellement intervenu reste possible et traçable ; cela ne prouve pas un consentement. L'import, la fusion proposée, le rattachement et la réouverture conservent les oppositions. Une levée admin exige preuve et motif ; aucune case implicite d'accord commercial.

Archiver masque la fiche des vues actives, conserve les liens et interdit les nouvelles sollicitations ; réactiver ne lève pas l'opposition. Fusion destructive et export massif ne sont pas définis par cette V1 : proposition de les différer, à confirmer avec ARB-05. Le rapprochement reste un rattachement explicitement choisi, avec historique.

## Passage au métier — CA-16/17/18

Décision ARB-08 validée le 9 octobre : rechercher un objet existant, afficher son type et sa référence, vérifier les droits métier, puis rattacher explicitement à l'opportunité. Un objet apparenté ne doit pas être rattaché à la mauvaise organisation ; le serveur vérifie les identifiants comparables, et une divergence impose correction/justification autorisée.

Si aucun objet n'existe, ouvrir le parcours canonique avec un retour CRM local contrôlé. Ne pas placer contacts, notes ou fichier dans l'URL. L'opérateur accomplit la création avec ses confirmations propres, revient et rattache l'identifiant produit. Une fermeture entre création et rattachement peut laisser un objet métier sans lien CRM : la reprise recherche cet objet, elle ne recrée pas automatiquement. Le CRM garantit l'unicité de son lien ; les producteurs existants gardent leurs garanties de création.

Les commandes « rattacher » et « déclarer gagnée » sont différentes. Une affaire peut être rattachée mais pas gagnée. Chaque opportunité a un lien principal par type de cible ; remplacement explicite avec motif, ancienne référence dans la chronologie. Plusieurs opportunités peuvent concerner la même organisation métier, mais une même preuve de vente ne doit pas gonfler les gains : définir avec ARB-04 l'unicité de la preuve par opportunité/affaire.

## Indicateurs — CA-07/22

Compter séparément organisations distinctes, opportunités, tâches dues et gains vérifiés. Les volumes liste/tableau/carte proviennent d'une même requête filtrée ; le nombre de points n'est pas le nombre de prospects. Afficher les non-localisés séparément. Le tableau ne déplace pas une carte par glisser-déposer sans la commande de transition, ses motifs et ses refus.

Afficher période, filtre d'axe et définition : taux de gain proposé = affaires gagnées / affaires gagnées ou perdues sur décisions de la période ; dénominateur zéro = « non calculable ». Une réouverture exclut l'affaire des décisions terminales courantes ; le journal conserve ses anciennes décisions. L'indicateur et sa définition restent soumis à ARB-04. Ne pas appeler une somme d'estimations « chiffre d'affaires », additionner des devises différentes ou attribuer à chaque axe l'intégralité d'une même commande.
