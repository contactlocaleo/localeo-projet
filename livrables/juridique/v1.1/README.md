# Sources juridiques éditables V1.1

Quatre DOCX et le [manifeste de correction](MANIFESTE_CORRECTIONS_V1_1.json) du 13 septembre 2026 ont été déplacés du backend. Le manifeste utilise désormais des chemins relatifs à la racine de `localeo-projet`. Les empreintes et le détail des corrections ont été conservés. Les quatre copies PDF identiques ont été supprimées ; `canonical_pdf` et `export_pdf` désignent le même PDF du corpus juridique.

Leur classement ne constitue pas une nouvelle validation ni une publication. Le [catalogue juridique](../../../docs/juridique/publication/catalogue.json) garde l’autorité sur les versions publiables.

## Contrat commerçant — correction du 28 septembre 2026

Une cinquième source Word est ajoutée :
[Contrat de partenariat commerçant avec fiche prestations](<LOCALEO - Contrat de Partenariat Commerçant avec fiche prestations - V1.docx>).
Elle correspond au [PDF canonique](<../../../docs/juridique/commercant/LOCALEO - Contrat de Partenariat Commerçant avec fiche prestations - V1.pdf>),
désormais en version 1.1 du 28 septembre 2026 ; les noms de fichiers restent stables.

Corrections demandées : article 7, « montant TTC », remplacement du paragraphe
technique par une explication courte de la commission conservant l'arrondi du net,
et « à posteriori » ; article 15, « six mois de vente ». Les autres clauses et la
fiche prestations sont conservées. La source historique reste dans
`versions-de-travail`. Le catalogue est actualisé avec la nouvelle version et
l'empreinte du PDF. Aucune publication distante ni modification des contrats
déjà signés n'est réalisée par cette correction locale.

## Publication en production du 28 septembre 2026

Le balisage des tableaux du contrat commerçant a été corrigé dans la source Word
et son export PDF pour permettre la conversion en lecture web. Le texte des huit
pages reste identique ; l'empreinte du catalogue est actualisée.

Le lot `1b64688ccf906fcdc2c0b525080270ed493b24202a12774e2c4dbadae24561c1`
a été publié en production : 12 documents publics, dont le contrat commerçant
1.1, sans retrait de document. Les contrôles API des fichiers et les contrôles
des lecteurs web ont réussi sur les quatre surfaces :

- [Commerçant](https://commercants.localeo.city/juridique) : 5 documents.
- [Animation](https://animation.localeo.city/juridique) : 7 documents.
- [Coffrets](https://coffrets.localeo.city/juridique) : 8 documents.
- [Live](https://coffrets.localeo.city/live/juridique) : 6 documents.

Certains documents sont communs à plusieurs surfaces. Tous les documents ont
été vérifiés sur ordinateur, ainsi qu'un document représentatif sur mobile par
surface, sans débordement horizontal ni erreur JavaScript. La clé temporaire de
publication a été révoquée après les contrôles. Les rapports et le lot exact sont
conservés hors Git dans `localeo-backend/tmp/juridique-prod-20260928/`.
Cette publication documentaire ne constitue pas un déploiement du code des
applications.
