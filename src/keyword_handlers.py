from syntax import Keywords, ComparisonOperators
from line_context import LineContext
from operator_handlers import handle_operators
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
            result = handle_operators(condition[i], condition[:i], condition[i + 1:], context.variable_table)

    if result:
        context.keyword = branch[0]
        context.line = " ".join(branch)
        return handle_keyword(context)


def handle_goto(context: LineContext):
    return context.story.node_table[context.line]

def handle_input(context: LineContext):
    player_input = input()
    context.variable_table[context.line] = f"{Types.STRING.value} {player_input}"

keyword_table = {
    Keywords.PRINT: handle_print,
    Keywords.IF: handle_if_then,
    Keywords.GOTO: handle_goto,
    Keywords.INPUT: handle_input
}

# Node is a special keyword and is handled in the parser when populating the table
def handle_keyword(context: LineContext) -> None:
    keyword = Keywords(context.keyword)
    if keyword == Keywords.NODE:
        return
    removed_keyword = " ".join(context.line.split()[1:])
    context.line = removed_keyword
    return keyword_table[keyword](context)
