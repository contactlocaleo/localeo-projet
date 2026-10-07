# Conservation des accès et validations — rattachement E70/E72

Version du **7 octobre 2026**, référence **E70-E72-CONSERVATION-20261007**.
Ce document précise le rattachement des nouvelles données aux règles existantes
pour [E70](../epic-70-validation-pin/README.md) et E72 (spécification publiée avec E72).
Il complète leurs architectures et matrices de preuves ; il ne remplace pas le
registre juridique et n'annonce ni purge exécutée ni batch déjà livré.

## 1. Source vérifiée et portée

Source : [Annexe A — registre des traitements et règles de conservation, V1.0 du
13 septembre 2026](<../../juridique/interne/Annexe A - Registre simplifié des traitements et tableau de conservation des données - V1.pdf>).
Le PDF de six pages a été extrait le 7 octobre en lecture seule, avec Node :
décompression des flux Flate et décodage des glyphes par leurs tables ToUnicode.
Les positions des textes distinguent les trois colonnes catégorie, usage et archive.
Aucun PDF n'a été modifié, aucun chiffre n'est déduit du seul DCT Animation.

Empreinte SHA-256 du PDF lu :
`09d55b5d06ed23b7926071faf0bb09728d52dd7c3044dbcea3ddcdc1370551f0`.

| Page / rubrique source | Règle existante utilisée |
| --- | --- |
| p. 1, T1 ; p. 2, T5 et T8 | Accès/habilitations ; consultation/consommation avec validateur, dates et incidents ; sécurité/audit. Le périmètre inclut les utilisateurs professionnels, pas seulement Animation. |
| p. 3, comptes et habilitations professionnels | Usage pendant la relation et l'habilitation ; retrait des droits à leur fin ; seuls les éléments utiles à la preuve sont archivés cinq ans après la fin de la relation. |
| p. 3, sessions et secrets techniques | Usage pendant la validité, révocation possible ; suppression des secrets devenus inutiles ; événements de sécurité selon T8, sans secrets bruts. |
| p. 4, liens de consultation | Marqueur d'utilisation maintenu au moins jusqu'à l'expiration du code et de la session, puis retrait des données techniques inutiles ; preuve de révocation selon sa finalité. |
| p. 4, commandes, droits et consommations | Usage pendant l'exécution et la validité du coffret ; preuves nécessaires cinq ans après la fin de la relation ou l'événement à établir ; pièces comptables distinctes. |
| p. 4, pièces comptables et références Stripe | Dix ans après clôture de l'exercice pour les pièces comptables ; ne pas étendre cette durée à tous les détails de validation, messages ou secrets. |
| p. 5, journaux de sécurité ordinaires | Douze mois au maximum ; seuls les éléments nécessaires d'un incident ou litige sont isolés pour une durée justifiée ; autres journaux supprimés. |
| p. 6, archivage, suppression et gel | Archive à accès limité, distincte de l'usage courant ; gel limité, justifié, avec périmètre/responsable/terme ; suppression normale après levée ; restauration réappliquant les suppressions et révocations dues. |

Le [DCT E41 §22](../epic-41-api/dct.md) contient un ancien délai de 24 mois pour
l'audit sécurité Animation. **Ce délai n'est pas repris pour les journaux ordinaires
E70/E72** : le rattachement est T8 et le plafond de 12 mois de l'Annexe A, pas une
extension implicite du DCT. Cette lecture ne réécrit pas toute la politique ou les
purges historiques Animation ; les éventuels écarts de ce périmètre restent distincts.

## 2. Catégories cibles, dates et données minimales

Le classement dépend de la **finalité de la donnée**, pas du nom de sa table ni du
canal QR/PIN. Une même action peut produire une preuve métier et un journal technique
différents ; elle ne justifie pas deux copies complètes conservées au délai le plus long.

