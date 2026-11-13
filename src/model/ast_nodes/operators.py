from enum import StrEnum


class ArithmeticOperator(StrEnum):
    ADD = "+"
    SUB = "-"


class ComparisonOperator(StrEnum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"
