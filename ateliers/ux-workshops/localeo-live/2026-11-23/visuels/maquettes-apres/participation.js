(() => {
  const emailTombola = 'Tombola publique marché de noel';
  const qrTombola = 'Test de tombola publique';
  const identityFields = `
    <label class="field">Nom <input type="text" autocomplete="off" required></label>
    <label class="field">Prénom <input type="text" autocomplete="off" required></label>
    <label class="field">Adresse e-mail <input type="email" autocomplete="off" required></label>
    <label class="field">Téléphone <input type="tel" autocomplete="off" required></label>`;
  const consent = `
    <fieldset>
      <legend>Vos choix</legend>
      <label><input type="checkbox" required> J’accepte le règlement de l’animation (obligatoire).</label>
    </fieldset>`;
  const ruleExample = `
    <details>
      <summary>Conditions et règlement de l’animation</summary>
      <p class="muted">Emplacement du règlement de l’organisateur.</p>
    </details>`;

  Object.assign(window.LiveMockScreens ??= {}, {
    'B1-fiche': {
      title: 'Fiche de la tombola',
      label: 'Conditions sur la fiche',
      tab: 'discover',
      body: `
        <button class="backlink" type="button" aria-disabled="true">← Retour aux animations</button>
        <div class="stack">
          <p class="eyebrow">L’animation · Bouliac</p>
          <h1>${emailTombola}</h1>
          <p class="muted">Du 21 au 23 novembre 2026</p>
          <section class="panel stack" aria-labelledby="b1-conditions">
            <h2 id="b1-conditions">Pour participer</h2>
            <p>Inscription gratuite. Aucun achat ni visite chez un commerçant.</p>
            <p>Préparez votre nom, votre prénom, votre adresse e-mail et votre téléphone.</p>
            <p class="muted">Conditions illustrées.</p>
            ${ruleExample}
            <a class="action" href="?etat=B1-formulaire">M’inscrire à cette animation</a>
            <button class="action secondary" type="button" aria-disabled="true">Retrouver mon inscription</button>
          </section>
          <button class="action secondary" type="button" aria-disabled="true">Partager</button>
          <details class="panel" open>
            <summary>Comment jouer ?</summary>
            <ol>
              <li>Renseignez les quatre champs du formulaire et acceptez le règlement.</li>
              <li>Si votre inscription est confirmée, retrouvez le lien personnel envoyé par e-mail.</li>
            </ol>
          </details>
        </div>`
    },
    'B1-formulaire': {
      title: 'Formulaire de la tombola',
      label: 'Formulaire',
      tab: 'discover',
      body: `
        <a class="backlink" href="?etat=B1-fiche">← Retour à l’animation</a>
        <section class="panel stack" aria-labelledby="b1-inscription">
          <p class="eyebrow">Inscription à l’animation · Bouliac</p>
          <h1 id="b1-inscription">${emailTombola}</h1>
          <p>Inscription gratuite. Aucun achat ni visite chez un commerçant.</p>
          <p class="muted">Conditions illustrées.</p>
          ${ruleExample}
          <p><strong>Les quatre champs ci-dessous sont obligatoires.</strong></p>
          ${identityFields}
          ${consent}
          <button class="action" type="button" aria-disabled="true">Valider mon inscription</button>
          <a class="action secondary" href="?etat=B1-fiche">Annuler</a>
          <p class="muted">Vos coordonnées servent à gérer votre participation.</p>
        </section>`
    },
    'B3-qr': {
      title: 'Inscription par QR sur place',
      label: 'QR reconnu et code du jour',
      tab: 'discover',
      body: `
        <section class="panel stack" aria-labelledby="b3-inscription">
          <p class="eyebrow">Inscription sur place · Bouliac</p>
          <h1 id="b3-inscription">${qrTombola}</h1>
          <p class="notice">QR de l’animation reconnu. Saisissez le code du jour affiché à côté.</p>
          <label class="field">Code du jour
            <input type="text" inputmode="numeric" maxlength="6" pattern="[0-9]{6}" autocomplete="off" aria-describedby="b3-code-aide" required>
            <small id="b3-code-aide">Les six chiffres indiqués sur l’affiche.</small>
          </label>
          <p><strong>Vos coordonnées sont obligatoires.</strong></p>
          ${identityFields}
          <details>
            <summary>Conditions et règlement de l’animation</summary>
            <p>Sur place, l’inscription requiert le QR de l’animation et le code du jour en vigueur.</p>
          </details>
          ${consent}
          <button class="action" type="button" aria-disabled="true">Valider mon inscription</button>
          <button class="action secondary" type="button" aria-disabled="true">Retour à l’animation</button>
        </section>`
    },
    'B3-confirmation': {
      title: 'Inscription enregistrée',
      label: 'Inscription enregistrée',
      tab: 'discover',
      body: `
        <section class="panel stack" aria-labelledby="b3-confirmee">
          <p class="eyebrow">Bouliac</p>
          <h1 id="b3-confirmee">Inscription enregistrée</h1>
          <h2>${qrTombola}</h2>
          <p role="status">Votre inscription au tirage est confirmée.</p>
          <div class="notice">
            <h2>Retrouvez votre ticket par e-mail</h2>
            <p>Ouvrez le lien personnel reçu, puis choisissez « Ajouter à mon carnet » pour retrouver la tombola sur cet appareil.</p>
          </div>
          <details>
            <summary>Je n’ai pas reçu l’e-mail</summary>
            <p>Vérifiez vos courriers indésirables et l’adresse utilisée à l’inscription. Attendez cinq minutes avant de demander un renvoi.</p>
            <button class="action secondary" type="button" aria-disabled="true">Retrouver mon inscription</button>
          </details>
          <button class="action secondary" type="button" aria-disabled="true">Retour à l’animation</button>
        </section>`
    },
    'B3-reprise': {
      title: 'Reprise après ajout au carnet',
      label: 'Après ajout au carnet',
      tab: 'carnet',
      body: `
        <div class="stack">
          <h1>Mon carnet</h1>
          <section class="panel stack" aria-labelledby="b3-participation">
            <p class="eyebrow">Mes participations · Bouliac</p>
            <h2 id="b3-participation">${qrTombola}</h2>
            <p><span class="badge">Inscrit</span></p>
            <p>Votre ticket est dans le carnet de cet appareil. Le résultat du tirage n’est pas encore disponible.</p>
            <button class="action" type="button" aria-disabled="true">Voir ma participation</button>
          </section>
          <button class="action secondary" type="button" aria-disabled="true">Retrouver mon carnet</button>
        </div>`
    },
    'B3-incertain': {
      title: 'Inscription à vérifier',
      label: 'Réponse incertaine',
      tab: 'discover',
      body: `
        <section class="panel stack" aria-labelledby="b3-verification">
          <p class="eyebrow">Inscription sur place · Bouliac</p>
          <h1 id="b3-verification">Inscription à vérifier</h1>
          <h2>${qrTombola}</h2>
          <p class="notice warning">La réponse n’a pas pu être vérifiée. Vous pouvez réessayer la demande en cours.</p>
          <button class="action" type="button" aria-disabled="true">Réessayer la même demande</button>
          <details>
            <summary>Retrouver ma demande après avoir quitté le formulaire</summary>
            <p>Vérifiez votre boîte e-mail ou recherchez votre inscription avant de remplir un nouveau formulaire.</p>
            <button class="action secondary" type="button" aria-disabled="true">Retrouver mon inscription</button>
          </details>
        </section>`
    },
    'B3-invalide': {
      title: 'Accès QR indisponible',
      label: 'QR invalide ou expiré',
      tab: 'discover',
      body: `
        <section class="panel stack" aria-labelledby="b3-acces">
          <h1 id="b3-acces">Ce QR ne permet pas de s’inscrire</h1>
          <p>Si vous êtes sur place, scannez le QR affiché à côté du code du jour.</p>
          <button class="action" type="button" aria-disabled="true">Découvrir les animations</button>
          <p>Déjà inscrit ? Ouvrez le lien personnel reçu par e-mail ou retrouvez votre accès.</p>
          <a class="action secondary" href="?etat=E1-recuperation&amp;retour=B3-invalide">Retrouver mon accès</a>
        </section>`
    }
  });
})();