| Catégorie cible | Données E70/E72 | Départ et durée de référence | Traitement attendu |
| --- | --- | --- | --- |
| `SECURITE_ORDINAIRE` (T8) | Échecs PIN, blocages/déblocages, authentification/refus, reauthentification, diagnostics de reset, audit technique de commandes d'accès et option ERP | Date serveur de l'événement ; échéance au plus tard +12 mois calendaires. Un délai opérationnel existant plus court reste applicable. Lecture/export ne repousse pas cette date. | Retirer du stockage courant et des copies/logs gérés au plafond ; extraire préalablement les seuls éléments d'un incident justifié. Jamais PIN, mot de passe, bearer, jeton ou vérificateur. |
| `PREUVE_CONSOMMATION_COFFRET` (T5) | Occurrence de validation, cible/coffret/droit, commerce, acteur professionnel minimal, mode, date, résultat acquis et références aux effets métier | Pour la preuve de la consommation, l'événement à établir est `validated_at` : échéance d'archive +5 ans. Les preuves de fin de relation utilisent leur date propre, sans report artificiel par une consultation ou un changement de PIN. | Conserver seulement la preuve nécessaire. À fin d'usage courant du coffret, la soustraire aux listes opérationnelles puis l'archiver avec droits restreints. Pas de prolongation du jeton ou du reçu public. |
| `PREUVE_HABILITATION` (T1) | Attribution/retrait du droit salarié ou du droit principal d'intervenir, acceptation et relation compte-commerce utiles pour expliquer une validation | Pendant relation/habilitation ; preuves utiles +5 ans depuis la fin de la relation correspondante, datée et sourcée. | Retirer les droits dès leur fin. Extraire ID acteur, commerce, rôle/périmètre, dates de début/fin, auteur et motif sûr ; pas tout le compte, ses sessions ou son mot de passe. |
| `SECRET_TECHNIQUE` (T1) | Vérificateur PIN/version, hash de lien invitation/reset, secret de session, charge chiffrée de remise | Validités E70/E72 : PIN 1..30 jours, invitation 24 h, reset 1 h, session selon contrat ; révocation anticipée possible. | Rendre inutilisable immédiatement à échéance/révocation ; supprimer la matière secrète dès qu'inutile. Garder un marqueur non authentifiant tant que nécessaire à l'anti-rejeu, puis seulement l'événement classé T8/T1. Aucun report à 12 mois ou 5 ans du secret. |
| `ETAT_ESSAIS_PIN` | Timestamps utilisés par la fenêtre glissante, compteur et `blocked_until` | Fenêtre de 15 minutes et blocage de 15 minutes de l'architecture E70 | Retirer les timestamps hors fenêtre et le blocage échu ; l'événement d'échec/blocage minimal suit T8. Ne pas transformer le compteur en deuxième journal durable. |
| `DEMANDE_TECHNIQUE_VALIDATION` | Demande de 5 minutes, versions, contexte transitoire, clé d'idempotence et liaison au résultat | Fin de l'opération, expiration ou annulation ; aucune durée probatoire générale pour le corps complet | Après fin, ne garder que le marqueur/liaison nécessaire à la reprise et au non-rejeu. Succès : reçu minimal lié à la preuve T5, sous droit client courant ; refus/abandon : événement T8 utile, puis retrait du contexte inutile. Pas d'archive automatique de cinq ans de toutes les demandes. |
| `PREUVE_INCIDENT` (T6/T8) | Sous-ensemble justifié de journaux et de pièces pour fraude/litige/demande d'autorité | Date/terme du dossier et durée justifiée consignés ; pas une durée automatique pour tous les événements | Archive isolée, justification, responsable et terme obligatoires ; recontrôle au terme et suppression due après levée, sans réactiver un accès. |
| `PIECE_COMPTABLE` | Facture, avoir ou pièce de rapprochement existante, liée à une validation | Clôture de l'exercice +10 ans selon la catégorie de l'Annexe A | Garder la pièce et ses références probatoires nécessaires dans le circuit comptable ; ne pas conserver un compte salarié complet ou des logs PIN à ce titre. |

Les périodes de 12 mois et de 5 ans sont calendaires, calculées en UTC depuis la
date métier enregistrée, avec rabattement au dernier jour du mois si nécessaire.
L'échéance est exclusive : `now >= echeance` rend la donnée candidate au traitement.
Le retrait effectif est contrôlé ; un batch en retard ne rallonge pas la politique.

**Fin de relation et identités salariées.** La désactivation de l'option est une
suspension réversible, pas une fin de relation. Une déconnexion, expiration de
session ou rotation du PIN ne sont pas non plus une fin. L'archive d'habilitation
doit recevoir la date effective de fin de la relation d'accès concernée, issue
d'une clôture/retrait documenté ; ne pas substituer silencieusement la fin du
partenariat du commerce à celle du compte. Un enregistrement ancien sans date
requise est signalé pour reprise des données, jamais supprimé sur une date inventée
ni laissé indéfiniment sans responsable de résolution.

