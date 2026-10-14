from enum import Enum

class Keywords(Enum):
    NODE = "NODE"
    PRINT = "PRINT"
    IF = "IF"
    THEN = "THEN"
    GOTO = "GOTO"
    INPUT = "INPUT"

class ComparisonOperators(Enum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"
