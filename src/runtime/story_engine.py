import os
from pathlib import Path

from exceptions import ExceptionContext
from model.ast_nodes import ASTNode, SceneFile
from model.context import StatementExecutionContext, StatementSemanticContext
from model.story import SceneInfo, Story
from model.syntax import Namespace
from parser import parse_scene
from runtime.handle_keyword import handle_keyword as handle
from scanner import scan_story_file
from semantic.declaration_analyser import DeclarationAnalyzer
from semantic.dispatcher import SemanticDispatcher


class StoryEngine:
    def __init__(self, story: Story) -> None:
        self.statement_number = 0
        self.story = story

    def set_scene(self, scene_info: SceneInfo) -> None:
        self.story.scene_info = scene_info
        self.statement_number = 0

    def set_line(self, new_line):
        self.statement_number = new_line

    def handle_statement(self, statement: ASTNode) -> int | str | None:
        if statement.file is None:
            raise RuntimeError("Internal error: Statement has no associated file")
        exception_context = ExceptionContext(statement.file, statement.line_number)
        execution_context = StatementExecutionContext(
            exception_context, self.story, statement, handle
        )
        return handle(execution_context)

    def next_line(self) -> None | int:
        if self.story.scene_info is None:
            raise RuntimeError("Internal error: No active scene set")
        self.statement_number += 1
        if self.statement_number >= len(self.story.scene_info.statements):
            return -1

    def step(self) -> None | int:
        if self.story.scene_info is None:
            raise RuntimeError("Internal error: No active scene set")
        result = self.handle_statement(
            self.story.scene_info.statements[self.statement_number]
        )
        if isinstance(result, int):
            self.set_line(result)
        elif isinstance(result, str):
            self.set_scene(self.story.get_scene(result))
        else:
            return self.next_line()

    def run_entry(self) -> None:
        entry_file = self.story.ast_tree.entry_file
        assert entry_file.file, "Internal Error: File not set"
        self.story.scene_info = SceneInfo(
            Path(entry_file.file).stem, entry_file.entry_statements, {}, {}
        )

        # Nothing to do...
        if len(entry_file.entry_statements) == 0:
            return

        while True:
            if self.step() == -1:
                self.statement_number = 0
                return

    def run_scene(self) -> None:
        assert self.story.scene_info, "Internal Error: Scene info not set"

        # Nothing to do...
        if len(self.story.scene_info.statements) == 0:
            return

        while True:
            if self.step() == -1:
                self.statement_number = 0
                return

    def run(self) -> None:
        self.run_entry()
        self.validate_story()

        # initial scene
        initial_scene = self.story.get_scene(0)
        self.set_scene(initial_scene)
        self.run_scene()

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
        for scene in self.story.ast_tree.scene_files:
            decl_visitor = DeclarationAnalyzer(
                global_variable_table=self.story.global_variables
            )
            decl_visitor.analyse(scene)

        for scene in self.story.ast_tree.scene_files:
            assert scene.file, "Internal Error: File not set"
            scene_visitor = SemanticDispatcher(StatementSemanticContext())
            scene_visitor.analyse_scene(scene)
            self.story.cached_scenes.append(
                SceneInfo(
                    Path(scene.file).stem,
                    scene.scene_statements,
                    scene_visitor.state.node_table,
                    scene_visitor.state.variable_table,
                )
            )

    def parse_scene(self, file_name: str) -> None:
        file_path = os.path.join(os.getcwd(), f"{file_name}.txt")

        # Scan
        scene_lines = scan_story_file(file_path, Namespace.SCENE)

        # Parse
        parse_scene(scene_lines, file_path, self.story.ast_tree)
