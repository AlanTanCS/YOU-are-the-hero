import os
import sys

from exceptions import StoryException
from model.story import Story
from parser import parse_entry_point
from runtime.initialise_global_variables import global_init
from runtime.story_engine import StoryEngine


def handle_arguments() -> str:
    path = ""
    if len(sys.argv) > 2:
        print(r"YOU-are-the-hero: error: too many arguments")
        print(r"Usage: YOU-are-the-hero [<entry-file>]")
    elif len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = r"entry.txt"

    return os.path.join(os.getcwd(), path)


def find_entry_file(file_path: str) -> str:
    if not os.path.isfile(file_path):
        print(f"YOU-are-the-hero: error: entry file '{file_path}' not found")
        print(r"Usage: YOU-are-the-hero [<entry-file>]")
        print(
            r"Specify a valid entry file path or create 'entry.txt' in the working directory."
        )
        sys.exit()
    return file_path


def main() -> None:
    entry = handle_arguments()
    ENTRY_FILE = find_entry_file(entry)
    scenes, combats, global_variable_statements = parse_entry_point(ENTRY_FILE)
    global_variables = global_init(global_variable_statements, ENTRY_FILE)
    story = Story(scenes, combats, global_variables)
    story_engine = StoryEngine(story)
    story_engine.run()


if __name__ == "__main__":
    try:
        main()
    except StoryException as exception:
        RED = "\033[91m"
        RESET = "\033[0m"
        print(f"{RED}{exception}{RESET}")
