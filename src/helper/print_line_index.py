def print_line_index(line_index):
    if isinstance(line_index, list):
        out = ""
        for i in line_index:
            if i:
                out = f"{out} {i.type} {i.value}"
            else:
                out = f"{out} None"
    elif isinstance(line_index, dict):
        out = ""
        for key, value in line_index.items():
            if value:
                out = f"{out} {key} {value.type} {value.value},"
            else:
                out = f"{out} {key} None,"
    else:
        if line_index:
            out = f" {line_index.type} {line_index.value}"
        else:
            out = f" None"

    print(out)
