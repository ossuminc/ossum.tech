# Synapify

**The Solution Architect's Toolbench**

Synapify is a professional desktop application for designing distributed,
reactive, cloud-native systems using the [RIDDL](../riddl/index.md)
specification language. Whether you're a domain expert sketching out business
processes or a software architect defining precise system boundaries, Synapify
provides the visual and textual tools you need to create, validate, and
simulate your designs.

!!! warning "Early Access"
    Synapify is currently in active development. Core features are functional,
    with additional capabilities being added regularly. Check back for updates
    on availability.

---

## Why Synapify?

Traditional system design tools force a choice: either draw diagrams that
can't be validated, or write specifications that domain experts can't read.
Synapify bridges this gap by providing:

- **Visual modeling** that domain experts can understand and contribute to
- **Formal specification** that can be validated, simulated, and used for
  code generation
- **Bidirectional synchronization** so visual and textual views always match
- **AI assistance** to accelerate modeling and catch issues early

The result is a specification that serves as the single source of truth—from
initial design through implementation and beyond.

---

## Who Is Synapify For?

Synapify supports the full spectrum of RIDDL users:

### Domain Experts

Subject matter experts who understand the business domain deeply. Use
Synapify's visual editor to:

- Review and validate domain models created by others
- Contribute domain knowledge through intuitive diagrams
- Understand system structure without learning syntax
- Verify that models accurately represent business processes

### Authors

Those who create and maintain RIDDL models. Use Synapify to:

- Build models visually with drag-and-drop components
- Refine details in the synchronized text editor
- Validate models in real-time as you work
- Organize large models across multiple files

### Implementors

Developers who transform models into working software. Use Synapify to:

- Understand the system design before implementation
- Generate documentation and starter code
- Run simulations to validate behavioral assumptions
- Track model changes that affect implementation

### Developers

Those who extend the RIDDL ecosystem itself. Use Synapify to:

- Test language features with immediate visual feedback
- Explore how models parse and validate
- Debug issues in the RIDDL toolchain

---

## Core Capabilities

### Visual Editor

The primary workspace for designing your system. The visual editor displays
your RIDDL model as interactive blocks that represent domains, contexts,
entities, and other definitions. You can:

- **Navigate** the model hierarchy by expanding and collapsing containers
- **Select** definitions to view their details and edit properties
- **Arrange** components to create clear, readable diagrams
- **Drag and drop** new definitions from the palette

*Some visual editing features are still in development.*

### Text Editor

A full-featured RIDDL source editor powered by Monaco (the same editor engine
as VS Code). The text editor provides:

- **Syntax highlighting** for all RIDDL language elements
- **Real-time validation** with inline error and warning indicators
- **Code folding** for managing large files
- **Search and replace** across your model files

The text editor appears below the visual editor and stays synchronized—changes
in one view immediately appear in the other.

### Project Management

Synapify organizes your work into projects, each containing:

- A main RIDDL entry point file
- Supporting files for large models (via `include`)
- Project metadata and settings
- Git integration for version control

### Model Validation

As you work, Synapify continuously validates your model using the RIDDL
compiler. Validation catches:

- Syntax errors in your RIDDL definitions
- Undefined references to types or entities
- Structural issues like invalid containment
- Missing required elements

Errors and warnings appear in both the visual and text editors, with clear
messages explaining what needs to be fixed.

---

## Integrated Services

Synapify connects to external services to extend its capabilities beyond
design and validation.

### Model Simulation

!!! note "Coming Soon"
    Simulation integration is under development.

