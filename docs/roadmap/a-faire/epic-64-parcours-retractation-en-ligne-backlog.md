# Epic 64 - Parcours de retractation en ligne depuis le site

- Date : 13 septembre 2026.
- Statut : **A developper - cadrage initial**.
- Priorite : **Critique**, obligation applicable aux contrats de consommation
  conclus en ligne depuis le 19 juin 2026 lorsqu'un droit de retractation est ouvert.
- Demande : permettre a l'acheteur de declarer sa retractation depuis le site,
  recevoir une preuve durable et suivre le traitement de sa demande.
- Dependances : Epic 7 (acces achat), Epic 8 (support), Epic 20 (remboursements),
  Epic 22 (timeline), Epic 38 (documents), Epic 39 (Stripe), Epic 51 (vision achat).
- Origine : [revue finale des documents juridiques V1](../../juridique/REVUE_FINALE_V1_2026-09-13.md),
  points 1.1 et 1.2 ; CGV Marketplace, article 8, et formulaire de retractation V1.

## Probleme et resultat attendu

Aujourd'hui, `/retractation` affiche une page juridique et un PDF. Les CGV
annoncent une fonctionnalite en ligne, mais aucun parcours public de declaration,
confirmation et accuse de reception n'a ete identifie dans le code examine.

Demain, l'acheteur accede a cette fonction sans creer de compte, identifie le
contrat concerne, confirme sa declaration et recoit une preuve conservable.
Localeo dispose d'un dossier suivi jusqu'a une decision motivee et, lorsque des
sommes sont dues, jusqu'au remboursement confirme.

Exemple : un acheteur ayant offert un coffret retrouve la fonction depuis le
site ou son email d'achat. Son lien de consultation a expire : il peut quand
meme deposer sa declaration. L'accuse en conserve la date initiale, meme si
le rapprochement de la commande ou le traitement financier intervient ensuite.

**La declaration de retractation, son instruction et le remboursement financier
sont trois operations distinctes.** Une panne Stripe, un transfert deja effectue
ou une regle technique historique ne doit pas empecher le depot de la declaration.
L'instruction constate les effets du droit et les sommes dues ; son exercice
ne depend pas d'une autorisation prealable de Localeo.

## Fondement et exigences applicables

Les sources officielles ont ete verifiees le 13 septembre 2026.

- [Article L. 221-21](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053310520/2026-06-19) :
  fonctionnalite gratuite permettant l'exercice du droit sur l'interface en ligne,
  applicable aux nouveaux contrats concernes depuis le 19 juin 2026. Le texte
  ne se limite pas aux services financiers. Les contrats deja en cours a cette
  date restent soumis aux dispositions anterieures ; leur droit eventuel subsiste.
- [Article D. 221-5](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053303365/2026-07-27) :
  acces visible et facile durant le delai, nom/prenom, informations identifiant
  le contrat et moyen electronique de reception de l'accuse ; confirmation
  explicite, puis accuse durable contenant la declaration et sa date/heure.
  Libelles proposes : **Renoncer au contrat ici**, puis **Confirmer la retractation**.
- [Article L. 221-19](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032226840/2017-09-20)
  et [article L. 221-20](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000044563199/2025-12-31) :
  appliquer les regles de computation et de prorogation, dont les jours non
  ouvrables et les consequences d'une information manquante. Ne pas coder un
  simple refus automatique apres quatorze fois vingt-quatre heures.
- [Article L. 221-24](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032226828/2020-09-08) :
  rembourser les sommes dues sans retard injustifie et dans le delai applicable,
  normalement au plus tard quatorze jours apres information de la decision du
  consommateur ; meme moyen de paiement sauf accord expres conforme. Le debut
  du suivi ne doit pas etre reporte a la date de decision d'un operateur.

Le formulaire PDF, le courriel et les autres declarations valables restent
utilisables. Aucun motif de changement d'avis, justificatif disproportionne,
appel telephonique ou consentement marketing n'est requis pour deposer.
Les conditions d'execution anticipee et les exceptions doivent etre examinees
selon le contrat, sans assimiler ouverture de lien, ajout dans Live ou QR a une
renonciation : [L. 221-25](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563179/2026-06-24)
et [L. 221-28](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563170/2026-05-04).

## Perimetre initial

