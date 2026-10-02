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
const source = s => s ? `${escape(s.slug ?? s.book ?? s.title)} · PDF page ${escape(s.pdf_page ?? (s.pdf_pages || []).join(', '))}` : 'Source unavailable';
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

function sourceLink(s) {
  if (!s) return 'Source unavailable';
  let url;
  try { url = new URL(s.url); } catch { return source(s); }
  if (url.protocol !== 'https:') return source(s);
  return `<a href="${escape(url.href)}" target="_blank" rel="noopener noreferrer">${source(s)}${s.chapter ? ` · chapter ${escape(s.chapter)}${s.sloka ? `, verse ${escape(s.sloka)}` : ''}` : ''}</a>`;
}
function lifeAspectReading(aspects) {
  if (!aspects?.career?.candidates?.length) return '';
  const cards = aspects.career.candidates.map(c => `<article class="route-card">
    <h3>${escape(c.reference)} route · not selected</h3>
    <p class="route-reading">${escape(c.conditional_reading)}</p>
    <p class="route-geometry">The tenth sign from ${escape(c.reference)} is ${escape(c.tenth_sign)}, ruled by ${escape(c.tenth_lord)}. That lord is in ${escape(c.navamsa_sign)} Navamsa, owned by ${escape(c.navamsa_owner)}.</p>
    <p class="route-caveat">${escape(c.navamsa_owner)}'s strength has not been established. This route has not been ranked or selected.</p>
    <p class="route-source">${sourceLink(c.occupation_source)}</p>
    <details><summary>Wealth condition for this route</summary><p>${escape(c.wealth_conditional_reading)}</p><p>${sourceLink(c.wealth_source)}</p></details>
  </article>`).join('');
  return `<section class="life-aspects" aria-labelledby="career-title"><p class="eyebrow">Source-based alternatives</p><h2 id="career-title">Career · three possible routes</h2>
    <p>These are conditional historical readings, not a chosen profession. The source asks for the strongest Lagna, Moon or Sun route. The engine has not made that comparison or completed the required strength examination, and the whole-sign versus degree-bhava application is unresolved.</p>
    <div class="route-list">${cards}</div>
    <p class="aspect-limit">${escape(aspects.career.notice)} Repeated Navamsa owners do not select a route or independently confirm a prediction. These examples are disclosed, non-stigmatizing subsets of the historical verses, not complete translations or assumptions about your gender.</p>
    <p class="route-source">Route selection: ${sourceLink(aspects.career.selection_source)}<br>Strength requirement: ${sourceLink(aspects.strength_gate_source)}</p>
    <div class="aspect-stop"><h3>Wealth, marriage, health and timing</h3><p>No wealth outcome is selected. Each route's wealth condition is available above, but its owner's strength is unknown. No income amount, financial advice or foreign move is predicted. Marriage has no selected reading; no medical prediction is supplied; calendar timing and outcome selection remain unresolved.</p></div>
  </section>`;
}

