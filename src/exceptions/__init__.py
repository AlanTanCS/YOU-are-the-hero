import linecache
from dataclasses import dataclass


@dataclass
class ExceptionContext:
    file_path: str
    line_number: int | None = None


class StoryException(Exception):
    """Base class for exceptions raised by YOU-are-the-hero."""

    def __init__(self, message: str):
        self.message = f"{type(self).__name__}: {message}"
        super().__init__(self.message)


def get_line(file: str, line_number: int):
    return linecache.getline(file, line_number).strip()


def report_error_info(exception_context: ExceptionContext):
    err_msg = f"\nIn file: {exception_context.file_path}"

    if exception_context.line_number:
        err_msg += f"\nAt line {exception_context.line_number}"
        err_msg += f": '{get_line(exception_context.file_path, int(exception_context.line_number))}'"

    return err_msg
