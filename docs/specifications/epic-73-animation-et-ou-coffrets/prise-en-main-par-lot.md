# E73 — Fonctionnalités et accès par lot

Ce compte rendu accompagne le [suivi de réalisation](suivi-implementation.md).
Les lots 01 à 10 sont implémentés et leurs contrôles et commits locaux sont
consignés dans le suivi. La recette humaine et les vérifications sur l’hébergement
restent à réaliser ; ce compte rendu ne constitue pas une mise en service.
**Aucun push, déploiement ou changement d’un environnement partagé n’a été effectué.**

Les chemins commençant par `/internal/` sont relatifs au backend de l’environnement
qui sera déployé ultérieurement. Les autres accès indiquent les menus du portail
Animation. Les noms de domaine réels et leur configuration ne sont pas présumés
disponibles. Les droits, la commune active et les modules conditionnent les menus.

| Lot | Fonctionnalités à regarder | Accès et profil | Essai conseillé |
| --- | --- | --- | --- |
| 00 — Préparation | Dossier canonique, plan, conventions UX, preuves et restrictions de livraison | Ce dossier et le suivi d’implémentation ; aucun écran propre | Lire le périmètre des dix lots et les limites avant de préparer une livraison |
| 01 — Comptes et équipes | Inscription/demande de rattachement, récupération d’accès, choix organisation/commune, invitations, profils et délégations, transfert accepté de responsabilité | Animation → **Compte et équipe**, responsable ; ERP → **Accès Animation**, `/internal/erp/acces-animation` et `/internal/erp/acces-animation/organisations`, opérateur habilité | Inviter un collaborateur, accepter avec son compte, retirer une autorisation et vérifier le refus avec sa session encore ouverte |
| 02 — Périmètres commerçants | Animation, Coffrets ou les deux ; activation ERP, prérequis OnBoard adaptés, menus Pro et continuité des engagements lors du retrait | ERP → fiche commerçant → périmètres ; OnBoard → dossier du commerçant ; Pro → compte de ce commerce | Ouvrir un commerce Animation uniquement : préparer son dossier sans prestations ni pièces propres aux Coffrets, puis vérifier ses menus et ses refus d’accès directs |
| 03 — Souscriptions et modules | Catalogue versionné, achat/cadeau/essai, droits et quotas, renouvellement, changement d’offre, facturation et demandes de remboursement contrôlées | Animation → **Abonnement** et **Finance**, responsable ou délégation Achat ; ERP → catalogue/modules/souscriptions/remboursements selon habilitation | Comparer droit absent, essai et droit acheté ; vérifier l’échéance, le quota disponible et la conservation des conditions déjà acquises |
| 04 — Dotation externe | Choix explicite Coffrets ou lots libres, gestion externe, description et ordre des lots, tirage, suppléants, suivi contact/remise | Animation → **Animations** → créer ou ouvrir une fiche → configuration/dotation puis tirage et lots | Créer une animation à lots libres externes, publier, tirer et déclarer une remise sans produire de commande Coffret ni de QR de bon |
| 05 — Bons numériques | Modèles et exemplaires, stock affecté exclusivement, attribution, email au gagnant, bon indivisible, QR et PIN, prolongation/révocation/remplacement/correction tracés | Animation → fiche → **Lots** pour une dotation libre numérique ; Pro → scan du bon ; participant → lien du bon reçu et parcours de validation par PIN | Attribuer deux exemplaires, consommer l’un, rescanner pour voir le reçu ; remplacer un QR et vérifier le refus de l’ancien |
| 06 — Import commerçants | XLSX/CSV, modèle et association des colonnes, aperçu, conflits email/SIRET, deltas champ par champ, lignes valides, rapport et reprise du même import | Animation → **Import commerçants**, module actif et autorisation dédiée ; arbitrages sensibles dans l’ERP | Importer un fichier de moins de 100 lignes/2 Mo, corriger une fiche, réimporter une version modifiée : la correction locale doit être conservée ou présentée comme conflit |
| 07 — Chasse accompagnée | Module chasse et quota indépendant, demande complète, préparation à distance, compléments, suivi du délai, relance et validation terrain | Animation → **Modèles** → chasse, puis suivi dans la fiche ; ERP → **Préparations Animation**, `/internal/erp/preparations-animation` | Soumettre une demande, demander un complément côté Localeo, répondre puis déclarer la préparation prête ; vérifier le calendrier et les droits avant publication |
| 08 — Communication | Campagnes immédiates/programmées, quatre audiences, messages Live et Push facultatif, quota mensuel, fréquence, suspensions et reprises, alertes internes regroupées | Animation → fiche → communication participants, module et autorisation Communication ; participant → messagerie/préférences Live ; Ops pour les alertes | Envoyer une campagne synthétique à un participant sans permission navigateur : le message reste lisible dans Live ; vérifier exclusion de fréquence et absence de double dépôt au rejeu |
| 09 — Parcours et résultats | Assistant de publication, site public Animation sur socle partagé, fiches commerçants, continuité des carnets, support privé, nouvelle édition, sources de diffusion, objectifs, bilans et satisfaction | Animation → **Animations**, **Bilans**, **Support** ; fiche → assistant/bilan/nouvelle édition ; site public configuré en surface Animation ; Live après clôture | Parcourir découverte → inscription → participation → bilan, puis créer une nouvelle édition sans recopier participants, gains ni consentements |
| 10 — Exploitation et sortie | Coûts internes et budgets, exports responsables, fermeture accompagnée, conservation et restauration contrôlées, lectures paginées et vérifications finales | Animation → **Compte et équipe** → export/fermeture ; ERP → `/internal/erp/pilotage-economique` et `/internal/erp/reversibilite` ; Ops pour les alertes ; maintenance par commandes opérateur | Demander un export puis lire son manifeste ; demander une fermeture avec un engagement ouvert et vérifier qu’elle reste bloquée jusqu’à sa résolution ou une reprise effectivement disponible |

## Préparer une recette ultérieure

Utiliser des comptes distincts : administrateur Localeo, opérateur avec habilitation
dédiée, responsable d’organisation, gestionnaire, lecteur, commerçant et salarié.
Prévoir une commune et une organisation étrangères pour vérifier les refus. Le
générateur local et ses tests fournissent des scénarios synthétiques ; un fichier
d’accès privé n’est jamais ajouté à ce dossier documentaire.

Les parcours d’achat, emails et Push ont été testés avec des transports isolés.
Leur recette sur un environnement requiert une préparation de livraison séparée :
versions cohérentes des dépôts, migrations, stockage, calendrier ouvré, clés et
origines, workers et fournisseurs de test. Cette page n’autorise pas leur activation.

La validation humaine prévue reste **Localeo puis Martignas-sur-Jalle**. La cible
de capacité est de **10 communes, 10 000 participants au total et 10 utilisateurs
simultanés**. Les exercices sur l’hébergement doivent démontrer **4 heures maximum
de perte de données** et **8 heures maximum de reprise**. Les résultats locaux et
les limites détaillées figurent dans le suivi, sans équivalence automatique avec
une recette hébergée.
