# Conception technique - Epic 58 Filtre annuel global

## 1. Contrat backend cible

### 1.1 Années disponibles

Ajouter un endpoint protégé, calculé dans le contexte de la commune active :

```http
GET /protected/animation-locale/animations/annees
```

Réponse proposée :

```json
{
  "items": [
    { "annee": 2026, "nombre_animations": 8 },
    { "annee": 2025, "nombre_animations": 12 }
  ],
  "annee_courante": 2026
}
```

L'année courante est toujours présente, même sans animation, afin de conserver
une valeur par défaut stable. Les autres années sans animation sont omises.

Une alternative acceptable consiste à fournir les mêmes informations dans une
facette d'un endpoint de contexte, à condition de ne pas obliger le frontend à
parcourir toutes les pages d'animations.

### 1.2 Paramètres temporels

Ajouter `date_debut` et `date_fin` aux collections qui ne les acceptent pas :

| Endpoint | Évolution |
| --- | --- |
| `/participants` | filtrer par période de l'animation associée |
| `/tirages` | filtrer par période de l'animation associée |
| `/flyers` | filtrer par période de l'animation associée |
| `/gains/coffrets/consommation` | filtrer par période de l'animation associée |

La sémantique commune est le chevauchement de période de l'animation. Les
paramètres ne filtrent pas sur la date d'inscription, de validation, de tirage,
de génération du flyer ou de consommation du gain.

Les endpoints déjà dotés de bornes temporelles doivent être vérifiés et alignés
sur cette même sémantique.

### 1.3 Pagination et agrégats

- le filtre est appliqué avant pagination ;
- `pagination.total` représente le total filtré ;
- les KPI et agrégats sont calculés sur l'ensemble filtré, jamais sur la page ;
- les index nécessaires couvrent les jointures animation/commune/période ;
- les réponses d'erreur conservent le `correlationId` canonique.

## 2. État global frontend

Créer un contexte annuel au niveau racine de l'application :

```ts
interface AnnualContext {
  year: number;
  availableYears: Array<{ year: number; animationCount: number }>;
  startDate: string;
  endDate: string;
  setYear(year: number): void;
}
```

Le sélecteur est rendu dans `TopBar`, à côté de la commune. `TopBar` ne porte
pas seul cet état : les vues doivent le consommer depuis le niveau `App` ou un
provider dédié.

## 3. Persistance et navigation

- valeur initiale : année civile courante ;
- URL canonique : paramètre `annee`, par exemple `?annee=2026` ;
- `localStorage` peut mémoriser le dernier choix comme fallback ;
- l'URL prime sur le stockage local lorsqu'elle contient une année valide ;
- les navigations internes conservent `annee` ;
- les liens profonds vers une animation restent valides sans contrôle bloquant
  de l'année.

Lors d'un changement de commune, la liste des années est rechargée. Si l'année
courante de sélection n'est plus disponible, le frontend sélectionne l'année
civile courante.

## 4. Combinaison avec les filtres locaux

Les filtres locaux sont intersectés avec les bornes annuelles.

- Tableau de bord : pour l'année courante, conserver la période courte par
  défaut ; pour une année passée, sélectionner toute l'année par défaut.
- Animations : les champs `Du/Au` restent dans les limites de l'année et ne
  peuvent pas élargir le contexte global.
- Filtres par animation : ne proposer que les animations de l'année.
- Changement d'année : réinitialiser les filtres locaux devenus invalides et
  revenir à la première page.

Une fonction centrale calcule l'intersection afin d'éviter des variantes entre
les vues.

## 5. Matrice frontend

| Vue | Application du contexte annuel |
| --- | --- |
| Dashboard | transmettre les bornes et adapter le filtre de période |
| Animations | transmettre les bornes et borner `Du/Au` |
| Participants | transmettre les bornes, recalculer KPI et options animation |
| Validations | transmettre les bornes |
| Tirages et gains | transmettre les bornes |
| Flyers | transmettre les bornes |
| Bilans | transmettre les bornes |
| Consommation des gains | transmettre les bornes |
| Détail animation | ignorer le filtre pour la lecture directe |
| Modèles, coffrets, abonnement, support | ne pas appliquer |
| Notifications | ne pas appliquer |

## 6. États d'interface

- chargement des années sans bloquer toute la barre supérieure ;
- année courante affichée même sans historique ;
- état vide contextualisé : `Aucune animation en 2025` ;
- libellé accessible du sélecteur : `Année des animations` ;
- compte d'animations optionnel dans les choix ;
- erreur de chargement : conserver l'année courante et permettre une relance.

## 7. Tests

### Backend

- animation incluse dans une seule année ;
- animation chevauchant deux années ;
- année sans animation ;
- isolation par commune et habilitation ;
- filtrage avant pagination et agrégats ;
- bornes et fuseau aux changements d'année ;
- non-régression des requêtes sans filtre.

### Frontend

- défaut sur l'année courante ;
- restauration URL et stockage local ;
- changement de commune avec année encore valide ou absente ;
- propagation à chaque vue concernée ;
- combinaison avec période Dashboard et `Du/Au` Animations ;
- conservation du contexte pendant la navigation ;
- ouverture d'une animation hors année ;
- absence d'effet sur les vues hors périmètre.
