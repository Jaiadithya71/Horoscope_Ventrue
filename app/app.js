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
  if (candidate.timezone) {
    const listed=[...form.elements.timezone.options].some(o=>o.value===candidate.timezone);
    form.elements.timezone.value=listed?candidate.timezone:'__other';
    form.elements.timezone_other.value=listed?'':candidate.timezone;
    form.elements.timezone.dispatchEvent(new Event('change'));
  }
  error.hidden = true;
  form.elements.latitude.value = candidate.latitude;
  form.elements.longitude.value = candidate.longitude;
  resolved.innerHTML = `Using ${candidate.latitude.toFixed(4)}, ${candidate.longitude.toFixed(4)} · <span data-private>${escape(candidate.display_name)}</span>${candidate.timezone ? ` · ${escape(candidate.timezone)} (check birth-date zone)` : " · choose time zone manually"}<button type="button" id="change-place">change</button>`;
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
      `<label><input type="radio" name="candidate" value="${i}"><span data-private>${escape(c.display_name)}</span></label>`).join('');
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
  paragraphs.push(`Born ${escape(chart.birth_utc.slice(0,10))}, <span data-private>${escape(chart.birth_place)}</span>. ` +
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
    const nodeNote = planet === 'Rahu' ? ` (${chart.node_mode||'mean'} node)` : '';
    paragraphs.push(`${escape(planet)}${nodeNote} sits in ${escape(p.sign)}${retro} - your ${ord(house)} house from the ascendant.${ruledText}${aspectText}`);
  }
  const periods = chart.moon_periods;
  paragraphs.push(`Your period sequence opens with ${escape(periods.initial_lord)}, with ${Number(periods.initial_remaining_solar_years).toFixed(2)} solar-year units of it remaining at birth. The full order is listed below. These offsets are not calendar dates. The four dated alternatives are shown separately above; no one convention is selected.`);
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


const CHIP = t => t.level === 'mixed' ? ['mixed', 'Mixed signals'] : (t.level === 'strong' || t.level === 'good') ? (t.confidence === 'tentative' ? ['moderate', 'Moderate indication'] : ['strong', 'Strong indication']) : ['light', 'Light indication'];
function outcomeSection(summary) {
  if (!summary?.topics?.length) return '';
  const cards = summary.topics.map(t => { const [cls, label] = CHIP(t); return `<article class="outcome-card chip-${cls}"><div class="outcome-top"><h3>${escape(t.title)}</h3><span class="chip">${label}</span></div>
    <p class="outcome-head">${escape(t.headline)}</p><p class="outcome-text">${escape(t.text)}</p>
    ${t.points?.length ? `<ul class="outcome-points">${t.points.map(p => `<li>${escape(p)}</li>`).join('')}</ul>` : ''}${t.evidence?.length ? `<details class="why"><summary>Why the chart says this</summary><ul class="outcome-points">${t.evidence.map(p => `<li>${escape(p)}</li>`).join('')}</ul></details>` : ''}</article>`; }).join('');
  return `<section class="outcomes" aria-labelledby="outcomes-title"><p class="eyebrow">What your chart says</p><h2 id="outcomes-title">Your reading in plain words</h2><div class="outcome-list">${cards}</div>
    <p class="aspect-limit">${escape(summary.basis)}</p></section>`;
}

const TONE = {strong:['strong','Supportive'], weak:['weak','Testing'], mixed:['mixed','Mixed']};
const KIND = {money:'money', career:'career', partnership:'partnership', children:'children'};
function whoSection(w) {
  if (!w) return '';
  const card = (title, o) => `<div class="who-card"><h3>${escape(title)}</h3><p class="outcome-text">${escape(o.text)}</p><p class="p-hl">${o.pointers.map(k => `<span class="hl">${escape(k)}</span>`).join('')}</p>
    <details class="why"><summary>Why the chart says this</summary><ul class="cond-list">${o.rules.map(r => `<li>${escape(r.sign)}: ${escape(r.effect)} <span class="route-source">${sourceLink(r.source)}</span></li>`).join('')}</ul></details></div>`;
  return `<section class="who" aria-labelledby="who-title"><p class="eyebrow">Who you are</p><h2 id="who-title">The person behind the chart</h2>
    ${card('How you come across', w.outer_you)}${w.same_sign ? '<p class="muted">Your outer and inner nature point the same way, so the same sketch applies to both.</p>' : card('Your inner nature', w.inner_you)}
    <p class="aspect-limit">${escape(w.notice)}</p></section>`;
}

function periodsSection(lp) {
  if (!lp?.periods?.length) return '';
  const now = new Date().getFullYear();
  const items = lp.periods.map(p => {
    const [cls, label] = TONE[p.tone] || TONE.mixed;
    const current = p.when === 'now' || (!p.when && p.years_about[0] <= now && now <= p.years_about[1]);
    const hl = (p.highlight_words || []).map(k => `<span class="hl">${escape(k)}</span>`).join('');
    const phaseHead = b => `<span class="ph-years">${escape(b.years_about[0])} to ${escape(b.years_about[1])}</span> <span class="chip">${escape(b.label)}</span>`;
    const phaseAreas = b => (b.phase_areas || []).length ? (b.phase_areas).map(x => `<div class="ph-area"><strong>${escape(x.label)}.</strong> ${escape(x.text)} <span class="guide-inline">${escape(x.guidance)}</span></div>`).join('') + '<p class="route-caveat">Areas for a smaller phase are our reading, not stated by the book.</p>' : '<p class="route-caveat">No area stands out for this phase, so the overall feel of the stretch applies.</p>';
    const subs = p.bhuktis.map(b => { const chips = (b.phase_areas || []).map(x => `<span class="hl">${escape(x.label)}</span>`).join('');
      return p.depth === 'full'
        ? `<section class="phase-open sub-${escape(b.tone)}"><h4>${phaseHead(b)}</h4><p class="p-hl">${chips}</p>${phaseAreas(b)}</section>`
        : `<details class="phase sub-${escape(b.tone)}"><summary>${phaseHead(b)} ${chips}</summary>${phaseAreas(b)}</details>`; }).join('');
    const asp = Object.values(p.aspects || {});
    const aspChips = asp.filter(x => x.status !== 'quiet').map(x => `<span class="hl asp-${escape(x.status)}">${escape(x.label)}: ${escape(x.status)}</span>`).join('');
    const full = p.depth === 'full';
    const aspects = full ? `<div class="aspects">${asp.map(x => `<details class="aspect asp-${escape(x.status)}"><summary><span class="a-name">${escape(x.label)}</span><span class="chip">${escape(x.status === 'quiet' ? 'nothing specific' : x.status)}</span></summary><p>${escape(x.text)}</p>${x.guidance ? `<p class="guide">${escape(x.guidance)}</p>` : ''}</details>`).join('')}</div>` : (aspChips ? `<p class="p-hl">${aspChips}</p>` : '');
    const reasons = p.bhuktis.map(b => `<li>${escape(b.years_about[0])} to ${escape(b.years_about[1])}: ${escape(b.lord)}. ${escape(b.basis)}</li>`).join('');
    const rules = p.rules.map(r => `<li>${escape(r.effect)} <span class="route-source">${sourceLink(r.source)}</span></li>`).join('');
    return `<details class="period period-${cls} depth-${escape(p.depth || "short")}"${current ? ' open' : ''}><summary><span class="p-lord">${escape(p.years_about[0])} to ${escape(p.years_about[1])}</span>${current ? '<span class="chip chip-now">Now</span>' : p.when === 'next' ? '<span class="chip">Next</span>' : ''}<span class="chip tone-${cls}">${escape(p.label || label)}</span></summary>
      <p class="outcome-text">${escape(p.you_text || p.summary)}</p>${hl ? `<p class="p-hl">Stands out for: ${hl}</p>` : ''}
      ${p.confidence === 'tentative' ? '<p class="route-caveat">The chart is less clear-cut for this stretch, so read it as a softer signal.</p>' : ''}
      ${aspects}${full ? `<h3 class="phases-title">Phase by phase</h3><div class="phase-list open">${subs}</div>` : `<details class="phases"><summary>Smaller phases inside it</summary><div class="phase-list">${subs}</div></details>`}
      <details class="why"><summary>Why the chart says this</summary><p class="route-caveat">Ruling planet for this stretch: ${escape(p.lord)}. ${escape(p.basis.join('; '))}.</p><ul class="cond-list">${rules}</ul><p class="route-caveat">Smaller phases:</p><ul class="cond-list">${reasons}</ul></details></details>`;
  }).join('');
  return `<section class="periods" aria-labelledby="periods-title"><p class="eyebrow">What happens when</p><h2 id="periods-title">Your life, period by period</h2>
    <p class="muted">Your life moves through long stretches, each with its own flavour. These are themes, not dated events. Years are rounded, because the traditional sources count them in more than one way.</p>
    <div class="period-list">${items}</div><p class="aspect-limit">${escape(lp.notice)}</p></section>`;
}

