from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from model.ast_nodes import ASTNode

if TYPE_CHECKING:
    from model.ast_nodes.collections import ListLiteral
    from model.ast_nodes.list import ListGet, ListLength
    from model.ast_nodes.operators import ComparisonOperator
    from model.ast_nodes.primatives import Identifier, Integer, String


@dataclass
class Function(ASTNode):
    function: ListGet | ListLength


@dataclass
class Expression(ASTNode):
    value: ExpressionValue | BinaryExpression | None


class ArithmeticOperator(StrEnum):
    ADD = "+"
    SUB = "-"


@dataclass
class BinaryExpression(ASTNode):
    left: ExpressionValue
    operator: ArithmeticOperator
    right: ExpressionValue


@dataclass
class ExpressionValue(ASTNode):
    value: String | Integer | Identifier | Expression | Function


@dataclass
class Value(ASTNode):
    value: String | Integer | Identifier | ListLiteral | Expression


@dataclass
class Comparison(ASTNode):
    left: Value
    operator: ComparisonOperator
    right: Value
