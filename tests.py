from unittest import TestCase
from model import Neighborhood, Service, User, FavPlace, connect_to_db, db, example_data
from server import app
import server
#where is the appropriate place to make example example_data

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Welcome", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()