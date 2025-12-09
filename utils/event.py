"""Event handling class.

This class provides a mechanism to manage and trigger events.
It allows adding, removing, and invoking event handlers dynamically.
"""

class Event(object):
    """A class to manage event handlers and trigger events."""

    def __init__(self):
        """Initialize the Event instance with an empty list of event handlers."""
        self.__event_handlers = []

    def __iadd__(self, handler):
        """Add an event handler to the list.

        Args:
            handler (callable): A callable object (e.g., function) to handle the event.

        Returns:
            Event: The current instance to allow chaining.
        """
        self.__event_handlers.append(handler)
        return self

    def __isub__(self, handler):
        """Remove an event handler from the list.

        Args:
            handler (callable): The event handler to remove.

        Returns:
            Event: The current instance to allow chaining.
        """
        self.__event_handlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        """Invoke all registered event handlers with the given arguments.

        Args:
            *args: Positional arguments to pass to the event handlers.
            **keywargs: Keyword arguments to pass to the event handlers.
        """
        for eventhandler in self.__event_handlers:
            eventhandler(*args, **keywargs)