const STATUS_LABEL = {met:'Condition met', possibly_met:'Possibly met', unresolved:'Unresolved', not_met:'Not met', house_model_dependent:'Depends on house system'};
const MODEL_LABEL = {whole_sign:'Whole-sign houses', sripati_degree_bhava:'Sripati degree houses'};
const day = v => escape(String(v ?? '').slice(0, 10));
const visibleRows = rows => (rows || []).filter(r => r.ship_default !== false);
function conditionRow(r) {
  const dep = r.status === 'house_model_dependent';
  const models = dep && r.status_by_house_model ? `<p class="cond-models">${Object.entries(r.status_by_house_model).map(([k, v]) => `${escape(MODEL_LABEL[k] || k)}: ${escape(STATUS_LABEL[v] || v)}`).join(' · ')}</p>` : '';
  return `<li class="cond-row cond-${escape(r.status)}"><p class="cond-status">${escape(STATUS_LABEL[r.status] || r.status)}</p>
    <p class="cond-condition">${escape(r.condition)}</p>
    <p class="cond-effect">${escape(r.effect_paraphrase)}</p>${models}
    <p class="route-source">${/^[\[{]/.test(String(r.detail ?? '')) ? '' : escape(r.detail) + ' · '}${sourceLink(r.source)}</p></li>`;
}
function conditionSection(title, id, data, intro) {
  if (!data?.rows) return '';
  const rows = visibleRows(data.rows);
  const active = rows.filter(r => r.status !== 'not_met');
  const notMet = rows.filter(r => r.status === 'not_met');
  const dep = active.some(r => r.status === 'house_model_dependent');
  return `<section class="life-aspects life-extra" aria-labelledby="${id}"><p class="eyebrow">Source-based conditions</p><h2 id="${id}">${escape(title)}</h2>
    <p>${escape(intro)}${dep ? ' Some rows depend on the house system: the two models give different answers and neither is chosen.' : ''}</p>
    ${active.length ? `<ul class="cond-list">${active.map(conditionRow).join('')}</ul>` : '<p class="route-caveat">No condition in this set is met or open for this chart.</p>'}
    ${notMet.length ? `<details><summary>${notMet.length} conditions checked and not met</summary><ul class="cond-list">${notMet.map(conditionRow).join('')}</ul></details>` : ''}
    <p class="aspect-limit">${escape(data.notice)}</p></section>`;
}
const RUPA = v => Array.isArray(v) ? (v[0] === v[1] ? v[0].toFixed(2) : `${v[0].toFixed(2)} to ${v[1].toFixed(2)}`) : 'Unavailable';
const VERDICT = {meets_sripati_minimum_in_all_variants:'Meets the minimum in every variant', unresolved_across_variants:'Unresolved: variants disagree'};
function strengthSection(profile) {
  if (!profile?.planets) return '';
  const entries = Object.entries(profile.planets);
  const body = entries.map(([name, p]) => `<tr><td>${escape(name)}</td><td>${RUPA(p.total_rupa_interval)}</td><td>${escape(p.minimum_rupa)}</td><td>${escape(VERDICT[p.verdict] || p.verdict)}</td></tr>`).join('');
  const clear = entries.filter(([, p]) => p.verdict === 'meets_sripati_minimum_in_all_variants').map(([n]) => n);
  const open = entries.filter(([, p]) => p.verdict !== 'meets_sripati_minimum_in_all_variants').map(([n]) => n);
  return `<section class="life-aspects life-extra" aria-labelledby="strength-title"><p class="eyebrow">Planet strength</p><h2 id="strength-title">Strength, as a range</h2>
    <p>${clear.length ? `${escape(clear.join(', '))} clear the traditional minimum however the inputs are read.` : 'No planet clears the minimum under every reading.'} ${open.length ? `For ${escape(open.join(', '))} the answer changes with the inputs, so no verdict is given.` : ''}</p>
    <details><summary>Strength table (rupas)</summary><div class="table-wrap"><table><thead><tr><th>Planet</th><th>Total range</th><th>Minimum</th><th>Verdict</th></tr></thead><tbody>${body}</tbody></table></div><p>${escape(profile.notice)}</p><p>${sourceLink(profile.source)}</p></details></section>`;
}
function timingSection(t) {
  if (!t?.timelines) return '';
  const lords = (t.marriage_candidate_lords || []).join(', ');
  const blocks = Object.values(t.timelines).map(tl => {
    const label = `${tl.balance_reading === 'moon_time_in_nakshatra_bj' ? 'Moon time in nakshatra' : 'Uniform longitude'} · ${Number(tl.year_length_days).toFixed(tl.year_length_days === 360 ? 0 : 3)}-day year`;
    const maha = tl.mahadasas.map(m => `<tr><td>${escape(m.lord)}</td><td>${day(m.start)}</td><td>${day(m.end)}</td></tr>`).join('');
    const win = (tl.marriage_candidate_antardasa_windows || []).map(w => `<tr><td>${escape(w.maha_lord)} / ${escape(w.antar_lord)}</td><td>${day(w.start)}</td><td>${day(w.end)}</td></tr>`).join('');
    return `<details><summary>${escape(label)}</summary><div class="table-wrap"><table><thead><tr><th>Main period</th><th>From</th><th>To</th></tr></thead><tbody>${maha}</tbody></table></div>
      ${win ? `<h3 class="sub">Windows where both lords are marriage candidates</h3><div class="table-wrap"><table><thead><tr><th>Period</th><th>From</th><th>To</th></tr></thead><tbody>${win}</tbody></table></div>` : ''}</details>`;
  }).join('');
  return `<section class="life-aspects life-extra" aria-labelledby="timing-title"><p class="eyebrow">Dated periods</p><h2 id="timing-title">Timing, four ways</h2>
    <p>The dates depend on two conventions the books leave open: how the opening balance is read and how long a year is. Four timelines are shown side by side and none is chosen. Marriage windows are where both period lords are among ${escape(lords)}; that is a source condition, not a prediction.</p>
    ${blocks}<p class="route-source">${sourceLink(t.source)}</p><p class="aspect-limit">${escape(t.notice)}</p></section>`;
}
function lifeSections(report) {
  return conditionSection('Marriage · what the sources condition', 'marriage-title', report.marriage_conditional, 'Each row is a rule from the sources, checked against this chart. Marriage timing is not selected and the spouse\'s sex is not an input.') +
    conditionSection('Wealth · what the sources condition', 'wealth-title', report.wealth_conditional, 'Each row is a rule from the sources, checked against this chart. No income level is produced.') +
    strengthSection(report.shadbala_working_profile) + timingSection(report.timing_conditional);
}
function publicReport(report) {
  const copy = JSON.parse(JSON.stringify(report));
  for (const k of ['marriage_conditional', 'wealth_conditional']) if (copy[k]?.rows) copy[k].rows = visibleRows(copy[k].rows);
  return copy;
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
  ${lifeAspectReading(report.life_aspect_candidates)}
  ${lifeSections(report)}
  <h2 class="chart-structure-title">The structure of your chart</h2>
  <section class="reading">${reading.map(t => `<p>${t}</p>`).join('')}</section>
  <div class="boundary"><h3>Where this reading stops</h3><p>The career alternatives above add source-based conditional interpretation to the chart structure. They do not choose the strongest route or a profession. Selected strength, calendar timing and life outcomes remain research-gated. No complete personal forecast or predictive accuracy is established.</p><p>Chart mechanics do not establish a life outcome or reproduce a professional astrologer's judgement.</p></div>
  <details><summary>Planet placements</summary><p>Whole-sign and Sripati degree houses are separate models, not interchangeable. Rahu is the mean node. Ketu is not supplied in this engine report; no extra placement is invented.</p><div class="table-wrap"><table><thead><tr><th>Planet</th><th>Sign / degree</th><th>Whole-sign house</th><th>Sripati house</th></tr></thead><tbody>${rows}</tbody></table></div></details>
  <details><summary>Period arithmetic</summary><p>Initial lord: ${escape(periods.initial_lord)}. Remaining at birth: ${Number(periods.initial_remaining_solar_years).toFixed(3)} solar-year units.</p><p>${escape(periods.date_limit)} ${escape(periods.method_note)}</p><div class="table-wrap"><table><thead><tr><th>Lord</th><th>Start from birth<br>(solar-year units)</th><th>End from birth<br>(solar-year units)</th></tr></thead><tbody>${periodRows}</tbody></table></div><p>No current-period label or calendar date is inferred.</p></details>
  <details><summary>Source references & model</summary><p>${escape(chart.model)}</p>${unique.map(s => `<div class="source-row">${source(s)}<p>${s.verified_against_page_image ? 'Page image checked in the engine source audit.' : 'Page-image verification not recorded.'} This preview lists references only; it does not display scanned pages or authoritative interpretations.</p></div>`).join('')}<p>${escape(chart.notice)}</p></details>
  <details><summary>Inspect the engine report</summary><p>Raw evidence includes research candidates, not selected verdicts. Unknown values remain null.</p><pre>${escape(JSON.stringify(publicReport(report), null, 2))}</pre></details>`;
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
