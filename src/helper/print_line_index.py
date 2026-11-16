from model.story_token import Token


def print_raw_line(line_index: list[Token] | dict) -> None:
    if isinstance(line_index, list):
        out = ""
        for token in line_index:
            out = f"{out} {token.value}"
    elif isinstance(line_index, dict):
        out = ""
        for token_list in line_index.values():
            out += "\n"
            for token in token_list:
                out = f"{out} {token.value}"
    print(out)


def print_line_index(line_index: list[Token] | dict) -> None:
    if isinstance(line_index, list):
        out = ""
        for i in line_index:
            if i:
                out = f"{out} {i.type} {i}"
            else:
                out = f"{out} None"
    elif isinstance(line_index, dict):
        out = ""
        for key, value in line_index.items():
            if value:
                out = f"{out} {key} {value.type} {value},"
            else:
                out = f"{out} {key} None,"
    else:
        if line_index:
            out = f" {line_index.type} {line_index}"
        else:
            out = " None"

    print(out)
