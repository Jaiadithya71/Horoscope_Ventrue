const form = document.querySelector('#birth-form');
const button = document.querySelector('#calculate');
const workspace = document.querySelector('#workspace');
const error = document.querySelector('#error');
const output = document.querySelector('#results');
const resolved = document.querySelector('#resolved');
const candidatesBox = document.querySelector('#candidates');
const findButton = document.querySelector('#find-place');
let resolvedFromLookup = false;
const escape = value => String(value ?? 'Unavailable').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const source = s => s ? `${escape(s.slug)} · PDF page ${escape(s.pdf_page ?? (s.pdf_pages || []).join(', '))}` : 'Source unavailable';
function fail(message) { error.textContent = message; error.hidden = false; }
function showResolved(candidate) {
  resolvedFromLookup = true;
  error.hidden = true;
  form.elements.latitude.value = candidate.latitude;
  form.elements.longitude.value = candidate.longitude;
  resolved.innerHTML = `Using ${candidate.latitude.toFixed(4)}, ${candidate.longitude.toFixed(4)} · ${escape(candidate.display_name)}<button type="button" id="change-place">change</button>`;
  resolved.hidden = false;
  candidatesBox.hidden = true;
  resolved.querySelector('#change-place').addEventListener('click', () => {
    form.elements.latitude.value = ''; form.elements.longitude.value = '';
    resolvedFromLookup = false; resolved.hidden = true; form.elements.place.focus();
  });
}
async function findCoordinates() {
  error.hidden = true;
  const place = form.elements.place.value.trim();
  if (!place) { fail('Enter a city, town or state first.'); return false; }
  findButton.disabled = true; findButton.textContent = 'Finding…';
  try {
    const response = await fetch(`/api/geocode?place=${encodeURIComponent(place)}`, {signal: AbortSignal.timeout(15000)});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Place lookup failed.');
    if (!data.candidates.length) {
      fail(`No match for "${place}". Add the state or country, or enter coordinates manually.`); return false;
    }
    if (data.candidates.length === 1) { showResolved(data.candidates[0]); return true; }
    candidatesBox.innerHTML = data.candidates.map((c, i) =>
      `<label><input type="radio" name="candidate" value="${i}">${escape(c.display_name)}</label>`).join('');
    candidatesBox.hidden = false; resolved.hidden = true;
    candidatesBox.querySelectorAll('input').forEach(input =>
      input.addEventListener('change', () => showResolved(data.candidates[Number(input.value)])));
    fail('More than one place matches. Pick the right one above.');
    return false;
  } catch (e) { fail(e.name === 'TimeoutError' ? 'Place lookup timed out. Try again or enter coordinates manually.' : e.message); return false; }
  finally { findButton.disabled = false; findButton.textContent = 'Find coordinates'; }
}
findButton.addEventListener('click', findCoordinates);
form.elements.place.addEventListener('input', () => { resolvedFromLookup = false; resolved.hidden = true; candidatesBox.hidden = true; });
form.elements.latitude.addEventListener('input', () => { resolvedFromLookup = false; });
form.elements.longitude.addEventListener('input', () => { resolvedFromLookup = false; });

const ORDINALS = ['','1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th'];
const ord = n => ORDINALS[n] || `${n}th`;
function readingParagraphs(chart) {
  const asc = chart.ascendant.sign;
  const star = chart.moon_nakshatra;
  const structure = chart.structural_factors_from_ascendant;
  const lordships = structure?.lordships?.houses || [];
  const factors = structure?.planet_factors || [];
  const lagnaLord = lordships.find(h => h.house === 1)?.lord;
  const paragraphs = [];
  paragraphs.push(`Born ${escape(chart.birth_utc.slice(0,10))}, ${escape(chart.birth_place)}. ` +
    `Your lagna is ${escape(asc)}. Your Moon is in ${escape(chart.placements.Moon.sign)}, in ${escape(star.name)}, pada ${escape(star.pada)}.`);
  if (lagnaLord) {
    const owned = lordships.filter(h => h.lord === lagnaLord).map(h => ord(h.house));
    const ownText = owned.length > 1 ? `It also rules your ${owned.slice(1).join(' and ')} house.` : '';
    paragraphs.push(`${escape(lagnaLord)} rules your ascendant${owned.length > 1 ? ' and your ' + owned.slice(1).join(' and ') + ' house' : ''} - your lagna lord. Watch where it sits: that is the anchor of this chart.`);
  }
  const order = [lagnaLord, 'Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu'].filter((v,i,a)=>v&&a.indexOf(v)===i);
  for (const planet of order) {
    const p = chart.placements[planet]; if (!p) continue;
    const f = factors.find(x => x.planet === planet);
    const house = f?.house_from_reference ?? p.whole_sign_house_from_ascendant;
    const ruled = (f?.rules_owned || []).map(h => ord(h));
    const ruledText = ruled.length ? ` It rules your ${ruled.join(' and ')} house.` : '';
    const aspects = (f?.aspects || []).map(a => `your ${ord(a.target_house_from_reference)} house (${escape(a.target_sign)})`);
    const aspectText = aspects.length ? ` From there it aspects ${aspects.join(' and ')}.` : '';
    const retro = p.retrograde ? ', retrograde' : '';
    const nodeNote = planet === 'Rahu' ? ' (the mean node)' : '';
    paragraphs.push(`${escape(planet)}${nodeNote} sits in ${escape(p.sign)}${retro} - your ${ord(house)} house from the ascendant.${ruledText}${aspectText}`);
  }
  const periods = chart.moon_periods;
  paragraphs.push(`Your period sequence opens with ${escape(periods.initial_lord)}, with ${Number(periods.initial_remaining_solar_years).toFixed(2)} solar-year units of it remaining at birth. The full order is listed below. The engine gives no calendar dates for these boundaries yet - that conversion is still research-gated.`);
  return paragraphs;
}

