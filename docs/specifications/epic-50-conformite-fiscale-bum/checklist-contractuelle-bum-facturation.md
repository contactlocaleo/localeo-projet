# Epic 50 - Checklist contractuelle BUM, TVA et facturation

## 1. Objet

Cette checklist recense les clauses, informations precontractuelles, mandats,
preuves et documents a preparer pour l'Epic 50. Elle sert de support de travail
avec Juridica, Finance, l'expert-comptable et le DPO. Elle ne constitue pas un
avis juridique ou fiscal.

Chaque point doit recevoir un statut :

- `[A REDIGER]` : aucun texte valide n'existe ;
- `[A VALIDER]` : proposition disponible, validation externe requise ;
- `[VALIDE]` : texte, version, validateur et date references ;
- `[INTEGRE]` : texte valide publie dans tous les parcours et documents cibles.

### Etat de preparation documentaire au 30/08/2026

Les propositions consolidees ont ete ajoutees aux documents Word references par
`docs/juridique/INDEX_DOCUMENTS_JURIDIQUES.md`. Elles restent au
statut **`[A VALIDER]`** : leur presence dans un projet contractuel ne vaut ni
validation juridique ou fiscale, ni publication.

- `E50-CTR-001` a `E50-CTR-021` : couverture partielle dans les CGV Marketplace,
  la convention commercant, le formulaire de retractation et les mentions
  legales ;
- `E50-CTR-022` a `E50-CTR-028` : couverture partielle dans les conditions
  Localeo Animation ; le parcours Marketplace Pro est implemente cote backend
  mais son wording contractuel reste a valider ;
- `E50-CTR-029` a `E50-CTR-052` : couverture partielle dans la convention
  commercant et la politique de confidentialite ; l'assistant reste limite a
  la preparation de brouillons sous le controle du commercant ;
- `E50-CTR-053` a `E50-CTR-058` : mandat et depot manuel implementes derriere
  indicateur ; textes et preuve d'acceptation restent a valider avant activation ;
- `E50-CTR-059` a `E50-CTR-066` : non actives, dans l'attente des arbitrages
  B2B cites en section 9 ;
- `E50-CTR-067` a `E50-CTR-080` : couverture partielle ; les modeles fiscaux et
  les annexes internes V3 restent a produire et a valider ;
- `E50-CTR-081` a `E50-CTR-087` : gouvernance restant a executer lors de la
  validation et de la publication finales.

La synthese, les documents manquants et les annexes a regenerer sont recenses
dans `docs/juridique/SYNTHESE_MISE_A_JOUR_EPIC_50.md`.

## 2. Matrice des documents a maintenir

| Document | Public | Objet principal |
| --- | --- | --- |
| CGV Marketplace B2C | Acheteur particulier | Achat, emission et utilisation du coffret |
| Parcours Marketplace Pro a consolider | Organisation acheteuse | Achat B2B, facturation et credit d'achat |
| Conditions Localeo Animation | Partenaire public ou prive | Abonnement, lots, facturation et credit Animation |
| Convention partenaire commercant | Commercant | Referencement, BUM, execution, commission, reversement et factures |
| Assistant de facturation integre au produit | Commercant | Preparation facultative d'un brouillon sous le controle du commercant |
| Politique de confidentialite | Tous les acteurs | Traitements, destinataires, droits et conservation |
| Annexe RGPD Animation conditionnelle | Localeo et partenaire Animation | Clauses de l'article 28 du RGPD uniquement lorsque les roles l'exigent |
| Justificatif d'acquisition | Acheteur | Preuve d'acquisition du BUM sans TVA sous-jacente facturee |
| Modele de facture commercant | Acheteur apres execution | Facture de la prestation emise sous la responsabilite du commercant |
| Factures Localeo | Commercant / partenaire | Commission et abonnement emis par Localeo |

Si `CGP` designe dans l'organisation un document different des conditions du
partenaire ou du commercant, chaque exigence ci-dessous doit etre remappee vers
le document juridiquement opposable approprie.

## 3. Qualification BUM et role des parties

