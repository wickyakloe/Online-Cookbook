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

    def register(self, username, displayname, country, password):
        return self.app.post(
            '/register',
            data=dict(username=username, displayname=displayname, country=country, password=password),
            follow_redirects=True
        )

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_valid_user_registration(self):
        response = self.register('testuser', 'testdisplayname', 'testcountry', 'testpassword')
        self.assertEqual(response.status_code, 200)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_page(self):
        response = self.app.get('/view_recipe/<recipe_id>', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        response = self.app.get('/create_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_page(self):
        response = self.app.get('/edit_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
