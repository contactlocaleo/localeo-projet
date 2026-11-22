# Limites, sécurité des actions et reprise

## Couverture

- Première connexion **de cette session** seulement. Création de compte organisateur, activation, récupération du mot de passe et MFA non testés.
- Deux créations de brouillons et un clonage exécutés. Publication non exécutée : le brouillon tombola reste bloqué par les invitations et accords manquants ; aucun accord réel n’a été sollicité pour débloquer le parcours.
- Invitations et notifications existantes consultées, sans envoi ni relance. L’environnement est marqué TEST, mais cela ne prouve pas la neutralisation des fournisseurs d’email/push ni que tous les comptes existants sont des destinataires jetables.
- Clôture explorée jusqu’à sa confirmation. Pas de clôture, tirage, remplacement de gagnant, remise, fin ou archivage d’une animation existante : ces objets ne sont pas des créations isolées de cet audit.
- Import : flux, dépôt, mapping et aperçu réalisés ; aucune confirmation, aucun traitement de création de fiche. Les deux lignes sans identité email/SIRET n’établissent pas le comportement des doublons partageant une identité forte. Aucune activation de marchand.
- Ajout individuel d’une nouvelle fiche non trouvé dans les surfaces visitées. Cette absence locale n’est pas une preuve d’inexistence dans l’ERP ou d’autres profils.
- Communication bloquée par HTTP 500 reproduit. Création, aperçu, programmation et envoi d’une campagne restent non vérifiés dans cet environnement.
- Consultation des bilans, pas d’export PDF/CSV exécuté. Flyer publié consulté, pas de régénération ni diffusion. Aperçu de création observé, fidélité du PDF final non vérifiée.
- Pas de publication d’une tombola publique supplémentaire : le parcours demandé de tombola locale a été testé en brouillon. Les autres moteurs ont été parcourus uniquement aux endroits documentés.
- Aucun chronométrage humain. La durée de la session automatisée inclut lecture du code, reprises d’outils et rédaction ; elle ne mesure pas le temps d’usage. Promesse 5–10 minutes non établie.
- Mobile : Chromium de bureau redimensionné à 390 × 844, sans émulation tactile ni appareil physique. Pas de contrôle Safari/iOS, Android réel, clavier virtuel, zoom 200 %, lecteur d’écran, réseau dégradé ou hors ligne. L’absence de débordement global ne prouve pas l’absence de tout défilement local.
- Code local lu à un commit connu ; version déployée non attestée. Les conclusions issues du code sont séparées des observations à l’écran. Aucun test applicatif ou build lancé : aucune modification applicative.
- Quelques sélecteurs Playwright ont nécessité une correction (radio/texte, libellés accessibles, boutons homonymes). Ce sont des incidents d’instrumentation, pas des erreurs utilisateur du produit. Un premier contexte a été perdu lors d’un délai dépassé ; reconnexion au même compte, avant toute création de données.
- Les captures `fullPage` suivent le document navigateur ; l’application comporte aussi un défilement interne. Une capture n’est donc pas un relevé exhaustif de toutes les sections d’une rubrique. Les captures 60–63 complètent les zones de publication, dotation, confirmation de clôture et gagnant après défilement.

## Objets de test créés

Tous ont été créés sur l’origine TEST demandée, dans le contexte organisateur autorisé, avec des noms explicites. Ils sont conservés pour permettre une reprise ; aucun nettoyage destructif n’a été entrepris.

| Objet | Identifiant / nom | État laissé |
| --- | --- | --- |
| Tombola | `9e7d3fe3-0046-4b92-9705-5c53ad2916da` — UX TEST 2026-11-18 — Tombola brouillon | Brouillon ; 01–05 décembre ; un commerce sélectionné ; une demande Non envoyée ; un lot libre fictif. |
| Passeport | `d83a41f2-aeb4-42a9-8447-fedba0476a1e` — UX TEST 2026-11-18 — Passeport brouillon | Brouillon ; 01–05 décembre ; deux commerces sélectionnés ; seuil deux ; deux demandes À envoyer ; un lot libre fictif. |
| Clone | `3f7df158-21ad-4b76-b233-a44e9ade9d79` — UX TEST 2026-11-18 — Clone tombola | Brouillon ; 08–12 décembre ; textes et paramètres sélectionnés ; commerces et lots à préparer de nouveau. |
| Flux d’import | UX TEST 2026-11-18 | Nouveau flux du contexte Bouliac. |
| Dépôt d’import | `ux-test-2026-11-18.csv`, déposé vers 11 h 31 Paris | Aperçu à vérifier ; deux créations proposées, zéro sélection, aucune confirmation. |

Les lots sont nommés « Lot fictif UX — ne pas distribuer », avec consignes d’absence de remise et de contact. Le fichier CSV a été fourni en mémoire au navigateur, sans email, téléphone, SIRET ou secret, et sans copie applicative locale. Ses dix colonnes sont celles du modèle fourni ; les deux lignes partagent un nom synthétique et une adresse de test. Le flux et le dépôt sont des écritures réelles sur TEST, pas une simulation de l’interface.

## Protection des informations

Le prompt a été archivé avec `[CONFIDENTIEL]` pour les deux identifiants. Aucun état d’authentification, cookie, jeton, trace réseau complète, corps d’authentification ou fichier de configuration opérateur n’a été enregistré. La capture de connexion a été prise avant saisie. Les coordonnées visibles des gagnants et du détail marchand ont été masquées à la capture. Les relevés HTTP ne contiennent que chemin et statut d’erreur.

## Prochain geste

Attendre l’autorisation explicite de l’utilisateur pour l’étape 2 Localeo Animation. Préparer ensuite le workshop à partir de ces faits, en conservant les limites ci-dessus. Une publication complète et une recette des communications demanderont des destinataires de test maîtrisés et un service de communication fonctionnel. Aucun vote Pro antérieur ne s’applique à cette exécution Animation.
