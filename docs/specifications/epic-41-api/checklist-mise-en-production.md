# Epic 41 - Checklist de mise en production

> Consolidation documentaire du 18 septembre 2026 : contributions Backend et Animation réunies. Les cases sont un modèle de contrôle à renseigner pour chaque livraison ; elles ne décrivent pas le statut de réalisation de l’EPIC.

Cette checklist complete le diagnostic interne `/internal/animation-locale/readiness`. Une production est
autorisee uniquement lorsque tous les controles techniques sont vrais et que les preuves externes sont tracees.

| Prerequis | Configuration ou preuve | Validation |
| --- | --- | --- |
| URLs publiques HTTPS | Templates Animation et Participant complets, placeholders présents, plus URL du portail gestionnaire | [ ] |
| Stockage objet prive | `LOCALEO_DOCUMENT_STORAGE_PROVIDER` non local et secrets objet configures | [ ] |
| Stripe | Cle, secret webhook, evenements de test et idempotence verifies | [ ] |
| Emails | Mode production, identite d'envoi et contenus valides | [ ] |
| Flyers | Direction artistique validee ; conformite du rendu implemente, distinction QR public/QR personnel, scans, impression et declinaisons recettees selon [la specification](flyer-direction-artistique.md) | [ ] |
| Application commercant | Premiere version avec parcours QR Coffret et Animation recettee de bout en bout | [ ] |
| RGPD | Validation juridique datee des durees et informations participant | [ ] |
| Habilitations participant | Attribuer `animation:supprimer_participant` uniquement aux gestionnaires autorises et verifier un refus `403` pour les autres profils | [ ] |
| Reprise | Sauvegarde, restauration et reprise des operations testees | [ ] |
| Charge et securite | Rapports de recette attaches au dossier de release | [ ] |

Variables de preuve applicative :

- `LOCALEO_ANIMATION_RGPD_LEGAL_VALIDATED=true`
- `LOCALEO_ANIMATION_EMAIL_CONTENT_VALIDATED=true`
- `LOCALEO_ANIMATION_FLYER_CHARTER_VALIDATED=true`

Ces variables ne remplacent pas les preuves de validation ; elles attestent qu'elles ont ete controlees
dans le processus de release.
