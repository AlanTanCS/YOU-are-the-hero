class SceneInfo:
    def __init__(self, line_indexes, node_table, variable_table, file_path):
        self.line_indexes = line_indexes
        self.node_table = node_table
        self.variable_table = variable_table
        self.file_path = file_path


class Story:
    def __init__(
        self,
        scenes: list,
        combats: list,
        global_variables: dict,
        scene_info: SceneInfo | None = None,
    ):
        self.scenes = scenes
        self.combats = combats
        self.global_variables = global_variables
        self.scene_info = scene_info
        self.cached_scenes = scenes[::]

    def get_scene(self, scene: int | str) -> SceneInfo:
        if isinstance(scene, int):
            return self.cached_scenes[scene]

        return self.cached_scenes[self.scenes.index(scene)]

    def get_active_scene(self) -> SceneInfo:
        if self.scene_info is None:
            raise RuntimeError("Internal error, no active scene set right now.")
        return self.scene_info

    def get_line(self, line_number: int) -> str:
        return self.get_active_scene().line_indexes.get(line_number)
