# EPIC 73 — Dotation, tirages et remise des lots

## Portée et statut

Spécification cible du 17 octobre 2026, **non implémentée par ce document**. Les choix produit restent ceux du [backlog E73](../../roadmap/en-cours/epic-73-animation-et-ou-coffrets-backlog.md), notamment DEC-01 à 03, 07, 10 à 12, 19, 33 à 51. Ce chapitre couvre US01, US02 et US04 à US10 ; les périmètres et droits résiduels sont définis dans [les parcours SaaS](perimetres-parcours-saas.md), les conventions communes dans [l’architecture](architecture-contrats.md), les preuves dans [la vérification de livraison](verification-livraison.md).

Trois branches métier sont distinguées :

| Nature de dotation | Gestion | Produit remis | Effets financiers propres à la dotation |
| --- | --- | --- | --- |
| `COFFRETS` | Circuit Coffrets existant | Instance de coffret et ses droits de prestations | Achat, paiement/réservation, activation et suivi existants |
| `LIBRE` | `EXTERNE` | Lot décrit par l’organisateur, remise déclarée facultative | Aucun achat, activation, commission ou reversement Coffrets |
| `LIBRE` | `NUMERIQUE` | Bon numérique indivisible pour un exemplaire de lot | Aucun achat, activation, commission ou reversement Coffrets |

La souscription Animation et les modules restent distincts de la dotation. Une offre Animation seule permet le parcours libre complet. Une offre Coffrets seule ne requiert aucun abonnement ni onboarding Animation. Le moteur de participation, la qualification et le gel de population ne sont pas remplacés par un moteur de lots.

## Existant vérifié et changements nécessaires

Les liens ci-dessous désignent les producteurs et consommateurs réellement lus ; ils prouvent la structure actuelle, pas la disponibilité des nouvelles fonctions.

| Source actuelle | Fait observé | Conséquence de conception |
| --- | --- | --- |
| [Animation](../../../../localeo-backend/app/domaine/animation_locale/entities/animation.py) | États `BROUILLON`, `CONFIGUREE`, `PUBLIEE`, `EN_COURS`, `CLOTUREE`, `ARCHIVEE`, `ANNULEE` ; configuration versionnée et contrôle des périodes de jeu | Étendre la configuration de dotation ; conserver les contrôles de publication, clôture et jeu. Un brouillon fonctionnel comprend les états techniques BROUILLON/CONFIGUREE avant publication |
| [PopulationEligibleAnimation et TirageAnimation](../../../../localeo-backend/app/domaine/animation_locale/entities/tirage_animation.py) | Population versionnée sans doublon ; `selectionner` refuse si les candidats sont moins nombreux que le nombre demandé de gagnants | Introduire la politique libre `min(lots, candidats)` sans modifier implicitement celle des Coffrets |
| [GainAnimation](../../../../localeo-backend/app/domaine/animation_locale/entities/gain_animation.py) | `coffret_id` obligatoire ; remplacement limité aux gains `A_ENVOYER`/`ECHEC` ; envoi lié à `coffret_instance_id` | Typage des gains et séparation entre attribution, notification et remise ; remplacement libre possible après envoi selon les conditions décidées |
| [ServiceTiragesAnimation](../../../../localeo-backend/app/application/animation_locale/services/tirages_animation.py) | Lots issus de `configuration.parametres.lots[].coffret_id` ; verrou d’animation ; gain envoyé en réservant/activant une instance Coffrets et préparant email/notification Live | Brancher la dotation libre avant tout appel au distributeur Coffrets. Tirage et nouvelle politique pure restent dans le domaine ; application = UoW, repositories, outbox |
| [API Animation](../../../../localeo-backend/app/api/animation_locale_api.py) | DTO `GainAnimationPayload.coffret_id` obligatoire ; commandes tirage/envoi/remplacement avec `Idempotency-Key` | Évolution coordonnée du contrat et de tous les lecteurs ; aucune fausse valeur de coffret pour satisfaire l’ancien DTO |
| [Client API Animation](../../../../localeo-animation/src/app/api.ts), [règles d’affichage des lots](../../../../localeo-animation/src/app/lib/animationLots.ts), [gains](../../../../localeo-animation/src/app/lib/gains.ts) | Types de lots fondés sur coffret, écran de paiement et action d’envoi de gain | Formulaire et récapitulatif discriminés ; aucun paiement Coffrets visible comme prérequis d’une dotation libre |
| [Gain dans Live](../../../../localeo-marketplace/src/live/LiveAnimationGain.jsx) | Texte « Votre coffret », ajout au carnet limité à `/live/coffrets/ajouter` | Nouvelle entrée de carnet de bon, textes et liens par nature ; pas de déguisement en coffret |
| [API PIN](../../../../localeo-backend/app/api/pin_validation_api.py), [orchestration PIN](../../../../localeo-backend/app/application/exploitation/services/validation_pin.py), [demande PIN du domaine](../../../../localeo-backend/app/domaine/exploitation/demande_validation_pin.py) | Types Coffret/Animation, demande de cinq minutes, lecture du résultat et confirmation ; branche binaire dans plusieurs méthodes | Ajouter une branche explicite `BON_LOT` dans les contrats, droits, notifications et effets. Un type inconnu doit être refusé, jamais traité comme une étape Animation |
| [Service QR](../../../../localeo-backend/app/infrastructure/securite/service_qr.py), [scanner salarié](../../../../localeo-commercant/src/features/employees/EmployeeScanner.jsx), [client salarié](../../../../localeo-commercant/src/features/employees/api.js) | Secrets QR vérifiés côté serveur, parcours de confirmation et lecture de reçu ; contrôles de capacité salarié | Réutiliser la surface de scan et le reçu de validation, avec un type de lot distinct et une commande métier commune aux canaux |
| [Composant PIN Live](../../../../localeo-marketplace/src/components/PinValidation.jsx) | États attente/validé/anomalie/expiré/annulé ; résultat incertain relu, PIN non persisté | Étendre le type et le libellé « Remettre ce lot », sans perdre la reprise contrôlée ni annoncer un succès sur erreur réseau |

