import os

from exceptions import ExceptionContext, declaration_exception, syntax_exception
from model.context import StatementParseContext
from model.story_token import Token
from model.syntax import EntryKeywords, Keywords

from .entry import parse_entry_statement
from .scene import create_node_table, parse_scene_statement


def parse_scene(
    scene_path: str,
    scenes: list[str],
    combats: list[str],
    global_variables: dict[str, Token],
) -> tuple[dict[int, list[Token]], int, dict[str, int]]:

    exception_context = ExceptionContext(scene_path)
    # Create lookup for each line
    line_indexes = {}
    end_line = 0

    with open(scene_path) as story_data:
        for i, line in enumerate(story_data):
            line = line.strip()
            exception_context.line_number = i + 1
            if line == "" or line[:2] == "//":
                continue
            if line.split()[0] not in Keywords:
                if line.split()[0] in EntryKeywords:
                    raise syntax_exception.InvalidKeywordException(
                        exception_context, EntryKeywords(line.split()[0])
                    )
                else:
                    raise syntax_exception.UnknownKeywordException(
                        exception_context, line.split()[0]
                    )
            line_indexes[i + 1] = line

            end_line = max(end_line, i + 1)

    node_table = create_node_table(exception_context, line_indexes)

    # Parse each line
    for line_number, line in line_indexes.items():
        exception_context.line_number = line_number
        statement_parse_context = StatementParseContext(
            exception_context,
            line,
            node_table,
            scenes,
            combats,
            global_variables,
        )
        result = parse_scene_statement(statement_parse_context)

        line_indexes[line_number] = result

    return line_indexes, end_line, node_table


def parse_entry_point(
    entry_path: str,
) -> tuple[list[str], list[str], dict[int, list[Token]]]:
    exception_context = ExceptionContext(entry_path)

    scenes = []
    combats = []
    line_indexes = {}
    global_variable_statements = {}

    with open(entry_path) as story_data:
        for i, line in enumerate(story_data):
            exception_context.line_number = i + 1
            line = line.strip()
            if line == "" or line[:2] == "//":
                continue
            if line.split()[0] in Keywords:
                raise syntax_exception.InvalidKeywordException(
                    exception_context, Keywords(line.split()[0])
                )
            if line.split()[0] not in EntryKeywords:
                raise syntax_exception.UnknownKeywordException(
                    exception_context, line.split()[0]
                )
            line_indexes[i + 1] = line

    for line_number, line in line_indexes.items():
        exception_context.line_number = line_number
        scenes_res, combats_res, result = parse_entry_statement(exception_context, line)
        if scenes_res != [] and scenes != []:
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.SCENE_LIST
            )
        if combats_res != [] and combats != []:
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.COMBAT_LIST
            )
        scenes += scenes_res
        combats += combats_res

        if result != []:
            global_variable_statements[line_number] = result

    for scene in scenes:
        path = os.path.join(os.getcwd(), f"{scene}.txt")
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

    for combat in combats:
        path = os.path.join(os.getcwd(), f"{combat}.txt")
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

    return scenes, combats, global_variable_statements
