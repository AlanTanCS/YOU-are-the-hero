from collections.abc import Sequence
from dataclasses import dataclass, field

from model.ast_nodes import ASTNode, StoryNode
from model.story_token import Token


@dataclass
class SceneInfo:
    scene_name: str
    statements: Sequence[ASTNode]
    node_table: dict[str, int]
    variable_table: dict[str, ASTNode] = field(default_factory=dict)


class Story:
    def __init__(
        self,
        ast_tree: StoryNode,
        scenes: list[str],
        combats: list[str],
        global_variables: dict[str, ASTNode],
        scene_info: SceneInfo | None = None,
    ) -> None:
        self.ast_tree = ast_tree
        self.scenes = scenes
        self.combats = combats
        self.global_variables = global_variables
        self.scene_info = scene_info
        self.cached_scenes = []

    def get_scene(self, scene: int | str) -> SceneInfo:
        if isinstance(scene, int):
            return self.cached_scenes[scene]
        return self.cached_scenes[self.scenes.index(scene)]
