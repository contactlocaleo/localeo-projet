# Catalogue des APIs - EPIC 41

> Consolidation documentaire du 18 septembre 2026 : contributions Backend et Animation réunies, avec les précisions sur les périodes, l’audit et la suppression des notifications. Les catégories « à faire évoluer » et « à implémenter » décrivent le cadrage initial ; le [contrat généré](openapi.json) décrit les routes du code local et la [roadmap](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md) porte le statut de l’EPIC.

## 1. Synthese

| Categorie | Nombre de contrats/capacites identifies | Conclusion |
| --- | ---: | --- |
| `REUTILISER` | 8 | Briques core utilisables sans changer leur responsabilite. |
| `FAIRE_EVOLUER` | 8 | Authentification, support, documentaire, paiement, notifications et application commercant doivent accueillir le contexte animation. |
| `IMPLEMENTER` | 65 | Le portail partenaire, les parcours participant et commercant, le suivi des operations et la supervision Localeo necessitent une API `animation_locale` dediee. |

Le nombre indique un inventaire de cadrage et non un engagement de granularite definitive. Certains endpoints de lecture pourront etre regroupes apres definition des schemas et contraintes de performance.

## 2. APIs et capacites a reutiliser

| ID | Route/capacite existante | Usage EPIC 41 | Mode de reutilisation | Observation |
| --- | --- | --- | --- | --- |
| REU-01 | `GET /public/referencement/villes` | Recherche et affichage d'une commune. | API existante pour les vues publiques ; use case/repository pour les projections protegees. | Le tenant animation reference une ville existante. |
| REU-02 | `GET /public/referencement/villes/{ville_id}` | Libelle et metadonnees de commune. | API existante ou use case `ConsulterDetailVille`. | Ne pas dupliquer la commune. |
| REU-03 | `GET /public/referencement/commercants?ville_id=...` | Affichage public des commercants d'une commune. | API publique existante pour les besoins strictement publics. | L'eligibilite de creation ne doit pas utiliser directement ce contrat. |
| REU-04 | `GET /public/referencement/commercants/{commercant_id}` | Detail public d'un commercant. | API existante. | Les donnees internes restent exclues. |
| REU-05 | `GET /public/commercialisation/coffrets?ville_id=...` | Consultation du catalogue public des coffrets. | API existante pour les vues publiques ; use case/repository cote serveur. | La selection de lots exige une projection protegee plus restrictive. |
| REU-06 | `GET /public/commercialisation/coffrets/{coffret_id}` | Detail public d'un coffret. | API existante. | Ne remplace pas le controle d'eligibilite du lot. |
| REU-07 | Capacites `dam` d'images | Logos et visuels d'animation. | Reutiliser le stockage et les metadonnees ; rattachement porte par l'animation. | Les droits d'upload partenaire restent a definir. |
| REU-08 | Outbox email/SMS, audit et batch runner `exploitation` | Confirmation d'inscription, QR, gagnants, relances et traces. | Reutilisation interne par ports/use cases, jamais appel direct du frontend. | Ajouter des types d'evenements animation, sans dupliquer l'infrastructure. |

## 3. APIs et capacites a faire evoluer

| ID | Domaine proprietaire | Existant | Evolution necessaire | Contrat cible indicatif | Priorite |
| --- | --- | --- | --- | --- | --- |
| EVO-01 | `identite_acces` | Sessions commercant et API keys. | Adapter le mecanisme Localeo de token/session a un profil Animation distinct portant acteur, partenaire, roles et communes habilitees. | Session Animation dediee et contexte injecte dans les routes protected ; aucun OIDC externe au MVP. | P0 |
| EVO-02 | `support` | Contacts consommateur publics et threads commercant. | Ajouter un canal protege partenaire avec rattachement facultatif a une animation. | `GET /protected/support/animation-locale/ressources`, `POST /protected/support/animation-locale/messages`. | P1 |
| EVO-03 | `documentaire` | Documents publics, commercants et administration. | Stocker, securiser, versionner et telecharger flyers, bilans et exports d'animation. | Acces via facades `animation_locale`; API documentaire directe reservee aux traitements internes. | P0 |
| EVO-04 | `exploitation` | Outbox email/SMS et envoi WebPush batch. | Ajouter notifications participant, gestionnaire et commercant, push, statuts de diffusion et deeplinks animation. | Types d'evenements et subscriptions ; batchs existants reutilises. | P0 |
| EVO-05 | `gestion_achats` | Achat professionnel Stripe, activation et consultation des `CoffretInstance`. | Rattacher l'achat professionnel d'une ligne de lots a l'animation, reserver les instances creees apres confirmation et activer une instance prepayee lors de l'envoi du gain. | L'achat conserve son montant catalogue et sa transaction Stripe ; aucun achat a zero euro n'est cree pour le gain. | P0 |
| EVO-06 | Application commercant / `exploitation` | Validation de prestation par QR coffret. | Reconnaitre un QR participant, valider une etape, consulter les animations du commerce et recevoir les notifications d'inclusion. Masquer la rubrique si Animation n'est pas active dans la commune. | Contrats commerçant `ANI-M-*` avec contexte issu de la session. | P0 |
| EVO-07 | Paiement / Stripe | Paiement d'achat professionnel et Stripe plateforme. | Reutiliser le checkout d'achat professionnel pour financer chaque ligne de lots et verifier la confirmation avant publication. | Initialisation exposee par `animation_locale`, webhook et preuve de paiement portes par `gestion_achats`. | P0 |
| EVO-08 | `dam` | Upload d'image surtout public/admin selon route actuelle. | Autoriser les assets d'une animation pour un gestionnaire habilite et appliquer quotas/formats. | Route protegee DAM ou facade d'upload animation. | P1 |

