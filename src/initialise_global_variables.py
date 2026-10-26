from value_types import Types
from operator_handlers import resolve_expression

def global_init(global_variable_statements: list):
    global_variables = {}
    for statement in global_variable_statements:
        removed_keyword = statement[1:]
        if removed_keyword[0].type != Types.VARIABLE:
            raise #TODO AssignmentOnNonVariable
        if removed_keyword[1].type != Types.EXPRESSION_START:
            global_variables[removed_keyword[0].value] = removed_keyword[1]
        
        # we have an expression
        try:
            result = resolve_expression(removed_keyword[1:], global_variables)
        except TypeError:
            raise #TODO Add exception
        except NameError:
            raise #TODO Add exception
        global_variables[removed_keyword[0].value] = result

    return global_variables