Les imports d’infrastructure présents dans l’orchestration historique des gains ne constituent pas un modèle à recopier. Les nouvelles règles de dotation, remplacement et consommation seront des objets de domaine purs, testables sans ORM, fournisseur ni horloge globale. Cryptographie, rendu et envoi passent par des ports.

## Responsabilités et invariants

| Propriétaire cible | Responsabilité | Entrées qui doivent appeler la même décision |
| --- | --- | --- |
| `animation_locale.ConfigurationDotation` | Choix explicite, mode unique, durée, ordre des lots, gel | Création/configuration API, portail, ERP, publication |
| `animation_locale.ModeleLotLibre` et `ExemplaireLotLibre` | Description versionnée, commerçant unique, quantité, affectation exclusive | Gestionnaire, ERP, reprise de génération d’exemplaires |
| `animation_locale.AttributionLotLibre` et politique de tirage libre | Population figée, unicité du gagnant, ordre, suppléants, remplacement | Tirage initial, commande de remplacement, retirage explicite |
| `animation_locale.BonLot` | Validité, bénéficiaire, génération de QR, révocation, prolongation, consommation totale et correction | Orchestration de scan Pro, confirmation PIN, corrections gestionnaire/ERP |
| `exploitation` | Demande de validation, reçu, canal, audit terrain | Scan principal/salarié et PIN gagnant |
| `identite_acces` | Sessions, habilitations, capacités de consultation, preuve PIN, limitation | Toutes les routes, ERP et traitements de reprise |

Invariants normatifs :

1. Une animation a une seule branche de dotation ; un choix absent est une erreur de formulaire, pas une valeur par défaut. Le choix et la gestion libre changent uniquement avant publication, sans achat, réservation ni affectation engagée. Le test porte sur les faits persistés, pas sur le seul statut du paiement affiché.
2. Aucun lot libre ne crée de commande Coffrets, de prestation Coffrets ni d’instance fictive. Les paiements de souscription restent possibles et séparés.
3. Un exemplaire appartient à une organisation/commune et à au plus une affectation active. Un bon attribué n’est jamais du stock disponible, même révoqué.
4. Un participant ne reçoit qu’un lot par animation libre, tous modèles confondus. Les anciens gagnants remplacés restent dans la preuve d’attribution et ne sont pas réintroduits par un retirage « non gagnants ».
5. Un exemplaire a au plus un bon courant utilisable. Le remplacement révoque l’ancien avant de rendre le nouveau utilisable, dans la même transaction.
6. Une seule consommation totale active existe pour un bon, quels que soient le canal et le nombre de commandes concurrentes. Une correction annule la consommation active par événement compensatoire, sans effacer la validation.
7. Un principal ou salarié ne remet que les lots du commerce désigné et avec ses habilitations courantes. Un PIN identifie le commerce, pas un salarié supposé. La continuation autorisée après retrait de périmètre ne lève aucune suspension administrative.
8. Le succès d’un email n’est ni la réponse du gagnant ni la remise du lot. Le résultat d’une requête réseau incertaine n’est jamais un succès métier supposé.

## Préparation et publication

Le formulaire commence par « Coffrets » ou « Lots libres », sans présélection. En libre, le second choix obligatoire est « Gestion hors Localeo » ou « Bons numériques Localeo ». Le récapitulatif reprend le choix, la responsabilité de fourniture physique externe et la méthode de remise ; revenir à l’écran précédent ne change pas le mode implicitement.

En gestion externe, chaque ligne porte un libellé, une quantité entière positive, un responsable de remise et les consignes de contact/remise. Le responsable peut être externe : ni compte Pro ni commerce Localeo actif ne sont exigés. La prévisualisation montre autant de positions de gain que d’unités déclarées, ordonnées par le gestionnaire.

En numérique, le gestionnaire habilité crée un modèle de lot puis une quantité d’exemplaires. Un modèle possède un seul commerce de remise habilité Animation, choisi explicitement dans le périmètre autorisé. Il ne peut contenir ni solde fractionné, ni plusieurs commerces, ni plusieurs prestations consommables séparément. Le modèle n’accorde aucun droit avant attribution ; ses exemplaires ont leurs propres identifiants et références. Leur mise à disposition d’une animation est une réservation métier exclusive, pas une vente.

Les champs descriptifs du modèle peuvent évoluer par nouvelle version. Une affectation conserve sa version descriptive ; les informations de dotation publiées et les bons émis ne changent pas silencieusement. Changer le commerce d’un lot déjà engagé n’est pas une édition descriptive : l’action est refusée, les procédures d’incident et de fermeture accompagnée sont utilisées.

La durée commune des bons vaut 90 jours par défaut ; le gestionnaire peut choisir de 1 à 365 jours avant publication. L’ordre des lots, la durée, le mode et les descriptions engagées sont figés par la publication. Les quantités et affectations retenues sont capturées dans cette révision pour empêcher d’ajouter après publication des lots ou un ordre non annoncés. Aucun prélèvement d’exemplaire non disponible ne peut être caché par un calcul local.

La publication libre contrôle les règles communes du moteur, les droits de souscription/type, les participations requises et sa dotation complète. Elle ne consulte pas le statut de paiement d’une commande Coffrets comme condition de succès. La publication Coffrets conserve son parcours financier et ses avertissements existants.

## Modèle de données cible

Noms logiques à mapper dans une migration additive backend ; ils ne prétendent pas être des tables déjà livrées.

