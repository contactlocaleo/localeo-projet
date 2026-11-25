# EPIC 84 — Adhérents hors commune dans Localeo Animation

Le CEJ pilote une animation à Martignas-sur-Jalle. Un adhérent de Saint-Jean-d’Illac reçoit une invitation individuelle et choisit de participer à cette même animation. Son établissement conserve sa commune réelle. [Backlog et critères HC-01 à HC-09](../../roadmap/en-cours/epic-84-adherents-hors-commune-animation-backlog.md)

## Établissement, réseau et accès

Référencement porte le rattachement nominatif entre une organisation, sa commune de pilotage et un établissement. La clé de ce lien exclut le numéro de souscription et le terme commercial. Une autre association de Martignas conserve son propre réseau. Un renouvellement du CEJ pour la même commune retrouve les liens précédents. La souscription et les habilitations effectives sont contrôlées à chaque nouvelle opération. Le réseau communal existant continue à fournir les candidats locaux. Aucun quota de rattachements extérieurs ne s’applique.

Dans **Commerçants**, le formulaire propose la commune active et son code postal. La recherche d’une autre commune retourne des localités du référentiel. Une création enregistre l’établissement à sa véritable adresse. Une fiche existante est réutilisable si sa commune, son SIRET et son email concordent après normalisation. Le CEJ ne peut ni réattribuer le compte Pro, ni modifier l’identité ou les autres produits d’un commerce par ce rapprochement. Une collision est présentée comme une vérification Localeo sans exposer de fiche extérieure. Une écriture répétée ou concurrente conserve un lien unique.

## Saisie, import et éligibilité

La gestion utilise la session Animation, sa commune courante et les contrôles de permission existants. Sous `/protected/referencement/commercants-animation`, la recherche des communes aide à renseigner la destination. Les lectures de liste et de détail retournent la commune réelle et les actions autorisées. Les écritures conservent les contrôles de version et d’idempotence.

La liste **Commerçants** affiche le total correspondant à la recherche, la
page courante sur le nombre de pages et les boutons première, précédente et
suivante. Elle lit jusqu’à 25 fiches à la fois. Une nouvelle recherche repart
de la première page. L’actualisation relit la page courante et revient à la
première si elle a disparu entre-temps.

Le lot d’import porte sur le périmètre autorisé de son initiateur. Sa commune de pilotage est distincte de la commune de chaque ligne. Le serveur résout la commune et la catégorie, vérifie l’identité puis propose création, rattachement, complétion ou vérification. Le CEJ peut confirmer les lignes prêtes. Une confirmation acceptée engage un traitement différé : le résultat d’une ligne n’est acquis qu’après validation de sa transaction. Le worker revérifie les faits et les droits applicables. Il ne cumule pas les privilèges d’organisations différentes.

Une création complète, avec une catégorie reconnue et les champs obligatoires renseignés, ouvre le seul produit Animation. Une création sans catégorie reste en préparation. Un rapprochement sur une fiche existante respecte ses droits de produit et sa suspension éventuelle. Le résultat distingue la disponibilité pour une animation et le besoin de complétion. La création, l’activation Animation et le rattachement d’une ligne réussissent ensemble. L’import et ses reprises ne créent aucun identifiant Pro, jeton d’initialisation ou email sortant. L’invitation à initialiser l’accès personnel reste une commande explicite.

## Participation, retrait et publication

Animation contrôle l’éligibilité à la sélection et à l’envoi. L’établissement doit être actif, autorisé pour Animation et local ou rattaché à ce réseau. L’autorisation de répondre dans Pro est fondée sur l’identité du commerce destinataire et sa demande. Chaque commerce décide pour la version de sa mission. Le jeu conserve ses propres conditions de publication, de préparation et de validation terrain. Une chasse peut utiliser un commerce extérieur retenu comme étape.

Avant détachement, le CEJ peut identifier les invitations en attente concernées. La confirmation annule les demandes encore en attente de ce CEJ pour cette commune, puis retire le lien. Les accords déjà pris restent attachés à l’animation. Un retrait de participation suit le circuit métier existant avec ses contrôles après publication. Un changement intervenu depuis la confirmation présentée à l’utilisateur doit être revérifié côté serveur.

Live projette l’animation publiée dans la commune de pilotage et les communes publiées où une participation acceptée est effective. La sélection publique conserve l’identité de l’animation quelle que soit la ville consultée. Un habitant qui suit deux villes retrouve une seule fiche et la même inscription. Le retrait effectif du dernier participant d’une ville extérieure retire cette visibilité. La suppression de son seul rattachement au CEJ conserve son engagement. Les notifications aux habitants suivent leurs règles de ciblage actuelles.

