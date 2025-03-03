# Enhanced RIDDL Language Reference Guide

## Overview

RIDDL (Reactive Interface to Domain Definition Language) is a domain-specific 
language designed for modeling reactive systems using Domain-Driven Design (DDD)
principles. It bridges the gap between business domain experts and software 
engineers by providing a language that's both expressive for domain modeling and
precise enough for implementation.

## Core Philosophy

RIDDL emphasizes:
- Declarative syntax with natural language readability
- Event-driven and reactive design patterns
- State-based entity modeling with explicit transitions
- Clear separation of commands, events, queries and results
- Saga-based coordination of complex atomic processes and possibly distributed
- Comprehensive domain modeling through DDD concepts
- Asynchronous, non-blocking communications (implied)

## Language Structure

### Domain Hierarchy

RIDDL models are organized hierarchically:
- **Root**: Top-level container for the entire system. Roots are not defined but 
  consist of the top level definitions in a file. Roots can contain Modules,
  Domains, and Authors
- **Domain**: A container for the specification of some knowledge domain. Domains 
  may only contain Contexts
- **Context**: Bounded context containing related entities and components
- **Entity**: Stateful business objects with commands, events, and handlers
- **Repository**: Persistent storage for entities
- **Saga**: Orchestration of multi-step processes with compensation
- **Epic**: Collection of user stories/use cases
- **Case**: Specific user interaction flow

### Basic Syntax Elements

1. **Readability Words**: Optional keywords that improve human readability
   - `is`, `are`, `as`, `by`, `from`, `to`, `with`, etc.
   - Can be replaced with `:` in many contexts

2. **Definition Structure**:
   ```
   [type] [name] is {
     // definition contents
   } with {
     briefly as "Brief description"
     described by {
       | Detailed description
       | across multiple lines
     }
   }
   ```

   The metadata section (with `briefly` and `described by`) must always come after the closing brace of the definition, not within it.

3. **Type References**: Always specify the kind of reference
   - `entity Product`
   - `command CreateCart`
   - `event OrderCreated`
   - `state ProductData`
   - `user Customer`

## Containment Rules

RIDDL follows strict containment rules that define what elements can be defined within other elements:

1. **Domain** can contain:
   - Authors (metadata)
   - Types
   - Contexts
   - Nested Domains
   - Users
   - Epics

2. **Context** can contain:
   - Types
   - Entities
   - Repositories
   - Sagas
   - Streamlets
   - Pages (UI components)

3. **Entity** can contain:
   - States
   - Commands
   - Events
   - Functions
   - Handlers

4. **Authors** contain only their metadata and cannot contain any other RIDDL definitions.

## Type System

### Basic Types
- `UUID`, `String(min, max)`, `Integer`, `Decimal(whole, fractional)`
- `Boolean`, `Pattern("regex")`, `Real`, `Natural`, etc.

### Complex Types
- **Record Types**: Named collections of fields
  ```
  type Address is {
    street1 is String
    city is String
    state is String
    zipCode is String
    country is String
  } with {
    briefly as "Physical mailing address"
    described by {
      | Represents a physical address with standard components
      | used for shipping and billing purposes.
    }
  }
  ```

- **Enumerations**:
  ```
  type Status is any of {
    Active
    Inactive
    Suspended
  } with {
    briefly as "Possible entity statuses"
    described by {
      | Defines the possible states for an entity's lifecycle.
    }
  }
  ```

- **Collections**:
  ```
  items is many Item
  ```

## Entities and States

Entities are stateful objects with explicit states:

```
entity Product is {
  state ProductData of ProductRecord with {
    briefly as "Product state containing all product information"
    described by {
      | Contains the complete product information including identification,
      | pricing, and inventory information.
    }
  }
  
  // Commands, events, handlers
} with {
  briefly as "Represents a purchasable item"
  described by {
    | The Product entity represents items that can be purchased.
    | It contains all product attributes and responds to commands.
  }
}
```

States reference record types that define the data structure:

```
type ProductRecord is {
  id is ProductId
  name is Name
  price is Price
  // other fields
} with {
  briefly as "Record type containing product data"
  described by {
    | Defines the structure of product data including identification and pricing.
  }
}
```

## Commands and Events

Commands represent requests to change state:

```
command UpdatePrice is {
  productId is ProductId
  newPrice is Price
} with {
  briefly as "Command to change a product's price"
  described by {
    | Updates the price of a specific product identified by productId.
    | The new price must be a positive value.
  }
}
```

