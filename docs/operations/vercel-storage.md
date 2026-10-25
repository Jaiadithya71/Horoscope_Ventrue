# Vercel function storage control

The 2026-10-25 baseline production deployment had five Python functions at
53.6 MB each in IAD1. The team Functions Storage project breakdown showed
7.67 GB for this project (7.74 GB team total).

Python bundles include project files unless excluded. `vercel.json` excludes
archival research, media pipelines, tests, frontend assets and development
packages from function bundles. It does not remove any source files from Git,
or change the static site's existing paths. `engine/` and all its JSON rule
data stay bundled. Root requirements remain unchanged.

`scripts/vercel-ignore-build.cjs` skips archive-only pushes by comparing the
previous deployed Git SHA with HEAD. Missing history or any runtime/config
change builds normally. A skipped build uses Vercel's exit-0 convention.
Documentation changes remain available in Git without republishing the app.

Smaller bundles only affect future deployments. Existing stored deployment
artifacts require a separate, owner-approved retention/rollback decision.

Verified production outcome for e4702a2: all five bundles are 10.7 MB each in
IAD1 (about 80% reduction). All five public API endpoints returned HTTP 200
with expected JSON; the home, weekly, studio and JavaScript assets returned
HTTP 200. The full source-tree engine suite passed 634 tests. An isolated
runtime-only tree also passed representative calls to every API adapter;
research CLI/fixture tests still require the excluded source directories in
normal development. No live user records were written during these checks.
