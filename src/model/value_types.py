from enum import StrEnum


class Types(StrEnum):
    STRING = "<str>"
    INTEGER = "<int>"
    VARIABLE = "<var>"
    GLOBAL_VARIABLE = "<global_var>"
    KEYWORD = "<keyword>"
    LOCATION = "<location>"
    ARITHMETIC_OPERATOR = "<arithmetic_operator>"
    COMPARISON_OPERATOR = "<comparison_operator>"
    EXPRESSION_END = "<expr_end>"
    EXPRESSION_START = "<expr_start>"
