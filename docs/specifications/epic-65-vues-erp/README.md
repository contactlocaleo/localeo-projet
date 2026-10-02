# EPIC 65 — Vues ERP audit, paiements et reversements

## Statut et périmètre

Spécification V1 du **26 septembre 2026**, implémentation **V1.4 le 1er octobre 2026**, issue du
[backlog EPIC 65](../../roadmap/en-cours/epic-65-vues-erp-audit-paiements-reversements-backlog.md).
État produit : **En cours**, selon la [roadmap](../../roadmap/README.md).
Les trois consultations sont implémentées localement dans le backend ; les
preuves et limites figurent dans le [bilan](verification-livraison.md#bilan-dimplementation-v14).
Aucun déploiement ni changement de profils E69 n'est déclaré réalisé.

- [Architecture et contrats cibles](architecture-contrats.md).
- [Traçabilité, tests et livraison](verification-livraison.md).
- Dépendances : socle [ERP 60](../epic-60-vision-360-commercialisation/README.md),
  [Vision 360 Achats](../epic-51-vision-360-achats/README.md),
  [EPIC 30](../../roadmap/terminees/epic-30-vue-360-reversements-paiements-backlog.md),
  [Stripe Connect 39](../../roadmap/terminees/epic-39-stripe-connect-psp-backlog.md)
  et [suivi bancaire 43](../../roadmap/terminees/epic-43-suivi-payouts-bancaires-stripe-connect-backlog.md).

Le backend, qui sert déjà l’ERP, est l’unique application à modifier. Les trois
frontends ne consomment pas ces nouveaux écrans ni leurs API internes.

### Choix et hypothèses

Le cadrage des profils est porté depuis le 1er octobre 2026 par la nouvelle
[EPIC 69](../../roadmap/en-cours/epic-69-profils-acces-erp-satellites-backlog.md) :
Lecteur, Backoffice, Finance et cumul Backoffice + Finance. Elle nécessite de
réviser `E65-D02` pour les lectures financières selon leur périmètre, en gardant
Audit global, SQLAdmin et commandes d'argent réservés à l'admin historique.
Ce changement reste à spécifier et implémenter dans E69 ; la V1.3 conserve
le socle ADMIN et explicite ci-dessous les conditions de livraison combinée.
Les tests de refus de ce socle ne constituent pas les preuves des nouveaux profils.

| Référence | Décision ou hypothèse | Conséquence |
| --- | --- | --- |
| E65-D01 | Demande acquise : trois vues intégrées à l’ERP, Audit dans Supervision, Paiements et Reversements dans « Paiements et facturation ». | Remplacer les raccourcis vers les listes SQLAdmin pour ces consultations. |
| E65-D02 | Conservation des droits existants : ADMIN exclusivement. | EXPLOITATION reste refusé même avec une session ERP et des communes ; aucune permission nouvelle accordée. |
| E65-H01 | Confirmé par l'utilisateur le 1er octobre 2026 : paiements de `PaiementOrm`, achats et commandes d’achat. | Abonnements et commandes de souscription restent dans leurs dossiers existants ; pas d’agrégation de sources financières différentes. Les achats de lots Animation représentés par une commande d’achat sont inclus. |
| E65-H02 | Confirmé par l'utilisateur le 1er octobre 2026 : consultation ERP et liens vers les actions financières existantes. | Pas de nouveau formulaire de lancement/reprise de campagne dans ces vues ; les contrôles d’accès et de commande des écrans actuels sont conservés. |
| E65-D03 | Contrainte conservée : lecture sans mutation métier ni appel Stripe. | L’actualisation ne synchronise pas les frais, ne réconcilie rien, ne génère pas de document. |
| E65-D04 | Choix technique : projections paginées, filtrage en base, détails bornés, dates et montants explicites. | Ne pas exposer une liste ORM ni tronquer des données en mémoire à 200 lignes. |

Les références H01/H02 sont conservées pour la traçabilité : l'utilisateur a
confirmé ce périmètre avant l'implémentation des lots financiers. Abonnements
et nouvelles actions intégrées restent exclus. Les consultations utilisent
les mêmes droits ADMIN que l'audit, sans élargissement implicite E69.

### Dépendance aux profils E69

| Surface | Livraison E65 autonome | Cible combinée E69 / E65 |
| --- | --- | --- |
| Audit global, recherche et détail | ADMIN | Admin seulement |
| Paiements, reversements, synthèses et sections métier | ADMIN | Lecteur, Backoffice, Finance et Admin dans leur périmètre effectif |
| Liens vers actions financières existantes | ADMIN, droits actuels de la destination | Suivi financier spécialisé à Finance/Admin ; commandes d'argent à Admin seul, même pour Backoffice + Finance ; aucune commande pour Lecteur |
| Console historique mixte, références techniques et révélations personnelles | Droits ADMIN existants | SQLAdmin reste admin seul ; classification et masquage portés par E69, aucun accès technique induit par la lecture métier |

La colonne combinée reprend `E69-CA-11/20`, sans créer dès maintenant des rôles
acceptés par les routes. Avant son activation, E69 doit définir la politique
de capacités, le périmètre de chaque projection et des totaux, les champs
autorisés et la réévaluation des sessions. Le contrôle s'applique aussi aux
sections, pièces et liens directs, avant chargement. Les tests futurs doivent
prouver à la fois l'accès métier et les refus techniques, ainsi que la révocation.
L'ouverture financière est bloquée tant que ces conditions ne sont pas remplies ;
la conception et l'implémentation du socle ADMIN restent indépendantes.

## Existant vérifié

Constat initial sur le backend `7049de7`, documentation de base `631fd10` avec
cadrage local ; revue ciblée sur le backend `eec63d2` et le projet `696d487`.
Ce constat ne prouve pas l’état déployé.

Relecture V1.2 : backend `3252c72`, projet `484f10d` avant les modifications
documentaires de cette tâche. Les raccourcis SQLAdmin, le garde ERP
ADMIN/EXPLOITATION et la politique ADMIN des interfaces historiques sont
toujours présents. Les nouvelles routes E65 ne sont pas déclarées dans le code
examiné. Le fichier de suivi des environnements, déjà modifié localement, reste
hors de cette intervention.

Relecture V1.3 : backend `ad42635`, projet `92f3d2a`, arbres propres au démarrage.
Les trois destinations renvoient toujours aux listes SQLAdmin et les routes
internes E65 restent absentes. La vérification de session persistée est portée
par `AdminSessionMiddleware`, distinct du contrôle des attributs du cookie ERP.
La revue des producteurs financiers précise les devises EUR/eur et le compte
Stripe historisé du reversement ; les contrats ci-dessous intègrent ces points.

| Surface | Code existant | Écart à traiter |
| --- | --- | --- |
| Navigation | `app/infrastructure/erp/erp.js`, `app/api/erp_ui.py` | Les trois destinations pointent vers SQLAdmin ; ajouter les pages ERP et leur contrôle ADMIN avant de charger les données. |
| Audit | `EvenementAuditOrm`, repository `EvenementAuditRepositorySqlAlchemy`, `EvenementAuditAdmin` | Lecture seule existante, mais `lister(limit=200)` ne fournit pas une recherche globale filtrée/paginée. Des écritures ORM directes imposent d’assainir aussi les données historiques à la lecture. |
| Paiements | `PaiementOrm`, `PaiementAdmin`, `ServiceVision360Achats._payment_payload` et `.paiements` | Recherche globale paginée absente ; mapping des états/montants et racine achat/commande déjà disponible. `date_creation` n’est pas une date d’encaissement. |
| Reversements | `_build_reversements_360_data`, console `/internal/reversements/vue-360`, API finance | Suivi métier existant, à extraire en projection réutilisable ; le rendu HTML et ses agrégats actuels ne constituent pas un contrat paginé à copier dans l’ERP. |
| Facturation | Traces consultées par achat enfant, dossiers de facturation existants | La page actuelle n'atteste pas la disponibilité d'un fichier et contient un lien GET vers un reçu généré seulement en POST. Corriger ce lien dans le parcours réutilisé ; distinguer trace et téléchargement. Aucune relation directe pièce→paiement à inventer. |

Sources applicatives dans le [backend](../../../../localeo-backend/README.md) ;
les correspondances et frontières sont précisées dans l’architecture.

La revue du 27 septembre précise le rattachement des paiements sources des
reversements : conserver tous les liens explicites, signaler les cas ambigus
et ne pas réduire plusieurs paiements au dernier paiement d’un achat. Elle
précise aussi la sélection commune des paiements directs et des achats enfants
dans la Vision 360 Achats, les couples de filtres de campagne et les tris des sections.
Les dix critères d’acceptation, les droits et les exclusions restent conservés.

La revue V1.2 précise les refus HTTP, la pagination sur un jeu stable,
l'assainissement des chemins d'audit et les liens documentaires réellement
consultables. Elle ne transforme ni les hypothèses H01/H02 ni les profils E69
en fonctionnalités livrées.

## Parcours commun — E65-CA-01, 07, 08, 09, 10

L’administrateur ouvre une rubrique, filtre une liste, consulte un détail puis
revient à la même recherche. Les nouveaux chemins IHM sont :

- `/internal/erp/audit` et `/internal/erp/audit/{id}` ;
- `/internal/erp/paiements` et `/internal/erp/paiements/{id}` ;
- `/internal/erp/reversements` et `/internal/erp/reversements/{id}`.

Les pages avec identifiant contrôlent son format UUID. L’accès anonyme à une
page renvoie vers la connexion interne selon le mécanisme existant ; une session
EXPLOITATION reçoit un refus, sans masquer simplement le tableau côté JavaScript.
Les API restent protégées indépendamment de l’IHM. La rubrique Finance conserve
ses autres destinations, notamment factures et demandes de facturation.

Sur ordinateur, la page occupe la largeur utile de l’ERP : titre et date de
lecture, barre de recherche/filtres, synthèse financière compacte le cas échéant,
tableau puis pagination. Le détail remplace la liste ou occupe un panneau large,
avec URL propre ; il n’empile pas une succession de fenêtres. Sur petit écran,
les mêmes informations essentielles sont présentées par lignes étiquetées ;
les références techniques et données secondaires restent repliées.

Recherche validée par Entrée ou « Rechercher », filtres appliqués ensemble,
« Réinitialiser » visible. Les filtres non sensibles, page et taille sont portés
dans l’URL ; aucune donnée bancaire, adresse email ou valeur de métadonnée n’y
est ajoutée. Un changement de filtre revient à la première page. Le retour
restaure les filtres et le focus. Les liens de détail restent utilisables au clavier.

Par défaut : 30 derniers jours calendaires Europe/Paris pour Audit et Paiements,
campagne courante pour Reversements, taille 25. Audit et paiements sont triés du
plus récent au plus ancien avec UUID comme second critère ; les commerces de la
vue Reversements par nom puis UUID. Le libellé du filtre précise la date et le
fuseau utilisés : événement, création du paiement, ou périmètre de reversement
(bornes UTC historiques explicitement affichées, voir le contrat).
Les listes ne sont pas rafraîchies automatiquement en arrière-plan ; « Actualiser »
relit sans écriture. Chaque résultat affiche sa date de lecture.

Pendant le chargement, les contrôles concernés sont occupés et le bouton de
relecture désactivé. Une requête devenue obsolète après filtre/navigation/session
ne remplace pas l’état courant. Après erreur, un ancien résultat peut rester
visible avec « Données non actualisées » ; l’erreur ne devient pas une liste vide.
Une expiration de session efface les données sensibles et utilise la reconnexion
ERP. Le changement de compte annule toute requête et réinitialise les résultats.

## Audit — E65-CA-02

Colonnes initiales : date/heure, action, phase, acteur, ressource. Recherche sur
références, action et corrélation ; filtres avancés acteur, phase, type/identifiant
de ressource, référence métier, identifiant de requête. L’API applique tous les
filtres avant pagination ; un événement ancien ne disparaît pas parce que 200
autres événements plus récents ont été collectés.

Le détail présente les identifiants, le contexte métier et les métadonnées
autorisées sous forme de texte échappé. Une phase inconnue garde sa valeur
assainie ; elle n’est pas traduite arbitrairement en succès ou échec. L’acteur
manquant est « Non renseigné », jamais l’administrateur qui consulte.

Les liens vers achat, commerce ou instance sont construits depuis des types
et identifiants reconnus. Un chemin HTTP enregistré ou une URL de métadonnée
n’est jamais utilisé comme destination libre. Secrets, cookies, jetons, QR,
charges utiles prestataire et coordonnées bancaires complètes restent exclus.
La V1 n’expose pas IP, user-agent ni identifiant de session d’authentification.
Les métadonnées sont limitées à une liste positive de champs documentés à
l’implémentation (codes, identifiants métier, versions, compteurs, champs modifiés) ;
pas de bouton « JSON brut ». Les valeurs libres sont bornées et assainies.

## Paiements — E65-CA-03, 04

Colonnes initiales : création, référence du paiement, achat/commande, origine,
payeur masqué, montant/devise, état du paiement, disponibilité des données financières.
Le filtre d’état utilise la normalisation existante (succès, en attente, échec,
expiré, inconnu), tout en conservant l’état source dans le détail.

Le détail sépare trois zones :

1. **Paiement** : montant, devise, état, date de création, achat/commande source.
2. **Données financières** : frais Stripe, net, commission brute et commission
   nette estimée ; état/date de synchronisation et incident assaini. Une valeur
   inconnue est indiquée comme telle, jamais remplacée par zéro.
3. **Pièces et facturation** : achats enfants concernés et liens vers leurs
   dossiers de traces, documents effectivement disponibles et demandes existantes.
   Une trace seule est libellée « Trace disponible, téléchargement indisponible » ;
   une erreur de lecture n'est pas une absence de pièce. Aucun reçu, facture ou remboursement n’est
   généré au chargement ; les anciennes routes supprimées, dont `pack.zip`, ne
   sont pas proposées.

L’API n’invente pas de `paidAt` : un horodatage d’achat éventuellement disponible
est présenté comme tel, avec sa provenance, sans être attribué à chaque tentative.
Plusieurs tentatives d’une même commande restent des paiements distincts. Un
résultat ambigu comportant plusieurs succès n’est ni fusionné ni masqué ; le
dossier achat conserve son diagnostic. La synthèse est intitulée « Paiements
enregistrés », pas « Chiffre d’affaires ».

Les remboursements sont accessibles via le dossier achat et peuvent concerner
plusieurs lignes ; ils ne sont pas retranchés d’un paiement par estimation. La
V1 ne calcule pas de total remboursé par paiement sans rattachement canonique.
Les filtres de période portent sur la création des paiements, et la synthèse
porte sur l’intégralité de ces mêmes paiements, par devise et état normalisé.

## Reversements — E65-CA-05, 06

La vue présente période/campagne, synthèse et liste **par commerçant**, comme le
suivi 360 existant. Ouvrir un commerce présente ses mouvements, reversements et
paiements ; chaque reversement possède aussi un détail avec URL propre. Le filtre
par commerçant est conservé avec la recherche. Les mouvements à reverser sans
reversement associé restent visibles sous « À préparer » ; ils ne sont pas
fabriqués comme reversements virtuels. Leur montant reste distinct des reversements
déjà constitués. Le filtre de statut, s’il est utilisé, nomme explicitement son
objet ; aucun statut universel ne mélange mouvement, reversement et virement.

La synthèse distingue à préparer, en cours, transféré et échec
selon les règles de lecture existantes à partager. Les montants sont regroupés
par devise ; les inconnus et données incomplètes ont leurs compteurs propres.
La période est un filtre de lecture, pas une nouvelle campagne persistée.

Le détail fournit composition complète et paginée, commerçant, paiements de
reversement et tentatives, anomalies, références sources et progression bancaire.
Les mouvements appartenant au reversement restent visibles même hors période ;
ils sont signalés dans le détail et ne sont pas comptés deux fois dans la synthèse.

« Transféré » signifie fonds arrivés sur le solde Stripe du commerçant ; il ne
signifie pas « Reçu en banque ». Le suivi bancaire garde état Stripe et état de
rapprochement distincts, réutilise le domaine Payout existant et indique les
associations indisponibles. Un payout groupé affiche son périmètre réel, pas son
montant total comme paiement individuel du reversement. Plusieurs tentatives
de virement et un échec tardif restent visibles.

« Ouvrir la console de traitement » mène à l’écran financier existant avec ses
filtres compatibles. Ce lien ne déclenche pas sa campagne, son export ou sa
réconciliation. Les actions restent explicites dans cet écran ; leur présence
ne justifie aucun nouveau POST dans les trois vues de consultation.

## Préparation de l’implémentation

La V1.3 complète les contrats et les preuves, sans changer les dix critères ni
ouvrir de nouveaux droits. Le découpage suivant permet de livrer des vues
complètes et de garder explicites les dépendances :

| Lot | Périmètre et résultat vérifiable | Condition de préparation |
| --- | --- | --- |
| E65-L01 | Navigation ADMIN, chaîne de session, Audit liste/détail, filtres, pagination et occultation | Indépendant de H01/H02 et des nouveaux profils E69 ; tests CA-01/02/07/08/09/10 prévus |
| E65-L02 | Paiements d'achats/commandes, parité Vision 360, synthèses par devise et pièces disponibles | Contrats décrits pour H01, avec liens existants selon H02 ; aucune souscription agrégée ou commande supplémentaire déduite de l'absence de réponse |
| E65-L03 | Projection commune ERP/360 des reversements, sources et couverture bancaire | Politique de lecture partagée, compte de destination historique et devises normalisées ; tests CA-05/06 et non-régression de la console |

L01/L02/L03 sont implémentés dans le périmètre ADMIN ; H01/H02 ont été confirmés
le 1er octobre. Leur validation et les limites restantes sont suivies dans le bilan.
L'EPIC 69 n'est pas incluse dans ces lots. Les plans SQL sont examinés sur
base jetable, sans en déduire une capacité de production ou un index nécessaire.
La couverture des modèles de souscription et l'intégration d'actions nouvelles
restent des extensions à spécifier si elles sont retenues.

Le [bilan de validation](verification-livraison.md#bilan-dimplementation-v14)
porte les tests réellement exécutés, les revues, les captures et les limites.
La disponibilité sur un environnement réel dépend d'une livraison distincte.
