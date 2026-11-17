```ebnf
story                   = entry_file, { scene_file } ;
entry_file              = { blank_line | entry_statement } ;
scene_file              = { blank_line | scene_statement } ;

entry_statement         = entry_action | comment ;
entry_action            = scene_list | combat_list | global_declaration | "SCENE.", scene_action | "LIST.", list_statement
scene_list              = "SCENE_LIST", name_list ;
combat_list             = "COMBAT_LIST", name_list ;
global_declaration      = "GLOBAL", identifier, value ;

scene_statement         = node_declaration | scene_action | comment ;
scene_action            = print_statement | input_statement
                        | set_statement | conditional_statement | goto_statement
                        | "ENTRY.", entry_action | "LIST.", list_statement ;
node_declaration        = "NODE", name ;
print_statement         = "PRINT", value ;
input_statement         = "INPUT", identifier ;
set_statement           = "SET", identifier, value ;
conditional_statement   = "IF", comparison, "THEN", scene_action ;
goto_statement          = "GOTO", ("NODE" | "SCENE" | "COMBAT"), name ;

list_statement          = list_get | list_set | list_insert | list_remove | list_length ;
list_index              = integer | expression ;
list_get                = "GET", ( Identifier | ListLiteral ), list_index ;
list_set                = "SET", ( Identifier | ListLiteral ), list_index, value ;
list_insert             = "INSERT", ( Identifier | ListLiteral ), list_index, value ;
list_remove             = "REMOVE", ( Identifier | ListLiteral ), list_index ;
list_length             = "LENGTH", ( Identifier | ListLiteral ) ;

function                = list_get | list_length ;
expression              = "(", [ additive_expression ], ")" ;
additive_expression     = mult_expression, { arithmetic_operator, mult_expression } ;
mult_expression         = expression_value, { multiplication_operator, expression_value } ;
expression_value        = string | integer | identifier | expression | function ;
value                   = string | integer | identifier | list_literal | expression ;
comparison              = value, comparison_operator, value, { comparison_operator, value } ;

name_list               = "[", [ name, { ",", name } ], "]" ;
list_literal            = "[", [ value, { ",", value } ], "]" ;

name                    = identifier ;
identifier              = ( letter | under_score ), { letter | digit | under_score } ;
integer                 = [ "-" ], digit, { digit } ;
string                  = '"', { any_character_except_quote_or_newline }, '"' ;

arithmetic_operator     = "+" | "-" ;
comparison_operator     = "==" | ">" | "<" ;

comment                 = "//", { any_character }, newline ;
blank_line              = newline ;
```