Events represent state changes that have occurred:

```
event PriceUpdated is {
  productId is ProductId
  oldPrice is Price
  newPrice is Price
} with {
  briefly as "Event indicating a product price change"
  described by {
    | Emitted when a product's price is successfully updated.
    | Contains both old and new prices for auditing and UI updates.
  }
}
```

### Command-Event Relationship

Commands should always result in one or more events being emitted. This follows the reactive principles of RIDDL:

```
handler ProductCommandHandler is {
  on command UpdatePrice is {
    if "newPrice > 0" then {
      morph entity Product to state ProductData with command UpdatePrice
      tell event PriceUpdated to entity Product  // Emitting an event is essential
    } else {
      error "Price must be greater than zero"
    } end
  }
} with {
  briefly as "Processes commands for product management"
  described by {
    | Handles commands related to product information management.
    | Validates input data, updates product state, and emits relevant events.
  }
}
```

## Handlers

Handlers process commands and emit events:

```
handler ProductCommandHandler is {
  on command UpdatePrice is {
    if "newPrice > 0" then {
      morph entity Product to state ProductData with command UpdatePrice
      tell event PriceUpdated to entity Product
    } else {
      error "Price must be greater than zero"
    } end
  }
} with {
  briefly as "Processes commands for product management"
  described by {
    | Handles commands related to product information and pricing management.
    | Validates input data, updates product state, and emits relevant events.
  }
}
```

## Statement Syntax

### Morph Statement
Changes entity state:
```
morph entity Product to state ProductData with command UpdatePrice
```

### Tell Statement
Sends events or commands:
```
tell event ItemAdded to entity Cart
tell command ProcessPayment to entity PaymentService
```

### Set Statement
Assigns values:
```
set field status to "Active"
```

### If Statement
Conditional logic:
```
if "condition" then {
  // actions
} else if "another condition" then {
  // actions
} else {
  // actions
} end
```

The `end` keyword is required to terminate if statements.

### Foreach Statement
Iteration:
```
foreach field Cart.items do {
  // actions for each item
} end
```

The `end` keyword is required to terminate foreach loops.

### Arbitrary Statement
Allows for implementation code inside functions and handler actions:
```
"var subtotal = 0;
 for (var i = 0; i < items.length; i++) {
   subtotal += items[i].totalPrice;
 }
 return subtotal;"
```

## Functions

Functions define reusable operations:

```
function calculateTotal is {
  requires {
    subtotal is Price
    taxes is Price
    shipping is Price
    discount is Price
  }
  returns {
    total is Price
  }
  
  // Implementation using arbitrary statement
  "return subtotal + taxes + shipping - discount;"
} with {
  briefly as "Calculates the final cart total"
  described by {
    | Calculates the final amount by adding subtotal, taxes, and shipping,
    | then subtracting any discounts.
  }
}
```

## Sagas

Sagas coordinate multi-step processes with compensation:

```
saga CheckoutProcess is {
  requires {
    cartId is CartId
    customerInfo is CustomerInfo
  }
  
  returns {
    success is Boolean
    orderId is UUID
  }
  
  step ProcessPayment is {
    // Payment processing logic
    tell command ProcessPayment to entity PaymentService
  } reverted by {
    // Compensation logic to refund
    tell command RefundPayment to entity PaymentService
  } with {
    briefly as "Processes payment for the order"
    described by {
      | Attempts to process payment using the provided payment details.
      | If payment fails, the checkout process is aborted.
      | If later steps fail, payment is refunded as part of compensation.
    }
  }
  
  // Additional steps
} with {
  briefly as "Orchestrates the checkout process steps"
  described by {
    | This saga orchestrates the multi-step process of completing a checkout,
    | including validating the cart and inventory, processing payment,
    | creating an order, and sending confirmation.
  }
}
```

## Repositories

Repositories define persistence:

```
repository CartRepository is {
  schema CartData is relational of
    cart as Cart
    link cartItems as field Cart.items.id to field Product.id
    
  handler CartRepositoryHandler is {
    on event CartCreated is {
      write "Create new cart record" to Cart
    }
    
    // Other event handlers
  } with {
    briefly as "Handles persistence of cart events"
    described by {
      | Handles all event-driven persistence operations related to shopping carts.
      | Responds to cart events by updating the persistent state of carts.
    }
  }
} with {
  briefly as "Persistent storage for shopping cart data"
  described by {
    | The CartRepository provides persistent storage for shopping cart data,
    | including the cart itself and all items within it.
  }
}
```

