from keywords import Keywords
from line_context import LineContext
from value_types import Types

def handle_print(context: LineContext):
    split = context.line.split()
    type = split[0]
    value = " ".join(split[1:])
    if Types(type) == Types.INT or Types(type) == Types.STRING:
        print(value)

def handle_if_then(context: LineContext):
    split = context.line.split()
    condition = split[:split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1:]
    print(condition, branch)
    # Not always a GOTO here just temporary...
    context.keyword = branch[0]
    context.line = " ".join(branch)
    return handle_keyword(context)


def handle_goto(context: LineContext):
    return context.story.node_table[context.line]

def handle_input(context: LineContext):
    player_input = input()
    context.variable_table[context.line] = f"{Types.STRING.value} {player_input}"

table = {
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
    return table[keyword](context)