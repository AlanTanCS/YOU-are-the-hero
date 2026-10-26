from exceptions import ExceptionContext, SyntaxException, AlreadyDeclared
from syntax import Keywords, EntryKeywords
from .scene import parse_scene_statement, create_node_table
from .entry import parse_entry_statement

import os

def parse_scene(scene_path: str, scenes: list, combats: list, global_variables: dict):

    exception_context = ExceptionContext(scene_path)
    # Create lookup for each line
    line_indexes = {}
    line_indexes["EOF"] = 0

    variables = {}

    with open(scene_path) as story_data:
        for i, line in enumerate(story_data):
            line = line.strip()
            exception_context.line_number = i + 1
            exception_context.line = line
            if line == '' or line[:2] == "//":
                continue
            if line.split()[0] not in Keywords:
                raise SyntaxException(exception_context)
            line_indexes[i] = line
        
            line_indexes["EOF"] = max(line_indexes["EOF"], i) 


    node_table = create_node_table(line_indexes)

    # Parse each line
    for line_number, line in line_indexes.items():
        if line_number == "EOF":
            continue
        exception_context.line_number, exception_context.line = line_number + 1, line
        result = parse_scene_statement(line, line_number, variables, node_table, exception_context, scenes, combats, global_variables)

        line_indexes[line_number] = result

    return line_indexes, node_table, variables

def parse_entry_point(entry_path: str):
    exception_context = ExceptionContext(entry_path)

    scenes = []
    combats = []
    line_indexes = {}
    global_variable_statements = []

    with open(entry_path) as story_data:
        for i, line in enumerate(story_data):
            exception_context.line_number, exception_context.line = i + 1, line
            line = line.strip()
            if line == '' or line[:2] == "//":
                continue
            if line.split()[0] in Keywords:
                exception_context.line = line
                raise SyntaxException(exception_context, Keywords)
            if line.split()[0] not in EntryKeywords:
                raise SyntaxException(exception_context)
            line_indexes[i] = line

    for line_number, line in line_indexes.items():
        exception_context.line_number, exception_context.line = line_number + 1, line
        scenes_res, combats_res, result = parse_entry_statement(line, exception_context)
        if scenes_res != [] and scenes != []:
            raise AlreadyDeclared(exception_context, EntryKeywords.SCENE_LIST)
        if combats_res != [] and combats != []:
            raise AlreadyDeclared(exception_context, EntryKeywords.COMBAT_LIST)
        scenes += scenes_res
        combats += combats_res

        if result:
            global_variable_statements.append(result)

    for scene in scenes:
        path = os.path.join(os.getcwd(), f"{scene}.txt")
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

    for combat in combats:
        path = os.path.join(os.getcwd(), f"{combat}.txt")
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

    return scenes, combats, global_variable_statements