## Matrice de recette

### Contrats consommés par Animation

- Gestion du réseau : `GET /protected/referencement/commercants-animation` renvoie `total` pour toutes les pages de la recherche dans le réseau autorisé. La continuation conserve le curseur et l’ordre par nom puis identifiant. `GET /protected/referencement/commercants-animation/communes` accepte une recherche. Le formulaire transmet `commune_commerce_id` à la création. Les réponses de gestion portent `commune_nom` et, pour un lien extérieur, `rattachement_id`. Les contacts d’une fiche partagée suivent la projection autorisée pour le gestionnaire.
- Import : les lignes ajoutent `commune_reconnue` et `activation_animation_prevue` dans l’aperçu. Le résultat inclut `selectionnable_animation`, constat à l’application de la ligne. Une valeur absente ou nulle indique que l’ancien rapport ne fournit pas cette information. Le rapport CSV restitue la disponibilité Animation. Une reprise d’un ancien lot déjà confirmé garde la décision de préparation enregistrée dans son plan.
- Retrait : `GET /{commerce_id}/apercu-detachement` sous la racine de gestion retourne le rattachement et une page d’invitations à envoyer ou en attente (identité de l’animation, libellé, statut). Le client transmet à `POST /{commerce_id}/detacher` le lien, les versions et les couples identifiant/statut qu’il a présentés. Si l’ensemble a évolué, le serveur refuse la confirmation. Le gestionnaire relance **Détacher** pour consulter le nouvel aperçu.
- Sélecteur : la réponse enrichit les métadonnées des fiches avec la commune réelle. Les clients peuvent afficher la localité postale en présence d’une réponse antérieure. Les adresses de participation, les inscriptions et le contrat des notifications habitantes conservent leur forme.

Les préconditions du détachement portent sur l’identité du lien et la liste exacte des invitations et de leurs statuts. Les versions de fiche et de périmètre accompagnent la commande pour compatibilité avec les clients de gestion. Une modification des seules coordonnées du commerce ne bloque pas le retrait. Une réponse du commerçant intervenue entre l’aperçu et la confirmation impose une nouvelle lecture. L’annulation rend l’invitation inopérante, y compris depuis un ancien email. Un email déjà remis au transport peut encore parvenir au destinataire.

### Vérifications par parcours

| Critères | Entrée et preuve attendue | Impact |
| --- | --- | --- |
| HC-01, HC-03, HC-09 | Création et rapprochement manuel, ambiguïté opaque, réimport, concurrence, autre association de la même ville et renouvellement du CEJ | Référentiel, gestion Animation, migration additive et diagnostic du lien |
| HC-02, HC-04, HC-06 | Lot mixte, ligne prête, fiche protégée et ligne incomplète. Contrôler la disponibilité après traitement, l’unicité et les tables de comptes, jetons et emails | Import CSV/XLSX, worker et rapport, guide Animation |
| HC-05, HC-07 | Le CEJ invite le local et l’adhérent extérieur. Le troisième commerce est refusé. Réponse dans Pro, kit, chasse jouée en magasin et agendas dédupliqués | Sélecteurs, Pro, terrain, Live, guide Commerçant |
| HC-08 | Retrait avec invitations en attente, accord préservé, impacts isolés par association et disparition de l’agenda après retrait effectif | Commande de détachement, liste des invitations et projection Live |

## Données et exploitation

La migration v336 crée la relation d’appartenance et ses index. Les commerces historiques conservent leur adresse et leur éligibilité locale. Seul un rattachement explicite ouvre l’accès au réseau extérieur. Appliquer la migration, puis livrer le backend compatible avant les clients. [Migration du réseau de commerçants](../../../../localeo-backend/sql/v336_reseau_commercants_animation.sql)

Pour une ligne d’import ambiguë, relever la référence du lot et la ligne dans l’aperçu, utiliser le circuit de vérification Localeo puis reprendre les lignes concernées avec les droits de la commune de pilotage. Le rapport du lot distingue confirmation, traitement et succès par ligne.

Le jeu de recette comprend un commerce local, un adhérent extérieur et un autre établissement de la même commune extérieure. Suivre la présence dans le sélecteur du CEJ et l’absence d’email à l’import avant de tester l’accord, l’étape et la publication. [Exploitation des démonstrations](../../exploitation/demonstration/exploitation.md)

## Preuves de comportement

