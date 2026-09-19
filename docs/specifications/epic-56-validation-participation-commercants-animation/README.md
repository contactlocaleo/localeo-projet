# Epic 56 - Validation de la participation des commercants aux animations

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-56-validation-participation-commercants-animation-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

> Consolidation documentaire du 18 septembre 2026 : versions Backend, Animation et Commerçant réunies. Le complément du 13 septembre sur les lots est intégré comme une évolution explicitement annoncée par sa source. Les différences sur l’aperçu privé du flyer restent signalées, sans arbitrage supplémentaire.

## Objet

Cette Epic remplace l'inclusion implicite des commercants dans une animation par un consentement explicite et tracable. Elle couvre l'invitation, la decision dans l'application commercant, le pilotage des reponses dans Localeo Animation, l'acces au flyer, l'eligibilite des lots et les metriques associees.

## Documents

- [Backlog](../../roadmap/terminees/epic-56-validation-participation-commercants-animation-backlog.md)
- [Conception technique](conception-technique.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Vocabulaire

- **commercant selectionne** : commercant ajoute par le partenaire a la liste de sollicitation ;
- **demande de participation** : proposition versionnee adressee a un commercant pour une animation ;
- **commercant participant** : commercant dont la demande est acceptee ;
- **mission** : metadonnee versionnee de l'animation decrivant les actions et obligations attendues du commercant ;
- **participant public** : projection publique d'un commercant participant, sans donnee relative a sa demande.

## Metadonnee de mission

La mission commercant appartient a l'animation. Elle est portee par le backend dans les metadonnees versionnees de sa configuration, au meme niveau que les `regles`. Le contrat de l'animation expose donc notamment :

- les `regles` applicables a l'instance de l'animation ;
- la `mission_commercant` attendue pour cette animation ;
- le reglement rattache au type d'animation, selon le mecanisme existant.

Le nom technique retenu est `mission_commercant`. Localeo Animation la consulte et la modifie au travers du contrat de l'animation. L'application commercant la consulte dans la demande de participation.

La demande de participation ne possede pas une mission editable autonome. Elle conserve seulement l'identifiant ou l'instantane de la version de configuration presentee au moment de l'envoi, afin de prouver le contenu sur lequel le commercant a pris sa decision.

## Extension de préparation des chasses — à réaliser dans EPIC 55

Le [moteur Chasse, section 8.1.1](../moteur-animation/localeo_animation_engine_spec.md#811-préparation-et-choix-des-missions-commerçantes), étend la mission versionnée à des alternatives par commerçant (TRE-ARB-89). Cette extension cible n’est pas couverte par le statut historique « Terminée » de l’EPIC 56. Elle réutilise ses demandes, droits, échéances, envois et décisions.

La configuration Chasse contient idéalement deux missions candidates par commerce. Après relecture de l’organisateur, l’invitation présente la version concernée. L’acceptation doit sélectionner une mission et confirmer tous ses prérequis (produit, message, mise en place), avec référence de variante et version, auteur/date et audit ; aucun choix ni accord n’est généré par le LLM. La demande conserve sa référence/son snapshot et n’a pas de mission éditable autonome. La préparation effective est vérifiée avant publication ; une mission n’est pas réputée installée parce que le commerce a accepté de la réaliser.

Les conditions de publication et de renouvellement des accords ci-dessous restent applicables. Une modification substantielle du contenu ou des préparatifs invalide l’accord concerné et nécessite un nouvel envoi. Seule la mission retenue intègre le parcours joué ; les alternatives non retenues restent privées. Les refus sont traités dans le brouillon par adaptation ou annulation explicite, sans bascule silencieuse vers une autre mission. Pour chaque chasse, l’organisateur fixe un minimum de commerces retenus avec accord valide et mission confirmée, au moins égal au minimum éventuel du type. En dessous, la publication est bloquée ; adaptation ou annulation restent sa décision explicite. Aucune annulation automatique ni réduction automatique du minimum. Les autres conditions de publication restent exigées, notamment l’absence de demande EN_ATTENTE. Les règles Passeport/Tombola ne sont pas modifiées par cette extension.

## Evolution du modele existant

La liste `configuration.parametres.commercant_ids` ne doit plus etre interpretee comme une liste de participants effectifs. Elle peut servir de liste de commercants selectionnes pendant la transition, mais l'etat metier est porte par une demande de participation persistante.

Modele conceptuel minimal :

```text
Animation 1 --- n DemandeParticipationCommercant n --- 1 Commercant
                         |
                         +-- statut et horodatages
                         +-- reference/snapshot de la version d'animation presentee
                         +-- historique des envois et relances
                         +-- decision et motif facultatif
```

La liste effective est derivee ainsi :

```text
participants_effectifs = demandes(animation_id, statut = ACCEPTEE)
```

Elle devient la source des API publiques, des autorisations de validation chez un commercant et du controle des lots.

## Contenu presente au commercant

La demande doit fournir suffisamment d'informations pour un consentement eclaire :

- nom, type, commune, organisateur et contact ;
- description, dates et horaires utiles ;
- reglement complet et version applicable ;
- mission du commercant, notamment le mode de validation attendu ;
- contraintes particulieres, materiel necessaire et condition d'achat eventuelle ;
- date limite de reponse ;
- informations disponibles sur les lots et le flyer.

La decision enregistre la version de l'animation effectivement presentee, dont sa mission. Une modification substantielle ne doit pas conserver silencieusement une acceptation obtenue sur un autre contenu.

## Notifications et relances

Le premier envoi et chaque relance produisent des sorties distinctes rattachees a la meme demande :

- un email dans l'outbox existante ;
- une notification dans l'espace commercant ;
- une WebPush si une souscription exploitable existe.

L'absence de WebPush ne fait pas echouer la demande puisque l'email et la notification applicative restent obligatoires. Le lien profond identifie la ressource a afficher, mais la decision exige toujours une session commercant authentifiee.

La relance est manuelle, limitee a trois occurrences par demande et soumise a un delai minimal de 24 heures. Chaque relance conserve la demande initiale mais cree de nouvelles sorties afin de garder un historique complet.

## Conditions de publication

La publication est autorisee uniquement lorsque :

- aucune demande envoyee n'est encore `EN_ATTENTE` ;
- au moins un commercant a accepte ;
- le minimum eventuellement defini par le type d'animation est atteint ;
- tous les lots respectent la regle d'eligibilite.

Le partenaire peut relancer une demande, attendre la decision ou annuler une sollicitation en attente. La liste des participants est donc stabilisee avant la publication.

Avant publication, une modification substantielle du reglement, de la mission ou des dates annule les demandes concernees et impose un nouvel envoi. Le commercant peut retirer seul son acceptation avant publication. Apres publication, le retrait passe par le partenaire et declenche les controles d'impact sur le parcours, les lots et la visibilite, avec audit.

La prolongation de la date de fin d'une animation en cours constitue l'exception de compatibilite : elle conserve les participants acceptes, regenere le flyer et les notifie. Elle ne permet pas de modifier simultanement le reglement ou la mission.

Une decision apres la date limite est refusee. Avant publication, le partenaire peut prolonger l'echeance puis relancer le commercant.

## Flyer

Le flyer reste genere et versionne par le socle Animation. Aucun flyer ni apercu n'est disponible dans l'application commercant tant que l'animation n'est pas publiee. La source backend précise qu’un aperçu privé peut être généré par le partenaire en brouillon ; les anciennes copies frontend ne précisent pas cette faculté et leur conception emploie une interdiction de génération avant publication. Cette différence de portée est conservée comme point documentaire à vérifier. Apres publication, l'Epic accorde aux seuls commercants acceptes un droit de lecture, de telechargement et d'impression sur la version courante. Le commercant ne peut ni remplacer le document source, ni modifier une version publiee.

## Lots

La [mise à jour du 13 septembre 2026](avertissement-lots-sans-participant.md) remplace la condition bloquante de rattachement à un commerçant participant par un avertissement.

Les contrôles de catalogue, commune, statut et financement restent applicables. Un coffret sans prestation active chez un commerçant participant peut néanmoins être sélectionné, acheté et offert. Le code `COFFRET_LOT_SANS_PRESTATION_PARTICIPANT` est informatif ; il ne bloque ni le paiement, ni la publication, ni à lui seul le retrait d’un commerçant. Les autres conditions du retrait restent inchangées.

Le diagnostic de couverture est recalculé aux étapes concernées et présente les `commercant_ids_couvrants`. Aucune couverture de tous les commerçants n’est exigée. La conception technique détaille les projections et le message affiché.

## Indicateurs retenus

- taux de reponse : `(demandes acceptees + demandes refusees) / demandes envoyees` ;
- taux d'acceptation : `demandes acceptees / (demandes acceptees + demandes refusees)` ;
- volumes bruts par statut et nombre de relances, toujours affiches avec les taux.

Une absence de denominateur produit un taux de `0`.

## Frontieres de responsabilite

- le Backoffice/backend porte la source de verite, les controles, notifications, documents, indicateurs et l'audit ;
- Localeo Animation configure, envoie, relance, suit les reponses et choisit les lots eligibles ;
- l'application commercant informe, recueille la decision et met le flyer a disposition ;
- la Marketplace ne fait que projeter les participants acceptes et les lots conformes ;
- Localeo Live consomme la projection acceptee sans porter le workflow de consentement.

## Compatibilite et migration

Les animations deja publiees avant cette evolution doivent conserver leurs commercants comme participants afin d'eviter une disparition publique ou un blocage du parcours. La migration recommandee cree pour chacun une demande technique `ACCEPTEE`, horodatee par la migration et marquee comme reprise de l'existant.

Pour les brouillons et animations configurees mais non publiees, les commercants deviennent des demandes a envoyer et doivent repondre avant d'etre consideres participants.

## Decisions fonctionnelles acquises

Les seize arbitrages du registre sont valides. Le motif de refus reste facultatif et n'est visible que du partenaire et du backoffice. La Marketplace ne recoit que la projection des participants acceptes et ne doit exposer ni les demandes, ni les relances, ni les motifs de refus.

## Implementation technique cible

- schema de persistance et contraintes d'unicite ;
- ajout de la metadonnee de mission au schema versionne et aux contrats existants de l'animation ;
- contrats API Localeo Animation et application commercant ;
- integration aux outbox email, notification et WebPush ;
- controle SQL de l'eligibilite des lots et gestion des courses concurrentes ;
- migration des participants historiques selon les regles validees ;
- propagation de la liste acceptee aux projections Marketplace et aux validations terrain.

[Retour à l’index des spécifications](../INDEX.md)
