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

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_myrecipes_page(self):
        response = self.app.get('/my_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_code, 200)

    def test_show_page(self):
        recipe_id = ObjectId("5d8359843a5f1a53eb5885b5")
        response = self.app.get('/view_recipe/{}'.format(recipe_id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        response = self.app.get('/create_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_code, 200)

    def test_edit_page(self):
        recipe_id = ObjectId("5d8359843a5f1a53eb5885b5")
        response = self.app.get('/edit_recipe/{}'.format(recipe_id), follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
