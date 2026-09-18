# Backlog Epic 12 - Traitement des reversements et export des paiements

## Perimetre

Epic source : `Epic 12. Traitement des reversements et export des paiements`
Reference : [docs/roadmap/product-roadmap.md](../product-roadmap.md)

Objectif historique : outiller le traitement operationnel des reversements deja prepares afin de generer les paiements associes, produire un export exploitable pour un paiement manuel en banque et tracer l'execution de bout en bout.

Decision EPIC 39 : ce flux manuel est completement decommissionne. Il ne doit
pas etre implemente comme cible, fallback ou mecanisme de retrocompatibilite. Les
nouveaux paiements et reversements commercants doivent passer exclusivement par
Stripe Connect.

## Statut global

- Epic 12 : `Abandonne` ; flux decommissionne, classement clarifie le 15 septembre 2026.
- Avancement : contenu conserve comme historique documentaire ; les parcours operationnels manuels doivent etre retires ou neutralises.

## Analyse d'impact

### Synthese

Le socle metier de reversement existe deja :
- la validation d'une prestation cree un `MouvementReversement` en statut `A_REVERSER` ;
- `CreerReversementCommercant` agrege ces mouvements dans un `Reversement` en statut `EN_PREPARATION` ;
- `ExecuterReversement` permet aujourd'hui de finaliser un reversement de facon simplifiee.

Le besoin manquant est le dernier kilometre d'exploitation :
- identifier les `Reversement` prets a etre payes ;
- generer un `PaiementReversement` associe sans integration bancaire automatique ;
- exporter une liste fiable des virements a effectuer dans la banque ;
- permettre ensuite de confirmer ou corriger manuellement l'execution.

### Objectif V1 historique decommissionne

Le mode V1 retenu est un mode :
- `MANUEL_BANQUE`
- pilote depuis le back-office
- avec export de fichier simple, prioritairement `CSV`
- sans integration API bancaire
- avec confirmation manuelle apres execution en banque

## Regles de gestion consolidees

- Un `Reversement` n'est eligible au paiement que s'il est en statut `EN_PREPARATION`.
- Un `Reversement` eligible doit avoir :
  - un `compte_bancaire` actif ;
  - au moins une `LigneReversement` ;
  - un `montant_total` strictement positif ;
  - des `MouvementReversement` tous en statut `EN_COURS_DE_REVERSEMENT`.
- La generation d'un paiement ne doit jamais produire un double paiement pour un meme `Reversement`.
- Le traitement doit etre idempotent : un rejeu sur le meme lot ou le meme `Reversement` ne doit pas creer un nouveau `PaiementReversement` si un paiement ouvert existe deja.
- Un lot peut contenir des reversements de plusieurs commercants.
- En V1, l'export ne declenche pas le paiement bancaire ; il prepare seulement la liste des virements a executer hors systeme.
- Le passage a `PAYE` ne doit intervenir qu'apres confirmation manuelle explicite.
- En cas d'echec ou d'abandon, le systeme doit permettre de conserver une trace sans perdre le lien avec le `Reversement`.
- En cas d'echec, une reprise cree un nouveau `PaiementReversement` ; le paiement precedent reste historise en `ECHEC`.

## Flux historique decommissionne

1. L'operateur exploitation liste les `Reversement` eligibles au paiement.
2. Il selectionne un ou plusieurs `Reversement`.
3. Le systeme cree les `PaiementReversement` associes en statut `A_INITIER`.
4. Le systeme constitue un lot d'export bancaire manuel.
5. Le systeme produit un fichier `CSV` telechargeable avec les informations necessaires au virement.
6. L'operateur execute les paiements dans sa banque.
7. L'operateur confirme ensuite dans Localeo :
   - soit `EXECUTE` avec reference de paiement ;
   - soit `ECHEC` avec motif ;
   - soit maintien en attente si la banque n'a pas encore ete traitee.
