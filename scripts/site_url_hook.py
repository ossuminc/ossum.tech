"""Set ``site_url`` from the environment at build time.

Why this exists
---------------
``site_url`` is what MkDocs writes into ``sitemap.xml`` and the canonical link
tag. It is a static string in ``mkdocs.yml``, but the real URL of a build is
only known at deploy time, because ``mike`` puts each build under
``/<prefix>/<version>/``.

Before this hook, ``site_url`` was ``https://ossum.tech/`` for every build, so
the sitemap inside ``/latest/`` advertised unversioned root URLs -- which no
longer resolve directly. Every URL a crawler took from the sitemap was a soft
404, and ``/latest/sitemap.xml`` and ``/next/sitemap.xml`` claimed the same
canonical URLs as each other.

Usage
-----
The publishing workflow exports ``DOCS_SITE_URL`` per deploy, e.g.::

    DOCS_SITE_URL=https://ossum.tech/riddl/2.0/

When the variable is absent -- a local ``mkdocs serve`` or ``mkdocs build`` --
the value in the config is left alone, so local builds behave as before.
"""

from __future__ import annotations

import logging
import os

log = logging.getLogger("mkdocs.hooks.site_url")


def on_config(config, **kwargs):
    url = os.environ.get("DOCS_SITE_URL", "").strip()
    if not url:
        return config

    # MkDocs requires a trailing slash for correct relative-URL arithmetic.
    if not url.endswith("/"):
        url += "/"

    log.info("site_url overridden from DOCS_SITE_URL: %s", url)
    config.site_url = url
    return config
