// Admin-gated visit counts. GET /api/stats?key=<STATS_KEY>
// Counts are page-load requests, not unique people: repeat opens count again.
const DAY_MS = 86400000;

async function countInto(prefix, field, campaigns, withDays) {
  const { list } = await import('@vercel/blob');
  let total = 0, cursor;
  do {
    const r = await list({ prefix, cursor, limit: 1000 });
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
  } while (cursor);
  return total;
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!process.env.STATS_KEY || req.query.key !== process.env.STATS_KEY) {
    return res.status(401).json({ error: 'unauthorized' });
  }
  try {
    const campaigns = {};
    await countInto('visits/', 'loads', campaigns, true);
    await countInto('visits-bot/', 'botLoads', campaigns, false);
    const testProbes = await countInto('visits-test/', 'probes', {}, false);
    const cutoff = Date.now() - 31 * DAY_MS;
    for (const slot of Object.values(campaigns)) {
      for (const d of Object.keys(slot.days)) if (new Date(d).getTime() < cutoff) delete slot.days[d];
    }
    return res.status(200).json({
      ok: true,
      campaigns,
      testProbes,
      generatedAt: new Date().toISOString(),
      note: 'loads are page-load requests, not unique people or link taps; repeat opens count again. botLoads are likely scripted loads, kept out of loads.',
    });
  } catch (e) {
    return res.status(500).json({ error: 'stats failed', message: String(e && e.message) });
  }
};
