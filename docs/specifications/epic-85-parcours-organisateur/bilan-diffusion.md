# Consulter et partager le bilan d’une animation

**E85-EVO-BILAN-DIFFUSION · 27 novembre 2026**

Le bilan s’adresse au gestionnaire qui suit l’édition et prépare un compte rendu
pour les commerces, la mairie ou ses partenaires. L’ancien écran rassemble les
chiffres clés et les exports. Le PDF détaillé inclut les verbatims et l’audit.
Le nouvel écran met en avant les résultats à lire et le rapport à partager.

## Parcours du gestionnaire

Dans **Bilan → Résultats**, ou dans **Participation → Bilan provisoire** pendant
l’animation, le gestionnaire retrouve la période couverte, la date d’observation
et les résultats principaux. Il peut ensuite examiner la progression, la
satisfaction, les lots et les commerces selon le jeu et les données disponibles.
Les vues **Objectifs**, **Origine des inscriptions**, **Commentaires** et
**Comparaison** restent accessibles depuis la navigation de la fiche. Une
actualisation concerne les résultats de l’édition et préserve les vues et leur
navigation. La version du bilan reste provisoire jusqu’à la fin de gestion.

**Télécharger le bilan PDF** ouvre le téléchargement du rapport à partager. Le
menu des autres exports propose le **PDF avec annexes internes** et le CSV. Le
backend vérifie `animation:exporter` ainsi que l’organisation et la commune
actives pour chaque PDF. Le gestionnaire choisit les destinataires après le
téléchargement.

## Plan du rapport PDF

- **Synthèse** avec édition, commune, repères de dates, état provisoire ou
  définitif, principaux résultats, constats et sommaire.
- **Participation au fil du temps** avec graphique, lecture des jours de plus
  forte activité et tableau des inscriptions et passages encore valides. Les
  dates sont civiles en heure de Paris. Les périodes longues sont regroupées
  en intervalles contigus et explicitement datés. Les totaux couvrent les mêmes
  populations que le bilan. Une annulation cesse de compter au jour de la
  validation d’origine. Le graphique couvre les dates d’activité et la fenêtre
  entre publication et clôture (ou la date d’observation), y compris les jours
  sans activité enregistrée.
- **Résultats et objectifs** avec progression, qualification, couverture,
  objectifs chiffrés et écarts calculables. Les états du tirage distinguent une
  attente, une indisponibilité et un résultat confirmé avec zéro gagnant.
- **Commerces et lots** selon les mesures disponibles, avec les passages, les
  commerces actifs et leur classement, l’envoi et la remise des gains ainsi que
  la consommation des coffrets et les montants constatés lorsque cela s’applique.
- **Diffusion et satisfaction** avec inscriptions attribuées, sans support ou
  hors collecte, ouvertures par support, moyenne, part des notes 4 et 5 et nombre
  de répondants volontaires. Le rapport explique la couverture des mesures et
  leurs limites d’interprétation pour les partenaires.

Les constats s’appuient sur les chiffres réellement disponibles. Une mesure
inconnue, une mesure sans objet et un zéro observé ont des libellés distincts.
Les passages attestent une activité enregistrée. Le montant réinjecté couvre
les prestations de coffrets consommées. Les ouvertures de supports comptent des
événements, et les réponses volontaires couvrent les seuls répondants.

Le PDF A4 reprend le bleu nuit et le repère orange de la charte Localeo
Animation. Il utilise des titres, un sommaire avec liens, des signets, des textes
sélectionnables, des en-têtes de tableau répétés, des contrastes et des légendes
explicites. Le tableau rend lisibles les mêmes valeurs que le graphique. La
version à partager contient uniquement des résultats agrégés, y compris les noms
des commerces et des supports de diffusion. Les verbatims et l’audit sont dans
les annexes de la version interne.

## Contrat et traçabilité

Backend projette les données par édition dans l’instantané `REPEATABLE READ`
existant et rend le fichier après la transaction. Les règles d’éligibilité, de
validation et de tirage continuent de provenir de leurs propriétaires métier.
La nouvelle route `GET /protected/animation-locale/animations/{animation_id}/bilan/rapport.pdf`
retourne le PDF à partager. `bilan/export.pdf` conserve le rôle de PDF interne.
Les deux réponses sont privées et non mises en cache. La borne synchrone et le
refus `EXPORT_DIFFERE_REQUIS` s’appliquent aux listes exportées. La version à
partager ne charge pas les deux listes internes. Une version ancienne du serveur
rend la nouvelle route indisponible jusqu’au déploiement du backend correspondant.

| Critère | Comportement | Preuve attendue |
| --- | --- | --- |
| E85-CA-21 | Lire les résultats et choisir le bon export sur mobile et ordinateur. | Recette navigateur Bilan avec API synthétique, navigation, zoom, focus, états de chargement ou d’erreur et trois téléchargements. |
| E85-CA-22 | Retrouver les inscriptions et passages valides à leur jour de Paris et rapprocher les totaux du bilan. | Test PostgreSQL sur plusieurs dates, validations non valides, périmètre et borne. Vérification du rendu des petits et grands intervalles. |
| E85-CA-23 | Comprendre et présenter les résultats d’une édition, leurs objectifs et la couverture. | PDF lus et rendus, contrôles de texte, liens et signets, cas avec données et historique lacunaire. |
| E85-CA-24 | Partager le rapport agrégé et conserver les annexes pour son usage interne. | Tests API et application pour les deux documents, droits, instantané, bornes et absence de données individuelles dans le rapport à partager. |

Le [guide Animation](../../produit/formation/animation/guide-quotidien-animation.md)
couvre ce geste et ses deux PDF. Le guide Commerçant n’a pas de parcours
d’export du bilan organisateur. Les données, migrations, variables et le
générateur de démonstration existants suffisent, car les mesures reposent sur
les participations et validations déjà enregistrées. La vérification de diffusion
associe le backend et le portail Animation de la même livraison.
