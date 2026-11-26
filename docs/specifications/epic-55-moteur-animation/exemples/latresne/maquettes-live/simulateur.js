/*
 * Maquette documentaire : ce fichier simule un serveur dans le navigateur.
 * Il ne constitue ni une API de production ni un stockage de participation réel.
 * La fixture contient les solutions pour fonctionner sans réseau ; seuls les
 * champs de project() sont destinés au rendu joueur. Aucune requête n'est envoyée.
 */
(function () {
  'use strict';

  const STORAGE_KEY = 'localeo-ux-hunt-v1';
  const data = window.LiveMockData;
  if (!data || !Array.isArray(data.steps) || !data.steps.length) {
    throw new Error('La fixture de démonstration doit précéder le simulateur.');
  }
  const clone = value => typeof structuredClone === 'function'
    ? structuredClone(value) : JSON.parse(JSON.stringify(value));
  const subscribers = new Set();
  let revision = 0;
  let busy = false;

  function freshState() {
    return {
      registered: false, email: '', current: 0, variant: 'standard',
      steps: data.steps.map(() => ({ solved: null, proof: false, attempts: 0, hint: false, bypassed: false })),
      network: 'online', pending: null, closed: false, started: true, log: []
    };
  }
  function readStorage() {
    try {
      const parsed = JSON.parse(window.localStorage.getItem(STORAGE_KEY));
      if (!parsed || !Number.isInteger(parsed.current) || parsed.current < 0 ||
          parsed.current >= data.steps.length || !Array.isArray(parsed.steps) ||
          parsed.steps.length !== data.steps.length || !Array.isArray(parsed.log)) return null;
      if (!parsed.steps.every(step => step && [null, 'success', 'help'].includes(step.solved) &&
          typeof step.proof === 'boolean' && Number.isInteger(step.attempts) && step.attempts >= 0)) return null;
      if (parsed.variant !== undefined && !['standard', 'code'].includes(parsed.variant)) return null;
      if (parsed.variant === 'code' && !data.codeVariant) return null;
      // Une ancienne session de recette sans vue confirmée ne peut pas servir
      // à reconstruire honnêtement une réponse perdue : repartir de l'accueil.
      if (parsed.pending && (!parsed.pending.confirmedProjection || !parsed.pending.confirmedProjection.state)) return null;
      return { ...parsed, variant: parsed.variant || 'standard' };
    } catch (_) { return null; }
  }
  let state = readStorage() || freshState();
  function effectiveStep(index) {
    return index === 3 && state.variant === 'code' && data.codeVariant ? data.codeVariant : data.steps[index];
  }
  function save() {
    try { window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) { /* repli mémoire */ }
  }
  function failure(code, message) {
    const error = new Error(message);
    error.code = code;
    return error;
  }
  function requireCondition(condition, code, message) {
    if (!condition) throw failure(code, message);
  }
  function hasProof(index) {
    return effectiveStep(index).kind === 'VIRTUAL' || state.steps[index].proof;
  }
  function effective(index) {
    const step = state.steps[index];
    return step.bypassed || (Boolean(step.solved) && hasProof(index));
  }
  function record(type, status) {
    // Ni réponse, ni email, ni capacité, ni lieu futur dans le journal.
    state.log.push({ type, status, at: new Date().toISOString() });
    state.log = state.log.slice(-24);
  }
  function publicChallenge(challenge, stepState) {
    if (!challenge) return null;
    const result = { type: challenge.type };
    for (const key of ['question', 'texte', 'bouton', 'choix', 'elements', 'elementsGauche', 'elementsDroite', 'normalisation']) {
      if (challenge[key] !== undefined) result[key] = clone(challenge[key]);
    }
    if (stepState.hint) result.indice = challenge.indice;
    if (stepState.solved === 'help') result.aideResolution = challenge.aideResolution;
    return result;
  }
  function publicPresentation(presentation) {
    if (!presentation || typeof presentation !== 'object') return null;
    const result = {};
    if (presentation.illustration && typeof presentation.illustration === 'object') {
      result.illustration = {};
      for (const key of ['id', 'texteAlternatif', 'style', 'ratio', 'format']) {
        if (presentation.illustration[key] !== undefined) result.illustration[key] = clone(presentation.illustration[key]);
      }
    }
    if (presentation.themeVisuel && typeof presentation.themeVisuel === 'object') {
      result.themeVisuel = {};
      for (const key of ['polices', 'couleurs']) {
        if (presentation.themeVisuel[key] !== undefined) result.themeVisuel[key] = clone(presentation.themeVisuel[key]);
      }
    }
    return result;
  }
  function serverProjection() {
    const current = effectiveStep(state.current);
    const currentState = state.steps[state.current];
    const contentLocked = current.kind === 'POI' && !currentState.proof && !currentState.bypassed;
    let currentStep = null;
    if (state.registered) {
      currentStep = {
        id: current.id, lieu: current.lieu, title: current.title || current.titre,
        kind: current.kind, address: current.address || null, contentLocked,
        presentation: contentLocked || currentState.bypassed ? null : publicPresentation(current.presentation),
        texteJoueur: contentLocked || currentState.bypassed ? null : current.texteJoueur,
        consigne: contentLocked || currentState.bypassed ? null : current.consigne,
        interactionCommercant: contentLocked || currentState.bypassed ? null : current.interactionCommercant,
        defi: contentLocked || currentState.bypassed ? null : publicChallenge(current.defi, currentState)
      };
    }
    // Seules la couverture publique et l’image de l’étape accessible sont projetées.
    const allowedMediaIds = new Set([data.themeVisuel?.illustrationCouverture?.id,
      currentStep?.presentation?.illustration?.id].filter(Boolean));
    const medias = (data.medias || []).filter(media => allowedMediaIds.has(media.id)).map(media => {
      const projected = {};
      for (const key of ['id', 'format', 'largeur', 'hauteur', 'octets', 'sha256', 'base64']) {
        if (media[key] !== undefined) projected[key] = clone(media[key]);
      }
      return projected;
    });
    const completed = state.registered && state.current === data.steps.length - 1 &&
      state.steps.every(step => step.solved || step.bypassed);
    const qualified = completed && state.steps.every((_, index) => effective(index));
    const regularizationSteps = state.registered ? data.steps.flatMap((_, index) => {
      const step = effectiveStep(index);
      const stepState = state.steps[index];
      return index <= state.current && step.kind === 'MERCHANT' && stepState.solved &&
        !stepState.proof && !stepState.bypassed && (index < state.current || completed)
        ? [{ index, id: step.id, lieu: step.lieu, title: step.title || step.titre, address: step.address || null }] : [];
    }) : [];
    const done = state.registered ? state.current + Number(effective(state.current)) : 0;
    return {
      state: clone(state), currentStep, medias,
      progress: { done, total: data.steps.length, percent: Math.round(done / data.steps.length * 100) },
      completed, qualified, canAdvance: state.registered && effective(state.current) && state.current < data.steps.length - 1,
      needsRegularization: regularizationSteps.length > 0, regularizationSteps,
      eligibleForHelp: state.registered && currentState.attempts > 0 && !currentState.solved &&
        !currentState.bypassed && !contentLocked && current.defi.type !== 'INFORMATION'
    };
  }
  function project() {
    if (!state.pending) return serverProjection();
    // Le serveur a pu valider l'action, mais le client n'en sait encore rien.
    // Ne révéler ni progression, ni inscription, ni preuve, ni lieu suivant
    // avant une relecture explicite. Ce snapshot survit au rechargement.
    const confirmed = clone(state.pending.confirmedProjection);
    confirmed.state.pending = { type: state.pending.type, at: state.pending.at };
    confirmed.state.network = state.network;
    confirmed.state.log = [...confirmed.state.log, {
      type: state.pending.type, status: 'UNCERTAIN', at: state.pending.at
    }].slice(-24);
    confirmed.canAdvance = false;
    confirmed.eligibleForHelp = false;
    return confirmed;
  }
  function normalized(input, profile) {
    requireCondition(typeof input === 'string' && [...input].length <= 80, 'INVALID_ANSWER', 'Saisissez une réponse courte, de 80 caractères maximum.');
    const text = input.normalize('NFKC').trim();
    requireCondition(text.length > 0, 'INVALID_ANSWER', 'Saisissez une réponse avant de valider.');
    if (profile === 'CODE') {
      const code = text.replace(/[a-z]/g, character => character.toUpperCase());
      requireCondition(/^[A-Z0-9-]{1,32}$/.test(code), 'INVALID_ANSWER', 'Le code accepte 1 à 32 lettres, chiffres ou tirets, sans espace intérieur.');
      return code;
    }
    // Profil TEXTE illustratif, adapté aux mots français de la maquette.
    // Le contrat de production exige un casefold Unicode complet côté serveur.
    return text.replace(/\s+/gu, ' ').toLowerCase().replace(/ß/g, 'ss').replace(/ς/g, 'σ')
      .normalize('NFD').replace(/\p{Mn}/gu, '').normalize('NFC');
  }
  function sameIds(answer, ids) {
    return Array.isArray(answer) && answer.length === ids.length &&
      new Set(answer).size === ids.length && answer.every(id => typeof id === 'string' && ids.includes(id));
  }
  function checkAnswer(defi, answer) {
    if (defi.type === 'SINGLE_CHOICE') {
      requireCondition(typeof answer === 'string' && defi.choix.some(choice => choice.id === answer), 'INVALID_ANSWER', 'Choisissez une des réponses proposées.');
      return answer === defi.bonneReponseId;
    }
    if (defi.type === 'ORDERING') {
      requireCondition(sameIds(answer, defi.elements.map(element => element.id)), 'INVALID_ANSWER', 'Replacez tous les fragments, une seule fois chacun.');
      return answer.every((id, index) => id === defi.ordreAttendu[index]);
    }
    if (defi.type === 'ASSOCIATION') {
      requireCondition(Array.isArray(answer) && answer.every(pair => pair && typeof pair === 'object'), 'INVALID_ANSWER', 'Associez chaque élément à une seule proposition.');
      requireCondition(sameIds(answer.map(pair => pair.gaucheId), defi.elementsGauche.map(element => element.id)) &&
        sameIds(answer.map(pair => pair.droiteId), defi.elementsDroite.map(element => element.id)), 'INVALID_ANSWER', 'Complétez toutes les associations, sans utiliser deux fois le même élément.');
      return answer.every(pair => defi.pairesAttendues.some(expected => expected.gaucheId === pair.gaucheId && expected.droiteId === pair.droiteId));
    }
    if (defi.type === 'TEXT_INPUT') {
      const value = normalized(answer, defi.normalisation);
      return defi.reponsesAcceptees.some(expected => normalized(expected, defi.normalisation) === value);
    }
    throw failure('INVALID_ACTION', 'Cette activité ne demande pas de réponse évaluée.');
  }
  function applyCommand(type, payload) {
    if (type === 'REGISTER') {
      requireCondition(!state.closed, 'CLOSED', 'Cette chasse est clôturée. Les inscriptions sont terminées.');
      if (state.registered) return 'ALREADY_REGISTERED';
      requireCondition(typeof payload.email === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email.trim()), 'INVALID_EMAIL', 'Indiquez une adresse e-mail valide.');
      requireCondition(payload.adult === true && payload.rules === true, 'CONSENT_REQUIRED', 'Confirmez votre majorité et votre acceptation du règlement.');
      state.registered = true;
      state.email = payload.email.trim();
      return 'REGISTERED';
    }
    requireCondition(state.registered, 'NOT_REGISTERED', 'Inscrivez-vous pour commencer la chasse.');
    requireCondition(!state.closed, 'CLOSED', 'Cette chasse est clôturée. Votre carnet reste consultable.');
    requireCondition(state.started, 'NOT_STARTED', 'La chasse n’a pas encore commencé. Retrouvez votre accès au démarrage.');
    const current = effectiveStep(state.current);
    const stepState = state.steps[state.current];
    if (payload.index !== undefined && type !== 'MERCHANT_PROOF') {
      requireCondition(payload.index === state.current, 'STEP_LOCKED', 'Seule l’étape actuellement débloquée est accessible.');
    }
    if (type === 'MERCHANT_PROOF') {
      const index = payload.index === undefined ? state.current : payload.index;
      requireCondition(Number.isInteger(index) && index >= 0 && index <= state.current && index < data.steps.length,
        'STEP_LOCKED', 'Ce commerce n’est pas encore accessible.');
      const target = state.steps[index];
      requireCondition(effectiveStep(index).kind === 'MERCHANT' && !target.bypassed, 'INVALID_PROOF', 'Une attestation commerçante n’est pas attendue pour cette étape.');
      requireCondition(index === state.current || Boolean(target.solved), 'INVALID_PROOF', 'Cette attestation ne correspond pas à une régularisation autorisée.');
      if (target.proof) return 'PROOF_ALREADY_RECEIVED';
      target.proof = true;
      return 'PROOF_RECEIVED';
    }
    if (type === 'NEXT') {
      requireCondition(effective(state.current), 'STEP_INCOMPLETE', 'Terminez le défi et faites confirmer votre passage avant de continuer.');
      requireCondition(state.current < data.steps.length - 1, 'LAST_STEP', 'Vous êtes déjà à la dernière étape.');
      state.current += 1;
      return 'NEXT_STEP';
    }
    requireCondition(!stepState.bypassed, 'BYPASSED', 'Cette étape est neutralisée pour tous les joueurs. Vous pouvez poursuivre.');
    if (type === 'SCAN_POI') {
      requireCondition(current.kind === 'POI', 'INVALID_PROOF', 'Un QR de lieu est attendu uniquement sur un point d’intérêt.');
      if (stepState.proof) return 'POI_ALREADY_OPEN';
      stepState.proof = true;
      return 'POI_OPEN';
    }
    requireCondition(current.kind !== 'POI' || stepState.proof, 'SCAN_REQUIRED', 'Scannez le QR du lieu pour accéder à cette activité.');
    if (type === 'CONTINUE') {
      requireCondition(current.defi.type === 'INFORMATION', 'INVALID_ACTION', 'Cette étape demande de répondre au défi.');
      if (stepState.solved) return 'ALREADY_RESOLVED';
      stepState.solved = 'success';
      return 'ACTIVITY_CONFIRMED';
    }
    if (type === 'SUBMIT') {
      // Réémettre une réponse résolue n'ajoute aucun essai ni effet.
      if (stepState.solved) return 'ALREADY_RESOLVED';
      const correct = checkAnswer(current.defi, payload.answer);
      stepState.attempts += 1;
      if (correct) stepState.solved = 'success';
      return correct ? 'CORRECT' : 'INCORRECT';
    }
    if (type === 'HINT' || type === 'HELP') {
      requireCondition(current.defi.type !== 'INFORMATION', 'INVALID_ACTION', 'Cette activité libre ne demande pas d’aide à la résolution.');
      if (stepState.solved) return 'ALREADY_RESOLVED';
      requireCondition(stepState.attempts > 0, 'HELP_LOCKED', 'Essayez d’abord une réponse. L’indice et la solution seront ensuite disponibles.');
      if (type === 'HINT') stepState.hint = true;
      else stepState.solved = 'help';
      return type === 'HINT' ? 'HINT_REVEALED' : 'RESOLVED_WITH_HELP';
    }
    throw failure('INVALID_ACTION', 'Cette action n’existe pas dans la maquette.');
  }
  async function command(type, payload = {}) {
    requireCondition(!busy, 'REQUEST_PENDING', 'Une action est déjà en cours.');
    requireCondition(state.network !== 'offline', 'OFFLINE', 'Vous êtes hors connexion. Votre saisie est conservée ; aucune progression n’a été validée.');
    requireCondition(!state.pending || type === 'RECONCILE', 'UNCERTAIN', 'Le résultat de la dernière action est à vérifier avant de continuer.');
    const sentRevision = revision;
    busy = true;
    try {
      await new Promise(resolve => setTimeout(resolve, 500));
      requireCondition(sentRevision === revision, 'STALE_COMMAND', 'L’état de démonstration a changé. Consultez à nouveau l’écran.');
      requireCondition(state.network !== 'offline', 'OFFLINE', 'Connexion interrompue. L’action n’a pas été enregistrée.');
      if (type === 'RECONCILE') {
        const recovered = Boolean(state.pending);
        state.pending = null;
        record(type, recovered ? 'RECOVERED_WITHOUT_REPLAY' : 'UP_TO_DATE');
        save();
        return project();
      }
      requireCondition(payload && typeof payload === 'object' && !Array.isArray(payload), 'INVALID_PAYLOAD', 'Le format de cette action est invalide.');
      const confirmedProjection = state.network === 'next-lost' ? project() : null;
      const status = applyCommand(type, payload);
      record(type, status);
      if (state.network === 'next-lost') {
        state.network = 'online';
        state.pending = { type, at: new Date().toISOString(), confirmedProjection };
        save();
        throw failure('UNCERTAIN', 'La réponse du serveur a été perdue. Vérifiez le résultat sans renvoyer votre réponse.');
      }
      save();
      return project();
    } finally { busy = false; }
  }
  function setNetwork(mode) {
    requireCondition(['online', 'offline', 'next-lost'].includes(mode), 'INVALID_NETWORK', 'Mode de connexion inconnu.');
    state.network = mode;
    save();
    return project();
  }
  function setScenario(name) {
    const scenarios = ['debut', 'ordering', 'association', 'qcm', 'texte', 'code', 'information', 'erreur', 'indice',
      'attente-preuve', 'horsligne', 'incertain', 'neutralisation', 'terminee', 'regularisation', 'fermee', 'avant-debut'];
    requireCondition(scenarios.includes(name), 'INVALID_SCENARIO', 'Scénario de maquette inconnu.');
    requireCondition(name !== 'code' || Boolean(data.codeVariant), 'INVALID_SCENARIO', 'La mission alternative avec code n’est pas disponible.');
    revision += 1;
    state = freshState();
    state.variant = name === 'code' ? 'code' : 'standard';
    const target = { ordering: 1, association: 2, qcm: 3, texte: 4, code: 3, information: 5, erreur: 3, indice: 3,
      'attente-preuve': 1, horsligne: 3, incertain: 3, neutralisation: 2, terminee: 5, regularisation: 5, fermee: 5,
      'avant-debut': 0, debut: 0 }[name];
    state.current = Math.min(target, data.steps.length - 1);
    if (name !== 'debut') {
      state.registered = true;
      state.email = 'camille@example.test';
      for (let index = 0; index < state.current; index += 1) {
        state.steps[index].solved = 'success';
        state.steps[index].proof = effectiveStep(index).kind !== 'VIRTUAL';
      }
      if (effectiveStep(state.current).kind === 'POI' && name !== 'avant-debut') state.steps[state.current].proof = true;
    }
    const active = state.steps[state.current];
    if (['erreur', 'indice'].includes(name)) active.attempts = 1;
    if (name === 'indice') active.hint = true;
    if (name === 'attente-preuve') { active.solved = 'success'; active.attempts = 1; }
    if (name === 'horsligne') state.network = 'offline';
    if (name === 'incertain') {
      active.proof = true;
      const confirmedProjection = project();
      active.solved = 'success'; active.attempts = 1;
      state.pending = { type: 'SUBMIT', at: new Date().toISOString(), confirmedProjection };
    }
    if (name === 'neutralisation') active.bypassed = true;
    if (['terminee', 'regularisation', 'fermee'].includes(name)) {
      state.steps.forEach((step, index) => { step.solved = 'success'; step.proof = effectiveStep(index).kind !== 'VIRTUAL'; });
    }
    if (name === 'regularisation') state.steps[1].proof = false;
    if (name === 'fermee') state.closed = true;
    if (name === 'avant-debut') state.started = false;
    record('SCENARIO', name);
    save();
    return project();
  }
  function reset() {
    revision += 1;
    state = freshState();
    save();
    return project();
  }
  function subscribe(fn) {
    if (typeof fn !== 'function') throw new TypeError('Une fonction de réception est attendue.');
    subscribers.add(fn);
    return () => subscribers.delete(fn);
  }
  window.addEventListener('storage', event => {
    if (event.key !== STORAGE_KEY) return;
    const incoming = readStorage();
    if (!incoming) return;
    revision += 1;
    state = incoming;
    for (const fn of subscribers) fn(project());
  });
  window.LiveMockAPI = Object.freeze({ getState: () => clone(state), project, command, setScenario, setNetwork, reset, subscribe });
})();
