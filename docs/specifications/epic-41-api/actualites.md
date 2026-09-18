# Epic 41 - Actualites rattachees aux animations

## Specifications applicatives

- [Localeo Animation - Creation et pilotage editorial](actualites-interface-animation.md)
- [Localeo Live - Feed, consultation et notifications](actualites-localeo-live.md)

Le present document reste la specification transverse des regles metier, des contrats et de la persistance partages entre les deux applications.

## État documentaire

Le [bilan du 23 août 2026](actualites-interface-animation.md) documente l’implémentation backend/back-office avec `v176`. La [roadmap EPIC 41](../../roadmap/terminees/epic-41-plateforme-animation-locale-mvp-backlog.md) porte le statut terminé. Les absences décrites dans le contexte initial ci-dessous expliquent l’origine du besoin ; elles ne décrivent pas le code actuel.

## Contexte initial, avant l’implémentation

Au moment du cadrage, le backend savait gerer des actualites editoriales generiques `ACTUALITE_EDITORIALE`, les publier dans `activites_locales` et produire des notifications Localeo Live. En revanche :

- aucune relation metier ne relie une actualite a une animation ;
- Localeo Animation ne permet pas de creer ou gerer les actualites d'une fiche animation ;
- le filtre `Animations` du fil `En direct` ne peut pas distinguer une actualite d'animation ;
- le deep link et la notification ne portent pas de contexte Animation garanti.

Ce constat initial motivait l’évolution du socle éditorial existant. Les règles et contrats qui suivent constituent la spécification du besoin, enrichie par les arbitrages validés.

## Objectif fonctionnel

Un gestionnaire habilite peut preparer, programmer, publier, modifier et masquer les actualites d'une animation depuis Localeo Animation. Une actualite publiee apparait dans Localeo Live, onglet `En direct`, filtre `Animations`, et produit une notification lorsque la categorie `ANIMATION` est activee sur l'installation cible.

## Etat des arbitrages

- `ARB-64` est valide : reutilisation de `activites_locales`, rattachement relationnel a l'animation, gestion depuis Localeo Animation, projection sous `En direct > Animations` et categorie Live `ANIMATION`.
- `ARB-65` a `ARB-69` sont valides sans amendement : audience, semantique inbox/WebPush, deep link configurable, permission et statuts autorisant la publication.
- Les regles correspondantes ci-dessous sont normatives pour l'implementation.

## Choix de conception

- Reutiliser `activites_locales`, ses statuts editoriaux et son batch de diffusion ; ne pas creer un second moteur de news dans `animation_locale`.
- Ajouter `animation_id` nullable avec cle etrangere vers `animations(id)` dans `activites_locales`.
- Utiliser le type canonique `ACTUALITE_ANIMATION` pour le feed et la cle de deduplication des notifications.
- Conserver la gestion partenaire sous les routes `animation_locale`; l'application delegue l'ecriture a un port du domaine `exploitation`.
- Heriter obligatoirement la ville de l'animation. Le gestionnaire ne choisit pas un autre scope territorial.
- Classer `ACTUALITE_ANIMATION` dans le filtre fonctionnel `ANIMATION` du feed et dans la preference de notification Localeo Live `ANIMATION`.
- Utiliser `LOCALEO_FRONT_LIVE_ANIMATION_URL_TEMPLATE`, contenant `{animation_id}`, sans reutiliser le template d'ajout d'une participation (`ARB-67`). Un lien vers le detail de l'actualite pourra le remplacer lorsque cet ecran existe.

## Parcours Localeo Animation

La fiche animation comporte un onglet `Actualites` avec :

- liste antichronologique et filtres par statut ;
- creation d'un brouillon avec titre, description, visuel optionnel, date de publication et date d'expiration optionnelle ;
- apercu du rendu Localeo Live ;
- programmation ou publication immediate ;
- modification tant que l'actualite n'est pas expiree ;
- masquage d'une actualite publiee ;
- suppression physique limitee aux brouillons ;
- affichage du statut de diffusion et du nombre de notifications creees/envoyees/en erreur.

Le rattachement a l'animation est fixe par le contexte de la fiche et ne peut pas etre change apres creation.

## Cycle de vie et regles

Les statuts restent `BROUILLON`, `PROGRAMMEE`, `PUBLIEE`, `MASQUEE`, `EXPIREE`.

