from exceptions import ExceptionContext, declaration_exception
from model.ast_nodes.entry import GlobalDeclaration, SceneList
from model.syntax import EntryKeywords
from semantic import ASTVisitor


class EntrySemanticAnalyser(ASTVisitor):
    def __init__(self) -> None:
        self.global_variable_table = {}
        self.scene_list = {}
        self.combat_list = {}

    def analyse(self, node):
        self.visit_node(node)

    def visit_globaldeclaration(self, node: GlobalDeclaration):
        self.global_variable_table[node.identifier.value] = node.value.value

    def visit_scenelist(self, node: SceneList):
        exception_context = ExceptionContext(node.file, node.line_number)
        if self.scene_list != {}:
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.SCENE_LIST
            )
        self.scene_list = node.list.list

    def visit_combatlist(self, node):
        print(node)
