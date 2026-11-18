# Votes et arbitrages — simulation

**12 voix fictives, une par participant, 14 orientations, 168 votes nominatifs.** Le facilitateur n’a aucune voix prépondérante. Pour ≥ 7 : ADOPTÉE ; Pour = 6 : NON ADOPTÉE ; Pour ≤ 5 : REJETÉE. Une abstention conserve le dénominateur de douze. Les sept commerçants ont sept voix, mais votent individuellement. Aucun vote ne représente un entretien, un consentement utilisateur ou une recette technique.

Les avis initiaux ont été rédigés avant le vote dans trois revues séparées (experts, quatre commerçants, trois commerçants), puis confrontés dans le [compte rendu](compte-rendu.md). Les votes portent sur les formulations précises des fiches [adoptées](backlog-ux.md) et [rejetées](orientations-rejetees.md). Les arguments sont restitués de façon concise, sans changer les voix.

| ID | Orientation | Pour | Contre | Abstention | Décision |
| --- | --- | ---: | ---: | ---: | --- |
| A1 | Identifier l’accès Pro et expliquer son rôle en une phrase | 11 | 0 | 1 | ADOPTÉE |
| A2 | Imposer cinq écrans de tutoriel avant le premier scan | 1 | 11 | 0 | REJETÉE |
| B1 | Rendre le scan et son résultat compréhensibles, éprouver les garanties existantes | 11 | 1 | 0 | ADOPTÉE |
| B2 | Valider automatiquement tout QR reconnu | 1 | 11 | 0 | REJETÉE |
| C1 | Distinguer information reçue et action attendue | 12 | 0 | 0 | ADOPTÉE |
| C2 | Relancer chaque jour tous les messages non lus par push | 0 | 12 | 0 | REJETÉE |
| D1 | Rendre cohérents dates, états et prochaine action de préparation | 9 | 0 | 3 | ADOPTÉE |
| D2 | Fusionner les états dans « Tout est prêt » | 2 | 10 | 0 | REJETÉE |
| E1 | Présenter les supports par usage et des dates lisibles | 12 | 0 | 0 | ADOPTÉE |
| E2 | Déclarer prêt dès le téléchargement du kit | 1 | 11 | 0 | REJETÉE |
| F1 | Retrouver le contexte fiable après interruption ou absence | 12 | 0 | 0 | ADOPTÉE |
| F2 | Afficher une validation réussie hors connexion puis synchroniser | 1 | 10 | 1 | REJETÉE |
| G1 | Alléger les répétitions en gardant les repères et le détail accessible | 10 | 0 | 2 | ADOPTÉE |
| G2 | Remplacer systématiquement le grand scanner par la prochaine tâche | 2 | 8 | 2 | REJETÉE |

<a id="a1"></a>

## A1 — Identifier l’accès Pro et expliquer son rôle en une phrase

Vérifier les liens réellement diffusés ; identifier clairement l’espace commerçant et ajouter, si utile, une phrase sur la participation aux animations avec une aide courte à la demande.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | POUR | Clarifie destination et rôle sans ralentir l’entrée. |
| Expert 2 — Accessibilité | POUR | L’aide doit rester identifiable et accessible au clavier. |
| Expert 3 — Product Manager B2B | POUR | Clarifie l’accès sans présumer une erreur des supports actuels. |
| Expert 4 — Opérations terrain | POUR | Une indication courte aide à rejoindre le bon portail. |
| Expert 5 — Researcher et facilitateur | POUR | Ne généralisons pas l’erreur d’URL de cet audit. |
| Martine — fleuriste, 63 ans | POUR | Je saurais où me connecter et à quoi sert cet endroit. |
| Patrick — boulanger, 57 ans | POUR | Donnez-moi le bon accès, je peux commencer. |
| Nadia — salon de coiffure, 44 ans | POUR | Une explication courte me suffit pour me repérer. |
| Julien — restaurateur, 35 ans | POUR | L’accès commerçant doit être facile à identifier. |
| Claire — prêt-à-porter, 51 ans | POUR | Je saurais quelle adresse conserver pour retrouver mon espace. |
| Hugo — boutique spécialisée, 29 ans | ABSTENTION | Vérifions les accès existants avant d’ajouter du texte. |
| Isabelle — libraire, 48 ans | POUR | Après plusieurs semaines, identifier mon espace me rassurerait. |

