'use strict';

// Les dossiers sont des exemples de lecture de la même édition que demo.follow.
const deroulement = (() => {
  const profiles = {
    passeport: {
      list: 'Passeports des participants', filter: 'À un tampon du seuil', indexes: [1, 4], focus: 1,
      title: 'Jules Leroy est à une visite du seuil',
      evidence: [['Les Halles', 'Tampon acquis'], ['Maison du pain', 'Tampon acquis'], ['Troisième commerce distinct', 'Passage attendu']],
      rule: 'Un tampon acquis dans trois commerces distincts qualifie le passeport. Le choix « Visite sans achat » s’applique à cette édition.'
    },
    'tombola-locale': {
      list: 'Achats validés par participant', filter: 'En attente du premier achat', indexes: [3, 5], focus: 0,
      title: 'Trois achats, une chance pour Nina Robert',
      evidence: [['Épicerie du Pont', 'Premier achat validé · qualification acquise'], ['Librairie du Bourg', 'Achat validé'], ['Maison du pain', 'Achat validé']],
      rule: 'Le premier achat confirmé donne une chance. Les validations suivantes restent consultables dans le dossier.'
    },
    'tombola-publique': {
      list: 'Inscriptions sur le marché', filter: 'Anciennes demandes en attente', indexes: [2, 5], focus: 2,
      title: 'Lou Morel a une demande en attente',
      evidence: [['Inscription', 'Ancienne demande en attente'], ['Formulaire actuel', 'Inscription explicite pendant la période ouverte'], ['Chance acquise à ce stade', '0']],
      rule: 'Un formulaire validé donne une chance par adresse e-mail. Le QR et le code du jour servent à ouvrir puis compléter le formulaire sur place.'
    },
    chasse: {
      list: 'Progression dans la chasse', filter: 'Preuve à régulariser', indexes: [0], focus: 0,
      title: 'Une preuve manque au dossier d’Ana Roy',
      evidence: [['Récit', 'Finale terminée'], ['Mission chez Mirga', 'Défi réussi'], ['Preuve de passage chez Mirga', 'Attestation annulée']],
      rule: 'La qualification exige le parcours et les preuves prévus par la version publiée. Seules les attestations encore effectives comptent.'
    },
    prix: {
      list: 'Progression par participant', filter: 'Passage manquant', indexes: [0], focus: 0,
      title: 'Lina Roux attend un passage en boutique',
      evidence: [['Fournil du Bourg', 'Réussite et passage validé'], ['Épicerie du Pont', 'Réussite obtenue · passage attendu'], ['Progression retenue', '1 commerce pour un seuil de 2']],
      rule: 'Pour cette édition, il faut une estimation dans la tolérance et un passage au même commerce. Le dossier expose la progression autorisée.'
    },
    vitrines: {
      list: 'Suivi des installations', filter: 'Vitrine avec incident', indexes: [0], focus: 0,
      title: 'Jeu suspendu après le déplacement d’un intrus',
      evidence: [['Signalement', 'Intrus déplacé à la Librairie du Bourg'], ['Installation', 'Rétablie à l’identique'], ['Nouveau contrôle lié à cet incident', 'Enregistré pendant la période ouverte']],
      rule: 'La reprise nécessite le rétablissement à l’identique et les contrôles de ce cycle d’incidents, pendant une période encore ouverte.'
    },
    'mots-croises': {
      list: 'Grilles et visites des participants', filter: 'Grille correcte, visite manquante', indexes: [1], focus: 1,
      title: 'Une visite reste à attester pour Léa',
      evidence: [['Contrôle de la grille', 'Correcte'], ['Visites attestées', '2 sur 3'], ['Condition restante', 'Dernier passage chez le commerce requis']],
      rule: 'Une grille entièrement correcte et tous les passages requis donnent une chance. L’ordre dans lequel les deux preuves arrivent peut varier.'
    },
    avent: {
      list: 'Calendrier des cases', filter: 'Case ouverte', indexes: [1], focus: 1,
      title: 'La case du 5 décembre est ouverte',
      evidence: [['Commerce du jour', 'Atelier des Saveurs'], ['Participations à cette case', '34'], ['Dotation du jour', 'Coffret Gourmand réservé']],
      rule: 'Cet exemple prospectif rattache la période, les participations et la dotation à une case précise. Les modalités du modèle restent à arbitrer.'
    },
    'escape-game': {
      list: 'Parties par étape de la mission', filter: 'Parties en cours', indexes: [0, 1], focus: 1,
      title: 'Six parties se poursuivent à la librairie',
      evidence: [['Étape du récit', 'Deuxième énigme · librairie'], ['Parties à cette étape', '6'], ['Point à examiner en cas de signalement', 'Disponibilité du lieu et de la consigne du scénario publié']],
      rule: 'La mission se joue sur un téléphone, seul ou en famille. La réussite de la finale relève du jeu. La récompense éventuelle et les modalités de traitement des incidents restent à définir.'
    }
  };

  const pageSize = 4;
  function resumed(demo, state) {
    return demo.id === 'vitrines' && (state.runResumed || state.closed);
  }
  function simulationNext(demo, state) {
    if (demo.id === 'vitrines' && !resumed(demo, state)) return '';
    const label = demo.id === 'avent' ? 'Examiner la clôture du 5 décembre' :
      demo.id === 'escape-game' ? 'Examiner la fin de période' : 'Examiner la clôture';
    return action('next', label, 'plain');
  }
  function isRecordOpen(state) {
    return Number.isInteger(state.runIndex);
  }
  function listContent(demo, state) {
    const { columns, rows } = demo.follow;
    const profile = profiles[demo.id];
    const ids = state.runFiltered ? profile.indexes : rows.map((_, i) => i);
    const page = state.runPage || 0;
    const start = page * pageSize;
    const count = ids.length;
    const pages = Math.ceil(count / pageSize);
    const body = ids.slice(start, start + pageSize).map(id => {
      const row = rows[id];
      const cells = row.map((v, i) => '<td data-label="'+safe(columns[i])+'">'+safe(v)+'</td>').join('');
      return '<tr>'+cells+'<td data-label="Dossier"><button class="plain" type="button" data-act="run-ticket-'+id+'" aria-label="Ouvrir le dossier · '+safe(row[0])+'">Ouvrir</button></td></tr>';
    }).join('');
    return {body,page,pages,count:count+' ligne'+(count>1?'s':'')+' dans l’extrait'+(pages>1?' · Page '+(page+1)+' sur '+pages:'')};
  }
  function participants(demo, state) {
    const profile=profiles[demo.id];
    const {body,page,pages,count}=listContent(demo,state);
    const filterButton = (key, text, selected) => '<button type="button" data-act="'+key+'" aria-pressed="'+selected+'" class="'+(selected?'':'plain')+'">'+safe(text)+'</button>';
    const tableHead = demo.follow.columns.concat('Dossier').map(col => '<th scope="col">'+safe(col)+'</th>').join('');
    const pageButton = (key, text, disabled) => '<button type="button" data-act="'+key+'"'+(disabled?' disabled':'')+'>'+text+'</button>';
    return '<section data-run-list><h3>'+safe(profile.list)+'</h3>'+
      '<div class="actions" role="group" aria-label="Filtrer la liste">'+filterButton('run-all','Tout l’extrait',!state.runFiltered)+filterButton('run-filter',profile.filter,!!state.runFiltered)+'</div>'+
      '<p class="note" role="status">'+count+'</p>'+
      '<table><thead><tr>'+tableHead+'</tr></thead><tbody>'+body+'</tbody></table>'+
      '<div data-run-pages'+(pages>1?'':' hidden')+'>'+actions(pageButton('run-first','Première page',page===0)+pageButton('run-prev','Page précédente',page===0)+pageButton('run-next','Page suivante',page>=pages-1))+'</div></section>';
  }
  function refreshList(demo,state,key) {
    if(!['run-all','run-filter','run-first','run-prev','run-next'].includes(key))return false;
    const list = document.querySelector('[data-run-list]');
    if(!list)return false;
    const {body,page,pages,count}=listContent(demo,state);
    list.querySelector('tbody').innerHTML=body;
    list.querySelector('[role=status]').textContent=count;
    list.querySelector('[data-run-pages]').hidden=pages<=1;
    for(const button of list.querySelectorAll('button[aria-pressed]')){
      const selected=(button.dataset.act==='run-filter')===!!state.runFiltered;
      button.setAttribute('aria-pressed',String(selected));
      button.classList.toggle('plain',!selected);
    }
    for(const button of list.querySelectorAll('[data-run-pages] button')){
      button.disabled=button.dataset.act==='run-next'?page>=pages-1:page===0;
    }
    return true;
  }
  function dossier(demo, state) {
    const s = demo.follow, p = profiles[demo.id], i = state.runIndex;
    const row = s.rows[i];
    const featured = i === p.focus;
    const info = featured ? p.evidence : row.slice(1).map((v, n) => [s.columns[n+1], v]);
    const back = action('run-back','Retour à la liste','plain');
    let content = heading(row[0],p.list+' · '+state.title)+rowTable(['Information','État du dossier'],info);
    if (demo.id === 'vitrines' && featured) {
      if (resumed(demo,state)) {
        content += receipt('Reprise confirmée pendant la période ouverte. Les progressions acquises sont conservées.');
      } else if (state.runResumePrompt) {
        content += '<section class="warning"><h3>Reprendre le jeu des vitrines ?</h3><p>Le contrôle de la librairie est enregistré. Les quatre défis et les règles de l’édition restent identiques.</p>'+
          actions(action('run-resume','Confirmer la reprise')+action('run-cancel-resume','Annuler','plain'))+'</section>';
      } else {
        content += '<p class="lead">'+safe(p.rule)+'</p>'+actions(action('run-review-resume','Préparer la reprise'));
      }
    } else {
      content += '<p class="lead">'+safe(featured ? s.effect : p.rule)+'</p>';
    }
    return content+actions(back+simulationNext(demo,state));
  }
  function render(demo, state) {
    if (isRecordOpen(state)) return dossier(demo,state);
    const p = profiles[demo.id], s = demo.follow;
    const activeAgain = resumed(demo,state);
    const focusTitle = activeAgain ? 'Incident traité à la Librairie du Bourg' : p.title;
    const focusAction = demo.id === 'vitrines' ? 'Ouvrir le dossier de la librairie' : s.action;
    const next = simulationNext(demo,state);
    return heading(s.title,activeAgain?'Le nouveau contrôle de la librairie et la reprise du jeu sont enregistrés.':s.lead)+
      measures(s.metrics)+
      '<aside class="aside"><h3>'+safe(focusTitle)+'</h3>'+actions(action('detail',focusAction)+next)+'</aside>'+
      participants(demo,state)+
      '<details class="alternatives"><summary>Communication et diffusion</summary><h3>'+safe(state.title)+'</h3><p>'+safe(state.presentation)+'</p><p class="note">'+safe(demo.communication)+'</p></details>';
  }
  function restoreFocus(key) {
    if (typeof requestAnimationFrame === 'function') requestAnimationFrame(() => {
      document.querySelector('button[data-act="'+key+'"]:not(:disabled)')?.focus({preventScroll:true});
    });
  }
  function click(key, demo, state) {
    const p = profiles[demo.id];
    if (key === 'detail' || /^run-ticket-\d+$/.test(key)) {
      const id = key === 'detail' ? p.focus : Number(key.slice('run-ticket-'.length));
      if (!demo.follow.rows[id]) return false;
      state.runIndex = id;
      state.runReturn = key;
      state.runResumePrompt = false;
      return true;
    }
    switch (key) {
      case 'run-back':
        state.runIndex = null; state.runResumePrompt = false;
        restoreFocus(state.runReturn || 'detail'); return true;
      case 'run-filter':
      case 'run-all':
        state.runFiltered = key === 'run-filter'; state.runPage = 0;
        restoreFocus(key); return true;
      case 'run-first':
      case 'run-prev':
      case 'run-next': {
        const count = state.runFiltered ? p.indexes.length : demo.follow.rows.length;
        const last = Math.ceil(count/pageSize)-1;
        const current = state.runPage || 0;
        state.runPage = key === 'run-first' ? 0 : Math.min(last,Math.max(0,current+(key==='run-next'?1:-1)));
        restoreFocus(state.runPage===0?'run-next':state.runPage===last?'run-prev':key); return true;
      }
      case 'run-review-resume':
      case 'run-cancel-resume':
      case 'run-resume':
        if (demo.id !== 'vitrines' || state.runIndex !== p.focus || resumed(demo,state)) return false;
        if (key === 'run-resume' && state.runResumePrompt) {
          state.runResumed = true; state.detail = true;
        }
        state.runResumePrompt = key === 'run-review-resume'; return true;
      default: return false;
    }
  }
  return {render, click, refreshList};
})();