## UI Components

RIDDL supports UI modeling:

```
context UserInterface is {
  page ProductDetails is { /* ... */ } with {
    briefly as "Page showing product information"
    described by {
      | Displays detailed information about a product including name,
      | description, price, and images.
    }
  }
  
  page ShoppingCart is {
    button Checkout activates type Boolean with {
      briefly as "Checkout button to proceed to payment"
      described by {
        | Button that initiates the checkout process when clicked.
        | Transitions the user from the shopping cart view to the 
        | checkout information entry page.
      }
    }
  } with {
    briefly as "Page showing cart contents"
    described by {
      | Displays all items added to the cart with quantities and prices.
      | Allows customers to update quantities and proceed to checkout.
    }
  }
  
  page Payment is {
    form PaymentEntry submits type PaymentDetails with {
      briefly as "Form for entering payment information"
      described by {
        | Collects payment method and details from the customer.
        | Payment information is tokenized for security before processing.
      }
    }
  } with {
    briefly as "Page for payment processing"
    described by {
      | Allows customers to enter and submit payment information.
    }
  }
} with {
  briefly as "User interface components for the system"
  described by {
    | Contains all UI components used in the system including
    | product details, shopping cart, and checkout pages.
  }
}
```

## Epics and Use Cases

Epics model user stories:

```
epic ShoppingCartEpic is {
  user Customer wants to "add items to a shopping cart" 
  so that "they can purchase multiple items at once"
  
  case AddingToCart is {
    user Customer wants to "add products to cart" 
    so that "they can purchase them later"
    
    step from user Customer "views" page UserInterface.ProductDetails
    step send command AddToCart from user Customer to entity Cart
    step from entity Cart "updates" to page UserInterface.ShoppingCart
    step focus user Customer on page UserInterface.ShoppingCart
  } with {
    briefly as "Adding products to the shopping cart"
    described by {
      | This use case describes the process of a customer adding a product
      | to their shopping cart from a product detail page.
    }
  }
  
  // Additional cases
} with {
  briefly as "User stories related to shopping cart management"
  described by {
    | This epic covers the core shopping cart functionality including
    | adding items to carts, updating quantities, and removing items.
  }
}
```

## Metadata Placement

Metadata should always be placed after the closing brace of the definition, not within it:

**Correct:**
```
entity Product is {
  // Entity definition content
} with {
  briefly as "Product available for purchase"
  described by {
    | Represents a product in the catalog that customers can purchase.
    | Contains pricing, inventory, and product details.
  }
}
```

**Incorrect:**
```
entity Product is {
  // Entity definition content
  with {  // <-- This is wrong
    briefly as "Product available for purchase"
    described by {
      | Represents a product in the catalog that customers can purchase.
      | Contains pricing, inventory, and product details.
    }
  }
}
```

## Best Practices

1. **Include Metadata**: Add descriptions to all definitions with `with` clauses after their closing braces
2. **Be Explicit**: Always specify reference types (entity, command, event, etc.)
3. **Place Functions Close to Usage**: Define functions within the entities that use them
4. **End Control Structures**: Always terminate control structures with `end` keyword
5. **Use Field References**: In foreach loops, use `foreach field X.items`
6. **Provide Default Actions**: Use `"nothing"` for empty else branches
7. **Model Complete Flows**: Include UI components and user interactions
8. **Maintain Semantic Consistency**: Use the same field names for the same concepts
9. **Emit Events from Commands**: Ensure commands emit events to follow reactive principles
10. **Document UI Components**: Provide clear descriptions for UI elements that interact with users
11. **Follow Containment Rules**: Only define elements within their appropriate containers (domain, context, entity, etc.)
12. **Separate Metadata**: Always place metadata sections after a definition's closing brace, never inside it

## Common Syntax Issues

1. Don't use assignment operators (`=`); use `set field x to "value"`
2. Don't forget `end` after if statements and foreach loops
3. Always include reference types before identifiers
4. Use proper syntax for function parameters and return values
5. Make sure all morph/tell statements have correct type references
6. Place comments only where definitions are allowed, not within clauses
7. Ensure metadata blocks follow their definitions rather than being nested within them
8. Never place entity, type, or repository definitions directly within a domain - they must be in a context
9. Never place definitions inside an author - authors only contain metadata
10. Make sure each context contains related definitions that form a bounded context

## Incomplete Definitions

Use `???` as a placeholder for incomplete definitions:

