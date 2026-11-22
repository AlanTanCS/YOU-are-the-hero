from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from exceptions import ExceptionContext
from model.ast_nodes import ASTNode
from model.ast_nodes.entry import EntryAction
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.scene import NodeDeclaration, SceneAction
from model.story import Story
from model.syntax import Namespace
from semantic.dispatcher import SemanticDispatcher

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


@dataclass
class StatementSemanticContext:
    global_declarations: dict[str, list[int]] = field(default_factory=dict)
    scene_list: list[str] = field(default_factory=list)
    combat_list: list[str] = field(default_factory=list)
    global_variable_table: dict[str, ASTNode] = field(default_factory=dict)
    dispatcher: SemanticDispatcher | None = None
