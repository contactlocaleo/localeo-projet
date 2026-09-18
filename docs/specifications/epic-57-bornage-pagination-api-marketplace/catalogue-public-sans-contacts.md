# Catalogue public sans contacts operationnels

Le catalogue commercant utilise /public/referencement/commercants/page et /{id}.
La projection exclut contact et date_referencement ; les coordonnees du contact
principal ne sont plus publiees. La fiche continue a afficher la description,
les images, les prestations et le profil public valide. La section de contact
reste absente tant qu'aucune coordonnee explicitement publique n'est fournie.
Le backend doit etre deploye avant cette adaptation frontend.

Validation : tests de pagination avec le nouveau chemin et build production.