- Une actualite peut etre preparee pour toute animation non archivee, mais elle ne peut pas etre publiee avant l'animation (`ARB-69`).
- La publication et la programmation executable exigent une animation `PUBLIEE`, `EN_COURS` ou `CLOTUREE` et non archivee (`ARB-69`).
- Une actualite programmee dont l'animation est archivee ou dans un statut incompatible a la date d'execution n'est pas diffusee et expose une erreur actionnable `409` (`ARB-69`).
- La ville, le nom et le lien public de l'animation sont resolves cote serveur ; ils ne sont jamais acceptes comme source de verite depuis le client.
- Le droit dedie est `animation:gerer_actualites`, toujours controle avec le tenant de l'animation. Sa reprise sur les habilitations existantes exige la presence conjointe de `animation:modifier` et `animation:publier` (`ARB-68`).
- La creation, modification, programmation, publication, masquage et suppression sont auditees.
- Une actualite publiee n'est pas supprimee physiquement ; elle est masquee afin de conserver l'audit et les preuves de diffusion.

## Contrats API partenaire

| Methode et route | Usage | Reponse principale |
| --- | --- | --- |
| `GET /protected/animation-locale/animations/{animation_id}/actualites` | Lister les actualites de l'animation avec pagination et filtre de statut. | `ActualiteAnimationListResponse` |
| `POST /protected/animation-locale/animations/{animation_id}/actualites` | Creer un brouillon rattache a l'animation. | `201 ActualiteAnimationResponse` |
| `GET /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}` | Consulter le detail et l'etat de diffusion. | `ActualiteAnimationResponse` |
| `PATCH /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}` | Modifier le contenu ou la programmation autorisee. | `ActualiteAnimationResponse` |
| `POST /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}/publier` | Publier immediatement de facon idempotente. | `ActualiteAnimationResponse` |
| `POST /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}/masquer` | Retirer du feed sans suppression de l'historique. | `ActualiteAnimationResponse` |
| `DELETE /protected/animation-locale/animations/{animation_id}/actualites/{actualite_id}` | Supprimer uniquement un brouillon. | `204` |

Les commandes acceptent `Idempotency-Key` lorsque leur repetition peut creer un effet de diffusion. Les erreurs couvrent `403` permission insuffisante, `404` ressource hors tenant ou inconnue et `409` transition editoriale ou statut Animation incompatible.

## Projection publique Localeo Live

`ActiviteLocalePayload` evolue avec une reference Animation optionnelle :

- `animation.id` ;
- `animation.nom` ;
- `animation.statut` ;
- `animation.commune` ;
- `cta_url` ou deep link calcule.

Le filtre `type_activite=ANIMATION` retourne `ANIMATION_PUBLIEE` et `ACTUALITE_ANIMATION`. Le filtre `NEWS` continue de ne retourner que les publications editoriales generiques.

## Notifications Localeo Live

A la premiere publication effective (`ARB-65`, `ARB-66`) :

1. le batch cree une notification inbox idempotente avec la cle `ACTUALITE_ANIMATION:{actualite_id}` ;
2. la categorie est `ANIMATION` ;
3. les installations dont la categorie `ANIMATION` est desactivee sont exclues ;
4. les installations sont ciblees si elles suivent la ville de l'animation ou une participation a cette animation ;
5. le WebPush n'est tente que pour un abonnement actif ; l'inbox reste consultable selon les preferences de l'installation ;
6. le payload ne contient aucune donnee participant et ouvre le deep link Animation ;
7. les reprises techniques ne creent jamais une seconde notification fonctionnelle.

Le masquage retire l'actualite du feed mais ne supprime pas retroactivement une notification deja remise.

## Persistance et index

- migration additive de `activites_locales.animation_id UUID NULL REFERENCES animations(id)` ;
- index `idx_activites_locales_animation_publication(animation_id, niveau_visibilite, date_publication)` ;
- contrainte applicative : `animation_id` obligatoire lorsque `type_activite = 'ACTUALITE_ANIMATION'` ;
- unicite de diffusion conservee par `type_activite + source_type + source_id` ;
- aucune duplication du nom, de la commune ou du statut de l'animation dans une nouvelle table d'actualites.

## Criteres de recette

- un gestionnaire ne voit et ne gere que les actualites des animations de ses tenants ;
- une actualite en brouillon n'apparait ni dans le feed ni dans l'inbox ;
- une actualite publiee apparait dans `En direct > Animations` avec le bon nom, la bonne commune et le bon deep link ;
- elle n'apparait pas sous `News` sauf choix frontend explicite d'un filtre global `Tout` ;
- une installation avec `ANIMATION=false` ne recoit aucune notification ;
- deux executions du batch ne creent qu'une notification par installation et actualite ;
- une actualite d'une animation non publiee ne peut pas etre rendue publique ;
- le masquage retire la publication du feed sans effacer son audit ;
- les contrats OpenAPI exposent tous les objets de requete et de reponse sans modele ORM.