| ID | Point a integrer ou valider | Document cible | Validation |
| --- | --- | --- | --- |
| `E50-CTR-001` | Decrire le coffret comme un bon a usages multiples uniquement lorsque les prestations possibles ne permettent pas de connaitre, a l'emission, le lieu et la TVA dus | CGV, contrat commercant, fiche coffret | Juridica / Fiscaliste |
| `E50-CTR-002` | Ne jamais presenter le libelle commercial `SOLO / MULTI` comme une qualification fiscale | CGV, catalogue, CGP | Juridica / Produit |
| `E50-CTR-003` | Identifier Localeo comme emetteur ou distributeur du coffret et identifier le commercant comme fournisseur de la prestation sous-jacente | CGV, contrat commercant | Juridica |
| `E50-CTR-004` | Expliquer que le transfert du BUM precedant son utilisation ne porte pas la TVA de la prestation sous-jacente | CGV, justificatif | Juridica / Comptable |
| `E50-CTR-005` | Faire valider, pour chaque offre, la qualification du bon, le fait generateur et l'exigibilite de la TVA ; ne pas poser une regle generale rattachee a la seule execution | CGV, contrat commercant, aide facturation | Juridica / Comptable |
| `E50-CTR-006` | Distinguer contractuellement prix du coffret, valeur des prestations, commission Localeo et eventuels frais propres a Localeo | Tous contrats et documents financiers | Finance / Juridica |
| `E50-CTR-007` | Prevoir la requalification, la depublication et le traitement des droits deja acquis lorsqu'une offre cesse de respecter la politique BUM | CGV, contrat commercant | Juridica / Produit |
| `E50-CTR-008` | Integrer dans la convention signee les engagements BUM du commercant et l'obligation de signaler toute modification substantielle ; OnBoard ne porte pas d'attestation autonome | Convention partenaire commercant | Juridica |

Point d'attention : un contrat ne transforme pas a lui seul une offre en BUM.
La qualification depend des caracteristiques effectives du bon et des
prestations accessibles.

## 4. CGV Marketplace B2C

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-009` | Decrire les caracteristiques essentielles : promesse garantie, exemples indicatifs, territoire, commercants et prestations eligibles | Juridica / Produit |
| `E50-CTR-010` | Indiquer prix total, devise, frais, moyens de paiement et moment de conclusion de la commande | Juridica / Finance |
| `E50-CTR-011` | Decrire emission, activation, livraison numerique, ajout a Localeo Live et preuve de remise | Juridica / Produit |
| `E50-CTR-012` | Fixer date de debut, duree de validite, fuseau et instant exact d'expiration | Juridica / Produit |
| `E50-CTR-013` | Definir cessibilite, cadeau, beneficiaire, perte, vol, compromission, opposition et regeneration des acces | Juridica / Securite |
| `E50-CTR-014` | Expliquer les conditions d'utilisation totale ou partielle et le traitement du solde, si un usage partiel est possible | Juridica / Finance |
| `E50-CTR-015` | Decrire reservation, annulation, indisponibilite, fermeture du commercant, substitution et impossibilite d'execution | Juridica / Support |
| `E50-CTR-016` | Definir remboursement, annulation du coffret, annulation d'une prestation et consequences sur les droits et reversements | Juridica / Finance |
| `E50-CTR-017` | Faire valider l'application du droit de retractation, son point de depart, son formulaire et chaque exception eventuelle | Juridica |
| `E50-CTR-018` | Afficher un bouton de commande indiquant sans ambiguite l'obligation de paiement et fournir les CGV sur support durable | Juridica / Produit |
| `E50-CTR-019` | Identifier le service reclamation et le mediateur de la consommation avec ses coordonnees et son site | Juridica / Support |
| `E50-CTR-020` | Definir responsabilites respectives de Localeo et du commercant sans clause supprimant les droits legaux du consommateur | Juridica |
| `E50-CTR-021` | Preciser la valeur probante des emails, journaux, QR, validations et versions contractuelles, sans renversement abusif de la charge de la preuve | Juridica / Securite |

Les ventes a distance aux consommateurs exigent notamment une information
precontractuelle sur le prix, les caracteristiques, l'execution et la
retractation. Le consommateur dispose en principe de quatorze jours, sous
reserve des exceptions legales a qualifier pour chaque offre. Les coordonnees
du mediateur doivent figurer sur le site, dans les CGV et sur les bons de
commande.

## 5. CGV Pro et conditions Animation

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-022` | Identifier l'organisation acheteuse, son etablissement, son SIRET, le signataire habilite et le proprietaire des droits | Juridica / Finance |
| `E50-CTR-023` | Definir prix, remises, echeances, moyens de paiement, penalites de retard et indemnite forfaitaire de recouvrement applicables | Juridica / Finance |
| `E50-CTR-024` | Expliquer le justificatif BUM remis a l'achat et sa distinction avec une facture de prestation ou une facture Localeo | Juridica / Comptable |
| `E50-CTR-025` | Decrire allocation des coffrets, beneficiaires, remise des acces, expiration et traitement des lots non distribues | Juridica / Produit |
| `E50-CTR-026` | Definir les habilitations du partenaire Animation, le perimetre partenaire + commune et la responsabilite sur les donnees des beneficiaires | Juridica / DPO |
| `E50-CTR-027` | Identifier les operations relevant de l'e-invoicing B2B, de l'e-reporting ou de Chorus Pro et les obligations de chaque partie | Juridica / Comptable |
| `E50-CTR-028` | Autoriser la transmission des donnees necessaires a une plateforme agreee et imposer la mise a jour des adresses de facturation | Juridica / DPO |

