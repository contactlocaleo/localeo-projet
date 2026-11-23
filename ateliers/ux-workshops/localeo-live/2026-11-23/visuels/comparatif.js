(() => {
  const publicCapture = (image, note, alt) => ({ image, note, alt, equivalent: true });
  const contextCapture = (image, note, alt) => ({ image, note, alt });
  const lotsContext = {
    ...contextCapture('34-lots-vides-390.png', 'Le carnet de test est vide. La capture situe Mes lots. L’état avec un lot attribué manque dans l’exploration du 23.', 'Mes lots vide avec l’entrée de récupération'),
    extra: 'Live-meslots.jpg',
    extraLabel: 'Voir le JPG fourni · session et date non vérifiées'
  };
  const qrContext = contextCapture('31-fiche-qr-public-390.png', 'La fiche publique demande un QR sur place et le code du jour. Le formulaire ouvert par un QR valide n’a pas été observé.', 'Fiche de la tombola publique et consigne pour scanner le QR');
  const refusedContext = contextCapture('37-qr-refuse-focus-390.png', 'Refus observé sur la route d’ajout au carnet. Le refus du QR d’entrée sur place reste à vérifier.', 'Refus d’un accès d’ajout au carnet et focus du lien de récupération');
  const programme = publicCapture('20-programme-bouliac-390.png', 'Le premier titre affiche « En cours » avec une fin prévue au 13 novembre. Le programme a été observé le 23.', 'Programme de Bouliac avec la première tombola et ses dates');
  const programmeEmpty = publicCapture('21-prochainement-clavier-390.png', 'Le raccourci déplace déjà le focus sur la période vide. Le geste est préservé.', 'Section Prochainement vide avec son titre entouré par le focus');
  const missingDetail = publicCapture('61-passeport-detail-390.png', 'Le Passeport figurait au programme. La fiche a renvoyé 404, y compris après un nouvel essai.', 'Fiche Passeport indisponible dans Localeo Live');
  const recovery = publicCapture('40-recuperation-stable-390.png', 'Le formulaire de récupération et les autres chemins d’accès sont visibles.', 'Formulaire de récupération du carnet');
  const orientations = {
    B1: {
      name: 'Inscription', mission: 'Participer', title: 'Rendre cohérentes les conditions d’inscription',
      vote: '12 pour · 0 contre · 0 abst.', effort: 'S',
      benefit: 'Savoir quelles informations préparer et si une visite est requise avant d’ouvrir le formulaire.',
      before: publicCapture('63-tombola-inscription-action-390.png', 'La fiche annonce l’e-mail. Le formulaire demande quatre informations et présente deux consignes incompatibles sur la visite.', 'Fiche de la tombola avec son bouton d’inscription'),
      after: 'Scénario illustratif sans visite. Faire confirmer la règle réelle et vérifier le règlement avant tout changement.',
      states: {
        'B1-formulaire': { before: publicCapture('41-formulaire-tombola-email-390.png', 'Le formulaire affiche les champs obligatoires et juxtapose les deux consignes sur la visite.', 'Formulaire réel de la tombola avec les deux consignes de visite') }
      }
    },
    B3: {
      name: 'QR et reprise', mission: 'Participer', title: 'Suivre la même animation du QR à la reprise',
      vote: '11 pour · 0 contre · 1 abst.', effort: 'M',
      benefit: 'Reconnaître l’animation, comprendre le résultat de l’inscription et savoir comment la retrouver.',
      before: qrContext,
      after: 'Chaîne illustrée à éprouver avec un QR autorisé. Le ticket n’apparaît dans le carnet qu’après l’ajout confirmé.',
      states: {
        'B3-confirmation': { before: { note: 'Aucune confirmation d’inscription reçue pendant la visite du 23.' }, after: 'État illustratif. Afficher « Inscription enregistrée » après preuve de succès et expliquer comment ajouter le ticket au carnet.' },
        'B3-reprise': { before: contextCapture('35-participations-vides-390.png', 'Liste publique vide. Le carnet rempli et sa reprise n’ont pas été rejoués.', 'État vide de la liste personnelle des participations') },
        'B3-incertain': { before: { note: 'Aucune inscription envoyée. Un résultat incertain de soumission n’a donc pas été observé.' }, after: 'État illustratif. Vérifier l’e-mail et attendre une réponse certaine. Un réessai éventuel reprend la même demande, selon le mécanisme existant.' },
        'B3-invalide': { before: refusedContext, after: 'État illustratif du QR d’entrée invalide ou expiré. Aucun titre déduit si le QR ne donne pas un contexte fiable.' }
      }
    },
    C1: {
      name: 'Mes lots', mission: 'Gérer les lots', title: 'Reconnaître l’état et les consignes du lot',
      vote: '11 pour · 0 contre · 1 abst.', effort: 'M',
      benefit: 'Savoir si le lot est disponible, où aller et quel geste faire.',
      before: lotsContext,
      after: 'Lot, commerce et dates fictifs. Les actions suivent l’état confirmé. Présenter ou fermer un bon ne confirme aucune remise.',
      states: {
        'C1-incertain': { after: 'Le dernier état connu est distinct du résultat actuel. L’action d’actualisation est proposée, le retrait dépend d’un état confirmé.' },
        'C1-bon': { after: 'La zone du code est illustrative et non scannable. La fermeture représente un retour avec état relu, sans remise déclenchée.' }
      }
    },
    D1: {
      name: 'Programme', mission: 'Consulter les dates', title: 'Distinguer dates prévues et statut public',
      vote: '12 pour · 0 contre · 0 abst.', effort: 'M',
      benefit: 'Comprendre la période d’une animation et retrouver rapidement les prochaines dates.',
      before: programme,
      after: 'Le statut public reste visible. Le repère de date passée aide à lire la carte et renvoie aux modalités de la fiche.',
      states: {
        'D1-prochainement': { before: programmeEmpty, after: 'La période vide garde son repère et l’issue « Modifier mes communes ».' },
        'D1-futur': { before: { note: 'Bouliac n’avait aucune animation future dans l’aperçu du 23. Il manque une capture équivalente.' }, after: 'Exemple fictif d’animation à venir et d’animation sans dépassement de la fin prévue.' },
        'D1-partiel': { before: publicCapture('66-programme-contre-verification-390.png', 'Une passe ordinaire a reçu HTTP 429. Le site affiche « Aperçu partiel » et une action de reprise.', 'Découvrir affiche un programme partiel après limitation des requêtes'), after: 'Cas d’affichage du programme partiel. Les dates et comptes non vérifiés restent inconnus. Cette planche ne traite pas la cause de la 429.' }
      }
    },
    D3: {
      name: 'Fiche indisponible', mission: 'Découvrir et participer', title: 'Continuer après une fiche indisponible',
      vote: '12 pour · 0 contre · 0 abst.', effort: 'M',
      benefit: 'Retrouver la sélection de Bouliac et poursuivre son choix depuis le programme.',
      before: missingDetail,
      after: 'Exemple pour une indisponibilité publique confirmée. Le retour rouvre le programme de la commune et place le focus à un repère de reprise.',
      states: {
        'D3-temporaire': { before: { note: 'Les deux ouvertures du Passeport ont reçu HTTP 404. Il manque un AVANT équivalent pour une erreur temporaire.' }, after: 'Erreur temporaire illustrée. Proposer de réessayer ou de revenir au programme, en laissant l’état de publication indéterminé.' },
        'D3-retour': { before: contextCapture('27-programme-retabli-390.png', 'La capture montre le Passeport et la carte suivante dans la liste. Elle ne montre pas un retour depuis la 404.', 'Aperçu avec la carte du Passeport au-dessus du Juste Prix local'), after: 'Retour illustratif au niveau du choix précédent. La position et le focus utiles dépendent de la liste encore disponible.' }
      }
    },
    E1: {
      name: 'Accessibilité', mission: 'Les trois missions', title: 'Rendre les erreurs et leur issue lisibles',
      vote: '11 pour · 0 contre · 1 abst.', effort: 'M',
      benefit: 'Identifier l’action utile et continuer au clavier ou avec des aides de lecture.',
      before: publicCapture('37-qr-refuse-focus-390.png', 'Le lien de récupération est déjà activable au clavier, avec un focus visible et un contraste mesuré.', 'Écran d’accès refusé, focus du lien Retrouver mon accès'),
      after: 'Repères existants à préserver. L’exemple d’erreur e-mail est un cas de recette, à vérifier avec les aides d’accès.',
      states: {
        'E1-recuperation': { before: recovery },
        'E1-erreur': { before: contextCapture('40-recuperation-stable-390.png', 'Formulaire réel avant toute saisie. Aucune erreur e-mail équivalente n’a été observée.', 'État initial du formulaire de récupération'), after: 'Erreur illustrée. Un résumé pointe vers le champ, qui conserve sa valeur et le détail de la correction.' }
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
    const key = Object.hasOwn(screens, hash) ? hash : keysFor(Object.hasOwn(orientations, hash) ? hash : 'B1')[0];
    selectState(key, { updateHash: false });
  }
  window.addEventListener('hashchange', openHash);
  openHash();
})();