8. A confirmation `EXECUTE` :
   - le `PaiementReversement` passe a `EXECUTE` ;
   - le `Reversement` passe a `PAYE` ;
   - les `MouvementReversement` du reversement passent a `REVERSE`.
   - le commercant est notifie qu'un virement va lui etre verse.

## Evolutions de modele recommandees

### `LotPaiementReversement`

Ajouter une entite de lot d'export afin de figer le perimetre d'une campagne de paiement.

Champs recommandes :
- `id`
- `mode_execution` : `MANUEL_BANQUE`
- `format_export` : `CSV`
- `statut` : `PREPARE`, `EXPORTE`, `CLOTURE`, `ANNULE`
- `created_by`
- `date_creation`
- `date_export` nullable
- `commentaire` nullable
- `fichier_export_nom` nullable

Notes :
- un lot sert a regrouper plusieurs paiements prepares ensemble ;
- il permet d'eviter les doubles exports et de garder une trace d'exploitation.

### `PaiementReversement`

Conserver l'entite existante, mais l'enrichir pour le traitement manuel.

Champs recommandes a ajouter :
- `lot_paiement_id` nullable
- `mode_execution` : `MANUEL_BANQUE`
- `date_export` nullable
- `export_reference` nullable
- `exported_by` nullable

Regles :
- un `PaiementReversement` est cree avant paiement bancaire effectif ;
- son statut initial est `A_INITIER` ;
- apres export, il passe a `EN_COURS_MANUEL` ;
- apres confirmation, il passe a `EXECUTE` ou `ECHEC`.

## Contrat d'export historique decommissionne

Format V1 recommande : `CSV UTF-8`

Colonnes minimales :
- `lot_paiement_id`
- `paiement_reversement_id`
- `reversement_id`
- `commercant_id`
- `commercant_nom`
- `titulaire_compte`
- `iban`
- `montant_eur`
- `reference_paiement_suggeree`
- `libelle_virement`

Contraintes :
- une ligne = un paiement de reversement ;
- le fichier doit etre re-exportable a l'identique tant que le lot n'est pas modifie ;
- le separateur est `;` ;
- le nom de fichier suit le format `localeo_reversement_YYYYMMDD.csv` ;
- les montants doivent etre explicites en euros avec 2 decimales, au format `1234.56` avec point decimal et sans separateur de milliers ;
- les colonnes doivent etre exploitables sans retraitement complexe.

## Impacts use cases

Use cases a creer :
- `ListerReversementsEligiblesAuPaiement`
- `PreparerLotPaiementReversement`
- `ExporterLotPaiementReversementCsv`
- `ConfirmerExecutionPaiementReversement`
- `MarquerPaiementReversementEnEchec`
- `NotifierCommercantPaiementReversementExecute`

Use cases a adapter :
- `CreerReversementCommercant` : aucun changement de regle, mais doit rester compatible avec la chaine aval.
- `ExecuterReversement` : a repositionner pour les cas automatiques ou a remplacer par un traitement manuel plus fin en V1.
- consultation commercant des reversements effectues : doit refleter uniquement les paiements confirmes `EXECUTE`.

## Impacts back-office

Surfaces recommandees :
- une page interne dediee de traitement des reversements eligibles ;
- une action de selection / preparation de lot ;
- une action d'export CSV ;
- une vue des `PaiementReversement` avec statuts et references ;
- une action de confirmation manuelle `EXECUTE` / `ECHEC`.

Informations minimales attendues :
- commercant ;
- compte bancaire actif ;
- montant total ;
- nombre de lignes ;
- statut du reversement ;
- statut du paiement ;
- lot d'export associe ;
- date d'export ;
- reference de paiement.

## Securite et audit

- Seuls des operateurs back-office habilites peuvent preparer, exporter ou confirmer des paiements de reversement.
- Aucun export ne doit inclure de donnees inutiles ou sensibles hors besoin bancaire.
- Les IBAN doivent etre visibles uniquement sur les surfaces d'exploitation autorisees.
- Toute action de preparation, export, confirmation ou echec doit etre auditee.