## 6. Contrat ou CGP commercant

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-029` | Decrire le processus de referencement, screening, qualification BUM et publication | Juridica / Produit |
| `E50-CTR-030` | Imposer l'exactitude et la mise a jour des identites legale, fiscale, bancaire, reglementaire et commerciale | Juridica / Finance |
| `E50-CTR-031` | Definir la prestation garantie, sa valeur brute TTC, ses conditions d'execution et les restrictions opposables au beneficiaire | Juridica / Produit |
| `E50-CTR-032` | Faire accepter le processus de validation de consommation et les modes de secours | Juridica / Operations |
| `E50-CTR-033` | Preciser que seule une prestation validee ouvre le droit au reversement et a une demande de facture | Juridica / Finance |
| `E50-CTR-034` | Definir commission Localeo TTC, taux ou montant configurable, TVA de la commission, facture separee et net reverse | Juridica / Comptable |
| `E50-CTR-035` | Definir calendrier, seuil, moyen, suspension, correction et rapprochement des reversements Stripe Connect | Finance / Juridica |
| `E50-CTR-036` | Rendre le commercant responsable du regime, du taux, des mentions et de la TVA de sa prestation executee | Juridica / Comptable |
| `E50-CTR-037` | Decrire reception, delai de traitement, contenu, upload ou emission assistee des demandes de facture | Juridica / Operations |
| `E50-CTR-038` | Definir conservation, accessibilite, correction et opposabilite des factures et avoirs | Juridica / Comptable |
| `E50-CTR-039` | Encadrer les controles, demandes de preuves, audits, suspension et depublication en cas d'information incomplete ou obsolete | Juridica |
| `E50-CTR-040` | Regler fermeture, resiliation, prestations deja vendues, substitutions, remboursements, reversements et factures encore dus | Juridica / Finance |
| `E50-CTR-041` | Encadrer droits sur textes, marques, photos et autorisation de publication des contenus | Juridica |
| `E50-CTR-042` | Informer sur Stripe Connect, controles KYC, destinataires des donnees et consequences d'un compte non operationnel | Juridica / DPO / Finance |

## 7. Assistant de facturation commercant

Ces points sont couverts par la convention unique et par le parcours produit.
Ils ne forment pas une annexe contractuelle separee dans le perimetre actuel.

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-043` | Presenter Localeo comme outil de preparation et non comme vendeur ou prestataire sous-jacent | Juridica |
| `E50-CTR-044` | Confirmer si le fonctionnement reste celui d'un logiciel sous le controle du commercant ou exige un mandat de facturation par un tiers | Juridica / Fiscaliste |
| `E50-CTR-045` | Exiger une confirmation explicite du commercant avant chaque emission et conserver sa preuve | Juridica / Securite |
| `E50-CTR-046` | Faire verifier identite, client, dates, lignes, TVA, exonerations, paiement par coffret et mentions propres a l'activite | Commercant / Comptable |
| `E50-CTR-047` | Definir la serie de numerotation propre au commercant, son prefixe, son point de depart, sa continuite et la procedure de correction | Juridica / Comptable |
| `E50-CTR-048` | Preciser qu'un brouillon n'est pas une facture, ne porte aucun numero definitif et n'est jamais transmis au client | Juridica |
| `E50-CTR-049` | Rendre la facture emise immuable et imposer un avoir ou document correctif reference | Juridica / Comptable |
| `E50-CTR-050` | Prevoir export, recuperation des archives, indisponibilite du service et continuite de la numerotation lors d'une sortie de Localeo | Juridica / Technique |
| `E50-CTR-051` | Maintenir le choix d'uploader une facture emise dans un autre outil | Produit / Juridica |
| `E50-CTR-052` | Informer du futur recours a une plateforme agreee, des formats structures, statuts et donnees transmises | Juridica / DPO |