| Objet | Attributs structurants et contraintes |
| --- | --- |
| Configuration de dotation | `animation_id`, `revision`, `nature: COFFRETS/LIBRE`, `gestion_libre: EXTERNE/NUMERIQUE/null`, `validite_jours/null`, `published_at`, référence de configuration publiée. Cohérence exclusive entre les trois branches |
| Ligne externe | `id`, organisation, commune, animation, libellé, quantité, responsable, consignes, ordre, version. Pas de référence obligatoire vers un commerce |
| Modèle numérique | `id`, organisation, commune, libellé, description, `commercant_remise_id`, version, auteur/dates ; une version utilisée est conservée |
| Exemplaire numérique | `id`, `modele_id`, version de modèle, référence, état d’affectation, animation affectée, date/auteur, `ever_attribue`, version. Une affectation active au plus ; quantité matérialisée exactement |
| Attribution libre | `id`, animation, tirage, participant, rang de lot, nature, ligne externe + index d’unité OU exemplaire numérique, instant d’attribution, état, ancienne attribution remplacée, motif. Unité de lot exclusive ; index unique animation/participant dans la preuve historique |
| Suppléance | Tirage, participant, rang aléatoire, état disponible/utilisé/inéligible avec motif. Une réservation de suppléant n’est pas encore un gain |
| Contact/remise externe | Attribution, événements de contact/réponse/refus/incident/remise déclarée/correction ; date, acteur, motif. « Non renseigné » reste distinct de « Non remis » |
| Bon numérique | `id`, exemplaire, attribution, instant initial d’attribution, échéance, révocation, génération QR, version ; instant courant du serveur, consommation active et état dérivé |
| Consommation et correction | Bon, validation, commerce, date, mode `QR/PIN`, acteur de scan ou identité PIN, référence de demande/transaction ; correction référant la validation et son motif. Unicité d’une consommation active par bon |
| Livraison d’email | Attribution, type d’email, opération de remise à l’outbox, état transport, première date de succès d’envoi, échecs/reprises. L’identité de l’envoi initial ne change pas au rejeu |

Les projections de gain exposent une union discriminée `nature: COFFRET | LOT_EXTERNE | BON_NUMERIQUE`. Seul `COFFRET` comporte `coffret_id/coffret_instance_id`. Un gain libre a `attribution_id`, une description et un état de remise ; un numérique possède `bon_id`. Aucun UUID nul de substitution et aucun objet Coffrets vide ne représentent un lot libre.

La disponibilité d’un QR ne suffit pas à autoriser une remise : version du QR, attribution courante, commerce, droits, révocation, échéance et consommation sont revérifiés au serveur. Le QR et le droit personnel de consultation sont deux capacités distinctes. Le QR de lot ne devient jamais un jeton de session organisateur ou commerçant.

## Tirage et remplacement

### Tirage initial libre

1. Le gestionnaire consulte les positions de lots figées, le nombre de participants éligibles et le maximum de gagnants possible. Le moteur a clôturé l’animation et gelé sa population avec provenance et version.
2. La confirmation explicite « Confirmer le tirage et les attributions » est la commande définitive. Aucune répétition automatique ne sert à obtenir un autre résultat. L’éventuel aperçu ne tire pas des gagnants provisoires.
3. La politique de domaine choisit `min(nombre_lots, nombre_eligibles)` gagnants distincts aléatoirement. Le premier reçoit la première unité dans l’ordre des lots ; plusieurs exemplaires d’un modèle occupent des positions successives explicites. Les dernières unités restent non attribuées si les candidats manquent.
4. Une permutation ordonnée des éligibles non gagnants constitue la réserve de suppléants, persistée avec le tirage ; elle est paginée à la lecture si nécessaire. Avec zéro candidat, le résultat documente zéro gain et ne déclenche aucun email de gain.
5. Résultat, attributions, bons éventuels et intentions d’emails sont persistés atomiquement. Le worker d’email intervient après commit. Un rejeu rend le même résultat, les mêmes bons et le même ordre de suppléants.

Pour la dotation numérique, la confirmation et son commit revérifient l’habilitation Animation effective de chaque commerce de remise et l’absence de suspension administrative. Une publication antérieure ne suffit pas : DEC-42 ne protège que les bons déjà attribués au retrait du périmètre. Si un commerce a perdu ses droits entre publication et tirage, l’attribution concernée est impossible et la confirmation atomique entière refuse `ATTRIBUTION_COMMERCE_INDISPONIBLE` : aucun tirage confirmé, gain, bon ni email partiel n’est enregistré. Le portail affiche l’incident et conserve la dotation publiée ; il n’exclut pas silencieusement le lot et ne relance pas un tirage. La résolution passe par les commandes habilitées, notamment une réactivation ERP après validation des prérequis, avant une nouvelle confirmation explicite. Un éventuel calcul aléatoire interne à une transaction annulée n’est pas un résultat confirmé présenté au client.

Le générateur aléatoire est un port ; le domaine reçoit son résultat contrôlable en test. Le stockage du tirage permet de prouver la population, l’ordre, les attributions et leur auteur. Il n’est pas nécessaire d’exposer une graine permettant d’anticiper un tirage.

### Volumétrie du tirage

Le [protocole SQL du tirage libre préparé](tirage-libre-protocole.md) précise les bornes, index, reprises et le marqueur de visibilité retenus avant l'implémentation LOT04.

La réserve de suppléants contient potentiellement toute la population non gagnante : le travail total et son stockage sont proportionnels à cette population, même avec un seul lot. Ne pas charger cette population et sa permutation intégralement dans une requête interactive, ni exécuter `ORDER BY random()` sur les participations vivantes comme raccourci. Préparer un résultat privé depuis la population figée/versionnée, en flux ou avec stockage temporaire borné et tri externe adapté, sous une opération durable/idempotente. La méthode conserve une permutation aléatoire sans biais ; la vérification porte sur l’unicité, la population et la reproductibilité de la reprise, sans rendre le tirage prévisible au client.

La préparation ne donne aucun gagnant officiel, bon utilisable, réservation concurrente cachée ou email. Le résultat préparé est scellé et lié à l’opération demandée ; une reprise ne relance pas une sélection pour obtenir un autre résultat. La confirmation finale revérifie versions, droits des commerces et disponibilité des unités. Les lignes préparées ne deviennent des faits métier qu’avec une confirmation atomique identifiée ; tous les lecteurs, workers et commandes doivent exclure les résultats non confirmés. Les réservations/unicités acquises et le marqueur de confirmation sont commités ensemble. Un conflit ne publie aucun résultat partiel.

