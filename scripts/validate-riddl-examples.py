#!/usr/bin/env python3
"""Validate ```riddl code fences in documentation against a real riddlc.

Most fences are FRAGMENTS -- a `context` with no enclosing `domain`, an
`entity` with no enclosing context -- so they cannot be validated as written.
Each fence therefore declares how to make it whole, via an HTML comment
immediately above it. HTML comments do not render, so this is invisible to
readers.

    <!-- riddl: standalone -->        a complete model; validate as-is (default)
    <!-- riddl: in-domain -->         wrap in `domain Example is { ... }`
    <!-- riddl: in-context -->        wrap in a domain AND a context
    <!-- riddl: in-entity -->         wrap in a domain, context AND entity
    <!-- riddl: in-handler -->        wrap deep enough to be inside an on-clause
    <!-- riddl: in-clauses -->        wrap in a handler (for `on ...` clause fragments)
    <!-- riddl: in-usecase -->        wrap in an epic + use case (for interaction steps)
    <!-- riddl: in-epic -->           wrap in an epic (for a whole `case`)
    <!-- riddl: in-epic-story -->     give each bare user story an epic of its own
    <!-- riddl: in-app-context --> wrap in an `application` context (for groups)
    <!-- riddl: in-application -->    as in-handler, but an `application` context (for `put`)
    <!-- riddl: in-app-clauses -->    as in-clauses, but an `application` handler
    <!-- riddl: in-function -->       wrap in a function body (for `return`)
    <!-- riddl: in-record -->         wrap in a record (for a bare field declaration)
    <!-- riddl: skip -->              not RIDDL, or deliberately invalid
    <!-- riddl: skip reason=... -->   same, with the reason recorded

A page may also declare a PRELUDE: definitions that fragments reference but
do not show. It is injected into the wrapper alongside the fence body, at
CONTEXT level.

    <!-- riddl-prelude
    record Thing is { a is String }
    -->

Domain-level vocabulary is declared separately, and is read ONLY by
in-domain. The two cannot be one block: a `user` is legal only in a domain,
a `record` only in a context.

    <!-- riddl-domain-prelude
    user Customer is "a shopper"
    -->

A fence that DEFINES a name the prelude also supplies collides with it --
same context, duplicate content names. Such a fence names what it owns:

    <!-- riddl: in-context no-prelude=Cart -->
    <!-- riddl: in-context no-prelude=Cart,Order -->

Only those entries are withheld; the rest of the page vocabulary still
reaches the fence. A bare `no-prelude` withholds everything, which is
rarely what you want -- a fence that defines `Cart` usually still needs the
`CartItem` and `Money` around it, and dropping the lot just trades one
error for a pile of unresolved paths.

Usage:
    scripts/validate-riddl-examples.py <riddlc> <file.md> [file.md ...]

Exit status is non-zero if any fence fails to validate, so this is usable as
a gate -- unlike check-riddl-blocks.py, which is advisory.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE = re.compile(
    r"^(?P<indent>[ \t]*)```+riddl[^\n]*\n(?P<body>.*?)^(?P=indent)```+",
    re.MULTILINE | re.DOTALL,
)
DIRECTIVE = re.compile(r"<!--\s*riddl:\s*(?P<what>[a-z-]+)(?P<rest>[^>]*)-->", re.IGNORECASE)
PRELUDE = re.compile(r"<!--\s*riddl-prelude\s*\n(?P<body>.*?)-->", re.DOTALL | re.IGNORECASE)
# Domain-level vocabulary is a SEPARATE declaration, not the same prelude at a
# different depth: a `user` is legal only in a domain and a `record` only in a
# context, so one block cannot serve both. in-domain reads only this one.
DOMAIN_PRELUDE = re.compile(
    r"<!--\s*riddl-domain-prelude\s*\n(?P<body>.*?)-->", re.DOTALL | re.IGNORECASE
)
NO_PRELUDE = re.compile(r"no-prelude(?:=(?P<names>[A-Za-z0-9_,]+))?")
# The head of a top-level prelude entry: a keyword and the name it defines.
PRELUDE_ENTRY = re.compile(
    r"^\s*(?:entity|context|type|record|command|event|query|result|outlet|inlet"
    r"|function|repository|projector|saga|adaptor|streamlet|source|sink|flow"
    r"|merge|split|router|connector|constant|invariant|handler)\s+(?P<name>\w+)\b"
)


def strip_from_prelude(prelude: str, names: set[str]) -> str:
    """Drop the named top-level definitions from a prelude.

    A fence that DEFINES `Cart` must not also receive the prelude's `Cart`,
    or the two collide as duplicate content names -- but it still needs the
    rest of the page vocabulary, so dropping the whole prelude trades one
    error for a pile of unresolved paths. Entries are tracked by brace depth
    so a multi-line definition is removed whole.
    """
    out, depth, dropping = [], 0, False
    for line in prelude.split("\n"):
        if depth == 0:
            m = PRELUDE_ENTRY.match(line)
            dropping = bool(m and m.group("name") in names)
        if not dropping:
            out.append(line)
        depth += line.count("{") - line.count("}")
        if depth <= 0:
            depth, dropping = 0, False
    return "\n".join(out)


def directive_for(text: str, fence_start: int) -> tuple[str, str]:
    """The directive in the comment closest above this fence, if any."""
    head = text[:fence_start]
    # Only look at the last few lines, so a directive cannot leak across prose.
    tail = "\n".join(head.rstrip("\n").split("\n")[-4:])
    m = None
    for m in DIRECTIVE.finditer(tail):
        pass  # take the last one
    if not m:
        return "standalone", ""
    return m.group("what").lower(), m.group("rest").strip()


def wrap(kind: str, body: str, prelude: str, domain_prelude: str = "") -> str:
    """Nest a fragment deep enough to be a whole model.

    The prelude always lands at CONTEXT level, whatever the depth, because
    that is where a page's shared vocabulary belongs -- a fragment nested in
    a handler still needs to see the types the page defined around it.
    """
    body = body.rstrip()

    def ind(txt: str, n: int) -> str:
        pad = " " * n
        return "\n".join(pad + ln if ln.strip() else ln for ln in txt.split("\n"))

    pre = ind(prelude.strip(), 4) if prelude.strip() else ""
    # An author may only be DEFINED in a Module or Domain, so a context-level
    # page prelude cannot supply one -- yet `by author X` appears on many
    # pages. Every wrapper therefore defines one at domain level.
    AUTHOR = '  author Reid is { name is "Reid Spencer" email is "reid@ossuminc.com" }\n'

    if kind == "in-function":
        # `return` is legal only in a function body. A `Tax.Compute` is
        # supplied because `return call function ...` is the form the docs
        # use; it must resolve AND agree with the enclosing function's return
        # type, hence `returns Tax.TaxIn`. Tax is a sibling CONTEXT, not a
        # nested function: rc.9-54 fails internally on a call to a nested
        # function by dotted path, emitting a bare `[severe] empty(1:1->1)`.
        # TaxIn has exactly one field because the call passes one argument.
        return (
            "domain Example is {\n" + AUTHOR +
            "  context Tax is {\n"
            "    record TaxIn is { subtotal is Natural }\n"
            "    function Compute is { requires TaxIn returns TaxIn ??? }\n"
            "  }\n"
            "  context Example is {\n" + pre + "\n"
            "    record FnInput is { note is String, subtotal is Natural }\n"
            "    function ExampleFunction is {\n"
            "      requires FnInput returns Tax.TaxIn\n"
            + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-app-context":
        # Groups, inputs and outputs are context-level definitions, and RIDDL
        # 2.0 only allows them in a context with the `application` intention.
        # in-application is NOT the same thing: it wraps in an on-clause, so a
        # group lands where only statements are legal.
        return (
            "domain Example is {\n" + AUTHOR +
            "  user Shopper is \"a customer using the store\"\n"
            "  application context Example is {\n" + pre + "\n"
            + ind(body, 4) + "\n  }\n}\n"
        )
    if kind == "in-application":
        # `put ... to output` is legal only in an application/context handler.
        return (
            "domain Example is {\n" + AUTHOR + "  application context Example is {\n" + pre + "\n"
            "    record ExampleOrder is { confirmationNumber is String }\n"
            "    record ExampleData is { note is String }\n"
            "    command ExampleCommand is { note is String, order is ExampleOrder }\n"
            "    page ExamplePage is {\n"
            # `shows type X` needs a resolvable Type: a predefined name like
            # String is not in the symbol table here.
            "      document ExampleOutput shows type ExampleData\n"
            "      document ConfirmationPanel shows type ExampleOrder\n"
            "      form ExampleInput accepts type ExampleData\n"
            "    }\n"
            "    handler ExampleHandler is {\n"
            "      on command ExampleCommand {\n"
            + ind(body, 8) + "\n"
            "      }\n    }\n  }\n}\n"
        )
    if kind == "in-app-clauses":
        # An `on ...` clause in an APPLICATION handler. in-clauses is NOT the
        # same thing: it builds an ENTITY handler, where `put` is not in the
        # statement set and an output cannot exist -- outputs live in a page
        # or group, which only an application context may hold.
        # `order` is a field of the handled query because `put order.field`
        # resolves its root against the handled message.
        return (
            "domain Example is {\n" + AUTHOR +
            "  application context Example is {\n" + pre + "\n"
            "    record ExampleOrder is { confirmationNumber is String }\n"
            "    query GetReceipt is { order is ExampleOrder }\n"
            "    page ExamplePage is {\n"
            "      document Receipt shows type ExampleOrder\n"
            "    }\n"
            "    handler ExampleHandler is {\n"
            + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-epic-story":
        # A bare user story, or a MENU of them showing alternative spellings.
        # An epic admits exactly one opening story -- `epic_body = user_story
        # {epic_definitions}`, and a second story is not an epic_definition --
        # so each story here gets an epic of its own. A line beginning `user`
        # starts a new story; anything else continues the current one, which
        # is how a story with its `so that` on the next line stays intact.
        stories: list[list[str]] = []
        for ln in body.split("\n"):
            if ln.strip().startswith("user ") or not stories:
                stories.append([ln])
            else:
                stories[-1].append(ln)
        epics = ""
        for n, story in enumerate(stories):
            text = "\n".join(story).strip()
            if not text:
                continue
            epics += (
                f"  epic ExampleEpic{n} is {{\n" + ind(text, 4) + "\n"
                "    case ExampleCase is {\n"
                "      user Customer wants to \"do a thing\" so that \"a benefit follows\"\n"
                "      ???\n"
                "    }\n  }\n"
            )
        return (
            "domain Example is {\n" + AUTHOR +
            "  user Customer is \"a customer\"\n"
            "  user Auditor is \"an auditor\"\n"
            "  user Guest is \"a guest\"\n"
            + epics + "}\n"
        )
    if kind == "in-epic":
        # A user story, or a whole `case`, lives in an epic -- which is a
        # DOMAIN-level definition, so no context wrapper will hold it. The
        # epic's own opening user story is mandatory (epic_body = user_story
        # {epic_definitions}), so the wrapper supplies one before the body.
        # The context carries the `application` intention so that a page
        # prelude may define the pages, forms and documents an interaction
        # step refers to -- `group` is a context_definition, but RIDDL 2.0
        # admits it only in an application context.
        return (
            "domain Example is {\n" + AUTHOR +
            "  user Customer is \"a customer\"\n"
            "  application context Example is {\n" + pre + "\n"
            "    entity Cart is { ??? }\n"
            "  }\n"
            "  epic ExampleEpic is {\n"
            "    user Customer wants to \"do a thing\" so that \"a benefit follows\"\n"
            + ind(body, 4) + "\n"
            "  }\n}\n"
        )
    if kind == "in-record":
        # A bare field declaration, e.g. `items is many Item`.
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    record ExampleRecord is {\n" + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-usecase":
        # An interaction step lives in a use case, inside an epic, inside a
        # domain -- three levels no other wrapper provides.
        return (
            "domain Example is {\n" + AUTHOR +
            "  user Customer is \"a customer\"\n"
            "  context Example is {\n" + pre + "\n"
            "    record ExampleData is { note is String }\n"
            "    entity Cart is { ??? }\n"
            "  }\n"
            "  epic ExampleEpic is {\n"
            "    user Customer wants to \"do a thing\" so that \"a benefit follows\"\n"
            "    case ExampleCase is {\n"
            "      user Customer wants to \"do a thing\" so that \"a benefit follows\"\n"
            + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-clauses":
        # An `on ...` clause fragment: give it a handler to sit in.
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    record ExampleData is { note is String, balance is Natural }\n"
            "    command ExampleCommand is { note is String, amount is Natural }\n"
            "    entity ExampleEntity is {\n"
            "      state ExampleState of record ExampleData is {\n"
            "        handler ExampleHandler is {\n"
            + ind(body, 10) + "\n"
            "        }\n      }\n    }\n  }\n}\n"
        )
    if kind == "in-handler":
        # Statement-level fragment: give it an on-clause to live in.
        # The handled command carries a nested `cart` record so that the
        # dotted references docs actually write -- `cart.itemCount` -- have
        # something to resolve against. Fields are only ever ADDED here: an
        # extra field cannot break a fence that ignores it, but a renamed one
        # would break every fence that used the old name.
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    type ExampleLimit is Natural\n"
            "    record ExampleLine is { sku is String, quantity is Natural }\n"
            "    record ExampleOrder is { id is String, number is String,\n"
            "      total is Natural, status is String, isPaid is Boolean,\n"
            "      isCancelled is Boolean, isRefunded is Boolean,\n"
            "      confirmationNumber is String, items is many ExampleLine }\n"
            # The state record: `foreach ... in field X` takes a DIRECT field of
            # the state, handled message or function input -- a dotted path such
            # as `order.lines` is rejected -- so the iterable lives here.
            "    record ExampleData is { note is String, itemCount is Natural,\n"
            "      id is String, total is Natural, balance is Natural,\n"
            "      lines is many ExampleLine }\n"
            "    command ExampleCommand is { note is String, cart is ExampleData,\n"
            "      order is ExampleOrder, orderId is String, amount is Natural,\n"
            "      limits is ExampleLimit }\n"
            "    entity ExampleEntity is {\n"
            "      invariant BalanceNonNegative is \"the balance must not go negative\"\n"
            "      invariant UnderLimit requires ExampleLimit is \"must stay under the limit\"\n"
            "      state ExampleState of record ExampleData is {\n"
            "        handler ExampleHandler is {\n"
            "          on command ExampleCommand {\n"
            + ind(body, 12) + "\n"
            "          }\n        }\n      }\n    }\n  }\n}\n"
        )
    if kind == "in-entity":
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            "    entity ExampleEntity is {\n" + ind(body, 6) + "\n"
            "    }\n  }\n}\n"
        )
    if kind == "in-context":
        return (
            "domain Example is {\n" + AUTHOR + "  context Example is {\n" + pre + "\n"
            + ind(body, 4) + "\n  }\n}\n"
        )
    if kind == "in-domain":
        # Reads riddl-domain-prelude, NOT riddl-prelude: what an in-domain
        # fence needs supplied is domain-level vocabulary -- a `user` an
        # epic's story refers to -- and the ordinary prelude holds
        # context-level definitions that are illegal at this depth.
        dom_pre = ind(domain_prelude.strip(), 2) + "\n" if domain_prelude.strip() else ""
        return "domain Example is {\n" + AUTHOR + dom_pre + ind(body, 2) + "\n}\n"
    # standalone: complete by definition, so the prelude is NOT injected --
    # a page prelude holds context-level definitions, and those are illegal at
    # root, which would break the very fences that need no help.
    return body + "\n"


def validate(riddlc: str, source: str) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".riddl", delete=False) as fh:
        fh.write(source)
        path = fh.name
    try:
        proc = subprocess.run(
            [riddlc, "validate", path],
            capture_output=True, text=True, timeout=120,
        )
        out = proc.stdout + proc.stderr
        # Strip ANSI so the report is readable when redirected to a file.
        out = re.sub(r"\x1b\[[0-9;]*m", "", out)
        bad = [
            ln for ln in out.split("\n")
            if "[error]" in ln or "[severe]" in ln or "[deprecated]" in ln
        ]
        detail = "\n".join(
            ln for ln in out.split("\n")
            if any(k in ln for k in ("[error]", "[severe]", "[deprecated]"))
            or ln.startswith(("Expected", "Context:"))
        )
        return (proc.returncode == 0 and not bad), detail.strip()
    finally:
        Path(path).unlink(missing_ok=True)


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    args = [a for a in sys.argv[1:] if a != "--auto"]
    auto = "--auto" in sys.argv
    riddlc, files = args[0], args[1:]

    total = skipped = failed = 0
    for f in files:
        md = Path(f)
        text = md.read_text(encoding="utf-8")
        prelude = "\n".join(m.group("body") for m in PRELUDE.finditer(text))
        dom_prelude = "\n".join(m.group("body") for m in DOMAIN_PRELUDE.finditer(text))

        for fm in FENCE.finditer(text):
            line = text[: fm.start()].count("\n") + 1
            kind, rest = directive_for(text, fm.start())
            # A fence that defines what the prelude also supplies must not
            # receive it, or the two collide as duplicate content names.
            np = NO_PRELUDE.search(rest)
            if not np:
                fence_prelude = prelude
            elif np.group("names"):
                fence_prelude = strip_from_prelude(
                    prelude, set(np.group("names").split(","))
                )
            else:
                fence_prelude = ""
            if auto and kind == "standalone":
                kind = "auto"
            if kind == "skip":
                skipped += 1
                continue
            total += 1
            if kind == "auto":
                # Try each wrapping; a fence that fits ANY of them is a
                # fragment needing context, not a broken example. Used to
                # measure how many fences are genuinely wrong on pages that
                # do not yet carry directives.
                ok, detail = False, ""
                for attempt in ("standalone", "in-domain", "in-context", "in-entity", "in-handler", "in-app-context", "in-application", "in-app-clauses", "in-function", "in-record", "in-clauses", "in-usecase", "in-epic", "in-epic-story"):
                    ok, detail = validate(riddlc, wrap(attempt, fm.group("body"), fence_prelude, dom_prelude))
                    if ok:
                        break
            else:
                ok, detail = validate(riddlc, wrap(kind, fm.group("body"), fence_prelude, dom_prelude))
            if not ok:
                failed += 1
                print(f"\nFAIL {md}:{line}  (riddl: {kind})")
                for ln in detail.split("\n")[:8]:
                    print("    " + ln)

    # `total` counts fences ATTEMPTED, so the passing count is total - failed.
    # Reporting `total` as "validated" overstates it whenever anything failed.
    print(
        f"\n{total - failed} fence(s) validated, {skipped} skipped, "
        f"{failed} failed ({total} attempted)"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
