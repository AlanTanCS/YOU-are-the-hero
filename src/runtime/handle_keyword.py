from model.context import StatementExecutionContext
from model.syntax import Namespace
from runtime.entry_keyword_handlers import handle_global
from runtime.list_keyword_handlers import handle_keyword as handle_list_keyword

from .scene_keyword_handlers import handle_keyword as handle_scene_keyword

keyword_handlers = {
    Namespace.SCENE: handle_scene_keyword,
    Namespace.ENTRY: handle_global,
    Namespace.LIST: handle_list_keyword,
}


def handle_keyword(context: StatementExecutionContext) -> None | int | str:
    if context.keyword.namespace is None:
        raise RuntimeError("Internal Error: Namespace not properly parsed")

    return keyword_handlers[context.keyword.namespace](context)
