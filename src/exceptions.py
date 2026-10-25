from enum import Enum
import syntax

class ExceptionContext():
    def __init__(self, file_path: str = None, line_number: str = None, line: str = None):
        self.file_path = file_path
        self.line_number = line_number
        self.line = line

class SyntaxException(Exception):
    """Exception raised for syntax errors."""

    def __init__(self, exception_context: ExceptionContext, keyword_type: Enum = None):
        print(type(keyword_type))
        if keyword_type == syntax.Keywords:
            self.message = f"Syntax error at line {exception_context.line_number}, entry syntax not used: {exception_context.line}"
        elif keyword_type == syntax.EntryKeywords:
            self.message = f"Syntax error at line {exception_context.line_number}, scene syntax not used: {exception_context.line}"
        else:
            self.message = f"Syntax error at line {exception_context.line_number}, unrecognised syntax: {exception_context.line}"
        super().__init__(self.message)

class DuplicateNodeException(Exception):
    """Exception raised for duplicate node identifiers."""

    def __init__(self, line_number_first: int, line_number_second: int, node: str):
        self.message = f"Duplicate node identifiers at lines {line_number_first} and {line_number_second}: {node}"
        super().__init__(self.message)

class InvalidTypeException(Exception):
    """Exception raised for invalid types."""

    def __init__(self, exception_context: ExceptionContext, allowed_types: dict):
        result = ""
        if len(allowed_types) > 1:
            result = ", ".join(allowed_types[:-1]) + " or " + allowed_types[-1]
        elif allowed_types:
            result = allowed_types[0]
        self.message = f"Invalid type at line {exception_context.line_number}, expected: {result} at {exception_context.line}"
        super().__init__(self.message)

class InvalidConditionException(Exception):
    """Exception raised for conditions with too many arguements."""

    def __init__(self, line_number: int, line: str, oper_num: int):
        self.message = f"Number of operands and operators {oper_num} does not equal 3 at line {line_number}: {line}"
        super().__init__(self.message)

class InvalidNumberOfArguments(Exception):
    """Exception raised for functions with an invalid number of arguments."""

    def __init__(self, line_number: int, line: str, expected: int):
        self.message = f"Number of arguments does not equal expected number of arguements ({expected}) at line {line_number}: {line}"
        super().__init__(self.message)

class InvalidVariableName(Exception):
    """Exception raised for functions with an invalid variable name."""

    def __init__(self, variable_name: str):
        self.message = f"Variable name must be alphanumeric: \"{variable_name}\" is invalid"
        super().__init__(self.message)

class InvalidExpression(Exception):
    """Exception raised for expressions with an invalid structure."""

    def __init__(self, expression: str):
        self.message = f"Expressions must have closing parethesis: {expression}"
        super().__init__(self.message)

class IllegalTypeOperation(Exception):
    """Exception raised for operations between disagreeing types."""

    def __init__(self, expression: str):
        self.message = f"Failure to determine type: {expression}"
        super().__init__(self.message)

class IllegalStringOperation(Exception):
    """Exception raised for illegal operation on strings."""

    def __init__(self, line_number: int):
        self.message = f"Illegal operation between strings on line {line_number}"
        super().__init__(self.message)

class SetUsedOnNonVariable(Exception):
    """Exception raised for attempt to set a non variable."""

    def __init__(self, line_number: int):
        self.message = f"Cannot use SET on a non-variable at line {line_number}"
        super().__init__(self.message)

class VariableUnset(Exception):
    """Exception raised for attempt to use an unset variable."""

    def __init__(self, line_number: int):
        self.message = f"Cannot use non SET variables at line {line_number}"
        super().__init__(self.message)

class AlreadyDeclared(Exception):
    """Exception raised for attempt to use redeclared something that cannot be decalred again."""

    def __init__(self, exception_context: ExceptionContext, keyword: Enum):
        self.message = f"{keyword.value} already declared, cannot declare a second time at line {exception_context.line_number}: {exception_context.line}"
        super().__init__(self.message)

class LocationNotFound(Exception):
    """Exception raised for when a GOTO is used for a location that doesnt exist."""

    def __init__(self, exception_context: ExceptionContext):
        self.message = f"Cannot find the location referenced on line {exception_context.line_number}: {exception_context.line}"
        super().__init__(self.message)