**Décision : 11 pour / 0 contre / 1 abstention — **ADOPTÉE**.** Hugo s’abstient : vérifier les accès existants avant d’ajouter du texte.

<a id="a2"></a>

## A2 — Imposer cinq écrans de tutoriel avant le premier scan

Tutoriel obligatoire en cinq écrans avant l’accès initial au scanner.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | CONTRE | Cinq écrans imposés retardent l’action sans besoin démontré. |
| Expert 2 — Accessibilité | CONTRE | Un passage obligatoire multiplie les obstacles avant l’action. |
| Expert 3 — Product Manager B2B | CONTRE | Le coût d’entrée précède tout bénéfice utilisateur établi. |
| Expert 4 — Opérations terrain | CONTRE | En service, le commerçant doit pouvoir scanner immédiatement. |
| Expert 5 — Researcher et facilitateur | CONTRE | Aucun débutant observé ne justifie ce dispositif obligatoire. |
| Martine — fleuriste, 63 ans | POUR | La première fois, je préfère qu’on me montre chaque étape. |
| Patrick — boulanger, 57 ans | CONTRE | Cinq écrans avant de servir un client, c’est trop. |
| Nadia — salon de coiffure, 44 ans | CONTRE | Je voudrais consulter l’aide au moment où j’en ai besoin. |
| Julien — restaurateur, 35 ans | CONTRE | Je dois pouvoir scanner immédiatement. |
| Claire — prêt-à-porter, 51 ans | CONTRE | Cinq écrans avant de servir une cliente, c’est trop. |
| Hugo — boutique spécialisée, 29 ans | CONTRE | Je préfère une aide accessible au moment utile. |
| Isabelle — libraire, 48 ans | CONTRE | Je risque d’oublier avant ma prochaine utilisation. |

**Décision : 1 pour / 11 contre / 0 abstention — **REJETÉE**.** Martine vote pour : elle souhaite être guidée la première fois. Les onze autres refusent l’obligation.

<a id="b1"></a>

## B1 — Rendre le scan et son résultat compréhensibles, éprouver les garanties existantes

Corriger le message hors contexte ; expliquer quel QR présenter et le prochain geste possible. Conserver la confirmation distincte, le reçu et les protections contre les renvois. Recetter sur téléphone puis modifier seulement les écarts établis.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | POUR | Le message observé manque de contexte et de prochaine action. |
| Expert 2 — Accessibilité | POUR | Vérifier aussi les annonces accessibles et le focus. |
| Expert 3 — Product Manager B2B | POUR | La recette préalable préserve les garanties déjà présentes. |
| Expert 4 — Opérations terrain | POUR | Un résultat explicite aide à décider devant le participant. |
| Expert 5 — Researcher et facilitateur | POUR | Vérifier les scénarios manquants avant toute modification complémentaire. |
| Martine — fleuriste, 63 ans | POUR | Je veux vérifier avant de confirmer et être rassurée après. |
| Patrick — boulanger, 57 ans | CONTRE | Je veux une réponse claire, mais confirmer chaque client me ralentit. |
| Nadia — salon de coiffure, 44 ans | POUR | Vérifier l’animation avant de confirmer évite une mauvaise manipulation. |
| Julien — restaurateur, 35 ans | POUR | Gardons la vérification tant que les erreurs restent mal connues. |
| Claire — prêt-à-porter, 51 ans | POUR | Je comprendrais quel code demander et quoi faire ensuite. |
| Hugo — boutique spécialisée, 29 ans | POUR | Vérifions les vrais écarts avant de modifier le scanner. |
| Isabelle — libraire, 48 ans | POUR | Une confirmation claire m’aiderait à répondre au client sans hésiter. |

**Décision : 11 pour / 1 contre / 0 abstention — **ADOPTÉE**.** Patrick vote contre le maintien de la confirmation à chaque client ; la recette doit mesurer son coût sans retirer la garantie.

<a id="b2"></a>

## B2 — Valider automatiquement tout QR reconnu

