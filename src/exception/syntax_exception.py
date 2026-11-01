from . import ExceptionContext, StoryException, report_error_info
from enum import Enum
import syntax


class SyntaxException(StoryException):
    """Base class for syntax exceptions raised by YOU-are-the-hero."""


class InvalidKeyword(SyntaxException):
    """Exception raised when an invalid keyword is found"""

    def __init__(self, exception_context: ExceptionContext, keyword_type: Enum = None):
        if keyword_type == syntax.Keywords:
            self.message = "Found a keyword for scenes in the entry file"
        elif keyword_type == syntax.EntryKeywords:
            self.message = "Found a keyword for entry in a scene file"
        else:
            self.message = "Found an invalid keyword"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)

class InvalidExpression(SyntaxException):
    """Exception raised there is an invalid expression."""

    def __init__(self, exception_context: ExceptionContext, keyword_type: Enum = None):
        if keyword_type == syntax.Keywords:
            self.message = "Found a keyword for scenes in the entry file"
        elif keyword_type == syntax.EntryKeywords:
            self.message = "Found a keyword for entry in a scene file"
        else:
            self.message = "Found an invalid keyword"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