Documenter le protocole SQL précis de préparation/visibilité et ses index avant implémentation du tirage : la transaction finale ne doit pas réécrire toute la réserve de suppléants. Le coût restant lié au nombre de lots/commerces à valider est mesuré séparément ; une préparation asynchrone ne justifie pas une phase finale sans borne éprouvée. Si l’enveloppe mesurée est dépassée, conserver une opération en attente diagnostiquée jusqu’à traitement adapté, sans tronquer les suppléants, créer un plafond commercial implicite ou laisser une requête HTTP ouverte. La réponse initiale peut être `202` avec ID/état de traitement et consultation bornée ; un reçu « confirmé » exige la fin effective. Ce complément concerne le nouveau tirage libre ; les contrats Coffrets historiques sont conservés tant que leurs consommateurs ne sont pas migrés.

### Remplacement d’un gagnant

Le gestionnaire enregistre une réponse, un refus explicite ou une absence de réponse. Le délai de 14 jours part du premier succès d’envoi de l’email de gain, pas de sa mise en file, de son ouverture ou d’une relance. Une panne d’email ne fait pas commencer ce délai. Une réponse enregistrée invalide le motif « sans réponse » ; un refus explicite documenté permet de remplacer avant le délai.

La commande vérifie : gain courant, lot non remis, motif, délai ou refus, acteur habilité et prochain suppléant encore éligible selon la population figée. Les suppléants sont proposés dans leur ordre ; ignorer un candidat exige une inéligibilité constatée et tracée, pas un choix arbitraire de gagnant. Deux gestionnaires ne peuvent attribuer le même suppléant à deux lots.

En numérique, l’ancien bon est définitivement révoqué, la nouvelle attribution liée à l’ancienne et un nouveau bon créé pour le même exemplaire. La nouvelle durée complète part de cette nouvelle attribution ; le plafond d’une prolongation future est calculé depuis cette nouvelle attribution, sans prolonger l’ancien bon. L’historique de l’exemplaire prouve qu’il ne s’agit pas d’une nouvelle unité de stock.

Le remplacement est une nouvelle attribution : il exige au commit que le commerce soit encore autorisé à recevoir cet engagement. Un droit résiduel de remise sur l’ancien bon ne suffit pas. Si le périmètre a été retiré ou le commerce suspendu, la commande refuse `ATTRIBUTION_COMMERCE_INDISPONIBLE`, conserve l’ancien bon dans son état et ne consomme aucun suppléant. L’incident bloque le remplacement concerné jusqu’à résolution habilitée ; aucun transfert à un autre commerce, retirage ou révocation automatique ne le contourne. La révocation explicite de l’ancien bon reste possible selon ses propres règles, mais n’accorde pas le droit d’en émettre un nouveau.

Si aucun suppléant disponible ne reste, un bouton distinct propose un nouveau tirage parmi les membres éligibles non gagnants de la population figée. Ce tirage supplémentaire est versionné et lié au remplacement demandé ; aucune nouvelle inscription n’y entre. Sans candidat restant, il ne crée ni attribution ni email et rend `AUCUN_CANDIDAT_ELIGIBLE`. La révocation pour lot indisponible reste une commande séparée ; un retirage infructueux ne révoque pas silencieusement un bon.

### Fin des attributions et stock

Après résultat confirmé et fin des attributions, le gestionnaire peut confirmer la libération des exemplaires numériques jamais attribués. La commande montre la liste exacte, leur animation et la quantité libérée. Elle refuse tout exemplaire ayant une attribution, même remplacée ou révoquée. Un nouvel essai concurrent d’affectation ne peut profiter d’un état intermédiaire. Un stock libéré est réutilisable dans une autre animation du périmètre autorisé ; aucune nouvelle édition ne copie les attributions antérieures.

## États et commandes des bons

L’état affiché est dérivé des faits de domaine, avec priorité à la révocation et à la consommation active ; l’expiration ne dépend pas d’un batch ayant déjà tourné. Les instants sont stockés en UTC, reçus en ISO 8601 avec zone et affichés en Europe/Paris. La durée de validité se calcule depuis l’instant d’attribution ; à l’instant d’échéance le bon est expiré.

| État / précondition | Commande | Résultat / refus |
| --- | --- | --- |
| Exemplaire affecté, sans attribution | Tirage confirmé | Bon attribué, échéance attribution + durée figée, QR propre, intention d’email |
| Bon attribué valide, non consommé, non révoqué | Remise QR ou PIN du commerce autorisé | Une consommation totale, reçu « Lot remis », audit et notification prévus ; aucun solde |
| Consommation active existante | Nouvelle tentative | Restitution « Déjà remis » avec date/reçu autorisés, aucune nouvelle consommation |
| Bon expiré non consommé/non révoqué ou bon valide | Prolonger avec motif et nouvelle échéance | Nouvelle échéance strictement plus tardive, au maximum attribution initiale du bon + 365 jours ; si expiré, nouvelle échéance future. Refus sinon |
| Bon non consommé/non révoqué | Renvoyer | Même bon et même droit, même échéance ; nouvel envoi explicite suivi. Aucun état « remis » |
| Bon non consommé/non révoqué | Remplacer le QR avec motif | Génération QR incrémentée ; ancien QR immédiatement refusé. Lot, gagnant, validité et attribution inchangés |
| Bon non consommé | Révoquer avec motif | Bon définitivement inutilisable, historique et attribution préservés. Pas de remise au stock |
| Consommation marquée par erreur sans remise réelle | Corriger avec motif obligatoire | Événement compensatoire, validation d’origine conservée, consommation active annulée. Bon réutilisable uniquement s’il est valide et non révoqué ; QR et échéance inchangés |
| Bon consommé/révoqué | Prolonger, tourner QR ou remplacer le gagnant | Refus ; un remplacement ne corrige pas implicitement une consommation |
| Retrait du périmètre Animation après attribution | Remise d’un bon engagé | Droit résiduel limité aux bons déjà attribués non consommés jusqu’à échéance, sous habilitations et hors suspension. Pas de nouvelle affectation ni attribution fondée sur ce droit résiduel |

