from exceptions import SetUsedOnNonVariable, VariableUnset, IllegalStringOperation
from line_context import LineContext
from operator_handlers import handle_comparison_operators, resolve_expression, resolve_value
from syntax import Keywords
from token import Token
from value_types import Types

def handle_print(context: LineContext):
    argument = context.line[0]
    # Add global variables onto local variables for calculations
    var_table_copy = dict(context.variable_table)
    var_table_copy.update(context.global_variables)
    if argument.type == Types.INTEGER or argument.type == Types.STRING:
        print(argument.value)
    if argument.type == Types.GLOBAL_VARIABLE:
        print(resolve_value(argument, var_table_copy).value)
    if argument.type == Types.VARIABLE:
        print(resolve_value(argument, var_table_copy).value)
    if argument.type == Types.EXPRESSION_START:
        try:
            print(resolve_expression(context.line, var_table_copy).value)
        except TypeError:
            raise IllegalStringOperation(context.loc)
        except NameError:
            raise VariableUnset(context.loc)

def handle_if_then(context: LineContext):
    condition = []
    branch = []
    for token_pos in range(len(context.line)):
        if context.line[token_pos].value == Keywords.THEN:
            condition = context.line[:token_pos]
            branch = context.line[token_pos + 1:]
            break

    result = False
    for i in range(len(condition)):
        if condition[i].type == Types.COMPARISON_OPERATOR:
            result = handle_comparison_operators(condition[i], condition[:i], condition[i + 1:], context.variable_table)

    if result:
        context.keyword = branch[0]
        context.line = branch
        return handle_keyword(context)

def handle_goto(context: LineContext):
    if context.line[0].value == Keywords.NODE:
        return context.story.scene_info.node_table[context.line[1].value]
    if context.line[0].value == Keywords.SCENE:
        return context.line[1].value

def handle_input(context: LineContext):
    player_input = input()
    context.line.append(Token(Types.STRING, player_input))
    handle_set(context)

def handle_set(context: LineContext):
    var_table_copy = dict(context.variable_table)
    var_table_copy.update(context.global_variables)
    if context.line[0].type != Types.VARIABLE and context.line[0].type != Types.GLOBAL_VARIABLE:
        raise SetUsedOnNonVariable(context.loc)
    if context.line[1].type != Types.EXPRESSION_START:
        resolved = resolve_value(context.line[1], var_table_copy)
        if resolved == None:
            raise VariableUnset(context.loc)
        if context.line[0].value in context.global_variables:
            context.global_variables[context.line[0].value] = resolved
        else:
            context.variable_table[context.line[0].value] = resolved
        return

    # we have an expression
    try:
        result = resolve_expression(context.line[1:], var_table_copy)
    except TypeError:
        raise IllegalStringOperation(context.loc)
    except NameError:
        raise VariableUnset(context.loc)
    if context.line[0].type == Types.VARIABLE:
        context.variable_table[context.line[0].value] = result
    else:
        context.global_variables[context.line[0].value] = result

keyword_table = {
    Keywords.PRINT: handle_print,
    Keywords.IF: handle_if_then,
    Keywords.GOTO: handle_goto,
    Keywords.INPUT: handle_input,
    Keywords.SET: handle_set,
}

# Node is a special keyword and is handled in the parser when populating the table
def handle_keyword(context: LineContext) -> None:
    keyword = context.keyword.value
    if keyword == Keywords.NODE:
        return
    removed_keyword = context.line[1:]

    context.line = removed_keyword
    return keyword_table[keyword](context)
