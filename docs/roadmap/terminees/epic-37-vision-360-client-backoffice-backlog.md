# Epic 37 - Vision 360 client backoffice

## Synthese

- Criticite : `Elevee`
- Statut : `Termine`
- Objectif : fournir au back-office une vision 360 d'un client afin de traiter rapidement les demandes clients depuis un point d'entree unique, avec recherche par nom, prenom ou telephone.
- Decision produit : la vue cible est une surface support/exploitation interne, orientee traitement de demandes clients.
- Decision technique : la vue agrege les donnees existantes sans creer une nouvelle source de verite analytique.
- Decision operationnelle : un operateur doit pouvoir retrouver un client, comprendre son historique, renvoyer un QR code, gerer un remboursement et consulter la valeur generee par ce client.
- Decision securite : les donnees client sont sensibles ; les acces, recherches et actions doivent etre limites aux profils autorises et audites.
- Decision produit : la cle de consolidation client MVP est l'email.
- Decision technique : le MVP cree une vraie table `clients`.
- Decision produit : le renvoi QR utilise un type email dedie `RENVOI_QR_CLIENT`.
- Decision produit : la repartition CA par commercant s'appuie sur deux lectures : prestations achetees et prestations validees.
- Decision produit : les seuils de niveau client sont fixes en dur en MVP.
- Decision securite : seules les personnes avec role `ADMIN` peuvent voir les coordonnees completes et initier un remboursement depuis la vision 360 client.
- Decision reprise historique : les achats sans email valide restent en `client non consolide` tant qu'un email valide n'est pas disponible.
- Decision doublons : les doublons apparents avec emails differents sont hors MVP ; le MVP peut afficher une suspicion de doublon sans fusion automatique.
- Decision droits : aucune delegation a `SUPPORT` ou `FINANCE` n'est prevue en MVP pour les coordonnees completes et les remboursements.

## Probleme

Les informations utiles pour aider un client sont dispersees entre achats, coffrets instances, validations, emails/SMS, remboursements, messages support et documents. Lorsqu'un client contacte Localeo pour une perte de QR code, une question sur un coffret, une prestation non disponible ou un remboursement, l'operateur doit reconstruire manuellement son parcours.

## Risque business

- Traitement support lent lors des demandes clients.
- Risque de renvoyer le mauvais QR code ou de ne pas identifier le bon coffret en cours.
- Mauvaise visibilite sur la valeur et la fidelite d'un client.
- Difficultes a piloter les remboursements ou gestes commerciaux.
- Experience client degradee en cas de perte de mail, perte de QR code ou incident commercant.

## Risque technique

- Les clients sont consolides par email en MVP, avec telephone normalise en critere de recherche secondaire.
- Les achats historiques sans email valide ne sont pas rattaches automatiquement a un client consolide.
- Une recherche telephone doit normaliser les formats nationaux et internationaux.
- Les donnees personnelles doivent etre masquees ou limitees selon le role back-office.
- Les actions depuis la vue 360 doivent reutiliser les use cases existants et le pattern Unit of Work.
- Les indicateurs financiers doivent distinguer CA client, revenu Localeo, reversements commercants et remboursements.

## Perimetre MVP

- Ajouter une entree back-office `Vision 360 client`.
- Rechercher un client par nom, prenom, email si disponible et numero de telephone.
- Creer et maintenir une table `clients` consolidee par email.
- Identifier les achats sans email valide comme non consolidables en MVP.
- Normaliser la recherche telephone.
- Afficher une fiche synthese client :
  - nom ;
  - prenom ;
  - email ;
  - telephone ;
  - date du premier achat ;
  - date du dernier achat ;
  - nombre de coffrets achetes ;
  - statut relationnel ou niveau client.
- Afficher l'historique de ses coffrets.
- Afficher les coffrets en cours.
- Afficher les dernieres prestations realisees.
- Permettre de renvoyer un email contenant le QR code sur un coffret en cours eligible.
- Afficher une notation/niveau client base sur le nombre de coffrets achetes.
- Afficher le CA genere par le client :
  - global ;
  - revenu Localeo ;
  - repartition par commercant si disponible ;
  - remboursements et reste net si disponible.
