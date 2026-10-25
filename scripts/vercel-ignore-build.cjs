// Vercel: exit 0 skips a build; exit 1 builds. Unknown history fails open.
const {execFileSync} = require('node:child_process');
const before = process.env.VERCEL_GIT_PREVIOUS_SHA;
if (!before) process.exit(1);
try {
  const files = execFileSync('git', ['diff', '--name-only', '-z', before, 'HEAD'], {encoding:'utf8'}).split('\0').filter(Boolean);
  const archivalOnly = files.length > 0 && files.every(p => /^(docs|pipeline|extracted|benchmarks|profiles)\//.test(p) || /^(README\.md|books\.json)$/.test(p));
  console.log(archivalOnly ? 'Archive/research-only change: keep current app deployment.' : 'Runtime/configuration change or empty diff: build.');
  process.exit(archivalOnly ? 0 : 1);
} catch {
  console.log('Previous deployment history unavailable: build safely.');
  process.exit(1);
}
