# Contrôle de l’archive et anomalies

Préparation : 2026-11-19T07:43:58+01:00 (Europe/Paris). Exécution courante : `2026-11-18`, commencée le 18 et poursuivie le 19 novembre 2026.

## Inventaire demandé

| Livrable | État / preuve |
| --- | --- |
| Observations et couverture | Présentes : [constats](../observations/observations-factuelles.md), [couverture](../observations/couverture-pilotage-commercial.md), [limites](../observations/limitations.md). |
| Cartographie et écrans | Présents : [20 parcours](../observations/cartographie-parcours.md), [inventaire](../observations/inventaire-ecrans.md). Certains parcours restent partiels ou non vérifiés. |
| Captures AVANT | 15 PNG réels bureau ; aucun AVANT mobile exploitable. Empreintes de référence conservées. |
| Rapport exécutif | [Présent](../workshop/rapport-executif.md) ; conclusion de préparation GO SOUS CONDITIONS, pas validation d’un lancement. |
| Votes nominatifs | [Présents](../workshop/votes-et-arbitrages.md) : 12 profils fictifs nommés, 156 bulletins motivés sur 13 orientations ; sources JSON conservées. Aucun votant réel. |
| Backlog, rejets, quick wins | [Backlog](../workshop/backlog-ux.md), [3 rejets](../workshop/orientations-rejetees.md), [quick wins proposés](../workshop/quick-wins.md). |
| Maquettes et galerie | 12 scènes HTML, 24 PNG bureau/mobile, [galerie](../visuels/comparatif-avant-apres.html), sources et [arbitrages](../visuels/arbitrages-complementaires.md). |
| Décisions | [Registre présent](../validation/decisions.md), **cinq décisions manquantes** ; aucun accord explicite reçu. |
| Roadmap | [Créée en étape 5](roadmap-ux.md) ; aucun P0/P1 validé à planifier. |
| Plan de tests | [Créé en étape 5](plan-tests-utilisateurs.md), huit scénarios à conduire avec de vraies personnes ; aucune séance exécutée. |
| Prompts | [Provenance](provenance-prompts.md) : 01–05 complets, 00 seulement constat d’absence ; relance v1.0 créée pour le futur. |

## Anomalies et limites restantes

1. **Protocole global initial absent** : 00 ne contient pas d’instruction distincte, car aucune n’a été fournie. Historique non fabriqué.
2. **Validation utilisateur absente** : UX01–UX05 en attente. La roadmap n’intègre aucune P1 comme validée. La demande d’étape 5 ne change pas ce statut.
3. **Recette incomplète** : mobile, multi-compte, exhaustivité du pilotage, affectation et cycle complet du rendez-vous non établis ; livraison réelle des rappels non testée. [Risques R01–R08](../validation/risques-non-resolus.md).
4. **Anonymisation partielle des captures** : revue visuelle des 15 AVANT effectuée en étape 5 ; les captures 04, 05, 09, 14 et 15 montrent encore des noms de collaborateurs et/ou libellés d’activité. Les noms de structures restent également visibles. Les coordonnées des résultats Prospects sont masquées, mais cela ne constitue pas une anonymisation intégrale. Aucun identifiant de connexion visible relevé. Les originaux probants restent inchangés ; l’absence générale de données personnelles ou commercialement sensibles **n’est pas certifiée**. Cette réserve concerne aussi leurs reprises dans la galerie et ses captures de contrôle. Ne pas considérer l’archive comme un export public anonymisé.
5. **Objets fictifs encore dans TEST** : inventoriés dans les limitations, non supprimés pendant l’archivage.
6. **Traçabilité technique partielle** : version déployée inconnue ; modèles exacts et niveaux de raisonnement des étapes précédentes non établis. Les scripts temporaires de génération ne sont pas archivés ici ; les HTML/CSS/JS, fragments et PNG permettent de consulter les maquettes, sans promettre une régénération identique.

## Historique

Un seul répertoire d’exécution CRM est présent sous `docs/ux-workshops/localeo-crm/` : `2026-11-18`. Aucun workshop CRM précédent identifié dans ce périmètre ; la comparaison historique est **non applicable**. Aucun fichier `comparaison-precedent.md` factice n’est créé. Aucune correction produit n’est revendiquée ; les anciennes conclusions d’étape restent des états historiques datés.

Un [audit UX antérieur du 12 novembre 2026](../../../../../docs/audits/backend/localeo-crm-ux-productivite-2026-11-12.md) existe dans le dépôt. Il ne constitue pas un workshop à douze votes et ses captures ne sont pas archivées en PNG. Il reste une référence documentaire distincte, sans comparaison homogène des notes ou des décisions ni preuve de correction.

## Vérification finale

Le rapport machine `controle-final.json` consigne les contrôles effectués, leurs limites et l’état Git des applications. Le manifeste `manifest-integrite.json` décrit les tailles et SHA-256 des fichiers, en excluant uniquement son propre contenu. Les documents non modifiés des phases précédentes sont comparés à l’instantané de début d’étape 5 ; les captures AVANT et maquettes sont également comparées aux empreintes archivées.

Le contrôle textuel cherche les valeurs des identifiants fournis sans les afficher, valide les JSON, les liens locaux et les bulletins. Les PNG sont vérifiés pour leur structure et leurs données. Les rendus et interactions de galerie conservent les preuves d’étape 3 ; aucun nouveau test fonctionnel CRM n’est effectué. Une absence de correspondance textuelle avec les secrets ne prouve pas une anonymisation complète.

**Statut : archivage documentaire finalisé avec réserves ; workshop incomplet au regard du protocole global initial, de la validation utilisateur et des recettes restantes. Aucune implémentation ni modification applicative.**
