async function loadPapers() {
  const res = await fetch('./data/papers.p1.json', { cache: 'no-store' });
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

function matches(p, q, subject, year, assessment) {
  if (subject && p.subject !== subject) return false;
  if (year && String(p.year) !== String(year)) return false;
  if (assessment && p.assessment !== assessment) return false;

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
  const papers = await loadPapers();

  const q = byId('q');
  const subject = byId('subject');
  const year = byId('year');
  const assessment = byId('assessment');
  const tbody = byId('tbody');
  const count = byId('count');

  renderOptions(subject, uniq(papers.map(p => p.subject)).sort(), 'All subjects');
  renderOptions(year, uniq(papers.map(p => String(p.year))).sort((a,b) => b-a), 'All years');
  renderOptions(assessment, uniq(papers.map(p => p.assessment)).sort(), 'All assessments');

  function draw() {
    const rows = papers.filter(p => matches(p, q.value, subject.value, year.value, assessment.value));
    count.textContent = `${rows.length} result${rows.length === 1 ? '' : 's'}`;
    tbody.innerHTML = '';

    rows.forEach(p => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><a class="a" href="paper.html?id=${encodeURIComponent(p.id)}">${p.subject}</a><div class="small">${p.school}</div></td>
        <td>${p.year}</td>
        <td>${p.assessment}</td>
        <td>${p.hasAnswers === true ? 'Yes' : (p.hasAnswers === false ? 'No' : '—')}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  [q, subject, year, assessment].forEach(el => el.addEventListener('input', draw));
  draw();
}

async function initPaper() {
  const params = new URLSearchParams(location.search);
  const id = params.get('id');
  const papers = await loadPapers();
  const p = papers.find(x => x.id === id);

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

  title.textContent = `${p.level} ${p.subject} (${p.year})`;
  const ans = (p.hasAnswers === true ? 'Yes' : (p.hasAnswers === false ? 'No' : 'Unknown'));
  meta.textContent = `${p.assessment} • ${p.school} • Answers: ${ans}`;
  link.href = p.sourceUrl;
  link.textContent = 'Go to source link';
  notes.textContent = p.notes || '';
}
