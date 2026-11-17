import os

from exceptions import (
    ExceptionContext,
    declaration_exception,
    reference_exception,
    syntax_exception,
)
from model.ast_nodes import EntryFile, StoryNode
from model.ast_nodes.entry import EntryStatement
from model.context import SceneStatementParseContext, StatementParseContext
from model.story_token import Token
from model.syntax import DEFAULT_NAMESPACES, EntryKeywords, Namespace, SceneKeywords
from model.value_types import Types
from parser.tokenise import get_qualified_name, split_statement, strip_qualified_name

from .entry import parse_entry_statement, parse_global
from .lists import parse_list_statement
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
            parse_statement,
        )
        result = parse_statement(statement_parse_context)

        line_indexes[line_number] = result

    return line_indexes, end_line, node_table


namespace_table = {
    Namespace.ENTRY: parse_entry_statement,
    Namespace.SCENE: parse_scene_statement,
    Namespace.LIST: parse_list_statement,
}


def parse_entry_point(entry_lines: dict[int, list[Token]], entry_path: str):

    exception_context = ExceptionContext(entry_path)
    entry_file = EntryFile([])
    ast_tree = StoryNode(entry_file, [])

    for line_number, line in entry_lines.items():
        exception_context.line_number = line_number
        if line[0].type != Types.KEYWORD:
            raise syntax_exception.UnknownKeywordException(
                exception_context, line[0].value
            )

        if line[0].namespace is None:
            raise RuntimeError(
                "Internal error: Cannot have a keyword without assigned namespace"
            )

        parse_context = StatementParseContext(exception_context, line)
        statement = EntryStatement(namespace_table[line[0].namespace](parse_context))
        statement.set_line_number(line_number)
        entry_file.entry_statements.append(statement)

    entry_file.set_file(entry_path)

    return ast_tree


def validate_namespace_children(
    namespaces: list[Namespace], exception_context: ExceptionContext
) -> None:
    prev = namespaces[0]
    for i in namespaces[1:]:
        if i not in DEFAULT_NAMESPACES[prev]:
            raise reference_exception.NamespaceNotFoundException(exception_context, i)
        prev = i


# def parse_statement(statement_parse_context: StatementParseContext) -> list[Token]:
#     keyword = split_statement(statement_parse_context.line)[0]
#     statement_parse_context.namespace += get_qualified_name(
#         statement_parse_context.exception_context, keyword
#     )
#     validate_namespace_children(
#         statement_parse_context.namespace, statement_parse_context.exception_context
#     )

#     if statement_parse_context.namespace[-1] == Namespace.SCENE:
#         if not isinstance(statement_parse_context, SceneStatementParseContext):
#             raise RuntimeError("Internal error, namespace not properly parsed.")
#         statement_parse_context.line = " ".join(
#             [strip_qualified_name(keyword)]
#             + split_statement(statement_parse_context.line)[1:]
#         )
#         return parse_scene_statement(statement_parse_context)

#     if statement_parse_context.namespace[-1] == Namespace.ENTRY:
#         statement_parse_context.line = " ".join(
#             [strip_qualified_name(keyword)]
#             + split_statement(statement_parse_context.line)[1:]
#         )
#         return parse_global(statement_parse_context)

#     if statement_parse_context.namespace[-1] == Namespace.LIST:
#         statement_parse_context.line = " ".join(
#             [strip_qualified_name(keyword)]
#             + split_statement(statement_parse_context.line)[1:]
#         )
#         return parse_list_statement(statement_parse_context)
#     raise RuntimeError("Internal error: namespace not assigned")
