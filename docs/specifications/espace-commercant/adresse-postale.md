# Adresse postale du commerce — référence commune

Décision utilisateur du 20 septembre 2026. Applications concernées : backend, ERP,
backoffice historique, Onboard, portail Commerçant et Localeo Animation.

## 1. Source de vérité et périmètre

L’adresse de visite est portée par la fiche `Commercant`, sous `adresse_postale`.
Elle décrit l’établissement, indépendamment de son contact, de l’adresse fiscale
et de la commune de rattachement `ville_id`. Une localité postale et une commune
de rattachement ne sont pas substituables. Il n’existe plus d’adresse commerçante
à renseigner séparément pour chaque nouvelle demande de génération d’animation.

Le périmètre livré est l’adresse française (`pays: FR`). Les données existantes
peuvent rester sans adresse pendant leur complétion. La migration ne déduit pas
une rue du nom de la commune et ne reprend pas automatiquement une adresse fiscale.
La saisie d’une adresse structurellement valide ne certifie pas son existence
physique ; aucun service de validation postale externe n’est appelé.

## 2. Structure postale et normalisation

Références consultées le 20 septembre 2026 :
[AFNOR NF Z10-011, janvier 2013](https://www.boutique.afnor.org/fr-fr/norme/nf-z10011/adresse-postale-redaction-de-ladresse-postale-regles-de-presentation-du-cour/fa178533/40541)
et [règles de présentation de La Poste](https://www.laposte.fr/conseils-pratiques/bien-rediger-l-adresse-d-une-lettre-ou-d-un-colis).
Le modèle organise le bloc postal sur six lignes au maximum ; les lignes
inutilisées sont omises. Chaque ligne d’adresse est limitée à 38 caractères,
espaces compris. Le nom du commerce fournit l’identité du destinataire (ligne 1) ;
les champs d’adresse correspondent aux lignes 2 à 6 ci-dessous.

| Champ | Rôle | Présence |
| --- | --- | --- |
| `complement_destinataire` | Ligne 2 : service, appartement, étage | Facultatif |
| `complement_geographique` | Ligne 3 : bâtiment, résidence, entrée | Facultatif |
| `voie` | Ligne 4 : numéro éventuel et libellé de voie | Voie ou lieu-dit obligatoire |
| `lieu_dit` | Ligne 5 : lieu-dit ou distribution spéciale | Voie ou lieu-dit obligatoire |
| `code_postal` | Début de ligne 6, chaîne de cinq chiffres | Obligatoire |
| `localite` | Fin de ligne 6, localité postale | Obligatoire |
| `pays` | `FR`, non ajouté au bloc national | Obligatoire, valeur FR |

Le domaine centralise la normalisation des espaces et de la présentation postale
(majuscules, accents et ponctuation). Les contrôles portent sur le résultat
normalisé, notamment la ligne composée `code_postal + espace + localite`.
Les valeurs trop longues sont refusées avec une explication ; aucune troncature
ou abréviation devinée ne modifie une adresse. Un numéro de voie n’est pas inventé
ni imposé pour un lieu qui n’en possède pas. Un code postal reste une chaîne,
afin de conserver son zéro initial. L’adresse doit être affichée comme texte
échappé dans toutes les interfaces.

```json
{
  "complement_destinataire": null,
  "complement_geographique": null,
  "voie": "12 RUE DU BOURG",
  "lieu_dit": null,
  "code_postal": "33360",
  "localite": "LATRESNE",
  "pays": "FR"
}
```

Cet exemple est synthétique et ne constitue pas l’adresse d’un commerce réel.

## 3. Droits et modifications

Le commerçant authentifié peut consulter et modifier sa propre adresse depuis
son profil, y compris dans le parcours de préparation de son compte. Son identité
vient de la session ; le corps de commande ne permet pas de choisir un autre
commerce. Les restrictions existantes des comptes suspendus ou archivés restent
applicables. Les agents habilités saisissent et corrigent les mêmes informations
dans l’ERP, le backoffice et Onboard, dans leur périmètre territorial.

Les modifications passent par le même contrôle du domaine. Une adresse renseignée
ne peut pas être remplacée par une adresse incomplète. La version du référentiel
protège les mises à jour concurrentes : un conflit exige une relecture, sans
écrasement silencieux. Une réponse réseau perdue n’est pas une confirmation ;
l’interface relit l’adresse avant de proposer une nouvelle écriture.

Le profil expose `adresse_postale` et `version_referentiel`. La modification
commerçante utilise `PATCH /protected/referencement/commercants/me/adresse-postale`
avec `{adresse_postale, version_referentiel}`. Les contrats sont produits par le
générateur backend puis synchronisés auprès des consommateurs.

## 4. Onboard

L’adresse est saisissable à la création et à l’édition du commerce depuis Onboard.
Le contrôle `POSTAL_ADDRESS_COMPLETE` est requis, indépendant des recommandations
catalogue. Sans adresse complète et valide, le dossier ne peut pas être validé,
y compris lors d’une revalidation. Une clôture relit également l’adresse du
commerce : une validation historique ne contourne pas une adresse devenue absente.
Cette règle s’applique côté serveur et ne
dépend pas d’un bouton désactivé. Les données historiques ne sont pas enrichies
artificiellement ; les adresses manquantes sont explicitement signalées.

Cette demande n’étend pas implicitement les conditions d’activation commerciale
hors onboarding et ne révoque pas en masse les sessions ou comptes déjà actifs.

## 5. Animation et snapshots

Pour une nouvelle demande ou révision, le client transmet les références des
commerçants et les faits utiles à la mission. Le serveur résout le nom et l’adresse
depuis la fiche autorisée. Une adresse commerçante fournie par le client ne peut
pas remplacer cette source. Le formulaire Animation affiche l’adresse en lecture
seule ; si elle manque, il invite à compléter la fiche et la génération est
refusée. Les POI conservent leur propre adresse.

Le prompt conserve une photographie riche des lieux, comprenant l’adresse texte
issue de la fiche. Elle reste nécessaire au LLM et à la relecture du parcours.
Les prompts, résultats et définitions déjà publiés ne sont pas réécrits lorsqu’un
commerce change d’adresse. Les contrôles de dépendances/version détectent une
modification du référentiel pendant une génération en attente. Réviser une demande
ou réutiliser un modèle recharge les adresses actuelles des commerces autorisés.
Le schéma de réponse créative du LLM ne change pas ; seuls les contrats de demande
et les projections enrichies sont adaptés. Les snapshots historiques restent lisibles.

Cette règle remplace la saisie organisateur des adresses commerçantes de T2-D04
dans la [conception du moteur](../moteur-animation/conception-technique.md).

## 6. Livraison et vérification

Migration additive `v247` du backend, puis déploiement du backend avant les
frontends consommateurs. Aucun remplissage ou validation automatique des adresses
existantes. Onboard et ERP sont livrés par le dépôt backend. Les quatre dépôts
applicatifs gardent leurs historiques ; le dépôt central porte cette spécification.
La livraison comporte un commit par dépôt modifié.

Les preuves couvrent : normalisation et refus métier, persistance, droits de
modification, conflit de version, blocage de validation Onboard, origine serveur
des adresses du prompt, conservation des snapshots, interfaces mobile/bureau et
synchronisation des contrats. Le [bilan d’exécution](../moteur-animation/suivi-implementation.md#évolution-transverse--adresse-postale-du-commerce-20-septembre-2026)
détaille les commandes, résultats et limites. La migration a été vérifiée sur
une base PostgreSQL jetable ; elle n’a pas été appliquée à un environnement distant.