La recette locale des 24 et 25 novembre 2026 utilise des bases jetables et des écrans alimentés par des données fictives. L’export OpenAPI hors ligne a été comparé aux contrats de gestion et d’import Animation : 28 opérations et 43 schémas accessibles concordent. Le contrôle des contrats consommés couvre également les routes Référencement utilisées par Animation.

- **HC-02, HC-04, HC-06.** Le test PostgreSQL crée les fiches complètes et incomplètes par le worker d’import, vérifie le produit Animation ainsi que l’absence d’identifiant, de jeton et d’email, puis rejoue le flux. [Import et réimport](../../../../localeo-backend/tests/security/test_imports_commercants_postgres.py)
- **HC-05, HC-07.** La recette PostgreSQL couvre le catalogue du CEJ et Pro sans abonnement dans la commune extérieure. Une deuxième recette va jusqu’à l’attestation de l’étape de chasse chez le commerçant qui a déjà accepté, y compris après son détachement. [Parcours hors commune](../../../../localeo-backend/tests/security/test_adherents_hors_commune_parcours.py)
- **Recherche publique.** Le test navigateur recherche l’animation depuis chacune des deux communes. Il retrouve la même fiche et la même destination d’inscription. Le détail conserve la commune consultée pour revenir aux résultats. Le plan PostgreSQL du sélecteur de préparation a aussi été contrôlé avec 10 000 références par type. [Recherche Marketplace](../../../../localeo-marketplace/tests/visual/discovery-premium.spec.cjs)
- **HC-01, HC-03, HC-08.** La recette de gestion vérifie création, rapprochement, protection des coordonnées et aperçu du retrait. Si une invitation change, le gestionnaire relance le retrait pour revoir les invitations concernées. [Tests PostgreSQL du réseau](../../../../localeo-backend/tests/security/test_gestion_commercants_animation_postgres.py) · [Parcours navigateur de gestion](../../../../localeo-animation/tests/browser/merchant-network.mjs)
- **HC-09.** Le test achète le renouvellement par le service commercial puis vérifie l’éligibilité de l’adhérent à la date de début de la nouvelle période, pour le même partenaire et la même commune de pilotage. [Renouvellement et droits](../../../../localeo-backend/tests/security/test_commerce_droits_integration_postgres.py)
- **Démonstration.** Le générateur a été exécuté sur une base PostgreSQL migrée et isolée. Parmi les trois commerces de référence produits, le sélecteur du partenaire a retourné le commerce local et son adhérent extérieur. [Jeu et assertions de recette](../../../../localeo-backend/tests/integration/test_demo_dataset.py)
- **Supports.** Les deux guides couvrent l’adhésion hors commune et la première connexion. La liste des commerces et l’aperçu d’import ont été capturés sur les données fictives du navigateur. [Guide Animation](../../produit/formation/animation/guide-quotidien-animation.md) · [Guide Commerçant](../../produit/formation/commercant/guide-quotidien-commercant.md)

Les recettes navigateur couvrent 42 scénarios d’import et 10 scénarios de gestion du réseau, sur ordinateur et mobile. Dans les campagnes PostgreSQL élargies, le premier passage a relevé deux jeux de test invalides. Le dossier de retrait utilisait une référence d’animation au mauvais format. Le second écrivain du test de concurrence d’import présentait une adresse vide. Après correction des données, les deux scénarios ont réussi avec leurs assertions de concurrence. [Recette d’import](../../../../localeo-animation/tests/browser/merchant-imports.mjs) · [Recette de gestion du réseau](../../../../localeo-animation/tests/browser/merchant-network.mjs)

### Limites de la recette de démonstration

La campagne PostgreSQL de compatibilité compte 12 scénarios réussis et 2 échecs. Le test du jeu de données complet, y compris sa restauration PostgreSQL et ses lecteurs métier, a réussi sur la version finale. Une recette indépendante du Jeu des vitrines échoue lorsqu’elle tente d’attester un passage après une réponse définitivement erronée. Le moteur refuse cette attestation conformément à sa règle sur les étapes en échec. Ce cas a été reproduit séparément. [Scénario Vitrines](../../../../localeo-backend/tests/integration/test_demonstration_vitrines.py)

Sur le schéma de travail qui comprend aussi l’EPIC 83, le contrôle préalable du générateur signale trois tables de clés d’accès absentes de son registre (`passkeys_pro`, `passkeys_pro_challenges`, `passkeys_pro_etat`). Ce contrôle bloque une opération de démonstration sur ce schéma. La table de rattachement de l’EPIC 84 figure dans le registre. [Registre de démonstration](../../../../localeo-backend/scripts/demonstration/table_registry.json)