L'obligation d'emettre la facture reste celle de l'assujetti. Dans le perimetre
actuel, Localeo prepare uniquement un brouillon sans numero definitif ; le
commercant controle puis emet la facture sous sa responsabilite. Toute evolution
vers une emission par un tiers exigerait un nouvel arbitrage et un mandat adapte.

## 8. Depot Chorus Pro hors perimetre actuel

Les exigences ci-dessous sont conservees pour la tracabilite historique mais
sont **desactivees**. Localeo ne depose pas de facture au nom du commercant et
aucun mandat Chorus Pro n'est propose a la signature. Toute reactivation exige
un nouvel arbitrage formel, une validation Juridica/comptable et une mise a jour
du corpus contractuel.

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-053` | Identifier mandant, mandataire, SIRET emetteur, perimetre des factures et destinataires publics | Juridica |
| `E50-CTR-054` | Autoriser explicitement Localeo a deposer la facture sans devenir son emetteur fiscal | Juridica / Comptable |
| `E50-CTR-055` | Fixer prise d'effet, duree, preuve d'acceptation, revocation et sort des depots en cours | Juridica |
| `E50-CTR-056` | Repartir les responsabilites sur contenu fiscal, references Chorus, depot, suivi, rejet et correction | Juridica / Operations |
| `E50-CTR-057` | Collecter SIRET destinataire et, seulement lorsqu'ils sont exiges, code service et engagement juridique | Finance / Operations |
| `E50-CTR-058` | Informer des donnees transmises a Chorus Pro et de leur conservation | DPO / Juridica |

## 9. Credit d'achat B2B

Ne pas publier ces clauses avant validation de `BUM-ARB-27`, `BUM-ARB-29`,
`BUM-ARB-30`, `BUM-ARB-32` et `BUM-ARB-40`.

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-059` | Qualifier juridiquement et comptablement le credit issu d'un BUM expire | Juridica / Finance |
| `E50-CTR-060` | Definir beneficiaire : organisation Pro ou partenaire + commune Animation | Juridica / Produit |
| `E50-CTR-061` | Expliquer la formule d'allocation sur le montant effectivement paye, les exclusions et les arrondis | Finance / Juridica |
| `E50-CTR-062` | Fixer fait generateur, duree de 12 mois proposee, fuseau, instant d'expiration et notifications | Juridica / Finance |
| `E50-CTR-063` | Indiquer non-remboursabilite, non-transferabilite et usages B2B eligibles | Juridica |
| `E50-CTR-064` | Decrire paiement mixte, reservation temporaire, liberation et priorite d'utilisation | Finance / Produit |
| `E50-CTR-065` | Definir effets d'un remboursement, litige, annulation ou erreur apres attribution ou consommation | Juridica / Finance |
| `E50-CTR-066` | Faire accepter les conditions a l'achat puis a la premiere utilisation et conserver leur version | Juridica / Securite |

## 10. Documents fiscaux et mentions

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-067` | Valider le titre et le wording du `Justificatif d'acquisition d'un bon a usages multiples` | Juridica / Comptable |
| `E50-CTR-068` | Interdire toute TVA sous-jacente facturee sur le justificatif BUM et separer les frais propres a Localeo | Comptable / Juridica |
| `E50-CTR-069` | Verifier toutes les mentions obligatoires de la facture de prestation selon le profil du commercant et du client | Comptable |
| `E50-CTR-070` | Valider la presentation du brut TTC, du reglement par coffret et du net a payer nul | Juridica / Comptable |
| `E50-CTR-071` | Valider les mentions, series et TVA des factures de commission et d'abonnement emises par Localeo | Comptable |
| `E50-CTR-072` | Definir la mention et le lien vers la facture d'origine sur chaque avoir ou correctif | Comptable |
| `E50-CTR-073` | Definir durees de conservation, format lisible, integrite, export et acces aux factures | Juridica / Comptable / DPO |

## 11. Donnees personnelles et preuves

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-074` | Cartographier Localeo, commercant, Stripe, stockage, email, signature, Chorus et plateforme agreee comme responsables ou sous-traitants | DPO / Juridica |
| `E50-CTR-075` | Documenter finalites et bases legales : contrat, obligation legale, preuve, securite et interet legitime le cas echeant | DPO |
| `E50-CTR-076` | Appliquer la minimisation et ne pas collecter une piece d'identite si une verification Stripe ou registre suffit | DPO / Securite |
| `E50-CTR-077` | Fixer une duree par categorie : onboarding, contrats, audit, factures, prospects, comptes et documents expires | DPO / Juridica |
| `E50-CTR-078` | Informer sur destinataires, transferts hors UE, mesures de securite, droits et contact DPO | DPO |
| `E50-CTR-079` | Encadrer signature ou acceptation electronique : version, horodatage, identite, support durable et empreinte | Juridica / Securite |
| `E50-CTR-080` | Definir acces, rectification, purge, gel contentieux, export et journalisation des documents sensibles | DPO / Juridica |

