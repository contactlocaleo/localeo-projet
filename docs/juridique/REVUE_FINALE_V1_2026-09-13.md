# Revue finale du corpus juridique Localeo V1

Relecture du 13 septembre 2026 — 16 PDF, 69 pages.

**Mise à jour après correction :** quatre PDF ont depuis été révisés en version 1.1 ; le corpus compte maintenant 70 pages. Le [suivi des corrections](SUIVI_CORRECTIONS_V1_2026-09-13.md) précise les changements, les décisions retenues et les points restant ouverts. Les constats ci-dessous décrivent le corpus au moment de la revue initiale.

**Conclusion : le corpus couvre l'essentiel et la simplification du contrat commerçant est cohérente. Je ne recommande pas de supprimer un des seize documents sans reprendre son contenu utile ailleurs. En revanche, la publication des PDF ne suffit pas encore à rendre les parcours conformes à ce qu'ils annoncent. Les priorités sont la rétractation en ligne, la preuve et la remise des conditions de vente, l'accessibilité compte tenu du périmètre déjà retenu, puis les compléments contractuels ciblés B2B et RGPD commerçant.**

Les textes ont été lus intégralement, répartis entre trois volets juridiques, puis rapprochés des dépôts locaux backend, Marketplace/Live, Pro et Animation. Des pages de tableaux et la fiche commerçant ont aussi été contrôlées visuellement, sans défaut de mise en page majeur sur cet échantillon. Aucune modification des PDF, des applications ou des données déployées n'a été effectuée.

Les constats techniques portent sur les espaces de travail locaux, pas sur une recette de production. Une pièce absente du dossier V1 peut exister ailleurs : les réserves de cette nature sont signalées comme telles. Cette revue n'atteste pas l'adhésion au médiateur, les contrats fournisseurs, les purges exécutées ou l'accessibilité réelle des interfaces.

Les décisions déjà prises sont conservées : Découverte à **390 € HT**, Essentielle à **990 € HT** ; régime **BUM des coffrets SOLO et MULTI** tenu pour confirmé ; un contrat commerçant avec fiche intégrée, signé en deux exemplaires ; aucune ventilation fiscale des prestations imposée à l'avance.

La synthèse interne précédente, examinée lors de la revue, consigne également **l'adhésion confirmée au médiateur Avenir Conso** et **l'absence d'exemption microentreprise pour l'accessibilité**. Cette revue reprend ces décisions ; elle ne les remet pas en attente d'une nouvelle confirmation. La preuve d'adhésion reste à conserver et le contrôle de l'accessibilité reste à réaliser ou à documenter s'il l'a déjà été.

## 1. Points à traiter en priorité

### 1.1 Rétractation Marketplace : la promesse documentaire n'est pas mise en œuvre dans le code inspecté

**Constat certain sur les fichiers inspectés — priorité avant de considérer le parcours de vente prêt.**

Les CGV, article 8, page 4, et le formulaire, page 2, annoncent une fonctionnalité de rétractation en ligne. La route `/retractation` de Marketplace affiche actuellement une page documentaire et son PDF. Aucun parcours public de déclaration, de confirmation et d'accusé de réception n'a été identifié. Les remboursements du back-office ne remplissent pas cette fonction pour le client.

Depuis le **19 juin 2026**, les nouveaux contrats de consommation conclus à distance par interface en ligne doivent, lorsqu'un droit de rétractation est ouvert, permettre son exercice par une fonctionnalité gratuite. Cette obligation générale ne se limite pas aux services financiers, malgré le titre de l'ordonnance qui l'a introduite. [Code de la consommation, article L. 221-21](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053310520/2026-06-24).

