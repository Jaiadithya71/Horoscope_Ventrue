// Admin-gated visit counts. Auth: Authorization: Bearer <STATS_KEY> header only.
// Never accept the key as a query parameter - URLs leak into history, logs and referrers.
// Counts are page-load requests, not unique people: repeat opens count again.
// list() pages are capped so a stats view has a bounded Blob operation cost.
const DAY_MS = 86400000;
const MAX_PAGES = 20;

async function countInto(prefix, field, campaigns, withDays) {
  const { list } = await import('@vercel/blob');
  let total = 0, cursor, pages = 0, truncated = false;
  do {
    const r = await list({ prefix, cursor, limit: 1000 });
    pages++;
    for (const bl of r.blobs) {
      const m = bl.pathname.match(/^[a-z-]+\/([a-z0-9-]+)\/(\d+)-/);
      if (!m) continue;
      const c = m[1], ts = Number(m[2]);
      const slot = (campaigns[c] ||= { loads: 0, botLoads: 0, first: ts, last: ts, days: {} });
      slot[field]++;
      slot.first = Math.min(slot.first, ts);
      slot.last = Math.max(slot.last, ts);
      if (withDays) {
        const day = new Date(ts).toISOString().slice(0, 10);
        slot.days[day] = (slot.days[day] || 0) + 1;
      }
      total++;
    }
    cursor = r.hasMore ? r.cursor : undefined;
    if (cursor && pages >= MAX_PAGES) { truncated = true; cursor = undefined; }
  } while (cursor);
  return { total, truncated };
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const auth = String(req.headers['authorization'] || '');
  if (!process.env.STATS_KEY || auth !== 'Bearer ' + process.env.STATS_KEY) {
    return res.status(401).json({ error: 'unauthorized' });
  }
  try {
    const campaigns = {};
    const a = await countInto('visits/', 'loads', campaigns, true);
    const b = await countInto('visits-bot/', 'botLoads', campaigns, false);
    const t = await countInto('visits-test/', 'probes', {}, false);
    const cutoff = Date.now() - 31 * DAY_MS;
    for (const slot of Object.values(campaigns)) {
      for (const d of Object.keys(slot.days)) if (new Date(d).getTime() < cutoff) delete slot.days[d];
    }
    return res.status(200).json({
      ok: true,
      campaigns,
      testProbes: t.total,
      truncated: a.truncated || b.truncated || t.truncated,
      generatedAt: new Date().toISOString(),
      note: 'loads are page-load requests, not unique people or link taps; repeat opens count again. botLoads are likely scripted loads, kept out of loads.',
    });
  } catch (e) {
    return res.status(500).json({ error: 'stats failed', message: String(e && e.message) });
  }
};
