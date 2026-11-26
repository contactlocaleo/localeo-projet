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

Le [moteur Chasse, section 8.1.1](../epic-55-moteur-animation/localeo_animation_engine_spec.md#811-préparation-et-choix-des-missions-commerçantes), étend la mission versionnée à des alternatives par commerçant (TRE-ARB-89). Cette extension cible n’est pas couverte par le statut historique « Terminée » de l’EPIC 56. Elle réutilise ses demandes, droits, échéances, envois et décisions.

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

## Évolution associée du 24 septembre 2026 — kit et déclaration de préparation

Le statut historique de l’EPIC 56 reste **Terminée**. La nouvelle demande de kit
commerçant, supports joueurs par QR et déclaration « prêt » est suivie dans
[E55-KIT/E55-SUIVI](../epic-55-moteur-animation/conception-technique.md#évolution-du-24-septembre-2026--kit-commerçant-et-préparation-du-démarrage).
Elle distingue le consentement à participer de la réalisation des préparatifs :
le kit appartient au seul commerce de l’invitation acceptée et la déclaration
est liée à cette invitation. Le suivi est facultatif à la création ; lorsqu’il
est actif, il bloque l’ouverture du jeu tant que les commerçants participants
ne sont pas prêts, sauf forçage explicite et tracé par le gestionnaire habilité.
Le [suivi d’implémentation E55](../epic-55-moteur-animation/suivi-implementation.md) porte
ses preuves et limites propres ; la clôture historique ne vaut pas validation
de ce nouveau périmètre.

## E56-UX-01 — préparation commerçant simplifiée (26 septembre 2026)

Le suivi [E73-EVO-SUIVI-ANIMATION du 18 novembre 2026](../epic-73-animation-et-ou-coffrets/parcours-organisateur.md#évolution-du-18-novembre-2026--suivi-animation-et-pro)
complète les accès depuis l’accueil Pro et la présentation des blocages de
publication. SA-01 à SA-03 réutilisent les décisions et préparations E56 ;
acceptation, téléchargement et confirmation restent des faits distincts.

L’évolution rattachée au [backlog E56](../../roadmap/terminees/epic-56-validation-participation-commercants-animation-backlog.md)
remplace les confirmations répétées par deux moments : accepter la participation,
puis préparer le commerce et signaler qu’il est prêt. Elle s’applique aux demandes
génériques et aux missions privées de chasse (E55).

Avant acceptation, les dates, l’organisateur et la mission restent visibles.
Le règlement versionné, la description et les informations complémentaires
restent consultables dans des sections repliables. Le bouton d’acceptation porte
la décision explicite : il n’ouvre plus une seconde confirmation.

Pour une chasse, une seule mission ne requiert plus de sélection ; si plusieurs
missions sont proposées, le choix reste obligatoire. La liste complète des
préparatifs de la mission choisie est visible, suivie d’un accord global non
précoché. Cet accord transmet exactement tous les identifiants de conditions
attendus, avec la version, révision et empreinte présentées. Changer de mission
ou relire après conflit efface cet accord. Le refus et le retrait conservent une
confirmation et un motif facultatif.

Après acceptation, la préparation met le téléchargement du kit et la déclaration
« Je suis prêt » en évidence. Le guide intégral reste dépliable, y compris ses
consignes métier et supports privés : aucune ligne n’est filtrée selon son titre.
Le [complément E80](../epic-80-fiabilite-parcours-localeo-pro/README.md)
présente les bornes du guide en heure de Paris, sans changer les instants ni
assimiler la fin à minuit à une journée entière supplémentaire.
La lecture et le téléchargement ne constituent jamais une déclaration de
préparation. Les droits backend et le suivi facultatif déterminent la présence
de l’action. Le flyer séparé s’ouvre à la demande, selon ses droits existants.

Les commandes restent verrouillées pendant l’envoi. Une réponse incertaine exige
une relecture explicite avant renvoi ; aucun succès ni renvoi automatique.
L’acceptation de chasse conserve son protocole de reçu et sa clé ; la participation
générique et la déclaration « prêt » relisent l’état serveur et conservent leur
clé pour une même intention incertaine.

Impacts : frontend Commerçant et documentation fonctionnelle/formation. Les
propriétaires backend restent `missions_commercantes.verifier_choix`, la demande
de participation et le service de préparation. Aucune règle, permission, API,
donnée ou migration ne change ; les contrats embarqués, autres consommateurs,
ERP, batchs et générateur de démonstration sont sans impact. Les fixtures de
parcours sont adaptées au consentement global et aux informations dépliables.
Aucune configuration ni ordre de déploiement interapplications nouveau ; le
frontend demeure compatible avec le backend existant. Les reprises réseau
restent documentées dans le [guide commerçant](../../produit/formation/commercant/guide-commercant.md).

### Bilan local

Arbres de travail : Commerçant à partir de `574ab07`, Projet à partir de `c2ff6e0`,
branche `feat-moteur-animation`. Les critères E56-UX-01-A à D sont couverts :

- **98 tests Vitest** du périmètre `src/features/animations` réussis : accord global,
  mission unique, choix historique, changement de version, double clic, réponse
  perdue, relecture et préparation distincte.
- **13 scénarios Playwright** réussis (`hunt-missions`, `animation-kit`,
  `animations`, `animation-flyer`) : clavier, mobile/bureau, téléchargement
  authentifié, guide dépliable, réception perdue sans second POST et retour liste.
- Build isolé `scripts/build-browser-tests.mjs` réussi ; captures relues.
- `check_guidance.py` : 87 guides, 869 liens, aucun écart ;
  `sync_documentation.py --check-sources` : 118 documents vérifiés.
- Revue indépendante du consentement et des reprises : aucun point bloquant.

Les anciennes assertions de double confirmation et de flyer immédiatement
visible ont été remplacées par les attentes E56-UX-01, en conservant les contrôles
de droits et de contenu. Les erreurs réseau sont simulées et aucune recette avec
un backend déployé n’est revendiquée. Pas de commit, push ni déploiement dans
ce périmètre ; la clôture historique E56 et le statut E55 restent inchangés.

## E56-EVO-ETATS-PREPARATION — préparation et déclaration distinctes (22 novembre 2026)

Le statut historique **Terminée** de l’EPIC 56 est conservé. Cette évolution
concerne le backend et **Localeo Pro**, côté commerçant. Elle remplace
l’indicateur unique qui confondait contenu, attente d’approbation et déclaration
facultative « Je suis prêt ». Le suivi organisateur Animation garde le sens
déclaratif de `pret_at`.

### Comportements et critères

| Critère | Comportement attendu | Preuve ciblée |
| --- | --- | --- |
| E56-EP-01 | Liste et détail présentent séparément avancement de préparation et déclaration à l’organisateur, prochaine action et acteur ; l’étape 2 rend l’avancement immédiatement visible | Contrat de lecture, résumé Pro, liste → détail |
| E56-EP-02 | Juste Prix distingue à compléter, à proposer, à corriger, attente organisateur et terminé après approbation ; modifier le produit exige une nouvelle approbation | Projection et parcours produit |
| E56-EP-03 | Pour un passeport, une tombola ou une chasse avec des préparatifs, l’étape 2 propose « J’ai terminé ma préparation » et enregistre la date, l’acteur et le contexte. Une reprise explicite remet la préparation à faire. | Domaine, commande, persistance et parcours Pro |
| E56-EP-04 | « Je suis prêt » reste indépendant, facultatif selon le suivi et daté ; terminer l’étape 2 ne notifie pas et ne modifie pas le démarrage | Non-effet sur `pret_at`, notification et garde de démarrage |
| E56-EP-05 | L’accueil signale préparation restante, attente organisateur et déclaration manquante si suivi actif ; raisons cumulables sans doubler le compte d’une préparation | Parité projection/SQL, pagination et accueil |
| E56-EP-06 | Mission, consigne ou support utile changé invalide la confirmation ; consultation, téléchargement et activation du suivi ne la confirment ni ne l’invalident ; un autre commerce ne rend pas la confirmation obsolète | Contexte ciblé, rejeu et suivi |
| E56-EP-07 | Droits et concurrence vérifiés côté serveur ; aucun succès sur résultat incertain ; saisies, navigation et focus préservés | Refus/conflits, isolation, mobile/bureau |
| E56-EP-08 | Guides et contrats synchronisés ; Vitrines conserve quatre étapes, installation et contrôle | Exports, guides rendus et régression |

### Contrats, propriété et compatibilité

Le domaine Animation, auprès de la demande de participation commerçant, possède
la nouvelle confirmation. L’application orchestre chargement, transaction et
audit ; la projection compose les faits sans autoriser une commande.

Les lectures `/commercants/me/preparations` et `/{demande_id}` ajoutent
`avancement`, `declaration`, version et contexte opaque de préparation ; les
champs existants restent compatibles. La nouvelle commande
`POST /commercants/me/preparations/{demande_id}/avancement` reçoit `terminee`,
`expectedVersion` et `contextePreparation`, avec `Idempotency-Key`. Elle est
réservée au compte principal propriétaire de la participation courante acceptée,
pour les jeux sans contenu à approuver, avant échéance et dans une animation
active. Version et contexte sont vérifiés atomiquement. Un reçu ancien ne
constitue jamais une preuve de complétion du contexte actuel.

La confirmation conserve date, acteur et contexte via une migration additive.
Aucune ancienne déclaration n’est transformée en confirmation d’étape 2. Les
changements utiles de mission, consigne ou support rendent la confirmation
obsolète. L’empreinte est limitée à la mission/étape du commerce, son QR,
thème/dates effectives et flyer officiel diffusable (version/empreinte) ; le
contenu d’un autre commerce et le suivi facultatif seul ne l’invalident pas.
Le contrat `/pret`, la
notification transactionnelle `COMMERCANT_PRET` et la garde de démarrage restent
inchangés. Une déclaration enregistrée peut coexister avec une préparation à
revoir. Vitrines conserve ses faits d’installation et de contrôle.

Les filtres d’accueil portent sur les deux axes, pas seulement sur l’acteur
prioritaire historique. Filtrage et comptage distinct des préparations précèdent
la pagination ; les lectures restent bornées et groupées, sans détail individuel
supplémentaire par ligne. L’historique reste consultable sans alerte active.

Pour le passeport, la tombola et la chasse, une consigne de mission explicite,
un flyer officiel diffusé au commerce ou le QR d’une étape de chasse constituent
des préparatifs à confirmer. En l’absence de préparatif, l’avancement est
`NON_REQUISE` et la fiche reste consultable dans la liste complète. Une
déclaration facultative ne compte que si elle est demandée et reste à envoyer.

### Impacts et preuves de livraison

| Critères | Documentation / consommateurs | Données / démonstration | Exploitation / preuves |
| --- | --- | --- | --- |
| EP-01/02/05 | E56 canonique, espace Commerçant, OpenAPI et contrat Pro actualisés | Fixtures : préparation, attentes et raisons cumulées | Réussi localement : projection/SQL, pagination, bornes et mobile/bureau ; rapports ci-dessous |
| EP-03/04/06/07 | Commande Pro ; suivi organisateur conservé | Migration additive vérifiée ; aucun rattrapage depuis `pret_at` ; générateur compatible par champs nullable | Réussi localement : domaine, accès, version/contexte, idempotence et non-notification |
| EP-08 | Guides Commerçant détaillé et quotidien actualisés : accueil, préparation et Juste Prix | Captures réelles sur API synthétique | Réussi : douze pages rendues/relues, égalité PDF et lien applicatif |

**Guide Animation examiné : sans modification pour cette évolution.** Son suivi
déclaratif organisateur conserve actions, libellés et règles. Marketplace, ERP
et batchs ne consomment pas la nouvelle action commerçant ; aucun nouveau
parcours ni configuration n’y est introduit. Les contrats documentaires sont
régénérés par les outils backend.

### Bilan local de l’évolution

**Réalisation et vérifications ciblées locales terminées.** Le statut historique
de l’EPIC 56 est conservé. La passe backend principale finale couvre **96 tests réussis**
(domaine, indépendance de `/pret`, matrice des états, API stricte/rejeu/refus),
rapport `localeo-backend/tmp/preparation-dual-primary-final.xml`, y compris le
refus d’un compte salarié par la politique d’autorisation. Les contrôles
d’architecture ont **772 tests réussis**, puis la passe finale de contrats de
modules a **767 tests réussis**. La persistance et la migration passent
**106 tests SQLite/PostgreSQL**, sans skip, dans
`localeo-backend/tmp/preparation-dual-infra-final.xml`. Les trois tests
consommateurs Animation du suivi et de publication sont réussis.
Les passes antérieures ne sont pas additionnées à ces nombres.

Côté Pro, les **92 tests unitaires ciblés** des six fichiers sont réussis,
sans skip, dont le normaliseur, les deux états, l’accueil, le kit et le contrat
OpenAPI de la nouvelle commande. Rapport :
`localeo-commercant/tmp/preparation-dual-unit-targeted-final-rested.json`.
Le rapport navigateur final unique confirme **10 scénarios réussis, zéro skip,
zéro échec et zéro flaky** : sept parcours de préparation, deux de kit et un
suivi sans déclaration facultative. Il couvre notamment Juste Prix,
**Mes actions**, contexte obsolète, rechargement des consignes du nouveau
contexte, conservation de l’étape consultée, mobile et texte agrandi. Build
synthétique et Axe réussis ; captures finales relues. Rapport :
`localeo-commercant/tmp/preparation-dual-ui-report-final-unified/results.json` ;
captures : `localeo-commercant/tmp/preparation-dual-ui-results-final-unified`.

**Limite de régression : la suite générale Pro a été interrompue après plus de
douze minutes et n’est pas validée.** Un timeout du test d’accueil « Animation
seule : accueil sans paiement, prestations ni requête financière » a été
reproduit sur le HEAD antérieur
`e27ffec8831f4252edd31af799a13c334ff9d33e`, observation dans
`localeo-commercant/tmp/preparation-dual-baseline/observation.json`. Les autres
timeouts de la première tentative ne sont pas qualifiés de préexistants.
Deux anciennes assertions de présentation du kit ont été comparées à ce HEAD
(`tmp/preparation-dual-kit-comparison.json` dans Pro), puis alignées sur les
consignes déjà visibles. Les contrôles de téléchargement sans déclaration,
QR, reprise et idempotence ont été conservés et passent dans le rapport final.

Mesure locale PostgreSQL à 10/100 préparations : **11 lectures constantes** et
**5 lignes hydratées** par page d’accueil. Les plans SQL de la page sont
mesurés à **3,713/25,664 ms** ; les lectures complètes mesurent
**1 240,211/1 690,820 ms** dans cette passe locale. Ces valeurs restent propres à une fixture de schéma
allégé, pas une qualification de capacité en exploitation. Rapport :
`localeo-backend/tmp/preparation-dual-infra-mesures-postgresql.json`.

Pour EP-08, guide Commerçant source et captures accueil/étape 2
actualisés ; PDF de douze pages rendu et relu, copie embarquée identique.
La recette locale du lien a réussi à 390 et 1440 px : navigation, focus,
assistance indisponible, HTTP 200, octets du PDF et zéro violation Axe.
La fixture navigateur vérifie aussi qu’une déclaration déjà enregistrée sans
nouvelle attestation laisse l’étape 2 à compléter, avec sa commande disponible.
[Commandes et provenance](../../produit/formation/commercant/illustrations/guide-quotidien/README.md#e56-evo-etats-preparation--22-novembre-2026).
Contrôles Projet exécutés : `py -3.14 scripts/check_guidance.py` (122 guides,
1 868 liens, zéro erreur/avertissement) et
`py -3.14 scripts/sync_documentation.py --check-sources` (155 documents).
La migration `sql/v330_avancement_preparation_commercant.sql` ajoute trois
colonnes nullable sans rattrapage et un contrôle de cohérence date/acteur/contexte.
Inspection du générateur : la création des
demandes dans `scripts/demonstration/generator.py` omet ces champs et `pret_at`,
donc ne fabrique aucune attestation. Aucun changement de générateur ni aucune
génération sur un environnement installé ; compatibilité de cette insertion
inspectée, génération/restauration complète non exécutée dans ce périmètre.
Ordre de livraison : appliquer **v330**, livrer le backend puis Localeo Pro.
La coexistence avec les anciens consommateurs est conservée par les champs
additifs ; aucune variable de configuration nouvelle. L’export des contrats
canoniques et embarqués accompagne le code producteur/consommateur.
Aucun déploiement, commit ou push déclenché.
Les serveurs des recettes locales sont arrêtés. Aucune activation distante ni
recette sur appareil réel ou avec un backend déployé n’est revendiquée.

## E56-EVO-ACHAT-PASSEPORT — condition d’achat du Passeport (24 novembre 2026)

Le modèle standard sur TEST exigeait un achat sans montant minimum à chaque
passage. L’organisateur pouvait régler le seuil de validation et adapter la
mission destinée aux commerçants. Le règlement et les conditions publiques
reprenaient la condition d’achat du modèle.

L’organisateur choisit désormais une condition commune à tous les passages du
Passeport, à la création et en configuration. **Achat requis** conserve la
règle historique, avec un achat sans montant minimum. **Visite sans achat**
autorise le commerçant à valider le passage à l’occasion d’une simple visite.
Dans les deux cas, le commerçant atteste le passage par le circuit de
validation habituel. Un passage validé par commerce compte vers le seuil.
Les autres clauses du règlement sont conservées. Une clause d’achat
explicitement incompatible avec le choix fait refuser l’enregistrement.

### Critères et preuves attendues

| Critère | Comportement attendu | Vérification |
| --- | --- | --- |
| E56-AP-01 | À la création et en configuration, le gestionnaire autorisé voit les deux options. **Achat requis** est prérempli. La valeur choisie est conservée après enregistrement et reprise. | Parcours navigateur à la création, reprise de préparation et modification d’un brouillon, sur téléphone et ordinateur. |
| E56-AP-02 | Le domaine du Passeport porte le choix sous `regles.achat_requis`, un booléen. Une configuration historique sans ce champ conserve la règle d’achat applicable. L’édition respecte les droits existants. La publication vérifie la version de configuration et fige la condition acceptée. | Tests de normalisation, charge utile invalide, version de publication obsolète et refus après publication. |
| E56-AP-03 | La condition choisie apparaît dans la mission communiquée au commerçant, le règlement et les conditions publiées dans Localeo Live. Le changement invalide les accords portant sur la condition précédente. L’organisateur renvoie les invitations concernées pour recueillir l’accord sur la version qui sera publiée. | Vérifier les deux valeurs dans les documents communiqués. Simuler un accord, changer de condition, puis vérifier le nouvel envoi et le nouvel accord. |
| E56-AP-04 | Chaque validation effective reste une attestation par un commerçant autorisé. Le seuil, l’unicité de la validation par commerce et les chances suivent les règles du Passeport. | Tests du moteur et des refus existants, avec un seuil franchi sous les deux conditions. |

### Impacts de livraison

| Périmètre | Vérification prévue |
| --- | --- |
| Domaine et parcours | Le backend produit les textes à partir de la condition stockée. Animation saisit et relit le choix. Pro et Live restituent les consignes et le règlement fournis par le serveur. Le [contrat du moteur Passeport](../epic-55-moteur-animation/localeo_animation_engine_spec.md#431-configuration-et-invariants-du-passeport) conserve la qualification actuelle. |
| Données et démonstration | Le choix est stocké dans les règles JSON de la configuration existante. Tester la lecture d’une configuration ancienne, la conservation des instantanés déjà publiés et la cohérence des textes d’un Passeport démo avec sa condition. |
| Guides | Actualiser les guides Animation et Commerçant et leurs copies distribuées. Le premier décrit le réglage dans le portail et le second précise ce que le commerçant vérifie au moment de valider. |
| Exploitation | Livrer le backend puis le portail Animation et le guide embarqué de Localeo Pro. Vérifier deux Passeports avec les deux conditions et comparer l’invitation à la fiche et au règlement publics après publication sur un environnement de recette. |

### Vérifications des consommateurs

- Live (`f12035d`) : neuf tests réussis avec
  `node --test tests/security/live-public-detail-presentation.test.cjs`, dont
  la restitution des conditions publiques d’achat et des textes sans achat.
- Pro (`f5c8fd5`) : 183 tests réussis avec
  `npm test -- src/features/animations/contracts.test.js src/features/animations/pages/ParticipationRequestDetailPage.test.jsx src/features/animations/AnimationPages.test.jsx`.
  La lecture des invitations, du règlement et de la mission utilise les
  champs déjà fournis par le serveur.

### Recette locale de l’organisateur

- Animation (`475e063` avec les modifications de cette évolution). `pnpm typecheck`,
  `pnpm lint`, `pnpm test` et la construction avec `scripts/build-pwa-tests.mjs`
  réussis. La suite Node compte 431 réussites.
- `tests/browser/qualification-threshold.mjs` réussit les douze combinaisons du
  Passeport, du Jeu des vitrines et du Juste Prix à 320, 390 et 1 280 px et à
  1 280 px avec le texte à 200 %. Le scénario parcourt les deux formulaires,
  vérifie le choix au clavier, le PATCH suivi d’une relecture et la requête de
  création à partir du récapitulatif. `tests/manual-preparation.test.mjs` vérifie
  aussi la sérialisation et la reprise du choix sans achat.
- Le guide Animation a été régénéré, ses dix-huit pages rendues et relues.
  `pnpm guide:check` et `tests/browser/animation-guide.mjs --access-only`
  confirment la copie embarquée et l’accès au PDF depuis le build local.
- Les treize pages du guide Commerçant ont été rendues et relues. L’illustration
  du chapitre 7 montre la navigation et les états de préparation. Le contrôle
  `guide:check` et `scripts/capture-merchant-guide.mjs --check-guide --verify-only`
  confirment le PDF et son accès à 390 et 1 440 px depuis le build synthétique.

### Recette locale du backend

- Backend (`47293b1d` avec les modifications de cette évolution). Le lanceur
  `scripts/validation/test_isolated.py` valide les deux conditions et le refus
  après publication dans `test_achat_passeport.py`. Les tests ciblés de
  préparation manuelle, d’invitations, de catalogue public et de lecture Pro
  passent dans la même campagne de 103 tests. `test_publication_api_t3.py`
  ajoute 14 vérifications du contrat de publication, dont la version exigée.
  Les 783 contrôles d’architecture et de couverture des classes de domaine
  passent avec le même lanceur isolé.
- `test_seuil_qualification_audit.py` vérifie les deux conditions et le cas
  historique, ainsi que l’exclusion des doublons et des commerces hors du
  parcours. Le scénario PostgreSQL de `test_generation_animation_postgres.py`
  couvre la conservation du choix lors de la réutilisation d’un template.
- Le générateur utilise le mode **Visite sans achat** pour les nouveaux
  Passeports de démonstration et produit le règlement et la version associés.
  Le test `test_generator_links_publications_executions_and_consents_to_the_current_model`
  l’a vérifié sur une fixture isolée. Le champ étant stocké dans les règles
  JSON existantes, aucune migration SQL n’est requise.
- La campagne de démonstration sur PostgreSQL 18 jetable a terminé dix cas
  avec succès et reproduit l’échec préexistant de Vitrines Pâques avec passage
  sur `47293b1d`. Le scénario de réinstallation/restauration a été interrompu
  au bout d’une vingtaine de minutes de campagne et les deux derniers cas
  restent non exécutés. Le journal local est dans
  `localeo-backend/tmp/passeport-achat-demo/exit.txt`. Les serveurs sont arrêtés.
  Dans la suite unitaire élargie, l’échec de
  `test_proofs_require_a_participating_merchant_and_an_open_period` est aussi
  reproduit sur `47293b1d`.
