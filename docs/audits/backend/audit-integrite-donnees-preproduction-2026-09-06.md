## VERDICT DE MISE EN PRODUCTION

🔴 **NO-GO**

Des scénarios réalistes peuvent laisser un coffret utilisable après remboursement, confirmer un achat insuffisamment financé, calculer un reversement sur le mauvais montant ou perdre un document. Les protections doivent être corrigées avant l’ouverture aux transactions réelles.

### 1. Executive summary

Audit en lecture seule du commit `0e386a2a83d1b3a284cff60b85463df271787f1b`, branche `main`.

Le socle comporte des protections utiles : Unit of Work partagé, contraintes d’unicité, validation atomique d’une prestation, signatures Stripe, contrôle des communes dans l’ERP et intention Checkout persistée avant l’appel externe.

Ces protections restent incomplètes entre les parcours. Les principaux écarts touchent les remboursements, le crédit B2B, les reprises de reversement, les versions vendues et les accès historiques du back-office.

Quatre assertions isolées, exécutées en mémoire à partir de fonctions extraites du code, reproduisent des défauts du remboursement et du stockage documentaire, ainsi que l’absence de contrôle d’origine sur GET. Elles ne constituent pas une recette PostgreSQL ni un test complet de l’application.

Aucune migration, opération financière, modification de fichier, commit ou push n’a été effectué. La suite complète de tests n’a pas été réexécutée pendant cet audit.

### 2. Risques bloquants avant production

| ID | Sévérité | Risque |
|---|---|---|
| DATA-001 | HAUTE | Remboursement confirmé par webhook sans invalidation du coffret |
| DATA-002 | HAUTE | Paiement mixte confirmé après libération du crédit réservé |
| DATA-003 | HAUTE | Remboursement Stripe calculé sur le montant total, crédit compris |
| DATA-004 | HAUTE | Transfer Stripe exécuté avant persistance durable de son intention |
| DATA-005 | HAUTE | Validation et remboursement simultanés incompatibles |
| DATA-006 | HAUTE | Reversement calculé depuis la prestation courante, malgré une version vendue figée |
| DATA-008 | HAUTE | Restrictions ERP contournables par des accès historiques |
| DATA-009 | HAUTE | Publication par GET exposée au CSRF |
| DATA-010 | HAUTE | Ancien fichier supprimé avant confirmation de sa modification en base |
| DATA-011 | HAUTE | Suppression documentaire sans contrôle de conservation |

Les constats dépendant de Stripe Connect ou du crédit B2B supposent l’activation de ces fonctionnalités. **Leur configuration réelle en production n’a pas été vérifiée.** Les autres constats suffisent néanmoins à justifier le verdict.

### 3. Analyse intégrité des données

**DATA-006 — HAUTE — Montant de reversement détaché de la version vendue**

