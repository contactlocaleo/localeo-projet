# Localeo Atelier — Domaine, données et transaction

[Spécification V1 et décisions](README.md) · [Contrats](contrats.md)

## Responsabilités

Conception conforme à l'[ADR domaine d'abord](../../architecture/decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md).
Le domaine **commercialisation** porte la préparation, la cohérence du retour et
la création du coffret. Référencement fournit les faits des commerçants/modèles ;
identité/accès fournit les capacités et communes autorisées ; DAM possède les médias.
La conformité BUM et les règles financières existantes restent leurs propriétaires.

| Élément | Responsabilité et opérations |
| --- | --- |
| Préparation persistée et règles pures de préparation | UUID, commune, paramètres opérateur, sélection versionnée, contexte émis, proposition validée, état, version et résultat. Les commandes orchestrent modifier, émettre un contexte, accepter une proposition, retoucher, marquer créée, en appliquant les règles du domaine. |
| Sélection normalisée | 1..20 modèles distincts pour émission/import/création ; références/version, commune unique, absence de libellés incompatibles et ordre complet. Un enregistrement incomplet peut avoir 0 sélection. |
| Proposition éditoriale normalisée | Nom/accroche/description, ordre et texte alternatif, référence du média validé, limites du contrat, absence de champs de commande. Le base64 appartient au transport et n'est pas conservé dans cette valeur. |
| Service de domaine pur de préparation | Compare contexte courant et émis ; exige ensemble exact, mêmes versions et faits applicables ; réutilise les règles d'éligibilité et budget de l'Atelier. |
| Politique média Atelier | Décide à partir des faits certifiés par l'adaptateur : image active, WebP décodable, taille réelle < 150 000, quota et accès. Le domaine ne décode pas d'octets et n'appelle pas le DAM. |
| Coffret et prestations existants | Conservent états, copies/version, budget et qualification. Une opération explicite de rattachement en brouillon protège le statut cible sans modifier les autres usages d'Atelier. |

L'application charge les faits et autorisations, ouvre l'UoW, obtient les verrous,
appelle le domaine, persiste et audite. Les repositories traduisent les modèles
persistés. Les routes valident le transport et présentent les refus. Aucune règle
de composition nouvelle ne doit être recopiée dans JavaScript, SQLAdmin ou l'API.

Les règles pures sont portées par
[`preparation_coffret_assiste.py`](../../../../localeo-backend/app/domaine/commercialisation/services/preparation_coffret_assiste.py).
`ServiceAtelierAssiste` orchestre les snapshots et la session transactionnelle ;
la composition réutilise `ServiceAtelierErp.rattacher_en_brouillon` avec un ordre
explicite. Le rattachement ERP historique conserve son comportement. Les modèles
de préparation sont dans `atelier_assiste_models.py` ; il ne s'agit pas de nouveaux
agrégats objet nommés `SelectionPrestations` ou `PropositionEditoriale`.

```mermaid
flowchart LR
    ERP["Localeo Atelier / ERP"] --> API["API interne commercialisation"]
    API --> UC["Cas d'usage + transaction"]
    UC --> DOM["Préparation + règles Atelier"]
    UC --> SOURCES["Ports référentiel et modèles"]
    UC --> DAM["Port médias"]
    UC --> DB["Repositories et UoW"]
    ERP -->|"copie manuelle"| IA["IA externe choisie par l'opérateur"]
    IA -->|"réponse collée"| ERP
    DB --> COFFRET["Coffret et prestations BROUILLON"]
```

## Invariants et états

| Référence | Invariant | Entrées et preuves liées |
| --- | --- | --- |
| E66-I01 | Droits ERP et commune recontrôlés à chaque consultation/commande, avant même un rejeu. Être auteur ne donne aucun droit persistant. | Liste, détail, prompt, import, média, création ; CA-01/11. |
| E66-I02 | Exactement tous les modèles sélectionnés, une fois, dans leur version acceptée, issus de la commune. Budget et éligibilité partagés avec l'ERP. | Sauvegarde, prompt, import, retouche et création ; CA-02/05/09. |
| E66-I03 | Une proposition appartient au contexte serveur courant de cette préparation ; un identifiant recopié par l'IA n'est ni un secret ni une autorisation. | Import puis création ; CA-03/04/09. |
| E66-I04 | L'IA ne fournit aucun montant, droit, statut, validation fiscale, URL à télécharger ou modification de source. | Schéma fermé et domaine ; CA-03/05/10. |
| E66-I05 | L'image base64 est décodée strictement et conforme au format/poids réel/accès ; import de la proposition et du média atomique, conformité recontrôlée à la création. | Import, dépôt de remplacement, bibliothèque, rattachement final ; CA-04/05/06. |
| E66-I06 | Une préparation ne produit qu'un coffret, atomiquement, pour tous acteurs/clés et sans expiration de cette garantie. | Transaction et contrainte durable ; CA-07/08. |
| E66-I07 | Coffret et toutes copies/snapshots initiaux sont BROUILLON ; origine IA sans exemption de publication. | Composition et diagnostic ; CA-07/10. |

