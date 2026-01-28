---
title: "Example Models"
description: >-
  Browse real-world RIDDL model examples. Learn from working models and
  contribute your own to help the community.
---
# Example Models

The **[riddl-models](https://github.com/ossuminc/riddl-models)** repository
contains a curated collection of RIDDL models demonstrating real-world patterns
and best practices. These examples serve as:

- **Learning resources** - Study how experienced modelers structure their work
- **Starting points** - Fork and adapt models for your own projects
- **Pattern catalog** - Reference implementations of common DDD patterns

---

## Browse Models

Visit the repository to explore available models:

[:material-github: Browse riddl-models](https://github.com/ossuminc/riddl-models){ .md-button .md-button--primary }

Each top-level directory represents a complete example domain. Models include:

- Full RIDDL source files
- README explaining the domain and design decisions
- Validation status and any known limitations

---

## Example Categories

Models in the repository cover various domains and patterns:

### Business Domains

| Domain | Description |
|--------|-------------|
| E-commerce | Product catalogs, shopping carts, orders, fulfillment |
| Healthcare | Patient records, appointments, prescriptions |
| Finance | Accounts, transactions, payments, ledgers |
| Logistics | Shipping, tracking, warehouse management |

### Technical Patterns

| Pattern | Description |
|---------|-------------|
| Event Sourcing | Entities that store state as event logs |
| Saga Orchestration | Multi-step processes with compensation |
| CQRS | Separate command and query models |
| State Machines | Entities with explicit lifecycle states |

!!! note "Growing Collection"
    The model collection is actively growing. If you don't see an example
    for your use case, consider [contributing one](#contribute-your-model).

---

## Using Examples

### Clone and Explore

```bash
git clone https://github.com/ossuminc/riddl-models.git
cd riddl-models

# Pick an example
cd ecommerce

# Validate with riddlc
riddlc validate main.riddl
```

### Adapt for Your Project

1. **Fork the repository** or copy the relevant files
2. **Rename domains and contexts** to match your terminology
3. **Modify types and entities** to fit your requirements
4. **Add your own handlers** with domain-specific logic
5. **Validate frequently** as you make changes

---

## Contribute Your Model

We welcome community contributions! Sharing your models helps others learn
and strengthens the RIDDL ecosystem.

### Contribution Guidelines

Your model should:

- [ ] **Pass validation** - `riddlc validate` with no errors
- [ ] **Include documentation** - README explaining the domain
- [ ] **Follow conventions** - Use standard RIDDL naming patterns
- [ ] **Be self-contained** - No external dependencies
- [ ] **Have educational value** - Demonstrate patterns worth learning

### Submission Process

1. **Fork** the [riddl-models repository](https://github.com/ossuminc/riddl-models)

2. **Create a directory** for your model:
   ```
   riddl-models/
   └── your-domain-name/
       ├── README.md          # Domain description
       ├── main.riddl         # Entry point
       └── *.riddl            # Additional files
   ```

3. **Add a README** with:
   - Domain overview and purpose
   - Key design decisions
   - Patterns demonstrated
   - Any limitations or simplifications

4. **Validate your model**:
   ```bash
   riddlc validate your-domain-name/main.riddl
   ```

5. **Submit a pull request** with:
   - Clear title describing the domain
   - Brief description of what makes this example valuable

### Example README Template

```markdown
# [Domain Name]

Brief description of what this domain models.

## Overview

What business or technical problem does this model address?
What are the main bounded contexts and their responsibilities?

## Key Patterns

- **Pattern 1**: How it's demonstrated
- **Pattern 2**: How it's demonstrated

## Design Decisions

Why were certain choices made? What alternatives were considered?

## Limitations

What simplifications were made for educational clarity?
What would a production model need to add?

## Usage

How to validate and explore this model.
```

---

## Model Quality Standards

Contributed models are reviewed for:

### Correctness

- Validates without errors
- Types are properly defined
- References resolve correctly
- Handlers cover expected messages

### Clarity

- Meaningful names following conventions
- `briefly` clauses on all definitions
- Comments explaining non-obvious choices
- Logical organization of files

### Educational Value

- Demonstrates useful patterns
- Appropriate complexity for learning
- Well-documented design decisions
- Realistic domain (not contrived)

---

## Get Help

- **Questions about contributing**: Open an issue on
  [riddl-models](https://github.com/ossuminc/riddl-models/issues)
- **RIDDL language questions**: See the
  [Language Reference](../references/language-reference.md)
- **Validation errors**: Check the
  [Author's Guide](../guides/authors/index.md#common-validation-issues)

---

## Related Resources

- [5-Minute Quickstart](../quickstart.md) - Build your first model
- [Author's Guide](../guides/authors/index.md) - Complete authoring guide
- [Concepts](../concepts/index.md) - Deep dive into RIDDL concepts
- [Language Reference](../references/language-reference.md) - Full syntax
