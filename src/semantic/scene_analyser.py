from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.context import StatementSemanticContext

from model.ast_nodes import ASTNode
from semantic import ASTVisitor


class SceneSemanticAnalyser(ASTVisitor):
    def __init__(self, context) -> None:
        self.context: StatementSemanticContext = context

    def analyse(self, node: ASTNode) -> None:
        self.visit_node(node)

    def visit_nodedeclaration(self, node):
        self.context.node_table[node.name.value.value] = node.line_number

    def visit_printstatement(self, node):
        pass

    def visit_inputstatement(self, node):
        pass

    def visit_setstatement(self, node):
        pass

    def visit_conditionalstatement(self, node):
        pass

    def visit_gotostatement(self, node):
        pass

    def visit_entryaction(self, node):
        pass

    def visit_liststatement(self, node):
        pass