Inclus : achats consommateurs de coffrets Marketplace, y compris cadeaux,
acces depuis le site mobile et les liens d'achat, declaration sans compte,
preuve, instruction interne, articulation avec les remboursements existants,
mise a jour des liens juridiques et recette complete.

Le beneficiaire d'un cadeau n'est pas automatiquement l'acheteur. Un acces
de consultation du coffret ne donne pas le droit de declencher son remboursement.
La declaration vise le contrat identifie ; le dossier permet son rapprochement
avec une ou plusieurs instances si la commande en comporte plusieurs.

Les abonnements et lots B2B Animation, la resiliation d'abonnement et la
refonte generale du checkout sont hors perimetre initial. Cette delimitation
produit n'ecarte aucun droit imperatif eventuellement applicable. Les demandes
hors parcours standard sont orientees et conservees pour examen.

La remise des CGV lors de l'achat, relevee dans la revue V1, reste une dependance
documentaire a traiter : les versions et dates d'information utiles au calcul
doivent etre accessibles. Leur absence historique ne peut empecher le depot.

## Parcours cible

1. **Acces** : entree permanente depuis le site et lien dans la confirmation
   d'achat ; ouverture directe sur mobile, sans connexion obligatoire. Conserver
   `/retractation` comme point d'entree et l'acces au formulaire telechargeable.
2. **Declaration** : identite du declarant, reference ou informations suffisantes
   pour retrouver le contrat, adresse electronique souhaitee pour l'accuse.
   Un commentaire reste facultatif. Ne pas imposer une reference introuvable
   comme seul moyen d'identifier un achat.
3. **Relecture et confirmation** : recapitulatif des informations saisies,
   possibilite de correction, action explicite distincte du simple affichage.
4. **Reception** : persistance de la declaration, reference et horodatage serveur
   du depot confirme, dates d'envoi et de reception clairement identifiees,
   preuve du contenu confirme et preparation transactionnelle de l'accuse.
   L'ecran confirme la reception, sans annoncer un remboursement deja execute.
5. **Accuse** : courriel conservable et copie recuperable ; un echec d'envoi
   ne supprime ni la declaration ni sa date. Reprise et alerte operationnelle.
6. **Rapprochement et instruction** : verification proportionnee de l'acheteur,
   du contrat, du delai et des sommes dues, avec traitement manuel des cas
   ambigus. Le depot n'attend pas une verification d'identite ulterieure.
7. **Traitement** : decision motivee, execution du remboursement du au moyen
   du moteur existant et mise a jour coordonnee des droits concernes.
8. **Information et suivi** : communiquer les suites au demandeur, conserver
   les preuves de paiement et rendre le dossier visible au support jusqu'a sa
   resolution, y compris en cas d'echec fournisseur.

## Regles metier et protections

1. La declaration est immuable apres confirmation. Les precisions, repetitions,
   rapprochements et decisions s'ajoutent a son historique. Conserver la date
   initiale pertinente en cas de retry ou de reprise par le support.
2. L'acces public ne revele pas si une commande tierce existe. Avant verification,
   l'accuse reprend les donnees declarees, sans enrichissement par des informations
   confidentielles de commande. Aucun token beneficiaire ne vaut mandat acheteur.
3. Pas d'annulation, de suspension de droits ou de remboursement sur la seule
   base d'un depot public non rapproche et non attribue a l'acheteur. La securite
   de l'action financiere est distincte de la possibilite de declarer a temps.
4. Le calcul du delai conserve l'evenement de depart, la version des conditions
   remise, les preuves d'information, la regle appliquee et l'echeance. Un cas
   indeterminable est soumis a examen, pas silencieusement rejete.
5. Le delai de validite du coffret, celui d'un lien et celui de retractation sont
   independants. Un statut utilise/expire ou un transfert commercant ne suffit
   pas a conclure que le droit est absent. Les exclusions financieres historiques
   ne doivent pas etre copiees dans le controle du depot.
6. Les montants sont determines cote serveur d'apres le paiement et les regles
   applicables ; aucune retenue automatique des frais Stripe ou de commission,
   aucun avoir impose. Les cas legalement dus que le moteur standard refuse
   doivent disposer d'une voie operationnelle explicite et auditable.
7. Un refus d'automatisation n'est pas un refus du droit. Un dossier manuel
   conserve responsable, echeance et preuve d'execution ; il ne suspend pas les
   obligations envers l'acheteur dans l'attente d'une reprise de transfert.
