# Localeo V53 - Observabilité et logs applicatifs

Cette version ajoute des logs applicatifs orientés traçabilité et performance.

## Ajouts
- `app/observability.py`
- instrumentation des use cases principaux
- logs de timing dans les repositories, notamment commerçants
- logs d'invariants métier
- logs de décisions métier

## Exemples de traces
- début / fin d'un use case
- temps par couche (use case/repository/sérialisation)
- invariants validés ou invalidés
- filtres appliqués
- décisions prises par les algorithmes