États persistés :

| État | Opérations permises | Transition |
| --- | --- | --- |
| `BROUILLON` | Sauvegarder une préparation incomplète ou valide ; aucun dépôt/sélection de remplacement avant import complet | Émission valide → `PROMPT_DISPONIBLE`. |
| `PROMPT_DISPONIBLE` | Relire/copier le contexte courant ; importer une réponse | Import valide → `APERCU_VALIDE`. Changement de contexte → `BROUILLON`. |
| `APERCU_VALIDE` | Retoucher les champs éditoriaux, l'ordre ou l'image ; confirmer création ; remplacer le retour sous le même contexte | Création réussie → `CREEE`. Changement de contexte → `BROUILLON` et proposition invalidée. |
| `CREEE` | Consulter le résultat et ouvrir le dossier ERP selon droits actuels | Terminal pour l'assemblage ; aucune nouvelle création ou retouche de préparation. Contenu préparatoire nettoyable après 30 jours, résultat durable conservé. |
| `EXPIREE` | Aucune reprise ni création | Préparation non créée arrivée au terme des 30 jours ; identifiant jamais réutilisé. |

L'import valide le JSON, le contexte et la sélection puis décode le base64 dans
l'adaptateur sous les bornes de transport. L'image doit être un WebP valide de
1..149 999 octets. L'application persiste asset DAM, proposition normalisée,
référence/checksum et `media_contexte_id` dans une seule transaction. L'import
réutilise quota, limitation de débit et protection idempotente du DAM ; aucun
stockage de la chaîne base64 ou du body brut dans la préparation, les audits ou
le registre de résultats HTTP. Un remplacement sous une nouvelle clé ne duplique
pas un asset de même checksum déjà associé à cette préparation ; ne pas révéler
l'existence d'un asset d'un autre périmètre par une déduplication globale.

Un import refusé ne modifie ni la préparation ni le DAM ; l'ancienne proposition éventuelle
reste stockée et explicitement identifiable comme telle. L'interface ne présente
jamais la réponse refusée comme acceptée. Une source devenue obsolète produit un
blocage dérivé, visible en lecture sans mutation ; pour poursuivre, recharger les
faits et réémettre un contexte par commande. Aucun GET ne crée de coffret, contexte
ou document ; la journalisation de consultation autorisée reste possible.

### Contexte et concurrence

`version` est un entier croissant sur toute mutation de préparation. Chaque commande
reçoit `expected_version`. Un conflit renvoie 409 et la version courante accessible,
sans écrasement. `contexte_id` est un UUID généré côté serveur lors de l'émission ;
le serveur conserve une empreinte SHA-256 du contexte normalisé : commune, paramètres
opérateur, intention, références/versions et faits sources utiles.

Les faits comprennent les textes publics réellement inclus, commerçant et commune,
statuts, version des modèles, montants du calcul interne, situation d'éligibilité
et configuration de contrôle applicable. L'empreinte inclut les faits internes
nécessaires sans les exporter vers l'IA. Une évolution d'éligibilité ou de contenu
invalide l'import même si l'ancien numéro de modèle n'a pas changé. Ignorer les
timestamps sans effet métier. À l'import et à la création, relire/recalculer cette
empreinte sous les verrous nécessaires ; ne pas croire un hash fourni par le client.

Retoucher des textes ou changer d'image incrémente la version et modifie le contenu
confirmé sans changer `contexte_id`. Émettre un nouveau contexte invalide la réponse
précédente et sa confirmation d'image (`media_contexte_id`), même pour la même
sélection. L'import valide associe l'image décodée au nouveau contexte ; une
sélection/confirmation volontaire de remplacement fait de même. Un double clic avec la même clé rejoue
l'émission déjà réussie et ne crée pas un contexte différent.

## Création atomique et reprise

1. Authentifier, vérifier droit de mutation et commune, CSRF et clé d'idempotence.
2. Réutiliser la sérialisation ERP par acteur puis verrouiller la préparation.
   L'ordre de verrouillage de toutes les entrées doit être documenté et commun.
3. Si un résultat existe pour la même version confirmée, vérifier l'accès au coffret
   courant et renvoyer ce résultat. Ne pas revalider les anciennes sources d'un
   assemblage déjà réussi. Une autre version demandée donne un conflit.
4. Sinon exiger `APERCU_VALIDE` et la version attendue. Verrouiller modèles et
   commerçants dans un ordre d'identifiants stable, puis leurs faits d'éligibilité
   et le média retenu ; recontrôler contexte, références, budget et droits.
