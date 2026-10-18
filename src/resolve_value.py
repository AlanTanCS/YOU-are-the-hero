from value_types import Types

def resolve_value(variable, variable_table):
    if variable[0] != Types.VARIABLE.value:
        return variable
    return resolve_value(variable_table[" ".join(variable)].split(), variable_table)
