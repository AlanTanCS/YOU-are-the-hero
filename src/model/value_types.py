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
    EXPRESSION_START = "<expr_start>"
    EXPRESSION_END = "<expr_end>"
    LIST_START = "<list_start>"
    LIST_END = "<list_end>"
