(() => {
  const fictiveLot = 'Panier de saison';
  const fictiveAnimation = 'Tombola du marché';
  const lotsBack = '<a class="backlink" href="?etat=C1-lots">← Retour à mes lots</a>';
  const deadline = '<time datetime="2026-11-29">29 novembre 2026</time>';
  const expiry = '<time datetime="2026-11-20">20 novembre 2026</time>';

  const contacts = `
    <details>
      <summary id="aide-lot">Besoin d’aide ?</summary>
      <p>Contactez l’organisateur pour toute question sur votre lot.</p>
      <button class="action secondary" type="button" aria-disabled="true">Contacter l’organisateur</button>
    </details>`;

  const lotOptions = `
    ${contacts}
    <details>
      <summary>Conserver ce bon dans mon carnet</summary>
      <p>Gardez l’accès à ce bon sur cet appareil.</p>
      <button class="action secondary" type="button" aria-disabled="true">Ajouter au carnet</button>
    </details>
    <button class="action secondary" type="button" aria-disabled="true">Marquer comme vu</button>`;

  const lotScreen = (label, status, information) => ({
    title: `${fictiveLot} · ${label}`,
    label,
    tab: 'lots',
    body: `
      ${lotsBack}
      <h1>Mon lot</h1>
      <section class="panel stack" aria-labelledby="lot-name">
        <div>
          <h2 id="lot-name">${fictiveLot}</h2>
          <p class="muted">${fictiveAnimation} · Exemple fictif</p>
        </div>
        ${status}
        ${information}
      </section>
      ${lotOptions}`,
  });

  const recoveryOptions = `
    <p class="muted">Pour un coffret, utilisez son lien personnel.</p>
    <details>
      <summary>J’ai mon lien</summary>
      <p>Ouvrez le dernier lien personnel reçu par e-mail, puis choisissez « Ajouter à mon carnet ».</p>
    </details>
    <details>
      <summary>J’ai un coffret</summary>
      <p>Ouvrez le dernier lien personnel reçu pour ce coffret.</p>
    </details>
    <details>
      <summary>J’ai une sauvegarde</summary>
      <p>Importez votre fichier personnel depuis les réglages.</p>
    </details>`;

  const recoveryScreen = (invalid) => {
    const errorSummary = invalid ? `
      <div class="notice warning" role="alert">
        <strong>Vérifiez votre adresse e-mail.</strong>
        <p><a href="#e1-courriel" data-focus-target>Corriger l’adresse e-mail</a></p>
      </div>` : '';
    const errorAttributes = invalid ? 'value="monadresse" aria-invalid="true" aria-describedby="e1-format"' : '';
    const errorHint = invalid ? '<p id="e1-format">Saisissez une adresse avec un @, par exemple vous@example.org.</p>' : '';

    return {
      title: 'Retrouver mon carnet',
      label: invalid ? 'Adresse e-mail à corriger' : 'Récupération par e-mail',
      tab: 'carnet',
      body: `
        <a class="backlink" href="?etat=E1-refus">← Retour à l’écran précédent</a>
        <h1>Retrouver mon carnet</h1>
        <p class="muted">Vos participations et leurs lots associés, grâce à un lien par e-mail.</p>
        ${errorSummary}
        <form class="panel stack">
          <div class="field">
            <label for="e1-courriel">E-mail utilisé pour vos inscriptions</label>
            <input id="e1-courriel" type="email" inputmode="email" autocomplete="off" required ${errorAttributes}>
            ${errorHint}
          </div>
          <button class="action" type="button" aria-disabled="true">Recevoir mon lien personnel</button>
        </form>
        ${recoveryOptions}`,
    };
  };

  Object.assign(window.LiveMockScreens ??= {}, {
    'C1-disponible': lotScreen('À retirer', '<p class="badge">À retirer</p>', `
      <dl class="kv">
        <div><dt>Valable jusqu’au</dt><dd>${deadline}</dd></div>
        <div><dt>Lieu de retrait</dt><dd>Commerce exemple · Bouliac</dd></div>
        <div><dt>Adresse</dt><dd>À confirmer auprès de l’organisateur. <a href="#aide-lot" data-focus-target>Voir l’aide sur ce lot</a>.</dd></div>
        <div><dt>Sur place</dt><dd>Présentez le bon au commerçant.</dd></div>
      </dl>
      <a class="action" href="?etat=C1-bon">Présenter mon bon</a>`),

    'C1-bon': {
      title: `${fictiveLot} · Présenter mon bon`,
      label: 'Bon à présenter',
      tab: 'lots',
      body: `
        <a class="backlink" href="?etat=C1-disponible">← Retour à mon lot</a>
        <h1>Présenter mon bon</h1>
        <section class="panel stack" aria-labelledby="lot-name">
          <div>
            <h2 id="lot-name">${fictiveLot}</h2>
            <p class="muted">${fictiveAnimation} · Exemple fictif</p>
          </div>
          <p class="badge">À retirer</p>
          <div class="notice">
            <strong>Emplacement du QR du bon</strong>
            <p>Dans Localeo Live, présentez ce bon au commerçant.</p>
          </div>
          <p>Le commerçant confirme la remise. En fermant cet écran, vous retrouvez l’état du bon après vérification.</p>
          <a class="action secondary" href="?etat=C1-disponible">Fermer le bon</a>
        </section>
        ${lotsBack}`,
    },

    'C1-incertain': lotScreen('État à vérifier', `
      <div class="notice warning" role="status">
        <strong>Impossible de vérifier le bon</strong>
        <p>Dernier état connu · À retirer</p>
      </div>`, `
      <p>Vérifiez votre connexion, puis actualisez le bon avant de vous déplacer.</p>
      <button class="action" type="button" aria-disabled="true">Actualiser mon bon</button>`),

    'C1-remis': lotScreen('Lot remis', '<p class="badge">Lot remis</p>', `
      <p>La remise de ce lot a été enregistrée.</p>`),

    'C1-expire': lotScreen('Bon expiré', '<p class="badge">Bon expiré</p>', `
      <p>La date limite du ${expiry} est passée. Contactez l’organisateur si vous avez une question.</p>`),

    'C1-annule': lotScreen('Bon annulé', '<p class="badge">Bon annulé</p>', `
      <p>Contactez l’organisateur pour connaître la suite.</p>`),

    'C1-lots': {
      title: 'Mes lots',
      label: 'Retour à Mes lots',
      tab: 'lots',
      body: `
        <h1>Mes lots</h1>
        <section class="stack" aria-labelledby="lots-utiliser">
          <h2 id="lots-utiliser">Lots à utiliser</h2>
          <article class="panel stack">
            <div>
              <h3>${fictiveLot}</h3>
              <p class="muted">${fictiveAnimation} · Exemple fictif</p>
            </div>
            <p class="badge">À retirer</p>
            <p>Valable jusqu’au ${deadline}.</p>
            <a class="action" href="?etat=C1-disponible">Voir les consignes de retrait</a>
          </article>
        </section>
        ${contacts}`,
    },

    'E1-refus': {
      title: 'Garder ma participation',
      label: 'Récupération après accès refusé',
      tab: 'carnet',
      body: `
        <button class="backlink" type="button" aria-disabled="true">← Retour à mon carnet</button>
        <h1>Garder ma participation</h1>
        <p>Cet accès n’est plus disponible. Retrouvez votre lien personnel.</p>
        <a class="action" href="?etat=E1-recuperation">Retrouver mon accès</a>
        <p>Pas encore inscrit ? Revenez à votre carnet pour découvrir les animations.</p>`,
    },

    'E1-recuperation': recoveryScreen(false),
    'E1-erreur': recoveryScreen(true),
  });
})();
