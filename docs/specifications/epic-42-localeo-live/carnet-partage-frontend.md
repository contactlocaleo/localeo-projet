# Specification frontend - Carnet Localeo Live persistant et partage entre appareils

> Statut : conception a valider. Cette evolution concerne le module `/live` du projet `localeo-marketplace` et depend des contrats decrits dans `carnet-partage-backend.md`.

## 1. Objectif d'experience

L'utilisateur doit pouvoir :

- continuer a utiliser Localeo Live sans creer de compte ;
- activer volontairement la sauvegarde de son carnet ;
- retrouver les memes passeports/coffrets et participations sur plusieurs appareils ;
- ajouter un appareil en scannant un QR temporaire ;
- recuperer le carnet avec une passkey lorsqu'aucun appareil autorise n'est disponible ;
- identifier et revoquer un appareil perdu ;
- comprendre quelles donnees sont partagees et lesquelles restent locales.

La terminologie visible utilise `carnet`, `appareil`, `synchronisation` et `recuperation`. Les termes `compte`, `connexion`, `profil client` et `mot de passe Localeo` sont exclus de ce parcours.

## 2. Modes du carnet

| Mode | Description | Source de verite |
| --- | --- | --- |
| `LOCAL` | Bibliotheque actuelle, limitee a l'appareil. | IndexedDB. |
| `ACTIVATION` | Creation du carnet et enregistrement du moyen de recuperation. | Etat temporaire local et backend. |
| `PARTAGE` | Carnet persistant accessible depuis plusieurs appareils. | Backend ; IndexedDB sert de cache. |
| `HORS_LIGNE` | Consultation du dernier snapshot non sensible et commandes differees. | Cache IndexedDB minimise ; QR et tokens exclus. |
| `RECUPERATION` | Rattachement d'une nouvelle installation par passkey. | Backend apres verification WebAuthn. |
| `SUSPENDU` | Carnet inaccessible ou en cours de suppression. | Aucun contenu sensible affiche. |

L'activation de la synchronisation n'est jamais implicite lors de l'installation de la PWA, de l'ajout d'un coffret ou de l'acceptation du WebPush.

## 3. Architecture d'etat frontend

Le module Live separe quatre espaces :

1. `installationStore` : identifiant et secret propres a l'appareil ;
2. `localLibraryStore` : bibliotheque historique avant activation ;
3. `sharedNotebookStore` : snapshot, revision et etat de synchronisation du carnet partage ;
4. `deviceSecurityStore` : credential local de protection des QR et preferences de verrouillage.

La passkey de recuperation n'est jamais stockee par l'application. La PWA conserve uniquement les metadonnees non sensibles utiles a l'affichage, le navigateur ou le gestionnaire de mots de passe conservant la cle privee.

Le credential local de protection des QR reste distinct de la passkey de recuperation :

- protection QR : verification locale avant affichage, sans authentification serveur supplementaire ;
- recuperation : assertion WebAuthn verifiee par le backend pour rattacher un nouvel appareil au carnet.

## 4. Navigation et ecrans

### 4.1 Reglages du carnet

Nouvelle section `Mon carnet` dans `Reglages` :

- etat `Seulement sur cet appareil` ou `Synchronise` ;
- date de derniere synchronisation ;
- nombre d'appareils rattaches ;
- action `Sauvegarder et partager mon carnet` en mode local ;
- action `Ajouter un appareil` en mode partage ;
- action `Gerer mes appareils` ;
- action `Gerer mes moyens de recuperation` ;
- action `Arreter la synchronisation sur cet appareil` ;
- action secondaire et protegee `Supprimer le carnet partage`.

### 4.2 Activation de la sauvegarde

Parcours recommande en trois etapes :

1. **Explication** : liste exacte des donnees partagees et locales, sans promesse de compte.
2. **Protection** : creation obligatoire d'une passkey recuperable avec le verrouillage de l'appareil.
3. **Import** : validation et transfert des entrees de la bibliotheque locale vers le carnet.

Message principal :

> Sauvegardez votre carnet pour le retrouver sur vos autres appareils. Aucun compte, email ou mot de passe Localeo n'est necessaire.

La PWA affiche le resultat de l'import : ajoutes, deja presents, invalides ou expires. Elle ne supprime pas la bibliotheque locale avant d'avoir recu et persiste un snapshot serveur complet.

### 4.3 Ajouter un appareil

