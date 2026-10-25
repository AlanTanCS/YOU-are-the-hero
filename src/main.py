from parser import parse_entry_point
from story import Story, SceneInfo
from story_engine import StoryEngine

import sys
import os

def handle_arguments():
    path = ""
    if len(sys.argv) > 2:
        print(r"YOU-are-the-hero: error: too many arguments")
        print(r"Usage: YOU-are-the-hero [<entry-file>]")
    elif len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = r"entry.txt"

    return os.path.join(os.getcwd(), path)

def find_entry_file(file_path):
    if not os.path.isfile(file_path):
        print(f"YOU-are-the-hero: error: entry file '{file_path}' not found")
        print(r"Usage: YOU-are-the-hero [<entry-file>]")
        print(r"Specify a valid entry file path or create 'entry.txt' in the working directory.")
        sys.exit()
    return file_path

def main():
    entry = handle_arguments()
    SAVE_PATH = find_entry_file(entry)
    scenes, combats = parse_entry_point(SAVE_PATH)
    story = Story(scenes, combats)
    story_engine = StoryEngine(story)
    story_engine.run()

if __name__ == "__main__":
    main()