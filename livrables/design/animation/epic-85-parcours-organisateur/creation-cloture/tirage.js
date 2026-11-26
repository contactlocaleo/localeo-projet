'use strict';
// Jeu de démonstration hors ligne. Les attributions reproduisent des résultats fictifs.
const apresCloture = (() => {
  const editions = {
    passeport: {eligible:8, kind:'externe', allocations:[
      ['Panier du marché · 1','Camille Martin','Accueil de la mairie'],
      ['Panier du marché · 2','Inès Robin','Accueil de la mairie']]},
    'tombola-locale': {eligible:18, kind:'coffret', allocations:[
      ['Coffret découverte · 1','Nina Robert','Distribution des Coffrets'],
      ['Coffret découverte · 2','Paul David','Distribution des Coffrets']]},
    'tombola-publique': {eligible:21, kind:'bon', allocations:[
      ['Panier de saison · bon 1','Alice Durand','Épicerie du Pont'],
      ['Panier de saison · bon 2','Tom Mercier','Épicerie du Pont']]},
    chasse: {eligible:14, kind:'externe', allocations:[
      ['Le livre des contes','Jules Blanc','Lisons sous la pluie'],
      ['Panier des saveurs','Noé Lamy','Chez Mirga'],
      ['Écharpe d’automne','Participant CH-018','Chez Mode de Biche'],
      ['Lanterne décorative','Participant CH-020','À la mairie']]},
    prix: {eligible:12, kind:'externe', allocations:[
      ['Coffret de miel','Marc Noël','Épicerie du Pont'],
      ['Duo de tasses','Nils Adam','Atelier Argile'],
      ['Panier du boulanger','Participant JP-019','Fournil du Bourg'],
      ['Bougie de saison','Participant JP-024','Maison Cire']]},
    vitrines: {eligible:16, kind:'externe', allocations:[
      ['Roman illustré','Participant VI-003','Librairie du Bourg'],
      ['Bouquet de saison','Participant VI-009','Atelier des fleurs'],
      ['Assortiment de thés','Participant VI-012','Maison des thés'],
      ['Étui à lunettes','Participant VI-015','Optique du Centre']]},
    'mots-croises': {eligible:12, kind:'externe', allocations:[
      ['Panier du quartier','Participant MC-007','Accueil de la mairie']]}
  };
  const days = [
    {date:'4 décembre', commerce:'Librairie du Bourg', entries:29, gift:'Coffret Lecture'},
    {date:'5 décembre', commerce:'Atelier des Saveurs', entries:34, gift:'Coffret Gourmand'},
    {date:'6 décembre', commerce:'Épicerie du Pont', entries:27, gift:'Coffret Découverte'}
  ];
  function fresh(variant='nominal'){
    return {variant, phase:'ready', resolved:[], sent:[], opened:null, proof:false, reason:false,
      noWinnerReason:false, confirmEnd:false, day:1, dayPhase:'ready', daySent:false, narrative:false};
  }
  function ctx(state){
    return state.afterDraw || (state.afterDraw=fresh());
  }
  function labels(demo){
    if(demo.id==='escape-game')return ['Résultats','Bilan'];
    if(demo.id==='avent')return ['Tirages par case','Distribution'];
    return ['Tirage','Gains et fin'];
  }
  function initPreview(demo,state,page){
    state.afterDraw=fresh();
    state.editionFinished=false;
    if(page===7 && editions[demo.id])state.afterDraw.phase='done';
    if(page===7 && demo.id==='avent')state.afterDraw.dayPhase='done';
  }
  function population(s,c){
    if(c.variant==='aucun')return 0;
    if(c.variant==='rare')return 1;
    return s.eligible;
  }
  function counts(s,c){
    const eligible=population(s,c), total=s.allocations.length;
    const blocked=s.kind==='coffret' && eligible<total;
    const winners=blocked?0:Math.min(eligible,total);
    return {eligible,total,blocked,winners,remaining:total-winners};
  }
  function otherCases(s,c){
    return '<details class="alternatives"><summary>Explorer un autre cas de tirage</summary>'+
      '<p class="note">Chaque cas utilise une autre population fictive, déjà clôturée.</p>'+
      actions((c.variant==='nominal'?'':action('draw-case-nominal','Population de l’édition','plain'))+
        (c.variant==='aucun'?'':action('draw-case-aucun','Aucun éligible','plain'))+
        (s.allocations.length>1 && c.variant!=='rare'?action('draw-case-rare','Un seul éligible','plain'):'')+
        (c.variant==='incertain'?'':action('draw-case-incertain','Réponse perdue à la confirmation','plain')))+'</details>';
  }
  function drawScreen(demo,state){
    const s=editions[demo.id], c=ctx(state), n=counts(s,c);
    if(c.phase==='done'){
      const result=s.allocations.slice(0,n.winners).map(([lot,winner,place])=>[lot,winner,place]);
      return heading(n.winners?'Tirage confirmé':'Tirage confirmé sans gagnant',state.title)+
        measures([[n.eligible,'Participants éligibles'],[n.winners,'Lots attribués'],[n.remaining,'Exemplaires sans gagnant']])+
        (result.length?rowTable(['Lot attribué','Bénéficiaire','Circuit de remise'],result):
        '<p class="note">La liste figée ne contient aucun participant qualifié. Le résultat est enregistré et les unités sans gagnant restent à justifier.</p>')+
        actions(action('next',state.editionFinished?'Voir le bilan final':'Ouvrir les dossiers de gains'));
    }
    if(c.phase==='uncertain'){
      return heading('Réponse du tirage en attente','La confirmation a été transmise. Consultez le résultat de cette opération avant toute autre intervention.')+
        '<p class="warning" role="status">L’attribution doit encore être vérifiée.</p>'+actions(action('draw-read','Relire le résultat du tirage'));
    }
    const summary=measures([[n.eligible,'Participants éligibles'],[n.total,'Exemplaires à attribuer']]);
    if(n.blocked){
      return heading('Tirage Coffrets indisponible','Cette dotation requiert autant de personnes distinctes que de Coffrets réservés.')+summary+
        '<p class="warning" role="status">La population figée est insuffisante. Les Coffrets restent réservés et aucune attribution n’est enregistrée.</p>'+otherCases(s,c);
    }
    if(c.phase==='confirm'){
      return heading('Confirmer le tirage de cette édition ?',state.title)+summary+
        '<p class="warning">'+safe(n.winners?'La confirmation attribuera '+n.winners+' lot'+(n.winners>1?'s':'')+' parmi les participants éligibles. Le résultat sera conservé.':'La confirmation enregistrera un tirage sans gagnant.')+'</p>'+
        actions(action('draw-submit','Confirmer le tirage')+action('draw-cancel','Annuler',''));
    }
    return heading('Vérifier le tirage',demo.id==='mots-croises'?'Scénario prospectif. Chaque grille correcte accompagnée de tous les passages requis donne une chance.':'La clôture a figé la population de cette édition. Chaque personne qualifiée dispose d’une chance dans cet exemple.')+
      summary+rowTable(['Exemplaire','Circuit de remise'],s.allocations.map(([lot,,place])=>[lot,place]))+
      (n.remaining?'<p class="note">'+n.winners+' attribution(s) possible(s). Les autres exemplaires seront à justifier.</p>':'')+
      actions(action('draw-review','Passer à la confirmation'))+otherCases(s,c);
  }
  function proofLabels(kind){
    if(kind==='coffret')return {todo:'À distribuer',wait:'Envoi effectué · réception à attester',done:'Réception attestée',ask:'Attester la réception',confirm:'Confirmer la réception'};
    if(kind==='bon')return {todo:'À retirer',done:'Bon consommé dans Pro',ask:'Consulter le retrait dans Pro',confirm:'Simuler le retrait confirmé par le commerce'};
    return {todo:'À remettre',done:'Remise déclarée',ask:'Déclarer la remise',confirm:'Confirmer la remise du lot'};
  }
  function gainsScreen(demo,state){
    const c=ctx(state),s=editions[demo.id],n=counts(s,c),pr=proofLabels(s.kind);
    if(c.phase!=='done')return heading('Attributions en attente','La liste des bénéficiaires sera disponible après confirmation du tirage.')+actions('<button type="button" data-page="6" class="primary">Revenir au tirage</button>');
    const rows=s.allocations.slice(0,n.winners);
    const status=i=>c.resolved[i]==='reason'?'Dossier clôturé sur décision motivée':c.resolved[i]?pr.done:c.sent[i]?pr.wait:pr.todo;
    const unresolved=rows.filter((_,i)=>!c.resolved[i]).length;
    const allDone=unresolved===0 && (!n.remaining || c.noWinnerReason);
    if(state.editionFinished){
      return heading('Édition terminée','La décision de fin est enregistrée dans cette simulation. Les preuves de traitement restent consultables.')+
        measures([[n.eligible,'Éligibles à la clôture'],[n.winners,'Lots attribués'],[0,'Dossiers à résoudre']])+
        (rows.length?rowTable(['Lot','Bénéficiaire','État final'],rows.map(([lot,winner],i)=>[lot,winner,status(i)])):'')+
        (n.remaining?receipt(n.remaining+' exemplaire(s) sans gagnant justifié(s).'):'')+actions('<a class="return" href="index.html">Choisir un autre modèle</a>');
    }
    if(c.confirmEnd){
      return heading('Terminer cette animation ?',state.title)+receipt('Tous les dossiers de gains et les exemplaires sans gagnant sont résolus.')+
        '<p class="note">La fin fige la gestion de l’édition et conserve son bilan.</p>'+actions(action('gain-end','Confirmer la fin de l’animation')+action('gain-cancel-end','Annuler',''));
    }
    if(c.opened!==null){
      const i=c.opened,[lot,winner,place]=rows[i];
      let controls='';
      if(!c.resolved[i]){
        if(c.reason){
          controls='<section class="warning"><h3>Clôturer ce dossier de gain ?</h3><p>Motif de l’exemple : renonciation confirmée du bénéficiaire.'+
          (s.kind==='bon'?' Le bon numérique sera révoqué.':'')+'</p>'+actions(action('gain-confirm-reason','Confirmer la clôture motivée')+action('gain-cancel-proof','Annuler',''))+'</section>';
        }else if(c.proof){
          const note=s.kind==='bon'?'Dans cet exemple, le commerçant confirme dans Pro un retrait autorisé. Animation relit la consommation enregistrée.':s.kind==='coffret'?'Le bénéficiaire a confirmé la réception. L’attestation complète le dossier.':'Le bénéficiaire a retiré le lot au lieu indiqué. Enregistrez la remise dans son dossier.';
          controls='<section class="warning"><p>'+note+'</p>'+actions(action('gain-confirm-proof',pr.confirm)+action('gain-cancel-proof','Annuler',''))+'</section>';
        }else{
          controls=actions((s.kind==='coffret'&&!c.sent[i]?action('gain-send','Simuler l’envoi du Coffret'):action('gain-proof',pr.ask))+action('gain-reason','Clôturer le dossier avec un motif','plain'));
        }
      }
      return heading(lot,winner)+rowTable(['Lieu ou circuit','État du dossier'],[[place,status(i)]])+controls+
        actions(action('gain-back','Retour aux dossiers','plain'));
    }
    const list=rows.length?rowTable(['Bénéficiaire','Lot','Traitement'],rows.map(([lot,winner],i)=>[winner,lot,status(i)])):'';
    return heading('Traiter les gains avant la fin',s.kind==='coffret'?'Suivez l’envoi puis la réception de chaque Coffret.':s.kind==='bon'?'Le commerce valide le retrait dans Pro. Le dossier présente la consommation effective du bon.':'Pour chaque lot, déclarez la remise ou consignez une décision motivée.')+
      measures([[n.winners,'Lots attribués'],[unresolved,'Dossiers à résoudre'],[n.remaining,'Exemplaires sans gagnant']])+list+
      (rows.length?actions(rows.map(([,w],i)=>action('gain-open-'+i,'Dossier de '+w,'plain')).join('')):'')+
      (n.remaining?(c.noWinnerReason?receipt('Unités sans gagnant justifiées · population éligible insuffisante.'):
        '<section class="warning"><h3>Justifier les exemplaires sans gagnant</h3><p>'+n.remaining+' exemplaire(s) de la dotation publiée restent sans bénéficiaire. Motif de l’exemple : population figée insuffisante.</p>'+actions(action('gain-justify','Enregistrer la justification'))+'</section>'):'')+
      (allDone?actions(action('gain-review-end','Terminer l’animation')): '<p class="note">La fin sera disponible lorsque les dossiers ouverts et les exemplaires sans gagnant auront été traités.</p>');
  }
  function advent(demo,state){
    const c=ctx(state),d=days[c.day];
    if(state.page===7){
      if(c.parentReviewed)return heading('Revue de fin du calendrier','Exemple au 24 décembre. Les 24 cases de cette édition sont fermées. Le tableau détaille un extrait de trois journées.')+
        measures([[24,'Cases fermées'],[90,'Participations sur ces trois cases'],[3,'Coffrets envoyés dans cet extrait']])+
        rowTable(['Journée','Participations','Coffret envoyé'],days.map(v=>[v.date,v.entries,v.gift]))+
        '<p class="note">La commande et les conditions de clôture du calendrier parent restent à préciser dans E54.</p>'+actions('<a class="return" href="index.html">Choisir un autre modèle</a>');
      return heading('Distribuer le Coffret du 5 décembre','Le Coffret Gourmand est attribué au bénéficiaire de cette case. Suivez son envoi indépendamment des autres journées.')+
        rowTable(['Journée','Coffret','Distribution'],[['4 décembre',days[0].gift,'Envoyé'],['5 décembre',days[1].gift,c.daySent?'Envoyé':'Envoi en attente'],['6 décembre',days[2].gift,'Case à venir']])+
        (c.daySent?receipt('L’envoi du 5 décembre est confirmé pour cette attribution.')+actions(action('gain-day-parent','Voir la revue après la dernière case')):
        actions(action('gain-day-send','Simuler l’envoi du Coffret du 5 décembre')));
    }
    const picker=actions(days.map((v,i)=>'<button type="button" data-act="draw-day-'+i+'" aria-pressed="'+(i===c.day)+'" class="'+(i===c.day?'primary':'')+'">'+v.date+'</button>').join(''));
    const top=heading('Tirages par journée','Dans cette édition prospective, chaque case dispose de sa propre population et de sa propre dotation. Le déclenchement et la reprise des tirages restent à arbitrer dans E54.')+picker;
    if(c.day===2)return top+rowTable(['Case à venir','Commerce','Coffret réservé'],[[d.date,d.commerce,d.gift]])+'<p class="note">La population de cette journée sera connue à sa clôture.</p>';
    const info=measures([[d.entries,'Participations de la case'],[1,'Coffret pour cette journée']])+rowTable(['Case consultée','Commerce','Dotation'],[[d.date,d.commerce,d.gift]]);
    if(c.day===0)return top+info+receipt('Tirage du 4 décembre confirmé. Le Coffret Lecture a été envoyé.')+actions(action('draw-day-1','Revenir à la case du 5 décembre'));
    if(c.dayPhase==='done')return top+info+receipt('Tirage du 5 décembre confirmé. Le Coffret Gourmand est attribué à un bénéficiaire de cette case.')+actions(action('next','Suivre l’envoi du Coffret'));
    if(c.dayPhase==='confirm')return top+info+'<p class="warning">Dans cette simulation, le tirage désignera un bénéficiaire du Coffret Gourmand parmi les 34 participations du 5 décembre.</p>'+actions(action('draw-day-submit','Simuler la confirmation du tirage quotidien')+action('draw-day-cancel','Annuler',''));
    return top+info+actions(action('draw-day-review','Préparer le tirage du 5 décembre'));
  }
  function escapeGame(demo,state){
    const c=ctx(state);
    if(state.page===7)return heading('Bilan de la mission','Les résultats portent sur les progressions suivies sur un téléphone.')+
      measures([[24,'Parties commencées'],[13,'Finales réussies'],[11,'Parties inachevées']])+
      rowTable(['Indicateur','Portée'],[['Mission accomplie','Coffre virtuel ouvert'],['Mode de récompense','Arbitrage E79 ouvert']])+actions('<a class="return" href="index.html">Choisir un autre modèle</a>');
    return heading('Résultats de la mission','La réussite de la finale clôt le récit dans cet exemple. La règle de qualification et le mode de récompense relèvent de l’arbitrage E79.')+
      rowTable(['Situation de jeu','Parties'],[['Finale réussie','13'],['Mission en cours à l’échéance','11']])+
      (c.narrative?receipt('Les 13 ouvertures du coffre virtuel sont des réussites narratives. Aucun lot à distribuer dans cette simulation.'):
       actions(action('draw-narrative','Examiner le résultat de la finale')))+actions(action('next','Consulter le bilan de la mission',c.narrative?'primary':'plain'));
  }
  function render(demo,state){
    if(demo.id==='avent')return advent(demo,state);
    if(demo.id==='escape-game')return escapeGame(demo,state);
    return state.page===6?drawScreen(demo,state):gainsScreen(demo,state);
  }
  function click(key,demo,state){
    if(!key || (!key.startsWith('draw-')&&!key.startsWith('gain-')))return false;
    const c=ctx(state);
    if(state.editionFinished)return true;
    if(demo.id==='escape-game'){if(key==='draw-narrative')c.narrative=true;return true}
    if(demo.id==='avent'){
      if(/^draw-day-[0-2]$/.test(key)){
        c.day=Number(key.slice(-1));
        if(c.dayPhase==='confirm')c.dayPhase='ready';
      }
      if(c.day===1 && key==='draw-day-cancel' && c.dayPhase==='confirm')c.dayPhase='ready';
      if(c.day===1 && key==='draw-day-review' && c.dayPhase==='ready')c.dayPhase='confirm';
      if(c.day===1 && key==='draw-day-submit' && c.dayPhase==='confirm')c.dayPhase='done';
      if(key==='gain-day-send' && c.dayPhase==='done')c.daySent=true;
      if(key==='gain-day-parent' && c.daySent)c.parentReviewed=true;
      return true;
    }
    const s=editions[demo.id], n=counts(s,c);
    if(key.startsWith('draw-case-')&&c.phase==='ready'){
      const variant=key.slice('draw-case-'.length);
      if(['nominal','rare','aucun','incertain'].includes(variant))state.afterDraw=fresh(variant);
      return true;
    }
    if(key==='draw-review'&&c.phase==='ready'&&!n.blocked)c.phase='confirm';
    if(key==='draw-cancel'&&c.phase==='confirm')c.phase='ready';
    if(key==='draw-submit'&&c.phase==='confirm')c.phase=c.variant==='incertain'?'uncertain':'done';
    if(key==='draw-read'&&c.phase==='uncertain')c.phase='done';
    if(c.phase!=='done')return true;
    if(/^gain-open-\d+$/.test(key)){
      const i=Number(key.slice('gain-open-'.length));
      if(i<n.winners){c.opened=i;c.reason=false;c.proof=false}
    }
    if(key==='gain-back'){c.opened=null;c.reason=false;c.proof=false}
    if(c.opened!==null&&!c.resolved[c.opened]){
      if(key==='gain-send'&&s.kind==='coffret')c.sent[c.opened]=true;
      if(key==='gain-proof'&&(s.kind!=='coffret'||c.sent[c.opened]))c.proof=true;
      if(key==='gain-confirm-proof'&&c.proof){c.resolved[c.opened]='proof';c.proof=false}
      if(key==='gain-reason')c.reason=true;
      if(key==='gain-confirm-reason'&&c.reason){c.resolved[c.opened]='reason';c.reason=false}
      if(key==='gain-cancel-proof'){c.proof=false;c.reason=false}
    }
    if(key==='gain-justify'&&n.remaining)c.noWinnerReason=true;
    if(key==='gain-review-end'&&c.resolved.filter(Boolean).length===n.winners&&(!n.remaining||c.noWinnerReason))c.confirmEnd=true;
    if(key==='gain-cancel-end')c.confirmEnd=false;
    if(key==='gain-end'&&c.confirmEnd){c.confirmEnd=false;state.editionFinished=true}
    return true;
  }
  return {render,click,labels,initPreview};
})();
