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
