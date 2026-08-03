---
title: "AST, Finder and Passes"
description: "The programmatic API for reading and analysing a RIDDL model: the AST node hierarchy, the content accessors, the Finder, and the Pass infrastructure."
---

# AST, Finder and Passes

This page is for people writing **tools** against RIDDL — generators, IDE
plugins, linters, anything that reads a parsed model rather than writing one.
It documents three layers:

| Layer | Answers |
|---|---|
| **[AST](#the-ast)** | What is in the model? |
| **[Finder](#finder)** | Where in the model is *X*? |
| **[Passes](#passes)** | How do I walk the whole model and produce something? |

!!! info "Source of truth"
    Everything here is taken from `language/.../AST.scala`, `Finder.scala` and
    `passes/.../Pass.scala` on riddl's `release/2` branch. Where the scaladoc
    explains *why* a thing is the way it is, that reasoning is reproduced here
    rather than paraphrased away — it is usually the part that saves you time.

---

## The AST

### `RiddlValue`, the root of everything

Every node in a parsed model is a `RiddlValue`. It carries four things worth
knowing about before you build anything on top of it.

| Member | Type | Notes |
|---|---|---|
| `loc` | `At` | Where the value was parsed from |
| `span` | `Option[(Int, Int)]` | Character offsets `(start, end)` into `declaringFile` |
| `declaringFile` | `Option[String]` | The file that **declared** this value |
| `kind` | `String` | The node's class name, for messages |
| `format` | `String` | A short rendering, for error messages |

Two of these exist specifically for tools that edit source, and both have a
trap attached:

**`span` is character offsets, not line/column.** A definition needs a start
*and* an end, which costs two integers this way and two pairs the other. It is
`None` when the location is unknown — a value built programmatically, or
rebuilt from a serialization that carried no offsets. If you are editing RIDDL
in place, use this; deriving the range by re-scanning the text is how you
delete the wrong thing.

**`declaringFile` survives `FlattenPass`.** It comes from the parser input the
value was parsed from, not from the enclosing `Include` wrapper, so it is still
correct after includes are folded away. That is exactly what a multi-file
editing tool needs — *which file do I write this change into?*

!!! warning "Do not reconstruct provenance yourself"
    Two tempting approaches are both wrong: reading `Include.origin` before
    flattening, and keying definitions by a synthetic `(kind, id, line, col)`
    tuple — which collides across files. `declaringFile` is the supported
    answer.

### Containers, Branches, Leaves and Definitions

```
RiddlValue
├── Container[CV]        — holds `contents: Contents[CV]`
│   └── Branch[CV]       — a Container that is also a Definition
└── Definition           — has an Identifier and metadata
    └── Leaf             — a Definition with no contents
```

`Parents` is `Seq[Branch[?]]` — the chain from a node up to the root.

!!! warning "`isEmpty` is semantic, not structural"
    A container is empty when it holds **no definitions**; comments do not
    count. `context C is { // TODO }` is a stub, not a defined context, and
    treating it as non-empty let it slip past every completeness check.

    If you need to know whether there are any children *at all* — a text
    emitter deciding whether to open a brace, say — ask `contents.isEmpty`
    directly instead.

### Content accessors

Rather than filtering `contents` by hand, every container mixes in accessor
traits that name what it can hold — `WithTypes` gives `types`, `WithEntities`
gives `entities`, and so on. There are **35 declarations across 34 names**:

```
comments   types      constants   invariants  functions   handlers
inlets     outlets    states      groups      outputs     inputs
statements contexts   authors     versions    copyrights  users
epics      domains    projectors  repositories entities   streamlets
connectors adaptors   sagas       sagaSteps   cases       shownBy
modules    fields     methods     clauses
```

!!! warning "`repositories` means two different things"
    It is the one name declared twice, and the return types differ:

    | Where | Returns |
    |---|---|
    | `WithRepositories` (contexts, domains…) | `Seq[Repository]` — the **definitions** |
    | `Projector` | `Seq[RepositoryRef]` — the **references** |

    A tool that treats `projector.repositories` as definitions gets refs, and
    the mistake type-checks only if you were not looking.

#### They see through includes *and* imports

All 35 are implemented with `filterThroughWrappers`, which descends into
`Include` and `BASTImport` wrappers before applying the type test:

```scala
def filterThroughWrappers[T <: RiddlValue: ClassTag]: Seq[T] =
  val theClass = classTag[T].runtimeClass
  def loop(items: Seq[RiddlValue]): Seq[T] =
    items.flatMap {
      case inc: Include[?]                            => loop(inc.contents.toSeq)
      case bi: BASTImport                             => loop(bi.contents.toSeq)
      case x if theClass.isAssignableFrom(x.getClass) => Seq(x.asInstanceOf[T])
      case _                                          => Seq.empty
    }
  loop(container.toSeq)
```

**This is a recent change, and it fixed a real hole.** Previously
`context.entities` was empty whenever the entity happened to be written in an
included file, while `context.repositories` in the same context returned its
one repository — the same model giving different answers depending only on
which file the author typed a definition into. riddl-generator produced 582
files for reactive-bbq without a single entity class in them, and *nothing
failed*: the model validated, the generator succeeded, and the output merely
had a hole.

The principle settled on: **provenance is riddl's bookkeeping, not the
reader's**. A client asking what is in a container wants the full list;
whether a member was written inline, included, or imported is not a
distinction any consumer has a stake in.

!!! danger "Do not add your own include walk"
    If you have code like `context.entities ++ context.includes.flatMap(...)`,
    delete the second half. It now returns every included definition **twice**.

    riddl had seven such hand-rolled walks internally — helpers like
    `getEntities` that existed purely to paper over the gap. They are now thin
    aliases for the accessor they were compensating for. They remain public
    (`@JSExport`) so nothing breaks, but new code should call the accessor.

#### Three that deliberately stay literal

`processors`, `definitions` and `vitals` still use plain `filter` and do **not**
descend wrappers. They are consumed by riddl's own passes, whose callers
already reach included definitions another way, so making them transparent
would double-count rather than fix anything.

`includes` also stays on `filter` — a wrapper is matched *before* the type
test, so `filterThroughWrappers` is the wrong tool for finding the wrappers
themselves.

!!! warning "Reading and resolving diverge for imports"
    `domain.types` reports a `.bast`-imported type, but a **reference** to that
    type still fails to resolve until an explicit flatten, because the symbol
    table is built by traversal rather than by these accessors.

    This is defensible — reading is the client's question, resolving is the
    model's — but it means a model can name a type its own accessors report.
    Whether `SymbolsPass` should index wrapper contents is an open question in
    riddl's backlog.

### Entity intentions

As of RIDDL 2.0-rc.9, an entity's semantics are keywords before `entity`
rather than options in metadata (see
[Entity Intentions](../authors/authoring-riddl.md#entity-intentions) for the language
side). On the AST they are a first-class field:

```scala
case class Entity(
  loc: At,
  id: Identifier,
  contents: Contents[EntityContents] = Contents.empty(),
  ascribedShape: Option[StreamletShape] = None,
  intentions: Seq[EntityIntention] = Seq.empty,
  metadata: Contents[MetaData] = Contents.empty()
) extends Processor[EntityContents] with WithStates[EntityContents]:

  def hasIntention(intention: EntityIntention): Boolean = intentions.contains(intention)
```

Ask `hasIntention` rather than searching `metadata` for an option. The parser
stores `intentions` **canonically sorted**, because `Definition.equals`
compares the field — write order must never make two otherwise-identical
entities structurally unequal.

The deprecated option spellings are *consumed* by the parser: they set the
intention and are removed from metadata, so a tool never sees both forms.

---

## Finder

`Finder` wraps a container and searches it. Construct one with
`Finder(container)`.

| Method | Returns |
|---|---|
| `find(select: CV => Boolean)` | every value matching a predicate |
| `findByType[T]` | every value of a type |
| `recursiveFindByType[T]` | as above, but descends into nested statements |
| `findWithParents[T](select)` | matches paired with their `Parents` |
| `findParents(node)` | the parent chain of one definition |
| `findAllPaths` | a `HashMap[Definition, Parents]` for the whole tree |
| `findEmpty` | every empty definition, with parents |
| `findInParents[T](...)` | search upward instead of downward |
| `transform[TT](select)(f)` | rewrite matching nodes |

`findByType` and `recursiveFindByType` **cache per type**, so repeated queries
for the same type do not re-traverse the tree. The cache lives on the `Finder`
instance — keep one around rather than constructing a fresh `Finder` per query.

`Finder` is `@JSExportTopLevel`, so it is available from JavaScript as
`Finder`, as are its methods.

---

## Passes

A **Pass** walks the model once and produces a `PassOutput`. Passes are how
riddl itself is built — symbols, resolution and validation are all passes — and
how a tool should do any whole-model analysis.

### The shapes available

| Base class | Use when |
|---|---|
| `Pass` | You want full control of traversal |
| `DepthFirstPass` | Depth-first over every value |
| `HierarchyPass` | You care about *entering* and *leaving* containers |
| `VisitingPass[VT]` | You want a separate visitor object to receive the callbacks |
| `CollectingPass[ET]` | You are accumulating a `Seq[ET]` |

`HierarchyPass` is the one most tools want. Its callbacks:

```scala
protected def openContainer(definition: Definition, parents: Parents): Unit
protected def processLeaf(definition: Leaf, parents: Parents): Unit
protected def processValue(value: RiddlValue, parents: Parents): Unit
protected def closeContainer(definition: Definition, parents: Parents): Unit

// Wrappers get their own hooks, all defaulting to no-op:
protected def openInclude(include: Include[?], parents: Parents): Unit = ()
protected def closeInclude(include: Include[?], parents: Parents): Unit = ()
protected def openBASTImport(bi: BASTImport, parents: Parents): Unit = ()
protected def closeBASTImport(bi: BASTImport, parents: Parents): Unit = ()
protected def traverseBASTImportContents(bi: BASTImport): Boolean = true
```

Note that a Pass **traverses** wrappers rather than seeing through them — the
opposite of the accessors. That is deliberate: a pass building a symbol table
cares where a definition came from, while a client reading a container does
not. Override `traverseBASTImportContents` to skip imported content.

### Declaring one

Every pass has a `name`, may declare prerequisites, and returns a result:

```scala
def name: String
protected final def requires[OPT <: PassOptions](passInfo: PassInfo[OPT]): Unit
def preProcess(root: PassRoot): PassRoot = root
protected def process(definition: RiddlValue, parents: ParentStack): Unit
def postProcess(root: PassRoot): Unit = ()
def result(root: PassRoot): PassOutput
def close(): Unit = ()
```

`PassRoot` is `Branch[?]`. `requires` is how a pass states that it must run
after another — call it in the constructor.

### Running them

```scala
Pass.runThesePasses(input: PassInput, passes: PassCreators): PassesResult
```

`Pass.standardPasses` gives the three that every model needs, in order:

1. **`SymbolsPass`** — builds the symbol table
2. **`ResolutionPass`** — resolves path references
3. **`ValidationPass`** — validates

!!! important "Only run your own pass after these three"
    A model is not processable until all three have succeeded. Anything you
    build on an unresolved AST is reading references that do not yet point
    anywhere.

Two variants exist:

- **`Pass.quickValidationPasses`** — the same three, but validation in Quick
  mode, skipping expensive streaming analysis and handler classification.
  Intended for interactive and LSP use, where speed beats exhaustiveness.
- **`standardPasses` with completeness warnings enabled** additionally runs
  `MessageFlowPass`, `EntityLifecyclePass`, `UseCaseWitnessPass` and
  `UseCaseTracePass`, in that order — the first two feed the second two. They
  are gated so a plain `validate` pays nothing for them.

### Reading the results

`PassesResult` is what you get back:

| Member | Gives you |
|---|---|
| `root` | the `PassRoot` that was processed |
| `messages` | every message from every pass, plus any added |
| `symbols` | `SymbolsOutput` — the symbol table |
| `resolution` | `ResolutionOutput` |
| `validation` | `ValidationOutput` |
| `refMap` | `ReferenceMap` — what each reference resolved to |
| `usage` | `Usages` — who uses what |
| `outputOf[T](passName)` | any other pass's output, by name |
| `hasOutputOf(passName)` | whether a pass ran |

`refMap` and `usage` are shortcuts into `resolution`, and they are the two most
tools actually want: `refMap` turns a `Reference` into the `Definition` it
points at, which is the step every generator needs and the reason a model must
be resolved before you read it.

Pass the name from the pass's companion object — `SymbolsPass.name`, not a
string literal.

---

## Related

- [Design Principles](principles.md) — why the language is shaped this way
- [Language Reference](../../references/language-reference.md) — the surface syntax
- [EBNF Grammar](../../references/ebnf-grammar.md) — the parser's grammar
