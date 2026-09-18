# Factures Localeo : PDF et mentions

Le modèle `LOCALEO_INVOICE_2026_09` utilise le logo, les couleurs et les polices
embarquées Localeo. Il affiche les identités et adresses, SIREN/SIRET, RCS,
capital, forme juridique, numéros de TVA, dates, période de prestation,
bon de commande lorsqu'il est transmis, détail quantité/prix/remise/TVA,
ventilation de TVA et totaux. Les avoirs mentionnent le numéro de la facture
d'origine et leur motif. Le numéro de document est répété sur chaque page.

Les prochaines commissions de campagne sont considérées comme déjà prélevées
sur les sommes encaissées, conformément au fonctionnement confirmé par Localeo :
déjà réglé = total TTC, net à payer = zéro. Cela ne confirme pas l'arrivée
du reversement bancaire. La date de prestation de commission correspond à
l'exécution de la campagne, distincte des validations des expériences clientes.

## Configuration avant émission

Dans **Paiements et facturation > Profil de facturation Localeo**, compléter
forme juridique, capital social en euros, RCS, SIRET, TVA, siège social si
différent de l'adresse de facturation. Déclarer l'option TVA sur les débits
uniquement si elle a effectivement été exercée. Une ligne à TVA nulle nécessite
un fondement fiscal explicite ; aucun régime d'exonération n'est déduit.

L'émission exige les données légales de l'émetteur, une date de prestation ou
période, ainsi qu'une échéance pour les factures restant à payer. Les conditions
sont figées dans le snapshot : escompte néant, pénalités interprofessionnelles
au taux BCE du semestre majoré de 10 points, indemnité de recouvrement de 40 EUR.
Faire confirmer leur cohérence avec les contrats/CGV par le conseil comptable.
Ces mentions interprofessionnelles ne remplacent pas le régime spécifique
des marchés publics. Les profils clients doivent être exacts et complets.

Les documents déjà stockés ne sont pas régénérés. Pour un snapshot historique
sans conditions, le rendu indique l'absence des informations ; il n'invente
pas de nouvelles données ni un acquittement rétroactif. Une facture déjà émise
incorrecte doit suivre une correction traçable (avoir/facture rectificative).

## Références officielles vérifiées le 10 septembre 2026

- [Mentions obligatoires, Service Public](https://entreprendre.service-public.gouv.fr/vosdroits/F31808?profil=societe) : Code de commerce L. 441-9 ; CGI annexe II, article 242 nonies A.
- [Délais de paiement, DGCCRF](https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/delais-de-paiement-les-regles-connaitre) : L. 441-10 et D. 441-5.

Ce PDF ne constitue pas à lui seul une facture électronique structurée transmise
par une plateforme agréée. La réforme s'applique selon le calendrier et la
catégorie d'entreprise ; elle constitue un chantier distinct. Les applications
commerçant, Animation et marketplace conservent les mêmes contrats de téléchargement.
