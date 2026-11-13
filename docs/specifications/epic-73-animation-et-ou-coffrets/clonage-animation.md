# E73 — Cloner une animation

**Évolution E73-EVO-CLONAGE — 13 novembre 2026. Implémentée ; vérifications locales réalisées, CL-11 partiel.**
Rattachement : [backlog E73](../../roadmap/terminees/epic-73-animation-et-ou-coffrets-backlog.md),
critère historique **E73-CA-59** et [nouvelle édition](perimetres-parcours-saas.md#63-nouvelle-édition).
Le statut Terminée et la clôture historique de l’EPIC 73 restent inchangés.

## 1. Besoin, existant et périmètre

L’organisateur veut repartir d’une animation existante pour préparer une autre
animation sans ressaisir ses contenus. Le résultat attendu est un nouveau
brouillon indépendant, reconnaissable et modifiable, avec les vérifications
nécessaires avant publication.

Lecture des sources le 13 novembre : backend `95babb7`, Animation `a00bb2a`,
projet `492f164`, avec les modifications documentaires préexistantes de clôture
automatique conservées. Aucun accès à un environnement déployé n’a été effectué.

Avant cette évolution, le mécanisme existait sous **Nouvelle édition** :

- [ServiceEditionsAnimation](../../../../localeo-backend/app/application/animation_locale/services/editions_animation.py)
  et domaine [NouvelleEdition](../../../../localeo-backend/app/domaine/animation_locale/valorisation/regles.py) ;
- [NewEditionWorkspace](../../../../localeo-animation/src/app/components/NewEditionWorkspace.tsx),
  accessible uniquement depuis **Fiche → Bilan**, après chargement de ses mesures ;
- préparation serveur, sélection textes/visuels/scénario, nouvelles dates,
  dotation explicite, création atomique et reçu de rapprochement déjà disponibles.

L’évolution expose ce même mécanisme sous **Cloner l’animation**, depuis la
liste, les archives et la fiche, sans dépendre du chargement des statistiques.
Elle précise la fidélité des sections reprises, les refus et la reprise après
incident. Elle ne crée ni second service de duplication ni second historique.

**Périmètre confirmé par l’utilisateur le 13 novembre 2026 :** accès direct au
clonage existant, avec reprise des textes, visuels et scénario. Conserver les
décisions acquises de CA-59 :
même organisation, même commune et même moteur ; sélection explicite des textes,
visuels et scénario/paramètres ; nouvelle dotation à choisir. Le préremplissage
supplémentaire des commerçants et des lignes de dotation n’est pas retenu dans
cette évolution. Aucun arbitrage produit ne reste ouvert sur ce choix de périmètre.

Hors périmètre : clonage en masse, changement de commune ou d’organisation,
changement de moteur, publication automatique, achat de lots, reconduction
des accords et notifications aux participants ou commerçants.

## 2. Parcours cible

1. **Animations** et **Mes archives** : action secondaire **Cloner l’animation**
   sur une ligne/carte autorisée, distincte de l’ouverture et de la prochaine
   action recommandée. Dans la fiche, même action dans **Autres actions sur
   l’animation**, y compris lorsque la source est en lecture seule.
2. Destination commune `/animations/{animation_id}/cloner`. L’entrée du Bilan
   ouvre également ce parcours ; elle est renommée sans supprimer les anciennes
   possibilités de navigation. Une erreur de Bilan ne bloque pas le clonage.
3. Afficher source, commune, moteur et explication **Un nouveau brouillon sera
   créé. L’animation d’origine restera inchangée.** Proposer **Copie de {nom}**,
   modifiable, borné à 160 caractères. L’homonymie n’est pas une identité ni un
   motif pour réutiliser une animation existante.
4. Nom et dates sont obligatoires. Dates initialement vides, saisie en calendrier
   Paris, dernier jour inclus converti en fin exclusive selon le helper existant.
   Ne pas ajouter une interdiction de date passée absente des règles actuelles ;
   les règles usuelles de création/publication continuent de s’appliquer.
5. Présenter les sections disponibles et leurs limites. Leur sélection reste
   explicite, sans « tout copier » caché. Une indisponibilité explique le motif.
   Choisir de nouveau la dotation Coffrets / Libre externe / Libre numérique,
   sans présélection héritée ni engagement de stock.
6. Récapitulatif court : contenu repris, contenu à préparer de nouveau et liste
   serveur des revalidations. Confirmation puis **Créer le brouillon cloné**.
   Ouvrir ce formulaire et consulter un aperçu n’écrit aucune animation.
7. Après confirmation serveur, annoncer **Brouillon cloné créé** puis ouvrir
   l’Assistant de la cible. Conserver sa provenance sans modifier la source.
   Une source brouillon utilisée par une édition reste protégée par la provenance :
   sa suppression doit expliquer ce lien, sans erreur SQL brute ni suppression
   en cascade des éditions.

Annuler revient au point d’entrée : fiche/onglet ou liste/archives avec filtres,
page, position et focus conservés. Une saisie modifiée utilise la garde commune.
À 320/390 px et texte 200 %, aucun débordement global ; action au clavier,
libellé explicite, focus sur erreur/résultat et retour au déclencheur. Les espaces
de gestion utilisent la largeur disponible avec alignement à gauche.

## 3. Règles de reprise et de réinitialisation

| Élément | Comportement du clone |
| --- | --- |
| Identité et cycle | Nouveaux ID, référence et configuration ; statut `BROUILLON`, version initiale ; aucun instant de publication/clôture/fin/archivage hérité |
| Source | Configuration courante avant publication ; configuration publiée avec paramètres d’exploitation et retraits effectifs ensuite, via le résolveur existant. ID/version/empreinte de cette source contrôlés à confirmation |
| Nom, calendrier, inscriptions | Nom proposé modifiable, nouvelles dates obligatoires ; pas de reprise d’une fermeture historique, d’un gel ou d’un état d’inscription exécuté |
| Textes | Description et mission commerçant si `TEXTES` sélectionné ; valeurs propres à la cible, sans modifier la source |
| Scénario et paramètres | Sections supportées sélectionnées, capacité d’inscription et paramètres réutilisables ; nouvelle préparation éditable. Contenus personnalisés et leurs relations doivent être préservés ou déclarés non réutilisables avant confirmation |
| Identifiants du scénario | Identifiants propres à la nouvelle préparation et références internes remappées ensemble ; aucune condition, mission, objet de continuité ou média ne doit pointer vers un élément privé de l’ancienne exécution |
| Visuels | Seulement les médias dont le réemploi est autorisé et contrôlé ; nouvelles associations aux artefacts existants, sans copie physique inutile. Une purge ou révocation entre aperçu et commande interdit la reprise atomiquement |
| Commerçants | Références historiques uniquement comme candidats de provenance ; sélections actives, invitations, demandes et accords non repris. Nouvelle sélection et nouveaux accords avant publication |
| Dotation | Nouveau choix explicite du mode ; lignes, exemplaires affectés, achats, réservations, paiements et bons non repris |
| Règlement et terrain | Relecture et validation propres à la nouvelle animation ; aucune attestation, acceptation légale, validation de terrain ou vérification POI héritée |
| Participants et activité | Aucun participant, consentement, token, QR personnel, progression, validation, tirage, gain, remise, résultat, avis ou compteur repris |
| Communication et diffusion | Aucune campagne, programmation, audience, notification, source d’acquisition ou QR/lien de diffusion reconduit ; les futurs supports désignent la cible |
| Objectifs et suivi | Objectifs à définir de nouveau ; provenance sélectionnée conservée, sans reprendre l’audit ni les mesures de la source comme activité de la cible |

**Écart corrigé :** le réemploi initial reconstruisait la préparation depuis
son `resultat`. Des champs personnalisés de chasse (`collectibles`,
`continuityElements`, adaptations hors résultat) peuvent être omis. Le libellé
« scénario et paramètres » ne doit pas promettre une copie complète si ces
éléments sont perdus. Définir une transformation par moteur/version : conserver
les contenus supportés et remapper le graphe ; pour une variante non supportée,
rendre cette section indisponible avec un motif avant la confirmation. Ne pas
effacer silencieusement les éléments personnalisés pour réussir une copie.

Tous les statuts source lisibles restent admissibles selon les droits courants,
y compris `BROUILLON`, `CONFIGUREE`, `PUBLIEE`, `EN_COURS`, `CLOTUREE`, `TERMINEE`,
`ARCHIVEE`, `ANNULEE`. Le statut de la source n’accorde aucun droit de création.
Une archive reste figée : lire sa configuration pour créer une autre racine
n’est pas la rouvrir. Source absente, configuration illisible ou moteur non
réutilisable donnent un refus explicite, pas un brouillon vide présenté comme copie.

Le clonage ne consomme aucun crédit de génération ou de publication. La future
publication utilise les droits et quotas courants. Si la clôture automatique
CAF est livrée, la cible applique les valeurs de création standard de cette
version ; aucun report, échéancier, rapport ou notification de la source n’est
reconduit. La spécification CAF ne constitue pas une dépendance de livraison.

## 4. Domaine, orchestration et contrats

`NouvelleEdition` reste propriétaire des règles pures : périmètre identique,
sélection autorisée, dates, identité indépendante, fidélité et liste blanche.
Les transformations de scénario appartiennent aux politiques du moteur ; elles
ne sont pas réalisées par React, SQL ou un export/import JSON générique.
`ServiceEditionsAnimation` charge les faits via les ports, autorise, coordonne
transaction, nouvelle animation, provenance, médias, audit et reçu atomiques.
Les droits commerciaux, le catalogue et la réversibilité restent leurs domaines
existants. Aucun appel fournisseur ou binaire complet dans la transaction.

### Contrats conservés

Préfixe `/protected/animation-locale` :

| Route | Comportement |
| --- | --- |
| `GET /animations/{id}/editions/preparation` | Source versionnée, sections disponibles, motifs, revalidations et `allowedActions` ; lecture seule |
| `POST /animations/{id}/editions` | Même commande fermée : `expected_version`, `sourceConfigurationId`, `sourceConfigurationHash`, `communeId`, `nom`, `dateDebut`, `dateFin`, `sections`, `dotation` ; en-tête `Idempotency-Key` |
| `GET /animations/{id}/editions/commandes/{cle}` | Rapprochement du résultat confirmé, en cours ou absent, sans création implicite |

Le résultat conserve `animationId`, `configurationVersion`, `statut=BROUILLON`,
provenance, revalidations et `rejoue`. Les noms techniques « édition » sont
conservés. Aucun endpoint `/cloner` concurrent n’est ajouté au backend.

### Projection additive de disponibilité

Ajouter à `AnimationSummaryPayload` et au détail un objet facultatif nullable
`reemploi`, même forme sur liste/archives/fiche : `items[].reemploi` dans les
pages et `animation.reemploi` dans `AnimationDetailPayload`, via son résumé
hérité. Ne pas introduire une seconde copie divergente au niveau racine du détail.

```json
{
  "allowedActions": ["CREER_EDITION"],
  "motifsIndisponibilite": []
}
```

`allowedActions` vide signifie indisponible avec motifs lisibles. Champ absent
ou nul signifie capacité non fournie, pas autorisation. L’interface n’infère
pas ce droit du statut ni d’un droit sur une autre commune. Les autres actions
du détail et les clients existants restent compatibles.

La projection utilise les faits courants de lecture/création, organisation,
commune, modèle actif, droit du type et réversibilité, calculés par les mêmes
politiques que la commande. Elle ne charge ni les mesures, ni les médias, ni
les préparations par ligne. La préparation détaillée recontrôle les sections
au clic et la commande refait les vérifications complètes ; aucune réservation
de droit n’est déduite de la projection.

API productrice : [valorisation_animation_api](../../../../localeo-backend/app/api/valorisation_animation_api.py),
[DTO valorisation](../../../../localeo-backend/app/application/animation_locale/contrats_moteur/valorisation.py)
et projections d’[animation_locale_api](../../../../localeo-backend/app/api/animation_locale_api.py).
Consommateur : `api.ts`, `resultsApi.ts`, `resultsContracts.ts`, formulaire commun
et route dédiée de Localeo Animation. À l’implémentation, synchroniser les
composants concernés d’[OpenAPI E41](../epic-41-api/openapi.json), de la vue E42
qui contient également les résumés d’animation, et du contrat embarqué
`localeo-animation/src/imports/openapi.json`, depuis
[generate_epic41_openapi.py](../../../../localeo-backend/scripts/documentation/generate_epic41_openapi.py)
et [generate_epic42_openapi.py](../../../../localeo-backend/scripts/documentation/generate_epic42_openapi.py).
Les vues OpenAPI E41/E42 et le contrat embarqué Animation sont régénérés depuis
le producteur ; le champ reste facultatif pour les anciens consommateurs.

### Concurrence et reprise

Source modifiée entre préparation et confirmation : `VERSION_OBSOLETE`, aucune
cible créée, nouvelle lecture obligatoire ; conserver nom/dates compatibles,
invalider la confirmation et signaler les sections devenues indisponibles.
Source supprimée, média purgé ou droit retiré : refus sans données partielles.

Double clic/rejeu avec même clé et même intention : un seul brouillon, même ID,
audit et provenance. Même clé avec contenu différent : conflit. Deux intentions
explicitement distinctes peuvent créer deux brouillons, jamais deux débits de
publication. Clé et intention restent en mémoire ; réponse perdue → lire le
reçu → attendre si en cours, ouvrir la cible si confirmé, rejouer explicitement
la même commande seulement si absent. Pas de retry automatique d’écriture.

**Absent a un sens contractuel précis :** seul le `404` portant le code
`COMMANDE_NON_ENREGISTREE` autorise ce rejeu explicite. Un `404`
`RESSOURCE_INTROUVABLE` après suppression/perte d’accès source, un refus
d’autorisation ou un `409 COMMANDE_EXPIREE` après réduction du reçu ne prouvent
pas qu’aucun clone n’a été créé. Ils interdisent le rejeu proposé et demandent
de vérifier les animations/provenances accessibles ou de solliciter l’assistance.
Ne pas remplacer la clé pour lever cette incertitude. La politique de conservation
en vigueur reste inchangée ; aucune nouvelle durée de rétention n’est décidée.

Le hook partagé `useCampaignCommand.ts` assimilait toute réponse `404`
à une absence : le clonage et les consommateurs partagés distinguent désormais
le code contractuel. Un reçu confirmé dont la cible
est devenue inaccessible affiche cet état, sans proposer de recréation implicite.

Changement d’organisation/commune, révocation ou déconnexion : appliquer la garde
commune, annuler/invalider lectures anciennes, ne pas ouvrir une cible d’un ancien
contexte. Ne pas stocker de configuration privée en localStorage/sessionStorage.

## 5. Critères ajoutés et preuves attendues

CA-59 reste conservé ; CL-01 à CL-12 le complètent. Les preuves exécutées et
leurs limites sont consignées dans le [bilan de vérification](verification-livraison.md#évolution--e73-evo-clonage-13-novembre-2026).

| ID | Critère observable | Preuve prévue |
| --- | --- | --- |
| CL-01 | Clonage trouvé dans liste, archives et fiche, même formulaire depuis le Bilan ; indépendant des statistiques | Navigateur : quatre entrées, Bilan en panne, source active et archivée |
| CL-02 | Même organisation/commune/moteur ; droits courants et modèles actifs contrôlés, refus API directe hors périmètre | Domaine et API : tous statuts lisibles, rôle lecture seule, droit retiré, organisation fermée, autre commune |
| CL-03 | Nom modifiable ≤160, dates requises sans reprise automatique, Paris et fin inclusive correctement convertis, choix de dotation explicite | Contrat et navigateur : dates invalides, changement d’heure été/hiver, trois dotations |
| CL-04 | Seules les sections sélectionnées disponibles sont copiées ; fidélité ou indisponibilité expliquée, aucune perte silencieuse | Domaine : textes seuls, visuels seuls, chacun des moteurs supportés dont tombola, chasse/passeport personnalisés, objets/continuité/références, moteur/version non supportés |
| CL-05 | Nouveau brouillon indépendant, source inchangée ; aucun engagement/participant/résultat/notification hérité | PostgreSQL : comparer source/cible, absence d’invitation, gain, paiement, QR, campagne ou outbox ; provenance protégée |
| CL-06 | Version source et réemploi des médias revérifiés atomiquement ; échec sans cible partielle | PostgreSQL : modification/suppression/purge concurrentes, rollback injecté, préparation devenue indisponible |
| CL-07 | Rejeu même intention = même cible ; conflit d’intention ; réponse perdue rapprochée sans second clone ; seul le code d’absence autorise le rejeu | Concurrence PostgreSQL, API reçu 200/202/404 `COMMANDE_NON_ENREGISTREE`, 404 `RESSOURCE_INTROUVABLE`, 403, 409 `COMMANDE_EXPIREE`, cible inaccessible et hook partagé |
| CL-08 | Assistant du nouveau brouillon et revalidations visibles après réussite ; aucun crédit génération/publication consommé avant publication | Domaine/application : compteurs inchangés puis publication normale avec nouveaux accords et dotation |
| CL-09 | Retour conserve origine/filtres/page/focus, saisie protégée et réponses d’ancien tenant ignorées | Navigateur : Retour/Avancer, Annuler, changement commune pendant GET et commande incertaine |
| CL-10 | Action/formulaire utilisables à 320/390/1280 px, texte 200 %, clavier et erreurs accessibles | Recette visuelle, focus, annonces, absence de débordement et de dépendance à la couleur |
| CL-11 | Capacité fournie par une projection groupée ; aucune requête Bilan/préparation par animation affichée ; traitement borné | Contrats + SQL N/10N, pages 25/100, source simple/maximale, charge mixte et mémoire |
| CL-12 | Contrats anciens/nouveaux compatibles, provenance/export/rétention cohérents, générateur et diagnostic documentés | Tests consommateurs, fixtures démo, échec média/source, contrôle migration et recette de livraison |

Suites existantes à étendre : backend `tests/domain/animation_locale/` pour les
règles de valorisation, `tests/security/test_valorisation_animation_postgres.py`,
tests API de valorisation ; Animation `saas-journey-contracts.test.mjs`,
`saas-journey-http-contracts.test.mjs`, `tests/browser/saas-journey.mjs`,
`productivity-workspace.mjs`, `fin-animation.mjs` et gardes de navigation.
Ajouter les scénarios qui manquent, sans considérer leurs anciens résultats
comme preuve de cette évolution.

## 6. Performance, données et livraison

| Parcours | Bornes et accès | Budget à vérifier avant activation |
| --- | --- | --- |
| Liste/archives et capacité | Pagination SQL 25, maximum 100 ; enrichissement de la seule page ; faits d’habilitation/droit groupés par périmètre, sans configuration/média/Bilan hydraté | Nombre de requêtes constant de 25 à 100 lignes ; p95 ≤700 ms ; N=1 000 puis 10N=10 000 animations avec tenants étrangers et archives |
| Préparation de copie | Une seule source/version ; lecture des métadonnées médias avec `LIMIT 201`, réemploi ≤200 ; pas de binaire, descendants ni historique de participants ; enveloppe de source ci-dessous | p95 ≤900 ms ; mesurer nombre d’objets, octets et mémoire sur source minimale et maximale, à froid et à chaud |
| Création et reçu | Une cible atomique, verrous courts source/droits/reçu ; index UUID et unicité de la clé existants ; aucun fournisseur ni copie binaire synchrone | Création p95 ≤1 500 ms, reçu ≤500 ms ; 10 utilisateurs concurrents, lecture/publication mixte, deux clés et même clé ; aucun doublon ni blocage global |

Ces budgets sont des objectifs de recette, pas des performances mesurées.
Enveloppe de conception issue des limites existantes à réappliquer au réemploi :
commande HTTP ≤16 384 octets ; configuration effective sérialisée en JSON UTF-8
compact ≤8 000 000 octets, profondeur ≤32, textes éditoriaux cumulés ≤512 000
octets ; médias ≤200 avec chacun ≤44 000 octets binaires et ≤60 000 octets de
représentation JSON lorsqu’un import est concerné. La préparation de clonage
ne renvoie que leurs métadonnées, jamais leurs base64. Contrôler la taille de la
source côté persistance avant de l’hydrater et remesurer après résolution des
paramètres effectifs ; une source historique hors borne devient explicitement
non réutilisable, sans troncature. Ces bornes techniques n’ajoutent aucun quota
commercial de clonage.

L’existant ne borne pas uniformément le nombre de positions, objets, conditions
ou candidats commerçants en dehors de la taille des contenus. L1 doit contrôler
les collections dans l’enveloppe ci-dessus, mesurer la mémoire des graphes les
plus denses autorisés et borner les paramètres de requêtes SQL par lots de 100.
Le nombre de requêtes dépend du contenu borné de la source, jamais du nombre de
participants ni des autres animations. Si l’enveloppe ne respecte pas les budgets,
documenter la borne effective avant activation du moteur concerné ; aucun plafond
réduit silencieusement après confirmation.

Persistance : réutiliser `animation_editions`, les configurations, associations
de médias et reçus existants. Aucun backfill ni réécriture des animations
historiques prévu. Une migration supplémentaire n’est pas présumée nécessaire ;
si une transformation supportée exige un champ de provenance, la préciser et
la tester en L1 avant activation. Préserver les FK `RESTRICT` de provenance et
la protection de la suppression d’une source utilisée.

| Critères | Documentation / contrat | Démonstration et fixtures | Exploitation / livraison |
| --- | --- | --- | --- |
| CL-01/03/09/10 | Présent parcours, aide de création/édition et libellés Animation | Brouillon, animation active et archivée, noms longs, mobile et retours de liste | Frontend après backend compatible ; pas de nouveau paramètre d’environnement |
| CL-02/04/05/06/08 | CA-59, règles du domaine/moteurs et revalidations | Sources synthétiques des moteurs, médias valides/révoqués, scénario personnalisé, trois dotations ; vérifier le générateur si sa sélection de sections évolue | Même droits et quotas ; aucune notification réelle ni opération financière pour la recette |
| CL-07/11/12 | DTO/OpenAPI, reçu et budgets ci-dessus | Reprise de réponse perdue, export/restauration d’une chaîne d’éditions, retrait de droits | Diagnostic par IDs source/cible/opération et code de refus, sans secret ni corps privé dans les logs ; reprise du reçu existant |

Le [guide de parcours de la plateforme](../../exploitation/exploitation/parcours-plateforme-animation.md)
et la [prise en main par lot](prise-en-main-par-lot.md) décrivent les nouveaux
points d’entrée et la reprise après incident. Leur disponibilité sur un
environnement dépend de la livraison du backend puis du portail compatibles.

Backend/ERP et Localeo Animation sont concernés. L’ERP conserve son rôle de
consultation/configuration ; aucun nouveau bouton de duplication ERP ni batch
n’est demandé. Marketplace/Live et Commerçant ne reçoivent aucune cible avant
publication : leurs contrats publics restent inchangés, leurs scénarios de
publication/accords doivent conserver leurs refus. La démonstration n’est pas
générée sur un environnement réel pendant cette phase.

## 7. Lots et préparation

| Lot | Périmètre | Dépendances / sortie |
| --- | --- | --- |
| L1 | Politique de réemploi groupée, contrat additif, fidélité et bornes par moteur, refus de provenance/médias | CL-02/04/06/11/12 ; critères de fidélité et transformations testés avant exposition |
| L2 | Route et action Cloner, formulaire commun, nom/dates/récapitulatif, retour et garde | Contrats L1 ; CL-01/03/09/10 ; aucune seconde commande métier |
| L3 | Atomicité/rejeu, publication/revalidations, régression, performance, documentation et démo | L1/L2 ; CL-05/07/08/11/12, résultats à consigner dans le bilan E73 |

Le parcours de base est implémenté avec son périmètre confirmé par l’utilisateur ;
le préremplissage étendu est exclu de cette évolution. Les préparations Passeport
1.0 et Chasse connues sont reprises ; les objets et continuités personnalisés de
chasse sont conservés avec leurs références remappées. Les variantes inconnues
ou les définitions de chasse sans préparation reconstructible rendent la section
scénario indisponible. Les tombolas et brouillons sans préparation réutilisent
leurs paramètres autorisés. Les preuves et limites d’acceptation figurent au
bilan ; aucune livraison sur un environnement partagé n’est attestée ici.
