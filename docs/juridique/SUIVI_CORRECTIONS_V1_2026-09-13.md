# Corrections du corpus juridique V1 — 13 septembre 2026

Les quatre PDF ci-dessous ont été remplacés directement dans `docs/juridique/V1`. Leurs noms de fichiers sont conservés ; le document, ses métadonnées et son pied de page portent la **version 1.1 du 13 septembre 2026**. Les douze autres PDF sont inchangés. Le corpus contient toujours seize documents, désormais sur soixante-dix pages.

Ce suivi complète la [revue initiale](REVUE_FINALE_V1_2026-09-13.md). Il distingue les corrections réalisées des actions qui demandent encore des preuves fournisseurs ou une évolution des applications. Il ne constitue pas une attestation de conformité globale.

## Documents corrigés

| Document | Modification | Pages |
|---|---|---:|
| [Annexe C — Gestion des flux financiers](<interne/Annexe C - Gestion des Flux financiers Localeo - V1.pdf>) | Statut de procédure interne explicite. Renvoi obsolète à l'Annexe D remplacé par l'article 7 du contrat commerçant et sa fiche intégrée. Distinction entre paiement réservant les lots Animation et activation lors de leur mise à disposition au gagnant. | 4 |
| [CGV Marketplace](<marketplace/LOCALEO - Conditions Générales de Vente Marketplace - V1.pdf>) | Article 11 : qualification explicite des coffrets SOLO et MULTI en **bons à usages multiples (BUM)**. Distinction entre justificatif d'achat du bon, facture de la prestation du commerçant et opérations propres à Localeo, sans ventilation fiscale anticipée de la prestation. | 7 |
| [Conditions particulières Animation](<animation/LOCALEO - Conditions particulières Localeo Animation - V1.pdf>) | Article 9 : report des lots financés restant disponibles après clôture, sans remboursement automatique, avec conditions de disponibilité et récapitulatif accepté. Maintien des droits déjà acquis et des recours applicables. | 6 |
| [Politique de confidentialité](<communs/LOCALEO - Politique de Confidentialité - V1.pdf>) | Article 5 : engagements publics de Render, Stripe, Brevo et Scaleway identifiés et reliés à leurs sources ; chaîne WebPush distinguée. Les formulations attribuent ces engagements aux fournisseurs, sans affirmer que leur application aux comptes Localeo est vérifiée. | 6 |

Les tarifs Animation **Découverte : 390 € HT** et **Essentielle : 990 € HT** sont conservés. Le contrat commerçant fusionné avec sa fiche prestations et commissions n'a pas été modifié.

## Décision relative aux lots Animation

Décision donnée par le responsable Localeo : **« Report vers une autre animation, sans remboursement automatique »**.

La rédaction prévoit une demande à `contact@localeo.city`, pour une autre animation du même partenaire, après vérification des lots disponibles. Un lot ne peut pas être repris simplement parce qu'un courriel n'a pas été ouvert ou que le bénéficiaire ne l'a pas encore utilisé. Un lot attribué mais non envoyé exige une renonciation ou une décision conforme au règlement, respectant les suppléants et les délais annoncés. Un coffret activé conserve ses droits jusqu'à son échéance, sous réserve des restrictions légales ou de sécurité justifiées.

Le récapitulatif accepté du report précise les lots, quantités, valeur affectée, animation de destination et conditions de validité et d'utilisation. Le report des lots n'accorde pas automatiquement de nouveaux droits d'abonnement. Les remboursements prévus avant publication et les recours imposés par la loi ou une inexécution restent préservés.

**Action d'exploitation à organiser :** recevoir la demande, vérifier les droits des bénéficiaires et suppléants, établir le récapitulatif, obtenir son acceptation, puis tracer l'exécution du report. Aucune fonction automatique de transfert entre animations n'a été développée dans cette correction documentaire. Le règlement remis aux participants continue de régir leurs droits ; le report financier entre Localeo et l'organisateur ne peut pas les réduire.

## Confidentialité : dossier fournisseurs restant à constituer

Le responsable Localeo a confirmé ne pas disposer d'un dossier fournisseurs validé. Les annexes B et E constituent des supports de gouvernance ; les documents de travail et les exemples techniques ne prouvent pas les contrats, régions ou garanties effectivement applicables. L'enrichissement de l'article 5 **ne clôt donc pas la vérification des transferts internationaux**. Cette absence de dossier ne prouve pas, à elle seule, l'absence de contrat ni l'illicéité d'un transfert.