Actions d'audit minimales :
- `reversement.payment.prepared`
- `reversement.payment.exported`
- `reversement.payment.executed`
- `reversement.payment.notification.created`
- `reversement.payment.notification.failed`
- `reversement.payment.failed`

Portee d'audit retenue :
- audit au niveau lot et paiement ;
- `reversement_id` doit etre present dans le payload des evenements concernes.

## User Stories

### Story `PRD-055` - Lister les reversements eligibles au paiement

Priorite : `P0`
Statut : `Termine`

Valeur metier : donner a l'exploitation une vue fiable de ce qui peut etre paye.

Criteres d'acceptation :
- le back-office liste les `Reversement` en statut `EN_PREPARATION` eligibles ;
- un reversement sans compte bancaire actif est exclu ou signale explicitement ;
- la liste expose le commercant, le montant, le compte bancaire cible et le nombre de lignes ;
- un reversement deja associe a un paiement non solde n'est pas repropose a tort.

### Story `PRD-056` - Generer les paiements de reversement a initier

Priorite : `P0`
Statut : `Termine`

Valeur metier : figer les paiements a traiter avant execution bancaire.

Criteres d'acceptation :
- le systeme cree un `PaiementReversement` pour chaque `Reversement` selectionne ;
- le statut initial du paiement est `A_INITIER` ;
- la creation est idempotente et n'engendre pas de doublon ;
- le paiement reste rattache au `Reversement` correspondant ;
- les paiements peuvent etre regroupes dans un lot.

### Story `PRD-057` - Exporter un lot de paiements pour execution manuelle en banque

Priorite : `P0`
Statut : `Termine`

Valeur metier : permettre une execution bancaire manuelle sans ressaisie fastidieuse.

Criteres d'acceptation :
- le systeme genere un fichier `CSV` pour un lot de paiements ;
- chaque ligne contient les informations necessaires au virement ;
- l'export est telechargeable facilement depuis le back-office ;
- une trace du lot exporte est conservee ;
- les paiements exportes passent a `EN_COURS_MANUEL`.

### Story `PRD-058` - Confirmer l'execution manuelle d'un paiement de reversement

Priorite : `P0`
Statut : `Termine`

Valeur metier : garder une verite systeme alignee avec les paiements reels.

Criteres d'acceptation :
- un operateur peut confirmer un paiement comme `EXECUTE` ;
- la reference de paiement bancaire peut etre saisie ;
- le `Reversement` associe passe a `PAYE` ;
- les `MouvementReversement` associes passent a `REVERSE` ;
- un paiement deja confirme ne peut pas etre rejoue.

### Story `PRD-059` - Tracer les echecs et incidents de paiement de reversement

Priorite : `P1`
Statut : `Termine`

Valeur metier : permettre la reprise d'exploitation en cas d'erreur bancaire ou operatoire.

Criteres d'acceptation :
- un paiement peut etre marque `ECHEC` avec un motif ;
- le systeme conserve l'historique du paiement echoue ;
- le reversement n'est pas marque `PAYE` en cas d'echec ;
- la reprise ulterieure reste possible selon une regle explicite.

### Story `PRD-059 bis` - Notifier le commercant lorsqu'un paiement de reversement est valide

Priorite : `P0`
Statut : `Termine`

Valeur metier : informer le commercant qu'un virement va lui etre verse des que Localeo a valide l'execution du paiement de reversement.

Criteres d'acceptation :
- la notification est declenchee uniquement apres confirmation `EXECUTE` d'un `PaiementReversement` ;
- la notification n'est pas envoyee a la preparation du paiement ni a l'export CSV ;
- le commercant recoit une notification sur son email de contact si celui-ci est renseigne ;
- le contenu indique le montant du virement, la reference de paiement si disponible et la date de confirmation ;
- le contenu ne contient pas de donnees client ni de detail bancaire complet ;
- le traitement est idempotent : rejouer une confirmation deja `EXECUTE` ne cree pas de doublon de notification ;
- l'absence d'email de contact cree une anomalie exploitable ou un audit d'echec, mais ne bloque pas la confirmation du paiement ;
- la creation ou l'echec de notification est auditee avec `paiement_reversement_id`, `reversement_id` et `commercant_id`.

