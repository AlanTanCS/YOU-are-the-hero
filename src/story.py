from typing import overload

class SceneInfo():
    def __init__(self, line_indexes, node_table, variable_table):
        self.line_indexes = line_indexes
        self.node_table = node_table
        self.variable_table = variable_table

class Story():
    def __init__(self, scenes: list, combats: list, global_variables: dict, scene_info: SceneInfo = None):
        self.scenes = scenes
        self.combats = combats
        self.global_variables = global_variables
        self.scene_info = scene_info
        self.cached_scenes = scenes[::]

    @overload
    def get_scene(self, scene_number: int) -> SceneInfo:
        ...

    @overload
    def get_scene(self, scene_name: str) -> SceneInfo:
        ...

    def get_scene(self, scene: int | str) -> SceneInfo:
        if isinstance(scene, int):
            return self.cached_scenes[scene]

        return self.cached_scenes[self.scenes.index(scene)]

    def get_line(self, line_number: int) -> str | None:
        return self.scene_info.line_indexes.get(line_number)
