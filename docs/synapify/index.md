# Synapify

Synapify is the visual editing interface for creating and managing
[RIDDL](../riddl/index.md) domain models. It combines powerful editing
capabilities with AI assistance to streamline your model development
workflow.

!!! warning "Coming Soon"
    Synapify is currently in active development. Features described below
    represent the planned capabilities. Check back for updates on
    availability.

---

## Overview

Synapify provides a complete environment for domain modeling with RIDDL:

- **Visual and Textual Editing** - Switch between graphical diagrams and
  source code views
- **Automatic Diagram Generation** - Visualize your model structure
  automatically
- **AI-Powered Assistance** - Integrated with your AI and Ossum's MCP Server
- **Model Simulation** - Request simulations to validate model behavior
- **Code Generation** - Generate implementation code from your models (coming
  soon)

---

## Editing Modes

### Graphical View

Visualize your domain model as interactive diagrams:

- **Domain hierarchy** - See contexts, entities, and their relationships
- **Message flows** - Trace commands, events, and queries between components
- **Type structures** - View aggregations and type definitions graphically
- **Drag-and-drop editing** - Modify your model visually

### Textual View

Full-featured RIDDL source editor:

- **Syntax highlighting** - Clear visual distinction of language elements
- **Real-time validation** - Immediate feedback on errors and warnings
- **Code completion** - Intelligent suggestions as you type
- **Synchronized views** - Changes in text update diagrams automatically

---

## Diagram Generation

Synapify automatically generates diagrams from your RIDDL model:

| Diagram Type | Shows |
|--------------|-------|
| **Context Map** | Bounded contexts and their relationships |
| **Entity Diagram** | Entities, their state, and message handlers |
| **Message Flow** | How messages move between components |
| **Type Hierarchy** | Type definitions and their relationships |
| **Saga Workflow** | Multi-step process coordination flows |

Diagrams update in real-time as you edit your model.

---

## AI Integration

Synapify integrates with AI assistants through Ossum's
[MCP Server](../MCP/index.md) to provide intelligent modeling support:

### Capabilities

- **Validate models** - Get detailed feedback on errors and warnings
- **Check completeness** - Identify missing elements in your model
- **Generate suggestions** - Receive recommendations for what to add next
- **Explain errors** - Understand validation issues with fix suggestions
- **Convert descriptions** - Transform natural language into RIDDL structures

### How It Works

1. Connect your preferred AI assistant (Claude, Gemini, Copilot, etc.)
2. Configure the RIDDL MCP Server connection
3. Ask questions or request assistance directly in Synapify
4. AI responses include proper RIDDL syntax ready to insert

---

## Model Simulation

Request simulations to validate your model's behavior before implementation:

- **Behavioral validation** - Verify handlers respond correctly to messages
- **State transitions** - Confirm entities move through expected states
- **Saga coordination** - Test multi-step process flows
- **Edge cases** - Explore boundary conditions and error scenarios

Simulation results help you refine your model before committing to code.

---

## Code Generation

*Coming soon*

Generate implementation code from your validated RIDDL models:

- Target multiple languages and frameworks
- Produce type-safe message definitions
- Create entity implementations with handlers
- Generate API endpoints and documentation

---

## Getting Started

When Synapify becomes available:

1. Download and install Synapify
2. Create or open a RIDDL project
3. Connect to the MCP Server for AI assistance
4. Start modeling with visual or textual editing
5. Generate diagrams to visualize your design
6. Run simulations to validate behavior

---

## Requirements

- **Platform**: macOS, Windows, Linux
- **MCP Server**: For AI integration features
- **Network**: For simulation and code generation services

---

## Stay Updated

Synapify is under active development. For updates:

- **Lined In**: Follow us here: https://www.linkedin.com/company/ossum-inc/
- **Email**: Ask a question here: support@ossuminc.com
- **List**: Join email list here: https://www.ossuminc.com/ (scroll down)
- **GitHub**: Developers: [github.com/ossuminc](https://github.com/ossuminc)

---

## Related Documentation

- [RIDDL Language Reference](../riddl/references/language-reference.md)
- [Authoring RIDDL Sources](../OSS/authoring-riddl.md)
- [MCP Server Integration](../MCP/index.md)