Supprimer la confirmation après reconnaissance du QR.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | CONTRE | Reconnaître un QR ne suffit pas à confirmer l’intention. |
| Expert 2 — Accessibilité | CONTRE | Une action immédiate réduit le contrôle de l’utilisateur. |
| Expert 3 — Product Manager B2B | CONTRE | Supprime une garantie sans nécessité ni contrat vérifié. |
| Expert 4 — Opérations terrain | CONTRE | Une lecture accidentelle pourrait déclencher une validation non souhaitée. |
| Expert 5 — Researcher et facilitateur | CONTRE | Aucun essai complet ne justifie de supprimer la confirmation. |
| Martine — fleuriste, 63 ans | CONTRE | J’aurais peur de valider sans m’en rendre compte. |
| Patrick — boulanger, 57 ans | POUR | Si le code est reconnu, je veux passer au client suivant. |
| Nadia — salon de coiffure, 44 ans | CONTRE | Je préfère garder un instant pour vérifier. |
| Julien — restaurateur, 35 ans | CONTRE | Reconnaître un code ne garantit pas la bonne validation. |
| Claire — prêt-à-porter, 51 ans | CONTRE | Je veux pouvoir vérifier avant de confirmer. |
| Hugo — boutique spécialisée, 29 ans | CONTRE | Reconnaître un code ne garantit pas que je souhaite valider. |
| Isabelle — libraire, 48 ans | CONTRE | Un scan involontaire pourrait engager une action que j’ignore. |

**Décision : 1 pour / 11 contre / 0 abstention — **REJETÉE**.** Patrick est seul favorable. Sa contrainte de temps reste une exigence de recette de B1.

<a id="c1"></a>

## C1 — Distinguer information reçue et action attendue

Donner la priorité aux notifications Animation pour ce profil, replier la section PIN vide sans retirer son accès. Exposer animation, nature information/action, échéance connue et lien direct vers l’action autorisée.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | POUR | La priorité Animation correspond au profil et préserve PIN. |
| Expert 2 — Accessibilité | POUR | Le repli doit annoncer son état et rester accessible. |
| Expert 3 — Product Manager B2B | POUR | Sépare consultation du message et accomplissement opérationnel. |
| Expert 4 — Opérations terrain | POUR | Le lien direct rapproche information et action attendue. |
| Expert 5 — Researcher et facilitateur | POUR | Exploite les constats sans présumer l’efficacité des canaux. |
| Martine — fleuriste, 63 ans | POUR | Je verrais plus facilement ce qui me concerne aujourd’hui. |
| Patrick — boulanger, 57 ans | POUR | Montrez-moi directement ce qui attend une action. |
| Nadia — salon de coiffure, 44 ans | POUR | Lire une consigne ne veut pas dire l’avoir appliquée. |
| Julien — restaurateur, 35 ans | POUR | Chaque message doit m’amener à ce que je dois faire. |
| Claire — prêt-à-porter, 51 ans | POUR | Je distinguerais informations et demandes attendant ma réponse. |
| Hugo — boutique spécialisée, 29 ans | POUR | Gardons les liens directs et replions le bloc vide. |
| Isabelle — libraire, 48 ans | POUR | Une demande déjà lue peut encore nécessiter mon intervention. |

**Décision : 12 pour / 0 contre / 0 abstention — **ADOPTÉE**.** Unanimité sur ce périmètre limité, sans soutien au rappel quotidien C2.

<a id="c2"></a>

## C2 — Relancer chaque jour tous les messages non lus par push

Push quotidien systématique à tous tant qu’un message reste non lu.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | CONTRE | Une nonlecture ne signifie pas qu’une action reste nécessaire. |
| Expert 2 — Accessibilité | CONTRE | Le rappel imposé ne respecte pas les besoins individuels. |
| Expert 3 — Product Manager B2B | CONTRE | Le déclencheur ignore urgence, échéance et préférences. |
| Expert 4 — Opérations terrain | CONTRE | Des rappels sans action pertinente deviennent du bruit. |
| Expert 5 — Researcher et facilitateur | CONTRE | Réception et utilité du push restent non vérifiées. |
| Martine — fleuriste, 63 ans | CONTRE | Tous les jours, je finirais par ne plus les regarder. |
| Patrick — boulanger, 57 ans | CONTRE | Je couperais les notifications dès la première semaine. |
| Nadia — salon de coiffure, 44 ans | CONTRE | Rappelez-moi l’échéance, pas simplement que je n’ai pas ouvert. |
| Julien — restaurateur, 35 ans | CONTRE | Je veux choisir les alertes qui interrompent mon service. |
| Claire — prêt-à-porter, 51 ans | CONTRE | Je finirais par couper ces rappels quotidiens. |
| Hugo — boutique spécialisée, 29 ans | CONTRE | Un message non lu ne justifie pas systématiquement une relance. |
| Isabelle — libraire, 48 ans | CONTRE | Certains jours, je ne participe à aucune animation. |

