# Limites de l'inventaire

Lecture statique du checkout local et de consommateurs ciblés, pas inventaire des services déployés. Aucun trafic, SLA ou incident de production observé. Six revues indépendantes ne constituent pas une preuve de saturation.

Les cinq SHAs et états Git initiaux sont conservés dans [baseline](../validation/baseline.json). Backend propre et identique à la référence 7049e7fafc76f9119924f1082a5ee7457a175d85 ; git cat-file confirme l'objet, git diff référence HEAD vide. La documentation contient déjà des travaux non suivis (ancien audit et atelier CRM) préservés. Les observations nouvellement documentées ne sont donc pas des régressions introduites depuis la référence.

Les sorties brutes et outils d'audit restent ignorés dans le backend. L'archive documentaire contient protocoles, résultats synthétisés et empreintes, pas les données de travail. Leur disponibilité future hors Git reste une dépendance de rejouabilité.
