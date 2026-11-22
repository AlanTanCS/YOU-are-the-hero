from model.ast_nodes.entry import EntryAction
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.scene import NodeDeclaration, SceneAction
from model.context import StatementExecutionContext
from runtime.entry_keyword_handlers import handle_entry_keyword
from runtime.list_keyword_handlers import handle_list_keyword
from runtime.scene_keyword_handlers import handle_scene_keyword

keyword_handlers = {
    SceneAction: handle_scene_keyword,
    EntryAction: handle_entry_keyword,
    ListStatement: handle_list_keyword,
}


# Node is a special keyword and is handled in semantic analysis when populating the table
def handle_keyword(context: StatementExecutionContext) -> None | int | str:
    if isinstance(context.statement, NodeDeclaration):
        return
    return keyword_handlers[type(context.statement)](context)
