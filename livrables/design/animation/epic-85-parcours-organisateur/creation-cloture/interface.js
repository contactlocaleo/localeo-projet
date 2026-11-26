'use strict';
const demo = JSON.parse(document.getElementById('scenario').textContent);
const main = document.querySelector('main');
const names = ['Création', 'Règles', 'Préparation', 'Publication', 'Déroulement', demo.id==='avent'?'Clôture du jour':'Clôture', ...apresCloture.labels(demo)];
const routes = ['creation','regles','preparation','publication','deroulement','cloture','tirage','gains'];
const journey = {
  page: 0, unlocked: 0, created: false, published: false, closed: false, confirm: false,
  prepCount: 0, examined: false, detail: false, notice: '', title: demo.title,
  start: demo.dates[0], end: demo.dates[1], brief: demo.brief, presentation: demo.intro,
};
let state = journey;
const previews = new Map();
const drafts = new WeakMap();
const safe = val => String(val ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
const action = (key, label, style='primary') => '<button type="button" data-act="'+key+'" class="'+style+'">'+safe(label)+'</button>';
const receipt = message => '<p class="ok" role="status">'+safe(message)+'</p>';
const rowTable = (columns, rows) => '<table><thead><tr>'+columns.map(x=>'<th scope="col">'+safe(x)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map((v,i)=>'<td data-label="'+safe(columns[i])+'">'+safe(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';
const measures = pairs => '<div class="metrics">'+pairs.map(([v,l])=>'<div><b>'+safe(v)+'</b><small>'+safe(l)+'</small></div>').join('')+'</div>';
const date = iso => new Intl.DateTimeFormat('fr-FR',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(iso+'T12:00:00Z'));
const heading = (title,lead='') => '<h2 id="work-title" tabindex="-1">'+safe(title)+'</h2>'+(lead?'<p class="lead">'+safe(lead)+'</p>':'');
const actions = html => '<div class="actions">'+html+'</div>';
const intro = demo.prospect ? 'Simulation d’un modèle en projet' : 'Simulation du parcours organisateur';
function statusLabel(){
  if(state.editionFinished) return 'Édition terminée';
  if(demo.id==='avent' && state.closed) return state.page===7?'Suivi du calendrier':'Case clôturée';
  if(state.closed) return demo.finalStatus || 'Édition clôturée';
  if(demo.id==='vitrines' && state.page===4 && !state.runResumed) return 'Jeu suspendu';
  if(state.published) return state.page===5?'Fin de période':'Édition publiée';
  if(state.created) return demo.assisted && !state.prepCount?'Demande transmise':'En préparation';
  return 'Nouvelle édition';
}
function examples(){
  const key=['Création','Règles','Préparation','Publication','Suivi','Clôture'][state.page];
  const cases=demo.cases.filter(c=>c.phase===key);
  if(!cases.length)return '';
  return '<details class="alternatives"><summary>Autres situations à cette étape ('+cases.length+')</summary>'+cases.map(c=>'<details class="case"><summary>'+safe(c.title)+'</summary><p>'+safe(c.context)+'</p><details><summary>'+safe(c.action)+'</summary>'+receipt(c.result)+'</details></details>').join('')+'</details>';
}
function creation(){
  const locked=state.created?' readonly':'';
  const dateLock=demo.id==='avent'?' readonly':locked;
  return heading(demo.assisted?'Préparer la demande':'Créer l’édition',demo.intro)+'<div class="split"><form id="creation"><div class="fields"><label>Nom de l’animation<input name="title" required maxlength="120" value="'+safe(state.title)+'"'+locked+'></label><label>Premier jour<input name="start" type="date" required value="'+safe(state.start)+'"'+dateLock+'></label><label>Dernier jour<input name="end" type="date" required value="'+safe(state.end)+'"'+dateLock+'></label></div>'+
  (demo.assisted?'<label class="longfield">Brief pour la préparation<textarea name="brief" required rows="3"'+locked+'>'+safe(state.brief)+'</textarea></label>':'')+
  actions(state.created?action('next','Retrouver les règles de l’édition'):'<button class="primary" type="submit">'+safe(demo.operation)+'</button>')+'</form><aside class="aside"><h3>'+safe(demo.name)+'</h3><p>'+safe(demo.prospect?'Parcours prospectif à Latresne.':'Commune organisatrice · Latresne')+'</p><ul>'+demo.settings.slice(0,3).map(([k,v])=>'<li>'+safe(k)+' · '+safe(v)+'</li>').join('')+'</ul></aside></div>';
}
function rules(){
  return heading('Règles et présentation','Relisez les conditions de cette édition et préparez le texte présenté aux habitants.')+
  rowTable(['Paramètre','Valeur dans cette édition'],demo.settings)+
  '<form id="rules"><label class="longfield">Présentation de l’animation<textarea rows="2" name="copy" required maxlength="700" '+(state.published?'readonly':'')+'>'+safe(state.presentation)+'</textarea></label>'+
  actions('<button class="primary" type="submit">'+(state.published?'Retrouver la préparation':'Enregistrer et préparer l’édition')+'</button>')+'</form>';
}
function preparation(){
  const i=state.prepCount, task=demo.prep[i], finished=!task||state.published;
  const steps='<aside class="aside"><h3>Préparation de cette édition</h3><ol class="tasklist">'+demo.prep.map((v,n)=>'<li><b>'+safe(v.title)+'</b><small>'+ (n<i?'Traité':v.optional?'Facultatif':n===i?'En cours':'À suivre')+'</small></li>').join('')+'</ol></aside>';
  return '<div class="split"><section>'+heading(finished?'Préparation terminée':task.title,finished?'Retrouvez les conditions de publication et l’aperçu destiné aux habitants.':task.context)+
  (!finished&&demo.prepPreview.at===i?rowTable(demo.prepPreview.columns,demo.prepPreview.rows):'')+
  (i?receipt(demo.prep[i-1].result):'')+actions(finished?action('next','Vérifier la publication'):action('task',task.action)+(task.optional?action('next','Ouvrir la revue de publication','plain'):''))+'</section>'+steps+'</div>';
}
function publication(){
  const s=demo.publish;
  const rows=s.rows.map(row=>/^(communes? et dates|dates|période)$/i.test(row[0])?[row[0],'Latresne · '+date(state.start)+' – '+date(state.end),row[2]]:row);
  if(state.published)return heading('Édition publiée',state.presentation)+receipt(s.effect)+actions(action('next','Ouvrir le suivi de l’édition'));
  return heading(s.title,s.lead)+measures(s.metrics)+rowTable(s.columns,rows)+
    '<details class="alternatives"><summary>Aperçu pour les habitants</summary><h3>'+safe(state.title)+'</h3><p>'+safe(state.presentation)+'</p><p>'+date(state.start)+' – '+date(state.end)+'</p></details>'+
    (state.confirm?'<section class="warning"><h3>Publier cette édition ?</h3><p>La version présentée sera publiée pour la période affichée.</p>'+actions(action('publish','Confirmer la publication')+action('cancel','Annuler',''))+'</section>':actions(action('ask','Publier l’animation')+action('editRules','Modifier la présentation','plain')));
}
function closure(){
  const s=demo.close;
  const daily=demo.id==='avent', narrative=demo.id==='escape-game';
  const nextLabel=narrative?'Consulter les réussites de la mission':daily?'Consulter le tirage du 5 décembre':'Préparer le tirage';
  if(state.closed)return heading(demo.finalStatus||'Édition clôturée',state.title)+receipt(s.effect)+measures(s.metrics)+
    rowTable(daily?['Journée','Population examinée']:['Édition','Période examinée'],[daily?['5 décembre',s.metrics[0][0]+' participations dans cette case']:[state.title,date(state.start)+' – '+date(state.end)]])+
    actions(action('next',nextLabel)+'<a class="return" href="exploitation.html">Revenir aux modèles</a>');
  if(state.confirm)return heading(demo.finalQuestion||'Confirmer la clôture de cette édition ?',state.title)+measures(s.metrics)+
    '<section class="warning"><h3>Effet de la confirmation</h3><p>'+safe(demo.finalNote||'Les inscriptions et les validations seront fermées. La liste des éligibles sera figée et pourra être contrôlée avant le tirage.')+'</p>'+
    actions(action('close',demo.finalButton||'Confirmer la clôture')+action('cancel','Revenir au contrôle',''))+'</section>';
  return heading(s.title,s.lead)+measures(s.metrics)+rowTable(s.columns,s.rows)+
    actions(action('ask',demo.finalAction||'Clôturer l’animation')+action('inspectRun',daily?'Vérifier les dossiers de la journée':'Vérifier les dossiers du déroulement','plain'));
}
function draw(focus=true){
  const p=state.page;
  const plan=p<4?'planches/'+demo.id+'.png':'planches/exploitation-'+demo.id+'.png';
  const render=[creation,rules,preparation,publication,()=>deroulement.render(demo,state),closure,()=>apresCloture.render(demo,state),()=>apresCloture.render(demo,state)];
  main.innerHTML='<div class="crumbs"><a href="'+(p<4?'index.html':'exploitation.html')+'">Tous les modèles</a><span aria-hidden="true">/</span>'+safe(demo.name)+(demo.prospect?' · Modèle en projet':'')+'<a class="overview" href="'+plan+'">'+(p<4?'Voir la création jusqu’à la clôture en images':'Voir le déroulement et la fin en images')+'</a></div><div class="identity"><h1>'+safe(state.title)+'</h1><span class="tag">'+safe(statusLabel())+'</span></div>'+
  '<section class="box"><nav class="rail" aria-label="Accès direct aux écrans de gestion">'+names.map((n,i)=>'<button type="button" data-page="'+i+'"'+(i===p?' aria-current="step"':'')+'><span>'+ (i<journey.unlocked?'✓':(i+1))+'</span>'+safe(n)+'</button>').join('')+'</nav><div class="inside"><div class="kicker">'+safe(state===journey?intro:'Aperçu · '+demo.name)+' · Vue '+(p+1)+' sur '+names.length+'</div>'+
  (state.notice?receipt(state.notice):'')+render[p]()+((state.closed&&p===5)||p>5?'':examples())+'</div></section>';
  const form=main.querySelector('form');
  if(form)for(const [name,value] of Object.entries(drafts.get(state)?.[form.id]||{})){
    if(!form.elements[name].readOnly)form.elements[name].value=value;
  }
  if(focus)main.querySelector('#work-title')?.focus({preventScroll:true});
}
function openPage(p){
  if(p===state.page)return;
  const form=main.querySelector('form');
  if(form){
    const data=drafts.get(state)||{};
    data[form.id]=Object.fromEntries(new FormData(form));
    drafts.set(state,data);
  }
  if(p<=journey.unlocked){
    state=journey;
  }else{
    // Each future stage has its own sample edition. Browsing cannot advance the guided edition.
    if(!previews.has(p)){
      const sample={
        ...structuredClone(journey), page:p, unlocked:p, created:true, published:p>=4, closed:p>=6,
        prepCount:p>=3?demo.prep.length:0, detail:false, confirm:false, notice:'',
        runResumed:demo.id==='vitrines' && p>4
      };
      apresCloture.initPreview(demo,sample,p);
      previews.set(p,sample);
    }
    state=previews.get(p);
  }
  go(p);
}
function go(p,notice=''){
  state.page=p;state.confirm=false;state.notice=notice;
  if(state!==journey && p>journey.unlocked)previews.set(p,state);
  draw();
}
function advance(notice=''){
  const next=state.page+1;state.unlocked=Math.max(state.unlocked,next);go(next,notice);
}
main.addEventListener('submit',e=>{
  e.preventDefault();const f=e.target;
  if(f.id==='creation'){
    const x=f.elements;
    x.title.setCustomValidity(x.title.value.trim()?'':'Saisissez un nom pour cette édition.');
    x.end.setCustomValidity(x.end.value>=x.start.value?'':'Choisissez une fin à partir du premier jour.');
    if(x.brief)x.brief.setCustomValidity(x.brief.value.trim()?'':'Décrivez la mission à préparer.');
    if(!f.reportValidity())return;
    state.title=x.title.value.trim();state.start=x.start.value;state.end=x.end.value;state.brief=x.brief?.value.trim()||'';state.created=true;drafts.delete(state);
    advance(demo.assisted?'Demande transmise dans la simulation. La préparation reprend sur la version reçue de Localeo.':'Brouillon créé pour la commune de Latresne.');
  }else if(f.id==='rules'){
    const field=f.elements.copy;field.setCustomValidity(field.value.trim()?'':'Saisissez une présentation.');if(!f.reportValidity())return;
    state.presentation=field.value.trim();drafts.delete(state);advance(state.published?'':'Présentation enregistrée pour cette édition.');
  }
});
main.addEventListener('input',e=>{if(e.target.setCustomValidity)e.target.setCustomValidity('');if(e.target.name==='start')e.target.form.elements.end.setCustomValidity('')});
main.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b||b.disabled)return;
  if(b.hasAttribute('data-page')){openPage(Number(b.dataset.page));return}
  if(state.page===4 && deroulement.click(b.dataset.act,demo,state)){
    if(!deroulement.refreshList(demo,state,b.dataset.act))draw();
    return;
  }
  if(state.page>=6 && apresCloture.click(b.dataset.act,demo,state)){
    state.notice='';draw();return;
  }
  switch(b.dataset.act){
    case 'next':advance();return;
    case 'inspectRun':go(4);return;
    case 'editRules':go(1);return;
    case 'task':state.prepCount++;break;
    case 'ask':state.confirm=true;break;
    case 'cancel':state.confirm=false;break;
    case 'publish':state.published=true;state.confirm=false;state.unlocked=4;break;
    case 'detail':state.detail=true;break;
    case 'close':state.closed=true;state.confirm=false;state.unlocked=Math.max(state.unlocked,6);break;
    case 'restart':location.reload();return;
    default:return;
  }
  state.notice='';draw();
});
const entry=routes.indexOf(location.hash.slice(1));
if(entry>0)openPage(entry);else draw(false);
