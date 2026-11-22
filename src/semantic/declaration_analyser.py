from exceptions import ExceptionContext, declaration_exception
from model.ast_nodes import ASTNode
from model.ast_nodes.entry import GlobalDeclaration
from model.ast_nodes.scene import InputStatement, NodeDeclaration, SetStatement
from model.syntax import EntryKeywords, SceneKeywords
from semantic import ASTVisitor


class DeclarationAnalyzer(ASTVisitor):
    def __init__(self, global_variable_table={}) -> None:
        self.global_variable_table: dict[str, list[int]] = global_variable_table
        self.node_table: dict[str, int] = {}
        self.variable_table: dict[str, list[int]] = {}

    def analyse(self, node: ASTNode) -> None:
        self.visit_node(node)

    def visit_globaldeclaration(self, node: GlobalDeclaration):
        if node.target.value in self.global_variable_table:
            assert node.file
            exception_context = ExceptionContext(node.file, node.line_number)
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, EntryKeywords.GLOBAL
            )

        assert node.line_number
        self.global_variable_table.setdefault(node.target.value, []).append(
            node.line_number
        )

    def visit_nodedeclaration(self, node: NodeDeclaration):
        if node.name.value.value in self.node_table:
            assert node.file
            exception_context = ExceptionContext(node.file, node.line_number)
            raise declaration_exception.AlreadyDeclaredException(
                exception_context, SceneKeywords.NODE
            )

        assert node.line_number
        self.node_table[node.name.value.value] = node.line_number

    def visit_inputstatement(self, node: InputStatement):
        assert node.line_number
        self.variable_table.setdefault(node.target.value, []).append(node.line_number)

    def visit_setstatement(self, node: SetStatement):
        assert node.line_number
        self.variable_table.setdefault(node.target.value, []).append(node.line_number)
