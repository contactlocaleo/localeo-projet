# Revue contradictoire des maquettes — simulation

18 novembre 2026 · cinq experts et sept commerçants fictifs. **Aucun entretien réel, aucune mesure de vitesse, aucune preuve de réduction d’erreur.** Les voix de l’étape 2 restent inchangées. Cette revue exprime des préférences de conception, pas une autorisation de développement.

## Méthode et limites

L’agent principal a inspecté les captures réelles et les rendus PNG de conception. Trois revues indépendantes ont repris les rôles du workshop : cinq experts, quatre commerçants, trois commerçants. Ces sous-agents ne disposaient pas des outils de lecture d’image : ils ont reçu une transcription du contenu et de la hiérarchie des maquettes, des constats AVANT et des limites. **Leurs réactions sont une revue de contenu, sans inspection visuelle autonome.** Elles ne sont pas présentées comme douze tests utilisateurs devant un navigateur.

La transcription couvrait : B1 erreur/reconnaissance/confirmation/succès/doublon/refus/incertitude ; C1 information et action après lecture ; D1 accueil et trois états de préparation ; E1 flyer, consignes, dates et deux QR ; F1 retour, session expirée et interruption avant confirmation. Le cadre visuel décrit conservait la charte, le scanner et les repères de navigation.

Les six questions posées à chaque rôle étaient : comprenez-vous mieux cet écran ? savez-vous immédiatement quoi faire ? cette version vous ferait-elle gagner du temps ? le risque d’erreur est-il réduit ? préférez-vous l’ancienne ou la nouvelle version ? qu’est-ce qui reste difficile ? Réponses condensées ci-dessous, toutes **SIMULÉES**. Les corrections retenues sont tracées dans les [arbitrages M01 à M08](arbitrages-maquettes.md).

## Les cinq experts fictifs

| Rôle | Compréhension | Geste immédiat | Temps potentiel | Risque d’erreur | Préférence | Difficulté restante |
| --- | --- | --- | --- | --- | --- | --- |
| UX senior | Reconnu, confirmé, doublon et incertain sont mieux distingués ; message et tâche aussi. | Rescanner, vérifier ou reprendre sont explicites. | Moins d’interprétation possible ; trop de statuts pourrait déplacer l’effort vers la lecture. | « Aucune validation » doit rester réservé à une absence certaine. | Après B1/C1 ; conditionnelle D1/E1/F1. | Hiérarchiser les états et expliquer le reçu. |
| Accessibilité | Les mots apportent du sens au-delà de la couleur. | Les intitulés indiquent généralement la conséquence. | Aucune conclusion clavier ou lecteur d’écran à partir du texte. | Focus ou alerte non annoncée pourrait faire manquer le résultat. | Après sous conditions pour les cinq. | Contrastes, cibles, ordre de lecture, accordéons et annonces réelles à tester. |
| Product Manager B2B | Téléchargement, préparation et validation ne sont plus assimilés. | Pertinent si fondé sur l’état autorisé. | Liens directs potentiellement utiles ; aucun gain chiffré. | Des libellés peuvent être pris pour de nouvelles obligations. | Après C1 ; conditionnelle B1/D1/E1/F1. | Vérifier capacités de reçu, période et règles de préparation. |
| Opérations terrain | Résultat et différence des QR plus faciles à expliquer. | Scanner conservé et participant suivant utiles en boutique. | Peut éviter des recherches, à mesurer pendant la file. | Résultat inconnu difficile à expliquer à l’habitant. | Après B1/C1/E1 ; conditionnelle D1/F1. | Que faire si la vérification n’aboutit pas ou si l’organisateur tarde ? |
| Researcher / facilitateur | Les propositions rendent les hypothèses testables. | La tâche permet de demander « que feriez-vous ? » sans souffler le chemin. | Impossible à estimer sur transcription. | Exemple de compteur et état fictif pourraient passer pour une correction prouvée. | Après sous conditions pour les cinq. | Comparaison sur tâches équivalentes, débutants, caméra physique et absence réelle. |

## Les sept commerçants fictifs

