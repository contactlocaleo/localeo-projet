# Backlog Epic 27 - Vision 360 commercant backoffice

## Synthese

- Criticite : `Haute`
- Statut : `Termine`
- Objectif : fournir au back-office une vue 360 d'un commercant selectionne par recherche, regroupant son referentiel, son activite commerciale, son profil public, ses coffrets actifs, ses validations recentes, ses revenus et ses alertes operationnelles.
- Decision produit : la vision 360 est une vue support/exploitation interne, differente du dashboard operationnel commercant de l'Epic 19 qui est destine au commercant authentifie.
- Decision technique : la vue doit agreger les donnees existantes sans creer une nouvelle source de verite analytique.
- Decision operationnelle : un operateur doit pouvoir rechercher un commercant par nom puis obtenir en une page les informations utiles pour comprendre son activite Localeo.
- Decision produit : afficher le `CA encaisse commercant`, le `montant reverse` et le `montant a reverser`.
- Decision produit : le `CA encaisse commercant` correspond au montant effectivement encaisse par le commercant via les reversements payes/executes, pas au prix client total des coffrets.
- Decision produit : inclure les messages support du commercant dans la V1.
- Decision produit : afficher les emails/SMS envoyes au commercant depuis la communication libre.
- Decision produit : limiter les listes recentes a 20 elements.
- Decision produit : ajouter une periode personnalisee avec dates de debut et fin.
- Decision produit : ajouter un raccourci `Contacter ce commercant` vers la communication libre, pre-remplie avec le commercant.
- Decision produit : inclure les documents/facturation utiles au support financier commercant.
- Decision produit : inclure les incidents et anomalies recentes.
- Decision produit : inclure l'activite back-office recente et permettre les notes internes.

## Probleme

Les informations d'un commercant sont aujourd'hui dispersees entre plusieurs vues back-office : fiche commercant, prestations, coffrets, profils commercants, achats, validations, reversements, emails/SMS, feedbacks, activites locales et demandes support.

Quand un operateur veut comprendre la situation d'un commercant, il doit naviguer entre plusieurs tables et reconstruire manuellement :

- quels coffrets actifs contiennent ses prestations ;
- quand son profil a ete modifie ou publie ;
- quelle activite commerciale recente il genere ;
- quels coffrets ou prestations ont ete recemment valides ;
- quel chiffre d'affaires ou montant reverse est associe a son activite ;
- quels points bloquent son referencement ou son exploitation.

Sans vue 360, le support commercant et le pilotage operationnel sont plus lents, moins fiables et plus dependants de la connaissance technique de l'operateur.

## Risque business

- Support commercant lent faute de vue consolidee.
- Difficultes a identifier les commercants actifs, performants ou en difficulte.
- Manque de visibilite sur la contribution d'un commercant au revenu Localeo.
- Risque de ne pas detecter rapidement un profil obsolere, non publie ou une offre inactive.
- Pilotage commercial moins efficace lors des relances partenaires.

## Risque technique

- Duplication de calculs deja presents dans les dashboards et use cases existants.
- Requetes back-office lourdes si les agregats ne sont pas limites et indexes.
- Ambiguite entre CA encaisse commercant, montant reverse, montant a reverser et revenu net Localeo.
- Exposition excessive de donnees client si les listes recentes ne sont pas masquees.
- Incoherence des indicateurs si les periodes et sources ne sont pas definies clairement.

## Perimetre MVP

- Ajouter une entree back-office `Vision 360 commercant`.
- Permettre de rechercher un commercant par nom de commerce.
- Permettre de selectionner un commercant dans les resultats.
- Afficher une fiche synthese du commercant :
  - statut ;
  - ville ;
  - type ;
  - contact operationnel ;
  - acces commercant existant ou non ;
  - compte connecte Stripe eligible ou non si disponible.
- Afficher les coffrets actifs contenant au moins une prestation du commercant.
- Afficher les prestations actives, brouillon/reference et suspendues du commercant.
- Afficher la derniere mise a jour du profil commercant :
  - date de derniere soumission ;
  - date de derniere publication ;
  - statut de publication ;
  - score de completion si disponible.
- Afficher les indicateurs d'activite du commercant :
  - jour courant ;
  - 7 derniers jours ;
  - 30 derniers jours ;
  - annee en cours ;
  - periode personnalisee.
