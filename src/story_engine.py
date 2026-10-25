from keyword_handlers import handle_keyword as handle
from line_context import LineContext
from parser import parse_scene
from story import Story, SceneInfo

import sys
import os

class StoryEngine:
    def __init__ (self, story: Story):
        self.loc = 0
        self.scene_number = 0
        self.story = story

    def set_current_file(self, file_name: str):
        file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)

        line_indexes, node_table, variable_table = parse_scene(file_path)
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

    def handle_keyword(self, keyword: str, line: str) -> None:
        # keyword will be None if we're looking at a line thats empty
        if keyword:
            new_line = handle(LineContext(keyword, line, self.get_current_line_number(), self.story, self.story.scene_info.variable_table))
            if new_line:
                self.set_current_line_number(new_line)

    def next_line(self) -> None | int:
        if self.loc < self.story.scene_info.line_indexes["EOF"] + 1:
            self.loc += 1
        else:
            # End of file
            self.loc = 0
            return -1

    def step(self):
        self.handle_keyword(self.get_current_keyword(), self.get_current_line())
        return self.next_line()

    def run_scene(self):
        while True:
            if self.step() == -1:
                break

    def validate_story(self):
        for scene_number, scene in self.story.scenes.items():
            self.story.cached_scenes[scene_number] = self.set_current_file(scene)
        self.story.scene_info = None

    def run(self):
        self.validate_story()

        # initial scene
        scene_info = self.story.get_scene(self.scene_number)
        if type(scene_info) is SceneInfo:
            self.story.scene_info = scene_info
        else:
            self.story.scene_info = self.set_current_file(scene_info)

        # execute scene and then move onto next
        while True:
            self.run_scene()
            self.scene_number += 1
            if self.scene_number not in self.story.scenes:
                break
            scene_info = self.story.get_scene(self.scene_number)
            if type(scene_info) is SceneInfo:
                self.story.scene_info = scene_info
            else:
                self.story.scene_info = self.set_current_file(scene_info)
