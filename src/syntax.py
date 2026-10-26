from enum import Enum

class Keywords(Enum):
    NODE = "NODE"
    PRINT = "PRINT"
    IF = "IF"
    THEN = "THEN"
    GOTO = "GOTO"
    INPUT = "INPUT"
    SET = "SET"
    SCENE = "SCENE"
    COMBAT = "COMBAT"

class EntryKeywords(Enum):
    SCENE_LIST = "SCENE_LIST"
    COMBAT_LIST = "COMBAT_LIST"
    GLOBAL = "GLOBAL"

class ComparisonOperators(Enum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"

class ArithmeticOperators(Enum):
    ADD = "+"
    SUB = "-"
