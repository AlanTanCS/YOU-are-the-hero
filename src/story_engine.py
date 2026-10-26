from keyword_handlers import handle_keyword as handle
from line_context import LineContext
from parser import parse_scene
from story import Story, SceneInfo

import os

class StoryEngine:
    def __init__ (self, story: Story):
        self.loc = 0
        self.story = story
        self.global_variables = {}

    def get_file_scene_info(self, file_name: str):
        file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)

        line_indexes, node_table, variable_table = parse_scene(file_path, self.story.scenes, self.story.combats)
        scene_info = SceneInfo(line_indexes, node_table, variable_table)
        return scene_info

    def get_current_line_number(self) -> int:
        return self.loc + 1

    def set_current_line_number(self, new_value: int) -> None:
        self.loc = new_value - 1

    def get_current_line(self) -> str | None:
        return self.story.get_line(self.loc)
    
    def get_current_keyword(self) -> str:
        current_line = self.get_current_line()
        if current_line:
            return current_line[0]
        else:
            return None

    def set_new_loc(self, new_loc):
        if isinstance(new_loc, int):
            self.set_current_line_number(new_loc)
            return
        else:
            self.set_scene(self.story.get_scene(new_loc))

    def set_scene(self, scene_info):
        self.loc = 0
        self.story.scene_info = scene_info

    def handle_keyword(self, keyword: str, line: str) -> None:
        # keyword will be None if we're looking at a line thats empty
        if keyword:
            new_loc = handle(LineContext(keyword, line, self.get_current_line_number(), self.story, self.story.scene_info.variable_table))
            if new_loc:
                self.set_new_loc(new_loc)

    def next_line(self) -> None | int:
        if self.loc < self.story.scene_info.line_indexes["EOF"] + 1:
            self.loc += 1
        else:
            # End of file
            self.loc = 0
            return -1

    def run_scene(self):
        while True:
            if self.step() == -1:
                return -1

    def step(self):
        self.handle_keyword(self.get_current_keyword(), self.get_current_line())
        return self.next_line()

    def validate_story(self):
        for scene in range(len(self.story.scenes)):
            self.story.cached_scenes[scene] = self.get_file_scene_info(self.story.scenes[scene])
        self.story.scene_info = None

    def run(self):
        self.validate_story()

        # initial scene
        scene_info = self.story.get_scene(0)
        if isinstance(scene_info, SceneInfo):
            self.set_scene(scene_info)
        else:
            self.set_scene(self.get_file_scene_info(scene_info))

        # execute scene and then move onto next
        while True:
            if self.run_scene() == -1:
                break
