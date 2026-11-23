(() => {
  const lotHeader = (level, id) => `
    <div class="card-title">
      <div class="stack">
        <p class="muted">Lot libre</p>
        <h${level} id="${id}" tabindex="-1">Chèque cadeau</h${level}>
        <p class="badge success">À retirer</p>
      </div>
      <span class="glyph" data-icon="gift"></span>
    </div>
    <p>Gagné lors de « Tombola 2 »</p>`;

  const lotLinks = `
    <button class="text-button" type="button" aria-disabled="true">Voir l’animation <span aria-hidden="true">→</span></button>
    <button class="text-button" type="button" aria-disabled="true">Marquer comme vu</button>`;

  const progressSteps = `
    <ol class="section-links journey-steps" aria-label="Étapes de la participation">
      <li><div><strong>Inscrit</strong><br>Confirmé</div></li>
      <li><div><strong>Qualifié</strong><br>Confirmé</div></li>
      <li><div><strong>Tirage</strong><br>À réaliser</div></li>
      <li><div><strong>Résultat</strong><br>À venir</div></li>
    </ol>`;

  const previousState = `
    <details class="panel" open>
      <summary>Dernier état connu</summary>
      <p>2 visites validées sur 2. Votre participation était qualifiée pour le tirage.</p>
      ${progressSteps}
      <p>La date du tirage restait à annoncer.</p>
    </details>`;

  const carnetBack = '<button class="backlink" type="button" aria-disabled="true">← Retour à mon carnet</button>';

  const passportHeader = `
    <div class="stack">
      <h1>Mon passeport</h1>
      <h2>Passeport commerçant</h2>
      <p class="muted">Bouliac</p>
    </div>`;

  Object.assign(window.LiveMockScreens ??= {}, {
    'C1-consignes': {
      title: 'Mon lot · Chèque cadeau',
      label: 'Consignes de retrait',
      tab: 'lots',
      body: `
        <a class="backlink" href="?etat=C1-liste#c1-ouvrir">← Retour à mes lots</a>
        <h1>Mon lot</h1>
        <section class="panel stack" aria-labelledby="c1-lot-titre">
          ${lotHeader(2, 'c1-lot-titre')}
          <h3>Retirer mon lot</h3>
          <dl class="kv">
            <div><dt>Échéance</dt><dd>Non précisée</dd></div>
            <div><dt>Adresse de retrait</dt><dd>À confirmer auprès de l’organisateur</dd></div>
          </dl>
          <p class="notice">Avant de vous déplacer, demandez où retirer le lot, jusqu’à quand et ce que vous devez présenter.</p>
          <a class="action" href="#c1-aide" data-focus-target>Comment joindre l’organisateur ?</a>
          <details>
            <summary>Consigne communiquée</summary>
            <p>Test</p>
          </details>
          ${lotLinks}
        </section>
        <section class="panel stack" aria-labelledby="c1-aide">
          <h2 id="c1-aide" tabindex="-1">Préparer le retrait</h2>
          <button class="action secondary" type="button" aria-disabled="true">Contacter l’organisateur</button>
          <p>Consultez votre e-mail d’inscription ou le support de l’animation pour trouver les coordonnées de l’organisateur.</p>
          <a class="backlink" href="#c1-lot-titre" data-focus-target>Retour aux consignes</a>
        </section>
        <button class="text-button" type="button" aria-disabled="true">Retrouver mon carnet</button>`,
    },

    'C1-liste': {
      title: 'Mes lots',
      label: 'Retour à la liste des lots',
      tab: 'lots',
      body: `
        <h1>Mes lots</h1>
        <div class="section-links" aria-label="Dans Mes lots">
          <a href="#c1-lots-a-utiliser" data-focus-target>1 lot à retrouver</a>
          <a href="?etat=D1-tirages">4 tirages à venir</a>
        </div>
        <section class="stack" aria-labelledby="c1-lots-a-utiliser">
          <h2 id="c1-lots-a-utiliser" tabindex="-1">Lots à utiliser</h2>
          <article class="panel stack" aria-labelledby="c1-lot-titre">
            ${lotHeader(3, 'c1-lot-titre')}
            <p class="badge">Nouveau</p>
            <p>Échéance non précisée. Adresse de retrait à confirmer.</p>
            <a id="c1-ouvrir" class="action" href="?etat=C1-consignes">Voir les consignes de retrait</a>
            ${lotLinks}
          </article>
        </section>
        <a class="backlink" href="?etat=D1-tirages">Mes prochains tirages</a>`,
    },

    'F1-confirme': {
      title: 'Mon passeport · Parcours qualifié',
      label: 'Participation qualifiée',
      tab: 'carnet',
      body: `
        ${carnetBack}
        <section class="panel stack" aria-label="Suivi du passeport">
          <p class="badge">Animation en cours</p>
          ${passportHeader}
          <p><strong>Parcours accompli</strong> · Vos deux visites chez les commerçants sont validées.</p>
          ${progressSteps}
          <div class="notice success">
            <p><strong>2 visites validées sur 2 · Qualifié pour le tirage</strong></p>
            <p><strong>Prochaine étape</strong> · Attendre le tirage. Sa date reste à annoncer.</p>
            <p>Vous n’avez plus de visite à faire. Le résultat n’est pas encore disponible.</p>
          </div>
          <a class="action secondary" href="?etat=F1-verification">Actualiser mon parcours</a>
        </section>
        <details class="panel" open>
          <summary>Le détail de mon parcours</summary>
          <p><strong>2 visites validées sur 2</strong></p>
          <h3>Les commerces de mon parcours</h3>
          <ul><li>Première visite validée</li><li>Deuxième visite validée</li></ul>
        </details>`,
    },

    'F1-verification': {
      title: 'Mon passeport · Lecture en cours',
      label: 'Vérification en cours',
      tab: 'carnet',
      body: `
        ${carnetBack}
        <section class="panel stack" aria-label="Suivi du passeport">
          ${passportHeader}
          <div class="notice" role="status">
            <p><strong>Vérification de votre parcours…</strong></p>
            <p>Vous pouvez consulter le dernier état connu pendant la vérification.</p>
          </div>
        </section>
        ${previousState}`,
    },

    'F1-incertain': {
      title: 'Mon passeport · État à vérifier',
      label: 'Échec de vérification illustratif',
      tab: 'carnet',
      body: `
        ${carnetBack}
        <section class="panel stack" aria-label="Suivi du passeport">
          ${passportHeader}
          <div class="notice warning" role="status">
            <p><strong>Impossible de vérifier votre parcours</strong></p>
            <p>Consultez le dernier état connu. Réessayez pour vérifier si le tirage ou le résultat a changé.</p>
          </div>
          <a class="action" href="?etat=F1-verification">Réessayer</a>
        </section>
        ${previousState}`,
    },
  });
})();
