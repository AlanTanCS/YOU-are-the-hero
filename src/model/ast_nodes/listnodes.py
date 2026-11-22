from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from model.ast_nodes import ASTNode

if TYPE_CHECKING:
    from model.ast_nodes.collections import ListLiteral
    from model.ast_nodes.primatives import Identifier, Integer
    from model.ast_nodes.values import Expression, Value


@dataclass
class ListStatement(ASTNode):
    statement: ListGet | ListSet | ListInsert | ListRemove | ListLength


@dataclass
class ListIndex(ASTNode):
    index: Integer | Expression | Identifier


@dataclass
class ListGet(ASTNode):
    identifier: Identifier | ListLiteral
    index: ListIndex


@dataclass
class ListSet(ASTNode):
    target: Identifier | ListLiteral
    index: ListIndex
    source: Value


@dataclass
class ListInsert(ASTNode):
    target: Identifier | ListLiteral
    index: ListIndex
    source: Value


@dataclass
class ListRemove(ASTNode):
    target: Identifier | ListLiteral
    index: ListIndex


@dataclass
class ListLength(ASTNode):
    identifier: Identifier | ListLiteral