**Décision : 0 pour / 12 contre / 0 abstention — **REJETÉE**.** Aucun vote favorable ; le besoin d’anticipation de Nadia reste couvert par C1/D1/F1.

<a id="d1"></a>

## D1 — Rendre cohérents dates, états et prochaine action de préparation

Diagnostiquer la règle et le périmètre des compteurs, puis afficher des états cohérents ou des différences explicitement justifiées. Mettre en avant le prochain geste, son responsable et sa date connue, en conservant les distinctions métier derrière une présentation progressive.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | ABSTENTION | La hiérarchie de cinq statuts mérite clarification avant adoption. |
| Expert 2 — Accessibilité | ABSTENTION | La compréhension dépend d’une présentation encore indéfinie. |
| Expert 3 — Product Manager B2B | POUR | Vérifier la règle serveur évite d’inventer une correction métier. |
| Expert 4 — Opérations terrain | POUR | Responsable, échéance et prochain geste facilitent la préparation. |
| Expert 5 — Researcher et facilitateur | POUR | Conserve l’incertitude causale et exige une vérification préalable. |
| Martine — fleuriste, 63 ans | ABSTENTION | Je veux savoir quoi faire, mais tous ces mots m’inquiètent. |
| Patrick — boulanger, 57 ans | POUR | Dites-moi ce qui manque et qui doit s’en occuper. |
| Nadia — salon de coiffure, 44 ans | POUR | Je dois distinguer mon accord de ma préparation réelle. |
| Julien — restaurateur, 35 ans | POUR | Les chiffres doivent raconter la même chose partout. |
| Claire — prêt-à-porter, 51 ans | POUR | Je saurais ce qui reste à préparer pour demain. |
| Hugo — boutique spécialisée, 29 ans | POUR | Des compteurs cohérents éviteraient mes vérifications inutiles. |
| Isabelle — libraire, 48 ans | POUR | Je retrouverais ma situation sans recommencer toutes les vérifications. |

**Décision : 9 pour / 0 contre / 3 abstention — **ADOPTÉE**.** UX, Accessibilité et Martine s’abstiennent : cinq statuts pourraient surcharger. La présentation devra faire l’objet d’un test de compréhension.

<a id="d2"></a>

## D2 — Fusionner les états dans « Tout est prêt »

Un bouton unique fusionnerait accepté, prêt, approuvé et contrôlé.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | CONTRE | Efface des distinctions potentiellement nécessaires à la compréhension. |
| Expert 2 — Accessibilité | CONTRE | Un libellé unique masquerait les conditions réellement remplies. |
| Expert 3 — Product Manager B2B | CONTRE | Ces états engagent des acteurs et garanties différents. |
| Expert 4 — Opérations terrain | CONTRE | Accepter ne prouve pas que l’installation est terminée. |
| Expert 5 — Researcher et facilitateur | CONTRE | Les équivalences entre ces états n’ont pas été établies. |
| Martine — fleuriste, 63 ans | POUR | Un état simple me rassurerait, si je comprends ce qu’il signifie. |
| Patrick — boulanger, 57 ans | POUR | Un seul bouton serait plus rapide entre deux clients. |
| Nadia — salon de coiffure, 44 ans | CONTRE | Accepter ne signifie pas que mes affiches sont installées. |
| Julien — restaurateur, 35 ans | CONTRE | Je perdrais la distinction entre mon travail et celui du gestionnaire. |
| Claire — prêt-à-porter, 51 ans | CONTRE | Accepter une invitation ne signifie pas avoir installé les supports. |
| Hugo — boutique spécialisée, 29 ans | CONTRE | Ce bouton masquerait des situations demandant des actions différentes. |
| Isabelle — libraire, 48 ans | CONTRE | Ma collègue pourrait croire que tout est installé. |

