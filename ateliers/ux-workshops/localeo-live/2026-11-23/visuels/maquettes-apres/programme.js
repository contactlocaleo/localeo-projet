(() => {
  const region = (counts) => `
    <div class="programme-head">
      <h1>Découvrir</h1>
      <div class="locality"><span data-icon="pin"></span><strong>Bouliac</strong><button class="text-button" type="button" aria-disabled="true">Changer</button></div>
      <nav class="section-links" aria-label="Découvrir">
        <span aria-current="page">Animations</span><span>Commerçants</span><span>Coffrets</span>
      </nav>
      <h2>Le programme de vos communes</h2>
      <nav class="period-links" aria-label="Périodes du programme">
        <a href="#en-cours" data-focus-target>En ce moment</a>
        <a href="#prochainement" data-focus-target>Prochainement ${counts}</a>
      </nav>
    </div>`;
  const current = (search = true) => `
    <div class="period-title">
      <h2 id="en-cours" tabindex="-1"><span data-icon="calendar"></span>En ce moment</h2>
      ${search ? '<button class="text-button" type="button" aria-disabled="true">Rechercher</button>' : ''}
    </div>`;
  const upcoming = `
    <div class="period-title"><h2 id="prochainement" tabindex="-1"><span data-icon="calendar"></span>Prochainement</h2></div>`;
  const empty = `${upcoming}
    <section class="panel">
      <p>Aucune animation à venir dans votre sélection.</p>
      <button class="action secondary" type="button" aria-disabled="true">Modifier mes communes</button>
    </section>`;
  const tombola = `
    <article class="panel">
      <span class="badge">En cours</span>
      <div class="card-title">
        <div class="stack">
          <h3>TEST2-Tombola Delphine-05/11/2026</h3>
          <p class="muted">Tombola · Bouliac</p>
        </div>
        <span class="glyph" data-icon="gift"></span>
      </div>
      <p class="key-date">Du 6 au 13 novembre 2026</p>
      <p class="notice warning"><strong>Fin prévue dépassée.</strong> Consultez la fiche pour vérifier les modalités de participation.</p>
      <p>Participez au tirage chez les commerçants.</p>
      <p><strong>À gagner</strong> · Lot fictif de formation</p>
      <p>Achat requis, sans minimum, chez un partenaire.</p>
      <button class="action" type="button" aria-disabled="true">Voir l’animation <span aria-hidden="true">→</span></button>
      <button class="text-button" type="button" aria-disabled="true">Partager</button>
    </article>`;
  const back = '<a class="backlink" href="?etat=D3-retour#suite">← Retour aux animations</a>';
  const context = '<p class="eyebrow">Animation · Bouliac</p><h1>Passeport commercant</h1>';

  Object.assign(window.LiveMockScreens ??= {}, {
    'D1-programme': {
      title: 'Programme et fin prévue', label: 'Date de fin dépassée', tab: 'discover',
      body: `${region('0')}<p class="muted">Extrait de l’aperçu de Bouliac</p>${current()}${tombola}${empty}`
    },
    'D1-prochainement': {
      title: 'Prochainement sans animation', label: 'À venir · vide', tab: 'discover', startAt: 'prochainement',
      body: `${region('0')}${current()}${tombola}${empty}`
    },
    'D1-futur': {
      title: 'Animation future et fin prévue', label: 'À venir · exemple fictif', tab: 'discover',
      body: `${region('1')}
        ${current()}
        <article class="panel">
          <span class="badge">En cours</span>
          <h3>Tombola des commerces</h3>
          <p class="muted">Bouliac · Exemple</p>
          <p class="key-date">Du 20 au 28 novembre 2026</p>
          <button class="action" type="button" aria-disabled="true">Voir l’animation</button>
        </article>
        ${upcoming}
        <article class="panel">
          <span class="badge">À venir</span>
          <h3>Défi des vitrines de décembre</h3>
          <p class="muted">Bouliac · Exemple</p>
          <p class="key-date">Du 1 au 7 décembre 2026</p>
          <button class="action" type="button" aria-disabled="true">Voir l’animation</button>
        </article>`
    },
    'D1-partiel': {
      title: 'Programme partiel', label: 'Programme partiel', tab: 'discover',
      body: `${region('')}
        <div class="notice warning">
          <p role="status"><strong>Programme incomplet.</strong> Certaines animations n’ont pas pu être chargées.</p>
          <button class="action secondary" type="button" aria-disabled="true">Réessayer</button>
        </div>
        ${current()}
        <section class="panel"><p>La liste des animations en cours n’a pas pu être vérifiée.</p></section>
        ${upcoming}
        <section class="panel"><p>Les prochaines animations n’ont pas pu être vérifiées.</p></section>`
    },
    'D3-indisponible': {
      title: 'Fiche indisponible', label: 'Fiche indisponible', tab: 'discover',
      body: `${back}<div class="stack">${context}</div>
        <section class="panel status-card">
          <h2>Animation indisponible</h2>
          <p>La fiche de cette animation n’est pas accessible dans le programme public.</p>
          <a class="action" href="?etat=D3-retour#suite">Retour au programme de Bouliac</a>
          <button class="action secondary" type="button" aria-disabled="true">Réessayer</button>
          <button class="text-button" type="button" aria-disabled="true">Mes participations</button>
        </section>`
    },
    'D3-temporaire': {
      title: 'Erreur temporaire à l’ouverture', label: 'Erreur temporaire', tab: 'discover',
      body: `${back}<div class="stack">${context}</div>
        <section class="panel status-card">
          <h2>Lecture momentanément impossible</h2>
          <p>Impossible de vérifier la fiche pour le moment. Vous pouvez réessayer ou revoir le programme de Bouliac.</p>
          <button class="action" type="button" aria-disabled="true">Réessayer</button>
          <a class="action secondary" href="?etat=D3-retour#suite">Retour au programme de Bouliac</a>
          <button class="text-button" type="button" aria-disabled="true">Mes participations</button>
        </section>`
    },
    'D3-retour': {
      title: 'Retour dans le programme', label: 'Retour au programme', tab: 'discover',
      body: `${region('0')}
        ${current()}
        <p class="notice" role="status" id="suite" tabindex="-1">Vous êtes revenu dans le programme de Bouliac.</p>
        <article class="panel">
          <span class="badge">En cours</span>
          <h3>Juste prix local TCA</h3>
          <p class="muted">Le Juste Prix Local · Bouliac</p>
          <p class="key-date">Le 22 novembre 2026</p>
          <p class="notice warning"><strong>Fin prévue dépassée.</strong> Consultez la fiche pour vérifier les modalités de participation.</p>
          <p>Estimez le prix proposé dans les commerces. Bonne réponse et passage validé sont requis dans le même commerce.</p>
          <button class="action" type="button" aria-disabled="true">Voir l’animation</button>
        </article>${empty}`
    }
  });
})();
