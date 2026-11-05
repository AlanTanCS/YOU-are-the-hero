from dataclasses import dataclass

from exceptions import ExceptionContext
from model.story import Story

from .story_token import Token


@dataclass
class StatementExecutionContext:
    exception_context: ExceptionContext
    keyword: Token
    line: list[Token]
    story: Story
    variable_table: dict[str, Token]
    global_variables: dict[str, Token]


@dataclass
class StatementParseContext:
    exception_context: ExceptionContext
    line: str
    node_table: dict[str, int]
    scenes: list[str]
    combats: list[str]
    global_variables: dict[str, Token]
