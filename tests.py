from unittest import TestCase
from model import Neighborhood, Service, User, FavPlace, connect_to_db, db, example_data
from server import app
import server

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Welcome", result.data)

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Welcome", result.data)
        self.assertIn('Mission', result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/logged-in", 
                                  data={"email": "jill@gmail.com", "password": "easy"},
                                  follow_redirects=True)
        self.assertIn("logged in", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()