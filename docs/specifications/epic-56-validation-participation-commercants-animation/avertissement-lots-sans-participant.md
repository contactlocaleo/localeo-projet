# Lots sans prestation chez un participant — 13 septembre 2026

Cette évolution remplace le caractère bloquant de la règle décrite dans la
conception technique, sections 11, 12 et 14.

Un coffret peut être sélectionné, payé et offert dans une animation même s’il ne
contient aucune prestation active d’un commerçant participant. Cette absence ne
bloque pas non plus le retrait d’un commerçant ; les autres conditions de retrait
restent applicables.

Le code `COFFRET_LOT_SANS_PRESTATION_PARTICIPANT` est conservé à titre informatif :

- `validation-publication` le retourne dans `avertissements`, jamais dans
  `erreurs` ; il ne rend pas `valide` faux.
- Le catalogue conserve le coffret dans les résultats `eligible=true` si ses
  autres conditions d’éligibilité sont remplies. Le diagnostic est exposé dans
  `metadata.avertissements`, avec `commercant_ids_couvrants`.
- La création de commande et la transaction de publication n’imposent plus ce
  lien entre lots et participants.
- L’interface affiche : « Un ou plusieurs coffrets ne contiennent aucune
  prestation active d’un commerçant participant. Vous pouvez néanmoins payer
  les lots et publier l’animation. »

Les contrôles de catalogue, de commune, de statut, de financement et de
participation des commerçants à l’animation restent applicables indépendamment.
Il faut déployer le serveur et l’interface pour disposer du comportement complet.

Validation : tests serveur du catalogue, du calcul des lignes de commande, de la
validation et de la transaction de publication ; parcours navigateur vérifiant
le paiement et la publication autorisés malgré l’avertissement, ainsi que le
maintien du blocage des coffrets indisponibles.