## Decisions actees

- Le mode V1 `MANUEL_BANQUE` est decommissionne.
- Le format d'export V1 `CSV` n'est plus un livrable operationnel.
- Les lots V1 doivent etre supprimes dans la cible EPIC 39, l'application n'etant pas en production.
- Le systeme cible ne doit plus generer de paiements avant execution bancaire effective.
- Le statut `EN_COURS_MANUEL` est historique et ne doit plus etre produit par les nouveaux flux.
- La reprise apres echec doit passer par Stripe Connect ou rester bloquee jusqu'a resolution.
- Aucune reference de paiement bancaire manuel ne doit etre saisie dans le parcours cible.
- Le passage a `PAYE` doit etre derive des statuts Stripe Connect et de l'audit applicatif.
- Les lots d'export dedies ne doivent plus etre utilises.
- Le CSV V1 ne doit pas etre conserve comme format operationnel ou archive applicative par defaut.
- Le back-office cible ne doit plus proposer de page ou action d'execution manuelle bancaire.
- L'audit cible est porte par les campagnes Stripe, transfers, payouts, webhooks et reprises Stripe.
- Le perimetre cible exclut preparation, export et confirmation bancaire manuelle.
- Le commercant doit etre notifie selon les statuts Stripe Connect et non apres confirmation bancaire manuelle.

## Hors perimetre V1

- integration API avec une banque ou un PSP de payout ;
- emission automatique de virements ;
- rapprochement bancaire automatique ;
- gestion multi-comptes bancaires complexes par commercant ;
- export aux formats bancaires specialises type `SEPA XML pain.001` ;
- annulation automatique d'un paiement deja emis par la banque.

## Chantiers transverses

### BX-EP12-01 - Evolution du modele de paiement de reversement

Priorite : `P0`

Livrables :
- enrichissement de `PaiementReversement` ;
- eventuelle nouvelle table `LotPaiementReversement` ;
- migration SQL associee.

### BX-EP12-02 - Use cases d'exploitation

Priorite : `P0`

Livrables :
- listing des reversements eligibles ;
- preparation des paiements ;
- export CSV ;
- confirmation d'execution ;
- gestion d'echec.

### BX-EP12-03 - Surfaces back-office et audit

Priorite : `P0`

Livrables :
- vues SQLAdmin ou pages internes ;
- actions de lot ;
- audit des etapes clefs.

## Ordre recommande de livraison

1. `PRD-055`


   - Statut : `Termine`
2. `PRD-056`
   - Statut : `Termine`
3. `PRD-057`
   - Statut : `Termine`
4. `PRD-058`
   - Statut : `Termine`
5. `PRD-059 bis`
   - Statut : `Termine`
6. `PRD-059`
   - Statut : `Termine`

## Tickets historiques non implementables en cible

Ces tickets ne doivent pas etre pris comme backlog cible apres l'EPIC 39. Ils
sont conserves uniquement pour comprendre l'ancien cadrage manuel.

- `EP12-T01` Lister les `Reversement` eligibles au paiement.
- `EP12-T02` Ajouter le modele de lot d'export des paiements.
- `EP12-T03` Enrichir `PaiementReversement` pour le mode manuel banque.
- `EP12-T04` Implementer `PreparerLotPaiementReversement`.
- `EP12-T05` Implementer `ExporterLotPaiementReversementCsv`.
- `EP12-T06` Ajouter la confirmation manuelle `EXECUTE` avec reference bancaire.
- `EP12-T07` Ajouter la gestion `ECHEC` avec motif.
- `EP12-T08` Ajouter les vues et actions back-office.
- `EP12-T09` Ajouter les audits du traitement de paiement de reversement.
- `EP12-T10` Envoyer une notification au commercant apres confirmation `EXECUTE` d'un paiement de reversement.