Une correction de consommation exige la référence exacte de la validation corrigée ; rejouer cette correction ne peut annuler une consommation ultérieure. De même, relire un ancien reçu réussi après correction doit rendre le reçu historique et l’état courant : l’écran ne doit pas confondre l’événement ancien avec une remise active.

Les incidents de fournisseur ou de remise sont visibles dans le suivi. Ils ne changent ni le commerce ni le bénéficiaire d’un bon par une modification directe de fiche. Aucun transfert de lot ne peut contourner les conditions de remplacement et de continuité définies ici.

## Contrat HTTP cible

Ce contrat est une cible à implémenter et à générer dans les contrats embarqués ; les routes nouvelles ne sont pas présentées comme disponibles. Les commandes organisateur utilisent la session Animation et son CSRF existants ; les commandes ERP utilisent la session interne et les capacités correspondantes. Les écrans ERP doivent orchestrer les mêmes use cases, pas écrire directement les états ORM.

### Conventions de mutation et lectures

- `Idempotency-Key` : UUID pour les nouvelles commandes, lié à organisation, acteur autorisé, type d’action et cible. Même clé et même corps : même résultat après contrôle des droits courants ; même clé/corps différent : `409 IDEMPOTENCE_CONFLIT`.
- `expected_version` : entier positif obligatoire pour les modifications de la ressource visée, y compris la configuration de dotation. Le tirage contrôle également `population_version`, version distincte de la population figée ; l’édition d’un modèle contrôle sa version et non celle d’une animation. Ces versions de domaine ne remplacent pas `contract_version`. Une version obsolète ne réécrit pas une décision plus récente.
- Les nouveaux objets portent `contract_version: "1"`, distinct de leur version métier. Les changements incompatibles de forme demandent une nouvelle version de contrat et une livraison coordonnée ; les clients refusent un type de gain inconnu avec un état explicite, jamais un repli Coffret.
- Le reçu comprend `operation_id`, `resource_id`, `version`, `resultat`, `server_time`, et le cas échéant `validation_id`, `validated_at`, `mode_effectif`, `rejoue`. Les valeurs secrètes ne sont pas incluses dans les reçus d’audit. Les opérations organisateur se relisent par le mécanisme existant de consultation des opérations Animation ; l’autorisation est contrôlée à chaque lecture.
- Les listes nouvelles reçoivent `cursor` et `limit` (25 par défaut, maximum 100) et renvoient `{items, next_cursor}`. Le curseur opaque est lié aux filtres et au périmètre autorisé, avec ordre stable et identifiant de départage. Les filtres de commune/animation sont autorisés côté serveur, pas uniquement par le client. Les listes historiques et leurs lecteurs conservent leur forme actuelle (tableau ou pagination par page) pendant la livraison coordonnée ; aucune conversion implicite n’est imposée aux anciens contrats.
- États et opérations privées : `Cache-Control: no-store`. Identifiants étrangers au tenant : 404. Session absente/invalide : 401 ; permission manquante sur une ressource accessible : 403 ; corps invalide : 422 ; conflit métier/version : 409 ; capacité expirée ou QR remplacé : 410 ; limitations PIN : 429 avec reprise selon E70.
- Format d’erreur stable : `{code, detail, correlationId, request_id}` ; valeurs techniques sans secret. Le code est traduit en action compréhensible dans chaque interface.

### Organisateur et ERP

Préfixe organisateur `P = /protected/animation-locale`. Les commandes ERP homologues sont exposées sous `/internal/animation-locale` avec audit de l’opérateur et motif ; elles ne réutilisent pas une session client ni un contournement de tenant.

| Méthode et route cible | Entrée métier | Sortie / règles |
| --- | --- | --- |
| `PUT P/animations/{id}/dotation` | Version attendue, nature, gestion libre, durée éventuelle, lignes ordonnées | Dotation versionnée ; choix explicites et gel vérifiés |
| `GET/POST P/modeles-lots` | Filtre de commune / libellé, description, commerce de remise | Page / modèle créé ; gestionnaire habilité ou Localeo ; contrôle du périmètre |
| `PUT P/modeles-lots/{id}` | Version attendue et description | Nouvelle version sans réécriture des versions engagées |
| `POST P/modeles-lots/{id}/exemplaires` | Version modèle, quantité entière positive | `202` opération suivie, identifiants uniques ; reprise crée exactement le total demandé, jamais deux lots de la même commande |
| `GET P/exemplaires-lots` | Commune, modèle, état, cursor, limit | Stock autorisé, sans QR de gagnant ni données personnelles |
| `POST P/animations/{id}/lots/affectations` | Version dotation, liste exacte `exemplaire_ids`, ordre | Affectation atomique exclusive et nouvelle version ; refus si un élément est indisponible |
| `POST P/animations/{id}/lots/liberations` | Version dotation, liste exacte, confirmation | Seuls les jamais-attribués après fin des attributions ; résultat détaillé |
| `POST P/animations/{id}/tirages` | Version population, configuration, confirmation | Pour libre : `202` opération durable acceptée, `operation_id`, état/progression consultables par le mécanisme d’opérations Animation ; résultat définitif disponible seulement après commit atomique du tirage/attributions/intention d’envois. Le même rejeu retrouve cette opération. Coffrets conserve son contrat actuel |
| `GET P/animations/{id}/gains` | Lecture autorisée | Union discriminée ; conserver la compatibilité Coffrets au déploiement coordonné |
| `POST P/animations/{id}/gains/{gain_id}/remplacer` | Version gain, motif, référence de refus ou constat sans réponse | Consomme le prochain suppléant disponible ; refus si conditions non remplies |
| `POST P/animations/{id}/gains/{gain_id}/retirer-au-sort` | Version, motif, confirmation distincte | Retirage complémentaire explicite uniquement si suppléance épuisée ; même population, aucun candidat déjà gagnant |
| `POST P/animations/{id}/gains/{gain_id}/suivi-externe` | Version, événement `CONTACT/REPONSE/REFUS/INCIDENT/REMISE_DECLAREE/CORRECTION`, date, motif/détail | Journal externe ; aucun QR ni consommation terrain simulée |
| `POST P/bons-lots/{id}/prolonger` | Version, `expires_at`, motif | Bon avec nouvelle échéance contrôlée |
| `POST P/bons-lots/{id}/revoquer` | Version et motif | Révocation durable, pas de retour au stock |
| `POST P/bons-lots/{id}/renvoyer` | Version et motif de renvoi | Opération email, même bon |
| `POST P/bons-lots/{id}/remplacer-qr` | Version et motif | Version QR suivante ; envoi du nouveau bon par outbox, ancien immédiatement invalide |
| `POST P/bons-lots/{id}/corriger-consommation` | Version, `validation_id`, motif, attestation de l’absence de remise réelle | Correction auditable ; pas de mutation de validité ni de QR |

