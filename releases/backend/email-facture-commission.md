# Notification de facture de commission Localeo

Le mail `LOCALEO_INVOICE_ISSUED` des factures `COMMISSION_COMMERCANT`
issues d'un `REVERSEMENT` utilise un modèle HTML aux couleurs Localeo,
avec logo, numéro de facture et version texte de secours.

Il explique le lien avec la campagne de reversement Localeo et indique le
parcours **Finance et facturation > Factures Localeo** dans l'espace commerçant
pour télécharger le PDF. Il distingue la disponibilité de la facture de
l'arrivée du reversement sur le compte bancaire.

L'envoi reste géré par l'outbox existante. Le changement concerne les prochaines
notifications préparées ; aucun email existant n'est renvoyé. Les notifications
d'abonnement et d'avoir restent inchangées. Aucun changement des applications
commerçant, Animation ou marketplace n'est nécessaire.