**Décision : 2 pour / 10 contre / 0 abstention — **REJETÉE**.** Martine et Patrick votent pour la simplicité ; cette demande motive la présentation progressive de D1.

<a id="e1"></a>

## E1 — Présenter les supports par usage et des dates lisibles

Vérifier le kit réel puis annoncer les supports effectivement disponibles et leur usage. Rendre les dates locales lisibles. Relier les consignes d’impression, d’affichage et d’équipe aux bons documents et expliciter le rôle des QR.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | POUR | Relie chaque support à son usage et clarifie les QR. |
| Expert 2 — Accessibilité | POUR | Dates locales plus lisibles ; fichiers encore à vérifier. |
| Expert 3 — Product Manager B2B | POUR | Distingue accès au kit et préparation effective. |
| Expert 4 — Opérations terrain | POUR | Imprimer, afficher et partager deviennent des consignes distinctes. |
| Expert 5 — Researcher et facilitateur | POUR | Le contenu annoncé dépend de l’examen des fichiers. |
| Martine — fleuriste, 63 ans | POUR | Je saurais quoi imprimer et quel code montrer. |
| Patrick — boulanger, 57 ans | POUR | Je veux trouver immédiatement les documents utiles au comptoir. |
| Nadia — salon de coiffure, 44 ans | POUR | Je pourrais vérifier mes supports avant le jour prévu. |
| Julien — restaurateur, 35 ans | POUR | Je veux connaître le contenu avant de télécharger. |
| Claire — prêt-à-porter, 51 ans | POUR | Je saurais quoi imprimer et quel QR afficher. |
| Hugo — boutique spécialisée, 29 ans | POUR | Annonçons précisément les fichiers réellement disponibles. |
| Isabelle — libraire, 48 ans | POUR | Je pourrais transmettre des consignes compréhensibles à ma collègue. |

**Décision : 12 pour / 0 contre / 0 abstention — **ADOPTÉE**.** Unanimité conditionnée à l’examen des fichiers ; aucun accord pour E2.

<a id="e2"></a>

## E2 — Déclarer prêt dès le téléchargement du kit

Déclencher automatiquement l’état prêt au téléchargement.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | CONTRE | Télécharger ne renseigne pas sur les actions physiques restantes. |
| Expert 2 — Accessibilité | CONTRE | Le changement automatique communique un état opérationnel trompeur. |
| Expert 3 — Product Manager B2B | CONTRE | Confond disponibilité documentaire et exécution de la préparation. |
| Expert 4 — Opérations terrain | CONTRE | Recevoir le fichier ne signifie ni imprimer ni afficher. |
| Expert 5 — Researcher et facilitateur | CONTRE | Aucune observation ne relie téléchargement et préparation terminée. |
| Martine — fleuriste, 63 ans | CONTRE | J’aurais récupéré le fichier, pas forcément réussi à l’imprimer. |
| Patrick — boulanger, 57 ans | POUR | Ça m’éviterait une étape, je gère ensuite l’installation moi-même. |
| Nadia — salon de coiffure, 44 ans | CONTRE | Mes supports peuvent rester plusieurs jours dans mes téléchargements. |
| Julien — restaurateur, 35 ans | CONTRE | Un fichier récupéré ne prouve pas que mon équipe est prête. |
| Claire — prêt-à-porter, 51 ans | CONTRE | Télécharger ne veut pas dire avoir imprimé les affiches. |
| Hugo — boutique spécialisée, 29 ans | CONTRE | Un fichier téléchargé ne prouve aucune préparation du magasin. |
| Isabelle — libraire, 48 ans | CONTRE | Je télécharge parfois pour m’en occuper plusieurs jours après. |

**Décision : 1 pour / 11 contre / 0 abstention — **REJETÉE**.** Patrick vote pour ; Martine souligne qu’elle peut avoir téléchargé sans réussir à imprimer.

<a id="f1"></a>

## F1 — Retrouver le contexte fiable après interruption ou absence

