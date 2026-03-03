async function loadPapers(level) {
  const file = level === 'p2' ? './data/papers.p2.json' : './data/papers.p1.json';
  const res = await fetch(file, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load dataset');
  return res.json();
}

function uniq(arr) {
  return [...new Set(arr)].filter(Boolean);
}

function byId(id) {
  return document.getElementById(id);
}

function normalize(s) {
  return String(s ?? '').toLowerCase().trim();
}

function matches(p, q, subject, year, assessmentType) {
  if (subject && p.subject !== subject) return false;
  if (year && String(p.year) !== String(year)) return false;
  if (assessmentType && (p.assessmentType || '') !== assessmentType) return false;

  if (!q) return true;
  const hay = normalize([p.level, p.subject, p.year, p.assessment, p.school, p.id].join(' '));
  return hay.includes(normalize(q));
}

function renderOptions(select, items, placeholder) {
  select.innerHTML = '';
  const opt0 = document.createElement('option');
  opt0.value = '';
  opt0.textContent = placeholder;
  select.appendChild(opt0);

  items.forEach(v => {
    const o = document.createElement('option');
    o.value = v;
    o.textContent = v;
    select.appendChild(o);
  });
}

async function initBrowse() {
  const level = byId('level');
  const q = byId('q');
  const subject = byId('subject');
  const year = byId('year');
  const atype = byId('atype');
  const tbody = byId('tbody');
  const count = byId('count');

  let papers = [];

  // Allow shareable pre-filtered links: browse.html?level=p2&subject=Maths&year=latest&type=Quiz
  {
    const params = new URLSearchParams(location.search);
    const pLevel = params.get('level');
    if (pLevel === 'p1' || pLevel === 'p2') level.value = pLevel;
  }

  function applyParams() {
    const params = new URLSearchParams(location.search);
    const pSubject = params.get('subject') || '';
    const pYear = params.get('year') || '';
    const pType = params.get('type') || '';

    if (pSubject) subject.value = pSubject;

    if (pYear) {
      if (pYear === 'latest') {
        const ys = papers.map(p => Number(p.year)).filter(Boolean);
        const latest = ys.length ? String(Math.max(...ys)) : '';
        if (latest) year.value = latest;
      } else {
        year.value = pYear;
      }
    }

    if (pType) atype.value = pType;
  }

  async function reload({ resetFilters = true } = {}) {
    papers = await loadPapers(level.value);

    renderOptions(subject, uniq(papers.map(p => p.subject)).sort(), 'All subjects');
    renderOptions(year, uniq(papers.map(p => String(p.year))).sort((a,b) => b-a), 'All years');
    const order = ['SA','CA','WA','Test','Quiz','Review','Other'];
    const types = uniq(papers.map(p => p.assessmentType)).sort((a,b) => order.indexOf(a) - order.indexOf(b));
    renderOptions(atype, types, 'All types');

    if (resetFilters) {
      q.value = '';
      subject.value = '';
      year.value = '';
      atype.value = '';
    }

    applyParams();
    draw();
  }

  function draw() {
    const rows = papers.filter(p => matches(p, q.value, subject.value, year.value, atype.value));
    count.textContent = `${rows.length} result${rows.length === 1 ? '' : 's'}`;
    tbody.innerHTML = '';

    rows.forEach(p => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><a class="a" href="papers/${encodeURIComponent(p.id)}.html">${p.subject}</a><div class="small">${p.school}</div></td>
        <td>${p.year}</td>
        <td>${p.assessment}</td>
        <td>${p.hasAnswers === true ? 'Yes' : (p.hasAnswers === false ? 'No' : '—')}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  [q, subject, year, atype].forEach(el => el.addEventListener('input', draw));

  const chip = (id, value) => {
    const el = byId(id);
    if (!el) return;
    el.addEventListener('click', () => {
      subject.value = value;
      draw();
    });
  };
  chip('chip-all', '');
  chip('chip-english', 'English');
  chip('chip-maths', 'Maths');
  chip('chip-chinese', 'Chinese');

  level.addEventListener('change', () => reload({ resetFilters: true }));

  // Initial load: keep URL params if present.
  await reload({ resetFilters: false });
}

async function initPaper() {
  const params = new URLSearchParams(location.search);
  const id = params.get('id');

  const p1 = await loadPapers('p1');
  const p2 = await loadPapers('p2');
  const all = [...p1, ...p2];
  const p = all.find(x => x.id === id);

  const title = byId('title');
  const meta = byId('meta');
  const link = byId('link');
  const notes = byId('notes');

  if (!p) {
    title.textContent = 'Paper not found';
    meta.textContent = 'Try going back to Browse.';
    link.style.display = 'none';
    notes.textContent = '';
    return;
  }

  // Legacy support: redirect old query-param URLs to the shareable static page.
  location.replace(`papers/${encodeURIComponent(p.id)}.html`);
}
