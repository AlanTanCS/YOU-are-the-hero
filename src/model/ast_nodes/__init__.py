from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.ast_nodes.entry import EntryStatement
    from model.ast_nodes.scene import SceneStatement


class ASTNode:
    def __init__(self, file: None | str = None, line_number: None | int = None):
        # AST Node base class. Each one of these nodes represents a node on our abstract syntax tree.
        self.file = file
        self.line_number = line_number

    def set_file(self, file: str | None):
        self.file = file

        for value in vars(self).values():
            if isinstance(value, ASTNode):
                value.set_file(file)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        item.set_file(file)

    def set_line_number(self, line_number: int | None):
        self.line_number = line_number

        for value in vars(self).values():
            if isinstance(value, ASTNode):
                value.set_line_number(line_number)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        item.set_line_number(line_number)


@dataclass
class EntryFile(ASTNode):
    entry_statements: list[EntryStatement]


@dataclass
class SceneFile(ASTNode):
    scene_statements: list[SceneStatement]


@dataclass
class StoryNode(ASTNode):
    entry_file: EntryFile
    scene_files: list[SceneFile]
