# Epic 54 - Calendrier de l'Avent local

> Suivi produit au 18 septembre 2026 : **À faire** — [backlog de référence](../../roadmap/a-faire/epic-54-calendrier-avent-local-backlog.md). Les bilans techniques datés ci-dessous conservent leur portée historique.

## Etat

`A developper`. Le cadrage est initialise ; les arbitrages et la conception
technique doivent etre finalises avant l'implementation.

## Objet

Cette Epic ajoute une animation saisonniere composee de plusieurs cycles quotidiens. Chaque case met en avant un commercant, collecte ses propres participations et attribue son propre coffret.

Le calendrier reste une seule animation. Les journees ne doivent pas etre materialisees par 12 ou 24 animations independantes.

## Documents

- [Backlog](../../roadmap/a-faire/epic-54-calendrier-avent-local-backlog.md)
- [Registre des arbitrages](registre-arbitrages.md)

## Concept metier a introduire

Une entite generique `MancheAnimation` est recommandee pour porter :

- l'animation parente ;
- son ordre et sa periode d'ouverture ;
- son contenu public et ses commercants ;
- ses lots reserves ;
- sa population eligible ;
- son tirage, ses gains et son statut.

Le nom technique doit rester generique afin de servir ulterieurement d'autres animations a tirages repetes.

## Cycle d'une journee

```text
PROGRAMMEE -> OUVERTE -> CLOTUREE -> TIREE -> GAINS_ENVOYES
```

Chaque transition automatique doit etre idempotente, auditee et relancable manuellement depuis Localeo Animation ou le Backoffice selon les droits.

## Frontieres de responsabilite

- le Backoffice et le backend portent le moteur de manches, les batchs et la supervision ;
- Localeo Animation configure et pilote le calendrier ;
- la Marketplace assure sa visibilite publique et la mise en avant du jour ;
- Localeo Live fournit l'experience calendrier et participant ;
- l'application commercant produit les validations quotidiennes.

## Reutilisation

Inscriptions, QR participants, commercants, coffrets, commandes de lots, notifications, audit et bilans de l'Epic 41 doivent etre etendus, et non dupliques. La principale rupture fonctionnelle est le passage d'un tirage global unique a plusieurs tirages scopes par manche.

## Points a concevoir ensuite

- schema de persistance des manches et rattachement des validations ;
- strategie de reservation des lots par jour ;
- orchestration APScheduler et reprise des traitements manques ;
- projection publique masquant les cases futures ;
- volumetrie des notifications et preferences participant ;
- bilan agrege et comparaison des journees.

[Retour à l’index des spécifications](../INDEX.md)