```
record PaymentDetails is { ??? } with {
  briefly as "Record for payment information details"
  described by {
    | Contains all payment information required for processing.
  }
}

page Checkout is { ??? } with {
  briefly as "Checkout page for completing purchase"
  described by {
    | Allows customers to review items and provide checkout information.
  }
}
```

## Author Inheritance

Authors are defined once and inherited throughout the model hierarchy, but cannot contain any definitions:

```
domain ShopifyCart is {
  author Claude is {
    name is "Anthropic Claude"
    email is "support@anthropic.com"
  } with {
    briefly as "Model creator and maintainer"
    described by {
      | Primary architect responsible for designing this model.
    }
  }
  
  // All definitions within the domain inherit Claude as author
  context ShoppingContext is {
    // No need to repeat author information here
  } with {
    briefly as "Main shopping context containing commerce entities"
    described by {
      | The ShoppingContext is the primary bounded context for the shopping system.
    }
  }
} with {
  briefly as "Shopping cart domain model"
  described by {
    | This domain model represents a shopping cart system.
    | It includes core entities, commands, events, and processes.
  }
}
```

## Additional Syntax Clarifications

From the formal grammar analysis, several important syntax points deserve special emphasis:

1. **Sequential Execution**: Statement blocks are executed sequentially, and while actions appear to flow naturally, there's no "implicit flow" - each action in handlers and functions must be explicitly defined.

2. **Reference Type Consistency**: When referring to entities, commands, events, etc., always use the correct reference type (e.g., `entity Product`, not just `Product`).

3. **Nested Element Validation**: Elements can only be nested within specific parent elements according to strict containment rules. For example, types must be defined within contexts, not directly within domains.

4. **Termination of Statements**: Control flow statements must be properly terminated:
   - If statements must end with the `end` keyword
   - Foreach loops must end with the `end` keyword
   - Other statements are implicitly terminated

5. **Handler Clauses**: Handlers must use specific clause types:
   - `on command X` for command handlers
   - `on event X` for event handlers
   - `on init` for initialization
   - `on term` for termination
   - `on other` for default/catch-all behavior

6. **Readability Words**: While readability words like `is`, `as`, `by`, etc. are often optional, their proper placement significantly improves model clarity. Use them consistently.

## Formal EBNF Grammar

Below is the formal Extended Backus-Naur Form (EBNF) grammar for RIDDL. This grammar provides a precise definition of RIDDL syntax and can be used as a reference when constructing valid RIDDL expressions.