function render(report, birth, coordsWereResolved) {
  window.__lastReport = report; window.__lastBirth = birth; window.__lastCoords = coordsWereResolved;
  const chart = report.natal_chart;
  const star = chart.moon_nakshatra;
  const rows = Object.entries(chart.placements).map(([name, p]) => `<tr><td>${escape(name)}</td><td>${escape(p.sign)}<br><small>${(p.longitude % 30).toFixed(5)}° ${p.retrograde ? 'retrograde' : ''}</small></td><td>${escape(p.whole_sign_house_from_ascendant)}</td><td>${escape(p.sripati_degree_house?.house)}${p.sripati_degree_house?.at_sandhi ? ' (sandhi)' : ''}</td></tr>`).join('');
  const periods = chart.moon_periods;
  const periodRows = periods.periods.map(p => `<tr><td>${escape(p.lord)}</td><td>${Number(p.start_solar_years_after_birth).toFixed(3)}</td><td>${Number(p.end_solar_years_after_birth).toFixed(3)}</td></tr>`).join('');
  const sources = [star.source, periods.source, ...Object.values(chart.placements).map(p => p.sripati_degree_house?.source)].filter(Boolean);
  const unique = [...new Map(sources.map(s => [JSON.stringify(s), s])).values()];
  const coordsNote = coordsWereResolved ? ' · coordinates from place lookup' : '';
  const reading = readingParagraphs(chart);
  output.innerHTML = `<div class="result-head"><p class="eyebrow">Your reading · ${birth.place === 'Synthetic example' ? 'synthetic example' : 'explicit birth inputs'}</p><h2>${escape(lagnaName(chart.ascendant.sign))} lagna · ${escape(star.name)}</h2><p><span data-private>${escape(birth.place)}</span> · ${escape(birth.date)} · ${escape(birth.time)} · ${escape(chart.latitude)}°, ${escape(chart.longitude)}°${coordsNote}</p></div>
  ${inspectionSwitch()}${astrologerPanel(report,birth)}<div id="plain-reading" ${inspectionState.view!=='plain'?'hidden':''}>
  <button type="button" id="story-open" class="story-open">Read your life as a story</button>
  <nav class="secnav" aria-label="Sections"><a href="#who-title">Who you are</a><a href="#periods-title">Life by period</a><a href="#evidence">Evidence</a></nav>
  ${tamilSheet(report, birth)}
  ${whoSection(report.who_you_are)}
  ${outcomeSection(report.outcome_summary)}
  ${periodsSection(report.life_periods)}
  <details class="evidence-all" id="evidence"><summary>See the evidence and calculations behind this</summary>
  ${lifeAspectReading(report.life_aspect_candidates)}
  ${lifeSections(report)}
  <h2 class="chart-structure-title">The structure of your chart</h2>
  <section class="reading">${reading.map(t => `<p>${t}</p>`).join('')}</section>
  <div class="boundary"><h3>Where this reading stops</h3><p>The career alternatives above add source-based conditional interpretation to the chart structure. They do not choose the strongest route or a profession. Selected strength, calendar timing and life outcomes remain research-gated. No complete personal forecast or predictive accuracy is established.</p><p>Chart mechanics do not establish a life outcome or reproduce a professional astrologer's judgement.</p></div>
  <details><summary>Planet placements</summary><p>Whole-sign and Sripati degree houses are separate models, not interchangeable. Rahu uses the ${escape(chart.node_mode || "mean")} node. Ketu in the Tamil sheet is its opposite point, not an independently computed planet.</p><div class="table-wrap"><table><thead><tr><th>Planet</th><th>Sign / degree</th><th>Whole-sign house</th><th>Sripati house</th></tr></thead><tbody>${rows}</tbody></table></div></details>
  <details><summary>Period arithmetic</summary><p>Initial lord: ${escape(periods.initial_lord)}. Remaining at birth: ${Number(periods.initial_remaining_solar_years).toFixed(3)} solar-year units.</p><p>${escape(periods.date_limit)} ${escape(periods.method_note)}</p><div class="table-wrap"><table><thead><tr><th>Lord</th><th>Start from birth<br>(solar-year units)</th><th>End from birth<br>(solar-year units)</th></tr></thead><tbody>${periodRows}</tbody></table></div><p>No current-period label or calendar date is inferred.</p></details>
  <details><summary>Source references & model</summary><p>${escape(chart.model)}</p>${unique.map(s => `<div class="source-row">${source(s)}<p>${s.verified_against_page_image ? 'Page image checked in the engine source audit.' : 'Page-image verification not recorded.'} This preview lists references only; it does not display scanned pages or authoritative interpretations.</p></div>`).join('')}<p>${escape(chart.notice)}</p></details>
  <details><summary>Inspect the engine report</summary><p>Raw evidence includes research candidates, not selected verdicts. Unknown values remain null.</p><pre>${escape(JSON.stringify(publicReport(report), null, 2))}</pre></details></details></div>`;
  if(window.__lastNote)output.querySelector('.result-head').insertAdjacentHTML('beforeend', `<p class="lagna-note">${escape(window.__lastNote)}</p>`);document.querySelector('#empty').hidden = true;
  output.hidden = false;
}
const LAGNA_TA = {"Aries": "மேஷம்", "Taurus": "ரிஷபம்", "Gemini": "மிதுனம்", "Cancer": "கடகம்", "Leo": "சிம்மம்", "Virgo": "கன்னி", "Libra": "துலாம்", "Scorpio": "விருச்சிகம்", "Sagittarius": "தனுசு", "Capricorn": "மகரம்", "Aquarius": "கும்பம்", "Pisces": "மீனம்"};
const lagnaName = s => LAGNA_TA[s] ? `${s} (${LAGNA_TA[s]})` : s;
const timeMode = () => form.elements.timemode.value;
const choicesBox = document.querySelector('#lagna-choices');
function applyMode() {
  const m = timeMode();
  document.querySelector('#time-pick').hidden = m !== 'sure';
  document.querySelector('#window-pick').hidden = m !== 'window';
  document.querySelector('#known-pick').hidden = m !== 'known';
  choicesBox.hidden = true;
}
for (const r of form.elements.timemode) r.addEventListener('change', applyMode);
const clock = t => { const [h, m] = t.split(':').map(Number); return `${h % 12 || 12}:${pad(m)} ${h >= 12 ? 'PM' : 'AM'}`; };
async function runCalc(birth, note) {
  inspectionState={view:'plain',profile:'',at:new Date().toISOString().slice(0,19),house:1,planet:'Jupiter'};
  button.disabled = true; button.textContent = 'Calculating…'; workspace.setAttribute('aria-busy', 'true');
  try {
    const response = await fetch('/api/calculate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({birth,tamil_view:document.querySelector("#tamil-view").checked,node_mode:form.elements.node_mode.value}), signal:AbortSignal.timeout(30000)});
    const report = await response.json();
    if (!response.ok) throw new Error(report.error || 'Calculation is unavailable.');
    window.__lastNote=note||'';render(report, birth, resolvedFromLookup);

    if (matchMedia('(max-width:700px)').matches) workspace.scrollIntoView({behavior:'smooth', block:'start'});
  } catch (e) { fail(e.name === 'TimeoutError' ? 'The calculation timed out. Try again; no result has been generated.' : e.message); }
  finally { button.disabled = false; button.textContent = 'Calculate chart'; workspace.setAttribute('aria-busy', 'false'); }
}
function spanText(s) {
  const f = s.from.slice(11), t = s.to.slice(11), next = s.to.slice(0, 10) !== s.from.slice(0, 10) ? ' (next day)' : '';
  return `${clock(f)} to ${clock(t)}${next}`;
}
function chooseSpan(base, span, how) {
  choicesBox.hidden = true;
  const birth = {...base, date: span.stand_in_date, time: span.stand_in_time};
  const steady = span.moon_sign_steady && span.moon_star_steady ? 'Your Moon sign and star stay the same across this stretch.' : 'Your Moon moves to another sign or star during this stretch, so the Moon-based parts are less certain.';
  runCalc(birth, `${lagnaName(span.lagna)} lagna, ${how}. The chart is read from ${clock(span.stand_in_time)}, the middle of the stretch ${spanText(span)}. That is a stand-in, not your birth time. ${steady}`);
}
async function lagnaOptions(base) {
  const m = timeMode(), body = {date: base.date, timezone: base.timezone, latitude: base.latitude, longitude: base.longitude};
  if (m === 'window') {
    if (!form.elements.win_start.value || !form.elements.win_end.value) return fail('Choose the earliest and latest time it could have been.');
    Object.assign(body, {mode:'window', start: form.elements.win_start.value, end: form.elements.win_end.value});
  } else {
    if (!form.elements.known_lagna.value) return fail('Choose your lagna.');
    Object.assign(body, {mode:'known', lagna: form.elements.known_lagna.value, around: form.elements.known_around.value || ''});
  }
  button.disabled = true; button.textContent = 'Checking…';
  try {
    const response = await fetch('/api/lagna', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body), signal:AbortSignal.timeout(20000)});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Lagna options are unavailable.');
    const spans = data.spans;
    if (!spans.length) return fail('That lagna does not rise at your birthplace on that date. Check the date, place and time zone.');
    const how = m === 'known' ? 'chosen by you' : 'the only one that fits your time window';
    if (spans.length === 1) return chooseSpan(base, spans[0], how);
    choicesBox.innerHTML = `<p class="eyebrow">${m === 'known' ? 'Your lagna rises twice on this date' : 'Which of these fits you?'}</p>` + spans.map((s, i) => `<button type="button" class="secondary choice" data-i="${i}"><b>${escape(lagnaName(s.lagna))} lagna</b><br><small>${escape(spanText(s))}${s.cut_by_window && m === 'window' ? ' · continues past your window' : ''}</small></button>`).join('') + '<p class="help">If you can narrow your time window, you get fewer options. Pick the one that matches what your family remembers.</p>';
    choicesBox.hidden = false;
    choicesBox.querySelectorAll('.choice').forEach(b => b.addEventListener('click', () => chooseSpan(base, spans[Number(b.dataset.i)], 'chosen by you from the options')));
  } catch (e) { fail(e.name === 'TimeoutError' ? 'That took too long. Try again.' : e.message); }
  finally { button.disabled = false; button.textContent = 'Calculate chart'; }
}
form.addEventListener('submit', async e => {
  e.preventDefault(); error.hidden = true; output.hidden = true; choicesBox.hidden = true;
  document.querySelector('#empty').hidden = false;
  if (!form.elements.date.value) return fail('Choose the full date of birth: day, month and a four-digit year.');
  if (timeMode() === 'sure' && !form.elements.time.value) return fail('Choose the time of birth: hour, minute and AM or PM.');
  if (form.elements.latitude.value === '' || form.elements.longitude.value === '') {
    const ok = await findCoordinates();
    if (!ok || form.elements.latitude.value === '') return;
  }
  const values = Object.fromEntries(new FormData(form));
  const birth = {date: values.date, time: values.time, timezone: values.timezone === '__other' ? (values.timezone_other || '').trim() : values.timezone, place: values.place,
    latitude: Number(values.latitude), longitude: Number(values.longitude)};
  if (timeMode() !== 'sure') return lagnaOptions(birth);
  runCalc(birth, '');
});
document.querySelector('#example').addEventListener('click', () => {
  const example = {place:'Synthetic example',timezone:'Asia/Kolkata',latitude:13,longitude:80};
  for (const [key, value] of Object.entries(example)) form.elements[key].value = value;
  setPickers('2000-01-01', '14:30');
  form.elements.timezone.dispatchEvent(new Event('change'));
  resolvedFromLookup = false; resolved.hidden = true; candidatesBox.hidden = true; error.hidden = true;
});