## 4. APIs `animation_locale` a implementer

### 4.1 Portail partenaire - contexte et pilotage

| ID | Methode et chemin cible | Besoin maquette | Priorite |
| --- | --- | --- | --- |
| ANI-P-001 | `GET /protected/animation-locale/contexte-portail` | Utilisateur, partenaire, commune active, communes habilitees, abonnement et permissions. | P0 |
| ANI-P-002 | `PUT /protected/animation-locale/contexte-portail/commune-active` | Changer explicitement de tenant commune. | P0 |
| ANI-P-003 | `GET /protected/animation-locale/notifications` | Liste des alertes et notifications avec `animation_id`, `action_cible`, `onglet_cible`. | P1 |
| ANI-P-004 | `POST /protected/animation-locale/notifications/{notification_id}/lire` | Marquer une notification comme lue, de facon idempotente. | P1 |
| ANI-P-005 | `GET /protected/animation-locale/dashboard-performance` | KPIs, series, top commercants, alertes, animations a action et indicateurs economiques/d'usage des gains ; accepte `horizon_expiration_jours` de 1 a 365, 30 par defaut. | P0 |
| ANI-P-006 | `GET /protected/animation-locale/abonnement` | Projection UX de la formule, du statut, des limites et droits. | P0 |
| ANI-P-007 | `POST /protected/animation-locale/notifications/lire-tout` | Marquer toutes les notifications du gestionnaire comme lues. | P2 |

### 4.2 Modeles, eligibilite et creation

| ID | Methode et chemin cible | Besoin maquette | Priorite |
| --- | --- | --- | --- |
| ANI-C-001 | `GET /protected/animation-locale/modeles` | Catalogue contextualise des modeles disponibles. | P0 |
| ANI-C-002 | `GET /protected/animation-locale/modeles/{modele_code}` | Detail, prerequis et parametres du modele. | P0 |
| ANI-C-003 | `GET /protected/animation-locale/communes/{commune_id}/commercants-eligibles` | Selection des commercants et raisons de non-eligibilite. | P0 |
| ANI-C-004 | `GET /protected/animation-locale/communes/{commune_id}/coffrets-eligibles` | Selection des lots actifs de la commune et raisons de non-eligibilite. | P0 |
| ANI-C-005 | `POST /protected/animation-locale/animations` | Creer le brouillon initial. | P0 |
| ANI-C-006 | `PATCH /protected/animation-locale/animations/{animation_id}` | Enregistrer la configuration modifiable. | P0 |
| ANI-C-007 | `GET /protected/animation-locale/animations/{animation_id}/validation-publication` | Lister prerequis, erreurs et avertissements avant publication. | P0 |
| ANI-C-008 | `POST /protected/animation-locale/animations/{animation_id}/publier` | Publier, generer le QR/flyer et lancer la diffusion aux commercants. | P0 |
| ANI-C-009 | `GET /protected/animation-locale/animations/{animation_id}/lots/financements` | Suivre achat, montant, checkout, paiement effectif et instances reservees par lot. | P0 |
| ANI-C-010 | `POST /protected/animation-locale/animations/{animation_id}/lots/{lot_ordre}/paiement/initialiser` | Initialiser ou reprendre le checkout Stripe professionnel d'une ligne de lots. Entete `Idempotency-Key` obligatoire. | P0 |

### 4.3 Liste et fiche animation

