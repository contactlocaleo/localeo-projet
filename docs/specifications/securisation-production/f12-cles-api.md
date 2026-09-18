# F12 - Usage des cles API

L'autorisation relit en base le hash, l'etat actif et le scope a chaque appel.
Elle ne met pas en cache une autorisation : une revocation reste immediate.
`last_used_at` est une indication d'exploitation arrondie a un intervalle de
cinq minutes. Son UPDATE est conditionnel en base pour eviter les ecritures
concurrentes inutiles ; ce champ n'est pas un journal exhaustif des appels.