// ---- Friendly date, time and time-zone pickers
const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const dayEl = document.querySelector('#d-day'), monEl = document.querySelector('#d-mon'), yearEl = document.querySelector('#d-year');
const hourEl = document.querySelector('#t-hour'), minEl = document.querySelector('#t-min'), ampmEl = document.querySelector('#t-ampm');
const dateEcho = document.querySelector('#date-echo');
const pad = n => String(n).padStart(2, '0');
function syncDate() {
  const d = Number(dayEl.value), m = Number(monEl.value), y = Number(yearEl.value);
  form.elements.date.value = '';
  if (!d || !m || !/^\d{4}$/.test(yearEl.value)) { dateEcho.textContent = ''; return; }
  const dt = new Date(Date.UTC(y, m - 1, d));
  if (y < 1800 || y > 2399 || dt.getUTCMonth() !== m - 1) { dateEcho.textContent = y < 1800 || y > 2399 ? 'Year must be between 1800 and 2399.' : `${MONTHS[m - 1]} ${y} has no day ${d}.`; return; }
  form.elements.date.value = `${y}-${pad(m)}-${pad(d)}`;
  dateEcho.textContent = dt.toLocaleDateString(interfaceLanguage==='ta'?'ta-IN':'en-GB', {weekday:'long', day:'numeric', month:'long', year:'numeric', timeZone:'UTC'});
  relabelZones();
}
function syncTime() {
  const h = Number(hourEl.value), mi = minEl.value;
  form.elements.time.value = (!h || mi === '' || !ampmEl.value) ? '' : `${pad(h % 12 + (ampmEl.value === 'PM' ? 12 : 0))}:${pad(Number(mi))}`;
}
for (const el of [dayEl, monEl, yearEl]) el.addEventListener('input', syncDate);
for (const el of [hourEl, minEl, ampmEl]) el.addEventListener('input', syncTime);
function setPickers(date, time) {
  const [y, m, d] = date.split('-').map(Number);
  yearEl.value = y; monEl.value = m; dayEl.value = d; syncDate();
  const [hh, mm] = time.split(':').map(Number);
  hourEl.value = hh % 12 || 12; minEl.value = mm; ampmEl.value = hh >= 12 ? 'PM' : 'AM'; syncTime();
}
function zoneOffset(zone) {
  try {
    const iso = form.elements.date.value;
    const at = iso ? new Date(`${iso}T12:00:00Z`) : new Date();
    const part = new Intl.DateTimeFormat('en', {timeZone: zone, timeZoneName: 'shortOffset'}).formatToParts(at).find(p => p.type === 'timeZoneName');
    return part ? part.value.replace('GMT', 'UTC') : '';
  } catch { return ''; }
}
function relabelZones() {
  for (const o of form.elements.timezone.options) {
    if (o.value === '__other') continue;
    o.dataset.base ??= o.textContent.replace(/ \(.*\)$/, '');
    const off = zoneOffset(o.value);
    o.textContent = off ? `${o.dataset.base} · ${off}` : o.dataset.base;
  }
}
function fillZoneList() {
  const zones = typeof Intl.supportedValuesOf === 'function' ? Intl.supportedValuesOf('timeZone') : [];
  document.querySelector('#zone-list').innerHTML = zones.map(z => `<option value="${escape(z)}">${escape(zoneOffset(z))}</option>`).join('');
}
relabelZones(); fillZoneList();

form.elements.timezone.addEventListener('change', () => {
  const other = form.elements.timezone.value === '__other';
  document.querySelector('#zone-other-wrap').hidden = !other;
  form.elements.timezone_other.required = other;
  if (other) form.elements.timezone_other.focus();
});


