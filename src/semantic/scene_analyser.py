from __future__ import annotations

from typing import TYPE_CHECKING

from model.ast_nodes.scene import SceneAction

if TYPE_CHECKING:
    from model.context import StatementSemanticContext

from model.ast_nodes import SceneFile
from semantic import ASTVisitor


class SceneSemanticAnalyser(ASTVisitor):
    def __init__(self, context) -> None:
        self.context: StatementSemanticContext = context

    def analyse(self, node: list[SceneFile]) -> None:
        for scene in node:
            self.visit_node(scene)

    def analyse_action(self, action: SceneAction) -> None:
        self.visit_node(action)

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
