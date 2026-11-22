from __future__ import annotations

import os
from typing import TYPE_CHECKING

from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.scene import SceneAction

if TYPE_CHECKING:
    from model.context import StatementSemanticContext
from exceptions import ExceptionContext, declaration_exception
from model.ast_nodes import EntryFile
from model.ast_nodes.entry import CombatList, EntryAction, GlobalDeclaration, SceneList
from model.syntax import EntryKeywords
from semantic import ASTVisitor


class EntrySemanticAnalyser(ASTVisitor):
    def __init__(self, context: StatementSemanticContext) -> None:
        self.context: StatementSemanticContext = context

    def analyse(self, node: EntryFile) -> None:
        self.visit_node(node)

    def analyse_action(self, action: EntryAction) -> None:
        self.visit_node(action)

    def visit_globaldeclaration(self, node: GlobalDeclaration) -> None:
        # TODO
        # print("asoidjaoisjdoiasdji")
        pass
        # self.global_variable_table[node.target.value] = node.source.value

    def visit_sceneaction(self, node: SceneAction) -> None:
        assert self.context.dispatcher, (
            "Internal error: Dispatcher has not been assigned"
        )
        self.context.dispatcher.analyse_scene_action(node)

    def visit_liststatement(self, node: ListStatement) -> None:
        pass

    def visit_scenelist(self, node: SceneList) -> None:
        assert node.file, "Internal error: We have lost track of the file were on."
        exception_context = ExceptionContext(node.file, node.line_number)
        if self.context.scene_list != []:
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.SCENE_LIST
            )

        for scene in range(len(node.list.list)):
            self.context.scene_list.append(node.list.list[scene].value.value)
            self.verify_files(node.list.list[scene].value.value)

    def visit_combatlist(self, node: CombatList) -> None:
        assert node.file, "Internal error: We have lost track of the file were on."
        exception_context = ExceptionContext(node.file, node.line_number)
        if self.context.combat_list != []:
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.SCENE_LIST
            )

        for scene in range(len(node.list.list)):
            self.context.combat_list.append(node.list.list[scene].value.value)
            self.verify_files(node.list.list[scene].value.value)

    def verify_files(self, file_name: str):
        file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