- Permettre de gerer un remboursement sur un coffret depuis la vue 360.
- Afficher les communications envoyees au client : emails, SMS et notifications utiles.
- Afficher les demandes support rattachees au client.
- Afficher les documents disponibles : recu, factures, pack documents si applicable.
- Ajouter des liens directs vers achats, coffrets instances, validations, remboursements et timeline support.
- Auditer les actions sensibles : recherche detaillee, renvoi QR, creation de remboursement, consultation de donnees sensibles.

## Hors perimetre MVP

- Espace client authentifie.
- Fusion automatique de fiches clients.
- Scoring marketing avance.
- Segmentation commerciale ou campagne marketing.
- Export complet de donnees personnelles.
- Modification directe des donnees client depuis la vue 360.
- Remboursement automatique sans validation back-office.

## User Stories

1. `PRD-274` En tant qu'operateur back-office, je veux rechercher un client par nom, prenom ou telephone afin d'ouvrir rapidement sa vision 360.
   - Statut : `Termine`
   - Resultat attendu : la recherche accepte nom, prenom, email si disponible et telephone.
   - Resultat attendu : le telephone est normalise pour retrouver un client meme si le format saisi differe.
   - Resultat attendu : les resultats affichent nom, prenom, email masque, telephone masque et dernier achat.

2. `PRD-275` En tant qu'operateur support, je veux consulter une fiche synthese client afin d'identifier rapidement la personne qui contacte Localeo.
   - Statut : `Termine`
   - Resultat attendu : la fiche affiche identite, coordonnees, premier achat, dernier achat, nombre de coffrets et statut relationnel.
   - Resultat attendu : les donnees sensibles sont masquees selon les droits back-office.

3. `PRD-276` En tant qu'operateur support, je veux voir l'historique des coffrets du client afin de comprendre son parcours d'achat.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les coffrets achetes avec date, statut, ville, montant, destinataire et liens back-office.
   - Resultat attendu : les coffrets rembourses, expires, termines et en cours sont distingues.

4. `PRD-277` En tant qu'operateur support, je veux voir les coffrets en cours afin de traiter rapidement une demande active.
   - Statut : `Termine`
   - Resultat attendu : la vue isole les coffrets encore utilisables ou en attente d'activation.
   - Resultat attendu : chaque coffret en cours affiche expiration, prestations restantes, QR/code disponible et alertes.

5. `PRD-278` En tant qu'operateur support, je veux voir les dernieres prestations realisees afin de comprendre ce que le client a deja consomme.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche les dernieres validations avec date, coffret, prestation, commercant et statut.
   - Resultat attendu : les validations annulees ou en anomalie sont signalees.

6. `PRD-279` En tant qu'operateur support, je veux renvoyer un email avec le QR code d'un coffret en cours afin d'aider un client qui a perdu son mail.
   - Statut : `Termine`
   - Resultat attendu : l'action est disponible uniquement sur les coffrets en cours eligibles.
   - Resultat attendu : l'email QR reutilise le service de preparation email existant.
   - Resultat attendu : l'action est auditee et cree un email sortant dans l'outbox.

7. `PRD-280` En tant qu'operateur support, je veux voir un niveau client base sur le nombre de coffrets achetes afin d'adapter le traitement relationnel.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche un niveau simple, base sur les seuils MVP fixes et documentes.
   - Resultat attendu : le niveau reste informatif et ne declenche aucune decision automatique en MVP.

8. `PRD-281` En tant que responsable exploitation, je veux voir le CA genere par le client afin d'evaluer son importance economique.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche le CA global encaisse sur les achats confirmes.
   - Resultat attendu : la vue affiche la part Localeo disponible selon la source financiere existante.
   - Resultat attendu : la vue affiche les remboursements et le net client si disponible.

9. `PRD-282` En tant que responsable exploitation, je veux voir la repartition du CA client par commercant afin de comprendre quels partenaires ont beneficie de son activite.
   - Statut : `Termine`
   - Resultat attendu : la vue agrege les montants par commercant selon les coffrets/prestations achetes ou valides.
   - Resultat attendu : les montants sont clairement qualifies pour eviter la confusion entre prix client et reversement commercant.

