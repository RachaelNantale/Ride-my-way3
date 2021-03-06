import unittest
import os
import json
from app import create_app
from tests.BaseTest import BaseTest


class TestClass(BaseTest):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.userlist = {'username': 'Rachael', 'email': 'rachael@sample.com',
                         'password': '123abc', 'phone': '0708999000'}
        self.loginlist = {'username': 'Rachael', 'password': '123abc'}
        

    def test_sigin_user(self):
        """Test API if a user already exists"""
        res = self.client().post('/api/v1/auth/signup', data=self.userlist)
        self.assertEqual(res.status_code, 400)
        self.assertIn(' "Message": "User Not Created."', str(res.data))

    def test_right_user_logged_in(self):
        self.client().post('/api/v1/auth/signup',
                           content_type='application/json',
                           data=json.dumps(self.userlist))
        res = self.client().post('/api/v1/auth/login',
                                 content_type='application/json',
                                 data=json.dumps(self.loginlist))
        reply = res.data.decode()
        self.assertEqual(res.status_code, 200)
        self.assertIn('"User not found. Please sign up"', str(reply))

    def test_if_symbols_are_input(self):
        """ Test whether the client has input data"""
        res = self.client().post('/api/v1/auth/signup',
                                 data={'username': '@!#$$',
                                       'email': 'rachael@sample.com',
                                       'password': '123abc', 'phone': '0708999000'})
        print(res)
        self.assertEqual(res.status_code, 400)
        self.assertIn('"Please  donot use symbols"', str(res.data))

    def test_if_fields_left_blank(self):
        """ Test whether the client has input data"""
        res = self.client().post('/api/v1/auth/signup',
                                 data={'username': ' ',
                                       'email': 'rachael@sample.com',
                                       'password': '123abc', 
                                       'phone': '0708999000'})
        print(res)
        self.assertEqual(res.status_code, 400)
        self.assertIn("User Not Created", str(res.data))

    def test_if_ride_data_is_input(self):
        """Test whether the symbols have been input"""
        res = self.client().post('/api/v1/rides',
                                 data=json.dumps(self.userlist))
        print(res)
        self.assertEqual(res.status_code, 400)
        self.assertIn('No driver provided', str(res.data))

    def test_for_wrong_url(self):
        """Test whether the right url has been input"""
        res = self.client().post('/api/v1/rides/',
                                 data=json.dumps(self.userlist))
        self.assertEqual(res.status_code, 404)
        # self.assertIn('404 Not Found ', str(res.data))

    def test_api_can_get_by_id(self):
        """Test API can get a single ride by using it's id."""
        res = self.client().post('/api/v1/rides', data=json.dumps(self.userlist))
        self.assertEqual(res.status_code, 400)
        print(res)
        result_in_json = json.loads(
            res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/api/v1/rides/<string:id>'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Rachael', str(result.data))

    
if __name__ == "__main__":
    unittest.main()
