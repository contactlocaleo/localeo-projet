# Identifiant QR et validation sans camera

Chaque vue de presentation d'un QR Animation ou Coffret affiche un bloc
« Identifiant du QR code » et un bouton de copie. Cet identifiant sert au
commercant a retrouver la meme participation ou le meme coffret que le scan.

- Coffret : afficher et copier exactement `qr_token` fourni avec le QR par
  `fetchConsumerCoffretInstanceQrCode`. Ne pas utiliser `verification_code`,
  l'identifiant d'instance ou le token de consultation a sa place.
- Animation : afficher et copier le jeton participant. Le scanner Pro accepte
  aussi l’ancien lien participant et le nouveau [lien Pro E82](../epic-82-scan-qr-externe-localeo-pro/README.md).
- Le bloc reste associe au QR sur la page Coffret, dans Localeo Live, sur la
  carte cadeau, dans son export et sur la page d'impression.
- En cas d'absence de `qr_token`, ne pas lui substituer un autre code.
- La copie conserve la casse et l'integralite de la valeur. Si le presse-papiers
  est indisponible, selectionner le texte pour permettre une copie manuelle.

Dans Localeo Pro, la saisie « Identifiant du QR code » reste accessible si la
camera est indisponible. Elle ouvre les prestations du coffret ou l'etape de
l'animation. La validation conserve sa confirmation explicite et ses controles
serveur habituels. Aucun nouveau endpoint ni changement backend n'est requis.

La valeur copiée reste dans la vue courante. L’export volontaire d’une carte
contient le QR et son identifiant pour que le bénéficiaire puisse les présenter.
Lorsque le nouveau QR contient un lien Pro, son fragment est retiré dès
l’arrivée dans Pro. L’identifiant reste exclu des statistiques et du stockage
du carnet.
