# Epic 50 - Politique BUM et conformite fiscale des coffrets

> Suivi produit au 18 septembre 2026 : **Terminée** — [backlog de référence](../../roadmap/terminees/epic-50-conformite-fiscale-bum-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Etat

`Implementation backend terminee`. Les validations externes explicites restent
des prerequis d'activation et ne sont pas presentees comme obtenues.

## Objet

Cette Epic introduit une politique fiscale transverse pour les coffrets Localeo. Elle separe quatre evenements : acquisition d'un bon, emission du droit digital, execution de la prestation et facturation eventuelle de cette prestation.

Etat au 1er septembre 2026 : le socle backend et le parcours `Localeo OnBoard`
`PRD-551` a `PRD-559` sont implementes. La PWA interne disponible sur
`/internal/onboard` couvre le portefeuille, le referentiel, la checklist
conditionnelle, les preuves documentaires securisees, les prestations, la
preparation financiere, l'invitation, le test d'acces et la cloture par
capacites serveur. Elle ne publie ni ne qualifie un coffret. Le wording
definitif du justificatif, la liste documentaire `BUM-ARB-45`, les champs
Chorus Pro et les validations externes Juridica/Finance restent des conditions
d'activation. Le backend de l'assistant de facturation commercant `PRD-560`
est implemente derriere un indicateur desactive ; son activation reste
conditionnee a la validation Juridica/comptable de `BUM-ARB-49`.
Le mandat commercant et le suivi manuel Chorus Pro `PRD-469` sont egalement
implementes derriere `LOCALEO_FEATURE_CHORUS_MANUAL_DEPOSIT_ENABLED`. La file
commune de `PRD-468` prend en charge les factures commercants et Localeo.
Le socle de facturation Localeo `PRD-470/473`, la facture de commission
`PRD-471` et le backend de souscription `PRD-472` sont implementes derriere
`LOCALEO_FEATURE_LOCALEO_INVOICING_ENABLED`. Le webhook Stripe de souscription
est raccorde ; l'activation attend la validation comptable et la recette.
Le credit d'achat B2B et les demandes groupees Pro `PRD-474` a `PRD-478` sont
implementes par `v209` a `v214`, derriere
`LOCALEO_FEATURE_B2B_PURCHASE_CREDIT_ENABLED`. Le registre, les reservations
FEFO, les sessions code + OTP, le paiement mixte, les restitutions a echeance
d'origine, les corrections de facture groupee, le rattachement des achats Pro
et les vues Pro/Animation sont disponibles. Le flag reste desactive jusqu'aux
validations Finance/Juridica et a la recette Stripe.

Hypothese de depart validee : des coffrets existent techniquement, mais aucun n'a encore ete ouvert a la commercialisation. La migration auditable `v191` les initialise automatiquement en `MULTI_PURPOSE / VALIDATED`. Aucune revue manuelle ni periode transitoire n'est requise. Une fois les indicateurs actives, les controles BUM s'appliquent des la premiere publication et toute modification significative ulterieure impose une requalification.

## Documents

- [Backlog Epic 50](../../roadmap/terminees/epic-50-conformite-fiscale-bum-backlog.md)
- [Specification fonctionnelle](specification-fonctionnelle.md)
- [Specification Localeo Commercant](localeo-commercant.md)
- [Specification Localeo Marketplace](localeo-marketplace.md)
- [Specification Localeo Animation](localeo-animation.md)
- [Specification Localeo Live](localeo-live.md)
- [Checklist contractuelle BUM, TVA et facturation](checklist-contractuelle-bum-facturation.md)
- [Analyse de l'existant et impacts](analyse-existant-impacts.md)
- [Conception technique](conception-technique.md)
- [Credit d'achat B2B sur coffrets expires](credit-achat-b2b.md)
- [Onboarding commercant mobile](onboarding-commercant-mobile.md)
- [Justificatif d'achat et demandes de facture](workflow-demandes-factures.md)
- [Factures emises par Localeo](factures-localeo.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Decoupage documentaire valide

Le decoupage actuel est conserve car chaque document porte une responsabilite
distincte : le backlog pilote les lots et leur statut, la specification
fonctionnelle porte les exigences `E50-RG-*`, la conception technique decrit
les composants et migrations, le registre fixe les decisions, les guides
specialises detaillent credit, facturation et OnBoard, et la checklist
contractuelle reste la source des validations externes. Une evolution metier
doit mettre a jour backlog, exigence et conception dans le meme changement.

Les quatre specifications applicatives ajoutent une vue d'implementation par
client sans dupliquer la doctrine commune. Elles fixent les ecrans, parcours,
contrats API, erreurs, criteres d'acceptation et dependances propres a chaque
application. En cas d'ecart, la specification fonctionnelle et le registre
d'arbitrages restent les sources metier ; le contrat OpenAPI du backend reste
la source technique des routes effectivement disponibles.

## Matrice des responsabilites applicatives

| Fonction | Commercant | Marketplace | Animation | Live |
| --- | --- | --- | --- | --- |
| Afficher les coffrets vendables | Non | Oui | Oui | Non |
| Qualifier ou valider le BUM | Non | Non | Non | Non |
| Afficher le justificatif d'acquisition | Non | Oui | Oui | Redirection |
| Creer une demande de facture | Traite | Oui | Oui | Non |
| Fournir/emettre la facture commercant | Oui | Non | Non | Non |
| Consulter la facture commercant | Non | Oui | Oui | Notification/redirection |
| Consulter les factures Localeo | Commission | Non | Souscription | Non |
| Consulter/utiliser le credit B2B | Non | Pro uniquement | Oui | Non |
| Gerer le mandat Chorus commercant | Oui | Non | Non | Non |
| Afficher le statut Chorus partenaire | Non | Non | Lecture seule | Non |

### Passages entre applications

1. Marketplace ou Animation cree l'achat et expose le justificatif.
2. La validation de prestation rend une ligne eligible a la facturation.
3. Marketplace ou Animation cree la demande, separee par commercant.
4. Localeo Commercant traite la demande et fournit la facture.
5. Marketplace ou Animation expose le document au demandeur.
6. Localeo Live peut notifier le beneficiaire et le rediriger vers la vue
   Marketplace, sans porter lui-meme le document ou le secret d'acces.

### Raccordements backend restant visibles dans les specifications

- acces Marketplace securise au justificatif d'acquisition deja genere ;
- profil factuel `me` pour Localeo Commercant ;
- profil de facturation partenaire et projection Chorus en lecture seule pour
  Localeo Animation ;
- categorie `FACTURATION` et projecteur d'evenements vers Localeo Live.

Ces raccordements ne remettent pas en cause l'etat du socle Epic 50. Ils sont
les contrats de presentation necessaires pour livrer les quatre clients sans
utiliser de route BackOffice ou de contournement non securise.

## Positionnement dans l'existant Localeo

L'Epic 50 est une evolution transverse du socle existant, pas une nouvelle chaine metier parallele. Elle reutilise le controle central de vendabilite, les versions de prestation, `AchatCoffret`, `CommandeAchat`, `CoffretInstance`, `ValidationPrestation`, les mouvements de reversement, Stripe Connect, les snapshots et les documents d'achat.

Elle inclut aussi un parcours terrain pour l'equipe commerciale. L'application
mobile interne orchestre les memes cas d'usage afin de completer le dossier,
collecter les contrats signes, qualifier les blocages et verifier l'acces au
portail pendant le rendez-vous. Elle ne duplique ni le referentiel commercant,
ni les prestations, ni les decisions BUM.

Le principal remplacement concerne la facturation commercant de l'Epic 14 : la generation de nouvelles factures par commercant et par achat avant consommation est neutralisee. Le workflow actif cree une demande de facture rattachee aux prestations effectivement validees. Le recu de paiement existant, deja presente comme non fiscal, sert de base au justificatif d'acquisition BUM.

## Architecture conceptuelle initiale

```text
Partenaire + convention       Prestation + donnees factuelles
             \                    /
              diagnostic interne
                        |
             decision admin sur le coffret
                        |
       Coffret MULTI_PURPOSE + VALIDATED
                        |
        commande -> justificatif d'acquisition
                        |
              coffret emis / fonds en attente
                        |
             consommation QR validee
                   /             \
    mouvement reversement     commission
                   \
      demande de facture rattachee
       a ValidationPrestation
                   |
          facture du commercant
```

## Frontieres de responsabilite

| Sujet | Localeo | Juridica / commercant |
| --- | --- | --- |
| Screening | Collecte, evalue et explique | Juridica valide la politique |
| Qualification | Trace la decision habilitee | Decision selon gouvernance validee |
| Justificatif d'acquisition | Genere le document | Wording fiscal valide par Juridica |
| Facture de prestation | Orchestre la demande, fournit l'upload ou un assistant de brouillon et trace l'emission | Le commercant verifie les donnees fiscales et declenche l'emission sous sa responsabilite |
| Commission Localeo | Emet une facture consolidee au commercant depuis un snapshot fiscal immuable | Donnees de facturation fournies et maintenues par le commercant |
| Abonnement Animation | Emet et met a disposition la facture Localeo au partenaire | Coordonnees de facturation fournies par le partenaire |

## Principes de conception

- aucune equivalence technique entre `SOLO / MULTI` et `BUU / BUM` ;
- aucun `UNKNOWN` transforme en BUM par defaut ;
- regles et decisions versionnees, snapshots immuables ;
- migration des coffrets existants avec `qualifiedBy = SYSTEM_MIGRATION`, motif `INITIAL_CATALOG_BOOTSTRAP` et version de politique initiale ;
- predicat de publication unique reutilise par tous les canaux ;
- depublishing coherent lors d'une requalification requise ;
- contraintes anti-doublon garanties en base, pas seulement dans l'interface ;
- documents et donnees de facturation cloisonnes par acheteur et commercant ;
- modele extensible vers facturation electronique sans l'inclure en V1 ;
- assistant facultatif : aucun numero ni document final avant confirmation
  explicite du commercant ;
- aucune duplication de `ValidationPrestation`, `MouvementReversement`, `CommandeAchat` ou du moteur documentaire existant sans ecart fonctionnel demontre ;
- remplacement explicite de la generation de facture commercant a l'achat prevue par l'Epic 14.

## Lots de conception livres

1. modele de domaine, schema de persistence et migration idempotente du catalogue technique ;
2. moteur de screening configurable et gouvernance des decisions ;
3. contrats API BackOffice, Marketplace et referencement ;
4. garde-fous de publication multicanal ;
5. modele documentaire des justificatifs B2C, Pro et Animation ;
6. cycle financier et articulation avec Stripe Connect ;
7. migration de `DemandeFacturationAchatOrm`, `BillingProfile`, lignes unitaires, demandes groupees et notifications ;
8. contrats Pro, Animation et application Commercant ;
9. securite, audit, observabilite, reprise et recette.
10. mandat de depot, file BackOffice et suivi manuel Chorus Pro ; raccordement API reporte en V2.
11. aggregate commun des factures Localeo, snapshots fiscaux, avoirs et rendu PDF idempotent a la demande.
12. registre de credit d'achat B2B, generation a l'expiration et consommation dans les commandes Animation et Pro.

## Risques majeurs

- figer dans le code une interpretation fiscale encore non validee ;
- autoriser une premiere publication avant l'activation effective des controles ;
- diverger entre les controles de publication des differents canaux ;
- confondre paiement du bon, TVA de la prestation et commission Localeo ;
- creer deux demandes actives pour une meme consommation en concurrence ;
- exposer des donnees de facturation a un acteur non autorise ;
- presenter comme garanti un contenu seulement indicatif.

## Portes d'activation restantes

- arbitrages P0 renseignes dans le registre ;
- avis Juridica reference et version de politique attribuee ;
- migration auditable des coffrets existants et garde-fous BUM actifs avant la premiere commercialisation ;
- modele d'habilitation des qualificateurs defini ;
- predicat de publication et effets de requalification specifies ;
- wording et maquettes documentaires valides ;
- contrats d'API et contraintes d'idempotence documentes ;
- plan de tests et de deploiement progressif accepte.

Le bilan d'origine annonce la conception technique implémentée dans le [backend Localeo](../../../../localeo-backend/README.md), et non dans ce dépôt documentaire. Les validations
documentaires restantes sont externalisees et les fonctions concernees restent
desactivees jusqu'a leur approbation et leur recette.

## Documents complémentaires du dossier

- [Patch ANO-ANI-02 — proposition non appliquée](ano-ani-02-backend.patch)
- [ANO-ANI-02 — Facturation par animation](ano-ani-02-facturation-animation.md)
- [F16 — Révocation Chorus sans traitement du rejet asynchrone](chorus-mandat-fiabilite.md)

[Retour à l’index des spécifications](../INDEX.md)