function render(report, birth, coordsWereResolved) {
  const chart = report.natal_chart;
  const star = chart.moon_nakshatra;
  const rows = Object.entries(chart.placements).map(([name, p]) => `<tr><td>${escape(name)}</td><td>${escape(p.sign)}<br><small>${(p.longitude % 30).toFixed(2)}° ${p.retrograde ? 'retrograde' : ''}</small></td><td>${escape(p.whole_sign_house_from_ascendant)}</td><td>${escape(p.sripati_degree_house?.house)}${p.sripati_degree_house?.at_sandhi ? ' (sandhi)' : ''}</td></tr>`).join('');
  const periods = chart.moon_periods;
  const periodRows = periods.periods.map(p => `<tr><td>${escape(p.lord)}</td><td>${Number(p.start_solar_years_after_birth).toFixed(3)}</td><td>${Number(p.end_solar_years_after_birth).toFixed(3)}</td></tr>`).join('');
  const sources = [star.source, periods.source, ...Object.values(chart.placements).map(p => p.sripati_degree_house?.source)].filter(Boolean);
  const unique = [...new Map(sources.map(s => [JSON.stringify(s), s])).values()];
  const coordsNote = coordsWereResolved ? ' · coordinates from place lookup' : '';
  const reading = readingParagraphs(chart);
  output.innerHTML = `<div class="result-head"><p class="eyebrow">Your reading · ${birth.place === 'Synthetic example' ? 'synthetic example' : 'explicit birth inputs'}</p><h2>${escape(chart.ascendant.sign)} lagna · ${escape(star.name)}</h2><p>${escape(birth.place)} · ${escape(birth.date)} · ${escape(birth.time)} · ${escape(chart.latitude)}°, ${escape(chart.longitude)}°${coordsNote}</p></div>
  <section class="reading">${reading.map(t => `<p>${t}</p>`).join('')}</section>
  <div class="boundary"><h3>Where this reading stops</h3><p>This is the structure of your chart, read the way a reader would lay it out - placements, lordships, aspects, periods. What comes next in a real consultation is judgement: strength, timing, outcomes. That layer is still research-gated, so it is not here. No strength totals, no calendar dates, no predictions.</p><p>Chart mechanics do not establish a life outcome or reproduce a professional astrologer's judgement.</p></div>
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
  if (form.elements.latitude.value === '' || form.elements.longitude.value === '') {
    const ok = await findCoordinates();
    if (!ok || form.elements.latitude.value === '') return;
  }
  button.disabled = true; button.textContent = 'Calculating…'; workspace.setAttribute('aria-busy', 'true');
  const values = Object.fromEntries(new FormData(form));
  const birth = {date: values.date, time: values.time, timezone: values.timezone, place: values.place,
    latitude: Number(values.latitude), longitude: Number(values.longitude)};
  try {
    const response = await fetch('/api/calculate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({birth}), signal:AbortSignal.timeout(30000)});
    const report = await response.json();
    if (!response.ok) throw new Error(report.error || 'Calculation is unavailable.');
    render(report, birth, resolvedFromLookup);
    if (matchMedia('(max-width:700px)').matches) workspace.scrollIntoView({behavior:'smooth', block:'start'});
  } catch (e) { fail(e.name === 'TimeoutError' ? 'The calculation timed out. Try again; no result has been generated.' : e.message); }
  finally { button.disabled = false; button.textContent = 'Calculate chart'; workspace.setAttribute('aria-busy', 'false'); }
});
document.querySelector('#example').addEventListener('click', () => {
  const example = {date:'2000-01-01',time:'14:30',place:'Synthetic example',timezone:'Asia/Kolkata',latitude:13,longitude:80};
  for (const [key, value] of Object.entries(example)) form.elements[key].value = value;
  resolvedFromLookup = false; resolved.hidden = true; candidatesBox.hidden = true; error.hidden = true;
});
