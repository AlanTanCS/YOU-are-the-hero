from enum import Enum

class Types(Enum):
    STRING = "<str>"
    INTEGER = "<int>"
    VARIABLE = "<var>"
    KEYWORD = "<keyword>"
    LOCATION = "<location>"
    OPERATOR = "<operator>"
    EXPRESSION_END = "<expr_end>"
    EXPRESSION_START = "<expr_start>"
