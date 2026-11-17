from model.ast_nodes.entry import EntryStatement
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.scene import SceneStatement
from model.context import StatementExecutionContext
from runtime.entry_keyword_handlers import handle_entry_keyword
from runtime.list_keyword_handlers import handle_keyword as handle_list_keyword

from .scene_keyword_handlers import handle_keyword as handle_scene_keyword

keyword_handlers = {
    SceneStatement: handle_scene_keyword,
    EntryStatement: handle_entry_keyword,
    ListStatement: handle_list_keyword,
}


def handle_keyword(context: StatementExecutionContext) -> None | int | str:
    return keyword_handlers[type(context.statement)](context)
