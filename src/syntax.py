from enum import Enum

class Keywords(Enum):
    NODE = "NODE"
    PRINT = "PRINT"
    IF = "IF"
    THEN = "THEN"
    GOTO = "GOTO"
    INPUT = "INPUT"
    SET = "SET"

class EntryKeywords(Enum):
    SCENE_LIST = "SCENE_LIST"
    COMBAT_LIST = "COMBAT_LIST"

class ComparisonOperators(Enum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"

class ArithmeticOperators(Enum):
    ADD = "+"
    SUB = "-"
