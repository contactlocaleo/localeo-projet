# Cartographie des parcours — étape 1

Commune de référence demandée : **Bouliac**. Visite automatisée sur `https://test-live.localeo.city`, le 18 novembre 2026, dans des navigateurs mobiles vierges (320, 390 et 430 px de large). Les captures sont dans [`../visuels/captures-avant/`](../visuels/captures-avant/).

| Mission | Chemin inspecté et résultat | Statut | Captures |
| --- | --- | --- | --- |
| Entrer et revenir | Racine du domaine → `/live/carnet` ; retour navigateur de `/live/communes` à `/live/decouvrir` avec Bouliac conservée. | OBSERVÉ | `01-accueil-*`, `11-retour-decouvrir-bouliac-390x844.png` |
| Découvrir | `/live/decouvrir` → recherche « Bouliac » → « Suivre Bouliac » → liste « En ce moment » et « Prochainement ». | OBSERVÉ | `02-decouvrir-bouliac-*` |
| Consulter une animation | Liste → fiches « Test juste prix Local », « Test jeu des vitrines », « Test tombola Locale ». Les fiches affichent dates, conditions disponibles, lots prévus et accès à l’inscription. | OBSERVÉ | `03-detail-juste-prix-*`, `05-detail-vitrines-*`, `06-detail-tombola-*` |
| Rejoindre | Fiche « Test juste prix Local » → formulaire d’inscription avec nom, prénom, e-mail, téléphone et choix obligatoires. Aucun envoi réalisé. | OBSERVÉ | `04-inscription-juste-prix-390x844.png` |
| Accès QR | Un lien d’ajout d’animation avec code volontairement invalide affiche « Cet accès n’est plus disponible » et « Retrouver mon accès ». Aucun QR réel disponible pour un test positif. | OBSERVÉ | `10-qr-invalide-390x844.png` |
| Suivre une participation | `/live/animations` affiche un état vide et un lien de récupération. Le suivi d’une participation réelle reste à vérifier. | OBSERVÉ | `07-participations-vides-390x844.png` |
| Gérer les lots | `/live/lots` passe par « Lecture de vos lots et tirages… », puis affiche « Aucun lot à utiliser ou retirer pour le moment ». Aucun gain utilisable dans le navigateur vierge. | OBSERVÉ | `08-lots-vides-390x844.png` |
| Retrouver le carnet | `/live/retrouver-mon-carnet` demande l’e-mail utilisé pour les inscriptions et propose l’envoi d’un lien personnel. Le champ vide bloque l’envoi par validation native. | OBSERVÉ | `09-retrouver-carnet-390x844.png` |
| Calendrier | Dans Découvrir, groupes « En ce moment » et « Prochainement » ; les cartes indiquent des périodes et ouvrent les fiches. `/live/calendrier` redirige vers Découvrir. | OBSERVÉ | `02-decouvrir-bouliac-*`, `03-detail-juste-prix-*`, `06-detail-tombola-*` |
| Utiliser un lot, participer au jeu, suivi après retour | Le code contient ces parcours, mais aucune inscription, participation ou remise de lot n’a été déclenchée. | DÉDUIT | Aucune capture de résultat personnel |

La rubrique Coffrets est visible dans le carnet vide ; l’onglet bas reste « Mon carnet / Mes lots / Découvrir ». Son comportement au-delà de cette présence n’a pas été étudié.
