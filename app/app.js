const form = document.querySelector('#birth-form');
const button = document.querySelector('#calculate');
const workspace = document.querySelector('#workspace');
const error = document.querySelector('#error');
const output = document.querySelector('#results');
const escape = value => String(value ?? 'Unavailable').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const source = s => s ? `${escape(s.slug)} · PDF page ${escape(s.pdf_page ?? (s.pdf_pages || []).join(', '))}` : 'Source unavailable';
function render(report, birth) {
  const chart = report.natal_chart;
  const star = chart.moon_nakshatra;
  const rows = Object.entries(chart.placements).map(([name, p]) => `<tr><td>${escape(name)}</td><td>${escape(p.sign)}<br><small>${(p.longitude % 30).toFixed(2)}° ${p.retrograde ? 'retrograde' : ''}</small></td><td>${escape(p.whole_sign_house_from_ascendant)}</td><td>${escape(p.sripati_degree_house?.house)}${p.sripati_degree_house?.at_sandhi ? ' (sandhi)' : ''}</td></tr>`).join('');
  const periods = chart.moon_periods;
  const periodRows = periods.periods.map(p => `<tr><td>${escape(p.lord)}</td><td>${Number(p.start_solar_years_after_birth).toFixed(3)}</td><td>${Number(p.end_solar_years_after_birth).toFixed(3)}</td></tr>`).join('');
  const sources = [star.source, periods.source, ...Object.values(chart.placements).map(p => p.sripati_degree_house?.source)].filter(Boolean);
  const unique = [...new Map(sources.map(s => [JSON.stringify(s), s])).values()];
  output.innerHTML = `<div class="result-head"><p class="eyebrow">Calculated chart · ${birth.place === 'Synthetic example' ? 'synthetic example' : 'explicit birth inputs'}</p><h2>${escape(birth.place)}</h2><p>${escape(birth.date)} · ${escape(birth.time)} · ${escape(birth.timezone)}</p><p>UTC ${escape(chart.birth_utc)} · ${escape(chart.latitude)}°, ${escape(chart.longitude)}°</p></div>
  <div class="summary-grid"><div><span>Ascendant</span><strong>${escape(chart.ascendant.sign)}</strong><small>${(chart.ascendant.longitude % 30).toFixed(2)}° within sign</small></div><div><span>Moon sign</span><strong>${escape(chart.placements.Moon.sign)}</strong><small>Lahiri sidereal</small></div><div><span>Nakshatra</span><strong>${escape(star.name)}</strong><small>Pada ${escape(star.pada)}</small></div></div>
  <div class="boundary"><h3>Research-gated, not zero</h3><p>Complete strength: not selected. Historical calendar: not selected. Personal forecast: unavailable. Predictive accuracy: unscored.</p><p>Chart mechanics do not establish a life outcome or reproduce a professional astrologer's judgement.</p></div>
  <details><summary>Planet placements</summary><p>Whole-sign and Sripati degree houses are separate models, not interchangeable. Rahu is the mean node. Ketu is not supplied in this engine report; no extra placement is invented.</p><div class="table-wrap"><table><thead><tr><th>Planet</th><th>Sign / degree</th><th>Whole-sign house</th><th>Sripati house</th></tr></thead><tbody>${rows}</tbody></table></div></details>
  <details><summary>Period arithmetic</summary><p>Initial lord: ${escape(periods.initial_lord)}. Remaining at birth: ${Number(periods.initial_remaining_solar_years).toFixed(3)} solar-year units.</p><p>${escape(periods.date_limit)} ${escape(periods.method_note)}</p><div class="table-wrap"><table><thead><tr><th>Lord</th><th>Start from birth<br>(solar-year units)</th><th>End from birth<br>(solar-year units)</th></tr></thead><tbody>${periodRows}</tbody></table></div><p>No current-period label or calendar date is inferred.</p></details>
  <details><summary>Source references & model</summary><p>${escape(chart.model)}</p>${unique.map(s => `<div class="source-row">${source(s)}<p>${s.verified_against_page_image ? 'Page image checked in the engine source audit.' : 'Page-image verification not recorded.'} This preview lists references only; it does not display scanned pages or authoritative interpretations.</p></div>`).join('')}<p>${escape(chart.notice)}</p></details>
  <details><summary>Inspect the engine report</summary><p>Raw evidence includes research candidates, not selected verdicts. Unknown values remain null.</p><pre>${escape(JSON.stringify(report, null, 2))}</pre></details>`;
  document.querySelector('#empty').hidden = true;
  output.hidden = false;
}
form.addEventListener('submit', async e => {
  e.preventDefault(); error.hidden = true; output.hidden = true;
  document.querySelector('#empty').hidden = false;
  button.disabled = true; button.textContent = 'Calculating…'; workspace.setAttribute('aria-busy', 'true');
  const values = Object.fromEntries(new FormData(form));
  const birth = {...values, latitude: Number(values.latitude), longitude: Number(values.longitude)};
  try {
    const response = await fetch('/api/calculate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({birth}), signal:AbortSignal.timeout(30000)});
    const report = await response.json();
    if (!response.ok) throw new Error(report.error || 'Calculation is unavailable.');
    render(report, birth);
    if (matchMedia('(max-width:700px)').matches) workspace.scrollIntoView({behavior:'smooth', block:'start'});
  } catch (e) { error.textContent = e.name === 'TimeoutError' ? 'The calculation timed out. Try again; no result has been generated.' : e.message; error.hidden = false; }
  finally { button.disabled = false; button.textContent = 'Calculate chart'; workspace.setAttribute('aria-busy', 'false'); }
});
document.querySelector('#example').addEventListener('click', () => {
  const example = {date:'2000-01-01',time:'14:30',place:'Synthetic example',timezone:'Asia/Kolkata',latitude:13,longitude:80};
  for (const [key, value] of Object.entries(example)) form.elements[key].value = value;
});
