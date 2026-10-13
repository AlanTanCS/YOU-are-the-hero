from keyword_handlers import handle_keyword as handle
from story import Story

class StoryEngine:
    def __init__ (self, story: Story):
        self.loc = 0
        self.story = story
        self.eof = story.line_indexes["EOF"] + 1

    def get_current_line_number(self) -> int:
        return self.loc + 1

    def set_current_line_number(self, new_value: int) -> None:
        self.loc = new_value - 1

    def get_current_line(self) -> str | None:
        return self.story.get_line(self.loc)
    
    def get_current_keyword(self) -> str:
        current_line = self.get_current_line()
        if current_line:
            return current_line.split()[0]
        else:
            return None

    def handle_keyword(self, keyword: str, line: str) -> None:
        # keyword will be None if we're looking at a line thats empty
        if keyword:
            handle(keyword, line, self.get_current_line_number())

    def next_line(self) -> None | int:
        if self.loc < self.eof:
            self.loc += 1
        else:
            # End of file
            return -1

    def run(self):
        self.handle_keyword(self.get_current_keyword(), self.get_current_line())
        # while True:
        #     self.handle_keyword(self.get_current_keyword(), self.get_current_line())
        #     if self.next_line() == -1:
        #         break