Éprouver les reprises existantes ; après reconnexion, relire l’état autorisé et redonner le contexte de l’animation, la prochaine échéance connue et l’étape restante. Compléter uniquement les manques démontrés.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | POUR | Retrouver contexte et prochaine action facilite la reprise. |
| Expert 2 — Accessibilité | POUR | Annoncer l’état sans déplacement imprévisible du focus. |
| Expert 3 — Product Manager B2B | POUR | L’état autorisé prévaut ; vérifier les capacités existantes d’abord. |
| Expert 4 — Opérations terrain | POUR | Après interruption, retrouver ce qui reste à faire. |
| Expert 5 — Researcher et facilitateur | POUR | Vérifier évite de transformer un scénario inédit en défaut. |
| Martine — fleuriste, 63 ans | POUR | Je retrouverais ce qu’il reste à faire sans tout chercher. |
| Patrick — boulanger, 57 ans | POUR | Après une interruption, je dois reprendre immédiatement. |
| Nadia — salon de coiffure, 44 ans | POUR | Je pourrais reprendre ma préparation entre deux rendez-vous. |
| Julien — restaurateur, 35 ans | POUR | Je veux retrouver le dernier état réellement enregistré. |
| Claire — prêt-à-porter, 51 ans | POUR | Je reprendrais là où j’en étais sans chercher partout. |
| Hugo — boutique spécialisée, 29 ans | POUR | Après interruption, je veux retrouver un état fiable. |
| Isabelle — libraire, 48 ans | POUR | C’est le rappel dont j’ai besoin après plusieurs semaines. |

**Décision : 12 pour / 0 contre / 0 abstention — **ADOPTÉE**.** Unanimité sur la continuité fiable ; Patrick préfère aussi F2, rejeté pour son faux succès.

<a id="f2"></a>

## F2 — Afficher une validation réussie hors connexion puis synchroniser

Coche verte immédiate hors connexion, puis synchronisation automatique.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | CONTRE | La coche présente comme certain un résultat encore différé. |
| Expert 2 — Accessibilité | CONTRE | Le succès annoncé serait trompeur quelle que soit sa modalité. |
| Expert 3 — Product Manager B2B | CONTRE | Conflits et doublons différés sans traitement établi. |
| Expert 4 — Opérations terrain | CONTRE | Une validation refusée ensuite serait difficile à expliquer. |
| Expert 5 — Researcher et facilitateur | CONTRE | Aucun test hors connexion ne justifie cette promesse. |
| Martine — fleuriste, 63 ans | ABSTENTION | Je ne comprends pas comment savoir si c’est vraiment terminé. |
| Patrick — boulanger, 57 ans | POUR | Une mauvaise connexion ne doit pas bloquer toute ma file. |
| Nadia — salon de coiffure, 44 ans | CONTRE | Je croirais la participation enregistrée alors qu’elle attend. |
| Julien — restaurateur, 35 ans | CONTRE | Une coche verte doit correspondre à une validation certaine. |
| Claire — prêt-à-porter, 51 ans | CONTRE | Une coche verte me ferait annoncer une validation encore incertaine. |
| Hugo — boutique spécialisée, 29 ans | CONTRE | Sans réponse serveur, je veux connaître l’incertitude. |
| Isabelle — libraire, 48 ans | CONTRE | Je ne saurais pas expliquer un échec découvert plus tard. |

**Décision : 1 pour / 10 contre / 1 abstention — **REJETÉE**.** Patrick vote pour afin de préserver la file ; Martine s’abstient car elle ne saurait pas si l’action est terminée.

<a id="g1"></a>

## G1 — Alléger les répétitions en gardant les repères et le détail accessible

