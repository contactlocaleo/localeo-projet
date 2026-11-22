'use strict';
document.documentElement.classList.add('js');
const articles=[...document.querySelectorAll('article[data-orientation]')];
document.querySelectorAll('[data-compare]').forEach(button=>button.addEventListener('click',()=>{
 const article=button.closest('article');article.dataset.show=button.dataset.compare;
 article.querySelectorAll('[data-compare]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
}));
const priority=document.querySelector('#priority'),mission=document.querySelector('#mission');
function filter(){let count=0;for(const a of articles){const ok=(!priority.value||a.dataset.priority===priority.value)&&(!mission.value||a.dataset.mission===mission.value);a.hidden=!ok;if(ok)count++;}document.querySelector('#count').textContent=count+' orientation'+(count>1?'s':'')+' affichée'+(count>1?'s':'')+' sur 9';document.querySelector('#empty').hidden=count!==0;}
priority.addEventListener('change',filter);mission.addEventListener('change',filter);
document.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',()=>{priority.value='';mission.value='';filter();}));
filter();
document.querySelectorAll('a.shot').forEach(a=>a.addEventListener('click',()=>{const img=a.querySelector('img');if(img?.currentSrc)a.href=img.currentSrc;}));
