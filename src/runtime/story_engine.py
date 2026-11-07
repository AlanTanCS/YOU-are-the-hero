import os

from exceptions import ExceptionContext, reference_exception
from model.context import StatementExecutionContext
from model.story import SceneInfo, Story
from model.story_token import Token
from parser import parse_scene
from runtime.handle_keyword import handle_keyword as handle


class StoryEngine:
    def __init__(self, story: Story) -> None:
        self.loc = 0
        self.story = story

    def get_file_scene_info(self, file_name: str) -> SceneInfo:
        file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)

        line_indexes, end_line, node_table = parse_scene(
            file_path,
            self.story.scenes,
            self.story.combats,
            self.story.global_variables,
        )
        scene_info = SceneInfo(line_indexes, end_line, node_table, file_path)
        return scene_info

    def get_current_line_number(self) -> int:
        return self.loc

    def set_current_line_number(self, new_value: int) -> None:
        self.loc = new_value - 1

    def get_current_line(self) -> list[Token]:
        return self.story.get_line(self.loc)

    def get_current_keyword(self) -> Token | None:
        current_line = self.get_current_line()
        if current_line:
            return current_line[0]
        else:
            return None

    def set_new_loc(self, new_loc: int | str) -> None:
        if isinstance(new_loc, int):
            self.set_current_line_number(new_loc)
        else:
            self.set_scene(self.story.get_scene(new_loc))

    def set_scene(self, scene_info: SceneInfo) -> None:
        self.loc = 0
        self.story.scene_info = scene_info

    def handle_keyword(self, keyword: Token | None, line: list[Token]) -> None:
        # keyword will be None if we're looking at a line thats empty
        if keyword is None:
            return

        exception_context = ExceptionContext(
            self.story.get_active_scene().file_path, self.get_current_line_number()
        )
        new_loc = handle(
            StatementExecutionContext(
                exception_context,
                keyword,
                line,
                self.story,
                self.story.get_active_scene().variable_table,
            )
        )
        if new_loc is not None:
            self.set_new_loc(new_loc)

    def next_line(self) -> None | int:
        if self.loc < self.story.get_active_scene().end_line:
            self.loc += 1
        else:
            # End of file
            self.loc = 0
            return -1

    def run_scene(self) -> int:
        while True:
            if self.step() == -1:
                return -1

    def step(self) -> None | int:
        self.handle_keyword(self.get_current_keyword(), self.get_current_line())
        return self.next_line()

    def validate_story(self) -> None:
        self.story.cached_scenes = [
            self.get_file_scene_info(scene) for scene in self.story.scenes
        ]
        if self.story.cached_scenes == []:
            raise reference_exception.ScenesNotFoundException()
        self.story.scene_info = None

    def run(self) -> None:
        self.validate_story()
        # initial scene
        initial_scene = self.story.get_scene(0)
        if isinstance(initial_scene, SceneInfo):
            self.set_scene(initial_scene)
        else:
            self.set_scene(self.get_file_scene_info(initial_scene))

        # execute scene and then move onto next
        while True:
            if self.run_scene() == -1:
                break
