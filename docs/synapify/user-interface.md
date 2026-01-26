# User Interface Guide

Synapify's interface is designed to support both visual and textual modeling
workflows. This guide explains each component of the interface and how to use
them effectively.

---

## Interface Layout

The Synapify window is organized into four panels arranged in three columns.
Three of the panels can be hidden to maximize workspace, leaving the visual
editor to fill the entire window.

```
┌─────────────┬─────────────────────────┬─────────────┐
│             │                         │             │
│   Model     │     Visual Editor       │  Metadata   │
│   Tree      │     (primary)           │     &       │
│             │                         │   Info      │
│  [hideable] │                         │ [hideable]  │
│             ├─────────────────────────┤             │
│             │     Text Editor         │             │
│             │     (Monaco)            │             │
│             │     [hideable]          │             │
└─────────────┴─────────────────────────┴─────────────┘
```

| Panel | Position | Hideable | Purpose |
|-------|----------|----------|---------|
| **Model Tree** | Left | Yes | Navigate the RIDDL definition hierarchy |
| **Visual Editor** | Center top | No | Primary editing canvas |
| **Text Editor** | Center bottom | Yes | RIDDL source code editing |
| **Metadata & Info** | Right | Yes | Definition metadata and model statistics |

!!! note "Screen Size"
    Synapify is a desktop application optimized for larger screens. While it
    may function on tablets, it is not recommended for small screen devices
    like phones.

---

## Visual Editor

The visual editor occupies the center-top position and is the primary
workspace for designing RIDDL models. This panel cannot be hidden—when you
collapse the other three panels, the visual editor expands to fill the
entire window.

The visual editor displays your RIDDL model as a hierarchy of interactive
blocks representing domains, contexts, entities, and other definitions.

### Canvas Navigation

- **Pan**: Click and drag on empty canvas space, or use two-finger scroll
- **Zoom**: Use pinch gestures, scroll wheel with modifier key, or zoom
  controls
- **Fit to view**: Double-click empty canvas space to fit all content

### Definition Blocks

Each RIDDL definition appears as a block on the canvas. Blocks are visually
distinguished by type:

| Definition Type | Description |
|-----------------|-------------|
| **Domain** | Top-level container, typically the outermost block |
| **Context** | Bounded context within a domain |
| **Entity** | Stateful business object |
| **Repository** | Persistent storage abstraction |
| **Projector** | Event projection component |
| **Saga** | Multi-step process coordinator |
| **Streamlet** | Stream processing unit |
| **Adaptor** | Message translation bridge |

### Working with Blocks

**Selecting**: Click a block to select it. The metadata panel updates to
show details for the selected definition, and the text editor scrolls to
the corresponding source.

**Expanding/Collapsing**: Container blocks (domains, contexts) can be
expanded to show their contents or collapsed to save space.

**Navigating**: Use the breadcrumb bar above the canvas to see your current
location in the hierarchy and quickly navigate to parent containers.

### Adding Definitions

!!! note "Coming Soon"
    Full drag-and-drop editing from a palette is under development.

---

## Text Editor

The text editor occupies the center-bottom position, directly below the
visual editor. It provides full source-level access to your RIDDL model
and can be hidden when you want to focus entirely on visual modeling.

The editor is powered by Monaco, the same editor engine used in Visual
Studio Code.

### Editor Features

**Syntax Highlighting**: RIDDL keywords, types, strings, comments, and other
language elements are color-coded for readability.

**Line Numbers**: Displayed in the gutter for easy reference and navigation.

**Code Folding**: Collapse definition bodies to focus on structure. Click
the fold icons in the gutter, or use keyboard shortcuts:

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Fold | ++cmd+option+bracket-left++ | ++ctrl+shift+bracket-left++ |
| Unfold | ++cmd+option+bracket-right++ | ++ctrl+shift+bracket-right++ |
| Fold All | ++cmd+k++ ++cmd+0++ | ++ctrl+k++ ++ctrl+0++ |
| Unfold All | ++cmd+k++ ++cmd+j++ | ++ctrl+k++ ++ctrl+j++ |

**Search and Replace**: Find and replace text within the current file:

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Find | ++cmd+f++ | ++ctrl+f++ |
| Replace | ++cmd+h++ | ++ctrl+h++ |

**Multiple Cursors**: Hold ++option++ (macOS) or ++alt++ (Windows/Linux) and
click to place multiple cursors for simultaneous editing.

### Synchronization

The text editor stays synchronized with the visual editor bidirectionally:

- Edit in text and see the visual representation update
- Select a block visually and the text editor scrolls to that definition
- Changes in either view are immediately reflected in the other

If the RIDDL source has syntax errors, the visual editor shows the last
valid state while the text editor highlights the problems.

---

## Model Tree Panel

The model tree occupies the left side of the window and displays the RIDDL
definition hierarchy derived from the parsed AST (Abstract Syntax Tree).
This panel can be hidden to maximize the editing area.

### Hierarchy Navigation

The tree shows the logical structure of your model:

