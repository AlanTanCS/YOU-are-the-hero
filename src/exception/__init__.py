from enum import Enum
import linecache
import syntax

class ExceptionContext():
    def __init__(self, file_path: str = None, line_number: str = None, line: str = None):
        self.file_path = file_path
        self.line_number = line_number
        self.line = line

class StoryException(Exception):
    """Base class for exceptions raised by YOU-are-the-hero."""

def get_line(file: str, line_number: int):
    return linecache.getline(file, line_number).strip()

def report_error_info(exception_context: ExceptionContext):
    err_msg = f"\nIn file: {exception_context.file_path}"

    if exception_context.line_number:
        err_msg += f"\nAt line {exception_context.line_number}"

    if exception_context.line_number and exception_context.line:
        err_msg += f": \'{get_line(exception_context.file_path, int(exception_context.line_number))}\'"

    return err_msg
