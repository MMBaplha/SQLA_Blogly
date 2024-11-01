import unittest
from app import app, db, User

class UserModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a test client and a test database."""

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()
            user = User(first_name="Test", last_name="User", image_url="")
            db.session.add(user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test database."""

        with app.app_context():
            db.drop_all()

    def test_home_redirect(self):
        """Test the home route redirects to /users."""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertIn(b'/users', response.location)  # Should redirect to /users

    def test_list_users(self):
        """Test the list users route."""

        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)  # Should succeed 200
        self.assertIn(b'Test User', response.data)  # Check for the test user's name

    def test_add_user_page(self):
        """Test the add user form page."""

        response = self.client.get('/user/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add User', response.data) 

    def test_user_detail_page(self):
        """Test the user detail page."""

        user = User.query.first()
        response = self.client.get(f'/user/{user.id}')
        self.assertEqual(response.status_code, 200) 
        self.assertIn(b'Test User', response.data)  

if __name__ == '__main__':
    unittest.main()
