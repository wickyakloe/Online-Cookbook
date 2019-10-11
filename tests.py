import unittest
import os
from app import *


class tests_Flask_application(unittest.TestCase):

    ############################
    # setup and teardown #
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['MONGO_URI'] = os.getenv("MONGO_URI")
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    # Helper methods
    def register(self, username, display_name, country, password):
        return self.app.post(
            '/register',
            data=dict(username=username, display_name=display_name,
                      country=country, password=password),
            follow_redirects=True)

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    # Tests
    def test_valid_user_registration(self):
        """Test if the user can register.
        If successfull they are redirected to
        createrecipe.html where there is
        hidden input with the username
        """
        response = self.register('testUser', 'testUserDN',
                                 'testCRY', 'TestPass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testUser', response.data)

    def test_valid_user_login(self):
        """Test if user can login
        and redirect to them to
        myrecipes.html
        """
        response = self.login('testUser', 'TestPass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipes created by:' and b'testUser', response.data)

    def test_invalid_user_login(self):
        """Test if user cant login
        and flash message
        """
        response = self.login('testUser', 'InvalidPass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username and or password', response.data)

    def test_main_page(self):
        """Test if mainpage is
        presented to all users.
        This redirects to /recipe
        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_myrecipes_page(self):
        """Test if myrecipes.html
        is accessible to anonymous users
        """
        response = self.app.get('/recipe/my_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_myrecipes_page_loggedin(self):
        """Test if myrecipes.html
        is accessible to loggedin users
        """
        self.login('testUser', 'TestPass')
        response = self.app.get('/recipe/my_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipes created by:' and b'testUser', response.data)

    def test_show_page(self):
        """Test if recipe.html
        is accessible to all users.
        Note that the ObjectId used is fictional
        """
        recipe_id = ObjectId("5d8359843a5f1a53eb5885b5")
        response = self.app.get('/recipe/{}'.format(recipe_id),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        """Test if createrecipe.html
        is accessible to anonymous users
        """
        response = self.app.get('/recipe/create', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_create_page_loggedin(self):
        """Test if createrecipe.html
        is accessible to loggedin users
        """
        self.login('testUser', 'TestPass')
        response = self.app.get('/recipe/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testUser', response.data)

    def test_edit_page(self):
        """Test if editrecipe.html
        is accessible to anonymous users.
        Note that the ObjectId used is fictional
        """
        recipe_id = ObjectId("5d8359843a5f1a53eb5885b5")
        response = self.app.get('/recipe/edit/{}'.format(recipe_id),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_edit_page_loggedin(self):
        """Test if editrecipe.html
        is accessible to loggedin users.
        Note that the ObjectId used is fictional
        """
        self.login('testUser', 'TestPass')
        recipe_id = ObjectId("5d8359843a5f1a53eb5885b5")
        response = self.app.get('/recipe/edit/{}'.format(recipe_id),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testUser', response.data)

    def test_delete_page(self):
        """Test if anoymous users
        are able to delete recipes.
        Note that the ObjectId used is fictional
        """
        recipe_id = ObjectId("5d8359843a5f1a53eb5885b5")
        response = self.app.get('/recipe/delete/{}'.format(recipe_id),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_page_loggedin(self):
        """Test if loggedin users
        are able to delete recipes.
        Note that the ObjectId used is fictional
        """
        self.login('testUser', 'TestPass')
        recipe_id = ObjectId("5d8359843a5f1a53eb5885b5")
        response = self.app.get('/recipe/delete/{}'.format(recipe_id),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        """Test if dashboard is accessible
        to all users
        """
        response = self.app.get('/recipe/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
