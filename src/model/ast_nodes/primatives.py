from dataclasses import dataclass

from model.ast_nodes import ASTNode


@dataclass
class Identifier(ASTNode):
    value: str


@dataclass
class Name(ASTNode):
    value: Identifier


@dataclass
class Integer(ASTNode):
    value: int


@dataclass
class String(ASTNode):
    value: str
