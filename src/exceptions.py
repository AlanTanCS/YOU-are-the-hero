from enum import Enum
import linecache
import syntax

class ExceptionContext():
    def __init__(self, file_path: str = None, line_number: str = None, line: str = None):
        self.file_path = file_path
        self.line_number = line_number
        self.line = line

class StoryException(Exception):
    """Base class for exceptions raised by YOU-are-the-hero."""

class SyntaxException(StoryException):
    """Exception raised for syntax errors."""

    def __init__(self, exception_context: ExceptionContext, keyword_type: Enum = None):
        if keyword_type == syntax.Keywords:
            self.message = f"Found scene syntax in the entry file"
        elif keyword_type == syntax.EntryKeywords:
            self.message = f"Found entry syntax in a scene file"
        else:
            self.message = f"Found a syntax error"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)

class DuplicateNodeException(StoryException):
    """Exception raised for duplicate node identifiers."""

    def __init__(self, exception_context: ExceptionContext, line_number_first: int, line_number_second: int, node: str):
        self.message = f"Found duplicated node identifier: {node}"
        exception_context.line_number = None
        self.message += report_error_info(exception_context)
        self.message += f"\nAt lines {line_number_first} and {line_number_second}: ['{get_line(exception_context.file_path, line_number_first)}', '{get_line(exception_context.file_path, line_number_second)}']"
        super().__init__(self.message)

class InvalidTypeException(StoryException):
    """Exception raised for invalid types."""

    def __init__(self, exception_context: ExceptionContext, allowed_types: dict):
        result = ""
        if len(allowed_types) > 1:
            result = ", ".join(allowed_types[:-1]) + " or " + allowed_types[-1]
        elif allowed_types:
            result = allowed_types[0]
        self.message = f"Found unexpected type, did not find expected type: {result}"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)

class InvalidNumberOfArguments(StoryException):
    """Exception raised for functions with an invalid number of arguments."""

    def __init__(self, exception_context: ExceptionContext, expected: int, actual: int):
        self.message = f"Expected {expected} arguements instead got {actual}"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)

class InvalidVariableName(StoryException):
    """Exception raised for functions with an invalid variable name."""

    def __init__(self, exception_context: ExceptionContext, variable_name: str):
        self.message = f"Variable name must be alphanumeric: \"{variable_name}\" is invalid"
        super().__init__(self.message)

class InvalidExpression(StoryException):
    """Exception raised for expressions with an invalid structure."""

    def __init__(self, expression: str):
        self.message = f"Expressions must have closing parethesis: {expression}"
        super().__init__(self.message)

class IllegalTypeOperation(StoryException):
    """Exception raised for operations between disagreeing types."""

    def __init__(self, expression: str):
        self.message = f"Failure to determine type: {expression}"
        super().__init__(self.message)

class IllegalStringOperation(StoryException):
    """Exception raised for illegal operation on strings."""

    def __init__(self, line_number: int):
        self.message = f"Illegal operation between strings on line {line_number}"
        super().__init__(self.message)

class SetUsedOnNonVariable(StoryException):
    """Exception raised for attempt to set a non variable."""

    def __init__(self, line_number: int):
        self.message = f"Cannot use SET on a non-variable at line {line_number}"
        super().__init__(self.message)

class VariableUnset(StoryException):
    """Exception raised for attempt to use an unset variable."""

    def __init__(self, line_number: int):
        self.message = f"Cannot use non SET variables at line {line_number}"
        super().__init__(self.message)

class AlreadyDeclared(StoryException):
    """Exception raised for attempt to use redeclared something that cannot be decalred again."""

    def __init__(self, exception_context: ExceptionContext, keyword: Enum):
        self.message = f"{keyword.value} already declared, cannot declare a second time at line {exception_context.line_number}: {exception_context.line}"
        super().__init__(self.message)

class LocationNotFound(StoryException):
    """Exception raised for when a GOTO is used for a location that doesnt exist."""

    def __init__(self, exception_context: ExceptionContext):
        self.message = f"Cannot find the location referenced on line {exception_context.line_number}: {exception_context.line}"
        super().__init__(self.message)

class RedeclaredGlobal(StoryException):
    """Exception raised for attempt to use redeclared something that cannot be decalred again."""

    def __init__(self, exception_context: ExceptionContext, variable: str):
        self.message = f"Cannot declare global variable '{variable}', cannot declare a pre-existing local variable as GLOBAL on line {exception_context.line_number}: {exception_context.line}"
        super().__init__(self.message)

def get_line(file: str, line_number: int):
    return linecache.getline(file, line_number).strip()

def report_error_info(exception_context: ExceptionContext):
    err_msg = f"\nIn file: {exception_context.file_path}"

    if exception_context.line_number:
        err_msg += f"\nAt line {exception_context.line_number}"

    if exception_context.line_number and exception_context.line:
        err_msg += f": \'{get_line(exception_context.file_path, int(exception_context.line_number))}\'"

    return err_msg
