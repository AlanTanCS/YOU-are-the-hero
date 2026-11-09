from enum import StrEnum


class SceneKeywords(StrEnum):
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


class ListKeywords(StrEnum):
    GET = "GET"
    SET = "SET"
    INSERT = "INSERT"
    REMOVE = "REMOVE"
    LENGTH = "LENGTH"


class Namespace(StrEnum):
    SCENE = "SCENE"
    ENTRY = "ENTRY"
    GOTO = "GOTO"
    LIST = "LIST"


class ComparisonOperators(StrEnum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"


class ArithmeticOperators(StrEnum):
    ADD = "+"
    SUB = "-"


DEFAULT_NAMESPACES: dict[Namespace, set[Namespace]] = {
    Namespace.SCENE: {Namespace.LIST, Namespace.ENTRY},
    Namespace.ENTRY: {Namespace.LIST, Namespace.SCENE},
    Namespace.GOTO: set(),
    Namespace.LIST: set(),
}

KEYWORD_ENUMS = (
    SceneKeywords,
    EntryKeywords,
    ListKeywords,
)
