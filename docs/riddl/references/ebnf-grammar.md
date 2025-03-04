# Formal EBNF Grammar

Below is the formal Extended Backus-Naur Form (EBNF) grammar for RIDDL. 
This grammar provides a precise definition of RIDDL syntax and can be used as a 
reference when constructing valid RIDDL expressions. This grammar was 
automaticaly extracted from the reference grammar written in Scala/fastparse 
form at March 1, 2025. The maintainers will keep it up to date.  

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