- **Localisation :** `ServiceValidationPrestation.executer`, [service_validation_prestation.py:113](../../../../localeo-backend/app/application/exploitation/services/service_validation_prestation.py#L113), puis calcul du mouvement ; `ServiceAtelierErp.enregistrer_prestation`, [atelier_erp.py:255](../../../../localeo-backend/app/application/commercialisation/services/atelier_erp.py#L255).
- **Règle :** préservation des conditions vendues, EPIC 60 §5 ; recette `COM-005` et `FIN-001`.
- **Problème :** le statut d’instance conserve `prestation_version`, mais la validation charge la prestation courante et utilise son `montant_reversement`.
- **Scénario :** vente avec reversement de 20 € ; modification du catalogue à 30 € ; consommation de l’ancien coffret ; création d’un mouvement de 30 €.
- **Impact :** dette commerçant et commission différentes des conditions historiques.
- **Correction minimale :** calculer le mouvement depuis la version référencée par le droit vendu. Ne pas remplacer silencieusement une version historique introuvable par la version courante.

**DATA-007 — MOYENNE — Prestation réouverte mais impossible à revalider**

- **Localisation :** [AnnulerValidationPrestation.execute:54](../../../../localeo-backend/app/application/exploitation/use_cases/annuler_validation_prestation.py#L54), création d’une nouvelle validation dans [service_validation_prestation.py:149](../../../../localeo-backend/app/application/exploitation/services/service_validation_prestation.py#L149), unicité dans [models.py:675](../../../../localeo-backend/app/infrastructure/persistence/models.py#L675).
- **Règle :** EPIC 31 : annulation encadrée, recalcul des droits et conservation de l’historique.
- **Problème :** l’annulation remet le droit à `A_VALIDER`, mais conserve la validation historique. Une nouvelle validation tente un nouvel INSERT alors que `statut_prestation_coffret_instance_id` est unique. La clé d’idempotence du mouvement reste également attachée au même droit.
- **Scénario :** validation → annulation → nouvelle transaction QR → tentative de validation → violation d’unicité.
- **Impact :** droit affiché comme disponible mais inutilisable. Rejouer l’ancienne transaction peut aussi renvoyer son ancien succès sans reconsommer le droit.
- **Correction minimale :** distinguer les occurrences de validation, conserver leur annulation et garantir une seule occurrence active. Adapter l’idempotence à cette occurrence, sans supprimer l’historique.

**DATA-011 — HAUTE — Conservation documentaire non imposée**

- **Localisation :** [GestionDocumentaireService.supprimer_document:392](../../../../localeo-backend/app/application/documentaire/services/gestion_documentaire.py#L392), appelée par [GestionDocumentaireAdmin.supprimer_documentaire:8866](../../../../localeo-backend/app/infrastructure/admin/admin.py#L8866).
- **Règle :** spécification fonctionnelle, UC-21 : conservation des contrats et documents comptables, conservation des anciennes versions légales.
- **Problème :** la suppression contrôle l’existence de documents dérivés, mais aucune durée de conservation. Le remplacement du contenu conserve aussi le même document tout en supprimant son ancien fichier.
- **Scénario :** suppression d’une ancienne version légale sans document dérivé, avant la fin de sa conservation.
- **Impact :** disparition d’une preuve documentaire. La récupération dépend alors d’éventuelles sauvegardes ou versions du stockage, non auditées.
- **Correction minimale :** rendre les versions probantes immuables ; imposer une politique de conservation dans les commandes de suppression et de remplacement ; privilégier l’archivage.

**DATA-013 — MOYENNE — Plusieurs documents publics peuvent rester publiés pour le même type et scope**

- **Localisation :** [GestionDocumentaireService.publier_document:322](../../../../localeo-backend/app/application/documentaire/services/gestion_documentaire.py#L322), [DocumentOrm:1482](../../../../localeo-backend/app/infrastructure/persistence/models.py#L1482).
- **Règle :** UC-21 : une version publiée par couple type/scope ; publication de la suivante = archivage de la précédente.
- **Scénario :** publier successivement deux documents CGV de même scope. La commande publie le second sans rechercher ni archiver le premier.
- **Impact :** plusieurs versions restent accessibles comme documents publiés, même si une lecture « dernier document » en privilégie une.
- **Correction minimale :** sérialiser la publication par type/scope et archiver la précédente dans la même transaction. Garantir l’unicité de la publication active.

Les contraintes SQL examinées protègent notamment les racines de paiement des commandes, certaines relations uniques et les montants des lignes. Elles ne protègent pas, à elles seules, les invariants traversant remboursement, consommation et reversement.

### 4. Transactions et concurrence

**DATA-005 — HAUTE — Course entre remboursement et consommation**

- **Localisation :** `RemboursementAchatAdmin._motif_ineligibilite_execution` et `remboursement_execute`, [admin.py:11164](../../../../localeo-backend/app/infrastructure/admin/admin.py#L11164) ; [ServiceValidationPrestation.executer:83](../../../../localeo-backend/app/application/exploitation/services/service_validation_prestation.py#L83).
- **Règle :** atomicité des transitions et cohérence entre droits consommés et remboursement.
- **Problème :** le contrôle d’éligibilité au remboursement et la validation ne verrouillent pas ensemble l’instance.

Scénario de concurrence :

1. A vérifie que le coffret est actif et sans prestation consommée.
2. B valide une prestation et crée son mouvement de reversement.
3. A déclenche le remboursement Stripe.
4. A annule l’instance, mais sa sélection initiale des mouvements ne contenait pas celui créé par B.

**Impact :** prestation consommée, remboursement client et mouvement commerçant peuvent coexister.

**Correction minimale :** verrouiller la même instance avant toute décision de validation ou remboursement. Persister ensuite une intention de remboursement qui bloque la consommation avant l’appel Stripe, puis finaliser ou réconcilier cette intention.

Ce scénario découle de l’ordonnancement du code ; **il n’a pas été exécuté avec deux connexions PostgreSQL**. L’analyse suppose l’isolation PostgreSQL usuelle `READ COMMITTED`, aucune isolation renforcée n’étant définie dans la création du moteur inspectée. [Documentation PostgreSQL](https://www.postgresql.org/docs/current/transaction-iso.html).

**DATA-012 — MOYENNE — Deux dernières prestations validées, instance encore ACTIVE**

- **Localisation :** calcul des prestations restantes dans [service_validation_prestation.py:129](../../../../localeo-backend/app/application/exploitation/services/service_validation_prestation.py#L129) ; lecture d’instance sans verrou dans [repositories_sqlalchemy.py:264](../../../../localeo-backend/app/infrastructure/persistence/repositories/repositories_sqlalchemy.py#L264).
- **Règle :** une instance dont toutes les prestations sont consommées doit devenir `UTILISE`.
- **Scénario :** A et B valident deux prestations différentes ; chacun voit l’autre prestation encore disponible ; chacun conserve l’instance active ; les deux transactions terminent.
- **Impact :** état d’instance incohérent avec ses droits, faussant les parcours et indicateurs qui utilisent ce statut.
- **Correction minimale :** sérialiser les validations d’une même instance avant de recalculer son état.

**Protection confirmée :** la mise à jour conditionnelle `A_VALIDER → VALIDEE`, contrôlée par `rowcount`, protège une **même prestation** contre la double consommation. Elle ne sérialise pas les autres transitions de son instance.

### 5. Respect des ADR et conventions

Les références déterminantes sont :

- l’ADR du 28 août sur le placement des invariants dans le domaine ;
- l’ADR Stripe Connect du 9 juillet ;
- les conventions de sécurité et de transactions ;
- les spécifications EPIC 60, EPIC 50 et documentaire ;
- les critères de recette portant sur les versions vendues et les reversements.

La conformité est **partielle** :

- l’ERP applique des contrôles explicites de rôle, commune, version et idempotence ;
- les paiements utilisent des signatures et des identifiants de déduplication ;
- les commandes historiques n’appliquent pas systématiquement les mêmes autorisations ;
- les invariants de remboursement diffèrent entre action administrative et webhook ;
- les intentions financières durables sont correctement introduites pour le Checkout unitaire, mais pas pour la campagne de transfers.

Les références et preuves sont regroupées dans la matrice de la section 11.

### 6. Architecture et DDD

Le découpage domaine/application/infrastructure existe. Le Unit of Work instancie ses repositories avec une session commune et annule la transaction sur exception : [sqlalchemy_unit_of_work.py](../../../../localeo-backend/app/infrastructure/persistence/uow/sqlalchemy_unit_of_work.py).

La recherche d’imports directs n’a pas relevé de dépendance SQLAlchemy, FastAPI ou Pydantic dans `app/domaine`. Cela ne constitue pas une preuve exhaustive de pureté de toutes les dépendances transitives.

L’écart principal est comportemental : les règles de remboursement résident en partie dans SQLAdmin et en partie dans un traitement de webhook. **DATA-001 et DATA-003 montrent une conséquence concrète de cette duplication.**

La correction doit rester ciblée : une transition de remboursement commune, des faits financiers explicites et une orchestration partagée entre administration et webhook. Une réécriture générale du backend n’est pas nécessaire.

### 7. Sécurité des données

**DATA-008 — HAUTE — Autorisations différentes selon le point d’entrée**

- **Localisation :** [contexte_erp:7](../../../../localeo-backend/app/security/erp.py#L7), comparé à [require_admin_session:19](../../../../localeo-backend/app/api/profils_commercants_api.py#L19) et [credit_achat_b2b_api.py](../../../../localeo-backend/app/api/credit_achat_b2b_api.py).
- **Règle :** EPIC 35 : permissions côté serveur ; EPIC 60 : contrôle des communes et séparation des fonctions administratives.
- **Problème :** plusieurs routes historiques vérifient uniquement `admin_authenticated`. Elles ne vérifient ni rôle ni commune. Le filtrage SQLAdmin par `admin_ville_id` est un filtre de navigation, pas une autorisation.
- **Scénario :** un opérateur EXPLOITATION limité à une commune appelle directement une publication de profil hors périmètre ; si le crédit B2B est actif, il peut également atteindre l’ajustement d’un compte par identifiant.
- **Impact :** modification hors territoire ou accès à une commande financière sans permission dédiée.
- **Correction minimale :** appliquer une politique commune aux routes historiques, actions SQLAdmin et accès par identifiant. Contrôler la ressource chargée, pas seulement la visibilité du menu.

**DATA-009 — HAUTE — Publication sensible par GET**

- **Localisation :** [admin_approuver_publication_profil:15029](../../../../localeo-backend/app/infrastructure/admin/admin.py#L15029), [CsrfOriginMiddleware:112](../../../../localeo-backend/app/security/http.py#L112).
- **Règle :** protection des commandes administratives contre le CSRF.
- **Problème :** GET publie effectivement le profil et commit. Le middleware ne contrôle que les méthodes de mutation.
- **Scénario :** un administrateur connecté suit un lien externe vers cette URL contenant un identifiant de version connu de l’attaquant. Une navigation GET peut transporter le cookie de session.
- **Impact :** publication sans action intentionnelle de modération.
- **Correction minimale :** transformer la commande en POST protégé. Examiner aussi les autres GET déclenchant des batchs et les actions SQLAdmin.
- **Vérification exécutée :** la fonction de décision du middleware ne demande aucun contrôle d’origine pour GET avec cookie de session.

**Protections constatées :** schémas ERP avec `extra="forbid"`, contrôle des ressources par commune, CSRF des commandes ERP et authentification des webhooks Stripe. Je n’ai pas identifié de mass assignment arbitraire dans les commandes ERP examinées : [erp_schemas.py:7](../../../../localeo-backend/app/api/erp_schemas.py#L7).

### 8. Intégrations externes

**DATA-001 — HAUTE — Confirmation asynchrone du remboursement incomplète**

- **Localisation :** [_mettre_a_jour_remboursement_orm:251](../../../../localeo-backend/app/application/referencement/use_cases/stripe_connect_onboarding.py#L251).
- **Règle :** cohérence remboursement/droits et transitions fiables des projections Stripe.
- **Scénario :** l’action administrative reçoit `pending` ; un webhook ultérieur reçoit `succeeded` ; seul le remboursement devient `REMBOURSE`. L’instance reste utilisable.
- **Impact :** consommation possible après remboursement. La commande administrative ignore ensuite les remboursements déjà marqués `REMBOURSE`.
- **Autre défaut de transition :** un ancien événement `pending` reçu après `succeeded` remet le remboursement à `EN_COURS`.
- **Correction minimale :** finalisation commune et atomique : remboursement, invalidation des droits, restitution du crédit applicable, audit et notification. Empêcher les régressions dues à l’ordre des événements.
- **Vérification exécutée :** les deux comportements sont reproduits en mémoire avec la fonction extraite.

**DATA-002 — HAUTE — Crédit expiré ignoré lors de la confirmation d’un achat mixte**

- **Localisation :** [ServiceCreditAchatB2b.reserver:189](../../../../localeo-backend/app/application/conformite_fiscale_bum/service_credit_achat_b2b.py#L189), [ValiderPaiement.execute:378](../../../../localeo-backend/app/application/gestion_achats/use_cases/valider_paiement.py#L378).
- **Règle :** PRD-475 : crédit réservé puis capturé au paiement.
- **Scénario :** achat de 100 €, dont 60 € de crédit et 40 € Stripe ; réservation expirée puis marquée `EXPIRED` par une consultation ou réconciliation ; paiement des 40 € ; le webhook ne trouve aucune réservation `ACTIVE` et confirme l’achat sans capturer les 60 €.
- **Impact :** achat confirmé insuffisamment financé ; crédit libéré potentiellement réutilisable.
- **Cause complémentaire :** réservation limitée à 30 minutes, alors que le Checkout créé ne fournit pas `expires_at`. Stripe utilise normalement 24 heures. [Documentation Stripe](https://docs.stripe.com/api/checkout/sessions/create).
- **Correction minimale :** vérifier systématiquement la ventilation financière persistée, même si la réservation n’est plus active ; traiter le paiement tardif en réconciliation explicite ; coordonner expiration Checkout et réservation.

**DATA-003 — HAUTE — Remboursement mixte calculé sur le total brut**

- **Localisation :** [CreerRemboursementClientVision360.execute:609](../../../../localeo-backend/app/application/support/use_cases/vision_360_client_backoffice.py#L609), [RemboursementAchatAdmin.remboursement_execute:11370](../../../../localeo-backend/app/infrastructure/admin/admin.py#L11370).
- **Règle :** PRD-476 : rembourser uniquement la part Stripe et restituer séparément le crédit.
- **Scénario :** achat de 100 €, payé 60 € en crédit et 40 € par carte ; la demande calcule 100 € pour l’instance et transmet ce montant au remboursement Stripe.
- **Impact :** refus du remboursement faute de montant disponible ; pour un achat multi-instance dont le paiement Stripe global reste suffisant, remboursement monétaire supérieur à la part de l’instance.
- **Correction minimale :** conserver et utiliser une allocation par instance des parts Stripe et crédit, avec répartition déterministe des centimes et plafonds cumulés.

**DATA-004 — HAUTE — Transfer Stripe avant commit de l’intention**

- **Localisation :** [LancerCampagneTransfersStripe.execute:201](../../../../localeo-backend/app/application/gestion_reversement/use_cases/transfers_stripe.py#L201), [_metadata_transfer:160](../../../../localeo-backend/app/application/gestion_reversement/use_cases/transfers_stripe.py#L160).
- **Règle :** ADR Stripe Connect : journalisation, idempotence et reprise financière.
- **Scénario :** création locale des identifiants de reversement/paiement ; transfer accepté par Stripe ; panne avant le commit final de campagne ; rollback des identifiants locaux.
- **Impact :** transfer réel sans rattachement local durable. Le webhook peut répondre `transfer_not_found`.
- **Reprise :** la clé issue du mouvement reste stable, mais les UUID transmis dans les métadonnées sont recréés. Une reprise peut donc utiliser la même clé avec des paramètres différents, ce que Stripe rejette. La conservation des clés Stripe n’est pas illimitée. [Contrat d’idempotence Stripe](https://docs.stripe.com/api/idempotent_requests).
- **Correction minimale :** persister l’intention et tous les paramètres avant l’appel ; reprendre exactement cette intention ; réconcilier les résultats incertains avant toute nouvelle émission.

**DATA-010 — HAUTE — Suppression du fichier avant commit SQL**

- **Localisation :** [GestionDocumentaireService.mettre_a_jour_contenu_document:342](../../../../localeo-backend/app/application/documentaire/services/gestion_documentaire.py#L342), [MettreAJourContenuDocument.execute:212](../../../../localeo-backend/app/application/documentaire/use_cases/gestion_documentaire.py#L212).
- **Règle :** cohérence entre métadonnées persistées et contenu externe.
- **Scénario :** écriture du nouveau fichier ; suppression de l’ancien ; échec du commit SQL ; rollback vers l’ancienne référence, dont le fichier a disparu.
- **Impact :** document inaccessible et nouveau fichier orphelin.
- **Correction minimale :** conserver l’ancien objet jusqu’au commit ; supprimer ensuite via une tâche durable, uniquement si aucune référence et aucune conservation ne l’exigent.
- **Vérification exécutée :** suppression de l’ancien binaire reproduite en stockage mémoire avant tout commit.

**DATA-014 — MOYENNE — Emails et SMS réservés sans reprise automatique après arrêt**

- **Localisation :** [LancerBatchEmails.execute:19](../../../../localeo-backend/app/application/exploitation/use_cases/emails_batch.py#L19), [repositories_sqlalchemy.py:925](../../../../localeo-backend/app/infrastructure/persistence/repositories/repositories_sqlalchemy.py#L925). Même structure dans [sms_batch.py](../../../../localeo-backend/app/application/exploitation/use_cases/sms_batch.py).
- **Règle :** outbox relançable, reprise des traitements interrompus.
- **Scénario :** réservation de messages en `EN_COURS_ENVOI`, commit, arrêt du processus avant envoi.
- **Impact :** messages exclus des prochains envois ; absence d’identifiant fournisseur empêchant aussi leur synchronisation. Intervention nécessaire pour les débloquer.
- **Correction minimale :** réservation atomique avec échéance et reprise des réservations abandonnées. Prévoir le cas ambigu « fournisseur accepté, réponse perdue ».
- **Distinction :** le WebPush examiné possède une reprise des réservations anciennes ; sa livraison « au moins une fois » n’est pas assimilée à une anomalie.

### 9. Migrations

**DATA-015 — MOYENNE — Procédure standard non autonome sur base vierge**

- **Localisation :** [discover_migrations / runner](../../../../localeo-backend/scripts/database/apply_migrations.py#L51), [v71_reversements.sql:1](../../../../localeo-backend/sql/v71_reversements.sql#L1), [bootstrap.py:557](../../../../localeo-backend/app/bootstrap.py#L557).
- **Règle :** procédure de déploiement reproductible par migrations versionnées.
- **Problème :** les 116 scripts numérotés commencent à v71, qui référence immédiatement `commercants`. Le runner ne charge pas `schema.sql`. Le bootstrap DDL est désactivé en production.
- **Scénario :** exécuter la commande de pré-déploiement documentée sur une base vide ; la première migration rencontre des tables référencées absentes.
- **Impact :** première installation ou reconstruction sans sauvegarde non reproductible par la procédure standard.
- **Correction minimale :** définir un baseline versionné et une procédure d’initialisation unique, puis tester base vierge et mise à niveau. Le bootstrap ORM utilisé par l’outil de performance ne suffit pas à prouver cette procédure.

**Protections présentes :** ordre numérique, verrou consultatif de session, contrôle des checksums, exclusion des scripts de purge/seed et mode dry-run sans écriture de migration.

**NON AUDITÉ — éléments insuffisants :** conformité du schéma réellement déployé, contraintes effectives, données historiques incompatibles, durées de verrouillage et restauration. Il manque un état de schéma, l’historique des migrations et une base représentative autorisée pour ces essais. Aucune migration n’a été exécutée.

### 10. Dette technique secondaire

**DATA-016 — FAIBLE — Référentiel documentaire contradictoire**

- **Localisation :** [architecture-solution.md:390](../../architecture/transverse/architecture-solution.md#L390), opposée à l’ADR Stripe Connect acceptée.
- **Problème :** une section décrit encore les paiements commerçants comme manuels en V1, alors que l’ADR exclut ce fallback.
- **Scénario / impact :** une procédure d’exploitation construite depuis cette section peut orienter vers un traitement financier contraire à la cible.
- **Correction minimale :** supprimer l’ambiguïté et désigner explicitement l’ADR applicable.

Je n’en déduis pas l’existence d’un fallback bancaire exécutable dans le code.

### 11. Matrice de conformité

Les états portent sur les règles et parcours examinés, pas sur une certification globale du backend.

| Référence | Règle | État | Preuve |
|---|---|---|---|
| [Architecture solution](../../architecture/transverse/architecture-solution.md) | Session commune aux repositories du UOW | ✅ Conforme | `SqlAlchemyUnitOfWork.__enter__` |
| [ADR domaine, 28 août](../../architecture/decisions/ADR-2026-08-28-domaine-avant-services-applicatifs.md) | Source unique des invariants | ⚠️ Partiel | Remboursement réparti entre SQLAdmin et webhook |
| [ADR Stripe Connect](../../architecture/decisions/ADR-2026-07-09-epic-39-stripe-connect-implementation.md) | Opérations financières traçables et reprenables | ⚠️ Partiel | DATA-001, DATA-004 |
| [Conventions sécurité](../../architecture/transverse/conventions-securite.md) | Validation résistante aux répétitions | ⚠️ Partiel | UPDATE conditionnel présent ; DATA-007 après annulation |
| [EPIC 35](../../architecture/backend/epics/epic-35-profils-backoffice-differencies-architecture.md) | Permissions serveur par rôle | ❌ Non conforme | DATA-008 |
| [EPIC 60, §2](../../specifications/epic-60-vision-360-commercialisation/specifications-fonctionnelles.md#L22) | Cloisonnement des ressources | ⚠️ Partiel | ERP contrôlé ; routes historiques divergentes |
| [EPIC 60, §5](../../specifications/epic-60-vision-360-commercialisation/specifications-fonctionnelles.md#L133) | Préservation des conditions vendues | ⚠️ Partiel | Versions enregistrées ; DATA-006 au calcul du reversement |
| [EPIC 50, PRD-475/476](../../roadmap/terminees/epic-50-conformite-fiscale-bum-backlog.md#L562) | Capture et restitution exactes du crédit | ❌ Non conforme | DATA-002, DATA-003 |
| [Spécification fonctionnelle, UC-21](../../produit/specification-fonctionnelle.md#L340) | Unicité de publication et conservation | ❌ Non conforme | DATA-011, DATA-013 |
| [Checkout durable F06](../../specifications/securisation-production/f06-checkout-durable.md) | Intention persistée avant Stripe | ✅ Conforme sur l’ordre des opérations | `InitialiserPaiement` commit avant `_envoyer_demande_checkout` |
| [Reprise WebPush F07](../../specifications/securisation-production/f07-reprise-webpush.md) | Reprise des réservations abandonnées | ✅ Conforme sur le mécanisme examiné | Verrouillage et sélection des réservations anciennes |
| [Conventions migrations](../../specifications/securisation-production/migrations.md) | Sérialisation des runners | ✅ Conforme dans le code | Verrou conservé sur une connexion |
| [Guide de déploiement](../../exploitation/technique/reference-guide-exploitation-plateforme.md#L1004) | Initialisation reproductible | ⚠️ Partiel | DATA-015 |
| [Recette générale](../../exploitation/recette/cahier-recette-generale-avant-mep.md) | Validation sur environnement représentatif | ❓ Non vérifiable ici | Recette complète non exécutée dans cet audit |

### 12. Plan de remédiation

#### P0 — avant production

1. **Unifier le remboursement et ses effets** : DATA-001, DATA-003, DATA-005. Tester réponse immédiate, confirmation différée, événements désordonnés et consommation concurrente.
2. **Sécuriser la capture du crédit** : DATA-002. Tester paiement après expiration, crédit réutilisé entre-temps et webhook retardé.
3. **Persister les intentions de transfer avant Stripe** : DATA-004. Injecter une panne après acceptation fournisseur et avant sauvegarde du résultat ; vérifier la reprise sans nouvel effet financier.
4. **Calculer les reversements depuis les versions vendues** : DATA-006. Acheter N, modifier en N+1, consommer N et comparer les montants.
5. **Uniformiser les autorisations et supprimer les mutations GET** : DATA-008, DATA-009. Tester chaque rôle sur sa commune et hors périmètre, y compris via les anciennes routes.
6. **Protéger les documents** : DATA-010, DATA-011. Simuler un commit en échec et vérifier que l’ancien document reste lisible ; refuser les suppressions interdites par la conservation.
7. **Valider la livraison sur PostgreSQL jetable** : schéma vierge, migration représentative, contraintes et scénarios à deux connexions. Résoudre DATA-015 avant une première installation.

Ces corrections doivent inclure les tests de non-régression correspondants. Un nouveau GO exige leurs résultats exécutés et une vérification du schéma cible.

#### P1 — immédiatement après mise en production

Sous réserve de ne pas exposer auparavant les parcours concernés :

- DATA-007 : rendre cohérente la revalidation après annulation ;
- DATA-012 : fiabiliser l’état final d’instance ;
- DATA-013 : garantir la publication documentaire unique ;
- DATA-014 : reprendre automatiquement les emails/SMS abandonnés.

Si ces parcours sont nécessaires dès l’ouverture, leurs corrections remontent en P0.

#### P2 — amélioration

- DATA-016 : consolider le référentiel documentaire.
- Regrouper progressivement les invariants du remboursement dans le domaine.
- Étendre les essais de panne aux frontières SQL/Stripe/stockage/messagerie.

**NON AUDITÉ — éléments insuffisants :** configuration réelle des fournisseurs, protections du stockage, sauvegardes/restauration, configuration des comptes et secrets déployés, charge réelle et conformité effective des données existantes. Le rapport établit des défauts dans le code ; il ne prétend pas constater des incidents déjà survenus.

> **« Si ce backend était mis en production aujourd’hui avec de vraies données clients et de vraies transactions financières, ai-je identifié dans le code un scénario réaliste pouvant corrompre, perdre, dupliquer, exposer ou rendre incohérente la donnée ? »**

**OUI.** Un remboursement confirmé peut laisser le coffret utilisable ; un paiement mixte peut être confirmé sans capture du crédit ; un remplacement documentaire peut supprimer le fichier encore référencé après rollback. Ces scénarios justifient de suspendre la mise en production jusqu’à correction et validation des points P0.
