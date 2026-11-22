from exceptions import ExceptionContext
from model.story_token import Token
from model.syntax import Namespace
from scanner.tokenise import split_statement, tokenise


def scan_story_file(path: str, namespace: Namespace) -> dict[int, list[Token]]:

    line_indexes = {}
    exception_context = ExceptionContext(path)

    with open(path) as story_data:
        for i, line in enumerate(story_data):
            exception_context.line_number = i + 1
            if line.strip() == "" or line.strip()[:2] == "//":
                continue
            line_indexes[i + 1] = []
            split = split_statement(line)
            for lexeme in split:
                token = tokenise(lexeme, namespace, exception_context)
                line_indexes[i + 1] += token

    return line_indexes
