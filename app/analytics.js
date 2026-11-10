/* Page-view attribution only: no form fields, free text, queries or hashes. */
window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
window.va('beforeSend', function (event) {
  try {
    var u = new URL(event.url, location.origin);
    var p = u.pathname;
    var selections = (window.HOROSCOPE_REELS || []).map(function (r) { return '/from/' + r.slug; });
    selections.push('/from/unknown');
    if (['/', '/chart', '/weekly', '/stats', '/reels'].indexOf(p) < 0 && selections.indexOf(p) < 0 && !/^\/r\/[a-z0-9][a-z0-9-]{2,40}$/.test(p)) p = '/other';
    event.url = u.origin + p;
  } catch (e) { return null; } // Never pass an unparseable address through unchanged.
  return event;
});
