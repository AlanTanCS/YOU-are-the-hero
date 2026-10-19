class SyntaxException(Exception):
    """Exception raised for syntax error scenarios."""

    def __init__(self, line_number: int, line: str):
        self.message = f"Syntax error at line {line_number}, unrecognised syntax: {line}"
        super().__init__(self.message)

class DuplicateNodeException(Exception):
    """Exception raised for duplicate node identifier error scenarios."""

    def __init__(self, line_number_first: int, line_number_second: int, node: str):
        self.message = f"Duplicate node identifiers at lines {line_number_first} and {line_number_second}: {node}"
        super().__init__(self.message)

class InvalidTypeException(Exception):
    """Exception raised for invalid type error scenarios."""

    def __init__(self, line_number: int, line: str):
        self.message = f"Invalid type at line {line_number}: {line}"
        super().__init__(self.message)

class InvalidConditionException(Exception):
    """Exception raised for conditions with too many arguements error scenarios."""

    def __init__(self, line_number: int, line: str, oper_num: int):
        self.message = f"Expected number of operands and operators {oper_num} does not equal 3 at line {line_number}: {line}"
        super().__init__(self.message)

class InvalidNumberOfArguments(Exception):
    """Exception raised for functions with an invalid number of arguments error scenarios."""

    def __init__(self, line_number: int, line: str, arguments: int, expected: int):
        self.message = f"Expected number of arguments {arguments} does not equal expected {expected} at line {line_number}: {line}"
        super().__init__(self.message)

class InvalidVariableName(Exception):
    """Exception raised for functions with an invalid number of arguments error scenarios."""

    def __init__(self, variable_name: str):
        self.message = f"Variable name must be alphanumeric: \"{variable_name}\" is invalid"
        super().__init__(self.message)

class InvalidExpression(Exception):
    """Exception raised for expressions with an invalid structure error scenarios."""

    def __init__(self, expression: str):
        self.message = f"Expressions must have closing parethesis: {expression}"
        super().__init__(self.message)

class IllegalTypeOperation(Exception):
    """Exception raised for operations between disagreeing type error scenarios."""

    def __init__(self, expression: str):
        self.message = f"Failure to determine type: {expression}"
        super().__init__(self.message)

class IllegalStringOperation(Exception):
    """Exception raised for illegal operation on strings error scenarios."""

    def __init__(self, expression: str):
        self.message = f"Illegal operation between strings: {expression}"
        super().__init__(self.message)

class SetUsedOnNonVariable(Exception):
    """Exception raised for attempt to set a non variable error scenarios."""

    def __init__(self, line_number: int):
        self.message = f"Cannot use SET on a non-variable at line {line_number}"
        super().__init__(self.message)

class VariableUnset(Exception):
    """Exception raised for attempt to use an unset variable error scenarios."""

    def __init__(self, line_number: int):
        self.message = f"Cannot use non SET variables at line {line_number}"
        super().__init__(self.message)
