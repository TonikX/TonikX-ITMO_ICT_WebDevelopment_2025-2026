(function(){
  const $ = (s, p=document)=>p.querySelector(s);
  const $$ = (s, p=document)=>Array.from(p.querySelectorAll(s));

  const searchInput = $('#searchInput');
  const clearBtn = $('#clearSearch');
  const typeFilter = $('#typeFilter');
  const airlineFilter = $('#airlineFilter');
  const originFilter = $('#originFilter');
  const tableView = $('#tableView');
  const cardsView = $('#cardsView');
  const toggleBtns = $$('.view-toggle button');
  const tbody = $('#flightsBody');

  // собрать все элементы (и строки, и карточки) для единого фильтра
  const rowEls = $$('#flightsBody .row');
  const cardEls = $$('#cardsView .card');

  function norm(s){ return (s||'').toString().toLowerCase(); }

  function passFilters(el){
    const q = norm(searchInput.value);
    const t = typeFilter.value;
    const a = airlineFilter.value;
    const o = originFilter.value;

    const hay = [
      el.dataset.number, el.dataset.airline,
      el.dataset.origin, el.dataset.destination,
      el.dataset.gate
    ].map(norm).join(' ');

    if(q && !hay.includes(q)) return false;
    if(t && el.dataset.type !== t) return false;
    if(a && el.dataset.airline !== a) return false;
    if(o && el.dataset.origin !== o) return false;
    return true;
  }

  function applyFilters(){
    rowEls.forEach(el => el.style.display = passFilters(el) ? '' : 'none');
    cardEls.forEach(el => el.style.display = passFilters(el) ? '' : 'none');
  }

  searchInput?.addEventListener('input', applyFilters);
  [typeFilter, airlineFilter, originFilter].forEach(x=>x?.addEventListener('change', applyFilters));
  clearBtn?.addEventListener('click', ()=>{ searchInput.value=''; applyFilters(); });

  // переключение вида
  toggleBtns.forEach(btn=>{
    btn.addEventListener('click',()=>{
      toggleBtns.forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      const v = btn.dataset.view;
      if(v==='cards'){ cardsView.hidden=false; tableView.hidden=true; }
      else { cardsView.hidden=true; tableView.hidden=false; }
    });
  });

  // сортировка по клику в thead
  let sortState = { key:null, dir:1 };
  const head = $('table.flights thead');
  head?.addEventListener('click', (e)=>{
    const th = e.target.closest('[data-sort]');
    if(!th) return;
    const key = th.dataset.sort;
    sortState.dir = (sortState.key===key) ? -sortState.dir : 1;
    sortState.key = key;

    const rows = Array.from(tbody.children);
    rows.sort((r1,r2)=>{
      const v1 = getCellValue(r1,key);
      const v2 = getCellValue(r2,key);
      if(!isNaN(Date.parse(v1)) && !isNaN(Date.parse(v2))){
        return (new Date(v1)-new Date(v2))*sortState.dir;
      }
      const n1 = parseFloat(v1), n2 = parseFloat(v2);
      if(!isNaN(n1) && !isNaN(n2)) return (n1-n2)*sortState.dir;
      return v1.localeCompare(v2,'ru')*sortState.dir;
    });
    rows.forEach(r=>tbody.appendChild(r));
  });

  function getCellValue(row, key){
    switch(key){
      case 'number': return row.dataset.number || '';
      case 'airline': return row.dataset.airline || '';
      case 'route': return (row.dataset.origin||'') + ' ' + (row.dataset.destination||'');
      case 'type': return row.dataset.type || '';
      case 'gate': return row.dataset.gate || '';
      case 'depart': return row.dataset.depart || '';
      case 'arrive': return row.dataset.arrive || '';
      case 'capacity': return row.querySelector('.cap-text')?.textContent || '';
      default: return '';
    }
  }

  // убрать дубли в селектах (если в пагинации повторяются)
  function deduplicateOptions(sel){
    const seen = new Set();
    $$( 'option', sel ).forEach(opt=>{
      if(!opt.value) return;
      const k = opt.value;
      if(seen.has(k)) opt.remove();
      else seen.add(k);
    });
  }
  [airlineFilter, originFilter].forEach(deduplicateOptions);

  applyFilters();
})();