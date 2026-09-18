# Epic 49 - Registre des arbitrages

## Mode d'emploi

La colonne `Validation ou amendement` porte la decision produit. Au 23 aout 2026, tous les arbitrages de l'Epic 49 sont valides.

| ID | Arbitrage a rendre | Detail et impact | Priorite | Proposition de reponse | Validation ou amendement |
| --- | --- | --- | --- | --- | --- |
| MKTANIM-ARB-01 | Statuts d'abonnement autorisant la visibilite | L'abonnement reel est rattache au couple `(partenaire_id, commune_id)`. `EN_GRACE` est aujourd'hui accepte par plusieurs controles metier, mais le backlog parle d'abonnement actif. | P0 | Seul `ACTIF`, dans sa periode de validite, autorise la visibilite ; exclure `EN_GRACE`, `ABSENT`, `NON_DEMARRE`, `EXPIRE` et `SUSPENDU`. | Valide avec amendement : uniquement `ACTIF`. |
| MKTANIM-ARB-02 | Expiration pendant une animation | Un retrait public immediat peut casser la decouverte, mais l'acces participant doit rester possible pour honorer une inscription existante. | P0 | Retirer immediatement l'animation des routes publiques de decouverte et de detail ; conserver les routes tokenisees du participant et les operations de continuite. | Valide. |
| MKTANIM-ARB-03 | Definition d'une commune publiable | Le modele ORM historique se nomme `VilleOrm` et le payload animation retourne actuellement `active: true` en dur. Il s'agit pourtant du meme concept metier. | P0 | Utiliser `commune` comme terme metier et API canonique. `commune_id` reference l'unique table historique `villes`, sur laquelle est porte l'etat de publication Marketplace ; aucune entite ou table `communes` distincte n'est creee. | Valide avec amendement : commune et ville designent le meme referentiel. |
| MKTANIM-ARB-04 | Horizon des animations futures | Sans borne, une animation publiee tres en avance pollue le catalogue et les compteurs. | P0 | Exposer les animations commencant dans les 90 prochains jours ; rendre cette valeur configurable cote backend avec un defaut de 90 jours. | Valide. |
| MKTANIM-ARB-05 | Source du visuel officiel | `asset_ids` ne designe pas explicitement un visuel principal et l'apercu du flyer est actuellement protege. | P0 | Ajouter `visuel_principal_asset_id` a la configuration, servir un URL public controle ; utiliser ensuite l'apercu flyer, puis un bloc typographique sans image. | Valide. |
| MKTANIM-ARB-06 | Compatibilite avec Localeo Live | Localeo Live consomme deja la liste, le detail et le parametre `limit`. Une rupture imposerait une livraison simultanee. | P0 | Faire une evolution additive, conserver `limit` comme alias deprecie pendant la migration et ne retirer aucun champ existant avant mise a jour des consommateurs. | Valide. |
| MKTANIM-ARB-07 | Pagination publique | La liste actuelle charge tout en memoire et son `count` est ambigu. | P0 | Adopter un curseur stable avec `page_size` borne a 50 ; conserver `count` comme nombre d'items retournes et ajouter `pagination.total` et `pagination.next_cursor`. | Valide. |
| MKTANIM-ARB-08 | Sens du lien coffret-animation | Le modele actuel ne connait que les coffrets presents dans `configuration.lots`. Une simple eligibilite territoriale ne prouve pas le lien. | P1 | N'exposer que les coffrets de la version publiee des `lots`, avec la nature publique `LOT_A_GAGNER`. Le paiement reste implicite car il conditionne deja la publication. | Valide. |
| MKTANIM-ARB-09 | Cache public | Un cache applicatif impose une invalidation sur publication, annulation, expiration et abonnement. | P1 | Commencer par `Cache-Control: public, max-age=60, stale-while-revalidate=300`, sans cache serveur ; reevaluer apres mesure de charge. | Valide. |
| MKTANIM-ARB-10 | Activation progressive | Les nouvelles surfaces peuvent modifier fortement l'accueil et doivent pouvoir etre desactivees sans couper l'API utilisee par Live. | P1 | Ajouter le flag runtime Marketplace `LOCALEO_FEATURE_MARKETPLACE_ANIMATIONS_ENABLED`; laisser les contrats backend publics disponibles. | Valide. |
| MKTANIM-ARB-11 | Analytics et consentement | Les impressions et clics sont utiles, mais aucun identifiant ou token personnel ne doit etre collecte. | P1 | Reutiliser le service analytics et son consentement existants ; limiter les proprietes a `animation_id`, `commune_id`, surface et action. | Valide. |
| MKTANIM-ARB-12 | Portee de la synthese d'accueil | L'accueil peut representer tout le reseau ou la commune memorisee, ce qui change les chiffres affiches. | P1 | Afficher la synthese de la commune selectionnee lorsqu'elle existe, sinon la synthese globale ; annoncer explicitement le perimetre dans le libelle. | Valide. |
| MKTANIM-ARB-13 | Niveau SEO du MVP | La Marketplace est une SPA : les metadonnees injectees dans le navigateur ne garantissent pas les apercus des robots sociaux. | P1 | Livrer titre, canonique et JSON-LD `Event` cote client au MVP ; traiter pre-rendu ou SSR dans une evolution distincte si l'indexation serveur est obligatoire. | Valide. |

## Points non soumis a arbitrage

- `commune` et `ville` designent le meme referentiel ; `commune` est le terme metier canonique et la table historique reste `villes` ;
- aucune table `communes` distincte de `villes` ;
- aucune PII participant dans les projections publiques ou les analytics ;
- aucun calcul d'eligibilite dans React ;
- aucune exposition brute de `configuration.regles` sans liste blanche ;
- aucun appel detail par ligne dans la liste publique ;
- `404` pour une animation inexistante ou non eligible afin de ne pas reveler son existence.
