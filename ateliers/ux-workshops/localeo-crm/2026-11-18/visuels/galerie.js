'use strict';
document.documentElement.classList.add('js');
document.querySelectorAll('[data-orientation]').forEach(section=>{
  section.querySelectorAll('[data-show]').forEach(button=>button.addEventListener('click',()=>{
    section.dataset.mode=button.dataset.show;
    section.querySelectorAll('[data-show]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  }));
  section.querySelector('[data-scene]').addEventListener('change',event=>{
    const name=event.target.value;
    const img=section.querySelector('[data-after]');
    img.src=`maquettes-apres/${name}-bureau.png`;
    img.alt=`Maquette ${section.dataset.orientation} : ${event.target.selectedOptions[0].textContent} ; données fictives`;
    section.querySelector('source').srcset=`maquettes-apres/${name}-mobile.png`;
    section.querySelector('[data-full]').href=`maquettes-apres/${name}-${matchMedia('(max-width:760px)').matches?'mobile':'bureau'}.png`;
    section.querySelector('[data-html]').href=`maquettes-apres/${name}.html`;
    section.querySelector('[data-png]').href=`maquettes-apres/${name}-bureau.png`;
  });
  const syncFull=()=>{const name=section.querySelector('[data-scene]').value;section.querySelector('[data-full]').href=`maquettes-apres/${name}-${matchMedia('(max-width:760px)').matches?'mobile':'bureau'}.png`;};
  syncFull();window.addEventListener('resize',syncFull);
});
