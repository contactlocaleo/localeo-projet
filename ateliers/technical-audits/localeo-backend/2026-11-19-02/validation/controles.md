# Contrôles de l'exécution

Mesures : trois commandes du lanceur isolé, chacune 1 test réussi (9,72 s /7,30 s /2,54 s). Aucun échec/arrêt de mesure dans cette relance ; anciens échecs/arrêt conservés historiquement. Aucune recette HTTP/PostgreSQL, métier complète ou UI exécutée.

Documentation : sync_documentation.py --check-sources via py -3.14, sortie «151 documents verifies.», code0. Les nouveaux audits ne modifient aucune source exportée. Les contrôles de guides/liens/intégrité/confidentialité finaux sont consignés ci-dessous après exécution.

Les SHAs applicatifs et empreintes suivies sont comparés à la baseline, les anciennes archives et bruts à leurs empreintes initiales. Les scripts/harness/bruts de cette exécution sont dans le backend ignoré, pas transportés par Git documentaire. Aucun secret privé/dotenv lu. Une recherche de motifs expurgée est un contrôle ciblé, pas une certification exhaustive.

## Résultats documentaires et intégrité

- Contrôle général : 119 guides, 1 793 liens locaux, zéro erreur/avertissement ; guidance.json.
- Contrôle avec tous les Markdown de cette archive : 171 guides/documents, 1 851 liens, zéro erreur/avertissement ; guidance-audit.json. Les ancres, URLs externes et sens métier ne sont pas certifiés par ce contrôle.
- Inventaire des livrables : 42 requis présents, plus briefs, annexes de validation et preuves auxiliaires. Les six rapports principaux contiennent 2/4/2/3/3/3 constats, chacun au plus cinq.
- 101 fichiers de l'archive précédente conservés à l'identique, aucun ajout dans l'ancien dossier ; ancien manifeste interne 99/99 conforme. Anciennes sources et 14 artefacts de mesure inchangés ; les autres audits backend sont également comparés à leur baseline.
- Aucun fichier suivi modifié dans les cinq dépôts ; seuls nouveaux documents dans cette exécution et artefacts ignorés backend. L'atelier CRM non suivi préexistant n'a fait l'objet d'aucune écriture de l'audit.
- 167 références explicites avec chemin complet app/sql/src et numéro de ligne contrôlées. Premier passage : cinq fins de plage au-delà du fichier ; corrigées factuellement dans les rapports de cette nouvelle exécution, avec empreintes avant/après et substitutions dans rectifications-references.json. Le premier résultat défavorable reste dans verification-premier-passage.json ; le résultat final est dans verification-finale.json. Aucune conclusion source affaiblie. Les références abrégées sont relues manuellement, l'existence d'une ligne ne certifie pas son sens.
- Recherche ciblée expurgée des clés privées, jetons fournisseurs/GitHub/AWS, JWT et URLs avec identifiants : aucun motif détecté dans le nouveau dossier. Aucun secret en clair imprimé ; contrôle non exhaustif.

Les tests composants réussis n'attestent ni invariants complets, ni recette UI, ni capacité API. Les contrôles d'architecture/métier complets ne sont pas lancés pour cet audit sans modification de code. Aucun HTTP/PostgreSQL intégré exécuté faute de cible jetable explicitement désignée. Les choix utilisateur restent vides et aucun gain après correction n'est mesuré.

## Incidents et limites d'exécution

Le premier alias python a échoué avant création du dossier ; py -3.14 a ensuite servi sans installation. Première extraction d'inventaire rejetée pour codec mal nommé, puis 1 329 modules parsés sans erreur après correction du seul outil. Une transcription de messages et notes via PowerShell/Python a perdu des accents ; le registre exact UTF-8 et la pièce jointe octet pour octet sont conservés, les notes rectifiées. Deux appels d'édition de références sans contexte correspondant ont été refusés sans mutation ; les éditions réussies sont tracées. Ces incidents d'outillage ne sont pas des échecs applicatifs ou de benchmark.

Un spécialiste persistance a été interrompu après lecture accidentelle d'extraits historiques, puis remplacé en contexte neuf ; son analyse n'est pas retenue. La contre-expertise réelle est indépendante des anciennes archives, les votes sont simulés par l'orchestrateur.

Statut d'archivage : local uniquement. Le manifeste final exclut lui-même et son empreinte pour éviter la circularité. Bruts et outils ignorés backend restent une dépendance de rejouabilité hors archive Git, aucune sauvegarde externe ou signature revendiquée.
