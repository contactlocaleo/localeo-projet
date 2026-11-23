(() => {
  const header = `
    <div class="programme-head">
      <h1>Découvrir</h1>
      <div class="locality"><span data-icon="pin"></span><strong>Bouliac</strong><button class="text-button" type="button" aria-disabled="true">Changer</button></div>
      <nav class="section-links" aria-label="Découvrir"><span aria-current="page">Animations</span><span>Commerçants</span><span>Coffrets</span></nav>
      <h2>Le programme de vos communes</h2>
      <nav class="period-links" aria-label="Périodes du programme"><a href="#en-cours" data-focus-target>En ce moment 10</a><a href="#prochainement" data-focus-target>Prochainement 0</a></nav>
    </div>`;
  const list = `
    <div class="period-title"><h2 id="en-cours" tabindex="-1"><span data-icon="calendar"></span>En ce moment</h2><button class="text-button" type="button" aria-disabled="true">Rechercher</button></div>
    <article class="panel">
      <span class="badge">En cours</span>
      <div class="card-title"><div class="stack"><h3>TEST2-Tombola Delphine-05/11/2026</h3><p class="muted">Tombola · Bouliac</p></div><span class="glyph" data-icon="gift"></span></div>
      <p class="key-date">Dates prévues de l’animation · 6 au 13 novembre 2026</p>
      <p class="notice warning"><strong>Fin prévue dépassée.</strong> Consultez la fiche pour vérifier si vous pouvez encore participer.</p>
      <p>Participez au tirage chez les commerçants.</p>
      <p><strong>Achat requis</strong> · Sans minimum, chez un partenaire.</p>
      <p><strong>À gagner</strong> · Lot fictif de formation</p>
      <button class="action" type="button" aria-disabled="true">Voir l’animation <span aria-hidden="true">→</span></button>
      <button class="text-button" type="button" aria-disabled="true">Partager</button>
    </article>
    <div class="period-title"><h2 id="prochainement" tabindex="-1"><span data-icon="calendar"></span>Prochainement</h2></div>
    <section class="panel"><p>Aucune animation à venir dans votre sélection.</p><button class="action secondary" type="button" aria-disabled="true">Modifier mes communes</button></section>`;
  Object.assign(window.LiveMockScreens ??= {}, {
    'D1-programme': {
      title: 'Dates prévues du programme', label: 'Statut et fin prévue', tab: 'discover',
      body: `${header}<p class="muted">Extrait de l’aperçu de Bouliac</p>${list}`
    },
    'D1-vide': {
      title: 'Prochainement', label: 'Prochainement · vide', tab: 'discover', startAt: 'prochainement',
      body: `${header}<p class="muted">Extrait de l’aperçu de Bouliac</p>${list}`
    },
    'D1-tirages': {
      title: 'Mes prochains tirages', label: 'Date du tirage à annoncer', tab: 'lots',
      body: `
        <a class="backlink" href="?etat=C1-liste">← Retour à mes lots</a>
        <h1>Mes prochains tirages</h1>
        <p class="muted">4 tirages à venir · Extrait de Mes lots</p>
        <article class="panel">
          <span class="badge success">Qualifié</span>
          <h2>Test Tombola</h2>
          <p class="muted">Latresne</p>
          <p class="key-date">Date du tirage à annoncer</p>
          <button class="action" type="button" aria-disabled="true">Voir ma participation</button>
        </article>
        <article class="panel">
          <span class="badge success">Qualifié</span>
          <h2 id="tirage-passeport" tabindex="-1">Passeport commercant</h2>
          <p class="muted">Bouliac</p>
          <p class="key-date">Date du tirage à annoncer</p>
          <a class="action" href="?etat=F1-confirme&amp;origine=tirages">Voir ma participation <span aria-hidden="true">→</span></a>
        </article>`
    }
  });
})();