- Afficher les derniers coffrets ou prestations valides chez le commercant.
- Afficher les derniers achats contenant une prestation du commercant, avec donnees client masquees.
- Afficher les derniers feedbacks rattaches au commercant si disponibles.
- Afficher les dernieres activites locales rattachees au commercant si disponibles.
- Afficher les messages support recents rattaches au commercant.
- Afficher les emails/SMS de communication libre envoyes au commercant.
- Afficher un raccourci `Contacter ce commercant` vers la page de communication libre avec le destinataire preselectionne.
- Afficher les documents/factures/reversements utiles au support financier commercant.
- Afficher les incidents et anomalies recentes :
  - paiements en erreur sur achats contenant le commercant ;
  - validations incoherentes ou annulees si disponible ;
  - emails/SMS en erreur ;
  - reversements bloques, en echec ou a traiter.
- Afficher l'activite back-office recente liee au commercant.
- Permettre de consulter et ajouter des notes internes back-office rattachees au commercant.
- Afficher les alertes operationnelles :
  - commercant non actif ;
  - aucune prestation active ;
  - aucun coffret actif ;
  - profil non publie ou en attente de moderation ;
  - compte bancaire manquant ;
  - validation recente en anomalie si disponible.
- Permettre de naviguer facilement depuis la vue 360 vers les elements rattaches au commercant :
  - fiche commercant ;
  - profil public et versions de profil ;
  - coffrets ;
  - prestations ;
  - achats ;
  - coffrets instances ;
  - validations ;
  - reversements ;
  - feedbacks ;
  - activites locales ;
  - emails/SMS ou communications rattachees si disponibles.

## Hors perimetre MVP

- Comparaison entre commercants.
- Segmentation commerciale avancee.
- Export Excel/PDF de la fiche 360.
- Graphiques analytiques complexes.
- Forecast ou scoring automatique de performance.
- Modification des donnees depuis la vue 360.
- Calcul comptable exhaustif du revenu net Localeo.
- Acces public ou acces commercant a cette vue.

## User Stories

1. `PRD-167` En tant qu'operateur back-office, je veux rechercher un commercant par nom afin d'ouvrir rapidement sa vue 360.
   - Statut : `Termine`
   - Resultat attendu : la recherche accepte le nom de commerce et retourne les commercants correspondants.
   - Resultat attendu : chaque resultat affiche nom, ville, statut et contact masque.

2. `PRD-168` En tant qu'operateur back-office, je veux consulter une fiche synthese du commercant afin d'identifier son etat operationnel en un coup d'oeil.
   - Statut : `Termine`
   - Resultat attendu : la fiche affiche statut, ville, type, contact, acces commercant et compte bancaire.
   - Resultat attendu : les donnees sensibles sont masquees quand l'affichage complet n'est pas necessaire.

3. `PRD-169` En tant qu'operateur back-office, je veux voir les coffrets actifs du commercant afin de comprendre dans quelles offres il est actuellement vendu.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les coffrets actifs contenant au moins une prestation active du commercant.
   - Resultat attendu : chaque coffret affiche nom, ville, prix, statut et nombre de prestations du commercant.

4. `PRD-170` En tant qu'operateur back-office, je veux voir l'etat des prestations du commercant afin d'identifier les offres actives, en brouillon ou bloquees.
   - Statut : `Termine`
   - Resultat attendu : les prestations sont regroupees par statut.
   - Resultat attendu : les prestations actives affichent leur montant de reversement si disponible.

5. `PRD-171` En tant qu'operateur back-office, je veux voir la derniere mise a jour du profil commercant afin de savoir si sa fiche publique est recente et publiee.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche le statut du profil, derniere soumission, derniere moderation, derniere publication et score de completion si disponible.
   - Resultat attendu : un profil en attente de moderation est signale.

6. `PRD-172` En tant qu'operateur back-office, je veux voir les indicateurs d'activite du commercant par periode afin de mesurer rapidement son activite recente.
   - Statut : `Termine`
   - Resultat attendu : les periodes jour courant, 7 jours, 30 jours et annee en cours sont affichees.
   - Resultat attendu : chaque periode affiche au minimum validations, prestations consommees, CA encaisse commercant, montant reverse et montant a reverser.

7. `PRD-173` En tant qu'operateur back-office, je veux voir les dernieres validations du commercant afin de comprendre son activite terrain recente.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les dernieres validations avec date, coffret, prestation, statut et email client masque.
   - Resultat attendu : un lien permet d'ouvrir la validation ou la `CoffretInstance` associee.

8. `PRD-174` En tant qu'operateur back-office, je veux voir les derniers achats contenant une prestation du commercant afin de comprendre la demande recente.
   - Statut : `Termine`
   - Resultat attendu : la vue liste les derniers achats rattaches aux coffrets contenant une prestation du commercant.
   - Resultat attendu : les donnees client sont masquees.

