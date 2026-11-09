// CONTAINED: public visit counting is disabled.
// Hobby Blob usage is account-wide: an unauthenticated write endpoint here could exhaust the
// shared advanced-operations allowance and trigger a 30-day Blob lockout for every store on
// the account, including unrelated apps. Until a design without shared-quota exposure exists,
// this endpoint acknowledges every request and writes nothing. Existing records are preserved
// and remain readable through the authenticated stats endpoint.
const SLUG = /^[a-z0-9][a-z0-9-]{2,40}$/;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = null; } }
  if (!b || typeof b !== 'object') return res.status(400).json({ error: 'bad body' });
  const c = String(b.c || '');
  if (!SLUG.test(c)) return res.status(400).json({ error: 'bad campaign' });
  return res.status(200).json({ ok: true, counted: false, disabled: true });
};
