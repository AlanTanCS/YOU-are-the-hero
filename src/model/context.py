from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from exceptions import ExceptionContext
from model.ast_nodes import ASTNode
from model.ast_nodes.entry import EntryAction
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.scene import NodeDeclaration, SceneAction
from model.story import Story
from model.syntax import Namespace

from .story_token import Token

T = TypeVar("T", bound=ASTNode)


@dataclass
class StatementExecutionContext(Generic[T]):
    exception_context: ExceptionContext
    story: Story
    statement: T
    dispatch: Callable[[StatementExecutionContext], None | int | str] | None = None


@dataclass
class StatementParseContext:
    exception_context: ExceptionContext
    line: list[Token]
    dispatch: dict[
        Namespace,
        Callable[
            [StatementParseContext],
            EntryAction | ListStatement | SceneAction | NodeDeclaration,
        ],
    ]


# @dataclass
# class SceneStatementParseContext(StatementParseContext):
#     scenes: list[str]
#     combats: list[str]
#     node_table: dict[str, int]
#     global_variables: dict[str, Token]
#     dispatch: Callable[["StatementParseContext"], list[Token]] | None = None
