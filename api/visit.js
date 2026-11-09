// Count page loads that arrive from a shared link (?from=<slug>).
// Stores only {ts, c} per event - no IP, no user-agent, no cookie, no birth details.
// Likely bots (missing/scripted UA) go to a separate prefix; test-* slugs go to a probe prefix.
// Only slugs listed in CAMPAIGN_SLUGS (plus test-*) are stored; anything else is acknowledged
// without a store write, so unknown ?from= values cannot spend Blob operations.
const SLUG = /^[a-z0-9][a-z0-9-]{2,40}$/;
const BOT = /bot|crawler|spider|slurp|curl|wget|python-requests|headless|lighthouse|pingdom|monitor|preview/i;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  // Browser same-site beacons carry Sec-Fetch-Site: same-origin/same-site/none.
  // A present cross-site value means a cross-origin browser POST - refuse it.
  const sfs = req.headers['sec-fetch-site'];
  if (sfs && !['same-origin', 'same-site', 'none'].includes(String(sfs))) {
    return res.status(403).json({ error: 'forbidden' });
  }
  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = null; } }
  if (!b || typeof b !== 'object') return res.status(400).json({ error: 'bad body' });
  const c = String(b.c || '');
  if (!SLUG.test(c)) return res.status(400).json({ error: 'bad campaign' });
  const allowed = (process.env.CAMPAIGN_SLUGS || '').split(',').map(s => s.trim()).filter(Boolean);
  const isTest = c.startsWith('test-');
  if (!isTest && !allowed.includes(c)) {
    // Known shape, unknown campaign: fine for the caller, but do not spend a store op on it.
    return res.status(200).json({ ok: true, counted: false });
  }
  const ua = String(req.headers['user-agent'] || '');
  const prefix = isTest ? 'visits-test/' : (!ua || BOT.test(ua)) ? 'visits-bot/' : 'visits/';
  const ts = Date.now();
  const rand = Math.random().toString(36).slice(2, 10);
  try {
    const { put } = await import('@vercel/blob');
    await put(`${prefix}${c}/${ts}-${rand}.json`, JSON.stringify({ ts, c }), {
      access: 'private',
      contentType: 'application/json',
      addRandomSuffix: false,
    });
    return res.status(200).json({ ok: true, counted: true });
  } catch (e) {
    return res.status(500).json({ error: 'store failed' });
  }
};
