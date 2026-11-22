import os

from exceptions import ExceptionContext, reference_exception
from model.ast_nodes import ASTNode, SceneFile
from model.context import StatementExecutionContext
from model.story import SceneInfo, Story
from model.story_token import Token
from model.syntax import Namespace
from parser import parse_scene
from runtime.handle_keyword import handle_keyword as handle
from scanner import scan_story_file
from semantic.declaration_analyser import DeclarationAnalyzer
from semantic.scene_analyser import SceneSemanticAnalyser


class StoryEngine:
    def __init__(self, story: Story) -> None:
        self.statement_number = 0
        self.loc = 0
        self.story = story

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

    # def set_new_loc(self, new_loc: int | str) -> None:
    #     if isinstance(new_loc, int):
    #         self.set_current_line_number(new_loc)
    #     else:
    #         self.set_scene(self.story.get_scene(new_loc))

    # def set_scene(self, scene_info: SceneInfo) -> None:
    #     self.loc = 0
    #     self.story.scene_info = scene_info

    # def handle_keyword(self, keyword: Token | None, line: list[Token]) -> None:
    #     # keyword will be None if we're looking at a line thats empty
    #     if keyword is None:
    #         return

    #     exception_context = ExceptionContext(
    #         self.story.get_active_scene().file_path, self.get_current_line_number()
    #     )
    #     new_loc = handle(
    #         StatementExecutionContext(
    #             exception_context,
    #             keyword,
    #             line,
    #             self.story,
    #             self.story.get_active_scene().variable_table,
    #             handle,
    #         )
    #     )
    #     if isinstance(new_loc, (int, str)):
    #         self.set_new_loc(new_loc)

    def handle_statement(self, statement: ASTNode) -> None:
        if statement.file is None:
            raise RuntimeError("Internal error: Statement has no associated file")
        exception_context = ExceptionContext(statement.file, statement.line_number)
        execution_context = StatementExecutionContext(
            exception_context, self.story, statement, handle
        )
        handle(execution_context)

    def next_line(self) -> None | int:
        if self.story.scene_info is None:
            raise RuntimeError("Internal error: No active scene set")
        self.statement_number += 1
        if self.statement_number >= len(self.story.scene_info.line_indexes):
            return -1

    def step(self) -> None | int:
        if self.story.scene_info is None:
            raise RuntimeError("Internal error: No active scene set")

        self.handle_statement(self.story.scene_info.line_indexes[self.statement_number])
        return self.next_line()

    def run_entry(self) -> None:
        entry_file = self.story.ast_tree.entry_file
        self.story.scene_info = SceneInfo(entry_file.entry_statements, {}, {})

        # Nothing to do...
        if len(entry_file.entry_statements) == 0:
            return

        while True:
            if self.step() == -1:
                return

    def run_scenes(self) -> None:
        while True:
            if self.step() == -1:
                return

    def run(self) -> None:
        self.run_entry()
        self.validate_story()
        # # initial scene
        # initial_scene = self.story.get_scene(0)
        # if isinstance(initial_scene, SceneInfo):
        #     self.set_scene(initial_scene)
        # else:
        #     self.set_scene(self.get_file_scene_info(initial_scene))

        # # execute scene and then move onto next
        # while True:
        #     if self.run_scene() == -1:
        #         break

    def validate_story(self) -> None:
        """Parses all scenes declared in entry and caches the AST, and symbol tables"""

        # Scan and parse
        for scene in self.story.scenes:
            self.parse_scene(scene)

        # Semantic analysis
        decl_visitor = DeclarationAnalyzer()
        for scene in self.story.ast_tree.scene_files:
            decl_visitor.analyse(scene)

        # scene_visitor = SceneSemanticAnalyser(
        #     decl_visitor.global_variable_table, [], [], {}
        # )
        # scene_visitor.analyse(self.story.ast_tree.scene_files)

    def parse_scene(self, file_name: str) -> SceneFile:
        file_path = os.path.join(os.getcwd(), f"{file_name}.txt")

        # Scan
        scene_lines = scan_story_file(file_path, Namespace.SCENE)

        # Parse
        scene_file = parse_scene(scene_lines, file_path, self.story.ast_tree)

        return scene_file
