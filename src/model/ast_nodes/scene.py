from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from model.ast_nodes import ASTNode

if TYPE_CHECKING:
    from model.ast_nodes.entry import EntryAction
    from model.ast_nodes.list import ListStatement
    from model.ast_nodes.primatives import Identifier, Name
    from model.ast_nodes.values import Comparison, Value


@dataclass
class SceneStatement(ASTNode):
    statement: NodeDeclaration | SceneAction


@dataclass
class SceneAction(ASTNode):
    action: (
        PrintStatement
        | InputStatement
        | SetStatement
        | ConditionalStatement
        | GotoStatement
        | EntryAction
        | ListStatement
    )


@dataclass
class NodeDeclaration(ASTNode):
    name: Name


@dataclass
class PrintStatement(ASTNode):
    value: Value


@dataclass
class InputStatement(ASTNode):
    identifier: Identifier


@dataclass
class SetStatement(ASTNode):
    identifier: Identifier
    value: Value


@dataclass
class ConditionalStatement(ASTNode):
    comparison: Comparison
    action: SceneAction


class GotoType(StrEnum):
    NODE = "NODE"
    SCENE = "SCENE"
    COMBAT = "COMBAT"


@dataclass
class GotoStatement(ASTNode):
    type: GotoType
    identifier: Identifier
