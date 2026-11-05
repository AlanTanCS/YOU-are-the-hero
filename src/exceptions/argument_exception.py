from . import ExceptionContext, StoryException, report_error_info


class ArgumentException(StoryException):
    """Base class for argument exceptions raised by YOU-are-the-hero."""


class InvalidNumberOfArgumentsException(ArgumentException):
    """Exception raised for functions with an invalid number of arguments."""

    def __init__(
        self, exception_context: ExceptionContext, expected: int, actual: int
    ) -> None:
        self.message = f"Expected {expected} arguments instead got {actual}"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
