# Catalogue public et contacts operationnels

Les GET /public/referencement/commercants, /page et /{id} exposent une projection
explicite du catalogue actif : identite du commerce, ville, categorie, description
et images. Les nom/prenom/email/telephone du contact et la date de referencement
ne sont plus publics. Aucun champ de contact n'est actuellement qualifie comme
public dans le modele : ils restent donc tous prives.

Les listes historiques sous /protected exigent ADMIN. Le detail historique
exige une session commercant avec le scope commercant:profil et le rattachement
au commerce demande. /protected/profils/commercants/me reste disponible.
La marketplace utilise les nouvelles routes ; sa section contact n'apparait
plus sans coordonnees publiques explicites. Les applications Commercant et
Animation ne necessitent pas de changement pour ce contrat.

Deployer le backend avec les routes publiques avant le frontend coordonne.
Tests : anonymat refuse sur les routes privees, absence de donnees de contact
sur les trois formes publiques, acces au propre commerce et refus du tiers.
