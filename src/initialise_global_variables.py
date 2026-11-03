from exceptions import ExceptionContext, variable_exception
from value_types import Types
from operator_handlers import resolve_expression

def global_init(global_variable_statements: dict, entry_file: str):
    global_variables = {}
    for line_number, statement in global_variable_statements.items():
        exception_context = ExceptionContext(entry_file, line_number)
        removed_keyword = statement[1:]
        if removed_keyword[0].type != Types.VARIABLE:
            raise variable_exception.InvalidAssignmentTargetException(exception_context)
        if removed_keyword[1].type != Types.EXPRESSION_START:
            global_variables[removed_keyword[0].value] = removed_keyword[1]
        
        global_variables[removed_keyword[0].value] = resolve_expression(removed_keyword[1:], global_variables, exception_context)

    return global_variables
