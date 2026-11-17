import os

from exceptions import ExceptionContext, declaration_exception
from model.ast_nodes.entry import GlobalDeclaration, SceneList
from model.syntax import EntryKeywords
from semantic import ASTVisitor


class EntrySemanticAnalyser(ASTVisitor):
    def __init__(self) -> None:
        self.global_variable_table = {}
        self.scene_list = []
        self.combat_list = []

    def analyse(self, node) -> None:
        self.visit_node(node)

    def visit_globaldeclaration(self, node: GlobalDeclaration) -> None:
        self.global_variable_table[node.target.value] = node.source.value

    def visit_scenelist(self, node: SceneList) -> None:
        if node.file is None:
            raise RuntimeError(
                "Internal error: We have lost track of the file were on."
            )
        exception_context = ExceptionContext(node.file, node.line_number)
        if self.scene_list != []:
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.SCENE_LIST
            )

        for scene in range(len(node.list.list)):
            self.scene_list.append(node.list.list[scene].value.value)
            self.verify_files(node.list.list[scene].value.value)

    def visit_combatlist(self, node) -> None:
        if node.file is None:
            raise RuntimeError(
                "Internal error: We have lost track of the file were on."
            )
        exception_context = ExceptionContext(node.file, node.line_number)
        if self.combat_list != []:
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.SCENE_LIST
            )

        for scene in range(len(node.list.list)):
            self.combat_list.append(node.list.list[scene].value.value)
            self.verify_files(node.list.list[scene].value.value)

    def verify_files(self, file_name):
        file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
