from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from model.ast_nodes import ASTNode

if TYPE_CHECKING:
    from model.ast_nodes.primatives import Name
    from model.ast_nodes.values import Value


@dataclass
class NameList(ASTNode):
    list: list[Name]


@dataclass
class ListLiteral(ASTNode):
    list: list[Value]