5. Créer le coffret BROUILLON avec les paramètres opérateur et textes validés.
   Copier chaque modèle avec **statut cible BROUILLON** et snapshot version 1,
   enregistrer le rattachement et l'ordre. Conserver les montants de la source.
   Les brouillons réservent déjà leur budget dans le calcul ERP courant.
6. Lier la préparation au coffret, enregistrer résultat final, version confirmée,
   acteur et audit ; effectuer **un seul commit**. Une erreur à n'importe quelle
   étape annule toutes ces écritures, y compris copies/snapshots et résultat.

Ne pas enchaîner les endpoints existants depuis le navigateur : chacun commettrait
une transaction. Réutiliser les services/ports dans une UoW commune et extraire
vers le domaine les règles touchées ; ne pas créer une seconde politique d'Atelier.
Avec les incréments actuels, la version coffret créée vaut `1 + N` après N copies ;
retourner la version effectivement persistée, jamais la version initiale mémorisée.
Un interblocage ou échec transitoire entraîne rollback et reprise de la même commande.

Le registre ERP de 24 h protège les retries HTTP par acteur. Il est complété par
le résultat durable de préparation et son verrou, avec `coffret_id` unique non nul
uniquement à l'état CREEE. Après 24 h, une nouvelle clé ou un autre acteur autorisé
retrouve le même coffret. Si le coffret est supprimé ultérieurement par une opération
permise, conserver une trace terminale et renvoyer « Coffret supprimé » (410), jamais
recréer. Une purge de contenu doit conserver le marqueur de création et la version
confirmée ; les identifiants supprimés ne sont jamais réutilisés.

## Persistance cible et compatibilité

### Conservation de 30 jours — E66-D05 / E66-CA-11

L'échéance se calcule côté serveur en UTC : dernière modification persistée de
la préparation + **30 × 24 heures** (création initiale si jamais modifiée).
Une lecture, un refus, une tentative échouée, un rejeu idempotent ou le nettoyage
ne modifient pas cette date. Afficher l'échéance à l'opérateur. Toute mutation
valide avant expiration recalcule l'échéance ; une préparation expirée ne peut
pas être réactivée par une ancienne requête.

Dès `maintenant >= expires_at`, interdire reprise/import/création d'une préparation
non créée, y compris avant le passage du nettoyage. Contrôler cette condition
avant le registre de rejeu. La préparation devient EXPIREE ; le contenu à nettoyer
comprend intention, sélection, faits/prompt, proposition éditoriale et références
de travail. Conserver seulement une trace minimale d'identifiant/état/échéance et
de périmètre nécessaire au refus d'accès, sans contenu IA. Elle ne réutilise pas l'ID.

Pour CREEE, nettoyer le même contenu préparatoire après 30 jours mais conserver
le lien/résultat minimal, la version confirmée et le marqueur d'unicité durable.
Ne supprimer ni le coffret, ni ses prestations, ni leurs versions ou achats.
Les médias utilisés par un coffret, une autre préparation ou un autre objet DAM
sont conservés. Pour les médias de travail devenus orphelins, effacer les octets
et marquer l'asset `PURGEE` après vérification de toutes les références. Conserver
son identifiant comme sentinelle : une ancienne URI ne doit jamais retrouver un
nouveau contenu. Le trigger v250 verrouille les assets lors du rattachement d'une
référence et refuse un asset `PURGEE`, pour fermer la course entre purge et usage.
Les sentinelles sont terminales, protégées contre UPDATE et DELETE. Les références
métier sont recherchées aussi dans les snapshots JSON et les variantes d'UUID
(canonique, majuscules, hexadécimal compact) ou d'URI encodées. Toute nouvelle table
persistante doit recevoir le trigger : une couverture incomplète fait refuser la
purge, sans effacement partiel. Les verrous d'assets `NOWAIT` et la reprise de la
transaction complète sur SQLSTATE `55P03`, `40P01`, `40001` sont bornés à trois
tentatives. Un média référencé à l'échéance quitte le suivi temporaire Atelier et
reste un asset DAM durable ; sa libération ultérieure ne déclenche aucune purge
Atelier. Cette conservation n'est pas un ramasse-miettes global du DAM.

Le nettoyage automatique rejoint l'ordonnancement existant, par lots bornés,
avec simulation `dry_run`, audit de compteurs sans contenu et reprise idempotente.
Le batch `commercialisation.atelier.conserver` est planifié chaque jour à 04:00 UTC,
avec une limite de 100 préparations par défaut. L'accès est déjà bloqué à l'échéance, la suppression
physique a lieu au prochain passage réussi. Superviser le retard de nettoyage.
Sous verrou de préparation, recalculer l'échéance avant purge : une sauvegarde
concurrente valide ne doit pas être effacée ; une création déjà réussie conserve
toujours son résultat. Ne pas présenter le nettoyage de la base active comme
l'effacement des sauvegardes, qui suivent la politique d'exploitation existante.

