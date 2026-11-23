(() => {
  const before = (image, note, alt, equivalent = true) => ({ image, note, alt, equivalent });
  const missingProof = note => ({ note });
  const form = before('public-formulaire-390.png', 'Le formulaire demande quatre champs et juxtapose deux consignes opposées sur la visite.', 'Formulaire réel avec les deux consignes sur la visite');
  const passport = before('session-passeport-bouliac-390.png', 'Le Passeport de Bouliac affiche 2 visites sur 2, la frise et la date du tirage à annoncer.', 'Passeport personnel avec deux visites validées et la qualification');
  const orientations = {
    B1: {
      name: 'Inscription', mission: 'Participer', title: 'Aligner la fiche et le formulaire',
      vote: '12 pour · 0 contre · 0 abst.', effort: 'S',
      benefit: 'Connaître les informations à préparer et la règle de visite avant de s’inscrire.',
      before: { ...form, equivalent: false, note: 'Le formulaire a été ouvert dans cette exécution. La fiche du premier passage du 23 est consultable en contexte.', extra: '../../2026-11-23/visuels/captures-avant/63-tombola-inscription-action-390.png', extraLabel: 'Fiche du premier passage du 23' },
      after: 'Fiche et formulaire portent la même condition illustrée. La règle réelle doit être confirmée avec le règlement de la tombola.',
      states: { 'B1-formulaire': { before: form } }
    },
    B3: {
      name: 'QR et reprise', mission: 'Participer', title: 'Vérifier le parcours du QR au carnet',
      vote: '10 pour · 0 contre · 2 abst.', effort: 'M',
      benefit: 'Savoir si l’inscription a abouti, puis retrouver la même animation.',
      before: before('public-qr-invalide-390.png', 'Refus observé sur un lien d’ajout. L’entrée sur place avec QR valide reste à rejouer.', 'Refus du lien et action Retrouver mon accès', false),
      after: 'Scénario de recette. Les états positifs et la réponse incertaine n’ont pas été déclenchés. La confirmation dépend d’un succès attesté.',
      states: {
        'B3-confirmation': { before: missingProof('Les inscriptions existaient déjà. Aucun nouveau message de confirmation n’a été déclenché.') },
        'B3-reprise': { before: before('session-carnet-390.png', 'Le carnet rempli et ses participations sont réels. Le chemin précis depuis le QR jusqu’à ce carnet reste à rejouer.', 'Vue du carnet rempli', false) },
        'B3-incertain': { before: missingProof('Aucun formulaire soumis. Cet état représente une réponse à éprouver.') }
      }
    },
    C1: {
      name: 'Lot à retirer', mission: 'Gérer les lots', title: 'Savoir quoi faire quand les consignes manquent',
      vote: '12 pour · 0 contre · 0 abst.', effort: 'M',
      benefit: 'Vérifier le lieu et l’échéance avant de se déplacer, à partir du vrai détail de lot.',
      before: before('session-detail-lot-390.png', 'Lot libre réellement à retirer. La consigne de test et l’échéance non précisée sont visibles. Le nom est masqué.', 'Détail réel d’un chèque cadeau à retirer avec le nom du responsable masqué'),
      after: 'Les données manquantes sont explicites. Le contact est accessible sans transformer le lot libre en bon à code.',
      states: { 'C1-liste': { before: before('session-lots-390.png', 'La vraie liste annonce un lot à retrouver et quatre prochains tirages. Le nom du responsable est masqué.', 'Un lot libre à retirer dans Mes lots') } }
    },
    D1: {
      name: 'Programme et dates', mission: 'Consulter le calendrier', title: 'Distinguer fin prévue, statut et date de tirage',
      vote: '12 pour · 0 contre · 0 abst.', effort: 'M',
      benefit: 'Trouver les prochaines dates et savoir quelle information vérifier dans la fiche.',
      before: before('public-programme-390.png', 'La carte de tombola indique En cours alors que le 13 novembre est passé.', 'Programme public de Bouliac avec la carte de tombola et ses dates'),
      after: 'L’extrait garde le statut public. La fin prévue et l’action pour vérifier les modalités sont nommées.',
      states: {
        'D1-vide': { before: before('public-prochainement-390.png', 'Le focus du raccourci atteint déjà le titre de la période vide.', 'Programme de Bouliac, section Prochainement vide') },
        'D1-tirages': { before: before('session-tirages-390.png', 'Quatre tirages sont annoncés dans Mes lots. Les cartes lues indiquent une date à annoncer.', 'Liste personnelle des prochains tirages'), after: 'Les cartes nomment la date comme date du tirage. Les dates de participation restent au programme.' }
      }
    },
    F1: {
      name: 'Passeport et reprise', mission: 'Suivre sa participation', title: 'Savoir ce qui suit la qualification',
      vote: '12 pour · 0 contre · 0 abst.', effort: 'M',
      benefit: 'Savoir, en rouvrant le Passeport, s’il faut agir ou attendre le tirage.',
      before: passport,
      after: 'La frise et le détail déplié restent visibles. Après confirmation, la suite est d’attendre le tirage dont la date est à annoncer.',
      states: {
        'F1-verification': { before: { ...passport, equivalent: false, note: 'Le dernier état connu a été vu pendant la lecture. La capture archivée montre l’état stabilisé.' }, after: 'Pendant la lecture, le dernier état connu est distingué de la vérification en cours.' },
        'F1-incertain': { before: missingProof('Aucun échec durable du détail Passeport n’a été établi pendant cette lecture.'), after: 'Échec de vérification illustratif. Garder la dernière information avec son statut et l’action de relecture.' }
      }
    }
  };

  const screens = window.LiveMockScreens || {};
  const nav = document.querySelector('#orientations');
  const selector = document.querySelector('#state');
  const frame = document.querySelector('#mock');
  const capture = document.querySelector('#capture');
  const source = document.querySelector('#source');
  const additional = document.querySelector('#extra-source');
  const missing = document.querySelector('#missing');
  const comparison = document.querySelector('.comparison');
  const sideButtons = Array.from(document.querySelectorAll('[data-side][type="button"]'));
  const setText = (id, value) => { document.getElementById(id).textContent = value; };
  const keysFor = (id) => Object.keys(screens).filter(key => key.startsWith(id + '-'));
  let activeId = '';
  let selectedKey = '';

  function selectState(key, { updateFrame = true, updateHash = true } = {}) {
    if (!Object.hasOwn(screens, key) || selectedKey === key) return;
    const id = key.split('-')[0];
    const orientation = orientations[id];
    if (!orientation) return;
    const state = orientation.states[key] || {};
    const before = state.before || orientation.before;
    const url = 'maquettes-apres/planche.html?etat=' + encodeURIComponent(key);
    if (activeId !== id) {
      activeId = id;
      selector.replaceChildren(...keysFor(id).map(entry => new Option(screens[entry].label, entry)));
      nav.querySelectorAll('button').forEach(button => {
        if (button.dataset.orientation === id) button.setAttribute('aria-current', 'true');
        else button.removeAttribute('aria-current');
      });
      setText('mission', id + ' · ' + orientation.mission);
      setText('title', orientation.title);
      setText('benefit', orientation.benefit);
      setText('priority', 'P1');
      setText('vote', orientation.vote);
      setText('effort', orientation.effort);
    }
    selectedKey = key;
    selector.value = key;
    setText('kind', before.equivalent ? 'Capture réelle' : before.image ? 'Capture de contexte' : 'Avant manquant');
    setText('before-note', before.note);
    setText('after-note', state.after || orientation.after);
    capture.hidden = source.hidden = !before.image;
    missing.hidden = Boolean(before.image);
    if (before.image) {
      source.href = capture.src = 'captures-avant/' + before.image;
      capture.alt = before.alt;
    } else {
      capture.removeAttribute('src');
      capture.alt = '';
      source.removeAttribute('href');
    }
    additional.hidden = !before.extra;
    if (before.extra) {
      additional.href = before.extra;
      additional.textContent = before.extraLabel;
    } else {
      additional.removeAttribute('href');
    }
    frame.title = id + ' · ' + screens[key].title;
    if (updateFrame) frame.src = url;
    document.querySelector('#standalone').href = url;
    if (updateHash) history.replaceState(null, '', '#' + key);
  }

  Object.entries(orientations).forEach(([id, orientation]) => {
    const button = document.createElement('button');
    const reference = document.createElement('small');
    button.type = 'button';
    button.dataset.orientation = id;
    reference.textContent = id;
    button.append(reference, document.createTextNode(orientation.name));
    button.addEventListener('click', () => selectState(keysFor(id)[0]));
    nav.append(button);
  });
  selector.addEventListener('change', () => selectState(selector.value));
  sideButtons.forEach(button => button.addEventListener('click', () => {
    comparison.dataset.side = button.dataset.side;
    sideButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  }));
  window.addEventListener('message', (event) => {
    if (event.source === frame.contentWindow && event.data?.type === 'localeo-planche' && typeof event.data.key === 'string') {
      selectState(event.data.key, { updateFrame: false });
    }
  });
  function openHash() {
    const hash = location.hash.slice(1);
    const key = Object.hasOwn(screens, hash) ? hash : keysFor(Object.hasOwn(orientations, hash) ? hash : 'C1')[0];
    selectState(key, { updateHash: false });
  }
  window.addEventListener('hashchange', openHash);
  openHash();
})();