/* ---------- Story view: swipeable cards, one beat per card ---------- */
function storyCards(report) {
  const cards = [];
  const chip = (t, k) => `<span class="chip ${k || ''}">${escape(t)}</span>`;
  const why = rules => rules?.length ? `<details class="why"><summary>Why the chart says this</summary><ul class="cond-list">${rules.map(r => `<li>${escape(r.sign ? r.sign + ': ' : '')}${escape(r.effect)} <span class="route-source">${sourceLink(r.source)}</span></li>`).join('')}</ul></details>` : '';
  const add = (eyebrow, title, body, extra) => cards.push({eyebrow, title, body, extra: extra || ''});
  const w = report.who_you_are, lp = report.life_periods;
  add('Your reading', 'Your life in about a minute', '<p>A short read: who you are, the stretch of life you are in, the phase you are in right now and what helps. Tap Next or swipe. Everything else is one tap away at the end.</p>');
  if (w) {
    const pt = o => `<p class="p-hl">${o.pointers.map(k => `<span class="hl">${escape(k)}</span>`).join('')}</p>`;
    add('Who you are', 'The person behind the chart', `<p><strong>How you come across.</strong> ${escape(w.outer_you.text)}</p>${w.same_sign ? '<p class="muted">Your inner nature points the same way.</p>' : `<p><strong>Your inner nature.</strong> ${escape(w.inner_you.text)}</p>`}${pt(w.outer_you)}`, why(w.outer_you.rules.concat(w.same_sign ? [] : w.inner_you.rules)));
  }
  const toneCls = t => ({strong: 'tone-strong', weak: 'tone-weak', mixed: 'tone-mixed'}[t] || 'tone-mixed');
  const periods = lp?.periods || [];
  const cur = periods.find(p => p.when === 'now'), nxt = periods.find(p => p.when === 'next');
  const yrOf = p => `${p.years_about[0]} to ${p.years_about[1]}`;
  if (cur) {
    const rulesWhy = why((cur.rules || []).map(r => ({effect: r.effect, source: r.source})));
    const basis = `<details class="why"><summary>The chart basis</summary><p class="route-caveat">Ruling planet: ${escape(cur.lord)}. ${escape((cur.basis || []).join('; '))}.</p></details>`;
    const chips = Object.values(cur.aspects || {}).filter(a => a.status !== 'quiet').map(a => `<span class="hl">${escape(a.label)}: ${escape(a.status)}</span>`).join('');
    add('Right now', yrOf(cur), `<p>${chip(cur.label, toneCls(cur.tone))}</p><p>${escape(cur.you_text || cur.summary)}</p>${chips ? `<p class="p-hl">${chips}</p>` : ''}${cur.confidence === 'tentative' ? '<p class="route-caveat">The chart is less clear-cut for this stretch, so read it as a softer signal.</p>' : ''}`, rulesWhy + basis);
    const yr = new Date().getFullYear();
    const ph = [...(cur.bhuktis || [])].filter(b => b.years_about[0] <= yr && yr <= b.years_about[1]).sort((x, y) => y.years_about[0] - x.years_about[0])[0];
    if (ph) add('Your current phase', `About ${ph.years_about[0]} to ${ph.years_about[1]}`, `<p>${chip(ph.label)}</p>${(ph.phase_areas || []).length ? ph.phase_areas.map(x => `<p><strong>${escape(x.label)}.</strong> ${escape(x.text)}</p>`).join('') + '<p class="route-caveat">Areas for a smaller phase are our reading, not stated by the book.</p>' : '<p>No single area stands out in this phase, so the overall feel of your stretch applies.</p>'}`, `<details class="why"><summary>Why the chart says this</summary><p class="route-caveat">${escape(ph.basis)}</p></details>`);
    const gl = Object.values(cur.aspects || {}).filter(a => a.guidance).sort((x, y) => (x.status === 'testing' ? 0 : 1) - (y.status === 'testing' ? 0 : 1)).slice(0, 3);
    if (gl.length) add('What helps', 'What to lean on, what to watch', gl.map(a => `<p><strong>${escape(a.label)}.</strong> ${escape(a.text)}</p><p class="guide">${escape(a.guidance)}</p>`).join(''), `<details class="why"><summary>Why the chart says this</summary><ul class="cond-list">${gl.flatMap(a => a.items || []).map(i => `<li>${escape(i.effect)} <span class="route-source">${sourceLink(i.source)}</span></li>`).join('')}</ul></details>`);
  }
  if (nxt) {
    const chips = Object.values(nxt.aspects || {}).filter(a => a.status !== 'quiet').map(a => `<span class="hl">${escape(a.label)}: ${escape(a.status)}</span>`).join('');
    add('Coming next', yrOf(nxt), `<p>${chip(nxt.label, toneCls(nxt.tone))}</p><p>${escape(nxt.you_text || nxt.summary)}</p>${chips ? `<p class="p-hl">${chips}</p>` : ''}`, why((nxt.rules || []).map(r => ({effect: r.effect, source: r.source}))));
  }
  add('The fine print', 'There is more', `<p>${escape(lp?.notice || 'Themes from one classical text, not fixed events.')}</p><p>Not tested against real outcomes. Not medical, legal or financial advice.</p><p><button type="button" class="story-jump" data-jump="periods-title">See every stretch, phase and area</button></p>`);
  return cards;
}

function openStory() {
  const report = window.__lastReport; if (!report) return;
  let cards = storyCards(report); let i = 0;
  const ov = document.createElement('div'); ov.className = 'story'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Your life as a story');
  ov.innerHTML = '<button type="button" class="story-language">தமிழ் / English</button><div class="story-bars"></div><button type="button" class="story-close" aria-label="Close story">×</button><div class="story-card" tabindex="0"></div><button type="button" class="story-prev" aria-label="Previous card">Back</button><button type="button" class="story-next" aria-label="Next card">Next</button><p class="story-count"></p>';
  document.body.appendChild(ov); document.body.classList.add('story-on');
  const bars = ov.querySelector('.story-bars'), card = ov.querySelector('.story-card'), count = ov.querySelector('.story-count');
  bars.innerHTML = cards.map(() => '<i></i>').join('');
  const close = () => { ov.remove(); document.body.classList.remove('story-on'); document.removeEventListener('keydown', key); document.removeEventListener('languagechange', languageChanged); document.querySelector('#story-open')?.focus(); };
  const show = n => { i = Math.max(0, Math.min(cards.length - 1, n)); const c = cards[i];
    card.innerHTML = `<p class="eyebrow">${escape(c.eyebrow)}</p><h2>${escape(c.title)}</h2><div class="story-body">${c.body}</div>${c.extra}`; card.scrollTop = 0;
    [...bars.children].forEach((b, k) => b.className = k < i ? 'done' : k === i ? 'cur' : '');
    count.textContent = `${i + 1} of ${cards.length}`; };
  const key = e => { if (e.key === 'ArrowRight') show(i + 1); else if (e.key === 'ArrowLeft') show(i - 1); else if (e.key === 'Escape') close(); };
  document.addEventListener('keydown', key);
  ov.querySelector('.story-next').onclick = () => i === cards.length - 1 ? close() : show(i + 1);
  ov.querySelector('.story-prev').onclick = () => show(i - 1);
  ov.querySelector('.story-close').onclick = close;
  let x0 = null; ov.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, {passive: true});
  ov.addEventListener('touchend', e => { if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1)); });
  const languageChanged=()=>{cards=storyCards(report);show(i);};document.addEventListener('languagechange',languageChanged);ov.querySelector('.story-language').onclick=()=>document.querySelector(`[data-language=${interfaceLanguage==='ta'?'en':'ta'}]`).click();show(0); card.focus();
}
document.addEventListener('click', e => {
  if (e.target.closest('#story-open')) openStory();
  const j = e.target.closest('.story-jump');
  if (j) { document.querySelector('.story .story-close')?.click(); setTimeout(() => document.getElementById(j.dataset.jump)?.scrollIntoView({behavior: 'smooth'}), 50); }
});