Migration **additive**
[`v250_localeo_atelier.sql`](../../../../localeo-backend/sql/v250_localeo_atelier.sql),
sans modification des SQL historiques. Son existence dans le dépôt ne signifie
pas qu'elle a été appliquée sur les environnements déployés. Le contrôle de schéma
exige les nouvelles tables et colonnes, même lorsque la fonctionnalité est désactivée :

- `preparations_coffret_assiste` : UUID, `ville_id`, `etat`, `version`, acteur/date de
  création/modification, `expires_at` et date de nettoyage, type/prix/validité/intention, sélection ordonnée et versions,
  contexte UUID/empreinte/version du schéma, faits émis autorisés, proposition normalisée,
  `media_id`/checksum/`media_contexte_id`, résultat coffret et version confirmée. Références relationnelles
  aux ressources stables ; snapshots bornés pour contexte et proposition. Index
  `(ville_id, updated_at, id)` pour listes, contrainte d'unicité du résultat.
- `medias_preparation_atelier` : liens préparation/asset et checksum, avec unicité
  par préparation et empreinte. Ils portent la provenance et la déduplication
  locale ; la conservation vérifie les autres usages avant de purger les octets.
- `coffrets` : `accroche` (160), `description` (4 000), `image_alt` (180), nullables,
  limites également portées par les objets-valeur et API. Le nom reste `nom` (200),
  l'image reste `image_uri` dérivée du média. Aucun alias avec les textes BUM.
- `prestations_coffret` : `ordre_presentation` positif nullable. Ordres non nuls
  uniques par coffret ; les créations Atelier affectent 1..N. Les anciennes lignes
  restent nulles, sans changement des textes, prix, statuts ou achats.
- Étendre entités, mappers, repositories, commandes de modification/détail ERP et
  projections publiques. Modifier uniquement les champs fournis : une ancienne
  commande ne doit pas effacer l'accroche/description/alt/ordre nouvellement persistés.

Tri canonique pour les nouvelles compositions : positions explicites croissantes,
puis lignes sans position triées par libellé et UUID. Une prestation ajoutée ensuite
via le dossier ERP prend la dernière position lorsque le coffret utilise déjà ce
mode ; suppression laisse un trou sans changer l'ordre relatif. Pour les coffrets
sans position, conserver le comportement de tri existant de chaque lecteur ; ne
pas réordonner des achats historiques. Toute commande de réordonnancement valide
l'ensemble complet et la version coffret. L'ordre ne change pas la consommation.

La préparation conserve les textes et références du média validé, jamais le base64.
Les photos ne sont pas copiées en base de préparation : réutiliser les références
DAM. Quota, contrôle de flux et stockage des octets restent au DAM. Une référence
libre `image_uri` ne remplace pas un média autorisé dans la commande Atelier.

### Médias

La bibliothèque actuelle n'encode pas un droit territorial par média. V1 : ADMIN
peut choisir les médias actifs du DAM ; EXPLOITATION choisit ceux déposés et liés
à une préparation d'une commune qui lui est actuellement autorisée. Ne pas ouvrir
tout le DAM à un profil limité. Une sélection d'UUID direct applique le même filtre.
Tracer provenance et commune du dépôt dans les données de préparation, pas seulement
dans un libellé de fichier. Les autres parcours DAM conservent leurs droits.

Le contrôle de signature existant ne suffit pas à garantir un WebP valide. L'adaptateur
doit vérifier le décodage, les dimensions et la taille réellement lue, avec limites
de ressources (V1 : image statique, maximum 16 millions de pixels et 8 192 pixels
par côté). Ces bornes de sûreté ne prescrivent aucun ratio créatif. Le texte
alternatif décrit l'image effectivement choisie ; l'opérateur peut corriger celui
proposé avant d'enregistrer. Dépôt refusé : aucun asset ; échec de création : un
asset déjà déposé reste attaché à sa préparation, sans doublon ni suppression globale.

## Effets et frontière fiscale

Création/retouche émet uniquement les audits internes prévus. Pas d'email, paiement,
appel IA, publication ou webhook externe. Les audits portent acteur, IDs, opération,
versions et code résultat ; aucun texte collé, prompt complet, jeton ou texte privé.
L'édition de la promesse garantie et la qualification BUM restent explicites dans
les services existants. Les descriptions éditoriales ne doivent jamais remplacer
les mentions contractuelles dans le panier, le reçu ou les droits du bénéficiaire.
La vérité factuelle du texte reste soumise à la relecture humaine avant création
et à la préparation habituelle avant publication.
