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
    variable_table: dict
    global_variables: dict


@dataclass
class StatementParseContext:
    exception_context: ExceptionContext
    line: str
    line_number: int
    variables: dict
    node_table: dict
    scenes: list
    combats: list
    global_variables: dict
