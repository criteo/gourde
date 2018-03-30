import unittest
from example import app


class AppTest(unittest.TestCase):

    """Very basic tests."""

    def test_app(self):
        self.assertIsNotNone(app.app)
        # TODO: start main and send a SIGKILL from a thread.


if __name__ == '__main__':
    unittest.main()
