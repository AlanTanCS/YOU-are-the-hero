from collections.abc import Sequence
from dataclasses import dataclass, field

from model.ast_nodes import ASTNode, StoryNode
from model.ast_nodes.entry import EntryStatement
from model.ast_nodes.primatives import Name
from model.ast_nodes.scene import SceneStatement
from model.story_token import Token


@dataclass
class SceneInfo:
    line_indexes: Sequence[SceneStatement | EntryStatement]
    node_table: dict[str, int]
    file_path: str | None
    variable_table: dict[str, Token] = field(default_factory=dict)


class Story:
    def __init__(
        self,
        tree: StoryNode,
        scenes: list[Name],
        combats: list[Name],
        global_variables: dict[str, ASTNode],
        scene_info: SceneInfo | None = None,
    ) -> None:
        self.tree = tree
        self.scenes = scenes
        self.combats = combats
        self.global_variables = global_variables
        self.scene_info = scene_info
        self.cached_scenes = []

    def get_scene(self, scene: int | str) -> SceneInfo:
        if isinstance(scene, int):
            return self.cached_scenes[scene]
        print(self.scenes.index(scene))
        return self.cached_scenes[self.scenes.index(scene)]

    def get_active_scene(self) -> SceneInfo:
        if self.scene_info is None:
            raise RuntimeError("Internal error, no active scene set right now.")
        return self.scene_info

    def get_line(self, line_number: int) -> list[Token]:
        return self.get_active_scene().line_indexes.get(line_number, [])
