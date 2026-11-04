from . import ExceptionContext, StoryException, report_error_info


class TypeException(StoryException):
    """Base class for type exceptions raised by YOU-are-the-hero."""


class UnexpectedTypeException(TypeException):
    """Exception raised for unexpected types."""

    def __init__(self, exception_context: ExceptionContext, allowed_types: list[str]):
        result = ""
        if len(allowed_types) > 1:
            result = ", ".join(allowed_types[:-1]) + " or " + allowed_types[-1]
        elif allowed_types:
            result = allowed_types[0]
        self.message = f"Found unexpected type, did not find expected type: {result}"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)


class UnsupportedOperationException(TypeException):
    """Raised when an operator is not supported for the given operand types."""

    def __init__(
        self,
        exception_context: ExceptionContext,
        operation: str,
        lhs_type: str,
        rhs_type: str,
    ):
        self.message = f"Cannot apply '{operation}' to {lhs_type} and {rhs_type}."
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
