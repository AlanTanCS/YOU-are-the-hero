from enum import Enum

from . import ExceptionContext, StoryException, get_line, report_error_info


class DeclarationException(StoryException):
    """Base class for declaration exceptions raised by YOU-are-the-hero."""


class DuplicateNodeException(DeclarationException):
    """Exception raised for duplicate node identifiers."""

    def __init__(
        self,
        exception_context: ExceptionContext,
        line_number_first: int,
        line_number_second: int,
        node: str,
    ) -> None:
        self.message = f"Found duplicated node identifier: {node}"
        exception_context.line_number = None
        self.message += report_error_info(exception_context)
        self.message += f"\nAt lines {line_number_first} and {line_number_second}: ['{get_line(exception_context.file_path, line_number_first)}', '{get_line(exception_context.file_path, line_number_second)}']"
        super().__init__(self.message)


class AlreadyDeclaredException(DeclarationException):
    """Exception raised for attempt to redeclare something that may only be declared once."""

    def __init__(self, exception_context: ExceptionContext, keyword: Enum) -> None:
        self.message = f"Cannot redeclare {keyword} more than once"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