| ID | Methode et chemin cible | Besoin maquette | Priorite |
| --- | --- | --- | --- |
| ANI-A-001 | `GET /protected/animation-locale/animations` | Liste paginee et filtrable du tenant actif. | P0 |
| ANI-A-002 | `GET /protected/animation-locale/animations/{animation_id}` | En-tete et synthese de la fiche. | P0 |
| ANI-A-003 | `GET /protected/animation-locale/animations/{animation_id}/configuration` | Lecture de la configuration courante. | P0 |
| ANI-A-004 | `GET /protected/animation-locale/animations/{animation_id}/workflow` | Etapes, blocages, transitions et prochaine action. | P0 |
| ANI-A-005 | `GET /protected/animation-locale/animations/{animation_id}/live` | Compteurs et alertes live. | P0 |
| ANI-A-006 | `GET /protected/animation-locale/animations/{animation_id}/live/evenements` | Flux recent pagine ou incremental. | P1 |
| ANI-A-007 | `GET /protected/animation-locale/animations/{animation_id}/participants` | Participants masques, progression et qualification. | P0 |
| ANI-A-008 | `GET /protected/animation-locale/animations/{animation_id}/validations` | Validations, anomalies et filtres. | P0 |
| ANI-A-009 | `GET /protected/animation-locale/animations/{animation_id}/audit` | Audit partenaire limite aux evenements publiables. | P1 |
| ANI-A-010 | `POST /protected/animation-locale/animations/{animation_id}/cloturer` | Cloture atomique, arret inscriptions/validations et gel des eligibles. | P0 |
| ANI-A-011 | `POST /protected/animation-locale/animations/{animation_id}/annuler` | Annule un brouillon si aucun lot n'est payé, expire le paiement en attente, annule les invitations et libère le quota one-shot éventuel. | P1 |
| ANI-A-012 | `GET /protected/animation-locale/animations/{animation_id}/participants/export.csv` | Export CSV trace des participants d'une animation. | P0 |
| ANI-A-013 | `POST /protected/animation-locale/animations/archiver-lot` | Archiver un lot d'animations eligibles, avec resultat unitaire. | P2 |
| ANI-A-014 | `DELETE /protected/animation-locale/animations/{animation_id}/participants/{participant_id}` | Supprimer une inscription erronee avec droit dedie, audit et controle des dependances de tirage. | P0 |

### 4.4 Application commercant

| ID | Methode et chemin cible | Besoin application | Priorite |
| --- | --- | --- | --- |
| ANI-M-001 | `GET /protected/animation-locale/commercants/me/contexte` | Exposer la commune active, les permissions, le compteur de notifications et la disponibilite explicite du module Animation. | P0 |
| ANI-M-002 | `GET /protected/animation-locale/commercants/me/animations` | Lister uniquement les animations auxquelles le commerce de la session participe. | P0 |
| ANI-M-003 | `GET /protected/animation-locale/commercants/me/animations/{animation_id}` | Afficher le detail en lecture seule et les donnees agregees de l'etape du commerce. | P0 |
| ANI-M-004 | `GET /protected/animation-locale/commercants/me/notifications`, `POST /protected/animation-locale/commercants/me/notifications/{notification_id}/lire`, `POST /protected/animation-locale/commercants/me/notifications/{notification_id}/non-lire`, `DELETE /protected/animation-locale/commercants/me/notifications/{notification_id}` | Inbox persistante, badge, deeplink, lecture réversible et suppression logique d'une notification du commerce. | P0 |

La disponibilite du module est determinee depuis son activation ou son abonnement pour la commune active, jamais depuis le nombre d'animations. La creation d'une inclusion produit l'evenement idempotent `ANIMATION_COMMERCANT_INCLUS`. L'inbox est obligatoire ; WebPush et email respectent les abonnements et preferences du commerçant.

### 4.5 Flyers, tirages, gains et bilans

