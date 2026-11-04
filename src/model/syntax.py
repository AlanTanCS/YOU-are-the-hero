from enum import StrEnum


class Keywords(StrEnum):
    PRINT = "PRINT"
    IF = "IF"
    THEN = "THEN"
    GOTO = "GOTO"
    INPUT = "INPUT"
    SET = "SET"
    NODE = "NODE"
    SCENE = "SCENE"
    COMBAT = "COMBAT"


class EntryKeywords(StrEnum):
    SCENE_LIST = "SCENE_LIST"
    COMBAT_LIST = "COMBAT_LIST"
    GLOBAL = "GLOBAL"


class ComparisonOperators(StrEnum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"


class ArithmeticOperators(StrEnum):
    ADD = "+"
    SUB = "-"
