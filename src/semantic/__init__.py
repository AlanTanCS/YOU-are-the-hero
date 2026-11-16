from dataclasses import fields

from model.ast_nodes import ASTNode


class ASTVisitor:
    def visit_node(self, node: ASTNode):
        method_name = f"visit_{type(node).__name__.lower()}"
        # print(method_name)
        method = getattr(self, method_name, self.traverse(node))
        # return method
        if method is not None:
            return method(node)

    def traverse(self, node):
        for field in fields(node):
            value = getattr(node, field.name)

            if isinstance(value, list):
                for item in value:
                    self.visit_node(item)

            elif isinstance(value, ASTNode):
                self.visit_node(value)
