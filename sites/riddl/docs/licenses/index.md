---
title: "Third-Party Licenses"
description: >-
  Open-source software distributed with RIDDL, and the license notices those
  licenses require to be reproduced.
---

# Third-Party Licenses

RIDDL is Copyright © 2019-2026 Ossum Inc. and is licensed under the
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

RIDDL is built on the work of others. What follows is the complete set of
notices for the open-source software distributed with it, reproduced verbatim
because several of these licenses require exactly that — Apache-2.0 §4(d)
obliges us to carry each project's own `NOTICE` text unaltered.

!!! info "This page is version-specific"
    These notices describe the dependencies of **this** release of RIDDL. A
    different RIDDL version ships a different set, so use the version selector
    above if you are looking for another release. `riddlc info` prints the URL
    matching the binary you are running.

## Notices

```text title="THIRD-PARTY-NOTICES.txt"
--8<-- "licenses/THIRD-PARTY-NOTICES.txt"
```

## How this page stays current

The text above is included verbatim from `THIRD-PARTY-NOTICES.txt`, vendored
into this repository beside this page. It is **not** generated: the RIDDL side
maintains it by hand, alongside a matching constant in
`utils/src/main/scala/com/ossuminc/riddl/utils/ThirdPartyNotices.scala`, so it
does not update itself when RIDDL's dependencies change.

To refresh it when a new RIDDL version is documented:

```bash
cp ../riddl/THIRD-PARTY-NOTICES.txt \
   sites/riddl/docs/licenses/THIRD-PARTY-NOTICES.txt
```

A copy is used rather than a build-time fetch so that drift shows up as a diff
in review, and so the documentation build has no network dependency.