```
OnlineRetail (domain)
├── Catalog (context)
│   ├── Product (entity)
│   │   ├── CreateProduct (command)
│   │   ├── ProductCreated (event)
│   │   └── Active (state)
│   └── Category (entity)
├── Shopping (context)
│   └── Cart (entity)
└── Fulfillment (context)
    └── Order (entity)
```

### Using the Tree

**Navigation**: Click any item in the tree to:

- Select it in the visual editor
- Scroll the text editor to its source location
- Display its metadata in the right panel

**Rapid Movement**: The tree provides the fastest way to jump between
definitions in a large model. Rather than scrolling through the visual
canvas or searching text, click directly on the definition you need.

**Structure Understanding**: The tree reveals the complete model hierarchy
regardless of how definitions are organized across files. Included files
appear as part of the unified structure.

---

## Metadata & Info Panel

The metadata and information panel occupies the right side of the window.
It serves two purposes: editing definition metadata and displaying model
statistics. This panel can be hidden when not needed.

### Definition Metadata

When you select a definition (in the visual editor, text editor, or model
tree), the metadata panel shows the contents of its `with` clause:

**Common Metadata Fields**:

- **briefly**: Short one-line description
- **described as**: Full multi-line documentation
- **term**: Glossary definition for ubiquitous language
- **author**: Who created or maintains this definition

Edit these fields directly in the panel. Changes are reflected in the
text editor's source code.

**Example**: For a selected entity, you might see:

```
Name: Product
Brief: A product available for purchase
Description:
  The Product entity represents items in the catalog
  that customers can browse and purchase...
Author: jane.doe@example.com
```

### Model Statistics

The panel also displays statistics about your model:

| Statistic | Description |
|-----------|-------------|
| **Node Count** | Total number of definitions in the model |
| **Domain Count** | Number of top-level domains |
| **Context Count** | Number of bounded contexts |
| **Entity Count** | Number of entities |
| **Unresolved References** | Links to undefined definitions |
| **Warnings** | Validation warnings from the compiler |
| **Errors** | Validation errors that must be fixed |

These statistics update as you edit, giving you continuous insight into
your model's size and health.

---

## Panel Visibility

Toggle panel visibility to customize your workspace:

### Hiding Panels

- **Model Tree**: Click the tree toggle button or use the keyboard shortcut
- **Text Editor**: Click the text toggle button or use the keyboard shortcut
- **Metadata Panel**: Click the info toggle button or use the keyboard shortcut

### Focus Mode

Hide all three collapsible panels to enter focus mode, where the visual
editor fills the entire window. This is useful for:

- Presenting your model to stakeholders
- Working on a smaller screen
- Concentrating on visual layout without distractions

### Suggested Layouts

| Task | Recommended Layout |
|------|-------------------|
| **Initial design** | Visual + Text (hide tree and metadata) |
| **Navigation** | Visual + Tree (hide text and metadata) |
| **Documentation** | Visual + Metadata (hide tree and text) |
| **Detailed editing** | All panels visible |
| **Presentation** | Visual only (hide all) |

---

## Keyboard Shortcuts

### Global

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| New Project | ++cmd+n++ | ++ctrl+n++ |
| Open Project | ++cmd+o++ | ++ctrl+o++ |
| Save | ++cmd+s++ | ++ctrl+s++ |
| Save All | ++cmd+shift+s++ | ++ctrl+shift+s++ |
| Close Project | ++cmd+w++ | ++ctrl+w++ |
| Preferences | ++cmd+comma++ | ++ctrl+comma++ |

### Panel Visibility

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Toggle Model Tree | ++cmd+1++ | ++ctrl+1++ |
| Toggle Text Editor | ++cmd+2++ | ++ctrl+2++ |
| Toggle Metadata Panel | ++cmd+3++ | ++ctrl+3++ |

### Navigation

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Go to Definition | ++cmd+click++ | ++ctrl+click++ |
| Go to File | ++cmd+p++ | ++ctrl+p++ |
| Next Error | ++f8++ | ++f8++ |
| Previous Error | ++shift+f8++ | ++shift+f8++ |

### Editing

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Undo | ++cmd+z++ | ++ctrl+z++ |
| Redo | ++cmd+shift+z++ | ++ctrl+y++ |
| Delete Selection | ++delete++ | ++delete++ |

---

## Tips for Effective Modeling

### Start Visual, Refine in Text

Begin with the visual editor to establish structure—domains, contexts, and
major entities. Use the text editor when you need to add detailed handlers,
complex types, or precise business logic.

### Use the Model Tree for Large Models

As your model grows, the tree becomes essential for navigation. Rather than
scrolling through a large canvas, click directly on the definition you need.

### Keep Metadata Current

Use the metadata panel to document definitions as you create them. The
`briefly` description is especially important—it appears in tooltips,
generated documentation, and helps others understand your model.

### Watch the Statistics

The unresolved references count and error count are early warning signals.
Address issues as they appear rather than accumulating technical debt.

### Customize Your Layout

Different tasks benefit from different panel arrangements. Learn the
keyboard shortcuts for toggling panels so you can quickly switch between
layouts as your focus changes.