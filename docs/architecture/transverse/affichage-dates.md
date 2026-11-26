# Dates affichées — heure de Paris

Décision utilisateur du 9 octobre 2026, correctif **UX-DATES-20261009-PARIS**.

Les interfaces Localeo affichent les instants dans le fuseau IANA `Europe/Paris`,
indépendamment du fuseau du navigateur ou du serveur. Les règles du fuseau assurent
le passage été/hiver ; aucun décalage fixe de +1 h ou +2 h n’est appliqué.
Un libellé « heure de Paris » accompagne les horaires ou leur contexte d’affichage.

Une date civile (`YYYY-MM-DD`) reste le même jour et ne reçoit pas d’heure
artificielle. Une date absente ou invalide produit le libellé de remplacement du
parcours. Les timestamps historiques sans offset suivent la convention UTC des
contrats existants. Les dates avec offset conservent leur instant réel.

## Présentation Live sans heure — 21 novembre 2026

Sur demande utilisateur, **Localeo Live affiche uniquement la date**, y compris
pour les inscriptions, validations, résultats, messages, actualités, échéances
de lots et dernières lectures réussies. Le jour reste calculé dans `Europe/Paris` ;
une date civile reste inchangée. Les libellés relatifs serveur contenant des
heures ou minutes ne remplacent plus cette date. La mention « heure de Paris »
n'accompagne pas ces dates seules.

**Exception demandée le 21 novembre 2026 :** la page de détail d’une étape du
parcours personnel Live affiche aussi l’heure des preuves enregistrées : réponse
confirmée, étape achevée, visite ou passage validé. Cette restitution utilise
`Europe/Paris`, avec la mention « heure de Paris », indépendamment du fuseau
de l’appareil et en tenant compte du changement été/hiver. Elle concerne les
passeports, chasses, vitrines et juste prix ; leurs autres dates restent sans
heure. Seul un horodatage réel de la preuve autorise cet affichage : une date
civile, une valeur absente ou invalide ne reçoit aucune heure reconstruite. Le
détail signale alors que la date et l’heure ne sont pas disponibles. Les instants
historiques sans offset restent interprétés en UTC selon la convention commune.

Live affiche aussi la date et l’heure de Paris d’un retrait confirmé à partir
de `remise_at` dans l’historique et le détail personnel du lot. Si l’horodatage
est absent, invalide ou limité à une date civile, l’interface affiche
« Date et heure de retrait indisponibles. ».

Cette règle de présentation ne modifie ni les instants API, ni les contrôles
d'ouverture ou d'expiration, ni les horaires pratiques des commerces, ni les
instants exportés dans l'agenda. Les composants partagés conservent leur
présentation avec heure hors de Live, notamment la confirmation Marketplace.

Les fins d’animation constituent des **bornes exclusives** : pour afficher le
dernier jour inclus, retirer une milliseconde au timestamp avant de déterminer
le jour de Paris, comme dans Animation et le flyer. Une valeur civile
`YYYY-MM-DD` désigne déjà ce dernier jour et reste inchangée. Cette présentation
spécifique ne s’applique pas aux expirations de lots/coffrets, ni aux messages,
inscriptions et tirages. La fin prévue n’implique pas une clôture effective ;
voir la [règle Live](../../specifications/epic-73-animation-et-ou-coffrets/localeo-live-entree-unique.md#correctif-du-21-novembre-2026--date-prévue-et-clôture-effective).

## Portée applicative

- **Pro** : formateurs partagés, historique salarié, PIN, notifications, animations,
  rendez-vous, documents juridiques et mention de fuseau dans le pied de page.
- **Marketplace et Live** : dates des coffrets, prestations, activités et parcours
  clients par les formateurs communs.
- **Animation** : dates de consultation et de notifications ; champs d’actualités
  affichés en heure de Paris et reconvertis avec les outils Paris existants.
- **Backend et interfaces internes** : ERP, Support, Atelier, OnBoard et Control,
  écrans de préparation/génération/conservation Animation, formateur partagé
  `app/infrastructure/erp/dates.js`. SQLAdmin et les pages de supervision serveur
  possèdent déjà `_render_local_datetime` en Europe/Paris (CET/CEST).

Les API, la persistance, les journaux techniques UTC, les échéances métier et les
planifications restent inchangés. Aucune migration ni nouvelle configuration.
Le générateur de démonstration conserve ses timestamps : ce sont les interfaces
qui changent leur présentation, pas les données. Les scripts et contrats de test
restent dans chaque dépôt applicatif.

## Vérification et limites

Les preuves ciblées contrôlent l’hiver, l’été, le changement de jour, les dates
civiles, les entrées invalides et les timestamps sans offset avec des navigateurs
hors de France. Les tests d’interfaces vérifient aussi le chargement du formateur
partagé, pour éviter de transformer une correction de date en panne de démarrage.

La conversion des **filtres** d’historique Pro et le choix du mois initial de son
tableau de bord restent dépendants du fuseau navigateur : ils ne sont pas modifiés
par ce correctif d’affichage. Cette limite ne concerne pas les heures rendues à
l’écran mais les bornes de recherche. Les formulaires exprimant explicitement un
fuseau de rendez-vous conservent leurs règles de saisie.

Aucune recette distante ni déploiement effectué pour ce lot. Les travaux UX
Coffret déjà présents dans Pro et sa documentation sont conservés séparément.


## Preuves locales du 9 octobre 2026

Backend : **492 tests Python réussis**, dont l’architecture obligatoire, les
formateurs SQLAdmin, les routes Support et le cycle PWA. Chromium vérifie le
formateur dans les zones Los Angeles, Tokyo et Paris, avec les deux transitions
été/hiver, minuit, UTC naïf, date civile et jour impossible. Le parcours réel
Support est vérifié depuis Los Angeles. Les quatre cycles PWA internes, les six
scénarios Administration OnBoard, les six scénarios Conservation, les parcours
Préparation et Génération ERP mobile/ordinateur réussissent. Les fixtures servent
la nouvelle dépendance de présentation ; les attentes des chargements asynchrones
sont explicites, sans retirer d’assertion de pagination.

Pro : **35 tests unitaires** sous `TZ=America/Los_Angeles`, scénario navigateur
sur l’historique et build production réussis. Les corrections UX Coffret du lot
précédent restent présentes et ne sont pas comptées comme tests de fuseau.

Marketplace/Live : **8 tests Node** et **2 scénarios navigateur** sur la vraie
confirmation client depuis Los Angeles/Tokyo, hiver/été, lisibilité à 390 pixels ;
lint ciblé et build isolé réussis. Les deux scénarios ont réussi, mais le runner
Playwright est resté bloqué à l’arrêt du serveur sous Windows et a été interrompu
manuellement : aucune sortie normale de ce runner n’est revendiquée.

Animation : **8 tests Node**, **2 scénarios navigateur** du formulaire Actualité
depuis Los Angeles/Tokyo, avec conservation de l’instant après enregistrement et
refus des heures absentes au changement d’heure, y compris en programmation.
Contrôle de types, lint et build réussis.

Complément final Pro : validation calendaire des valeurs ISO (jour impossible,
mois et année bissextile). Les **19 tests du formateur** passent sous Los Angeles,
dont six ajoutés après la suite initiale de 35 ; ces nombres se recouvrent.
Ce dernier ajustement du parseur est vérifié par ses tests ciblés, sans nouvelle
exécution du build complet.