/* Client notebook. Explicit save only. Never sends records or notes to a server. */
(() => {
  const KEY = 'horoscope-client-notebook-v1';
  let selected = null, editingConsult = null, records = [], ready = true, storedRaw = null;
  const panel = document.createElement('section');
  panel.className = 'client-panel'; panel.setAttribute('aria-labelledby','clients-title');
  panel.innerHTML = `<details><summary id="clients-title">Client notebook</summary>
  <p class="muted">Saved only in this browser on this device. Not encrypted, not synced and not a cloud backup. Anyone using this browser can read the records. Save only with the client's permission. Clearing browser data deletes them.</p>
  <label>Find a client<input id="client-search" maxlength="120" type="search"></label><div id="client-list"></div>
  <button type="button" class="secondary" id="client-new">New client</button>
  <form id="client-form"><label>Client name or private label<input id="client-name" maxlength="120" required autocomplete="off"></label>
  <p id="client-birth" class="help">Fill the birth form, then save it here. An uncertain time stays uncertain.</p>
  <button type="submit">Save birth details to this browser</button></form>
  <div id="client-detail" hidden><div class="pair"><button type="button" class="secondary" id="client-load">Load birth details</button><button type="button" class="secondary" id="client-delete">Delete client</button></div>
  <h3>Consultation history</h3><p class="help">Keep the astrologer's reading separate from what the client later reports. These notes are not proof that a forecast is accurate. Nothing is submitted for benchmarking.</p>
  <form id="consult-form"><label>Consultation date<input id="consult-date" type="date" required></label>
  <label>Astrologer's reading<textarea id="consult-reading" maxlength="8000" rows="3"></textarea></label>
  <label>Client-reported events / follow-up<textarea id="consult-observed" maxlength="8000" rows="3"></textarea></label>
  <label>Private notes<textarea id="consult-notes" maxlength="8000" rows="3"></textarea></label>
  <button type="submit">Save consultation</button></form><div id="consult-list"></div></div>
  <details><summary>Private backup</summary><p class="help">Backup files include all birth details and private notes. Keep them somewhere private. Import adds records, never overwrites existing ones.</p>
  <button type="button" class="secondary" id="clients-export">Download private backup</button><label>Import a notebook backup<input id="clients-import" type="file" accept="application/json,.json"></label></details>
  <p id="client-status" role="status"></p></details>`;
  document.querySelector('.layout').after(panel);
  const style = document.createElement('style'); style.textContent = '.client-panel{margin-top:30px;border-top:1px solid var(--line);max-width:720px}.client-panel textarea{width:100%;min-height:90px;font:14px Arial;padding:10px;border:1px solid #cdc9ca;border-radius:4px;margin-top:6px}.client-panel textarea:focus{outline:2px solid var(--teal)}.client-item,.consult-item{border:1px solid var(--line);padding:14px;margin-top:12px;border-radius:4px;overflow-wrap:anywhere}.consult-item p{white-space:pre-wrap;font-size:13px}.client-panel h3{margin-top:24px}#client-status{font-size:13px;color:var(--teal)}'; document.head.append(style);
  const $ = id => panel.querySelector('#'+id);
  const say = msg => { $('client-status').textContent = msg; };
  const id = () => crypto.randomUUID();
  const current = () => records.find(r => r.id === selected);
  function validate(data) {
    if (!data || data.version !== 1 || !Array.isArray(data.records) || data.records.length > 500) throw Error('Not a supported notebook backup.');
    const seen = new Set();
    for (const r of data.records) {
      if (!r || typeof r.id !== 'string' || seen.has(r.id) || typeof r.name !== 'string' || !r.name.trim() || r.name.length > 120 || !r.input || !Array.isArray(r.consultations) || r.consultations.length > 1000) throw Error('Invalid client record. Nothing was imported.');
      seen.add(r.id);
      const b = r.input;
      if (!/^\d{4}-\d{2}-\d{2}$/.test(b.date) || !['sure','window','known'].includes(b.timemode) || typeof b.place !== 'string' || b.place.length > 120 || typeof b.timezone !== 'string' || b.timezone.length > 120 || !Number.isFinite(b.latitude) || !Number.isFinite(b.longitude) || Math.abs(b.latitude)>=90 || Math.abs(b.longitude)>180) throw Error('Invalid birth details. Nothing was imported.');
      const dateObj=new Date(b.date+'T12:00:00Z'); if(!Number.isFinite(dateObj.getTime())||dateObj.toISOString().slice(0,10)!==b.date||Number(b.date.slice(0,4))<1800||Number(b.date.slice(0,4))>2399)throw Error('Invalid birth date.');
      if(b.node_mode!=null&&!['mean','true'].includes(b.node_mode))throw Error('Invalid node convention.');if(b.tamil_view!=null&&typeof b.tamil_view!=='boolean')throw Error('Invalid Tamil view.');try{new Intl.DateTimeFormat('en',{timeZone:b.timezone});}catch{throw Error('Invalid birth time zone.');}
      const clockOk=t=>/^([01]\d|2[0-3]):[0-5]\d$/.test(t);
      if(b.timemode==='sure'&&!clockOk(b.time)||b.timemode==='window'&&(!clockOk(b.win_start)||!clockOk(b.win_end))||b.timemode==='known'&&!['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'].includes(b.known_lagna))throw Error('Invalid birth-time choice.');
      for (const key of ['time','win_start','win_end','known_lagna','known_around']) if (typeof b[key] !== 'string' || b[key].length > 30) throw Error('Invalid birth-time fields.');
      for (const c of r.consultations) if (!c || typeof c.id !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(c.date) || ['reading','observed','notes'].some(k => typeof c[k] !== 'string' || c[k].length > 8000)) throw Error('Invalid consultation. Nothing was imported.');
    }
    // Whitelist fields: untrusted backup content never becomes markup or executable code.
    return data.records.map(r=>({id:r.id,name:r.name,input:{...Object.fromEntries(['date','time','timezone','place','latitude','longitude','timemode','win_start','win_end','known_lagna','known_around','node_mode','tamil_view'].map(k=>[k,r.input[k]]))},consultations:r.consultations.map(c=>({id:c.id,date:c.date,reading:c.reading,observed:c.observed,notes:c.notes})),updated:typeof r.updated==='string'?r.updated:''}));
  }
  try { const raw = localStorage.getItem(KEY); storedRaw = raw; if (raw) records = validate(JSON.parse(raw)); }
  catch { ready = false; say('Saved records could not be read. They have not been overwritten. Download the stored backup before repairing browser data.'); }
  function persist(next) {
    if (!ready) throw Error('Storage is unavailable or unreadable. No records were changed.');
    if (localStorage.getItem(KEY) !== storedRaw) throw Error("Notebook changed in another tab. Reload before saving; nothing was overwritten.");
    validate({version:1,records:next});
    try { const raw = JSON.stringify({version:1,records:next}); localStorage.setItem(KEY, raw); storedRaw = raw; }
    catch { throw Error('Browser storage is full or unavailable. Nothing was saved. Download a backup and try again.'); }
    records = next;
  }
  function renderNotebook() {
    $('client-list').replaceChildren();
    const q = $('client-search').value.toLowerCase();
    records.filter(r=>r.name.toLowerCase().includes(q)).forEach(r=>{
      const b=document.createElement('button'); b.type='button';b.className='secondary client-item';b.dataset.private='';b.textContent=`${r.name} · ${r.input.date} · ${r.input.place}`;
      b.onclick=()=>{editingConsult=null; $('consult-form button').textContent='Save consultation'; for(const k of ['consult-reading','consult-observed','consult-notes'])$(k).value='';selected=r.id; $('client-name').value=r.name;renderNotebook();};$('client-list').append(b);
    });
    const r=current(); $('client-detail').hidden=!r;
    $('client-birth').textContent=r ? `Saved: ${r.input.date} · ${r.input.timemode==='sure'?r.input.time:r.input.timemode==='window'?`uncertain, ${r.input.win_start} to ${r.input.win_end}`:`known lagna: ${r.input.known_lagna}`} · ${r.input.place}. Saving again replaces these birth details with the current form; consultation notes stay.` : 'Fill the birth form, then save it here. An uncertain time stays uncertain.';
    if(r){const line=$('client-birth'),raw=line.textContent,place=r.input.place,pos=raw.lastIndexOf(place);if(pos>=0){line.replaceChildren(document.createTextNode(raw.slice(0,pos)));const privatePlace=document.createElement('span');privatePlace.dataset.private='';privatePlace.textContent=place;line.append(privatePlace,document.createTextNode(raw.slice(pos+place.length)));}}
    $('consult-list').replaceChildren();
    if(r) [...r.consultations].reverse().forEach(c=>{
      const card=document.createElement('article');card.className='consult-item';
      const title=document.createElement('h3');title.textContent=c.date;card.append(title);
      for(const [key,label] of [['reading',"Astrologer's reading"],['observed','Client-reported events / follow-up'],['notes','Private notes']]) if(c[key]) {const p=document.createElement('p');const heading=document.createElement('strong');heading.textContent=label+': ';const note=document.createElement('span');note.dataset.private='';note.textContent=c[key];p.append(heading,note);card.append(p);}
      const edit=document.createElement('button');edit.type='button';edit.className='secondary';edit.textContent='Edit consultation';edit.onclick=()=>{editingConsult=c.id; $('consult-date').value=c.date;for(const [k,v] of [['consult-reading',c.reading],['consult-observed',c.observed],['consult-notes',c.notes]])$(k).value=v;$('consult-form button').textContent='Update consultation';$('consult-date').focus();};card.append(edit);
      const del=document.createElement('button');del.type='button';del.className='secondary';del.textContent='Delete consultation';del.onclick=()=>{if(!confirm('Delete this consultation permanently from this browser?'))return;try{persist(records.map(x=>x.id===r.id?{...x,consultations:x.consultations.filter(z=>z.id!==c.id)}:x));renderNotebook();say('Consultation deleted.');}catch(e){say(e.message);}};card.append(del);$('consult-list').append(card);
    });
  }
  function inputSnapshot() {
    const v=Object.fromEntries(new FormData(form));
    if(!v.date || !v.place.trim() || v.latitude==='' || v.longitude==='')throw Error('Complete the birth date, birthplace and coordinates first.');
    if(v.timemode==='sure'&&!v.time)throw Error('Choose the birth time first.');
    if(v.timemode==='window'&&(!v.win_start||!v.win_end))throw Error('Choose the earliest and latest possible time.');
    if(v.timemode==='known'&&!v.known_lagna)throw Error('Choose the known lagna.');
    return {date:v.date,time:v.time,timezone:v.timezone==='__other'?v.timezone_other.trim():v.timezone,place:v.place.trim(),latitude:Number(v.latitude),longitude:Number(v.longitude),node_mode:form.elements.node_mode.value,tamil_view:document.querySelector('#tamil-view').checked,timemode:v.timemode,win_start:v.win_start,win_end:v.win_end,known_lagna:v.known_lagna,known_around:v.known_around};
  }
  $('client-form').onsubmit=e=>{e.preventDefault();try{const input=inputSnapshot(),name=$('client-name').value.trim();if(!name)throw Error('Give this client a name or private label.');const r=current();if(r&&!confirm('Replace the saved birth details for '+r.name+' with the current birth form?'))return;const saved={id:r?.id||id(),name,input,consultations:r?.consultations||[],updated:new Date().toISOString()};persist(r?records.map(x=>x.id===r.id?saved:x):[...records,saved]);selected=saved.id;renderNotebook();say('Birth details saved in this browser only.');}catch(e){say(e.message);}};
  $('client-new').onclick=()=>{selected=null;editingConsult=null;$('consult-form button').textContent='Save consultation';for(const k of ['consult-reading','consult-observed','consult-notes'])$(k).value='';$('client-name').value='';renderNotebook();say('New client. Fill or check the birth form before saving.');$('client-name').focus();};
  $('client-search').oninput=renderNotebook;
  $('client-load').onclick=()=>{const r=current();if(!r)return;if(!confirm('Replace the current birth form with '+r.name+"'s saved details?"))return;const b=r.input;form.elements.node_mode.value=b.node_mode==='true'?'true':'mean';document.querySelector('#tamil-view').checked=b.tamil_view!==false;setPickers(b.date,b.time||'00:00');if(!b.time){hourEl.value='';minEl.value='';ampmEl.value='';syncTime();}for(const k of ['place','latitude','longitude','timemode','win_start','win_end','known_lagna','known_around'])form.elements[k].value=b[k];const available=[...form.elements.timezone.options].some(o=>o.value===b.timezone);form.elements.timezone.value=available?b.timezone:'__other';form.elements.timezone_other.value=available?'':b.timezone;form.elements.timezone.dispatchEvent(new Event('change'));applyMode();resolvedFromLookup=false;resolved.hidden=true;candidatesBox.hidden=true;choicesBox.hidden=true;output.hidden=true;document.querySelector('#empty').hidden=false;say('Saved details loaded. Check them, then calculate a fresh chart.');document.querySelector('#birth-title').scrollIntoView({behavior:'smooth'});};
  $('client-delete').onclick=()=>{const r=current();if(!r||!confirm('Delete '+r.name+' and all their consultation notes permanently from this browser?'))return;try{persist(records.filter(x=>x.id!==r.id));selected=null;$('client-name').value='';renderNotebook();say('Client and consultation history deleted.');}catch(e){say(e.message);}};
  $('consult-date').value=new Date().toLocaleDateString('en-CA');
  $('consult-form').onsubmit=e=>{e.preventDefault();try{const r=current();if(!r)throw Error('Select a client first.');const c={id:editingConsult||id(),date:$('consult-date').value,reading:$('consult-reading').value.trim(),observed:$('consult-observed').value.trim(),notes:$('consult-notes').value.trim()};if(!c.reading&&!c.observed&&!c.notes)throw Error('Add a reading, follow-up or note first.');persist(records.map(x=>x.id===r.id?{...x,consultations:editingConsult?x.consultations.map(z=>z.id===editingConsult?c:z):[...x.consultations,c],updated:new Date().toISOString()}:x));editingConsult=null;$('consult-form button').textContent='Save consultation';for(const k of ['consult-reading','consult-observed','consult-notes'])$(k).value='';renderNotebook();say('Consultation saved locally. Nothing was sent for benchmarking.');}catch(e){say(e.message);}};
  $('clients-export').onclick=()=>{try{const raw=ready?JSON.stringify({version:1,records},null,2):localStorage.getItem(KEY);if(!raw)throw Error('No saved backup is available.');const blob=new Blob([raw],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='horoscope-private-notebook.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);say('Private backup downloaded. It contains client birth details and notes.');}catch(e){say(e.message);}};
  $('clients-import').onchange=async()=>{try{const file=$('clients-import').files[0];if(!file)return;if(file.size>5*1024*1024)throw Error('Backup exceeds the 5 MB limit.');const added=validate(JSON.parse(await file.text()));if(!confirm(`Add ${added.length} client records from this private backup? Existing records will stay unchanged.`))return;persist([...records,...added.map(r=>({...r,id:id(),consultations:r.consultations.map(c=>({...c,id:id()}))}))]);renderNotebook();say(`${added.length} client records imported. Existing records were not overwritten.`);}catch(e){say(e.message);}finally{$('clients-import').value='';}};
  window.addEventListener('storage',e=>{if(e.key!==KEY)return;try{storedRaw=e.newValue;records=e.newValue?validate(JSON.parse(e.newValue)):[];ready=true;selected=null;$('client-name').value='';renderNotebook();say('Notebook updated in another tab. Select a client again before editing.');}catch{ready=false;say('Notebook changed in another tab and could not be read. Writes are paused.');}});
  const privacy=[...form.querySelectorAll('.help')].find(e=>e.textContent.startsWith('No account.'));
  if(privacy) privacy.textContent="No account. Birth details are sent only to this app's own calculation endpoints. The place name goes to OpenStreetMap's Nominatim for lookup. Nothing is saved unless you choose Save in the client notebook. Notes stay in this browser; no analytics or automatic benchmarking.";
  renderNotebook();
})();

// Tamil-first birth sheet. Modern astronomical profiles are stated, not hidden.
const PLANET_TA={Sun:'சூரியன்',Moon:'சந்திரன்',Mars:'செவ்வாய்',Mercury:'புதன்',Jupiter:'குரு',Venus:'சுக்கிரன்',Saturn:'சனி',Rahu:'ராகு',Ketu:'கேது'};
const TITHI_TA=['பிரதமை','துவிதியை','திருதியை','சதுர்த்தி','பஞ்சமி','சஷ்டி','சப்தமி','அஷ்டமி','நவமி','தசமி','ஏகாதசி','துவாதசி','திரயோதசி','சதுர்த்தசி'];
const YOGA_TA=['விஷ்கம்பம்','பிரீதி','ஆயுஷ்மான்','சௌபாக்கியம்','சோபனம்','அதிகண்டம்','சுகர்மம்','திருதி','சூலம்','கண்டம்','விருத்தி','துருவம்','வியாகாதம்','ஹர்ஷணம்','வஜ்ரம்','சித்தி','வியதீபாதம்','வரியான்','பரிகம்','சிவம்','சித்தம்','சாத்தியம்','சுபம்','சுப்பிரம்','பிராமியம்','ஐந்திரம்','வைதிருதி'];
const localStamp=(value,zone)=>value?new Intl.DateTimeFormat('en-GB',{timeZone:zone,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(value)):'Unavailable';
const tamilLord=n=>`${PLANET_TA[n]||n} / ${n}`;
function karanaName(i){return i===1?'கிம்ஸ்துக்னம்':i<=57?['பவம்','பாலவம்','கௌலவம்','தைதுலம்','கரசை','வணிசை','பத்திரை'][(i-2)%7]:['சகுனி','சதுஷ்பாதம்','நாகவம்'][i-58];}
function tamilSheet(report,birth){
  const p=report.tamil_panchangam;if(!p)return '';
  const d=p.tamil_solar_date, c=report.natal_chart;
  const naz=p.udayadi_nazhikai==null?'Unavailable':`${Math.floor(p.udayadi_nazhikai)} நா. ${p.udayadi_vinadi.toFixed(2)} வி.`;
  const tithi=p.tithi_in_paksha===15?(p.tithi_index_1_based===15?'பௌர்ணமி':'அமாவாசை'):TITHI_TA[p.tithi_in_paksha-1];
  const fields=[['தமிழ் தேதி / Solar date',d.status==='computed_profile'?`${d.year_name} · ${interfaceLanguage==='en'?['Chithirai','Vaikasi','Aani','Aadi','Aavani','Purattasi','Aippasi','Karthigai','Margazhi','Thai','Maasi','Panguni'][d.month_index_1_based-1]:d.month} ${d.day}`:'Unavailable'],['கிழமை / Weekday',p.weekday],['நட்சத்திரம் / Star',`${p.nakshatra_tamil} · ${p.pada} பாதம்`],['உதயம் / Sunrise',localStamp(p.sunrise,p.timezone)],['அஸ்தமனம் / Sunset',localStamp(p.sunset,p.timezone)],['உதயாதி / From last sunrise',naz],['நட்சத்திர மணி / Sidereal clock',p.local_apparent_sidereal_time],['திதி / Tithi',`${tithi} · ${p.paksha}`],['யோகம் / Yoga',YOGA_TA[p.yoga_index_1_based-1]],['கரணம் / Karana',karanaName(p.karana_half_index_1_based)],['அயனாம்சம் / Lahiri',`${p.ayanamsa_degrees.toFixed(6)}°`],['நேர மண்டலம் / Time zone',`${p.timezone} · UTC ${p.utc_offset_seconds/3600>=0?'+':''}${(p.utc_offset_seconds/3600).toFixed(4)} h`]];
  const longitudeRows=[...Object.entries(c.placements),['Ketu',{longitude:p.ketu_longitude,sign:Object.keys(LAGNA_TA)[Math.floor(p.ketu_longitude/30)]}]];
  const charts=['rasi','navamsa'].map(kind=>southChart(p.chart_signs,kind)).join('');
  const planets=longitudeRows.map(([name,x])=>`<div class="tamil-position"><strong>${escape(tamilLord(name))}</strong><span>${escape(LAGNA_TA[x.sign]||x.sign)} · ${(x.longitude%30).toFixed(5)}°</span></div>`).join('');
  const periods=Object.entries(report.timing_conditional.timelines).map(([key,t])=>`<details class="tamil-period"><summary>${t.balance_reading==='moon_longitude_uniform'?'Longitude balance / கோண இருப்பு':'Moon crossing time / கடக்கும் நேரம்'} · ${t.year_length_days}-day year</summary><p>Dates are local to ${escape(birth.timezone)}. From is inclusive; To is the next boundary, exclusive. First period is its remainder at birth.</p>${t.mahadasas.map(m=>`<details><summary>${escape(tamilLord(m.lord))}: ${localStamp(m.start,birth.timezone)} to ${localStamp(m.end,birth.timezone)}</summary>${m.antardasas.map(a=>`<div class="bhukti-row"><strong>${escape(tamilLord(a.lord))} புத்தி</strong><span>${localStamp(a.start,birth.timezone)}<br>to ${localStamp(a.end,birth.timezone)}</span></div>`).join('')}</details>`).join('')}</details>`).join('');
  return `<section class="tamil-sheet" aria-labelledby="tamil-title"><p class="eyebrow">தமிழ் முதலில் / Tamil-first</p><h2 id="tamil-title">பிறப்பு ஜாதகக் குறிப்பு / Birth sheet</h2><div class="tamil-fields">${fields.map(([label,value])=>`<div><span>${escape(label)}</span><strong>${escape(value)}</strong></div>`).join('')}</div><p class="help">Solar date: local-sunset Lahiri profile, not a Vakya calendar. Panchang angles are at birth. Before sunrise, udayadi uses the previous day's sunrise. Missing polar events stay unavailable.</p>${charts}<details><summary>கிரக நிலைகள் / Planet degrees</summary><p>${escape(p.node_mode)} Rahu; Ketu is 180° opposite. Absolute longitudes remain in the report.</p>${planets}</details><details><summary>முறை / Calculation profiles</summary><p>${escape(p.solar_event_profile)}</p><p>${escape(p.sidereal_clock_notice)}</p><p>${escape(d.notice||d.reason)}</p><p>1 நாழிகை = 24 minutes; 1 வினாடி = 24 seconds. No terrain or observed sunrise correction.</p></details><h3>திசை - புத்தி / Dasha - bhukti</h3><p>Four named Vimshottari options. No single historical convention or site formula is selected. Expand the one you use.</p>${periods}<p class="aspect-limit">${escape(p.notice)}</p></section>`;
}

function southChart(signs,kind){
  const layout=['Pisces','Aries','Taurus','Gemini','Aquarius',null,null,'Cancer','Capricorn',null,null,'Leo','Sagittarius','Scorpio','Libra','Virgo'];
  const short={Sun:'சூ',Moon:'சந்',Mars:'செ',Mercury:'பு',Jupiter:'கு',Venus:'சு',Saturn:'சனி',Rahu:'ரா',Ketu:'கே',Lagna:'லக்'};
  return `<div class="south-chart" role="img" aria-label="${kind==='rasi'?'South Indian rasi chart':'South Indian navamsa chart'}"><div class="south-centre">${kind==='rasi'?'இராசி / Rasi':'நவாம்சம் / Navamsa'}<small>Fixed signs<br>லக் = lagna</small></div>${layout.map((sign,i)=>sign?`<div class="south-cell" style="grid-column:${i%4+1};grid-row:${Math.floor(i/4)+1}"><span>${escape(LAGNA_TA[sign])}</span><strong>${Object.entries(signs).filter(([name,x])=>x[kind]===sign).map(([n])=>interfaceLanguage==='en'?({Sun:'Su',Moon:'Mo',Mars:'Ma',Mercury:'Me',Jupiter:'Ju',Venus:'Ve',Saturn:'Sa',Rahu:'Ra',Ketu:'Ke',Lagna:'Asc'}[n]):short[n]).join(' · ')}</strong></div>`:'').join('')}</div>`;
                                             }

// Display-only inspection. No report fields or calculation requests are changed.
let inspectionState = {view:'plain', profile:'', at:new Date().toISOString().slice(0,19), house:1, planet:'Jupiter'};
const astText=(en,ta)=>interfaceLanguage==='ta'?ta:en;
const astPlanet=n=>interfaceLanguage==='ta'?(PLANET_TA[n]||n):n;
const astSign=n=>interfaceLanguage==='ta'?(LAGNA_TA[n]||n):n;
function activeInspectionPeriod(timeline, instant) {
  const t=Date.parse(instant);
  if(!Number.isFinite(t)||!timeline)return null;
  const maha=timeline.mahadasas.find(p=>Date.parse(p.start)<=t&&t<Date.parse(p.end));
  if(!maha)return null;
  return {maha,bhukti:(maha.antardasas||[]).find(p=>Date.parse(p.start)<=t&&t<Date.parse(p.end))||null};
}
function houseDistance(reference, placement){return ((placement-reference+12)%12)+1;}
function inspectionPlanetCard(name,report,compact=false){
 const chart=report.natal_chart,p=chart.placements[name];
 if(!p)return `<p>${escape(astPlanet(name))}: ${astText('Not supplied in this report.','இந்த அறிக்கையில் அளிக்கப்படவில்லை.')}</p>`;
 const f=chart.structural_factors_from_ascendant?.planet_factors?.find(x=>x.planet===name);
 const strength=report.shadbala_working_profile?.planets?.[name];
 const dignity=chart.natal_factors?.dignity?.[name]?.flags;
 const conditions=dignity?Object.entries(dignity).filter(([,v])=>v===true).map(([k])=>({own_sign:astText('Own sign','ஆட்சி'),exaltation_sign:astText('Exaltation sign','உச்ச ராசி'),fall_sign:astText('Debilitation sign','நீச ராசி'),moolatrikona_portion:astText('Moolatrikona portion','மூலத்திரிகோணப் பகுதி')}[k])).filter(Boolean).join(' · '):astText('Dignity not supplied','ஆட்சி / உச்சம் / நீசம் அளிக்கப்படவில்லை');
 const pairs=[
  [astText('Sign / degree','ராசி / பாகை'),`${astSign(p.sign)} · ${(p.longitude%30).toFixed(5)}°`],
  [astText('Rasi house / Sripati house','ராசிப் பாவம் / ஸ்ரீபதி பாவம்'),`${p.whole_sign_house_from_ascendant} / ${p.sripati_degree_house?.house??'—'}${p.sripati_degree_house?.at_sandhi?' · '+astText('Sandhi','சந்தி'):''}`],
  [astText('Owned houses','அதிபதியான பாவங்கள்'),(f?.rules_owned||[]).join(', ')||'—'],
  [astText('Sign condition / motion','ராசி நிலை / இயக்கம்'),conditions+' · '+(p.retrograde?astText('Retrograde','வக்கிரம்'):astText('Direct','நேர் இயக்கம்'))],
  [astText('Aspects to houses (whole-sign)','பார்வை பெறும் பாவங்கள் (ராசி முறை)'),(f?.aspects||[]).map(a=>a.target_house_from_reference).join(', ')||astText('Not supplied','அளிக்கப்படவில்லை')],
  [astText('Strength range (rupas)','பல வரம்பு (ரூபா)'),strength?RUPA(strength.total_rupa_interval).replace(' to ',interfaceLanguage==='ta'?' முதல் ':' to '):astText('Not supplied','அளிக்கப்படவில்லை')]
 ];
 return `<article class="inspection-planet${compact?' inspection-compact':''}" data-planet="${escape(name)}"><h4>${escape(astPlanet(name))}</h4><dl>${pairs.map(([l,v])=>`<div><dt>${escape(l)}</dt><dd>${escape(v)}</dd></div>`).join('')}</dl>${!compact?`<details><summary>${astText('Evidence references','ஆதாரக் குறிப்புகள்')}</summary><p>${escape(source(f?.sources?.lordship))}</p><p>${escape(source(p.sripati_degree_house?.source))}</p><p>${escape(source(report.shadbala_working_profile?.source))}</p></details>`:''}</article>`;
}
function astrologerPanel(report,birth){
 const s=inspectionState,timelines=report.timing_conditional?.timelines||{};
 const label=t=>`${astText(t.balance_reading==='moon_time_in_nakshatra_bj'?'Moon crossing time':'Longitude balance',t.balance_reading==='moon_time_in_nakshatra_bj'?'சந்திரன் கடக்கும் நேரம்':'கோண இருப்பு')} · ${t.year_length_days} ${astText('day year','நாள் ஆண்டு')}`;
 const timeline=timelines[s.profile],active=activeInspectionPeriod(timeline,s.at+'Z');
 const periodRow=(title,p)=>`<div class="inspection-period-row"><strong>${title}: ${escape(astPlanet(p.lord))}</strong><span>${escape(localStamp(p.start,birth.timezone))} → ${escape(localStamp(p.end,birth.timezone))}</span></div>`;
 const p=report.natal_chart.placements[s.planet]||Object.values(report.natal_chart.placements)[0];
 const placement=p.whole_sign_house_from_ascendant,count=houseDistance(s.house,placement);
 const path=Array.from({length:count},(_,i)=>(s.house+i-1)%12+1);
 return `<section id="astrologer-panel" data-private ${s.view!=='astro'?'hidden':''} aria-labelledby="astrologer-title"><h2 id="astrologer-title">${astText('Astrologer view','ஜோதிடர் பார்வை')}</h2><p class="inspection-intro">${astText('Inspect the arithmetic, not a new prediction. This view does not change the engine, the plain reading or saved birth inputs.','இது கணக்கைப் பார்ப்பதற்கான பகுதி; புதிய கணிப்பு அல்ல. கணக்கீட்டு இயந்திரம், எளிய வாசிப்பு, சேமித்த பிறப்பு விவரங்கள் மாறாது.')}</p>
 <section class="inspection-block"><h3>${astText('Viewing profile','பார்வைக்கான கணக்கு முறை')}</h3><label>${astText('Choose a timing profile','காலக் கணக்கு முறையைத் தேர்ந்தெடுங்கள்')}<select id="inspection-profile"><option value="">${astText('Choose explicitly; no default is selected','நீங்களே தேர்ந்தெடுங்கள்; இயல்புநிலை இல்லை')}</option>${Object.entries(timelines).map(([k,t])=>`<option value="${escape(k)}" ${s.profile===k?'selected':''}>${escape(label(t))}</option>`).join('')}</select></label><label>${astText('Inspection instant (UTC)','பார்க்கும் நேரம் (UTC)')}<input id="inspection-at" type="datetime-local" step="1" value="${escape(s.at)}"></label><p class="inspection-banner">${timeline?escape(label(timeline)):astText('No viewing profile selected.','பார்வை முறை தேர்ந்தெடுக்கப்படவில்லை.')} ${astText('Display choice only. No historical convention or complete strength has been selected by the engine.','இது காட்சிக்கான தேர்வு மட்டும். இயந்திரம் வரலாற்றுக் கால முறையையோ முழுப் பலக் கணக்கையோ தேர்ந்தெடுக்கவில்லை.')}</p><p class="help">${astText('Boundaries below use the birth timezone:','கீழுள்ள எல்லைகள் பிறந்த இடத்தின் நேர மண்டலத்தில்:')} ${escape(birth.timezone)}. ${astText('Start inclusive; end exclusive. Rounded life themes are separate.','தொடக்க நேரம் உட்படும்; முடிவு நேரம் உட்படாது. தோராயமான வாழ்க்கை வாசிப்பு தனியாக உள்ளது.')}</p>
 <h3>${astText('Active periods in this viewing profile','இந்த முறையில் நடக்கும் திசை - புத்தி')}</h3><div id="inspection-active">${!timeline?`<p>${astText('Choose a profile to inspect its active periods.','நடக்கும் திசை - புத்தியைப் பார்க்க ஒரு முறையைத் தேர்ந்தெடுங்கள்.')}</p>`:!active?`<p>${astText('No active period is supplied for this instant. Check the instant and the available timeline range.','இந்த நேரத்திற்கான காலப்பகுதி அளிக்கப்படவில்லை. நேரத்தையும் கணக்கின் கால வரம்பையும் சரிபார்க்கவும்.')}</p>`:periodRow(astText('Dasha','திசை'),active.maha)+(active.bhukti?periodRow(astText('Bhukti','புத்தி'),active.bhukti):`<p>${astText('Bhukti unavailable','புத்தி கிடைக்கவில்லை')}</p>`)+`<div class="inspection-lords">${[...new Set([active.maha.lord,active.bhukti?.lord].filter(Boolean))].map(n=>inspectionPlanetCard(n,report,true)).join('')}</div>`}</div><p class="help">${astText('Antara is not displayed. These date boundaries do not establish an event or predictive accuracy.','அந்தரம் காட்டப்படவில்லை. இந்தக் கால எல்லைகள் நிகழ்வையோ கணிப்புத் துல்லியத்தையோ உறுதிப்படுத்தாது.')}</p></section>
 <section class="inspection-block"><h3>${astText('Count from a reference house','ஒரு பாவத்திலிருந்து எண்ணுங்கள்')}</h3><div class="inspection-controls"><label>${astText('Reference house','தொடக்கப் பாவம்')}<select id="inspection-house">${Array.from({length:12},(_,i)=>`<option value="${i+1}" ${s.house===i+1?'selected':''}>${i+1}</option>`).join('')}</select></label><label>${astText('Planet placement','கிரக இருப்பிடம்')}<select id="inspection-planet">${Object.keys(report.natal_chart.placements).map(n=>`<option value="${n}" ${s.planet===n?'selected':''}>${escape(astPlanet(n))}</option>`).join('')}</select></label></div><p class="inspection-count" id="inspection-count">${astText('Reference','தொடக்கம்')} ${s.house} → ${astText('placement','இருப்பிடம்')} ${placement} = <strong>${count}</strong> ${astText('houses, counting inclusively','பாவங்கள், தொடக்கத்தையும் எண்ணி')}</p><div class="inspection-path" aria-label="${astText('Inclusive house counting path','தொடக்கத்துடன் எண்ணும் பாவ வரிசை')}">${path.map((h,i)=>`<span><b>${h}</b><small>${i+1}</small></span>`).join('')}</div><p class="help">${astText('Whole-sign houses from lagna only. Formula: ((placement − reference + 12) mod 12) + 1. Each small number is the count, not a strength score.','லக்னத்திலிருந்து ராசிப் பாவங்கள் மட்டும். சூத்திரம்: ((இருப்பிடம் − தொடக்கம் + 12) mod 12) + 1. சிறிய எண் எண்ணிக்கையே; பல மதிப்பெண் அல்ல.')}</p><p class="inspection-banner">${astText('Sixth or eighth is a distance, not a harm verdict. The video rule is unvalidated. No family, health or lifespan prediction is added.','ஆறு அல்லது எட்டு என்பது இடைவெளி மட்டுமே; தீமைத் தீர்ப்பு அல்ல. காணொளி விதி சோதிக்கப்படவில்லை. குடும்பம், உடல்நலம், ஆயுள் பற்றிய கணிப்பு சேர்க்கப்படவில்லை.')}</p></section>
 <section class="inspection-block"><h3>${astText('Planet inspection','கிரக ஆய்வு')}</h3><p class="help">${astText('Whole-sign and Sripati are different models. Ranges are partial evidence, not final strength scores. Dignity flags are not supplied by this public report and are left unavailable rather than inferred.','ராசி, ஸ்ரீபதி இரண்டும் வெவ்வேறு முறைகள். வரம்புகள் பகுதி ஆதாரங்களே; இறுதிப் பல மதிப்பெண்கள் அல்ல. பொதுவான அறிக்கையில் ஆட்சி / உச்சம் / நீசம் அளிக்கப்படாததால் ஊகிக்காமல் கிடைக்கவில்லை எனக் காட்டப்படுகிறது.')}</p><div class="inspection-grid">${Object.keys(report.natal_chart.placements).map(n=>inspectionPlanetCard(n,report)).join('')}</div></section></section>`;
}
function inspectionSwitch(){return `<div class="inspection-switch" data-private role="group" aria-label="${astText('Reading view','வாசிப்புப் பார்வை')}"><button type="button" data-inspection-view="plain" aria-pressed="${inspectionState.view==='plain'}">${astText('Plain view','எளிய பார்வை')}</button><button type="button" data-inspection-view="astro" aria-pressed="${inspectionState.view==='astro'}">${astText('Astrologer view','ஜோதிடர் பார்வை')}</button></div>`;}
function refreshInspection(){
 if(!window.__lastReport)return;
 const old=document.querySelector('#astrologer-panel');if(old)old.outerHTML=astrologerPanel(window.__lastReport,window.__lastBirth);
 const plain=document.querySelector('#plain-reading');if(plain)plain.hidden=inspectionState.view!=='plain';
 document.querySelectorAll('[data-inspection-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.inspectionView===inspectionState.view)));
}
document.addEventListener('click',e=>{const b=e.target.closest('[data-inspection-view]');if(b){inspectionState.view=b.dataset.inspectionView;refreshInspection();}});
document.addEventListener('change',e=>{const fields={'inspection-profile':'profile','inspection-at':'at','inspection-house':'house','inspection-planet':'planet'};const key=fields[e.target.id];if(key){inspectionState[key]=key==='house'?Number(e.target.value):e.target.value;refreshInspection();document.getElementById(e.target.id)?.focus();}});
