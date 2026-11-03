from . import ExceptionContext, StoryException, report_error_info


class VariableException(StoryException):
    """Base class for variable exceptions raised by YOU-are-the-hero."""


class InvalidVariableNameException(VariableException):
    """Exception raised for functions with an invalid variable name."""

    def __init__(self, exception_context: ExceptionContext, variable_name: str):
        self.message = (
            f'Variable name must be alphanumeric: "{variable_name}" is invalid'
        )
        self.message += report_error_info(exception_context)
        super().__init__(self.message)


class VariableNotSetException(VariableException):
    """Exception raised for attempt to use a variable that hasn't been assigned a value."""

    def __init__(self, exception_context: int, variable: str):
        self.message = f"Variable '{variable}' has not been assigned a value"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)


class InvalidAssignmentTargetException(VariableException):
    """Exception raised for attempt to set a non variable type."""

    def __init__(self, exception_context: int):
        self.message = f"Assignment target must be a valid variable"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
