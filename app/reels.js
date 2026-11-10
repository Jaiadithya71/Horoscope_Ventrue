(function () {
  'use strict';
  var language = 'ta';
  try { language = localStorage.getItem('horoscope-language') === 'en' ? 'en' : 'ta'; } catch (e) {}
  var search = document.getElementById('reel-search');
  function render() {
    var query = search.value.trim().toLocaleLowerCase();
    var list = document.getElementById('reel-list');
    list.replaceChildren();
    window.HOROSCOPE_REELS.forEach(function (reel) {
      if (query && [reel.ta, reel.en, reel.detailTa, reel.detailEn].join(' ').toLocaleLowerCase().indexOf(query) < 0) return;
      var a = document.createElement('a'); a.className = 'reel-card'; a.href = '/from/' + reel.slug;
      var title = document.createElement('strong'); title.textContent = reel[language];
      var detail = document.createElement('span'); detail.className = 'detail'; detail.textContent = reel[language === 'ta' ? 'detailTa' : 'detailEn'];
      var arrow = document.createElement('span'); arrow.className = 'arrow'; arrow.textContent = '→'; arrow.setAttribute('aria-hidden', 'true');
      a.append(title, detail, arrow); list.append(a);
    });
    document.getElementById('no-matches').hidden = list.children.length !== 0;
  }
  function setLanguage(lang) {
    language = lang; document.documentElement.lang = lang;
    document.querySelectorAll('[data-ta]').forEach(function (el) { el.textContent = el.dataset[lang]; });
    document.querySelectorAll('[data-lang]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.lang === lang)); });
    search.placeholder = lang === 'ta' ? 'திருமணம், கோலம்…' : 'Marriage, kolam…';
    try { localStorage.setItem('horoscope-language', lang); } catch (e) {}
    render();
  }
  document.querySelectorAll('[data-lang]').forEach(function (button) { button.onclick = function () { setLanguage(button.dataset.lang); }; });
  search.oninput = render; setLanguage(language);
})();
