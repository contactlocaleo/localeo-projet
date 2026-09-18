# Bilan du recentrage de l'Epic 63

Date : 12 septembre 2026. Ce bilan remplace celui du mode applicatif de démonstration.

## Résultat

La génération fonctionne comme un outillage autonome. Les modèles, règles,
services et rendus du produit sont réutilisés sans adaptation de leur code.
Le principe absolu est inscrit dans [AGENT.md](../../../../localeo-backend/AGENT.md), dans les
instructions du générateur et dans le backlog.

Les adaptations du backend, de ses templates, de la Marketplace, de Localeo
Commerçant et de Localeo Animation ont été retirées. L'endpoint de contexte,
le middleware, les filtres fournisseurs, les modifications de sessions/QR,
le badge et le marquage PDF spécifique sont supprimés. La migration de contrôle
du runtime est supprimée. Le builder peut reproduire le schéma existant de la
cible historique ou rejouer les migrations ordinaires, sans nouvelle migration.

Les modifications préexistantes hors Epic 63 sont conservées.

## Outillage conservé et adapté

- Configuration privée, résolution de commune et de trois voisines.
- Catalogue réaliste, versions de prestations, coffrets, BUM, historique
  d'achats, finance, animations, participants, gains, support et actualités.
- Calculs et validations par les fonctions et services ordinaires.
- Adresses internes distinctes directement inscrites dans les données,
  sans filtre ou renvoi applicatif.
- QR au format et avec le trousseau habituel de la cible.
- Suppression des notifications historiques du builder avant export,
  sans modifier le service normal qui les met en file.
- Sauvegarde complète et essai réel de restauration, import atomique,
  séquences restaurées et journal privé hors base.
- Nouveau jeu d'identifiants et d'accès à chaque reconstruction ; reset
  refusé pour une génération déjà utilisée.
- Préparation optionnelle de vrais comptes Connect et contreparties Stripe test,
  avec manifeste privé ; aucun simulateur et aucune table fournisseur spécifique.
- Conducteur privé et archives par génération.

La file de réévaluation alimentée par les triggers normaux est restaurée en
dernier dans le transfert, afin de retrouver exactement son contenu d'origine.
Aucun trigger n'est désactivé ni modifié.

## Vérifications

Le complément explicite des mentions manquantes du profil émetteur est couvert
par deux tests unitaires et par le cycle PostgreSQL complet : le jeu utilise
les mentions complétées, puis la restauration retrouve le profil initial
incomplet sans perte. Cette passe a réussi en **214,93 secondes**. La première
construction Latresne a également réussi en **45,90 secondes**, avec 4 communes,
16 commerçants, 18 coffrets, 10 animations, 60 achats et 100 inscriptions.
Ces vérifications locales ne constituent pas une installation ni une recette
des paiements sur l'environnement de test connecté.

La préparation sur la recette historique a conduit à ajouter un mode de copie
du schéma dans le builder : aucun alignement ni changement de la cible n'est
nécessaire. Le test PostgreSQL reproduit une colonne et un index historiques,
vérifie le rejet d'une archive de schéma altérée, puis le cycle complet
d'installation et de restauration (**9 tests réussis en 210,67 secondes** avec
les tests unitaires de configuration/références). Les tests des commandes
PostgreSQL et des archives passent également (**4 tests**), notamment pour les
options de lecture seule contenant des espaces et les mots de passe conservés
hors arguments de commande.

Les tests de cette version couvrent configuration, alias, fichiers locaux/S3,
schéma sans runtime de démonstration, profil complet et lectures métier.
La génération est aussi contrôlée pour ne modifier aucun fichier applicatif
suivi dans `app/`, `templates/` ou `sql/`.

Le cycle PostgreSQL utilise trois bases jetables créées depuis les migrations
ordinaires : construction, dump, restore d'essai, import, nouvelle génération,
refus de réutiliser les identifiants, interruption après chargement et restauration
exacte de la recette originale. Il vérifie le verrou concurrent, le rejet d'une
archive corrompue et la reprise fondée sur les lignes et séquences après un
commit dont le reçu a été interrompu.

La passe finale du recentrage a donné **12 tests réussis en 229,77 secondes**,
y compris la reprise après interruption du reçu de commit et le contrôle des
empreintes des fichiers applicatifs. La compilation Python et la vérification
des différences Git passent également. Deux avertissements de réflexion
SQLAlchemy subsistent sans échec de validation.
Deux constructions de la passe précédente ont été mesurées à **40,58 et 39,31 secondes**, hors
sauvegarde/fournisseurs. Les 98 tests et builds de l'ancien bilan concernent
l'architecture retirée et ne servent pas de preuve à cette version.

## Exploitation

Aucun déploiement applicatif ni migration spécifique n'est requis pour utiliser
le script sur un environnement disposant déjà des fonctionnalités nécessaires.
La configuration normale de la cible reste à fournir au CLI, notamment pour
BUM et les QR.

L'arrêt/reprise des services, la vérification des opérations fournisseur et
webhooks en cours ainsi que les sessions navigateur propres relèvent de la
procédure d'exploitation. Aucun mécanisme de quarantaine, rejeu, filtre de
notification ou nettoyage de cache n'est ajouté au produit.

Les cinq parcours avec fournisseurs connectés et le chronométrage du Passeport
restent à effectuer avant la première séance. La base de test partagée n'a pas
été modifiée. Les commits, push et déploiements ne sont pas exécutés par ce
recentrage.
