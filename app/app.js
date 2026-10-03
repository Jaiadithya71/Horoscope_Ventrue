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
  window.__lastReport = report;
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
  <button type="button" id="story-open" class="story-open">Read your life as a story</button>
  <nav class="secnav" aria-label="Sections"><a href="#who-title">Who you are</a><a href="#periods-title">Life by period</a><a href="#evidence">Evidence</a></nav>
  ${whoSection(report.who_you_are)}
  ${outcomeSection(report.outcome_summary)}
  ${periodsSection(report.life_periods)}
  <details class="evidence-all" id="evidence"><summary>See the evidence and calculations behind this</summary>
  ${lifeAspectReading(report.life_aspect_candidates)}
  ${lifeSections(report)}
  <h2 class="chart-structure-title">The structure of your chart</h2>
  <section class="reading">${reading.map(t => `<p>${t}</p>`).join('')}</section>
  <div class="boundary"><h3>Where this reading stops</h3><p>The career alternatives above add source-based conditional interpretation to the chart structure. They do not choose the strongest route or a profession. Selected strength, calendar timing and life outcomes remain research-gated. No complete personal forecast or predictive accuracy is established.</p><p>Chart mechanics do not establish a life outcome or reproduce a professional astrologer's judgement.</p></div>
  <details><summary>Planet placements</summary><p>Whole-sign and Sripati degree houses are separate models, not interchangeable. Rahu is the mean node. Ketu is not supplied in this engine report; no extra placement is invented.</p><div class="table-wrap"><table><thead><tr><th>Planet</th><th>Sign / degree</th><th>Whole-sign house</th><th>Sripati house</th></tr></thead><tbody>${rows}</tbody></table></div></details>
  <details><summary>Period arithmetic</summary><p>Initial lord: ${escape(periods.initial_lord)}. Remaining at birth: ${Number(periods.initial_remaining_solar_years).toFixed(3)} solar-year units.</p><p>${escape(periods.date_limit)} ${escape(periods.method_note)}</p><div class="table-wrap"><table><thead><tr><th>Lord</th><th>Start from birth<br>(solar-year units)</th><th>End from birth<br>(solar-year units)</th></tr></thead><tbody>${periodRows}</tbody></table></div><p>No current-period label or calendar date is inferred.</p></details>
  <details><summary>Source references & model</summary><p>${escape(chart.model)}</p>${unique.map(s => `<div class="source-row">${source(s)}<p>${s.verified_against_page_image ? 'Page image checked in the engine source audit.' : 'Page-image verification not recorded.'} This preview lists references only; it does not display scanned pages or authoritative interpretations.</p></div>`).join('')}<p>${escape(chart.notice)}</p></details>
  <details><summary>Inspect the engine report</summary><p>Raw evidence includes research candidates, not selected verdicts. Unknown values remain null.</p><pre>${escape(JSON.stringify(publicReport(report), null, 2))}</pre></details></details>`;
  document.querySelector('#empty').hidden = true;
  output.hidden = false;
}
form.addEventListener('submit', async e => {
  e.preventDefault(); error.hidden = true; output.hidden = true;
  document.querySelector('#empty').hidden = false;
  if (!form.elements.date.value) return fail('Choose the full date of birth: day, month and a four-digit year.');
  if (!form.elements.time.value) return fail('Choose the time of birth: hour, minute and AM or PM.');
  if (form.elements.latitude.value === '' || form.elements.longitude.value === '') {
    const ok = await findCoordinates();
    if (!ok || form.elements.latitude.value === '') return;
  }
  button.disabled = true; button.textContent = 'Calculating…'; workspace.setAttribute('aria-busy', 'true');
  const values = Object.fromEntries(new FormData(form));
  const birth = {date: values.date, time: values.time, timezone: values.timezone === '__other' ? (values.timezone_other || '').trim() : values.timezone, place: values.place,
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
  dateEcho.textContent = dt.toLocaleDateString('en-GB', {weekday:'long', day:'numeric', month:'long', year:'numeric', timeZone:'UTC'});
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
  add('Your reading', 'Your life, one card at a time', '<p>Tap Next or swipe left to go on, Back or swipe right to return. Each card is one piece: who you are, then each stretch of life, the phases inside, and every area of life. Read as themes from classical texts, not fixed events.</p>');
  if (w) {
    add('Who you are', 'How you come across', `<p>${escape(w.outer_you.text)}</p><p class="p-hl">${w.outer_you.pointers.map(k => `<span class="hl">${escape(k)}</span>`).join('')}</p>`, why(w.outer_you.rules));
    if (!w.same_sign) add('Who you are', 'Your inner nature', `<p>${escape(w.inner_you.text)}</p><p class="p-hl">${w.inner_you.pointers.map(k => `<span class="hl">${escape(k)}</span>`).join('')}</p>`, why(w.inner_you.rules));
  }
  const ps = (lp?.periods || []).filter(p => p.when !== 'past');
  const toneCls = t => ({strong: 'tone-strong', weak: 'tone-weak', mixed: 'tone-mixed'}[t] || 'tone-mixed');
  ps.forEach(p => {
    const yrs = `${p.years_about[0]} to ${p.years_about[1]}`;
    const tag = p.when === 'now' ? 'Right now' : p.when === 'next' ? 'Coming next' : 'Further ahead';
    const rulesWhy = why((p.rules || []).map(r => ({effect: r.effect, source: r.source})));
    const basis = `<details class="why"><summary>The chart basis</summary><p class="route-caveat">Ruling planet: ${escape(p.lord)}. ${escape((p.basis || []).join('; '))}.</p></details>`;
    add(tag, yrs, `<p>${chip(p.label, toneCls(p.tone))}</p><p>${escape(p.you_text || p.summary)}</p>${p.confidence === 'tentative' ? '<p class="route-caveat">The chart is less clear-cut for this stretch, so read it as a softer signal.</p>' : ''}`, rulesWhy + basis);
    if (p.depth === 'full') {
      Object.values(p.aspects || {}).forEach(a => add(`${yrs} · ${a.label}`, a.label, `<p>${chip(a.status === 'quiet' ? 'nothing specific' : a.status, 'asp-' + a.status)}</p><p>${escape(a.text)}</p>${a.guidance ? `<p class="guide">${escape(a.guidance)}</p>` : ''}`, a.items?.length ? `<details class="why"><summary>Why the chart says this</summary><ul class="cond-list">${a.items.map(i => `<li>${escape(i.effect)} <span class="route-source">${sourceLink(i.source)}</span></li>`).join('')}</ul></details>` : ''));
      p.bhuktis.forEach(b => add(`${yrs} · phase`, `${b.years_about[0]} to ${b.years_about[1]}`, `<p>${chip(b.label)}</p>${(b.phase_areas || []).length ? b.phase_areas.map(x => `<p><strong>${escape(x.label)}.</strong> ${escape(x.text)}</p><p class="guide">${escape(x.guidance)}</p>`).join('') + '<p class="route-caveat">Areas for a smaller phase are our reading, not stated by the book.</p>' : '<p>No area stands out for this phase, so the overall feel of the stretch applies.</p>'}`, `<details class="why"><summary>Why the chart says this</summary><p class="route-caveat">${escape(b.basis)}</p></details>`));
    } else {
      const chips = Object.values(p.aspects || {}).filter(a => a.status !== 'quiet').map(a => `<span class="hl">${escape(a.label)}: ${escape(a.status)}</span>`).join('');
      if (chips) cards[cards.length - 1].body += `<p class="p-hl">${chips}</p>`;
    }
  });
  add('The fine print', 'What this is, and is not', `<p>${escape(lp?.notice || '')}</p><p>These are broad themes from one classical text. They were not tested against real outcomes, and nothing here is medical, legal or financial advice.</p>`);
  return cards;
}

function openStory() {
  const report = window.__lastReport; if (!report) return;
  const cards = storyCards(report); let i = 0;
  const ov = document.createElement('div'); ov.className = 'story'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Your life as a story');
  ov.innerHTML = '<div class="story-bars"></div><button type="button" class="story-close" aria-label="Close story">×</button><div class="story-card" tabindex="0"></div><button type="button" class="story-prev" aria-label="Previous card">Back</button><button type="button" class="story-next" aria-label="Next card">Next</button><p class="story-count"></p>';
  document.body.appendChild(ov); document.body.classList.add('story-on');
  const bars = ov.querySelector('.story-bars'), card = ov.querySelector('.story-card'), count = ov.querySelector('.story-count');
  bars.innerHTML = cards.map(() => '<i></i>').join('');
  const close = () => { ov.remove(); document.body.classList.remove('story-on'); document.removeEventListener('keydown', key); document.querySelector('#story-open')?.focus(); };
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
  show(0); card.focus();
}
document.addEventListener('click', e => { if (e.target.closest('#story-open')) openStory(); });