Depuis un appareil proprietaire :

1. appuyer sur `Ajouter un appareil` ;
2. effectuer une verification locale si la politique produit la retient ;
3. afficher un QR d'appairage, un code temporaire saisissable et leur duree restante ;
4. permettre de revoquer immediatement l'invitation ;
5. afficher la demande recue avec un libelle d'appareil et un code visuel ;
6. confirmer ou refuser ;
7. afficher la reussite et le nouvel appareil dans la liste.

Sur le nouvel appareil :

1. ouvrir `/live/appairer#code=...` apres scan ;
2. lire puis supprimer immediatement le fragment avec `history.replaceState` ;
3. creer une installation si necessaire ;
4. afficher un ecran d'attente et le meme code visuel ;
5. interroger l'etat avec temporisation bornee ;
6. apres confirmation, charger le carnet puis ouvrir `Passeports`.

#### Variante PC ou appareil sans camera

Le mobile affiche sous le QR l'action `L'autre appareil n'a pas de camera` et un code temporaire lisible, par exemple `K7MP-4T9Q-W2DX`.

Sur le PC :

1. ouvrir `/live/appairer` depuis la navigation Localeo Live ou saisir cette adresse courte ;
2. choisir `Saisir un code d'appairage` ;
3. saisir les douze caracteres, les tirets et la casse etant facultatifs ;
4. creer automatiquement l'installation technique du navigateur si elle n'existe pas ;
5. afficher le code visuel de controle et attendre la confirmation sur le mobile ;
6. synchroniser le carnet apres confirmation ;
7. proposer ensuite l'installation de la PWA sur le PC, sans la rendre obligatoire.

La PWA peut aussi proposer `Copier le lien d'appairage` pour les appareils partageant un presse-papiers, mais le code manuel reste toujours disponible et ne depend d'aucune camera, application de messagerie ou adresse email.

Apres cinq erreurs ou a l'expiration, la saisie est bloquee et l'interface demande de generer une nouvelle invitation sur le mobile. Le message d'erreur ne precise pas si un code partiel correspond a une invitation existante.

Le QR et le code d'appairage ne sont pas des QR ou codes personnels de consommation. Ils restent temporaires, ne sont pas places dans le cache du service worker, IndexedDB ou les analytics, et sont masques des que l'invitation expire ou est revoquee.

### 4.4 Recuperer un carnet

L'accueil d'une installation vide propose :

- `Commencer un nouveau carnet` ;
- `Retrouver mon carnet` ;
- `Ajouter cet appareil avec un QR`.

Parcours `Retrouver mon carnet` :

1. expliquer que la passkey doit avoir ete activee avant la perte de l'ancien appareil ;
2. demander les options WebAuthn de recuperation ;
3. laisser le navigateur presenter les passkeys decouvrables ;
4. envoyer l'assertion et l'identite de la nouvelle installation au backend ;
5. apres succes, afficher le nombre de coffrets, participations et appareils retrouves ;
6. proposer `Revoquer les appareils perdus` avec une selection explicite ;
7. synchroniser le carnet ;
8. proposer l'enrolement local necessaire a la protection des QR sur ce nouvel appareil.

La PWA ne doit pas afficher le contenu ou les appareils du carnet avant verification reussie de la passkey.

En absence de passkey disponible :

- expliquer qu'une passkey non enregistree ne peut pas etre recreee par Localeo ;
- proposer le code de recuperation si cet arbitrage est valide ;
- sinon proposer de creer un nouveau carnet et d'y reimporter les liens personnels encore disponibles dans les emails.

### 4.5 Gestion des appareils

Chaque ligne affiche :

- libelle choisi par l'utilisateur ;
- type generique si disponible sans fingerprinting excessif ;
- role ;
- appareil actuel ;
- derniere activite avec une precision limitee ;
- action `Revoquer` selon les droits.

La revocation d'un autre appareil demande une confirmation forte. La revocation de l'appareil actuel avertit que la bibliotheque locale synchronisee et le secret seront effaces apres confirmation serveur.

### 4.6 Gestion des passkeys

L'ecran affiche une liste non sensible : libelle, date d'ajout, derniere utilisation et statut. Il permet :

- d'ajouter une autre passkey ;
- de renommer une passkey ;
- d'en revoquer une ;
- de verifier qu'au moins un moyen de recuperation demeure actif ;
- de generer ou renouveler le code de secours si cette option est validee.

