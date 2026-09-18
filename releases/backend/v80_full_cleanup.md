# Localeo V80 - Nettoyage complet admin et références résiduelles

## Objectif
Nettoyer les résidus du modèle `AchatCoffret` encore utilisés là où le pivot métier est désormais `CoffretInstance`, en particulier dans SQLAdmin et les éléments connexes.

## Actions appliquées
- correction des références cassées `*.achat_id` vers `*.coffret_instance_id`
- passe globale sur les fichiers texte du projet
- nettoyage ciblé du fichier `app/infrastructure/admin/admin.py`

## Vérifications visées
- partie admin SQLAdmin
- vues liées aux validations
- vues liées aux transactions de validation
- vues liées aux statuts de prestation coffret instance

## Références détectées avant nettoyage
### DDL/schema.sql
- ligne 74 — `achat_id` → `achat_id UUID NOT NULL REFERENCES achats_coffret(id),`
- ligne 91 — `achat_id` → `achat_id UUID NOT NULL REFERENCES achats_coffret(id),`
- ligne 100 — `achat_id` → `achat_id UUID NOT NULL REFERENCES achats_coffret(id),`
- ligne 108 — `achat_id` → `achat_id UUID NOT NULL REFERENCES achats_coffret(id),`
- ligne 123 — `achat_id` → `CREATE INDEX idx_paiements_achat_id ON paiements(achat_id);`
- ligne 124 — `achat_id` → `CREATE INDEX idx_statuts_prestation_coffret_instance_achat_id ON statuts_prestation_coffret_instance(achat_id);`
- ligne 127 — `achat_id` → `CREATE INDEX idx_transactions_validation_achat_id ON transactions_validation(achat_id);`
- ligne 129 — `achat_id` → `CREATE INDEX idx_validations_prestation_achat_id ON validations_prestation(achat_id);`

### DDL/v74_coffret_instances.sql
- ligne 6 — `achat_id` → `achat_id UUID NOT NULL REFERENCES achats_coffret(id),`
- ligne 26 — `achat_id` → `ALTER TABLE transactions_validation DROP COLUMN IF EXISTS achat_id;`
- ligne 29 — `achat_id` → `ALTER TABLE validations_prestation DROP COLUMN IF EXISTS achat_id;`

### docs/v74_parcours_unifie_particulier_professionnel.md
- ligne 23 — `achat_id` → `- `GET /clients/achats-coffret/{achat_id}/coffrets-instances``

### docs/v79_admin_runtime_fix.md
- ligne 6 — `achat_id` → `- `StatutPrestationCoffretInstanceOrm.achat_id``
- ligne 14 — `achat_id` → `- remplacement de `achat_id` par `coffret_instance_id` dans les vues admin concernées`
- ligne 6 — `StatutPrestationCoffretInstanceOrm.achat_id` → `- `StatutPrestationCoffretInstanceOrm.achat_id``

### app/api/clients_api.py
- ligne 10 — `achat_id` → `@router.get("/achats-coffret/{achat_id}")`
- ligne 11 — `achat_id` → `def consulter_detail_achat_coffret(achat_id: str):`
- ligne 12 — `achat_id` → `return ConsulterDetailAchatCoffret(SqlAlchemyUnitOfWork).execute(achat_id)`
- ligne 14 — `achat_id` → `@router.get("/achats-coffret/{achat_id}/coffrets-instances")`
- ligne 15 — `achat_id` → `def lister_coffret_instances_achat(achat_id: str):`
- ligne 16 — `achat_id` → `return ListerCoffretInstancesAchat(SqlAlchemyUnitOfWork).execute(achat_id)`

### app/domaine/modeles.py
- ligne 112 — `achat_id` → `achat_id: UUID`
- ligne 131 — `achat_id` → `achat_id: UUID`

### app/infrastructure/admin/admin.py
- ligne 127 — `achat_id` → `column_list = [PaiementOrm.id, PaiementOrm.achat_id, PaiementOrm.provider, PaiementOrm.status]`
- ligne 137 — `achat_id` → `column_list = [TransactionValidationOrm.id, TransactionValidationOrm.achat_id, TransactionValidationOrm.statut]`
- ligne 137 — `TransactionValidationOrm.achat_id` → `column_list = [TransactionValidationOrm.id, TransactionValidationOrm.achat_id, TransactionValidationOrm.statut]`

### app/infrastructure/paiement/paiement_gateway.py
- ligne 12 — `achat_id` → `def initialiser_paiement(self, achat_id: str, nom_coffret: str, montant_centimes: int, email_client: str, quantite: int = 1):`
- ligne 13 — `achat_id` → `logger.info("Initialisation paiement pour achat %s", achat_id)`
- ligne 26 — `achat_id` → `metadata={"achat_id": achat_id},`

