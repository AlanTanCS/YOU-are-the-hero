import os

from exceptions import (
    ExceptionContext,
    declaration_exception,
    reference_exception,
    syntax_exception,
)
from model.context import SceneStatementParseContext, StatementParseContext
from model.story_token import Token
from model.syntax import EntryKeywords, Namespace, SceneKeywords
from parser.tokenise import get_qualified_name, split_statement, strip_qualified_name

from .entry import parse_global, parse_scene_combat
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

            keyword = line.split()[0]
            namespace = keyword.split(".")[0]

            if keyword not in SceneKeywords and namespace not in Namespace:
                if keyword in EntryKeywords:
                    raise syntax_exception.InvalidKeywordException(
                        exception_context, EntryKeywords(keyword)
                    )
                else:
                    raise syntax_exception.UnknownKeywordException(
                        exception_context, keyword
                    )
            line_indexes[i + 1] = line

            end_line = max(end_line, i + 1)

    node_table = create_node_table(exception_context, line_indexes)

    # Parse each line
    for line_number, line in line_indexes.items():
        exception_context.line_number = line_number
        statement_parse_context = SceneStatementParseContext(
            exception_context,
            line,
            [Namespace.SCENE],
            scenes,
            combats,
            node_table,
            global_variables,
        )
        result = parse_statement(statement_parse_context)

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
            if line.split()[0] in SceneKeywords:
                raise syntax_exception.InvalidKeywordException(
                    exception_context, SceneKeywords(line.split()[0])
                )
            if line.split()[0] not in EntryKeywords:
                raise syntax_exception.UnknownKeywordException(
                    exception_context, line.split()[0]
                )
            line_indexes[i + 1] = line

    for line_number, line in line_indexes.items():
        exception_context.line_number = line_number
        enum_value = EntryKeywords(line.split()[0])
        scenes_res, combats_res, result = [], [], []
        if enum_value == EntryKeywords.SCENE_LIST:
            scenes_res = parse_scene_combat(exception_context, line)
        if enum_value == EntryKeywords.COMBAT_LIST:
            combats_res = parse_scene_combat(exception_context, line)
        if enum_value == EntryKeywords.GLOBAL:
            context = StatementParseContext(exception_context, line, [Namespace.ENTRY])
            result = parse_statement(context)

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


VALID_CHILDREN: dict[Namespace, set[Namespace]] = {
    Namespace.SCENE: {Namespace.LIST, Namespace.ENTRY},
    Namespace.ENTRY: {Namespace.LIST, Namespace.SCENE},
    Namespace.GOTO: set(),
    Namespace.LIST: set(),
}


def validate_namespace_children(
    namespaces: list[Namespace], exception_context: ExceptionContext
):
    prev = namespaces[0]
    for i in namespaces[1:]:
        if i not in VALID_CHILDREN[prev]:
            raise reference_exception.NamespaceNotFoundException(exception_context, i)
        prev = i


def parse_statement(statement_parse_context: StatementParseContext):
    keyword = split_statement(statement_parse_context.line)[0]
    statement_parse_context.namespace += get_qualified_name(
        statement_parse_context.exception_context, keyword
    )
    validate_namespace_children(
        statement_parse_context.namespace, statement_parse_context.exception_context
    )

    if statement_parse_context.namespace[-1] == Namespace.SCENE:
        if not isinstance(statement_parse_context, SceneStatementParseContext):
            raise RuntimeError("Internal error, namespace not properly parsed.")
        statement_parse_context.line = " ".join(
            [strip_qualified_name(keyword)]
            + split_statement(statement_parse_context.line)[1:]
        )
        return parse_scene_statement(statement_parse_context)

    if statement_parse_context.namespace[-1] == Namespace.ENTRY:
        statement_parse_context.line = " ".join(
            [strip_qualified_name(keyword)]
            + split_statement(statement_parse_context.line)[1:]
        )
        return parse_global(statement_parse_context)

    if statement_parse_context.namespace[-1] == Namespace.LIST:
        # print("LIST NAMESPACE")
        pass
