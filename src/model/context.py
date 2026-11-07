from dataclasses import dataclass

from exceptions import ExceptionContext
from model.story import Story
from model.syntax import Namespace

from .story_token import Token


@dataclass
class StatementExecutionContext:
    exception_context: ExceptionContext
    keyword: Token
    line: list[Token]
    story: Story
    variable_table: dict[str, Token]


@dataclass
class StatementParseContext:
    exception_context: ExceptionContext
    line: str
    namespace: list[Namespace]


@dataclass
class SceneStatementParseContext(StatementParseContext):
    scenes: list[str]
    combats: list[str]
    node_table: dict[str, int]
    global_variables: dict[str, Token]
