# Simulation Guide

!!! note "Coming Soon"
    Simulation integration is under active development. This guide describes
    the planned capabilities.

Synapify integrates with [riddlsim](https://github.com/ossuminc/riddlsim) to
let you validate your model's behavior before writing any implementation code.
Simulation catches logical errors, verifies state transitions, and builds
confidence that your design will work as intended.

---

## Why Simulate?

A RIDDL model defines *what* your system should do—the commands it accepts,
events it produces, and states it maintains. But does the design actually
work? Simulation answers this question by executing your model against
realistic scenarios.

**Benefits of simulation:**

- **Catch design errors early** before they become expensive implementation
  bugs
- **Verify state transitions** to ensure entities move through expected
  lifecycles
- **Test edge cases** that might be overlooked in manual review
- **Build stakeholder confidence** by demonstrating working behavior
- **Document expected behavior** through executable scenarios

---

## How It Works

Synapify connects to riddlsim via HTTP requests. When you run a simulation:

1. **Synapify sends your model** to riddlsim (either the full RIDDL content
   or a reference to a publicly accessible GitHub repository)
2. **Synapify sends scenarios** that define what inputs to provide and what
   outcomes to expect
3. **riddlsim parses the model** and builds its own AST representation
4. **riddlsim executes the scenarios** against the model
5. **Results stream back** to Synapify showing pass/fail status and any
   unexpected behavior

The simulation runs independently on riddlsim's infrastructure. Synapify
displays progress and results as they arrive.

---

## Simulation Scenarios

A simulation scenario describes a sequence of interactions with your model
and the expected outcomes. Scenarios are the "test cases" for your design.

### Scenario Structure

Each scenario includes:

- **Name and description** explaining what behavior is being tested
- **Setup** establishing initial state if needed
- **Steps** defining commands to send and events to expect
- **Assertions** verifying the final state matches expectations

### Example Scenario

For a shopping cart entity, a scenario might test adding items:

```
Scenario: Add item to empty cart
  Given an empty Cart for customer "C123"
  When command AddItem with {productId: "P456", quantity: 2}
  Then event ItemAdded is published
  And Cart state contains item "P456" with quantity 2
```

### Scenario Editor

!!! note "Coming Soon"
    The graphical scenario editor is under development.

Synapify will provide a visual editor for creating simulation scenarios:

- **Drag and drop** to build step sequences
- **Autocomplete** for commands, events, and field names from your model
- **Visual timeline** showing the expected flow
- **Inline validation** catching errors before you run

---

## Running Simulations

### Single Scenario

To run one scenario:

1. Select the scenario in the simulation panel
2. Click "Run" or use the keyboard shortcut
3. Watch results stream in as steps execute
4. Review pass/fail status for each assertion

### Scenario Suites

Group related scenarios into suites for batch execution:

- **Smoke tests**: Quick scenarios verifying basic functionality
- **Entity lifecycle**: Complete state transition coverage
- **Integration**: Cross-context message flows
- **Edge cases**: Boundary conditions and error handling

Run an entire suite to verify broad model correctness after changes.

### Continuous Validation

Configure Synapify to run key scenarios automatically:

- **On save**: Run smoke tests whenever you save
- **On demand**: Run full suite before committing changes
- **Scheduled**: Run comprehensive tests periodically

---

## Understanding Results

### Success

When a scenario passes:

- All commands were accepted by the model
- All expected events were produced
- All state assertions matched

The model behaves as designed for this scenario.

### Failure

When a scenario fails, riddlsim reports:

- **Which step failed** in the scenario sequence
- **What was expected** based on your assertions
- **What actually happened** in the simulation
- **Model state** at the point of failure

Use this information to determine whether the issue is in your model
design or in the scenario's expectations.

### Common Issues

| Symptom | Likely Cause |
|---------|--------------|
| Command rejected | Missing handler or guard condition failed |
| Wrong event produced | Handler logic doesn't match intent |
| State mismatch | Field updates missing or incorrect |
| Timeout | Infinite loop or missing state transition |

---

## Organizing Scenarios

### File Storage

Simulation scenarios can be stored alongside your RIDDL model:

```
my-project/
├── src/
│   └── main.riddl
├── scenarios/
│   ├── cart-lifecycle.sim
│   ├── order-placement.sim
│   └── inventory-edge-cases.sim
└── project.json
```

Storing scenarios in the same repository as your model ensures they stay
synchronized and can be versioned together.

### Naming Conventions

- **Descriptive names**: `cart-add-remove-items.sim` not `test1.sim`
- **Group by entity or feature**: Keep related scenarios together
- **Indicate coverage level**: `smoke-`, `full-`, `edge-` prefixes

### Documentation

Each scenario file should include:

- Purpose: What behavior is being validated
- Prerequisites: Any setup required
- Coverage: What paths through the model are exercised

---

## Best Practices

### Start Simple

Begin with basic "happy path" scenarios that verify core functionality.
Add edge cases and error scenarios as the model matures.

### One Concept Per Scenario

Each scenario should test one specific behavior. This makes failures
easier to diagnose and keeps scenarios maintainable.

### Use Realistic Data

Scenarios with realistic field values catch issues that abstract examples
miss. Use plausible customer IDs, product names, and quantities.

### Maintain Scenarios

When you change your model, update affected scenarios. Outdated scenarios
give false confidence or spurious failures.

### Review Failures Carefully

A failing scenario might indicate:

- A bug in your model design (fix the model)
- An incorrect expectation (fix the scenario)
- A missing feature (add to the model)

Don't dismiss failures without understanding the root cause.

---

## Integration with Development Workflow

### Design Phase

Use simulation to validate design decisions before implementation:

1. Draft the model structure
2. Write scenarios for key use cases
3. Run simulations to verify behavior
4. Iterate until scenarios pass

### Implementation Phase

As implementation proceeds, simulations serve as acceptance criteria:

- Implementors know exactly what behavior to produce
- Generated code can be validated against the same scenarios
- Discrepancies between model and implementation are caught early

### Maintenance Phase

When changes are needed:

1. Update scenarios to reflect new requirements
2. Run simulations to see what breaks
3. Update the model to pass new scenarios
4. Verify existing scenarios still pass

---

## Related Documentation

- [RIDDL Language Reference](../riddl/references/language-reference.md) -
  Handler and statement syntax
- [Author's Guide](../riddl/guides/authors/index.md) - Writing effective
  handlers
- [riddlsim Repository](https://github.com/ossuminc/riddlsim) - Simulation
  engine details