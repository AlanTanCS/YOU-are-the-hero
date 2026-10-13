from keywords import Keywords

def handle_print(line: str):
    print(line)
    pass

def handle_if(line: str):
    pass

def handle_then(line: str):
    pass

def handle_goto(line: str):
    pass

def handle_input(line: str):
    pass

table = {
    Keywords.PRINT: handle_print,
    Keywords.IF: handle_if,
    Keywords.THEN: handle_then,
    Keywords.GOTO: handle_goto,
    Keywords.INPUT: handle_input
}

# Node is a special keyword and is handled in the parser when populating the table
def handle_keyword(keyword_string: Keywords, line: str, loc: int) -> None:
    keyword = Keywords(keyword_string)
    if keyword == Keywords.NODE:
        return
    removed_keyword = " ".join(line.split()[1:])
    table[keyword](removed_keyword)