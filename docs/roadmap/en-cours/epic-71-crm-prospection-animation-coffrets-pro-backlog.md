# EPIC 71 — Localeo CRM, prospection Animation et Coffrets

## Références et recadrage E71-EVOL-03

- État produit : **En cours**, selon la [roadmap commune](../README.md).
- Cadrage initial : 2 octobre 2026 ; décisions/imports E71-EVOL-01 et E71-EVOL-02 du 9 octobre ; **recadrage du 3 novembre 2026** à la demande utilisateur.
- [Spécification canonique V1](../../specifications/epic-71-crm-prospection/README.md), [format d'import et gabarit](../../specifications/epic-71-crm-prospection/import-carte.md).
- Phase présente : implémentation locale du CRM, migrations v290–v292 et vérification sur données synthétiques. Aucun déploiement, compte réel ou envoi fournisseur.

**Besoin actuel :** créer une application **Localeo CRM (PWA)** simple pour gérer la prospection commerciale et le suivi de la relation client sur les périmètres Animation et Coffrets. Saisir un prospect et ses contacts, suivre les échanges et étapes, prendre des notes et programmer des rappels WebPush/e-mail facultatif. Réutiliser les profils ERP avec des droits CRM distincts. Initialiser puis enrichir depuis un fichier produit par l'utilisateur depuis Excel, sans écraser le contexte existant.

La cible n'est plus un module de prospection seulement inclus dans l'ERP. La **carte interactive est maintenue en V1 sur confirmation utilisateur**. La V1 reporte les fiches communales enrichies et le parseur spécifique Gironde sur confirmation utilisateur du 3 novembre ; le besoin de réimport est couvert par un CSV standard. Ce report est **confirmé**, sans valider ni implémenter les anciens critères. Le détail historique demeure dans Git ; aucun classeur privé repris dans ce dépôt.

## Résultat attendu

Le commercial ouvre « Aujourd'hui », sait qui rappeler, ouvre une fiche pour retrouver ses contacts et le dernier échange, consigne sa note puis programme la suite. Une association intéressée par une animation et par des coffrets garde une fiche commune, avec deux dossiers commerciaux distincts. Après gain, les échanges restent consultables et les liens vers les applications métier permettent le suivi de la relation.

Acteurs : utilisateurs internes explicitement habilités au CRM ; responsable d'un dossier ou rappel ; administrateur des comptes ERP pour attribution/retrait des droits. Aucun accès prospect ni compte CRM autonome.

## Périmètre V1 retenu

1. **PWA CRM** PC/mobile, installation, identité visuelle Localeo et session interne partagée ; proposition d'implantation `/internal/crm/` sur le domaine backoffice.
2. **Fiches prospects et contacts** : coordonnées connues, commune, source, plusieurs contacts, notes et chronologie ; recherche, filtres, opposition et archivage.
3. **Dossiers commerciaux** : Animation ou Coffrets ; pour Coffrets, recrutement de partenaire commerçant ou achat entreprises/CSE. Responsable, six étapes simples, priorité normale/haute et prochaine action calculée.
4. **Carte et pilotage quotidien** : carte interactive par commune avec filtres partagés, groupes et accès aux fiches ; Aujourd'hui, suivi par étapes, mes rappels, dossiers sans action ; indicateurs simples, sans prévision de chiffre d'affaires.
5. **Rappels internes** persistants, WebPush volontaire par appareil, e-mail facultatif désactivé initialement ; destinataire = responsable interne, jamais prospect.
6. **Import CSV** : source et références stables, aperçu et bilan, INIT crée les absents ; UPSERT ajoute et complète les champs jamais renseignés, sans remplacer notes, statut, affectation ou rappels.
7. **Rattachements métier** explicites vers ERP/OnBoard, souscriptions Animation et commandes Coffrets, avec les droits de chaque domaine ; aucune conversion implicite.

Compléments recommandés : détection de doublons, responsable et prochaine action visibles, « Ne plus contacter », archivage réversible, filtres conservés et rappel accessible depuis la fiche. Ils évitent les oublis sans ajouter une administration complexe.

### Hors V1 retenue

Import XLSX Gironde et sections communales (CA-24), campagnes automatiques vers les prospects, synchronisation de boîtes mail, scraping/enrichissement, scoring IA, pipeline personnalisable, devis/facturation/paiement, fusion destructive, export massif et modification hors ligne. Le dossier continue de relier les applications métier qui possèdent ces fonctions.

## Décisions conservées et remplacées

- Coffrets comprend les achats entreprises/CSE, sens de « Pro » acquis le 2 octobre ; ne pas confondre avec Localeo Pro ou E72.
- Rattachements et preuves de gain du 9 octobre conservés : commerçant accepté et OnBoard lié, souscription Animation activée payée/gratuite, commande Coffrets payée. Accord verbal et paiement sont distincts.
- La demande du 3 novembre remplace « pas de nouvelle PWA » et ajoute WebPush/e-mail facultatif. Elle remplace l'attribution CRM implicite par des autorisations distinctes gérées dans ERP.
- Pour simplifier, recommandation de six étapes, CSV standard et upsert « compléter sans remplacer », plutôt que mapping mensuel multi-onglets et résolution à trois versions. Les IDs de critères restent stables.
- ARB-04b (une preuve canonique pour un seul dossier gagnant) et le CSV standard seul/report Gironde sont confirmés par l’utilisateur ; ARB-07 (conservation par catégorie) reste à définir avant données réelles. Les autres arbitrages et leur statut figurent dans le [README canonique](../../specifications/epic-71-crm-prospection/README.md).

## Critères d'acceptation

**Implémentation locale réalisée ; preuves et réserves dans le [bilan de vérification](../../specifications/epic-71-crm-prospection/verification-livraison.md).** 29 identifiants conservés/ajoutés, dont **28 actifs dans la V1 retenue** et **1 reporté**. CA-13 reste actif ; CA-24 n’est ni réutilisé pour un autre besoin ni coché comme réussi.

| Critère | Acteur / action | Résultat observable et refus attendu |
| --- | --- | --- |
| E71-CA-01 | Gestionnaire CRM crée un prospect et ses contacts | Saisie minimale possible, données inconnues visibles, plusieurs contacts ; aucun compte ou objet opérationnel/envoi implicite |
| E71-CA-02 | Ajouter un dossier Animation et un dossier Coffrets ou une nouvelle campagne | Une seule fiche prospect ; étapes, responsables et historique propres, pas d'écrasement d'un dossier passé |
| E71-CA-03 | Changer d'étape, pause/perte/gain/réouverture | Six étapes, motifs sensibles et réexamen, historique ; gain refusé sans preuve canonique ou si elle est attribuée à un autre dossier, aucune activation/paiement par changement d'étape |
| E71-CA-04 | Ajouter/corriger note, appel, rendez-vous ou e-mail consigné | Auteur, dates d'événement/saisie et correction retrouvables ; aucun envoi ou état de délivrance déduit d'une note |
| E71-CA-05 | Planifier, terminer, reporter, annuler ou réaffecter | Responsable habilité, échéance, résultat, retard et prochaine action cohérents ; aucune tâche terminée par consultation |
| E71-CA-06 | Ouvrir Aujourd'hui/Rappels et traiter l'échéance | File interne persistante, retard/jour/à venir et fuseau explicites, aucune duplication au rejeu ; tâche fermée/ancienne échéance ne renotifie pas |
| E71-CA-07 | Rechercher et filtrer les listes et le suivi par étapes | Même périmètre filtré en liste/suivi/carte, compteurs cohérents, pagination serveur, filtres conservés et vide distinct d'une erreur |
| E71-CA-08 | Déposer le CSV, choisir source/mode et prévisualiser | Aperçu sans mutation CRM, compléments/protections/doublons/rejets explicites ; fichier invalide refusé sans exécution |
| E71-CA-09 | Corriger/exclure des groupes incomplets ou incohérents | Rapport par ligne et groupe, valeurs non inventées ; aucune application partielle d'un groupe prospect |
| E71-CA-10 | Importer ou saisir un prospect ressemblant à un existant | Clés source stables, comparaison et rapprochement explicites ; jamais de fusion automatique au nom/commune/e-mail générique |
| E71-CA-11 | Réimporter, reprendre après panne ou traiter un lot concurrent | Aucun doublon, aucun écrasement des enrichissements/protections ; révision/candidat de rapprochement changé après aperçu = conflit explicite, y compris entre deux sources ou avec la saisie manuelle |
| E71-CA-12 | Consulter le bilan, arrêter/reprendre un lot | Source/mode/auteur/empreinte/résultats privés traçables ; arrêt conserve les groupes déjà appliqués et leurs enrichissements ultérieurs |
| E71-CA-13 | Ouvrir la carte interactive et un groupe communal | Centres identifiés comme approximatifs, regroupements bornés, mêmes filtres que la liste, accès aux prospects/dossiers sans doublons ; non-localisés toujours accessibles |
| E71-CA-14 | Prospect sans commune/INSEE ou hors catalogue | Saisie possible, anomalie non bloquante de localisation, correction explicite ; aucune ville marchande créée/publiée |
| E71-CA-15 | Utilisateur PC/mobile/clavier | Liste/fiche/notes/rappels exploitables, actions compréhensibles, retours cohérents, pas de scroll horizontal imposé ; liste utilisable si carte/référentiel indisponible, aucune donnée de contact/note transmise au fond de carte |
| E71-CA-16 | Rattacher un commerçant / ouvrir OnBoard puis reprendre | Droits métier propres, référence et dossier canoniques, historique CRM conservé, pas d'activation ou duplication automatique |
| E71-CA-17 | Rattacher partenaire/souscription Animation | Lien exact, droit vérifié, gain seulement sur activation canonique ; aucune invitation/commande/publication implicite |
| E71-CA-18 | Relier achat/commande Coffrets | Référence typée réelle, distinction estimé/commandé/payé, pas de paiement ni facture déclenchés par CRM |
| E71-CA-19 | Profils internes, session expirée/révoquée ou accès API direct | Contrôles serveur courants, CSRF, mêmes droits globaux, aucune fuite de contact/note et aucun accès SQLAdmin additionnel |
| E71-CA-20 | Marquer Ne plus contacter, réimporter ou rouvrir | Sollicitations bloquées, opposition conservée, levée réservée ; archivage/obsolescence jamais effacés par import |
| E71-CA-21 | Enregistrer ou envoyer des commandes concurrentes | Versions/idempotence/transaction, conflit explicite, notes indépendantes conservées ; révocation prime sur rejeu |
| E71-CA-22 | Consulter indicateurs et dossiers sans action | Prospects/dossiers distincts, gains comptés par preuves canoniques distinctes sans doubler une réouverture, filtres/période affichés, inconnus visibles ; pas de fausse conversion ou de chiffre d'affaires déduit |
| E71-CA-23 | Suivre le guide et le parcours synthétique | Installation/connexion → import → note → rappel → suivi → rattachement vérifiés par tests fonctionnels, documentation disponible selon droits ; pas de pilote externe exigé pour clôturer |
| E71-CA-24 | **Reporté : import spécifique Gironde et sections communales** | Ancien critère conservé ; contrat CSV CA-08 à 12/28 le remplace dans V1 retenue, sans prétendre traiter l'ancien XLSX |
| E71-CA-25 | Installer/ouvrir/actualiser Localeo CRM en PWA | Application nommée et scope propres, routes profondes et retour après connexion, mise à jour réelle, écran offline clair sans cache de données privées |
| E71-CA-26 | Activer/refuser WebPush puis recevoir/ouvrir un rappel | Opt-in par appareil, compte interne courant, aucune fuite sur écran verrouillé ; refus/expiration conserve le rappel interne ; retries/report/révocation sans doublons applicatifs |
| E71-CA-27 | Activer/désactiver les rappels par e-mail | Désactivés initialement, destinataire interne seulement, envoi à l'échéance sans rattrapage massif ni fallback implicite ; tâche annulée/droit retiré/adresse modifiée empêche l'envoi encore en attente ; vérification et opt-in liés à la version courante de l'adresse |
| E71-CA-28 | Utiliser le même modèle en INIT puis UPSERT | INIT ignore le prospect déjà connu ; UPSERT complète les vides non protégés et ajoute contacts/dossiers ; notes/statuts/responsables/rappels/oppositions conservés, absents non supprimés |
| E71-CA-29 | Administrateur ERP attribue/retire les droits CRM | Cases consulter/gérer/importer/administrer distinctes et dépendances contrôlées ; aucun droit automatique sur compte non admin existant, menu et API immédiatement cohérents |

## Impacts et limites

| Périmètre | Impact |
| --- | --- |
| Backend | Domaine prospection, API privées, persistance additive, import durable, worker/rappels et preuves de gain |
| ERP / E69 | Catalogue fermé des autorisations, API des comptes, écran de profils, menu et liens CRM ; identités actuelles conservées |
| Nouvelle surface CRM | PWA satellite dans le backend proposée ; manifest/scope, navigation, formulaires, listes et notifications |
| Email / WebPush | Transports existants, nouveaux abonnements CRM internes et outbox/déduplication ; pas de campagne prospect |
| OnBoard / Animation / Achats | Liens et lecture de preuves autorisés ; pas de création parallèle d'objets métier |
| Pro / Animation / Marketplace | Pas de nouvelle API publique ni modification directe de ces frontends ; destinataires métier existants préservés |
| Carte / géographie | Centres communaux, communes hors catalogue, regroupement et fallback liste ; composant/fournisseur à sélectionner, configuration et couverture à tester |
| Import / données | CSV documentaire vide fourni ; fichiers réels privés, pas de migration automatique des clients existants ; conservation à arrêter |
| Générateur / tests | Fixtures synthétiques dans le backend : deux périmètres, import/rejeu/conflit, opposition, rappels et profils ; aucun envoi réel |
| Documentation / exploitation | Guides CRM/import/profils, runbooks reprise/notifications, schéma/readiness/capacité et bundle à adapter à l'implémentation |

Ordre de réalisation : domaine/droits et PWA → fiches/notes/suivi/carte → tâches/rappels → import → rattachements/recette. Le [plan de vérification](../../specifications/epic-71-crm-prospection/verification-livraison.md) relie chaque critère aux tests, documents, fixtures et conditions d'activation. Le statut est **En cours** ; le bilan de vérification distingue les tests exécutés et les réserves de livraison.
