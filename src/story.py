class SceneInfo():
    def __init__(self, line_indexes, node_table, variable_table):
        self.line_indexes = line_indexes
        self.node_table = node_table
        self.variable_table = variable_table

class Story():
    def __init__(self, scenes: dict, combats: dict, scene_info: SceneInfo = None):
        self.scenes = scenes
        self.combats = combats
        self.scene_info = scene_info
        self.cached_scenes = scenes

    def get_scene(self, scene_number):
        return self.cached_scenes[scene_number]

    def get_line(self, line_number: int) -> str | None:
        return self.scene_info.line_indexes.get(line_number)
