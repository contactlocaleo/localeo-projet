# EPIC 65 — Vues ERP audit, paiements et reversements

## Statut et périmètre

Spécification V1 du **26 septembre 2026**, issue du
[backlog EPIC 65](../../roadmap/a-faire/epic-65-vues-erp-audit-paiements-reversements-backlog.md).
État produit : **À faire**, selon la [roadmap](../../roadmap/README.md).
Ce dossier décrit une cible à implémenter ; aucune route nouvelle, migration
ou recette métier n’est déclarée livrée.

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

| Référence | Décision ou hypothèse | Conséquence |
| --- | --- | --- |
| E65-D01 | Demande acquise : trois vues intégrées à l’ERP, Audit dans Supervision, Paiements et Reversements dans « Paiements et facturation ». | Remplacer les raccourcis vers les listes SQLAdmin pour ces consultations. |
| E65-D02 | Conservation des droits existants : ADMIN exclusivement. | EXPLOITATION reste refusé même avec une session ERP et des communes ; aucune permission nouvelle accordée. |
| E65-H01 | Hypothèse de première livraison, soumise à précision utilisateur : paiements de `PaiementOrm`, achats et commandes d’achat. | Abonnements et commandes de souscription restent dans leurs dossiers existants ; pas d’agrégation de sources financières différentes. Les achats de lots Animation représentés par une commande d’achat sont inclus. |
| E65-H02 | Hypothèse de première livraison, soumise à précision utilisateur : consultation ERP et liens vers les actions financières existantes. | Pas de nouveau formulaire de lancement/reprise de campagne dans ces vues ; les contrôles d’accès et de commande des écrans actuels sont conservés. |
| E65-D03 | Contrainte conservée : lecture sans mutation métier ni appel Stripe. | L’actualisation ne synchronise pas les frais, ne réconcilie rien, ne génère pas de document. |
| E65-D04 | Choix technique : projections paginées, filtrage en base, détails bornés, dates et montants explicites. | Ne pas exposer une liste ORM ni tronquer des données en mémoire à 200 lignes. |

Les deux questions H01/H02 ont été posées pendant la spécification ; leur absence
de réponse ne vaut pas validation. La conception ci-dessous est complète pour
ce périmètre conservateur. Une demande d’agrégation des abonnements ou d’actions
intégrées doit compléter ses contrats avant d’implémenter ces extensions ; elle
n’empêche pas de préparer Audit et les composants de lecture communs.

## Existant vérifié

Lecture du backend `7049de7`, documentation de base `631fd10` avec cadrage local.
Ce constat ne prouve pas l’état déployé.

| Surface | Code existant | Écart à traiter |
| --- | --- | --- |
| Navigation | `app/infrastructure/erp/erp.js`, `app/api/erp_ui.py` | Les trois destinations pointent vers SQLAdmin ; ajouter les pages ERP et leur contrôle ADMIN avant de charger les données. |
| Audit | `EvenementAuditOrm`, repository `EvenementAuditRepositorySqlAlchemy`, `EvenementAuditAdmin` | Lecture seule existante, mais `lister(limit=200)` ne fournit pas une recherche globale filtrée/paginée. Des écritures ORM directes imposent d’assainir aussi les données historiques à la lecture. |
| Paiements | `PaiementOrm`, `PaiementAdmin`, `ServiceVision360Achats._payment_payload` et `.paiements` | Recherche globale paginée absente ; mapping des états/montants et racine achat/commande déjà disponible. `date_creation` n’est pas une date d’encaissement. |
| Reversements | `_build_reversements_360_data`, console `/internal/reversements/vue-360`, API finance | Suivi métier existant, à extraire en projection réutilisable ; le rendu HTML et ses agrégats actuels ne constituent pas un contrat paginé à copier dans l’ERP. |
| Facturation | Documents consultés par achat enfant, dossiers de facturation existants | Aucune relation directe pièce→paiement à inventer ; un achat racine peut avoir plusieurs achats enfants. Générer un reçu est une commande, exclue des lectures. |

Sources applicatives dans le [backend](../../../../localeo-backend/README.md) ;
les correspondances et frontières sont précisées dans l’architecture.

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
   documents et demandes existants. Aucun reçu, facture ou remboursement n’est
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

Audit, navigation ADMIN et composants de lecture peuvent être implémentés selon
ces contrats. Les vues financières sont décrites pour H01/H02, sans traiter ces
hypothèses comme un consentement à étendre les flux. La couverture des modèles
de souscription et l’intégration d’actions supplémentaires nécessitent un
complément si elles sont retenues.

La disponibilité effective dépendra des tests de contrats, d’isolation et des
requêtes sur base jetable, puis de la recette bureau/mobile. Les limites, jeux
et contrôles prévus figurent dans le document de vérification ; aucun résultat
de test applicatif n’est annoncé sur la seule base de cette spécification.