| ID | Methode et chemin cible | Besoin maquette | Priorite |
| --- | --- | --- | --- |
| ANI-F-001 | `GET /protected/animation-locale/animations/{animation_id}/flyer` | Metadonnees et apercu du flyer courant. | P0 |
| ANI-F-002 | `POST /protected/animation-locale/animations/{animation_id}/flyer/regenerer` | Regeneration tracee et idempotente. | P0 |
| ANI-F-003 | `GET /protected/animation-locale/animations/{animation_id}/flyer/download` | Telechargement securise du PDF. | P0 |
| ANI-T-001 | `GET /protected/animation-locale/animations/{animation_id}/tirages` | Population figee, tirages et gagnants. | P0 |
| ANI-T-002 | `POST /protected/animation-locale/animations/{animation_id}/tirages` | Executer un tirage idempotent sur population figee. | P0 |
| ANI-G-001 | `GET /protected/animation-locale/animations/{animation_id}/gains` | Liste et statut des gains. | P0 |
| ANI-G-002 | `POST /protected/animation-locale/animations/{animation_id}/gains/{gain_id}/envoyer` | Creer/activer le coffret et notifier le gagnant. | P0 |
| ANI-G-003 | `GET /protected/animation-locale/animations/{animation_id}/gains/coffrets/consommation` | Suivi de consommation des coffrets gagnes. | P1 |
| ANI-G-004 | `POST /protected/animation-locale/animations/{animation_id}/gains/{gain_id}/remplacer` | Remplacer un gagnant par le prochain suppleant, avec motif et audit. | P0 |
| ANI-G-005 | `POST /protected/animation-locale/animations/{animation_id}/gains/{gain_id}/relancer` | Relancer la notification d'un gagnant sans recreer son gain. | P1 |
| ANI-B-001 | `GET /protected/animation-locale/animations/{animation_id}/bilan` | KPIs, synthese finale et objet `consommation_financiere` defini par l'Epic 41 ; accepte `horizon_expiration_jours` de 1 a 365, 30 par defaut. | P0 |
| ANI-B-002 | `GET /protected/animation-locale/animations/{animation_id}/bilan/export.csv` | Export CSV du bilan. | P1 |
| ANI-B-003 | `GET /protected/animation-locale/animations/{animation_id}/bilan/export.pdf` | Export PDF complet du bilan. | P2 |

### 4.6 Vues globales du portail

| ID | Methode et chemin cible | Besoin maquette | Priorite |
| --- | --- | --- | --- |
| ANI-V-001 | `GET /protected/animation-locale/participants` | Vue participants multi-animations du tenant actif. | P1 |
| ANI-V-002 | `GET /protected/animation-locale/validations` | Vue validations multi-animations. | P1 |
| ANI-V-003 | `GET /protected/animation-locale/validations/export.csv` | Export selon les filtres actifs. | P1 |
| ANI-V-004 | `GET /protected/animation-locale/tirages` | Vue tirages et gains multi-animations. | P1 |
| ANI-V-005 | `GET /protected/animation-locale/gains/coffrets/consommation` | Vue globale des coffrets gagnes. | P1 |
| ANI-V-006 | `GET /protected/animation-locale/flyers` | Liste et statut des flyers. | P1 |
| ANI-V-007 | `GET /protected/animation-locale/bilans` | Comparaison des bilans. | P1 |
| ANI-V-008 | `GET /protected/animation-locale/bilans/export.csv` | Export global filtre. | P1 |

### 4.7 Parcours public participant

| ID | Methode et chemin cible | Besoin | Priorite |
| --- | --- | --- | --- |
| ANI-U-001 | `GET /public/animation-locale/animations/{animation_id}` | Page publique contextualisee de l'animation. | P0 |
| ANI-U-002 | `GET /public/animation-locale/inscriptions/{token}` | Resoudre et verifier un QR/lien d'inscription. | P0 |
| ANI-U-003 | `POST /public/animation-locale/animations/{animation_id}/inscriptions` | Inscrire nom, prenom, email et telephone avec consentements. | P0 |
| ANI-U-004 | `GET /public/animation-locale/participants/{token}` | Consulter progression, qualification et QR personnel sans compte. | P0 |
| ANI-U-005 | `GET /public/animation-locale/participants/{token}/qrcode` | Rendre l'image du QR participant. | P0 |
| ANI-U-006 | `POST /public/animation-locale/participants/{token}/renvoyer-qrcode` | Renvoyer le QR avec anti-abus. | P1 |

### 4.8 Supervision interne Localeo

| ID | Methode et chemin cible | Besoin | Priorite |
| --- | --- | --- | --- |
| ANI-I-001 | `GET /internal/animation-locale/animations/live` | Vision live globale et blocages. | P1 |
| ANI-I-002 | `GET /internal/animation-locale/animations/{animation_id}` | Diagnostic complet support. | P1 |
| ANI-I-003 | `GET /internal/animation-locale/animations/{animation_id}/audit` | Audit complet reserve Localeo. | P1 |
| ANI-I-004 | `POST /internal/animation-locale/animations/{animation_id}/corriger` | Correction exceptionnelle motivee et auditee. | P2 |
| ANI-I-005 | `POST /internal/animation-locale/conservation/purger` | Batch de purge/anonymisation. | P1 |

### 4.9 Suivi des operations asynchrones

