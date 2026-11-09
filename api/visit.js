// Count page loads that arrive from a shared link (?from=<slug>).
// Stores only {ts, c} per event - no IP, no user-agent, no cookie, no birth details.
// Likely bots (missing/scripted UA) go to a separate prefix; test-* slugs go to a probe prefix.
const SLUG = /^[a-z0-9][a-z0-9-]{2,40}$/;
const BOT = /bot|crawler|spider|slurp|curl|wget|python-requests|headless|lighthouse|pingdom|monitor|preview/i;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = null; } }
  if (!b || typeof b !== 'object') return res.status(400).json({ error: 'bad body' });
  const c = String(b.c || '');
  if (!SLUG.test(c)) return res.status(400).json({ error: 'bad campaign' });
  const ua = String(req.headers['user-agent'] || '');
  const prefix = c.startsWith('test-') ? 'visits-test/' : (!ua || BOT.test(ua)) ? 'visits-bot/' : 'visits/';
  const ts = Date.now();
  const rand = Math.random().toString(36).slice(2, 10);
  try {
    const { put } = await import('@vercel/blob');
    await put(`${prefix}${c}/${ts}-${rand}.json`, JSON.stringify({ ts, c }), {
      access: 'private',
      contentType: 'application/json',
      addRandomSuffix: false,
    });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(500).json({ error: 'store failed' });
  }
};
