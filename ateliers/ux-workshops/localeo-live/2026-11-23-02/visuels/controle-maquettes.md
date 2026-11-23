# Vérification des nouvelles maquettes

Les fichiers locaux ont été ouverts avec Playwright et Chromium le 23 novembre. Le contrôle porte sur les maquettes de la seconde exécution.

| Contrôle | Résultat |
| --- | --- |
| Comparatif | Deux colonnes à 1 440 px. Bascule AVANT/APRÈS à 320, 390 et 430 px. 14 états ouverts, sept AVANT équivalents, quatre captures de contexte et trois AVANT manquants. |
| Planches | 42 lectures aux trois largeurs et 14 lectures à 320 px avec texte à 200 %. Aucun débordement horizontal. Un titre principal et identifiants uniques pour chaque état. |
| Navigation et clavier | Mes lots → Tirages → Passeport → retour au tirage, avec focus sur sa carte. Le lien d’aide du lot atteint sa section. Entrée sur « Prochainement » déplace le focus sur le titre de période. |
| Ressources et rendu | Galerie ordinateur, vue mobile et planches P1 relues. Aucune erreur JavaScript, ressource manquante ou requête HTTP externe pendant l’essai local. |

Le prototype couvre les affichages et les retours simulés. Le fonctionnement d’un contact effectif, le scan QR de bout en bout, le retrait et les aides d’accès sur appareil restent à vérifier dans Live. [Références des maquettes](reference-maquettes.md) · [Limites du constat](../observations/limitations.md)