9. `PRD-175` En tant qu'operateur back-office, je veux voir les signaux qualitatifs recents du commercant afin de reperer les retours clients et activites visibles.
   - Statut : `Termine`
   - Resultat attendu : la vue affiche les derniers feedbacks moderes ou a moderer rattaches au commercant.
   - Resultat attendu : la vue affiche les dernieres activites locales rattachees au commercant si disponibles.

10. `PRD-176` En tant que responsable exploitation, je veux voir les alertes operationnelles du commercant afin de traiter les blocages prioritaires.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les alertes de referencement, profil, coffrets, prestations, compte bancaire et activite.
    - Resultat attendu : chaque alerte propose un lien vers la vue back-office pertinente.

11. `PRD-177` En tant que responsable produit, je veux que les indicateurs financiers soient clairement nommes afin d'eviter la confusion entre CA encaisse, montant reverse et montant a reverser.
    - Statut : `Termine`
    - Resultat attendu : le CA encaisse commercant est libelle comme montant effectivement encaisse via reversements payes/executes.
    - Resultat attendu : le montant reverse et le montant a reverser sont libelles distinctement selon la source disponible.

12. `PRD-178` En tant qu'operateur back-office, je veux naviguer facilement depuis la vue 360 vers les objets du commercant afin d'agir ou de verifier un detail sans refaire une recherche.
    - Statut : `Termine`
    - Resultat attendu : la synthese propose des liens directs vers la fiche commercant, le profil commercant, les prestations et les comptes bancaires.
    - Resultat attendu : chaque coffret, achat, `CoffretInstance`, validation, reversement, feedback ou activite locale affichee propose un lien vers sa fiche back-office.
    - Resultat attendu : les alertes operationnelles pointent vers l'ecran de correction pertinent quand il existe.

13. `PRD-179` En tant qu'operateur back-office, je veux voir les messages support et communications libres recentes du commercant afin de comprendre les derniers echanges avec Localeo.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les 20 derniers messages support rattaches au commercant.
    - Resultat attendu : la vue affiche les 20 derniers emails/SMS de communication libre envoyes au commercant.
    - Resultat attendu : chaque message ou communication propose un lien vers sa fiche back-office quand elle existe.

14. `PRD-180` En tant qu'operateur back-office, je veux filtrer les indicateurs sur une periode personnalisee afin d'analyser une fenetre commerciale ou support precise.
    - Statut : `Termine`
    - Resultat attendu : la vue accepte `date_debut` et `date_fin`.
    - Resultat attendu : les indicateurs de la periode personnalisee affichent validations, prestations consommees, CA encaisse commercant, montant reverse et montant a reverser.

15. `PRD-181` En tant qu'operateur back-office, je veux contacter le commercant depuis la vue 360 afin de passer rapidement de l'analyse a l'action.
    - Statut : `Termine`
    - Resultat attendu : un bouton `Contacter ce commercant` ouvre la communication libre avec le commercant preselectionne.
    - Resultat attendu : email et telephone du commercant sont pre-remplis depuis le referentiel.

16. `PRD-182` En tant qu'operateur back-office, je veux voir les documents et elements financiers du commercant afin de repondre aux questions de facturation ou reversement.
    - Statut : `Termine`
    - Resultat attendu : la vue expose les liens vers reversements, paiements de reversement, lots de paiement et documents/factures disponibles.
    - Resultat attendu : les montants distinguent `montant reverse` et `montant a reverser`.

17. `PRD-183` En tant qu'operateur back-office, je veux voir les incidents et anomalies recentes du commercant afin de prioriser les corrections.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les paiements en erreur, validations incoherentes, emails/SMS en erreur et reversements bloques ou en echec.
    - Resultat attendu : chaque anomalie propose un lien vers l'objet a diagnostiquer.

18. `PRD-184` En tant qu'operateur back-office, je veux voir l'activite back-office recente du commercant afin de comprendre les dernieres interventions internes.
    - Statut : `Termine`
    - Resultat attendu : la vue affiche les derniers evenements d'audit rattaches au commercant.
    - Resultat attendu : un lien permet d'ouvrir la liste d'audit filtree si disponible.

