import os
import sys

from exceptions import StoryException
from model.context import StatementSemanticContext
from model.story import Story
from model.syntax import Namespace
from parser import parse_entry
from runtime.story_engine import StoryEngine
from scanner import scan_story_file
from semantic.declaration_analyser import DeclarationAnalyzer
from semantic.dispatcher import SemanticDispatcher


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
    entry_lines = scan_story_file(ENTRY_FILE, Namespace.ENTRY)
    ast_tree = parse_entry(entry_lines, ENTRY_FILE)

    decl_visitor = DeclarationAnalyzer()
    decl_visitor.analyse(ast_tree.entry_file)

    visitor = SemanticDispatcher(StatementSemanticContext())
    visitor.analyse_entry(ast_tree.entry_file)

    story = Story(
        ast_tree,
        visitor.entry_analyser.context.scene_list,
        visitor.entry_analyser.context.combat_list,
        visitor.entry_analyser.context.global_variable_table,
    )
    story_engine = StoryEngine(story)
    story_engine.run()
    # story_engine.run_entry()

    # set_line_and_scene(story_engine, 0, 3)
    # print(story_engine.story.get_active_scene())
    # story_engine.step()
    # print(story_engine.get_current_line())
    # story_engine.run()


if __name__ == "__main__":
    try:
        main()
    except StoryException as exception:
        RED = "\033[91m"
        RESET = "\033[0m"
        print(f"{RED}{exception}{RESET}")
