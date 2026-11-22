from dataclasses import fields, is_dataclass

from model.ast_nodes import ASTNode


class ASTVisitor:
    def visit_node(self, node: ASTNode):
        method = getattr(self, f"visit_{type(node).__name__.lower()}", self.traverse)
        # return method
        if method is not None:
            return method(node)

    def traverse(self, node: ASTNode):
        if not is_dataclass(node):
            return
        for field in fields(node):
            value = getattr(node, field.name)

            if isinstance(value, list):
                for item in value:
                    self.visit_node(item)

            elif isinstance(value, ASTNode):
                self.visit_node(value)