| ID | Methode et chemin cible | Besoin | Priorite |
| --- | --- | --- | --- |
| ANI-O-001 | `GET /protected/animation-locale/operations/{operation_id}` | Suivre publication, document, export ou notification asynchrone. | P0 |

## 5. Decisions de reutilisation

1. Le portail ne compose pas lui-meme les APIs villes, commercants et coffrets pour determiner l'eligibilite. Cette logique appartient a `animation_locale` et appelle les domaines core cote serveur.
2. Les flyers et exports sont exposes sous `/animation-locale` parce que leurs droits et leur cycle de vie sont metier ; le contenu binaire et ses versions restent portes par `documentaire`.
3. Le financement d'un lot et l'envoi d'un gain sont des commandes `animation_locale`; le checkout, le paiement Stripe, la creation et l'activation de la `CoffretInstance` restent portes par `gestion_achats`.
4. Le support partenaire conserve des routes sous `/support`, meme si elles sont accessibles depuis le portail Animation.
5. La validation par l'application commercant utilise une route `animation_locale`, distincte de la validation d'une prestation de coffret.

## 6. Arbitrages valides

Tous les choix techniques `ARB-01` a `ARB-63` sont actees dans le [registre des arbitrages](registre-arbitrages.md). Conformement a l'amendement valide de `ARB-35`, la vue globale Participants `ANI-V-001` appartient au MVP. Conformement a l'amendement valide de `ARB-46`, le chiffrement applicatif des PII participant est reporte apres le MVP et doit etre reevalue avant production. `ARB-60` encadre la suppression manuelle d'un participant avant son integration a une population de tirage. `ARB-61` et `ARB-62` encadrent la disponibilite par commune, la projection commercant et la notification d'inclusion. `ARB-63` impose le paiement professionnel Stripe des lots et leur reservation avant publication. Les contrats utilisent une origine publique configurable, des gabarits email/flyer versionnes et l'abstraction de stockage prive de `documentaire` ; les integrations Stripe et application commercant sont des lots coordonnes.

## 7. Prise en compte du rapport Figma

Le [rapport des APIs manquantes](rapport-apis-manquantes.md) a ete rapproche du contrat canonique :

- ajouts reels : reference participant anonymisee, export participants, contenu flyer, remplacement/relance de gain et trois fonctions P2 ;
- contrats deja presents : dashboard, audit, flyer download, pagination participants et filtres validations ;
- conventions conservees : `/protected/animation-locale/dashboard-performance` plutot que `/partenaire/dashboard`, `page/page_size` pour les listes stables et `cursor` pour l'audit ;
- enrichissements compatibles : alias `q` pour la recherche animation, filtre rapide `periode=7j|30j|12m`, PATCH racine traite comme mise a jour partielle de configuration ;
- SSE/WebSocket reste hors MVP conformement a `ARB-24`; le polling a 15 secondes est conserve.

### Periode d activite du tableau de bord

Les bornes `date_debut` et `date_fin` filtrent les inscriptions par `inscrit_at` et les validations par `validated_at`, independamment : une validation recente reste comptabilisee meme si son participant est inscrit avant la periode. Les indicateurs participants et eligibles concernent les inscrits de la periode. Les series journalieres utilisent Europe/Paris ; les comparaisons utilisent UTC. Sans bornes, tout l historique est retenu. Le nombre d animations et les alertes restent une vue de la situation courante de la commune, sous les filtres animation, modele et statut applicables aux animations.


### Audit partenaire d'une animation

La requete filtre les traces en base sur l'animation autorisee (ressource,
metadata.animation_id ou participant/validation rattache), sans plafond global.
Les inscriptions et validations persistees completent les traces historiques,
y compris pour les imports ; chaque activite est comptee une seule fois.
Une validation annulee reste une activite historique avec son statut actuel ;
sa trace d'annulation est distincte. Seules les informations non nominatives
sont projetees. Le curseur est lie a l'animation, trie par date puis identifiant ;
le portail parcourt les pages pour afficher toute l'activite, tous types par defaut,
avec volumes quotidiens en Europe/Paris et filtre par action.


### Suppression des notifications partenaire

DELETE /protected/animation-locale/notifications/{notification_id} supprime une
notification de l'inbox du partenaire pour la commune active. La suppression est
persistante et idempotente (204, y compris si elle est deja absente ou hors du
perimetre autorise). La requete SQL impose partenaire_id et commune_id ; elle ne
modifie ni l'activite ni l'audit de l'animation. Le portail propose la suppression
individuelle depuis la cloche, recharge la liste et son compteur apres succes,
et parcourt toutes les pages pour rendre les anciennes notifications accessibles.
