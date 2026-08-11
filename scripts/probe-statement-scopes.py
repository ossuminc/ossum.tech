#!/usr/bin/env python3
"""Probe which statements riddlc accepts in which container.

Each cell is a WHOLE model differing only in the statement under test and the
container holding it, so a rejection is attributable to that pair. Where a
statement needs a particular trigger to be legal at all (yield needs a command
declaring `yields`; reply needs a query declaring `replies`), the container
template supplies that trigger rather than the generic one -- otherwise the
probe would measure the trigger, not the statement.
"""
import subprocess, tempfile, re, sys, os

RIDDLC = "/Users/reid/Code/ossuminc/bin/riddlc"

# Shared context-level vocabulary. Deliberately rich so that no probe fails for
# want of a name to point at.
VOCAB = '''
    type Status is any of { Pending, Done }
    constant Zero is Natural = "0"
    record Line is { sku is String, qty is Natural }
    record Acct is { balance is Natural, status is String, lines is many Line }
    record Other is { note is String }
    record FnIn is { amount is Natural }
    event Ev is { note is String }
    event Ev2 is { note is String }
    command Plain is { amount is Natural }
    command WithYields yields event Ev is { amount is Natural }
    command Target is { amount is Natural }
    result Ans is { balance is Natural }
    query Ask replies result Ans is { id is UUID }
    outlet Out is type Ev
    function Calc is { requires FnIn returns FnIn ??? }
    entity Peer is {
      state PS of record Other is {
        handler PH is { on command Target { ??? } }
      }
    }
'''

# Statement snippets. `trigger` says which on-clause the container must use.
STMTS = {
  "when":    ('when prompt("it is so") then { do "a" } end', "plain"),
  "match":   ('match Acct.status { case Pending { do "a" } default { do "b" } }', "plain"),
  "foreach": ('foreach ln in field Acct.lines { do "a" }', "plain"),
  "send":    ('send event Ev to outlet Out', "plain"),
  "tell":    ('tell command Target to entity Peer', "plain"),
  "yield":   ('yield event Ev(note = "x")', "yields"),
  "reply":   ('reply result Ans()', "query"),
  "require": ('require Zero == Zero', "plain"),
  "set":     ('set field Acct.balance to "1"', "plain"),
  "let":     ('let v = Zero', "plain"),
  "do":      ('do "a thing"', "plain"),
  "error":   ('error "nope"', "plain"),
  "code":    ('```scala\nval x = 1\n```', "plain"),
  "morph":   ('morph entity Self to state S2 with record Other(note = "x")', "plain"),
  "become":  ('become entity Self to handler H2', "plain"),
  "put":     ('put "text" to output Panel', "plain"),
  "return":  ('return FnIn.amount', "plain"),
  "call":    ('let r = call function Calc(FnIn)', "plain"),
}

def trig(kind, which):
    """The on-clause header appropriate to the statement being probed."""
    return {"plain": "on command Plain", "yields": "on command WithYields",
            "query": "on query Ask"}[which]

def entity_handler(stmt, which):
    return f'''domain D is {{
  author A is {{ name is "R" email is "r@o.com" }}
  context C is {{{VOCAB}
    entity Self is {{
      state S of record Acct is {{
        handler H is {{ {trig("e", which)} {{
{stmt}
        }} }}
      }}
      state S2 of record Other is {{ handler H2 is {{ on command Plain {{ ??? }} }} }}
    }}
  }}
}}'''

def context_handler(stmt, which):
    return f'''domain D is {{
  author A is {{ name is "R" email is "r@o.com" }}
  context C is {{{VOCAB}
    entity Self is {{ state S of record Acct is {{ handler H is {{ on command Plain {{ ??? }} }} }}
      state S2 of record Other is {{ handler H2 is {{ on command Plain {{ ??? }} }} }} }}
    handler CH is {{ {trig("c", which)} {{
{stmt}
    }} }}
  }}
}}'''