19. `PRD-185` En tant qu'operateur back-office, je veux ajouter des notes internes sur un commercant afin de conserver un contexte support ou commercial partage.
    - Statut : `Termine`
    - Resultat attendu : une note interne peut etre ajoutee depuis la vue 360.
    - Resultat attendu : les notes internes affichent auteur, date et contenu.
    - Resultat attendu : les notes internes restent strictement back-office.

## Regles de gestion

- La vue 360 est reservee au back-office.
- La recherche MVP se fait par nom de commerce.
- Les donnees client affichees dans les listes recentes sont masquees.
- La vue est en lecture seule.
- Les indicateurs financiers doivent distinguer :
  - CA encaisse commercant ;
  - montant reverse ;
  - montant a reverser ;
  - montant reverse effectivement traite si disponible.
- Le CA encaisse commercant correspond aux reversements payes/executes sur la periode.
- Le montant a reverser correspond aux mouvements ou reversements eligibles/non payes selon les donnees disponibles.
- Le montant reverse et le montant a reverser doivent etre affiches systematiquement quand les donnees sources existent.
- Les periodes standard sont :
  - aujourd'hui ;
  - 7 derniers jours glissants ;
  - 30 derniers jours glissants ;
  - annee civile en cours.
- Une periode personnalisee peut etre fournie par `date_debut` et `date_fin`.
- Les periodes personnalisees doivent etre bornees et validees pour eviter les requetes trop larges.
- Les validations sont rattachees au commercant via `validations_prestation.commercant_id` ou via les statuts de prestation si necessaire.
- Les achats sont rattaches au commercant si le coffret achete contient au moins une prestation du commercant.
- Une absence de donnees doit etre affichee comme un etat vide explicite, pas comme une erreur technique.
- Les calculs MVP peuvent etre reconstruits a la demande, avec listes recentes limitees a 20 elements.
- Les requetes de listes recentes doivent etre explicitement bornees a 20 elements.
- Les agregats de periode doivent utiliser des bornes de dates et eviter les scans non bornes.
- Les index necessaires sur dates, `commercant_id`, `coffret_id`, `achat_id` et statuts doivent etre verifies avant mise en production.
- Chaque element liste doit exposer un lien back-office direct quand une fiche admin existe.
- Les liens de navigation ne doivent pas exposer de token, QR ou secret dans l'URL.
- Les liens doivent ouvrir la fiche detail existante plutot qu'une nouvelle vue dediee si une vue SQLAdmin existe deja.

## Sources de donnees MVP

### Referentiel commercant

- `commercants`
- `villes`
- `types_commercants`
- `identifiants_commercant`
- `comptes_bancaires_commercant`

### Catalogue et coffrets

- `prestations_coffret`
- `coffrets`
- `types_coffrets`
- `statuts_prestation_coffret_instance`
- `coffrets_instances`

### Activite commerciale

- `achats_coffret`
- `validations_prestation`
- `transactions_validation`
- `mouvements_reversement`
- `reversements`
- `lignes_reversement`

### Profil, contenu et signaux qualitatifs

- `profils_commercants`
- `profils_commercants_versions`
- `feedbacks_prestation`
- `activites_locales`
- `messages_contact`
- `emails_sortants`
- `sms_sortants`
- `evenements_audit`
- notes internes commercant a creer si aucune table existante ne convient

## Back-office cible

### Page de recherche

- `GET /admin/vision-360-commercant`
- Parametres :
  - `q` : recherche par nom de commerce.

### Page detail

- `GET /admin/vision-360-commercant/{commercant_id}`
- Sections attendues :
  - synthese ;
  - alertes ;
  - raccourcis operationnels ;
  - activite par periode ;
  - coffrets actifs ;
  - prestations ;
  - profil public ;
  - validations recentes ;
  - achats recents ;
  - feedbacks et activites ;
  - messages support et communications libres ;
  - documents/facturation ;
  - incidents/anomalies ;
  - activite back-office ;
  - notes internes ;
  - liens operationnels.

## Contrat de donnees cible

```json
{
  "commercant": {
    "id": "uuid",
    "nom": "Nom commerce",
    "statut": "ACTIF",
    "ville": "Ville",
    "type": "Restaurant",
    "contact_email_masque": "co***@example.com",
    "contact_telephone_masque": "06***12"
  },
  "alertes": [],
  "liens_operationnels": {
    "fiche_commercant": "/admin/commercant-orm/details/uuid",
    "profil_commercant": "/admin/profil-commercant-orm/details/uuid",
    "prestations": "/admin/prestation-coffret-orm/list?..."
  },
  "activite": {
    "aujourdhui": {
      "validations": 0,
      "prestations_consommees": 0,
      "ca_encaisse_commercant": 0,
      "montant_reverse": 0,
      "montant_a_reverser": 0
    },
    "sept_jours": {},
    "trente_jours": {},
    "annee_en_cours": {},
    "periode_personnalisee": {}
  },
  "coffrets_actifs": [],
  "prestations": [],
  "profil": {},
  "validations_recentes": [],
  "achats_recents": [],
  "signaux_qualitatifs": {},
  "messages_support_recents": [],
  "communications_libres_recentes": [],
  "documents_financiers": [],
  "anomalies_recentes": [],
  "activite_backoffice_recente": [],
  "notes_internes": []
}
```

