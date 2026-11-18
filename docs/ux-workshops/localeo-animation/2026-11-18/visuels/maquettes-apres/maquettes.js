'use strict';
const controls=[...document.querySelectorAll('[data-state]')];
const panels=[...document.querySelectorAll('[data-panel]')];
document.querySelectorAll('table').forEach(table=>{
 table.classList.add('responsive');table.setAttribute('role','table');
 const headings=[...table.querySelectorAll('thead th')].map(h=>h.textContent);
 table.querySelectorAll('tbody tr').forEach(row=>{
  row.setAttribute('role','row');
  [...row.children].forEach((cell,i)=>{
   if(cell.tagName==='TD'){
    cell.setAttribute('role','cell');
    const label=document.createElement('span');label.className='mobile-cell-label';label.setAttribute('aria-hidden','true');label.textContent=headings[i]||'';cell.prepend(label);
   }else cell.setAttribute('scope','row');
  });
 });
});
function showState(name,focus=false){
 if(!panels.some(p=>p.dataset.panel===name))return;
 panels.forEach(p=>p.hidden=p.dataset.panel!==name);
 const active=panels.find(p=>p.dataset.panel===name);if(active?.dataset.heading)document.querySelector('h1').textContent=active.dataset.heading;
 controls.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===name)));
 if(focus){const h=document.querySelector('[data-panel]:not([hidden]) h2');if(h){h.tabIndex=-1;h.focus({preventScroll:true});h.scrollIntoView({block:'nearest'});}}
 const u=new URL(location.href);u.searchParams.set('etat',name);history.replaceState(null,'',u);
}
controls.forEach(b=>b.addEventListener('click',()=>showState(b.dataset.state)));
document.querySelectorAll('[data-goto]').forEach(b=>b.addEventListener('click',()=>showState(b.dataset.goto,true)));
document.querySelectorAll('[data-dialog]').forEach(b=>b.addEventListener('click',()=>document.getElementById(b.dataset.dialog).showModal()));
document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
document.querySelectorAll('[data-unlock]').forEach(b=>b.addEventListener('change',()=>{document.getElementById(b.dataset.unlock).disabled=!b.checked;}));
document.querySelectorAll('form').forEach(f=>f.addEventListener('submit',e=>e.preventDefault()));
showState(new URL(location.href).searchParams.get('etat')||panels[0]?.dataset.panel);
