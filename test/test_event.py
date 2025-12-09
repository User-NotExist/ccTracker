import unittest
from utils.event import Event

class TestEvent(unittest.TestCase):
    def test_adds_handler_and_invokes_it(self):
        event = Event()
        result = []

        def handler(arg):
            result.append(arg)

        event += handler
        event("test")
        self.assertEqual(result, ["test"])

    def test_removes_handler_and_does_not_invoke_it(self):
        event = Event()
        result = []

        def handler(arg):
            result.append(arg)

        event += handler
        event -= handler
        event("test")
        self.assertEqual(result, [])

    def test_handles_multiple_handlers(self):
        event = Event()
        result = []

        def handler1(arg):
            result.append(f"handler1-{arg}")

        def handler2(arg):
            result.append(f"handler2-{arg}")

        event += handler1
        event += handler2
        event("test")
        self.assertEqual(result, ["handler1-test", "handler2-test"])

    def test_raises_error_when_removing_nonexistent_handler(self):
        event = Event()

        def handler(arg):
            pass

        with self.assertRaises(ValueError):
            event -= handler

    def test_supports_passing_multiple_arguments(self):
        event = Event()
        result = []

        def handler(arg1, arg2):
            result.append((arg1, arg2))

        event += handler
        event("arg1", "arg2")
        self.assertEqual(result, [("arg1", "arg2")])

    def test_supports_passing_keyword_arguments(self):
        event = Event()
        result = []

        def handler(**kwargs):
            result.append(kwargs)

        event += handler
        event(key1="value1", key2="value2")
        self.assertEqual(result, [{"key1": "value1", "key2": "value2"}])


if __name__ == "__main__":
    unittest.main()
