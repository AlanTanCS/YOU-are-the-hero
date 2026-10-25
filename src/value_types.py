from enum import Enum

class Types(Enum):
    STRING = "<str>"
    INTEGER = "<int>"
    VARIABLE = "<var>"
    KEYWORD = "<keyword>"
    LOCATION = "<location>"
    ARITHMETIC_OPERATOR = "<arithmetic_operator>"
    COMPARISON_OPERATOR = "<comparison_operator>"
    EXPRESSION_END = "<expr_end>"
    EXPRESSION_START = "<expr_start>"