def app_handler(stmt, which):
    return f'''domain D is {{
  author A is {{ name is "R" email is "r@o.com" }}
  user U is "a person"
  application context C is {{{VOCAB}
    entity Self is {{ state S of record Acct is {{ handler H is {{ on command Plain {{ ??? }} }} }}
      state S2 of record Other is {{ handler H2 is {{ on command Plain {{ ??? }} }} }} }}
    page P is {{ document Panel shows type Other }}
    handler AH is {{ {trig("a", which)} {{
{stmt}
    }} }}
  }}
}}'''

def function_body(stmt, which):
    return f'''domain D is {{
  author A is {{ name is "R" email is "r@o.com" }}
  context C is {{{VOCAB}
    entity Self is {{
      function Fn is {{ requires FnIn returns FnIn
{stmt}
      }}
      state S of record Acct is {{ handler H is {{ on command Plain {{ ??? }} }} }}
      state S2 of record Other is {{ handler H2 is {{ on command Plain {{ ??? }} }} }}
    }}
  }}
}}'''

def on_activate(stmt, which):
    return f'''domain D is {{
  author A is {{ name is "R" email is "r@o.com" }}
  context C is {{{VOCAB}
    entity Self is {{
      handler L is {{ on activate {{
{stmt}
      }} }}
      state S of record Acct is {{ handler H is {{ on command Plain {{ ??? }} }} }}
      state S2 of record Other is {{ handler H2 is {{ on command Plain {{ ??? }} }} }}
    }}
  }}
}}'''

def on_event(stmt, which):
    return f'''domain D is {{
  author A is {{ name is "R" email is "r@o.com" }}
  context C is {{{VOCAB}
    entity Self is {{
      state S of record Acct is {{ handler H is {{ on event Ev2 {{
{stmt}
      }} }} }}
      state S2 of record Other is {{ handler H2 is {{ on command Plain {{ ??? }} }} }}
    }}
  }}
}}'''

def saga_step(stmt, which):
    return f'''domain D is {{
  author A is {{ name is "R" email is "r@o.com" }}
  context C is {{{VOCAB}
    entity Self is {{ state S of record Acct is {{ handler H is {{ on command Plain {{ ??? }} }} }}
      state S2 of record Other is {{ handler H2 is {{ on command Plain {{ ??? }} }} }} }}
    saga Sg is {{
      requires FnIn
      returns Other
      step One is {{
{stmt}
      }} reverted by {{ tell command Target to entity Peer }}
      step Two is {{ tell command Target to entity Peer }}
        reverted by {{ tell command Target to entity Peer }}
    }}
  }}
}}'''

CONTAINERS = [
  ("entity handler", entity_handler),
  ("context handler", context_handler),
  ("app-ctx handler", app_handler),
  ("function", function_body),
  ("on activate", on_activate),
  ("on event", on_event),
  ("saga step", saga_step),
]

def run(src):
    with tempfile.NamedTemporaryFile("w", suffix=".riddl", delete=False) as fh:
        fh.write(src); path = fh.name
    try:
        p = subprocess.run([RIDDLC, "validate", path], capture_output=True,
                           text=True, timeout=120)
        out = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout + p.stderr)
        bad = [l for l in out.split("\n")
               if l.startswith("[error]") or l.startswith("[severe]")
               or l.startswith("[deprecated]")]
        if not bad:
            return "yes", ""
        i = out.split("\n").index(bad[0])
        return "NO", " ".join(out.split("\n")[i:i+2])[:150]
    finally:
        os.unlink(path)

only = sys.argv[1:] or list(STMTS)
print(f"{'statement':10}" + "".join(f"{c[:15]:>17}" for c, _ in CONTAINERS))
detail = []
for s in only:
    snippet, which = STMTS[s]
    row = f"{s:10}"
    for cname, fn in CONTAINERS:
        verdict, msg = run(fn(snippet, which))
        row += f"{verdict:>17}"
        if verdict == "NO":
            detail.append((s, cname, msg))
    print(row, flush=True)
print("\n--- rejections ---")
for s, c, m in detail:
    print(f"{s:9} {c:16} {m}")
