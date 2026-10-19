from exceptions import SetUsedOnNonVariable, VariableUnset
from line_context import LineContext
from operator_handlers import handle_comparison_operators, resolve_expression
from syntax import Keywords, ComparisonOperators
from value_types import Types

def handle_print(context: LineContext):
    split = context.line.split()
    type = split[0]
    value = " ".join(split[1:])
    if Types(type) == Types.INTEGER or Types(type) == Types.STRING:
        print(value)
    else:
        # Handle variables here by resolving the variable value and checking for if it has been defined yet in the variable table
        pass

def handle_if_then(context: LineContext):
    split = context.line.split()
    condition = split[:split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1:]

    result = False
    # Not always a GOTO here just temporary...
    for i in range(len(condition)):
        if condition[i] in ComparisonOperators:
            result = handle_comparison_operators(condition[i], " ".join(condition[:i]), " ".join(condition[i + 1:]), context.variable_table)

    if result:
        context.keyword = branch[0]
        context.line = " ".join(branch)
        return handle_keyword(context)


def handle_goto(context: LineContext):
    return context.story.node_table[context.line]

def handle_input(context: LineContext):
    player_input = input()
    context.line = f"{context.line} {Types.STRING.value} {player_input}"
    handle_set(context)

def handle_set(context: LineContext):
    split = context.line.split()
    if split[0] != Types.VARIABLE.value:
        raise SetUsedOnNonVariable(context.loc)
    result, unresolved_vars = resolve_expression(" ".join(split[2:]), context.variable_table, context.line)
    result = result[0].split()
    context.variable_table[split[1]] = f"{result[0]} {result[2]}"
    if unresolved_vars != []:
        raise VariableUnset(context.loc)

keyword_table = {
    Keywords.PRINT: handle_print,
    Keywords.IF: handle_if_then,
    Keywords.GOTO: handle_goto,
    Keywords.INPUT: handle_input,
    Keywords.SET: handle_set
}

# Node is a special keyword and is handled in the parser when populating the table
def handle_keyword(context: LineContext) -> None:
    keyword = Keywords(context.keyword)
    if keyword == Keywords.NODE:
        return
    removed_keyword = " ".join(context.line.split()[1:])
    context.line = removed_keyword
    return keyword_table[keyword](context)