| Rôle | Compréhension | Geste immédiat | Temps potentiel | Risque d’erreur | Préférence | Difficulté restante |
| --- | --- | --- | --- | --- | --- | --- |
| Martine, fleuriste, 63 ans | « QR non reconnu » est plus clair que « pack » ; les deux QR deviennent distincts. | Demander le QR du client puis réessayer ; reprendre étape 2/4. | Chercherait probablement moins dans les messages. | « Aucune validation » rassure, mais doit être distingué du résultat inconnu. | Nouvelle, avec aide simple pour D1/E1/F1. | Version, attestation, saisie manuelle et fin à zéro heure. |
| Patrick, boulanger, 57 ans | Sait mieux si le passage est enregistré, déjà fait ou inconnu. | Scanner à nouveau, participant suivant, une seule action de préparation. | Scanner en premier utile ; confirmation toujours ressentie comme un coût. | Risque de s’arrêter avant le dernier bouton s’il est interrompu. | Nouvelle sous conditions ; désaccord sur la confirmation conservé. | Vérifier puis rescanner semble long, surtout avec une file. |
| Nadia, salon, 44 ans | Distingue information/tâche et accepté/prêt. | Reprendre la question ; savoir si l’accord permet l’installation. | Kit et dates pourraient faciliter l’anticipation. | Télécharger ne signifie plus que l’équipe est prête. | Nouvelle ; D1 sous condition de cohérence du prochain geste. | Ne pas afficher « installer » et « attendre accord » pour le même état. |
| Julien, restaurateur, 35 ans | Succès, doublon et inconnu sont plus exploitables. | Vérifier le résultat si l’opération peut réellement être retrouvée. | Hésitations potentiellement réduites ; dépend du serveur et du nombre d’étapes. | Pas de renvoi automatique utile seulement si garanti. | Nouvelle sous conditions techniques. | Résultat toujours inconnu ; écart des compteurs encore non diagnostiqué. |
| Claire, prêt-à-porter, 51 ans | Sait mieux quel QR demander et distingue information/demande. | Préparation de demain puis kit ; scanner devant une cliente. | Liens directs pourraient éviter plusieurs menus. | « 19–23 » peut laisser croire que tout le 23 est ouvert. | Nouvelle B1/C1/F1 ; D1/E1 conditionnelles. | Trop de statuts ; fin de période à rendre visible sans déplier. |
| Hugo, boutique spécialisée, 29 ans | Distingue code reconnu, validation, doublon et réponse inconnue. | Vérifier avant toute nouvelle tentative. | Repères conservés et PIN vide replié potentiellement plus rapides. | Vérification dangereuse si elle renvoie en réalité la validation. | Nouvelle C1 ; autres sous conditions de fonctionnement. | Issue d’une vérification impossible et identification du reçu. |
| Isabelle, libraire, 48 ans | Nom, date et prochaine action faciliteraient le retour. | Préparation, consignes pour collègue ; résultat avant reprise d’un scan. | Pourrait éviter une préparation répétée ou un appel à la commune. | Une tâche lue peut être oubliée dans le filtre non-lu. | Nouvelle B1/D1/E1 ; C1/F1 conditionnelles. | Après reconnexion, ne plus savoir si elle avait confirmé ou seulement scanné. |

## Préférences détaillées, sans nouveau scrutin

« Après sous conditions » exprime une préférence pour le contenu proposé ; cela ne valide ni son rendu accessible ni son comportement. Les réserves ne sont pas converties en voix POUR ou CONTRE.

| Rôle | B1 | C1 | D1 | E1 | F1 |
| --- | --- | --- | --- | --- | --- |
| UX senior | Après | Après | Sous conditions | Sous conditions | Sous conditions |
| Accessibilité | Sous conditions | Sous conditions | Sous conditions | Sous conditions | Sous conditions |
| PM B2B | Sous conditions | Après | Sous conditions | Sous conditions | Sous conditions |
| Opérations | Après | Après | Sous conditions | Après | Sous conditions |
| Researcher | Sous conditions | Sous conditions | Sous conditions | Sous conditions | Sous conditions |
| Martine | Après | Après | Sous conditions | Sous conditions | Sous conditions |
| Patrick | Sous conditions | Sous conditions | Sous conditions | Sous conditions | Sous conditions |
| Nadia | Après | Après | Sous conditions | Après | Après |
| Julien | Sous conditions | Sous conditions | Sous conditions | Sous conditions | Sous conditions |
| Claire | Après | Après | Sous conditions | Sous conditions | Après |
| Hugo | Sous conditions | Après | Sous conditions | Sous conditions | Sous conditions |
| Isabelle | Après | Sous conditions | Après | Après | Sous conditions |

## Contradictions conservées et suites

Martine apprécie la confirmation qui gêne Patrick ; la maquette la maintient et renvoie son coût à une mesure réelle. Nadia et Isabelle veulent des détails transmissibles, Patrick veut l’action immédiatement visible : un résumé précède les détails, sans les supprimer. Claire privilégie la préparation au retour et Hugo le scanner : les deux restent disponibles, scanner en premier. Julien et Hugo refusent de confondre une présentation rassurante avec une garantie serveur éprouvée.

La fin de période est maintenant visible, un état « résultat toujours inconnu » a été ajouté, et le repère des actions attendues reste distinct de la lecture. Les libellés techniques de version/attestation restent dans le détail du cas prêt. Les consignes d’attente avant installation et les gestes du kit proviennent des captures existantes : il ne s’agit pas de règles ajoutées par les personas.

Les [arbitrages](arbitrages-maquettes.md) concluent à l’absence de changement substantiel des cinq orientations. Aucun nouveau vote nécessaire pour ces précisions. Une nouvelle règle métier ou un changement de périmètre imposerait une nouvelle décision, mais les votes simulés ne constitueraient toujours pas une autorisation de développement.

**Conclusion de conception :** propositions présentables pour validation, avec les limites documentées. Une revue visuelle par de vrais utilisateurs, une recette des états serveur et un contrôle d’accessibilité du produit restent à réaliser.
