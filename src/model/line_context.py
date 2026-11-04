from dataclasses import dataclass

from exceptions import ExceptionContext
from model.story import Story

from .story_token import Token


@dataclass
class LineContext:
    exception_context: ExceptionContext
    keyword: Token
    line: list[Token]
    story: Story
    variable_table: dict
    global_variables: dict
