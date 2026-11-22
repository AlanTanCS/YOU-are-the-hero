from __future__ import annotations

from typing import TYPE_CHECKING

from model.ast_nodes.entry import EntryAction
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.scene import SceneAction, SceneStatement
from semantic.scene_analyser import SceneSemanticAnalyser

if TYPE_CHECKING:
    from model.context import StatementSemanticContext
from model.ast_nodes import EntryFile, SceneFile
from semantic.entry_analyser import EntrySemanticAnalyser


class SemanticDispatcher:
    def __init__(self, state: StatementSemanticContext):
        self.state = state
        self.state.dispatcher = self

        self.entry_analyser = EntrySemanticAnalyser(self.state)
        self.scene_analyser = SceneSemanticAnalyser(self.state)

    def analyse_entry(self, node: EntryFile):
        self.entry_analyser.analyse(node)

        # Convert raw line to statement number
        line_to_index = {s.line_number: i for i, s in enumerate(node.entry_statements)}

        self.state.node_table = {
            name: line_to_index[line] for name, line in self.state.node_table.items()
        }

    def analyse_scene(self, node: SceneFile | list[SceneStatement]):
        if isinstance(node, list):
            for scene in node:
                self.scene_analyser.analyse(scene)
        else:
            self.scene_analyser.analyse(node)

            # Convert raw line to statement number
            line_to_index = {
                s.line_number: i for i, s in enumerate(node.scene_statements)
            }

            self.state.node_table = {
                name: line_to_index[line]
                for name, line in self.state.node_table.items()
            }

    def analyse_entry_action(self, node: EntryAction):
        self.entry_analyser.analyse(node)

    def analyse_scene_action(self, node: SceneAction):
        self.scene_analyser.analyse(node)

    def analyse_list_statement(self, node: ListStatement):
        pass