10. `PRD-283` En tant qu'operateur support, je veux gerer un remboursement depuis un coffret de la fiche client afin de traiter une demande sans changer de contexte.
    - Statut : `Termine`
    - Resultat attendu : la vue expose l'etat de remboursement du coffret.
    - Resultat attendu : l'action reutilise le workflow de remboursement existant.
    - Resultat attendu : les remboursements impossibles affichent un motif explicite.

11. `PRD-284` En tant qu'operateur support, je veux voir les communications envoyees au client afin de savoir ce qu'il a deja recu.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les derniers emails et SMS rattaches au client, dont QR renvoye, remboursement et communications libres.
    - Resultat attendu : les statuts d'envoi et erreurs recentes sont visibles.

12. `PRD-285` En tant qu'operateur support, je veux voir les demandes support rattachees au client afin de comprendre l'historique des echanges.
    - Statut : `Termine`
    - Resultat attendu : la vue liste les messages support et contacts rattaches aux coordonnees du client.
    - Resultat attendu : un lien permet d'ouvrir la timeline support associee.

13. `PRD-286` En tant qu'operateur support, je veux acceder aux documents du client afin de repondre aux demandes de justificatifs.
    - Statut : `Termine`
    - Resultat attendu : la vue propose les liens vers recus, factures ou packs documents disponibles.
    - Resultat attendu : l'acces aux documents est limite aux profils autorises.

14. `PRD-287` En tant que responsable securite, je veux que la vision 360 client encadre les donnees personnelles afin de limiter les risques de fuite.
    - Statut : `Termine`
    - Resultat attendu : les recherches et consultations detaillees sont auditees.
    - Resultat attendu : les roles non autorises ne peuvent pas consulter les donnees personnelles completes.

15. `PRD-288` En tant qu'operateur back-office, je veux naviguer depuis la vision 360 client vers tous les objets rattaches afin d'agir rapidement.
    - Statut : `Termine`
    - Resultat attendu : les achats, coffrets instances, validations, remboursements, emails/SMS, documents et messages support disposent de liens directs.

## Regles de gestion

- La recherche client doit accepter plusieurs criteres sans exposer une liste trop large de donnees personnelles.
- Les numeros de telephone doivent etre normalises avant recherche.
- Un email QR ne peut etre renvoye que pour un coffret en cours, non expire, non rembourse et encore eligible.
- Le renvoi QR doit passer par l'outbox email existante.
- Un remboursement depuis la vision 360 doit reutiliser les use cases existants de remboursement.
- Les indicateurs financiers doivent distinguer :
  - CA client encaisse ;
  - revenu ou marge Localeo quand disponible ;
  - reversements commercants ;
  - remboursements ;
  - net apres remboursement.
- La notation client MVP est informative, basee sur le nombre de coffrets achetes.
- La notation client MVP suit le bareme suivant :
  - `Nouveau` : 1 coffret achete ;
  - `Regulier` : 2 a 3 coffrets achetes ;
  - `Fidele` : 4 a 7 coffrets achetes ;
  - `Ambassadeur` : 8 coffrets achetes ou plus.
- La repartition CA par commercant doit distinguer les prestations achetees et les prestations validees.
- Les coordonnees completes et l'action de remboursement sont reservees au role `ADMIN`.
- Les achats sans email valide restent visibles depuis les achats/coffrets, mais ne creent pas de fiche client consolidee.
- Les doublons apparents avec emails differents peuvent etre signales, sans action de fusion en MVP.
- Toute action sensible doit respecter le pattern Unit of Work.
- Les donnees personnelles doivent etre masquees ou limitees selon les roles back-office.

## Modele cible

### Client

Table cible : `clients`

Champs cibles :

- `id`
- `email`
- `nom`
- `prenom`
- `telephone`
- `telephone_normalise`
- `premier_achat_at`
- `dernier_achat_at`
- `nombre_coffrets`
- `niveau_client`
- `created_at`
- `updated_at`

Regle MVP : `email` est la cle de consolidation et doit etre unique quand il est renseigne. Le telephone normalise sert a la recherche, pas a fusionner automatiquement deux clients.

