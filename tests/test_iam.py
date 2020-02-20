from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import db

import sys
import pytest

class IAMTestCase(BaseTestCase):

    auth = None

    @pytest.mark.run(order=1)
    def test_iam_unauth(self):
        self.fake_user()
        response = self.post('/iam/createRole', {
            "auth": self.jwt,
            "roleName": "Veteran",
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 403)
    

    @pytest.mark.run(order=2)
    def test_iam_login(self):
        response = self.post('/user/login', {
            "email": "admin@polarapp.xyz",
            "password": "password"
        })
        data = response.get_json()
        self.assertIn("auth", data)
        self.__class__.auth = data['auth']
        self.assertEqual(response.status_code, 200)


    def test_iam_auth(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Veteran",
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 200)
    

    def test_iam_missing(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 400)
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Volunteer"
        })
        self.assertEqual(response.status_code, 400)

    
    def test_iam_duplicate(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Veteran",
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 400)
    

    def test_iam_invalid(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Volunteer",
            "permissions": [12,20,30]
        })
        self.assertEqual(response.status_code, 400)