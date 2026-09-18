# Résultats lisibles dans le Live

La table des événements récents affiche les colonnes Date, Type, Événement et
Résultat. Le résultat contient le nom du commerçant pour une validation ou la
référence du participant pour une inscription. Si un commerçant est introuvable,
la référence du participant est utilisée lorsqu’elle est disponible ; sinon un
libellé « non renseigné » est affiché. Le JSON technique n’est plus rendu.

L’API `GET /protected/animation-locale/animations/{id}/live/evenements` ajoute
deux champs optionnels : `commercant_nom` et `participant_reference`. Les anciens
champs sont conservés pour compatibilité. Le contrôle du partenaire et de la
commune précède la lecture. Les jointures n’exposent pas les coordonnées des
participants et restent limitées à l’animation et à la commune demandées.

Le flux est construit par une seule requête SQL : chaque source est ordonnée et
limitée à N événements, puis les deux sources sont fusionnées et limitées à N
avant les jointures des noms et références. N vaut 50 par défaut, plafonné à 100.
Le navigateur ne charge pas les fiches individuelles. Le rafraîchissement toutes
les 15 secondes reste inchangé.

Les index déjà livrés par `v169_epic45_vision_360_animation.sql` couvrent ces tris :
`idx_animation_participants_animation_inscrit` et
`idx_animation_validations_animation_date`. Aucune migration supplémentaire.

Vérifications : tests serveur sur les résultats, le tri stable, l’isolation, les
références manquantes, les limites et le nombre de requêtes ; tests frontend et
parcours navigateur sur ordinateur et mobile. Mesure locale PostgreSQL 18 du
13 septembre 2026 sur 100 000 inscriptions et 100 000 validations synthétiques,
réparties entre deux animations : 50 résultats, 1,490 ms d’exécution SQL,
6,016 ms de planification, index utilisés et buffers en mémoire. Cette mesure
exclut le réseau et le contrôle d’accès ; elle ne constitue pas une mesure de
l’environnement de test déployé.

Déployer le backend et le frontend ensemble pour bénéficier des nouveaux champs.
