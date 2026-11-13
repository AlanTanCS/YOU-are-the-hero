from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.ast_nodes.entry import EntryStatement
    from model.ast_nodes.scene import SceneStatement


class ASTNode:
    # AST Node base class. Each one of these nodes represents a node on our abstract syntax tree.
    pass


@dataclass
class EntryFile(ASTNode):
    entry_statement: list[EntryStatement]


@dataclass
class SceneFile(ASTNode):
    entry_statement: list[SceneStatement]


@dataclass
class Story(ASTNode):
    entry_file: EntryFile
    scene_files: list[SceneFile]