Les donnees ne peuvent pas etre conservees indefiniment. Une duree doit etre
definie selon la finalite, tout en tenant compte des obligations legales ; la
CNIL rappelle notamment une conservation de dix ans des donnees de facturation
au titre du Code de commerce.

## 12. Gouvernance de validation et publication

| ID | Point a integrer ou valider | Validation |
| --- | --- | --- |
| `E50-CTR-081` | Designer un proprietaire et un validateur pour chaque document | Direction / Juridica |
| `E50-CTR-082` | Affecter code version, statut, date d'effet, approbateur, date d'approbation et empreinte | Juridica / Technique |
| `E50-CTR-083` | Conserver la version acceptee avec chaque achat, convention partenaire, mandat et emission assistee | Juridica / Technique |
| `E50-CTR-084` | Definir les modifications exigeant une nouvelle acceptation explicite | Juridica / Produit |
| `E50-CTR-085` | Verifier la coherence entre CGV, CGP, fiches produit, checkout, emails, PDF, aide et BackOffice | Juridica / QA |
| `E50-CTR-086` | Interdire l'activation d'une fonction si son arbitrage juridique est absent ou si la version valide n'est pas configuree | Direction / Technique |
| `E50-CTR-087` | Organiser une revue annuelle et une revue lors de toute evolution fiscale, commerciale ou de plateforme | Juridica / Finance |

## 13. Priorites de validation avant mise en production

### P0 - Bloque l'activation de la fonction concernee

- qualification et wording BUM : `E50-CTR-001` a `E50-CTR-008` ;
- retractation, expiration, remboursement et responsabilites B2C :
  `E50-CTR-012` a `E50-CTR-020` ;
- responsabilites fiscales et financieres du commercant : `E50-CTR-033` a
  `E50-CTR-040` ;
- assistant de facturation : `E50-CTR-043` a `E50-CTR-052` ;
- mandat Chorus : `E50-CTR-053` a `E50-CTR-058` ;
- credit B2B : `E50-CTR-059` a `E50-CTR-066` ;
- documents fiscaux : `E50-CTR-067` a `E50-CTR-073`.

### P1 - Requis avant generalisation

- clauses operationnelles, support, continuite et sortie ;
- matrice RGPD, conservation et sous-traitants ;
- preuve d'acceptation, nouvelle acceptation et revue periodique ;
- coherence de toutes les surfaces et supports durables.

## 14. Sources officielles de travail

- [BOFiP - operations realisees au moyen de bons](https://bofip.impots.gouv.fr/bofip/11738-PGP.html/identifiant%3DBOI-TVA-CHAMP-10-10-40-50-20240214) ;
- [Ministere de l'Economie - mentions obligatoires d'une facture](https://www.economie.gouv.fr/entreprises/gerer-son-entreprise-au-quotidien/gerer-sa-comptabilite-et-ses-demarches/mentions-obligatoires-dune-facture-tout-savoir) ;
- [Ministere de l'Economie - CGV entre professionnels](https://www.economie.gouv.fr/entreprises/gerer-sa-comptabilite-et-ses-demarches/conditions-generales-de-vente-entre) ;
- [DGCCRF - regles du commerce electronique B2C](https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/e-commerce-les-regles-entre-professionnels-et-consommateurs) ;
- [Mediation de la consommation - obligations du professionnel](https://www.economie.gouv.fr/mediation-conso/vous-etes-un-professionnel/vos-principales-obligations-0) ;
- [DGFiP - facturation electronique et plateformes agreees](https://www.impots.gouv.fr/facturation-electronique-et-plateformes-agreees) ;
- [CNIL - durees de conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees).

Ces sources servent a preparer les travaux. La version applicable a la date de
mise en production doit etre reverifiee et la validation externe referencee
dans le registre d'arbitrage.