### app/infrastructure/persistence/mappers.py
- ligne 79 — `achat_id` → `id=orm.id, achat_id=orm.achat_id, coffret_id=orm.coffret_id, statut=StatutCoffretInstance(orm.statut),`
- ligne 87 — `achat_id` → `id=entity.id, achat_id=entity.achat_id, coffret_id=entity.coffret_id, statut=entity.statut.value,`
- ligne 94 — `achat_id` → `return Paiement(id=orm.id, achat_id=orm.achat_id, provider=orm.provider, transaction_id=orm.transaction_id, status=orm.status, payload=orm.payload, date_creation=orm.date_creation)`
- ligne 97 — `achat_id` → `return PaiementOrm(id=entity.id, achat_id=entity.achat_id, provider=entity.provider, transaction_id=entity.transaction_id, status=entity.status, payload=entity.payload, date_creation=entity.date_creation)`

### app/infrastructure/persistence/models.py
- ligne 101 — `achat_id` → `achat_id = Column(UUID(as_uuid=True), ForeignKey("achats_coffret.id"), nullable=False, index=True)`
- ligne 117 — `achat_id` → `achat_id = Column(UUID(as_uuid=True), ForeignKey("achats_coffret.id"), nullable=False, index=True)`

### app/infrastructure/securite/service_qr.py
- ligne 22 — `achat_id` → `def generer_qr_achat_coffret(self, achat_id: str, expiration_ts: int | None = None) -> str:`
- ligne 23 — `achat_id` → `logger.info("Génération QR achat coffret pour %s", achat_id)`
- ligne 24 — `achat_id` → `payload = {"typ": "achat_coffret", "aid": achat_id, "exp": expiration_ts or int(time.time()) + 90 * 24 * 3600}`

### app/infrastructure/persistence/repositories/repositories_sqlalchemy.py
- ligne 112 — `achat_id` → `def lister_par_achat(self, achat_id):`
- ligne 113 — `achat_id` → `rows = self.session.execute(select(CoffretInstanceOrm).where(CoffretInstanceOrm.achat_id == achat_id).order_by(CoffretInstanceOrm.date_creation)).scalars().all()`
- ligne 121 — `achat_id` → `def obtenir_par_achat(self, achat_id):`
- ligne 122 — `achat_id` → `orm = self.session.execute(select(PaiementOrm).where(PaiementOrm.achat_id == achat_id)).scalar_one_or_none()`

### app/domaine/repositories/protocols.py
- ligne 38 — `achat_id` → `def lister_par_achat(self, achat_id: Any) -> Sequence[Any]: ...`
- ligne 42 — `achat_id` → `def obtenir_par_achat(self, achat_id: Any) -> Any | None: ...`

### app/application/use_cases/consulter_historique_prestations_commercant.py
- ligne 19 — `achat_id` → `"achat_id": str(achat.id),`

### app/application/use_cases/initialiser_paiement.py
- ligne 36 — `achat_id` → `created = timed_call(scope, "repository_add_achat", lambda: uow.achats_coffret.ajouter(achat), achat_id=str(achat.id))`
- ligne 43 — `achat_id` → `return {"achat_id": str(created.id), "checkout_url": url}`

### app/application/use_cases/valider_paiement.py
- ligne 46 — `achat_id` → `achat_id = payload["metadata"]["achat_id"]`
- ligne 47 — `achat_id` → `achat = uow.achats_coffret.obtenir(achat_id)`
- ligne 59 — `achat_id` → `id=uuid.uuid4(), achat_id=achat.id, provider="paiement_externe",`
- ligne 74 — `achat_id` → `achat_id=achat.id,`
- ligne 96 — `achat_id` → `achat_id=achat.id,`
- ligne 122 — `achat_id` → `"achat_id": str(achat.id),`

### app/application/use_cases/valider_prestation.py
- ligne 57 — `achat_id` → `achat = uow.achats_coffret.obtenir(coffret_instance.achat_id)`

### app/application/use_cases/consulter_detail_achat_coffret.py
- ligne 5 — `achat_id` → `def execute(self, achat_id):`
- ligne 7 — `achat_id` → `achat = uow.achats_coffret.obtenir(achat_id)`
- ligne 13 — `achat_id` → `"achat_id": str(achat.id),`

### app/application/use_cases/activer_coffret_instance.py
- ligne 22 — `achat_id` → `achat = uow.achats_coffret.obtenir(coffret_instance.achat_id)`

### app/application/use_cases/lister_coffret_instances_achat.py
- ligne 5 — `achat_id` → `def execute(self, achat_id: str):`
- ligne 7 — `achat_id` → `instances = uow.coffrets_instances.lister_par_achat(achat_id)`

## Résultat
- nettoyage appliqué sur les références ORM résiduelles les plus critiques
- base préparée pour une nouvelle relance runtime

## Point honnête
Cette passe est un nettoyage structurel et de cohérence textuelle. Le meilleur prochain test reste une relance complète de l'application pour remonter la prochaine éventuelle erreur runtime réelle.
