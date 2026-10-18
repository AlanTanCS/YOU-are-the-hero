from parser import parse_story
from story import Story
from story_engine import StoryEngine

SAVE_PATH = r"tests/System Test/Data/Basic Story2.txt"

def main():
    line_indexes, node_table, variables = parse_story(SAVE_PATH)
    story = Story(line_indexes, node_table)
    story_engine = StoryEngine(story, variables)
    story_engine.set_current_line_number(10)
    print(line_indexes[9])
    print(variables)
    # story_engine.set_current_line_number(14)
    # story_engine.step()
    # print(variables)
    # print(story_engine.get_current_line())
    # story_engine.step()
    # print(line_indexes)
    # print(story_engine.variables)
    # story_engine.run()

if __name__ == "__main__":
    main()