## 5. Synchronisation

### 5.1 Demarrage

1. charger l'installation locale ;
2. afficher immediatement le dernier snapshot disponible ;
3. envoyer `If-None-Match` avec l'ETag local ;
4. remplacer atomiquement le snapshot si le backend retourne une revision plus recente ;
5. mettre a jour l'indicateur `Synchronise`, `En cours`, `Hors ligne` ou `Action requise`.

Le contenu public du feed ne depend pas de cette synchronisation.

### 5.2 Mutations

Chaque commande locale porte :

- un UUID d'idempotence ;
- la revision connue ;
- la date locale uniquement a titre informatif ;
- aucune donnee analytique ou identifiant publicitaire.

Une commande reussie met a jour le snapshot avec la representation retournee par le backend. En cas de `409`, la PWA recharge le snapshot et rejoue uniquement une commande encore pertinente apres confirmation si elle risque d'ecraser un choix distant.

### 5.3 Mode hors ligne

- le dernier snapshot peut etre affiche sans QR ni donnee interdite au cache ;
- l'ajout par token necessite le reseau pour valider la preuve ;
- la suppression ou l'archivage peut etre place dans une file locale explicite ;
- l'interface distingue `Enregistre sur cet appareil` de `Synchronise` ;
- le logout technique ou la revocation vide les donnees partagees locales ;
- le service worker ne traite ni ne journalise les tokens personnels.

## 6. Import et fusion

### 6.1 Passage du mode local au mode partage

Pour chaque entree IndexedDB :

1. lire le token uniquement dans le contexte du parcours d'import ;
2. appeler l'ajout de ressource ;
3. supprimer la variable temporaire apres la reponse ;
4. marquer l'entree comme synchronisee, invalide ou expiree ;
5. recuperer le snapshot final ;
6. conserver localement uniquement ce qui reste requis par les contrats existants pendant la migration.

### 6.2 Nouvel appareil avec une bibliotheque locale

Si l'appareil rejoint un carnet alors qu'il contient deja des entrees locales :

- afficher les volumes avant toute action ;
- proposer `Ajouter mes elements locaux au carnet partage` ;
- valider chaque preuve et dedupliquer cote backend ;
- ne jamais ecraser silencieusement les donnees locales ;
- afficher un bilan des ressources non importables.

### 6.3 Appareil deja rattache a un autre carnet partage

Aucune fusion silencieuse n'est permise. Tant qu'un contrat de fusion backend n'est pas implemente, la PWA bloque l'appairage et propose de revenir au carnet actuel ou de revoquer explicitement cet appareil avant de rejoindre l'autre carnet.

## 7. Affichage des ressources partagees

Les listes `Passeports` et `Mes participations` utilisent les projections autorisees par le carnet. Elles ne demandent pas au nouvel appareil de posseder les tokens originaux.

Une ressource peut afficher :

- `Disponible` ;
- `Archivee` ;
- `Indisponible` avec motif non sensible ;
- `Synchronisation en attente` ;
- `Action requise` si une nouvelle preuve est exceptionnellement necessaire.

Le retrait d'une ressource du carnet affecte tous les appareils. L'interface doit l'indiquer explicitement avant confirmation :

> Ce passeport sera retire de votre carnet sur tous vos appareils.

## 8. Protection des QR

La synchronisation du carnet ne modifie pas `LIVE-ARB-40` :

- chaque appareil realise son propre enrolement WebAuthn local ;
- la passkey de recuperation ne deverrouille pas automatiquement un QR ;
- chaque affichage d'un QR Coffret ou Participant exige une verification locale ;
- le QR est charge apres succes, non cache, puis masque sur changement de visibilite ;
- un appareil recupere doit activer sa protection locale avant son premier affichage de QR.

## 9. IndexedDB

Schema logique cible :

| Store | Contenu |
| --- | --- |
| `installation` | `installation_id`, secret, dates et version de schema. |
| `localLibrary` | Entrees historiques non encore synchronisees et tokens locaux pendant la migration. |
| `sharedNotebookSnapshot` | Carnet, ressources, revision, ETag et date de synchronisation ; aucun token brut. |
| `pendingCommands` | Commandes hors ligne avec idempotency key et revision attendue. |
| `deviceSecurity` | Metadonnees du credential local de protection QR, jamais la cle privee. |
| `uiPreferences` | Commune, filtres, aide et preferences strictement locales. |