8. Definir le moment de protection des droits des que la demande est attribuee
   et la retractation applicable ; coordonner cette protection avec la consommation,
   l'activation, les QR et les verrous existants. Ne pas laisser un achat rembourse
   utilisable, ni effacer une prestation effectivement realisee de l'historique.
9. Requetes et traitements idempotents : double clic, retour navigateur, timeout,
   deux operateurs et webhooks repetes ne creent pas de double effet financier.
   Un resultat Stripe inconnu exige rapprochement avant toute nouvelle emission.
   Meme cle et meme contenu : meme resultat ; meme cle et contenu different :
   conflit explicite, sans modification de la declaration initiale.
10. Les decisions relevent d'operateurs habilites et sont auditees. Limiter les
    donnees conservees au dossier utile, definir les durees et purges avec le
    registre existant ; pas de declaration complete, email ou jeton dans les logs.

## Existant a reutiliser et points d'attention

| Element | Reutilisation ou adaptation a concevoir |
| --- | --- |
| `../../localeo-marketplace/src/App.jsx` et `src/pages/LegalPage.jsx` | La route documentaire existe ; ajouter le parcours fonctionnel et ses acces. |
| `app/infrastructure/persistence/models.py`, `RemboursementAchatOrm` | Remboursement unique par instance ; distinguer cette obligation financiere de la declaration pouvant concerner un contrat entier ou rester a rapprocher. |
| `app/application/support/use_cases/vision_360_client_backoffice.py` | Creation interne et suivi existants ; les controles d'usage actuels ne conviennent pas directement a la reception publique. |
| `app/application/gestion_achats/services/service_documents_achat.py` | Annulation, invalidation des droits, revocation des acces et notifications ; reutilisation apres decision appropriee. |
| `app/infrastructure/admin/admin.py` | Execution Stripe, intention persistante et rapprochement ; traiter explicitement la limite actuelle d'automatisation apres transfert. |
| `app/domaine/gestion_achats/services/intention_remboursement.py` | Reprise d'une tentative et verification de correlation ; conserver les garanties contre une emission en double. |
| `app/application/gestion_achats/services/finaliser_remboursement.py`, `verrouiller_instance.py`, `ventilation_remboursement.py` | Finalisation, concurrence avec consommation et calculs en centimes ; etendre selon le cas juridique sans creer un second moteur financier. |
| Outbox email, audit, documents, Vision 360 achat/client | Accuse, suivi des echecs, preuve durable et dossier de traitement. |

L'Epic 20 reste **terminee**. Son texte de MVP mentionne un traitement manuel,
alors que le code actuel comporte une execution Stripe et des reprises. Cette
nouvelle epic porte le parcours de retractation et les adaptations necessaires,
sans requalifier retroactivement la livraison historique.

## Backlog initial et criteres d'acceptation

Toutes les stories ci-dessous sont **A developper**.

| Story | Livrable | Criteres de recette |
| --- | --- | --- |
| E64-01 | Acces site et emails | Fonction retrouvable sans compte, depuis le site et l'achat ; ancienne route et PDF conserves ; clavier, lecteur d'ecran et mobile utilisables. |
| E64-02 | Declaration et confirmation | Champs minimaux, reference alternative, recapitulatif corrigeable ; aucun motif obligatoire ; afficher une confirmation uniquement apres persistance reussie. |
| E64-03 | Preuve et accuse durable | Contenu et horodatage conserves ; reference stable ; outbox dans la transaction de depot ; echec email repris sans perte de date ; aucune donnee d'un achat tiers exposee. |
| E64-04 | Rapprochement securise | Cadeau, lien expire et achat invite traites ; verification proportionnee avant toute action sur droits/paiement ; preuve accessible uniquement au demandeur autorise, jamais sur la seule reference du dossier ; absence de correspondance dirigee vers le support. |
| E64-05 | Delai et instruction juridique | Calcul teste aux bornes, jours non ouvrables, prolongation et information manquante ; consultation QR sans renonciation ; decision fondee et tracable pour cas utilises ou ambigus. |
| E64-06 | File interne et decisions | Responsable, anciennete, echeance, references achat/instances et remboursement ; decisions motivees ; alerte avant retard et suivi des dossiers manuels ; acces habilites. |
| E64-07 | Articulation remboursement et droits | Moteur existant reutilise ; annulation coordonnee ; cas deja transferes ou non standards suivis jusqu'a resolution ; montant et moyen conformes aux sommes dues. |
| E64-08 | Concurrence et reprise | Double soumission, deux operateurs, consommation concurrente et timeout PSP sans double effet ; cle reutilisee avec contenu different rejetee sans alteration ; rapprochement des resultats ambigus ; notification definitive sur preuve d'execution. |
| E64-09 | Information et documents | Adresse du parcours dans CGV/formulaire et emails ; HTML/PDF concordants ; version applicable et preuves accessibles ; autres canaux de declaration maintenus. |
| E64-10 | Livraison et exploitation | Recette complete en Stripe test, preuves et courriels verifies ; permissions, protection contre abus et absence de fuite ; surveillance file/outbox/delais ; procedure de panne et reprise. |

