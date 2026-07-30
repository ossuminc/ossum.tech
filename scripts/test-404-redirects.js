#!/usr/bin/env node
/**
 * Verify the legacy-URL mapping in scripts/gh-pages-404.html.
 *
 * That file is the only thing keeping years of inbound links and search
 * results working across three different URL shapes, and it CANNOT be checked
 * with curl: GitHub Pages serves it with an HTTP 404 status and the rewrite
 * happens in the browser afterwards. So every request to a legacy URL looks
 * like a failure from the command line whether the redirect works or not.
 *
 * This runs the real script from the real file against a fake window.location.
 *
 *     node scripts/test-404-redirects.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const file = path.join(__dirname, 'gh-pages-404.html');
const match = fs.readFileSync(file, 'utf8').match(/<script>([\s\S]*?)<\/script>/);
if (!match) {
  console.error(`No <script> block found in ${file}`);
  process.exit(1);
}
const script = new vm.Script(match[1]);

function run(pathname) {
  let target = null;
  const window = {
    location: { pathname, search: '', hash: '', replace(u) { target = u; } },
  };
  script.runInNewContext({ window });
  return target;
}

// [requested path, expected destination]  --  null means "no redirect; show
// the not-found message", which is the correct outcome for a genuine 404.
const cases = [
  // shape 1: pre-versioning, e.g. /riddl/concepts/entity.html
  ['/riddl/concepts/entity.html',            '/riddl/latest/concepts/entity/'],
  ['/riddl/index.html',                      '/riddl/latest/'],
  ['/MCP/gemini.html',                       '/riddlg/latest/MCP/gemini/'],
  ['/OSS/authoring-riddl.html',              '/riddl/latest/OSS/authoring-riddl/'],
  ['/synapify/generation.html',              '/synapify/latest/generation/'],
  ['/about/privacy-policy.html',             '/about/privacy-policy/'],
  ['/coming-soon/index.html',                '/coming-soon/'],
  ['/riddl/tools/riddlg/installation.html',  '/riddlg/latest/installation/'],

  // shape 2: one version axis for the whole site, version segment first
  ['/latest/riddl/concepts/entity.html',     '/riddl/latest/concepts/entity/'],
  ['/next/riddl/concepts/entity.html',       '/riddl/next/concepts/entity/'],
  ['/2.0/riddl/quickstart.html',             '/riddl/2.0/quickstart/'],
  ['/1.31/riddl/quickstart.html',            '/riddl/1.31/quickstart/'],
  ['/latest/riddl/tools/riddlg/models.html', '/riddlg/latest/models/'],
  ['/latest/MCP/claude-code.html',           '/riddlg/latest/MCP/claude-code/'],
  ['/latest/synapify/index.html',            '/synapify/latest/'],
  ['/latest/about/privacy-policy.html',      '/about/privacy-policy/'],
  ['/latest/index.html',                     '/'],

  // A version segment in shape 2 was always RIDDL's. riddlg and Synapify have
  // their own numbering, so it must be dropped rather than carried across --
  // there is no Synapify 2.0.
  ['/2.0/synapify/generation.html',          '/synapify/latest/generation/'],
  ['/2.0/MCP/gemini.html',                   '/riddlg/latest/MCP/gemini/'],

  // shape 3: already current. Must NOT be rewritten -- "riddl" is both a
  // current prefix and a former top-level section, so without the loop guard
  // these would become /riddl/latest/latest/...
  ['/riddl/latest/concepts/entity/',         null],
  ['/riddl/2.0/concepts/nonexistent/',       null],
  ['/riddlg/latest/mcp-tools/',              null],
  ['/synapify/0.17/generation/',             null],

  // unknown paths fall through to the message rather than guessing
  ['/totally/unknown/thing',                 null],
  ['/favicon.ico',                           null],
];

let failed = 0;
for (const [input, expected] of cases) {
  const got = run(input);
  if (got === expected) {
    console.log(`ok    ${input}\n        -> ${got}`);
  } else {
    failed++;
    console.log(`FAIL  ${input}\n        -> ${got}   (expected ${expected})`);
  }
}
console.log(`\n${cases.length - failed}/${cases.length} passed`);
process.exit(failed ? 1 : 0);
