from exceptions import ExceptionContext
from model.story_token import Token
from model.syntax import Namespace
from scanner.tokenise import split_statement, tokenise


def scan_entry_point(entry_path: str) -> dict[int, list[Token]]:

    line_indexes = {}
    exception_context = ExceptionContext(entry_path)

    with open(entry_path) as story_data:
        for i, line in enumerate(story_data):
            exception_context.line_number = i + 1
            if line.strip() == "" or line[:2].strip() == "//":
                continue
            line_indexes[i + 1] = []
            split = split_statement(line)
            for lexeme in split:
                token = tokenise(lexeme, Namespace.ENTRY, exception_context)
                line_indexes[i + 1] += token

    return line_indexes


def scan_scene():
    pass
