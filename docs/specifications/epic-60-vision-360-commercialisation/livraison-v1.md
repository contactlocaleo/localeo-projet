# EPIC 60 - Livraison et exploitation V1

Le developpement et le push ne constituent pas un deploiement en production.

## Preparation et bascule

1. Sauvegarder la base selon la procedure habituelle. Appliquer les migrations
   avec `scripts/database/apply_migrations.py`, jusqu'a `v218_epic60_backoffice_erp.sql`,
   avant de demarrer le nouveau code.
2. Verifier les tables de projection, demandes, evenements, alertes,
   notifications, modeles, rattachements et idempotence. Aucune prestation
   vendue n'est migree en modele et aucune activation metier n'est automatique.
3. Configurer les roles/perimetres existants. ADMIN est global ; EXPLOITATION
   exige des UUID de communes explicites. Une session sans role ne donne aucun droit :
   l'IHM redirige vers `/admin/login`, les API renvoient 401. Se reconnecter renouvelle
   le role depuis `LOCALEO_ADMIN_ROLE`. Si le refus 403 persiste apres reconnexion,
   verifier que le compte est configure ADMIN ou EXPLOITATION ; les autres profils
   restent exclus des ateliers. La casse et les espaces autour du role sont normalises.
4. Pour le parcours complet Onboard, activer ses flags existants
   `LOCALEO_FEATURE_MERCHANT_ONBOARDING_ENABLED` et, selon le perimetre fiscal,
   `LOCALEO_FEATURE_BUM_QUALIFICATION_ENABLED`. Les gardes BUM et Stripe
   conservent leur configuration propre ; l'ERP ne les active pas.
5. Demarrer l'ordonnanceur avec son scope `internal:batch`. Verifier la tache
   `commercialisation.reevaluer` chaque minute. La migration alimente la file
   initiale ; les diagnostics restent indetermines jusqu'au calcul.
6. Surveiller les compteurs et vider la file initiale avant la recette
   commerciale. Un lot de 1000/minute traite 10000 coffrets en dix passages
   hors surcroit de mutations. La fraicheur est limitee a 20 minutes.
7. Recetter `/admin` : accueil ERP, creation commercant, reprise Onboard,
   composition, simulation, publication et retrait. Tester aussi un operateur
   limite a une commune.

## Navigation remplacee

### Connexion derriere un proxy HTTPS

Si `POST /admin/login` renvoie `Cross-origin state-changing request rejected`,
verifier que le proxy conserve le Host public. Avec un ancien cookie, la connexion
est elle aussi soumise au controle CSRF. L'origine HTTPS publique peut differer
du transport HTTP entre proxy et application : cet ecart est accepte uniquement
avec `Sec-Fetch-Site: same-origin` et le meme hote/port public. Les domaines tiers,
ports differents et requetes `same-site`/`cross-site` restent refuses. Les en-tetes
`X-Forwarded-*` seuls n'accordent aucune autorisation. Sans preuve navigateur,
le schema ASGI doit correspondre a l'origine publique via la configuration du
proxy de confiance. Les commandes ERP exigent toujours leur jeton CSRF.

| Ancienne destination | Destination canonique |
| --- | --- |
| `/admin` | `/internal/erp` |
| Recherche Vision 360 commercant | `/internal/erp/commercants` |
| Fiche Vision 360 et CRUD commercant | Dossier ERP du commercant |
| Recherche Vision 360 coffret | `/internal/erp/coffrets` |
| Fiche Vision 360 et CRUD coffret | Atelier ERP du coffret |
| Edition d'une prestation | Composition de son coffret |
| `/internal/onboard` | Module Onboard integre dans l'ERP |

Les GET historiques redirigent. Les anciens formulaires CRUD d'ecriture sont
retires (410). Les fonctions specialisees de finance, achats, animations,
support, documents, moderation et supervision restent referencees dans la
navigation avancee ADMIN. Les traitements historiques restent disponibles
selon leurs autorisations propres.

L'entree SQLAdmin « Espace de travail ERP » utilise l'identite explicite
`espace-travail-erp` et la route nommee `admin:view-espace-travail-erp`.
Cette identite doit rester alignee avec le decorateur `expose` : un ecart fait
echouer le rendu du menu de toutes les listes SQLAdmin (`NoMatchFound`). La
recette couvre le rendu du menu complet et la resolution de chaque lien visible.

## Alertes et incidents

Les triggers invalident les projections apres changement de coffret,
prestation, commercant, commune, politique ou qualification BUM. La lecture
ne recalcule pas les donnees metier. Reevaluer controle une correction ;
Publier recalcule toujours les sources courantes.

Un incident de lecture donne INDETERMINE et une alerte technique. Une perte
observee donne une alerte metier, conservee pendant une indetermination
intermediaire. Les causes changees ouvrent une nouvelle occurrence du meme
episode ; le retour vendable resout l'episode. Le retrait volontaire est
identifiable par le statut et l'audit. Un brouillon initial ne genere pas
de fausse perte de disponibilite.

En cas d'echec, verifier la supervision des batchs, PostgreSQL, l'age des
demandes et les droits de la cle. Relancer
`POST /protected/commercialisation/batch/reevaluer?limit=1000` : le traitement
reprend les demandes persistantes, par transactions de 100 et SKIP LOCKED.
Stripe et Brevo ne sont jamais appeles par le diagnostic.

## Canaux optionnels et conservation

Le modele `.env.example` documente :

- `LOCALEO_COM360_WEBPUSH_ENABLED=false` ; necessite aussi Control WebPush
  actif et un abonnement de l'acteur configure, autorise sur le territoire.
- `LOCALEO_COM360_EMAIL_ENABLED=false`, `LOCALEO_COM360_EMAIL_RECIPIENT` vide ;
  renseigner explicitement un destinataire interne habilite avant activation.

Les notifications sont dedupliquees et passent par les outbox existantes.
Elles sont non nominatives ; leurs liens repassent par l'autorisation serveur.
L'activation d'un canal ne renvoie pas retroactivement les alertes historiques.

Idempotence : 24 h. Evenements et alertes fermees : 365 jours. Aucune purge
d'alerte ouverte. Les audits/outbox gardent leur retention existante. Les
mesures de parcours ne stockent pas le contenu des formulaires.

## Retour arriere

Arreter d'abord la nouvelle tache planifiee, puis redeployer le code precedent.
Conserver les tables v218 et les donnees collectees ; ne pas supprimer le
schema. Verifier les offres preparees avant de retablir la vente. Ce repli
est une operation d'exploitation, pas une seconde interface maintenue par V1.
