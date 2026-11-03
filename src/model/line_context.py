class LineContext:
    def __init__(
        self, keyword, line, exception_context, story, variable_table, global_variables
    ):
        self.keyword = keyword
        self.line = line
        self.story = story
        self.variable_table = variable_table
        self.global_variables = global_variables
        self.exception_context = exception_context
