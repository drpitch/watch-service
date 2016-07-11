import unittest
from watcher import WatchService, Configuration

class TestWatchService(unittest.TestCase):
    class TestNotifier(unittest.TestCase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.count = 0

        def notify(self, line):
            self.assertIn(line, ["hello", "goooodbye"])
            self.count += 1

    def setUp(self):
        self.config = Configuration("test_settings.json")

    def test_notification(self):
        test = self.TestNotifier()
        self.config.notifiers.append(test)
        watcher = WatchService(self.config)
        watcher.run(["goooodbye", "hello", "I see trees of green"])
        self.assertEqual(test.count, 2)

    def test_no_notification(self):
        test = self.TestNotifier()
        self.config.notifiers.append(test)
        watcher = WatchService(self.config)
        watcher.run(["hi", "Red roses too"])
        self.assertEqual(test.count, 0)

if __name__ == "__main__":
    unittest.main()
