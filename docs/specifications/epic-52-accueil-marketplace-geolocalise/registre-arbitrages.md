# Epic 52 - Registre des arbitrages

## Mode d'emploi

Le registre contient uniquement les decisions necessaires pour commencer la conception. La colonne `Proposition simple` fournit la solution initiale la moins complexe ; la derniere colonne reste a valider ou amender.

| ID | Point a arbitrer | Explication detaillee | Priorite | Proposition simple | Validation ou amendement |
| --- | --- | --- | --- | --- | --- |
| GEO-ARB-01 | Declenchement de la demande | Une demande native affichee sans contexte est souvent refusee et peut degrader la premiere visite. | P0 | Proposer `Autour de moi` par defaut, expliquer son usage, puis tenter la geolocalisation apres acceptation ; reutiliser ensuite l'autorisation navigateur disponible. | Valide. |
| GEO-ARB-02 | Rayon de proximite | Un rayon trop faible produit souvent un resultat vide ; un rayon trop large dilue la notion de local. | P0 | Defaut de `30 km`, configurable cote backend, maximum initial de `100 km`. | Valide et implemente. |
| GEO-ARB-03 | Contenu du resultat | Retourner toutes les communes connues peut proposer un territoire indisponible ou vide. | P0 | Retourner uniquement les communes avec `publiee_marketplace=true` et coordonnees completes ; traiter la presence de contenu comme filtre P1. | Valide et implemente sans filtre de contenu au MVP. |
| GEO-ARB-04 | Presentation multi-communes | Limiter l'accueil a la commune la plus proche ou a la seule ville choisie ignorerait les offres pertinentes des communes voisines. | P0 | Agreger les contenus de toutes les communes publiees du rayon, que son origine soit la position du visiteur ou les coordonnees de la ville choisie. | Valide. |
| GEO-ARB-05 | Stockage de la preference | Redemander le mode ou la ville a chaque visite est intrusif ; stocker la position exacte serait disproportionne. | P0 | Stocker dans le navigateur `{mode: AUTOUR_DE_MOI | VILLE_PREFEREE | AUCUNE, ville_id?}` sans coordonnees, jusqu'au changement explicite du choix ou a l'effacement du stockage local. | Valide ; implementation Marketplace restante. |
| GEO-ARB-06 | Source des coordonnees communales | Le modele historique ne possede pas de code INSEE et un code postal peut correspondre a plusieurs communes. Un appel externe dans le parcours public rendrait aussi l'accueil dependant d'un tiers. | P0 | Ajouter `code_insee`, utiliser le centre retourne par l'API Decoupage administratif `geo.api.gouv.fr`, faire confirmer les rapprochements historiques ambigus, puis conserver coordonnees, source et date localement. Autoriser une correction manuelle auditee. | Valide. |
| GEO-ARB-07 | Resultat vide ou refus | Le parcours ne doit pas devenir inutilisable lorsque la position est refusee, imprecise ou eloignee du reseau. | P0 | Proposer une ville de preference comme nouvelle origine du rayon, ou le mode `AUCUNE`, sans redemander l'autorisation en boucle. | Valide. |
| GEO-ARB-08 | Technologie de distance | PostGIS est puissant mais ajoute une dependance ; un calcul applicatif devient couteux avec un tres grand referentiel. | P1 | Utiliser Haversine pour le MVP ; reevaluer PostGIS apres mesure du volume et des performances. | Valide et implemente dans le domaine. |
| GEO-ARB-09 | Geolocalisation par IP | Elle evite la demande navigateur mais reste approximative et constitue un traitement supplementaire. | P1 | L'exclure du MVP ; ne jamais l'utiliser sans cadrage confidentialite distinct. | Valide, hors perimetre. |
| GEO-ARB-10 | Precision et conservation des requetes | Les coordonnees exactes peuvent identifier les habitudes ou le domicile d'un visiteur si elles sont conservees. | P0 | Calcul en memoire uniquement, aucun stockage ni log des valeurs, analytics limite a succes/refus/vide et commune finalement choisie. | Valide et implemente cote backend. |
| GEO-ARB-11 | Accueil sans contexte territorial | Les cinq widgets locaux n'ont pas de resultat pertinent sans territoire. | P0 | En mode `AUCUNE`, ne pas rendre `Coffret du moment`, `Communes disponibles`, `Les animations a vivre pres de chez vous`, `En ce moment` et `Derniers coffrets ajoutes` ; conserver l'acces au choix du mode ou de la ville. | Valide. |
| GEO-ARB-12 | Perimetre des widgets | Appliquer la preference a toute la Marketplace modifierait implicitement catalogues, recherche et pages de detail. | P0 | Limiter le contexte aux cinq widgets identifies sur la page d'accueil ; ne filtrer aucune autre page automatiquement. | Valide. |
| GEO-ARB-13 | Contrat multi-communes des widgets | Etendre tous les endpoints generiques introduirait un filtre dont les autres surfaces n'ont pas besoin. Effectuer un appel par commune multiplierait les requetes et produirait des tris divergents. | P0 | Creer une projection backend d'accueil dediee aux cinq widgets, alimentee par la liste de communes du rayon, avec tri et limites propres a chaque widget. | Valide et implemente. |
| GEO-ARB-14 | Transport de la position | Des coordonnees passees dans l'URL d'un `GET` peuvent apparaitre dans l'historique, les journaux de proxy ou les outils d'observabilite. | P0 | Utiliser `POST /public/referencement/villes/proches/rechercher` avec un corps JSON, sans cache partage et avec redaction explicite des donnees sensibles. | Valide et implemente. |
| GEO-ARB-15 | Origine du rayon | Implementer deux moteurs pour le GPS et la ville de preference produirait des ecarts de filtrage. | P0 | Un service unique accepte soit des coordonnees ponctuelles, soit un `commune_origine_id`, resout le point d'origine cote backend et retourne le meme contrat. | Valide. |
| GEO-ARB-16 | Moment de l'appel a l'API communale | Appeler `geo.api.gouv.fr` pendant une visite rendrait la Marketplace sensible a sa latence et a sa disponibilite. | P0 | Appeler la source uniquement depuis le Backoffice ou un batch borne ; tous les parcours publics utilisent les coordonnees stockees dans `villes`. | Valide. |
| GEO-ARB-17 | Mise a jour des coordonnees | Une synchronisation automatique pourrait ecraser une correction locale volontaire. | P1 | Rafraichissement manuel au MVP ; batch ulterieur par code INSEE, sans ecrasement silencieux des valeurs de source `SAISIE_MANUELLE`. | Valide pour le MVP. |

## Points non soumis a arbitrage

- la geolocalisation ne bloque jamais la Marketplace ;
- `commune` et `ville` restent un seul referentiel, stocke dans `villes` ;
- le backend determine la proximite et l'eligibilite ;
- la distance affichee est une distance a vol d'oiseau ;
- aucune carte ni API d'itineraire n'est necessaire au MVP ;
- les coordonnees de l'internaute ne sont pas integrees aux URLs partageables.
- une ville memorisee doit encore etre publiable lors de sa restauration ;
- les coordonnees exactes ne sont jamais memorisees, y compris en mode `AUTOUR_DE_MOI`.
- la ville selectionnee sert de centre au rayon ; elle n'en limite pas a elle seule le contenu.