Comparer une présentation plus courte du détail, centrée sur mission, état et accès préparation/kit, en gardant l’historique et les consignes complètes atteignables. Maintenir les destinations actuelles.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | POUR | Réduire les répétitions si la compréhension progresse. |
| Expert 2 — Accessibilité | POUR | Conserver les repères protège l’orientation. |
| Expert 3 — Product Manager B2B | POUR | La comparaison préalable vérifie l’utilité de la modification. |
| Expert 4 — Opérations terrain | ABSTENTION | Des répétitions pourraient éviter les allers-retours en préparation. |
| Expert 5 — Researcher et facilitateur | POUR | La compréhension devient un critère comparatif préalable. |
| Martine — fleuriste, 63 ans | POUR | Je chercherais moins si les informations ne se répétaient pas partout. |
| Patrick — boulanger, 57 ans | POUR | Moins de répétitions, c’est moins de temps perdu. |
| Nadia — salon de coiffure, 44 ans | POUR | Je veux garder les consignes complètes près des supports. |
| Julien — restaurateur, 35 ans | POUR | Simplifiez si je retrouve toujours rapidement chaque détail. |
| Claire — prêt-à-porter, 51 ans | POUR | Moins de répétitions m’aideraient à retrouver les consignes utiles. |
| Hugo — boutique spécialisée, 29 ans | POUR | Comparons la compréhension avant de supprimer des répétitions. |
| Isabelle — libraire, 48 ans | ABSTENTION | Je voudrais voir si je retrouve toujours mes repères. |

**Décision : 10 pour / 0 contre / 2 abstention — **ADOPTÉE**.** Opérations et Isabelle s’abstiennent : des répétitions peuvent éviter des allers-retours ou servir de repères.

<a id="g2"></a>

## G2 — Remplacer systématiquement le grand scanner par la prochaine tâche

Remplacer le grand scanner de l’accueil par une carte tâche ; conserver le scanner uniquement dans la navigation.

| Participant | Vote | Argument individuel simulé |
| --- | --- | --- |
| Expert 1 — UX Designer senior | CONTRE | Le remplacement ignore les moments où scanner est prioritaire. |
| Expert 2 — Accessibilité | ABSTENTION | L’effet dépend de l’accessibilité réelle des deux accès. |
| Expert 3 — Product Manager B2B | CONTRE | La priorité permanente par tâche manque de justification. |
| Expert 4 — Opérations terrain | CONTRE | Pendant l’animation, le scanner doit rester saillant. |
| Expert 5 — Researcher et facilitateur | CONTRE | Aucun comparatif ne justifie ce changement systématique. |
| Martine — fleuriste, 63 ans | CONTRE | Le gros bouton m’aide à savoir où scanner. |
| Patrick — boulanger, 57 ans | CONTRE | Pendant le service, scanner reste mon premier besoin. |
| Nadia — salon de coiffure, 44 ans | POUR | Je verrais plus tôt ce que je dois préparer. |
| Julien — restaurateur, 35 ans | CONTRE | L’action fréquente doit rester immédiatement accessible sur l’accueil. |
| Claire — prêt-à-porter, 51 ans | POUR | Je préfère voir ma prochaine tâche dès l’ouverture. |
| Hugo — boutique spécialisée, 29 ans | CONTRE | Au comptoir, le scanner doit rester immédiatement visible. |
| Isabelle — libraire, 48 ans | ABSTENTION | Mes besoins changent entre préparation et journée d’animation. |

**Décision : 2 pour / 8 contre / 2 abstention — **REJETÉE**.** Nadia et Claire votent pour ; Accessibilité et Isabelle s’abstiennent. Le besoin d’échéance est repris par D1/F1 sans retirer le scanner.

## Arbitrages transverses

- B1/B2 : conserver la confirmation et mesurer le coût en caisse demandé par Patrick ; aucune promesse de rapidité déduite des captures.
- D1/D2 : neuf voix pour la cohérence et la prochaine action, mais trois abstentions sur la lisibilité des statuts. Ne pas confondre maintien des distinctions métier et affichage simultané de cinq badges.
- E1/E2 : le kit et la préparation effective restent distincts ; le besoin de rapidité de Patrick ne prouve pas que télécharger équivaut à installer.
- F1/F2 : reprendre un état serveur fiable ; une coche de réussite hors connexion serait trompeuse, même si elle obtenait sept voix.
- G1/G2 : dix voix pour alléger sous condition de compréhension ; refus de remplacer systématiquement le scanner. Les repères d’Isabelle et les allers-retours évoqués par Opérations doivent être testés.

Les conditions de recette B1/F1, l’accès au bon portail et la vérification d’accessibilité ne sont pas levés par ces votes. Voir le [rapport exécutif](rapport-executif.md).
