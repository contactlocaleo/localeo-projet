# Controle des procedures avant et apres migration

Source avant : localeo-backend-before.zip ; source apres : localeo-projet/docs/exploitation.

42 procedures controlees ; 13 ecarts de plan et 12 absences de catalogue avant comme apres ; 0 resultat modifie.

| Document | Plan non conforme avant/apres | Absent catalogue avant/apres | Ecarts du plan |
|---|---|---|---|
| technique/provisionner-referentiels.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| technique/publier-documents-juridiques.md | oui/oui | non/non | ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| technique/sessions-administration.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/corriger-accents-contenus-animation.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/creer-offre-animation.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/desactiver-antivirus-documentaire.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/gerer-acces-animation.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/gerer-souscriptions-animation.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/localeo-ops.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/localeo-support.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/menu-animation-erp.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/profil-facturation-localeo.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |
| exploitation/reprise-commissions.md | oui/oui | oui/oui | statut absent des 800 premiers caracteres ; ## Fiche réflexe ; ## Problèmes traités ; ## Résultat attendu ; ## Procédure ; ## Contrôles après action ; ## Échec, arrêt et escalade |

Le test historique pytest comptait 15 echecs : 13 cas parametres de plan et 2 catalogues (un par categorie). Le test unittest conserve les memes exigences ; ses subTests comptent les 12 liens absents individuellement, soit 25 sous-echecs au total. Selection via documentation.exports.json : exactement les 42 procedures du corpus backend sauvegarde, aucun skip ajoute.
