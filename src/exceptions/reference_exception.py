from . import ExceptionContext, StoryException, report_error_info


class ReferenceException(StoryException):
    """Base class for reference exceptions raised by YOU-are-the-hero."""


class LocationNotFoundException(ReferenceException):
    """Exception raised for when a GOTO is used for a location that cannot be found."""

    def __init__(self, exception_context: ExceptionContext, location: str):
        self.message = f"Cannot find the referenced location: {location}"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