```ebnf
(* RIDDL Grammar in EBNF *)

(* Basic Elements *)
letter = "A" | "B" | ... | "Z" | "a" | "b" | ... | "z" ;
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
identifier = simple_identifier | quoted_identifier ;
simple_identifier = letter { letter | digit | "_" | "-" } ;
quoted_identifier = "'" { letter | digit | "_" | "+" | "\\" | "-" | "|" | "/" | "@" | "$" | "%" | "&" | "," | ":" | " " }+ "'" ;
path_identifier = identifier { "." identifier } ;
literal_string = '"' { string_char | escape_sequence } '"' ;
escape_sequence = "\\" ( "\\" | '"' | "a" | "e" | "f" | "n" | "r" | "t" | hexEscape | unicodeEscape ) ;
hexEscape = "\\x" digit digit [digit [digit [digit [digit [digit [digit]]]]]] ;
unicodeEscape = "\\u" digit digit digit digit ;
integer = ["+"|"-"] digit {digit} ;

(* Comments *)
comment = inline_comment | end_of_line_comment ;
inline_comment = "/*" {any_char_except_end_comment} "*/" ;
end_of_line_comment = "//" {any_char_except_newline} newline ;

(* Main Structure *)
root = {root_content}+ ;
root_content = module_content | module | root_include ;
module_content = domain | author | comment ;
root_include = "include" literal_string ;

(* Module *)
module = "module" identifier "is" "{" {module_content | module_include}+ "}" [with_metadata] ;
module_include = "include" literal_string ;

(* Domain *)
domain = "domain" identifier "is" "{" domain_body "}" [with_metadata] ;
domain_body = domain_definitions | "???" ;
domain_definitions = {domain_content}+ ;
domain_content = vital_definition_contents | author | context | domain | user | epic | saga | import_def | domain_include | comment ;
import_def = "import" "domain" identifier "from" literal_string ;
domain_include = "include" literal_string ;

(* Context *)
context = "context" identifier "is" "{" context_body "}" [with_metadata] ;
context_body = context_definitions | "???" ;
context_definitions = {context_definition}+ ;
context_definition = processor_definition_contents | entity | adaptor | group | saga | streamlet | projector | repository | connector | context_include | comment ;
context_include = "include" literal_string ;

(* Entity *)
entity = "entity" identifier "is" "{" entity_body "}" [with_metadata] ;
entity_body = entity_definitions | "???" ;
entity_definitions = {entity_content}+ ;
entity_content = processor_definition_contents | state | entity_include ;
state = "state" identifier ("of" | "is") type_ref [with_metadata] ;
entity_include = "include" literal_string ;

(* Processor Definition Contents *)
processor_definition_contents = vital_definition_contents | constant | invariant | function | handler | streamlet | connector | relationship ;
vital_definition_contents = type_def | comment ;

(* Type Definition *)
type_def = def_of_type | def_of_type_kind_type ;
def_of_type = "type" identifier "is" type_expression [with_metadata] ;
def_of_type_kind_type = aggregate_use_case identifier (scala_aggregate_definition | ("is" (aliased_type_expression | aggregation))) [with_metadata] ;
aggregate_use_case = "type" | "command" | "query" | "event" | "result" | "record" | "graph" | "table" ;

(* Type Expressions *)
type_expression = cardinality(
    predefined_types | pattern_type | unique_id_type | enumeration | sequence_type | mapping_from_to | a_set_type |
    graph_type | table_type | replica_type | range_type | decimal_type | alternation | entity_reference_type | 
    aggregation | aggregate_use_case_type_expression | aliased_type_expression
) ;

cardinality = ["many"] ["optional"] type_expression_base ["?" | "*" | "+"] ;
type_expression_base = predefined_types | pattern_type | unique_id_type | enumeration | sequence_type | mapping_from_to | a_set_type |
    graph_type | table_type | replica_type | range_type | decimal_type | alternation | entity_reference_type | 
    aggregation | aggregate_use_case_type_expression | aliased_type_expression ;

(* Predefined Types *)
predefined_types = string_type | currency_type | url_type | integer_predef_types | real_predef_types | time_predef_types | zoned_predef_types | decimal_type | other_predef_types ;
string_type = "String" ["(" [integer] "," [integer] ")"] ;
currency_type = "Currency" "(" iso_country_code ")" ;
url_type = "URL" ["(" literal_string ")"] ;
integer_predef_types = "Boolean" | "Integer" | "Natural" | "Whole" ;
real_predef_types = "Current" | "Length" | "Luminosity" | "Mass" | "Mole" | "Number" | "Real" | "Temperature" ;
time_predef_types = "Duration" | "DateTime" | "Date" | "TimeStamp" | "Time" ;
zoned_predef_types = ("ZonedDate" | "ZonedDateTime") "(" [zone] ")" ;
other_predef_types = "Abstract" | "Location" | "Nothing" | "UUID" | "UserId" ;
zone = {letter | digit | ":" | "." | "+" | "-"} ;

(* Type Expressions *)
pattern_type = "Pattern" "(" {literal_string} ")" ;
unique_id_type = "Id" "(" ["entity"] path_identifier ")" ;
enumeration = "any" ["of"] "{" enumerators "}" ;
enumerators = {enumerator [","]} | "???" ;
enumerator = identifier [enum_value] [with_metadata] ;
enum_value = "(" integer ")" ;
sequence_type = "sequence" "of" type_expression ;
mapping_from_to = "mapping" "from" type_expression "to" type_expression ;
a_set_type = "set" "of" type_expression ;
graph_type = "graph" "of" type_expression ;
table_type = "table" "of" type_expression "of" "[" integer {"," integer} "]" ;
replica_type = "replica" "of" replica_type_expression ;
replica_type_expression = integer_predef_types | mapping_from_to | a_set_type ;
range_type = "range" "(" [integer] "," [integer] ")" ;
decimal_type = "Decimal" "(" integer "," integer ")" ;
alternation = "one" ["of"] "{" {aliased_type_expression} "}" ;
entity_reference_type = "reference" ["to"] ["entity"] path_identifier ;
aggregation = "{" aggregate_definitions "}" ;
aggregate_definitions = {aggregate_content [","]} | "???" ;
aggregate_content = field | method | comment ;
aggregate_use_case_type_expression = aggregate_use_case aggregation ;
aliased_type_expression = [aggregate_use_case] path_identifier ;
scala_aggregate_definition = "(" {field [","]} ")" ;

(* Fields and Methods *)
field = identifier "is" field_type_expression [with_metadata] ;
method = identifier "(" [arguments] ")" "is" field_type_expression [with_metadata] ;
arguments = {method_argument [","]} ;
method_argument = identifier ":" field_type_expression ;
field_type_expression = cardinality(
    predefined_types | pattern_type | unique_id_type | enumeration | sequence_type | mapping_from_to | a_set_type |
    graph_type | table_type | replica_type | range_type | decimal_type | alternation | aggregation |
    aliased_type_expression | entity_reference_type
) ;

(* Functions *)
function = "function" identifier "is" "{" function_body "}" [with_metadata] ;
function_body = [func_input] [func_output] function_definitions ;
func_input = "requires" aggregation ;
func_output = "returns" aggregation ;
function_definitions = {"???" | (vital_definition_contents | function | function_include | statement)} ;
function_include = "include" literal_string ;

(* References *)
type_ref = [aggregate_use_case] path_identifier ;
field_ref = "field" path_identifier ;
constant_ref = "constant" path_identifier ;
message_ref = command_ref | event_ref | query_ref | result_ref | record_ref ;
command_ref = "command" path_identifier ;
event_ref = "event" path_identifier ;
query_ref = "query" path_identifier ;
result_ref = "result" path_identifier ;
record_ref = "record" path_identifier ;
adaptor_ref = "adaptor" path_identifier ;
entity_ref = "entity" path_identifier ;
function_ref = "function" path_identifier ;
handler_ref = "handler" path_identifier ;
state_ref = "state" path_identifier ;
context_ref = "context" path_identifier ;
outlet_ref = "outlet" path_identifier ;
inlet_ref = "inlet" path_identifier ;
streamlet_ref = "streamlets" path_identifier ;
projector_ref = "projector" path_identifier ;
repository_ref = "repository" path_identifier ;
saga_ref = "saga" path_identifier ;
epic_ref = "epic" path_identifier ;
user_ref = "user" path_identifier ;
output_ref = output_aliases path_identifier ;
input_ref = input_aliases path_identifier ;
group_ref = group_aliases path_identifier ;
author_ref = "by" "author" path_identifier ;
processor_ref = adaptor_ref | context_ref | entity_ref | projector_ref | repository_ref | streamlet_ref ;
any_interaction_ref = processor_ref | saga_ref | input_ref | output_ref | group_ref | user_ref ;

(* Handlers *)
handler = "handler" identifier "is" "{" handler_body "}" [with_metadata] ;
handler_body = {"???" | handler_contents} ;
handler_contents = {on_clause | comment} ;
on_clause = on_init_clause | on_other_clause | on_term_clause | on_message_clause ;
on_init_clause = "on init" "is" pseudo_code_block [with_metadata] ;
on_other_clause = "on other" "is" pseudo_code_block [with_metadata] ;
on_term_clause = "on term" "is" pseudo_code_block [with_metadata] ;
on_message_clause = "on" message_ref ["from" [identifier ":"] message_origins] "is" pseudo_code_block [with_metadata] ;
message_origins = inlet_ref | processor_ref | user_ref | epic_ref ;

(* Statements *)
statement = send_statement | arbitrary_statement | error_statement | the_set_statement | tell_statement | call_statement |
    stop_statement | if_then_else_statement | for_each_statement | code_statement | comment | reply_statement |
    focus_statement | morph_statement | become_statement | return_statement | read_statement | write_statement ;

send_statement = "send" message_ref "to" (outlet_ref | inlet_ref) ;
arbitrary_statement = literal_string ;
error_statement = "error" literal_string ;
the_set_statement = "set" field_ref "to" literal_string ;
tell_statement = "tell" message_ref "to" processor_ref ;
call_statement = "call" function_ref ;
stop_statement = "stop" ;
if_then_else_statement = "if" literal_string "then" pseudo_code_block ["else" pseudo_code_block "end"] ;
for_each_statement = "foreach" (field_ref | inlet_ref | outlet_ref) "do" pseudo_code_block "end" ;
code_statement = "```" ("scala" | "java" | "python" | "mojo") code_contents "```" ;
code_contents = {any_char_except_triple_backtick} ;
reply_statement = "reply" ["with"] message_ref ;
focus_statement = "focus" "on" group_ref ;
morph_statement = "morph" entity_ref "to" state_ref "with" message_ref ;
become_statement = "become" entity_ref "to" handler_ref ;
return_statement = "return" literal_string ;
read_statement = ("read" | "get" | "query" | "find" | "select") literal_string "from" type_ref "where" literal_string ;
write_statement = ("write" | "put" | "create" | "update" | "delete" | "remove" | "append" | "insert" | "modify") literal_string "to" type_ref ;

(* Pseudo Code Block *)
pseudo_code_block = "???" | {statement} | "{" {statement} "}" ;

(* Constants and Invariants *)
constant = "constant" identifier "is" type_expression "=" literal_string [with_metadata] ;
invariant = "invariant" identifier "is" [literal_string] [with_metadata] ;

(* Relationship *)
relationship = "relationship" identifier "to" processor_ref "as" relationship_cardinality ["label" "as" literal_string] [with_metadata] ;
relationship_cardinality = "1:1" | "1:N" | "N:1" | "N:N" ;

(* Streamlet-related *)
streamlet = source | sink | flow | merge | split | router | void ;
source = "source" identifier "is" "{" streamlet_body "}" [with_metadata] ;
sink = "sink" identifier "is" "{" streamlet_body "}" [with_metadata] ;
flow = "flow" identifier "is" "{" streamlet_body "}" [with_metadata] ;
merge = "merge" identifier "is" "{" streamlet_body "}" [with_metadata] ;
split = "split" identifier "is" "{" streamlet_body "}" [with_metadata] ;
router = "router" identifier "is" "{" streamlet_body "}" [with_metadata] ;
void = "void" identifier "is" "{" streamlet_body "}" [with_metadata] ;
streamlet_body = {"???" | streamlet_definition} ;
streamlet_definition = {inlet | outlet | streamlet_include | processor_definition_contents} ;
streamlet_include = "include" literal_string ;
inlet = "inlet" identifier "is" type_ref [with_metadata] ;
outlet = "outlet" identifier "is" type_ref [with_metadata] ;
connector = "connector" identifier "is" connector_definitions [with_metadata] ;
connector_definitions = ["(" "from" outlet_ref "to" inlet_ref ")" | "from" outlet_ref "to" inlet_ref] ;

(* Group-related *)
group = group_aliases identifier "is" "{" {"???" | group_definitions} "}" [with_metadata] ;
group_definitions = {group | contained_group | shown_by | group_output | group_input | comment} ;
contained_group = "contains" identifier "as" group_ref [with_metadata] ;
group_output = output_aliases identifier presentation_aliases (literal_string | constant_ref | type_ref) [output_definitions] [with_metadata] ;
group_input = input_aliases identifier acquisition_aliases type_ref [input_definitions] [with_metadata] ;
output_definitions = ["is" "{" {"???" | (group_output | type_ref)} "}"] ;
input_definitions = ["is" "{" {"???" | group_input} "}"] ;
group_aliases = "group" | "page" | "pane" | "dialog" | "menu" | "popup" | "frame" | "column" | "window" | "section" | "tab" | "flow" | "block" ;
output_aliases = "output" | "document" | "list" | "table" | "graph" | "animation" | "picture" ;
input_aliases = "input" | "form" | "text" | "button" | "picklist" | "selector" | "item" ;
presentation_aliases = "presents" | "shows" | "displays" | "writes" | "emits" ;
acquisition_aliases = "acquires" | "reads" | "takes" | "accepts" | "admits" | "initiates" | "submits" | "triggers" | "activates" | "starts" ;

(* Repository-related *)
repository = "repository" identifier "is" "{" repository_body "}" [with_metadata] ;
repository_body = {"???" | repository_definitions} ;
repository_definitions = {processor_definition_contents | schema | repository_include} ;
repository_include = "include" literal_string ;
schema = "schema" identifier "is" schema_kind {data} {link} {index} [with_metadata] ;
schema_kind = "flat" | "relational" | "time-series" | "graphical" | "hierarchical" | "star" | "document" | "columnar" | "vector" | "other" ;
data = "of" identifier "as" type_ref ;
link = "link" identifier "as" field_ref "to" field_ref ;
index = "index" "on" field_ref ;

(* Adaptor-related *)
adaptor = "adaptor" identifier adaptor_direction context_ref "is" "{" adaptor_body "}" [with_metadata] ;
adaptor_direction = "from" | "to" ;
adaptor_body = {"???" | adaptor_contents} ;
adaptor_contents = {processor_definition_contents | handler | adaptor_include} ;
adaptor_include = "include" literal_string ;

(* Projector-related *)
projector = "projector" identifier "is" "{" projector_body "}" [with_metadata] ;
projector_body = {"???" | projector_definitions} ;
projector_definitions = {processor_definition_contents | updates | projector_include} ;
projector_include = "include" literal_string ;
updates = "updates" repository_ref ;

(* Saga-related *)
saga = "saga" identifier "is" "{" saga_body "}" [with_metadata] ;
saga_body = [func_input] [func_output] {saga_definitions} ;
saga_definitions = {saga_step | inlet | outlet | function | term | saga_include | option} ;
saga_include = "include" literal_string ;
saga_step = "step" identifier "is" pseudo_code_block "reverted" ["by"] pseudo_code_block [with_metadata] ;

(* Epic-related *)
epic = "epic" identifier "is" "{" epic_body "}" [with_metadata] ;
epic_body = user_story {epic_definitions} ;
epic_definitions = {vital_definition_contents | use_case | shown_by | epic_include} ;
epic_include = "include" literal_string ;
use_case = "case" identifier "is" "{" user_story {"???" | interactions} "}" [with_metadata] ;
user_story = user_ref "wants" ["to"] literal_string "so" ["that"] literal_string ;
interactions = {interaction} ;
interaction = parallel_interactions | optional_interactions | sequential_interactions | step_interactions ;
parallel_interactions = "parallel" "{" interactions "}" ;
optional_interactions = "optional" "{" interactions "}" ;
sequential_interactions = "sequence" "{" interactions "}" ;
step_interactions = "step" (focus_on_group_step | direct_user_to_url | select_input_step | take_input_step | 
                            show_output_step | self_processing_step | send_message_step | arbitrary_step | vague_step) ;
focus_on_group_step = "focus" user_ref "on" group_ref [with_metadata] ;
direct_user_to_url = "direct" user_ref "to" http_url [with_metadata] ;
select_input_step = user_ref "selects" input_ref [with_metadata] ;
take_input_step = "take" input_ref "from" user_ref [with_metadata] ;
show_output_step = "show" output_ref "to" user_ref [with_metadata] ;
self_processing_step = "for" any_interaction_ref "is" literal_string [with_metadata] ;
send_message_step = "send" message_ref "from" any_interaction_ref "to" processor_ref [with_metadata] ;
arbitrary_step = "from" any_interaction_ref literal_string ["to"] any_interaction_ref [with_metadata] ;
vague_step = "is" literal_string literal_string literal_string [with_metadata] ;

(* User-related *)
user = "user" identifier "is" literal_string [with_metadata] ;

(* Author-related *)
author = "author" identifier "is" "{" [("???" | ("name" "is" literal_string "email" "is" literal_string 
        ["organization" "is" literal_string] ["title" "is" literal_string] ["url" "is" http_url]))] "}" [with_metadata] ;

(* URLs *)
http_url = ("http" | "https") "://" host_string [":" port_num] "/" [url_path] ;
host_string = {letter | digit | "-"} {"." {letter | digit | "-"}} ;
port_num = digit {digit} ;
url_path = {letter | digit | "-" | "_" | "." | "~" | "!" | "$" | "&" | "'" | "(" | ")" | "*" | "+" | "," | ";" | "="} ;

(* Metadata *)
with_metadata = ["with" "{" {"???" | {meta_data}} "}"] ;
meta_data = brief_description | description | term | option | author_ref | attachment | ulid_attachment | comment ;
brief_description = "briefly" ["by" | "as"] literal_string ;
description = "described" (("by" | "as") doc_block | ("at" http_url) | ("in" "file" literal_string)) ;
term = "term" identifier "is" doc_block ;
option = "option" ["is"] option_name ["(" {literal_string} ")"] ;
option_name = {lower_letter | digit | "_" | "-"} ;
attachment = "attachment" identifier "is" mime_type (("in" "file" literal_string) | ("as" literal_string)) ;
ulid_attachment = "attachment" "ULID" "is" literal_string ;
doc_block = "{" {markdown_lines | literal_strings | "???"} "}" | literal_string ;
markdown_lines = {markdown_line}+ ;
markdown_line = "|" {any_char_except_newline} ;
literal_strings = {literal_string}+ ;
shown_by = "shown" "by" "{" {http_url} "}" ;
mime_type = ("application" | "audio" | "example" | "font" | "image" | "model" | "text" | "video") "/" {mime_type_chars} ;
mime_type_chars = lower_letter | "." | "-" | "*" ;
```

This EBNF grammar provides a formal representation of the RIDDL language syntax. It's particularly useful for understanding the exact structure of each language element and how they relate to each other.