**Relation avec l'historique E72.** « Toutes les validations du commerce » concerne
le périmètre métier, pas un accès salarié perpétuel aux archives probatoires. La
liste opérationnelle affiche les validations encore d'usage courant du commerce,
quel que soit leur acteur/mode. L'archive n'est accessible qu'aux personnes habilitées
au besoin de preuve, selon les droits internes existants ; aucun accès Finance ou
audit global n'est accordé au salarié par cette conservation. Une preuve isolée
est minimisée ; un UUID encore réidentifiable n'est pas déclaré anonymisé.

## 3. Notifications et Animation : circuits distincts

- Les notifications commerçantes suivent le [registre Animation du 19 septembre](../../juridique/interne/registre-interne-moteur-animation-2026-09-19.md),
  catégorie notifications Animation **et commerçantes** : 12 mois calendaires depuis
  création, sauf preuve d'envoi nécessaire isolée. La nouvelle collection PIN de Pro
  est rattachée à cette finalité commerçante, même si son stockage est séparé.
- Les alertes de sécurité PIN restent aussi soumises au plafond T8 : une copie de
  notification ne doit pas servir à conserver un journal plus longtemps.
- Les reçus d'attestation Animation gardent fin effective +90 jours et les catégories
  de preuve de gains leurs règles existantes. La preuve Coffret n'est pas un reçu
  Animation ; 90 jours ne devient pas une durée de validation Coffret.
- Les informations techniques de distribution WebPush/email suivent leurs politiques
  plus courtes existantes ; le délai de la notification visible ne les prolonge pas.

## 4. Domaine, traitements et sécurité de la purge

`identite_acces` porte l'expiration et révocation des accès, la finalité des preuves
d'habilitation et la politique pure de conservation T1/T8. `exploitation` porte la
preuve T5 et sa transition usage courant/archivage. La comptabilité et Animation
conservent leurs propriétaires. L'application orchestre simulation, relecture sous
verrou, suppression, export d'archive minimal et rapport ; les adaptateurs traitent
tables, fichiers de journalisation, emails et copies. Les routes/ERP/batch ne calculent
pas chacun leur propre délai.

Contrat de décision cible : catégorie, date de référence sourcée, échéance, état
d'usage, références probatoires nécessaires, gel actif et résultat
`CONSERVER_USAGE / ARCHIVER_MINIMAL / SUPPRIMER / EXCLURE_GEL / DATE_MANQUANTE`.
Une référence financière ne bloque que les champs nécessaires à sa preuve, pas
l'intégralité des données d'authentification. Les secrets ne sont pas archivés
pour « préserver le lien » : remplacer les dépendances par des IDs non authentifiants.

Avant suppression, contrôler les clés étrangères et liens validation → mouvement,
feedback, preuve, reçu, session et acteur. La révocation ne supprime pas la preuve
de consommation. L'archivage/suppression des sessions ne doit ni mettre en cascade
les validations ni retirer leur attribution professionnelle minimale.

Les journaux d'audit SQL et JSONL peuvent être chaînés : ne pas supprimer ou réécrire
une ligne au milieu d'une chaîne comme s'il s'agissait d'une table sans dépendance.
Prévoir un format/une migration d'archives segmentées par finalité et échéance,
avec vérification de l'intégrité et des transitions avant retrait des segments
échus. Une extraction probatoire ne copie que les événements concernés ; pas de
gel global du journal parce qu'un seul incident existe. Le chaînage ne justifie
pas la conservation illimitée de données personnelles. L'ancien stockage mixte
doit avoir une stratégie de transition testée avant activation des nouvelles traces.

Simulation obligatoire sur données isolées puis dry-run sur la cible autorisée,
rapport avec catégorie, bornes, candidats, archives, suppressions, exclusions,
dates manquantes et erreurs. Reprise idempotente après échec ; aucun secret ou
contenu client dans le rapport. La suppression des copies et la rotation des
sauvegardes suivent le cycle existant ; une restauration réapplique les retraits
dus et révocations avant ouverture au trafic. Aucun délai de sauvegarde nouveau.

## 5. Écarts de réalisation constatés le 7 octobre

Lecture seule du backend ; aucun traitement exécuté :

