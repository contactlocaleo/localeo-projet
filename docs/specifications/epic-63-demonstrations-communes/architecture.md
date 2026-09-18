# Architecture — générer des données sans adapter le produit

## Principe absolu

L'Epic 63 ne modifie ni `app/`, ni les templates, ni les frontends, ni les
migrations SQL. Elle n'ajoute aucun comportement conditionné à une démonstration.
Le générateur doit s'adapter aux contrats existants. Tout défaut applicatif
découvert est signalé séparément.

Les modèles ORM, fonctions du domaine, services de documents et règles de
vendabilité existants sont appelés avec leurs interfaces normales. Aucun
monkeypatch ni remplacement de méthode n'est livré. Les fonctions pures du
domaine restent la source des calculs ; l'outillage assemble leurs entrées.

## Composants de l'outillage

| Composant | Responsabilité |
| --- | --- |
| `configuration.py`, `operator.py`, `geography.py` | Configuration stricte, cible autorisée et communes résolues. |
| `database.py`, `table_registry.json` | Inventaire, références, export, contraintes et séquences. |
| `content.py`, `editorial.py`, `generator.py` | Contenus réalistes et construction du graphe métier. |
| `images.py`, `assets/`, `pricing.py` | Visuels thématiques locaux scellés et six gammes de prix TTC. |
| `checks.py`, `verification.py` | Appel des règles existantes et cohérence du jeu. |
| `archive.py`, `files.py` | Sauvegarde PostgreSQL, fichiers et restauration d'essai. |
| `operations.py`, `lifecycle.py`, `common.py` | Transferts atomiques, journal privé et reprise prouvée. |
| `access.py`, `guide.py` | Adresses internes, accès ordinaires, QR et conducteur privé. |
| `providers.py` | Préparation optionnelle de vrais objets fournisseurs de test. |
| `cleanup.py` | Rétention et suppression des archives privées résolues. |

## Exécution

Trois bases distinctes sont désignées explicitement : cible de test, builder
vide et base vide d'essai de restauration. Pour une base historique, le profil
`builder_schema: "target"` copie son schéma exact dans le builder. `prepare`
exporte uniquement les définitions SQL et le registre des migrations, depuis
le même instantané PostgreSQL que les références. L'archive privée est liée au
plan par son empreinte. `build` la restaure uniquement dans le builder vide,
puis vérifie l'identité complète du schéma avant de générer les données.

Le mode `migrations`, conservé par défaut pour les anciens profils, rejoue les
migrations existantes. Dans les deux modes, l'outil refuse les tables inconnues,
un schéma incompatible ou un changement de la cible depuis la préparation.

Les références incluent toute la table `api_keys`, avec ses identifiants,
hashes, scopes et états. Seule la date volatile `last_used_at` est ignorée par
la comparaison des références ; son évolution ne modifie pas les droits.
Les fichiers de secrets fournisseurs ne sont pas réécrits par l'outillage.

Les images embarquées sont sélectionnées par clé canonique d'objet. Les
personnalisations éditoriales peuvent remplacer chaque visuel. Le plan fixe
leur SHA-256 ; le build vérifie les fichiers et stocke leurs octets dans le DAM.
Les copies de prestations reprennent le visuel de leur modèle. Les coffrets et
animations disposent de visuels propres. Aucun téléchargement d'image n'a lieu
lors de la génération ou des parcours applicatifs de démonstration.

Les prix des coffrets sont bornés aux six valeurs TTC de 19,90 € à 69,90 € par
pas de 10 €. Les compositions et montants des modèles sont adaptés dans le
catalogue fictif pour préserver la marge et les règles économiques existantes.

Le processus CLI n'importe pas implicitement les fichiers `.env` du dépôt.
L'opérateur fournit ses connexions et la configuration ordinaire BUM/QR de
la cible. La désactivation du bootstrap et du scheduler concerne exclusivement
ce processus CLI ; aucun réglage des applications déployées n'est modifié.

Tous les opérateurs de la cible utilisent le même stockage privé de suivi.
Les verrous PostgreSQL excluent les mutations concurrentes. Le journal et le
fichier de suivi par cible empêchent de démarrer un second run non résolu.
Ils ne sont jamais consultés par les applications.

## Fournisseurs et exploitation

La génération historique n'émet ni email ni paiement rétroactif. Les messages
mis en file par le service normal de facturation sont retirés du builder
avant export. Les contacts générés sont directement des alias internes.

La préparation fournisseur appelle réellement Stripe test et utilise les
colonnes métier existantes pour les comptes Connect et paiements. Elle ne
simule aucun statut fournisseur. Les callbacks empruntent les handlers normaux.

Le remplacement se fait hors ligne, services et producteurs arrêtés.
L'opérateur termine les opérations Stripe en cours et contrôle les webhooks
avant les transferts. Il n'existe aucune quarantaine spécifique dans le produit.
Les présentateurs utilisent une session navigateur propre après chaque échange
de jeu. Le script ne pilote pas le navigateur ni les services.