## Impacts techniques a concevoir

- **Domaine** : declaration, calcul du delai, instruction, invariants de droits
  et transitions ; regles pures testables sans base ni fournisseur.
- **Application et persistance** : depot/rapprochement/decision dans une unite
  de travail, archive du contenu et lien vers obligations financieres, audit
  et outbox atomiques ; schema et migration a definir a l'implementation.
- **API publique** : contrat de depot et recuperation de preuve sans compte,
  validation de taille/format, protection contre abus et non-divulgation.
  Une verification par email ne doit pas retarder la date du depot confirme.
- **Interface interne** : file et dossier dans le back-office/Localeo Support,
  liens Vision 360 ; les droits de decision et d'execution sont distincts.
- **Marketplace/Live** : formulaire, etats de reprise, accessibilite et liens
  directs ; le carnet local ne doit pas etre une condition d'acces.
- **Pro/Animation** : verifier les effets des changements de droits et statuts
  consultes ; aucun nouveau parcours de retractation B2B n'est deduit de cette epic.
- **Exploitation** : mesurer depots, accuses en echec, dossiers non rapproches,
  echeances proches/depassees et remboursements a rapprocher. Retenir une cible
  interne d'accuse immediat via outbox, puis alerte/reprise si l'envoi echoue.

## Arbitrages restant a instruire avant implementation

1. Mode de rapprochement/verifications acheteur, recovery sans reference et
   acces a la preuve, en respectant le depot sans compte ni retard de date.
2. Cartographie du point de depart et des cas d'execution anticipee selon les
   contrats/offres ; traitement des commandes multi-instances et des montants
   particuliers legalement dus, au-dela des restrictions du moteur standard.
3. Moment exact de protection des droits, habilitations de decision et traitement
   des cas apres transfert ; aucun blocage automatique sur simple saisie anonyme.
4. File principale SQLAdmin ou Localeo Support, objectifs internes de prise en
   charge, alertes, durees de conservation et articulation avec les demandes
   deja recues par courriel/courrier, en conservant leur date initiale.

Ces arbitrages concernent les modalites de realisation. Ils ne remettent pas
en question la necessite du parcours demandee par l'utilisateur.

## Definition de termine

- [ ] Stories E64-01 a E64-10 realisees et criteres verifies.
- [ ] Tests domaine : delais, information absente, qualification et transitions.
- [ ] Tests PostgreSQL : depot/outbox atomiques, liens de dossier, concurrence
  et idempotence de bout en bout.
- [ ] Recette visiteur mobile et clavier : achat pour soi/cadeau, lien expire,
  reference manquante, confirmation, preuve et information sur le traitement.
- [ ] Cas limites : limite de delai, doublon, usage concurrent, transfert deja
  effectue, panne email, timeout Stripe, remboursement anterieur, refus motive.
- [ ] Remboursement Stripe test et cas manuel rapproches sans double effet ;
  chronologie et droits effectivement coherents.
- [ ] Documents et liens verifies apres deploiement ; aucune simple presence
  du PDF ne vaut validation de la fonctionnalite.
- [ ] Procedure d'exploitation, surveillance et reprise disponibles ; acces
  acheteur maintenu en cas de rollback, sans perte des declarations deja recues.

Cette initialisation cree le backlog uniquement. Aucun parcours applicatif,
changement de donnees, commit, push ou deploiement n'est realise a ce stade.
