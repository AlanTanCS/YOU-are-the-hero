from parser import parse_story
from story import Story
from story_engine import StoryEngine

SAVE_PATH = r"tests/System Test/Data/Basic Story2.txt"
KEY_WORDS = r"src\keywords.txt"

def main():
    line_indexes, node_table = parse_story(KEY_WORDS, SAVE_PATH)
    story = Story(line_indexes, node_table)
    story_engine = StoryEngine(story)
    story_engine.next_line()
    story_engine.run()
    print(story.line_indexes)

if __name__ == "__main__":
    main()