Exemple de dotation numérique (identifiants illustratifs, pas des valeurs de production) :

```json
{
  "expected_version": 4,
  "nature": "LIBRE",
  "gestion_libre": "NUMERIQUE",
  "validite_jours": 90,
  "lots": [
    {"exemplaire_id": "11111111-1111-4111-8111-111111111111", "ordre": 1},
    {"exemplaire_id": "22222222-2222-4222-8222-222222222222", "ordre": 2}
  ]
}
```

La réservation de ces exemplaires est faite par la commande d’affectation ; enregistrer cette configuration vérifie qu’elle référence exactement les affectations autorisées. Une API ne peut injecter un exemplaire d’une autre commune dans le tableau. Une dotation externe utilise des lignes décrites et leur quantité, pas `exemplaire_id` ; une dotation Coffrets conserve `coffret_id`. Les combinaisons incohérentes sont refusées.

### Gagnant, scan Pro et PIN

| Route cible | Authentification et entrée | Résultat |
| --- | --- | --- |
| `POST /protected/animation-locale/bons-lots/{id}/acces` | Capacité personnelle issue du lien du gagnant dans le corps, jamais un PIN ; échange selon le mécanisme d’accès personnel | Droit de consultation limité au bon ; nettoyer le lien entrant après échange |
| `GET /protected/animation-locale/bons-lots/{id}` | Bearer personnel du bon ; aucun droit de gestion | Description figée, commerce/adresse/consignes, état, échéance, QR courant et disponibilité du PIN pour ce bon |
| `POST /protected/exploitation/bons-lots/scans` | Session commerce principal/salarié et QR dans le corps | Contexte de scan, version du bon, commerce, état, action autorisée et référence du contexte ; aucune consommation à la lecture |
| `POST /protected/exploitation/bons-lots/{id}/consommations` | Même session, contexte de scan, version attendue et idempotence | Reçu de consommation ; seul le commerce désigné est accepté |
| `GET /protected/exploitation/bons-lots/operations/{operation_id}` | Session commerce habilitée sur la ressource | Reçu durable + état courant pour lever l’incertitude ; ne rejoue pas l’écriture |
| `POST /protected/exploitation/validations-pin/bons-lots/demandes` | Bearer personnel du bon, `{bon_id, expected_version}`, idempotence | Demande E70 de type `BON_LOT`, commerce déterminé par le bon ; effet « Remettre ce lot » |
| `GET/DELETE /protected/exploitation/validations-pin/demandes/{id}` et `POST /protected/exploitation/validations-pin/demandes/{id}/confirmer` | Bearer personnel correspondant ; confirmation avec PIN à six chiffres | Extension typée de l’existant : demande valable cinq minutes, confirmation/lecture/annulation, reçu E70. Pas de changement des canaux Coffret/étape |

Le client PIN n’envoie pas un commerce choisi librement : le serveur le déduit du bon. Un token de participation à une animation n’autorise pas à consulter tous ses lots ; la capacité personnelle porte sur le bon attribué. Une rotation du QR invalide également les contextes de scan/demandes PIN encore en attente basés sur son ancienne version, afin qu’une ancienne présentation ne soit pas consommable. Elle ne crée aucun nouveau gain ; le gagnant conserve un chemin de récupération de son bon courant.

Le type du QR est distinct, par exemple `bon_lot`, avec version de format, identifiant opaque et génération ; les détails cryptographiques et clés restent dans l’adaptateur. L’expiration métier est contrôlée dans le domaine : une prolongation doit rendre le bon utilisable sans être bloquée par une ancienne échéance cryptographique non renouvelable. La rotation de clé et le remplacement individuel du QR sont deux opérations distinctes. Les QR ne contiennent ni PIN, ni email, ni nom du gagnant.

Erreurs ciblées : `DOTATION_NON_RENSEIGNEE`, `DOTATION_FIGEE`, `LOT_INDISPONIBLE`, `CONFLIT_VERSION`, `LOT_DEJA_ATTRIBUE`, `ATTRIBUTION_COMMERCE_INDISPONIBLE`, `REMPLACEMENT_PREMATURE`, `REPONSE_GAGNANT_ENREGISTREE`, `AUCUN_SUPPLEANT`, `AUCUN_CANDIDAT_ELIGIBLE`, `BON_NON_ATTRIBUE`, `BON_EXPIRE`, `BON_REVOQUE`, `QR_REMPLACE`, `COMMERCE_NON_AUTORISE`, `BON_DEJA_CONSOMME`, `PROLONGATION_HORS_LIMITE`. Les codes E70 de PIN incorrect/bloqué/indisponible, demande expirée et idempotence restent conservés. « Déjà remis » peut rendre le reçu existant au commerce autorisé ; il ne doit pas révéler un reçu à un commerce refusé.

## Transactions, concurrence et effets secondaires

