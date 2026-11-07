from . import ExceptionContext, StoryException, report_error_info


class ReferenceException(StoryException):
    """Base class for reference exceptions raised by YOU-are-the-hero."""


class LocationNotFoundException(ReferenceException):
    """Exception raised for when a GOTO is used for a location that cannot be found."""

    def __init__(self, exception_context: ExceptionContext, location: str) -> None:
        self.message = f"Cannot find the referenced location: {location}"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)


class ScenesNotFoundException(ReferenceException):
    """Exception raised for when scenelist is empty."""

    # scenes are not found there is no location to report this
    def __init__(self) -> None:
        self.message = (
            "Cannot find any scenes, have you included a scene list in the entry file?"
        )
        super().__init__(self.message)


class NamespaceNotFoundException(ReferenceException):
    """Exception raised when a namespace cannot be resolved."""

    def __init__(
        self,
        exception_context: ExceptionContext,
        namespace: str,
    ) -> None:
        self.message = f"Cannot find the referenced namespace: {namespace}"
        self.message += report_error_info(exception_context)
        super().__init__(self.message)