**Action :** proposer une entrée visible, utilisable par un acheteur sans compte, permettant d'identifier la commande, de déclarer puis confirmer sa rétractation. Envoyer un accusé conservable avec le contenu de la demande et sa date/heure. Garder le formulaire PDF et le courriel comme autres moyens utilisables. Ajouter l'adresse précise de la fonction dans les textes. Les modalités sont définies par [l'article D. 221-5](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053303365/2026-07-27).

### 1.2 Achat particulier : compléter la preuve d'acceptation et la remise du dossier contractuel

**Écart constaté dans le parcours local — priorité avant validation de la vente en ligne.**

Le checkout indique que l'acheteur reconnaît avoir consulté les CGV et la politique de confidentialité. Sa requête ne transmet pas d'acceptation/version des CGV et le schéma backend ne les enregistre pas dans ce chemin. Les conditions de crédit B2B présentes ailleurs ne constituent pas cette preuve.

Le courriel de confirmation inspecté joint le reçu, mais aucune remise des CGV applicables et du formulaire de rétractation n'a été repérée. Les CGV, article 3, page 2, prévoient pourtant une confirmation sur support durable. La présence d'un PDF sur le site ne démontre pas sa remise au client. [Code de la consommation, article L. 221-13](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563210/2025-03-18).

**Action :** recueillir un acte d'acceptation clair des CGV, lié à la commande et à la version exacte présentée. Une case dédiée non précochée est une solution simple de preuve, sans être une formalité universellement imposée sous cette forme. Remettre ensuite le récapitulatif, les CGV acceptées et le formulaire, idéalement en pièces jointes. Archiver le contenu applicable et la trace de remise. Un lien vers une page courante modifiable ne suffit pas à prouver la version remise.

La politique de confidentialité informe sur les traitements : elle ne doit pas être présentée comme un consentement général obligatoire à tous les usages des données.

### 1.3 Vente de coffrets aux entreprises hors Animation : couverture contractuelle manquante dans ce corpus

**Complément nécessaire si ce parcours est ouvert et qu'aucun contrat applicable n'existe ailleurs.**

Les CGV Marketplace, article 1, page 1, concernent les consommateurs et renvoient les achats professionnels à leurs conditions particulières. Les Conditions particulières Animation couvrent l'organisateur et ses lots ; elles ne couvrent pas automatiquement les cadeaux d'entreprise ordinaires.

Le code comporte un parcours `CommandeProPage`. Les conditions dites d'achat professionnel retrouvées portent sur le **crédit d'achat**. Elles ne couvrent pas, à elles seules, l'ensemble de la vente B2B.

**Action :** ajouter des conditions de vente de coffrets aux professionnels, ou une section B2B explicite dans un document existant. Traiter commande, prix et justificatifs BUM, paiement, bénéficiaires, activation/validité, annulation, indisponibilité et responsabilités. Les conditions de crédit restent un complément lorsque ce financement est utilisé. Ne pas appliquer par défaut les CGV consommateurs à ce parcours alors qu'elles l'excluent.

### 1.4 Assistant de facturation Pro : compléter les clauses de sous-traitance de données

**Complément ciblé avant usage du service avec des données personnelles, sauf accord applicable déjà conclu ailleurs.**

Le contrat commerçant, articles 10–11, page 5, prévoit un outil de préparation de facture et le dépôt d'une copie. Il distingue correctement les responsabilités propres de Localeo et du commerçant, mais ne contient pas l'accord complet de sous-traitance RGPD pour le service fourni sur instructions du commerçant.

Ce périmètre est déjà reconnu par l'Annexe A : T9 page 2 et conservation des documents du commerçant page 4. L'Annexe B, paragraphe 4, page 2, présuppose également l'autorisation contractuelle des sous-traitants ultérieurs. Le code de l'assistant persiste les brouillons, dont les coordonnées du destinataire. La seule annexe article 28 du dossier V1 concerne les partenaires Animation.

**Action :** intégrer au contrat commerçant les clauses article 28 relatives à cette préparation/hébergement : objet, durée, données et personnes, instructions, confidentialité, sécurité, assistance, incidents, prestataires ultérieurs, audit et restitution/suppression. Une annexe acceptée est possible, mais l'intégration préserve la simplicité du dossier papier. La qualification dépend du service effectivement rendu. [CNIL, qualification des rôles](https://www.cnil.fr/fr/rgpd-comment-bien-identifier-son-role), [RGPD, article 28](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4).

Cela **n'impose pas un mandat de facturation** : le commerçant peut continuer à contrôler et émettre ses propres factures. Les traitements que chaque partie détermine pour ses finalités propres restent distincts.

### 1.5 Animation : remettre le dossier complet et figer les règles acceptées

**Documents génériques utiles ; compléments propres à chaque contrat/opération et preuve à organiser.**

- Les Conditions particulières, articles 1 et 3, pages 1–2, renvoient au récapitulatif accepté de la souscription. Il faut effectivement produire ce récapitulatif : partenaire, signataire habilité, offre, territoire, droits, dates, prix/taxes, paiement et options. Remettre ensemble ce récapitulatif, les Conditions particulières et l'annexe données.
- L'annexe données, article 5, page 3, vise une liste de sous-traitants **communiquée avec le contrat**. Fournir cette liste datée à partir des fournisseurs effectivement vérifiés. Le registre B interne ne constitue pas automatiquement la liste contractuelle remise au partenaire.
- Le règlement général suppose une **fiche d'opération** complète : organisateur/contact, éligibilité, dates/heures, conditions de participation, qualification, gagnants/suppléants, lots, valeur/validité/restrictions, remise et information sur les données de l'organisateur. Le participant doit voir ce dossier avant inscription.
- La page publique affiche un règlement et une case obligatoire distincte des notifications. En revanche, le chemin backend examiné conserve la date d'acceptation sans rattacher explicitement la participation à la version du règlement et de la fiche. Conserver leur contenu exact ou une référence immuable à leur archive. La date seule ne prouve pas ce qui a été accepté.

L'invitation des commerçants possède déjà une trace de configuration et de contenu présenté : il faut conserver cette distinction avec le parcours des participants publics.

### 1.6 Accessibilité : conserver la déclaration, traiter l'état réel du service

**Priorité opérationnelle, compte tenu de l'absence d'exemption déjà consignée.**

La déclaration, article 2, page 1, annonce honnêtement l'absence d'audit et ne revendique pas de conformité démontrée. Ce texte n'établit pas que toutes les fonctions sont inaccessibles ; il ne prouve pas non plus le respect des obligations applicables.

**Action :** contrôler les parcours essentiels, notamment consultation d'offre, commande, paiement, rétractation et documents, corriger les obstacles, puis publier une information correspondant aux résultats réels. Réunir les preuves déjà disponibles le cas échéant. La création d'un second PDF d'accessibilité ne résoudrait pas ce sujet. Le régime commerce électronique et le champ propre de l'article 47/RGAA doivent être distingués pour déterminer les formalités exactes ; l'exemption microentreprise n'est pas à rouvrir ici.

## 2. Corrections et ambiguïtés dans les textes

| Document et emplacement | Constat | Correction recommandée |
|---|---|---|
| Annexe C, §4, p. 2 | Renvoi aux arrondis de l'**Annexe D**, absente du corpus final | Remplacer le renvoi par l'article 7 du contrat commerçant et sa fiche intégrée. Ne pas recréer l'Annexe D. |
| Annexe C, §1, p. 1 | Elle dit compléter le contrat et son récapitulatif tarifaire, alors qu'elle est classée interne et n'est pas automatiquement incorporée au contrat fusionné | La conserver comme procédure interne explicite ; laisser les engagements opposables dans le contrat. Si elle devait devenir contractuelle, il faudrait l'identifier et la remettre comme telle. |
| Annexe C, §1 et §3, p. 1 | Le déroulement général active les droits après paiement ; l'exclusion vise les abonnements Animation sans préciser le cas des lots | Préciser que ce déroulement vise la vente standard et distinguer les lots réservés au paiement, activés lors de l'envoi au gagnant. |
| CGV Marketplace, art. 11, p. 6 | La qualification BUM reste conditionnelle, contrairement au contrat commerçant et au périmètre confirmé | Dire explicitement que les coffrets SOLO et MULTI concernés sont des BUM. Conserver la distinction acquisition du bon / prestation / commission, sans TVA de prestation inventée à l'avance. |
| Conditions particulières Animation, art. 9, p. 4 ; règlement, art. 7 et 9, p. 3–4 | Le sort financier des lots payés mais jamais attribués ou non réclamés après clôture reste indéterminé | Choisir une règle claire : report, crédit, remboursement ou autre régime convenu, avec délai, conditions et traitement des remplacements. Les textes actuels ne permettent pas de choisir entre ces solutions. |
| Politique de confidentialité, art. 5, p. 3–4 ; notice Live, art. 7, p. 3 | Les transferts internationaux sont décrits par des mécanismes possibles, sans rattachement assez précis aux traitements et destinataires réels | Ajouter un tableau public bref des destinations et garanties effectivement applicables, établi depuis les dossiers B/E. Ne pas annoncer une certification non vérifiée. |
| Politique cookies, art. 3 et 5, p. 2–3 | Un choix analytics est décrit alors qu'aucune mesure d'audience n'est active | Simplifier ce réglage et son explication tant que le service est absent. Garder l'information sur les stockages nécessaires. |

Le défaut de précision sur les transferts ne démontre pas un transfert illicite. Il faut distinguer la qualité de l'information publique de la validité des mécanismes réellement conclus. Les recommandations de transparence demandent une information suffisamment identifiable sur le mécanisme et les pays concernés. [CNIL/G29, lignes directrices sur la transparence, annexe p. 45–46](https://www.cnil.fr/sites/cnil/files/atoms/files/wp260_guidelines-transparence-fr.pdf).

Les arrondis, les frais Stripe, le régime BUM et les droits conservés après fin du partenariat sont déjà traités dans le contrat commerçant. Sa fiche décrit les prestations et commissions sans exiger une composition fiscale inconnue à l'avance : conserver cette logique.

## 3. Documents manquants, documents supprimables

### Compléments réellement utiles

| Complément | Quand est-il nécessaire ? | Forme la plus simple |
|---|---|---|
| Conditions d'achat de coffrets B2B hors Animation | Si ce parcours est commercialisé sans autre contrat applicable | Document court dédié ou section professionnelle explicite |
| Clauses RGPD du service documentaire/facturation commerçant | Si Localeo traite des données personnelles pour le compte du commerçant | Intégration au contrat unique ou annexe acceptée |
| Récapitulatif de souscription/commande Animation | À chaque engagement du partenaire | Devis, bon de commande ou dossier généré et accepté |
| Fiche d'opération et règlement complet | Pour chaque animation ouverte aux participants | Page lisible et version archivée/téléchargeable |
| Liste des sous-traitants autorisés pour Animation | Avec le contrat et lors des changements prévus par l'annexe | Extrait daté des dossiers fournisseurs vérifiés |
| Information contextuelle sur les données | Formulaires et premier contact avec un bénéficiaire dont les coordonnées viennent d'un tiers | Texte court et lien vers la politique/notice pertinente |
| Dossiers de preuve et registre des activités réalisées pour les clients | Pour documenter la réalité de la gouvernance RGPD | Registre interne vivant et pièces associées, sans nouveau PDF public |

Pour la collecte indirecte, le premier courriel au bénéficiaire doit notamment permettre d'identifier Localeo, l'origine des coordonnées, la finalité et l'accès à ses droits. La politique générale ne remplace pas cette information au bon moment. Pour Animation, identifier aussi l'organisateur responsable des traitements qui lui appartiennent. [CNIL, information des personnes](https://www.cnil.fr/fr/conformite-rgpd-information-des-personnes-et-transparence).

L'Annexe A indique qu'un registre distinct est tenu pour les opérations réalisées pour le compte des partenaires. Le PDF seul ne prouve pas que ce registre et ses entrées clients existent. Vérifier ce dossier et compléter l'Annexe A ou son registre associé, sans publier l'identité des clients ni les informations de sécurité. [CNIL, registre des activités](https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement).

### Décision sur chacun des seize PDF

Les noms ci-dessous sont abrégés pour la lecture ; les liens visent les fichiers exacts de V1.

| Document | Pages | Décision et destinataire |
|---|---:|---|
| [Mentions légales](<communs/LOCALEO - Mentions Légales - V1.pdf>) | 2 | **Conserver**, public sur les quatre plateformes |
| [Politique de confidentialité](<communs/LOCALEO - Politique de Confidentialité - V1.pdf>) | 6 | **Conserver**, socle public commun ; préciser les transferts |
| [Politique cookies](<communs/LOCALEO - Politique de Cookies - V1.pdf>) | 3 | **Conserver l'information** ; fusion possible dans la confidentialité avec accès direct au chapitre, mais pas suppression des stockages décrits |
| [Déclaration d'accessibilité](<communs/LOCALEO - Déclaration d'accessibilité - V1.pdf>) | 2 | **Conserver une page publique**, contrôler/corriger les parcours selon le régime applicable et l'absence d'exemption déjà retenue |
| [CGU Live](<live/LOCALEO - Conditions Générales d'Utilisation Localeo Live - V1.pdf>) | 3 | **Conserver**, distinctes des conditions de vente |
| [Notice de confidentialité Live](<live/LOCALEO - Notice de confidentialité Localeo Live - V1.pdf>) | 5 | **Conserver**, informations propres au carnet, installations, sauvegarde et notifications ; fusion possible seulement en reprenant ces détails |
| [CGV Marketplace](<marketplace/LOCALEO - Conditions Générales de Vente Marketplace - V1.pdf>) | 7 | **Conserver**, public et dossier de commande |
| [Formulaire de rétractation](<marketplace/LOCALEO - Formulaire de Rétractation Localeo - V1.pdf>) | 2 | **Conserver**, téléchargement direct et remise à l'acheteur, en complément de la fonction en ligne |
| [Contrat commerçant avec fiche](<commercant/LOCALEO - Contrat de Partenariat Commerçant avec fiche prestations - V1.pdf>) | 8 | **Conserver comme seul dossier commerçant à signer**, sous réserve du complément RGPD ciblé |
| [Conditions particulières Animation](<animation/LOCALEO - Conditions particulières Localeo Animation - V1.pdf>) | 5 | **Conserver**, avec récapitulatif accepté |
| [Annexe données Animation](<animation/LOCALEO - Annexe protection des données partenaire Animation - V1.pdf>) | 5 | **Conserver**, accord contractuel distinct de l'information publique |
| [Règlement type d'animation](<animation/LOCALEO - Règlement type d'une animation - V1.pdf>) | 5 | **Conserver comme socle**, à compléter par la fiche propre à chaque opération |
| [Annexe A — traitements et conservation](<interne/Annexe A - Registre simplifié des traitements et tableau de conservation des données - V1.pdf>) | 6 | **Conserver en interne** et maintenir le registre réel |
| [Annexe B — sous-traitants](<interne/Annexe B - Registre des sous-traitants - V1.pdf>) | 3 | **Conserver en interne** ; communiquer les extraits contractuels utiles |
| [Annexe C — flux financiers](<interne/Annexe C - Gestion des Flux financiers Localeo - V1.pdf>) | 4 | **Conserver comme procédure interne**, sans signature commerçant supplémentaire ; corriger son statut et le renvoi D |
| [Annexe E — DPF/CCT](<interne/Annexe E - Vérification DPF CCT - V1.pdf>) | 3 | **Conserver le contrôle et les preuves** ; fusion possible dans le dossier fournisseurs B pour réduire le nombre de fichiers |

**À ne pas réintroduire :** Annexe D tarifaire, ancien contrat commerçant séparé, ancienne fiche autonome utilisée simultanément avec le contrat fusionné. Ils ajouteraient des doublons et des risques de divergence. Aucun besoin identifié de créer des CGU Pro générales supplémentaires si le contrat unique couvre l'utilisation de Pro ; le complément nécessaire concerne le service de traitement de données, pas un nouveau contrat général.

On peut réunir les Conditions particulières, le récapitulatif et l'annexe données Animation dans un seul dossier à accepter. Cela simplifie la remise sans supprimer les clauses. Les annexes A/B/C/E ne sont pas des documents à faire signer systématiquement aux partenaires.

## 4. Points à vérifier dans le fonctionnement réel

Ces points ne sont pas des non-conformités déduites de l'absence d'un justificatif dans V1.

| Sujet | Vérification utile |
|---|---|
| Prestations utilisées pendant les quatorze premiers jours | Les CGV art. 8 excluent à raison une renonciation automatique par QR. Organiser, lorsqu'elle est pertinente au montage, la demande expresse d'exécution anticipée et l'information sur ses conséquences. Traiter le cas acheteur différent du bénéficiaire. Aucun recueil dédié n'a été repéré dans le parcours examiné. |
| Médiation Avenir Conso | L'adhésion est consignée comme confirmée dans la synthèse précédente ; conserver le justificatif et maintenir les coordonnées. Aucun nouveau document à créer pour rouvrir ce point. |
| Fournisseurs et transferts | B/E décrivent une méthode et des pièces à tenir ; vérifier les entités contractantes, services, pays/régions, DPA acceptés, garanties DPF/CCT réellement applicables et date de contrôle. Ne pas confondre une liste de documents à réunir avec les justificatifs réunis. |
| Durées de conservation | Vérifier les tâches réellement exécutées : Live 90 jours, données et accès Animation selon leur catégorie, archives légales, fichiers et sauvegardes. L'existence d'un batch ne prouve pas son exécution ni l'effacement du stockage. |
| Notifications et courriels | Vérifier catégories, permission du navigateur, retrait, distinction gestion/marketing et paramétrage des pixels. Les textes distinguent correctement ces sujets. |
| Accessibilité | L'exemption microentreprise a déjà été écartée selon la synthèse précédente. Contrôler/corriger les interfaces et conserver les résultats ; préciser les formalités relevant du régime applicable. Une déclaration d'absence d'audit ne suffit pas. |

Les règles d'exécution anticipée et les exceptions de rétractation doivent être appliquées à l'opération concernée, pas déduites de la simple livraison du bon. [Articles L. 221-25](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563179/2026-06-24) et [L. 221-28](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563170/2026-05-04).

L'absence d'exemption retenue pour Localeo conduit à traiter les obligations d'accessibilité du commerce électronique. Leur périmètre et leurs formalités ne se confondent pas avec ceux de l'article 47/RGAA ; vendre à une commune ne tranche pas à lui seul ce second statut. [Code de la consommation, L. 412-13](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000047284913/2024-01-13), [DGCCRF, champ et exemptions](https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/la-nouvelle-directive-europeenne-accessibilite-pour-des-produits-et-des-services-accessibles-aux-personnes-en-situation), [champ RGAA](https://accessibilite.numerique.gouv.fr/obligations/champ-application/).

Les autorisations d'image et règles adaptées aux mineurs ne sont à ajouter que si ces usages sont ouverts. Le standard Animation prévoit dix-huit ans et un accord distinct pour l'image. De même, une offre de voyage/séjour relevant du Code du tourisme demanderait une vérification spécifique avant commercialisation ; la mention d'hébergement parmi les exemples des CGV ne prouve pas que le catalogue le propose. [DGCCRF, coffrets cadeaux](https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/coffrets-cadeaux-que-faire-en-cas-de-deconvenue).

## 5. Mise à disposition sur les quatre plateformes

**Socle commun :** mentions légales, confidentialité, cookies/stockages et accessibilité, accessibles sans connexion. Une page HTML lisible au mobile est préférable pour la consultation ; conserver le PDF daté téléchargeable. Un lien vers une source publique commune suffit : il n'est pas utile d'entretenir quatre versions divergentes.

| Plateforme | Accès permanent | Moment de présentation | Remise et conservation |
|---|---|---|---|
| **Marketplace** | Pied de page : socle commun, CGV, rétractation. Accès direct à la fonction de rétractation. | CGV et caractéristiques de l'offre avant engagement ; acceptation des CGV ; information près des champs acheteur/bénéficiaire. | Email : récapitulatif, CGV exactes et formulaire. Conserver les documents applicables et la preuve liée à la commande. Prévoir la couverture B2B pour les entreprises. |
| **Live** | Réglages « Informations et conditions » : CGU Live, notice Live et socle commun ; accessibles sans carnet préalable. | Information courte au premier usage du carnet ; explications avant sauvegarde/export ; choix des notifications distincts de la permission technique. Avant une inscription Animation : règlement et fiche propres à l'opération. | Accès aux règles applicables après inscription ; version archivée. Informations d'utilisation et d'échéance du coffret facilement retrouvables. |
| **Pro** | Socle commun sur la connexion et dans l'application. Espace privé « Mon contrat et mes prestations » : contrat signé, fiche et avenants. | Contrat complet et fiche à l'onboarding terrain ; complément article 28 avant usage du service concerné ; conditions des animations avant participation. | Deux originaux papier complets, un pour chaque partie. Scan lisible du contrat et de toutes ses fiches, rattaché au commerçant, consultable en privé. Le backend possède déjà un contrôle de contrat signé. |
| **Animation** | Socle commun sur la connexion. Espace privé « Abonnement et contrat » : récapitulatif, Conditions particulières, annexe données et liste des prestataires. | Dossier avant souscription ; coût et conditions avant achat de lots. Règlement/fiche complets avant publication d'une opération. | Remettre le dossier accepté au signataire habilité et l'archiver. Publier pour les participants le règlement de leur opération et l'information de confidentialité correspondante. |

**Onboarding commerçant papier recommandé :** renseigner les prestations, leur valeur globale et la commission ; barrer les lignes inutilisées ; joindre les éventuelles fiches supplémentaires aux deux exemplaires ; signer les deux dossiers complets ; remettre immédiatement un original au commerçant ; scanner l'ensemble pour le dossier privé. Toute modification économique ultérieure doit être acceptée et identifiable. Une modification dans le catalogue ne remplace pas cet accord.

Les exemplaires signés, coordonnées individualisées et registres internes ne doivent pas être copiés dans les répertoires publics des applications. Publier les modèles génériques utiles n'autorise pas la publication des dossiers personnels signés.

### État constaté dans les dépôts

- **Marketplace/Live :** les huit PDF publics sont identiques octet pour octet aux huit V1 correspondants ; les empreintes enregistrées concordent. Les 458 fragments de contenu HTML contrôlés se retrouvent dans les PDF, après normalisation des espaces et césures. Les pages légales possèdent version, téléchargement et sommaire. Cela valide la cohérence des fichiers locaux, pas encore celle du site déployé.
- **Pro :** les liens vers le socle juridique et la consultation du contrat signé n'ont pas été identifiés dans l'interface inspectée. L'archivage backend avec date, version, signataires et lisibilité existe déjà.
- **Animation :** la vue Abonnement présente la formule et ses droits, mais aucun accès au dossier Conditions particulières/annexe données n'a été repéré. L'information d'inscription des participants doit aussi être contextualisée pour l'organisateur.

### Publication et maintien des versions

1. Corriger les points de texte, puis arrêter la version et sa date d'effet.
2. Conserver les sources modifiables et un manifeste maître dans un dossier distinct du corpus public : document, public visé, version, date, fichier, empreinte et source.
3. Produire depuis cette source l'HTML et le PDF concordants. Le script Marketplace actuel attend des DOCX et un manifeste absents du dossier V1 composé uniquement de PDF : conserver ces entrées ailleurs ou adapter l'import avant la prochaine mise à jour.
4. Garder des fichiers immuables par version. Les liens courants peuvent désigner les conditions en vigueur ; les commandes et participations doivent retrouver la version qui leur était applicable. Après diffusion, ne pas écraser silencieusement une version acceptée.
5. Séparer publication des textes génériques et archivage privé des contrats signés.
6. Après déploiement, vérifier sans connexion et sur mobile les liens, PDF, version servie, preuve d'acceptation, contenu reçu par courriel, rétractation et récupération d'une ancienne version.

## 6. Ordre de travail proposé

1. **Marketplace :** réaliser la rétractation en ligne, enregistrer la version acceptée des CGV et remettre les pièces contractuelles avec la confirmation.
2. **Accessibilité :** contrôler les parcours, corriger les obstacles et documenter le résultat selon le périmètre déjà retenu.
3. **Couverture contractuelle :** compléter l'achat B2B et les clauses RGPD du service commerçant pour les parcours concernés.
4. **Animation :** produire le récapitulatif et la liste prestataires ; préciser les lots non attribués ; figer règlement et fiche dans la preuve de participation.
5. **Texte et gouvernance :** corriger les renvois de l'Annexe C, harmoniser BUM, préciser les transferts et vérifier les dossiers opérationnels annoncés.
6. **Diffusion :** ajouter les accès Pro/Animation et les informations contextuelles, puis vérifier les versions effectivement déployées.

La priorité est de terminer ces dossiers et parcours. Ajouter des chartes ou annexes générales supplémentaires n'apporterait pas la même protection.

## 7. Références techniques des constats

Chemins relatifs à la racine du dépôt backend ; numéros de lignes constatés le jour de la revue et susceptibles d'évoluer.

| Constat | Références locales |
|---|---|
| Routes et pages juridiques, rétractation statique | `../localeo-marketplace/src/App.jsx:264`, `:271` ; `src/pages/LegalPage.jsx:54` |
| Acceptation CGV particulier non rattachée à la version | `../localeo-marketplace/src/pages/CoffretPage.jsx:489`, `:697` ; `app/api/schemas.py:675` |
| Confirmation avec reçu, sans remise CGV/formulaire repérée | `app/application/gestion_achats/use_cases/valider_paiement.py:653`, `:667` ; `renvoyer_email_confirmation_coffret_instance.py:103` dans le même dossier ; `app/infrastructure/email/templates/confirmation_coffret.html` |
| Acceptation règlement participant sans version liée | `app/infrastructure/persistence/models.py:1669` ; `app/application/animation_locale/services/participants_animation.py:69` |
| Preuve plus détaillée dans l'invitation commerçant | `app/infrastructure/persistence/models.py:1801` ; `../localeo-commercant/src/features/animations/pages/ParticipationRequestDetailPage.jsx:151` |
| Contrat papier et archivage déjà prévus | `app/application/conformite_fiscale_bum/service_onboarding_commercant.py:866`, `:905`, `:968` |
| Données du brouillon de facture commerçant persistées | `app/application/conformite_fiscale_bum/service_facture_commercant_assistee.py:56` |
| Parcours achat B2B et conditions de crédit | `../localeo-marketplace/src/pages/CommandeProPage.jsx:380` ; `app/api/paiements_api.py:43` |
| Liens juridiques Pro/Animation non identifiés | `../localeo-commercant/src/app/ApplicationFrame.jsx:42` ; `../localeo-animation/src/app/App.tsx:3575` et recherches dans leurs sources publiques |
| Analytics suspendu | `../localeo-marketplace/src/services/analytics.js:9`, `:84` |
| Import documentaire exigeant sources et manifeste | `../localeo-marketplace/scripts/import-legal-documents.ps1:10` ; `src/content/legalDocuments.v1.json` ; `public/legal/v1/` |

Inventaire de contrôle, extractions et notes de lecture conservés dans `tmp/pdfs/final-v1-audit/`. Les seize PDF de V1 ont été laissés intacts.
