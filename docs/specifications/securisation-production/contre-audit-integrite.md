# Corrections du contre-audit d'integrite

Reference de depart : 39d8c54, contre-audit REAUDIT-001 a REAUDIT-009.

## REAUDIT-001 - Activations concurrentes

L'activation prend le verrou commun de l'instance avant toute decision et refuse
un remboursement en cours. Un rejeu avec le meme beneficiaire retourne l'etat
existant sans nouveaux droits, email ni rotation de token. Le lien secret de
consultation n'est pas reconstitue : le rejeu retourne consultation_url=null.
Un autre beneficiaire est refuse. La base impose une prestation par instance.

Deploiement : v221 refuse les doublons historiques sans en supprimer aucun.
Inventorier par GROUP BY coffret_instance_id, prestation_coffret_id HAVING count(*)>1
et rapprocher consommations et preuves avant toute correction historique.
Recette : deux activations PostgreSQL simultanees, un seul jeu de droits et email,
rejeu sans rotation et unicite SQL ; controle du beneficiaire dans le domaine.

## REAUDIT-002 - Expiration concurrente

Le batch prend le verrou de chaque instance avant lecture de ses droits, avec
FOR UPDATE SKIP LOCKED. Une instance deja verrouillee est reportee au prochain
passage. Les instances remboursees ou gelees par un remboursement EN_COURS
sont exclues. La consommation et le credit d'expiration ne peuvent donc pas
valider simultanement le meme droit. Les compteurs portent sur les instances
effectivement selectionnees et verrouillees. Le dry-run applique le meme filtre.
Recette PostgreSQL : gel, transaction concurrente puis consommation confirmee ;
aucun droit reecrit ni email d'expiration.

## REAUDIT-003 - Intention de remboursement durable

v222 ajoute intention_stripe (requete et premiere_demande). La transaction
la persiste avec le gel EN_COURS avant l'appel PSP. Toute reprise reutilise les
parametres exacts et la cle initiale ; apres 23 heures, ou pour une demande
historique incertaine sans intention, seul un rapprochement est autorise. Une
reference fournisseur deja connue interdit egalement une nouvelle creation.
Cette marge precede la retention minimale Stripe de 24 heures :
https://docs.stripe.com/api/idempotent_requests

Le webhook retrouve aussi la demande via metadata.remboursement_achat_id et
controle montant, devise, paiement et identifiants metier contre l'intention.
Un remboursement inconnu provoque une erreur rejouable, sans acquittement
idempotent. Apres rapprochement, renvoyer le webhook signe depuis Stripe.
Ne jamais remplacer la cle ni rajeunir premiere_demande pour forcer une reprise.
Les demandes historiques EN_COURS/ECHEC necessitent verification Stripe avant
reprise ; aucune date de demande n'est inventee par la migration.

## REAUDIT-004 - Etats de transfert monotones

Apres l'appel Stripe, la campagne relit sous verrou mouvement puis paiement.
Une confirmation ou une inversion par webhook prime sur le retour HTTP, y compris
un timeout. Les webhooks verrouillent les mouvements dans l'ordre de leurs ids,
puis paiement et reversement. Une inversion reste terminale meme si un evenement
created ancien arrive ensuite. La campagne recalcule son agregat depuis les
mouvements persistants au lieu de recopier un objet lu avant l'appel.
Recette : webhook pendant l'appel, retour HTTP reussi ou perdu, puis evenements
reversed/created dans le desordre ; aucun retour a TRANSFER_DEMANDE.

## REAUDIT-005 - Index historique de revalidation

v223 retire les index uniques autonomes non partiels portant exclusivement
sur le droit consomme. Cela couvre l'index cree historiquement par v147, que
v219 (contraintes seulement) ne supprimait pas. L'unicite de la validation active
et celle de la transaction restent obligatoires. Les migrations appliquees ne
sont pas modifiees. Recette sur chaine complete depuis une base vide : validation,
annulation, nouvelle validation, rejet du rejeu ancien et d'une seconde active.

## REAUDIT-006 - Activation conforme aux conditions vendues

Activation manuelle et distribution d'un gain utilisent les lignes du snapshot
d'achat : composition, commercants, versions, libelles et duree de validite.
Les prestations ajoutees apres vente n'ajoutent aucun droit ; une modification
du catalogue ne remplace pas la version vendue. Snapshot absent, version absente,
duree inconnue ou composition dupliquee bloquent l'activation sans droits ni email.
Rapprocher les preuves historiques avant de completer un dossier incomplet ;
ne jamais reconstruire silencieusement ces conditions depuis le catalogue actuel.
Recette : achat professionnel, catalogue modifie ensuite, activation et controle
de la version 1, de la composition d'origine et des 365 jours vendus.

## REAUDIT-007 - Quota des essais OTP

Chaque code errone consomme une tentative persistante avant la reponse HTTP
d'erreur. Le service retourne un refus sans exception transactionnelle ; l'API
committe puis renvoie l'erreur metier uniforme. Le verrou du challenge serialise
les essais concurrents. Apres cinq essais, meme le bon code est refuse, sans
creation de token. Les erreurs ulterieures d'activation (conditions obsoletes,
echec SQL) conservent leur rollback normal. Recette HTTP sur PostgreSQL : cinq
reponses 409, compteurs 1 a 5, puis bon OTP refuse avec compteur stable a 5.

## REAUDIT-008 - Perimetre communal de reservation

La permission MODIFIER est completee par la verification de la ressource cible :
commande ANIMATION_LOTS, partenaire identique et commune de l'animation identique
a la commune active habilitee. Sinon, reponse 404 avant creation de compte ou
reservation, meme pour deux communes du meme partenaire. Recette HTTP : autre
commune refusee sans mutation, puis meme commande autorisee dans sa commune.

## REAUDIT-009 - Confirmation des lots financee integralement

La confirmation de paiement des lots exige un credit actif non expire et une
reponse de capture CAPTURED du montant exact. Le debit est realise avant la
creation du paiement local et le passage a PAYEE, dans la meme transaction.
Une reservation disparue entre lecture et capture provoque un rollback ; ni
paiement confirme ni materialisation. Le webhook reste rejouable apres resolution
de l'incident. Ne pas forcer le statut PAYEE sur un financement incomplet.
La capture et l'expiration (y compris le batch de rapprochement) verrouillent
compte puis reservation, comme la consultation,
et relit l'etat apres verrouillage. Un autre evenement pour le meme paiement
deja confirme reprend uniquement la materialisation, sans seconde capture.
Recette PostgreSQL : expiration concurrente avant capture, financement mixte
4000 centimes Stripe + 6000 credit, puis rejeu avec un seul debit.
