# v179 - Epic 51 Vision 360 des achats

## Livraisons

- nouvelle Vision 360 BackOffice centree sur une commande ou un achat historique ;
- recherche par reference metier, client et references Stripe ;
- synthese commande, achats enfants, instances, documents, remboursements et communications ;
- detail des tentatives de paiement et selection non ambigue du paiement faisant foi ;
- suivi du montant brut, des frais Stripe, du net Stripe et des commissions Localeo ;
- synchronisation des Balance Transactions et prise en charge des commandes de lots Animation ;
- chronologie consolidee et alertes actionnables ;
- masquage des donnees personnelles et audit de leur consultation complete ;
- API interne sous `/internal/gestion-achats/vision-360` ;
- migration `sql/v179_epic51_vision_360_achats.sql`.

## Deploiement

1. appliquer les migrations avec `scripts/database/apply_migrations.py` ;
2. verifier le readiness du schema ;
3. controler un achat unitaire, une commande Pro et un lot Animation ;
4. verifier que les paiements Stripe de plus de 24 heures sans frais remontent une alerte ;
5. mesurer les temps de reponse de la recherche, du detail et de la chronologie.
