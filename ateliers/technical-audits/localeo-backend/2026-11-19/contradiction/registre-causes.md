# Registre des causes — étape 3

Le registre initial vide est désormais renseigné par [causes-racines.md](causes-racines.md), source unique de correspondance constats → causes → orientations. Il contient 14 causes candidates ; le [backlog](../recommandations/backlog-preliminaire.md) retient huit orientations. Ne pas ouvrir de tickets distincts par domaine CPU/mémoire/SQL pour RC-01, ni deux tickets de bail pour ASY-03/SRE-01. RC-07 reste distincte : le bail et la remise transactionnelle ont des garanties différentes.

Aucun ticket externe créé. Les recommandations restent documentaires ; la contre-expertise et les votes ne donnent aucune autorisation d’implémentation.

API-02 est scindée entre RC-11 (échéance I/O) et RC-14 (répétition des contrôles) : ni le réglage réseau ni un cache ne résout automatiquement l’autre mécanisme.
