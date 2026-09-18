# ADR-2026-08-28 - Privilegier le domaine aux services applicatifs

## Statut

Acceptee

## Contexte

Plusieurs evolutions recentes, en particulier dans `animation_locale`, ont concentre des regles metier dans
des classes de `app/application/<domaine>/services`. Ces classes assurent correctement l'orchestration des
transactions, repositories, notifications et integrations, mais portent aussi des controles de statut, de
dates, d'eligibilite et de transition qui appartiennent au modele metier.

Cette repartition produit un modele de domaine trop anemique et dilue les invariants entre plusieurs services
applicatifs. Une meme regle risque alors d'etre reproduite differemment dans une API, un batch, une commande
administrative ou une integration. Elle devient egalement plus difficile a tester sans Unit of Work ni
infrastructure.

Cette situation n'est pas une orientation cible. Elle constitue une dette d'architecture a corriger
progressivement.

## Decision

Toute nouvelle regle metier ou modification substantielle d'une regle existante doit etre implementee en
priorite dans `app/domaine/<domaine>`.

La question de placement est tranchee dans cet ordre :

1. **Entite ou agregat** lorsque la regle depend de son etat, protege une transition ou garantit sa coherence.
2. **Objet-valeur** lorsque la regle definit la validite, la normalisation ou les operations d'une valeur.
3. **Service de domaine** lorsque la decision metier associe plusieurs entites ou agregats et reste pure,
   sans acces a la base, au reseau, au framework ou a un fournisseur externe.
4. **Couche application** uniquement pour orchestrer le scenario, charger les objets, verifier le perimetre
   d'acces, ouvrir la transaction, appeler le domaine, persister le resultat et declencher les effets
   secondaires.
5. **Infrastructure** pour les implementations SQLAlchemy, stockage, rendu documentaire, messagerie et
   fournisseurs externes.

Un service applicatif ne doit pas devenir le proprietaire d'une regle sous pretexte qu'il dispose deja du
Unit of Work ou des objets ORM necessaires a son execution.

### Matrice de placement

| Nature du comportement | Couche cible | Exemple |
| --- | --- | --- |
| Transition autorisee selon le statut courant | Entite/agregat | Une animation peut-elle etre publiee ou cloturee ? |
| Coherence interne de dates ou de montants | Entite ou objet-valeur | Une date de fin doit etre posterieure au debut. |
| Regle associant plusieurs objets metier | Service de domaine | Eligibilite d'un lot par rapport aux participants acceptes. |
| Chargement, transaction et sauvegarde | Application | Charger l'animation, appeler `publier`, persister et commiter. |
| Autorisation et perimetre de tenant | Application, avec concepts d'acces du domaine si necessaire | Verifier que le gestionnaire agit sur sa commune. |
| Notification, audit et outbox | Application | Emettre l'evenement apres une transition reussie. |
| SQL, HTTP, Stripe, email, PDF ou stockage | Infrastructure | Repository SQLAlchemy ou moteur de rendu du flyer. |
| Projection de lecture sans invariant | Application | Dashboard ou Vision 360. |

### Regles de conception obligatoires

- Une entite ne doit pas exposer un changement de statut public sans verifier elle-meme la transition.
- Un invariant ne doit pas etre duplique entre API, service applicatif, batch et back-office.
- La couche application peut assembler les donnees necessaires a une decision, mais elle transmet ensuite
  des objets ou faits metier au domaine pour obtenir cette decision.
- Un service de domaine est sans etat technique et sans dependance a FastAPI, SQLAlchemy, Pydantic, Stripe,
  Brevo, ReportLab ou a un client reseau.
- Les objets ORM ne sont pas le modele de domaine et ne doivent pas recevoir les invariants par commodite.
- Toute exception a ce placement doit etre motivee dans la conception technique ou dans un ADR.

### Controle en revue de code

Pour toute condition ou exception ajoutee dans `app/application`, la revue doit poser la question suivante :

> Cette condition exprime-t-elle une orchestration technique ou une regle qui doit rester vraie quel que
> soit le point d'entree ?

Si elle doit rester vraie quel que soit le point d'entree, elle appartient au domaine. La pull request doit
alors contenir :

- le comportement dans une entite, un objet-valeur ou un service de domaine ;
- un test domaine sans base de donnees ni fournisseur externe ;
- un test applicatif verifiant l'orchestration, sans recopier l'algorithme metier dans ses fakes.

Une nouvelle Epic doit identifier, dans sa conception technique, les agregats modifies, les invariants et
les transitions avant de lister les services applicatifs ou les endpoints.

## Dette existante et trajectoire

La decision n'impose pas une reecriture globale immediate. La migration suit une regle de remise en ordre au
fil de l'eau : toute Epic qui modifie une regle existante doit profiter de cette modification pour la replacer
dans le domaine avant de l'etendre.

Les zones suivantes de `animation_locale` sont identifiees comme candidates prioritaires :

- autorisation des transitions de creation, modification, publication, demarrage et cloture ;
- coherence des dates et modification de la date de fin d'une animation en cours ;
- ouverture des inscriptions et possibilite de valider un passage ;
- eligibilite de publication, gel des participants et coherence des lots ;
- transitions des demandes de participation commercant et des commandes de lots ;
- calcul de l'etat fonctionnel du workflow.

Le rendu d'un flyer, l'appel au stockage documentaire et l'emission de notifications restent, eux, des
responsabilites applicatives ou techniques. En revanche, les faits autorisant leur generation et les donnees
metier figees doivent provenir du domaine.

## Consequences

- Les regles critiques disposent d'une source de verite unique.
- Les entites deviennent comportementales plutot que de simples conteneurs de donnees.
- Les tests domaine sont plus rapides et independants de SQLAlchemy.
- Les services applicatifs deviennent plus courts et lisibles, centres sur l'orchestration.
- Certaines evolutions demanderont un mapping domaine/ORM plus explicite.
- La dette existante sera reduite progressivement, sans refonte globale risquee.

## Alternatives considerees

- **Conserver des services applicatifs riches** : refuse, car les invariants restent disperses et dependants
  des points d'entree.
- **Placer les regles dans les modeles ORM** : refuse, car le domaine deviendrait dependant de SQLAlchemy et
  plus difficile a tester.
- **Effectuer une reecriture immediate de tous les domaines** : refuse, car le risque et le volume seraient
  disproportionnes ; la correction au fil des evolutions est retenue.
