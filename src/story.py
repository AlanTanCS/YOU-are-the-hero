class Story():
    def __init__(self, line_indexes, node_table):
        self.line_indexes = line_indexes
        self.node_table = node_table

    def get_line(self, line_number: int) -> str | None:
        return self.line_indexes.get(line_number)
