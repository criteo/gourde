import unittest

from gourde import testutils
from example import app


class AppTest(unittest.TestCase):
    """Very basic tests."""

    def setUp(self):
        testutils.setup(app.gourde)
        self.app = app.app.test_client()

    def test_views(self):
        rv = self.app.get("/")
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get("/example")
        self.assertEqual(rv.status_code, 200)

    def test_gourde_views(self):
        """Test generic views, just for fun."""
        rv = self.app.get("/-/")
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get("/-/threads")
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get("/-/ready")
        self.assertEqual(rv.status_code, 200)


if __name__ == "__main__":
    unittest.main()