| Stockage / entrée existante | Constat et travail restant |
| --- | --- |
| [Audit SQL](../../../../localeo-backend/app/infrastructure/persistence/models.py) et [service d'audit](../../../../localeo-backend/app/application/exploitation/services/service_audit.py) | Aucun traitement général de conservation identifié. La voie `enregistrer_dans_uow` écrit le JSONL externe avant le commit SQL : un rollback peut laisser une copie externe. Traiter les deux stockages et les événements orphelins, avec transition vérifiable des chaînes et gels limités. |
| [Purge des sessions commerçants](../../../../localeo-backend/app/application/identite_acces/use_cases/purger_sessions_commercant.py) | Job existant avec délai technique par défaut de 30 jours après expiration/révocation ; détache la FK session de l'audit avant suppression. Ce délai ne définit ni la durée des audits ni celle des habilitations. Vérifier séparément retrait des secrets inutiles et preuves nécessaires ; aucun contrôle de gel identifié dans ce job. |
| [Sessions de consultation Coffret](../../../../localeo-backend/app/infrastructure/persistence/repositories/session_consultation_coffret_repository.py) | Aucun job de purge identifié. La présence du hash sert de mémoire du code utilisé : préserver le marqueur jusqu'à expiration du code et de la session sans prolonger inutilement le secret. |
| Validations Coffret et liens financiers | Aucun traitement dédié identifié. Email actuellement obligatoire, liens feedback/secours/fiscalité/reversements et unicité de transaction : prévoir une migration permettant minimisation et maintien de la preuve/idempotence. |

La qualification du départ est une décision de domaine à persister avec sa source :
la date de validation sert à la **preuve de cette consommation**, pas à toutes les
preuves du dossier. La fin de relation n'est pas un champ existant démontré par
cette exploration ; sa reprise doit être explicite pour les données qui en dépendent.
Les règles proposées sont des contrats cibles, pas des capacités déjà disponibles.

## 6. Preuves à produire avant mise en service

Cette matrice complète E70-CA-13/23/26/27/28/33 et E72-CA-15/16/17/21/22,
sans renumérotation ni nouveau statut produit.

| Preuve prévue | Résultat observable attendu |
| --- | --- |
| Horloge avant/à/après +12 mois, année bissextile et changement de fuseau | Journaux ordinaires jamais conservés au-delà du plafond ; lecture/export ne reporte rien |
| Consommation à `validated_at`, échéance +5 ans | Preuve minimale conservée jusqu'à son échéance, retrait usage courant distinct ; refus PIN non classé abusivement comme preuve de consommation |
| Relation d'accès terminée vs option seulement suspendue | Bon départ de l'archive d'habilitation ; absence de date signalée, aucune purge automatique sur date supposée |
| Session, invitation/reset et PIN expirés/révoqués | Aucun secret conservé pour la preuve ; marqueur anti-rejeu non authentifiant ; aucun rejeu rendu possible par la purge |
| Demande réussie, échouée et réponse perdue | Corps technique retiré dès inutile ; reçu minimal relu sous droit courant, pas de deuxième consommation après nettoyage |
| Gel sur un incident, fin de gel, course gel/purge | Seul sous-ensemble justifié isolé ; autres journaux supprimés ; recontrôle atomique et retour au cycle normal à la levée |
| FK validation/mouvement/acteur/session et journal chaîné SQL/JSONL | Pas de cascade détruisant une preuve, pas de chaîne silencieusement corrompue ; contrôle de transition d'archive |
| Historique salarié et archives | Accès salarié aux validations courantes de son commerce ; archive probatoire soumise aux droits distincts, pas de fuite financière |
| Sauvegarde puis restauration et reprise batch | Révocations/suppressions dues réappliquées, erreur visible, reprise sans double effet |

**État au 7 octobre :** rattachement documentaire établi sur la source primaire.
La réalisation et les tests de ces traitements restent des travaux d'implémentation
E70/E72 ; aucun résultat de purge, activation ordonnanceur ou conformité déployée
n'est déduit de la seule lecture de l'Annexe A.


## 7. Réalisation E70 — 7 octobre 2026

Le backend fournit le service de conservation, les migrations 256/257 et le CLI
`python scripts/database/conserver_validations_pin.py` (simulation par défaut).
Les audits métier PIN sont classés avec les audits du canal et écrits dans des
segments JSONL dédiés ; le journal historique demeure inchangé. Les curseurs
persistants évitent qu’un gel ou une date absente bloque les lots suivants. Les
preuves minimales Coffret, reçus Animation et métadonnées de génération suivent
leurs catégories ; aucun secret n’est conservé comme preuve.

18 tests dédiés passent, dont 7 sur PostgreSQL : bornes calendaires, gels et course
avec purge, reprise des lots, intégrité des segments et lectures après archivage.
La conservation des comptes salariés reste du périmètre E72. Les écritures
financières historiques conservent leurs propres politiques ; ce traitement ne
purge pas arbitrairement les tables comptables existantes. L’activation et la
surveillance du job, les copies externes et les restaurations en exploitation
restent des contrôles préalables à la mise en service, sans exécution réelle ici.
