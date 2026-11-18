# Risques non résolus — indépendants des votes UX

18 novembre 2026. Référence : [conditions du rapport exécutif](../workshop/rapport-executif.md#conditions-avant-ouverture-a-500-commercants), [limitations réelles](../observations/limitations.md), [arbitrages de conception](../visuels/arbitrages-maquettes.md).

**Aucun P0 produit n’est démontré.** Les risques critiques ci-dessous désignent des conséquences possibles sur les parcours essentiels et des preuves encore manquantes, pas des pannes établies. La validation d’une maquette ne les clôture pas. Aucun risque n’est considéré comme accepté par l’utilisateur à ce stade.

## Risques critiques pour les parcours essentiels

| ID | Qualification et risque | Conséquence possible | Preuve manquante / condition de levée proposée | Orientations et responsables à mobiliser |
| --- | --- | --- | --- | --- |
| R01 | **OBSERVÉ** : QR invalide rejeté ; **DÉDUIT** : confirmation, doublon et reçu existent ; **HYPOTHÈSE** : mauvais résultat ou double effet en usage réel. | Affirmer à tort qu’un passage est validé, ou le compter deux fois. | QR dédiés autorisés, téléphone physique, succès/refus/doublon/double clic, caméra autorisée/refusée et repli manuel ; un seul effet et résultat conforme au serveur. | B1 ; Pro + domaine backend + opérations. |
| R02 | **Non testé** : réponse perdue, expiration, interruption et absence prolongée. | Rejouer une validation, perdre le contexte, afficher une réussite sans preuve. | Coupure avant/après envoi, vérification du reçu sans mutation, reconnexion avec relecture des droits et états, reprise identifiable, aucune réussite locale. | B1/F1 ; Pro + backend. |
| R03 | **OBSERVÉ** : compteurs 2/3, période passée classée en cours, dates brutes ; **cause inconnue**. | Préparer ou valider au mauvais moment, suivre une action non valable. | Diagnostic producteur/consommateur ; compte, périmètre et instant identiques ; bornes et changements de dates Paris ; états incomplet, attente et prêt cohérents. | D1/E1 ; produit + backend + Pro. |
| R04 | **OBSERVÉ** : accès au kit et consignes ; **non vérifié** : fichier, impression et QR. | Supports inutilisables en boutique, mauvais QR, commerce déclaré prêt sans préparatifs. | Téléchargement autorisé en test avec effets connus, ouverture/impression, contrôle du contenu, QR et dates ; séparation téléchargement/installation/déclaration prêt. | E1 ; producteur des documents + opérations + Pro. |
| R05 | **Non testé sur le produit** : lecteur d’écran, zoom, focus et annonces pendant les tâches essentielles ; aucune mesure terrain. | Bloquer une personne peu à l’aise ou utilisant une aide technique, manquer un résultat de validation. | Recette accessible sur les tâches réelles, puis observation de commerçants variés ; corriger les blocages constatés. Les contrôles de la galerie ne remplacent pas cette recette. | Tous ; Pro + accessibilité + recherche/opérations. |

Ces conditions étaient déjà signalées avant une ouverture à 500 commerces. Les requalifier en défaut avéré, incident ou P0 nécessiterait une preuve nouvelle ; aucune n’est produite à cette étape.

## Autres risques opérationnels à conserver

| ID | Constat / limite | Vérification proposée | Portée |
| --- | --- | --- | --- |
| R06 | **OBSERVÉ** : URL fournie initialement vers le portail Animation, refus du compte ; Pro fonctionne à l’URL documentée. Aucun lien produit erroné démontré. | Vérifier le support de diffusion réel de la campagne et le premier accès commerçant. | A1 P2, hors lot de décision P1 ; le risque d’accès n’est pas effacé par ce classement. |
| R07 | **HYPOTHÈSE** : confondre lu/terminé ou perdre une action après absence. Push/email non reçus pendant l’essai, sans panne démontrée. | Action fondée sur un état actuel et autorisé, disponible après lecture ; liens après reconnexion. Tester la réception séparément si ces canaux sont promis. | C1/F1 ; produit + Pro + producteur des notifications. |

## Sujets rejetés : le rejet de la solution ne supprime pas le besoin

Votes simulés au format pour / contre / abstention. Ces résultats ne constituent ni vos refus ni une acceptation du risque résiduel. [Registre des votes](../workshop/votes-et-arbitrages.md) et [arguments détaillés](../workshop/orientations-rejetees.md).

| Alternative rejetée | Vote | Risque de la solution rejetée | Besoin restant et traitement proposé |
| --- | --- | --- | --- |
| B2 · valider automatiquement le QR reconnu | 1 / 11 / 0 | Reconnaissance prise pour validation, confirmation involontaire. | Rapidité en caisse : mesurer le coût de B1, conserver contexte et confirmation. R01 reste ouvert. |
| F2 · succès hors connexion puis synchronisation | 1 / 10 / 1 | Réussite affirmée sans preuve, conflit ou double effet ultérieur. | Continuité en réseau dégradé : résultat incertain, reçu relu, conduite à tenir si vérification impossible. R01/R02 restent ouverts. |
| D2 · fusionner accepté/prêt/approuvé/contrôlé | 2 / 10 / 0 | Masquer la responsabilité et l’étape réellement accomplie. | Lisibilité : prochain geste dominant, détail des états préservé dans D1. R03 et compréhension restent ouverts. |
| E2 · déclarer prêt au téléchargement | 1 / 11 / 0 | Télécharger pris pour imprimer, installer et préparer l’équipe. | Préparation rapide : supports par usage et déclaration explicite dans E1. R04 reste ouvert. |
| A2 · imposer cinq écrans de tutoriel | 1 / 11 / 0 | Barrière avant l’action, gêne pendant le service. | Aide aux débutants : aide courte au moment utile, accès et compréhension à éprouver. R05/R06 restent ouverts ; pas de tutoriel recréé ici. |
| C2 · push quotidien sur tous les non-lus | 0 / 12 / 0 | Fatigue et confusion entre lecture et obligation. | Repérer les tâches : C1 et boîte interne ; aucun canal de réception supposé garanti. R07 reste ouvert. |
| G2 · remplacer systématiquement le scanner par la prochaine tâche | 2 / 8 / 2 | Perdre l’accès rapide à la validation. | Préparation visible et scanner conservé dans D1/F1 ; tester la hiérarchie pendant le service. |

Les quatre premières alternatives touchent directement la fiabilité ou la préparation essentielle. Les trois suivantes portent surtout sur l’accès, la charge de lecture et la cadence ; leur rejet ne suffit pas à les qualifier de risques critiques établis.

## État de suivi

Tous les risques ci-dessus sont **ouverts** ; aucun test supplémentaire de l’application n’a été réalisé à l’étape 4. Les responsables cités sont des rôles à mobiliser, pas des engagements d’équipe. La décision utilisateur sur une orientation est enregistrée uniquement dans [decisions.md](decisions.md). Aucun vote fictif ne peut lever une preuve manquante.
