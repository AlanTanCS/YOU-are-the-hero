from enum import Enum

class Keywords(Enum):
    NODE = "NODE"
    PRINT = "PRINT"
    IF = "IF"
    THEN = "THEN"
    GOTO = "GOTO"
    INPUT = "INPUT"
    SET = "SET"

class ComparisonOperators(Enum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"

class ArithmeticOperators(Enum):
    ADD = "+"
    SUB = "-"
