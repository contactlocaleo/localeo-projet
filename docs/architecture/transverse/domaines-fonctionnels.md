# Domaines fonctionnels

## Intention

Le backend Localeo est organise autour de domaines fonctionnels visibles dans `app/domaine` et `app/application`.

La couche `app/infrastructure` reste transverse : elle porte les adaptateurs SQLAlchemy, SQLAdmin, Stripe, Brevo, stockage objet, email, SMS et autres integrations techniques.

## Domaines cibles

| Domaine | Responsabilite applicative |
| --- | --- |
| `referencement` | Villes, typologies, commercants, acces commercants metier et taxonomies. |
| `commercialisation` | Offre vendable, coffrets, prestations, configuration de type coffret. |
| `gestion_achats` | Achats Coffrets, paiements, remboursements, documents d'achat, instances de coffret et consultation post-achat. |
| `abonnements_plateforme` | Offres, souscriptions partenaire/commune, commandes et droits plateforme ; extensions E73 pour modules, quotas et remboursements de ces commandes. |
| `gestion_reversement` | Comptes bancaires commercants, mouvements, reversements, paiements et lots. |
| `exploitation` | Validation terrain, validations de secours, liens, activite locale, audit operationnel, sessions operationnelles et transactions. |
| `support` | Communications, notes, contacts, demandes de facturation, motifs de contact et traitement support. |
| `profils` | Profils commercants et surfaces publiques de presentation. |
| `dam` | Images et assets media. |
| `documentaire` | Documents, versions internes, publication et exposition documentaire. |
| `identite_acces` | Authentification, sessions, tokens, API keys, rate limit et autorisations. |
| `animation_locale` | Enveloppe du domaine animation locale, plateforme partenaire, inscriptions, tirages et suivi. |

## Regles de classement

- Un objet appartient au domaine qui porte sa regle metier principale.
- Un objet de securite ou d'acces reste dans `identite_acces`, meme s'il protege un parcours d'un autre domaine.
- Un document metier ou contractuel va dans `documentaire`; une image ou un asset visuel va dans `dam`.
- Les objets financiers d'un achat Coffrets restent dans `gestion_achats`. Les commandes de souscriptions/modules et leur disponible remboursable appartiennent a `abonnements_plateforme` ; ne pas les deplacer au seul motif qu'elles utilisent un paiement client. Les adaptateurs de paiement et le circuit documentaire financier peuvent etre reutilises sans partager leurs modeles ORM entre domaines. Voir la [frontiere E73](../../specifications/epic-73-animation-et-ou-coffrets/architecture-contrats.md) pour la conception cible, distincte de sa livraison.
- Les objets financiers lies au paiement commercant restent dans `gestion_reversement`.
- Les vues globales de pilotage peuvent rester transverses, mais leurs vues specialisees doivent etre rattachees a leur domaine.

## Frontieres

```mermaid
flowchart LR
    Front[API / Back-office / PWA] --> App[Use cases par domaine]
    App --> Dom[Domaine fonctionnel]
    App --> Infra[Infrastructure transverse]
    App --> Ports[Ports applicatifs]
    Infra -. implemente .-> Ports

    App --> REF[referencement]
    App --> COM[commercialisation]
    App --> ACH[gestion_achats]
    App --> ABO[abonnements_plateforme]
    App --> REV[gestion_reversement]
    App --> EXP[exploitation]
    App --> SUP[support]
    App --> ID[identite_acces]
    App --> DOC[documentaire]
    App --> DAM[dam]
    App --> ANI[animation_locale]
```

