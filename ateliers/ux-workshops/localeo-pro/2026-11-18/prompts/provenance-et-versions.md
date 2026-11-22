# Provenance et versions des instructions

**Suite du 18 novembre 2026 :** les mentions de décisions en attente dans ce relevé décrivent l'archivage initial. La décision ultérieure est consignée dans le [registre](../validation/decisions.md).

18 novembre 2026. Version documentaire de la suite : **LOCALEO-PRO-UX-1.0**. Cet identifiant est attribué à l’archivage, sans prétendre qu’il figurait dans les instructions initiales. Il désigne les étapes 1 à 5 archivées ; le prompt de relance est une nouvelle instruction proposée pour l’avenir, pas une instruction déjà exécutée.

| Fichier | Source et complétude | Évolution documentée |
| --- | --- | --- |
| [00-protocole-global.md](00-protocole-global.md) | Instruction complète utilisateur de l’étape 1 disponible dans la conversation ; login et mot de passe remplacés par `[CONFIDENTIEL]`. Une note éditoriale identifie la transcription. | Contenu métier conservé ; expurgation volontaire et obligatoire des deux secrets. |
| [01-exploration.md](01-exploration.md) | L’instruction globale de l’étape 1 était celle appliquée à l’exploration ; elle est désormais reproduite intégralement dans 01. **Aucun second prompt utilisateur distinct 01 n’a été fourni.** | Le fichier initial était un protocole d’exécution résumé. Ses octets sont conservés dans [01-exploration-initial.txt](historique/01-exploration-initial.txt). Ajout d’une notice et du texte utilisateur connu, sans inventer un prompt autonome historique. |
| [02-workshop.md](02-workshop.md) | Prompt complet provenant de la pièce jointe utilisateur `Pasted text.txt`. | Copie identique contrôlée à l’étape 2, à nouveau confrontée à la pièce jointe à l’archivage. SHA-256 attendu : `c496604b58d5c236cb6bbc613b9dd0393e64ef22f70259ea1abcd83c5a24dc1e`. |
| [03-maquettes.md](03-maquettes.md) | Instruction complète utilisateur de l’étape 3, transcrite depuis la conversation. | Remplace le simple emplacement réservé de l’étape 1. Aucune modification des règles de périmètre ou de vote. |
| [04-validation.md](04-validation.md) | Instruction complète utilisateur de l’étape 4, transcrite depuis la conversation. | Remplace l’emplacement réservé. Le registre reste en attente, car aucune décision n’a suivi. |
| [05-archivage.md](05-archivage.md) | Instruction complète utilisateur de l’étape 5, transcrite depuis la conversation. | Remplace l’emplacement réservé lors de cette étape ; archivage demandé sans validation implicite des orientations. |
| [RELANCER-WORKSHOP.md](RELANCER-WORKSHOP.md) | Nouveau prompt autonome conçu à l’étape 5 pour une future exécution. | Version 1.0 ; non exécuté dans ce workshop. |

## Adaptations d’exécution, sans réécriture des demandes

- L’adresse fournie à l’étape 1 menait au portail gestionnaire Animation. Après vérification documentaire, l’exploration a utilisé le portail Pro de test avec le seul compte fourni. La demande originale conserve son URL ; le README et les preuves documentent l’écart.
- Caméra physique, QR valide, reçu/doublon, kit téléchargé et retour différé non testés : ces limites ne sont pas masquées par une modification rétroactive des instructions.
- L’étape 3 a retenu uniquement les cinq P1 adoptées. Les ajustements M01 à M08 n’ont pas modifié substantiellement leur orientation et sont conservés dans les arbitrages.
- L’étape 4 est préparée mais sans décisions utilisateur. L’étape 5 clôture l’archivage à cet état partiel.

## Limite de rejouabilité exacte

Les demandes utilisateur connues et le protocole d’exploration sont archivés ; **une transcription verbatim exhaustive de tous les prompts internes de délégation et de toutes les commandes interactives n’est pas disponible dans ces fichiers**. Les scripts de navigation/rendu temporaires ont été supprimés après leur exécution ; les scénarios, sources des maquettes et rapports de contrôle restent disponibles. Ne pas reconstruire ces éléments en les présentant comme un historique exact.

La relance vise une exploration et une analyse reproductibles avec preuves et versions nouvelles, pas la reproduction déterministe de votes fictifs ou de données de test qui peuvent avoir changé. Les empreintes du manifeste décrivent les fichiers archivés, pas leur qualité métier.
