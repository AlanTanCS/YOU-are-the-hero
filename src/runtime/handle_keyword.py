from model.context import StatementExecutionContext
from model.syntax import Namespace
from runtime.initialise_global_variables import global_init_test

from .scene_keyword_handlers import handle_keyword as handle_scene_keyword

keyword_handlers = {
    Namespace.SCENE: handle_scene_keyword,
    Namespace.ENTRY: global_init_test,
}


def handle_keyword(context: StatementExecutionContext) -> None | int | str:
    # print(context.line)
    if context.keyword.namespace is None:
        raise RuntimeError("Internal Error: Namespace not properly parsed")

    return keyword_handlers[context.keyword.namespace](context)
