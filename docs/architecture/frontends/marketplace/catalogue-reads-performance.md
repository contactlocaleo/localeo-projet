# Lectures du catalogue Marketplace

Les lecteurs `fetchCoffrets` et `fetchCommercants` conservent leur resultat sous
forme de tableau complet. Ils parcourent les pages de cent elements des routes
`/coffrets/page` (curseur) et `/commercants/page` (numero de page). Aucun maximum
silencieux ne tronque les tris, compteurs ou experiences de la page commune.
Les reponses de pagination incoherentes produisent une erreur; une annulation
arrete le transport et empeche le chargement de la page suivante.

La page commune demande les prestations dans le catalogue et ne recharge plus
chaque fiche coffret. Les details, animations et compteurs transmettent le signal
d'annulation de React Query au client HTTP.

La fiche commercant demande uniquement ses coffrets au serveur. Elle charge les
commercants rattaches aux prestations par groupes d'au plus cent identifiants.
La fiche coffret reutilise cette lecture groupee. Les champs de presentation sont
identiques a ceux de la fiche commercant; l'ordre des adresses du coffret est
conserve. Les selections partagent une cle de cache normalisee par identifiants.

Le catalogue filtre d'un commercant utilise une cle distincte du catalogue de
commune et ne remplace jamais les listes completes de la commune en session.
La politique de fraicheur existante des coffrets reste appliquee, sans nouveau
cache global de publication ou de conformite BUM/Stripe.

Validation: `node --test tests/security/catalogue-pagination.test.cjs
tests/security/merchant-pagination.test.cjs tests/security/request-deadline.test.cjs`
et `npm run build`.