Les informations publiques ont été rapprochées des documents suivants : le [DPA Render](https://render.com/dpa), le [DPA Stripe](https://stripe.com/legal/dpa) et son [annexe sur les transferts](https://stripe.com/legal/dta), les informations Brevo sur le [stockage](https://help.brevo.com/hc/en-us/articles/360001005510-Data-storage-location) et l'[emplacement du DPA](https://help.brevo.com/hc/en-us/articles/15403782599570-Where-can-I-find-the-Data-Processing-Agreement-DPA), ainsi que le [DPA Scaleway](https://www-uploads.scaleway.com/DPA_EN_v17072024_0ca3d55b58.pdf) et sa [liste de sous-traitants](https://www.scaleway.com/en/subprocessorlist/). Ces sources décrivent les engagements généraux des fournisseurs, pas une validation des comptes Localeo.

| Fournisseur ou chaîne | Pièces et vérifications à réunir |
|---|---|
| Render | Entité contractante et DPA applicable daté ; régions réelles de l'application, de la base et des sauvegardes ; accès support et sous-traitants pertinents ; mécanisme de transfert et couverture de l'entité vérifiés. |
| Stripe | Pays du compte, entités et accords des services utilisés, notamment paiement/Connect ; DPA et annexe sur les transferts applicables ; destinataires et garanties effectives. Les entités des différents accords ne sont pas nécessairement identiques. |
| Brevo | Conditions acceptées et DPA correspondant ; entité contractante ; services et options réellement utilisés ; sous-traitants, pays d'accès et garanties. Un stockage annoncé dans l'UE ne suffit pas à exclure les accès internationaux. |
| Scaleway | Contrat du produit utilisé ; preuves des régions du stockage et des sauvegardes, classes de stockage ; sous-traitants et accès applicables. Une configuration d'exemple `fr-par` ne prouve pas le paramétrage déployé. |
| WebPush | Services de transport réellement rencontrés selon le navigateur/système ; conditions pertinentes, rôles, métadonnées, pays et garanties de chaque chaîne. Ne pas assimiler automatiquement WebPush à un contrat Firebase. |

Pour chaque ligne, conserver la source, sa version, la date de vérification, le résultat et le responsable. Si le mécanisme invoqué est le DPF, vérifier le statut actif de l'entité et son champ ; si ce sont les clauses contractuelles types, identifier les clauses et modules réellement applicables et les vérifications nécessaires. Le DPA encadre la sous-traitance et ne remplace pas, à lui seul, le mécanisme requis pour un transfert. Voir le [cadre des transferts expliqué par la CNIL](https://www.cnil.fr/fr/transferts-de-donnees-hors-ue-le-cadre-general-prevu-par-le-rgpd).

Une fois ce dossier rapproché des usages réels, finaliser l'information publique par destinataire, finalité, pays et garantie applicable, avec un moyen d'obtenir les garanties. Compléter alors la notice Live si les informations propres aux notifications le nécessitent. Les identifiants de compte, secrets, noms de buckets et URL d'abonnement WebPush restent hors des documents publics.

## Sources éditables et contrôle

Les quatre sources Word corrigées sont conservées dans [`output/docx/v1.1`](../../livrables/juridique/v1.1), avec un [manifeste des modifications et empreintes SHA-256](../../livrables/juridique/v1.1/MANIFESTE_CORRECTIONS_V1_1.json). Les exports correspondants sont également disponibles dans [`output/pdf/v1.1`](publication/catalogue.json).

Les vingt-trois pages des documents modifiés ont été rendues et contrôlées visuellement. Le texte exporté a été comparé aux sources, les tarifs et marqueurs de révision vérifiés, ainsi que la disparition du renvoi à l'Annexe D. La politique contient ses liens fournisseurs cliquables. Le contrôle des empreintes confirme que les douze autres PDF V1 sont restés identiques.

## Diffusion et actions distinctes

Les CGV et la confidentialité sont synchronisées dans le dépôt local `localeo-marketplace` : nouveaux PDF sous `public/legal/v1.1/`, contenu HTML et métadonnées mis à jour pour `/cgv` et `/confidentialite`. Les huit PDF publics sous `public/legal/v1/` restent archivés à l'identique ; les six autres entrées documentaires n'ont pas changé. L'affichage des pages prend maintenant en charge les libellés de liens provenant des sources Word. Aucun déploiement n'a été effectué.

Validation Marketplace : compilation réussie, **2/2 tests Playwright « documents publics »** et **1/1 test serveur « public legal PDFs »** réussis. Le rapprochement des 82 fragments des CGV et des 104 fragments de la confidentialité entre HTML et PDF ne relève aucun texte manquant. Les modifications utilisateur dans les autres fonctionnalités sont préservées.

Le contrôle local en navigateur confirme les neuf hyperliens de confidentialité et l'accès aux huit anciennes URL PDF, avec leurs empreintes initiales.

Les autres actions de la revue restent à suivre : parcours de rétractation de l'[epic 64](../roadmap/a-faire/epic-64-parcours-retractation-en-ligne-backlog.md), preuve d'acceptation et remise du dossier contractuel, accessibilité effective, compléments B2B et RGPD commerçant selon les usages, puis simplification éventuelle du réglage analytics tant qu'aucun service n'est actif. Les modifier ou les déclarer achevées nécessiterait un travail distinct des quatre corrections de texte ci-dessus.
