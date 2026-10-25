from exceptions import ExceptionContext, InvalidTypeException
from syntax import EntryKeywords

def parse_entry_statement(line: str, exception_context: ExceptionContext):
    enum_value = EntryKeywords(line.split()[0])
    
    scene_table = []
    combat_table = []

    if enum_value == EntryKeywords.SCENE_LIST:
        scene_table = parse_scene_combat(line, exception_context)
    if enum_value == EntryKeywords.COMBAT_LIST:
        combat_table = parse_scene_combat(line, exception_context)

    return scene_table, combat_table

def parse_scene_combat(line: str, exception_context: ExceptionContext):
    scene_combat_list = line.split(maxsplit=1)
    if scene_combat_list[1][0] != '[' or scene_combat_list[1][-1] != ']':
        raise InvalidTypeException(exception_context, ["list"])
    scene_combats = scene_combat_list[1][1:-1]
    scene_combats = scene_combats.split(",")
    for scene_combat in range(len(scene_combats)):
        scene_combats[scene_combat] = scene_combats[scene_combat].strip()

    return scene_combats