Connect to [riddlsim](https://github.com/ossuminc/riddlsim) to validate your
model's behavior before writing any code:

- **Define scenarios** that describe expected system behavior
- **Run simulations** against your model to verify handlers respond correctly
- **Test state transitions** to confirm entities move through expected states
- **Explore edge cases** to find issues before they become bugs

Simulation scenarios can be saved alongside your model and run repeatedly as
the model evolves.

### Code Generation

!!! note "Coming Soon"
    Code generation integration is under development.

Connect to riddl-gen to transform your validated models into implementation
artifacts:

- **Documentation** in AsciiDoc and Hugo formats
- **Akka/Scala** code for reactive microservices
- **Quarkus/Java** code (planned)
- Additional targets as the ecosystem grows

Generated code provides a starting point that preserves your model's structure
and behavior, reducing the gap between design and implementation.

### AI Assistance

Synapify integrates with AI assistants through the
[RIDDL MCP Server](../MCP/index.md) to provide intelligent modeling support:

- **Validate models** with detailed, actionable feedback
- **Generate suggestions** for what to add next based on patterns
- **Convert descriptions** from natural language into RIDDL structures
- **Explain errors** with fix recommendations

Configure your preferred AI assistant (Claude, Gemini, Copilot, etc.) with
the MCP server to enable these capabilities.

---

## Getting Started

### Installation

Synapify is available for macOS, Windows, and Linux. Download the installer
for your platform:

!!! note "Coming Soon"
    Installers will be available when Synapify reaches public release.

### System Requirements

- **macOS**: 11.0 (Big Sur) or later
- **Windows**: Windows 10 or later
- **Linux**: Ubuntu 20.04, Fedora 34, or equivalent
- **Memory**: 4 GB RAM minimum, 8 GB recommended
- **Disk**: 500 MB for installation
- **Network**: Required for simulation and code generation services

### Your First Project

1. **Launch Synapify** and choose "New Project" from the welcome screen
2. **Name your project** and select a location on your filesystem
3. **Start modeling** by adding a domain from the palette
4. **Add contexts** within your domain to represent bounded business areas
5. **Define entities** to model the stateful objects in each context
6. **Validate** your model using the built-in compiler integration
7. **Save** your work—Synapify auto-generates the proper file structure

See the [User Interface Guide](user-interface.md) for detailed information
on working with Synapify's editors and panels.

---

## Subscription Tiers

!!! note "Pricing Coming Soon"
    Subscription details will be announced closer to public release.

### Individual

For independent consultants and solo practitioners:

- Full visual and text editing
- Local project storage
- Simulation and code generation access
- Standard support

### Team

For small teams working together:

- Everything in Individual
- Shared project repositories
- Author attribution and tracking
- Collaborative editing features
- Priority support

### Enterprise

For organizations with advanced needs:

- Everything in Team
- Custom integration options
- On-premises deployment available
- Dedicated support
- Volume licensing

---

## Platform Architecture

Synapify is built with modern technologies chosen for reliability and
cross-platform consistency:

- **Electron** provides the desktop application framework
- **Scala.js** enables type-safe application logic
- **Monaco Editor** powers the text editing experience
- **Laminar** delivers reactive, functional UI components

The application runs entirely on your machine, with network access only
needed for simulation, code generation, and AI assistance services.

---

## Stay Updated

Synapify is under active development. For updates and announcements:

- **LinkedIn**: Follow us at
  [linkedin.com/company/ossum-inc](https://www.linkedin.com/company/ossum-inc/)
- **Email**: Questions? Contact support@ossuminc.com
- **Mailing List**: Subscribe at [ossuminc.com](https://www.ossuminc.com/)
  (scroll to newsletter signup)
- **GitHub**: Developers can follow progress at
  [github.com/ossuminc](https://github.com/ossuminc)

---

## Related Documentation

- [User Interface Guide](user-interface.md) - Detailed editor and panel
  documentation
- [Simulation Guide](simulation.md) - Running behavioral simulations
- [Code Generation Guide](generation.md) - Generating implementation artifacts
- [RIDDL Language Reference](../riddl/references/language-reference.md) -
  Complete language documentation
- [Authoring RIDDL Sources](../OSS/authoring-riddl.md) - Best practices for
  writing RIDDL
- [MCP Server Integration](../MCP/index.md) - Configuring AI assistance