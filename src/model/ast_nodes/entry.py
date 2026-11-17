from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from model.ast_nodes import ASTNode

if TYPE_CHECKING:
    from model.ast_nodes.collections import NameList
    from model.ast_nodes.listnodes import ListStatement
    from model.ast_nodes.primatives import Identifier
    from model.ast_nodes.scene import SceneAction
    from model.ast_nodes.values import Value


@dataclass
class EntryStatement(ASTNode):
    statement: EntryAction


@dataclass
class EntryAction(ASTNode):
    action: SceneList | CombatList | GlobalDeclaration | SceneAction | ListStatement


@dataclass
class SceneList(ASTNode):
    list: NameList


@dataclass
class CombatList(ASTNode):
    list: NameList


@dataclass
class GlobalDeclaration(ASTNode):
    target: Identifier
    source: Value
