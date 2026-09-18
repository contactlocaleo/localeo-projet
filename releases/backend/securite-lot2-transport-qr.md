# Transport des QR hors des URL HTTP

Le scan accepte uniquement le champ qr_coffret_instance du corps JSON (4096
caracteres maximum). Le fallback query est retire et un parametre QR dans
l'URL est refuse, meme si un corps est fourni.

GET /public/gestion-achats/qrcode/image.png exige X-QR-Token, comme /detail.
Aucun consommateur applicatif de l'ancien PNG en query n'a ete trouve ; les
emails affichent le QR dans le corps du message sans chargement de ce PNG par URL. L'application commercant
envoie deja le scan dans le corps JSON.

Tests : scan JSON accepte ; query seule ou accompagnee du corps refusee ;
PNG valide par header et refus des anciennes URL.