Une migration IndexedDB est atomique et reprise en cas d'interruption. Une erreur ne doit jamais supprimer la seule copie d'un token encore non synchronise.

## 10. Etats d'erreur

| Situation | Comportement attendu |
| --- | --- |
| Invitation expiree | Expliquer l'expiration et demander un nouveau QR. |
| Invitation deja utilisee | Ne reveler aucun detail du carnet et recommencer. |
| Confirmation refusee | Effacer le code local et revenir au choix initial. |
| Appareil revoque | Effacer secret, snapshot et commandes locales, puis proposer recuperation ou nouveau carnet. |
| Passkey absente | Proposer le secours valide ou la reconstruction depuis les liens. |
| Assertion annulee | Rester sur l'ecran sans creer de carnet ni d'association. |
| Token de ressource invalide | Conserver l'entree locale avec statut explicite, sans l'ajouter au carnet. |
| Conflit de revision | Resynchroniser et expliquer uniquement si une decision utilisateur est necessaire. |
| Backend indisponible | Conserver le snapshot, interdire les QR non disponibles hors ligne et permettre de reessayer. |

## 11. Accessibilite et ergonomie

- aucune etape ne depend uniquement du QR : un lien d'appairage peut etre copie ;
- un code temporaire saisissable permet l'appairage d'un PC ou d'un appareil sans camera, sans dependance a une messagerie ;
- le code visuel d'appairage est lisible par lecteur d'ecran sans devenir le secret d'acces ;
- les comptes a rebours annoncent sobrement l'expiration ;
- les boutons de confirmation et de revocation ont des libelles explicites ;
- la passkey est expliquee comme `verrouillage securise de votre appareil` avant le terme technique ;
- les etats de synchronisation ne reposent pas uniquement sur une couleur ;
- les animations respectent `prefers-reduced-motion` ;
- le parcours reste utilisable au clavier sur desktop.

## 12. Vie privee et analytics

Evenements autorises sous forme agregee :

- activation commencee, terminee ou abandonnee ;
- appairage commence, confirme, expire ou refuse ;
- recuperation commencee, reussie ou echouee par categorie technique ;
- import local termine avec nombres agreges ;
- conflit et erreur de synchronisation.

Sont interdits dans les analytics : token, secret, credential ID, carnet ID brut, ressource ID personnelle, libelle d'appareil, contenu du carnet et donnees WebAuthn.

## 13. Criteres d'acceptation frontend

- un utilisateur peut activer un carnet partage sans email, mot de passe ou compte Localeo ;
- l'activation exige un moyen de recuperation avant de rendre le carnet partage actif ;
- un appareil proprietaire peut generer une invitation et confirmer un nouvel appareil ;
- un appareil sans camera peut rejoindre le carnet en saisissant le code temporaire affiche par l'appareil proprietaire ;
- le fragment d'appairage est retire avant tout appel tiers ;
- deux appareils affichent le meme ensemble de coffrets et participations apres synchronisation ;
- les preferences WebPush restent independantes ;
- une passkey permet de recuperer le carnet sur une installation vide sans ancien appareil ;
- la recuperation permet de revoquer un appareil perdu ;
- aucune ressource personnelle n'est affichee avant verification reussie ;
- aucune fusion ni suppression silencieuse n'est effectuee ;
- les commandes hors ligne sont idempotentes et leur etat est visible ;
- aucun token personnel ne figure dans le snapshot partage, les logs, le service worker ou les analytics ;
- chaque QR personnel reste protege localement selon `LIVE-ARB-40` ;
- les parcours d'echec, annulation, expiration, incompatibilite et revocation sont testes.

## 14. Decoupage frontend propose

| Lot | Contenu | Dependances |
| --- | --- | --- |
| F9 | Modele local, activation et migration IndexedDB | F2, backend B9 |
| F10 | Synchronisation, appairage et gestion des appareils | F9, backend B10 |
| F11 | Passkeys de recuperation, revocation et recette multi-appareils | F10, backend B11 |

## 15. Hors perimetre

- partage volontaire du carnet avec une autre personne ;
- permissions ressource par ressource entre membres ;
- compte client Localeo ;
- synchronisation des abonnements WebPush et autorisations systeme ;
- recuperation automatique par email ou numero de telephone ;
- fusion automatique de deux carnets partages ;
- prevention des captures d'ecran apres affichage d'un QR.
