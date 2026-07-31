---
title: "Search all documentation"
description: >-
  Search across the RIDDL, riddlg and Synapify documentation at once.
---

# Search all documentation

The documentation is published as several independent sites — one per product,
each with its own versions. The search box in each site's header searches
*that* site. This page searches **all of them at once**.

<div id="pagefind-search" data-pagefind-ignore></div>

<div id="pagefind-unavailable" hidden markdown>
!!! warning "Search index unavailable"
    The cross-site search index could not be loaded. It is built after the
    documentation is published, so it may be missing for a few minutes after a
    release. Each site's own search box is unaffected — use the magnifying
    glass in the header.
</div>

<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<script
  src="/pagefind/pagefind-ui.js"
  onerror="document.getElementById('pagefind-unavailable').hidden = false"
></script>
<script>
  window.addEventListener("DOMContentLoaded", function () {
    if (typeof PagefindUI === "undefined") {
      document.getElementById("pagefind-unavailable").hidden = false;
      return;
    }
    new PagefindUI({
      element: "#pagefind-search",
      showSubResults: true,
      showImages: false,
      // The index covers each product's default version only, so a result is
      // never a stale copy of the page above it.
      resetStyles: false,
    });
  });
</script>

<style>
  /* Pagefind ships its own styling; map it onto Material's palette so the page
     does not look pasted in, and so it follows the light/dark toggle. */
  :root {
    --pagefind-ui-scale: 0.85;
    --pagefind-ui-primary: var(--md-primary-fg-color);
    --pagefind-ui-text: var(--md-typeset-color);
    --pagefind-ui-background: var(--md-default-bg-color);
    --pagefind-ui-border: var(--md-default-fg-color--lightest);
    --pagefind-ui-tag: var(--md-default-fg-color--lightest);
    --pagefind-ui-font: var(--md-text-font-family, inherit);
  }
</style>

## What is covered

| Site | Indexed |
|------|---------|
| [RIDDL](/riddl/latest/) | the current release |
| [riddlg](/riddlg/latest/) | the current release |
| [Synapify](/synapify/latest/) | the current release |
| This site | Home, About, Coming Soon |

**Older versions are deliberately not indexed.** Each product publishes several
versions, and every alias is a full copy of a version directory, so indexing
everything would return the same page three or four times. Searching here finds
the current documentation; to search a specific older release, open that
version and use its own search box.