Les achats historiques sans email valide restent en `client non consolide` tant qu'aucun email valide n'est disponible. Deux emails differents ne sont jamais fusionnes automatiquement en MVP, meme si le nom, le prenom ou le telephone semblent similaires.

### Indicateurs financiers client

- `ca_total_encaisse`
- `revenu_localeo`
- `montant_reverse_commercants`
- `montant_rembourse`
- `net_client`
- `repartition_par_commercant_prestations_achetees`
- `repartition_par_commercant_prestations_validees`

### Actions support

- `RENVOI_QR_CLIENT`
- `CREATION_REMBOURSEMENT_CLIENT`
- `CONSULTATION_VISION_360_CLIENT`

## APIs et integration cible

- Back-office :
  - rechercher un client ;
  - ouvrir une fiche 360 client ;
  - renvoyer le QR d'un coffret en cours ;
  - initier ou consulter un remboursement ;
  - naviguer vers les objets rattaches.
- Emails :
  - utiliser le type dedie `RENVOI_QR_CLIENT` pour historiser clairement le renvoi d'un QR a la demande du client.
- Support :
  - integrer les messages contact et timeline support.
- Finance :
  - reutiliser le workflow remboursement existant.

## Lots d'implementation

### Lot 1 - Recherche et consolidation client

- Appliquer la consolidation par email.
- Creer la table `clients`.
- Normaliser les telephones.
- Marquer les achats sans email valide comme non consolides.
- Implementer la recherche nom/prenom/email/telephone.

### Lot 2 - Fiche synthese et coffrets

- Afficher identite, niveau client et indicateurs de synthese.
- Lister historique de coffrets et coffrets en cours.
- Ajouter liens vers achats et coffrets instances.

### Lot 3 - Prestations et support

- Afficher dernieres prestations realisees.
- Afficher demandes support et communications recentes.
- Ajouter liens vers timelines.

### Lot 4 - Actions client

- Ajouter renvoi email QR.
- Ajouter gestion remboursement depuis coffret.
- Auditer les actions sensibles.

### Lot 5 - Indicateurs financiers

- Calculer CA global client.
- Calculer revenu Localeo disponible.
- Calculer repartition par commercant sur prestations achetees.
- Calculer repartition par commercant sur prestations validees.
- Afficher remboursements et net.

### Lot 6 - Securite et droits

- Appliquer permissions back-office.
- Masquer les donnees personnelles selon role.
- Reserver coordonnees completes et remboursement au role `ADMIN`.
- Refuser toute delegation `SUPPORT` ou `FINANCE` en MVP sur coordonnees completes et remboursement.
- Ajouter tests d'audit et acces refuse.

## Propositions complementaires utiles

- Afficher une alerte si un coffret en cours expire bientot.
- Afficher une alerte si un email QR recent est en echec.
- Afficher une alerte si un remboursement est en attente ou en echec.
- Afficher les moyens de contact preferes selon les donnees disponibles.
- Ajouter un bouton `Contacter ce client` vers la communication libre avec email/telephone preselectionnes.
- Afficher les notes internes client si un referentiel de notes client est cree.
- Afficher les incidents recents : paiement en erreur, email/SMS en echec, QR regenere, remboursement ouvert.

## Tests attendus

- Recherche par nom.
- Recherche par prenom.
- Recherche par telephone normalise.
- Affichage historique coffrets.
- Filtrage coffrets en cours.
- Renvoi QR refuse sur coffret expire/rembourse/non eligible.
- Renvoi QR cree un email sortant et un audit.
- Remboursement reutilise le workflow existant.
- Calcul du niveau client.
- Achat sans email valide classe en client non consolide.
- Doublon apparent avec email different signale sans fusion automatique.
- Un client a 1 coffret est `Nouveau`.
- Un client a 2 ou 3 coffrets est `Regulier`.
- Un client a 4 a 7 coffrets est `Fidele`.
- Un client a 8 coffrets ou plus est `Ambassadeur`.
- Un role non `ADMIN` ne peut pas voir les coordonnees completes ni initier un remboursement.
- Masquage donnees personnelles selon role.