Le service applicatif charge les faits et verrouille dans un ordre constant : autorité organisatrice si concernée, gardes commune/commerce, option salarié/identité/session, PIN et demande ou contexte de scan, animation/opération, exemplaires triés, attribution/bon, droit personnel, puis occurrence/reçu/audit/outbox. La demande PIN précède donc la cible, conformément à E70 ; une prélecture sans verrou repère seulement sa hiérarchie. Les chemins QR et PIN partagent le verrou du même bon et la même commande de consommation, sans UoW imbriquée ni commit interne. L’ordre final est vérifié avec les verrous E70 existants par un test PostgreSQL ; aucune branche ne prend les mêmes verrous en ordre inverse.

| Course / panne | Résultat exigé |
| --- | --- |
| Changement de mode vs affectation/achat/publication | Une seule transition gagne sous verrou de configuration ; l’autre refuse, aucun engagement orphelin |
| Deux animations affectent le même exemplaire | Une seule affectation, protégée aussi par contrainte SQL ; l’autre ne réserve rien |
| Deux confirmations du tirage, clés égales ou différentes | Un tirage initial effectif par animation/configuration ; résultat existant retourné. Les tirages supplémentaires ne passent que par leur commande explicite |
| QR et PIN simultanés, ou deux salariés | Une consommation active et un reçu métier, résultat existant ou conflit pour l’autre ; pas de double email/notification métier |
| Remplacement gagnant vs consommation | Consommation gagnante interdit le remplacement ; remplacement gagnant révoque l’ancien et empêche sa consommation. Jamais deux bons actifs |
| Retrait du périmètre/suspension du commerce vs émission initiale ou remplacement | Même garde transactionnelle du commerce. Si le retrait gagne, la nouvelle émission refuse avant tout commit de tirage/attribution ; remplacement refusé sans toucher l’ancien bon ni le suppléant. Si l’émission gagne, le bon est déjà attribué au retrait et bénéficie seulement de DEC-42, sans contourner une suspension. Verrouiller les commerces concernés dans un ordre stable avant les lots évite une vérification devenue obsolète |
| Rotation QR vs scan préparé | Validation recontrôle génération/version ; ancien contexte refusé, même si la lecture avait réussi |
| Prolongation vs expiration | Heure serveur et échéance relues au commit ; domaine sans dépendance au passage d’un batch |
| Correction vs seconde validation | Correction cible exactement la validation initiale et sa version ; un rejeu ne corrige pas une remise postérieure |
| Commit réussi, réponse HTTP perdue | Relecture du reçu/opération ; pas de nouvelle attribution/consommation pour « vérifier » |
| Commit réussi, fournisseur email indisponible | Outbox conservée et état en échec/en attente ; reprise du même événement sans nouveau bon. Aucun rollback de gain déjà attribué |
| Changement de périmètre ou révocation salarié en session ouverte | Contrôle serveur courant au début de la commande et garde transactionnelle cohérente ; aucun droit acquis par simple ouverture de l’écran |

Contraintes attendues : index unique d’affectation active par exemplaire ; unicité de position attribuée et de participant gagnant libre par animation ; une attribution courante par unité ; un bon courant par exemplaire ; index partiel de consommation active ; index de clé d’idempotence ; unicité du message outbox par événement/attribution. Les erreurs de contrainte sont traduites en conflits de domaine, jamais en succès partiel.

L’audit renseigne action, acteur réel, organisation, commune, animation, modèle/exemplaire/attribution/bon, version avant/après, canal, validation corrigée ou remplacée, motif et corrélation. Il ne stocke pas le secret QR, le PIN ou les capacités personnelles. Les durées et gels sont rattachés au dispositif de conservation existant, avec la preuve de consommation et la continuité des gains ouverts ; aucun effacement générique ne supprime un bon encore engagé. Voir les [contrats et la conservation E70](../epic-70-validation-pin/architecture-contrats.md) et les modalités transverses du présent dossier.

## UX, emails et suivi

- **Gestionnaire** : trois branches explicites, stock disponible/affecté/attribué lisible, ordre visible avant publication. Les actions de correction, retrait, remplacement et retirage ont leur confirmation et leur motif. Un indicateur « Envoi en attente/Envoyé/Échec » ne remplace jamais l’état « Lot remis ». Le suivi externe affiche « Remise non renseignée » tant qu’aucune déclaration n’existe.
- **Gagnant externe** : nom de l’animation, lot, organisateur, responsable et consignes, contact, délai annoncé de 14 jours sans réponse avant remplacement ; aucun faux QR à consommer.
- **Gagnant numérique** : même contexte, plus le bon, son commerce de remise, échéance en heure de Paris et état courant. Le lien rejoint une entrée de carnet de type bon libre. Le QR personnel et « Faire valider par PIN » sont proposés lorsque leur canal est effectivement disponible ; le PIN reste saisi par le commerçant sur le téléphone du gagnant.
- **Principal et salarié Pro** : le scan déjà central reçoit le type lot libre, puis affiche description, commerce et action unique. Vert + « Lot à remettre » si valide ; bleu + « Déjà remis » et date si consommé ; rouge + motif si mauvais commerce, expiré ou révoqué. Icône et texte rendent la couleur non indispensable. Après confirmation serveur : « Lot remis » et reçu, puis « Scanner un autre QR ». Pas de bouton actif pendant l’envoi ni d’écran de succès local en mode hors ligne.
- **Incident réseau** : message « Résultat non confirmé » et action de lecture du reçu. Aucun nouvel identifiant de mutation créé tant que le résultat précédent n’a pas été vérifié. L’écran relit également l’état courant après une correction ou une rotation.
- **Email automatique** : déclenché après confirmation du tirage libre et de l’attribution ; rendu système commun, texte + HTML, valeurs échappées, lien personnel protégé. Un renvoi explicite est distinct d’une reprise technique. L’email de remplacement indique le nouveau droit ; consulter l’ancien bon affiche sa révocation sans montrer les coordonnées du suppléant.
- **Notifications Pro** : une validation PIN réussie crée la notification prévue par E70 ; extension du type de cible au bon. La consultation de l’historique salarié reste limitée aux informations autorisées de son commerce ; aucun accès aux outils de stock, tirage ou PIN administrateur n’est ajouté.

