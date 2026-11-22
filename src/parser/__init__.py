from collections.abc import Callable
from typing import cast

from exceptions import ExceptionContext, syntax_exception
from model.ast_nodes import EntryFile, SceneFile, StoryNode
from model.ast_nodes.entry import EntryAction, EntryStatement
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.scene import NodeDeclaration, SceneAction, SceneStatement
from model.context import StatementParseContext
from model.story_token import Token
from model.syntax import Namespace
from model.value_types import Types
from parser.entry import parse_entry_statement
from parser.lists import parse_list_statement
from parser.scene import parse_scene_statement

namespace_table: dict[
    Namespace,
    Callable[
        [StatementParseContext],
        EntryAction | ListStatement | SceneAction | NodeDeclaration,
    ],
] = {
    Namespace.ENTRY: parse_entry_statement,
    Namespace.SCENE: parse_scene_statement,
    Namespace.LIST: parse_list_statement,
}


def parse_entry(entry_lines: dict[int, list[Token]], entry_path: str) -> StoryNode:

    exception_context = ExceptionContext(entry_path)
    entry_file = EntryFile([])
    ast_tree = StoryNode(entry_file, [])

    for line_number, line in entry_lines.items():
        exception_context.line_number = line_number
        if line[0].type != Types.KEYWORD:
            raise syntax_exception.UnknownKeywordException(
                exception_context, line[0].value
            )

        assert line[0].namespace, (
            "Internal error: Cannot have a keyword without assigned namespace"
        )

        parse_context = StatementParseContext(exception_context, line, namespace_table)
        statement = EntryStatement(
            cast(EntryAction, namespace_table[line[0].namespace](parse_context))
        )
        statement.set_line_number(line_number)
        entry_file.entry_statements.append(statement)

    entry_file.set_file(entry_path)

    return ast_tree


def parse_scene(
    scene_lines: dict[int, list[Token]], scene_path: str, ast_tree: StoryNode
) -> SceneFile:
    exception_context = ExceptionContext(scene_path)
    scene_file = SceneFile([])
    ast_tree.scene_files.append(scene_file)

    for line_number, line in scene_lines.items():
        exception_context.line_number = line_number
        if line[0].type != Types.KEYWORD:
            raise syntax_exception.UnknownKeywordException(
                exception_context, line[0].value
            )

        if line[0].namespace is None:
            raise RuntimeError(
                "Internal error: Cannot have a keyword without assigned namespace"
            )

        parse_context = StatementParseContext(exception_context, line, namespace_table)
        statement = SceneStatement(
            cast(
                SceneAction | NodeDeclaration,
                namespace_table[line[0].namespace](parse_context),
            )
        )
        statement.set_line_number(line_number)
        scene_file.scene_statements.append(statement)

    scene_file.set_file(scene_path)

    return scene_file
