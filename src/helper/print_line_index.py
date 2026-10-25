def print_line_index(line_index):
    if type(line_index) is list:
        out = ""
        for i in line_index:
            if i:
                out = f"{out} {i.type} {i.value}"
            else:
                out = f"{out} None"
    else:
        if line_index:
            out = f" {line_index.type} {line_index.value}"
        else:
            out = f" None"

    print(out)