## Lots d'implementation

### Lot 1 - Cadrage donnees et recherche

- Definir le contrat de reponse de la vision 360.
- Ajouter la recherche commercant par nom.
- Ajouter les regles de masquage email/telephone.
- Ajouter les limites de listes recentes.

### Lot 2 - Agregats referentiel/catalogue

- Charger la fiche commercant.
- Charger coffrets actifs et prestations par statut.
- Charger l'etat du profil commercant.
- Calculer les alertes referencement/profil/catalogue.

### Lot 3 - Agregats activite et financiers

- Calculer les periodes jour, 7 jours, 30 jours, annee.
- Ajouter la periode personnalisee `date_debut` / `date_fin`.
- Calculer validations et prestations consommees.
- Calculer CA encaisse commercant, montant reverse et montant a reverser.
- Distinguer les montants reverses effectivement traites des montants a reverser.

### Lot 4 - Listes recentes et signaux

- Lister validations recentes.
- Lister achats recents.
- Lister feedbacks recents.
- Lister activites locales recentes.
- Lister messages support recents.
- Lister emails/SMS de communication libre recents envoyes au commercant.
- Lister documents et elements financiers recents.
- Lister incidents et anomalies recentes.
- Lister activite back-office recente.
- Ajouter les liens vers les vues back-office existantes.
- Ajouter les liens detail sur chaque ligne affichable.

### Lot 5 - UI back-office

- Ajouter la vue `Vision 360 commercant`.
- Ajouter la page recherche.
- Ajouter la page detail lisible pour un operateur non technique.
- Ajouter etats vides, alertes et liens d'action.
- Ajouter une zone de raccourcis operationnels vers les principales fiches du commercant.
- Ajouter le bouton `Contacter ce commercant`.
- Rendre chaque carte/liste navigable vers l'objet source quand il existe.

### Lot 6 - Notes internes

- Definir le modele de note interne commercant si aucune table existante ne convient.
- Ajouter l'ajout de note depuis la vue 360.
- Afficher les 20 dernieres notes internes.
- Auditer la creation de note.

### Lot 7 - Tests et performance

- Tester la recherche.
- Tester les agregats par periode.
- Tester la periode personnalisee.
- Tester le masquage des donnees client.
- Tester les etats vides.
- Tester les liens operationnels.
- Tester l'ajout de note interne.
- Verifier les temps de reponse sur un commercant avec beaucoup d'achats/validations.

## Definition of Done

- Un operateur peut rechercher un commercant par nom.
- Un operateur peut ouvrir une vue 360 d'un commercant.
- La vue affiche synthese, alertes, coffrets actifs, prestations, profil, activite par periode, validations recentes et achats recents.
- La vue affiche messages support et communications libres recentes.
- La vue affiche documents financiers, anomalies recentes, activite back-office et notes internes.
- Un bouton permet de contacter le commercant via la communication libre pre-remplie.
- La vue permet de naviguer vers les fiches back-office des objets affiches.
- Les indicateurs financiers affichent CA encaisse commercant, montant reverse et montant a reverser.
- Une periode personnalisee est disponible.
- Les donnees client sensibles sont masquees.
- La vue est en lecture seule et reservee au back-office.
- Les etats vides sont explicites.
- Les tests couvrent recherche, agregats, masquage et etats vides.
- Les listes recentes sont limitees a 20 elements.

## Points arbitres

- Afficher systematiquement `CA encaisse commercant`, `montant reverse` et `montant a reverser`.
- Le CA encaisse commercant correspond aux reversements payes/executes.
- Inclure les messages support du commercant dans la V1.
- Afficher les emails/SMS envoyes au commercant depuis la communication libre.
- Limiter les listes recentes a 20 elements.
- Ajouter les periodes personnalisees.
- Ajouter un raccourci `Contacter ce commercant`.
- Inclure documents/facturation, anomalies recentes, activite back-office et notes internes.
