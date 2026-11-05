from enum import Enum

from model import syntax

from . import ExceptionContext, StoryException, report_error_info


class SyntaxException(StoryException):
    """Base class for syntax exceptions raised by YOU-are-the-hero."""


class UnknownKeywordException(SyntaxException):
    """Exception raised when an invalid keyword is found"""

    def __init__(self, exception_context: ExceptionContext, unknown_word: str) -> None:
        self.message = f"Could not find a matching keyword for '{unknown_word}'"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)


class InvalidKeywordException(SyntaxException):
    """Exception raised when an invalid keyword is found"""

    def __init__(self, exception_context: ExceptionContext, keyword_used: Enum) -> None:
        if keyword_used == syntax.Keywords:
            # self.message = "Found a keyword for scenes in the entry file"
            self.message = f"Keyword '{keyword_used}' was found in the entry file and is only allowed in scenes"
        elif keyword_used == syntax.EntryKeywords:
            self.message = f"Keyword '{keyword_used}' was found in a scene file and is only allowed in the entry file"
        else:
            self.message = f"Keyword '{keyword_used}' is not allowed in this context"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)


class MissingKeywordException(SyntaxException):
    """Exception raised for when a keyword is expected but not found."""

    def __init__(
        self, exception_context: ExceptionContext, keyword: syntax.Keywords
    ) -> None:
        self.message = f"Expected keyword: '{keyword}' but could not find '{keyword}'"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)


class InvalidExpressionException(SyntaxException):
    """Exception raised for expressions with an invalid structure."""

    def __init__(self, exception_context: ExceptionContext) -> None:
        self.message = "All expressions must have a closing parenthesis"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