## Migration, compatibilité et livraison

1. Ajouter les nouvelles tables/colonnes/contraintes, sans modifier les SQL déjà appliqués ni fabriquer de données métier. Les animations historiques dont la dotation Coffrets est prouvée sont explicitement marquées `COFFRETS`. Un dossier incohérent est rapporté et maintenu hors bascule automatique ; aucune animation n’est convertie en lot libre par absence de coffret dans un export partiel.
2. Préserver les anciennes instances, dates, paiements, preuves de population, gains et liens Coffrets. Les nouvelles références de gains sont discriminées ; la contrainte de cohérence interdit simultanément une référence Coffret et libre. Les anciens clients ne savent pas rendre ces gains : ne pas activer la création libre avant livraison des consommateurs compatibles.
3. Étendre les projections publique, organisateur, commerçant, Live et la vision ERP/CRM. Aucun bilan financier ne additionne des quantités de lots libres à un chiffre d’affaires Coffrets. Le « lot remis » externe est une déclaration, le numérique une consommation ; les deux sont distingués dans les exports.
4. Régénérer le contrat backend et ses consommateurs : [OpenAPI documentaire Animation](../epic-41-api/openapi.json), [OpenAPI Live](../epic-42-localeo-live/openapi.json), [vision ERP](../epic-45-vision-360-animation/openapi.json), `localeo-animation/src/imports/openapi.json`, `localeo-commercant/api/localeo-openapi.json` et les schémas moteur concernés. Réutiliser les [générateurs backend](../../../../localeo-backend/scripts/documentation) et les commandes de génération propres aux lecteurs ; aucun JSON embarqué n’est modifié manuellement pour contourner un test.
5. Conserver le fonctionnement Coffrets et E70 existants pendant le déploiement. L’activation pilote libre est une étape après contrats, stockage, outbox, frontends et preuves. Un retour applicatif ancien devient incompatible dès création de bons : documenter une correction en avant ou une restauration contrôlée, sans prétendre qu’une migration destructive est réversible.
6. Adapter le générateur de démonstration : gestion externe sans Pro, commerce Animation seule avec salarié, plusieurs exemplaires, stock concurrent, bon valide/expiré/révoqué/consommé/corrigé, suppléant et remplacement, candidat insuffisant, email en erreur simulée. Données synthétiques et secrets temporaires uniquement ; aucune génération réelle au titre de la spécification.

## Preuves à produire

Tous les tests ci-dessous sont **prévus, non exécutés** à cette phase. Les suites historiques citées servent de points de prolongement et de régression, pas de preuve déjà acquise sur les lots libres.

| US / critères | Scénarios observables et couche | Point de départ réel / nouvelle preuve attendue |
| --- | --- | --- |
| US01, US02 — CA-01 à 05, CA-11 | Choix obligatoire ; gel à publication/engagement, concurrence avec affectation ; libre sans achat Coffrets ; non-régression Coffrets seule | Domaine configuration + API et navigateur portail ; facture/instance Coffrets absentes après parcours libre |
| US04 — CA-06, CA-08 à 10, CA-29 | Responsable externe sans compte Pro ; quantité/ordre ; contact et remise facultative, correction tracée, zéro QR forcé, refus hors tenant | Nouveau test domaine/application suivi externe + scénario navigateur gestionnaire/gagnant |
| US05/06 — CA-30/31 | Plusieurs modèles/exemplaires exacts, snapshot préservé, tentative Pro refusée ; deux réservations concurrentes ; libération confirmée jamais-attribués uniquement | Tests domaine modèle/exemplaire et intégration PostgreSQL multi-UoW ; génération interrompue puis reprise sans doublon |
| US07 — CA-07/32 | Zéro/moins/autant/plus de candidats ; un gain par participant ; suppléants figés ; ordre des unités ; rejeu et double commande ; délai 14 jours, réponse/refus, retirage, aucun candidat ; retrait de commerce après publication puis refus atomique de confirmation sans aucun gain/email partiel | Étendre [tests de tirage domaine](../../../../localeo-backend/tests/domain/animation_locale/test_tirage_gain_animation.py) et [tirage tous lots](../../../../localeo-backend/tests/application/animation_locale/test_tirage_tous_lots_animation.py), maintenir la politique Coffrets |
| US08 — CA-08/09/33 | Email automatique outbox unique, envoi en échec, reprise, consultation autorisée, bornes 1/365 et défaut 90, ancien QR après rotation | Tests fournisseur simulé + Live/contrat ; aucun envoi réel ; étendre [test de non-gagnant](../../../../localeo-backend/tests/application/animation_locale/test_envoi_gain_non_gagnant.py) |
| US09 — CA-34/35 | Principal/salarié du bon commerce, mauvais commerce, token invalide/expiré/remplacé, PIN actif/bloqué/révoqué ; QR/PIN simultanés, reçu relu après timeout | Étendre [tests API E70](../../../../localeo-backend/tests/api/test_pin_validation_e70.py), [validations salariés](../../../../localeo-backend/tests/security/test_validations_salaries_e72.py) ; nouvelle concurrence PostgreSQL et navigateur Pro/Live |
| US10 — CA-36 | Prolongations successives jusqu’au plafond et refus au-delà ; expiré réactivable, consommé/révoqué refusé ; correction ciblée rejouée après nouvelle remise ; remplacement vs scan ; remplacement après retrait refusé en conservant ancien bon et suppléant ; course retrait/émission ; continuité sans contourner suspension | Domaine bon et propriété consommation unique ; tests application + PostgreSQL + droits en session déjà ouverte ; fixtures et audits |

Les suites de domaine sont exécutées sans ORM ni configuration opérateur, les tests d’orchestration avec doubles de ports et les courses sur PostgreSQL jetable. Les tests frontend vérifient contrats, absence de faux succès, isolation de sessions et états lisibles sur mobile ; les builds seuls ne prouvent pas les invariants de lot. L’exécution et ses résultats seront consignés dans [verification-livraison.md](verification-livraison.md).
