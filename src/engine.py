from node_handlers.scene_handler import handle as handle_scene
from node_handlers.decision_handler import handle as handle_decision
from node_handlers.combat_handler import handle as handle_combat

import json_reader
import node_types

SAVE_PATH = "tests/System Test/Data/Basic Story.json"

class StoryEngine:
    def __init__ (self, story):
        self.story = story
        self.current_index = 0

    def current_node_name(self) -> str:
        return self.story.nodes[self.current_index]

    def current_node(self) -> dict:
        return self.story.data[self.current_node_name()]

    def process_current_node(self) -> None:
        current_node_name = self.current_node_name()[:-1]

        handlers = { node_types.NodeType.SCENE: handle_scene,
                     node_types.NodeType.DECISION: handle_decision,
                     node_types.NodeType.COMBAT: handle_combat }

        handler = handlers[node_types.NodeType(current_node_name)]
        next_node_name = handler(self.current_node())

        # we need to go to a different node
        if next_node_name is not None:
            # increment by 1 after processing so go to scene before
            self.current_index = self.story.node_indexes[next_node_name] - 1

    def run(self) -> None:
        while self.current_index < len(self.story.nodes):
            self.process_current_node()
            self.current_index += 1
            json_reader.update_current_node(SAVE_PATH, self.current_index)

def main():
    story = json_reader.read_json(SAVE_PATH)
    story_engine = StoryEngine(story)
    story_engine.run()


if __name__ == "__main__":
    main()
