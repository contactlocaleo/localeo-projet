# EPIC 72 — Accès salariés dans Localeo Pro

Spécification du 5 octobre 2026. Le [backlog E72](../../roadmap/en-cours/epic-72-acces-salaries-validation-localeo-pro-backlog.md) conserve les 22 critères et le statut produit ; implémentation et vérifications locales des 7–8 octobre 2026, après publication E70. Aucun déploiement effectué.

- [Utilisation et exploitation](guide-utilisation-exploitation.md).
- [Architecture, invariants et contrats](architecture-contrats.md).
- [Preuves, démonstration et livraison](verification-livraison.md).
- [E70 — Validation par PIN](../epic-70-validation-pin/README.md) : identité partagée du commerce distincte de l'identité individuelle salariée ; livraison indépendante possible.

## Décisions acquises

L'option salariés est désactivée par défaut pour tout commerce, existant ou nouveau. Seuls Admin et Backoffice Localeo l'activent depuis l'ERP. Le responsable dispose alors de la gestion des salariés dans Localeo Pro, sans plafond ni facturation en V1. La possibilité de monétisation future ne crée aucun tarif ni dépendance à un paiement.

Le responsable invite par email. Le lien est à usage unique et valable 24 heures. Son destinataire choisit son mot de passe avant toute connexion. Un email normalisé ne peut appartenir qu'à un seul accès Localeo Pro : pas de cumul responsable/salarié ni de rattachement à un autre commerce, pas de fusion automatique. Les identités ERP restent un espace distinct ; un salarié n'acquiert aucun rôle interne.

Le salarié utilise son navigateur mobile personnel sans installation obligatoire. Après connexion, il arrive sur le scanner Coffret/Animation. Il peut consulter toutes les validations du commerce, quel que soit l'auteur ou le mode, en lecture seule et sans donnée financière. Les autres fonctionnalités, notamment PIN, catalogue, profil commercial, remboursements, exports, messages, facturation et administration Animation, lui sont interdites, y compris par API.

## Parcours et refus

1. **Inviter** : responsable connecté, option activée ; saisie email, confirmation d'envoi ou état d'échec récupérable. L'invitation n'accorde aucun droit. L'ancien lien est annulé lors d'un renvoi. Une invitation expirée peut être renvoyée ; aucune création de compte doublon.
2. **Accepter** : écran public Localeo Pro, email masqué et commerce non modifiables, obtenus par résolution du lien sans le consommer, choix du mot de passe ; acceptation atomique puis invitation à se connecter. Lien expiré, annulé ou utilisé : message générique et orientation vers le responsable, sans révéler de comptes tiers.
3. **Valider** : scanner, récapitulatif minimal, confirmation explicite, résultat serveur ; même éligibilité, consommation et progression que le principal. Un échec réseau ne produit jamais de succès local. Après réponse incertaine, relire le reçu avant toute nouvelle commande.
4. **Historique** : liste paginée des validations du seul commerce, filtres type/date/mode, détail limité au service ou passage, date, résultat et auteur professionnel. Aucun client nominatif, montant, reversement ou export. Les validations anciennes sans auteur individuel sont étiquetées « Compte principal — historique », jamais attribuées rétroactivement à un salarié.
5. **Révoquer** : le responsable révoque un salarié ; refus immédiat des anciennes sessions et confirmations postérieures à l'effet de révocation. L'historique et le compte sont conservés. Une nouvelle invitation ou un reset ne contourne pas sa révocation ; la restauration individuelle explicite reste hors de cette conception, sans décréter le compte irréversible ni réserver l’email à vie.
6. **Désactiver l'option** : ERP, suspension immédiate des salariés et annulation définitive de toutes les invitations en attente. Le compte principal, les comptes salariés et leurs traces sont conservés. Réactivation : salariés non révoqués de nouveau éligibles après nouvelle connexion ; aucune ancienne session ou invitation ressuscitée.
7. **Récupérer** : email autonome, lien unique valable une heure. Mot de passe modifié : toutes les sessions de ce salarié sont invalidées, pas celles du principal ou de ses collègues. L'opération ne lève ni révocation ni suspension. La perte du téléphone est traitée par cette récupération ou la révocation par le responsable ; aucun transfert de session vers un autre appareil.

## Portée et limites

Backend/ERP et Localeo Pro sont concernés. Marketplace/Live n'accueille ni identité salariée ni lien d'invitation ; les droits client restent inchangés. L'application partenaire `localeo-animation` n'acquiert aucun rôle salarié : seul le backend transmet l'attribution de l'acteur dans les traces existantes. Le support E68 présente cette possibilité sans imposer son activation.

Les décisions produit recensées sont résolues. Le [rattachement commun de conservation](../identite-acces/conservation-validations-acces.md) est établi depuis le 7 octobre sur l'Annexe A, sans durée nouvelle propre à E72. La [matrice de livraison](verification-livraison.md) consigne les preuves locales d’implémentation et de conservation, ainsi que les contrôles d’exploitation restant à effectuer avant mise en service.
