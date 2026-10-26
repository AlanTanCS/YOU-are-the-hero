class LineContext:
    def __init__(self, keyword, line, loc, story, variable_table, global_variables):
        self.keyword = keyword
        self.line = line
        self.loc = loc
        self.story = story
        self.variable_table = variable_table
        self.global_variables = global_variables
