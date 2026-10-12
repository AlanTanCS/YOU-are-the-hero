import output

def handle(node: dict) -> str:
    # decision text is a question and needs and answer
    output.print_text(node)
    ans = int(input(""))
    return node["GOTO"][ans - 1]
